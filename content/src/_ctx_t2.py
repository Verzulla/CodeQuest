"""Теория модуля «contextlib» темы «Контекстные менеджеры».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- ctx-m2-l1 ----------
'ctx-m2-l1': dict(
    full=t(r'''
## Зачем это нужно

Писать класс с `__enter__` и `__exit__` ради простого «сделать до и после» — многословно. Модуль `contextlib` позволяет написать менеджер как **функцию** с `yield`: всё, что до `yield`, — вход, всё, что после, — выход.

## @contextmanager

```python
from contextlib import contextmanager

@contextmanager
def step(name):
    print("▶", name)
    yield
    print("✔", name)

with step("логин"):
    print("вводим пароль")
```

Что делает каждая строка:

- `from contextlib import contextmanager` — декоратор из стандартной библиотеки.
- `@contextmanager` превращает функцию-генератор в контекстный менеджер.
- Код до `yield` выполняется при входе в `with`.
- На `yield` функция «замирает» — в это время выполняется тело блока `with`.
- После блока функция продолжается с места `yield` — это выход.
- `yield` в функции делает её **генератором** (подробно — в теме «Генераторы»). Здесь важно одно: `yield` должен выполниться ровно один раз.
- Вывод: `▶ логин`, `вводим пароль`, `✔ логин`.

## Значение для as

```python
from contextlib import contextmanager

@contextmanager
def opened(name):
    print("открываю", name)
    yield name.upper()
    print("закрываю", name)

with opened("db") as handle:
    print("работаю с", handle)
print(handle)
```

- `yield значение` — это значение попадёт в переменную после `as` (как `return` из `__enter__`).
- Вывод: `открываю db`, `работаю с DB`, `закрываю db`, `DB`.

## Подготовка данных

```python
from contextlib import contextmanager

@contextmanager
def collector():
    items = []
    yield items
    items.sort()

with collector() as items:
    items.extend([3, 1, 2])
    print("внутри:", items)
print("после:", items)
```

- Менеджер создаёт объект, отдаёт его в блок, а после блока обрабатывает.
- Вывод: `внутри: [3, 1, 2]`, `после: [1, 2, 3]`.

## Временная ресурсная обёртка

```python
from contextlib import contextmanager

@contextmanager
def temp_user():
    user = {"name": "test_user"}
    print("создан")
    try:
        yield user
    finally:
        print("удалён")

try:
    with temp_user() as u:
        print(u["name"])
        raise RuntimeError("тест упал")
except RuntimeError as e:
    print("ошибка:", e)
```

- Если внутри блока произошла ошибка, она «возникает» в точке `yield`. Без `try/finally` код после `yield` не выполнится.
- `try: yield ... finally: уборка` — обязательный шаблон, когда уборка важна (подробно — в следующем уроке).
- Вывод: `создан`, `test_user`, `удалён`, `ошибка: тест упал`.

## Итог

- `@contextmanager` + функция с одним `yield`.
- До `yield` — вход, после — выход; `yield x` → `as x`.
- Для надёжной уборки — `try/finally` вокруг `yield`.
'''),
    short=t(r'''
```py
from contextlib import contextmanager

@contextmanager
def resource(name):
    r = acquire(name)       # вход
    try:
        yield r             # → as r; здесь выполняется блок
    finally:
        release(r)          # выход (всегда)

with resource("db") as r:
    ...
```
'''),
    quiz=[
        q('Что попадает в `as` у менеджера на `@contextmanager`?',
            ['Возвращаемое значение функции', 'Значение из yield', 'Сама функция', 'None всегда'],
            1, 'yield x работает как return из __enter__.'),
        q('Сколько раз должен выполниться `yield` в такой функции?',
            ['Сколько угодно', 'Ровно один', 'Ни одного', 'Два: вход и выход'],
            1, 'Иначе RuntimeError.'),
        q('Где выполняется тело блока `with` относительно функции-менеджера?',
            ['До вызова функции', 'В момент yield', 'После return', 'Параллельно'],
            1, 'Функция замирает на yield.'),
    ],
),

# ---------- ctx-gen-errors ----------
'ctx-gen-errors': dict(
    full=t(r'''
## Зачем это нужно

Если внутри блока `with` возникает исключение, Python «забрасывает» его в функцию-менеджер **в точку `yield`**. Если это не учесть, уборка после `yield` не выполнится. Зато с `try/except` вокруг `yield` менеджер может реагировать на ошибки: логировать, глушить, переводить в другие.

## Без try уборка пропадает

```python
from contextlib import contextmanager

@contextmanager
def resource():
    print("взял")
    yield
    print("вернул")

try:
    with resource():
        raise ValueError("сбой")
except ValueError:
    print("ошибка")
```

- Ошибка из блока возникает на строке `yield`. Код после неё не выполняется — «вернул» не напечатано. Ресурс утёк!
- Вывод: `взял`, `ошибка`.

## try/finally спасает

```python
from contextlib import contextmanager

@contextmanager
def resource():
    print("взял")
    try:
        yield
    finally:
        print("вернул")

try:
    with resource():
        raise ValueError("сбой")
except ValueError:
    print("ошибка")
```

- `finally` выполнится и при успехе, и при ошибке. Исключение после этого полетит дальше.
- Вывод: `взял`, `вернул`, `ошибка`.
- Правило: если после `yield` есть уборка — оберни `yield` в `try/finally`.

## Поймать и заглушить

```python
from contextlib import contextmanager

@contextmanager
def soft(name):
    try:
        yield
    except ZeroDivisionError as e:
        print(f"{name}: поймал {e}")
    else:
        print(f"{name}: без ошибок")

with soft("A"):
    1 / 0
with soft("B"):
    pass
print("дальше")
```

- `except` вокруг `yield` ловит ошибку из блока. Если не выбросить её снова — она **заглушена** (как `return True` в `__exit__`).
- `else` — выполняется, если ошибки не было.
- Вывод: `A: поймал division by zero`, `B: без ошибок`, `дальше`.

## Записать и пробросить

```python
from contextlib import contextmanager

@contextmanager
def step(log, name):
    try:
        yield
    except AssertionError as e:
        log.append(f"FAIL {name}: {e}")
        raise
    log.append(f"PASS {name}")

log = []
with step(log, "открыть"):
    pass
try:
    with step(log, "войти"):
        assert False, "нет кнопки"
except AssertionError:
    pass
print(log)
```

- `raise` без аргументов — пробросить ту же ошибку дальше, тест всё равно упадёт.
- Код после `try/except` выполнится только при успехе.
- Вывод: `['PASS открыть', 'FAIL войти: нет кнопки']`.

## Перевести ошибку

```python
from contextlib import contextmanager

@contextmanager
def translate(from_exc, to_exc, message):
    try:
        yield
    except from_exc as e:
        raise to_exc(message) from e

try:
    with translate(KeyError, LookupError, "нет пользователя"):
        {}["anna"]
except LookupError as e:
    print(type(e).__name__, e, type(e.__cause__).__name__)
```

- `raise новая from старая` — выбросить понятную ошибку, сохранив исходную в `__cause__`.
- `except from_exc` — в `except` можно подставить переменную с классом ошибки.
- Вывод: `LookupError нет пользователя KeyError`.

## Итог

- Ошибка из блока появляется в точке `yield`.
- `try/finally` вокруг `yield` — обязательная уборка.
- `except` без повторного `raise` — глушит; с `raise` — пробрасывает.
- `raise X from e` — перевести ошибку.
'''),
    short=t(r'''
```py
@contextmanager
def cm():
    setup()
    try:
        yield
    except KeyError:
        ...              # без raise — заглушить
    except AssertionError:
        log(); raise     # записать и пробросить
    else:
        ...              # не было ошибки
    finally:
        cleanup()        # всегда
```
'''),
    quiz=[
        q('Где возникает исключение из блока `with` внутри функции с `@contextmanager`?',
            ['В начале функции', 'В точке yield', 'После функции', 'Нигде'],
            1, 'Python «забрасывает» его в генератор.'),
        q('Что будет с уборкой после `yield` без `try/finally`, если в блоке ошибка?',
            ['Выполнится', 'Не выполнится', 'Выполнится дважды', 'Зависит от ошибки'],
            1, 'Код после yield пропускается.'),
        q('Как заглушить ошибку в менеджере на `@contextmanager`?',
            ['return True', 'Поймать в except вокруг yield и не выбрасывать снова', 'yield None', 'Нельзя'],
            1, 'Пойманная ошибка считается обработанной.'),
    ],
),

# ---------- ctx-m2-l2 ----------
'ctx-m2-l2': dict(
    full=t(r'''
## Зачем это нужно

В `contextlib` уже есть готовые менеджеры для частых задач: игнорировать ожидаемую ошибку, перехватить вывод функции, открыть заранее неизвестное число ресурсов. Их полезно знать, чтобы не писать свои.

## suppress: игнорировать ошибку

```python
from contextlib import suppress

with suppress(KeyError):
    print("до")
    {}["x"]
    print("после")
print("дальше")
```

- `suppress(Тип1, Тип2, ...)` глушит перечисленные исключения.
- Блок прерывается в месте ошибки — «после» не напечатается, выполнение продолжится после `with`.
- Короткая замена `try: ... except KeyError: pass`.
- Вывод: `до`, `дальше`.

## Удалить, если есть

```python
import os
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("возможно_нет.txt")
print("ок")
```

- Типичное применение: удалить файл, которого может не быть.
- Вывод: `ок`.

## redirect_stdout и redirect_stderr

```python
import io
import sys
from contextlib import redirect_stdout, redirect_stderr

buf = io.StringIO()
with redirect_stdout(buf):
    print("секрет")
print("перехвачено:", buf.getvalue().strip())

err = io.StringIO()
with redirect_stderr(err):
    print("предупреждение", file=sys.stderr)
print("stderr:", err.getvalue().strip())
```

- `redirect_stdout(файл)` — всё, что печатается внутри блока, уходит в указанный «файл», а не на экран.
- `io.StringIO()` — файл в памяти; `getvalue()` — перехваченный текст.
- `redirect_stderr` — то же для потока ошибок (`sys.stderr`).
- Так в тестах проверяют, что функция напечатала правильный текст.
- Вывод: `перехвачено: секрет`, `stderr: предупреждение`.

## ExitStack: много менеджеров

```python
from contextlib import contextmanager, ExitStack

@contextmanager
def res(name):
    print("открыл", name)
    yield name
    print("закрыл", name)

with ExitStack() as stack:
    for name in ["БД", "браузер"]:
        stack.enter_context(res(name))
    print("тест")
```

- `ExitStack` — «стопка» менеджеров. `stack.enter_context(менеджер)` входит в него и запоминает, что нужно выйти.
- При выходе из `with ExitStack()` все менеджеры закрываются **в обратном порядке**.
- Нужен, когда количество ресурсов заранее неизвестно (список файлов, набор сервисов).
- Вывод: `открыл БД`, `открыл браузер`, `тест`, `закрыл браузер`, `закрыл БД`.

## ExitStack.callback

```python
from contextlib import ExitStack

log = []
with ExitStack() as stack:
    stack.callback(log.append, "удалить пользователя")
    stack.callback(log.append, "закрыть браузер")
    log.append("тест")
print(log)
```

- `callback(функция, *аргументы)` — зарегистрировать функцию уборки. Вызовутся при выходе, в обратном порядке.
- Вывод: `['тест', 'закрыть браузер', 'удалить пользователя']`.

## Итог

- `suppress(*типы)` — игнорировать ошибки.
- `redirect_stdout(buf)` / `redirect_stderr(buf)` — перехват вывода.
- `ExitStack`: `enter_context(cm)`, `callback(f, *args)`; выход в обратном порядке.
'''),
    short=t(r'''
```py
from contextlib import suppress, redirect_stdout, ExitStack
import io

with suppress(FileNotFoundError):
    os.remove(p)

buf = io.StringIO()
with redirect_stdout(buf):
    func()
buf.getvalue()

with ExitStack() as stack:
    files = [stack.enter_context(open(p)) for p in paths]
    stack.callback(cleanup, arg)     # вызов при выходе
```
'''),
    quiz=[
        q('Что делает `suppress(KeyError)`?',
            ['Выбрасывает KeyError', 'Игнорирует KeyError внутри блока', 'Удаляет ключ', 'Логирует ошибку'],
            1, 'Аналог try/except KeyError: pass.'),
        q('Когда нужен `ExitStack`?',
            ['Всегда вместо with', 'Когда число менеджеров заранее неизвестно', 'Для исключений', 'Для генераторов'],
            1, 'enter_context в цикле.'),
        q('Как перехватить то, что печатает функция?',
            ['suppress', 'redirect_stdout с io.StringIO', 'ExitStack', 'closing'],
            1, 'Вывод уйдёт в буфер.'),
    ],
),

# ---------- ctx-stdlib ----------
'ctx-stdlib': dict(
    full=t(r'''
## Зачем это нужно

Контекстные менеджеры встречаются по всей стандартной библиотеке. Знать их — значит писать короче и надёжнее: закрыть объект без `__exit__`, временно сменить папку или точность вычислений, подставить «пустой» менеджер.

## closing: для объектов с close()

```python
from contextlib import closing

class Connection:
    def __init__(self):
        self.open = True

    def query(self):
        return "данные"

    def close(self):
        self.open = False
        print("соединение закрыто")

with closing(Connection()) as conn:
    print(conn.query())
print(conn.open)
```

- У многих старых объектов есть метод `close()`, но нет `__enter__`/`__exit__`.
- `closing(obj)` делает из них менеджер: при выходе вызовет `obj.close()`.
- Если метод называется иначе (`quit()`, `disconnect()`), используй `try/finally` или свой менеджер.
- Вывод: `данные`, `соединение закрыто`, `False`.

## nullcontext: менеджер-заглушка

```python
from contextlib import nullcontext

def process(data, lock=None):
    with lock if lock is not None else nullcontext():
        return sum(data)

print(process([1, 2, 3]))
with nullcontext("значение") as v:
    print(v)
```

- `nullcontext()` ничего не делает при входе и выходе. Нужен, когда менеджер то есть, то нет, — чтобы не писать код дважды.
- `nullcontext(x)` отдаёт `x` в `as`.
- Вывод: `6`, `значение`.

## chdir: временно сменить папку

```python
import os
from contextlib import chdir
from pathlib import Path

Path("work/inner").mkdir(parents=True, exist_ok=True)
start = os.getcwd()
with chdir("work"):
    print(sorted(os.listdir(".")))
print(os.getcwd() == start)
```

- `chdir(путь)` (Python 3.11+) — сменить текущую папку на время блока и вернуть обратно.
- `os.getcwd()` — текущая рабочая папка.
- Вывод: `['inner']`, `True`.

## localcontext: временная точность

```python
from decimal import Decimal, localcontext

with localcontext() as ctx:
    ctx.prec = 3
    print(Decimal(1) / Decimal(7))
print(Decimal(1) / Decimal(7))
```

- `Decimal` — точные десятичные числа (для денег). `prec` — число значащих цифр.
- `localcontext()` меняет настройки только внутри блока.
- Вывод: `0.143`, `0.1428571428571428571428571429`.

## Другие менеджеры, которые стоит знать

```py
open(...)                          # файлы
tempfile.TemporaryDirectory()      # временная папка
threading.Lock()                   # блокировка для потоков
sqlite3.connect(...)               # транзакция БД (commit/rollback)
requests.Session()                 # HTTP-сессия
unittest.mock.patch(...)           # подмена объекта в тестах
pytest.raises(...)                 # ожидаемое исключение
```

- Общее правило: если у объекта есть «открыть/закрыть» или «начать/закончить» — скорее всего, он поддерживает `with`.

## Итог

- `closing(obj)` — вызовет `obj.close()`.
- `nullcontext(x)` — пустой менеджер.
- `chdir(path)`, `localcontext()` — временная смена состояния.
- Многие объекты библиотек — менеджеры: используй `with`.
'''),
    short=t(r'''
```py
from contextlib import closing, nullcontext, chdir
from decimal import localcontext

with closing(obj) as o: ...          # obj.close() при выходе
cm = open(p) if p else nullcontext() # заглушка
with chdir("dir"): ...               # 3.11+, вернёт папку
with localcontext() as ctx:
    ctx.prec = 5                     # точность Decimal
```
'''),
    quiz=[
        q('Что делает `closing(obj)`?',
            ['Закрывает obj сразу', 'Вызывает obj.close() при выходе из with', 'Вызывает obj.quit()', 'Удаляет obj'],
            1, 'Для объектов без __exit__, но с close().'),
        q('Зачем нужен `nullcontext()`?',
            ['Для ошибок', 'Как пустой менеджер, когда настоящий не нужен', 'Для потоков', 'Для None'],
            1, 'Чтобы не дублировать код с with и без.'),
        q('Что вернёт `os.getcwd()` после блока `with chdir("work")`?',
            ['work', 'Исходную папку', 'Ошибку', 'None'],
            1, 'Папка восстанавливается.'),
    ],
),

}
