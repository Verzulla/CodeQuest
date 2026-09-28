"""Тема «pytest», модуль 3 «Маркеры, параллельность, настройка» — задания. Теория — в _pyt_t3.py."""
from ._lib import cmd, lesson, module, pyt, t

P = "pyt"

m3 = module(f"{P}-m3", "Маркеры, параллельность и настройка", "🏷️", "skip, skipif, xfail и свои маркеры, pytest-xdist, pytest.ini и pyproject, хорошие тесты",

lesson(f"{P}-marks", "Маркеры: skip, skipif, xfail и свои",
    pyt(f"{P}-marks-e1", t("""
        Тест `test_new_feature` проверяет ещё не готовую функцию. Пропусти его маркером `skip` с причиной `"фича в разработке"`. Второй тест `test_ready` должен выполняться и проходить.
        """),
        """
        import pytest


        def ready():
            return True
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"test_new_feature": "skipped", "test_ready": "passed"}, res
            assert "reason=" in open("solution.py", encoding="utf-8").read(), "Укажи reason"
        """,
        """
        import pytest


        def ready():
            return True


        @pytest.mark.skip(reason="фича в разработке")
        def test_new_feature():
            assert False


        def test_ready():
            assert ready()
        """),
    pyt(f"{P}-marks-e2", t("""
        Тест `test_unix_path` имеет смысл только не в Windows. Пропусти его через `skipif`, если `sys.platform` начинается с `"win"`. Сам тест проверяет, что `join_path("a", "b") == "a/b"`.
        """),
        """
        import sys
        import pytest


        def join_path(*parts):
            return "/".join(parts)
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"test_unix_path": "passed"}, res
            src = open("solution.py", encoding="utf-8").read()
            assert "skipif" in src and "sys.platform" in src, "Используй skipif с условием на sys.platform"
        """,
        """
        import sys
        import pytest


        def join_path(*parts):
            return "/".join(parts)


        @pytest.mark.skipif(sys.platform.startswith("win"), reason="только Unix")
        def test_unix_path():
            assert join_path("a", "b") == "a/b"
        """),
    pyt(f"{P}-marks-e3", t("""
        Известный баг: `discount(100, 150)` возвращает отрицательную цену. Напиши тест `test_big_discount`, который проверяет, что цена не ниже 0, и пометь его `xfail` с причиной `"BUG-42"` — пока баг не исправлен, тест «ожидаемо падает» и не краснит прогон.
        """),
        """
        import pytest


        def discount(price, percent):
            return price * (100 - percent) / 100
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"test_big_discount": "skipped"}, f"Тест должен быть xfail: {res}"
            assert code == 0, "xfail не должен ронять прогон"
            assert "BUG-42" in open("solution.py", encoding="utf-8").read(), "Укажи причину BUG-42"

        def test_turns_green_when_fixed():
            code, res = run_pytest(patch={"discount": lambda p, pc: max(0, p * (100 - pc) / 100)})
            assert res == {"test_big_discount": "passed"}, f"Когда баг исправят, тест должен пройти (xpass): {res}"
        """,
        """
        import pytest


        def discount(price, percent):
            return price * (100 - percent) / 100


        @pytest.mark.xfail(reason="BUG-42")
        def test_big_discount():
            assert discount(100, 150) >= 0
        """, hint="xfail засчитывается как пропуск; если тест вдруг пройдёт — это xpass."),
    pyt(f"{P}-marks-e4", t("""
        Пометь тесты своими маркерами: `test_login` и `test_logout` — `@pytest.mark.smoke`, `test_report` — `@pytest.mark.slow`. Проверка запустит `pytest -m smoke` и убедится, что выполнились только smoke-тесты.
        """),
        """
        import pytest


        def test_login():
            assert True


        def test_logout():
            assert True


        def test_report():
            assert True
        """,
        """
        def test_written():
            code, res = run_pytest("-m", "smoke", "-p", "no:warnings")
            assert res == {"test_login": "passed", "test_logout": "passed"}, f"-m smoke должен выбрать 2 теста: {res}"
            code, res = run_pytest("-m", "slow", "-p", "no:warnings")
            assert res == {"test_report": "passed"}, res
        """,
        """
        import pytest


        @pytest.mark.smoke
        def test_login():
            assert True


        @pytest.mark.smoke
        def test_logout():
            assert True


        @pytest.mark.slow
        def test_report():
            assert True
        """),
    cmd(f"{P}-marks-e5", "Запусти только тесты с маркером `smoke`.",
        ["pytest -m smoke", "pytest -m 'smoke'", 'pytest -m "smoke"', "python -m pytest -m smoke"]),
    cmd(f"{P}-marks-e6", "Запусти все тесты, **кроме** помеченных `slow`.",
        ["pytest -m 'not slow'", 'pytest -m "not slow"', "python -m pytest -m 'not slow'"]),
    cmd(f"{P}-marks-e7", "Сколько тестов **пропущено** (skip)? Введи число.",
        ["2"],
        context="""
        $ pytest -q
        ..s.xs.                                                                  [100%]
        4 passed, 2 skipped, 1 xfailed in 0.05s
        """, hint="s — skipped, x — xfailed."),
    cmd(f"{P}-marks-e8", "Какую строку добавить в секцию `markers` файла `pytest.ini`, чтобы зарегистрировать маркер `smoke` с описанием «быстрые проверки» (без предупреждения PytestUnknownMarkWarning)?",
        ["smoke: быстрые проверки", "smoke:быстрые проверки"], xp=15),
),

lesson(f"{P}-xdist", "Параллельный запуск: pytest-xdist",
    cmd(f"{P}-xdist-e1", "Установи плагин для параллельного запуска тестов.",
        ["pip install pytest-xdist", "python -m pip install pytest-xdist", "uv add --dev pytest-xdist", "uv add pytest-xdist --dev"]),
    cmd(f"{P}-xdist-e2", "Запусти тесты в 4 параллельных процессах.",
        ["pytest -n 4", "pytest -n4", "python -m pytest -n 4", "pytest --numprocesses 4", "pytest --numprocesses=4"]),
    cmd(f"{P}-xdist-e3", "Запусти тесты в стольких процессах, сколько ядер у процессора.",
        ["pytest -n auto", "python -m pytest -n auto", "pytest --numprocesses=auto", "pytest --numprocesses auto", "pytest -n logical"]),
    cmd(f"{P}-xdist-e4", "Запусти параллельно так, чтобы все тесты **одного модуля** выполнялись на одном воркере (нужно, если у них общая module-фикстура).",
        ["pytest -n 4 --dist loadscope", "pytest -n 4 --dist=loadscope", "pytest --dist loadscope -n 4", "pytest -n auto --dist loadscope",
         "pytest -n auto --dist=loadscope", "pytest -n 4 --dist loadfile", "pytest -n auto --dist loadfile"]),
    cmd(f"{P}-xdist-e5", "Сколько воркеров запущено? Введи число.",
        ["4"],
        context="""
        $ pytest -n auto
        4 workers [120 items]
        ........................................................................ [ 60%]
        ................................................                         [100%]
        120 passed in 8.31s
        """),
    pyt(f"{P}-xdist-e6", t("""
        Тесты, которые делят общее изменяемое состояние, при параллельном запуске ломаются. Исправь тесты: сейчас `test_add` и `test_count` используют общий глобальный список `CART`. Сделай фикстуру `cart`, возвращающую **новый** список, и перепиши оба теста на неё, чтобы они были независимы и проходили в любом порядке и параллельно.
        """),
        """
        import pytest

        CART = []


        def test_add():
            CART.append("чай")
            assert CART == ["чай"]


        def test_count():
            assert len(CART) == 0
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"test_add": "passed", "test_count": "passed"}, res
            import re
            src = open("solution.py", encoding="utf-8").read()
            assert re.search(r"def test_add\\(\\s*cart", src) and re.search(r"def test_count\\(\\s*cart", src), "Тесты должны получать фикстуру cart"

        def test_parallel():
            code, res = run_pytest("-n", "2")
            assert res.get("test_add") == "passed" and res.get("test_count") == "passed", f"Параллельно тесты тоже должны проходить: {res}"
        """,
        """
        import pytest


        @pytest.fixture
        def cart():
            return []


        def test_add(cart):
            cart.append("чай")
            assert cart == ["чай"]


        def test_count(cart):
            assert len(cart) == 0
        """),
    cmd(f"{P}-xdist-e7", "Можно ли рассчитывать на **порядок** выполнения тестов при `pytest -n 4`? Ответь `да` или `нет`.",
        ["нет"], hint="Тесты раздаются воркерам по мере освобождения."),
    cmd(f"{P}-xdist-e8", "Как узнать в фикстуре номер текущего воркера xdist? Введи имя переменной окружения, которую выставляет xdist.",
        ["PYTEST_XDIST_WORKER"], hint="Значения вида gw0, gw1…; удобно для уникальных тестовых данных на воркер.", xp=15),
),

lesson(f"{P}-config", "Настройка: pytest.ini и pyproject.toml",
    cmd(f"{P}-config-e1", "Как называется секция pytest в файле `pyproject.toml`? Введи заголовок.",
        ["[tool.pytest.ini_options]"]),
    cmd(f"{P}-config-e2", "Какую строку добавить в секцию настроек pytest, чтобы тесты искались только в папке `tests`?",
        ['testpaths = ["tests"]', "testpaths = ['tests']", "testpaths = tests"]),
    cmd(f"{P}-config-e3", "Какую строку добавить, чтобы pytest **всегда** запускался с флагами `-v --tb=short`?",
        ['addopts = "-v --tb=short"', "addopts = '-v --tb=short'", "addopts = -v --tb=short"]),
    cmd(f"{P}-config-e4", "С какими флагами на самом деле запустится pytest? Введи их через пробел (сначала из настроек).",
        ["-v -n 2 -x"],
        context="""
        [tool.pytest.ini_options]
        addopts = "-v -n 2"

        $ pytest -x
        """, hint="addopts добавляется перед флагами из командной строки."),
    cmd(f"{P}-config-e5", "Покажи, какие тесты pytest **найдёт**, не запуская их.",
        ["pytest --collect-only", "pytest --co", "pytest --collect-only -q", "pytest --co -q"]),
    cmd(f"{P}-config-e6", "Запусти pytest, **временно отключив** addopts из конфига (флаг переопределения опций `-o`).",
        ['pytest -o addopts=""', "pytest -o addopts=''", "pytest -o addopts="]),
    cmd(f"{P}-config-e7", "Какую строку добавить в настройки, чтобы любые предупреждения превращались в ошибки (правило для `filterwarnings`)? Введи значение правила.",
        ["error"]),
    cmd(f"{P}-config-e8", "Какой минимальной версии pytest требует проект? Введи номер.",
        ["8.0"],
        context="""
        [tool.pytest.ini_options]
        minversion = "8.0"
        testpaths = ["tests"]
        markers = ["smoke: быстрые проверки", "slow: долгие тесты"]
        """),
),

lesson(f"{P}-practice", "Практика: хорошие тесты",
    pyt(f"{P}-practice-e1", t("""
        Тест в стиле **AAA** (Arrange — Act — Assert). Напиши `test_checkout` для класса `Cart`: подготовь корзину с товарами по 100 и 250 (Arrange), вызови `checkout()` (Act), проверь, что вернулось `350` и корзина стала пустой (Assert).
        """),
        """
        import pytest


        class Cart:
            def __init__(self):
                self.items = []

            def add(self, price):
                self.items.append(price)

            def checkout(self):
                total = sum(self.items)
                self.items.clear()
                return total
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_checkout") == "passed", res

        def test_catches_bugs():
            class NoClear(sys.modules["solution"].Cart):
                def checkout(self):
                    return sum(self.items)
            class WrongSum(sys.modules["solution"].Cart):
                def checkout(self):
                    total = max(self.items)
                    self.items.clear()
                    return total
            for bug in (NoClear, WrongSum):
                code, res = run_pytest(patch={"Cart": bug})
                assert code == 1, f"Тест пропустил ошибку ({bug.__name__})"
        """,
        """
        import pytest


        class Cart:
            def __init__(self):
                self.items = []

            def add(self, price):
                self.items.append(price)

            def checkout(self):
                total = sum(self.items)
                self.items.clear()
                return total


        def test_checkout():
            cart = Cart()
            cart.add(100)
            cart.add(250)

            total = cart.checkout()

            assert total == 350
            assert cart.items == []
        """),
    pyt(f"{P}-practice-e2", t("""
        Граничные значения: функция `can_register(age)` разрешает регистрацию с 18 до 99 лет включительно. Напиши параметризованный тест `test_age(age, expected)`, покрывающий **обе границы с обеих сторон**: 17, 18, 99, 100.
        """),
        """
        import pytest


        def can_register(age):
            return 18 <= age <= 99
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert len(res) >= 4 and all(v == "passed" for v in res.values()), res

        def test_catches_boundary_bugs():
            bugs = [lambda a: 18 < a <= 99, lambda a: 18 <= a < 99, lambda a: 17 <= a <= 99, lambda a: 18 <= a <= 100]
            for i, bug in enumerate(bugs):
                code, res = run_pytest(patch={"can_register": bug})
                assert code == 1, f"Тест пропустил ошибку на границе (вариант {i + 1})"
        """,
        """
        import pytest


        def can_register(age):
            return 18 <= age <= 99


        @pytest.mark.parametrize("age, expected", [(17, False), (18, True), (99, True), (100, False)])
        def test_age(age, expected):
            assert can_register(age) == expected
        """),
    pyt(f"{P}-practice-e3", t("""
        Тест не должен зависеть от реального времени. Функция `greeting(now)` принимает время параметром. Напиши параметризованный тест `test_greeting(hour, expected)` для часов `9 → "Доброе утро"`, `15 → "Добрый день"`, `22 → "Добрый вечер"`, создавая `datetime(2024, 3, 8, hour)`.
        """),
        """
        from datetime import datetime
        import pytest


        def greeting(now):
            if now.hour < 12:
                return "Доброе утро"
            if now.hour < 18:
                return "Добрый день"
            return "Добрый вечер"
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert len(res) == 3 and all(v == "passed" for v in res.values()), res

        def test_catches_bug():
            code, res = run_pytest(patch={"greeting": lambda now: "Доброе утро"})
            assert code == 1, "Тест должен ловить неправильное приветствие"
        """,
        """
        from datetime import datetime
        import pytest


        def greeting(now):
            if now.hour < 12:
                return "Доброе утро"
            if now.hour < 18:
                return "Добрый день"
            return "Добрый вечер"


        @pytest.mark.parametrize("hour, expected", [(9, "Доброе утро"), (15, "Добрый день"), (22, "Добрый вечер")])
        def test_greeting(hour, expected):
            assert greeting(datetime(2024, 3, 8, hour)) == expected
        """),
    pyt(f"{P}-practice-e4", t("""
        Замени обращение к «сети» подделкой. Класс `UserService` получает клиента в конструкторе. Напиши фейковый класс `FakeClient` с методом `get(path)`, который для `"/users/1"` возвращает `{"id": 1, "name": "anna"}`, и тест `test_name`, проверяющий, что `UserService(FakeClient()).name(1) == "anna"`.
        """),
        """
        import pytest


        class UserService:
            def __init__(self, client):
                self.client = client

            def name(self, user_id):
                return self.client.get(f"/users/{user_id}")["name"]
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_name") == "passed", res
            assert "class FakeClient" in open("solution.py", encoding="utf-8").read(), "Нужен класс FakeClient"

        def test_catches_bug():
            class Broken(sys.modules["solution"].UserService):
                def name(self, user_id):
                    return self.client.get(f"/users/{user_id + 1}").get("name")
            code, res = run_pytest(patch={"UserService": Broken})
            assert code == 1, "Тест должен ловить запрос не того пользователя"
        """,
        """
        import pytest


        class UserService:
            def __init__(self, client):
                self.client = client

            def name(self, user_id):
                return self.client.get(f"/users/{user_id}")["name"]


        class FakeClient:
            def get(self, path):
                data = {"/users/1": {"id": 1, "name": "anna"}}
                return data.get(path, {})


        def test_name():
            assert UserService(FakeClient()).name(1) == "anna"
        """),
    cmd(f"{P}-practice-e5", "Тест проходит при запуске в одиночку, но падает в общем прогоне. Как называют такой тест? Введи одно слово латиницей.",
        ["flaky"]),
    cmd(f"{P}-practice-e6", "Перезапусти только упавшие в прошлый раз тесты, а после них — все остальные (флаг «сначала упавшие»).",
        ["pytest --ff", "pytest --failed-first"]),
    cmd(f"{P}-practice-e7", "Покажи 5 самых медленных тестов после прогона.",
        ["pytest --durations=5", "pytest --durations 5"]),
    pyt(f"{P}-practice-e8", t("""
        Итоговое задание. Для функции `validate_password(pw)` (возвращает список ошибок) напиши набор тестов:

        - параметризованный `test_valid(pw)` для двух хороших паролей: `"Secret123"` и `"Qwerty2024x"` (ошибок нет);
        - параметризованный `test_invalid(pw, error)` для случаев: `"Ab1"` → `"короткий"`, `"secret123"` → `"нет заглавной"`, `"SecretPass"` → `"нет цифры"` (ошибка есть в списке);
        - `test_none` — `validate_password(None)` выбрасывает `TypeError`.
        """),
        """
        import pytest


        def validate_password(pw):
            if not isinstance(pw, str):
                raise TypeError("пароль должен быть строкой")
            errors = []
            if len(pw) < 8:
                errors.append("короткий")
            if not any(c.isupper() for c in pw):
                errors.append("нет заглавной")
            if not any(c.isdigit() for c in pw):
                errors.append("нет цифры")
            return errors
        """,
        """
        def test_written():
            code, res = run_pytest()
            names = sorted(res)
            assert sum(n.startswith("test_valid[") for n in names) == 2, names
            assert sum(n.startswith("test_invalid[") for n in names) == 3, names
            assert res.get("test_none") == "passed" and all(v == "passed" for v in res.values()), res

        def test_catches_bugs():
            real = sys.modules["solution"].validate_password
            def no_len(pw):
                return [e for e in real(pw) if e != "короткий"]
            def no_upper(pw):
                return [e for e in real(pw) if e != "нет заглавной"]
            def no_digit(pw):
                return [e for e in real(pw) if e != "нет цифры"]
            def no_type(pw):
                return [] if pw is None else real(pw)
            def too_strict(pw):
                return real(pw) + ["слабый"]
            for bug in (no_len, no_upper, no_digit, no_type, too_strict):
                code, res = run_pytest(patch={"validate_password": bug})
                assert code == 1, f"Тесты пропустили ошибку ({bug.__name__})"
        """,
        """
        import pytest


        def validate_password(pw):
            if not isinstance(pw, str):
                raise TypeError("пароль должен быть строкой")
            errors = []
            if len(pw) < 8:
                errors.append("короткий")
            if not any(c.isupper() for c in pw):
                errors.append("нет заглавной")
            if not any(c.isdigit() for c in pw):
                errors.append("нет цифры")
            return errors


        @pytest.mark.parametrize("pw", ["Secret123", "Qwerty2024x"])
        def test_valid(pw):
            assert validate_password(pw) == []


        @pytest.mark.parametrize("pw, error", [("Ab1", "короткий"), ("secret123", "нет заглавной"), ("SecretPass", "нет цифры")])
        def test_invalid(pw, error):
            assert error in validate_password(pw)


        def test_none():
            with pytest.raises(TypeError):
                validate_password(None)
        """, xp=30),
),
)
