"""Тема «Git» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "git"

EXPLAIN = {

# ===== Модуль 1. Основы =====

f"{P}-intro-e1": x(
    idea="`git init` создаёт в папке скрытую `.git` — с этого момента git отслеживает историю.",
    lines=[("git init", "Новый пустой репозиторий.")],
    mistake="`git clone` — это скачать чужой репозиторий."),

f"{P}-intro-e2": x(
    idea="`git clone URL` скачивает репозиторий со всей историей в новую папку.",
    lines=[("git clone", "Скопировать."), ("https://github.com/acme/api-tests.git", "Откуда.")],
    mistake="`git pull URL` — работает только внутри уже существующего репозитория."),

f"{P}-intro-e3": x(
    idea="`git status` — главная команда «где я и что изменено».",
    lines=[("git status", "Ветка, изменённые, добавленные и новые файлы.")],
    mistake="`git log` — история коммитов, а не текущие изменения."),

f"{P}-intro-e4": x(
    idea="Первая строка `git status` — текущая ветка.",
    lines=[("On branch main", "Ветка `main`.")],
    mistake="Ответить `origin/main` — это удалённая ветка, с которой она связана."),

f"{P}-intro-e5": x(
    idea="Untracked — файлы, которых git ещё не знает. Modified — уже отслеживаемые и изменённые.",
    lines=[("Untracked files:", "Новые файлы."), ("tests/test_cart.py", "Тот самый.")],
    mistake="Ответить test_login.py — он отслеживается, просто изменён."),

f"{P}-intro-e6": x(
    idea="`--global` — настройка для всех репозиториев пользователя.",
    lines=[("git config --global", "Для всех проектов."), ('user.name "Anna Petrova"', "Имя с пробелом — в кавычках.")],
    mistake="Без кавычек — в имя попадёт только `Anna`."),

f"{P}-intro-e7": x(
    idea="Последний аргумент `clone` — имя папки.",
    lines=[("git clone https://github.com/acme/ui-tests.git", "Что скачать."), ("ui", "В какую папку.")],
    mistake="Сначала создать `ui` и клонировать в неё — получится `ui/ui-tests`."),

f"{P}-intro-e8": x(
    idea="Первые два символа — статус, с четвёртого — путь. Порядок проверок важен: `??` раньше остальных.",
    lines=[
        ("code, path = line[:2], line[3:]", "Статус и путь."),
        ('if code == "??":', "Неотслеживаемый."),
        ('elif "A" in code:', "Добавленный."),
        ('elif "D" in code:', "Удалённый."),
        ('elif "M" in code:', "Изменённый — в любой из двух колонок."),
    ],
    mistake="Сравнивать `code == \"M\"` — статус всегда из двух символов."),

f"{P}-commit-e1": x(
    idea="`git add` кладёт изменения файла в индекс — «черновик» следующего коммита.",
    lines=[("git add tests/test_login.py", "Один файл.")],
    mistake="Думать, что `add` уже сохраняет в историю — нужен ещё `commit`."),

f"{P}-commit-e2": x(
    idea="`.` — все изменения в текущей папке и вложенных.",
    lines=[("git add .", "Всё сразу.")],
    mistake="`git add *` — пропустит файлы, начинающиеся с точки."),

f"{P}-commit-e3": x(
    idea="`-m` — сообщение коммита сразу в команде.",
    lines=[("git commit -m", "Коммит с сообщением."), ('"Add login tests"', "В кавычках — там пробелы.")],
    mistake="Без `-m` — откроется редактор."),

f"{P}-commit-e4": x(
    idea="`-a` добавляет изменения всех **отслеживаемых** файлов; новые файлы не попадут.",
    lines=[("git commit -am", "add + commit."), ('"Fix flaky test"', "Сообщение.")],
    mistake="Ждать, что новый файл тоже попадёт в коммит."),

f"{P}-commit-e5": x(
    idea="`restore --staged` убирает файл из индекса, изменения на диске остаются.",
    lines=[("git restore --staged debug.log", "Только из индекса.")],
    mistake="`git restore debug.log` без `--staged` — откатит сам файл."),

f"{P}-commit-e6": x(
    idea="В коммит попадает только раздел «Changes to be committed».",
    lines=[("Changes to be committed:", "conftest.py и test_cart.py.")],
    mistake="Посчитать README.md — он не добавлен."),

f"{P}-commit-e7": x(
    idea="Шаблон `*.py` раскрывает оболочка (или git, если в кавычках).",
    lines=[("git add tests/*.py", "Все `.py` в `tests`.")],
    mistake="`git add *.py` — из текущей папки, а не из `tests`."),

f"{P}-commit-e8": x(
    idea="Регулярное выражение: тип из списка, необязательная область в скобках, двоеточие с пробелом, описание.",
    lines=[
        ('PATTERN = re.compile(r"(feat|fix|test|docs|refactor|chore|ci)(\\([\\w-]+\\))?: (.+)")', "Три группы: тип, область, описание."),
        ('first = message.splitlines()[0] if message else ""', "Проверяем первую строку."),
        ("m = PATTERN.fullmatch(first)", "Вся строка целиком."),
        ("return bool(m) and len(m.group(3)) <= 72", "Описание не длиннее 72."),
    ],
    mistake="`match` вместо `fullmatch` — пройдёт строка с мусором в конце."),

f"{P}-log-e1": x(
    idea="`--oneline` — короткий хеш и заголовок, одна строка на коммит.",
    lines=[("git log --oneline", "Компактная история.")],
    mistake="`git log` без флага — многострочный вывод."),

f"{P}-log-e2": x(
    idea="`-5` ограничивает число коммитов.",
    lines=[("git log --oneline -5", "Пять последних.")],
    mistake="`| head -5` без `--oneline` — первые 5 строк, а не коммитов."),

f"{P}-log-e3": x(
    idea="`git diff` без флагов — изменения, которых ещё нет в индексе.",
    lines=[("git diff", "Рабочие файлы против индекса.")],
    mistake="Ждать в выводе уже добавленные изменения."),

f"{P}-log-e4": x(
    idea="`--staged` — что уже в индексе, то есть войдёт в коммит.",
    lines=[("git diff --staged", "Индекс против последнего коммита.")],
    mistake="`git diff` — покажет только то, что не добавлено."),

f"{P}-log-e5": x(
    idea="`git show` — сообщение, автор и изменения коммита.",
    lines=[("git show a1b2c3d", "Коммит по хешу.")],
    mistake="`git log a1b2c3d` — история начиная с этого коммита."),

f"{P}-log-e6": x(
    idea="Путь после `git log` ограничивает историю одним файлом.",
    lines=[("git log tests/test_login.py", "Только коммиты, менявшие файл.")],
    mistake="`git show tests/test_login.py` — не история файла."),

f"{P}-log-e7": x(
    idea="Первый столбец `--oneline` — короткий хеш, дальше сообщение.",
    lines=[("9f8e7d6 test: add cart tests", "Добавил тесты корзины.")],
    mistake="Взять 4c3b2a1 — это исправление таймаута."),

f"{P}-log-e8": x(
    idea="Хеш — до первого пробела; пометку в скобках в начале убираем регуляркой.",
    lines=[
        ('sha, rest = line.split(" ", 1)', "Хеш и остаток."),
        ('rest = re.sub(r"^\\([^)]*\\) ", "", rest)', "Только скобки в самом начале."),
        ('result.append({"hash": sha, "message": rest})', "Словарь."),
    ],
    mistake="Удалять любые скобки — испортится сообщение вроде `fix(api): …`."),

f"{P}-ignore-e1": x(
    idea="Строка `.venv/` в `.gitignore` — игнорировать папку `.venv`.",
    lines=[(".venv/", "Слеш в конце — именно папка.")],
    mistake="Коммитить виртуальное окружение — тысячи лишних файлов."),

f"{P}-ignore-e2": x(
    idea="`*` — любое имя.",
    lines=[("*.log", "Все логи.")],
    mistake="`.log` — только файл с именем `.log`."),

f"{P}-ignore-e3": x(
    idea="Результаты прогона генерируются заново — их не коммитят.",
    lines=[("allure-results/", "Папка результатов.")],
    mistake="Игнорировать `allure-report` вместо `allure-results`."),

f"{P}-ignore-e4": x(
    idea="`.gitignore` не действует на уже отслеживаемые файлы. `rm --cached` убирает файл из git, оставляя на диске.",
    lines=[("git rm --cached .env", "Из индекса, не с диска.")],
    mistake="`git rm .env` — удалит и файл."),

f"{P}-ignore-e5": x(
    idea="Шаблон без `/` в начале действует на любом уровне вложенности.",
    lines=[("__pycache__/", "Все такие папки.")],
    mistake="`/__pycache__/` — только в корне."),

f"{P}-ignore-e6": x(
    idea="`check-ignore -v` показывает файл и строку `.gitignore` с правилом.",
    lines=[("git check-ignore -v report.html", "Какое правило сработало.")],
    mistake="Искать вручную по всем `.gitignore`."),

f"{P}-ignore-e7": x(
    idea="`!` в начале — исключение из предыдущих правил.",
    lines=[("!schema.json", "Не игнорировать этот файл.")],
    mistake="Поставить исключение выше `*.json` — следующее правило его перекроет."),

f"{P}-ignore-e8": x(
    idea="Шаблон с `/` на конце проверяем только на папках пути, остальные — на всех частях.",
    lines=[
        ('parts = path.split("/")', "Части пути."),
        ('dir_only = pat.endswith("/")', "Только папки?"),
        ("candidates = parts[:-1] if dir_only else parts", "Без имени файла."),
        ("if any(fnmatch.fnmatch(part, pat) for part in candidates):", "Хоть одна часть подходит."),
    ],
    mistake="Не убрать `/` из шаблона — `fnmatch` не совпадёт ни с одной частью."),

# ===== Модуль 2. Ветки и командная работа =====

f"{P}-branch-e1": x(
    idea="`git branch` — локальные ветки, текущая отмечена `*`.",
    lines=[("git branch", "Список.")],
    mistake="`git branch имя` — создаст ветку."),

f"{P}-branch-e2": x(
    idea="`switch -c` — создать и сразу переключиться.",
    lines=[("git switch -c", "Create + switch."), ("feature/login-tests", "Имя ветки.")],
    mistake="`git branch feature/login-tests` — создаст, но не переключит."),

f"{P}-branch-e3": x(
    idea="`git switch` переключает ветку.",
    lines=[("git switch main", "На `main`.")],
    mistake="`git switch -c main` — попытка создать уже существующую."),

f"{P}-branch-e4": x(
    idea="`-d` удаляет только слитую ветку (безопасно); `-D` — любую.",
    lines=[("git branch -d feature/old", "Слитая — удалится.")],
    mistake="`-D` по привычке — можно потерять неслитые коммиты."),

f"{P}-branch-e5": x(
    idea="`-a` — и локальные, и `remotes/origin/...`.",
    lines=[("git branch -a", "Все ветки.")],
    mistake="`git branch -r` — только удалённые."),

f"{P}-branch-e6": x(
    idea="Текущая ветка отмечена звёздочкой.",
    lines=[("* bugfix/timeout", "Звёздочка — здесь.")],
    mistake="Ответить `main` — она первая в списке, но не текущая."),

f"{P}-branch-e7": x(
    idea="`-m` (move) переименовывает; без старого имени — текущую ветку.",
    lines=[("git branch -m feature/cart-tests", "Новое имя.")],
    mistake="Создать новую ветку и удалить старую — лишние шаги."),

f"{P}-branch-e8": x(
    idea="`fullmatch` — вся строка по шаблону: тип из списка, `/`, описание из разрешённых символов.",
    lines=[('return re.fullmatch(r"(feature|bugfix|test|hotfix)/[a-z0-9-]+", name) is not None', "Заглавные и подчёркивания не пройдут.")],
    mistake="`re.match` — пропустит хвост с недопустимыми символами."),

f"{P}-merge-e1": x(
    idea="`git merge ветка` вливает её в **текущую**.",
    lines=[("git merge feature/cart", "В `main`, где ты сейчас.")],
    mistake="Сначала переключиться на `feature/cart` — тогда `main` вольётся в неё."),

f"{P}-merge-e2": x(
    idea="`--abort` отменяет слияние и возвращает всё как было.",
    lines=[("git merge --abort", "Как будто merge не начинали.")],
    mistake="`git reset --hard` — потеряешь и незакоммиченную работу."),

f"{P}-merge-e3": x(
    idea="Строка `CONFLICT` называет файл.",
    lines=[("Merge conflict in tests/conftest.py", "Этот файл.")],
    mistake="Ответить «Auto-merging» — это ещё не конфликт."),

f"{P}-merge-e4": x(
    idea="После ручного исправления файл добавляют в индекс — это и значит «разрешён».",
    lines=[("git add tests/conftest.py", "Конфликт снят.")],
    mistake="Сразу `git commit` без `add` — git скажет, что конфликты не разрешены."),

f"{P}-merge-e5": x(
    idea="`git commit` без `-m` завершает слияние со стандартным сообщением.",
    lines=[("git commit", "Коммит слияния.")],
    mistake="`git merge feature/cart` ещё раз — слияние уже идёт."),

f"{P}-merge-e6": x(
    idea="До `=======` — текущая ветка (HEAD), после — вливаемая.",
    lines=[("TIMEOUT = 30", "Сторона `feature/cart`.")],
    mistake="Ответить 10 — это `HEAD`, твоя ветка."),

f"{P}-merge-e7": x(
    idea="`--diff-filter=U` — только неслитые (Unmerged), `--name-only` — только имена.",
    lines=[("git diff --name-only --diff-filter=U", "Список файлов в конфликте.")],
    mistake="`git diff` без флагов — весь текст изменений."),

f"{P}-merge-e8": x(
    idea="Состояние: вне конфликта, в части ours, в части theirs. Маркеры не копируем, строки берём только нужной стороны.",
    lines=[
        ('if line.startswith("<<<<<<<"):\n            state = "ours"', "Начало блока."),
        ('elif line.startswith("=======") and state == "ours":\n            state = "theirs"', "Разделитель."),
        ('elif line.startswith(">>>>>>>") and state == "theirs":\n            state = None', "Конец блока."),
        ("elif state is None or state == side:\n            result.append(line)", "Общие строки и выбранная сторона."),
    ],
    mistake="Считать `=======` маркером вне блока — испортится текст с такой строкой."),

f"{P}-remote-e1": x(
    idea="`remote -v` — имена удалённых репозиториев и их адреса.",
    lines=[("git remote -v", "origin и URL.")],
    mistake="`git remote` без `-v` — только имена."),

f"{P}-remote-e2": x(
    idea="`-u` связывает локальную ветку с удалённой — дальше хватит `git push`.",
    lines=[("git push -u", "Отправить и связать."), ("origin feature/login-tests", "Куда и какую ветку.")],
    mistake="Без `-u` — каждый раз придётся указывать `origin ветка`."),

f"{P}-remote-e3": x(
    idea="Ветка связана — `git push` знает, куда отправлять.",
    lines=[("git push", "Новые коммиты — на сервер.")],
    mistake="`git commit` — не отправляет, а только сохраняет локально."),

f"{P}-remote-e4": x(
    idea="`pull` = `fetch` + `merge`.",
    lines=[("git pull", "Скачать и влить.")],
    mistake="`git fetch` — скачает, но не вольёт."),

f"{P}-remote-e5": x(
    idea="`fetch` обновляет `origin/*`, твои ветки не трогает.",
    lines=[("git fetch", "Только скачать.")],
    mistake="`git pull` — сразу вольёт."),

f"{P}-remote-e6": x(
    idea="`git switch имя` сам создаст локальную ветку, связанную с `origin/имя`.",
    lines=[("git switch feature/payment", "Локальная копия ветки коллеги.")],
    mistake="`git switch -c feature/payment` без источника — создаст пустую ветку от текущей."),

f"{P}-remote-e7": x(
    idea="«behind by N» — на сервере N коммитов, которых нет у тебя.",
    lines=[("behind 'origin/main' by 3 commits", "Отставание — 3.")],
    mistake="Путать behind (отстаёшь) и ahead (опережаешь)."),

f"{P}-remote-e8": x(
    idea="`pull --rebase` забирает чужие коммиты и переставляет твои поверх — без коммита слияния.",
    lines=[("git pull --rebase", "Потом можно снова `git push`.")],
    mistake="`git push --force` — затрёшь работу коллег."),

f"{P}-pr-e1": x(
    idea="Перед новой задачей обновляют `main`, чтобы ветвиться от свежей версии.",
    lines=[("git pull", "Свежий `main`.")],
    mistake="Ветвиться от старого `main` — потом конфликты."),

f"{P}-pr-e2": x(
    idea="Создать ветку задачи и перейти на неё.",
    lines=[("git switch -c test/cart-e2e", "Новая ветка от `main`.")],
    mistake="Коммитить прямо в `main`."),

f"{P}-pr-e3": x(
    idea="`&&` выполняет вторую команду, только если первая прошла успешно.",
    lines=[("git add .", "Всё в индекс."), ("git commit -m \"test: add cart e2e\"", "Коммит.")],
    mistake="`;` вместо `&&` — коммит попробует выполниться даже после ошибки `add`."),

f"{P}-pr-e4": x(
    idea="Первая отправка ветки — с `-u`.",
    lines=[("git push -u origin test/cart-e2e", "Ветка на сервере — можно открывать PR.")],
    mistake="`git push` без `-u` — git спросит, куда отправлять."),

f"{P}-pr-e5": x(
    idea="`gh pr create` открывает PR из текущей ветки и спросит заголовок и описание.",
    lines=[("gh pr create", "Pull request с терминала.")],
    mistake="`git pr create` — у git нет такой команды."),

f"{P}-pr-e6": x(
    idea="`gh pr checkout N` скачивает ветку PR и переключается на неё.",
    lines=[("gh pr checkout 42", "Ветка PR №42 локально.")],
    mistake="Искать имя ветки вручную."),

f"{P}-pr-e7": x(
    idea="Новый коммит в ту же ветку сам обновит PR.",
    lines=[
        ("git add .", "Изменения."),
        ("git commit -m \"fix: review comments\"", "Коммит."),
        ("git push", "PR обновился."),
    ],
    mistake="Открывать новый PR на каждую правку."),

f"{P}-pr-e8": x(
    idea="Проверки независимы — каждая добавляет своё замечание.",
    lines=[
        ('if not pr["title"].startswith(("feat:", "fix:", "test:")):', "`startswith` принимает кортеж."),
        ('if pr["branch"] == "main":', "PR из main."),
        ('has_src = any(f.startswith("src/") for f in pr["files"])', "Менялся код."),
        ("if has_src and not has_tests:", "Код без тестов."),
        ('if not pr["tests_passed"]:', "Упавшие тесты."),
    ],
    mistake="`elif` между проверками — найдётся только первое замечание."),

# ===== Модуль 3. Исправление ошибок и продвинутое =====

f"{P}-undo-e1": x(
    idea="`git restore файл` возвращает файл к версии последнего коммита. Изменения пропадут.",
    lines=[("git restore conftest.py", "Откат одного файла.")],
    mistake="`git reset --hard` — откатит все файлы."),

f"{P}-undo-e2": x(
    idea="`--amend` заменяет последний коммит, `--no-edit` оставляет сообщение.",
    lines=[("git commit --amend", "Переделать последний коммит."), ("--no-edit", "Сообщение прежнее.")],
    mistake="Делать новый коммит «забыл файл» — лишний шум в истории."),

f"{P}-undo-e3": x(
    idea="`--amend -m` меняет сообщение последнего коммита.",
    lines=[("git commit --amend -m", "Новое сообщение."), ('"test: add login cases"', "Текст.")],
    mistake="Амендить уже отправленный коммит — придётся `push --force`."),

f"{P}-undo-e4": x(
    idea="`reset HEAD~1` переносит ветку на коммит назад; изменения остаются в файлах.",
    lines=[("git reset HEAD~1", "`HEAD~1` — предыдущий коммит.")],
    mistake="`--hard` — изменения пропадут."),

f"{P}-undo-e5": x(
    idea="`revert` создаёт новый коммит-«антипод» — история не переписывается, это безопасно для общей ветки.",
    lines=[("git revert a1b2c3d", "Отменяющий коммит.")],
    mistake="`reset` на отправленной ветке — сломает историю коллегам."),

f"{P}-undo-e6": x(
    idea="`--hard` выбрасывает и коммит, и изменения в файлах.",
    lines=[("git reset --hard HEAD~1", "Безвозвратно (почти — есть reflog).")],
    mistake="Делать это с отправленным коммитом."),

f"{P}-undo-e7": x(
    idea="`reflog` хранит все перемещения HEAD — даже «потерянные» коммиты.",
    lines=[("git reflog", "Найти хеш и вернуться к нему.")],
    mistake="`git log` — потерянного коммита там уже нет."),

f"{P}-undo-e8": x(
    idea="`clean -f` удаляет неотслеживаемые файлы, `-d` — и папки.",
    lines=[("git clean -fd", "Мусор после прогона.")],
    mistake="Запускать без проверки — `git clean -n` сначала покажет, что удалится."),

f"{P}-stash-e1": x(
    idea="`stash` прячет незакоммиченные изменения, рабочая папка становится чистой.",
    lines=[("git stash", "Отложить работу.")],
    mistake="Коммитить недоделанное, чтобы переключить ветку."),

f"{P}-stash-e2": x(
    idea="`pop` — применить последний stash и удалить его из списка.",
    lines=[("git stash pop", "Вернуть отложенное.")],
    mistake="`apply` — применит, но оставит в списке."),

f"{P}-stash-e3": x(
    idea="`stash list` — все отложенные наборы, свежий — `stash@{0}`.",
    lines=[("git stash list", "Список.")],
    mistake="`git stash show` — содержимое одного набора."),

f"{P}-stash-e4": x(
    idea="`-m` — описание, чтобы не запутаться в нескольких stash.",
    lines=[("git stash push -m", "С сообщением."), ('"wip cart tests"', "Описание.")],
    mistake="Без описания — в списке будет только название ветки."),

f"{P}-stash-e5": x(
    idea="По умолчанию stash не берёт новые файлы; `-u` — включить неотслеживаемые.",
    lines=[("git stash -u", "И новые файлы тоже.")],
    mistake="Обычный `stash` — новые файлы останутся в папке."),

f"{P}-stash-e6": x(
    idea="`apply` применяет и оставляет stash в списке; номер — в фигурных скобках.",
    lines=[("git stash apply", "Не удалять."), ("stash@{1}", "Второй по счёту.")],
    mistake="`stash@{2}` — нумерация с нуля."),

f"{P}-stash-e7": x(
    idea="`stash@{0}` — самый свежий.",
    lines=[("stash@{0}: On test/login: wip login", "Нулевой — последний.")],
    mistake="Ответить wip cart — он старше."),

f"{P}-stash-e8": x(
    idea="`stash clear` удаляет все наборы.",
    lines=[("git stash clear", "Список пуст.")],
    mistake="`git stash drop` — удаляет только один."),

f"{P}-rebase-e1": x(
    idea="`rebase main` переставляет твои коммиты поверх `main` — история получается прямой.",
    lines=[("git rebase main", "Твои коммиты — после свежего `main`.")],
    mistake="Делать rebase, стоя на `main`."),

f"{P}-rebase-e2": x(
    idea="После исправления конфликта и `git add` — продолжить.",
    lines=[("git rebase --continue", "Следующий коммит.")],
    mistake="`git commit` — rebase сам создаёт коммиты."),

f"{P}-rebase-e3": x(
    idea="`--abort` возвращает ветку как было до rebase.",
    lines=[("git rebase --abort", "Отмена.")],
    mistake="`git merge --abort` — это для слияния."),

f"{P}-rebase-e4": x(
    idea="После rebase хеши меняются — нужен принудительный push. `--force-with-lease` не затрёт чужие новые коммиты.",
    lines=[("git push --force-with-lease", "Безопасный force.")],
    mistake="`--force` — затрёт коммиты, которые кто-то успел отправить."),

f"{P}-rebase-e5": x(
    idea="`cherry-pick` копирует один коммит в текущую ветку.",
    lines=[("git cherry-pick 9f8e7d6", "Копия коммита.")],
    mistake="`git merge` — заберёт все коммиты ветки."),

f"{P}-rebase-e6": x(
    idea="`pull --rebase origin main` — забрать свежий `main` с сервера и перенести свои коммиты поверх.",
    lines=[("git pull --rebase", "Без коммита слияния."), ("origin main", "Откуда.")],
    mistake="`git pull` — создаст коммит слияния."),

f"{P}-rebase-e7": x(
    idea="`main..test/cart` — коммиты ветки, которых нет в `main`; они и переносятся.",
    lines=[("git log --oneline main..test/cart", "Два коммита.")],
    mistake="Считать коммиты `main`."),

f"{P}-rebase-e8": x(
    idea="Общий предок пропускаем; твои коммиты — копии с новыми хешами (отмечаем `'`).",
    lines=[("return list(base) + [c + \"'\" for c in branch_commits[1:]]", "База + переписанные коммиты.")],
    mistake="Оставить общий коммит в списке твоих — он появится дважды."),

f"{P}-advanced-e1": x(
    idea="`-a` — аннотированный тег (с автором, датой, сообщением).",
    lines=[("git tag -a v1.2.0", "Тег."), ('-m "Release 1.2.0"', "Сообщение.")],
    mistake="`git tag v1.2.0` — лёгкий тег без сообщения."),

f"{P}-advanced-e2": x(
    idea="Обычный `push` теги не отправляет.",
    lines=[("git push --tags", "Все теги.")],
    mistake="Ждать, что тег уедет с обычным push."),

f"{P}-advanced-e3": x(
    idea="`blame` показывает для каждой строки коммит и автора.",
    lines=[("git blame tests/test_pay.py", "Кто и когда менял строку.")],
    mistake="`git log` — история коммитов, без разбивки по строкам."),

f"{P}-advanced-e4": x(
    idea="`bisect` — двоичный поиск коммита, где сломалось.",
    lines=[("git bisect start", "Начать.")],
    mistake="Проверять коммиты по одному подряд."),

f"{P}-advanced-e5": x(
    idea="Тест падает — коммит «плохой».",
    lines=[("git bisect bad", "Git перейдёт в середину оставшегося.")],
    mistake="`good` — тест падает, значит плохой."),

f"{P}-advanced-e6": x(
    idea="`bisect run команда` — git сам запускает тест: код 0 — хороший, иначе — плохой.",
    lines=[("git bisect run", "Автоматически."), ("pytest tests/test_pay.py", "Проверка на каждом шаге.")],
    mistake="Запускать тесты вручную на каждом шаге."),

f"{P}-advanced-e7": x(
    idea="`-S текст` — коммиты, где этот текст появился или исчез.",
    lines=[('git log -S "TIMEOUT"', "Поиск по содержимому изменений.")],
    mistake="`git log --grep TIMEOUT` — ищет в сообщениях коммитов."),

f"{P}-advanced-e8": x(
    idea="Держим границы «хороший — плохой» и делим отрезок пополам, пока они не станут соседями.",
    lines=[
        ("lo, hi = 0, len(commits) - 1      # lo — хороший, hi — плохой", "Начальные границы."),
        ("mid = (lo + hi) // 2", "Середина."),
        ("if is_bad(commits[mid]):\n            hi = mid", "Сломалось раньше."),
        ("else:\n            lo = mid", "Сломалось позже."),
        ("return commits[hi]", "Первый плохой."),
    ],
    mistake="Проверять коммиты по очереди — n вызовов вместо log2(n)."),
}
