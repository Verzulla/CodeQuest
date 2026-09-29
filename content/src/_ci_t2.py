"""Теория модуля «GitHub Actions» темы «CI/CD для тестировщика».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- dci-m2-l2 ----------
'dci-m2-l2': dict(
    full=t(r'''
## Зачем это нужно

GitHub Actions — самый распространённый CI для проектов на GitHub: workflow лежит прямо в репозитории, запускается на готовых раннерах и не требует своего сервера. Большинство вакансий автоматизаторов ждут умения его читать и править.

## Workflow

Файл `.github/workflows/tests.yml`:

```yaml
name: tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements.txt
      - run: pytest --junitxml=reports/junit.xml
        env:
          BASE_URL: ${{ vars.STAGE_URL }}
          API_TOKEN: ${{ secrets.API_TOKEN }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: reports
          path: reports/
```

- `on` — когда запускать; `jobs` — что делать; `runs-on` — на какой машине (`ubuntu-latest`, `windows-latest`, `macos-latest`).
- `steps` — шаги по порядку: `uses` — готовое действие (action) с версией после `@`, `run` — команда оболочки.
- `actions/checkout` — скачать код репозитория. Без него на раннере пусто!
- `with` — параметры действия, `env` — переменные окружения шага.
- `${{ … }}` — выражения: `matrix.*`, `secrets.*`, `vars.*`, `github.*`.
- `timeout-minutes` — не дать зависшему тесту съесть 6 часов (лимит по умолчанию).

## Секреты маскируются

Значения из `secrets` GitHub заменяет в логах на `***`. Но только их — токен, который тест сам сгенерировал и напечатал, утечёт.

## Матрица

```yaml
strategy:
  matrix:
    python: ["3.11", "3.12"]
```

Job запустится для каждой комбинации значений — `${{ matrix.python }}` в шагах.

## GitHub CLI

```bash
gh run list                          # последние запуски
gh run view 9876543210 --log-failed  # логи упавших шагов
gh run rerun 9876543210 --failed     # перезапустить упавшие job-ы
gh run watch                         # следить за текущим запуском
```

## Итог

- Workflow = `on` + `jobs`; job = `runs-on` + `steps`.
- `uses` — action с версией, `run` — команда; первым шагом — `actions/checkout`.
- `secrets` маскируются, `if: always()` — для отчётов, `timeout-minutes` — от зависаний.
- `gh run list/view/rerun` — работа с запусками из терминала.
'''),
    short=t(r'''
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12", cache: pip}
      - run: pytest
        env: {API_TOKEN: "${{ secrets.API_TOKEN }}"}
```
```bash
gh run list ; gh run view <id> --log-failed ; gh run rerun <id> --failed
```
'''),
    quiz=[
        q('Что будет, если забыть шаг `actions/checkout`?',
            ['Ничего', 'На раннере не будет кода репозитория — pytest ничего не найдёт', 'Workflow не запустится', 'Не будет Python'],
            1, 'Раннер — чистая машина.'),
        q('Чем `uses` отличается от `run`?',
            ['Ничем', '`uses` — готовое действие, `run` — команда оболочки', '`run` — только для Docker', '`uses` выполняется в конце'],
            1, 'Actions переиспользуют чужие шаги.'),
        q('Как посмотреть логи только упавших шагов запуска из терминала?',
            ['`gh run list`', '`gh run view <id> --log-failed`', '`gh logs`', '`git log`'],
            1, 'GitHub CLI.'),
    ],
),

# ---------- ci-matrix ----------
'ci-matrix': dict(
    full=t(r'''
## Зачем это нужно

Приложение должно работать в трёх браузерах, на двух версиях Python и на разных ОС. Писать job на каждую комбинацию — копипаста. **Матрица** описывает оси, а GitHub сам разворачивает все комбинации.

## Матрица

```yaml
jobs:
  ui-tests:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      max-parallel: 4
      matrix:
        os: [ubuntu-latest, windows-latest]
        browser: [chromium, firefox, webkit]
        exclude:
          - os: windows-latest
            browser: webkit
        include:
          - os: macos-latest
            browser: webkit
    steps:
      - run: pytest --browser ${{ matrix.browser }}
```

- Комбинаций: 2 × 3 = 6, минус 1 (`exclude`), плюс 1 (`include`) = 6 запусков.
- `exclude` убирает комбинации, совпадающие по всем указанным ключам.
- `include` добавляет новые комбинации — или новые ключи к существующим, если совпали все её значения.
- `fail-fast` (по умолчанию `true`) — первое падение **отменяет** остальные незаконченные запуски. Для тестов обычно ставят `false`: нужно видеть все упавшие браузеры, а не только первый.
- `max-parallel` — не больше N запусков одновременно.

## Выражения и контексты

- `${{ matrix.browser }}`, `${{ github.ref }}` (`refs/heads/main`), `${{ github.ref_name }}` (`main`), `${{ github.sha }}`, `${{ github.event_name }}`.
- Условия: `if: github.ref == 'refs/heads/main'` — строки в одинарных кавычках; функции `success()`, `failure()`, `always()`, `contains(...)`, `startsWith(...)`.

## Окружения

Разные ветки → разные стенды: `main` → staging, тег `v1.2.0` → production, pull request → временный review-стенд. В GitHub это **environments** (`environment: staging`) — со своими секретами и правилами одобрения.

```python
ref = "refs/tags/v1.4.0"
print(ref.startswith("refs/tags/v"), ref.split("/")[-1])
```

Вывод: `True v1.4.0`.

## Итог

- Матрица = оси; `exclude`/`include` правят комбинации.
- `fail-fast: false` для тестов — видеть все падения.
- Контексты `matrix`, `github`; условия `if:` с функциями.
- Ветка определяет стенд; environments хранят его секреты.
'''),
    short=t(r'''
```yaml
strategy:
  fail-fast: false
  matrix:
    browser: [chromium, firefox, webkit]
    exclude: [{browser: webkit}]
    include: [{browser: webkit, os: macos-latest}]
if: github.ref == 'refs/heads/main'
# ${{ matrix.browser }} ${{ github.ref_name }} ${{ github.sha }}
```
'''),
    quiz=[
        q('Что делает `fail-fast: true` в матрице?',
            ['Ускоряет тесты', 'Отменяет остальные запуски после первого падения', 'Повторяет упавшие', 'Запускает всё последовательно'],
            1, 'Для тестов обычно выключают.'),
        q('Матрица 2 ОС × 3 браузера и один `exclude`. Сколько запусков?',
            ['6', '5', '7', '3'],
            1, '6 − 1.'),
        q('Как записать условие «только ветка main»?',
            ['`if: branch = main`', "`if: github.ref == 'refs/heads/main'`", '`if: main`', '`on: main`'],
            1, 'Строки в выражениях — в одинарных кавычках.'),
    ],
),

# ---------- ci-secrets ----------
'ci-secrets': dict(
    full=t(r'''
## Зачем это нужно

Автотестам нужны пароли тестовых пользователей, токены API, строки подключения к базе. Положить их в код — значит отдать всем, у кого есть доступ к репозиторию (а иногда и всему интернету). CI хранит их отдельно и подставляет только во время работы.

## Секреты и переменные в GitHub

- **Secrets** (`Settings → Secrets and variables → Actions` или `gh secret set API_TOKEN`) — зашифрованы, маскируются в логах: `${{ secrets.API_TOKEN }}`.
- **Variables** — несекретные настройки (адрес стенда): `${{ vars.STAGE_URL }}`.
- Уровни: репозиторий, окружение (environment), организация.

```yaml
jobs:
  api-tests:
    runs-on: ubuntu-latest
    env:
      BASE_URL: ${{ vars.STAGE_URL }}
      API_TOKEN: ${{ secrets.API_TOKEN }}
```

## В тестах — через окружение

```python
import os

os.environ["BASE_URL"] = "https://stage.test"
print(os.environ.get("BASE_URL"), os.environ.get("API_TOKEN", "нет"))
```

Вывод: `https://stage.test нет`. Если секрет обязателен — падай **сразу** с понятным сообщением («Не задан API_TOKEN»), а не через десять тестов с «401 Unauthorized».

## Утечки

- Маскируются только известные значения. Если тест печатает заголовки запросов или URL с паролем — секрет уйдёт в лог. Не логируй `Authorization`, пароли в URL.
- Секрет, полученный во время работы, можно замаскировать: `echo "::add-mask::$TOKEN"`.
- Pull request из **форка** не получает секреты — иначе любой мог бы их украсть, изменив workflow.
- `.env` с настоящими значениями — в `.gitignore`; в репозитории — `.env.example` без секретов.
- Утёкший секрет — **сразу отозвать** и выпустить новый: удаление коммита не помогает, история и форки остаются.

## Итог

- `secrets.*` — зашифровано и маскируется, `vars.*` — обычные настройки.
- В тестах — `os.environ`, обязательные проверяй в начале.
- Не печатай секреты; `::add-mask::`; `.env` — в `.gitignore`; утёк — отзывай.
'''),
    short=t(r'''
```yaml
env:
  BASE_URL: ${{ vars.STAGE_URL }}
  API_TOKEN: ${{ secrets.API_TOKEN }}
```
```bash
gh secret set API_TOKEN
echo "::add-mask::$TOKEN"
# .env → .gitignore, в репозитории — .env.example
# из форков секреты не приходят
```
'''),
    quiz=[
        q('Чем `secrets.X` отличается от `vars.X`?',
            ['Ничем', 'Секреты зашифрованы и маскируются в логах, переменные — нет', 'vars нельзя использовать в job-ах', 'secrets видны в логах'],
            1, 'Для паролей и токенов — только secrets.'),
        q('Токен случайно закоммитили в публичный репозиторий. Что делать первым?',
            ['Удалить коммит', 'Отозвать токен и выпустить новый', 'Сделать репозиторий приватным', 'Ничего'],
            1, 'История и форки уже могли его сохранить.'),
        q('Почему pull request из форка не видит секреты?',
            ['Это баг', 'Иначе автор форка мог бы изменить workflow и украсть их', 'Форки не запускают CI', 'Секреты только для main'],
            1, 'Защита от кражи.'),
    ],
),

# ---------- ci-docker ----------
'ci-docker': dict(
    full=t(r'''
## Зачем это нужно

API-тестам нужна база, UI-тестам — запущенное приложение. В CI их поднимают теми же контейнерами, что и локально, — окружение одинаковое, и «у меня работает» перестаёт быть оправданием.

## Сервисы job-а

```yaml
jobs:
  api-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: secret
        ports:
          - "5432:5432"
        options: >-
          --health-cmd "pg_isready -U postgres"
          --health-interval 2s
          --health-retries 10
    steps:
      - uses: actions/checkout@v4
      - run: pytest tests/api
        env:
          DATABASE_URL: postgresql://postgres:secret@localhost:5432/postgres
```

- GitHub поднимает контейнеры **до** шагов и ждёт их healthcheck (`options` — флаги `docker run`).
- Шаги идут прямо на раннере, поэтому база доступна как `localhost:5432` (порт опубликован).

## Docker Compose в CI

Если стенд уже описан в compose — используй его и в CI:

```yaml
steps:
  - uses: actions/checkout@v4
  - run: docker compose up --build --exit-code-from tests
  - uses: actions/upload-artifact@v4
    if: always()
    with: {name: reports, path: reports/}
  - run: docker compose down -v
    if: always()
```

## Условия шагов

- по умолчанию `success()` — все предыдущие шаги успешны;
- `failure()` — только если что-то упало (уведомления, дамп логов);
- `always()` — всегда (отчёты, уборка).

## Образ тестов в реестр

```bash
echo "$CR_TOKEN" | docker login ghcr.io -u acme --password-stdin
docker build -t ghcr.io/acme/tests:$GITHUB_SHA .
docker push ghcr.io/acme/tests:$GITHUB_SHA
```

- Токен — через `--password-stdin`: в аргументах он попал бы в историю и в список процессов.
- Теги: `sha-<коммит>` (точно знаем код), имя ветки, версия из git-тега, `latest` для main.

## Итог

- `services:` — контейнеры рядом с job-ом; с healthcheck; доступ через localhost.
- Compose в CI: `up --build --exit-code-from tests`, отчёты и `down -v` с `if: always()`.
- `success()` / `failure()` / `always()`.
- Логин по `--password-stdin`, теги по коммиту и версии.
'''),
    short=t(r'''
```yaml
services:
  postgres:
    image: postgres:16
    ports: ["5432:5432"]
    options: --health-cmd "pg_isready -U postgres" --health-interval 2s
- run: docker compose down -v
  if: always()                 # success() по умолчанию · failure() · always()
```
```bash
echo "$CR_TOKEN" | docker login ghcr.io -u acme --password-stdin
docker build -t ghcr.io/acme/tests:$GITHUB_SHA .
```
'''),
    quiz=[
        q('Как шаги job-а обращаются к сервису `postgres` с `ports: ["5432:5432"]`?',
            ['postgres:5432', 'localhost:5432', 'db:5432', 'Никак'],
            1, 'Шаги идут на раннере, порт опубликован на нём.'),
        q('Почему токен передают через `--password-stdin`, а не `-p`?',
            ['Так быстрее', 'Аргументы видны в истории, списке процессов и логах', '-p не существует', 'Так требует GitHub'],
            1, 'stdin не светится.'),
        q('Какое условие у шага уборки стенда `docker compose down -v`?',
            ['`if: success()`', '`if: always()`', '`if: failure()`', 'Без условия'],
            1, 'Убирать нужно и после падения.'),
    ],
),

}
