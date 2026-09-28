"""Тема «Декораторы», модуль 1 «Функции-обёртки» — задания. Теория — в _dec_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "dec"

m1 = module(f"{P}-m1", "Функции-обёртки", "🎁", "Функции как объекты, функции, возвращающие функции, первый декоратор, синтаксис @",

lesson(f"{P}-funcobj", "Функция — это объект",
    out(f"{P}-funcobj-e1", "Что выведет программа?", """
        def hello():
            return "привет"

        greet = hello
        print(greet())
        print(greet is hello, hello.__name__, greet.__name__)
        print(type(hello).__name__)
        """, hint="Без скобок — сама функция, со скобками — её результат."),
    out(f"{P}-funcobj-e2", "Что выведет программа? Функция как аргумент.", """
        def apply(func, value):
            return func(value)

        def double(x):
            return x * 2

        print(apply(double, 5))
        print(apply(str.upper, "abc"))
        print(apply(len, [1, 2, 3]))
        """),
    out(f"{P}-funcobj-e3", "Что выведет программа? Словарь функций.", """
        def add(a, b):
            return a + b

        def sub(a, b):
            return a - b

        ops = {"+": add, "-": sub, "*": lambda a, b: a * b}
        for sign in ["+", "-", "*"]:
            print(sign, ops[sign](6, 3))
        """),
    cod(f"{P}-funcobj-e4", t("""
        Напиши функцию `apply_twice(func, x)` — применить функцию дважды: `func(func(x))`.

        ```
        apply_twice(lambda n: n + 3, 1)   # → 7
        apply_twice(str.upper, "a")       # → "A"
        ```
        """),
        """
        def apply_twice(func, x):
            pass
        """,
        """
        def test_values():
            assert apply_twice(lambda n: n + 3, 1) == 7 and apply_twice(lambda s: s + "!", "hi") == "hi!!" and apply_twice(str.upper, "a") == "A", "Неверный результат"
        """,
        """
        def apply_twice(func, x):
            return func(func(x))
        """),
    cod(f"{P}-funcobj-e5", t("""
        Напиши функцию `calculate(a, op, b)` — калькулятор на словаре функций. Операции: `"+"`, `"-"`, `"*"`, `"/"`. Неизвестная операция — `ValueError("неизвестная операция")`. Не используй `if`/`elif` для выбора операции.
        """),
        """
        def calculate(a, op, b):
            pass
        """,
        """
        def test_values():
            assert calculate(6, "+", 3) == 9 and calculate(6, "-", 3) == 3 and calculate(6, "*", 3) == 18 and calculate(6, "/", 3) == 2, "Операции"
            try:
                calculate(1, "%", 2)
            except ValueError as e:
                assert str(e) == "неизвестная операция", str(e)
            else:
                assert False, "Нужен ValueError"
            assert "elif" not in open("solution.py", encoding="utf-8").read(), "Используй словарь, а не elif"
        """,
        """
        OPS = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }

        def calculate(a, op, b):
            if op not in OPS:
                raise ValueError("неизвестная операция")
            return OPS[op](a, b)
        """),
    cod(f"{P}-funcobj-e6", t("""
        Напиши функцию `pipeline(value, *funcs)` — пропустить значение через функции по очереди.

        ```
        pipeline("  Hi ", str.strip, str.lower)   # → "hi"
        pipeline(5)                               # → 5
        ```
        """),
        """
        def pipeline(value, *funcs):
            pass
        """,
        """
        def test_values():
            assert pipeline("  Hi ", str.strip, str.lower) == "hi" and pipeline(5) == 5 and pipeline(2, lambda x: x + 1, lambda x: x * 10) == 30, "Неверный результат"
        """,
        """
        def pipeline(value, *funcs):
            for func in funcs:
                value = func(value)
            return value
        """),
    cod(f"{P}-funcobj-e7", t("""
        Напиши функцию `run_checks(value, checks)` — `checks` — список функций-проверок, каждая возвращает `True`/`False`. Верни список **имён** (`__name__`) проверок, которые не прошли.

        ```
        def is_positive(x): return x > 0
        def is_even(x): return x % 2 == 0
        run_checks(-3, [is_positive, is_even])   # → ["is_positive", "is_even"]
        ```
        """),
        """
        def run_checks(value, checks):
            pass
        """,
        """
        def test_values():
            def is_positive(x): return x > 0
            def is_even(x): return x % 2 == 0
            assert run_checks(-3, [is_positive, is_even]) == ["is_positive", "is_even"] and run_checks(4, [is_positive, is_even]) == [] and run_checks(3, [is_even]) == ["is_even"], "Неверный результат"
        """,
        """
        def run_checks(value, checks):
            return [check.__name__ for check in checks if not check(value)]
        """),
    cod(f"{P}-funcobj-e8", t("""
        Напиши функцию `count_calls(func, args_list)` — вызвать `func` с каждым аргументом из списка и вернуть словарь «результат → сколько раз получен».

        ```
        count_calls(len, ["a", "bb", "c"])   # → {1: 2, 2: 1}
        ```
        """),
        """
        def count_calls(func, args_list):
            pass
        """,
        """
        def test_values():
            assert count_calls(len, ["a", "bb", "c"]) == {1: 2, 2: 1} and count_calls(abs, [-1, 1, 2]) == {1: 2, 2: 1} and count_calls(len, []) == {}, "Неверный результат"
        """,
        """
        def count_calls(func, args_list):
            result = {}
            for arg in args_list:
                r = func(arg)
                result[r] = result.get(r, 0) + 1
            return result
        """, xp=20),
),

lesson(f"{P}-factory", "Функция, которая возвращает функцию",
    out(f"{P}-factory-e1", "Что выведет программа?", """
        def make_multiplier(k):
            def multiply(x):
                return x * k
            return multiply

        double = make_multiplier(2)
        triple = make_multiplier(3)
        print(double(5), triple(5))
        print(double.__name__)
        """, hint="Внутренняя функция запоминает k — это замыкание."),
    out(f"{P}-factory-e2", "Что выведет программа? Состояние в замыкании.", """
        def make_counter():
            count = 0
            def counter():
                nonlocal count
                count += 1
                return count
            return counter

        a = make_counter()
        b = make_counter()
        print(a(), a(), a(), b())
        """),
    out(f"{P}-factory-e3", "Что выведет программа? Функция получает и возвращает функцию.", """
        def loud(func):
            def inner(text):
                return func(text).upper() + "!"
            return inner

        def greet(name):
            return f"привет, {name}"

        loud_greet = loud(greet)
        print(greet("аня"))
        print(loud_greet("аня"))
        """, hint="Это уже почти декоратор."),
    cod(f"{P}-factory-e4", t("""
        Напиши функцию `make_adder(n)` — вернуть функцию, которая прибавляет `n` к аргументу.

        ```
        add5 = make_adder(5)
        add5(10)   # → 15
        ```
        """),
        """
        def make_adder(n):
            pass
        """,
        """
        def test_values():
            add5 = make_adder(5)
            assert add5(10) == 15 and make_adder(-1)(0) == -1 and callable(add5), "Неверный результат"
        """,
        """
        def make_adder(n):
            def add(x):
                return x + n
            return add
        """),
    cod(f"{P}-factory-e5", t("""
        Напиши функцию `make_validator(min_len, max_len)` — вернуть функцию-проверку строки: `True`, если длина в диапазоне включительно.

        ```
        check = make_validator(3, 5)
        check("ab"), check("abcd")   # → (False, True)
        ```
        """),
        """
        def make_validator(min_len, max_len):
            pass
        """,
        """
        def test_values():
            check = make_validator(3, 5)
            assert [check(s) for s in ["ab", "abc", "abcde", "abcdef"]] == [False, True, True, False], "Неверная проверка"
        """,
        """
        def make_validator(min_len, max_len):
            def check(text):
                return min_len <= len(text) <= max_len
            return check
        """),
    cod(f"{P}-factory-e6", t("""
        Напиши функцию `make_accumulator()` — вернуть функцию `add(x)`, которая копит сумму всех переданных чисел и возвращает текущую сумму. У каждого аккумулятора своя сумма.
        """),
        """
        def make_accumulator():
            pass
        """,
        """
        def test_values():
            a, b = make_accumulator(), make_accumulator()
            assert a(10) == 10 and a(5) == 15 and b(1) == 1 and a(0) == 15, "Неверная сумма"
        """,
        """
        def make_accumulator():
            total = 0
            def add(x):
                nonlocal total
                total += x
                return total
            return add
        """, hint="Для изменения внешней переменной нужен nonlocal."),
    cod(f"{P}-factory-e7", t("""
        Напиши функцию `negate(func)` — вернуть новую функцию, которая возвращает `not func(...)`.

        ```
        def is_even(x): return x % 2 == 0
        is_odd = negate(is_even)
        is_odd(3)   # → True
        ```
        """),
        """
        def negate(func):
            pass
        """,
        """
        def test_values():
            def is_even(x): return x % 2 == 0
            is_odd = negate(is_even)
            assert is_odd(3) is True and is_odd(4) is False and negate(str.isdigit)("12") is False, "Неверный результат"
        """,
        """
        def negate(func):
            def inner(x):
                return not func(x)
            return inner
        """),
    cod(f"{P}-factory-e8", t("""
        Напиши функцию `compose(f, g)` — вернуть функцию `h(x) = f(g(x))`.

        ```
        inc = lambda x: x + 1
        dbl = lambda x: x * 2
        compose(inc, dbl)(5)   # → 11
        compose(dbl, inc)(5)   # → 12
        ```
        """),
        """
        def compose(f, g):
            pass
        """,
        """
        def test_values():
            inc = lambda x: x + 1
            dbl = lambda x: x * 2
            assert compose(inc, dbl)(5) == 11 and compose(dbl, inc)(5) == 12 and compose(str.upper, str.strip)(" a ") == "A", "Неверный результат"
        """,
        """
        def compose(f, g):
            def h(x):
                return f(g(x))
            return h
        """, xp=20),
),

lesson(f"{P}-first", "Первый декоратор",
    out(f"{P}-first-e1", "Что выведет программа?", """
        def announce(func):
            def wrapper():
                print("до вызова")
                func()
                print("после вызова")
            return wrapper

        def work():
            print("работаю")

        work = announce(work)
        work()
        """, hint="work теперь ссылается на wrapper, а старая work живёт внутри как func."),
    out(f"{P}-first-e2", "Что выведет программа? Декоратор теряет результат.", """
        def announce(func):
            def wrapper():
                print("вызов")
                func()
            return wrapper

        def get_answer():
            return 42

        get_answer = announce(get_answer)
        print(get_answer())
        """, hint="wrapper не возвращает результат func — значит возвращает None."),
    out(f"{P}-first-e3", "Что выведет программа? Декоратор срабатывает при каждом вызове.", """
        def twice(func):
            def wrapper():
                func()
                func()
            return wrapper

        def ping():
            print("ping")

        ping = twice(ping)
        ping()
        print("---")
        ping()
        """),
    cod(f"{P}-first-e4", t("""
        Напиши декоратор `shout(func)` для функций **без аргументов**, возвращающих строку: результат переводится в верхний регистр и к нему добавляется `"!"`.

        ```
        def hello(): return "привет"
        hello = shout(hello)
        hello()   # → "ПРИВЕТ!"
        ```
        """),
        """
        def shout(func):
            pass
        """,
        """
        def test_values():
            def hello():
                return "привет"
            h = shout(hello)
            assert h() == "ПРИВЕТ!" and hello() == "привет", "Неверный результат"
        """,
        """
        def shout(func):
            def wrapper():
                return func().upper() + "!"
            return wrapper
        """),
    cod(f"{P}-first-e5", t("""
        Напиши декоратор `log_call(func)` для функций без аргументов: перед вызовом печатает `вызов <имя функции>`, затем вызывает функцию и **возвращает её результат**.
        """),
        """
        def log_call(func):
            pass
        """,
        """
        import io, contextlib

        def test_values():
            def answer():
                return 42
            f = log_call(answer)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                r = f()
            assert r == 42, "Результат нужно вернуть"
            assert buf.getvalue() == "вызов answer\\n", f"Напечатано: {buf.getvalue()!r}"
        """,
        """
        def log_call(func):
            def wrapper():
                print(f"вызов {func.__name__}")
                return func()
            return wrapper
        """),
    cod(f"{P}-first-e6", t("""
        Напиши декоратор `safe(func)` для функций без аргументов: если функция выбросила любое исключение (`Exception`), вернуть `None` вместо падения.
        """),
        """
        def safe(func):
            pass
        """,
        """
        def test_values():
            def bad():
                return 1 / 0
            def good():
                return "ok"
            assert safe(bad)() is None and safe(good)() == "ok", "Неверный результат"
        """,
        """
        def safe(func):
            def wrapper():
                try:
                    return func()
                except Exception:
                    return None
            return wrapper
        """),
    cod(f"{P}-first-e7", t("""
        Напиши декоратор `count_calls(func)` для функций без аргументов: обёртка считает вызовы в своём атрибуте `calls` (функции — объекты, им можно добавлять атрибуты).

        ```
        f = count_calls(some_func)
        f(); f()
        f.calls   # → 2
        ```
        """),
        """
        def count_calls(func):
            pass
        """,
        """
        def test_values():
            def ping():
                return "pong"
            f = count_calls(ping)
            assert f.calls == 0, "Начальное значение 0"
            assert f() == "pong" and f() == "pong" and f.calls == 2, "Счётчик вызовов"
            assert count_calls(ping).calls == 0, "У каждой обёртки свой счётчик"
        """,
        """
        def count_calls(func):
            def wrapper():
                wrapper.calls += 1
                return func()
            wrapper.calls = 0
            return wrapper
        """),
    cod(f"{P}-first-e8", t("""
        Напиши декоратор `once(func)` для функций без аргументов: функция реально выполняется только при **первом** вызове, дальше обёртка возвращает сохранённый результат.
        """),
        """
        def once(func):
            pass
        """,
        """
        def test_values():
            log = []
            def init():
                log.append(1)
                return "готово"
            f = once(init)
            assert f() == "готово" and f() == "готово" and log == [1], f"Функция должна выполниться один раз, log={log}"
        """,
        """
        def once(func):
            done = False
            result = None
            def wrapper():
                nonlocal done, result
                if not done:
                    result = func()
                    done = True
                return result
            return wrapper
        """, xp=20),
),

lesson(f"{P}-syntax", "Синтаксис @ и любые аргументы",
    out(f"{P}-syntax-e1", "Что выведет программа?", """
        def exclaim(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs) + "!"
            return wrapper

        @exclaim
        def greet(name, greeting="Привет"):
            return f"{greeting}, {name}"

        print(greet("Аня"))
        print(greet("Боря", greeting="Здравствуй"))
        """, hint="@exclaim над def — то же, что greet = exclaim(greet)."),
    out(f"{P}-syntax-e2", "Что выведет программа? Когда срабатывает декоратор.", """
        def register(func):
            print("декорирую", func.__name__)
            return func

        @register
        def a():
            print("a")

        @register
        def b():
            print("b")

        print("старт")
        a()
        """, hint="Сам декоратор выполняется один раз — при объявлении функции."),
    out(f"{P}-syntax-e3", "Что выведет программа? Обёртка видит аргументы.", """
        def show_args(func):
            def wrapper(*args, **kwargs):
                print("args:", args, "kwargs:", kwargs)
                return func(*args, **kwargs)
            return wrapper

        @show_args
        def area(w, h=1):
            return w * h

        print(area(3, h=4))
        print(area(5))
        """),
    cod(f"{P}-syntax-e4", t("""
        Напиши декоратор `double_result`, который удваивает результат функции с **любыми** аргументами. Примени его через `@` к функции `add(a, b)`.

        ```
        add(2, 3)       # → 10
        add(a=1, b=1)   # → 4
        ```
        """),
        """
        def double_result(func):
            pass


        def add(a, b):
            return a + b
        """,
        """
        def test_values():
            assert add(2, 3) == 10 and add(a=1, b=1) == 4, "add должна быть задекорирована"
            @double_result
            def s(*xs):
                return sum(xs)
            assert s(1, 2, 3) == 12, "Работает с любыми аргументами"
        """,
        """
        def double_result(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs) * 2
            return wrapper


        @double_result
        def add(a, b):
            return a + b
        """),
    cod(f"{P}-syntax-e5", t("""
        Напиши декоратор `log_args`: печатает `имя(аргументы)` в виде `add(2, 3, b=5)` и возвращает результат функции.

        - позиционные аргументы — через `repr`;
        - именованные — `ключ=repr(значение)`;
        - всё через `", "`.
        """),
        """
        def log_args(func):
            pass
        """,
        """
        import io, contextlib

        def test_values():
            @log_args
            def add(a, b, c=0):
                return a + b + c
            @log_args
            def hi(name):
                return name
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                r = add(2, 3, c=5)
                hi("Аня")
            assert r == 10, "Результат"
            assert buf.getvalue() == "add(2, 3, c=5)\\nhi('Аня')\\n", f"Напечатано: {buf.getvalue()!r}"
        """,
        """
        def log_args(func):
            def wrapper(*args, **kwargs):
                parts = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
                print(f"{func.__name__}({', '.join(parts)})")
                return func(*args, **kwargs)
            return wrapper
        """),
    cod(f"{P}-syntax-e6", t("""
        Напиши декоратор `positive_args` — перед вызовом проверяет, что все **позиционные** аргументы-числа больше нуля. Иначе — `ValueError("аргументы должны быть > 0")`, функция не вызывается.
        """),
        """
        def positive_args(func):
            pass
        """,
        """
        def test_values():
            calls = []
            @positive_args
            def area(w, h):
                calls.append(1)
                return w * h
            assert area(2, 3) == 6, "Нормальный вызов"
            try:
                area(2, -1)
            except ValueError as e:
                assert str(e) == "аргументы должны быть > 0" and calls == [1], "Функция не должна вызываться"
                return
            assert False, "Нужен ValueError"
        """,
        """
        def positive_args(func):
            def wrapper(*args, **kwargs):
                for a in args:
                    if a <= 0:
                        raise ValueError("аргументы должны быть > 0")
                return func(*args, **kwargs)
            return wrapper
        """),
    cod(f"{P}-syntax-e7", t("""
        Напиши декоратор `strip_strings` — перед вызовом у всех строковых аргументов (позиционных и именованных) убирает пробелы по краям. Нестроковые аргументы не меняются.
        """),
        """
        def strip_strings(func):
            pass
        """,
        """
        def test_values():
            @strip_strings
            def join(a, b, sep="-"):
                return f"{a}{sep}{b}"
            assert join("  x ", " y", sep=" + ") == "x+y" and join(1, " z ") == "1-z", "Неверный результат"
        """,
        """
        def strip_strings(func):
            def clean(v):
                return v.strip() if isinstance(v, str) else v

            def wrapper(*args, **kwargs):
                args = [clean(a) for a in args]
                kwargs = {k: clean(v) for k, v in kwargs.items()}
                return func(*args, **kwargs)
            return wrapper
        """),
    cod(f"{P}-syntax-e8", t("""
        Напиши декоратор `collect_errors` — обёртка ловит любое `Exception`, добавляет в свой атрибут-список `errors` строку `"ИмяОшибки: текст"` и возвращает `None`. Успешные вызовы возвращают результат как обычно.
        """),
        """
        def collect_errors(func):
            pass
        """,
        """
        def test_values():
            @collect_errors
            def div(a, b):
                return a / b
            assert div(6, 3) == 2 and div(1, 0) is None and div("a", 1) is None, "Результаты"
            assert div.errors == ["ZeroDivisionError: division by zero", "TypeError: unsupported operand type(s) for /: 'str' and 'int'"], div.errors
        """,
        """
        def collect_errors(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    wrapper.errors.append(f"{type(e).__name__}: {e}")
                    return None
            wrapper.errors = []
            return wrapper
        """, xp=20),
),
)
