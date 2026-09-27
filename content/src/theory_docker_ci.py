"""Подробная теория и «Проверь себя» для темы «Docker и CI/CD»."""
from ._lib import t

THEORY = {
"dci-m1-l1": {"full": t("""
    ## Зачем это нужно

    «У меня всё проходит, а в CI падает», «на стенде другая версия Python», «чтобы поднять проект, нужен день» — знакомо каждому тестировщику. Docker упаковывает приложение **вместе с окружением** (ОС, версия Python, библиотеки, настройки) в образ, который одинаково запускается на ноутбуке, у коллеги и в CI. Для QA это ещё и способ за минуту поднять БД, браузер или всё приложение для тестов.

    ## Как это работает

    ### Образ и контейнер

    - **Образ (image)** — неизменяемый «слепок» окружения. Аналогия — класс или установочный диск.
    - **Контейнер** — запущенный экземпляр образа со своим состоянием. Аналогия — объект. Из одного образа можно запустить сколько угодно контейнеров.
    - **Реестр** (Docker Hub, GitLab Registry) — хранилище образов.
    - **Тег** — версия образа: `python:3.12-slim`, `postgres:16`. Без тега подставляется `latest` — в CI так делать не стоит, «последняя» версия может смениться без предупреждения.

    ### Основные команды

    ```bash
    docker pull postgres:16                         # скачать образ
    docker run --rm -p 8080:80 nginx                # запустить; удалить контейнер после остановки
    docker run -d --name db -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres:16
    docker ps                                       # запущенные контейнеры (-a — все)
    docker logs -f db                               # логи — первое, куда смотреть при падении
    docker exec -it db psql -U postgres             # команда внутри контейнера
    docker stop db && docker rm db                  # остановить и удалить
    ```

    Флаги `docker run`:
    - `-d` — в фоне; `--name` — имя; `--rm` — удалить после остановки;
    - `-p ХОСТ:КОНТЕЙНЕР` — пробросить порт;
    - `-e КЛЮЧ=значение` — переменная окружения (так настраивают тесты: адрес стенда, браузер);
    - `-v ./reports:/app/reports` — пробросить папку (например, чтобы забрать отчёты тестов).

    ### Коды выхода

    Код выхода контейнера = код выхода команды внутри. `0` — успех; `1` — ошибка приложения (например, упали тесты); `125` — ошибка самого Docker; `127` — команда не найдена; `137` — процесс убит (часто нехватка памяти, OOM).

    ### docker compose

    Несколько связанных контейнеров (приложение + БД + браузер) описывают в `compose.yaml` и поднимают одной командой `docker compose up -d`:

    ```yaml
    services:
      app:
        image: my-shop:1.4
        ports: ["8000:8000"]
        environment:
          DATABASE_URL: postgres://postgres:secret@db:5432/shop
        depends_on: [db]
      db:
        image: postgres:16
        environment:
          POSTGRES_PASSWORD: secret
    ```

    Контейнеры видят друг друга по имени сервиса: приложение подключается к `db:5432`.

    ## Примеры

    ### Пример 1. Разбор ссылки на образ

    ```python
    def parse_image(ref):
        name, _, tag = ref.partition(":")
        return name, tag or "latest"

    for ref in ["python:3.12-slim", "nginx", "selenium/standalone-chrome:124.0"]:
        print(ref, "->", parse_image(ref))
    ```

    ### Пример 2. Сборка команды запуска

    ```python
    def docker_run_cmd(image, ports=None, env=None, rm=True):
        parts = ["docker", "run"]
        if rm:
            parts.append("--rm")
        for host, container in (ports or {}).items():
            parts.append(f"-p {host}:{container}")
        for key, value in (env or {}).items():
            parts.append(f"-e {key}={value}")
        parts.append(image)
        return " ".join(parts)

    print(docker_run_cmd("my-tests:1.0", env={"BASE_URL": "http://app:8000", "BROWSER": "chrome"}))
    print(docker_run_cmd("nginx", ports={8080: 80}, rm=False))
    ```

    ### Пример 3. Настройка тестов через окружение

    Внутри контейнера тесты читают настройки из переменных окружения — так один образ запускается против разных стендов:

    ```python
    import os

    os.environ["BASE_URL"] = "http://staging:8000"     # в жизни задаётся через docker run -e
    base_url = os.environ.get("BASE_URL", "http://localhost:8000")
    browser = os.environ.get("BROWSER") or "chrome"
    headless = os.environ.get("HEADLESS", "true").lower() == "true"
    print(base_url, browser, headless)
    ```

    ### Пример 4. Расшифровка кода выхода

    ```python
    MEANING = {0: "ok", 1: "app error (упали тесты?)", 125: "docker error",
               127: "command not found", 137: "killed — нехватка памяти?"}
    for code in [0, 1, 137, 42]:
        print(code, "->", MEANING.get(code, "unknown"))
    ```

    ## Частые ошибки

    **`latest` в CI.** Сегодня один Python, завтра другой — «вдруг всё упало».

    **Ожидание, что данные сохранятся.** Файлы внутри контейнера исчезают вместе с ним. Отчёты и данные — через `-v`.

    **`localhost` внутри контейнера** — это сам контейнер, а не твоя машина. Другие сервисы в compose — по имени сервиса.

    **Игнорировать `docker logs`.** Почти любая загадка «контейнер сразу завершился» решается чтением логов.

    ## Шпаргалка

    ```bash
    docker run --rm -e KEY=val -p 8080:80 -v ./reports:/app/reports image:tag
    docker ps -a · docker logs -f NAME · docker exec -it NAME sh
    docker compose up -d · docker compose logs -f · docker compose down
    ```
    """), "quiz": [
    {"q": "Чем образ отличается от контейнера?",
     "options": ["Ничем, это синонимы", "Образ — неизменяемый шаблон, контейнер — запущенный экземпляр образа", "Контейнер хранится в реестре, образ — нет", "Образ — это запущенный процесс"], "answer": 1,
     "explain": "Как класс и объект: из одного образа можно запустить много контейнеров."},
    {"q": "Что значит `-p 8080:80` в `docker run`?",
     "options": ["Порт 80 хоста → порт 8080 контейнера", "Порт 8080 хоста → порт 80 контейнера", "Ограничить процессор", "Запустить 80 копий"], "answer": 1,
     "explain": "Формат `ХОСТ:КОНТЕЙНЕР` — на машине открываешь `localhost:8080`, а внутри отвечает сервис на порту 80."},
    {"q": "Контейнер с тестами завершился с кодом 137. Что проверить в первую очередь?",
     "options": ["Опечатки в тестах", "Нехватку памяти — процесс был убит", "Сеть", "Версию Python"], "answer": 1,
     "explain": "137 = 128 + 9 (SIGKILL). Чаще всего процесс убивает ядро из-за нехватки памяти."},
]},

"dci-m1-l2": {"full": t("""
    ## Зачем это нужно

    Готовых образов недостаточно, когда нужно упаковать **свои** автотесты: нужная версия Python, зависимости, код тестов, команда запуска. Рецепт образа — `Dockerfile`. Хорошо написанный Dockerfile собирается за секунды благодаря кэшу, плохо написанный — каждый раз заново качает все зависимости.

    ## Как это работает

    ### Основные инструкции

    ```dockerfile
    FROM python:3.12-slim                      # базовый образ
    WORKDIR /app                               # рабочая папка (создаётся сама)
    ENV PYTHONDONTWRITEBYTECODE=1              # переменная окружения по умолчанию
    COPY requirements.txt .                    # скопировать файл из контекста сборки
    RUN pip install --no-cache-dir -r requirements.txt   # выполнить команду при сборке
    COPY . .                                   # скопировать остальной код
    CMD ["pytest", "-v", "--junitxml=reports/junit.xml"] # команда при запуске контейнера
    ```

    - `RUN` выполняется **при сборке** образа, `CMD` — **при запуске** контейнера.
    - `CMD` в форме списка (`["pytest", "-v"]`) — рекомендуемая: без лишнего shell.
    - Аргументы `docker run my-tests pytest -k login` заменяют `CMD`.

    Сборка и запуск:

    ```bash
    docker build -t my-tests:1.0 .
    docker run --rm -e BASE_URL=http://staging:8000 -v ./reports:/app/reports my-tests:1.0
    ```

    ### Слои и кэш

    Каждая инструкция — **слой**. При повторной сборке Docker берёт слои из кэша, пока входные данные не изменились. Как только слой изменился — **он и все последующие** пересобираются.

    Отсюда главное правило порядка: **что меняется редко — выше, что часто — ниже**. Зависимости (`requirements.txt`) меняются редко, код тестов — постоянно. Поэтому сначала копируем только `requirements.txt` и ставим зависимости, а потом — весь код. Тогда правка теста не запускает долгий `pip install`.

    ### .dockerignore

    Всё, что лежит в папке сборки (контекст), отправляется Docker. `.dockerignore` исключает лишнее — сборка быстрее, образ меньше, секреты не утекают:

    ```text
    .git
    .venv
    __pycache__
    *.pyc
    reports/
    .env
    ```

    ## Примеры

    ### Пример 1. Разбор Dockerfile

    ```python
    DOCKERFILE = '''
    # образ для автотестов
    FROM python:3.12-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install -r requirements.txt
    COPY . .
    CMD ["pytest", "-v"]
    '''

    def parse(text):
        result = []
        for line in text.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                instr, _, args = line.partition(" ")
                result.append((instr.upper(), args))
        return result

    for instr, args in parse(DOCKERFILE):
        print(f"{instr:8} {args}")
    ```

    ### Пример 2. Какой слой пересоберётся

    ```python
    def first_rebuilt(steps, changed):
        for i, (cmd, files) in enumerate(steps):
            if changed & set(files):
                return i
        return None

    good = [("FROM python:3.12-slim", []), ("COPY requirements.txt .", ["requirements.txt"]),
            ("RUN pip install -r requirements.txt", []), ("COPY . .", ["requirements.txt", "tests/test_api.py"])]
    bad = [("FROM python:3.12-slim", []), ("COPY . .", ["requirements.txt", "tests/test_api.py"]),
           ("RUN pip install -r requirements.txt", [])]

    for name, steps in [("правильный порядок", good), ("неправильный", bad)]:
        i = first_rebuilt(steps, {"tests/test_api.py"})
        rebuilt = [cmd for cmd, _ in steps[i:]]
        print(f"{name}: пересоберутся {rebuilt}")
    ```

    Во втором варианте правка одного теста заставляет заново ставить все зависимости.

    ### Пример 3. Проверка порядка для кэша

    ```python
    def cache_friendly(instructions):
        texts = [f"{i} {a}" for i, a in instructions]
        try:
            pip = next(k for k, s in enumerate(texts) if s.startswith("RUN pip install"))
            code = next(k for k, s in enumerate(texts) if s.startswith("COPY . "))
        except StopIteration:
            return False
        return pip < code

    print(cache_friendly([("COPY", "requirements.txt ."), ("RUN", "pip install -r requirements.txt"), ("COPY", ". .")]))
    print(cache_friendly([("COPY", ". ."), ("RUN", "pip install -r requirements.txt")]))
    ```

    ### Пример 4. Упрощённый .dockerignore

    ```python
    from fnmatch import fnmatch

    PATTERNS = [".git", ".venv", "__pycache__", "*.pyc", "reports", ".env"]

    def ignored(path):
        return any(fnmatch(part, p) for part in path.split("/") for p in PATTERNS)

    for path in [".git/config", "tests/test_api.py", "app/__pycache__/x.pyc", ".env", "requirements.txt"]:
        print(f"{path:28} {'исключён' if ignored(path) else 'в образ'}")
    ```

    ## Частые ошибки

    **`COPY . .` до `pip install`** — кэш зависимостей сбрасывается при каждой правке кода.

    **Путаница `RUN` и `CMD`.** `RUN pytest` запустит тесты при **сборке** образа, а не при запуске контейнера.

    **Секреты в образе.** `COPY .env` или `ENV TOKEN=...` — токен останется в слоях образа навсегда. Передавай секреты при запуске (`-e`) или через секреты CI.

    **Нет `.dockerignore`** — в контекст уходят `.git` и `.venv` на сотни мегабайт.

    ## Шпаргалка

    ```dockerfile
    FROM python:3.12-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    CMD ["pytest", "-v"]
    ```

    Редко меняется — выше, часто — ниже. `RUN` — при сборке, `CMD` — при запуске.
    """), "quiz": [
    {"q": "Когда выполняется инструкция `RUN` в Dockerfile?",
     "options": ["При запуске контейнера", "При сборке образа", "При каждом `docker ps`", "При остановке контейнера"], "answer": 1,
     "explain": "`RUN` — шаг сборки образа. При запуске контейнера выполняется `CMD` (или `ENTRYPOINT`)."},
    {"q": "Почему `requirements.txt` копируют и устанавливают **до** `COPY . .`?",
     "options": ["Так требует синтаксис", "Чтобы правка кода не сбрасывала кэш долгой установки зависимостей", "Чтобы образ был безопаснее", "Иначе pip не найдёт файл"], "answer": 1,
     "explain": "Слой пересобирается, если изменились его входные файлы, и вместе с ним все последующие. Зависимости меняются редко — их слой должен быть выше."},
    {"q": "Где правильно хранить токен для тестов, чтобы он не попал в образ?",
     "options": ["`ENV TOKEN=...` в Dockerfile", "`COPY .env .`", "Передавать при запуске: `docker run -e TOKEN=...` или через секреты CI", "В коде тестов"], "answer": 2,
     "explain": "Всё, что попало в Dockerfile, остаётся в слоях образа. Секреты передают только в момент запуска."},
]},

"dci-m2-l1": {"full": t("""
    ## Зачем это нужно

    Тесты, которые никто не запускает, не ловят баги. **CI** (Continuous Integration) запускает сборку и тесты автоматически на каждый push и pull request — ошибку видно через минуты после коммита, а не через неделю на регрессе. **CD** (Continuous Delivery/Deployment) идёт дальше: если всё зелёное, приложение само выкатывается на стенд или в прод. Тестировщик в современной команде настраивает и поддерживает свою часть пайплайна.

    ## Как это работает

    ### Пайплайн

    Последовательность **стадий** (stages), в каждой — один или несколько **job**-ов:

    ```text
    lint → unit → build (docker) → api-tests → ui-tests → deploy
    ```

    - **Fail fast**: быстрые и дешёвые проверки — первыми. Упал линтер за 20 секунд — незачем 30 минут гонять UI-тесты.
    - **Зависимости** (`needs:`): job запускается, когда готовы его зависимости. Независимые job-ы идут **параллельно** (api-tests и ui-tests после build).
    - **Артефакты** — файлы, которые job сохраняет и передаёт дальше или прикладывает к результату: отчёты, скриншоты, логи, собранный образ.

    ### Код выхода — язык CI

    CI не читает вывод тестов — он смотрит только на **код выхода** команды: `0` — job зелёный, любое другое — красный.

    Коды выхода `pytest`:
    - `0` — все тесты прошли;
    - `1` — есть упавшие тесты;
    - `2` — прерван (Ctrl+C);
    - `3` — внутренняя ошибка;
    - `4` — неверные аргументы командной строки;
    - `5` — **не найдено ни одного теста**. Частая ошибка конфигурации: тесты «прошли», потому что их не запустили.

    ### Когда деплоить

    Обычно: только из основной ветки (`main`) и только если **все** проверки зелёные. Feature-ветки гоняют тесты, но не выкатываются.

    ## Примеры

    ### Пример 1. Fail fast

    ```python
    jobs = [("lint", 0), ("unit", 0), ("api-tests", 1), ("ui-tests", 0), ("deploy", 0)]
    for name, code in jobs:
        if code != 0:
            print(f"❌ {name} (код {code}) — дальше не идём")
            break
        print(f"✅ {name}")
    else:
        print("🚀 всё зелёное")
    ```

    ### Пример 2. Расшифровка кода pytest

    ```python
    PYTEST = ["all passed", "tests failed", "interrupted", "internal error", "usage error", "no tests collected"]
    for code in [0, 1, 5]:
        print(code, PYTEST[code])
    ```

    ### Пример 3. Решение о деплое

    ```python
    def should_deploy(branch, codes):
        return branch == "main" and all(c == 0 for c in codes)

    for branch, codes in [("main", [0, 0, 0]), ("feature/login", [0, 0]), ("main", [0, 1])]:
        print(f"{branch:15} {codes} -> {'деплой' if should_deploy(branch, codes) else 'без деплоя'}")
    ```

    ### Пример 4. Порядок job-ов по зависимостям

    ```python
    needs = {
        "deploy": ["api-tests", "ui-tests"],
        "api-tests": ["build"],
        "ui-tests": ["build"],
        "build": ["lint", "unit"],
        "lint": [],
        "unit": [],
    }
    done, wave = set(), 1
    while len(done) < len(needs):
        ready = sorted(j for j, deps in needs.items() if j not in done and all(d in done for d in deps))
        print(f"волна {wave} (параллельно): {ready}")
        done.update(ready)
        wave += 1
    ```

    Так CI-система понимает, что можно запускать одновременно.

    ## Частые ошибки

    **Тяжёлые проверки первыми** — долгое ожидание обратной связи.

    **Команда, которая «глотает» код выхода** (`pytest || true`, `pytest | tee log.txt` без `set -o pipefail`) — job зелёный при упавших тестах.

    **Код 5 не считается ошибкой** — пустой прогон выглядит как успех.

    **Флаки в пайплайне** — команда привыкает к красному и перестаёт на него реагировать.

    ## Шпаргалка

    ```text
    CI  = собрать + протестировать на каждый push/PR
    CD  = выкатить автоматически, если всё зелёное
    0 — успех, всё остальное — провал
    pytest: 0 ok · 1 упали тесты · 5 тестов не найдено
    Порядок: быстрые проверки → сборка → медленные тесты → деплой
    ```
    """), "quiz": [
    {"q": "По какому признаку CI решает, что job прошёл?",
     "options": ["По тексту в логе", "По коду выхода команды: 0 — успех", "По времени выполнения", "По количеству тестов"], "answer": 1,
     "explain": "CI смотрит только на код выхода. Именно поэтому команды, «глотающие» ненулевой код, опасны."},
    {"q": "Что означает код выхода pytest `5`?",
     "options": ["5 тестов упало", "Не найдено ни одного теста", "Таймаут", "Все тесты прошли"], "answer": 1,
     "explain": "Код 5 — «no tests collected». Часто это ошибка в путях или маске файлов, и её важно не пропустить."},
    {"q": "Почему линтер и модульные тесты ставят в начало пайплайна?",
     "options": ["Они важнее UI-тестов", "Они быстрые: при ошибке пайплайн остановится рано и не потратит время на долгие этапы", "Так требует GitHub", "Они не зависят от кода"], "answer": 1,
     "explain": "Принцип fail fast: дешёвые проверки дают обратную связь за секунды и отсекают заведомо сломанные сборки."},
]},

"dci-m2-l2": {"full": t("""
    ## Зачем это нужно

    GitHub Actions — встроенная CI/CD-система GitHub, одна из самых популярных. Тестировщику нужно уметь прочитать и поправить workflow: добавить прогон своих тестов, матрицу браузеров, сохранение отчётов, передачу секретов. А результаты тестов CI понимает через стандартный формат отчёта **JUnit XML**.

    ## Как это работает

    ### Workflow

    Файл `.github/workflows/tests.yml`:

    ```yaml
    name: tests
    on:
      push:
        branches: [main]
      pull_request:

    jobs:
      api-tests:
        runs-on: ubuntu-latest
        strategy:
          fail-fast: false
          matrix:
            python: ["3.11", "3.12"]
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: ${{ matrix.python }}
          - run: pip install -r requirements.txt
          - run: pytest --junitxml=reports/junit.xml
            env:
              BASE_URL: https://staging.example.com
              API_TOKEN: ${{ secrets.API_TOKEN }}
          - uses: actions/upload-artifact@v4
            if: always()
            with:
              name: reports-${{ matrix.python }}
              path: reports/
    ```

    Разбор:
    - `on` — события-триггеры: push в main, любой pull request, расписание (`schedule`), ручной запуск (`workflow_dispatch`).
    - `jobs` — задачи; каждая выполняется на свежей виртуальной машине (`runs-on`).
    - `steps` — шаги: `uses` — готовое действие из маркетплейса, `run` — shell-команда.
    - `actions/checkout` — **обязательный** первый шаг: без него в машине нет кода репозитория.
    - `matrix` — запустить job для всех комбинаций параметров (версии, браузеры, ОС). `fail-fast: false` — не отменять остальные комбинации при падении одной.
    - `secrets.*` — пароли и токены из настроек репозитория. В логах GitHub автоматически заменяет их на `***`.
    - `if: always()` — выполнить шаг даже если предыдущие упали. Для отчётов это критично: они нужнее всего именно при падении.

    Отступы в YAML — часть синтаксиса, как в Python.

    ### JUnit XML

    `pytest --junitxml=report.xml` создаёт отчёт, который понимают GitHub, GitLab, Jenkins и Allure:

    ```xml
    <testsuites>
      <testsuite name="api" tests="3" failures="1" skipped="1">
        <testcase name="test_get_user" time="0.12"/>
        <testcase name="test_create_user" time="0.20">
          <failure message="assert 200 == 201"/>
        </testcase>
        <testcase name="test_delete" time="0.01"><skipped/></testcase>
      </testsuite>
    </testsuites>
    ```

    ## Примеры

    ### Пример 1. Разворачивание матрицы

    ```python
    from itertools import product

    matrix = {"python": ["3.11", "3.12"], "browser": ["chromium", "firefox", "webkit"]}
    keys = list(matrix)
    jobs = [dict(zip(keys, combo)) for combo in product(*matrix.values())]
    print(len(jobs), "job-ов:")
    for j in jobs:
        print(" ", j)
    ```

    ### Пример 2. Маскирование секретов

    ```python
    def mask(log, secrets):
        for s in secrets:
            if s:                           # пустая строка замаскировала бы всё
                log = log.replace(s, "***")
        return log

    log = "curl -H 'Authorization: Bearer abc123' https://user:pa55@host/api"
    print(mask(log, ["abc123", "pa55", ""]))
    ```

    ### Пример 3. Разбор JUnit-отчёта

    ```python
    import xml.etree.ElementTree as ET

    REPORT = '''<testsuites>
      <testsuite name="api">
        <testcase name="test_get_user" time="0.12"/>
        <testcase name="test_create_user" time="0.20"><failure message="assert 200 == 201"/></testcase>
        <testcase name="test_delete" time="0.01"><skipped/></testcase>
      </testsuite>
      <testsuite name="ui">
        <testcase name="test_login" time="3.10"><error message="TimeoutError"/></testcase>
      </testsuite>
    </testsuites>'''

    root = ET.fromstring(REPORT)
    cases = list(root.iter("testcase"))
    failed = [c for c in cases if c.find("failure") is not None or c.find("error") is not None]
    skipped = [c for c in cases if c.find("skipped") is not None]
    print(f"всего {len(cases)}, упало {len(failed)}, пропущено {len(skipped)}")
    for c in failed:
        reason = (c.find("failure") if c.find("failure") is not None else c.find("error")).get("message")
        print(f"  ❌ {c.get('name')}: {reason}")
    slowest = max(cases, key=lambda c: float(c.get("time")))
    print("самый долгий:", slowest.get("name"), slowest.get("time"), "с")
    ```

    ### Пример 4. Проверка workflow на типичные ошибки

    ```python
    WORKFLOW = '''
    name: tests
    on: [push, pull_request]
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/setup-python@v5
          - run: pytest
    '''

    problems = []
    if "actions/checkout" not in WORKFLOW:
        problems.append("нет checkout — в раннере не будет кода")
    if "pip install" not in WORKFLOW:
        problems.append("зависимости не устанавливаются")
    if "upload-artifact" not in WORKFLOW:
        problems.append("отчёты не сохраняются")
    print("\\n".join(problems) or "выглядит нормально")
    ```

    ## Частые ошибки

    **Забыли `actions/checkout`** — «pytest: no tests collected» или «requirements.txt not found».

    **Отчёты без `if: always()`** — при упавших тестах шаг загрузки не выполнится, и разбирать будет нечего.

    **Секреты прямо в YAML** — они навсегда остаются в истории git. Только `secrets.*`.

    **Неправильные отступы** в YAML — workflow не запускается или ведёт себя странно.

    ## Шпаргалка

    ```yaml
    on: [push, pull_request]
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with: {python-version: "3.12"}
          - run: pip install -r requirements.txt
          - run: pytest --junitxml=reports/junit.xml
          - uses: actions/upload-artifact@v4
            if: always()
            with: {name: reports, path: reports/}
    ```
    """), "quiz": [
    {"q": "Зачем шаг `actions/checkout` в начале job-а?",
     "options": ["Чтобы проверить синтаксис", "Чтобы скачать код репозитория в раннер — без него кода нет", "Чтобы установить Python", "Чтобы отправить отчёт"], "answer": 1,
     "explain": "Каждый job выполняется на чистой машине. Код репозитория туда попадает только через checkout."},
    {"q": "Зачем шагу загрузки отчётов условие `if: always()`?",
     "options": ["Чтобы он выполнялся быстрее", "Чтобы отчёт сохранился, даже если тесты упали", "Чтобы шаг запускался по расписанию", "Это обязательно для всех шагов"], "answer": 1,
     "explain": "По умолчанию после упавшего шага остальные пропускаются. А отчёт нужнее всего именно при падении."},
    {"q": "Сколько job-ов создаст матрица `python: [\"3.11\", \"3.12\"]` × `browser: [\"chromium\", \"firefox\"]`?",
     "options": ["2", "3", "4", "1"], "answer": 2,
     "explain": "Матрица запускает все комбинации: 2 × 2 = 4 job-а."},
]},
}
