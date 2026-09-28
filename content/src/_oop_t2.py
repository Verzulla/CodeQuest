"""Теория модуля «Наследование» темы «Классы».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- oop-m2-l1 ----------
'oop-m2-l1': dict(
    full=t(r'''
## Зачем это нужно

Часто классы похожи: обычный пользователь и администратор, кошка и собака, запрос и запрос с авторизацией. **Наследование** позволяет описать общее один раз в родительском классе, а в дочерних добавить только отличия. Во фреймворках для тестов наследование повсюду: `class TestLogin(BaseTest)`, `class LoginPage(BasePage)`.

## Термины

- **Родитель** (базовый класс, суперкласс) — класс, от которого наследуют.
- **Потомок** (дочерний класс, подкласс) — класс, который наследует.
- Потомок получает **все** атрибуты и методы родителя и может добавить свои или заменить родительские.

## Простое наследование

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def intro(self):
        return f"Я {self.name}"

class Cat(Animal):
    def meow(self):
        return "Мяу"

c = Cat("Мурка")
print(c.intro(), c.meow())
```

- `class Cat(Animal):` — в скобках указан родитель.
- У `Cat` нет своего `__init__` и `intro` — они взяты из `Animal`. Поэтому `Cat("Мурка")` вызывает `Animal.__init__`.
- `meow` есть только у `Cat`; у `Animal` его нет.
- Вывод: `Я Мурка Мяу`.

## Свой __init__ и super()

```python
class User:
    def __init__(self, name):
        self.name = name
        self.permissions = ["read"]

class Admin(User):
    def __init__(self, name, level):
        super().__init__(name)
        self.level = level
        self.permissions.append("delete")

a = Admin("Аня", 3)
print(a.name, a.level, a.permissions)
```

- У `Admin` свой `__init__` — он **заменяет** родительский. Родительский сам не вызовется!
- `super()` — «родительская часть» текущего объекта. `super().__init__(name)` запускает конструктор `User`, который создаёт `name` и `permissions`.
- После этого добавляем то, что есть только у админа.
- Если забыть `super().__init__`, у объекта не будет `name` и `permissions` → `AttributeError` при обращении.
- Вывод: `Аня 3 ['read', 'delete']`.

## Расширить метод родителя

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def yearly(self):
        return self.salary * 12

class Manager(Employee):
    def __init__(self, name, salary, bonus):
        super().__init__(name, salary)
        self.bonus = bonus

    def yearly(self):
        return super().yearly() + self.bonus

print(Employee("Аня", 100).yearly(), Manager("Боря", 100, 500).yearly())
```

- `Manager.yearly` **переопределяет** метод, но не копирует его код, а зовёт `super().yearly()` и добавляет бонус.
- Если в `Employee` поменяется формула, менеджер автоматически её получит.
- Вывод: `1200 1700`.

## Цепочка из нескольких уровней

```python
class A:
    def hello(self):
        return "A"

class B(A):
    def hello(self):
        return "B>" + super().hello()

class C(B):
    def hello(self):
        return "C>" + super().hello()

print(C().hello())
```

- `super()` в `C` ведёт к `B`, а `super()` в `B` — к `A`.
- Вывод: `C>B>A`.

## Все классы наследуют object

Если родитель не указан, класс неявно наследует встроенный `object`. Оттуда берутся «запасные» `__str__`, `__repr__`, `__eq__` и другие методы — поэтому их можно не писать.

## Итог

- `class Child(Parent):` — наследование, потомок получает всё от родителя.
- Свой `__init__` у потомка заменяет родительский — вызывай `super().__init__(...)`.
- `super().method()` — вызвать версию родителя и расширить её.
- Все классы в итоге наследуют `object`.
'''),
    short=t(r'''
```py
class User:
    def __init__(self, name):
        self.name = name

    def info(self):
        return self.name

class Admin(User):                  # наследование
    def __init__(self, name, level):
        super().__init__(name)      # конструктор родителя!
        self.level = level

    def info(self):                 # переопределение
        return super().info() + " (admin)"

Admin("Аня", 3).info()   # 'Аня (admin)'
```
'''),
    quiz=[
        q('Что будет, если в `__init__` потомка не вызвать `super().__init__()`?',
            ['Родительский вызовется сам', 'Атрибуты родителя не создадутся', 'SyntaxError', 'Ничего'],
            1, 'Свой `__init__` полностью заменяет родительский.'),
        q('Что вернёт `super().yearly()` внутри `Manager.yearly`?',
            ['Результат `Manager.yearly`', 'Результат `Employee.yearly` для этого объекта', 'Ошибку рекурсии', 'None'],
            1, 'super() — вызов версии родителя с тем же self.'),
        q('От какого класса наследуется класс без указания родителя?',
            ['Ни от какого', '`object`', '`type`', '`Base`'],
            1, 'Все классы в Python — потомки object.'),
    ],
),

# ---------- oop-override ----------
'oop-override': dict(
    full=t(r'''
## Зачем это нужно

Главная сила наследования в том, что родитель может описать **общий алгоритм**, а потомки — подменить отдельные шаги. Чтобы этим пользоваться, нужно понимать, как Python ищет метод, когда их несколько с одинаковым именем.

## Родитель вызывает метод потомка

```python
class Base:
    def hello(self):
        return "Base"

    def run(self):
        return "run: " + self.hello()

class Child(Base):
    def hello(self):
        return "Child"

print(Base().run())
print(Child().run())
```

- `run` определён только в `Base`. Но внутри он вызывает `self.hello()`.
- Для `Child()` объект `self` — это `Child`, поэтому Python находит `Child.hello`.
- Поиск метода всегда начинается с **настоящего класса объекта**, где бы ни был написан вызов.
- Вывод: `run: Base`, `run: Child`.

## Порядок поиска — MRO

```python
class A:
    def who(self):
        return "A"

class B(A):
    pass

class C(B):
    pass

print(C().who())
print([cls.__name__ for cls in C.__mro__])
```

- **MRO** (Method Resolution Order) — порядок, в котором Python ищет атрибут: сначала объект, потом класс, потом родители.
- `C.__mro__` — кортеж классов в этом порядке. У `C` и `B` нет `who`, он найден в `A`.
- Вывод: `A`, `['C', 'B', 'A', 'object']`.

## Атрибуты класса тоже переопределяются

```python
class Shape:
    name = "фигура"

    def area(self):
        return 0

    def describe(self):
        return f"{self.name}: площадь {self.area()}"

class Square(Shape):
    name = "квадрат"

    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

print(Shape().describe())
print(Square(3).describe())
```

- `self.name` ищется так же, как метод: у `Square` свой `name`.
- `describe` пишется один раз, а работает для любой фигуры.
- Вывод: `фигура: площадь 0`, `квадрат: площадь 9`.

## Множественное наследование

```python
class Loggable:
    def info(self):
        return "log"

class Savable:
    def info(self):
        return "save"

    def save(self):
        return "saved"

class Report(Loggable, Savable):
    pass

r = Report()
print(r.info(), r.save())
print([c.__name__ for c in Report.__mro__])
```

- У класса может быть несколько родителей. Метод ищется **слева направо**: сначала `Loggable`, потом `Savable`.
- `info` есть у обоих — выигрывает левый. `save` только у `Savable`.
- Вывод: `log saved`, `['Report', 'Loggable', 'Savable', 'object']`.

## Миксины

**Миксин** (mixin) — маленький класс с одной полезной способностью, который «подмешивают» к другим классам:

```python
class JsonMixin:
    def to_dict(self):
        return dict(vars(self))

class User(JsonMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

print(User("Аня", 30).to_dict())
```

- `JsonMixin` ничего не знает про `User` — он работает с любым `self`.
- `dict(vars(self))` — копия словаря атрибутов.
- Вывод: `{'name': 'Аня', 'age': 30}`.

## Переопределить и дополнить

```python
class Request:
    def headers(self):
        return {"Accept": "json"}

class AuthRequest(Request):
    def __init__(self, token):
        self.token = token

    def headers(self):
        h = super().headers()
        h["Authorization"] = f"Bearer {self.token}"
        return h

print(AuthRequest("abc").headers())
```

- Частый шаблон: взять результат родителя через `super()`, дополнить, вернуть.
- Вывод: `{'Accept': 'json', 'Authorization': 'Bearer abc'}`.

## Итог

- Метод ищется от настоящего класса объекта вверх по MRO: `Класс.__mro__`.
- Родитель может вызывать `self.метод()`, а потомок — подменить этот метод.
- При нескольких родителях — слева направо.
- Миксин — маленький класс-способность.
'''),
    short=t(r'''
```py
class Base:
    name = "base"
    def step(self): return "base"
    def run(self):  return self.step()   # вызовет версию потомка

class Child(Base):
    name = "child"                        # атрибуты тоже
    def step(self): return "child"

Child().run()                  # 'child'
Child.__mro__                  # (Child, Base, object)

class R(Loggable, Savable): …  # поиск слева направо
class JsonMixin:               # миксин
    def to_dict(self): return dict(vars(self))
```
'''),
    quiz=[
        q('`Base.run` вызывает `self.step()`. Чей `step` выполнится для объекта `Child`?',
            ['Base.step', 'Child.step', 'Оба', 'Ошибка'],
            1, 'Поиск начинается с класса объекта.'),
        q('В `class R(A, B)` оба родителя имеют метод `info`. Какой вызовется?',
            ['A.info', 'B.info', 'Оба по очереди', 'TypeError'],
            0, 'Родители просматриваются слева направо.'),
        q('Что показывает `Класс.__mro__`?',
            ['Список методов', 'Порядок поиска атрибутов', 'Список объектов', 'Имя модуля'],
            1, 'Method Resolution Order.'),
    ],
),

# ---------- oop-m2-l2 ----------
'oop-m2-l2': dict(
    full=t(r'''
## Зачем это нужно

**Полиморфизм** — возможность работать с разными объектами одинаково. Функции `notify_all` всё равно, email это или SMS, — она просто вызывает `send()`. Благодаря этому код легко расширять: добавил новый канал — ничего менять не надо.

## Утиная типизация

«Если оно ходит как утка и крякает как утка — это утка». Python не проверяет тип объекта, а просто вызывает нужный метод:

```python
class Email:
    def send(self, text):
        return f"email: {text}"

class Sms:
    def send(self, text):
        return f"sms: {text[:5]}"

class Push:
    def send(self, text):
        return f"push: {text.upper()}"

for channel in [Email(), Sms(), Push()]:
    print(channel.send("тест упал"))
```

- Три класса не связаны наследованием, но у всех есть `send`.
- Цикл одинаково вызывает `send` — и получает разное поведение.
- Вывод: `email: тест упал`, `sms: тест `, `push: ТЕСТ УПАЛ`.
- Если у объекта нет метода — `AttributeError` в момент вызова.

## Абстрактный класс

Иногда нужно **гарантировать**, что потомок реализует определённые методы. Для этого есть модуль `abc`:

```python
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, text):
        pass

    def notify(self, text):
        return "→ " + self.send(text)

class Email(Notifier):
    def send(self, text):
        return f"email: {text}"

class Broken(Notifier):
    pass

print(Email().notify("привет"))
for cls in [Notifier, Broken]:
    try:
        cls()
    except TypeError:
        print(cls.__name__, "нельзя создать")
```

- `class Notifier(ABC)` — наследуем от `ABC` (Abstract Base Class).
- `@abstractmethod` — декоратор: «потомок обязан это реализовать». Тело обычно пустое (`pass`).
- Объект абстрактного класса создать нельзя → `TypeError`. Потомок без реализации — тоже абстрактный.
- Неабстрактные методы (`notify`) работают как обычно и могут вызывать абстрактные.
- Вывод: `→ email: привет`, `Notifier нельзя создать`, `Broken нельзя создать`.

## Шаблонный метод

Родитель задаёт порядок шагов, потомки заполняют шаги:

```python
from abc import ABC, abstractmethod

class Check(ABC):
    def run(self):
        self.setup()
        ok = self.check()
        return "PASS" if ok else "FAIL"

    def setup(self):
        pass

    @abstractmethod
    def check(self):
        pass

class StatusCheck(Check):
    def check(self):
        return 200 == 200

print(StatusCheck().run())
```

- `run` — «шаблон»: последовательность шагов одна для всех проверок.
- `setup` — необязательный шаг с пустой реализацией, `check` — обязательный.
- Именно так устроены тестовые фреймворки: `setUp` → тест → `tearDown`.
- Вывод: `PASS`.

## Когда что выбирать

- Утиная типизация — проще и гибче, достаточно в большинстве случаев.
- ABC — когда пишешь базовый класс для других и хочешь, чтобы забытый метод обнаружился **сразу** при создании объекта, а не в момент вызова.

## Итог

- Полиморфизм: один вызов — разное поведение у разных классов.
- Утиная типизация: важен метод, а не тип.
- `ABC` + `@abstractmethod` — обязательные методы; абстрактный класс не создать.
- Шаблонный метод: родитель задаёт порядок, потомки — шаги.
'''),
    short=t(r'''
```py
for ch in [Email(), Sms()]:   # утиная типизация
    ch.send("x")              # важен метод, не тип

from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, text): pass     # потомок обязан
    def notify(self, text):        # обычный метод
        return self.send(text)

Notifier()      # TypeError: абстрактный
class Email(Notifier):
    def send(self, text): return text
```
'''),
    quiz=[
        q('Что будет при попытке создать объект абстрактного класса?',
            ['Создастся пустой', 'TypeError', 'AttributeError', 'Предупреждение'],
            1, 'Python не даст создать объект, пока есть нереализованные абстрактные методы.'),
        q('Что нужно, чтобы функция `notify_all(channels)` работала с объектом нового класса?',
            ['Наследовать от Email', 'Иметь метод `send`', 'Зарегистрировать класс', 'Использовать ABC'],
            1, 'Утиная типизация: достаточно нужного метода.'),
        q('Можно ли в абстрактном классе иметь обычные методы?',
            ['Нет', 'Да', 'Только static', 'Только в Python 2'],
            1, 'Они наследуются и могут вызывать абстрактные.'),
    ],
),

# ---------- oop-isinstance ----------
'oop-isinstance': dict(
    full=t(r'''
## Зачем это нужно

Иногда нужно узнать, какого типа объект: обработать строку иначе, чем список, отличить серверную ошибку от клиентской, проверить в тесте, что API вернул правильный тип. Для этого есть `isinstance`, `type` и `issubclass`.

## isinstance и type

```python
class Animal: pass
class Dog(Animal): pass

d = Dog()
print(isinstance(d, Dog), isinstance(d, Animal), isinstance(d, object))
print(type(d) is Dog, type(d) is Animal)
print(issubclass(Dog, Animal), issubclass(Animal, Dog))
```

- `isinstance(obj, Класс)` — `True`, если объект этого класса **или его потомка**.
- `type(obj)` — точный класс объекта. `type(d) is Animal` — `False`, хотя собака — животное.
- `issubclass(A, B)` — является ли класс `A` потомком `B` (сам себе тоже).
- `class Animal: pass` — пустой класс в одну строку; `pass` значит «ничего».
- Вывод: `True True True`, `True False`, `True False`.
- Почти всегда используют `isinstance`: он уважает наследование.

## Проверка нескольких типов

```python
values = [1, 2.5, "3", True, None, [4]]
for v in values:
    print(type(v).__name__, isinstance(v, (int, float)))
```

- Вторым аргументом можно передать **кортеж** классов: «хотя бы один из них».
- `type(v).__name__` — имя класса строкой.
- Внимание: `bool` — потомок `int`, поэтому `isinstance(True, int)` → `True`.
- Вывод: `int True`, `float True`, `str False`, `bool True`, `NoneType False`, `list False`.

Чтобы исключить `bool`:

```python
def only_numbers(values):
    return [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]

print(only_numbers([1, "2", 3.5, True, None]))
```

- Вывод: `[1, 3.5]`.

## Информация о классе

```python
class HttpError(Exception): pass
class NotFound(HttpError): pass

e = NotFound("нет страницы")
print(type(e).__name__, e.__class__.__name__)
print(NotFound.__bases__[0].__name__)
print(isinstance(e, Exception))
```

- `obj.__class__` — то же, что `type(obj)`.
- `Класс.__bases__` — кортеж непосредственных родителей.
- Вывод: `NotFound NotFound`, `HttpError`, `True`.

## Порядок проверок важен

```python
class ApiError(Exception): pass
class ClientError(ApiError): pass
class NotFound(ClientError): pass

def kind(error):
    if isinstance(error, NotFound):
        return "404"
    if isinstance(error, ClientError):
        return "4xx"
    return "другое"

print(kind(NotFound()), kind(ClientError()), kind(ApiError()))
```

- Сначала проверяем **более конкретный** класс: `NotFound` — это тоже `ClientError`, поэтому при обратном порядке мы бы никогда не дошли до `"404"`.
- Вывод: `404 4xx другое`.

## Рекурсия с isinstance

```python
def flatten(data):
    result = []
    for item in data:
        if isinstance(item, (list, tuple)):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

print(flatten([1, [2, (3, "ab")], [[4]]]))
```

- Если элемент — список или кортеж, разворачиваем его той же функцией; иначе добавляем как есть.
- Строка — тоже последовательность, но мы её не разворачиваем, потому что она не в кортеже типов.
- Вывод: `[1, 2, 3, 'ab', 4]`.

## Не злоупотребляй

Длинная цепочка `if isinstance(x, A) ... elif isinstance(x, B)` часто означает, что лучше дать классам общий метод и использовать полиморфизм.

## Итог

- `isinstance(obj, Cls)` / `isinstance(obj, (A, B))` — с учётом наследования.
- `type(obj) is Cls` — точный класс; `type(obj).__name__` — имя.
- `issubclass(A, B)`, `Cls.__bases__`, `Cls.__mro__`.
- `bool` — подкласс `int`. Конкретные классы проверяй раньше общих.
'''),
    short=t(r'''
```py
isinstance(d, Animal)           # с наследованием
isinstance(v, (int, float))     # любой из
type(d) is Dog                  # точный тип
type(d).__name__                # 'Dog'
issubclass(Dog, Animal)         # True
Dog.__bases__                   # (Animal,)
isinstance(True, int)           # True! bool ⊂ int
# сначала конкретный класс, потом общий
```
'''),
    quiz=[
        q('Что вернёт `isinstance(Dog(), Animal)`, если `Dog(Animal)`?',
            ['True', 'False', 'TypeError', 'None'],
            0, 'isinstance учитывает наследование.'),
        q('Что вернёт `type(Dog()) is Animal`?',
            ['True', 'False', 'Ошибка', 'Зависит от MRO'],
            1, 'type — точный класс, без родителей.'),
        q('Что вернёт `isinstance(True, int)`?',
            ['True', 'False', 'TypeError', 'None'],
            0, 'bool — подкласс int.'),
    ],
),

# ---------- oop-composition ----------
'oop-composition': dict(
    full=t(r'''
## Зачем это нужно

Наследование описывает отношение «**является**»: админ является пользователем. Но часто отношение другое — «**имеет**»: у машины есть двигатель, у заказа есть товары, у сервиса есть хранилище. Для этого один объект кладут внутрь другого — это **композиция**. Правило опытных разработчиков: «предпочитай композицию наследованию».

## Объект внутри объекта

```python
class Engine:
    def __init__(self, power):
        self.power = power

    def start(self):
        return f"двигатель {self.power} л.с. завёлся"

class Car:
    def __init__(self, model, power):
        self.model = model
        self.engine = Engine(power)

    def start(self):
        return f"{self.model}: {self.engine.start()}"

car = Car("Лада", 90)
print(car.start())
print(car.engine.power)
```

- `self.engine = Engine(power)` — атрибут машины хранит объект другого класса.
- `Car.start` **делегирует** работу: вызывает `self.engine.start()` и дополняет результат.
- `car.engine.power` — точки идут цепочкой: машина → двигатель → мощность.
- Вывод: `Лада: двигатель 90 л.с. завёлся`, `90`.

## Коллекция объектов

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

class Group:
    def __init__(self):
        self.students = []

    def add(self, student):
        self.students.append(student)

    def best(self):
        return max(self.students, key=lambda s: s.score).name

g = Group()
g.add(Student("Аня", 90))
g.add(Student("Боря", 95))
print(g.best(), len(g.students))
```

- Группа хранит список объектов `Student`.
- `max(..., key=lambda s: s.score)` — объект с наибольшим баллом, затем берём его имя.
- Вывод: `Боря 2`.

## Зависимость передаётся снаружи

```python
class RealApi:
    def get(self):
        return "данные с сервера"

class FakeApi:
    def get(self):
        return "тестовые данные"

class Service:
    def __init__(self, api):
        self.api = api

    def report(self):
        return "отчёт: " + self.api.get()

print(Service(RealApi()).report())
print(Service(FakeApi()).report())
```

- `Service` не создаёт API сам, а **получает** его в конструкторе. Это называется **внедрение зависимости** (dependency injection).
- В бою передаём настоящий API, в тестах — подделку (fake / mock). Код сервиса не меняется.
- Вывод: `отчёт: данные с сервера`, `отчёт: тестовые данные`.

## Почему не наследование

```python
class Order:
    def __init__(self):
        self.items = []

    def add(self, name):
        self.items.append(name)

    def count(self):
        return len(self.items)

o = Order()
o.add("чай")
print(o.count())
```

- Можно было бы написать `class Order(list)` — но тогда у заказа появились бы **все** методы списка (`sort`, `clear`, `insert`…), даже ненужные и опасные.
- С композицией снаружи виден только нужный интерфейс: `add` и `count`.
- Вывод: `1`.

## Итог

- «Является» → наследование, «имеет» → композиция.
- Внешний объект делегирует работу внутреннему: `self.engine.start()`.
- Зависимости лучше передавать в конструктор — так их легко подменить в тестах.
- Композиция открывает наружу только нужные методы.
'''),
    short=t(r'''
```py
class Car:
    def __init__(self, engine):     # зависимость снаружи
        self.engine = engine        # «имеет»

    def start(self):
        return self.engine.start()  # делегирование

Car(Engine(90))                     # в бою
Car(FakeEngine())                   # в тестах

class Order:                        # не class Order(list)
    def __init__(self):
        self.items = []
```
'''),
    quiz=[
        q('Какое отношение описывает композиция?',
            ['«является»', '«имеет»', '«равен»', '«наследует»'],
            1, 'Машина имеет двигатель.'),
        q('Зачем передавать зависимость в конструктор, а не создавать внутри?',
            ['Быстрее работает', 'Её легко подменить в тестах', 'Так требует Python', 'Экономит память'],
            1, 'Внедрение зависимости — основа тестируемого кода.'),
        q('Чем плох `class Order(list)` для заказа?',
            ['Не работает', 'Появляются все методы списка, даже ненужные', 'Нельзя добавить атрибуты', 'Медленно'],
            1, 'Наследование открывает весь интерфейс родителя.'),
    ],
),

}
