"""Тема «Переменные и типы данных»."""
from ._lib import cod, lesson, module, out, t, topic

P = "var"

# ============================================================
m1 = module(f"{P}-m1", "Первые шаги", "🐣", "print, переменные и основные типы",

lesson(f"{P}-m1-l1", "Первая программа: print", 
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        print("Hello")
        print("Python")
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа? Обрати внимание на запятые.", """
        print("Мне", 20, "лет")
        print("2024", "09", "27", sep="-")
        """, hint="Через запятую — через пробел, а `sep` заменяет пробел на свой разделитель."),
    cod(f"{P}-m1-l1-e3", t("""
        Выведи на экран фразу `Hello, World!`.

        Текст должен совпасть **символ в символ**: заглавные `H` и `W`, запятая, пробел, восклицательный знак.

        Ожидаемый вывод:
        ```
        Hello, World!
        ```
        """),
        "",
        """
        def test_output():
            assert OUTPUT.strip() == "Hello, World!", f"Ожидалось 'Hello, World!', а напечатано {OUTPUT.strip()!r}"
        """,
        'print("Hello, World!")',
        hint="`print(\"...\")` — текст внутри кавычек."),
    cod(f"{P}-m1-l1-e4", t("""
        Выведи три слова, каждое на отдельной строке.

        Ожидаемый вывод:
        ```
        один
        два
        три
        ```
        """),
        "",
        """
        def test_words():
            assert OUTPUT.split() == ["один", "два", "три"], f"Напечатано: {OUTPUT.split()}"

        def test_lines():
            assert len(OUTPUT.strip().splitlines()) == 3, "Каждое слово — на своей строке"
        """,
        """
        print("один")
        print("два")
        print("три")
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Выведи время в формате `часы:минуты:секунды` **одним вызовом** `print`, передав три числа через запятую и задав разделитель `sep`.

        Числа: `12`, `30`, `45`. Ожидаемый вывод:
        ```
        12:30:45
        ```
        """),
        "",
        """
        import inspect

        def test_output():
            assert OUTPUT.strip() == "12:30:45", f"Напечатано {OUTPUT.strip()!r}"

        def test_one_print():
            src = open("solution.py", encoding="utf-8").read()
            assert src.count("print(") == 1 and "sep" in src, "Нужен один print с параметром sep"
        """,
        'print(12, 30, 45, sep=":")',
        hint="`print(a, b, c, sep=\":\")`")),

lesson(f"{P}-m1-l2", "Переменные", 
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        x = 5
        x = 10
        print(x)
        """, hint="Второе присваивание перезаписывает первое."),
    out(f"{P}-m1-l2-e2", "Что выведет программа?", """
        a = 3
        b = a
        a = 7
        print(a, b)
        """, hint="`b = a` копирует текущее значение `a`; дальнейшие изменения `a` на `b` не влияют."),
    cod(f"{P}-m1-l2-e3", t("""
        Создай две переменные:
        - `city` — строка `"Казань"`;
        - `year` — **число** `2024` (без кавычек).

        Печатать ничего не нужно — тесты сами прочитают переменные.
        """),
        "",
        """
        def test_city():
            assert city == "Казань", "city должна быть строкой 'Казань'"

        def test_year():
            assert year == 2024 and isinstance(year, int), "year должна быть числом 2024, без кавычек"
        """,
        """
        city = "Казань"
        year = 2024
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Поменяй местами значения переменных `a` и `b`.

        В заготовке `a = 10`, `b = 20`. Допиши код так, чтобы строка `print(a, b)` вывела:
        ```
        20 10
        ```
        Нельзя просто написать `a = 20` — код должен работать для любых значений.
        """),
        """
        a = 10
        b = 20
        # поменяй a и b местами

        print(a, b)
        """,
        """
        import re

        def test_swapped():
            assert (a, b) == (20, 10), f"Ожидалось a=20, b=10, сейчас a={a}, b={b}"

        def test_no_hardcode():
            src = open("solution.py", encoding="utf-8").read()
            assert not re.search(r"^\\s*a\\s*=\\s*20\\s*$", src, re.M), "Не присваивай числа напрямую — поменяй значения местами"
        """,
        """
        a = 10
        b = 20
        a, b = b, a
        print(a, b)
        """,
        hint="В Python можно так: `a, b = b, a`."),
    cod(f"{P}-m1-l2-e5", t("""
        Счётчик попыток.

        Создай переменную `attempts` со значением `0`, затем **три раза** увеличь её на 1 (используй `+=`) и выведи.

        Ожидаемый вывод:
        ```
        3
        ```
        """),
        "",
        """
        def test_value():
            assert attempts == 3, f"attempts должна быть 3, сейчас {attempts}"

        def test_output():
            assert OUTPUT.strip() == "3", f"Напечатано {OUTPUT.strip()!r}"

        def test_increment():
            src = open("solution.py", encoding="utf-8").read()
            assert src.count("+=") >= 3, "Увеличь переменную три раза через +="
        """,
        """
        attempts = 0
        attempts += 1
        attempts += 1
        attempts += 1
        print(attempts)
        """)),

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
        """)),
)

# ============================================================
m2 = module(f"{P}-m2", "Числа", "🔢", "int, float, арифметика и преобразования",

lesson(f"{P}-m2-l1", "Целые и дробные числа", 
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        print(2 + 3)
        print(2 + 3.0)
        print(1_000_000 + 1)
        print(1e3)
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа? Знаменитая особенность дробных чисел.", """
        print(0.1 + 0.2)
        print(0.1 + 0.2 == 0.3)
        print(round(0.1 + 0.2, 2) == 0.3)
        """, hint="Дробные числа хранятся в двоичном виде приближённо."),
    cod(f"{P}-m2-l1-e3", t("""
        Напиши функцию `almost_equal(a, b)`, которая сравнивает два дробных числа **с точностью до 9 знаков** после запятой.

        - Возвращает `True`, если после округления до 9 знаков (`round(x, 9)`) числа равны.

        Примеры:
        ```
        almost_equal(0.1 + 0.2, 0.3)   # → True
        almost_equal(1.0, 1.1)         # → False
        ```
        """),
        """
        def almost_equal(a, b):
            pass
        """,
        """
        def test_float():
            assert almost_equal(0.1 + 0.2, 0.3) is True, "0.1 + 0.2 почти равно 0.3"

        def test_different():
            assert almost_equal(1.0, 1.1) is False, "1.0 и 1.1 разные"
        """,
        """
        def almost_equal(a, b):
            return round(a, 9) == round(b, 9)
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `to_kopecks(rubles)`, которая переводит сумму в рублях (дробное число) в **целое** количество копеек.

        - Получает: `rubles` — число, например `12.34`.
        - Возвращает: `int` — количество копеек, **округлённое** до целого.

        Примеры:
        ```
        to_kopecks(12.34)   # → 1234
        to_kopecks(0.1)     # → 10
        to_kopecks(5)       # → 500
        ```
        Осторожно: `12.34 * 100` даёт `1233.9999999999998`, поэтому нужен `round()`, а не `int()`.
        """),
        """
        def to_kopecks(rubles):
            pass
        """,
        """
        def test_values():
            assert to_kopecks(12.34) == 1234, f"Получено {to_kopecks(12.34)!r}"
            assert to_kopecks(0.1) == 10 and to_kopecks(5) == 500, "0.1 → 10, 5 → 500"

        def test_int():
            assert isinstance(to_kopecks(1.5), int), "Верни именно int"
        """,
        """
        def to_kopecks(rubles):
            return round(rubles * 100)
        """,
        hint="`round(x)` без второго аргумента возвращает `int`.", xp=20),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `is_whole(x)`, которая проверяет, что дробное число на самом деле **целое** (без дробной части).

        Примеры:
        ```
        is_whole(3.0)    # → True
        is_whole(3.5)    # → False
        is_whole(-2.0)   # → True
        ```
        У `float` есть метод `.is_integer()`, но можно и через `x == int(x)`.
        """),
        """
        def is_whole(x):
            pass
        """,
        """
        def test_values():
            got = [is_whole(v) for v in (3.0, 3.5, -2.0, 0.0)]
            assert got == [True, False, True, True], f"Получено {got}"
        """,
        """
        def is_whole(x):
            return float(x).is_integer()
        """)),

lesson(f"{P}-m2-l2", "Арифметические операторы", 
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        print(7 // 2, 7 % 2, 7 / 2)
        print(2 ** 5)
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа? Следи за приоритетом.", """
        print(2 + 3 * 4)
        print((2 + 3) * 4)
        print(-2 ** 2)
        """, hint="Степень выполняется раньше унарного минуса: `-2 ** 2` — это `-(2 ** 2)`."),
    cod(f"{P}-m2-l2-e3", t("""
        Напиши функцию `split_time(seconds)`, которая раскладывает секунды на минуты и секунды.

        - Получает: `seconds` — целое число секунд.
        - Возвращает: пару `(минуты, оставшиеся_секунды)`.

        Примеры:
        ```
        split_time(135)   # → (2, 15)
        split_time(120)   # → (2, 0)
        split_time(59)    # → (0, 59)
        ```
        Пригодятся `//` и `%`. Вернуть пару: `return a, b`.
        """),
        """
        def split_time(seconds):
            pass
        """,
        """
        def test_values():
            got = [split_time(s) for s in (135, 120, 59)]
            assert got == [(2, 15), (2, 0), (0, 59)], f"Получено {got}"
        """,
        """
        def split_time(seconds):
            return seconds // 60, seconds % 60
        """),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `last_digit(n)`, которая возвращает **последнюю цифру** целого неотрицательного числа.

        Примеры:
        ```
        last_digit(2024)   # → 4
        last_digit(7)      # → 7
        last_digit(10)     # → 0
        ```
        Последняя цифра — остаток от деления на 10.
        """),
        """
        def last_digit(n):
            pass
        """,
        """
        def test_values():
            got = [last_digit(n) for n in (2024, 7, 10, 999)]
            assert got == [4, 7, 0, 9], f"Получено {got}"
        """,
        """
        def last_digit(n):
            return n % 10
        """),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `boxes_needed(items, per_box)` — сколько коробок нужно, чтобы упаковать `items` предметов, если в одну коробку помещается `per_box`.

        Неполная коробка тоже считается.

        Примеры:
        ```
        boxes_needed(10, 5)   # → 2
        boxes_needed(11, 5)   # → 3   две полные + одна с одним предметом
        boxes_needed(0, 5)    # → 0
        ```
        Реши без `if`: через `//` и `%` или через трюк `(items + per_box - 1) // per_box`.
        """),
        """
        def boxes_needed(items, per_box):
            pass
        """,
        """
        def test_values():
            got = [boxes_needed(i, 5) for i in (10, 11, 0, 1, 4)]
            assert got == [2, 3, 0, 1, 1], f"Получено {got}"
        """,
        """
        def boxes_needed(items, per_box):
            return (items + per_box - 1) // per_box
        """,
        hint="Целых коробок `items // per_box`, и ещё одна, если остаток `items % per_box` не ноль.", xp=20)),

lesson(f"{P}-m2-l3", "Преобразование типов и округление", 
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        print(int("42") + 1)
        print(int(3.99))
        print(float("2.5") * 2)
        print(str(10) + str(20))
        """),
    out(f"{P}-m2-l3-e2", "Что выведет программа? Округление в Python «банковское».", """
        print(round(2.567, 2))
        print(round(2.5), round(3.5))
        print(round(-1.5))
        """, hint="При ровно .5 Python округляет к ближайшему **чётному** числу."),
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
        hint="```py\ntry:\n    return int(text)\nexcept ValueError:\n    return default\n```")),
)

# ============================================================
m3 = module(f"{P}-m3", "Строки", "🔤", "Текст, методы строк и f-строки",

lesson(f"{P}-m3-l1", "Строки: склейка, длина, экранирование", 
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        s = "Code" + "Quest"
        print(s)
        print(len(s))
        print("-" * 5)
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа?", """
        s = "автотест"
        print("тест" in s)
        print("Тест" in s)
        print(len(""))
        """, hint="Проверка `in` чувствительна к регистру."),
    cod(f"{P}-m3-l1-e3", t("""
        Напиши функцию `greet(name)`, которая **возвращает** строку `Привет, <имя>!` — через склейку `+`.

        Примеры:
        ```
        greet("Аня")   # → "Привет, Аня!"
        ```
        """),
        """
        def greet(name):
            pass
        """,
        """
        def test_greet():
            assert greet("Аня") == "Привет, Аня!", f"Получено {greet('Аня')!r}"
            assert greet("Bob") == "Привет, Bob!", "Для Bob — «Привет, Bob!»"
        """,
        """
        def greet(name):
            return "Привет, " + name + "!"
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `frame(text)`, которая возвращает текст в «рамке» из символов `*` — **три строки**, разделённые `\\n`.

        Ширина рамки = длина текста + 4.

        Пример для `frame("hi")`:
        ```
        ******
        * hi *
        ******
        ```
        То есть результат — строка `"******\\n* hi *\\n******"`.
        """),
        """
        def frame(text):
            pass
        """,
        """
        def test_hi():
            assert frame("hi") == "******\\n* hi *\\n******", f"Получено:\\n{frame('hi')}"

        def test_word():
            lines = frame("Python").split("\\n")
            assert lines == ["**********", "* Python *", "**********"], f"Получено: {lines}"
        """,
        """
        def frame(text):
            border = "*" * (len(text) + 4)
            return border + "\\n* " + text + " *\\n" + border
        """,
        hint="Граница — `\"*\" * (len(text) + 4)`. Строки соедини через `\"\\n\"`.", xp=20),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `contains_ignore_case(text, word)` — есть ли `word` в `text` **без учёта регистра**.

        Примеры:
        ```
        contains_ignore_case("Ошибка ERROR в логе", "error")   # → True
        contains_ignore_case("всё хорошо", "error")            # → False
        ```
        Приведи обе строки к одному регистру методом `.lower()`.
        """),
        """
        def contains_ignore_case(text, word):
            pass
        """,
        """
        def test_values():
            assert contains_ignore_case("Ошибка ERROR в логе", "error") is True, "ERROR и error — одно и то же"
            assert contains_ignore_case("всё хорошо", "error") is False, "Слова нет — False"
            assert contains_ignore_case("Timeout", "TIME") is True, "Регистр не важен"
        """,
        """
        def contains_ignore_case(text, word):
            return word.lower() in text.lower()
        """)),

lesson(f"{P}-m3-l2", "Методы строк", 
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        s = "  Hello, World  "
        print(s.strip())
        print(s.strip().upper())
        print(s.strip().replace("World", "Python"))
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа?", """
        line = "ERROR;db;timeout"
        parts = line.split(";")
        print(parts)
        print(" | ".join(parts))
        print(line.startswith("ERROR"), line.count("t"))
        """),
    cod(f"{P}-m3-l2-e3", t("""
        Напиши функцию `normalize_email(email)`, которая приводит email к единому виду: убирает пробелы по краям и переводит в нижний регистр.

        Примеры:
        ```
        normalize_email("  Anna@Mail.RU ")   # → "anna@mail.ru"
        ```
        """),
        """
        def normalize_email(email):
            pass
        """,
        """
        def test_email():
            assert normalize_email("  Anna@Mail.RU ") == "anna@mail.ru", f"Получено {normalize_email('  Anna@Mail.RU ')!r}"
        """,
        """
        def normalize_email(email):
            return email.strip().lower()
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши функцию `initials(full_name)`, которая из полного имени делает инициалы.

        - Получает: строку из 2–3 слов через пробел, например `"иванов иван петрович"`.
        - Возвращает: первые буквы слов **заглавными**, каждая с точкой, без пробелов.

        Примеры:
        ```
        initials("иванов иван петрович")   # → "И.И.П."
        initials("Anna Smith")             # → "A.S."
        ```
        """),
        """
        def initials(full_name):
            pass
        """,
        """
        def test_values():
            assert initials("иванов иван петрович") == "И.И.П.", f"Получено {initials('иванов иван петрович')!r}"
            assert initials("Anna Smith") == "A.S.", f"Получено {initials('Anna Smith')!r}"
        """,
        """
        def initials(full_name):
            return "".join(word[0].upper() + "." for word in full_name.split())
        """,
        hint="`split()` разобьёт на слова, `word[0]` — первая буква.", xp=20),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `log_level(line)`, которая определяет уровень строки лога.

        - Строка лога начинается с уровня в квадратных скобках: `"[ERROR] нет связи"`, `"[info] старт"`.
        - Возвращает: уровень **заглавными буквами** без скобок, например `"ERROR"`.
        - Если строка не начинается с `[` — вернуть `"UNKNOWN"`.

        Примеры:
        ```
        log_level("[ERROR] нет связи")   # → "ERROR"
        log_level("[info] старт")        # → "INFO"
        log_level("просто текст")        # → "UNKNOWN"
        ```
        Пригодятся `startswith`, `find("]")` и срез.
        """),
        """
        def log_level(line):
            pass
        """,
        """
        def test_values():
            got = [log_level(s) for s in ("[ERROR] нет связи", "[info] старт", "просто текст", "[Warn]x")]
            assert got == ["ERROR", "INFO", "UNKNOWN", "WARN"], f"Получено {got}"
        """,
        """
        def log_level(line):
            if not line.startswith("["):
                return "UNKNOWN"
            end = line.find("]")
            return line[1:end].upper()
        """,
        hint="`line[1:end]` — текст между `[` и `]`, где `end = line.find(\"]\")`.", xp=20)),

lesson(f"{P}-m3-l3", "f-строки и форматирование", 
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        name = "Аня"
        solved = 3
        print(f"{name} решила {solved} задачи и получила {solved * 10} XP")
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа? Форматирование чисел.", """
        pi = 3.14159
        print(f"{pi:.2f}")
        print(f"{0.756:.0%}")
        print(f"{1234567:,}")
        """),
    cod(f"{P}-m3-l3-e3", t("""
        Напиши функцию `price_tag(name, price)`, которая возвращает ценник в формате `"<название>: <цена> руб."`, где цена всегда **с двумя знаками** после точки.

        Примеры:
        ```
        price_tag("Чай", 99)       # → "Чай: 99.00 руб."
        price_tag("Кофе", 249.5)   # → "Кофе: 249.50 руб."
        ```
        Формат с двумя знаками: `{price:.2f}`.
        """),
        """
        def price_tag(name, price):
            pass
        """,
        """
        def test_values():
            assert price_tag("Чай", 99) == "Чай: 99.00 руб.", f"Получено {price_tag('Чай', 99)!r}"
            assert price_tag("Кофе", 249.5) == "Кофе: 249.50 руб.", f"Получено {price_tag('Кофе', 249.5)!r}"
        """,
        """
        def price_tag(name, price):
            return f"{name}: {price:.2f} руб."
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `progress(done, total)`, которая возвращает строку прогресса вида `"3/10 (30%)"`.

        - Процент — целый, без дробной части.
        - Если `total` равен 0 — процент считать 0.

        Примеры:
        ```
        progress(3, 10)   # → "3/10 (30%)"
        progress(1, 3)    # → "1/3 (33%)"
        progress(0, 0)    # → "0/0 (0%)"
        ```
        """),
        """
        def progress(done, total):
            pass
        """,
        """
        def test_values():
            got = [progress(3, 10), progress(1, 3), progress(0, 0), progress(5, 5)]
            assert got == ["3/10 (30%)", "1/3 (33%)", "0/0 (0%)", "5/5 (100%)"], f"Получено {got}"
        """,
        """
        def progress(done, total):
            pct = done * 100 // total if total else 0
            return f"{done}/{total} ({pct}%)"
        """, xp=20),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `table_row(name, passed, failed)`, которая возвращает строку таблицы отчёта:

        - имя теста **выровнено влево** на ширину 12 символов;
        - числа `passed` и `failed` **выровнены вправо** на ширину 4 символа каждое;
        - между колонками по одному пробелу.

        Пример:
        ```
        table_row("login", 10, 2)
        # → "login          10    2"
        #    ^^^^^^^^^^^^ 12 символов, затем пробел, "  10", пробел, "   2"
        ```
        Форматы: `{name:<12}` и `{passed:>4}`.
        """),
        """
        def table_row(name, passed, failed):
            pass
        """,
        """
        def test_row():
            assert table_row("login", 10, 2) == "login          10    2", f"Получено {table_row('login', 10, 2)!r}"
            assert len(table_row("search", 100, 0)) == 22, "Ширина строки: 12 + 1 + 4 + 1 + 4 = 22"
        """,
        """
        def table_row(name, passed, failed):
            return f"{name:<12} {passed:>4} {failed:>4}"
        """)),
)

TOPIC = topic("py-vars", "Переменные и типы данных", "📦", "#58cc02",
              "print, переменные, числа, строки и преобразование типов",
              m1, m2, m3, group="Python")
