"""Тема «Python-проект», модуль 2 «uv и запуск» — задания. Теория — в _prj_t2.py."""
from ._lib import cmd, cod, lesson, module, t

P = "prj"

m2 = module(f"{P}-m2", "uv и запуск", "⚡", "Менеджер проектов uv: init, add, sync, run, lock, инструменты; запуск скриптов и аргументы",

lesson(f"{P}-uv", "uv: проект и зависимости",
    cmd(f"{P}-uv-e1", "Создай новый Python-проект с помощью `uv` в текущей папке.",
        ["uv init", "uv init ."]),
    cmd(f"{P}-uv-e2", "Добавь в проект зависимость `requests`.",
        ["uv add requests"]),
    cmd(f"{P}-uv-e3", "Добавь `pytest` как зависимость **для разработки** (dev).",
        ["uv add --dev pytest", "uv add pytest --dev", "uv add --group dev pytest"]),
    cmd(f"{P}-uv-e4", "Удали из проекта зависимость `selenium`.",
        ["uv remove selenium"]),
    cmd(f"{P}-uv-e5", "Ты склонировал проект с `pyproject.toml` и `uv.lock`. Создай окружение и установи **ровно** те версии, что в lock-файле.",
        ["uv sync", "uv sync --frozen", "uv sync --locked"]),
    cmd(f"{P}-uv-e6", "Запусти тесты через `uv`, чтобы они выполнились в окружении проекта (без ручной активации).",
        ["uv run pytest", "uv run python -m pytest"]),
    cmd(f"{P}-uv-e7", "Добавь `pydantic` с ограничением «версия 2 и выше».",
        ["uv add 'pydantic>=2'", 'uv add "pydantic>=2"', "uv add pydantic>=2", "uv add 'pydantic>=2.0'", 'uv add "pydantic>=2.0"']),
    cod(f"{P}-uv-e8", t("""
        Напиши функцию `uv_commands(deps, dev_deps)` — по спискам зависимостей вернуть список команд, которые настроят новый проект: сначала `uv init`, затем **одна** команда `uv add` со всеми обычными зависимостями (если они есть), затем **одна** `uv add --dev` со всеми dev-зависимостями (если есть), последней — `uv sync`.
        """),
        """
        def uv_commands(deps, dev_deps):
            pass
        """,
        """
        def test_values():
            assert uv_commands(["requests", "pydantic"], ["pytest"]) == ["uv init", "uv add requests pydantic", "uv add --dev pytest", "uv sync"], uv_commands(["requests", "pydantic"], ["pytest"])
            assert uv_commands([], []) == ["uv init", "uv sync"] and uv_commands([], ["ruff"]) == ["uv init", "uv add --dev ruff", "uv sync"], "Пустые списки"
        """,
        """
        def uv_commands(deps, dev_deps):
            commands = ["uv init"]
            if deps:
                commands.append("uv add " + " ".join(deps))
            if dev_deps:
                commands.append("uv add --dev " + " ".join(dev_deps))
            commands.append("uv sync")
            return commands
        """),
),

lesson(f"{P}-uvlock", "Lock-файл, версии Python и uv pip",
    cmd(f"{P}-uvlock-e1", "Обнови lock-файл `uv.lock` по текущему `pyproject.toml`, ничего не устанавливая.",
        ["uv lock"]),
    cmd(f"{P}-uvlock-e2", "Обнови в lock-файле пакет `requests` до последней допустимой версии.",
        ["uv lock --upgrade-package requests", "uv lock -P requests"]),
    cmd(f"{P}-uvlock-e3", "Установи через `uv` интерпретатор Python версии 3.12.",
        ["uv python install 3.12"]),
    cmd(f"{P}-uvlock-e4", "Закрепи для проекта версию Python 3.12 (uv создаст файл `.python-version`).",
        ["uv python pin 3.12"]),
    cmd(f"{P}-uvlock-e5", "Создай виртуальное окружение `.venv` с помощью `uv` (быстрая замена `python -m venv`).",
        ["uv venv", "uv venv .venv"]),
    cmd(f"{P}-uvlock-e6", "В проекте без `pyproject.toml` установи зависимости из `requirements.txt` через `uv` (pip-совместимый режим).",
        ["uv pip install -r requirements.txt"]),
    cmd(f"{P}-uvlock-e7", "Нужно ли коммитить `uv.lock` в git для проекта с автотестами? Ответь `да` или `нет`.",
        ["да"], hint="Lock-файл гарантирует одинаковые версии у всех и в CI."),
    cmd(f"{P}-uvlock-e8", "В CI нужно установить зависимости и **упасть**, если `uv.lock` не соответствует `pyproject.toml`. Какой командой?",
        ["uv sync --locked", "uv sync --frozen"], hint="--locked проверяет актуальность lock-файла.", xp=15),
),

lesson(f"{P}-uvtools", "Инструменты: uvx и uv tool",
    cmd(f"{P}-uvtools-e1", "Запусти линтер `ruff` один раз без установки в проект (`uv` скачает его во временное окружение).",
        ["uvx ruff check .", "uvx ruff check", "uv tool run ruff check .", "uv tool run ruff check"]),
    cmd(f"{P}-uvtools-e2", "Установи `ruff` как глобальный инструмент, чтобы команда `ruff` была доступна везде.",
        ["uv tool install ruff"]),
    cmd(f"{P}-uvtools-e3", "Покажи список инструментов, установленных через `uv tool`.",
        ["uv tool list"]),
    cmd(f"{P}-uvtools-e4", "Запусти тесты через `uv run` в 4 параллельных процесса (`pytest-xdist` уже установлен).",
        ["uv run pytest -n 4", "uv run pytest -n4", "uv run python -m pytest -n 4"]),
    cmd(f"{P}-uvtools-e5", "Запусти скрипт `scripts/seed_data.py` в окружении проекта через `uv`.",
        ["uv run scripts/seed_data.py", "uv run python scripts/seed_data.py"]),
    cmd(f"{P}-uvtools-e6", "Покажи дерево зависимостей проекта через `uv`.",
        ["uv tree"]),
    cmd(f"{P}-uvtools-e7", "Какой командой установить сам `uv` на Linux/macOS официальным скриптом? Введи команду с `curl`.",
        ["curl -LsSf https://astral.sh/uv/install.sh | sh", "curl -LsSf https://astral.sh/uv/install.sh | bash"]),
    cmd(f"{P}-uvtools-e8", "Запусти скрипт `check.py` c временной зависимостью `requests`, не добавляя её в проект.",
        ["uv run --with requests check.py", "uv run --with requests python check.py"], xp=15),
),

lesson(f"{P}-run", "Запуск скриптов и аргументы командной строки",
    cmd(f"{P}-run-e1", "Запусти скрипт `seed.py` с аргументами `--users 10`.",
        ["python seed.py --users 10", "python3 seed.py --users 10"]),
    cmd(f"{P}-run-e2", "Запусти модуль `pytest` через интерпретатор Python (так гарантированно используется pytest из текущего окружения).",
        ["python -m pytest", "python3 -m pytest"]),
    cmd(f"{P}-run-e3", "Выполни однострочник: выведи версию Python через `python -c`.",
        ["python -c 'import sys; print(sys.version)'", 'python -c "import sys; print(sys.version)"', "python --version", "python -V",
         "python3 --version", "python3 -V"]),
    cmd(f"{P}-run-e4", "Что будет в `sys.argv`? Введи Python-список.",
        ["['seed.py', '--users', '10']", '["seed.py", "--users", "10"]'],
        context="""
        $ python seed.py --users 10
        """),
    cod(f"{P}-run-e5", t("""
        Напиши функцию `parse_args(argv)` на `argparse`: аргументы `--env` (строка, по умолчанию `"dev"`), `--workers` (int, по умолчанию `1`) и флаг `--headless` (по умолчанию `False`). Вернуть объект `Namespace`.
        """),
        """
        import argparse


        def parse_args(argv):
            pass
        """,
        """
        def test_values():
            a = parse_args([])
            assert (a.env, a.workers, a.headless) == ("dev", 1, False), vars(a)
            b = parse_args(["--env", "stage", "--workers", "4", "--headless"])
            assert (b.env, b.workers, b.headless) == ("stage", 4, True), vars(b)
        """,
        """
        import argparse


        def parse_args(argv):
            parser = argparse.ArgumentParser()
            parser.add_argument("--env", default="dev")
            parser.add_argument("--workers", type=int, default=1)
            parser.add_argument("--headless", action="store_true")
            return parser.parse_args(argv)
        """, hint="action='store_true' — флаг без значения."),
    cod(f"{P}-run-e6", t("""
        Напиши функцию `main(argv)` для скрипта-проверки: `argv` — список аргументов без имени скрипта. Если передан хотя бы один аргумент — вернуть код `0` и напечатать `"проверяю: a, b"` (аргументы через запятую). Если аргументов нет — напечатать `"usage: check.py FILE..."` и вернуть код `2`.
        """),
        """
        def main(argv):
            pass
        """,
        """
        import io, contextlib

        def test_values():
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                codes = (main(["a.json", "b.json"]), main([]))
            assert codes == (0, 2), codes
            assert buf.getvalue() == "проверяю: a.json, b.json\\nusage: check.py FILE...\\n", repr(buf.getvalue())
        """,
        """
        def main(argv):
            if not argv:
                print("usage: check.py FILE...")
                return 2
            print("проверяю: " + ", ".join(argv))
            return 0
        """, hint="В настоящем скрипте: if __name__ == '__main__': sys.exit(main(sys.argv[1:]))"),
    cmd(f"{P}-run-e7", "Какой код выхода у успешной программы? Введи число.",
        ["0"], hint="CI считает шаг проваленным при любом ненулевом коде."),
    cmd(f"{P}-run-e8", "Покажи код выхода последней выполненной команды в bash.",
        ["echo $?"], xp=15),
),
)
