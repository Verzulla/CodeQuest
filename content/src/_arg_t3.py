"""Теория модуля «Всё вместе» темы «*args и **kwargs».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- arg-m3-l1 ----------
'arg-m3-l1': dict(
    full=t(r'''
## Зачем это нужно

В одной функции можно сочетать всё: обычные параметры, значения по умолчанию, `*args`, параметры только по имени и `**kwargs`. Чтобы читать чужие сигнатуры (библиотек, фреймворков) и писать свои, нужно знать **порядок** и правила распределения аргументов.

## Порядок в сигнатуре

```
def f(позиционные_только, /, обычные, *args, только_по_имени, **kwargs)
```

1. Параметры до `/` — только по позиции (необязательная часть).
2. Обычные параметры (по позиции или по имени), в том числе со значениями по умолчанию.
3. `*args` — остаток позиционных аргументов. Вместо него может стоять одиночная `*` — «дальше только по имени».
4. Параметры после `*args`/`*` — только по имени (keyword-only), могут быть обязательными.
5. `**kwargs` — остаток именованных; всегда последний.

Другой порядок — `SyntaxError`.

## Как раздаются аргументы

```python
def f(a, b=2, *args, c, d=4, **kwargs):
    print(a, b, args, c, d, kwargs)

f(1, c=3)
f(1, 5, 6, 7, c=8, e=9)
```

- Позиционные заполняют `a`, `b`, остаток — в `args`.
- Именованные сопоставляются с параметрами по имени (`c`, `d`), остаток — в `kwargs`.
- `c` без умолчания после `*args` — обязательный и только по имени.
- Вывод: `1 2 () 3 4 {}`, `1 5 (6, 7) 8 4 {'e': 9}`.

```viz
{"type": "paths", "auto": true, "title": "Как раздаются аргументы: выбери вызов", "cases": [{"label": "f(1, c=3)", "code": "def f(a, b=2, *args, c, **kwargs):\n    print(\"a =\", a, \"| b =\", b, \"| args =\", args, \"| c =\", c, \"| kwargs =\", kwargs)\n\nf(1, c=3)", "note": "`b` взял значение по умолчанию, `args` и `kwargs` пустые."}, {"label": "f(1, 5, c=3)", "code": "def f(a, b=2, *args, c, **kwargs):\n    print(\"a =\", a, \"| b =\", b, \"| args =\", args, \"| c =\", c, \"| kwargs =\", kwargs)\n\nf(1, 5, c=3)", "note": "Второй позиционный — в `b`."}, {"label": "f(1, 5, 6, 7, c=3)", "code": "def f(a, b=2, *args, c, **kwargs):\n    print(\"a =\", a, \"| b =\", b, \"| args =\", args, \"| c =\", c, \"| kwargs =\", kwargs)\n\nf(1, 5, 6, 7, c=3)", "note": "Лишние позиционные собрались в кортеж `args`."}, {"label": "f(1, c=3, d=4, e=5)", "code": "def f(a, b=2, *args, c, **kwargs):\n    print(\"a =\", a, \"| b =\", b, \"| args =\", args, \"| c =\", c, \"| kwargs =\", kwargs)\n\nf(1, c=3, d=4, e=5)", "note": "Лишние именованные — в словарь `kwargs`."}, {"label": "f(1, 2, 3)", "code": "def f(a, b=2, *args, c, **kwargs):\n    print(\"a =\", a, \"| b =\", b, \"| args =\", args, \"| c =\", c, \"| kwargs =\", kwargs)\n\nf(1, 2, 3)", "note": "`c` стоит после `*args` — его можно передать **только по имени**. Здесь его нет — ошибка."}]}
```

## Одиночная звёздочка: только по имени

```python
def g(*, key):
    return key

print(g(key=1))
try:
    g(1)
except TypeError:
    print("key только по имени")
```

- `*` без имени не собирает аргументы, а просто требует передавать всё после неё по имени. Вывод: `1`, `key только по имени`.

## Косая черта: только по позиции

```python
def h(a, /, b, *, c):
    return a + b + c

print(h(1, 2, c=3), h(1, b=2, c=3))
try:
    h(a=1, b=2, c=3)
except TypeError:
    print("a только по позиции")
```

- `a` — только позиционно, `b` — как угодно, `c` — только по имени. Вывод: `6 6`, `a только по позиции`.

## Реальный пример сигнатуры

```python
def run(cmd, *args, env=None, **options):
    return {"cmd": cmd, "args": list(args), "env": env or {}, "options": options}

print(run("pytest", "-v", "tests/", env={"CI": "1"}, timeout=60))
```

- Команда — первым аргументом, её аргументы — сколько угодно позиционных, окружение — только по имени, прочие опции — в `options`.
- `env or {}` — пустой словарь, если `env` не передан (а не изменяемое значение по умолчанию — тема «Функции»).
- Вывод: `{'cmd': 'pytest', 'args': ['-v', 'tests/'], 'env': {'CI': '1'}, 'options': {'timeout': 60}}`.

## Итог

- Порядок: `позиционные-только, /, обычные, *args (или *), только-по-имени, **kwargs`.
- Позиционные аргументы: сначала в обычные параметры, остаток — в `*args`.
- Именованные: по именам, остаток — в `**kwargs`.
- После `*args` или `*` — только по имени; до `/` — только по позиции.
'''),
    short=t(r'''
```py
def f(a, b=2, *args, c, d=4, **kwargs): ...
f(1, 5, 6, 7, c=8, e=9)   # a=1 b=5 args=(6,7) c=8 d=4 kwargs={'e':9}
def g(*, key): ...        # key только по имени
def h(a, /, b, *, c): ... # a — по позиции, c — по имени
# порядок: pos-only, /, обычные, *args|*, kw-only, **kwargs
```
'''),
    quiz=[
        q('Что попадёт в `args` при `f(1, 2, 3)` для `def f(a, b=0, *args)`?',
            ['`(2, 3)`', '`(3,)`', '`()`', '`(1, 2, 3)`'],
            1, 'a=1, b=2, остаток — 3.'),
        q('Какая сигнатура допустима?',
            ['`def f(**kw, *args)`', '`def f(*args, **kw)`', '`def f(**kw, a)`', '`def f(*args, *more)`'],
            1, '**kwargs — всегда последний.'),
        q('Что означает одиночная `*` в `def f(a, *, b)`?',
            ['b — список', 'b можно передать только по имени', 'b необязательный', 'Ошибка'],
            1, 'Дальше — только по имени.'),
    ],
),

# ---------- arg-m3-l2 ----------
'arg-m3-l2': dict(
    full=t(r'''
## Зачем это нужно

Главное практическое применение `*args` и `**kwargs` вместе — **функции-обёртки**: принять **любые** аргументы и передать их другой функции без изменений. Так делают логирование вызовов, повтор при ошибках, подсчёт вызовов, замер времени — и на этом построены декораторы (отдельная тема) и фикстуры тестовых фреймворков.

## Передать всё дальше

```python
def logged(func, *args, **kwargs):
    print("вызов", func.__name__, args, kwargs)
    return func(*args, **kwargs)

print(logged(max, 3, 7))
print(logged(sorted, [3, 1, 2], reverse=True))
```

- В `def` звёздочки **собирают** всё, что передали, в `args` и `kwargs`.
- В вызове `func(*args, **kwargs)` звёздочки **раскладывают** обратно — `func` получает ровно то же, что передали в обёртку.
- `func.__name__` — имя функции.
- Вывод: `вызов max (3, 7) {}`, `7`, `вызов sorted ([3, 1, 2],) {'reverse': True}`, `[3, 2, 1]`.

## Обёртка-замыкание

```python
def make_logger(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}{args} -> {result}")
        return result
    return wrapper

def add(a, b):
    return a + b

add = make_logger(add)
add(2, 3)
```

- `make_logger` возвращает **новую** функцию `wrapper`, которая помнит `func` (замыкание, тема «Область видимости»).
- `add = make_logger(add)` — подменяем функцию обёрнутой версией; вызывающий код не меняется. Это и есть идея **декоратора**.
- Вывод: `add(2, 3) -> 5`.

## Подсчёт вызовов

```python
calls = []

def counted(func):
    def wrapper(*args, **kwargs):
        calls.append(args)
        return func(*args, **kwargs)
    return wrapper

double = counted(lambda x: x * 2)
print(double(3), double(5), len(calls))
```

Вывод: `6 10 2`.

## Повтор при ошибке

```python
def retry(func, attempts, *args, **kwargs):
    for _ in range(attempts):
        try:
            return func(*args, **kwargs)
        except Exception:
            pass
    return None

print(retry(int, 3, "5"), retry(int, 3, "x"))
```

- Параметры самой обёртки (`func`, `attempts`) стоят **до** `*args`, чтобы не смешаться с аргументами `func`.
- Вывод: `5 None`.

## Параметры обёртки — только по имени

```python
def safe(func, *args, default=None, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception:
        return default

print(safe(int, "x", default=0), safe(int, "ff", base=16))
```

- `default` стоит после `*args` → передаётся только по имени и **не** уходит в `func`. А `base=16` уходит в `kwargs` и дальше в `int`.
- Вывод: `0 255`.

## Умолчания для чужой функции

```python
def with_defaults(func, **defaults):
    def wrapper(*args, **kwargs):
        return func(*args, **{**defaults, **kwargs})
    return wrapper

def connect(host, port=80, timeout=5):
    return (host, port, timeout)

c = with_defaults(connect, port=8080)
print(c("db"), c("db", port=1))
```

- Аргументы вызова важнее умолчаний обёртки. Вывод: `('db', 8080, 5) ('db', 1, 5)`. (В стандартной библиотеке то же делает `functools.partial`.)

## Итог

- Обёртка: `def wrapper(*args, **kwargs): return func(*args, **kwargs)` — передаёт всё без изменений.
- Собственные параметры обёртки — до `*args` или только по имени, чтобы не смешаться с аргументами `func`.
- Обёртка-замыкание, подменяющая функцию, — основа декораторов.
- Применения: логирование, повторы, подсчёт, умолчания.
'''),
    short=t(r'''
```py
def wrapper(*args, **kwargs):          # принять что угодно
    return func(*args, **kwargs)       # передать без изменений
def safe(func, *args, default=None, **kwargs): ...   # default — только по имени
def make_logger(func):
    def wrapper(*args, **kwargs): ...
    return wrapper
add = make_logger(add)                 # подмена — идея декоратора
```
'''),
    quiz=[
        q('Что делает `func(*args, **kwargs)` внутри обёртки?',
            ['Вызывает func без аргументов', 'Передаёт func те же аргументы, что получила обёртка', 'Ошибка', 'Передаёт кортеж и словарь двумя аргументами'],
            1, 'Звёздочки раскладывают обратно.'),
        q('Попадёт ли `default=0` в `func` при `safe(int, "x", default=0)` для `def safe(func, *args, default=None, **kwargs)`?',
            ['Да', 'Нет — это параметр самой safe', 'Только если int его принимает', 'Ошибка'],
            1, 'У default свой параметр.'),
        q('На каком приёме основаны декораторы?',
            ['Списковые включения', 'Обёртка-замыкание, которая принимает *args, **kwargs', 'Рекурсия', 'Кортежи'],
            1, 'Функция возвращает обёрнутую функцию.'),
    ],
),

# ---------- arg-m3-l3 ----------
'arg-m3-l3': dict(
    full=t(r'''
## Зачем это нужно

С `*args` и `**kwargs` появляются новые варианты `TypeError`. Сообщения точные — научившись их читать, ты мгновенно поймёшь, какой аргумент попал не туда.

## Обязательный параметр только по имени

```python
def f(a, *args, b):
    return a, args, b

try:
    f(1, 2, 3)
except TypeError as e:
    print(e)
print(f(1, 2, b=3))
```

- `*args` забрал все позиционные аргументы (2 и 3), для `b` ничего не осталось.
- Сообщение: `missing 1 required keyword-only argument: 'b'` — «не хватает обязательного аргумента, передаваемого только по имени».
- Вывод: сообщение, затем `(1, (2,), 3)`.

## Два значения для одного параметра

```python
def g(x, **kw):
    return x, kw

try:
    g(1, x=2)
except TypeError as e:
    print(e)
print(g(1, y=2))
```

- `1` уже ушло в `x` по позиции, а `x=2` пытается передать его ещё раз. В `**kw` оно не попадает — у `x` есть свой параметр.
- Вывод: `g() got multiple values for argument 'x'`, `(1, {'y': 2})`.

## Позиционный туда, где только **kwargs

```python
def h(**kw):
    return kw

try:
    h(1)
except TypeError as e:
    print(e)
print(h(**{"a": 1}))
try:
    h(**{1: "x"})
except TypeError:
    print("ключи должны быть строками")
```

- `**kw` принимает только именованные — `takes 0 positional arguments but 1 was given`.
- При `**словарь` ключи должны быть строками (это имена аргументов).
- Вывод: сообщение, `{'a': 1}`, `ключи должны быть строками`.

## Параметр ушёл в *args

```python
def summary(*values, precision):
    return round(sum(values), precision)

try:
    summary(1.234, 2.345, 2)
except TypeError as e:
    print(e)
print(summary(1.234, 2.345, precision=2))
```

- Классическая ошибка: хотели передать `precision`, а он стал третьим числом в `values`.
- Вывод: `summary() missing 1 required keyword-only argument: 'precision'`, `3.58`.

## Свои проверки аргументов

Функция с `**kwargs` молча принимает опечатки. Если набор допустимых настроек известен, проверь его сам и выбрось понятную ошибку:

```python
DEFAULTS = {"timeout": 30, "retries": 3}

def strict_config(**kwargs):
    for key in kwargs:
        if key not in DEFAULTS:
            raise TypeError(f"неизвестный параметр: {key}")
    return {**DEFAULTS, **kwargs}

print(strict_config(timeout=5))
try:
    strict_config(timout=5)
except TypeError as e:
    print(e)
```

- `raise TypeError(...)` — выбросить ошибку с собственным текстом (тема «Исключения»).
- Вывод: `{'timeout': 5, 'retries': 3}`, `неизвестный параметр: timout`.

## Итог

- `missing ... keyword-only argument` — обязательный параметр после `*args` не передан по имени.
- `got multiple values for argument` — аргумент передан и по позиции, и по имени.
- `takes 0 positional arguments` — позиционный аргумент туда, где только `**kwargs`.
- `keywords must be strings` — в `**словарь` ключи не строки.
- Для `**kwargs` с известным набором — своя проверка и `raise TypeError`.
'''),
    short=t(r'''
```py
f(1, 2, 3)            # missing 1 required keyword-only argument: 'b'
g(1, x=2)             # got multiple values for argument 'x'
h(1)                  # takes 0 positional arguments but 1 was given
h(**{1: "x"})         # keywords must be strings
summary(1, 2, precision=2)   # параметр после *args — по имени!
raise TypeError(f"неизвестный параметр: {key}")
```
'''),
    quiz=[
        q('Почему `f(1, 2, 3)` для `def f(a, *args, b)` падает?',
            ['Много аргументов', '*args забрал всё позиционное, b не передан', 'a лишний', 'Не падает'],
            1, 'b — только по имени.'),
        q('Что значит `got multiple values for argument \'x\'`?',
            ['x передан дважды: по позиции и по имени', 'x — список', 'x не передан', 'x лишний'],
            0, 'Один параметр — два значения.'),
        q('Как защититься от опечаток в именах при `**kwargs`?',
            ['Никак', 'Проверить ключи и выбросить TypeError для неизвестных', 'Использовать *args', 'Удалить **kwargs'],
            1, 'Своя проверка допустимого набора.'),
    ],
),

# ---------- arg-m3-l4 ----------
'arg-m3-l4': dict(
    full=t(r'''
## Зачем это нужно

В автотестах постоянно нужны **тестовые данные**: пользователь, товар, заказ — обычно «стандартный», но в каждом тесте с парой отличий. И нужен удобный **клиент API**, который принимает путь и любые параметры. Оба инструмента естественно пишутся через `**kwargs`.

## Фабрика тестовых данных

```python
def make_user(**overrides):
    user = {"name": "test", "email": "test@x.ru", "active": True}
    user.update(overrides)
    return user

print(make_user())
print(make_user(name="admin", active=False))
```

- Значения по умолчанию описаны один раз; тест указывает только то, что для него важно.
- Каждый вызов создаёт **новый** словарь — тесты не влияют друг на друга.
- Вывод: пользователь по умолчанию и пользователь `admin` с `active=False`.

Короче через распаковку: `return {"name": "test", ..., **overrides}`.

## Много объектов сразу

```python
def make_users(n, **common):
    return [{"id": i, **common} for i in range(1, n + 1)]

print(make_users(2, role="qa"))
```

- Общие поля передаются один раз, `id` у каждого свой. Вывод: `[{'id': 1, 'role': 'qa'}, {'id': 2, 'role': 'qa'}]`.

## Построитель запроса

```python
def build_request(method, path, **params):
    query = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
    line = f"{method.upper()} {path}"
    if query:
        line += "?" + query
    return line

print(build_request("get", "/users", page=2, q=None))
print(build_request("delete", "/users/7"))
```

- Параметры запроса — именованными аргументами; незаданные (`None`) пропускаются.
- Вывод: `GET /users?page=2`, `DELETE /users/7`.

## Клиент API: чёткие и свободные параметры

```python
def api_call(method, path, *, json=None, headers=None, **params):
    return {"method": method, "path": path, "params": params, "json": json, "headers": headers or {}}

print(api_call("POST", "/users", json={"name": "Аня"}, page=1))
```

- Важные параметры (`json`, `headers`) объявлены явно и только по имени — их видно в сигнатуре, и в них нельзя опечататься.
- Всё прочее — параметры запроса — в `**params`.
- Вывод: `{'method': 'POST', 'path': '/users', 'params': {'page': 1}, 'json': {'name': 'Аня'}, 'headers': {}}`.

Так устроен популярный `requests`: `requests.post(url, json=..., headers=..., params=..., timeout=...)`.

## Одинаковые настройки для многих вызовов

```python
def batch(func, items, **kwargs):
    return [func(item, **kwargs) for item in items]

print(batch(round, [1.234, 5.678], ndigits=1), batch(int, ["ff", "10"], base=16))
```

Вывод: `[1.2, 5.7] [255, 16]`.

## Итог

- Фабрика данных: умолчания + `**overrides`; каждый вызов — новый объект.
- `make_users(n, **common)` — пачка объектов с общими полями.
- Параметры запроса — `**params`, `None` пропускаем.
- Важные параметры — явно (и только по имени), остальное — в `**kwargs`.
'''),
    short=t(r'''
```py
def make_user(**overrides):
    return {"name": "test", "active": True, **overrides}
[{"id": i, **common} for i in range(1, n + 1)]
"&".join(f"{k}={v}" for k, v in params.items() if v is not None)
def api_call(method, path, *, json=None, headers=None, **params): ...
[func(item, **kwargs) for item in items]
```
'''),
    quiz=[
        q('Что вернёт `make_user(active=False)` для фабрики с умолчаниями `{"name": "test", "active": True}`?',
            ['`{"active": False}`', '`{"name": "test", "active": False}`', 'Ошибка', '`{"name": "test", "active": True}`'],
            1, 'Переопределяется только переданное.'),
        q('Зачем фабрика создаёт новый словарь при каждом вызове?',
            ['Быстрее', 'Чтобы тесты не влияли друг на друга', 'Так требует Python', 'Не нужно'],
            1, 'Общий объект испортился бы между тестами.'),
        q('Почему `json` и `headers` в `api_call` объявлены явно, а не в `**params`?',
            ['Короче', 'Они видны в сигнатуре и защищены от опечаток', 'Так быстрее', 'Иначе ошибка'],
            1, 'Важные параметры — явно.'),
    ],
),
}
