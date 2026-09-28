"""Тема «Классы», модуль 3 «Магия и удобства» — задания. Теория — в _oop_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "oop"

m3 = module(f"{P}-m3", "Магия и удобства", "✨", "Dunder-методы, сравнение и хеш, property, classmethod, dataclass, Page Object",

lesson(f"{P}-m3-l1", "Dunder-методы",
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
    out(f"{P}-m3-l1-e6", "Что выведет программа? __bool__ и __len__.", """
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
        if Flag(False):
            print("включён")
        else:
            print("выключен")
        """, hint="Без __bool__ Python спрашивает __len__: пустой — значит ложь."),
    cod(f"{P}-m3-l1-e7", t("""
        Создай класс `Range2(start, stop)` — свой аналог `range` с шагом 1. Нужны:

        - `__iter__` — чтобы работал `for` (можно вернуть `iter(...)` от списка или использовать `yield`);
        - `__len__`;
        - `__contains__` — проверка `x in r` **без** перебора.
        """),
        "",
        """
        def test_range():
            r = Range2(3, 7)
            assert list(r) == [3, 4, 5, 6] and len(r) == 4 and list(r) == [3, 4, 5, 6], "Итерация и длина (повторная тоже)"
            assert 5 in r and 7 not in r and 2 not in r, "in"
            assert len(Range2(5, 2)) == 0 and list(Range2(5, 2)) == [], "Пустой диапазон"
        """,
        """
        class Range2:
            def __init__(self, start, stop):
                self.start = start
                self.stop = stop

            def __iter__(self):
                current = self.start
                while current < self.stop:
                    yield current
                    current += 1

            def __len__(self):
                return max(0, self.stop - self.start)

            def __contains__(self, x):
                return self.start <= x < self.stop
        """),
    cod(f"{P}-m3-l1-e8", t("""
        Создай класс `Multiplier(k)`, объекты которого можно **вызывать как функцию** (`__call__`):

        ```
        double = Multiplier(2)
        double(21)                        # → 42
        list(map(Multiplier(3), [1, 2]))  # → [3, 6]
        ```

        Также объект считает свои вызовы в атрибуте `calls`.
        """),
        "",
        """
        def test_call():
            d = Multiplier(2)
            assert d(21) == 42 and d(1) == 2 and d.calls == 2, "Вызов и счётчик"
            assert list(map(Multiplier(3), [1, 2])) == [3, 6] and callable(d), "Вызываемый объект"
        """,
        """
        class Multiplier:
            def __init__(self, k):
                self.k = k
                self.calls = 0

            def __call__(self, x):
                self.calls += 1
                return x * self.k
        """, xp=20),
),

lesson(f"{P}-compare", "Сравнение, сортировка и хеш",
    out(f"{P}-compare-e1", "Что выведет программа? __lt__ и сортировка.", """
        class Task:
            def __init__(self, name, priority):
                self.name = name
                self.priority = priority

            def __lt__(self, other):
                return self.priority < other.priority

        tasks = [Task("деплой", 3), Task("баг", 1), Task("ревью", 2)]
        print([t.name for t in sorted(tasks)])
        print(max(tasks).name, Task("a", 1) < Task("b", 2))
        """, hint="sorted, min и max используют оператор <."),
    out(f"{P}-compare-e2", "Что выведет программа? __eq__ без __hash__.", """
        class Point:
            def __init__(self, x, y):
                self.x, self.y = x, y

            def __eq__(self, other):
                return (self.x, self.y) == (other.x, other.y)

        print(Point(1, 2) == Point(1, 2), Point(1, 2) != Point(3, 4))
        try:
            {Point(1, 2)}
        except TypeError as e:
            print(e)
        """, hint="Определив __eq__, класс теряет __hash__ по умолчанию."),
    out(f"{P}-compare-e3", "Что выведет программа? total_ordering.", """
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
        """),
    cod(f"{P}-compare-e4", t("""
        Создай класс `Point(x, y)` с `__eq__` и `__hash__`, чтобы точки можно было класть в множество и использовать как ключи словаря.

        ```
        len({Point(1, 2), Point(1, 2), Point(3, 4)})   # → 2
        ```
        """),
        "",
        """
        def test_hash():
            assert len({Point(1, 2), Point(1, 2), Point(3, 4)}) == 2, "Множество"
            d = {Point(0, 0): "начало"}
            assert d[Point(0, 0)] == "начало" and Point(1, 2) == Point(1, 2) and Point(1, 2) != Point(2, 1), "Ключ словаря"
        """,
        """
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y

            def __eq__(self, other):
                return (self.x, self.y) == (other.x, other.y)

            def __hash__(self):
                return hash((self.x, self.y))
        """, hint="Равные объекты обязаны иметь одинаковый хеш: хешируй тот же кортеж, что сравниваешь."),
    cod(f"{P}-compare-e5", t("""
        Создай класс `Bug(title, severity)`, где `severity` — одно из `"low"`, `"medium"`, `"high"`, `"critical"`. Сделай так, чтобы `sorted(bugs)` упорядочивал баги от самого лёгкого к самому серьёзному. Используй `@total_ordering`, чтобы работали все операторы сравнения.
        """),
        "",
        """
        def test_sort():
            bugs = [Bug("a", "high"), Bug("b", "low"), Bug("c", "critical"), Bug("d", "medium")]
            assert [b.title for b in sorted(bugs)] == ["b", "d", "a", "c"], "Сортировка"
            assert Bug("x", "high") >= Bug("y", "medium") and Bug("x", "low") <= Bug("y", "low") and Bug("x", "low") == Bug("y", "low"), "Операторы"
        """,
        """
        from functools import total_ordering

        LEVELS = ["low", "medium", "high", "critical"]


        @total_ordering
        class Bug:
            def __init__(self, title, severity):
                self.title = title
                self.severity = severity

            def rank(self):
                return LEVELS.index(self.severity)

            def __eq__(self, other):
                return self.rank() == other.rank()

            def __lt__(self, other):
                return self.rank() < other.rank()
        """),
    cod(f"{P}-compare-e6", t("""
        Классы менять нельзя: у `User` нет операторов сравнения. Напиши функцию `sort_users(users)` — отсортировать по возрасту по убыванию, при равенстве — по имени по алфавиту. Вернуть список имён.
        """),
        """
        class User:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        def sort_users(users):
            pass
        """,
        """
        def test_values():
            us = [User("Вика", 25), User("Аня", 30), User("Боря", 25)]
            assert sort_users(us) == ["Аня", "Боря", "Вика"] and sort_users([]) == [], f"Получено {sort_users(us)}"
        """,
        """
        class User:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        def sort_users(users):
            return [u.name for u in sorted(users, key=lambda u: (-u.age, u.name))]
        """, hint="key=lambda u: (-u.age, u.name)"),
    cod(f"{P}-compare-e7", t("""
        Создай класс `Money(amount, currency)`: `__eq__` сравнивает и сумму, и валюту, а `__lt__` при разных валютах выбрасывает `ValueError("разные валюты")`. Сравнение с объектом другого типа через `==` должно давать `False` (верни `NotImplemented`).
        """),
        "",
        """
        def test_money():
            assert Money(5, "RUB") == Money(5, "RUB") and Money(5, "RUB") != Money(5, "USD") and Money(5, "RUB") != 5, "=="
            assert Money(1, "RUB") < Money(2, "RUB"), "<"
            try:
                Money(1, "RUB") < Money(2, "USD")
            except ValueError as e:
                assert str(e) == "разные валюты", str(e)
                return
            assert False, "Нужен ValueError"
        """,
        """
        class Money:
            def __init__(self, amount, currency):
                self.amount = amount
                self.currency = currency

            def __eq__(self, other):
                if not isinstance(other, Money):
                    return NotImplemented
                return (self.amount, self.currency) == (other.amount, other.currency)

            def __lt__(self, other):
                if self.currency != other.currency:
                    raise ValueError("разные валюты")
                return self.amount < other.amount
        """),
    cod(f"{P}-compare-e8", t("""
        Напиши функцию `unique_users(users)` — убрать дубликаты: два пользователя одинаковые, если у них одинаковый `email` **без учёта регистра**. Сохранить первое вхождение. Для этого добавь в `User` методы `__eq__` и `__hash__`.
        """),
        """
        class User:
            def __init__(self, name, email):
                self.name = name
                self.email = email

        def unique_users(users):
            pass
        """,
        """
        def test_values():
            us = [User("Аня", "A@x.ru"), User("Аня2", "a@X.ru"), User("Боря", "b@x.ru")]
            r = unique_users(us)
            assert [u.name for u in r] == ["Аня", "Боря"], [u.name for u in r]
            assert User("x", "Q@q.ru") == User("y", "q@q.RU") and len({User("x", "a@a"), User("y", "A@A")}) == 1, "__eq__ и __hash__"
        """,
        """
        class User:
            def __init__(self, name, email):
                self.name = name
                self.email = email

            def __eq__(self, other):
                return self.email.lower() == other.email.lower()

            def __hash__(self):
                return hash(self.email.lower())

        def unique_users(users):
            seen = set()
            result = []
            for u in users:
                if u not in seen:
                    seen.add(u)
                    result.append(u)
            return result
        """, xp=20),
),

lesson(f"{P}-m3-l2", "property, classmethod, staticmethod",
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
    out(f"{P}-m3-l2-e6", "Что выведет программа? Свойство только для чтения.", """
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
        """, hint="Свойство без setter нельзя присвоить."),
    out(f"{P}-m3-l2-e7", "Что выведет программа? classmethod и staticmethod.", """
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
        """),
    cod(f"{P}-m3-l2-e8", t("""
        Создай класс `Password(value)` со свойством `value`:

        - setter проверяет длину: меньше 8 символов — `ValueError("слишком короткий")`;
        - getter возвращает `"*" * длина` (сам пароль наружу не показываем);
        - метод `check(guess)` → `True`, если совпадает.

        Проверка работает и в конструкторе, и при присваивании `p.value = ...`.
        """),
        "",
        """
        def test_password():
            p = Password("secret123")
            assert p.value == "*********" and p.check("secret123") and not p.check("x"), "getter и check"
            p.value = "newpassword"
            assert p.check("newpassword"), "setter"
            for bad in [lambda: Password("123"), lambda: setattr(p, "value", "short")]:
                try:
                    bad()
                except ValueError as e:
                    assert str(e) == "слишком короткий", str(e)
                else:
                    assert False, "Нужен ValueError"
            assert p.check("newpassword"), "Неудачное присваивание не меняет пароль"
        """,
        """
        class Password:
            def __init__(self, value):
                self.value = value

            @property
            def value(self):
                return "*" * len(self._value)

            @value.setter
            def value(self, new):
                if len(new) < 8:
                    raise ValueError("слишком короткий")
                self._value = new

            def check(self, guess):
                return guess == self._value
        """),
    cod(f"{P}-m3-l2-e9", t("""
        Создай класс `Color(r, g, b)` с альтернативными конструкторами-`classmethod`:

        - `Color.from_hex("#ff8000")` → `Color(255, 128, 0)`;
        - `Color.gray(v)` → `Color(v, v, v)`.

        И `staticmethod` `Color.clamp(x)` — ограничить число диапазоном 0…255. Конструктор применяет `clamp` к каждому каналу.
        """),
        "",
        """
        def test_color():
            c = Color.from_hex("#ff8000")
            assert (c.r, c.g, c.b) == (255, 128, 0) and isinstance(c, Color), "from_hex"
            g = Color.gray(300)
            assert (g.r, g.g, g.b) == (255, 255, 255), "gray + clamp"
            assert Color.clamp(-5) == 0 and Color.clamp(100) == 100, "clamp"
        """,
        """
        class Color:
            def __init__(self, r, g, b):
                self.r = Color.clamp(r)
                self.g = Color.clamp(g)
                self.b = Color.clamp(b)

            @classmethod
            def from_hex(cls, code):
                code = code.lstrip("#")
                return cls(int(code[0:2], 16), int(code[2:4], 16), int(code[4:6], 16))

            @classmethod
            def gray(cls, v):
                return cls(v, v, v)

            @staticmethod
            def clamp(x):
                return max(0, min(255, x))
        """, hint="int('ff', 16) == 255"),
    cod(f"{P}-m3-l2-e10", t("""
        Создай класс `Rectangle(width, height)` с вычисляемыми свойствами (`@property`) `area` и `is_square`. Свойство `width` — с setter: отрицательная ширина → `ValueError`.
        """),
        "",
        """
        def test_rect():
            r = Rectangle(2, 3)
            assert r.area == 6 and not r.is_square, "area и is_square"
            r.width = 3
            assert r.area == 9 and r.is_square, "После изменения ширины"
            try:
                r.width = -1
            except ValueError:
                assert r.width == 3, "Ширина не меняется"
                return
            assert False, "Нужен ValueError"
        """,
        """
        class Rectangle:
            def __init__(self, width, height):
                self.width = width
                self.height = height

            @property
            def width(self):
                return self._width

            @width.setter
            def width(self, value):
                if value < 0:
                    raise ValueError("отрицательная ширина")
                self._width = value

            @property
            def area(self):
                return self.width * self.height

            @property
            def is_square(self):
                return self.width == self.height
        """, xp=20),
),

lesson(f"{P}-dataclass", "dataclass",
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
    out(f"{P}-dataclass-e1", "Что выведет программа? Значения по умолчанию и field.", """
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
        """, hint="default_factory создаёт новый список для каждого объекта."),
    out(f"{P}-dataclass-e2", "Что выведет программа? frozen и order.", """
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
        """),
    out(f"{P}-dataclass-e3", "Что выведет программа? asdict и replace.", """
        from dataclasses import dataclass, asdict, replace

        @dataclass
        class User:
            name: str
            age: int

        u = User("Аня", 30)
        u2 = replace(u, age=31)
        print(asdict(u), u2)
        print(u == User("Аня", 30), u == u2)
        """),
    cod(f"{P}-dataclass-e5", t("""
        Опиши `@dataclass` `Range(start: int, stop: int)`. В `__post_init__` проверь: если `start > stop`, выбросить `ValueError("start > stop")`. Добавь свойство `length`.
        """),
        "",
        """
        def test_range():
            assert Range(2, 5).length == 3 and Range(1, 1).length == 0, "length"
            try:
                Range(5, 2)
            except ValueError as e:
                assert str(e) == "start > stop", str(e)
                return
            assert False, "Нужен ValueError"
        """,
        """
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
        """),
    cod(f"{P}-dataclass-e6", t("""
        Опиши неизменяемый (`frozen=True`) `@dataclass` `Coord(lat: float, lon: float)`. Напиши функцию `unique_coords(coords)` — количество разных точек (frozen-dataclass можно класть в множество).
        """),
        "",
        """
        def test_coords():
            cs = [Coord(55.7, 37.6), Coord(55.7, 37.6), Coord(59.9, 30.3)]
            assert unique_coords(cs) == 2 and unique_coords([]) == 0, "Подсчёт"
            try:
                cs[0].lat = 0
            except AttributeError:
                return
            assert False, "Coord должен быть frozen"
        """,
        """
        from dataclasses import dataclass


        @dataclass(frozen=True)
        class Coord:
            lat: float
            lon: float


        def unique_coords(coords):
            return len(set(coords))
        """, hint="FrozenInstanceError — наследник AttributeError."),
    cod(f"{P}-dataclass-e7", t("""
        Опиши `@dataclass(order=True)` `Task` с полями `priority: int` и `title: str`. Напиши функцию `plan(tasks)` — названия задач по возрастанию приоритета (при равном — по алфавиту). Используй встроенное сравнение dataclass, без `key=`.
        """),
        "",
        """
        def test_plan():
            ts = [Task(2, "ревью"), Task(1, "баг"), Task(2, "деплой")]
            assert plan(ts) == ["баг", "деплой", "ревью"] and plan([]) == [], f"Получено {plan(ts)}"
            assert "key=" not in open("solution.py", encoding="utf-8").read(), "Без key="
        """,
        """
        from dataclasses import dataclass


        @dataclass(order=True)
        class Task:
            priority: int
            title: str


        def plan(tasks):
            return [t.title for t in sorted(tasks)]
        """, hint="order=True сравнивает объекты как кортежи полей по порядку."),
    cod(f"{P}-dataclass-e8", t("""
        Напиши функцию `users_from_json(data)` — принимает список словарей `{"name": ..., "age": ...}` (лишние ключи игнорировать) и возвращает список объектов `@dataclass User(name: str, age: int)`. Также функцию `users_to_json(users)` — обратно в список словарей (используй `asdict`).
        """),
        "",
        """
        def test_roundtrip():
            data = [{"name": "Аня", "age": 30, "extra": 1}, {"name": "Боря", "age": 25}]
            us = users_from_json(data)
            assert us == [User("Аня", 30), User("Боря", 25)], "users_from_json"
            assert users_to_json(us) == [{"name": "Аня", "age": 30}, {"name": "Боря", "age": 25}], "users_to_json"
        """,
        """
        from dataclasses import dataclass, asdict


        @dataclass
        class User:
            name: str
            age: int


        def users_from_json(data):
            return [User(d["name"], d["age"]) for d in data]


        def users_to_json(users):
            return [asdict(u) for u in users]
        """, xp=20),
),

lesson(f"{P}-pom", "Практика: классы в автотестах",
    out(f"{P}-pom-e1", "Что выведет программа? Page Object.", """
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

        d = FakeDriver()
        LoginPage(d).login("anna", "123")
        for a in d.actions:
            print(a)
        """, hint="Page Object прячет селекторы внутри класса страницы — тест вызывает только login()."),
    out(f"{P}-pom-e2", "Что выведет программа? API-клиент.", """
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
        print(ApiClient("http://x").headers())
        """),
    out(f"{P}-pom-e3", "Что выведет программа? Наследование страниц.", """
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
        """),
    cod(f"{P}-pom-e4", t("""
        Создай Page Object `SearchPage(driver)`:

        - селекторы — атрибуты класса `INPUT = "#q"`, `BUTTON = "#go"`;
        - метод `search(text)` — вызвать `driver.type(INPUT, text)` и `driver.click(BUTTON)`, вернуть `self`;
        - метод `results()` — вернуть `driver.find_all(".result")`.
        """),
        "",
        """
        def test_page():
            class D:
                def __init__(self):
                    self.log = []
                def type(self, s, t):
                    self.log.append(("type", s, t))
                def click(self, s):
                    self.log.append(("click", s))
                def find_all(self, s):
                    return [s + "1", s + "2"]
            d = D()
            page = SearchPage(d)
            assert page.search("python") is page, "search возвращает self"
            assert d.log == [("type", "#q", "python"), ("click", "#go")], f"Действия: {d.log}"
            assert page.results() == [".result1", ".result2"] and SearchPage.INPUT == "#q", "results и селекторы"
        """,
        """
        class SearchPage:
            INPUT = "#q"
            BUTTON = "#go"

            def __init__(self, driver):
                self.driver = driver

            def search(self, text):
                self.driver.type(self.INPUT, text)
                self.driver.click(self.BUTTON)
                return self

            def results(self):
                return self.driver.find_all(".result")
        """),
    cod(f"{P}-pom-e5", t("""
        Создай класс `ApiClient(base_url, session)`. `session` — объект с методом `request(method, url, json=None)`, который возвращает словарь-ответ. Методы клиента:

        - `get(path)` и `post(path, data)` — вызывают `session.request` с методом `"GET"`/`"POST"` и полным адресом (`base_url` без завершающего `/` + `path`);
        - `get_user(user_id)` — `get(f"/users/{user_id}")`.
        """),
        "",
        """
        def test_client():
            class S:
                def __init__(self):
                    self.calls = []
                def request(self, method, url, json=None):
                    self.calls.append((method, url, json))
                    return {"ok": True}
            s = S()
            c = ApiClient("https://api.test/", s)
            assert c.get_user(7) == {"ok": True}, "Ответ сессии"
            c.post("/users", {"name": "Аня"})
            assert s.calls == [("GET", "https://api.test/users/7", None), ("POST", "https://api.test/users", {"name": "Аня"})], f"Вызовы: {s.calls}"
        """,
        """
        class ApiClient:
            def __init__(self, base_url, session):
                self.base_url = base_url.rstrip("/")
                self.session = session

            def get(self, path):
                return self.session.request("GET", self.base_url + path)

            def post(self, path, data):
                return self.session.request("POST", self.base_url + path, json=data)

            def get_user(self, user_id):
                return self.get(f"/users/{user_id}")
        """),
    cod(f"{P}-pom-e6", t("""
        Создай класс `UserFactory` — генератор тестовых пользователей:

        - `create(**overrides)` — вернуть словарь `{"id": N, "name": "user_N", "email": "user_N@test.ru", "active": True}`, где `N` — порядковый номер (1, 2, 3… — **у каждой фабрики свой** счётчик); любые поля можно переопределить через `overrides`;
        - `create_many(n)` — список из `n` пользователей.
        """),
        "",
        """
        def test_factory():
            f = UserFactory()
            assert f.create() == {"id": 1, "name": "user_1", "email": "user_1@test.ru", "active": True}, "Первый"
            assert f.create(active=False)["active"] is False, "overrides"
            many = f.create_many(2)
            assert [u["id"] for u in many] == [3, 4], "Номера продолжаются"
            assert UserFactory().create()["id"] == 1, "У новой фабрики свой счётчик"
        """,
        """
        class UserFactory:
            def __init__(self):
                self.counter = 0

            def create(self, **overrides):
                self.counter += 1
                n = self.counter
                user = {"id": n, "name": f"user_{n}", "email": f"user_{n}@test.ru", "active": True}
                user.update(overrides)
                return user

            def create_many(self, n):
                return [self.create() for _ in range(n)]
        """),
    cod(f"{P}-pom-e7", t("""
        Создай класс `Response(status, body)` с удобными методами для проверок:

        - свойство `ok` — `True`, если статус 200–299;
        - `json()` — вернуть `body`;
        - `assert_status(expected)` — при несовпадении `AssertionError(f"ожидали {expected}, получили {status}")`, иначе вернуть `self` (чтобы цеплять вызовы);
        - `assert_has(key)` — `AssertionError(f"нет поля {key}")`, если ключа нет в body; иначе `self`.
        """),
        "",
        """
        def test_response():
            r = Response(201, {"id": 1})
            assert r.ok and not Response(404, {}).ok and r.json() == {"id": 1}, "ok и json"
            assert r.assert_status(201).assert_has("id") is r, "Цепочка"
            for call, msg in [(lambda: r.assert_status(200), "ожидали 200, получили 201"), (lambda: r.assert_has("name"), "нет поля name")]:
                try:
                    call()
                except AssertionError as e:
                    assert str(e) == msg, str(e)
                else:
                    assert False, "Нужен AssertionError"
        """,
        """
        class Response:
            def __init__(self, status, body):
                self.status = status
                self.body = body

            @property
            def ok(self):
                return 200 <= self.status < 300

            def json(self):
                return self.body

            def assert_status(self, expected):
                if self.status != expected:
                    raise AssertionError(f"ожидали {expected}, получили {self.status}")
                return self

            def assert_has(self, key):
                if key not in self.body:
                    raise AssertionError(f"нет поля {key}")
                return self
        """),
    cod(f"{P}-pom-e8", t("""
        Создай класс `FakeUserApi` — подделку API для тестов (хранит пользователей в словаре):

        - `create(name)` → словарь `{"id": N, "name": name}` (id с 1), пустое имя — `ValueError("пустое имя")`;
        - `get(user_id)` → пользователь или `None`;
        - `delete(user_id)` → `True`, если удалён, иначе `False`;
        - `count()` — сколько пользователей сейчас.

        id не переиспользуются после удаления.
        """),
        "",
        """
        def test_fake_api():
            api = FakeUserApi()
            a = api.create("Аня")
            b = api.create("Боря")
            assert a == {"id": 1, "name": "Аня"} and b["id"] == 2 and api.get(1) == a and api.get(9) is None, "create/get"
            assert api.delete(1) is True and api.delete(1) is False and api.count() == 1, "delete/count"
            assert api.create("Вика")["id"] == 3, "id не переиспользуются"
            try:
                api.create("")
            except ValueError as e:
                assert str(e) == "пустое имя", str(e)
                return
            assert False, "Нужен ValueError"
        """,
        """
        class FakeUserApi:
            def __init__(self):
                self.users = {}
                self.next_id = 1

            def create(self, name):
                if not name:
                    raise ValueError("пустое имя")
                user = {"id": self.next_id, "name": name}
                self.users[self.next_id] = user
                self.next_id += 1
                return user

            def get(self, user_id):
                return self.users.get(user_id)

            def delete(self, user_id):
                return self.users.pop(user_id, None) is not None

            def count(self):
                return len(self.users)
        """, xp=25),
),
)
