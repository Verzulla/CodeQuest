"""Тема «sorted, filter и map», модуль 3 «Другие помощники» — задания. Теория — в _srt_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "srt"

m3 = module(f"{P}-m3", "Другие помощники", "🧰", "min/max с key, reversed, enumerate, zip, any/all и конвейеры данных",

lesson(f"{P}-m3-l1", "min и max с key и default",
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        words = ["banana", "fig", "kiwi"]
        print(min(words), max(words))
        print(min(words, key=len), max(words, key=len))
        """, hint="Без key строки сравниваются по алфавиту."),
    out(f"{P}-m3-l1-e2", "Что выведет программа? Пустая коллекция.", """
        print(max([], default=0), min([], default=None))
        try:
            max([])
        except ValueError:
            print("ValueError: пустая последовательность")
        """),
    out(f"{P}-m3-l1-e3", "Что выведет программа? Равные ключи.", """
        users = [("Аня", 30), ("Боря", 30), ("Вика", 25)]
        print(max(users, key=lambda u: u[1]))
        print(min(users, key=lambda u: u[1])[0])
        """, hint="При равенстве max и min возвращают первый."),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `longest(words)` — самое длинное слово (первое при равенстве); пустой список — `""`.
        """),
        """
        def longest(words):
            pass
        """,
        """
        def test_values():
            assert [longest(["banana", "fig", "apples"]), longest([])] == ["banana", ""], "Неверный результат"
        """,
        """
        def longest(words):
            return max(words, key=len, default="")
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `cheapest(products)` — название самого дешёвого товара из списка словарей `name`, `price`; пустой — `None`.
        """),
        """
        def cheapest(products):
            pass
        """,
        """
        def test_values():
            assert cheapest([{"name": "a", "price": 30}, {"name": "b", "price": 10}]) == "b" and cheapest([]) is None, "Неверный результат"
        """,
        """
        def cheapest(products):
            best = min(products, key=lambda p: p["price"], default=None)
            return best["name"] if best else None
        """),
    cod(f"{P}-m3-l1-e6", t("""
        Напиши функцию `top_scorer(scores)` — имя с наибольшим числом очков из словаря `{имя: очки}`.

        ```
        top_scorer({"Аня": 80, "Боря": 95})   # → "Боря"
        ```
        """),
        """
        def top_scorer(scores):
            pass
        """,
        """
        def test_values():
            assert top_scorer({"Аня": 80, "Боря": 95, "Вика": 70}) == "Боря", "Неверный результат"
        """,
        """
        def top_scorer(scores):
            return max(scores, key=scores.get)
        """),
    cod(f"{P}-m3-l1-e7", t("""
        Напиши функцию `closest(nums, target)` — число из списка, ближайшее к `target` (при равенстве — первое).

        ```
        closest([1, 5, 9], 6)   # → 5
        ```
        """),
        """
        def closest(nums, target):
            pass
        """,
        """
        def test_values():
            assert [closest([1, 5, 9], 6), closest([1, 5, 9], 7), closest([10], 0)] == [5, 5, 10], "Неверный результат"
        """,
        """
        def closest(nums, target):
            return min(nums, key=lambda n: abs(n - target))
        """),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `range_of(nums)` — разница между максимумом и минимумом; для пустого списка — `0`. Используй `default`.
        """),
        """
        def range_of(nums):
            pass
        """,
        """
        def test_values():
            assert [range_of([3, 9, 1]), range_of([]), range_of([5])] == [8, 0, 0], "Неверный результат"
        """,
        """
        def range_of(nums):
            return max(nums, default=0) - min(nums, default=0)
        """),
),

lesson(f"{P}-m3-l2", "reversed, enumerate и zip",
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        items = ["a", "b", "c"]
        print(list(reversed(items)), items)
        for i, x in enumerate(reversed(items), start=1):
            print(i, x)
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа? zip и распаковка.", """
        names = ["Аня", "Боря"]
        ages = [25, 30]
        pairs = list(zip(names, ages))
        print(pairs)
        n, a = zip(*pairs)
        print(n, a)
        """, hint="zip(*pairs) — «обратный» zip: разложить пары обратно."),
    out(f"{P}-m3-l2-e3", "Что выведет программа? Разная длина.", """
        print(list(zip([1, 2, 3], "ab")))
        try:
            list(zip([1, 2, 3], "ab", strict=True))
        except ValueError:
            print("strict: разная длина")
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши функцию `last_n_reversed(items, n)` — последние `n` элементов в обратном порядке (самый последний — первым). Используй `reversed`.

        ```
        last_n_reversed(["a", "b", "c", "d"], 2)   # → ["d", "c"]
        ```
        """),
        """
        def last_n_reversed(items, n):
            pass
        """,
        """
        def test_values():
            assert [last_n_reversed(["a", "b", "c", "d"], 2), last_n_reversed(["a"], 5), last_n_reversed([], 1)] == [["d", "c"], ["a"], []], "Неверный результат"
        """,
        """
        def last_n_reversed(items, n):
            return list(reversed(items))[:n]
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `to_dict(keys, values)` — словарь из двух списков через `zip`.
        """),
        """
        def to_dict(keys, values):
            pass
        """,
        """
        def test_values():
            assert to_dict(["a", "b"], [1, 2]) == {"a": 1, "b": 2} and to_dict([], []) == {}, "Неверный словарь"
        """,
        """
        def to_dict(keys, values):
            return dict(zip(keys, values))
        """),
    cod(f"{P}-m3-l2-e6", t("""
        Напиши функцию `unzip(pairs)` — из списка пар вернуть два списка: первые элементы и вторые. Для пустого — `([], [])`.

        ```
        unzip([("a", 1), ("b", 2)])   # → (["a", "b"], [1, 2])
        ```
        """),
        """
        def unzip(pairs):
            pass
        """,
        """
        def test_values():
            assert unzip([("a", 1), ("b", 2)]) == (["a", "b"], [1, 2]) and unzip([]) == ([], []), "Неверный результат"
        """,
        """
        def unzip(pairs):
            if not pairs:
                return [], []
            first, second = zip(*pairs)
            return list(first), list(second)
        """, hint="zip(*pairs) раскладывает пары обратно; для пустого списка распаковка не сработает."),
    cod(f"{P}-m3-l2-e7", t("""
        Напиши функцию `diffs(expected, actual)` — строки `"#<номер с 1>: <e> != <a>"` для несовпадающих позиций. Если длины списков разные — выбросить `ValueError` (используй `zip(..., strict=True)`).
        """),
        """
        def diffs(expected, actual):
            pass
        """,
        """
        def test_values():
            assert diffs([1, 2, 3], [1, 5, 3]) == ["#2: 2 != 5"] and diffs([], []) == [], "Неверный результат"

        def test_strict():
            try:
                diffs([1], [1, 2])
            except ValueError:
                return
            assert False, "Разная длина — ValueError"
        """,
        """
        def diffs(expected, actual):
            return [f"#{i}: {e} != {a}" for i, (e, a) in enumerate(zip(expected, actual, strict=True), start=1) if e != a]
        """, xp=20),
    cod(f"{P}-m3-l2-e8", t("""
        Напиши функцию `numbered_report(results)` — для списка пар `(имя, статус)` строки `"<N>. <имя>: <статус>"`, нумерация с 1.
        """),
        """
        def numbered_report(results):
            pass
        """,
        """
        def test_values():
            assert numbered_report([("login", "pass"), ("pay", "fail")]) == ["1. login: pass", "2. pay: fail"], "Неверный отчёт"
        """,
        """
        def numbered_report(results):
            return [f"{i}. {name}: {status}" for i, (name, status) in enumerate(results, start=1)]
        """),
),

lesson(f"{P}-m3-l3", "any, all и подсчёты с условием",
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        codes = [200, 201, 404]
        print(any(c >= 400 for c in codes), all(c < 500 for c in codes))
        print(any([]), all([]))
        """, hint="any пустого — False, all пустого — True."),
    out(f"{P}-m3-l3-e2", "Что выведет программа?", """
        print(any([0, "", None]), any([0, "x"]), all([1, "a", [0]]), all([1, []]))
        """),
    out(f"{P}-m3-l3-e3", "Что выведет программа? Подсчёт True.", """
        results = ["pass", "fail", "pass"]
        print(sum(r == "pass" for r in results))
        print(sum(1 for r in results if r == "fail"))
        """, hint="True считается как 1, False — как 0."),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `all_passed(results)` — все ли статусы равны `"pass"`.
        """),
        """
        def all_passed(results):
            pass
        """,
        """
        def test_values():
            assert [all_passed(["pass", "pass"]), all_passed(["pass", "fail"]), all_passed([])] == [True, False, True], "Неверный результат"
        """,
        """
        def all_passed(results):
            return all(r == "pass" for r in results)
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `has_server_error(codes)` — есть ли хоть один код `5xx`.
        """),
        """
        def has_server_error(codes):
            pass
        """,
        """
        def test_values():
            assert [has_server_error([200, 503]), has_server_error([404]), has_server_error([])] == [True, False, False], "Неверный результат"
        """,
        """
        def has_server_error(codes):
            return any(500 <= c < 600 for c in codes)
        """),
    cod(f"{P}-m3-l3-e6", t("""
        Напиши функцию `count_passed(results)` — количество `"pass"` через `sum` с логическими значениями.
        """),
        """
        def count_passed(results):
            pass
        """,
        """
        def test_values():
            assert [count_passed(["pass", "fail", "pass"]), count_passed([])] == [2, 0], "Неверный подсчёт"
        """,
        """
        def count_passed(results):
            return sum(r == "pass" for r in results)
        """),
    cod(f"{P}-m3-l3-e7", t("""
        Напиши функцию `strong_password(p)` — пароль длиной не меньше 8, в котором есть хоть одна цифра, хоть одна заглавная и хоть одна строчная буква.
        """),
        """
        def strong_password(p):
            pass
        """,
        """
        def test_values():
            got = [strong_password("Secret123"), strong_password("secret123"), strong_password("SECRET123"), strong_password("Secretxx"), strong_password("Ab1")]
            assert got == [True, False, False, False, False], f"Получено {got}"
        """,
        """
        def strong_password(p):
            return (len(p) >= 8
                    and any(ch.isdigit() for ch in p)
                    and any(ch.isupper() for ch in p)
                    and any(ch.islower() for ch in p))
        """),
    cod(f"{P}-m3-l3-e8", t("""
        Напиши функцию `response_valid(items)` — у **всех** объектов списка есть поле `"id"` и оно — положительное целое (не `bool`).
        """),
        """
        def response_valid(items):
            pass
        """,
        """
        def test_values():
            got = [response_valid([{"id": 1}, {"id": 2}]), response_valid([{"id": 0}]), response_valid([{"x": 1}]), response_valid([{"id": True}]), response_valid([])]
            assert got == [True, False, False, False, True], f"Получено {got}"
        """,
        """
        def response_valid(items):
            return all(isinstance(i.get("id"), int) and not isinstance(i.get("id"), bool) and i["id"] > 0 for i in items)
        """),
),

lesson(f"{P}-m3-l4", "Практика: конвейер обработки данных",
    out(f"{P}-m3-l4-e1", "Что выведет программа?", """
        log = ["INFO start", "ERROR db", "WARN slow", "ERROR api", "ERROR db"]
        errors = [line.split()[1] for line in log if line.startswith("ERROR")]
        print(sorted(set(errors)), max(set(errors), key=errors.count))
        """),
    out(f"{P}-m3-l4-e2", "Что выведет программа?", """
        results = [("login", 1.2, "pass"), ("pay", 3.4, "fail"), ("cart", 0.5, "pass")]
        passed = filter(lambda r: r[2] == "pass", results)
        names = map(lambda r: r[0], sorted(passed, key=lambda r: r[1]))
        print(list(names))
        """),
    out(f"{P}-m3-l4-e3", "Что выведет программа?", """
        prices = ["100", " 250 ", "", "x", "40"]
        clean = [int(p) for p in map(str.strip, prices) if p.isdigit()]
        print(clean, sum(clean), max(clean, default=0))
        """),
    cod(f"{P}-m3-l4-e4", t("""
        Напиши функцию `top_errors(log, n)` — `n` самых частых текстов ошибок из строк `"LEVEL текст"` (только уровень `ERROR`), по убыванию частоты; при равной частоте — по алфавиту.

        ```
        top_errors(["ERROR db", "ERROR api", "ERROR db", "INFO x"], 2)   # → ["db", "api"]
        ```
        """),
        """
        def top_errors(log, n):
            pass
        """,
        """
        def test_values():
            log = ["ERROR db", "ERROR api", "ERROR db", "INFO x", "ERROR cache"]
            assert top_errors(log, 2) == ["db", "api"] and top_errors([], 3) == [], "Неверный результат"
        """,
        """
        def top_errors(log, n):
            errors = [line.split(" ", 1)[1] for line in log if line.startswith("ERROR ")]
            unique = set(errors)
            return sorted(unique, key=lambda e: (-errors.count(e), e))[:n]
        """, xp=20),
    cod(f"{P}-m3-l4-e5", t("""
        Напиши функцию `fast_passed(results, limit)` — имена прошедших тестов, которые шли меньше `limit` секунд, отсортированные по времени. `results` — список кортежей `(имя, время, статус)`.
        """),
        """
        def fast_passed(results, limit):
            pass
        """,
        """
        def test_values():
            res = [("login", 1.2, "pass"), ("pay", 0.4, "fail"), ("cart", 0.5, "pass"), ("x", 3, "pass")]
            assert fast_passed(res, 2) == ["cart", "login"] and fast_passed([], 1) == [], "Неверный результат"
        """,
        """
        def fast_passed(results, limit):
            ok = [r for r in results if r[2] == "pass" and r[1] < limit]
            return [r[0] for r in sorted(ok, key=lambda r: r[1])]
        """),
    cod(f"{P}-m3-l4-e6", t("""
        Напиши функцию `clean_prices(raw)` — из списка строк оставить только целые числа (после `strip`), вернуть их отсортированный по убыванию список.

        ```
        clean_prices(["100", " 250 ", "", "x", "40"])   # → [250, 100, 40]
        ```
        """),
        """
        def clean_prices(raw):
            pass
        """,
        """
        def test_values():
            assert clean_prices(["100", " 250 ", "", "x", "40"]) == [250, 100, 40] and clean_prices([]) == [], "Неверный результат"
        """,
        """
        def clean_prices(raw):
            return sorted((int(p) for p in map(str.strip, raw) if p.isdigit()), reverse=True)
        """),
    cod(f"{P}-m3-l4-e7", t("""
        Напиши функцию `summary(results)` — словарь сводки для списка словарей `name`, `status`, `time`:

        - `"total"` — количество;
        - `"passed"` — количество `pass`;
        - `"slowest"` — имя самого долгого (или `None`);
        - `"all_green"` — все ли `pass`.
        """),
        """
        def summary(results):
            pass
        """,
        """
        def test_values():
            res = [{"name": "a", "status": "pass", "time": 1}, {"name": "b", "status": "fail", "time": 3}]
            assert summary(res) == {"total": 2, "passed": 1, "slowest": "b", "all_green": False}, f"Получено {summary(res)}"
            assert summary([]) == {"total": 0, "passed": 0, "slowest": None, "all_green": True}, "Пустой прогон"
        """,
        """
        def summary(results):
            slowest = max(results, key=lambda r: r["time"], default=None)
            return {
                "total": len(results),
                "passed": sum(r["status"] == "pass" for r in results),
                "slowest": slowest["name"] if slowest else None,
                "all_green": all(r["status"] == "pass" for r in results),
            }
        """, xp=20),
    cod(f"{P}-m3-l4-e8", t("""
        Напиши функцию `merge_sorted_names(*groups)` — объединить несколько списков имён, убрать повторы без учёта регистра (оставить вариант, встретившийся первым) и отсортировать без учёта регистра.

        ```
        merge_sorted_names(["bob", "Anna"], ["anna", "Cat"])   # → ["Anna", "bob", "Cat"]
        ```
        """),
        """
        def merge_sorted_names(*groups):
            pass
        """,
        """
        def test_values():
            assert merge_sorted_names(["bob", "Anna"], ["anna", "Cat"]) == ["Anna", "bob", "Cat"] and merge_sorted_names() == [], "Неверный результат"
        """,
        """
        def merge_sorted_names(*groups):
            seen = {}
            for group in groups:
                for name in group:
                    seen.setdefault(name.lower(), name)
            return sorted(seen.values(), key=str.lower)
        """, hint="Словарь «нижний регистр → первый вариант» с setdefault.", xp=20),
),
)
