"""Теория модуля «Docker Compose» темы «Docker для тестировщика».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- dkr-compose ----------
'dkr-compose': dict(
    full=t(r'''
## Зачем это нужно

Реальному стенду нужно несколько контейнеров: приложение, база, кэш, иногда очередь и сами тесты. Запускать каждый длинной командой `docker run` с десятком флагов неудобно и легко ошибиться. **Docker Compose** описывает весь стенд одним YAML-файлом и поднимает его одной командой.

## docker-compose.yml

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret
  app:
    image: shop-app:1.0
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:secret@db:5432/postgres
    depends_on:
      - db
```

- `services` — контейнеры стенда; ключ — имя сервиса.
- `image` — готовый образ, или `build: .` — собрать из Dockerfile.
- `ports`, `environment`, `volumes` — те же `-p`, `-e`, `-v`, только в файле. Порты пиши в кавычках: YAML может прочитать `22:22` как число в шестидесятеричной системе.
- `depends_on` — порядок запуска: `app` стартует после `db`.
- Сервисы автоматически в одной сети и находят друг друга **по имени**: в `DATABASE_URL` хост — `db`.

YAML: отступы — только пробелами, списки — через `- `, `ключ: значение`.

## Команды

```bash
docker compose up -d            # поднять всё в фоне (соберёт/скачает образы)
docker compose ps               # что запущено
docker compose logs -f app      # логи сервиса
docker compose stop             # остановить, не удаляя
docker compose down             # остановить и удалить контейнеры и сеть
docker compose down -v          # …и тома (данные базы)
```

`docker compose` (через пробел) — современная версия, встроенная в Docker. Старая отдельная утилита называлась `docker-compose` (через дефис).

## Это просто YAML

```python
import yaml

text = """
services:
  app: {image: shop-app:1.0, depends_on: [db]}
  db: {image: postgres:16}
"""
services = yaml.safe_load(text)["services"]
print(sorted(services), services["app"]["depends_on"])
```

Вывод: `['app', 'db'] ['db']`. Поэтому compose-файлы легко проверять и генерировать скриптами.

## Итог

- Compose = стенд из нескольких сервисов в одном YAML-файле.
- `image`/`build`, `ports`, `environment`, `volumes`, `depends_on`.
- Сервисы видят друг друга по именам.
- `up -d`, `ps`, `logs -f`, `down -v`.
'''),
    short=t(r'''
```yaml
services:
  db:  {image: postgres:16, environment: {POSTGRES_PASSWORD: secret}}
  app:
    image: shop-app:1.0
    ports: ["8000:8000"]
    depends_on: [db]          # хост базы для app — просто "db"
```
```bash
docker compose up -d ; docker compose ps ; docker compose logs -f app
docker compose down -v        # вместе с томами
```
'''),
    quiz=[
        q('Как приложение из compose обращается к сервису базы `db`?',
            ['По localhost', 'По имени сервиса: `db`', 'По IP хоста', 'Никак — нужна ручная сеть'],
            1, 'Compose создаёт общую сеть с DNS по именам сервисов.'),
        q('Чем `docker compose down -v` отличается от `docker compose down`?',
            ['Ничем', 'Удаляет ещё и тома — данные базы', 'Показывает подробный вывод', 'Удаляет образы'],
            1, '-v — volumes.'),
        q('Почему порты в compose-файле пишут в кавычках?',
            ['Так красивее', 'YAML может разобрать `22:22` не как строку', 'Иначе compose не запустится никогда', 'Для Windows'],
            1, 'Кавычки гарантируют строку.'),
    ],
),

# ---------- dkr-env ----------
'dkr-env': dict(
    full=t(r'''
## Зачем это нужно

Один compose-файл должен работать на ноутбуке, в CI и на тестовом стенде — с разными адресами, паролями и версиями. Для этого значения выносят в **переменные**.

## Подстановка переменных

```yaml
services:
  tests:
    build: .
    environment:
      BASE_URL: ${BASE_URL:-http://app:8000}
      BROWSER: ${BROWSER:-chromium}
  app:
    image: shop-app:${APP_VERSION:?укажи версию}
```

- `${VAR}` — значение переменной (пусто, если её нет).
- `${VAR:-default}` — значение или `default`, если переменной нет **или она пустая**.
- `${VAR:?сообщение}` — обязательная: без неё compose остановится с ошибкой.

## Файл .env

Compose сам читает `.env` рядом с `docker-compose.yml`:

```bash
# .env — не коммитить, если в нём секреты!
BASE_URL=http://stage.test
APP_VERSION=1.4.2
```

Приоритет значений: переменная **оболочки** (`BASE_URL=… docker compose up`) → файл **`.env`** → значение по умолчанию из `:-`. Другой файл: `docker compose --env-file .env.stage up -d`.

Проверить, что подставилось: `docker compose config` — выводит итоговый файл.

## environment и env_file

- `environment:` — переменные контейнера прямо в файле; словарём (`KEY: value`) или списком (`- KEY=value`) — это одно и то же.
- `env_file: .env.tests` — загрузить переменные контейнера из файла.

Осторожно с YAML: `DEBUG: true` без кавычек — это булево значение; compose передаст строку, но лучше писать `DEBUG: "true"`.

```python
as_list = ["BASE_URL=http://app", "TOKEN=a=b"]
print(dict(item.split("=", 1) for item in as_list))
```

Вывод: `{'BASE_URL': 'http://app', 'TOKEN': 'a=b'}` — делим по **первому** `=`.

## Итог

- `${VAR}`, `${VAR:-default}`, `${VAR:?error}`.
- `.env` читается автоматически; `--env-file` — другой файл; `docker compose config` — проверить результат.
- Оболочка сильнее `.env`, `.env` сильнее значения по умолчанию.
'''),
    short=t(r'''
```yaml
BASE_URL: ${BASE_URL:-http://app:8000}    # по умолчанию, если нет или пусто
image: app:${APP_VERSION:?нужна версия}   # обязательная
env_file: .env.tests
```
```bash
docker compose --env-file .env.stage up -d
docker compose config                     # итоговый файл с подстановками
# приоритет: оболочка > .env > :-default
```
'''),
    quiz=[
        q('Чему равно `${BROWSER:-chromium}`, если `BROWSER=""`?',
            ['Пустой строке', '`chromium`', 'Ошибке', '`BROWSER`'],
            1, '`:-` срабатывает и для пустого значения.'),
        q('Как увидеть compose-файл с уже подставленными переменными?',
            ['`docker compose ps`', '`docker compose config`', '`cat docker-compose.yml`', '`docker compose env`'],
            1, 'config печатает итоговую конфигурацию.'),
        q('Где значение сильнее: в `.env` или в переменной оболочки?',
            ['В `.env`', 'В переменной оболочки', 'Одинаково', 'Compose игнорирует оболочку'],
            1, 'Так удобно переопределять значения в CI.'),
    ],
),

# ---------- dkr-stand ----------
'dkr-stand': dict(
    full=t(r'''
## Зачем это нужно

Тесты стартовали, а база ещё инициализируется — первые тесты падают с «connection refused». `depends_on` в короткой форме ждёт только **запуска** контейнера, а не готовности сервиса. Надёжный стенд ждёт **здоровья**.

## healthcheck и condition

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 2s
      retries: 10
  app:
    image: shop-app:1.0
    depends_on:
      db:
        condition: service_healthy
  tests:
    build: .
    environment:
      BASE_URL: http://app:8000
    depends_on:
      - app
```

- `healthcheck.test` — команда проверки; код 0 — здоров. Docker повторяет её каждые `interval`, после `retries` неудач помечает сервис `unhealthy`.
- `condition: service_healthy` — стартовать, когда зависимость **здорова**. Есть ещё `service_started` (по умолчанию) и `service_completed_successfully` (дождаться, пока одноразовый сервис вроде миграций завершится с кодом 0).

## Прогон тестов в CI одной командой

```bash
docker compose up --build --exit-code-from tests
docker compose down -v --remove-orphans
```

- `--exit-code-from tests` — вся команда завершится, когда закончится сервис `tests`, и вернёт **его** код выхода (включает `--abort-on-container-exit`).
- `--build` — пересобрать образы (код тестов мог измениться).

Точечные запуски на поднятом стенде:

```bash
docker compose run --rm tests pytest -m smoke    # одноразовый контейнер сервиса
docker compose exec db psql -U postgres          # консоль в работающем сервисе
```

## Адреса: изнутри и снаружи

- Тесты **в контейнере** той же сети → `http://app:8000` (имя сервиса и порт контейнера).
- Тесты **на хосте** → `http://localhost:<опубликованный порт>` из `ports`.

## Ожидание готовности в коде

Та же идея — «пробуем, ждём, повторяем» — нужна и в фикстурах тестов, когда стенд поднимается рядом: опрашивать `/health` с паузами и сдаться после N попыток с понятной ошибкой.

## Итог

- `healthcheck` + `condition: service_healthy` — ждать готовности, а не запуска.
- `up --build --exit-code-from tests` — прогон в CI, код выхода тестов.
- `run --rm` — разовый запуск, `exec` — внутрь работающего.
- Изнутри сети — имя сервиса, снаружи — localhost и опубликованный порт.
'''),
    short=t(r'''
```yaml
healthcheck: {test: ["CMD", "pg_isready", "-U", "postgres"], interval: 2s, retries: 10}
depends_on:
  db: {condition: service_healthy}     # service_started | service_completed_successfully
```
```bash
docker compose up --build --exit-code-from tests
docker compose run --rm tests pytest -m smoke
docker compose exec db psql -U postgres
# изнутри: http://app:8000 · с хоста: http://localhost:<ports>
```
'''),
    quiz=[
        q('Чего ждёт `depends_on: [db]` в короткой форме?',
            ['Пока база будет готова принимать запросы', 'Только запуска контейнера db', 'Пока db завершится', 'Ничего'],
            1, 'Для готовности нужен healthcheck и condition: service_healthy.'),
        q('Что делает `--exit-code-from tests`?',
            ['Удаляет сервис tests', 'Останавливает стенд, когда закончился tests, и возвращает его код выхода', 'Запускает только tests', 'Печатает код выхода'],
            1, 'Так CI узнаёт результат тестов.'),
        q('Тесты запущены на хосте, а в compose у app `ports: ["8080:8000"]`. Какой адрес?',
            ['http://app:8000', 'http://localhost:8080', 'http://localhost:8000', 'http://app:8080'],
            1, 'С хоста — опубликованный порт.'),
    ],
),

# ---------- dkr-practice ----------
'dkr-practice': dict(
    full=t(r'''
## Зачем это нужно

Соберём всё в рабочую схему, которую используют в командах: стенд в compose, тесты в контейнере, отчёты наружу, диагноз при падении и уборка за собой.

## Структура проекта

```bash
shop-tests/
  Dockerfile               # образ с тестами
  .dockerignore
  docker-compose.yml       # стенд: db + app + tests
  docker-compose.ci.yml    # надстройка для CI
  .env.example             # пример переменных (без секретов)
  tests/ …
  requirements.txt
```

## Несколько файлов и профили

```bash
docker compose -f docker-compose.yml -f docker-compose.ci.yml up -d
```

Второй файл **дополняет и переопределяет** первый: в CI можно поменять образы на собранные, убрать публикацию портов, добавить переменные.

```yaml
services:
  ui-tests:
    build: .
    profiles: ["ui"]        # не стартует без --profile ui
```

`docker compose --profile ui up -d` — поднять и «необязательные» сервисы профиля.

## Прогон и разбор

```bash
docker compose up --build --exit-code-from tests    # прогон
docker compose ps -a                                 # кто упал
docker compose logs --tail 100 app                   # почему
docker cp tests:/app/reports .                       # забрать отчёт, если тома нет
docker compose down -v --remove-orphans              # уборка
```

Типичные диагнозы:

- `exited (137)` — не хватило памяти (подними лимит или найди утечку);
- `exited (1)` и `Traceback` в логах — ошибка в коде сервиса;
- `running (unhealthy)` — сервис жив, но не прошёл healthcheck;
- «connection refused» в тестах — сервис не готов: нет healthcheck/condition или неверный адрес (`localhost` вместо имени сервиса).

## Из Python

Обвязку (скрипты CI, фикстуры) удобно писать на Python — списком аргументов:

```python
files = ["docker-compose.yml", "docker-compose.ci.yml"]
cmd = ["docker", "compose"]
for f in files:
    cmd += ["-f", f]
cmd += ["up", "-d"]
print(" ".join(cmd))
```

Вывод: `docker compose -f docker-compose.yml -f docker-compose.ci.yml up -d`. Запуск — `subprocess.run(cmd, check=True)`.

## Итог

- Стенд: Dockerfile тестов + compose (db, app, tests) + `.env`.
- Надстройки `-f`, профили `--profile`.
- Прогон `--exit-code-from`, разбор `ps`/`logs`, уборка `down -v --remove-orphans`.
'''),
    short=t(r'''
```bash
docker compose -f docker-compose.yml -f docker-compose.ci.yml up -d
docker compose --profile ui up -d
docker compose up --build --exit-code-from tests
docker cp tests:/app/reports .
docker compose down -v --remove-orphans
# 137 — память · 1 + Traceback — код · unhealthy — healthcheck
```
'''),
    quiz=[
        q('Что делает второй файл в `docker compose -f a.yml -f b.yml up`?',
            ['Запускает второй стенд', 'Дополняет и переопределяет настройки первого', 'Игнорируется', 'Заменяет первый целиком'],
            1, 'Так делают надстройки для CI.'),
        q('Сервис с `profiles: ["ui"]` при обычном `docker compose up`…',
            ['Запустится', 'Не запустится без `--profile ui`', 'Упадёт с ошибкой', 'Запустится последним'],
            1, 'Профили — для необязательных сервисов.'),
        q('Тесты падают с «connection refused» к app, хотя app в статусе running. Что проверить первым?',
            ['Версию pytest', 'Адрес (имя сервиса, а не localhost) и ожидание готовности (healthcheck)', 'Размер образа', 'Тег latest'],
            1, 'Самые частые причины.'),
    ],
),

}
