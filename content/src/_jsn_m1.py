"""Тема «JSON», модуль 1 «JSON и Python» — задания. Теория — в _jsn_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "jsn"

m1 = module(f"{P}-m1", "JSON и Python", "🧾", "Формат JSON, loads и dumps, форматирование и соответствие типов",

lesson(f"{P}-m1-l1", "Что такое JSON",
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        import json
        text = '{"name": "Аня", "age": 25, "skills": ["qa", "sql"]}'
        data = json.loads(text)
        print(type(text).__name__, type(data).__name__)
        print(data["name"], data["skills"][1])
        """, hint="JSON — это строка; loads превращает её в объекты Python."),
    out(f"{P}-m1-l1-e2", "Что выведет программа?", """
        import json
        print(json.loads("[1, 2, 3]"), json.loads("true"), json.loads("null"))
        print(json.loads('"текст"'), json.loads("3.5"))
        """),
    out(f"{P}-m1-l1-e3", "Что выведет программа? Из Python в JSON.", """
        import json
        user = {"name": "Аня", "active": True, "phone": None}
        print(json.dumps(user, ensure_ascii=False))
        """, hint="True → true, None → null, кавычки — только двойные."),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `parse_name(text)` — разобрать JSON-строку с объектом пользователя и вернуть значение поля `"name"`.

        ```
        parse_name('{"name": "Аня", "age": 25}')   # → "Аня"
        ```
        """),
        """
        import json

        def parse_name(text):
            pass
        """,
        """
        def test_values():
            assert parse_name('{"name": "Аня", "age": 25}') == "Аня" and parse_name('{"id": 1, "name": "Bob"}') == "Bob", "Неверное имя"
        """,
        """
        import json

        def parse_name(text):
            return json.loads(text)["name"]
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `to_json(data)` — превратить Python-объект в JSON-строку, **не экранируя** кириллицу (`ensure_ascii=False`).

        ```
        to_json({"город": "Казань"})   # → '{"город": "Казань"}'
        ```
        """),
        """
        import json

        def to_json(data):
            pass
        """,
        """
        def test_values():
            assert to_json({"город": "Казань"}) == '{"город": "Казань"}' and to_json([1, None, True]) == "[1, null, true]", "Неверный JSON"
        """,
        """
        import json

        def to_json(data):
            return json.dumps(data, ensure_ascii=False)
        """),
    cod(f"{P}-m1-l1-e6", t("""
        Напиши функцию `count_items(text)` — сколько элементов в JSON-массиве.

        ```
        count_items('[{"id": 1}, {"id": 2}]')   # → 2
        count_items("[]")                       # → 0
        ```
        """),
        """
        import json

        def count_items(text):
            pass
        """,
        """
        def test_values():
            assert [count_items('[{"id": 1}, {"id": 2}]'), count_items("[]"), count_items("[1, 2, 3]")] == [2, 0, 3], "Неверное количество"
        """,
        """
        import json

        def count_items(text):
            return len(json.loads(text))
        """),
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `is_active(text)` — `True`, если в JSON-объекте поле `"active"` равно `true`; если поля нет или оно другое — `False`.

        ```
        is_active('{"active": true}')    # → True
        is_active('{"active": 1}')       # → False
        is_active('{}')                  # → False
        ```
        """),
        """
        import json

        def is_active(text):
            pass
        """,
        """
        def test_values():
            got = [is_active('{"active": true}'), is_active('{"active": 1}'), is_active('{}'), is_active('{"active": false}')]
            assert got == [True, False, False, False], f"Получено {got}"
        """,
        """
        import json

        def is_active(text):
            return json.loads(text).get("active") is True
        """, hint="1 == True в Python, поэтому сравнивай через is True."),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `skills_line(text)` — из JSON-объекта с массивом `"skills"` вернуть навыки через запятую с пробелом.

        ```
        skills_line('{"skills": ["qa", "sql", "python"]}')   # → "qa, sql, python"
        ```
        """),
        """
        import json

        def skills_line(text):
            pass
        """,
        """
        def test_values():
            assert skills_line('{"skills": ["qa", "sql", "python"]}') == "qa, sql, python" and skills_line('{"skills": []}') == "", "Неверная строка"
        """,
        """
        import json

        def skills_line(text):
            return ", ".join(json.loads(text)["skills"])
        """),
),

lesson(f"{P}-m1-l2", "json.loads: из строки в Python",
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        import json
        data = json.loads('{"a": 1, "b": [true, false], "c": {"d": null}}')
        print(data)
        print(data["c"]["d"] is None, data["b"][0])
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа? Числа в JSON.", """
        import json
        print(type(json.loads("10")).__name__, type(json.loads("10.0")).__name__, type(json.loads("1e3")).__name__)
        """),
    out(f"{P}-m1-l2-e3", "Что выведет программа? Одинарные кавычки.", """
        import json
        try:
            json.loads("{'name': 'Аня'}")
        except json.JSONDecodeError as e:
            print("ошибка:", e.msg)
        """, hint="В JSON строки и ключи — только в двойных кавычках."),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `total_price(text)` — JSON-массив товаров `[{"price": ...}, ...]`; вернуть сумму цен.

        ```
        total_price('[{"price": 300}, {"price": 150.5}]')   # → 450.5
        ```
        """),
        """
        import json

        def total_price(text):
            pass
        """,
        """
        def test_values():
            assert total_price('[{"price": 300}, {"price": 150.5}]') == 450.5 and total_price("[]") == 0, "Неверная сумма"
        """,
        """
        import json

        def total_price(text):
            return sum(item["price"] for item in json.loads(text))
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `get_ids(text)` — список значений `"id"` из JSON-массива объектов.

        ```
        get_ids('[{"id": 3}, {"id": 7}]')   # → [3, 7]
        ```
        """),
        """
        import json

        def get_ids(text):
            pass
        """,
        """
        def test_values():
            assert get_ids('[{"id": 3}, {"id": 7}]') == [3, 7] and get_ids("[]") == [], "Неверный список"
        """,
        """
        import json

        def get_ids(text):
            return [obj["id"] for obj in json.loads(text)]
        """),
    cod(f"{P}-m1-l2-e6", t("""
        Напиши функцию `parse_or_none(text)` — разобрать JSON, а если строка не является корректным JSON — вернуть `None`. Лови `json.JSONDecodeError`.

        ```
        parse_or_none('{"a": 1}')   # → {"a": 1}
        parse_or_none("{a: 1}")     # → None
        ```
        """),
        """
        import json

        def parse_or_none(text):
            pass
        """,
        """
        def test_values():
            assert parse_or_none('{"a": 1}') == {"a": 1} and parse_or_none("{a: 1}") is None and parse_or_none("") is None, "Неверный результат"
            assert parse_or_none("null") is None and parse_or_none("[]") == [], "Корректный JSON разбирается"
        """,
        """
        import json

        def parse_or_none(text):
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return None
        """),
    cod(f"{P}-m1-l2-e7", t("""
        Напиши функцию `keys_of(text)` — отсортированный список ключей верхнего уровня JSON-объекта.

        ```
        keys_of('{"name": "a", "id": 1, "email": "x"}')   # → ["email", "id", "name"]
        ```
        """),
        """
        import json

        def keys_of(text):
            pass
        """,
        """
        def test_values():
            assert keys_of('{"name": "a", "id": 1, "email": "x"}') == ["email", "id", "name"] and keys_of("{}") == [], "Неверные ключи"
        """,
        """
        import json

        def keys_of(text):
            return sorted(json.loads(text))
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши функцию `count_nulls(text)` — сколько полей верхнего уровня JSON-объекта имеют значение `null`.

        ```
        count_nulls('{"a": null, "b": 0, "c": null, "d": ""}')   # → 2
        ```
        """),
        """
        import json

        def count_nulls(text):
            pass
        """,
        """
        def test_values():
            assert count_nulls('{"a": null, "b": 0, "c": null, "d": ""}') == 2 and count_nulls("{}") == 0, "Неверный подсчёт"
        """,
        """
        import json

        def count_nulls(text):
            return sum(1 for v in json.loads(text).values() if v is None)
        """),
),

lesson(f"{P}-m1-l3", "json.dumps: форматирование",
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        import json
        d = {"b": 1, "a": [1, 2]}
        print(json.dumps(d))
        print(json.dumps(d, sort_keys=True))
        print(json.dumps(d, separators=(",", ":")))
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа? Отступы.", """
        import json
        print(json.dumps({"x": 1, "y": [1, 2]}, indent=2))
        """),
    out(f"{P}-m1-l3-e3", "Что выведет программа? Кириллица.", """
        import json
        print(json.dumps("Привет"))
        print(json.dumps("Привет", ensure_ascii=False))
        """, hint="По умолчанию не-ASCII символы экранируются как \\uXXXX."),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `compact(data)` — самая компактная JSON-строка: без пробелов после `,` и `:`.

        ```
        compact({"a": 1, "b": [1, 2]})   # → '{"a":1,"b":[1,2]}'
        ```
        """),
        """
        import json

        def compact(data):
            pass
        """,
        """
        def test_values():
            assert compact({"a": 1, "b": [1, 2]}) == '{"a":1,"b":[1,2]}', f"Получено {compact({'a': 1, 'b': [1, 2]})!r}"
        """,
        """
        import json

        def compact(data):
            return json.dumps(data, separators=(",", ":"))
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `pretty(data)` — «красивый» JSON для отчёта: отступ 2 пробела, ключи отсортированы, кириллица без экранирования.

        ```
        print(pretty({"б": 2, "а": 1}))
        # {
        #   "а": 1,
        #   "б": 2
        # }
        ```
        """),
        """
        import json

        def pretty(data):
            pass
        """,
        """
        def test_values():
            assert pretty({"б": 2, "а": 1}) == '{\\n  "а": 1,\\n  "б": 2\\n}', f"Получено {pretty({'б': 2, 'а': 1})!r}"
        """,
        """
        import json

        def pretty(data):
            return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
        """),
    cod(f"{P}-m1-l3-e6", t("""
        Напиши функцию `canonical(data)` — «каноническая» форма JSON для сравнения: ключи отсортированы, без лишних пробелов. Два словаря с одинаковым содержимым в разном порядке дадут одну и ту же строку.

        ```
        canonical({"b": 1, "a": 2}) == canonical({"a": 2, "b": 1})   # → True
        canonical({"b": 1, "a": 2})                                  # → '{"a":2,"b":1}'
        ```
        """),
        """
        import json

        def canonical(data):
            pass
        """,
        """
        def test_values():
            assert canonical({"b": 1, "a": 2}) == '{"a":2,"b":1}', "Неверная строка"
            assert canonical({"x": {"b": 1, "a": 2}}) == '{"x":{"a":2,"b":1}}', "Сортировка вложенных ключей тоже"
        """,
        """
        import json

        def canonical(data):
            return json.dumps(data, sort_keys=True, separators=(",", ":"))
        """),
    cod(f"{P}-m1-l3-e7", t("""
        Напиши функцию `json_size(data)` — размер компактного JSON (без экранирования кириллицы, без пробелов) **в байтах** UTF-8. Кириллическая буква занимает 2 байта.

        ```
        json_size({"a": 1})      # → 7    '{"a":1}'
        json_size({"я": 1})      # → 8
        ```
        """),
        """
        import json

        def json_size(data):
            pass
        """,
        """
        def test_values():
            assert [json_size({"a": 1}), json_size({"я": 1}), json_size([])] == [7, 8, 2], "Неверный размер"
        """,
        """
        import json

        def json_size(data):
            text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            return len(text.encode("utf-8"))
        """, hint='text.encode("utf-8") — байты строки; len — их количество.'),
    cod(f"{P}-m1-l3-e8", t("""
        Напиши функцию `to_lines(records)` — формат **JSON Lines**: каждая запись — компактный JSON на отдельной строке (строки через `\\n`).

        ```
        to_lines([{"id": 1}, {"id": 2}])   # → '{"id":1}\\n{"id":2}'
        ```
        """),
        """
        import json

        def to_lines(records):
            pass
        """,
        """
        def test_values():
            assert to_lines([{"id": 1}, {"id": 2}]) == '{"id":1}\\n{"id":2}' and to_lines([]) == "", "Неверный формат"
        """,
        """
        import json

        def to_lines(records):
            return "\\n".join(json.dumps(r, separators=(",", ":")) for r in records)
        """),
),

lesson(f"{P}-m1-l4", "Соответствие типов и подводные камни",
    out(f"{P}-m1-l4-e1", "Что выведет программа? Туда и обратно.", """
        import json
        data = {"t": (1, 2), 1: "one", "ok": True, "none": None}
        text = json.dumps(data)
        print(text)
        back = json.loads(text)
        print(back["t"], back["1"], back == data)
        """, hint="Кортеж становится массивом, а числовой ключ — строкой."),
    out(f"{P}-m1-l4-e2", "Что выведет программа?", """
        import json
        try:
            json.dumps({"tags": {"a", "b"}})
        except TypeError as e:
            print("TypeError:", e)
        """),
    out(f"{P}-m1-l4-e3", "Что выведет программа? Параметр default.", """
        import json
        from datetime import date
        print(json.dumps({"d": date(2024, 1, 15)}, default=str))
        """, hint="default вызывается для объектов, которые JSON не умеет сохранять."),
    cod(f"{P}-m1-l4-e4", t("""
        Напиши функцию `serialize(data)` — JSON-строка, где **множества** превращаются в отсортированные списки. Используй параметр `default` функции `dumps` со своей функцией-конвертером.

        ```
        serialize({"tags": {"b", "a"}})   # → '{"tags": ["a", "b"]}'
        ```
        """),
        """
        import json

        def serialize(data):
            pass
        """,
        """
        def test_values():
            assert serialize({"tags": {"b", "a"}}) == '{"tags": ["a", "b"]}' and serialize({"x": 1}) == '{"x": 1}', "Неверный JSON"
        """,
        """
        import json

        def convert(obj):
            if isinstance(obj, set):
                return sorted(obj)
            raise TypeError(f"не умею сохранять {type(obj).__name__}")

        def serialize(data):
            return json.dumps(data, default=convert)
        """, xp=20),
    cod(f"{P}-m1-l4-e5", t("""
        Напиши функцию `roundtrip_equal(data)` — совпадёт ли объект сам с собой после `dumps` → `loads`.

        ```
        roundtrip_equal({"a": [1, 2]})    # → True
        roundtrip_equal({"a": (1, 2)})    # → False   кортеж вернётся списком
        roundtrip_equal({1: "x"})         # → False   ключ станет "1"
        ```
        """),
        """
        import json

        def roundtrip_equal(data):
            pass
        """,
        """
        def test_values():
            got = [roundtrip_equal({"a": [1, 2]}), roundtrip_equal({"a": (1, 2)}), roundtrip_equal({1: "x"}), roundtrip_equal(None)]
            assert got == [True, False, False, True], f"Получено {got}"
        """,
        """
        import json

        def roundtrip_equal(data):
            return json.loads(json.dumps(data)) == data
        """),
    cod(f"{P}-m1-l4-e6", t("""
        После JSON числовые ключи словаря стали строками. Напиши функцию `fix_keys(d)` — вернуть новый словарь, где ключи из одних цифр снова превращены в `int`.

        ```
        fix_keys({"1": "a", "20": "b", "x": "c"})   # → {1: "a", 20: "b", "x": "c"}
        ```
        """),
        """
        def fix_keys(d):
            pass
        """,
        """
        def test_values():
            assert fix_keys({"1": "a", "20": "b", "x": "c"}) == {1: "a", 20: "b", "x": "c"} and fix_keys({}) == {}, "Неверные ключи"
        """,
        """
        def fix_keys(d):
            return {int(k) if k.isdigit() else k: v for k, v in d.items()}
        """),
    cod(f"{P}-m1-l4-e7", t("""
        Напиши **рекурсивную** функцию `to_jsonable(obj)` — привести структуру к виду, который JSON сохранит без потерь смысла:

        - кортежи → списки;
        - множества → отсортированные списки;
        - ключи словарей → строки;
        - вложенные структуры обрабатываются рекурсивно; остальное — как есть.

        ```
        to_jsonable({1: (2, {3}), "a": [(4,)]})   # → {"1": [2, [3]], "a": [[4]]}
        ```
        """),
        """
        def to_jsonable(obj):
            pass
        """,
        """
        def test_values():
            assert to_jsonable({1: (2, {3}), "a": [(4,)]}) == {"1": [2, [3]], "a": [[4]]}, f"Получено {to_jsonable({1: (2, {3}), 'a': [(4,)]})}"
            assert to_jsonable({"s": {"b", "a"}}) == {"s": ["a", "b"]} and to_jsonable(5) == 5, "Неверный результат"
        """,
        """
        def to_jsonable(obj):
            if isinstance(obj, dict):
                return {str(k): to_jsonable(v) for k, v in obj.items()}
            if isinstance(obj, (list, tuple)):
                return [to_jsonable(x) for x in obj]
            if isinstance(obj, set):
                return [to_jsonable(x) for x in sorted(obj)]
            return obj
        """, xp=25),
    cod(f"{P}-m1-l4-e8", t("""
        Напиши функцию `safe_dumps(data)` — JSON-строка, в которой любые «неудобные» объекты (даты, множества…) превращаются в строки через `str`. Используй `default=str`.

        ```
        from datetime import date
        safe_dumps({"d": date(2024, 5, 1)})   # → '{"d": "2024-05-01"}'
        ```
        """),
        """
        import json

        def safe_dumps(data):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert safe_dumps({"d": date(2024, 5, 1)}) == '{"d": "2024-05-01"}' and safe_dumps([1]) == "[1]", "Неверный JSON"
        """,
        """
        import json

        def safe_dumps(data):
            return json.dumps(data, default=str)
        """),
),
)
