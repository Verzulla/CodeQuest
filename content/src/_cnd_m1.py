"""Тема «Условные операторы», модуль 1 «Основы if» — задания. Теория — в _cnd_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "cnd"

m1 = module(f"{P}-m1", "Основы if", "🔀", "if/else, сравнения, строки и типы, elif, границы диапазонов",

lesson(f"{P}-m1-l1", "if и else",
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        t = 25
        if t > 20:
            print("жарко")
        else:
            print("прохладно")
        print("конец")
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа? Внимание на отступы.", """
        x = 3
        if x > 5:
            print("A")
            print("B")
        print("C")
        """, hint="«A» и «B» внутри if, «C» — снаружи."),
    out(f"{P}-m1-l1-e6", "Что выведет программа? `if` без `else`.", """
        t = 15
        if t > 20:
            print("жарко")
        print("конец")
        """, hint="Условие ложно — блок пропускается, а `else` нет."),
    out(f"{P}-m1-l1-e7", "Что выведет программа? В блоке может быть несколько строк.", """
        n = 7
        if n % 2 == 0:
            print("чётное")
            n = n // 2
        else:
            print("нечётное")
            n = n * 3 + 1
        print(n)
        """, hint="7 нечётное: выполняется весь блок `else` — обе строки."),
    cod(f"{P}-m1-l1-e3", t("""
        Напиши функцию `is_adult(age)`, которая проверяет совершеннолетие.

        - Возвращает `True`, если возраст **18 или больше**, иначе `False`.

        Примеры:
        ```
        is_adult(30)   # → True
        is_adult(10)   # → False
        is_adult(18)   # → True
        ```
        """),
        """
        def is_adult(age):
            pass
        """,
        """
        def test_values():
            got = [is_adult(a) for a in (30, 10, 18, 17)]
            assert got == [True, False, True, False], f"Получено {got} — проверь границу 18"
        """,
        """
        def is_adult(age):
            return age >= 18
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `max2(a, b)`, которая возвращает большее из двух чисел, **без** встроенной `max`.

        Примеры:
        ```
        max2(5, 3)    # → 5
        max2(-1, 8)   # → 8
        max2(4, 4)    # → 4
        ```
        """),
        """
        def max2(a, b):
            pass
        """,
        """
        def test_values():
            assert [max2(5, 3), max2(-1, 8), max2(4, 4)] == [5, 8, 4], "Неверный максимум"

        def test_no_max():
            assert "max(" not in open("solution.py", encoding="utf-8").read().replace("max2(", ""), "Не используй встроенную max"
        """,
        """
        def max2(a, b):
            if a > b:
                return a
            return b
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `check_status(code)` для проверки ответа API.

        - Если `code` равен `200` — вернуть строку `"OK"`.
        - Иначе — вернуть `"FAIL: <код>"`, например `"FAIL: 404"`.

        Примеры:
        ```
        check_status(200)   # → "OK"
        check_status(500)   # → "FAIL: 500"
        ```
        """),
        """
        def check_status(code):
            pass
        """,
        """
        def test_values():
            assert check_status(200) == "OK", "200 → OK"
            assert check_status(404) == "FAIL: 404" and check_status(500) == "FAIL: 500", "Иначе — FAIL: код"
        """,
        """
        def check_status(code):
            if code == 200:
                return "OK"
            else:
                return f"FAIL: {code}"
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `abs_value(n)` — модуль числа **без** встроенной `abs`:
        отрицательное число превращается в положительное, остальные остаются как есть.

        Примеры:
        ```
        abs_value(-5)   # → 5
        abs_value(3)    # → 3
        abs_value(0)    # → 0
        ```
        """),
        """
        def abs_value(n):
            pass
        """,
        """
        def test_values():
            got = [abs_value(-5), abs_value(3), abs_value(0), abs_value(-0.5)]
            assert got == [5, 3, 0, 0.5], f"Получено {got}"

        def test_no_abs():
            src = open("solution.py", encoding="utf-8").read()
            assert "abs(" not in src.replace("abs_value(", ""), "Реши через if, без встроенной abs"
        """,
        """
        def abs_value(n):
            if n < 0:
                return -n
            return n
        """,
        hint="Если `n < 0` — верни `-n`, иначе `n`.")),

lesson(f"{P}-m1-l2", "Операторы сравнения",
    out(f"{P}-m1-l2-e6", "Что выведет программа?", """
        print(5 == 5.0, 5 != 5)
        print(3 >= 3, 2 > 3, 2 <= 3)
        """),
    out(f"{P}-m1-l2-e7", "Что выведет программа? Цепочки сравнений.", """
        print(1 < 2 < 3)
        print(3 > 2 > 1)
        print(1 < 3 > 2)
        print(1 < 3 < 2)
        """, hint="`a < b < c` — это «a < b и b < c»: должны выполняться оба сравнения."),
    out(f"{P}-m1-l2-e8", "Что выведет программа? Результат сравнения можно сохранить.", """
        x = 7
        ok = 0 <= x <= 10
        print(ok)
        print(type(ok).__name__)
        """),
    cod(f"{P}-m1-l2-e3", t("""
        Напиши функцию `in_range(x, low, high)` — лежит ли `x` в отрезке **от `low` до `high` включительно**.

        Используй цепочку сравнений.

        Примеры:
        ```
        in_range(5, 1, 10)    # → True
        in_range(10, 1, 10)   # → True   граница входит
        in_range(0, 1, 10)    # → False
        ```
        """),
        """
        def in_range(x, low, high):
            pass
        """,
        """
        def test_values():
            got = [in_range(5, 1, 10), in_range(10, 1, 10), in_range(1, 1, 10), in_range(0, 1, 10), in_range(11, 1, 10)]
            assert got == [True, True, True, False, False], f"Получено {got}"
        """,
        """
        def in_range(x, low, high):
            return low <= x <= high
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `is_valid_port(port)` — проверка номера порта.

        Порт корректен, если это целое число от **1 до 65535** включительно.

        Примеры:
        ```
        is_valid_port(8080)    # → True
        is_valid_port(0)       # → False
        is_valid_port(65536)   # → False
        ```
        """),
        """
        def is_valid_port(port):
            pass
        """,
        """
        def test_values():
            got = [is_valid_port(p) for p in (8080, 1, 65535, 0, 65536, -1)]
            assert got == [True, True, True, False, False, False], f"Получено {got}"
        """,
        """
        def is_valid_port(port):
            return 1 <= port <= 65535
        """),
    cod(f"{P}-m1-l2-e9", t("""
        Напиши функцию `is_teen(age)` — подросток ли человек: возраст **от 13 до 19 включительно**. Используй цепочку сравнений.

        Примеры:
        ```
        is_teen(13)   # → True
        is_teen(19)   # → True
        is_teen(20)   # → False
        is_teen(12)   # → False
        ```
        """),
        """
        def is_teen(age):
            pass
        """,
        """
        def test_values():
            got = [is_teen(13), is_teen(19), is_teen(16), is_teen(20), is_teen(12)]
            assert got == [True, True, True, False, False], f"Получено {got}"
        """,
        """
        def is_teen(age):
            return 13 <= age <= 19
        """),
    cod(f"{P}-m1-l2-e10", t("""
        Напиши функцию `is_passing(score, threshold)` — сдан ли тест: баллов **не меньше** порога.

        Примеры:
        ```
        is_passing(75, 60)   # → True
        is_passing(60, 60)   # → True    ровно порог — сдан
        is_passing(59, 60)   # → False
        ```
        """),
        """
        def is_passing(score, threshold):
            pass
        """,
        """
        def test_values():
            got = [is_passing(75, 60), is_passing(60, 60), is_passing(59, 60)]
            assert got == [True, True, False], f"Получено {got}"
        """,
        """
        def is_passing(score, threshold):
            return score >= threshold
        """),
    cod(f"{P}-m1-l2-e11", t("""
        Напиши функцию `strictly_between(x, low, high)` — лежит ли `x` **строго между** границами (сами границы не входят).

        Примеры:
        ```
        strictly_between(5, 1, 10)    # → True
        strictly_between(1, 1, 10)    # → False   граница не входит
        strictly_between(10, 1, 10)   # → False
        ```
        """),
        """
        def strictly_between(x, low, high):
            pass
        """,
        """
        def test_values():
            got = [strictly_between(5, 1, 10), strictly_between(1, 1, 10), strictly_between(10, 1, 10), strictly_between(0, 1, 10)]
            assert got == [True, False, False, False], f"Получено {got}"
        """,
        """
        def strictly_between(x, low, high):
            return low < x < high
        """)),

lesson(f"{P}-strcmp", "Сравнение строк и разных типов",
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        print(5 == 5.0, 5 != 6)
        print(3 < 7 < 10, 3 < 7 > 10)
        print("apple" < "banana", "Z" < "a")
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа? Сравнение строк с числами.", """
        print("10" == 10)
        print("10" < "9")
        print(int("10") < int("9"))
        """, hint="Строки сравниваются посимвольно: `\"1\"` меньше `\"9\"`."),
    out(f"{P}-strcmp-e1", "Что выведет программа? Как строки сравниваются по буквам.", """
        print("abc" < "abd")
        print("Zoo" < "apple")
        print("a" < "ab")
        print("" < "a")
        """, hint="Сравнение идёт посимвольно; заглавные латинские буквы «меньше» строчных; более короткое начало — меньше."),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `compare_versions(a, b)` для версий вида `"1.10"` и `"1.9"` (ровно две части через точку).

        - Возвращает `-1`, если `a` меньше `b`; `1`, если больше; `0`, если равны.
        - Сравнивать нужно **как числа**, а не как строки: `1.10` больше `1.9`.

        Примеры:
        ```
        compare_versions("1.10", "1.9")   # → 1
        compare_versions("2.0", "2.0")    # → 0
        compare_versions("0.9", "1.0")    # → -1
        ```
        Подсказка: `tuple(int(p) for p in a.split("."))` превращает `"1.10"` в `(1, 10)`, а кортежи сравниваются поэлементно.
        """),
        """
        def compare_versions(a, b):
            pass
        """,
        """
        def test_values():
            got = [compare_versions("1.10", "1.9"), compare_versions("2.0", "2.0"), compare_versions("0.9", "1.0")]
            assert got == [1, 0, -1], f"Получено {got}"
        """,
        """
        def compare_versions(a, b):
            va = tuple(int(p) for p in a.split("."))
            vb = tuple(int(p) for p in b.split("."))
            if va < vb:
                return -1
            if va > vb:
                return 1
            return 0
        """, xp=20),
    cod(f"{P}-strcmp-e2", t("""
        Напиши функцию `equal_ignore_case(a, b)` — равны ли две строки **без учёта регистра**.

        Примеры:
        ```
        equal_ignore_case("Python", "PYTHON")   # → True
        equal_ignore_case("Аня", "аня")         # → True
        equal_ignore_case("ok", "okay")         # → False
        ```
        """),
        """
        def equal_ignore_case(a, b):
            pass
        """,
        """
        def test_values():
            got = [equal_ignore_case("Python", "PYTHON"), equal_ignore_case("Аня", "аня"), equal_ignore_case("ok", "okay")]
            assert got == [True, True, False], f"Получено {got}"
        """,
        """
        def equal_ignore_case(a, b):
            return a.lower() == b.lower()
        """),
    cod(f"{P}-strcmp-e3", t("""
        Напиши функцию `first_alphabetically(a, b)` — какое из двух слов идёт **раньше по алфавиту без учёта регистра**.
        Вернуть само слово, как оно было передано. Если слова равны без учёта регистра — вернуть `a`.

        Примеры:
        ```
        first_alphabetically("banana", "Apple")   # → "Apple"
        first_alphabetically("кот", "Кит")        # → "Кит"
        first_alphabetically("Ok", "ok")          # → "Ok"
        ```
        Без встроенной `min`.
        """),
        """
        def first_alphabetically(a, b):
            pass
        """,
        """
        def test_values():
            got = [first_alphabetically("banana", "Apple"), first_alphabetically("кот", "Кит"), first_alphabetically("Ok", "ok"),
                   first_alphabetically("a", "b")]
            assert got == ["Apple", "Кит", "Ok", "a"], f"Получено {got}"
        """,
        """
        def first_alphabetically(a, b):
            if a.lower() <= b.lower():
                return a
            return b
        """,
        hint="Сравни `a.lower()` и `b.lower()`, а вернуть нужно исходное слово."),
    cod(f"{P}-strcmp-e4", t("""
        Напиши функцию `same_price(a, b)` — равны ли две цены с точностью до копеек.
        Из-за неточности дробных чисел сравнивай **округлённые** до 2 знаков значения.

        Примеры:
        ```
        same_price(0.1 + 0.2, 0.3)   # → True
        same_price(9.99, 9.98)       # → False
        ```
        """),
        """
        def same_price(a, b):
            pass
        """,
        """
        def test_values():
            assert same_price(0.1 + 0.2, 0.3) is True, "0.1 + 0.2 и 0.3 — одна цена"
            assert same_price(9.99, 9.98) is False and same_price(10, 10.0) is True, "Неверное сравнение"
        """,
        """
        def same_price(a, b):
            return round(a, 2) == round(b, 2)
        """),
    cod(f"{P}-strcmp-e5", t("""
        Напиши функцию `text_equals_number(text, number)` — равно ли число, записанное строкой `text`, числу `number`.
        Строка всегда содержит целое число, возможно с пробелами по краям.

        Примеры:
        ```
        text_equals_number("42", 42)     # → True
        text_equals_number(" 7 ", 7)     # → True
        text_equals_number("10", 1)      # → False
        ```
        Помни: строка `"42"` и число `42` не равны — сначала преврати строку в число.
        """),
        """
        def text_equals_number(text, number):
            pass
        """,
        """
        def test_values():
            got = [text_equals_number("42", 42), text_equals_number(" 7 ", 7), text_equals_number("10", 1)]
            assert got == [True, True, False], f"Получено {got}"
        """,
        """
        def text_equals_number(text, number):
            return int(text) == number
        """)),

lesson(f"{P}-m1-l3", "elif — много вариантов",
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        n = 15
        if n > 10:
            print("A")
        elif n > 5:
            print("B")
        else:
            print("C")
        """, hint="Сработает только первая подходящая ветка."),
    out(f"{P}-m1-l3-e2", "Что выведет программа? Здесь два отдельных if.", """
        n = 15
        if n > 10:
            print("A")
        if n > 5:
            print("B")
        """),
    out(f"{P}-m1-l3-e6", "Что выведет программа? Внимательно с границей.", """
        t = 25
        if t < 0:
            print("мороз")
        elif t < 15:
            print("холодно")
        elif t < 25:
            print("тепло")
        else:
            print("жарко")
        """, hint="25 < 25 — ложь."),
    cod(f"{P}-m1-l3-e3", t("""
        Напиши функцию `sign(n)`, которая называет знак числа.

        - `"плюс"` — если больше нуля;
        - `"минус"` — если меньше нуля;
        - `"ноль"` — если равно нулю.

        Примеры:
        ```
        sign(5)    # → "плюс"
        sign(-3)   # → "минус"
        sign(0)    # → "ноль"
        ```
        """),
        """
        def sign(n):
            pass
        """,
        """
        def test_values():
            assert [sign(5), sign(-3), sign(0)] == ["плюс", "минус", "ноль"], "Неверный знак"
        """,
        """
        def sign(n):
            if n > 0:
                return "плюс"
            elif n < 0:
                return "минус"
            return "ноль"
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `grade(score)`, которая переводит баллы (0–100) в оценку:

        - 90 и больше → `"A"`
        - от 75 до 89 → `"B"`
        - от 60 до 74 → `"C"`
        - меньше 60 → `"F"`

        Примеры:
        ```
        grade(95)   # → "A"
        grade(75)   # → "B"
        grade(59)   # → "F"
        ```
        """),
        """
        def grade(score):
            pass
        """,
        """
        def test_values():
            got = [grade(s) for s in (95, 90, 89, 75, 74, 60, 59, 0)]
            assert got == ["A", "A", "B", "B", "C", "C", "F", "F"], f"Получено {got}"
        """,
        """
        def grade(score):
            if score >= 90:
                return "A"
            elif score >= 75:
                return "B"
            elif score >= 60:
                return "C"
            return "F"
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Классика собеседований — FizzBuzz. Напиши функцию `fizzbuzz(n)`, которая возвращает **строку**:

        - `"FizzBuzz"` — если `n` делится и на 3, и на 5;
        - `"Fizz"` — если делится только на 3;
        - `"Buzz"` — если делится только на 5;
        - иначе — само число строкой: `str(n)`.

        Примеры:
        ```
        fizzbuzz(9)    # → "Fizz"
        fizzbuzz(10)   # → "Buzz"
        fizzbuzz(30)   # → "FizzBuzz"
        fizzbuzz(7)    # → "7"
        ```
        """),
        """
        def fizzbuzz(n):
            pass
        """,
        """
        def test_values():
            got = [fizzbuzz(n) for n in (9, 10, 30, 7, 15)]
            assert got == ["Fizz", "Buzz", "FizzBuzz", "7", "FizzBuzz"], f"Получено {got} — проверь порядок условий"
        """,
        """
        def fizzbuzz(n):
            if n % 15 == 0:
                return "FizzBuzz"
            elif n % 3 == 0:
                return "Fizz"
            elif n % 5 == 0:
                return "Buzz"
            return str(n)
        """,
        hint="Проверку «на 3 и 5 одновременно» (`n % 15 == 0`) ставь первой.", xp=20),
    cod(f"{P}-m1-l3-e7", t("""
        Напиши функцию `http_class(code)` — класс HTTP-ответа по коду:

        - 200–299 → `"успех"`
        - 300–399 → `"перенаправление"`
        - 400–499 → `"ошибка клиента"`
        - 500–599 → `"ошибка сервера"`
        - любой другой → `"неизвестно"`

        Примеры:
        ```
        http_class(200)   # → "успех"
        http_class(404)   # → "ошибка клиента"
        http_class(503)   # → "ошибка сервера"
        http_class(99)    # → "неизвестно"
        ```
        """),
        """
        def http_class(code):
            pass
        """,
        """
        def test_values():
            got = [http_class(c) for c in (200, 299, 301, 404, 499, 503, 599, 99, 600)]
            assert got == ["успех", "успех", "перенаправление", "ошибка клиента", "ошибка клиента",
                           "ошибка сервера", "ошибка сервера", "неизвестно", "неизвестно"], f"Получено {got}"
        """,
        """
        def http_class(code):
            if 200 <= code <= 299:
                return "успех"
            elif 300 <= code <= 399:
                return "перенаправление"
            elif 400 <= code <= 499:
                return "ошибка клиента"
            elif 500 <= code <= 599:
                return "ошибка сервера"
            return "неизвестно"
        """),
    cod(f"{P}-m1-l3-e8", t("""
        Напиши функцию `season(month)` — время года по номеру месяца (1–12):

        - 3, 4, 5 → `"весна"`
        - 6, 7, 8 → `"лето"`
        - 9, 10, 11 → `"осень"`
        - 12, 1, 2 → `"зима"`

        Примеры:
        ```
        season(4)    # → "весна"
        season(12)   # → "зима"
        season(1)    # → "зима"
        ```
        Подсказка: проверь весну, лето и осень диапазонами, а зиму оставь для `else`.
        """),
        """
        def season(month):
            pass
        """,
        """
        def test_values():
            got = [season(m) for m in range(1, 13)]
            assert got == ["зима", "зима", "весна", "весна", "весна", "лето", "лето", "лето",
                           "осень", "осень", "осень", "зима"], f"Получено {got}"
        """,
        """
        def season(month):
            if 3 <= month <= 5:
                return "весна"
            elif 6 <= month <= 8:
                return "лето"
            elif 9 <= month <= 11:
                return "осень"
            else:
                return "зима"
        """)),

lesson(f"{P}-bounds", "Границы и диапазоны",
    out(f"{P}-bounds-e1", "Что выведет программа?", """
        age = 18
        if age > 18:
            print("A")
        elif age == 18:
            print("B")
        else:
            print("C")
        """),
    out(f"{P}-bounds-e2", "Что выведет программа? Строгие и нестрогие границы.", """
        score = 90
        print(score > 90, score >= 90)
        print(80 < score < 90, 80 < score <= 90)
        """),
    out(f"{P}-bounds-e3", "Что выведет программа? Полуоткрытые диапазоны.", """
        x = 100
        if 0 <= x < 100:
            print("меньше 100")
        elif 100 <= x < 1000:
            print("трёхзначное")
        else:
            print("большое")
        """, hint="`0 <= x < 100` — от 0 включительно до 100 НЕ включительно."),
    cod(f"{P}-bounds-e4", t("""
        Напиши функцию `discount(total)` — скидка в процентах по сумме заказа:

        - меньше 1000 → `0`
        - от 1000 до 4999 включительно → `5`
        - 5000 и больше → `10`

        Проверь себя на границах: 999, 1000, 4999, 5000.
        """),
        """
        def discount(total):
            pass
        """,
        """
        def test_boundaries():
            got = [discount(t) for t in (0, 999, 1000, 4999, 5000, 100000)]
            assert got == [0, 0, 5, 5, 10, 10], f"Для 0, 999, 1000, 4999, 5000, 100000 получено {got}"
        """,
        """
        def discount(total):
            if total < 1000:
                return 0
            elif total < 5000:
                return 5
            return 10
        """),
    cod(f"{P}-bounds-e5", t("""
        Напиши функцию `shipping_cost(weight)` — стоимость доставки по весу посылки в кг:

        - больше 0 и до 1 включительно → `300`
        - больше 1 и до 5 включительно → `500`
        - больше 5 и до 20 включительно → `1000`
        - иначе (0, отрицательный или больше 20) → `-1` (посылку не принимаем)

        Примеры:
        ```
        shipping_cost(0.5)   # → 300
        shipping_cost(1)     # → 300
        shipping_cost(1.1)   # → 500
        shipping_cost(20)    # → 1000
        shipping_cost(0)     # → -1
        ```
        """),
        """
        def shipping_cost(weight):
            pass
        """,
        """
        def test_values():
            got = [shipping_cost(w) for w in (0.5, 1, 1.1, 5, 5.5, 20, 20.1, 0, -3)]
            assert got == [300, 300, 500, 500, 1000, 1000, -1, -1, -1], f"Получено {got}"
        """,
        """
        def shipping_cost(weight):
            if 0 < weight <= 1:
                return 300
            elif 1 < weight <= 5:
                return 500
            elif 5 < weight <= 20:
                return 1000
            return -1
        """),
    cod(f"{P}-bounds-e6", t("""
        Напиши функцию `speed_fine(speed, limit)` — штраф за превышение скорости. Превышение = `speed - limit`:

        - до 20 включительно (или скорость не превышена) → `0`
        - больше 20 и до 40 включительно → `500`
        - больше 40 и до 60 включительно → `1500`
        - больше 60 → `5000`

        Примеры:
        ```
        speed_fine(80, 60)    # → 0      превышение 20
        speed_fine(81, 60)    # → 500
        speed_fine(100, 60)   # → 500    превышение 40
        speed_fine(125, 60)   # → 5000
        ```
        """),
        """
        def speed_fine(speed, limit):
            pass
        """,
        """
        def test_values():
            got = [speed_fine(s, 60) for s in (50, 80, 81, 100, 101, 120, 121)]
            assert got == [0, 0, 500, 500, 1500, 1500, 5000], f"Для 50, 80, 81, 100, 101, 120, 121 получено {got}"
        """,
        """
        def speed_fine(speed, limit):
            over = speed - limit
            if over <= 20:
                return 0
            elif over <= 40:
                return 500
            elif over <= 60:
                return 1500
            return 5000
        """, xp=20),
    cod(f"{P}-bounds-e7", t("""
        Функция `is_valid_percent(p)` должна принимать проценты **от 0 до 100 включительно**, но отвергает сами `0` и `100`.
        Найди ошибку на границах и исправь.
        """),
        """
        def is_valid_percent(p):
            return 0 < p < 100
        """,
        """
        def test_values():
            got = [is_valid_percent(p) for p in (0, 50, 100, -1, 101)]
            assert got == [True, True, True, False, False], f"Для 0, 50, 100, -1, 101 получено {got}"
        """,
        """
        def is_valid_percent(p):
            return 0 <= p <= 100
        """,
        hint="Строгое `<` не включает границу; нужно `<=`."),
    cod(f"{P}-bounds-e8", t("""
        Напиши функцию `age_group(age)`:

        - отрицательный возраст → `"ошибка"`
        - 0–12 → `"ребёнок"`
        - 13–17 → `"подросток"`
        - 18–64 → `"взрослый"`
        - 65 и больше → `"пенсионер"`
        """),
        """
        def age_group(age):
            pass
        """,
        """
        def test_values():
            got = [age_group(a) for a in (-1, 0, 12, 13, 17, 18, 64, 65, 100)]
            assert got == ["ошибка", "ребёнок", "ребёнок", "подросток", "подросток", "взрослый", "взрослый",
                           "пенсионер", "пенсионер"], f"Получено {got}"
        """,
        """
        def age_group(age):
            if age < 0:
                return "ошибка"
            elif age <= 12:
                return "ребёнок"
            elif age <= 17:
                return "подросток"
            elif age <= 64:
                return "взрослый"
            return "пенсионер"
        """)),
)
