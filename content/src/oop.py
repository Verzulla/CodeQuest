"""Тема «ООП»."""
from ._lib import t, cod, lesson, module, out, topic

P = "oop"

m1 = module(f"{P}-m1", "Классы и объекты", "🧱", "class, __init__, атрибуты и методы",
    lesson(f"{P}-m1-l1", "Первый класс", """
        # Класс — чертёж, объект — изделие

        ```
        class Dog:
            def __init__(self, name, age):
                self.name = name        # атрибуты объекта
                self.age = age

            def bark(self):             # метод
                return f"{self.name}: Гав!"

        rex = Dog("Рекс", 3)            # создаём объект (экземпляр)
        print(rex.name)                 # Рекс
        print(rex.bark())               # Рекс: Гав!
        ```

        - `__init__` — **конструктор**, вызывается при создании объекта.
        - `self` — ссылка на сам объект. Python передаёт её автоматически: `rex.bark()` ≈ `Dog.bark(rex)`.
        - Каждый объект хранит **свои** значения атрибутов.
        """,
        out(f"{P}-m1-l1-e1", "Что выведет программа?", """
            class Dog:
                def __init__(self, name):
                    self.name = name
                def bark(self):
                    return self.name + ": Гав!"

            a = Dog("Рекс")
            b = Dog("Шарик")
            print(a.bark())
            print(b.name)
            """),
        out(f"{P}-m1-l1-e2", "Что выведет программа? Методы могут менять состояние объекта.", """
            class Counter:
                def __init__(self):
                    self.value = 0
                def inc(self, step=1):
                    self.value += step

            c = Counter()
            c.inc()
            c.inc(5)
            print(c.value)
            """),
        out(f"{P}-m1-l1-e3", "Что выведет программа?", """
            class Box:
                def __init__(self, items):
                    self.items = items

            a = Box([1])
            b = a
            b.items.append(2)
            print(a.items)
            print(a is b)
            """, hint="`b = a` не копирует объект — это второе имя для того же объекта."),
        cod(f"{P}-m1-l1-e4", t("""
            Создай класс `User` — пользователь с именем и почтой.

            - Конструктор принимает два аргумента: `name` и `email`.
            - Сохраняет их в атрибуты объекта `self.name` и `self.email`.

            Пример:
            ```
            u = User("Аня", "anna@mail.ru")
            u.name    # → "Аня"
            u.email   # → "anna@mail.ru"
            ```
            """),
            "",
            """
            def test_user():
                u = User("Аня", "anna@mail.ru")
                assert u.name == "Аня" and u.email == "anna@mail.ru", "Атрибуты name и email должны сохраняться из конструктора"
            """,
            """
            class User:
                def __init__(self, name, email):
                    self.name = name
                    self.email = email
            """,
            hint="`def __init__(self, name, email):` и внутри `self.name = name`…"),
        cod(f"{P}-m1-l1-e5", t("""
            Допиши класс `Rectangle` — прямоугольник. Конструктор уже есть, добавь два метода:

            - `area()` — возвращает площадь: ширина × высота;
            - `perimeter()` — возвращает периметр: 2 × (ширина + высота).

            Пример:
            ```
            r = Rectangle(3, 4)
            r.area()        # → 12
            r.perimeter()   # → 14
            ```
            """),
            """
            class Rectangle:
                def __init__(self, width, height):
                    self.width = width
                    self.height = height
            """,
            """
            def test_area():
                assert Rectangle(3, 4).area() == 12, "Площадь 3x4 = 12"

            def test_perimeter():
                assert Rectangle(3, 4).perimeter() == 14, "Периметр 3x4 = 14"
            """,
            """
            class Rectangle:
                def __init__(self, width, height):
                    self.width = width
                    self.height = height

                def area(self):
                    return self.width * self.height

                def perimeter(self):
                    return 2 * (self.width + self.height)
            """),
        cod(f"{P}-m1-l1-e6", t("""
            Создай класс `BankAccount` — банковский счёт.

            **Конструктор** `BankAccount(owner, balance=0)`: сохраняет владельца в `self.owner` и начальный баланс в `self.balance` (по умолчанию 0).

            **Методы:**
            - `deposit(amount)` — пополнить: увеличивает `balance` на `amount`;
            - `withdraw(amount)` — снять: уменьшает `balance` на `amount`. Если денег не хватает (`amount` больше баланса) — бросает `ValueError`, а баланс **остаётся прежним**.

            Пример:
            ```
            acc = BankAccount("Аня", 50)
            acc.withdraw(20)    # balance → 30
            acc.deposit(100)    # balance → 130
            acc.withdraw(500)   # ValueError, balance по-прежнему 130
            ```
            Бросить исключение: `raise ValueError("Недостаточно средств")`.
            """),
            """
            class BankAccount:
                pass
            """,
            """
            def test_deposit():
                acc = BankAccount("Аня")
                acc.deposit(100)
                assert acc.balance == 100, "После deposit(100) баланс 100"

            def test_withdraw():
                acc = BankAccount("Аня", 50)
                acc.withdraw(20)
                assert acc.balance == 30, "50 - 20 = 30"

            def test_not_enough():
                acc = BankAccount("Аня", 10)
                try:
                    acc.withdraw(100)
                except ValueError:
                    pass
                else:
                    assert False, "При нехватке денег нужен ValueError"
                assert acc.balance == 10, "Баланс не должен меняться при ошибке"
            """,
            """
            class BankAccount:
                def __init__(self, owner, balance=0):
                    self.owner = owner
                    self.balance = balance

                def deposit(self, amount):
                    self.balance += amount

                def withdraw(self, amount):
                    if amount > self.balance:
                        raise ValueError("Недостаточно средств")
                    self.balance -= amount
            """,
            hint="`raise ValueError(\"...\")` — бросить исключение. Проверку делай до изменения баланса.", xp=20),
    ),
    lesson(f"{P}-m1-l2", "Атрибуты класса и __str__", """
        # Атрибуты класса

        Атрибут, объявленный прямо в теле класса, **общий** для всех объектов:

        ```
        class Test:
            count = 0                  # атрибут класса

            def __init__(self, name):
                self.name = name       # атрибут экземпляра
                Test.count += 1
        ```

        # Как объект выглядит при печати

        - `__str__` — «красивое» представление для людей, его использует `print` и `str()`.
        - `__repr__` — однозначное представление для разработчиков (в отладчике, в списке).

        ```
        class Point:
            def __init__(self, x, y):
                self.x, self.y = x, y
            def __str__(self):
                return f"({self.x}, {self.y})"
            def __repr__(self):
                return f"Point({self.x}, {self.y})"

        print(Point(1, 2))      # (1, 2)
        print([Point(1, 2)])    # [Point(1, 2)] — в списке используется repr
        ```
        """,
        out(f"{P}-m1-l2-e1", "Что выведет программа?", """
            class Test:
                count = 0
                def __init__(self):
                    Test.count += 1

            Test(); Test(); Test()
            print(Test.count)
            """),
        out(f"{P}-m1-l2-e2", "Что выведет программа?", """
            class Point:
                def __init__(self, x, y):
                    self.x, self.y = x, y
                def __str__(self):
                    return f"({self.x}, {self.y})"
                def __repr__(self):
                    return f"Point({self.x}, {self.y})"

            p = Point(1, 2)
            print(p)
            print([p])
            """),
        out(f"{P}-m1-l2-e3", "Ловушка: изменяемый атрибут класса. Что выведет программа?", """
            class Cart:
                items = []
                def add(self, x):
                    self.items.append(x)

            a = Cart()
            b = Cart()
            a.add("яблоко")
            print(b.items)
            """, hint="Список объявлен в классе — он один на всех. Правильно создавать его в __init__."),
        cod(f"{P}-m1-l2-e4", t("""
            Добавь в класс `Book` метод `__str__`, чтобы книга красиво печаталась.

            `__str__` должен возвращать строку в формате: название в кавычках-«ёлочках», пробел, длинное тире, пробел, автор.

            Пример:
            ```
            print(Book("Дюна", "Герберт"))
            ```
            Вывод:
            ```
            «Дюна» — Герберт
            ```
            Символы `«`, `»` и `—` можно скопировать прямо отсюда.
            """),
            """
            class Book:
                def __init__(self, title, author):
                    self.title = title
                    self.author = author
            """,
            """
            def test_str():
                assert str(Book("Дюна", "Герберт")) == "«Дюна» — Герберт", f"Получено {str(Book('Дюна', 'Герберт'))!r}"
            """,
            """
            class Book:
                def __init__(self, title, author):
                    self.title = title
                    self.author = author

                def __str__(self):
                    return f"«{self.title}» — {self.author}"
            """),
        cod(f"{P}-m1-l2-e5", t("""
            Допиши класс `Bug`, чтобы каждый новый баг получал уникальный номер.

            - Конструктор `Bug(title)` сохраняет название в `self.title`.
            - Каждому созданному багу присваивается номер `self.id`: первому — 1, второму — 2, третьему — 3 и т. д.
            - Счётчик следующего номера хранится в **атрибуте класса** `Bug.next_id` (он уже есть в заготовке) — он общий для всех багов.

            Пример:
            ```
            a = Bug("не работает логин")
            b = Bug("кнопка не видна")
            a.id   # → 1
            b.id   # → 2
            ```
            """),
            """
            class Bug:
                next_id = 1
            """,
            """
            def test_ids():
                Bug.next_id = 1
                a, b, c = Bug("a"), Bug("b"), Bug("c")
                assert (a.id, b.id, c.id) == (1, 2, 3), f"Получены id {(a.id, b.id, c.id)}"
                assert a.title == "a", "title должен сохраняться"
            """,
            """
            class Bug:
                next_id = 1

                def __init__(self, title):
                    self.title = title
                    self.id = Bug.next_id
                    Bug.next_id += 1
            """,
            hint="В `__init__`: `self.id = Bug.next_id`, затем `Bug.next_id += 1`."),
        cod(f"{P}-m1-l2-e6", t("""
            Исправь баг в классе `Cart` (корзина покупок).

            Сейчас список `items` объявлен прямо в теле класса, поэтому он **один на все корзины**: товар, добавленный в одну корзину, появляется во всех.

            Нужно, чтобы у каждой корзины был **свой** список:
            ```
            a, b = Cart(), Cart()
            a.add("яблоко")
            a.items   # → ["яблоко"]
            b.items   # → []
            ```
            Метод `add(x)` должен остаться. Создавай список в конструкторе `__init__`.
            """),
            """
            class Cart:
                items = []

                def add(self, x):
                    self.items.append(x)
            """,
            """
            def test_separate():
                a, b = Cart(), Cart()
                a.add("яблоко")
                assert b.items == [], "У корзины b не должно быть чужих товаров"
                assert a.items == ["яблоко"], "У корзины a должно быть яблоко"
            """,
            """
            class Cart:
                def __init__(self):
                    self.items = []

                def add(self, x):
                    self.items.append(x)
            """,
            hint="Создавай список в `__init__`: `self.items = []`."),
    ),
)

m2 = module(f"{P}-m2", "Наследование", "🌳", "super(), полиморфизм и абстрактные классы",
    lesson(f"{P}-m2-l1", "Наследование и super()", """
        # Наследование

        Дочерний класс получает всё от родителя и может добавить или изменить поведение:

        ```
        class Animal:
            def __init__(self, name):
                self.name = name
            def speak(self):
                return "..."

        class Cat(Animal):              # Cat наследует Animal
            def speak(self):            # переопределяем метод
                return "Мяу"

        class Lion(Cat):
            def __init__(self, name, pride):
                super().__init__(name)  # вызываем конструктор родителя
                self.pride = pride
        ```

        - `super()` — доступ к методам родителя.
        - `isinstance(obj, Class)` учитывает наследование: лев — это тоже кот.
        - Поиск метода идёт от класса объекта вверх по цепочке родителей.
        """,
        out(f"{P}-m2-l1-e1", "Что выведет программа?", """
            class Animal:
                def speak(self):
                    return "..."
                def intro(self):
                    return "Я говорю: " + self.speak()

            class Cat(Animal):
                def speak(self):
                    return "Мяу"

            print(Animal().intro())
            print(Cat().intro())
            """, hint="intro вызывает self.speak() — а self у кота свой метод speak."),
        out(f"{P}-m2-l1-e2", "Что выведет программа?", """
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
            """),
        out(f"{P}-m2-l1-e3", "Что выведет программа?", """
            class Animal: pass
            class Cat(Animal): pass
            class Dog(Animal): pass

            c = Cat()
            print(isinstance(c, Cat), isinstance(c, Animal), isinstance(c, Dog))
            print(issubclass(Dog, Animal))
            """),
        cod(f"{P}-m2-l1-e4", t("""
            Создай класс `Admin` — наследник класса `User` из заготовки.

            - Конструктор: `Admin(name, permissions)`, где `permissions` — список разрешённых действий.
            - Имя должен сохранять конструктор родителя — вызови `super().__init__(name)`.
            - Список разрешений сохрани в `self.permissions`.

            Пример:
            ```
            a = Admin("root", ["delete"])
            a.name                # → "root"
            a.permissions         # → ["delete"]
            isinstance(a, User)   # → True — админ тоже пользователь
            ```
            """),
            """
            class User:
                def __init__(self, name):
                    self.name = name
                    self.role = "user"

            # напиши класс Admin
            """,
            """
            def test_admin():
                a = Admin("root", ["delete"])
                assert isinstance(a, User), "Admin должен наследовать User"
                assert a.name == "root" and a.permissions == ["delete"], "name и permissions должны сохраняться"
            """,
            """
            class User:
                def __init__(self, name):
                    self.name = name
                    self.role = "user"

            class Admin(User):
                def __init__(self, name, permissions):
                    super().__init__(name)
                    self.permissions = permissions
            """),
        cod(f"{P}-m2-l1-e5", t("""
            Доработай класс `Admin` из заготовки.

            1. У обычного `User` поле `role` равно `"user"`. У админа оно должно быть `"admin"`: присвой новое значение в конструкторе `Admin` **после** вызова `super().__init__`.
            2. Добавь метод `can(action)` — возвращает `True`, если действие `action` есть в списке `permissions`, иначе `False`.

            Пример:
            ```
            a = Admin("root", ["delete", "ban"])
            a.role            # → "admin"
            a.can("ban")      # → True
            a.can("fly")      # → False
            User("anna").role # → "user"   у обычных пользователей не меняется
            ```
            """),
            """
            class User:
                def __init__(self, name):
                    self.name = name
                    self.role = "user"

            class Admin(User):
                def __init__(self, name, permissions):
                    super().__init__(name)
                    self.permissions = permissions
            """,
            """
            def test_role():
                assert Admin("root", []).role == "admin", "У админа role = 'admin'"
                assert User("anna").role == "user", "У обычного пользователя role = 'user'"

            def test_can():
                a = Admin("root", ["delete", "ban"])
                assert a.can("ban") is True and a.can("fly") is False, "can проверяет наличие действия в permissions"
            """,
            """
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
            """,
            hint="Присвой `self.role = \"admin\"` **после** вызова `super().__init__`."),
        cod(f"{P}-m2-l1-e6", t("""
            Создай иерархию геометрических фигур и функцию подсчёта общей площади.

            1. `Shape` (уже в заготовке) — базовая фигура, `area()` возвращает `0`.
            2. `Square(side)` — наследник `Shape`, квадрат со стороной `side`. `area()` возвращает `side * side`.
            3. `Circle(r)` — наследник `Shape`, круг радиуса `r`. `area()` возвращает `3.14 * r * r`.
            4. Функция `total_area(shapes)` — получает список любых фигур и возвращает сумму их площадей.

            Пример:
            ```
            Square(3).area()                              # → 9
            Circle(1).area()                              # → 3.14
            total_area([Square(2), Circle(1), Shape()])   # → 7.14   (4 + 3.14 + 0)
            ```
            """),
            """
            class Shape:
                def area(self):
                    return 0
            """,
            """
            def test_square():
                assert Square(3).area() == 9, "Площадь квадрата 3 = 9"

            def test_circle():
                assert Circle(1).area() == 3.14, "Площадь круга r=1 = 3.14"

            def test_total():
                total = total_area([Square(2), Circle(1), Shape()])
                assert round(total, 2) == 7.14, f"Ожидалось 7.14, получено {total}"

            def test_inherits():
                assert isinstance(Square(1), Shape) and isinstance(Circle(1), Shape), "Фигуры должны наследовать Shape"
            """,
            """
            class Shape:
                def area(self):
                    return 0

            class Square(Shape):
                def __init__(self, side):
                    self.side = side

                def area(self):
                    return self.side * self.side

            class Circle(Shape):
                def __init__(self, r):
                    self.r = r

                def area(self):
                    return 3.14 * self.r * self.r

            def total_area(shapes):
                return sum(s.area() for s in shapes)
            """,
            xp=20),
    ),
    lesson(f"{P}-m2-l2", "Полиморфизм и абстрактные классы", """
        # Полиморфизм

        Разные классы с **одинаковым интерфейсом** можно использовать одинаково:

        ```
        for shape in [Square(2), Circle(1)]:
            print(shape.area())     # у каждого своя реализация
        ```

        Так устроены драйверы браузеров в UI-тестах: у Chrome и Firefox разный код, но методы `open()`, `click()` одинаковые.

        # Абстрактный класс

        Запрещает создавать «недоделанные» объекты и заставляет наследников реализовать методы:

        ```
        from abc import ABC, abstractmethod

        class Notifier(ABC):
            @abstractmethod
            def send(self, text): ...

        class EmailNotifier(Notifier):
            def send(self, text):
                return f"email: {text}"

        Notifier()          # TypeError — нельзя, метод send не реализован
        EmailNotifier()     # можно
        ```
        """,
        out(f"{P}-m2-l2-e1", "Что выведет программа?", """
            class Chrome:
                def open(self, url):
                    return f"Chrome открыл {url}"

            class Firefox:
                def open(self, url):
                    return f"Firefox открыл {url}"

            for driver in [Chrome(), Firefox()]:
                print(driver.open("/login"))
            """),
        out(f"{P}-m2-l2-e2", "Что выведет программа?", """
            from abc import ABC, abstractmethod

            class Base(ABC):
                @abstractmethod
                def run(self): ...

            class Impl(Base):
                def run(self):
                    return "работаю"

            try:
                Base()
            except TypeError:
                print("нельзя создать Base")
            print(Impl().run())
            """),
        cod(f"{P}-m2-l2-e3", t("""
            Создай абстрактный класс уведомлений и два его варианта.

            1. `Notifier` — абстрактный класс (наследник `ABC`) с абстрактным методом `send(text)` (декоратор `@abstractmethod`). Создать объект `Notifier()` напрямую должно быть нельзя — Python выбросит `TypeError`.
            2. `EmailNotifier` — наследник `Notifier`, его `send(text)` возвращает строку `"email: <text>"`.
            3. `SmsNotifier` — наследник `Notifier`, его `send(text)` возвращает `"sms: <text>"`.

            Пример:
            ```
            EmailNotifier().send("hi")   # → "email: hi"
            SmsNotifier().send("hi")     # → "sms: hi"
            Notifier()                   # TypeError
            ```
            """),
            """
            from abc import ABC, abstractmethod
            """,
            """
            def test_abstract():
                try:
                    Notifier()
                except TypeError:
                    pass
                else:
                    assert False, "Notifier должен быть абстрактным (ABC + @abstractmethod)"

            def test_impls():
                assert EmailNotifier().send("hi") == "email: hi", "EmailNotifier.send"
                assert SmsNotifier().send("hi") == "sms: hi", "SmsNotifier.send"
                assert isinstance(SmsNotifier(), Notifier), "Наследники должны наследовать Notifier"
            """,
            """
            from abc import ABC, abstractmethod

            class Notifier(ABC):
                @abstractmethod
                def send(self, text): ...

            class EmailNotifier(Notifier):
                def send(self, text):
                    return f"email: {text}"

            class SmsNotifier(Notifier):
                def send(self, text):
                    return f"sms: {text}"
            """),
        cod(f"{P}-m2-l2-e4", t("""
            Напиши функцию `notify_all(notifiers, text)` — разослать сообщение через все каналы.

            - Получает: `notifiers` — список объектов, у каждого есть метод `send(text)`; `text` — сообщение.
            - Вызывает `send(text)` у каждого объекта по порядку.
            - Возвращает: список результатов этих вызовов.

            Пример (классы условные):
            ```
            notify_all([EmailNotifier(), SmsNotifier()], "x")   # → ["email: x", "sms: x"]
            ```
            Функция не должна проверять, какого класса объект, — ей важно только, что у него есть `send`. Это и есть полиморфизм.
            """),
            """
            def notify_all(notifiers, text):
                pass
            """,
            """
            class A:
                def send(self, t):
                    return "A:" + t

            class B:
                def send(self, t):
                    return "B:" + t

            def test_all():
                assert notify_all([A(), B(), A()], "x") == ["A:x", "B:x", "A:x"], "Ожидался список результатов send"
            """,
            """
            def notify_all(notifiers, text):
                return [n.send(text) for n in notifiers]
            """),
        cod(f"{P}-m2-l2-e5", t("""
            Допиши систему проверок по паттерну «шаблонный метод».

            1. В базовом классе `Check` допиши метод `run(value)`: он вызывает `self.check(value)` и возвращает `"PASS"`, если проверка вернула истину, иначе `"FAIL"`.
            2. Создай наследника `NotEmpty` — его `check(value)` возвращает `True`, если строка `value` не пустая.
            3. Создай наследника `IsPositive` — его `check(value)` возвращает `True`, если число `value` больше нуля.

            Пример:
            ```
            NotEmpty().run("abc")   # → "PASS"
            NotEmpty().run("")      # → "FAIL"
            IsPositive().run(5)     # → "PASS"
            IsPositive().run(-1)    # → "FAIL"
            ```
            Общий алгоритм (`run`) живёт в родителе, а детали (`check`) — в наследниках.
            """),
            """
            from abc import ABC, abstractmethod

            class Check(ABC):
                def run(self, value):
                    pass

                @abstractmethod
                def check(self, value): ...
            """,
            """
            def test_not_empty():
                assert NotEmpty().run("abc") == "PASS" and NotEmpty().run("") == "FAIL", "NotEmpty"

            def test_positive():
                assert IsPositive().run(5) == "PASS" and IsPositive().run(-1) == "FAIL", "IsPositive"
            """,
            """
            from abc import ABC, abstractmethod

            class Check(ABC):
                def run(self, value):
                    return "PASS" if self.check(value) else "FAIL"

                @abstractmethod
                def check(self, value): ...

            class NotEmpty(Check):
                def check(self, value):
                    return value != ""

            class IsPositive(Check):
                def check(self, value):
                    return value > 0
            """,
            hint="Общий алгоритм в родителе, детали в наследниках — паттерн «шаблонный метод».", xp=20),
    ),
)

m3 = module(f"{P}-m3", "Магия Python", "✨", "Dunder-методы, property, classmethod и dataclass",
    lesson(f"{P}-m3-l1", "Dunder-методы", """
        # Магические (dunder) методы

        Методы с двойным подчёркиванием позволяют объекту работать со встроенными операциями:

        - `__eq__(self, other)` — сравнение `==`
        - `__lt__(self, other)` — `<` (и сортировка!)
        - `__len__(self)` — `len(obj)`
        - `__add__(self, other)` — `obj + other`
        - `__contains__(self, x)` — `x in obj`
        - `__getitem__(self, i)` — `obj[i]`

        ```
        class Money:
            def __init__(self, amount):
                self.amount = amount
            def __add__(self, other):
                return Money(self.amount + other.amount)
            def __eq__(self, other):
                return self.amount == other.amount
        ```

        Без `__eq__` два объекта равны, **только если это один и тот же объект**.
        """,
        out(f"{P}-m3-l1-e1", "Что выведет программа?", """
            class P:
                def __init__(self, x):
                    self.x = x

            print(P(1) == P(1))

            class Q:
                def __init__(self, x):
                    self.x = x
                def __eq__(self, other):
                    return self.x == other.x

            print(Q(1) == Q(1))
            """),
        out(f"{P}-m3-l1-e2", "Что выведет программа?", """
            class Playlist:
                def __init__(self, songs):
                    self.songs = songs
                def __len__(self):
                    return len(self.songs)
                def __contains__(self, song):
                    return song in self.songs
                def __getitem__(self, i):
                    return self.songs[i]

            p = Playlist(["A", "B", "C"])
            print(len(p), "B" in p, p[-1])
            """),
        cod(f"{P}-m3-l1-e3", t("""
            Научи класс `Money` складываться и сравниваться.

            Добавь два магических метода:
            - `__add__(self, other)` — вызывается при `a + b`. Возвращает **новый** объект `Money`, у которого `amount` равен сумме сумм.
            - `__eq__(self, other)` — вызывается при `a == b`. Возвращает `True`, если у объектов одинаковый `amount`.

            Пример:
            ```
            total = Money(100) + Money(50)
            total.amount              # → 150
            Money(10) == Money(10)    # → True
            Money(10) == Money(20)    # → False
            ```
            """),
            """
            class Money:
                def __init__(self, amount):
                    self.amount = amount
            """,
            """
            def test_add():
                total = Money(100) + Money(50)
                assert isinstance(total, Money) and total.amount == 150, "Money(100) + Money(50) → Money(150)"

            def test_eq():
                assert Money(10) == Money(10) and not (Money(10) == Money(20)), "Сравнение по amount"
            """,
            """
            class Money:
                def __init__(self, amount):
                    self.amount = amount

                def __add__(self, other):
                    return Money(self.amount + other.amount)

                def __eq__(self, other):
                    return self.amount == other.amount
            """),
        cod(f"{P}-m3-l1-e4", t("""
            Научи класс `Version` правильно сравнивать номера версий.

            Проблема: как строки `"1.10.0" < "1.9.2"` — потому что символ `"1"` меньше `"9"`. А по смыслу версия 1.10 новее 1.9.

            В заготовке конструктор уже превращает строку в кортеж чисел: `Version("1.10.0").parts == (1, 10, 0)`.
            Добавь метод `__lt__(self, other)` (оператор `<`), который сравнивает версии по `parts`. Кортежи сравниваются поэлементно: `(1, 9, 2) < (1, 10, 0)` — верно.

            Пример:
            ```
            Version("1.9.2") < Version("1.10.0")   # → True
            [v.text for v in sorted([Version("2.0.0"), Version("1.10.0"), Version("1.9.2")])]
            # → ["1.9.2", "1.10.0", "2.0.0"]
            ```
            Когда есть `__lt__`, начинает работать и `sorted`.
            """),
            """
            class Version:
                def __init__(self, text):
                    self.parts = tuple(int(p) for p in text.split("."))
                    self.text = text
            """,
            """
            def test_lt():
                assert Version("1.9.2") < Version("1.10.0"), "1.9.2 < 1.10.0 (числа, а не строки!)"

            def test_sorted():
                vs = [Version("2.0.0"), Version("1.10.0"), Version("1.9.2")]
                assert [v.text for v in sorted(vs)] == ["1.9.2", "1.10.0", "2.0.0"], "sorted должен работать"
            """,
            """
            class Version:
                def __init__(self, text):
                    self.parts = tuple(int(p) for p in text.split("."))
                    self.text = text

                def __lt__(self, other):
                    return self.parts < other.parts
            """,
            hint="Кортежи сравниваются поэлементно: `(1, 9, 2) < (1, 10, 0)`."),
        cod(f"{P}-m3-l1-e5", t("""
            Допиши класс `TestSuite` — набор тестов, который ведёт себя как коллекция.

            Добавь:
            - метод `add(test_name)` — добавляет имя теста в `self.tests`;
            - `__len__` — чтобы работал `len(suite)` (количество тестов);
            - `__contains__` — чтобы работало `"имя" in suite`;
            - `__iter__` — чтобы набор можно было перебрать циклом `for`.

            Пример:
            ```
            s = TestSuite("smoke")
            s.add("login")
            s.add("search")
            len(s)          # → 2
            "login" in s    # → True
            "pay" in s      # → False
            list(s)         # → ["login", "search"]
            ```
            """),
            """
            class TestSuite:
                def __init__(self, name):
                    self.name = name
                    self.tests = []
            """,
            """
            def test_suite():
                s = TestSuite("smoke")
                s.add("login")
                s.add("search")
                assert len(s) == 2, "len(suite) → 2"
                assert "login" in s and "pay" not in s, "Проверка in"
                assert list(s) == ["login", "search"], "Перебор suite в цикле"
            """,
            """
            class TestSuite:
                def __init__(self, name):
                    self.name = name
                    self.tests = []

                def add(self, test_name):
                    self.tests.append(test_name)

                def __len__(self):
                    return len(self.tests)

                def __contains__(self, item):
                    return item in self.tests

                def __iter__(self):
                    return iter(self.tests)
            """,
            hint="`__iter__` может просто вернуть `iter(self.tests)`.", xp=20),
    ),
    lesson(f"{P}-m3-l2", "property, classmethod, dataclass", """
        # @property — атрибут с логикой

        ```
        class Temperature:
            def __init__(self, celsius):
                self.celsius = celsius

            @property
            def fahrenheit(self):              # читается как атрибут, без скобок
                return self.celsius * 9 / 5 + 32

            @fahrenheit.setter
            def fahrenheit(self, value):       # и присваивается как атрибут
                self.celsius = (value - 32) * 5 / 9
        ```

        # @classmethod и @staticmethod

        ```
        class User:
            def __init__(self, name, email):
                self.name, self.email = name, email

            @classmethod
            def from_string(cls, text):        # альтернативный конструктор
                name, email = text.split(",")
                return cls(name, email)

            @staticmethod
            def is_valid_email(email):         # просто функция внутри класса
                return "@" in email
        ```

        # @dataclass — класс для данных без рутины

        ```
        from dataclasses import dataclass

        @dataclass
        class Point:
            x: int
            y: int = 0
        ```
        Автоматически создаст `__init__`, `__repr__` и `__eq__`.
        """,
        out(f"{P}-m3-l2-e1", "Что выведет программа?", """
            class Temperature:
                def __init__(self, celsius):
                    self.celsius = celsius

                @property
                def fahrenheit(self):
                    return self.celsius * 9 / 5 + 32

            t = Temperature(100)
            print(t.fahrenheit)
            t.celsius = 0
            print(t.fahrenheit)
            """),
        out(f"{P}-m3-l2-e2", "Что выведет программа?", """
            from dataclasses import dataclass

            @dataclass
            class Point:
                x: int
                y: int = 0

            p = Point(3)
            print(p)
            print(p == Point(3, 0))
            """),
        cod(f"{P}-m3-l2-e3", t("""
            Добавь в класс `User` два метода-декоратора.

            1. **`@classmethod` `from_string(cls, text)`** — альтернативный конструктор. Получает строку вида `"имя,email"`, разбивает её по запятой и возвращает **новый объект** `User`.
            2. **`@staticmethod` `is_valid_email(email)`** — возвращает `True`, если в строке есть символ `@`, иначе `False`.

            Пример:
            ```
            u = User.from_string("Аня,anna@mail.ru")
            u.name    # → "Аня"
            u.email   # → "anna@mail.ru"

            User.is_valid_email("a@b.c")   # → True
            User.is_valid_email("abc")     # → False
            ```
            """),
            """
            class User:
                def __init__(self, name, email):
                    self.name = name
                    self.email = email
            """,
            """
            def test_from_string():
                u = User.from_string("Аня,anna@mail.ru")
                assert isinstance(u, User) and u.name == "Аня" and u.email == "anna@mail.ru", "from_string разбирает строку"

            def test_valid():
                assert User.is_valid_email("a@b.c") is True and User.is_valid_email("abc") is False, "is_valid_email проверяет @"
            """,
            """
            class User:
                def __init__(self, name, email):
                    self.name = name
                    self.email = email

                @classmethod
                def from_string(cls, text):
                    name, email = text.split(",")
                    return cls(name, email)

                @staticmethod
                def is_valid_email(email):
                    return "@" in email
            """),
        cod(f"{P}-m3-l2-e4", t("""
            Защити цену товара от некорректных значений с помощью `@property`.

            Сейчас в `Product` можно записать любую цену, даже отрицательную. Сделай `price` **свойством**:
            - чтение `p.price` возвращает цену (храни её в `self._price`);
            - запись `p.price = значение` проверяет: если значение меньше 0 — бросает `ValueError` и цену **не меняет**, иначе сохраняет.
            - Проверка должна срабатывать и при создании объекта: `Product("чай", -1)` → `ValueError`. (Строку `self.price = price` в конструкторе оставь — она сама пройдёт через проверку.)

            Пример:
            ```
            p = Product("чай", 100)
            p.price = 150    # ок
            p.price = -5     # ValueError, цена осталась 150
            ```
            Нужны `@property def price(self)` и `@price.setter def price(self, value)`.
            """),
            """
            class Product:
                def __init__(self, name, price):
                    self.name = name
                    self.price = price
            """,
            """
            def test_ok():
                p = Product("чай", 100)
                p.price = 150
                assert p.price == 150, "Цену можно менять"

            def test_negative():
                p = Product("чай", 100)
                try:
                    p.price = -5
                except ValueError:
                    pass
                else:
                    assert False, "Отрицательная цена должна давать ValueError"
                assert p.price == 100, "Цена не должна измениться"

            def test_init():
                try:
                    Product("чай", -1)
                except ValueError:
                    return
                assert False, "Проверка должна работать и в конструкторе"
            """,
            """
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
                        raise ValueError("Цена не может быть отрицательной")
                    self._price = value
            """,
            hint="`@property def price(self)` + `@price.setter def price(self, value)`. Присваивание в `__init__` тоже пройдёт через setter.", xp=20),
        cod(f"{P}-m3-l2-e5", t("""
            Создай класс-данные `TestResult` с помощью `@dataclass`.

            Поля (с аннотациями типов):
            - `name: str` — имя теста;
            - `passed: bool` — прошёл ли;
            - `duration: float = 0.0` — время выполнения, по умолчанию `0.0`.

            И метод `status()`, который возвращает `"✅ имя"` для прошедшего теста и `"❌ имя"` для упавшего.

            Пример:
            ```
            r = TestResult("login", True)
            r.duration                          # → 0.0
            r.status()                          # → "✅ login"
            TestResult("pay", False).status()   # → "❌ pay"
            r == TestResult("login", True)      # → True   dataclass сравнивает по полям сам
            ```
            """),
            """
            from dataclasses import dataclass
            """,
            """
            from dataclasses import is_dataclass

            def test_dataclass():
                assert is_dataclass(TestResult), "TestResult должен быть @dataclass"
                r = TestResult("login", True)
                assert r.duration == 0.0, "duration по умолчанию 0.0"
                assert r == TestResult("login", True, 0.0), "dataclass сам умеет сравнивать"

            def test_status():
                assert TestResult("a", True).status() == "✅ a" and TestResult("b", False).status() == "❌ b", "status()"
            """,
            """
            from dataclasses import dataclass

            @dataclass
            class TestResult:
                name: str
                passed: bool
                duration: float = 0.0

                def status(self):
                    return f"{'✅' if self.passed else '❌'} {self.name}"
            """),
    ),
)

TOPIC = topic("oop", "ООП", "🏛️", "#ff4b4b",
              "Классы, наследование, полиморфизм, dunder-методы и dataclass", m1, m2, m3, group="Python")
