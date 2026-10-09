"""Тема «pytest» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py).
Строка `pytest.main(...)` в конце решений — только для кнопки «▶ Запустить», её не разбираем."""
from ._lib import x

P = "pyt"

EXPLAIN = {

# ===== Модуль 1. Основы pytest =====

f"{P}-first-e1": x(
    idea="Тест в pytest — функция с именем `test_…`, внутри обычный `assert`.",
    lines=[
        ("def test_add():", "Имя начинается с `test_` — pytest найдёт её сам."),
        ("assert add(2, 3) == 5", "Ложное условие — тест упал."),
    ],
    mistake="Назвать функцию `check_add` — pytest её не соберёт."),

f"{P}-first-e2": x(
    idea="Каждая проверка — отдельный тест: упадёт одна, другая всё равно покажет результат.",
    lines=[
        ("assert is_even(4)", "Истинное значение — прошёл."),
        ("assert not is_even(7)", "`not` — ожидаем ложь."),
    ],
    mistake="`assert is_even(7) == False` — работает, но `not` читается проще."),

f"{P}-first-e3": x(
    idea="`pytest` без аргументов собирает тесты во всём проекте.",
    lines=[("pytest", "Все `test_*.py`.")],
    mistake="`python tests.py` — тестов pytest это не запустит."),

f"{P}-first-e4": x(
    idea="Путь к файлу ограничивает прогон.",
    lines=[("pytest tests/test_cart.py", "Только этот файл.")],
    mistake="`pytest test_cart` — без пути и расширения файл не найдётся."),

f"{P}-first-e5": x(
    idea="Итоговая строка: сколько упало и сколько прошло. Точки — прошедшие, `F` — упавшие.",
    lines=[("1 failed, 3 passed", "Три прошло.")],
    mistake="Посчитать все 4 собранных."),

f"{P}-first-e6": x(
    idea="pytest ищет файлы `test_*.py` и `*_test.py`.",
    lines=[("test_api.py", "Начинается с `test_`."), ("ui_test.py", "Заканчивается на `_test`.")],
    mistake="Посчитать `api_tests.py` — `_tests` с `s` не подходит."),

f"{P}-first-e7": x(
    idea="Тесты группируют в класс `Test…` без `__init__`; методы получают `self`.",
    lines=[
        ("class TestCart:", "Имя с `Test`."),
        ("def test_empty_total(self):", "Метод-тест."),
        ("assert total([100, 250]) == 350", "Вторая проверка."),
    ],
    mistake="Добавить в класс `__init__` — pytest пропустит такой класс."),

f"{P}-first-e8": x(
    idea="Несколько `assert` в одном тесте: первая неудача остановит тест.",
    lines=[
        ('assert slugify("Hello World") == "hello-world"', "Обычный случай."),
        ('assert slugify("  Python  ") == "python"', "Пробелы по краям."),
        ('assert slugify("A B C") == "a-b-c"', "Несколько слов."),
    ],
    mistake="Писать проверки без `assert` — тест пройдёт всегда."),

f"{P}-assert-e1": x(
    idea="Словари сравниваются целиком; при неудаче pytest покажет, какие ключи отличаются.",
    lines=[('assert get_user(1) == {"id": 1, "name": "anna", "active": True}', "Один `assert` на весь ответ.")],
    mistake="Проверять ключи по одному — длиннее и легко пропустить лишний ключ."),

f"{P}-assert-e2": x(
    idea="`pytest.approx` сравнивает числа с допуском — для float обязательно.",
    lines=[("assert price_with_tax(0.1) == pytest.approx(0.12)", "0.12000000000000001 ≈ 0.12.")],
    mistake="`== 0.12` — упадёт из-за погрешности float."),

f"{P}-assert-e3": x(
    idea="Сообщение после запятой выводится при падении — сразу видно, в чём дело.",
    lines=[
        ('assert "smoke" in tags, f"нет smoke в {tags}"', "Есть тег."),
        ('assert "broken" not in tags, f"лишний тег broken в {tags}"', "Тега нет."),
    ],
    mistake="`assert (\"smoke\" in tags, \"…\")` в скобках — кортеж всегда истинен, тест не упадёт."),

f"{P}-assert-e4": x(
    idea="Строка `where` раскрывает значения в упавшем `assert`.",
    lines=[("where 90.5 = discount(100, 10)", "Функция вернула 90.5.")],
    mistake="Ответить 90 — это ожидаемое значение."),

f"{P}-assert-e5": x(
    idea="pytest показывает разницу словарей: одинаковые пункты пропускает, отличающиеся — перечисляет.",
    lines=[("{'role': 'qa'} != {'role': 'admin'}", "Отличается только `role`.")],
    mistake="Посчитать «2 identical items» — это совпадающие."),

f"{P}-assert-e6": x(
    idea="Хороший тест проверяет и результат, и отсутствие побочных эффектов.",
    lines=[
        ("result = sort_users(users)", "Действие."),
        ('assert [u["age"] for u in result] == [20, 30]', "Порядок по возрасту."),
        ('assert users == [{"name": "b", "age": 30}, {"name": "a", "age": 20}]', "Исходный список не тронут."),
    ],
    mistake="Не проверить вход — `users.sort()` внутри функции прошёл бы незамеченным."),

f"{P}-assert-e7": x(
    idea="В строке `assert 2 == 3` слева — фактическое значение, справа — ожидаемое.",
    lines=[("assert len(items) == 3", "Ожидали 3.")],
    mistake="Ответить 2 — это фактическая длина."),

f"{P}-assert-e8": x(
    idea="Проверяем ответ API по шагам: статус, наличие ключа, тип, каждый элемент.",
    lines=[
        ('assert resp["status"] == 200', "Статус."),
        ('assert "items" in resp["body"]', "Ключ есть."),
        ("assert isinstance(items, list)", "Тип."),
        ('assert isinstance(item.get("id"), int)', "`get` — нет ключа, будет `None`, и проверка упадёт понятно."),
    ],
    mistake="`item[\"id\"]` — при отсутствии ключа тест упадёт с `KeyError`, а не с понятным assert."),

f"{P}-raises-e1": x(
    idea="`pytest.raises` проходит, только если внутри блока возникло нужное исключение.",
    lines=[("with pytest.raises(ZeroDivisionError):", "Ждём ошибку."), ("divide(1, 0)", "Действие внутри блока.")],
    mistake="Вызвать `divide(1, 0)` до `with` — тест упадёт с ошибкой."),

f"{P}-raises-e2": x(
    idea="`match=` проверяет текст исключения регулярным выражением (поиском).",
    lines=[('with pytest.raises(ValueError, match="age"):', "Тип и кусок текста.")],
    mistake="Ожидать полного совпадения текста — достаточно подстроки."),

f"{P}-raises-e3": x(
    idea="`as exc_info` даёт доступ к исключению после блока: `exc_info.value`.",
    lines=[
        ("with pytest.raises(ApiError) as exc_info:", "Ловим и сохраняем."),
        ("assert exc_info.value.status == 404", "Проверка атрибута — после блока."),
    ],
    mistake="Писать `assert` внутри `with` после вызова — эта строка не выполнится."),

f"{P}-raises-e4": x(
    idea="«DID NOT RAISE» — блок выполнился без исключения.",
    lines=[("DID NOT RAISE", "Ошибки не было.")],
    mistake="Решить, что было другое исключение — тогда pytest показал бы его."),

f"{P}-raises-e5": x(
    idea="При несовпадении `match` pytest показывает шаблон и настоящий текст.",
    lines=[("Input: 'bad value'", "Фактический текст.")],
    mistake="Ответить age — это шаблон."),

f"{P}-raises-e6": x(
    idea="Каждое значение — свой `with`: иначе после первой ошибки остальные не проверятся.",
    lines=[
        ('for value in ["abc", "-1", "70000"]:', "Все плохие значения."),
        ("with pytest.raises(ValueError):", "Новый блок на каждое."),
        ("parse_port(value)", "Должен упасть."),
    ],
    mistake="Цикл внутри одного `with` — проверится только первое значение."),

f"{P}-raises-e7": x(
    idea="Если внутри возникло другое исключение, оно пролетает сквозь `raises` и роняет тест.",
    lines=[("TypeError: '<' not supported", "Получен `TypeError`.")],
    mistake="Ответить ValueError — это ожидаемый тип."),

f"{P}-raises-e8": x(
    idea="Позитивный и негативный сценарии — разные тесты.",
    lines=[
        ("assert withdraw(100, 30) == 70", "Без исключения."),
        ('with pytest.raises(ValueError, match="недостаточно"):', "Ошибка с нужным текстом."),
    ],
    mistake="Проверять только ошибку — сломанный обычный сценарий останется незамеченным."),

f"{P}-cli-e1": x(
    idea="`-v` — по строке на тест с результатом.",
    lines=[("pytest -v", "Подробный вывод.")],
    mistake="`-q` — наоборот, тише."),

f"{P}-cli-e2": x(
    idea="`-k` выбирает тесты по подстроке имени.",
    lines=[("pytest -k login", "Все тесты с login в имени.")],
    mistake="`-m login` — это маркеры."),

f"{P}-cli-e3": x(
    idea="`-x` — стоп на первом падении.",
    lines=[("pytest -x", "Экономит время при отладке.")],
    mistake="`-k` — фильтр по имени, а не остановка."),

f"{P}-cli-e4": x(
    idea="`--lf` (last failed) — только упавшие в прошлый раз.",
    lines=[("pytest --lf", "Быстрая проверка исправления.")],
    mistake="Гонять весь набор после каждой правки."),

f"{P}-cli-e5": x(
    idea="`файл::тест` — один тест по полному имени.",
    lines=[("pytest tests/test_cart.py::test_checkout", "Только он.")],
    mistake="`pytest test_checkout` — будет искать файл."),

f"{P}-cli-e6": x(
    idea="pytest перехватывает вывод тестов; `-s` его отключает.",
    lines=[("pytest -s", "print виден сразу.")],
    mistake="Искать print в обычном выводе — его покажут только у упавших тестов."),

f"{P}-cli-e7": x(
    idea="В `-k` работают `and`, `or`, `not`; выражение — в кавычках.",
    lines=[("pytest -k 'cart and not slow'", "cart, но без slow.")],
    mistake="Без кавычек — оболочка разобьёт выражение на аргументы."),

f"{P}-cli-e8": x(
    idea="`--tb=line` — одна строка на ошибку, `-ra` — сводка по всем непрошедшим в конце.",
    lines=[("pytest --tb=line", "Короткие ошибки."), ("-ra", "Итоговая сводка.")],
    mistake="`--tb=no` — ошибок не будет видно совсем."),

# ===== Модуль 2. Фикстуры и параметризация =====

f"{P}-fixtures-e1": x(
    idea="Фикстура — подготовка данных. Тест получает её по имени параметра.",
    lines=[
        ("@pytest.fixture", "Объявление фикстуры."),
        ('return {"name": "anna", "role": "qa"}', "Что получит тест."),
        ("def test_role(user):", "Имя параметра = имя фикстуры."),
    ],
    mistake="Вызывать `user()` внутри теста — pytest подставляет фикстуру сам."),

f"{P}-fixtures-e2": x(
    idea="Фикстура может запросить другую фикстуру параметром — pytest выстроит цепочку.",
    lines=[
        ("def users_url(base_url):", "Зависит от `base_url`."),
        ('return base_url + "/users"', "Строит адрес."),
        ("def test_url(users_url):", "Тест получает итог цепочки."),
    ],
    mistake="Импортировать или вызывать фикстуру напрямую."),

f"{P}-fixtures-e3": x(
    idea="До `yield` — подготовка, после — уборка, которая выполнится после теста.",
    lines=[
        ("yield items", "Тест получает список."),
        ("items.clear()", "Уборка."),
        ('LOG.append("cart cleared")', "След уборки."),
    ],
    mistake="`return` вместо `yield` — код уборки не выполнится."),

f"{P}-fixtures-e4": x(
    idea="Порядок: код фикстуры до `yield`, тест, код после `yield`.",
    lines=[('print("setup")', "Первым."), ('print("test")', "Тест."), ('print("teardown")', "Последним.")],
    mistake="Ждать teardown до теста."),

f"{P}-fixtures-e5": x(
    idea="Фикстура вызывается заново для каждого теста — данные не протекают.",
    lines=[
        ('return {"items": [], "status": "new"}', "Новый словарь каждый раз."),
        ('order["items"].append("чай")', "Меняем только свою копию."),
        ('assert order["items"] == []', "У второго теста — снова пусто."),
    ],
    mistake="Держать заказ в глобальной переменной — тесты станут зависеть от порядка."),

f"{P}-fixtures-e6": x(
    idea="Фикстура-фабрика возвращает функцию: тест создаёт столько объектов, сколько нужно.",
    lines=[
        ('def make(name, role="qa"):', "Внутренняя функция."),
        ("return make", "Фикстура отдаёт функцию."),
        ('boss = make_user("boss", role="admin")', "Второй объект с другими данными."),
    ],
    mistake="`return make()` — фикстура вернёт один словарь, а не фабрику."),

f"{P}-fixtures-e7": x(
    idea="Имя параметра теста должно совпадать с именем фикстуры.",
    lines=[("def test_name(usr):", "Фикстуры `usr` нет.")],
    mistake="Ответить user — эта фикстура как раз есть."),

f"{P}-fixtures-e8": x(
    idea="Код после `yield` выполняется и после упавшего теста.",
    lines=[
        ('EVENTS.append("login")', "Перед тестом."),
        ('yield "token"', "Тест."),
        ('EVENTS.append("logout")', "После теста — в любом случае."),
        ("assert False", "Падение не мешает уборке."),
    ],
    mistake="Делать уборку в самом тесте — при падении она не выполнится."),

f"{P}-scope-e1": x(
    idea="`scope=\"module\"` — одна фикстура на все тесты файла.",
    lines=[
        ('@pytest.fixture(scope="module")', "Один раз на модуль."),
        ('CALLS.append("connect")', "Выполнится один раз на три теста."),
    ],
    mistake="Без `scope` — подключение на каждый тест."),

f"{P}-scope-e2": x(
    idea="`autouse=True` — фикстура применяется ко всем тестам без параметра.",
    lines=[
        ("@pytest.fixture(autouse=True)", "Для каждого теста."),
        ("STATE.clear()", "Чистое состояние перед тестом."),
        ("assert STATE == {}", "Оба теста видят пустой словарь."),
    ],
    mistake="Забыть `autouse` — второй тест увидит данные первого."),

f"{P}-scope-e3": x(
    idea="По умолчанию `scope=\"function\"` — фикстура создаётся заново для каждого теста.",
    lines=[("@pytest.fixture", "Без scope — на каждый тест.")],
    mistake="Ответить 1 — так было бы с `scope=\"module\"`."),

f"{P}-scope-e4": x(
    idea="Области: function < class < module < package < session.",
    lines=[("session", "Один раз на весь прогон.")],
    mistake="`global` — такого значения нет."),

f"{P}-scope-e5": x(
    idea="Фикстуры из `conftest.py` видны всем тестам папки без импорта.",
    lines=[("conftest.py", "Общие фикстуры.")],
    mistake="Импортировать фикстуры из файла в каждый тест."),

f"{P}-scope-e6": x(
    idea="Фикстура в `conftest.py` доступна тестам по имени, без `import`.",
    lines=[
        ("@pytest.fixture", "Обычная фикстура."),
        ('return "https://stage.example.com"', "Значение для всех тестов."),
    ],
    mistake="Назвать файл `conftests.py` — pytest его не загрузит."),

f"{P}-scope-e7": x(
    idea="`scope=\"session\"` — авторизация один раз на весь прогон.",
    lines=[
        ('@pytest.fixture(scope="session")', "Одна на прогон."),
        ('AUTH_CALLS.append("auth")', "Выполнится один раз."),
        ('return "t-1"', "Общий токен."),
    ],
    mistake="Без scope — логин в каждом тесте, прогон станет медленным."),

f"{P}-scope-e8": x(
    idea="Хук `pytest_addoption` добавляет опцию командной строки, `request.config.getoption` её читает.",
    lines=[
        ("def pytest_addoption(parser):", "Хук — имя строго такое."),
        ('parser.addoption("--env", default="dev", help="стенд для тестов")', "Опция и значение по умолчанию."),
        ('return request.config.getoption("--env")', "Значение из командной строки."),
    ],
    mistake="Объявить хук в файле тестов — опции регистрируются только в `conftest.py`."),

f"{P}-param-e1": x(
    idea="`parametrize` превращает один тест в несколько — по случаю на набор данных.",
    lines=[
        ('@pytest.mark.parametrize("value, expected", [', "Имена параметров — строкой через запятую."),
        ('("a@b.ru", True),', "Один случай — кортеж."),
        ("def test_email(value, expected):", "Параметры теста — те же имена."),
    ],
    mistake="Цикл по случаям внутри теста — первая неудача скроет остальные."),

f"{P}-param-e2": x(
    idea="`ids` дают случаям читаемые имена в отчёте.",
    lines=[
        ('@pytest.mark.parametrize("code, ok", [(200, True), (201, True), (404, False), (500, False)],', "Данные."),
        ('ids=["ok", "created", "not_found", "server_error"])', "По имени на случай."),
    ],
    mistake="Число ids не совпадает с числом случаев — ошибка сбора."),

f"{P}-param-e3": x(
    idea="Два декоратора `parametrize` дают все комбинации: 2 × 3.",
    lines=[('@pytest.mark.parametrize("browser", ["chrome", "firefox"])', "2."), ('@pytest.mark.parametrize("lang", ["ru", "en", "de"])', "× 3.")],
    mistake="Сложить 2 + 3."),

f"{P}-param-e4": x(
    idea="Без `ids` pytest называет случай значениями через дефис в квадратных скобках.",
    lines=[("(2, 3, 5)", "Второй случай → `[2-3-5]`.")],
    mistake="`test_add[1]` — номера pytest не ставит."),

f"{P}-param-e5": x(
    idea="Отдельные декораторы — все комбинации qty × discount.",
    lines=[
        ('@pytest.mark.parametrize("qty", [1, 5])', "Количество."),
        ('@pytest.mark.parametrize("discount", [0, 10])', "Скидка — 4 теста."),
        ("assert 0 < result <= 100 * qty", "Цепочка сравнений."),
    ],
    mistake="Один декоратор с парами — получится 2 случая, а не 4."),

f"{P}-param-e6": x(
    idea="Параметр — целый словарь; `ids` строим из поля `name`.",
    lines=[
        ('@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])', "Словарь — один случай."),
        ('assert login(case["user"], case["password"]) == case["expected"]', "Данные из словаря."),
    ],
    mistake="Без ids — имена `case0`, `case1`, по ним не понять, что упало."),

f"{P}-param-e7": x(
    idea="`pytest.param(..., marks=...)` помечает один случай — например, известной ошибкой.",
    lines=[
        ('pytest.param(2.675, 2.68, marks=pytest.mark.xfail(reason="float: 2.675 хранится как 2.67499…")),', "Ожидаемо падает."),
        ("assert round_price(value) == expected", "Общая проверка."),
    ],
    mistake="Пометить xfail весь тест — хорошие случаи перестанут проверяться."),

f"{P}-param-e8": x(
    idea="`params` у фикстуры — тест запустится по разу на каждое значение `request.param`.",
    lines=[
        ('@pytest.fixture(params=["admin", "qa", "guest"])', "Три значения."),
        ("return request.param", "Текущее значение."),
        ("def test_can_view(role):", "Три теста."),
    ],
    mistake="`return params` — такой переменной нет, значение берётся из `request`."),

f"{P}-builtin-e1": x(
    idea="`tmp_path` — новая временная папка для каждого теста (объект `Path`).",
    lines=[
        ('path = tmp_path / "report.txt"', "Файл во временной папке."),
        ('save_report(path, "passed: 5")', "Действие."),
        ('assert path.read_text(encoding="utf-8") == "passed: 5"', "Содержимое."),
    ],
    mistake="Писать в реальную папку проекта — тесты оставят мусор."),

f"{P}-builtin-e2": x(
    idea="`capsys.readouterr()` возвращает перехваченный вывод: `.out` и `.err`.",
    lines=[('greet("Аня")', "Печатает."), ('assert capsys.readouterr().out == "Привет, Аня!\\n"', "`print` добавил `\\n`.")],
    mistake="Сравнивать без `\\n`."),

f"{P}-builtin-e3": x(
    idea="`monkeypatch.setenv` задаёт переменную окружения на время теста и потом откатывает.",
    lines=[('monkeypatch.setenv("BASE_URL", "https://stage.example.com")', "Только в этом тесте."), ('assert base_url() == "https://stage.example.com"', "Функция видит значение.")],
    mistake="`os.environ[...] = …` — переменная останется для остальных тестов."),

f"{P}-builtin-e4": x(
    idea="`monkeypatch.setattr` подменяет функцию в модуле на время теста — никакой «сети».",
    lines=[
        ('monkeypatch.setattr(sys.modules[__name__], "fetch_status", lambda: 503)', "Модуль, имя, подделка."),
        ('assert status_text() == "недоступен"', "Проверяем поведение при 503."),
    ],
    mistake="Переприсвоить `fetch_status = …` в тесте — создастся локальная переменная, функция не подменится."),

f"{P}-builtin-e5": x(
    idea="`tmp_path` — встроенная фикстура: уникальная папка на тест.",
    lines=[("tmp_path", "Объект `pathlib.Path`.")],
    mistake="`tmpdir` — старый вариант, возвращает другой тип."),

f"{P}-builtin-e6": x(
    idea="`capsys` перехватывает stdout и stderr.",
    lines=[("capsys", "`readouterr().out`.")],
    mistake="`caplog` — для логов модуля `logging`."),

f"{P}-builtin-e7": x(
    idea="`--fixtures` — список доступных фикстур с описаниями.",
    lines=[("pytest --fixtures", "Встроенные и свои.")],
    mistake="`pytest --help` — общий список опций."),

f"{P}-builtin-e8": x(
    idea="Один тест — удачный путь, второй — ошибка; оба на временной папке.",
    lines=[
        ('path.write_text(json.dumps({"url": "http://x"}), encoding="utf-8")', "Готовим файл."),
        ('assert load_config(path) == {"url": "http://x"}', "Читается правильно."),
        ('load_config(tmp_path / "nope.json")', "Файла нет — ошибка."),
    ],
    mistake="Использовать реальный конфиг проекта — тест зависит от окружения."),

# ===== Модуль 3. Маркеры, параллельность и настройка =====

f"{P}-marks-e1": x(
    idea="`skip` пропускает тест, в отчёте будет причина.",
    lines=[('@pytest.mark.skip(reason="фича в разработке")', "Не выполняется."), ("assert False", "Не запустится — прогон не краснеет.")],
    mistake="Закомментировать тест — о нём забудут."),

f"{P}-marks-e2": x(
    idea="`skipif(условие, reason=…)` пропускает тест, если условие истинно.",
    lines=[('@pytest.mark.skipif(sys.platform.startswith("win"), reason="только Unix")', "На Windows — пропуск.")],
    mistake="`if` внутри теста с `return` — тест «пройдёт», хотя ничего не проверил."),

f"{P}-marks-e3": x(
    idea="`xfail` — тест ожидаемо падает из-за известного бага. Когда баг починят — pytest покажет XPASS.",
    lines=[('@pytest.mark.xfail(reason="BUG-42")', "Ссылка на баг."), ("assert discount(100, 150) >= 0", "Правильное ожидание.")],
    mistake="Написать неверную проверку, чтобы тест «проходил»."),

f"{P}-marks-e4": x(
    idea="Свои маркеры группируют тесты: потом запускают только нужную группу.",
    lines=[("@pytest.mark.smoke", "Быстрые проверки."), ("@pytest.mark.slow", "Долгий тест.")],
    mistake="Не зарегистрировать маркеры — pytest выдаст предупреждение."),

f"{P}-marks-e5": x(
    idea="`-m` выбирает тесты по маркеру.",
    lines=[("pytest -m smoke", "Только smoke.")],
    mistake="`-k smoke` — по имени, а не по маркеру."),

f"{P}-marks-e6": x(
    idea="В `-m` работают `not`, `and`, `or`.",
    lines=[("pytest -m 'not slow'", "Всё, кроме slow.")],
    mistake="Без кавычек — `not` и `slow` станут разными аргументами."),

f"{P}-marks-e7": x(
    idea="`s` — пропущенный, `x` — xfail. Итог в последней строке.",
    lines=[("2 skipped", "Два пропущено.")],
    mistake="Посчитать xfailed как пропущенный."),

f"{P}-marks-e8": x(
    idea="Регистрация маркера — строка `имя: описание`.",
    lines=[("smoke: быстрые проверки", "В секции `markers`.")],
    mistake="Писать `@pytest.mark.smoke` в конфиге — там нужно только имя и описание."),

f"{P}-xdist-e1": x(
    idea="Параллельный запуск даёт плагин `pytest-xdist`.",
    lines=[("pip install pytest-xdist", "Установка.")],
    mistake="Искать флаг `-n` в чистом pytest — без плагина его нет."),

f"{P}-xdist-e2": x(
    idea="`-n N` — число процессов-воркеров.",
    lines=[("pytest -n 4", "Четыре воркера.")],
    mistake="`pytest -j 4` — такого флага нет."),

f"{P}-xdist-e3": x(
    idea="`-n auto` — по числу ядер.",
    lines=[("pytest -n auto", "Сколько ядер — столько воркеров.")],
    mistake="Ставить заведомо больше процессов, чем ядер."),

f"{P}-xdist-e4": x(
    idea="`--dist loadscope` раздаёт тесты группами по модулю/классу — общая фикстура создаётся один раз на воркер.",
    lines=[("pytest -n 4", "Параллельно."), ("--dist loadscope", "Модуль — целиком на один воркер.")],
    mistake="Обычный `-n 4` — тесты модуля разбегутся по воркерам."),

f"{P}-xdist-e5": x(
    idea="Первая строка xdist — число воркеров и тестов.",
    lines=[("4 workers [120 items]", "Четыре.")],
    mistake="Ответить 120 — это число тестов."),

f"{P}-xdist-e6": x(
    idea="Независимые тесты: каждый получает свой новый список из фикстуры.",
    lines=[
        ("return []", "Новый на каждый тест."),
        ('cart.append("чай")', "Меняем только свою корзину."),
        ("assert len(cart) == 0", "Второй тест не видит чужих данных."),
    ],
    mistake="Оставить глобальный `CART` — результат зависит от порядка и параллельности."),

f"{P}-xdist-e7": x(
    idea="Воркеры работают одновременно — порядок не гарантирован. Тесты не должны зависеть друг от друга.",
    lines=[("нет", "Порядка нет.")],
    mistake="Писать тест, который опирается на данные предыдущего."),

f"{P}-xdist-e8": x(
    idea="xdist выставляет `PYTEST_XDIST_WORKER` (`gw0`, `gw1`, …) — по нему делают уникальные данные на воркер.",
    lines=[("PYTEST_XDIST_WORKER", "Номер воркера.")],
    mistake="Использовать одну тестовую базу на все воркеры — тесты помешают друг другу."),

f"{P}-config-e1": x(
    idea="В `pyproject.toml` настройки pytest лежат в `[tool.pytest.ini_options]`.",
    lines=[("[tool.pytest.ini_options]", "Секция pytest.")],
    mistake="`[pytest]` — это заголовок для `pytest.ini`."),

f"{P}-config-e2": x(
    idea="`testpaths` — где искать тесты.",
    lines=[('testpaths = ["tests"]', "Только папка tests.")],
    mistake="`testdir` — такой настройки нет."),

f"{P}-config-e3": x(
    idea="`addopts` — флаги, которые добавляются к каждому запуску.",
    lines=[('addopts = "-v --tb=short"', "Всегда подробно и коротко.")],
    mistake="Писать флаги в каждой команде вручную."),

f"{P}-config-e4": x(
    idea="Флаги из `addopts` идут первыми, потом — из командной строки.",
    lines=[('addopts = "-v -n 2"', "Из настроек."), ("pytest -x", "Добавится `-x`.")],
    mistake="Думать, что `-x` заменяет addopts."),

f"{P}-config-e5": x(
    idea="`--collect-only` показывает собранные тесты без запуска.",
    lines=[("pytest --collect-only", "Что будет запущено.")],
    mistake="`pytest -v` — тесты выполнятся."),

f"{P}-config-e6": x(
    idea="`-o` переопределяет настройку из конфига на один запуск.",
    lines=[('pytest -o addopts=""', "Пустые addopts.")],
    mistake="Править конфиг ради одного запуска."),

f"{P}-config-e7": x(
    idea="Правило `error` в `filterwarnings` превращает предупреждения в ошибки.",
    lines=[("error", "Любое предупреждение — падение.")],
    mistake="`ignore` — наоборот, спрячет предупреждения."),

f"{P}-config-e8": x(
    idea="`minversion` — минимальная версия pytest.",
    lines=[('minversion = "8.0"', "Не ниже 8.0.")],
    mistake="Перепутать с версией Python."),

f"{P}-practice-e1": x(
    idea="AAA: подготовка, действие, проверка — пустые строки разделяют части.",
    lines=[
        ("cart = Cart()", "Arrange."),
        ("total = cart.checkout()", "Act — одно действие."),
        ("assert total == 350", "Assert результата."),
        ("assert cart.items == []", "Assert побочного эффекта."),
    ],
    mistake="Смешивать действия и проверки — непонятно, что именно сломалось."),

f"{P}-practice-e2": x(
    idea="Граничные значения: сама граница и соседнее значение с каждой стороны.",
    lines=[('@pytest.mark.parametrize("age, expected", [(17, False), (18, True), (99, True), (100, False)])', "Обе границы с обеих сторон.")],
    mistake="Проверить только 18 и 99 — ошибка `<` вместо `<=` не поймается."),

f"{P}-practice-e3": x(
    idea="Время передаётся параметром — тест одинаков в любой момент запуска.",
    lines=[
        ('@pytest.mark.parametrize("hour, expected", [(9, "Доброе утро"), (15, "Добрый день"), (22, "Добрый вечер")])', "По случаю на часть дня."),
        ("assert greeting(datetime(2024, 3, 8, hour)) == expected", "Фиксированная дата, разные часы."),
    ],
    mistake="`datetime.now()` в тесте — результат зависит от времени запуска."),

f"{P}-practice-e4": x(
    idea="Клиента передают в конструктор — в тесте подставляем подделку без сети.",
    lines=[
        ("class FakeClient:", "Подделка с тем же методом."),
        ('data = {"/users/1": {"id": 1, "name": "anna"}}', "Заранее заданный ответ."),
        ('assert UserService(FakeClient()).name(1) == "anna"', "Сервис работает с подделкой."),
    ],
    mistake="Ходить в настоящий API из юнит-теста — медленно и нестабильно."),

f"{P}-practice-e5": x(
    idea="Flaky — нестабильный тест: результат зависит от порядка, времени или окружения.",
    lines=[("flaky", "«Мигающий» тест.")],
    mistake="Просто перезапускать flaky-тесты — причину надо найти."),

f"{P}-practice-e6": x(
    idea="`--ff` (failed first) — сначала упавшие, потом остальные.",
    lines=[("pytest --ff", "Быстрая обратная связь.")],
    mistake="`--lf` — только упавшие, без остальных."),

f"{P}-practice-e7": x(
    idea="`--durations=N` — N самых медленных тестов.",
    lines=[("pytest --durations=5", "Топ-5 медленных.")],
    mistake="Искать медленные тесты на глаз."),

f"{P}-practice-e8": x(
    idea="Полный набор: хорошие данные, по случаю на каждую ошибку, неверный тип.",
    lines=[
        ('@pytest.mark.parametrize("pw", ["Secret123", "Qwerty2024x"])', "Хорошие пароли."),
        ("assert validate_password(pw) == []", "Ошибок нет."),
        ("assert error in validate_password(pw)", "Нужная ошибка в списке."),
        ("with pytest.raises(TypeError):", "Не строка — исключение."),
    ],
    mistake="Сравнивать весь список ошибок — тест сломается, когда добавят новое правило."),
}
