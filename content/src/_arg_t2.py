"""Теория модуля «**kwargs» темы «*args и **kwargs».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- arg-m2-l1 ----------
'arg-m2-l1': dict(
    full=t(r'''
## Зачем это нужно

`*args` собирает позиционные аргументы. Для **именованных** аргументов есть `**kwargs` — они собираются в **словарь** «имя → значение». Так делают функции с произвольными настройками: `request(url, timeout=5, verify=False)`, фабрики тестовых данных `make_user(name="admin", role="qa")`, построители запросов.

## Две звёздочки

```python
def show(**kwargs):
    print(kwargs, type(kwargs).__name__)

show(a=1, b="x")
show()
```

- `**kwargs` — «собери все именованные аргументы в словарь `kwargs`». Ключи — имена аргументов (строки), значения — переданные значения.
- Без именованных аргументов — пустой словарь.
- Вывод: `{'a': 1, 'b': 'x'} dict`, `{} dict`.
- Имя `kwargs` (от «keyword arguments») — соглашение; главное — две звёздочки.

## Работа с kwargs — как со словарём

```python
def describe(**info):
    for key, value in info.items():
        print(f"{key} = {value}")

describe(name="Аня", age=25)
```

- Порядок пар — порядок, в котором аргументы переданы при вызове.
- Вывод: `name = Аня`, `age = 25`.

```python
def count(**kw):
    return len(kw)

def to_query(**params):
    return "&".join(f"{k}={v}" for k, v in params.items())

print(count(), count(a=1, b=2), to_query(page=2, sort="name"))
```

Вывод: `0 2 page=2&sort=name`.

## Позиционные в **kwargs не попадают

```python
def show(**kwargs):
    return kwargs

try:
    show(1)
except TypeError as e:
    print(e)
```

- `**kwargs` собирает **только** именованные аргументы. Позиционный — ошибка.
- Вывод: `show() takes 0 positional arguments but 1 was given`.

## Имена аргументов — ключи-строки

```python
def f(**kw):
    return sorted(kw), all(isinstance(k, str) for k in kw)

print(f(b=1, a=2))
```

- Ключи всегда строки — это имена аргументов, записанные при вызове. Вывод: `(['a', 'b'], True)`.

## Фильтрация значений

```python
def only_numbers(**kwargs):
    return {k: v for k, v in kwargs.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}

print(only_numbers(a=1, b="x", c=2.5, d=True))
```

- Словарное включение — обычная обработка словаря. `bool` отсекаем отдельно: это подтип `int`.
- Вывод: `{'a': 1, 'c': 2.5}`.

## Итог

- `def f(**kwargs)` — все именованные аргументы собираются в **словарь**.
- Без именованных — `{}`; позиционные в `kwargs` не попадают.
- Ключи — строки-имена аргументов, порядок — порядок передачи.
- Внутри — обычный словарь: `items()`, `get`, включения.
'''),
    short=t(r'''
```py
def show(**kwargs):        # kwargs — СЛОВАРЬ именованных аргументов
    return kwargs
show(a=1, b="x")           # {'a': 1, 'b': 'x'}
show()                     # {}
show(1)                    # TypeError — позиционные сюда не попадают
for key, value in kwargs.items(): ...
```
'''),
    quiz=[
        q('Какой тип у `kwargs` в `def f(**kwargs)`?',
            ['tuple', 'list', 'dict', 'set'],
            2, 'Именованные аргументы — в словарь.'),
        q('Что вернёт `f(x=1, y=2)` для `def f(**kw): return list(kw)`?',
            ['`[1, 2]`', "`['x', 'y']`", '`[("x", 1), ("y", 2)]`', 'Ошибка'],
            1, 'Перебор словаря даёт ключи.'),
        q('Что будет при `f(5)` для `def f(**kw)`?',
            ['kw = {5: 5}', '`TypeError`', 'kw = {}', 'kw = (5,)'],
            1, 'Позиционный аргумент принять некуда.'),
    ],
),

# ---------- arg-m2-l2 ----------
'arg-m2-l2': dict(
    full=t(r'''
## Зачем это нужно

Обычно у функции есть несколько **обязательных** параметров и много **необязательных** настроек. Обязательные объявляют явно, а «всё остальное» собирают в `**kwargs` и читают с умолчаниями через `get`. Так устроены HTTP-клиенты: `requests.get(url, timeout=..., headers=..., params=...)`.

## Обычные параметры + **kwargs

```python
def connect(host, port=80, **options):
    print(host, port, options)

connect("db")
connect("db", 5432, timeout=5, ssl=True)
connect(host="x", retries=3)
```

- Сначала аргументы распределяются по **своим** параметрам (`host`, `port`) — позиционно или по имени.
- В `**options` попадают только те именованные аргументы, для которых своего параметра нет.
- Вывод: `db 80 {}`, `db 5432 {'timeout': 5, 'ssl': True}`, `x 80 {'retries': 3}`.

## Умолчания через get и pop

```python
def f(**kw):
    timeout = kw.get("timeout", 30)
    debug = kw.pop("debug", False)
    return timeout, debug, kw

print(f(), f(timeout=5, debug=True, x=1))
```

- `kw.get("timeout", 30)` — прочитать с умолчанием, ключ остаётся в словаре.
- `kw.pop("debug", False)` — **извлечь** с умолчанием: ключ удаляется. Удобно, когда функция сама обрабатывает часть настроек, а остальное передаёт дальше.
- Вывод: `(30, False, {}) (5, True, {'timeout': 5, 'x': 1})`.

## Без **kwargs лишнее — ошибка

```python
def strict(a, b):
    return a + b

def loose(a, b, **extra):
    return a + b

try:
    strict(1, 2, c=3)
except TypeError as e:
    print(e)
print(loose(1, 2, c=3))
```

- У `strict` нет параметра `c` — `TypeError: ... got an unexpected keyword argument 'c'`. Это **хорошо**: опечатка в имени сразу видна.
- `loose` молча принимает лишнее. Удобно для гибкости, но опечатку `timout=5` никто не заметит.
- Вывод: `strict() got an unexpected keyword argument 'c'`, `3`.

## Описание запроса

```python
def request(method, url, **options):
    return {
        "method": method.upper(),
        "url": url,
        "timeout": options.get("timeout", 10),
        "headers": options.get("headers", {}),
    }

print(request("get", "/users", timeout=3))
```

Вывод: `{'method': 'GET', 'url': '/users', 'timeout': 3, 'headers': {}}`.

## Умолчания словарём

```python
DEFAULTS = {"timeout": 30, "retries": 3}

def configure(**settings):
    return {**DEFAULTS, **settings}

print(configure(timeout=5), DEFAULTS)
```

- `{**DEFAULTS, **settings}` — новый словарь: сначала умолчания, поверх — переданные (тема «Словари»).
- Вывод: `{'timeout': 5, 'retries': 3} {'timeout': 30, 'retries': 3}`.

## Итог

- Обязательные параметры — явно, необязательные настройки — в `**kwargs`.
- В `**kwargs` попадают только именованные аргументы без своего параметра.
- `kw.get(k, умолчание)` — прочитать; `kw.pop(k, умолчание)` — извлечь.
- Без `**kwargs` неизвестное имя — `TypeError` (защита от опечаток); с ним — молчаливое принятие.
- `{**DEFAULTS, **kwargs}` — настройки с умолчаниями.
'''),
    short=t(r'''
```py
def connect(host, port=80, **options): ...
connect("db", 5432, timeout=5)   # options = {'timeout': 5}
timeout = kw.get("timeout", 30)  # прочитать с умолчанием
debug = kw.pop("debug", False)   # извлечь (ключ удалится)
{**DEFAULTS, **settings}         # умолчания + переданное
strict(1, c=3)                   # без **kwargs — TypeError (опечатки видны)
```
'''),
    quiz=[
        q('Что попадёт в `options` при `connect("db", port=1, ssl=True)` для `def connect(host, port=80, **options)`?',
            ["`{'port': 1, 'ssl': True}`", "`{'ssl': True}`", '`{}`', 'Ошибка'],
            1, 'port — свой параметр.'),
        q('Чем `kw.pop("x", 0)` отличается от `kw.get("x", 0)`?',
            ['Ничем', 'pop удаляет ключ из словаря', 'get удаляет ключ', 'pop без умолчания'],
            1, 'pop — извлечь.'),
        q('Какой минус у функции с `**kwargs`?',
            ['Медленная', 'Опечатка в имени аргумента не вызывает ошибку', 'Нельзя передать позиционные', 'Нет минусов'],
            1, 'Лишнее принимается молча.'),
    ],
),

# ---------- arg-m2-l3 ----------
'arg-m2-l3': dict(
    full=t(r'''
## Зачем это нужно

Как `*` раскладывает список в позиционные аргументы, так `**` при **вызове** раскладывает **словарь** в именованные. Это нужно, когда настройки уже лежат в словаре (прочитаны из конфига или JSON), а функция принимает их параметрами: `connect(**db_config)`.

## Две звёздочки при вызове

```python
def connect(host, port):
    return f"{host}:{port}"

cfg = {"host": "localhost", "port": 5432}
print(connect(**cfg))
print(connect("db", **{"port": 1}))
```

- `connect(**cfg)` — то же, что `connect(host="localhost", port=5432)`: каждая пара словаря становится именованным аргументом.
- Можно смешивать с обычными аргументами.
- Вывод: `localhost:5432`, `db:1`.

## Имена должны совпадать с параметрами

```python
def f(a, b):
    return a - b

params = {"b": 1, "a": 10}
print(f(**params))
try:
    f(**{"a": 1, "c": 2})
except TypeError as e:
    print(e)
```

- Порядок ключей не важен — значения раздаются **по именам**. `f(**params)` = `f(a=10, b=1)`.
- Лишний ключ `c` — `unexpected keyword argument`; не хватает `b` — `missing ... argument`.
- Вывод: `9`, `f() got an unexpected keyword argument 'c'`.

## Настройки print из словаря

```python
opts = {"sep": ", ", "end": "!\n"}
print("a", "b", **opts)
print("x", "y", **{"sep": "-"})
```

Вывод: `a, b!`, `x-y`.

## Словарь с умолчаниями + переопределения

```python
def build_url(host, port, path="/"):
    return f"http://{host}:{port}{path}"

defaults = {"host": "localhost", "port": 80}
print(build_url(**defaults))
print(build_url(**{**defaults, "port": 8080, "path": "/api"}))
```

- `{**defaults, ...}` собирает итоговый словарь, `**` раскладывает его в вызов.
- Вывод: `http://localhost:80/`, `http://localhost:8080/api`.

## Список словарей — в функцию по одному

```python
def format_user(name, age, city="?"):
    return f"{name}, {age}, {city}"

records = [{"name": "Аня", "age": 25}, {"age": 30, "name": "Боря", "city": "Казань"}]
print([format_user(**r) for r in records])
```

- Каждая запись раскладывается в параметры; отсутствующий `city` берётся по умолчанию.
- Вывод: `['Аня, 25, ?', 'Боря, 30, Казань']`.

## Безопасный вызов

```python
def f(a, b):
    return a + b

def safe_call(func, params):
    try:
        return func(**params)
    except TypeError:
        return None

print(safe_call(f, {"a": 1, "b": 2}), safe_call(f, {"a": 1}))
```

Вывод: `3 None`.

## Итог

- `f(**d)` раскладывает словарь в именованные аргументы.
- Ключи должны совпадать с именами параметров; порядок не важен.
- Лишний ключ или недостающий обязательный — `TypeError`.
- Комбинация `f(**{**defaults, **overrides})` — вызов с умолчаниями.
- В `def` две звёздочки собирают, в вызове — раскладывают.
'''),
    short=t(r'''
```py
connect(**{"host": "db", "port": 1})   # = connect(host="db", port=1)
connect("db", **{"port": 1})
f(**{"a": 1, "c": 2})                  # TypeError: unexpected keyword 'c'
func(**{**defaults, **overrides})
[format_user(**r) for r in records]
```
'''),
    quiz=[
        q('Что делает `f(**{"x": 1})`?',
            ['Передаёт словарь одним аргументом', 'Вызывает f(x=1)', 'Ошибка', 'Вызывает f(1)'],
            1, 'Пары становятся именованными аргументами.'),
        q('Важен ли порядок ключей в словаре при `f(**d)`?',
            ['Да', 'Нет — значения раздаются по именам', 'Только для первых двух', 'Зависит от версии'],
            1, 'Именованные аргументы сопоставляются по имени.'),
        q('Что будет при `f(**{"z": 1})` для `def f(a):`?',
            ['a = 1', '`TypeError`', 'a = None', 'z игнорируется'],
            1, 'Нет параметра z и не хватает a.'),
    ],
),

# ---------- arg-m2-l4 ----------
'arg-m2-l4': dict(
    full=t(r'''
## Зачем это нужно

`**kwargs` особенно удобен, когда функция **строит данные** из переданных полей: тело запроса, обновлённую копию объекта, HTML-атрибуты, фильтр по полям. Вызов читается как описание: `payload(name="Аня", age=25)`.

## Тело запроса без пустых полей

```python
def payload(**fields):
    return {k: v for k, v in fields.items() if v is not None}

print(payload(name="Аня", email=None, age=25))
```

- Необязательные поля, которые не заданы (`None`), в запрос не попадают. Значения `0`, `False`, `""` оставляем — это настоящие данные.
- Вывод: `{'name': 'Аня', 'age': 25}`.

## Обновлённая копия

```python
def update(obj, **changes):
    new = dict(obj)
    new.update(changes)
    return new

user = {"name": "Аня", "age": 25}
print(update(user, age=26), user)
```

- Изменения — именованными аргументами; исходный словарь не меняется.
- Короче: `return {**obj, **changes}`.
- Вывод: `{'name': 'Аня', 'age': 26} {'name': 'Аня', 'age': 25}`.

## Фильтр по полям

```python
def filter_users(users, **criteria):
    return [u for u in users if all(u.get(k) == v for k, v in criteria.items())]

users = [{"name": "Аня", "role": "qa", "age": 25}, {"name": "Боря", "role": "dev", "age": 25}]
print(filter_users(users, role="qa"))
print(len(filter_users(users, age=25)), len(filter_users(users)))
```

- Каждый именованный аргумент — условие «поле равно значению»; `all` требует выполнения всех.
- Без критериев `all(...)` пустого набора — `True`: подходят все.
- Вывод: список с Аней, затем `2 2`.

## HTML-атрибуты и зарезервированные слова

```python
def html(tag, text, **attrs):
    parts = "".join(f' {k.rstrip("_")}="{v}"' for k, v in attrs.items())
    return f"<{tag}{parts}>{text}</{tag}>"

print(html("a", "ссылка", href="/x"))
print(html("div", "hi", class_="card"))
```

- Имя аргумента должно быть допустимым именем Python. `class` — зарезервированное слово, поэтому принято писать `class_` и убирать `_` внутри функции.
- Вывод: `<a href="/x">ссылка</a>`, `<div class="card">hi</div>`.

## Строка лога

```python
def log_event(event, **data):
    return " ".join([event] + [f"{k}={data[k]}" for k in sorted(data)])

print(log_event("login", user="anna", ok=True))
```

- Сортировка ключей делает строки лога стабильными — их легко сравнивать и искать.
- Вывод: `login ok=True user=anna`.

## Итог

- `**kwargs` — удобный способ передать набор полей: тело запроса, изменения, фильтры, атрибуты.
- Пустые (`None`) поля отфильтровывай, `0`/`False` — оставляй.
- `{**obj, **changes}` — обновлённая копия.
- Зарезервированные слова передают с подчёркиванием: `class_`.
'''),
    short=t(r'''
```py
{k: v for k, v in fields.items() if v is not None}   # тело без None
{**obj, **changes}                                    # обновлённая копия
all(u.get(k) == v for k, v in criteria.items())       # фильтр по полям
html("div", "hi", class_="card")                      # class -> class_
k.rstrip("_")
```
'''),
    quiz=[
        q('Почему атрибут `class` передают как `class_`?',
            ['Так короче', '`class` — зарезервированное слово Python', 'Так требует HTML', 'Без причины'],
            1, 'Имя аргумента не может быть ключевым словом.'),
        q('Что вернёт `filter_users(users)` без критериев (all по пустому набору)?',
            ['Пустой список', 'Всех пользователей', 'Ошибку', 'None'],
            1, 'all([]) — True.'),
        q('Как сделать обновлённую копию словаря `obj` с изменениями из `**changes`?',
            ['`obj.update(changes)`', '`{**obj, **changes}`', '`obj + changes`', '`changes`'],
            1, 'Исходный не меняется.'),
    ],
),
}
