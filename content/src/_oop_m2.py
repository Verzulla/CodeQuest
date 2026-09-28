"""Тема «Классы», модуль 2 «Наследование» — задания. Теория — в _oop_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "oop"

m2 = module(f"{P}-m2", "Наследование", "🧬", "Наследование и super(), переопределение, полиморфизм, ABC, isinstance, композиция",

lesson(f"{P}-m2-l1", "Наследование и super()",
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
    cod(f"{P}-m2-l1-e7", t("""
        Создай класс `Employee(name, salary)` с методом `yearly()` — годовой доход (`salary * 12`). Затем наследника `Manager(name, salary, bonus)`: его `__init__` вызывает `super().__init__`, а `yearly()` добавляет годовой бонус к результату родителя.
        """),
        "",
        """
        def test_values():
            assert Employee("Аня", 100).yearly() == 1200, "Employee"
            m = Manager("Боря", 100, 500)
            assert m.name == "Боря" and m.yearly() == 1700 and isinstance(m, Employee), "Manager"
        """,
        """
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
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Есть базовый класс `Logger` с методом `log(msg)`, который добавляет строку в `self.lines`. Создай наследника `PrefixLogger(prefix)`: он добавляет к каждому сообщению префикс в квадратных скобках и **сохраняет через родительский метод**.

        ```
        l = PrefixLogger("API")
        l.log("старт")
        l.lines   # → ["[API] старт"]
        ```
        """),
        """
        class Logger:
            def __init__(self):
                self.lines = []

            def log(self, msg):
                self.lines.append(msg)
        """,
        """
        def test_prefix():
            l = PrefixLogger("API")
            l.log("старт")
            l.log("стоп")
            assert l.lines == ["[API] старт", "[API] стоп"], f"Получено {l.lines}"
            assert "super()" in open("solution.py", encoding="utf-8").read(), "Используй super()"
        """,
        """
        class Logger:
            def __init__(self):
                self.lines = []

            def log(self, msg):
                self.lines.append(msg)


        class PrefixLogger(Logger):
            def __init__(self, prefix):
                super().__init__()
                self.prefix = prefix

            def log(self, msg):
                super().log(f"[{self.prefix}] {msg}")
        """, xp=20),
),

lesson(f"{P}-override", "Переопределение и порядок поиска методов",
    out(f"{P}-override-e1", "Что выведет программа?", """
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
        """, hint="self.hello() ищется у настоящего класса объекта — даже внутри метода родителя."),
    out(f"{P}-override-e2", "Что выведет программа? Порядок поиска (MRO).", """
        class A:
            def who(self):
                return "A"

        class B(A):
            pass

        class C(B):
            pass

        print(C().who())
        print([cls.__name__ for cls in C.__mro__])
        """),
    out(f"{P}-override-e3", "Что выведет программа? Множественное наследование.", """
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
        """, hint="Родители просматриваются слева направо."),
    cod(f"{P}-override-e4", t("""
        Есть класс `Shape` с методом `describe()`, который возвращает `f"{self.name}: площадь {self.area()}"`. Создай наследников:

        - `Square(side)` — `name = "квадрат"`, площадь `side ** 2`;
        - `Circle(r)` — `name = "круг"`, площадь `round(3.14 * r ** 2, 2)`.

        `describe` переписывать не нужно — он сам вызовет нужный `area`.
        """),
        """
        class Shape:
            name = "фигура"

            def area(self):
                return 0

            def describe(self):
                return f"{self.name}: площадь {self.area()}"
        """,
        """
        def test_shapes():
            assert Square(3).describe() == "квадрат: площадь 9", Square(3).describe()
            assert Circle(1).describe() == "круг: площадь 3.14", Circle(1).describe()
            assert "describe" not in open("solution.py", encoding="utf-8").read().split("class Square")[1], "describe переопределять не нужно"
        """,
        """
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


        class Circle(Shape):
            name = "круг"

            def __init__(self, r):
                self.r = r

            def area(self):
                return round(3.14 * self.r ** 2, 2)
        """),
    cod(f"{P}-override-e5", t("""
        Создай класс `Request(url)` с методом `headers()` → `{"Accept": "json"}`. Наследник `AuthRequest(url, token)` переопределяет `headers()`: берёт заголовки родителя и добавляет `"Authorization": "Bearer <token>"`.
        """),
        "",
        """
        def test_headers():
            assert Request("/a").headers() == {"Accept": "json"}, "Request"
            r = AuthRequest("/a", "abc")
            assert r.url == "/a" and r.headers() == {"Accept": "json", "Authorization": "Bearer abc"}, f"Получено {r.headers()}"
        """,
        """
        class Request:
            def __init__(self, url):
                self.url = url

            def headers(self):
                return {"Accept": "json"}


        class AuthRequest(Request):
            def __init__(self, url, token):
                super().__init__(url)
                self.token = token

            def headers(self):
                h = super().headers()
                h["Authorization"] = f"Bearer {self.token}"
                return h
        """),
    cod(f"{P}-override-e6", t("""
        Создай класс `Stack` (методы `push`, `pop`, атрибут `items`) и наследника `LimitedStack(limit)`: его `push` при переполнении выбрасывает `OverflowError("стек полон")`, иначе вызывает родительский `push`.
        """),
        "",
        """
        def test_limited():
            s = LimitedStack(2)
            s.push(1)
            s.push(2)
            try:
                s.push(3)
            except OverflowError as e:
                assert str(e) == "стек полон" and s.items == [1, 2], "Третий элемент не добавляется"
            else:
                assert False, "Нужен OverflowError"
            assert s.pop() == 2 and isinstance(s, Stack), "pop унаследован"
        """,
        """
        class Stack:
            def __init__(self):
                self.items = []

            def push(self, x):
                self.items.append(x)

            def pop(self):
                return self.items.pop()


        class LimitedStack(Stack):
            def __init__(self, limit):
                super().__init__()
                self.limit = limit

            def push(self, x):
                if len(self.items) >= self.limit:
                    raise OverflowError("стек полон")
                super().push(x)
        """),
    cod(f"{P}-override-e7", t("""
        Напиши функцию `mro_names(cls)` — список имён классов в порядке поиска методов, **без** `object`.

        ```
        class A: pass
        class B(A): pass
        mro_names(B)   # → ["B", "A"]
        ```
        """),
        """
        def mro_names(cls):
            pass
        """,
        """
        def test_values():
            class A: pass
            class B(A): pass
            class C: pass
            class D(B, C): pass
            assert mro_names(B) == ["B", "A"] and mro_names(D) == ["D", "B", "A", "C"] and mro_names(int) == ["int"], "Неверный порядок"
        """,
        """
        def mro_names(cls):
            return [c.__name__ for c in cls.__mro__ if c is not object]
        """),
    cod(f"{P}-override-e8", t("""
        Создай «миксин» `JsonMixin` с методом `to_dict()` — возвращает копию `vars(self)`. Затем класс `User(JsonMixin)` с атрибутами `name`, `age`. Миксин не знает про `User` — он работает для любого класса.
        """),
        "",
        """
        def test_mixin():
            u = User("Аня", 30)
            d = u.to_dict()
            assert d == {"name": "Аня", "age": 30}, f"Получено {d}"
            d["name"] = "X"
            assert u.name == "Аня", "Нужна копия"
            class Point(JsonMixin):
                def __init__(self):
                    self.x = 1
            assert Point().to_dict() == {"x": 1}, "Миксин работает для любого класса"
        """,
        """
        class JsonMixin:
            def to_dict(self):
                return dict(vars(self))


        class User(JsonMixin):
            def __init__(self, name, age):
                self.name = name
                self.age = age
        """, xp=20),
),

lesson(f"{P}-m2-l2", "Полиморфизм и абстрактные классы",
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
    out(f"{P}-m2-l2-e6", "Что выведет программа? Одинаковый вызов — разное поведение.", """
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
        """),
    cod(f"{P}-m2-l2-e7", t("""
        Создай абстрактный класс `Storage(ABC)` с абстрактными методами `save(key, value)` и `load(key)`. Затем реализацию `MemoryStorage` на словаре (`load` несуществующего ключа → `None`).
        """),
        "",
        """
        def test_abc():
            try:
                Storage()
            except TypeError:
                pass
            else:
                assert False, "Storage должен быть абстрактным"
            s = MemoryStorage()
            s.save("a", 1)
            assert s.load("a") == 1 and s.load("b") is None and isinstance(s, Storage), "MemoryStorage"
        """,
        """
        from abc import ABC, abstractmethod


        class Storage(ABC):
            @abstractmethod
            def save(self, key, value):
                pass

            @abstractmethod
            def load(self, key):
                pass


        class MemoryStorage(Storage):
            def __init__(self):
                self.data = {}

            def save(self, key, value):
                self.data[key] = value

            def load(self, key):
                return self.data.get(key)
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `total_area(shapes)` — сумма `area()` всех фигур. Функция не должна проверять тип фигуры: любой объект с методом `area()` подходит (утиная типизация). Создай также классы `Rect(w, h)` и `Square(side)`.
        """),
        "",
        """
        def test_total():
            class Custom:
                def area(self):
                    return 100
            assert total_area([Rect(2, 3), Square(2), Custom()]) == 110 and total_area([]) == 0, "Неверная сумма"
            assert "isinstance" not in open("solution.py", encoding="utf-8").read(), "Без проверок типа"
        """,
        """
        class Rect:
            def __init__(self, w, h):
                self.w = w
                self.h = h

            def area(self):
                return self.w * self.h


        class Square:
            def __init__(self, side):
                self.side = side

            def area(self):
                return self.side ** 2


        def total_area(shapes):
            return sum(s.area() for s in shapes)
        """),
),

lesson(f"{P}-isinstance", "isinstance, type и проверки классов",
    out(f"{P}-isinstance-e1", "Что выведет программа?", """
        class Animal: pass
        class Dog(Animal): pass

        d = Dog()
        print(isinstance(d, Dog), isinstance(d, Animal), isinstance(d, object))
        print(type(d) is Dog, type(d) is Animal)
        print(issubclass(Dog, Animal), issubclass(Animal, Dog))
        """, hint="isinstance учитывает наследование, type(...) is — нет."),
    out(f"{P}-isinstance-e2", "Что выведет программа? Кортеж типов.", """
        values = [1, 2.5, "3", True, None, [4]]
        for v in values:
            print(type(v).__name__, isinstance(v, (int, float)))
        """, hint="bool — наследник int!"),
    out(f"{P}-isinstance-e3", "Что выведет программа? Имя класса объекта.", """
        class HttpError(Exception): pass
        class NotFound(HttpError): pass

        e = NotFound("нет страницы")
        print(type(e).__name__, e.__class__.__name__)
        print(NotFound.__bases__[0].__name__)
        print(isinstance(e, Exception))
        """),
    cod(f"{P}-isinstance-e4", t("""
        Напиши функцию `only_numbers(values)` — оставить только числа (`int` и `float`), но **не** `bool`.

        ```
        only_numbers([1, "2", 3.5, True, None])   # → [1, 3.5]
        ```
        """),
        """
        def only_numbers(values):
            pass
        """,
        """
        def test_values():
            assert only_numbers([1, "2", 3.5, True, None]) == [1, 3.5] and only_numbers([]) == [] and only_numbers([False, 0]) == [0], "Неверный фильтр"
        """,
        """
        def only_numbers(values):
            return [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]
        """),
    cod(f"{P}-isinstance-e5", t("""
        Напиши функцию `describe(value)`:

        - строка → `"строка из N символов"`;
        - список или кортеж → `"коллекция из N элементов"`;
        - словарь → `"словарь с N ключами"`;
        - что угодно другое → имя типа (`"int"`, `"NoneType"`…).
        """),
        """
        def describe(value):
            pass
        """,
        """
        def test_values():
            assert describe("abc") == "строка из 3 символов", describe("abc")
            assert describe([1, 2]) == "коллекция из 2 элементов" and describe((1,)) == "коллекция из 1 элементов", "Коллекции"
            assert describe({"a": 1}) == "словарь с 1 ключами" and describe(5) == "int" and describe(None) == "NoneType", "Прочее"
        """,
        """
        def describe(value):
            if isinstance(value, str):
                return f"строка из {len(value)} символов"
            if isinstance(value, (list, tuple)):
                return f"коллекция из {len(value)} элементов"
            if isinstance(value, dict):
                return f"словарь с {len(value)} ключами"
            return type(value).__name__
        """),
    cod(f"{P}-isinstance-e6", t("""
        Напиши функцию `count_by_type(objs)` — словарь «имя класса → сколько объектов». Порядок ключей — по первому появлению.

        ```
        count_by_type([1, "a", 2, None])   # → {"int": 2, "str": 1, "NoneType": 1}
        ```
        """),
        """
        def count_by_type(objs):
            pass
        """,
        """
        def test_values():
            r = count_by_type([1, "a", 2, None])
            assert r == {"int": 2, "str": 1, "NoneType": 1} and list(r) == ["int", "str", "NoneType"] and count_by_type([]) == {}, f"Получено {r}"
        """,
        """
        def count_by_type(objs):
            result = {}
            for o in objs:
                name = type(o).__name__
                result[name] = result.get(name, 0) + 1
            return result
        """),
    cod(f"{P}-isinstance-e7", t("""
        Есть иерархия ошибок API. Напиши функцию `severity(error)`:

        - `ServerError` и его наследники → `"critical"`;
        - `ClientError` и его наследники → `"warning"`;
        - прочие исключения → `"unknown"`.
        """),
        """
        class ApiError(Exception): pass
        class ClientError(ApiError): pass
        class NotFound(ClientError): pass
        class ServerError(ApiError): pass
        class Timeout(ServerError): pass

        def severity(error):
            pass
        """,
        """
        def test_values():
            assert severity(Timeout()) == "critical" and severity(ServerError()) == "critical", "Серверные"
            assert severity(NotFound()) == "warning" and severity(ClientError()) == "warning", "Клиентские"
            assert severity(ApiError()) == "unknown" and severity(ValueError()) == "unknown", "Прочие"
        """,
        """
        class ApiError(Exception): pass
        class ClientError(ApiError): pass
        class NotFound(ClientError): pass
        class ServerError(ApiError): pass
        class Timeout(ServerError): pass

        def severity(error):
            if isinstance(error, ServerError):
                return "critical"
            if isinstance(error, ClientError):
                return "warning"
            return "unknown"
        """),
    cod(f"{P}-isinstance-e8", t("""
        Напиши функцию `flatten(data)` — развернуть вложенные списки и кортежи любой глубины в плоский список. Строки не разворачивать!

        ```
        flatten([1, [2, (3, "ab")], [[4]]])   # → [1, 2, 3, "ab", 4]
        ```
        """),
        """
        def flatten(data):
            pass
        """,
        """
        def test_values():
            assert flatten([1, [2, (3, "ab")], [[4]]]) == [1, 2, 3, "ab", 4] and flatten([]) == [] and flatten([[[]]]) == [], "Неверный результат"
        """,
        """
        def flatten(data):
            result = []
            for item in data:
                if isinstance(item, (list, tuple)):
                    result.extend(flatten(item))
                else:
                    result.append(item)
            return result
        """, xp=20),
),

lesson(f"{P}-composition", "Композиция: объект внутри объекта",
    out(f"{P}-composition-e1", "Что выведет программа?", """
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
        """, hint="Car не наследует Engine, а содержит его — «имеет», а не «является»."),
    out(f"{P}-composition-e2", "Что выведет программа? Коллекция объектов.", """
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
        g.add(Student("Вика", 80))
        print(g.best(), len(g.students))
        """),
    out(f"{P}-composition-e3", "Что выведет программа? Подмена зависимости.", """
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
        """, hint="Зависимость передаётся снаружи — в тестах её легко подменить."),
    cod(f"{P}-composition-e4", t("""
        Создай классы:

        - `Item(name, price, qty)` с методом `cost()` — `price * qty`;
        - `Order()` с методами `add(item)` и `total()` — сумма `cost()` всех позиций.
        """),
        "",
        """
        def test_order():
            o = Order()
            assert o.total() == 0, "Пустой заказ"
            o.add(Item("чай", 300, 2))
            o.add(Item("кофе", 500, 1))
            assert o.total() == 1100, f"Получено {o.total()}"
        """,
        """
        class Item:
            def __init__(self, name, price, qty):
                self.name = name
                self.price = price
                self.qty = qty

            def cost(self):
                return self.price * self.qty


        class Order:
            def __init__(self):
                self.items = []

            def add(self, item):
                self.items.append(item)

            def total(self):
                return sum(item.cost() for item in self.items)
        """),
    cod(f"{P}-composition-e5", t("""
        Создай класс `UserService(storage)`, который **получает хранилище снаружи**. Методы:

        - `register(name)` — если имя уже есть в хранилище (`storage.load(name)` не `None`), выбросить `ValueError("занято")`, иначе `storage.save(name, True)`;
        - `exists(name)` — `True`/`False`.

        Хранилище — любой объект с методами `save(key, value)` и `load(key)`.
        """),
        "",
        """
        def test_service():
            class FakeStorage:
                def __init__(self):
                    self.data = {}
                def save(self, k, v):
                    self.data[k] = v
                def load(self, k):
                    return self.data.get(k)
            st = FakeStorage()
            s = UserService(st)
            s.register("аня")
            assert st.data == {"аня": True} and s.exists("аня") and not s.exists("боря"), "register/exists"
            try:
                s.register("аня")
            except ValueError as e:
                assert str(e) == "занято", str(e)
                return
            assert False, "Нужен ValueError"
        """,
        """
        class UserService:
            def __init__(self, storage):
                self.storage = storage

            def register(self, name):
                if self.storage.load(name) is not None:
                    raise ValueError("занято")
                self.storage.save(name, True)

            def exists(self, name):
                return self.storage.load(name) is not None
        """),
    cod(f"{P}-composition-e6", t("""
        Создай класс `Library` с методами:

        - `add(book)` — книга — объект `Book(title, author)`;
        - `by_author(author)` — список названий книг автора в порядке добавления;
        - `authors()` — отсортированный список уникальных авторов.

        Класс `Book` тоже создай.
        """),
        "",
        """
        def test_library():
            lib = Library()
            lib.add(Book("Мцыри", "Лермонтов"))
            lib.add(Book("Онегин", "Пушкин"))
            lib.add(Book("Демон", "Лермонтов"))
            assert lib.by_author("Лермонтов") == ["Мцыри", "Демон"] and lib.by_author("Гоголь") == [], "by_author"
            assert lib.authors() == ["Лермонтов", "Пушкин"], "authors"
        """,
        """
        class Book:
            def __init__(self, title, author):
                self.title = title
                self.author = author


        class Library:
            def __init__(self):
                self.books = []

            def add(self, book):
                self.books.append(book)

            def by_author(self, author):
                return [b.title for b in self.books if b.author == author]

            def authors(self):
                return sorted({b.author for b in self.books})
        """),
    cod(f"{P}-composition-e7", t("""
        Создай класс `Notifier(*channels)` — хранит каналы (объекты с методом `send(text)`, возвращающим строку). Метод `broadcast(text)` отправляет сообщение во все каналы и возвращает список результатов.
        """),
        "",
        """
        def test_broadcast():
            class A:
                def send(self, t):
                    return "A:" + t
            class B:
                def send(self, t):
                    return "B:" + t
            assert Notifier(A(), B()).broadcast("x") == ["A:x", "B:x"] and Notifier().broadcast("x") == [], "broadcast"
        """,
        """
        class Notifier:
            def __init__(self, *channels):
                self.channels = list(channels)

            def broadcast(self, text):
                return [ch.send(text) for ch in self.channels]
        """),
    cod(f"{P}-composition-e8", t("""
        Создай класс `TestRunner(reporter)`:

        - `run(tests)` — `tests` — словарь «имя → функция». Каждую функцию вызвать: без ошибки — `reporter.passed(name)`, при `AssertionError` — `reporter.failed(name)`. Вернуть количество упавших.

        Также создай класс `ListReporter` с атрибутом `log` (список) и методами `passed(name)` → `log.append("✓ " + name)` и `failed(name)` → `log.append("✗ " + name)`.
        """),
        "",
        """
        def test_runner():
            def ok(): assert 1 == 1
            def bad(): assert 1 == 2
            rep = ListReporter()
            n = TestRunner(rep).run({"ok": ok, "bad": bad, "ok2": ok})
            assert n == 1 and rep.log == ["✓ ok", "✗ bad", "✓ ok2"], f"{n}, {rep.log}"
        """,
        """
        class ListReporter:
            def __init__(self):
                self.log = []

            def passed(self, name):
                self.log.append("✓ " + name)

            def failed(self, name):
                self.log.append("✗ " + name)


        class TestRunner:
            def __init__(self, reporter):
                self.reporter = reporter

            def run(self, tests):
                failed = 0
                for name, func in tests.items():
                    try:
                        func()
                    except AssertionError:
                        failed += 1
                        self.reporter.failed(name)
                    else:
                        self.reporter.passed(name)
                return failed
        """, xp=25),
),
)
