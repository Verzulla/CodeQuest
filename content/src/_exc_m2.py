"""Тема «Исключения», модуль 2 «Выбрасывание исключений» — задания. Теория — в _exc_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "exc"

m2 = module(f"{P}-m2", "Выбрасывание исключений", "🚨", "raise, свои исключения, повторный выброс и цепочки, assert",

lesson(f"{P}-m2-l1", "raise: сообщить об ошибке",
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        def set_age(age):
            if age < 0:
                raise ValueError(f"возраст не может быть отрицательным: {age}")
            return age

        print(set_age(30))
        try:
            set_age(-5)
        except ValueError as e:
            print("ошибка:", e)
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа? Выбор типа ошибки.", """
        def check(value):
            if not isinstance(value, int):
                raise TypeError("нужно целое число")
            if value <= 0:
                raise ValueError("нужно положительное")
            return "ok"

        for v in [5, "5", -1]:
            try:
                print(check(v))
            except (TypeError, ValueError) as e:
                print(type(e).__name__, "-", e)
        """),
    out(f"{P}-m2-l1-e3", "Что выведет программа? raise прерывает функцию.", """
        def f():
            print("начало")
            raise RuntimeError("стоп")
            print("не выполнится")

        try:
            f()
        except RuntimeError as e:
            print(e.args)
        """, hint="e.args — кортеж аргументов, переданных в исключение."),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `withdraw(balance, amount)` — вернуть новый баланс. Если `amount <= 0` — `ValueError("сумма должна быть положительной")`; если `amount > balance` — `ValueError("недостаточно средств")`.
        """),
        """
        def withdraw(balance, amount):
            pass
        """,
        """
        def expect_error(func, text):
            try:
                func()
            except ValueError as e:
                assert str(e) == text, f"Текст ошибки: {e}"
                return
            assert False, "Нужен ValueError"

        def test_ok():
            assert withdraw(100, 30) == 70, "Неверный баланс"

        def test_errors():
            expect_error(lambda: withdraw(100, 0), "сумма должна быть положительной")
            expect_error(lambda: withdraw(100, 500), "недостаточно средств")
        """,
        """
        def withdraw(balance, amount):
            if amount <= 0:
                raise ValueError("сумма должна быть положительной")
            if amount > balance:
                raise ValueError("недостаточно средств")
            return balance - amount
        """),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `parse_port(text)` — номер порта из строки. Не число — `ValueError("порт должен быть числом")`; вне диапазона 1–65535 — `ValueError("порт вне диапазона")`.
        """),
        """
        def parse_port(text):
            pass
        """,
        """
        def test_values():
            assert parse_port("8080") == 8080, "Неверный порт"
            for bad, msg in [("x", "порт должен быть числом"), ("0", "порт вне диапазона"), ("70000", "порт вне диапазона")]:
                try:
                    parse_port(bad)
                except ValueError as e:
                    assert str(e) == msg, f"Для {bad!r} текст: {e}"
                    continue
                assert False, f"Для {bad!r} нужен ValueError"
        """,
        """
        def parse_port(text):
            if not text.isdigit():
                raise ValueError("порт должен быть числом")
            port = int(text)
            if not 1 <= port <= 65535:
                raise ValueError("порт вне диапазона")
            return port
        """),
    cod(f"{P}-m2-l1-e6", t("""
        Напиши функцию `require(data, *keys)` — проверить, что в словаре есть все ключи; иначе `KeyError` с именем **первого** отсутствующего. Если всё есть — вернуть `True`.
        """),
        """
        def require(data, *keys):
            pass
        """,
        """
        def test_values():
            assert require({"a": 1, "b": 2}, "a", "b") is True, "Все ключи есть"
            try:
                require({"a": 1}, "a", "x", "y")
            except KeyError as e:
                assert e.args[0] == "x", f"Первый отсутствующий — x, получено {e.args}"
                return
            assert False, "Нужен KeyError"
        """,
        """
        def require(data, *keys):
            for key in keys:
                if key not in data:
                    raise KeyError(key)
            return True
        """),
    cod(f"{P}-m2-l1-e7", t("""
        Напиши функцию `make_user(name, age)` — словарь пользователя. Проверки: `name` — непустая строка, иначе `TypeError("name: нужна непустая строка")`; `age` — `int` от 0 до 150, иначе `ValueError("age: от 0 до 150")`.
        """),
        """
        def make_user(name, age):
            pass
        """,
        """
        def test_ok():
            assert make_user("Аня", 25) == {"name": "Аня", "age": 25}, "Неверный пользователь"

        def test_errors():
            for args, exc in [(("", 1), TypeError), ((5, 1), TypeError), (("a", -1), ValueError), (("a", 200), ValueError), (("a", "5"), ValueError)]:
                try:
                    make_user(*args)
                except exc:
                    continue
                assert False, f"Для {args} нужен {exc.__name__}"
        """,
        """
        def make_user(name, age):
            if not isinstance(name, str) or not name:
                raise TypeError("name: нужна непустая строка")
            if not isinstance(age, int) or not 0 <= age <= 150:
                raise ValueError("age: от 0 до 150")
            return {"name": name, "age": age}
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `check_status(response)` — `response` словарь с полем `"status"`. Для кода `>= 400` выбросить `RuntimeError("HTTP <код>")`, иначе вернуть `response` без изменений. Так работает `raise_for_status` в HTTP-библиотеках.
        """),
        """
        def check_status(response):
            pass
        """,
        """
        def test_values():
            r = {"status": 200, "body": "ok"}
            assert check_status(r) is r, "Успешный ответ возвращается как есть"
            try:
                check_status({"status": 404})
            except RuntimeError as e:
                assert str(e) == "HTTP 404", f"Текст: {e}"
                return
            assert False, "Нужен RuntimeError"
        """,
        """
        def check_status(response):
            if response["status"] >= 400:
                raise RuntimeError(f"HTTP {response['status']}")
            return response
        """),
),

lesson(f"{P}-m2-l2", "Свои исключения",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        class ValidationError(Exception):
            pass

        try:
            raise ValidationError("email без @")
        except ValidationError as e:
            print(type(e).__name__, "-", e)
        print(issubclass(ValidationError, Exception))
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа? Иерархия своих ошибок.", """
        class AppError(Exception):
            pass

        class NotFound(AppError):
            pass

        class Forbidden(AppError):
            pass

        for err in [NotFound("нет пользователя"), Forbidden("нет доступа")]:
            try:
                raise err
            except AppError as e:
                print(type(e).__name__, e)
        """),
    out(f"{P}-m2-l2-e3", "Что выведет программа? Ошибка с данными.", """
        class HttpError(Exception):
            def __init__(self, status, message):
                super().__init__(f"{status}: {message}")
                self.status = status

        try:
            raise HttpError(503, "сервис недоступен")
        except HttpError as e:
            print(e.status, str(e))
        """, hint="Своё исключение может хранить дополнительные поля."),
    cod(f"{P}-m2-l2-e4", t("""
        Объяви своё исключение `ValidationError` (наследник `Exception`) и функцию `validate_email(email)`: если в адресе нет `@` — выбросить `ValidationError("нет @")`, иначе вернуть адрес.
        """),
        """
        def validate_email(email):
            pass
        """,
        """
        def test_values():
            assert validate_email("a@x.ru") == "a@x.ru", "Корректный адрес возвращается"
            assert issubclass(ValidationError, Exception), "ValidationError — наследник Exception"
            try:
                validate_email("bad")
            except ValidationError as e:
                assert str(e) == "нет @", f"Текст: {e}"
                return
            assert False, "Нужен ValidationError"
        """,
        """
        class ValidationError(Exception):
            pass

        def validate_email(email):
            if "@" not in email:
                raise ValidationError("нет @")
            return email
        """, hint="class ValidationError(Exception): pass — этого достаточно."),
    cod(f"{P}-m2-l2-e5", t("""
        Создай иерархию: `ApiError(Exception)`, от неё `NotFoundError` и `AuthError`. Напиши функцию `raise_for(status)`: `404` → `NotFoundError("не найдено")`, `401`/`403` → `AuthError("нет доступа")`, другие `>= 400` → `ApiError("ошибка <код>")`; иначе вернуть `"ok"`.
        """),
        """
        def raise_for(status):
            pass
        """,
        """
        def test_hierarchy():
            assert issubclass(NotFoundError, ApiError) and issubclass(AuthError, ApiError) and issubclass(ApiError, Exception), "Неверная иерархия"

        def test_values():
            assert raise_for(200) == "ok", "200 — ok"
            for status, exc, msg in [(404, NotFoundError, "не найдено"), (403, AuthError, "нет доступа"), (500, ApiError, "ошибка 500")]:
                try:
                    raise_for(status)
                except exc as e:
                    assert str(e) == msg and type(e) is exc, f"{status}: {type(e).__name__} {e}"
                    continue
                assert False, f"{status}: нужен {exc.__name__}"
        """,
        """
        class ApiError(Exception):
            pass

        class NotFoundError(ApiError):
            pass

        class AuthError(ApiError):
            pass

        def raise_for(status):
            if status == 404:
                raise NotFoundError("не найдено")
            if status in (401, 403):
                raise AuthError("нет доступа")
            if status >= 400:
                raise ApiError(f"ошибка {status}")
            return "ok"
        """, xp=20),
    cod(f"{P}-m2-l2-e6", t("""
        Используя иерархию из предыдущего задания (объяви её заново), напиши функцию `safe_call(status)` — вызвать `raise_for(status)` и вернуть `"ok"`, а при любой `ApiError` — строку `"<ИмяКласса>: <текст>"`.
        """),
        """
        def safe_call(status):
            pass
        """,
        """
        def test_values():
            assert [safe_call(200), safe_call(404), safe_call(401), safe_call(502)] == ["ok", "NotFoundError: не найдено", "AuthError: нет доступа", "ApiError: ошибка 502"], "Неверный результат"
        """,
        """
        class ApiError(Exception):
            pass

        class NotFoundError(ApiError):
            pass

        class AuthError(ApiError):
            pass

        def raise_for(status):
            if status == 404:
                raise NotFoundError("не найдено")
            if status in (401, 403):
                raise AuthError("нет доступа")
            if status >= 400:
                raise ApiError(f"ошибка {status}")
            return "ok"

        def safe_call(status):
            try:
                return raise_for(status)
            except ApiError as e:
                return f"{type(e).__name__}: {e}"
        """),
    cod(f"{P}-m2-l2-e7", t("""
        Объяви исключение `HttpError` с полем `status`: конструктор принимает `status` и `message`, передаёт в `super().__init__` строку `"<status>: <message>"` и сохраняет `self.status`. Напиши функцию `get_status(func)` — вызвать `func()`; при `HttpError` вернуть его `status`, иначе `200`.
        """),
        """
        def get_status(func):
            pass
        """,
        """
        def test_values():
            def fail():
                raise HttpError(503, "down")
            e = HttpError(404, "нет")
            assert str(e) == "404: нет" and e.status == 404, "Неверное исключение"
            assert get_status(fail) == 503 and get_status(lambda: None) == 200, "Неверный статус"
        """,
        """
        class HttpError(Exception):
            def __init__(self, status, message):
                super().__init__(f"{status}: {message}")
                self.status = status

        def get_status(func):
            try:
                func()
            except HttpError as e:
                return e.status
            return 200
        """, xp=20),
    cod(f"{P}-m2-l2-e8", t("""
        Объяви `ValidationError(Exception)` с полем `errors` — списком сообщений (конструктор принимает список, текст исключения — сообщения через `"; "`). Напиши `validate(user)`: собрать все ошибки (`name` пустое → `"name пустое"`, `age < 0` → `"age отрицательный"`) и выбросить **одно** исключение со всеми; если ошибок нет — вернуть `True`.
        """),
        """
        def validate(user):
            pass
        """,
        """
        def test_values():
            assert validate({"name": "a", "age": 1}) is True, "Корректный пользователь"
            try:
                validate({"name": "", "age": -1})
            except ValidationError as e:
                assert e.errors == ["name пустое", "age отрицательный"] and str(e) == "name пустое; age отрицательный", f"{e.errors} / {e}"
                return
            assert False, "Нужен ValidationError"
        """,
        """
        class ValidationError(Exception):
            def __init__(self, errors):
                super().__init__("; ".join(errors))
                self.errors = errors

        def validate(user):
            errors = []
            if not user["name"]:
                errors.append("name пустое")
            if user["age"] < 0:
                errors.append("age отрицательный")
            if errors:
                raise ValidationError(errors)
            return True
        """, xp=25),
),

lesson(f"{P}-m2-l3", "Повторный выброс и цепочки",
    out(f"{P}-m2-l3-e1", "Что выведет программа? raise без аргументов.", """
        log = []

        def process():
            try:
                1 / 0
            except ZeroDivisionError:
                log.append("записали в лог")
                raise

        try:
            process()
        except ZeroDivisionError:
            print("снаружи тоже поймали", log)
        """, hint="raise без аргументов внутри except выбрасывает то же исключение дальше."),
    out(f"{P}-m2-l3-e2", "Что выведет программа? raise ... from.", """
        class ConfigError(Exception):
            pass

        def load(cfg):
            try:
                return int(cfg["port"])
            except (KeyError, ValueError) as e:
                raise ConfigError("плохой конфиг") from e

        try:
            load({"port": "x"})
        except ConfigError as e:
            print(e, "| причина:", type(e.__cause__).__name__)
        """),
    out(f"{P}-m2-l3-e3", "Что выведет программа? Неявная цепочка.", """
        try:
            try:
                {}["x"]
            except KeyError:
                raise ValueError("не нашли")
        except ValueError as e:
            print(e, "|", type(e.__context__).__name__, e.__cause__)
        """, hint="Без from Python сам запоминает исходную ошибку в __context__."),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `logged_div(a, b, log)` — вернуть `a / b`; при `ZeroDivisionError` добавить в список `log` строку `"деление на ноль"` и **выбросить ту же ошибку дальше** (`raise`).
        """),
        """
        def logged_div(a, b, log):
            pass
        """,
        """
        def test_values():
            log = []
            assert logged_div(6, 3, log) == 2.0 and log == [], "Успешное деление"
            try:
                logged_div(1, 0, log)
            except ZeroDivisionError:
                assert log == ["деление на ноль"], f"log = {log}"
                return
            assert False, "Ошибка должна пройти дальше"
        """,
        """
        def logged_div(a, b, log):
            try:
                return a / b
            except ZeroDivisionError:
                log.append("деление на ноль")
                raise
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Объяви `ConfigError(Exception)` и функцию `load_port(cfg)` — `int(cfg["port"])`. При `KeyError` или `ValueError` выбросить `ConfigError("плохой порт")` **с указанием причины** (`from e`).
        """),
        """
        def load_port(cfg):
            pass
        """,
        """
        def test_values():
            assert load_port({"port": "80"}) == 80, "Корректный порт"
            for cfg, cause in [({}, KeyError), ({"port": "x"}, ValueError)]:
                try:
                    load_port(cfg)
                except ConfigError as e:
                    assert str(e) == "плохой порт" and isinstance(e.__cause__, cause), f"Причина: {e.__cause__!r}"
                    continue
                assert False, "Нужен ConfigError"
        """,
        """
        class ConfigError(Exception):
            pass

        def load_port(cfg):
            try:
                return int(cfg["port"])
            except (KeyError, ValueError) as e:
                raise ConfigError("плохой порт") from e
        """),
    cod(f"{P}-m2-l3-e6", t("""
        Напиши функцию `root_cause(exc)` — пройти по цепочке `__cause__` (а если его нет — `__context__`) до самой первой ошибки и вернуть имя её типа.
        """),
        """
        def root_cause(exc):
            pass
        """,
        """
        def test_values():
            try:
                try:
                    try:
                        {}["x"]
                    except KeyError as e:
                        raise ValueError("v") from e
                except ValueError:
                    raise RuntimeError("r")
            except RuntimeError as e:
                assert root_cause(e) == "KeyError", f"Получено {root_cause(e)}"
            assert root_cause(TypeError("t")) == "TypeError", "Без цепочки — сама ошибка"
        """,
        """
        def root_cause(exc):
            while True:
                nxt = exc.__cause__ or exc.__context__
                if nxt is None:
                    return type(exc).__name__
                exc = nxt
        """, xp=20),
    cod(f"{P}-m2-l3-e7", t("""
        Напиши функцию `convert_all(values)` — список `int` из строк. Если какая-то строка не число, выбросить `ValueError(f"элемент {i}: {значение!r}")` (номер с 0) с причиной — исходной ошибкой.
        """),
        """
        def convert_all(values):
            pass
        """,
        """
        def test_values():
            assert convert_all(["1", "2"]) == [1, 2], "Корректный список"
            try:
                convert_all(["1", "x", "3"])
            except ValueError as e:
                assert str(e) == "элемент 1: 'x'" and isinstance(e.__cause__, ValueError), f"{e} / {e.__cause__!r}"
                return
            assert False, "Нужен ValueError"
        """,
        """
        def convert_all(values):
            result = []
            for i, v in enumerate(values):
                try:
                    result.append(int(v))
                except ValueError as e:
                    raise ValueError(f"элемент {i}: {v!r}") from e
            return result
        """),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `quiet(func, default)` — вызвать `func()`; при ошибке вернуть `default`, **скрыв** причину: если нужно выбросить новое исключение — используй `from None`. Здесь проще: функция просто возвращает `default`. Дополнительно напиши функцию `wrap(func)` — при любой ошибке выбросить `RuntimeError("сбой")` **без** цепочки (`from None`, чтобы `__cause__` был `None` и `__suppress_context__` был `True`).
        """),
        """
        def quiet(func, default):
            pass

        def wrap(func):
            pass
        """,
        """
        def test_quiet():
            assert quiet(lambda: 1 / 0, 0) == 0 and quiet(lambda: 5, 0) == 5, "Неверный результат"

        def test_wrap():
            try:
                wrap(lambda: {}["x"])
            except RuntimeError as e:
                assert str(e) == "сбой" and e.__cause__ is None and e.__suppress_context__, "Используй raise ... from None"
                return
            assert False, "Нужен RuntimeError"
        """,
        """
        def quiet(func, default):
            try:
                return func()
            except Exception:
                return default

        def wrap(func):
            try:
                return func()
            except Exception:
                raise RuntimeError("сбой") from None
        """),
),

lesson(f"{P}-m2-l4", "assert и AssertionError",
    out(f"{P}-m2-l4-e1", "Что выведет программа?", """
        def average(nums):
            assert len(nums) > 0, "список пуст"
            return sum(nums) / len(nums)

        print(average([2, 4]))
        try:
            average([])
        except AssertionError as e:
            print("AssertionError:", e)
        """),
    out(f"{P}-m2-l4-e2", "Что выведет программа? Ловушка со скобками.", """
        try:
            assert (1 == 2, "никогда не сработает")
            print("assert прошёл!")
        except AssertionError:
            print("упал")
        """, hint="Скобки создали непустой кортеж — он всегда истинен."),
    out(f"{P}-m2-l4-e3", "Что выведет программа?", """
        print(issubclass(AssertionError, Exception))
        results = []
        for x in [1, -1]:
            try:
                assert x > 0, f"{x} не положительное"
                results.append("ok")
            except AssertionError as e:
                results.append(str(e))
        print(results)
        """),
    cod(f"{P}-m2-l4-e4", t("""
        Напиши функцию `check_equal(actual, expected)` — проверка для тестов: если значения различаются, `assert` с сообщением `"ожидали <expected!r>, получили <actual!r>"`; иначе вернуть `True`.
        """),
        """
        def check_equal(actual, expected):
            pass
        """,
        """
        def test_values():
            assert check_equal(1, 1) is True, "Равные — True"
            try:
                check_equal("5", 5)
            except AssertionError as e:
                assert str(e) == "ожидали 5, получили '5'", f"Текст: {e}"
                return
            assert False, "Нужен AssertionError"
        """,
        """
        def check_equal(actual, expected):
            assert actual == expected, f"ожидали {expected!r}, получили {actual!r}"
            return True
        """),
    cod(f"{P}-m2-l4-e5", t("""
        Исправь «вечно проходящий» `assert` из заготовки — скобки превратили его в проверку кортежа.
        """),
        """
        def check_positive(x):
            assert (x > 0, "нужно положительное")
            return x
        """,
        """
        def test_values():
            assert check_positive(5) == 5, "Положительное проходит"
            try:
                check_positive(-1)
            except AssertionError as e:
                assert str(e) == "нужно положительное", f"Текст: {e}"
                return
            assert False, "Для -1 нужен AssertionError"
        """,
        """
        def check_positive(x):
            assert x > 0, "нужно положительное"
            return x
        """),
    cod(f"{P}-m2-l4-e6", t("""
        Напиши функцию `run_checks(checks)` — `checks` это словарь «название → функция без аргументов, которая делает assert». Вернуть словарь «название → `"ok"` или текст ошибки AssertionError».
        """),
        """
        def run_checks(checks):
            pass
        """,
        """
        def test_values():
            def good():
                assert 1 == 1
            def bad():
                assert 1 == 2, "1 != 2"
            assert run_checks({"good": good, "bad": bad}) == {"good": "ok", "bad": "1 != 2"}, "Неверный результат"
        """,
        """
        def run_checks(checks):
            result = {}
            for name, check in checks.items():
                try:
                    check()
                    result[name] = "ok"
                except AssertionError as e:
                    result[name] = str(e)
            return result
        """),
    cod(f"{P}-m2-l4-e7", t("""
        Для проверки **пользовательских данных** `assert` не подходит (его можно отключить флагом `python -O`). Перепиши функцию из заготовки на `raise ValueError` с тем же текстом.
        """),
        """
        def set_quantity(q):
            assert q > 0, "количество должно быть положительным"
            return q
        """,
        """
        def test_values():
            assert set_quantity(3) == 3, "Корректное количество"
            try:
                set_quantity(0)
            except ValueError as e:
                assert str(e) == "количество должно быть положительным", f"Текст: {e}"
                return
            assert False, "Нужен ValueError"

        def test_no_assert():
            assert "assert " not in open("solution.py", encoding="utf-8").read(), "Замени assert на raise ValueError"
        """,
        """
        def set_quantity(q):
            if q <= 0:
                raise ValueError("количество должно быть положительным")
            return q
        """),
    cod(f"{P}-m2-l4-e8", t("""
        Напиши функцию `assert_raises(exc_type, func)` — проверить, что `func()` выбрасывает исключение указанного типа (как `pytest.raises`). Если выбросила — вернуть объект исключения; если не выбросила — `AssertionError("ожидали <ИмяТипа>")`. Исключения других типов пропускать наружу.
        """),
        """
        def assert_raises(exc_type, func):
            pass
        """,
        """
        def test_raises():
            e = assert_raises(ZeroDivisionError, lambda: 1 / 0)
            assert isinstance(e, ZeroDivisionError), "Должен вернуться объект исключения"

        def test_not_raises():
            try:
                assert_raises(ValueError, lambda: 1)
            except AssertionError as e:
                assert str(e) == "ожидали ValueError", f"Текст: {e}"
                return
            assert False, "Нужен AssertionError"

        def test_other():
            try:
                assert_raises(ValueError, lambda: [][0])
            except IndexError:
                return
            assert False, "Чужое исключение должно пройти наружу"
        """,
        """
        def assert_raises(exc_type, func):
            try:
                func()
            except exc_type as e:
                return e
            raise AssertionError(f"ожидали {exc_type.__name__}")
        """, xp=25),
),
)
