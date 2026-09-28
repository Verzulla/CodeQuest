"""Тема «lambda», модуль 1 «Основы lambda» — задания. Теория — в _lam_t1.py.

Слаги lam-* унаследованы от старой темы «Лямбда-функции» — так сохраняется прогресс."""
from ._lib import cod, lesson, module, out, t

P = "lam"

m1 = module(f"{P}-m1", "Основы lambda", "λ", "Синтаксис, ограничения, ключи сортировки и колбэки",

lesson(f"{P}-m1-l1", "Что такое lambda",
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
    cod(f"{P}-m1-l1-e7", t("""
        Создай лямбду `clamp` с тремя параметрами `x, lo, hi` — «зажать» число в границы: вернуть `lo`, если `x` меньше, `hi`, если больше, иначе `x`.

        ```
        clamp(15, 0, 10)   # → 10
        clamp(-3, 0, 10)   # → 0
        ```
        Подсказка: `max(lo, min(x, hi))`.
        """),
        "clamp = ...\n",
        """
        def test_is_lambda():
            assert callable(clamp) and clamp.__name__ == "<lambda>", "clamp должна быть лямбдой"

        def test_values():
            assert [clamp(15, 0, 10), clamp(-3, 0, 10), clamp(5, 0, 10)] == [10, 0, 5], "Неверный результат"
        """,
        "clamp = lambda x, lo, hi: max(lo, min(x, hi))\n"),
    cod(f"{P}-m1-l1-e8", t("""
        Создай лямбду `greet` с параметром `name`, у которого значение по умолчанию `"гость"`. Она возвращает `"Привет, <name>!"`.

        ```
        greet("Аня")   # → "Привет, Аня!"
        greet()        # → "Привет, гость!"
        ```
        """),
        "greet = ...\n",
        """
        def test_is_lambda():
            assert callable(greet) and greet.__name__ == "<lambda>", "greet должна быть лямбдой"

        def test_values():
            assert greet("Аня") == "Привет, Аня!" and greet() == "Привет, гость!", "Неверное приветствие"
        """,
        'greet = lambda name="гость": f"Привет, {name}!"\n'),
),

lesson(f"{P}-syntax", "Синтаксис и ограничения lambda",
    out(f"{P}-syntax-e1", "Что выведет программа? Разные параметры.", """
        f = lambda: "без параметров"
        g = lambda *args: len(args)
        h = lambda a, b=2, *, c=3: a + b + c
        print(f(), g(1, 2, 3), h(1), h(1, c=10))
        """),
    out(f"{P}-syntax-e2", "Что выведет программа? lambda и def.", """
        square = lambda x: x * x

        def square_def(x):
            return x * x

        print(square.__name__, square_def.__name__, square(5) == square_def(5))
        """, hint="У лямбды нет своего имени — только <lambda>."),
    out(f"{P}-syntax-e3", "Что выведет программа?", """
        parity = lambda n: "чёт" if n % 2 == 0 else "нечет"
        print([parity(n) for n in range(3)])
        print((lambda x: (x, x * 2))(4))
        """, hint="Вернуть несколько значений можно кортежем — в скобках."),
    cod(f"{P}-syntax-e4", t("""
        Создай лямбду `max2(a, b)` — большее из двух чисел, **без** встроенной `max`: используй условное выражение.
        """),
        "max2 = ...\n",
        """
        def test_is_lambda():
            assert callable(max2) and max2.__name__ == "<lambda>", "max2 должна быть лямбдой"
            assert "max(" not in open("solution.py", encoding="utf-8").read().replace("max2(", ""), "Без встроенной max"

        def test_values():
            assert [max2(3, 7), max2(9, 2), max2(4, 4)] == [7, 9, 4], "Неверный результат"
        """,
        "max2 = lambda a, b: a if a > b else b\n"),
    cod(f"{P}-syntax-e5", t("""
        Создай лямбду `count_args`, которая принимает **любое** количество позиционных аргументов и возвращает, сколько их передали.

        ```
        count_args(1, 2, 3)   # → 3
        count_args()          # → 0
        ```
        """),
        "count_args = ...\n",
        """
        def test_is_lambda():
            assert callable(count_args) and count_args.__name__ == "<lambda>", "count_args должна быть лямбдой"

        def test_values():
            assert [count_args(1, 2, 3), count_args()] == [3, 0], "Неверный результат"
        """,
        "count_args = lambda *args: len(args)\n"),
    cod(f"{P}-syntax-e6", t("""
        Создай лямбду `describe`, которая принимает любые **именованные** аргументы и возвращает строку `"k1=v1, k2=v2"` в порядке передачи.

        ```
        describe(a=1, b="x")   # → "a=1, b=x"
        ```
        """),
        "describe = ...\n",
        """
        def test_is_lambda():
            assert callable(describe) and describe.__name__ == "<lambda>", "describe должна быть лямбдой"

        def test_values():
            assert describe(a=1, b="x") == "a=1, b=x" and describe() == "", "Неверная строка"
        """,
        'describe = lambda **kw: ", ".join(f"{k}={v}" for k, v in kw.items())\n'),
    cod(f"{P}-syntax-e7", t("""
        В заготовке синтаксическая ошибка: внутри лямбды написан `return`. Исправь — лямбда `double` должна возвращать удвоенное число.
        """),
        "double = lambda x: return x * 2\n",
        """
        def test_values():
            assert double(4) == 8 and double.__name__ == "<lambda>", "double(4) → 8, и это должна остаться лямбда"
        """,
        "double = lambda x: x * 2\n", hint="После двоеточия лямбды — только выражение; return не пишут."),
    cod(f"{P}-syntax-e8", t("""
        По стилю PEP 8 лямбду не присваивают имени — для этого есть `def`. Перепиши `area` из заготовки обычной функцией с docstring `"Площадь прямоугольника."`.
        """),
        "area = lambda w, h: w * h\n",
        """
        def test_def():
            assert area.__name__ == "area", "Нужна обычная функция def area"
            assert area.__doc__ == "Площадь прямоугольника.", "Добавь docstring"
            assert area(3, 4) == 12, "Неверная площадь"
        """,
        '''
        def area(w, h):
            """Площадь прямоугольника."""
            return w * h
        '''),
),

lesson(f"{P}-m1-l2", "key= в sorted, min, max",
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
    cod(f"{P}-m1-l2-e7", t("""
        Напиши функцию `sort_by_domain(emails)` — адреса по домену (часть после `@`), при одинаковом домене — по всему адресу.

        ```
        sort_by_domain(["b@x.ru", "a@y.io", "a@x.ru"])   # → ["a@x.ru", "b@x.ru", "a@y.io"]
        ```
        """),
        """
        def sort_by_domain(emails):
            pass
        """,
        """
        def test_values():
            assert sort_by_domain(["b@x.ru", "a@y.io", "a@x.ru"]) == ["a@x.ru", "b@x.ru", "a@y.io"], "Неверный порядок"
        """,
        """
        def sort_by_domain(emails):
            return sorted(emails, key=lambda e: (e.split("@")[1], e))
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши функцию `oldest(users)` — имя самого старшего из списка словарей `name`, `age`; пустой список — `None`. Используй `max` с `key` и `default`.
        """),
        """
        def oldest(users):
            pass
        """,
        """
        def test_values():
            assert oldest([{"name": "a", "age": 20}, {"name": "b", "age": 40}]) == "b" and oldest([]) is None, "Неверный результат"
        """,
        """
        def oldest(users):
            best = max(users, key=lambda u: u["age"], default=None)
            return best["name"] if best else None
        """),
),

lesson(f"{P}-callbacks", "Функции как аргументы: колбэки",
    out(f"{P}-callbacks-e1", "Что выведет программа?", """
        def apply_twice(f, x):
            return f(f(x))

        print(apply_twice(lambda x: x + 3, 1), apply_twice(lambda s: s + "!", "ура"))
        """),
    out(f"{P}-callbacks-e2", "Что выведет программа? Две функции-параметра.", """
        def process(items, transform, keep):
            return [transform(x) for x in items if keep(x)]

        print(process([1, 2, 3, 4], lambda x: x * 10, lambda x: x % 2 == 0))
        """),
    out(f"{P}-callbacks-e3", "Что выведет программа?", """
        def retry(action, attempts, is_ok):
            for i in range(1, attempts + 1):
                result = action(i)
                if is_ok(result):
                    return i, result
            return None

        print(retry(lambda n: n * 100, 5, lambda r: r >= 300))
        """),
    cod(f"{P}-callbacks-e4", t("""
        Напиши функцию `apply_to_all(func, items)` — список результатов `func` для каждого элемента.

        ```
        apply_to_all(lambda x: x * x, [1, 2, 3])   # → [1, 4, 9]
        ```
        """),
        """
        def apply_to_all(func, items):
            pass
        """,
        """
        def test_values():
            assert apply_to_all(lambda x: x * x, [1, 2, 3]) == [1, 4, 9] and apply_to_all(str.upper, ["a"]) == ["A"], "Неверный результат"
        """,
        """
        def apply_to_all(func, items):
            return [func(x) for x in items]
        """),
    cod(f"{P}-callbacks-e5", t("""
        Напиши функцию `count_if(items, predicate)` — сколько элементов удовлетворяют условию-функции.

        ```
        count_if([1, -2, 3], lambda x: x > 0)   # → 2
        ```
        """),
        """
        def count_if(items, predicate):
            pass
        """,
        """
        def test_values():
            assert count_if([1, -2, 3], lambda x: x > 0) == 2 and count_if([], lambda x: True) == 0, "Неверный подсчёт"
        """,
        """
        def count_if(items, predicate):
            return sum(1 for x in items if predicate(x))
        """),
    cod(f"{P}-callbacks-e6", t("""
        Напиши функцию `find_first(items, predicate)` — первый элемент, для которого `predicate` вернул истину, или `None`.
        """),
        """
        def find_first(items, predicate):
            pass
        """,
        """
        def test_values():
            assert find_first([1, 8, 3, 9], lambda x: x > 5) == 8 and find_first([1], lambda x: x > 5) is None, "Неверный результат"
        """,
        """
        def find_first(items, predicate):
            for x in items:
                if predicate(x):
                    return x
            return None
        """),
    cod(f"{P}-callbacks-e7", t("""
        Напиши функцию `partition(items, predicate)` — пара списков `(подходящие, остальные)`.

        ```
        partition([1, 2, 3, 4], lambda x: x % 2 == 0)   # → ([2, 4], [1, 3])
        ```
        """),
        """
        def partition(items, predicate):
            pass
        """,
        """
        def test_values():
            assert partition([1, 2, 3, 4], lambda x: x % 2 == 0) == ([2, 4], [1, 3]) and partition([], bool) == ([], []), "Неверный результат"
        """,
        """
        def partition(items, predicate):
            yes, no = [], []
            for x in items:
                (yes if predicate(x) else no).append(x)
            return yes, no
        """),
    cod(f"{P}-callbacks-e8", t("""
        Напиши функцию `wait_for(check, max_attempts)` — вызывать `check(номер_попытки)` для попыток 1, 2, … до `max_attempts`; вернуть номер первой попытки, где `check` вернул истину, иначе `-1`.

        ```
        wait_for(lambda n: n >= 3, 5)   # → 3
        wait_for(lambda n: False, 2)    # → -1
        ```
        """),
        """
        def wait_for(check, max_attempts):
            pass
        """,
        """
        def test_values():
            assert [wait_for(lambda n: n >= 3, 5), wait_for(lambda n: False, 2), wait_for(lambda n: True, 1)] == [3, -1, 1], "Неверный результат"
        """,
        """
        def wait_for(check, max_attempts):
            for attempt in range(1, max_attempts + 1):
                if check(attempt):
                    return attempt
            return -1
        """),
),
)
