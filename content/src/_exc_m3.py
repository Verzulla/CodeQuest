"""Тема «Исключения», модуль 3 «Исключения на практике» — задания. Теория — в _exc_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "exc"

m3 = module(f"{P}-m3", "Исключения на практике", "🛡️", "EAFP и LBYL, ошибки в циклах, исключения в тестах, надёжная обработка",

lesson(f"{P}-m3-l1", "EAFP и LBYL: проверить или попробовать",
    out(f"{P}-m3-l1-e1", "Что выведет программа? Два стиля.", """
        data = {"a": 1}
        # LBYL: сначала проверить
        if "b" in data:
            print(data["b"])
        else:
            print("нет b (LBYL)")
        # EAFP: попробовать
        try:
            print(data["b"])
        except KeyError:
            print("нет b (EAFP)")
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа? Проверка не всё покрывает.", """
        for text in ["12", "-3", "4.5", " 7"]:
            print(repr(text), text.isdigit(), end=" | ")
            try:
                print(int(text))
            except ValueError:
                print("ValueError")
        """, hint="isdigit не пропускает минус и пробелы, а int их понимает."),
    out(f"{P}-m3-l1-e3", "Что выведет программа?", """
        config = {"timeout": "30"}
        print(config.get("retries", 3))
        try:
            print(int(config["timeout"]) * 2)
        except (KeyError, ValueError):
            print("по умолчанию")
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `get_int(data, key, default)` в стиле EAFP: `int(data[key])`, а при `KeyError`, `ValueError` или `TypeError` — `default`.
        """),
        """
        def get_int(data, key, default):
            pass
        """,
        """
        def test_values():
            d = {"a": "5", "b": "x", "c": None}
            assert [get_int(d, "a", 0), get_int(d, "b", 0), get_int(d, "c", 0), get_int(d, "z", -1)] == [5, 0, 0, -1], "Неверный результат"
        """,
        """
        def get_int(data, key, default):
            try:
                return int(data[key])
            except (KeyError, ValueError, TypeError):
                return default
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `is_number(text)` — можно ли превратить строку в `float` (включая `"-3"`, `"4.5"`, `" 7 "`, `"1e3"`). Проверки через `isdigit` тут не хватит — используй `try`.
        """),
        """
        def is_number(text):
            pass
        """,
        """
        def test_values():
            got = [is_number(x) for x in ["12", "-3", "4.5", " 7 ", "1e3", "abc", ""]]
            assert got == [True, True, True, True, True, False, False], f"Получено {got}"
        """,
        """
        def is_number(text):
            try:
                float(text)
                return True
            except ValueError:
                return False
        """),
    cod(f"{P}-m3-l1-e6", t("""
        Перепиши функцию из заготовки в стиле EAFP (без проверки `in`), сохранив поведение.
        """),
        """
        def price_of(prices, item):
            if item in prices:
                return prices[item]
            return 0
        """,
        """
        def test_values():
            assert price_of({"чай": 300}, "чай") == 300 and price_of({}, "x") == 0, "Неверный результат"

        def test_eafp():
            src = open("solution.py", encoding="utf-8").read()
            assert "try:" in src and " in prices" not in src, "Используй try/except KeyError"
        """,
        """
        def price_of(prices, item):
            try:
                return prices[item]
            except KeyError:
                return 0
        """),
    cod(f"{P}-m3-l1-e7", t("""
        Напиши функцию `nested_get(data, *keys, default=None)` — пройти по вложенным словарям по ключам; если на любом шаге ключа нет или значение не словарь — `default`. Используй EAFP.

        ```
        nested_get({"a": {"b": 1}}, "a", "b")         # → 1
        nested_get({"a": 1}, "a", "b", default=0)     # → 0
        ```
        """),
        """
        def nested_get(data, *keys, default=None):
            pass
        """,
        """
        def test_values():
            d = {"a": {"b": 1}, "x": 5}
            assert [nested_get(d, "a", "b"), nested_get(d, "x", "y", default=0), nested_get(d, "q"), nested_get(d)] == [1, 0, None, d], "Неверный результат"
        """,
        """
        def nested_get(data, *keys, default=None):
            try:
                for key in keys:
                    data = data[key]
                return data
            except (KeyError, TypeError):
                return default
        """),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `first_int(items)` — первое значение из списка, которое удаётся превратить в `int`, или `None`.
        """),
        """
        def first_int(items):
            pass
        """,
        """
        def test_values():
            assert [first_int(["x", None, " 42", "7"]), first_int(["a"]), first_int([])] == [42, None, None], "Неверный результат"
        """,
        """
        def first_int(items):
            for item in items:
                try:
                    return int(item)
                except (ValueError, TypeError):
                    continue
            return None
        """),
),

lesson(f"{P}-m3-l2", "Ошибки в циклах: пропустить, собрать, повторить",
    out(f"{P}-m3-l2-e1", "Что выведет программа? Пропуск плохих данных.", """
        total = 0
        errors = 0
        for raw in ["10", "x", "5", "", "7"]:
            try:
                total += int(raw)
            except ValueError:
                errors += 1
                continue
        print(total, errors)
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа? Сбор ошибок.", """
        rows = ["1,2", "3", "a,4"]
        good, bad = [], []
        for i, row in enumerate(rows):
            try:
                a, b = row.split(",")
                good.append(int(a) + int(b))
            except ValueError as e:
                bad.append(i)
        print(good, bad)
        """, hint="Распаковка неверного числа частей — тоже ValueError."),
    out(f"{P}-m3-l2-e3", "Что выведет программа? Повторы.", """
        answers = iter([ConnectionError("нет"), ConnectionError("нет"), "ok"])

        def request():
            value = next(answers)
            if isinstance(value, Exception):
                raise value
            return value

        for attempt in range(1, 5):
            try:
                print(attempt, request())
                break
            except ConnectionError as e:
                print(attempt, "ошибка:", e)
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши функцию `sum_valid(items)` — сумма значений, которые удаётся превратить в `int`; остальные пропустить. Вернуть пару `(сумма, количество_ошибок)`.
        """),
        """
        def sum_valid(items):
            pass
        """,
        """
        def test_values():
            assert [sum_valid(["10", "x", "5", None]), sum_valid([])] == [(15, 2), (0, 0)], "Неверный результат"
        """,
        """
        def sum_valid(items):
            total, errors = 0, 0
            for item in items:
                try:
                    total += int(item)
                except (ValueError, TypeError):
                    errors += 1
            return total, errors
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `parse_rows(rows)` — строки `"имя,возраст"` превратить в словари `{"name": ..., "age": int}`. Плохие строки не прерывают обработку: вернуть пару `(корректные_записи, номера_плохих_строк)` (нумерация с 1).
        """),
        """
        def parse_rows(rows):
            pass
        """,
        """
        def test_values():
            good, bad = parse_rows(["Аня,25", "Боря", "Вика,x", "Гоша,40"])
            assert good == [{"name": "Аня", "age": 25}, {"name": "Гоша", "age": 40}] and bad == [2, 3], f"{good} / {bad}"
        """,
        """
        def parse_rows(rows):
            good, bad = [], []
            for i, row in enumerate(rows, start=1):
                try:
                    name, age = row.split(",")
                    good.append({"name": name, "age": int(age)})
                except ValueError:
                    bad.append(i)
            return good, bad
        """, xp=20),
    cod(f"{P}-m3-l2-e6", t("""
        Напиши функцию `retry(func, attempts)` — вызывать `func()`, пока не пройдёт без `ConnectionError`, но не больше `attempts` раз. Вернуть результат; если все попытки упали — выбросить **последнюю** ошибку дальше.
        """),
        """
        def retry(func, attempts):
            pass
        """,
        """
        def make(fails):
            calls = []
            def func():
                calls.append(1)
                if len(calls) <= fails:
                    raise ConnectionError(f"сбой {len(calls)}")
                return "ok"
            return func, calls

        def test_success():
            func, calls = make(2)
            assert retry(func, 5) == "ok" and len(calls) == 3, "Успех с третьей попытки"

        def test_fail():
            func, calls = make(10)
            try:
                retry(func, 3)
            except ConnectionError as e:
                assert str(e) == "сбой 3" and len(calls) == 3, f"{e} / {len(calls)}"
                return
            assert False, "Нужна последняя ConnectionError"
        """,
        """
        def retry(func, attempts):
            for attempt in range(attempts):
                try:
                    return func()
                except ConnectionError:
                    if attempt == attempts - 1:
                        raise
        """, hint="На последней попытке — raise без аргументов.", xp=25),
    cod(f"{P}-m3-l2-e7", t("""
        Напиши функцию `run_all(tests)` — `tests` это словарь «название → функция». Выполнить все, даже если некоторые падают. Вернуть словарь «название → `"pass"` / `"fail"` (AssertionError) / `"error"` (любое другое исключение)».
        """),
        """
        def run_all(tests):
            pass
        """,
        """
        def test_values():
            def ok():
                assert True
            def bad():
                assert False
            def broken():
                return 1 / 0
            assert run_all({"ok": ok, "bad": bad, "broken": broken}) == {"ok": "pass", "bad": "fail", "broken": "error"}, "Неверный результат"
        """,
        """
        def run_all(tests):
            results = {}
            for name, test in tests.items():
                try:
                    test()
                    results[name] = "pass"
                except AssertionError:
                    results[name] = "fail"
                except Exception:
                    results[name] = "error"
            return results
        """, xp=20),
    cod(f"{P}-m3-l2-e8", t("""
        Напиши функцию `stop_on_critical(events)` — обработать события по очереди: строки `"ok"` считать, `"warn"` — пропускать, а на `"critical"` — **остановиться**, выбросив `RuntimeError("critical на шаге <номер с 1>")`. Если критических нет — вернуть количество `"ok"`.
        """),
        """
        def stop_on_critical(events):
            pass
        """,
        """
        def test_values():
            assert stop_on_critical(["ok", "warn", "ok"]) == 2, "Критических нет"
            try:
                stop_on_critical(["ok", "critical", "ok"])
            except RuntimeError as e:
                assert str(e) == "critical на шаге 2", f"Текст: {e}"
                return
            assert False, "Нужен RuntimeError"
        """,
        """
        def stop_on_critical(events):
            count = 0
            for i, event in enumerate(events, start=1):
                if event == "critical":
                    raise RuntimeError(f"critical на шаге {i}")
                if event == "ok":
                    count += 1
            return count
        """),
),

lesson(f"{P}-m3-l3", "Исключения и тесты",
    out(f"{P}-m3-l3-e1", "Что выведет программа? Проверяем, что ошибка есть.", """
        def check_raises(exc_type, func):
            try:
                func()
            except exc_type:
                return "ok: ошибка есть"
            return "плохо: ошибки нет"

        print(check_raises(ValueError, lambda: int("x")))
        print(check_raises(ValueError, lambda: int("5")))
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа? Проверяем текст ошибки.", """
        def withdraw(balance, amount):
            if amount > balance:
                raise ValueError(f"недостаточно средств: {balance} < {amount}")
            return balance - amount

        try:
            withdraw(100, 500)
        except ValueError as e:
            print("недостаточно" in str(e), e.args[0])
        """),
    out(f"{P}-m3-l3-e3", "Что выведет программа? Тест, который ловит слишком много.", """
        def buggy():
            return [][0]

        def test_bad():
            try:
                buggy()
            except Exception:
                return "тест прошёл?!"

        def test_good():
            try:
                buggy()
            except ValueError:
                return "ожидаемая ошибка"
            except Exception as e:
                return f"неожиданная {type(e).__name__}"

        print(test_bad(), "|", test_good())
        """, hint="Слишком широкий except прячет настоящий баг."),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши тест-функцию `test_parse_port()` для готовой `parse_port` из заготовки: проверь, что `"8080"` → `8080`, а для `"x"` и `"99999"` выбрасывается `ValueError` (используй `try/except` и `assert False`, если ошибки не было). Тест ничего не возвращает и молчит, если всё хорошо.
        """),
        """
        def parse_port(text):
            if not text.isdigit():
                raise ValueError("не число")
            port = int(text)
            if not 1 <= port <= 65535:
                raise ValueError("вне диапазона")
            return port

        def test_parse_port():
            pass
        """,
        """
        def test_runs():
            test_parse_port()

        def test_catches_bug():
            g = test_parse_port.__globals__
            original = g["parse_port"]
            g["parse_port"] = lambda text: int(text)
            try:
                test_parse_port()
            except (AssertionError, ValueError):
                return
            finally:
                g["parse_port"] = original
            assert False, "Тест должен падать на сломанной parse_port (без проверки диапазона)"
        """,
        """
        def parse_port(text):
            if not text.isdigit():
                raise ValueError("не число")
            port = int(text)
            if not 1 <= port <= 65535:
                raise ValueError("вне диапазона")
            return port

        def test_parse_port():
            assert parse_port("8080") == 8080
            for bad in ["x", "99999"]:
                try:
                    parse_port(bad)
                except ValueError:
                    continue
                assert False, f"для {bad!r} нет ValueError"
        """, xp=25),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `raises_with(exc_type, text, func)` — `True`, если `func()` выбросила исключение нужного типа и в его тексте есть подстрока `text`; `False` — если ошибки не было, тип другой или текст не совпал.
        """),
        """
        def raises_with(exc_type, text, func):
            pass
        """,
        """
        def test_values():
            got = [
                raises_with(ValueError, "base 10", lambda: int("x")),
                raises_with(ValueError, "другое", lambda: int("x")),
                raises_with(KeyError, "x", lambda: int("x")),
                raises_with(ValueError, "x", lambda: 1),
            ]
            assert got == [True, False, False, False], f"Получено {got}"
        """,
        """
        def raises_with(exc_type, text, func):
            try:
                func()
            except exc_type as e:
                return text in str(e)
            except Exception:
                return False
            return False
        """),
    cod(f"{P}-m3-l3-e6", t("""
        Напиши функцию `error_report(func, cases)` — вызвать `func` с каждым аргументом из списка `cases` и вернуть список строк: `"<аргумент!r>: ok <результат!r>"` или `"<аргумент!r>: <ИмяОшибки>"`.

        ```
        error_report(int, ["5", "x"])   # → ["'5': ok 5", "'x': ValueError"]
        ```
        """),
        """
        def error_report(func, cases):
            pass
        """,
        """
        def test_values():
            assert error_report(int, ["5", "x", None]) == ["'5': ok 5", "'x': ValueError", "None: TypeError"], "Неверный отчёт"
        """,
        """
        def error_report(func, cases):
            lines = []
            for case in cases:
                try:
                    result = func(case)
                    lines.append(f"{case!r}: ok {result!r}")
                except Exception as e:
                    lines.append(f"{case!r}: {type(e).__name__}")
            return lines
        """),
    cod(f"{P}-m3-l3-e7", t("""
        Тест в заготовке «зелёный» даже для сломанной функции: он ловит **любое** исключение. Исправь `test_divide`, чтобы он ожидал именно `ZeroDivisionError` и падал (`AssertionError`), если функция выбрасывает что-то другое или ничего.
        """),
        """
        def divide(a, b):
            return a / b

        def test_divide():
            try:
                divide(1, 0)
            except Exception:
                pass
        """,
        """
        def test_ok():
            test_divide()

        def test_strict():
            g = test_divide.__globals__
            original = g["divide"]
            g["divide"] = lambda a, b: [][0]
            try:
                test_divide()
            except (AssertionError, IndexError):
                return
            finally:
                g["divide"] = original
            assert False, "Тест должен падать, если выброшено не ZeroDivisionError"
        """,
        """
        def divide(a, b):
            return a / b

        def test_divide():
            try:
                divide(1, 0)
            except ZeroDivisionError:
                return
            assert False, "ожидали ZeroDivisionError"
        """),
    cod(f"{P}-m3-l3-e8", t("""
        Напиши функцию `expect(exc_type, func, *args)` — вызвать `func(*args)`. Если выброшено исключение типа `exc_type` — вернуть его **текст**; если ничего не выброшено — `AssertionError("не было исключения")`; если выброшено другое — `AssertionError("ожидали <Тип>, получили <Тип>")`.
        """),
        """
        def expect(exc_type, func, *args):
            pass
        """,
        """
        def test_values():
            assert expect(ValueError, int, "x") == "invalid literal for int() with base 10: 'x'", "Текст ошибки"
            for args, msg in [((ValueError, int, "5"), "не было исключения"), ((KeyError, int, "x"), "ожидали KeyError, получили ValueError")]:
                try:
                    expect(*args)
                except AssertionError as e:
                    assert str(e) == msg, f"Текст: {e}"
                    continue
                assert False, "Нужен AssertionError"
        """,
        """
        def expect(exc_type, func, *args):
            try:
                func(*args)
            except exc_type as e:
                return str(e)
            except Exception as e:
                raise AssertionError(f"ожидали {exc_type.__name__}, получили {type(e).__name__}")
            raise AssertionError("не было исключения")
        """, xp=25),
),

lesson(f"{P}-m3-l4", "Практика: надёжная обработка данных",
    out(f"{P}-m3-l4-e1", "Что выведет программа?", """
        import json
        bodies = ['{"id": 1}', "<html>", "", '{"id": "2"}']
        for body in bodies:
            try:
                data = json.loads(body)
                print("id =", int(data["id"]))
            except json.JSONDecodeError:
                print("не JSON")
        """),
    out(f"{P}-m3-l4-e2", "Что выведет программа?", """
        def load_user(raw):
            try:
                name, age = raw.split(":")
                age = int(age)
            except ValueError:
                return None
            if age < 0:
                raise ValueError("возраст < 0")
            return name, age

        for raw in ["Аня:25", "плохо", "Боря:-1"]:
            try:
                print(load_user(raw))
            except ValueError as e:
                print("ошибка данных:", e)
        """),
    out(f"{P}-m3-l4-e3", "Что выведет программа? Сводка ошибок.", """
        from collections import Counter
        errors = Counter()
        for value in ["1", "x", None, "2", [], "y"]:
            try:
                int(value)
            except Exception as e:
                errors[type(e).__name__] += 1
        print(dict(errors))
        """),
    cod(f"{P}-m3-l4-e4", t("""
        Напиши функцию `parse_body(text)` — разобрать JSON-тело ответа и вернуть поле `"id"` как `int`. Любая проблема (не JSON, нет поля, не число, корень не объект) — вернуть `None`.
        """),
        """
        import json

        def parse_body(text):
            pass
        """,
        """
        def test_values():
            got = [parse_body('{"id": 1}'), parse_body('{"id": "2"}'), parse_body("<html>"), parse_body('{"x": 1}'), parse_body('{"id": "a"}'), parse_body("[1]")]
            assert got == [1, 2, None, None, None, None], f"Получено {got}"
        """,
        """
        import json

        def parse_body(text):
            try:
                return int(json.loads(text)["id"])
            except (json.JSONDecodeError, KeyError, ValueError, TypeError):
                return None
        """),
    cod(f"{P}-m3-l4-e5", t("""
        Напиши функцию `error_stats(values)` — попытаться превратить каждое значение в `int`; вернуть словарь «имя типа ошибки → количество».
        """),
        """
        def error_stats(values):
            pass
        """,
        """
        def test_values():
            assert error_stats(["1", "x", None, "2", [], "y"]) == {"ValueError": 2, "TypeError": 2} and error_stats(["1"]) == {}, "Неверная сводка"
        """,
        """
        def error_stats(values):
            stats = {}
            for v in values:
                try:
                    int(v)
                except Exception as e:
                    name = type(e).__name__
                    stats[name] = stats.get(name, 0) + 1
            return stats
        """),
    cod(f"{P}-m3-l4-e6", t("""
        Напиши функцию `import_users(rows)` — строки `"имя;email;возраст"`. Для каждой строки: корректная → словарь `{"name", "email", "age"}`; некорректная (не 3 части, возраст не число, в email нет `@`) → запись в список ошибок `"строка <N>: <описание>"` (N с 1). Вернуть `(users, errors)`. Описания: `"неверный формат"`, `"возраст не число"`, `"нет @ в email"`.
        """),
        """
        def import_users(rows):
            pass
        """,
        """
        def test_values():
            users, errors = import_users(["Аня;a@x.ru;25", "плохо", "Боря;b@x.ru;x", "Вика;vika;30"])
            assert users == [{"name": "Аня", "email": "a@x.ru", "age": 25}], f"users = {users}"
            assert errors == ["строка 2: неверный формат", "строка 3: возраст не число", "строка 4: нет @ в email"], f"errors = {errors}"
        """,
        """
        def import_users(rows):
            users, errors = [], []
            for i, row in enumerate(rows, start=1):
                parts = row.split(";")
                if len(parts) != 3:
                    errors.append(f"строка {i}: неверный формат")
                    continue
                name, email, age = parts
                try:
                    age = int(age)
                except ValueError:
                    errors.append(f"строка {i}: возраст не число")
                    continue
                if "@" not in email:
                    errors.append(f"строка {i}: нет @ в email")
                    continue
                users.append({"name": name, "email": email, "age": age})
            return users, errors
        """, xp=25),
    cod(f"{P}-m3-l4-e7", t("""
        Напиши функцию `safe_pipeline(value, steps)` — применить к значению функции из списка `steps` по очереди. Если какой-то шаг упал, вернуть `("error", <номер шага с 1>, <имя ошибки>)`; если всё прошло — `("ok", результат)`.
        """),
        """
        def safe_pipeline(value, steps):
            pass
        """,
        """
        def test_values():
            assert safe_pipeline(" 5 ", [str.strip, int, lambda x: x * 2]) == ("ok", 10), "Успешный конвейер"
            assert safe_pipeline("x", [str.strip, int, lambda x: x * 2]) == ("error", 2, "ValueError"), "Ошибка на шаге 2"
        """,
        """
        def safe_pipeline(value, steps):
            for i, step in enumerate(steps, start=1):
                try:
                    value = step(value)
                except Exception as e:
                    return ("error", i, type(e).__name__)
            return ("ok", value)
        """),
    cod(f"{P}-m3-l4-e8", t("""
        Напиши функцию `load_settings(raw)` — словарь строк-настроек превратить в типизированный: `timeout` → `int` (по умолчанию 30), `debug` → `bool` из `"true"`/`"false"` (по умолчанию `False`). Неверное значение — выбросить `ValueError(f"плохое значение {ключ}: {значение!r}")` с причиной (`from`), если она есть.
        """),
        """
        def load_settings(raw):
            pass
        """,
        """
        def test_ok():
            assert load_settings({}) == {"timeout": 30, "debug": False}, "Умолчания"
            assert load_settings({"timeout": "5", "debug": "true"}) == {"timeout": 5, "debug": True}, "Значения"

        def test_errors():
            for raw, msg in [({"timeout": "x"}, "плохое значение timeout: 'x'"), ({"debug": "yes"}, "плохое значение debug: 'yes'")]:
                try:
                    load_settings(raw)
                except ValueError as e:
                    assert str(e) == msg, f"Текст: {e}"
                    continue
                assert False, "Нужен ValueError"
        """,
        """
        def load_settings(raw):
            try:
                timeout = int(raw.get("timeout", "30"))
            except ValueError as e:
                raise ValueError(f"плохое значение timeout: {raw['timeout']!r}") from e
            debug_raw = raw.get("debug", "false")
            if debug_raw not in ("true", "false"):
                raise ValueError(f"плохое значение debug: {debug_raw!r}")
            return {"timeout": timeout, "debug": debug_raw == "true"}
        """, xp=25),
),
)
