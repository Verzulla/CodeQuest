"""Тема «Списковые включения», модуль 2 «Вложенность, словари и генераторы» — задания. Теория — в _cmp_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "cmp"

m2 = module(f"{P}-m2", "Вложенность, словари, генераторы", "🪆", "Два for, матрицы, словарные включения, выражения-генераторы",

lesson(f"{P}-m2-l1", "Два for: сплющивание и комбинации",
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        print([(a, b) for a in [1, 2] for b in "xy"])
        """, hint="for читаются слева направо — как вложенные циклы сверху вниз."),
    out(f"{P}-m2-l1-e2", "Что выведет программа? Сплющивание.", """
        matrix = [[1, 2], [3], [4, 5, 6]]
        print([x for row in matrix for x in row])
        """),
    out(f"{P}-m2-l1-e3", "Что выведет программа?", """
        print([f"{b}@{s}" for b in ["chrome", "ff"] for s in [1920, 375] if not (b == "ff" and s == 375)])
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `flatten(lists)` — склеить список списков в один список одним включением с двумя `for`.

        ```
        flatten([[1, 2], [], [3]])   # → [1, 2, 3]
        ```
        """),
        """
        def flatten(lists):
            pass
        """,
        """
        def test_values():
            assert flatten([[1, 2], [], [3]]) == [1, 2, 3] and flatten([]) == [], "Неверный результат"
        """,
        """
        def flatten(lists):
            return [x for lst in lists for x in lst]
        """),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `test_matrix(browsers, sizes)` — все комбинации `"браузер@размер"` (сначала все размеры для первого браузера).

        ```
        test_matrix(["chrome", "ff"], [1920, 375])   # → ["chrome@1920", "chrome@375", "ff@1920", "ff@375"]
        ```
        """),
        """
        def test_matrix(browsers, sizes):
            pass
        """,
        """
        def test_values():
            assert test_matrix(["chrome", "ff"], [1920, 375]) == ["chrome@1920", "chrome@375", "ff@1920", "ff@375"] and test_matrix([], [1]) == [], "Неверный результат"
        """,
        """
        def test_matrix(browsers, sizes):
            return [f"{b}@{s}" for b in browsers for s in sizes]
        """),
    cod(f"{P}-m2-l1-e6", t("""
        Напиши функцию `all_chars(words)` — список всех символов всех слов подряд.

        ```
        all_chars(["ab", "c"])   # → ["a", "b", "c"]
        ```
        """),
        """
        def all_chars(words):
            pass
        """,
        """
        def test_values():
            assert all_chars(["ab", "c"]) == ["a", "b", "c"] and all_chars([]) == [], "Неверный результат"
        """,
        """
        def all_chars(words):
            return [ch for w in words for ch in w]
        """),
    cod(f"{P}-m2-l1-e7", t("""
        Напиши функцию `pairs(n)` — все пары `(i, j)` с `1 <= i < j <= n`. Второй `for` может использовать переменную первого.

        ```
        pairs(3)   # → [(1, 2), (1, 3), (2, 3)]
        ```
        """),
        """
        def pairs(n):
            pass
        """,
        """
        def test_values():
            assert pairs(3) == [(1, 2), (1, 3), (2, 3)] and pairs(1) == [], "Неверный результат"
        """,
        """
        def pairs(n):
            return [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `all_tags(tests)` — `tests` это список словарей с полем `"tags"` (список). Вернуть все теги подряд **без повторов** в порядке первого появления.

        ```
        all_tags([{"tags": ["smoke", "api"]}, {"tags": ["api", "ui"]}])   # → ["smoke", "api", "ui"]
        ```
        """),
        """
        def all_tags(tests):
            pass
        """,
        """
        def test_values():
            assert all_tags([{"tags": ["smoke", "api"]}, {"tags": ["api", "ui"]}]) == ["smoke", "api", "ui"] and all_tags([]) == [], "Неверный результат"
        """,
        """
        def all_tags(tests):
            flat = [tag for t in tests for tag in t["tags"]]
            return list(dict.fromkeys(flat))
        """, hint="dict.fromkeys(список) убирает повторы, сохраняя порядок."),
),

lesson(f"{P}-m2-l2", "Матрицы: включение внутри включения",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        print([[i * j for j in range(1, 4)] for i in range(1, 3)])
        """, hint="Внешнее включение создаёт строки, внутреннее — элементы строки."),
    out(f"{P}-m2-l2-e2", "Что выведет программа? Два разных результата.", """
        m = [[1, 2], [3, 4]]
        print([[x * 10 for x in row] for row in m])
        print([x * 10 for row in m for x in row])
        """),
    out(f"{P}-m2-l2-e3", "Что выведет программа? Ловушка умножения списков.", """
        bad = [[0] * 2] * 2
        good = [[0] * 2 for _ in range(2)]
        bad[0][0] = 1
        good[0][0] = 1
        print(bad, good)
        """, hint="[[0]*2]*2 — две ссылки на ОДИН список."),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `zeros(rows, cols)` — матрица `rows × cols` из нулей; строки должны быть **независимыми**.

        ```
        zeros(2, 3)   # → [[0, 0, 0], [0, 0, 0]]
        ```
        """),
        """
        def zeros(rows, cols):
            pass
        """,
        """
        def test_values():
            m = zeros(2, 3)
            assert m == [[0, 0, 0], [0, 0, 0]], f"Получено {m}"
            m[0][0] = 1
            assert m[1][0] == 0, "Строки должны быть независимыми"
        """,
        """
        def zeros(rows, cols):
            return [[0] * cols for _ in range(rows)]
        """),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `table(n)` — таблица умножения `n × n` в виде матрицы чисел.

        ```
        table(3)   # → [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
        ```
        """),
        """
        def table(n):
            pass
        """,
        """
        def test_values():
            assert table(3) == [[1, 2, 3], [2, 4, 6], [3, 6, 9]] and table(1) == [[1]], "Неверная таблица"
        """,
        """
        def table(n):
            return [[i * j for j in range(1, n + 1)] for i in range(1, n + 1)]
        """),
    cod(f"{P}-m2-l2-e6", t("""
        Напиши функцию `transpose(m)` — «повернуть» прямоугольную матрицу: столбцы становятся строками. Вложенное включение.

        ```
        transpose([[1, 2, 3], [4, 5, 6]])   # → [[1, 4], [2, 5], [3, 6]]
        ```
        """),
        """
        def transpose(m):
            pass
        """,
        """
        def test_values():
            assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]] and transpose([[7]]) == [[7]], "Неверный результат"
        """,
        """
        def transpose(m):
            return [[row[c] for row in m] for c in range(len(m[0]))]
        """),
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `scale_matrix(m, k)` — новая матрица, каждый элемент умножен на `k`.

        ```
        scale_matrix([[1, 2], [3, 4]], 10)   # → [[10, 20], [30, 40]]
        ```
        """),
        """
        def scale_matrix(m, k):
            pass
        """,
        """
        def test_values():
            src = [[1, 2], [3, 4]]
            assert scale_matrix(src, 10) == [[10, 20], [30, 40]] and src == [[1, 2], [3, 4]], "Неверный результат или исходная изменена"
        """,
        """
        def scale_matrix(m, k):
            return [[x * k for x in row] for row in m]
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `parse_csv(text)` — строки CSV (разделитель строк `\\n`, значений `,`) превратить в матрицу строк, убрав пробелы по краям значений; пустые строки пропускать.

        ```
        parse_csv("a, b\\n1 ,2\\n")   # → [["a", "b"], ["1", "2"]]
        ```
        """),
        """
        def parse_csv(text):
            pass
        """,
        """
        def test_values():
            assert parse_csv("a, b\\n1 ,2\\n") == [["a", "b"], ["1", "2"]] and parse_csv("") == [], "Неверный результат"
        """,
        """
        def parse_csv(text):
            return [[cell.strip() for cell in line.split(",")] for line in text.split("\\n") if line.strip()]
        """, xp=20),
),

lesson(f"{P}-m2-l3", "Словарные включения",
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        words = ["api", "ui", "docker"]
        print({w: len(w) for w in words})
        print({i: i * i for i in range(4) if i % 2})
        """),
    out(f"{P}-m2-l3-e2", "Что выведет программа?", """
        prices = {"чай": 300, "кофе": 500}
        print({k.upper(): v * 2 for k, v in prices.items()})
        print({v: k for k, v in prices.items()})
        """),
    out(f"{P}-m2-l3-e3", "Что выведет программа? Повторяющиеся ключи.", """
        words = ["apple", "avocado", "banana"]
        print({w[0]: w for w in words})
        """, hint="Для повторного ключа побеждает последнее значение."),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `name_lengths(names)` — словарь «имя → длина».

        ```
        name_lengths(["Аня", "Борис"])   # → {"Аня": 3, "Борис": 5}
        ```
        """),
        """
        def name_lengths(names):
            pass
        """,
        """
        def test_values():
            assert name_lengths(["Аня", "Борис"]) == {"Аня": 3, "Борис": 5} and name_lengths([]) == {}, "Неверный результат"
        """,
        """
        def name_lengths(names):
            return {n: len(n) for n in names}
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `with_discount(prices, percent)` — новый словарь цен со скидкой, округлённых до 2 знаков.

        ```
        with_discount({"чай": 300, "кофе": 99.9}, 10)   # → {"чай": 270.0, "кофе": 89.91}
        ```
        """),
        """
        def with_discount(prices, percent):
            pass
        """,
        """
        def test_values():
            assert with_discount({"чай": 300, "кофе": 99.9}, 10) == {"чай": 270.0, "кофе": 89.91}, "Неверный результат"
        """,
        """
        def with_discount(prices, percent):
            return {k: round(v * (1 - percent / 100), 2) for k, v in prices.items()}
        """),
    cod(f"{P}-m2-l3-e6", t("""
        Напиши функцию `only_failed(results)` — из словаря `{тест: статус}` оставить только пары со статусом `"fail"`.

        ```
        only_failed({"a": "pass", "b": "fail"})   # → {"b": "fail"}
        ```
        """),
        """
        def only_failed(results):
            pass
        """,
        """
        def test_values():
            assert only_failed({"a": "pass", "b": "fail"}) == {"b": "fail"} and only_failed({}) == {}, "Неверный результат"
        """,
        """
        def only_failed(results):
            return {k: v for k, v in results.items() if v == "fail"}
        """),
    cod(f"{P}-m2-l3-e7", t("""
        Напиши функцию `invert(d)` — поменять ключи и значения местами.

        ```
        invert({"a": 1, "b": 2})   # → {1: "a", 2: "b"}
        ```
        """),
        """
        def invert(d):
            pass
        """,
        """
        def test_values():
            assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"} and invert({}) == {}, "Неверный результат"
        """,
        """
        def invert(d):
            return {v: k for k, v in d.items()}
        """),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `from_pairs(lines)` — строки вида `"ключ=значение"` превратить в словарь; строки без `=` пропустить; ключи и значения очистить от пробелов.

        ```
        from_pairs(["host = db", "port=5432", "# comment"])   # → {"host": "db", "port": "5432"}
        ```
        """),
        """
        def from_pairs(lines):
            pass
        """,
        """
        def test_values():
            assert from_pairs(["host = db", "port=5432", "# comment"]) == {"host": "db", "port": "5432"} and from_pairs([]) == {}, "Неверный результат"
        """,
        """
        def from_pairs(lines):
            return {line.split("=", 1)[0].strip(): line.split("=", 1)[1].strip() for line in lines if "=" in line}
        """, hint='line.split("=", 1) делит только по первому знаку =.', xp=20),
),

lesson(f"{P}-m2-l4", "Выражения-генераторы",
    out(f"{P}-m2-l4-e1", "Что выведет программа?", """
        nums = [3, 7, 2]
        print(sum(n * n for n in nums))
        print(max(len(w) for w in ["a", "bbb", "cc"]))
        print(any(n > 5 for n in nums), all(n > 1 for n in nums))
        """, hint="Внутри вызова функции дополнительные скобки не нужны."),
    out(f"{P}-m2-l4-e2", "Что выведет программа? Генератор — не список.", """
        gen = (x * 2 for x in range(3))
        print(type(gen).__name__)
        print(list(gen))
        print(list(gen))
        """, hint="Генератор можно пройти только один раз."),
    out(f"{P}-m2-l4-e3", "Что выведет программа?", """
        words = ["api", "", "ui"]
        print(", ".join(w.upper() for w in words if w))
        print(sum(1 for w in words if not w))
        """),
    cod(f"{P}-m2-l4-e4", t("""
        Напиши функцию `sum_of_squares(nums)` — сумма квадратов через `sum` и выражение-генератор (без создания списка).

        ```
        sum_of_squares([1, 2, 3])   # → 14
        ```
        """),
        """
        def sum_of_squares(nums):
            pass
        """,
        """
        def test_values():
            assert sum_of_squares([1, 2, 3]) == 14 and sum_of_squares([]) == 0, "Неверная сумма"

        def test_generator():
            assert "[" not in open("solution.py", encoding="utf-8").read(), "Без квадратных скобок — выражение-генератор"
        """,
        """
        def sum_of_squares(nums):
            return sum(n * n for n in nums)
        """),
    cod(f"{P}-m2-l4-e5", t("""
        Напиши функцию `has_error(codes)` — есть ли хоть один код `>= 500`. Используй `any`.

        ```
        has_error([200, 503])   # → True
        ```
        """),
        """
        def has_error(codes):
            pass
        """,
        """
        def test_values():
            assert [has_error([200, 503]), has_error([200, 404]), has_error([])] == [True, False, False], "Неверный результат"
        """,
        """
        def has_error(codes):
            return any(c >= 500 for c in codes)
        """),
    cod(f"{P}-m2-l4-e6", t("""
        Напиши функцию `all_valid_emails(emails)` — у всех ли строк есть `@` и точка после него. Используй `all`.

        ```
        all_valid_emails(["a@x.ru", "b@y.io"])   # → True
        all_valid_emails(["a@x", "b@y.io"])      # → False
        ```
        """),
        """
        def all_valid_emails(emails):
            pass
        """,
        """
        def test_values():
            assert [all_valid_emails(["a@x.ru", "b@y.io"]), all_valid_emails(["a@x", "b@y.io"]), all_valid_emails([])] == [True, False, True], "Неверный результат"
        """,
        """
        def all_valid_emails(emails):
            return all("@" in e and "." in e.split("@", 1)[1] for e in emails)
        """),
    cod(f"{P}-m2-l4-e7", t("""
        Напиши функцию `longest_len(words)` — длина самого длинного слова через `max` с выражением-генератором; для пустого списка — `0` (параметр `default` у `max`).

        ```
        longest_len(["a", "bbb"])   # → 3
        longest_len([])             # → 0
        ```
        """),
        """
        def longest_len(words):
            pass
        """,
        """
        def test_values():
            assert [longest_len(["a", "bbb"]), longest_len([])] == [3, 0], "Неверный результат"
        """,
        """
        def longest_len(words):
            return max((len(w) for w in words), default=0)
        """, hint="Если есть ещё аргументы, генератор нужно взять в свои скобки: max((... for ...), default=0)."),
    cod(f"{P}-m2-l4-e8", t("""
        Напиши функцию `csv_line(values)` — значения через запятую, превращённые в строки; `None` заменять пустой строкой. Используй `join` с выражением-генератором.

        ```
        csv_line([1, None, "x"])   # → "1,,x"
        ```
        """),
        """
        def csv_line(values):
            pass
        """,
        """
        def test_values():
            assert csv_line([1, None, "x"]) == "1,,x" and csv_line([]) == "", "Неверный результат"
        """,
        """
        def csv_line(values):
            return ",".join("" if v is None else str(v) for v in values)
        """),
),
)
