"""Подробная теория и «Проверь себя» для темы «ООП»."""
from ._lib import t

THEORY = {
"oop-m1-l1": {"full": t("""
    ## Зачем это нужно

    Пока программа маленькая, хватает переменных и функций. Но когда появляется «пользователь» со своими именем, почтой, ролью и действиями — удобнее собрать данные и поведение в одно целое. Класс описывает, **какими бывают** объекты, а объекты — это конкретные экземпляры. Почти всё в автотестах построено на классах: Page Object, API-клиенты, фикстуры, модели данных.

    ## Как это работает

    ```py
    class Dog:
        def __init__(self, name, age):
            self.name = name          # атрибуты объекта
            self.age = age

        def bark(self):               # метод
            return f"{self.name}: Гав!"

    rex = Dog("Рекс", 3)              # создание объекта
    ```

    - **Класс** — чертёж. **Объект** (экземпляр) — изделие по чертежу. Из одного класса — сколько угодно объектов.
    - `__init__` — **конструктор**: вызывается автоматически при создании и заполняет атрибуты.
    - `self` — ссылка на сам объект. Python подставляет её сам: `rex.bark()` — это `Dog.bark(rex)`.
    - **Атрибуты** — данные объекта (`rex.name`), **методы** — функции объекта (`rex.bark()`).

    У каждого объекта свои значения атрибутов, методы общие.

    ## Примеры

    ### Пример 1. Класс и два объекта

    ```python
    class Dog:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def bark(self):
            return f"{self.name}: Гав!"

    rex = Dog("Рекс", 3)
    sharik = Dog("Шарик", 5)
    print(rex.bark(), sharik.bark())
    print(rex.age + sharik.age)
    ```

    ### Пример 2. Методы меняют состояние

    ```python
    class Counter:
        def __init__(self):
            self.value = 0

        def inc(self, step=1):
            self.value += step
            return self

    c = Counter()
    c.inc().inc(5).inc()
    print(c.value)
    ```

    `return self` позволяет вызывать методы цепочкой.

    ### Пример 3. Проверки внутри методов

    ```python
    class BankAccount:
        def __init__(self, owner, balance=0):
            self.owner = owner
            self.balance = balance

        def withdraw(self, amount):
            if amount > self.balance:
                raise ValueError(f"Недостаточно средств: {self.balance} < {amount}")
            self.balance -= amount

    acc = BankAccount("Аня", 100)
    acc.withdraw(30)
    try:
        acc.withdraw(500)
    except ValueError as e:
        print("ошибка:", e)
    print("баланс:", acc.balance)
    ```

    ### Пример 4. Объекты — ссылки

    ```python
    class Box:
        def __init__(self):
            self.items = []

    a = Box()
    b = a              # второе имя того же объекта
    b.items.append(1)
    print(a.items, a is b)
    ```

    ## Частые ошибки

    **Забыли `self` в параметрах метода** — `TypeError: takes 0 positional arguments but 1 was given`.

    **Забыли `self.` при обращении к атрибуту** — `name` внутри метода это локальная переменная, а не `self.name`.

    **Вызов метода без скобок.** `rex.bark` — это сам метод, а не результат его вызова.

    ## Шпаргалка

    ```py
    class User:
        def __init__(self, name):     # конструктор
            self.name = name          # атрибут
        def hello(self):              # метод
            return f"Привет, {self.name}"

    u = User("Аня")                   # объект
    u.name, u.hello()
    ```
    """), "quiz": [
    {"q": "Что такое `self` в методе класса?",
     "options": ["Имя класса", "Ссылка на объект, у которого вызван метод", "Глобальная переменная", "Обязательное ключевое слово без смысла"], "answer": 1,
     "explain": "`obj.method()` превращается в `Class.method(obj)` — `self` и есть этот `obj`."},
    {"q": "Когда вызывается `__init__`?",
     "options": ["При объявлении класса", "При создании каждого нового объекта", "При удалении объекта", "Только вручную"], "answer": 1,
     "explain": "`__init__` автоматически вызывается при `ClassName(...)` и заполняет атрибуты нового объекта."},
    {"q": "Что выведет код?\n```py\nclass A:\n    def __init__(self):\n        self.x = 1\n\na = A(); b = A()\nb.x = 5\nprint(a.x)\n```",
     "options": ["`5`", "`1`", "Ошибка", "`None`"], "answer": 1,
     "explain": "У каждого объекта свои атрибуты. Изменение `b.x` не влияет на `a.x`."},
]},

"oop-m1-l2": {"full": t("""
    ## Зачем это нужно

    Иногда данные должны быть **общими** для всех объектов класса: счётчик созданных объектов, настройки по умолчанию, константы. А ещё объекты надо удобно выводить: вместо `<__main__.Bug object at 0x10a…>` видеть что-то осмысленное — это особенно ценно в логах и отчётах об упавших тестах.

    ## Как это работает

    ### Атрибуты класса и экземпляра

    ```py
    class Test:
        count = 0              # атрибут КЛАССА — один на всех

        def __init__(self, name):
            self.name = name   # атрибут ЭКЗЕМПЛЯРА — у каждого свой
            Test.count += 1
    ```

    Когда ты читаешь `obj.attr`, Python ищет сначала в объекте, потом в классе. А присваивание `obj.attr = ...` всегда создаёт атрибут **в объекте**.

    ### Ловушка изменяемого атрибута класса

    Список или словарь, объявленный в теле класса, — **один на все объекты**. `self.items.append(...)` изменит общий список. Изменяемые данные создавай в `__init__`.

    ### __str__ и __repr__

    - `__str__` — «человеческое» представление: используется в `print()` и `str()`.
    - `__repr__` — «техническое», однозначное: в отладчике, в интерактивной консоли, **внутри списков**. Хорошая практика — чтобы по `repr` можно было воссоздать объект.

    Если `__str__` не задан, используется `__repr__`.

    ## Примеры

    ### Пример 1. Общий счётчик

    ```python
    class Bug:
        next_id = 1

        def __init__(self, title):
            self.title = title
            self.id = Bug.next_id
            Bug.next_id += 1

    bugs = [Bug("не работает логин"), Bug("кнопка не видна"), Bug("опечатка")]
    for b in bugs:
        print(b.id, b.title)
    ```

    ### Пример 2. Ловушка общего списка

    ```python
    class BadCart:
        items = []
        def add(self, x):
            self.items.append(x)

    class GoodCart:
        def __init__(self):
            self.items = []
        def add(self, x):
            self.items.append(x)

    a, b = BadCart(), BadCart()
    a.add("яблоко")
    print("плохо:", b.items)

    a, b = GoodCart(), GoodCart()
    a.add("яблоко")
    print("хорошо:", b.items)
    ```

    ### Пример 3. str и repr

    ```python
    class Point:
        def __init__(self, x, y):
            self.x, self.y = x, y
        def __str__(self):
            return f"({self.x}, {self.y})"
        def __repr__(self):
            return f"Point({self.x}, {self.y})"

    p = Point(1, 2)
    print(p)
    print([p, Point(3, 4)])
    print(f"точка {p}, отладка {p!r}")
    ```

    ### Пример 4. Без __repr__ и с ним

    ```python
    class Raw:
        def __init__(self, v):
            self.v = v

    class Nice(Raw):
        def __repr__(self):
            return f"Nice(v={self.v!r})"

    print(Raw(1))
    print(Nice("abc"))
    ```

    ## Частые ошибки

    **`self.count += 1` вместо `Класс.count += 1`.** Создаётся атрибут в объекте, а общий счётчик не меняется.

    **Изменяемый атрибут класса** (`items = []` в теле класса).

    **`__str__` возвращает не строку** (например, число) — `TypeError`.

    ## Шпаргалка

    ```py
    class C:
        shared = 0              # общий для всех
        def __init__(self):
            self.own = []       # свой у каждого (изменяемое — только здесь!)
        def __str__(self):  return "для людей"
        def __repr__(self): return "C()"   # для отладки, в списках
    ```
    """), "quiz": [
    {"q": "Что выведет код?\n```py\nclass C:\n    n = 0\n    def __init__(self):\n        C.n += 1\n\nC(); C()\nprint(C.n)\n```",
     "options": ["`0`", "`1`", "`2`", "Ошибка"], "answer": 2,
     "explain": "`n` — атрибут класса, общий для всех объектов. Каждый конструктор увеличивает его на 1."},
    {"q": "Какой метод Python использует, когда печатает объект **внутри списка**: `print([obj])`?",
     "options": ["`__str__`", "`__repr__`", "`__init__`", "`__format__`"], "answer": 1,
     "explain": "Для элементов коллекций используется `__repr__`, даже если у объекта есть `__str__`."},
    {"q": "Почему `items = []` в теле класса — ловушка?",
     "options": ["Это синтаксическая ошибка", "Этот список один на все объекты класса", "Список нельзя хранить в классе", "Список станет неизменяемым"], "answer": 1,
     "explain": "Атрибут класса общий. Изменения через любой объект видны во всех. Создавай список в `__init__`."},
]},

"oop-m2-l1": {"full": t("""
    ## Зачем это нужно

    Администратор — это пользователь с дополнительными правами. Кнопка «Войти» и ссылка «Забыли пароль?» — это элементы страницы с общими свойствами. Наследование позволяет описать общее один раз в **родительском** классе, а в **дочерних** — только отличия. Меньше дублирования — меньше мест, где можно ошибиться.

    ## Как это работает

    ```py
    class Animal:                     # родитель (базовый класс)
        def __init__(self, name):
            self.name = name
        def speak(self):
            return "..."

    class Cat(Animal):                # потомок наследует всё от Animal
        def speak(self):              # и переопределяет метод
            return "Мяу"
    ```

    ### Поиск методов

    При вызове `obj.method()` Python ищет метод в классе объекта, потом в его родителе, потом в родителе родителя — и так вверх по цепочке (это называется MRO). Используется первый найденный.

    ### super()

    `super()` даёт доступ к методам родителя. Главное применение — расширить, а не заменить поведение:

    ```py
    class Lion(Cat):
        def __init__(self, name, pride):
            super().__init__(name)    # родитель заполнит name
            self.pride = pride        # а мы — своё
    ```

    Если дочерний `__init__` не вызовет `super().__init__`, атрибуты родителя не появятся.

    ### Проверки типов

    - `isinstance(obj, Class)` — учитывает наследование: лев — это и кот, и животное.
    - `issubclass(Child, Parent)` — связь между классами.

    ## Примеры

    ### Пример 1. Переопределение и общий метод

    ```python
    class Animal:
        def speak(self):
            return "..."
        def intro(self):
            return f"{type(self).__name__} говорит: {self.speak()}"

    class Cat(Animal):
        def speak(self):
            return "Мяу"

    class Dog(Animal):
        def speak(self):
            return "Гав"

    for a in [Animal(), Cat(), Dog()]:
        print(a.intro())
    ```

    `intro` написан один раз в родителе, но вызывает `self.speak()` — и у каждого потомка срабатывает его версия.

    ### Пример 2. super() в конструкторе

    ```python
    class User:
        def __init__(self, name):
            self.name = name
            self.role = "user"

    class Admin(User):
        def __init__(self, name, permissions):
            super().__init__(name)
            self.permissions = permissions
            self.role = "admin"

        def can(self, action):
            return action in self.permissions

    a = Admin("root", ["delete", "ban"])
    print(a.name, a.role, a.can("ban"), a.can("fly"))
    print(isinstance(a, User), isinstance(User("x"), Admin))
    ```

    ### Пример 3. Расширение метода родителя

    ```python
    class Report:
        def render(self):
            return "Отчёт о тестировании"

    class HtmlReport(Report):
        def render(self):
            return f"<h1>{super().render()}</h1>"

    print(HtmlReport().render())
    ```

    ### Пример 4. Цепочка вызовов через super

    ```python
    class A:
        def hello(self):
            return "A"
    class B(A):
        def hello(self):
            return super().hello() + "B"
    class C(B):
        def hello(self):
            return super().hello() + "C"

    print(C().hello())
    print([k.__name__ for k in C.__mro__])
    ```

    ## Частые ошибки

    **Не вызвали `super().__init__()`** — `AttributeError` при обращении к атрибутам родителя.

    **Присваивание до `super().__init__`.** Если родитель тоже задаёт `role`, он перезапишет значение потомка. Сначала `super()`, потом своё.

    **Наследование ради одного метода.** Если связь не «является» (админ **является** пользователем), подумай о композиции: объект просто хранит другой объект.

    ## Шпаргалка

    ```py
    class Child(Parent):
        def __init__(self, a, b):
            super().__init__(a)    # сначала родитель
            self.b = b             # потом своё
        def method(self):
            base = super().method()  # расширить поведение родителя
            return base + "..."

    isinstance(obj, Parent)        # учитывает наследование
    ```
    """), "quiz": [
    {"q": "Что вернёт `C().hello()`, если `A.hello` возвращает `\"A\"`, `B(A).hello` — `super().hello() + \"B\"`, `C(B).hello` — `super().hello() + \"C\"`?",
     "options": ["`\"C\"`", "`\"CBA\"`", "`\"ABC\"`", "`\"AC\"`"], "answer": 2,
     "explain": "C вызывает версию B, B — версию A. Возвращаясь по цепочке, получаем `\"A\" + \"B\" + \"C\"`."},
    {"q": "Что будет, если в `__init__` потомка не вызвать `super().__init__(name)`, а родитель задаёт `self.name`?",
     "options": ["Python вызовет его сам", "У объекта не будет атрибута `name`", "Ошибка при объявлении класса", "`name` станет `None`"], "answer": 1,
     "explain": "Переопределённый `__init__` полностью заменяет родительский. Без явного `super().__init__` код родителя не выполнится."},
    {"q": "`class Admin(User)`. Что вернёт `isinstance(Admin(...), User)`?",
     "options": ["`True`", "`False`", "Ошибка", "Зависит от атрибутов"], "answer": 0,
     "explain": "`isinstance` учитывает наследование: админ является пользователем."},
]},

"oop-m2-l2": {"full": t("""
    ## Зачем это нужно

    Драйверы Chrome и Firefox устроены совершенно по-разному, но тест вызывает у них одни и те же `open()` и `click()`. Способы уведомлений разные — email, SMS, Telegram, — а код рассылки один. Это **полиморфизм**: работа с разными объектами через общий интерфейс. **Абстрактные классы** задают этот интерфейс и не дают создать «недоделанный» объект.

    ## Как это работает

    ### Полиморфизм

    Функции важно не **кто** объект, а **что он умеет**. Если у всех объектов есть метод `send(text)`, функция просто вызывает `n.send(text)` — и каждый объект делает это по-своему. В Python это называют «утиной типизацией»: если крякает как утка — значит, утка.

    ### Абстрактный класс

    ```py
    from abc import ABC, abstractmethod

    class Notifier(ABC):
        @abstractmethod
        def send(self, text): ...
    ```

    - Создать объект абстрактного класса нельзя — `TypeError`.
    - Потомок обязан реализовать **все** абстрактные методы, иначе его тоже нельзя создать.
    - В абстрактном классе могут быть и обычные методы с общей логикой.

    ### Шаблонный метод

    Общий алгоритм — в базовом классе, изменяемые шаги — абстрактные, их реализуют потомки. Так устроены многие фреймворки.

    ## Примеры

    ### Пример 1. Полиморфизм без наследования

    ```python
    class Chrome:
        def open(self, url):
            return f"Chrome открыл {url}"

    class Firefox:
        def open(self, url):
            return f"Firefox открыл {url}"

    def smoke_test(driver):
        return driver.open("/login")

    for d in [Chrome(), Firefox()]:
        print(smoke_test(d))
    ```

    ### Пример 2. Абстрактный класс не создать

    ```python
    from abc import ABC, abstractmethod

    class Notifier(ABC):
        @abstractmethod
        def send(self, text): ...

    class EmailNotifier(Notifier):
        def send(self, text):
            return f"email: {text}"

    class BrokenNotifier(Notifier):
        pass                          # забыли реализовать send

    for cls in [Notifier, EmailNotifier, BrokenNotifier]:
        try:
            obj = cls()
            print(cls.__name__, "->", obj.send("привет"))
        except TypeError as e:
            print(cls.__name__, "-> нельзя создать:", e)
    ```

    ### Пример 3. Шаблонный метод

    ```python
    from abc import ABC, abstractmethod

    class Check(ABC):
        def run(self, value):
            status = "PASS" if self.check(value) else "FAIL"
            return f"{type(self).__name__}({value!r}): {status}"

        @abstractmethod
        def check(self, value): ...

    class NotEmpty(Check):
        def check(self, value):
            return value != ""

    class IsPositive(Check):
        def check(self, value):
            return value > 0

    for c, v in [(NotEmpty(), "abc"), (NotEmpty(), ""), (IsPositive(), 5), (IsPositive(), -1)]:
        print(c.run(v))
    ```

    ### Пример 4. Рассылка по всем каналам

    ```python
    class Email:
        def send(self, t): return f"✉️ {t}"
    class Sms:
        def send(self, t): return f"📱 {t}"
    class Telegram:
        def send(self, t): return f"✈️ {t}"

    def notify_all(channels, text):
        return [c.send(text) for c in channels]

    print(notify_all([Email(), Sms(), Telegram()], "сборка упала"))
    ```

    ## Частые ошибки

    **Проверки `if type(x) == Chrome: ... elif ...`** вместо полиморфизма — каждый новый класс требует правки этой функции.

    **Забыли `ABC` в родителях** — тогда `@abstractmethod` ничего не запрещает.

    **Разные сигнатуры** одноимённых методов у потомков — полиморфный вызов сломается.

    ## Шпаргалка

    ```py
    from abc import ABC, abstractmethod

    class Base(ABC):
        def template(self):           # общий алгоритм
            return self.step()
        @abstractmethod
        def step(self): ...           # потомок обязан реализовать

    for obj in objects:
        obj.step()                    # полиморфизм
    ```
    """), "quiz": [
    {"q": "Что произойдёт при `Notifier()`, если `Notifier(ABC)` содержит абстрактный метод `send`?",
     "options": ["Создастся объект без метода send", "`TypeError`: нельзя создать экземпляр абстрактного класса", "Метод send вернёт None", "Ничего особенного"], "answer": 1,
     "explain": "Абстрактный класс с нереализованными абстрактными методами нельзя инстанцировать."},
    {"q": "Что такое полиморфизм?",
     "options": ["Наличие нескольких конструкторов", "Возможность работать с разными объектами через одинаковый интерфейс", "Наследование от нескольких классов", "Копирование объектов"], "answer": 1,
     "explain": "Код вызывает общий метод, а конкретный объект сам решает, как его выполнить."},
    {"q": "Потомок абстрактного класса не реализовал абстрактный метод. Можно ли создать объект потомка?",
     "options": ["Да", "Нет, будет `TypeError`", "Да, но метод вернёт ошибку при вызове", "Только через `super()`"], "answer": 1,
     "explain": "Пока реализованы не все абстрактные методы, потомок тоже считается абстрактным."},
]},

"oop-m3-l1": {"full": t("""
    ## Зачем это нужно

    Почему `len(list)` работает, а `len(мой_объект)` — нет? Почему `a == b` для двух одинаковых пользователей даёт `False`? Магические (dunder, от *double underscore*) методы позволяют твоим объектам работать со встроенными операторами и функциями Python так же естественно, как списки и числа.

    ## Как это работает

    Python переводит операции в вызовы специальных методов:

    - `a == b` → `a.__eq__(b)`
    - `a < b` → `a.__lt__(b)` (и тогда работает `sorted`)
    - `a + b` → `a.__add__(b)`
    - `len(a)` → `a.__len__()`
    - `x in a` → `a.__contains__(x)`
    - `a[i]` → `a.__getitem__(i)`
    - `for x in a` → `a.__iter__()`
    - `str(a)` / `repr(a)` → `__str__` / `__repr__`

    ### Равенство по умолчанию

    Без `__eq__` объекты равны, только если это **один и тот же** объект (`a is b`). Два пользователя с одинаковыми полями — разные объекты.

    ### Сравнение и сортировка

    Для `sorted` и `min`/`max` достаточно `__lt__`. Остальные операции сравнения можно получить декоратором `functools.total_ordering`.

    ## Примеры

    ### Пример 1. Равенство

    ```python
    class User:
        def __init__(self, email):
            self.email = email

    class UserEq(User):
        def __eq__(self, other):
            return isinstance(other, User) and self.email == other.email

    print(User("a@b.ru") == User("a@b.ru"))
    print(UserEq("a@b.ru") == UserEq("a@b.ru"))
    ```

    ### Пример 2. Сложение и сравнение

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

    total = Money(100) + Money(50) + Money(25)
    print(total, total == Money(175))
    ```

    ### Пример 3. Правильная сортировка версий

    ```python
    class Version:
        def __init__(self, text):
            self.text = text
            self.parts = tuple(int(p) for p in text.split("."))
        def __lt__(self, other):
            return self.parts < other.parts
        def __repr__(self):
            return self.text

    raw = ["1.10.0", "1.9.2", "2.0.0", "1.2.10"]
    print(sorted(raw))                        # как строки — неверно
    print(sorted(Version(v) for v in raw))    # как версии — верно
    ```

    ### Пример 4. Объект-коллекция

    ```python
    class TestSuite:
        def __init__(self, name):
            self.name = name
            self.tests = []
        def add(self, test):
            self.tests.append(test)
        def __len__(self):
            return len(self.tests)
        def __contains__(self, test):
            return test in self.tests
        def __iter__(self):
            return iter(self.tests)
        def __getitem__(self, i):
            return self.tests[i]

    s = TestSuite("smoke")
    for t in ["login", "search", "logout"]:
        s.add(t)
    print(len(s), "search" in s, s[0], s[-1])
    print([t.upper() for t in s])
    ```

    ## Частые ошибки

    **`__eq__` без проверки типа** — сравнение с объектом другого класса упадёт с `AttributeError`.

    **`__add__` изменяет `self`** вместо создания нового объекта — `a + b` неожиданно меняет `a`.

    **Сравнение версий строками.** `"1.10" < "1.9"` — `True`, потому что символ `1` меньше `9`.

    ## Шпаргалка

    ```py
    __eq__(self, o)       # ==
    __lt__(self, o)       # <, sorted
    __add__(self, o)      # +  (возвращай НОВЫЙ объект)
    __len__(self)         # len()
    __contains__(self, x) # in
    __getitem__(self, i)  # obj[i]
    __iter__(self)        # for
    ```
    """), "quiz": [
    {"q": "Что вернёт `P(1) == P(1)` для класса `P` без метода `__eq__`?",
     "options": ["`True`", "`False`", "Ошибка", "`None`"], "answer": 1,
     "explain": "Без `__eq__` сравнивается идентичность объектов. Это два разных объекта, поэтому `False`."},
    {"q": "Какой метод нужен, чтобы `sorted()` работал со списком твоих объектов?",
     "options": ["`__eq__`", "`__lt__`", "`__len__`", "`__sort__`"], "answer": 1,
     "explain": "Сортировка сравнивает элементы оператором `<`, то есть вызывает `__lt__`."},
    {"q": "Почему `sorted([\"1.10\", \"1.9\"])` даёт `['1.10', '1.9']`?",
     "options": ["Так правильно по смыслу", "Строки сравниваются посимвольно: `'1' < '9'`", "Ошибка Python", "Сортировка по длине"], "answer": 1,
     "explain": "Строки сравниваются по символам, а не как числа. Поэтому версии разбирают на кортеж чисел."},
]},

"oop-m3-l2": {"full": t("""
    ## Зачем это нужно

    Три инструмента, которые делают классы удобнее:
    - `@property` — атрибут с проверкой или вычислением, снаружи выглядит как обычное поле;
    - `@classmethod` и `@staticmethod` — альтернативные конструкторы и вспомогательные функции внутри класса;
    - `@dataclass` — классы для хранения данных без ручного написания `__init__`, `__repr__`, `__eq__`. В тестах это модели ответов API, тестовые данные, результаты.

    ## Как это работает

    ### @property

    ```py
    class Product:
        @property
        def price(self):              # чтение: p.price
            return self._price

        @price.setter
        def price(self, value):       # запись: p.price = 10
            if value < 0:
                raise ValueError("цена < 0")
            self._price = value
    ```

    Значение хранится в «приватном» `_price` (подчёркивание — договорённость «не трогай снаружи»). Присваивание в `__init__` (`self.price = price`) тоже проходит через setter.

    ### @classmethod и @staticmethod

    - `@classmethod` получает первым аргументом **класс** (`cls`). Типичное применение — альтернативный конструктор: `User.from_string("Аня,a@b.ru")`. Работает правильно и для наследников.
    - `@staticmethod` не получает ни `self`, ни `cls` — это обычная функция, которая логически относится к классу.

    ### @dataclass

    ```py
    from dataclasses import dataclass, field

    @dataclass
    class TestResult:
        name: str
        passed: bool
        duration: float = 0.0
        tags: list = field(default_factory=list)   # изменяемое значение по умолчанию
    ```

    Автоматически создаются `__init__`, `__repr__`, `__eq__`. `frozen=True` делает объект неизменяемым, `order=True` добавляет сравнение.

    ## Примеры

    ### Пример 1. property с проверкой и вычислением

    ```python
    class Temperature:
        def __init__(self, celsius):
            self.celsius = celsius

        @property
        def fahrenheit(self):
            return self.celsius * 9 / 5 + 32

        @fahrenheit.setter
        def fahrenheit(self, value):
            self.celsius = (value - 32) * 5 / 9

    t = Temperature(100)
    print(t.fahrenheit)
    t.fahrenheit = 32
    print(t.celsius)
    ```

    ### Пример 2. Защита от некорректных значений

    ```python
    class Product:
        def __init__(self, name, price):
            self.name = name
            self.price = price

        @property
        def price(self):
            return self._price

        @price.setter
        def price(self, value):
            if value < 0:
                raise ValueError(f"Цена не может быть отрицательной: {value}")
            self._price = value

    p = Product("чай", 100)
    try:
        p.price = -5
    except ValueError as e:
        print(e)
    print(p.price)
    ```

    ### Пример 3. classmethod и staticmethod

    ```python
    class User:
        def __init__(self, name, email):
            self.name, self.email = name, email

        @classmethod
        def from_string(cls, text):
            name, email = text.split(",")
            return cls(name.strip(), email.strip())

        @staticmethod
        def is_valid_email(email):
            return "@" in email and "." in email.split("@")[-1]

        def __repr__(self):
            return f"User({self.name!r}, {self.email!r})"

    print(User.from_string("Аня, anna@mail.ru"))
    print(User.is_valid_email("a@b.ru"), User.is_valid_email("abc"))
    ```

    ### Пример 4. dataclass

    ```python
    from dataclasses import dataclass, field

    @dataclass
    class TestResult:
        name: str
        passed: bool
        duration: float = 0.0
        tags: list = field(default_factory=list)

        def status(self):
            return f"{'✅' if self.passed else '❌'} {self.name} ({self.duration:.1f} с)"

    results = [TestResult("login", True, 1.2), TestResult("pay", False, 3.4, ["smoke"])]
    for r in results:
        print(r.status())
    print(results[1])
    print(TestResult("x", True) == TestResult("x", True))
    ```

    ## Частые ошибки

    **Рекурсия в property.** `self.price = value` внутри setter для `price` вызывает сам setter бесконечно. Храни в `self._price`.

    **`tags: list = []` в dataclass** — `ValueError`. Изменяемые значения по умолчанию — через `field(default_factory=list)`.

    **`@staticmethod` там, где нужен `cls`.** Альтернативный конструктор должен быть `@classmethod`, иначе для наследника создастся объект родителя.

    ## Шпаргалка

    ```py
    @property
    def x(self): return self._x
    @x.setter
    def x(self, v): self._x = v

    @classmethod
    def from_x(cls, ...): return cls(...)
    @staticmethod
    def helper(...): ...

    @dataclass
    class D:
        a: int
        b: list = field(default_factory=list)
    ```
    """), "quiz": [
    {"q": "Почему в setter свойства `price` значение сохраняют в `self._price`, а не в `self.price`?",
     "options": ["Так быстрее", "Присваивание `self.price` снова вызовет setter — бесконечная рекурсия", "Это требование dataclass", "Без разницы"], "answer": 1,
     "explain": "`self.price = ...` — это вызов того же setter. Поэтому реальное значение хранят под другим именем."},
    {"q": "Что получает первым аргументом метод с `@classmethod`?",
     "options": ["Объект (`self`)", "Класс (`cls`)", "Ничего", "Родительский класс"], "answer": 1,
     "explain": "`@classmethod` получает класс, поэтому может создавать объекты: `return cls(...)`."},
    {"q": "Что автоматически генерирует `@dataclass`?",
     "options": ["Только `__init__`", "`__init__`, `__repr__` и `__eq__`", "Только `__repr__`", "Методы сортировки всегда"], "answer": 1,
     "explain": "По умолчанию — конструктор, представление и сравнение на равенство. Сортировку добавляет `order=True`."},
]},
}
