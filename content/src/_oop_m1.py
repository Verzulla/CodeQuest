"""Тема «Классы», модуль 1 «Классы и объекты» — задания. Теория — в _oop_t1.py.

Слаги oop-* унаследованы от старой темы «ООП» — так сохраняется прогресс."""
from ._lib import cod, lesson, module, out, t

P = "oop"

m1 = module(f"{P}-m1", "Классы и объекты", "🏛️", "Первый класс, __init__, методы и self, атрибуты класса, ссылки и копии",

lesson(f"{P}-m1-l1", "Первый класс",
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
    cod(f"{P}-m1-l1-e7", t("""
        Создай класс `Timer` — секундомер:

        - `Timer(seconds=0)` — начальное значение в `self.seconds`;
        - `tick()` — прибавить одну секунду;
        - `reset()` — обнулить.

        ```
        t = Timer(5)
        t.tick(); t.tick()
        t.seconds   # → 7
        t.reset()
        t.seconds   # → 0
        ```
        """),
        "",
        """
        def test_timer():
            t = Timer(5)
            t.tick()
            t.tick()
            assert t.seconds == 7, f"После двух tick: {t.seconds}"
            t.reset()
            assert t.seconds == 0 and Timer().seconds == 0, "reset обнуляет, по умолчанию 0"
        """,
        """
        class Timer:
            def __init__(self, seconds=0):
                self.seconds = seconds

            def tick(self):
                self.seconds += 1

            def reset(self):
                self.seconds = 0
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Создай класс `Stack` — стек на основе списка:

        - `push(x)` — положить сверху;
        - `pop()` — снять верхний и вернуть (для пустого — `None`);
        - `peek()` — посмотреть верхний, не снимая (для пустого — `None`);
        - `size()` — количество элементов.
        """),
        "",
        """
        def test_stack():
            s = Stack()
            s.push(1)
            s.push(2)
            assert s.peek() == 2 and s.size() == 2, "peek и size"
            assert s.pop() == 2 and s.pop() == 1 and s.pop() is None and s.peek() is None and s.size() == 0, "pop"

        def test_independent():
            a, b = Stack(), Stack()
            a.push(1)
            assert b.size() == 0, "У каждого стека свой список"
        """,
        """
        class Stack:
            def __init__(self):
                self.items = []

            def push(self, x):
                self.items.append(x)

            def pop(self):
                if not self.items:
                    return None
                return self.items.pop()

            def peek(self):
                if not self.items:
                    return None
                return self.items[-1]

            def size(self):
                return len(self.items)
        """, xp=20),
),

lesson(f"{P}-init", "__init__, атрибуты и значения по умолчанию",
    out(f"{P}-init-e1", "Что выведет программа?", """
        class User:
            def __init__(self, name, role="user"):
                self.name = name
                self.role = role
                self.active = True

        u = User("Аня")
        a = User("Боря", role="admin")
        print(u.name, u.role, u.active)
        print(a.role, vars(a))
        """, hint="vars(объект) — словарь его атрибутов."),
    out(f"{P}-init-e2", "Что выведет программа?", """
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        try:
            Point(1)
        except TypeError as e:
            print(e)
        p = Point(1, 2)
        p.z = 3
        print(p.x, p.y, p.z)
        """, hint="Атрибуты можно добавить объекту и после создания — но лучше описывать всё в __init__."),
    out(f"{P}-init-e3", "Что выведет программа? Список по умолчанию.", """
        class Order:
            def __init__(self, items=None):
                self.items = items if items is not None else []

        a = Order()
        b = Order()
        a.items.append("чай")
        print(a.items, b.items)
        """),
    cod(f"{P}-init-e4", t("""
        Создай класс `Product` с конструктором `Product(name, price, qty=1)`, сохраняющим три атрибута.
        """),
        "",
        """
        def test_product():
            p = Product("чай", 300)
            assert (p.name, p.price, p.qty) == ("чай", 300, 1), "Значения атрибутов"
            assert Product("кофе", 500, 2).qty == 2, "qty передаётся"
        """,
        """
        class Product:
            def __init__(self, name, price, qty=1):
                self.name = name
                self.price = price
                self.qty = qty
        """),
    cod(f"{P}-init-e5", t("""
        Создай класс `Config` с конструктором `Config(host="localhost", port=8080, debug=False)` — все параметры сохраняются в одноимённые атрибуты.
        """),
        "",
        """
        def test_config():
            c = Config()
            assert (c.host, c.port, c.debug) == ("localhost", 8080, False), "Умолчания"
            d = Config(port=5432, debug=True)
            assert (d.host, d.port, d.debug) == ("localhost", 5432, True), "Переданные значения"
        """,
        """
        class Config:
            def __init__(self, host="localhost", port=8080, debug=False):
                self.host = host
                self.port = port
                self.debug = debug
        """),
    cod(f"{P}-init-e6", t("""
        Создай класс `Order` с параметром `items=None`: если список не передан, у каждого заказа должен быть **свой** пустой список (не общий!).
        """),
        "",
        """
        def test_independent():
            a, b = Order(), Order()
            a.items.append("x")
            assert b.items == [], "Списки заказов должны быть независимыми"
            assert Order(["y"]).items == ["y"], "Переданный список сохраняется"
        """,
        """
        class Order:
            def __init__(self, items=None):
                if items is None:
                    items = []
                self.items = items
        """, hint="Список в значении по умолчанию — один на все объекты. Используй None."),
    cod(f"{P}-init-e7", t("""
        Создай класс `Temperature(celsius)`: если температура ниже абсолютного нуля (`-273.15`), конструктор выбрасывает `ValueError("ниже абсолютного нуля")`.
        """),
        "",
        """
        def test_values():
            assert Temperature(20).celsius == 20, "Корректная температура"
            try:
                Temperature(-300)
            except ValueError as e:
                assert str(e) == "ниже абсолютного нуля", f"Текст: {e}"
                return
            assert False, "Нужен ValueError"
        """,
        """
        class Temperature:
            def __init__(self, celsius):
                if celsius < -273.15:
                    raise ValueError("ниже абсолютного нуля")
                self.celsius = celsius
        """),
    cod(f"{P}-init-e8", t("""
        Создай класс `Point(x=0, y=0)`: кроме `x` и `y` в конструкторе вычисли атрибут `distance` — расстояние до начала координат, округлённое до 2 знаков.
        """),
        "",
        """
        def test_values():
            p = Point(3, 4)
            assert (p.x, p.y, p.distance) == (3, 4, 5.0) and Point().distance == 0 and Point(1, 1).distance == 1.41, "Неверные атрибуты"
        """,
        """
        class Point:
            def __init__(self, x=0, y=0):
                self.x = x
                self.y = y
                self.distance = round((x * x + y * y) ** 0.5, 2)
        """),
),

lesson(f"{P}-methods", "Методы и self",
    out(f"{P}-methods-e1", "Что выведет программа? Цепочка вызовов.", """
        class Counter:
            def __init__(self):
                self.value = 0

            def inc(self):
                self.value += 1
                return self

        c = Counter()
        c.inc().inc().inc()
        print(c.value)
        """, hint="Метод вернул сам объект — у результата снова можно вызвать метод."),
    out(f"{P}-methods-e2", "Что выведет программа? Метод вызывает метод.", """
        class Cart:
            def __init__(self):
                self.items = []

            def add(self, name, price):
                self.items.append((name, price))

            def total(self):
                return sum(price for _, price in self.items)

            def summary(self):
                return f"{len(self.items)} товара на {self.total()} ₽"

        c = Cart()
        c.add("чай", 300)
        c.add("кофе", 500)
        print(c.summary())
        """),
    out(f"{P}-methods-e3", "Что выведет программа? Что такое self.", """
        class Greeter:
            def __init__(self, name):
                self.name = name

            def hello(self):
                return f"Привет, {self.name}"

        g = Greeter("Аня")
        print(g.hello(), Greeter.hello(g))
        m = g.hello
        print(m())
        """, hint="g.hello() — то же, что Greeter.hello(g): self — это g."),
    cod(f"{P}-methods-e4", t("""
        Создай класс `Cart` с методами `add(name, price)`, `total()` (сумма цен) и `count()` (количество товаров).
        """),
        "",
        """
        def test_cart():
            c = Cart()
            assert c.total() == 0 and c.count() == 0, "Пустая корзина"
            c.add("чай", 300)
            c.add("кофе", 500)
            assert c.total() == 800 and c.count() == 2, "Корзина с товарами"
        """,
        """
        class Cart:
            def __init__(self):
                self.items = []

            def add(self, name, price):
                self.items.append((name, price))

            def total(self):
                return sum(price for _, price in self.items)

            def count(self):
                return len(self.items)
        """),
    cod(f"{P}-methods-e5", t("""
        Создай класс `Account(balance=0)` с методами `deposit(amount)` и `withdraw(amount)`. Снятие больше баланса — `ValueError("недостаточно средств")`. Оба метода возвращают новый баланс.
        """),
        "",
        """
        def test_account():
            a = Account(100)
            assert a.deposit(50) == 150 and a.withdraw(30) == 120 and a.balance == 120, "Операции"
            try:
                a.withdraw(1000)
            except ValueError as e:
                assert str(e) == "недостаточно средств" and a.balance == 120, "Баланс не меняется при ошибке"
                return
            assert False, "Нужен ValueError"
        """,
        """
        class Account:
            def __init__(self, balance=0):
                self.balance = balance

            def deposit(self, amount):
                self.balance += amount
                return self.balance

            def withdraw(self, amount):
                if amount > self.balance:
                    raise ValueError("недостаточно средств")
                self.balance -= amount
                return self.balance
        """),
    cod(f"{P}-methods-e6", t("""
        Создай класс `TodoList`:

        - `add(task)` — добавить задачу (не выполнена);
        - `done(task)` — отметить выполненной;
        - `pending()` — список невыполненных задач в порядке добавления.
        """),
        "",
        """
        def test_todo():
            t = TodoList()
            t.add("код")
            t.add("тесты")
            t.add("деплой")
            t.done("тесты")
            assert t.pending() == ["код", "деплой"], f"Получено {t.pending()}"
        """,
        """
        class TodoList:
            def __init__(self):
                self.tasks = {}

            def add(self, task):
                self.tasks[task] = False

            def done(self, task):
                self.tasks[task] = True

            def pending(self):
                return [task for task, finished in self.tasks.items() if not finished]
        """),
    cod(f"{P}-methods-e7", t("""
        Создай класс `Counter` с методами `inc(step=1)` и `reset()`, **оба возвращают `self`**, чтобы вызовы можно было цеплять.

        ```
        Counter().inc().inc(5).value            # → 6
        Counter().inc(3).reset().inc().value    # → 1
        ```
        """),
        "",
        """
        def test_chain():
            assert Counter().inc().inc(5).value == 6 and Counter().inc(3).reset().inc().value == 1, "Цепочка вызовов"
        """,
        """
        class Counter:
            def __init__(self):
                self.value = 0

            def inc(self, step=1):
                self.value += step
                return self

            def reset(self):
                self.value = 0
                return self
        """),
    cod(f"{P}-methods-e8", t("""
        Создай класс `TextStats(text)` с методами:

        - `words()` — количество слов;
        - `chars()` — количество символов без пробелов;
        - `most_common()` — самое частое слово в нижнем регистре (при равенстве — встретившееся раньше).
        """),
        "",
        """
        def test_stats():
            s = TextStats("Тест упал тест прошёл")
            assert (s.words(), s.chars(), s.most_common()) == (4, 18, "тест"), f"{s.words()}, {s.chars()}, {s.most_common()}"
        """,
        """
        class TextStats:
            def __init__(self, text):
                self.text = text

            def words(self):
                return len(self.text.split())

            def chars(self):
                return len(self.text.replace(" ", ""))

            def most_common(self):
                words = self.text.lower().split()
                return max(words, key=words.count)
        """, xp=20),
),

lesson(f"{P}-m1-l2", "Атрибуты класса и __str__",
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
    cod(f"{P}-m1-l2-e7", t("""
        Создай класс `User(name)` с методами `__str__` (просто имя) и `__repr__` (вид `User('Аня')`, как в коде).

        ```
        u = User("Аня")
        str(u)    # → "Аня"
        repr(u)   # → "User('Аня')"
        ```
        """),
        "",
        """
        def test_str_repr():
            u = User("Аня")
            assert str(u) == "Аня" and f"{u}" == "Аня" and repr(u) == "User('Аня')" and repr([u]) == "[User('Аня')]", "Неверное представление"
        """,
        """
        class User:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return f"User({self.name!r})"
        """, hint="!r в f-строке добавит кавычки вокруг строки."),
    cod(f"{P}-m1-l2-e8", t("""
        Создай класс `Session` с атрибутом класса `active = 0` — количество открытых сессий. Создание сессии увеличивает счётчик, метод `close()` уменьшает. Повторный `close()` той же сессии счётчик не меняет.
        """),
        "",
        """
        def test_sessions():
            Session.active = 0
            a, b = Session(), Session()
            assert Session.active == 2, "Две сессии"
            a.close()
            a.close()
            assert Session.active == 1, "Повторный close не уменьшает счётчик"
        """,
        """
        class Session:
            active = 0

            def __init__(self):
                self.closed = False
                Session.active += 1

            def close(self):
                if not self.closed:
                    self.closed = True
                    Session.active -= 1
        """, xp=20),
),

lesson(f"{P}-identity", "Объекты, ссылки и копии",
    out(f"{P}-identity-e1", "Что выведет программа?", """
        class Box:
            def __init__(self, value):
                self.value = value

        a = Box(1)
        b = Box(1)
        c = a
        print(a == b, a is b, a is c)
        c.value = 99
        print(a.value)
        """, hint="Без __eq__ два разных объекта не равны, даже с одинаковыми атрибутами."),
    out(f"{P}-identity-e2", "Что выведет программа? Объект в функции.", """
        class User:
            def __init__(self, name):
                self.name = name

        def rename(user):
            user.name = user.name.upper()

        u = User("аня")
        rename(u)
        print(u.name)
        """),
    out(f"{P}-identity-e3", "Что выведет программа? copy и deepcopy.", """
        import copy

        class Team:
            def __init__(self, members):
                self.members = members

        t1 = Team(["Аня"])
        t2 = copy.copy(t1)
        t3 = copy.deepcopy(t1)
        t1.members.append("Боря")
        print(t2.members, t3.members)
        """),
    cod(f"{P}-identity-e4", t("""
        Напиши функцию `clone_user(user)` — новый объект `User` с теми же `name` и `tags` (список), полностью независимый от исходного.
        """),
        """
        class User:
            def __init__(self, name, tags):
                self.name = name
                self.tags = tags

        def clone_user(user):
            pass
        """,
        """
        def test_clone():
            u = User("Аня", ["qa"])
            c = clone_user(u)
            assert c is not u and c.name == "Аня" and c.tags == ["qa"], "Копия с теми же данными"
            c.tags.append("x")
            assert u.tags == ["qa"], "Список тегов должен быть независимым"
        """,
        """
        class User:
            def __init__(self, name, tags):
                self.name = name
                self.tags = tags

        def clone_user(user):
            return User(user.name, list(user.tags))
        """),
    cod(f"{P}-identity-e5", t("""
        Создай класс `Matrix(rows)` (список списков) с методом `copy()` — возвращает новую `Matrix` с полностью независимыми строками.
        """),
        "",
        """
        def test_copy():
            m = Matrix([[1, 2], [3, 4]])
            c = m.copy()
            c.rows[0][0] = 99
            assert m.rows == [[1, 2], [3, 4]] and c.rows[0][0] == 99 and isinstance(c, Matrix), "Строки должны копироваться"
        """,
        """
        class Matrix:
            def __init__(self, rows):
                self.rows = rows

            def copy(self):
                return Matrix([list(row) for row in self.rows])
        """),
    cod(f"{P}-identity-e6", t("""
        Напиши функцию `count_distinct_objects(objs)` — сколько **разных объектов** (а не разных значений) в списке. Используй `id(...)`.

        ```
        b = Box(1)
        count_distinct_objects([b, b, Box(1)])   # → 2
        ```
        """),
        """
        class Box:
            def __init__(self, value):
                self.value = value

        def count_distinct_objects(objs):
            pass
        """,
        """
        def test_values():
            b = Box(1)
            assert count_distinct_objects([b, b, Box(1)]) == 2 and count_distinct_objects([]) == 0, "Неверный подсчёт"
        """,
        """
        class Box:
            def __init__(self, value):
                self.value = value

        def count_distinct_objects(objs):
            return len({id(o) for o in objs})
        """),
    cod(f"{P}-identity-e7", t("""
        Создай класс `Settings(values)` (словарь) с методом `with_value(key, value)` — вернуть **новые** настройки с изменённым ключом; исходный объект не меняется.
        """),
        "",
        """
        def test_immutable():
            s = Settings({"timeout": 30})
            s2 = s.with_value("timeout", 5)
            assert s.values == {"timeout": 30} and s2.values == {"timeout": 5} and s2 is not s, "Исходные настройки не меняются"
        """,
        """
        class Settings:
            def __init__(self, values):
                self.values = values

            def with_value(self, key, value):
                return Settings({**self.values, key: value})
        """),
    cod(f"{P}-identity-e8", t("""
        Исправь класс `Team` из заготовки: он хранит **тот же** список, что передали снаружи, и изменение внешнего списка портит команду. Команда должна хранить собственную копию.
        """),
        """
        class Team:
            def __init__(self, members):
                self.members = members
        """,
        """
        def test_copy():
            names = ["Аня"]
            t = Team(names)
            names.append("Боря")
            assert t.members == ["Аня"], "Команда не должна зависеть от внешнего списка"
        """,
        """
        class Team:
            def __init__(self, members):
                self.members = list(members)
        """),
),
)
