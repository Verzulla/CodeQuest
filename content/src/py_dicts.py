"""Тема «Словари»."""
from ._lib import cod, lesson, module, out, t, topic

P = "dct"

# ============================================================
m1 = module(f"{P}-m1", "Основы словарей", "📖", "Создание, доступ, изменение и get",

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
        """)),

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
        """)),

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
        """)),
)

# ============================================================
m2 = module(f"{P}-m2", "Перебор и обработка", "🔄", "keys/values/items, подсчёт, группировка и сортировка",

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
        """)),

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
        """)),

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
        """)),
)

# ============================================================
m3 = module(f"{P}-m3", "Словари в реальных задачах", "🗂️", "Вложенные словари, слияние, копирование и включения",

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
        """, xp=25)),

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
        """, xp=25)),

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
        """, xp=20)),
)

TOPIC = topic("py-dicts", "Словари", "📖", "#ffc800",
              "Ключи и значения, get, перебор, подсчёт, группировка, вложенность и слияние",
              m1, m2, m3, group="Python")
