"""Тема «Кортежи», модуль 3 «Продвинутые кортежи» — задания. Теория — в _tpl_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "tpl"

m3 = module(f"{P}-m3", "Продвинутые кортежи", "🏷️", "namedtuple, кортежи из функций, изменяемое внутри, неизменяемость на практике",

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
    out(f"{P}-m3-l1-e6", "Что выведет программа?", """
        from collections import namedtuple
        Point = namedtuple("Point", "x y")
        p = Point(x=1, y=2)
        x, y = p
        print(x, y, p._fields)
        print(Point._make([5, 6]))
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
        """, xp=20),
    cod(f"{P}-m3-l1-e7", t("""
        Объяви namedtuple `Product` с полями `name`, `price`, `qty`, где у `qty` значение по умолчанию `1` (параметр `defaults=[1]`). Напиши функцию `total(products)` — сумма `price * qty` по всем товарам.

        ```
        total([Product("чай", 300), Product("кофе", 500, 2)])   # → 1300
        ```
        """),
        """
        from collections import namedtuple
        """,
        """
        def test_defaults():
            assert Product("чай", 300).qty == 1, "qty по умолчанию — 1"

        def test_total():
            assert total([Product("чай", 300), Product("кофе", 500, 2)]) == 1300 and total([]) == 0, "Неверная сумма"
        """,
        """
        from collections import namedtuple

        Product = namedtuple("Product", ["name", "price", "qty"], defaults=[1])

        def total(products):
            return sum(p.price * p.qty for p in products)
        """, hint="defaults применяются к последним полям: defaults=[1] — значение для qty."),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `to_dicts(results)` — превратить список namedtuple в список обычных словарей (для отправки в JSON). Используй `_asdict()`.

        ```
        R = namedtuple("R", "name status")
        to_dicts([R("login", "pass")])   # → [{"name": "login", "status": "pass"}]
        ```
        """),
        """
        def to_dicts(results):
            pass
        """,
        """
        from collections import namedtuple

        def test_values():
            R = namedtuple("R", "name status")
            got = to_dicts([R("login", "pass"), R("pay", "fail")])
            assert got == [{"name": "login", "status": "pass"}, {"name": "pay", "status": "fail"}] and to_dicts([]) == [], f"Получено {got}"
        """,
        """
        def to_dicts(results):
            return [dict(r._asdict()) for r in results]
        """),
),

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
    out(f"{P}-m3-l2-e6", "Что выведет программа?", """
        text = "name=Anna"
        print(text.partition("="), text.rpartition("x"))
        q, r = divmod(-7, 2)
        print(q, r)
        """, hint="divmod(-7, 2): целая часть округляется вниз, к -4; остаток 1."),
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
        """),
    cod(f"{P}-m3-l2-e7", t("""
        Напиши функцию `time_parts(seconds)` — кортеж `(часы, минуты, секунды)` из общего числа секунд. Используй `divmod` дважды.

        ```
        time_parts(3725)   # → (1, 2, 5)
        time_parts(59)     # → (0, 0, 59)
        ```
        """),
        """
        def time_parts(seconds):
            pass
        """,
        """
        def test_values():
            assert time_parts(3725) == (1, 2, 5) and time_parts(59) == (0, 0, 59) and time_parts(7200) == (2, 0, 0), "Неверный результат"

        def test_divmod():
            assert "divmod(" in open("solution.py", encoding="utf-8").read(), "Используй divmod"
        """,
        """
        def time_parts(seconds):
            minutes, s = divmod(seconds, 60)
            h, m = divmod(minutes, 60)
            return (h, m, s)
        """),
    cod(f"{P}-m3-l2-e8", t("""
        Напиши функцию `split_ext(filename)` — кортеж `(имя, расширение)` по **последней** точке (используй `rpartition`). Если точки нет — `(filename, "")`.

        ```
        split_ext("report.final.pdf")   # → ("report.final", "pdf")
        split_ext("README")             # → ("README", "")
        ```
        """),
        """
        def split_ext(filename):
            pass
        """,
        """
        def test_values():
            got = [split_ext("report.final.pdf"), split_ext("README"), split_ext("a.txt")]
            assert got == [("report.final", "pdf"), ("README", ""), ("a", "txt")], f"Получено {got}"
        """,
        """
        def split_ext(filename):
            name, dot, ext = filename.rpartition(".")
            if not dot:
                return (filename, "")
            return (name, ext)
        """, hint='Без разделителя rpartition вернёт ("", "", строка).'),
),

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
    out(f"{P}-m3-l3-e6", "Что выведет программа? Знаменитая загадка с +=.", """
        t = ([1], [2])
        t[0].append(10)
        print(t)
        try:
            t[0] += [20]
        except TypeError:
            print("TypeError")
        print(t)
        """, hint="+= сначала расширяет список на месте, а потом пытается записать его в кортеж — и падает."),
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
        """),
    cod(f"{P}-m3-l3-e7", t("""
        Напиши функцию `contains_mutable(t)` — есть ли в кортеже (на верхнем уровне) изменяемые элементы: списки, словари или множества.

        ```
        contains_mutable((1, "a", (2,)))   # → False
        contains_mutable((1, [2]))         # → True
        ```
        """),
        """
        def contains_mutable(t):
            pass
        """,
        """
        def test_values():
            got = [contains_mutable((1, "a", (2,))), contains_mutable((1, [2])), contains_mutable(({},)), contains_mutable((set(),)), contains_mutable(())]
            assert got == [False, True, True, True, False], f"Получено {got}"
        """,
        """
        def contains_mutable(t):
            for x in t:
                if isinstance(x, (list, dict, set)):
                    return True
            return False
        """),
    cod(f"{P}-m3-l3-e8", t("""
        Напиши функцию `snapshot(config)` — «снимок» словаря настроек, где значения — списки. Вернуть кортеж пар `(ключ, кортеж_значений)`, отсортированный по ключу. Снимок полностью неизменяемый и хешируемый.

        ```
        snapshot({"browsers": ["chrome", "ff"], "envs": ["dev"]})
        # → (("browsers", ("chrome", "ff")), ("envs", ("dev",)))
        ```
        """),
        """
        def snapshot(config):
            pass
        """,
        """
        def test_values():
            s = snapshot({"browsers": ["chrome", "ff"], "envs": ["dev"]})
            assert s == (("browsers", ("chrome", "ff")), ("envs", ("dev",))), f"Получено {s!r}"
            hash(s)
        """,
        """
        def snapshot(config):
            return tuple((key, tuple(config[key])) for key in sorted(config))
        """, xp=20),
),

lesson(f"{P}-immut", "Неизменяемость на практике",
    out(f"{P}-immut-e1", "Что выведет программа? += у кортежа и у списка.", """
        t = (1, 2)
        before = id(t)
        t += (3,)
        print(t, id(t) == before)
        lst = [1, 2]
        before = id(lst)
        lst += [3]
        print(lst, id(lst) == before)
        """, hint="id — «номер» объекта. Кортеж при += создаётся новый, список расширяется на месте."),
    out(f"{P}-immut-e2", "Что выведет программа? Кортеж как безопасное значение по умолчанию.", """
        def add_default(items=()):
            return items + ("default",)

        print(add_default(), add_default())
        """),
    out(f"{P}-immut-e3", "Что выведет программа?", """
        a = (1, 2, 3)
        b = a
        b = b + (4,)
        print(a, b, a is b)
        """),
    cod(f"{P}-immut-e4", t("""
        Напиши функцию `with_updated(t, index, value)` — **новый** кортеж, где элемент с индексом `index` заменён на `value`. Используй срезы.

        ```
        with_updated((1, 2, 3), 1, 99)   # → (1, 99, 3)
        ```
        """),
        """
        def with_updated(t, index, value):
            pass
        """,
        """
        def test_values():
            src = (1, 2, 3)
            assert with_updated(src, 1, 99) == (1, 99, 3) and with_updated(src, 0, 0) == (0, 2, 3) and src == (1, 2, 3), "Неверный результат"
        """,
        """
        def with_updated(t, index, value):
            return t[:index] + (value,) + t[index + 1:]
        """),
    cod(f"{P}-immut-e5", t("""
        Напиши функцию `remove_from(t, value)` — новый кортеж без всех вхождений `value`.

        ```
        remove_from((1, 2, 1, 3), 1)   # → (2, 3)
        ```
        """),
        """
        def remove_from(t, value):
            pass
        """,
        """
        def test_values():
            assert remove_from((1, 2, 1, 3), 1) == (2, 3) and remove_from((), 1) == () and remove_from((5,), 1) == (5,), "Неверный результат"
        """,
        """
        def remove_from(t, value):
            return tuple(x for x in t if x != value)
        """),
    cod(f"{P}-immut-e6", t("""
        Напиши функцию `insert_at(t, index, value)` — новый кортеж со вставленным перед позицией `index` значением.

        ```
        insert_at((1, 2, 3), 1, "x")   # → (1, "x", 2, 3)
        insert_at((1, 2), 2, "x")      # → (1, 2, "x")
        ```
        """),
        """
        def insert_at(t, index, value):
            pass
        """,
        """
        def test_values():
            assert insert_at((1, 2, 3), 1, "x") == (1, "x", 2, 3) and insert_at((1, 2), 2, "x") == (1, 2, "x") and insert_at((), 0, 5) == (5,), "Неверный результат"
        """,
        """
        def insert_at(t, index, value):
            return t[:index] + (value,) + t[index:]
        """),
    cod(f"{P}-immut-e7", t("""
        Напиши функцию `append_log(entry, log=())` — вернуть новый кортеж-журнал с добавленной записью. Кортеж по умолчанию безопасен: вызовы без `log` не должны «помнить» друг друга (в отличие от списка по умолчанию).

        ```
        append_log("a")          # → ("a",)
        append_log("b")          # → ("b",)
        append_log("c", ("a",))  # → ("a", "c")
        ```
        """),
        """
        def append_log(entry, log=()):
            pass
        """,
        """
        def test_values():
            assert append_log("a") == ("a",) and append_log("b") == ("b",) and append_log("c", ("a",)) == ("a", "c"), "Неверный журнал"
        """,
        """
        def append_log(entry, log=()):
            return log + (entry,)
        """),
    cod(f"{P}-immut-e8", t("""
        Напиши функцию `apply_moves(start, moves)` — точка `start = (x, y)` последовательно сдвигается на каждый `(dx, dy)` из списка. Каждый раз создаётся **новый** кортеж. Вернуть итоговую точку.

        ```
        apply_moves((0, 0), [(1, 2), (3, -1)])   # → (4, 1)
        ```
        """),
        """
        def apply_moves(start, moves):
            pass
        """,
        """
        def test_values():
            assert apply_moves((0, 0), [(1, 2), (3, -1)]) == (4, 1) and apply_moves((5, 5), []) == (5, 5), "Неверная точка"
        """,
        """
        def apply_moves(start, moves):
            point = start
            for dx, dy in moves:
                x, y = point
                point = (x + dx, y + dy)
            return point
        """),
),
)
