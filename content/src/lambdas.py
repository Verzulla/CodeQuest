"""Тема «Лямбда-функции»."""
from ._lib import t, cod, lesson, module, out, topic

P = "lam"

m1 = module(f"{P}-m1", "Основы lambda", "λ", "Анонимные функции и ключи сортировки",
    lesson(f"{P}-m1-l1", "Что такое lambda", """
        # Лямбда-функция

        `lambda` — короткая функция **без имени**, записанная в одно выражение:

        ```
        square = lambda x: x ** 2
        print(square(4))   # 16
        ```

        Это то же самое, что:
        ```
        def square(x):
            return x ** 2
        ```

        - После `lambda` — параметры, после `:` — **одно выражение**, его значение и возвращается.
        - `return` не пишут. Несколько строк, `if` как оператор, циклы — нельзя (тернарник можно!).
        - Параметров может быть несколько или ни одного: `lambda a, b: a + b`, `lambda: 42`.

        Главная польза — передать маленькую функцию **прямо в аргумент** другой функции.
        """,
        out(f"{P}-m1-l1-e1", "Что выведет программа?", """
            double = lambda x: x * 2
            print(double(21))
            print(double("ха"))
            """, hint="Для строки `*` означает повторение."),
        out(f"{P}-m1-l1-e2", "Что выведет программа?", """
            add = lambda a, b=10: a + b
            print(add(1, 2))
            print(add(5))
            """, hint="У `b` есть значение по умолчанию."),
        out(f"{P}-m1-l1-e3", "Что выведет программа? Лямбду можно вызвать сразу.", """
            print((lambda x, y: x * y)(6, 7))
            print((lambda: "без аргументов")())
            """),
        cod(f"{P}-m1-l1-e4", t("""
            Создай переменную `cube` и положи в неё лямбда-функцию, которая возводит число в куб.

            - Лямбда получает одно число `x`.
            - Возвращает `x` в третьей степени (`x * x * x` или `x ** 3`).

            Примеры использования:
            ```
            cube(3)    # → 27
            cube(-2)   # → -8
            ```
            Важно: именно `cube = lambda ...`, а не `def cube(...)` — тест это проверяет.
            """),
            "cube = ...\n",
            """
            def test_is_lambda():
                assert callable(cube) and cube.__name__ == "<lambda>", "cube должна быть лямбдой: cube = lambda x: ..."

            def test_values():
                assert cube(3) == 27 and cube(-2) == -8, "cube(3) → 27, cube(-2) → -8"
            """,
            "cube = lambda x: x ** 3\n"),
        cod(f"{P}-m1-l1-e5", t("""
            Создай переменную `is_even` — лямбду, которая проверяет, чётное ли число.

            - Получает: целое число.
            - Возвращает: `True`, если число чётное, иначе `False`.

            Примеры:
            ```
            is_even(4)   # → True
            is_even(7)   # → False
            ```
            Запись: `is_even = lambda n: ...`. Чётность проверяется остатком от деления на 2.
            """),
            "is_even = ...\n",
            """
            def test_is_lambda():
                assert callable(is_even) and is_even.__name__ == "<lambda>", "is_even должна быть лямбдой"

            def test_values():
                assert is_even(4) is True and is_even(7) is False, "is_even(4) → True, is_even(7) → False"
            """,
            "is_even = lambda n: n % 2 == 0\n"),
        cod(f"{P}-m1-l1-e6", t("""
            Создай переменную `sign` — лямбду, которая возвращает знак числа в виде символа.

            - Получает: число.
            - Возвращает строку:
              - `"+"` — если число больше нуля;
              - `"-"` — если меньше нуля;
              - `"0"` — если равно нулю.

            Примеры:
            ```
            sign(5)    # → "+"
            sign(-1)   # → "-"
            sign(0)    # → "0"
            ```
            В лямбде нельзя писать `if` как отдельную команду, но можно тернарный оператор — даже вложенный.
            """),
            "sign = ...\n",
            """
            def test_is_lambda():
                assert callable(sign) and sign.__name__ == "<lambda>", "sign должна быть лямбдой"

            def test_values():
                assert [sign(5), sign(-1), sign(0)] == ["+", "-", "0"], f"Получено {[sign(5), sign(-1), sign(0)]}"
            """,
            'sign = lambda x: "+" if x > 0 else "-" if x < 0 else "0"\n',
            xp=20),
    ),
    lesson(f"{P}-m1-l2", "key= в sorted, min, max", """
        # Лямбда как ключ

        `sorted`, `min`, `max` принимают аргумент `key` — функцию, которая говорит, **по чему сравнивать**:

        ```
        words = ["банан", "ёж", "яблоко"]
        sorted(words, key=len)                 # по длине
        sorted(words, key=lambda w: w[-1])     # по последней букве
        ```

        Со списком словарей:
        ```
        users = [{"name": "Аня", "age": 30}, {"name": "Боря", "age": 25}]
        youngest = min(users, key=lambda u: u["age"])
        ```

        - `reverse=True` — сортировка по убыванию.
        - Ключ может вернуть кортеж — тогда сравнение идёт по первому элементу, при равенстве по второму:
          `key=lambda u: (u["age"], u["name"])`.
        """,
        out(f"{P}-m1-l2-e1", "Что выведет программа?", """
            words = ["банан", "ёж", "яблоко", "кот"]
            print(sorted(words, key=len))
            """, hint="При равной длине порядок сохраняется как в исходном списке (сортировка стабильная)."),
        out(f"{P}-m1-l2-e2", "Что выведет программа?", """
            nums = [3, -10, 7, -2]
            print(max(nums, key=abs))
            print(sorted(nums, key=lambda x: -x))
            """),
        out(f"{P}-m1-l2-e3", "Что выведет программа?", """
            users = [("Аня", 30), ("Боря", 25), ("Вика", 30)]
            print(sorted(users, key=lambda u: (-u[1], u[0])))
            """, hint="Сначала по возрасту по убыванию (минус!), при равенстве — по имени."),
        cod(f"{P}-m1-l2-e4", t("""
            Напиши функцию `by_price(products)`, которая сортирует товары по цене.

            - Получает: `products` — список словарей вида `{"name": "чай", "price": 300}`.
            - Возвращает: **новый** список этих же товаров, отсортированный по цене **от дешёвых к дорогим**.

            Пример:
            ```
            by_price([{"name": "A", "price": 300},
                      {"name": "B", "price": 100},
                      {"name": "C", "price": 200}])
            # → [B (100), C (200), A (300)]
            ```
            Используй `sorted` с аргументом `key=lambda ...`.
            """),
            """
            def by_price(products):
                pass
            """,
            """
            def test_sort():
                data = [{"name": "A", "price": 300}, {"name": "B", "price": 100}, {"name": "C", "price": 200}]
                assert [p["name"] for p in by_price(data)] == ["B", "C", "A"], "Ожидался порядок B, C, A"
            """,
            """
            def by_price(products):
                return sorted(products, key=lambda p: p["price"])
            """),
        cod(f"{P}-m1-l2-e5", t("""
            Напиши функцию `slowest(tests)`, которая находит самый долгий тест.

            - Получает: `tests` — список пар `(имя_теста, время_в_секундах)`.
            - Возвращает: **имя** (строку) теста с наибольшим временем.

            Пример:
            ```
            slowest([("login", 1.2), ("search", 4.5), ("logout", 0.3)])   # → "search"
            ```
            Подсказка: `max` с `key=lambda ...` вернёт всю пару — из неё нужно взять имя.
            """),
            """
            def slowest(tests):
                pass
            """,
            """
            def test_basic():
                assert slowest([("login", 1.2), ("search", 4.5), ("logout", 0.3)]) == "search", "Самый долгий — search"
            """,
            """
            def slowest(tests):
                return max(tests, key=lambda t: t[1])[0]
            """,
            hint="`max(tests, key=lambda t: t[1])` вернёт пару, а нужно имя — возьми `[0]`."),
        cod(f"{P}-m1-l2-e6", t("""
            Напиши функцию `leaderboard(scores)`, которая строит таблицу лидеров.

            - Получает: `scores` — словарь `{имя: очки}`.
            - Возвращает: список **имён**, упорядоченный так:
              1. по очкам — от большего к меньшему;
              2. если очков поровну — по алфавиту.

            Пример:
            ```
            leaderboard({"Боря": 50, "Аня": 80, "Вика": 50, "Гоша": 10})
            # → ["Аня", "Боря", "Вика", "Гоша"]
            #    Аня — больше всех очков; у Бори и Вики поровну, поэтому по алфавиту
            ```
            Подсказка: ключ сортировки может быть кортежем, а «по убыванию» для чисел — это сортировка по `-очки`.
            """),
            """
            def leaderboard(scores):
                pass
            """,
            """
            def test_order():
                scores = {"Боря": 50, "Аня": 80, "Вика": 50, "Гоша": 10}
                assert leaderboard(scores) == ["Аня", "Боря", "Вика", "Гоша"], f"Получено {leaderboard(scores)}"
            """,
            """
            def leaderboard(scores):
                return sorted(scores, key=lambda name: (-scores[name], name))
            """,
            hint="Перебор словаря даёт ключи. Ключ сортировки — кортеж `(-очки, имя)`.", xp=20),
    ),
)

m2 = module(f"{P}-m2", "map, filter, reduce", "🔧", "Функции, которые принимают функции",
    lesson(f"{P}-m2-l1", "map и filter", """
        # map и filter

        `map(f, items)` — применяет функцию к каждому элементу:
        ```
        list(map(lambda x: x * 2, [1, 2, 3]))      # [2, 4, 6]
        list(map(str, [1, 2, 3]))                   # ['1', '2', '3']
        ```

        `filter(f, items)` — оставляет элементы, для которых функция вернула истину:
        ```
        list(filter(lambda x: x > 0, [3, -1, 5]))   # [3, 5]
        ```

        - Оба возвращают **ленивый итератор** — чтобы увидеть результат, оберни в `list()`.
        - Часто то же самое читабельнее генератором списка: `[x * 2 for x in items]`.
          Но `map`/`filter` полезно узнавать в чужом коде.
        """,
        out(f"{P}-m2-l1-e1", "Что выведет программа?", """
            print(list(map(lambda x: x ** 2, [1, 2, 3, 4])))
            print(list(filter(lambda x: x % 2, [1, 2, 3, 4])))
            """, hint="`x % 2` для нечётных равно 1 (истина), для чётных — 0 (ложь)."),
        out(f"{P}-m2-l1-e2", "Что выведет программа?", """
            words = ["api", "UI", "Docker"]
            print(list(map(str.upper, words)))
            print(list(map(len, words)))
            """, hint="Передавать можно любую функцию, не только лямбду."),
        out(f"{P}-m2-l1-e3", "Что выведет программа? `map` можно вызвать с двумя списками.", """
            print(list(map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30])))
            """),
        cod(f"{P}-m2-l1-e4", t("""
            Напиши функцию `to_ints(strings)`, которая превращает строки с числами в настоящие числа.

            - Получает: `strings` — список строк, в каждой записано целое число.
            - Возвращает: **список** целых чисел в том же порядке.

            Примеры:
            ```
            to_ints(["1", "20", "-3"])   # → [1, 20, -3]
            ```
            Используй `map`. Помни, что `map` возвращает не список, а итератор — оберни результат в `list(...)`.
            """),
            """
            def to_ints(strings):
                pass
            """,
            """
            def test_values():
                assert to_ints(["1", "20", "-3"]) == [1, 20, -3], f"Получено {to_ints(['1', '20', '-3'])}"

            def test_is_list():
                assert isinstance(to_ints(["1"]), list), "Верни именно список (оберни map в list)"
            """,
            """
            def to_ints(strings):
                return list(map(int, strings))
            """),
        cod(f"{P}-m2-l1-e5", t("""
            Напиши функцию `failed_codes(codes)`, которая отбирает коды ответов с ошибками.

            - Получает: `codes` — список HTTP-кодов ответов (числа).
            - Возвращает: список только тех кодов, которые **400 и больше** (ошибки клиента и сервера), в исходном порядке.

            Пример:
            ```
            failed_codes([200, 404, 201, 500, 302])   # → [404, 500]
            ```
            Используй `filter` с лямбдой и оберни результат в `list(...)`.
            """),
            """
            def failed_codes(codes):
                pass
            """,
            """
            def test_filter():
                assert failed_codes([200, 404, 201, 500, 302]) == [404, 500], f"Получено {failed_codes([200, 404, 201, 500, 302])}"
            """,
            """
            def failed_codes(codes):
                return list(filter(lambda c: c >= 400, codes))
            """),
        cod(f"{P}-m2-l1-e6", t("""
            Напиши функцию `emails(users)`, которая собирает email активных пользователей.

            - Получает: `users` — список словарей вида `{"email": "Anna@Mail.ru", "active": True}`.
            - Возвращает: список email **только активных** пользователей (`active` равно `True`), каждый email — в нижнем регистре.

            Пример:
            ```
            emails([
                {"email": "Anna@Mail.ru", "active": True},
                {"email": "bob@mail.ru",  "active": False},
                {"email": "VIKA@mail.ru", "active": True},
            ])
            # → ["anna@mail.ru", "vika@mail.ru"]
            ```
            Сначала `filter` (оставить активных), затем `map` (достать email и сделать `.lower()`).
            """),
            """
            def emails(users):
                pass
            """,
            """
            def test_emails():
                users = [
                    {"email": "Anna@Mail.ru", "active": True},
                    {"email": "bob@mail.ru", "active": False},
                    {"email": "VIKA@mail.ru", "active": True},
                ]
                assert emails(users) == ["anna@mail.ru", "vika@mail.ru"], f"Получено {emails(users)}"
            """,
            """
            def emails(users):
                active = filter(lambda u: u["active"], users)
                return list(map(lambda u: u["email"].lower(), active))
            """,
            xp=20),
    ),
    lesson(f"{P}-m2-l2", "reduce и замыкания", """
        # reduce

        `functools.reduce(f, items, start)` сворачивает список в одно значение, применяя `f` к накопленному результату и очередному элементу:

        ```
        from functools import reduce
        reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0)   # ((((0+1)+2)+3)+4) = 10
        ```

        # Лямбды и замыкания

        Лямбда «видит» переменные вокруг себя. Функция может **создавать и возвращать** функцию:

        ```
        def multiplier(n):
            return lambda x: x * n

        triple = multiplier(3)
        triple(5)   # 15
        ```

        ⚠️ Ловушка позднего связывания: лямбды в цикле запоминают **переменную**, а не её значение в момент создания.
        ```
        funcs = [lambda: i for i in range(3)]
        [f() for f in funcs]   # [2, 2, 2]  — а не [0, 1, 2]!
        ```
        Лечится значением по умолчанию: `lambda i=i: i`.
        """,
        out(f"{P}-m2-l2-e1", "Что выведет программа?", """
            from functools import reduce
            print(reduce(lambda acc, x: acc * x, [1, 2, 3, 4], 1))
            print(reduce(lambda acc, x: acc + x, ["a", "b", "c"], ""))
            """),
        out(f"{P}-m2-l2-e2", "Что выведет программа?", """
            def adder(n):
                return lambda x: x + n

            plus5 = adder(5)
            plus10 = adder(10)
            print(plus5(1), plus10(1))
            """),
        out(f"{P}-m2-l2-e3", "Ловушка! Что выведет программа?", """
            funcs = [lambda: i for i in range(3)]
            print([f() for f in funcs])
            fixed = [lambda i=i: i for i in range(3)]
            print([f() for f in fixed])
            """, hint="Все лямбды первого списка смотрят на одну и ту же переменную i, которая к концу цикла стала 2."),
        cod(f"{P}-m2-l2-e4", t("""
            Напиши функцию `max_by_reduce(nums)`, которая находит максимум с помощью `reduce`.

            - Получает: `nums` — непустой список чисел.
            - Возвращает: наибольшее число.

            Примеры:
            ```
            max_by_reduce([3, 9, 2])   # → 9
            max_by_reduce([-5, -1])    # → -1
            ```
            Ограничения: без встроенной `max`. Используй `functools.reduce` и лямбду, которая из двух чисел возвращает большее.
            """),
            """
            from functools import reduce

            def max_by_reduce(nums):
                pass
            """,
            """
            def test_values():
                assert max_by_reduce([3, 9, 2]) == 9 and max_by_reduce([-5, -1]) == -1, "Максимум посчитан неверно"
            """,
            """
            from functools import reduce

            def max_by_reduce(nums):
                return reduce(lambda a, b: a if a > b else b, nums)
            """),
        cod(f"{P}-m2-l2-e5", t("""
            Напиши функцию `make_validator(min_len)` — «фабрику» проверок длины.

            - Получает: `min_len` — минимально допустимую длину строки.
            - Возвращает: **новую функцию**. Эта функция принимает строку и возвращает `True`, если длина строки не меньше `min_len`, иначе `False`.

            Пример:
            ```
            check8 = make_validator(8)   # получили функцию
            check8("12345678")           # → True
            check8("123")                # → False

            check2 = make_validator(2)   # у каждой проверки — свой min_len
            check2("ab")                 # → True
            ```
            """),
            """
            def make_validator(min_len):
                pass
            """,
            """
            def test_validator():
                check8 = make_validator(8)
                assert callable(check8), "make_validator должна вернуть функцию"
                assert check8("12345678") is True and check8("123") is False, "check8 проверяет длину ≥ 8"

            def test_independent():
                check2 = make_validator(2)
                assert check2("ab") is True, "Каждый валидатор помнит свой min_len"
            """,
            """
            def make_validator(min_len):
                return lambda s: len(s) >= min_len
            """),
        cod(f"{P}-m2-l2-e6", t("""
            Напиши функцию `compose(f, g)`, которая склеивает две функции в одну.

            - Получает: две функции `f` и `g`, каждая принимает одно значение.
            - Возвращает: **новую функцию**, которая для аргумента `x` сначала вызывает `g(x)`, а потом передаёт результат в `f`. То есть считает `f(g(x))`.

            Пример:
            ```
            inc = lambda x: x + 1
            dbl = lambda x: x * 2
            compose(inc, dbl)(5)   # → 11   сначала dbl(5) = 10, потом inc(10) = 11
            compose(dbl, inc)(5)   # → 12   сначала inc(5) = 6,  потом dbl(6) = 12
            ```
            """),
            """
            def compose(f, g):
                pass
            """,
            """
            def test_compose():
                inc = lambda x: x + 1
                dbl = lambda x: x * 2
                assert compose(inc, dbl)(5) == 11, "compose(inc, dbl)(5) = inc(dbl(5)) = 11"
                assert compose(dbl, inc)(5) == 12, "compose(dbl, inc)(5) = dbl(inc(5)) = 12"
            """,
            """
            def compose(f, g):
                return lambda x: f(g(x))
            """,
            xp=20),
    ),
)

TOPIC = topic("lambdas", "Лямбда-функции", "λ", "#ce82ff",
              "Анонимные функции, key=, map, filter, reduce и замыкания", m1, m2, group="Python")
