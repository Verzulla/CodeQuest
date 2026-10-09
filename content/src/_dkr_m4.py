"""Тема «Docker для тестировщика», модуль 4 «Docker на практике» — задания. Теория — в _dkr_t4.py.

Docker Hub, образ изнутри и свой образ, Docker в Docker, Docker в CI. Docker в песочнице не запустить:
практика — команды («Терминал»), утилиты на Python и файлы (Dockerfile, CI-конфиги) строкой."""
from textwrap import dedent

from ._lib import cmd, cod, lesson, module, out, t
from ._dkr_m1 import anyorder
from ._dkr_m2 import DF_PARSE

P = "dkr"

# Разбор YAML в проверках (pyyaml есть в песочнице); «on:» PyYAML читает как True — возвращаем "on".
YML = '''import yaml


def load(text):
    data = yaml.safe_load(text) or {}
    if True in data:
        data["on"] = data.pop(True)
    return data
'''

SOCK = "-v /var/run/docker.sock:/var/run/docker.sock"

m4 = module(f"{P}-m4", "Docker на практике", "🚢", "Docker Hub, образ изнутри и свой образ для автотестов, Docker в Docker, Docker в CI-пайплайне",

lesson(f"{P}-hub", "Docker Hub и выбор образа",
    out(f"{P}-hub-e1", "Что выведет программа? Как Docker дописывает короткие имена образов.", """
            def full_name(ref):
                if "/" not in ref:
                    ref = "library/" + ref
                first = ref.split("/")[0]
                if "." not in first and ":" not in first and first != "localhost":
                    ref = "docker.io/" + ref
                if ":" not in ref.split("/")[-1]:
                    ref += ":latest"
                return ref

            for ref in ["python:3.12-slim", "anna/my-tests", "ghcr.io/acme/tests:1.0"]:
                print(full_name(ref))
            """),
    cod(f"{P}-hub-e2", t("""
            Напиши функцию `split_tag(tag)`, которая делит тег образа на версию и вариант.

            - Получает: `tag` — тег, например `"3.12-slim-bookworm"`.
            - Возвращает: кортеж `(версия, вариант)`:
              - версия — всё до **первого** дефиса;
              - вариант — всё после него; если дефиса нет — пустая строка `""`.

            Примеры:
            ```
            split_tag("3.12-slim-bookworm")   # → ("3.12", "slim-bookworm")
            split_tag("3.12-alpine")          # → ("3.12", "alpine")
            split_tag("3.12")                 # → ("3.12", "")
            split_tag("latest")               # → ("latest", "")
            ```
            """),
            """
            def split_tag(tag):
                pass
            """,
            """
            def test_variants():
                assert split_tag("3.12-slim-bookworm") == ("3.12", "slim-bookworm"), f"Получено {split_tag('3.12-slim-bookworm')}"
                assert split_tag("3.12-alpine") == ("3.12", "alpine")

            def test_plain():
                assert split_tag("3.12") == ("3.12", ""), "Без дефиса вариант — пустая строка"
                assert split_tag("latest") == ("latest", "")
            """,
            """
            def split_tag(tag):
                version, _, variant = tag.partition("-")
                return version, variant
            """,
            hint="`partition(\"-\")` делит по первому дефису и всегда возвращает три части."),
    cod(f"{P}-hub-e3", t("""
            Напиши функцию `pick_base(tags, version)`: выбрать базовый образ Python для автотестов.

            - Получает: `tags` — список доступных тегов образа `python`; `version` — нужная версия, например `"3.12"`.
            - Возвращает: тег по приоритету:
              1. `"<версия>-slim"`, если он есть;
              2. иначе просто `"<версия>"`, если он есть;
              3. иначе `None`.

            Тег `alpine` не выбираем никогда: в нём другая библиотека C, и часть пакетов не соберётся.

            Пример:
            ```
            tags = ["3.12", "3.12-slim", "3.12-alpine", "3.11-slim"]
            pick_base(tags, "3.12")      # → "3.12-slim"
            pick_base(["3.13", "3.13-alpine"], "3.13")   # → "3.13"
            pick_base(["3.12-alpine"], "3.12")           # → None
            ```
            """),
            """
            def pick_base(tags, version):
                pass
            """,
            """
            def test_slim_first():
                assert pick_base(["3.12", "3.12-slim", "3.12-alpine", "3.11-slim"], "3.12") == "3.12-slim"

            def test_plain():
                assert pick_base(["3.13", "3.13-alpine"], "3.13") == "3.13", "Нет slim — берём обычный"

            def test_no_alpine():
                assert pick_base(["3.12-alpine"], "3.12") is None, "alpine не берём"

            def test_other_version():
                assert pick_base(["3.11-slim"], "3.12") is None, "Нужна именно эта версия"
            """,
            """
            def pick_base(tags, version):
                for tag in (f"{version}-slim", version):
                    if tag in tags:
                        return tag
                return None
            """,
            hint="Перебери кандидатов по порядку: сначала `f\"{version}-slim\"`, потом `version`."),
    cod(f"{P}-hub-e4", t("""
            Напиши функцию `hub_url(ref)` — ссылка на страницу образа в Docker Hub.

            - Получает: `ref` — имя образа, возможно с тегом.
            - Возвращает:
              - официальный образ (в имени нет `/`, например `"postgres:16"`) → `"https://hub.docker.com/_/postgres"`;
              - образ пользователя (`"anna/my-tests:1.0"`) → `"https://hub.docker.com/r/anna/my-tests"`;
              - образ из другого реестра — первая часть до `/` содержит точку или двоеточие (`"ghcr.io/acme/tests"`, `"localhost:5000/app"`) → `None`.

            Тег (всё после `:` в **последней** части имени) в ссылку не входит.
            """),
            """
            def hub_url(ref):
                pass
            """,
            """
            def test_official():
                assert hub_url("postgres:16") == "https://hub.docker.com/_/postgres"
                assert hub_url("python") == "https://hub.docker.com/_/python"

            def test_user():
                assert hub_url("anna/my-tests:1.0") == "https://hub.docker.com/r/anna/my-tests"

            def test_other_registry():
                assert hub_url("ghcr.io/acme/tests:1.0") is None, "ghcr.io — не Docker Hub"
                assert hub_url("localhost:5000/app") is None, "localhost:5000 — свой реестр"
            """,
            """
            def hub_url(ref):
                parts = ref.split("/")
                if len(parts) > 1 and ("." in parts[0] or ":" in parts[0]):
                    return None
                parts[-1] = parts[-1].split(":")[0]
                if len(parts) == 1:
                    return f"https://hub.docker.com/_/{parts[0]}"
                return "https://hub.docker.com/r/" + "/".join(parts)
            """,
            hint="Сначала проверь первую часть на точку или двоеточие, потом отрежь тег у последней части.", xp=20),
    cmd(f"{P}-hub-e5", "Найди в Docker Hub образы `python`, но покажи **только официальные**.",
        ["docker search --filter is-official=true python", "docker search python --filter is-official=true",
         "docker search --filter=is-official=true python", "docker search -f is-official=true python"],
        hint="`docker search` с фильтром `--filter is-official=true`."),
    cmd(f"{P}-hub-e6", "Войди в Docker Hub как пользователь `anna`. Токен лежит в переменной `DOCKERHUB_TOKEN` — передай его через стандартный ввод, а не аргументом.",
        ['echo "$DOCKERHUB_TOKEN" | docker login -u anna --password-stdin',
         're:(echo|printf %s|printf "%s") "?\\$\\{?DOCKERHUB_TOKEN\\}?"? \\| docker login (-u anna --password-stdin|--password-stdin -u anna|--username anna --password-stdin|--password-stdin --username anna|-u anna --password-stdin docker\\.io)$'],
        hint="`echo \"$DOCKERHUB_TOKEN\" | docker login -u имя --password-stdin`."),
    cmd(f"{P}-hub-e7", "Локальный образ называется `my-tests`. Дай ему второе имя для Docker Hub: пользователь `anna`, репозиторий `my-tests`, тег `1.0`.",
        ["docker tag my-tests anna/my-tests:1.0", "docker tag my-tests:latest anna/my-tests:1.0", "docker image tag my-tests anna/my-tests:1.0"],
        hint="`docker tag старое-имя пользователь/репозиторий:тег`."),
    cmd(f"{P}-hub-e8", "Метка готова (см. вывод). Отправь образ в Docker Hub.",
        ["docker push anna/my-tests:1.0", "docker image push anna/my-tests:1.0"],
        context="""
            $ docker image ls
            REPOSITORY       TAG       IMAGE ID       SIZE
            anna/my-tests    1.0       4c1d2e3f5a6b   182MB
            my-tests         latest    4c1d2e3f5a6b   182MB
            """,
        hint="`docker push` и полное имя с тегом."),
),

lesson(f"{P}-image", "Образ изнутри и свой образ",
    out(f"{P}-image-e1", "Что выведет программа? Второй образ собран на той же базе — сколько придётся скачать?", """
            have = {"base1": 74, "base2": 3, "py": 41}       # слои первого образа на диске, МБ
            second = {"base1": 74, "base2": 3, "py": 41, "deps": 28, "tests": 1}

            new = {k: v for k, v in second.items() if k not in have}
            print(len(new), sum(new.values()))
            """),
    cod(f"{P}-image-e2", t("""
            Напиши функцию `merged_view(layers)` — что видит контейнер, если сложить слои образа.

            - Получает: `layers` — список слоёв **снизу вверх**. Каждый слой — словарь `{путь: содержимое}`; значение `None` означает «файл удалён в этом слое».
            - Возвращает: словарь файлов, которые видны в контейнере. Верхний слой перекрывает нижний; удалённых файлов в результате нет.

            Пример:
            ```
            layers = [
                {"/etc/os": "debian", "/app/old.py": "v1"},
                {"/app/old.py": None, "/app/test_api.py": "tests"},
                {"/etc/os": "debian 12"},
            ]
            merged_view(layers)
            # → {"/etc/os": "debian 12", "/app/test_api.py": "tests"}
            ```
            """),
            """
            def merged_view(layers):
                pass
            """,
            """
            LAYERS = [
                {"/etc/os": "debian", "/app/old.py": "v1"},
                {"/app/old.py": None, "/app/test_api.py": "tests"},
                {"/etc/os": "debian 12"},
            ]

            def test_merge():
                assert merged_view(LAYERS) == {"/etc/os": "debian 12", "/app/test_api.py": "tests"}, f"Получено {merged_view(LAYERS)}"

            def test_recreated():
                layers = [{"/a": "1"}, {"/a": None}, {"/a": "3"}]
                assert merged_view(layers) == {"/a": "3"}, "Файл удалили и создали снова — он есть"

            def test_input_untouched():
                layers = [{"/a": "1"}, {"/a": None}]
                merged_view(layers)
                assert layers == [{"/a": "1"}, {"/a": None}], "Слои образа только для чтения — не меняй их"
            """,
            """
            def merged_view(layers):
                files = {}
                for layer in layers:
                    for path, content in layer.items():
                        if content is None:
                            files.pop(path, None)
                        else:
                            files[path] = content
                return files
            """,
            hint="Иди по слоям снизу вверх и обновляй один общий словарь; `None` — `pop(path, None)`.", xp=20),
    cod(f"{P}-image-e3", t("""
            Напиши Dockerfile образа для автотестов — строкой в переменной `DOCKERFILE`.

            Требования:
            1. Первая инструкция — `FROM python:3.12-slim`.
            2. `ENV PYTHONUNBUFFERED=1` — вывод без буфера (можно вместе с другими переменными в одной строке `ENV`).
            3. `WORKDIR /tests`.
            4. Кэш слоёв: `COPY requirements.txt .` → `RUN pip install --no-cache-dir -r requirements.txt` → `COPY . .`.
            5. Создать пользователя (`RUN useradd ...`) и переключиться на него инструкцией `USER` — **после** установки зависимостей. Пользователь не `root`.
            6. `ENTRYPOINT ["pytest"]` — в exec-форме (JSON-список).
            7. Последняя инструкция — `CMD` с аргументами по умолчанию, например `CMD ["-v"]`.
            """),
            '''
            DOCKERFILE = """
            FROM python:3.12-slim
            """
            ''',
            DF_PARSE + dedent("""
            import json

            def _find(ins, name, start=""):
                return next((k for k, (i, a) in enumerate(ins) if i == name and a.startswith(start)), None)

            def test_from_env_workdir():
                ins = _instructions(DOCKERFILE)
                assert ins and ins[0] == ("FROM", "python:3.12-slim"), "Первая инструкция — FROM python:3.12-slim"
                assert any(i == "ENV" and "PYTHONUNBUFFERED=1" in a for i, a in ins), "Нужен ENV PYTHONUNBUFFERED=1"
                assert ("WORKDIR", "/tests") in ins, "Нужен WORKDIR /tests"

            def test_cache_order():
                ins = _instructions(DOCKERFILE)
                req, code = _find(ins, "COPY", "requirements.txt"), _find(ins, "COPY", ". ")
                pip = next((k for k, (i, a) in enumerate(ins) if i == "RUN" and "pip install" in a), None)
                assert None not in (req, pip, code), "Нужны COPY requirements.txt, RUN pip install и COPY . ."
                assert "--no-cache-dir" in ins[pip][1], "pip install с --no-cache-dir"
                assert req < pip < code, "Порядок: COPY requirements.txt → pip install → COPY . ."

            def test_user():
                ins = _instructions(DOCKERFILE)
                pip = next(k for k, (i, a) in enumerate(ins) if i == "RUN" and "pip install" in a)
                user = _find(ins, "USER")
                assert any(i == "RUN" and "useradd" in a for i, a in ins), "Создай пользователя: RUN useradd ..."
                assert user is not None and ins[user][1] not in ("root", "0"), "Нужен USER — не root"
                assert user > pip, "USER — после установки зависимостей"

            def test_entrypoint_cmd():
                ins = _instructions(DOCKERFILE)
                ep = _find(ins, "ENTRYPOINT")
                assert ep is not None and json.loads(ins[ep][1]) == ["pytest"], 'Нужен ENTRYPOINT ["pytest"] в exec-форме'
                assert ins[-1][0] == "CMD" and ins[-1][1].startswith("["), 'Последняя — CMD в exec-форме, например CMD ["-v"]'
            """),
            '''
            DOCKERFILE = """
            FROM python:3.12-slim
            ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
            WORKDIR /tests
            COPY requirements.txt .
            RUN pip install --no-cache-dir -r requirements.txt
            COPY . .
            RUN useradd --create-home tester
            USER tester
            ENTRYPOINT ["pytest"]
            CMD ["-v"]
            """
            ''',
            hint="Порядок: FROM, ENV, WORKDIR, COPY requirements.txt, RUN pip, COPY . ., RUN useradd, USER, ENTRYPOINT, CMD.", xp=25),
    cod(f"{P}-image-e4", t("""
            Напиши функцию `run_command(entrypoint, cmd, args=None, override=None)` — какую команду выполнит контейнер.

            - Получает:
              - `entrypoint`, `cmd` — списки из образа (`ENTRYPOINT` и `CMD`);
              - `args` — аргументы после имени образа в `docker run` (список или `None`);
              - `override` — значение флага `--entrypoint` (строка или `None`).
            - Возвращает: список — итоговую команду.

            Правила Docker:
            - если задан `override`, он заменяет `ENTRYPOINT`, а `CMD` образа **сбрасывается**: результат — `[override] + (args or [])`;
            - иначе — `entrypoint + args`, если `args` переданы (не пустые), и `entrypoint + cmd`, если нет.

            Примеры:
            ```
            run_command(["pytest"], ["-v"])                      # → ["pytest", "-v"]
            run_command(["pytest"], ["-v"], ["-m", "smoke"])     # → ["pytest", "-m", "smoke"]
            run_command(["pytest"], ["-v"], override="bash")     # → ["bash"]
            run_command(["pytest"], ["-v"], ["-c", "ls"], "sh")  # → ["sh", "-c", "ls"]
            ```
            """),
            """
            def run_command(entrypoint, cmd, args=None, override=None):
                pass
            """,
            """
            def test_default():
                assert run_command(["pytest"], ["-v"]) == ["pytest", "-v"]

            def test_args_replace_cmd():
                assert run_command(["pytest"], ["-v"], ["-m", "smoke"]) == ["pytest", "-m", "smoke"], "Аргументы заменяют CMD"

            def test_override_resets_cmd():
                assert run_command(["pytest"], ["-v"], override="bash") == ["bash"], "--entrypoint сбрасывает CMD образа"
                assert run_command(["pytest"], ["-v"], ["-c", "ls"], "sh") == ["sh", "-c", "ls"]
            """,
            """
            def run_command(entrypoint, cmd, args=None, override=None):
                if override is not None:
                    return [override] + (args or [])
                return entrypoint + (args if args else cmd)
            """,
            hint="Сначала проверь `override`; потом `entrypoint + (args if args else cmd)`."),
    out(f"{P}-image-e5", "Что выведет программа? Часть вывода `docker image inspect` — что запустится по умолчанию и от чьего имени.", """
            config = {
                "Env": ["PATH=/usr/local/bin:/usr/bin", "PYTHONUNBUFFERED=1"],
                "WorkingDir": "/tests",
                "User": "tester",
                "Entrypoint": ["pytest"],
                "Cmd": ["-v"],
            }
            env = dict(item.split("=", 1) for item in config["Env"])
            print(" ".join(config["Entrypoint"] + config["Cmd"]))
            print(config["User"] or "root", env["PYTHONUNBUFFERED"])
            """),
    cmd(f"{P}-image-e6", "Покажи полную информацию об образе `my-tests`: конфигурацию (ENTRYPOINT, CMD, ENV, USER) и список слоёв в JSON.",
        ["docker image inspect my-tests", "docker inspect my-tests"],
        hint="`docker image inspect образ`."),
    cmd(f"{P}-image-e7", "В образе `my-tests` — `ENTRYPOINT [\"pytest\"]`. Запусти контейнер так, чтобы прогнались только тесты с маркером `smoke`, а контейнер удалился после работы.",
        ["docker run --rm my-tests -m smoke", "docker container run --rm my-tests -m smoke"],
        hint="Аргументы после имени образа дописываются к ENTRYPOINT: `docker run --rm образ -m smoke`."),
    cmd(f"{P}-image-e8", "На стенде нет доступа к реестру. Сохрани образ `my-tests:1.0` в файл `my-tests.tar`, чтобы перенести его вручную.",
        ["docker save -o my-tests.tar my-tests:1.0", "docker save my-tests:1.0 -o my-tests.tar", "docker save --output my-tests.tar my-tests:1.0",
         "docker save my-tests:1.0 > my-tests.tar", "docker image save -o my-tests.tar my-tests:1.0"],
        hint="`docker save -o файл.tar образ`; на другой машине — `docker load -i файл.tar`."),
),

lesson(f"{P}-dind", "Docker в Docker",
    out(f"{P}-dind-e1", "Что выведет программа? CI-job работает в контейнере с проброшенным docker.sock и запускает `docker run -v /builds/app/reports:/reports ...`. Чей путь проверит демон?", """
            job_dirs = {"/builds/app", "/builds/app/reports"}      # папки внутри контейнера CI-job
            host_dirs = {"/home/runner", "/var/lib/docker"}         # папки на хосте

            mount = "/builds/app/reports"
            daemon_sees = mount in host_dirs     # путь из -v читает демон — а он на хосте
            print(mount in job_dirs, daemon_sees)
            print("отчёты на месте" if daemon_sees else "Docker создаст пустую папку на хосте")
            """),
    cod(f"{P}-dind-e2", t("""
            Напиши функцию `docker_access(command)`: как контейнер получит доступ к Docker.

            - Получает: `command` — строку команды `docker run ...`.
            - Возвращает:
              - `"socket"`, если в команде есть проброс сокета `-v /var/run/docker.sock:/var/run/docker.sock`;
              - `"dind"`, если есть флаг `--privileged` и образ (слово, которое начинается с `docker:`) заканчивается на `dind`;
              - `"none"` — иначе.

            Примеры:
            ```
            docker_access("docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker:27 docker ps")  # → "socket"
            docker_access("docker run -d --privileged --name dind docker:27-dind")                            # → "dind"
            docker_access("docker run -d docker:27-dind")                                                     # → "none"
            ```
            """),
            """
            def docker_access(command):
                pass
            """,
            """
            def test_socket():
                assert docker_access("docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker:27 docker ps") == "socket"

            def test_dind():
                assert docker_access("docker run -d --privileged --name dind docker:27-dind") == "dind"

            def test_dind_needs_privileged():
                assert docker_access("docker run -d docker:27-dind") == "none", "Без --privileged DinD не заработает"

            def test_plain():
                assert docker_access("docker run --rm --privileged python:3.12-slim") == "none"
            """,
            """
            def docker_access(command):
                words = command.split()
                if "/var/run/docker.sock:/var/run/docker.sock" in words:
                    return "socket"
                image = next((w for w in words if w.startswith("docker:")), "")
                if "--privileged" in words and image.endswith("dind"):
                    return "dind"
                return "none"
            """,
            hint="Разбей строку на слова: `command.split()`; образ — слово, которое начинается с `docker:`."),
    cod(f"{P}-dind-e3", t("""
            Напиши функцию `risky_services(services)` — ревью docker-compose на опасные настройки.

            - Получает: `services` — словарь сервисов из compose: `{имя: настройки}`. В настройках могут быть ключи `volumes` (список строк `"откуда:куда"`) и `privileged` (bool).
            - Возвращает: **отсортированный** по имени список пар `(имя, причина)`:
              - `"docker.sock"` — если хотя бы один том начинается с `/var/run/docker.sock`;
              - `"privileged"` — если `privileged` равен `True`.

              У одного сервиса могут быть обе причины — тогда две пары (сначала `docker.sock`).

            Пример:
            ```
            services = {
                "tests": {"volumes": ["./reports:/tests/reports"]},
                "runner": {"volumes": ["/var/run/docker.sock:/var/run/docker.sock"]},
                "dind": {"privileged": True},
            }
            risky_services(services)   # → [("dind", "privileged"), ("runner", "docker.sock")]
            ```
            """),
            """
            def risky_services(services):
                pass
            """,
            """
            def test_review():
                services = {
                    "tests": {"volumes": ["./reports:/tests/reports"]},
                    "runner": {"volumes": ["/var/run/docker.sock:/var/run/docker.sock"]},
                    "dind": {"privileged": True},
                }
                assert risky_services(services) == [("dind", "privileged"), ("runner", "docker.sock")], f"Получено {risky_services(services)}"

            def test_both():
                services = {"bad": {"privileged": True, "volumes": ["/var/run/docker.sock:/var/run/docker.sock:ro"]}}
                assert risky_services(services) == [("bad", "docker.sock"), ("bad", "privileged")]

            def test_clean():
                assert risky_services({"db": {"image": "postgres:16"}, "app": {"privileged": False}}) == []
            """,
            """
            def risky_services(services):
                found = []
                for name in sorted(services):
                    cfg = services[name]
                    if any(v.startswith("/var/run/docker.sock") for v in cfg.get("volumes", [])):
                        found.append((name, "docker.sock"))
                    if cfg.get("privileged") is True:
                        found.append((name, "privileged"))
                return found
            """,
            hint="Перебирай `sorted(services)`; `cfg.get(\"volumes\", [])` — пустой список, если ключа нет.", xp=20),
    cod(f"{P}-dind-e4", t("""
            Напиши job GitLab CI, который собирает образ через DinD, — строкой YAML в переменной `GITLAB_CI`.

            Job называется `build-image`, у него:
            - `image: docker:27` — образ с клиентом docker;
            - `services` со списком из одного элемента `docker:27-dind`;
            - `variables`: `DOCKER_HOST: tcp://docker:2376` и `DOCKER_TLS_CERTDIR: "/certs"`;
            - `script` — список команд, среди них сборка `docker build -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA" .` и отправка `docker push "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"` — именно в таком порядке.

            Проверки разберут YAML и посмотрят на структуру.
            """),
            '''
            GITLAB_CI = """
            build-image:
              image: docker:27
            """
            ''',
            YML + dedent("""

            def job():
                data = load(GITLAB_CI)
                assert "build-image" in data, "Нужен job build-image"
                return data["build-image"]

            def test_image_and_service():
                j = job()
                assert j.get("image") == "docker:27", "image: docker:27"
                assert j.get("services") == ["docker:27-dind"], "services: [docker:27-dind]"

            def test_variables():
                v = job().get("variables", {})
                assert v.get("DOCKER_HOST") == "tcp://docker:2376", "DOCKER_HOST: tcp://docker:2376"
                assert v.get("DOCKER_TLS_CERTDIR") == "/certs", 'DOCKER_TLS_CERTDIR: "/certs"'

            def test_script():
                script = job().get("script", [])
                build = next((k for k, s in enumerate(script) if s.startswith("docker build") and "$CI_COMMIT_SHA" in s), None)
                push = next((k for k, s in enumerate(script) if s.startswith("docker push") and "$CI_COMMIT_SHA" in s), None)
                assert build is not None, "Нужен docker build с тегом $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"
                assert push is not None, "Нужен docker push того же тега"
                assert build < push, "Сначала build, потом push"
            """),
            '''
            GITLAB_CI = """
            build-image:
              image: docker:27
              services:
                - docker:27-dind
              variables:
                DOCKER_HOST: tcp://docker:2376
                DOCKER_TLS_CERTDIR: "/certs"
              script:
                - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
                - docker build -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA" .
                - docker push "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"
            """
            ''',
            hint="Ключи job-а: image, services (список), variables (словарь), script (список строк).", xp=25),
    cod(f"{P}-dind-e5", t("""
            Напиши функцию `parse_docker_host(value)` — разобрать значение переменной `DOCKER_HOST`.

            - Получает: `value` — строку или `None` (переменная не задана).
            - Возвращает словарь:
              - `None` или пустая строка → `{"kind": "unix", "path": "/var/run/docker.sock"}` (сокет по умолчанию);
              - `"unix:///путь"` → `{"kind": "unix", "path": "/путь"}`;
              - `"tcp://хост:порт"` → `{"kind": "tcp", "host": хост, "port": порт (int), "tls": порт == 2376}`.

            Примеры:
            ```
            parse_docker_host(None)                    # → {"kind": "unix", "path": "/var/run/docker.sock"}
            parse_docker_host("tcp://docker:2376")     # → {"kind": "tcp", "host": "docker", "port": 2376, "tls": True}
            parse_docker_host("tcp://dind:2375")       # → {"kind": "tcp", "host": "dind", "port": 2375, "tls": False}
            ```
            """),
            """
            def parse_docker_host(value):
                pass
            """,
            """
            def test_default():
                assert parse_docker_host(None) == {"kind": "unix", "path": "/var/run/docker.sock"}
                assert parse_docker_host("") == {"kind": "unix", "path": "/var/run/docker.sock"}

            def test_unix():
                assert parse_docker_host("unix:///run/user/1000/docker.sock") == {"kind": "unix", "path": "/run/user/1000/docker.sock"}

            def test_tcp():
                assert parse_docker_host("tcp://docker:2376") == {"kind": "tcp", "host": "docker", "port": 2376, "tls": True}
                assert parse_docker_host("tcp://dind:2375") == {"kind": "tcp", "host": "dind", "port": 2375, "tls": False}
            """,
            """
            def parse_docker_host(value):
                if not value:
                    return {"kind": "unix", "path": "/var/run/docker.sock"}
                if value.startswith("unix://"):
                    return {"kind": "unix", "path": value[len("unix://"):]}
                host, _, port = value[len("tcp://"):].rpartition(":")
                return {"kind": "tcp", "host": host, "port": int(port), "tls": int(port) == 2376}
            """,
            hint="`unix://` — 7 символов, после них путь; для tcp раздели `хост:порт` через `rpartition(\":\")`."),
    cmd(f"{P}-dind-e6", "Запусти одноразовый контейнер из образа `docker:27` с проброшенным сокетом Docker хоста и выполни в нём `docker ps`.",
        [f"docker run --rm {SOCK} docker:27 docker ps", anyorder("docker run", ["--rm", SOCK], "docker:27 docker ps"),
         anyorder("docker run", ["--rm", SOCK.replace("-v ", "--volume ")], "docker:27 docker ps")],
        hint="Флаги `--rm` и `-v /var/run/docker.sock:/var/run/docker.sock`, потом образ и команда."),
    cmd(f"{P}-dind-e7", "Запусти в фоне настоящий DinD: контейнер с именем `dind` из образа `docker:27-dind` со всеми нужными ему правами.",
        ["docker run -d --privileged --name dind docker:27-dind", anyorder("docker run", ["-d", "--privileged", "--name dind"], "docker:27-dind"),
         anyorder("docker run", ["--detach", "--privileged", "--name dind"], "docker:27-dind")],
        hint="Флаги `-d`, `--privileged`, `--name dind`, затем образ."),
    cmd(f"{P}-dind-e8", "Какая переменная окружения говорит клиенту `docker`, к какому демону подключаться? Введи её имя.",
        ["DOCKER_HOST", "re:(?i)\\$?docker_host"],
        hint="Её задают в GitLab: `tcp://docker:2376`."),
),

lesson(f"{P}-ci", "Docker в CI на практике",
    out(f"{P}-ci-e1", "Что выведет программа? Какими тегами CI пометит образ после push в ветку.", """
            image = "ghcr.io/acme/shop-tests"
            sha = "3f2a1b9c8d7e6f5a4b3c"
            branch = "feature/login-form"

            tags = [sha[:7], branch.replace("/", "-")]
            for tag in tags:
                print(f"{image}:{tag}")
            """),
    cod(f"{P}-ci-e2", t("""
            Напиши функцию `image_tags(sha, branch, git_tag=None)` — список тегов образа для CI.

            - Получает: `sha` — полный хеш коммита; `branch` — имя ветки; `git_tag` — git-тег релиза вида `"v1.4.2"` или `None`.
            - Возвращает список тегов по порядку:
              1. первые 7 символов `sha`;
              2. имя ветки, где `/` заменён на `-`;
              3. если есть `git_tag`: версия без `v` (`"1.4.2"`), затем `MAJOR.MINOR` (`"1.4"`), затем `"latest"`.

            Пример:
            ```
            image_tags("3f2a1b9c8d7e", "feature/login")
            # → ["3f2a1b9", "feature-login"]
            image_tags("9e8d7c6b5a49", "main", "v1.4.2")
            # → ["9e8d7c6", "main", "1.4.2", "1.4", "latest"]
            ```
            """),
            """
            def image_tags(sha, branch, git_tag=None):
                pass
            """,
            """
            def test_branch():
                assert image_tags("3f2a1b9c8d7e", "feature/login") == ["3f2a1b9", "feature-login"], f"Получено {image_tags('3f2a1b9c8d7e', 'feature/login')}"

            def test_release():
                assert image_tags("9e8d7c6b5a49", "main", "v1.4.2") == ["9e8d7c6", "main", "1.4.2", "1.4", "latest"]

            def test_no_slash():
                assert all("/" not in t for t in image_tags("a" * 40, "release/2.0/hotfix")), "В теге не может быть /"
            """,
            """
            def image_tags(sha, branch, git_tag=None):
                tags = [sha[:7], branch.replace("/", "-")]
                if git_tag:
                    version = git_tag.removeprefix("v")
                    major_minor = ".".join(version.split(".")[:2])
                    tags += [version, major_minor, "latest"]
                return tags
            """,
            hint="`git_tag.removeprefix(\"v\")`, а `MAJOR.MINOR` — первые две части `split(\".\")`."),
    cod(f"{P}-ci-e3", t("""
            Напиши workflow GitHub Actions «собрать образ → прогнать тесты в нём» — строкой YAML в переменной `WORKFLOW`.

            Требования:
            - job `build`:
              - `permissions` с `packages: write`;
              - шаг с `uses: docker/build-push-action@v6` (версия — любая), у которого в `with` есть `push: true` и `tags`, содержащий `${{ github.sha }}`.
            - job `api-tests`:
              - `needs: build` (строкой или списком);
              - шаг `run`, в котором есть `docker run` и тот же образ с `${{ github.sha }}`;
              - шаг `uses: actions/upload-artifact@v4` с условием `if: always()`.

            Кроме этого, в workflow нужен ключ `on` (например, `on: [push]`), а у job-ов — `runs-on`. Логин в реестр и checkout можно добавить, проверки их не требуют.
            """),
            '''
            WORKFLOW = """
            on: [push]
            jobs:
              build:
                runs-on: ubuntu-latest
            """
            ''',
            YML + dedent("""

            def jobs():
                data = load(WORKFLOW)
                assert "on" in data, "Нужен ключ on"
                return data.get("jobs", {})

            def test_build():
                b = jobs().get("build")
                assert b, "Нужен job build"
                assert b.get("permissions", {}).get("packages") == "write", "permissions: packages: write"
                step = next((s for s in b.get("steps", []) if str(s.get("uses", "")).startswith("docker/build-push-action")), None)
                assert step, "Нужен шаг docker/build-push-action"
                w = step.get("with", {})
                assert w.get("push") is True, "with: push: true"
                assert "${{ github.sha }}" in str(w.get("tags", "")), "tags с ${{ github.sha }}"

            def test_tests_job():
                t = jobs().get("api-tests")
                assert t, "Нужен job api-tests"
                needs = t.get("needs")
                assert needs == "build" or needs == ["build"], "api-tests: needs: build"
                runs = [s.get("run", "") for s in t.get("steps", [])]
                assert any("docker run" in r and "${{ github.sha }}" in r for r in runs), "Шаг run с docker run образа ${{ github.sha }}"

            def test_artifact():
                t = jobs().get("api-tests", {})
                up = next((s for s in t.get("steps", []) if str(s.get("uses", "")).startswith("actions/upload-artifact")), None)
                assert up, "Нужен шаг actions/upload-artifact"
                assert "always()" in str(up.get("if", "")), "if: always() — отчёт и при падении"
            """),
            '''
            WORKFLOW = """
            on: [push]
            jobs:
              build:
                runs-on: ubuntu-latest
                permissions:
                  contents: read
                  packages: write
                steps:
                  - uses: actions/checkout@v4
                  - uses: docker/login-action@v3
                    with:
                      registry: ghcr.io
                      username: ${{ github.actor }}
                      password: ${{ secrets.GITHUB_TOKEN }}
                  - uses: docker/build-push-action@v6
                    with:
                      push: true
                      tags: ghcr.io/acme/shop-tests:${{ github.sha }}
              api-tests:
                needs: build
                runs-on: ubuntu-latest
                steps:
                  - uses: docker/login-action@v3
                    with:
                      registry: ghcr.io
                      username: ${{ github.actor }}
                      password: ${{ secrets.GITHUB_TOKEN }}
                  - run: docker run --rm -v "$PWD/reports:/tests/reports" ghcr.io/acme/shop-tests:${{ github.sha }} --junitxml=reports/junit.xml
                  - uses: actions/upload-artifact@v4
                    if: always()
                    with:
                      name: api-report
                      path: reports/
            """
            ''',
            hint="Два job-а; у build — permissions и build-push-action, у api-tests — needs, docker run и upload-artifact с if: always().", xp=30),
    cod(f"{P}-ci-e4", t("""
            Напиши `.gitlab-ci.yml` из двух этапов — строкой YAML в переменной `GITLAB_CI`.

            Требования:
            - `stages: [build, test]`;
            - job `build` со `stage: build`, в его `script` есть `docker push` с `$CI_COMMIT_SHA`;
            - job `api-tests` со `stage: test`:
              - `image: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA` — тесты идут прямо в собранном образе;
              - в `script` есть команда с `pytest` и `--junitxml=report.xml`;
              - `artifacts`: `when: always` и `reports: junit: report.xml`.
            """),
            '''
            GITLAB_CI = """
            stages: [build, test]
            """
            ''',
            YML + dedent("""

            def test_stages():
                assert load(GITLAB_CI).get("stages") == ["build", "test"], "stages: [build, test]"

            def test_build():
                b = load(GITLAB_CI).get("build", {})
                assert b.get("stage") == "build", "У build — stage: build"
                assert any(s.startswith("docker push") and "$CI_COMMIT_SHA" in s for s in b.get("script", [])), "В build нужен docker push образа с $CI_COMMIT_SHA"

            def test_tests():
                t = load(GITLAB_CI).get("api-tests", {})
                assert t.get("stage") == "test", "У api-tests — stage: test"
                assert t.get("image") == "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA", "image: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"
                assert any("pytest" in s and "--junitxml=report.xml" in s for s in t.get("script", [])), "pytest --junitxml=report.xml"

            def test_artifacts():
                a = load(GITLAB_CI).get("api-tests", {}).get("artifacts", {})
                assert a.get("when") == "always", "artifacts: when: always"
                assert a.get("reports", {}).get("junit") == "report.xml", "artifacts: reports: junit: report.xml"
            """),
            '''
            GITLAB_CI = """
            stages: [build, test]

            build:
              stage: build
              image: docker:27
              services: [docker:27-dind]
              variables:
                DOCKER_HOST: tcp://docker:2376
                DOCKER_TLS_CERTDIR: "/certs"
              script:
                - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
                - docker build -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA" .
                - docker push "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"

            api-tests:
              stage: test
              image: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
              script:
                - pytest --junitxml=report.xml
              artifacts:
                when: always
                reports:
                  junit: report.xml
            """
            ''',
            hint="Job-ы — ключи верхнего уровня рядом со `stages`; у api-tests `image` — только что собранный образ.", xp=25),
    cod(f"{P}-ci-e5", t("""
            Напиши функцию `promote(registry, sha, new_tag)` — промоутинг образа после зелёных тестов.

            - Получает:
              - `registry` — словарь «тег → дайджест», например `{"3f2a1b9": "sha256:aa…"}`;
              - `sha` — тег, который прошёл тесты; `new_tag` — новый тег (`"stable"`, `"1.4.2"`).
            - Возвращает: **новый** словарь, где `new_tag` указывает на **тот же дайджест**, что и `sha`. Исходный словарь не меняй.
            - Если тега `sha` нет — выбрось `KeyError`: продвигать нечего.

            Пример:
            ```
            reg = {"3f2a1b9": "sha256:aa11", "stable": "sha256:0ld0"}
            promote(reg, "3f2a1b9", "stable")
            # → {"3f2a1b9": "sha256:aa11", "stable": "sha256:aa11"}
            ```
            """),
            """
            def promote(registry, sha, new_tag):
                pass
            """,
            """
            import pytest

            def test_promote():
                reg = {"3f2a1b9": "sha256:aa11", "stable": "sha256:0ld0"}
                assert promote(reg, "3f2a1b9", "stable") == {"3f2a1b9": "sha256:aa11", "stable": "sha256:aa11"}

            def test_original_untouched():
                reg = {"3f2a1b9": "sha256:aa11"}
                promote(reg, "3f2a1b9", "1.4.2")
                assert reg == {"3f2a1b9": "sha256:aa11"}, "Исходный словарь не должен меняться"

            def test_missing():
                with pytest.raises(KeyError):
                    promote({"stable": "sha256:0ld0"}, "deadbee", "stable")
            """,
            """
            def promote(registry, sha, new_tag):
                digest = registry[sha]
                return {**registry, new_tag: digest}
            """,
            hint="`registry[sha]` сам выбросит KeyError; новый словарь — `{**registry, new_tag: digest}`."),
    cmd(f"{P}-ci-e6", "В шаге CI запусти тесты из образа `ghcr.io/acme/tests:$GITHUB_SHA`: контейнер удалить после работы, папку `reports` из текущей директории (`$PWD`) смонтировать в `/tests/reports`.",
        ['docker run --rm -v "$PWD/reports:/tests/reports" ghcr.io/acme/tests:$GITHUB_SHA',
         anyorder("docker run", ["--rm", '-v "$PWD/reports:/tests/reports"'], "ghcr.io/acme/tests:$GITHUB_SHA"),
         anyorder("docker run", ["--rm", "-v $PWD/reports:/tests/reports"], "ghcr.io/acme/tests:$GITHUB_SHA"),
         anyorder("docker run", ["--rm", '-v "$(pwd)/reports:/tests/reports"'], "ghcr.io/acme/tests:$GITHUB_SHA"),
         anyorder("docker run", ["--rm", "-v $(pwd)/reports:/tests/reports"], "ghcr.io/acme/tests:$GITHUB_SHA")],
        hint="`docker run --rm -v \"$PWD/reports:/tests/reports\" образ`."),
    cmd(f"{P}-ci-e7", "У DinD кэш пустой. Собери образ `ghcr.io/acme/tests:$GITHUB_SHA` из текущей папки, взяв кэш слоёв из `ghcr.io/acme/tests:latest`.",
        ["docker build --cache-from ghcr.io/acme/tests:latest -t ghcr.io/acme/tests:$GITHUB_SHA .",
         anyorder("docker build", ["--cache-from ghcr.io/acme/tests:latest", "-t ghcr.io/acme/tests:$GITHUB_SHA"], "."),
         anyorder("docker build", ["--cache-from=ghcr.io/acme/tests:latest", "-t ghcr.io/acme/tests:$GITHUB_SHA"], "."),
         anyorder("docker build", ["--cache-from ghcr.io/acme/tests:latest", "--tag ghcr.io/acme/tests:$GITHUB_SHA"], ".")],
        hint="Флаг `--cache-from образ`, тег через `-t`, в конце — точка."),
    cmd(f"{P}-ci-e8", "Тесты прошли на образе с дайджестом из вывода. Скачай на стенд **именно его** — по дайджесту, а не по тегу.",
        ["docker pull ghcr.io/acme/tests@sha256:9f86d081884c7d65", "docker image pull ghcr.io/acme/tests@sha256:9f86d081884c7d65"],
        context="""
            $ docker push ghcr.io/acme/tests:3f2a1b9
            3f2a1b9: digest: sha256:9f86d081884c7d65 size: 1784
            """,
        hint="Имя образа, затем `@` и дайджест: `образ@sha256:…`."),
),
)
