"""Теория модуля «map, filter, reduce» темы «lambda».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- lam-m2-l1 ----------
'lam-m2-l1': dict(
    full=t(r'''
## Зачем это нужно

`map` и `filter` — функции «высшего порядка»: они принимают функцию и применяют её к коллекции. Вместе с лямбдой это короткий способ преобразовать или отфильтровать данные. Подробно они разобраны в теме «sorted, filter и map»; здесь — упор на связку с лямбдами.

## map и filter с лямбдой

```python
print(list(map(lambda x: x ** 2, [1, 2, 3, 4])))
print(list(filter(lambda x: x % 2, [1, 2, 3, 4])))
```

- `map(f, items)` — `f(x)` для каждого элемента; `filter(f, items)` — элементы, где `f(x)` истинно.
- `x % 2` — 1 (истина) для нечётных, 0 (ложь) для чётных.
- Оба возвращают **ленивый итератор** — для списка `list(...)`.
- Вывод: `[1, 4, 9, 16]`, `[1, 3]`.

## Не только лямбды

```python
words = ["api", "UI", "Docker"]
print(list(map(str.upper, words)))
print(list(map(len, words)))
```

- Если функция уже есть — передай её по имени, лямбда не нужна: `map(len, ...)`, а не `map(lambda w: len(w), ...)`.
- Вывод: `['API', 'UI', 'DOCKER']`, `[3, 2, 6]`.

## Две коллекции

```python
print(list(map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30])))
```

- Лямбда с двумя параметрами получает элементы попарно. Вывод: `[11, 22, 33]`.

## Цепочка filter → map

```python
users = [
    {"email": "Anna@Mail.ru", "active": True},
    {"email": "bob@mail.ru", "active": False},
]
active = filter(lambda u: u["active"], users)
print(list(map(lambda u: u["email"].lower(), active)))
print(list(map(lambda s: float(s.replace(",", ".")), ["12,5", "3"])))
```

- Сначала отбор, потом преобразование; промежуточного списка нет — `map` берёт значения прямо из итератора `filter`.
- Вывод: `['anna@mail.ru']`, `[12.5, 3.0]`.

## То же включением

```python
nums = [1, 2, 3, 4]
print(list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, nums))))
print([x * x for x in nums if x % 2 == 0])
```

- Результат одинаковый. С лямбдами включение обычно читается легче; `map`/`filter` важно уметь **читать** в чужом коде.
- Вывод: `[4, 16]` дважды.

## Итог

- `map(lambda x: ..., items)` — преобразовать; `filter(lambda x: ..., items)` — отобрать.
- Готовую функцию передают без лямбды: `map(len, ...)`.
- Результат — итератор; для списка `list(...)`.
- Цепочка `map(..., filter(...))` эквивалентна включению с `if`.
'''),
    short=t(r'''
```py
list(map(lambda x: x ** 2, nums))
list(filter(lambda x: x % 2, nums))
list(map(len, words))                    # готовая функция — без lambda
list(map(lambda a, b: a + b, xs, ys))
list(map(lambda u: u["email"], filter(lambda u: u["active"], users)))
```
'''),
    quiz=[
        q('Что вернёт `list(filter(lambda x: x > 2, [1, 3, 5]))`?',
            ['`[1]`', '`[3, 5]`', '`[True, True]`', 'Ошибка'],
            1, 'Элементы, где условие истинно.'),
        q('Что лучше: `map(lambda w: len(w), words)` или `map(len, words)`?',
            ['Первое', 'Второе — функция уже есть', 'Одинаково', 'Оба ошибка'],
            1, 'Лишняя лямбда не нужна.'),
        q('Что возвращает `map` без `list`?',
            ['Список', 'Ленивый итератор', 'Кортеж', 'None'],
            1, 'Значения — по запросу.'),
    ],
),

# ---------- lam-m2-l2 ----------
'lam-m2-l2': dict(
    full=t(r'''
## Зачем это нужно

`reduce` **сворачивает** коллекцию в одно значение: произведение, строку, максимум. А лямбды, созданные внутри функции, умеют **запоминать** её переменные — это замыкания, на которых строятся «фабрики» функций. Обе идеи часто встречаются вместе с лямбдами.

## reduce

```python
from functools import reduce
print(reduce(lambda acc, x: acc * x, [1, 2, 3, 4], 1))
print(reduce(lambda acc, x: acc + x, ["a", "b", "c"], ""))
```

- `reduce` живёт в модуле `functools` — его нужно импортировать.
- `reduce(f, items, start)`: `acc = start`, затем для каждого `x` — `acc = f(acc, x)`. Результат — последний `acc`.
- Произведение: `((((1·1)·2)·3)·4) = 24`. Вывод: `24`, `abc`.

```python
from functools import reduce
print(reduce(lambda a, b: a if a > b else b, [3, 9, 2]))
```

- Максимум: на каждом шаге оставляем большее. Без начального значения `acc` — первый элемент. Вывод: `9`.

## Замыкание: функция, возвращающая лямбду

```python
def adder(n):
    return lambda x: x + n

plus5 = adder(5)
plus10 = adder(10)
print(plus5(1), plus10(1))
```

- Лямбда, созданная внутри `adder`, запоминает `n` из её вызова — это **замыкание** (тема «Область видимости»).
- Каждый вызов `adder` создаёт свою функцию со своим `n`. Вывод: `6 11`.

```python
def make_validator(min_len):
    return lambda s: len(s) >= min_len

check8 = make_validator(8)
print(check8("12345678"), check8("123"))

def compose(f, g):
    return lambda x: f(g(x))

print(compose(lambda x: x + 1, lambda x: x * 2)(5))
```

- Фабрика проверок; композиция двух функций: сначала `g`, потом `f`.
- Вывод: `True False`, `11`.

## Ловушка позднего связывания

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])
fixed = [lambda i=i: i for i in range(3)]
print([f() for f in fixed])
```

- Лямбды запоминают **переменную** `i`, а не её значение: к моменту вызова она равна 2.
- `i=i` — значение по умолчанию вычисляется при создании и фиксирует текущее `i`.
- Вывод: `[2, 2, 2]`, `[0, 1, 2]`.

## Итог

- `from functools import reduce`; `reduce(f, items, start)` сворачивает коллекцию.
- Лямбда внутри функции помнит её переменные — замыкание; так делают фабрики функций.
- Лямбды в цикле видят последнее значение переменной — фиксируй `x=x`.
'''),
    short=t(r'''
```py
from functools import reduce
reduce(lambda acc, x: acc * x, nums, 1)   # произведение
reduce(lambda a, b: a if a > b else b, nums)
def adder(n):
    return lambda x: x + n               # замыкание помнит n
[lambda i=i: i for i in range(3)]        # фиксация значения
```
'''),
    quiz=[
        q('Что вернёт `reduce(lambda a, x: a + x, [1, 2, 3], 10)`?',
            ['`6`', '`16`', '`10`', 'Ошибка'],
            1, '10 + 1 + 2 + 3.'),
        q('Откуда импортируют reduce?',
            ['Встроенная функция', '`from functools import reduce`', '`from operator import reduce`', '`import reduce`'],
            1, 'В Python 3 — из functools.'),
        q('Что вернёт `adder(3)(4)` для `def adder(n): return lambda x: x + n`?',
            ['`3`', '`7`', 'Функцию', 'Ошибка'],
            1, 'Лямбда помнит n = 3.'),
    ],
),

# ---------- lam-reduce ----------
'lam-reduce': dict(
    full=t(r'''
## Зачем это нужно

`reduce` — универсальный «свёртыватель»: из списка можно получить число, строку, словарь, даже функцию. Нужно понимать, как он проходит по элементам, зачем начальное значение и когда вместо `reduce` лучше `sum`, `max` или цикл.

## Начальное значение

```python
from functools import reduce
print(reduce(lambda a, b: a + b, [1, 2, 3, 4]))
print(reduce(lambda a, b: a + b, [5]))
print(reduce(lambda a, b: a + b, [], 0))
try:
    reduce(lambda a, b: a + b, [])
except TypeError:
    print("пустой список без начального значения")
```

- Без начального значения первый элемент становится `acc`, функция начинает со второго.
- Один элемент без начального — он и возвращается, функция не вызывается ни разу.
- Пустой список без начального — `TypeError`; с начальным — возвращается оно само.
- Вывод: `10`, `5`, `0`, `пустой список без начального значения`.

Правило: **передавай начальное значение**, если список может быть пустым.

## Шаги reduce

```python
from functools import reduce

def step(acc, x):
    print(f"acc={acc}, x={x}")
    return acc * 10 + x

print(reduce(step, [1, 2, 3]))
```

- Функция вызывается `len - 1` раз (без начального значения): `1*10+2 = 12`, `12*10+3 = 123`.
- Вывод: `acc=1, x=2`, `acc=12, x=3`, `123`.

```viz
{"type": "trace", "auto": true, "title": "reduce по шагам", "code": "from functools import reduce\n\ndef add(total, x):\n    return total + x\n\nprint(reduce(add, [5, 10, 20], 0))", "notes": {"6": "reduce передаёт в функцию накопленное `total` и очередной `x`, ответ становится новым `total`: 0 → 5 → 15 → 35."}}
```

## Накопление сложных значений

```python
from functools import reduce
words = ["a", "bb", "a"]
print(reduce(lambda d, w: {**d, w: d.get(w, 0) + 1}, words, {}))
print(reduce(lambda acc, lst: acc + lst, [[1, 2], [3], []], []))
print(reduce(lambda best, w: w if len(w) > len(best) else best, ["ab", "abcd", "xyzw"], ""))
```

- Накопитель может быть словарём, списком, строкой — каждый шаг возвращает **новый** накопитель.
- Вывод: `{'a': 2, 'bb': 1}`, `[1, 2, 3]`, `abcd`.

## Свёртка функций

```python
from functools import reduce
funcs = [lambda x: x + 1, lambda x: x * 10]
pipeline = reduce(lambda f, g: lambda x: g(f(x)), funcs, lambda x: x)
print(pipeline(2))
```

- Начинаем с функции «ничего не делать» `lambda x: x` и на каждом шаге оборачиваем: новая функция сначала применяет старую, потом очередную.
- Вывод: `30` — (2 + 1) × 10.

## Когда не нужен reduce

- Сумма — `sum(...)`, максимум — `max(...)`, склейка строк — `"".join(...)`, «все/хоть один» — `all`/`any`: они короче и понятнее.
- Сложная логика — обычный цикл с накопителем читается лучше.
- `reduce` хорош, когда нужна именно «свёртка» своей операцией: цифры → число, композиция функций, слияние словарей.

## Итог

- `reduce(f, items, start)` — `acc = f(acc, x)` для каждого элемента.
- Без `start` первый элемент — начальный `acc`; пустой список без `start` — `TypeError`.
- Накопитель может быть любым: число, словарь, список, функция.
- Для суммы, максимума, склейки есть готовые функции — используй их.
'''),
    short=t(r'''
```py
reduce(f, items)          # acc = первый элемент
reduce(f, items, start)   # acc = start (нужно для пустых)
reduce(f, [])             # TypeError
reduce(lambda acc, d: acc * 10 + d, digits, 0)
reduce(lambda acc, d: {**acc, **d}, dicts, {})
# sum, max, "".join, all, any — вместо reduce, где можно
```
'''),
    quiz=[
        q('Что вернёт `reduce(lambda a, b: a * b, [7])`?',
            ['`0`', '`7`', '`49`', 'Ошибка'],
            1, 'Один элемент — он и есть результат.'),
        q('Что будет при `reduce(lambda a, b: a + b, [])`?',
            ['`0`', '`TypeError`', '`None`', '`[]`'],
            1, 'Нужно начальное значение.'),
        q('Что лучше для суммы списка?',
            ['`reduce(lambda a, b: a + b, nums, 0)`', '`sum(nums)`', 'Одинаково', 'Цикл while'],
            1, 'Готовая функция понятнее.'),
    ],
),

# ---------- lam-operator ----------
'lam-operator': dict(
    full=t(r'''
## Зачем это нужно

Многие лямбды повторяют стандартные операции: `lambda a, b: a + b`, `lambda x: x[1]`, `lambda s: int(s, base=2)`. Для них в стандартной библиотеке есть готовые функции: модуль **`operator`** и **`functools.partial`**. Они короче, быстрее и часто понятнее.

## operator: операторы как функции

```python
import operator
from functools import reduce
print(operator.add(2, 3), operator.mul(4, 5))
print(reduce(operator.mul, [1, 2, 3, 4]))
```

- `operator.add(a, b)` — то же, что `a + b`; `operator.mul` — `a * b`. Есть `sub`, `truediv`, `eq`, `lt` и другие.
- Удобно передавать туда, где нужна функция двух аргументов: `reduce(operator.mul, ...)` вместо `reduce(lambda a, b: a * b, ...)`.
- Вывод: `5 20`, `24`.

## itemgetter: «достать элемент»

```python
from operator import itemgetter
pairs = [("b", 2), ("a", 3)]
print(sorted(pairs, key=itemgetter(0)))
get_name = itemgetter("name")
print(get_name({"name": "Аня", "age": 25}))
print(itemgetter(0, 2)("abc"))
users = [{"name": "Аня"}, {"name": "Боря"}]
print(list(map(itemgetter("name"), users)))
```

- `itemgetter(k)` — функция `lambda x: x[k]`: элемент по индексу или ключу.
- С несколькими аргументами возвращает кортеж — готовый ключ по нескольким полям.
- Вывод: `[('a', 3), ('b', 2)]`, `Аня`, `('a', 'c')`, `['Аня', 'Боря']`.

## partial: зафиксировать аргументы

```python
from functools import partial

def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube = partial(power, exp=3)
print(square(5), cube(2))
int2 = partial(int, base=2)
print(int2("101"))
```

- `partial(функция, аргументы...)` — новая функция, у которой часть аргументов уже подставлена.
- `partial(int, base=2)` — «разобрать двоичную строку».
- Вывод: `25 8`, `5`.

```python
from functools import partial

def log(message, level="DEBUG"):
    return f"[{level}] {message}"

log_info = partial(log, level="INFO")
print(log("x"), log_info("старт"))
```

- `partial` против лямбды: `partial(log, level="INFO")` ≈ `lambda m: log(m, level="INFO")`, но у `partial` видно, какая функция и какие аргументы зафиксированы.
- Вывод: `[DEBUG] x [INFO] старт`.

## Итог

- `operator.add`, `mul`, … — операторы как функции для `reduce`, `map`, `sorted`.
- `itemgetter(k)` — `lambda x: x[k]`; с несколькими ключами — кортеж.
- `partial(f, ...)` — новая функция с зафиксированными аргументами.
- Готовые функции часто заменяют короткие лямбды.
'''),
    short=t(r'''
```py
import operator
reduce(operator.mul, nums, 1)          # вместо lambda a, b: a * b
from operator import itemgetter
sorted(pairs, key=itemgetter(1))       # вместо lambda p: p[1]
map(itemgetter("name"), users)
from functools import partial
from_bin = partial(int, base=2)        # from_bin("101") -> 5
```
'''),
    quiz=[
        q('Чему эквивалентен `itemgetter(1)`?',
            ['`lambda x: x + 1`', '`lambda x: x[1]`', '`lambda x: 1`', '`lambda x: x * 1`'],
            1, 'Элемент по индексу 1.'),
        q('Что вернёт `partial(pow, 2)(10)`?',
            ['`100`', '`1024`', '`20`', 'Ошибка'],
            1, 'pow(2, 10).'),
        q('Что делает `operator.add(2, 3)`?',
            ['Ошибка', 'Возвращает 5', 'Складывает на месте', 'Возвращает функцию'],
            1, 'Оператор + как функция.'),
    ],
),
}
