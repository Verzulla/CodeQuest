"""Тема «Словари», модуль 3 «Словари в реальных задачах» — задания. Теория — в _dct_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "dct"

m3 = module(f"{P}-m3", "Словари в реальных задачах", "🗂️", "Вложенность, слияние и копии, включения, сравнение словарей, проверки API",

lesson(f"{P}-m3-l1", "Вложенные словари",
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        resp = {"status": 200, "data": {"user": {"name": "Аня", "roles": ["qa", "admin"]}}}
        user = resp["data"]["user"]
        print(user["name"], user["roles"][-1])
        print(resp.get("meta", {}).get("page", 1))
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа?", """
        config = {"env": {"staging": {"url": "https://stg"}, "prod": {"url": "https://prod"}}}
        for name, settings in config["env"].items():
            print(name, settings["url"])
        config["env"]["dev"] = {"url": "http://localhost"}
        print(len(config["env"]))
        """),
    out(f"{P}-m3-l1-e6", "Что выведет программа?", """
        users = {"anna": {"age": 25, "skills": ["qa"]}}
        users["anna"]["skills"].append("sql")
        users["bob"] = {"age": 30, "skills": []}
        print(users["anna"], len(users))
        print([name for name, info in users.items() if info["age"] > 26])
        """),
    cod(f"{P}-m3-l1-e3", t("""
        Напиши функцию `user_city(resp)` — город пользователя из ответа вида `{"data": {"user": {"address": {"city": ...}}}}`. Если на любом уровне ключа нет — `None`. Используй цепочку `get` с `{}` по умолчанию.

        ```
        user_city({"data": {"user": {"address": {"city": "Казань"}}}})   # → "Казань"
        user_city({"data": {"user": {}}})                               # → None
        ```
        """),
        """
        def user_city(resp):
            pass
        """,
        """
        def test_values():
            assert user_city({"data": {"user": {"address": {"city": "Казань"}}}}) == "Казань", "Нужен город"
            assert user_city({"data": {"user": {}}}) is None and user_city({}) is None, "Нет ключа — None"
        """,
        """
        def user_city(resp):
            return resp.get("data", {}).get("user", {}).get("address", {}).get("city")
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `set_nested(d, path, value)` — установить значение по пути ключей, **создавая** промежуточные словари при необходимости. Изменить `d` на месте и вернуть его.

        ```
        d = {}
        set_nested(d, ["a", "b", "c"], 1)   # → {"a": {"b": {"c": 1}}}
        set_nested(d, ["a", "x"], 2)        # → {"a": {"b": {"c": 1}, "x": 2}}
        ```
        """),
        """
        def set_nested(d, path, value):
            pass
        """,
        """
        def test_values():
            d = {}
            assert set_nested(d, ["a", "b", "c"], 1) == {"a": {"b": {"c": 1}}}, "Неверная вложенность"
            assert set_nested(d, ["a", "x"], 2) == {"a": {"b": {"c": 1}, "x": 2}}, "Существующие ветки должны сохраняться"
        """,
        """
        def set_nested(d, path, value):
            current = d
            for key in path[:-1]:
                current = current.setdefault(key, {})
            current[path[-1]] = value
            return d
        """, xp=20),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `flatten_dict(d, prefix="")` — «расплющить» вложенный словарь в плоский с ключами через точку.

        ```
        flatten_dict({"a": 1, "b": {"c": 2, "d": {"e": 3}}})
        # → {"a": 1, "b.c": 2, "b.d.e": 3}
        ```
        Используй рекурсию.
        """),
        """
        def flatten_dict(d, prefix=""):
            pass
        """,
        """
        def test_values():
            assert flatten_dict({"a": 1, "b": {"c": 2, "d": {"e": 3}}}) == {"a": 1, "b.c": 2, "b.d.e": 3}, f"Получено {flatten_dict({'a': 1, 'b': {'c': 2, 'd': {'e': 3}}})}"
            assert flatten_dict({}) == {}, "Пусто — пусто"
        """,
        """
        def flatten_dict(d, prefix=""):
            flat = {}
            for key, value in d.items():
                full = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    flat.update(flatten_dict(value, full))
                else:
                    flat[full] = value
            return flat
        """, xp=25),
    cod(f"{P}-m3-l1-e7", t("""
        Напиши функцию `get_path(d, path, default=None)` — значение во вложенном словаре по списку ключей. Если на каком-то уровне ключа нет (или значение не словарь) — вернуть `default`.

        ```
        cfg = {"db": {"main": {"host": "localhost"}}}
        get_path(cfg, ["db", "main", "host"])        # → "localhost"
        get_path(cfg, ["db", "replica", "host"], "-")  # → "-"
        ```
        """),
        """
        def get_path(d, path, default=None):
            pass
        """,
        """
        def test_values():
            cfg = {"db": {"main": {"host": "localhost"}}, "x": 1}
            assert get_path(cfg, ["db", "main", "host"]) == "localhost", "Нужен host"
            assert get_path(cfg, ["db", "replica", "host"], "-") == "-" and get_path(cfg, ["x", "y"]) is None, "Нет пути — default"
            assert get_path(cfg, []) == cfg, "Пустой путь — сам словарь"
        """,
        """
        def get_path(d, path, default=None):
            current = d
            for key in path:
                if not isinstance(current, dict) or key not in current:
                    return default
                current = current[key]
            return current
        """, xp=20),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `count_leaves(d)` — сколько во вложенном словаре конечных значений (всё, что не словарь). Используй рекурсию.

        ```
        count_leaves({"a": 1, "b": {"c": 2, "d": {"e": 3, "f": 4}}})   # → 4
        ```
        """),
        """
        def count_leaves(d):
            pass
        """,
        """
        def test_values():
            assert count_leaves({"a": 1, "b": {"c": 2, "d": {"e": 3, "f": 4}}}) == 4 and count_leaves({}) == 0 and count_leaves({"a": {}}) == 0, "Неверный подсчёт"
        """,
        """
        def count_leaves(d):
            total = 0
            for value in d.values():
                if isinstance(value, dict):
                    total += count_leaves(value)
                else:
                    total += 1
            return total
        """),
),

lesson(f"{P}-m3-l2", "Слияние и копирование",
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        defaults = {"timeout": 30, "browser": "chrome", "headless": True}
        overrides = {"browser": "firefox", "retries": 2}
        print({**defaults, **overrides})
        print(defaults | overrides == {**defaults, **overrides})
        print(defaults)
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа? Мелкая копия.", """
        import copy
        original = {"name": "Аня", "tags": ["qa"]}
        shallow = original.copy()
        deep = copy.deepcopy(original)
        shallow["tags"].append("admin")
        shallow["name"] = "Боря"
        print(original)
        print(deep)
        """, hint="copy() копирует только верхний уровень; список tags общий."),
    out(f"{P}-m3-l2-e6", "Что выведет программа? Второе имя против копии.", """
        a = {"x": 1}
        b = a
        c = dict(a)
        b["y"] = 2
        print(a, c, a is b, a is c)
        """),
    cod(f"{P}-m3-l2-e3", t("""
        Напиши функцию `build_config(overrides)` — объединить настройки по умолчанию `DEFAULTS = {"timeout": 30, "browser": "chrome", "headless": True}` с переданными `overrides` (они важнее) и вернуть **новый** словарь. `DEFAULTS` не должен меняться.

        ```
        build_config({"browser": "firefox"})   # → {"timeout": 30, "browser": "firefox", "headless": True}
        ```
        """),
        """
        DEFAULTS = {"timeout": 30, "browser": "chrome", "headless": True}

        def build_config(overrides):
            pass
        """,
        """
        def test_values():
            assert build_config({"browser": "firefox"}) == {"timeout": 30, "browser": "firefox", "headless": True}, "Неверный конфиг"
            build_config({"timeout": 5})
            assert DEFAULTS == {"timeout": 30, "browser": "chrome", "headless": True}, "DEFAULTS изменился"
        """,
        """
        DEFAULTS = {"timeout": 30, "browser": "chrome", "headless": True}

        def build_config(overrides):
            return {**DEFAULTS, **overrides}
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Функция `make_test_user(base)` должна вернуть **независимую** копию шаблона пользователя с добавленным тегом `"temp"` в список `tags`. Сейчас она портит шаблон, потому что делает мелкую копию.

        Исправь с помощью `copy.deepcopy`.

        ```
        TEMPLATE = {"name": "test", "tags": ["auto"]}
        make_test_user(TEMPLATE)   # → {"name": "test", "tags": ["auto", "temp"]}
        TEMPLATE                   # → {"name": "test", "tags": ["auto"]}   без изменений
        ```
        """),
        """
        def make_test_user(base):
            user = base.copy()
            user["tags"].append("temp")
            return user
        """,
        """
        def test_independent():
            template = {"name": "test", "tags": ["auto"]}
            user = make_test_user(template)
            assert user == {"name": "test", "tags": ["auto", "temp"]}, f"Получено {user}"
            assert template == {"name": "test", "tags": ["auto"]}, "Шаблон испорчен — нужна глубокая копия"
        """,
        """
        import copy

        def make_test_user(base):
            user = copy.deepcopy(base)
            user["tags"].append("temp")
            return user
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `deep_merge(base, override)` — рекурсивное слияние: если по ключу в обоих словарях лежат словари — слить их рекурсивно; иначе значение из `override` побеждает. Вернуть **новый** словарь, исходные не менять.

        ```
        deep_merge({"db": {"host": "localhost", "port": 5432}, "debug": False},
                   {"db": {"host": "stg-db"}, "debug": True})
        # → {"db": {"host": "stg-db", "port": 5432}, "debug": True}
        ```
        """),
        """
        def deep_merge(base, override):
            pass
        """,
        """
        def test_values():
            base = {"db": {"host": "localhost", "port": 5432}, "debug": False}
            over = {"db": {"host": "stg-db"}, "debug": True}
            assert deep_merge(base, over) == {"db": {"host": "stg-db", "port": 5432}, "debug": True}, f"Получено {deep_merge(base, over)}"
            assert base == {"db": {"host": "localhost", "port": 5432}, "debug": False}, "base изменился"
        """,
        """
        def deep_merge(base, override):
            result = dict(base)
            for key, value in override.items():
                if isinstance(result.get(key), dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result
        """, xp=25),
    cod(f"{P}-m3-l2-e7", t("""
        Напиши функцию `merge_all(dicts)` — слить список словарей слева направо в **новый** словарь (более поздние важнее). Исходные не менять.

        ```
        merge_all([{"a": 1}, {"b": 2}, {"a": 3}])   # → {"a": 3, "b": 2}
        ```
        """),
        """
        def merge_all(dicts):
            pass
        """,
        """
        def test_values():
            src = [{"a": 1}, {"b": 2}, {"a": 3}]
            assert merge_all(src) == {"a": 3, "b": 2} and src[0] == {"a": 1} and merge_all([]) == {}, "Неверный результат"
        """,
        """
        def merge_all(dicts):
            result = {}
            for d in dicts:
                result.update(d)
            return result
        """),
    cod(f"{P}-m3-l2-e8", t("""
        Напиши функцию `with_key(d, key, value)` — новый словарь: всё из `d` плюс пара `key: value` (перезаписывает существующую). Исходный не менять. Используй `{**d, ...}`.

        ```
        with_key({"a": 1}, "b", 2)   # → {"a": 1, "b": 2}
        ```
        """),
        """
        def with_key(d, key, value):
            pass
        """,
        """
        def test_values():
            src = {"a": 1}
            assert with_key(src, "b", 2) == {"a": 1, "b": 2} and with_key(src, "a", 5) == {"a": 5} and src == {"a": 1}, "Неверный результат"
        """,
        """
        def with_key(d, key, value):
            return {**d, key: value}
        """),
),

lesson(f"{P}-m3-l3", "Словарные включения",
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        names = ["api", "ui", "docker"]
        print({n: len(n) for n in names})
        prices = {"чай": 300, "кофе": 500, "сок": 150}
        print({k: v for k, v in prices.items() if v >= 300})
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа?", """
        codes = {"OK": 200, "Created": 201, "Not Found": 404}
        by_code = {code: text for text, code in codes.items()}
        print(by_code[404])
        print({k.lower(): v for k, v in codes.items()})
        """),
    out(f"{P}-m3-l3-e6", "Что выведет программа?", """
        nums = [1, 2, 3, 4]
        print({n: n * n for n in nums if n % 2 == 0})
        print({x: ("чёт" if x % 2 == 0 else "нечет") for x in range(3)})
        """),
    cod(f"{P}-m3-l3-e3", t("""
        Напиши функцию `drop_none(d)` — новый словарь без пар, у которых значение `None`. Используй словарное включение.

        ```
        drop_none({"a": 1, "b": None, "c": 0, "d": ""})   # → {"a": 1, "c": 0, "d": ""}
        ```
        """),
        """
        def drop_none(d):
            pass
        """,
        """
        def test_values():
            assert drop_none({"a": 1, "b": None, "c": 0, "d": ""}) == {"a": 1, "c": 0, "d": ""}, "Удалить только None (0 и пустая строка остаются)"
        """,
        """
        def drop_none(d):
            return {k: v for k, v in d.items() if v is not None}
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `index_by_id(users)` — словарь `{id: пользователь}` из списка словарей-пользователей. Так поиск по id становится мгновенным.

        ```
        index_by_id([{"id": 1, "name": "Аня"}, {"id": 2, "name": "Боря"}])
        # → {1: {"id": 1, "name": "Аня"}, 2: {"id": 2, "name": "Боря"}}
        ```
        """),
        """
        def index_by_id(users):
            pass
        """,
        """
        def test_values():
            users = [{"id": 1, "name": "Аня"}, {"id": 2, "name": "Боря"}]
            assert index_by_id(users) == {1: users[0], 2: users[1]} and index_by_id([]) == {}, "Неверный индекс"
        """,
        """
        def index_by_id(users):
            return {u["id"]: u for u in users}
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `normalize_keys(d)` — вернуть новый словарь с ключами в стиле `snake_case`: ключи из `camelCase` превратить так, чтобы перед каждой заглавной буквой стояло `_`, а всё было в нижнем регистре.

        ```
        normalize_keys({"userName": "Аня", "createdAt": "2024", "id": 1})
        # → {"user_name": "Аня", "created_at": "2024", "id": 1}
        ```
        Сначала напиши вспомогательную функцию для одного ключа, затем словарное включение.
        """),
        """
        def normalize_keys(d):
            pass
        """,
        """
        def test_values():
            got = normalize_keys({"userName": "Аня", "createdAt": "2024", "id": 1, "HTTPCode": 200})
            assert got == {"user_name": "Аня", "created_at": "2024", "id": 1, "_h_t_t_p_code": 200}, f"Получено {got}"
        """,
        """
        def to_snake(key):
            return "".join("_" + ch.lower() if ch.isupper() else ch for ch in key)

        def normalize_keys(d):
            return {to_snake(k): v for k, v in d.items()}
        """, xp=20),
    cod(f"{P}-m3-l3-e7", t("""
        Напиши функцию `squares_dict(n)` — словарь `{i: i²}` для `i` от 1 до `n` включительно. Словарное включение.

        ```
        squares_dict(3)   # → {1: 1, 2: 4, 3: 9}
        ```
        """),
        """
        def squares_dict(n):
            pass
        """,
        """
        def test_values():
            assert squares_dict(3) == {1: 1, 2: 4, 3: 9} and squares_dict(0) == {}, "Неверный словарь"
        """,
        """
        def squares_dict(n):
            return {i: i * i for i in range(1, n + 1)}
        """),
    cod(f"{P}-m3-l3-e8", t("""
        Напиши функцию `filter_keys(d, allowed)` — новый словарь только с ключами из списка `allowed`.

        ```
        filter_keys({"id": 1, "name": "Аня", "password": "x"}, ["id", "name"])   # → {"id": 1, "name": "Аня"}
        ```
        """),
        """
        def filter_keys(d, allowed):
            pass
        """,
        """
        def test_values():
            assert filter_keys({"id": 1, "name": "Аня", "password": "x"}, ["id", "name"]) == {"id": 1, "name": "Аня"} and filter_keys({"a": 1}, []) == {}, "Неверный результат"
        """,
        """
        def filter_keys(d, allowed):
            return {k: v for k, v in d.items() if k in allowed}
        """),
),

lesson(f"{P}-views", "Сравнение словарей: ключи как множества",
    out(f"{P}-views-e1", "Что выведет программа?", """
        a = {"x": 1, "y": 2, "z": 3}
        b = {"y": 20, "z": 3, "w": 4}
        print(sorted(a.keys() & b.keys()))
        print(sorted(a.keys() - b.keys()), sorted(a.keys() | b.keys()))
        """),
    out(f"{P}-views-e2", "Что выведет программа? Совпадающие пары.", """
        a = {"x": 1, "y": 2}
        b = {"x": 1, "y": 3}
        changed = [k for k in a if k in b and a[k] != b[k]]
        print(changed, a.items() & b.items())
        """),
    out(f"{P}-views-e3", "Что выведет программа?", """
        d = {"a": 1}
        keys = d.keys()
        print(type(keys).__name__, "a" in keys)
        d["b"] = 2
        print(len(keys))
        """, hint="keys() — «живое» представление, а не копия."),
    cod(f"{P}-views-e4", t("""
        Напиши функцию `missing_keys(expected, actual)` — отсортированный список ключей, которые есть в `expected`, но отсутствуют в `actual`.

        ```
        missing_keys({"id": 1, "name": "a", "email": "b"}, {"id": 1})   # → ["email", "name"]
        ```
        """),
        """
        def missing_keys(expected, actual):
            pass
        """,
        """
        def test_values():
            assert missing_keys({"id": 1, "name": "a", "email": "b"}, {"id": 1}) == ["email", "name"] and missing_keys({}, {"x": 1}) == [], "Неверный результат"
        """,
        """
        def missing_keys(expected, actual):
            return sorted(expected.keys() - actual.keys())
        """),
    cod(f"{P}-views-e5", t("""
        Напиши функцию `extra_keys(expected, actual)` — отсортированный список «лишних» ключей: есть в `actual`, но нет в `expected`.

        ```
        extra_keys({"id": 1}, {"id": 1, "debug": True, "trace": "x"})   # → ["debug", "trace"]
        ```
        """),
        """
        def extra_keys(expected, actual):
            pass
        """,
        """
        def test_values():
            assert extra_keys({"id": 1}, {"id": 1, "debug": True, "trace": "x"}) == ["debug", "trace"] and extra_keys({"a": 1}, {"a": 2}) == [], "Неверный результат"
        """,
        """
        def extra_keys(expected, actual):
            return sorted(actual.keys() - expected.keys())
        """),
    cod(f"{P}-views-e6", t("""
        Напиши функцию `changed_values(before, after)` — словарь `{ключ: (старое, новое)}` для ключей, которые есть в **обоих** словарях, но значения отличаются.

        ```
        changed_values({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 5, "d": 4})   # → {"b": (2, 5)}
        ```
        """),
        """
        def changed_values(before, after):
            pass
        """,
        """
        def test_values():
            assert changed_values({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 5, "d": 4}) == {"b": (2, 5)} and changed_values({}, {}) == {}, "Неверный результат"
        """,
        """
        def changed_values(before, after):
            return {k: (before[k], after[k]) for k in before.keys() & after.keys() if before[k] != after[k]}
        """),
    cod(f"{P}-views-e7", t("""
        Напиши функцию `dict_diff(before, after)` — отчёт об изменениях: словарь с тремя отсортированными списками ключей: `"added"` (появились), `"removed"` (исчезли), `"changed"` (есть в обоих, значения разные).

        ```
        dict_diff({"a": 1, "b": 2}, {"b": 3, "c": 4})
        # → {"added": ["c"], "removed": ["a"], "changed": ["b"]}
        ```
        """),
        """
        def dict_diff(before, after):
            pass
        """,
        """
        def test_values():
            got = dict_diff({"a": 1, "b": 2}, {"b": 3, "c": 4})
            assert got == {"added": ["c"], "removed": ["a"], "changed": ["b"]}, f"Получено {got}"
            assert dict_diff({"x": 1}, {"x": 1}) == {"added": [], "removed": [], "changed": []}, "Без изменений — пустые списки"
        """,
        """
        def dict_diff(before, after):
            common = before.keys() & after.keys()
            return {
                "added": sorted(after.keys() - before.keys()),
                "removed": sorted(before.keys() - after.keys()),
                "changed": sorted(k for k in common if before[k] != after[k]),
            }
        """, xp=20),
    cod(f"{P}-views-e8", t("""
        Напиши функцию `common_items(a, b)` — словарь из пар, которые **совпадают** в обоих словарях (и ключ, и значение). Используй `a.items() & b.items()`.

        ```
        common_items({"x": 1, "y": 2}, {"x": 1, "y": 3})   # → {"x": 1}
        ```
        """),
        """
        def common_items(a, b):
            pass
        """,
        """
        def test_values():
            assert common_items({"x": 1, "y": 2}, {"x": 1, "y": 3}) == {"x": 1} and common_items({}, {"a": 1}) == {}, "Неверный результат"
        """,
        """
        def common_items(a, b):
            return dict(a.items() & b.items())
        """),
),

lesson(f"{P}-api", "Словари в проверках API",
    out(f"{P}-api-e1", "Что выведет программа?", """
        resp = {"status": 200, "body": {"id": 7, "name": "Аня", "email": None}}
        body = resp["body"]
        print(resp["status"] == 200, set(body) == {"id", "name", "email"})
        print([k for k, v in body.items() if v is None])
        """),
    out(f"{P}-api-e2", "Что выведет программа? Проверка типов по схеме.", """
        schema = {"id": int, "name": str}
        body = {"id": "7", "name": "Аня"}
        for field, typ in schema.items():
            print(field, isinstance(body[field], typ))
        """),
    out(f"{P}-api-e3", "Что выведет программа? Ожидаемое — подмножество ответа.", """
        expected = {"status": "ok", "code": 200}
        actual = {"status": "ok", "code": 200, "trace_id": "abc"}
        print(expected.items() <= actual.items())
        print(all(actual.get(k) == v for k, v in expected.items()))
        """),
    cod(f"{P}-api-e4", t("""
        Напиши функцию `check_schema(body, schema)` — проверить тело ответа по схеме `{поле: тип}`. Вернуть список ошибок в порядке полей схемы:

        - поля нет → `"нет поля <поле>"`;
        - тип не тот → `"поле <поле>: ожидали <имя типа>"`.

        ```
        check_schema({"id": "7"}, {"id": int, "name": str})
        # → ["поле id: ожидали int", "нет поля name"]
        ```
        """),
        """
        def check_schema(body, schema):
            pass
        """,
        """
        def test_values():
            assert check_schema({"id": "7"}, {"id": int, "name": str}) == ["поле id: ожидали int", "нет поля name"], "Неверные ошибки"
            assert check_schema({"id": 1, "name": "a"}, {"id": int, "name": str}) == [], "Всё верно — пусто"
        """,
        """
        def check_schema(body, schema):
            errors = []
            for field, typ in schema.items():
                if field not in body:
                    errors.append(f"нет поля {field}")
                elif not isinstance(body[field], typ):
                    errors.append(f"поле {field}: ожидали {typ.__name__}")
            return errors
        """, hint="typ.__name__ — имя типа строкой: int → 'int'.", xp=20),
    cod(f"{P}-api-e5", t("""
        Напиши функцию `contains_subset(actual, expected)` — содержит ли ответ `actual` все пары из `expected` (лишние поля в ответе допустимы).

        ```
        contains_subset({"status": "ok", "id": 5, "ts": 1}, {"status": "ok", "id": 5})   # → True
        contains_subset({"status": "ok"}, {"status": "error"})                             # → False
        ```
        """),
        """
        def contains_subset(actual, expected):
            pass
        """,
        """
        def test_values():
            assert contains_subset({"status": "ok", "id": 5, "ts": 1}, {"status": "ok", "id": 5}) is True, "Подмножество"
            assert contains_subset({"status": "ok"}, {"status": "error"}) is False and contains_subset({}, {"a": None}) is False, "Не подмножество"
        """,
        """
        def contains_subset(actual, expected):
            for key, value in expected.items():
                if key not in actual or actual[key] != value:
                    return False
            return True
        """, hint="Отсутствующий ключ и ключ со значением None — разные вещи: проверяй key in actual."),
    cod(f"{P}-api-e6", t("""
        Напиши функцию `mask_secrets(d)` — новый словарь для логов: значения ключей, в названии которых есть `token` или `password` (в любом регистре), заменить на `"***"`.

        ```
        mask_secrets({"user": "a", "Password": "x", "access_token": "y"})
        # → {"user": "a", "Password": "***", "access_token": "***"}
        ```
        """),
        """
        def mask_secrets(d):
            pass
        """,
        """
        def test_values():
            src = {"user": "a", "Password": "x", "access_token": "y"}
            assert mask_secrets(src) == {"user": "a", "Password": "***", "access_token": "***"} and src["Password"] == "x", "Неверный результат или исходный изменён"
        """,
        """
        def mask_secrets(d):
            result = {}
            for key, value in d.items():
                lowered = key.lower()
                if "token" in lowered or "password" in lowered:
                    result[key] = "***"
                else:
                    result[key] = value
            return result
        """),
    cod(f"{P}-api-e7", t("""
        Напиши функцию `pick(d, keys)` — новый словарь только с перечисленными ключами, которые реально есть в `d` (порядок — как в `keys`).

        ```
        pick({"id": 1, "name": "Аня", "age": 25}, ["name", "id", "email"])   # → {"name": "Аня", "id": 1}
        ```
        """),
        """
        def pick(d, keys):
            pass
        """,
        """
        def test_values():
            got = pick({"id": 1, "name": "Аня", "age": 25}, ["name", "id", "email"])
            assert got == {"name": "Аня", "id": 1} and list(got) == ["name", "id"], f"Получено {got}"
        """,
        """
        def pick(d, keys):
            return {k: d[k] for k in keys if k in d}
        """),
    cod(f"{P}-api-e8", t("""
        Напиши функцию `compare_responses(expected, actual, ignore)` — отсортированный список ключей, по которым ответы **различаются**. Учитывай ключи из обоих словарей (отсутствующий ключ — тоже различие), а ключи из списка `ignore` (например, `"timestamp"`) пропускай.

        ```
        compare_responses({"id": 1, "ts": 100, "a": 1}, {"id": 1, "ts": 200, "b": 2}, ["ts"])
        # → ["a", "b"]
        ```
        """),
        """
        def compare_responses(expected, actual, ignore):
            pass
        """,
        """
        def test_values():
            assert compare_responses({"id": 1, "ts": 100, "a": 1}, {"id": 1, "ts": 200, "b": 2}, ["ts"]) == ["a", "b"], "Неверный результат"
            assert compare_responses({"x": 1}, {"x": 2}, []) == ["x"] and compare_responses({"x": None}, {}, []) == ["x"], "Отсутствие ключа — различие"
        """,
        """
        def compare_responses(expected, actual, ignore):
            diffs = []
            for key in expected.keys() | actual.keys():
                if key in ignore:
                    continue
                if key not in expected or key not in actual or expected[key] != actual[key]:
                    diffs.append(key)
            return sorted(diffs)
        """, xp=20),
),
)
