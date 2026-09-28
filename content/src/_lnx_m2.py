"""Тема «Linux и терминал», модуль 2 «Поиск и обработка текста» — задания. Теория — в _lnx_t2.py."""
from ._lib import cmd, cod, lesson, module, t

P = "lnx"

m2 = module(f"{P}-m2", "Поиск и обработка текста", "🔎", "grep, конвейеры и перенаправление, find, sort, uniq, cut и awk",

lesson(f"{P}-grep", "Поиск в тексте: grep",
    cmd(f"{P}-grep-e1", "Найди в файле `app.log` все строки, содержащие слово `ERROR`.",
        ["grep ERROR app.log", "grep 'ERROR' app.log", 'grep "ERROR" app.log']),
    cmd(f"{P}-grep-e2", "Найди в `app.log` строки со словом `error` **без учёта регистра** (ERROR, Error, error).",
        ["grep -i error app.log", "grep -i 'error' app.log", 'grep -i "error" app.log']),
    cmd(f"{P}-grep-e3", "Посчитай, **сколько** строк в `app.log` содержат `ERROR` (одной командой grep).",
        ["grep -c ERROR app.log", "grep -c 'ERROR' app.log", 'grep -c "ERROR" app.log']),
    cmd(f"{P}-grep-e4", "Найди строки с `ERROR` в `app.log` и покажи **номера строк**.",
        ["grep -n ERROR app.log", "grep -n 'ERROR' app.log", 'grep -n "ERROR" app.log']),
    cmd(f"{P}-grep-e5", "Найди во **всех файлах** папки `tests` (и вложенных) строки с `@pytest.fixture`.",
        ["grep -r @pytest.fixture tests", "grep -r '@pytest.fixture' tests", 'grep -r "@pytest.fixture" tests',
         "grep -rn '@pytest.fixture' tests", 'grep -rn "@pytest.fixture" tests', "grep -rn @pytest.fixture tests",
         "grep -r '@pytest.fixture' tests/", 'grep -r "@pytest.fixture" tests/']),
    cmd(f"{P}-grep-e6", "Покажи все строки `app.log`, в которых **нет** слова `DEBUG`.",
        ["grep -v DEBUG app.log", "grep -v 'DEBUG' app.log", 'grep -v "DEBUG" app.log']),
    cmd(f"{P}-grep-e7", "Сколько строк выведет команда? Введи число.",
        ["2"],
        context="""
        $ cat app.log
        INFO старт
        ERROR нет базы
        WARN медленно
        error таймаут
        $ grep -i error app.log
        """),
    cod(f"{P}-grep-e8", t("""
        Напиши на Python аналог `grep -n -i`: функцию `grep(lines, pattern)` — вернуть список строк вида `"номер:строка"` (нумерация с 1) для строк, в которых есть `pattern` без учёта регистра.
        """),
        """
        def grep(lines, pattern):
            pass
        """,
        """
        def test_values():
            lines = ["INFO старт", "ERROR нет базы", "WARN медленно", "error таймаут"]
            assert grep(lines, "error") == ["2:ERROR нет базы", "4:error таймаут"] and grep(lines, "xyz") == [], grep(lines, "error")
        """,
        """
        def grep(lines, pattern):
            p = pattern.lower()
            return [f"{i}:{line}" for i, line in enumerate(lines, start=1) if p in line.lower()]
        """, xp=20),
),

lesson(f"{P}-pipes", "Конвейеры и перенаправление",
    cmd(f"{P}-pipes-e1", "Сохрани список файлов текущей папки (`ls`) в файл `files.txt` (перезаписать, если он есть).",
        ["ls > files.txt", "ls >files.txt"]),
    cmd(f"{P}-pipes-e2", "**Допиши** строку `done` в конец файла `progress.log` командой `echo`.",
        ["echo done >> progress.log", "echo 'done' >> progress.log", 'echo "done" >> progress.log']),
    cmd(f"{P}-pipes-e3", "Выведи строки с `ERROR` из `app.log` и посчитай их количество с помощью конвейера `grep … | wc -l`.",
        ["grep ERROR app.log | wc -l", "grep 'ERROR' app.log | wc -l", 'grep "ERROR" app.log | wc -l', "cat app.log | grep ERROR | wc -l"]),
    cmd(f"{P}-pipes-e4", "Запусти `pytest` и сохрани в файл `pytest.log` **и** обычный вывод, **и** ошибки.",
        ["pytest > pytest.log 2>&1", "pytest &> pytest.log", "pytest >pytest.log 2>&1", "pytest &>pytest.log"],
        hint="2>&1 — отправить поток ошибок туда же, куда обычный вывод."),
    cmd(f"{P}-pipes-e5", "Запусти `./cleanup.sh`, полностью **скрыв** все сообщения об ошибках (выбросить их).",
        ["./cleanup.sh 2> /dev/null", "./cleanup.sh 2>/dev/null"]),
    cmd(f"{P}-pipes-e6", "Покажи последние 50 строк `app.log`, в которых встречается `ERROR`: сначала `grep`, потом `tail` через конвейер.",
        ["grep ERROR app.log | tail -n 50", "grep ERROR app.log | tail -50", "grep 'ERROR' app.log | tail -n 50",
         'grep "ERROR" app.log | tail -n 50', "grep 'ERROR' app.log | tail -50", 'grep "ERROR" app.log | tail -50']),
    cmd(f"{P}-pipes-e7", "Что будет в файле `out.txt` после этих команд? Строки введи через пробел.",
        ["b"],
        context="""
        $ echo a > out.txt
        $ echo b > out.txt
        """, hint="> перезаписывает файл."),
    cmd(f"{P}-pipes-e8", t("""
        Одной строкой: выведи результат `pytest` на экран **и одновременно** сохрани его в файл `run.log` (понадобится команда `tee`).
        """),
        ["pytest | tee run.log", "pytest 2>&1 | tee run.log", "pytest |& tee run.log"], xp=15),
),

lesson(f"{P}-find", "Поиск файлов: find",
    cmd(f"{P}-find-e1", "Найди в текущей папке и во всех вложенных файлы с именем `conftest.py`.",
        ["find . -name conftest.py", "find . -name 'conftest.py'", 'find . -name "conftest.py"', "find . -type f -name conftest.py",
         "find . -type f -name 'conftest.py'", 'find . -type f -name "conftest.py"']),
    cmd(f"{P}-find-e2", "Найди все файлы тестов `test_*.py` в папке `tests`.",
        ["find tests -name 'test_*.py'", 'find tests -name "test_*.py"', "find tests -type f -name 'test_*.py'",
         'find tests -type f -name "test_*.py"', "find tests/ -name 'test_*.py'", 'find tests/ -name "test_*.py"'],
        hint="Шаблон с * бери в кавычки, иначе его раскроет сам shell."),
    cmd(f"{P}-find-e3", "Найди в текущей папке только **папки** (не файлы) с именем `__pycache__`.",
        ["find . -type d -name __pycache__", "find . -type d -name '__pycache__'", 'find . -type d -name "__pycache__"',
         "find . -name __pycache__ -type d", "find . -name '__pycache__' -type d"]),
    cmd(f"{P}-find-e4", "Найди в папке `logs` файлы `.log`, изменённые больше 7 дней назад.",
        ["find logs -name '*.log' -mtime +7", 'find logs -name "*.log" -mtime +7', "find logs -type f -name '*.log' -mtime +7",
         'find logs -type f -name "*.log" -mtime +7', "find logs -mtime +7 -name '*.log'"]),
    cmd(f"{P}-find-e5", "Найди и сразу **удали** все папки `__pycache__` в проекте с помощью `find`.",
        ["find . -type d -name __pycache__ -exec rm -rf {} +", "find . -type d -name '__pycache__' -exec rm -rf {} +",
         'find . -type d -name "__pycache__" -exec rm -rf {} +', "find . -name __pycache__ -type d -exec rm -rf {} +",
         "find . -type d -name __pycache__ -prune -exec rm -rf {} +", "find . -type d -name '__pycache__' -prune -exec rm -rf {} +",
         "find . -type d -name __pycache__ | xargs rm -rf", "find . -type d -name '__pycache__' | xargs rm -rf",
         "re:find \\. -type d -name ['\"]?__pycache__['\"]? -exec rm -rf \\{\\} (\\+|\\\\;)"]),
    cmd(f"{P}-find-e6", "Найди в текущей папке файлы **больше 100 мегабайт**.",
        ["find . -size +100M", "find . -type f -size +100M"]),
    cmd(f"{P}-find-e7", "Сколько файлов найдёт команда? Введи число.",
        ["2"],
        context="""
        $ ls -R
        .:
        tests  README.md
        ./tests:
        test_api.py  test_ui.py  helpers.py
        $ find . -name 'test_*.py'
        """),
    cod(f"{P}-find-e8", t("""
        Напиши на Python упрощённый `find`: функцию `find_files(paths, pattern)` — `paths` — список путей файлов (строки), `pattern` — шаблон имени вроде `"test_*.py"`. Вернуть отсортированный список путей, у которых **имя файла** (последняя часть пути) подходит под шаблон. Используй `fnmatch.fnmatch`.
        """),
        """
        import fnmatch


        def find_files(paths, pattern):
            pass
        """,
        """
        def test_values():
            paths = ["tests/test_api.py", "tests/helpers.py", "test_main.py", "src/app.py", "tests/ui/test_login.py"]
            assert find_files(paths, "test_*.py") == ["test_main.py", "tests/test_api.py", "tests/ui/test_login.py"], find_files(paths, "test_*.py")
            assert find_files(paths, "*.txt") == [], "Нет совпадений"
        """,
        """
        import fnmatch


        def find_files(paths, pattern):
            return sorted(p for p in paths if fnmatch.fnmatch(p.split("/")[-1], pattern))
        """, xp=20),
),

lesson(f"{P}-text", "Обработка текста: sort, uniq, cut, awk",
    cmd(f"{P}-text-e1", "Отсортируй строки файла `names.txt` по алфавиту и выведи на экран.",
        ["sort names.txt", "cat names.txt | sort"]),
    cmd(f"{P}-text-e2", "Выведи **уникальные** строки файла `names.txt` (повторы убрать), отсортированные.",
        ["sort -u names.txt", "sort names.txt | uniq", "cat names.txt | sort | uniq", "cat names.txt | sort -u"],
        hint="uniq убирает только соседние повторы — сначала sort."),
    cmd(f"{P}-text-e3", "Посчитай, сколько раз встречается каждая строка в `levels.txt` (например, INFO — 10, ERROR — 3).",
        ["sort levels.txt | uniq -c", "cat levels.txt | sort | uniq -c"]),
    cmd(f"{P}-text-e4", "Выведи только **второй** столбец CSV-файла `users.csv` (разделитель — запятая) с помощью `cut`.",
        ["cut -d , -f 2 users.csv", "cut -d, -f2 users.csv", "cut -d ',' -f 2 users.csv", "cut -d',' -f2 users.csv",
         'cut -d "," -f 2 users.csv', 'cut -d"," -f2 users.csv', "cut -f 2 -d , users.csv", "cut -f2 -d, users.csv"]),
    cmd(f"{P}-text-e5", "Выведи только **первое слово** каждой строки файла `access.log` с помощью `awk`.",
        ["awk '{print $1}' access.log", 'awk "{print \\$1}" access.log', "awk '{ print $1 }' access.log", "cat access.log | awk '{print $1}'"]),
    cmd(f"{P}-text-e6", "Замени в файле `config.env` все `dev` на `prod` **прямо в файле** с помощью `sed`.",
        ["sed -i 's/dev/prod/g' config.env", 'sed -i "s/dev/prod/g" config.env', "sed -i '' 's/dev/prod/g' config.env",
         "sed -i -e 's/dev/prod/g' config.env"], hint="На macOS после -i нужен пустой аргумент ''."),
    cmd(f"{P}-text-e7", "Что выведет последняя команда? Строки введи через пробел.",
        ["2 ERROR 1 INFO"],
        context="""
        $ cat levels.txt
        ERROR
        INFO
        ERROR
        $ sort levels.txt | uniq -c
        """, hint="Вывод uniq -c: количество, пробел, строка."),
    cod(f"{P}-text-e8", t("""
        Классическая задача тестировщика: «топ ошибок из лога». Напиши на Python аналог конвейера
        `grep ERROR app.log | awk '{print $2}' | sort | uniq -c | sort -rn | head -n N`:
        функция `top_errors(lines, n)` — среди строк, где **первое** слово `ERROR`, взять **второе** слово (код ошибки) и вернуть `n` самых частых как список кортежей `(код, количество)` по убыванию количества (при равенстве — по алфавиту кода).
        """),
        """
        def top_errors(lines, n):
            pass
        """,
        """
        def test_values():
            lines = ["ERROR E42 нет базы", "INFO ok", "ERROR E13 таймаут", "ERROR E42 снова", "ERROR E7 x", "ERROR E13 y", "ERROR E42 z"]
            assert top_errors(lines, 2) == [("E42", 3), ("E13", 2)] and top_errors([], 3) == [], top_errors(lines, 2)
            assert top_errors(["ERROR B", "ERROR A"], 5) == [("A", 1), ("B", 1)], "Равенство — по алфавиту"
        """,
        """
        def top_errors(lines, n):
            counts = {}
            for line in lines:
                words = line.split()
                if len(words) >= 2 and words[0] == "ERROR":
                    counts[words[1]] = counts.get(words[1], 0) + 1
            return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
        """, xp=25),
),
)
