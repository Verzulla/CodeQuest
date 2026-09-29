"""Тема «CI/CD для тестировщика», модуль 2 «GitHub Actions» — задания. Теория — в _ci_t2.py.

Урок dci-m2-l2 унаследован от старой темы «Docker и CI/CD» — так сохраняется прогресс."""
from ._lib import cmd, cod, lesson, module, out, t
from ._ci_m1 import wfy

P = "ci"
O = "dci"

m2 = module(f"{P}-m2", "GitHub Actions", "⚙️", "Workflow и шаги, матрицы, секреты и переменные, Docker и сервисы в CI",

lesson(f"{O}-m2-l2", "GitHub Actions и отчёты",
    out(f"{O}-m2-l2-e1", "Что выведет программа? Секреты маскируются в логах.", """
            log = "login with token=abc123 to https://user:pa55@host"
            for secret in ["abc123", "pa55"]:
                log = log.replace(secret, "***")
            print(log)
            """),
    cod(f"{O}-m2-l2-e2", t("""
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
    cod(f"{O}-m2-l2-e3", t("""
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
    cod(f"{O}-m2-l2-e4", t("""
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
    cod(f"{O}-m2-l2-e5", t("""
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
    cmd(f"{O}-m2-l2-e6", "Покажи через GitHub CLI список последних запусков workflow в репозитории.",
        ["gh run list", "gh run ls"],
        hint="`gh run ...`."),
    cmd(f"{O}-m2-l2-e7", "Запуск `9876543210` упал. Покажи через GitHub CLI логи **только упавших шагов**.",
        ["gh run view 9876543210 --log-failed", "gh run view --log-failed 9876543210"],
        hint="`gh run view <номер> --log-failed`."),
    cmd(f"{O}-m2-l2-e8", "Перезапусти в запуске `9876543210` **только упавшие** job-ы.",
        ["gh run rerun 9876543210 --failed", "gh run rerun --failed 9876543210"],
        hint="`gh run rerun <номер> --failed`."),
),

lesson(f"{P}-matrix", "Матрицы и окружения",
    out(f"{P}-matrix-e1", "Что выведет программа? Матрица — все комбинации параметров: каждая становится отдельным запуском job-а.", """
        from itertools import product

        matrix = {"os": ["ubuntu-latest", "windows-latest"], "python": ["3.11", "3.12"]}
        runs = [dict(zip(matrix, combo)) for combo in product(*matrix.values())]
        print(len(runs))
        for run in runs:
            print(run["os"], run["python"])
        """),
    cod(f"{P}-matrix-e2", t("""
        Кроме декартова произведения у матрицы есть `exclude` — убрать комбинации — и `include` — добавить свои.

        Напиши функцию `expand_matrix(matrix)`:
        - `matrix` — словарь: списки значений по ключам плюс необязательные `"exclude"` и `"include"` — списки словарей;
        - сначала все комбинации (ключи — в порядке словаря, без `exclude`/`include`);
        - затем выброшены комбинации, которые **совпадают по всем ключам** хотя бы одного словаря из `exclude`;
        - в конец добавлены словари из `include`.

        Пример:
        ```
        expand_matrix({
            "os": ["ubuntu", "windows"],
            "browser": ["chromium", "webkit"],
            "exclude": [{"os": "windows", "browser": "webkit"}],
            "include": [{"os": "macos", "browser": "webkit"}],
        })
        # → [{"os": "ubuntu", "browser": "chromium"}, {"os": "ubuntu", "browser": "webkit"},
        #    {"os": "windows", "browser": "chromium"}, {"os": "macos", "browser": "webkit"}]
        ```
        """),
        """
        from itertools import product


        def expand_matrix(matrix):
            pass
        """,
        """
        def test_expand():
            got = expand_matrix({
                "os": ["ubuntu", "windows"],
                "browser": ["chromium", "webkit"],
                "exclude": [{"os": "windows", "browser": "webkit"}],
                "include": [{"os": "macos", "browser": "webkit"}],
            })
            assert got == [{"os": "ubuntu", "browser": "chromium"}, {"os": "ubuntu", "browser": "webkit"},
                           {"os": "windows", "browser": "chromium"}, {"os": "macos", "browser": "webkit"}], got

        def test_partial_exclude():
            got = expand_matrix({"os": ["a", "b"], "py": ["1", "2"], "exclude": [{"os": "b"}]})
            assert got == [{"os": "a", "py": "1"}, {"os": "a", "py": "2"}], "exclude по одному ключу убирает все комбинации с ним"
        """,
        """
        from itertools import product


        def expand_matrix(matrix):
            keys = [k for k in matrix if k not in ("exclude", "include")]
            runs = [dict(zip(keys, combo)) for combo in product(*(matrix[k] for k in keys))]
            for ex in matrix.get("exclude", []):
                runs = [r for r in runs if not all(r.get(k) == v for k, v in ex.items())]
            return runs + list(matrix.get("include", []))
        """, xp=20),
    cod(f"{P}-matrix-e3", t("""
        Напиши workflow `WORKFLOW`: job `ui-tests` на `ubuntu-latest` с матрицей браузеров `browser: [chromium, firefox, webkit]` и `fail-fast: false` (упал один браузер — остальные доигрывают). Шаг — `run: pytest --browser ${{ matrix.browser }}`.

        Раздел `strategy` выглядит так:
        ```yaml
        strategy:
          fail-fast: false
          matrix:
            browser: [chromium, firefox, webkit]
        ```
        """),
        '''
        WORKFLOW = """
        name: ui
        on: [push]
        jobs:
          ui-tests:
            runs-on: ubuntu-latest
        """
        ''',
        wfy("""
        def test_strategy():
            job = wf()["jobs"]["ui-tests"]
            st = job.get("strategy") or {}
            assert st.get("fail-fast") is False, "fail-fast: false"
            assert (st.get("matrix") or {}).get("browser") == ["chromium", "firefox", "webkit"], "matrix.browser: [chromium, firefox, webkit]"

        def test_step():
            runs = [s.get("run", "") for s in steps("ui-tests")]
            assert any(r.replace(" ", "") == "pytest--browser${{matrix.browser}}" for r in runs), f"Шаг: pytest --browser ${{{{ matrix.browser }}}}: {runs}"
        """),
        '''
        WORKFLOW = """
        name: ui
        on: [push]
        jobs:
          ui-tests:
            runs-on: ubuntu-latest
            strategy:
              fail-fast: false
              matrix:
                browser: [chromium, firefox, webkit]
            steps:
              - uses: actions/checkout@v4
              - run: pip install -r requirements.txt
              - run: pytest --browser ${{ matrix.browser }}
        """
        ''', xp=20),
    cod(f"{P}-matrix-e4", t("""
        Напиши функцию `render(template, context)` — упрощённую подстановку выражений GitHub Actions `${{ путь }}`, где путь — ключи через точку: `matrix.python`, `github.ref_name`.

        - Пробелы внутри `${{ … }}` не важны.
        - Путь ищется во вложенных словарях `context`; если чего-то нет — подставляется пустая строка.

        Пример:
        ```
        ctx = {"matrix": {"python": "3.12"}, "github": {"ref_name": "main"}}
        render("tests-${{ matrix.python }}-${{github.ref_name}}", ctx)   # → "tests-3.12-main"
        render("x${{ env.NOPE }}y", ctx)                                  # → "xy"
        ```
        """),
        """
        import re


        def render(template, context):
            pass
        """,
        """
        def test_render():
            ctx = {"matrix": {"python": "3.12"}, "github": {"ref_name": "main"}}
            assert render("tests-${{ matrix.python }}-${{github.ref_name}}", ctx) == "tests-3.12-main"
            assert render("x${{ env.NOPE }}y", ctx) == "xy"
            assert render("no expr", ctx) == "no expr"
        """,
        """
        import re


        def render(template, context):
            def value(m):
                node = context
                for key in m.group(1).split("."):
                    if not isinstance(node, dict) or key not in node:
                        return ""
                    node = node[key]
                return str(node)
            return re.sub(r"\\$\\{\\{\\s*([\\w.-]+)\\s*\\}\\}", value, template)
        """, xp=20),
    out(f"{P}-matrix-e5", "Что выведет программа? С `fail-fast: true` (по умолчанию) первое падение отменяет ещё не закончившиеся запуски матрицы.", """
        results = [("chromium", "success"), ("firefox", "failure"), ("webkit", "success")]
        for fail_fast in (True, False):
            status = {}
            stopped = False
            for browser, result in results:
                status[browser] = "cancelled" if stopped else result
                if result == "failure" and fail_fast:
                    stopped = True
            print(fail_fast, status)
        """),
    cod(f"{P}-matrix-e6", t("""
        Тесты гоняют на разных стендах в зависимости от ветки. Напиши функцию `target_env(ref)` по полной ссылке git:

        - `refs/heads/main` → `"staging"`;
        - `refs/tags/v…` (тег версии) → `"production"`;
        - `refs/pull/…` (pull request) → `"review"`;
        - любая другая ветка → `"dev"`.
        """),
        """
        def target_env(ref):
            pass
        """,
        """
        def test_envs():
            assert target_env("refs/heads/main") == "staging"
            assert target_env("refs/tags/v1.4.0") == "production"
            assert target_env("refs/pull/42/merge") == "review"
            assert target_env("refs/heads/feature/cart") == "dev"
            assert target_env("refs/heads/main-old") == "dev"
        """,
        """
        def target_env(ref):
            if ref == "refs/heads/main":
                return "staging"
            if ref.startswith("refs/tags/v"):
                return "production"
            if ref.startswith("refs/pull/"):
                return "review"
            return "dev"
        """),
    cmd(f"{P}-matrix-e7", "Напиши условие для шага (значение `if:`), чтобы он выполнялся **только в ветке main**. Используй контекст `github.ref`.",
        ["github.ref == 'refs/heads/main'", "${{ github.ref == 'refs/heads/main' }}", "github.ref_name == 'main'", "${{ github.ref_name == 'main' }}"],
        hint="`github.ref == 'refs/heads/main'` — строки в выражениях Actions в одинарных кавычках."),
    out(f"{P}-matrix-e8", "Что выведет программа? `include` добавляет к существующей комбинации новые ключи, если совпадают все её ключи.", """
        runs = [{"browser": "chromium"}, {"browser": "firefox"}]
        include = [{"browser": "chromium", "headed": True}, {"browser": "webkit"}]
        for extra in include:
            base = {k: v for k, v in extra.items() if k == "browser"}
            match = next((r for r in runs if all(r.get(k) == v for k, v in base.items())), None)
            if match is not None:
                match.update(extra)
            else:
                runs.append(dict(extra))
        print(runs)
        """),
),

lesson(f"{P}-secrets", "Секреты и переменные",
    out(f"{P}-secrets-e1", "Что выведет программа? Тесты читают настройки из переменных окружения, которые задал CI.", """
        import os

        os.environ["BASE_URL"] = "https://stage.shop.test"
        base_url = os.environ.get("BASE_URL", "http://localhost:8000")
        token = os.environ.get("API_TOKEN")
        print(base_url)
        print(token is None)
        """),
    cod(f"{P}-secrets-e2", t("""
        Тест без нужного секрета должен падать сразу и понятно, а не где-то в середине с «401».

        Напиши функцию `require_env(names, env)`:
        - `names` — список обязательных переменных, `env` — словарь окружения;
        - если все есть и **непустые** — вернуть словарь `{имя: значение}` только для них;
        - иначе бросить `RuntimeError` с текстом `"Не заданы: A, B"` — отсутствующие и пустые, в порядке `names`.
        """),
        """
        def require_env(names, env):
            pass
        """,
        """
        def test_ok():
            assert require_env(["BASE_URL", "API_TOKEN"], {"BASE_URL": "u", "API_TOKEN": "t", "X": "1"}) == {"BASE_URL": "u", "API_TOKEN": "t"}

        def test_missing():
            try:
                require_env(["BASE_URL", "API_TOKEN", "DB"], {"BASE_URL": "u", "DB": ""})
            except RuntimeError as e:
                assert str(e) == "Не заданы: API_TOKEN, DB", str(e)
                return
            assert False, "Нужно бросить RuntimeError"
        """,
        """
        def require_env(names, env):
            missing = [n for n in names if not env.get(n)]
            if missing:
                raise RuntimeError("Не заданы: " + ", ".join(missing))
            return {n: env[n] for n in names}
        """),
    cod(f"{P}-secrets-e3", t("""
        Напиши workflow `WORKFLOW`: job `api-tests` (`ubuntu-latest`), у которого на уровне job-а заданы переменные окружения:

        ```yaml
        env:
          BASE_URL: ${{ vars.STAGE_URL }}
          API_TOKEN: ${{ secrets.API_TOKEN }}
        ```
        `vars` — обычные настройки репозитория, `secrets` — секреты (маскируются в логах). Шаг — `run: pytest tests/api`.
        """),
        '''
        WORKFLOW = """
        name: api
        on: [push]
        jobs:
          api-tests:
            runs-on: ubuntu-latest
            steps:
              - run: pytest tests/api
        """
        ''',
        wfy("""
        def norm(v):
            return str(v).replace(" ", "")

        def test_env():
            job = wf()["jobs"]["api-tests"]
            env = job.get("env") or {}
            assert norm(env.get("BASE_URL")) == "${{vars.STAGE_URL}}", "BASE_URL: ${{ vars.STAGE_URL }}"
            assert norm(env.get("API_TOKEN")) == "${{secrets.API_TOKEN}}", "API_TOKEN: ${{ secrets.API_TOKEN }}"
            assert any(s.get("run") == "pytest tests/api" for s in steps("api-tests")), "Шаг: pytest tests/api"

        def test_no_plain_secret():
            assert "secrets." in WORKFLOW and "token=" not in WORKFLOW.lower(), "Секрет — только через secrets"
        """),
        '''
        WORKFLOW = """
        name: api
        on: [push]
        jobs:
          api-tests:
            runs-on: ubuntu-latest
            env:
              BASE_URL: ${{ vars.STAGE_URL }}
              API_TOKEN: ${{ secrets.API_TOKEN }}
            steps:
              - uses: actions/checkout@v4
              - run: pip install -r requirements.txt
              - run: pytest tests/api
        """
        '''),
    cod(f"{P}-secrets-e4", t("""
        GitHub маскирует только **известные** ему секреты. Токен, который тест случайно напечатал сам, утечёт. Напиши функцию `find_leaks(log)`, которая ищет в логе похожие на секреты строки:

        - `Bearer <токен>` — токен из 20+ символов `[A-Za-z0-9._-]`;
        - `ghp_` + 36 букв/цифр — токен GitHub;
        - `password=<что угодно без пробела>`.

        Возвращает список номеров строк (с 1), где найдено хоть что-то.
        """),
        """
        import re


        def find_leaks(log):
            pass
        """,
        """
        LOG = "\\n".join([
            "GET /users 200",
            "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.payload.sig",
            "clone with ghp_" + "a1" * 18,
            "login ok",
            "db url postgres://u@h?password=qwerty",
            "Bearer short",
        ])

        def test_leaks():
            assert find_leaks(LOG) == [2, 3, 5], find_leaks(LOG)

        def test_clean():
            assert find_leaks("all good\\nBearer ***") == []
        """,
        """
        import re

        PATTERNS = [r"Bearer [A-Za-z0-9._-]{20,}", r"ghp_[A-Za-z0-9]{36}", r"password=\\S+"]


        def find_leaks(log):
            return [i for i, line in enumerate(log.splitlines(), 1)
                    if any(re.search(p, line) for p in PATTERNS)]
        """, xp=20),
    cmd(f"{P}-secrets-e5", "Добавь в репозиторий секрет `API_TOKEN` через GitHub CLI (значение команда спросит сама).",
        ["gh secret set API_TOKEN"],
        hint="`gh secret set ИМЯ`."),
    cmd(f"{P}-secrets-e6", "Шаг получил токен в переменной `TOKEN` во время работы. Попроси GitHub **маскировать** его значение в логах (команда workflow `add-mask`).",
        ['echo "::add-mask::$TOKEN"', "echo ::add-mask::$TOKEN", "echo '::add-mask::'$TOKEN"],
        hint='`echo "::add-mask::значение"`.'),
    cod(f"{P}-secrets-e7", t("""
        Файл `.env` с настоящими паролями не должен попасть в git. Напиши функцию `env_ignored(gitignore)`: `True`, если среди строк `.gitignore` есть шаблон, под который подходит файл `.env` (`fnmatch`: подойдут `.env`, `.env*`, `*.env`, `/.env`), и при этом он **не** отменён строкой `!.env` ниже.

        Пустые строки и комментарии `#` пропускай.
        """),
        """
        from fnmatch import fnmatch


        def env_ignored(gitignore):
            pass
        """,
        """
        def test_ignored():
            assert env_ignored(".venv\\n.env\\n") is True
            assert env_ignored("# local\\n.env*\\n") is True
            assert env_ignored("/.env\\n") is True

        def test_not_ignored():
            assert env_ignored(".venv\\n__pycache__\\n") is False
            assert env_ignored(".env*\\n!.env\\n") is False, "!.env отменяет игнор"
            assert env_ignored("# .env\\n") is False
        """,
        """
        from fnmatch import fnmatch


        def env_ignored(gitignore):
            ignored = False
            for line in gitignore.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                negate = line.startswith("!")
                pattern = line.lstrip("!").lstrip("/")
                if fnmatch(".env", pattern):
                    ignored = not negate
            return ignored
        """),
    out(f"{P}-secrets-e8", "Что выведет программа? Секреты не передаются в workflow из форков — pull request из чужого репозитория видит их пустыми.", """
        def secret_for(event, from_fork, secrets):
            if event == "pull_request" and from_fork:
                return ""
            return secrets.get("API_TOKEN", "")

        secrets = {"API_TOKEN": "s3cr3t"}
        for event, fork in [("push", False), ("pull_request", False), ("pull_request", True)]:
            value = secret_for(event, fork, secrets)
            print(event, fork, "есть" if value else "пусто")
        """),
),

lesson(f"{P}-docker", "Docker и сервисы в CI",
    cod(f"{P}-docker-e1", t("""
        GitHub Actions умеет поднимать рядом с job-ом контейнеры-**сервисы**. Напиши `WORKFLOW`: job `api-tests` (`ubuntu-latest`) с сервисом базы:

        ```yaml
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
        ```
        Порт пиши в кавычках: без них YAML может прочитать `5432:5432` как число.

        Шаги: `actions/checkout@v4`, `pip install -r requirements.txt`, `pytest tests/api` с `env: {DATABASE_URL: postgresql://postgres:secret@localhost:5432/postgres}`.
        """),
        '''
        WORKFLOW = """
        name: api
        on: [push]
        jobs:
          api-tests:
            runs-on: ubuntu-latest
        """
        ''',
        wfy("""
        def test_service():
            job = wf()["jobs"]["api-tests"]
            pg = (job.get("services") or {}).get("postgres") or {}
            assert pg.get("image") == "postgres:16", "services.postgres.image: postgres:16"
            assert (pg.get("env") or {}).get("POSTGRES_PASSWORD") == "secret", "POSTGRES_PASSWORD: secret"
            assert pg.get("ports") == ["5432:5432"], f'ports: ["5432:5432"] — в кавычках, а сейчас {pg.get("ports")}'
            assert "--health-cmd" in str(pg.get("options", "")), "options: --health-cmd ..."

        def test_steps():
            s = steps("api-tests")
            assert s and s[0].get("uses") == "actions/checkout@v4"
            test = [x for x in s if x.get("run") == "pytest tests/api"]
            assert test, "Шаг pytest tests/api"
            assert (test[0].get("env") or {}).get("DATABASE_URL") == "postgresql://postgres:secret@localhost:5432/postgres", "DATABASE_URL у шага тестов"
        """),
        '''
        WORKFLOW = """
        name: api
        on: [push]
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
              - run: pip install -r requirements.txt
              - run: pytest tests/api
                env:
                  DATABASE_URL: postgresql://postgres:secret@localhost:5432/postgres
        """
        ''', xp=25),
    cod(f"{P}-docker-e2", t("""
        Образ тестов, собранный в CI, помечают несколькими тегами. Напиши функцию `image_tags(image, sha, ref)`:

        - всегда — `<image>:sha-<первые 7 символов sha>`;
        - ветка `refs/heads/<имя>` → ещё `<image>:<имя>`, где `/` заменён на `-`; для `main` — дополнительно `<image>:latest`;
        - тег `refs/tags/v<версия>` → ещё `<image>:<версия>` (без `v`).

        Порядок: sha-тег, затем остальные в порядке правил.

        Пример:
        ```
        image_tags("ghcr.io/acme/tests", "3f2a1b9c8d7e6f", "refs/heads/main")
        # → ["ghcr.io/acme/tests:sha-3f2a1b9", "ghcr.io/acme/tests:main", "ghcr.io/acme/tests:latest"]
        ```
        """),
        """
        def image_tags(image, sha, ref):
            pass
        """,
        """
        I = "ghcr.io/acme/tests"

        def test_main():
            assert image_tags(I, "3f2a1b9c8d7e6f", "refs/heads/main") == [I + ":sha-3f2a1b9", I + ":main", I + ":latest"]

        def test_branch():
            assert image_tags(I, "abcdef0123", "refs/heads/feature/cart") == [I + ":sha-abcdef0", I + ":feature-cart"]

        def test_version():
            assert image_tags(I, "abcdef0123", "refs/tags/v1.4.2") == [I + ":sha-abcdef0", I + ":1.4.2"]
        """,
        """
        def image_tags(image, sha, ref):
            tags = [f"{image}:sha-{sha[:7]}"]
            if ref.startswith("refs/heads/"):
                branch = ref[len("refs/heads/"):]
                tags.append(f"{image}:{branch.replace('/', '-')}")
                if branch == "main":
                    tags.append(f"{image}:latest")
            elif ref.startswith("refs/tags/v"):
                tags.append(f"{image}:{ref[len('refs/tags/v'):]}")
            return tags
        """, xp=20),
    cmd(f"{P}-docker-e3", "Шаг CI: собери образ `ghcr.io/acme/tests` с тегом из **хеша коммита** — переменная окружения `GITHUB_SHA`.",
        ["docker build -t ghcr.io/acme/tests:$GITHUB_SHA .", "docker build -t ghcr.io/acme/tests:${GITHUB_SHA} .",
         "docker build --tag ghcr.io/acme/tests:$GITHUB_SHA .", "docker build -t ghcr.io/acme/tests:${{ github.sha }} ."],
        hint="`docker build -t образ:$GITHUB_SHA .`"),
    cmd(f"{P}-docker-e4", "Шаг CI: подними стенд из compose, прогони сервис `tests` и заверши шаг с **его** кодом выхода (с пересборкой образов).",
        ["docker compose up --build --exit-code-from tests", "docker compose up --exit-code-from tests --build",
         "docker compose up --build --abort-on-container-exit --exit-code-from tests"],
        hint="`--exit-code-from сервис`."),
    cod(f"{P}-docker-e5", t("""
        Напиши `WORKFLOW` с job-ом `e2e`, который гоняет тесты через Docker Compose. Шаги по порядку:

        1. `uses: actions/checkout@v4`;
        2. `run: docker compose up --build --exit-code-from tests`;
        3. `uses: actions/upload-artifact@v4` с `if: always()` и `with: {name: reports, path: reports/}`;
        4. `run: docker compose down -v` с `if: always()` — убрать стенд даже при падении.
        """),
        '''
        WORKFLOW = """
        name: e2e
        on: [push]
        jobs:
          e2e:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
        """
        ''',
        wfy("""
        def cond(step):
            return str(step.get("if", "")).replace("${{", "").replace("}}", "").strip()

        def test_order():
            s = steps("e2e")
            kinds = [x.get("uses", "").split("@")[0] or x.get("run", "") for x in s]
            assert kinds == ["actions/checkout", "docker compose up --build --exit-code-from tests", "actions/upload-artifact", "docker compose down -v"], kinds

        def test_always():
            s = steps("e2e")
            assert cond(s[2]) == "always()" and cond(s[3]) == "always()", "Выгрузка отчёта и уборка — с if: always()"
            assert (s[2].get("with") or {}) == {"name": "reports", "path": "reports/"}
        """),
        '''
        WORKFLOW = """
        name: e2e
        on: [push]
        jobs:
          e2e:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - run: docker compose up --build --exit-code-from tests
              - uses: actions/upload-artifact@v4
                if: always()
                with:
                  name: reports
                  path: reports/
              - run: docker compose down -v
                if: always()
        """
        ''', xp=20),
    out(f"{P}-docker-e6", "Что выведет программа? Условия шагов: по умолчанию шаг выполняется, только если все предыдущие успешны (`success()`), `always()` — всегда, `failure()` — только после падения.", """
        def runs(condition, failed_before):
            return {"success()": not failed_before, "always()": True, "failure()": failed_before}[condition]

        steps = [("pytest", "success()"), ("upload report", "always()"), ("notify", "failure()"), ("deploy", "success()")]
        failed = False
        for name, condition in steps:
            if runs(condition, failed):
                print("▶", name)
                if name == "pytest":
                    failed = True
            else:
                print("—", name)
        """),
    cmd(f"{P}-docker-e7", "Шаг CI: войди в реестр `ghcr.io` пользователем `acme`, передав токен из переменной `CR_TOKEN` через **stdin** (не в аргументе — он попал бы в историю и логи).",
        ['echo "$CR_TOKEN" | docker login ghcr.io -u acme --password-stdin', "echo $CR_TOKEN | docker login ghcr.io -u acme --password-stdin",
         'echo "$CR_TOKEN" | docker login ghcr.io --username acme --password-stdin', 'echo "$CR_TOKEN" | docker login -u acme --password-stdin ghcr.io'],
        hint="`echo \"$CR_TOKEN\" | docker login реестр -u пользователь --password-stdin`."),
    cod(f"{P}-docker-e8", t("""
        Напиши функцию `step_runs(condition, previous)` — выполнится ли шаг с условием `if` при данных результатах предыдущих шагов.

        - `previous` — список статусов предыдущих шагов: `"success"`, `"failure"`, `"skipped"`.
        - `condition`: `"success()"` (по умолчанию) — нет ни одного `"failure"`; `"failure()"` — есть хотя бы один `"failure"`; `"always()"` — всегда; `"cancelled()"` — в этой задаче всегда `False`.
        - Условие может быть обёрнуто в `${{ … }}` и иметь пробелы — убери их.
        - Пустое условие `""` — то же, что `"success()"`.
        """),
        """
        def step_runs(condition, previous):
            pass
        """,
        """
        def test_conditions():
            assert step_runs("", ["success"]) is True
            assert step_runs("success()", ["success", "failure"]) is False
            assert step_runs("${{ failure() }}", ["success", "failure"]) is True
            assert step_runs("failure()", ["success", "skipped"]) is False
            assert step_runs(" always() ", ["failure"]) is True
            assert step_runs("cancelled()", ["failure"]) is False
        """,
        """
        def step_runs(condition, previous):
            cond = condition.strip()
            if cond.startswith("${{") and cond.endswith("}}"):
                cond = cond[3:-2].strip()
            failed = "failure" in previous
            return {"": not failed, "success()": not failed, "failure()": failed,
                    "always()": True, "cancelled()": False}[cond]
        """),
),
)
