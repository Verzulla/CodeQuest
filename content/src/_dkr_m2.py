"""Тема «Docker для тестировщика», модуль 2 «Dockerfile и сборка» — задания. Теория — в _dkr_t2.py.

Урок dci-m1-l2 унаследован от старой темы «Docker и CI/CD» — так сохраняется прогресс."""
from textwrap import dedent

from ._lib import cmd, cod, lesson, module, out, t
from ._dkr_m1 import anyorder

P = "dkr"
O = "dci"

# Разбор Dockerfile в проверках: [(ИНСТРУКЦИЯ, аргументы)], без пустых строк и комментариев.
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


def df(body):
    """Проверки задания «напиши Dockerfile строкой»: разборщик + тесты."""
    return DF_PARSE + dedent(body)


m2 = module(f"{P}-m2", "Dockerfile и сборка", "🧱", "Слои и кэш, инструкции Dockerfile, автотесты в контейнере, размер и безопасность образа",

lesson(f"{O}-m1-l2", "Dockerfile и слои",
    out(f"{O}-m1-l2-e1", "Что выведет программа? Какой шаг сборки первым пересоберётся, если поменять только код тестов?", """
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
    cod(f"{O}-m1-l2-e2", t("""
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
    cod(f"{O}-m1-l2-e3", t("""
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
    cod(f"{O}-m1-l2-e4", t("""
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
    cod(f"{O}-m1-l2-e5", t("""
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
    cmd(f"{O}-m1-l2-e6", "Собери образ из `Dockerfile` в текущей папке и назови его `my-tests`.",
        ["docker build -t my-tests .", "docker build --tag my-tests .", "docker build . -t my-tests", "docker image build -t my-tests ."],
        hint="`docker build -t имя .` — точка в конце: контекст сборки."),
    cmd(f"{O}-m1-l2-e7", "Кэш слоёв подвёл (например, `apt-get update` взялся из кэша недельной давности). Пересобери `my-tests` **без кэша**.",
        ["docker build --no-cache -t my-tests .", anyorder("docker build", ["--no-cache", "-t my-tests"], "."),
         anyorder("docker build", ["--no-cache", "--tag my-tests"], ".")],
        hint="Флаг `--no-cache`."),
    cmd(f"{O}-m1-l2-e8", "Посмотри, из каких слоёв состоит образ `my-tests` и сколько весит каждый.",
        ["docker history my-tests", "docker image history my-tests"],
        hint="`docker history образ`."),
),

lesson(f"{P}-instructions", "Инструкции: ENV, ARG, CMD и ENTRYPOINT",
    out(f"{P}-instructions-e1", "Что выведет программа? CMD в **exec-форме** — это JSON-список аргументов, а в **shell-форме** — строка для `/bin/sh -c`.", """
        import json
        import shlex

        exec_form = '["pytest", "-v", "-m", "smoke and not slow"]'
        shell_form = 'pytest -v -m "smoke and not slow"'
        print(json.loads(exec_form))
        print(shlex.split(shell_form))
        print(json.loads(exec_form) == shlex.split(shell_form))
        """),
    cod(f"{P}-instructions-e2", t("""
        Напиши функцию `final_command(entrypoint, cmd, run_args)`, которая определяет, какую команду выполнит контейнер.

        Правила Docker (всё — списки строк):
        - аргументы из `docker run образ АРГУМЕНТЫ` (`run_args`) **заменяют** `CMD`;
        - итог — `ENTRYPOINT + (run_args, если они есть, иначе CMD)`.

        Примеры:
        ```
        final_command(["pytest"], ["-v"], [])                  # → ["pytest", "-v"]
        final_command(["pytest"], ["-v"], ["-m", "smoke"])     # → ["pytest", "-m", "smoke"]
        final_command([], ["pytest", "-v"], ["bash"])          # → ["bash"]
        ```
        """),
        """
        def final_command(entrypoint, cmd, run_args):
            pass
        """,
        """
        def test_rules():
            assert final_command(["pytest"], ["-v"], []) == ["pytest", "-v"]
            assert final_command(["pytest"], ["-v"], ["-m", "smoke"]) == ["pytest", "-m", "smoke"], "Аргументы run заменяют CMD"
            assert final_command([], ["pytest", "-v"], ["bash"]) == ["bash"], "Без ENTRYPOINT аргументы run — вся команда"
            assert final_command(["pytest"], [], []) == ["pytest"]
        """,
        """
        def final_command(entrypoint, cmd, run_args):
            return entrypoint + (run_args or cmd)
        """),
    cod(f"{P}-instructions-e3", t("""
        Напиши Dockerfile строкой в переменной `DOCKERFILE`, где версия Python и адрес стенда настраиваются:

        1. `ARG PYTHON_VERSION=3.12` — аргумент сборки (**до** `FROM`, чтобы его можно было использовать в `FROM`);
        2. `FROM python:${PYTHON_VERSION}-slim`;
        3. `WORKDIR /app`, `COPY . .`, `RUN pip install -r requirements.txt`;
        4. `ENV BASE_URL=http://app:8000` — адрес по умолчанию, его можно переопределить через `docker run -e`;
        5. `ENTRYPOINT ["pytest"]` и `CMD ["-v"]` — `pytest` запускается всегда, а аргументы по умолчанию можно заменить.
        """),
        '''
        DOCKERFILE = """
        FROM python:3.12-slim
        """
        ''',
        df("""

        def test_arg_before_from():
            ins = _instructions(DOCKERFILE)
            assert ins[0] == ("ARG", "PYTHON_VERSION=3.12"), "Первая строка — ARG PYTHON_VERSION=3.12"
            assert ins[1] == ("FROM", "python:${PYTHON_VERSION}-slim"), "Затем FROM python:${PYTHON_VERSION}-slim"

        def test_env():
            assert ("ENV", "BASE_URL=http://app:8000") in _instructions(DOCKERFILE), "Нужен ENV BASE_URL=http://app:8000"

        def test_entrypoint_cmd():
            import json
            ins = dict(_instructions(DOCKERFILE))
            assert json.loads(ins.get("ENTRYPOINT", "null")) == ["pytest"], 'ENTRYPOINT ["pytest"] в exec-форме'
            assert json.loads(ins.get("CMD", "null")) == ["-v"], 'CMD ["-v"] в exec-форме'
            assert ("RUN", "pip install -r requirements.txt") in _instructions(DOCKERFILE), "Установи зависимости"
        """),
        '''
        DOCKERFILE = """
        ARG PYTHON_VERSION=3.12
        FROM python:${PYTHON_VERSION}-slim
        WORKDIR /app
        COPY . .
        RUN pip install -r requirements.txt
        ENV BASE_URL=http://app:8000
        ENTRYPOINT ["pytest"]
        CMD ["-v"]
        """
        ''', xp=20),
    cmd(f"{P}-instructions-e4", "Собери образ `my-tests`, передав аргумент сборки `PYTHON_VERSION=3.11`.",
        ["docker build --build-arg PYTHON_VERSION=3.11 -t my-tests .",
         anyorder("docker build", ["--build-arg PYTHON_VERSION=3.11", "-t my-tests"], "."),
         anyorder("docker build", ["--build-arg PYTHON_VERSION=3.11", "--tag my-tests"], ".")],
        hint="`--build-arg ИМЯ=значение`."),
    cod(f"{P}-instructions-e5", t("""
        Напиши простой линтер `lint_dockerfile(text)`, который ищет типичные ошибки. Возвращает **отсортированный** список кодов найденных проблем:

        - `"latest"` — в `FROM` нет тега или тег `latest` (`FROM python`, `FROM python:latest`);
        - `"add"` — используется `ADD` (для локальных файлов нужен `COPY`);
        - `"no-user"` — нет инструкции `USER` (контейнер работает от root);
        - `"pip-cache"` — есть `RUN pip install` без `--no-cache-dir` (кэш pip раздувает образ).

        Пустые строки и комментарии пропускай; регистр инструкций не важен.
        """),
        """
        def lint_dockerfile(text):
            pass
        """,
        """
        BAD = "FROM python\\nADD . /app\\nRUN pip install -r requirements.txt\\nCMD [\\"pytest\\"]"
        GOOD = "# ok\\nFROM python:3.12-slim\\nCOPY . /app\\nRUN pip install --no-cache-dir -r requirements.txt\\nUSER nobody\\nCMD [\\"pytest\\"]"

        def test_bad():
            assert lint_dockerfile(BAD) == ["add", "latest", "no-user", "pip-cache"], lint_dockerfile(BAD)

        def test_good():
            assert lint_dockerfile(GOOD) == [], lint_dockerfile(GOOD)

        def test_latest_tag():
            assert "latest" in lint_dockerfile("from node:latest\\nuser node")
        """,
        """
        def lint_dockerfile(text):
            problems = set()
            has_user = False
            for line in text.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                instr, _, args = line.partition(" ")
                instr = instr.upper()
                if instr == "FROM":
                    image = args.split()[0]
                    last = image.split("/")[-1]
                    if ":" not in last or last.endswith(":latest"):
                        problems.add("latest")
                elif instr == "ADD":
                    problems.add("add")
                elif instr == "USER":
                    has_user = True
                elif instr == "RUN" and "pip install" in args and "--no-cache-dir" not in args:
                    problems.add("pip-cache")
            if not has_user:
                problems.add("no-user")
            return sorted(problems)
        """, xp=20),
    out(f"{P}-instructions-e6", "Что выведет программа? Переменные окружения контейнера: `ENV` из Dockerfile — значения по умолчанию, `-e` при запуске — переопределяет.", """
        dockerfile_env = {"BASE_URL": "http://app:8000", "HEADLESS": "true"}
        run_env = {"BASE_URL": "http://stage.test", "BROWSER": "firefox"}
        env = {**dockerfile_env, **run_env}
        for name in sorted(env):
            print(f"{name}={env[name]}")
        """),
    cmd(f"{P}-instructions-e7", "В образе `my-tests` задано `ENTRYPOINT [\"pytest\"]` и `CMD [\"-v\"]`. Запусти его (с `--rm`) так, чтобы выполнилось `pytest -m smoke`.",
        ["docker run --rm my-tests -m smoke", r"re:docker run --rm my-tests -m (smoke|'smoke'|\"smoke\")"],
        context="""
        ENTRYPOINT ["pytest"]
        CMD ["-v"]
        """,
        hint="Всё после имени образа заменяет CMD, а ENTRYPOINT остаётся."),
    cod(f"{P}-instructions-e8", t("""
        Docker (и Compose) подставляют переменные в строки: `${VAR}` — значение, `${VAR:-default}` — значение или `default`, если переменной нет или она пустая.

        Напиши функцию `expand(text, env)`, которая делает такую подстановку. Переменной нет и значения по умолчанию нет — подставь пустую строку.

        Примеры:
        ```
        env = {"PY": "3.12", "EMPTY": ""}
        expand("python:${PY}-slim", env)               # → "python:3.12-slim"
        expand("${URL:-http://app:8000}/api", env)     # → "http://app:8000/api"
        expand("[${EMPTY:-x}] [${NOPE}]", env)         # → "[x] []"
        ```
        Удобно через `re.sub(r"\\$\\{(\\w+)(?::-([^}]*))?\\}", функция, text)`.
        """),
        """
        import re


        def expand(text, env):
            pass
        """,
        """
        def test_expand():
            env = {"PY": "3.12", "EMPTY": ""}
            assert expand("python:${PY}-slim", env) == "python:3.12-slim"
            assert expand("${URL:-http://app:8000}/api", env) == "http://app:8000/api"
            assert expand("[${EMPTY:-x}] [${NOPE}]", env) == "[x] []", expand("[${EMPTY:-x}] [${NOPE}]", env)
            assert expand("no vars", env) == "no vars"
        """,
        """
        import re


        def expand(text, env):
            def replace(m):
                name, default = m.group(1), m.group(2)
                value = env.get(name, "")
                if default is not None and not value:
                    return default
                return value
            return re.sub(r"\\$\\{(\\w+)(?::-([^}]*))?\\}", replace, text)
        """,
        hint="В функции-замене `m.group(2)` — значение по умолчанию или `None`, если его нет.", xp=20),
),

lesson(f"{P}-tests", "Автотесты в контейнере",
    cod(f"{P}-tests-e1", t("""
        Напиши Dockerfile для прогона автотестов строкой `DOCKERFILE`:

        1. `FROM python:3.12-slim`, `WORKDIR /app`;
        2. `COPY requirements.txt .` и `RUN pip install --no-cache-dir -r requirements.txt` — зависимости отдельным слоем и без кэша pip;
        3. `COPY . .`;
        4. `CMD` в exec-форме, который запускает `pytest` с отчётом `--junitxml=reports/junit.xml` — например, `CMD ["pytest", "--junitxml=reports/junit.xml"]`.
        """),
        '''
        DOCKERFILE = """
        FROM python:3.12-slim
        """
        ''',
        df("""

        def test_layers():
            ins = _instructions(DOCKERFILE)
            names = [f"{i} {a}" for i, a in ins]
            assert names[0] == "FROM python:3.12-slim" and "WORKDIR /app" in names, "FROM python:3.12-slim и WORKDIR /app"
            req = names.index("COPY requirements.txt .") if "COPY requirements.txt ." in names else None
            pip = next((k for k, s in enumerate(names) if s.startswith("RUN pip install") and "-r requirements.txt" in s), None)
            code = names.index("COPY . .") if "COPY . ." in names else None
            assert None not in (req, pip, code) and req < pip < code, "Порядок: COPY requirements.txt . → RUN pip install → COPY . ."
            assert "--no-cache-dir" in names[pip], "pip install с --no-cache-dir"

        def test_cmd():
            import json
            instr, args = _instructions(DOCKERFILE)[-1]
            assert instr == "CMD", "Последняя инструкция — CMD"
            argv = json.loads(args)
            assert argv[0] == "pytest" and "--junitxml=reports/junit.xml" in argv, f'CMD ["pytest", "--junitxml=reports/junit.xml"], а сейчас {argv}'
        """),
        '''
        DOCKERFILE = """
        FROM python:3.12-slim
        WORKDIR /app
        COPY requirements.txt .
        RUN pip install --no-cache-dir -r requirements.txt
        COPY . .
        CMD ["pytest", "--junitxml=reports/junit.xml"]
        """
        ''', xp=20),
    cmd(f"{P}-tests-e2", "Запусти образ `my-tests` (с `--rm`) на стенде `BASE_URL=http://stage.test` и забери отчёты: папка `reports` текущей директории хоста → `/app/reports` в контейнере (через `$(pwd)`).",
        ["docker run --rm -e BASE_URL=http://stage.test -v $(pwd)/reports:/app/reports my-tests",
         anyorder("docker run", ["--rm", "-e BASE_URL=http://stage.test", "-v $(pwd)/reports:/app/reports"], "my-tests"),
         anyorder("docker run", ["--rm", "-e BASE_URL=http://stage.test", "-v ${PWD}/reports:/app/reports"], "my-tests"),
         anyorder("docker run", ["--rm", "-e BASE_URL=http://stage.test", '-v "$(pwd)/reports:/app/reports"'], "my-tests"),
         anyorder("docker run", ["--rm", "-e BASE_URL=http://stage.test", "-v ./reports:/app/reports"], "my-tests")],
        hint="`-e` для переменной и `-v` для папки."),
    cmd(f"{P}-tests-e3", "В образе `my-tests` задано `CMD [\"pytest\"]`. Запусти (с `--rm`) только тесты с маркером `smoke`.",
        ["docker run --rm my-tests pytest -m smoke", r"re:docker run --rm my-tests pytest -m (smoke|'smoke'|\"smoke\")"],
        hint="Команда после имени образа заменяет CMD целиком."),
    cod(f"{P}-tests-e4", t("""
        Напиши содержимое `.dockerignore` строкой `DOCKERIGNORE` — по шаблону на строку. В контекст сборки не должны попасть:

        `.git`, `.venv`, `__pycache__`, `*.pyc`, `reports`, `allure-results`, `.pytest_cache`.
        """),
        '''
        DOCKERIGNORE = """
        .git
        """
        ''',
        """
        NEED = {".git", ".venv", "__pycache__", "*.pyc", "reports", "allure-results", ".pytest_cache"}

        def test_patterns():
            got = {line.strip() for line in DOCKERIGNORE.splitlines() if line.strip() and not line.strip().startswith("#")}
            missing = NEED - got
            assert not missing, f"Не хватает: {sorted(missing)}"
        """,
        '''
        DOCKERIGNORE = """
        .git
        .venv
        __pycache__
        *.pyc
        .pytest_cache
        reports
        allure-results
        """
        '''),
    cod(f"{P}-tests-e5", t("""
        Напиши функцию `docker_test_cmd(image, reports, env, args)`, которая собирает список аргументов для `subprocess.run` — запуск тестов в контейнере:

        ```
        ["docker", "run", "--rm", "-v", "<reports>:/app/reports", "-e", "ИМЯ=значение", …, image, *args]
        ```
        - переменные из `env` — по алфавиту имён, каждая через отдельный `-e`;
        - `args` — аргументы после образа (может быть пустым списком).

        Пример:
        ```
        docker_test_cmd("my-tests", "/ci/reports", {"BASE_URL": "http://stage"}, ["pytest", "-m", "smoke"])
        # → ["docker", "run", "--rm", "-v", "/ci/reports:/app/reports", "-e", "BASE_URL=http://stage", "my-tests", "pytest", "-m", "smoke"]
        ```
        """),
        """
        def docker_test_cmd(image, reports, env, args):
            pass
        """,
        """
        def test_full():
            got = docker_test_cmd("my-tests", "/ci/reports", {"BASE_URL": "http://stage"}, ["pytest", "-m", "smoke"])
            assert got == ["docker", "run", "--rm", "-v", "/ci/reports:/app/reports", "-e", "BASE_URL=http://stage", "my-tests", "pytest", "-m", "smoke"], got

        def test_sorted_env():
            got = docker_test_cmd("t", "/r", {"B": "2", "A": "1"}, [])
            assert got == ["docker", "run", "--rm", "-v", "/r:/app/reports", "-e", "A=1", "-e", "B=2", "t"], got
        """,
        """
        def docker_test_cmd(image, reports, env, args):
            cmd = ["docker", "run", "--rm", "-v", f"{reports}:/app/reports"]
            for name in sorted(env):
                cmd += ["-e", f"{name}={env[name]}"]
            return cmd + [image, *args]
        """),
    out(f"{P}-tests-e6", "Что выведет программа? CI узнаёт результат тестов только по коду выхода: `docker run` возвращает код команды внутри контейнера.", """
        def container_exit(results):
            return 0 if all(r == "passed" for r in results.values()) else 1

        for run in [{"test_login": "passed", "test_cart": "passed"},
                    {"test_login": "passed", "test_cart": "failed"}]:
            code = container_exit(run)
            print(code, "зелёный" if code == 0 else "красный")
        """),
    cod(f"{P}-tests-e7", t("""
        Для UI-тестов на Playwright есть официальный образ с уже установленными браузерами. Напиши `DOCKERFILE`:

        1. `FROM mcr.microsoft.com/playwright/python:v1.47.0-noble` — базовый образ с **зафиксированной** версией;
        2. `WORKDIR /app`;
        3. `COPY requirements.txt .`, `RUN pip install --no-cache-dir -r requirements.txt`, `COPY . .`;
        4. `CMD ["pytest", "--browser", "chromium"]`.
        """),
        '''
        DOCKERFILE = """
        FROM ...
        """
        ''',
        df("""

        def test_from():
            ins = _instructions(DOCKERFILE)
            assert ins and ins[0][0] == "FROM", "Первая инструкция — FROM"
            image = ins[0][1]
            assert image.startswith("mcr.microsoft.com/playwright/python:"), "Базовый образ — mcr.microsoft.com/playwright/python"
            assert not image.endswith(":latest"), "Зафиксируй версию, не latest"

        def test_rest():
            import json
            ins = _instructions(DOCKERFILE)
            assert ("WORKDIR", "/app") in ins and ("COPY", "requirements.txt .") in ins and ("COPY", ". .") in ins
            assert any(i == "RUN" and "pip install" in a and "--no-cache-dir" in a for i, a in ins), "pip install --no-cache-dir"
            assert ins[-1][0] == "CMD" and json.loads(ins[-1][1]) == ["pytest", "--browser", "chromium"], 'CMD ["pytest", "--browser", "chromium"]'
        """),
        '''
        DOCKERFILE = """
        FROM mcr.microsoft.com/playwright/python:v1.47.0-noble
        WORKDIR /app
        COPY requirements.txt .
        RUN pip install --no-cache-dir -r requirements.txt
        COPY . .
        CMD ["pytest", "--browser", "chromium"]
        """
        '''),
    cmd(f"{P}-tests-e8", "Контейнер с тестами завершился. Выведи в терминал **код выхода** последней выполненной команды.",
        ["echo $?"],
        hint="Специальная переменная оболочки `$?`."),
),

lesson(f"{P}-optimize", "Размер, кэш и безопасность",
    out(f"{P}-optimize-e1", "Что выведет программа? Размер образа — сумма размеров слоёв.", """
        layers = [
            ("FROM python:3.12-slim", 125.4),
            ("RUN pip install -r requirements.txt", 310.2),
            ("COPY . .", 1.6),
        ]
        total = sum(size for _, size in layers)
        print(f"{total:.1f} MB")
        biggest = max(layers, key=lambda layer: layer[1])
        print(biggest[0])
        """),
    cod(f"{P}-optimize-e2", t("""
        Напиши функцию `biggest_layers(layers, n)`: из списка слоёв `(команда, размер_в_МБ)` верни команды **n** самых тяжёлых слоёв — от большего к меньшему.

        Пример:
        ```
        biggest_layers([("FROM", 125), ("RUN apt-get", 210), ("COPY", 2), ("RUN pip", 310)], 2)
        # → ["RUN pip", "RUN apt-get"]
        ```
        """),
        """
        def biggest_layers(layers, n):
            pass
        """,
        """
        def test_top():
            layers = [("FROM", 125), ("RUN apt-get", 210), ("COPY", 2), ("RUN pip", 310)]
            assert biggest_layers(layers, 2) == ["RUN pip", "RUN apt-get"], biggest_layers(layers, 2)
            assert biggest_layers(layers, 10) == ["RUN pip", "RUN apt-get", "FROM", "COPY"]
        """,
        """
        def biggest_layers(layers, n):
            ordered = sorted(layers, key=lambda layer: layer[1], reverse=True)
            return [command for command, _ in ordered[:n]]
        """),
    cod(f"{P}-optimize-e3", t("""
        **Многоэтапная сборка** (multi-stage): в первом, «толстом» этапе собираем зависимости, во второй, лёгкий образ копируем только результат. Напиши `DOCKERFILE`:

        ```
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
        Проверка убедится, что этапов два, первый назван `builder`, финальный — на `slim`, колёса копируются `COPY --from=builder`, а тесты запускаются не от root.
        """),
        '''
        DOCKERFILE = """
        FROM python:3.12
        """
        ''',
        df("""

        def test_stages():
            froms = [a for i, a in _instructions(DOCKERFILE) if i == "FROM"]
            assert len(froms) == 2, f"Нужно два этапа (два FROM), а сейчас {len(froms)}"
            assert froms[0].replace(" as ", " AS ").endswith(" AS builder"), "Первый этап: FROM ... AS builder"
            assert froms[1] == "python:3.12-slim", "Финальный этап — python:3.12-slim"

        def test_copy_from():
            ins = _instructions(DOCKERFILE)
            assert any(i == "COPY" and a.startswith("--from=builder") for i, a in ins), "Скопируй результат: COPY --from=builder ..."
            assert any(i == "USER" and a != "root" for i, a in ins), "Запускай не от root: USER nobody"
            assert ins[-1][0] == "CMD", "Последняя инструкция — CMD"
        """),
        '''
        DOCKERFILE = """
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
        """
        ''', xp=20),
    cod(f"{P}-optimize-e4", t("""
        Секреты (пароли, токены) нельзя «запекать» в образ: любой, кто скачал образ, увидит их в `docker history`. Напиши функцию `find_secrets(text)`, которая находит в Dockerfile подозрительные `ENV` и `ARG`.

        - Проверяются строки `ENV ИМЯ=значение` и `ARG ИМЯ[=значение]`.
        - Подозрительно имя, в котором (без учёта регистра) есть `PASSWORD`, `TOKEN`, `SECRET` или `KEY`.
        - Возвращает: список таких имён в порядке появления.

        Пример:
        ```
        find_secrets("FROM python:3.12\\nENV BASE_URL=http://app\\nENV DB_PASSWORD=qwerty\\nARG api_token\\n")
        # → ["DB_PASSWORD", "api_token"]
        ```
        """),
        """
        def find_secrets(text):
            pass
        """,
        """
        def test_find():
            text = "FROM python:3.12\\nENV BASE_URL=http://app\\nENV DB_PASSWORD=qwerty\\nARG api_token\\n"
            assert find_secrets(text) == ["DB_PASSWORD", "api_token"], find_secrets(text)

        def test_clean():
            assert find_secrets("FROM x\\nENV HEADLESS=true\\nARG PYTHON_VERSION=3.12\\nRUN echo KEY") == []
        """,
        """
        def find_secrets(text):
            found = []
            for line in text.splitlines():
                instr, _, args = line.strip().partition(" ")
                if instr.upper() in ("ENV", "ARG") and args:
                    name = args.split("=")[0].strip()
                    if any(word in name.upper() for word in ("PASSWORD", "TOKEN", "SECRET", "KEY")):
                        found.append(name)
            return found
        """),
    cmd(f"{P}-optimize-e5", "Место на диске закончилось. Удали **неиспользуемые** образы (висящие, без тегов).",
        ["docker image prune", "docker image prune -f", "docker image prune --force"],
        hint="`docker image prune`."),
    cmd(f"{P}-optimize-e6", "Покажи, сколько места занимают образы, контейнеры, тома и кэш сборки Docker.",
        ["docker system df", "docker system df -v"],
        hint="`docker system ...`."),
    cod(f"{P}-optimize-e7", t("""
        Напиши функцию `human_size(n)`, которая переводит размер в байтах в удобный вид, как это делает `docker images`.

        - Единицы: `B`, `KB`, `MB`, `GB` с основанием **1024**.
        - Выбирай самую крупную единицу, в которой значение ≥ 1; байты — целым числом, остальное — с одним знаком после точки.

        Примеры:
        ```
        human_size(512)           # → "512 B"
        human_size(2048)          # → "2.0 KB"
        human_size(131_596_288)   # → "125.5 MB"
        human_size(3 * 1024**3)   # → "3.0 GB"
        ```
        """),
        """
        def human_size(n):
            pass
        """,
        """
        def test_sizes():
            assert human_size(512) == "512 B"
            assert human_size(2048) == "2.0 KB"
            assert human_size(131_596_288) == "125.5 MB", human_size(131_596_288)
            assert human_size(3 * 1024**3) == "3.0 GB"
            assert human_size(1023) == "1023 B"
        """,
        """
        def human_size(n):
            if n < 1024:
                return f"{n} B"
            for unit in ("KB", "MB", "GB"):
                n /= 1024
                if n < 1024 or unit == "GB":
                    return f"{n:.1f} {unit}"
        """),
    cmd(f"{P}-optimize-e8", "Проверь образ `my-tests:1.0` на известные уязвимости сканером **Trivy**.",
        ["trivy image my-tests:1.0", "docker scout cves my-tests:1.0"],
        hint="`trivy image образ`."),
),
)
