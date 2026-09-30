"""Тема «JSON» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "jsn"

EXPLAIN = {

# ===== Модуль 1. Что такое JSON =====

f"{P}-m1-l1-e1": x(
    idea="JSON — это **текст**. `json.loads` превращает его в обычные объекты Python: объект → `dict`, массив → `list`.",
    lines=[
        ("data = json.loads(text)", "Из строки получили словарь."),
        ("print(type(text).__name__, type(data).__name__)", "`str dict`."),
        ('print(data["name"], data["skills"][1])', "Дальше — обычная работа со словарём и списком."),
    ],
    mistake="Пытаться достать `text[\"name\"]` из строки — сначала нужен `loads`."),

f"{P}-m1-l1-e2": x(
    idea="Любое значение JSON превращается в своё значение Python: `true` → `True`, `null` → `None`, строка в кавычках → `str`.",
    lines=[
        ('print(json.loads("[1, 2, 3]"), json.loads("true"), json.loads("null"))', "`[1, 2, 3] True None`."),
        ("""print(json.loads('"текст"'), json.loads("3.5"))""", "Строка JSON пишется в двойных кавычках."),
    ],
    mistake="Ожидать `true` и `null` в выводе — Python печатает свои `True` и `None`."),

f"{P}-m1-l1-e3": x(
    idea="`json.dumps` — обратное превращение: `True` → `true`, `None` → `null`. `ensure_ascii=False` оставляет кириллицу читаемой.",
    lines=[
        ("print(json.dumps(user, ensure_ascii=False))", "Двойные кавычки, `true`, `null`."),
    ],
    mistake="Ожидать одинарные кавычки, как у `print(словарь)`."),

f"{P}-m1-l1-e4": x(
    idea="Разобрать строку и взять поле — одна строка.",
    lines=[
        ('return json.loads(text)["name"]', "Сначала словарь, потом ключ."),
    ],
    mistake="`text[\"name\"]` — у строки нет ключей."),

f"{P}-m1-l1-e5": x(
    idea="Без `ensure_ascii=False` кириллица превратится в коды `\\u0433…`.",
    lines=[
        ("return json.dumps(data, ensure_ascii=False)", "`{\"город\": \"Казань\"}`."),
    ],
    mistake="`str(data)` — одинарные кавычки, это не JSON."),

f"{P}-m1-l1-e6": x(
    idea="Массив JSON становится списком — дальше `len`.",
    lines=[
        ("return len(json.loads(text))", "`[]` → 0."),
    ],
    mistake="`len(text)` — длина строки в символах."),

f"{P}-m1-l1-e7": x(
    idea="`get` — на случай отсутствующего поля; `is True` — строго логическое `true`, а не 1.",
    lines=[
        ('return json.loads(text).get("active") is True', "`1` не `True` по `is`."),
    ],
    mistake="`== True` — 1 тоже пройдёт, потому что `1 == True`."),

f"{P}-m1-l1-e8": x(
    idea="Массив навыков — список строк, его склеиваем `join`.",
    lines=[
        ('return ", ".join(json.loads(text)["skills"])', "`qa, sql, python`."),
    ],
    mistake="`str(skills)` — получится `['qa', 'sql', …]`."),

# ===== json.loads =====

f"{P}-m1-l2-e1": x(
    idea="Вложенный JSON превращается во вложенные словари и списки. `null` становится `None`.",
    lines=[
        ("print(data)", "`true` → `True`, `null` → `None`."),
        ('print(data["c"]["d"] is None, data["b"][0])', "`True True`."),
    ],
    mistake="Ожидать строку `\"null\"`."),

f"{P}-m1-l2-e2": x(
    idea="Число без точки — `int`; с точкой или в научной записи — `float`.",
    lines=[
        ('print(type(json.loads("10")).__name__, type(json.loads("10.0")).__name__, type(json.loads("1e3")).__name__)', "`int float float`."),
    ],
    mistake="Решить, что `1e3` — целое."),

f"{P}-m1-l2-e3": x(
    idea="В JSON строки и ключи — **только в двойных кавычках**. Одинарные — ошибка разбора.",
    lines=[
        ("""json.loads("{'name': 'Аня'}")""", "Это запись словаря Python, а не JSON."),
        ('print("ошибка:", e.msg)', "`msg` — короткое описание ошибки."),
    ],
    mistake="Пытаться разобрать `str(словарь)` через `json.loads`."),

f"{P}-m1-l2-e4": x(
    idea="Список словарей — генератор по полю `price` и `sum`.",
    lines=[
        ('return sum(item["price"] for item in json.loads(text))', "300 + 150.5."),
    ],
    mistake="Разбирать JSON внутри цикла для каждого элемента."),

f"{P}-m1-l2-e5": x(
    idea="Списковое включение по разобранному массиву.",
    lines=[
        ('return [obj["id"] for obj in json.loads(text)]', "`[3, 7]`."),
    ],
    mistake="Вернуть сами объекты вместо id."),

f"{P}-m1-l2-e6": x(
    idea="Некорректный JSON вызывает `json.JSONDecodeError` — ловим именно его.",
    lines=[
        ("try:\n        return json.loads(text)", "Корректный — результат."),
        ("except json.JSONDecodeError:\n        return None", "`{a: 1}` — ключ без кавычек."),
    ],
    mistake="Ловить `Exception` — спрячет и другие ошибки."),

f"{P}-m1-l2-e7": x(
    idea="`sorted(словарь)` — отсортированные ключи.",
    lines=[
        ("return sorted(json.loads(text))", "email, id, name."),
    ],
    mistake="Сортировать значения."),

f"{P}-m1-l2-e8": x(
    idea="`null` становится `None` — считаем именно их. `0` и `\"\"` — не `null`.",
    lines=[
        ("return sum(1 for v in json.loads(text).values() if v is None)", "`a` и `c`."),
    ],
    mistake="`if not v` — посчитает и 0, и пустую строку."),

# ===== json.dumps: форматирование =====

f"{P}-m1-l3-e1": x(
    idea="`sort_keys` упорядочивает ключи, `separators` задаёт разделители — без пробелов получается компактнее.",
    lines=[
        ("print(json.dumps(d))", "Порядок как в словаре, с пробелами."),
        ("print(json.dumps(d, sort_keys=True))", "`a` раньше `b`."),
        ('print(json.dumps(d, separators=(",", ":")))', "Без пробелов."),
    ],
    mistake="Ожидать, что `dumps` сам сортирует ключи."),

f"{P}-m1-l3-e2": x(
    idea="`indent=2` — многострочный вывод с отступом в два пробела для каждого уровня вложенности.",
    lines=[
        ('print(json.dumps({"x": 1, "y": [1, 2]}, indent=2))', "Каждый элемент — на своей строке, даже элементы списка."),
    ],
    mistake="Ожидать список `[1, 2]` в одну строку."),

f"{P}-m1-l3-e3": x(
    idea="По умолчанию `dumps` экранирует всё, что не ASCII: кириллица превращается в `\\uXXXX`. `ensure_ascii=False` это выключает.",
    lines=[
        ('print(json.dumps("Привет"))', "Коды символов."),
        ('print(json.dumps("Привет", ensure_ascii=False))', "Читаемый текст."),
    ],
    mistake="Ожидать `Привет` без кавычек — JSON-строка всегда в кавычках."),

f"{P}-m1-l3-e4": x(
    idea="`separators=(\",\", \":\")` убирает пробелы после запятых и двоеточий.",
    lines=[
        ('return json.dumps(data, separators=(",", ":"))', "`{\"a\":1,\"b\":[1,2]}`."),
    ],
    mistake="`.replace(\" \", \"\")` — удалит пробелы и внутри строковых значений."),

f"{P}-m1-l3-e5": x(
    idea="Три параметра сразу: отступ, сортировка ключей, кириллица без экранирования.",
    lines=[
        ("return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)", "Удобно читать в отчёте."),
    ],
    mistake="Забыть `ensure_ascii=False` — ключи превратятся в коды."),

f"{P}-m1-l3-e6": x(
    idea="Одинаковые данные в разном порядке дают одну строку, если сортировать ключи и убрать пробелы.",
    lines=[
        ('return json.dumps(data, sort_keys=True, separators=(",", ":"))', "Каноническая форма."),
    ],
    mistake="Без `sort_keys` строки будут разными."),

f"{P}-m1-l3-e7": x(
    idea="Размер в байтах — длина **закодированной** строки. Кириллица в UTF-8 занимает 2 байта на символ.",
    lines=[
        ('text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))', "Компактно, без экранирования."),
        ('return len(text.encode("utf-8"))', "`{\"я\":1}` — 7 символов, но 8 байт."),
    ],
    mistake="`len(text)` — это символы, а не байты."),

f"{P}-m1-l3-e8": x(
    idea="JSON Lines: каждая запись — отдельная компактная JSON-строка, строки через перевод строки.",
    lines=[
        ('return "\\n".join(json.dumps(r, separators=(",", ":")) for r in records)', "Без переноса в конце."),
    ],
    mistake="`json.dumps(records)` — получится один массив, а не строки."),

# ===== Соответствие типов =====

f"{P}-m1-l4-e1": x(
    idea="JSON теряет часть типов: кортеж становится списком, ключ-число — строкой. После обратного разбора данные уже не равны исходным.",
    lines=[
        ("print(text)", "`(1, 2)` → `[1, 2]`, ключ `1` → `\"1\"`."),
        ('print(back["t"], back["1"], back == data)', "Список, ключ-строка, `False`."),
    ],
    mistake="Ожидать `back == data`."),

f"{P}-m1-l4-e2": x(
    idea="Множества в JSON нет — `dumps` падает с `TypeError`.",
    lines=[
        ('json.dumps({"tags": {"a", "b"}})', "`set is not JSON serializable`."),
    ],
    mistake="Ожидать, что множество превратится в список само."),

f"{P}-m1-l4-e3": x(
    idea="`default=функция` вызывается для объектов, которые JSON не умеет сохранять. `str` превращает дату в строку.",
    lines=[
        ('print(json.dumps({"d": date(2024, 1, 15)}, default=str))', "`\"2024-01-15\"`."),
    ],
    mistake="Ожидать `TypeError` — `default` спасает."),

f"{P}-m1-l4-e4": x(
    idea="Своя функция-конвертер: множество → отсортированный список, остальное — честная ошибка.",
    lines=[
        ("if isinstance(obj, set):\n        return sorted(obj)", "Сортировка делает результат предсказуемым."),
        ('raise TypeError(f"не умею сохранять {type(obj).__name__}")', "Незнакомые объекты не глотаем молча."),
        ("return json.dumps(data, default=convert)", "Функция без скобок."),
    ],
    mistake="`default=convert()` — это вызов, а нужна сама функция."),

f"{P}-m1-l4-e5": x(
    idea="Туда и обратно: `loads(dumps(x)) == x` только если все типы есть в JSON.",
    lines=[
        ("return json.loads(json.dumps(data)) == data", "Кортеж и ключ-число не переживут."),
    ],
    mistake="Сравнивать строки JSON — это не проверит типы."),

f"{P}-m1-l4-e6": x(
    idea="Ключи из одних цифр возвращаем к `int`, остальные оставляем.",
    lines=[
        ("return {int(k) if k.isdigit() else k: v for k, v in d.items()}", "Условное выражение в ключе."),
    ],
    mistake="`int(k)` для всех — упадёт на `x`."),

f"{P}-m1-l4-e7": x(
    idea="Рекурсивное приведение: у словаря — ключи в строки, у кортежей и списков — в списки, у множеств — в отсортированные списки.",
    lines=[
        ("return {str(k): to_jsonable(v) for k, v in obj.items()}", "Ключи — строки, значения — рекурсивно."),
        ("return [to_jsonable(x) for x in obj]", "Кортеж → список."),
        ("return [to_jsonable(x) for x in sorted(obj)]", "Множество → отсортированный список."),
        ("return obj", "Числа, строки — как есть."),
    ],
    mistake="Не спускаться внутрь — вложенные кортежи и множества останутся."),

f"{P}-m1-l4-e8": x(
    idea="`default=str` — универсальная страховка: всё неизвестное превращается в строку.",
    lines=[
        ("return json.dumps(data, default=str)", "Дата → `\"2024-05-01\"`."),
    ],
    mistake="`default=str()` — вызов вместо функции."),

# ===== Модуль 2. Навигация по вложенному JSON =====

f"{P}-m2-l1-e1": x(
    idea="Разобранный ответ API — вложенные словари и списки. Промежуточная переменная упрощает доступ.",
    lines=[
        ('users = resp["data"]["users"]', "Список пользователей."),
        ('print(len(users), users[1]["name"], resp["total"])', "`2 Боря 2`."),
    ],
    mistake="Путать индекс: второй пользователь — `[1]`."),

f"{P}-m2-l1-e2": x(
    idea="`null` становится `None`, у которого нет `.get`. `or {}` подставляет пустой словарь, и дальше можно безопасно читать.",
    lines=[
        ('address = resp["data"]["user"]["address"] or {}', "`None or {}` → `{}`."),
        ('print(address.get("city", "нет города"))', "Нет города."),
        ('print(resp.get("meta", {}).get("page"))', "Нет `meta` — `None`."),
    ],
    mistake="`address.get(...)` на `None` — `AttributeError`."),

f"{P}-m2-l1-e3": x(
    idea="Список позиций заказа перебираем с номерами через `enumerate`.",
    lines=[
        ('for i, item in enumerate(order["items"], start=1):', "Номера с 1."),
    ],
    mistake="Нумерация с 0."),

f"{P}-m2-l1-e4": x(
    idea="Доходим до списка и берём первого, только если он есть.",
    lines=[
        ('users = json.loads(text)["data"]["users"]', "Список."),
        ("if not users:\n        return None", "Пусто."),
        ('return users[0]["name"]', "Первый."),
    ],
    mistake="`users[0]` без проверки — `IndexError`."),

f"{P}-m2-l1-e5": x(
    idea="На каждом шаге смотрим тип текущего значения: у словаря ищем ключ, у списка — допустимый индекс. Не подошло — `default`.",
    lines=[
        ("if isinstance(current, dict) and key in current:", "Шаг по объекту."),
        ("elif isinstance(current, list) and isinstance(key, int) and -len(current) <= key < len(current):", "Шаг по массиву с проверкой границ."),
        ("else:\n            return default", "Пути нет."),
    ],
    mistake="Использовать `try/except` только с `KeyError` — выход за границы списка даст `IndexError`."),

f"{P}-m2-l1-e6": x(
    idea="`get` не падает на отсутствующем поле; `is not None` отсекает и отсутствие, и `null`.",
    lines=[
        ('return [u["email"] for u in users if u.get("email") is not None]', "Только `a@x`."),
    ],
    mistake="`u[\"email\"]` без проверки — `KeyError` на втором пользователе."),

f"{P}-m2-l1-e7": x(
    idea="Сумма по полю списка позиций.",
    lines=[
        ('return sum(item["qty"] for item in json.loads(text)["items"])', "2 + 1."),
    ],
    mistake="`len(items)` — количество позиций, а не товаров."),

f"{P}-m2-l1-e8": x(
    idea="Поиск по полю: первое совпадение — сразу `return`.",
    lines=[
        ('if user["id"] == uid:\n            return user', "Весь объект."),
        ("return None", "Не нашли."),
    ],
    mistake="Сравнивать с `str(uid)` — в JSON id число."),

# ===== Списки объектов =====

f"{P}-m2-l2-e1": x(
    idea="Фильтр и сумма по списку объектов из JSON.",
    lines=[
        ('cheap = [p["name"] for p in products if p["price"] < 400]', "Чай и сок."),
        ('print(cheap, sum(p["price"] for p in products))', "300 + 500 + 150."),
    ],
    mistake="Включить кофе — 500 не меньше 400."),

f"{P}-m2-l2-e2": x(
    idea="`Counter` по полю статуса — сводка результатов тестов.",
    lines=[
        ('print(Counter(t["status"] for t in tests))', "`pass` — 2, `fail` — 1."),
    ],
    mistake="Ожидать порядок появления — `Counter` печатается по убыванию."),

f"{P}-m2-l2-e3": x(
    idea="Сортировка и `max` с ключом по полю объекта.",
    lines=[
        ('print([u["name"] for u in sorted(users, key=lambda u: u["age"])])', "По возрасту: Аня, Боря."),
        ('print(max(users, key=lambda u: u["age"])["name"])', "Старший — Боря."),
    ],
    mistake="Сортировать без ключа — словари нельзя сравнить."),

f"{P}-m2-l2-e4": x(
    idea="Фильтр по полю, в ответ — имена.",
    lines=[
        ('return [t["name"] for t in json.loads(text) if t["status"] == status]', "`[\"a\"]`."),
    ],
    mistake="Вернуть объекты целиком."),

f"{P}-m2-l2-e5": x(
    idea="Пустой массив — отдельно, иначе деление на ноль.",
    lines=[
        ("if not items:\n        return None", "Защита."),
        ('return round(sum(i["price"] for i in items) / len(items), 2)', "175.0."),
    ],
    mistake="Разобрать JSON дважды — лишняя работа."),

f"{P}-m2-l2-e6": x(
    idea="Счётчик по значению поля: `get(value, 0) + 1`.",
    lines=[
        ("value = obj[field]", "Значение поля."),
        ("counts[value] = counts.get(value, 0) + 1", "`qa` — 2."),
    ],
    summary="Или `dict(Counter(obj[field] for obj in json.loads(text)))`.",
    mistake="`counts[value] += 1` — `KeyError` на новом значении."),

f"{P}-m2-l2-e7": x(
    idea="Индекс для быстрого поиска: ключ — значение поля, значение — весь объект.",
    lines=[
        ("return {obj[field]: obj for obj in json.loads(text)}", "Поиск по id — мгновенный."),
    ],
    mistake="Хранить в индексе только одно поле."),

f"{P}-m2-l2-e8": x(
    idea="Сортируем объекты по полю по убыванию, берём первые `n`, из них — имена.",
    lines=[
        ("items = sorted(json.loads(text), key=lambda obj: obj[field], reverse=True)", "b 3.4, c 2.0, a 1.2."),
        ('return [obj["name"] for obj in items[:n]]', "`[\"b\", \"c\"]`."),
    ],
    mistake="Забыть `reverse=True` — возьмутся самые маленькие."),

# ===== Сборка и изменение JSON =====

f"{P}-m2-l3-e1": x(
    idea="Тело запроса собирают как обычный словарь, а в JSON превращают в самом конце.",
    lines=[
        ('payload["roles"].append("admin")', "Меняем список внутри словаря."),
        ('payload["active"] = True', "Новое поле."),
        ("print(json.dumps(payload, ensure_ascii=False))", "`True` → `true`."),
    ],
    mistake="Собирать JSON-строку вручную через `+` — легко ошибиться с кавычками."),

f"{P}-m2-l3-e2": x(
    idea="Строку JSON не изменить на месте: разбираем, меняем словарь, собираем новую строку.",
    lines=[
        ("data = json.loads(text)", "В словарь."),
        ('data["count"] += 1', "Меняем значение."),
        ("text = json.dumps(data)", "Обратно в строку."),
    ],
    mistake="Пытаться заменить цифру в строке через `replace` — сломается на других значениях."),

f"{P}-m2-l3-e3": x(
    idea="`loads` создаёт новые объекты — изменения в них не трогают исходную строку.",
    lines=[
        ('data["b"]["c"] = 99', "Меняется словарь."),
        ("print(original)", "Строка осталась прежней."),
    ],
    mistake="Ожидать, что `original` тоже изменится."),

f"{P}-m2-l3-e4": x(
    idea="Разобрать → изменить → собрать.",
    lines=[
        ("data[key] = value", "Добавление или замена."),
        ("return json.dumps(data)", "`True` → `true`."),
    ],
    mistake="Вернуть словарь вместо строки."),

f"{P}-m2-l3-e5": x(
    idea="`pop` снимает значение по старому ключу и кладёт под новый — новый ключ оказывается в конце.",
    lines=[
        ("if old in data:\n        data[new] = data.pop(old)", "Переименование."),
    ],
    mistake="`data[new] = data[old]` без удаления — останутся оба поля."),

f"{P}-m2-l3-e6": x(
    idea="Фильтр по `None` в словарном включении, результат — снова в JSON.",
    lines=[
        ("return json.dumps({k: v for k, v in data.items() if v is not None})", "`c: 0` остаётся."),
    ],
    mistake="`if v` — пропадёт `c: 0`."),

f"{P}-m2-l3-e7": x(
    idea="`get(\"version\", 0)` — версия или 0, прибавляем единицу.",
    lines=[
        ('data["version"] = data.get("version", 0) + 1', "3 → 4, нет поля → 1."),
    ],
    mistake="`data[\"version\"] += 1` — `KeyError` для пустого объекта."),

f"{P}-m2-l3-e8": x(
    idea="Слияние разобранных объектов и `sort_keys` для предсказуемого порядка.",
    lines=[
        ("merged = {**json.loads(a), **json.loads(b)}", "`b` важнее."),
        ("return json.dumps(merged, sort_keys=True)", "a, b, c."),
    ],
    mistake="Склеивать строки JSON — получится некорректный JSON."),

# ===== Файлы: dump и load =====

f"{P}-m2-l4-e1": x(
    idea="`dump`/`load` (без `s`) пишут и читают **файл**, `dumps`/`loads` — строку. `StringIO` — файл в памяти.",
    lines=[
        ('json.dump({"a": 1}, buffer)', "Запись в «файл»."),
        ("buffer.seek(0)", "Перемотка в начало, иначе читать нечего."),
        ("print(json.load(buffer))", "Чтение обратно — словарь."),
    ],
    mistake="Забыть `seek(0)` — `load` прочитает пустоту и упадёт."),

f"{P}-m2-l4-e2": x(
    idea="`json.load(f)` читает весь файл и разбирает его.",
    lines=[
        ("data = json.load(f)", "Список из двух объектов."),
        ('print(len(data), data[-1]["id"])', "`2 2`."),
    ],
    mistake="`json.loads(f)` — `loads` ждёт строку, а не файл."),

f"{P}-m2-l4-e3": x(
    idea="JSON Lines читают построчно: каждая непустая строка — отдельный JSON.",
    lines=[
        ("rows = [json.loads(line) for line in f if line.strip()]", "Пустая строка пропущена."),
    ],
    mistake="`json.load(f)` — весь файл не является одним JSON."),

f"{P}-m2-l4-e4": x(
    idea="`json.dump` пишет прямо в открытый файл; параметры те же, что у `dumps`.",
    lines=[
        ("json.dump(data, fp, indent=2, ensure_ascii=False)", "Читаемо и с кириллицей."),
    ],
    mistake="`fp.write(data)` — записать словарь напрямую нельзя."),

f"{P}-m2-l4-e5": x(
    idea="`json.load` читает массив из файла, дальше — обычный список.",
    lines=[
        ('return [obj["id"] for obj in json.load(fp)]', "Список id."),
    ],
    mistake="`fp.read()` без `loads` — останется строка."),

f"{P}-m2-l4-e6": x(
    idea="Файл перебирается построчно; пустые строки пропускаем.",
    lines=[
        ("return [json.loads(line) for line in fp if line.strip()]", "Каждая строка — объект."),
    ],
    mistake="Не пропустить пустые — `JSONDecodeError`."),

f"{P}-m2-l4-e7": x(
    idea="Каждый объект — `dumps` и перевод строки.",
    lines=[
        ('fp.write(json.dumps(r) + "\\n")', "`write` сам перевод строки не добавляет."),
    ],
    mistake="`json.dump(records, fp)` — получится один массив."),

f"{P}-m2-l4-e8": x(
    idea="Идём по строкам, разбираем непустые и считаем `fail`.",
    lines=[
        ('if line.strip() and json.loads(line)["status"] == "fail":', "`and` не даст разбирать пустую строку."),
    ],
    mistake="Загрузить весь файл через `json.load` — это не один JSON."),

# ===== Модуль 3. Проверка полей и типов =====

f"{P}-m3-l1-e1": x(
    idea="Проверка типов по схеме: `isinstance` для каждого поля и `all` для итога.",
    lines=[
        ('checks = {"id": int, "name": str, "tags": list, "score": float}', "Поле → тип."),
        ("print(all(isinstance(body[k], t) for k, t in checks.items()))", "Все совпали."),
    ],
    mistake="Ожидать `False` для пустого списка — тип всё равно `list`."),

f"{P}-m3-l1-e2": x(
    idea="Число в кавычках в JSON — это строка. Частый баг API: `\"7\"` вместо `7`.",
    lines=[
        ('print(isinstance(body["id"], int), type(body["id"]).__name__)', "`False str`."),
    ],
    mistake="Считать `\"7\"` числом."),

f"{P}-m3-l1-e3": x(
    idea="`10` в JSON — целое. Если цена может быть и целой, и дробной, проверяют кортежем `(int, float)`.",
    lines=[
        ('print(isinstance(body["price"], float), isinstance(body["price"], (int, float)))', "`False True`."),
    ],
    mistake="Требовать строго `float` — тест упадёт на целой цене."),

f"{P}-m3-l1-e4": x(
    idea="Идём по списку обязательных полей и собираем отсутствующие.",
    lines=[
        ("return [f for f in required if f not in body]", "Порядок — как в `required`."),
    ],
    mistake="`set(required) - set(body)` — порядок потеряется."),

f"{P}-m3-l1-e5": x(
    idea="Проверяем тип только у присутствующих полей; `isinstance` понимает и кортеж типов.",
    lines=[
        ("return [f for f, typ in schema.items() if f in body and not isinstance(body[f], typ)]", "`id` — строка вместо числа."),
    ],
    mistake="Не проверять наличие — `KeyError` на отсутствующем поле."),

f"{P}-m3-l1-e6": x(
    idea="Три независимые проверки, у каждой свой текст ошибки. `get` — поле может отсутствовать.",
    lines=[
        ('if not (isinstance(uid, int) and not isinstance(uid, bool) and uid > 0):\n        errors.append("bad id")', "`True` — не id."),
        ('if not (isinstance(email, str) and "@" in email):', "Проверка типа до `in`."),
        ('if not (isinstance(name, str) and name):', "Пустая строка ложна."),
    ],
    mistake="`\"@\" in email` без проверки типа — для числа будет `TypeError`."),

f"{P}-m3-l1-e7": x(
    idea="`all` по объектам массива; для пустого массива — `True`.",
    lines=[
        ("return all(field in obj for obj in json.loads(text))", "У второго нет `id`."),
    ],
    mistake="`any` — хватит одного объекта."),

f"{P}-m3-l1-e8": x(
    idea="Сначала статус, потом тип корня, потом ключи.",
    lines=[
        ("if status != 200:\n        return False", "Разбирать тело не нужно."),
        ('return isinstance(body, dict) and "data" in body and "error" not in body', "Массив — не объект."),
    ],
    mistake="Не проверить, что корень — объект: для массива `[\"data\"]` проверка `\"data\" in body` вернёт `True`."),

# ===== Сравнение JSON =====

f"{P}-m3-l2-e1": x(
    idea="Разобранные объекты сравниваются по содержимому. Строки JSON — посимвольно, поэтому порядок ключей важен, если не сортировать.",
    lines=[
        ("print(a == b, json.dumps(a) == json.dumps(b), json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True))", "`True False True`."),
    ],
    mistake="Сравнивать ответы API как строки."),

f"{P}-m3-l2-e2": x(
    idea="Порядок в массиве важен. `1 == 1.0` и `True == 1` в Python — поэтому обычное `==` их не различит.",
    lines=[
        ('print(json.loads("[1, 2]") == json.loads("[2, 1]"))', "`False`."),
        ('print(json.loads("1") == json.loads("1.0"), json.loads("true") == json.loads("1"))', "`True True`."),
    ],
    mistake="Ожидать `False` для `true == 1`."),

f"{P}-m3-l2-e3": x(
    idea="Изменчивые поля (время, id запроса) убирают перед сравнением.",
    lines=[
        ('actual.pop("ts", None)', "Удалили метку времени."),
        ("print(actual == expected)", "`True`."),
    ],
    mistake="Сравнивать с `ts` — тест будет падать каждый раз."),

f"{P}-m3-l2-e4": x(
    idea="Разобрать обе строки и сравнить объекты — пробелы и порядок ключей перестают влиять.",
    lines=[
        ("return json.loads(a) == json.loads(b)", "Порядок в массивах важен."),
    ],
    mistake="`a == b` — строки с разными пробелами не равны."),

f"{P}-m3-l2-e5": x(
    idea="Убираем игнорируемые поля из обоих объектов и сравниваем остаток.",
    lines=[
        ("da = {k: v for k, v in json.loads(a).items() if k not in ignore}", "Без `ts`."),
        ("return da == db", "`True`."),
    ],
    mistake="Удалять только из одного объекта."),

f"{P}-m3-l2-e6": x(
    idea="Разности множеств ключей в обе стороны.",
    lines=[
        ('return {"only_a": sorted(ka - kb), "only_b": sorted(kb - ka)}', "`x` и `y`."),
    ],
    mistake="Сравнивать значения — задание только про набор полей."),

f"{P}-m3-l2-e7": x(
    idea="Словари нельзя сортировать напрямую, а их канонические строки — можно. Отсортированные списки строк равны, если наборы объектов одинаковые.",
    lines=[
        ("return sorted(json.dumps(obj, sort_keys=True) for obj in json.loads(text))", "Каждый объект → строка."),
        ("return canon(a) == canon(b)", "Порядок элементов больше не важен."),
    ],
    mistake="`sorted(json.loads(a))` — словари не сравниваются, `TypeError`."),

f"{P}-m3-l2-e8": x(
    idea="В JSON `true` и `1` — разные строки, поэтому сравнение канонических JSON-строк строгое.",
    lines=[
        ("return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)", "`\"ok\": true` ≠ `\"ok\": 1`."),
    ],
    mistake="`a == b` — `True == 1` даст равенство."),

# ===== Ошибки разбора =====

f"{P}-m3-l3-e1": x(
    idea="Корректный JSON — строго по правилам: двойные кавычки, без висящих запятых, непустой текст. `null` — корректный JSON.",
    lines=[
        ("print(repr(json.loads(text)))", "`null` → `None`."),
        ('print("не JSON:", repr(text))', "Одинарные кавычки, запятая в конце, пустая строка."),
    ],
    mistake="Считать `null` ошибкой."),

f"{P}-m3-l3-e2": x(
    idea="Ошибка разбора знает, где сломался JSON: `lineno` — строка, `colno` — позиция в ней.",
    lines=[
        ("print(e.lineno, e.colno, e.msg)", "Вторая строка, после `\"b\": ` ждали значение."),
    ],
    mistake="Считать позицию от начала всего текста — `colno` отсчитывается в строке."),

f"{P}-m3-l3-e3": x(
    idea="`JSONDecodeError` — подкласс `ValueError`, поэтому ловится и как `ValueError`.",
    lines=[
        ("print(issubclass(json.JSONDecodeError, ValueError))", "`True`."),
    ],
    mistake="Думать, что нужен именно `JSONDecodeError`."),

f"{P}-m3-l3-e4": x(
    idea="Ошибка разбора — вернуть значение по умолчанию.",
    lines=[
        ("except json.JSONDecodeError:\n        return default", "`oops` → `{}`."),
    ],
    mistake="`return None` вместо `default`."),

f"{P}-m3-l3-e5": x(
    idea="Пробуем разобрать каждую строку, неудачные индексы собираем.",
    lines=[
        ("for i, text in enumerate(texts):", "Индекс нужен в ответе."),
        ("except json.JSONDecodeError:\n            bad.append(i)", "1 и 3."),
    ],
    mistake="Один `try` вокруг всего цикла — остановится на первой ошибке."),

f"{P}-m3-l3-e6": x(
    idea="Разбор может пройти, но корень оказаться не объектом — это отдельная проверка.",
    lines=[
        ("data = json.loads(text)", "Ошибку разбора не ловим."),
        ('if not isinstance(data, dict):\n        raise ValueError("ожидали объект")', "Массив — ошибка."),
    ],
    mistake="Оборачивать всё в `try/except` — задание просит ошибку разбора не перехватывать."),

f"{P}-m3-l3-e7": x(
    idea="Позиция ошибки — атрибуты исключения. Корректная строка — `None` после `try`.",
    lines=[
        ("return (e.lineno, e.colno)", "`(1, 9)` для висящей запятой."),
        ("return None", "Ошибки не было."),
    ],
    mistake="Вернуть `e.pos` — это позиция от начала всего текста, а нужны строка и столбец."),

f"{P}-m3-l3-e8": x(
    idea="Три случая: пустое тело, корректный JSON, мусор вроде HTML-страницы ошибки.",
    lines=[
        ("if not text.strip():\n        return {}", "Пустое тело — не ошибка."),
        ('except json.JSONDecodeError:\n        return {"error": "invalid json"}', "`<html>`."),
    ],
    mistake="Не проверить пустоту — `\"\"` станет `invalid json`."),

# ===== Практика: отчёт о прогоне =====

f"{P}-m3-l4-e1": x(
    idea="Отчёт — словарь со списком словарей, в JSON превращается целиком.",
    lines=[
        ('report = {"total": len(results), "tests": [{"name": n, "status": s, "time": t} for n, s, t in results]}', "Кортежи → объекты."),
    ],
    mistake="Сохранять кортежи — в JSON они станут безымянными массивами."),

f"{P}-m3-l4-e2": x(
    idea="Разбор отчёта и подсчёт упавших и прошедших.",
    lines=[
        ('failed = [t["name"] for t in report["tests"] if t["status"] == "fail"]', "`['b']`."),
        ('print(failed, len(report["tests"]) - len(failed))', "Прошедших 1."),
    ],
    mistake="Ответить `['b'] 2` — всего тестов два, упал один, значит прошёл один."),

f"{P}-m3-l4-e3": x(
    idea="Процент прохождения и сортировка ключей в выводе.",
    lines=[
        ('summary["rate"] = round(summary["passed"] / (summary["passed"] + summary["failed"]) * 100, 1)', "2 / 3 · 100 = 66.7."),
        ("print(json.dumps(summary, sort_keys=True))", "failed, passed, rate."),
    ],
    mistake="Округлить долю до умножения — получится 70.0."),

f"{P}-m3-l4-e4": x(
    idea="Сначала список объектов тестов, из него — счётчики.",
    lines=[
        ('tests = [{"name": n, "status": s, "time": t} for n, s, t in results]', "Объекты."),
        ('"passed": sum(1 for t in tests if t["status"] == "pass"),', "Подсчёт."),
    ],
    mistake="Считать `failed` как `total - passed` — статусы бывают и другими (skip)."),

f"{P}-m3-l4-e5": x(
    idea="Счётчики по кортежам, JSON с отсортированными ключами.",
    lines=[
        ('passed = sum(1 for _, s in results if s == "pass")', "`_` — имя не нужно."),
        ('return json.dumps({"passed": passed, "failed": failed}, sort_keys=True)', "`failed` раньше `passed`."),
    ],
    mistake="Без `sort_keys` порядок будет `passed, failed`."),

f"{P}-m3-l4-e6": x(
    idea="Разобрать отчёт и отфильтровать по статусу.",
    lines=[
        ('return [t["name"] for t in json.loads(text)["tests"] if t["status"] == "fail"]', "Имена."),
    ],
    mistake="Забыть `[\"tests\"]` — перебор пойдёт по ключам отчёта."),

f"{P}-m3-l4-e7": x(
    idea="`max` по полю времени, пустой список — отдельно.",
    lines=[
        ("if not tests:\n        return None", "`max([])` упал бы."),
        ('return max(tests, key=lambda t: t["time"])["name"]', "Имя самого долгого."),
    ],
    mistake="Вернуть весь объект теста."),

f"{P}-m3-l4-e8": x(
    idea="Разбираем каждую сводку и складываем в общий счётчик.",
    lines=[
        ('total = {"passed": 0, "failed": 0}', "Старт с нулей."),
        ('total["passed"] += report["passed"]', "Накопление."),
    ],
    mistake="Склеивать строки JSON — это не сложит числа."),
}
