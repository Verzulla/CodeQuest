"""Тема «Декораторы», модуль 3 «Продвинутые декораторы» — задания. Теория — в _dec_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "dec"

m3 = module(f"{P}-m3", "Продвинутые декораторы", "🧙", "Декораторы с параметрами, несколько декораторов, методы и классы, декораторы в тестах",

lesson(f"{P}-params", "Декораторы с параметрами",
    out(f"{P}-params-e1", "Что выведет программа?", """
        from functools import wraps

        def repeat(times):
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    return [func(*args, **kwargs) for _ in range(times)]
                return wrapper
            return decorator

        @repeat(3)
        def hello(name):
            return f"hi {name}"

        print(hello("аня"))
        print(hello.__name__)
        """, hint="repeat(3) возвращает декоратор, и уже он применяется к hello."),
    out(f"{P}-params-e2", "Что выведет программа? Префикс в логе.", """
        from functools import wraps

        def tag(label):
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    return f"[{label}] {func(*args, **kwargs)}"
                return wrapper
            return decorator

        @tag("API")
        def get_user():
            return "Аня"

        @tag("DB")
        def save():
            return "сохранено"

        print(get_user())
        print(save())
        """),
    out(f"{P}-params-e3", "Что выведет программа? Без синтаксиса @.", """
        from functools import wraps

        def multiply(k):
            def decorator(func):
                @wraps(func)
                def wrapper(x):
                    return func(x) * k
                return wrapper
            return decorator

        def inc(x):
            return x + 1

        decorator = multiply(10)
        f = decorator(inc)
        g = multiply(2)(inc)
        print(f(1), g(1), inc(1))
        """, hint="@multiply(10) — то же, что inc = multiply(10)(inc)."),
    cod(f"{P}-params-e4", t("""
        Напиши декоратор с параметром `repeat(times)`: функция вызывается `times` раз, возвращается **последний** результат.
        """),
        """
        def repeat(times):
            pass
        """,
        """
        def test_values():
            calls = []
            @repeat(3)
            def f(x):
                calls.append(x)
                return len(calls)
            assert f("a") == 3 and calls == ["a", "a", "a"] and f.__name__ == "f", "Три вызова"
        """,
        """
        from functools import wraps


        def repeat(times):
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    result = None
                    for _ in range(times):
                        result = func(*args, **kwargs)
                    return result
                return wrapper
            return decorator
        """),
    cod(f"{P}-params-e5", t("""
        Напиши декоратор `retry(times, exceptions)`: повторять вызов до `times` раз, если функция выбрасывает исключение из кортежа `exceptions`. Остальные ошибки — сразу пробрасывать. Если попытки кончились — пробросить последнюю ошибку.

        ```
        @retry(times=3, exceptions=(ConnectionError, TimeoutError))
        def request(): ...
        ```
        """),
        """
        def retry(times, exceptions):
            pass
        """,
        """
        def test_values():
            state = {"n": 0}
            @retry(times=4, exceptions=(ConnectionError, TimeoutError))
            def flaky():
                state["n"] += 1
                if state["n"] == 1:
                    raise ConnectionError
                if state["n"] == 2:
                    raise TimeoutError
                return "ok"
            assert flaky() == "ok" and state["n"] == 3, "Повторы"
            state["n"] = 0
            @retry(times=2, exceptions=(ConnectionError,))
            def dead():
                state["n"] += 1
                raise ConnectionError
            try:
                dead()
            except ConnectionError:
                assert state["n"] == 2, "Ровно times попыток"
            state["n"] = 0
            @retry(times=5, exceptions=(ConnectionError,))
            def wrong():
                state["n"] += 1
                raise ValueError
            try:
                wrong()
            except ValueError:
                assert state["n"] == 1, "Чужие ошибки не повторяются"
                return
            assert False, "ValueError должен пробрасываться"
        """,
        """
        from functools import wraps


        def retry(times, exceptions):
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    for attempt in range(times):
                        try:
                            return func(*args, **kwargs)
                        except exceptions:
                            if attempt == times - 1:
                                raise
                return wrapper
            return decorator
        """),
    cod(f"{P}-params-e6", t("""
        Напиши декоратор `validate_range(low, high)`: все **позиционные** аргументы должны быть в диапазоне `low…high` включительно, иначе — `ValueError(f"{значение} вне [{low}, {high}]")`.
        """),
        """
        def validate_range(low, high):
            pass
        """,
        """
        def test_values():
            @validate_range(1, 10)
            def add(a, b):
                return a + b
            assert add(1, 10) == 11, "Граничные значения"
            try:
                add(5, 11)
            except ValueError as e:
                assert str(e) == "11 вне [1, 10]", str(e)
                return
            assert False, "Нужен ValueError"
        """,
        """
        from functools import wraps


        def validate_range(low, high):
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    for a in args:
                        if not low <= a <= high:
                            raise ValueError(f"{a} вне [{low}, {high}]")
                    return func(*args, **kwargs)
                return wrapper
            return decorator
        """),
    cod(f"{P}-params-e7", t("""
        Напиши декоратор `expect_type(t)`: если результат функции — не экземпляр типа `t`, выбросить `TypeError(f"ожидали {t.__name__}, получили {тип результата}")`.

        ```
        @expect_type(int)
        def f(): return "5"
        f()   # TypeError: ожидали int, получили str
        ```
        """),
        """
        def expect_type(t):
            pass
        """,
        """
        def test_values():
            @expect_type(int)
            def good():
                return 5
            @expect_type(dict)
            def bad():
                return [1]
            assert good() == 5, "Верный тип"
            try:
                bad()
            except TypeError as e:
                assert str(e) == "ожидали dict, получили list", str(e)
                return
            assert False, "Нужен TypeError"
        """,
        """
        from functools import wraps


        def expect_type(t):
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    result = func(*args, **kwargs)
                    if not isinstance(result, t):
                        raise TypeError(f"ожидали {t.__name__}, получили {type(result).__name__}")
                    return result
                return wrapper
            return decorator
        """),
    cod(f"{P}-params-e8", t("""
        Напиши декоратор `limit_calls(n)`: функцию можно вызвать не больше `n` раз; следующий вызов — `RuntimeError(f"{имя}: лимит {n} вызовов")`. У каждой задекорированной функции свой счётчик.
        """),
        """
        def limit_calls(n):
            pass
        """,
        """
        def test_values():
            @limit_calls(2)
            def ping():
                return "pong"
            @limit_calls(1)
            def other():
                return 1
            assert ping() == "pong" and ping() == "pong" and other() == 1, "Разрешённые вызовы"
            try:
                ping()
            except RuntimeError as e:
                assert str(e) == "ping: лимит 2 вызовов", str(e)
                return
            assert False, "Нужен RuntimeError"
        """,
        """
        from functools import wraps


        def limit_calls(n):
            def decorator(func):
                count = 0

                @wraps(func)
                def wrapper(*args, **kwargs):
                    nonlocal count
                    if count >= n:
                        raise RuntimeError(f"{func.__name__}: лимит {n} вызовов")
                    count += 1
                    return func(*args, **kwargs)
                return wrapper
            return decorator
        """, xp=20),
),

lesson(f"{P}-stack", "Несколько декораторов",
    out(f"{P}-stack-e1", "Что выведет программа? Порядок применения.", """
        def bold(func):
            def wrapper():
                return "<b>" + func() + "</b>"
            return wrapper

        def italic(func):
            def wrapper():
                return "<i>" + func() + "</i>"
            return wrapper

        @bold
        @italic
        def text():
            return "привет"

        print(text())
        """, hint="Ближний к функции декоратор применяется первым: text = bold(italic(text))."),
    out(f"{P}-stack-e2", "Что выведет программа? Порядок выполнения.", """
        def trace(name):
            def decorator(func):
                def wrapper():
                    print("вход", name)
                    result = func()
                    print("выход", name)
                    return result
                return wrapper
            return decorator

        @trace("A")
        @trace("B")
        def work():
            print("работа")
            return 1

        print(work())
        """, hint="Как матрёшка: внешняя обёртка входит первой и выходит последней."),
    out(f"{P}-stack-e3", "Что выведет программа? Порядок важен.", """
        def add_one(func):
            def wrapper():
                return func() + 1
            return wrapper

        def double(func):
            def wrapper():
                return func() * 2
            return wrapper

        @add_one
        @double
        def five():
            return 5

        @double
        @add_one
        def five2():
            return 5

        print(five(), five2())
        """),
    cod(f"{P}-stack-e4", t("""
        Есть декораторы `strip` (убирает пробелы по краям у результата) и `upper` (переводит результат в верхний регистр). Примени **оба** к функции `get_name()` через `@` так, чтобы она возвращала `"АНЯ"`.
        """),
        """
        def strip(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs).strip()
            return wrapper


        def upper(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs).upper()
            return wrapper


        def get_name():
            return "  аня  "
        """,
        """
        def test_values():
            assert get_name() == "АНЯ", f"Получено {get_name()!r}"
            assert get_name.__name__ == "wrapper", "Функция должна быть задекорирована"
        """,
        """
        def strip(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs).strip()
            return wrapper


        def upper(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs).upper()
            return wrapper


        @strip
        @upper
        def get_name():
            return "  аня  "
        """, hint="Здесь порядок не важен — но оба декоратора нужны."),
    cod(f"{P}-stack-e5", t("""
        Есть декораторы `add_prefix` (добавляет `"> "` в начало результата) и `limit10` (обрезает результат до 10 символов). Функция `message()` должна возвращать `"> Длинное со"`: сначала обрезать до 10, **потом** добавить префикс. Расставь декораторы в правильном порядке.
        """),
        """
        def add_prefix(func):
            def wrapper():
                return "> " + func()
            return wrapper


        def limit10(func):
            def wrapper():
                return func()[:10]
            return wrapper


        def message():
            return "Длинное сообщение об ошибке"
        """,
        """
        def test_values():
            assert message() == "> Длинное со", f"Получено {message()!r}"
        """,
        """
        def add_prefix(func):
            def wrapper():
                return "> " + func()
            return wrapper


        def limit10(func):
            def wrapper():
                return func()[:10]
            return wrapper


        @add_prefix
        @limit10
        def message():
            return "Длинное сообщение об ошибке"
        """, hint="Ближний к def декоратор работает с результатом функции первым."),
    cod(f"{P}-stack-e6", t("""
        Напиши функцию `apply_decorators(func, *decorators)` — применить декораторы так же, как если бы они были записаны через `@` **в указанном порядке сверху вниз**.

        ```
        apply_decorators(f, bold, italic)   # то же, что bold(italic(f))
        ```
        """),
        """
        def apply_decorators(func, *decorators):
            pass
        """,
        """
        def test_values():
            def bold(f):
                return lambda: "<b>" + f() + "</b>"
            def italic(f):
                return lambda: "<i>" + f() + "</i>"
            text = lambda: "x"
            assert apply_decorators(text, bold, italic)() == "<b><i>x</i></b>" and apply_decorators(text)() == "x", "Неверный порядок"
        """,
        """
        def apply_decorators(func, *decorators):
            for deco in reversed(decorators):
                func = deco(func)
            return func
        """),
    cod(f"{P}-stack-e7", t("""
        Напиши декоратор `record(name)`: при вызове функции добавляет `name` в глобальный список `ORDER` **до** вызова функции и `"/" + name` — **после**. Затем задекорируй `work()` так, чтобы после вызова `ORDER` был `["auth", "log", "work", "/log", "/auth"]` (функция `work` сама добавляет `"work"`).
        """),
        """
        ORDER = []


        def record(name):
            pass


        def work():
            ORDER.append("work")
        """,
        """
        def test_values():
            ORDER.clear()
            work()
            assert ORDER == ["auth", "log", "work", "/log", "/auth"], ORDER
        """,
        """
        from functools import wraps

        ORDER = []


        def record(name):
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    ORDER.append(name)
                    result = func(*args, **kwargs)
                    ORDER.append("/" + name)
                    return result
                return wrapper
            return decorator


        @record("auth")
        @record("log")
        def work():
            ORDER.append("work")
        """),
    cod(f"{P}-stack-e8", t("""
        Напиши декоратор `require_auth` (если первый аргумент `user` — `None`, выбросить `PermissionError("нужен вход")`) и декоратор `log_calls` (добавляет имя функции в глобальный `CALLS` при каждом вызове). Задекорируй `delete_item(user, item_id)` так, чтобы вызов без пользователя **не попадал** в `CALLS`, а успешный — попадал. Оба декоратора — с `@wraps`.
        """),
        """
        CALLS = []


        def require_auth(func):
            pass


        def log_calls(func):
            pass


        def delete_item(user, item_id):
            return f"{user} удалил {item_id}"
        """,
        """
        def test_values():
            CALLS.clear()
            assert delete_item("аня", 5) == "аня удалил 5" and CALLS == ["delete_item"], "Успешный вызов логируется"
            try:
                delete_item(None, 5)
            except PermissionError as e:
                assert str(e) == "нужен вход" and CALLS == ["delete_item"], f"Неавторизованный вызов не логируется: {CALLS}"
                return
            assert False, "Нужен PermissionError"
        """,
        """
        from functools import wraps

        CALLS = []


        def require_auth(func):
            @wraps(func)
            def wrapper(user, *args, **kwargs):
                if user is None:
                    raise PermissionError("нужен вход")
                return func(user, *args, **kwargs)
            return wrapper


        def log_calls(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                CALLS.append(func.__name__)
                return func(*args, **kwargs)
            return wrapper


        @require_auth
        @log_calls
        def delete_item(user, item_id):
            return f"{user} удалил {item_id}"
        """, xp=20),
),

lesson(f"{P}-methods", "Декораторы для методов и классы-декораторы",
    out(f"{P}-methods-e1", "Что выведет программа? Декоратор на методе.", """
        from functools import wraps

        def log(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print("вызов", func.__name__, "аргументов:", len(args))
                return func(*args, **kwargs)
            return wrapper

        class Cart:
            def __init__(self):
                self.items = []

            @log
            def add(self, item):
                self.items.append(item)

        c = Cart()
        c.add("чай")
        print(c.items)
        """, hint="self попадает в args первым."),
    out(f"{P}-methods-e2", "Что выведет программа? Класс как декоратор.", """
        class CountCalls:
            def __init__(self, func):
                self.func = func
                self.calls = 0

            def __call__(self, *args, **kwargs):
                self.calls += 1
                return self.func(*args, **kwargs)

        @CountCalls
        def hello(name):
            return f"hi {name}"

        print(hello("аня"), hello("боря"))
        print(hello.calls, type(hello).__name__)
        """, hint="@CountCalls — то же, что hello = CountCalls(hello). Вызов объекта — __call__."),
    out(f"{P}-methods-e3", "Что выведет программа? Декоратор класса.", """
        def add_repr(cls):
            def __repr__(self):
                fields = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
                return f"{cls.__name__}({fields})"
            cls.__repr__ = __repr__
            return cls

        @add_repr
        class User:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        print(User("Аня", 30))
        """, hint="Декоратор может принимать и возвращать класс — так работает @dataclass."),
    cod(f"{P}-methods-e4", t("""
        Напиши декоратор `check_positive` для методов: второй аргумент (первый после `self`) должен быть больше нуля, иначе `ValueError("сумма должна быть > 0")`. Примени его к методам `deposit` и `withdraw` класса `Account`.
        """),
        """
        def check_positive(func):
            pass


        class Account:
            def __init__(self):
                self.balance = 0

            def deposit(self, amount):
                self.balance += amount

            def withdraw(self, amount):
                self.balance -= amount
        """,
        """
        def test_values():
            a = Account()
            a.deposit(100)
            a.withdraw(30)
            assert a.balance == 70, "Операции"
            for call in [lambda: a.deposit(-5), lambda: a.withdraw(0)]:
                try:
                    call()
                except ValueError as e:
                    assert str(e) == "сумма должна быть > 0", str(e)
                else:
                    assert False, "Нужен ValueError"
            assert a.balance == 70, "Баланс не меняется"
        """,
        """
        from functools import wraps


        def check_positive(func):
            @wraps(func)
            def wrapper(self, amount, *args, **kwargs):
                if amount <= 0:
                    raise ValueError("сумма должна быть > 0")
                return func(self, amount, *args, **kwargs)
            return wrapper


        class Account:
            def __init__(self):
                self.balance = 0

            @check_positive
            def deposit(self, amount):
                self.balance += amount

            @check_positive
            def withdraw(self, amount):
                self.balance -= amount
        """),
    cod(f"{P}-methods-e5", t("""
        Напиши декоратор `log_method` для методов: добавляет в список `self.history` (он есть у объекта) имя вызванного метода. Примени его к `open` и `close` класса `Door`.
        """),
        """
        def log_method(func):
            pass


        class Door:
            def __init__(self):
                self.history = []
                self.is_open = False

            def open(self):
                self.is_open = True

            def close(self):
                self.is_open = False
        """,
        """
        def test_values():
            d = Door()
            d.open()
            d.close()
            d.open()
            assert d.history == ["open", "close", "open"] and d.is_open, d.history
            assert Door().history == [], "У каждой двери своя история"
        """,
        """
        from functools import wraps


        def log_method(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                self.history.append(func.__name__)
                return func(self, *args, **kwargs)
            return wrapper


        class Door:
            def __init__(self):
                self.history = []
                self.is_open = False

            @log_method
            def open(self):
                self.is_open = True

            @log_method
            def close(self):
                self.is_open = False
        """),
    cod(f"{P}-methods-e6", t("""
        Напиши **класс**-декоратор `Memoize`: `__init__(self, func)` сохраняет функцию и создаёт словарь `cache`, `__call__(self, *args)` возвращает результат из кэша или вызывает функцию.
        """),
        """
        class Memoize:
            pass
        """,
        """
        def test_values():
            calls = []
            @Memoize
            def sq(n):
                calls.append(n)
                return n * n
            assert [sq(3), sq(3), sq(4)] == [9, 9, 16] and calls == [3, 4] and sq.cache == {(3,): 9, (4,): 16}, f"calls={calls}"
            assert isinstance(sq, Memoize), "sq — объект Memoize"
        """,
        """
        class Memoize:
            def __init__(self, func):
                self.func = func
                self.cache = {}

            def __call__(self, *args):
                if args not in self.cache:
                    self.cache[args] = self.func(*args)
                return self.cache[args]
        """),
    cod(f"{P}-methods-e7", t("""
        Напиши декоратор класса `singleton`: сколько бы раз ни вызывали класс, возвращается **один и тот же** объект (созданный при первом вызове). Декоратор возвращает функцию-обёртку.
        """),
        """
        def singleton(cls):
            pass
        """,
        """
        def test_values():
            @singleton
            class Config:
                def __init__(self):
                    self.debug = False
            a = Config()
            a.debug = True
            b = Config()
            assert a is b and b.debug, "Должен быть один объект"
            @singleton
            class Other:
                pass
            assert Other() is not a, "У каждого класса свой объект"
        """,
        """
        def singleton(cls):
            instance = None

            def get_instance(*args, **kwargs):
                nonlocal instance
                if instance is None:
                    instance = cls(*args, **kwargs)
                return instance
            return get_instance
        """),
    cod(f"{P}-methods-e8", t("""
        Напиши декоратор класса `auto_str`: добавляет классу метод `__str__`, возвращающий атрибуты объекта в виде `"name=Аня; age=30"` (порядок — как в `vars`). Декоратор возвращает **тот же** класс.
        """),
        """
        def auto_str(cls):
            pass
        """,
        """
        def test_values():
            @auto_str
            class User:
                def __init__(self, name, age):
                    self.name = name
                    self.age = age
            assert str(User("Аня", 30)) == "name=Аня; age=30" and User.__name__ == "User" and isinstance(User("x", 1), User), str(User("Аня", 30))
        """,
        """
        def auto_str(cls):
            def __str__(self):
                return "; ".join(f"{k}={v}" for k, v in vars(self).items())
            cls.__str__ = __str__
            return cls
        """, xp=20),
),

lesson(f"{P}-practice", "Практика: декораторы в тестах",
    out(f"{P}-practice-e1", "Что выведет программа? Реестр тестов.", """
        TESTS = []

        def test(func):
            TESTS.append(func)
            return func

        @test
        def check_login():
            assert True

        @test
        def check_cart():
            assert 1 + 1 == 3

        def helper():
            pass

        for t in TESTS:
            try:
                t()
                print("PASS", t.__name__)
            except AssertionError:
                print("FAIL", t.__name__)
        """, hint="Так фреймворки собирают тесты: декоратор регистрирует функцию."),
    out(f"{P}-practice-e2", "Что выведет программа? Метки как в pytest.mark.", """
        def mark(*tags):
            def decorator(func):
                func.tags = set(tags)
                return func
            return decorator

        @mark("smoke", "api")
        def test_status(): pass

        @mark("regression")
        def test_history(): pass

        @mark("smoke")
        def test_login(): pass

        tests = [test_status, test_history, test_login]
        print([t.__name__ for t in tests if "smoke" in t.tags])
        """),
    out(f"{P}-practice-e3", "Что выведет программа? Параметризация.", """
        def parametrize(cases):
            def decorator(func):
                def run_all():
                    return [func(*case) for case in cases]
                return run_all
            return decorator

        @parametrize([(2, 3, 5), (0, 0, 0), (-1, 1, 1)])
        def check_add(a, b, expected):
            return "ok" if a + b == expected else f"FAIL {a}+{b}"

        print(check_add())
        """, hint="Похоже на @pytest.mark.parametrize — один тест, много наборов данных."),
    cod(f"{P}-practice-e4", t("""
        Напиши декоратор `skip_if(condition, reason)`: если `condition` истинно, функция **не вызывается**, а обёртка возвращает строку `f"SKIP: {reason}"`. Иначе функция работает как обычно.
        """),
        """
        def skip_if(condition, reason):
            pass
        """,
        """
        def test_values():
            calls = []
            @skip_if(True, "нет Windows")
            def t1():
                calls.append(1)
                return "ran"
            @skip_if(False, "не важно")
            def t2():
                return "ran"
            assert t1() == "SKIP: нет Windows" and calls == [] and t2() == "ran" and t1.__name__ == "t1", "Неверный результат"
        """,
        """
        from functools import wraps


        def skip_if(condition, reason):
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    if condition:
                        return f"SKIP: {reason}"
                    return func(*args, **kwargs)
                return wrapper
            return decorator
        """),
    cod(f"{P}-practice-e5", t("""
        Напиши декоратор-регистратор `route(path)` для мини-веб-фреймворка: сохраняет функцию в глобальный словарь `ROUTES[path]` и возвращает **ту же** функцию. И функцию `handle(path)` — вызвать обработчик пути; если пути нет — вернуть `"404"`.
        """),
        """
        ROUTES = {}


        def route(path):
            pass


        def handle(path):
            pass
        """,
        """
        def test_values():
            ROUTES.clear()
            @route("/")
            def index():
                return "главная"
            @route("/about")
            def about():
                return "о нас"
            assert handle("/") == "главная" and handle("/about") == "о нас" and handle("/x") == "404", "handle"
            assert ROUTES["/"] is index and index() == "главная", "Та же функция в реестре"
        """,
        """
        ROUTES = {}


        def route(path):
            def decorator(func):
                ROUTES[path] = func
                return func
            return decorator


        def handle(path):
            if path not in ROUTES:
                return "404"
            return ROUTES[path]()
        """, hint="Так устроены @app.get('/path') во FastAPI и Flask."),
    cod(f"{P}-practice-e6", t("""
        Напиши декоратор `parametrize(cases)`: превращает функцию `check(*args)` в функцию без аргументов, которая прогоняет `check` на каждом кортеже из `cases` и возвращает **количество упавших** случаев (упал — выбросил `AssertionError`).
        """),
        """
        def parametrize(cases):
            pass
        """,
        """
        def test_values():
            @parametrize([(1, 1, 2), (2, 2, 5), (0, 5, 5), (3, 3, 7)])
            def check_add(a, b, expected):
                assert a + b == expected
            assert check_add() == 2, f"Получено {check_add()}"
        """,
        """
        from functools import wraps


        def parametrize(cases):
            def decorator(func):
                @wraps(func)
                def run_all():
                    failed = 0
                    for case in cases:
                        try:
                            func(*case)
                        except AssertionError:
                            failed += 1
                    return failed
                return run_all
            return decorator
        """),
    cod(f"{P}-practice-e7", t("""
        Напиши декоратор `fixture` — упрощённая фикстура: функция-фикстура вызывается **один раз** при первом обращении, дальше возвращается тот же объект. И декоратор `use(fix)` для тестов: передаёт результат фикстуры тесту первым аргументом.

        ```
        @fixture
        def db(): return {"users": []}

        @use(db)
        def test_add(database):
            database["users"].append("аня")
        ```
        """),
        """
        def fixture(func):
            pass


        def use(fix):
            pass
        """,
        """
        def test_values():
            created = []
            @fixture
            def db():
                created.append(1)
                return {"users": []}
            @use(db)
            def test_add(database, name):
                database["users"].append(name)
                return len(database["users"])
            assert test_add("аня") == 1 and test_add("боря") == 2 and created == [1] and db() is db(), "Фикстура создаётся один раз"
        """,
        """
        from functools import wraps


        def fixture(func):
            cache = []

            @wraps(func)
            def wrapper():
                if not cache:
                    cache.append(func())
                return cache[0]
            return wrapper


        def use(fix):
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    return func(fix(), *args, **kwargs)
                return wrapper
            return decorator
        """),
    cod(f"{P}-practice-e8", t("""
        Напиши мини-раннер: декоратор `test(*tags)` регистрирует функцию в глобальном списке `REGISTRY` как пару `(функция, множество_тегов)` и возвращает функцию без изменений. Функция `run(tag=None)` запускает зарегистрированные тесты (все или только с тегом) и возвращает словарь `{"passed": [...имена], "failed": [...имена]}`; упал — выбросил `AssertionError`.
        """),
        """
        REGISTRY = []


        def test(*tags):
            pass


        def run(tag=None):
            pass
        """,
        """
        def test_values():
            REGISTRY.clear()
            @test("smoke")
            def a():
                assert True
            @test("smoke", "api")
            def b():
                assert False
            @test("api")
            def c():
                assert 1
            assert run() == {"passed": ["a", "c"], "failed": ["b"]}, run()
            assert run("smoke") == {"passed": ["a"], "failed": ["b"]} and run("ui") == {"passed": [], "failed": []}, run("smoke")
        """,
        """
        REGISTRY = []


        def test(*tags):
            def decorator(func):
                REGISTRY.append((func, set(tags)))
                return func
            return decorator


        def run(tag=None):
            result = {"passed": [], "failed": []}
            for func, tags in REGISTRY:
                if tag is not None and tag not in tags:
                    continue
                try:
                    func()
                except AssertionError:
                    result["failed"].append(func.__name__)
                else:
                    result["passed"].append(func.__name__)
            return result
        """, xp=25),
),
)
