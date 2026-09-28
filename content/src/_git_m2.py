"""Тема «Git», модуль 2 «Ветки и командная работа» — задания. Теория — в _git_t2.py."""
from ._lib import cmd, cod, lesson, module, t

P = "git"

m2 = module(f"{P}-m2", "Ветки и командная работа", "🌿", "Ветки, слияние и конфликты, удалённый репозиторий, pull request",

lesson(f"{P}-branch", "Ветки",
    cmd(f"{P}-branch-e1", "Покажи список локальных веток.",
        ["git branch", "git branch --list"]),
    cmd(f"{P}-branch-e2", "Создай новую ветку `feature/login-tests` и сразу переключись на неё.",
        ["git switch -c feature/login-tests", "git checkout -b feature/login-tests"]),
    cmd(f"{P}-branch-e3", "Переключись на существующую ветку `main`.",
        ["git switch main", "git checkout main"]),
    cmd(f"{P}-branch-e4", "Удали локальную ветку `feature/old`, которая уже слита в основную.",
        ["git branch -d feature/old", "git branch --delete feature/old"]),
    cmd(f"{P}-branch-e5", "Покажи **все** ветки, включая ветки удалённого репозитория.",
        ["git branch -a", "git branch --all"]),
    cmd(f"{P}-branch-e6", "На какой ветке ты сейчас? Введи её имя.",
        ["bugfix/timeout"],
        context="""
        $ git branch
          main
        * bugfix/timeout
          feature/cart
        """, hint="Текущая ветка отмечена звёздочкой."),
    cmd(f"{P}-branch-e7", "Переименуй **текущую** ветку в `feature/cart-tests`.",
        ["git branch -m feature/cart-tests", "git branch --move feature/cart-tests"]),
    cod(f"{P}-branch-e8", t("""
        В команде договорились называть ветки так: `тип/описание`, где тип — `feature`, `bugfix`, `test` или `hotfix`, а описание — строчные латинские буквы, цифры и дефисы (например, `test/login-2fa`). Напиши функцию `valid_branch(name)`.
        """),
        """
        import re


        def valid_branch(name):
            pass
        """,
        """
        def test_values():
            good = ["feature/login", "test/login-2fa", "bugfix/cart-timeout", "hotfix/500-on-pay"]
            bad = ["main", "feature/Login", "tests/login", "feature/", "feature/login tests", "feature/логин"]
            assert all(valid_branch(b) for b in good), [b for b in good if not valid_branch(b)]
            assert not any(valid_branch(b) for b in bad), [b for b in bad if valid_branch(b)]
        """,
        """
        import re


        def valid_branch(name):
            return re.fullmatch(r"(feature|bugfix|test|hotfix)/[a-z0-9-]+", name) is not None
        """),
),

lesson(f"{P}-merge", "Слияние и конфликты",
    cmd(f"{P}-merge-e1", "Ты на ветке `main`. Влей в неё изменения из ветки `feature/cart`.",
        ["git merge feature/cart"]),
    cmd(f"{P}-merge-e2", "Во время слияния возник конфликт, и ты хочешь всё отменить и вернуться к состоянию до `merge`.",
        ["git merge --abort"]),
    cmd(f"{P}-merge-e3", "Какой файл в конфликте? Введи путь.",
        ["tests/conftest.py"],
        context="""
        $ git merge feature/cart
        Auto-merging tests/conftest.py
        CONFLICT (content): Merge conflict in tests/conftest.py
        Automatic merge failed; fix conflicts and then commit the result.
        """),
    cmd(f"{P}-merge-e4", "Ты вручную исправил конфликт в `tests/conftest.py`. Какой командой отметить файл как разрешённый?",
        ["git add tests/conftest.py"]),
    cmd(f"{P}-merge-e5", "После разрешения всех конфликтов заверши слияние коммитом (без указания сообщения — git подставит своё).",
        ["git commit", "git commit --no-edit", "git merge --continue"]),
    cmd(f"{P}-merge-e6", "Какое значение `TIMEOUT` в ветке, которую **вливают** (`feature/cart`)? Введи число.",
        ["30"],
        context="""
        <<<<<<< HEAD
        TIMEOUT = 10
        =======
        TIMEOUT = 30
        >>>>>>> feature/cart
        """, hint="Между <<<<<<< и ======= — текущая ветка, между ======= и >>>>>>> — вливаемая."),
    cmd(f"{P}-merge-e7", "Покажи список файлов с неразрешёнными конфликтами одной командой `git diff` с флагом.",
        ["git diff --name-only --diff-filter=U", "git diff --diff-filter=U --name-only"]),
    cod(f"{P}-merge-e8", t("""
        Напиши функцию `resolve(text, side)` — разрешить конфликты в тексте файла: для каждого блока
        `<<<<<<< …` / `=======` / `>>>>>>> …` оставить строки стороны `"ours"` (до `=======`) или `"theirs"` (после). Строки вне конфликтов сохраняются. Вернуть текст с `\\n` между строками.
        """),
        """
        def resolve(text, side):
            pass
        """,
        """
        TEXT = "import os\\n<<<<<<< HEAD\\nTIMEOUT = 10\\n=======\\nTIMEOUT = 30\\nRETRIES = 2\\n>>>>>>> feature/cart\\nURL = 'x'"

        def test_values():
            assert resolve(TEXT, "ours") == "import os\\nTIMEOUT = 10\\nURL = 'x'", resolve(TEXT, "ours")
            assert resolve(TEXT, "theirs") == "import os\\nTIMEOUT = 30\\nRETRIES = 2\\nURL = 'x'", resolve(TEXT, "theirs")
            assert resolve("a\\nb", "ours") == "a\\nb", "Без конфликтов"
        """,
        """
        def resolve(text, side):
            result = []
            state = None
            for line in text.split("\\n"):
                if line.startswith("<<<<<<<"):
                    state = "ours"
                elif line.startswith("=======") and state == "ours":
                    state = "theirs"
                elif line.startswith(">>>>>>>") and state == "theirs":
                    state = None
                elif state is None or state == side:
                    result.append(line)
            return "\\n".join(result)
        """, xp=25),
),

lesson(f"{P}-remote", "Удалённый репозиторий: push, pull, fetch",
    cmd(f"{P}-remote-e1", "Покажи удалённые репозитории и их адреса.",
        ["git remote -v", "git remote --verbose"]),
    cmd(f"{P}-remote-e2", "Отправь новую ветку `feature/login-tests` в удалённый репозиторий `origin` впервые и свяжи её с ним.",
        ["git push -u origin feature/login-tests", "git push --set-upstream origin feature/login-tests"]),
    cmd(f"{P}-remote-e3", "Ветка уже связана с удалённой. Отправь новые коммиты.",
        ["git push"]),
    cmd(f"{P}-remote-e4", "Забери свежие изменения из удалённой ветки и сразу влей их в текущую.",
        ["git pull", "git pull origin", "git pull --rebase"]),
    cmd(f"{P}-remote-e5", "Скачай информацию о новых коммитах и ветках с `origin`, **ничего не вливая** в свои ветки.",
        ["git fetch", "git fetch origin", "git fetch --all"]),
    cmd(f"{P}-remote-e6", "Переключись на ветку коллеги `feature/payment`, которая есть только на `origin` (после `git fetch`).",
        ["git switch feature/payment", "git checkout feature/payment", "git switch -c feature/payment origin/feature/payment",
         "git checkout -b feature/payment origin/feature/payment", "git checkout -t origin/feature/payment",
         "git switch --track origin/feature/payment", "git checkout --track origin/feature/payment"]),
    cmd(f"{P}-remote-e7", "На сколько коммитов твоя ветка отстаёт от удалённой? Введи число.",
        ["3"],
        context="""
        $ git status
        On branch main
        Your branch is behind 'origin/main' by 3 commits, and can be fast-forwarded.
        """),
    cmd(f"{P}-remote-e8", t("""
        `git push` отклонён: «Updates were rejected because the remote contains work that you do not have locally». Какой командой **сначала** забрать чужие изменения, переставив свои коммиты поверх них (без коммита слияния)?
        """),
        ["git pull --rebase", "git pull --rebase origin main", "git pull -r"], xp=15),
),

lesson(f"{P}-pr", "Pull request и работа в команде",
    cmd(f"{P}-pr-e1", t("""
        Типичный цикл тестировщика. Ты на `main`. Сначала обнови `main` с сервера — введи команду.
        """),
        ["git pull", "git pull origin main", "git pull --rebase"]),
    cmd(f"{P}-pr-e2", "Создай от `main` ветку `test/cart-e2e` и переключись на неё.",
        ["git switch -c test/cart-e2e", "git checkout -b test/cart-e2e"]),
    cmd(f"{P}-pr-e3", "Ты написал тесты. Добавь все изменения и сделай коммит `test: add cart e2e`.",
        ['git add . && git commit -m "test: add cart e2e"', "git add . && git commit -m 'test: add cart e2e'",
         'git add -A && git commit -m "test: add cart e2e"', "git add -A && git commit -m 'test: add cart e2e'",
         'git commit -am "test: add cart e2e"', "git commit -am 'test: add cart e2e'"],
        hint="Две команды можно соединить через &&."),
    cmd(f"{P}-pr-e4", "Отправь ветку `test/cart-e2e` на `origin` и свяжи её, чтобы открыть pull request.",
        ["git push -u origin test/cart-e2e", "git push --set-upstream origin test/cart-e2e", "git push -u origin HEAD"]),
    cmd(f"{P}-pr-e5", "Создай pull request из текущей ветки через GitHub CLI (утилита `gh`), без дополнительных параметров.",
        ["gh pr create", "gh pr create --fill", "gh pr create -f"]),
    cmd(f"{P}-pr-e6", "Скачай к себе и переключись на ветку pull request №42 через GitHub CLI, чтобы протестировать его локально.",
        ["gh pr checkout 42"]),
    cmd(f"{P}-pr-e7", "Ревьюер попросил поправить тест. Ты исправил файл. Какими командами обновить PR? Добавь все изменения, закоммить с сообщением `fix: review comments` и отправь.",
        ['git add . && git commit -m "fix: review comments" && git push', "git add . && git commit -m 'fix: review comments' && git push",
         'git commit -am "fix: review comments" && git push', "git commit -am 'fix: review comments' && git push",
         'git add -A && git commit -m "fix: review comments" && git push', "git add -A && git commit -m 'fix: review comments' && git push"],
        xp=15),
    cod(f"{P}-pr-e8", t("""
        Напиши функцию `pr_checklist(pr)` — «бот» для pull request. `pr` — словарь `{"title": str, "branch": str, "files": [пути], "tests_passed": bool}`. Вернуть список замечаний (пустой — всё хорошо):

        - `"нет префикса в заголовке"` — если заголовок не начинается с `feat:`, `fix:` или `test:`;
        - `"ветка main"` — если ветка `main`;
        - `"изменён код без тестов"` — если среди файлов есть `src/...`, но нет ни одного `tests/...`;
        - `"тесты упали"` — если `tests_passed` ложно.
        """),
        """
        def pr_checklist(pr):
            pass
        """,
        """
        def test_values():
            ok = {"title": "test: cart", "branch": "test/cart", "files": ["tests/test_cart.py"], "tests_passed": True}
            assert pr_checklist(ok) == [], pr_checklist(ok)
            bad = {"title": "cart", "branch": "main", "files": ["src/cart.py"], "tests_passed": False}
            assert pr_checklist(bad) == ["нет префикса в заголовке", "ветка main", "изменён код без тестов", "тесты упали"], pr_checklist(bad)
            mixed = {"title": "fix: cart", "branch": "bugfix/cart", "files": ["src/cart.py", "tests/test_cart.py"], "tests_passed": True}
            assert pr_checklist(mixed) == [], "Код с тестами — хорошо"
        """,
        """
        def pr_checklist(pr):
            issues = []
            if not pr["title"].startswith(("feat:", "fix:", "test:")):
                issues.append("нет префикса в заголовке")
            if pr["branch"] == "main":
                issues.append("ветка main")
            has_src = any(f.startswith("src/") for f in pr["files"])
            has_tests = any(f.startswith("tests/") for f in pr["files"])
            if has_src and not has_tests:
                issues.append("изменён код без тестов")
            if not pr["tests_passed"]:
                issues.append("тесты упали")
            return issues
        """, xp=20),
),
)
