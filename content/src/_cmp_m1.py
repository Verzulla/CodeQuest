"""Тема «Списковые включения», модуль 1 «Списковые включения» — задания. Теория — в _cmp_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "cmp"

m1 = module(f"{P}-m1", "Списковые включения", "🧺", "От цикла к включению, фильтр, условное выражение, функции в выражении",

lesson(f"{P}-m1-l1", "От цикла к включению",
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        squares = []
        for n in range(5):
            squares.append(n * n)
        print(squares)
        print([n * n for n in range(5)])
        """, hint="Цикл с append и включение дают одно и то же."),
    out(f"{P}-m1-l1-e2", "Что выведет программа?", """
        words = ["api", "ui", "docker"]
        print([w.upper() for w in words])
        print([len(w) for w in words])
        print(words)
        """, hint="Включение создаёт НОВЫЙ список, исходный не меняется."),
    out(f"{P}-m1-l1-e3", "Что выведет программа?", """
        print([x for x in "abc"])
        print([0 for _ in range(3)])
        print([str(i) for i in [1, 2]])
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `doubled(nums)` — новый список, где каждое число удвоено. Используй **списковое включение**.

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

        def test_comprehension():
            src = open("solution.py", encoding="utf-8").read()
            assert "[" in src and " for " in src and "append" not in src, "Используй списковое включение, без append"
        """,
        """
        def doubled(nums):
            return [n * 2 for n in nums]
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `lengths(words)` — список длин слов через включение.

        ```
        lengths(["a", "bb", "ccc"])   # → [1, 2, 3]
        ```
        """),
        """
        def lengths(words):
            pass
        """,
        """
        def test_values():
            assert lengths(["a", "bb", "ccc"]) == [1, 2, 3] and lengths([]) == [], "Неверный результат"
        """,
        """
        def lengths(words):
            return [len(w) for w in words]
        """),
    cod(f"{P}-m1-l1-e6", t("""
        Перепиши функцию `to_strings` из заготовки одним списковым включением.
        """),
        """
        def to_strings(items):
            result = []
            for x in items:
                result.append(str(x))
            return result
        """,
        """
        def test_values():
            assert to_strings([1, 2.5, None]) == ["1", "2.5", "None"], "Неверный результат"

        def test_comprehension():
            assert "append" not in open("solution.py", encoding="utf-8").read(), "Перепиши через включение"
        """,
        """
        def to_strings(items):
            return [str(x) for x in items]
        """),
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `squares_up_to(n)` — квадраты чисел от 1 до `n` включительно.

        ```
        squares_up_to(4)   # → [1, 4, 9, 16]
        ```
        """),
        """
        def squares_up_to(n):
            pass
        """,
        """
        def test_values():
            assert squares_up_to(4) == [1, 4, 9, 16] and squares_up_to(0) == [], "Неверный результат"
        """,
        """
        def squares_up_to(n):
            return [i * i for i in range(1, n + 1)]
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `endpoints(paths)` — полные адреса: к каждому пути добавить префикс `"https://api.shop.ru"`.

        ```
        endpoints(["/users", "/items"])   # → ["https://api.shop.ru/users", "https://api.shop.ru/items"]
        ```
        """),
        """
        BASE = "https://api.shop.ru"

        def endpoints(paths):
            pass
        """,
        """
        def test_values():
            assert endpoints(["/users", "/items"]) == ["https://api.shop.ru/users", "https://api.shop.ru/items"] and endpoints([]) == [], "Неверный результат"
        """,
        """
        BASE = "https://api.shop.ru"

        def endpoints(paths):
            return [BASE + p for p in paths]
        """),
),

lesson(f"{P}-m1-l2", "Фильтр: if в конце",
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        nums = [5, -2, 8, 0, -7, 3]
        print([n for n in nums if n > 0])
        print([n * 10 for n in nums if n < 0])
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа? Два условия.", """
        print([n for n in range(20) if n % 2 == 0 if n % 3 == 0])
        print([n for n in range(20) if n % 2 == 0 and n % 3 == 0])
        """, hint="Несколько if подряд работают как and."),
    out(f"{P}-m1-l2-e3", "Что выведет программа?", """
        words = ["api", "", "ui", "  ", "ci"]
        print([w for w in words if w.strip()])
        print(len([w for w in words if not w.strip()]))
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `evens(nums)` — только чётные числа.

        ```
        evens([1, 2, 3, 4])   # → [2, 4]
        ```
        """),
        """
        def evens(nums):
            pass
        """,
        """
        def test_values():
            assert evens([1, 2, 3, 4]) == [2, 4] and evens([1, 3]) == [] and evens([0, -2]) == [0, -2], "Неверный результат"
        """,
        """
        def evens(nums):
            return [n for n in nums if n % 2 == 0]
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `errors_only(codes)` — коды ответов `>= 400`.

        ```
        errors_only([200, 404, 301, 500])   # → [404, 500]
        ```
        """),
        """
        def errors_only(codes):
            pass
        """,
        """
        def test_values():
            assert errors_only([200, 404, 301, 500]) == [404, 500] and errors_only([]) == [], "Неверный результат"
        """,
        """
        def errors_only(codes):
            return [c for c in codes if c >= 400]
        """),
    cod(f"{P}-m1-l2-e6", t("""
        Напиши функцию `long_upper(words, n)` — слова длиннее `n`, переведённые в верхний регистр.

        ```
        long_upper(["api", "docker", "ci", "pytest"], 3)   # → ["DOCKER", "PYTEST"]
        ```
        """),
        """
        def long_upper(words, n):
            pass
        """,
        """
        def test_values():
            assert long_upper(["api", "docker", "ci", "pytest"], 3) == ["DOCKER", "PYTEST"] and long_upper([], 1) == [], "Неверный результат"
        """,
        """
        def long_upper(words, n):
            return [w.upper() for w in words if len(w) > n]
        """),
    cod(f"{P}-m1-l2-e7", t("""
        Напиши функцию `multiples(n, a, b)` — числа от 1 до `n`, которые делятся **и** на `a`, **и** на `b`.

        ```
        multiples(30, 2, 3)   # → [6, 12, 18, 24, 30]
        ```
        """),
        """
        def multiples(n, a, b):
            pass
        """,
        """
        def test_values():
            assert multiples(30, 2, 3) == [6, 12, 18, 24, 30] and multiples(5, 7, 1) == [], "Неверный результат"
        """,
        """
        def multiples(n, a, b):
            return [i for i in range(1, n + 1) if i % a == 0 and i % b == 0]
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши функцию `failed(results)` — `results` это список пар `(имя, статус)`. Вернуть имена со статусом `"fail"`. Распакуй пару прямо во включении.

        ```
        failed([("login", "pass"), ("pay", "fail")])   # → ["pay"]
        ```
        """),
        """
        def failed(results):
            pass
        """,
        """
        def test_values():
            assert failed([("login", "pass"), ("pay", "fail"), ("cart", "fail")]) == ["pay", "cart"] and failed([]) == [], "Неверный результат"
        """,
        """
        def failed(results):
            return [name for name, status in results if status == "fail"]
        """),
),

lesson(f"{P}-m1-l3", "Условное выражение: if-else в результате",
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        nums = [3, -1, 0, 5]
        print(["+" if n > 0 else "-" for n in nums])
        print([n if n >= 0 else 0 for n in nums])
        """, hint="if-else слева выбирает ЗНАЧЕНИЕ для каждого элемента."),
    out(f"{P}-m1-l3-e2", "Что выведет программа? Фильтр против выбора.", """
        nums = [1, 2, 3, 4]
        print([n for n in nums if n % 2 == 0])
        print([n if n % 2 == 0 else None for n in nums])
        """),
    out(f"{P}-m1-l3-e3", "Что выведет программа? И то и другое.", """
        codes = [200, 404, 500, 301, 503]
        print(["client" if c < 500 else "server" for c in codes if c >= 400])
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `parity(nums)` — для каждого числа строка `"чёт"` или `"нечет"`.

        ```
        parity([1, 2, 3])   # → ["нечет", "чёт", "нечет"]
        ```
        """),
        """
        def parity(nums):
            pass
        """,
        """
        def test_values():
            assert parity([1, 2, 3]) == ["нечет", "чёт", "нечет"] and parity([]) == [], "Неверный результат"
        """,
        """
        def parity(nums):
            return ["чёт" if n % 2 == 0 else "нечет" for n in nums]
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `clip_negative(nums)` — отрицательные числа заменить нулями, остальные оставить.

        ```
        clip_negative([3, -1, 5, -9])   # → [3, 0, 5, 0]
        ```
        """),
        """
        def clip_negative(nums):
            pass
        """,
        """
        def test_values():
            assert clip_negative([3, -1, 5, -9]) == [3, 0, 5, 0] and clip_negative([]) == [], "Неверный результат"
        """,
        """
        def clip_negative(nums):
            return [n if n >= 0 else 0 for n in nums]
        """),
    cod(f"{P}-m1-l3-e6", t("""
        Напиши функцию `icons(statuses)` — `"✅"` для `"pass"`, `"❌"` для всего остального.

        ```
        icons(["pass", "fail", "skip"])   # → ["✅", "❌", "❌"]
        ```
        """),
        """
        def icons(statuses):
            pass
        """,
        """
        def test_values():
            assert icons(["pass", "fail", "skip"]) == ["✅", "❌", "❌"], "Неверный результат"
        """,
        """
        def icons(statuses):
            return ["✅" if s == "pass" else "❌" for s in statuses]
        """),
    cod(f"{P}-m1-l3-e7", t("""
        Напиши функцию `fizzbuzz(n)` — список для чисел от 1 до `n`: `"FizzBuzz"` для кратных 15, `"Fizz"` для кратных 3, `"Buzz"` для кратных 5, иначе само число. Одним включением с вложенными условными выражениями.

        ```
        fizzbuzz(5)   # → [1, 2, "Fizz", 4, "Buzz"]
        ```
        """),
        """
        def fizzbuzz(n):
            pass
        """,
        """
        def test_values():
            got = fizzbuzz(15)
            assert got[:5] == [1, 2, "Fizz", 4, "Buzz"] and got[14] == "FizzBuzz" and got[5] == "Fizz" and fizzbuzz(0) == [], f"Получено {got}"
        """,
        """
        def fizzbuzz(n):
            return ["FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else i for i in range(1, n + 1)]
        """, xp=20),
    cod(f"{P}-m1-l3-e8", t("""
        Напиши функцию `server_errors_flags(codes)` — для кодов `>= 400` (остальные отбросить) вернуть `True`, если это ошибка сервера (`>= 500`), иначе `False`.

        ```
        server_errors_flags([200, 404, 503])   # → [False, True]
        ```
        """),
        """
        def server_errors_flags(codes):
            pass
        """,
        """
        def test_values():
            assert server_errors_flags([200, 404, 503]) == [False, True] and server_errors_flags([200]) == [], "Неверный результат"
        """,
        """
        def server_errors_flags(codes):
            return [c >= 500 for c in codes if c >= 400]
        """, hint="Сравнение само даёт True/False — if-else не нужен."),
),

lesson(f"{P}-m1-l4", "Функции, методы, enumerate и zip во включениях",
    out(f"{P}-m1-l4-e1", "Что выведет программа?", """
        raw = [" Anna ", "BOB", "  cat"]
        print([s.strip().lower() for s in raw])
        print([int(x) for x in "1 2 3".split()])
        """),
    out(f"{P}-m1-l4-e2", "Что выведет программа?", """
        names = ["a", "b", "c"]
        print([f"{i}. {n}" for i, n in enumerate(names, start=1)])
        print([a * b for a, b in zip([1, 2, 3], [10, 20, 30])])
        """),
    out(f"{P}-m1-l4-e3", "Что выведет программа?", """
        def square(x):
            return x * x

        print([square(x) for x in range(4)])
        print([len(w) for w in "мама мыла раму".split() if len(w) > 3])
        """),
    cod(f"{P}-m1-l4-e4", t("""
        Напиши функцию `clean(emails)` — убрать пробелы по краям и перевести в нижний регистр каждый email.

        ```
        clean([" Anna@Mail.ru ", "BOB@x.io"])   # → ["anna@mail.ru", "bob@x.io"]
        ```
        """),
        """
        def clean(emails):
            pass
        """,
        """
        def test_values():
            assert clean([" Anna@Mail.ru ", "BOB@x.io"]) == ["anna@mail.ru", "bob@x.io"], "Неверный результат"
        """,
        """
        def clean(emails):
            return [e.strip().lower() for e in emails]
        """),
    cod(f"{P}-m1-l4-e5", t("""
        Напиши функцию `parse_ints(text)` — строку чисел через запятую превратить в список `int`; пустые элементы пропустить.

        ```
        parse_ints("1, 2,,3")   # → [1, 2, 3]
        ```
        """),
        """
        def parse_ints(text):
            pass
        """,
        """
        def test_values():
            assert parse_ints("1, 2,,3") == [1, 2, 3] and parse_ints("") == [] and parse_ints(" 7 ") == [7], "Неверный результат"
        """,
        """
        def parse_ints(text):
            return [int(part) for part in text.split(",") if part.strip()]
        """, hint="int(' 2') работает — пробелы по краям int терпит."),
    cod(f"{P}-m1-l4-e6", t("""
        Напиши функцию `numbered(items)` — строки `"<номер>) <элемент>"`, нумерация с 1, через `enumerate`.

        ```
        numbered(["login", "pay"])   # → ["1) login", "2) pay"]
        ```
        """),
        """
        def numbered(items):
            pass
        """,
        """
        def test_values():
            assert numbered(["login", "pay"]) == ["1) login", "2) pay"] and numbered([]) == [], "Неверный результат"
        """,
        """
        def numbered(items):
            return [f"{i}) {x}" for i, x in enumerate(items, start=1)]
        """),
    cod(f"{P}-m1-l4-e7", t("""
        Напиши функцию `line_totals(prices, qtys)` — стоимости строк заказа: цена × количество попарно (`zip`).

        ```
        line_totals([100, 50], [2, 3])   # → [200, 150]
        ```
        """),
        """
        def line_totals(prices, qtys):
            pass
        """,
        """
        def test_values():
            assert line_totals([100, 50], [2, 3]) == [200, 150] and line_totals([], []) == [], "Неверный результат"
        """,
        """
        def line_totals(prices, qtys):
            return [p * q for p, q in zip(prices, qtys)]
        """),
    cod(f"{P}-m1-l4-e8", t("""
        Напиши функцию `mismatches(expected, actual)` — номера (с 1) позиций, где значения двух списков различаются.

        ```
        mismatches([200, 201, 404], [200, 500, 404])   # → [2]
        ```
        """),
        """
        def mismatches(expected, actual):
            pass
        """,
        """
        def test_values():
            assert mismatches([200, 201, 404], [200, 500, 404]) == [2] and mismatches([1, 2], [3, 4]) == [1, 2] and mismatches([], []) == [], "Неверный результат"
        """,
        """
        def mismatches(expected, actual):
            return [i for i, (e, a) in enumerate(zip(expected, actual), start=1) if e != a]
        """),
),
)
