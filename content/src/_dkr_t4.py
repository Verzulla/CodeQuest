"""Теория модуля «Docker на практике» темы «Docker для тестировщика»: Docker Hub, образ изнутри
и свой образ, Docker в Docker, Docker в CI.

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- dkr-hub ----------
'dkr-hub': dict(
    full=t(r'''
## Зачем это нужно

Почти каждый Dockerfile начинается с `FROM чужой-образ`, а почти каждый стенд — с `image: postgres:16`. Эти образы скачиваются с **Docker Hub** — главного публичного реестра. Тестировщику нужно уметь найти там нужный образ, выбрать правильный тег, отличить надёжный образ от случайного и выложить свой — чтобы коллеги и CI запускали автотесты одной командой.

## Что такое Docker Hub

- **Docker Hub** (hub.docker.com) — реестр по умолчанию: если в имени образа не указан реестр, Docker идёт туда. `postgres:16` = `docker.io/library/postgres:16`.
- Образы лежат в **репозиториях**. У репозитория есть владелец (пользователь или организация) и набор **тегов**.
- `library/` — пространство **официальных образов**: `python`, `postgres`, `nginx`, `redis`. Их префикс можно не писать.
- Образ пользователя или компании: `anna/my-tests`, `selenium/standalone-chrome`. Здесь префикс — обязательная часть имени.

```bash
docker pull python:3.12-slim          # = docker.io/library/python:3.12-slim
docker pull anna/my-tests:1.0         # = docker.io/anna/my-tests:1.0
docker pull ghcr.io/acme/tests:1.0    # другой реестр — Docker Hub ни при чём
```

## Каким образам доверять

На странице образа в Hub есть значки:

- **Docker Official Image** — официальные образы: их собирают по открытым Dockerfile, регулярно обновляют и проверяют на уязвимости. Первый выбор для базового образа.
- **Verified Publisher** — образ от проверенной компании (например, от разработчиков самого продукта).
- **Sponsored OSS** — открытый проект, который поддерживает Docker.

Образ без значков от неизвестного автора может содержать что угодно, в том числе майнер или кражу секретов. В CI, где у job-а есть токены, это особенно опасно. Смотри на значок, число скачиваний, дату обновления и ссылку на исходный Dockerfile.

```bash
docker search --filter is-official=true python   # поиск только среди официальных
```

## Варианты тегов

У популярных образов много тегов на одну версию. На примере `python`:

| Тег | Что внутри | Размер |
|---|---|---|
| `3.12` | полный Debian с компиляторами и утилитами | ~1 ГБ |
| `3.12-slim` | урезанный Debian, только нужное для Python | ~130 МБ |
| `3.12-alpine` | Alpine Linux (musl вместо glibc) | ~50 МБ |
| `3.12-slim-bookworm` | slim на конкретной версии Debian (bookworm) | ~130 МБ |

- Для автотестов обычно берут **`-slim`**: маленький и совместимый со всеми pip-пакетами.
- **`alpine`** самый маленький, но использует другую стандартную библиотеку C (musl). Часть пакетов с C-кодом не найдёт готовой сборки и начнёт компилироваться, а то и не соберётся. Экономия места оборачивается долгой сборкой и странными ошибками.
- Тег с именем ОС (`-bookworm`) фиксирует ещё и версию системы: обновление Debian не сломает сборку внезапно.
- Для UI-тестов есть готовые образы с браузерами — например, официальный образ Playwright от Microsoft `mcr.microsoft.com/playwright/python:v1.48.0-noble`. Он лежит в реестре Microsoft (`mcr.microsoft.com`), а не в Docker Hub.

## Один тег — несколько платформ

Один и тот же тег `python:3.12-slim` содержит сборки под разные процессоры: `linux/amd64` (обычные серверы и CI), `linux/arm64` (Mac на Apple Silicon). Docker сам скачивает подходящую. Если нужна чужая платформа — например, воспроизвести ошибку CI на Mac — укажи её явно:

```bash
docker run --rm --platform linux/amd64 python:3.12-slim python -c "import platform; print(platform.machine())"
```

## Лимиты на скачивание

Docker Hub ограничивает число скачиваний образов: у анонимных запросов лимит в час с одного IP небольшой, у вошедших пользователей — заметно больше (точные цифры Docker периодически меняет — смотри docs.docker.com). В CI много job-ов ходят с одного IP, и лимит кончается быстро. Симптом — ошибка:

```bash
toomanyrequests: You have reached your pull rate limit.
```

Что делают:

- в CI **логинятся** в Docker Hub перед скачиванием (токеном, см. ниже);
- кэшируют образы или держат копии в своём реестре (зеркало, ghcr.io, корпоративный Nexus или Harbor);
- не скачивают одно и то же в каждом шаге.

## Свой образ в Docker Hub

1. Зарегистрироваться на hub.docker.com — имя пользователя станет префиксом образов (`anna/...`).
2. Создать **токен доступа**: Account settings → Personal access tokens. Пароль от аккаунта в CI не используют — токен можно ограничить правами (только чтение) и отозвать.
3. Войти и отправить образ:

```bash
echo "$DOCKERHUB_TOKEN" | docker login -u anna --password-stdin
docker tag my-tests anna/my-tests:1.0      # второе имя с префиксом пользователя
docker push anna/my-tests:1.0
```

- `--password-stdin` читает токен из ввода: он не попадёт в историю команд и в список процессов.
- Публичный репозиторий может скачать кто угодно — **никаких секретов в образе** (паролей, `.env`, ключей). Приватных репозиториев на бесплатном плане мало.
- После `push` образ доступен на любой машине: `docker pull anna/my-tests:1.0`.

## Итог

- Docker Hub — реестр по умолчанию; `library/` — официальные образы.
- Доверяй значкам Official Image и Verified Publisher, смотри на исходный Dockerfile.
- Для тестов — `-slim`; `alpine` маленький, но с подвохами; тег с ОС фиксирует систему.
- Один тег — несколько платформ; `--platform` выбирает нужную.
- Лимиты скачиваний: в CI логинься и кэшируй.
- Свой образ: токен → `docker login --password-stdin` → `tag пользователь/имя:тег` → `push`.
'''),
    short=t(r'''
```bash
docker pull python:3.12-slim                 # = docker.io/library/python:3.12-slim
docker search --filter is-official=true python
docker run --platform linux/amd64 ...        # чужая платформа
echo "$DOCKERHUB_TOKEN" | docker login -u anna --password-stdin
docker tag my-tests anna/my-tests:1.0
docker push anna/my-tests:1.0
```

- Официальные — `library/`, значки Official Image и Verified Publisher.
- `-slim` — для тестов; `alpine` — musl, сборка пакетов может сломаться.
- `toomanyrequests` — лимит скачиваний: логинься, кэшируй, держи зеркало.
- В публичном образе — никаких секретов.
'''),
    quiz=[
        q('Какое полное имя у образа `redis:7`?',
            ['redis:7', 'docker.io/redis/redis:7', 'docker.io/library/redis:7', 'hub.docker.com/redis:7'],
            2, 'Реестр по умолчанию — docker.io, официальные образы — в library/.'),
        q('Почему для автотестов чаще берут `python:3.12-slim`, а не `python:3.12-alpine`?',
            ['alpine не поддерживает Python 3.12', 'В alpine другая библиотека C (musl): часть пакетов не найдёт готовой сборки и будет компилироваться или упадёт', 'slim меньше alpine', 'alpine платный'],
            1, 'slim немного больше, зато совместим со всеми pip-пакетами.'),
        q('В CI скачивание образов падает с `toomanyrequests`. Что помогает?',
            ['Использовать тег latest', 'Войти в Docker Hub токеном и кэшировать или зеркалировать образы', 'Добавить --no-cache', 'Перезапустить job'],
            1, 'У вошедших лимит выше, а кэш и зеркало убирают лишние скачивания.'),
    ],
),

# ---------- dkr-image ----------
'dkr-image': dict(
    full=t(r'''
## Зачем это нужно

Мы уже писали Dockerfile по частям. Теперь соберём картину целиком: из чего физически состоит образ, почему контейнер «забывает» изменения и как с нуля написать хороший образ для своих автотестов — такой, который запускается одной командой, принимает параметры и не работает от root.

## Образ изнутри

Образ — это не один файл, а набор частей:

- **Слои** — архивы изменений файловой системы, только для чтения. Каждая инструкция `RUN`, `COPY`, `ADD` даёт слой.
- **Конфигурация** — то, что не файлы: `ENV`, `WORKDIR`, `USER`, `ENTRYPOINT`, `CMD`, открытые порты, метки.
- **Манифест** — список слоёв и ссылка на конфигурацию. Его хеш — **дайджест** образа (`sha256:…`). Изменился хоть байт — изменился дайджест.

Слои **общие** между образами: если два образа начинаются с `FROM python:3.12-slim`, базовые слои скачаются и займут место на диске один раз.

```bash
docker image ls                                  # образы, их размер и ID
docker history my-tests                          # слои и какая инструкция их создала
docker image inspect my-tests                    # конфигурация и слои в JSON
docker image inspect --format '{{.Config.Entrypoint}} {{.Config.Cmd}}' my-tests
```

## Контейнер = образ + слой для записи

Когда контейнер запускается, Docker кладёт поверх слоёв образа ещё один — тонкий **слой для записи**. Все изменения (новые файлы, отчёты, логи) попадают туда. Чтение идёт сверху вниз: файл берётся из самого верхнего слоя, где он есть. Удаление файла из нижнего слоя — это пометка «удалён» в верхнем; сам нижний слой не меняется.

Отсюда два важных следствия:

- **Удалили контейнер — потеряли всё, что он записал.** Отчёты тестов надо выносить наружу через том (`-v ./reports:/app/reports`).
- **Образ не меняется от запуска.** Хоть сто прогонов — каждый начнёт с одинакового чистого состояния. Именно это и нужно тестам.

Есть команда `docker commit` — сохранить изменённый контейнер как образ. Для работы она не годится: никто не узнает, что внутри поменяли руками, и повторить это нельзя. Образ всегда описывают Dockerfile-ом.

## Свой образ для автотестов: шаг за шагом

Проект:

```bash
tests-project/
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── pytest.ini
└── tests/
    └── test_api.py
```

Dockerfile:

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /tests

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home tester
USER tester

ENTRYPOINT ["pytest"]
CMD ["-v"]
```

Разбор решений:

- `FROM python:3.12-slim` — официальный образ, маленький и совместимый.
- `PYTHONDONTWRITEBYTECODE=1` — не создавать `.pyc`; `PYTHONUNBUFFERED=1` — печатать вывод сразу, без буфера, иначе логи в CI приходят пачками или теряются при падении.
- Зависимости — **до** кода (кэш слоёв, урок «Dockerfile и слои»). `--no-cache-dir` — не хранить в образе кэш pip.
- `useradd` + `USER tester` — тесты работают **не от root**. Если в коде или зависимости найдётся уязвимость, у процесса будет меньше прав.
- `ENTRYPOINT ["pytest"]` — контейнер **и есть** pytest. `CMD ["-v"]` — аргументы по умолчанию, их заменяет то, что передали в `docker run`.

## Сборка, запуск, параметры

```bash
docker build -t my-tests:1.0 .
docker run --rm my-tests:1.0                              # pytest -v
docker run --rm my-tests:1.0 -m smoke                     # pytest -m smoke
docker run --rm -e BASE_URL=https://stage.example.com my-tests:1.0
docker run --rm -v "$PWD/reports:/tests/reports" my-tests:1.0 --junitxml=reports/junit.xml
docker run --rm --entrypoint bash -it my-tests:1.0        # зайти внутрь и осмотреться
```

- Аргументы после имени образа заменяют `CMD` и дописываются к `ENTRYPOINT`.
- `--entrypoint` подменяет сам `ENTRYPOINT` — и **сбрасывает** `CMD` образа. Удобно для отладки: открыть оболочку вместо тестов.
- Адрес стенда, браузер, токены — через `-e`, а не внутри образа: один образ гоняют на разных стендах.

## Метки и перенос без реестра

```dockerfile
LABEL org.opencontainers.image.source="https://github.com/acme/shop-tests"
```

Метка `org.opencontainers.image.source` связывает образ с репозиторием: GitHub по ней показывает пакет на странице репозитория.

Если реестра нет (закрытый контур, стенд без интернета), образ переносят файлом:

```bash
docker save -o my-tests.tar my-tests:1.0       # образ → архив
docker load -i my-tests.tar                    # архив → образ на другой машине
```

## Итог

- Образ = слои (только чтение) + конфигурация + манифест; дайджест — отпечаток содержимого.
- Контейнер пишет в свой верхний слой; удалили контейнер — потеряли записанное. Отчёты — через том.
- Образ описывают Dockerfile-ом, а не `docker commit`.
- Хороший образ тестов: `-slim`, `PYTHONUNBUFFERED=1`, зависимости до кода, `--no-cache-dir`, не root, `ENTRYPOINT ["pytest"]` + `CMD`.
- Аргументы `docker run` заменяют `CMD`; `--entrypoint` заменяет `ENTRYPOINT` и сбрасывает `CMD`.
- `docker save` / `docker load` — перенос без реестра.
'''),
    short=t(r'''
```dockerfile
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /tests
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd --create-home tester
USER tester
ENTRYPOINT ["pytest"]
CMD ["-v"]
```
```bash
docker image inspect --format '{{.Config.Cmd}}' my-tests
docker run --rm my-tests -m smoke                 # аргументы заменяют CMD
docker run --rm --entrypoint bash -it my-tests    # отладка
docker save -o my-tests.tar my-tests ; docker load -i my-tests.tar
```
'''),
    quiz=[
        q('Тест в контейнере записал файл `/tests/reports/junit.xml`, контейнер запущен с `--rm` без томов. Где файл после прогона?',
            ['В образе', 'Нигде: он был в слое для записи удалённого контейнера', 'В папке reports на хосте', 'В кэше Docker'],
            1, 'Отчёты выносят наружу через том -v.'),
        q('В образе `ENTRYPOINT ["pytest"]` и `CMD ["-v"]`. Что выполнит `docker run --rm img -m smoke`?',
            ['pytest -v -m smoke', 'pytest -m smoke', '-m smoke', 'pytest -v'],
            1, 'Аргументы run заменяют CMD и дописываются к ENTRYPOINT.'),
        q('Зачем в образе тестов `USER tester`?',
            ['Чтобы pytest работал быстрее', 'Чтобы процесс не имел прав root внутри контейнера', 'Чтобы работал кэш слоёв', 'Без него образ не соберётся'],
            1, 'Меньше прав — меньше ущерб, если что-то пойдёт не так.'),
    ],
),

# ---------- dkr-dind ----------
'dkr-dind': dict(
    full=t(r'''
## Зачем это нужно

Иногда Docker нужен **внутри** контейнера:

- CI-job работает в контейнере, а ему нужно собрать и запушить образ (`docker build`, `docker push`).
- Тесты сами поднимают базу или брокер на время прогона — библиотека **Testcontainers** запускает контейнеры прямо из кода теста.
- Тесты проверяют сам инструмент, который управляет контейнерами.

Это называют «Docker в Docker». Способов два, и у каждого свои ловушки.

## Как устроен docker

`docker` — только **клиент**. Он отправляет команды **демону** `dockerd`, а контейнеры создаёт и запускает именно демон. Клиент находит демона:

- по умолчанию — через сокет `/var/run/docker.sock`;
- или по адресу из переменной **`DOCKER_HOST`**: `unix:///var/run/docker.sock`, `tcp://docker:2376`.

Значит, чтобы `docker` работал внутри контейнера, нужен клиент и доступ к **какому-то** демону.

## Способ 1: пробросить сокет хоста

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker:27 docker ps
```

- Клиент в контейнере говорит с демоном **хоста**. `docker ps` внутри покажет контейнеры хоста, в том числе самого себя.
- Новые контейнеры — **соседи** на хосте, а не вложенные. Это быстро, и кэш образов общий.
- Ловушка с путями: в `docker run -v ./reports:/reports` путь читает **демон хоста**. Папки, которая есть только внутри контейнера CI, на хосте нет — Docker создаст пустую, и отчёты «пропадут».
- Ловушка с сетью: соседний контейнер не доступен по `localhost` контейнера с тестами — у них разные сети.
- **Риск:** доступ к сокету = root на хосте. Любой код в контейнере может запустить `docker run -v /:/host --privileged ...` и делать с машиной что угодно. Пробрасывай сокет только доверенным образам.

## Способ 2: настоящий DinD

Отдельный демон Docker в своём контейнере — образ `docker:dind`:

```bash
docker run -d --privileged --name dind docker:27-dind
```

- Внутри — свой `dockerd` со своими образами и контейнерами, изолированный от хоста.
- Ему нужен флаг **`--privileged`**: контейнер получает почти все права хоста. Безопаснее сокета не в разы, просто иначе.
- Кэш образов **пустой** при каждом запуске — сборки медленнее, если не настроить кэш через реестр.
- Демон стартует несколько секунд: клиенту нужно подождать его, иначе — `Cannot connect to the Docker daemon`.

## DinD в GitLab CI

Классическая схема: job в образе с клиентом `docker`, рядом — сервис `docker:dind`, связь по TLS:

```yaml
build-image:
  image: docker:27
  services:
    - docker:27-dind
  variables:
    DOCKER_HOST: tcp://docker:2376
    DOCKER_TLS_CERTDIR: "/certs"
  script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
    - docker build -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA" .
    - docker push "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"
```

- `services: docker:27-dind` — демон рядом с job-ом, доступен по имени `docker`.
- `DOCKER_HOST: tcp://docker:2376` — клиенту: «демон там». Порт `2376` — с TLS, `2375` — без шифрования (так делать не стоит).
- `DOCKER_TLS_CERTDIR` — куда положить сертификаты; клиент и демон обменяются ими сами.
- GitLab Runner должен быть настроен с `privileged = true` — это делают администраторы.

В **GitHub Actions** всё проще: обычный job работает на виртуальной машине, где Docker уже установлен. `docker build` и `docker run` работают сразу, DinD не нужен.

## Testcontainers: контейнеры из кода тестов

```py
from testcontainers.postgres import PostgresContainer


def test_users_table():
    with PostgresContainer("postgres:16") as pg:
        url = pg.get_connection_url()
        # подключаемся к свежей базе, создаём таблицы, проверяем
```

- Библиотека через Docker поднимает контейнер, ждёт готовности, отдаёт адрес и удаляет контейнер после блока `with`.
- Каждый прогон — с чистой базой, без общего стенда.
- Нужен доступ к Docker: локально он есть, в CI — VM GitHub Actions, сокет или DinD.

## Как выбрать

| | Сокет хоста | DinD |
|---|---|---|
| Скорость и кэш | быстро, кэш общий | медленнее, кэш пустой |
| Изоляция | контейнеры — соседи на хосте | свой демон |
| Права | доступ к сокету = root на хосте | `--privileged` |
| Пути в `-v` | пути хоста | пути внутри DinD |

Если нужно только **собрать** образ без доступа к демону, есть инструменты без Docker: Buildah, BuildKit в rootless-режиме (раньше часто использовали Kaniko).

## Итог

- `docker` — клиент; работу делает демон. Где демон — `/var/run/docker.sock` или `DOCKER_HOST`.
- Сокет хоста: быстро, контейнеры-соседи, пути и сеть хоста, но это root-доступ.
- DinD: `docker:dind` + `--privileged`, изоляция, пустой кэш, ждать запуска демона.
- GitLab: `services: docker:dind`, `DOCKER_HOST: tcp://docker:2376`, `DOCKER_TLS_CERTDIR`.
- GitHub Actions: Docker уже есть на VM.
- Testcontainers поднимает зависимости прямо из тестов.
'''),
    short=t(r'''
```bash
# сокет хоста: контейнеры-соседи, root-доступ к хосту
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker:27 docker ps
# настоящий DinD: свой демон, нужен --privileged
docker run -d --privileged --name dind docker:27-dind
```
```yaml
# GitLab CI
image: docker:27
services: [docker:27-dind]
variables:
  DOCKER_HOST: tcp://docker:2376      # 2376 — TLS, 2375 — без
  DOCKER_TLS_CERTDIR: "/certs"
```
```py
with PostgresContainer("postgres:16") as pg:    # testcontainers
    url = pg.get_connection_url()
```
'''),
    quiz=[
        q('Контейнер запущен с `-v /var/run/docker.sock:/var/run/docker.sock`. Что покажет `docker ps` внутри него?',
            ['Пустой список', 'Контейнеры хоста, включая этот', 'Только вложенные контейнеры', 'Ошибку'],
            1, 'Клиент говорит с демоном хоста.'),
        q('Чем опасен проброс docker.sock в контейнер?',
            ['Ничем', 'Это фактически root-доступ к хосту', 'Он замедляет сборку', 'Он удаляет кэш'],
            1, 'Через демон можно запустить привилегированный контейнер с файловой системой хоста.'),
        q('В GitLab job с `services: docker:27-dind` клиент пишет `Cannot connect to the Docker daemon`. Чего не хватает?',
            ['`DOCKER_HOST: tcp://docker:2376` (и TLS-настройки), либо демон ещё не запустился', 'Флага --rm', 'Тега latest', 'docker login'],
            0, 'Клиент должен знать, где демон, и дождаться его.'),
    ],
),

# ---------- dkr-ci ----------
'dkr-ci': dict(
    full=t(r'''
## Зачем это нужно

Связываем всё вместе: как на практике Docker живёт в CI-пайплайне автотестов. Цель — тесты в CI идут в **том же** окружении, что и у тебя локально, а образ, который прошёл тесты, — тот же самый, что дальше уходит на стенды.

## Главный принцип: собрать один раз

```bash
build  →  push (тег = коммит)  →  test в этом образе  →  промоутинг того же образа
```

- Образ собирают **один раз** и помечают хешем коммита: `ghcr.io/acme/shop-tests:3f2a1b9`. Видно, из какого кода он собран.
- Все следующие job-ы **скачивают** этот образ, а не собирают заново. Иначе тестируется одно, а выкатывается другое.
- Прошли тесты — тому же образу добавляют тег (`stable`, `1.4.2`). Это **промоутинг**: новый тег указывает на тот же дайджест, ничего не пересобирается.

## Теги в CI

| Тег | Зачем |
|---|---|
| `3f2a1b9` (короткий хеш коммита) | точная ссылка на код; основной тег |
| `main`, `feature-login` (ветка, `/` → `-`) | последний образ ветки |
| `1.4.2`, `1.4`, `latest` | релиз из git-тега `v1.4.2` |

`/` в имени ветки в теге нельзя — его заменяют на `-`. В CI ссылаются на хеш коммита, а `latest` — только для людей.

## GitHub Actions: собрать, запушить, прогнать

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: ghcr.io/acme/shop-tests:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  api-tests:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - run: mkdir -p reports
      - run: >
          docker run --rm
          -e BASE_URL=${{ vars.STAGE_URL }}
          -v "$PWD/reports:/tests/reports"
          ghcr.io/acme/shop-tests:${{ github.sha }}
          --junitxml=reports/junit.xml
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: api-report
          path: reports/
```

- `permissions: packages: write` — встроенному `GITHUB_TOKEN` разрешено пушить в ghcr.io. Отдельный секрет не нужен.
- `build-push-action` собирает и пушит одним шагом. `cache-from/cache-to: type=gha` хранит кэш слоёв между запусками — без него каждая сборка начинается с нуля (новая VM).
- `docker run` возвращает **код выхода pytest**: тесты упали — шаг красный, job красный.
- Отчёт пишется в том `reports/`, а `upload-artifact` с `if: always()` сохраняет его **и при падении**.

## GitLab CI: тесты прямо в собранном образе

```yaml
stages: [build, test]

build:
  stage: build
  image: docker:27
  services: [docker:27-dind]
  variables:
    DOCKER_HOST: tcp://docker:2376
    DOCKER_TLS_CERTDIR: "/certs"
  script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
    - docker pull "$CI_REGISTRY_IMAGE:latest" || true
    - docker build --cache-from "$CI_REGISTRY_IMAGE:latest" --build-arg BUILDKIT_INLINE_CACHE=1
        -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA" -t "$CI_REGISTRY_IMAGE:latest" .
    - docker push "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"
    - docker push "$CI_REGISTRY_IMAGE:latest"

api-tests:
  stage: test
  image: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  script:
    - pytest --junitxml=report.xml
  artifacts:
    when: always
    reports:
      junit: report.xml
```

- В GitLab job и так работает в контейнере: `image:` — это образ, в котором выполняется `script`. Указываем только что собранный образ — и тесты идут в нём.
- `CI_REGISTRY_IMAGE`, `CI_COMMIT_SHA`, `CI_REGISTRY_USER`, `CI_REGISTRY_PASSWORD` — готовые переменные GitLab.
- `--cache-from` + `BUILDKIT_INLINE_CACHE=1` — взять кэш слоёв из прошлого образа в реестре: у DinD свой кэш пустой.
- `artifacts: reports: junit` — GitLab покажет упавшие тесты прямо в merge request.

## Стенд рядом с тестами

Если тестам нужны база и приложение, их поднимают в том же job-е через Compose (урок «Тестовый стенд в Compose») и обязательно убирают за собой:

```yaml
- run: docker compose up --build --exit-code-from tests
- run: docker compose down -v
  if: always()
```

## Частые проблемы

- **Отчётов нет** — забыли том или `if: always()` у загрузки артефакта.
- **`Permission denied` в папке отчётов** — в контейнере другой пользователь, чем владелец папки на хосте. Запуск с `--user "$(id -u):$(id -g)"` или права на папку.
- **Сборка каждый раз с нуля** — не настроен кэш (`type=gha` или `--cache-from`).
- **`toomanyrequests`** — лимит Docker Hub: логин или свой реестр.
- **Тест прошёл в CI, на стенде другое поведение** — образ пересобрали между этапами. Ссылайся на хеш коммита или дайджест: `docker pull ghcr.io/acme/shop-tests@sha256:…`.

## Итог

- Собрать один раз → тег хешем коммита → тесты в этом образе → промоутинг тем же дайджестом.
- GitHub: `login-action` + `build-push-action` с кэшем `type=gha`; тесты — `docker run` с томом для отчётов; артефакты с `if: always()`.
- GitLab: сборка в DinD с `--cache-from`; тестовый job с `image: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA`.
- Код выхода контейнера = результат тестов; стенд — Compose с уборкой.
'''),
    short=t(r'''
```yaml
# GitHub Actions
permissions: {packages: write}
- uses: docker/build-push-action@v6
  with: {push: true, tags: "ghcr.io/acme/tests:${{ github.sha }}", cache-from: type=gha, cache-to: "type=gha,mode=max"}
- run: docker run --rm -v "$PWD/reports:/tests/reports" ghcr.io/acme/tests:${{ github.sha }}
- uses: actions/upload-artifact@v4
  if: always()
# GitLab
api-tests:
  image: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  script: [pytest --junitxml=report.xml]
  artifacts: {when: always, reports: {junit: report.xml}}
```

- Собрать один раз, тег — хеш коммита, промоутинг — тот же дайджест.
- Нет кэша → сборка с нуля; нет тома → нет отчётов.
'''),
    quiz=[
        q('Почему job с тестами скачивает образ из реестра, а не собирает его заново?',
            ['Так быстрее скачать, чем собрать', 'Чтобы тестировался ровно тот образ, который пойдёт дальше', 'Собрать в CI нельзя', 'Из-за лимитов Docker Hub'],
            1, 'Пересборка может дать другой образ: новые версии пакетов, другая база.'),
        q('Тесты в `docker run` упали. Что увидит CI?',
            ['Шаг зелёный — контейнер же отработал', 'Шаг красный: docker run возвращает код выхода pytest', 'Предупреждение', 'Зависит от тега'],
            1, 'Код выхода процесса в контейнере становится кодом docker run.'),
        q('Что такое промоутинг образа?',
            ['Пересборка с тегом release', 'Новый тег для того же образа (того же дайджеста) после прохождения тестов', 'Удаление старых тегов', 'Публикация в Docker Hub'],
            1, 'Ничего не пересобирается — меняется только метка.'),
    ],
),

}
