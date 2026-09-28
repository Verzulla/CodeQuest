"""Тема «JSON», модуль 3 «JSON в тестах API» — задания. Теория — в _jsn_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "jsn"

m3 = module(f"{P}-m3", "JSON в тестах API", "🧪", "Проверка полей и типов, сравнение, ошибки разбора, отчёт о прогоне",

lesson(f"{P}-m3-l1", "Проверка полей и типов ответа",
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        import json
        body = json.loads('{"id": 7, "name": "Аня", "tags": [], "score": 4.5}')
        checks = {"id": int, "name": str, "tags": list, "score": float}
        print(all(isinstance(body[k], t) for k, t in checks.items()))
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа? Число в кавычках.", """
        import json
        body = json.loads('{"id": "7"}')
        print(isinstance(body["id"], int), type(body["id"]).__name__)
        """),
    out(f"{P}-m3-l1-e3", "Что выведет программа? 10 или 10.0.", """
        import json
        body = json.loads('{"price": 10}')
        print(isinstance(body["price"], float), isinstance(body["price"], (int, float)))
        """, hint="JSON-число без точки становится int."),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `missing_fields(text, required)` — список обязательных полей (в порядке `required`), которых нет в JSON-объекте.

        ```
        missing_fields('{"id": 1}', ["id", "name", "email"])   # → ["name", "email"]
        ```
        """),
        """
        import json

        def missing_fields(text, required):
            pass
        """,
        """
        def test_values():
            assert missing_fields('{"id": 1}', ["id", "name", "email"]) == ["name", "email"] and missing_fields('{"a": null}', ["a"]) == [], "Неверный список"
        """,
        """
        import json

        def missing_fields(text, required):
            body = json.loads(text)
            return [f for f in required if f not in body]
        """, hint="Поле со значением null — есть, просто пустое."),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `wrong_types(text, schema)` — список полей (в порядке схемы), которые **есть** в JSON-объекте, но имеют не тот тип. `schema` — словарь `{поле: тип или кортеж типов}`.

        ```
        wrong_types('{"id": "7", "price": 10}', {"id": int, "price": (int, float)})   # → ["id"]
        ```
        """),
        """
        import json

        def wrong_types(text, schema):
            pass
        """,
        """
        def test_values():
            assert wrong_types('{"id": "7", "price": 10}', {"id": int, "price": (int, float)}) == ["id"], "Неверный список"
            assert wrong_types('{"a": 1}', {"a": int, "b": str}) == [], "Отсутствующие поля не считаем"
        """,
        """
        import json

        def wrong_types(text, schema):
            body = json.loads(text)
            return [f for f, typ in schema.items() if f in body and not isinstance(body[f], typ)]
        """),
    cod(f"{P}-m3-l1-e6", t("""
        Напиши функцию `validate_user(text)` — список ошибок пользователя из JSON (в указанном порядке проверок):

        - `id` — целое положительное число, иначе `"bad id"`;
        - `email` — строка с `@`, иначе `"bad email"`;
        - `name` — непустая строка, иначе `"bad name"`.

        ```
        validate_user('{"id": 1, "email": "a@x", "name": "Аня"}')   # → []
        validate_user('{"id": 0, "email": "ax", "name": ""}')        # → ["bad id", "bad email", "bad name"]
        ```
        """),
        """
        import json

        def validate_user(text):
            pass
        """,
        """
        def test_values():
            assert validate_user('{"id": 1, "email": "a@x", "name": "Аня"}') == [], "Корректный пользователь"
            assert validate_user('{"id": 0, "email": "ax", "name": ""}') == ["bad id", "bad email", "bad name"], "Все ошибки"
            assert validate_user('{"id": "1", "name": "x"}') == ["bad id", "bad email"], "Тип id и отсутствующий email"
            assert validate_user('{"id": true, "email": "a@b", "name": "x"}') == ["bad id"], "true — не id"
        """,
        """
        import json

        def validate_user(text):
            u = json.loads(text)
            errors = []
            uid = u.get("id")
            if not (isinstance(uid, int) and not isinstance(uid, bool) and uid > 0):
                errors.append("bad id")
            email = u.get("email")
            if not (isinstance(email, str) and "@" in email):
                errors.append("bad email")
            name = u.get("name")
            if not (isinstance(name, str) and name):
                errors.append("bad name")
            return errors
        """, hint="JSON true становится True, а isinstance(True, int) — True. Исключи bool отдельно.", xp=25),
    cod(f"{P}-m3-l1-e7", t("""
        Напиши функцию `all_have(text, field)` — у **каждого** объекта JSON-массива есть поле `field`. Для пустого массива — `True`.

        ```
        all_have('[{"id": 1}, {"id": 2}]', "id")    # → True
        all_have('[{"id": 1}, {"x": 2}]', "id")     # → False
        ```
        """),
        """
        import json

        def all_have(text, field):
            pass
        """,
        """
        def test_values():
            assert [all_have('[{"id": 1}, {"id": 2}]', "id"), all_have('[{"id": 1}, {"x": 2}]', "id"), all_have("[]", "id")] == [True, False, True], "Неверный результат"
        """,
        """
        import json

        def all_have(text, field):
            return all(field in obj for obj in json.loads(text))
        """),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `response_ok(status, text)` — успешен ли ответ API: статус `200`, тело — JSON-**объект**, в нём есть ключ `"data"` и **нет** ключа `"error"`.

        ```
        response_ok(200, '{"data": []}')                 # → True
        response_ok(200, '{"data": 1, "error": "x"}')    # → False
        response_ok(200, '[1, 2]')                       # → False
        ```
        """),
        """
        import json

        def response_ok(status, text):
            pass
        """,
        """
        def test_values():
            got = [response_ok(200, '{"data": []}'), response_ok(200, '{"data": 1, "error": "x"}'), response_ok(200, '[1, 2]'), response_ok(500, '{"data": 1}'), response_ok(200, '{}')]
            assert got == [True, False, False, False, False], f"Получено {got}"
        """,
        """
        import json

        def response_ok(status, text):
            if status != 200:
                return False
            body = json.loads(text)
            return isinstance(body, dict) and "data" in body and "error" not in body
        """),
),

lesson(f"{P}-m3-l2", "Сравнение JSON",
    out(f"{P}-m3-l2-e1", "Что выведет программа? Строки против объектов.", """
        import json
        a = json.loads('{"x": 1, "y": 2}')
        b = json.loads('{"y": 2, "x": 1}')
        print(a == b, json.dumps(a) == json.dumps(b), json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True))
        """, hint="Словари равны без учёта порядка, а строки JSON — нет."),
    out(f"{P}-m3-l2-e2", "Что выведет программа?", """
        import json
        print(json.loads("[1, 2]") == json.loads("[2, 1]"))
        print(json.loads("1") == json.loads("1.0"), json.loads("true") == json.loads("1"))
        """, hint="Порядок в массивах важен. А в Python 1 == 1.0 и True == 1."),
    out(f"{P}-m3-l2-e3", "Что выведет программа?", """
        import json
        expected = {"id": 1, "status": "ok"}
        actual = json.loads('{"id": 1, "status": "ok", "ts": 1712}')
        actual.pop("ts", None)
        print(actual == expected)
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши функцию `json_equal(a, b)` — равны ли две JSON-строки **по содержимому** (порядок ключей и пробелы не важны).

        ```
        json_equal('{"a": 1, "b": 2}', '{"b":2,"a":1}')   # → True
        json_equal('[1, 2]', '[2, 1]')                    # → False
        ```
        """),
        """
        import json

        def json_equal(a, b):
            pass
        """,
        """
        def test_values():
            assert [json_equal('{"a": 1, "b": 2}', '{"b":2,"a":1}'), json_equal('[1, 2]', '[2, 1]'), json_equal("null", "null")] == [True, False, True], "Неверное сравнение"
        """,
        """
        import json

        def json_equal(a, b):
            return json.loads(a) == json.loads(b)
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `equal_ignoring(a, b, ignore)` — равны ли два JSON-объекта (строки), если не учитывать поля верхнего уровня из списка `ignore` (например, время и id запроса).

        ```
        equal_ignoring('{"id": 1, "ts": 5}', '{"id": 1, "ts": 9}', ["ts"])   # → True
        ```
        """),
        """
        import json

        def equal_ignoring(a, b, ignore):
            pass
        """,
        """
        def test_values():
            assert equal_ignoring('{"id": 1, "ts": 5}', '{"id": 1, "ts": 9}', ["ts"]) is True, "ts игнорируем"
            assert equal_ignoring('{"id": 1}', '{"id": 2}', ["ts"]) is False and equal_ignoring('{"id": 1, "x": 1}', '{"id": 1}', []) is False, "Различия"
        """,
        """
        import json

        def equal_ignoring(a, b, ignore):
            da = {k: v for k, v in json.loads(a).items() if k not in ignore}
            db = {k: v for k, v in json.loads(b).items() if k not in ignore}
            return da == db
        """),
    cod(f"{P}-m3-l2-e6", t("""
        Напиши функцию `diff_keys(a, b)` — различия в наборе полей двух JSON-объектов: словарь `{"only_a": [...], "only_b": [...]}` с отсортированными списками.

        ```
        diff_keys('{"id": 1, "x": 2}', '{"id": 1, "y": 3}')   # → {"only_a": ["x"], "only_b": ["y"]}
        ```
        """),
        """
        import json

        def diff_keys(a, b):
            pass
        """,
        """
        def test_values():
            assert diff_keys('{"id": 1, "x": 2}', '{"id": 1, "y": 3}') == {"only_a": ["x"], "only_b": ["y"]}, "Неверные различия"
            assert diff_keys("{}", "{}") == {"only_a": [], "only_b": []}, "Нет различий"
        """,
        """
        import json

        def diff_keys(a, b):
            ka = json.loads(a).keys()
            kb = json.loads(b).keys()
            return {"only_a": sorted(ka - kb), "only_b": sorted(kb - ka)}
        """),
    cod(f"{P}-m3-l2-e7", t("""
        Напиши функцию `same_items(a, b)` — содержат ли два JSON-массива объектов одни и те же объекты, **без учёта порядка** элементов. Подсказка: превращай каждый объект в каноническую строку `json.dumps(obj, sort_keys=True)` и сравнивай отсортированные списки строк.

        ```
        same_items('[{"id": 1}, {"id": 2}]', '[{"id": 2}, {"id": 1}]')   # → True
        ```
        """),
        """
        import json

        def same_items(a, b):
            pass
        """,
        """
        def test_values():
            assert same_items('[{"id": 1}, {"id": 2}]', '[{"id": 2}, {"id": 1}]') is True, "Порядок не важен"
            assert same_items('[{"id": 1}, {"id": 1}]', '[{"id": 1}]') is False and same_items('[{"a": 1, "b": 2}]', '[{"b": 2, "a": 1}]') is True, "Повторы важны, порядок ключей — нет"
        """,
        """
        import json

        def same_items(a, b):
            def canon(text):
                return sorted(json.dumps(obj, sort_keys=True) for obj in json.loads(text))
            return canon(a) == canon(b)
        """, xp=20),
    cod(f"{P}-m3-l2-e8", t("""
        В Python `True == 1`, поэтому обычное сравнение не отличит JSON `true` от `1`. Напиши функцию `strict_equal(a, b)` — строгое сравнение двух Python-объектов через их каноническую JSON-форму (`sort_keys=True`).

        ```
        strict_equal({"ok": True}, {"ok": 1})    # → False
        strict_equal({"a": 1, "b": 2}, {"b": 2, "a": 1})   # → True
        ```
        """),
        """
        import json

        def strict_equal(a, b):
            pass
        """,
        """
        def test_values():
            assert [strict_equal({"ok": True}, {"ok": 1}), strict_equal({"a": 1, "b": 2}, {"b": 2, "a": 1}), strict_equal([1], [1.0])] == [False, True, False], "Неверное сравнение"
        """,
        """
        import json

        def strict_equal(a, b):
            return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
        """),
),

lesson(f"{P}-m3-l3", "Ошибки разбора и безопасная обработка",
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        import json
        for text in ['{"a": 1}', "{'a': 1}", '{"a": 1,}', "", "null"]:
            try:
                print(repr(json.loads(text)))
            except json.JSONDecodeError:
                print("не JSON:", repr(text))
        """, hint="JSON не допускает одинарные кавычки и запятую в конце; пустая строка — тоже не JSON."),
    out(f"{P}-m3-l3-e2", "Что выведет программа? Где ошибка.", """
        import json
        try:
            json.loads('{"a": 1,\\n "b": }')
        except json.JSONDecodeError as e:
            print(e.lineno, e.colno, e.msg)
        """),
    out(f"{P}-m3-l3-e3", "Что выведет программа?", """
        import json
        print(issubclass(json.JSONDecodeError, ValueError))
        try:
            json.loads("abc")
        except ValueError:
            print("поймали как ValueError")
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `safe_parse(text, default=None)` — разобрать JSON, а при ошибке разбора вернуть `default`.

        ```
        safe_parse('[1]')          # → [1]
        safe_parse('oops', {})     # → {}
        ```
        """),
        """
        import json

        def safe_parse(text, default=None):
            pass
        """,
        """
        def test_values():
            assert [safe_parse('[1]'), safe_parse('oops', {}), safe_parse('')] == [[1], {}, None], "Неверный результат"
        """,
        """
        import json

        def safe_parse(text, default=None):
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return default
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `invalid_indexes(texts)` — индексы строк из списка, которые **не** являются корректным JSON.

        ```
        invalid_indexes(['{"a": 1}', "{a: 1}", "[]", "nul"])   # → [1, 3]
        ```
        """),
        """
        import json

        def invalid_indexes(texts):
            pass
        """,
        """
        def test_values():
            assert invalid_indexes(['{"a": 1}', "{a: 1}", "[]", "nul"]) == [1, 3] and invalid_indexes([]) == [], "Неверные индексы"
        """,
        """
        import json

        def invalid_indexes(texts):
            bad = []
            for i, text in enumerate(texts):
                try:
                    json.loads(text)
                except json.JSONDecodeError:
                    bad.append(i)
            return bad
        """),
    cod(f"{P}-m3-l3-e6", t("""
        Напиши функцию `parse_object(text)` — разобрать JSON и убедиться, что это **объект**. Если корень — не объект (массив, число…), выбросить `ValueError("ожидали объект")`. Ошибку разбора не перехватывать (она сама является `ValueError`).

        ```
        parse_object('{"a": 1}')   # → {"a": 1}
        parse_object('[1]')        # ValueError: ожидали объект
        ```
        """),
        """
        import json

        def parse_object(text):
            pass
        """,
        """
        def test_ok():
            assert parse_object('{"a": 1}') == {"a": 1}, "Объект разбирается"

        def test_not_object():
            for bad in ("[1]", "5", "null", "{oops"):
                try:
                    parse_object(bad)
                except ValueError:
                    continue
                assert False, f"Для {bad!r} нужен ValueError"
        """,
        """
        import json

        def parse_object(text):
            data = json.loads(text)
            if not isinstance(data, dict):
                raise ValueError("ожидали объект")
            return data
        """),
    cod(f"{P}-m3-l3-e7", t("""
        Напиши функцию `error_position(text)` — пара `(номер строки, номер столбца)` места ошибки разбора JSON или `None`, если строка корректна. Используй атрибуты `lineno` и `colno` исключения.

        ```
        error_position('{"a": 1}')        # → None
        error_position('{"a": 1,}')       # → (1, 9)
        ```
        """),
        """
        import json

        def error_position(text):
            pass
        """,
        """
        def test_values():
            assert error_position('{"a": 1}') is None and error_position('{"a": 1,}') == (1, 9), "Неверная позиция"
        """,
        """
        import json

        def error_position(text):
            try:
                json.loads(text)
            except json.JSONDecodeError as e:
                return (e.lineno, e.colno)
            return None
        """),
    cod(f"{P}-m3-l3-e8", t("""
        Напиши функцию `parse_body(text)` — разбор тела ответа API:

        - пустое тело (или только пробелы) → `{}`;
        - корректный JSON → результат разбора;
        - некорректный → `{"error": "invalid json"}`.

        ```
        parse_body("  ")          # → {}
        parse_body('{"a": 1}')    # → {"a": 1}
        parse_body("<html>")      # → {"error": "invalid json"}
        ```
        """),
        """
        import json

        def parse_body(text):
            pass
        """,
        """
        def test_values():
            assert [parse_body("  "), parse_body('{"a": 1}'), parse_body("<html>"), parse_body("[]")] == [{}, {"a": 1}, {"error": "invalid json"}, []], "Неверный результат"
        """,
        """
        import json

        def parse_body(text):
            if not text.strip():
                return {}
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {"error": "invalid json"}
        """),
),

lesson(f"{P}-m3-l4", "Практика: отчёт о прогоне тестов",
    out(f"{P}-m3-l4-e1", "Что выведет программа?", """
        import json
        results = [("login", "pass", 1.2), ("pay", "fail", 3.4)]
        report = {"total": len(results), "tests": [{"name": n, "status": s, "time": t} for n, s, t in results]}
        print(json.dumps(report, ensure_ascii=False))
        """),
    out(f"{P}-m3-l4-e2", "Что выведет программа?", """
        import json
        text = '{"tests": [{"name": "a", "status": "pass"}, {"name": "b", "status": "fail"}]}'
        report = json.loads(text)
        failed = [t["name"] for t in report["tests"] if t["status"] == "fail"]
        print(failed, len(report["tests"]) - len(failed))
        """),
    out(f"{P}-m3-l4-e3", "Что выведет программа?", """
        import json
        summary = {"passed": 2, "failed": 1}
        summary["rate"] = round(summary["passed"] / (summary["passed"] + summary["failed"]) * 100, 1)
        print(json.dumps(summary, sort_keys=True))
        """),
    cod(f"{P}-m3-l4-e4", t("""
        Напиши функцию `make_report(results)` — `results` это список кортежей `(имя, статус, время)`. Вернуть словарь:

        ```
        {"total": N, "passed": ..., "failed": ..., "tests": [{"name": ..., "status": ..., "time": ...}, ...]}
        ```

        ```
        make_report([("a", "pass", 1.0), ("b", "fail", 2.0)])
        # → {"total": 2, "passed": 1, "failed": 1, "tests": [{"name": "a", "status": "pass", "time": 1.0}, {"name": "b", "status": "fail", "time": 2.0}]}
        ```
        """),
        """
        def make_report(results):
            pass
        """,
        """
        def test_values():
            got = make_report([("a", "pass", 1.0), ("b", "fail", 2.0)])
            assert got == {"total": 2, "passed": 1, "failed": 1, "tests": [{"name": "a", "status": "pass", "time": 1.0}, {"name": "b", "status": "fail", "time": 2.0}]}, f"Получено {got}"
            assert make_report([]) == {"total": 0, "passed": 0, "failed": 0, "tests": []}, "Пустой прогон"
        """,
        """
        def make_report(results):
            tests = [{"name": n, "status": s, "time": t} for n, s, t in results]
            return {
                "total": len(tests),
                "passed": sum(1 for t in tests if t["status"] == "pass"),
                "failed": sum(1 for t in tests if t["status"] == "fail"),
                "tests": tests,
            }
        """, xp=20),
    cod(f"{P}-m3-l4-e5", t("""
        Напиши функцию `summary_json(results)` — JSON-строка сводки `{"failed": ..., "passed": ...}` с **отсортированными** ключами для списка кортежей `(имя, статус)`.

        ```
        summary_json([("a", "pass"), ("b", "fail"), ("c", "pass")])   # → '{"failed": 1, "passed": 2}'
        ```
        """),
        """
        import json

        def summary_json(results):
            pass
        """,
        """
        def test_values():
            assert summary_json([("a", "pass"), ("b", "fail"), ("c", "pass")]) == '{"failed": 1, "passed": 2}' and summary_json([]) == '{"failed": 0, "passed": 0}', "Неверная сводка"
        """,
        """
        import json

        def summary_json(results):
            passed = sum(1 for _, s in results if s == "pass")
            failed = sum(1 for _, s in results if s == "fail")
            return json.dumps({"passed": passed, "failed": failed}, sort_keys=True)
        """),
    cod(f"{P}-m3-l4-e6", t("""
        Напиши функцию `failed_names(text)` — имена упавших тестов из JSON-отчёта `{"tests": [{"name": ..., "status": ...}]}`.
        """),
        """
        import json

        def failed_names(text):
            pass
        """,
        """
        def test_values():
            text = '{"tests": [{"name": "a", "status": "pass"}, {"name": "b", "status": "fail"}]}'
            assert failed_names(text) == ["b"] and failed_names('{"tests": []}') == [], "Неверный список"
        """,
        """
        import json

        def failed_names(text):
            return [t["name"] for t in json.loads(text)["tests"] if t["status"] == "fail"]
        """),
    cod(f"{P}-m3-l4-e7", t("""
        Напиши функцию `slowest(text)` — имя самого долгого теста из JSON-отчёта `{"tests": [{"name": ..., "time": ...}]}`; пустой список — `None`.
        """),
        """
        import json

        def slowest(text):
            pass
        """,
        """
        def test_values():
            text = '{"tests": [{"name": "a", "time": 1.2}, {"name": "b", "time": 3.4}, {"name": "c", "time": 0.5}]}'
            assert slowest(text) == "b" and slowest('{"tests": []}') is None, "Неверный результат"
        """,
        """
        import json

        def slowest(text):
            tests = json.loads(text)["tests"]
            if not tests:
                return None
            return max(tests, key=lambda t: t["time"])["name"]
        """),
    cod(f"{P}-m3-l4-e8", t("""
        Напиши функцию `merge_reports(texts)` — сложить сводки нескольких прогонов: каждый элемент списка — JSON-строка `{"passed": ..., "failed": ...}`. Вернуть словарь с суммами.

        ```
        merge_reports(['{"passed": 2, "failed": 1}', '{"passed": 5, "failed": 0}'])   # → {"passed": 7, "failed": 1}
        ```
        """),
        """
        import json

        def merge_reports(texts):
            pass
        """,
        """
        def test_values():
            assert merge_reports(['{"passed": 2, "failed": 1}', '{"passed": 5, "failed": 0}']) == {"passed": 7, "failed": 1} and merge_reports([]) == {"passed": 0, "failed": 0}, "Неверная сумма"
        """,
        """
        import json

        def merge_reports(texts):
            total = {"passed": 0, "failed": 0}
            for text in texts:
                report = json.loads(text)
                total["passed"] += report["passed"]
                total["failed"] += report["failed"]
            return total
        """),
),
)
