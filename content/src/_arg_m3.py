"""Тема «*args и **kwargs», модуль 3 «Всё вместе» — задания. Теория — в _arg_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "arg"

m3 = module(f"{P}-m3", "Всё вместе", "🧩", "Полная сигнатура, функции-обёртки, ошибки вызова и практика",

lesson(f"{P}-m3-l1", "Порядок параметров: полная сигнатура",
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        def f(a, b=2, *args, c, d=4, **kwargs):
            print(a, b, args, c, d, kwargs)

        f(1, c=3)
        f(1, 5, 6, 7, c=8, e=9)
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа? Только по имени.", """
        def g(*, key):
            return key

        print(g(key=1))
        try:
            g(1)
        except TypeError:
            print("key только по имени")
        """),
    out(f"{P}-m3-l1-e3", "Что выведет программа? / и *.", """
        def h(a, /, b, *, c):
            return a + b + c

        print(h(1, 2, c=3), h(1, b=2, c=3))
        try:
            h(a=1, b=2, c=3)
        except TypeError:
            print("a только по позиции")
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `describe_call(*args, **kwargs)` — строка `"args=<кортеж>, kwargs=<словарь>"`.

        ```
        describe_call(1, 2, x=3)   # → "args=(1, 2), kwargs={'x': 3}"
        describe_call()            # → "args=(), kwargs={}"
        ```
        """),
        """
        def describe_call(*args, **kwargs):
            pass
        """,
        """
        def test_values():
            assert [describe_call(1, 2, x=3), describe_call()] == ["args=(1, 2), kwargs={'x': 3}", "args=(), kwargs={}"], "Неверная строка"
        """,
        """
        def describe_call(*args, **kwargs):
            return f"args={args}, kwargs={kwargs}"
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `send(to, *attachments, subject="", urgent=False)` — описание письма словарём: `to`, `attachments` (список), `subject`, `urgent`. Тема и срочность — только по имени.

        ```
        send("a@x.ru", "report.pdf", subject="Отчёт")
        # → {"to": "a@x.ru", "attachments": ["report.pdf"], "subject": "Отчёт", "urgent": False}
        ```
        """),
        """
        def send(to, *attachments, subject="", urgent=False):
            pass
        """,
        """
        def test_values():
            assert send("a@x.ru", "report.pdf", subject="Отчёт") == {"to": "a@x.ru", "attachments": ["report.pdf"], "subject": "Отчёт", "urgent": False}, "Неверное письмо"
            assert send("b@x.ru", urgent=True) == {"to": "b@x.ru", "attachments": [], "subject": "", "urgent": True}, "Без вложений"
        """,
        """
        def send(to, *attachments, subject="", urgent=False):
            return {"to": to, "attachments": list(attachments), "subject": subject, "urgent": urgent}
        """),
    cod(f"{P}-m3-l1-e6", t("""
        Напиши функцию `run(cmd, *args, env=None, **options)` — описание запуска команды: `{"cmd": ..., "args": [...], "env": ..., "options": {...}}`. Если `env` не передан — пустой словарь.

        ```
        run("pytest", "-v", "tests/", env={"CI": "1"}, timeout=60)
        # → {"cmd": "pytest", "args": ["-v", "tests/"], "env": {"CI": "1"}, "options": {"timeout": 60}}
        ```
        """),
        """
        def run(cmd, *args, env=None, **options):
            pass
        """,
        """
        def test_values():
            got = run("pytest", "-v", "tests/", env={"CI": "1"}, timeout=60)
            assert got == {"cmd": "pytest", "args": ["-v", "tests/"], "env": {"CI": "1"}, "options": {"timeout": 60}}, f"Получено {got}"
            assert run("ls") == {"cmd": "ls", "args": [], "env": {}, "options": {}}, "Умолчания"
        """,
        """
        def run(cmd, *args, env=None, **options):
            if env is None:
                env = {}
            return {"cmd": cmd, "args": list(args), "env": env, "options": options}
        """),
    cod(f"{P}-m3-l1-e7", t("""
        Напиши функцию `sum_and_label(*nums, label)` — строка `"<label>: <сумма>"`. Параметр `label` обязательный и передаётся только по имени.

        ```
        sum_and_label(1, 2, 3, label="итого")   # → "итого: 6"
        ```
        """),
        """
        def sum_and_label(*nums, label):
            pass
        """,
        """
        def test_values():
            assert [sum_and_label(1, 2, 3, label="итого"), sum_and_label(label="пусто")] == ["итого: 6", "пусто: 0"], "Неверная строка"

        def test_required():
            try:
                sum_and_label(1, 2)
            except TypeError:
                return
            assert False, "Без label должна быть ошибка"
        """,
        """
        def sum_and_label(*nums, label):
            return f"{label}: {sum(nums)}"
        """),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `area(width, height, /, *, unit="см")` — строка `"<площадь> <unit>²"`. Размеры — только по позиции, единица — только по имени.

        ```
        area(3, 4)              # → "12 см²"
        area(2, 5, unit="м")    # → "10 м²"
        ```
        """),
        """
        def area(width, height, /, *, unit="см"):
            pass
        """,
        """
        def test_values():
            assert [area(3, 4), area(2, 5, unit="м")] == ["12 см²", "10 м²"], "Неверная строка"

        def test_signature():
            for bad in (lambda: area(width=1, height=2), lambda: area(1, 2, "м")):
                try:
                    bad()
                except TypeError:
                    continue
                assert False, "Нарушение сигнатуры должно давать TypeError"
        """,
        """
        def area(width, height, /, *, unit="см"):
            return f"{width * height} {unit}²"
        """),
),

lesson(f"{P}-m3-l2", "Функции-обёртки: передать всё дальше",
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        def logged(func, *args, **kwargs):
            print("вызов", func.__name__, args, kwargs)
            return func(*args, **kwargs)

        print(logged(max, 3, 7))
        print(logged(sorted, [3, 1, 2], reverse=True))
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа? Обёртка-замыкание.", """
        def make_logger(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                print(f"{func.__name__}{args} -> {result}")
                return result
            return wrapper

        def add(a, b):
            return a + b

        add = make_logger(add)
        add(2, 3)
        """),
    out(f"{P}-m3-l2-e3", "Что выведет программа?", """
        calls = []

        def counted(func):
            def wrapper(*args, **kwargs):
                calls.append(args)
                return func(*args, **kwargs)
            return wrapper

        double = counted(lambda x: x * 2)
        print(double(3), double(5), len(calls))
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши функцию `call_twice(func, *args, **kwargs)` — вызвать `func` дважды с одними и теми же аргументами и вернуть список двух результатов.

        ```
        call_twice(pow, 2, 3)                   # → [8, 8]
        call_twice(sorted, [2, 1], reverse=True)  # → [[2, 1], [2, 1]]
        ```
        """),
        """
        def call_twice(func, *args, **kwargs):
            pass
        """,
        """
        def test_values():
            assert [call_twice(pow, 2, 3), call_twice(sorted, [2, 1], reverse=True)] == [[8, 8], [[2, 1], [2, 1]]], "Неверный результат"
        """,
        """
        def call_twice(func, *args, **kwargs):
            return [func(*args, **kwargs), func(*args, **kwargs)]
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `safe(func, *args, default=None, **kwargs)` — вызвать `func(*args, **kwargs)`; если возникло любое исключение — вернуть `default`.

        ```
        safe(int, "42")                 # → 42
        safe(int, "x", default=0)       # → 0
        safe(int, "ff", base=16)        # → 255
        ```
        """),
        """
        def safe(func, *args, default=None, **kwargs):
            pass
        """,
        """
        def test_values():
            assert [safe(int, "42"), safe(int, "x", default=0), safe(int, "ff", base=16), safe(int, "x")] == [42, 0, 255, None], "Неверный результат"
        """,
        """
        def safe(func, *args, default=None, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                return default
        """, hint="default стоит после *args — значит, передаётся только по имени и не попадёт в func."),
    cod(f"{P}-m3-l2-e6", t("""
        Напиши функцию `retry(func, attempts, *args, **kwargs)` — вызывать `func(*args, **kwargs)`, пока вызов не пройдёт без исключения, но не больше `attempts` раз. Вернуть результат или `None`, если все попытки упали.

        ```
        retry(int, 3, "5")    # → 5
        retry(int, 3, "x")    # → None
        ```
        """),
        """
        def retry(func, attempts, *args, **kwargs):
            pass
        """,
        """
        def test_values():
            calls = []
            def flaky(x, y=0):
                calls.append(1)
                if len(calls) < 3:
                    raise ConnectionError("нет связи")
                return x + y
            assert retry(flaky, 5, 1, y=2) == 3 and len(calls) == 3, "Должно получиться с третьей попытки"
            assert retry(int, 3, "x") is None, "Все попытки упали — None"
        """,
        """
        def retry(func, attempts, *args, **kwargs):
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    pass
            return None
        """, xp=20),
    cod(f"{P}-m3-l2-e7", t("""
        Напиши функцию `with_defaults(func, **defaults)` — вернуть новую функцию, которая вызывает `func` с переданными аргументами и именованными значениями по умолчанию `defaults` (аргументы вызова важнее).

        ```
        def connect(host, port=80, timeout=5): return (host, port, timeout)
        c = with_defaults(connect, port=8080)
        c("db")               # → ("db", 8080, 5)
        c("db", port=1)       # → ("db", 1, 5)
        ```
        """),
        """
        def with_defaults(func, **defaults):
            pass
        """,
        """
        def test_values():
            def connect(host, port=80, timeout=5):
                return (host, port, timeout)
            c = with_defaults(connect, port=8080)
            assert [c("db"), c("db", port=1), c("x", timeout=1)] == [("db", 8080, 5), ("db", 1, 5), ("x", 8080, 1)], "Неверные вызовы"
        """,
        """
        def with_defaults(func, **defaults):
            def wrapper(*args, **kwargs):
                return func(*args, **{**defaults, **kwargs})
            return wrapper
        """, xp=20),
    cod(f"{P}-m3-l2-e8", t("""
        Напиши функцию `count_calls(func)` — вернуть **пару** `(wrapper, get_count)`: `wrapper` вызывает `func` с любыми аргументами и считает вызовы, `get_count()` возвращает число вызовов.

        ```
        w, get_count = count_calls(max)
        w(1, 2); w(3, 4)
        get_count()   # → 2
        ```
        """),
        """
        def count_calls(func):
            pass
        """,
        """
        def test_values():
            w, get_count = count_calls(max)
            assert w(1, 2) == 2 and w(3, 4, key=abs) == 4 and get_count() == 2, "Неверный подсчёт"
        """,
        """
        def count_calls(func):
            count = 0
            def wrapper(*args, **kwargs):
                nonlocal count
                count += 1
                return func(*args, **kwargs)
            def get_count():
                return count
            return wrapper, get_count
        """),
),

lesson(f"{P}-m3-l3", "Ошибки вызова с *args и **kwargs",
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        def f(a, *args, b):
            return a, args, b

        try:
            f(1, 2, 3)
        except TypeError as e:
            print(e)
        print(f(1, 2, b=3))
        """, hint="Всё позиционное съел *args — для b ничего не осталось."),
    out(f"{P}-m3-l3-e2", "Что выведет программа?", """
        def g(x, **kw):
            return x, kw

        try:
            g(1, x=2)
        except TypeError as e:
            print(e)
        print(g(1, y=2))
        """),
    out(f"{P}-m3-l3-e3", "Что выведет программа?", """
        def h(**kw):
            return kw

        try:
            h(1)
        except TypeError as e:
            print(e)
        print(h(**{"a": 1}))
        try:
            h(**{1: "x"})
        except TypeError:
            print("ключи должны быть строками")
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `try_call(func, *args, **kwargs)` — вызвать функцию; при `TypeError` вернуть строку `"ошибка вызова: <текст ошибки>"`, иначе результат.

        ```
        try_call(max, 1, 2)          # → 2
        try_call(len, 1, 2)          # → "ошибка вызова: len() takes exactly one argument (2 given)"
        ```
        """),
        """
        def try_call(func, *args, **kwargs):
            pass
        """,
        """
        def test_values():
            assert try_call(max, 1, 2) == 2, "Успешный вызов"
            got = try_call(len, 1, 2)
            assert isinstance(got, str) and got.startswith("ошибка вызова: ") and "len()" in got, f"Получено {got!r}"
        """,
        """
        def try_call(func, *args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TypeError as e:
                return f"ошибка вызова: {e}"
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Программа падает: функция `summary(*values, precision)` ждёт `precision` **по имени**, а её передают позиционно, и он попадает в `values`. Исправь **вызов** (функцию не меняй), чтобы программа напечатала сумму `1.234 + 2.345`, округлённую до 2 знаков.

        Ожидаемый вывод:
        ```
        3.58
        ```
        """),
        """
        def summary(*values, precision):
            return round(sum(values), precision)

        print(summary(1.234, 2.345, 2))
        """,
        """
        def test_output():
            assert OUTPUT.strip() == "3.58", f"Напечатано {OUTPUT.strip()!r}"

        def test_function_same():
            assert summary(1, 2, precision=0) == 3, "Функцию менять не нужно"
        """,
        """
        def summary(*values, precision):
            return round(sum(values), precision)

        print(summary(1.234, 2.345, precision=2))
        """),
    cod(f"{P}-m3-l3-e6", t("""
        Напиши функцию `unexpected(allowed, **kwargs)` — отсортированный список имён аргументов, которых нет в списке `allowed`.

        ```
        unexpected(["timeout", "retries"], timeout=5, colour="red", debug=True)   # → ["colour", "debug"]
        ```
        """),
        """
        def unexpected(allowed, **kwargs):
            pass
        """,
        """
        def test_values():
            assert unexpected(["timeout", "retries"], timeout=5, colour="red", debug=True) == ["colour", "debug"] and unexpected(["a"], a=1) == [], "Неверный результат"
        """,
        """
        def unexpected(allowed, **kwargs):
            return sorted(k for k in kwargs if k not in allowed)
        """),
    cod(f"{P}-m3-l3-e7", t("""
        Напиши функцию `strict_config(**kwargs)` — настройки с умолчаниями `{"timeout": 30, "retries": 3}`. Если передан **неизвестный** параметр — выбросить `TypeError` с текстом `"неизвестный параметр: <имя>"` (для первого такого по порядку).

        ```
        strict_config(timeout=5)   # → {"timeout": 5, "retries": 3}
        strict_config(colour=1)    # TypeError: неизвестный параметр: colour
        ```
        """),
        """
        def strict_config(**kwargs):
            pass
        """,
        """
        def test_values():
            assert strict_config(timeout=5) == {"timeout": 5, "retries": 3} and strict_config() == {"timeout": 30, "retries": 3}, "Неверные настройки"

        def test_unknown():
            try:
                strict_config(timeout=1, colour=1)
            except TypeError as e:
                assert str(e) == "неизвестный параметр: colour", f"Текст ошибки: {e}"
                return
            assert False, "Нужен TypeError"
        """,
        """
        DEFAULTS = {"timeout": 30, "retries": 3}

        def strict_config(**kwargs):
            for key in kwargs:
                if key not in DEFAULTS:
                    raise TypeError(f"неизвестный параметр: {key}")
            return {**DEFAULTS, **kwargs}
        """, hint='raise TypeError("текст") — выбросить ошибку.', xp=20),
    cod(f"{P}-m3-l3-e8", t("""
        Напиши функцию `explain_call(func, *args, **kwargs)` — вызвать функцию и вернуть `"ok: <результат>"`, а при `TypeError` — `"TypeError: <текст>"`.

        ```
        def f(a, *, b): return a + b
        explain_call(f, 1, b=2)   # → "ok: 3"
        explain_call(f, 1, 2)     # → "TypeError: f() takes 1 positional argument but 2 were given"
        ```
        """),
        """
        def explain_call(func, *args, **kwargs):
            pass
        """,
        """
        def test_values():
            def f(a, *, b):
                return a + b
            assert explain_call(f, 1, b=2) == "ok: 3", "Успешный вызов"
            got = explain_call(f, 1, 2)
            assert got.startswith("TypeError: ") and got.endswith("takes 1 positional argument but 2 were given"), f"Получено {got!r}"
        """,
        """
        def explain_call(func, *args, **kwargs):
            try:
                return f"ok: {func(*args, **kwargs)}"
            except TypeError as e:
                return f"TypeError: {e}"
        """),
),

lesson(f"{P}-m3-l4", "Практика: фабрики тестовых данных и API-клиент",
    out(f"{P}-m3-l4-e1", "Что выведет программа?", """
        def make_user(**overrides):
            user = {"name": "test", "email": "test@x.ru", "active": True}
            user.update(overrides)
            return user

        print(make_user())
        print(make_user(name="admin", active=False))
        """),
    out(f"{P}-m3-l4-e2", "Что выведет программа?", """
        def build_request(method, path, **params):
            query = "&".join(f"{k}={v}" for k, v in params.items())
            return f"{method} {path}" + (f"?{query}" if query else "")

        print(build_request("GET", "/users", page=2, limit=10))
        print(build_request("DELETE", "/users/7"))
        """),
    out(f"{P}-m3-l4-e3", "Что выведет программа?", """
        def make_users(n, **common):
            return [{"id": i, **common} for i in range(1, n + 1)]

        print(make_users(2, role="qa"))
        """),
    cod(f"{P}-m3-l4-e4", t("""
        Напиши фабрику тестовых данных `make_product(**overrides)` — товар по умолчанию `{"name": "товар", "price": 100, "qty": 1}`, поля которого можно переопределить.

        ```
        make_product(price=500)   # → {"name": "товар", "price": 500, "qty": 1}
        ```
        """),
        """
        def make_product(**overrides):
            pass
        """,
        """
        def test_values():
            assert make_product(price=500) == {"name": "товар", "price": 500, "qty": 1} and make_product() == {"name": "товар", "price": 100, "qty": 1}, "Неверный товар"
            a = make_product()
            a["price"] = 1
            assert make_product()["price"] == 100, "Каждый вызов — новый словарь"
        """,
        """
        def make_product(**overrides):
            return {"name": "товар", "price": 100, "qty": 1, **overrides}
        """),
    cod(f"{P}-m3-l4-e5", t("""
        Напиши функцию `build_request(method, path, **params)` — строка запроса: метод в верхнем регистре, путь и параметры `?k=v&...`; параметры со значением `None` пропускать. Если параметров нет — без `?`.

        ```
        build_request("get", "/users", page=2, q=None)   # → "GET /users?page=2"
        build_request("delete", "/x")                    # → "DELETE /x"
        ```
        """),
        """
        def build_request(method, path, **params):
            pass
        """,
        """
        def test_values():
            assert [build_request("get", "/users", page=2, q=None), build_request("delete", "/x")] == ["GET /users?page=2", "DELETE /x"], "Неверный запрос"
        """,
        """
        def build_request(method, path, **params):
            query = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
            line = f"{method.upper()} {path}"
            if query:
                line += "?" + query
            return line
        """),
    cod(f"{P}-m3-l4-e6", t("""
        Напиши функцию `make_users(n, **common)` — список из `n` пользователей с `id` от 1 до `n` и общими полями `common`.

        ```
        make_users(2, role="qa")   # → [{"id": 1, "role": "qa"}, {"id": 2, "role": "qa"}]
        ```
        """),
        """
        def make_users(n, **common):
            pass
        """,
        """
        def test_values():
            assert make_users(2, role="qa") == [{"id": 1, "role": "qa"}, {"id": 2, "role": "qa"}] and make_users(0) == [], "Неверный список"
        """,
        """
        def make_users(n, **common):
            return [{"id": i, **common} for i in range(1, n + 1)]
        """),
    cod(f"{P}-m3-l4-e7", t("""
        Напиши функцию `api_call(method, path, *, json=None, headers=None, **params)` — описание вызова API словарём с ключами `method`, `path`, `params` (словарь остальных именованных), `json`, `headers` (если не передан — пустой словарь).

        ```
        api_call("POST", "/users", json={"name": "Аня"}, page=1)
        # → {"method": "POST", "path": "/users", "params": {"page": 1}, "json": {"name": "Аня"}, "headers": {}}
        ```
        """),
        """
        def api_call(method, path, *, json=None, headers=None, **params):
            pass
        """,
        """
        def test_values():
            got = api_call("POST", "/users", json={"name": "Аня"}, page=1)
            assert got == {"method": "POST", "path": "/users", "params": {"page": 1}, "json": {"name": "Аня"}, "headers": {}}, f"Получено {got}"
        """,
        """
        def api_call(method, path, *, json=None, headers=None, **params):
            return {"method": method, "path": path, "params": params, "json": json, "headers": headers or {}}
        """),
    cod(f"{P}-m3-l4-e8", t("""
        Напиши функцию `batch(func, items, **kwargs)` — применить `func` к каждому элементу, передавая одинаковые именованные аргументы: `func(item, **kwargs)`.

        ```
        batch(round, [1.234, 5.678], ndigits=1)   # → [1.2, 5.7]
        ```
        """),
        """
        def batch(func, items, **kwargs):
            pass
        """,
        """
        def test_values():
            assert batch(round, [1.234, 5.678], ndigits=1) == [1.2, 5.7] and batch(str, []) == [], "Неверный результат"
            assert batch(int, ["ff", "10"], base=16) == [255, 16], "kwargs передаются в каждый вызов"
        """,
        """
        def batch(func, items, **kwargs):
            return [func(item, **kwargs) for item in items]
        """),
),
)
