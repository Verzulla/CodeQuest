"""Теория модуля «Функции-обёртки» темы «Декораторы».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- dec-funcobj ----------
'dec-funcobj': dict(
    full=t(r'''
## Зачем это нужно

Декоратор — это функция, которая принимает функцию и возвращает новую функцию. Чтобы это понять, сначала нужно привыкнуть к мысли: **функция в Python — такой же объект, как число или строка**. Её можно положить в переменную, передать в другую функцию, вернуть из функции, сохранить в список или словарь.

## Имя функции — просто переменная

```python
def hello():
    return "привет"

greet = hello
print(greet())
print(greet is hello, hello.__name__, greet.__name__)
print(type(hello).__name__)
```

- `def hello():` создаёт объект-функцию и кладёт его в переменную `hello`.
- `greet = hello` — **без скобок**: не вызываем функцию, а берём сам объект. Теперь на него ссылаются два имени.
- `greet()` — со скобками: вызов.
- `__name__` — имя, данное функции в `def`. У `greet` оно тоже `hello`: объект тот же.
- `type(hello).__name__` — класс функций называется `function`.
- Вывод: `привет`, `True hello hello`, `function`.

## Функция как аргумент

```python
def apply(func, value):
    return func(value)

def double(x):
    return x * 2

print(apply(double, 5))
print(apply(str.upper, "abc"))
print(apply(len, [1, 2, 3]))
```

- Параметр `func` получает функцию, а `func(value)` её вызывает.
- Передавать можно любые функции: свои, встроенные (`len`), методы (`str.upper`), `lambda`.
- Ты уже так делал: `sorted(..., key=len)`, `map(str, ...)`, `filter(...)`.
- Вывод: `10`, `ABC`, `3`.

## Функции в словаре

```python
def add(a, b):
    return a + b

def sub(a, b):
    return a - b

ops = {"+": add, "-": sub, "*": lambda a, b: a * b}
for sign in ["+", "-", "*"]:
    print(sign, ops[sign](6, 3))
```

- В словаре лежат функции. `ops[sign]` достаёт функцию, `(6, 3)` — вызывает её.
- Это замена длинной цепочки `if/elif`: добавить операцию — добавить одну пару в словарь.
- Вывод: `+ 9`, `- 3`, `* 18`.

## Список функций-проверок

```python
def is_positive(x):
    return x > 0

def is_even(x):
    return x % 2 == 0

checks = [is_positive, is_even]
value = -3
failed = [c.__name__ for c in checks if not c(value)]
print(failed)
```

- Перебираем функции как обычные элементы списка и вызываем каждую.
- `c.__name__` — удобно для отчёта, какая проверка не прошла.
- Вывод: `['is_positive', 'is_even']`.

## Последовательность преобразований

```python
def pipeline(value, *funcs):
    for func in funcs:
        value = func(value)
    return value

print(pipeline("  Hi ", str.strip, str.lower))
```

- `*funcs` собирает любое количество функций в кортеж.
- Результат каждой функции становится входом следующей.
- Вывод: `hi`.

## Итог

- Функция — объект: `f` — сама функция, `f()` — её вызов.
- Функции можно передавать, хранить в списках и словарях.
- `f.__name__` — имя функции.
- Декораторы построены именно на этом.
'''),
    short=t(r'''
```py
greet = hello          # без скобок — объект функции
greet()                # вызов
hello.__name__         # 'hello'

def apply(func, x):    # функция как аргумент
    return func(x)
apply(len, "abc")      # 3

ops = {"+": add, "-": sub}
ops["+"](2, 3)         # 5
```
'''),
    quiz=[
        q('Чем отличаются `f` и `f()`?',
            ['Ничем', '`f` — сама функция, `f()` — результат вызова', '`f()` — функция, `f` — результат', '`f` — ошибка'],
            1, 'Скобки означают вызов.'),
        q('Что выведет `print(len.__name__)`?',
            ['len', 'function', 'builtin', '3'],
            0, '`__name__` — имя функции.'),
        q('Можно ли хранить функции в словаре?',
            ['Нет', 'Да, как любые объекты', 'Только lambda', 'Только встроенные'],
            1, 'Функции — обычные объекты.'),
    ],
),

# ---------- dec-factory ----------
'dec-factory': dict(
    full=t(r'''
## Зачем это нужно

Функция может не только принимать другую функцию, но и **создавать и возвращать** новую. Внутренняя функция при этом помнит переменные внешней — это **замыкание**. Декоратор — это ровно такая функция: принимает функцию и возвращает новую, которая помнит исходную.

## Функция возвращает функцию

```python
def make_multiplier(k):
    def multiply(x):
        return x * k
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5), triple(5))
print(double.__name__)
```

- Внутри `make_multiplier` объявлена функция `multiply`. `return multiply` — возвращаем её **без вызова**.
- `double = make_multiplier(2)` — получаем функцию, у которой `k = 2`.
- `multiply` использует `k` из внешней функции. Внешняя уже завершилась, но `k` не исчез: вложенная функция его «запомнила». Это и есть **замыкание** (closure).
- У каждого вызова `make_multiplier` своё `k`: `double` помнит 2, `triple` — 3.
- Вывод: `10 15`, `multiply`.

## Замыкание с состоянием

```python
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

a = make_counter()
b = make_counter()
print(a(), a(), a(), b())
```

- `nonlocal count` — «`count` — это переменная внешней функции, я хочу её менять». Без `nonlocal` строка `count += 1` дала бы `UnboundLocalError`.
- Читать внешнюю переменную можно без `nonlocal`, а вот присваивать — только с ним.
- `a` и `b` — разные счётчики со своими `count`.
- Вывод: `1 2 3 1`.

## Функция принимает функцию и возвращает функцию

```python
def loud(func):
    def inner(text):
        return func(text).upper() + "!"
    return inner

def greet(name):
    return f"привет, {name}"

loud_greet = loud(greet)
print(greet("аня"))
print(loud_greet("аня"))
```

- `loud` получает функцию `func` и создаёт `inner`, которая вызывает `func` и изменяет результат.
- `loud_greet` — **новая** функция; исходная `greet` не изменилась.
- Это уже декоратор, только применённый вручную.
- Вывод: `привет, аня`, `ПРИВЕТ, АНЯ!`.

## Полезные примеры

```python
def negate(func):
    def inner(x):
        return not func(x)
    return inner

def compose(f, g):
    def h(x):
        return f(g(x))
    return h

is_odd = negate(lambda x: x % 2 == 0)
inc_then_double = compose(lambda x: x * 2, lambda x: x + 1)
print(is_odd(3), inc_then_double(5))
```

- `negate` переворачивает результат любой функции-проверки.
- `compose(f, g)` — сначала `g`, потом `f`: `(5 + 1) * 2`.
- Вывод: `True 12`.

## Итог

- Вложенная функция может быть возвращена наружу — без скобок.
- Она помнит переменные внешней функции (замыкание).
- Изменять их — через `nonlocal`.
- Функция, принимающая функцию и возвращающая новую, — это декоратор.
'''),
    short=t(r'''
```py
def make_adder(n):
    def add(x):
        return x + n      # помнит n (замыкание)
    return add            # без скобок!

add5 = make_adder(5)
add5(10)                  # 15

def make_counter():
    count = 0
    def counter():
        nonlocal count    # чтобы менять
        count += 1
        return count
    return counter
```
'''),
    quiz=[
        q('Что такое замыкание?',
            ['Закрытый класс', 'Вложенная функция, помнящая переменные внешней', 'Функция без return', 'Ошибка области видимости'],
            1, 'Значения внешней функции остаются доступны после её завершения.'),
        q('Зачем `nonlocal`?',
            ['Чтобы читать внешнюю переменную', 'Чтобы присваивать переменной внешней функции', 'Чтобы создать глобальную', 'Чтобы удалить переменную'],
            1, 'Без него присваивание создаёт локальную переменную.'),
        q('Что вернёт `make_multiplier(2)`?',
            ['Число 2', 'Функцию', 'None', 'Ошибку'],
            1, 'Возвращается вложенная функция multiply.'),
    ],
),

# ---------- dec-first ----------
'dec-first': dict(
    full=t(r'''
## Зачем это нужно

Иногда к функции нужно добавить поведение, не меняя её код: записать в лог каждый вызов, замерить время, поймать ошибку, проверить права. Если делать это в каждой функции вручную — будет много одинакового кода. **Декоратор** оборачивает функцию: добавляет действия до и после вызова, а сама функция остаётся нетронутой.

## Первый декоратор

```python
def announce(func):
    def wrapper():
        print("до вызова")
        func()
        print("после вызова")
    return wrapper

def work():
    print("работаю")

work = announce(work)
work()
```

Что делает каждая строка:

- `def announce(func):` — декоратор принимает функцию, которую будем оборачивать.
- `def wrapper():` — **обёртка**: новая функция, которая будет вызываться вместо исходной. Имя `wrapper` — традиция.
- Внутри обёртки: действие до, вызов исходной `func()`, действие после.
- `return wrapper` — возвращаем обёртку (без скобок).
- `work = announce(work)` — **подменяем** функцию: имя `work` теперь указывает на `wrapper`. Исходная функция живёт внутри обёртки как `func` (замыкание).
- `work()` — на самом деле вызывает `wrapper()`.
- Вывод: `до вызова`, `работаю`, `после вызова`.

## Не потеряй результат

```python
def announce(func):
    def wrapper():
        print("вызов")
        func()
    return wrapper

def get_answer():
    return 42

get_answer = announce(get_answer)
print(get_answer())
```

- `wrapper` вызывает `func()`, но **не возвращает** её результат. Функция без `return` возвращает `None`.
- Вывод: `вызов`, `None` — результат потерян!

Правильно:

```python
def announce(func):
    def wrapper():
        print("вызов")
        return func()
    return wrapper

def get_answer():
    return 42

get_answer = announce(get_answer)
print(get_answer())
```

- `return func()` — вызываем и возвращаем результат.
- Если нужно что-то сделать после вызова — сохрани результат в переменную: `result = func()`, действия, `return result`.
- Вывод: `вызов`, `42`.

## Обёртка может менять результат

```python
def shout(func):
    def wrapper():
        return func().upper() + "!"
    return wrapper

def hello():
    return "привет"

print(shout(hello)())
```

- `shout(hello)` — обёртка, `()` — сразу её вызов.
- Вывод: `ПРИВЕТ!`.

## Обёртка может ловить ошибки

```python
def safe(func):
    def wrapper():
        try:
            return func()
        except Exception:
            return None
    return wrapper

def broken():
    return 1 / 0

print(safe(broken)())
```

- Ошибка исходной функции не выходит наружу — обёртка возвращает `None`.
- Вывод: `None`.

## Обёртка может хранить состояние

```python
def count_calls(func):
    def wrapper():
        wrapper.calls += 1
        return func()
    wrapper.calls = 0
    return wrapper

def ping():
    return "pong"

ping = count_calls(ping)
ping()
ping()
print(ping.calls)
```

- Функции — объекты, им можно добавлять атрибуты: `wrapper.calls = 0`.
- Внутри обёртки обращаемся к ней по имени `wrapper` и увеличиваем счётчик.
- Вывод: `2`.

## Итог

- Декоратор: `def deco(func): def wrapper(): ... return wrapper`.
- Применение вручную: `f = deco(f)`.
- В обёртке **обязательно** `return func()`, иначе результат потеряется.
- Обёртка может делать что-то до/после, менять результат, ловить ошибки, хранить атрибуты.
'''),
    short=t(r'''
```py
def deco(func):
    def wrapper():
        print("до")           # действие до
        result = func()       # вызов исходной
        print("после")        # действие после
        return result         # не забыть!
    return wrapper            # без скобок

work = deco(work)             # подмена функции
work()                        # вызывает wrapper
```
'''),
    quiz=[
        q('Что вернёт задекорированная функция, если в `wrapper` написано `func()` без `return`?',
            ['Результат func', 'None', 'wrapper', 'Ошибку'],
            1, 'Функция без return возвращает None.'),
        q('Что делает строка `work = announce(work)`?',
            ['Вызывает work', 'Подменяет work обёрткой', 'Удаляет work', 'Копирует work'],
            1, 'Имя work теперь указывает на wrapper.'),
        q('Где хранится исходная функция после декорирования?',
            ['Нигде, удалена', 'Внутри обёртки как func (замыкание)', 'В глобальной переменной', 'В модуле functools'],
            1, 'Обёртка помнит func.'),
    ],
),

# ---------- dec-syntax ----------
'dec-syntax': dict(
    full=t(r'''
## Зачем это нужно

Писать `work = announce(work)` после каждой функции неудобно, и легко забыть. Python даёт короткую запись — **`@`** над функцией. А чтобы один декоратор подходил к любым функциям, обёртка должна принимать любые аргументы.

## Синтаксис @

```python
def exclaim(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) + "!"
    return wrapper

@exclaim
def greet(name, greeting="Привет"):
    return f"{greeting}, {name}"

print(greet("Аня"))
print(greet("Боря", greeting="Здравствуй"))
```

- `@exclaim` над `def greet` — **ровно то же**, что `greet = exclaim(greet)` сразу после объявления.
- `def wrapper(*args, **kwargs):` — обёртка принимает **любые** аргументы: позиционные собираются в кортеж `args`, именованные — в словарь `kwargs`.
- `func(*args, **kwargs)` — передаём их исходной функции в том же виде (распаковка).
- Благодаря этому декоратор подходит к функции с любой сигнатурой.
- Вывод: `Привет, Аня!`, `Здравствуй, Боря!`.

## Когда выполняется декоратор

```python
def register(func):
    print("декорирую", func.__name__)
    return func

@register
def a():
    print("a")

@register
def b():
    print("b")

print("старт")
a()
```

- Декоратор выполняется **один раз** — в момент объявления функции (при загрузке модуля), а не при каждом вызове.
- При каждом вызове выполняется **обёртка** (если декоратор её вернул). Здесь `register` возвращает саму функцию, без обёртки.
- Вывод: `декорирую a`, `декорирую b`, `старт`, `a`.

## Что видит обёртка

```python
def show_args(func):
    def wrapper(*args, **kwargs):
        print("args:", args, "kwargs:", kwargs)
        return func(*args, **kwargs)
    return wrapper

@show_args
def area(w, h=1):
    return w * h

print(area(3, h=4))
print(area(5))
```

- `args` — кортеж позиционных аргументов, `kwargs` — словарь именованных.
- Значения по умолчанию (`h=1`) в `kwargs` не попадают: их подставляет уже сама `area`.
- Вывод: `args: (3,) kwargs: {'h': 4}`, `12`, `args: (5,) kwargs: {}`, `5`.

## Проверка аргументов

```python
def positive_args(func):
    def wrapper(*args, **kwargs):
        for a in args:
            if a <= 0:
                raise ValueError("аргументы должны быть > 0")
        return func(*args, **kwargs)
    return wrapper

@positive_args
def area(w, h):
    return w * h

print(area(2, 3))
try:
    area(2, -1)
except ValueError as e:
    print(e)
```

- Обёртка проверяет аргументы **до** вызова. Если что-то не так — функция не вызывается вовсе.
- Вывод: `6`, `аргументы должны быть > 0`.

## Изменение аргументов

```python
def strip_strings(func):
    def wrapper(*args, **kwargs):
        args = [a.strip() if isinstance(a, str) else a for a in args]
        return func(*args, **kwargs)
    return wrapper

@strip_strings
def join(a, b):
    return a + "|" + b

print(join("  x ", " y"))
```

- Обёртка может «почистить» аргументы, прежде чем передать их функции. `*args` распаковывает и список.
- Вывод: `x|y`.

## Итог

- `@deco` над `def f` = `f = deco(f)`.
- Обёртка `wrapper(*args, **kwargs)` + вызов `func(*args, **kwargs)` — подходит к любым функциям.
- Декоратор выполняется один раз при объявлении, обёртка — при каждом вызове.
- Обёртка может проверять и менять аргументы до вызова.
'''),
    short=t(r'''
```py
def deco(func):
    def wrapper(*args, **kwargs):    # любые аргументы
        # проверить/изменить args
        result = func(*args, **kwargs)
        # изменить result
        return result
    return wrapper

@deco                 # = f = deco(f)
def f(a, b=1): ...
```
'''),
    quiz=[
        q('Чему эквивалентна запись `@deco` над `def f`?',
            ['`f = deco()`', '`f = deco(f)`', '`deco = f(deco)`', '`f(deco)`'],
            1, 'Декоратор получает функцию и заменяет её результатом.'),
        q('Когда выполняется сам декоратор (не обёртка)?',
            ['При каждом вызове', 'Один раз при объявлении функции', 'Никогда', 'При выходе из программы'],
            1, 'Обёртка — при вызовах, декоратор — при объявлении.'),
        q('Зачем обёртке `*args, **kwargs`?',
            ['Для скорости', 'Чтобы подходить к функциям с любыми аргументами', 'Так требует синтаксис @', 'Чтобы запретить аргументы'],
            1, 'Все аргументы передаются исходной функции как есть.'),
    ],
),

}
