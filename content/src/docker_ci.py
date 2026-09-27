"""Тема «Docker и CI/CD для тестировщика».

Docker и GitHub Actions в песочнице не запустить, поэтому практика:
написать Dockerfile/workflow строкой (тесты разбирают его по строкам)
и утилиты, которые реально нужны в пайплайне.
"""
from textwrap import dedent

from ._lib import t, cod, lesson, module, out, topic

P = "dci"

DF_PARSE = '''
def _instructions(text):
    result = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        instr, _, args = line.partition(" ")
        result.append((instr.upper(), args.strip()))
    return result
'''

m1 = module(f"{P}-m1", "Docker", "🐳", "Образы, контейнеры и Dockerfile",
    lesson(f"{P}-m1-l1", "Образы и контейнеры", """
        # Зачем тестировщику Docker

        «У меня работает, а в CI падает» — классика. Docker упаковывает приложение **вместе с окружением** (версия Python, библиотеки, настройки), и оно одинаково запускается везде.

        - **Образ (image)** — шаблон, «слепок» окружения. Неизменяемый. Пример: `python:3.12-slim`.
        - **Контейнер** — запущенный экземпляр образа. Из одного образа можно запустить сколько угодно контейнеров.
        - **Тег** — версия образа после двоеточия. Без тега подставится `latest` (в CI так лучше не делать — версия может смениться).

        # Основные команды

        ```
        docker pull postgres:16                  # скачать образ
        docker run --rm -p 8080:80 nginx         # запустить; --rm удалит контейнер после остановки
        docker run -d --name db -e POSTGRES_PASSWORD=secret postgres:16   # в фоне, с переменной окружения
        docker ps                                # запущенные контейнеры
        docker logs db                           # логи контейнера — первое, что смотреть при падении
        docker exec -it db psql -U postgres      # выполнить команду внутри контейнера
        docker stop db
        ```

        - `-p 8080:80` — порт **хоста**:порт **контейнера**.
        - `-v $(pwd)/reports:/app/reports` — пробросить папку (чтобы забрать отчёты тестов).
        - Код выхода контейнера = код выхода команды внутри. `137` — контейнер убит (часто нехватка памяти).
        """,
        out(f"{P}-m1-l1-e1", "Что выведет программа? Разбираем ссылку на образ.", """
            for ref in ["python:3.12-slim", "nginx", "postgres:16"]:
                name, _, tag = ref.partition(":")
                print(name, tag or "latest")
            """),
        out(f"{P}-m1-l1-e2", "Что выведет программа? Конфигурацию тестов часто передают через переменные окружения (`-e` в docker run).", """
            env = {"BASE_URL": "http://app:8000", "BROWSER": ""}
            base_url = env.get("BASE_URL", "http://localhost")
            browser = env.get("BROWSER") or "chrome"
            headless = env.get("HEADLESS", "true") == "true"
            print(base_url, browser, headless)
            """),
        cod(f"{P}-m1-l1-e3", t("""
            Напиши функцию `parse_image(ref)`, которая разбирает ссылку на Docker-образ.

            Ссылка имеет вид `имя:тег`, тег необязателен.

            - Получает: `ref` — строку-ссылку.
            - Возвращает: пару `(имя, тег)`. Если тега нет — тег `"latest"`.

            Примеры:
            ```
            parse_image("python:3.12-slim")   # → ("python", "3.12-slim")
            parse_image("nginx")              # → ("nginx", "latest")
            ```
            """),
            """
            def parse_image(ref):
                pass
            """,
            """
            def test_with_tag():
                assert parse_image("python:3.12-slim") == ("python", "3.12-slim"), f"Получено {parse_image('python:3.12-slim')}"

            def test_no_tag():
                assert parse_image("nginx") == ("nginx", "latest"), "Без тега → latest"
            """,
            """
            def parse_image(ref):
                name, _, tag = ref.partition(":")
                return name, tag or "latest"
            """),
        cod(f"{P}-m1-l1-e4", t("""
            Напиши функцию `docker_run_cmd(image, ports=None, env=None, rm=True)`, которая собирает команду `docker run`.

            - Получает:
              - `image` — образ;
              - `ports` — словарь `{порт_хоста: порт_контейнера}` или `None`;
              - `env` — словарь переменных окружения `{ИМЯ: значение}` или `None`;
              - `rm` — добавлять ли флаг `--rm`.
            - Возвращает: команду одной строкой, части через пробел, **строго в таком порядке**:
              1. `docker run`
              2. `--rm` — если `rm` истинно
              3. `-p хост:контейнер` — для каждой пары из `ports`
              4. `-e ИМЯ=значение` — для каждой переменной из `env`
              5. образ

            Примеры:
            ```
            docker_run_cmd("app:1.0", ports={8080: 80}, env={"DEBUG": "1", "MODE": "test"})
            # → "docker run --rm -p 8080:80 -e DEBUG=1 -e MODE=test app:1.0"

            docker_run_cmd("nginx", rm=False)
            # → "docker run nginx"
            ```
            """),
            """
            def docker_run_cmd(image, ports=None, env=None, rm=True):
                pass
            """,
            """
            def test_full():
                got = docker_run_cmd("app:1.0", ports={8080: 80}, env={"DEBUG": "1", "MODE": "test"})
                assert got == "docker run --rm -p 8080:80 -e DEBUG=1 -e MODE=test app:1.0", f"Получено {got!r}"

            def test_minimal():
                assert docker_run_cmd("nginx", rm=False) == "docker run nginx", f"Получено {docker_run_cmd('nginx', rm=False)!r}"
            """,
            """
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
            """,
            hint="Собери части в список и соедини через `\" \".join(parts)`. `ports or {}` спасает от None.", xp=20),
        cod(f"{P}-m1-l1-e5", t("""
            Напиши функцию `explain_exit(code)`, которая объясняет код выхода упавшего контейнера.

            - Получает: `code` — код выхода (число).
            - Возвращает строку-пояснение:
              - `0` → `"ok"`
              - `1` → `"app error"` — ошибка в самом приложении
              - `125` → `"docker error"` — ошибка самого Docker
              - `127` → `"command not found"` — команда не найдена
              - `137` → `"killed (OOM?)"` — процесс убит, часто из-за нехватки памяти
              - любой другой код → `"unknown"`

            Примеры:
            ```
            explain_exit(137)   # → "killed (OOM?)"
            explain_exit(42)    # → "unknown"
            ```
            """),
            """
            def explain_exit(code):
                pass
            """,
            """
            def test_known():
                got = [explain_exit(c) for c in (0, 1, 125, 127, 137)]
                assert got == ["ok", "app error", "docker error", "command not found", "killed (OOM?)"], f"Получено {got}"

            def test_unknown():
                assert explain_exit(42) == "unknown", "Неизвестный код → unknown"
            """,
            """
            def explain_exit(code):
                return {0: "ok", 1: "app error", 125: "docker error", 127: "command not found",
                        137: "killed (OOM?)"}.get(code, "unknown")
            """,
            hint="Словарь + `.get(code, \"unknown\")`."),
    ),
    lesson(f"{P}-m1-l2", "Dockerfile и слои", """
        # Dockerfile — рецепт образа

        ```
        FROM python:3.12-slim              # базовый образ
        WORKDIR /app                       # рабочая папка внутри образа
        COPY requirements.txt .            # сначала только зависимости…
        RUN pip install -r requirements.txt
        COPY . .                           # …потом весь код
        ENV BASE_URL=http://app:8000       # переменная окружения по умолчанию
        CMD ["pytest", "-v", "--junitxml=reports/junit.xml"]   # что запустить при старте
        ```

        Собрать и запустить: `docker build -t my-tests .` → `docker run --rm my-tests`.

        # Слои и кэш

        Каждая инструкция — **слой**. При пересборке Docker берёт слои из кэша, пока не встретит изменение; **всё после изменённого слоя пересобирается**.

        Поэтому `requirements.txt` копируют **до** остального кода: код меняется постоянно, а зависимости редко — и долгий `pip install` берётся из кэша.

        `.dockerignore` исключает лишнее из контекста сборки: `.git`, `.venv`, `__pycache__`, отчёты.
        """,
        out(f"{P}-m1-l2-e1", "Что выведет программа? Какой шаг сборки первым пересоберётся, если поменять только код тестов?", """
            steps = [
                ("FROM python:3.12-slim", []),
                ("COPY requirements.txt .", ["requirements.txt"]),
                ("RUN pip install -r requirements.txt", []),
                ("COPY . .", ["tests/test_login.py", "requirements.txt"]),
                ('CMD ["pytest"]', []),
            ]
            changed = {"tests/test_login.py"}
            for i, (cmd, files) in enumerate(steps):
                if changed & set(files):
                    print(i, cmd)
                    break
            """),
        cod(f"{P}-m1-l2-e2", t("""
            Напиши функцию `parse_dockerfile(text)`, которая разбирает Dockerfile на инструкции.

            - Получает: `text` — содержимое Dockerfile (многострочная строка).
            - Возвращает: список пар `(ИНСТРУКЦИЯ, аргументы)` — по одной паре на каждую значимую строку:
              - инструкция — первое слово строки, приведённое к **верхнему регистру**;
              - аргументы — всё после первого пробела, без пробелов по краям;
              - пустые строки и комментарии (начинаются с `#`) пропускаются.

            Пример:
            ```
            text = "# тесты\\nFROM python:3.12\\n\\nworkdir /app\\nRUN pip install -r requirements.txt\\n"
            parse_dockerfile(text)
            # → [("FROM", "python:3.12"), ("WORKDIR", "/app"), ("RUN", "pip install -r requirements.txt")]
            ```
            """),
            """
            def parse_dockerfile(text):
                pass
            """,
            """
            def test_parse():
                text = "# тесты\\nFROM python:3.12\\n\\nworkdir /app\\nRUN pip install -r requirements.txt\\n"
                assert parse_dockerfile(text) == [("FROM", "python:3.12"), ("WORKDIR", "/app"), ("RUN", "pip install -r requirements.txt")], \\
                    f"Получено {parse_dockerfile(text)}"
            """,
            """
            def parse_dockerfile(text):
                result = []
                for line in text.splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    instr, _, args = line.partition(" ")
                    result.append((instr.upper(), args.strip()))
                return result
            """,
            hint="`line.partition(\" \")` делит строку по первому пробелу."),
        cod(f"{P}-m1-l2-e3", t("""
            Напиши Dockerfile для запуска автотестов — строкой в переменной `DOCKERFILE`.

            Требования (инструкции по порядку):
            1. `FROM python:3.12-slim` — базовый образ (**первой** строкой);
            2. `WORKDIR /app` — рабочая папка;
            3. `COPY requirements.txt .` — сначала только файл зависимостей;
            4. `RUN pip install -r requirements.txt` — установка зависимостей;
            5. `COPY . .` — потом весь остальной код;
            6. `CMD`, который запускает `pytest` (**последней** строкой), например `CMD ["pytest", "-v"]`.

            Почему зависимости копируются отдельно и раньше кода — объяснено в теории про кэш слоёв.

            Тесты разберут твою строку построчно и проверят наличие и порядок инструкций.
            """),
            '''
            DOCKERFILE = """
            FROM ...
            """
            ''',
            DF_PARSE + dedent("""

            def test_from():
                ins = _instructions(DOCKERFILE)
                assert ins and ins[0] == ("FROM", "python:3.12-slim"), "Первая инструкция — FROM python:3.12-slim"

            def test_workdir():
                assert ("WORKDIR", "/app") in _instructions(DOCKERFILE), "Нужен WORKDIR /app"

            def test_cache_order():
                ins = _instructions(DOCKERFILE)
                names = [f"{i} {a}" for i, a in ins]
                req = next((k for k, s in enumerate(names) if s.startswith("COPY requirements.txt")), None)
                pip = next((k for k, s in enumerate(names) if s.startswith("RUN pip install -r requirements.txt")), None)
                code = next((k for k, s in enumerate(names) if s.startswith("COPY . ")), None)
                assert None not in (req, pip, code), "Нужны COPY requirements.txt, RUN pip install -r requirements.txt и COPY . ."
                assert req < pip < code, "Порядок для кэша: COPY requirements.txt → RUN pip install → COPY . ."

            def test_cmd():
                ins = _instructions(DOCKERFILE)
                assert ins[-1][0] == "CMD" and "pytest" in ins[-1][1], "Последняя инструкция — CMD с pytest"
            """),
            '''
            DOCKERFILE = """
            FROM python:3.12-slim
            WORKDIR /app
            COPY requirements.txt .
            RUN pip install -r requirements.txt
            COPY . .
            CMD ["pytest", "-v"]
            """
            ''',
            hint="Шесть строк: FROM, WORKDIR, COPY requirements.txt ., RUN pip install -r requirements.txt, COPY . ., CMD [\"pytest\"].", xp=25),
        cod(f"{P}-m1-l2-e4", t("""
            Напиши функцию `first_rebuilt(steps, changed)`: с какого шага Docker начнёт пересобирать образ.

            - Получает:
              - `steps` — шаги сборки: список пар `(команда, [файлы, которые шаг использует])`;
              - `changed` — **множество** изменённых файлов.
            - Возвращает: **индекс** первого шага, который использует хотя бы один изменённый файл (с него кэш перестаёт работать). Если ни один шаг не затронут — `None`.

            Пример:
            ```
            steps = [
                ("FROM python:3.12-slim", []),
                ("COPY requirements.txt .", ["requirements.txt"]),
                ("RUN pip install -r requirements.txt", []),
                ("COPY . .", ["app.py", "requirements.txt", "tests/test_api.py"]),
            ]
            first_rebuilt(steps, {"tests/test_api.py"})   # → 3
            first_rebuilt(steps, {"requirements.txt"})    # → 1
            first_rebuilt(steps, {"README.md"})           # → None
            ```
            Пересечение множеств: `changed & set(files)` — не пустое, если есть общие файлы.
            """),
            """
            def first_rebuilt(steps, changed):
                pass
            """,
            """
            STEPS = [
                ("FROM python:3.12-slim", []),
                ("COPY requirements.txt .", ["requirements.txt"]),
                ("RUN pip install -r requirements.txt", []),
                ("COPY . .", ["app.py", "requirements.txt", "tests/test_api.py"]),
            ]

            def test_code_change():
                assert first_rebuilt(STEPS, {"tests/test_api.py"}) == 3, "Изменение теста пересобирает с COPY . ."

            def test_requirements_change():
                assert first_rebuilt(STEPS, {"requirements.txt"}) == 1, "Изменение зависимостей — с COPY requirements.txt"

            def test_nothing():
                assert first_rebuilt(STEPS, {"README.md"}) is None, "Файл не используется в сборке → None"
            """,
            """
            def first_rebuilt(steps, changed):
                for i, (_, files) in enumerate(steps):
                    if changed & set(files):
                        return i
                return None
            """),
        cod(f"{P}-m1-l2-e5", t("""
            Напиши функцию `ignored(path, patterns)` — упрощённый `.dockerignore`.

            - Получает: `path` — путь к файлу через `/`, например `"app/__pycache__/x.pyc"`; `patterns` — список шаблонов.
            - Возвращает: `True`, если файл нужно исключить из сборки: **хотя бы одна часть пути** (кусок между `/`) подходит **хотя бы под один** шаблон. Иначе `False`.

            Шаблоны могут содержать `*` — «любые символы». Сравнивай через `fnmatch(часть, шаблон)`: `fnmatch("old.pyc", "*.pyc")` → `True`.

            Примеры (`patterns = [".git", ".venv", "__pycache__", "*.pyc", "reports"]`):
            ```
            ignored(".git/config", patterns)           # → True    часть ".git"
            ignored("tests/old.pyc", patterns)         # → True    "old.pyc" подходит под "*.pyc"
            ignored("tests/test_api.py", patterns)     # → False
            ```
            """),
            """
            from fnmatch import fnmatch

            def ignored(path, patterns):
                pass
            """,
            """
            PATTERNS = [".git", ".venv", "__pycache__", "*.pyc", "reports"]

            def test_ignored():
                assert ignored(".git/config", PATTERNS), ".git исключается"
                assert ignored("app/__pycache__/x.cpython.pyc", PATTERNS), "__pycache__ исключается"
                assert ignored("tests/old.pyc", PATTERNS), "*.pyc исключается"

            def test_kept():
                assert not ignored("tests/test_api.py", PATTERNS), "Тесты должны попасть в образ"
                assert not ignored("requirements.txt", PATTERNS), "requirements.txt нужен"
            """,
            """
            from fnmatch import fnmatch

            def ignored(path, patterns):
                return any(fnmatch(part, p) for part in path.split("/") for p in patterns)
            """,
            hint="`path.split(\"/\")` даёт части пути; `fnmatch(\"x.pyc\", \"*.pyc\")` → True.", xp=20),
    ),
)

m2 = module(f"{P}-m2", "CI/CD", "🚀", "Пайплайны, GitHub Actions и отчёты",
    lesson(f"{P}-m2-l1", "Пайплайн", """
        # CI и CD

        - **CI (Continuous Integration)** — на каждый push/pull request автоматически собрать проект и прогнать тесты.
        - **CD (Continuous Delivery/Deployment)** — если всё зелёное, автоматически выкатить на стенд или в прод.

        Типичный пайплайн — последовательность **стадий**:
        ```
        lint → unit → build (docker) → api-tests → ui-tests → deploy
        ```

        - **Fail fast**: быстрые проверки — первыми. Упал линтер — нет смысла 20 минут гонять UI-тесты.
        - Job-ы могут зависеть друг от друга (`needs:`) и идти параллельно, если не зависят.
        - **Артефакты** — файлы, которые job сохраняет: отчёты, скриншоты, логи.

        # Коды выхода

        CI смотрит только на код выхода команды: `0` — успех, иначе — провал.

        Коды выхода `pytest`:
        - `0` — все тесты прошли
        - `1` — есть упавшие тесты
        - `2` — прерван пользователем
        - `3` — внутренняя ошибка
        - `4` — ошибка в параметрах командной строки
        - `5` — не найдено ни одного теста (частая ошибка конфигурации!)
        """,
        out(f"{P}-m2-l1-e1", "Что выведет программа? Имитация пайплайна с fail fast.", """
            jobs = [("lint", 0), ("unit", 0), ("api-tests", 1), ("ui-tests", 0), ("deploy", 0)]
            for name, code in jobs:
                if code != 0:
                    print("❌", name)
                    break
                print("✅", name)
            else:
                print("🚀 всё зелёное")
            """, hint="`else` у цикла выполняется, только если не было break."),
        cod(f"{P}-m2-l1-e2", t("""
            Напиши функцию `pipeline_status(jobs)`, которая вычисляет итог CI-пайплайна.

            - Получает: `jobs` — список пар `(имя_job, код_выхода)` в порядке запуска. Код `0` — успех, любой другой — провал.
            - Возвращает:
              - `("failed", имя)` — где имя — **первого** упавшего job-а;
              - `("success", None)` — если все завершились с кодом 0.

            Примеры:
            ```
            pipeline_status([("lint", 0), ("unit", 1), ("ui", 1)])   # → ("failed", "unit")
            pipeline_status([("lint", 0), ("unit", 0)])              # → ("success", None)
            ```
            """),
            """
            def pipeline_status(jobs):
                pass
            """,
            """
            def test_failed():
                assert pipeline_status([("lint", 0), ("unit", 1), ("ui", 1)]) == ("failed", "unit"), "Первый упавший — unit"

            def test_success():
                assert pipeline_status([("lint", 0), ("unit", 0)]) == ("success", None), "Все с кодом 0 → success"
            """,
            """
            def pipeline_status(jobs):
                for name, code in jobs:
                    if code != 0:
                        return "failed", name
                return "success", None
            """),
        cod(f"{P}-m2-l1-e3", t("""
            Напиши функцию `pytest_exit(code)`, которая расшифровывает код выхода pytest.

            - Получает: `code` — число от 0 до 5.
            - Возвращает строку:
              - `0` → `"all passed"`
              - `1` → `"tests failed"`
              - `2` → `"interrupted"`
              - `3` → `"internal error"`
              - `4` → `"usage error"`
              - `5` → `"no tests collected"`

            Пример:
            ```
            pytest_exit(5)   # → "no tests collected"
            ```
            """),
            """
            def pytest_exit(code):
                pass
            """,
            """
            def test_codes():
                got = [pytest_exit(c) for c in range(6)]
                assert got == ["all passed", "tests failed", "interrupted", "internal error", "usage error", "no tests collected"], f"Получено {got}"
            """,
            """
            def pytest_exit(code):
                return ["all passed", "tests failed", "interrupted", "internal error", "usage error", "no tests collected"][code]
            """),
        cod(f"{P}-m2-l1-e4", t("""
            Напиши функцию `should_deploy(branch, jobs)`, которая решает, можно ли выкатывать релиз.

            - Получает: `branch` — имя git-ветки; `jobs` — список кодов выхода всех job-ов пайплайна.
            - Возвращает `True`, только если выполнены **оба** условия:
              1. ветка — `"main"`;
              2. **все** коды выхода равны `0`.

            Примеры:
            ```
            should_deploy("main", [0, 0, 0])          # → True
            should_deploy("feature/login", [0, 0])    # → False   не main
            should_deploy("main", [0, 1])             # → False   есть упавший job
            ```
            """),
            """
            def should_deploy(branch, jobs):
                pass
            """,
            """
            def test_main_green():
                assert should_deploy("main", [0, 0, 0]) is True, "main + всё зелёное → деплой"

            def test_feature_branch():
                assert should_deploy("feature/login", [0, 0]) is False, "Не main → не деплоим"

            def test_red():
                assert should_deploy("main", [0, 1]) is False, "Есть упавший job → не деплоим"
            """,
            """
            def should_deploy(branch, jobs):
                return branch == "main" and all(code == 0 for code in jobs)
            """),
        cod(f"{P}-m2-l1-e5", t("""
            Напиши функцию `run_order(needs)`, которая определяет порядок запуска job-ов с зависимостями.

            - Получает: `needs` — словарь `{job: [список job-ов, от которых он зависит]}`. Job можно запустить только когда **все** его зависимости уже выполнены.
            - Возвращает: список всех job-ов в порядке запуска. Если одновременно готовы несколько — сначала запускается тот, чьё имя раньше **по алфавиту**, и после него готовность пересчитывается заново.

            Пример:
            ```
            run_order({
                "deploy":    ["api-tests", "ui-tests"],
                "api-tests": ["build"],
                "ui-tests":  ["build"],
                "build":     ["lint", "unit"],
                "lint":      [],
                "unit":      [],
            })
            # → ["lint", "unit", "build", "api-tests", "ui-tests", "deploy"]
            ```
            Алгоритм: пока не все выполнены — найди готовые (ещё не выполнен и все зависимости выполнены), отсортируй, возьми первый.
            """),
            """
            def run_order(needs):
                pass
            """,
            """
            def test_pipeline():
                needs = {
                    "deploy": ["api-tests", "ui-tests"],
                    "api-tests": ["build"],
                    "ui-tests": ["build"],
                    "build": ["lint", "unit"],
                    "lint": [],
                    "unit": [],
                }
                assert run_order(needs) == ["lint", "unit", "build", "api-tests", "ui-tests", "deploy"], f"Получено {run_order(needs)}"

            def test_independent():
                assert run_order({"b": [], "a": []}) == ["a", "b"], "Независимые — по алфавиту"
            """,
            """
            def run_order(needs):
                done = []
                while len(done) < len(needs):
                    ready = sorted(j for j, deps in needs.items() if j not in done and all(d in done for d in deps))
                    done.append(ready[0])
                return done
            """,
            hint="Пока не все выполнены: найди готовые (не выполнен, все зависимости в done), отсортируй, возьми первый.", xp=25),
    ),
    lesson(f"{P}-m2-l2", "GitHub Actions и отчёты", """
        # Workflow в GitHub Actions

        Файл `.github/workflows/tests.yml`:

        ```
        name: tests
        on: [push, pull_request]

        jobs:
          test:
            runs-on: ubuntu-latest
            strategy:
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
                  API_TOKEN: ${{ secrets.API_TOKEN }}
              - uses: actions/upload-artifact@v4
                if: always()
                with:
                  name: reports-${{ matrix.python }}
                  path: reports/
        ```

        - `on` — когда запускать. `runs-on` — на какой машине.
        - `uses` — готовое действие, `run` — shell-команда.
        - `matrix` — запустить job для всех комбинаций параметров.
        - `secrets` — пароли и токены. GitHub **маскирует** их в логах как `***`.
        - `if: always()` — сохранить отчёт, даже если тесты упали (особенно если упали!).

        **JUnit XML** — универсальный формат отчёта о тестах, его понимают GitHub, GitLab, Jenkins, Allure.
        """,
        out(f"{P}-m2-l2-e1", "Что выведет программа? Секреты маскируются в логах.", """
            log = "login with token=abc123 to https://user:pa55@host"
            for secret in ["abc123", "pa55"]:
                log = log.replace(secret, "***")
            print(log)
            """),
        cod(f"{P}-m2-l2-e2", t("""
            Напиши workflow для GitHub Actions — строкой YAML в переменной `WORKFLOW`.

            Требования:
            1. запуск на событиях `push` **и** `pull_request`;
            2. job работает на `runs-on: ubuntu-latest`;
            3. шаги по порядку:
               - `uses: actions/checkout@v4` — скачать код репозитория;
               - `uses: actions/setup-python@v5` — установить Python;
               - `run: pip install -r requirements.txt` — установить зависимости;
               - `run: pytest` — запустить тесты (**после** установки зависимостей).

            За основу возьми пример из теории и упрости его: матрица и артефакты не нужны. Следи за отступами — в YAML они важны.
            """),
            '''
            WORKFLOW = """
            name: tests
            on: [push]
            """
            ''',
            """
            import re

            def lines():
                return [l.strip() for l in WORKFLOW.splitlines() if l.strip()]

            def test_triggers():
                on = next((l for l in lines() if l.startswith("on:")), "")
                text = WORKFLOW
                assert "push" in on or re.search(r"^\\s*push:", text, re.M), "Нужен триггер push"
                assert "pull_request" in text, "Нужен триггер pull_request"

            def test_runner():
                assert "runs-on: ubuntu-latest" in lines(), "Нужно runs-on: ubuntu-latest"

            def test_steps():
                text = WORKFLOW
                assert "actions/checkout" in text, "Нужен шаг actions/checkout — без него в раннере нет кода"
                assert "actions/setup-python" in text, "Нужен шаг actions/setup-python"
                assert "pip install -r requirements.txt" in text, "Нужна установка зависимостей"

            def test_pytest_after_install():
                text = WORKFLOW
                assert "pytest" in text, "Нужен запуск pytest"
                assert text.index("pip install -r requirements.txt") < text.rindex("pytest"), "pytest запускается после установки зависимостей"
            """,
            '''
            WORKFLOW = """
            name: tests
            on: [push, pull_request]

            jobs:
              test:
                runs-on: ubuntu-latest
                steps:
                  - uses: actions/checkout@v4
                  - uses: actions/setup-python@v5
                    with:
                      python-version: "3.12"
                  - run: pip install -r requirements.txt
                  - run: pytest
            """
            ''',
            hint="Возьми пример из теории и упрости: без matrix и артефактов.", xp=25),
        cod(f"{P}-m2-l2-e3", t("""
            Напиши функцию `mask_secrets(log, secrets)`, которая прячет секреты в логах CI.

            - Получает: `log` — текст лога; `secrets` — список секретных значений (пароли, токены).
            - Возвращает: лог, в котором каждое вхождение каждого секрета заменено на `***`.
            - Пустые строки в `secrets` нужно **пропускать** — иначе замена пустой строки испортит весь текст.

            Примеры:
            ```
            mask_secrets("token=abc pass=xyz", ["abc", "xyz"])   # → "token=*** pass=***"
            mask_secrets("hello", [""])                          # → "hello"
            ```
            """),
            """
            def mask_secrets(log, secrets):
                pass
            """,
            """
            def test_mask():
                assert mask_secrets("token=abc pass=xyz", ["abc", "xyz"]) == "token=*** pass=***", f"Получено {mask_secrets('token=abc pass=xyz', ['abc', 'xyz'])!r}"

            def test_empty_secret():
                assert mask_secrets("hello", [""]) == "hello", "Пустой секрет не должен ничего ломать"
            """,
            """
            def mask_secrets(log, secrets):
                for s in secrets:
                    if s:
                        log = log.replace(s, "***")
                return log
            """),
        cod(f"{P}-m2-l2-e4", t("""
            Напиши функцию `matrix_jobs(matrix)`, которая разворачивает матрицу GitHub Actions в список запусков.

            - Получает: `matrix` — словарь `{параметр: [возможные значения]}`.
            - Возвращает: список словарей — по одному на **каждую комбинацию** значений. Порядок — как у `itertools.product`: первый параметр меняется медленнее всех.

            Примеры:
            ```
            matrix_jobs({"python": ["3.11", "3.12"], "os": ["ubuntu", "windows"]})
            # → [{"python": "3.11", "os": "ubuntu"},
            #    {"python": "3.11", "os": "windows"},
            #    {"python": "3.12", "os": "ubuntu"},
            #    {"python": "3.12", "os": "windows"}]

            matrix_jobs({"browser": ["chrome"]})   # → [{"browser": "chrome"}]
            ```
            `product(*matrix.values())` даёт кортежи значений, а `dict(zip(ключи, кортеж))` превращает кортеж в словарь.
            """),
            """
            from itertools import product

            def matrix_jobs(matrix):
                pass
            """,
            """
            def test_matrix():
                got = matrix_jobs({"python": ["3.11", "3.12"], "os": ["ubuntu", "windows"]})
                assert got == [
                    {"python": "3.11", "os": "ubuntu"},
                    {"python": "3.11", "os": "windows"},
                    {"python": "3.12", "os": "ubuntu"},
                    {"python": "3.12", "os": "windows"},
                ], f"Получено {got}"

            def test_single():
                assert matrix_jobs({"browser": ["chrome"]}) == [{"browser": "chrome"}], "Один параметр — одна комбинация"
            """,
            """
            from itertools import product

            def matrix_jobs(matrix):
                keys = list(matrix)
                return [dict(zip(keys, combo)) for combo in product(*matrix.values())]
            """,
            hint="`product(*matrix.values())` даёт кортежи значений; `dict(zip(keys, combo))` превращает их в словари.", xp=20),
        cod(f"{P}-m2-l2-e5", t("""
            Напиши функцию `junit_summary(xml_text)`, которая читает отчёт о тестах в формате JUnit XML.

            Такой отчёт создаёт `pytest --junitxml=...`: каждый тест — тег `<testcase name="...">`. Внутри упавшего теста есть тег `<failure>` или `<error>`, внутри пропущенного — `<skipped>`.

            - Получает: `xml_text` — текст отчёта.
            - Возвращает словарь:
              - `"total"` — сколько всего `<testcase>` (на любой глубине);
              - `"failed"` — сколько из них содержат `<failure>` **или** `<error>`;
              - `"skipped"` — сколько содержат `<skipped>`;
              - `"failed_names"` — список атрибутов `name` упавших тестов, в порядке в отчёте.

            Пример результата для отчёта из 4 тестов, где один упал с failure, один с error и один пропущен:
            ```
            {"total": 4, "failed": 2, "skipped": 1, "failed_names": ["test_create_user", "test_login"]}
            ```
            Разобрать XML: `root = ET.fromstring(xml_text)`; все testcase: `root.iter("testcase")`; есть ли вложенный тег: `case.find("failure") is not None`; атрибут: `case.get("name")`.
            """),
            """
            import xml.etree.ElementTree as ET

            def junit_summary(xml_text):
                pass
            """,
            """
            REPORT = '''<testsuites>
              <testsuite name="api" tests="4">
                <testcase name="test_get_user" time="0.1"/>
                <testcase name="test_create_user" time="0.2"><failure message="assert 200 == 201"/></testcase>
                <testcase name="test_delete" time="0.1"><skipped/></testcase>
              </testsuite>
              <testsuite name="ui" tests="1">
                <testcase name="test_login" time="3.1"><error message="TimeoutError"/></testcase>
              </testsuite>
            </testsuites>'''

            def test_summary():
                got = junit_summary(REPORT)
                assert got == {"total": 4, "failed": 2, "skipped": 1, "failed_names": ["test_create_user", "test_login"]}, f"Получено {got}"
            """,
            """
            import xml.etree.ElementTree as ET

            def junit_summary(xml_text):
                root = ET.fromstring(xml_text)
                cases = list(root.iter("testcase"))
                failed = [c for c in cases if c.find("failure") is not None or c.find("error") is not None]
                return {
                    "total": len(cases),
                    "failed": len(failed),
                    "skipped": sum(1 for c in cases if c.find("skipped") is not None),
                    "failed_names": [c.get("name") for c in failed],
                }
            """,
            hint="`root.iter(\"testcase\")` найдёт все testcase на любой глубине; `case.find(\"failure\") is not None` — есть ли вложенный тег.", xp=25),
    ),
)

TOPIC = topic("docker-ci", "Docker и CI/CD", "🐳", "#2496ed",
              "Контейнеры, Dockerfile, пайплайны и GitHub Actions для тестировщика", m1, m2, group="Тестирование и DevOps")
