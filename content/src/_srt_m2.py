"""Тема «sorted, filter и map», модуль 2 «filter и map» — задания. Теория — в _srt_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "srt"

m2 = module(f"{P}-m2", "filter и map", "🧪", "Фильтрация и преобразование функциями, сравнение с включениями, ленивость",

lesson(f"{P}-m2-l1", "filter: оставить подходящие",
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        def is_even(n):
            return n % 2 == 0

        print(list(filter(is_even, [1, 2, 3, 4])))
        print(list(filter(lambda s: len(s) > 2, ["a", "api", "ui", "test"])))
        """, hint="filter(функция, коллекция) оставляет элементы, для которых функция вернула истину."),
    out(f"{P}-m2-l1-e2", "Что выведет программа? filter с None.", """
        values = [0, 1, "", "a", None, [], [0], False]
        print(list(filter(None, values)))
        """, hint="None вместо функции — оставить «истинные» значения."),
    out(f"{P}-m2-l1-e3", "Что выведет программа?", """
        f = filter(str.isdigit, ["12", "x", "7"])
        print(type(f).__name__)
        print(list(f))
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `positives(nums)` — положительные числа через `filter` (результат — список).

        ```
        positives([3, -1, 0, 5])   # → [3, 5]
        ```
        """),
        """
        def positives(nums):
            pass
        """,
        """
        def test_values():
            assert positives([3, -1, 0, 5]) == [3, 5] and positives([]) == [], "Неверный результат"

        def test_filter():
            assert "filter(" in open("solution.py", encoding="utf-8").read(), "Используй filter"
        """,
        """
        def positives(nums):
            return list(filter(lambda n: n > 0, nums))
        """),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `non_empty(strings)` — убрать пустые строки, используя `filter(None, ...)`.

        ```
        non_empty(["a", "", "b", ""])   # → ["a", "b"]
        ```
        """),
        """
        def non_empty(strings):
            pass
        """,
        """
        def test_values():
            assert non_empty(["a", "", "b", ""]) == ["a", "b"] and non_empty([]) == [], "Неверный результат"

        def test_filter_none():
            assert "filter(None" in open("solution.py", encoding="utf-8").read(), "Используй filter(None, ...)"
        """,
        """
        def non_empty(strings):
            return list(filter(None, strings))
        """),
    cod(f"{P}-m2-l1-e6", t("""
        Напиши функцию `digits_only(items)` — строки, состоящие только из цифр. Передай в `filter` метод `str.isdigit`.

        ```
        digits_only(["12", "x1", "7"])   # → ["12", "7"]
        ```
        """),
        """
        def digits_only(items):
            pass
        """,
        """
        def test_values():
            assert digits_only(["12", "x1", "7", ""]) == ["12", "7"], "Неверный результат"
        """,
        """
        def digits_only(items):
            return list(filter(str.isdigit, items))
        """),
    cod(f"{P}-m2-l1-e7", t("""
        Напиши функцию `failed(results)` — словари результатов со статусом `"fail"` через `filter`.

        ```
        failed([{"n": "a", "status": "pass"}, {"n": "b", "status": "fail"}])   # → [{"n": "b", "status": "fail"}]
        ```
        """),
        """
        def failed(results):
            pass
        """,
        """
        def test_values():
            res = [{"n": "a", "status": "pass"}, {"n": "b", "status": "fail"}]
            assert failed(res) == [res[1]] and failed([]) == [], "Неверный результат"
        """,
        """
        def failed(results):
            return list(filter(lambda r: r["status"] == "fail", results))
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `valid_emails(emails)` — адреса, прошедшие проверку своей функцией `is_valid(email)`: есть ровно один `@`, и после него есть точка.

        ```
        valid_emails(["a@x.ru", "bad", "c@@x.ru", "d@x"])   # → ["a@x.ru"]
        ```
        """),
        """
        def is_valid(email):
            pass

        def valid_emails(emails):
            pass
        """,
        """
        def test_values():
            assert valid_emails(["a@x.ru", "bad", "c@@x.ru", "d@x"]) == ["a@x.ru"], "Неверный результат"
            assert is_valid("q@w.e") is True, "is_valid должна вернуть True для корректного адреса"
        """,
        """
        def is_valid(email):
            return email.count("@") == 1 and "." in email.split("@")[1]

        def valid_emails(emails):
            return list(filter(is_valid, emails))
        """),
),

lesson(f"{P}-m2-l2", "map: преобразовать каждый",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        print(list(map(str.upper, ["api", "ui"])))
        print(list(map(int, "1 2 3".split())))
        print(list(map(lambda x: x * 10, range(3))))
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа? Несколько коллекций.", """
        print(list(map(pow, [2, 3, 4], [3, 2])))
        print(list(map(lambda a, b: a + b, [1, 2], [10, 20])))
        """, hint="map с двумя коллекциями берёт элементы попарно и останавливается на короткой."),
    out(f"{P}-m2-l2-e3", "Что выведет программа?", """
        a, b = map(int, "3 4".split())
        print(a * b)
        print(sum(map(len, ["ab", "cde"])))
        """, hint="Результат map можно сразу распаковать."),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `to_ints(strings)` — список чисел из списка строк через `map`.

        ```
        to_ints(["1", "20", "-3"])   # → [1, 20, -3]
        ```
        """),
        """
        def to_ints(strings):
            pass
        """,
        """
        def test_values():
            assert to_ints(["1", "20", "-3"]) == [1, 20, -3] and to_ints([]) == [], "Неверный результат"

        def test_map():
            assert "map(" in open("solution.py", encoding="utf-8").read(), "Используй map"
        """,
        """
        def to_ints(strings):
            return list(map(int, strings))
        """),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `parse_pair(text)` — строку `"ширина высота"` превратить в два числа и вернуть их произведение. Используй распаковку результата `map`.

        ```
        parse_pair("3 4")   # → 12
        ```
        """),
        """
        def parse_pair(text):
            pass
        """,
        """
        def test_values():
            assert parse_pair("3 4") == 12 and parse_pair(" 10 2 ") == 20, "Неверный результат"
        """,
        """
        def parse_pair(text):
            w, h = map(int, text.split())
            return w * h
        """),
    cod(f"{P}-m2-l2-e6", t("""
        Напиши функцию `total_chars(words)` — суммарная длина слов через `sum` и `map(len, ...)`.

        ```
        total_chars(["ab", "cde"])   # → 5
        ```
        """),
        """
        def total_chars(words):
            pass
        """,
        """
        def test_values():
            assert total_chars(["ab", "cde"]) == 5 and total_chars([]) == 0, "Неверный результат"
        """,
        """
        def total_chars(words):
            return sum(map(len, words))
        """),
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `line_totals(prices, qtys)` — попарные произведения через `map` с двумя коллекциями.

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
            assert line_totals([100, 50], [2, 3]) == [200, 150] and line_totals([1], []) == [], "Неверный результат"
        """,
        """
        def line_totals(prices, qtys):
            return list(map(lambda p, q: p * q, prices, qtys))
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `normalize_all(emails)` — к каждому адресу применить свою функцию `normalize(email)` (убрать пробелы по краям, нижний регистр) через `map`.
        """),
        """
        def normalize(email):
            pass

        def normalize_all(emails):
            pass
        """,
        """
        def test_values():
            assert normalize_all([" A@x.ru ", "B@Y.io"]) == ["a@x.ru", "b@y.io"] and normalize_all([]) == [], "Неверный результат"
        """,
        """
        def normalize(email):
            return email.strip().lower()

        def normalize_all(emails):
            return list(map(normalize, emails))
        """),
),

lesson(f"{P}-m2-l3", "filter и map против включений",
    out(f"{P}-m2-l3-e1", "Что выведет программа? Одно и то же тремя способами.", """
        nums = [1, 2, 3, 4, 5]
        a = list(map(lambda x: x * x, filter(lambda x: x % 2, nums)))
        b = [x * x for x in nums if x % 2]
        c = []
        for x in nums:
            if x % 2:
                c.append(x * x)
        print(a, a == b == c)
        """),
    out(f"{P}-m2-l3-e2", "Что выведет программа?", """
        words = [" a ", "B", " c"]
        print(list(map(str.strip, words)))
        print([w.strip() for w in words])
        """, hint="Готовая функция — map читается хорошо; иначе нагляднее включение."),
    out(f"{P}-m2-l3-e3", "Что выведет программа?", """
        print(list(map(str, range(3))), [str(i) for i in range(3)])
        """),
    cod(f"{P}-m2-l3-e4", t("""
        Перепиши функцию из заготовки **списковым включением** (без `map` и `filter`), сохранив результат.
        """),
        """
        def squares_of_odds(nums):
            return list(map(lambda x: x * x, filter(lambda x: x % 2, nums)))
        """,
        """
        def test_values():
            assert squares_of_odds([1, 2, 3, 4, 5]) == [1, 9, 25] and squares_of_odds([]) == [], "Результат изменился"

        def test_comprehension():
            src = open("solution.py", encoding="utf-8").read()
            assert "map(" not in src and "filter(" not in src, "Используй включение"
        """,
        """
        def squares_of_odds(nums):
            return [x * x for x in nums if x % 2]
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Перепиши функцию из заготовки через `map` и `filter` (без включений и циклов).
        """),
        """
        def upper_long(words):
            return [w.upper() for w in words if len(w) > 2]
        """,
        """
        import re

        def test_values():
            assert upper_long(["a", "api", "test"]) == ["API", "TEST"] and upper_long([]) == [], "Результат изменился"

        def test_map_filter():
            src = open("solution.py", encoding="utf-8").read()
            assert "map(" in src and "filter(" in src and not re.search(r"\\bfor\\b", src), "Используй map и filter без for"
        """,
        """
        def upper_long(words):
            return list(map(str.upper, filter(lambda w: len(w) > 2, words)))
        """),
    cod(f"{P}-m2-l3-e6", t("""
        Напиши функцию `stripped(lines)` — убрать пробелы по краям каждой строки. Когда функция уже готова (`str.strip`), `map` особенно лаконичен.
        """),
        """
        def stripped(lines):
            pass
        """,
        """
        def test_values():
            assert stripped([" a ", "b "]) == ["a", "b"] and stripped([]) == [], "Неверный результат"
        """,
        """
        def stripped(lines):
            return list(map(str.strip, lines))
        """),
    cod(f"{P}-m2-l3-e7", t("""
        Напиши функцию `prices_with_tax(prices)` — цены с налогом 20%, округлённые до 2 знаков. Выбери сам: `map` или включение.

        ```
        prices_with_tax([100, 9.99])   # → [120.0, 11.99]
        ```
        """),
        """
        def prices_with_tax(prices):
            pass
        """,
        """
        def test_values():
            assert prices_with_tax([100, 9.99]) == [120.0, 11.99] and prices_with_tax([]) == [], "Неверный результат"
        """,
        """
        def prices_with_tax(prices):
            return [round(p * 1.2, 2) for p in prices]
        """),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `ids_of_active(users)` — id активных пользователей (`"active": True`). Выбери подходящий инструмент.

        ```
        ids_of_active([{"id": 1, "active": True}, {"id": 2, "active": False}])   # → [1]
        ```
        """),
        """
        def ids_of_active(users):
            pass
        """,
        """
        def test_values():
            assert ids_of_active([{"id": 1, "active": True}, {"id": 2, "active": False}, {"id": 3, "active": True}]) == [1, 3], "Неверный результат"
        """,
        """
        def ids_of_active(users):
            return [u["id"] for u in users if u["active"]]
        """),
),

lesson(f"{P}-m2-l4", "Ленивость: итераторы filter и map",
    out(f"{P}-m2-l4-e1", "Что выведет программа?", """
        m = map(str.upper, ["a", "b"])
        print(type(m).__name__, isinstance(m, list))
        print(list(m))
        """, hint="map возвращает объект-итератор, а не список."),
    out(f"{P}-m2-l4-e2", "Что выведет программа? Итератор расходуется.", """
        m = map(lambda x: x * 2, [1, 2, 3])
        print(list(m))
        print(list(m))
        """),
    out(f"{P}-m2-l4-e3", "Что выведет программа? next и ленивость.", """
        calls = []

        def double(x):
            calls.append(x)
            return x * 2

        m = map(double, [1, 2, 3])
        print(next(m), calls)
        print(next(m), calls)
        """, hint="Функция вызывается только тогда, когда значение запросили."),
    cod(f"{P}-m2-l4-e4", t("""
        Напиши функцию `first_valid(items)` — первое целое число из строк (строки из цифр), или `None`. Используй `next` с `filter` и значением по умолчанию — лишние элементы не будут проверяться.

        ```
        first_valid(["x", "12", "7"])   # → 12
        ```
        """),
        """
        def first_valid(items):
            pass
        """,
        """
        def test_values():
            assert [first_valid(["x", "12", "7"]), first_valid(["x"]), first_valid([])] == [12, None, None], "Неверный результат"
        """,
        """
        def first_valid(items):
            found = next(filter(str.isdigit, items), None)
            return int(found) if found is not None else None
        """),
    cod(f"{P}-m2-l4-e5", t("""
        Функция `stats(nums)` из заготовки возвращает `(0, 0)` вместо суммы и количества положительных: итератор `filter` израсходовался на первом использовании. Исправь, превратив результат в список.

        ```
        stats([3, -1, 5])   # → (8, 2)
        ```
        """),
        """
        def stats(nums):
            pos = filter(lambda n: n > 0, nums)
            total = sum(pos)
            count = len(list(pos))
            return total, count
        """,
        """
        def test_values():
            assert stats([3, -1, 5]) == (8, 2) and stats([]) == (0, 0), "Неверный результат"
        """,
        """
        def stats(nums):
            pos = list(filter(lambda n: n > 0, nums))
            return sum(pos), len(pos)
        """, hint="Итератор можно пройти только один раз. list(...) сохранит значения."),
    cod(f"{P}-m2-l4-e6", t("""
        Напиши функцию `calls_needed(items)` — сколько раз будет вызвана проверка `is_bad`, если искать **первый** плохой элемент через `next(filter(is_bad, items), None)`. Считай вызовы внутри `is_bad`.

        ```
        calls_needed([1, 2, -3, 4, -5])   # → 3   (плохой — отрицательный)
        ```
        """),
        """
        def calls_needed(items):
            pass
        """,
        """
        def test_values():
            assert [calls_needed([1, 2, -3, 4, -5]), calls_needed([1, 2]), calls_needed([-1])] == [3, 2, 1], "Неверный подсчёт"
        """,
        """
        def calls_needed(items):
            calls = 0
            def is_bad(x):
                nonlocal calls
                calls += 1
                return x < 0
            next(filter(is_bad, items), None)
            return calls
        """, xp=20),
    cod(f"{P}-m2-l4-e7", t("""
        Напиши функцию `pipeline(lines)` — ленивая цепочка: очистить строки (`strip`), убрать пустые, превратить в `int`; вернуть **сумму**. Не создавай промежуточных списков — передавай итераторы друг другу.

        ```
        pipeline([" 1 ", "", "2", "  "])   # → 3
        ```
        """),
        """
        def pipeline(lines):
            pass
        """,
        """
        def test_values():
            assert pipeline([" 1 ", "", "2", "  "]) == 3 and pipeline([]) == 0, "Неверная сумма"
        """,
        """
        def pipeline(lines):
            cleaned = map(str.strip, lines)
            non_empty = filter(None, cleaned)
            numbers = map(int, non_empty)
            return sum(numbers)
        """),
    cod(f"{P}-m2-l4-e8", t("""
        Напиши функцию `take(iterable, n)` — первые `n` элементов любого итерируемого объекта (в том числе бесконечного итератора) списком. Используй `next` в цикле; если элементы кончились раньше — вернуть сколько есть.

        ```
        take(map(lambda x: x * x, range(10)), 3)   # → [0, 1, 4]
        ```
        """),
        """
        def take(iterable, n):
            pass
        """,
        """
        import itertools

        def test_values():
            assert take(map(lambda x: x * x, range(10)), 3) == [0, 1, 4] and take([1, 2], 5) == [1, 2], "Неверный результат"
            assert take(itertools.count(), 3) == [0, 1, 2], "Должно работать с бесконечным итератором"
        """,
        """
        def take(iterable, n):
            it = iter(iterable)
            result = []
            for _ in range(n):
                try:
                    result.append(next(it))
                except StopIteration:
                    break
            return result
        """, hint="iter(x) — получить итератор; next бросает StopIteration, когда элементы кончились.", xp=25),
),
)
