"""Теория модуля «Магия и удобства» темы «Классы».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- oop-m3-l1 ----------
'oop-m3-l1': dict(
    full=t(r'''
## Зачем это нужно

Почему `len("abc")` работает, `3 + 4` работает, `x in [1, 2]` работает? Потому что у встроенных классов есть специальные методы с двойными подчёркиваниями — **dunder-методы** (double underscore), или «магические» методы. Добавив их в свой класс, ты научишь его работать с операторами `+`, `==`, `in`, `len()`, `for`, `[]`.

## Как это устроено

Python переводит операторы в вызовы методов:

- `a + b` → `a.__add__(b)`
- `a == b` → `a.__eq__(b)`
- `len(a)` → `a.__len__()`
- `x in a` → `a.__contains__(x)`
- `a[i]` → `a.__getitem__(i)`
- `for x in a` → `a.__iter__()`
- `bool(a)`, `if a:` → `a.__bool__()` (или `__len__`)
- `a(...)` → `a.__call__(...)`
- `str(a)` → `__str__`, `repr(a)` → `__repr__`

Сами эти методы напрямую обычно не вызывают — их вызывает Python.

## Сложение и равенство

```python
class Money:
    def __init__(self, amount):
        self.amount = amount

    def __add__(self, other):
        return Money(self.amount + other.amount)

    def __eq__(self, other):
        return self.amount == other.amount

    def __repr__(self):
        return f"Money({self.amount})"

total = Money(100) + Money(50)
print(total, total == Money(150))
```

- `__add__` возвращает **новый** объект, а не меняет `self` — так же ведут себя числа.
- `__eq__` возвращает `True`/`False`. Без него `==` сравнивал бы объекты как `is`.
- Вывод: `Money(150) True`.

## Класс-коллекция

```python
class Playlist:
    def __init__(self, songs):
        self.songs = songs

    def __len__(self):
        return len(self.songs)

    def __contains__(self, song):
        return song in self.songs

    def __getitem__(self, i):
        return self.songs[i]

p = Playlist(["a", "b", "c"])
print(len(p), "b" in p, p[0], p[-1], p[1:])
for song in p:
    print(song, end=" ")
print()
```

- `__getitem__` получает индекс или срез и передаёт его списку — поэтому работают и `p[-1]`, и `p[1:]`.
- Если нет `__iter__`, `for` использует `__getitem__` с индексами 0, 1, 2… до `IndexError`.
- Вывод: `3 True a c ['b', 'c']`, затем `a b c`.

## Своя итерация: __iter__

```python
class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

print(list(Countdown(3)), sum(Countdown(4)))
```

- `__iter__` с `yield` — самый простой способ сделать объект перебираемым (подробно `yield` — в теме «Генераторы»).
- Каждый `for` вызывает `__iter__` заново, поэтому объект можно перебирать много раз.
- Вывод: `[3, 2, 1] 10`.

## Истинность: __bool__ и __len__

```python
class Queue:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

class Flag:
    def __init__(self, on):
        self.on = on

    def __bool__(self):
        return self.on

print(bool(Queue([])), bool(Queue([1])))
print("включён" if Flag(True) else "выключен")
```

- `if obj:` сначала ищет `__bool__`, затем `__len__` (0 — ложь). Если нет ни того, ни другого — объект всегда истинный.
- Вывод: `False True`, `включён`.

## Вызываемый объект: __call__

```python
class Multiplier:
    def __init__(self, k):
        self.k = k

    def __call__(self, x):
        return x * self.k

double = Multiplier(2)
print(double(21), list(map(Multiplier(3), [1, 2])))
```

- Объект с `__call__` можно вызывать как функцию — и передавать туда, где ждут функцию (`map`, `sorted(key=...)`).
- В отличие от функции, у него есть состояние (`self.k`).
- Вывод: `42 [3, 6]`.

## Итог

- Операторы и встроенные функции вызывают dunder-методы.
- `__add__` возвращает новый объект; `__eq__` — `True`/`False`.
- Коллекция: `__len__`, `__contains__`, `__getitem__`, `__iter__`.
- `__bool__` — истинность, `__call__` — вызов как функции.
'''),
    short=t(r'''
```py
a + b      → __add__(self, other)   # вернуть новый
a == b     → __eq__(self, other)
len(a)     → __len__(self)
x in a     → __contains__(self, x)
a[i]       → __getitem__(self, i)
for x in a → __iter__(self)         # можно через yield
if a:      → __bool__ / __len__
a(x)       → __call__(self, x)
str / repr → __str__ / __repr__
```
'''),
    quiz=[
        q('Какой метод вызывает `x in obj`?',
            ['`__in__`', '`__contains__`', '`__has__`', '`__iter__`'],
            1, 'Если его нет, Python попробует перебрать объект.'),
        q('Что должен возвращать `__add__`?',
            ['None', 'Новый объект-результат', 'self', 'True'],
            1, 'Как и у чисел: `a + b` не меняет `a`.'),
        q('Что позволяет вызывать объект как функцию `obj(5)`?',
            ['`__init__`', '`__call__`', '`__func__`', '`__run__`'],
            1, 'Объект с `__call__` — «вызываемый».'),
    ],
),

# ---------- oop-compare ----------
'oop-compare': dict(
    full=t(r'''
## Зачем это нужно

Объекты часто нужно сравнивать, сортировать, класть в множества и использовать как ключи словаря: убрать дубликаты пользователей, отсортировать баги по серьёзности, найти последнюю версию. Для этого у класса должны быть методы сравнения и хеш.

## Операторы сравнения

- `==` → `__eq__`, `!=` → `__ne__` (по умолчанию — «не `__eq__`»)
- `<` → `__lt__` (less than), `<=` → `__le__`
- `>` → `__gt__` (greater than), `>=` → `__ge__`

```python
class Task:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

tasks = [Task("деплой", 3), Task("баг", 1), Task("ревью", 2)]
print([t.name for t in sorted(tasks)])
print(max(tasks).name, Task("a", 1) > Task("b", 2))
```

- `sorted`, `min`, `max` используют только `<` — достаточно `__lt__`.
- `a > b` Python может выполнить как `b < a` — поэтому работает и `>`.
- Вывод: `['баг', 'ревью', 'деплой']`, `деплой False`.

## total_ordering: все операторы из двух

```python
from functools import total_ordering

@total_ordering
class Grade:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

a, b = Grade(4), Grade(5)
print(a < b, a <= b, a > b, a >= Grade(4), a != b)
```

- Декоратор `@total_ordering` досоздаёт `<=`, `>`, `>=` по `__eq__` и `__lt__`.
- Вывод: `True True False True True`.

## Сравнение по кортежу

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, text):
        self.parts = tuple(int(p) for p in text.split("."))

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):
        return self.parts < other.parts

print(Version("1.10.0") > Version("1.9.3"), Version("2.0") == Version("2.0"))
```

- Кортежи сравниваются поэлементно — удобная основа для сравнения объектов по нескольким полям.
- `(1, 10, 0) > (1, 9, 3)`, потому что `10 > 9`. Строки `"1.10" < "1.9"` сравнились бы неправильно!
- Вывод: `True True`.

## NotImplemented

```python
class Money:
    def __init__(self, amount):
        self.amount = amount

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount

print(Money(5) == Money(5), Money(5) == 5)
```

- Если тип другого объекта не подходит, верни `NotImplemented` (специальное значение, **не** исключение). Python попробует сравнение с другой стороны, а если и там не выйдет — для `==` вернёт `False`.
- Без этой проверки `Money(5) == 5` упал бы с `AttributeError: 'int' object has no attribute 'amount'`.
- Вывод: `True False`.

## __hash__: объекты в множествах и словарях

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

try:
    {Point(1, 2)}
except TypeError as e:
    print(e)
```

- **Хеш** — число, по которому множество и словарь быстро находят элемент.
- Правило: **равные объекты обязаны иметь одинаковый хеш**. Поэтому, если определить `__eq__`, Python отключает хеш по умолчанию.
- Вывод: `unhashable type: 'Point'`.

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

print(len({Point(1, 2), Point(1, 2), Point(3, 4)}))
print({Point(0, 0): "начало"}[Point(0, 0)])
```

- `hash((self.x, self.y))` — хешируем кортеж тех же полей, которые сравниваем.
- Вывод: `2`, `начало`.
- Осторожно: если поля объекта поменять после добавления в множество, он «потеряется». Хешируемые объекты лучше делать неизменяемыми.

## Сортировка без методов сравнения

Если класс менять нельзя или сортировка нужна «по-разному» — используй `key`:

```python
class User:
    def __init__(self, name, age):
        self.name, self.age = name, age

us = [User("Вика", 25), User("Аня", 30), User("Боря", 25)]
print([u.name for u in sorted(us, key=lambda u: (-u.age, u.name))])
```

- `(-u.age, u.name)` — по возрасту по убыванию (минус), при равенстве — по имени.
- Вывод: `['Аня', 'Боря', 'Вика']`.

## Итог

- `__lt__` достаточно для `sorted/min/max`; `@total_ordering` + `__eq__` + `__lt__` — все операторы.
- Сравнивай кортежи полей.
- Чужой тип → `return NotImplemented`.
- `__eq__` без `__hash__` → объект нельзя класть в set/dict. Хешируй те же поля.
'''),
    short=t(r'''
```py
from functools import total_ordering

@total_ordering
class V:
    def __init__(self, a, b): self.a, self.b = a, b
    def key(self): return (self.a, self.b)
    def __eq__(self, o):
        if not isinstance(o, V): return NotImplemented
        return self.key() == o.key()
    def __lt__(self, o): return self.key() < o.key()
    def __hash__(self): return hash(self.key())

sorted(objs)                         # нужен __lt__
sorted(objs, key=lambda u: (-u.age, u.name))
```
'''),
    quiz=[
        q('Какого метода достаточно для `sorted(objects)`?',
            ['`__eq__`', '`__lt__`', '`__hash__`', '`__cmp__`'],
            1, 'Сортировка использует только оператор `<`.'),
        q('Что происходит с `__hash__`, если определить только `__eq__`?',
            ['Ничего', 'Он отключается — объект нельзя класть в set', 'Генерируется автоматически по полям', 'Ошибка при объявлении'],
            1, 'Иначе равные объекты могли бы иметь разный хеш.'),
        q('Что вернуть из `__eq__`, если другой объект неподходящего типа?',
            ['False', 'NotImplemented', 'raise TypeError', 'None'],
            1, 'Python попробует другую сторону и вернёт False для ==.'),
    ],
),

# ---------- oop-m3-l2 ----------
'oop-m3-l2': dict(
    full=t(r'''
## Зачем это нужно

Три декоратора делают классы удобнее:

- `@property` — метод, который выглядит как атрибут: можно проверять присваивания и вычислять значения на лету;
- `@classmethod` — метод класса, чаще всего — альтернативный конструктор (`User.from_string("...")`);
- `@staticmethod` — обычная функция, которую логично держать внутри класса.

## property: вычисляемый атрибут

```python
class Circle:
    def __init__(self, r):
        self.r = r

    @property
    def diameter(self):
        return self.r * 2

c = Circle(5)
print(c.diameter)
c.r = 10
print(c.diameter)
try:
    c.diameter = 1
except AttributeError:
    print("нельзя")
```

- `@property` над методом — к нему обращаются **без скобок**: `c.diameter`.
- Значение каждый раз вычисляется заново, поэтому после `c.r = 10` оно актуально (в отличие от атрибута, посчитанного в `__init__`).
- Без setter свойство только для чтения → `AttributeError` при присваивании.
- Вывод: `10`, `20`, `нельзя`.

## setter: проверка при присваивании

```python
class Product:
    def __init__(self, price):
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("цена < 0")
        self._price = value

p = Product(100)
p.price = 150
print(p.price)
try:
    p.price = -5
except ValueError as e:
    print(e, p.price)
```

- `@price.setter` — метод, который вызывается при `p.price = ...`.
- Настоящее значение хранится в `self._price`. Подчёркивание в начале — соглашение «внутреннее, не трогай снаружи». Если бы setter писал в `self.price`, он вызвал бы сам себя бесконечно.
- `self.price = price` в `__init__` тоже проходит через setter — проверка работает и при создании.
- Вывод: `150`, `цена < 0 150`.

## Соглашения об именах

- `name` — публичный атрибут.
- `_name` — внутренний: снаружи использовать можно, но не принято.
- `__name` — Python переименовывает его в `_Класс__name`, чтобы потомки случайно не перезаписали. Нужно редко.

## classmethod: альтернативный конструктор

```python
class Pizza:
    count = 0

    def __init__(self, toppings):
        self.toppings = toppings
        Pizza.count += 1

    @classmethod
    def margherita(cls):
        return cls(["сыр", "томаты"])

    @staticmethod
    def is_valid(topping):
        return topping != "ананас"

p = Pizza.margherita()
print(p.toppings, Pizza.count)
print(Pizza.is_valid("ананас"), p.is_valid("сыр"))
```

- `@classmethod` получает первым параметром не объект, а **класс** — его называют `cls`.
- `cls([...])` создаёт объект. Почему `cls`, а не `Pizza`? Если потомок вызовет `Потомок.margherita()`, создастся объект потомка.
- `@staticmethod` не получает ни `self`, ни `cls` — это обычная функция в «пространстве имён» класса. Вызывается и через класс, и через объект.
- Вывод: `['сыр', 'томаты'] 1`, `False True`.

## Классический пример: из строки

```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_string(cls, text):
        name, age = text.split(",")
        return cls(name.strip(), int(age))

u = User.from_string("Аня, 30")
print(u.name, u.age)
```

- Разбор строки спрятан в классе — снаружи одна понятная строчка.
- Так устроены `dict.fromkeys`, `datetime.fromisoformat`, `int.from_bytes`.
- Вывод: `Аня 30`.

## Итог

- `@property` — вычисление без скобок; `@x.setter` — проверка присваивания, значение в `self._x`.
- `@classmethod` (`cls`) — альтернативные конструкторы и работа с атрибутами класса.
- `@staticmethod` — функция без `self`/`cls`, логически относящаяся к классу.
'''),
    short=t(r'''
```py
class Product:
    def __init__(self, price):
        self.price = price           # через setter

    @property
    def price(self):                 # p.price
        return self._price

    @price.setter
    def price(self, v):              # p.price = v
        if v < 0: raise ValueError
        self._price = v

    @classmethod
    def free(cls):                   # Product.free()
        return cls(0)

    @staticmethod
    def fmt(v):                      # Product.fmt(5)
        return f"{v} ₽"
```
'''),
    quiz=[
        q('Как обратиться к свойству `diameter`, объявленному через `@property`?',
            ['`c.diameter()`', '`c.diameter`', '`c.get_diameter()`', '`Circle.diameter(c)()`'],
            1, 'Свойство читается как атрибут, без скобок.'),
        q('Что получает первым параметром `@classmethod`?',
            ['Объект', 'Класс', 'Ничего', 'Родителя'],
            1, 'Параметр принято называть `cls`.'),
        q('Почему setter хранит значение в `self._price`, а не в `self.price`?',
            ['Так быстрее', 'Иначе setter вызывал бы сам себя бесконечно', 'Требование синтаксиса', 'Чтобы скрыть от потомков'],
            1, '`self.price = ...` снова вызывает setter.'),
    ],
),

# ---------- oop-dataclass ----------
'oop-dataclass': dict(
    full=t(r'''
## Зачем это нужно

Многие классы просто хранят данные: пользователь, заказ, результат теста. Для них приходится писать однообразный `__init__`, `__repr__`, `__eq__`. Декоратор `@dataclass` генерирует всё это автоматически по списку полей.

## Первый dataclass

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int = 0

p = Point(1, 2)
print(p, Point(5))
print(p == Point(1, 2))
p.x = 10
print(p.x)
```

- `x: int` — **аннотация типа**: поле `x`, ожидается `int`. Python тип **не проверяет** — это подсказка для людей и редакторов.
- `y: int = 0` — поле со значением по умолчанию. Поля с умолчанием должны идти **после** полей без него.
- `@dataclass` создал `__init__(self, x, y=0)`, `__repr__` и `__eq__` (сравнение всех полей по порядку).
- Вывод: `Point(x=1, y=2) Point(x=5, y=0)`, `True`, `10`.

## Списки по умолчанию: field(default_factory=...)

```python
from dataclasses import dataclass, field

@dataclass
class Order:
    id: int
    items: list = field(default_factory=list)
    status: str = "new"

a = Order(1)
b = Order(2, status="paid")
a.items.append("чай")
print(a)
print(b)
```

- Писать `items: list = []` нельзя — dataclass выдаст `ValueError`, защищая от общего списка.
- `field(default_factory=list)` — вызывать `list()` для каждого нового объекта.
- Вывод: `Order(id=1, items=['чай'], status='new')`, `Order(id=2, items=[], status='paid')`.

## Проверка в __post_init__

```python
from dataclasses import dataclass

@dataclass
class Range:
    start: int
    stop: int

    def __post_init__(self):
        if self.start > self.stop:
            raise ValueError("start > stop")

    @property
    def length(self):
        return self.stop - self.start

print(Range(2, 5).length)
try:
    Range(5, 2)
except ValueError as e:
    print(e)
```

- `__init__` генерируется автоматически, но после него dataclass вызывает `__post_init__` — место для проверок и вычислений.
- В dataclass можно добавлять любые методы и свойства, как в обычный класс.
- Вывод: `3`, `start > stop`.

## frozen и order

```python
from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int

vs = [Version(1, 10), Version(1, 2), Version(0, 9)]
print(sorted(vs)[0], max(vs))
try:
    vs[0].major = 2
except Exception as e:
    print(type(e).__name__)
print(len({Version(1, 0), Version(1, 0)}))
```

- `order=True` — генерирует `<`, `<=`, `>`, `>=`: сравнение как кортежей полей по порядку объявления.
- `frozen=True` — объект неизменяемый: присваивание → `FrozenInstanceError` (потомок `AttributeError`). Зато появляется `__hash__` — можно класть в множество.
- Вывод: `Version(major=0, minor=9) Version(major=1, minor=10)`, `FrozenInstanceError`, `1`.

## asdict и replace

```python
from dataclasses import dataclass, asdict, replace

@dataclass
class User:
    name: str
    age: int

u = User("Аня", 30)
u2 = replace(u, age=31)
print(asdict(u), u2)
print(u == User("Аня", 30), u == u2)
```

- `asdict(obj)` — словарь полей (удобно для `json.dumps` и тел запросов).
- `replace(obj, поле=...)` — **копия** с изменёнными полями; исходный объект не меняется.
- Вывод: `{'name': 'Аня', 'age': 30} User(name='Аня', age=31)`, `True False`.

## Из JSON в объекты

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

data = [{"name": "Аня", "age": 30}, {"name": "Боря", "age": 25}]
users = [User(**d) for d in data]
print(users[1])
```

- `User(**d)` — распаковать словарь в именованные аргументы. Лишний ключ в словаре вызовет `TypeError`, тогда передавай поля явно: `User(d["name"], d["age"])`.
- Вывод: `User(name='Боря', age=25)`.

## Итог

- `@dataclass` + аннотации полей → `__init__`, `__repr__`, `__eq__` автоматически.
- Списки/словари — через `field(default_factory=list)`.
- `__post_init__` — проверки; `frozen=True` — неизменяемый и хешируемый; `order=True` — сравнения.
- `asdict`, `replace`, `User(**d)`.
'''),
    short=t(r'''
```py
from dataclasses import dataclass, field, asdict, replace

@dataclass(frozen=False, order=False)
class Order:
    id: int                                    # обязательное
    items: list = field(default_factory=list)  # не = []
    status: str = "new"                        # умолчание

    def __post_init__(self):                   # проверки
        if self.id <= 0: raise ValueError

asdict(o)              # {'id': 1, ...}
replace(o, status="paid")   # копия
Order(**d)             # из словаря
```
'''),
    quiz=[
        q('Что НЕ генерирует `@dataclass` по умолчанию?',
            ['`__init__`', '`__repr__`', '`__eq__`', '`__lt__`'],
            3, 'Сравнения `<` появляются только с `order=True`.'),
        q('Как задать поле-список со своим пустым списком у каждого объекта?',
            ['`items: list = []`', '`items: list = field(default_factory=list)`', '`items = list`', '`items: list = None`'],
            1, '`= []` dataclass запрещает.'),
        q('Что даёт `frozen=True`?',
            ['Быстрее работает', 'Объект нельзя менять, зато он хешируемый', 'Поля становятся приватными', 'Запрещает наследование'],
            1, 'Присваивание вызывает FrozenInstanceError.'),
    ],
),

# ---------- oop-pom ----------
'oop-pom': dict(
    full=t(r'''
## Зачем это нужно

В автотестах классы используют постоянно. Три самых частых шаблона:

- **Page Object** — класс на каждую страницу UI: селекторы и действия спрятаны внутри.
- **API-клиент** — класс, который знает базовый адрес, заголовки и эндпоинты.
- **Фабрика и подделки** — классы, которые создают тестовые данные и заменяют настоящие сервисы.

Здесь вместо настоящего браузера и сети — простые «фейковые» классы, но устройство такое же, как в Selenium, Playwright и requests.

## Page Object

```python
class FakeDriver:
    def __init__(self):
        self.actions = []

    def type(self, selector, text):
        self.actions.append(f"type {selector}={text}")

    def click(self, selector):
        self.actions.append(f"click {selector}")

class LoginPage:
    LOGIN = "#login"
    PASSWORD = "#password"
    SUBMIT = "button[type=submit]"

    def __init__(self, driver):
        self.driver = driver

    def login(self, user, password):
        self.driver.type(self.LOGIN, user)
        self.driver.type(self.PASSWORD, password)
        self.driver.click(self.SUBMIT)
        return self

d = FakeDriver()
LoginPage(d).login("anna", "123")
print(d.actions)
```

- `FakeDriver` записывает действия вместо настоящего браузера.
- Селекторы — **атрибуты класса** `LoginPage`: если вёрстка изменится, правим одно место.
- Драйвер передаётся в конструктор (композиция и внедрение зависимости).
- Тест пишет `LoginPage(driver).login("anna", "123")` — читается как сценарий, без селекторов.
- Вывод: `['type #login=anna', 'type #password=123', 'click button[type=submit]']`.

## Базовая страница

```python
class BasePage:
    url = "/"

    def open(self):
        return f"открыта {self.url}"

class CartPage(BasePage):
    url = "/cart"

class ProfilePage(BasePage):
    url = "/profile"

    def open(self):
        return super().open() + " (нужен вход)"

for page in [BasePage(), CartPage(), ProfilePage()]:
    print(page.open())
```

- Общие действия (открыть, дождаться, сделать скриншот) — в `BasePage`, страницы наследуют и переопределяют атрибут `url`.
- Вывод: `открыта /`, `открыта /cart`, `открыта /profile (нужен вход)`.

## API-клиент

```python
class ApiClient:
    def __init__(self, base_url, token=None):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def url(self, path):
        return f"{self.base_url}/{path.lstrip('/')}"

    def headers(self):
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

c = ApiClient("https://api.test/", token="t1")
print(c.url("/users/1"))
print(c.headers())
```

- `rstrip("/")` и `lstrip("/")` убирают лишние слеши, чтобы адрес не получился `https://api.test//users/1`.
- Заголовок авторизации добавляется, только если есть токен.
- В реальном клиенте методы `get_user(id)`, `create_user(data)` вызывают `requests` с этим адресом и заголовками.
- Вывод: `https://api.test/users/1`, `{'Content-Type': 'application/json', 'Authorization': 'Bearer t1'}`.

## Обёртка ответа с проверками

```python
class Response:
    def __init__(self, status, body):
        self.status = status
        self.body = body

    def assert_status(self, expected):
        assert self.status == expected, f"ожидали {expected}, получили {self.status}"
        return self

    def assert_has(self, key):
        assert key in self.body, f"нет поля {key}"
        return self

r = Response(200, {"id": 1})
r.assert_status(200).assert_has("id")
try:
    r.assert_status(404)
except AssertionError as e:
    print(e)
```

- Методы-проверки возвращают `self`, поэтому их можно цеплять.
- Понятные сообщения ошибок экономят время при разборе упавших тестов.
- Вывод: `ожидали 404, получили 200`.

## Фабрика тестовых данных

```python
class UserFactory:
    def __init__(self):
        self.counter = 0

    def create(self, **overrides):
        self.counter += 1
        n = self.counter
        user = {"id": n, "name": f"user_{n}", "active": True}
        user.update(overrides)
        return user

f = UserFactory()
print(f.create())
print(f.create(active=False))
```

- Каждый пользователь уникален благодаря счётчику, а `**overrides` позволяет поменять только нужные для теста поля.
- Вывод: `{'id': 1, 'name': 'user_1', 'active': True}`, `{'id': 2, 'name': 'user_2', 'active': False}`.

## Итог

- Page Object: селекторы — атрибуты класса, действия — методы, драйвер — в конструкторе.
- `BasePage` — общее поведение, страницы-потомки переопределяют детали.
- API-клиент хранит адрес и заголовки; ответ оборачивают методами-проверками.
- Фабрики и фейки — классы с состоянием для тестовых данных.
'''),
    short=t(r'''
```py
class LoginPage(BasePage):
    LOGIN = "#login"                  # селекторы
    def __init__(self, driver):
        self.driver = driver          # внедрение
    def login(self, user, pwd):
        self.driver.type(self.LOGIN, user)
        return self                   # цепочка

class ApiClient:
    def __init__(self, base_url, session):
        self.base_url = base_url.rstrip("/")
        self.session = session
    def get(self, path):
        return self.session.request("GET", self.base_url + path)
```
'''),
    quiz=[
        q('Где в Page Object принято хранить селекторы?',
            ['В тесте', 'В атрибутах класса страницы', 'В глобальных переменных', 'В драйвере'],
            1, 'Изменилась вёрстка — правим одно место.'),
        q('Зачем передавать драйвер в конструктор страницы?',
            ['Так быстрее', 'Чтобы использовать общий браузер и подменять его в тестах', 'Иначе SyntaxError', 'Чтобы наследовать драйвер'],
            1, 'Это композиция и внедрение зависимости.'),
        q('Зачем методам-проверкам возвращать `self`?',
            ['Для скорости', 'Чтобы цеплять проверки подряд', 'Иначе assert не работает', 'Так требует pytest'],
            1, '`r.assert_status(200).assert_has("id")`.'),
    ],
),

}
