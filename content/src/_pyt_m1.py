"""Тема «pytest», модуль 1 «Основы» — задания. Теория — в _pyt_t1.py.

В заданиях pyt(...) ученик пишет настоящие pytest-тесты: проверка запускает pytest на его
файле и смотрит исходы, в том числе на «сломанных» версиях функций (patch=)."""
from ._lib import cmd, lesson, module, pyt, t

P = "pyt"

m1 = module(f"{P}-m1", "Основы pytest", "🧪", "Первые тесты, assert и approx, pytest.raises, запуск из командной строки",

lesson(f"{P}-first", "Первый тест",
    pyt(f"{P}-first-e1", t("""
        Напиши тест `test_add`, который проверяет функцию `add`: `add(2, 3)` равно `5`.

        Нажми «▶ Запустить», чтобы увидеть вывод pytest, и «Проверить», чтобы сдать задание.
        """),
        """
        import pytest


        def add(a, b):
            return a + b


        # напиши тест ниже
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_add") == "passed", f"Нужен проходящий тест test_add, сейчас: {res}"

        def test_catches_bug():
            code, res = run_pytest(patch={"add": lambda a, b: a - b})
            assert res.get("test_add") == "failed", "Тест должен падать, если add считает неправильно"
        """,
        """
        import pytest


        def add(a, b):
            return a + b


        def test_add():
            assert add(2, 3) == 5
        """),
    pyt(f"{P}-first-e2", t("""
        Напиши **два** теста для `is_even(n)`: `test_even` (4 — чётное) и `test_odd` (7 — нечётное).
        """),
        """
        import pytest


        def is_even(n):
            return n % 2 == 0
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"test_even": "passed", "test_odd": "passed"}, f"Нужны два проходящих теста: {res}"

        def test_catches_bugs():
            for bug in (lambda n: True, lambda n: False):
                code, res = run_pytest(patch={"is_even": bug})
                assert code == 1, f"Тесты не заметили сломанную is_even: {res}"
        """,
        """
        import pytest


        def is_even(n):
            return n % 2 == 0


        def test_even():
            assert is_even(4)


        def test_odd():
            assert not is_even(7)
        """),
    cmd(f"{P}-first-e3", "Запусти все тесты проекта.",
        ["pytest", "python -m pytest", "uv run pytest"]),
    cmd(f"{P}-first-e4", "Запусти тесты только из файла `tests/test_cart.py`.",
        ["pytest tests/test_cart.py", "python -m pytest tests/test_cart.py", "uv run pytest tests/test_cart.py"]),
    cmd(f"{P}-first-e5", "Сколько тестов **прошло**? Введи число.",
        ["3"],
        context="""
        $ pytest
        ============================= test session starts ==============================
        collected 4 items

        tests/test_cart.py ..F.                                                  [100%]

        =================================== FAILURES ===================================
        ...
        ========================= 1 failed, 3 passed in 0.12s ==========================
        """, hint="Точка — прошёл, F — упал."),
    cmd(f"{P}-first-e6", "Какие из этих файлов pytest **найдёт** автоматически? Введи имена через пробел в порядке списка.",
        ["test_api.py ui_test.py"],
        context="""
        tests/
          test_api.py
          helpers.py
          ui_test.py
          api_tests.py
        """, hint="По умолчанию: test_*.py или *_test.py."),
    pyt(f"{P}-first-e7", t("""
        Сгруппируй тесты в класс: создай класс `TestCart` с методами `test_empty_total` (сумма пустой корзины — 0) и `test_total` (сумма `[100, 250]` — 350) для функции `total(prices)`.
        """),
        """
        import pytest


        def total(prices):
            return sum(prices)
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"TestCart::test_empty_total": "passed", "TestCart::test_total": "passed"}, res

        def test_catches_bug():
            code, res = run_pytest(patch={"total": lambda prices: len(prices)})
            assert code == 1, "Тесты должны поймать неправильный total"
        """,
        """
        import pytest


        def total(prices):
            return sum(prices)


        class TestCart:
            def test_empty_total(self):
                assert total([]) == 0

            def test_total(self):
                assert total([100, 250]) == 350
        """, hint="Класс с тестами называется Test…, методы — test_…, у методов параметр self; __init__ не нужен."),
    pyt(f"{P}-first-e8", t("""
        Функция `slugify(title)` превращает заголовок в часть URL. Напиши тест `test_slugify`, который проверит **три** случая: `"Hello World"` → `"hello-world"`, `"  Python  "` → `"python"`, `"A B C"` → `"a-b-c"`.
        """),
        """
        import pytest


        def slugify(title):
            return "-".join(title.lower().split())
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_slugify") == "passed", res

        def test_catches_bugs():
            bugs = [
                lambda s: s.lower().replace(" ", "-"),
                lambda s: "-".join(s.split()),
                lambda s: "_".join(s.lower().split()),
            ]
            for bug in bugs:
                code, res = run_pytest(patch={"slugify": bug})
                assert code == 1, "Тест пропустил ошибку — проверь все три случая"
        """,
        """
        import pytest


        def slugify(title):
            return "-".join(title.lower().split())


        def test_slugify():
            assert slugify("Hello World") == "hello-world"
            assert slugify("  Python  ") == "python"
            assert slugify("A B C") == "a-b-c"
        """, xp=25),
),

lesson(f"{P}-assert", "assert и сравнения",
    pyt(f"{P}-assert-e1", t("""
        Напиши тест `test_user`, проверяющий, что `get_user(1)` возвращает словарь, **равный** `{"id": 1, "name": "anna", "active": True}`. Сравнивай словарь целиком одним `assert`.
        """),
        """
        import pytest


        def get_user(user_id):
            return {"id": user_id, "name": "anna", "active": True}
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_user") == "passed", res

        def test_catches_bug():
            code, res = run_pytest(patch={"get_user": lambda i: {"id": i, "name": "anna", "active": False}})
            assert code == 1, "Тест должен замечать любое отличие в словаре"
        """,
        """
        import pytest


        def get_user(user_id):
            return {"id": user_id, "name": "anna", "active": True}


        def test_user():
            assert get_user(1) == {"id": 1, "name": "anna", "active": True}
        """),
    pyt(f"{P}-assert-e2", t("""
        `0.1 + 0.2` не равно `0.3` точно. Напиши тест `test_price`, проверяющий, что `price_with_tax(0.1)` примерно равно `0.12` с помощью `pytest.approx`.
        """),
        """
        import pytest


        def price_with_tax(price):
            return price * 1.2
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_price") == "passed", res
            assert "approx" in open("solution.py", encoding="utf-8").read(), "Используй pytest.approx"

        def test_catches_bug():
            code, res = run_pytest(patch={"price_with_tax": lambda p: p * 1.18})
            assert code == 1, "Неверный налог должен ронять тест"
        """,
        """
        import pytest


        def price_with_tax(price):
            return price * 1.2


        def test_price():
            assert price_with_tax(0.1) == pytest.approx(0.12)
        """),
    pyt(f"{P}-assert-e3", t("""
        Напиши тест `test_tags`, который проверяет, что в списке `get_tags()` есть тег `"smoke"` и **нет** тега `"broken"`. Добавь к каждому `assert` понятное сообщение после запятой.
        """),
        """
        import pytest


        def get_tags():
            return ["api", "smoke", "regression"]
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_tags") == "passed", res

        def test_catches_bugs():
            for bug in (lambda: ["api"], lambda: ["smoke", "broken"]):
                code, res = run_pytest(patch={"get_tags": bug})
                assert code == 1, f"Тест должен падать для {bug()}"
        """,
        """
        import pytest


        def get_tags():
            return ["api", "smoke", "regression"]


        def test_tags():
            tags = get_tags()
            assert "smoke" in tags, f"нет smoke в {tags}"
            assert "broken" not in tags, f"лишний тег broken в {tags}"
        """),
    cmd(f"{P}-assert-e4", "Какое значение вернула функция, если тест упал так? Введи число.",
        ["90.5"],
        context="""
        def test_discount():
        >       assert discount(100, 10) == 90
        E       assert 90.5 == 90
        E        +  where 90.5 = discount(100, 10)
        """, hint="pytest раскрывает, что вернула функция."),
    cmd(f"{P}-assert-e5", "Сколько ключей отличается в словарях? Введи число.",
        ["1"],
        context="""
        E       AssertionError: assert {'id': 1, 'name': 'anna', 'role': 'qa'} == {'id': 1, 'name': 'anna', 'role': 'admin'}
        E         Omitting 2 identical items, use -vv to show
        E         Differing items:
        E         {'role': 'qa'} != {'role': 'admin'}
        """),
    pyt(f"{P}-assert-e6", t("""
        Напиши тест `test_sorted`, который проверяет, что `sort_users(users)` возвращает пользователей, отсортированных по возрасту, **и** что исходный список не изменился. Данные: `[{"name": "b", "age": 30}, {"name": "a", "age": 20}]`.
        """),
        """
        import pytest


        def sort_users(users):
            return sorted(users, key=lambda u: u["age"])
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_sorted") == "passed", res

        def test_catches_bugs():
            def mutating(users):
                users.sort(key=lambda u: u["age"])
                return users
            for bug in (lambda users: list(users), mutating):
                code, res = run_pytest(patch={"sort_users": bug})
                assert code == 1, "Тест должен ловить и неверный порядок, и изменение исходного списка"
        """,
        """
        import pytest


        def sort_users(users):
            return sorted(users, key=lambda u: u["age"])


        def test_sorted():
            users = [{"name": "b", "age": 30}, {"name": "a", "age": 20}]
            result = sort_users(users)
            assert [u["age"] for u in result] == [20, 30]
            assert users == [{"name": "b", "age": 30}, {"name": "a", "age": 20}]
        """, hint="Сохрани копию исходных данных или сравни с литералом."),
    cmd(f"{P}-assert-e7", "Что выведет pytest в строке с ошибкой? Какое **ожидаемое** значение длины? Введи число.",
        ["3"],
        context="""
        >       assert len(items) == 3
        E       assert 2 == 3
        E        +  where 2 = len(['a', 'b'])
        """),
    pyt(f"{P}-assert-e8", t("""
        Напиши тест `test_response`, который проверяет ответ `fake_api()`: статус `200`, в теле есть ключ `"items"`, это список, и у **каждого** элемента есть `"id"` типа `int`.
        """),
        """
        import pytest


        def fake_api():
            return {"status": 200, "body": {"items": [{"id": 1}, {"id": 2}]}}
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_response") == "passed", res

        def test_catches_bugs():
            bugs = [
                lambda: {"status": 500, "body": {"items": [{"id": 1}]}},
                lambda: {"status": 200, "body": {}},
                lambda: {"status": 200, "body": {"items": {"id": 1}}},
                lambda: {"status": 200, "body": {"items": [{"id": 1}, {"name": "x"}]}},
                lambda: {"status": 200, "body": {"items": [{"id": "1"}]}},
            ]
            for i, bug in enumerate(bugs):
                code, res = run_pytest(patch={"fake_api": bug})
                assert code == 1, f"Тест не поймал ошибку №{i + 1}: {bug()}"
        """,
        """
        import pytest


        def fake_api():
            return {"status": 200, "body": {"items": [{"id": 1}, {"id": 2}]}}


        def test_response():
            resp = fake_api()
            assert resp["status"] == 200
            assert "items" in resp["body"]
            items = resp["body"]["items"]
            assert isinstance(items, list)
            for item in items:
                assert isinstance(item.get("id"), int)
        """, xp=25),
),

lesson(f"{P}-raises", "Проверка исключений: pytest.raises",
    pyt(f"{P}-raises-e1", t("""
        Напиши тест `test_zero`, который проверяет, что `divide(1, 0)` выбрасывает `ZeroDivisionError`. Используй `with pytest.raises(...)`.
        """),
        """
        import pytest


        def divide(a, b):
            return a / b
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_zero") == "passed", res

        def test_catches_bug():
            code, res = run_pytest(patch={"divide": lambda a, b: 0 if b == 0 else a / b})
            assert code == 1, "Тест должен падать, если исключения нет"
        """,
        """
        import pytest


        def divide(a, b):
            return a / b


        def test_zero():
            with pytest.raises(ZeroDivisionError):
                divide(1, 0)
        """),
    pyt(f"{P}-raises-e2", t("""
        Функция `set_age(age)` должна выбрасывать `ValueError` с текстом, содержащим `"age"`, для отрицательного возраста. Напиши тест `test_negative_age` с проверкой текста через `match=`.
        """),
        """
        import pytest


        def set_age(age):
            if age < 0:
                raise ValueError("age must be >= 0")
            return age
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_negative_age") == "passed", res
            assert "match=" in open("solution.py", encoding="utf-8").read(), "Используй match="

        def test_catches_bugs():
            def wrong_text(age):
                if age < 0:
                    raise ValueError("bad value")
                return age
            def wrong_type(age):
                if age < 0:
                    raise TypeError("age must be >= 0")
                return age
            for bug in (wrong_text, wrong_type, lambda age: age):
                code, res = run_pytest(patch={"set_age": bug})
                assert code == 1, f"Тест пропустил ошибку ({bug.__name__})"
        """,
        """
        import pytest


        def set_age(age):
            if age < 0:
                raise ValueError("age must be >= 0")
            return age


        def test_negative_age():
            with pytest.raises(ValueError, match="age"):
                set_age(-1)
        """),
    pyt(f"{P}-raises-e3", t("""
        Иногда нужно проверить **свойства** исключения. Функция `api_call()` выбрасывает `ApiError` с атрибутом `status`. Напиши тест `test_not_found`: исключение выброшено, и `status == 404`. Используй `with pytest.raises(...) as exc_info` и `exc_info.value`.
        """),
        """
        import pytest


        class ApiError(Exception):
            def __init__(self, status):
                super().__init__(f"HTTP {status}")
                self.status = status


        def api_call():
            raise ApiError(404)
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_not_found") == "passed", res
            assert ".value" in open("solution.py", encoding="utf-8").read(), "Проверь статус через exc_info.value"

        def test_catches_bug():
            def wrong():
                raise sys.modules["solution"].ApiError(500)
            code, res = run_pytest(patch={"api_call": wrong})
            assert code == 1, "Тест должен проверять статус"
        """,
        """
        import pytest


        class ApiError(Exception):
            def __init__(self, status):
                super().__init__(f"HTTP {status}")
                self.status = status


        def api_call():
            raise ApiError(404)


        def test_not_found():
            with pytest.raises(ApiError) as exc_info:
                api_call()
            assert exc_info.value.status == 404
        """),
    cmd(f"{P}-raises-e4", "Почему упал тест? Введи слово `нет`, если исключения не было, или `другое`, если было другое исключение.",
        ["нет"],
        context="""
        def test_zero():
            with pytest.raises(ZeroDivisionError):
        >       divide(1, 0)
        E       Failed: DID NOT RAISE <class 'ZeroDivisionError'>
        """),
    cmd(f"{P}-raises-e5", "Какой текст исключения был **на самом деле**? Введи его без кавычек.",
        ["bad value"],
        context="""
        E   AssertionError: Regex pattern did not match.
        E    Regex: 'age'
        E    Input: 'bad value'
        """),
    pyt(f"{P}-raises-e6", t("""
        Функция `parse_port(value)` превращает строку в номер порта. Напиши тест `test_invalid_ports`, который проверяет, что **каждое** из значений `"abc"`, `"-1"`, `"70000"` выбрасывает `ValueError`. Проверь их в цикле, для каждого — свой `with pytest.raises`.
        """),
        """
        import pytest


        def parse_port(value):
            port = int(value)
            if not 0 < port < 65536:
                raise ValueError(f"порт вне диапазона: {port}")
            return port
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_invalid_ports") == "passed", res

        def test_catches_bugs():
            def no_range(value):
                return int(value)
            def no_upper(value):
                port = int(value)
                if port <= 0:
                    raise ValueError("x")
                return port
            for bug in (no_range, no_upper):
                code, res = run_pytest(patch={"parse_port": bug})
                assert code == 1, f"Тест пропустил ошибку ({bug.__name__})"
        """,
        """
        import pytest


        def parse_port(value):
            port = int(value)
            if not 0 < port < 65536:
                raise ValueError(f"порт вне диапазона: {port}")
            return port


        def test_invalid_ports():
            for value in ["abc", "-1", "70000"]:
                with pytest.raises(ValueError):
                    parse_port(value)
        """, hint="int('abc') тоже выбрасывает ValueError."),
    cmd(f"{P}-raises-e7", "Какой тип исключения ожидали, а какой получили? Введи **полученный** тип.",
        ["TypeError"],
        context="""
        >       set_age("x")
        E       TypeError: '<' not supported between instances of 'str' and 'int'
        """),
    pyt(f"{P}-raises-e8", t("""
        Проверь и **отсутствие** ошибки: напиши два теста для `withdraw(balance, amount)`:

        - `test_ok` — снятие 30 со 100 возвращает 70 (без исключения);
        - `test_not_enough` — снятие 200 со 100 выбрасывает `ValueError` с текстом `"недостаточно"`.
        """),
        """
        import pytest


        def withdraw(balance, amount):
            if amount > balance:
                raise ValueError("недостаточно средств")
            return balance - amount
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"test_ok": "passed", "test_not_enough": "passed"}, res

        def test_catches_bugs():
            def always_raise(balance, amount):
                raise ValueError("недостаточно средств")
            def never_raise(balance, amount):
                return balance - amount
            for bug in (always_raise, never_raise):
                code, res = run_pytest(patch={"withdraw": bug})
                assert code == 1, f"Тесты пропустили ошибку ({bug.__name__})"
        """,
        """
        import pytest


        def withdraw(balance, amount):
            if amount > balance:
                raise ValueError("недостаточно средств")
            return balance - amount


        def test_ok():
            assert withdraw(100, 30) == 70


        def test_not_enough():
            with pytest.raises(ValueError, match="недостаточно"):
                withdraw(100, 200)
        """),
),

lesson(f"{P}-cli", "Запуск: полезные флаги",
    cmd(f"{P}-cli-e1", "Запусти тесты с подробным выводом: имя каждого теста и его результат.",
        ["pytest -v", "pytest --verbose", "python -m pytest -v"]),
    cmd(f"{P}-cli-e2", "Запусти только тесты, в имени которых есть `login`.",
        ["pytest -k login", "pytest -k 'login'", 'pytest -k "login"', "python -m pytest -k login"]),
    cmd(f"{P}-cli-e3", "Останови прогон на **первом** упавшем тесте.",
        ["pytest -x", "pytest --exitfirst", "pytest --maxfail=1", "pytest --maxfail 1"]),
    cmd(f"{P}-cli-e4", "Перезапусти только те тесты, которые упали в прошлый раз.",
        ["pytest --lf", "pytest --last-failed"]),
    cmd(f"{P}-cli-e5", "Запусти один тест `test_checkout` из файла `tests/test_cart.py`.",
        ["pytest tests/test_cart.py::test_checkout", "python -m pytest tests/test_cart.py::test_checkout"]),
    cmd(f"{P}-cli-e6", "Запусти тесты и **показывай print** из тестов (отключи перехват вывода).",
        ["pytest -s", "pytest --capture=no", "pytest -s -v", "pytest -v -s", "pytest -vs", "pytest -sv"]),
    cmd(f"{P}-cli-e7", "Запусти тесты, в имени которых есть `cart`, но нет `slow`.",
        ["pytest -k 'cart and not slow'", 'pytest -k "cart and not slow"']),
    cmd(f"{P}-cli-e8", "Сократи вывод ошибок до одной строки на тест и покажи сводку по всем непрошедшим тестам в конце (флаги `--tb` и `-r`).",
        ["pytest --tb=line -ra", "pytest -ra --tb=line", "pytest --tb=line -rA", "pytest -rA --tb=line", "pytest --tb=line -rf", "pytest -rf --tb=line"],
        xp=15),
),
)
