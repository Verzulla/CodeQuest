"""Тема «Исключения», модуль 1 «Ошибки и их перехват» — задания. Теория — в _exc_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "exc"

m1 = module(f"{P}-m1", "Ошибки и их перехват", "🧯", "Типы ошибок, try/except, else и finally, иерархия исключений",

lesson(f"{P}-m1-l1", "Что такое исключение",
    out(f"{P}-m1-l1-e1", "Что выведет программа? Какие ошибки возникают.", """
        checks = [
            lambda: int("abc"),
            lambda: 1 / 0,
            lambda: [1, 2][5],
            lambda: {"a": 1}["b"],
            lambda: "5" + 5,
        ]
        for check in checks:
            try:
                check()
            except Exception as e:
                print(type(e).__name__)
        """, hint="type(e).__name__ — имя класса ошибки."),
    out(f"{P}-m1-l1-e2", "Что выведет программа? Ошибка останавливает выполнение.", """
        def risky():
            print("до ошибки")
            x = 1 / 0
            print("после ошибки")

        try:
            risky()
        except ZeroDivisionError:
            print("поймали")
        print("программа продолжается")
        """),
    out(f"{P}-m1-l1-e3", "Что выведет программа? Текст ошибки.", """
        for text in ["12", "x"]:
            try:
                print(int(text))
            except ValueError as e:
                print("ошибка:", e)
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `error_name(func)` — вызвать функцию без аргументов и вернуть **имя типа** исключения, которое она выбросила, или `"нет ошибки"`.

        ```
        error_name(lambda: 1 / 0)      # → "ZeroDivisionError"
        error_name(lambda: 42)         # → "нет ошибки"
        ```
        """),
        """
        def error_name(func):
            pass
        """,
        """
        def test_values():
            got = [error_name(lambda: 1 / 0), error_name(lambda: 42), error_name(lambda: [][0]), error_name(lambda: int("x"))]
            assert got == ["ZeroDivisionError", "нет ошибки", "IndexError", "ValueError"], f"Получено {got}"
        """,
        """
        def error_name(func):
            try:
                func()
            except Exception as e:
                return type(e).__name__
            return "нет ошибки"
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `safe_int(text)` — `int(text)` или `None`, если строка не является числом.
        """),
        """
        def safe_int(text):
            pass
        """,
        """
        def test_values():
            assert [safe_int("42"), safe_int(" -7 "), safe_int("x"), safe_int("")] == [42, -7, None, None], "Неверный результат"
        """,
        """
        def safe_int(text):
            try:
                return int(text)
            except ValueError:
                return None
        """),
    cod(f"{P}-m1-l1-e6", t("""
        Напиши функцию `safe_div(a, b)` — `a / b`, а при делении на ноль — `None`.
        """),
        """
        def safe_div(a, b):
            pass
        """,
        """
        def test_values():
            assert [safe_div(6, 3), safe_div(1, 0)] == [2.0, None], "Неверный результат"
        """,
        """
        def safe_div(a, b):
            try:
                return a / b
            except ZeroDivisionError:
                return None
        """),
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `get_item(items, index)` — элемент списка по индексу или `None`, если индекса нет. Лови `IndexError`.
        """),
        """
        def get_item(items, index):
            pass
        """,
        """
        def test_values():
            assert [get_item([1, 2], 1), get_item([1, 2], 5), get_item([], 0), get_item([1, 2], -1)] == [2, None, None, 2], "Неверный результат"
        """,
        """
        def get_item(items, index):
            try:
                return items[index]
            except IndexError:
                return None
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `error_message(func)` — вызвать функцию; при ошибке вернуть строку `"<Тип>: <текст>"`, иначе `"ok"`.

        ```
        error_message(lambda: int("x"))
        # → "ValueError: invalid literal for int() with base 10: 'x'"
        ```
        """),
        """
        def error_message(func):
            pass
        """,
        """
        def test_values():
            assert error_message(lambda: int("x")) == "ValueError: invalid literal for int() with base 10: 'x'", "Неверное сообщение"
            assert error_message(lambda: 1) == "ok" and error_message(lambda: {}["k"]) == "KeyError: 'k'", "Неверный результат"
        """,
        """
        def error_message(func):
            try:
                func()
            except Exception as e:
                return f"{type(e).__name__}: {e}"
            return "ok"
        """),
),

lesson(f"{P}-m1-l2", "try/except подробно",
    out(f"{P}-m1-l2-e1", "Что выведет программа? Несколько except.", """
        def parse(text):
            try:
                return 100 / int(text)
            except ValueError:
                return "не число"
            except ZeroDivisionError:
                return "деление на ноль"

        print(parse("4"), parse("x"), parse("0"))
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа? Кортеж исключений.", """
        def lookup(data, key):
            try:
                return data[key]
            except (KeyError, IndexError, TypeError) as e:
                return f"не найдено ({type(e).__name__})"

        print(lookup({"a": 1}, "b"), lookup([1], 3), lookup(None, 0))
        """),
    out(f"{P}-m1-l2-e3", "Что выведет программа? Неперехваченное летит дальше.", """
        def inner():
            try:
                return [][0]
            except KeyError:
                return "KeyError"

        try:
            inner()
        except IndexError:
            print("IndexError поймали снаружи")
        """, hint="except ловит только указанные типы; остальные идут выше по вызовам."),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `parse_percent(text)` — строку превратить в число и вернуть `100 / число`. Ошибки:

        - не число → `"не число"`;
        - ноль → `"деление на ноль"`.
        """),
        """
        def parse_percent(text):
            pass
        """,
        """
        def test_values():
            assert [parse_percent("4"), parse_percent("x"), parse_percent("0")] == [25.0, "не число", "деление на ноль"], "Неверный результат"
        """,
        """
        def parse_percent(text):
            try:
                return 100 / int(text)
            except ValueError:
                return "не число"
            except ZeroDivisionError:
                return "деление на ноль"
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `safe_get(data, key)` — `data[key]` для словаря или списка; при `KeyError`, `IndexError` или `TypeError` — `None`. Перехватывай их одним `except` с кортежем.
        """),
        """
        def safe_get(data, key):
            pass
        """,
        """
        def test_values():
            assert [safe_get({"a": 1}, "a"), safe_get({"a": 1}, "b"), safe_get([1], 3), safe_get(None, 0), safe_get([1], "x")] == [1, None, None, None, None], "Неверный результат"

        def test_tuple():
            assert "except (" in open("solution.py", encoding="utf-8").read(), "Используй except с кортежем"
        """,
        """
        def safe_get(data, key):
            try:
                return data[key]
            except (KeyError, IndexError, TypeError):
                return None
        """),
    cod(f"{P}-m1-l2-e6", t("""
        Напиши функцию `to_float(value)` — привести значение к `float`; при `ValueError` (строка не число) или `TypeError` (например, `None`) — вернуть `0.0`.
        """),
        """
        def to_float(value):
            pass
        """,
        """
        def test_values():
            assert [to_float("2.5"), to_float(3), to_float("x"), to_float(None)] == [2.5, 3.0, 0.0, 0.0], "Неверный результат"
        """,
        """
        def to_float(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0
        """),
    cod(f"{P}-m1-l2-e7", t("""
        Напиши функцию `read_config(config, key)` — вернуть `int(config[key])`. Если ключа нет — `"нет ключа <key>"`; если значение не число — `"плохое значение <key>"`.
        """),
        """
        def read_config(config, key):
            pass
        """,
        """
        def test_values():
            cfg = {"port": "8080", "host": "x"}
            assert [read_config(cfg, "port"), read_config(cfg, "timeout"), read_config(cfg, "host")] == [8080, "нет ключа timeout", "плохое значение host"], "Неверный результат"
        """,
        """
        def read_config(config, key):
            try:
                return int(config[key])
            except KeyError:
                return f"нет ключа {key}"
            except ValueError:
                return f"плохое значение {key}"
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши функцию `first_error(funcs)` — вызывать функции списка по очереди; вернуть **имя типа** первой возникшей ошибки или `None`, если ошибок не было.
        """),
        """
        def first_error(funcs):
            pass
        """,
        """
        def test_values():
            assert first_error([lambda: 1, lambda: [][1], lambda: 1 / 0]) == "IndexError" and first_error([lambda: 1]) is None, "Неверный результат"
        """,
        """
        def first_error(funcs):
            for f in funcs:
                try:
                    f()
                except Exception as e:
                    return type(e).__name__
            return None
        """),
),

lesson(f"{P}-m1-l3", "else и finally",
    out(f"{P}-m1-l3-e1", "Что выведет программа? Порядок блоков.", """
        def run(text):
            try:
                n = int(text)
            except ValueError:
                print("except")
            else:
                print("else", n)
            finally:
                print("finally")

        run("5")
        run("x")
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа? finally и return.", """
        def f():
            try:
                return "из try"
            finally:
                print("finally выполнился")

        print(f())
        """, hint="finally выполняется даже при return."),
    out(f"{P}-m1-l3-e3", "Что выведет программа? finally при неперехваченной ошибке.", """
        def g():
            try:
                raise KeyError("x")
            finally:
                print("уборка")

        try:
            g()
        except KeyError:
            print("ошибка дошла наружу")
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `parse_and_double(text)` с `try/except/else`: в `try` — только превращение в число; в `except ValueError` — вернуть `None`; в `else` — вернуть удвоенное число.
        """),
        """
        def parse_and_double(text):
            pass
        """,
        """
        def test_values():
            assert [parse_and_double("4"), parse_and_double("x")] == [8, None], "Неверный результат"

        def test_else():
            assert "else:" in open("solution.py", encoding="utf-8").read(), "Используй блок else"
        """,
        """
        def parse_and_double(text):
            try:
                n = int(text)
            except ValueError:
                return None
            else:
                return n * 2
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `with_log(func, log)` — вызвать `func()` и вернуть результат (или `None` при любой ошибке). В любом случае в список `log` добавить `"done"` (используй `finally`).
        """),
        """
        def with_log(func, log):
            pass
        """,
        """
        def test_values():
            log = []
            assert with_log(lambda: 5, log) == 5 and with_log(lambda: 1 / 0, log) is None and log == ["done", "done"], f"log = {log}"

        def test_finally():
            assert "finally:" in open("solution.py", encoding="utf-8").read(), "Используй finally"
        """,
        """
        def with_log(func, log):
            try:
                return func()
            except Exception:
                return None
            finally:
                log.append("done")
        """),
    cod(f"{P}-m1-l3-e6", t("""
        Напиши функцию `use_resource(resource, action)` — `resource` это словарь `{"open": False}`. Функция «открывает» ресурс (`resource["open"] = True`), вызывает `action()`, а потом **обязательно** «закрывает» (`False`) — даже если `action` упала. Ошибку не перехватывать.
        """),
        """
        def use_resource(resource, action):
            pass
        """,
        """
        def test_ok():
            r = {"open": False}
            assert use_resource(r, lambda: 42) == 42 and r["open"] is False, "Ресурс должен закрыться"

        def test_error():
            r = {"open": False}
            try:
                use_resource(r, lambda: 1 / 0)
            except ZeroDivisionError:
                assert r["open"] is False, "Ресурс должен закрыться даже при ошибке"
                return
            assert False, "Ошибка должна пройти наружу"
        """,
        """
        def use_resource(resource, action):
            resource["open"] = True
            try:
                return action()
            finally:
                resource["open"] = False
        """, hint="try/finally без except: уборка выполнится, а ошибка полетит дальше.", xp=20),
    cod(f"{P}-m1-l3-e7", t("""
        Напиши функцию `steps(text)` — вернуть список этапов, через которые прошла обработка: всегда `"try"`, затем `"except"` (если `int(text)` упал) или `"else"`, и всегда `"finally"`.

        ```
        steps("5")   # → ["try", "else", "finally"]
        steps("x")   # → ["try", "except", "finally"]
        ```
        """),
        """
        def steps(text):
            pass
        """,
        """
        def test_values():
            assert steps("5") == ["try", "else", "finally"] and steps("x") == ["try", "except", "finally"], "Неверный порядок"
        """,
        """
        def steps(text):
            log = []
            try:
                log.append("try")
                int(text)
            except ValueError:
                log.append("except")
            else:
                log.append("else")
            finally:
                log.append("finally")
            return log
        """),
    cod(f"{P}-m1-l3-e8", t("""
        Напиши функцию `average_or_none(nums)` — среднее; для пустого списка деление на ноль даёт `ZeroDivisionError` — тогда `None`. Используй `try/except/else`: в `else` — округление до 2 знаков.
        """),
        """
        def average_or_none(nums):
            pass
        """,
        """
        def test_values():
            assert [average_or_none([1, 2, 2]), average_or_none([])] == [1.67, None], "Неверный результат"
        """,
        """
        def average_or_none(nums):
            try:
                avg = sum(nums) / len(nums)
            except ZeroDivisionError:
                return None
            else:
                return round(avg, 2)
        """),
),

lesson(f"{P}-m1-l4", "Иерархия исключений",
    out(f"{P}-m1-l4-e1", "Что выведет программа?", """
        print(issubclass(KeyError, LookupError), issubclass(IndexError, LookupError))
        print(issubclass(ZeroDivisionError, ArithmeticError), issubclass(ValueError, Exception))
        print(issubclass(KeyboardInterrupt, Exception))
        """, hint="KeyboardInterrupt наследует BaseException, а не Exception."),
    out(f"{P}-m1-l4-e2", "Что выведет программа? Базовый класс ловит потомков.", """
        for bad in [lambda: {}["x"], lambda: [][1]]:
            try:
                bad()
            except LookupError as e:
                print("LookupError поймал", type(e).__name__)
        """),
    out(f"{P}-m1-l4-e3", "Что выведет программа? Порядок except.", """
        try:
            {}["x"]
        except LookupError:
            print("сработал LookupError")
        except KeyError:
            print("сработал KeyError")
        """, hint="Срабатывает первый подходящий except — более общий перехватил раньше."),
    cod(f"{P}-m1-l4-e4", t("""
        Напиши функцию `lookup(data, key)` — `data[key]`; для отсутствующего ключа словаря **и** индекса списка вернуть `None`, перехватив **один** общий базовый класс `LookupError`.
        """),
        """
        def lookup(data, key):
            pass
        """,
        """
        def test_values():
            assert [lookup({"a": 1}, "a"), lookup({"a": 1}, "b"), lookup([1], 5)] == [1, None, None], "Неверный результат"

        def test_lookup_error():
            assert "LookupError" in open("solution.py", encoding="utf-8").read(), "Перехватывай LookupError"
        """,
        """
        def lookup(data, key):
            try:
                return data[key]
            except LookupError:
                return None
        """),
    cod(f"{P}-m1-l4-e5", t("""
        Напиши функцию `classify(func)` — вызвать функцию и вернуть:

        - `"lookup"` — для ошибок поиска (`LookupError` и потомки);
        - `"math"` — для арифметических (`ArithmeticError`);
        - `"other"` — для прочих `Exception`;
        - `"ok"` — если ошибки не было.

        Порядок `except` — от частного к общему.
        """),
        """
        def classify(func):
            pass
        """,
        """
        def test_values():
            got = [classify(lambda: {}["x"]), classify(lambda: 1 / 0), classify(lambda: int("x")), classify(lambda: 1)]
            assert got == ["lookup", "math", "other", "ok"], f"Получено {got}"
        """,
        """
        def classify(func):
            try:
                func()
            except LookupError:
                return "lookup"
            except ArithmeticError:
                return "math"
            except Exception:
                return "other"
            return "ok"
        """),
    cod(f"{P}-m1-l4-e6", t("""
        Исправь порядок `except` в заготовке: сейчас общий `Exception` стоит первым, и частный обработчик `KeyError` никогда не срабатывает.
        """),
        """
        def find(d, key):
            try:
                return d[key]
            except Exception:
                return "ошибка"
            except KeyError:
                return "нет ключа"
        """,
        """
        def test_values():
            assert find({"a": 1}, "b") == "нет ключа" and find(None, "x") == "ошибка" and find({"a": 1}, "a") == 1, "Неверный результат"
        """,
        """
        def find(d, key):
            try:
                return d[key]
            except KeyError:
                return "нет ключа"
            except Exception:
                return "ошибка"
        """),
    cod(f"{P}-m1-l4-e7", t("""
        Напиши функцию `ancestors(exc_type)` — список имён классов-предков исключения от него самого до `BaseException` включительно. Используй атрибут `__mro__` класса (порядок поиска методов) и остановись на `BaseException`.

        ```
        ancestors(KeyError)   # → ["KeyError", "LookupError", "Exception", "BaseException"]
        ```
        """),
        """
        def ancestors(exc_type):
            pass
        """,
        """
        def test_values():
            assert ancestors(KeyError) == ["KeyError", "LookupError", "Exception", "BaseException"], f"Получено {ancestors(KeyError)}"
            assert ancestors(ZeroDivisionError) == ["ZeroDivisionError", "ArithmeticError", "Exception", "BaseException"], "Неверная цепочка"
        """,
        """
        def ancestors(exc_type):
            result = []
            for cls in exc_type.__mro__:
                result.append(cls.__name__)
                if cls is BaseException:
                    break
            return result
        """, xp=20),
    cod(f"{P}-m1-l4-e8", t("""
        Напиши функцию `is_lookup_problem(exc)` — является ли **объект-исключение** ошибкой поиска (экземпляром `LookupError`). Используй `isinstance`.

        ```
        is_lookup_problem(KeyError("x"))     # → True
        is_lookup_problem(ValueError("x"))   # → False
        ```
        """),
        """
        def is_lookup_problem(exc):
            pass
        """,
        """
        def test_values():
            assert [is_lookup_problem(KeyError("x")), is_lookup_problem(IndexError()), is_lookup_problem(ValueError("x"))] == [True, True, False], "Неверный результат"
        """,
        """
        def is_lookup_problem(exc):
            return isinstance(exc, LookupError)
        """),
),
)
