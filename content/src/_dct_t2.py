"""Теория модуля «Перебор и обработка» темы «Словари».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- dct-m2-l1: Перебор словаря ----------
'dct-m2-l1': dict(
    full=t(r'''
## Зачем это нужно

Обработать все поля ответа, посчитать стоимость корзины, найти упавшие тесты — всё это перебор словаря. Перебирать можно ключи, значения или пары сразу. Выбор правильного способа делает код коротким.

## Три способа перебора

```python
prices = {"чай": 300, "кофе": 500}
for item in prices:
    print(item)
for item, price in prices.items():
    print(f"{item}: {price}")
print(sum(prices.values()))
```

- `for key in d` — перебор **ключей** (то же, что `d.keys()`).
- `for k, v in d.items()` — перебор **пар**; каждая пара — кортеж, распаковываемый в `k, v`.
- `d.values()` — только **значения**; удобно для `sum`, `max`, `min`.
- Перебор идёт в порядке добавления ключей.
- Вывод: `чай`, `кофе`, `чай: 300`, `кофе: 500`, `800`.

## Представления keys, values, items

```python
d = {"a": 1}
keys = d.keys()
d["b"] = 2
print(list(keys))
print(list(d.values()), list(d.items()))
```

- `keys()`, `values()`, `items()` возвращают **представления** (views) — «окна» в словарь, а не копии. Добавили ключ — представление сразу его видит.
- `list(...)` превращает представление в список.
- Вывод: `['a', 'b']`, `[1, 2] [('a', 1), ('b', 2)]`.

```python
d = {"x": 10, "y": 20}
print(list(d.keys()), list(d.values()))
print(list(enumerate(d)))
for i, (k, v) in enumerate(d.items(), start=1):
    print(i, k, v)
```

- `enumerate(d)` нумерует **ключи**. С `items()` и вложенной распаковкой `i, (k, v)` получаем номер, ключ и значение.
- Вывод: `['x', 'y'] [10, 20]`, `[(0, 'x'), (1, 'y')]`, `1 x 10`, `2 y 20`.

## Два словаря вместе

```python
cart = {"чай": 2, "кофе": 1}
prices = {"чай": 300, "кофе": 500, "сок": 150}
total = 0
for item, qty in cart.items():
    total += prices[item] * qty
print(total)
```

- Перебираем корзину, цену берём из второго словаря по тому же ключу. Вывод: `1100`.

## Фильтр по значению

```python
results = {"login": "pass", "pay": "fail", "cart": "fail"}
print(sorted(name for name, status in results.items() if status == "fail"))
print({k: v for k, v in {"a": 5, "b": 1}.items() if v >= 3})
```

- Генератор с условием внутри `sorted` — отсортированный список имён. Включение `{k: v ...}` — новый словарь (урок «Словарные включения»).
- Вывод: `['cart', 'pay']`, `{'a': 5}`.

## Ключ с наибольшим значением

```python
d = {"a": 3, "b": 7, "c": 7}
best_key, best_value = None, None
for key, value in d.items():
    if best_value is None or value > best_value:
        best_key, best_value = key, value
print(best_key, max(d, key=d.get))
```

- Ручной перебор или встроенный `max(d, key=d.get)`: перебираем ключи, сравниваем по `d.get(ключ)`.
- Оба варианта при равенстве берут первый. Вывод: `b b`.

## Строка из пар

```python
headers = {"Content-Type": "application/json", "X-Id": "42"}
print("\n".join(f"{name}: {value}" for name, value in headers.items()))
```

Вывод: две строки `Content-Type: application/json` и `X-Id: 42`.

## Итог

- `for k in d` — ключи; `for k, v in d.items()` — пары; `d.values()` — значения.
- Порядок перебора — порядок вставки.
- `keys()/values()/items()` — живые представления; `list(...)` — снимок.
- `max(d, key=d.get)` — ключ с наибольшим значением.
'''),
    short=t(r'''
```py
for key in d: ...                 # ключи
for key, value in d.items(): ...  # пары
sum(d.values())                   # значения
list(d.keys())                    # снимок представления
for i, (k, v) in enumerate(d.items(), start=1): ...
max(d, key=d.get)                 # ключ с max значением
```
'''),
    quiz=[
        q('Что перебирает `for x in d:` для словаря?',
            ['Значения', 'Ключи', 'Пары', 'Индексы'],
            1, 'По умолчанию — ключи.'),
        q('Что вернёт `sum({"a": 2, "b": 3}.values())`?',
            ['`5`', '`"ab"`', 'Ошибка', '`2`'],
            0, 'Сумма значений.'),
        q('Что даёт `max(d, key=d.get)`?',
            ['Наибольшее значение', 'Ключ с наибольшим значением', 'Наибольший ключ', 'Ошибка'],
            1, 'Перебираются ключи, сравнение — по значениям.'),
    ],
),

# ---------- dct-iter2: Изменение словаря во время перебора ----------
'dct-iter2': dict(
    full=t(r'''
## Зачем это нужно

Частая задача — пройти по словарю и удалить часть пар: пустые поля, нули, служебные ключи. Если удалять прямо во время перебора, Python остановит программу ошибкой. Разберём, что можно делать при переборе, а что нельзя, и как правильно.

## Нельзя менять размер при переборе

```python
d = {"a": 1, "b": 2, "c": 3}
try:
    for k in d:
        if d[k] == 2:
            del d[k]
except RuntimeError as e:
    print("RuntimeError:", e)
```

- Добавление или удаление ключей во время `for k in d` — ошибка `RuntimeError: dictionary changed size during iteration`.
- Словарь «следит» за перебором и не даёт запутаться (со списками аналогичная ошибка молча пропускает элементы — тема «Цикл for»).

## Решение 1: перебирать копию ключей

```python
d = {"a": 1, "b": 2, "c": 3}
for k in list(d):
    if d[k] == 2:
        del d[k]
print(d)
```

- `list(d)` — отдельный список ключей. Перебираем его, а удаляем из словаря — конфликта нет.
- Вывод: `{'a': 1, 'c': 3}`.

## Решение 2: построить новый словарь

```python
d = {"a": 0, "b": 2, "c": 0}
clean = {k: v for k, v in d.items() if v != 0}
print(clean, d)
```

- Исходный словарь не меняется — обычно это даже лучше (урок «Изменяемые объекты» в теме «Область видимости»).
- Вывод: `{'b': 2} {'a': 0, 'b': 2, 'c': 0}`.

## Менять значения — можно

```python
d = {"a": 1, "b": 2}
for k in d:
    d[k] *= 10
print(d)
```

- Присваивание существующему ключу не меняет **размер** словаря — ошибки нет.
- Вывод: `{'a': 10, 'b': 20}`.

## «Пустые» значения: осторожно с not

```python
d = {"a": None, "b": 0, "c": "", "d": [], "e": False, "f": "x"}
for key in list(d):
    value = d[key]
    if value is None or value == "" or value == [] or value == {}:
        del d[key]
print(d)
```

- `not value` истинно и для `0`, и для `False` — а это полноценные значения (0 товаров, флаг выключен). Поэтому «пустоту» проверяем явно.
- Вывод: `{'b': 0, 'e': False, 'f': 'x'}`.

## Переименовать ключи — новый словарь

```python
d = {"userName": "Аня", "id": 1}
mapping = {"userName": "user_name"}
print({mapping.get(k, k): v for k, v in d.items()})
```

- `mapping.get(k, k)` — новое имя, если оно есть, иначе старое.
- Вывод: `{'user_name': 'Аня', 'id': 1}`.

## Итог

- Добавлять/удалять ключи во время `for k in d` нельзя — `RuntimeError`.
- Удаление на месте: `for k in list(d): ... del d[k]`.
- Часто лучше собрать новый словарь включением.
- Менять значения существующих ключей при переборе можно.
- «Пусто» — проверяй явно, `not value` ловит и `0`/`False`.
'''),
    short=t(r'''
```py
for k in d:
    del d[k]                # RuntimeError: changed size
for k in list(d):           # перебор копии ключей — ОК
    if d[k] == 0:
        del d[k]
{k: v for k, v in d.items() if v != 0}   # новый словарь
for k in d:
    d[k] *= 10              # менять значения — можно
```
'''),
    quiz=[
        q('Что будет при `del d[k]` внутри `for k in d:`?',
            ['Ключ удалится', '`RuntimeError`', '`KeyError`', 'Ничего'],
            1, 'Размер словаря нельзя менять при переборе.'),
        q('Как безопасно удалять ключи в цикле?',
            ['Перебирать `list(d)`', 'Перебирать `d`', 'Перебирать `d.values()`', 'Никак'],
            0, 'Копия ключей отделена от словаря.'),
        q('Можно ли при переборе `for k in d` выполнять `d[k] = 0`?',
            ['Нет', 'Да — размер не меняется', 'Только для чисел', 'Только с list(d)'],
            1, 'Меняется значение, а не набор ключей.'),
    ],
),

# ---------- dct-m2-l2: Подсчёт и группировка ----------
'dct-m2-l2': dict(
    full=t(r'''
## Зачем это нужно

Самые частые задачи обработки данных — **подсчёт** (сколько тестов упало, какие ошибки чаще) и **группировка** (пользователи по ролям, слова по первой букве). Словарь для них идеален, а модуль `collections` даёт два специальных помощника: `Counter` и `defaultdict`.

## Подсчёт через get

```python
counts = {}
for ch in "aab c":
    if ch != " ":
        counts[ch] = counts.get(ch, 0) + 1
print(counts)
```

- `counts.get(ch, 0) + 1` — старое значение (или 0) плюс один. Вывод: `{'a': 2, 'b': 1, 'c': 1}`.

## Counter — готовый счётчик

```python
from collections import Counter
results = ["pass", "fail", "pass", "skip", "pass"]
c = Counter(results)
print(c["pass"], c["error"], c.most_common(1))
```

- `Counter(коллекция)` считает, сколько раз встречается каждый элемент.
- Для отсутствующего ключа возвращает `0`, а не `KeyError`.
- `most_common(n)` — `n` самых частых пар `(элемент, количество)` по убыванию.
- Вывод: `3 0 [('pass', 3)]`.

```python
from collections import Counter
c = Counter("banana")
print(c)
print(c.most_common(2), sum(c.values()))
print(dict(Counter("Тест упал тест".lower().split())))
```

- `Counter` — разновидность словаря; `dict(...)` превращает в обычный.
- Вывод: `Counter({'a': 3, 'n': 2, 'b': 1})`, `[('a', 3), ('n', 2)] 6`, `{'тест': 2, 'упал': 1}`.

### Топ ошибок из лога

```python
from collections import Counter
log = ["ERROR timeout", "INFO ok", "ERROR db down", "ERROR timeout"]
errors = [line.split(" ", 1)[1] for line in log if line.startswith("ERROR ")]
print(Counter(errors).most_common(1))
```

- `split(" ", 1)` — разрезать только по первому пробелу, `[1]` — текст после уровня.
- Вывод: `[('timeout', 2)]`.

## Группировка через setdefault

```python
users = [("Аня", "qa"), ("Боря", "dev"), ("Вика", "qa")]
groups = {}
for name, role in users:
    groups.setdefault(role, []).append(name)
print(groups)
```

Вывод: `{'qa': ['Аня', 'Вика'], 'dev': ['Боря']}`.

## defaultdict — словарь с автоматическим умолчанием

```python
from collections import defaultdict
groups = defaultdict(list)
for name, team in [("Аня", "qa"), ("Боря", "dev"), ("Вика", "qa")]:
    groups[team].append(name)
print(dict(groups))
print(groups["ops"])
```

- `defaultdict(list)` — при обращении к отсутствующему ключу сам создаёт значение, вызвав `list()` (пустой список), и записывает его.
- `defaultdict(int)` — умолчание `0`: удобно для счётчиков (`d[k] += 1`).
- Побочный эффект: даже **чтение** `groups["ops"]` создаёт ключ. Вывод: `{'qa': ['Аня', 'Вика'], 'dev': ['Боря']}`, `[]`.
- Для вывода и сравнения превращай в обычный `dict`.

```python
from collections import defaultdict
by_len = defaultdict(list)
for w in ["api", "ui", "db", "test"]:
    by_len[len(w)].append(w)
print(dict(by_len))
```

Вывод: `{3: ['api'], 2: ['ui', 'db'], 4: ['test']}`.

## Итог

- Подсчёт: `d[k] = d.get(k, 0) + 1` или `Counter(коллекция)`.
- `Counter` возвращает 0 для отсутствующих; `most_common(n)` — топ.
- Группировка: `d.setdefault(k, []).append(x)` или `defaultdict(list)`.
- `defaultdict` создаёт ключ даже при чтении; для вывода — `dict(...)`.
'''),
    short=t(r'''
```py
counts[x] = counts.get(x, 0) + 1
from collections import Counter, defaultdict
c = Counter(items);  c["нет"]   # 0
c.most_common(3)                # топ-3
groups.setdefault(key, []).append(x)
g = defaultdict(list);  g[key].append(x)
g = defaultdict(int);   g[key] += 1
dict(g)                         # обычный словарь
```
'''),
    quiz=[
        q('Что вернёт `Counter("aab")["z"]`?',
            ['`KeyError`', '`0`', '`None`', '`""`'],
            1, 'Counter возвращает 0 для отсутствующих.'),
        q('Что создаст `defaultdict(list)` при обращении к новому ключу?',
            ['Ошибку', 'Пустой список', 'None', '0'],
            1, 'Вызывается list().'),
        q('Что вернёт `Counter(["a", "b", "a"]).most_common(1)`?',
            ['`["a"]`', '`[("a", 2)]`', '`("a", 2)`', '`2`'],
            1, 'Список пар (элемент, количество).'),
    ],
),

# ---------- dct-m2-l3: Сортировка словарей ----------
'dct-m2-l3': dict(
    full=t(r'''
## Зачем это нужно

Отчёт «топ самых медленных тестов», таблица лидеров, упорядоченный вывод настроек — всё это сортировка словаря. Сам словарь не сортируется на месте, зато его ключи, значения и пары легко отсортировать `sorted` с нужным ключом.

## По ключам и по значениям

```python
scores = {"Боря": 50, "Аня": 80, "Вика": 65}
print(sorted(scores))
print(sorted(scores, key=scores.get, reverse=True))
print(sorted(scores.items(), key=lambda p: p[1]))
```

- `sorted(d)` — отсортированный **список ключей**.
- `key=scores.get` — сортировать ключи по их значениям; `reverse=True` — по убыванию.
- `sorted(d.items(), key=lambda p: p[1])` — список **пар** по значению; `p[1]` — второй элемент пары.
- Вывод: `['Аня', 'Боря', 'Вика']`, `['Аня', 'Вика', 'Боря']`, `[('Боря', 50), ('Вика', 65), ('Аня', 80)]`.

## Снова в словарь

```python
d = {"b": 2, "a": 1, "c": 3}
ordered = dict(sorted(d.items()))
print(ordered)
print(max(d, key=d.get), min(d.values()))
```

- `dict(отсортированные_пары)` — новый словарь в нужном порядке (словари помнят порядок вставки).
- Вывод: `{'a': 1, 'b': 2, 'c': 3}`, `c 1`.

```python
d = {"b": 1, "a": 3, "c": 2}
print(sorted(d.values()), sorted(d.items(), key=lambda p: -p[1])[0])
print(dict(sorted(d.items(), key=lambda p: p[1])))
```

- `-p[1]` — по убыванию значения без `reverse`; `[0]` — первая пара. Вывод: `[1, 2, 3] ('a', 3)`, `{'b': 1, 'c': 2, 'a': 3}`.

## Топ-N

```python
times = {"login": 1.2, "pay": 3.4, "search": 0.2, "cart": 2.0}
print(sorted(times, key=times.get, reverse=True)[:2])
top = sorted(times.items(), key=lambda p: p[1], reverse=True)[:2]
print(dict(top))
```

- Срез `[:n]` после сортировки — первые `n`. Вывод: `['pay', 'cart']`, `{'pay': 3.4, 'cart': 2.0}`.

## Несколько критериев

```python
d = {"b": 2, "a": 2, "c": 5, "d": 1}
print([k for k, _ in sorted(d.items(), key=lambda p: (-p[1], p[0]))])
```

- Ключ-кортеж: по значению по убыванию (`-p[1]`), при равенстве — по ключу по алфавиту. Вывод: `['c', 'a', 'b', 'd']`.

## Места в рейтинге

```python
scores = {"Боря": 50, "Аня": 80, "Вика": 65}
ordered = sorted(scores, key=scores.get, reverse=True)
print({name: place for place, name in enumerate(ordered, start=1)})
```

Вывод: `{'Аня': 1, 'Вика': 2, 'Боря': 3}`.

## Итог

- `sorted(d)` — ключи; `sorted(d, key=d.get)` — ключи по значениям.
- `sorted(d.items(), key=lambda p: p[1])` — пары по значению.
- `dict(sorted(...))` — упорядоченный словарь.
- Топ-N — срез `[:n]`; несколько критериев — ключ-кортеж, `-x` для убывания.
'''),
    short=t(r'''
```py
sorted(d)                                  # ключи
sorted(d, key=d.get, reverse=True)         # ключи по значению ↓
sorted(d.items(), key=lambda p: p[1])      # пары по значению
dict(sorted(d.items()))                    # упорядоченный словарь
sorted(d.items(), key=lambda p: (-p[1], p[0]))   # значение ↓, ключ ↑
```
'''),
    quiz=[
        q('Что возвращает `sorted({"b": 1, "a": 2})`?',
            ['Словарь', 'Список ключей `["a", "b"]`', 'Список пар', 'Список значений'],
            1, 'Перебор словаря даёт ключи.'),
        q('Как получить ключи по убыванию значений?',
            ['`sorted(d, reverse=True)`', '`sorted(d, key=d.get, reverse=True)`', '`sorted(d.values())`', '`d.sort()`'],
            1, 'key=d.get — сравнение по значениям.'),
        q('Есть ли у словаря метод `sort()`?',
            ['Да', 'Нет — используют sorted', 'Только в Python 3.12', 'Только для чисел'],
            1, 'Словарь сортируют через sorted и dict(...).'),
    ],
),

# ---------- dct-lookup: Словарь вместо if/elif ----------
'dct-lookup': dict(
    full=t(r'''
## Зачем это нужно

Длинная цепочка `if/elif`, где каждая ветка возвращает своё значение, — признак, что нужен **словарь-таблица**. Сопоставление «статус → значок», «код → описание», «команда → функция» в словаре короче, его легко расширять и даже загружать из файла настроек.

## Таблица соответствий

```python
def emoji(status):
    icons = {"pass": "✅", "fail": "❌", "skip": "⏭"}
    return icons.get(status, "❓")

print(emoji("pass"), emoji("fail"), emoji("error"))
```

- Вместо четырёх веток `if/elif/else` — словарь и `get` с умолчанием для «всего остального».
- Вывод: `✅ ❌ ❓`.

Та же логика через `if` заняла бы вдвое больше строк, а новый статус требовал бы новой ветки. Со словарём — одна новая пара.

## Ключ вычисляется

```python
CATEGORIES = {1: "info", 2: "success", 3: "redirect", 4: "client error", 5: "server error"}

def http_category(code):
    return CATEGORIES.get(code // 100, "unknown")

print(http_category(404), http_category(700))
```

- `code // 100` — первая цифра кода; по ней — категория. Вывод: `client error unknown`.
- Словарь-константа вынесен на уровень модуля и не создаётся заново при каждом вызове.

## Замена символов по таблице

```python
layout = {"q": "й", "w": "ц", "e": "у"}
word = "qwe"
print("".join(layout.get(ch, ch) for ch in word + "!"))
```

- `layout.get(ch, ch)` — замена, если она есть, иначе сам символ.
- Вывод: `йцу!`.

## Функции в словаре

```python
ops = {"+": lambda a, b: a + b, "*": lambda a, b: a * b}
print(ops["+"](2, 3), ops["*"](2, 3), "-" in ops)
```

- Значения словаря — функции. `ops["+"]` достаёт функцию, `(2, 3)` вызывает. Вывод: `5 6 False`.

```python
HANDLERS = {"upper": str.upper, "lower": str.lower, "title": str.title}

def run_command(cmd, text):
    handler = HANDLERS.get(cmd)
    if handler is None:
        return "неизвестная команда"
    return handler(text)

print(run_command("upper", "hi"), run_command("x", "abc"))
```

- `str.upper` — метод строки как обычная функция: `str.upper("hi")` = `"hi".upper()`.
- Вывод: `HI неизвестная команда`. Так устроены диспетчеры команд, роутеры URL, обработчики событий.

## Словарь + логика: римские числа

```python
VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
s = "MCMXCIV"
total = 0
for i in range(len(s)):
    value = VALUES[s[i]]
    if i + 1 < len(s) and value < VALUES[s[i + 1]]:
        total -= value
    else:
        total += value
print(total)
```

- Словарь хранит «что означает буква», а цикл — правило вычитания (IV = 5 − 1).
- Вывод: `1994`.

## Когда словарь не подходит

Если ветки проверяют **диапазоны** (`score >= 90`, `age < 18`), словарь не поможет — для точного совпадения ключа нужно конкретное значение. Тогда оставь `if/elif` или список порогов.

## Итог

- Много веток вида «значение → результат» — замени словарём и `get(ключ, умолчание)`.
- Ключ можно вычислить: `code // 100`, `ch.lower()`.
- Значениями могут быть функции — диспетчер команд.
- Таблицы-константы держи на уровне модуля.
- Диапазоны и сложные условия — по-прежнему `if`.
'''),
    short=t(r'''
```py
ICONS = {"pass": "✅", "fail": "❌"}
ICONS.get(status, "❓")                # вместо if/elif/else
CATEGORIES.get(code // 100, "unknown")
"".join(TR.get(ch, ch) for ch in text) # замена символов
HANDLERS = {"upper": str.upper}
HANDLERS[cmd](text)                    # функция из словаря
```
'''),
    quiz=[
        q('Чем заменить цепочку `if s == "a": return 1 / elif s == "b": return 2 / else: return 0`?',
            ['Циклом', '`{"a": 1, "b": 2}.get(s, 0)`', 'Списком', 'Никак'],
            1, 'Словарь-таблица с умолчанием.'),
        q('Что вернёт `{"+": lambda a, b: a + b}["+"](2, 5)`?',
            ['Функцию', '`7`', 'Ошибка', '`"+"`'],
            1, 'Достали функцию и вызвали.'),
        q('Когда словарь НЕ подходит вместо if?',
            ['Когда проверяются диапазоны (x >= 90)', 'Когда значений много', 'Когда значения — строки', 'Всегда подходит'],
            0, 'Нужно точное совпадение ключа.'),
    ],
),
}
