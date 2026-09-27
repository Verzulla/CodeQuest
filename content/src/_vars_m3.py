"""Тема «Переменные и типы данных», модуль 3 «Числа» — задания.
Теория уроков — в _vars_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "var"

m3 = module(f"{P}-m2", "Числа", "🔢", "int и float, арифметика, деление с остатком и округление",

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
    out(f"{P}-m2-l1-e6", "Что выведет программа? Какой тип получится.", """
        print(7 + 0.0)
        print(3 * 1.5)
        print(1e-3)
        print(2.50)
        """, hint="Лишние нули в конце дробного числа Python не печатает."),
    out(f"{P}-m2-l1-e7", "Что выведет программа? Большие целые и неточные дробные.", """
        print(2 ** 64)
        print(0.1 * 3)
        print(10 / 3)
        """, hint="У int нет предела, а float хранит около 16 значащих цифр."),
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
        Осторожно: например, `19.99 * 100` даёт `1998.9999999999998`, поэтому нужен `round()`, а не `int()`.
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
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `average2(a, b)` — среднее арифметическое двух чисел (сумма, делённая на 2).

        Примеры:
        ```
        average2(2, 4)    # → 3.0
        average2(1, 2)    # → 1.5
        average2(-3, 3)   # → 0.0
        ```
        Обрати внимание: результат — дробное число, даже если оно целое.
        """),
        """
        def average2(a, b):
            pass
        """,
        """
        def test_values():
            got = [average2(2, 4), average2(1, 2), average2(-3, 3)]
            assert got == [3.0, 1.5, 0.0], f"Получено {got}"
            assert isinstance(average2(2, 4), float), "Результат деления / — всегда float"
        """,
        """
        def average2(a, b):
            return (a + b) / 2
        """,
        hint="Не забудь скобки: `(a + b) / 2`.")),

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
    out(f"{P}-m2-l2-e6", "Что выведет программа? Порядок одинаковых операций.", """
        print(10 - 2 - 3)
        print(100 / 10 / 2)
        print(2 ** 3 ** 2)
        """, hint="`-` и `/` выполняются слева направо, а `**` — справа налево."),
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `rectangle_area(width, height)` — площадь прямоугольника.

        Примеры:
        ```
        rectangle_area(3, 4)     # → 12
        rectangle_area(2.5, 2)   # → 5.0
        ```
        """),
        """
        def rectangle_area(width, height):
            pass
        """,
        """
        def test_values():
            assert rectangle_area(3, 4) == 12 and rectangle_area(2.5, 2) == 5.0, "Площадь = ширина × высота"
        """,
        """
        def rectangle_area(width, height):
            return width * height
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `to_fahrenheit(celsius)` — перевод градусов Цельсия в Фаренгейты по формуле
        `F = C × 9 / 5 + 32`.

        Примеры:
        ```
        to_fahrenheit(0)     # → 32.0
        to_fahrenheit(100)   # → 212.0
        to_fahrenheit(-40)   # → -40.0
        ```
        """),
        """
        def to_fahrenheit(celsius):
            pass
        """,
        """
        def test_values():
            got = [to_fahrenheit(0), to_fahrenheit(100), to_fahrenheit(-40), to_fahrenheit(36.6)]
            assert [round(x, 2) for x in got] == [32.0, 212.0, -40.0, 97.88], f"Получено {got}"
        """,
        """
        def to_fahrenheit(celsius):
            return celsius * 9 / 5 + 32
        """),
    cod(f"{P}-m2-l2-e9", t("""
        Напиши функцию `average3(a, b, c)` — среднее арифметическое трёх чисел.

        Примеры:
        ```
        average3(1, 2, 3)    # → 2.0
        average3(5, 5, 6)    # → 5.333333333333333
        ```
        """),
        """
        def average3(a, b, c):
            pass
        """,
        """
        def test_values():
            assert average3(1, 2, 3) == 2.0, f"Получено {average3(1, 2, 3)!r}"
            assert round(average3(5, 5, 6), 4) == 5.3333, f"Получено {average3(5, 5, 6)!r}"
        """,
        """
        def average3(a, b, c):
            return (a + b + c) / 3
        """),
    cod(f"{P}-m2-l2-e10", t("""
        Напиши функцию `total_price(price, quantity, discount)` — стоимость покупки со скидкой.

        - `price` — цена одной штуки, `quantity` — количество, `discount` — скидка **в процентах** (например, `10` — это 10%).
        - Стоимость = цена × количество × (1 − скидка / 100).
        - Результат округли до 2 знаков: `round(..., 2)`.

        Примеры:
        ```
        total_price(100, 3, 10)    # → 270.0
        total_price(99.9, 2, 0)    # → 199.8
        ```
        """),
        """
        def total_price(price, quantity, discount):
            pass
        """,
        """
        def test_values():
            assert total_price(100, 3, 10) == 270.0, f"Получено {total_price(100, 3, 10)!r}"
            assert total_price(99.9, 2, 0) == 199.8, f"Получено {total_price(99.9, 2, 0)!r}"
            assert total_price(250, 1, 50) == 125.0, "Скидка 50% — половина цены"
        """,
        """
        def total_price(price, quantity, discount):
            return round(price * quantity * (1 - discount / 100), 2)
        """, xp=20),
    cod(f"{P}-m2-l2-e11", t("""
        Функция `avg(a, b)` должна считать среднее двух чисел, но возвращает неправильный результат:
        `avg(2, 4)` даёт `4.0` вместо `3.0`. Найди ошибку в порядке действий и исправь её.
        """),
        """
        def avg(a, b):
            return a + b / 2
        """,
        """
        def test_values():
            assert avg(2, 4) == 3.0 and avg(1, 2) == 1.5, f"avg(2, 4) вернула {avg(2, 4)!r}"
        """,
        """
        def avg(a, b):
            return (a + b) / 2
        """,
        hint="Деление выполняется раньше сложения: сейчас считается `a + (b / 2)`.")),

lesson(f"{P}-divmod", "// и %: деление с остатком",
    out(f"{P}-divmod-e1", "Что выведет программа?", """
        print(17 // 5, 17 % 5)
        print(divmod(17, 5))
        print(20 % 5, 3 % 10)
        """, hint="Если число меньше делителя, частное 0, а остаток — само число."),
    out(f"{P}-divmod-e2", "Что выведет программа? Отрицательные числа.", """
        print(-7 // 2)
        print(-7 % 2)
        print(7 // -2)
        """, hint="`//` округляет вниз, к меньшему числу: −3.5 → −4."),
    out(f"{P}-divmod-e3", "Что выведет программа? Цифры числа.", """
        n = 2024
        print(n % 10)
        print(n // 10 % 10)
        print(n // 100)
        """),
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
        hint="Целых коробок `items // per_box`, и ещё одна, если остаток `items % per_box` не ноль.", xp=20),
    cod(f"{P}-divmod-e4", t("""
        Напиши функцию `is_even(n)` — чётное ли целое число.

        Примеры:
        ```
        is_even(4)    # → True
        is_even(7)    # → False
        is_even(0)    # → True
        is_even(-2)   # → True
        ```
        Чётное число делится на 2 без остатка.
        """),
        """
        def is_even(n):
            pass
        """,
        """
        def test_values():
            got = [is_even(4), is_even(7), is_even(0), is_even(-2), is_even(-3)]
            assert got == [True, False, True, True, False], f"Получено {got}"
        """,
        """
        def is_even(n):
            return n % 2 == 0
        """),
    cod(f"{P}-divmod-e5", t("""
        Напиши функцию `hms(seconds)`, которая раскладывает секунды на часы, минуты и секунды и возвращает **три** числа.

        Примеры:
        ```
        hms(3725)   # → (1, 2, 5)     1 ч 2 мин 5 с
        hms(59)     # → (0, 0, 59)
        hms(7200)   # → (2, 0, 0)
        ```
        В часе 3600 секунд, в минуте 60. Вернуть три значения: `return h, m, s`.
        """),
        """
        def hms(seconds):
            pass
        """,
        """
        def test_values():
            got = [hms(3725), hms(59), hms(7200), hms(0)]
            assert got == [(1, 2, 5), (0, 0, 59), (2, 0, 0), (0, 0, 0)], f"Получено {got}"
        """,
        """
        def hms(seconds):
            hours, rest = divmod(seconds, 3600)
            minutes, secs = divmod(rest, 60)
            return hours, minutes, secs
        """,
        hint="`hours, rest = divmod(seconds, 3600)`, потом так же для минут.", xp=20)),

lesson(f"{P}-round", "Округление и модуль math",
    out(f"{P}-m2-l3-e2", "Что выведет программа? Округление в Python «банковское».", """
        print(round(2.567, 2))
        print(round(2.5), round(3.5))
        print(round(-1.5))
        """, hint="При ровно .5 Python округляет к ближайшему **чётному** числу."),
    out(f"{P}-round-e1", "Что выведет программа? Вниз, вверх и отбросить.", """
        import math
        print(math.floor(2.7), math.ceil(2.1))
        print(math.floor(-2.5), math.ceil(-2.5))
        print(int(-2.5), int(2.9))
        """, hint="floor — к меньшему, ceil — к большему, int — просто отбрасывает дробную часть."),
    out(f"{P}-round-e2", "Что выведет программа?", """
        print(abs(-5), abs(3.5))
        print(round(1234.567, -2))
        print(max(3, 9, 2), min(3, 9, 2))
        """, hint="Отрицательное число знаков в `round` округляет до десятков, сотен…"),
    cod(f"{P}-round-e3", t("""
        Напиши функцию `pages_needed(items, per_page)` — сколько страниц нужно, чтобы показать `items` записей,
        если на странице помещается `per_page`. Неполная страница тоже считается.

        Примеры:
        ```
        pages_needed(45, 10)   # → 5
        pages_needed(40, 10)   # → 4
        pages_needed(1, 10)    # → 1
        ```
        Используй `math.ceil` — округление вверх. Не забудь `import math`.
        """),
        """
        import math

        def pages_needed(items, per_page):
            pass
        """,
        """
        def test_values():
            got = [pages_needed(45, 10), pages_needed(40, 10), pages_needed(1, 10), pages_needed(0, 10)]
            assert got == [5, 4, 1, 0], f"Получено {got}"
        """,
        """
        import math

        def pages_needed(items, per_page):
            return math.ceil(items / per_page)
        """),
    cod(f"{P}-round-e4", t("""
        Напиши функцию `distance(x1, y1, x2, y2)` — расстояние между двумя точками на плоскости:
        корень из `(x2 − x1)² + (y2 − y1)²`. Результат округли до 2 знаков.

        Примеры:
        ```
        distance(0, 0, 3, 4)   # → 5.0
        distance(1, 1, 2, 2)   # → 1.41
        ```
        Квадратный корень — `math.sqrt(x)`.
        """),
        """
        import math

        def distance(x1, y1, x2, y2):
            pass
        """,
        """
        def test_values():
            assert distance(0, 0, 3, 4) == 5.0, f"Получено {distance(0, 0, 3, 4)!r}"
            assert distance(1, 1, 2, 2) == 1.41, f"Получено {distance(1, 1, 2, 2)!r}"
        """,
        """
        import math

        def distance(x1, y1, x2, y2):
            return round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), 2)
        """, xp=20),
    cod(f"{P}-round-e5", t("""
        Напиши функцию `circle_area(r)` — площадь круга радиуса `r`: π × r², округлённая до 2 знаков.

        Примеры:
        ```
        circle_area(1)   # → 3.14
        circle_area(2)   # → 12.57
        ```
        Число π — `math.pi`.
        """),
        """
        import math

        def circle_area(r):
            pass
        """,
        """
        def test_values():
            assert circle_area(1) == 3.14 and circle_area(2) == 12.57, f"Получено {circle_area(1)!r}, {circle_area(2)!r}"
        """,
        """
        import math

        def circle_area(r):
            return round(math.pi * r ** 2, 2)
        """),
    cod(f"{P}-round-e6", t("""
        Напиши функцию `diff(a, b)` — насколько два числа отличаются друг от друга (всегда неотрицательное число).

        Примеры:
        ```
        diff(3, 10)   # → 7
        diff(10, 3)   # → 7
        diff(-2, 2)   # → 4
        ```
        Модуль числа — `abs(x)`.
        """),
        """
        def diff(a, b):
            pass
        """,
        """
        def test_values():
            got = [diff(3, 10), diff(10, 3), diff(-2, 2), diff(5, 5)]
            assert got == [7, 7, 4, 0], f"Получено {got}"
        """,
        """
        def diff(a, b):
            return abs(a - b)
        """),
    cod(f"{P}-round-e7", t("""
        Напиши функцию `percent(part, whole)` — сколько процентов составляет `part` от `whole`, округлено до **1 знака**.

        Примеры:
        ```
        percent(1, 3)     # → 33.3
        percent(50, 200)  # → 25.0
        percent(2, 3)     # → 66.7
        ```
        """),
        """
        def percent(part, whole):
            pass
        """,
        """
        def test_values():
            got = [percent(1, 3), percent(50, 200), percent(2, 3)]
            assert got == [33.3, 25.0, 66.7], f"Получено {got}"
        """,
        """
        def percent(part, whole):
            return round(part / whole * 100, 1)
        """)),
)
