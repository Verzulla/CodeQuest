"""Тема «lambda», модуль 2 «map, filter, reduce» — задания. Теория — в _lam_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "lam"

m2 = module(f"{P}-m2", "map, filter, reduce", "🔧", "Функции высшего порядка, reduce, замыкания, operator и partial",

lesson(f"{P}-m2-l1", "map и filter с лямбдами",
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
    cod(f"{P}-m2-l1-e7", t("""
        Напиши функцию `squares_of_evens(nums)` — квадраты чётных чисел через `filter` и `map` с лямбдами.

        ```
        squares_of_evens([1, 2, 3, 4])   # → [4, 16]
        ```
        """),
        """
        def squares_of_evens(nums):
            pass
        """,
        """
        def test_values():
            assert squares_of_evens([1, 2, 3, 4]) == [4, 16] and squares_of_evens([]) == [], "Неверный результат"

        def test_map_filter():
            src = open("solution.py", encoding="utf-8").read()
            assert "map(" in src and "filter(" in src, "Используй map и filter"
        """,
        """
        def squares_of_evens(nums):
            return list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, nums)))
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `parse_prices(raw)` — строки цен с запятой в качестве разделителя (`"12,5"`) превратить в `float` через `map` и лямбду.

        ```
        parse_prices(["12,5", "3", "0,99"])   # → [12.5, 3.0, 0.99]
        ```
        """),
        """
        def parse_prices(raw):
            pass
        """,
        """
        def test_values():
            assert parse_prices(["12,5", "3", "0,99"]) == [12.5, 3.0, 0.99] and parse_prices([]) == [], "Неверный результат"
        """,
        """
        def parse_prices(raw):
            return list(map(lambda s: float(s.replace(",", ".")), raw))
        """),
),

lesson(f"{P}-m2-l2", "reduce и замыкания",
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
    cod(f"{P}-m2-l2-e7", t("""
        Напиши фабрику `make_formatter(prefix)` — возвращает лямбду, которая для сообщения возвращает `"[<prefix>] <сообщение>"`.

        ```
        info = make_formatter("INFO")
        info("старт")   # → "[INFO] старт"
        ```
        """),
        """
        def make_formatter(prefix):
            pass
        """,
        """
        def test_values():
            info, err = make_formatter("INFO"), make_formatter("ERR")
            assert info("старт") == "[INFO] старт" and err("x") == "[ERR] x", "Неверный формат"
        """,
        """
        def make_formatter(prefix):
            return lambda msg: f"[{prefix}] {msg}"
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `product(nums)` — произведение чисел через `reduce` с начальным значением `1` (для пустого списка — `1`).
        """),
        """
        from functools import reduce

        def product(nums):
            pass
        """,
        """
        def test_values():
            assert [product([2, 3, 4]), product([]), product([5])] == [24, 1, 5], "Неверное произведение"
        """,
        """
        from functools import reduce

        def product(nums):
            return reduce(lambda a, b: a * b, nums, 1)
        """),
),

lesson(f"{P}-reduce", "reduce подробнее",
    out(f"{P}-reduce-e1", "Что выведет программа? Начальное значение.", """
        from functools import reduce
        print(reduce(lambda a, b: a + b, [1, 2, 3, 4]))
        print(reduce(lambda a, b: a + b, [5]))
        print(reduce(lambda a, b: a + b, [], 0))
        try:
            reduce(lambda a, b: a + b, [])
        except TypeError:
            print("пустой список без начального значения")
        """),
    out(f"{P}-reduce-e2", "Что выведет программа? Проследи шаги.", """
        from functools import reduce

        def step(acc, x):
            print(f"acc={acc}, x={x}")
            return acc * 10 + x

        print(reduce(step, [1, 2, 3]))
        """, hint="Без начального значения первый элемент сразу становится acc."),
    out(f"{P}-reduce-e3", "Что выведет программа? Накопление словаря.", """
        from functools import reduce
        words = ["a", "bb", "a"]
        counts = reduce(lambda d, w: {**d, w: d.get(w, 0) + 1}, words, {})
        print(counts)
        """),
    cod(f"{P}-reduce-e4", t("""
        Напиши функцию `digits_to_number(digits)` — собрать число из списка цифр через `reduce`: `acc * 10 + x`. Пустой список — `0`.

        ```
        digits_to_number([1, 2, 3])   # → 123
        ```
        """),
        """
        from functools import reduce

        def digits_to_number(digits):
            pass
        """,
        """
        def test_values():
            assert [digits_to_number([1, 2, 3]), digits_to_number([]), digits_to_number([0, 7])] == [123, 0, 7], "Неверное число"
        """,
        """
        from functools import reduce

        def digits_to_number(digits):
            return reduce(lambda acc, d: acc * 10 + d, digits, 0)
        """),
    cod(f"{P}-reduce-e5", t("""
        Напиши функцию `longest_word(words)` — самое длинное слово через `reduce` (при равенстве — первое); пустой список — `""`.
        """),
        """
        from functools import reduce

        def longest_word(words):
            pass
        """,
        """
        def test_values():
            assert [longest_word(["ab", "abcd", "xyzw"]), longest_word([])] == ["abcd", ""], "Неверный результат"

        def test_reduce():
            assert "reduce(" in open("solution.py", encoding="utf-8").read(), "Используй reduce"
        """,
        """
        from functools import reduce

        def longest_word(words):
            return reduce(lambda best, w: w if len(w) > len(best) else best, words, "")
        """),
    cod(f"{P}-reduce-e6", t("""
        Напиши функцию `merge_dicts(dicts)` — слить список словарей в один (более поздние важнее) через `reduce` с начальным `{}`.
        """),
        """
        from functools import reduce

        def merge_dicts(dicts):
            pass
        """,
        """
        def test_values():
            assert merge_dicts([{"a": 1}, {"b": 2}, {"a": 3}]) == {"a": 3, "b": 2} and merge_dicts([]) == {}, "Неверный результат"
        """,
        """
        from functools import reduce

        def merge_dicts(dicts):
            return reduce(lambda acc, d: {**acc, **d}, dicts, {})
        """),
    cod(f"{P}-reduce-e7", t("""
        Напиши функцию `flatten(lists)` — склеить список списков через `reduce` и `+`.
        """),
        """
        from functools import reduce

        def flatten(lists):
            pass
        """,
        """
        def test_values():
            assert flatten([[1, 2], [3], []]) == [1, 2, 3] and flatten([]) == [], "Неверный результат"
        """,
        """
        from functools import reduce

        def flatten(lists):
            return reduce(lambda acc, lst: acc + lst, lists, [])
        """),
    cod(f"{P}-reduce-e8", t("""
        Напиши функцию `compose_all(funcs)` — одна функция, применяющая функции списка **слева направо**: `compose_all([f, g])(x) == g(f(x))`. Пустой список — функция, возвращающая аргумент без изменений.

        ```
        compose_all([lambda x: x + 1, lambda x: x * 10])(2)   # → 30
        ```
        """),
        """
        from functools import reduce

        def compose_all(funcs):
            pass
        """,
        """
        def test_values():
            assert compose_all([lambda x: x + 1, lambda x: x * 10])(2) == 30, "Сначала +1, потом *10"
            assert compose_all([])(5) == 5 and compose_all([str.strip, str.upper])(" a ") == "A", "Неверный результат"
        """,
        """
        from functools import reduce

        def compose_all(funcs):
            return reduce(lambda f, g: lambda x: g(f(x)), funcs, lambda x: x)
        """, hint="Начни с «тождественной» функции lambda x: x и на каждом шаге оборачивай.", xp=25),
),

lesson(f"{P}-operator", "Модуль operator и functools.partial",
    out(f"{P}-operator-e1", "Что выведет программа?", """
        import operator
        from functools import reduce
        print(operator.add(2, 3), operator.mul(4, 5))
        print(reduce(operator.mul, [1, 2, 3, 4]))
        """, hint="operator.add(a, b) — то же, что lambda a, b: a + b."),
    out(f"{P}-operator-e2", "Что выведет программа? itemgetter.", """
        from operator import itemgetter
        pairs = [("b", 2), ("a", 3)]
        print(sorted(pairs, key=itemgetter(0)))
        get_name = itemgetter("name")
        print(get_name({"name": "Аня", "age": 25}))
        print(itemgetter(0, 2)("abc"))
        """),
    out(f"{P}-operator-e3", "Что выведет программа? partial.", """
        from functools import partial

        def power(base, exp):
            return base ** exp

        square = partial(power, exp=2)
        cube = partial(power, exp=3)
        print(square(5), cube(2))
        int2 = partial(int, base=2)
        print(int2("101"))
        """, hint="partial «замораживает» часть аргументов и возвращает новую функцию."),
    cod(f"{P}-operator-e4", t("""
        Напиши функцию `product(nums)` — произведение через `reduce` и `operator.mul` (начальное значение `1`).
        """),
        """
        import operator
        from functools import reduce

        def product(nums):
            pass
        """,
        """
        def test_values():
            assert [product([2, 3, 4]), product([])] == [24, 1], "Неверное произведение"

        def test_operator():
            assert "operator.mul" in open("solution.py", encoding="utf-8").read(), "Используй operator.mul"
        """,
        """
        import operator
        from functools import reduce

        def product(nums):
            return reduce(operator.mul, nums, 1)
        """),
    cod(f"{P}-operator-e5", t("""
        Напиши функцию `sort_by_second(pairs)` — пары по второму элементу через `itemgetter(1)`.
        """),
        """
        from operator import itemgetter

        def sort_by_second(pairs):
            pass
        """,
        """
        def test_values():
            assert sort_by_second([("a", 3), ("b", 1)]) == [("b", 1), ("a", 3)], "Неверный порядок"

        def test_itemgetter():
            assert "itemgetter(1)" in open("solution.py", encoding="utf-8").read(), "Используй itemgetter(1)"
        """,
        """
        from operator import itemgetter

        def sort_by_second(pairs):
            return sorted(pairs, key=itemgetter(1))
        """),
    cod(f"{P}-operator-e6", t("""
        Напиши функцию `names(users)` — список значений `"name"` из списка словарей через `map` и `itemgetter("name")`.
        """),
        """
        from operator import itemgetter

        def names(users):
            pass
        """,
        """
        def test_values():
            assert names([{"name": "Аня"}, {"name": "Боря"}]) == ["Аня", "Боря"] and names([]) == [], "Неверный результат"
        """,
        """
        from operator import itemgetter

        def names(users):
            return list(map(itemgetter("name"), users))
        """),
    cod(f"{P}-operator-e7", t("""
        Напиши функцию `make_parsers()` — вернуть пару функций `(from_bin, from_hex)`, созданных через `partial(int, base=...)`.

        ```
        from_bin, from_hex = make_parsers()
        from_bin("101"), from_hex("ff")   # → 5, 255
        ```
        """),
        """
        from functools import partial

        def make_parsers():
            pass
        """,
        """
        def test_values():
            from_bin, from_hex = make_parsers()
            assert from_bin("101") == 5 and from_hex("ff") == 255, "Неверный разбор"
        """,
        """
        from functools import partial

        def make_parsers():
            return partial(int, base=2), partial(int, base=16)
        """),
    cod(f"{P}-operator-e8", t("""
        Напиши функцию `log(message, level="DEBUG")` — строка `"[<level>] <message>"`, и создай через `partial` функцию `log_info`, у которой уровень всегда `"INFO"`.

        ```
        log("x")          # → "[DEBUG] x"
        log_info("старт") # → "[INFO] старт"
        ```
        """),
        """
        from functools import partial

        def log(message, level="DEBUG"):
            pass

        log_info = None
        """,
        """
        def test_values():
            assert log("x") == "[DEBUG] x" and log_info("старт") == "[INFO] старт", "Неверный лог"

        def test_partial():
            assert "partial(" in open("solution.py", encoding="utf-8").read(), "Создай log_info через partial"
        """,
        """
        from functools import partial

        def log(message, level="DEBUG"):
            return f"[{level}] {message}"

        log_info = partial(log, level="INFO")
        """),
),
)
