"""Тема «Функции», модуль 3 «Функции глубже» — задания. Теория — в _fn_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "fn"

m3 = module(f"{P}-m3", "Функции глубже", "🚀", "Функции как объекты, рекурсия, чистые функции и тесты",

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
    out(f"{P}-m3-l1-e6", "Что выведет программа? Функции в списке.", """
        ops = [str.upper, str.lower, len]
        for f in ops:
            print(f.__name__, f("Аня"))
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
        """),
    cod(f"{P}-m3-l1-e7", t("""
        Напиши функцию `apply_to_all(func, items)` — новый список: `func`, применённая к каждому элементу.

        Примеры:
        ```
        apply_to_all(len, ["a", "bcd"])        # → [1, 3]
        apply_to_all(str.upper, ["qa", "dev"]) # → ["QA", "DEV"]
        ```
        """),
        """
        def apply_to_all(func, items):
            pass
        """,
        """
        def test_values():
            assert apply_to_all(len, ["a", "bcd"]) == [1, 3] and apply_to_all(str.upper, ["qa", "dev"]) == ["QA", "DEV"], "Неверный результат"
            assert apply_to_all(abs, []) == [], "Пустой — пустой"
        """,
        """
        def apply_to_all(func, items):
            result = []
            for x in items:
                result.append(func(x))
            return result
        """),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `get_tool(name)`, которая по названию возвращает **саму функцию** (не результат вызова):
        `"len"` → `len`, `"upper"` → `str.upper`, `"abs"` → `abs`; для неизвестного имени — `None`.
        Используй словарь.

        Примеры:
        ```
        get_tool("len")("abc")    # → 3
        get_tool("upper")("hi")   # → "HI"
        get_tool("xxx")           # → None
        ```
        """),
        """
        def get_tool(name):
            pass
        """,
        """
        def test_values():
            assert get_tool("len") is len and get_tool("upper") is str.upper and get_tool("abs") is abs, "Верни саму функцию"
            assert get_tool("len")("abc") == 3 and get_tool("xxx") is None, "Неверный результат"
        """,
        """
        TOOLS = {"len": len, "upper": str.upper, "abs": abs}

        def get_tool(name):
            return TOOLS.get(name)
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
    out(f"{P}-m3-l2-e6", "Что выведет программа?", """
        def s(n):
            if n == 0:
                return 0
            return n + s(n - 1)

        print(s(4), s(0))
        """, hint="s(4) = 4 + s(3) = 4 + 3 + s(2)…"),
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
        """, xp=25),
    cod(f"{P}-m3-l2-e7", t("""
        Напиши **рекурсивную** функцию `power(base, exp)` — `base` в степени `exp` (`exp >= 0`) без `**`, `pow` и циклов.

        Примеры:
        ```
        power(2, 10)   # → 1024
        power(5, 0)    # → 1
        ```
        """),
        """
        def power(base, exp):
            pass
        """,
        """
        def test_values():
            assert [power(2, 10), power(5, 0), power(3, 3)] == [1024, 1, 27], "Неверная степень"

        def test_recursive():
            src = open("solution.py", encoding="utf-8").read()
            assert "**" not in src and "pow(" not in src and "for " not in src and "while " not in src, "Реши рекурсией"
        """,
        """
        def power(base, exp):
            if exp == 0:
                return 1
            return base * power(base, exp - 1)
        """),
    cod(f"{P}-m3-l2-e8", t("""
        Напиши **рекурсивную** функцию `countdown_list(n)` — список чисел от `n` до 1 (без циклов).

        Примеры:
        ```
        countdown_list(3)   # → [3, 2, 1]
        countdown_list(0)   # → []
        ```
        """),
        """
        def countdown_list(n):
            pass
        """,
        """
        def test_values():
            assert countdown_list(3) == [3, 2, 1] and countdown_list(0) == [] and countdown_list(1) == [1], "Неверный список"

        def test_recursive():
            src = open("solution.py", encoding="utf-8").read()
            assert "for " not in src and "while " not in src and "range(" not in src, "Реши рекурсией"
        """,
        """
        def countdown_list(n):
            if n == 0:
                return []
            return [n] + countdown_list(n - 1)
        """)),

lesson(f"{P}-recur2", "Рекурсия: глубина, ошибки и цикл вместо рекурсии",
    out(f"{P}-recur2-e1", "Что выведет программа? Рекурсия без выхода.", """
        def bad(n):
            return bad(n - 1)

        try:
            bad(5)
        except RecursionError:
            print("слишком глубоко")
        """),
    out(f"{P}-recur2-e2", "Что выведет программа? Числа Фибоначчи.", """
        def fib(n):
            if n < 2:
                return n
            return fib(n - 1) + fib(n - 2)

        print([fib(i) for i in range(8)])
        """),
    out(f"{P}-recur2-e3", "Что выведет программа? Лимит глубины.", """
        import sys
        print(sys.getrecursionlimit() >= 1000)
        """),
    cod(f"{P}-recur2-e4", t("""
        Напиши **рекурсивную** функцию `reverse_str(s)` — строка в обратном порядке, без `[::-1]`, `reversed` и циклов.

        Идея: разворот строки — это разворот «всего, кроме первого символа», плюс первый символ.

        Примеры:
        ```
        reverse_str("abc")   # → "cba"
        reverse_str("")      # → ""
        ```
        """),
        """
        def reverse_str(s):
            pass
        """,
        """
        def test_values():
            assert reverse_str("abc") == "cba" and reverse_str("") == "" and reverse_str("a") == "a", "Неверный разворот"

        def test_recursive():
            src = open("solution.py", encoding="utf-8").read()
            assert "[::-1]" not in src and "reversed" not in src and "for " not in src and "while " not in src, "Реши рекурсией"
        """,
        """
        def reverse_str(s):
            if s == "":
                return ""
            return reverse_str(s[1:]) + s[0]
        """),
    cod(f"{P}-recur2-e5", t("""
        Напиши **рекурсивную** функцию `sum_digits(n)` — сумма цифр неотрицательного целого числа, без циклов и строк.

        Примеры:
        ```
        sum_digits(2024)   # → 8
        sum_digits(7)      # → 7
        ```
        Подсказка: последняя цифра — `n % 10`, число без неё — `n // 10`.
        """),
        """
        def sum_digits(n):
            pass
        """,
        """
        def test_values():
            assert [sum_digits(2024), sum_digits(7), sum_digits(0), sum_digits(999)] == [8, 7, 0, 27], "Неверная сумма"

        def test_recursive():
            src = open("solution.py", encoding="utf-8").read()
            assert "for " not in src and "while " not in src and "str(" not in src, "Реши рекурсией, без строк"
        """,
        """
        def sum_digits(n):
            if n < 10:
                return n
            return n % 10 + sum_digits(n // 10)
        """),
    cod(f"{P}-recur2-e6", t("""
        Рекурсивный `fib(n)` очень медленный: для `fib(40)` он делает сотни миллионов вызовов.
        Напиши функцию `fib_fast(n)` **циклом** — чтобы `fib_fast(80)` считалось мгновенно.

        Примеры:
        ```
        fib_fast(0)    # → 0
        fib_fast(10)   # → 55
        fib_fast(80)   # → 23416728348467685
        ```
        """),
        """
        def fib_fast(n):
            if n < 2:
                return n
            return fib_fast(n - 1) + fib_fast(n - 2)
        """,
        """
        def test_values():
            assert [fib_fast(i) for i in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34], "Неверные числа"

        def test_fast():
            assert fib_fast(80) == 23416728348467685, "fib_fast(80) неверно"
        """,
        """
        def fib_fast(n):
            a, b = 0, 1
            for _ in range(n):
                a, b = b, a + b
            return a
        """, xp=20),
    cod(f"{P}-recur2-e7", t("""
        Напиши **рекурсивную** функцию `is_pal(s)` — палиндром ли строка (с учётом регистра), без `[::-1]` и циклов.

        Идея: строка — палиндром, если первый и последний символы равны **и** середина — тоже палиндром.

        Примеры:
        ```
        is_pal("шалаш")   # → True
        is_pal("abca")    # → False
        is_pal("")        # → True
        ```
        """),
        """
        def is_pal(s):
            pass
        """,
        """
        def test_values():
            got = [is_pal("шалаш"), is_pal("abca"), is_pal(""), is_pal("a"), is_pal("abba")]
            assert got == [True, False, True, True, True], f"Получено {got}"

        def test_recursive():
            src = open("solution.py", encoding="utf-8").read()
            assert "[::-1]" not in src and "for " not in src and "while " not in src, "Реши рекурсией"
        """,
        """
        def is_pal(s):
            if len(s) < 2:
                return True
            if s[0] != s[-1]:
                return False
            return is_pal(s[1:-1])
        """),
    cod(f"{P}-recur2-e8", t("""
        Напиши **рекурсивную** функцию `flatten(items)` — сделать плоский список из списков любой вложенности.

        Примеры:
        ```
        flatten([1, [2, [3, [4]]], 5])   # → [1, 2, 3, 4, 5]
        flatten([])                      # → []
        ```
        """),
        """
        def flatten(items):
            pass
        """,
        """
        def test_values():
            assert flatten([1, [2, [3, [4]]], 5]) == [1, 2, 3, 4, 5] and flatten([]) == [] and flatten([[], [[]]]) == [], "Неверный результат"
        """,
        """
        def flatten(items):
            result = []
            for x in items:
                if isinstance(x, list):
                    result.extend(flatten(x))
                else:
                    result.append(x)
            return result
        """, xp=20)),

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
    out(f"{P}-m3-l3-e6", "Что выведет программа? Чистая версия.", """
        def add_good(items, x):
            return items + [x]

        data = [1]
        result = add_good(data, 2)
        print(data, result, data is result)
        """),
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
        """, xp=20),
    cod(f"{P}-m3-l3-e7", t("""
        Напиши **чистую** функцию `with_bonus(scores, bonus)` — новый список, где к каждому баллу прибавлен `bonus`.
        Исходный список не менять.

        Пример:
        ```
        data = [50, 70]
        with_bonus(data, 5)   # → [55, 75], data == [50, 70]
        ```
        """),
        """
        def with_bonus(scores, bonus):
            pass
        """,
        """
        def test_values():
            data = [50, 70]
            assert with_bonus(data, 5) == [55, 75] and data == [50, 70], f"data={data}"
        """,
        """
        def with_bonus(scores, bonus):
            result = []
            for s in scores:
                result.append(s + bonus)
            return result
        """),
    cod(f"{P}-m3-l3-e8", t("""
        Функция `next_counter()` берёт значение из глобальной переменной и меняет её — её результат зависит от истории вызовов.
        Перепиши её **чистой**: `next_counter(current)` получает текущее значение и возвращает следующее. Без `global`.

        Пример:
        ```
        next_counter(0)   # → 1
        next_counter(41)  # → 42
        ```
        """),
        """
        counter = 0

        def next_counter():
            global counter
            counter += 1
            return counter
        """,
        """
        import inspect

        def test_values():
            assert next_counter(0) == 1 and next_counter(41) == 42 and next_counter(0) == 1, "Одинаковый вызов — одинаковый результат"

        def test_no_global():
            assert "global" not in inspect.getsource(next_counter), "Без global"
        """,
        """
        def next_counter(current):
            return current + 1
        """)),

lesson(f"{P}-testing", "Функции и тесты",
    out(f"{P}-testing-e1", "Что выведет программа? assert, который прошёл.", """
        def add(a, b):
            return a + b

        assert add(2, 2) == 4
        assert add(-1, 1) == 0
        print("тесты прошли")
        """),
    out(f"{P}-testing-e2", "Что выведет программа? assert, который упал.", """
        try:
            assert 1 + 1 == 3, "математика сломалась"
        except AssertionError as e:
            print("упал:", e)
        """),
    out(f"{P}-testing-e3", "Что выведет программа? Тестовая функция.", """
        def test_upper():
            assert "ab".upper() == "AB"

        test_upper()
        print(test_upper.__name__, "ok")
        """),
    cod(f"{P}-testing-e4", t("""
        Напиши функцию `test_absolute()` — тест встроенной функции `abs` из **трёх** проверок через `assert`:
        положительное число, отрицательное число и ноль. Функция ничего не возвращает; если всё верно — не падает.
        """),
        """
        def test_absolute():
            pass
        """,
        """
        import inspect

        def test_runs():
            test_absolute()

        def test_has_asserts():
            src = inspect.getsource(test_absolute)
            assert src.count("assert") >= 3 and "abs(" in src, "Нужны три assert с abs"
        """,
        """
        def test_absolute():
            assert abs(5) == 5
            assert abs(-5) == 5
            assert abs(0) == 0
        """),
    cod(f"{P}-testing-e5", t("""
        Напиши функцию `assert_equal(actual, expected)`: если значения не равны — бросить `AssertionError`
        с сообщением `"<actual!r> != <expected!r>"`, иначе ничего не делать.

        Примеры:
        ```
        assert_equal(2 + 2, 4)       # ничего
        assert_equal("a", "b")       # AssertionError: 'a' != 'b'
        ```
        """),
        """
        def assert_equal(actual, expected):
            pass
        """,
        """
        def test_equal():
            assert assert_equal(4, 4) is None, "Для равных значений — ничего"

        def test_not_equal():
            try:
                assert_equal("a", "b")
            except AssertionError as e:
                assert str(e) == "'a' != 'b'", f"Сообщение {str(e)!r}"
                return
            assert False, "Для разных значений — AssertionError"
        """,
        """
        def assert_equal(actual, expected):
            assert actual == expected, f"{actual!r} != {expected!r}"
        """),
    cod(f"{P}-testing-e6", t("""
        Напиши функцию `check(func, cases)` — маленький тест-раннер. `cases` — список пар `(аргумент, ожидаемый_результат)`.
        Вызови `func(аргумент)` для каждой пары и верни список **аргументов**, на которых результат не совпал.

        Пример:
        ```
        check(abs, [(5, 5), (-3, 3), (-2, 5)])   # → [-2]
        ```
        """),
        """
        def check(func, cases):
            pass
        """,
        """
        def test_values():
            assert check(abs, [(5, 5), (-3, 3), (-2, 5)]) == [-2] and check(len, [("ab", 2)]) == [] and check(abs, []) == [], "Неверный результат"
        """,
        """
        def check(func, cases):
            failed = []
            for arg, expected in cases:
                if func(arg) != expected:
                    failed.append(arg)
            return failed
        """),
    cod(f"{P}-testing-e7", t("""
        Напиши функцию `count_passed(tests)`: `tests` — список тестовых функций без параметров.
        Запусти каждую; тест **прошёл**, если не бросил `AssertionError`. Верни количество прошедших.

        Пример:
        ```
        def t_ok():
            assert True
        def t_bad():
            assert False

        count_passed([t_ok, t_bad, t_ok])   # → 2
        ```
        """),
        """
        def count_passed(tests):
            pass
        """,
        """
        def test_values():
            def t_ok():
                assert True
            def t_bad():
                assert False, "упал"
            assert count_passed([t_ok, t_bad, t_ok]) == 2 and count_passed([]) == 0, "Неверный подсчёт"
        """,
        """
        def count_passed(tests):
            passed = 0
            for test in tests:
                try:
                    test()
                    passed += 1
                except AssertionError:
                    pass
            return passed
        """),
    cod(f"{P}-testing-e8", t("""
        Напиши функцию `is_even(n)` **и** тест к ней `test_is_even()` с несколькими `assert`: чётное, нечётное, ноль и
        отрицательное число. Тест должен **проходить** для правильной `is_even` и **падать**, если `is_even` сломать.
        """),
        """
        def is_even(n):
            pass

        def test_is_even():
            pass
        """,
        """
        def test_function():
            assert [is_even(4), is_even(7), is_even(0), is_even(-2)] == [True, False, True, True], "is_even неверна"

        def test_your_test_passes():
            test_is_even()

        def test_your_test_catches_bugs():
            g = test_is_even.__globals__
            original = g["is_even"]
            for broken in (lambda n: True, lambda n: False, lambda n: n % 2 == 1):
                g["is_even"] = broken
                try:
                    test_is_even()
                except AssertionError:
                    continue
                finally:
                    g["is_even"] = original
                assert False, "test_is_even не заметил сломанную is_even — добавь проверок"
        """,
        """
        def is_even(n):
            return n % 2 == 0

        def test_is_even():
            assert is_even(4)
            assert not is_even(7)
            assert is_even(0)
            assert is_even(-2)
        """, xp=20)),
)
