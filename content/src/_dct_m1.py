"""Тема «Словари», модуль 1 «Основы словарей» — задания. Теория — в _dct_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "dct"

m1 = module(f"{P}-m1", "Основы словарей", "📖", "Создание, доступ, изменение, get и тонкости ключей",

lesson(f"{P}-m1-l1", "Создание и доступ по ключу",
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        user = {"name": "Аня", "age": 25, "role": "qa"}
        print(user["name"], user["age"])
        print("role" in user, "email" in user, len(user))
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа?", """
        codes = {200: "OK", 404: "Not Found"}
        print(codes[404])
        try:
            print(codes[500])
        except KeyError as e:
            print("нет ключа", e)
        d = {"a": 1, "a": 2}
        print(d)
        """, hint="Повторяющийся ключ — последнее значение побеждает."),
    out(f"{P}-m1-l1-e6", "Что выведет программа? in проверяет ключи.", """
        empty = {}
        print(type(empty).__name__, len(empty))
        d = {"x": 1}
        print(d["x"], "x" in d, 1 in d)
        """, hint="in для словаря ищет среди ключей, а не значений."),
    cod(f"{P}-m1-l1-e3", t("""
        Создай словарь `user` с ключами `"name"` → `"Аня"`, `"age"` → `25`, `"active"` → `True`. Затем напиши функцию `describe(u)`, возвращающую строку `"<name>, <age> лет"`.

        ```
        describe(user)   # → "Аня, 25 лет"
        ```
        """),
        "",
        """
        def test_dict():
            assert user == {"name": "Аня", "age": 25, "active": True}, f"Получено {user}"

        def test_describe():
            assert describe(user) == "Аня, 25 лет" and describe({"name": "Боря", "age": 30}) == "Боря, 30 лет", "Неверная строка"
        """,
        """
        user = {"name": "Аня", "age": 25, "active": True}

        def describe(u):
            return f"{u['name']}, {u['age']} лет"
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `status_text(code)` — текст статуса по коду из словаря `STATUS = {200: "OK", 201: "Created", 404: "Not Found", 500: "Server Error"}`. Если кода нет — `"Unknown"`. Используй проверку `in`.

        ```
        status_text(404)   # → "Not Found"
        status_text(418)   # → "Unknown"
        ```
        """),
        """
        STATUS = {200: "OK", 201: "Created", 404: "Not Found", 500: "Server Error"}

        def status_text(code):
            pass
        """,
        """
        def test_values():
            assert [status_text(c) for c in (200, 404, 500, 418)] == ["OK", "Not Found", "Server Error", "Unknown"], "Неверный текст"
        """,
        """
        STATUS = {200: "OK", 201: "Created", 404: "Not Found", 500: "Server Error"}

        def status_text(code):
            if code in STATUS:
                return STATUS[code]
            return "Unknown"
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `has_required(data, required)` — есть ли в словаре `data` **все** ключи из списка `required`.

        ```
        has_required({"id": 1, "name": "A"}, ["id", "name"])           # → True
        has_required({"id": 1}, ["id", "email"])                        # → False
        ```
        """),
        """
        def has_required(data, required):
            pass
        """,
        """
        def test_values():
            assert has_required({"id": 1, "name": "A"}, ["id", "name"]) is True, "Все ключи есть"
            assert has_required({"id": 1}, ["id", "email"]) is False, "email нет"
            assert has_required({}, []) is True, "Нечего требовать — True"
        """,
        """
        def has_required(data, required):
            return all(key in data for key in required)
        """),
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `make_user(name, age)` — вернуть словарь пользователя с ключами `"name"`, `"age"` и `"active"` (всегда `True`).

        ```
        make_user("Аня", 25)   # → {"name": "Аня", "age": 25, "active": True}
        ```
        """),
        """
        def make_user(name, age):
            pass
        """,
        """
        def test_values():
            assert make_user("Аня", 25) == {"name": "Аня", "age": 25, "active": True}, f"Получено {make_user('Аня', 25)}"
        """,
        """
        def make_user(name, age):
            return {"name": name, "age": age, "active": True}
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `count_keys_with(d, prefix)` — сколько ключей словаря начинаются с `prefix`.

        ```
        count_keys_with({"test_login": 1, "test_pay": 2, "helper": 3}, "test_")   # → 2
        ```
        """),
        """
        def count_keys_with(d, prefix):
            pass
        """,
        """
        def test_values():
            assert count_keys_with({"test_login": 1, "test_pay": 2, "helper": 3}, "test_") == 2 and count_keys_with({}, "x") == 0, "Неверный подсчёт"
        """,
        """
        def count_keys_with(d, prefix):
            count = 0
            for key in d:
                if key.startswith(prefix):
                    count += 1
            return count
        """),
),

lesson(f"{P}-create2", "Способы создать словарь",
    out(f"{P}-create2-e1", "Что выведет программа?", """
        a = dict(name="Аня", age=25)
        b = dict([("x", 1), ("y", 2)])
        c = dict(zip(["k1", "k2"], [10, 20]))
        print(a, b, c)
        """),
    out(f"{P}-create2-e2", "Что выведет программа? dict.fromkeys.", """
        d = dict.fromkeys(["pass", "fail", "skip"], 0)
        print(d)
        e = dict.fromkeys("ab")
        print(e)
        """),
    out(f"{P}-create2-e3", "Что выведет программа? Ловушка fromkeys со списком.", """
        d = dict.fromkeys(["a", "b"], [])
        d["a"].append(1)
        print(d)
        """, hint="fromkeys кладёт ОДИН и тот же список во все ключи."),
    cod(f"{P}-create2-e4", t("""
        Напиши функцию `from_pairs(keys, values)` — словарь из двух списков через `dict(zip(...))`.

        ```
        from_pairs(["host", "port"], ["localhost", 8080])   # → {"host": "localhost", "port": 8080}
        ```
        """),
        """
        def from_pairs(keys, values):
            pass
        """,
        """
        def test_values():
            assert from_pairs(["host", "port"], ["localhost", 8080]) == {"host": "localhost", "port": 8080} and from_pairs([], []) == {}, "Неверный словарь"
        """,
        """
        def from_pairs(keys, values):
            return dict(zip(keys, values))
        """),
    cod(f"{P}-create2-e5", t("""
        Напиши функцию `init_counters(names)` — словарь, где каждому имени соответствует `0`. Используй `dict.fromkeys`.

        ```
        init_counters(["pass", "fail"])   # → {"pass": 0, "fail": 0}
        ```
        """),
        """
        def init_counters(names):
            pass
        """,
        """
        def test_values():
            assert init_counters(["pass", "fail"]) == {"pass": 0, "fail": 0} and init_counters([]) == {}, "Неверный словарь"

        def test_fromkeys():
            assert "fromkeys" in open("solution.py", encoding="utf-8").read(), "Используй dict.fromkeys"
        """,
        """
        def init_counters(names):
            return dict.fromkeys(names, 0)
        """),
    cod(f"{P}-create2-e6", t("""
        Напиши функцию `empty_groups(names)` — словарь, где каждому имени соответствует **свой** пустой список. Списки должны быть независимыми (`fromkeys` здесь не подходит!) — используй словарное включение или цикл.

        ```
        g = empty_groups(["qa", "dev"])
        g["qa"].append("Аня")
        g   # → {"qa": ["Аня"], "dev": []}
        ```
        """),
        """
        def empty_groups(names):
            pass
        """,
        """
        def test_independent():
            g = empty_groups(["qa", "dev"])
            g["qa"].append("Аня")
            assert g == {"qa": ["Аня"], "dev": []}, f"Списки общие: {g}"
        """,
        """
        def empty_groups(names):
            return {name: [] for name in names}
        """),
    cod(f"{P}-create2-e7", t("""
        Напиши функцию `parse_query(query)` — разобрать строку параметров URL `"a=1&b=2"` в словарь строк. Пустая строка — пустой словарь.

        ```
        parse_query("page=2&sort=name")   # → {"page": "2", "sort": "name"}
        parse_query("")                   # → {}
        ```
        """),
        """
        def parse_query(query):
            pass
        """,
        """
        def test_values():
            assert parse_query("page=2&sort=name") == {"page": "2", "sort": "name"} and parse_query("") == {} and parse_query("x=") == {"x": ""}, "Неверный разбор"
        """,
        """
        def parse_query(query):
            result = {}
            if not query:
                return result
            for part in query.split("&"):
                key, _, value = part.partition("=")
                result[key] = value
            return result
        """, xp=20),
    cod(f"{P}-create2-e8", t("""
        Напиши функцию `to_records(names, ages)` — список словарей `{"name": ..., "age": ...}` из двух параллельных списков.

        ```
        to_records(["Аня", "Боря"], [25, 30])
        # → [{"name": "Аня", "age": 25}, {"name": "Боря", "age": 30}]
        ```
        """),
        """
        def to_records(names, ages):
            pass
        """,
        """
        def test_values():
            assert to_records(["Аня", "Боря"], [25, 30]) == [{"name": "Аня", "age": 25}, {"name": "Боря", "age": 30}] and to_records([], []) == [], "Неверный результат"
        """,
        """
        def to_records(names, ages):
            return [{"name": n, "age": a} for n, a in zip(names, ages)]
        """),
),

lesson(f"{P}-m1-l2", "Добавление, изменение, удаление",
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        d = {"name": "Аня"}
        d["age"] = 25
        d["name"] = "Анна"
        d.update({"city": "Казань", "age": 26})
        print(d)
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа?", """
        d = {"a": 1, "b": 2, "c": 3}
        del d["a"]
        x = d.pop("b")
        y = d.pop("z", "нет")
        print(x, y, d)
        """),
    out(f"{P}-m1-l2-e6", "Что выведет программа? popitem и clear.", """
        d = {"a": 1, "b": 2}
        k = d.popitem()
        print(k, d)
        d.clear()
        print(d, len(d))
        """, hint="popitem снимает последнюю добавленную пару."),
    cod(f"{P}-m1-l2-e3", t("""
        Напиши функцию `update_user(user, changes)` — применить изменения из словаря `changes` к словарю `user` **на месте** и вернуть `user`.

        ```
        u = {"name": "Аня", "age": 25}
        update_user(u, {"age": 26, "city": "Казань"})
        # → {"name": "Аня", "age": 26, "city": "Казань"}, и u изменился
        ```
        """),
        """
        def update_user(user, changes):
            pass
        """,
        """
        def test_update():
            u = {"name": "Аня", "age": 25}
            result = update_user(u, {"age": 26, "city": "Казань"})
            assert result == {"name": "Аня", "age": 26, "city": "Казань"} and u == result, "Словарь должен измениться на месте"
        """,
        """
        def update_user(user, changes):
            user.update(changes)
            return user
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `remove_secrets(data, keys)` — вернуть **новый** словарь без указанных ключей (например, `"password"`, `"token"`). Отсутствующие ключи не должны вызывать ошибку, исходный словарь не меняется.

        ```
        remove_secrets({"user": "a", "password": "x", "token": "y"}, ["password", "token", "api_key"])
        # → {"user": "a"}
        ```
        """),
        """
        def remove_secrets(data, keys):
            pass
        """,
        """
        def test_values():
            src = {"user": "a", "password": "x", "token": "y"}
            assert remove_secrets(src, ["password", "token", "api_key"]) == {"user": "a"}, "Секреты должны быть удалены"
            assert src == {"user": "a", "password": "x", "token": "y"}, "Исходный словарь не должен меняться"
        """,
        """
        def remove_secrets(data, keys):
            result = dict(data)
            for key in keys:
                result.pop(key, None)
            return result
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `rename_key(d, old, new)` — переименовать ключ **на месте**, сохранив значение. Если ключа `old` нет — ничего не делать. Вернуть словарь.

        ```
        rename_key({"userName": "Аня", "age": 25}, "userName", "user_name")
        # → {"age": 25, "user_name": "Аня"}
        ```
        """),
        """
        def rename_key(d, old, new):
            pass
        """,
        """
        def test_values():
            d = {"userName": "Аня", "age": 25}
            assert rename_key(d, "userName", "user_name") == {"age": 25, "user_name": "Аня"} and "userName" not in d, "Ключ не переименован"
            assert rename_key({"a": 1}, "x", "y") == {"a": 1}, "Нет ключа — без изменений"
        """,
        """
        def rename_key(d, old, new):
            if old in d:
                d[new] = d.pop(old)
            return d
        """),
    cod(f"{P}-m1-l2-e7", t("""
        Напиши функцию `add_if_missing(d, key, value)` — добавить пару, только если такого ключа ещё нет. Вернуть `True`, если добавили, иначе `False`. Существующее значение не менять.

        ```
        d = {"a": 1}
        add_if_missing(d, "a", 99)   # → False, d не изменился
        add_if_missing(d, "b", 2)    # → True, d == {"a": 1, "b": 2}
        ```
        """),
        """
        def add_if_missing(d, key, value):
            pass
        """,
        """
        def test_values():
            d = {"a": 1}
            assert add_if_missing(d, "a", 99) is False and d == {"a": 1}, "Существующий ключ не трогаем"
            assert add_if_missing(d, "b", 2) is True and d == {"a": 1, "b": 2}, "Новый ключ добавляем"
        """,
        """
        def add_if_missing(d, key, value):
            if key in d:
                return False
            d[key] = value
            return True
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши функцию `increment(d, key, by=1)` — увеличить значение по ключу на `by` **на месте** (если ключа нет — считать, что было 0) и вернуть новое значение.

        ```
        stats = {}
        increment(stats, "pass")      # → 1
        increment(stats, "pass", 5)   # → 6
        stats                         # → {"pass": 6}
        ```
        """),
        """
        def increment(d, key, by=1):
            pass
        """,
        """
        def test_values():
            stats = {}
            assert [increment(stats, "pass"), increment(stats, "pass", 5), increment(stats, "fail")] == [1, 6, 1], "Неверные значения"
            assert stats == {"pass": 6, "fail": 1}, f"stats = {stats}"
        """,
        """
        def increment(d, key, by=1):
            d[key] = d.get(key, 0) + by
            return d[key]
        """),
),

lesson(f"{P}-m1-l3", "get и значения по умолчанию",
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        cfg = {"browser": "chrome", "retries": 0, "proxy": None}
        print(cfg.get("browser"), cfg.get("timeout"), cfg.get("timeout", 30))
        print(cfg.get("retries", 3), cfg.get("proxy", "нет"))
        """, hint="Для существующего ключа get возвращает его значение, даже 0 или None."),
    out(f"{P}-m1-l3-e2", "Что выведет программа?", """
        groups = {}
        groups.setdefault("qa", []).append("Аня")
        groups.setdefault("qa", []).append("Боря")
        groups.setdefault("dev", []).append("Вика")
        print(groups)
        """),
    out(f"{P}-m1-l3-e6", "Что выведет программа? get против setdefault.", """
        d = {"a": 1}
        print(d.get("b"), "b" in d)
        print(d.setdefault("b", 5), d)
        print(d.setdefault("a", 100), d["a"])
        """, hint="get только читает; setdefault ещё и записывает, если ключа нет."),
    cod(f"{P}-m1-l3-e3", t("""
        Напиши функцию `get_timeout(config)` — вернуть `config["timeout"]`, а если ключа нет — `30`. Используй `get`.

        ```
        get_timeout({"timeout": 5})   # → 5
        get_timeout({})               # → 30
        get_timeout({"timeout": 0})   # → 0
        ```
        """),
        """
        def get_timeout(config):
            pass
        """,
        """
        def test_values():
            assert [get_timeout({"timeout": 5}), get_timeout({}), get_timeout({"timeout": 0})] == [5, 30, 0], "Неверный таймаут"
        """,
        """
        def get_timeout(config):
            return config.get("timeout", 30)
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `group_by_role(users)` — сгруппировать имена пользователей по ролям с помощью `setdefault`.

        `users` — список словарей `{"name": ..., "role": ...}`.

        ```
        group_by_role([{"name": "Аня", "role": "qa"}, {"name": "Боря", "role": "dev"}, {"name": "Вика", "role": "qa"}])
        # → {"qa": ["Аня", "Вика"], "dev": ["Боря"]}
        ```
        """),
        """
        def group_by_role(users):
            pass
        """,
        """
        def test_values():
            users = [{"name": "Аня", "role": "qa"}, {"name": "Боря", "role": "dev"}, {"name": "Вика", "role": "qa"}]
            assert group_by_role(users) == {"qa": ["Аня", "Вика"], "dev": ["Боря"]}, f"Получено {group_by_role(users)}"
            assert group_by_role([]) == {}, "Пусто — пусто"
        """,
        """
        def group_by_role(users):
            groups = {}
            for u in users:
                groups.setdefault(u["role"], []).append(u["name"])
            return groups
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `resolve(config, key, default)` — настройка с учётом ловушки `None`: если ключа нет **или** его значение `None` — вернуть `default`, иначе значение (в том числе `0`, `False`, `""`).

        ```
        cfg = {"retries": 0, "proxy": None, "debug": False}
        resolve(cfg, "retries", 3)     # → 0
        resolve(cfg, "proxy", "none")  # → "none"
        resolve(cfg, "debug", True)    # → False
        resolve(cfg, "timeout", 30)    # → 30
        ```
        """),
        """
        def resolve(config, key, default):
            pass
        """,
        """
        def test_values():
            cfg = {"retries": 0, "proxy": None, "debug": False}
            got = [resolve(cfg, "retries", 3), resolve(cfg, "proxy", "none"), resolve(cfg, "debug", True), resolve(cfg, "timeout", 30)]
            assert got == [0, "none", False, 30], f"Получено {got}"
        """,
        """
        def resolve(config, key, default):
            value = config.get(key)
            return default if value is None else value
        """),
    cod(f"{P}-m1-l3-e7", t("""
        Напиши функцию `lookup_all(d, keys, default)` — список значений для каждого ключа из `keys`; для отсутствующих — `default`.

        ```
        lookup_all({"a": 1, "b": 2}, ["a", "x", "b"], 0)   # → [1, 0, 2]
        ```
        """),
        """
        def lookup_all(d, keys, default):
            pass
        """,
        """
        def test_values():
            assert lookup_all({"a": 1, "b": 2}, ["a", "x", "b"], 0) == [1, 0, 2] and lookup_all({}, [], None) == [], "Неверный результат"
        """,
        """
        def lookup_all(d, keys, default):
            return [d.get(k, default) for k in keys]
        """),
    cod(f"{P}-m1-l3-e8", t("""
        Настройка может называться по-разному в разных версиях конфига. Напиши функцию `first_existing(d, keys)` — значение **первого** ключа из списка `keys`, который есть в словаре; если ни одного нет — `None`.

        ```
        first_existing({"base_url": "x", "url": "y"}, ["url", "base_url"])   # → "y"
        first_existing({"host": "h"}, ["url", "base_url"])                  # → None
        ```
        """),
        """
        def first_existing(d, keys):
            pass
        """,
        """
        def test_values():
            assert first_existing({"base_url": "x", "url": "y"}, ["url", "base_url"]) == "y", "Первый найденный — url"
            assert first_existing({"base_url": "x"}, ["url", "base_url"]) == "x" and first_existing({"host": "h"}, ["url"]) is None, "Неверный результат"
            assert first_existing({"url": None, "b": 1}, ["url", "b"]) is None, "Ключ есть — берём его значение, даже None"
        """,
        """
        def first_existing(d, keys):
            for k in keys:
                if k in d:
                    return d[k]
            return None
        """),
),

lesson(f"{P}-keys", "Ключи: какие бывают и как сравниваются",
    out(f"{P}-keys-e1", "Что выведет программа? 1, True и 1.0 — один ключ.", """
        d = {1: "int", "1": "str"}
        print(d[1], d["1"], len(d))
        d[True] = "bool"
        d[1.0] = "float"
        print(d)
        """, hint="1 == True == 1.0 и у них одинаковый хеш — для словаря это один ключ."),
    out(f"{P}-keys-e2", "Что выведет программа? Порядок и регистр.", """
        a = {"x": 1, "y": 2}
        b = {"y": 2, "x": 1}
        print(a == b, list(a) == list(b))
        print({"A": 1}.get("a"))
        """),
    out(f"{P}-keys-e3", "Что выведет программа?", """
        d = {}
        d[(1, 2)] = "кортеж"
        try:
            d[[1, 2]] = "список"
        except TypeError:
            print("список не может быть ключом")
        d[None] = "None тоже можно"
        print(len(d), d[None])
        """),
    cod(f"{P}-keys-e4", t("""
        Напиши функцию `lower_keys(d)` — новый словарь с ключами в нижнем регистре. Если после приведения ключи совпали, побеждает значение, встреченное **позже**.

        ```
        lower_keys({"Host": "a", "PORT": 1, "host": "b"})   # → {"host": "b", "port": 1}
        ```
        """),
        """
        def lower_keys(d):
            pass
        """,
        """
        def test_values():
            assert lower_keys({"Host": "a", "PORT": 1, "host": "b"}) == {"host": "b", "port": 1} and lower_keys({}) == {}, "Неверный результат"
        """,
        """
        def lower_keys(d):
            result = {}
            for key, value in d.items():
                result[key.lower()] = value
            return result
        """),
    cod(f"{P}-keys-e5", t("""
        Заголовки HTTP не чувствительны к регистру. Напиши функцию `get_header(headers, name)` — значение заголовка без учёта регистра имени или `None`.

        ```
        get_header({"Content-Type": "json"}, "content-type")   # → "json"
        get_header({"X-Id": "1"}, "Authorization")             # → None
        ```
        """),
        """
        def get_header(headers, name):
            pass
        """,
        """
        def test_values():
            assert get_header({"Content-Type": "json"}, "content-type") == "json" and get_header({"X-Id": "1"}, "Authorization") is None, "Неверный результат"
            assert get_header({"x-token": "t"}, "X-TOKEN") == "t", "Регистр не важен с обеих сторон"
        """,
        """
        def get_header(headers, name):
            for key, value in headers.items():
                if key.lower() == name.lower():
                    return value
            return None
        """),
    cod(f"{P}-keys-e6", t("""
        В JSON ключи всегда строки. Напиши функцию `str_keys(d)` — новый словарь, где все ключи превращены в строки через `str`.

        ```
        str_keys({1: "a", "b": 2, (1, 2): "c"})   # → {"1": "a", "b": 2, "(1, 2)": "c"}
        ```
        """),
        """
        def str_keys(d):
            pass
        """,
        """
        def test_values():
            assert str_keys({1: "a", "b": 2, (1, 2): "c"}) == {"1": "a", "b": 2, "(1, 2)": "c"}, f"Получено {str_keys({1: 'a', 'b': 2, (1, 2): 'c'})}"
        """,
        """
        def str_keys(d):
            return {str(k): v for k, v in d.items()}
        """),
    cod(f"{P}-keys-e7", t("""
        Напиши функцию `same_ignoring_none(a, b)` — равны ли два словаря, если не считать пар со значением `None` (такое поле как будто отсутствует). Порядок ключей не важен.

        ```
        same_ignoring_none({"a": 1, "b": None}, {"a": 1})   # → True
        same_ignoring_none({"a": 1}, {"a": 2})              # → False
        ```
        """),
        """
        def same_ignoring_none(a, b):
            pass
        """,
        """
        def test_values():
            got = [same_ignoring_none({"a": 1, "b": None}, {"a": 1}), same_ignoring_none({"a": 1}, {"a": 2}), same_ignoring_none({"x": 0}, {"x": 0, "y": None}), same_ignoring_none({"x": 0}, {})]
            assert got == [True, False, True, False], f"Получено {got}"
        """,
        """
        def same_ignoring_none(a, b):
            clean_a = {k: v for k, v in a.items() if v is not None}
            clean_b = {k: v for k, v in b.items() if v is not None}
            return clean_a == clean_b
        """),
    cod(f"{P}-keys-e8", t("""
        Напиши функцию `key_types(d)` — отсортированный список **различных** имён типов ключей словаря (`type(k).__name__`).

        ```
        key_types({1: "a", "b": 2, (1, 2): 3, "c": 4})   # → ["int", "str", "tuple"]
        ```
        """),
        """
        def key_types(d):
            pass
        """,
        """
        def test_values():
            assert key_types({1: "a", "b": 2, (1, 2): 3, "c": 4}) == ["int", "str", "tuple"] and key_types({}) == [], "Неверный результат"
        """,
        """
        def key_types(d):
            names = []
            for k in d:
                name = type(k).__name__
                if name not in names:
                    names.append(name)
            return sorted(names)
        """),
),
)
