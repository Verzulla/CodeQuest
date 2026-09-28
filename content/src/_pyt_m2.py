"""Тема «pytest», модуль 2 «Фикстуры и параметризация» — задания. Теория — в _pyt_t2.py."""
from textwrap import dedent

from ._lib import cmd, lesson, module, pyt, t

P = "pyt"

# Для заданий про conftest.py: код ученика становится conftest.py, а тесты задания
# сами пишут файлы тестов, которые пользуются его фикстурами.
CONFTEST_RUNNER = """
import pytest, shutil, os


_RUNS = []


def run_with_conftest(test_code, *args):
    # Каждый запуск — в своей папке: иначе pytest возьмёт из sys.modules прошлые conftest и тесты.
    _RUNS.append(1)
    folder = f"ct{len(_RUNS)}"
    os.makedirs(folder, exist_ok=True)
    shutil.copy("solution.py", f"{folder}/conftest.py")
    with open(f"{folder}/test_generated_{len(_RUNS)}.py", "w", encoding="utf-8") as f:
        f.write(test_code)
    for name in [m for m in sys.modules if m == "conftest" or m.startswith("test_generated")]:
        del sys.modules[name]
    collector = _Collect()
    code = pytest.main(["-q", "-p", "no:cacheprovider", folder, *args], plugins=[collector])
    return int(code), collector.outcomes
"""



def ct(body):
    """Тесты задания про conftest.py: помощник run_with_conftest + проверки."""
    return CONFTEST_RUNNER + dedent(body)


m2 = module(f"{P}-m2", "Фикстуры и параметризация", "🧩", "Фикстуры и yield, области видимости и conftest.py, parametrize, встроенные фикстуры",

lesson(f"{P}-fixtures", "Фикстуры",
    pyt(f"{P}-fixtures-e1", t("""
        Создай фикстуру `user`, которая возвращает словарь `{"name": "anna", "role": "qa"}`, и тест `test_role`, который **получает её параметром** и проверяет роль.
        """),
        """
        import pytest
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_role") == "passed", res
            src = open("solution.py", encoding="utf-8").read()
            import re
            assert "@pytest.fixture" in src and re.search(r"def test_role\\(\\s*user\\s*\\)", src), "Нужна фикстура user и тест test_role(user)"
        """,
        """
        import pytest


        @pytest.fixture
        def user():
            return {"name": "anna", "role": "qa"}


        def test_role(user):
            assert user["role"] == "qa"
        """),
    pyt(f"{P}-fixtures-e2", t("""
        Фикстура может зависеть от другой фикстуры. Создай фикстуру `base_url` (возвращает `"https://api.test"`) и фикстуру `users_url(base_url)` — возвращает `base_url + "/users"`. Тест `test_url(users_url)` проверяет результат.
        """),
        """
        import pytest
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_url") == "passed", res
            src = open("solution.py", encoding="utf-8").read().replace(" ", "")
            assert "defusers_url(base_url)" in src, "users_url должна получать base_url параметром"
        """,
        """
        import pytest


        @pytest.fixture
        def base_url():
            return "https://api.test"


        @pytest.fixture
        def users_url(base_url):
            return base_url + "/users"


        def test_url(users_url):
            assert users_url == "https://api.test/users"
        """),
    pyt(f"{P}-fixtures-e3", t("""
        Фикстура с уборкой: создай фикстуру `cart`, которая создаёт пустой список, отдаёт его через `yield`, а **после** теста очищает (`cart.clear()`) и добавляет в глобальный список `LOG` строку `"cart cleared"`. Тест `test_add(cart)` добавляет товар и проверяет длину корзины.
        """),
        """
        import pytest

        LOG = []
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_add") == "passed", res
            assert sys.modules["solution"].LOG == ["cart cleared"], f"Уборка после теста не выполнена: {sys.modules['solution'].LOG}"
        """,
        """
        import pytest

        LOG = []


        @pytest.fixture
        def cart():
            items = []
            yield items
            items.clear()
            LOG.append("cart cleared")


        def test_add(cart):
            cart.append("чай")
            assert len(cart) == 1
        """, hint="Код после yield выполняется после теста — даже если тест упал."),
    cmd(f"{P}-fixtures-e4", "В каком порядке выведутся строки? Введи их через пробел.",
        ["setup test teardown"],
        context="""
        @pytest.fixture
        def db():
            print("setup")
            yield "conn"
            print("teardown")

        def test_query(db):
            print("test")

        $ pytest -s -q
        """),
    pyt(f"{P}-fixtures-e5", t("""
        Каждый тест должен получать **свежие** данные. Создай фикстуру `order`, которая возвращает новый словарь `{"items": [], "status": "new"}`. Напиши **два** теста: `test_add_item(order)` добавляет товар в `items` и проверяет длину `1`, `test_empty(order)` проверяет, что `items` пуст.
        """),
        """
        import pytest
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"test_add_item": "passed", "test_empty": "passed"}, res
        """,
        """
        import pytest


        @pytest.fixture
        def order():
            return {"items": [], "status": "new"}


        def test_add_item(order):
            order["items"].append("чай")
            assert len(order["items"]) == 1


        def test_empty(order):
            assert order["items"] == []
        """),
    pyt(f"{P}-fixtures-e6", t("""
        Фикстура-**фабрика**: создай фикстуру `make_user`, которая возвращает **функцию** `make(name, role="qa")`, создающую словарь `{"name": ..., "role": ...}`. Тест `test_two_users(make_user)` создаёт двух разных пользователей и проверяет их роли (`"qa"` и `"admin"`).
        """),
        """
        import pytest
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_two_users") == "passed", res
        """,
        """
        import pytest


        @pytest.fixture
        def make_user():
            def make(name, role="qa"):
                return {"name": name, "role": role}
            return make


        def test_two_users(make_user):
            anna = make_user("anna")
            boss = make_user("boss", role="admin")
            assert anna["role"] == "qa"
            assert boss["role"] == "admin"
        """),
    cmd(f"{P}-fixtures-e7", "Какая ошибка будет у теста? Введи слово из вывода pytest, которое её описывает (`fixture ... not found`): введи имя ненайденной фикстуры.",
        ["usr"],
        context="""
        @pytest.fixture
        def user():
            return {"name": "anna"}

        def test_name(usr):
            assert usr["name"] == "anna"
        """, hint="pytest ищет фикстуру по имени параметра."),
    pyt(f"{P}-fixtures-e8", t("""
        Фикстура `api` должна «логиниться» перед тестом и «разлогиниваться» после, **даже если тест упал**. Реализуй её через `yield`: до — `EVENTS.append("login")`, после — `EVENTS.append("logout")`, отдаёт строку `"token"`. Напиши тесты `test_ok(api)` (проверяет, что токен равен `"token"`) и `test_fails(api)` — намеренно падающий (`assert False`).
        """),
        """
        import pytest

        EVENTS = []
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"test_ok": "passed", "test_fails": "failed"}, res
            events = sys.modules["solution"].EVENTS
            assert events == ["login", "logout", "login", "logout"], f"logout должен быть и после упавшего теста: {events}"
        """,
        """
        import pytest

        EVENTS = []


        @pytest.fixture
        def api():
            EVENTS.append("login")
            yield "token"
            EVENTS.append("logout")


        def test_ok(api):
            assert api == "token"


        def test_fails(api):
            assert False
        """, xp=25),
),

lesson(f"{P}-scope", "Область видимости, autouse и conftest.py",
    pyt(f"{P}-scope-e1", t("""
        Подключение к базе дорогое: создавай его **один раз на модуль**. Создай фикстуру `db` со `scope="module"`, которая при каждом создании добавляет `"connect"` в `CALLS` и возвращает строку `"db"`. Напиши три теста `test_a`, `test_b`, `test_c`, использующие `db`.
        """),
        """
        import pytest

        CALLS = []
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"test_a": "passed", "test_b": "passed", "test_c": "passed"}, res
            calls = sys.modules["solution"].CALLS
            assert calls == ["connect"], f"Фикстура должна создаваться один раз, а создавалась {len(calls)}"
        """,
        """
        import pytest

        CALLS = []


        @pytest.fixture(scope="module")
        def db():
            CALLS.append("connect")
            return "db"


        def test_a(db):
            assert db == "db"


        def test_b(db):
            assert db == "db"


        def test_c(db):
            assert db == "db"
        """),
    pyt(f"{P}-scope-e2", t("""
        Фикстура с `autouse=True` применяется ко **всем** тестам без явного параметра. Создай такую фикстуру `reset_state`, которая перед каждым тестом очищает глобальный словарь `STATE` (`STATE.clear()`). Тесты `test_first` и `test_second` (без параметров!) должны оба проверять, что `STATE` пуст, и затем записывать в него ключ.
        """),
        """
        import pytest

        STATE = {}
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"test_first": "passed", "test_second": "passed"}, res
            src = open("solution.py", encoding="utf-8").read()
            assert "autouse=True" in src.replace(" ", ""), "Нужна фикстура с autouse=True"
            assert "def test_first()" in src and "def test_second()" in src, "Тесты без параметров"
        """,
        """
        import pytest

        STATE = {}


        @pytest.fixture(autouse=True)
        def reset_state():
            STATE.clear()


        def test_first():
            assert STATE == {}
            STATE["a"] = 1


        def test_second():
            assert STATE == {}
            STATE["b"] = 2
        """),
    cmd(f"{P}-scope-e3", "Сколько раз выполнится код фикстуры за прогон, если в модуле 5 тестов её используют? Введи число.",
        ["5"],
        context="""
        @pytest.fixture
        def browser():
            return start_browser()
        """, hint="scope по умолчанию — function."),
    cmd(f"{P}-scope-e4", "Какое значение `scope` сделает фикстуру общей для **всего прогона**? Введи строку без кавычек.",
        ["session"]),
    cmd(f"{P}-scope-e5", "Как называется файл, фикстуры из которого автоматически доступны всем тестам в его папке и вложенных? Введи имя.",
        ["conftest.py"]),
    pyt(f"{P}-scope-e6", t("""
        Твой код станет файлом `conftest.py`. Опиши в нём фикстуру `base_url`, которая возвращает `"https://stage.example.com"`. Проверка создаст рядом файл тестов, который использует эту фикстуру **без импорта**.
        """),
        """
        import pytest
        """,
        ct("""
        def test_conftest():
            code, res = run_with_conftest(
                "def test_url(base_url):\\n    assert base_url == 'https://stage.example.com'\\n")
            assert res == {"test_url": "passed"}, res
        """),
        """
        import pytest


        @pytest.fixture
        def base_url():
            return "https://stage.example.com"
        """),
    pyt(f"{P}-scope-e7", t("""
        Твой код станет `conftest.py`. Опиши фикстуру `session_token` со `scope="session"`, которая при каждом создании добавляет `"auth"` в глобальный список `AUTH_CALLS` и возвращает `"t-1"`. Проверка создаст **несколько** тестов, использующих фикстуру, и убедится, что авторизация была один раз.
        """),
        """
        import pytest

        AUTH_CALLS = []
        """,
        ct("""
        def test_conftest():
            tests = (
                "import conftest\\n"
                "def test_a(session_token):\\n    assert session_token == 't-1'\\n"
                "def test_b(session_token):\\n    assert session_token == 't-1'\\n"
                "def test_calls(session_token):\\n    assert conftest.AUTH_CALLS == ['auth'], conftest.AUTH_CALLS\\n"
            )
            code, res = run_with_conftest(tests)
            assert res == {"test_a": "passed", "test_b": "passed", "test_calls": "passed"}, res
        """),
        """
        import pytest

        AUTH_CALLS = []


        @pytest.fixture(scope="session")
        def session_token():
            AUTH_CALLS.append("auth")
            return "t-1"
        """),
    pyt(f"{P}-scope-e8", t("""
        Твой код станет `conftest.py`. Добавь в pytest **свою опцию командной строки** `--env` (по умолчанию `"dev"`) через хук `pytest_addoption(parser)` и фикстуру `env(request)`, которая возвращает её значение (`request.config.getoption("--env")`). Проверка запустит тесты с `--env stage`.
        """),
        """
        import pytest
        """,
        ct("""
        def test_conftest():
            code, res = run_with_conftest("def test_env(env):\\n    assert env == 'stage'\\n", "--env", "stage")
            assert res == {"test_env": "passed"}, res
            code, res = run_with_conftest("def test_env(env):\\n    assert env == 'dev'\\n")
            assert res == {"test_env": "passed"}, "Значение по умолчанию — dev"
        """),
        """
        import pytest


        def pytest_addoption(parser):
            parser.addoption("--env", default="dev", help="стенд для тестов")


        @pytest.fixture
        def env(request):
            return request.config.getoption("--env")
        """, hint="parser.addoption('--env', default='dev')", xp=25),
),

lesson(f"{P}-param", "Параметризация",
    pyt(f"{P}-param-e1", t("""
        Проверь функцию `is_valid_email` на наборе данных с помощью `@pytest.mark.parametrize`. Тест `test_email(value, expected)` с случаями:

        - `"a@b.ru"` → `True`;
        - `"no-at.ru"` → `False`;
        - `"@b.ru"` → `False`;
        - `"a@"` → `False`.
        """),
        """
        import pytest


        def is_valid_email(value):
            name, sep, domain = value.partition("@")
            return bool(name and sep and "." in domain)
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert len(res) == 4 and all(r == "passed" for r in res.values()), f"Нужно 4 проходящих случая: {res}"
            assert all(name.startswith("test_email[") for name in res), res

        def test_catches_bugs():
            for bug in (lambda v: "@" in v, lambda v: True, lambda v: "." in v):
                code, res = run_pytest(patch={"is_valid_email": bug})
                assert code == 1, "Параметризованный тест пропустил ошибку"
        """,
        """
        import pytest


        def is_valid_email(value):
            name, sep, domain = value.partition("@")
            return bool(name and sep and "." in domain)


        @pytest.mark.parametrize("value, expected", [
            ("a@b.ru", True),
            ("no-at.ru", False),
            ("@b.ru", False),
            ("a@", False),
        ])
        def test_email(value, expected):
            assert is_valid_email(value) == expected
        """),
    pyt(f"{P}-param-e2", t("""
        Дай случаям понятные имена через `ids`. Параметризуй тест `test_status(code, ok)` для функции `is_success(code)`: `200 → True`, `201 → True`, `404 → False`, `500 → False` с именами `ok`, `created`, `not_found`, `server_error`.
        """),
        """
        import pytest


        def is_success(code):
            return 200 <= code < 300
        """,
        """
        def test_written():
            code, res = run_pytest()
            expected = {f"test_status[{i}]": "passed" for i in ["ok", "created", "not_found", "server_error"]}
            assert res == expected, res
        """,
        """
        import pytest


        def is_success(code):
            return 200 <= code < 300


        @pytest.mark.parametrize("code, ok", [(200, True), (201, True), (404, False), (500, False)],
                                 ids=["ok", "created", "not_found", "server_error"])
        def test_status(code, ok):
            assert is_success(code) == ok
        """),
    cmd(f"{P}-param-e3", "Сколько тестов соберёт pytest? Введи число.",
        ["6"],
        context="""
        @pytest.mark.parametrize("browser", ["chrome", "firefox"])
        @pytest.mark.parametrize("lang", ["ru", "en", "de"])
        def test_home(browser, lang):
            ...
        """, hint="Два декоратора — все комбинации."),
    cmd(f"{P}-param-e4", "Как будет называться тест для второго случая? Введи имя целиком.",
        ["test_add[2-3-5]"],
        context="""
        @pytest.mark.parametrize("a, b, total", [(1, 1, 2), (2, 3, 5)])
        def test_add(a, b, total):
            assert a + b == total
        """),
    pyt(f"{P}-param-e5", t("""
        Параметризуй **две** переменные отдельными декораторами, чтобы получились все комбинации: тест `test_price(qty, discount)` для `qty` из `[1, 5]` и `discount` из `[0, 10]` проверяет, что `total(100, qty, discount)` больше `0` и не больше `100 * qty`.
        """),
        """
        import pytest


        def total(price, qty, discount):
            return price * qty * (100 - discount) / 100
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert len(res) == 4 and all(v == "passed" for v in res.values()), res
            assert open("solution.py", encoding="utf-8").read().count("@pytest.mark.parametrize") >= 2, "Нужно два декоратора parametrize"

        def test_catches_bug():
            code, res = run_pytest(patch={"total": lambda p, q, d: p * q * (100 + d) / 100})
            assert code == 1, "Тест должен ловить неверную скидку"
        """,
        """
        import pytest


        def total(price, qty, discount):
            return price * qty * (100 - discount) / 100


        @pytest.mark.parametrize("qty", [1, 5])
        @pytest.mark.parametrize("discount", [0, 10])
        def test_price(qty, discount):
            result = total(100, qty, discount)
            assert 0 < result <= 100 * qty
        """),
    pyt(f"{P}-param-e6", t("""
        Данные часто лежат отдельно от теста. Есть список `CASES` из словарей. Параметризуй тест `test_login(case)` так, чтобы каждый словарь был отдельным случаем, а `ids` брались из поля `"name"`. Тест проверяет, что `login(case["user"], case["password"]) == case["expected"]`.
        """),
        """
        import pytest

        CASES = [
            {"name": "valid", "user": "anna", "password": "secret", "expected": 200},
            {"name": "wrong_password", "user": "anna", "password": "x", "expected": 401},
            {"name": "empty_user", "user": "", "password": "secret", "expected": 400},
        ]


        def login(user, password):
            if not user:
                return 400
            return 200 if password == "secret" else 401
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"test_login[valid]": "passed", "test_login[wrong_password]": "passed", "test_login[empty_user]": "passed"}, res

        def test_catches_bug():
            code, res = run_pytest(patch={"login": lambda u, p: 200})
            assert code == 1, "Тест должен ловить сломанный login"
        """,
        """
        import pytest

        CASES = [
            {"name": "valid", "user": "anna", "password": "secret", "expected": 200},
            {"name": "wrong_password", "user": "anna", "password": "x", "expected": 401},
            {"name": "empty_user", "user": "", "password": "secret", "expected": 400},
        ]


        def login(user, password):
            if not user:
                return 400
            return 200 if password == "secret" else 401


        @pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
        def test_login(case):
            assert login(case["user"], case["password"]) == case["expected"]
        """),
    pyt(f"{P}-param-e7", t("""
        Отдельный случай можно пометить как ожидаемо падающий: `pytest.param(..., marks=pytest.mark.xfail)`. Параметризуй `test_round(value, expected)` для `round_price`: `(1.234, 1.23)`, `(2.5, 2.5)`, а случай `(2.675, 2.68)` пометь `xfail` (из-за двоичного представления float он даёт `2.67`).
        """),
        """
        import pytest


        def round_price(value):
            return round(value, 2)
        """,
        """
        def test_written():
            code, res = run_pytest()
            values = sorted(res.values())
            assert values == ["passed", "passed", "skipped"], f"Нужно 2 passed и 1 xfail: {res}"
            assert "pytest.param" in open("solution.py", encoding="utf-8").read(), "Используй pytest.param"
        """,
        """
        import pytest


        def round_price(value):
            return round(value, 2)


        @pytest.mark.parametrize("value, expected", [
            (1.234, 1.23),
            (2.5, 2.5),
            pytest.param(2.675, 2.68, marks=pytest.mark.xfail(reason="float: 2.675 хранится как 2.67499…")),
        ])
        def test_round(value, expected):
            assert round_price(value) == expected
        """, hint="xfail в отчёте засчитывается как «ожидаемо упал», не как провал."),
    pyt(f"{P}-param-e8", t("""
        Параметризовать можно и фикстуру: `@pytest.fixture(params=[...])` + `request.param`. Создай фикстуру `role` с параметрами `"admin"`, `"qa"`, `"guest"` и тест `test_can_view(role)`, проверяющий, что `can_view(role)` истинно для всех ролей. Получится 3 теста.
        """),
        """
        import pytest


        def can_view(role):
            return role in ("admin", "qa", "guest")
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"test_can_view[admin]": "passed", "test_can_view[qa]": "passed", "test_can_view[guest]": "passed"}, res

        def test_catches_bug():
            code, res = run_pytest(patch={"can_view": lambda r: r != "guest"})
            assert res.get("test_can_view[guest]") == "failed", res
        """,
        """
        import pytest


        def can_view(role):
            return role in ("admin", "qa", "guest")


        @pytest.fixture(params=["admin", "qa", "guest"])
        def role(request):
            return request.param


        def test_can_view(role):
            assert can_view(role)
        """, xp=25),
),

lesson(f"{P}-builtin", "Встроенные фикстуры: tmp_path, monkeypatch, capsys",
    pyt(f"{P}-builtin-e1", t("""
        Функция `save_report(path, text)` пишет отчёт в файл. Напиши тест `test_save(tmp_path)`: сохрани отчёт в `tmp_path / "report.txt"` и проверь содержимое файла.
        """),
        """
        import pytest


        def save_report(path, text):
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_save") == "passed", res
            assert "tmp_path" in open("solution.py", encoding="utf-8").read(), "Используй tmp_path"

        def test_catches_bug():
            def bad(path, text):
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text.upper())
            code, res = run_pytest(patch={"save_report": bad})
            assert code == 1, "Тест должен проверять содержимое файла"
        """,
        """
        import pytest


        def save_report(path, text):
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)


        def test_save(tmp_path):
            path = tmp_path / "report.txt"
            save_report(path, "passed: 5")
            assert path.read_text(encoding="utf-8") == "passed: 5"
        """),
    pyt(f"{P}-builtin-e2", t("""
        Функция `greet(name)` печатает приветствие. Напиши тест `test_greet(capsys)`, который перехватывает вывод и проверяет, что напечатано `"Привет, Аня!\\n"`.
        """),
        """
        import pytest


        def greet(name):
            print(f"Привет, {name}!")
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_greet") == "passed", res
            assert "readouterr" in open("solution.py", encoding="utf-8").read(), "Используй capsys.readouterr()"

        def test_catches_bug():
            code, res = run_pytest(patch={"greet": lambda n: print(f"Hello, {n}")})
            assert code == 1, "Тест должен проверять напечатанный текст"
        """,
        """
        import pytest


        def greet(name):
            print(f"Привет, {name}!")


        def test_greet(capsys):
            greet("Аня")
            assert capsys.readouterr().out == "Привет, Аня!\\n"
        """),
    pyt(f"{P}-builtin-e3", t("""
        Функция `base_url()` читает адрес стенда из переменной окружения `BASE_URL` (по умолчанию `http://localhost`). Напиши тест `test_env(monkeypatch)`: установи переменную через `monkeypatch.setenv` и проверь результат. Переменная не должна «протечь» в другие тесты — monkeypatch сам её уберёт.
        """),
        """
        import os
        import pytest


        def base_url():
            return os.environ.get("BASE_URL", "http://localhost")
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_env") == "passed", res
            assert "setenv" in open("solution.py", encoding="utf-8").read(), "Используй monkeypatch.setenv"
            assert "BASE_URL" not in os.environ, "Переменная протекла наружу"
        """,
        """
        import os
        import pytest


        def base_url():
            return os.environ.get("BASE_URL", "http://localhost")


        def test_env(monkeypatch):
            monkeypatch.setenv("BASE_URL", "https://stage.example.com")
            assert base_url() == "https://stage.example.com"
        """),
    pyt(f"{P}-builtin-e4", t("""
        Функция `status_text()` вызывает медленный `fetch_status()` (в тесте — «сеть»). Подмени `fetch_status` через `monkeypatch.setattr` на функцию, возвращающую `503`, и проверь, что `status_text()` вернёт `"недоступен"`. Тест — `test_down(monkeypatch)`.
        """),
        """
        import sys
        import pytest


        def fetch_status():
            raise RuntimeError("нет сети в тестах!")


        def status_text():
            return "работает" if fetch_status() == 200 else "недоступен"
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_down") == "passed", res
            assert "setattr" in open("solution.py", encoding="utf-8").read(), "Используй monkeypatch.setattr"
        """,
        """
        import sys
        import pytest


        def fetch_status():
            raise RuntimeError("нет сети в тестах!")


        def status_text():
            return "работает" if fetch_status() == 200 else "недоступен"


        def test_down(monkeypatch):
            monkeypatch.setattr(sys.modules[__name__], "fetch_status", lambda: 503)
            assert status_text() == "недоступен"
        """, hint="monkeypatch.setattr(sys.modules[__name__], 'fetch_status', ...) — подменить функцию в текущем модуле."),
    cmd(f"{P}-builtin-e5", "Какой фикстурой получить временную папку, уникальную для каждого теста?",
        ["tmp_path"]),
    cmd(f"{P}-builtin-e6", "Какой фикстурой проверить, что функция напечатала текст в stdout?",
        ["capsys"]),
    cmd(f"{P}-builtin-e7", "Покажи список всех доступных фикстур (встроенных и твоих) командой pytest.",
        ["pytest --fixtures", "python -m pytest --fixtures"]),
    pyt(f"{P}-builtin-e8", t("""
        Функция `load_config(path)` читает JSON-конфиг. Напиши **два** теста:

        - `test_load(tmp_path)` — запиши файл `config.json` с `{"url": "http://x"}` и проверь результат;
        - `test_missing(tmp_path)` — для несуществующего файла функция выбрасывает `FileNotFoundError`.
        """),
        """
        import json
        import pytest


        def load_config(path):
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"test_load": "passed", "test_missing": "passed"}, res

        def test_catches_bugs():
            def swallow(path):
                try:
                    with open(path, encoding="utf-8") as f:
                        return json.load(f)
                except FileNotFoundError:
                    return {}
            code, res = run_pytest(patch={"load_config": swallow})
            assert res.get("test_missing") == "failed", "test_missing должен ловить проглоченную ошибку"
            code, res = run_pytest(patch={"load_config": lambda p: {}})
            assert res.get("test_load") == "failed", "test_load должен проверять содержимое"
        """,
        """
        import json
        import pytest


        def load_config(path):
            with open(path, encoding="utf-8") as f:
                return json.load(f)


        def test_load(tmp_path):
            path = tmp_path / "config.json"
            path.write_text(json.dumps({"url": "http://x"}), encoding="utf-8")
            assert load_config(path) == {"url": "http://x"}


        def test_missing(tmp_path):
            with pytest.raises(FileNotFoundError):
                load_config(tmp_path / "nope.json")
        """, xp=25),
),
)
