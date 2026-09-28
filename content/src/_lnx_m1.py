"""Тема «Linux и терминал», модуль 1 «Навигация и файлы» — задания. Теория — в _lnx_t1.py."""
from ._lib import cmd, cod, lesson, module, t

P = "lnx"

m1 = module(f"{P}-m1", "Навигация и файлы", "📂", "Терминал и пути, ls, создание, копирование и удаление, просмотр файлов",

lesson(f"{P}-terminal", "Терминал, пути и cd",
    cmd(f"{P}-terminal-e1", "Какой командой узнать, в какой папке ты сейчас находишься?",
        ["pwd"], hint="print working directory"),
    cmd(f"{P}-terminal-e2", "Перейди в папку `projects`, которая лежит в текущей папке.",
        ["cd projects", "cd ./projects", "cd projects/", "cd ./projects/"]),
    cmd(f"{P}-terminal-e3", "Поднимись на одну папку вверх (в родительскую).",
        ["cd ..", "cd ../"]),
    cmd(f"{P}-terminal-e4", "Перейди в свою домашнюю папку. Подойдёт любой из стандартных способов.",
        ["cd ~", "cd", "cd ~/", "cd $HOME"]),
    cmd(f"{P}-terminal-e5", t("""
        Что выведет последняя команда?
        """),
        ["/home/anna/projects/api"],
        context="""
        $ pwd
        /home/anna/projects
        $ cd api
        $ pwd
        """, hint="cd api — относительный путь от текущей папки."),
    cmd(f"{P}-terminal-e6", t("""
        Что выведет последняя команда?
        """),
        ["/home/anna"],
        context="""
        $ pwd
        /home/anna/projects/api/tests
        $ cd ../..
        $ pwd
        """),
    cmd(f"{P}-terminal-e7", "Перейди в папку `/var/log` по **абсолютному** пути, откуда бы ты ни находился.",
        ["cd /var/log", "cd /var/log/"]),
    cmd(f"{P}-terminal-e8", t("""
        Ты был в `/home/anna/projects/api`, потом выполнил `cd /tmp`. Какой командой вернуться в **предыдущую** папку одним коротким действием?
        """),
        ["cd -"], hint="У cd есть специальный аргумент «минус».", xp=15),
),

lesson(f"{P}-ls", "Содержимое папки: ls",
    cmd(f"{P}-ls-e1", "Покажи содержимое текущей папки.",
        ["ls", "ls .", "ls ./"]),
    cmd(f"{P}-ls-e2", "Покажи содержимое папки **подробно**: права, владелец, размер, дата.",
        ["ls -l", "ll", "ls -l ."]),
    cmd(f"{P}-ls-e3", "Покажи **все** файлы, включая скрытые (те, что начинаются с точки), в подробном виде.",
        ["ls -la", "ls -al", "ls -l -a", "ls -a -l", "ll -a"]),
    cmd(f"{P}-ls-e4", "Покажи подробный список с размерами в понятном виде (К, М, Г вместо байтов).",
        ["ls -lh", "ls -hl", "ls -l -h", "ls -h -l", "ls -lah", "ls -alh", "ls -lha", "ls -hla"]),
    cmd(f"{P}-ls-e5", "Сколько **файлов** (не папок) в выводе ниже? Введи число.",
        ["2"],
        context="""
        $ ls -l
        total 12
        drwxr-xr-x 2 anna anna 4096 Mar  8 10:00 reports
        -rw-r--r-- 1 anna anna  220 Mar  8 10:01 README.md
        drwxr-xr-x 3 anna anna 4096 Mar  8 10:02 tests
        -rw-r--r-- 1 anna anna   57 Mar  8 10:03 requirements.txt
        """, hint="Первый символ строки: d — папка, - — обычный файл."),
    cmd(f"{P}-ls-e6", "Какой размер файла `requirements.txt` в байтах?",
        ["57"],
        context="""
        $ ls -l
        -rw-r--r-- 1 anna anna  220 Mar  8 10:01 README.md
        -rw-r--r-- 1 anna anna   57 Mar  8 10:03 requirements.txt
        """),
    cmd(f"{P}-ls-e7", "Покажи файлы, отсортированные по времени изменения — самые новые сверху, в подробном виде.",
        ["ls -lt", "ls -tl", "ls -l -t", "ls -t -l", "ls -lat", "ls -alt", "ls -lta", "ls -tla"]),
    cod(f"{P}-ls-e8", t("""
        Напиши функцию `parse_ls(output)` — разобрать вывод `ls -l` (без строки `total`) и вернуть словарь «имя → `"dir"` или `"file"`». Тип определяй по первому символу строки: `d` — папка, иначе файл. Имя — последнее слово строки.
        """),
        """
        def parse_ls(output):
            pass
        """,
        """
        OUT = '''drwxr-xr-x 2 anna anna 4096 Mar  8 10:00 reports
        -rw-r--r-- 1 anna anna  220 Mar  8 10:01 README.md
        drwxr-xr-x 3 anna anna 4096 Mar  8 10:02 tests'''

        def test_values():
            assert parse_ls(OUT) == {"reports": "dir", "README.md": "file", "tests": "dir"}, parse_ls(OUT)
            assert parse_ls("") == {}, "Пустой вывод"
        """,
        """
        def parse_ls(output):
            result = {}
            for line in output.splitlines():
                line = line.strip()
                if not line:
                    continue
                name = line.split()[-1]
                result[name] = "dir" if line.startswith("d") else "file"
            return result
        """, xp=20),
),

lesson(f"{P}-files", "Создать, скопировать, переместить, удалить",
    cmd(f"{P}-files-e1", "Создай папку `reports`.",
        ["mkdir reports"]),
    cmd(f"{P}-files-e2", "Создай сразу вложенные папки `reports/2024/march` одной командой (промежуточные папки ещё не существуют).",
        ["mkdir -p reports/2024/march", "mkdir -p ./reports/2024/march"], hint="Нужен флаг, который создаёт родителей."),
    cmd(f"{P}-files-e3", "Создай пустой файл `conftest.py`.",
        ["touch conftest.py"]),
    cmd(f"{P}-files-e4", "Скопируй файл `config.yaml` в `config.backup.yaml`.",
        ["cp config.yaml config.backup.yaml"]),
    cmd(f"{P}-files-e5", "Скопируй **папку** `tests` целиком в `tests_old`.",
        ["cp -r tests tests_old", "cp -R tests tests_old", "cp -a tests tests_old"], hint="Для папок нужен рекурсивный флаг."),
    cmd(f"{P}-files-e6", "Переименуй файл `test_old.py` в `test_login.py`.",
        ["mv test_old.py test_login.py"]),
    cmd(f"{P}-files-e7", "Удали папку `tmp_reports` вместе со всем содержимым.",
        ["rm -r tmp_reports", "rm -rf tmp_reports", "rm -fr tmp_reports", "rm -R tmp_reports"],
        hint="rm -rf удаляет без вопросов и без корзины — всегда проверяй путь."),
    cmd(f"{P}-files-e8", t("""
        Перемести все файлы с расширением `.log` из текущей папки в папку `logs` одной командой.
        """),
        ["mv *.log logs", "mv *.log logs/", "mv ./*.log logs/", "mv ./*.log logs"], hint="* — любые символы в имени.", xp=15),
),

lesson(f"{P}-view", "Просмотр файлов: cat, less, head, tail",
    cmd(f"{P}-view-e1", "Выведи всё содержимое файла `requirements.txt` в терминал.",
        ["cat requirements.txt"]),
    cmd(f"{P}-view-e2", "Покажи первые 5 строк файла `app.log`.",
        ["head -n 5 app.log", "head -5 app.log", "head -n5 app.log"]),
    cmd(f"{P}-view-e3", "Покажи последние 20 строк файла `app.log`.",
        ["tail -n 20 app.log", "tail -20 app.log", "tail -n20 app.log"]),
    cmd(f"{P}-view-e4", "Следи за файлом `app.log` в реальном времени: новые строки должны появляться по мере записи.",
        ["tail -f app.log", "tail -F app.log", "tail -n 20 -f app.log", "tail -f -n 20 app.log"],
        hint="Выход — Ctrl+C."),
    cmd(f"{P}-view-e5", "Посчитай, сколько строк в файле `users.csv`.",
        ["wc -l users.csv", "wc -l < users.csv", "cat users.csv | wc -l"]),
    cmd(f"{P}-view-e6", "Что выведет команда? Введи только число.",
        ["3"],
        context="""
        $ cat data.txt
        один
        два
        три
        $ wc -l < data.txt
        """),
    cmd(f"{P}-view-e7", "Открой большой файл `server.log` для постраничного просмотра (с прокруткой и поиском по `/`).",
        ["less server.log", "less +G server.log", "more server.log"]),
    cmd(f"{P}-view-e8", "Что выведет последняя команда? Строки вывода введи **через пробел**.",
        ["b c"],
        context="""
        $ cat letters.txt
        a
        b
        c
        $ tail -n 2 letters.txt
        """, hint="tail -n 2 — две последние строки.")),
)
