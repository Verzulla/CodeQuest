"""Теория темы «Словари»: краткая (short), подробная (full) и «Проверь себя» (quiz)
для каждого урока. build.py подставляет её в уроки content/src/py_dicts.py."""
from ._lib import q, t

THEORY = {

# ---------- dct-m1-l1: Создание и доступ по ключу ----------
'dct-m1-l1': dict(
    short=t(r'''
# Словарь (dict)

```
user = {"name": "Аня", "age": 25, "role": "qa"}
user["name"]        # "Аня"
user["email"]       # KeyError — такого ключа нет
"age" in user       # True — проверка ключа
len(user)           # 3
```

- Пары **ключ → значение**; поиск по ключу мгновенный.
- Ключи уникальные и хешируемые (строки, числа, кортежи).
- Порядок вставки сохраняется (Python 3.7+).
'''),
    full=t(r'''
## Зачем это нужно

Словарь — вторая по важности структура данных в Python после списка. Он хранит пары «ключ → значение» и мгновенно находит значение по ключу. JSON-ответы API — это словари; настройки, счётчики, кэши, группировки — тоже словари. Для тестировщика это основной инструмент проверки ответов.

## Как это работает

### Создание

```py
user = {"name": "Аня", "age": 25}
empty = {}                          # пустой словарь (не множество!)
pairs = dict([("a", 1), ("b", 2)])
kw = dict(name="Аня", age=25)
```

### Ключи

- Уникальны: повтор ключа перезаписывает значение.
- Должны быть **хешируемыми**: `str`, `int`, `float`, `bool`, `tuple` из неизменяемых. Список ключом быть не может.
- Значения — что угодно, включая списки и другие словари.

### Доступ

- `d[key]` — значение; если ключа нет — `KeyError`.
- `key in d` — проверка **ключа** (не значения!).
- `len(d)` — число пар.

Поиск по ключу работает за постоянное время независимо от размера словаря — в отличие от поиска в списке.

### Порядок

С Python 3.7 словари сохраняют порядок вставки ключей.

## Примеры

### Пример 1. Создание и доступ

```python
user = {"name": "Аня", "age": 25, "tags": ["qa", "admin"]}
print(user["name"], user["tags"][0])
print("age" in user, "Аня" in user)      # in проверяет ключи
print(len(user), list(user))
```

### Пример 2. KeyError

```python
resp = {"id": 1, "name": "Аня"}
try:
    print(resp["email"])
except KeyError as e:
    print("KeyError:", e)
```

### Пример 3. Разные ключи

```python
lookup = {200: "OK", "admin": True, (0, 0): "старт", 3.5: "дробь"}
print(lookup[200], lookup["admin"], lookup[(0, 0)])
try:
    bad = {[1, 2]: "x"}
except TypeError as e:
    print("TypeError:", e)
```

### Пример 4. Проверка обязательных полей

```python
required = ["id", "name", "email"]
resp = {"id": 1, "name": "Аня"}
missing = [k for k in required if k not in resp]
print("не хватает:", missing)
```

## Частые ошибки

**`d[key]` без уверенности, что ключ есть** — `KeyError`.

**`value in d`** — проверяет ключи, а не значения; для значений — `in d.values()`.

**`{}` для пустого множества** — это пустой словарь; множество — `set()`.

## Шпаргалка

```py
d = {"k": "v"}
d["k"]        # значение или KeyError
"k" in d      # есть ли ключ
len(d)
dict(a=1, b=2)
```
'''),
    quiz=[
        q('Что вернёт `"Аня" in {"name": "Аня"}`?',
            ['`True`', '`False`', 'Ошибка', '`"name"`'],
            1, '`in` для словаря проверяет ключи.'),
        q('Что будет в `d` после `d = {"a": 1, "a": 2}`?',
            ["`{'a': 1}`", "`{'a': 2}`", 'Ошибка', "`{'a': [1, 2]}`"],
            1, 'Ключ уникален, последнее значение перезаписывает.'),
        q('Что создаёт `{}`?',
            ['Пустое множество', 'Пустой словарь', 'Пустой кортеж', 'Ошибку'],
            1, 'Пустое множество — `set()`.'),
    ],
),

# ---------- dct-m1-l2: Добавление, изменение, удаление ----------
'dct-m1-l2': dict(
    short=t(r'''
# Изменение словаря

```
d["email"] = "a@b.ru"      # добавить или перезаписать
d.update({"age": 26, "city": "Казань"})   # несколько сразу
del d["city"]              # удалить (KeyError, если нет)
value = d.pop("age")       # удалить и вернуть
d.pop("x", None)           # без ошибки, если ключа нет
d.clear()                  # очистить
```
'''),
    full=t(r'''
## Зачем это нужно

Словари живут и меняются: добавляем поля к тестовым данным, убираем секреты перед логированием, обновляем настройки, переименовываем ключи при переходе API на новый формат. Важно знать, какие операции падают на отсутствующем ключе, а какие — нет.

## Как это работает

### Добавление и изменение

- `d[key] = value` — добавит новый ключ или перезапишет существующий.
- `d.update(other)` — добавит/перезапишет все пары из другого словаря (или из именованных аргументов: `d.update(age=26)`).

### Удаление

- `del d[key]` — `KeyError`, если ключа нет.
- `d.pop(key)` — удаляет и **возвращает** значение; `KeyError`, если нет.
- `d.pop(key, default)` — без ошибки: вернёт `default`.
- `d.popitem()` — удалить последнюю добавленную пару.
- `d.clear()` — всё.

### Изменение во время перебора

Нельзя добавлять/удалять ключи, перебирая тот же словарь: `RuntimeError: dictionary changed size during iteration`. Перебирай копию: `for k in list(d):`.

### Новый словарь вместо изменения

`{**d, "key": v}` или `d | {"key": v}` (Python 3.9+) — новый словарь, исходный не меняется.

## Примеры

### Пример 1. Добавление и обновление

```python
payload = {"name": "Аня"}
payload["email"] = "anna@mail.ru"
payload.update({"role": "qa", "name": "Анна"})
payload.update(active=True)
print(payload)
```

### Пример 2. Безопасное удаление

```python
log_data = {"user": "anna", "password": "secret", "token": "abc"}
for key in ["password", "token", "api_key"]:
    removed = log_data.pop(key, None)
    print(key, "->", "удалён" if removed is not None else "не было")
print(log_data)
```

### Пример 3. Изменение во время перебора

```python
d = {"a": 1, "b": 0, "c": 2}
try:
    for k in d:
        if d[k] == 0:
            del d[k]
except RuntimeError as e:
    print("RuntimeError:", e)
d = {"a": 1, "b": 0, "c": 2}
for k in list(d):
    if d[k] == 0:
        del d[k]
print(d)
```

### Пример 4. Новый словарь

```python
base = {"Accept": "application/json"}
with_auth = {**base, "Authorization": "Bearer x"}
also = base | {"X-Id": "1"}
print(base, with_auth, also, sep="\n")
```

## Частые ошибки

**`del d[k]` для отсутствующего ключа** — используй `pop(k, None)`.

**Удаление ключей во время перебора словаря.**

**Ожидание, что `update` вернёт словарь** — возвращает `None`.

## Шпаргалка

```py
d[k] = v;  d.update(x=1)
del d[k];  v = d.pop(k);  d.pop(k, None)
{**d, k: v};  d | other
for k in list(d): ...
```
'''),
    quiz=[
        q('Что вернёт `{"a": 1}.pop("b", 0)`?',
            ['`KeyError`', '`0`', '`None`', '`1`'],
            1, 'С вторым аргументом pop возвращает значение по умолчанию вместо ошибки.'),
        q('Что вернёт `d.update({"x": 1})`?',
            ['Обновлённый словарь', '`None`', '`1`', '`True`'],
            1, 'update меняет словарь на месте и возвращает None.'),
        q('Как удалить ключи из словаря во время перебора без ошибки?',
            ['Перебирать `d` напрямую', 'Перебирать копию ключей: `for k in list(d):`', 'Использовать `while d`', 'Никак'],
            1, 'Изменять размер словаря во время перебора нельзя.'),
    ],
),

# ---------- dct-m1-l3: get и значения по умолчанию ----------
'dct-m1-l3': dict(
    short=t(r'''
# Безопасное чтение

```
d.get("email")              # None, если ключа нет
d.get("timeout", 30)        # 30, если ключа нет
d.setdefault("tags", [])    # вернуть значение; если нет — вставить [] и вернуть
```

⚠️ `get(key, default)` вернёт default, только если **ключа нет**. Если ключ есть со значением `None` — вернётся `None`.
'''),
    full=t(r'''
## Зачем это нужно

Данные почти никогда не бывают полными: у пользователя может не быть email, в настройках — таймаута, в ответе API — необязательного поля. `get` и `setdefault` позволяют работать с такими словарями без `KeyError` и без громоздких проверок `if key in d`.

## Как это работает

### get

- `d.get(key)` — значение или `None`.
- `d.get(key, default)` — значение или `default`.

Ловушка: default подставляется, только если **ключа нет**. Если ключ есть со значением `None`, вернётся `None`. Когда `None` означает «не задано», проверяй явно: `v = d.get(k); v = default if v is None else v`.

### setdefault

`d.setdefault(key, default)`:
- если ключ есть — вернуть его значение;
- если нет — вставить `default` и вернуть его.

Классический приём группировки: `groups.setdefault(role, []).append(name)`.

### defaultdict

`collections.defaultdict(list)` — словарь, который сам создаёт значение по умолчанию при обращении к отсутствующему ключу. Подробнее — в уроке про группировку.

## Примеры

### Пример 1. get с разными значениями

```python
cfg = {"browser": "chrome", "retries": 0, "proxy": None}
for key in ["browser", "retries", "proxy", "timeout"]:
    print(f"{key:8} get={cfg.get(key)!r:10} get(default)={cfg.get(key, 'DEF')!r}")
```

### Пример 2. Безопасный доступ к необязательным полям ответа

```python
users = [{"name": "Аня", "email": "a@b.ru"}, {"name": "Боря"}]
for u in users:
    print(u["name"], "—", u.get("email", "email не указан"))
```

### Пример 3. Группировка через setdefault

```python
results = [("login", "pass"), ("pay", "fail"), ("cart", "pass"), ("search", "skip")]
by_status = {}
for name, status in results:
    by_status.setdefault(status, []).append(name)
print(by_status)
```

### Пример 4. None как «не задано»

```python
def resolve(config, key, default):
    value = config.get(key)
    return default if value is None else value

cfg = {"retries": 0, "proxy": None}
print(resolve(cfg, "retries", 3), resolve(cfg, "proxy", "direct"), resolve(cfg, "timeout", 30))
```

## Частые ошибки

**`d.get(k) or default`** — заменит и `0`, `False`, `""`.

**Ожидание default для ключа со значением `None`.**

**`setdefault` с дорогим вычислением default** — оно вычисляется всегда, даже если ключ есть.

## Шпаргалка

```py
d.get(k)            # None, если нет
d.get(k, default)   # default, если нет
d.setdefault(k, []).append(x)   # группировка
v = d.get(k); v = default if v is None else v
```
'''),
    quiz=[
        q('Что вернёт `{"a": None}.get("a", 5)`?',
            ['`5`', '`None`', '`KeyError`', '`"a"`'],
            1, 'Ключ существует — возвращается его значение, даже None.'),
        q('Что делает `d.setdefault("k", [])`, если ключа `k` нет?',
            ['Возвращает None', 'Вставляет `[]` под ключом `k` и возвращает этот список', 'Бросает KeyError', 'Ничего'],
            1, 'setdefault вставляет default и возвращает его.'),
        q('Чем опасно `d.get("retries") or 3`?',
            ['Ничем', 'Если retries = 0, подставится 3', 'Будет KeyError', 'Вернёт строку'],
            1, '`or` заменяет любое ложное значение.'),
    ],
),

# ---------- dct-m2-l1: Перебор словаря ----------
'dct-m2-l1': dict(
    short=t(r'''
# Перебор

```
for key in d:                   # ключи
for value in d.values():        # значения
for key, value in d.items():    # пары
```

`d.keys()`, `d.values()`, `d.items()` — «представления», они отражают текущее состояние словаря.
'''),
    full=t(r'''
## Зачем это нужно

Просуммировать значения, найти упавшие тесты, вывести заголовки запроса, сравнить два ответа — всё это требует перебора словаря. Важно выбрать правильный способ: по ключам, по значениям или парами.

## Как это работает

- `for k in d:` — ключи (то же, что `d.keys()`).
- `for v in d.values():` — значения.
- `for k, v in d.items():` — пары, сразу с распаковкой. Самый частый вариант.

`keys()`, `values()`, `items()` возвращают **представления** (views): они не копируют данные и отражают изменения словаря. Представления ключей и пар поддерживают операции множеств: `d1.keys() & d2.keys()` — общие ключи.

Нужен список — `list(d.values())`.

Порядок перебора — порядок вставки.

## Примеры

### Пример 1. Три способа

```python
stats = {"passed": 42, "failed": 3, "skipped": 5}
print(list(stats), list(stats.values()), list(stats.items()))
for status, count in stats.items():
    print(f"{status:8} {count:3}")
print("всего:", sum(stats.values()))
```

### Пример 2. Стоимость корзины

```python
cart = {"чай": 2, "кофе": 1}
prices = {"чай": 300, "кофе": 500}
total = 0
for item, qty in cart.items():
    line = prices[item] * qty
    total += line
    print(f"{item}: {qty} × {prices[item]} = {line}")
print("итого:", total)
```

### Пример 3. Сравнение ключей двух ответов

```python
expected = {"id": 1, "name": "Аня", "email": "a@b.ru"}
actual = {"id": 1, "name": "Аня", "phone": "123"}
print("пропали:", expected.keys() - actual.keys())
print("лишние:", actual.keys() - expected.keys())
print("общие:", expected.keys() & actual.keys())
```

### Пример 4. Различия значений

```python
expected = {"status": "active", "role": "qa", "age": 25}
actual = {"status": "blocked", "role": "qa", "age": 25}
for key, exp in expected.items():
    act = actual.get(key)
    if act != exp:
        print(f"{key}: ожидали {exp!r}, получили {act!r}")
```

## Частые ошибки

**`for k, v in d:`** — без `.items()` распаковка ключа-строки даст ошибку или мусор.

**Изменение размера словаря во время перебора.**

**`d.values()[0]`** — представление не индексируется; нужно `list(d.values())[0]`.

## Шпаргалка

```py
for k in d: ...
for v in d.values(): ...
for k, v in d.items(): ...
d1.keys() - d2.keys()     # разница ключей
sum(d.values())
```
'''),
    quiz=[
        q('Что перебирает `for x in d.items():`?',
            ['Ключи', 'Значения', 'Пары (ключ, значение)', 'Индексы'],
            2, 'items() даёт кортежи-пары.'),
        q('Что вернёт `{"a": 1, "b": 2}.keys() - {"a": 0}.keys()`?',
            ["`{'b'}`", "`{'a'}`", 'Ошибка', "`['b']`"],
            0, 'Представления ключей поддерживают операции множеств.'),
        q('Можно ли обратиться к `d.values()[0]`?',
            ['Да', 'Нет, представление не индексируется; нужен list()', 'Только для строк', 'Только в Python 2'],
            1, 'values() — представление, а не список.'),
    ],
),

# ---------- dct-m2-l2: Подсчёт и группировка ----------
'dct-m2-l2': dict(
    short=t(r'''
# Счётчики

```
counts = {}
for x in items:
    counts[x] = counts.get(x, 0) + 1

from collections import Counter
Counter(items).most_common(2)
```

# Группировка

```
from collections import defaultdict
groups = defaultdict(list)
for user in users:
    groups[user["role"]].append(user["name"])
```
'''),
    full=t(r'''
## Зачем это нужно

«Сколько раз встречается каждая ошибка?», «какие тесты упали в каждом браузере?», «разбить пользователей по ролям» — подсчёт и группировка — самые частые задачи обработки данных. Словарь решает их идеально, а модуль `collections` даёт готовые инструменты.

## Как это работает

### Подсчёт вручную

```py
counts = {}
for x in items:
    counts[x] = counts.get(x, 0) + 1
```

### Counter

`collections.Counter(iterable)` — словарь-счётчик:
- `c[x]` — количество, для отсутствующего — `0` (без `KeyError`);
- `c.most_common(n)` — `n` самых частых пар `(элемент, количество)`;
- счётчики можно складывать и вычитать: `c1 + c2`.

### Группировка вручную

`groups.setdefault(key, []).append(item)`.

### defaultdict

`collections.defaultdict(factory)` — при обращении к отсутствующему ключу вызывает `factory()` и вставляет результат:
- `defaultdict(list)` — группировка;
- `defaultdict(int)` — счётчик (`d[x] += 1`);
- `defaultdict(set)` — уникальные элементы в группе.

Осторожно: даже **чтение** отсутствующего ключа создаёт его. Перед возвратом из функции часто превращают в обычный `dict`.

## Примеры

### Пример 1. Три способа посчитать

```python
from collections import Counter, defaultdict
results = ["pass", "fail", "pass", "skip", "pass"]

manual = {}
for r in results:
    manual[r] = manual.get(r, 0) + 1

auto = defaultdict(int)
for r in results:
    auto[r] += 1

print(manual, dict(auto), Counter(results), sep="\n")
```

### Пример 2. Топ ошибок из лога

```python
from collections import Counter
log = ["ERROR timeout", "INFO ok", "ERROR db down", "ERROR timeout", "ERROR timeout"]
errors = Counter(line.split(" ", 1)[1] for line in log if line.startswith("ERROR"))
for message, count in errors.most_common(2):
    print(f"{count} × {message}")
```

### Пример 3. Упавшие тесты по браузерам

```python
from collections import defaultdict
runs = [("chrome", "login", "pass"), ("firefox", "login", "fail"),
        ("chrome", "pay", "fail"), ("firefox", "pay", "fail")]
failed = defaultdict(list)
for browser, test, status in runs:
    if status == "fail":
        failed[browser].append(test)
print(dict(failed))
```

### Пример 4. Ловушка defaultdict

```python
from collections import defaultdict
d = defaultdict(list)
print("ops" in d)
_ = d["ops"]          # просто прочитали…
print("ops" in d, dict(d))
```

## Частые ошибки

**`counts[x] += 1` в обычном словаре** — `KeyError` для нового ключа.

**Чтение из defaultdict создаёт ключи** — неожиданные пустые группы.

**`most_common()` без аргумента** — вернёт все элементы, а не один.

## Шпаргалка

```py
d[k] = d.get(k, 0) + 1
Counter(xs).most_common(3)
g = defaultdict(list); g[key].append(x)
dict(g)                    # вернуть обычный словарь
```
'''),
    quiz=[
        q('Что вернёт `Counter(["a"])["b"]`?',
            ['`KeyError`', '`0`', '`None`', '`1`'],
            1, 'Counter возвращает 0 для отсутствующих элементов.'),
        q('Что создаст `defaultdict(list)` при обращении к новому ключу?',
            ['KeyError', 'Пустой список под этим ключом', 'None', 'Ничего'],
            1, 'Вызывается фабрика list() и результат вставляется.'),
        q('Что вернёт `Counter("aabbbc").most_common(1)`?',
            ["`['b']`", "`[('b', 3)]`", "`('b', 3)`", "`{'b': 3}`"],
            1, 'Список пар (элемент, количество).'),
    ],
),

# ---------- dct-m2-l3: Сортировка словарей ----------
'dct-m2-l3': dict(
    short=t(r'''
# Сортировка

```
sorted(d)                                       # ключи по алфавиту
sorted(d.items())                               # пары по ключу
sorted(d.items(), key=lambda p: p[1])           # пары по значению
sorted(d, key=d.get, reverse=True)              # ключи по убыванию значений
dict(sorted(d.items()))                         # новый упорядоченный словарь
```
'''),
    full=t(r'''
## Зачем это нужно

Словарь хранит данные, но выводить их часто нужно в определённом порядке: самые медленные тесты вверху, самые частые ошибки первыми, настройки по алфавиту. Сам словарь сортировать нельзя «на месте», но можно получить отсортированный список ключей или пар — или новый упорядоченный словарь.

## Как это работает

- `sorted(d)` — список **ключей** по возрастанию.
- `sorted(d.items())` — список пар, отсортированных по ключу.
- `sorted(d.items(), key=lambda p: p[1])` — по значению.
- `sorted(d, key=d.get)` — ключи, упорядоченные по значениям (`d.get` — функция «ключ → значение»).
- `reverse=True` — по убыванию; для смешанных направлений — кортеж с минусом: `key=lambda p: (-p[1], p[0])`.
- `max(d, key=d.get)` — ключ с наибольшим значением.
- `dict(sorted(d.items()))` — новый словарь в нужном порядке (словари сохраняют порядок вставки).
- `heapq.nlargest(n, d, key=d.get)` — топ-N без полной сортировки.

## Примеры

### Пример 1. По ключу и по значению

```python
scores = {"Боря": 50, "Аня": 80, "Вика": 65}
print(sorted(scores))
print(sorted(scores.items()))
print(sorted(scores.items(), key=lambda p: p[1], reverse=True))
print(max(scores, key=scores.get))
```

### Пример 2. Таблица лидеров

```python
scores = {"Боря": 50, "Аня": 80, "Вика": 50, "Гоша": 10}
ranking = sorted(scores.items(), key=lambda p: (-p[1], p[0]))
for place, (name, pts) in enumerate(ranking, start=1):
    print(f"{place}. {name:5} {pts}")
```

### Пример 3. Топ медленных тестов

```python
import heapq
times = {"login": 1.2, "pay": 3.4, "search": 0.2, "cart": 2.0, "logout": 0.1}
print(sorted(times, key=times.get, reverse=True)[:3])
print(heapq.nlargest(3, times, key=times.get))
```

### Пример 4. Упорядоченный словарь

```python
config = {"timeout": 30, "browser": "chrome", "base_url": "https://x"}
print(dict(sorted(config.items())))
```

## Частые ошибки

**`d.sort()`** — у словаря нет метода sort.

**`sorted(d)` в ожидании пар** — сортирует ключи.

**`key=d.get()`** — передаётся функция без скобок.

## Шпаргалка

```py
sorted(d)                              # ключи
sorted(d.items(), key=lambda p: p[1])  # пары по значению
sorted(d, key=d.get, reverse=True)[:n] # топ ключей
max(d, key=d.get)
dict(sorted(d.items()))
```
'''),
    quiz=[
        q('Что вернёт `sorted({"b": 1, "a": 2})`?',
            ["`[('a', 2), ('b', 1)]`", "`['a', 'b']`", '`[1, 2]`', 'Ошибка'],
            1, 'sorted по словарю сортирует ключи.'),
        q('Что вернёт `max({"a": 3, "b": 7}, key={"a": 3, "b": 7}.get)`?',
            ['`7`', '`"b"`', '`("b", 7)`', '`"a"`'],
            1, 'max перебирает ключи, сравнивая их значения.'),
        q('Есть ли у словаря метод `.sort()`?',
            ['Да', 'Нет', 'Только в Python 3.12', 'Только для числовых ключей'],
            1, 'Сортируют через sorted(), получая список или новый словарь.'),
    ],
),

# ---------- dct-m3-l1: Вложенные словари ----------
'dct-m3-l1': dict(
    short=t(r'''
# JSON-подобные данные

```
resp = {"data": {"user": {"name": "Аня", "roles": ["qa"]}}, "status": 200}
resp["data"]["user"]["name"]          # "Аня"
resp.get("data", {}).get("meta", {})  # безопасный спуск
```

Каждый шаг может упасть с `KeyError`, если ключа нет.
'''),
    full=t(r'''
## Зачем это нужно

Ответы API, конфиги (YAML/JSON), фикстуры тестовых данных — всё это вложенные словари. Нужно уметь достать поле с любой глубины, безопасно пройти по необязательным веткам, построить вложенную структуру и превратить её в плоскую — например, чтобы сравнить два ответа поле за полем.

## Как это работает

### Доступ

`resp["data"]["user"]["name"]` — цепочка индексаций. Каждый шаг может дать `KeyError`.

### Безопасный спуск

`resp.get("data", {}).get("user", {}).get("name")` — `{}` по умолчанию позволяет продолжить цепочку, в конце получим значение или `None`. Осторожно: если по пути встретится не словарь (например, `None` или список), `.get` упадёт — тогда нужна функция с `try/except`.

### Построение

`d.setdefault(key, {})` — «зайти во вложенный словарь, создав его при необходимости». Отлично подходит для построения дерева по пути.

### Расплющивание

Рекурсивный обход: если значение — словарь, спускаемся глубже, добавляя ключ к префиксу; иначе — записываем `префикс.ключ → значение`. Плоский вид удобен для сравнения и отчётов.

## Примеры

### Пример 1. Разбор ответа

```python
resp = {"status": 200, "data": {"items": [{"id": 1, "tags": ["new"]}, {"id": 2, "tags": []}], "total": 2}}
items = resp["data"]["items"]
print("total совпадает:", len(items) == resp["data"]["total"])
for item in items:
    print(item["id"], item["tags"][0] if item["tags"] else "без тегов")
```

### Пример 2. Безопасный спуск

```python
def page(resp):
    return resp.get("meta", {}).get("pagination", {}).get("page", 1)

print(page({"meta": {"pagination": {"page": 3}}}), page({}), page({"meta": {}}))
```

### Пример 3. Построение по пути

```python
tree = {}
for path, value in [("env.staging.url", "https://stg"), ("env.prod.url", "https://prod"), ("timeout", 30)]:
    *parents, last = path.split(".")
    node = tree
    for key in parents:
        node = node.setdefault(key, {})
    node[last] = value
print(tree)
```

### Пример 4. Плоское сравнение двух ответов

```python
def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        out.update(flatten(v, key) if isinstance(v, dict) else {key: v})
    return out

expected = {"user": {"name": "Аня", "address": {"city": "Казань"}}, "active": True}
actual = {"user": {"name": "Аня", "address": {"city": "Москва"}}, "active": True}
fe, fa = flatten(expected), flatten(actual)
print({k: (fe[k], fa.get(k)) for k in fe if fe[k] != fa.get(k)})
```

## Частые ошибки

**Длинная цепочка `[]` без проверки** — `KeyError` на необязательном поле.

**`.get(...)` на значении `None`** — `AttributeError`.

**Изменение вложенного словаря «копии»**, сделанной через `dict(d)` — вложенные словари общие (следующий урок).

## Шпаргалка

```py
d["a"]["b"]["c"]
d.get("a", {}).get("b", {}).get("c")
node = node.setdefault(key, {})
flatten: рекурсия с префиксом "a.b.c"
```
'''),
    quiz=[
        q('Что вернёт `{}.get("a", {}).get("b")`?',
            ['`KeyError`', '`None`', '`{}`', 'Ошибка'],
            1, 'Первый get вернёт `{}`, второй — `None`.'),
        q('Что делает `node = node.setdefault(key, {})` в цикле по ключам пути?',
            ['Удаляет ключи', 'Спускается во вложенный словарь, создавая его при необходимости', 'Копирует словарь', 'Ничего'],
            1, 'Классический приём построения дерева.'),
        q('Что вернёт `{"a": None}.get("a", {}).get("b")`?',
            ['`None`', '`AttributeError`: у None нет get', '`{}`', '`KeyError`'],
            1, 'Ключ есть со значением None, а у None нет метода get.'),
    ],
),

# ---------- dct-m3-l2: Слияние и копирование ----------
'dct-m3-l2': dict(
    short=t(r'''
# Слияние

```
merged = {**defaults, **overrides}    # новый словарь, правый побеждает
merged = defaults | overrides         # то же (Python 3.9+)
defaults.update(overrides)            # на месте
```

# Копирование

```
shallow = d.copy()          # вложенные объекты — общие!
import copy
deep = copy.deepcopy(d)     # полная копия
```
'''),
    full=t(r'''
## Зачем это нужно

Конфигурация тестов почти всегда многослойная: настройки по умолчанию → настройки окружения (staging) → переопределения из командной строки. Это слияние словарей. А тестовые данные часто создают из шаблона — и если скопировать шаблон неправильно, один тест испортит данные для всех остальных.

## Как это работает

### Слияние

- `{**a, **b}` — новый словарь: сначала пары из `a`, потом из `b`; при совпадении ключей побеждает **правый**.
- `a | b` — то же самое (Python 3.9+); `a |= b` — обновление на месте.
- `a.update(b)` — на месте, возвращает `None`.

Все эти способы **поверхностные**: вложенный словарь из `b` целиком заменит вложенный словарь из `a`. Для «умного» слияния вложенных настроек нужна рекурсия.

### Копирование

- `d.copy()`, `dict(d)`, `{**d}` — **мелкая** копия: новый внешний словарь, но вложенные списки и словари — те же объекты.
- `copy.deepcopy(d)` — **глубокая** копия: всё копируется рекурсивно, изменения никак не влияют на оригинал.

## Примеры

### Пример 1. Слои конфигурации

```python
defaults = {"timeout": 30, "browser": "chrome", "headless": True}
staging = {"base_url": "https://stg.shop.ru"}
cli = {"browser": "firefox", "headless": False}
config = defaults | staging | cli
print(config)
```

### Пример 2. Поверхностное слияние теряет вложенное

```python
base = {"db": {"host": "localhost", "port": 5432}}
override = {"db": {"host": "stg-db"}}
print({**base, **override})       # port пропал!
```

### Пример 3. Рекурсивное слияние

```python
def deep_merge(base, override):
    result = dict(base)
    for key, value in override.items():
        if isinstance(result.get(key), dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

print(deep_merge({"db": {"host": "localhost", "port": 5432}}, {"db": {"host": "stg-db"}}))
```

### Пример 4. Мелкая и глубокая копия

```python
import copy
template = {"name": "test_user", "roles": ["qa"]}
a = template.copy()
b = copy.deepcopy(template)
a["roles"].append("admin")
print("шаблон:", template)
print("глубокая:", b)
```

## Частые ошибки

**`d2 = d1`** — не копия, а второе имя.

**Мелкая копия шаблона с вложенными списками** — тесты портят друг другу данные.

**Ожидание рекурсивного слияния от `|` или `update`.**

## Шпаргалка

```py
{**a, **b};  a | b;  a.update(b)   # правый побеждает, поверхностно
d.copy()                           # мелкая копия
copy.deepcopy(d)                   # глубокая
deep_merge — рекурсия для вложенных настроек
```
'''),
    quiz=[
        q('Что вернёт `{"a": 1, "b": 2} | {"b": 3}`?',
            ["`{'a': 1, 'b': 2}`", "`{'a': 1, 'b': 3}`", "`{'b': 3}`", 'Ошибка'],
            1, 'Правый словарь побеждает при совпадении ключей.'),
        q('Скопирует ли `d.copy()` вложенный список?',
            ['Да', 'Нет, вложенный список будет общим', 'Только если он пуст', 'Скопирует дважды'],
            1, 'copy() — мелкая копия.'),
        q('Что даст `{**{"db": {"host": "a", "port": 1}}, **{"db": {"host": "b"}}}`?',
            ["`{'db': {'host': 'b', 'port': 1}}`", "`{'db': {'host': 'b'}}`", 'Ошибка', "`{'db': {'host': 'a', 'port': 1}}`"],
            1, 'Слияние поверхностное: вложенный словарь заменён целиком.'),
    ],
),

# ---------- dct-m3-l3: Словарные включения ----------
'dct-m3-l3': dict(
    short=t(r'''
# dict comprehension

```
{k: v for k, v in pairs}
{name: len(name) for name in names}
{k: v for k, v in d.items() if v is not None}    # фильтр
{v: k for k, v in d.items()}                      # инверсия
```

Короткий способ построить словарь из данных.
'''),
    full=t(r'''
## Зачем это нужно

Построить словарь из данных нужно постоянно: индекс «id → объект» для быстрого поиска, словарь длин, отфильтрованные настройки, перевёрнутый справочник кодов. Словарное включение делает это одной понятной строкой.

## Как это работает

```py
{ключ: значение for элемент in коллекция if условие}
```

- Выражения ключа и значения вычисляются для каждого элемента.
- Необязательный `if` фильтрует элементы.
- Если ключи повторяются — остаётся **последнее** значение.
- У включения своя область видимости (переменные не «утекают»).

Типичные шаблоны:
- из списка: `{x: f(x) for x in xs}`;
- из пар: `{k: v for k, v in pairs}` (или просто `dict(pairs)`);
- преобразование словаря: `{k: f(v) for k, v in d.items()}`;
- фильтр: `{k: v for k, v in d.items() if cond(v)}`;
- инверсия: `{v: k for k, v in d.items()}` (значения должны быть уникальными и хешируемыми);
- индекс: `{obj["id"]: obj for obj in objects}`.

## Примеры

### Пример 1. Базовые формы

```python
words = ["api", "ui", "docker", "ci"]
print({w: len(w) for w in words})
print({w: len(w) for w in words if len(w) > 2})
```

### Пример 2. Индекс для быстрого поиска

```python
users = [{"id": 1, "name": "Аня"}, {"id": 2, "name": "Боря"}, {"id": 3, "name": "Вика"}]
by_id = {u["id"]: u for u in users}
print(by_id[2]["name"])
```

### Пример 3. Очистка и преобразование

```python
raw = {"Name ": " Аня", "AGE": "25", "email": None}
clean = {k.strip().lower(): v.strip() for k, v in raw.items() if v is not None}
print(clean)
```

### Пример 4. Инверсия и её подвох

```python
codes = {"OK": 200, "Success": 200, "Not Found": 404}
print({code: text for text, code in codes.items()})     # 200 перезаписался!
```

## Частые ошибки

**Инверсия с повторяющимися значениями** — часть данных теряется.

**Слишком сложное включение** — если не читается с одного взгляда, лучше цикл.

**`{x for x in xs}`** без двоеточия — это множество, а не словарь.

## Шпаргалка

```py
{x: f(x) for x in xs}
{k: v for k, v in d.items() if v is not None}
{v: k for k, v in d.items()}
{obj["id"]: obj for obj in objs}
```
'''),
    quiz=[
        q('Что создаёт `{x for x in [1, 2]}`?',
            ['Словарь', 'Множество', 'Список', 'Ошибку'],
            1, 'Без двоеточия фигурные скобки — множество.'),
        q('Что вернёт `{k: v for k, v in [("a", 1), ("a", 2)]}`?',
            ["`{'a': 1}`", "`{'a': 2}`", 'Ошибка', "`{'a': [1, 2]}`"],
            1, 'Повторяющийся ключ — последнее значение побеждает.'),
        q('Зачем строить индекс `{u["id"]: u for u in users}`?',
            ['Чтобы отсортировать', 'Чтобы находить пользователя по id мгновенно, без перебора списка', 'Чтобы удалить дубликаты', 'Незачем'],
            1, 'Поиск по ключу словаря не зависит от размера данных.'),
    ],
),
}
