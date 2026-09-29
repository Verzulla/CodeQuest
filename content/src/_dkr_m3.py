"""Тема «Docker для тестировщика», модуль 3 «Docker Compose» — задания. Теория — в _dkr_t3.py.

Файлы compose ученик пишет строкой YAML, проверки разбирают её через PyYAML (есть в песочнице)."""
from ._lib import cmd, cod, lesson, module, out, t
from ._dkr_m1 import anyorder

P = "dkr"

m3 = module(f"{P}-m3", "Docker Compose", "🧩", "Несколько сервисов одним файлом, переменные и .env, тестовый стенд со здоровьем сервисов, практика",

lesson(f"{P}-compose", "Compose: несколько сервисов",
    out(f"{P}-compose-e1", "Что выведет программа? `docker-compose.yml` — обычный YAML, его можно разобрать и в Python.", """
        import yaml

        text = '''
        services:
          app:
            image: shop-app:1.0
            ports:
              - "8000:8000"
          db:
            image: postgres:16
        '''
        compose = yaml.safe_load(text)
        print(list(compose["services"]))
        print(compose["services"]["app"]["ports"])
        print(compose["services"]["db"].get("ports", []))
        """),
    cod(f"{P}-compose-e2", t("""
        Напиши `docker-compose.yml` строкой YAML в переменной `COMPOSE` — магазин и его база:

        - сервис `db`: образ `postgres:16`, переменная окружения `POSTGRES_PASSWORD: secret`;
        - сервис `app`: образ `shop-app:1.0`, порт `"8000:8000"`, переменная `DATABASE_URL: postgresql://postgres:secret@db:5432/postgres`, и `depends_on: [db]` — запускать после базы.

        Отступы в YAML — пробелами, по два на уровень. Порт пиши в кавычках: `"8000:8000"`.
        """),
        '''
        COMPOSE = """
        services:
          db:
            image: postgres:16
        """
        ''',
        """
        import yaml

        def load():
            data = yaml.safe_load(COMPOSE)
            assert isinstance(data, dict) and "services" in data, "Верхний ключ — services"
            return data["services"]

        def test_db():
            db = load().get("db") or {}
            assert db.get("image") == "postgres:16", "db: image postgres:16"
            assert (db.get("environment") or {}).get("POSTGRES_PASSWORD") == "secret", "db: POSTGRES_PASSWORD: secret"

        def test_app():
            app = load().get("app") or {}
            assert app.get("image") == "shop-app:1.0", "app: image shop-app:1.0"
            assert app.get("ports") == ["8000:8000"], f"app: ports [\\"8000:8000\\"], а сейчас {app.get('ports')}"
            assert (app.get("environment") or {}).get("DATABASE_URL") == "postgresql://postgres:secret@db:5432/postgres", "app: DATABASE_URL"
            assert app.get("depends_on") == ["db"], "app: depends_on: [db]"
        """,
        '''
        COMPOSE = """
        services:
          db:
            image: postgres:16
            environment:
              POSTGRES_PASSWORD: secret
          app:
            image: shop-app:1.0
            ports:
              - "8000:8000"
            environment:
              DATABASE_URL: postgresql://postgres:secret@db:5432/postgres
            depends_on:
              - db
        """
        ''', xp=20),
    cmd(f"{P}-compose-e3", "Подними все сервисы из `docker-compose.yml` **в фоне**.",
        ["docker compose up -d", "docker compose up --detach", "docker-compose up -d"],
        hint="`docker compose up` + флаг фона."),
    cmd(f"{P}-compose-e4", "Останови и удали все контейнеры стенда **вместе с томами** (данные базы тоже нужно стереть).",
        ["docker compose down -v", "docker compose down --volumes", "docker-compose down -v"],
        hint="`docker compose down` + флаг томов."),
    cmd(f"{P}-compose-e5", "Смотри в реальном времени логи только сервиса `app`.",
        ["docker compose logs -f app", "docker compose logs --follow app", "docker-compose logs -f app", "docker compose logs app -f"],
        hint="`docker compose logs -f сервис`."),
    cod(f"{P}-compose-e6", t("""
        Напиши функцию `start_order(services)`, которая определяет порядок запуска сервисов по `depends_on`.

        - Получает: словарь `services` из compose-файла; у сервиса может быть `depends_on` — список имён.
        - Возвращает: список имён — каждый сервис идёт **после** всех, от кого зависит. Если выбор есть (несколько сервисов готовы к запуску), бери **первый по алфавиту**.

        Пример:
        ```
        start_order({
            "tests": {"depends_on": ["app"]},
            "app": {"depends_on": ["db", "cache"]},
            "db": {},
            "cache": {},
        })
        # → ["cache", "db", "app", "tests"]
        ```
        """),
        """
        def start_order(services):
            pass
        """,
        """
        def test_order():
            services = {"tests": {"depends_on": ["app"]}, "app": {"depends_on": ["db", "cache"]}, "db": {}, "cache": {}}
            assert start_order(services) == ["cache", "db", "app", "tests"], start_order(services)

        def test_independent():
            assert start_order({"b": {}, "a": {}}) == ["a", "b"]
        """,
        """
        def start_order(services):
            order = []
            while len(order) < len(services):
                ready = [name for name, s in services.items()
                         if name not in order and all(d in order for d in s.get("depends_on", []))]
                order.append(min(ready))
            return order
        """,
        hint="Повторяй: из ещё не запущенных выбери тех, чьи зависимости уже в списке, и добавь минимальный по алфавиту.", xp=20),
    cod(f"{P}-compose-e7", t("""
        Напиши функцию `published_ports(services)`: для каждого сервиса, у которого есть `ports`, верни список **портов хоста** числами.

        Порт в compose пишут строкой `"8080:80"` или `"127.0.0.1:5432:5432"` — порт хоста в них предпоследний.

        Пример:
        ```
        published_ports({"app": {"ports": ["8000:8000", "9000:9000"]}, "db": {"ports": ["127.0.0.1:5432:5432"]}, "worker": {}})
        # → {"app": [8000, 9000], "db": [5432]}
        ```
        """),
        """
        def published_ports(services):
            pass
        """,
        """
        def test_ports():
            got = published_ports({"app": {"ports": ["8000:8000", "9000:9000"]}, "db": {"ports": ["127.0.0.1:5432:5432"]}, "worker": {}})
            assert got == {"app": [8000, 9000], "db": [5432]}, got
        """,
        """
        def published_ports(services):
            return {name: [int(p.split(":")[-2]) for p in s["ports"]]
                    for name, s in services.items() if s.get("ports")}
        """),
    cmd(f"{P}-compose-e8", "Покажи состояние контейнеров текущего compose-проекта.",
        ["docker compose ps", "docker compose ps -a", "docker-compose ps"],
        hint="`docker compose ps`."),
),

lesson(f"{P}-env", "Переменные и .env",
    out(f"{P}-env-e1", "Что выведет программа? Файл `.env` — строки `ИМЯ=значение`, Compose читает его автоматически.", """
        text = '''
        # стенд
        BASE_URL=http://stage.test
        BROWSER=firefox
        '''
        env = {}
        for line in text.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                name, value = line.split("=", 1)
                env[name] = value
        print(env)
        """),
    cod(f"{P}-env-e2", t("""
        Напиши функцию `parse_env_file(text)`, которая разбирает файл `.env` в словарь.

        - Пустые строки и строки-комментарии (`#` в начале) пропускаются.
        - Делить по **первому** `=` (в значении `=` тоже бывает).
        - Пробелы по краям имени и значения убираются; если значение в одинарных или двойных кавычках — кавычки снимаются.

        Пример:
        ```
        text = "# стенд\\nBASE_URL=http://stage.test\\nTOKEN='a=b'\\n\\nNAME = \\"Аня\\"\\n"
        parse_env_file(text)
        # → {"BASE_URL": "http://stage.test", "TOKEN": "a=b", "NAME": "Аня"}
        ```
        """),
        """
        def parse_env_file(text):
            pass
        """,
        """
        def test_parse():
            text = "# стенд\\nBASE_URL=http://stage.test\\nTOKEN='a=b'\\n\\nNAME = \\"Аня\\"\\n"
            got = parse_env_file(text)
            assert got == {"BASE_URL": "http://stage.test", "TOKEN": "a=b", "NAME": "Аня"}, got

        def test_empty_value():
            assert parse_env_file("EMPTY=\\n") == {"EMPTY": ""}
        """,
        """
        def parse_env_file(text):
            env = {}
            for line in text.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                name, _, value = line.partition("=")
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\\"":
                    value = value[1:-1]
                env[name.strip()] = value
            return env
        """),
    cod(f"{P}-env-e3", t("""
        Откуда Compose берёт значение переменной? Приоритет (от сильного к слабому): **переменная оболочки** → файл **`.env`** → **значение по умолчанию** в `${VAR:-default}`.

        Напиши функцию `resolve(name, default, env_file, shell)`: вернуть значение по этим правилам. `env_file` и `shell` — словари; пустая строка считается «нет значения» (как в `:-`).

        Примеры:
        ```
        resolve("BASE_URL", "http://app", {"BASE_URL": "http://stage"}, {})               # → "http://stage"
        resolve("BASE_URL", "http://app", {"BASE_URL": "http://stage"}, {"BASE_URL": "http://prod"})   # → "http://prod"
        resolve("BROWSER", "chromium", {}, {"BROWSER": ""})                                 # → "chromium"
        ```
        """),
        """
        def resolve(name, default, env_file, shell):
            pass
        """,
        """
        def test_priority():
            assert resolve("BASE_URL", "http://app", {"BASE_URL": "http://stage"}, {}) == "http://stage"
            assert resolve("BASE_URL", "http://app", {"BASE_URL": "http://stage"}, {"BASE_URL": "http://prod"}) == "http://prod"
            assert resolve("BROWSER", "chromium", {}, {"BROWSER": ""}) == "chromium"
            assert resolve("X", "d", {"X": ""}, {}) == "d"
        """,
        """
        def resolve(name, default, env_file, shell):
            return shell.get(name) or env_file.get(name) or default
        """,
        hint="`a or b or c` вернёт первое непустое значение."),
    cmd(f"{P}-env-e4", "Подними стенд в фоне, взяв переменные из файла `.env.stage` вместо `.env`.",
        ["docker compose --env-file .env.stage up -d", anyorder("docker compose", ["--env-file .env.stage"], "up -d"),
         "docker compose --env-file .env.stage up --detach"],
        hint="Опция `--env-file` пишется до `up`."),
    cod(f"{P}-env-e5", t("""
        Напиши `COMPOSE` с сервисом `tests`:

        - `build: .` — образ собирается из Dockerfile рядом;
        - в `environment` переменная `BASE_URL` со значением `${BASE_URL:-http://app:8000}` — берётся из окружения, а по умолчанию указывает на сервис `app`;
        - `volumes`: `./reports:/app/reports` — отчёты попадут на хост.
        """),
        '''
        COMPOSE = """
        services:
          tests:
            build: .
        """
        ''',
        """
        import yaml

        def test_tests_service():
            tests = (yaml.safe_load(COMPOSE) or {}).get("services", {}).get("tests") or {}
            assert tests.get("build") == ".", "tests: build: ."
            env = tests.get("environment") or {}
            if isinstance(env, list):
                env = dict(item.split("=", 1) for item in env)
            assert env.get("BASE_URL") == "${BASE_URL:-http://app:8000}", f"BASE_URL: ${{BASE_URL:-http://app:8000}}, а сейчас {env.get('BASE_URL')!r}"
            assert tests.get("volumes") == ["./reports:/app/reports"], "volumes: ./reports:/app/reports"
        """,
        '''
        COMPOSE = """
        services:
          tests:
            build: .
            environment:
              BASE_URL: ${BASE_URL:-http://app:8000}
            volumes:
              - ./reports:/app/reports
        """
        '''),
    cmd(f"{P}-env-e6", "Покажи итоговую конфигурацию compose — с уже подставленными переменными (удобно проверить, что `${BASE_URL}` подхватился).",
        ["docker compose config", "docker-compose config"],
        hint="`docker compose config`."),
    out(f"{P}-env-e7", "Что выведет программа? `environment` в compose можно записать словарём или списком — это одно и то же.", """
        as_dict = {"BASE_URL": "http://app", "HEADLESS": "true"}
        as_list = ["BASE_URL=http://app", "HEADLESS=true"]
        from_list = dict(item.split("=", 1) for item in as_list)
        print(from_list)
        print(from_list == as_dict)
        """),
    cod(f"{P}-env-e8", t("""
        Напиши функцию `normalize_env(env)`, которая приводит `environment` из compose к словарю строк:

        - словарь → значения переводятся в строки (`True` → `"true"`, `False` → `"false"`, `None` → `""`, числа — `str`);
        - список `["A=1", "B"]` → `{"A": "1", "B": ""}` (элемент без `=` — пустое значение);
        - `None` → `{}`.

        Пример:
        ```
        normalize_env({"DEBUG": True, "WORKERS": 4, "EMPTY": None})   # → {"DEBUG": "true", "WORKERS": "4", "EMPTY": ""}
        normalize_env(["A=1", "B"])                                    # → {"A": "1", "B": ""}
        ```
        """),
        """
        def normalize_env(env):
            pass
        """,
        """
        def test_dict():
            assert normalize_env({"DEBUG": True, "WORKERS": 4, "EMPTY": None}) == {"DEBUG": "true", "WORKERS": "4", "EMPTY": ""}
            assert normalize_env({"OFF": False}) == {"OFF": "false"}

        def test_list():
            assert normalize_env(["A=1", "B", "C=x=y"]) == {"A": "1", "B": "", "C": "x=y"}

        def test_none():
            assert normalize_env(None) == {}
        """,
        """
        def normalize_env(env):
            if env is None:
                return {}
            if isinstance(env, list):
                return {name: value for name, _, value in (item.partition("=") for item in env)}
            result = {}
            for name, value in env.items():
                if isinstance(value, bool):
                    value = "true" if value else "false"
                elif value is None:
                    value = ""
                result[name] = str(value)
            return result
        """),
),

lesson(f"{P}-stand", "Тестовый стенд в Compose",
    cod(f"{P}-stand-e1", t("""
        Тесты должны стартовать, только когда база действительно **готова**, а не просто запущена. Для этого — `healthcheck` и `depends_on` с условием. Напиши `COMPOSE`:

        - `db`: `postgres:16`, `POSTGRES_PASSWORD: secret`, `healthcheck` с `test: ["CMD", "pg_isready", "-U", "postgres"]`, `interval: 2s`, `retries: 10`;
        - `tests`: `build: .`, `depends_on` в полной форме: `db: {condition: service_healthy}`.
        """),
        '''
        COMPOSE = """
        services:
          db:
            image: postgres:16
        """
        ''',
        """
        import yaml

        def services():
            return (yaml.safe_load(COMPOSE) or {}).get("services", {})

        def test_healthcheck():
            db = services().get("db") or {}
            hc = db.get("healthcheck") or {}
            assert hc.get("test") == ["CMD", "pg_isready", "-U", "postgres"], f"healthcheck.test: {hc.get('test')}"
            assert hc.get("interval") == "2s" and hc.get("retries") == 10, "interval: 2s, retries: 10"

        def test_depends():
            tests = services().get("tests") or {}
            assert tests.get("build") == ".", "tests: build: ."
            dep = tests.get("depends_on")
            assert isinstance(dep, dict) and (dep.get("db") or {}).get("condition") == "service_healthy", "depends_on: db: condition: service_healthy"
        """,
        '''
        COMPOSE = """
        services:
          db:
            image: postgres:16
            environment:
              POSTGRES_PASSWORD: secret
            healthcheck:
              test: ["CMD", "pg_isready", "-U", "postgres"]
              interval: 2s
              retries: 10
          tests:
            build: .
            depends_on:
              db:
                condition: service_healthy
        """
        ''', xp=20),
    cmd(f"{P}-stand-e2", "Подними стенд так, чтобы всё остановилось, когда закончатся тесты, а код выхода команды был **кодом выхода сервиса `tests`** — так делают в CI.",
        ["docker compose up --abort-on-container-exit --exit-code-from tests",
         anyorder("docker compose up", ["--abort-on-container-exit", "--exit-code-from tests"], ""),
         "docker compose up --exit-code-from tests"],
        hint="`--exit-code-from сервис` (он же включает `--abort-on-container-exit`)."),
    cmd(f"{P}-stand-e3", "Стенд поднят. Запусти **одноразовый** контейнер сервиса `tests` с командой `pytest -m smoke` и удали его после.",
        ["docker compose run --rm tests pytest -m smoke", r"re:docker compose run --rm tests pytest -m (smoke|'smoke'|\"smoke\")"],
        hint="`docker compose run --rm сервис команда`."),
    cod(f"{P}-stand-e4", t("""
        Так работает ожидание готовности — и `healthcheck`, и скрипты `wait-for-it`: пробуем, ждём, снова пробуем.

        Напиши функцию `wait_healthy(check, retries, interval, sleep)`:
        - вызывает `check()` (возвращает `True`/`False`) до `retries` раз;
        - после неудачной попытки (кроме последней) вызывает `sleep(interval)`;
        - если `check()` вернул `True` — вернуть номер попытки (с 1);
        - если все попытки неудачны — бросить `TimeoutError`.

        `sleep` передаётся параметром, чтобы проверка не ждала по-настоящему.
        """),
        """
        def wait_healthy(check, retries, interval, sleep):
            pass
        """,
        """
        def make(ok_on):
            calls = {"n": 0}
            def check():
                calls["n"] += 1
                return calls["n"] >= ok_on
            return check

        def test_third():
            slept = []
            assert wait_healthy(make(3), 5, 2, slept.append) == 3
            assert slept == [2, 2], f"Между попытками — sleep(interval): {slept}"

        def test_timeout():
            slept = []
            try:
                wait_healthy(make(99), 3, 1, slept.append)
            except TimeoutError:
                assert slept == [1, 1], "После последней попытки спать не нужно"
                return
            assert False, "Нужно бросить TimeoutError"
        """,
        """
        def wait_healthy(check, retries, interval, sleep):
            for attempt in range(1, retries + 1):
                if check():
                    return attempt
                if attempt < retries:
                    sleep(interval)
            raise TimeoutError(f"не дождались за {retries} попыток")
        """),
    out(f"{P}-stand-e5", "Что выведет программа? Внутри сети compose сервисы видят друг друга **по имени** и по порту контейнера, а с хоста — через `localhost` и опубликованный порт.", """
        services = {"app": {"ports": ["8080:8000"]}, "db": {}}

        def url(service, container_port, from_host):
            if from_host:
                for spec in services[service].get("ports", []):
                    host, container = spec.split(":")[-2:]
                    if int(container) == container_port:
                        return f"http://localhost:{host}"
                return None
            return f"http://{service}:{container_port}"

        print(url("app", 8000, from_host=False))
        print(url("app", 8000, from_host=True))
        print(url("db", 5432, from_host=True))
        """),
    cod(f"{P}-stand-e6", t("""
        Напиши функцию `base_url(services, service, port, from_host)` — адрес сервиса для автотестов:

        - тесты **в контейнере** той же сети (`from_host=False`) → `"http://<service>:<port>"`;
        - тесты **на хосте** (`from_host=True`) → `"http://localhost:<порт хоста>"`, где порт хоста берётся из `ports` сервиса по порту контейнера `port`; если порт не опубликован — `None`.

        Порты в `ports` — строки `"8080:8000"` или `"127.0.0.1:8080:8000"`.
        """),
        """
        def base_url(services, service, port, from_host):
            pass
        """,
        """
        S = {"app": {"ports": ["127.0.0.1:8080:8000", "9090:9000"]}, "db": {}}

        def test_inside():
            assert base_url(S, "app", 8000, False) == "http://app:8000"
            assert base_url(S, "db", 5432, False) == "http://db:5432"

        def test_host():
            assert base_url(S, "app", 8000, True) == "http://localhost:8080", base_url(S, "app", 8000, True)
            assert base_url(S, "app", 9000, True) == "http://localhost:9090"
            assert base_url(S, "db", 5432, True) is None, "Порт не опубликован — None"
        """,
        """
        def base_url(services, service, port, from_host):
            if not from_host:
                return f"http://{service}:{port}"
            for spec in services.get(service, {}).get("ports", []):
                host, container = spec.split(":")[-2:]
                if int(container) == port:
                    return f"http://localhost:{host}"
            return None
        """),
    cmd(f"{P}-stand-e7", "Открой консоль `psql` от пользователя `postgres` внутри запущенного сервиса `db`.",
        ["docker compose exec db psql -U postgres", "docker-compose exec db psql -U postgres"],
        hint="`docker compose exec сервис команда`."),
    cmd(f"{P}-stand-e8", "Ты поменял код тестов. Подними стенд в фоне, **пересобрав** образы перед запуском.",
        ["docker compose up -d --build", "docker compose up --build -d", "docker compose up --build --detach", "docker compose up --detach --build"],
        hint="Флаг `--build`."),
),

lesson(f"{P}-practice", "Практика: стенд для автотестов",
    cod(f"{P}-practice-e1", t("""
        Собери полный стенд — `COMPOSE` из трёх сервисов:

        - `db`: `postgres:16`, `POSTGRES_PASSWORD: secret`, healthcheck `["CMD", "pg_isready", "-U", "postgres"]`;
        - `app`: `image: shop-app:1.0`, порт `"8000:8000"`, `depends_on: {db: {condition: service_healthy}}`;
        - `tests`: `build: .`, переменная `BASE_URL: http://app:8000`, том `./reports:/app/reports`, `depends_on: [app]`.
        """),
        '''
        COMPOSE = """
        services:
        """
        ''',
        """
        import yaml

        def services():
            data = yaml.safe_load(COMPOSE) or {}
            return data.get("services") or {}

        def env_of(service):
            env = service.get("environment") or {}
            return dict(i.split("=", 1) for i in env) if isinstance(env, list) else env

        def test_db():
            db = services().get("db") or {}
            assert db.get("image") == "postgres:16" and env_of(db).get("POSTGRES_PASSWORD") == "secret", "db: postgres:16 и POSTGRES_PASSWORD"
            assert (db.get("healthcheck") or {}).get("test") == ["CMD", "pg_isready", "-U", "postgres"], "db: healthcheck"

        def test_app():
            app = services().get("app") or {}
            assert app.get("image") == "shop-app:1.0" and app.get("ports") == ["8000:8000"], "app: образ и порт"
            assert ((app.get("depends_on") or {}).get("db") or {}).get("condition") == "service_healthy", "app ждёт здоровую db"

        def test_tests():
            tests = services().get("tests") or {}
            assert tests.get("build") == "." and env_of(tests).get("BASE_URL") == "http://app:8000", "tests: build и BASE_URL"
            assert tests.get("volumes") == ["./reports:/app/reports"], "tests: том для отчётов"
            dep = tests.get("depends_on")
            assert dep == ["app"] or (isinstance(dep, dict) and "app" in dep), "tests: depends_on app"
        """,
        '''
        COMPOSE = """
        services:
          db:
            image: postgres:16
            environment:
              POSTGRES_PASSWORD: secret
            healthcheck:
              test: ["CMD", "pg_isready", "-U", "postgres"]
              interval: 2s
              retries: 10
          app:
            image: shop-app:1.0
            ports:
              - "8000:8000"
            depends_on:
              db:
                condition: service_healthy
          tests:
            build: .
            environment:
              BASE_URL: http://app:8000
            volumes:
              - ./reports:/app/reports
            depends_on:
              - app
        """
        ''', xp=25),
    cod(f"{P}-practice-e2", t("""
        Стенд упал в CI — нужен быстрый диагноз. Напиши функцию `diagnose(statuses, logs)`:

        - `statuses` — словарь `{сервис: статус}`, статусы как в `docker compose ps`: `"running"`, `"running (unhealthy)"`, `"exited (0)"`, `"exited (1)"`, `"exited (137)"`;
        - `logs` — словарь `{сервис: текст лога}`.

        Верни список проблем по сервисам **в алфавитном порядке**:
        - `exited (137)` → `"<сервис>: убит (не хватило памяти?)"`;
        - `exited (N)`, N ≠ 0, и в логе есть `Traceback` → `"<сервис>: ошибка в коде"`;
        - другой ненулевой `exited (N)` → `"<сервис>: код выхода N"`;
        - `(unhealthy)` → `"<сервис>: не прошёл healthcheck"`.

        Здоровые сервисы и `exited (0)` в список не попадают.
        """),
        """
        def diagnose(statuses, logs):
            pass
        """,
        """
        def test_diagnose():
            statuses = {"tests": "exited (1)", "app": "exited (137)", "db": "running (unhealthy)", "cache": "running", "migrate": "exited (0)", "worker": "exited (2)"}
            logs = {"tests": "collected 10 items\\nTraceback (most recent call last):", "worker": "bad config"}
            assert diagnose(statuses, logs) == [
                "app: убит (не хватило памяти?)",
                "db: не прошёл healthcheck",
                "tests: ошибка в коде",
                "worker: код выхода 2",
            ], diagnose(statuses, logs)

        def test_ok():
            assert diagnose({"db": "running", "job": "exited (0)"}, {}) == []
        """,
        """
        import re


        def diagnose(statuses, logs):
            problems = []
            for name in sorted(statuses):
                status = statuses[name]
                m = re.match(r"exited \\((\\d+)\\)", status)
                if m and m.group(1) != "0":
                    code = int(m.group(1))
                    if code == 137:
                        problems.append(f"{name}: убит (не хватило памяти?)")
                    elif "Traceback" in logs.get(name, ""):
                        problems.append(f"{name}: ошибка в коде")
                    else:
                        problems.append(f"{name}: код выхода {code}")
                elif "(unhealthy)" in status:
                    problems.append(f"{name}: не прошёл healthcheck")
            return problems
        """, xp=20),
    cmd(f"{P}-practice-e3", "Контейнер `tests` завершился, а отчёт остался внутри него в `/app/reports`. Скопируй эту папку в текущую директорию хоста.",
        ["docker cp tests:/app/reports .", "docker cp tests:/app/reports ./", "docker cp tests:/app/reports ./reports", "docker compose cp tests:/app/reports ."],
        hint="`docker cp контейнер:путь куда`."),
    out(f"{P}-practice-e4", "Что выведет программа? Итог прогона стенда — по кодам выхода всех одноразовых сервисов.", """
        exits = {"migrate": 0, "api-tests": 0, "ui-tests": 1}
        failed = [name for name, code in exits.items() if code != 0]
        print("упали:", ", ".join(failed) or "никто")
        print("код для CI:", 1 if failed else 0)
        """),
    cod(f"{P}-practice-e5", t("""
        Напиши функцию `compose_cmd(files, profile, services)` — аргументы для `subprocess.run`, чтобы поднять стенд:

        ```
        ["docker", "compose", "-f", файл1, "-f", файл2, …, "--profile", profile, "up", "-d", *services]
        ```
        - `files` — список compose-файлов (последующие переопределяют предыдущие);
        - `profile` — профиль или `None` (тогда `--profile` не добавляется);
        - `services` — какие сервисы поднять (пустой список — все).
        """),
        """
        def compose_cmd(files, profile, services):
            pass
        """,
        """
        def test_full():
            got = compose_cmd(["docker-compose.yml", "docker-compose.ci.yml"], "ui", ["app", "tests"])
            assert got == ["docker", "compose", "-f", "docker-compose.yml", "-f", "docker-compose.ci.yml", "--profile", "ui", "up", "-d", "app", "tests"], got

        def test_minimal():
            assert compose_cmd(["docker-compose.yml"], None, []) == ["docker", "compose", "-f", "docker-compose.yml", "up", "-d"]
        """,
        """
        def compose_cmd(files, profile, services):
            cmd = ["docker", "compose"]
            for f in files:
                cmd += ["-f", f]
            if profile:
                cmd += ["--profile", profile]
            return cmd + ["up", "-d", *services]
        """),
    cmd(f"{P}-practice-e6", "Подними стенд в фоне из **двух** файлов: базового `docker-compose.yml` и надстройки для CI `docker-compose.ci.yml`.",
        ["docker compose -f docker-compose.yml -f docker-compose.ci.yml up -d", "docker compose -f docker-compose.yml -f docker-compose.ci.yml up --detach"],
        hint="Флаг `-f` повторяется для каждого файла, порядок важен."),
    cmd(f"{P}-practice-e7", "Подними в фоне сервисы с профилем `ui` (например, браузерные тесты, которые по умолчанию не стартуют).",
        ["docker compose --profile ui up -d", "docker compose --profile ui up --detach"],
        hint="`--profile имя` до `up`."),
    cmd(f"{P}-practice-e8", "После прогона в CI убери за собой всё: контейнеры, **тома** и контейнеры-«сироты» от удалённых из файла сервисов.",
        ["docker compose down -v --remove-orphans", "docker compose down --remove-orphans -v", "docker compose down --volumes --remove-orphans", "docker compose down --remove-orphans --volumes"],
        hint="`down` + `-v` + `--remove-orphans`."),
),
)
