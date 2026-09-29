"""Тема «Docker для тестировщика», модуль 1 «Контейнеры» — задания. Теория — в _dkr_t1.py.

Урок dci-m1-l1 унаследован от старой темы «Docker и CI/CD» — так сохраняется прогресс.
Docker в песочнице не запустить: практика — команды («Терминал»), утилиты на Python
и файлы (Dockerfile, compose) строкой, которые проверки разбирают."""
import re

from ._lib import cmd, cod, lesson, module, out, t

P = "dkr"
O = "dci"   # префикс уроков старой темы


def anyorder(prefix, flags, tail):
    """Вариант ответа «re:…»: команда prefix, флаги flags в любом порядке, в конце tail."""
    look = "".join(f"(?=(?:.* )?{re.escape(f)}(?: |$))" for f in flags)
    rest = f"(?:\\S+ )*{re.escape(tail)}" if tail else "\\S+(?: \\S+)*"
    return f"re:{re.escape(prefix)} {look}{rest}"


m1 = module(f"{P}-m1", "Контейнеры", "🐳", "Образы и контейнеры, запуск с портами, переменными и томами, диагностика, реестры и теги",

lesson(f"{O}-m1-l1", "Образы и контейнеры",
    out(f"{O}-m1-l1-e1", "Что выведет программа? Разбираем ссылку на образ.", """
            for ref in ["python:3.12-slim", "nginx", "postgres:16"]:
                name, _, tag = ref.partition(":")
                print(name, tag or "latest")
            """),
    out(f"{O}-m1-l1-e2", "Что выведет программа? Конфигурацию тестов часто передают через переменные окружения (`-e` в docker run).", """
            env = {"BASE_URL": "http://app:8000", "BROWSER": ""}
            base_url = env.get("BASE_URL", "http://localhost")
            browser = env.get("BROWSER") or "chrome"
            headless = env.get("HEADLESS", "true") == "true"
            print(base_url, browser, headless)
            """),
    cod(f"{O}-m1-l1-e3", t("""
            Напиши функцию `parse_image(ref)`, которая разбирает ссылку на Docker-образ.

            Ссылка имеет вид `имя:тег`, тег необязателен.

            - Получает: `ref` — строку-ссылку.
            - Возвращает: пару `(имя, тег)`. Если тега нет — тег `"latest"`.

            Примеры:
            ```
            parse_image("python:3.12-slim")   # → ("python", "3.12-slim")
            parse_image("nginx")              # → ("nginx", "latest")
            ```
            """),
            """
            def parse_image(ref):
                pass
            """,
            """
            def test_with_tag():
                assert parse_image("python:3.12-slim") == ("python", "3.12-slim"), f"Получено {parse_image('python:3.12-slim')}"

            def test_no_tag():
                assert parse_image("nginx") == ("nginx", "latest"), "Без тега → latest"
            """,
            """
            def parse_image(ref):
                name, _, tag = ref.partition(":")
                return name, tag or "latest"
            """),
    cod(f"{O}-m1-l1-e4", t("""
            Напиши функцию `docker_run_cmd(image, ports=None, env=None, rm=True)`, которая собирает команду `docker run`.

            - Получает:
              - `image` — образ;
              - `ports` — словарь `{порт_хоста: порт_контейнера}` или `None`;
              - `env` — словарь переменных окружения `{ИМЯ: значение}` или `None`;
              - `rm` — добавлять ли флаг `--rm`.
            - Возвращает: команду одной строкой, части через пробел, **строго в таком порядке**:
              1. `docker run`
              2. `--rm` — если `rm` истинно
              3. `-p хост:контейнер` — для каждой пары из `ports`
              4. `-e ИМЯ=значение` — для каждой переменной из `env`
              5. образ

            Примеры:
            ```
            docker_run_cmd("app:1.0", ports={8080: 80}, env={"DEBUG": "1", "MODE": "test"})
            # → "docker run --rm -p 8080:80 -e DEBUG=1 -e MODE=test app:1.0"

            docker_run_cmd("nginx", rm=False)
            # → "docker run nginx"
            ```
            """),
            """
            def docker_run_cmd(image, ports=None, env=None, rm=True):
                pass
            """,
            """
            def test_full():
                got = docker_run_cmd("app:1.0", ports={8080: 80}, env={"DEBUG": "1", "MODE": "test"})
                assert got == "docker run --rm -p 8080:80 -e DEBUG=1 -e MODE=test app:1.0", f"Получено {got!r}"

            def test_minimal():
                assert docker_run_cmd("nginx", rm=False) == "docker run nginx", f"Получено {docker_run_cmd('nginx', rm=False)!r}"
            """,
            """
            def docker_run_cmd(image, ports=None, env=None, rm=True):
                parts = ["docker", "run"]
                if rm:
                    parts.append("--rm")
                for host, container in (ports or {}).items():
                    parts.append(f"-p {host}:{container}")
                for key, value in (env or {}).items():
                    parts.append(f"-e {key}={value}")
                parts.append(image)
                return " ".join(parts)
            """,
            hint="Собери части в список и соедини через `\" \".join(parts)`. `ports or {}` спасает от None.", xp=20),
    cod(f"{O}-m1-l1-e5", t("""
            Напиши функцию `explain_exit(code)`, которая объясняет код выхода упавшего контейнера.

            - Получает: `code` — код выхода (число).
            - Возвращает строку-пояснение:
              - `0` → `"ok"`
              - `1` → `"app error"` — ошибка в самом приложении
              - `125` → `"docker error"` — ошибка самого Docker
              - `127` → `"command not found"` — команда не найдена
              - `137` → `"killed (OOM?)"` — процесс убит, часто из-за нехватки памяти
              - любой другой код → `"unknown"`

            Примеры:
            ```
            explain_exit(137)   # → "killed (OOM?)"
            explain_exit(42)    # → "unknown"
            ```
            """),
            """
            def explain_exit(code):
                pass
            """,
            """
            def test_known():
                got = [explain_exit(c) for c in (0, 1, 125, 127, 137)]
                assert got == ["ok", "app error", "docker error", "command not found", "killed (OOM?)"], f"Получено {got}"

            def test_unknown():
                assert explain_exit(42) == "unknown", "Неизвестный код → unknown"
            """,
            """
            def explain_exit(code):
                return {0: "ok", 1: "app error", 125: "docker error", 127: "command not found",
                        137: "killed (OOM?)"}.get(code, "unknown")
            """,
            hint="Словарь + `.get(code, \"unknown\")`."),
    cmd(f"{O}-m1-l1-e6", "Скачай образ PostgreSQL версии **16** из Docker Hub (без запуска).",
        ["docker pull postgres:16", "docker image pull postgres:16"],
        hint="`docker pull имя:тег`."),
    cmd(f"{O}-m1-l1-e7", "Запусти контейнер из образа `hello-world` так, чтобы после завершения он **удалился** сам.",
        ["docker run --rm hello-world", "docker container run --rm hello-world"],
        hint="Флаг `--rm`."),
    cmd(f"{O}-m1-l1-e8", "`docker ps` показывает только запущенные контейнеры. Покажи **все**, включая остановленные.",
        ["docker ps -a", "docker ps --all", "docker container ls -a", "docker container ls --all"],
        hint="Флаг `-a`."),
),

lesson(f"{P}-run", "Запуск: порты, переменные, тома",
    out(f"{P}-run-e1", "Что выведет программа? Так оболочка разбивает команду на аргументы: кавычки не дают разрезать значение с пробелом.", """
        import shlex

        cmd = 'docker run --rm -e "GREETING=Привет мир" -p 8080:80 nginx'
        args = shlex.split(cmd)
        print(len(args))
        print(args[4])
        print(args[-1])
        """),
    cmd(f"{P}-run-e2", "Запусти `nginx` **в фоне** с именем `web`, пробросив порт **8080** хоста на порт **80** контейнера.",
        ["docker run -d --name web -p 8080:80 nginx", anyorder("docker run", ["-d", "--name web", "-p 8080:80"], "nginx")],
        hint="`-d` — в фоне, `--name` — имя, `-p хост:контейнер`."),
    cmd(f"{P}-run-e3", "Запусти образ `my-tests` с переменной окружения `BASE_URL=http://stage.test`; контейнер должен удалиться после завершения.",
        ["docker run --rm -e BASE_URL=http://stage.test my-tests",
         anyorder("docker run", ["--rm", "-e BASE_URL=http://stage.test"], "my-tests"),
         anyorder("docker run", ["--rm", "--env BASE_URL=http://stage.test"], "my-tests")],
        hint="`-e ИМЯ=значение`."),
    cmd(f"{P}-run-e4", "Тесты в контейнере пишут отчёты в `/app/reports`. Запусти `my-tests` (с `--rm`), пробросив туда папку `reports` из текущей директории хоста — через `$(pwd)`.",
        ["docker run --rm -v $(pwd)/reports:/app/reports my-tests",
         anyorder("docker run", ["--rm", "-v $(pwd)/reports:/app/reports"], "my-tests"),
         anyorder("docker run", ["--rm", '-v "$(pwd)/reports:/app/reports"'], "my-tests"),
         anyorder("docker run", ["--rm", "-v ${PWD}/reports:/app/reports"], "my-tests"),
         anyorder("docker run", ["--rm", "-v ./reports:/app/reports"], "my-tests")],
        hint="`-v путь_на_хосте:путь_в_контейнере`."),
    cod(f"{P}-run-e5", t("""
        Напиши функцию `parse_port(spec)`, которая разбирает значение флага `-p`.

        - Формат `"8080:80"` → `{"ip": "0.0.0.0", "host": 8080, "container": 80}` (слушать на всех адресах).
        - Формат `"127.0.0.1:5432:5432"` → `{"ip": "127.0.0.1", "host": 5432, "container": 5432}`.

        Порты — числа (`int`).
        """),
        """
        def parse_port(spec):
            pass
        """,
        """
        def test_two_parts():
            assert parse_port("8080:80") == {"ip": "0.0.0.0", "host": 8080, "container": 80}, parse_port("8080:80")

        def test_three_parts():
            got = parse_port("127.0.0.1:5432:5432")
            assert got == {"ip": "127.0.0.1", "host": 5432, "container": 5432}, got
        """,
        """
        def parse_port(spec):
            parts = spec.split(":")
            ip = parts[0] if len(parts) == 3 else "0.0.0.0"
            return {"ip": ip, "host": int(parts[-2]), "container": int(parts[-1])}
        """,
        hint="`spec.split(\":\")` — две или три части; хост и контейнер — всегда две последние."),
    cod(f"{P}-run-e6", t("""
        Из Python команды запускают через `subprocess.run([...])` — списком аргументов. Напиши функцию `env_flags(env)`, которая превращает словарь переменных в аргументы для `docker run`.

        - Получает: словарь `{ИМЯ: значение}`.
        - Возвращает: список `["-e", "ИМЯ=значение", "-e", …]`, переменные **по алфавиту** имён.

        Пример:
        ```
        env_flags({"HEADLESS": "true", "BASE_URL": "http://app"})
        # → ["-e", "BASE_URL=http://app", "-e", "HEADLESS=true"]
        ```
        """),
        """
        def env_flags(env):
            pass
        """,
        """
        def test_flags():
            got = env_flags({"HEADLESS": "true", "BASE_URL": "http://app"})
            assert got == ["-e", "BASE_URL=http://app", "-e", "HEADLESS=true"], got

        def test_empty():
            assert env_flags({}) == []

        def test_spaces():
            assert env_flags({"MSG": "Привет мир"}) == ["-e", "MSG=Привет мир"], "Пробел в значении — не повод делить аргумент"
        """,
        """
        def env_flags(env):
            result = []
            for name in sorted(env):
                result += ["-e", f"{name}={env[name]}"]
            return result
        """),
    out(f"{P}-run-e7", "Что выведет программа? Флаг `-p` с одним и тем же портом хоста у двух контейнеров — конфликт: порт хоста может занять только один.", """
        running = {}
        for name, spec in [("web", "8080:80"), ("api", "8000:8000"), ("web2", "8080:80")]:
            host = int(spec.split(":")[0])
            if host in running:
                print(f"{name}: порт {host} занят контейнером {running[host]}")
            else:
                running[host] = name
                print(f"{name}: ok")
        """),
    cmd(f"{P}-run-e8", "Открой **интерактивную** оболочку `bash` в новом контейнере `python:3.12-slim` (с удалением после выхода) — удобно, чтобы проверить окружение.",
        ["docker run --rm -it python:3.12-slim bash",
         anyorder("docker run", ["--rm", "-it"], "python:3.12-slim bash"),
         anyorder("docker run", ["--rm", "-it"], "python:3.12-slim sh"),
         anyorder("docker run", ["--rm", "-i", "-t"], "python:3.12-slim bash")],
        hint="`-it` — интерактивно с терминалом, команда — после образа."),
),

lesson(f"{P}-debug", "Диагностика: ps, logs, exec, inspect",
    cmd(f"{P}-debug-e1", "Контейнер `app` упал. Покажи **последние 50 строк** его логов.",
        ["docker logs --tail 50 app", "docker logs -n 50 app", "docker logs --tail=50 app", "docker logs app --tail 50", "docker logs -n50 app"],
        hint="`docker logs --tail N имя`."),
    cmd(f"{P}-debug-e2", "Смотри логи контейнера `app` **в реальном времени** (новые строки появляются по мере записи).",
        ["docker logs -f app", "docker logs --follow app", "docker logs app -f"],
        hint="Флаг `-f`."),
    cmd(f"{P}-debug-e3", "Зайди внутрь **уже запущенного** контейнера `db` интерактивной оболочкой `bash`.",
        ["docker exec -it db bash", "docker exec -it db sh", "docker container exec -it db bash"],
        hint="`docker exec -it имя команда`."),
    cmd(f"{P}-debug-e4", "Выведи **только код выхода** остановленного контейнера `app` через `docker inspect` и шаблон `{{.State.ExitCode}}`.",
        ["docker inspect -f '{{.State.ExitCode}}' app", 'docker inspect -f "{{.State.ExitCode}}" app',
         "docker inspect --format '{{.State.ExitCode}}' app", 'docker inspect --format "{{.State.ExitCode}}" app',
         "docker inspect --format='{{.State.ExitCode}}' app"],
        hint="`docker inspect -f 'шаблон' имя`."),
    cod(f"{P}-debug-e5", t("""
        Напиши функцию `parse_ps(output)`, которая разбирает вывод `docker ps -a` в список словарей.

        Вывод — таблица, колонки разделены **двумя и более** пробелами (внутри значений бывает по одному пробелу):
        ```
        CONTAINER ID   IMAGE         STATUS                     NAMES
        3f2a1b9c8d7e   postgres:16   Up 2 hours                 db
        9a8b7c6d5e4f   my-tests      Exited (1) 5 minutes ago   tests
        ```
        - Возвращает: список словарей с ключами `"image"`, `"status"`, `"name"` — по одному на строку (заголовок пропусти).

        Разрезать по двум и более пробелам: `re.split(r"\\s{2,}", line.strip())`.
        """),
        """
        import re


        def parse_ps(output):
            pass
        """,
        """
        OUT = '''CONTAINER ID   IMAGE         STATUS                     NAMES
        3f2a1b9c8d7e   postgres:16   Up 2 hours                 db
        9a8b7c6d5e4f   my-tests      Exited (1) 5 minutes ago   tests
        '''

        def test_parse():
            got = parse_ps(OUT)
            assert got == [
                {"image": "postgres:16", "status": "Up 2 hours", "name": "db"},
                {"image": "my-tests", "status": "Exited (1) 5 minutes ago", "name": "tests"},
            ], got
        """,
        """
        import re


        def parse_ps(output):
            rows = []
            for line in output.strip().splitlines()[1:]:
                _id, image, status, name = re.split(r"\\s{2,}", line.strip())
                rows.append({"image": image, "status": status, "name": name})
            return rows
        """),
    cod(f"{P}-debug-e6", t("""
        Напиши функцию `crashed(lines)`, которая находит упавшие контейнеры по выводу
        `docker ps -a --format "{{.Names}}|{{.Status}}"`.

        - Получает: список строк вида `"tests|Exited (1) 2 minutes ago"`.
        - Возвращает: список имён контейнеров, которые завершились с **ненулевым** кодом (`Exited (N)`, где N ≠ 0), в исходном порядке. Работающие (`Up …`) и завершившиеся успешно (`Exited (0)`) не попадают.

        Пример:
        ```
        crashed(["db|Up 2 hours", "tests|Exited (1) 1 minute ago", "migrate|Exited (0) 3 minutes ago", "app|Exited (137) 5 seconds ago"])
        # → ["tests", "app"]
        ```
        """),
        """
        def crashed(lines):
            pass
        """,
        """
        def test_crashed():
            lines = ["db|Up 2 hours", "tests|Exited (1) 1 minute ago", "migrate|Exited (0) 3 minutes ago", "app|Exited (137) 5 seconds ago"]
            assert crashed(lines) == ["tests", "app"], crashed(lines)

        def test_none():
            assert crashed(["db|Up 1 hour", "job|Exited (0) now"]) == []
        """,
        """
        import re


        def crashed(lines):
            names = []
            for line in lines:
                name, status = line.split("|", 1)
                m = re.match(r"Exited \\((\\d+)\\)", status)
                if m and m.group(1) != "0":
                    names.append(name)
            return names
        """,
        hint='Код — число в скобках после «Exited»: `re.match(r"Exited \\((\\d+)\\)", status)`.'),
    out(f"{P}-debug-e7", "Что выведет программа? `docker inspect` отдаёт JSON — из него достают состояние контейнера.", """
        import json

        raw = '''[{"Name": "/app", "State": {"Status": "exited", "ExitCode": 137, "OOMKilled": true}}]'''
        info = json.loads(raw)[0]
        state = info["State"]
        print(info["Name"].lstrip("/"), state["Status"], state["ExitCode"])
        if state["OOMKilled"]:
            print("не хватило памяти")
        """),
    cod(f"{P}-debug-e8", t("""
        Напиши функцию `find_errors(log)`, которая выбирает из лога контейнера строки с проблемами.

        - Получает: `log` — многострочный текст.
        - Возвращает: список пар `(номер строки, строка)` — нумерация с 1 — для строк, где встречается `ERROR` или которые начинаются с `Traceback`.

        Пример:
        ```
        log = "INFO start\\nERROR db timeout\\nINFO retry\\nTraceback (most recent call last):"
        find_errors(log)
        # → [(2, "ERROR db timeout"), (4, "Traceback (most recent call last):")]
        ```
        """),
        """
        def find_errors(log):
            pass
        """,
        """
        def test_errors():
            log = "INFO start\\nERROR db timeout\\nINFO retry\\nTraceback (most recent call last):"
            assert find_errors(log) == [(2, "ERROR db timeout"), (4, "Traceback (most recent call last):")], find_errors(log)

        def test_clean():
            assert find_errors("INFO ok\\nINFO done") == []
        """,
        """
        def find_errors(log):
            return [(i, line) for i, line in enumerate(log.splitlines(), 1)
                    if "ERROR" in line or line.startswith("Traceback")]
        """),
),

lesson(f"{P}-registry", "Реестры, теги и версии",
    out(f"{P}-registry-e1", "Что выведет программа? Полная ссылка на образ: реестр/владелец/имя:тег.", """
        ref = "ghcr.io/acme/shop-tests:1.4.2"
        path, _, tag = ref.rpartition(":")
        registry, *repo = path.split("/")
        print(registry)
        print("/".join(repo))
        print(tag)
        """),
    cod(f"{P}-registry-e2", t("""
        Напиши функцию `parse_ref(ref)`, которая разбирает полную ссылку на образ.

        - Возвращает словарь `{"registry": …, "repo": …, "tag": …}`.
        - **Реестр** — первая часть пути, если в ней есть точка или двоеточие (`ghcr.io`, `localhost:5000`) либо это `localhost`. Иначе реестр — `"docker.io"`, а вся ссылка — репозиторий.
        - **Тег** — после последнего `:` **в последней части пути**; нет тега — `"latest"`.

        Примеры:
        ```
        parse_ref("ghcr.io/acme/tests:1.4")    # → {"registry": "ghcr.io", "repo": "acme/tests", "tag": "1.4"}
        parse_ref("postgres")                  # → {"registry": "docker.io", "repo": "postgres", "tag": "latest"}
        parse_ref("localhost:5000/app:dev")    # → {"registry": "localhost:5000", "repo": "app", "tag": "dev"}
        ```
        """),
        """
        def parse_ref(ref):
            pass
        """,
        """
        def test_cases():
            assert parse_ref("ghcr.io/acme/tests:1.4") == {"registry": "ghcr.io", "repo": "acme/tests", "tag": "1.4"}, parse_ref("ghcr.io/acme/tests:1.4")
            assert parse_ref("postgres") == {"registry": "docker.io", "repo": "postgres", "tag": "latest"}, parse_ref("postgres")
            assert parse_ref("localhost:5000/app:dev") == {"registry": "localhost:5000", "repo": "app", "tag": "dev"}, parse_ref("localhost:5000/app:dev")

        def test_hub_namespace():
            assert parse_ref("acme/tests:2") == {"registry": "docker.io", "repo": "acme/tests", "tag": "2"}, parse_ref("acme/tests:2")
        """,
        """
        def parse_ref(ref):
            parts = ref.split("/")
            registry = "docker.io"
            if len(parts) > 1 and ("." in parts[0] or ":" in parts[0] or parts[0] == "localhost"):
                registry = parts.pop(0)
            last = parts[-1]
            tag = "latest"
            if ":" in last:
                last, tag = last.rsplit(":", 1)
            parts[-1] = last
            return {"registry": registry, "repo": "/".join(parts), "tag": tag}
        """,
        hint="Двоеточие в `localhost:5000` — порт реестра, а не тег: тег ищи только в последней части после `/`.", xp=20),
    cod(f"{P}-registry-e3", t("""
        В CI образы нужно указывать с **зафиксированной** версией — иначе завтра `latest` окажется другим, и тесты сломаются «сами».

        Напиши функцию `is_pinned(ref)`: `True`, если у ссылки есть дайджест (`@sha256:…`) или тег, отличный от `latest`. Иначе `False`.

        Примеры:
        ```
        is_pinned("postgres:16")                     # → True
        is_pinned("postgres")                        # → False
        is_pinned("nginx:latest")                    # → False
        is_pinned("nginx@sha256:4c0fdaa8b634")       # → True
        is_pinned("localhost:5000/app")              # → False   5000 — порт, а не тег
        ```
        """),
        """
        def is_pinned(ref):
            pass
        """,
        """
        def test_pinned():
            for ref in ["postgres:16", "nginx@sha256:4c0fdaa8b634", "ghcr.io/acme/tests:1.4", "localhost:5000/app:dev"]:
                assert is_pinned(ref) is True, f"{ref} — версия зафиксирована"

        def test_not_pinned():
            for ref in ["postgres", "nginx:latest", "localhost:5000/app", "acme/tests"]:
                assert is_pinned(ref) is False, f"{ref} — версия не зафиксирована"
        """,
        """
        def is_pinned(ref):
            if "@sha256:" in ref:
                return True
            last = ref.split("/")[-1]
            return ":" in last and last.rsplit(":", 1)[1] != "latest"
        """),
    cmd(f"{P}-registry-e4", "Дай локальному образу `my-tests:latest` второе имя для реестра — `ghcr.io/acme/my-tests:1.0`.",
        ["docker tag my-tests:latest ghcr.io/acme/my-tests:1.0", "docker image tag my-tests:latest ghcr.io/acme/my-tests:1.0",
         "docker tag my-tests ghcr.io/acme/my-tests:1.0"],
        hint="`docker tag источник новое_имя`."),
    cmd(f"{P}-registry-e5", "Войди в реестр GitHub `ghcr.io` (логин и токен команда спросит сама).",
        ["docker login ghcr.io"],
        hint="`docker login реестр`."),
    cmd(f"{P}-registry-e6", "Отправь образ `ghcr.io/acme/my-tests:1.0` в реестр.",
        ["docker push ghcr.io/acme/my-tests:1.0", "docker image push ghcr.io/acme/my-tests:1.0"],
        hint="`docker push имя:тег`."),
    cod(f"{P}-registry-e7", t("""
        Напиши функцию `latest_version(tags)`, которая выбирает самую свежую версию из списка тегов.

        - Учитываются только теги вида `X.Y.Z` из чисел (`"1.10.2"`); остальные (`"latest"`, `"dev"`, `"1.2"`) пропускаются.
        - Сравнивать нужно **как числа** по частям: `1.10.0` новее `1.9.9` (строками было бы наоборот).
        - Если подходящих тегов нет — `None`.

        Пример:
        ```
        latest_version(["1.2.0", "1.10.1", "latest", "1.9.9", "dev"])   # → "1.10.1"
        ```
        """),
        """
        def latest_version(tags):
            pass
        """,
        """
        def test_numeric():
            assert latest_version(["1.2.0", "1.10.1", "latest", "1.9.9", "dev"]) == "1.10.1", latest_version(["1.2.0", "1.10.1", "latest", "1.9.9", "dev"])
            assert latest_version(["2.0.0", "10.0.0", "9.99.99"]) == "10.0.0"

        def test_none():
            assert latest_version(["latest", "1.2", "v1.0.0"]) is None
        """,
        """
        import re


        def latest_version(tags):
            versions = [t for t in tags if re.fullmatch(r"\\d+\\.\\d+\\.\\d+", t)]
            if not versions:
                return None
            return max(versions, key=lambda t: tuple(int(x) for x in t.split(".")))
        """,
        hint='`max(..., key=lambda t: tuple(int(x) for x in t.split(".")))` — кортежи сравниваются по частям.'),
    cmd(f"{P}-registry-e8", "Покажи список локальных образов.",
        ["docker images", "docker image ls", "docker image list"],
        hint="`docker images`."),
),
)
