"""Теория модуля «Продвинутое и практика» темы «Генераторы».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- gen-send ----------
'gen-send': dict(
    full=t(r'''
## Зачем это нужно

Генератор умеет не только выдавать значения, но и **получать** их через `send`, а ещё его можно досрочно закрыть через `close`. Это нужно реже, но встречается: генераторы-накопители, конечные автоматы, `@contextmanager` (он построен на этом механизме), корректная уборка ресурсов в генераторе.

## send: значение внутрь генератора

```python
def echo():
    received = None
    while True:
        received = yield f"получил {received}"

g = echo()
print(next(g))
print(g.send("привет"))
print(g.send(42))
```

- `yield` — это ещё и **выражение**: `x = yield значение`.
- `g.send(v)` возобновляет генератор, и выражение `yield` принимает значение `v`. Затем генератор идёт до следующего `yield` и выдаёт его значение как результат `send`.
- Первый раз нужно вызвать `next(g)` (или `g.send(None)`), чтобы дойти до первого `yield`.
- Вывод: `получил None`, `получил привет`, `получил 42`.

## Генератор с состоянием

```python
def averager():
    total = count = 0
    avg = None
    while True:
        value = yield avg
        total += value
        count += 1
        avg = total / count

a = averager()
next(a)
print(a.send(10), a.send(20), a.send(60))
```

- Генератор хранит `total` и `count` между вызовами — как объект, но без класса.
- Вывод: `10.0 15.0 30.0`.

## close и finally

```python
def reader():
    print("открыл")
    try:
        n = 0
        while True:
            n += 1
            yield n
    finally:
        print("закрыл")

r = reader()
print(next(r), next(r))
r.close()
print("после close")
```

- `g.close()` завершает генератор: внутри в точке `yield` возникает `GeneratorExit`, и выполняются блоки `finally`.
- Генератор также закрывается, когда перестаёт быть нужен (сборщик мусора) — но полагаться лучше на явный `close` или `with`.
- Вывод: `открыл`, `1 2`, `закрыл`, `после close`.

## Уборка при досрочном выходе из for

```python
def lines(log):
    log.append("open")
    try:
        yield from ["a", "b", "c"]
    finally:
        log.append("close")

log = []
g = lines(log)
for line in g:
    if line == "a":
        break
g.close()
print(log)
```

- `break` не закрывает генератор сам по себе, пока на него есть ссылка. `close()` запускает `finally`.
- Вывод: `['open', 'close']`.

## Итог

- `x = yield value` — генератор может получать значения через `g.send(v)`.
- Перед первым `send` — `next(g)`.
- `g.close()` → `GeneratorExit` внутри → выполняется `finally`.
- Ресурсы в генераторе оборачивай в `try/finally`.
'''),
    short=t(r'''
```py
def acc():
    total = 0
    while True:
        x = yield total      # получить через send
        total += x

g = acc(); next(g)           # «прогреть» до первого yield
g.send(5)                    # 5
g.close()                    # GeneratorExit → finally
```
'''),
    quiz=[
        q('Что нужно сделать перед первым `g.send(value)`?',
            ['Ничего', 'Вызвать next(g) или g.send(None)', 'Вызвать g.close()', 'Создать список'],
            1, 'Генератор должен дойти до первого yield.'),
        q('Что происходит при `g.close()`?',
            ['Ничего', 'Внутри возникает GeneratorExit, выполняется finally', 'Генератор перезапускается', 'Ошибка всегда'],
            1, 'Так корректно освобождают ресурсы.'),
        q('Чем становится `yield` в записи `x = yield 1`?',
            ['Ошибкой', 'Выражением, которое получает значение из send', 'Циклом', 'return'],
            1, 'next() даёт None, send(v) — v.'),
    ],
),

# ---------- gen-bigdata ----------
'gen-bigdata': dict(
    full=t(r'''
## Зачем это нужно

Главная практическая сила генераторов — работа с данными, которые не помещаются в память или приходят частями: логи на гигабайты, большие CSV, API с пагинацией, потоки событий. Генератор обрабатывает по одному элементу и запрашивает следующую порцию только когда она нужна.

## Файл построчно

```python
with open("big.log", "w", encoding="utf-8") as f:
    for i in range(1000):
        f.write(f"{i} {'ERROR' if i % 250 == 0 else 'INFO'}\n")

def errors(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line:
                yield int(line.split()[0])

print(list(errors("big.log")))
```

- Файл внутри генератора открыт через `with` — закроется, когда генератор завершится.
- В памяти одновременно только одна строка.
- Вывод: `[0, 250, 500, 750]`.

## Пагинация API

```python
DATA = list(range(1, 8))

def fake_api(page, size=3):
    start = (page - 1) * size
    items = DATA[start:start + size]
    return {"items": items, "has_next": start + size < len(DATA)}

def all_items():
    page = 1
    while True:
        resp = fake_api(page)
        print("запрос страницы", page)
        yield from resp["items"]
        if not resp["has_next"]:
            break
        page += 1

for item in all_items():
    if item > 4:
        break
print("последний:", item)
```

- Для вызывающего кода все элементы выглядят как один поток — страницы спрятаны внутри генератора.
- Когда цикл прерван, лишние страницы не запрашиваются: третья страница не понадобилась.
- Вывод: `запрос страницы 1`, `запрос страницы 2`, `последний: 5`.

## Чтение кусками

```python
import io

def chunks(f, size):
    while True:
        block = f.read(size)
        if not block:
            return
        yield block

stream = io.StringIO("абвгдежз")
print(list(chunks(stream, 3)))
```

- `f.read(n)` читает не больше `n` символов (или байт в режиме `"rb"`). Пустой результат — конец файла.
- Так копируют и хешируют большие файлы, отправляют их по сети.
- Вывод: `['абв', 'где', 'жз']`.

## Подсчёт за один проход

```python
from collections import Counter

lines = (l for l in ["ERROR timeout", "INFO ok", "ERROR db", "ERROR timeout"])
counts = Counter(line[6:] for line in lines if line.startswith("ERROR "))
print(counts.most_common(1))
```

- Генератор можно перебрать только один раз, поэтому всю статистику собирают за один проход.
- `Counter` принимает итерируемое и считает вхождения; `most_common(n)` — самые частые.
- Вывод: `[('timeout', 2)]`.

## Итог

- Файлы, CSV, логи — генератор поверх `for line in f`.
- Пагинация — `while` + `yield from страница`; следующая страница только по требованию.
- Двоичные файлы — `read(size)` кусками.
- Данные из генератора — один проход: считай всё сразу.
'''),
    short=t(r'''
```py
def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")

def paginate(fetch):
    page = 1
    while items := fetch(page):
        yield from items
        page += 1

def chunks(f, size):
    while block := f.read(size):
        yield block
```
'''),
    quiz=[
        q('Почему генератор пагинации не запрашивает лишние страницы?',
            ['Кэширует их', 'Следующая страница запрашивается только когда нужны её элементы', 'API так устроен', 'Запрашивает все'],
            1, 'Ленивость.'),
        q('Что вернёт `f.read(3)` в конце файла?',
            ['None', 'Пустую строку', 'Ошибку', 'Последние 3 символа'],
            1, 'Пустой результат — сигнал конца.'),
        q('Сколько раз можно перебрать данные, пришедшие генератором?',
            ['Сколько угодно', 'Один', 'Два', 'Зависит от размера'],
            1, 'Собирай статистику за один проход.'),
    ],
),

# ---------- gen-memory ----------
'gen-memory': dict(
    full=t(r'''
## Зачем это нужно

Генератор экономит память, но умеет меньше, чем список. Нужно понимать, когда выбрать генератор, а когда — список, и как не наступить на грабли «функция перебирает данные дважды, а ей передали генератор».

## Размер в памяти

```python
import sys

big_list = [x for x in range(100_000)]
big_gen = (x for x in range(100_000))
print(sys.getsizeof(big_list) > 100_000, sys.getsizeof(big_gen) < 500)
print(sum(big_list) == sum(big_gen))
```

- `sys.getsizeof(obj)` — сколько байт занимает сам объект.
- Список хранит все 100 000 ссылок (сотни килобайт), генератор — только своё состояние (около двухсот байт), независимо от количества элементов.
- Вывод: `True True`, `True`.

## Чего генератор не умеет

```python
g = (x * 2 for x in range(5))
for op in [lambda: len(g), lambda: g[0]]:
    try:
        op()
    except TypeError as e:
        print(type(e).__name__)
items = list(g)
print(len(items), items[0], items[-1])
```

- У генератора нет длины, индексов и срезов: он не знает будущих элементов.
- Нужны они — превращай в список.
- Вывод: `TypeError`, `TypeError`, `5 0 8`.

## Два прохода

```python
from itertools import tee

def nums():
    yield from [3, 1, 2]

g = nums()
print(max(g), min(g, default="пусто"))

a, b = tee(nums())
print(max(a), min(b))

data = list(nums())
print(max(data), min(data))
```

- После `max` генератор пуст — `min` уже ничего не получит.
- `tee(it)` делает два независимых итератора из одного (внутри буферизует значения).
- Проще всего — сохранить в список, если данных немного.
- Вывод: `3 пусто`, `3 1`, `3 1`.

## Функция, которая принимает «что угодно»

```python
def normalize(values):
    values = list(values)
    top = max(values)
    return [v / top for v in values]

print(normalize(x for x in [1, 2, 4]))
```

- Если функции нужны несколько проходов, а на вход может прийти генератор — первой строкой сделай `list(values)`.
- Вывод: `[0.25, 0.5, 1.0]`.

## Как выбрать

- **Генератор**: один проход, большие или бесконечные данные, нужен только первый результат, конвейер.
- **Список**: несколько проходов, `len`, индексы, срезы, сортировка, данных немного.
- Сомневаешься — для небольших данных список проще и понятнее.

## Итог

- Генератор занимает постоянную память, список — пропорционально числу элементов.
- Нет `len`, индексов, повторного прохода.
- Несколько проходов — `list(...)` или `itertools.tee`.
- Выбор: один проход и много данных — генератор; иначе — список.
'''),
    short=t(r'''
```py
sys.getsizeof(gen)           # ~200 байт при любом размере
len(gen), gen[0]             # TypeError
max(g); min(g)               # второй — пусто!
a, b = itertools.tee(g)      # два прохода
values = list(values)        # если нужны len/индексы/повтор
sum(1 for _ in g)            # посчитать без списка
```
'''),
    quiz=[
        q('Что вернёт `len((x for x in range(3)))`?',
            ['3', 'TypeError', '0', 'None'],
            1, 'У генератора нет длины.'),
        q('Функции нужно два прохода по данным, а ей передают генератор. Что сделать?',
            ['Ничего', 'Первой строкой values = list(values)', 'Вызвать функцию дважды', 'Использовать len'],
            1, 'Или itertools.tee.'),
        q('Когда лучше генератор, чем список?',
            ['Всегда', 'Один проход по большим данным', 'Когда нужна сортировка', 'Когда нужны индексы'],
            1, 'Экономия памяти.'),
    ],
),

# ---------- gen-testing ----------
'gen-testing': dict(
    full=t(r'''
## Зачем это нужно

Генераторы — удобный инструмент тестировщика: они выдают уникальные тестовые данные, наборы проверок для параметризации, граничные значения, комбинации параметров. А фикстуры pytest с `yield` — это тоже генераторы.

## Уникальные тестовые данные

```python
from itertools import count

_ids = count(1)

def make_user():
    n = next(_ids)
    return {"id": n, "email": f"user{n}@test.ru"}

print(make_user())
print(make_user()["email"])
```

- Общий счётчик гарантирует, что каждый пользователь уникален — тесты не конфликтуют из-за занятых логинов и email.
- Вывод: `{'id': 1, 'email': 'user1@test.ru'}`, `user2@test.ru`.

## Набор случаев

```python
def cases():
    yield "", False
    yield "a@b.ru", True
    yield "без собаки", False

def is_email(s):
    return "@" in s and not s.startswith("@")

for value, expected in cases():
    print(repr(value), "ok" if is_email(value) == expected else "FAIL")
```

- Генератор выдаёт пары «вход → ожидание». Легко добавлять новые случаи.
- В pytest: `@pytest.mark.parametrize("value, expected", list(cases()))`.
- Вывод: `'' ok`, `'a@b.ru' ok`, `'без собаки' ok`.

## Граничные значения и комбинации

```python
from itertools import product

def boundary_values(low, high):
    seen = set()
    for v in (low - 1, low, low + 1, high - 1, high, high + 1):
        if v not in seen:
            seen.add(v)
            yield v

print(list(boundary_values(1, 100)))

params = {"browser": ["chrome", "firefox"], "lang": ["ru", "en"]}
combos = [dict(zip(params, values)) for values in product(*params.values())]
print(len(combos), combos[0])
```

- Граничные значения — классика тест-дизайна: ошибки чаще всего на краях диапазона.
- `product(*params.values())` — все комбинации значений; `zip(params, values)` связывает их с именами параметров.
- Вывод: `[0, 1, 2, 99, 100, 101]`, `4 {'browser': 'chrome', 'lang': 'ru'}`.

## Фикстура — это генератор

```python
def db_fixture(log):
    log.append("подключение")
    yield {"users": []}
    log.append("отключение")

log = []
gen = db_fixture(log)
db = next(gen)
db["users"].append("аня")
log.append(f"тест: {db['users']}")
next(gen, None)
print(log)
```

- Pytest поступает с фикстурой именно так: `next` — выполнить подготовку и получить значение, запустить тест, ещё один `next` — выполнить уборку после `yield`.
- `next(gen, None)` — дойти до конца без `StopIteration`.
- Строка с одинарными кавычками внутри выводится в двойных кавычках.
- Вывод: `['подключение', "тест: ['аня']", 'отключение']`.

## Итог

- `itertools.count` / генератор-фабрика — уникальные данные.
- Генераторы случаев — источник для `parametrize`.
- Граничные значения и `product` — тест-дизайн.
- Фикстуры с `yield` — генераторы: подготовка → значение → уборка.
'''),
    short=t(r'''
```py
from itertools import count, product
ids = count(1); next(ids)                # уникальные id

def cases():
    yield "", False
    yield "a@b.ru", True
# @pytest.mark.parametrize("v, exp", list(cases()))

[dict(zip(p, v)) for v in product(*p.values())]   # матрица

@pytest.fixture
def db():
    conn = connect(); yield conn; conn.close()
```
'''),
    quiz=[
        q('Зачем в тестовых данных уникальные id/email?',
            ['Красиво', 'Чтобы тесты не конфликтовали из-за повторов', 'Так требует pytest', 'Для скорости'],
            1, 'Повторный логин часто запрещён.'),
        q('Как pytest выполняет фикстуру с `yield`?',
            ['Вызывает один раз целиком', 'next до теста, next после теста', 'Только до yield', 'В отдельном процессе'],
            1, 'Код после yield — уборка.'),
        q('Какие значения относятся к граничным для диапазона 1–100?',
            ['50', '0, 1, 2, 99, 100, 101', 'Только 1 и 100', 'Случайные'],
            1, 'Около каждой границы — с обеих сторон.'),
    ],
),

}
