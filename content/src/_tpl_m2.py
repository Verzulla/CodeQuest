"""Тема «Кортежи», модуль 2 «Кортежи в деле» — задания. Теория — в _tpl_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "tpl"

m2 = module(f"{P}-m2", "Кортежи в деле", "🧷", "Кортеж или список, преобразования, ключи словаря, сортировка",

lesson(f"{P}-m2-l1", "Кортеж или список?",
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        import sys
        as_list = [1, 2, 3]
        as_tuple = (1, 2, 3)
        print(sys.getsizeof(as_list) > sys.getsizeof(as_tuple))
        print(hasattr(as_list, "append"), hasattr(as_tuple, "append"))
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа?", """
        users = [("Аня", 25), ("Боря", 30)]
        users.append(("Вика", 22))
        for name, age in users:
            print(name, age)
        """, hint="Типичная связка: список (меняется) из кортежей (фиксированные записи)."),
    out(f"{P}-m2-l1-e6", "Что выведет программа? Временно превратить в список.", """
        t = (1, 2, 3)
        lst = list(t)
        lst.append(4)
        t2 = tuple(lst)
        print(t, lst, t2)
        """),
    cod(f"{P}-m2-l1-e3", t("""
        Напиши функцию `to_records(names, ages)` — из двух списков сделай **список кортежей** `(имя, возраст)`.

        ```
        to_records(["Аня", "Боря"], [25, 30])   # → [("Аня", 25), ("Боря", 30)]
        ```
        """),
        """
        def to_records(names, ages):
            pass
        """,
        """
        def test_values():
            got = to_records(["Аня", "Боря"], [25, 30])
            assert got == [("Аня", 25), ("Боря", 30)] and isinstance(got, list) and all(isinstance(r, tuple) for r in got), f"Получено {got}"
        """,
        """
        def to_records(names, ages):
            return list(zip(names, ages))
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `oldest(records)` — из списка кортежей `(имя, возраст)` вернуть **имя** самого старшего. Для пустого списка — `None`.

        ```
        oldest([("Аня", 25), ("Боря", 30), ("Вика", 22)])   # → "Боря"
        ```
        """),
        """
        def oldest(records):
            pass
        """,
        """
        def test_values():
            assert oldest([("Аня", 25), ("Боря", 30), ("Вика", 22)]) == "Боря" and oldest([]) is None, "Неверный результат"
        """,
        """
        def oldest(records):
            if not records:
                return None
            name, _ = max(records, key=lambda r: r[1])
            return name
        """),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `constants()` — вернуть **кортеж** допустимых HTTP-методов `("GET", "POST", "PUT", "PATCH", "DELETE")`, а функцию `is_allowed(method)` — проверить, есть ли метод (в любом регистре) в этом кортеже.

        Кортеж выбран намеренно: набор методов не должен меняться во время работы программы.

        ```
        is_allowed("get")    # → True
        is_allowed("TRACE")  # → False
        ```
        """),
        """
        def constants():
            pass

        def is_allowed(method):
            pass
        """,
        """
        def test_constants():
            c = constants()
            assert isinstance(c, tuple) and c == ("GET", "POST", "PUT", "PATCH", "DELETE"), f"Получено {c!r}"

        def test_allowed():
            assert is_allowed("get") and is_allowed("Delete") and not is_allowed("TRACE"), "Неверная проверка"
        """,
        """
        def constants():
            return ("GET", "POST", "PUT", "PATCH", "DELETE")

        def is_allowed(method):
            return method.upper() in constants()
        """),
    cod(f"{P}-m2-l1-e7", t("""
        Напиши функцию `to_tuple_rows(rows)` — превратить список списков в список **кортежей** (строки таблицы «заморожены»).

        ```
        to_tuple_rows([[1, "a"], [2, "b"]])   # → [(1, "a"), (2, "b")]
        ```
        """),
        """
        def to_tuple_rows(rows):
            pass
        """,
        """
        def test_values():
            got = to_tuple_rows([[1, "a"], [2, "b"]])
            assert got == [(1, "a"), (2, "b")] and all(isinstance(r, tuple) for r in got) and to_tuple_rows([]) == [], f"Получено {got}"
        """,
        """
        def to_tuple_rows(rows):
            return [tuple(r) for r in rows]
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Объяви константу-кортеж `DAYS = ("пн", "вт", "ср", "чт", "пт", "сб", "вс")` и функцию `weekday_name(n)` — название дня по номеру от 0 до 6; для других номеров — `None`.

        ```
        weekday_name(0)   # → "пн"
        weekday_name(6)   # → "вс"
        weekday_name(7)   # → None
        ```
        """),
        """
        def weekday_name(n):
            pass
        """,
        """
        def test_values():
            assert [weekday_name(0), weekday_name(6), weekday_name(7), weekday_name(-1)] == ["пн", "вс", None, None], "Неверный день"

        def test_const():
            assert isinstance(DAYS, tuple) and len(DAYS) == 7, "DAYS — кортеж из 7 дней"
        """,
        """
        DAYS = ("пн", "вт", "ср", "чт", "пт", "сб", "вс")

        def weekday_name(n):
            if 0 <= n < len(DAYS):
                return DAYS[n]
            return None
        """, hint="Отрицательный индекс в Python допустим, поэтому -1 нужно отсечь проверкой."),
),

lesson(f"{P}-convert", "Кортежи и другие коллекции",
    out(f"{P}-convert-e1", "Что выведет программа?", """
        t = tuple("hello")
        print(t)
        print("".join(t), list(t)[:2], set(t) == {"h", "e", "l", "o"})
        """),
    out(f"{P}-convert-e2", "Что выведет программа? sorted возвращает список.", """
        t = (3, 1, 2)
        s = sorted(t)
        print(s, type(s).__name__, tuple(s))
        print(tuple(reversed(t)))
        """),
    out(f"{P}-convert-e3", "Что выведет программа? Кортежи и словари.", """
        d = {"a": 1, "b": 2}
        print(tuple(d), tuple(d.items()))
        print(dict([("x", 1), ("y", 2)]))
        """),
    cod(f"{P}-convert-e4", t("""
        Напиши функцию `sorted_tuple(t)` — отсортированная версия кортежа, **тоже кортеж** (`sorted` возвращает список!).

        ```
        sorted_tuple((3, 1, 2))   # → (1, 2, 3)
        ```
        """),
        """
        def sorted_tuple(t):
            pass
        """,
        """
        def test_values():
            got = sorted_tuple((3, 1, 2))
            assert got == (1, 2, 3) and isinstance(got, tuple) and sorted_tuple(()) == (), f"Получено {got!r}"
        """,
        """
        def sorted_tuple(t):
            return tuple(sorted(t))
        """),
    cod(f"{P}-convert-e5", t("""
        Напиши функцию `unique_tuple(t)` — кортеж без повторов, **в порядке первого появления**. (`set` порядок не сохраняет.)

        ```
        unique_tuple((3, 1, 3, 2, 1))   # → (3, 1, 2)
        ```
        """),
        """
        def unique_tuple(t):
            pass
        """,
        """
        def test_values():
            assert unique_tuple((3, 1, 3, 2, 1)) == (3, 1, 2) and unique_tuple(()) == () and unique_tuple(("a", "a")) == ("a",), "Неверный результат"
        """,
        """
        def unique_tuple(t):
            result = []
            for x in t:
                if x not in result:
                    result.append(x)
            return tuple(result)
        """),
    cod(f"{P}-convert-e6", t("""
        Напиши функцию `dict_to_pairs(d)` — кортеж пар `(ключ, значение)`, отсортированный по ключу.

        ```
        dict_to_pairs({"b": 2, "a": 1})   # → (("a", 1), ("b", 2))
        ```
        """),
        """
        def dict_to_pairs(d):
            pass
        """,
        """
        def test_values():
            assert dict_to_pairs({"b": 2, "a": 1}) == (("a", 1), ("b", 2)) and dict_to_pairs({}) == (), "Неверный результат"
        """,
        """
        def dict_to_pairs(d):
            return tuple(sorted(d.items()))
        """),
    cod(f"{P}-convert-e7", t("""
        Напиши функцию `word_tuple(text)` — кортеж слов строки в нижнем регистре.

        ```
        word_tuple("Hello big World")   # → ("hello", "big", "world")
        ```
        """),
        """
        def word_tuple(text):
            pass
        """,
        """
        def test_values():
            assert word_tuple("Hello big World") == ("hello", "big", "world") and word_tuple("") == (), "Неверный результат"
        """,
        """
        def word_tuple(text):
            return tuple(text.lower().split())
        """),
    cod(f"{P}-convert-e8", t("""
        Напиши функцию `pairs_to_dict(pairs)` — словарь из последовательности пар `(ключ, значение)`. Если ключ повторяется, побеждает **последнее** значение.

        ```
        pairs_to_dict([("a", 1), ("b", 2), ("a", 3)])   # → {"a": 3, "b": 2}
        ```
        """),
        """
        def pairs_to_dict(pairs):
            pass
        """,
        """
        def test_values():
            assert pairs_to_dict([("a", 1), ("b", 2), ("a", 3)]) == {"a": 3, "b": 2} and pairs_to_dict(()) == {}, "Неверный словарь"
        """,
        """
        def pairs_to_dict(pairs):
            return dict(pairs)
        """, hint="dict(...) умеет строить словарь из пар."),
),

lesson(f"{P}-m2-l2", "Кортежи как ключи словаря",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        grid = {(0, 0): "старт", (2, 3): "клад"}
        print(grid[(2, 3)])
        print((1, 1) in grid)
        try:
            d = {[1, 2]: "x"}
        except TypeError as e:
            print("список нельзя:", "unhashable" in str(e))
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа?", """
        results = {}
        for browser in ["chrome", "firefox"]:
            for size in [1920, 375]:
                results[(browser, size)] = "pass"
        results[("firefox", 375)] = "fail"
        print(len(results), results[("firefox", 375)])
        """),
    out(f"{P}-m2-l2-e6", "Что выведет программа?", """
        seats = {}
        seats[(1, "A")] = "Аня"
        seats[1, "B"] = "Боря"
        print(seats)
        print(seats.get((2, "A"), "свободно"))
        """, hint='seats[1, "B"] — то же, что seats[(1, "B")]: кортеж создаёт запятая.'),
    cod(f"{P}-m2-l2-e3", t("""
        Напиши функцию `matrix_results(runs)` — из списка троек `(браузер, размер, статус)` построй словарь с ключами-кортежами `(браузер, размер)` и значениями-статусами.

        ```
        matrix_results([("chrome", 1920, "pass"), ("firefox", 375, "fail")])
        # → {("chrome", 1920): "pass", ("firefox", 375): "fail"}
        ```
        """),
        """
        def matrix_results(runs):
            pass
        """,
        """
        def test_values():
            got = matrix_results([("chrome", 1920, "pass"), ("firefox", 375, "fail")])
            assert got == {("chrome", 1920): "pass", ("firefox", 375): "fail"}, f"Получено {got}"
        """,
        """
        def matrix_results(runs):
            return {(browser, size): status for browser, size, status in runs}
        """),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `count_pairs(events)` — посчитать, сколько раз встречается каждая пара `(пользователь, действие)`. `events` — список кортежей.

        ```
        count_pairs([("anna", "login"), ("bob", "login"), ("anna", "login"), ("anna", "pay")])
        # → {("anna", "login"): 2, ("bob", "login"): 1, ("anna", "pay"): 1}
        ```
        """),
        """
        def count_pairs(events):
            pass
        """,
        """
        def test_values():
            got = count_pairs([("anna", "login"), ("bob", "login"), ("anna", "login"), ("anna", "pay")])
            assert got == {("anna", "login"): 2, ("bob", "login"): 1, ("anna", "pay"): 1}, f"Получено {got}"
        """,
        """
        def count_pairs(events):
            counts = {}
            for pair in events:
                counts[pair] = counts.get(pair, 0) + 1
            return counts
        """),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `unique_points(points)` — убрать повторяющиеся точки из списка **списков** `[x, y]`, сохранив порядок первого появления. Результат — список **кортежей**.

        Подсказка: список нельзя положить в множество, а кортеж — можно.

        ```
        unique_points([[1, 2], [3, 4], [1, 2], [5, 6]])   # → [(1, 2), (3, 4), (5, 6)]
        ```
        """),
        """
        def unique_points(points):
            pass
        """,
        """
        def test_values():
            assert unique_points([[1, 2], [3, 4], [1, 2], [5, 6]]) == [(1, 2), (3, 4), (5, 6)] and unique_points([]) == [], "Неверный результат"
        """,
        """
        def unique_points(points):
            seen = set()
            result = []
            for p in points:
                key = tuple(p)
                if key not in seen:
                    seen.add(key)
                    result.append(key)
            return result
        """, xp=20),
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `neighbors(cell)` — список четырёх соседних клеток для клетки-кортежа `(row, col)`: сверху, снизу, слева, справа — именно в этом порядке.

        ```
        neighbors((1, 1))   # → [(0, 1), (2, 1), (1, 0), (1, 2)]
        ```
        """),
        """
        def neighbors(cell):
            pass
        """,
        """
        def test_values():
            assert neighbors((1, 1)) == [(0, 1), (2, 1), (1, 0), (1, 2)] and neighbors((0, 0)) == [(-1, 0), (1, 0), (0, -1), (0, 1)], "Неверные соседи"
        """,
        """
        def neighbors(cell):
            r, c = cell
            return [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `render(cells, rows, cols)` — `cells` это словарь `{(row, col): символ}`. Верни список строк поля размером `rows × cols`, где пустые клетки — точки.

        ```
        render({(0, 1): "#", (1, 0): "@"}, 2, 3)   # → [".#.", "@.."]
        ```
        """),
        """
        def render(cells, rows, cols):
            pass
        """,
        """
        def test_values():
            assert render({(0, 1): "#", (1, 0): "@"}, 2, 3) == [".#.", "@.."] and render({}, 1, 2) == [".."], "Неверное поле"
        """,
        """
        def render(cells, rows, cols):
            lines = []
            for r in range(rows):
                line = ""
                for c in range(cols):
                    line += cells.get((r, c), ".")
                lines.append(line)
            return lines
        """, xp=20),
),

lesson(f"{P}-m2-l3", "Сравнение и сортировка кортежей",
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        print((1, 9) < (1, 10), (2, 0) > (1, 99), (1, 2) == (1, 2))
        print((1, 2) < (1, 2, 0))
        print(sorted([(2, "b"), (1, "z"), (2, "a")]))
        """, hint="Более короткий кортеж меньше, если он — начало длинного."),
    out(f"{P}-m2-l3-e2", "Что выведет программа?", """
        versions = ["1.10.0", "1.9.2", "1.2.10"]
        print(sorted(versions))
        print(sorted(versions, key=lambda v: tuple(int(p) for p in v.split("."))))
        """),
    out(f"{P}-m2-l3-e6", "Что выведет программа?", """
        people = [("Боря", 30), ("Аня", 30), ("Вика", 25)]
        print(sorted(people))
        print(sorted(people, key=lambda p: p[1]))
        print(max(people, key=lambda p: p[1]))
        """, hint="Сортировка устойчивая: при равном ключе сохраняется исходный порядок."),
    cod(f"{P}-m2-l3-e3", t("""
        Напиши функцию `sort_versions(versions)` — отсортировать строки версий `"X.Y.Z"` **по смыслу** (как числа), по возрастанию. Используй ключ-кортеж.

        ```
        sort_versions(["1.10.0", "1.9.2", "2.0.0", "1.2.10"])
        # → ["1.2.10", "1.9.2", "1.10.0", "2.0.0"]
        ```
        """),
        """
        def sort_versions(versions):
            pass
        """,
        """
        def test_values():
            got = sort_versions(["1.10.0", "1.9.2", "2.0.0", "1.2.10"])
            assert got == ["1.2.10", "1.9.2", "1.10.0", "2.0.0"], f"Получено {got}"
        """,
        """
        def sort_versions(versions):
            return sorted(versions, key=lambda v: tuple(int(p) for p in v.split(".")))
        """),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `leaderboard(scores)` — `scores` это список пар `(имя, очки)`. Отсортируй: по очкам **по убыванию**, при равенстве — по имени **по возрастанию**. Вернуть список имён.

        ```
        leaderboard([("Боря", 50), ("Аня", 80), ("Вика", 50)])   # → ["Аня", "Боря", "Вика"]
        ```
        """),
        """
        def leaderboard(scores):
            pass
        """,
        """
        def test_values():
            assert leaderboard([("Боря", 50), ("Аня", 80), ("Вика", 50)]) == ["Аня", "Боря", "Вика"], f"Получено {leaderboard([('Боря', 50), ('Аня', 80), ('Вика', 50)])}"
        """,
        """
        def leaderboard(scores):
            return [name for name, _ in sorted(scores, key=lambda s: (-s[1], s[0]))]
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `sort_bugs(bugs)` — отсортировать баги (кортежи `(id, severity, created)`) так:

        1. по серьёзности в порядке `critical`, `major`, `minor` (используй словарь рангов);
        2. при равной серьёзности — по дате `created` (строка `"YYYY-MM-DD"`) от старых к новым.

        Вернуть список `id`.

        ```
        bugs = [(1, "minor", "2024-01-01"), (2, "critical", "2024-03-01"),
                (3, "major", "2024-02-01"), (4, "critical", "2024-01-15")]
        sort_bugs(bugs)   # → [4, 2, 3, 1]
        ```
        """),
        """
        def sort_bugs(bugs):
            pass
        """,
        """
        def test_values():
            bugs = [(1, "minor", "2024-01-01"), (2, "critical", "2024-03-01"), (3, "major", "2024-02-01"), (4, "critical", "2024-01-15")]
            assert sort_bugs(bugs) == [4, 2, 3, 1], f"Получено {sort_bugs(bugs)}"
        """,
        """
        RANK = {"critical": 0, "major": 1, "minor": 2}

        def sort_bugs(bugs):
            ordered = sorted(bugs, key=lambda b: (RANK[b[1]], b[2]))
            return [bug_id for bug_id, _, _ in ordered]
        """, xp=20),
    cod(f"{P}-m2-l3-e7", t("""
        Напиши функцию `compare_versions(a, b)` — сравнить две версии-кортежа: `-1`, если `a` меньше, `1`, если больше, `0`, если равны. Используй сравнение кортежей.

        ```
        compare_versions((1, 2, 0), (1, 10, 0))   # → -1
        compare_versions((2, 0), (1, 99))         # → 1
        ```
        """),
        """
        def compare_versions(a, b):
            pass
        """,
        """
        def test_values():
            got = [compare_versions((1, 2, 0), (1, 10, 0)), compare_versions((2, 0), (1, 99)), compare_versions((1, 0), (1, 0))]
            assert got == [-1, 1, 0], f"Получено {got}"
        """,
        """
        def compare_versions(a, b):
            if a < b:
                return -1
            if a > b:
                return 1
            return 0
        """),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `sort_by_date(events)` — события заданы как `(название, (год, месяц, день))`. Верни названия в хронологическом порядке.

        ```
        sort_by_date([("релиз", (2024, 5, 1)), ("старт", (2024, 1, 15)), ("демо", (2024, 1, 3))])
        # → ["демо", "старт", "релиз"]
        ```
        """),
        """
        def sort_by_date(events):
            pass
        """,
        """
        def test_values():
            got = sort_by_date([("релиз", (2024, 5, 1)), ("старт", (2024, 1, 15)), ("демо", (2024, 1, 3))])
            assert got == ["демо", "старт", "релиз"], f"Получено {got}"
        """,
        """
        def sort_by_date(events):
            ordered = sorted(events, key=lambda e: e[1])
            return [title for title, _ in ordered]
        """, hint="Даты-кортежи (год, месяц, день) сравниваются правильно сами по себе."),
),
)
