"""Теория модуля «Работа с данными» темы «JSON».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- jsn-m2-l1 ----------
'jsn-m2-l1': dict(
    full=t(r'''
## Зачем это нужно

Реальные ответы API вложенные: `{"data": {"users": [{...}, {...}]}, "meta": {...}}`. Чтобы достать нужное значение, идут по цепочке ключей и индексов. Главное — не упасть, если какого-то уровня нет или там `null`.

## Цепочка ключей и индексов

```python
import json
resp = json.loads('{"data": {"users": [{"id": 1, "name": "Аня"}, {"id": 2, "name": "Боря"}]}, "total": 2}')
users = resp["data"]["users"]
print(len(users), users[1]["name"], resp["total"])
```

- `resp["data"]` — словарь, `["users"]` — список, `[1]` — второй пользователь, `["name"]` — поле.
- Промежуточное значение удобно сохранить в переменную (`users`) — короче и понятнее.
- Вывод: `2 Боря 2`.

```viz
{"type": "json", "title": "Нажми на поле — увидишь путь в Python", "var": "data", "select": ["order", "items", 0, "price"], "data": {"order": {"id": 501, "items": [{"title": "Книга", "price": 450}, {"title": "Ручка", "price": 30}], "coupon": null}, "status": "paid"}}
```

## null и отсутствующие ключи

```python
import json
resp = json.loads('{"data": {"user": {"address": null}}}')
address = resp["data"]["user"]["address"] or {}
print(address.get("city", "нет города"))
print(resp.get("meta", {}).get("page"))
```

- Поле есть, но значение `null` (`None`): `resp[...]["address"]` не падает, но у `None` нет `.get`. Приём `значение or {}` подменяет `None` пустым словарём.
- Ключа нет вовсе: `resp.get("meta", {})` вернёт пустой словарь, и цепочку можно продолжать (тема «Словари»).
- Вывод: `нет города`, `None`.

## Перебор массива объектов

```python
import json
order = json.loads('{"items": [{"sku": "A", "qty": 2}, {"sku": "B", "qty": 1}]}')
for i, item in enumerate(order["items"], start=1):
    print(i, item["sku"], item["qty"])
print(sum(item["qty"] for item in order["items"]))
```

Вывод: `1 A 2`, `2 B 1`, `3`.

## Путь как список

```python
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

data = {"users": [{"name": "Аня"}, {"name": "Боря"}]}
print(get_in(data, ["users", 1, "name"]), get_in(data, ["users", 5, "name"], "-"))
```

- Строки в пути — ключи объектов, числа — индексы массивов.
- На каждом шаге проверяем, что двигаться можно: у словаря есть ключ, у списка — такой индекс.
- Вывод: `Боря -`.

## Поиск в массиве

```python
import json
users = json.loads('[{"id": 1, "name": "Аня"}, {"id": 2, "name": "Боря"}]')
found = next((u for u in users if u["id"] == 2), None)
print(found)
```

- `next(генератор, по_умолчанию)` — первый подходящий элемент или умолчание (аналог цикла с `return`).
- Вывод: `{'id': 2, 'name': 'Боря'}`.

## Итог

- Вложенный JSON — цепочка `data["a"]["b"][0]["c"]`; промежуточное — в переменную.
- `null` → `None`: `значение or {}`; нет ключа — `get(ключ, {})`.
- Путь списком ключей и индексов — цикл с проверками.
- Поиск первого — цикл или `next((... for ...), None)`.
'''),
    short=t(r'''
```py
users = resp["data"]["users"]         # по цепочке
users[1]["name"]
(resp["data"]["user"]["address"] or {}).get("city")   # null -> {}
resp.get("meta", {}).get("page")       # нет ключа
next((u for u in users if u["id"] == 2), None)        # найти первый
```
'''),
    quiz=[
        q('Что вернёт `json.loads(\'{"a": null}\')["a"] or {}`?',
            ['`None`', '`{}`', 'Ошибка', '`"null"`'],
            1, 'None ложен — берётся {}.'),
        q('Как безопасно прочитать `resp["meta"]["page"]`, если meta может отсутствовать?',
            ['`resp["meta"]["page"]`', '`resp.get("meta", {}).get("page")`', '`resp.meta.page`', 'Никак'],
            1, 'Цепочка get с пустым словарём.'),
        q('Что вернёт `next((x for x in [] ), "нет")`?',
            ['Ошибка', '`"нет"`', '`None`', '`[]`'],
            1, 'Значение по умолчанию.'),
    ],
),

# ---------- jsn-m2-l2 ----------
'jsn-m2-l2': dict(
    full=t(r'''
## Зачем это нужно

Очень часто API возвращает **массив объектов**: список товаров, пользователей, результатов тестов. После разбора это список словарей, и к нему применимы все знакомые приёмы: фильтр, сумма, подсчёт, сортировка, индекс.

## Фильтр и сумма

```python
import json
products = json.loads('[{"name": "чай", "price": 300}, {"name": "кофе", "price": 500}, {"name": "сок", "price": 150}]')
cheap = [p["name"] for p in products if p["price"] < 400]
print(cheap, sum(p["price"] for p in products))
```

- Списковое включение с условием и `sum` с генератором. Вывод: `['чай', 'сок'] 950`.

## Подсчёт по полю

```python
import json
from collections import Counter
tests = json.loads('[{"name": "a", "status": "pass"}, {"name": "b", "status": "fail"}, {"name": "c", "status": "pass"}]')
print(Counter(t["status"] for t in tests))
```

- `Counter` считает значения поля (тема «Словари»). Вывод: `Counter({'pass': 2, 'fail': 1})`.

Без `Counter` — словарь и `get`:

```python
import json
data = json.loads('[{"role": "qa"}, {"role": "dev"}, {"role": "qa"}]')
counts = {}
for obj in data:
    counts[obj["role"]] = counts.get(obj["role"], 0) + 1
print(counts)
```

Вывод: `{'qa': 2, 'dev': 1}`.

## Сортировка и лучший элемент

```python
import json
users = json.loads('[{"name": "Боря", "age": 30}, {"name": "Аня", "age": 25}]')
print([u["name"] for u in sorted(users, key=lambda u: u["age"])])
print(max(users, key=lambda u: u["age"])["name"])
```

- `key=lambda u: u["age"]` — сравнивать объекты по полю. Вывод: `['Аня', 'Боря']`, `Боря`.

Топ-N:

```python
import json
items = json.loads('[{"name": "a", "t": 1.2}, {"name": "b", "t": 3.4}, {"name": "c", "t": 2.0}]')
print([o["name"] for o in sorted(items, key=lambda o: o["t"], reverse=True)[:2]])
```

Вывод: `['b', 'c']`.

## Индекс по полю

```python
import json
data = json.loads('[{"id": 1, "n": "a"}, {"id": 2, "n": "b"}]')
by_id = {obj["id"]: obj for obj in data}
print(by_id[2]["n"])
```

- Словарь «id → объект» позволяет находить объект мгновенно, без перебора массива. Вывод: `b`.

## Среднее с защитой от пустого массива

```python
import json
items = json.loads("[]")
avg = round(sum(i["price"] for i in items) / len(items), 2) if items else None
print(avg)
```

- Для пустого массива деление на `len` дало бы `ZeroDivisionError`. Вывод: `None`.

## Итог

- Массив объектов после `loads` — список словарей.
- Фильтр — включение с `if`; сумма — `sum(o["f"] for o in ...)`.
- Подсчёт — `Counter` или словарь с `get`.
- Сортировка и `max` — с `key=lambda o: o["поле"]`.
- Индекс `{o["id"]: o for o in data}` — быстрый поиск.
- Пустой массив — проверяй перед делением.
'''),
    short=t(r'''
```py
[p["name"] for p in items if p["price"] < 400]
sum(p["price"] for p in items)
Counter(t["status"] for t in tests)
sorted(users, key=lambda u: u["age"])
max(users, key=lambda u: u["age"])
{o["id"]: o for o in data}              # индекс
```
'''),
    quiz=[
        q('Как отсортировать список объектов по полю "age"?',
            ['`sorted(users)`', '`sorted(users, key=lambda u: u["age"])`', '`users.sort("age")`', '`sorted(users["age"])`'],
            1, 'key — функция, вычисляющая поле.'),
        q('Зачем строить `{o["id"]: o for o in data}`?',
            ['Для красоты', 'Для быстрого поиска объекта по id', 'Чтобы отсортировать', 'Чтобы удалить дубли'],
            1, 'Поиск по ключу — мгновенный.'),
        q('Что случится при `sum(...) / len(items)` для пустого массива?',
            ['0', '`ZeroDivisionError`', 'None', 'nan'],
            1, 'Проверяй пустоту заранее.'),
    ],
),

# ---------- jsn-m2-l3 ----------
'jsn-m2-l3': dict(
    full=t(r'''
## Зачем это нужно

Для запросов к API нужно **собирать** JSON: тело POST-запроса, обновление объекта, сообщение в очередь. Схема всегда одна: собрать или изменить обычный словарь Python, а в конце превратить его в строку через `dumps`.

## Собрать тело запроса

```python
import json
payload = {"name": "Аня", "roles": ["qa"]}
payload["roles"].append("admin")
payload["active"] = True
print(json.dumps(payload, ensure_ascii=False))
```

- Работаем со словарём: добавляем, меняем, дополняем списки.
- `dumps` — последним шагом, перед отправкой. Вывод: `{"name": "Аня", "roles": ["qa", "admin"], "active": true}`.

## Изменить JSON-строку

JSON-строку нельзя «поменять на месте» — это просто текст. Схема: **разобрать → изменить → собрать**.

```python
import json
text = '{"count": 1}'
data = json.loads(text)
data["count"] += 1
text = json.dumps(data)
print(text)
```

Вывод: `{"count": 2}`.

```python
import json
original = '{"a": 1, "b": {"c": 2}}'
data = json.loads(original)
data["b"]["c"] = 99
print(original)
print(json.dumps(data))
```

- `loads` создаёт **новые** объекты; исходная строка остаётся прежней.
- Вывод: исходная строка без изменений, затем `{"a": 1, "b": {"c": 99}}`.

## Типичные преобразования

```python
import json
data = json.loads('{"userName": "a", "id": 1, "email": null, "version": 3}')
data["user_name"] = data.pop("userName")
data = {k: v for k, v in data.items() if v is not None}
data["version"] = data.get("version", 0) + 1
print(json.dumps(data))
```

- Переименование ключа — `pop` + присваивание (новый ключ окажется в конце).
- Удаление `null` — словарное включение.
- Увеличение счётчика с умолчанием — `get(ключ, 0) + 1`.
- Вывод: `{"id": 1, "version": 4, "user_name": "a"}`.

## Слияние двух JSON

```python
import json
a = '{"b": 1, "a": 1}'
b = '{"a": 2, "c": 3}'
merged = {**json.loads(a), **json.loads(b)}
print(json.dumps(merged, sort_keys=True))
```

- Разобрали оба, слили словари (правый важнее), собрали с сортировкой ключей. Вывод: `{"a": 2, "b": 1, "c": 3}`.

## Итог

- Собирай словарь Python, `dumps` — в конце.
- Изменение JSON-строки: `loads` → правка словаря → `dumps`.
- Исходная строка после `loads` не меняется.
- Переименование, удаление `null`, счётчики, слияние — обычные операции со словарями.
'''),
    short=t(r'''
```py
data = json.loads(text)      # разобрать
data["count"] += 1           # изменить словарь
text = json.dumps(data)      # собрать заново
data[new] = data.pop(old)    # переименовать
{k: v for k, v in data.items() if v is not None}   # убрать null
{**json.loads(a), **json.loads(b)}                  # слить
```
'''),
    quiz=[
        q('Как «увеличить поле» в JSON-строке?',
            ['Заменить подстроку', 'loads → изменить словарь → dumps', 'text["count"] += 1', 'Нельзя'],
            1, 'JSON-строка — текст.'),
        q('Меняется ли исходная строка после `data = json.loads(text); data["a"] = 5`?',
            ['Да', 'Нет — loads создал новые объекты', 'Только a', 'Ошибка'],
            1, 'Строки неизменяемы.'),
        q('Что выведет `json.dumps({"x": None})`?',
            ['`{"x": None}`', '`{"x": null}`', '`{}`', 'Ошибка'],
            1, 'None → null.'),
    ],
),

# ---------- jsn-m2-l4 ----------
'jsn-m2-l4': dict(
    full=t(r'''
## Зачем это нужно

JSON часто лежит в **файлах**: тестовые данные, конфиги, ожидаемые ответы («эталоны»), отчёты о прогоне. Для файлов в модуле `json` есть пара функций без буквы `s` на конце: `dump` пишет в файл, `load` читает из файла.

## dump и load

```python
import json, io
buffer = io.StringIO()
json.dump({"a": 1}, buffer)
print(buffer.getvalue())
buffer.seek(0)
print(json.load(buffer))
```

- `json.dump(объект, файл)` — записать JSON в открытый файл (у `dumps` — вернуть строку).
- `json.load(файл)` — прочитать и разобрать JSON из файла (у `loads` — из строки).
- `io.StringIO` — «файл в памяти»: ведёт себя как файл, но ничего не пишет на диск. Удобен для примеров и тестов.
- `getvalue()` — всё содержимое; `seek(0)` — вернуться в начало, чтобы читать.
- Вывод: `{"a": 1}`, `{'a': 1}`.

С настоящим файлом это выглядит так (подробно — тема «Файлы»):

```py
with open("users.json", "w", encoding="utf-8") as f:
    json.dump(users, f, ensure_ascii=False, indent=2)

with open("users.json", encoding="utf-8") as f:
    users = json.load(f)
```

- `open(путь, "w")` — открыть для записи, без режима — для чтения.
- `encoding="utf-8"` — обязательно для кириллицы.
- `with` сам закроет файл (тема «Контекстные менеджеры»).
- `dump` принимает те же параметры, что `dumps`: `indent`, `ensure_ascii`, `sort_keys`.

## Чтение массива из файла

```python
import json, io
f = io.StringIO('[{"id": 1}, {"id": 2}]')
data = json.load(f)
print(len(data), data[-1]["id"])
```

Вывод: `2 2`.

## JSON Lines: объект на строку

Большие логи и выгрузки пишут в формате JSON Lines — каждая строка отдельный JSON. Его читают **построчно** через `loads`, а не целиком через `load`:

```python
import json, io
f = io.StringIO('{"id": 1}\n{"id": 2}\n\n{"id": 3}\n')
rows = [json.loads(line) for line in f if line.strip()]
print([r["id"] for r in rows])
```

- Перебор файла идёт по строкам; пустые строки пропускаем через `line.strip()`.
- Вывод: `[1, 2, 3]`.

Запись JSON Lines — `dumps` для каждого объекта и перевод строки:

```python
import json, io
buf = io.StringIO()
for r in [{"id": 1}, {"id": 2}]:
    buf.write(json.dumps(r) + "\n")
print(repr(buf.getvalue()))
```

Вывод: `'{"id": 1}\n{"id": 2}\n'`.

## Итог

- `dump(obj, f)` / `load(f)` — файлы; `dumps(obj)` / `loads(s)` — строки.
- Для кириллицы — `encoding="utf-8"` при открытии и `ensure_ascii=False`.
- `io.StringIO` — файл в памяти для примеров и тестов.
- JSON Lines читают построчно `loads`, пишут `dumps(...) + "\n"`.
'''),
    short=t(r'''
```py
json.dump(data, f, ensure_ascii=False, indent=2)   # в файл
data = json.load(f)                                 # из файла
with open("x.json", encoding="utf-8") as f: ...
[json.loads(line) for line in f if line.strip()]    # JSON Lines
f.write(json.dumps(r) + "\n")
io.StringIO()                                       # файл в памяти
```
'''),
    quiz=[
        q('Чем `json.load` отличается от `json.loads`?',
            ['Ничем', 'load читает из файла, loads — из строки', 'load быстрее', 'loads — из файла'],
            1, 's — string.'),
        q('Как читать файл JSON Lines?',
            ['json.load(f)', 'Построчно json.loads(line)', 'f.read().split()', 'Нельзя'],
            1, 'Каждая строка — отдельный JSON.'),
        q('Зачем `encoding="utf-8"` при открытии JSON-файла с кириллицей?',
            ['Быстрее', 'Чтобы символы прочитались и записались правильно', 'Так требует json', 'Не нужно'],
            1, 'Иначе возможны ошибки кодировки.'),
    ],
),
}
