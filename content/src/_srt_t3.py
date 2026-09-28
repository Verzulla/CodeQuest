"""Теория модуля «Другие помощники» темы «sorted, filter и map».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- srt-m3-l1 ----------
'srt-m3-l1': dict(
    full=t(r'''
## Зачем это нужно

`min` и `max` находят наименьший и наибольший элемент, и у них есть тот же параметр `key`, что у `sorted`: самое длинное слово, самый дешёвый товар, число, ближайшее к цели. Сортировать весь список ради одного элемента не нужно.

## Без key и с key

```python
words = ["banana", "fig", "kiwi"]
print(min(words), max(words))
print(min(words, key=len), max(words, key=len))
```

- Без `key` строки сравниваются по алфавиту.
- С `key=len` — по длине; возвращается сам элемент.
- Вывод: `banana kiwi`, `fig banana`.

## Равные ключи

```python
users = [("Аня", 30), ("Боря", 30), ("Вика", 25)]
print(max(users, key=lambda u: u[1]))
print(min(users, key=lambda u: u[1])[0])
```

- При равенстве `max` и `min` возвращают **первый** такой элемент.
- Вывод: `('Аня', 30)`, `Вика`.

## Пустая коллекция и default

```python
print(max([], default=0), min([], default=None))
try:
    max([])
except ValueError:
    print("ValueError: пустая последовательность")
```

- `max([])` — `ValueError`. Параметр `default` задаёт результат для пустой коллекции.
- Вывод: `0 None`, `ValueError: пустая последовательность`.

## Типичные задачи

```python
scores = {"Аня": 80, "Боря": 95}
print(max(scores, key=scores.get))
products = [{"name": "a", "price": 30}, {"name": "b", "price": 10}]
print(min(products, key=lambda p: p["price"])["name"])
print(min([1, 5, 9], key=lambda n: abs(n - 6)))
nums = [3, 9, 1]
print(max(nums, default=0) - min(nums, default=0))
```

- Лучший по словарю; самый дешёвый товар; ближайшее к 6; размах значений.
- Вывод: `Боря`, `b`, `5`, `8`.

Можно передать и несколько аргументов: `max(3, 9, 2)` → `9`.

## Итог

- `min`/`max` с `key` — лучший элемент по признаку; сортировка не нужна.
- При равенстве — первый.
- Пустая коллекция — `ValueError`; `default=` — значение по умолчанию.
'''),
    short=t(r'''
```py
max(words, key=len)                  # самое длинное
min(products, key=lambda p: p["price"])
max(scores, key=scores.get)          # ключ с max значением
min(nums, key=lambda n: abs(n - t))  # ближайшее к t
max([], default=0)                   # без ValueError
```
'''),
    quiz=[
        q('Что вернёт `max(["aa", "b", "cc"], key=len)`?',
            ['`"cc"`', '`"aa"`', '`2`', '`"b"`'],
            1, 'При равенстве — первый.'),
        q('Что будет при `min([])`?',
            ['None', '`ValueError`', '0', '`[]`'],
            1, 'Используй default.'),
        q('Как найти число из `nums`, ближайшее к 10?',
            ['`min(nums)`', '`min(nums, key=lambda n: abs(n - 10))`', '`max(nums, key=10)`', '`sorted(nums)[10]`'],
            1, 'Ключ — расстояние до цели.'),
    ],
),

# ---------- srt-m3-l2 ----------
'srt-m3-l2': dict(
    full=t(r'''
## Зачем это нужно

`reversed`, `enumerate` и `zip` — три помощника перебора, которые встречались в темах про циклы. Здесь — их тонкости: `reversed` не создаёт список, `zip` умеет «распаковываться обратно» и проверять одинаковую длину.

## reversed

```python
items = ["a", "b", "c"]
print(list(reversed(items)), items)
for i, x in enumerate(reversed(items), start=1):
    print(i, x)
```

- `reversed(коллекция)` — итератор в обратном порядке; исходный список не меняется (в отличие от `list.reverse()`).
- Срез к `reversed` применить нельзя — сначала `list(...)`.
- Вывод: `['c', 'b', 'a'] ['a', 'b', 'c']`, затем `1 c`, `2 b`, `3 a`.

## zip и «обратный» zip

```python
names = ["Аня", "Боря"]
ages = [25, 30]
pairs = list(zip(names, ages))
print(pairs)
n, a = zip(*pairs)
print(n, a)
```

- `zip(a, b)` — пары элементов.
- `zip(*pairs)` — звёздочка раскладывает список пар в отдельные аргументы, и `zip` собирает первые элементы вместе, вторые вместе. Это «распаковка» — транспонирование.
- Результаты `zip` — кортежи. Для пустого списка распаковать в две переменные не получится — проверяй заранее.
- Вывод: `[('Аня', 25), ('Боря', 30)]`, `('Аня', 'Боря') (25, 30)`.

## Разная длина и strict

```python
print(list(zip([1, 2, 3], "ab")))
try:
    list(zip([1, 2, 3], "ab", strict=True))
except ValueError:
    print("strict: разная длина")
```

- По умолчанию `zip` молча останавливается на самой короткой коллекции — лишнее теряется.
- `strict=True` (Python 3.10+) — выбросить `ValueError`, если длины разные. Для тестов это полезно: сравнение ожидаемого и фактического не пропустит недостающие элементы.
- Вывод: `[(1, 'a'), (2, 'b')]`, `strict: разная длина`.

## Всё вместе

```python
expected = [1, 2, 3]
actual = [1, 5, 3]
print([f"#{i}: {e} != {a}" for i, (e, a) in enumerate(zip(expected, actual, strict=True), start=1) if e != a])
print(dict(zip(["a", "b"], [1, 2])))
```

- Нумерованные различия и словарь из двух списков.
- Вывод: `['#2: 2 != 5']`, `{'a': 1, 'b': 2}`.

## Итог

- `reversed(x)` — обратный итератор, исходник не меняется.
- `zip(*pairs)` — разложить пары обратно.
- `zip` обрезает по короткой коллекции; `strict=True` — ошибка при разной длине.
- `enumerate(zip(...), start=1)` — номер и пара сразу.
'''),
    short=t(r'''
```py
list(reversed(items))              # исходник не меняется
names, ages = zip(*pairs)          # обратный zip
zip(a, b, strict=True)             # ValueError при разной длине
enumerate(zip(e, a), start=1)
dict(zip(keys, values))
```
'''),
    quiz=[
        q('Что вернёт `list(zip(*[(1, "a"), (2, "b")]))`?',
            ['`[(1, "a"), (2, "b")]`', '`[(1, 2), ("a", "b")]`', '`[1, 2, "a", "b"]`', 'Ошибка'],
            1, 'Обратный zip.'),
        q('Что делает `strict=True` у zip?',
            ['Сортирует', 'Выбрасывает ValueError при разной длине', 'Убирает None', 'Ничего'],
            1, 'Python 3.10+.'),
        q('Меняет ли `reversed(lst)` сам список?',
            ['Да', 'Нет', 'Только для строк', 'Только при list()'],
            1, 'Это итератор.'),
    ],
),

# ---------- srt-m3-l3 ----------
'srt-m3-l3': dict(
    full=t(r'''
## Зачем это нужно

`any` и `all` отвечают на вопросы «есть ли хоть один?» и «все ли?», а `sum` с логическими значениями считает, «сколько подходит». Это основа проверок в тестах: все ли ответы 2xx, есть ли ошибка сервера, сколько тестов прошло.

## any и all

```python
codes = [200, 201, 404]
print(any(c >= 400 for c in codes), all(c < 500 for c in codes))
print(any([]), all([]))
```

- `any(...)` — `True`, если хотя бы один элемент истинный; останавливается на первом.
- `all(...)` — `True`, если все истинные; останавливается на первом ложном.
- Для пустой коллекции: `any` — `False` (нет ни одного), `all` — `True` (нет ни одного опровержения).
- Вывод: `True True`, `False True`.

## Истинность элементов

```python
print(any([0, "", None]), any([0, "x"]), all([1, "a", [0]]), all([1, []]))
```

- Без генератора проверяется истинность самих значений: `0`, `""`, `None`, `[]` — ложны.
- Вывод: `False True True False`.

## Подсчёт через sum

```python
results = ["pass", "fail", "pass"]
print(sum(r == "pass" for r in results))
print(sum(1 for r in results if r == "fail"))
```

- `True` в арифметике — `1`, `False` — `0`, поэтому сумма логических значений — количество истинных.
- Второй вариант: складывать единицы для подходящих.
- Вывод: `2`, `1`.

## Составные проверки

```python
p = "Secret123"
print(len(p) >= 8 and any(ch.isdigit() for ch in p) and any(ch.isupper() for ch in p) and any(ch.islower() for ch in p))
items = [{"id": 1}, {"id": True}]
print(all(isinstance(i.get("id"), int) and not isinstance(i.get("id"), bool) for i in items))
```

- Надёжный пароль: несколько `any` через `and`.
- Проверка ответа API: у всех объектов `id` — целое, но не `bool` (`True` — подтип `int`).
- Вывод: `True`, `False`.

## Итог

- `any` — хоть один; `all` — все; оба останавливаются досрочно.
- `any([])` — `False`, `all([])` — `True`.
- `sum(условие for x in ...)` — количество подходящих.
- Сложные правила — комбинация `any`/`all` через `and`.
'''),
    short=t(r'''
```py
any(c >= 500 for c in codes)       # хоть один
all(r == "pass" for r in results)  # все
any([]) is False; all([]) is True
sum(r == "pass" for r in results)  # сколько
```
'''),
    quiz=[
        q('Что вернёт `all([])`?',
            ['`False`', '`True`', 'Ошибка', '`None`'],
            1, 'Нет опровержений.'),
        q('Что вернёт `sum(x > 0 for x in [1, -2, 3])`?',
            ['`2`', '`4`', '`True`', 'Ошибка'],
            0, 'True считается как 1.'),
        q('Что вернёт `any([0, "", None])`?',
            ['`True`', '`False`', '`None`', 'Ошибка'],
            1, 'Все значения ложны.'),
    ],
),

# ---------- srt-m3-l4 ----------
'srt-m3-l4': dict(
    full=t(r'''
## Зачем это нужно

Реальная обработка данных — это **конвейер**: очистить, отфильтровать, преобразовать, отсортировать, подвести итог. Каждый шаг — один из изученных инструментов. Разберём несколько конвейеров из практики тестировщика.

## Частые ошибки в логе

```python
log = ["INFO start", "ERROR db", "WARN slow", "ERROR api", "ERROR db"]
errors = [line.split()[1] for line in log if line.startswith("ERROR")]
print(sorted(set(errors)), max(set(errors), key=errors.count))
print(sorted(set(errors), key=lambda e: (-errors.count(e), e)))
```

- Фильтр строк → извлечение текста → различные значения (`set`) → самое частое (`max` с `key=errors.count`) → рейтинг по частоте, при равенстве по алфавиту.
- Вывод: `['api', 'db'] db`, `['db', 'api']`.

## Быстрые прошедшие тесты

```python
results = [("login", 1.2, "pass"), ("pay", 3.4, "fail"), ("cart", 0.5, "pass")]
passed = filter(lambda r: r[2] == "pass", results)
names = map(lambda r: r[0], sorted(passed, key=lambda r: r[1]))
print(list(names))
```

- `filter` → `sorted` (принимает итератор) → `map`. Вывод: `['cart', 'login']`.

## Очистка «грязных» цен

```python
prices = ["100", " 250 ", "", "x", "40"]
clean = [int(p) for p in map(str.strip, prices) if p.isdigit()]
print(clean, sum(clean), max(clean, default=0), sorted(clean, reverse=True))
```

- `map(str.strip, ...)` чистит, фильтр оставляет числа, `int` превращает.
- Вывод: `[100, 250, 40] 390 250 [250, 100, 40]`.

## Сводка прогона

```python
results = [{"name": "a", "status": "pass", "time": 1}, {"name": "b", "status": "fail", "time": 3}]
slowest = max(results, key=lambda r: r["time"], default=None)
print({
    "total": len(results),
    "passed": sum(r["status"] == "pass" for r in results),
    "slowest": slowest["name"] if slowest else None,
    "all_green": all(r["status"] == "pass" for r in results),
})
```

- Каждое поле сводки — одна строка с подходящим инструментом.
- Вывод: `{'total': 2, 'passed': 1, 'slowest': 'b', 'all_green': False}`.

## Объединить и упорядочить без учёта регистра

```python
groups = [["bob", "Anna"], ["anna", "Cat"]]
seen = {}
for group in groups:
    for name in group:
        seen.setdefault(name.lower(), name)
print(sorted(seen.values(), key=str.lower))
```

- Словарь «нормализованный ключ → первый вариант» убирает дубли без учёта регистра; сортировка — тоже без учёта регистра.
- Вывод: `['Anna', 'bob', 'Cat']`.

## Итог

- Конвейер: очистить (`map`) → отфильтровать (`filter`/включение) → упорядочить (`sorted` с `key`) → подытожить (`sum`, `max`, `all`).
- Каждый шаг — короткая понятная строка; сложную логику выноси в функции.
- `sorted`, `sum`, `max` принимают итераторы — промежуточные списки часто не нужны.
'''),
    short=t(r'''
```py
clean = [int(p) for p in map(str.strip, raw) if p.isdigit()]
sorted(filter(cond, rows), key=lambda r: r[1])
max(set(errors), key=errors.count)
sorted(unique, key=lambda e: (-errors.count(e), e))
{"passed": sum(...), "all_green": all(...)}
```
'''),
    quiz=[
        q('Как найти самый частый элемент списка `errors`?',
            ['`max(errors)`', '`max(set(errors), key=errors.count)`', '`sorted(errors)[0]`', '`errors.count()`'],
            1, 'Ключ — количество вхождений.'),
        q('Принимает ли `sorted` итератор от `filter`?',
            ['Нет', 'Да', 'Только список', 'Только кортеж'],
            1, 'sorted работает с любой коллекцией.'),
        q('Что даст `[int(p) for p in map(str.strip, [" 5", "x"]) if p.isdigit()]`?',
            ['`[5]`', '`[" 5"]`', 'Ошибка', '`[5, "x"]`'],
            0, 'Очистка, фильтр, преобразование.'),
    ],
),
}
