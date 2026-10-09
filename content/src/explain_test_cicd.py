"""Тема «CI/CD для тестировщика» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py).
Часть заданий темы пришла из старой темы «Docker и CI» — у них префикс `dci`."""
from ._lib import x

P = "ci"
D = "dci"

EXPLAIN = {

# ===== Модуль 1. Основы CI/CD =====

f"{D}-m2-l1-e1": x(
    idea="Fail fast: первый упавший job останавливает пайплайн; `else` у цикла срабатывает, только если не было `break`.",
    lines=[
        ("if code != 0:", "Провал."),
        ("break", "Дальше не идём."),
        ('else:\n    print("🚀 всё зелёное")', "Сюда не дошли — был break."),
    ],
    mistake="Ожидать «всё зелёное» — `else` цикла не выполняется после break."),

f"{D}-m2-l1-e2": x(
    idea="Первый ненулевой код — провал с именем job-а; иначе успех.",
    lines=[("if code != 0:\n            return \"failed\", name", "Первый упавший."), ('return "success", None', "Все прошли.")],
    mistake="Возвращать последний упавший."),

f"{D}-m2-l1-e3": x(
    idea="Коды 0–5 подряд — удобно хранить в списке и брать по индексу.",
    lines=[('return ["all passed", "tests failed", "interrupted", "internal error", "usage error", "no tests collected"][code]', "Код = индекс.")],
    mistake="Считать код 5 успехом — тестов не нашлось, это тоже сигнал."),

f"{D}-m2-l1-e4": x(
    idea="Деплой — только с main и только при всех зелёных job-ах.",
    lines=[('return branch == "main" and all(code == 0 for code in jobs)', "Оба условия.")],
    mistake="`any` вместо `all` — выкатится с упавшими тестами."),

f"{D}-m2-l1-e5": x(
    idea="На каждом шаге запускаем готовый job (все зависимости выполнены), из нескольких — по алфавиту.",
    lines=[
        ("while len(done) < len(needs):", "Пока не все."),
        ("ready = sorted(j for j, deps in needs.items() if j not in done and all(d in done for d in deps))", "Готовые."),
        ("done.append(ready[0])", "Первый."),
    ],
    mistake="Запускать в порядке словаря — зависимость может оказаться позже."),

f"{D}-m2-l1-e6": x(
    idea="`a && b`: b запускается, только если a вернула 0; иначе возвращается код a.",
    lines=[
        ("return b() if code == 0 else code", "Логика `&&`."),
        ('print("exit", and_(lambda: run("ruff", 1), lambda: run("pytest", 0)))', "ruff упал — pytest не запускался."),
    ],
    mistake="Ждать «run pytest» в первом случае."),

f"{D}-m2-l1-e7": x(
    idea="`-x` — остановиться на первом упавшем тесте.",
    lines=[("pytest -x", "Быстрая обратная связь.")],
    mistake="Использовать в CI по умолчанию — не увидишь остальные падения."),

f"{D}-m2-l1-e8": x(
    idea="`&&` — второй шаг только после успешного первого.",
    lines=[("ruff check . && pytest", "Линтер, потом тесты.")],
    mistake="`;` — pytest запустится и после упавшего линтера."),

f"{P}-triggers-e1": x(
    idea="В YAML 1.1 `on` — это булево «да»; PyYAML превращает ключ в `True`. GitHub читает файл правильно.",
    lines=[("print(list(data))", "Ключ — True."), ("print(data[True])", "Значение под ним.")],
    mistake="Искать `data[\"on\"]` при разборе workflow в Python — KeyError."),

f"{P}-triggers-e2": x(
    idea="Под `on` — события; у push/PR — фильтр веток, у schedule — cron, `workflow_dispatch` — ручной запуск.",
    lines=[
        ("branches: [main]", "Только main."),
        ('- cron: "0 3 * * *"', "Каждую ночь в 03:00 UTC."),
        ("workflow_dispatch:", "Кнопка «Run workflow»."),
    ],
    mistake="Писать время cron по Москве — GitHub считает в UTC."),

f"{P}-triggers-e3": x(
    idea="Поля cron: минута, час, день, месяц, день недели; `1-5` — пн–пт.",
    lines=[("30 6 * * 1-5", "06:30 по будням.")],
    mistake="`6 30 * * 1-5` — сначала минуты, потом часы."),

f"{P}-triggers-e4": x(
    idea="`fnmatch` понимает шаблоны со `*`.",
    lines=[("return any(fnmatch(branch, p) for p in patterns)", "Хоть один подходит.")],
    mistake="Сравнивать `branch in patterns` — шаблоны не сработают."),

f"{P}-triggers-e5": x(
    idea="Хоть один изменённый файл под хоть одним шаблоном — запускаем UI-тесты.",
    lines=[("return any(fnmatch(f, p) for f in changed for p in paths)", "Все пары файл × шаблон.")],
    mistake="Проверять только первый изменённый файл."),

f"{P}-triggers-e6": x(
    idea="Событие должно быть в конфиге; фильтр веток — только если он задан.",
    lines=[
        ("if event not in config:\n        return False", "Событие не настроено."),
        ('branches = (config[event] or {}).get("branches")', "`None` у события без настроек → `{}`."),
        ("if branches is None:\n        return True", "Без фильтра — любая ветка."),
    ],
    mistake="`config[event].get(...)` — упадёт на `pull_request:` без значения (там None)."),

f"{P}-triggers-e7": x(
    idea="`gh workflow run` запускает workflow с `workflow_dispatch`.",
    lines=[("gh workflow run tests.yml", "Ручной запуск.")],
    mistake="Делать пустой коммит ради запуска."),

f"{P}-triggers-e8": x(
    idea="Событие запускает workflow, если ветка подходит под один из шаблонов этого события.",
    lines=[
        ("ok = any(fnmatch(branch, p) for p in on.get(event, []))", "Фильтр веток."),
        ("print(f\"{event:12} {branch:14} {'▶' if ok else '—'}\")", "`:12` — выравнивание."),
    ],
    mistake="Считать, что `feature/cart` подходит под `release/*`."),

f"{P}-jobs-e1": x(
    idea="Независимые job-ы идут параллельно: время — самая длинная цепочка.",
    lines=[
        ("start = max((finish[d] for d in needs[job]), default=0)", "Старт после всех зависимостей."),
        ("finish[job] = start + durations[job]", "Окончание."),
        ('print("пайплайн:", max(finish.values()), "мин, последовательно было бы", sum(durations.values()))', "15 против 22."),
    ],
    mistake="Складывать длительности всех job-ов."),

f"{P}-jobs-e2": x(
    idea="Волна — все job-ы, чьи зависимости уже выполнены; добавляем её целиком.",
    lines=[
        ("wave = sorted(j for j, deps in needs.items() if j not in done and all(d in done for d in deps))", "Готовые сейчас."),
        ("done.update(wave)", "Отмечаем всю волну."),
    ],
    mistake="Добавлять job-ы в `done` по одному внутри волны — следующий попадёт в ту же волну раньше времени."),

f"{P}-jobs-e3": x(
    idea="Окончание job-а = максимум окончаний зависимостей + своя длительность; запоминаем, чтобы не считать повторно.",
    lines=[
        ("if job not in finish:", "Ещё не считали."),
        ("finish[job] = max((end(d) for d in needs[job]), default=0) + durations[job]", "Рекурсия по зависимостям."),
        ("return max(end(job) for job in durations)", "Самый поздний."),
    ],
    mistake="Сумма длительностей зависимостей — они идут параллельно."),

f"{P}-jobs-e4": x(
    idea="`needs` задаёт зависимости; без него job-ы идут параллельно.",
    lines=[("lint:", "Без needs."), ("needs: [lint, unit]", "После обоих."), ("needs: [api-tests]", "После API-тестов.")],
    mistake="Забыть needs — UI-тесты стартуют одновременно с линтером."),

f"{P}-jobs-e5": x(
    idea="Пропуск распространяется по цепочке: повторяем, пока список пропущенных растёт.",
    lines=[
        ("while changed:", "Пока что-то добавилось."),
        ("if job not in bad and job not in skipped and any(d in bad or d in skipped for d in deps):", "Зависит от упавшего или пропущенного."),
        ("skipped.add(job)\n                changed = True", "Ещё один пропуск."),
    ],
    mistake="Один проход — непрямые зависимости потеряются."),

f"{P}-jobs-e6": x(
    idea="Шард — срез с шагом: раннер i берёт каждый total-й тест, начиная с i-го.",
    lines=[("return tests[index - 1::total]", "Индекс с 1 → срез с 0.")],
    mistake="`tests[index::total]` — сдвиг на один."),

f"{P}-jobs-e7": x(
    idea="`-n auto` — по числу ядер раннера.",
    lines=[("pytest -n auto", "Параллельно внутри job-а.")],
    mistake="Ставить фиксированное число — на другом раннере ядер может быть меньше."),

f"{P}-jobs-e8": x(
    idea="Если хоть одна зависимость не успешна — job пропускается.",
    lines=[('if any(result[d] != "success" for d in needs[job]):', "Зависимость упала или пропущена."), ('result[job] = "skipped"', "Пропуск.")],
    mistake="Ожидать, что ui выполнится — он зависит от пропущенного api."),

f"{P}-artifacts-e1": x(
    idea="Артефакт с `if: always()` сохраняет отчёты и при упавших тестах.",
    lines=[
        ("- run: pytest --junitxml=reports/junit.xml", "Отчёт в папку."),
        ("- uses: actions/upload-artifact@v4", "Загрузка."),
        ("if: always()", "Даже после провала."),
    ],
    mistake="Без `always()` — при упавших тестах шаг пропустится."),

f"{P}-artifacts-e2": x(
    idea="Ключ кэша — хеш файла зависимостей: изменился файл — новый ключ.",
    lines=[
        ("digest = hashlib.sha256(requirements.encode()).hexdigest()[:8]", "Первые 8 символов хеша."),
        ("print(a == b, a == c)", "Одинаковый текст — одинаковый ключ."),
        ("print(len(a))", "`pip-linux-` (10) + 8."),
    ],
    mistake="Ключ без хеша — кэш не обновится после изменения зависимостей."),

f"{P}-artifacts-e3": x(
    idea="ОС и версия Python в ключе — у разных раннеров свои кэши.",
    lines=[("digest = hashlib.sha256(requirements.encode()).hexdigest()[:12]", "12 символов."), ('return f"pip-{os_name}-{python}-{digest}"', "Формат ключа.")],
    mistake="Один кэш на все ОС — пакеты с бинарниками не подойдут."),

f"{P}-artifacts-e4": x(
    idea="JUnit XML — формат, который понимают все CI.",
    lines=[("pytest --junitxml=reports/junit.xml", "Отчёт.")],
    mistake="Сохранять только текстовый вывод."),

f"{P}-artifacts-e5": x(
    idea="Markdown-сводка: строка с цифрами и список упавших, если они есть.",
    lines=[
        ("count = lambda status: sum(1 for r in results.values() if r == status)", "Подсчёт по статусу."),
        ("failed = sorted(name for name, r in results.items() if r == \"failed\")", "Упавшие."),
        ('lines += ["", "Упали:"] + [f"- {name}" for name in failed]', "Список Markdown."),
    ],
    mistake="Выводить заголовок «Упали» и при нуле падений."),

f"{P}-artifacts-e6": x(
    idea="`>>` дописывает строку в файл сводки.",
    lines=[('echo "### Итоги" >> $GITHUB_STEP_SUMMARY', "Markdown на странице запуска.")],
    mistake="`>` — перезапишет то, что уже написали другие шаги."),

f"{P}-artifacts-e7": x(
    idea="Значения матрицы по алфавиту ключей, проблемные символы — в `_`.",
    lines=[('parts = [prefix] + [str(matrix[k]).replace("/", "_").replace(" ", "_") for k in sorted(matrix)]', "Стабильный порядок."), ('return "-".join(parts)', "Через дефис.")],
    mistake="Порядок словаря — имя зависит от порядка ключей в YAML."),

f"{P}-artifacts-e8": x(
    idea="`gh run download` скачивает артефакты запуска.",
    lines=[("gh run download 9876543210", "Номер запуска."), ("-n reports", "Имя артефакта.")],
    mistake="Скачивать zip вручную через браузер."),

# ===== Модуль 2. GitHub Actions =====

f"{D}-m2-l2-e1": x(
    idea="CI заменяет значения секретов на `***` в логах.",
    lines=[('log = log.replace(secret, "***")', "Каждый секрет.")],
    mistake="Печатать секреты в лог, надеясь на маскировку, — изменённый (например, base64) не замаскируется."),

f"{D}-m2-l2-e2": x(
    idea="Базовый workflow: скачать код, поставить Python и зависимости, запустить тесты.",
    lines=[
        ("on: [push, pull_request]", "Два события."),
        ("- uses: actions/checkout@v4", "Код репозитория."),
        ('python-version: "3.12"', "В кавычках — иначе 3.10 станет 3.1."),
        ("- run: pytest", "Тесты."),
    ],
    mistake="Забыть checkout — в раннере пусто."),

f"{D}-m2-l2-e3": x(
    idea="Пустой секрет пропускаем — `replace(\"\", …)` вставил бы `***` между каждым символом.",
    lines=[("if s:", "Только непустые."), ('log = log.replace(s, "***")', "Все вхождения.")],
    mistake="Не проверить пустую строку — лог станет нечитаемым."),

f"{D}-m2-l2-e4": x(
    idea="Матрица — декартово произведение значений; `zip` с ключами даёт словарь запуска.",
    lines=[("keys = list(matrix)", "Порядок параметров."), ("return [dict(zip(keys, combo)) for combo in product(*matrix.values())]", "Все комбинации.")],
    mistake="`product(matrix.values())` без `*` — один аргумент-список."),

f"{D}-m2-l2-e5": x(
    idea="Упавший тест — с `<failure>` или `<error>` внутри; пропущенный — со `<skipped>`.",
    lines=[
        ('cases = list(root.iter("testcase"))', "Все тесты."),
        ('failed = [c for c in cases if c.find("failure") is not None or c.find("error") is not None]', "`is not None` — пустой элемент ложен."),
        ('"failed_names": [c.get("name") for c in failed],', "Имена."),
    ],
    mistake="`if c.find(\"failure\")` — элемент без детей считается ложным."),

f"{D}-m2-l2-e6": x(
    idea="`gh run list` — последние запуски.",
    lines=[("gh run list", "Статусы запусков.")],
    mistake="`gh workflow list` — это список workflow, а не запусков."),

f"{D}-m2-l2-e7": x(
    idea="`--log-failed` — логи только упавших шагов.",
    lines=[("gh run view 9876543210", "Запуск."), ("--log-failed", "Только упавшее.")],
    mistake="`--log` — весь лог, искать долго."),

f"{D}-m2-l2-e8": x(
    idea="`rerun --failed` перезапускает только упавшие job-ы.",
    lines=[("gh run rerun 9876543210 --failed", "Экономит время.")],
    mistake="Перезапускать весь пайплайн."),

f"{P}-matrix-e1": x(
    idea="Матрица — все комбинации параметров, каждая — отдельный запуск.",
    lines=[("runs = [dict(zip(matrix, combo)) for combo in product(*matrix.values())]", "2 × 2 = 4."), ('print(run["os"], run["python"])', "Правый параметр меняется быстрее.")],
    mistake="Ожидать 2 запуска — это не zip, а произведение."),

f"{P}-matrix-e2": x(
    idea="Сначала все комбинации, затем убираем `exclude`, в конце добавляем `include`.",
    lines=[
        ('keys = [k for k in matrix if k not in ("exclude", "include")]', "Только параметры."),
        ("runs = [r for r in runs if not all(r.get(k) == v for k, v in ex.items())]", "Совпали все ключи exclude — убрать."),
        ('return runs + list(matrix.get("include", []))', "Добавить свои."),
    ],
    mistake="Включить `exclude` в декартово произведение как параметр."),

f"{P}-matrix-e3": x(
    idea="`fail-fast: false` — упал один браузер, остальные доигрывают; значение подставляется выражением `${{ matrix.browser }}`.",
    lines=[("fail-fast: false", "Все браузеры до конца."), ("browser: [chromium, firefox, webkit]", "Три запуска."), ("- run: pytest --browser ${{ matrix.browser }}", "Значение из матрицы.")],
    mistake="Оставить fail-fast по умолчанию — не узнаешь, падает ли в других браузерах."),

f"{P}-matrix-e4": x(
    idea="Регулярка ловит `${{ путь }}`; путь проходим по вложенным словарям, нет ключа — пустая строка.",
    lines=[
        ('for key in m.group(1).split("."):', "Части пути."),
        ('if not isinstance(node, dict) or key not in node:\n                return ""', "Нет — пусто."),
        ('return re.sub(r"\\$\\{\\{\\s*([\\w.-]+)\\s*\\}\\}", value, template)', "Пробелы внутри — не важны."),
    ],
    mistake="Падать с KeyError — GitHub подставляет пустую строку."),

f"{P}-matrix-e5": x(
    idea="С fail-fast первое падение отменяет оставшиеся запуски.",
    lines=[('status[browser] = "cancelled" if stopped else result', "После падения — отмена."), ('if result == "failure" and fail_fast:', "Только при fail-fast.")],
    mistake="Думать, что fail-fast отменяет уже завершившиеся."),

f"{P}-matrix-e6": x(
    idea="Стенд выбираем по ссылке git: main, тег версии, PR, остальное.",
    lines=[
        ('if ref == "refs/heads/main":', "Ветка main."),
        ('if ref.startswith("refs/tags/v"):', "Релиз."),
        ('if ref.startswith("refs/pull/"):', "Pull request."),
    ],
    mistake="Проверять `\"main\" in ref` — сработает на `refs/heads/feature/main-page`."),

f"{P}-matrix-e7": x(
    idea="`github.ref` — полная ссылка; для main — `refs/heads/main`.",
    lines=[("github.ref == 'refs/heads/main'", "Условие шага.")],
    mistake="`github.ref == 'main'` — ref содержит префикс refs/heads."),

f"{P}-matrix-e8": x(
    idea="include дополняет совпавшую комбинацию новыми ключами, а без совпадения — добавляет новую.",
    lines=[
        ("match = next((r for r in runs if all(r.get(k) == v for k, v in base.items())), None)", "Ищем комбинацию."),
        ("match.update(extra)", "chromium получил headed."),
        ("runs.append(dict(extra))", "webkit — новый запуск."),
    ],
    mistake="Ждать отдельный второй chromium."),

f"{P}-secrets-e1": x(
    idea="Настройки тестов — из переменных окружения; секрета нет — `None`.",
    lines=[('base_url = os.environ.get("BASE_URL", "http://localhost:8000")', "Задан — берём."), ('token = os.environ.get("API_TOKEN")', "Не задан — None.")],
    mistake="`os.environ[\"API_TOKEN\"]` — KeyError вместо понятной обработки."),

f"{P}-secrets-e2": x(
    idea="Проверяем все обязательные переменные сразу и называем недостающие.",
    lines=[("missing = [n for n in names if not env.get(n)]", "Нет или пустая."), ('raise RuntimeError("Не заданы: " + ", ".join(missing))', "Понятная ошибка."), ("return {n: env[n] for n in names}", "Только нужные.")],
    mistake="Падать на первой недостающей — придётся перезапускать по одной."),

f"{P}-secrets-e3": x(
    idea="`env` на уровне job-а доступен всем шагам; `vars` — настройки, `secrets` — секреты.",
    lines=[("BASE_URL: ${{ vars.STAGE_URL }}", "Обычная переменная."), ("API_TOKEN: ${{ secrets.API_TOKEN }}", "Маскируется в логах.")],
    mistake="Хранить токен в `vars` — он виден в логах."),

f"{P}-secrets-e4": x(
    idea="Ищем по шаблонам строки, похожие на токены и пароли.",
    lines=[('PATTERNS = [r"Bearer [A-Za-z0-9._-]{20,}", r"ghp_[A-Za-z0-9]{36}", r"password=\\S+"]', "Три признака утечки."), ("if any(re.search(p, line) for p in PATTERNS)]", "Номера строк.")],
    mistake="`re.match` — ищет только с начала строки."),

f"{P}-secrets-e5": x(
    idea="`gh secret set` добавляет секрет; значение вводится без эха.",
    lines=[("gh secret set API_TOKEN", "Секрет репозитория.")],
    mistake="Передавать значение в аргументе — останется в истории оболочки."),

f"{P}-secrets-e6": x(
    idea="Команда `::add-mask::значение` просит GitHub скрывать значение в логах дальше.",
    lines=[('echo "::add-mask::$TOKEN"', "Маска для динамического секрета.")],
    mistake="Печатать токен до маскировки — он уже в логе."),

f"{P}-secrets-e7": x(
    idea="Правила `.gitignore` применяются по порядку: последнее подходящее решает, `!` отменяет.",
    lines=[
        ('negate = line.startswith("!")', "Исключение."),
        ('pattern = line.lstrip("!").lstrip("/")', "Чистый шаблон."),
        ('if fnmatch(".env", pattern):\n            ignored = not negate', "Последнее совпадение побеждает."),
    ],
    mistake="Остановиться на первом совпадении — `!.env` ниже не учтётся."),

f"{P}-secrets-e8": x(
    idea="PR из форка не получает секретов — иначе любой мог бы их украсть.",
    lines=[('if event == "pull_request" and from_fork:\n        return ""', "Пусто для форка.")],
    mistake="Думать, что тесты из форка получат токен."),

f"{P}-docker-e1": x(
    idea="`services` поднимает контейнеры рядом с job-ом; healthcheck ждёт готовности базы.",
    lines=[
        ("image: postgres:16", "Сервис базы."),
        ('--health-cmd "pg_isready -U postgres"', "Проверка готовности."),
        ("DATABASE_URL: postgresql://postgres:secret@localhost:5432/postgres", "С раннера — localhost и опубликованный порт."),
    ],
    mistake="Хост `postgres` в адресе — job работает на раннере, а не в контейнере."),

f"{P}-docker-e2": x(
    idea="Теги образа: всегда по коммиту, плюс ветка (и latest для main) или версия тега.",
    lines=[
        ('tags = [f"{image}:sha-{sha[:7]}"]', "Короткий хеш."),
        ("tags.append(f\"{image}:{branch.replace('/', '-')}\")", "В теге нельзя `/`."),
        ("tags.append(f\"{image}:{ref[len('refs/tags/v'):]}\")", "Версия без `v`."),
    ],
    mistake="Оставить `/` в имени ветки — Docker не примет тег."),

f"{P}-docker-e3": x(
    idea="Тег по хешу коммита — образ однозначно связан с кодом.",
    lines=[("docker build -t ghcr.io/acme/tests:$GITHUB_SHA .", "Переменная раннера.")],
    mistake="Тег latest в CI — неясно, какой код внутри."),

f"{P}-docker-e4": x(
    idea="`--exit-code-from tests` делает код шага кодом тестов; `--build` — свежие образы.",
    lines=[("docker compose up --build", "Пересобрать."), ("--exit-code-from tests", "Код тестов.")],
    mistake="`docker compose up -d` — CI не узнает результат."),

f"{P}-docker-e5": x(
    idea="Отчёты и уборка — с `if: always()`, чтобы выполнились и после падения.",
    lines=[
        ("- run: docker compose up --build --exit-code-from tests", "Прогон."),
        ("if: always()", "Отчёт и при провале."),
        ("- run: docker compose down -v", "Уборка."),
    ],
    mistake="Уборка без always() — после падения стенд останется."),

f"{P}-docker-e6": x(
    idea="После упавшего шага выполняются только шаги с `always()` и `failure()`.",
    lines=[
        ('return {"success()": not failed_before, "always()": True, "failure()": failed_before}[condition]', "Таблица условий."),
        ('if name == "pytest":\n            failed = True', "Тесты упали."),
    ],
    mistake="Ждать deploy — success() после падения ложно."),

f"{P}-docker-e7": x(
    idea="`--password-stdin` читает токен из входа — его не будет в списке процессов и логах.",
    lines=[('echo "$CR_TOKEN"', "Токен в конвейер."), ("| docker login ghcr.io -u acme --password-stdin", "Вход.")],
    mistake="`-p $CR_TOKEN` — токен виден в аргументах."),

f"{P}-docker-e8": x(
    idea="Снимаем `${{ }}`, затем решаем по таблице; пустое условие = success().",
    lines=[
        ('if cond.startswith("${{") and cond.endswith("}}"):', "Обёртка выражения."),
        ('failed = "failure" in previous', "Было ли падение."),
        ('return {"": not failed, "success()": not failed, "failure()": failed,', "Пропущенные шаги провалом не считаются."),
    ],
    mistake="Считать skipped падением."),

# ===== Модуль 3. Качество и практика =====

f"{P}-gitlab-e1": x(
    idea="Стадии идут по очереди, job-ы одной стадии — параллельно.",
    lines=[('jobs = [name for name, job in ci.items() if isinstance(job, dict) and job.get("stage") == stage]', "Job-ы стадии; `stages` — список, его пропускаем."), ("print(stage, jobs)", "У report — пусто.")],
    mistake="Посчитать `stages` job-ом."),

f"{P}-gitlab-e2": x(
    idea="В GitLab: `stages`, у job-а — `stage`, `image`, `script`; отчёт JUnit — в `artifacts.reports`.",
    lines=[("stage: lint", "Первая стадия."), ("- pytest --junitxml=report.xml", "Отчёт."), ("junit: report.xml", "GitLab покажет результаты в MR.")],
    mistake="Забыть `when: always` — при падении отчёт не сохранится."),

f"{P}-gitlab-e3": x(
    idea="Job — словарь со `script` и именем не с точки; стадия по умолчанию — test.",
    lines=[
        ('if isinstance(job, dict) and "script" in job and not name.startswith(".")}', "Отбор job-ов."),
        ('names = sorted(n for n, j in jobs.items() if j.get("stage", "test") == stage)', "По алфавиту."),
        ("if names:\n            plan.append((stage, names))", "Пустые стадии не добавляем."),
    ],
    mistake="Считать шаблоны `.base` job-ами."),

f"{P}-gitlab-e4": x(
    idea="`rules` проверяются по порядку: первое совпавшее правило решает, как запускать job.",
    lines=[('- if: $CI_PIPELINE_SOURCE == "schedule"', "По расписанию — автоматически."), ('- if: $CI_COMMIT_BRANCH == "main"', "В main…"), ("when: manual", "…только вручную.")],
    mistake="Поставить правила в обратном порядке — расписание в main станет ручным."),

f"{P}-gitlab-e5": x(
    idea="Имя ветки — `$CI_COMMIT_BRANCH`.",
    lines=[("$CI_COMMIT_BRANCH", "Текущая ветка.")],
    mistake="`$CI_BRANCH` — такой переменной нет."),

f"{P}-gitlab-e6": x(
    idea="Полный хеш — `$CI_COMMIT_SHA`, короткий — `$CI_COMMIT_SHORT_SHA`.",
    lines=[("$CI_COMMIT_SHA", "Хеш коммита.")],
    mistake="Путать с `$GITHUB_SHA` из GitHub Actions."),

f"{P}-gitlab-e7": x(
    idea="`extends` — настройки шаблона, поверх — свои ключи job-а.",
    lines=[('resolved = {**base, **{k: v for k, v in api.items() if k != "extends"}}', "Шаблон + job без extends."), ("for key in sorted(resolved):", "По алфавиту.")],
    mistake="Оставить ключ extends в итоге."),

f"{P}-gitlab-e8": x(
    idea="Рекурсия: сначала разворачиваем шаблон, потом накладываем ключи job-а.",
    lines=[('parent = job.pop("extends", None)', "Убираем extends из копии."), ("return {**resolve_extends(ci, parent), **job}", "Шаблон снизу, job сверху.")],
    mistake="Менять `ci[name]` напрямую — испортишь исходный словарь."),

f"{P}-gates-e1": x(
    idea="`--cov-fail-under` превращает покрытие в условие прохождения.",
    lines=[("pytest --cov=app", "Замер для пакета."), ("--cov-fail-under=80", "Ниже 80% — провал.")],
    mistake="Мерить покрытие без порога — оно будет тихо падать."),

f"{P}-gates-e2": x(
    idea="`line-rate` — доля от 0 до 1; переводим в проценты.",
    lines=[('return round(float(root.get("line-rate")) * 100, 1)', "Строка → float → %.")],
    mistake="Забыть float — атрибут XML — строка."),

f"{P}-gates-e3": x(
    idea="Каждое правило проверяется, только если задано; нарушения копятся списком.",
    lines=[
        ('if "max_failed" in rules and stats["failed"] > rules["max_failed"]:', "Упавшие."),
        ('if "min_coverage" in rules and stats["coverage"] < rules["min_coverage"]:', "Покрытие."),
        ('if "max_skipped_share" in rules and total and stats["skipped"] / total > rules["max_skipped_share"]:', "Доля пропусков; `total` — защита от деления на ноль."),
    ],
    mistake="Падать на отсутствующем правиле с KeyError."),

f"{P}-gates-e4": x(
    idea="Карантин: падения известных флаки-тестов показываем, но пайплайн не краснеет.",
    lines=[('real = [t for t, r in results.items() if r == "failed" and t not in quarantine]', "Настоящие падения."), ('print("пайплайн:", "красный" if real else "зелёный")', "Решают только они.")],
    mistake="Держать тесты в карантине вечно — их нужно чинить."),

f"{P}-gates-e5": x(
    idea="Множества упавших до и после: разность — новые, пересечение — старые, прошедшие теперь — исправленные.",
    lines=[
        ('fixed = {t for t in failed_before if after.get(t) == "passed"}', "Починили."),
        ('return {"new": sorted(failed_after - failed_before),', "Новые падения."),
        ('"still": sorted(failed_after & failed_before)}', "Падали и падают."),
    ],
    mistake="Считать исправленным тест, который в ветке пропущен."),

f"{P}-gates-e6": x(
    idea="Линтер и проверка формата — два независимых барьера.",
    lines=[("ruff check .", "Ошибки."), ("ruff format --check .", "Формат без изменений.")],
    mistake="`ruff format .` в CI — исправит файлы и пройдёт."),

f"{P}-gates-e7": x(
    idea="Собираем (имя, время) и сортируем по убыванию времени.",
    lines=[('cases = [(c.get("name"), float(c.get("time", 0))) for c in ET.fromstring(junit_xml).iter("testcase")]', "Время — число."), ("return sorted(cases, key=lambda c: c[1], reverse=True)[:n]", "Топ-n.")],
    mistake="Сортировать строки времени."),

f"{P}-gates-e8": x(
    idea="`--durations=N` — N самых медленных тестов.",
    lines=[("pytest --durations=10", "Кандидаты на оптимизацию.")],
    mistake="Оценивать скорость тестов на глаз."),

f"{P}-notify-e1": x(
    idea="`allure generate` строит отчёт; `--clean` — очистить старый.",
    lines=[("allure generate allure-results", "Откуда."), ("-o allure-report --clean", "Куда, с очисткой.")],
    mistake="Без `--clean` — ошибка на существующей папке."),

f"{P}-notify-e2": x(
    idea="Иконка по наличию падений, до пяти имён упавших, ссылка в конце.",
    lines=[
        ('icon = "❌" if summary["failed"] else "✅"', "Статус."),
        ('lines += [f"• {name}" for name in names[:5]]', "Первые пять."),
        ('lines.append(f"…и ещё {len(names) - 5}")', "Остальные числом."),
    ],
    mistake="Перечислять все упавшие — сообщение станет простынёй."),

f"{P}-notify-e3": x(
    idea="По умолчанию `json.dumps` экранирует не-ASCII символы; `ensure_ascii=False` оставляет как есть.",
    lines=[("print(json.dumps(payload))", "`\\u…` вместо букв."), ("print(json.dumps(payload, ensure_ascii=False))", "Читаемо.")],
    mistake="Думать, что экранированный JSON неправильный — он валиден, просто нечитаем."),

f"{P}-notify-e4": x(
    idea="Уведомляем о падении и о смене статуса (починили); зелёный после зелёного — тишина.",
    lines=[('if cur == "failure":\n        return True', "Упал — всегда."), ("return prev is not None and prev != cur", "Сменился статус.")],
    mistake="Уведомлять на первый зелёный прогон — prev ещё None."),

f"{P}-notify-e5": x(
    idea="Вебхук — POST с JSON; адрес из переменной.",
    lines=[('-H "Content-Type: application/json"', "Тип тела."), ("-d '{\"text\": \"tests failed\"}'", "JSON в одинарных кавычках."), ("$WEBHOOK_URL", "Адрес.")],
    mistake="JSON в двойных кавычках — оболочка съест внутренние кавычки."),

f"{P}-notify-e6": x(
    idea="Последние 5 прогонов; полоска — число прошедших и упавших по десяткам.",
    lines=[
        ("runs = history + [current]", "История + текущий."),
        ("start = max(0, len(runs) - 5)", "Последние пять."),
        ('return [f"{i + 1} " + "█" * (r["passed"] // 10) + "░" * (r["failed"] // 10)', "Номер прогона сохраняется."),
    ],
    mistake="Нумеровать срез заново с 1 — номера прогонов собьются."),

f"{P}-notify-e7": x(
    idea="Копия `history` из прошлого отчёта даёт тренды в новом.",
    lines=[("cp -r allure-report/history allure-results/", "До генерации.")],
    mistake="Копировать после `allure generate` — история не попадёт."),

f"{P}-notify-e8": x(
    idea="Генерация и загрузка отчёта — с `if: always()`.",
    lines=[("- run: pytest --alluredir=allure-results", "Результаты."), ("- run: allure generate allure-results -o allure-report --clean", "Отчёт."), ("name: allure-report", "Артефакт.")],
    mistake="Без always() — отчёт появится только у зелёных прогонов, когда он не нужен."),

f"{P}-practice-e1": x(
    idea="Полный пайплайн: линтер → API → UI по матрице браузеров; отчёты — с always().",
    lines=[
        ("needs: lint", "API после линтера."),
        ("- run: pytest tests/api --junitxml=reports/api.xml", "Отчёт."),
        ("fail-fast: false", "Все браузеры до конца."),
        ("- run: pytest tests/ui --browser ${{ matrix.browser }}", "Браузер из матрицы."),
    ],
    mistake="UI без needs — тратит раннеры, даже когда линтер красный."),

f"{P}-practice-e2": x(
    idea="Проходим job-ы и копим коды проблем во множество.",
    lines=[
        ('if not any(u.startswith("actions/checkout") for u in uses):', "Нет checkout."),
        ('if any("@" not in u for u in uses):', "Действие без версии."),
        ('if s.get("uses", "").startswith("actions/upload-artifact") and "always()" not in str(s.get("if", "")):', "Артефакт без always()."),
        ('if "timeout-minutes" not in job:', "Нет таймаута."),
    ],
    mistake="Список вместо множества — повторы кодов из разных job-ов."),

f"{P}-practice-e3": x(
    idea="Одно падение — весь пайплайн красный; пропущенные job-ы итог не меняют.",
    lines=[('print(" ".join(f"{icons[s]} {name}" for name, s in jobs.items()))', "Строка статусов."), ('overall = "failure" if "failure" in jobs.values() else "success"', "Итог.")],
    mistake="Считать skipped провалом."),

f"{P}-practice-e4": x(
    idea="Каждый testcase попадает ровно в одну категорию: упал, пропущен или прошёл.",
    lines=[
        ('if case.find("failure") is not None or case.find("error") is not None:', "Упал."),
        ("summary[\"failed_names\"].append(f\"{case.get('classname')}::{case.get('name')}\")", "Полное имя."),
        ('elif case.find("skipped") is not None:', "Пропущен."),
        ('summary["passed"] += 1', "Иначе — прошёл."),
    ],
    mistake="Считать прошедшими только кейсы с атрибутом — у прошедших нет вложенных тегов."),

f"{P}-practice-e5": x(
    idea="Упавший тест воспроизводят точечно — по id узла, с подробным выводом.",
    lines=[("pytest tests/ui/test_cart.py::test_remove_item", "Один тест."), ("-v", "Подробно.")],
    mistake="Запускать весь набор ради одного теста."),

f"{P}-practice-e6": x(
    idea="`timeout-minutes` — предел времени job-а или шага.",
    lines=[("timeout-minutes", "По умолчанию 360 минут — слишком много.")],
    mistake="Не задавать — зависший тест съест 6 часов раннера."),

f"{P}-practice-e7": x(
    idea="Прошёл с первой попытки — passed; позже — flaky; ни разу — failed.",
    lines=[
        ('if results[0] == "passed":', "Сразу."),
        ('elif "passed" in results:', "Со второй и далее — флаки."),
        ("return {k: sorted(v) for k, v in report.items()}", "Списки по алфавиту."),
    ],
    mistake="Считать флаки обычным прохождением — пайплайн зелёный, а проблема остаётся."),

f"{P}-practice-e8": x(
    idea="Branch protection: «Require status checks to pass» — без зелёного CI слить нельзя.",
    lines=[("status", "Status checks.")],
    mistake="Полагаться на договорённость «не мержим красное»."),
}
