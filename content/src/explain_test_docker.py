"""Тема «Docker для тестировщика» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py).
Часть заданий темы пришла из старой темы «Docker и CI» — у них префикс `dci`."""
from ._lib import x

P = "dkr"
D = "dci"

EXPLAIN = {

# ===== Модуль 1. Контейнеры =====

f"{D}-m1-l1-e1": x(
    idea="Ссылка на образ — `имя:тег`; без тега Docker берёт `latest`.",
    lines=[('name, _, tag = ref.partition(":")', "Делим по первому двоеточию."), ('print(name, tag or "latest")', "Пустой тег → latest.")],
    mistake="Думать, что `nginx` без тега — «последняя стабильная»: latest — просто имя тега."),

f"{D}-m1-l1-e2": x(
    idea="Настройки тестов в контейнере передают переменными окружения; в коде — значения по умолчанию.",
    lines=[
        ('base_url = env.get("BASE_URL", "http://localhost")', "Есть — берём."),
        ('browser = env.get("BROWSER") or "chrome"', "Пустая строка — тоже по умолчанию."),
        ('headless = env.get("HEADLESS", "true") == "true"', "Нет переменной — True."),
    ],
    mistake="`env.get(\"BROWSER\", \"chrome\")` — пустая строка останется пустой."),

f"{D}-m1-l1-e3": x(
    idea="`partition` возвращает три части; если двоеточия нет, тег — пустая строка.",
    lines=[('name, _, tag = ref.partition(":")', "Имя и тег."), ('return name, tag or "latest"', "Тег по умолчанию.")],
    mistake="`split(\":\")` без проверки — распаковка упадёт, если тега нет."),

f"{D}-m1-l1-e4": x(
    idea="Собираем аргументы списком и склеиваем пробелами; образ — последним.",
    lines=[
        ('parts.append("--rm")', "Удалить после завершения."),
        ('parts.append(f"-p {host}:{container}")', "Порт хоста:контейнера."),
        ('parts.append(f"-e {key}={value}")', "Переменная окружения."),
        ("parts.append(image)", "Опции — до образа."),
    ],
    mistake="Поставить образ раньше опций — всё после образа уйдёт как команда контейнеру."),

f"{D}-m1-l1-e5": x(
    idea="Коды выхода контейнера подсказывают причину: 137 — убит (часто нехватка памяти).",
    lines=[('return {0: "ok", 1: "app error", 125: "docker error", 127: "command not found",', "Таблица кодов."), ('137: "killed (OOM?)"}.get(code, "unknown")', "Неизвестный — unknown.")],
    mistake="Считать любой ненулевой код ошибкой приложения."),

f"{D}-m1-l1-e6": x(
    idea="`docker pull` только скачивает образ.",
    lines=[("docker pull postgres:16", "Версия — тегом.")],
    mistake="`docker run postgres:16` — ещё и запустит."),

f"{D}-m1-l1-e7": x(
    idea="`--rm` удаляет контейнер после завершения — не копится мусор.",
    lines=[("docker run --rm hello-world", "Запустить и убрать.")],
    mistake="Забыть `--rm` в CI — остановленные контейнеры накапливаются."),

f"{D}-m1-l1-e8": x(
    idea="`-a` — и остановленные контейнеры тоже.",
    lines=[("docker ps -a", "Все контейнеры.")],
    mistake="`docker ps` — упавший контейнер там не виден."),

f"{P}-run-e1": x(
    idea="Кавычки не дают разрезать значение с пробелом — `shlex` разбирает команду так же, как оболочка.",
    lines=[
        ("args = shlex.split(cmd)", "Аргументы."),
        ("print(len(args))", "docker, run, --rm, -e, значение, -p, порты, nginx."),
        ("print(args[4])", "Значение с пробелом — один аргумент."),
    ],
    mistake="Считать по пробелам — получится 9."),

f"{P}-run-e2": x(
    idea="`-d` — в фоне, `--name` — имя, `-p хост:контейнер` — проброс порта.",
    lines=[("docker run -d", "Фон."), ("--name web", "Имя."), ("-p 8080:80", "8080 хоста → 80 контейнера."), ("nginx", "Образ — последним.")],
    mistake="`-p 80:8080` — порядок наоборот."),

f"{P}-run-e3": x(
    idea="`-e ИМЯ=значение` — переменная внутри контейнера.",
    lines=[("docker run --rm", "Удалить после."), ("-e BASE_URL=http://stage.test", "Адрес стенда."), ("my-tests", "Образ.")],
    mistake="Переменная после имени образа — уйдёт аргументом команды."),

f"{P}-run-e4": x(
    idea="`-v хост:контейнер` монтирует папку: отчёты из контейнера окажутся на хосте.",
    lines=[("-v $(pwd)/reports:/app/reports", "`$(pwd)` — абсолютный путь текущей папки.")],
    mistake="Без тома отчёты исчезнут вместе с контейнером (`--rm`)."),

f"{P}-run-e5": x(
    idea="Две или три части через `:` — с последнего конца всегда хост и контейнер.",
    lines=[
        ('parts = spec.split(":")', "Части."),
        ('ip = parts[0] if len(parts) == 3 else "0.0.0.0"', "IP — только в длинной форме."),
        ('return {"ip": ip, "host": int(parts[-2]), "container": int(parts[-1])}', "Отрицательные индексы."),
    ],
    mistake="`parts[0]` как порт хоста — в длинной форме это IP."),

f"{P}-run-e6": x(
    idea="Для `subprocess` каждый флаг и значение — отдельный элемент списка.",
    lines=[("for name in sorted(env):", "По алфавиту."), ('result += ["-e", f"{name}={env[name]}"]', "Два элемента на переменную.")],
    mistake="`\"-e NAME=value\"` одной строкой — Docker увидит неизвестный флаг."),

f"{P}-run-e7": x(
    idea="Порт хоста может занять только один контейнер.",
    lines=[
        ('host = int(spec.split(":")[0])', "Порт хоста."),
        ("if host in running:", "Уже занят."),
        ("running[host] = name", "Запоминаем владельца."),
    ],
    mistake="Думать, что конфликтует порт контейнера — внутри у каждого свой."),

f"{P}-run-e8": x(
    idea="`-it` — интерактивный режим с терминалом; команда после образа заменяет стандартную.",
    lines=[("docker run --rm -it", "Терминал, удалить после выхода."), ("python:3.12-slim bash", "Образ и команда.")],
    mistake="Без `-it` — bash сразу завершится."),

f"{P}-debug-e1": x(
    idea="`--tail N` — последние N строк логов.",
    lines=[("docker logs --tail 50 app", "Хвост лога.")],
    mistake="`docker logs app` — весь лог, может быть огромным."),

f"{P}-debug-e2": x(
    idea="`-f` (follow) — следить за логом.",
    lines=[("docker logs -f app", "Новые строки по мере записи.")],
    mistake="Перезапускать `docker logs` вручную."),

f"{P}-debug-e3": x(
    idea="`exec` запускает команду в уже работающем контейнере.",
    lines=[("docker exec -it db bash", "Оболочка внутри.")],
    mistake="`docker run -it db bash` — создаст новый контейнер из образа «db»."),

f"{P}-debug-e4": x(
    idea="`inspect -f` с Go-шаблоном выводит одно поле.",
    lines=[("docker inspect -f '{{.State.ExitCode}}' app", "Только код выхода.")],
    mistake="Двойные фигурные скобки забыть — шаблон не сработает."),

f"{P}-debug-e5": x(
    idea="Колонки разделены двумя и более пробелами — по этому правилу и режем.",
    lines=[
        ("for line in output.strip().splitlines()[1:]:", "Без заголовка."),
        ('_id, image, status, name = re.split(r"\\s{2,}", line.strip())', "Внутри статуса одиночные пробелы сохранятся."),
    ],
    mistake="`line.split()` — статус «Up 2 hours» развалится на части."),

f"{P}-debug-e6": x(
    idea="Код выхода — в скобках после `Exited`; ноль — нормальное завершение.",
    lines=[
        ('name, status = line.split("|", 1)', "Имя и статус."),
        ('m = re.match(r"Exited \\((\\d+)\\)", status)', "Код в скобках."),
        ('if m and m.group(1) != "0":', "Ненулевой — упал."),
    ],
    mistake="Считать упавшими все Exited — `Exited (0)` это успех."),

f"{P}-debug-e7": x(
    idea="`docker inspect` — JSON-массив; состояние контейнера в `State`.",
    lines=[
        ("info = json.loads(raw)[0]", "Первый (единственный) контейнер."),
        ('print(info["Name"].lstrip("/"), state["Status"], state["ExitCode"])', "Имя без слеша."),
        ('if state["OOMKilled"]:', "Убит из-за памяти."),
    ],
    mistake="Забыть `[0]` — `inspect` всегда возвращает список."),

f"{P}-debug-e8": x(
    idea="`enumerate(..., 1)` — номера строк с единицы.",
    lines=[("return [(i, line) for i, line in enumerate(log.splitlines(), 1)", "Номер и строка."), ('if "ERROR" in line or line.startswith("Traceback")]', "Два признака.")],
    mistake="Нумерация с 0."),

f"{P}-registry-e1": x(
    idea="Тег — после последнего двоеточия; реестр — первая часть пути.",
    lines=[
        ('path, _, tag = ref.rpartition(":")', "С конца — в адресе реестра тоже может быть `:`."),
        ('registry, *repo = path.split("/")', "Первая часть и остальное."),
        ('print("/".join(repo))', "acme/shop-tests."),
    ],
    mistake="`partition` — для `localhost:5000/…` тег определится неправильно."),

f"{P}-registry-e2": x(
    idea="Первая часть — реестр, только если похожа на адрес; иначе Docker Hub.",
    lines=[
        ('if len(parts) > 1 and ("." in parts[0] or ":" in parts[0] or parts[0] == "localhost"):', "Признаки адреса."),
        ("registry = parts.pop(0)", "Убираем реестр из пути."),
        ('last, tag = last.rsplit(":", 1)', "Тег — у последней части."),
    ],
    mistake="Считать `acme` реестром в `acme/tests`."),

f"{P}-registry-e3": x(
    idea="Зафиксирован дайджестом или конкретным тегом; `latest` и отсутствие тега — нет.",
    lines=[
        ('if "@sha256:" in ref:\n        return True', "Дайджест — самый надёжный."),
        ('last = ref.split("/")[-1]', "Тег ищем в последней части."),
        ('return ":" in last and last.rsplit(":", 1)[1] != "latest"', "Тег и не latest."),
    ],
    mistake="Искать `:` во всей ссылке — сработает на порт реестра."),

f"{P}-registry-e4": x(
    idea="`docker tag` даёт образу ещё одно имя — нужное для реестра.",
    lines=[("docker tag my-tests:latest ghcr.io/acme/my-tests:1.0", "Старое имя → новое.")],
    mistake="Пересобирать образ ради нового имени."),

f"{P}-registry-e5": x(
    idea="`docker login адрес` — вход в реестр.",
    lines=[("docker login ghcr.io", "Логин и токен спросит сама.")],
    mistake="Писать пароль в команде — останется в истории."),

f"{P}-registry-e6": x(
    idea="`docker push` отправляет образ по его имени.",
    lines=[("docker push ghcr.io/acme/my-tests:1.0", "Имя определяет реестр.")],
    mistake="Пушить без тега с реестром — уйдёт на Docker Hub."),

f"{P}-registry-e7": x(
    idea="Отбираем `X.Y.Z` и сравниваем кортежами чисел.",
    lines=[
        ('versions = [t for t in tags if re.fullmatch(r"\\d+\\.\\d+\\.\\d+", t)]', "Только полные версии."),
        ('return max(versions, key=lambda t: tuple(int(x) for x in t.split(".")))', "Числовое сравнение."),
    ],
    mistake="`max(versions)` по строкам — «1.9.9» больше «1.10.0»."),

f"{P}-registry-e8": x(
    idea="`docker images` — локальные образы.",
    lines=[("docker images", "Список с размерами.")],
    mistake="`docker ps` — это контейнеры."),

# ===== Модуль 2. Dockerfile и сборка =====

f"{D}-m1-l2-e1": x(
    idea="Слой пересобирается, если изменились его входные файлы; всё после него — тоже.",
    lines=[("if changed & set(files):", "Шаг использует изменённый файл."), ("print(i, cmd)", "Первый такой — `COPY . .`.")],
    mistake="Думать, что пересоберётся установка зависимостей — requirements.txt не менялся."),

f"{D}-m1-l2-e2": x(
    idea="Строка Dockerfile: инструкция и аргументы; комментарии и пустые пропускаем.",
    lines=[
        ('if not line or line.startswith("#"):\n            continue', "Пропуск."),
        ('instr, _, args = line.partition(" ")', "Первое слово."),
        ("result.append((instr.upper(), args.strip()))", "Инструкция — заглавными."),
    ],
    mistake="`split()` — аргументы разобьются на слова."),

f"{D}-m1-l2-e3": x(
    idea="Сначала копируем только requirements и ставим зависимости — этот слой кэшируется, пока зависимости не меняются.",
    lines=[
        ("FROM python:3.12-slim", "Базовый образ."),
        ("COPY requirements.txt .", "Только список зависимостей."),
        ("RUN pip install -r requirements.txt", "Кэшируемый слой."),
        ('CMD ["pytest", "-v"]', "Команда по умолчанию."),
    ],
    mistake="`COPY . .` до установки — любая правка теста переустановит все пакеты."),

f"{D}-m1-l2-e4": x(
    idea="Первый шаг, который использует изменённый файл, — с него начинается пересборка.",
    lines=[("if changed & set(files):\n            return i", "Пересечение множеств."), ("return None", "Ничего не пересобирается.")],
    mistake="Возвращать последний подходящий шаг."),

f"{D}-m1-l2-e5": x(
    idea="Исключаем файл, если хоть одна часть пути подходит под шаблон.",
    lines=[('return any(fnmatch(part, p) for part in path.split("/") for p in patterns)', "Все части × все шаблоны.")],
    mistake="Проверять весь путь — `__pycache__` в середине пути не совпадёт."),

f"{D}-m1-l2-e6": x(
    idea="`-t` — имя образа, `.` — контекст сборки (текущая папка).",
    lines=[("docker build -t my-tests .", "Не забыть точку.")],
    mistake="Без `.` — «requires 1 argument»."),

f"{D}-m1-l2-e7": x(
    idea="`--no-cache` — собрать все слои заново.",
    lines=[("docker build --no-cache -t my-tests .", "Без кэша.")],
    mistake="Удалять образ ради пересборки."),

f"{D}-m1-l2-e8": x(
    idea="`docker history` — слои образа и их размер.",
    lines=[("docker history my-tests", "Какой шаг сколько весит.")],
    mistake="`docker inspect` — метаданные, а не слои с размерами."),

f"{P}-instructions-e1": x(
    idea="Exec-форма — JSON-список, shell-форма — строка для оболочки; разобранные, они совпадают.",
    lines=[
        ("print(json.loads(exec_form))", "Список как есть."),
        ("print(shlex.split(shell_form))", "Кавычки собрали выражение в один аргумент."),
    ],
    mistake="Думать, что shell-форма разрежет `smoke and not slow` — кавычки этого не дают."),

f"{P}-instructions-e2": x(
    idea="Аргументы `docker run` заменяют CMD, ENTRYPOINT остаётся.",
    lines=[("return entrypoint + (run_args or cmd)", "Пустые run_args — берём CMD.")],
    mistake="Складывать run_args и cmd вместе."),

f"{P}-instructions-e3": x(
    idea="ARG до FROM — им можно параметризовать базовый образ; ENV — переменная по умолчанию внутри контейнера.",
    lines=[
        ("ARG PYTHON_VERSION=3.12", "Аргумент сборки."),
        ("FROM python:${PYTHON_VERSION}-slim", "Подстановка."),
        ("ENV BASE_URL=http://app:8000", "Стенд по умолчанию."),
        ('ENTRYPOINT ["pytest"]', "Всегда pytest; CMD — его аргументы."),
    ],
    mistake="ARG после FROM — в строке FROM он ещё не определён."),

f"{P}-instructions-e4": x(
    idea="`--build-arg` задаёт значение ARG при сборке.",
    lines=[("docker build --build-arg PYTHON_VERSION=3.11", "Другая версия."), ("-t my-tests .", "Имя и контекст.")],
    mistake="`-e` — это для запуска, а не для сборки."),

f"{P}-instructions-e5": x(
    idea="Проходим инструкции и копим коды проблем во множество.",
    lines=[
        ('if ":" not in last or last.endswith(":latest"):', "Нет тега или latest."),
        ('elif instr == "ADD":', "ADD вместо COPY."),
        ('elif instr == "RUN" and "pip install" in args and "--no-cache-dir" not in args:', "Кэш pip раздует образ."),
        ('if not has_user:\n        problems.add("no-user")', "Контейнер от root."),
    ],
    mistake="Проверять тег по всей строке FROM — сломается на `--platform` или реестре с портом."),

f"{P}-instructions-e6": x(
    idea="`-e` при запуске перекрывает ENV из Dockerfile — как правый словарь при слиянии.",
    lines=[("env = {**dockerfile_env, **run_env}", "run_env — поверх."), ('print(f"{name}={env[name]}")', "По алфавиту.")],
    mistake="Ожидать BASE_URL из Dockerfile."),

f"{P}-instructions-e7": x(
    idea="Аргументы после образа заменяют CMD: `pytest` + `-m smoke`.",
    lines=[("docker run --rm my-tests -m smoke", "ENTRYPOINT остаётся.")],
    mistake="`docker run --rm my-tests pytest -m smoke` — получится `pytest pytest -m smoke`."),

f"{P}-instructions-e8": x(
    idea="Регулярка ловит `${ИМЯ}` и необязательную часть `:-значение`; функция решает, что подставить.",
    lines=[
        ('value = env.get(name, "")', "Нет переменной — пусто."),
        ("if default is not None and not value:\n            return default", "Пусто и есть значение по умолчанию."),
        ('return re.sub(r"\\$\\{(\\w+)(?::-([^}]*))?\\}", replace, text)', "Все вхождения."),
    ],
    mistake="Подставлять default только при отсутствии — `:-` срабатывает и на пустом значении."),

f"{P}-tests-e1": x(
    idea="Зависимости — отдельным слоем и без кэша pip; отчёт JUnit — в папку, которую потом смонтируют.",
    lines=[
        ("COPY requirements.txt .", "Сначала только зависимости."),
        ("RUN pip install --no-cache-dir -r requirements.txt", "Кэш pip не попадёт в образ."),
        ('CMD ["pytest", "--junitxml=reports/junit.xml"]', "Exec-форма."),
    ],
    mistake="Shell-форма CMD — сигналы остановки не дойдут до pytest."),

f"{P}-tests-e2": x(
    idea="Стенд — переменной, отчёты — томом; контейнер удалится, а отчёты останутся.",
    lines=[("-e BASE_URL=http://stage.test", "Адрес стенда."), ("-v $(pwd)/reports:/app/reports", "Отчёты на хост."), ("my-tests", "Образ — последним.")],
    mistake="Забыть том — отчёты пропадут вместе с контейнером."),

f"{P}-tests-e3": x(
    idea="Команда после образа заменяет CMD целиком.",
    lines=[("docker run --rm my-tests", "Образ."), ("pytest -m smoke", "Новая команда.")],
    mistake="`docker run --rm my-tests -m smoke` — при CMD без ENTRYPOINT Docker попробует запустить `-m`."),

f"{P}-tests-e4": x(
    idea="`.dockerignore` исключает файлы из контекста сборки: быстрее сборка, меньше образ, нет мусора.",
    lines=[(".git", "История не нужна в образе."), (".venv", "Окружение хоста."), ("*.pyc", "Шаблоны работают.")],
    mistake="Не исключить `.venv` — в образ уедут сотни мегабайт."),

f"{P}-tests-e5": x(
    idea="Список аргументов для `subprocess`: флаги, переменные по алфавиту, образ, затем аргументы команды.",
    lines=[
        ('cmd = ["docker", "run", "--rm", "-v", f"{reports}:/app/reports"]', "Основа."),
        ('cmd += ["-e", f"{name}={env[name]}"]', "Каждая переменная — два элемента."),
        ("return cmd + [image, *args]", "`*args` распаковывает список."),
    ],
    mistake="`cmd + [image, args]` — список окажется одним элементом."),

f"{P}-tests-e6": x(
    idea="CI смотрит только на код выхода: `docker run` возвращает код команды внутри контейнера.",
    lines=[('return 0 if all(r == "passed" for r in results.values()) else 1', "Все прошли — 0.")],
    mistake="Ожидать, что CI прочитает текст отчёта."),

f"{P}-tests-e7": x(
    idea="Официальный образ Playwright уже содержит браузеры; версию фиксируем.",
    lines=[("FROM mcr.microsoft.com/playwright/python:v1.47.0-noble", "Зафиксированный тег."), ('CMD ["pytest", "--browser", "chromium"]', "Запуск UI-тестов.")],
    mistake="`FROM python` + установка браузеров вручную — долго и много зависимостей."),

f"{P}-tests-e8": x(
    idea="`$?` — код выхода последней команды, в том числе `docker run`.",
    lines=[("echo $?", "0 — тесты прошли.")],
    mistake="`docker ps` — код выхода там не виден."),

f"{P}-optimize-e1": x(
    idea="Размер образа — сумма слоёв; самый тяжёлый обычно — установка зависимостей.",
    lines=[
        ("total = sum(size for _, size in layers)", "Сумма."),
        ('print(f"{total:.1f} MB")', "Один знак."),
        ("biggest = max(layers, key=lambda layer: layer[1])", "По размеру."),
    ],
    mistake="`max(layers)` — сравнит команды по алфавиту."),

f"{P}-optimize-e2": x(
    idea="Сортируем по размеру по убыванию и берём первые n команд.",
    lines=[("ordered = sorted(layers, key=lambda layer: layer[1], reverse=True)", "Тяжёлые первыми."), ("return [command for command, _ in ordered[:n]]", "Только команды.")],
    mistake="Забыть `reverse=True`."),

f"{P}-optimize-e3": x(
    idea="Многоэтапная сборка: тяжёлый этап собирает колёса, лёгкий берёт только их.",
    lines=[
        ("FROM python:3.12 AS builder", "Этап с компиляторами."),
        ("RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels", "Готовые пакеты."),
        ("COPY --from=builder /wheels /wheels", "Только результат."),
        ("USER nobody", "Не от root."),
    ],
    mistake="Один этап на полном образе — финальный образ в разы тяжелее."),

f"{P}-optimize-e4": x(
    idea="Секреты в ENV и ARG видны в `docker history` — ищем подозрительные имена.",
    lines=[
        ('if instr.upper() in ("ENV", "ARG") and args:', "Только эти инструкции."),
        ('name = args.split("=")[0].strip()', "Имя без значения."),
        ('if any(word in name.upper() for word in ("PASSWORD", "TOKEN", "SECRET", "KEY")):', "Признаки секрета."),
    ],
    mistake="Проверять значение — секрет может прийти через `--build-arg`, а имя всё равно выдаёт его."),

f"{P}-optimize-e5": x(
    idea="`image prune` удаляет висящие образы без тегов.",
    lines=[("docker image prune", "Освободить место.")],
    mistake="`docker image prune -a` — удалит и все неиспользуемые образы с тегами."),

f"{P}-optimize-e6": x(
    idea="`docker system df` — сводка по месту.",
    lines=[("docker system df", "Образы, контейнеры, тома, кэш.")],
    mistake="`df -h` — место на диске целиком, без разбивки Docker."),

f"{P}-optimize-e7": x(
    idea="Делим на 1024, пока значение не станет меньше 1024; GB — предел.",
    lines=[
        ('if n < 1024:\n        return f"{n} B"', "Байты — целым."),
        ("n /= 1024", "Следующая единица."),
        ('if n < 1024 or unit == "GB":\n            return f"{n:.1f} {unit}"', "Подходящая единица."),
    ],
    mistake="Основание 1000 — по условию 1024."),

f"{P}-optimize-e8": x(
    idea="Trivy сканирует образ на известные уязвимости пакетов.",
    lines=[("trivy image my-tests:1.0", "Сканирование.")],
    mistake="Думать, что официальный базовый образ всегда без уязвимостей."),

# ===== Модуль 3. Docker Compose =====

f"{P}-compose-e1": x(
    idea="Compose-файл — YAML: словарь сервисов с их настройками.",
    lines=[
        ('print(list(compose["services"]))', "Имена сервисов."),
        ('print(compose["services"]["app"]["ports"])', "Порты — список строк."),
        ('print(compose["services"]["db"].get("ports", []))', "Нет портов — пустой список."),
    ],
    mistake="`[\"db\"][\"ports\"]` — KeyError."),

f"{P}-compose-e2": x(
    idea="Сервисы видят друг друга по имени: адрес базы — `db:5432`.",
    lines=[
        ("POSTGRES_PASSWORD: secret", "Пароль базы."),
        ("DATABASE_URL: postgresql://postgres:secret@db:5432/postgres", "Хост — имя сервиса."),
        ("depends_on:", "app стартует после db."),
    ],
    mistake="`localhost` в адресе базы — внутри контейнера app это сам app."),

f"{P}-compose-e3": x(
    idea="`up -d` поднимает все сервисы в фоне.",
    lines=[("docker compose up -d", "Стенд в фоне.")],
    mistake="Без `-d` — терминал занят логами."),

f"{P}-compose-e4": x(
    idea="`down -v` удаляет контейнеры, сеть и тома.",
    lines=[("docker compose down -v", "Чистый лист.")],
    mistake="`down` без `-v` — данные базы останутся."),

f"{P}-compose-e5": x(
    idea="`logs -f сервис` — следить за логами одного сервиса.",
    lines=[("docker compose logs -f app", "Только app.")],
    mistake="`docker logs app` — имя контейнера в compose обычно другое."),

f"{P}-compose-e6": x(
    idea="Топологическая сортировка: на каждом шаге берём готовый сервис (все зависимости уже запущены), из нескольких — по алфавиту.",
    lines=[
        ("while len(order) < len(services):", "Пока не расставили все."),
        ('ready = [name for name, s in services.items()', "Кандидаты…"),
        ('if name not in order and all(d in order for d in s.get("depends_on", []))]', "…у которых все зависимости уже стоят."),
        ("order.append(min(ready))", "Первый по алфавиту."),
    ],
    mistake="Сортировать просто по числу зависимостей — порядок цепочек сломается."),

f"{P}-compose-e7": x(
    idea="Порт хоста — предпоследняя часть строки.",
    lines=[('return {name: [int(p.split(":")[-2]) for p in s["ports"]]', "Числами."), ('for name, s in services.items() if s.get("ports")}', "Только сервисы с портами.")],
    mistake="`split(\":\")[0]` — в длинной форме это IP."),

f"{P}-compose-e8": x(
    idea="`compose ps` — контейнеры текущего проекта.",
    lines=[("docker compose ps", "Состояние стенда.")],
    mistake="`docker ps` — покажет все контейнеры машины."),

f"{P}-env-e1": x(
    idea="`.env` — строки `ИМЯ=значение`, комментарии с `#` пропускаются.",
    lines=[('if line and not line.startswith("#"):', "Пропуск."), ('name, value = line.split("=", 1)', "По первому `=`.")],
    mistake="Посчитать комментарий переменной."),

f"{P}-env-e2": x(
    idea="Делим по первому `=`, чистим пробелы, снимаем парные кавычки.",
    lines=[
        ('name, _, value = line.partition("=")', "Первое `=`."),
        ("if len(value) >= 2 and value[0] == value[-1] and value[0] in \"'\\\"\":", "Одинаковые кавычки по краям."),
        ("value = value[1:-1]", "Без кавычек."),
    ],
    mistake="`strip(\"\\\"'\")` — снимет и непарные кавычки."),

f"{P}-env-e3": x(
    idea="Цепочка `or` даёт первое непустое значение по приоритету.",
    lines=[("return shell.get(name) or env_file.get(name) or default", "Оболочка → .env → по умолчанию.")],
    mistake="Поставить .env выше оболочки — так Compose не делает."),

f"{P}-env-e4": x(
    idea="`--env-file` — другой файл переменных; ставится до `up`.",
    lines=[("docker compose --env-file .env.stage", "Файл стенда."), ("up -d", "Запуск.")],
    mistake="`docker compose up -d --env-file …` — опция compose, а не up."),

f"{P}-env-e5": x(
    idea="`${VAR:-default}` — значение из окружения или по умолчанию; том забирает отчёты.",
    lines=[("build: .", "Свой Dockerfile."), ("BASE_URL: ${BASE_URL:-http://app:8000}", "По умолчанию — сервис app."), ("- ./reports:/app/reports", "Отчёты на хосте.")],
    mistake="Захардкодить адрес — нельзя переключить стенд."),

f"{P}-env-e6": x(
    idea="`compose config` печатает итоговую конфигурацию с подставленными переменными.",
    lines=[("docker compose config", "Проверить подстановку.")],
    mistake="Гадать, подхватилась ли переменная, по поведению тестов."),

f"{P}-env-e7": x(
    idea="Список `A=B` превращаем в словарь — делим по первому `=`.",
    lines=[('from_list = dict(item.split("=", 1) for item in as_list)', "Пары → словарь."), ("print(from_list == as_dict)", "Одно и то же.")],
    mistake="`split(\"=\")` без ограничения — сломается на значении с `=`."),

f"{P}-env-e8": x(
    idea="Три формы: `None`, список и словарь; значения приводим к строкам как Compose.",
    lines=[
        ("if env is None:\n        return {}", "Ничего."),
        ('return {name: value for name, _, value in (item.partition("=") for item in env)}', "Без `=` — пустое значение."),
        ('value = "true" if value else "false"', "bool — строчными."),
    ],
    mistake="`str(True)` — «True» с заглавной."),

f"{P}-stand-e1": x(
    idea="healthcheck проверяет готовность базы, а `condition: service_healthy` ждёт её.",
    lines=[
        ('test: ["CMD", "pg_isready", "-U", "postgres"]', "Проверка готовности."),
        ("retries: 10", "Сколько раз пробовать."),
        ("condition: service_healthy", "Ждать здоровую базу."),
    ],
    mistake="`depends_on: [db]` — ждёт только запуска контейнера, не готовности."),

f"{P}-stand-e2": x(
    idea="`--abort-on-container-exit` останавливает стенд, `--exit-code-from tests` отдаёт код тестов.",
    lines=[("docker compose up", "Поднять."), ("--abort-on-container-exit", "Остановить всё после тестов."), ("--exit-code-from tests", "Код CI — от тестов.")],
    mistake="Без них стенд будет работать вечно, а CI получит 0."),

f"{P}-stand-e3": x(
    idea="`compose run` — одноразовый контейнер сервиса со своей командой.",
    lines=[("docker compose run --rm tests", "Сервис tests."), ("pytest -m smoke", "Команда.")],
    mistake="`exec` — работает только с уже запущенным контейнером."),

f"{P}-stand-e4": x(
    idea="Пробуем, ждём, снова пробуем; после последней неудачи — ошибка.",
    lines=[
        ("if check():\n            return attempt", "Готово."),
        ("if attempt < retries:\n            sleep(interval)", "Ждать, кроме последней попытки."),
        ('raise TimeoutError(f"не дождались за {retries} попыток")', "Попытки кончились."),
    ],
    mistake="Ждать и после последней попытки — лишняя пауза."),

f"{P}-stand-e5": x(
    idea="Внутри сети — имя сервиса и порт контейнера; с хоста — localhost и опубликованный порт.",
    lines=[
        ('return f"http://{service}:{container_port}"', "Из контейнера."),
        ('host, container = spec.split(":")[-2:]', "Пара портов."),
        ("return None", "У db портов нет — с хоста не достучаться."),
    ],
    mistake="С хоста идти на `app:8000` — такого имени хост не знает."),

f"{P}-stand-e6": x(
    idea="Из контейнера — по имени; с хоста — ищем опубликованный порт для нужного порта контейнера.",
    lines=[
        ('return f"http://{service}:{port}"', "Та же сеть."),
        ('for spec in services.get(service, {}).get("ports", []):', "Опубликованные порты."),
        ('return f"http://localhost:{host}"', "Порт хоста."),
    ],
    mistake="Возвращать порт контейнера для хоста."),

f"{P}-stand-e7": x(
    idea="`compose exec сервис команда` — команда в запущенном контейнере сервиса.",
    lines=[("docker compose exec db", "Контейнер базы."), ("psql -U postgres", "Консоль.")],
    mistake="`docker exec db` — имя контейнера в compose другое."),

f"{P}-stand-e8": x(
    idea="`--build` пересобирает образы перед запуском.",
    lines=[("docker compose up -d --build", "Свежий код тестов.")],
    mistake="`up -d` без `--build` — запустится старый образ."),

f"{P}-practice-e1": x(
    idea="Полный стенд: база с проверкой готовности, приложение ждёт базу, тесты ходят в приложение по имени.",
    lines=[
        ("condition: service_healthy", "app ждёт готовую базу."),
        ("BASE_URL: http://app:8000", "Тесты обращаются к сервису по имени."),
        ("- ./reports:/app/reports", "Отчёты на хосте."),
    ],
    mistake="`BASE_URL: http://localhost:8000` — внутри контейнера tests это он сам."),

f"{P}-practice-e2": x(
    idea="Разбираем статусы по порядку: код выхода (137 — память, Traceback — ошибка), потом healthcheck.",
    lines=[
        ('m = re.match(r"exited \\((\\d+)\\)", status)', "Код выхода."),
        ("if code == 137:", "Убит."),
        ('elif "Traceback" in logs.get(name, ""):', "Ошибка в коде."),
        ('elif "(unhealthy)" in status:', "Работает, но не здоров."),
    ],
    mistake="Считать `exited (0)` проблемой — одноразовые сервисы так и завершаются."),

f"{P}-practice-e3": x(
    idea="`docker cp контейнер:путь куда` копирует файлы и из остановленного контейнера.",
    lines=[("docker cp tests:/app/reports .", "Папка отчётов — сюда.")],
    mistake="Думать, что из остановленного контейнера файлы не достать."),

f"{P}-practice-e4": x(
    idea="Итог стенда — ненулевой, если упал хоть один одноразовый сервис.",
    lines=[('failed = [name for name, code in exits.items() if code != 0]', "Упавшие."), ('print("код для CI:", 1 if failed else 0)', "Красный.")],
    mistake="Брать код только последнего сервиса."),

f"{P}-practice-e5": x(
    idea="Флаги compose — до `up`; профиль — только если задан.",
    lines=[
        ('cmd += ["-f", f]', "Каждый файл — своим `-f`."),
        ('if profile:\n        cmd += ["--profile", profile]', "Профиль."),
        ('return cmd + ["up", "-d", *services]', "Подкоманда и сервисы."),
    ],
    mistake="Ставить `-f` после `up`."),

f"{P}-practice-e6": x(
    idea="Несколько `-f`: следующий файл переопределяет предыдущий.",
    lines=[("docker compose -f docker-compose.yml -f docker-compose.ci.yml", "База + надстройка."), ("up -d", "Запуск.")],
    mistake="Перепутать порядок — база перекроет CI-настройки."),

f"{P}-practice-e7": x(
    idea="Сервисы с профилем стартуют только при `--profile`.",
    lines=[("docker compose --profile ui up -d", "Плюс сервисы профиля ui.")],
    mistake="`docker compose up ui` — профиль и имя сервиса — разное."),

f"{P}-practice-e8": x(
    idea="Полная уборка: тома и «сироты».",
    lines=[("docker compose down", "Контейнеры и сеть."), ("-v --remove-orphans", "Тома и лишние контейнеры.")],
    mistake="Оставлять тома в CI — следующий прогон начнётся со старыми данными."),

# ===== Модуль 4. Docker на практике =====

f"{P}-hub-e1": x(
    idea="Docker дописывает короткое имя: `library/` для официальных, `docker.io/` если реестр не указан, `:latest` если нет тега.",
    trace=[
        ("print(full_name(ref))", "python:3.12-slim: нет / → library/…, реестра нет → docker.io/…", "docker.io/library/python:3.12-slim"),
        ("print(full_name(ref))", "anna/my-tests: anna — не реестр; тега нет → :latest", "docker.io/anna/my-tests:latest"),
        ("print(full_name(ref))", "ghcr.io/acme/tests:1.0: в ghcr.io есть точка — это реестр, тег есть", "ghcr.io/acme/tests:1.0"),
    ],
    mistake="Думать, что `ghcr.io/...` тоже пойдёт в Docker Hub: точка в первой части — признак другого реестра."),

f"{P}-hub-e2": x(
    idea="Версия — до первого дефиса, вариант — всё остальное.",
    lines=[('version, _, variant = tag.partition("-")', "Три части: до дефиса, сам дефис, после."), ("return version, variant", "Нет дефиса — variant пустой.")],
    mistake="`split(\"-\")` разобьёт `slim-bookworm` на два куска, и вариант потеряется."),

f"{P}-hub-e3": x(
    idea="Кандидаты в порядке приоритета: сначала slim, потом обычный; alpine в списке просто нет.",
    lines=[('for tag in (f"{version}-slim", version):', "Порядок перебора = приоритет."), ("if tag in tags:\n            return tag", "Первый найденный — ответ."), ("return None", "Ничего подходящего.")],
    mistake="Выбирать самый маленький образ — попадёшь на alpine с проблемами сборки пакетов."),

f"{P}-hub-e4": x(
    idea="Сначала отсекаем чужие реестры, потом убираем тег и строим ссылку: `_/имя` для официальных, `r/владелец/имя` для остальных.",
    lines=[
        ('if len(parts) > 1 and ("." in parts[0] or ":" in parts[0]):', "ghcr.io, localhost:5000 — не Docker Hub."),
        ('parts[-1] = parts[-1].split(":")[0]', "Тег — только в последней части."),
        ('return f"https://hub.docker.com/_/{parts[0]}"', "Официальный образ."),
    ],
    mistake="Резать тег по первому `:` во всей строке — сломается `localhost:5000/app`."),

f"{P}-hub-e5": x(
    idea="Фильтр `is-official=true` оставляет только Docker Official Images.",
    lines=[("docker search --filter is-official=true python", "Поиск в Docker Hub по слову python.")],
    mistake="Брать первый попавшийся образ из поиска — он может быть от кого угодно."),

f"{P}-hub-e6": x(
    idea="Токен передают через стандартный ввод — он не попадёт в историю команд и список процессов.",
    lines=[('echo "$DOCKERHUB_TOKEN"', "Токен из переменной (в CI — из секрета)."), ("| docker login -u anna --password-stdin", "Логин читает пароль из ввода.")],
    mistake="`docker login -p $DOCKERHUB_TOKEN` — токен виден в `ps` и истории, Docker сам предупреждает об этом."),

f"{P}-hub-e7": x(
    idea="`docker tag` добавляет образу второе имя — с префиксом пользователя Docker Hub.",
    lines=[("docker tag my-tests anna/my-tests:1.0", "Старое имя → новое имя:тег.")],
    mistake="Пушить `my-tests` без префикса — Docker попробует отправить в `library/`, куда у тебя нет прав."),

f"{P}-hub-e8": x(
    idea="Push отправляет образ по его полному имени: пользователь/репозиторий:тег.",
    lines=[("docker push anna/my-tests:1.0", "Слои, которых нет в реестре, загрузятся.")],
    mistake="Забыть `docker login` — получишь `denied: requested access to the resource is denied`."),

f"{P}-image-e1": x(
    idea="Слои общие: скачиваются только те, которых ещё нет на диске.",
    trace=[
        ("new = {k: v for k, v in second.items() if k not in have}", "base1, base2, py уже есть", ""),
        ("", "new = {'deps': 28, 'tests': 1}", ""),
        ("print(len(new), sum(new.values()))", "2 слоя, 28 + 1", "2 29"),
    ],
    mistake="Считать, что каждый образ скачивается целиком: общая база берётся с диска."),

f"{P}-image-e2": x(
    idea="Слои применяются снизу вверх к одному словарю: новое значение перезаписывает, `None` удаляет.",
    lines=[
        ("for layer in layers:", "Снизу вверх."),
        ("files.pop(path, None)", "Пометка «удалён»: убираем, если было."),
        ("files[path] = content", "Верхний слой перекрывает нижний."),
    ],
    mistake="Изменять сами слои (`layer.pop`) — слои образа только для чтения, и второй вызов даст другой результат."),

f"{P}-image-e3": x(
    idea="Хороший образ тестов: маленькая база, вывод без буфера, кэш зависимостей, не root, pytest как ENTRYPOINT.",
    lines=[
        ("ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1", "Логи сразу, без .pyc."),
        ("RUN pip install --no-cache-dir -r requirements.txt", "Без кэша pip внутри образа."),
        ("RUN useradd --create-home tester\nUSER tester", "Дальше всё — от обычного пользователя."),
        ('ENTRYPOINT ["pytest"]\nCMD ["-v"]', "Контейнер = pytest; аргументы по умолчанию."),
    ],
    mistake="Поставить `USER tester` до `pip install` — установка в системный Python упадёт без прав."),

f"{P}-image-e4": x(
    idea="`--entrypoint` заменяет ENTRYPOINT и сбрасывает CMD; обычные аргументы заменяют только CMD.",
    lines=[
        ("if override is not None:\n        return [override] + (args or [])", "CMD образа уже не участвует."),
        ("return entrypoint + (args if args else cmd)", "Аргументы или CMD по умолчанию."),
    ],
    mistake="Оставлять CMD после `--entrypoint`: `docker run --entrypoint bash img` не превращается в `bash -v`."),

f"{P}-image-e5": x(
    idea="Из `inspect` видно, что запустится по умолчанию и от чьего имени.",
    trace=[
        ('env = dict(item.split("=", 1) for item in config["Env"])', "{'PATH': …, 'PYTHONUNBUFFERED': '1'}", ""),
        ('print(" ".join(config["Entrypoint"] + config["Cmd"]))', "['pytest'] + ['-v']", "pytest -v"),
        ('print(config["User"] or "root", env["PYTHONUNBUFFERED"])', "User = tester", "tester 1"),
    ],
    mistake="`split(\"=\")` без лимита сломается на значении, где тоже есть `=`."),

f"{P}-image-e6": x(
    idea="`docker image inspect` показывает конфигурацию и слои образа в JSON.",
    lines=[("docker image inspect my-tests", "Можно сузить: `--format '{{.Config.Cmd}}'`.")],
    mistake="`docker inspect` без уточнения сработает тоже, но если есть контейнер с таким же именем, покажет его."),

f"{P}-image-e7": x(
    idea="При `ENTRYPOINT [\"pytest\"]` всё после имени образа — аргументы pytest.",
    lines=[("docker run --rm my-tests -m smoke", "Выполнится `pytest -m smoke`.")],
    mistake="`docker run --rm my-tests pytest -m smoke` — получится `pytest pytest -m smoke`."),

f"{P}-image-e8": x(
    idea="`docker save` упаковывает образ со всеми слоями в tar; `docker load` распаковывает на другой машине.",
    lines=[("docker save", "Образ со слоями и настройками → архив."), ("-o my-tests.tar", "Куда сохранить. На стенде — `docker load -i my-tests.tar`.")],
    mistake="Путать с `docker export` — тот сохраняет файловую систему контейнера без слоёв и настроек образа."),

f"{P}-dind-e1": x(
    idea="При пробросе сокета путь в `-v` читает демон хоста, а не контейнер, из которого запустили команду.",
    trace=[
        ("print(mount in job_dirs, daemon_sees)", "папка есть в job-е, но не на хосте", "True False"),
        ('print("отчёты на месте" if daemon_sees else "Docker создаст пустую папку на хосте")', "daemon_sees = False", "Docker создаст пустую папку на хосте"),
    ],
    mistake="Удивляться пустым отчётам: тесты писали в папку на хосте, которую никто не смотрит."),

f"{P}-dind-e2": x(
    idea="Сокет хоста узнаём по тому, где смонтирован docker.sock; DinD — по образу `docker:*dind` и флагу `--privileged`.",
    lines=[
        ('if "/var/run/docker.sock:/var/run/docker.sock" in words:', "Проброс сокета."),
        ('image = next((w for w in words if w.startswith("docker:")), "")', "Образ docker:…"),
        ('if "--privileged" in words and image.endswith("dind"):', "Без прав DinD не стартует."),
    ],
    mistake="Считать DinD любой контейнер `docker:dind` — без `--privileged` демон внутри не запустится."),

f"{P}-dind-e3": x(
    idea="Ревью compose: docker.sock в томах и `privileged: true` — две самые опасные настройки.",
    lines=[
        ("for name in sorted(services):", "Сразу в нужном порядке."),
        ('if any(v.startswith("/var/run/docker.sock") for v in cfg.get("volumes", [])):', "Сокет, в том числе с `:ro`."),
        ('if cfg.get("privileged") is True:', "Флаг привилегий."),
    ],
    mistake="Думать, что `:ro` на сокете спасает: через сокет только читать нельзя — API демона всё равно доступен."),

f"{P}-dind-e4": x(
    idea="Job с клиентом docker, сервис с демоном рядом, переменные — где демон и куда положить TLS-сертификаты.",
    lines=[
        ("image: docker:27", "Клиент docker."),
        ("services:\n    - docker:27-dind", "Демон по имени `docker`."),
        ("DOCKER_HOST: tcp://docker:2376", "Порт с TLS."),
        ('DOCKER_TLS_CERTDIR: "/certs"', "Общая папка для сертификатов."),
    ],
    mistake="Забыть `DOCKER_HOST` — клиент ищет локальный сокет и пишет `Cannot connect to the Docker daemon`."),

f"{P}-dind-e5": x(
    idea="Три формы: не задано — локальный сокет, `unix://путь`, `tcp://хост:порт` (2376 — TLS).",
    lines=[
        ("if not value:", "None и пустая строка — по умолчанию."),
        ('return {"kind": "unix", "path": value[len("unix://"):]}', "Путь — всё после схемы."),
        ('host, _, port = value[len("tcp://"):].rpartition(":")', "Порт — после последнего двоеточия."),
    ],
    mistake="Оставить порт строкой — `\"2376\" == 2376` даёт False, и tls всегда будет False."),

f"{P}-dind-e6": x(
    idea="Проброс сокета даёт клиенту в контейнере доступ к демону хоста.",
    lines=[("-v /var/run/docker.sock:/var/run/docker.sock", "Сокет хоста внутрь."), ("docker:27 docker ps", "Покажет контейнеры хоста.")],
    mistake="Ожидать увидеть пустой список: это тот же демон, контейнеры — общие."),

f"{P}-dind-e7": x(
    idea="Настоящему DinD нужен `--privileged`, иначе свой демон внутри не стартует.",
    lines=[("docker run -d --privileged --name dind docker:27-dind", "Фоновый контейнер с собственным dockerd.")],
    mistake="Запускать DinD без `--privileged` — контейнер сразу упадёт с ошибками монтирования."),

f"{P}-dind-e8": x(
    idea="`DOCKER_HOST` указывает клиенту адрес демона.",
    lines=[("DOCKER_HOST", "Например, `tcp://docker:2376` в GitLab CI; не задана — сокет `/var/run/docker.sock`.")],
    mistake="Путать с `DOCKER_TLS_CERTDIR` — та говорит, где сертификаты, а не где демон."),

f"{P}-ci-e1": x(
    idea="Тег по коммиту — первые 7 символов хеша; тег по ветке — имя без `/`.",
    trace=[
        ('tags = [sha[:7], branch.replace("/", "-")]', "['3f2a1b9', 'feature-login-form']", ""),
        ('print(f"{image}:{tag}")', "первый тег", "ghcr.io/acme/shop-tests:3f2a1b9"),
        ('print(f"{image}:{tag}")', "второй тег", "ghcr.io/acme/shop-tests:feature-login-form"),
    ],
    mistake="Оставить `/` из имени ветки — Docker не примет такой тег."),

f"{P}-ci-e2": x(
    idea="Тег коммита и тег ветки всегда; для релиза — ещё версия, MAJOR.MINOR и latest.",
    lines=[
        ('tags = [sha[:7], branch.replace("/", "-")]', "Базовые теги."),
        ('version = git_tag.removeprefix("v")', "v1.4.2 → 1.4.2."),
        ('major_minor = ".".join(version.split(".")[:2])', "1.4.2 → 1.4."),
    ],
    mistake="`git_tag.strip(\"v\")` — уберёт `v` с обоих концов; `removeprefix` надёжнее."),

f"{P}-ci-e3": x(
    idea="Build собирает и пушит образ с тегом коммита; api-tests после него запускает тесты в этом же образе и сохраняет отчёт всегда.",
    lines=[
        ("permissions:\n      packages: write", "GITHUB_TOKEN может пушить в ghcr.io."),
        ("push: true\n      tags: ghcr.io/acme/shop-tests:${{ github.sha }}", "Тег — хеш коммита."),
        ("needs: build", "Тесты ждут образ."),
        ("if: always()", "Отчёт и при красных тестах."),
    ],
    mistake="Собирать образ заново в api-tests — тестируется уже не тот образ, что ушёл в реестр."),

f"{P}-ci-e4": x(
    idea="В GitLab тестовый job просто указывает собранный образ в `image:` — script выполняется в нём.",
    lines=[
        ("stages: [build, test]", "Порядок этапов."),
        ("image: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA", "Образ этого коммита."),
        ("when: always\n    reports:\n      junit: report.xml", "Результаты в merge request — и при падении."),
    ],
    mistake="Забыть `when: always` — при упавших тестах отчёт не сохранится именно тогда, когда он нужен."),

f"{P}-ci-e5": x(
    idea="Промоутинг — новый тег на тот же дайджест; ничего не пересобирается.",
    lines=[("digest = registry[sha]", "Нет тега — KeyError сам."), ("return {**registry, new_tag: digest}", "Копия с новым тегом.")],
    mistake="`registry[new_tag] = …` — изменит исходный словарь."),

f"{P}-ci-e6": x(
    idea="Том выносит отчёты из контейнера на машину CI, `--rm` убирает контейнер.",
    lines=[('-v "$PWD/reports:/tests/reports"', "Папка CI ↔ папка в контейнере."), ("ghcr.io/acme/tests:$GITHUB_SHA", "Образ этого коммита.")],
    mistake="Относительный путь `-v reports:/tests/reports` — Docker поймёт его как имя тома, а не папку."),

f"{P}-ci-e7": x(
    idea="`--cache-from` берёт готовые слои из образа в реестре — DinD не начинает с нуля.",
    lines=[("--cache-from ghcr.io/acme/tests:latest", "Источник кэша."), ("-t ghcr.io/acme/tests:$GITHUB_SHA .", "Новый тег и контекст.")],
    mistake="Не скачать или не собрать образ-источник с inline-кэшем (`BUILDKIT_INLINE_CACHE=1`) — кэш не подхватится."),

f"{P}-ci-e8": x(
    idea="Дайджест неизменен: `образ@sha256:…` — ровно то содержимое, которое прошло тесты.",
    lines=[("docker pull ghcr.io/acme/tests@sha256:9f86d081884c7d65", "По отпечатку, а не по тегу.")],
    mistake="`docker pull ghcr.io/acme/tests:latest` — тег могли перезаписать после тестов."),
}
