"""Теория модуля «Выражения и конвейеры» темы «Генераторы».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- gen-m2-l1 ----------
'gen-m2-l1': dict(
    full=t(r'''
## Зачем это нужно

Простые генераторы можно записать в одну строку — **генераторным выражением**. Оно похоже на списковое включение, но в круглых скобках и не создаёт список в памяти. Идеально подходит для `sum`, `any`, `all`, `max`, `join`.

## Синтаксис

```python
g = (x * 10 for x in range(3))
print(type(g).__name__)
print(list(g))
print(list(g))
```

- `(выражение for x in итерируемое if условие)` — как списковое включение, только в круглых скобках.
- Результат — генератор: ленивый и одноразовый.
- Вывод: `generator`, `[0, 10, 20]`, `[]`.

## С функциями-агрегаторами

```python
nums = [3, 8, -1, 4]
print(sum(n for n in nums if n > 0))
print(any(n < 0 for n in nums))
print(all(n < 10 for n in nums))
```

- Если генераторное выражение — **единственный** аргумент функции, дополнительные скобки не нужны.
- `any` — есть ли хоть один истинный, `all` — все ли истинны.
- Вывод: `15`, `True`, `True`.

## any и all останавливаются рано

```python
def noisy(x):
    print("считаю", x)
    return x > 1

print(any(noisy(x) for x in [1, 2, 3, 4]))
```

- `any` прекращает перебор на первом `True` — остальные элементы даже не вычисляются. Со списком `[noisy(x) for x in ...]` посчитались бы все четыре.
- Вывод: `считаю 1`, `считаю 2`, `True`.

```viz
{"type": "trace", "title": "any останавливается на первом True", "code": "def noisy(x):\n    print(\"считаю\", x)\n    return x > 1\n\nprint(any(noisy(x) for x in [1, 2, 3, 4]))", "steps": [{"line": 5, "badge": "any берёт первый элемент", "note": "`any` просит у генератора первый элемент: `x = 1`."}, {"line": 2, "call": 5, "vars": {"x": "1"}, "out": "считаю 1"}, {"line": 3, "call": 5, "note": "`1 > 1` → `False`. Пока ничего не нашли — `any` просит следующий."}, {"line": 2, "call": 5, "vars": {"x": "2"}, "out": "считаю 2"}, {"line": 3, "call": 5, "badge": "найден True — стоп", "note": "`2 > 1` → `True`. Ответ уже ясен, дальше перебирать незачем."}, {"line": 5, "vars": {"x": null}, "out": "True", "note": "`3` и `4` **так и не посчитаны**. Со списком `[noisy(x) for x in ...]` напечатались бы все четыре «считаю»."}]}
```

## Другие примеры

```python
words = ["кот", "собака", "ёж"]
print(max(len(w) for w in words))
print(", ".join(w.upper() for w in words))
print(sorted((len(w), w) for w in words))
print(dict((w, len(w)) for w in words))
```

- Генераторное выражение подходит везде, где ждут итерируемое.
- Вывод: `6`, `КОТ, СОБАКА, ЁЖ`, `[(2, 'ёж'), (3, 'кот'), (6, 'собака')]`, `{'кот': 3, 'собака': 6, 'ёж': 2}`.

## Генератор или список

- Нужен **один проход** (сумма, проверка, запись) — генераторное выражение: меньше памяти.
- Нужно несколько проходов, `len`, индексы, срезы — списковое включение `[...]`.

## Итог

- `(expr for x in items if cond)` — ленивое выражение-генератор.
- Единственный аргумент — без лишних скобок: `sum(x for x in xs)`.
- `any`/`all` останавливаются рано.
- Один проход — генератор, много проходов — список.
'''),
    short=t(r'''
```py
(x * 2 for x in xs if x > 0)     # генератор, не список
sum(x for x in xs)
any(e.startswith("ERROR") for e in log)
all(r["ok"] for r in results)
", ".join(str(x) for x in xs)
max(len(w) for w in words)
```
'''),
    quiz=[
        q('Чем `(x for x in xs)` отличается от `[x for x in xs]`?',
            ['Ничем', 'Первое — ленивый генератор, второе — готовый список', 'Первое — кортеж', 'Второе быстрее всегда'],
            1, 'Круглые скобки — генератор.'),
        q('Сколько элементов проверит `any(x > 1 for x in [1, 2, 3])`?',
            ['1', '2', '3', '0'],
            1, 'Остановится на первом True.'),
        q('Можно ли писать `sum(x for x in xs)` без вторых скобок?',
            ['Нет', 'Да, если выражение — единственный аргумент', 'Только в Python 2', 'Только для sum'],
            1, 'Иначе нужны скобки.'),
    ],
),

# ---------- gen-pipeline ----------
'gen-pipeline': dict(
    full=t(r'''
## Зачем это нужно

Генераторы удобно соединять в **конвейер**: каждый этап берёт данные из предыдущего и передаёт дальше. Так обрабатывают логи, CSV, потоки событий: «прочитать → очистить → отфильтровать → преобразовать → посчитать». Каждый этап простой, а данные идут по одному элементу — памяти нужно мало.

## Цепочка генераторных выражений

```python
lines = ["  10 ", "", "abc", "25", "  ", "7"]

stripped = (s.strip() for s in lines)
non_empty = (s for s in stripped if s)
numbers = (int(s) for s in non_empty if s.isdigit())
print(sum(numbers))
```

- Каждая переменная — генератор поверх предыдущего. Пока не вызван `sum`, ничего не вычисляется.
- `isdigit()` — состоит ли строка только из цифр.
- Вывод: `42`.

## Порядок вычислений

```python
def source():
    for x in [1, 2]:
        print("взял", x)
        yield x

def double(items):
    for x in items:
        print("удвоил", x)
        yield x * 2

for result in double(source()):
    print("получил", result)
```

- Элемент проходит **весь** конвейер, прежде чем начнётся следующий. Это не «сначала всё взять, потом всё удвоить».
- Вывод: `взял 1`, `удвоил 1`, `получил 2`, `взял 2`, `удвоил 2`, `получил 4`.

```viz
{"type": "trace", "title": "Элемент проходит весь конвейер, потом следующий", "code": "def source():\n    for x in [1, 2]:\n        print(\"взял\", x)\n        yield x\n\ndef double(items):\n    for x in items:\n        print(\"удвоил\", x)\n        yield x * 2\n\nfor result in double(source()):\n    print(\"получил\", result)", "intro": "Три участника: `source` выдаёт числа, `double` их удваивает, цикл `for` печатает. Смотри, кто кого ждёт.", "steps": [{"line": 11, "badge": "for просит элемент у double", "note": "Генераторы созданы, но ещё ничего не выполнили. `for` просит первый элемент у `double`."}, {"line": 7, "call": 11, "badge": "double просит элемент у source", "note": "`double` сам ничего не имеет — он просит элемент у `source`."}, {"line": 3, "call": 7, "vars": {"x в source": "1"}, "out": "взял 1"}, {"line": 4, "call": 7, "badge": "⏸ source на паузе", "note": "`source` отдал `1` и замер."}, {"line": 8, "call": 11, "vars": {"x в double": "1"}, "out": "удвоил 1"}, {"line": 9, "call": 11, "badge": "⏸ double на паузе", "note": "`double` отдал `2` и тоже замер."}, {"line": 12, "vars": {"result": "2"}, "out": "получил 2", "badge": "⏸ source и double — оба на паузе", "note": "Первый элемент прошёл **весь** конвейер. Второй ещё даже не взят."}, {"line": 7, "call": 11, "badge": "▶ всё продолжается с пауз", "note": "Следующая итерация `for` будит `double`, а тот — `source`."}, {"line": 3, "call": 7, "vars": {"x в source": "2"}, "out": "взял 2"}, {"line": 8, "call": 11, "vars": {"x в double": "2"}, "out": "удвоил 2"}, {"line": 12, "vars": {"result": "4"}, "out": "получил 4", "badge": "", "note": "Порядок: взял → удвоил → получил, и так для каждого элемента. Не «сначала всё взять, потом всё удвоить»."}]}
```

## Этапы-функции

```python
def read(lines):
    for line in lines:
        yield line.strip()

def skip_comments(lines):
    for line in lines:
        if line and not line.startswith("#"):
            yield line

def parse(lines):
    for line in lines:
        key, value = line.split("=", 1)
        yield key, value

raw = ["# конфиг", " url=http://a ", "", "timeout=5"]
print(dict(parse(skip_comments(read(raw)))))
```

- Каждая функция-этап принимает итерируемое и возвращает генератор. Их можно тестировать по отдельности и переставлять.
- `dict(...)` из генератора пар — готовый словарь.
- Вывод: `{'url': 'http://a', 'timeout': '5'}`.

## Бесконечный источник

```python
def numbers():
    n = 0
    while True:
        n += 1
        yield n

squares = (n * n for n in numbers())
big = (s for s in squares if s > 50)
print(next(big), next(big))
```

- Конвейер над бесконечным источником безопасен: считается только то, что запросили.
- Вывод: `64 81`.

## Состояние в этапе

```python
def dedupe(items):
    seen = set()
    for x in items:
        if x not in seen:
            seen.add(x)
            yield x

print(list(dedupe([3, 1, 3, 2, 1])))
```

- Этап может хранить состояние между элементами — здесь множество уже встреченных.
- Вывод: `[3, 1, 2]`.

## Итог

- Конвейер: `этап3(этап2(этап1(источник)))` или цепочка выражений.
- Элементы идут по одному через все этапы.
- Этапы простые, тестируемые, переставляемые.
- Работает с бесконечными и огромными источниками.
'''),
    short=t(r'''
```py
def stage(items):              # шаблон этапа
    for x in items:
        if keep(x):
            yield transform(x)

result = sum(stage3(stage2(stage1(source))))

clean = (s.strip() for s in lines)
nums  = (int(s) for s in clean if s.isdigit())
```
'''),
    quiz=[
        q('Как элементы проходят конвейер из генераторов?',
            ['Сначала все через первый этап, потом через второй', 'По одному через все этапы', 'Случайно', 'Параллельно'],
            1, 'Поэтому памяти нужно мало.'),
        q('Когда начинаются вычисления в цепочке генераторных выражений?',
            ['При создании', 'Когда конечный потребитель запрашивает элементы', 'Сразу после первой строки', 'Никогда'],
            1, 'Например, sum или for.'),
        q('Можно ли строить конвейер над бесконечным генератором?',
            ['Нет', 'Да, если потребитель берёт ограниченное число элементов', 'Только с list', 'Только в Python 3.12'],
            1, 'Ленивость это позволяет.'),
    ],
),

# ---------- gen-m2-l2 ----------
'gen-m2-l2': dict(
    full=t(r'''
## Зачем это нужно

Часто генератор должен выдать все элементы другого итерируемого или другого генератора — для этого есть `yield from`. А модуль `itertools` — набор готовых «кубиков» для работы с итераторами: бесконечные счётчики, срезы, комбинации параметров.

## yield from

```python
def both():
    yield from [1, 2]
    yield from "ab"

print(list(both()))
```

- `yield from итерируемое` — выдать все его элементы по одному. Короткая запись `for x in items: yield x`.
- Вывод: `[1, 2, 'a', 'b']`.

## Рекурсивный обход

```python
def walk(tree, depth=0):
    yield "  " * depth + tree["name"]
    for child in tree.get("children", []):
        yield from walk(child, depth + 1)

site = {"name": "главная", "children": [
    {"name": "каталог", "children": [{"name": "товар"}]},
    {"name": "корзина"},
]}
for line in walk(site):
    print(line)
```

- Генератор вызывает сам себя для детей и передаёт наверх всё, что они выдали.
- Так обходят деревья: структуру сайта, вложенный JSON, папки.
- Вывод: `главная`, `  каталог`, `    товар`, `  корзина`.

## count и islice

```python
from itertools import count, islice

print(list(islice(count(10, 5), 4)))
print(list(islice("abcdefg", 2, 6, 2)))
```

- `count(start, step)` — бесконечный счётчик.
- `islice(итерируемое, stop)` или `islice(it, start, stop, step)` — срез для любых итераторов (обычный `[a:b]` у генераторов не работает).
- Вывод: `[10, 15, 20, 25]`, `['c', 'e']`.

## product: все комбинации

```python
from itertools import product

for browser, os in product(["chrome", "firefox"], ["win", "mac"]):
    print(browser, os)
```

- `product(a, b, ...)` — декартово произведение: каждый элемент первого с каждым элементом второго. Удобно для матрицы кроссбраузерных прогонов.
- Вывод: `chrome win`, `chrome mac`, `firefox win`, `firefox mac`.

## cycle и repeat

```python
from itertools import cycle, repeat, islice

print(list(islice(cycle(["A", "B"]), 5)))
print(list(repeat("x", 3)))
```

- `cycle(items)` — повторять по кругу бесконечно (например, распределять задачи между воркерами).
- `repeat(x, n)` — значение `n` раз.
- Вывод: `['A', 'B', 'A', 'B', 'A']`, `['x', 'x', 'x']`.

## Итог

- `yield from it` — выдать всё из `it`; удобно для рекурсии.
- `count`, `cycle`, `repeat` — бесконечные источники.
- `islice` — срез итератора.
- `product` — все комбинации параметров.
'''),
    short=t(r'''
```py
yield from items              # = for x in items: yield x
yield from walk(child)        # рекурсия

from itertools import count, islice, product, cycle, repeat
count(10, 5)                  # 10, 15, 20, …
islice(it, 5)                 # первые 5
islice(it, 2, 6, 2)
product(browsers, oses)       # все пары
cycle(["A", "B"])             # A B A B …
repeat("x", 3)
```
'''),
    quiz=[
        q('Что делает `yield from [1, 2]`?',
            ['Выдаёт список целиком', 'Выдаёт 1, затем 2', 'Возвращает список', 'Ошибка'],
            1, 'По одному элементу.'),
        q('Как взять первые 5 элементов бесконечного генератора?',
            ['g[:5]', 'itertools.islice(g, 5)', 'list(g)[:5]', 'g.take(5)'],
            1, 'Срезы у генераторов не работают.'),
        q('Что даёт `product(["a", "b"], [1, 2])`?',
            ['(a,1), (b,2)', 'Все 4 пары', 'a, b, 1, 2', 'Произведение чисел'],
            1, 'Декартово произведение.'),
    ],
),

# ---------- gen-itertools ----------
'gen-itertools': dict(
    full=t(r'''
## Зачем это нужно

В `itertools` есть ещё много полезного: склеить несколько последовательностей, получить накопленные суммы, пары соседей, разбить на пачки, сгруппировать подряд идущие одинаковые элементы. Всё это ленивое и работает с любыми итераторами.

## chain, accumulate, pairwise

```python
from itertools import chain, accumulate, pairwise

print(list(chain([1, 2], (3,), "ab")))
print(list(accumulate([1, 2, 3, 4])))
print(list(pairwise([10, 13, 19])))
```

- `chain(a, b, ...)` — перебрать последовательности одну за другой без склейки в новый список.
- `accumulate(xs)` — накопленные суммы (можно передать свою функцию, например `max`).
- `pairwise(xs)` — пары соседних элементов (Python 3.10+). Удобно для разниц между замерами.
- Вывод: `[1, 2, 3, 'a', 'b']`, `[1, 3, 6, 10]`, `[(10, 13), (13, 19)]`.

## takewhile, dropwhile, batched

```python
from itertools import takewhile, dropwhile, batched

nums = [1, 3, 5, 8, 9, 11]
print(list(takewhile(lambda n: n % 2, nums)))
print(list(dropwhile(lambda n: n % 2, nums)))
print(list(batched("abcdefg", 3)))
```

- `takewhile(условие, it)` — брать, **пока** условие истинно; на первом ложном — стоп.
- `dropwhile(условие, it)` — пропускать, пока истинно, дальше — всё.
- `batched(it, n)` — пачки по `n` элементов в виде кортежей (Python 3.12+). Для отправки данных в API порциями.
- `n % 2` — остаток 1 (нечётное) считается истиной.
- Вывод: `[1, 3, 5]`, `[8, 9, 11]`, `[('a', 'b', 'c'), ('d', 'e', 'f'), ('g',)]`.

## groupby: подряд идущие группы

```python
from itertools import groupby

log = ["ERROR", "ERROR", "INFO", "ERROR", "INFO", "INFO"]
print([(k, len(list(g))) for k, g in groupby(log)])

words = sorted(["кот", "кит", "собака", "сом"], key=lambda w: w[0])
print({k: list(g) for k, g in groupby(words, key=lambda w: w[0])})
```

- `groupby(it, key=...)` выдаёт пары `(ключ, группа)` для **подряд идущих** элементов с одинаковым ключом. Группа — итератор; `list(g)` превращает его в список.
- Чтобы сгруппировать все одинаковые, данные сначала сортируют по тому же ключу.
- Вывод: `[('ERROR', 2), ('INFO', 1), ('ERROR', 1), ('INFO', 2)]`, `{'к': ['кот', 'кит'], 'с': ['собака', 'сом']}`.

## combinations и permutations

```python
from itertools import combinations, permutations

print(list(combinations(["api", "ui", "db"], 2)))
print(len(list(permutations("abc"))))
```

- `combinations(it, r)` — все наборы по `r` без учёта порядка (пары сервисов для интеграционных тестов).
- `permutations(it)` — все перестановки с учётом порядка.
- Вывод: `[('api', 'ui'), ('api', 'db'), ('ui', 'db')]`, `6`.

```viz
{"type": "itertools", "title": "Песочница itertools: выбери функцию и меняй вход", "fn": "takewhile"}
```

## Итог

- `chain` — склеить, `accumulate` — накопить, `pairwise` — соседние пары.
- `takewhile` / `dropwhile` — до/после условия; `batched` — пачки.
- `groupby` — группы подряд идущих (сортируй заранее).
- `combinations`, `permutations`, `product` — перебор вариантов.
'''),
    short=t(r'''
```py
from itertools import (chain, accumulate, pairwise, takewhile,
                       dropwhile, batched, groupby, combinations, permutations)
chain(a, b)                 # a, затем b
accumulate([1, 2, 3])       # 1 3 6
pairwise([1, 5, 7])         # (1,5) (5,7)
takewhile(f, it); dropwhile(f, it)
batched(it, 100)            # кортежи по 100 (3.12+)
groupby(sorted(xs, key=k), key=k)   # (ключ, итератор группы)
combinations(xs, 2); permutations(xs)
```
'''),
    quiz=[
        q('Что делает `groupby` без предварительной сортировки?',
            ['Группирует все одинаковые', 'Группирует только подряд идущие одинаковые', 'Сортирует сам', 'Ошибка'],
            1, 'Сортируй по тому же ключу заранее.'),
        q('Что вернёт `list(pairwise([1, 2, 3]))`?',
            ['[(1, 2), (2, 3)]', '[(1, 2), (3,)]', '[1, 2, 3]', '[(1, 3)]'],
            0, 'Пары соседних.'),
        q('Чем `takewhile` отличается от фильтра?',
            ['Ничем', 'Останавливается на первом неподходящем элементе', 'Пропускает первый', 'Работает с конца'],
            1, 'Дальше не смотрит.'),
    ],
),

}
