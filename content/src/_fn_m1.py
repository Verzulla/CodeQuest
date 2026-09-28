"""Тема «Функции», модуль 1 «Основы функций» — задания. Теория — в _fn_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "fn"

m1 = module(f"{P}-m1", "Основы функций", "🧰", "def и вызов, порядок в программе, параметры, ошибки вызова, return",

lesson(f"{P}-m1-l1", "def и вызов функции",
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        def hello():
            print("Привет!")

        print("до")
        hello()
        hello()
        print("после")
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа? Функцию объявили, но…", """
        def boom():
            print("бум")

        print("старт")
        boom
        print("финиш")
        """, hint="Без скобок функция не вызывается — это просто обращение к объекту."),
    out(f"{P}-m1-l1-e6", "Что выведет программа? Результат функции — обычное значение.", """
        def greet(name):
            return "Привет, " + name

        msg = greet("Аня")
        print(msg.upper())
        print(len(greet("Bob")))
        """),
    cod(f"{P}-m1-l1-e3", t("""
        Напиши функцию `square(x)`, которая возвращает квадрат числа.

        Примеры:
        ```
        square(3)    # → 9
        square(-4)   # → 16
        ```
        """),
        "",
        """
        def test_values():
            assert square(3) == 9 and square(-4) == 16 and square(0) == 0, "Неверный квадрат"
        """,
        """
        def square(x):
            return x * x
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `separator()` **без параметров**, которая возвращает строку из 20 символов `-`.

        Затем **вызови её дважды** и выведи результат каждого вызова через `print`.

        Ожидаемый вывод:
        ```
        --------------------
        --------------------
        ```
        """),
        "",
        """
        def test_function():
            assert separator() == "-" * 20, "separator() должна вернуть 20 дефисов"

        def test_output():
            assert OUTPUT.split() == ["-" * 20] * 2, f"Напечатано {OUTPUT!r}"
        """,
        """
        def separator():
            return "-" * 20

        print(separator())
        print(separator())
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `celsius_to_fahrenheit(c)` — перевод температуры: `F = C * 9 / 5 + 32`.

        Примеры:
        ```
        celsius_to_fahrenheit(0)     # → 32.0
        celsius_to_fahrenheit(100)   # → 212.0
        celsius_to_fahrenheit(-40)   # → -40.0
        ```
        """),
        """
        def celsius_to_fahrenheit(c):
            pass
        """,
        """
        def test_values():
            got = [celsius_to_fahrenheit(c) for c in (0, 100, -40)]
            assert got == [32.0, 212.0, -40.0], f"Получено {got}"
        """,
        """
        def celsius_to_fahrenheit(c):
            return c * 9 / 5 + 32
        """),
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `is_even(n)`, которая возвращает `True` для чётного числа и `False` для нечётного.

        Примеры:
        ```
        is_even(4)   # → True
        is_even(7)   # → False
        ```
        """),
        "",
        """
        def test_values():
            got = [is_even(4), is_even(7), is_even(0), is_even(-3)]
            assert got == [True, False, True, False], f"Получено {got}"
        """,
        """
        def is_even(n):
            return n % 2 == 0
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `full_price(price, qty)` — стоимость `qty` штук товара по цене `price`.
        Затем **вызови** её для цены 150 и количества 3 и **выведи** результат.

        Ожидаемый вывод:
        ```
        450
        ```
        """),
        "",
        """
        def test_function():
            assert full_price(10, 2) == 20 and full_price(99, 0) == 0, "Неверная стоимость"

        def test_output():
            assert OUTPUT.strip() == "450", f"Напечатано {OUTPUT.strip()!r}"
        """,
        """
        def full_price(price, qty):
            return price * qty

        print(full_price(150, 3))
        """)),

lesson(f"{P}-order", "Тело функции и порядок в программе",
    out(f"{P}-order-e1", "Что выведет программа? Функция вызывает другую.", """
        def a():
            print("A")
            b()

        def b():
            print("B")

        a()
        print("конец")
        """, hint="К моменту вызова a() обе функции уже определены."),
    out(f"{P}-order-e2", "Что выведет программа? Определение ничего не выполняет.", """
        def f():
            print("внутри f")

        print("до")
        x = f
        print("после")
        """),
    out(f"{P}-order-e3", "Что выведет программа? Пустые функции.", """
        def stub():
            pass

        def todo():
            ...

        print(stub(), todo())
        """, hint="`pass` и `...` — пустое тело; функция без return возвращает None."),
    cod(f"{P}-order-e4", t("""
        Программа падает с `NameError: name 'greet' is not defined`: функцию вызывают **раньше**, чем определили.
        Исправь порядок, чтобы программа вывела:
        ```
        Привет, Аня
        ```
        """),
        """
        print(greet("Аня"))

        def greet(name):
            return "Привет, " + name
        """,
        """
        def test_output():
            assert OUTPUT.strip() == "Привет, Аня", f"Напечатано {OUTPUT.strip()!r}"
        """,
        """
        def greet(name):
            return "Привет, " + name

        print(greet("Аня"))
        """,
        hint="Сначала `def`, потом вызов."),
    cod(f"{P}-order-e5", t("""
        Напиши две функции:
        - `double(x)` — удвоенное число;
        - `quadruple(x)` — учетверённое число, которая **использует** `double` (дважды).

        Примеры:
        ```
        double(3)      # → 6
        quadruple(3)   # → 12
        ```
        """),
        "",
        """
        import inspect

        def test_values():
            assert double(3) == 6 and quadruple(3) == 12 and quadruple(-1) == -4, "Неверный результат"

        def test_uses_double():
            src = inspect.getsource(quadruple)
            assert "double(" in src, "quadruple должна вызывать double"
        """,
        """
        def double(x):
            return x * 2

        def quadruple(x):
            return double(double(x))
        """),
    cod(f"{P}-order-e6", t("""
        Напиши функцию `banner(text)`, которая **печатает** текст в рамке из звёздочек: `*** текст ***`.
        Возвращать ничего не нужно.

        Пример: `banner("hi")` печатает
        ```
        *** hi ***
        ```
        """),
        """
        def banner(text):
            pass
        """,
        """
        def test_print():
            assert capture(banner, "hi") == "*** hi ***\\n", f"Напечатано {capture(banner, 'hi')!r}"

        def test_returns_none():
            assert banner("x") is None, "Функция только печатает, return не нужен"
        """,
        """
        def banner(text):
            print("***", text, "***")
        """),
    cod(f"{P}-order-e7", t("""
        Напиши функцию `say_n_times(text, n)`, которая печатает `text` ровно `n` раз, каждый раз с новой строки.

        Пример: `say_n_times("ура", 2)` печатает
        ```
        ура
        ура
        ```
        """),
        """
        def say_n_times(text, n):
            pass
        """,
        """
        def test_print():
            assert capture(say_n_times, "ура", 2) == "ура\\nура\\n", f"Напечатано {capture(say_n_times, 'ура', 2)!r}"
            assert capture(say_n_times, "x", 0) == "", "При n = 0 ничего не печатать"
        """,
        """
        def say_n_times(text, n):
            for _ in range(n):
                print(text)
        """),
    cod(f"{P}-order-e8", t("""
        Напиши функцию `max2(a, b)` — большее из двух чисел (без встроенной `max`),
        и функцию `max3(a, b, c)` — большее из трёх, которая **использует** `max2`.

        Примеры:
        ```
        max2(3, 7)       # → 7
        max3(3, 9, 5)    # → 9
        ```
        """),
        "",
        """
        import inspect

        def test_values():
            assert max2(3, 7) == 7 and max2(7, 3) == 7 and max3(3, 9, 5) == 9 and max3(-1, -5, -3) == -1, "Неверный максимум"

        def test_no_builtin():
            src = inspect.getsource(max2) + inspect.getsource(max3)
            assert "max(" not in src.replace("max2(", "").replace("max3(", ""), "Без встроенной max"
            assert "max2(" in inspect.getsource(max3), "max3 должна использовать max2"
        """,
        """
        def max2(a, b):
            if a > b:
                return a
            return b

        def max3(a, b, c):
            return max2(max2(a, b), c)
        """)),

lesson(f"{P}-m1-l2", "Параметры и аргументы",
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        def power(base, exp):
            return base ** exp

        print(power(2, 3), power(3, 2))
        print(power(exp=2, base=5))
        """, hint="Для позиционных аргументов порядок важен, для именованных — нет."),
    out(f"{P}-m1-l2-e2", "Что выведет программа?", """
        def describe(name, role):
            return f"{name} — {role}"

        print(describe("Аня", "QA"))
        print(describe(role="QA", name="Боря"))
        try:
            describe("Вика")
        except TypeError:
            print("не хватает аргумента")
        """),
    out(f"{P}-m1-l2-e6", "Что выведет программа? Порядок позиционных аргументов.", """
        def sub(a, b):
            return a - b

        print(sub(10, 3), sub(3, 10))
        print(sub(b=10, a=3))
        """),
    cod(f"{P}-m1-l2-e3", t("""
        Напиши функцию `rectangle_area(width, height)` — площадь прямоугольника.

        Примеры:
        ```
        rectangle_area(3, 4)                  # → 12
        rectangle_area(height=2, width=10)    # → 20
        ```
        """),
        """
        def rectangle_area(width, height):
            pass
        """,
        """
        def test_values():
            assert rectangle_area(3, 4) == 12 and rectangle_area(height=2, width=10) == 20, "Неверная площадь"
        """,
        """
        def rectangle_area(width, height):
            return width * height
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `format_user(name, age, city)`, которая возвращает строку `"<имя>, <возраст> лет, <город>"`.

        Затем **вызови её с именованными аргументами** в порядке `city`, `name`, `age` для данных: Аня, 25, Казань — и выведи результат.

        Ожидаемый вывод:
        ```
        Аня, 25 лет, Казань
        ```
        """),
        "",
        """
        def test_function():
            assert format_user("Боря", 30, "Сочи") == "Боря, 30 лет, Сочи", "Неверный формат строки"

        def test_output():
            assert OUTPUT.strip() == "Аня, 25 лет, Казань", f"Напечатано {OUTPUT.strip()!r}"

        def test_keywords():
            src = open("solution.py", encoding="utf-8").read()
            assert "city=" in src and "name=" in src and "age=" in src, "Вызови функцию с именованными аргументами"
        """,
        """
        def format_user(name, age, city):
            return f"{name}, {age} лет, {city}"

        print(format_user(city="Казань", name="Аня", age=25))
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `discount_price(price, percent)` — цена со скидкой в процентах, округлённая до 2 знаков.

        Примеры:
        ```
        discount_price(1000, 15)    # → 850.0
        discount_price(99.9, 10)    # → 89.91
        discount_price(500, 0)      # → 500.0
        ```
        """),
        """
        def discount_price(price, percent):
            pass
        """,
        """
        def test_values():
            got = [discount_price(1000, 15), discount_price(99.9, 10), discount_price(500, 0)]
            assert got == [850.0, 89.91, 500.0], f"Получено {got}"
        """,
        """
        def discount_price(price, percent):
            return round(price * (1 - percent / 100), 2)
        """),
    cod(f"{P}-m1-l2-e7", t("""
        Напиши функцию `bmi(weight, height)` — индекс массы тела: вес (кг), делённый на квадрат роста (м), округлённый до 1 знака.

        Примеры:
        ```
        bmi(70, 1.75)              # → 22.9
        bmi(height=1.6, weight=50) # → 19.5
        ```
        """),
        """
        def bmi(weight, height):
            pass
        """,
        """
        def test_values():
            assert bmi(70, 1.75) == 22.9 and bmi(height=1.6, weight=50) == 19.5, f"Получено {bmi(70, 1.75)!r}"
        """,
        """
        def bmi(weight, height):
            return round(weight / height ** 2, 1)
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши функцию `mix(a, b)`, которая возвращает строку `"<a>-<b>"`.
        Затем вызови её **с именованными аргументами, записанными в порядке `b`, потом `a`**, для `a = "1"`, `b = "2"` и выведи результат.

        Ожидаемый вывод:
        ```
        1-2
        ```
        """),
        "",
        """
        def test_function():
            assert mix("x", "y") == "x-y", "Неверная строка"

        def test_output():
            assert OUTPUT.strip() == "1-2", f"Напечатано {OUTPUT.strip()!r}"

        def test_keywords():
            src = open("solution.py", encoding="utf-8").read().replace(" ", "")
            assert 'mix(b="2",a="1")' in src or "mix(b='2',a='1')" in src, "Вызови mix(b=..., a=...)"
        """,
        """
        def mix(a, b):
            return f"{a}-{b}"

        print(mix(b="2", a="1"))
        """)),

lesson(f"{P}-argerr", "Ошибки при вызове и порядок аргументов",
    out(f"{P}-argerr-e1", "Что выведет программа? Сколько аргументов передали.", """
        def f(a, b):
            return a + b

        try:
            f(1)
        except TypeError as e:
            print(e)
        try:
            f(1, 2, 3)
        except TypeError as e:
            print(e)
        """),
    out(f"{P}-argerr-e2", "Что выведет программа? Ошибки с именованными аргументами.", """
        def f(a, b):
            return a + b

        try:
            f(1, a=2)
        except TypeError as e:
            print(e)
        try:
            f(1, c=2)
        except TypeError as e:
            print(e)
        """),
    out(f"{P}-argerr-e3", "Что выведет программа? Параметр только по имени.", """
        def connect(host, *, timeout=5):
            return f"{host}:{timeout}"

        print(connect("db"), connect("db", timeout=1))
        try:
            connect("db", 1)
        except TypeError:
            print("timeout — только по имени")
        """),
    cod(f"{P}-argerr-e4", t("""
        Программа не запускается: `SyntaxError: positional argument follows keyword argument` —
        позиционный аргумент стоит после именованного. Исправь вызов, чтобы программа вывела `6`.
        """),
        """
        def area(w, h):
            return w * h

        print(area(w=2, 3))
        """,
        """
        def test_output():
            assert OUTPUT.strip() == "6", f"Напечатано {OUTPUT.strip()!r}"
        """,
        """
        def area(w, h):
            return w * h

        print(area(w=2, h=3))
        """,
        hint="Либо `area(2, 3)`, либо `area(2, h=3)`, либо `area(w=2, h=3)`."),
    cod(f"{P}-argerr-e5", t("""
        Напиши функцию `make_user(name, *, admin=False)`, где `admin` можно передать **только по имени**.
        Функция возвращает пару `(name, admin)`.

        Примеры:
        ```
        make_user("Аня")               # → ("Аня", False)
        make_user("Боря", admin=True)  # → ("Боря", True)
        make_user("Вика", True)        # TypeError
        ```
        """),
        """
        def make_user(name, admin=False):
            return name, admin
        """,
        """
        def test_values():
            assert make_user("Аня") == ("Аня", False) and make_user("Боря", admin=True) == ("Боря", True), "Неверный результат"

        def test_keyword_only():
            try:
                make_user("Вика", True)
            except TypeError:
                return
            assert False, "admin должен передаваться только по имени"
        """,
        """
        def make_user(name, *, admin=False):
            return name, admin
        """,
        hint="Звёздочка `*` в списке параметров: всё после неё — только по имени."),
    cod(f"{P}-argerr-e6", t("""
        Напиши функцию `clamp(x, low, high, /)`, где все параметры можно передать **только по позиции** (не по имени).
        Функция зажимает `x` в границы `[low, high]`.

        Примеры:
        ```
        clamp(15, 0, 10)          # → 10
        clamp(x=15, low=0, high=10)   # TypeError
        ```
        """),
        """
        def clamp(x, low, high):
            return max(low, min(x, high))
        """,
        """
        def test_values():
            assert clamp(15, 0, 10) == 10 and clamp(-5, 0, 10) == 0 and clamp(5, 0, 10) == 5, "Неверный результат"

        def test_positional_only():
            try:
                clamp(x=15, low=0, high=10)
            except TypeError:
                return
            assert False, "Параметры должны быть только позиционными"
        """,
        """
        def clamp(x, low, high, /):
            return max(low, min(x, high))
        """,
        hint="Косая черта `/` после параметров: всё до неё — только по позиции."),
    cod(f"{P}-argerr-e7", t("""
        Напиши функцию `safe_call(func, a, b)`: вызвать `func(a, b)` и вернуть результат, а если вызов
        упал с `TypeError` (неподходящие аргументы) — вернуть строку `"ошибка вызова"`.

        Примеры:
        ```
        def add(x, y):
            return x + y

        safe_call(add, 2, 3)     # → 5
        safe_call(add, 2, "3")   # → "ошибка вызова"   int + str
        safe_call(len, 1, 2)     # → "ошибка вызова"   len принимает один аргумент
        ```
        """),
        """
        def safe_call(func, a, b):
            pass
        """,
        """
        def test_values():
            def add(x, y):
                return x + y
            got = [safe_call(add, 2, 3), safe_call(add, 2, "3"), safe_call(len, 1, 2), safe_call(pow, 2, 3)]
            assert got == [5, "ошибка вызова", "ошибка вызова", 8], f"Получено {got}"
        """,
        """
        def safe_call(func, a, b):
            try:
                return func(a, b)
            except TypeError:
                return "ошибка вызова"
        """),
    cod(f"{P}-argerr-e8", t("""
        Функция `greet(name, greeting)` вызывается с аргументами, перепутанными местами, и выводит `"Аня, Привет!"`.
        Исправь **вызов** (не функцию), используя именованные аргументы, чтобы программа вывела:
        ```
        Привет, Аня!
        ```
        """),
        """
        def greet(name, greeting):
            return f"{greeting}, {name}!"

        print(greet("Привет", "Аня"))
        """,
        """
        def test_output():
            assert OUTPUT.strip() == "Привет, Аня!", f"Напечатано {OUTPUT.strip()!r}"

        def test_function_unchanged():
            assert greet("X", "Y") == "Y, X!", "Функцию менять не нужно — только вызов"
        """,
        """
        def greet(name, greeting):
            return f"{greeting}, {name}!"

        print(greet(greeting="Привет", name="Аня"))
        """)),

lesson(f"{P}-m1-l3", "return против print, None",
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        def shows(x):
            print(x * 2)

        def gives(x):
            return x * 2

        a = shows(5)
        b = gives(5)
        print(a, b)
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа? Код после return не выполняется.", """
        def check(n):
            if n < 0:
                return "отрицательное"
            return "неотрицательное"
            print("это не выполнится")

        print(check(-1), check(3))
        """),
    out(f"{P}-m1-l3-e6", "Что выведет программа? Пустой return.", """
        def f():
            return

        def g():
            pass

        print(f(), g(), f() == g())
        """),
    cod(f"{P}-m1-l3-e3", t("""
        В функции `total(prices)` ошибка: она **печатает** сумму вместо того, чтобы её **вернуть**, поэтому `result` получается `None`.

        Исправь функцию, чтобы она возвращала сумму и ничего не печатала.

        Пример:
        ```
        total([100, 250, 50])   # → 400
        ```
        """),
        """
        def total(prices):
            s = 0
            for p in prices:
                s += p
            print(s)
        """,
        """
        def test_returns():
            assert total([100, 250, 50]) == 400 and total([]) == 0, "Функция должна вернуть сумму"

        def test_no_print():
            assert capture(total, [1, 2]) == "", "Функция не должна ничего печатать"
        """,
        """
        def total(prices):
            s = 0
            for p in prices:
                s += p
            return s
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `find_negative(nums)` — вернуть **первое** отрицательное число списка, а если таких нет — `None`.

        Используй `return` внутри цикла, чтобы выйти сразу, как только нашлось число.

        Примеры:
        ```
        find_negative([3, -1, -5])   # → -1
        find_negative([1, 2])        # → None
        ```
        """),
        """
        def find_negative(nums):
            pass
        """,
        """
        def test_values():
            assert find_negative([3, -1, -5]) == -1 and find_negative([1, 2]) is None and find_negative([]) is None, "Неверный результат"
        """,
        """
        def find_negative(nums):
            for n in nums:
                if n < 0:
                    return n
            return None
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `report(passed, failed)`, которая **возвращает** строку отчёта (а не печатает её):

        - если упавших нет → `"Все <passed> тестов прошли"`;
        - иначе → `"Прошло: <passed>, упало: <failed>"`.

        Затем **выведи** результат вызова `report(10, 0)` через `print`.

        Ожидаемый вывод:
        ```
        Все 10 тестов прошли
        ```
        """),
        "",
        """
        def test_returns():
            assert report(10, 0) == "Все 10 тестов прошли" and report(8, 2) == "Прошло: 8, упало: 2", "Неверная строка отчёта"

        def test_function_does_not_print():
            assert capture(report, 1, 1) == "", "report должна возвращать строку, а не печатать"

        def test_output():
            assert OUTPUT.strip() == "Все 10 тестов прошли", f"Напечатано {OUTPUT.strip()!r}"
        """,
        """
        def report(passed, failed):
            if failed == 0:
                return f"Все {passed} тестов прошли"
            return f"Прошло: {passed}, упало: {failed}"

        print(report(10, 0))
        """),
    cod(f"{P}-m1-l3-e7", t("""
        Функция `total(prices)` должна вернуть сумму **всех** цен, но возвращает только первую: `return` стоит не на том уровне отступа.
        Исправь.

        Пример:
        ```
        total([1, 2, 3])   # → 6
        ```
        """),
        """
        def total(prices):
            s = 0
            for p in prices:
                s += p
                return s
        """,
        """
        def test_values():
            assert total([1, 2, 3]) == 6 and total([5]) == 5, f"total([1, 2, 3]) вернула {total([1, 2, 3])!r}"
            assert total([]) == 0, "Для пустого списка — 0, а не None"
        """,
        """
        def total(prices):
            s = 0
            for p in prices:
                s += p
            return s
        """,
        hint="`return` внутри цикла завершает функцию на первом шаге. Сдвинь его на уровень `for`."),
    cod(f"{P}-m1-l3-e8", t("""
        Напиши функцию `doubled(nums)`, которая **возвращает** новый список удвоенных чисел и ничего не печатает.

        Пример:
        ```
        doubled([1, 2, 3])   # → [2, 4, 6]
        ```
        """),
        """
        def doubled(nums):
            pass
        """,
        """
        def test_values():
            assert doubled([1, 2, 3]) == [2, 4, 6] and doubled([]) == [], "Неверный результат"

        def test_no_print():
            assert capture(doubled, [1]) == "", "Функция не должна печатать"
        """,
        """
        def doubled(nums):
            result = []
            for n in nums:
                result.append(n * 2)
            return result
        """)),

lesson(f"{P}-return", "return: ранний выход и несколько return",
    out(f"{P}-return-e1", "Что выведет программа?", """
        def classify(n):
            if n < 0:
                return "минус"
            if n == 0:
                return "ноль"
            return "плюс"

        print(classify(-5), classify(0), classify(7))
        """),
    out(f"{P}-return-e2", "Что выведет программа? return внутри цикла.", """
        def find(items, x):
            for i, v in enumerate(items):
                if v == x:
                    return i
            return -1

        print(find(["a", "b", "c"], "b"), find(["a"], "z"))
        """),
    out(f"{P}-return-e3", "Что выведет программа? Пустой return как «выйти».", """
        def process(x):
            if x is None:
                return
            print("обработка", x)

        process(None)
        process(5)
        print(process(1))
        """),
    cod(f"{P}-return-e4", t("""
        Напиши функцию `first_long_word(words, n)` — первое слово длиннее `n` символов, или `None`, если такого нет.
        Выходи из функции сразу, как только слово найдено.

        Примеры:
        ```
        first_long_word(["кот", "собака", "лошадь"], 4)   # → "собака"
        first_long_word(["да"], 5)                        # → None
        ```
        """),
        """
        def first_long_word(words, n):
            pass
        """,
        """
        def test_values():
            got = [first_long_word(["кот", "собака", "лошадь"], 4), first_long_word(["да"], 5), first_long_word([], 1)]
            assert got == ["собака", None, None], f"Получено {got}"
        """,
        """
        def first_long_word(words, n):
            for w in words:
                if len(w) > n:
                    return w
            return None
        """),
    cod(f"{P}-return-e5", t("""
        Напиши функцию `check_age(age)` с **ранними выходами**:

        - не целое число (`int`) → `"ошибка: не число"`
        - меньше 0 → `"ошибка: отрицательный"`
        - больше 150 → `"ошибка: слишком большой"`
        - иначе → `"ok"`

        Примеры:
        ```
        check_age("20")   # → "ошибка: не число"
        check_age(-1)     # → "ошибка: отрицательный"
        check_age(30)     # → "ok"
        ```
        """),
        """
        def check_age(age):
            pass
        """,
        """
        def test_values():
            got = [check_age("20"), check_age(2.5), check_age(-1), check_age(151), check_age(0), check_age(150)]
            assert got == ["ошибка: не число", "ошибка: не число", "ошибка: отрицательный", "ошибка: слишком большой", "ok", "ok"], f"Получено {got}"
        """,
        """
        def check_age(age):
            if not isinstance(age, int):
                return "ошибка: не число"
            if age < 0:
                return "ошибка: отрицательный"
            if age > 150:
                return "ошибка: слишком большой"
            return "ok"
        """),
    cod(f"{P}-return-e6", t("""
        Напиши функцию `contains_digit(s)` — есть ли в строке хотя бы одна цифра. Как только нашёл цифру —
        сразу `return True`; если цикл закончился — `False`. Без `any`.

        Примеры:
        ```
        contains_digit("abc1")   # → True
        contains_digit("abc")    # → False
        ```
        """),
        """
        def contains_digit(s):
            pass
        """,
        """
        def test_values():
            got = [contains_digit("abc1"), contains_digit("abc"), contains_digit(""), contains_digit("9")]
            assert got == [True, False, False, True], f"Получено {got}"

        def test_no_any():
            src = open("solution.py", encoding="utf-8").read()
            assert "any(" not in src, "Реши циклом с ранним return"
        """,
        """
        def contains_digit(s):
            for ch in s:
                if ch.isdigit():
                    return True
            return False
        """),
    cod(f"{P}-return-e7", t("""
        Функция `is_positive(n)` иногда возвращает `None` вместо `False`: в одной из веток нет `return`.
        Исправь, чтобы она **всегда** возвращала `True` или `False`.
        """),
        """
        def is_positive(n):
            if n > 0:
                return True
        """,
        """
        def test_values():
            got = [is_positive(5), is_positive(-1), is_positive(0)]
            assert got == [True, False, False], f"Получено {got!r}"
        """,
        """
        def is_positive(n):
            if n > 0:
                return True
            return False
        """,
        hint="Короче всего: `return n > 0`."),
    cod(f"{P}-return-e8", t("""
        Напиши функцию `safe_divide(a, b)`: если `b == 0` — сразу вернуть `None`, иначе вернуть `a / b`.

        Примеры:
        ```
        safe_divide(10, 4)   # → 2.5
        safe_divide(1, 0)    # → None
        ```
        """),
        """
        def safe_divide(a, b):
            pass
        """,
        """
        def test_values():
            assert safe_divide(10, 4) == 2.5 and safe_divide(1, 0) is None and safe_divide(0, 5) == 0, "Неверный результат"
        """,
        """
        def safe_divide(a, b):
            if b == 0:
                return None
            return a / b
        """)),
)
