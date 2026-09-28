"""Тема «Git», модуль 3 «Исправление ошибок и продвинутое» — задания. Теория — в _git_t3.py."""
from ._lib import cmd, cod, lesson, module, t

P = "git"

m3 = module(f"{P}-m3", "Исправление ошибок и продвинутое", "🛠️", "Отмена изменений, stash, rebase, cherry-pick, теги, blame и bisect",

lesson(f"{P}-undo", "Отменить изменения",
    cmd(f"{P}-undo-e1", "Отмени незакоммиченные изменения в файле `conftest.py` — верни его к последнему коммиту.",
        ["git restore conftest.py", "git checkout -- conftest.py", "git checkout conftest.py"]),
    cmd(f"{P}-undo-e2", "Ты сделал коммит, но забыл добавить файл и хочешь **исправить последний коммит** (файл уже добавлен в индекс), не меняя сообщение.",
        ["git commit --amend --no-edit", "git commit --no-edit --amend"]),
    cmd(f"{P}-undo-e3", "Исправь опечатку в сообщении последнего коммита на `test: add login cases`.",
        ['git commit --amend -m "test: add login cases"', "git commit --amend -m 'test: add login cases'"]),
    cmd(f"{P}-undo-e4", "Отмени последний коммит, но **сохрани** его изменения в рабочих файлах (коммит ещё не отправлен).",
        ["git reset HEAD~1", "git reset HEAD~", "git reset --mixed HEAD~1", "git reset --soft HEAD~1", "git reset HEAD^",
         "git reset --soft HEAD~", "git reset --mixed HEAD~"]),
    cmd(f"{P}-undo-e5", "Коммит `a1b2c3d` уже отправлен и сломал тесты. Создай новый коммит, который отменяет его изменения (историю не переписывать).",
        ["git revert a1b2c3d", "git revert --no-edit a1b2c3d"]),
    cmd(f"{P}-undo-e6", "Полностью выбрось последний **неотправленный** коммит вместе с изменениями (осторожно!).",
        ["git reset --hard HEAD~1", "git reset --hard HEAD~", "git reset --hard HEAD^"]),
    cmd(f"{P}-undo-e7", "Ты случайно сделал `reset --hard`. Какой командой посмотреть журнал всех перемещений HEAD, чтобы найти потерянный коммит?",
        ["git reflog", "git reflog show", "git log -g"]),
    cmd(f"{P}-undo-e8", t("""
        Удали из рабочей папки все **неотслеживаемые** файлы и папки (мусор после прогона тестов). Используй флаги для файлов и папок.
        """),
        ["git clean -fd", "git clean -df", "git clean -f -d", "git clean -d -f", "git clean -fdx", "git clean -xfd"],
        hint="Сначала можно посмотреть, что удалится: git clean -nd.", xp=15),
),

lesson(f"{P}-stash", "Отложить работу: stash",
    cmd(f"{P}-stash-e1", "Тебя срочно попросили проверить другую ветку. Спрячь текущие незакоммиченные изменения.",
        ["git stash", "git stash push"]),
    cmd(f"{P}-stash-e2", "Верни последние спрятанные изменения и удали их из хранилища.",
        ["git stash pop"]),
    cmd(f"{P}-stash-e3", "Покажи список всех спрятанных наборов изменений.",
        ["git stash list"]),
    cmd(f"{P}-stash-e4", "Спрячь изменения с понятным описанием `wip cart tests`.",
        ['git stash push -m "wip cart tests"', "git stash push -m 'wip cart tests'", 'git stash save "wip cart tests"',
         "git stash save 'wip cart tests'", 'git stash -m "wip cart tests"', "git stash -m 'wip cart tests'"]),
    cmd(f"{P}-stash-e5", "Спрячь изменения **вместе с новыми (неотслеживаемыми)** файлами.",
        ["git stash -u", "git stash push -u", "git stash --include-untracked", "git stash push --include-untracked"]),
    cmd(f"{P}-stash-e6", "Примени второй по счёту stash (`stash@{1}`), **не удаляя** его из списка.",
        ["git stash apply stash@{1}", "git stash apply 1"]),
    cmd(f"{P}-stash-e7", "Какой stash самый свежий? Введи его описание.",
        ["wip login"],
        context="""
        $ git stash list
        stash@{0}: On test/login: wip login
        stash@{1}: On test/cart: wip cart
        """, hint="stash@{0} — последний спрятанный."),
    cmd(f"{P}-stash-e8", "Удали все спрятанные наборы изменений.",
        ["git stash clear"]),
),

lesson(f"{P}-rebase", "Rebase и cherry-pick",
    cmd(f"{P}-rebase-e1", "Ты на ветке `test/cart`. Перенеси свои коммиты поверх свежего `main` (он уже обновлён локально).",
        ["git rebase main"]),
    cmd(f"{P}-rebase-e2", "Во время rebase был конфликт, ты его исправил и сделал `git add`. Как продолжить rebase?",
        ["git rebase --continue"]),
    cmd(f"{P}-rebase-e3", "Отмени начатый rebase и вернись к исходному состоянию ветки.",
        ["git rebase --abort"]),
    cmd(f"{P}-rebase-e4", "После rebase отправь переписанную ветку на сервер **безопасным** принудительным способом.",
        ["git push --force-with-lease", "git push --force-with-lease origin test/cart"],
        hint="--force-with-lease не затрёт чужие коммиты, которые ты ещё не видел."),
    cmd(f"{P}-rebase-e5", "Перенеси в текущую ветку один конкретный коммит `9f8e7d6` из другой ветки.",
        ["git cherry-pick 9f8e7d6"]),
    cmd(f"{P}-rebase-e6", "Обнови свою ветку от `origin/main` одной командой: забери изменения и перенеси свои коммиты поверх (ты на своей ветке).",
        ["git pull --rebase origin main", "git pull -r origin main"]),
    cmd(f"{P}-rebase-e7", "Сколько **твоих** коммитов будет перенесено при `git rebase main`? Введи число.",
        ["2"],
        context="""
        $ git log --oneline main..test/cart
        b2c3d4e test: cart edge cases
        a1b2c3d test: add cart tests
        """, hint="main..test/cart — коммиты, которые есть в test/cart, но нет в main."),
    cod(f"{P}-rebase-e8", t("""
        Смоделируй rebase. Функция `rebase(base, branch_commits)` — `base` — список коммитов целевой ветки (например, `main`), `branch_commits` — список коммитов твоей ветки, начиная с общего предка (первый элемент — общий коммит с `base`). Вернуть итоговую историю: все коммиты `base`, затем твои коммиты после общего предка, каждый с пометкой `'` (штрих — новый хеш после переноса).

        ```
        rebase(["A", "B", "C"], ["A", "X", "Y"])   # → ["A", "B", "C", "X'", "Y'"]
        ```
        """),
        """
        def rebase(base, branch_commits):
            pass
        """,
        """
        def test_values():
            assert rebase(["A", "B", "C"], ["A", "X", "Y"]) == ["A", "B", "C", "X'", "Y'"], rebase(["A", "B", "C"], ["A", "X", "Y"])
            assert rebase(["A", "B"], ["B", "Z"]) == ["A", "B", "Z'"] and rebase(["A"], ["A"]) == ["A"], "Другие случаи"
        """,
        """
        def rebase(base, branch_commits):
            return list(base) + [c + "'" for c in branch_commits[1:]]
        """, xp=20),
),

lesson(f"{P}-advanced", "Теги, blame, bisect",
    cmd(f"{P}-advanced-e1", "Поставь аннотированный тег `v1.2.0` на текущий коммит с сообщением `Release 1.2.0`.",
        ['git tag -a v1.2.0 -m "Release 1.2.0"', "git tag -a v1.2.0 -m 'Release 1.2.0'"]),
    cmd(f"{P}-advanced-e2", "Отправь все теги на `origin`.",
        ["git push --tags", "git push origin --tags"]),
    cmd(f"{P}-advanced-e3", "Узнай, кто и в каком коммите менял каждую строку файла `tests/test_pay.py`.",
        ["git blame tests/test_pay.py"]),
    cmd(f"{P}-advanced-e4", "Начни двоичный поиск коммита, который сломал тест.",
        ["git bisect start"]),
    cmd(f"{P}-advanced-e5", "Во время `bisect` ты проверил текущий коммит — тест **падает**. Как отметить его?",
        ["git bisect bad"]),
    cmd(f"{P}-advanced-e6", "Автоматизируй bisect: пусть git сам запускает `pytest tests/test_pay.py` на каждом шаге.",
        ["git bisect run pytest tests/test_pay.py", "git bisect run python -m pytest tests/test_pay.py"]),
    cmd(f"{P}-advanced-e7", "Покажи, в каких коммитах менялась строка `TIMEOUT` в истории (поиск по содержимому изменений).",
        ['git log -S "TIMEOUT"', "git log -S TIMEOUT", "git log -S 'TIMEOUT'", 'git log -G "TIMEOUT"', "git log -G TIMEOUT",
         'git log -p -S "TIMEOUT"', "git log -p -S TIMEOUT"]),
    cod(f"{P}-advanced-e8", t("""
        Реализуй идею `git bisect`: функция `first_bad(commits, is_bad)` — `commits` — список коммитов от старого к новому, первый точно хороший, последний точно плохой; `is_bad(commit)` — запуск теста. Найди **первый** плохой коммит двоичным поиском. Функция должна вызывать `is_bad` не больше `log2(n) + 2` раз.
        """),
        """
        def first_bad(commits, is_bad):
            pass
        """,
        """
        import math

        def test_values():
            commits = [f"c{i}" for i in range(100)]
            calls = []
            def is_bad(c):
                calls.append(c)
                return int(c[1:]) >= 63
            assert first_bad(commits, is_bad) == "c63", first_bad(commits, is_bad)
            assert len(calls) <= math.log2(100) + 2, f"Слишком много запусков: {len(calls)}"
            assert first_bad(["good", "bad"], lambda c: c == "bad") == "bad", "Два коммита"
        """,
        """
        def first_bad(commits, is_bad):
            lo, hi = 0, len(commits) - 1      # lo — хороший, hi — плохой
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if is_bad(commits[mid]):
                    hi = mid
                else:
                    lo = mid
            return commits[hi]
        """, xp=25),
),
)
