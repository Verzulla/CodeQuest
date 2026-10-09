"""Тема «Python-проект: окружение, зависимости, качество» — ручные разборы решений.

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "prj"

EXPLAIN = {

# ===== Модуль 1. Окружение и pip =====

f"{P}-venv-e1": x(
    idea="Виртуальное окружение — отдельная копия Python со своими пакетами для одного проекта.",
    lines=[("python -m venv", "Стандартный модуль `venv`."), (".venv", "Папка окружения.")],
    mistake="Ставить пакеты в системный Python — проекты начнут мешать друг другу."),

f"{P}-venv-e2": x(
    idea="Активация подменяет `python` и `pip` на версии из окружения в этом терминале.",
    lines=[("source .venv/bin/activate", "Скрипт активации для bash/zsh.")],
    mistake="Запустить `.venv/bin/activate` без `source` — он выполнится в отдельном процессе и ничего не изменит."),

f"{P}-venv-e3": x(
    idea="В Windows скрипты лежат в `Scripts`, а не в `bin`.",
    lines=[(".venv\\Scripts\\Activate.ps1", "Активация для PowerShell.")],
    mistake="`source .venv/bin/activate` — в Windows такого пути нет."),

f"{P}-venv-e4": x(
    idea="`deactivate` возвращает системный Python.",
    lines=[("deactivate", "Команду добавила активация.")],
    mistake="Закрывать терминал ради этого."),

f"{P}-venv-e5": x(
    idea="`which python` показывает, какой файл запустится.",
    lines=[("which python", "Путь внутри `.venv` — окружение активно.")],
    mistake="`python --version` — версия не говорит, из какого окружения Python."),

f"{P}-venv-e6": x(
    idea="Признаки активного окружения: `(.venv)` в приглашении и путь к Python внутри `.venv`.",
    lines=[("(.venv) anna@laptop:~/api-tests$ which python", "Префикс `(.venv)`."), ("/home/anna/api-tests/.venv/bin/python", "Python из окружения.")],
    mistake="Смотреть только на версию Python."),

f"{P}-venv-e7": x(
    idea="Python окружения можно вызвать по пути — активация не нужна.",
    lines=[(".venv/bin/python -m pytest", "pytest этого окружения.")],
    mistake="Просто `pytest` — запустится тот, что найдётся в PATH."),

f"{P}-venv-e8": x(
    idea="В окружении `sys.prefix` указывает на `.venv`, а `sys.base_prefix` — на исходный Python.",
    lines=[
        ("return sys.prefix != sys.base_prefix", "Отличаются — мы в venv."),
        ('return f"venv: {prefix}"', "Окружение."),
        ('return f"system: {base_prefix}"', "Системный."),
    ],
    mistake="Проверять переменную `VIRTUAL_ENV` — её нет, если Python запущен по пути без активации."),

f"{P}-pip-e1": x(
    idea="`pip install` ставит пакет в текущее окружение.",
    lines=[("pip install requests", "Последняя версия.")],
    mistake="Ставить без активного окружения — попадёт в системный Python."),

f"{P}-pip-e2": x(
    idea="`==` — точная версия.",
    lines=[("pip install pytest==8.3.2", "Ровно эта версия.")],
    mistake="`pytest=8.3.2` с одним `=` — ошибка синтаксиса."),

f"{P}-pip-e3": x(
    idea="`-U` (upgrade) обновляет уже установленный пакет.",
    lines=[("pip install -U requests", "До последней версии.")],
    mistake="`pip install requests` — пакет уже есть, ничего не изменится."),

f"{P}-pip-e4": x(
    idea="`-y` отвечает «да» на подтверждение.",
    lines=[("pip uninstall -y selenium", "Без вопроса.")],
    mistake="`pip remove` — такой команды нет."),

f"{P}-pip-e5": x(
    idea="`pip list` — таблица пакетов и версий.",
    lines=[("pip list", "Всё, что установлено.")],
    mistake="`pip show` — только про один пакет."),

f"{P}-pip-e6": x(
    idea="`pip show` — подробности одного пакета.",
    lines=[("pip show pytest", "Версия, зависимости, путь.")],
    mistake="`pip list pytest` — не показывает подробности."),

f"{P}-pip-e7": x(
    idea="Второй столбец — версия.",
    lines=[("requests   2.32.3", "Строка пакета.")],
    mistake="Взять версию urllib3 из соседней строки."),

f"{P}-pip-e8": x(
    idea="Версию сравнивают как кортеж чисел: `(2, 10) > (2, 9)`, а строки — посимвольно.",
    lines=[
        ('return tuple(int(part) for part in v.split("."))', "Строка → кортеж чисел."),
        ("return parse_version(a) > parse_version(b)", "Кортежи сравниваются по элементам."),
    ],
    mistake="`a > b` для строк — `\"2.9\" > \"2.10\"`."),

f"{P}-requirements-e1": x(
    idea="`-r файл` — установить всё из списка зависимостей.",
    lines=[("pip install -r requirements.txt", "Весь список.")],
    mistake="`pip install requirements.txt` — попытка найти пакет с таким именем."),

f"{P}-requirements-e2": x(
    idea="`pip freeze` печатает пакеты в формате `имя==версия`; `>` сохраняет вывод в файл.",
    lines=[("pip freeze", "Точные версии."), ("> requirements.txt", "В файл.")],
    mistake="`pip list > requirements.txt` — таблица, а не формат requirements."),

f"{P}-requirements-e3": x(
    idea="`>=` — «эта версия или новее».",
    lines=[("pytest>=8.0", "Не ниже 8.0.")],
    mistake="`pytest==8.0` — ровно 8.0."),

f"{P}-requirements-e4": x(
    idea="Строка `-r файл` внутри requirements подключает другой файл.",
    lines=[("-r requirements.txt", "Всё основное + dev-пакеты ниже.")],
    mistake="Копировать список — версии разъедутся."),

f"{P}-requirements-e5": x(
    idea="Комментарии и пустые строки не считаются.",
    lines=[("pytest==8.3.2", "1."), ("requests>=2.31", "2."), ("allure-pytest~=2.13", "3.")],
    mistake="Посчитать строку `# тесты`."),

f"{P}-requirements-e6": x(
    idea="`~=2.13.0` — «совместимая»: `>=2.13.0, <2.14`.",
    lines=[("allure-pytest~=2.13.0", "Любые 2.13.x.")],
    mistake="`~=2.13` — разрешит и 2.14, 2.15 (меняется последняя указанная часть)."),

f"{P}-requirements-e7": x(
    idea="Флаг `-r` можно повторить несколько раз.",
    lines=[("pip install -r requirements.txt -r requirements-dev.txt", "Оба файла сразу.")],
    mistake="Два файла через один `-r` — второй примется за имя пакета."),

f"{P}-requirements-e8": x(
    idea="Отрезаем комментарий, пропускаем пустые и строки с `-`, имя — до первого символа версии.",
    lines=[
        ('line = line.split("#", 1)[0].strip()', "Без комментария."),
        ('if not line or line.startswith("-"):\n            continue', "Пустые и `-r`."),
        ('m = re.match(r"([A-Za-z0-9_.\\-]+)\\s*(.*)", line)', "Имя и остаток."),
        ('result[m.group(1).lower()] = m.group(2).replace(" ", "")', "Нижний регистр, без пробелов."),
    ],
    mistake="Делить по `==` — не сработает для `>=` и `~=`."),

f"{P}-pyproject-e1": x(
    idea="`-e` (editable) — пакет ссылается на твою папку, правки видны сразу.",
    lines=[("pip install -e .", "`.` — текущий проект.")],
    mistake="Без `-e` — после каждой правки придётся переустанавливать."),

f"{P}-pyproject-e2": x(
    idea="`.[dev]` — проект плюс группа дополнительных зависимостей; кавычки защищают `[]` от оболочки.",
    lines=[("pip install -e '.[dev]'", "Проект и dev-пакеты.")],
    mistake="Без кавычек в zsh — `no matches found`."),

f"{P}-pyproject-e3": x(
    idea="`requires-python` — требуемая версия интерпретатора.",
    lines=[('requires-python = ">=3.11"', "Не ниже 3.11.")],
    mistake="Взять версию проекта 0.1.0."),

f"{P}-pyproject-e4": x(
    idea="Обязательные — в `dependencies`, дополнительные — в `optional-dependencies`.",
    lines=[('dependencies = ["requests>=2.31", "pydantic>=2"]', "Две.")],
    mistake="Прибавить pytest и ruff — они необязательные."),

f"{P}-pyproject-e5": x(
    idea="Настройки инструментов живут в `[tool.<имя>]`; у pytest — `ini_options`.",
    lines=[("[tool.pytest.ini_options]", "Секция pytest.")],
    mistake="`[pytest]` — так в `pytest.ini`, а не в pyproject."),

f"{P}-pyproject-e6": x(
    idea="Секция инструмента — `[tool.имя]`.",
    lines=[("[tool.ruff]", "Настройки ruff.")],
    mistake="`[ruff]` без `tool.`."),

f"{P}-pyproject-e7": x(
    idea="`tomllib.loads` превращает TOML-строку в словарь.",
    lines=[
        ('data = tomllib.loads(text)["project"]', "Секция `[project]`."),
        ('return data["name"], data["version"], data.get("dependencies", [])', "Зависимостей может не быть."),
    ],
    mistake="`data[\"dependencies\"]` — `KeyError` у проекта без зависимостей."),

f"{P}-pyproject-e8": x(
    idea="Цепочка `.get(..., {})` безопасно спускается по вложенным секциям.",
    lines=[
        ('opts = data.get("tool", {}).get("pytest", {}).get("ini_options", {}).get("addopts", "")', "Нет секции — пустая строка."),
        ("return opts.split()", "Строка → список аргументов."),
    ],
    mistake="`data[\"tool\"][\"pytest\"]` — упадёт, если секции нет."),

# ===== Модуль 2. uv и запуск =====

f"{P}-uv-e1": x(
    idea="`uv init` создаёт `pyproject.toml` и заготовку проекта.",
    lines=[("uv init", "Новый проект в текущей папке.")],
    mistake="`uv venv` — только окружение, без проекта."),

f"{P}-uv-e2": x(
    idea="`uv add` записывает зависимость в `pyproject.toml`, обновляет lock-файл и ставит пакет.",
    lines=[("uv add requests", "Всё одной командой.")],
    mistake="`uv pip install requests` — поставит, но в `pyproject.toml` не запишет."),

f"{P}-uv-e3": x(
    idea="`--dev` — зависимость только для разработки (тесты, линтеры).",
    lines=[("uv add --dev pytest", "В группу dev.")],
    mistake="Добавить pytest в основные зависимости."),

f"{P}-uv-e4": x(
    idea="`uv remove` убирает пакет из `pyproject.toml` и окружения.",
    lines=[("uv remove selenium", "Удалить зависимость.")],
    mistake="`uv uninstall` — такой команды нет."),

f"{P}-uv-e5": x(
    idea="`uv sync` приводит окружение в точное соответствие с `uv.lock`.",
    lines=[("uv sync", "Окружение = lock-файл.")],
    mistake="`uv add` для каждого пакета вручную."),

f"{P}-uv-e6": x(
    idea="`uv run` запускает команду в окружении проекта (и сначала синхронизирует его).",
    lines=[("uv run pytest", "Без активации.")],
    mistake="`uv pytest` — нет такой подкоманды."),

f"{P}-uv-e7": x(
    idea="Ограничение версии пишут прямо в имени; кавычки — чтобы `>` не стал перенаправлением.",
    lines=[("uv add 'pydantic>=2'", "Версия 2 и выше.")],
    mistake="Без кавычек — оболочка может создать файл `=2`."),

f"{P}-uv-e8": x(
    idea="Собираем команды по порядку; `uv add` добавляем, только если есть что добавлять.",
    lines=[
        ('commands = ["uv init"]', "Всегда первым."),
        ('if deps:\n        commands.append("uv add " + " ".join(deps))', "Одна команда на все пакеты."),
        ('if dev_deps:\n        commands.append("uv add --dev " + " ".join(dev_deps))', "Dev-пакеты."),
        ('commands.append("uv sync")', "В конце."),
    ],
    mistake="Команда `uv add` с пустым списком — ошибка."),

f"{P}-uvlock-e1": x(
    idea="`uv lock` пересчитывает `uv.lock` по `pyproject.toml`, не трогая окружение.",
    lines=[("uv lock", "Только lock-файл.")],
    mistake="`uv sync` — ещё и установит."),

f"{P}-uvlock-e2": x(
    idea="`--upgrade-package` обновляет в lock-файле один пакет, остальные остаются.",
    lines=[("uv lock --upgrade-package requests", "Только requests.")],
    mistake="`uv lock --upgrade` — обновит всё."),

f"{P}-uvlock-e3": x(
    idea="uv сам скачивает и ставит интерпретаторы Python.",
    lines=[("uv python install 3.12", "Python 3.12.")],
    mistake="`uv add python` — Python не пакет проекта."),

f"{P}-uvlock-e4": x(
    idea="`pin` записывает версию в `.python-version` — проект будет использовать её.",
    lines=[("uv python pin 3.12", "Закрепить.")],
    mistake="`install` — установит, но не закрепит."),

f"{P}-uvlock-e5": x(
    idea="`uv venv` — быстрый аналог `python -m venv`, по умолчанию папка `.venv`.",
    lines=[("uv venv", "Окружение `.venv`.")],
    mistake="`uv init` — создаст проект."),

f"{P}-uvlock-e6": x(
    idea="`uv pip` — совместимый с pip режим для старых проектов.",
    lines=[("uv pip install -r requirements.txt", "Как pip, только быстрее.")],
    mistake="`uv add -r requirements.txt` — запишет всё в pyproject."),

f"{P}-uvlock-e7": x(
    idea="Lock-файл фиксирует точные версии: у всех и в CI одинаковые пакеты — тесты воспроизводимы.",
    lines=[("да", "Коммитить.")],
    mistake="Игнорировать lock — «у меня проходит, а в CI нет»."),

f"{P}-uvlock-e8": x(
    idea="`--locked` падает, если lock-файл устарел относительно `pyproject.toml`.",
    lines=[("uv sync --locked", "Проверка в CI.")],
    mistake="`uv sync` — тихо обновит lock прямо в CI."),

f"{P}-uvtools-e1": x(
    idea="`uvx` запускает инструмент во временном окружении, не добавляя в проект.",
    lines=[("uvx ruff check .", "Разовый запуск.")],
    mistake="`uv add ruff` ради одной проверки."),

f"{P}-uvtools-e2": x(
    idea="`uv tool install` ставит утилиту глобально, в отдельное окружение.",
    lines=[("uv tool install ruff", "Команда `ruff` везде.")],
    mistake="`pip install ruff` в системный Python."),

f"{P}-uvtools-e3": x(
    idea="`uv tool list` — установленные инструменты.",
    lines=[("uv tool list", "Список.")],
    mistake="`uv pip list` — пакеты окружения."),

f"{P}-uvtools-e4": x(
    idea="`-n 4` — флаг pytest-xdist: число параллельных процессов.",
    lines=[("uv run pytest", "pytest проекта."), ("-n 4", "Четыре процесса.")],
    mistake="`uv run -n 4 pytest` — флаг попадёт к uv."),

f"{P}-uvtools-e5": x(
    idea="`uv run файл.py` запускает скрипт в окружении проекта.",
    lines=[("uv run scripts/seed_data.py", "С пакетами проекта.")],
    mistake="`python scripts/seed_data.py` — без окружения пакетов может не быть."),

f"{P}-uvtools-e6": x(
    idea="`uv tree` — какие пакеты от каких зависят.",
    lines=[("uv tree", "Дерево зависимостей.")],
    mistake="`uv list` — нет такой команды."),

f"{P}-uvtools-e7": x(
    idea="Скрипт скачивается `curl` и сразу выполняется оболочкой через `|`.",
    lines=[("curl -LsSf https://astral.sh/uv/install.sh", "Скачать установщик."), ("| sh", "Выполнить.")],
    mistake="`pip install uv` — тоже работает, но просили официальный скрипт."),

f"{P}-uvtools-e8": x(
    idea="`--with` добавляет пакет только на этот запуск.",
    lines=[("uv run --with requests check.py", "requests — временно.")],
    mistake="`uv add requests` — останется в проекте."),

f"{P}-run-e1": x(
    idea="Аргументы пишут после имени скрипта.",
    lines=[("python seed.py", "Скрипт."), ("--users 10", "Аргументы.")],
    mistake="`python --users 10 seed.py` — аргументы достанутся Python."),

f"{P}-run-e2": x(
    idea="`python -m pytest` запускает pytest именно этого интерпретатора.",
    lines=[("python -m pytest", "Модуль как программа.")],
    mistake="`pytest` — может найтись из другого окружения."),

f"{P}-run-e3": x(
    idea="`-c` выполняет код из строки.",
    lines=[("python -c 'import sys; print(sys.version)'", "Однострочник.")],
    mistake="Двойные кавычки внутри двойных — оболочка разорвёт строку."),

f"{P}-run-e4": x(
    idea="`sys.argv[0]` — имя скрипта, дальше аргументы строками.",
    lines=[("python seed.py --users 10", "Три элемента.")],
    mistake="Ожидать `10` числом — все аргументы строки."),

f"{P}-run-e5": x(
    idea="`argparse` разбирает аргументы, сам приводит типы и даёт значения по умолчанию.",
    lines=[
        ('parser.add_argument("--env", default="dev")', "Строка."),
        ('parser.add_argument("--workers", type=int, default=1)', "Число."),
        ('parser.add_argument("--headless", action="store_true")', "Флаг: есть — True."),
        ("return parser.parse_args(argv)", "Список аргументов — для тестов."),
    ],
    mistake="`parse_args()` без `argv` — возьмёт аргументы самого pytest."),

f"{P}-run-e6": x(
    idea="Код выхода: 0 — успех, 2 — неверное использование.",
    lines=[
        ('if not argv:\n        print("usage: check.py FILE...")\n        return 2', "Нет аргументов."),
        ('print("проверяю: " + ", ".join(argv))', "Список через запятую."),
        ("return 0", "Успех."),
    ],
    mistake="Вернуть 1 при отсутствии аргументов — просили 2."),

f"{P}-run-e7": x(
    idea="0 — успех, любое другое число — ошибка. На этом построен CI.",
    lines=[("0", "Успешно.")],
    mistake="Думать, что 1 — «да, успешно»."),

f"{P}-run-e8": x(
    idea="`$?` — код выхода последней команды.",
    lines=[("echo $?", "0 или код ошибки.")],
    mistake="`echo $!` — PID фонового процесса."),

# ===== Модуль 3. Качество кода =====

f"{P}-lint-e1": x(
    idea="`ruff check` ищет ошибки и подозрительный код.",
    lines=[("ruff check", "Весь проект.")],
    mistake="`ruff format` — это форматирование, а не проверка."),

f"{P}-lint-e2": x(
    idea="`--fix` исправляет то, что ruff считает безопасным.",
    lines=[("ruff check --fix", "Автоисправление.")],
    mistake="Ждать, что `--fix` исправит всё — часть ошибок нужно править руками."),

f"{P}-lint-e3": x(
    idea="Путь после `check` ограничивает проверку.",
    lines=[("ruff check tests", "Только тесты.")],
    mistake="`ruff tests` — без `check` нет команды."),

f"{P}-lint-e4": x(
    idea="Формат: `файл:строка:столбец: КОД сообщение`.",
    lines=[("F401 [*] `os` imported but unused", "Неиспользуемый импорт.")],
    mistake="E501 — это длинная строка."),

f"{P}-lint-e5": x(
    idea="Первое число после имени файла — строка, второе — столбец.",
    lines=[("tests/test_api.py:9:89: E501", "Строка 9, столбец 89.")],
    mistake="Ответить 89 — это столбец."),

f"{P}-lint-e6": x(
    idea="`# noqa: КОД` отключает одну проверку на одной строке.",
    lines=[("# noqa: E501", "В конце строки.")],
    mistake="`# noqa` без кода — отключит вообще все проверки строки."),

f"{P}-lint-e7": x(
    idea="`ruff rule КОД` — описание и примеры правила.",
    lines=[("ruff rule F401", "Справка по правилу.")],
    mistake="Гуглить каждый код."),

f"{P}-lint-e8": x(
    idea="`ast` разбирает код в дерево: собираем импортированные имена и имена, которые используются.",
    lines=[
        ("tree = ast.parse(source)", "Дерево кода."),
        ("if isinstance(node, (ast.Import, ast.ImportFrom)):", "Узлы импорта."),
        ('imported.add((alias.asname or alias.name).split(".")[0])', "`as`-имя или первая часть имени."),
        ("used = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}", "Использованные имена."),
        ("return sorted(imported - used)", "Разность множеств."),
    ],
    mistake="Искать имя в тексте поиском подстроки — найдётся в строках и комментариях."),

f"{P}-format-e1": x(
    idea="`ruff format` переписывает файлы в едином стиле.",
    lines=[("ruff format", "Форматирование проекта.")],
    mistake="`ruff check` — не форматирует."),

f"{P}-format-e2": x(
    idea="`--check` ничего не меняет и возвращает 1, если есть что форматировать.",
    lines=[("ruff format --check", "Проверка для CI.")],
    mistake="`ruff format` в CI — исправит файлы и пройдёт, не сообщив о проблеме."),

f"{P}-format-e3": x(
    idea="`--diff` показывает изменения, не применяя их.",
    lines=[("ruff format --diff", "Как будет.")],
    mistake="`--check` — только список файлов."),

f"{P}-format-e4": x(
    idea="Путь к файлу ограничивает форматирование.",
    lines=[("ruff format tests/test_cart.py", "Только один файл.")],
    mistake="Форматировать весь проект ради одного файла."),

f"{P}-format-e5": x(
    idea="Итоговая строка — сколько файлов будет переформатировано.",
    lines=[("2 files would be reformatted", "Два.")],
    mistake="Ответить 14 — они уже в порядке."),

f"{P}-format-e6": x(
    idea="Сначала исправить линтер, потом форматировать: `--fix` может изменить код.",
    lines=[("ruff check --fix", "Исправления."), ("&& ruff format", "Потом форматирование.")],
    mistake="Обратный порядок — после `--fix` формат может снова сбиться."),

f"{P}-format-e7": x(
    idea="Ненулевой код выхода — сигнал CI, что проверка не прошла.",
    lines=[("1", "Есть что форматировать.")],
    mistake="Ответить 0 — тогда CI ничего бы не заметил."),

f"{P}-format-e8": x(
    idea="`re.sub` с функцией: для каждой строки в одинарных кавычках решаем, менять ли.",
    lines=[
        ("inner = m.group(1)", "Текст внутри кавычек."),
        ("return m.group(0) if '\"' in inner else f'\"{inner}\"'", "Есть двойные — оставляем."),
        ("return re.sub(r\"'([^']*)'\", repl, line)", "Все строки в одинарных кавычках."),
    ],
    mistake="`line.replace(\"'\", '\"')` — сломает строки с двойными кавычками внутри."),

f"{P}-ruffcfg-e1": x(
    idea="`line-length` — максимальная длина строки.",
    lines=[("line-length = 120", "Вместо 88 по умолчанию.")],
    mistake="`max-line-length` — так в flake8, у ruff иначе."),

f"{P}-ruffcfg-e2": x(
    idea="`select` — какие группы правил включить.",
    lines=[('select = ["E", "F", "I"]', "pycodestyle, pyflakes, isort.")],
    mistake="Строка вместо списка — `select = \"EFI\"`."),

f"{P}-ruffcfg-e3": x(
    idea="Префикс `I` — правила isort.",
    lines=[("I", "Сортировка импортов.")],
    mistake="`S` — это правила безопасности."),

f"{P}-ruffcfg-e4": x(
    idea="`ignore` — отключить правила.",
    lines=[('ignore = ["E501"]', "Длина строки не проверяется.")],
    mistake="Удалить `E` из `select` — отключит всю группу."),

f"{P}-ruffcfg-e5": x(
    idea="`per-file-ignores` отключает правила для части файлов. S101 — «использован assert», в тестах это норма.",
    lines=[('"tests/**" = ["S101"]', "Для всех файлов в tests.")],
    mistake="Ответить `tests/**` — это шаблон файлов, а не правило."),

f"{P}-ruffcfg-e6": x(
    idea="`target-version` — минимальная версия Python кода: ruff учтёт доступный синтаксис.",
    lines=[('target-version = "py312"', "Формат `pyXY`.")],
    mistake="`target-version = \"3.12\"` — неверный формат."),

f"{P}-ruffcfg-e7": x(
    idea="Спускаемся по секциям через `.get(..., {})` и подставляем значения по умолчанию.",
    lines=[
        ('ruff = tomllib.loads(text).get("tool", {}).get("ruff", {})', "`[tool.ruff]`."),
        ('lint = ruff.get("lint", {})', "`[tool.ruff.lint]`."),
        ('"line_length": ruff.get("line-length", 88),', "В TOML — через дефис."),
    ],
    mistake="Искать `line_length` с подчёркиванием — в TOML ключ `line-length`."),

f"{P}-ruffcfg-e8": x(
    idea="Нумеруем строки с 1, пропускаем строки с `# noqa: E501` в конце.",
    lines=[
        ("for n, line in enumerate(source.splitlines(), start=1):", "Номер строки."),
        ('if line.rstrip().endswith("# noqa: E501"):\n            continue', "Исключение."),
        ('result.append(f"строка {n}: длина {len(line)} > {limit}")', "Сообщение."),
    ],
    mistake="`>=` вместо `>` — строка ровно по лимиту тоже станет ошибкой."),

f"{P}-precommit-e1": x(
    idea="pre-commit — утилита, которая запускает проверки перед каждым коммитом.",
    lines=[("pip install pre-commit", "Установка.")],
    mistake="Думать, что хуки работают без установки утилиты."),

f"{P}-precommit-e2": x(
    idea="`pre-commit install` прописывает хук в `.git/hooks` — дальше проверки идут сами.",
    lines=[("pre-commit install", "Подключить к git.")],
    mistake="Забыть этот шаг — конфиг есть, а проверки не запускаются."),

f"{P}-precommit-e3": x(
    idea="По умолчанию проверяются только изменённые файлы; `--all-files` — все.",
    lines=[("pre-commit run --all-files", "Весь проект.")],
    mistake="`pre-commit run` — только файлы в индексе."),

f"{P}-precommit-e4": x(
    idea="`autoupdate` обновляет `rev` хуков в конфиге.",
    lines=[("pre-commit autoupdate", "Свежие версии.")],
    mistake="Править версии руками."),

f"{P}-precommit-e5": x(
    idea="Хуки перечислены в `hooks` по `id`.",
    lines=[("- id: ruff", "Первый."), ("- id: ruff-format", "Второй.")],
    mistake="Посчитать `args: [--fix]` хуком."),

f"{P}-precommit-e6": x(
    idea="`--no-verify` пропускает хуки — только в крайнем случае.",
    lines=[('git commit -m "wip"', "Коммит."), ("--no-verify", "Без проверок.")],
    mistake="Делать так постоянно — смысл хуков пропадает."),

f"{P}-precommit-e7": x(
    idea="Имя хука после `run` — запустить только его.",
    lines=[("pre-commit run ruff-format", "Один хук."), ("--all-files", "На всех файлах.")],
    mistake="`pre-commit ruff-format` — без `run`."),

f"{P}-precommit-e8": x(
    idea="Хук «падает», если что-то исправил: файлы изменились — коммит нужно повторить.",
    lines=[
        ("result = dict(files)", "Копия — исходный словарь не меняем."),
        ('if not path.endswith(".py"):\n                continue', "Только `.py`."),
        ("if new != text:\n                result[path] = new\n                changed = True", "Хук изменил файл."),
        ("if changed:\n            failed.append(name)", "Хук отмечен как упавший."),
    ],
    mistake="Применять хуки к исходному `files` — следующий хук не увидит исправлений предыдущего."),
}
