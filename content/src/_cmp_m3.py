"""Тема «Списковые включения», модуль 3 «Когда и как использовать» — задания. Теория — в _cmp_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "cmp"

m3 = module(f"{P}-m3", "Когда и как использовать", "🧭", "Множественные включения, ловушки, читаемость и практика",

lesson(f"{P}-m3-l1", "Включения для множеств",
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        words = ["Api", "api", "UI", "ui", "ci"]
        unique = {w.lower() for w in words}
        print(sorted(unique), len(unique))
        """, hint="Множество хранит только уникальные значения."),
    out(f"{P}-m3-l1-e2", "Что выведет программа? Скобки решают.", """
        a = [x % 3 for x in range(6)]
        b = {x % 3 for x in range(6)}
        c = {x: x % 3 for x in range(3)}
        print(a, sorted(b), c)
        """),
    out(f"{P}-m3-l1-e3", "Что выведет программа?", """
        print(type({}).__name__, type({1}).__name__, type({x for x in []}).__name__)
        """, hint="Пустые фигурные скобки — это словарь."),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `unique_domains(emails)` — **отсортированный** список различных доменов (часть после `@`, в нижнем регистре). Используй множественное включение.

        ```
        unique_domains(["a@Mail.ru", "b@mail.ru", "c@x.io"])   # → ["mail.ru", "x.io"]
        ```
        """),
        """
        def unique_domains(emails):
            pass
        """,
        """
        def test_values():
            assert unique_domains(["a@Mail.ru", "b@mail.ru", "c@x.io"]) == ["mail.ru", "x.io"] and unique_domains([]) == [], "Неверный результат"
        """,
        """
        def unique_domains(emails):
            return sorted({e.split("@")[1].lower() for e in emails})
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `count_unique_lengths(words)` — сколько **различных** длин встречается среди слов.

        ```
        count_unique_lengths(["a", "bb", "cc", "ddd"])   # → 3
        ```
        """),
        """
        def count_unique_lengths(words):
            pass
        """,
        """
        def test_values():
            assert [count_unique_lengths(["a", "bb", "cc", "ddd"]), count_unique_lengths([])] == [3, 0], "Неверный результат"
        """,
        """
        def count_unique_lengths(words):
            return len({len(w) for w in words})
        """),
    cod(f"{P}-m3-l1-e6", t("""
        Напиши функцию `common_letters(a, b)` — отсортированная строка из букв, которые есть в обоих словах (без повторов).

        ```
        common_letters("python", "typo")   # → "opty"
        ```
        """),
        """
        def common_letters(a, b):
            pass
        """,
        """
        def test_values():
            assert common_letters("python", "typo") == "opty" and common_letters("abc", "xyz") == "", "Неверный результат"
        """,
        """
        def common_letters(a, b):
            return "".join(sorted({ch for ch in a if ch in b}))
        """),
    cod(f"{P}-m3-l1-e7", t("""
        Напиши функцию `failed_modules(results)` — `results` это список строк `"модуль::тест::статус"`. Вернуть отсортированный список модулей, в которых есть хотя бы один `fail`.

        ```
        failed_modules(["auth::login::pass", "auth::logout::fail", "cart::add::fail"])   # → ["auth", "cart"]
        ```
        """),
        """
        def failed_modules(results):
            pass
        """,
        """
        def test_values():
            got = failed_modules(["auth::login::pass", "auth::logout::fail", "cart::add::fail", "pay::x::pass"])
            assert got == ["auth", "cart"] and failed_modules([]) == [], f"Получено {got}"
        """,
        """
        def failed_modules(results):
            return sorted({r.split("::")[0] for r in results if r.split("::")[2] == "fail"})
        """),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `has_duplicates(items)` — есть ли повторы: сравни длину списка с длиной множества его элементов.

        ```
        has_duplicates([1, 2, 1])   # → True
        ```
        """),
        """
        def has_duplicates(items):
            pass
        """,
        """
        def test_values():
            assert [has_duplicates([1, 2, 1]), has_duplicates([1, 2]), has_duplicates([])] == [True, False, False], "Неверный результат"
        """,
        """
        def has_duplicates(items):
            return len(set(items)) != len(items)
        """),
),

lesson(f"{P}-m3-l2", "Ловушки включений",
    out(f"{P}-m3-l2-e1", "Что выведет программа? Переменная включения не «утекает».", """
        x = "снаружи"
        squares = [x * x for x in range(3)]
        print(squares, x)
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа? Лямбды во включении.", """
        fs = [lambda: i for i in range(3)]
        print([f() for f in fs])
        fixed = [lambda i=i: i for i in range(3)]
        print([f() for f in fixed])
        """, hint="Все лямбды первого списка видят одну i — последнюю."),
    out(f"{P}-m3-l2-e3", "Что выведет программа? Включение ради побочного эффекта.", """
        result = [print(n) for n in [1, 2]]
        print(result)
        """, hint="print возвращает None — получился бесполезный список."),
    cod(f"{P}-m3-l2-e4", t("""
        Функция `print_all` из заготовки использует списковое включение только ради `print` — это плохой стиль (создаётся ненужный список из `None`). Перепиши её обычным циклом `for`.

        Ожидаемый вывод `print_all(["a", "b"])`:
        ```
        a
        b
        ```
        """),
        """
        def print_all(items):
            [print(x) for x in items]

        print_all(["a", "b"])
        """,
        """
        def test_output():
            assert OUTPUT.split() == ["a", "b"], f"Напечатано {OUTPUT!r}"

        def test_loop():
            assert "[print" not in open("solution.py", encoding="utf-8").read(), "Используй обычный цикл для печати"
        """,
        """
        def print_all(items):
            for x in items:
                print(x)

        print_all(["a", "b"])
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Исправь позднее связывание: `make_multipliers(n)` должна вернуть список функций, где функция с индексом `i` умножает аргумент на `i`.

        ```
        [m(10) for m in make_multipliers(3)]   # → [0, 10, 20]
        ```
        """),
        """
        def make_multipliers(n):
            return [lambda x: x * i for i in range(n)]
        """,
        """
        def test_values():
            assert [m(10) for m in make_multipliers(3)] == [0, 10, 20], f"Получено {[m(10) for m in make_multipliers(3)]}"
        """,
        """
        def make_multipliers(n):
            return [lambda x, i=i: x * i for i in range(n)]
        """),
    cod(f"{P}-m3-l2-e6", t("""
        Функция `grid(n)` должна вернуть матрицу `n × n` из независимых строк, но в заготовке строки общие. Исправь через включение.

        ```
        g = grid(2)
        g[0][0] = 1
        g   # → [[1, 0], [0, 0]]
        ```
        """),
        """
        def grid(n):
            return [[0] * n] * n
        """,
        """
        def test_values():
            g = grid(2)
            g[0][0] = 1
            assert g == [[1, 0], [0, 0]], f"Строки общие: {g}"
        """,
        """
        def grid(n):
            return [[0] * n for _ in range(n)]
        """),
    cod(f"{P}-m3-l2-e7", t("""
        Функция `safe_ints(items)` должна превратить в числа только те строки, которые являются целыми числами (со знаком минус допустимо), остальные пропустить. Во включении нельзя поймать исключение — поэтому напиши вспомогательную функцию `is_int(s)` с `try/except` и используй её в условии.

        ```
        safe_ints(["1", "x", "-3", "2.5"])   # → [1, -3]
        ```
        """),
        """
        def safe_ints(items):
            pass
        """,
        """
        def test_values():
            assert safe_ints(["1", "x", "-3", "2.5"]) == [1, -3] and safe_ints([]) == [], "Неверный результат"
        """,
        """
        def is_int(s):
            try:
                int(s)
                return True
            except ValueError:
                return False

        def safe_ints(items):
            return [int(s) for s in items if is_int(s)]
        """, xp=20),
    cod(f"{P}-m3-l2-e8", t("""
        Не меняй список, по которому идёт перебор. Функция `without(items, value)` должна вернуть **новый** список без всех вхождений `value`, исходный — не менять.

        ```
        src = [1, 2, 2, 3]
        without(src, 2)   # → [1, 3]
        src               # → [1, 2, 2, 3]
        ```
        """),
        """
        def without(items, value):
            pass
        """,
        """
        def test_values():
            src = [1, 2, 2, 3]
            assert without(src, 2) == [1, 3] and src == [1, 2, 2, 3], "Неверный результат или исходный изменён"
        """,
        """
        def without(items, value):
            return [x for x in items if x != value]
        """),
),

lesson(f"{P}-m3-l3", "Включение или цикл: читаемость",
    out(f"{P}-m3-l3-e1", "Что выведет программа? Одно и то же двумя способами.", """
        data = [" a ", "", "B", " c"]
        clean = []
        for s in data:
            s = s.strip()
            if s:
                clean.append(s.lower())
        print(clean)
        print([s.strip().lower() for s in data if s.strip()])
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа? Слишком сложное включение.", """
        m = [[1, -2], [3, 4], [-5, 6]]
        print([x * 2 for row in m if sum(row) > 0 for x in row if x > 0])
        """, hint="Читай for и if слева направо как вложенные циклы и условия."),
    out(f"{P}-m3-l3-e3", "Что выведет программа?", """
        def normalize(s):
            return s.strip().lower()

        raw = [" Anna ", "BOB"]
        print([normalize(s) for s in raw])
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Перепиши сложное включение из заготовки обычными циклами с понятными именами — результат должен остаться тем же. (Проверка запрещает квадратные скобки с `for` внутри.)
        """),
        """
        def positive_doubled(m):
            return [x * 2 for row in m if sum(row) > 0 for x in row if x > 0]
        """,
        """
        import re

        def test_values():
            assert positive_doubled([[1, -2], [3, 4], [-5, 6]]) == [6, 8, 12] and positive_doubled([]) == [], "Результат изменился"

        def test_loops():
            src = open("solution.py", encoding="utf-8").read()
            assert not re.search(r"\\[[^\\]]* for ", src), "Перепиши через обычные циклы"
        """,
        """
        def positive_doubled(m):
            result = []
            for row in m:
                if sum(row) <= 0:
                    continue
                for x in row:
                    if x > 0:
                        result.append(x * 2)
            return result
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Вынеси обработку одного элемента в функцию: напиши `slugify(title)` — нижний регистр, пробелы по краям убрать, внутренние пробелы заменить на `-`, — и `slugify_all(titles)`, которая применяет её включением.

        ```
        slugify_all([" Hello World ", "API Tests"])   # → ["hello-world", "api-tests"]
        ```
        """),
        """
        def slugify(title):
            pass

        def slugify_all(titles):
            pass
        """,
        """
        def test_values():
            assert slugify(" Hello World ") == "hello-world", "Неверный slugify"
            assert slugify_all([" Hello World ", "API Tests"]) == ["hello-world", "api-tests"], "Неверный slugify_all"
        """,
        """
        def slugify(title):
            return "-".join(title.strip().lower().split())

        def slugify_all(titles):
            return [slugify(t) for t in titles]
        """),
    cod(f"{P}-m3-l3-e6", t("""
        Напиши функцию `first_negative(nums)` — первое отрицательное число или `None`. Тут включение **не нужно**: оно перебрало бы весь список. Используй цикл с `return` или `next(...)` с генератором.

        ```
        first_negative([3, -1, -5])   # → -1
        ```
        """),
        """
        def first_negative(nums):
            pass
        """,
        """
        def test_values():
            assert [first_negative([3, -1, -5]), first_negative([1, 2]), first_negative([])] == [-1, None, None], "Неверный результат"
        """,
        """
        def first_negative(nums):
            return next((n for n in nums if n < 0), None)
        """),
    cod(f"{P}-m3-l3-e7", t("""
        Напиши функцию `stats(nums)` — словарь `{"pos": [...], "neg": [...], "zero": N}`. Три коротких включения читаются лучше одного сложного цикла.

        ```
        stats([1, -2, 0, 3, 0])   # → {"pos": [1, 3], "neg": [-2], "zero": 2}
        ```
        """),
        """
        def stats(nums):
            pass
        """,
        """
        def test_values():
            assert stats([1, -2, 0, 3, 0]) == {"pos": [1, 3], "neg": [-2], "zero": 2} and stats([]) == {"pos": [], "neg": [], "zero": 0}, "Неверный результат"
        """,
        """
        def stats(nums):
            return {
                "pos": [n for n in nums if n > 0],
                "neg": [n for n in nums if n < 0],
                "zero": sum(1 for n in nums if n == 0),
            }
        """),
    cod(f"{P}-m3-l3-e8", t("""
        Напиши функцию `running_total(nums)` — нарастающие суммы. Включение здесь неудобно (нужно состояние между шагами) — используй обычный цикл.

        ```
        running_total([1, 2, 3])   # → [1, 3, 6]
        ```
        """),
        """
        def running_total(nums):
            pass
        """,
        """
        def test_values():
            assert running_total([1, 2, 3]) == [1, 3, 6] and running_total([]) == [], "Неверный результат"
        """,
        """
        def running_total(nums):
            result = []
            total = 0
            for n in nums:
                total += n
                result.append(total)
            return result
        """),
),

lesson(f"{P}-m3-l4", "Практика: обработка результатов тестов",
    out(f"{P}-m3-l4-e1", "Что выведет программа?", """
        results = [{"name": "login", "status": "pass", "time": 1.2},
                   {"name": "pay", "status": "fail", "time": 3.4},
                   {"name": "cart", "status": "pass", "time": 0.5}]
        print([r["name"] for r in results if r["status"] == "fail"])
        print(round(sum(r["time"] for r in results), 1))
        print({r["name"]: r["time"] for r in results if r["time"] > 1})
        """),
    out(f"{P}-m3-l4-e2", "Что выведет программа?", """
        log = ["INFO start", "ERROR db", "WARN slow", "ERROR api"]
        levels = {line.split()[0] for line in log}
        print(sorted(levels))
        print([line.split(" ", 1)[1] for line in log if line.startswith("ERROR")])
        """),
    out(f"{P}-m3-l4-e3", "Что выведет программа?", """
        suites = {"auth": ["pass", "fail"], "cart": ["pass", "pass"]}
        print({name: all(s == "pass" for s in runs) for name, runs in suites.items()})
        """),
    cod(f"{P}-m3-l4-e4", t("""
        Напиши функцию `slow_tests(results, limit)` — имена тестов (словари `name`, `time`), которые шли дольше `limit` секунд, отсортированные по убыванию времени.

        ```
        slow_tests([{"name": "a", "time": 1.2}, {"name": "b", "time": 3.4}, {"name": "c", "time": 2.0}], 1.5)   # → ["b", "c"]
        ```
        """),
        """
        def slow_tests(results, limit):
            pass
        """,
        """
        def test_values():
            res = [{"name": "a", "time": 1.2}, {"name": "b", "time": 3.4}, {"name": "c", "time": 2.0}]
            assert slow_tests(res, 1.5) == ["b", "c"] and slow_tests(res, 10) == [], "Неверный результат"
        """,
        """
        def slow_tests(results, limit):
            slow = [r for r in results if r["time"] > limit]
            return [r["name"] for r in sorted(slow, key=lambda r: r["time"], reverse=True)]
        """),
    cod(f"{P}-m3-l4-e5", t("""
        Напиши функцию `error_messages(log)` — тексты сообщений уровня `ERROR` из строк `"LEVEL текст"`.

        ```
        error_messages(["INFO ok", "ERROR db down"])   # → ["db down"]
        ```
        """),
        """
        def error_messages(log):
            pass
        """,
        """
        def test_values():
            assert error_messages(["INFO ok", "ERROR db down", "ERROR x"]) == ["db down", "x"] and error_messages([]) == [], "Неверный результат"
        """,
        """
        def error_messages(log):
            return [line.split(" ", 1)[1] for line in log if line.startswith("ERROR ")]
        """),
    cod(f"{P}-m3-l4-e6", t("""
        Напиши функцию `suite_status(suites)` — `suites` это словарь «набор → список статусов». Вернуть словарь «набор → `"green"`, если все `pass`, иначе `"red"`».

        ```
        suite_status({"auth": ["pass", "fail"], "cart": ["pass"]})   # → {"auth": "red", "cart": "green"}
        ```
        """),
        """
        def suite_status(suites):
            pass
        """,
        """
        def test_values():
            assert suite_status({"auth": ["pass", "fail"], "cart": ["pass"]}) == {"auth": "red", "cart": "green"} and suite_status({}) == {}, "Неверный результат"
        """,
        """
        def suite_status(suites):
            return {name: "green" if all(s == "pass" for s in runs) else "red" for name, runs in suites.items()}
        """),
    cod(f"{P}-m3-l4-e7", t("""
        Напиши функцию `by_status(results)` — словарь «статус → список имён» для списка пар `(имя, статус)`. Ключи — различные статусы (множественное включение), значения — списковые включения.

        ```
        by_status([("a", "pass"), ("b", "fail"), ("c", "pass")])   # → {"pass": ["a", "c"], "fail": ["b"]}
        ```
        """),
        """
        def by_status(results):
            pass
        """,
        """
        def test_values():
            assert by_status([("a", "pass"), ("b", "fail"), ("c", "pass")]) == {"pass": ["a", "c"], "fail": ["b"]} and by_status([]) == {}, "Неверный результат"
        """,
        """
        def by_status(results):
            statuses = {s for _, s in results}
            return {st: [n for n, s in results if s == st] for st in statuses}
        """, xp=20),
    cod(f"{P}-m3-l4-e8", t("""
        Напиши функцию `report_lines(results)` — строки отчёта `"✅ имя (время с)"` или `"❌ имя (время с)"` для списка словарей `name`, `status`, `time`.

        ```
        report_lines([{"name": "a", "status": "pass", "time": 1.2}])   # → ["✅ a (1.2 с)"]
        ```
        """),
        """
        def report_lines(results):
            pass
        """,
        """
        def test_values():
            got = report_lines([{"name": "a", "status": "pass", "time": 1.2}, {"name": "b", "status": "fail", "time": 3}])
            assert got == ["✅ a (1.2 с)", "❌ b (3 с)"], f"Получено {got}"
        """,
        """
        def report_lines(results):
            return [f"{'✅' if r['status'] == 'pass' else '❌'} {r['name']} ({r['time']} с)" for r in results]
        """),
),
)
