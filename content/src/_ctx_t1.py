"""Теория модуля «Оператор with» темы «Контекстные менеджеры».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- ctx-m1-l1 ----------
'ctx-m1-l1': dict(
    full=t(r'''
## Зачем это нужно

Многие ресурсы нужно не только взять, но и обязательно **отдать**: закрыть файл, закрыть соединение с базой, выйти из браузера, удалить тестового пользователя. Если между «взял» и «отдал» случится ошибка, уборка не выполнится — и ресурсы «утекут». **Контекстный менеджер** и оператор `with` гарантируют уборку в любом случае.

## try/finally: уборка всегда

```python
try:
    print("начало")
    1 / 0
    print("не дойдём")
except ZeroDivisionError:
    print("поймали")
finally:
    print("уборка")
```

- `finally` выполняется **всегда**: и после успешного `try`, и после исключения (пойманного или нет).
- Вывод: `начало`, `поймали`, `уборка`.

## finally при return и break

```python
def f():
    try:
        return "из try"
    finally:
        print("finally")

print(f())
for i in range(3):
    try:
        if i == 1:
            break
    finally:
        print("итерация", i)
```

- Даже `return` не обходит `finally`: сначала выполнится `finally`, потом функция вернёт значение.
- То же с `break` и `continue`.
- Вывод: `finally`, `из try`, `итерация 0`, `итерация 1`.

## Ручная уборка — многословно

```python
f = open("notes.txt", "w", encoding="utf-8")
try:
    f.write("данные")
finally:
    f.close()
print(f.closed)
```

- Правильный, но громоздкий способ: открыть, всё остальное — в `try`, закрытие — в `finally`.
- Вывод: `True`.

## with делает то же короче

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("первая\n")
    f.write("вторая\n")
print(f.closed)

with open("notes.txt", encoding="utf-8") as f:
    print(f.read().splitlines())
```

- `with выражение as имя:` — выражение должно вернуть **контекстный менеджер**: объект, который умеет «войти» и «выйти».
- При входе файл открыт, при выходе из блока (любом: обычном, по `return`, по исключению) — закрыт.
- Это ровно тот же `try/finally`, только спрятанный внутрь объекта.
- Вывод: `True`, `['первая', 'вторая']`.

## Функция с гарантированной уборкой

```python
def run_with_cleanup(action, cleanup):
    try:
        return action()
    finally:
        cleanup()

log = []
print(run_with_cleanup(lambda: 42, lambda: log.append("убрано")), log)
```

- Шаблон «сделать и в любом случае убрать» — основа всех контекстных менеджеров.
- Вывод: `42 ['убрано']`.

## Итог

- `finally` выполняется всегда: после успеха, ошибки, `return`, `break`.
- `with` — короткая запись `try/finally` для объектов-менеджеров.
- Файлы, соединения, блокировки — всегда через `with`.
'''),
    short=t(r'''
```py
try:
    ...
except SomeError:
    ...
finally:
    cleanup()             # всегда: успех, ошибка, return, break

with open(p, encoding="utf-8") as f:   # = try/finally f.close()
    ...
f.closed                  # True после блока
```
'''),
    quiz=[
        q('Выполнится ли `finally`, если в `try` стоит `return`?',
            ['Нет', 'Да, перед возвратом значения', 'Только при ошибке', 'Только без return'],
            1, 'finally нельзя обойти.'),
        q('Что гарантирует `with open(...) as f`?',
            ['Файл откроется быстрее', 'Файл закроется при любом выходе из блока', 'Ошибок не будет', 'Файл не изменится'],
            1, 'Даже при исключении.'),
        q('Какой конструкции эквивалентен `with`?',
            ['if/else', 'try/finally', 'for', 'while'],
            1, 'Вход — до try, выход — в finally.'),
    ],
),

# ---------- ctx-multi ----------
'ctx-multi': dict(
    full=t(r'''
## Зачем это нужно

Часто нужно несколько ресурсов сразу: читать один файл и писать в другой, открыть браузер и соединение с базой. Их можно открыть в одном `with` — важно понимать, в каком порядке они откроются и закроются.

## Несколько менеджеров через запятую

```python
with open("a.txt", "w", encoding="utf-8") as fa, open("b.txt", "w", encoding="utf-8") as fb:
    fa.write("A")
    fb.write("B")
print(fa.closed, fb.closed)
with open("a.txt", encoding="utf-8") as fa, open("b.txt", encoding="utf-8") as fb:
    print(fa.read() + fb.read())
```

- Менеджеры перечисляются через запятую, у каждого свой `as`.
- После блока закрыты все.
- Вывод: `True True`, `AB`.

## Порядок: вход слева направо, выход — наоборот

```python
class Box:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print("открыл", self.name)
        return self

    def __exit__(self, *args):
        print("закрыл", self.name)

with Box("А") as a, Box("Б") as b:
    print("внутри", a.name, b.name)
```

- `Box` — простой свой менеджер (как их писать — в следующем уроке).
- Запись через запятую равна вложенным `with`: `with A: with B: ...`.
- Закрытие в **обратном** порядке: последний открытый закрывается первым. Так `Б`, который мог зависеть от `А`, закроется раньше.
- Вывод: `открыл А`, `открыл Б`, `внутри А Б`, `закрыл Б`, `закрыл А`.

## Если второй не открылся

```python
class Box:
    def __init__(self, name, fail=False):
        self.name = name
        self.fail = fail

    def __enter__(self):
        if self.fail:
            raise OSError(f"не открыть {self.name}")
        print("открыл", self.name)
        return self

    def __exit__(self, *args):
        print("закрыл", self.name)

try:
    with Box("БД") as db, Box("браузер", fail=True) as br:
        print("тест")
except OSError as e:
    print(e)
```

- Первый менеджер уже открыт — он будет закрыт, хотя второй упал при открытии.
- Тело блока не выполняется.
- Вывод: `открыл БД`, `закрыл БД`, `не открыть браузер`.

## Длинный with в скобках

```python
with (
    open("in.txt", "w", encoding="utf-8") as fin,
    open("out.txt", "w", encoding="utf-8") as fout,
):
    fin.write("x")
    fout.write("y")
print(fin.closed and fout.closed)
```

- С Python 3.10 менеджеры можно взять в скобки и расположить по одному на строке — удобно, когда строка слишком длинная.
- Вывод: `True`.

## Заранее неизвестное число файлов

```python
paths = ["f1.txt", "f2.txt"]
for i, p in enumerate(paths):
    with open(p, "w", encoding="utf-8") as f:
        f.write(str(i))

contents = []
for p in paths:
    with open(p, encoding="utf-8") as f:
        contents.append(f.read())
print(contents)
```

- Если файлы нужны по очереди — `with` внутри цикла.
- Если нужны **одновременно**, а их число неизвестно, используют `ExitStack` (урок про готовые менеджеры).
- Вывод: `['0', '1']`.

## Итог

- `with A() as a, B() as b:` — несколько менеджеров, как вложенные `with`.
- Вход слева направо, выход — справа налево.
- Если один не открылся, открытые раньше всё равно закроются.
- Длинный список — в скобках, по одному на строке.
'''),
    short=t(r'''
```py
with open(a) as fa, open(b, "w") as fb:   # = вложенные with
    ...

with (                                     # Python 3.10+
    open(a) as fa,
    open(b, "w") as fb,
):
    ...
# вход: A → B;  выход: B → A
# упал вход в B → A всё равно закроется
```
'''),
    quiz=[
        q('В каком порядке закроются менеджеры в `with A() as a, B() as b:`?',
            ['A, затем B', 'B, затем A', 'Одновременно', 'Случайно'],
            1, 'Обратно порядку открытия.'),
        q('Что будет с A, если `B.__enter__` выбросил исключение?',
            ['A не закроется', 'A закроется', 'A откроется заново', 'Программа зависнет'],
            1, 'Уже открытые менеджеры всегда закрываются.'),
        q('С какой версии Python можно писать менеджеры в скобках на нескольких строках?',
            ['2.7', '3.6', '3.10', '4.0'],
            2, 'Парентезированные контекстные менеджеры.'),
    ],
),

# ---------- ctx-m1-l2 ----------
'ctx-m1-l2': dict(
    full=t(r'''
## Зачем это нужно

`with` работает не только с файлами. Любой объект, у которого есть методы `__enter__` и `__exit__`, — контекстный менеджер. Написав их, ты сделаешь свой класс «самоубирающимся»: сессия API, соединение с базой, браузер, временные данные.

## Протокол менеджера

```python
class Tag:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"<{self.name}>")

    def __exit__(self, *args):
        print(f"</{self.name}>")

with Tag("div"):
    with Tag("p"):
        print("текст")
```

- `with Tag("div"):` — сначала создаётся объект, затем Python вызывает его `__enter__()`.
- После блока — `__exit__(...)`, в любом случае.
- `*args` — `__exit__` получает три аргумента об исключении (разберём в уроке про исключения), здесь они не нужны.
- Вывод: `<div>`, `<p>`, `текст`, `</p>`, `</div>`.

## Что попадает в as

```python
class Conn:
    def __enter__(self):
        return "соединение №1"

    def __exit__(self, *args):
        return False

with Conn() as c:
    print(c)
```

- В переменную после `as` попадает **то, что вернул `__enter__`** — не обязательно сам объект.
- Чаще всего `__enter__` возвращает `self`, чтобы внутри блока пользоваться методами объекта.
- Вывод: `соединение №1`.

## Полноценный пример

```python
class Resource:
    def __init__(self, name, log):
        self.name = name
        self.log = log
        self.opened = False

    def __enter__(self):
        self.opened = True
        self.log.append("open " + self.name)
        return self

    def __exit__(self, exc_type, exc, tb):
        self.opened = False
        self.log.append("close " + self.name)
        return False

    def use(self):
        return f"работаю с {self.name}"

log = []
with Resource("db", log) as r:
    print(r.use(), r.opened)
print(r.opened, log)
```

- `__enter__` захватывает ресурс и возвращает `self`.
- `__exit__` освобождает ресурс. `return False` — «исключения не глушить» (подробно — дальше).
- Объект из `as` доступен и после блока, но уже в «закрытом» состоянии.
- Вывод: `работаю с db True`, `False ['open db', 'close db']`.

## Повторное использование

```python
class Counter:
    def __init__(self):
        self.entered = 0

    def __enter__(self):
        self.entered += 1
        return self

    def __exit__(self, *args):
        return False

c = Counter()
with c:
    pass
with c as same:
    print(same is c, same.entered)
```

- В `with` можно передать уже созданный объект. Один объект может входить в `with` много раз — если его логика это позволяет. Файл, например, после закрытия заново не откроешь.
- Вывод: `True 2`.

## Итог

- Менеджер — объект с `__enter__(self)` и `__exit__(self, exc_type, exc, tb)`.
- `with obj as x:` — `x` = результат `__enter__` (обычно `self`).
- `__exit__` вызывается всегда; `return False` — не глушить ошибки.
'''),
    short=t(r'''
```py
class Resource:
    def __enter__(self):
        # захватить ресурс
        return self                      # → в as

    def __exit__(self, exc_type, exc, tb):
        # освободить ресурс (всегда)
        return False                     # не глушить ошибки

with Resource() as r:
    r.use()
```
'''),
    quiz=[
        q('Что попадает в переменную после `as`?',
            ['Сам объект всегда', 'Результат `__enter__`', 'Результат `__exit__`', 'None'],
            1, 'Чаще всего __enter__ возвращает self.'),
        q('Когда вызывается `__exit__`?',
            ['Только при ошибке', 'При любом выходе из блока', 'Только при успехе', 'При создании объекта'],
            1, 'Как finally.'),
        q('Какие два метода делают класс контекстным менеджером?',
            ['__init__ и __del__', '__enter__ и __exit__', '__open__ и __close__', '__start__ и __stop__'],
            1, 'Это протокол контекстного менеджера.'),
    ],
),

# ---------- ctx-exit ----------
'ctx-exit': dict(
    full=t(r'''
## Зачем это нужно

Главная сила `__exit__` — он **знает**, закончился ли блок ошибкой, и может на неё отреагировать: записать в лог, сделать скриншот, откатить изменения или даже заглушить ошибку. Так устроены `pytest.raises`, `contextlib.suppress`, транзакции в базах данных.

## Аргументы __exit__

```python
class Show:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        print(exc_type, exc, tb is None)
        return False

with Show():
    print("без ошибки")

try:
    with Show():
        int("x")
except ValueError:
    print("ошибка полетела дальше")
```

- `exc_type` — класс исключения, `exc` — сам объект исключения, `tb` — трассировка (traceback).
- Если блок завершился без ошибки — все три `None`.
- Вывод: `без ошибки`, `None None True`, `<class 'ValueError'> invalid literal for int() with base 10: 'x' False`, `ошибка полетела дальше`.

## Возвращаемое значение: глушить или нет

```python
class IgnoreKey:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return exc_type is not None and issubclass(exc_type, KeyError)

with IgnoreKey():
    {}["нет"]
print("KeyError заглушен")

try:
    with IgnoreKey():
        [][0]
except IndexError:
    print("IndexError прошёл насквозь")
```

- `__exit__` вернул **истину** → исключение считается обработанным, программа продолжается после `with`.
- Вернул `False` или `None` (или ничего не вернул) → исключение летит дальше.
- `issubclass(exc_type, KeyError)` — проверка типа ошибки с учётом наследников.
- Глушить стоит только **конкретные** ожидаемые ошибки.
- Вывод: `KeyError заглушен`, `IndexError прошёл насквозь`.

## Реакция на ошибку без глушения

```python
class Status:
    def __init__(self, log):
        self.log = log

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.log.append("ok" if exc_type is None else f"fail: {exc_type.__name__}")
        return False

log = []
with Status(log):
    pass
try:
    with Status(log):
        raise TimeoutError
except TimeoutError:
    pass
print(log)
```

- Записали результат и отпустили исключение дальше — вызывающий код о нём узнает.
- Вывод: `['ok', 'fail: TimeoutError']`.

## Откат изменений

```python
class Transaction:
    def __init__(self, data):
        self.data = data

    def __enter__(self):
        self.snapshot = dict(self.data)
        return self.data

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.data.clear()
            self.data.update(self.snapshot)
        return False

account = {"balance": 100}
try:
    with Transaction(account):
        account["balance"] -= 500
        raise ValueError("недостаточно средств")
except ValueError as e:
    print(e, account)
```

- При входе делаем снимок, при ошибке восстанавливаем. Так работают транзакции в базах данных: всё или ничего.
- `clear()` + `update()` меняют **тот же** словарь, поэтому изменения видны снаружи.
- Вывод: `недостаточно средств {'balance': 100}`.

## return внутри with

```python
class Log:
    def __enter__(self):
        print("вход")
        return self

    def __exit__(self, exc_type, exc, tb):
        print("выход, ошибка:", exc_type)

def find(items, target):
    with Log():
        for i, x in enumerate(items):
            if x == target:
                return i
    return -1

print(find(["a", "b"], "b"))
```

- `return` из середины блока — тоже выход: `__exit__` вызывается с `None`.
- Вывод: `вход`, `выход, ошибка: None`, `1`.

## Итог

- `__exit__(self, exc_type, exc, tb)`: при успехе — три `None`.
- Вернуть `True` — заглушить исключение; `False`/`None` — пропустить дальше.
- Глуши только конкретные типы (`issubclass`).
- `__exit__` подходит для логов, скриншотов, откатов.
'''),
    short=t(r'''
```py
def __exit__(self, exc_type, exc, tb):
    if exc_type is None:
        ...                        # блок прошёл успешно
    elif issubclass(exc_type, KeyError):
        return True                # заглушить
    else:
        rollback()                 # среагировать
    return False                   # пропустить ошибку дальше
```
'''),
    quiz=[
        q('Что получает `__exit__`, если блок прошёл без ошибок?',
            ['Ничего', 'Три None', 'Объект Success', 'True'],
            1, 'exc_type, exc и tb — None.'),
        q('Что будет, если `__exit__` вернёт `True` при исключении?',
            ['Исключение полетит дальше', 'Исключение будет заглушено', 'Блок выполнится заново', 'Ошибка TypeError'],
            1, 'Программа продолжится после with.'),
        q('Что вернёт `__exit__` без явного return?',
            ['True', 'None — исключение пойдёт дальше', 'False — ошибка', 'self'],
            1, 'None — ложное значение.'),
    ],
),

}
