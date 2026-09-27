"""Тема «Кортежи»."""
from ._lib import cod, lesson, module, out, t, topic

P = "tpl"

# ============================================================
m1 = module(f"{P}-m1", "Основы кортежей", "📎", "Создание, доступ и распаковка",

lesson(f"{P}-m1-l1", "Создание и неизменяемость", 
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        a = (42)
        b = (42,)
        c = 1, 2, 3
        print(type(a).__name__, type(b).__name__, type(c).__name__)
        print(len(c), tuple("abc"))
        """, hint="Кортеж создаёт запятая, а не скобки."),
    out(f"{P}-m1-l1-e2", "Что выведет программа?", """
        point = (3, 4)
        try:
            point[0] = 10
        except TypeError:
            print("кортеж нельзя изменить")
        point = (10, point[1])
        print(point)
        """),
    cod(f"{P}-m1-l1-e3", t("""
        Создай переменные:
        - `origin` — кортеж из двух нулей `(0, 0)`;
        - `single` — кортеж из **одного** элемента `"only"`;
        - `letters` — кортеж из символов строки `"xyz"` (через `tuple()`).
        """),
        "",
        """
        def test_values():
            assert origin == (0, 0) and isinstance(origin, tuple), "origin — (0, 0)"
            assert single == ("only",) and isinstance(single, tuple), "single — кортеж из одного элемента: не забудь запятую"
            assert letters == ("x", "y", "z"), "letters — ('x', 'y', 'z')"
        """,
        """
        origin = (0, 0)
        single = ("only",)
        letters = tuple("xyz")
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `move(point, dx, dy)` — вернуть **новый** кортеж-точку, сдвинутую на `dx` по X и `dy` по Y. Исходный кортеж неизменяемый, поэтому нужно создать новый.

        ```
        move((3, 4), 1, -2)   # → (4, 2)
        ```
        """),
        """
        def move(point, dx, dy):
            pass
        """,
        """
        def test_values():
            assert move((3, 4), 1, -2) == (4, 2) and move((0, 0), 0, 0) == (0, 0), "Неверная точка"
            assert isinstance(move((1, 1), 1, 1), tuple), "Верни кортеж"
        """,
        """
        def move(point, dx, dy):
            x, y = point
            return (x + dx, y + dy)
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `freeze(items)` — превратить список в кортеж, чтобы его нельзя было случайно изменить. Функция должна возвращать кортеж, а изменения исходного списка **после** вызова не должны влиять на результат.

        ```
        data = [1, 2]
        frozen = freeze(data)
        data.append(3)
        frozen   # → (1, 2)
        ```
        """),
        """
        def freeze(items):
            return items
        """,
        """
        def test_freeze():
            data = [1, 2]
            frozen = freeze(data)
            data.append(3)
            assert frozen == (1, 2) and isinstance(frozen, tuple), f"Получено {frozen!r}"
        """,
        """
        def freeze(items):
            return tuple(items)
        """)),

lesson(f"{P}-m1-l2", "Доступ, срезы, count и index", 
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        t = (10, 20, 30, 20)
        print(t[1], t[-1], t[1:3])
        print(t.count(20), t.index(30), 40 in t)
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа?", """
        a = (1, 2)
        b = a + (3,)
        c = a * 2
        print(a, b, c)
        print(a is b)
        """),
    cod(f"{P}-m1-l2-e3", t("""
        Напиши функцию `rgb_to_hex(color)` — перевести кортеж `(r, g, b)` (числа 0–255) в строку `"#rrggbb"` в нижнем регистре.

        ```
        rgb_to_hex((255, 0, 128))   # → "#ff0080"
        rgb_to_hex((0, 0, 0))       # → "#000000"
        ```
        Формат одного числа: `f"{n:02x}"`.
        """),
        """
        def rgb_to_hex(color):
            pass
        """,
        """
        def test_values():
            assert rgb_to_hex((255, 0, 128)) == "#ff0080" and rgb_to_hex((0, 0, 0)) == "#000000" and rgb_to_hex((16, 32, 48)) == "#102030", "Неверный цвет"
        """,
        """
        def rgb_to_hex(color):
            r, g, b = color
            return f"#{r:02x}{g:02x}{b:02x}"
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `most_common(t)` — элемент кортежа, который встречается **чаще всего** (при равенстве — тот, что раньше встречается в кортеже). Используй `count`.

        ```
        most_common(("pass", "fail", "pass", "skip"))   # → "pass"
        most_common((1, 2, 2, 1))                       # → 1
        ```
        """),
        """
        def most_common(t):
            pass
        """,
        """
        def test_values():
            assert most_common(("pass", "fail", "pass", "skip")) == "pass" and most_common((1, 2, 2, 1)) == 1 and most_common(("x",)) == "x", "Неверный результат"
        """,
        """
        def most_common(t):
            return max(t, key=t.count)
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `version_str(version)` — кортеж версии в строку через точку, а функцию `bump_minor(version)` — вернуть **новый** кортеж с увеличенной второй частью и обнулённой третьей.

        ```
        version_str((1, 10, 3))   # → "1.10.3"
        bump_minor((1, 10, 3))    # → (1, 11, 0)
        ```
        """),
        """
        def version_str(version):
            pass

        def bump_minor(version):
            pass
        """,
        """
        def test_str():
            assert version_str((1, 10, 3)) == "1.10.3" and version_str((2, 0, 0)) == "2.0.0", "Неверная строка"

        def test_bump():
            assert bump_minor((1, 10, 3)) == (1, 11, 0) and bump_minor((0, 0, 9)) == (0, 1, 0), "Неверная версия"
        """,
        """
        def version_str(version):
            return ".".join(str(p) for p in version)

        def bump_minor(version):
            major, minor, _ = version
            return (major, minor + 1, 0)
        """)),

lesson(f"{P}-m1-l3", "Упаковка и распаковка", 
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        point = (3, 4, 5)
        x, y, z = point
        print(x + y + z)
        first, *rest = point
        print(first, rest)
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа?", """
        results = [("login", True), ("pay", False)]
        for name, ok in results:
            print(name, "✅" if ok else "❌")
        a, b = 1, 2
        a, b = b, a
        print(a, b)
        """),
    cod(f"{P}-m1-l3-e3", t("""
        Напиши функцию `distance(p1, p2)` — расстояние между двумя точками-кортежами `(x, y)`, округлённое до 2 знаков. Распакуй координаты в переменные.

        Формула: `√((x2 − x1)² + (y2 − y1)²)`.

        ```
        distance((0, 0), (3, 4))   # → 5.0
        distance((1, 1), (2, 2))   # → 1.41
        ```
        """),
        """
        def distance(p1, p2):
            pass
        """,
        """
        def test_values():
            assert distance((0, 0), (3, 4)) == 5.0 and distance((1, 1), (2, 2)) == 1.41 and distance((5, 5), (5, 5)) == 0, "Неверное расстояние"
        """,
        """
        def distance(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            return round(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5, 2)
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `parse_record(record)` — распаковать кортеж записи теста `(имя, статус, время, *теги)` в словарь:

        ```
        parse_record(("login", "pass", 1.2, "smoke", "auth"))
        # → {"name": "login", "status": "pass", "time": 1.2, "tags": ["smoke", "auth"]}
        parse_record(("pay", "fail", 3.4))
        # → {"name": "pay", "status": "fail", "time": 3.4, "tags": []}
        ```
        """),
        """
        def parse_record(record):
            pass
        """,
        """
        def test_values():
            assert parse_record(("login", "pass", 1.2, "smoke", "auth")) == {"name": "login", "status": "pass", "time": 1.2, "tags": ["smoke", "auth"]}, "Неверная распаковка"
            assert parse_record(("pay", "fail", 3.4))["tags"] == [], "Без тегов — пустой список"
        """,
        """
        def parse_record(record):
            name, status, time, *tags = record
            return {"name": name, "status": status, "time": time, "tags": tags}
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `rotate(t)` — циклический сдвиг кортежа влево на один элемент, используя распаковку со звёздочкой.

        ```
        rotate((1, 2, 3, 4))   # → (2, 3, 4, 1)
        rotate(("a",))         # → ("a",)
        rotate(())             # → ()
        ```
        """),
        """
        def rotate(t):
            pass
        """,
        """
        def test_values():
            assert rotate((1, 2, 3, 4)) == (2, 3, 4, 1) and rotate(("a",)) == ("a",) and rotate(()) == (), "Неверный сдвиг"
        """,
        """
        def rotate(t):
            if not t:
                return ()
            first, *rest = t
            return (*rest, first)
        """)),
)

# ============================================================
m2 = module(f"{P}-m2", "Кортежи в деле", "🧷", "Когда кортеж, а когда список; ключи словаря; сортировка",

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
        """)),

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
        """, xp=20)),

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
        """, xp=20)),
)

# ============================================================
m3 = module(f"{P}-m3", "Продвинутые кортежи", "🏷️", "namedtuple, кортежи из функций и подвох с изменяемым содержимым",

lesson(f"{P}-m3-l1", "namedtuple", 
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        from collections import namedtuple
        Point = namedtuple("Point", ["x", "y"])
        p = Point(3, 4)
        print(p)
        print(p.x + p.y, p[0], isinstance(p, tuple))
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа?", """
        from collections import namedtuple
        TestResult = namedtuple("TestResult", "name status duration")
        r = TestResult("login", "pass", 1.2)
        r2 = r._replace(status="fail")
        print(r.status, r2.status)
        print(r._asdict())
        """),
    cod(f"{P}-m3-l1-e3", t("""
        Создай namedtuple `User` с полями `name`, `email`, `role` и функцию `make_admin(name, email)`, возвращающую `User` с ролью `"admin"`.

        ```
        u = make_admin("root", "root@x.ru")
        u.name, u.role    # → ("root", "admin")
        ```
        """),
        """
        from collections import namedtuple
        """,
        """
        def test_user():
            u = make_admin("root", "root@x.ru")
            assert (u.name, u.email, u.role) == ("root", "root@x.ru", "admin"), f"Получено {u}"
            assert isinstance(u, tuple) and type(u).__name__ == "User", "Используй namedtuple с именем User"
        """,
        """
        from collections import namedtuple

        User = namedtuple("User", ["name", "email", "role"])

        def make_admin(name, email):
            return User(name, email, "admin")
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Есть namedtuple `Bug(id, title, status)` (объявлен в заготовке). Напиши функцию `close_bug(bug)` — вернуть **новый** баг со статусом `"closed"` (исходный кортеж неизменяемый). Используй `_replace`.

        ```
        b = Bug(1, "не работает логин", "open")
        close_bug(b)   # → Bug(id=1, title='не работает логин', status='closed')
        ```
        """),
        """
        from collections import namedtuple

        Bug = namedtuple("Bug", ["id", "title", "status"])

        def close_bug(bug):
            pass
        """,
        """
        def test_close():
            b = Bug(1, "не работает логин", "open")
            closed = close_bug(b)
            assert closed.status == "closed" and closed.id == 1 and b.status == "open", "Нужен новый кортеж со статусом closed"
        """,
        """
        from collections import namedtuple

        Bug = namedtuple("Bug", ["id", "title", "status"])

        def close_bug(bug):
            return bug._replace(status="closed")
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `parse_results(rows)` — превратить строки CSV `"name,status,duration"` в список namedtuple `Result(name, status, duration)`, где `duration` — `float`. Затем функцию `slowest(results)` — имя самого медленного результата.

        ```
        rows = ["login,pass,1.2", "pay,fail,3.4", "cart,pass,0.5"]
        results = parse_results(rows)
        results[1].status   # → "fail"
        slowest(results)    # → "pay"
        ```
        """),
        """
        from collections import namedtuple

        Result = namedtuple("Result", ["name", "status", "duration"])

        def parse_results(rows):
            pass

        def slowest(results):
            pass
        """,
        """
        def test_parse():
            res = parse_results(["login,pass,1.2", "pay,fail,3.4", "cart,pass,0.5"])
            assert res[1] == Result("pay", "fail", 3.4) and isinstance(res[0].duration, float), f"Получено {res}"

        def test_slowest():
            res = parse_results(["login,pass,1.2", "pay,fail,3.4", "cart,pass,0.5"])
            assert slowest(res) == "pay", "Самый медленный — pay"
        """,
        """
        from collections import namedtuple

        Result = namedtuple("Result", ["name", "status", "duration"])

        def parse_results(rows):
            result = []
            for row in rows:
                name, status, duration = row.split(",")
                result.append(Result(name, status, float(duration)))
            return result

        def slowest(results):
            return max(results, key=lambda r: r.duration).name
        """, xp=20)),

lesson(f"{P}-m3-l2", "Кортежи из функций и встроенных инструментов", 
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        print(divmod(17, 5))
        print(list(enumerate("ab")))
        print(list(zip([1, 2], ["x", "y"])))
        print("key=value".partition("="))
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа?", """
        def stats(nums):
            return min(nums), max(nums), sum(nums) / len(nums)

        r = stats([2, 4, 9])
        print(type(r).__name__, len(r))
        lo, hi, avg = r
        print(lo, hi, avg)
        """),
    cod(f"{P}-m3-l2-e3", t("""
        Напиши функцию `split_header(line)` — разобрать строку HTTP-заголовка `"Имя: значение"` в кортеж `(имя в нижнем регистре, значение без пробелов по краям)`. Используй `partition`.

        ```
        split_header("Content-Type: application/json")   # → ("content-type", "application/json")
        split_header("X-Id:42")                          # → ("x-id", "42")
        ```
        """),
        """
        def split_header(line):
            pass
        """,
        """
        def test_values():
            assert split_header("Content-Type: application/json") == ("content-type", "application/json") and split_header("X-Id:42") == ("x-id", "42"), "Неверный разбор"
        """,
        """
        def split_header(line):
            name, _, value = line.partition(":")
            return name.strip().lower(), value.strip()
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши функцию `min_max_avg(nums)` — вернуть кортеж `(минимум, максимум, среднее)` со средним, округлённым до 2 знаков. Для пустого списка вернуть `(None, None, None)`.

        ```
        min_max_avg([2, 4, 9])   # → (2, 9, 5.0)
        min_max_avg([])          # → (None, None, None)
        ```
        """),
        """
        def min_max_avg(nums):
            pass
        """,
        """
        def test_values():
            assert min_max_avg([2, 4, 9]) == (2, 9, 5.0) and min_max_avg([]) == (None, None, None) and min_max_avg([1, 2]) == (1, 2, 1.5), "Неверный результат"
        """,
        """
        def min_max_avg(nums):
            if not nums:
                return None, None, None
            return min(nums), max(nums), round(sum(nums) / len(nums), 2)
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `invert(d)` — «перевернуть» словарь: ключи становятся значениями и наоборот. Используй перебор `d.items()` с распаковкой кортежей.

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
            assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"} and invert({}) == {}, "Неверный словарь"
        """,
        """
        def invert(d):
            result = {}
            for key, value in d.items():
                result[value] = key
            return result
        """)),

lesson(f"{P}-m3-l3", "Изменяемое внутри неизменяемого", 
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        t = ("tags", ["smoke"])
        t[1].append("regress")
        print(t)
        try:
            t[1] = []
        except TypeError:
            print("заменить элемент нельзя")
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа?", """
        a = (1, 2)
        b = (1, [2])
        for value in (a, b):
            try:
                hash(value)
                print(value, "хешируемый")
            except TypeError:
                print(value, "нехешируемый")
        """),
    cod(f"{P}-m3-l3-e3", t("""
        Напиши функцию `is_hashable(value)` — можно ли использовать значение как ключ словаря. Попробуй вызвать `hash(value)` и перехвати `TypeError`.

        ```
        is_hashable((1, 2))      # → True
        is_hashable((1, [2]))    # → False
        is_hashable([1])         # → False
        is_hashable("abc")       # → True
        ```
        """),
        """
        def is_hashable(value):
            pass
        """,
        """
        def test_values():
            got = [is_hashable(v) for v in ((1, 2), (1, [2]), [1], "abc", {"a": 1}, frozenset([1]))]
            assert got == [True, False, False, True, False, True], f"Получено {got}"
        """,
        """
        def is_hashable(value):
            try:
                hash(value)
                return True
            except TypeError:
                return False
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `deep_freeze(value)` — рекурсивно превратить вложенную структуру из списков в кортежи, чтобы результат стал **полностью неизменяемым и хешируемым**. Не-списки возвращать как есть.

        ```
        deep_freeze([1, [2, [3]], 4])   # → (1, (2, (3,)), 4)
        hash(deep_freeze([1, [2]]))     # работает
        ```
        """),
        """
        def deep_freeze(value):
            pass
        """,
        """
        def test_values():
            assert deep_freeze([1, [2, [3]], 4]) == (1, (2, (3,)), 4), f"Получено {deep_freeze([1, [2, [3]], 4])!r}"
            assert deep_freeze(5) == 5 and deep_freeze([]) == (), "Не-списки и пустой список"
            hash(deep_freeze([1, [2]]))
        """,
        """
        def deep_freeze(value):
            if isinstance(value, list):
                return tuple(deep_freeze(v) for v in value)
            return value
        """, xp=20),
    cod(f"{P}-m3-l3-e5", t("""
        В функции `make_config()` баг: она возвращает кортеж-«константу», внутри которого список, и вызывающий код его портит. Сделай так, чтобы настройки были по-настоящему неизменяемыми: верни кортеж `("staging", ("chrome", "firefox"))` — со списком браузеров, превращённым в кортеж.

        ```
        cfg = make_config()
        cfg[1].append("safari")   # должно падать с AttributeError
        ```
        """),
        """
        def make_config():
            return ("staging", ["chrome", "firefox"])
        """,
        """
        def test_frozen():
            cfg = make_config()
            assert cfg == ("staging", ("chrome", "firefox")), f"Получено {cfg!r}"
            try:
                cfg[1].append("safari")
            except AttributeError:
                return
            assert False, "Список браузеров всё ещё можно изменить"
        """,
        """
        def make_config():
            return ("staging", ("chrome", "firefox"))
        """)),
)

TOPIC = topic("py-tuples", "Кортежи", "📎", "#ff86d0",
              "Неизменяемые последовательности, распаковка, ключи словаря и namedtuple",
              m1, m2, m3, group="Python")
