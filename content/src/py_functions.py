"""Тема «Функции»."""
from ._lib import cod, lesson, module, out, t, topic

P = "fn"

# ============================================================
m1 = module(f"{P}-m1", "Основы функций", "🧰", "def, параметры, return",

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
        """)),
)

# ============================================================
m2 = module(f"{P}-m2", "Параметры по-взрослому", "⚙️", "Значения по умолчанию, несколько результатов, аннотации",

lesson(f"{P}-m2-l1", "Значения по умолчанию", 
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        def greet(name, greeting="Привет"):
            return f"{greeting}, {name}!"

        print(greet("Аня"))
        print(greet("Боря", "Здравствуй"))
        print(greet(greeting="Хай", name="Вика"))
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа? Знаменитая ловушка.", """
        def add_item(item, items=[]):
            items.append(item)
            return items

        print(add_item("a"))
        print(add_item("b"))
        """, hint="Список по умолчанию создаётся один раз при объявлении функции и переиспользуется."),
    cod(f"{P}-m2-l1-e3", t("""
        Напиши функцию `make_url(path, host="localhost", port=8000)`, которая возвращает `"http://<host>:<port><path>"`.

        Примеры:
        ```
        make_url("/api")                          # → "http://localhost:8000/api"
        make_url("/api", port=9000)               # → "http://localhost:9000/api"
        make_url("/", host="staging", port=80)    # → "http://staging:80/"
        ```
        """),
        """
        def make_url(path, host="localhost", port=8000):
            pass
        """,
        """
        def test_values():
            got = [make_url("/api"), make_url("/api", port=9000), make_url("/", host="staging", port=80)]
            assert got == ["http://localhost:8000/api", "http://localhost:9000/api", "http://staging:80/"], f"Получено {got}"
        """,
        """
        def make_url(path, host="localhost", port=8000):
            return f"http://{host}:{port}{path}"
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Исправь функцию `add_tag(tag, tags=[])` — у неё ловушка изменяемого значения по умолчанию: теги «копятся» между вызовами.

        Должно быть так:
        ```
        add_tag("smoke")              # → ["smoke"]
        add_tag("regress")            # → ["regress"]      (а не ["smoke", "regress"])
        add_tag("api", ["ui"])        # → ["ui", "api"]
        ```
        Используй `tags=None` и создавай новый список внутри функции.
        """),
        """
        def add_tag(tag, tags=[]):
            tags.append(tag)
            return tags
        """,
        """
        def test_independent_calls():
            assert add_tag("smoke") == ["smoke"], "Первый вызов — ['smoke']"
            assert add_tag("regress") == ["regress"], "Второй вызов не должен помнить первый"

        def test_given_list():
            assert add_tag("api", ["ui"]) == ["ui", "api"], "Переданный список дополняется"
        """,
        """
        def add_tag(tag, tags=None):
            if tags is None:
                tags = []
            tags.append(tag)
            return tags
        """,
        hint="```py\ndef add_tag(tag, tags=None):\n    if tags is None:\n        tags = []\n```", xp=20),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `retry_delays(attempts=3, base=1.0, factor=2.0)` — список задержек между повторами по экспоненциальной схеме: `base, base*factor, base*factor², …` (всего `attempts` значений).

        Примеры:
        ```
        retry_delays()                   # → [1.0, 2.0, 4.0]
        retry_delays(4, base=0.5)        # → [0.5, 1.0, 2.0, 4.0]
        retry_delays(2, factor=3)        # → [1.0, 3.0]
        ```
        """),
        """
        def retry_delays(attempts=3, base=1.0, factor=2.0):
            pass
        """,
        """
        def test_values():
            got = [retry_delays(), retry_delays(4, base=0.5), retry_delays(2, factor=3)]
            assert got == [[1.0, 2.0, 4.0], [0.5, 1.0, 2.0, 4.0], [1.0, 3.0]], f"Получено {got}"
        """,
        """
        def retry_delays(attempts=3, base=1.0, factor=2.0):
            return [base * factor ** i for i in range(attempts)]
        """, xp=20)),

lesson(f"{P}-m2-l2", "Несколько возвращаемых значений", 
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        def min_max(nums):
            return min(nums), max(nums)

        result = min_max([3, 1, 4])
        print(result, type(result).__name__)
        lo, hi = min_max([10, -2, 7])
        print(lo, hi)
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа?", """
        def parse(line):
            name, _, value = line.partition("=")
            return name.strip(), value.strip()

        key, val = parse("timeout = 30")
        print(key, val, int(val) * 2)
        """),
    cod(f"{P}-m2-l2-e3", t("""
        Напиши функцию `divide(a, b)`, которая возвращает **пару** `(целая часть, остаток)`.

        Примеры:
        ```
        divide(17, 5)   # → (3, 2)
        q, r = divide(10, 3)   # q == 3, r == 1
        ```
        """),
        """
        def divide(a, b):
            pass
        """,
        """
        def test_values():
            assert divide(17, 5) == (3, 2) and divide(10, 3) == (3, 1), "Неверная пара"
        """,
        """
        def divide(a, b):
            return a // b, a % b
        """),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `stats(nums)` — вернуть **три** значения: минимум, максимум и среднее (округлённое до 2 знаков).

        Пример:
        ```
        stats([1, 2, 3, 10])   # → (1, 10, 4.0)
        lo, hi, avg = stats([5, 5])   # (5, 5, 5.0)
        ```
        """),
        """
        def stats(nums):
            pass
        """,
        """
        def test_values():
            assert stats([1, 2, 3, 10]) == (1, 10, 4.0) and stats([5, 5]) == (5, 5, 5.0), "Неверная статистика"
        """,
        """
        def stats(nums):
            return min(nums), max(nums), round(sum(nums) / len(nums), 2)
        """),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `split_results(results)` — разделить результаты тестов на два списка: имена прошедших и имена упавших.

        - `results` — список пар `(имя, прошёл_ли)`.
        - Вернуть пару списков `(passed, failed)`.

        Пример:
        ```
        split_results([("login", True), ("pay", False), ("cart", True)])
        # → (["login", "cart"], ["pay"])
        ```
        """),
        """
        def split_results(results):
            pass
        """,
        """
        def test_values():
            got = split_results([("login", True), ("pay", False), ("cart", True)])
            assert got == (["login", "cart"], ["pay"]), f"Получено {got}"
            assert split_results([]) == ([], []), "Пустой вход — два пустых списка"
        """,
        """
        def split_results(results):
            passed, failed = [], []
            for name, ok in results:
                (passed if ok else failed).append(name)
            return passed, failed
        """)),

lesson(f"{P}-m2-l3", "Docstring и аннотации типов", 
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        def add(a: int, b: int) -> int:
            \"\"\"Сложить два числа.\"\"\"
            return a + b

        print(add.__doc__)
        print(add.__annotations__)
        print(add("а", "б"))
        """, hint="Аннотации — только подсказки: строки тоже «сложатся»."),
    out(f"{P}-m2-l3-e2", "Что выведет программа?", """
        def f(items: list[str], limit: int | None = None) -> list[str]:
            return items[:limit]

        print(f(["a", "b", "c"]))
        print(f(["a", "b", "c"], 2))
        """),
    cod(f"{P}-m2-l3-e3", t("""
        Напиши функцию `is_valid_email` с **аннотациями типов** и **docstring**:

        - параметр `email: str`, возвращает `bool`;
        - docstring — непустая строка с описанием;
        - логика: в строке ровно один `@`, и после него есть точка.

        Примеры:
        ```
        is_valid_email("a@b.ru")   # → True
        is_valid_email("a@b")      # → False
        is_valid_email("a@@b.ru")  # → False
        ```
        """),
        """
        def is_valid_email(email):
            pass
        """,
        """
        def test_logic():
            got = [is_valid_email(e) for e in ("a@b.ru", "a@b", "a@@b.ru", "ab.ru")]
            assert got == [True, False, False, False], f"Получено {got}"

        def test_docs():
            assert is_valid_email.__doc__ and is_valid_email.__doc__.strip(), "Добавь docstring"
            ann = is_valid_email.__annotations__
            assert ann.get("email") is str and ann.get("return") is bool, f"Нужны аннотации email: str и -> bool, сейчас {ann}"
        """,
        """
        def is_valid_email(email: str) -> bool:
            \"\"\"Проверить, похож ли email на корректный: один @ и точка в домене.\"\"\"
            if email.count("@") != 1:
                return False
            return "." in email.split("@")[1]
        """, xp=20),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `describe_function(func)`, которая возвращает **первую строку** docstring переданной функции, а если docstring нет — `"нет описания"`.

        Пример:
        ```
        def login():
            \"\"\"Войти в систему.
            Подробности...\"\"\"

        describe_function(login)   # → "Войти в систему."
        describe_function(print)   # → первая строка документации print
        ```
        """),
        """
        def describe_function(func):
            pass
        """,
        """
        def test_doc():
            def login():
                \"\"\"Войти в систему.
                Подробности на второй строке.\"\"\"
            assert describe_function(login) == "Войти в систему.", f"Получено {describe_function(login)!r}"

        def test_no_doc():
            def nodoc():
                pass
            assert describe_function(nodoc) == "нет описания", "Без docstring — «нет описания»"
        """,
        """
        def describe_function(func):
            doc = func.__doc__
            if not doc:
                return "нет описания"
            return doc.strip().splitlines()[0]
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `typed_call(func, *args)`, которая проверяет аргументы по аннотациям функции `func` и вызывает её.

        - Для каждого позиционного аргумента: если в `func.__annotations__` есть тип для соответствующего параметра и аргумент не этого типа — бросить `TypeError`.
        - Иначе вернуть `func(*args)`.

        Имена параметров по порядку: `func.__code__.co_varnames[:func.__code__.co_argcount]`.

        Пример:
        ```
        def add(a: int, b: int) -> int:
            return a + b

        typed_call(add, 1, 2)       # → 3
        typed_call(add, 1, "2")     # TypeError
        ```
        """),
        """
        def typed_call(func, *args):
            pass
        """,
        """
        def test_ok():
            def add(a: int, b: int) -> int:
                return a + b
            assert typed_call(add, 1, 2) == 3, "Корректные типы — вызов"

        def test_bad():
            def add(a: int, b: int) -> int:
                return a + b
            try:
                typed_call(add, 1, "2")
            except TypeError:
                return
            assert False, "Неверный тип аргумента — TypeError"

        def test_no_annotation():
            def echo(x):
                return x
            assert typed_call(echo, "что угодно") == "что угодно", "Без аннотаций — без проверки"
        """,
        """
        def typed_call(func, *args):
            names = func.__code__.co_varnames[:func.__code__.co_argcount]
            for name, value in zip(names, args):
                expected = func.__annotations__.get(name)
                if expected is not None and not isinstance(value, expected):
                    raise TypeError(f"{name}: ожидался {expected.__name__}, получен {type(value).__name__}")
            return func(*args)
        """, xp=25)),
)

# ============================================================
m3 = module(f"{P}-m3", "Функции глубже", "🚀", "Функции как объекты, рекурсия и чистые функции",

lesson(f"{P}-m3-l1", "Функции как объекты", 
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        def shout(s):
            return s.upper() + "!"

        f = shout
        print(f("привет"))
        print(f is shout, f.__name__)
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа?", """
        def apply_all(funcs, value):
            return [f(value) for f in funcs]

        print(apply_all([len, str.upper, str.title], "codeQuest"))
        """),
    cod(f"{P}-m3-l1-e3", t("""
        Напиши функцию `apply_twice(func, value)` — применить функцию к значению **дважды**: `func(func(value))`.

        Примеры:
        ```
        apply_twice(lambda x: x + 3, 10)   # → 16
        apply_twice(str.upper, "ab")       # → "AB"
        ```
        """),
        """
        def apply_twice(func, value):
            pass
        """,
        """
        def test_values():
            assert apply_twice(lambda x: x + 3, 10) == 16 and apply_twice(lambda x: x * 2, 1) == 4 and apply_twice(str.upper, "ab") == "AB", "Неверный результат"
        """,
        """
        def apply_twice(func, value):
            return func(func(value))
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `calculate(op, a, b)`, которая выбирает операцию из **словаря функций**:

        ```
        OPS = {"+": ..., "-": ..., "*": ..., "/": ...}
        ```

        - Вернуть результат операции `op` над `a` и `b`.
        - Если операции нет в словаре — бросить `ValueError`.

        Примеры:
        ```
        calculate("+", 2, 3)   # → 5
        calculate("/", 7, 2)   # → 3.5
        calculate("%", 1, 1)   # ValueError
        ```
        """),
        """
        def calculate(op, a, b):
            pass
        """,
        """
        def test_values():
            got = [calculate("+", 2, 3), calculate("-", 2, 3), calculate("*", 2, 3), calculate("/", 7, 2)]
            assert got == [5, -1, 6, 3.5], f"Получено {got}"

        def test_unknown():
            try:
                calculate("%", 1, 1)
            except ValueError:
                return
            assert False, "Неизвестная операция — ValueError"
        """,
        """
        OPS = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }

        def calculate(op, a, b):
            if op not in OPS:
                raise ValueError(f"неизвестная операция {op}")
            return OPS[op](a, b)
        """, xp=20),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `run_checks(value, checks)`, где `checks` — список функций-проверок, каждая возвращает `True`/`False`.

        Вернуть список **имён** проверок (`func.__name__`), которые **не прошли**.

        Пример:
        ```
        def not_empty(s): return s != ""
        def has_digit(s): return any(c.isdigit() for c in s)
        def long_enough(s): return len(s) >= 8

        run_checks("abc", [not_empty, has_digit, long_enough])
        # → ["has_digit", "long_enough"]
        ```
        """),
        """
        def run_checks(value, checks):
            pass
        """,
        """
        def not_empty(s): return s != ""
        def has_digit(s): return any(c.isdigit() for c in s)
        def long_enough(s): return len(s) >= 8

        def test_values():
            assert run_checks("abc", [not_empty, has_digit, long_enough]) == ["has_digit", "long_enough"], f"Получено {run_checks('abc', [not_empty, has_digit, long_enough])}"
            assert run_checks("abcdefg1", [not_empty, has_digit, long_enough]) == [], "Все проверки прошли"
        """,
        """
        def run_checks(value, checks):
            return [check.__name__ for check in checks if not check(value)]
        """)),

lesson(f"{P}-m3-l2", "Рекурсия", 
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        def countdown(n):
            if n == 0:
                print("Старт!")
                return
            print(n)
            countdown(n - 1)

        countdown(3)
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа?", """
        def depth(item):
            if not isinstance(item, list):
                return 0
            return 1 + max((depth(x) for x in item), default=0)

        print(depth(5), depth([]), depth([1, [2, [3]]]))
        """),
    cod(f"{P}-m3-l2-e3", t("""
        Напиши **рекурсивную** функцию `factorial(n)` (без циклов).

        Примеры:
        ```
        factorial(0)   # → 1
        factorial(5)   # → 120
        ```
        """),
        """
        def factorial(n):
            pass
        """,
        """
        def test_values():
            assert [factorial(n) for n in (0, 1, 5, 10)] == [1, 1, 120, 3628800], "Неверный факториал"

        def test_recursive():
            src = open("solution.py", encoding="utf-8").read()
            assert "for " not in src and "while " not in src, "Реши без циклов — рекурсией"
        """,
        """
        def factorial(n):
            if n <= 1:
                return 1
            return n * factorial(n - 1)
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши рекурсивную функцию `deep_sum(data)` — сумма всех чисел во вложенных списках любой глубины.

        Примеры:
        ```
        deep_sum([1, [2, 3], [[4]], []])   # → 10
        deep_sum([])                       # → 0
        ```
        """),
        """
        def deep_sum(data):
            pass
        """,
        """
        def test_values():
            assert deep_sum([1, [2, 3], [[4]], []]) == 10 and deep_sum([]) == 0 and deep_sum([[[[5]]], 5]) == 10, "Неверная сумма"
        """,
        """
        def deep_sum(data):
            total = 0
            for item in data:
                if isinstance(item, list):
                    total += deep_sum(item)
                else:
                    total += item
            return total
        """, xp=20),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши рекурсивную функцию `find_keys(data, key)` — список **всех** значений по ключу `key` в JSON-подобной структуре (вложенные словари и списки).

        Пример:
        ```
        data = {"id": 1, "items": [{"id": 2}, {"meta": {"id": 3}}], "owner": {"name": "x"}}
        find_keys(data, "id")   # → [1, 2, 3]
        ```
        Порядок — обход «сначала сам словарь, потом вложенные значения по порядку».
        """),
        """
        def find_keys(data, key):
            pass
        """,
        """
        def test_values():
            data = {"id": 1, "items": [{"id": 2}, {"meta": {"id": 3}}], "owner": {"name": "x"}}
            assert find_keys(data, "id") == [1, 2, 3], f"Получено {find_keys(data, 'id')}"
            assert find_keys([], "id") == [] and find_keys(5, "id") == [], "Нет словарей — пусто"
        """,
        """
        def find_keys(data, key):
            found = []
            if isinstance(data, dict):
                if key in data:
                    found.append(data[key])
                for value in data.values():
                    found.extend(find_keys(value, key))
            elif isinstance(data, list):
                for item in data:
                    found.extend(find_keys(item, key))
            return found
        """, xp=25)),

lesson(f"{P}-m3-l3", "Чистые функции и побочные эффекты", 
    out(f"{P}-m3-l3-e1", "Что выведет программа? Функция меняет аргумент.", """
        def add_bad(items, x):
            items.append(x)
            return items

        data = [1]
        result = add_bad(data, 2)
        print(data, result, data is result)
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа?", """
        counter = 0

        def next_id():
            global counter
            counter += 1
            return counter

        print(next_id(), next_id(), next_id())
        print(counter)
        """, hint="Функция с global зависит от внешнего состояния — одинаковый вызов даёт разные результаты."),
    cod(f"{P}-m3-l3-e3", t("""
        Функция `normalize(names)` «грязная»: она изменяет переданный список. Перепиши её **чистой** — вернуть **новый** список с именами в нижнем регистре без пробелов по краям, не трогая исходный.

        Пример:
        ```
        data = ["  Аня ", "БОРЯ"]
        normalize(data)   # → ["аня", "боря"],  data по-прежнему ["  Аня ", "БОРЯ"]
        ```
        """),
        """
        def normalize(names):
            for i in range(len(names)):
                names[i] = names[i].strip().lower()
            return names
        """,
        """
        def test_result():
            assert normalize(["  Аня ", "БОРЯ"]) == ["аня", "боря"], "Неверная нормализация"

        def test_pure():
            data = ["  Аня ", "БОРЯ"]
            normalize(data)
            assert data == ["  Аня ", "БОРЯ"], "Исходный список изменился — функция должна быть чистой"
        """,
        """
        def normalize(names):
            return [name.strip().lower() for name in names]
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Функция `apply_discount` зависит от **глобальной** переменной `DISCOUNT`, из-за чего её трудно тестировать. Перепиши её так, чтобы скидка передавалась **параметром** `percent` (по умолчанию 10).

        Примеры:
        ```
        apply_discount(1000)       # → 900.0
        apply_discount(1000, 25)   # → 750.0
        ```
        В решении не должно быть слова `global` и обращения к `DISCOUNT` внутри функции.
        """),
        """
        DISCOUNT = 10

        def apply_discount(price):
            global DISCOUNT
            return price * (1 - DISCOUNT / 100)
        """,
        """
        import inspect

        def test_values():
            assert apply_discount(1000) == 900.0 and apply_discount(1000, 25) == 750.0, "Неверная цена"

        def test_no_global():
            src = inspect.getsource(apply_discount)
            assert "global" not in src and "DISCOUNT" not in src, "Функция не должна зависеть от глобальной переменной"
        """,
        """
        def apply_discount(price, percent=10):
            return price * (1 - percent / 100)
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Раздели «грязную» функцию на **чистую** логику и действие.

        Напиши две функции:
        1. `build_report(results)` — **чистая**: по списку пар `(имя, прошёл)` возвращает строку отчёта, строки через `\\n`: `"✅ login"` / `"❌ pay"`.
        2. `print_report(results)` — печатает то, что вернула `build_report`.

        Пример:
        ```
        build_report([("login", True), ("pay", False)])   # → "✅ login\\n❌ pay"
        ```
        """),
        """
        def build_report(results):
            pass

        def print_report(results):
            pass
        """,
        """
        def test_pure():
            assert build_report([("login", True), ("pay", False)]) == "✅ login\\n❌ pay", f"Получено {build_report([('login', True), ('pay', False)])!r}"
            assert capture(build_report, [("x", True)]) == "", "build_report ничего не печатает"

        def test_print():
            assert capture(print_report, [("login", True)]).strip() == "✅ login", "print_report печатает отчёт"
        """,
        """
        def build_report(results):
            return "\\n".join(f"{'✅' if ok else '❌'} {name}" for name, ok in results)

        def print_report(results):
            print(build_report(results))
        """, xp=20)),
)

TOPIC = topic("py-functions", "Функции", "🧰", "#e05ab0",
              "def, параметры, return, значения по умолчанию, функции как объекты и рекурсия",
              m1, m2, m3, group="Python")
