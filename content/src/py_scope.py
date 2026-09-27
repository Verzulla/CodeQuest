"""Тема «Область видимости переменных»."""
from ._lib import cod, lesson, module, out, t, topic

P = "scp"

# ============================================================
m1 = module(f"{P}-m1", "Локальные и глобальные", "🏠", "Где живут переменные и как их менять",

lesson(f"{P}-m1-l1", "Локальные переменные", 
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        def f():
            x = 10
            return x * 2

        print(f())
        try:
            print(x)
        except NameError:
            print("x не существует снаружи")
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа? Одинаковые имена в разных функциях.", """
        def a():
            value = "из a"
            return value

        def b():
            value = "из b"
            return value

        print(a(), "|", b())
        """),
    cod(f"{P}-m1-l1-e3", t("""
        Напиши функцию `make_greeting(name)`, которая создаёт **локальную** переменную `greeting` со строкой `"Привет, <имя>!"` и возвращает её.

        После вызова переменная `greeting` не должна существовать снаружи — это проверит тест.

        Пример:
        ```
        make_greeting("Аня")   # → "Привет, Аня!"
        ```
        """),
        """
        def make_greeting(name):
            pass
        """,
        """
        def test_value():
            assert make_greeting("Аня") == "Привет, Аня!", "Неверное приветствие"

        def test_local():
            make_greeting("x")
            assert "greeting" not in globals(), "greeting не должна быть глобальной"
        """,
        """
        def make_greeting(name):
            greeting = f"Привет, {name}!"
            return greeting
        """),
    cod(f"{P}-m1-l1-e4", t("""
        В коде ошибка: результат вычисления внутри функции пытаются использовать снаружи по имени локальной переменной, и программа падает с `NameError`.

        Исправь: функция `total_price(prices)` должна **вернуть** сумму, а снаружи результат нужно сохранить в переменную `total` и напечатать.

        Ожидаемый вывод:
        ```
        450
        ```
        """),
        """
        def total_price(prices):
            s = sum(prices)

        total_price([100, 200, 150])
        print(s)
        """,
        """
        def test_output():
            assert OUTPUT.strip() == "450", f"Напечатано {OUTPUT.strip()!r}"

        def test_function():
            assert total_price([1, 2]) == 3, "total_price должна возвращать сумму"
            assert total == 450, "Результат сохрани в переменную total"
        """,
        """
        def total_price(prices):
            s = sum(prices)
            return s

        total = total_price([100, 200, 150])
        print(total)
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `call_counter_demo()`, которая **трижды** вызывает вложенную логику: внутри неё объяви функцию `step()`, у которой есть локальная переменная `n = 0`, увеличивающаяся на 1 и возвращаемая.

        Вернуть список результатов трёх вызовов `step()`.

        Результат покажет, что локальные переменные создаются **заново** при каждом вызове:
        ```
        call_counter_demo()   # → [1, 1, 1]
        ```
        """),
        """
        def call_counter_demo():
            pass
        """,
        """
        def test_values():
            assert call_counter_demo() == [1, 1, 1], f"Получено {call_counter_demo()}"
        """,
        """
        def call_counter_demo():
            def step():
                n = 0
                n += 1
                return n
            return [step(), step(), step()]
        """)),

lesson(f"{P}-m1-l2", "Глобальные переменные", 
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        TIMEOUT = 30

        def show():
            return f"таймаут {TIMEOUT}"

        print(show())
        TIMEOUT = 60
        print(show())
        """, hint="Функция читает глобальную переменную в момент вызова."),
    out(f"{P}-m1-l2-e2", "Что выведет программа? Присваивание создаёт локальную.", """
        x = "глобальная"

        def f():
            x = "локальная"
            return x

        print(f())
        print(x)
        """),
    cod(f"{P}-m1-l2-e3", t("""
        Есть глобальная константа `BASE_URL = "https://api.shop.ru"`. Напиши функцию `endpoint(path)`, которая **читает** её и возвращает полный адрес.

        Пример:
        ```
        endpoint("/users")   # → "https://api.shop.ru/users"
        ```
        """),
        """
        BASE_URL = "https://api.shop.ru"

        def endpoint(path):
            pass
        """,
        """
        def test_values():
            assert endpoint("/users") == "https://api.shop.ru/users", "Неверный адрес"

        def test_reads_global():
            g = endpoint.__globals__
            old = g["BASE_URL"]
            g["BASE_URL"] = "http://localhost"
            try:
                assert endpoint("/x") == "http://localhost/x", "Функция должна читать глобальную BASE_URL, а не хардкодить адрес"
            finally:
                g["BASE_URL"] = old
        """,
        """
        BASE_URL = "https://api.shop.ru"

        def endpoint(path):
            return BASE_URL + path
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `describe_env()`, которая возвращает строку `"<ENV>: <BROWSER>"`, используя глобальные настройки `ENV` и `BROWSER`, объявленные в заготовке.

        ```
        describe_env()   # → "staging: chrome"
        ```
        Не создавай внутри функции переменных с такими же именами.
        """),
        """
        ENV = "staging"
        BROWSER = "chrome"

        def describe_env():
            pass
        """,
        """
        def test_value():
            assert describe_env() == "staging: chrome", f"Получено {describe_env()!r}"
        """,
        """
        ENV = "staging"
        BROWSER = "chrome"

        def describe_env():
            return f"{ENV}: {BROWSER}"
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Функция `apply_tax` должна использовать глобальную ставку `TAX = 20`, но вместо этого всегда считает с нулевым налогом: внутри неё по ошибке создаётся **локальная** переменная `TAX = 0`.

        Исправь функцию — она должна читать глобальную ставку.

        ```
        apply_tax(100)   # → 120.0
        ```
        """),
        """
        TAX = 20

        def apply_tax(price):
            TAX = 0
            return price * (1 + TAX / 100)
        """,
        """
        def test_value():
            assert apply_tax(100) == 120.0, f"Получено {apply_tax(100)}"
        """,
        """
        TAX = 20

        def apply_tax(price):
            return price * (1 + TAX / 100)
        """)),

lesson(f"{P}-m1-l3", "global и почему лучше без него", 
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        counter = 0

        def increment():
            global counter
            counter += 1
            return counter

        increment()
        increment()
        print(counter)
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа? UnboundLocalError.", """
        total = 10

        def add():
            try:
                total += 5
            except UnboundLocalError as e:
                return "ошибка: " + type(e).__name__
            return total

        print(add())
        """, hint="Присваивание делает total локальной во всей функции, а читать её до присваивания нельзя."),
    cod(f"{P}-m1-l3-e3", t("""
        Функция `register()` должна увеличивать **глобальный** счётчик `users_count` на 1 и возвращать новое значение. Сейчас она падает с `UnboundLocalError`.

        Исправь с помощью `global`.

        ```
        register()   # → 1
        register()   # → 2
        ```
        """),
        """
        users_count = 0

        def register():
            users_count += 1
            return users_count
        """,
        """
        def test_values():
            g = register.__globals__
            g["users_count"] = 0
            assert register() == 1 and register() == 2 and g["users_count"] == 2, "Глобальный счётчик должен расти"
        """,
        """
        users_count = 0

        def register():
            global users_count
            users_count += 1
            return users_count
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Перепиши код **без `global`**: функция `add_points(score, points)` получает текущий счёт параметром и **возвращает** новый.

        Снаружи обнови переменную `score` результатом двух вызовов (+10, затем +5) и выведи её.

        Ожидаемый вывод:
        ```
        15
        ```
        """),
        """
        score = 0

        def add_points(points):
            global score
            score += points

        add_points(10)
        add_points(5)
        print(score)
        """,
        """
        import inspect

        def test_output():
            assert OUTPUT.strip() == "15", f"Напечатано {OUTPUT.strip()!r}"

        def test_pure():
            assert add_points(3, 4) == 7, "add_points(score, points) должна вернуть сумму"
            assert "global" not in open("solution.py", encoding="utf-8").read(), "Избавься от global"
        """,
        """
        def add_points(score, points):
            return score + points

        score = 0
        score = add_points(score, 10)
        score = add_points(score, 5)
        print(score)
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Сделай счётчик запросов **без `global`**: напиши класс-хранилище не нужно — используй **словарь** состояния, который передаётся в функцию.

        Функция `track(stats, endpoint)` увеличивает счётчик вызовов для `endpoint` в словаре `stats` (изменяя его) и возвращает новое значение счётчика.

        ```
        stats = {}
        track(stats, "/users")   # → 1
        track(stats, "/users")   # → 2
        track(stats, "/items")   # → 1
        stats                    # → {"/users": 2, "/items": 1}
        ```
        """),
        """
        def track(stats, endpoint):
            pass
        """,
        """
        def test_values():
            stats = {}
            assert [track(stats, "/users"), track(stats, "/users"), track(stats, "/items")] == [1, 2, 1], "Неверные счётчики"
            assert stats == {"/users": 2, "/items": 1}, f"Состояние: {stats}"

        def test_no_global():
            assert "global" not in open("solution.py", encoding="utf-8").read(), "Реши без global"
        """,
        """
        def track(stats, endpoint):
            stats[endpoint] = stats.get(endpoint, 0) + 1
            return stats[endpoint]
        """)),
)

# ============================================================
m2 = module(f"{P}-m2", "Вложенные функции", "🪆", "Правило LEGB, nonlocal и замыкания",

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
        """)),

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
        """, xp=20)),

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
        hint="Зафиксируй значение аргументом по умолчанию: `lambda name=name: ...`.")),
)

# ============================================================
m3 = module(f"{P}-m3", "Подводные камни", "⚠️", "Затенение, изменяемые объекты и области в циклах",

lesson(f"{P}-m3-l1", "Затенение имён", 
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        def f(sum):
            try:
                return sum([1, 2])
            except TypeError:
                return "sum затенён параметром"

        print(f(10))
        print(sum([1, 2]))
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа?", """
        id = 42
        try:
            print(id(object()) > 0)
        except TypeError:
            print("встроенная id сломана")
        del id
        print(callable(id))
        """),
    cod(f"{P}-m3-l1-e3", t("""
        Функция `stats(list)` падает: параметр назван `list`, и внутри не работает встроенная `list()`. Переименуй параметр в `items`, чтобы функция возвращала `(список_уникальных_элементов_по_порядку_первого_появления, количество)`.

        ```
        stats([3, 1, 3, 2, 1])   # → ([3, 1, 2], 5)
        ```
        """),
        """
        def stats(list):
            unique = list(dict.fromkeys(list))
            return unique, len(list)
        """,
        """
        import inspect

        def test_values():
            assert stats([3, 1, 3, 2, 1]) == ([3, 1, 2], 5), f"Получено {stats([3, 1, 3, 2, 1])}"

        def test_param_name():
            params = list(inspect.signature(stats).parameters)
            assert params == ["items"], f"Параметр должен называться items, сейчас {params}"
        """,
        """
        def stats(items):
            unique = list(dict.fromkeys(items))
            return unique, len(items)
        """),
    cod(f"{P}-m3-l1-e4", t("""
        В заготовке функция `find_max_id(users)` использует переменную `max` для текущего максимума — и из-за этого внутри не работает встроенная `max`. Перепиши её: верни наибольший `id` среди пользователей с помощью **встроенной** `max` и генератора. Не используй имена встроенных функций для переменных.

        ```
        find_max_id([{"id": 3}, {"id": 10}, {"id": 7}])   # → 10
        ```
        """),
        """
        def find_max_id(users):
            max = 0
            for u in users:
                if u["id"] > max:
                    max = u["id"]
            return max
        """,
        """
        def test_value():
            assert find_max_id([{"id": 3}, {"id": 10}, {"id": 7}]) == 10 and find_max_id([{"id": -5}]) == -5, "Неверный максимум"

        def test_uses_builtin():
            src = open("solution.py", encoding="utf-8").read()
            assert "max(" in src and "max =" not in src, "Используй встроенную max, не затеняя её"
        """,
        """
        def find_max_id(users):
            return max(u["id"] for u in users)
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `shadowed_builtins(names)` — из списка имён переменных вернуть те, что **совпадают с именами встроенных функций/типов** Python (в исходном порядке).

        Используй модуль `builtins`: имя встроенное, если `hasattr(builtins, name)`.

        ```
        shadowed_builtins(["items", "list", "user_id", "id", "total", "sum"])
        # → ["list", "id", "sum"]
        ```
        """),
        """
        import builtins

        def shadowed_builtins(names):
            pass
        """,
        """
        def test_values():
            got = shadowed_builtins(["items", "list", "user_id", "id", "total", "sum"])
            assert got == ["list", "id", "sum"], f"Получено {got}"
            assert shadowed_builtins([]) == [], "Пусто — пусто"
        """,
        """
        import builtins

        def shadowed_builtins(names):
            return [n for n in names if hasattr(builtins, n)]
        """)),

lesson(f"{P}-m3-l2", "Изменяемые объекты и области", 
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        items = []

        def add(x):
            items.append(x)

        def reset():
            items = []

        add(1)
        add(2)
        reset()
        print(items)
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа?", """
        def modify(lst):
            lst.append(99)
            lst = [0]
            lst.append(1)
            return lst

        data = [1]
        result = modify(data)
        print(data, result)
        """, hint="После `lst = [0]` имя внутри функции указывает на новый список."),
    cod(f"{P}-m3-l2-e3", t("""
        Функция `clear_log()` должна **очищать** глобальный список `LOG`, но сейчас не работает: она создаёт локальную переменную.

        Исправь **без `global`**, изменяя сам объект (например, `LOG.clear()`).

        ```
        LOG.append("x"); clear_log(); LOG   # → []
        ```
        """),
        """
        LOG = []

        def clear_log():
            LOG = []
        """,
        """
        def test_clear():
            LOG.append("x")
            LOG.append("y")
            clear_log()
            assert LOG == [], f"LOG не очищен: {LOG}"

        def test_no_global():
            assert "global" not in open("solution.py", encoding="utf-8").read(), "Реши без global — измени сам объект"
        """,
        """
        LOG = []

        def clear_log():
            LOG.clear()
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Функция `add_default_headers(headers)` должна вернуть **новый** словарь заголовков, дополненный `"Accept": "application/json"`, **не изменяя** переданный словарь. Сейчас она портит аргумент.

        ```
        h = {"Authorization": "Bearer x"}
        add_default_headers(h)   # → {"Authorization": "Bearer x", "Accept": "application/json"}
        h                        # → {"Authorization": "Bearer x"}   без изменений
        ```
        """),
        """
        def add_default_headers(headers):
            headers["Accept"] = "application/json"
            return headers
        """,
        """
        def test_new_dict():
            h = {"Authorization": "Bearer x"}
            result = add_default_headers(h)
            assert result == {"Authorization": "Bearer x", "Accept": "application/json"}, "Неверный результат"
            assert h == {"Authorization": "Bearer x"}, "Исходный словарь изменён"
        """,
        """
        def add_default_headers(headers):
            return {**headers, "Accept": "application/json"}
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `reset_in_place(items, value)` — заменить **всё содержимое** переданного списка одним элементом `value`, так чтобы изменение было видно через **все** ссылки на этот список. Функция ничего не возвращает.

        ```
        a = [1, 2, 3]
        b = a
        reset_in_place(a, 0)
        a, b     # → [0], [0]
        ```
        Используй присваивание срезом `items[:] = ...`.
        """),
        """
        def reset_in_place(items, value):
            items = [value]
        """,
        """
        def test_in_place():
            a = [1, 2, 3]
            b = a
            assert reset_in_place(a, 0) is None, "Функция ничего не возвращает"
            assert a == [0] and b == [0], f"a={a}, b={b}"
        """,
        """
        def reset_in_place(items, value):
            items[:] = [value]
        """)),

lesson(f"{P}-m3-l3", "Области в циклах и списочных включениях", 
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        for i in range(3):
            pass
        print("после for:", i)

        squares = [n * n for n in range(3)]
        try:
            print(n)
        except NameError:
            print("n из включения не видна")
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа?", """
        x = "снаружи"
        result = [x for x in ["a", "b"]]
        print(result, x)

        for x in ["c", "d"]:
            pass
        print(x)
        """, hint="Включение не трогает внешнюю x, а обычный цикл — перезаписывает."),
    cod(f"{P}-m3-l3-e3", t("""
        В функции `process(items)` баг: переменная цикла `item` используется **после** цикла, и для пустого списка функция падает с `UnboundLocalError`.

        Исправь: функция должна возвращать последний элемент списка, а для пустого — `None`.

        ```
        process([1, 2, 3])   # → 3
        process([])          # → None
        ```
        """),
        """
        def process(items):
            for item in items:
                pass
            return item
        """,
        """
        def test_values():
            assert process([1, 2, 3]) == 3 and process(["a"]) == "a", "Нужен последний элемент"
            assert process([]) is None, "Пустой список — None"
        """,
        """
        def process(items):
            last = None
            for item in items:
                last = item
            return last
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `name_after_loop(names)`, которая доказывает разницу областей: верни пару

        1. результат списочного включения `[n.upper() for n in names]`;
        2. значение внешней переменной `n`, которой **до** включения присвоено `"внешняя"` — она не должна измениться.

        ```
        name_after_loop(["a", "b"])   # → (["A", "B"], "внешняя")
        ```
        """),
        """
        def name_after_loop(names):
            n = "внешняя"
            pass
        """,
        """
        def test_values():
            assert name_after_loop(["a", "b"]) == (["A", "B"], "внешняя"), f"Получено {name_after_loop(['a', 'b'])}"
        """,
        """
        def name_after_loop(names):
            n = "внешняя"
            upper = [n.upper() for n in names]
            return upper, n
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `make_multipliers(n)` — список из `n` функций, где функция с индексом `i` умножает аргумент на `i`. Реши **списочным включением** с лямбдой и позаботься о позднем связывании.

        ```
        ms = make_multipliers(4)
        [m(10) for m in ms]   # → [0, 10, 20, 30]
        ```
        """),
        """
        def make_multipliers(n):
            return [lambda x: x * i for i in range(n)]
        """,
        """
        def test_values():
            ms = make_multipliers(4)
            assert [m(10) for m in ms] == [0, 10, 20, 30], f"Получено {[m(10) for m in ms]}"
        """,
        """
        def make_multipliers(n):
            return [lambda x, i=i: x * i for i in range(n)]
        """)),
)

TOPIC = topic("py-scope", "Область видимости переменных", "🔭", "#ff4b4b",
              "Локальные и глобальные переменные, LEGB, global, nonlocal и замыкания",
              m1, m2, m3, group="Python")
