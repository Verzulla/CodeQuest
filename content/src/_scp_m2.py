"""Тема «Область видимости», модуль 2 «Вложенные функции» — задания. Теория — в _scp_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "scp"

m2 = module(f"{P}-m2", "Вложенные функции", "🪆", "Правило LEGB, вложенные функции, nonlocal и замыкания",

lesson(f"{P}-m2-l1", "Правило LEGB",
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        x = "global"

        def outer():
            x = "enclosing"
            def inner():
                return x
            return inner()

        print(outer())
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа?", """
        x = "global"

        def outer():
            def inner():
                return x
            return inner()

        def outer2():
            x = "enclosing"
            def inner():
                x = "local"
                return x
            return inner(), x

        print(outer())
        print(outer2())
        """),
    out(f"{P}-m2-l1-e6", "Что выведет программа? Три уровня вложенности.", """
        x = "G"

        def a():
            x = "E1"
            def b():
                def c():
                    return x
                return c()
            return b()

        print(a())
        """, hint="Поиск идёт от ближайшей объемлющей функции наружу."),
    cod(f"{P}-m2-l1-e3", t("""
        Напиши функцию `make_formatter(prefix)`, внутри которой объяви функцию `fmt(message)`, возвращающую `"<prefix>: <message>"`. Вложенная функция должна брать `prefix` из **объемлющей** области. `make_formatter` возвращает результат `fmt("готово")`.

        ```
        make_formatter("INFO")   # → "INFO: готово"
        ```
        """),
        """
        def make_formatter(prefix):
            pass
        """,
        """
        def test_value():
            assert make_formatter("INFO") == "INFO: готово" and make_formatter("ERR") == "ERR: готово", "Неверная строка"
        """,
        """
        def make_formatter(prefix):
            def fmt(message):
                return f"{prefix}: {message}"
            return fmt("готово")
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `which_scope()`, возвращающую список из трёх строк: значение переменной `level`, полученное из **трёх** уровней.

        Структура:
        - глобальная `level = "G"` (уже в заготовке);
        - внутри `which_scope` — `level = "E"` и вложенная функция `inner()`, где `level = "L"`;
        - `inner` возвращает свою `level`, а `which_scope` возвращает `[inner(), level, глобальная level]`.

        ```
        which_scope()   # → ["L", "E", "G"]
        ```
        Глобальную прочитай через `globals()["level"]`.
        """),
        """
        level = "G"

        def which_scope():
            pass
        """,
        """
        def test_value():
            assert which_scope() == ["L", "E", "G"], f"Получено {which_scope()}"
        """,
        """
        level = "G"

        def which_scope():
            level = "E"
            def inner():
                level = "L"
                return level
            return [inner(), level, globals()["level"]]
        """),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `count_items(items)`, которая использует встроенную `len` — **но** в заготовке глобально объявлена переменная `len = 5`, которая «ломает» встроенную функцию.

        Исправь заготовку так, чтобы `count_items` работала: удали затеняющую переменную.

        ```
        count_items([1, 2, 3])   # → 3
        ```
        """),
        """
        len = 5

        def count_items(items):
            return len(items)
        """,
        """
        def test_value():
            assert count_items([1, 2, 3]) == 3 and count_items([]) == 0, "count_items должна вернуть длину"
        """,
        """
        def count_items(items):
            return len(items)
        """),
    cod(f"{P}-m2-l1-e7", t("""
        Есть глобальный разделитель `SEPARATOR = "-"`. Напиши функцию `make_labels(prefix, n)`: внутри неё вложенная функция `label(i)` берёт `prefix` из объемлющей области, а `SEPARATOR` — из глобальной. Вернуть список меток для `i` от 1 до `n`.

        ```
        make_labels("id", 3)   # → ["id-1", "id-2", "id-3"]
        ```
        """),
        """
        SEPARATOR = "-"

        def make_labels(prefix, n):
            pass
        """,
        """
        def test_values():
            assert make_labels("id", 3) == ["id-1", "id-2", "id-3"] and make_labels("x", 0) == [], "Неверные метки"

        def test_reads_global():
            g = make_labels.__globals__
            old = g["SEPARATOR"]
            g["SEPARATOR"] = "_"
            try:
                assert make_labels("a", 1) == ["a_1"], "Разделитель должен браться из глобальной SEPARATOR"
            finally:
                g["SEPARATOR"] = old
        """,
        """
        SEPARATOR = "-"

        def make_labels(prefix, n):
            def label(i):
                return f"{prefix}{SEPARATOR}{i}"
            return [label(i) for i in range(1, n + 1)]
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Функция `price_list(prices, rate)` падает с `UnboundLocalError`: во вложенной функции строка `rate = rate / 100` делает `rate` **локальной** для `with_rate`. Исправь, заведя переменную с другим именем.

        ```
        price_list([100, 50], 20)   # → [120.0, 60.0]
        ```
        """),
        """
        def price_list(prices, rate):
            def with_rate(p):
                rate = rate / 100
                return round(p * (1 + rate), 2)
            return [with_rate(p) for p in prices]
        """,
        """
        def test_values():
            assert price_list([100, 50], 20) == [120.0, 60.0] and price_list([], 5) == [], "Неверные цены"
        """,
        """
        def price_list(prices, rate):
            def with_rate(p):
                r = rate / 100
                return round(p * (1 + r), 2)
            return [with_rate(p) for p in prices]
        """),
),

lesson(f"{P}-nested", "Вложенные функции",
    out(f"{P}-nested-e1", "Что выведет программа?", """
        def outer():
            def helper(x):
                return x * 2
            return helper(5)

        print(outer())
        try:
            helper(1)
        except NameError:
            print("helper снаружи не виден")
        """),
    out(f"{P}-nested-e2", "Что выведет программа? Вложенная функция видит параметры внешней.", """
        def greet_all(greeting, names):
            def one(name):
                return f"{greeting}, {name}!"
            return [one(n) for n in names]

        print(greet_all("Привет", ["Аня", "Боря"]))
        """),
    out(f"{P}-nested-e3", "Что выведет программа? Значение берётся в момент вызова.", """
        def outer():
            msg = "раз"
            def show():
                return msg
            first = show()
            msg = "два"
            return first, show()

        print(outer())
        """),
    cod(f"{P}-nested-e4", t("""
        Напиши функцию `missing_fields(user)` — список обязательных полей `["name", "email"]`, которых нет в словаре `user` или которые пустые.

        Внутри объяви вложенную функцию `is_filled(field)`, которая проверяет одно поле (читая `user` из объемлющей области).

        ```
        missing_fields({"name": "Аня", "email": ""})   # → ["email"]
        missing_fields({})                             # → ["name", "email"]
        ```
        """),
        """
        def missing_fields(user):
            pass
        """,
        """
        def test_values():
            got = [missing_fields({"name": "Аня", "email": ""}), missing_fields({}), missing_fields({"name": "a", "email": "b"})]
            assert got == [["email"], ["name", "email"], []], f"Получено {got}"
        """,
        """
        def missing_fields(user):
            def is_filled(field):
                return bool(user.get(field))
            return [f for f in ["name", "email"] if not is_filled(f)]
        """, hint='user.get(field) вернёт None, если поля нет; bool("") — False.'),
    cod(f"{P}-nested-e5", t("""
        Напиши функцию `format_table(rows)` — список строк таблицы, где значения каждой строки склеены через `" | "`. Преобразование одной строки вынеси во вложенную функцию `fmt_row(row)`; значения превращай в строки через `str`.

        ```
        format_table([["id", "name"], [1, "Аня"]])   # → ["id | name", "1 | Аня"]
        ```
        """),
        """
        def format_table(rows):
            pass
        """,
        """
        def test_values():
            assert format_table([["id", "name"], [1, "Аня"]]) == ["id | name", "1 | Аня"] and format_table([]) == [], "Неверная таблица"
        """,
        """
        def format_table(rows):
            def fmt_row(row):
                return " | ".join(str(x) for x in row)
            return [fmt_row(r) for r in rows]
        """),
    cod(f"{P}-nested-e6", t("""
        Напиши функцию `stats(nums)` — пара `(среднее, размах)`, где размах = максимум − минимум. Внутри объяви две вложенные функции без параметров — `mean()` и `spread()`, — которые берут `nums` из объемлющей области. Для пустого списка — `(0, 0)`.

        ```
        stats([2, 4, 9])   # → (5.0, 7)
        ```
        """),
        """
        def stats(nums):
            pass
        """,
        """
        def test_values():
            assert stats([2, 4, 9]) == (5.0, 7) and stats([]) == (0, 0) and stats([3]) == (3.0, 0), "Неверный результат"
        """,
        """
        def stats(nums):
            def mean():
                return sum(nums) / len(nums)
            def spread():
                return max(nums) - min(nums)
            if not nums:
                return (0, 0)
            return (mean(), spread())
        """),
    cod(f"{P}-nested-e7", t("""
        Напиши функцию `clean_all(texts, chars)` — очистить каждую строку от символов `chars` по краям (`strip(chars)`) и привести к нижнему регистру. Одну строку обрабатывает вложенная `clean(text)`, которая берёт `chars` из объемлющей области.

        ```
        clean_all(["**Аня**", "*БОРЯ"], "*")   # → ["аня", "боря"]
        ```
        """),
        """
        def clean_all(texts, chars):
            pass
        """,
        """
        def test_values():
            assert clean_all(["**Аня**", "*БОРЯ"], "*") == ["аня", "боря"] and clean_all([" x "], " ") == ["x"], "Неверная очистка"
        """,
        """
        def clean_all(texts, chars):
            def clean(text):
                return text.strip(chars).lower()
            return [clean(t) for t in texts]
        """),
    cod(f"{P}-nested-e8", t("""
        Напиши функцию `flatten(data)` — «сплющить» вложенные списки любой глубины. Используй вложенную **рекурсивную** функцию `walk(item)`, которая добавляет числа в список `result` внешней функции (метод `append` меняет объект — `nonlocal` не нужен).

        ```
        flatten([1, [2, [3, 4]], 5])   # → [1, 2, 3, 4, 5]
        ```
        """),
        """
        def flatten(data):
            pass
        """,
        """
        def test_values():
            assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5] and flatten([]) == [] and flatten([[[]]]) == [], "Неверный результат"
        """,
        """
        def flatten(data):
            result = []
            def walk(item):
                if isinstance(item, list):
                    for x in item:
                        walk(x)
                else:
                    result.append(item)
            walk(data)
            return result
        """, xp=20),
),

lesson(f"{P}-m2-l2", "nonlocal",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        def outer():
            count = 0
            def inc():
                nonlocal count
                count += 1
            inc()
            inc()
            return count

        print(outer())
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа? Список меняется без nonlocal.", """
        def outer():
            log = []
            total = 0
            def add(x):
                log.append(x)
            add(1)
            add(2)
            return log, total

        print(outer())
        """, hint="append меняет объект, а не переменную; присваивания нет — nonlocal не нужен."),
    out(f"{P}-m2-l2-e6", "Что выведет программа? С nonlocal и без.", """
        def outer():
            x = 1
            def no():
                x = 2
            def yes():
                nonlocal x
                x = 3
            no()
            a = x
            yes()
            return a, x

        print(outer())
        """),
    cod(f"{P}-m2-l2-e3", t("""
        Функция `sum_with_helper(nums)` должна суммировать числа через вложенную функцию `add(x)`, которая увеличивает переменную `total` внешней функции. Сейчас она падает с `UnboundLocalError`.

        Исправь с помощью `nonlocal`.

        ```
        sum_with_helper([1, 2, 3])   # → 6
        ```
        """),
        """
        def sum_with_helper(nums):
            total = 0
            def add(x):
                total += x
            for n in nums:
                add(n)
            return total
        """,
        """
        def test_value():
            assert sum_with_helper([1, 2, 3]) == 6 and sum_with_helper([]) == 0, "Неверная сумма"
        """,
        """
        def sum_with_helper(nums):
            total = 0
            def add(x):
                nonlocal total
                total += x
            for n in nums:
                add(n)
            return total
        """),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `make_counter()`, которая возвращает **функцию** `inc()`: каждый вызов `inc()` увеличивает внутренний счётчик на 1 и возвращает его. Используй `nonlocal`.

        ```
        c = make_counter()
        c(), c(), c()      # → 1, 2, 3
        d = make_counter()
        d()                # → 1   у каждого счётчика своё состояние
        ```
        """),
        """
        def make_counter():
            pass
        """,
        """
        def test_counter():
            c = make_counter()
            assert [c(), c(), c()] == [1, 2, 3], "Счётчик должен расти"
            d = make_counter()
            assert d() == 1 and c() == 4, "Счётчики независимы"

        def test_nonlocal():
            assert "nonlocal" in open("solution.py", encoding="utf-8").read(), "Используй nonlocal"
        """,
        """
        def make_counter():
            count = 0
            def inc():
                nonlocal count
                count += 1
                return count
            return inc
        """),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `make_accumulator(start=0)`, возвращающую функцию `add(x)`: она прибавляет `x` к накопленной сумме и возвращает новую сумму. Также у возвращаемой функции должна быть возможность **сбросить** сумму вызовом `add(reset=True)` (вернуть `start`).

        ```
        acc = make_accumulator(10)
        acc(5)            # → 15
        acc(5)            # → 20
        acc(reset=True)   # → 10
        acc(1)            # → 11
        ```
        """),
        """
        def make_accumulator(start=0):
            pass
        """,
        """
        def test_values():
            acc = make_accumulator(10)
            assert [acc(5), acc(5), acc(reset=True), acc(1)] == [15, 20, 10, 11], "Неверные суммы"
            other = make_accumulator()
            assert other(3) == 3, "Независимые аккумуляторы"
        """,
        """
        def make_accumulator(start=0):
            total = start
            def add(x=0, reset=False):
                nonlocal total
                if reset:
                    total = start
                else:
                    total += x
                return total
            return add
        """, xp=20),
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `make_toggle()` — возвращает функцию, которая при каждом вызове переключает внутреннее состояние (сначала `False`) и возвращает новое значение. Используй `nonlocal`.

        ```
        t = make_toggle()
        t(), t(), t()   # → True, False, True
        ```
        """),
        """
        def make_toggle():
            pass
        """,
        """
        def test_values():
            t = make_toggle()
            assert [t(), t(), t()] == [True, False, True], "Неверные значения"
            assert make_toggle()() is True, "Новый переключатель независим"

        def test_nonlocal():
            assert "nonlocal" in open("solution.py", encoding="utf-8").read(), "Используй nonlocal"
        """,
        """
        def make_toggle():
            state = False
            def toggle():
                nonlocal state
                state = not state
                return state
            return toggle
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `running_average()` — возвращает функцию `add(x)`, которая запоминает все переданные числа и возвращает **среднее** всех чисел на данный момент. Храни в замыкании сумму и количество, меняй их через `nonlocal`.

        ```
        avg = running_average()
        avg(10)   # → 10.0
        avg(20)   # → 15.0
        avg(0)    # → 10.0
        ```
        """),
        """
        def running_average():
            pass
        """,
        """
        def test_values():
            avg = running_average()
            assert [avg(10), avg(20), avg(0)] == [10.0, 15.0, 10.0], "Неверные средние"
        """,
        """
        def running_average():
            total = 0
            count = 0
            def add(x):
                nonlocal total, count
                total += x
                count += 1
                return total / count
            return add
        """, hint="nonlocal total, count — несколько имён через запятую."),
),

lesson(f"{P}-m2-l3", "Замыкания",
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        def multiplier(n):
            def mul(x):
                return x * n
            return mul

        double, triple = multiplier(2), multiplier(3)
        print(double(10), triple(10))
        """),
    out(f"{P}-m2-l3-e2", "Что выведет программа? Ловушка позднего связывания.", """
        funcs = []
        for i in range(3):
            funcs.append(lambda: i)
        print([f() for f in funcs])

        fixed = []
        for i in range(3):
            fixed.append(lambda i=i: i)
        print([f() for f in fixed])
        """, hint="Замыкание помнит переменную, а не её значение в момент создания."),
    out(f"{P}-m2-l3-e6", "Что выведет программа? Где хранится запомненное значение.", """
        def make_greeter(greeting):
            def greet(name):
                return f"{greeting}, {name}"
            return greet

        hi = make_greeter("Hi")
        print(hi("Ann"), hi.__name__)
        print(hi.__closure__[0].cell_contents)
        """),
    cod(f"{P}-m2-l3-e3", t("""
        Напиши функцию `make_validator(min_len)` — фабрику проверок: возвращает функцию, которая получает строку и возвращает `True`, если её длина не меньше `min_len`.

        ```
        check8 = make_validator(8)
        check8("12345678")   # → True
        check8("123")        # → False
        ```
        """),
        """
        def make_validator(min_len):
            pass
        """,
        """
        def test_values():
            check8, check2 = make_validator(8), make_validator(2)
            assert check8("12345678") is True and check8("123") is False and check2("ab") is True, "Неверная проверка"
        """,
        """
        def make_validator(min_len):
            def check(s):
                return len(s) >= min_len
            return check
        """),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `make_cache(func)` — возвращает новую функцию, которая вызывает `func(x)` только при **первом** обращении с этим `x`, а дальше берёт результат из словаря-кэша (в замыкании).

        У возвращаемой функции должен быть атрибут-счётчик реальных вызовов недоступен — поэтому проверка сделает сама: `func` будет считать свои вызовы.

        ```
        slow_square = ...   # считает вызовы
        fast = make_cache(slow_square)
        fast(4), fast(4), fast(5)    # → 16, 16, 25; реальных вызовов — 2
        ```
        """),
        """
        def make_cache(func):
            pass
        """,
        """
        def test_cache():
            calls = []
            def slow_square(x):
                calls.append(x)
                return x * x
            fast = make_cache(slow_square)
            assert [fast(4), fast(4), fast(5), fast(4)] == [16, 16, 25, 16], "Неверные результаты"
            assert calls == [4, 5], f"Реальные вызовы: {calls} — повторы должны браться из кэша"
        """,
        """
        def make_cache(func):
            cache = {}
            def cached(x):
                if x not in cache:
                    cache[x] = func(x)
                return cache[x]
            return cached
        """, xp=20),
    cod(f"{P}-m2-l3-e5", t("""
        Исправь ловушку позднего связывания: функция `make_handlers(names)` должна вернуть список функций, каждая из которых возвращает **свою** строку `"обработчик <имя>"`. Сейчас все возвращают последнее имя.

        ```
        hs = make_handlers(["a", "b", "c"])
        [h() for h in hs]   # → ["обработчик a", "обработчик b", "обработчик c"]
        ```
        """),
        """
        def make_handlers(names):
            handlers = []
            for name in names:
                handlers.append(lambda: f"обработчик {name}")
            return handlers
        """,
        """
        def test_values():
            hs = make_handlers(["a", "b", "c"])
            assert [h() for h in hs] == ["обработчик a", "обработчик b", "обработчик c"], f"Получено {[h() for h in hs]}"
        """,
        """
        def make_handlers(names):
            handlers = []
            for name in names:
                handlers.append(lambda name=name: f"обработчик {name}")
            return handlers
        """,
        hint="Зафиксируй значение аргументом по умолчанию: `lambda name=name: ...`."),
    cod(f"{P}-m2-l3-e7", t("""
        Напиши фабрику `make_url(base)` — возвращает функцию `url(path)`, которая склеивает базовый адрес и путь **ровно с одним** `/` между ними (лишние слэши на стыке убрать).

        ```
        api = make_url("https://api.shop.ru/")
        api("/users")   # → "https://api.shop.ru/users"
        api("items")    # → "https://api.shop.ru/items"
        ```
        """),
        """
        def make_url(base):
            pass
        """,
        """
        def test_values():
            api = make_url("https://api.shop.ru/")
            assert api("/users") == "https://api.shop.ru/users" and api("items") == "https://api.shop.ru/items", "Неверный адрес"
            assert make_url("http://x")("y") == "http://x/y", "Без слэшей — добавить один"
        """,
        """
        def make_url(base):
            def url(path):
                return base.rstrip("/") + "/" + path.lstrip("/")
            return url
        """),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши фабрику `make_limiter(max_calls)` — возвращает функцию `allow()`, которая первые `max_calls` раз возвращает `True`, а дальше — `False` (ограничитель частоты запросов).

        ```
        allow = make_limiter(2)
        allow(), allow(), allow()   # → True, True, False
        ```
        """),
        """
        def make_limiter(max_calls):
            pass
        """,
        """
        def test_values():
            allow = make_limiter(2)
            assert [allow(), allow(), allow(), allow()] == [True, True, False, False], "Неверные ответы"
            assert make_limiter(0)() is False, "Лимит 0 — сразу False"
        """,
        """
        def make_limiter(max_calls):
            calls = 0
            def allow():
                nonlocal calls
                if calls >= max_calls:
                    return False
                calls += 1
                return True
            return allow
        """),
),

lesson(f"{P}-closure2", "Замыкания на практике",
    out(f"{P}-closure2-e1", "Что выведет программа? Две функции — одно состояние.", """
        def make_account(balance):
            def deposit(x):
                nonlocal balance
                balance += x
                return balance
            def get():
                return balance
            return deposit, get

        dep, get = make_account(100)
        dep(50)
        print(get())
        dep2, get2 = make_account(0)
        print(get(), get2())
        """),
    out(f"{P}-closure2-e2", "Что выведет программа?", """
        def outer():
            items = []
            def add(x):
                items.append(x)
                return len(items)
            return add

        add = outer()
        print(add("a"), add("b"), add("c"))
        """),
    out(f"{P}-closure2-e3", "Что выведет программа? Фабрика против лямбды в цикле.", """
        def make(n):
            return lambda x: x + n

        fs = [make(i) for i in range(3)]
        print([f(10) for f in fs])
        gs = [lambda x: x + i for i in range(3)]
        print([g(10) for g in gs])
        """, hint="Каждый вызов make создаёт своё n. Лямбды во включении делят одну i."),
    cod(f"{P}-closure2-e4", t("""
        Напиши функцию `make_stack()` — возвращает **три** функции `(push, pop, size)`, работающие с одним общим списком в замыкании:

        - `push(x)` — положить элемент;
        - `pop()` — снять верхний и вернуть (для пустого — `None`);
        - `size()` — сколько элементов.

        ```
        push, pop, size = make_stack()
        push(1); push(2)
        pop(), size()   # → 2, 1
        ```
        """),
        """
        def make_stack():
            pass
        """,
        """
        def test_values():
            push, pop, size = make_stack()
            push(1)
            push(2)
            assert pop() == 2 and size() == 1 and pop() == 1 and pop() is None and size() == 0, "Неверная работа стека"
            p2, _, s2 = make_stack()
            p2("x")
            assert size() == 0 and s2() == 1, "Стеки независимы"
        """,
        """
        def make_stack():
            items = []
            def push(x):
                items.append(x)
            def pop():
                if not items:
                    return None
                return items.pop()
            def size():
                return len(items)
            return push, pop, size
        """, xp=20),
    cod(f"{P}-closure2-e5", t("""
        Напиши фабрику `make_converter(rates)` — `rates` это словарь курсов `{"USD": 90, "EUR": 100}`. Возвращает функцию `convert(amount, currency)`, которая переводит сумму в рубли. Неизвестная валюта — `None`.

        ```
        conv = make_converter({"USD": 90, "EUR": 100})
        conv(2, "USD")   # → 180
        conv(1, "JPY")   # → None
        ```
        """),
        """
        def make_converter(rates):
            pass
        """,
        """
        def test_values():
            conv = make_converter({"USD": 90, "EUR": 100})
            assert conv(2, "USD") == 180 and conv(1, "EUR") == 100 and conv(1, "JPY") is None, "Неверная конвертация"
        """,
        """
        def make_converter(rates):
            def convert(amount, currency):
                if currency not in rates:
                    return None
                return amount * rates[currency]
            return convert
        """),
    cod(f"{P}-closure2-e6", t("""
        Напиши функцию `make_counter_pair()` — возвращает пару функций `(inc, reset)` с общим счётчиком: `inc()` увеличивает и возвращает значение, `reset()` обнуляет и возвращает 0.

        ```
        inc, reset = make_counter_pair()
        inc(), inc(), reset(), inc()   # → 1, 2, 0, 1
        ```
        """),
        """
        def make_counter_pair():
            pass
        """,
        """
        def test_values():
            inc, reset = make_counter_pair()
            assert [inc(), inc(), reset(), inc()] == [1, 2, 0, 1], "Неверные значения"
        """,
        """
        def make_counter_pair():
            count = 0
            def inc():
                nonlocal count
                count += 1
                return count
            def reset():
                nonlocal count
                count = 0
                return count
            return inc, reset
        """),
    cod(f"{P}-closure2-e7", t("""
        Напиши функцию `compose(f, g)` — возвращает новую функцию, которая для `x` вычисляет `f(g(x))`.

        ```
        inc = lambda x: x + 1
        double = lambda x: x * 2
        compose(inc, double)(5)   # → 11
        compose(double, inc)(5)   # → 12
        ```
        """),
        """
        def compose(f, g):
            pass
        """,
        """
        def test_values():
            inc = lambda x: x + 1
            double = lambda x: x * 2
            assert compose(inc, double)(5) == 11 and compose(double, inc)(5) == 12, "Неверная композиция"
            assert compose(str.upper, str.strip)("  ok ") == "OK", "Работает с любыми функциями"
        """,
        """
        def compose(f, g):
            def composed(x):
                return f(g(x))
            return composed
        """),
    cod(f"{P}-closure2-e8", t("""
        Напиши фабрику `make_history(limit)` — возвращает функцию `add(item)`, которая запоминает элементы, хранит только **последние** `limit` штук и возвращает **копию** текущей истории.

        ```
        add = make_history(2)
        add("a")   # → ["a"]
        add("b")   # → ["a", "b"]
        add("c")   # → ["b", "c"]
        ```
        """),
        """
        def make_history(limit):
            pass
        """,
        """
        def test_values():
            add = make_history(2)
            assert [add("a"), add("b"), add("c")] == [["a"], ["a", "b"], ["b", "c"]], "Неверная история"

        def test_copy():
            add = make_history(3)
            h = add("x")
            h.append("хак")
            assert add("y") == ["x", "y"], "Возвращай копию, чтобы историю нельзя было испортить снаружи"
        """,
        """
        def make_history(limit):
            items = []
            def add(item):
                items.append(item)
                if len(items) > limit:
                    items.pop(0)
                return list(items)
            return add
        """, hint="list(items) — копия списка.", xp=20),
),
)
