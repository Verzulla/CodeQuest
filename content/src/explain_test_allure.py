"""Тема «Allure и отчёты» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "alr"

EXPLAIN = {

# ===== Модуль 1. Allure в тестах =====

f"{P}-intro-e1": x(
    idea="`allure-pytest` — плагин, который во время прогона пишет результаты в формате Allure.",
    lines=[("pip install allure-pytest", "Плагин для pytest.")],
    mistake="`pip install allure` — это другой пакет; генератор отчётов ставится отдельно."),

f"{P}-intro-e2": x(
    idea="`--alluredir` — куда плагин сложит JSON-файлы результатов.",
    lines=[("pytest --alluredir=allure-results", "Сырые результаты.")],
    mistake="Ждать HTML-отчёт сразу — это только данные для него."),

f"{P}-intro-e3": x(
    idea="`allure generate` строит HTML из результатов; `-o` — куда, `--clean` — очистить папку.",
    lines=[("allure generate allure-results", "Откуда."), ("-o allure-report", "Куда."), ("--clean", "Без старых файлов.")],
    mistake="Без `--clean` — ошибка, если папка отчёта уже есть."),

f"{P}-intro-e4": x(
    idea="`allure serve` генерирует отчёт во временную папку и открывает браузер.",
    lines=[("allure serve allure-results", "Быстрый просмотр.")],
    mistake="Открыть `index.html` двойным кликом — отчёт не загрузится без веб-сервера."),

f"{P}-intro-e5": x(
    idea="`allure open` поднимает веб-сервер для готового отчёта.",
    lines=[("allure open allure-report", "Открыть сгенерированное.")],
    mistake="`allure serve allure-report` — serve ждёт результаты, а не отчёт."),

f"{P}-intro-e6": x(
    idea="Командная утилита Allure написана на Java — ей нужна Java.",
    lines=[("Java", "Без неё команда `allure` не запустится.")],
    mistake="Думать, что хватит `allure-pytest` — это только плагин для записи результатов."),

f"{P}-intro-e7": x(
    idea="Один тест — один файл `*-result.json`; container — фикстуры, attachment — вложения.",
    lines=[("1b2c-result.json   7f8e-result.json   9a0b-result.json", "Три теста.")],
    mistake="Посчитать все файлы папки."),

f"{P}-intro-e8": x(
    idea="Для базового отчёта ничего добавлять не нужно — плагин сам запишет результат.",
    lines=[("import allure", "Импорт — для проверки, что плагин стоит."), ('assert health() == "ok"', "Обычный тест.")],
    mistake="Думать, что без шагов и меток тест в отчёт не попадёт."),

f"{P}-steps-e1": x(
    idea="`with allure.step(\"…\")` — именованный шаг в отчёте; всё внутри блока относится к нему.",
    lines=[
        ('with allure.step("Открыть страницу входа"):', "Первый шаг."),
        ('assert enter("anna", "secret")', "Проверка внутри шага."),
        ('with allure.step("Проверить приветствие"):', "Последний шаг."),
    ],
    mistake="Писать шаги комментариями — в отчёте их не будет."),

f"{P}-steps-e2": x(
    idea="Декоратор `@allure.step` делает шагом каждый вызов; `{item}` подставит аргумент.",
    lines=[
        ('@allure.step("Добавить {item} в корзину")', "Название с параметром."),
        ('add_to_cart("чай")', "Шаг «Добавить 'чай' в корзину»."),
    ],
    mistake="f-строка в декораторе — `item` ещё не существует при объявлении."),

f"{P}-steps-e3": x(
    idea="Вложенные `with` дают дерево шагов.",
    lines=[
        ('with allure.step("Оформить заказ"):', "Родитель."),
        ('with allure.step("Заполнить адрес"):', "Вложенный."),
        ('with allure.step("Оплатить"):', "Вложенный."),
    ],
    mistake="Поставить шаги подряд без отступа — получатся три шага одного уровня."),

f"{P}-steps-e4": x(
    idea="Упавший шаг отмечен ✗; после него шаги не выполнялись (·).",
    lines=[("✗ Оплатить", "Здесь упало.")],
    mistake="Ответить «Проверить письмо» — до него не дошли."),

f"{P}-steps-e5": x(
    idea="Строковый аргумент подставляется в название через repr — с кавычками.",
    lines=[("Войти как 'anna'", "Значение параметра в названии.")],
    mistake="Ожидать `{user}` в названии буквально."),

f"{P}-steps-e6": x(
    idea="Упавший `assert` внутри шага помечает этот шаг — в отчёте видно, где именно сломалось.",
    lines=[
        ('order = {"id": 1}', "Шаг «Создать заказ» прошёл."),
        ('assert pay() == "paid"', "Шаг «Проверить статус» упал."),
    ],
    mistake="Делать все проверки в конце теста вне шагов."),

f"{P}-steps-e7": x(
    idea="`failed` — не прошла проверка (`assert`), `broken` — тест сломался другим исключением.",
    lines=[("assert", "failed = упавший assert.")],
    mistake="Считать broken и failed одним и тем же — broken часто значит проблему в тесте или окружении."),

f"{P}-steps-e8": x(
    idea="Методы Page Object со `@allure.step` — тест читается как сценарий, а шаги появляются в отчёте сами.",
    lines=[
        ('@allure.step("Открыть страницу входа")', "Шаг-метод."),
        ('@allure.step("Войти как {user}")', "Параметр в названии."),
        ('page.login("anna")', "Вызов — шаг в отчёте."),
    ],
    mistake="Писать `allure.step` в каждом тесте вручную — дублирование."),

f"{P}-attach-e1": x(
    idea="`allure.attach` прикладывает данные к тесту; тип определяет, как их показать.",
    lines=[
        ('allure.attach(json.dumps(body), name="response", attachment_type=allure.attachment_type.JSON)', "Строка JSON + имя + тип."),
        ('assert body["status"] == "active"', "Проверка — после вложения, чтобы оно было и при падении."),
    ],
    mistake="Передать словарь без `json.dumps` — нужна строка."),

f"{P}-attach-e2": x(
    idea="Вложение внутри шага привязывается к этому шагу.",
    lines=[
        ('with allure.step("Выполнить запрос"):', "Шаг."),
        ('allure.attach("GET /users -> 200", name="request", attachment_type=allure.attachment_type.TEXT)', "Текстовый лог."),
    ],
    mistake="Приложить вне шага — лог окажется у теста целиком."),

f"{P}-attach-e3": x(
    idea="`allure.attach.file` прикладывает файл с диска.",
    lines=[
        ('path.write_text("id,status\\n1,ok\\n", encoding="utf-8")', "Готовим файл."),
        ('allure.attach.file(path, name="report", attachment_type=allure.attachment_type.CSV)', "Прикладываем."),
    ],
    mistake="`allure.attach(path, ...)` — приложится строка пути, а не содержимое."),

f"{P}-attach-e4": x(
    idea="Скриншот — изображение PNG.",
    lines=[("PNG", "`allure.attachment_type.PNG`.")],
    mistake="TEXT — картинка не отобразится."),

f"{P}-attach-e5": x(
    idea="`pytest_runtest_makereport` вызывается после этапов теста — там видно, упал ли он.",
    lines=[("pytest_runtest_makereport", "Хук отчёта о тесте.")],
    mistake="`pytest_sessionfinish` — один раз на весь прогон."),

f"{P}-attach-e6": x(
    idea="Скриншот — только при падении, иначе отчёт разрастается.",
    lines=[
        ("if not passed:", "Только при неудаче."),
        ('allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)', "Байты как PNG."),
        ("assert False", "`test_bad` падает — вложение есть."),
    ],
    mistake="Прикладывать скриншот всегда."),

f"{P}-attach-e7": x(
    idea="Каждый вызов `allure.attach` — одно вложение.",
    lines=[('allure.attach(req, name="request", attachment_type=allure.attachment_type.JSON)', "1."), ('allure.attach(resp, name="response", attachment_type=allure.attachment_type.JSON)', "2.")],
    mistake="Посчитать шаг вложением."),

f"{P}-attach-e8": x(
    idea="Помощник оформляет запрос как шаг с двумя вложениями — тесты остаются короткими.",
    lines=[
        ('with allure.step(f"{method} {url}"):', "Шаг с названием запроса."),
        ('allure.attach(f"status: {status}", name="status", attachment_type=allure.attachment_type.TEXT)', "Статус текстом."),
        ('allure.attach(json.dumps(body), name="body", attachment_type=allure.attachment_type.JSON)', "Тело как JSON."),
    ],
    mistake="Повторять эти три строки в каждом тесте."),

f"{P}-labels-e1": x(
    idea="`title` — название в отчёте вместо имени функции, `description` — описание.",
    lines=[('@allure.title("Вход с правильным паролем")', "Название."), ('@allure.description("Проверяем успешный вход")', "Описание.")],
    mistake="Переименовывать функцию по-русски."),

f"{P}-labels-e2": x(
    idea="`severity` — важность теста; по ней фильтруют отчёт.",
    lines=[("@allure.severity(allure.severity_level.CRITICAL)", "Критичный."), ("@allure.severity(allure.severity_level.MINOR)", "Незначительный.")],
    mistake="Строка `\"critical\"` вместо константы."),

f"{P}-labels-e3": x(
    idea="Метки на классе применяются ко всем методам; story — у каждого свой.",
    lines=[
        ('@allure.epic("Магазин")', "Самый крупный уровень."),
        ('@allure.feature("Корзина")', "Функциональность."),
        ('@allure.story("Добавление товара")', "Сценарий конкретного теста."),
    ],
    mistake="Дублировать epic и feature на каждом методе."),

f"{P}-labels-e4": x(
    idea="Ссылки связывают тест с тест-кейсом и багом — из отчёта можно перейти.",
    lines=[('@allure.testcase("https://tms/TC-15", "TC-15")', "Тест-кейс."), ('@allure.issue("https://tracker/BUG-42", "BUG-42")', "Баг.")],
    mistake="Писать ссылки в описании — по ним нельзя фильтровать."),

f"{P}-labels-e5": x(
    idea="Уровни: blocker, critical, normal, minor, trivial.",
    lines=[("blocker", "Самый важный.")],
    mistake="Ответить critical — он второй."),

f"{P}-labels-e6": x(
    idea="Без метки severity — normal.",
    lines=[("normal", "Уровень по умолчанию.")],
    mistake="Ответить minor."),

f"{P}-labels-e7": x(
    idea="`allure.dynamic` меняет метки во время теста — удобно для параметров.",
    lines=[('@pytest.mark.parametrize("role", ["admin", "qa"])', "Два случая."), ('allure.dynamic.title(f"Доступ для роли {role}")', "Название с параметром.")],
    mistake="`@allure.title` с f-строкой — `role` там ещё неизвестна."),

f"{P}-labels-e8": x(
    idea="Полностью оформленный тест: метки сверху, шаги и вложения внутри.",
    lines=[
        ('@allure.title("Оформление заказа")', "Название."),
        ('@allure.tag("smoke")', "Тег."),
        ('with allure.step("Оплатить"):', "Шаг."),
        ('allure.attach("paid", name="status", attachment_type=allure.attachment_type.TEXT)', "Вложение в шаге."),
    ],
    mistake="Перепутать tag и feature — это разные метки."),

# ===== Модуль 2. Отчёты =====

f"{P}-report-e1": x(
    idea="`--single-file` собирает отчёт в один HTML, который открывается без сервера.",
    lines=[("allure generate allure-results --single-file", "Один файл."), ("-o allure-report --clean", "Куда и с очисткой.")],
    mistake="Отправлять папку отчёта архивом — получателю нужен веб-сервер."),

f"{P}-report-e2": x(
    idea="Тренды строятся из папки `history` прошлого отчёта.",
    lines=[("history", "Скопировать в новые результаты.")],
    mistake="Копировать весь старый отчёт."),

f"{P}-report-e3": x(
    idea="`cp -r` копирует папку целиком.",
    lines=[("cp -r allure-report/history allure-results/", "История — в новые результаты.")],
    mistake="Без `-r` — папка не скопируется."),

f"{P}-report-e4": x(
    idea="`environment.properties` — пары `ключ=значение` для блока Environment.",
    lines=[("environment.properties", "Стенд, браузер, версии.")],
    mistake="Класть файл в папку отчёта — его читают из результатов."),

f"{P}-report-e5": x(
    idea="`categories.json` — свои категории ошибок по статусу и тексту.",
    lines=[("categories.json", "Классификация падений.")],
    mistake="Ставить категории метками в тестах."),

f"{P}-report-e6": x(
    idea="Формат properties: строка `ключ=значение`; сортировка делает файл стабильным.",
    lines=[("for key in sorted(env):", "По алфавиту."), ('f.write(f"{key}={env[key]}\\n")', "Одна пара на строку.")],
    mistake="Писать JSON — Allure ждёт properties."),

f"{P}-report-e7": x(
    idea="Категория: имя, статусы и необязательный шаблон текста ошибки.",
    lines=[
        ('{"name": "Проблемы окружения", "matchedStatuses": ["broken"], "messageRegex": ".*ConnectionError.*"},', "Сломанные из-за сети."),
        ("json.dump(make_categories(), f, ensure_ascii=False, indent=2)", "Кириллица без экранирования."),
    ],
    mistake="Без `ensure_ascii=False` — названия станут `\\u041f…` (работает, но нечитаемо)."),

f"{P}-report-e8": x(
    idea="Блок Environment показывает значения как есть.",
    lines=[("Browser=firefox", "Ключ Browser.")],
    mistake="Взять Browser.Version."),

f"{P}-status-e1": x(
    idea="Упавший assert — failed.",
    lines=[("failed", "Проверка не прошла.")],
    mistake="broken — для других исключений."),

f"{P}-status-e2": x(
    idea="Любое исключение, кроме AssertionError, — broken.",
    lines=[("broken", "Тест сломался.")],
    mistake="failed — только для assert."),

f"{P}-status-e3": x(
    idea="Пропущенный тест — skipped.",
    lines=[("skipped", "Не выполнялся.")],
    mistake="passed — он не проверял ничего."),

f"{P}-status-e4": x(
    idea="Строка broken в сводке.",
    lines=[("broken    2", "Два.")],
    mistake="Сложить failed и broken."),

f"{P}-status-e5": x(
    idea="Упавший тест различаем по типу исключения; остальные статусы — как есть.",
    lines=[
        ('if outcome == "failed":', "Только для упавших."),
        ('return "failed" if exc_type == "AssertionError" else "broken"', "assert или другое."),
        ("return outcome", "passed и skipped без изменений."),
    ],
    mistake="Проверять `exc_type` для прошедших тестов."),

f"{P}-status-e6": x(
    idea="Первая категория, где совпал статус и (если задан) шаблон сообщения.",
    lines=[
        ('if result["status"] not in cat["matchedStatuses"]:\n            continue', "Статус не тот."),
        ('if pattern and not re.fullmatch(pattern, result.get("message", ""), re.S):\n            continue', "Текст не подходит; `re.S` — точка ловит и перевод строки."),
        ('return cat["name"]', "Первая подходящая."),
    ],
    mistake="`re.search` — Allure сравнивает текст целиком."),

f"{P}-status-e7": x(
    idea="Flaky — результат меняется без изменений кода.",
    lines=[("flaky", "Нестабильный тест.")],
    mistake="Считать его просто упавшим."),

f"{P}-status-e8": x(
    idea="Множество статусов: есть и успех, и падение — значит нестабилен.",
    lines=[
        ("s = set(statuses)", "Уникальные статусы."),
        ('if "passed" in s and s & {"failed", "broken"}:', "И проходил, и падал."),
        ("return sorted(result)", "По алфавиту."),
    ],
    mistake="Считать flaky тест, который падает всегда."),

f"{P}-junit-e1": x(
    idea="JUnit XML — формат, который понимают почти все CI.",
    lines=[("pytest --junitxml=report.xml", "Встроено в pytest.")],
    mistake="Ставить отдельный плагин — флаг уже есть."),

f"{P}-junit-e2": x(
    idea="HTML-отчёт pytest — плагин `pytest-html`.",
    lines=[("pip install pytest-html", "Установка.")],
    mistake="Путать с Allure — это более простой отчёт."),

f"{P}-junit-e3": x(
    idea="`--self-contained-html` встраивает стили в один файл.",
    lines=[("pytest --html=report.html", "Отчёт."), ("--self-contained-html", "Один файл без папки ресурсов.")],
    mistake="Без флага — рядом появится папка `assets`, без неё отчёт сломается."),

f"{P}-junit-e4": x(
    idea="`failures` — упавшие assert, `errors` — сломанные.",
    lines=[('failures="1"', "Один упал.")],
    mistake="Прибавить errors."),

f"{P}-junit-e5": x(
    idea="Корень может быть `testsuite` или `testsuites`; атрибуты — строки, переводим в int.",
    lines=[
        ("root = ET.fromstring(xml_text)", "Разбор XML."),
        ('suite = root if root.tag == "testsuite" else root.find("testsuite")', "Нужный узел."),
        ('return {key: int(suite.get(key, 0)) for key in ("tests", "failures", "errors", "skipped")}', "Числа."),
    ],
    mistake="Оставить строки — `\"5\"` вместо 5."),

f"{P}-junit-e6": x(
    idea="Ищем в каждом testcase узел failure, а если нет — error.",
    lines=[
        ('for case in ET.fromstring(xml_text).iter("testcase"):', "Все тест-кейсы."),
        ('problem = case.find("failure")', "Сначала failure."),
        ("if problem is None:", "`is None` — у пустого узла `bool` ложен."),
        ("result.append(f\"{case.get('classname')}::{case.get('name')}: {problem.get('message')}\")", "Строка отчёта."),
    ],
    mistake="`if not problem:` — элемент без детей считается ложным."),

f"{P}-junit-e7": x(
    idea="Собираем пары (имя, время) и сортируем по убыванию.",
    lines=[
        ('cases = [(c.get("name"), float(c.get("time", 0))) for c in ET.fromstring(xml_text).iter("testcase")]', "Время — float."),
        ("return sorted(cases, key=lambda c: -c[1])[:n]", "Самые долгие."),
    ],
    mistake="Сортировать строки времени — `\"10.0\" < \"9.0\"`."),

f"{P}-junit-e8": x(
    idea="JUnit XML — общий язык результатов тестов для CI.",
    lines=[("JUnit XML", "Формат.")],
    mistake="Думать, что CI понимают только Allure."),

f"{P}-summary-e1": x(
    idea="Заранее заводим все четыре ключа, чтобы нули тоже были в ответе.",
    lines=[
        ('counts = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0}', "Все ключи."),
        ('counts[r["status"]] = counts.get(r["status"], 0) + 1', "Подсчёт."),
        ('counts["total"] = len(results)', "Всего."),
    ],
    mistake="Пустой словарь — отсутствующих статусов не будет в ответе."),

f"{P}-summary-e2": x(
    idea="Процент считаем от выполненных — пропущенные не учитываем.",
    lines=[
        ('executed = counts["passed"] + counts["failed"] + counts["broken"]', "Без skipped."),
        ("if executed == 0:\n        return 0.0", "Деления на ноль нет."),
        ('return round(counts["passed"] * 100 / executed, 1)', "Один знак."),
    ],
    mistake="Делить на total — пропуски занизят процент."),

f"{P}-summary-e3": x(
    idea="`glob(\"*-result.json\")` выбирает только результаты тестов.",
    lines=[('return [json.loads(p.read_text(encoding="utf-8")) for p in Path(folder).glob("*-result.json")]', "Список словарей.")],
    mistake="Читать все `*.json` — попадут container-файлы."),

f"{P}-summary-e4": x(
    idea="Метки — список словарей `name`/`value`; берём первую feature.",
    lines=[
        ('if r["status"] not in ("failed", "broken"):\n            continue', "Только упавшие."),
        ('features = [l["value"] for l in r.get("labels", []) if l["name"] == "feature"]', "Все feature-метки."),
        ('key = features[0] if features else "без feature"', "Запасной ключ."),
    ],
    mistake="`r[\"labels\"][\"feature\"]` — labels — список, а не словарь."),

f"{P}-summary-e5": x(
    idea="start и stop — миллисекунды: разницу делим на 1000.",
    lines=[('return round((result["stop"] - result["start"]) / 1000, 2)', "Секунды."), ("return round(sum(duration_sec(r) for r in results), 2)", "Сумма.")],
    mistake="Забыть деление — получатся миллисекунды."),

f"{P}-summary-e6": x(
    idea="Виджеты отчёта лежат в `widgets/`; итоговые цифры — `summary.json`.",
    lines=[("widgets/summary.json", "Сводка.")],
    mistake="Искать сводку в `allure-results`."),

f"{P}-summary-e7": x(
    idea="`jq` достаёт поле из JSON по пути.",
    lines=[("jq .statistic.failed", "Путь к полю."), ("allure-report/widgets/summary.json", "Файл.")],
    mistake="grep по JSON — легко зацепить не то поле."),

f"{P}-summary-e8": x(
    idea="Правила проверяются по порядку; первое нарушение — ответ.",
    lines=[
        ('if counts["broken"]:\n        return False, f"есть broken: {counts[\'broken\']}"', "Сломанные — сразу стоп."),
        ('rate = round(counts["passed"] * 100 / executed, 1) if executed else 0.0', "Процент без skipped."),
        ('return False, f"pass rate {rate}% < {min_rate}%"', "Слишком мало прошло."),
        ('return True, "ok"', "Всё хорошо."),
    ],
    mistake="Поменять порядок проверок — при broken будет другое сообщение."),

# ===== Модуль 3. Отчёты в CI и на сервере =====

f"{P}-ci-e1": x(
    idea="`if: always()` — шаг выполнится, даже если предыдущие упали.",
    lines=[("always()", "Результаты сохранятся и при падении тестов.")],
    mistake="Без условия — при упавших тестах шаг пропустится, отчёта не будет."),

f"{P}-ci-e2": x(
    idea="`actions/upload-artifact` сохраняет файлы прогона.",
    lines=[("actions/upload-artifact@v4", "Официальное действие.")],
    mistake="Указать без версии."),

f"{P}-ci-e3": x(
    idea="В GitLab `artifacts: when: always` — сохранять при любом исходе.",
    lines=[("always", "Даже при падении.")],
    mistake="`on_success` — значение по умолчанию."),

f"{P}-ci-e4": x(
    idea="Каждый элемент списка `steps` (с `-`) — шаг.",
    lines=[("- uses: actions/checkout@v4", "1."), ("- uses: actions/upload-artifact@v4", "5-й, последний.")],
    mistake="Считать `with:` и `if:` отдельными шагами."),

f"{P}-ci-e5": x(
    idea="pytest сам возвращает 1, если есть падения, — CI это видит.",
    lines=[("ничего", "Флаги не нужны.")],
    mistake="Добавлять `|| true` — CI перестанет замечать падения."),

f"{P}-ci-e6": x(
    idea="GitHub Pages раздаёт статические сайты — отчёт Allure как раз такой.",
    lines=[("GitHub Pages", "Хостинг статики.")],
    mistake="Хранить отчёт только в артефактах — его неудобно открывать."),

f"{P}-ci-e7": x(
    idea="Собираем команды строками: выбор инструмента, флаг параллельности только при `workers > 1`.",
    lines=[
        ('install = "uv sync --locked" if use_uv else "pip install -r requirements.txt"', "Установка."),
        ('if workers > 1:\n        run += f" -n {workers}"', "Параллельно."),
        ('return [install, run + " --alluredir=allure-results"]', "Две команды."),
    ],
    mistake="Добавлять `-n 1` — лишний флаг."),

f"{P}-ci-e8": x(
    idea="`download-artifact` забирает артефакт, загруженный другим job.",
    lines=[("actions/download-artifact@v4", "Парный к upload.")],
    mistake="Ждать, что файлы сами перейдут между job — у каждого свой чистый раннер."),

f"{P}-server-e1": x(
    idea="Allure TestOps — коммерческий сервер для истории запусков и тест-кейсов.",
    lines=[("Allure TestOps", "Система управления тестированием.")],
    mistake="Путать с Allure Report — тот бесплатный и локальный."),

f"{P}-server-e2": x(
    idea="`-p хост:контейнер` пробрасывает порт.",
    lines=[("docker run -p 5050:5050", "Порт 5050."), ("frankescobar/allure-docker-service", "Образ.")],
    mistake="Без `-p` — сервер внутри контейнера недоступен снаружи."),

f"{P}-server-e3": x(
    idea="`allurectl upload` отправляет папку результатов в TestOps.",
    lines=[("upload", "Подкоманда загрузки.")],
    mistake="`send` — так называется эндпоинт docker-сервиса, а не подкоманда."),

f"{P}-server-e4": x(
    idea="Файлы читаются байтами и кодируются в base64 — так их можно передать в JSON.",
    lines=[
        ("files = sorted(p for p in Path(folder).iterdir() if p.is_file())", "Только файлы, по имени."),
        ('{"file_name": p.name, "content_base64": base64.b64encode(p.read_bytes()).decode()}', "`decode` — bytes → str."),
    ],
    mistake="`read_text` — картинки и вложения испортятся."),

f"{P}-server-e5": x(
    idea="`params=` собирает строку запроса, `json=` — тело; не 200 — ошибка.",
    lines=[
        ('params={"project_id": project},', "`?project_id=…`."),
        ("json=payload,", "JSON-тело."),
        ('raise RuntimeError(f"сервер ответил {response.status_code}")', "Понятная ошибка."),
    ],
    mistake="Без `timeout` — запрос может висеть бесконечно."),

f"{P}-server-e6": x(
    idea="`raise_for_status` бросит исключение на 4xx/5xx; ссылка лежит во вложенных полях.",
    lines=[("response.raise_for_status()", "Ошибка HTTP — исключение."), ('return response.json()["data"]["report_url"]', "Путь к ссылке.")],
    mistake="Читать JSON без проверки статуса — при ошибке получишь непонятный KeyError."),

f"{P}-server-e7": x(
    idea="Сервер хранит прогоны — видны тренды и флаки.",
    lines=[("история", "Главное преимущество.")],
    mistake="Думать, что сервер нужен для скорости."),

f"{P}-server-e8": x(
    idea="`-d @файл` отправляет содержимое файла как тело запроса.",
    lines=[("-H 'Content-Type: application/json'", "Тип тела."), ("-d @payload.json", "Тело из файла.")],
    mistake="`-d payload.json` без `@` — отправится строка с именем файла."),

f"{P}-notify-e1": x(
    idea="Заголовок зависит от наличия падений; ссылка — второй строкой.",
    lines=[
        ('if counts["failed"] or counts["broken"]:', "Есть проблемы."),
        ("head = f\"✅ Тесты прошли: {counts['passed']}/{counts['total']}\"", "Всё хорошо."),
        ('return f"{head}\\nОтчёт: {report_url}"', "Две строки."),
    ],
    mistake="Проверять только failed — сломанные тесты останутся незамеченными."),

f"{P}-notify-e2": x(
    idea="Telegram Bot API: POST на `/bot<токен>/sendMessage`, ответ содержит `ok`.",
    lines=[
        ('f"https://api.telegram.org/bot{token}/sendMessage",', "Адрес с токеном."),
        ('json={"chat_id": chat_id, "text": text},', "Тело."),
        ('return response.json().get("ok") is True', "Успех по ответу API."),
    ],
    mistake="Смотреть только код 200 — Telegram может вернуть ошибку в теле."),

f"{P}-notify-e3": x(
    idea="Slack-блоки: ссылка на отчёт и, если есть, список упавших (не больше 5).",
    lines=[
        ('blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": f"<{report_url}|Открыть отчёт>"}}]', "Ссылка в формате Slack."),
        ('lines = [f"• {name}" for name in failed_names[:5]]', "Первые пять."),
        ('lines.append(f"• …и ещё {len(failed_names) - 5}")', "Остальные — числом."),
    ],
    mistake="Выводить все имена — сообщение на сотню строк."),

f"{P}-notify-e4": x(
    idea="Токены хранят в секретах CI, а не в коде.",
    lines=[("secrets", "Зашифрованные переменные репозитория.")],
    mistake="Коммитить токен — его увидит любой с доступом к репозиторию."),

f"{P}-notify-e5": x(
    idea="Секрет подставляется выражением `${{ secrets.ИМЯ }}`.",
    lines=[("${{ secrets.TELEGRAM_TOKEN }}", "Значение секрета.")],
    mistake="`$TELEGRAM_TOKEN` — переменной окружения нет, пока её не задать в `env:`."),

f"{P}-notify-e6": x(
    idea="`.get` с запасным значением на каждом уровне — шаблон не упадёт на неполных данных.",
    lines=[
        ('stat = data.get("statistic", {})', "Нет секции — пустой словарь."),
        ('return {key: stat.get(key, 0) for key in ("passed", "failed", "broken", "skipped", "total")}', "Нет поля — 0."),
    ],
    mistake="`data[\"statistic\"]` — KeyError на пустом отчёте."),

f"{P}-notify-e7": x(
    idea="`-d` без `-H` отправляет данные как форму; переменные `$TOKEN` и `$CHAT` подставит оболочка.",
    lines=[
        ('"https://api.telegram.org/bot$TOKEN/sendMessage"', "В двойных кавычках `$TOKEN` раскроется."),
        ("-d chat_id=$CHAT", "Поле формы."),
        ('-d text="Тесты упали"', "Текст с пробелом — в кавычках."),
    ],
    mistake="Одинарные кавычки вокруг URL — `$TOKEN` не подставится."),

f"{P}-notify-e8": x(
    idea="Уведомления при каждом прогоне быстро перестают читать.",
    lines=[("при падении", "Сигнал, когда нужна реакция.")],
    mistake="Слать «всё хорошо» каждые 10 минут."),

f"{P}-practice-e1": x(
    idea="autouse-фикстура в conftest добавляет метку всем тестам сразу.",
    lines=[("@pytest.fixture(autouse=True)", "Для каждого теста."), ('allure.dynamic.tag("stage")', "Метка-тег.")],
    mistake="Писать `@allure.tag` над каждым тестом."),

f"{P}-practice-e2": x(
    idea="hookwrapper: до `yield` — до стандартной реализации, после — уже есть отчёт о тесте.",
    lines=[
        ("@pytest.hookimpl(hookwrapper=True)", "Обёртка вокруг хука."),
        ("outcome = yield", "Pytest делает свою работу."),
        ("report = outcome.get_result()", "Отчёт об этапе."),
        ('if report.when == "call" and report.failed:', "Упал сам тест."),
    ],
    mistake="Не проверить `when` — вложение приложится и за упавший setup."),

f"{P}-practice-e3": x(
    idea="`pytest_sessionfinish` — после всего прогона; папку результатов берём из опций.",
    lines=[
        ('folder = session.config.getoption("--alluredir")', "Куда пишет Allure."),
        ("if not folder:\n        return", "Запуск без Allure."),
        ('f.write("Python=3.12\\nStand=stage\\n")', "Две пары."),
    ],
    mistake="Захардкодить путь — при другом `--alluredir` файл окажется не там."),

f"{P}-practice-e4": x(
    idea="Фикстура-фабрика возвращает функцию, а та — контекстный менеджер шага.",
    lines=[
        ("def step(name):", "Функция для теста."),
        ('return allure.step(f"API: {name}")', "Шаг с префиксом."),
        ("return step", "Фикстура отдаёт функцию."),
    ],
    mistake="`return step(...)` — фикстура вернёт один шаг, а не фабрику."),

f"{P}-practice-e5": x(
    idea="`pytest_sessionfinish` вызывается один раз в конце.",
    lines=[("pytest_sessionfinish", "Хук конца прогона.")],
    mistake="`pytest_runtest_teardown` — после каждого теста."),

f"{P}-practice-e6": x(
    idea="`hookwrapper=True` — хук-обёртка с `yield`.",
    lines=[("hookwrapper=True", "Код до и после реализации.")],
    mistake="`tryfirst=True` — только меняет порядок вызова."),

f"{P}-practice-e7": x(
    idea="Этапы теста: setup, call, teardown. `call` — сам тест.",
    lines=[("call", "Выполнение тела теста.")],
    mistake="setup — это подготовка фикстур."),

f"{P}-practice-e8": x(
    idea="Итог: метка всем тестам через autouse и лог при падении через hookwrapper.",
    lines=[
        ('allure.dynamic.label("owner", "qa-team")', "Владелец теста."),
        ("outcome = yield", "Ждём результат."),
        ('if report.when == "call" and report.failed:', "Упал сам тест."),
        ('allure.attach("LOG: " + item.name, name="log", attachment_type=allure.attachment_type.TEXT)', "Лог в отчёт."),
    ],
    mistake="Прикладывать лог к каждому тесту — отчёт раздуется."),
}
