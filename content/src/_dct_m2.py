"""Тема «Словари», модуль 2 «Перебор и обработка» — задания. Теория — в _dct_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "dct"

m2 = module(f"{P}-m2", "Перебор и обработка", "🔄", "keys/values/items, изменение при переборе, подсчёт, сортировка, словарь вместо if",

lesson(f"{P}-m2-l1", "Перебор словаря",
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        prices = {"чай": 300, "кофе": 500}
        for item in prices:
            print(item)
        for item, price in prices.items():
            print(f"{item}: {price}")
        print(sum(prices.values()))
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа? Представления «живые».", """
        d = {"a": 1}
        keys = d.keys()
        d["b"] = 2
        print(list(keys))
        print(list(d.values()), list(d.items()))
        """),
    out(f"{P}-m2-l1-e6", "Что выведет программа?", """
        d = {"x": 10, "y": 20}
        print(list(d.keys()), list(d.values()))
        print(list(enumerate(d)))
        for i, (k, v) in enumerate(d.items(), start=1):
            print(i, k, v)
        """),
    cod(f"{P}-m2-l1-e3", t("""
        Напиши функцию `total_cost(cart, prices)` — стоимость корзины. `cart` — словарь `{товар: количество}`, `prices` — `{товар: цена}`.

        ```
        total_cost({"чай": 2, "кофе": 1}, {"чай": 300, "кофе": 500, "сок": 150})   # → 1100
        ```
        """),
        """
        def total_cost(cart, prices):
            pass
        """,
        """
        def test_values():
            assert total_cost({"чай": 2, "кофе": 1}, {"чай": 300, "кофе": 500, "сок": 150}) == 1100 and total_cost({}, {"чай": 1}) == 0, "Неверная стоимость"
        """,
        """
        def total_cost(cart, prices):
            total = 0
            for item, qty in cart.items():
                total += prices[item] * qty
            return total
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `failed_tests(results)` — `results` это словарь `{имя_теста: статус}`. Вернуть **отсортированный** список имён тестов со статусом `"fail"`.

        ```
        failed_tests({"login": "pass", "pay": "fail", "cart": "fail"})   # → ["cart", "pay"]
        ```
        """),
        """
        def failed_tests(results):
            pass
        """,
        """
        def test_values():
            assert failed_tests({"login": "pass", "pay": "fail", "cart": "fail"}) == ["cart", "pay"] and failed_tests({}) == [], "Неверный список"
        """,
        """
        def failed_tests(results):
            return sorted(name for name, status in results.items() if status == "fail")
        """),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `format_headers(headers)` — превратить словарь заголовков в строку, где каждая пара — на отдельной строке в формате `Имя: значение`, в порядке словаря.

        ```
        format_headers({"Content-Type": "application/json", "X-Id": "42"})
        # → "Content-Type: application/json\\nX-Id: 42"
        ```
        """),
        """
        def format_headers(headers):
            pass
        """,
        """
        def test_values():
            assert format_headers({"Content-Type": "application/json", "X-Id": "42"}) == "Content-Type: application/json\\nX-Id: 42", "Неверный формат"
            assert format_headers({}) == "", "Пусто — пустая строка"
        """,
        """
        def format_headers(headers):
            return "\\n".join(f"{name}: {value}" for name, value in headers.items())
        """),
    cod(f"{P}-m2-l1-e7", t("""
        Напиши функцию `max_key(d)` — ключ с наибольшим значением (при равенстве — первый по порядку словаря). Для пустого словаря — `None`. Реши перебором `items()`.

        ```
        max_key({"a": 3, "b": 7, "c": 7})   # → "b"
        ```
        """),
        """
        def max_key(d):
            pass
        """,
        """
        def test_values():
            assert max_key({"a": 3, "b": 7, "c": 7}) == "b" and max_key({}) is None and max_key({"x": -1}) == "x", "Неверный ключ"
        """,
        """
        def max_key(d):
            best_key = None
            best_value = None
            for key, value in d.items():
                if best_value is None or value > best_value:
                    best_key, best_value = key, value
            return best_key
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `filter_by_value(d, min_value)` — новый словарь только с парами, где значение `>= min_value`.

        ```
        filter_by_value({"a": 5, "b": 1, "c": 3}, 3)   # → {"a": 5, "c": 3}
        ```
        """),
        """
        def filter_by_value(d, min_value):
            pass
        """,
        """
        def test_values():
            assert filter_by_value({"a": 5, "b": 1, "c": 3}, 3) == {"a": 5, "c": 3} and filter_by_value({}, 0) == {}, "Неверный результат"
        """,
        """
        def filter_by_value(d, min_value):
            result = {}
            for key, value in d.items():
                if value >= min_value:
                    result[key] = value
            return result
        """),
),

lesson(f"{P}-iter2", "Изменение словаря во время перебора",
    out(f"{P}-iter2-e1", "Что выведет программа?", """
        d = {"a": 1, "b": 2, "c": 3}
        try:
            for k in d:
                if d[k] == 2:
                    del d[k]
        except RuntimeError as e:
            print("RuntimeError:", e)
        """),
    out(f"{P}-iter2-e2", "Что выведет программа? Перебор копии ключей.", """
        d = {"a": 1, "b": 2, "c": 3}
        for k in list(d):
            if d[k] == 2:
                del d[k]
        print(d)
        """),
    out(f"{P}-iter2-e3", "Что выведет программа? Менять значения можно.", """
        d = {"a": 1, "b": 2}
        for k in d:
            d[k] *= 10
        print(d)
        """, hint="Размер словаря не меняется — ошибки нет."),
    cod(f"{P}-iter2-e4", t("""
        Напиши функцию `remove_zeros(d)` — удалить **на месте** все пары со значением `0`. Функция ничего не возвращает. Перебирай копию ключей `list(d)`.

        ```
        d = {"a": 0, "b": 2, "c": 0}
        remove_zeros(d)
        d   # → {"b": 2}
        ```
        """),
        """
        def remove_zeros(d):
            pass
        """,
        """
        def test_values():
            d = {"a": 0, "b": 2, "c": 0}
            assert remove_zeros(d) is None and d == {"b": 2}, f"d = {d}"
        """,
        """
        def remove_zeros(d):
            for key in list(d):
                if d[key] == 0:
                    del d[key]
        """),
    cod(f"{P}-iter2-e5", t("""
        Напиши функцию `without_zeros(d)` — **новый** словарь без пар со значением `0`; исходный не меняется.

        ```
        without_zeros({"a": 0, "b": 2})   # → {"b": 2}
        ```
        """),
        """
        def without_zeros(d):
            pass
        """,
        """
        def test_values():
            src = {"a": 0, "b": 2}
            assert without_zeros(src) == {"b": 2} and src == {"a": 0, "b": 2}, "Неверный результат или исходный изменён"
        """,
        """
        def without_zeros(d):
            return {k: v for k, v in d.items() if v != 0}
        """),
    cod(f"{P}-iter2-e6", t("""
        Напиши функцию `double_values(d)` — удвоить **все значения** словаря на месте. Функция ничего не возвращает.

        ```
        d = {"a": 1, "b": 5}
        double_values(d)
        d   # → {"a": 2, "b": 10}
        ```
        """),
        """
        def double_values(d):
            pass
        """,
        """
        def test_values():
            d = {"a": 1, "b": 5}
            assert double_values(d) is None and d == {"a": 2, "b": 10}, f"d = {d}"
        """,
        """
        def double_values(d):
            for key in d:
                d[key] *= 2
        """),
    cod(f"{P}-iter2-e7", t("""
        Напиши функцию `prune_empty(d)` — удалить на месте пары с «пустыми» значениями: `None`, `""`, `[]`, `{}`. Значения `0` и `False` — **не** пустые, их оставить.

        ```
        d = {"a": None, "b": 0, "c": "", "d": [], "e": False, "f": "x"}
        prune_empty(d)
        d   # → {"b": 0, "e": False, "f": "x"}
        ```
        """),
        """
        def prune_empty(d):
            pass
        """,
        """
        def test_values():
            d = {"a": None, "b": 0, "c": "", "d": [], "e": False, "f": "x", "g": {}}
            prune_empty(d)
            assert d == {"b": 0, "e": False, "f": "x"}, f"d = {d}"
        """,
        """
        def prune_empty(d):
            for key in list(d):
                value = d[key]
                if value is None or value == "" or value == [] or value == {}:
                    del d[key]
        """, hint="not value отбросит и 0, и False — поэтому проверяй пустые значения явно.", xp=20),
    cod(f"{P}-iter2-e8", t("""
        Напиши функцию `rename_keys(d, mapping)` — новый словарь, где ключи переименованы по словарю `mapping` (`старое → новое`); ключи, которых нет в `mapping`, остаются как есть.

        ```
        rename_keys({"userName": "Аня", "id": 1}, {"userName": "user_name"})
        # → {"user_name": "Аня", "id": 1}
        ```
        """),
        """
        def rename_keys(d, mapping):
            pass
        """,
        """
        def test_values():
            assert rename_keys({"userName": "Аня", "id": 1}, {"userName": "user_name"}) == {"user_name": "Аня", "id": 1}, "Неверный результат"
        """,
        """
        def rename_keys(d, mapping):
            return {mapping.get(k, k): v for k, v in d.items()}
        """, hint="mapping.get(k, k) — новое имя или старое, если замены нет."),
),

lesson(f"{P}-m2-l2", "Подсчёт и группировка",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        from collections import Counter
        results = ["pass", "fail", "pass", "skip", "pass"]
        c = Counter(results)
        print(c["pass"], c["error"], c.most_common(1))
        """, hint="Counter возвращает 0 для отсутствующего ключа, без KeyError."),
    out(f"{P}-m2-l2-e2", "Что выведет программа?", """
        from collections import defaultdict
        groups = defaultdict(list)
        for name, team in [("Аня", "qa"), ("Боря", "dev"), ("Вика", "qa")]:
            groups[team].append(name)
        print(dict(groups))
        print(groups["ops"])
        """),
    out(f"{P}-m2-l2-e6", "Что выведет программа?", """
        from collections import Counter
        c = Counter("banana")
        print(c)
        print(c.most_common(2), sum(c.values()))
        """),
    cod(f"{P}-m2-l2-e3", t("""
        Напиши функцию `char_count(text)` — словарь «символ → сколько раз встречается», **без** пробелов, через `get`.

        ```
        char_count("aab c")   # → {"a": 2, "b": 1, "c": 1}
        ```
        """),
        """
        def char_count(text):
            pass
        """,
        """
        def test_values():
            assert char_count("aab c") == {"a": 2, "b": 1, "c": 1} and char_count("") == {}, "Неверный подсчёт"
        """,
        """
        def char_count(text):
            counts = {}
            for ch in text:
                if ch != " ":
                    counts[ch] = counts.get(ch, 0) + 1
            return counts
        """),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `top_errors(log, n)` — `n` самых частых сообщений об ошибках. `log` — список строк `"LEVEL текст"`; учитывай только уровень `ERROR`. Верни список пар `(текст, количество)` по убыванию количества. Используй `Counter.most_common`.

        ```
        log = ["ERROR timeout", "INFO ok", "ERROR db down", "ERROR timeout"]
        top_errors(log, 1)   # → [("timeout", 2)]
        ```
        """),
        """
        from collections import Counter

        def top_errors(log, n):
            pass
        """,
        """
        def test_values():
            log = ["ERROR timeout", "INFO ok", "ERROR db down", "ERROR timeout", "WARN slow"]
            assert top_errors(log, 1) == [("timeout", 2)], f"Получено {top_errors(log, 1)}"
            assert top_errors(log, 5) == [("timeout", 2), ("db down", 1)], f"Получено {top_errors(log, 5)}"
        """,
        """
        from collections import Counter

        def top_errors(log, n):
            errors = [line.split(" ", 1)[1] for line in log if line.startswith("ERROR ")]
            return Counter(errors).most_common(n)
        """, xp=20),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `group_by_first_letter(words)` — сгруппировать слова по первой букве (в нижнем регистре) с помощью `defaultdict(list)`. Вернуть обычный `dict`, слова внутри групп — в исходном порядке.

        ```
        group_by_first_letter(["Apple", "avocado", "banana", "Blueberry", "cherry"])
        # → {"a": ["Apple", "avocado"], "b": ["banana", "Blueberry"], "c": ["cherry"]}
        ```
        """),
        """
        from collections import defaultdict

        def group_by_first_letter(words):
            pass
        """,
        """
        def test_values():
            got = group_by_first_letter(["Apple", "avocado", "banana", "Blueberry", "cherry"])
            assert got == {"a": ["Apple", "avocado"], "b": ["banana", "Blueberry"], "c": ["cherry"]} and type(got) is dict, f"Получено {got!r}"
        """,
        """
        from collections import defaultdict

        def group_by_first_letter(words):
            groups = defaultdict(list)
            for w in words:
                groups[w[0].lower()].append(w)
            return dict(groups)
        """),
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `word_counts(text)` — словарь «слово в нижнем регистре → количество». Используй `Counter` и верни обычный `dict`.

        ```
        word_counts("Тест упал тест")   # → {"тест": 2, "упал": 1}
        ```
        """),
        """
        from collections import Counter

        def word_counts(text):
            pass
        """,
        """
        def test_values():
            got = word_counts("Тест упал тест")
            assert got == {"тест": 2, "упал": 1} and type(got) is dict and word_counts("") == {}, f"Получено {got!r}"
        """,
        """
        from collections import Counter

        def word_counts(text):
            return dict(Counter(text.lower().split()))
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `group_lengths(words)` — словарь «длина слова → список слов такой длины» (в исходном порядке). Используй `defaultdict(list)`, верни обычный `dict`.

        ```
        group_lengths(["api", "ui", "db", "test"])   # → {3: ["api"], 2: ["ui", "db"], 4: ["test"]}
        ```
        """),
        """
        from collections import defaultdict

        def group_lengths(words):
            pass
        """,
        """
        def test_values():
            got = group_lengths(["api", "ui", "db", "test"])
            assert got == {3: ["api"], 2: ["ui", "db"], 4: ["test"]} and type(got) is dict, f"Получено {got!r}"
        """,
        """
        from collections import defaultdict

        def group_lengths(words):
            groups = defaultdict(list)
            for w in words:
                groups[len(w)].append(w)
            return dict(groups)
        """),
),

lesson(f"{P}-m2-l3", "Сортировка словарей",
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        scores = {"Боря": 50, "Аня": 80, "Вика": 65}
        print(sorted(scores))
        print(sorted(scores, key=scores.get, reverse=True))
        print(sorted(scores.items(), key=lambda p: p[1]))
        """),
    out(f"{P}-m2-l3-e2", "Что выведет программа?", """
        d = {"b": 2, "a": 1, "c": 3}
        ordered = dict(sorted(d.items()))
        print(ordered)
        print(max(d, key=d.get), min(d.values()))
        """),
    out(f"{P}-m2-l3-e6", "Что выведет программа?", """
        d = {"b": 1, "a": 3, "c": 2}
        print(sorted(d.values()), sorted(d.items(), key=lambda p: -p[1])[0])
        print(dict(sorted(d.items(), key=lambda p: p[1])))
        """),
    cod(f"{P}-m2-l3-e3", t("""
        Напиши функцию `slowest_tests(times, n)` — имена `n` самых медленных тестов по убыванию времени. `times` — словарь `{имя: секунды}`.

        ```
        slowest_tests({"login": 1.2, "pay": 3.4, "search": 0.2, "cart": 2.0}, 2)   # → ["pay", "cart"]
        ```
        """),
        """
        def slowest_tests(times, n):
            pass
        """,
        """
        def test_values():
            assert slowest_tests({"login": 1.2, "pay": 3.4, "search": 0.2, "cart": 2.0}, 2) == ["pay", "cart"], "Неверный результат"
            assert slowest_tests({}, 3) == [], "Пусто — пусто"
        """,
        """
        def slowest_tests(times, n):
            return sorted(times, key=times.get, reverse=True)[:n]
        """),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `sort_by_value_then_key(d)` — вернуть список ключей, отсортированных по значению **по убыванию**, а при равных значениях — по ключу **по алфавиту**.

        ```
        sort_by_value_then_key({"b": 2, "a": 2, "c": 5, "d": 1})   # → ["c", "a", "b", "d"]
        ```
        """),
        """
        def sort_by_value_then_key(d):
            pass
        """,
        """
        def test_values():
            assert sort_by_value_then_key({"b": 2, "a": 2, "c": 5, "d": 1}) == ["c", "a", "b", "d"], f"Получено {sort_by_value_then_key({'b': 2, 'a': 2, 'c': 5, 'd': 1})}"
        """,
        """
        def sort_by_value_then_key(d):
            return [k for k, _ in sorted(d.items(), key=lambda p: (-p[1], p[0]))]
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `report(stats)` — строки отчёта `"<статус>: <кол-во>"` для словаря `{статус: количество}`, отсортированные по количеству по убыванию. Статусы с нулевым количеством пропустить.

        ```
        report({"passed": 42, "failed": 3, "skipped": 0, "error": 1})
        # → ["passed: 42", "failed: 3", "error: 1"]
        ```
        """),
        """
        def report(stats):
            pass
        """,
        """
        def test_values():
            assert report({"passed": 42, "failed": 3, "skipped": 0, "error": 1}) == ["passed: 42", "failed: 3", "error: 1"], f"Получено {report({'passed': 42, 'failed': 3, 'skipped': 0, 'error': 1})}"
        """,
        """
        def report(stats):
            ordered = sorted(stats.items(), key=lambda p: p[1], reverse=True)
            return [f"{status}: {count}" for status, count in ordered if count > 0]
        """),
    cod(f"{P}-m2-l3-e7", t("""
        Напиши функцию `rank(scores)` — словарь «имя → место» (с 1) по убыванию очков. Очки у всех разные.

        ```
        rank({"Боря": 50, "Аня": 80, "Вика": 65})   # → {"Аня": 1, "Вика": 2, "Боря": 3}
        ```
        """),
        """
        def rank(scores):
            pass
        """,
        """
        def test_values():
            assert rank({"Боря": 50, "Аня": 80, "Вика": 65}) == {"Аня": 1, "Вика": 2, "Боря": 3} and rank({}) == {}, "Неверные места"
        """,
        """
        def rank(scores):
            ordered = sorted(scores, key=scores.get, reverse=True)
            return {name: place for place, name in enumerate(ordered, start=1)}
        """),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `top_n_dict(d, n)` — новый словарь из `n` пар с наибольшими значениями, **упорядоченный** по убыванию значения.

        ```
        top_n_dict({"a": 1, "b": 5, "c": 3, "d": 4}, 2)   # → {"b": 5, "d": 4}
        ```
        """),
        """
        def top_n_dict(d, n):
            pass
        """,
        """
        def test_values():
            got = top_n_dict({"a": 1, "b": 5, "c": 3, "d": 4}, 2)
            assert got == {"b": 5, "d": 4} and list(got) == ["b", "d"], f"Получено {got}"
        """,
        """
        def top_n_dict(d, n):
            ordered = sorted(d.items(), key=lambda p: p[1], reverse=True)
            return dict(ordered[:n])
        """),
),

lesson(f"{P}-lookup", "Словарь вместо if/elif",
    out(f"{P}-lookup-e1", "Что выведет программа?", """
        def emoji(status):
            icons = {"pass": "✅", "fail": "❌", "skip": "⏭"}
            return icons.get(status, "❓")

        print(emoji("pass"), emoji("fail"), emoji("error"))
        """),
    out(f"{P}-lookup-e2", "Что выведет программа? Функции в словаре.", """
        ops = {"+": lambda a, b: a + b, "*": lambda a, b: a * b}
        print(ops["+"](2, 3), ops["*"](2, 3), "-" in ops)
        """),
    out(f"{P}-lookup-e3", "Что выведет программа? Замена символов по таблице.", """
        layout = {"q": "й", "w": "ц", "e": "у"}
        word = "qwe"
        print("".join(layout.get(ch, ch) for ch in word + "!"))
        """),
    cod(f"{P}-lookup-e4", t("""
        Напиши функцию `day_type(day)` — `"выходной"` для `"сб"` и `"вс"`, `"будний"` для остальных. Используй словарь и `get` с умолчанием, без `if`.

        ```
        day_type("сб")   # → "выходной"
        day_type("пн")   # → "будний"
        ```
        """),
        """
        def day_type(day):
            pass
        """,
        """
        def test_values():
            assert [day_type(d) for d in ("сб", "вс", "пн", "xx")] == ["выходной", "выходной", "будний", "будний"], "Неверный тип дня"

        def test_no_if():
            assert "if " not in open("solution.py", encoding="utf-8").read(), "Реши словарём, без if"
        """,
        """
        def day_type(day):
            return {"сб": "выходной", "вс": "выходной"}.get(day, "будний")
        """),
    cod(f"{P}-lookup-e5", t("""
        Напиши функцию `http_category(code)` — категория HTTP-кода по первой цифре: `1` → `"info"`, `2` → `"success"`, `3` → `"redirect"`, `4` → `"client error"`, `5` → `"server error"`, иначе `"unknown"`. Первая цифра — `code // 100`; используй словарь.

        ```
        http_category(404)   # → "client error"
        http_category(700)   # → "unknown"
        ```
        """),
        """
        def http_category(code):
            pass
        """,
        """
        def test_values():
            got = [http_category(c) for c in (101, 200, 301, 404, 503, 700)]
            assert got == ["info", "success", "redirect", "client error", "server error", "unknown"], f"Получено {got}"
        """,
        """
        CATEGORIES = {1: "info", 2: "success", 3: "redirect", 4: "client error", 5: "server error"}

        def http_category(code):
            return CATEGORIES.get(code // 100, "unknown")
        """),
    cod(f"{P}-lookup-e6", t("""
        Напиши функцию `run_command(cmd, text)` — применить к строке команду из словаря обработчиков: `"upper"` → `str.upper`, `"lower"` → `str.lower`, `"title"` → `str.title`. Неизвестная команда — вернуть `"неизвестная команда"`.

        ```
        run_command("upper", "hi")    # → "HI"
        run_command("title", "abc")   # → "Abc"
        run_command("x", "abc")       # → "неизвестная команда"
        ```
        """),
        """
        def run_command(cmd, text):
            pass
        """,
        """
        def test_values():
            got = [run_command("upper", "hi"), run_command("title", "abc"), run_command("lower", "AB"), run_command("x", "abc")]
            assert got == ["HI", "Abc", "ab", "неизвестная команда"], f"Получено {got}"
        """,
        """
        HANDLERS = {"upper": str.upper, "lower": str.lower, "title": str.title}

        def run_command(cmd, text):
            handler = HANDLERS.get(cmd)
            if handler is None:
                return "неизвестная команда"
            return handler(text)
        """),
    cod(f"{P}-lookup-e7", t("""
        Напиши функцию `transliterate(text)` — заменить русские буквы латинскими по словарю `TR` из заготовки; символы, которых нет в словаре, оставить как есть.

        ```
        transliterate("кот")    # → "kot"
        transliterate("мак!")   # → "mak!"
        ```
        """),
        """
        TR = {"к": "k", "о": "o", "т": "t", "м": "m", "а": "a"}

        def transliterate(text):
            pass
        """,
        """
        def test_values():
            assert transliterate("кот") == "kot" and transliterate("мак!") == "mak!" and transliterate("") == "", "Неверная транслитерация"
        """,
        """
        TR = {"к": "k", "о": "o", "т": "t", "м": "m", "а": "a"}

        def transliterate(text):
            return "".join(TR.get(ch, ch) for ch in text)
        """),
    cod(f"{P}-lookup-e8", t("""
        Напиши функцию `roman_to_int(s)` — перевести римское число в обычное. Значения букв храни в словаре: `I=1, V=5, X=10, L=50, C=100, D=500, M=1000`.

        Правило: если буква меньше **следующей**, её значение вычитается (IV = 4, XC = 90), иначе прибавляется.

        ```
        roman_to_int("XIV")       # → 14
        roman_to_int("MCMXCIV")   # → 1994
        ```
        """),
        """
        def roman_to_int(s):
            pass
        """,
        """
        def test_values():
            got = [roman_to_int(s) for s in ("III", "IV", "IX", "XIV", "LVIII", "MCMXCIV")]
            assert got == [3, 4, 9, 14, 58, 1994], f"Получено {got}"
        """,
        """
        VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

        def roman_to_int(s):
            total = 0
            for i in range(len(s)):
                value = VALUES[s[i]]
                if i + 1 < len(s) and value < VALUES[s[i + 1]]:
                    total -= value
                else:
                    total += value
            return total
        """, xp=25),
),
)
