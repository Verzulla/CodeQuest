"""Тема «Python-проект», модуль 3 «Качество кода» — задания. Теория — в _prj_t3.py."""
from ._lib import cmd, cod, lesson, module, t

P = "prj"

m3 = module(f"{P}-m3", "Качество кода", "🧹", "Линтер ruff: проверки и автоисправления, форматирование, настройка, pre-commit",

lesson(f"{P}-lint", "Линтер ruff: ruff check",
    cmd(f"{P}-lint-e1", "Проверь весь проект линтером `ruff`.",
        ["ruff check", "ruff check .", "uv run ruff check", "uv run ruff check .", "uvx ruff check", "uvx ruff check ."]),
    cmd(f"{P}-lint-e2", "Проверь ruff и **автоматически исправь** всё, что можно исправить безопасно.",
        ["ruff check --fix", "ruff check --fix .", "ruff check . --fix", "uv run ruff check --fix", "uv run ruff check --fix ."]),
    cmd(f"{P}-lint-e3", "Проверь только папку `tests`.",
        ["ruff check tests", "ruff check tests/", "uv run ruff check tests"]),
    cmd(f"{P}-lint-e4", "Какой код у ошибки «импорт не используется»? Введи его.",
        ["F401"],
        context="""
        $ ruff check
        tests/test_api.py:1:8: F401 [*] `os` imported but unused
        tests/test_api.py:9:89: E501 Line too long (104 > 88)
        Found 2 errors.
        [*] 1 fixable with the `--fix` option.
        """),
    cmd(f"{P}-lint-e5", "На какой **строке** файла слишком длинная строка кода? Введи номер.",
        ["9"],
        context="""
        $ ruff check
        tests/test_api.py:1:8: F401 [*] `os` imported but unused
        tests/test_api.py:9:89: E501 Line too long (104 > 88)
        """, hint="Формат: файл:строка:столбец: код описание."),
    cmd(f"{P}-lint-e6", "Как в коде **отключить** одну конкретную проверку `E501` для одной строки? Введи комментарий, который ставят в конце строки.",
        ["# noqa: E501", "#noqa: E501", "# noqa:E501"]),
    cmd(f"{P}-lint-e7", "Покажи объяснение правила `F401` прямо в терминале.",
        ["ruff rule F401", "uv run ruff rule F401"]),
    cod(f"{P}-lint-e8", t("""
        Напиши свою мини-проверку «неиспользуемый импорт» (как `F401`): функция `unused_imports(source)` — разобрать код модулем `ast` и вернуть отсортированный список имён, которые импортированы (`import x`, `from y import z`, `import a as b` → имя `b`), но нигде в коде не используются как имя (`ast.Name`) или начало атрибута (`x.attr`).
        """),
        """
        import ast


        def unused_imports(source):
            pass
        """,
        """
        SRC = '''
        import os
        import json
        import requests as rq
        from pathlib import Path
        from typing import List

        def load(p):
            return json.loads(Path(p).read_text())

        def get(url):
            return rq.get(url)
        '''

        def test_values():
            assert unused_imports(SRC) == ["List", "os"], unused_imports(SRC)
            assert unused_imports("import sys\\nprint(sys.argv)") == [], "Всё используется"
        """,
        """
        import ast


        def unused_imports(source):
            tree = ast.parse(source)
            imported = set()
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    for alias in node.names:
                        imported.add((alias.asname or alias.name).split(".")[0])
            used = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
            return sorted(imported - used)
        """, xp=25),
),

lesson(f"{P}-format", "Форматирование: ruff format",
    cmd(f"{P}-format-e1", "Отформатируй весь проект форматтером ruff.",
        ["ruff format", "ruff format .", "uv run ruff format", "uv run ruff format .", "uvx ruff format", "uvx ruff format ."]),
    cmd(f"{P}-format-e2", "Проверь форматирование в CI: **ничего не меняя**, упади с ошибкой, если файлы не отформатированы.",
        ["ruff format --check", "ruff format --check .", "uv run ruff format --check", "uv run ruff format --check ."]),
    cmd(f"{P}-format-e3", "Покажи, **какие именно** изменения внёс бы форматтер, не применяя их.",
        ["ruff format --diff", "ruff format --diff .", "uv run ruff format --diff"]),
    cmd(f"{P}-format-e4", "Отформатируй только один файл `tests/test_cart.py`.",
        ["ruff format tests/test_cart.py", "uv run ruff format tests/test_cart.py"]),
    cmd(f"{P}-format-e5", "Сколько файлов **будет переформатировано**? Введи число.",
        ["2"],
        context="""
        $ ruff format --check
        Would reformat: tests/test_api.py
        Would reformat: tests/conftest.py
        2 files would be reformatted, 14 files already formatted
        """),
    cmd(f"{P}-format-e6", "Одной строкой: сначала исправь проблемы линтера, затем отформатируй код (через `&&`).",
        ["ruff check --fix && ruff format", "ruff check --fix . && ruff format .", "ruff check . --fix && ruff format .",
         "uv run ruff check --fix && uv run ruff format"]),
    cmd(f"{P}-format-e7", "Какой код выхода вернёт `ruff format --check`, если есть неотформатированные файлы: `0` или `1`?",
        ["1"], hint="Ненулевой код роняет шаг CI."),
    cod(f"{P}-format-e8", t("""
        Мини-форматтер для одной проверки: функция `normalize_quotes(line)` — заменить одинарные кавычки строк на двойные, **если** внутри строки нет двойных кавычек (как делает ruff format). Считай, что в строке кода кавычки не экранированы и строки не вложены.

        ```
        normalize_quotes("x = 'abc'")          # → 'x = "abc"'
        normalize_quotes("s = 'say \\"hi\\"'")  # без изменений
        ```
        """),
        """
        import re


        def normalize_quotes(line):
            pass
        """,
        """
        def test_values():
            assert normalize_quotes("x = 'abc'") == 'x = "abc"', normalize_quotes("x = 'abc'")
            assert normalize_quotes("d = {'a': 'b'}") == 'd = {"a": "b"}', normalize_quotes("d = {'a': 'b'}")
            assert normalize_quotes("s = 'say \\"hi\\"'") == "s = 'say \\"hi\\"'", "С двойными внутри — без изменений"
            assert normalize_quotes('y = "ok"') == 'y = "ok"', "Уже двойные"
        """,
        """
        import re


        def normalize_quotes(line):
            def repl(m):
                inner = m.group(1)
                return m.group(0) if '"' in inner else f'"{inner}"'
            return re.sub(r"'([^']*)'", repl, line)
        """, xp=20),
),

lesson(f"{P}-ruffcfg", "Настройка ruff",
    cmd(f"{P}-ruffcfg-e1", "Какую строку добавить в секцию `[tool.ruff]`, чтобы максимальная длина строки была 120 символов?",
        ["line-length = 120", "line-length=120"]),
    cmd(f"{P}-ruffcfg-e2", "Какую строку добавить в `[tool.ruff.lint]`, чтобы включить правила pyflakes (`F`), pycodestyle-ошибки (`E`) и сортировку импортов (`I`)?",
        ['select = ["E", "F", "I"]', "select = ['E', 'F', 'I']", 'select = ["F", "E", "I"]', 'select = ["E","F","I"]']),
    cmd(f"{P}-ruffcfg-e3", "Какой префикс правил отвечает за сортировку импортов (isort)? Введи букву.",
        ["I"]),
    cmd(f"{P}-ruffcfg-e4", "Какую строку добавить в `[tool.ruff.lint]`, чтобы **отключить** правило `E501`?",
        ['ignore = ["E501"]', "ignore = ['E501']"]),
    cmd(f"{P}-ruffcfg-e5", "Какие правила **отключены** для файлов тестов? Введи код.",
        ["S101"],
        context="""
        [tool.ruff.lint.per-file-ignores]
        "tests/**" = ["S101"]
        """, hint="S101 — «использован assert»: в тестах assert — норма."),
    cmd(f"{P}-ruffcfg-e6", "Какую строку добавить в `[tool.ruff]`, чтобы ruff знал целевую версию Python 3.12?",
        ['target-version = "py312"', "target-version = 'py312'"]),
    cod(f"{P}-ruffcfg-e7", t("""
        Напиши функцию `ruff_settings(text)` — прочитать `pyproject.toml` модулем `tomllib` и вернуть словарь `{"line_length": ..., "select": [...], "ignore": [...]}` из секций `[tool.ruff]` и `[tool.ruff.lint]`. Значения по умолчанию: `88`, `["E", "F"]`, `[]`.
        """),
        """
        import tomllib


        def ruff_settings(text):
            pass
        """,
        """
        TEXT = '''
        [tool.ruff]
        line-length = 120

        [tool.ruff.lint]
        select = ["E", "F", "I", "B"]
        ignore = ["E501"]
        '''

        def test_values():
            assert ruff_settings(TEXT) == {"line_length": 120, "select": ["E", "F", "I", "B"], "ignore": ["E501"]}, ruff_settings(TEXT)
            assert ruff_settings('[project]\\nname = "x"') == {"line_length": 88, "select": ["E", "F"], "ignore": []}, "По умолчанию"
        """,
        """
        import tomllib


        def ruff_settings(text):
            ruff = tomllib.loads(text).get("tool", {}).get("ruff", {})
            lint = ruff.get("lint", {})
            return {
                "line_length": ruff.get("line-length", 88),
                "select": lint.get("select", ["E", "F"]),
                "ignore": lint.get("ignore", []),
            }
        """),
    cod(f"{P}-ruffcfg-e8", t("""
        Реализуй проверку `E501`: функция `long_lines(source, limit=88)` — вернуть список сообщений `"строка N: длина L > limit"` для строк длиннее лимита. Строки с комментарием `# noqa: E501` в конце пропускать.
        """),
        """
        def long_lines(source, limit=88):
            pass
        """,
        """
        def test_values():
            src = "a = 1\\n" + "x" * 90 + "\\n" + "y" * 95 + "  # noqa: E501\\nb = 2"
            assert long_lines(src) == ["строка 2: длина 90 > 88"], long_lines(src)
            assert long_lines("z" * 100, limit=120) == [], "Свой лимит"
        """,
        """
        def long_lines(source, limit=88):
            result = []
            for n, line in enumerate(source.splitlines(), start=1):
                if line.rstrip().endswith("# noqa: E501"):
                    continue
                if len(line) > limit:
                    result.append(f"строка {n}: длина {len(line)} > {limit}")
            return result
        """, xp=20),
),

lesson(f"{P}-precommit", "pre-commit: проверки перед каждым коммитом",
    cmd(f"{P}-precommit-e1", "Установи утилиту `pre-commit` в окружение через pip.",
        ["pip install pre-commit", "python -m pip install pre-commit", "uv add --dev pre-commit", "uv tool install pre-commit"]),
    cmd(f"{P}-precommit-e2", "Подключи хуки pre-commit к git-репозиторию (после создания `.pre-commit-config.yaml`).",
        ["pre-commit install", "uv run pre-commit install"]),
    cmd(f"{P}-precommit-e3", "Прогони все хуки на **всех** файлах проекта, а не только на изменённых.",
        ["pre-commit run --all-files", "pre-commit run -a", "uv run pre-commit run --all-files"]),
    cmd(f"{P}-precommit-e4", "Обнови версии хуков в `.pre-commit-config.yaml` до последних.",
        ["pre-commit autoupdate", "uv run pre-commit autoupdate"]),
    cmd(f"{P}-precommit-e5", "Какие хуки ruff подключены? Введи их `id` через пробел в порядке файла.",
        ["ruff ruff-format"],
        context="""
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
            rev: v0.6.9
            hooks:
              - id: ruff
                args: [--fix]
              - id: ruff-format
        """),
    cmd(f"{P}-precommit-e6", "Срочно нужно закоммитить, **пропустив** хуки (исключение, не привычка). Коммит с сообщением `wip`.",
        ['git commit -m "wip" --no-verify', "git commit -m 'wip' --no-verify", 'git commit --no-verify -m "wip"',
         "git commit --no-verify -m 'wip'", 'git commit -n -m "wip"', "git commit -n -m 'wip'"]),
    cmd(f"{P}-precommit-e7", "Запусти только один хук `ruff-format` на всех файлах.",
        ["pre-commit run ruff-format --all-files", "pre-commit run ruff-format -a", "pre-commit run --all-files ruff-format"]),
    cod(f"{P}-precommit-e8", t("""
        Смоделируй работу pre-commit: функция `run_hooks(files, hooks)` — `files` — словарь «путь → содержимое», `hooks` — список пар `(имя, функция)`, где функция принимает содержимое и возвращает **исправленное** содержимое (или то же самое). Применить хуки по порядку ко всем файлам `.py` (остальные не трогать). Вернуть кортеж `(новые_файлы, упавшие_хуки)`, где упавший хук — тот, что **изменил** хотя бы один файл (так pre-commit блокирует коммит).
        """),
        """
        def run_hooks(files, hooks):
            pass
        """,
        """
        def test_values():
            strip_ws = ("trailing-whitespace", lambda s: "\\n".join(l.rstrip() for l in s.split("\\n")))
            end_nl = ("end-of-file-fixer", lambda s: s if s.endswith("\\n") else s + "\\n")
            files = {"a.py": "x = 1  \\n", "b.py": "y = 2", "README.md": "text  "}
            new, failed = run_hooks(files, [strip_ws, end_nl])
            assert new == {"a.py": "x = 1\\n", "b.py": "y = 2\\n", "README.md": "text  "}, new
            assert failed == ["trailing-whitespace", "end-of-file-fixer"], failed
            assert run_hooks({"c.py": "ok\\n"}, [strip_ws, end_nl]) == ({"c.py": "ok\\n"}, []), "Всё чисто"
        """,
        """
        def run_hooks(files, hooks):
            result = dict(files)
            failed = []
            for name, fix in hooks:
                changed = False
                for path, text in result.items():
                    if not path.endswith(".py"):
                        continue
                    new = fix(text)
                    if new != text:
                        result[path] = new
                        changed = True
                if changed:
                    failed.append(name)
            return result, failed
        """, xp=25),
),
)
