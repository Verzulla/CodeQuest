"""Тема «Python-проект», модуль 1 «Окружение и pip» — задания. Теория — в _prj_t1.py."""
from ._lib import cmd, cod, lesson, module, t

P = "prj"

m1 = module(f"{P}-m1", "Окружение и pip", "📦", "Виртуальное окружение, pip, requirements.txt, pyproject.toml",

lesson(f"{P}-venv", "Виртуальное окружение",
    cmd(f"{P}-venv-e1", "Создай в текущей папке виртуальное окружение в папке `.venv` стандартным модулем Python.",
        ["python -m venv .venv", "python3 -m venv .venv"]),
    cmd(f"{P}-venv-e2", "Активируй окружение `.venv` в Linux или macOS.",
        ["source .venv/bin/activate", ". .venv/bin/activate"]),
    cmd(f"{P}-venv-e3", "Активируй окружение `.venv` в Windows (PowerShell).",
        [".venv\\Scripts\\Activate.ps1", ".venv\\Scripts\\activate", ".\\.venv\\Scripts\\Activate.ps1", ".\\.venv\\Scripts\\activate"]),
    cmd(f"{P}-venv-e4", "Выйди из активного виртуального окружения.",
        ["deactivate"]),
    cmd(f"{P}-venv-e5", "Проверь, какой Python сейчас используется (путь к файлу).",
        ["which python", "command -v python", "python -c 'import sys; print(sys.executable)'",
         'python -c "import sys; print(sys.executable)"', "which python3"]),
    cmd(f"{P}-venv-e6", "Окружение активно? Введи `да` или `нет`.",
        ["да"],
        context="""
        (.venv) anna@laptop:~/api-tests$ which python
        /home/anna/api-tests/.venv/bin/python
        """, hint="Префикс (.venv) в приглашении и путь внутри проекта."),
    cmd(f"{P}-venv-e7", "Запусти pytest из окружения `.venv`, **не активируя** его.",
        [".venv/bin/python -m pytest", ".venv/bin/pytest", "./.venv/bin/python -m pytest", "./.venv/bin/pytest"]),
    cod(f"{P}-venv-e8", t("""
        Напиши функцию `in_venv()` — `True`, если код запущен внутри виртуального окружения. Признак: `sys.prefix` отличается от `sys.base_prefix`. Затем функцию `describe(prefix, base_prefix)` — строку `"venv: <prefix>"` или `"system: <base_prefix>"` (для проверки на разных значениях).
        """),
        """
        import sys


        def in_venv():
            pass


        def describe(prefix, base_prefix):
            pass
        """,
        """
        import sys

        def test_values():
            assert in_venv() == (sys.prefix != sys.base_prefix), "in_venv"
            assert describe("/p/.venv", "/usr") == "venv: /p/.venv" and describe("/usr", "/usr") == "system: /usr", "describe"
        """,
        """
        import sys


        def in_venv():
            return sys.prefix != sys.base_prefix


        def describe(prefix, base_prefix):
            if prefix != base_prefix:
                return f"venv: {prefix}"
            return f"system: {base_prefix}"
        """),
),

lesson(f"{P}-pip", "Установка пакетов: pip",
    cmd(f"{P}-pip-e1", "Установи пакет `requests`.",
        ["pip install requests", "python -m pip install requests", "pip3 install requests", "python3 -m pip install requests"]),
    cmd(f"{P}-pip-e2", "Установи `pytest` **ровно** версии `8.3.2`.",
        ["pip install pytest==8.3.2", "python -m pip install pytest==8.3.2", "pip install 'pytest==8.3.2'", 'pip install "pytest==8.3.2"']),
    cmd(f"{P}-pip-e3", "Обнови уже установленный пакет `requests` до последней версии.",
        ["pip install -U requests", "pip install --upgrade requests", "python -m pip install -U requests", "python -m pip install --upgrade requests"]),
    cmd(f"{P}-pip-e4", "Удали пакет `selenium` без вопроса-подтверждения.",
        ["pip uninstall -y selenium", "pip uninstall selenium -y", "python -m pip uninstall -y selenium", "pip uninstall --yes selenium"]),
    cmd(f"{P}-pip-e5", "Покажи список установленных пакетов с версиями.",
        ["pip list", "python -m pip list", "pip freeze", "python -m pip freeze"]),
    cmd(f"{P}-pip-e6", "Покажи информацию о пакете `pytest`: версию, зависимости, где он установлен.",
        ["pip show pytest", "python -m pip show pytest"]),
    cmd(f"{P}-pip-e7", "Какая версия `requests` установлена? Введи номер.",
        ["2.32.3"],
        context="""
        $ pip list
        Package    Version
        ---------- -------
        pytest     8.3.2
        requests   2.32.3
        urllib3    2.2.2
        """),
    cod(f"{P}-pip-e8", t("""
        Напиши функцию `parse_version(v)` — превратить строку версии `"2.32.3"` в кортеж чисел `(2, 32, 3)`, и функцию `is_newer(a, b)` — `True`, если версия `a` новее `b`. Сравнивать строки напрямую нельзя: `"2.10"` больше `"2.9"`, хотя как строка меньше.
        """),
        """
        def parse_version(v):
            pass


        def is_newer(a, b):
            pass
        """,
        """
        def test_values():
            assert parse_version("2.32.3") == (2, 32, 3) and parse_version("8") == (8,), "parse_version"
            assert is_newer("2.10.0", "2.9.5") and not is_newer("1.0", "1.0") and is_newer("1.0.1", "1.0") and not is_newer("0.9", "1.0"), "is_newer"
        """,
        """
        def parse_version(v):
            return tuple(int(part) for part in v.split("."))


        def is_newer(a, b):
            return parse_version(a) > parse_version(b)
        """),
),

lesson(f"{P}-requirements", "requirements.txt",
    cmd(f"{P}-requirements-e1", "Установи все зависимости проекта из файла `requirements.txt`.",
        ["pip install -r requirements.txt", "python -m pip install -r requirements.txt"]),
    cmd(f"{P}-requirements-e2", "Сохрани точные версии всех установленных пакетов в `requirements.txt`.",
        ["pip freeze > requirements.txt", "python -m pip freeze > requirements.txt"]),
    cmd(f"{P}-requirements-e3", "Какую строку добавить в `requirements.txt`, чтобы требовать `pytest` версии **не ниже** 8.0?",
        ["pytest>=8.0", "pytest >= 8.0", "pytest>=8"]),
    cmd(f"{P}-requirements-e4", "Какую строку добавить в `requirements-dev.txt`, чтобы он **включал** все зависимости из `requirements.txt`?",
        ["-r requirements.txt", "--requirement requirements.txt"]),
    cmd(f"{P}-requirements-e5", "Сколько пакетов будет установлено **напрямую** из этого файла (не считая их собственных зависимостей)? Введи число.",
        ["3"],
        context="""
        $ cat requirements.txt
        # тесты
        pytest==8.3.2
        requests>=2.31

        allure-pytest~=2.13
        """, hint="Комментарии и пустые строки не считаются."),
    cmd(f"{P}-requirements-e6", "Какую строку написать, чтобы разрешить любые версии `2.13.x` пакета `allure-pytest`, но не `2.14`? Используй оператор совместимой версии.",
        ["allure-pytest~=2.13.0", "allure-pytest ~= 2.13.0", "allure-pytest>=2.13,<2.14", "allure-pytest>=2.13.0,<2.14"]),
    cmd(f"{P}-requirements-e7", "Установи зависимости из `requirements.txt` и **одновременно** из `requirements-dev.txt` одной командой pip.",
        ["pip install -r requirements.txt -r requirements-dev.txt", "python -m pip install -r requirements.txt -r requirements-dev.txt"]),
    cod(f"{P}-requirements-e8", t("""
        Напиши функцию `parse_requirements(text)` — разобрать содержимое `requirements.txt` в словарь «имя пакета (в нижнем регистре) → спецификатор версии» (пустая строка, если версия не указана). Пропускать пустые строки, комментарии `#` (в том числе в конце строки) и строки, начинающиеся с `-` (например, `-r`).
        """),
        """
        import re


        def parse_requirements(text):
            pass
        """,
        """
        TEXT = '''# тесты
        pytest==8.3.2
        Requests>=2.31  # http

        -r base.txt
        allure-pytest~=2.13
        pydantic
        '''

        def test_values():
            assert parse_requirements(TEXT) == {"pytest": "==8.3.2", "requests": ">=2.31", "allure-pytest": "~=2.13", "pydantic": ""}, parse_requirements(TEXT)
        """,
        """
        import re


        def parse_requirements(text):
            result = {}
            for line in text.splitlines():
                line = line.split("#", 1)[0].strip()
                if not line or line.startswith("-"):
                    continue
                m = re.match(r"([A-Za-z0-9_.\\-]+)\\s*(.*)", line)
                result[m.group(1).lower()] = m.group(2).replace(" ", "")
            return result
        """, xp=20),
),

lesson(f"{P}-pyproject", "pyproject.toml",
    cmd(f"{P}-pyproject-e1", "Установи текущий проект (с `pyproject.toml`) в окружение в **режиме разработки**, чтобы изменения кода сразу подхватывались.",
        ["pip install -e .", "python -m pip install -e .", "pip install --editable ."]),
    cmd(f"{P}-pyproject-e2", "Установи проект вместе с дополнительной группой зависимостей `dev` (секция `[project.optional-dependencies]`).",
        ["pip install -e '.[dev]'", 'pip install -e ".[dev]"', "pip install '.[dev]'", 'pip install ".[dev]"', "pip install -e .[dev]",
         "python -m pip install -e '.[dev]'", 'python -m pip install -e ".[dev]"'], hint="Квадратные скобки лучше взять в кавычки — zsh их раскрывает."),
    cmd(f"{P}-pyproject-e3", "Какая минимальная версия Python нужна проекту? Введи номер.",
        ["3.11"],
        context="""
        [project]
        name = "api-tests"
        version = "0.1.0"
        requires-python = ">=3.11"
        dependencies = ["requests>=2.31", "pydantic>=2"]
        """),
    cmd(f"{P}-pyproject-e4", "Сколько обязательных зависимостей у проекта в примере выше? Введи число.",
        ["2"],
        context="""
        [project]
        name = "api-tests"
        dependencies = ["requests>=2.31", "pydantic>=2"]

        [project.optional-dependencies]
        dev = ["pytest>=8", "ruff"]
        """),
    cmd(f"{P}-pyproject-e5", "Как называется секция `pyproject.toml`, в которой лежат настройки pytest? Введи её заголовок в квадратных скобках.",
        ["[tool.pytest.ini_options]"]),
    cmd(f"{P}-pyproject-e6", "Как называется секция с настройками линтера ruff?",
        ["[tool.ruff]"]),
    cod(f"{P}-pyproject-e7", t("""
        Напиши функцию `project_info(text)` — прочитать содержимое `pyproject.toml` (строку) модулем `tomllib` и вернуть кортеж `(имя, версия, список_зависимостей)`. Если зависимостей нет — пустой список.
        """),
        """
        import tomllib


        def project_info(text):
            pass
        """,
        """
        TEXT = '''
        [project]
        name = "api-tests"
        version = "0.1.0"
        dependencies = ["requests>=2.31", "pydantic>=2"]
        '''

        def test_values():
            assert project_info(TEXT) == ("api-tests", "0.1.0", ["requests>=2.31", "pydantic>=2"]), project_info(TEXT)
            assert project_info('[project]\\nname = "x"\\nversion = "1"') == ("x", "1", []), "Без зависимостей"
        """,
        """
        import tomllib


        def project_info(text):
            data = tomllib.loads(text)["project"]
            return data["name"], data["version"], data.get("dependencies", [])
        """, hint="tomllib.loads(строка) → словарь (модуль есть в Python 3.11+)."),
    cod(f"{P}-pyproject-e8", t("""
        Напиши функцию `pytest_addopts(text)` — достать из `pyproject.toml` значение `addopts` в секции `[tool.pytest.ini_options]` и вернуть его **списком** аргументов (разбить по пробелам). Если секции или ключа нет — пустой список.
        """),
        """
        import tomllib


        def pytest_addopts(text):
            pass
        """,
        """
        TEXT = '''
        [tool.pytest.ini_options]
        addopts = "-v --tb=short -n 2"
        testpaths = ["tests"]
        '''

        def test_values():
            assert pytest_addopts(TEXT) == ["-v", "--tb=short", "-n", "2"], pytest_addopts(TEXT)
            assert pytest_addopts('[project]\\nname = "x"') == [], "Нет секции"
        """,
        """
        import tomllib


        def pytest_addopts(text):
            data = tomllib.loads(text)
            opts = data.get("tool", {}).get("pytest", {}).get("ini_options", {}).get("addopts", "")
            return opts.split()
        """, xp=20),
),
)
