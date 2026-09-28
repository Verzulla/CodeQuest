"""Тема «Linux и терминал», модуль 3 «Система» — задания. Теория — в _lnx_t3.py."""
from ._lib import cmd, cod, lesson, module, t

P = "lnx"

m3 = module(f"{P}-m3", "Система", "⚙️", "Права и sudo, процессы и порты, переменные окружения, сеть, диск и архивы",

lesson(f"{P}-perms", "Права доступа и sudo",
    cmd(f"{P}-perms-e1", "Сделай скрипт `run_tests.sh` исполняемым.",
        ["chmod +x run_tests.sh", "chmod u+x run_tests.sh", "chmod a+x run_tests.sh", "chmod 755 run_tests.sh"]),
    cmd(f"{P}-perms-e2", "Запусти исполняемый скрипт `run_tests.sh` из текущей папки.",
        ["./run_tests.sh", "bash run_tests.sh", "sh run_tests.sh"]),
    cmd(f"{P}-perms-e3", "Кто может **изменять** файл? Варианты: `владелец`, `группа`, `все`. Введи одно слово.",
        ["владелец"],
        context="""
        $ ls -l report.html
        -rw-r--r-- 1 anna qa 5120 Mar  8 10:00 report.html
        """, hint="rw- — владелец, r-- — группа, r-- — остальные."),
    cmd(f"{P}-perms-e4", "Какие права в числовом виде у файла с правами `rwxr-xr-x`? Введи три цифры.",
        ["755"], hint="r = 4, w = 2, x = 1; складывай по тройкам."),
    cmd(f"{P}-perms-e5", "Поставь файлу `secret.env` права «читать и писать может только владелец, остальным — ничего» (числом).",
        ["chmod 600 secret.env", "chmod u=rw,go= secret.env", "chmod u=rw,g=,o= secret.env"]),
    cmd(f"{P}-perms-e6", "Выполни команду `apt update` с правами администратора.",
        ["sudo apt update", "sudo apt-get update"]),
    cmd(f"{P}-perms-e7", "Сделай пользователя `qa` владельцем папки `/opt/reports` (и всего внутри) с правами администратора.",
        ["sudo chown -R qa /opt/reports", "sudo chown -R qa:qa /opt/reports", "sudo chown -R qa: /opt/reports"]),
    cod(f"{P}-perms-e8", t("""
        Напиши функцию `to_octal(perms)` — перевести строку прав вида `"rwxr-xr--"` (9 символов) в число-строку `"754"`. Каждая тройка: `r` = 4, `w` = 2, `x` = 1.
        """),
        """
        def to_octal(perms):
            pass
        """,
        """
        def test_values():
            assert [to_octal(p) for p in ["rwxr-xr--", "rw-r--r--", "rwx------", "---------"]] == ["754", "644", "700", "000"], "Неверный результат"
        """,
        """
        def to_octal(perms):
            values = {"r": 4, "w": 2, "x": 1}
            digits = []
            for i in range(0, 9, 3):
                digits.append(str(sum(values.get(ch, 0) for ch in perms[i:i + 3])))
            return "".join(digits)
        """, xp=20),
),

lesson(f"{P}-proc", "Процессы и порты",
    cmd(f"{P}-proc-e1", "Покажи **все** запущенные процессы всех пользователей в подробном виде.",
        ["ps aux", "ps -ef", "ps -aux"]),
    cmd(f"{P}-proc-e2", "Найди процессы, в названии которых есть `chrome`, через `ps` и `grep`.",
        ["ps aux | grep chrome", "ps -ef | grep chrome", "ps aux | grep -i chrome", "pgrep -a chrome", "pgrep -l chrome"]),
    cmd(f"{P}-proc-e3", "Корректно заверши процесс с PID `4321`.",
        ["kill 4321", "kill -15 4321", "kill -TERM 4321", "kill -SIGTERM 4321"]),
    cmd(f"{P}-proc-e4", "Процесс `4321` завис и не реагирует на обычный `kill`. Заверши его **принудительно**.",
        ["kill -9 4321", "kill -KILL 4321", "kill -SIGKILL 4321"]),
    cmd(f"{P}-proc-e5", "Узнай, какой процесс занял порт `8000` (тест не может поднять сервер: «address already in use»).",
        ["lsof -i :8000", "sudo lsof -i :8000", "lsof -i tcp:8000", "ss -ltnp | grep 8000", "sudo ss -ltnp | grep 8000",
         "netstat -tlnp | grep 8000", "sudo netstat -tlnp | grep 8000", "ss -tlnp | grep 8000", "sudo ss -tlnp | grep 8000"]),
    cmd(f"{P}-proc-e6", "Запусти сервер `python -m http.server 8000` **в фоне**, чтобы терминал остался свободным.",
        ["python -m http.server 8000 &", "python3 -m http.server 8000 &", "nohup python -m http.server 8000 &",
         "nohup python3 -m http.server 8000 &"]),
    cmd(f"{P}-proc-e7", "Каким сочетанием клавиш остановить программу, которая сейчас работает в терминале? Введи его как `Ctrl+X`.",
        ["Ctrl+C", "ctrl+c", "Ctrl-C", "ctrl-c", "^C"]),
    cmd(f"{P}-proc-e8", "Какой PID у процесса `uvicorn`? Введи число.",
        ["2817"],
        context="""
        $ ps aux | grep uvicorn
        anna      2817  1.2  0.8 123456 34567 ?  S  10:00  0:03 python -m uvicorn app:app
        anna      3001  0.0  0.0   6432   736 pts/0 S+ 10:05  0:00 grep uvicorn
        """, hint="PID — второй столбец; последняя строка — это сам grep.", xp=15),
),

lesson(f"{P}-env", "Переменные окружения и PATH",
    cmd(f"{P}-env-e1", "Выведи значение переменной окружения `HOME`.",
        ["echo $HOME", 'echo "$HOME"', "echo ${HOME}", "printenv HOME"]),
    cmd(f"{P}-env-e2", "Задай переменную окружения `BASE_URL=https://stage.example.com` так, чтобы её видели запущенные дальше программы.",
        ["export BASE_URL=https://stage.example.com", "export BASE_URL='https://stage.example.com'",
         'export BASE_URL="https://stage.example.com"']),
    cmd(f"{P}-env-e3", "Запусти `pytest` так, чтобы переменная `ENV=stage` была задана **только для этого запуска**.",
        ["ENV=stage pytest", "env ENV=stage pytest"]),
    cmd(f"{P}-env-e4", "Покажи все переменные окружения.",
        ["env", "printenv", "export -p"]),
    cmd(f"{P}-env-e5", "Узнай, какой именно файл запускается, когда ты вводишь `python` (полный путь).",
        ["which python", "command -v python", "type python", "which -a python"]),
    cmd(f"{P}-env-e6", "Выведи содержимое переменной `PATH`.",
        ["echo $PATH", 'echo "$PATH"', "printenv PATH", "echo ${PATH}"]),
    cmd(f"{P}-env-e7", "Что выведет последняя команда?",
        ["stage"],
        context="""
        $ export ENV=prod
        $ ENV=stage bash -c 'echo $ENV'
        """, hint="VAR=значение перед командой задаёт переменную только для неё."),
    cod(f"{P}-env-e8", t("""
        В тестах конфигурацию часто берут из переменных окружения. Напиши функцию `load_settings(env)` — `env` — словарь (как `os.environ`). Вернуть словарь:

        - `"base_url"` — из `BASE_URL`, по умолчанию `"http://localhost:8000"`;
        - `"timeout"` — из `TIMEOUT` как **int**, по умолчанию `10`;
        - `"headless"` — из `HEADLESS`: `True`, если значение `"1"`, `"true"` или `"yes"` (в любом регистре), иначе `False`; по умолчанию `True`.
        """),
        """
        def load_settings(env):
            pass
        """,
        """
        def test_values():
            assert load_settings({}) == {"base_url": "http://localhost:8000", "timeout": 10, "headless": True}, load_settings({})
            assert load_settings({"BASE_URL": "https://stage", "TIMEOUT": "30", "HEADLESS": "no"}) == {"base_url": "https://stage", "timeout": 30, "headless": False}, "Заданные значения"
            assert load_settings({"HEADLESS": "YES"})["headless"] is True, "Регистр не важен"
        """,
        """
        def load_settings(env):
            return {
                "base_url": env.get("BASE_URL", "http://localhost:8000"),
                "timeout": int(env.get("TIMEOUT", "10")),
                "headless": env.get("HEADLESS", "true").lower() in ("1", "true", "yes"),
            }
        """, xp=20),
),

lesson(f"{P}-net", "Сеть, диск и архивы",
    cmd(f"{P}-net-e1", "Отправь GET-запрос на `https://api.example.com/health` и выведи ответ с помощью `curl`.",
        ["curl https://api.example.com/health", "curl -s https://api.example.com/health", "curl -sS https://api.example.com/health"]),
    cmd(f"{P}-net-e2", "Покажи через `curl` **только заголовки** ответа `https://api.example.com/health` (метод HEAD).",
        ["curl -I https://api.example.com/health", "curl --head https://api.example.com/health", "curl -sI https://api.example.com/health"]),
    cmd(f"{P}-net-e3", t("""
        Отправь POST-запрос на `https://api.example.com/users` с JSON-телом `{"name": "anna"}` и заголовком `Content-Type: application/json`.
        """),
        ["""curl -X POST https://api.example.com/users -H 'Content-Type: application/json' -d '{"name": "anna"}'""",
         """curl -X POST -H 'Content-Type: application/json' -d '{"name": "anna"}' https://api.example.com/users""",
         """curl https://api.example.com/users -H 'Content-Type: application/json' -d '{"name": "anna"}'""",
         """curl -H 'Content-Type: application/json' -d '{"name": "anna"}' https://api.example.com/users""",
         """curl -X POST https://api.example.com/users -H "Content-Type: application/json" -d '{"name": "anna"}'""",
         """curl -X POST https://api.example.com/users --json '{"name": "anna"}'""",
         """curl https://api.example.com/users --json '{"name": "anna"}'""",
         """re:curl .*-d '\\{"name": ?"anna"\\}'.*""",
         """re:curl .*--data '\\{"name": ?"anna"\\}'.*"""],
        hint="-X — метод, -H — заголовок, -d — тело запроса.", xp=15),
    cmd(f"{P}-net-e4", "Подключись по SSH к серверу `203.0.113.10` под пользователем `qa`.",
        ["ssh qa@203.0.113.10", "ssh -l qa 203.0.113.10"]),
    cmd(f"{P}-net-e5", "Скачай с сервера `qa@203.0.113.10` файл `/var/log/app.log` в текущую папку с помощью `scp`.",
        ["scp qa@203.0.113.10:/var/log/app.log .", "scp qa@203.0.113.10:/var/log/app.log ./"]),
    cmd(f"{P}-net-e6", "Покажи, сколько места свободно на дисках, в понятном виде (Г, М).",
        ["df -h", "df -H"]),
    cmd(f"{P}-net-e7", "Узнай, сколько места занимает папка `allure-results` целиком (одно число в понятном виде).",
        ["du -sh allure-results", "du -sh allure-results/", "du -hs allure-results", "du -sh ./allure-results"]),
    cmd(f"{P}-net-e8", "Упакуй папку `allure-report` в сжатый архив `report.tar.gz`.",
        ["tar -czf report.tar.gz allure-report", "tar czf report.tar.gz allure-report", "tar -czvf report.tar.gz allure-report",
         "tar -zcf report.tar.gz allure-report", "tar -czf report.tar.gz allure-report/", "tar czvf report.tar.gz allure-report",
         "tar -cvzf report.tar.gz allure-report", "tar -zcvf report.tar.gz allure-report"],
        hint="c — create, z — gzip, f — имя архива.", xp=15),
),
)
