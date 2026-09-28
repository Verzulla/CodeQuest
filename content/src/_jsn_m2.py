"""Тема «JSON», модуль 2 «Работа с данными» — задания. Теория — в _jsn_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "jsn"

m2 = module(f"{P}-m2", "Работа с данными", "🗃️", "Вложенный JSON, списки объектов, сборка и изменение, файлы",

lesson(f"{P}-m2-l1", "Навигация по вложенному JSON",
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        import json
        resp = json.loads('{"data": {"users": [{"id": 1, "name": "Аня"}, {"id": 2, "name": "Боря"}]}, "total": 2}')
        users = resp["data"]["users"]
        print(len(users), users[1]["name"], resp["total"])
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа? null и отсутствующие ключи.", """
        import json
        resp = json.loads('{"data": {"user": {"address": null}}}')
        address = resp["data"]["user"]["address"] or {}
        print(address.get("city", "нет города"))
        print(resp.get("meta", {}).get("page"))
        """),
    out(f"{P}-m2-l1-e3", "Что выведет программа?", """
        import json
        order = json.loads('{"items": [{"sku": "A", "qty": 2}, {"sku": "B", "qty": 1}]}')
        for i, item in enumerate(order["items"], start=1):
            print(i, item["sku"], item["qty"])
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `first_user_name(text)` — имя первого пользователя из ответа вида `{"data": {"users": [...]}}`. Если список пуст — `None`.

        ```
        first_user_name('{"data": {"users": [{"name": "Аня"}]}}')   # → "Аня"
        first_user_name('{"data": {"users": []}}')                  # → None
        ```
        """),
        """
        import json

        def first_user_name(text):
            pass
        """,
        """
        def test_values():
            assert first_user_name('{"data": {"users": [{"name": "Аня"}, {"name": "Б"}]}}') == "Аня" and first_user_name('{"data": {"users": []}}') is None, "Неверный результат"
        """,
        """
        import json

        def first_user_name(text):
            users = json.loads(text)["data"]["users"]
            if not users:
                return None
            return users[0]["name"]
        """),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `get_in(data, path, default=None)` — значение во вложенной структуре по пути: путь — список ключей (строки для объектов) и индексов (числа для массивов). Если на каком-то шаге ключа/индекса нет — `default`.

        ```
        data = {"users": [{"name": "Аня"}, {"name": "Боря"}]}
        get_in(data, ["users", 1, "name"])        # → "Боря"
        get_in(data, ["users", 5, "name"], "-")   # → "-"
        ```
        """),
        """
        def get_in(data, path, default=None):
            pass
        """,
        """
        def test_values():
            data = {"users": [{"name": "Аня"}, {"name": "Боря"}], "x": None}
            assert get_in(data, ["users", 1, "name"]) == "Боря" and get_in(data, ["users", 5, "name"], "-") == "-", "Неверный путь"
            assert get_in(data, ["nope"]) is None and get_in(data, ["x", "y"], 0) == 0 and get_in(data, []) == data, "Неверный результат"
        """,
        """
        def get_in(data, path, default=None):
            current = data
            for key in path:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                elif isinstance(current, list) and isinstance(key, int) and -len(current) <= key < len(current):
                    current = current[key]
                else:
                    return default
            return current
        """, xp=25),
    cod(f"{P}-m2-l1-e6", t("""
        Напиши функцию `user_emails(text)` — список email-ов из `{"data": {"users": [...]}}`; пользователей без поля `"email"` (или с `null`) пропускать.

        ```
        user_emails('{"data": {"users": [{"email": "a@x"}, {"name": "b"}, {"email": null}]}}')   # → ["a@x"]
        ```
        """),
        """
        import json

        def user_emails(text):
            pass
        """,
        """
        def test_values():
            assert user_emails('{"data": {"users": [{"email": "a@x"}, {"name": "b"}, {"email": null}]}}') == ["a@x"], "Неверный список"
        """,
        """
        import json

        def user_emails(text):
            users = json.loads(text)["data"]["users"]
            return [u["email"] for u in users if u.get("email") is not None]
        """),
    cod(f"{P}-m2-l1-e7", t("""
        Напиши функцию `total_qty(text)` — общее количество товаров в заказе `{"items": [{"sku": ..., "qty": ...}, ...]}`.

        ```
        total_qty('{"items": [{"sku": "A", "qty": 2}, {"sku": "B", "qty": 1}]}')   # → 3
        ```
        """),
        """
        import json

        def total_qty(text):
            pass
        """,
        """
        def test_values():
            assert total_qty('{"items": [{"sku": "A", "qty": 2}, {"sku": "B", "qty": 1}]}') == 3 and total_qty('{"items": []}') == 0, "Неверная сумма"
        """,
        """
        import json

        def total_qty(text):
            return sum(item["qty"] for item in json.loads(text)["items"])
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `find_by_id(text, uid)` — объект пользователя с данным `id` из JSON-массива или `None`.

        ```
        find_by_id('[{"id": 1, "name": "Аня"}, {"id": 2, "name": "Боря"}]', 2)   # → {"id": 2, "name": "Боря"}
        ```
        """),
        """
        import json

        def find_by_id(text, uid):
            pass
        """,
        """
        def test_values():
            text = '[{"id": 1, "name": "Аня"}, {"id": 2, "name": "Боря"}]'
            assert find_by_id(text, 2) == {"id": 2, "name": "Боря"} and find_by_id(text, 9) is None, "Неверный результат"
        """,
        """
        import json

        def find_by_id(text, uid):
            for user in json.loads(text):
                if user["id"] == uid:
                    return user
            return None
        """),
),

lesson(f"{P}-m2-l2", "Списки объектов",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        import json
        products = json.loads('[{"name": "чай", "price": 300}, {"name": "кофе", "price": 500}, {"name": "сок", "price": 150}]')
        cheap = [p["name"] for p in products if p["price"] < 400]
        print(cheap, sum(p["price"] for p in products))
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа?", """
        import json
        from collections import Counter
        tests = json.loads('[{"name": "a", "status": "pass"}, {"name": "b", "status": "fail"}, {"name": "c", "status": "pass"}]')
        print(Counter(t["status"] for t in tests))
        """),
    out(f"{P}-m2-l2-e3", "Что выведет программа?", """
        import json
        users = json.loads('[{"name": "Боря", "age": 30}, {"name": "Аня", "age": 25}]')
        print([u["name"] for u in sorted(users, key=lambda u: u["age"])])
        print(max(users, key=lambda u: u["age"])["name"])
        """),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `names_by_status(text, status)` — имена тестов с заданным статусом из JSON-массива `[{"name": ..., "status": ...}]`.

        ```
        names_by_status('[{"name": "a", "status": "fail"}, {"name": "b", "status": "pass"}]', "fail")   # → ["a"]
        ```
        """),
        """
        import json

        def names_by_status(text, status):
            pass
        """,
        """
        def test_values():
            text = '[{"name": "a", "status": "fail"}, {"name": "b", "status": "pass"}, {"name": "c", "status": "fail"}]'
            assert names_by_status(text, "fail") == ["a", "c"] and names_by_status(text, "skip") == [], "Неверный список"
        """,
        """
        import json

        def names_by_status(text, status):
            return [t["name"] for t in json.loads(text) if t["status"] == status]
        """),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `average_price(text)` — средняя цена товаров из JSON-массива `[{"price": ...}]`, округлённая до 2 знаков. Пустой массив — `None`.

        ```
        average_price('[{"price": 100}, {"price": 250}]')   # → 175.0
        ```
        """),
        """
        import json

        def average_price(text):
            pass
        """,
        """
        def test_values():
            assert [average_price('[{"price": 100}, {"price": 250}]'), average_price("[]"), average_price('[{"price": 1}, {"price": 2}, {"price": 2}]')] == [175.0, None, 1.67], "Неверное среднее"
        """,
        """
        import json

        def average_price(text):
            items = json.loads(text)
            if not items:
                return None
            return round(sum(i["price"] for i in items) / len(items), 2)
        """),
    cod(f"{P}-m2-l2-e6", t("""
        Напиши функцию `count_by(text, field)` — словарь «значение поля → сколько объектов» для JSON-массива.

        ```
        count_by('[{"role": "qa"}, {"role": "dev"}, {"role": "qa"}]', "role")   # → {"qa": 2, "dev": 1}
        ```
        """),
        """
        import json

        def count_by(text, field):
            pass
        """,
        """
        def test_values():
            assert count_by('[{"role": "qa"}, {"role": "dev"}, {"role": "qa"}]', "role") == {"qa": 2, "dev": 1} and count_by("[]", "x") == {}, "Неверный подсчёт"
        """,
        """
        import json

        def count_by(text, field):
            counts = {}
            for obj in json.loads(text):
                value = obj[field]
                counts[value] = counts.get(value, 0) + 1
            return counts
        """),
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `index_by(text, field)` — словарь «значение поля → объект» (индекс для быстрого поиска).

        ```
        index_by('[{"id": 1, "n": "a"}, {"id": 2, "n": "b"}]', "id")   # → {1: {"id": 1, "n": "a"}, 2: {"id": 2, "n": "b"}}
        ```
        """),
        """
        import json

        def index_by(text, field):
            pass
        """,
        """
        def test_values():
            assert index_by('[{"id": 1, "n": "a"}, {"id": 2, "n": "b"}]', "id") == {1: {"id": 1, "n": "a"}, 2: {"id": 2, "n": "b"}}, "Неверный индекс"
        """,
        """
        import json

        def index_by(text, field):
            return {obj[field]: obj for obj in json.loads(text)}
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `top_n(text, field, n)` — значения поля `"name"` у `n` объектов с наибольшим значением `field` (по убыванию).

        ```
        top_n('[{"name": "a", "t": 1.2}, {"name": "b", "t": 3.4}, {"name": "c", "t": 2.0}]', "t", 2)   # → ["b", "c"]
        ```
        """),
        """
        import json

        def top_n(text, field, n):
            pass
        """,
        """
        def test_values():
            text = '[{"name": "a", "t": 1.2}, {"name": "b", "t": 3.4}, {"name": "c", "t": 2.0}]'
            assert top_n(text, "t", 2) == ["b", "c"] and top_n(text, "t", 0) == [] and top_n("[]", "t", 3) == [], "Неверный результат"
        """,
        """
        import json

        def top_n(text, field, n):
            items = sorted(json.loads(text), key=lambda obj: obj[field], reverse=True)
            return [obj["name"] for obj in items[:n]]
        """),
),

lesson(f"{P}-m2-l3", "Сборка и изменение JSON",
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        import json
        payload = {"name": "Аня", "roles": ["qa"]}
        payload["roles"].append("admin")
        payload["active"] = True
        print(json.dumps(payload, ensure_ascii=False))
        """),
    out(f"{P}-m2-l3-e2", "Что выведет программа? Строку JSON нельзя «поменять» — только разобрать и собрать заново.", """
        import json
        text = '{"count": 1}'
        data = json.loads(text)
        data["count"] += 1
        text = json.dumps(data)
        print(text)
        """),
    out(f"{P}-m2-l3-e3", "Что выведет программа?", """
        import json
        original = '{"a": 1, "b": {"c": 2}}'
        data = json.loads(original)
        data["b"]["c"] = 99
        print(original)
        print(json.dumps(data))
        """, hint="Исходная строка не меняется — меняется разобранный словарь."),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `add_field(text, key, value)` — добавить (или заменить) поле в JSON-объекте и вернуть новую JSON-строку (обычный `dumps`, без параметров).

        ```
        add_field('{"a": 1}', "b", True)   # → '{"a": 1, "b": true}'
        ```
        """),
        """
        import json

        def add_field(text, key, value):
            pass
        """,
        """
        def test_values():
            assert add_field('{"a": 1}', "b", True) == '{"a": 1, "b": true}' and add_field('{"a": 1}', "a", None) == '{"a": null}', "Неверный JSON"
        """,
        """
        import json

        def add_field(text, key, value):
            data = json.loads(text)
            data[key] = value
            return json.dumps(data)
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `rename_field(text, old, new)` — переименовать поле JSON-объекта (если оно есть) и вернуть новую JSON-строку.

        ```
        rename_field('{"userName": "a", "id": 1}', "userName", "user_name")   # → '{"id": 1, "user_name": "a"}'
        ```
        """),
        """
        import json

        def rename_field(text, old, new):
            pass
        """,
        """
        def test_values():
            assert rename_field('{"userName": "a", "id": 1}', "userName", "user_name") == '{"id": 1, "user_name": "a"}', "Неверный JSON"
            assert rename_field('{"a": 1}', "x", "y") == '{"a": 1}', "Нет поля — без изменений"
        """,
        """
        import json

        def rename_field(text, old, new):
            data = json.loads(text)
            if old in data:
                data[new] = data.pop(old)
            return json.dumps(data)
        """),
    cod(f"{P}-m2-l3-e6", t("""
        Напиши функцию `remove_nulls(text)` — убрать из JSON-объекта поля со значением `null` и вернуть новую JSON-строку.

        ```
        remove_nulls('{"a": 1, "b": null, "c": 0}')   # → '{"a": 1, "c": 0}'
        ```
        """),
        """
        import json

        def remove_nulls(text):
            pass
        """,
        """
        def test_values():
            assert remove_nulls('{"a": 1, "b": null, "c": 0}') == '{"a": 1, "c": 0}' and remove_nulls("{}") == "{}", "Неверный JSON"
        """,
        """
        import json

        def remove_nulls(text):
            data = json.loads(text)
            return json.dumps({k: v for k, v in data.items() if v is not None})
        """),
    cod(f"{P}-m2-l3-e7", t("""
        Напиши функцию `bump_version(text)` — увеличить поле `"version"` на 1 (если поля нет — считать, что было 0) и вернуть новую JSON-строку.

        ```
        bump_version('{"name": "app", "version": 3}')   # → '{"name": "app", "version": 4}'
        bump_version('{}')                              # → '{"version": 1}'
        ```
        """),
        """
        import json

        def bump_version(text):
            pass
        """,
        """
        def test_values():
            assert bump_version('{"name": "app", "version": 3}') == '{"name": "app", "version": 4}' and bump_version("{}") == '{"version": 1}', "Неверный JSON"
        """,
        """
        import json

        def bump_version(text):
            data = json.loads(text)
            data["version"] = data.get("version", 0) + 1
            return json.dumps(data)
        """),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `merge_json(a, b)` — слить два JSON-объекта (строки): поля `b` важнее. Вернуть JSON-строку с **отсортированными** ключами.

        ```
        merge_json('{"b": 1, "a": 1}', '{"a": 2, "c": 3}')   # → '{"a": 2, "b": 1, "c": 3}'
        ```
        """),
        """
        import json

        def merge_json(a, b):
            pass
        """,
        """
        def test_values():
            assert merge_json('{"b": 1, "a": 1}', '{"a": 2, "c": 3}') == '{"a": 2, "b": 1, "c": 3}', "Неверный JSON"
        """,
        """
        import json

        def merge_json(a, b):
            merged = {**json.loads(a), **json.loads(b)}
            return json.dumps(merged, sort_keys=True)
        """),
),

lesson(f"{P}-m2-l4", "Файлы: dump и load",
    out(f"{P}-m2-l4-e1", "Что выведет программа? StringIO — «файл в памяти».", """
        import json, io
        buffer = io.StringIO()
        json.dump({"a": 1}, buffer)
        print(buffer.getvalue())
        buffer.seek(0)
        print(json.load(buffer))
        """, hint="dump пишет в файл, load читает из файла. seek(0) — вернуться в начало."),
    out(f"{P}-m2-l4-e2", "Что выведет программа?", """
        import json, io
        f = io.StringIO('[{"id": 1}, {"id": 2}]')
        data = json.load(f)
        print(len(data), data[-1]["id"])
        """),
    out(f"{P}-m2-l4-e3", "Что выведет программа? JSON Lines.", """
        import json, io
        f = io.StringIO('{"id": 1}\\n{"id": 2}\\n\\n{"id": 3}\\n')
        rows = [json.loads(line) for line in f if line.strip()]
        print([r["id"] for r in rows])
        """, hint="Перебор файла идёт по строкам; пустые пропускаем."),
    cod(f"{P}-m2-l4-e4", t("""
        Напиши функцию `save(data, fp)` — записать данные в открытый файл `fp` как JSON с отступом 2 и без экранирования кириллицы (`json.dump`).

        Проверка передаст «файл в памяти» `io.StringIO`.
        """),
        """
        import json

        def save(data, fp):
            pass
        """,
        """
        import io

        def test_values():
            buf = io.StringIO()
            save({"имя": "Аня"}, buf)
            assert buf.getvalue() == '{\\n  "имя": "Аня"\\n}', f"В файле: {buf.getvalue()!r}"
        """,
        """
        import json

        def save(data, fp):
            json.dump(data, fp, indent=2, ensure_ascii=False)
        """),
    cod(f"{P}-m2-l4-e5", t("""
        Напиши функцию `load_ids(fp)` — прочитать из файла JSON-массив объектов (`json.load`) и вернуть список их `"id"`.
        """),
        """
        import json

        def load_ids(fp):
            pass
        """,
        """
        import io

        def test_values():
            assert load_ids(io.StringIO('[{"id": 3}, {"id": 5}]')) == [3, 5] and load_ids(io.StringIO("[]")) == [], "Неверный список"
        """,
        """
        import json

        def load_ids(fp):
            return [obj["id"] for obj in json.load(fp)]
        """),
    cod(f"{P}-m2-l4-e6", t("""
        Напиши функцию `read_lines(fp)` — прочитать файл в формате JSON Lines (по объекту на строку) и вернуть список объектов; пустые строки пропускать.
        """),
        """
        import json

        def read_lines(fp):
            pass
        """,
        """
        import io

        def test_values():
            assert read_lines(io.StringIO('{"a": 1}\\n\\n{"a": 2}\\n')) == [{"a": 1}, {"a": 2}] and read_lines(io.StringIO("")) == [], "Неверный результат"
        """,
        """
        import json

        def read_lines(fp):
            return [json.loads(line) for line in fp if line.strip()]
        """),
    cod(f"{P}-m2-l4-e7", t("""
        Напиши функцию `write_lines(records, fp)` — записать список объектов в файл в формате JSON Lines: каждый объект — `json.dumps` на своей строке, после каждой строки — `\\n`.
        """),
        """
        import json

        def write_lines(records, fp):
            pass
        """,
        """
        import io

        def test_values():
            buf = io.StringIO()
            write_lines([{"id": 1}, {"id": 2}], buf)
            assert buf.getvalue() == '{"id": 1}\\n{"id": 2}\\n', f"В файле: {buf.getvalue()!r}"
        """,
        """
        import json

        def write_lines(records, fp):
            for r in records:
                fp.write(json.dumps(r) + "\\n")
        """),
    cod(f"{P}-m2-l4-e8", t("""
        Напиши функцию `failed_count(fp)` — в файле JSON Lines записаны результаты тестов `{"name": ..., "status": ...}`. Вернуть количество записей со статусом `"fail"`.
        """),
        """
        import json

        def failed_count(fp):
            pass
        """,
        """
        import io

        def test_values():
            data = '{"name": "a", "status": "fail"}\\n{"name": "b", "status": "pass"}\\n{"name": "c", "status": "fail"}\\n'
            assert failed_count(io.StringIO(data)) == 2 and failed_count(io.StringIO("")) == 0, "Неверный подсчёт"
        """,
        """
        import json

        def failed_count(fp):
            count = 0
            for line in fp:
                if line.strip() and json.loads(line)["status"] == "fail":
                    count += 1
            return count
        """),
),
)
