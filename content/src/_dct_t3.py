"""Теория модуля «Словари в реальных задачах» темы «Словари».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- dct-m3-l1: Вложенные словари ----------
'dct-m3-l1': dict(
    full=t(r'''
## Зачем это нужно

Реальные данные вложенные: ответ API содержит `data`, в нём `user`, в нём `address`; конфиг — окружения, в каждом — адреса и настройки. В Python это словари внутри словарей (и списки внутри них). Нужно уметь безопасно доставать значения на любой глубине и создавать вложенность.

## Доступ по цепочке

```python
resp = {"status": 200, "data": {"user": {"name": "Аня", "roles": ["qa", "admin"]}}}
user = resp["data"]["user"]
print(user["name"], user["roles"][-1])
print(resp.get("meta", {}).get("page", 1))
```

- `resp["data"]["user"]` — последовательные обращения: сначала `resp["data"]` (словарь), у него `["user"]`.
- Промежуточный результат удобно сохранить в переменную.
- `resp.get("meta", {})` — если ключа нет, вернётся пустой словарь, у которого снова можно вызвать `get`. Так строят **безопасную цепочку** без `KeyError`.
- Вывод: `Аня admin`, `1`.

## Изменение вложенного

```python
users = {"anna": {"age": 25, "skills": ["qa"]}}
users["anna"]["skills"].append("sql")
users["bob"] = {"age": 30, "skills": []}
print(users["anna"], len(users))
print([name for name, info in users.items() if info["age"] > 26])
```

- Добраться до нужного уровня и изменить — как обычно.
- Вывод: `{'age': 25, 'skills': ['qa', 'sql']} 2`, `['bob']`.

## Перебор вложенного

```python
config = {"env": {"staging": {"url": "https://stg"}, "prod": {"url": "https://prod"}}}
for name, settings in config["env"].items():
    print(name, settings["url"])
```

Вывод: `staging https://stg`, `prod https://prod`.

## Путь из списка ключей

```python
def get_path(d, path, default=None):
    current = d
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current

cfg = {"db": {"main": {"host": "localhost"}}}
print(get_path(cfg, ["db", "main", "host"]), get_path(cfg, ["db", "replica", "host"], "-"))
```

- Идём по ключам, «спускаясь» на уровень ниже; если ключа нет или значение — не словарь, возвращаем умолчание.
- Вывод: `localhost -`.

## Создание вложенности: setdefault

```python
d = {}
path = ["a", "b", "c"]
current = d
for key in path[:-1]:
    current = current.setdefault(key, {})
current[path[-1]] = 1
print(d)
```

- `setdefault(key, {})` вернёт существующий подсловарь или создаст пустой. Последний ключ получает значение.
- Вывод: `{'a': {'b': {'c': 1}}}`.

## Рекурсия по вложенности

```python
def flatten_dict(d, prefix=""):
    flat = {}
    for key, value in d.items():
        full = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten_dict(value, full))
        else:
            flat[full] = value
    return flat

print(flatten_dict({"a": 1, "b": {"c": 2, "d": {"e": 3}}}))
```

- Если значение — словарь, обрабатываем его той же функцией с удлинённым префиксом.
- Вывод: `{'a': 1, 'b.c': 2, 'b.d.e': 3}` — так конфиги превращают в плоские переменные окружения.

## Итог

- `d["a"]["b"]` — доступ по цепочке; `KeyError` на любом уровне.
- `d.get("a", {}).get("b")` — безопасная цепочка.
- `setdefault(k, {})` — создать промежуточный уровень.
- Путь списком ключей — цикл со «спуском»; произвольная глубина — рекурсия.
'''),
    short=t(r'''
```py
resp["data"]["user"]["name"]              # KeyError на любом уровне
resp.get("data", {}).get("user", {}).get("name")   # безопасно
current = current.setdefault(key, {})     # создать уровень
isinstance(value, dict)                   # спускаться ли глубже
```
'''),
    quiz=[
        q('Что вернёт `{"a": {}}.get("a", {}).get("b", 0)`?',
            ['`KeyError`', '`0`', '`{}`', '`None`'],
            1, 'Безопасная цепочка get.'),
        q('Что делает `d.setdefault("x", {})`?',
            ['Всегда создаёт новый словарь', 'Возвращает d["x"], создав {} при отсутствии', 'Удаляет x', 'Ошибка'],
            1, 'Создаёт только если ключа нет.'),
        q('Как обойти словарь произвольной вложенности?',
            ['Двумя циклами', 'Рекурсией', 'Нельзя', 'Через sorted'],
            1, 'Глубина заранее неизвестна.'),
    ],
),

# ---------- dct-m3-l2: Слияние и копирование ----------
'dct-m3-l2': dict(
    full=t(r'''
## Зачем это нужно

Настройки по умолчанию + переопределения, шаблон тестового пользователя + уникальные поля — постоянные задачи со словарями. Важно уметь слить словари и **не испортить** исходные: мелкая копия и присваивание второго имени ведут себя совсем не так, как кажется.

## Второе имя — не копия

```python
a = {"x": 1}
b = a
c = dict(a)
b["y"] = 2
print(a, c, a is b, a is c)
```

- `b = a` — второе имя для **того же** словаря: изменение через `b` видно через `a`.
- `dict(a)` (или `a.copy()`) — новый словарь с теми же парами.
- Вывод: `{'x': 1, 'y': 2} {'x': 1} True False`.

## Слияние

```python
defaults = {"timeout": 30, "browser": "chrome", "headless": True}
overrides = {"browser": "firefox", "retries": 2}
print({**defaults, **overrides})
print(defaults | overrides == {**defaults, **overrides})
print(defaults)
```

- `{**a, **b}` — новый словарь: сначала пары `a`, потом `b`; совпадающие ключи берутся из `b` (правый важнее).
- `a | b` (Python 3.9+) — то же самое; `a |= b` — обновить `a` на месте, как `a.update(b)`.
- Исходные словари не меняются. Вывод: объединённый словарь, `True`, неизменённый `defaults`.

Добавить одну пару в копию: `{**d, "key": value}`.

Слить список словарей:

```python
result = {}
for d in [{"a": 1}, {"b": 2}, {"a": 3}]:
    result.update(d)
print(result)
```

Вывод: `{'a': 3, 'b': 2}`.

## Мелкая копия и глубокая

```python
import copy
original = {"name": "Аня", "tags": ["qa"]}
shallow = original.copy()
deep = copy.deepcopy(original)
shallow["tags"].append("admin")
shallow["name"] = "Боря"
print(original)
print(deep)
```

- `copy()` / `dict(d)` / `{**d}` — **мелкие** копии: новый словарь, но значения — те же объекты. Список `tags` у `original` и `shallow` **общий**.
- Замена значения (`shallow["name"] = ...`) на оригинал не влияет, а изменение общего списка — влияет.
- `copy.deepcopy(d)` рекурсивно копирует всё, включая вложенные списки и словари.
- Вывод: `{'name': 'Аня', 'tags': ['qa', 'admin']}`, `{'name': 'Аня', 'tags': ['qa']}`.

Правило: если в словаре есть изменяемые значения (списки, словари) и ты их меняешь — нужен `deepcopy`.

## Рекурсивное слияние

```python
def deep_merge(base, override):
    result = dict(base)
    for key, value in override.items():
        if isinstance(result.get(key), dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

base = {"db": {"host": "localhost", "port": 5432}, "debug": False}
print(deep_merge(base, {"db": {"host": "stg-db"}, "debug": True}))
```

- Обычное слияние заменило бы весь `db` и потеряло `port`. Рекурсия сливает вложенные словари по ключам.
- Вывод: `{'db': {'host': 'stg-db', 'port': 5432}, 'debug': True}`.

## Итог

- `b = a` — то же самое; `dict(a)`, `a.copy()`, `{**a}` — мелкая копия.
- `{**a, **b}` и `a | b` — новый объединённый словарь (правый важнее); `a.update(b)` — на месте.
- Вложенные изменяемые значения при мелкой копии общие — `copy.deepcopy`.
- Вложенные конфиги сливают рекурсивно.
'''),
    short=t(r'''
```py
b = a                     # то же самое!
c = dict(a)               # мелкая копия (a.copy(), {**a})
{**defaults, **overrides} # слияние, правый важнее
defaults | overrides      # то же (3.9+)
a.update(b)               # на месте
{**d, "key": value}       # копия + пара
import copy; copy.deepcopy(d)   # глубокая копия
```
'''),
    quiz=[
        q('Что будет в `a` после `a = {"x": 1}; b = a; b["y"] = 2`?',
            ['`{"x": 1}`', '`{"x": 1, "y": 2}`', 'Ошибка', '`{"y": 2}`'],
            1, 'b — второе имя того же словаря.'),
        q('Что вернёт `{**{"a": 1}, **{"a": 2}}`?',
            ['`{"a": 1}`', '`{"a": 2}`', 'Ошибка', '`{"a": [1, 2]}`'],
            1, 'Правый словарь важнее.'),
        q('Когда нужен `copy.deepcopy`?',
            ['Всегда', 'Если меняешь вложенные изменяемые значения копии', 'Для пустых словарей', 'Никогда'],
            1, 'Мелкая копия разделяет вложенные объекты.'),
    ],
),

# ---------- dct-m3-l3: Словарные включения ----------
'dct-m3-l3': dict(
    full=t(r'''
## Зачем это нужно

**Словарное включение** — короткая запись «построй словарь из коллекции»: отфильтровать поля, переименовать ключи, построить индекс по id, перевернуть словарь. Это тот же цикл с `d[k] = v`, записанный в одну строку.

## Синтаксис

```python
names = ["api", "ui", "docker"]
print({n: len(n) for n in names})
prices = {"чай": 300, "кофе": 500, "сок": 150}
print({k: v for k, v in prices.items() if v >= 300})
```

- `{ключ: значение for элемент in коллекция}` — для каждого элемента вычисляется пара.
- `if условие` в конце — фильтр.
- Вывод: `{'api': 3, 'ui': 2, 'docker': 6}`, `{'чай': 300, 'кофе': 500}`.

Эквивалентный цикл:

```python
lengths = {}
for n in ["api", "ui"]:
    lengths[n] = len(n)
print(lengths)
```

Вывод: `{'api': 3, 'ui': 2}`.

## Преобразования

```python
codes = {"OK": 200, "Created": 201, "Not Found": 404}
by_code = {code: text for text, code in codes.items()}
print(by_code[404])
print({k.lower(): v for k, v in codes.items()})
```

- Поменять ключи и значения местами — «перевернуть» словарь (значения должны быть уникальными, иначе останется последний).
- Изменить ключи или значения — вычислить их в выражении.
- Вывод: `Not Found`, `{'ok': 200, 'created': 201, 'not found': 404}`.

## Выражение со значением-условием

```python
nums = [1, 2, 3, 4]
print({n: n * n for n in nums if n % 2 == 0})
print({x: ("чёт" if x % 2 == 0 else "нечет") for x in range(3)})
```

- `if` в **конце** — фильтр (какие элементы брать).
- `a if условие else b` в **значении** — выбор значения для каждого элемента.
- Вывод: `{2: 4, 4: 16}`, `{0: 'чёт', 1: 'нечет', 2: 'чёт'}`.

## Типичные задачи

```python
users = [{"id": 1, "name": "Аня"}, {"id": 2, "name": "Боря"}]
index = {u["id"]: u for u in users}
print(index[2]["name"])
d = {"a": 1, "b": None, "c": 0}
print({k: v for k, v in d.items() if v is not None})
print({k: v for k, v in {"id": 1, "password": "x"}.items() if k in ["id"]})
```

- **Индекс по id**: поиск пользователя по номеру становится мгновенным, без перебора списка.
- Убрать `None`, но оставить `0` — проверка `is not None`.
- Оставить только разрешённые ключи.
- Вывод: `Боря`, `{'a': 1, 'c': 0}`, `{'id': 1}`.

## Ключи из функции

```python
def to_snake(key):
    return "".join("_" + ch.lower() if ch.isupper() else ch for ch in key)

print({to_snake(k): v for k, v in {"userName": "Аня", "createdAt": 2024}.items()})
```

- Сложное преобразование выносят в функцию, а включение остаётся коротким.
- Вывод: `{'user_name': 'Аня', 'created_at': 2024}`.

## Итог

- `{k: v for x in коллекция}` — новый словарь; `if` в конце — фильтр.
- `a if cond else b` — условие в значении.
- Частые приёмы: инверсия, индекс по полю, фильтр ключей/значений, переименование.
- Сложную логику — в функцию, включение — короткое.
'''),
    short=t(r'''
```py
{n: len(n) for n in names}
{k: v for k, v in d.items() if v is not None}   # фильтр
{v: k for k, v in d.items()}                    # инверсия
{u["id"]: u for u in users}                     # индекс по id
{k.lower(): v for k, v in d.items()}            # переименование
{x: ("чёт" if x % 2 == 0 else "нечет") for x in range(3)}
```
'''),
    quiz=[
        q('Что вернёт `{x: x * 2 for x in range(3)}`?',
            ['`{0: 0, 1: 2, 2: 4}`', '`[0, 2, 4]`', '`{0, 2, 4}`', 'Ошибка'],
            0, 'Пары ключ: значение.'),
        q('Как оставить в словаре только пары со значением больше 0?',
            ['`{k: v for k, v in d if v > 0}`', '`{k: v for k, v in d.items() if v > 0}`', '`d.filter(v > 0)`', '`[v for v in d if v > 0]`'],
            1, 'Перебор d.items() и фильтр.'),
        q('Что получится при инверсии `{"a": 1, "b": 1}`?',
            ['`{1: "a"}`', '`{1: "b"}`', 'Ошибка', '`{1: ["a", "b"]}`'],
            1, 'Повторяющийся ключ — побеждает последний.'),
    ],
),

# ---------- dct-views: Сравнение словарей ----------
'dct-views': dict(
    full=t(r'''
## Зачем это нужно

В тестировании постоянно сравнивают словари: ожидаемый ответ API с фактическим, конфиг до и после изменения. Равенство `==` отвечает только «да/нет», а нужно понять **что** отличается: каких полей не хватает, какие лишние, какие изменились. Представления `keys()` и `items()` умеют работать как **множества** — это делает такие сравнения короткими.

## keys() — как множество

```python
a = {"x": 1, "y": 2, "z": 3}
b = {"y": 20, "z": 3, "w": 4}
print(sorted(a.keys() & b.keys()))
print(sorted(a.keys() - b.keys()), sorted(a.keys() | b.keys()))
```

- `&` — пересечение: ключи, которые есть в **обоих**.
- `-` — разность: есть в `a`, но нет в `b`.
- `|` — объединение: все ключи из обоих.
- Результат — множество (без порядка), поэтому для стабильного вывода используем `sorted`.
- Вывод: `['y', 'z']`, `['x'] ['w', 'x', 'y', 'z']`.

## Живое представление

```python
d = {"a": 1}
keys = d.keys()
print(type(keys).__name__, "a" in keys)
d["b"] = 2
print(len(keys))
```

- `dict_keys` — представление, которое видит изменения словаря. Вывод: `dict_keys True`, `2`.

## Недостающие и лишние поля

```python
expected = {"id": 1, "name": "a", "email": "b"}
actual = {"id": 1, "debug": True}
print(sorted(expected.keys() - actual.keys()), sorted(actual.keys() - expected.keys()))
```

- «Не хватает» — ожидаемые минус фактические; «лишние» — наоборот.
- Вывод: `['email', 'name'] ['debug']`.

## Изменённые значения

```python
a = {"x": 1, "y": 2}
b = {"x": 1, "y": 3}
changed = [k for k in a if k in b and a[k] != b[k]]
print(changed, a.items() & b.items())
```

- Изменённые — ключ есть в обоих, значения разные.
- `a.items() & b.items()` — пары, совпадающие полностью (ключ **и** значение). Работает, если значения хешируемые.
- Вывод: `['y'] {('x', 1)}`.

## Полный отчёт о различиях

```python
before = {"a": 1, "b": 2, "x": 0}
after = {"b": 3, "c": 4, "x": 0}
common = before.keys() & after.keys()
print({
    "added": sorted(after.keys() - before.keys()),
    "removed": sorted(before.keys() - after.keys()),
    "changed": sorted(k for k in common if before[k] != after[k]),
})
```

- Вывод: `{'added': ['c'], 'removed': ['a'], 'changed': ['b']}` — такой «дифф» удобно печатать в сообщении упавшего теста.

## Итог

- `keys()` и `items()` поддерживают операции множеств: `&`, `-`, `|`.
- Не хватает: `expected.keys() - actual.keys()`; лишние: наоборот.
- Изменённые: общие ключи с разными значениями.
- Совпадающие пары: `a.items() & b.items()`.
- Множества без порядка — для вывода `sorted(...)`.
'''),
    short=t(r'''
```py
a.keys() & b.keys()        # общие ключи
a.keys() - b.keys()        # есть в a, нет в b
a.keys() | b.keys()        # все
a.items() & b.items()      # совпадающие пары
[k for k in a.keys() & b.keys() if a[k] != b[k]]   # изменённые
```
'''),
    quiz=[
        q('Что вернёт `{"a": 1, "b": 2}.keys() - {"b": 5}.keys()`?',
            ['`{"b"}`', '`{"a"}`', '`{"a", "b"}`', 'Ошибка'],
            1, 'Разность множеств ключей.'),
        q('Как найти ключи, которые есть в обоих словарях?',
            ['`a.keys() | b.keys()`', '`a.keys() & b.keys()`', '`a == b`', '`a.keys() - b.keys()`'],
            1, 'Пересечение.'),
        q('Что даёт `a.items() & b.items()`?',
            ['Общие ключи', 'Пары, совпадающие и по ключу, и по значению', 'Все пары', 'Ошибка'],
            1, 'Пересечение пар.'),
    ],
),

# ---------- dct-api: Словари в проверках API ----------
'dct-api': dict(
    full=t(r'''
## Зачем это нужно

Главная работа тестировщика API — проверить ответ сервера: пришли ли нужные поля, правильных ли они типов, совпадают ли значения с ожидаемыми, нет ли лишнего. Ответ в формате JSON превращается в Python-словарь, и все проверки — это операции со словарями, которые ты уже знаешь.

## Базовые проверки

```python
resp = {"status": 200, "body": {"id": 7, "name": "Аня", "email": None}}
body = resp["body"]
print(resp["status"] == 200, set(body) == {"id", "name", "email"})
print([k for k, v in body.items() if v is None])
```

- Код ответа, **точный** набор полей (`set(body)` — множество ключей), поля со значением `null` (в Python — `None`).
- Вывод: `True True`, `['email']`.

## Проверка типов по схеме

```python
schema = {"id": int, "name": str}
body = {"id": "7", "name": "Аня"}
for field, typ in schema.items():
    print(field, isinstance(body[field], typ))
```

- **Схема** — словарь «поле → ожидаемый тип». Типы (`int`, `str`) — тоже объекты, их можно хранить в словаре и передавать в `isinstance`.
- Частый баг API: `id` пришёл строкой `"7"` вместо числа. Вывод: `id False`, `name True`.

Функция, собирающая все ошибки:

```python
def check_schema(body, schema):
    errors = []
    for field, typ in schema.items():
        if field not in body:
            errors.append(f"нет поля {field}")
        elif not isinstance(body[field], typ):
            errors.append(f"поле {field}: ожидали {typ.__name__}")
    return errors

print(check_schema({"id": "7"}, {"id": int, "name": str}))
```

- Лучше собрать **все** ошибки, чем упасть на первой — отчёт полезнее. `typ.__name__` — имя типа строкой.
- Вывод: `['поле id: ожидали int', 'нет поля name']`.

## Ожидаемое — подмножество ответа

Часто в ответе есть поля, которые меняются (`trace_id`, `timestamp`), и проверять нужно только часть:

```python
expected = {"status": "ok", "code": 200}
actual = {"status": "ok", "code": 200, "trace_id": "abc"}
print(expected.items() <= actual.items())
print(all(actual.get(k) == v for k, v in expected.items()))
```

- `<=` для `items()` — «все пары слева есть справа» (подмножество).
- Вариант через `all` работает и с нехешируемыми значениями. Но осторожно: `actual.get(k)` вернёт `None` и для отсутствующего ключа — если ожидается `None`, проверяй `k in actual`.
- Вывод: `True`, `True`.

## Игнорируемые поля

```python
def compare_responses(expected, actual, ignore):
    diffs = []
    for key in expected.keys() | actual.keys():
        if key in ignore:
            continue
        if key not in expected or key not in actual or expected[key] != actual[key]:
            diffs.append(key)
    return sorted(diffs)

print(compare_responses({"id": 1, "ts": 100, "a": 1}, {"id": 1, "ts": 200, "b": 2}, ["ts"]))
```

- Перебираем объединение ключей, пропускаем игнорируемые, отсутствие ключа с любой стороны — тоже различие.
- Вывод: `['a', 'b']`.

## Логи без секретов

```python
def mask_secrets(d):
    result = {}
    for key, value in d.items():
        lowered = key.lower()
        result[key] = "***" if "token" in lowered or "password" in lowered else value
    return result

print(mask_secrets({"user": "a", "Password": "x", "access_token": "y"}))
```

- Пароли и токены нельзя писать в логи и отчёты. Новый словарь — чтобы не испортить данные, которые ещё нужны.
- Вывод: `{'user': 'a', 'Password': '***', 'access_token': '***'}`.

## Итог

- Ответ API — словарь; проверки: код, набор полей (`set(body)`), значения, `None`.
- Схема `{поле: тип}` + `isinstance` — проверка типов; собирай все ошибки списком.
- Частичное совпадение: `expected.items() <= actual.items()` или `all(...)`.
- Изменчивые поля (время, id трассировки) исключай из сравнения.
- Секреты маскируй перед логированием.
'''),
    short=t(r'''
```py
set(body) == {"id", "name"}              # точный набор полей
isinstance(body[f], typ)                 # тип по схеме {поле: тип}
expected.items() <= actual.items()       # подмножество
all(actual.get(k) == v for k, v in expected.items())
for key in expected.keys() | actual.keys(): ...   # сравнение с ignore
"***" if "token" in key.lower() else value        # маскировка
```
'''),
    quiz=[
        q('Как проверить, что в ответе ровно поля id и name?',
            ['`"id" in body`', '`set(body) == {"id", "name"}`', '`len(body) == 2`', '`body == {"id", "name"}`'],
            1, 'Множество ключей.'),
        q('Что означает `expected.items() <= actual.items()`?',
            ['Словари равны', 'Все пары expected есть в actual', 'actual меньше', 'Ошибка'],
            1, 'Проверка подмножества.'),
        q('Почему лучше собирать все ошибки схемы в список, а не падать на первой?',
            ['Быстрее', 'Отчёт сразу показывает все проблемы', 'Так требует Python', 'Без разницы'],
            1, 'Полезнее для разбора бага.'),
    ],
),
}
