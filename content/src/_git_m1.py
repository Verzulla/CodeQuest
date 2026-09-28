"""Тема «Git», модуль 1 «Основы» — задания. Теория — в _git_t1.py."""
from ._lib import cmd, cod, lesson, module, t

P = "git"

m1 = module(f"{P}-m1", "Основы", "🌱", "Репозиторий, коммиты и индекс, история и diff, .gitignore",

lesson(f"{P}-intro", "Репозиторий: init, clone, status",
    cmd(f"{P}-intro-e1", "Преврати текущую папку в git-репозиторий.",
        ["git init"]),
    cmd(f"{P}-intro-e2", "Скачай репозиторий `https://github.com/acme/api-tests.git` к себе на компьютер.",
        ["git clone https://github.com/acme/api-tests.git", "git clone https://github.com/acme/api-tests"]),
    cmd(f"{P}-intro-e3", "Покажи текущее состояние репозитория: какие файлы изменены, какие добавлены в коммит.",
        ["git status", "git status -s", "git status --short"]),
    cmd(f"{P}-intro-e4", "Как называется текущая ветка? Введи только её имя.",
        ["main"],
        context="""
        $ git status
        On branch main
        Your branch is up to date with 'origin/main'.

        nothing to commit, working tree clean
        """),
    cmd(f"{P}-intro-e5", "Какой файл git ещё **не отслеживает** (новый)? Введи имя файла.",
        ["tests/test_cart.py"],
        context="""
        $ git status
        On branch main
        Changes not staged for commit:
                modified:   tests/test_login.py

        Untracked files:
                tests/test_cart.py
        """),
    cmd(f"{P}-intro-e6", "Задай имя автора коммитов `Anna Petrova` для **всех** своих репозиториев.",
        ['git config --global user.name "Anna Petrova"', "git config --global user.name 'Anna Petrova'"]),
    cmd(f"{P}-intro-e7", "Скачай репозиторий `https://github.com/acme/ui-tests.git` в папку с именем `ui`.",
        ["git clone https://github.com/acme/ui-tests.git ui", "git clone https://github.com/acme/ui-tests ui"]),
    cod(f"{P}-intro-e8", t("""
        Напиши функцию `parse_status(lines)` — разобрать короткий вывод `git status -s`. Каждая строка: два символа статуса, пробел, путь. Верни словарь `{"modified": [...], "added": [...], "untracked": [...], "deleted": [...]}`:

        - `" M"` или `"M "` → modified;
        - `"A "` → added;
        - `"??"` → untracked;
        - `" D"` или `"D "` → deleted.
        """),
        """
        def parse_status(lines):
            pass
        """,
        """
        def test_values():
            lines = [" M tests/test_login.py", "?? tests/test_cart.py", "A  conftest.py", " D old.py", "M  README.md"]
            assert parse_status(lines) == {"modified": ["tests/test_login.py", "README.md"], "added": ["conftest.py"],
                                           "untracked": ["tests/test_cart.py"], "deleted": ["old.py"]}, parse_status(lines)
            assert parse_status([]) == {"modified": [], "added": [], "untracked": [], "deleted": []}, "Чистый репозиторий"
        """,
        """
        def parse_status(lines):
            result = {"modified": [], "added": [], "untracked": [], "deleted": []}
            for line in lines:
                code, path = line[:2], line[3:]
                if code == "??":
                    result["untracked"].append(path)
                elif "A" in code:
                    result["added"].append(path)
                elif "D" in code:
                    result["deleted"].append(path)
                elif "M" in code:
                    result["modified"].append(path)
            return result
        """, xp=20),
),

lesson(f"{P}-commit", "Коммиты: add и commit",
    cmd(f"{P}-commit-e1", "Добавь в индекс (подготовь к коммиту) файл `tests/test_login.py`.",
        ["git add tests/test_login.py"]),
    cmd(f"{P}-commit-e2", "Добавь в индекс **все** изменения в текущей папке.",
        ["git add .", "git add -A", "git add --all"]),
    cmd(f"{P}-commit-e3", "Сделай коммит с сообщением `Add login tests`.",
        ['git commit -m "Add login tests"', "git commit -m 'Add login tests'"]),
    cmd(f"{P}-commit-e4", "Одной командой добавь в коммит все изменения **уже отслеживаемых** файлов и сделай коммит с сообщением `Fix flaky test`.",
        ['git commit -am "Fix flaky test"', "git commit -am 'Fix flaky test'", 'git commit -a -m "Fix flaky test"',
         "git commit -a -m 'Fix flaky test'"], hint="Флаг -a сам добавляет изменённые файлы (но не новые)."),
    cmd(f"{P}-commit-e5", "Убери файл `debug.log` из индекса (он был добавлен по ошибке), не удаляя сам файл.",
        ["git restore --staged debug.log", "git reset debug.log", "git reset HEAD debug.log", "git rm --cached debug.log"]),
    cmd(f"{P}-commit-e6", "Сколько файлов попадёт в следующий коммит? Введи число.",
        ["2"],
        context="""
        $ git status
        Changes to be committed:
                modified:   conftest.py
                new file:   tests/test_cart.py

        Changes not staged for commit:
                modified:   README.md
        """, hint="В коммит попадает только то, что в разделе «Changes to be committed»."),
    cmd(f"{P}-commit-e7", "Добавь в индекс все файлы `.py` из папки `tests`.",
        ["git add tests/*.py", "git add 'tests/*.py'", 'git add "tests/*.py"', "git add tests/\\*.py"]),
    cod(f"{P}-commit-e8", t("""
        Во многих командах сообщения коммитов пишут по правилу **Conventional Commits**: `тип(область): описание` или `тип: описание`, где тип — один из `feat`, `fix`, `test`, `docs`, `refactor`, `chore`, `ci`. Описание не пустое и не длиннее 72 символов.

        Напиши функцию `is_conventional(message)` — `True`, если **первая строка** сообщения подходит под правило.
        """),
        """
        import re


        def is_conventional(message):
            pass
        """,
        """
        def test_values():
            good = ["test: add login cases", "fix(api): handle 404", "ci: run tests in parallel\\n\\nподробности"]
            bad = ["Add tests", "feat:", "bug: fix", "test(api) add", "docs: " + "x" * 80]
            assert all(is_conventional(m) for m in good), [m for m in good if not is_conventional(m)]
            assert not any(is_conventional(m) for m in bad), [m for m in bad if is_conventional(m)]
        """,
        """
        import re

        PATTERN = re.compile(r"(feat|fix|test|docs|refactor|chore|ci)(\\([\\w-]+\\))?: (.+)")


        def is_conventional(message):
            first = message.splitlines()[0] if message else ""
            m = PATTERN.fullmatch(first)
            return bool(m) and len(m.group(3)) <= 72
        """, xp=20),
),

lesson(f"{P}-log", "История и изменения: log, diff, show",
    cmd(f"{P}-log-e1", "Покажи историю коммитов, по одной строке на коммит.",
        ["git log --oneline", "git log --pretty=oneline"]),
    cmd(f"{P}-log-e2", "Покажи последние 5 коммитов в кратком виде.",
        ["git log --oneline -5", "git log --oneline -n 5", "git log -5 --oneline", "git log -n 5 --oneline", "git log --oneline -n5"]),
    cmd(f"{P}-log-e3", "Покажи, что изменилось в файлах, но ещё **не добавлено** в индекс.",
        ["git diff"]),
    cmd(f"{P}-log-e4", "Покажи изменения, которые **уже в индексе** и попадут в коммит.",
        ["git diff --staged", "git diff --cached"]),
    cmd(f"{P}-log-e5", "Покажи содержимое коммита `a1b2c3d`: сообщение и изменения.",
        ["git show a1b2c3d"]),
    cmd(f"{P}-log-e6", "Покажи историю изменений только одного файла `tests/test_login.py`.",
        ["git log tests/test_login.py", "git log -- tests/test_login.py", "git log --oneline tests/test_login.py",
         "git log --oneline -- tests/test_login.py", "git log -p tests/test_login.py", "git log -p -- tests/test_login.py"]),
    cmd(f"{P}-log-e7", "Какой хеш у коммита, который **добавил тесты корзины**? Введи 7 символов.",
        ["9f8e7d6"],
        context="""
        $ git log --oneline
        4c3b2a1 (HEAD -> main) fix: flaky timeout in cart
        9f8e7d6 test: add cart tests
        1a2b3c4 feat: cart page
        """),
    cod(f"{P}-log-e8", t("""
        Напиши функцию `parse_oneline(lines)` — разобрать вывод `git log --oneline` в список словарей `{"hash": ..., "message": ...}`. Пометки в скобках вроде `(HEAD -> main)` или `(tag: v1.0)` в начале сообщения нужно убрать.
        """),
        """
        import re


        def parse_oneline(lines):
            pass
        """,
        """
        def test_values():
            lines = ["4c3b2a1 (HEAD -> main, origin/main) fix: flaky timeout", "9f8e7d6 test: add cart tests", "1a2b3c4 (tag: v1.0) feat: cart page"]
            assert parse_oneline(lines) == [
                {"hash": "4c3b2a1", "message": "fix: flaky timeout"},
                {"hash": "9f8e7d6", "message": "test: add cart tests"},
                {"hash": "1a2b3c4", "message": "feat: cart page"},
            ], parse_oneline(lines)
        """,
        """
        import re


        def parse_oneline(lines):
            result = []
            for line in lines:
                sha, rest = line.split(" ", 1)
                rest = re.sub(r"^\\([^)]*\\) ", "", rest)
                result.append({"hash": sha, "message": rest})
            return result
        """, xp=20),
),

lesson(f"{P}-ignore", "Что не коммитить: .gitignore",
    cmd(f"{P}-ignore-e1", "Какую строку добавить в `.gitignore`, чтобы git игнорировал папку виртуального окружения `.venv`?",
        [".venv/", ".venv", "/.venv", "/.venv/"]),
    cmd(f"{P}-ignore-e2", "Какая строка в `.gitignore` заставит игнорировать **все** файлы с расширением `.log`?",
        ["*.log"]),
    cmd(f"{P}-ignore-e3", "Какая строка игнорирует папку с результатами Allure `allure-results`?",
        ["allure-results/", "allure-results", "/allure-results/", "/allure-results"]),
    cmd(f"{P}-ignore-e4", "Файл `.env` с паролями **уже** попал в репозиторий. Убери его из git (из отслеживания), но оставь на диске.",
        ["git rm --cached .env"], hint="Потом добавь .env в .gitignore и закоммить удаление."),
    cmd(f"{P}-ignore-e5", "Какая строка `.gitignore` игнорирует все папки `__pycache__` на любом уровне?",
        ["__pycache__/", "__pycache__", "**/__pycache__/", "**/__pycache__"]),
    cmd(f"{P}-ignore-e6", "Проверь, какое правило `.gitignore` заставляет игнорировать файл `report.html`.",
        ["git check-ignore -v report.html", "git check-ignore --verbose report.html"]),
    cmd(f"{P}-ignore-e7", "Как в `.gitignore` сделать **исключение**: игнорировать все `.json`, кроме `schema.json`? Введи строку-исключение.",
        ["!schema.json", "!/schema.json"], hint="Исключение начинается с восклицательного знака."),
    cod(f"{P}-ignore-e8", t("""
        Напиши упрощённую проверку `.gitignore`: функцию `is_ignored(path, patterns)`. Путь игнорируется, если **хотя бы одна часть** пути (папка или имя файла) подходит под один из шаблонов (`fnmatch`). Шаблон может заканчиваться на `/` — тогда он относится только к папкам (не к последней части пути). Исключений `!` в этой задаче нет.
        """),
        """
        import fnmatch


        def is_ignored(path, patterns):
            pass
        """,
        """
        def test_values():
            pats = [".venv/", "*.log", "__pycache__/", "allure-results/"]
            yes = [".venv/lib/x.py", "app.log", "tests/__pycache__/a.pyc", "allure-results/1.json", "logs/run.log"]
            no = ["tests/test_log.py", "README.md", "src/app.py", "venv.txt"]
            assert all(is_ignored(p, pats) for p in yes), [p for p in yes if not is_ignored(p, pats)]
            assert not any(is_ignored(p, pats) for p in no), [p for p in no if is_ignored(p, pats)]
            assert not is_ignored("allure-results", pats), "Шаблон с / — только для папок"
        """,
        """
        import fnmatch


        def is_ignored(path, patterns):
            parts = path.split("/")
            for pat in patterns:
                dir_only = pat.endswith("/")
                pat = pat.rstrip("/")
                candidates = parts[:-1] if dir_only else parts
                if any(fnmatch.fnmatch(part, pat) for part in candidates):
                    return True
            return False
        """, xp=25),
),
)
