"""Теория модуля «Вложенные функции» темы «Область видимости».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- scp-m2-l1: Правило LEGB ----------
'scp-m2-l1': dict(
    full=t(r'''
## Зачем это нужно

Когда в коде встречается имя, Python должен решить, **какую** переменную оно означает: локальную, глобальную, встроенную функцию? Порядок поиска описывается правилом **LEGB**. Зная его, ты всегда сможешь сказать, откуда берётся значение.

## Четыре области

Python ищет имя по очереди в четырёх областях, от ближней к дальней, и берёт **первое найденное**:

1. **L — Local**: локальные имена текущей функции.
2. **E — Enclosing**: локальные имена **объемлющих** функций (если функция вложена в другую).
3. **G — Global**: глобальные имена модуля.
4. **B — Built-in**: встроенные имена Python: `len`, `print`, `sum`, `int`…

Если имя не найдено нигде — `NameError`.

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        return x
    return inner()

print(outer())
```

- В `inner` нет своей `x` (L) → ищем в объемлющей `outer` (E) и находим. Вывод: `enclosing`.

```viz
{"type": "lookup", "title": "LEGB: где Python найдёт имя", "code": "x = \"глобальная\"\n\ndef outer():\n    y = \"из outer\"\n    def inner():\n        z = \"локальная\"\n        print(z, y, x, len)\n    inner()", "ask": "Какое имя ищет inner()?", "queries": ["z", "y", "x", "len", "w"], "levels": [{"name": "L — локальная", "sub": "inner()", "names": {"z": "'локальная'"}}, {"name": "E — объемлющая", "sub": "outer()", "names": {"y": "'из outer'", "inner": "функция"}}, {"name": "G — глобальная", "sub": "модуль", "names": {"x": "'глобальная'", "outer": "функция"}}, {"name": "B — встроенные", "sub": "builtins", "names": {"len": "функция", "print": "функция", "range": "класс"}}]}
```

## Каждая область по очереди

```python
x = "global"

def outer():
    def inner():
        return x
    return inner()

def outer2():
    x = "enclosing"
    def inner():
        x = "local"
        return x
    return inner(), x

print(outer())
print(outer2())
```

- `outer`: ни в L, ни в E нет `x` → G: `global`.
- `outer2`: в `inner` есть своя `x` (L) — берётся она; сама `outer2` видит свою `x`.
- Вывод: `global`, `('local', 'enclosing')`.

## Ближайшая объемлющая

```python
x = "G"

def a():
    x = "E1"
    def b():
        def c():
            return x
        return c()
    return b()

print(a())
```

- В `c` и `b` нет `x`; поиск идёт наружу **по уровням вложенности** и останавливается на ближайшей — в `a`. Вывод: `E1`.

## B — встроенные имена

```python
print(len("abc"), sum([1, 2]), max(3, 7))
```

- `len`, `sum`, `max` не определены ни локально, ни глобально — их находят в последней области, встроенной. Вывод: `3 3 7`.
- Если создать глобальную (или локальную) переменную с таким же именем, она **затенит** встроенную — поиск остановится раньше (урок «Затенение имён»).

## Одна переменная — разные области одновременно

```python
level = "G"

def which_scope():
    level = "E"
    def inner():
        level = "L"
        return level
    return [inner(), level, globals()["level"]]

print(which_scope())
```

- `globals()` — словарь глобальных имён модуля; `globals()["level"]` — глобальная, даже когда её затеняют.
- Вывод: `['L', 'E', 'G']`.

## Присваивание во вложенной функции

Правило «присваивание делает имя локальным» действует и здесь:

```python
def price_list(prices, rate):
    def with_rate(p):
        r = rate / 100
        return round(p * (1 + r), 2)
    return [with_rate(p) for p in prices]

print(price_list([100, 50], 20))
```

- `rate` только **читается** во вложенной функции — берётся из E. Если бы там было `rate = rate / 100`, `rate` стала бы локальной для `with_rate`, и получился бы `UnboundLocalError`. Поэтому результат — в новое имя `r`.
- Вывод: `[120.0, 60.0]`.

## Итог

- Порядок поиска имени: **L**ocal → **E**nclosing → **G**lobal → **B**uilt-in; берётся первое найденное.
- Не нашли нигде — `NameError`.
- Enclosing — локальные объемлющих функций, от ближайшей наружу.
- Присваивание во вложенной функции делает имя локальным для неё.
'''),
    short=t(r'''
```py
# поиск имени: Local → Enclosing → Global → Built-in
x = "G"
def outer():
    x = "E"
    def inner():
        return x     # нет в L → нашли в E
    return inner()
globals()["x"]       # глобальная, даже если затенена
```
'''),
    quiz=[
        q('В каком порядке Python ищет имя?',
            ['Global → Local → Built-in', 'Local → Enclosing → Global → Built-in', 'Built-in → Global → Local', 'Только Local'],
            1, 'LEGB.'),
        q('Где Python находит `len`, если такого имени нет ни в функции, ни в модуле?',
            ['Enclosing', 'Built-in', 'Нигде — NameError', 'Global'],
            1, 'Встроенные имена — последняя область.'),
        q('Что вернёт `inner()`, если `x` есть и в `outer`, и глобально, а в `inner` нет?',
            ['Глобальную', 'Из outer', 'Ошибку', 'None'],
            1, 'Enclosing ближе, чем Global.'),
    ],
),

# ---------- scp-nested: Вложенные функции ----------
'scp-nested': dict(
    full=t(r'''
## Зачем это нужно

Функцию можно определить **внутри** другой функции. Зачем? Чтобы спрятать вспомогательный код, который нужен только одной функции, и чтобы этот помощник мог пользоваться её параметрами без передачи аргументов. А ещё вложенные функции — основа замыканий и декораторов.

## Вложенная функция видна только внутри

```python
def outer():
    def helper(x):
        return x * 2
    return helper(5)

print(outer())
try:
    helper(1)
except NameError:
    print("helper снаружи не виден")
```

- `def helper` внутри `outer` — это просто **локальная переменная** `helper`, значение которой — функция.
- Снаружи имени `helper` нет, как и любой другой локальной. Вывод: `10`, `helper снаружи не виден`.
- Каждый вызов `outer` создаёт `helper` заново.

## Доступ к параметрам внешней функции

```python
def greet_all(greeting, names):
    def one(name):
        return f"{greeting}, {name}!"
    return [one(n) for n in names]

print(greet_all("Привет", ["Аня", "Боря"]))
```

- `one` получает только `name`, а `greeting` берёт из объемлющей области (буква E в LEGB) — передавать его каждый раз не нужно.
- Вывод: `['Привет, Аня!', 'Привет, Боря!']`.

## Значение читается в момент вызова

```python
def outer():
    msg = "раз"
    def show():
        return msg
    first = show()
    msg = "два"
    return first, show()

print(outer())
```

- Вложенная функция запоминает не значение, а **переменную** внешней функции. При каждом вызове читается её текущее значение.
- Вывод: `('раз', 'два')`.

## Помощники без параметров

```python
def stats(nums):
    def mean():
        return sum(nums) / len(nums)
    def spread():
        return max(nums) - min(nums)
    if not nums:
        return (0, 0)
    return (mean(), spread())

print(stats([2, 4, 9]))
```

- Обе вложенные функции работают с `nums` внешней функции.
- Функции определены до проверки `if not nums`, но **вызываются** только после неё — поэтому деления на ноль нет.
- Вывод: `(5.0, 7)`.

## Рекурсивный помощник и общий результат

```python
def flatten(data):
    result = []
    def walk(item):
        if isinstance(item, list):
            for x in item:
                walk(x)
        else:
            result.append(item)
    walk(data)
    return result

print(flatten([1, [2, [3, 4]], 5]))
```

- `walk` вызывает сама себя и добавляет числа в `result` внешней функции.
- `result.append(...)` — вызов метода, а не присваивание, поэтому `result` остаётся «внешней» переменной и ничего объявлять не нужно.
- Вывод: `[1, 2, 3, 4, 5]`.

## Когда выносить наружу

Вложенная функция уместна, если помощник:
- нужен только одной функции;
- пользуется её параметрами;
- короткий.

Если помощник пригодится в другом месте или его нужно отдельно тестировать — сделай его обычной функцией модуля.

## Итог

- `def` внутри функции создаёт локальную функцию — снаружи её не видно.
- Вложенная функция читает переменные внешней (E в LEGB) в момент своего вызова.
- Изменять внешние **объекты** (`append`) можно свободно; переприсвоить внешнее **имя** — только с `nonlocal` (следующий урок).
- Вложенные функции прячут детали реализации и избавляют от передачи лишних аргументов.
'''),
    short=t(r'''
```py
def outer(greeting, names):
    def one(name):                    # видна только внутри outer
        return f"{greeting}, {name}"  # greeting — из объемлющей области
    return [one(n) for n in names]
def flatten(data):
    result = []
    def walk(item):
        result.append(item)           # метод — nonlocal не нужен
```
'''),
    quiz=[
        q('Можно ли вызвать вложенную функцию снаружи внешней?',
            ['Да', 'Нет — это локальное имя', 'Только с global', 'Только если она без параметров'],
            1, 'NameError.'),
        q('Какое значение внешней переменной увидит вложенная функция?',
            ['На момент def', 'На момент вызова', 'Всегда первое', 'None'],
            1, 'Читается текущее значение.'),
        q('Нужен ли `nonlocal`, чтобы вызвать `result.append(x)` для списка внешней функции?',
            ['Да', 'Нет — это вызов метода, не присваивание', 'Только в рекурсии', 'Нужен global'],
            1, 'Объект меняется, имя не переприсваивается.'),
    ],
),

# ---------- scp-m2-l2: nonlocal ----------
'scp-m2-l2': dict(
    full=t(r'''
## Зачем это нужно

Вложенная функция может **читать** переменные внешней, но если попытаться **присвоить** — получится новая локальная переменная (или `UnboundLocalError`). Чтобы вложенная функция могла изменить переменную объемлющей функции, есть объявление **`nonlocal`** — «родственник» `global`, но для вложенных функций.

## Проблема

```python
def outer():
    count = 0
    def inc():
        try:
            count += 1
        except UnboundLocalError:
            return "UnboundLocalError"
    return inc()

print(outer())
```

- `count += 1` — присваивание, поэтому `count` локальна для `inc`, а прочитать её до присваивания нельзя. Вывод: `UnboundLocalError`.

## Решение: nonlocal

```python
def outer():
    count = 0
    def inc():
        nonlocal count
        count += 1
    inc()
    inc()
    return count

print(outer())
```

- `nonlocal count` — «имя `count` означает переменную из **объемлющей** функции». Теперь присваивание меняет её.
- Вывод: `2`.

## С nonlocal и без

```python
def outer():
    x = 1
    def no():
        x = 2
    def yes():
        nonlocal x
        x = 3
    no()
    a = x
    yes()
    return a, x

print(outer())
```

- `no` создала свою локальную `x` и ничего не изменила снаружи; `yes` изменила `x` внешней функции.
- Вывод: `(1, 3)`.

## Когда nonlocal не нужен

```python
def outer():
    log = []
    total = 0
    def add(x):
        log.append(x)
    add(1)
    add(2)
    return log, total

print(outer())
```

- `log.append(x)` меняет **объект** — список, а имя `log` не переприсваивается. Поэтому `nonlocal` не нужен.
- Вывод: `([1, 2], 0)`.

`nonlocal` нужен только для **присваивания**: `=`, `+=`, `-=` и т. п.

## Несколько имён сразу

```python
def running_average():
    total = 0
    count = 0
    def add(x):
        nonlocal total, count
        total += x
        count += 1
        return total / count
    return add

avg = running_average()
print(avg(10), avg(20), avg(0))
```

- `nonlocal total, count` — два имени через запятую.
- Функция `add` возвращается наружу и продолжает помнить `total` и `count` — это **замыкание** (следующий урок).
- Вывод: `10.0 15.0 10.0`.

## Ограничения

- `nonlocal` ищет имя только в **объемлющих функциях**, не в глобальной области. Для глобальных — `global`.
- Имя должно уже существовать во внешней функции, иначе `SyntaxError: no binding for nonlocal 'x' found`.

## Итог

- Присваивание во вложенной функции создаёт локальную; изменить внешнюю переменную — `nonlocal имя`.
- Для изменения объекта (`append`, `d[k] = v`) `nonlocal` не нужен.
- `nonlocal a, b` — несколько имён.
- `nonlocal` — для объемлющих функций; `global` — для модуля.
'''),
    short=t(r'''
```py
def outer():
    count = 0
    def inc():
        nonlocal count   # менять переменную объемлющей функции
        count += 1
    log = []
    def add(x):
        log.append(x)    # метод — nonlocal не нужен
nonlocal total, count    # несколько имён
```
- `nonlocal` — объемлющая функция; `global` — модуль.
'''),
    quiz=[
        q('Когда нужен `nonlocal`?',
            ['Чтобы прочитать внешнюю переменную', 'Чтобы присвоить переменной объемлющей функции', 'Для глобальных переменных', 'Для append'],
            1, 'Только для присваивания.'),
        q('Что вернёт `outer()`?\n```py\ndef outer():\n    x = 1\n    def f():\n        x = 5\n    f()\n    return x\n```',
            ['`5`', '`1`', 'Ошибка', '`None`'],
            1, 'Без nonlocal f создаёт свою x.'),
        q('Можно ли через `nonlocal` изменить глобальную переменную модуля?',
            ['Да', 'Нет — для этого global', 'Только в классах', 'Только для списков'],
            1, 'nonlocal ищет только в объемлющих функциях.'),
    ],
),

# ---------- scp-m2-l3: Замыкания ----------
'scp-m2-l3': dict(
    full=t(r'''
## Зачем это нужно

**Замыкание** (closure) — функция, которая «запомнила» переменные той области, где была создана, и пользуется ими даже после того, как внешняя функция завершилась. С помощью замыканий делают **фабрики функций** (множитель, валидатор с настройками), счётчики, кэш, а также декораторы — важная тема для автотестов.

## Фабрика функций

```python
def multiplier(n):
    def mul(x):
        return x * n
    return mul

double, triple = multiplier(2), multiplier(3)
print(double(10), triple(10))
```

- `multiplier(2)` создаёт функцию `mul`, которая помнит `n = 2`, и **возвращает** её (без скобок — саму функцию).
- `multiplier` завершилась, её локальные должны были исчезнуть — но `n` продолжает жить, потому что на неё ссылается `mul`.
- Каждый вызов `multiplier` создаёт **своё** `n`. Вывод: `20 30`.

```viz
{"type": "trace", "auto": true, "title": "Замыкание помнит переменную между вызовами", "code": "def make_counter():\n    count = 0\n    def step():\n        nonlocal count\n        count += 1\n        return count\n    return step\n\nc = make_counter()\nprint(c())\nprint(c())", "notes": {"7": "`make_counter` закончилась, но `count` не исчез: его запомнила функция `step`.", "11": "Второй вызов продолжил с того же `count` — состояние живёт в замыкании."}}
```

## Где хранится запомненное

```python
def make_greeter(greeting):
    def greet(name):
        return f"{greeting}, {name}"
    return greet

hi = make_greeter("Hi")
print(hi("Ann"), hi.__name__)
print(hi.__closure__[0].cell_contents)
```

- `hi.__name__` — имя, данное в `def`: `greet`.
- `__closure__` — кортеж «ячеек» с запомненными переменными; `cell_contents` — значение в ячейке.
- Вывод: `Hi, Ann greet`, `Hi`.

## Замыкание с настройкой

```python
def make_validator(min_len):
    def check(s):
        return len(s) >= min_len
    return check

check8 = make_validator(8)
print(check8("12345678"), check8("123"))
```

- Одна фабрика — много проверок с разными порогами. Вывод: `True False`.

## Замыкание с состоянием (nonlocal)

```python
def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc

c = make_counter()
d = make_counter()
print(c(), c(), c(), d())
```

- `c` и `d` — разные замыкания со своими `count`. Вывод: `1 2 3 1`.

## Кэш в замыкании

```python
def make_cache(func):
    cache = {}
    def cached(x):
        if x not in cache:
            cache[x] = func(x)
        return cache[x]
    return cached

calls = []
def slow_square(x):
    calls.append(x)
    return x * x

fast = make_cache(slow_square)
print(fast(4), fast(4), fast(5), calls)
```

- Словарь `cache` живёт в замыкании; повторный вызов с тем же `x` берёт готовый ответ.
- Вывод: `16 16 25 [4, 5]` — медленная функция вызвана только дважды.

## Ловушка позднего связывания

```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)
print([f() for f in funcs])

fixed = []
for i in range(3):
    fixed.append(lambda i=i: i)
print([f() for f in fixed])
```

- Замыкание помнит **переменную**, а не её значение в момент создания. Все три лямбды ссылаются на одну `i`, которая к моменту вызова стала 2.
- Лечение: значение по умолчанию `i=i` — оно вычисляется в момент создания лямбды (тема «Функции», значения по умолчанию). Или фабрика `make(i)`, создающая отдельную область.
- Вывод: `[2, 2, 2]`, `[0, 1, 2]`.

## Итог

- Замыкание — вложенная функция, которая помнит переменные внешней после её завершения.
- Фабрика: внешняя функция принимает настройки и возвращает вложенную (без скобок).
- Каждый вызов фабрики создаёт своё независимое замыкание.
- Состояние в замыкании меняют через `nonlocal` или методы объекта.
- Замыкание помнит переменную, а не значение: в цикле фиксируй значение через `x=x` или фабрику.
'''),
    short=t(r'''
```py
def multiplier(n):
    def mul(x):
        return x * n       # n запомнена
    return mul             # без скобок!
double = multiplier(2)     # double(10) -> 20
f.__closure__[0].cell_contents   # запомненное значение
[lambda: i for i in range(3)]        # все вернут 2!
[lambda i=i: i for i in range(3)]    # 0, 1, 2
```
'''),
    quiz=[
        q('Что вернёт `multiplier(5)(3)`, если `multiplier(n)` возвращает `lambda x: x * n`?',
            ['`8`', '`15`', 'Функцию', 'Ошибка'],
            1, 'Первые скобки создают функцию, вторые вызывают.'),
        q('Что выведет `print([f() for f in [lambda: i for i in range(3)]])`?',
            ['`[0, 1, 2]`', '`[2, 2, 2]`', '`[0, 0, 0]`', 'Ошибка'],
            1, 'Все лямбды ссылаются на одну i.'),
        q('Что такое замыкание?',
            ['Закрытая функция', 'Функция, помнящая переменные области, где создана', 'Функция без return', 'Ошибка области'],
            1, 'Переменные живут, пока на них ссылается функция.'),
    ],
),

# ---------- scp-closure2: Замыкания на практике ----------
'scp-closure2': dict(
    full=t(r'''
## Зачем это нужно

Замыкания — лёгкий способ сделать «объект с состоянием» без классов: счётчик, стек, счёт, историю. Несколько функций могут делить одно состояние, фабрика может получать словарь настроек, а функции можно комбинировать. Разберём эти приёмы.

## Несколько функций — одно состояние

```python
def make_account(balance):
    def deposit(x):
        nonlocal balance
        balance += x
        return balance
    def get():
        return balance
    return deposit, get

dep, get = make_account(100)
dep(50)
print(get())
dep2, get2 = make_account(0)
print(get(), get2())
```

- `deposit` и `get` созданы в **одном** вызове `make_account` и видят одну и ту же `balance`.
- Фабрика возвращает кортеж функций, который распаковывается в `dep, get`.
- Второй вызов фабрики создаёт независимый «счёт». Вывод: `150`, `150 0`.

Так же устроены стек или пара «увеличить/сбросить»:

```python
def make_stack():
    items = []
    def push(x):
        items.append(x)
    def pop():
        return items.pop() if items else None
    def size():
        return len(items)
    return push, pop, size

push, pop, size = make_stack()
push(1)
push(2)
print(pop(), size(), pop(), pop())
```

- Список `items` скрыт — снаружи к нему нет доступа, кроме как через три функции. Это **инкапсуляция**: данные защищены от случайной порчи.
- Вывод: `2 1 1 None`.

## Изменение объекта в замыкании

```python
def outer():
    items = []
    def add(x):
        items.append(x)
        return len(items)
    return add

add = outer()
print(add("a"), add("b"), add("c"))
```

- `nonlocal` не нужен: меняется список, а не имя. Вывод: `1 2 3`.

## Фабрика с настройками

```python
def make_converter(rates):
    def convert(amount, currency):
        if currency not in rates:
            return None
        return amount * rates[currency]
    return convert

conv = make_converter({"USD": 90, "EUR": 100})
print(conv(2, "USD"), conv(1, "JPY"))
```

- Замыкание запомнило словарь курсов. Вывод: `180 None`.

## Композиция функций

```python
def compose(f, g):
    def composed(x):
        return f(g(x))
    return composed

inc = lambda x: x + 1
double = lambda x: x * 2
print(compose(inc, double)(5), compose(double, inc)(5))
```

- `compose` запоминает две функции и возвращает новую — их последовательное применение.
- Вывод: `11 12` (5·2+1 и (5+1)·2).

## Фабрика против лямбды в цикле

```python
def make(n):
    return lambda x: x + n

fs = [make(i) for i in range(3)]
print([f(10) for f in fs])
gs = [lambda x: x + i for i in range(3)]
print([g(10) for g in gs])
```

- Каждый вызов `make(i)` создаёт **новую область** со своим `n`, поэтому значения фиксируются.
- Лямбды во включении делят одну переменную `i`. Вывод: `[10, 11, 12]`, `[12, 12, 12]`.

## Возвращай копию

```python
def make_history(limit):
    items = []
    def add(item):
        items.append(item)
        if len(items) > limit:
            items.pop(0)
        return list(items)
    return add

add = make_history(2)
print(add("a"), add("b"), add("c"))
```

- Если вернуть сам `items`, внешний код сможет изменить скрытое состояние. `list(items)` — **копия**.
- Вывод: `['a'] ['a', 'b'] ['b', 'c']`.

## Итог

- Фабрика может вернуть несколько функций с общим состоянием — простая замена класса.
- Скрытое состояние в замыкании недоступно снаружи — возвращай копии, чтобы его не испортили.
- Фабрики удобны для настроек (курсы, адреса, лимиты) и комбинирования функций (`compose`).
- Вызов фабрики в цикле фиксирует значения лучше, чем лямбда в цикле.
'''),
    short=t(r'''
```py
def make_account(balance):
    def deposit(x):
        nonlocal balance
        balance += x
    def get():
        return balance
    return deposit, get         # общее состояние
dep, get = make_account(100)
def compose(f, g):
    return lambda x: f(g(x))    # f(g(x))
return list(items)              # копия, чтобы не испортили
```
'''),
    quiz=[
        q('Видят ли `deposit` и `get` из одного вызова `make_account` одну и ту же `balance`?',
            ['Да', 'Нет', 'Только get', 'Только после nonlocal в get'],
            0, 'Они созданы в одной области.'),
        q('Что вернёт `compose(lambda x: x + 1, lambda x: x * 10)(2)`?',
            ['`30`', '`21`', '`12`', '`3`'],
            1, 'Сначала g: 20, затем f: 21.'),
        q('Зачем возвращать `list(items)`, а не `items`?',
            ['Быстрее', 'Чтобы внешний код не изменил скрытое состояние', 'Иначе ошибка', 'Без разницы'],
            1, 'Копия защищает данные замыкания.'),
    ],
),
}
