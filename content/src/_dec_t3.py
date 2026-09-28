"""Теория модуля «Продвинутые декораторы» темы «Декораторы».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- dec-params ----------
'dec-params': dict(
    full=t(r'''
## Зачем это нужно

`retry3` всегда делает 3 попытки. А если в одном месте нужно 5, а в другом — 2? Хочется писать `@retry(times=5)`. Для этого нужен **декоратор с параметрами** — функция, которая по параметрам **создаёт** декоратор. Ты уже видел такие: `@wraps(func)`, `@lru_cache(maxsize=2)`.

## Три уровня вложенности

```python
from functools import wraps

def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(times)]
        return wrapper
    return decorator

@repeat(3)
def hello(name):
    return f"hi {name}"

print(hello("аня"))
print(hello.__name__)
```

Что делает каждый уровень:

- `repeat(times)` — **фабрика декораторов**: принимает параметры и возвращает декоратор.
- `decorator(func)` — обычный декоратор, как раньше: принимает функцию, возвращает обёртку.
- `wrapper(*args, **kwargs)` — обёртка, выполняется при каждом вызове. Она видит и `func`, и `times` (замыкание на два уровня).
- `@repeat(3)` — сначала вызывается `repeat(3)`, получается декоратор, и уже он применяется к `hello`.
- Вывод: `['hi аня', 'hi аня', 'hi аня']`, `hello`.

## Как это выглядит без @

```python
from functools import wraps

def multiply(k):
    def decorator(func):
        @wraps(func)
        def wrapper(x):
            return func(x) * k
        return wrapper
    return decorator

def inc(x):
    return x + 1

decorator = multiply(10)
f = decorator(inc)
g = multiply(2)(inc)
print(f(1), g(1), inc(1))
```

- `@multiply(10)` над `inc` = `inc = multiply(10)(inc)`: две пары скобок — два вызова.
- Вывод: `20 4 2`.

## Частая ошибка: забыть скобки

- `@repeat` (без скобок) передаст функцию в параметр `times`. Декоратор вернёт `decorator`, и при вызове функции получится путаница или `TypeError`.
- `@retry3` без параметров и `@retry(3)` с параметрами — разные декораторы с разной вложенностью.

## Настраиваемый retry

```python
from functools import wraps

def retry(times, exceptions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times - 1:
                        raise
        return wrapper
    return decorator

state = {"n": 0}

@retry(times=4, exceptions=(ConnectionError, TimeoutError))
def flaky():
    state["n"] += 1
    if state["n"] < 3:
        raise TimeoutError
    return "ok"

print(flaky(), state["n"])
```

- `except exceptions:` — в `except` можно передать переменную с кортежем типов ошибок.
- Вывод: `ok 3`.

## Состояние на каждую функцию

```python
from functools import wraps

def limit_calls(n):
    def decorator(func):
        count = 0
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal count
            if count >= n:
                raise RuntimeError(f"{func.__name__}: лимит {n} вызовов")
            count += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

@limit_calls(1)
def init():
    return "ok"

print(init())
try:
    init()
except RuntimeError as e:
    print(e)
```

- `count = 0` стоит внутри `decorator`, а `decorator` выполняется один раз для каждой задекорированной функции — значит, у каждой функции свой счётчик. Глобальная переменная была бы общей для всех.
- Вывод: `ok`, `init: лимит 1 вызовов`.

## Итог

- Декоратор с параметрами: `фабрика(параметры) → decorator(func) → wrapper(*args)`.
- `@deco(x)` = `f = deco(x)(f)`.
- Параметры доступны в обёртке через замыкание.
- Состояние для каждой функции — в `decorator`.
'''),
    short=t(r'''
```py
from functools import wraps

def retry(times=3):                  # параметры
    def decorator(func):             # функция
        @wraps(func)
        def wrapper(*args, **kwargs):  # вызов
            for i in range(times):
                ...
            return func(*args, **kwargs)
        return wrapper
    return decorator

@retry(times=5)       # = f = retry(times=5)(f)
def f(): ...
```
'''),
    quiz=[
        q('Сколько уровней вложенных функций у декоратора с параметрами?',
            ['1', '2', '3', '4'],
            2, 'Фабрика → декоратор → обёртка.'),
        q('Чему равно `@repeat(3)` над `def f`?',
            ['`f = repeat(f, 3)`', '`f = repeat(3)(f)`', '`f = repeat(3)`', '`f = f(repeat(3))`'],
            1, 'Сначала repeat(3) даёт декоратор, потом он применяется к f.'),
        q('Где хранить счётчик, чтобы он был свой для каждой задекорированной функции?',
            ['В глобальной переменной', 'Внутри decorator (среднего уровня)', 'Внутри wrapper как локальную', 'В параметре times'],
            1, 'decorator выполняется один раз на каждую функцию.'),
    ],
),

# ---------- dec-stack ----------
'dec-stack': dict(
    full=t(r'''
## Зачем это нужно

К одной функции часто применяют несколько декораторов: проверка авторизации, логирование, повтор, кэш. Важно понимать, в каком порядке они применяются и выполняются, — от этого зависит результат.

## Порядок применения

```python
def bold(func):
    def wrapper():
        return "<b>" + func() + "</b>"
    return wrapper

def italic(func):
    def wrapper():
        return "<i>" + func() + "</i>"
    return wrapper

@bold
@italic
def text():
    return "привет"

print(text())
```

- Декораторы применяются **снизу вверх**: ближайший к `def` — первым.
- Запись равна `text = bold(italic(text))`.
- `italic` оборачивает исходную функцию, `bold` — результат `italic`.
- Вывод: `<b><i>привет</i></b>`.

## Порядок выполнения: матрёшка

```python
def trace(name):
    def decorator(func):
        def wrapper():
            print("вход", name)
            result = func()
            print("выход", name)
            return result
        return wrapper
    return decorator

@trace("A")
@trace("B")
def work():
    print("работа")
    return 1

print(work())
```

- При вызове выполнение идёт **сверху вниз** внутрь: сначала внешняя обёртка A, она вызывает B, B вызывает функцию.
- Возврат — в обратном порядке: B выходит первой, A — последней.
- Вывод: `вход A`, `вход B`, `работа`, `выход B`, `выход A`, `1`.

## Порядок меняет результат

```python
def add_one(func):
    def wrapper():
        return func() + 1
    return wrapper

def double(func):
    def wrapper():
        return func() * 2
    return wrapper

@add_one
@double
def five():
    return 5

@double
@add_one
def five2():
    return 5

print(five(), five2())
```

- `five`: сначала `double` (5 × 2 = 10), потом `add_one` (11).
- `five2`: сначала `add_one` (6), потом `double` (12).
- Вывод: `11 12`.

## Практический порядок

```python
from functools import wraps

CALLS = []

def require_auth(func):
    @wraps(func)
    def wrapper(user, *args):
        if user is None:
            raise PermissionError("нужен вход")
        return func(user, *args)
    return wrapper

def log_calls(func):
    @wraps(func)
    def wrapper(*args):
        CALLS.append(func.__name__)
        return func(*args)
    return wrapper

@require_auth
@log_calls
def delete_item(user, item_id):
    return f"{user} удалил {item_id}"

print(delete_item("аня", 5))
try:
    delete_item(None, 5)
except PermissionError as e:
    print(e, CALLS)
```

- `require_auth` — внешний: проверка срабатывает **первой**. Неавторизованный вызов отсекается, до лога дело не доходит.
- Поменяй порядок — и в лог попадут и отклонённые вызовы. Иногда это нужно (аудит попыток), иногда нет.
- Вывод: `аня удалил 5`, `нужен вход ['delete_item']`.

## Правила расстановки

- Проверки доступа и валидация — **снаружи** (выше), чтобы отсекать плохие вызовы раньше.
- `@lru_cache` — обычно ближе к функции (ниже), чтобы кэшировать чистый результат.
- `@retry` — снаружи того, что может временно падать.
- `@property`, `@classmethod`, `@staticmethod` — всегда **самые верхние** над методом.

## Итог

- Применение: снизу вверх (`@a @b def f` = `a(b(f))`).
- Выполнение: сверху вниз внутрь, выход — обратно.
- От порядка зависит результат и то, какие действия выполнятся.
'''),
    short=t(r'''
```py
@a          # применяется вторым, выполняется первым
@b          # применяется первым
def f(): ...
# f = a(b(f))

# вызов:  a-до → b-до → f → b-после → a-после

@require_auth     # проверки — снаружи
@log_calls
@lru_cache        # кэш — у функции
def handler(): ...
```
'''),
    quiz=[
        q('Чему равна запись `@a` `@b` `def f`?',
            ['`f = b(a(f))`', '`f = a(b(f))`', '`f = a(f); f = b(f)` без вложенности', 'Ошибка'],
            1, 'Ближний к def применяется первым.'),
        q('Чья часть «до вызова» выполнится первой при `@a @b def f`?',
            ['a', 'b', 'f', 'Одновременно'],
            0, 'Внешняя обёртка вызывается первой.'),
        q('Где лучше ставить декоратор проверки прав?',
            ['Ближе всех к def', 'Снаружи (выше других)', 'Не важно', 'Только отдельно от других'],
            1, 'Плохой вызов отсекается раньше остальной логики.'),
    ],
),

# ---------- dec-methods ----------
'dec-methods': dict(
    full=t(r'''
## Зачем это нужно

Декораторы работают не только с обычными функциями. Их применяют к **методам** классов (например, логировать действия Page Object), сами декораторы можно писать **классами**, а ещё можно декорировать **классы целиком** — так устроены `@dataclass` и `@total_ordering`.

## Декоратор на методе

```python
from functools import wraps

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("вызов", func.__name__, "аргументов:", len(args))
        return func(*args, **kwargs)
    return wrapper

class Cart:
    def __init__(self):
        self.items = []

    @log
    def add(self, item):
        self.items.append(item)

c = Cart()
c.add("чай")
print(c.items)
```

- Метод — это функция, у которой первый аргумент `self`. Поэтому обычный декоратор с `*args` работает и для методов.
- `self` попадает в `args` первым: `args == (c, "чай")`.
- Вывод: `вызов add аргументов: 2`, `['чай']`.

## Обёртка, которая пользуется self

```python
from functools import wraps

def log_method(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.history.append(func.__name__)
        return func(self, *args, **kwargs)
    return wrapper

class Door:
    def __init__(self):
        self.history = []

    @log_method
    def open(self):
        pass

    @log_method
    def close(self):
        pass

d = Door()
d.open()
d.close()
print(d.history)
```

- Если явно выделить `self` в сигнатуре обёртки, можно работать с атрибутами объекта.
- Вывод: `['open', 'close']`.

## Класс как декоратор

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)

@CountCalls
def hello(name):
    return f"hi {name}"

print(hello("аня"), hello("боря"))
print(hello.calls, type(hello).__name__)
```

- `@CountCalls` = `hello = CountCalls(hello)`: создаётся **объект**, а исходная функция сохраняется в `self.func`.
- Вызов `hello(...)` — это вызов объекта, то есть метод `__call__`.
- Состояние хранится в атрибутах объекта — удобнее, чем атрибуты функции или `nonlocal`.
- Минус: такой декоратор не подходит для методов без дополнительных хитростей — `self` метода не передаётся.
- Вывод: `hi аня hi боря`, `2 CountCalls`.

## Декоратор класса

```python
def add_repr(cls):
    def __repr__(self):
        fields = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{cls.__name__}({fields})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

print(User("Аня", 30))
```

- Декоратор получает **класс**, добавляет ему метод и возвращает тот же класс.
- `cls.__repr__ = __repr__` — методы можно добавлять классу и после объявления.
- Именно так работает `@dataclass`: он читает поля класса и дописывает `__init__`, `__repr__`, `__eq__`.
- Вывод: `User(name='Аня', age=30)`.

## Встроенные декораторы методов

Ты уже знаешь их из темы «Классы»:

- `@property` — метод читается как атрибут;
- `@classmethod` — первым получает класс (`cls`);
- `@staticmethod` — не получает ни `self`, ни `cls`;
- `@abstractmethod` — метод обязан быть реализован в потомке.

Все они — обычные декораторы: получают функцию и возвращают специальный объект.

## Итог

- Обычный декоратор с `*args` подходит и для методов: `self` — первый в `args`.
- Класс-декоратор: `__init__(self, func)` + `__call__`.
- Декоратор класса получает и возвращает класс, может добавлять методы.
- `@property`, `@classmethod`, `@dataclass` — тоже декораторы.
'''),
    short=t(r'''
```py
def log_method(func):           # для методов
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.history.append(func.__name__)
        return func(self, *args, **kwargs)
    return wrapper

class CountCalls:               # класс-декоратор
    def __init__(self, func): self.func, self.calls = func, 0
    def __call__(self, *a, **kw):
        self.calls += 1
        return self.func(*a, **kw)

def add_repr(cls):              # декоратор класса
    cls.__repr__ = lambda self: f"{cls.__name__}{vars(self)}"
    return cls
```
'''),
    quiz=[
        q('Каким элементом `args` окажется `self` при декорировании метода?',
            ['Последним', 'Первым', 'Не попадёт', 'В kwargs'],
            1, 'Метод вызывается как функция с self первым аргументом.'),
        q('Какой метод вызывается при вызове объекта-декоратора `hello("аня")`?',
            ['`__init__`', '`__call__`', '`__new__`', '`__wrapped__`'],
            1, 'Вызов объекта — это `__call__`.'),
        q('Что получает декоратор класса?',
            ['Объект класса', 'Сам класс', 'Метод __init__', 'Строку с именем'],
            1, 'И обычно возвращает тот же класс.'),
    ],
),

# ---------- dec-practice ----------
'dec-practice': dict(
    full=t(r'''
## Зачем это нужно

В автотестах декораторы на каждом шагу: `@pytest.fixture`, `@pytest.mark.smoke`, `@pytest.mark.parametrize`, `@pytest.mark.skipif`, `@allure.step`. Во фреймворках для API — `@app.get("/users")`. Разберём, как устроены такие декораторы, написав их упрощённые версии.

## Регистрация: собрать функции в список

```python
TESTS = []

def test(func):
    TESTS.append(func)
    return func

@test
def check_login():
    assert True

@test
def check_cart():
    assert 1 + 1 == 3

def helper():
    pass

for t in TESTS:
    try:
        t()
        print("PASS", t.__name__)
    except AssertionError:
        print("FAIL", t.__name__)
```

- Декоратор не оборачивает функцию, а **регистрирует**: добавляет в список и возвращает её же.
- `helper` без декоратора в список не попал — раннер его не запустит.
- Вывод: `PASS check_login`, `FAIL check_cart`.
- Так же работают маршруты веб-фреймворков: `@app.get("/users")` кладёт функцию в словарь «путь → обработчик».

## Метки

```python
def mark(*tags):
    def decorator(func):
        func.tags = set(tags)
        return func
    return decorator

@mark("smoke", "api")
def test_status(): pass

@mark("regression")
def test_history(): pass

tests = [test_status, test_history]
print([t.__name__ for t in tests if "smoke" in t.tags])
```

- Метка — атрибут функции. Раннер читает его и решает, запускать ли тест.
- Это упрощённый `@pytest.mark.smoke`: `pytest -m smoke` запускает только помеченные.
- Вывод: `['test_status']`.

## Пропуск по условию

```python
from functools import wraps

def skip_if(condition, reason):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if condition:
                return f"SKIP: {reason}"
            return func(*args, **kwargs)
        return wrapper
    return decorator

import sys

@skip_if(sys.platform == "no-such-os", "не та ОС")
def test_paths():
    return "ran"

@skip_if(True, "баг #123")
def test_known_bug():
    return "ran"

print(test_paths(), test_known_bug())
```

- `condition` вычисляется **один раз** при декорировании.
- Аналог: `@pytest.mark.skipif(sys.platform == "win32", reason="...")`.
- Вывод: `ran SKIP: баг #123`.

## Параметризация

```python
def parametrize(cases):
    def decorator(func):
        def run_all():
            return [func(*case) for case in cases]
        return run_all
    return decorator

@parametrize([(2, 3, 5), (0, 0, 0), (-1, 1, 1)])
def check_add(a, b, expected):
    return "ok" if a + b == expected else f"FAIL {a}+{b}"

print(check_add())
```

- Один тест — много наборов данных. `func(*case)` распаковывает кортеж в аргументы.
- В pytest: `@pytest.mark.parametrize("a, b, expected", [(2, 3, 5), ...])`, и каждый набор становится отдельным тестом в отчёте.
- Вывод: `['ok', 'ok', 'FAIL -1+1']`.

## Фикстура

```python
from functools import wraps

def fixture(func):
    cache = []
    @wraps(func)
    def wrapper():
        if not cache:
            cache.append(func())
        return cache[0]
    return wrapper

@fixture
def db():
    print("подключение к БД")
    return {"users": []}

db()["users"].append("аня")
print(db())
```

- Фикстура готовит данные для тестов. Здесь она создаётся один раз и переиспользуется, как `@pytest.fixture(scope="session")`.
- `cache` — список: пустой — значит, ещё не создавали.
- Вывод: `подключение к БД`, `{'users': ['аня']}`.

## Итог

- Регистрирующий декоратор кладёт функцию в список/словарь и возвращает её.
- Метки — атрибуты функции (`func.tags`).
- `skip_if`, `parametrize`, `fixture` — декораторы с параметрами или состоянием.
- Pytest устроен на тех же приёмах, только богаче.
'''),
    short=t(r'''
```py
REGISTRY = []
def test(func):                     # регистрация
    REGISTRY.append(func)
    return func

def mark(*tags):                    # метки
    def deco(func):
        func.tags = set(tags)
        return func
    return deco

# pytest:
# @pytest.fixture
# @pytest.mark.smoke
# @pytest.mark.skipif(cond, reason="...")
# @pytest.mark.parametrize("a, b", [(1, 2), (3, 4)])
```
'''),
    quiz=[
        q('Что делает регистрирующий декоратор?',
            ['Оборачивает функцию', 'Сохраняет функцию в реестр и возвращает её', 'Удаляет функцию', 'Вызывает функцию сразу'],
            1, 'Функция остаётся прежней, но попадает в список.'),
        q('Как устроена метка `@mark("smoke")` в нашей реализации?',
            ['Обёртка', 'Атрибут функции `tags`', 'Глобальная переменная', 'Имя функции'],
            1, 'Раннер читает атрибут и фильтрует тесты.'),
        q('Что делает `@pytest.mark.parametrize`?',
            ['Пропускает тест', 'Запускает тест с разными наборами данных', 'Кэширует тест', 'Повторяет упавший тест'],
            1, 'Каждый набор — отдельный тест в отчёте.'),
    ],
),

}
