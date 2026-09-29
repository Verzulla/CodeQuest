"""Теория модуля «Dockerfile и сборка» темы «Docker для тестировщика».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- dci-m1-l2 ----------
'dci-m1-l2': dict(
    full=t(r'''
## Зачем это нужно

Готовых образов для твоих автотестов нет — их собирают сами, по рецепту **Dockerfile**. Хороший Dockerfile собирается быстро (кэш), весит мало и одинаково работает везде.

## Dockerfile — рецепт образа

```dockerfile
FROM python:3.12-slim              # базовый образ
WORKDIR /app                       # рабочая папка (создастся сама)
COPY requirements.txt .            # сначала только зависимости…
RUN pip install -r requirements.txt
COPY . .                           # …потом весь код
CMD ["pytest", "-v"]               # что запустить при старте контейнера
```

- `FROM` — с чего начинаем; всегда первая инструкция (кроме `ARG` перед ней).
- `WORKDIR` — `cd` внутри образа для всех следующих инструкций и для запуска.
- `COPY откуда куда` — файлы из **контекста сборки** (папки, переданной в `docker build`) в образ.
- `RUN` — выполнить команду **при сборке** (установить пакеты).
- `CMD` — команда **при запуске** контейнера.

```bash
docker build -t my-tests .     # . — контекст сборки: текущая папка
docker run --rm my-tests
```

## Слои и кэш

Каждая инструкция создаёт **слой**. При пересборке Docker идёт по инструкциям и берёт слои из кэша, пока ничего не изменилось. Как только инструкция или файлы, которые она копирует, изменились, пересобирается этот слой и **все после него**.

Поэтому зависимости копируют **отдельно и раньше кода**: код тестов меняется постоянно, `requirements.txt` — редко. Правка теста пересоберёт только `COPY . .`, а долгий `pip install` возьмётся из кэша. Если написать `COPY . .` до `pip install`, любая правка будет заново ставить все библиотеки.

```bash
docker history my-tests         # слои образа и их размер
docker build --no-cache -t my-tests .   # собрать без кэша
```

## .dockerignore

Всё содержимое контекста отправляется Docker'у при сборке, а `COPY . .` копирует его в образ. Лишнее исключают файлом `.dockerignore` (синтаксис как у `.gitignore`):

```bash
.git
.venv
__pycache__
*.pyc
.pytest_cache
reports
allure-results
```

Меньше контекст — быстрее сборка, меньше образ, и правка отчётов не сбивает кэш `COPY . .`.

## Итог

- `FROM`, `WORKDIR`, `COPY`, `RUN` (сборка), `CMD` (запуск).
- Слой меняется — пересобирается он и всё после; зависимости — до кода.
- `.dockerignore` убирает мусор из контекста.
'''),
    short=t(r'''
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["pytest", "-v"]
```
```bash
docker build -t my-tests .
docker build --no-cache -t my-tests .
docker history my-tests
# .dockerignore: .git .venv __pycache__ *.pyc reports
```
'''),
    quiz=[
        q('Почему `COPY requirements.txt .` и `RUN pip install` ставят раньше `COPY . .`?',
            ['Так требует синтаксис', 'Чтобы правка кода не сбивала кэш установки зависимостей', 'Чтобы образ был меньше', 'Чтобы тесты шли быстрее'],
            1, 'Изменённый слой пересобирает всё после себя.'),
        q('Чем `RUN` отличается от `CMD`?',
            ['Ничем', '`RUN` выполняется при сборке образа, `CMD` — при запуске контейнера', '`CMD` выполняется при сборке', '`RUN` только для pip'],
            1, 'RUN меняет образ, CMD задаёт команду по умолчанию.'),
        q('Что означает точка в `docker build -t my-tests .`?',
            ['Имя образа', 'Контекст сборки — текущая папка', 'Последний тег', 'Ничего'],
            1, 'Оттуда берутся файлы для COPY.'),
    ],
),

# ---------- dkr-instructions ----------
'dkr-instructions': dict(
    full=t(r'''
## Зачем это нужно

Один и тот же образ с тестами хочется запускать по-разному: на разных стендах, разным набором (`smoke` или весь регресс), с разными версиями Python. Для этого Dockerfile делают **настраиваемым**.

## ENV и ARG

```dockerfile
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim
ENV BASE_URL=http://app:8000 \
    HEADLESS=true
```

- `ARG` — переменная **сборки**: `docker build --build-arg PYTHON_VERSION=3.11 .`. В запущенном контейнере её нет. Чтобы использовать в `FROM`, объявляй до него.
- `ENV` — переменная **окружения** контейнера со значением по умолчанию; `docker run -e BASE_URL=…` её переопределяет.
- Подстановка `${VAR}` и `${VAR:-по_умолчанию}` работает и в Dockerfile, и в compose.

## CMD и ENTRYPOINT

```dockerfile
ENTRYPOINT ["pytest"]
CMD ["-v"]
```

- Контейнер выполняет `ENTRYPOINT + CMD` → `pytest -v`.
- Аргументы после имени образа **заменяют CMD**: `docker run --rm my-tests -m smoke` → `pytest -m smoke`.
- Без `ENTRYPOINT` аргументы заменяют всю команду: `docker run --rm my-tests bash`.
- Итого: `ENTRYPOINT` — что запускаем всегда, `CMD` — аргументы по умолчанию.

## Exec-форма и shell-форма

```dockerfile
CMD ["pytest", "-v"]      # exec-форма: JSON-список, процесс запускается напрямую
CMD pytest -v             # shell-форма: строка, выполняется через /bin/sh -c
```

Предпочитай exec-форму: процесс получает сигналы остановки (`docker stop` завершит pytest аккуратно), а аргументы не портятся кавычками. Exec-форма — строгий JSON: только **двойные** кавычки.

```python
import json

print(json.loads('["pytest", "-m", "smoke and not slow"]'))
```

Вывод: `['pytest', '-m', 'smoke and not slow']`.

## Другие инструкции

- `USER nobody` — дальше работать не от root (безопаснее).
- `EXPOSE 8000` — документирует порт приложения (сам ничего не публикует; публикует `-p`).
- `ADD` — как `COPY`, но умеет распаковывать архивы и качать URL; для обычных файлов используют `COPY`.
- `LABEL`, `HEALTHCHECK`, `VOLUME` — метаданные, проверка здоровья, тома.

## Итог

- `ARG` — при сборке (`--build-arg`), `ENV` — в контейнере (`-e` переопределяет).
- `ENTRYPOINT` + `CMD`; аргументы `docker run` заменяют `CMD`.
- Exec-форма `["…"]` лучше shell-формы.
'''),
    short=t(r'''
```dockerfile
ARG PYTHON_VERSION=3.12                 # docker build --build-arg PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim
ENV BASE_URL=http://app:8000            # docker run -e BASE_URL=… переопределит
USER nobody
ENTRYPOINT ["pytest"]                   # всегда
CMD ["-v"]                              # по умолчанию; docker run img -m smoke → pytest -m smoke
```
'''),
    quiz=[
        q('В образе `ENTRYPOINT ["pytest"]` и `CMD ["-v"]`. Что выполнит `docker run img -m smoke`?',
            ['`pytest -v -m smoke`', '`pytest -m smoke`', '`-m smoke`', '`pytest -v`'],
            1, 'Аргументы run заменяют CMD, ENTRYPOINT остаётся.'),
        q('Чем `ARG` отличается от `ENV`?',
            ['Ничем', '`ARG` существует только при сборке, `ENV` — и в запущенном контейнере', '`ENV` только при сборке', '`ARG` нельзя переопределить'],
            1, 'ARG задают через --build-arg.'),
        q('Почему exec-форма `CMD ["pytest"]` лучше `CMD pytest`?',
            ['Короче', 'Процесс запускается напрямую и корректно получает сигналы остановки', 'Работает только она', 'Быстрее собирается'],
            1, 'Shell-форма запускает команду через /bin/sh -c.'),
    ],
),

# ---------- dkr-tests ----------
'dkr-tests': dict(
    full=t(r'''
## Зачем это нужно

Автотесты в контейнере запускаются одинаково у всех: у тебя, у коллеги, в CI. Не нужно «поставь Python 3.12, потом вот эти пакеты, потом браузер» — только `docker run`.

## Образ для автотестов

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["pytest", "--junitxml=reports/junit.xml"]
```

- `--no-cache-dir` — pip не хранит скачанные пакеты: образ меньше.
- Отчёт пишется в `reports/` — эту папку пробрасывают наружу томом.

## Запуск

```bash
docker build -t my-tests .
docker run --rm \
  -e BASE_URL=http://stage.test \
  -v $(pwd)/reports:/app/reports \
  my-tests
echo $?                                    # код выхода: 0 — все тесты прошли
docker run --rm my-tests pytest -m smoke   # свой набор вместо CMD
```

- Адрес стенда — переменной окружения, тесты читают `os.environ["BASE_URL"]`.
- Отчёты — томом, иначе они исчезнут вместе с контейнером.
- Код выхода `docker run` = код выхода pytest, и CI поймёт, прошли ли тесты.

## UI-тесты: образ с браузерами

Ставить браузеры и их системные библиотеки руками долго. У Playwright есть официальный образ, где всё уже есть:

```dockerfile
FROM mcr.microsoft.com/playwright/python:v1.47.0-noble
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["pytest", "--browser", "chromium"]
```

Версия образа должна совпадать с версией пакета `playwright` в `requirements.txt` — иначе браузеры не подойдут.

## Контейнер тестов и стенд

- Стенд на хосте → в контейнере `localhost` — это сам контейнер, а не хост! На Mac/Windows хост доступен как `host.docker.internal`.
- Стенд в других контейнерах → общая сеть и адрес по имени сервиса (`http://app:8000`) — это делает Compose (модуль 3).

## Итог

- Образ тестов: зависимости слоем, `--no-cache-dir`, `CMD` с pytest и отчётом.
- `-e` — стенд, `-v` — отчёты, аргументы после образа — свой набор тестов.
- Код выхода контейнера = результат тестов для CI.
- UI-тесты — на официальном образе Playwright той же версии.
'''),
    short=t(r'''
```bash
docker run --rm -e BASE_URL=http://stage.test -v $(pwd)/reports:/app/reports my-tests
docker run --rm my-tests pytest -m smoke
echo $?            # 0 — зелёный
# UI: FROM mcr.microsoft.com/playwright/python:v1.47.0-noble (версия = версии playwright)
# localhost в контейнере — сам контейнер; хост: host.docker.internal
```
'''),
    quiz=[
        q('Зачем при запуске тестов в контейнере `-v $(pwd)/reports:/app/reports`?',
            ['Чтобы тесты шли быстрее', 'Чтобы отчёты остались на хосте после удаления контейнера', 'Чтобы подключить базу', 'Для логов Docker'],
            1, 'Иначе отчёты исчезнут с контейнером.'),
        q('Тесты в контейнере обращаются к `http://localhost:8000`, а приложение запущено на хосте. Что будет?',
            ['Всё работает', 'Не подключится: localhost внутри контейнера — это сам контейнер', 'Docker сам перенаправит', 'Зависит от pytest'],
            1, 'Нужен адрес хоста или общая сеть с приложением.'),
        q('Как CI узнаёт, что тесты в контейнере упали?',
            ['По логам', 'По ненулевому коду выхода `docker run`', 'По размеру отчёта', 'Никак'],
            1, 'Код выхода контейнера = код pytest.'),
    ],
),

# ---------- dkr-optimize ----------
'dkr-optimize': dict(
    full=t(r'''
## Зачем это нужно

Образ на 2 ГБ скачивается в CI минутами на каждый прогон, а образ с паролем внутри — дыра в безопасности. Размер и безопасность образа — тоже качество.

## Откуда берётся размер

Образ — сумма слоёв. Посмотреть:

```bash
docker history my-tests       # слои и их размер
docker images                 # итоговый размер образов
docker system df              # сколько места занимает Docker целиком
```

Что помогает:

- **slim/alpine-база**: `python:3.12-slim` (~130 МБ) вместо `python:3.12` (~1 ГБ).
- `pip install --no-cache-dir` и `apt-get install … && rm -rf /var/lib/apt/lists/*` **в одной** инструкции `RUN`: удаление в следующем слое место не вернёт — файлы останутся в предыдущем.
- `.dockerignore` — не тащить `.git`, `.venv`, отчёты.

## Многоэтапная сборка

```dockerfile
FROM python:3.12 AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*
COPY . .
USER nobody
CMD ["pytest"]
```

Первый этап — «толстый» (компиляторы, заголовки), во второй копируется только результат (`COPY --from=builder`). В итоговый образ попадает лишь последний этап.

## Безопасность

- **Не root**: `USER nobody` (или свой пользователь). Уязвимость в зависимости не даст root-доступ.
- **Никаких секретов в образе**: `ENV DB_PASSWORD=…` и `ARG TOKEN` видны каждому через `docker history` и `docker inspect`. Секреты передают при запуске (`-e`, секреты CI) или через `--secret` при сборке.
- **Фиксированные версии**: `FROM python:3.12.5-slim`, а не `latest`.
- **Сканирование уязвимостей**: `trivy image my-tests:1.0` или `docker scout cves my-tests:1.0`.

## Уборка

```bash
docker image prune            # висящие образы без тегов
docker system prune           # остановленные контейнеры, неиспользуемые сети, висящие образы и кэш
```

## Итог

- Slim-база, `--no-cache-dir`, установка и уборка в одном `RUN`, `.dockerignore`.
- Multi-stage: собираем в толстом этапе, копируем результат в тонкий.
- `USER` не root, секреты — не в образе, версии зафиксированы, образ сканируется.
'''),
    short=t(r'''
```dockerfile
FROM python:3.12 AS builder
RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels
FROM python:3.12-slim
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*
USER nobody
```
```bash
docker history my-tests ; docker system df
docker image prune ; docker system prune
trivy image my-tests:1.0
```
'''),
    quiz=[
        q('Почему `RUN apt-get install x` и в следующей строке `RUN rm -rf /var/lib/apt/lists/*` не уменьшают образ?',
            ['Уменьшают', 'Файлы остаются в предыдущем слое — удалять нужно в той же инструкции RUN', 'rm не работает в Docker', 'Нужно добавить --no-cache'],
            1, 'Слои только добавляются поверх.'),
        q('Что попадает в итоговый образ при многоэтапной сборке?',
            ['Все этапы', 'Только последний этап (и то, что в него скопировали)', 'Только первый', 'Только кэш'],
            1, 'Отсюда и экономия.'),
        q('Где хранить пароль к тестовой базе для контейнера с тестами?',
            ['В `ENV` Dockerfile', 'Передавать при запуске (`-e`, секреты CI), не в образе', 'В имени образа', 'В `LABEL`'],
            1, 'Всё из Dockerfile видно в образе.'),
    ],
),

}
