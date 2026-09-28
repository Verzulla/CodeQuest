"""Тема «Область видимости», модуль 1 «Локальные и глобальные» — задания. Теория — в _scp_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "scp"

m1 = module(f"{P}-m1", "Локальные и глобальные", "🏠", "Где живут переменные, параметры, UnboundLocalError и global",

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
    out(f"{P}-m1-l1-e6", "Что выведет программа? Каждый вызов — с чистого листа.", """
        def f():
            y = 1
            y += 1
            return y

        print(f(), f(), f())
        """, hint="Локальная y создаётся заново при каждом вызове."),
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
        """),
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `summary(nums)`, которая считает количество и сумму в **локальных** переменных `count` и `total` и возвращает строку `"n=<количество>, sum=<сумма>"`.

        После вызова переменные `count` и `total` не должны появиться снаружи.

        ```
        summary([1, 2, 3])   # → "n=3, sum=6"
        ```
        """),
        """
        def summary(nums):
            pass
        """,
        """
        def test_value():
            assert summary([1, 2, 3]) == "n=3, sum=6" and summary([]) == "n=0, sum=0", "Неверная строка"

        def test_local():
            summary([5])
            assert "count" not in globals() and "total" not in globals(), "count и total должны быть локальными"
        """,
        """
        def summary(nums):
            count = len(nums)
            total = sum(nums)
            return f"n={count}, sum={total}"
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Встроенная функция `locals()` возвращает словарь локальных переменных в текущий момент.

        Напиши функцию `describe(a, b)`, которая создаёт локальную `c = a + b` и возвращает **отсортированный список имён** своих локальных переменных: `sorted(locals())`.

        ```
        describe(1, 2)   # → ["a", "b", "c"]
        ```
        """),
        """
        def describe(a, b):
            pass
        """,
        """
        def test_value():
            assert describe(1, 2) == ["a", "b", "c"], f"Получено {describe(1, 2)}"
        """,
        """
        def describe(a, b):
            c = a + b
            return sorted(locals())
        """, hint="Параметры — тоже локальные переменные, поэтому a и b попадут в список."),
),

lesson(f"{P}-params", "Параметры — тоже локальные переменные",
    out(f"{P}-params-e1", "Что выведет программа?", """
        def change(x):
            x = x * 100
            return x

        n = 5
        print(change(n), n)
        """, hint="x — отдельное локальное имя; переприсваивание x не трогает n."),
    out(f"{P}-params-e2", "Что выведет программа?", """
        def rename(name):
            name = name.upper()
            print("внутри:", name)

        user = "аня"
        rename(user)
        print("снаружи:", user)
        """),
    out(f"{P}-params-e3", "Что выведет программа? У каждого вызова рекурсии — свои локальные.", """
        def depth(n):
            label = "уровень " + str(n)
            if n < 2:
                depth(n + 1)
            print(label)

        depth(0)
        """),
    cod(f"{P}-params-e4", t("""
        Программа должна напечатать очищенный email, но печатает исходный: функция меняет только свой параметр.

        Исправь: `normalize(text)` должна **возвращать** результат, а снаружи его нужно сохранить обратно в `email`.

        Ожидаемый вывод:
        ```
        anna@mail.ru
        ```
        """),
        """
        def normalize(text):
            text = text.strip().lower()

        email = "  Anna@Mail.RU "
        normalize(email)
        print(email)
        """,
        """
        def test_output():
            assert OUTPUT.strip() == "anna@mail.ru", f"Напечатано {OUTPUT.strip()!r}"

        def test_function():
            assert normalize(" X ") == "x", "normalize должна возвращать результат"
        """,
        """
        def normalize(text):
            text = text.strip().lower()
            return text

        email = "  Anna@Mail.RU "
        email = normalize(email)
        print(email)
        """),
    cod(f"{P}-params-e5", t("""
        Напиши функцию `clamp(value, low, high)` — «зажать» число в границы. Переприсваивай **сам параметр** `value` и верни его.

        ```
        clamp(15, 0, 10)   # → 10
        clamp(-3, 0, 10)   # → 0
        clamp(5, 0, 10)    # → 5
        ```
        """),
        """
        def clamp(value, low, high):
            pass
        """,
        """
        def test_values():
            assert [clamp(15, 0, 10), clamp(-3, 0, 10), clamp(5, 0, 10)] == [10, 0, 5], "Неверный результат"
        """,
        """
        def clamp(value, low, high):
            if value < low:
                value = low
            if value > high:
                value = high
            return value
        """),
    cod(f"{P}-params-e6", t("""
        Напиши функцию `greet(name=None)`: если имя не передано, внутри присвой параметру значение `"гость"`. Вернуть `"Привет, <имя>!"`.

        ```
        greet("Аня")   # → "Привет, Аня!"
        greet()        # → "Привет, гость!"
        ```
        """),
        """
        def greet(name=None):
            pass
        """,
        """
        def test_values():
            assert greet("Аня") == "Привет, Аня!" and greet() == "Привет, гость!", "Неверное приветствие"
        """,
        """
        def greet(name=None):
            if name is None:
                name = "гость"
            return f"Привет, {name}!"
        """),
    cod(f"{P}-params-e7", t("""
        Напиши функцию `double_n_times(x, n)` — удвоить `x` ровно `n` раз, **меняя параметр** `x` в цикле, и вернуть результат. Переменная снаружи, переданная как `x`, измениться не должна.

        ```
        start = 3
        double_n_times(start, 3)   # → 24
        start                      # → 3
        ```
        """),
        """
        def double_n_times(x, n):
            pass
        """,
        """
        def test_values():
            start = 3
            assert double_n_times(start, 3) == 24 and start == 3 and double_n_times(5, 0) == 5, "Неверный результат"
        """,
        """
        def double_n_times(x, n):
            for _ in range(n):
                x *= 2
            return x
        """),
    cod(f"{P}-params-e8", t("""
        Напиши **рекурсивную** функцию `countdown_str(n)` — строка обратного отсчёта от `n` до 1 через пробел и слово `"старт"` в конце. У каждого вызова свой параметр `n`.

        ```
        countdown_str(3)   # → "3 2 1 старт"
        countdown_str(0)   # → "старт"
        ```
        """),
        """
        def countdown_str(n):
            pass
        """,
        """
        def test_values():
            assert countdown_str(3) == "3 2 1 старт" and countdown_str(0) == "старт" and countdown_str(1) == "1 старт", "Неверная строка"
        """,
        """
        def countdown_str(n):
            if n == 0:
                return "старт"
            return f"{n} " + countdown_str(n - 1)
        """),
),

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
    out(f"{P}-m1-l2-e6", "Что выведет программа?", """
        LIMIT = 3

        def check(n):
            return n <= LIMIT

        print(check(2), check(5))
        LIMIT = 10
        print(check(5))
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
        """),
    cod(f"{P}-m1-l2-e7", t("""
        Есть глобальный список администраторов `ADMINS = ["root", "anna"]`. Напиши функцию `is_admin(user)`, которая **читает** этот список.

        ```
        is_admin("anna")   # → True
        is_admin("bob")    # → False
        ```
        """),
        """
        ADMINS = ["root", "anna"]

        def is_admin(user):
            pass
        """,
        """
        def test_values():
            assert is_admin("anna") is True and is_admin("bob") is False, "Неверный результат"

        def test_reads_global():
            g = is_admin.__globals__
            old = g["ADMINS"]
            g["ADMINS"] = ["bob"]
            try:
                assert is_admin("bob") is True, "Функция должна читать глобальный ADMINS"
            finally:
                g["ADMINS"] = old
        """,
        """
        ADMINS = ["root", "anna"]

        def is_admin(user):
            return user in ADMINS
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Программа падает с `NameError`: функцию вызывают **раньше**, чем создаётся глобальная переменная, которую она читает. Исправь порядок строк.

        Ожидаемый вывод:
        ```
        Привет, мир
        ```
        """),
        """
        def greet():
            return GREETING + ", мир"

        print(greet())
        GREETING = "Привет"
        """,
        """
        def test_output():
            assert OUTPUT.strip() == "Привет, мир", f"Напечатано {OUTPUT.strip()!r}"
        """,
        """
        def greet():
            return GREETING + ", мир"

        GREETING = "Привет"
        print(greet())
        """, hint="Глобальная переменная должна существовать к моменту вызова, а не к моменту def."),
),

lesson(f"{P}-unbound", "UnboundLocalError: почему имя стало локальным",
    out(f"{P}-unbound-e1", "Что выведет программа? Присваивание стоит ПОСЛЕ чтения.", """
        x = 1

        def f():
            print("до")
            try:
                print(x)
            except UnboundLocalError:
                print("UnboundLocalError")
            x = 2

        f()
        print(x)
        """, hint="Python решает, что x локальная, ещё до запуска функции — по наличию присваивания."),
    out(f"{P}-unbound-e2", "Что выведет программа? Присваивание в невыполненной ветке.", """
        value = "глобальная"

        def g(flag):
            if flag:
                value = "локальная"
            return value

        print(g(True))
        try:
            print(g(False))
        except UnboundLocalError:
            print("ошибка при flag=False")
        """),
    out(f"{P}-unbound-e3", "Что выведет программа? Цикл for тоже присваивает.", """
        i = 100

        def h():
            for i in range(3):
                pass
            return i

        print(h(), i)
        """),
    cod(f"{P}-unbound-e4", t("""
        Функция `total_pay(salary)` должна прибавлять глобальный бонус `BONUS = 1000`, но при зарплате больше 50000 бонус не положен. Сейчас она падает с `UnboundLocalError`.

        Исправь **без `global`**: заведи локальную переменную с другим именем. Глобальный `BONUS` меняться не должен.

        ```
        total_pay(40000)   # → 41000
        total_pay(60000)   # → 60000
        ```
        """),
        """
        BONUS = 1000

        def total_pay(salary):
            if salary > 50000:
                BONUS = 0
            return salary + BONUS
        """,
        """
        def test_values():
            assert total_pay(40000) == 41000 and total_pay(60000) == 60000, "Неверная выплата"
            assert total_pay.__globals__["BONUS"] == 1000, "Глобальный BONUS не должен меняться"

        def test_no_global():
            assert "global" not in open("solution.py", encoding="utf-8").read(), "Реши без global"
        """,
        """
        BONUS = 1000

        def total_pay(salary):
            bonus = 0 if salary > 50000 else BONUS
            return salary + bonus
        """),
    cod(f"{P}-unbound-e5", t("""
        Функция `log(msg)` должна добавлять сообщение в глобальный список `LOG`, но `LOG += [msg]` вызывает `UnboundLocalError` — `+=` тоже присваивание.

        Исправь **без `global`**: измени сам список методом.

        ```
        log("a"); log("b")
        LOG   # → ["a", "b"]
        ```
        """),
        """
        LOG = []

        def log(msg):
            LOG += [msg]
        """,
        """
        def test_values():
            LOG.clear()
            log("a")
            log("b")
            assert LOG == ["a", "b"], f"LOG = {LOG}"

        def test_no_global():
            assert "global" not in open("solution.py", encoding="utf-8").read(), "Реши без global — append"
        """,
        """
        LOG = []

        def log(msg):
            LOG.append(msg)
        """, hint="LOG.append(msg) — не присваивание, а вызов метода; имя остаётся глобальным."),
    cod(f"{P}-unbound-e6", t("""
        Python хранит имена локальных переменных функции в `func.__code__.co_varnames`.

        Напиши функцию `is_local(func, name)` — будет ли `name` **локальной** в функции `func`.

        ```
        def f(a):
            b = a
            return c
        is_local(f, "a"), is_local(f, "b"), is_local(f, "c")   # → True, True, False
        ```
        """),
        """
        def is_local(func, name):
            pass
        """,
        """
        def test_values():
            def f(a):
                b = a
                return c
            def g():
                for i in range(1):
                    pass
            assert [is_local(f, "a"), is_local(f, "b"), is_local(f, "c"), is_local(g, "i")] == [True, True, False, True], "Неверный результат"
        """,
        """
        def is_local(func, name):
            return name in func.__code__.co_varnames
        """),
    cod(f"{P}-unbound-e7", t("""
        Функция `sum_list(nums)` падает: внутри используется имя глобальной `total`, и `total = total + n` делает его локальным. Исправь: функция должна считать сумму в **собственной** локальной переменной, начиная с 0. Глобальная `total` меняться не должна.

        ```
        sum_list([1, 2, 3])   # → 6
        ```
        """),
        """
        total = 0

        def sum_list(nums):
            for n in nums:
                total = total + n
            return total
        """,
        """
        def test_values():
            assert sum_list([1, 2, 3]) == 6 and sum_list([]) == 0, "Неверная сумма"
            assert sum_list.__globals__["total"] == 0, "Глобальная total не должна меняться"
        """,
        """
        total = 0

        def sum_list(nums):
            total = 0
            for n in nums:
                total = total + n
            return total
        """),
    cod(f"{P}-unbound-e8", t("""
        Функция `circle_area(r)` падает с `UnboundLocalError` на строке с `math.pi` — хотя `math` импортирован вверху. Причина: **`import` внутри функции** тоже создаёт локальное имя. Исправь.

        ```
        circle_area(1)    # → 3.14
        circle_area(2)    # → 12.57
        ```
        """),
        """
        import math

        def circle_area(r):
            result = math.pi * r * r
            if r > 100:
                import math
            return round(result, 2)
        """,
        """
        def test_values():
            assert circle_area(1) == 3.14 and circle_area(2) == 12.57, "Неверная площадь"
        """,
        """
        import math

        def circle_area(r):
            result = math.pi * r * r
            return round(result, 2)
        """, hint="Строка import math внутри функции делает math локальным во ВСЕЙ функции."),
),

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
    out(f"{P}-m1-l3-e6", "Что выведет программа?", """
        x = 1

        def set_x():
            global x
            x = 5

        def read_x():
            return x

        print(read_x())
        set_x()
        print(read_x())
        """),
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
        """),
    cod(f"{P}-m1-l3-e7", t("""
        `global` может не только менять, но и **создавать** глобальную переменную.

        Напиши функцию `init_config()`, которая через `global` создаёт глобальную `CONFIG = {"debug": False}` и ничего не возвращает. До вызова `CONFIG` не существует.
        """),
        """
        def init_config():
            pass
        """,
        """
        def test_creates():
            g = init_config.__globals__
            g.pop("CONFIG", None)
            init_config()
            assert g.get("CONFIG") == {"debug": False}, "CONFIG должна появиться после вызова"

        def test_global():
            assert "global CONFIG" in open("solution.py", encoding="utf-8").read(), "Используй global CONFIG"
        """,
        """
        def init_config():
            global CONFIG
            CONFIG = {"debug": False}
        """),
    cod(f"{P}-m1-l3-e8", t("""
        Перепиши переключатель **без `global`**: функция `toggle(state)` принимает текущее состояние и возвращает противоположное. Снаружи обнови `dark_mode` двумя вызовами и напечатай значения после каждого.

        Ожидаемый вывод:
        ```
        True
        False
        ```
        """),
        """
        dark_mode = False

        def toggle():
            global dark_mode
            dark_mode = not dark_mode

        toggle()
        print(dark_mode)
        toggle()
        print(dark_mode)
        """,
        """
        def test_output():
            assert OUTPUT.split() == ["True", "False"], f"Напечатано {OUTPUT.split()}"

        def test_pure():
            assert toggle(True) is False and toggle(False) is True, "toggle(state) должна вернуть not state"
            assert "global" not in open("solution.py", encoding="utf-8").read(), "Избавься от global"
        """,
        """
        def toggle(state):
            return not state

        dark_mode = False
        dark_mode = toggle(dark_mode)
        print(dark_mode)
        dark_mode = toggle(dark_mode)
        print(dark_mode)
        """),
),
)
