"""Тема «Изменяемые и неизменяемые», модуль 2 «Функции и копии» — задания. Теория — в _mut_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "mut"

m2 = module(f"{P}-m2", "Функции и копии", "📋", "Аргументы-ссылки, изменяемые значения по умолчанию, поверхностная и глубокая копия",

lesson(f"{P}-args", "Изменяемые аргументы функций",
    out(f"{P}-args-e1", "Что выведет программа? Функция меняет список.", """
        def add_bonus(scores):
            for i in range(len(scores)):
                scores[i] += 10

        my = [50, 70]
        add_bonus(my)
        print(my)
        """, hint="Функция получает ссылку на тот же список."),
    out(f"{P}-args-e2", "Что выведет программа? Переприсваивание внутри функции.", """
        def reset(items):
            items = []
            items.append("новый")
            return items

        def clear(items):
            items.clear()

        data = [1, 2]
        print(reset(data), data)
        clear(data)
        print(data)
        """, hint="items = [] меняет только локальное имя, clear() — сам объект."),
    out(f"{P}-args-e3", "Что выведет программа? Числа и строки не изменить.", """
        def inc(n):
            n += 1
            return n

        def shout(s):
            s += "!"
            return s

        x, word = 5, "привет"
        print(inc(x), x)
        print(shout(word), word)
        """),
    cod(f"{P}-args-e4", t("""
        Напиши функцию `with_bonus(scores, bonus)` — вернуть **новый** список баллов, увеличенных на `bonus`. Исходный список не менять.
        """),
        """
        def with_bonus(scores, bonus):
            pass
        """,
        """
        def test_values():
            s = [50, 70]
            assert with_bonus(s, 10) == [60, 80] and s == [50, 70], "Исходный список изменился"
        """,
        """
        def with_bonus(scores, bonus):
            return [x + bonus for x in scores]
        """),
    cod(f"{P}-args-e5", t("""
        Функция `normalize_user` из заготовки портит переданный словарь. Исправь: работать с копией, исходный словарь не менять.
        """),
        """
        def normalize_user(user):
            user["name"] = user["name"].strip().title()
            user["email"] = user["email"].lower()
            return user
        """,
        """
        def test_values():
            u = {"name": "  аня ", "email": "A@X.RU", "id": 1}
            r = normalize_user(u)
            assert r == {"name": "Аня", "email": "a@x.ru", "id": 1} and u == {"name": "  аня ", "email": "A@X.RU", "id": 1}, u
        """,
        """
        def normalize_user(user):
            user = dict(user)
            user["name"] = user["name"].strip().title()
            user["email"] = user["email"].lower()
            return user
        """),
    cod(f"{P}-args-e6", t("""
        Напиши функцию `move_done(todo, done)` — перенести все задачи, заканчивающиеся на `"✓"`, из списка `todo` в список `done` **на месте** (оба списка меняются). Вернуть количество перенесённых.
        """),
        """
        def move_done(todo, done):
            pass
        """,
        """
        def test_values():
            todo = ["код ✓", "тесты", "ревью ✓"]
            done = ["старт ✓"]
            assert move_done(todo, done) == 2 and todo == ["тесты"] and done == ["старт ✓", "код ✓", "ревью ✓"], (todo, done)
        """,
        """
        def move_done(todo, done):
            finished = [t for t in todo if t.endswith("✓")]
            todo[:] = [t for t in todo if not t.endswith("✓")]
            done.extend(finished)
            return len(finished)
        """),
    cod(f"{P}-args-e7", t("""
        Напиши функцию `safe_process(data, func)` — вызвать `func(копия_data)` и вернуть результат. Даже если `func` меняет переданный список, исходный `data` должен остаться прежним.
        """),
        """
        def safe_process(data, func):
            pass
        """,
        """
        def test_values():
            def evil(x):
                x.append(99)
                return len(x)
            d = [1, 2]
            assert safe_process(d, evil) == 3 and d == [1, 2], d
        """,
        """
        def safe_process(data, func):
            return func(list(data))
        """),
    cod(f"{P}-args-e8", t("""
        Напиши функцию `apply_discount(cart, percent)` — `cart` — список словарей `{"name", "price"}`. Вернуть **новый** список новых словарей с уменьшенной ценой (округлить до 2 знаков). Исходная корзина и её словари не должны меняться.
        """),
        """
        def apply_discount(cart, percent):
            pass
        """,
        """
        def test_values():
            cart = [{"name": "чай", "price": 100}, {"name": "кофе", "price": 250}]
            r = apply_discount(cart, 10)
            assert r == [{"name": "чай", "price": 90.0}, {"name": "кофе", "price": 225.0}], r
            assert cart == [{"name": "чай", "price": 100}, {"name": "кофе", "price": 250}], "Исходная корзина изменилась"
        """,
        """
        def apply_discount(cart, percent):
            return [{**item, "price": round(item["price"] * (1 - percent / 100), 2)} for item in cart]
        """, hint="Копировать нужно и список, и каждый словарь.", xp=20),
),

lesson(f"{P}-default", "Изменяемые значения по умолчанию",
    out(f"{P}-default-e1", "Что выведет программа? Классическая ловушка.", """
        def add(item, items=[]):
            items.append(item)
            return items

        print(add("a"))
        print(add("b"))
        print(add("c", []))
        print(add("d"))
        """, hint="Список по умолчанию создаётся один раз — при объявлении функции."),
    out(f"{P}-default-e2", "Что выведет программа? Где живёт значение по умолчанию.", """
        def log(msg, history=[]):
            history.append(msg)
            return len(history)

        log("старт")
        log("стоп")
        print(log.__defaults__)
        """),
    out(f"{P}-default-e3", "Что выведет программа? Правильный вариант.", """
        def add(item, items=None):
            if items is None:
                items = []
            items.append(item)
            return items

        print(add("a"), add("b"))
        shared = ["x"]
        print(add("y", shared), shared)
        """),
    cod(f"{P}-default-e4", t("""
        Исправь функцию `add_tag` из заготовки: у неё значение по умолчанию — изменяемый список, поэтому теги «накапливаются» между вызовами.
        """),
        """
        def add_tag(tag, tags=[]):
            tags.append(tag)
            return tags
        """,
        """
        def test_values():
            assert add_tag("a") == ["a"] and add_tag("b") == ["b"], "Вызовы не должны влиять друг на друга"
            mine = ["x"]
            assert add_tag("y", mine) == ["x", "y"] and mine == ["x", "y"], "Переданный список дополняется"
        """,
        """
        def add_tag(tag, tags=None):
            if tags is None:
                tags = []
            tags.append(tag)
            return tags
        """),
    cod(f"{P}-default-e5", t("""
        Исправь функцию `make_request` из заготовки: у неё словарь по умолчанию, и заголовки из одного вызова попадают в другой.
        """),
        """
        def make_request(url, headers={}):
            headers["Accept"] = "json"
            return {"url": url, "headers": headers}
        """,
        """
        def test_values():
            r1 = make_request("/a")
            r1["headers"]["X-Token"] = "secret"
            r2 = make_request("/b")
            assert r2["headers"] == {"Accept": "json"}, f"Заголовки протекли: {r2['headers']}"
        """,
        """
        def make_request(url, headers=None):
            headers = dict(headers or {})
            headers["Accept"] = "json"
            return {"url": url, "headers": headers}
        """),
    cod(f"{P}-default-e6", t("""
        Напиши функцию `has_mutable_defaults(func)` — `True`, если среди значений по умолчанию функции (`func.__defaults__`, может быть `None`) есть список, словарь или множество.
        """),
        """
        def has_mutable_defaults(func):
            pass
        """,
        """
        def test_values():
            def a(x, y=[]): pass
            def b(x, y=None, z=1): pass
            def c(x): pass
            def d(x={}): pass
            assert has_mutable_defaults(a) and not has_mutable_defaults(b) and not has_mutable_defaults(c) and has_mutable_defaults(d), "Неверный результат"
        """,
        """
        def has_mutable_defaults(func):
            return any(isinstance(v, (list, dict, set)) for v in (func.__defaults__ or ()))
        """),
    cod(f"{P}-default-e7", t("""
        Иногда «общий» изменяемый объект нужен специально — например, для кэша. Напиши функцию `cached_square(n, _cache={})` — считает `n * n`, сохраняет результат в словаре по умолчанию и возвращает кортеж `(результат, был_ли_в_кэше)`.
        """),
        """
        def cached_square(n, _cache={}):
            pass
        """,
        """
        def test_values():
            assert cached_square(4) == (16, False) and cached_square(4) == (16, True) and cached_square(5) == (25, False), "Неверный результат"
        """,
        """
        def cached_square(n, _cache={}):
            if n in _cache:
                return _cache[n], True
            _cache[n] = n * n
            return _cache[n], False
        """, hint="Подчёркивание в имени — знак «не передавать снаружи»."),
    cod(f"{P}-default-e8", t("""
        Исправь класс `Suite` из заготовки: у всех наборов тестов оказывается один общий список `tests`, потому что он задан значением по умолчанию в `__init__`.
        """),
        """
        class Suite:
            def __init__(self, name, tests=[]):
                self.name = name
                self.tests = tests

            def add(self, test):
                self.tests.append(test)
        """,
        """
        def test_values():
            a, b = Suite("api"), Suite("ui")
            a.add("login")
            assert b.tests == [] and a.tests == ["login"], "Списки наборов должны быть разными"
            src = ["x"]
            c = Suite("c", src)
            c.add("y")
            assert src == ["x"], "Переданный список не должен меняться"
        """,
        """
        class Suite:
            def __init__(self, name, tests=None):
                self.name = name
                self.tests = list(tests) if tests is not None else []

            def add(self, test):
                self.tests.append(test)
        """, xp=20),
),

lesson(f"{P}-copy", "Поверхностная копия",
    out(f"{P}-copy-e1", "Что выведет программа? Способы скопировать список.", """
        a = [1, 2, 3]
        copies = [a[:], list(a), a.copy(), [*a]]
        for c in copies:
            c.append(4)
        print(a, [c is a for c in copies])
        """),
    out(f"{P}-copy-e2", "Что выведет программа? Вложенные списки общие.", """
        a = [[1, 2], [3, 4]]
        b = a.copy()
        b.append([5])
        b[0].append(99)
        print(a)
        print(b)
        print(a[0] is b[0])
        """, hint="Копия поверхностная: внешний список новый, внутренние — те же."),
    out(f"{P}-copy-e3", "Что выведет программа? Копия словаря.", """
        user = {"name": "Аня", "tags": ["qa"]}
        copy1 = dict(user)
        copy2 = user.copy()
        copy1["name"] = "Боря"
        copy2["tags"].append("api")
        print(user)
        """),
    cod(f"{P}-copy-e4", t("""
        Напиши функцию `copy_and_sort(items)` — вернуть отсортированную **копию** списка через `.copy()` и `.sort()`; исходный список не менять.
        """),
        """
        def copy_and_sort(items):
            pass
        """,
        """
        def test_values():
            x = [3, 1, 2]
            assert copy_and_sort(x) == [1, 2, 3] and x == [3, 1, 2], "Неверный результат"
        """,
        """
        def copy_and_sort(items):
            result = items.copy()
            result.sort()
            return result
        """),
    cod(f"{P}-copy-e5", t("""
        Напиши функцию `copy_matrix(matrix)` — копия списка списков, в которой **каждая строка** тоже скопирована (изменение копии не затрагивает оригинал). Без модуля `copy`.
        """),
        """
        def copy_matrix(matrix):
            pass
        """,
        """
        def test_values():
            m = [[1, 2], [3, 4]]
            c = copy_matrix(m)
            c[0][0] = 99
            c.append([5])
            assert m == [[1, 2], [3, 4]] and c == [[99, 2], [3, 4], [5]], (m, c)
        """,
        """
        def copy_matrix(matrix):
            return [row[:] for row in matrix]
        """),
    cod(f"{P}-copy-e6", t("""
        Напиши функцию `copy_users(users)` — `users` — список словарей с простыми значениями. Вернуть список **копий** словарей, чтобы изменение копий не трогало оригиналы.
        """),
        """
        def copy_users(users):
            pass
        """,
        """
        def test_values():
            src = [{"name": "Аня"}, {"name": "Боря"}]
            c = copy_users(src)
            c[0]["name"] = "X"
            assert src == [{"name": "Аня"}, {"name": "Боря"}] and c == [{"name": "X"}, {"name": "Боря"}], src
        """,
        """
        def copy_users(users):
            return [dict(u) for u in users]
        """),
    cod(f"{P}-copy-e7", t("""
        Напиши функцию `shares_inner(a, b)` — два списка списков. Верни `True`, если хотя бы один внутренний список является **одним и тем же** объектом в обоих (так бывает после поверхностной копии).
        """),
        """
        def shares_inner(a, b):
            pass
        """,
        """
        def test_values():
            m = [[1], [2]]
            assert shares_inner(m, m.copy()) and not shares_inner(m, [r[:] for r in m]) and not shares_inner([], []), "Неверный результат"
        """,
        """
        def shares_inner(a, b):
            ids = {id(x) for x in a}
            return any(id(x) in ids for x in b)
        """),
    cod(f"{P}-copy-e8", t("""
        Напиши функцию `update_config(config, section, key, value)` — `config` — словарь словарей. Вернуть новый конфиг, где `config[section][key] = value`. Исходный конфиг (включая вложенный словарь секции) должен остаться прежним; остальные секции можно не копировать.
        """),
        """
        def update_config(config, section, key, value):
            pass
        """,
        """
        def test_values():
            cfg = {"api": {"url": "prod", "timeout": 5}, "ui": {"browser": "chrome"}}
            new = update_config(cfg, "api", "url", "test")
            assert new == {"api": {"url": "test", "timeout": 5}, "ui": {"browser": "chrome"}}, new
            assert cfg["api"]["url"] == "prod", "Исходный конфиг изменился"
            assert update_config(cfg, "db", "host", "x")["db"] == {"host": "x"}, "Новая секция"
        """,
        """
        def update_config(config, section, key, value):
            new = dict(config)
            new[section] = {**config.get(section, {}), key: value}
            return new
        """, xp=20),
),

lesson(f"{P}-deepcopy", "Глубокая копия",
    out(f"{P}-deepcopy-e1", "Что выведет программа? copy и deepcopy.", """
        import copy

        data = {"users": [{"name": "Аня"}]}
        shallow = copy.copy(data)
        deep = copy.deepcopy(data)
        data["users"][0]["name"] = "Изменено"
        print(shallow["users"][0]["name"], deep["users"][0]["name"])
        """),
    out(f"{P}-deepcopy-e2", "Что выведет программа? Ловушка умножения списка.", """
        grid = [[0] * 3] * 2
        grid[0][0] = 1
        print(grid, grid[0] is grid[1])

        good = [[0] * 3 for _ in range(2)]
        good[0][0] = 1
        print(good)
        """, hint="* повторяет ссылку на тот же внутренний список."),
    out(f"{P}-deepcopy-e3", "Что выведет программа? Общие ссылки сохраняются.", """
        import copy

        shared = [1, 2]
        pair = [shared, shared]
        clone = copy.deepcopy(pair)
        clone[0].append(3)
        print(clone, clone[0] is clone[1], shared)
        """, hint="deepcopy копирует каждый объект один раз и сохраняет структуру ссылок."),
    cod(f"{P}-deepcopy-e4", t("""
        Напиши функцию `clone(data)` — полностью независимая копия любой вложенной структуры (используй `copy.deepcopy`).
        """),
        """
        import copy


        def clone(data):
            pass
        """,
        """
        def test_values():
            d = {"a": [1, {"b": [2]}]}
            c = clone(d)
            c["a"][1]["b"].append(3)
            assert d == {"a": [1, {"b": [2]}]} and c == {"a": [1, {"b": [2, 3]}]}, d
        """,
        """
        import copy


        def clone(data):
            return copy.deepcopy(data)
        """),
    cod(f"{P}-deepcopy-e5", t("""
        Напиши функцию `deep_copy(value)` **без** модуля `copy`: рекурсивно скопировать списки и словари (ключи копировать не нужно), остальные значения вернуть как есть.
        """),
        """
        def deep_copy(value):
            pass
        """,
        """
        def test_values():
            d = {"a": [1, [2]], "b": {"c": [3]}}
            c = deep_copy(d)
            c["a"][1].append(9)
            c["b"]["c"].append(9)
            assert d == {"a": [1, [2]], "b": {"c": [3]}} and c == {"a": [1, [2, 9]], "b": {"c": [3, 9]}}, d
            assert "import copy" not in open("solution.py", encoding="utf-8").read(), "Без модуля copy"
        """,
        """
        def deep_copy(value):
            if isinstance(value, list):
                return [deep_copy(v) for v in value]
            if isinstance(value, dict):
                return {k: deep_copy(v) for k, v in value.items()}
            return value
        """),
    cod(f"{P}-deepcopy-e6", t("""
        Функция `make_board` из заготовки создаёт игровое поле через умножение списков, и ход в одну клетку отражается во всех строках. Исправь её.
        """),
        """
        def make_board(size):
            return [["."] * size] * size
        """,
        """
        def test_values():
            b = make_board(3)
            b[1][1] = "X"
            assert b == [[".", ".", "."], [".", "X", "."], [".", ".", "."]], b
        """,
        """
        def make_board(size):
            return [["."] * size for _ in range(size)]
        """),
    cod(f"{P}-deepcopy-e7", t("""
        Напиши функцию `template_payload(template, **changes)` — `template` — вложенный словарь (эталонное тело запроса). Верни **глубокую копию** с заменёнными верхнеуровневыми ключами из `changes`. Эталон не должен меняться даже при изменении вложенных частей результата.
        """),
        """
        import copy


        def template_payload(template, **changes):
            pass
        """,
        """
        TEMPLATE = {"user": {"name": "test", "roles": ["reader"]}, "active": True}

        def test_values():
            p = template_payload(TEMPLATE, active=False)
            p["user"]["roles"].append("admin")
            assert p == {"user": {"name": "test", "roles": ["reader", "admin"]}, "active": False}, p
            assert TEMPLATE == {"user": {"name": "test", "roles": ["reader"]}, "active": True}, "Эталон изменился"
        """,
        """
        import copy


        def template_payload(template, **changes):
            payload = copy.deepcopy(template)
            payload.update(changes)
            return payload
        """),
    cod(f"{P}-deepcopy-e8", t("""
        Напиши функцию `is_independent(a, b)` — `True`, если две вложенные структуры из списков и словарей **не имеют общих изменяемых объектов** (ни на каком уровне). Сравнивай по `id`.
        """),
        """
        import copy


        def is_independent(a, b):
            pass
        """,
        """
        import copy

        def test_values():
            d = {"x": [1, {"y": [2]}]}
            assert is_independent(d, copy.deepcopy(d)), "Глубокая копия независима"
            assert not is_independent(d, copy.copy(d)), "Поверхностная делит вложенные"
            assert not is_independent(d, d), "Сам с собой"
        """,
        """
        import copy


        def _mutable_ids(value, acc):
            if isinstance(value, (list, dict)):
                acc.add(id(value))
                items = value.values() if isinstance(value, dict) else value
                for v in items:
                    _mutable_ids(v, acc)
            return acc


        def is_independent(a, b):
            return not (_mutable_ids(a, set()) & _mutable_ids(b, set()))
        """, xp=25),
),
)
