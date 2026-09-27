"""Тема «Переменные и типы данных», модуль 2 «Типы данных» — задания.
Теория уроков — в _vars_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "var"

m2 = module(f"{P}-types", "Типы данных", "🧩", "int, float, str, bool, None и превращение одного типа в другой",

lesson(f"{P}-m1-l3", "Типы данных: str, int, float, bool, None",
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        print(type(42).__name__)
        print(type(3.0).__name__)
        print(type("3").__name__)
        print(type(True).__name__)
        print(type(None).__name__)
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа? Сравни число и строку.", """
        print(2024 == "2024")
        print(2 == 2.0)
        print(isinstance(True, int))
        """, hint="`bool` в Python — подтип `int`, поэтому `True` — это тоже целое число."),
    cod(f"{P}-m1-l3-e3", t("""
        Напиши функцию `type_name(value)`, которая возвращает **название типа** значения строкой.

        - Получает: любое значение.
        - Возвращает: `"int"`, `"float"`, `"str"`, `"bool"`, `"NoneType"` и т. д.

        Примеры:
        ```
        type_name(5)       # → "int"
        type_name("5")     # → "str"
        type_name(None)    # → "NoneType"
        ```
        Имя типа хранится в атрибуте `__name__`: `type(value).__name__`.
        """),
        """
        def type_name(value):
            pass
        """,
        """
        def test_values():
            got = [type_name(v) for v in (5, 5.0, "5", True, None)]
            assert got == ["int", "float", "str", "bool", "NoneType"], f"Получено {got}"
        """,
        """
        def type_name(value):
            return type(value).__name__
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `is_number(value)`, которая проверяет, является ли значение **числом**.

        - Возвращает `True` для `int` и `float`.
        - Возвращает `False` для строк, `None` и **для `True`/`False`** (логические значения числами считать не будем).

        Примеры:
        ```
        is_number(5)      # → True
        is_number(2.5)    # → True
        is_number("5")    # → False
        is_number(True)   # → False
        ```
        """),
        """
        def is_number(value):
            pass
        """,
        """
        def test_numbers():
            assert is_number(5) is True and is_number(2.5) is True and is_number(-1) is True, "int и float — числа"

        def test_not_numbers():
            assert is_number("5") is False and is_number(None) is False, "строка и None — не числа"

        def test_bool():
            assert is_number(True) is False and is_number(False) is False, "bool не считаем числом"
        """,
        """
        def is_number(value):
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        """,
        hint="`isinstance(value, (int, float))` проверяет сразу два типа. Но `True` тоже `int` — исключи `bool` отдельно.", xp=20),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `describe(value)`, которая возвращает строку вида `"<значение> — <тип>"`.

        Примеры:
        ```
        describe(42)       # → "42 — int"
        describe("hi")     # → "hi — str"
        describe(None)     # → "None — NoneType"
        ```
        Длинное тире `—` можно скопировать отсюда. Удобнее всего через f-строку.
        """),
        """
        def describe(value):
            pass
        """,
        """
        def test_describe():
            assert describe(42) == "42 — int", f"Получено {describe(42)!r}"
            assert describe("hi") == "hi — str", f"Получено {describe('hi')!r}"
            assert describe(None) == "None — NoneType", f"Получено {describe(None)!r}"
        """,
        """
        def describe(value):
            return f"{value} — {type(value).__name__}"
        """),
    out(f"{P}-m1-l3-e6", "Что выведет программа? Тип результата вычислений.", """
        print(type(7 / 7).__name__)
        print(type(7 * 1.0).__name__)
        print(type("7" * 2).__name__)
        """, hint="Деление `/` всегда даёт float; строка, умноженная на число, остаётся строкой."),
    out(f"{P}-m1-l3-e7", "Что выведет программа? `isinstance` с несколькими типами.", """
        print(isinstance(5, (int, float)))
        print(isinstance(2.5, (int, float)))
        print(isinstance("5", (int, float)))
        """),
    cod(f"{P}-m1-l3-e8", t("""
        Напиши функцию `same_type(a, b)`, которая возвращает `True`, если у двух значений **одинаковый тип**, иначе `False`.

        Примеры:
        ```
        same_type(1, 2)       # → True    оба int
        same_type(1, "1")     # → False   int и str
        same_type(1, 1.0)     # → False   int и float
        same_type(True, 1)    # → False   bool и int
        ```
        Сравни `type(a)` и `type(b)` через `==`.
        """),
        """
        def same_type(a, b):
            pass
        """,
        """
        def test_values():
            got = [same_type(1, 2), same_type(1, "1"), same_type(1, 1.0), same_type(True, 1), same_type("a", "")]
            assert got == [True, False, False, False, True], f"Получено {got}"
        """,
        """
        def same_type(a, b):
            return type(a) == type(b)
        """)),

lesson(f"{P}-bool", "bool и None",
    out(f"{P}-bool-e1", "Что выведет программа? Сравнения дают bool.", """
        print(5 > 3, 5 == 3, 5 != 3)
        print(type(5 > 3).__name__)
        """),
    out(f"{P}-bool-e2", "Что выведет программа? bool ведёт себя как число.", """
        print(True + True)
        print(True * 10)
        print(False + 1)
        """, hint="`True` — это 1, `False` — это 0."),
    out(f"{P}-bool-e3", "Что выведет программа? None — не ноль и не пустая строка.", """
        x = None
        print(x is None)
        print(x == 0)
        print(x is not None)
        """),
    cod(f"{P}-bool-e4", t("""
        Напиши функцию `is_adult(age)`, которая возвращает `True`, если `age` **18 или больше**, иначе `False`.

        Примеры:
        ```
        is_adult(30)   # → True
        is_adult(18)   # → True
        is_adult(10)   # → False
        ```
        Сравнение `>=` уже даёт `True` или `False` — его можно сразу вернуть.
        """),
        """
        def is_adult(age):
            pass
        """,
        """
        def test_values():
            got = [is_adult(30), is_adult(18), is_adult(17), is_adult(10)]
            assert got == [True, True, False, False], f"Получено {got}"
        """,
        """
        def is_adult(age):
            return age >= 18
        """,
        hint="`return age >= 18`"),
    cod(f"{P}-bool-e5", t("""
        Напиши функцию `is_missing(value)`, которая возвращает `True`, только если значение — `None`.
        Ноль, пустая строка и `False` — это **не** отсутствие значения.

        Примеры:
        ```
        is_missing(None)   # → True
        is_missing(0)      # → False
        is_missing("")     # → False
        is_missing(False)  # → False
        ```
        """),
        """
        def is_missing(value):
            pass
        """,
        """
        def test_values():
            got = [is_missing(None), is_missing(0), is_missing(""), is_missing(False), is_missing("None")]
            assert got == [True, False, False, False, False], f"Получено {got}"
        """,
        """
        def is_missing(value):
            return value is None
        """,
        hint="`value is None`"),
    cod(f"{P}-bool-e6", t("""
        Напиши функцию `count_true(a, b, c)`, которая получает три логических значения и возвращает, **сколько из них `True`**.

        Примеры:
        ```
        count_true(True, False, True)    # → 2
        count_true(False, False, False)  # → 0
        ```
        Пользуйся тем, что `True` ведёт себя как `1`, а `False` как `0`.
        """),
        """
        def count_true(a, b, c):
            pass
        """,
        """
        def test_values():
            got = [count_true(True, False, True), count_true(False, False, False), count_true(True, True, True)]
            assert got == [2, 0, 3], f"Получено {got}"
        """,
        """
        def count_true(a, b, c):
            return a + b + c
        """),
    cod(f"{P}-bool-e7", t("""
        Напиши функцию `same_value(a, b)`, которая возвращает `True`, если значения **равны**.

        Примеры:
        ```
        same_value(2, 2)      # → True
        same_value(1, 1.0)    # → True    числа равны по величине
        same_value(1, "1")    # → False   число и строка не равны
        ```
        """),
        """
        def same_value(a, b):
            pass
        """,
        """
        def test_values():
            got = [same_value(2, 2), same_value(1, 1.0), same_value(1, "1"), same_value("a", "A")]
            assert got == [True, True, False, False], f"Получено {got}"
        """,
        """
        def same_value(a, b):
            return a == b
        """),
    cod(f"{P}-bool-e8", t("""
        Функция `triple(n)` должна возвращать число, умноженное на 3, но сейчас возвращает `None`.
        Найди и исправь ошибку.

        Пример:
        ```
        triple(4)   # → 12
        ```
        """),
        """
        def triple(n):
            n * 3
        """,
        """
        def test_values():
            assert triple(4) == 12 and triple(0) == 0, f"triple(4) вернула {triple(4)!r}"
        """,
        """
        def triple(n):
            return n * 3
        """,
        hint="Выражение вычисляется, но результат никуда не возвращается. Нужен `return`.")),

lesson(f"{P}-m2-l3", "Преобразование типов",
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        print(int("42") + 1)
        print(int(3.99))
        print(float("2.5") * 2)
        print(str(10) + str(20))
        """),
    out(f"{P}-m2-l3-e6", "Что выведет программа? Истинность значений.", """
        print(bool(0), bool(0.0), bool(42))
        print(bool(""), bool("0"), bool(" "))
        print(bool(None))
        """, hint='Ложь — только ноль, пустая строка и None. Строка `"0"` не пустая.'),
    out(f"{P}-m2-l3-e7", "Что выведет программа?", """
        print(str(3.0))
        print(int("-7") * 2)
        print(float("1e2"))
        """),
    cod(f"{P}-m2-l3-e3", t("""
        Напиши функцию `sum_strings(a, b)`, которая получает **два числа в виде строк** и возвращает их сумму **числом**.

        Примеры:
        ```
        sum_strings("2", "3")      # → 5
        sum_strings("10", "-4")    # → 6
        ```
        """),
        """
        def sum_strings(a, b):
            pass
        """,
        """
        def test_sum():
            assert sum_strings("2", "3") == 5, f"Получено {sum_strings('2', '3')!r} — строки нужно превратить в числа"
            assert sum_strings("10", "-4") == 6, "10 + (-4) = 6"
        """,
        """
        def sum_strings(a, b):
            return int(a) + int(b)
        """),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `parse_price(text)`, которая превращает цену из строки вида `"1 299,50"` (пробел между разрядами, запятая вместо точки) в `float`.

        Примеры:
        ```
        parse_price("1 299,50")   # → 1299.5
        parse_price("99,90")      # → 99.9
        parse_price("15")         # → 15.0
        ```
        Используй `.replace()`: убери пробелы и замени запятую на точку, потом `float()`.
        """),
        """
        def parse_price(text):
            pass
        """,
        """
        def test_values():
            got = [parse_price(s) for s in ("1 299,50", "99,90", "15")]
            assert got == [1299.5, 99.9, 15.0], f"Получено {got}"
        """,
        """
        def parse_price(text):
            return float(text.replace(" ", "").replace(",", "."))
        """, xp=20),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `safe_int(text, default=0)`, которая превращает строку в целое число, а если это невозможно — возвращает `default`.

        Примеры:
        ```
        safe_int("42")         # → 42
        safe_int("abc")        # → 0
        safe_int("", -1)       # → -1
        safe_int(" 7 ")        # → 7    int сам игнорирует пробелы по краям
        ```
        Используй `try` / `except ValueError`.
        """),
        """
        def safe_int(text, default=0):
            pass
        """,
        """
        def test_ok():
            assert safe_int("42") == 42 and safe_int(" 7 ") == 7, "Числа должны преобразовываться"

        def test_bad():
            assert safe_int("abc") == 0 and safe_int("", -1) == -1 and safe_int("2.5") == 0, "Нечисловые строки → default"
        """,
        """
        def safe_int(text, default=0):
            try:
                return int(text)
            except ValueError:
                return default
        """,
        hint="```py\ntry:\n    return int(text)\nexcept ValueError:\n    return default\n```"),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `to_int(x)`, которая превращает в целое число и строку с дробным числом, и само дробное число.
        Дробная часть **отбрасывается** (не округляется).

        Примеры:
        ```
        to_int("2.9")   # → 2
        to_int("7")     # → 7
        to_int(3.7)     # → 3
        ```
        `int("2.9")` упадёт с ошибкой — сначала превратите строку во `float`.
        """),
        """
        def to_int(x):
            pass
        """,
        """
        def test_values():
            got = [to_int("2.9"), to_int("7"), to_int(3.7), to_int("-1.5")]
            assert got == [2, 7, 3, -1], f"Получено {got}"
        """,
        """
        def to_int(x):
            return int(float(x))
        """,
        hint="`int(float(x))`"),
    cod(f"{P}-m2-l3-e9", t("""
        Напиши функцию `label(name, n)`, которая склеивает текст и число через `+` и возвращает строку `"<name>: <n>"`.

        Примеры:
        ```
        label("Попыток", 3)    # → "Попыток: 3"
        label("Цена", 99.5)    # → "Цена: 99.5"
        ```
        Склеить строку с числом нельзя — число нужно превратить в строку.
        """),
        """
        def label(name, n):
            pass
        """,
        """
        def test_values():
            assert label("Попыток", 3) == "Попыток: 3", f"Получено {label('Попыток', 3)!r}"
            assert label("Цена", 99.5) == "Цена: 99.5", f"Получено {label('Цена', 99.5)!r}"
        """,
        """
        def label(name, n):
            return name + ": " + str(n)
        """,
        hint='`name + ": " + str(n)`')),
)
