"""Тема «Генераторы»."""
from ._lib import t, cod, lesson, module, out, topic

P = "gen"

m1 = module(f"{P}-m1", "Итераторы и yield", "♻️", "Как работает for и функции-генераторы",
    lesson(f"{P}-m1-l1", "Итераторы", """
        # Что происходит внутри for

        Цикл `for` работает с любым **итерируемым** объектом (список, строка, словарь, файл…). Под капотом:

        ```
        it = iter([10, 20])   # получаем итератор
        next(it)              # 10
        next(it)              # 20
        next(it)              # StopIteration — элементы кончились
        ```

        - `iter(obj)` — получить итератор, `next(it)` — следующий элемент.
        - Итератор **одноразовый**: пройдя его до конца, второй раз ничего не получишь.
        - `next(it, default)` вернёт `default` вместо исключения.
        """,
        out(f"{P}-m1-l1-e1", "Что выведет программа?", """
            it = iter("abc")
            print(next(it))
            print(next(it))
            print(next(it, "конец"))
            print(next(it, "конец"))
            """),
        out(f"{P}-m1-l1-e2", "Что выведет программа? Итератор одноразовый.", """
            it = iter([1, 2, 3])
            print(list(it))
            print(list(it))
            """),
        out(f"{P}-m1-l1-e3", "Что выведет программа?", """
            it = iter([1, 2, 3, 4])
            next(it)
            for x in it:
                print(x)
            """, hint="Первый элемент уже забрали вызовом next."),
        cod(f"{P}-m1-l1-e4", t("""
            Напиши функцию `first_two(items)`, которая берёт первые два элемента.

            - Получает: `items` — **любой** итерируемый объект: список, строку или даже итератор (у итератора нет индексов и срезов!).
            - Возвращает: список из первых двух элементов.

            Примеры:
            ```
            first_two([5, 6, 7])       # → [5, 6]
            first_two(iter("xyz"))     # → ["x", "y"]
            ```
            Используй `iter()` и два вызова `next()` — это работает для любого итерируемого.
            """),
            """
            def first_two(items):
                pass
            """,
            """
            def test_list():
                assert first_two([5, 6, 7]) == [5, 6], "first_two([5, 6, 7]) → [5, 6]"

            def test_iterator():
                assert first_two(iter("xyz")) == ["x", "y"], "Должно работать и с итератором, у которого нет срезов"
            """,
            """
            def first_two(items):
                it = iter(items)
                return [next(it), next(it)]
            """),
        cod(f"{P}-m1-l1-e5", t("""
            Допиши класс-итератор `Countdown` — обратный отсчёт.

            Объект `Countdown(n)` при переборе в цикле выдаёт числа `n, n-1, …, 1`, а потом заканчивается.

            Что нужно сделать — дописать метод `__next__` (остальное уже в заготовке):
            - если числа закончились (`self.n` дошёл до 0) — `raise StopIteration`;
            - иначе вернуть текущее число и уменьшить `self.n` на 1.

            Примеры:
            ```
            list(Countdown(3))   # → [3, 2, 1]
            list(Countdown(0))   # → []
            ```
            """),
            """
            class Countdown:
                def __init__(self, n):
                    self.n = n

                def __iter__(self):
                    return self

                def __next__(self):
                    pass
            """,
            """
            def test_list():
                assert list(Countdown(3)) == [3, 2, 1], f"Получено {list(Countdown(3))}"

            def test_zero():
                assert list(Countdown(0)) == [], "Countdown(0) — пусто"
            """,
            """
            class Countdown:
                def __init__(self, n):
                    self.n = n

                def __iter__(self):
                    return self

                def __next__(self):
                    if self.n <= 0:
                        raise StopIteration
                    self.n -= 1
                    return self.n + 1
            """,
            hint="В `__next__`: если n ≤ 0 — `raise StopIteration`, иначе уменьши n и верни прежнее значение.", xp=20),
    ),
    lesson(f"{P}-m1-l2", "yield", """
        # Функция-генератор

        Писать класс-итератор долго. Проще — функция с `yield`:

        ```
        def countdown(n):
            while n > 0:
                yield n
                n -= 1

        for x in countdown(3):
            print(x)          # 3 2 1
        ```

        - Вызов `countdown(3)` **не выполняет** код сразу — он возвращает объект-генератор.
        - Каждый `next()` выполняет код до следующего `yield`, отдаёт значение и **замирает**, запомнив все переменные.
        - Когда функция доходит до конца — генератор исчерпан (`StopIteration`).
        - Генератор **ленивый**: значения создаются по одному, когда их просят. Поэтому можно работать даже с бесконечными последовательностями.
        """,
        out(f"{P}-m1-l2-e1", "Что выведет программа?", """
            def gen():
                yield 1
                yield 2
                yield 3

            print(list(gen()))
            g = gen()
            print(next(g), next(g))
            """),
        out(f"{P}-m1-l2-e2", "Что выведет программа? Следи за порядком печати.", """
            def gen():
                print("старт")
                yield "A"
                print("середина")
                yield "B"
                print("конец")

            g = gen()
            print("создан")
            print(next(g))
            print(next(g))
            """, hint="Код генератора начинает выполняться только при первом next()."),
        out(f"{P}-m1-l2-e3", "Что выведет программа?", """
            def evens(limit):
                for i in range(limit):
                    if i % 2 == 0:
                        yield i

            print(sum(evens(10)))
            print(list(evens(5)))
            """),
        cod(f"{P}-m1-l2-e4", t("""
            Напиши функцию-генератор `squares(n)`, которая по очереди выдаёт квадраты чисел.

            - Получает: `n` — целое положительное число.
            - Выдаёт (через `yield`, по одному): `1², 2², …, n²`.

            Пример:
            ```
            list(squares(4))   # → [1, 4, 9, 16]
            ```
            Это должен быть именно генератор: в функции должен быть `yield`, а не `return` списка.
            """),
            """
            def squares(n):
                pass
            """,
            """
            import inspect

            def test_is_generator():
                assert inspect.isgeneratorfunction(squares), "squares должна быть генератором — используй yield"

            def test_values():
                assert list(squares(4)) == [1, 4, 9, 16], f"Получено {list(squares(4))}"
            """,
            """
            def squares(n):
                for i in range(1, n + 1):
                    yield i * i
            """),
        cod(f"{P}-m1-l2-e5", t("""
            Напиши **бесконечный** генератор `fibonacci()` — числа Фибоначчи.

            Последовательность начинается с `0, 1`, а каждое следующее число — сумма двух предыдущих:
            ```
            0, 1, 1, 2, 3, 5, 8, 13, 21, 34, …
            ```
            - Функция ничего не получает.
            - Выдаёт числа через `yield` бесконечно — не останавливается сама.

            Проверка возьмёт первые 10 чисел через `itertools.islice(fibonacci(), 10)`.
            Бесконечность не страшна: генератор ленивый и считает следующее число только когда его просят.
            """),
            """
            def fibonacci():
                pass
            """,
            """
            import inspect
            from itertools import islice

            def test_is_generator():
                assert inspect.isgeneratorfunction(fibonacci), "fibonacci должна быть генератором"

            def test_first_ten():
                assert list(islice(fibonacci(), 10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34], "Первые 10 чисел Фибоначчи неверны"
            """,
            """
            def fibonacci():
                a, b = 0, 1
                while True:
                    yield a
                    a, b = b, a + b
            """,
            hint="`while True:` + `yield a` + `a, b = b, a + b`. Бесконечность не страшна — генератор ленивый.", xp=20),
        cod(f"{P}-m1-l2-e6", t("""
            Напиши генератор `chunks(items, size)`, который режет последовательность на куски.

            - Получает: `items` — список или строку; `size` — длина куска.
            - Выдаёт по очереди куски длины `size`. Последний кусок может быть короче, если элементов не хватило.

            Примеры:
            ```
            list(chunks([1, 2, 3, 4, 5], 2))   # → [[1, 2], [3, 4], [5]]
            list(chunks("abcdef", 3))          # → ["abc", "def"]
            ```
            Удобно перебирать начала кусков через `range(0, len(items), size)` и брать срез.
            """),
            """
            def chunks(items, size):
                pass
            """,
            """
            def test_chunks():
                assert list(chunks([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]], f"Получено {list(chunks([1, 2, 3, 4, 5], 2))}"

            def test_exact():
                assert list(chunks("abcdef", 3)) == ["abc", "def"], "Должно работать и со строкой"
            """,
            """
            def chunks(items, size):
                for i in range(0, len(items), size):
                    yield items[i:i + size]
            """,
            hint="`range(0, len(items), size)` даёт начала кусков.", xp=20),
    ),
)

m2 = module(f"{P}-m2", "Генераторные выражения", "🌊", "Ленивые конвейеры и itertools",
    lesson(f"{P}-m2-l1", "Генераторные выражения", """
        # Круглые скобки вместо квадратных

        ```
        squares_list = [x * x for x in range(5)]   # список — всё сразу в памяти
        squares_gen  = (x * x for x in range(5))   # генератор — по одному по запросу
        ```

        - Генераторное выражение экономит память: `sum(x * x for x in range(10**8))` не создаёт огромный список.
        - Если выражение — единственный аргумент функции, вторые скобки не нужны: `sum(x for x in nums)`.
        - Генератор, как и итератор, **одноразовый**.
        - `any(...)` и `all(...)` останавливаются, как только ответ ясен — вместе с генератором это очень экономно.
        """,
        out(f"{P}-m2-l1-e1", "Что выведет программа?", """
            g = (x * 10 for x in range(3))
            print(type(g).__name__)
            print(list(g))
            print(list(g))
            """),
        out(f"{P}-m2-l1-e2", "Что выведет программа?", """
            nums = [3, 8, -1, 4]
            print(sum(n for n in nums if n > 0))
            print(any(n < 0 for n in nums))
            print(all(n < 10 for n in nums))
            """),
        out(f"{P}-m2-l1-e3", "Что выведет программа? Ленивость в действии.", """
            def noisy(x):
                print("считаю", x)
                return x > 1

            print(any(noisy(x) for x in [1, 2, 3, 4]))
            """, hint="any останавливается на первом True — дальше элементы не вычисляются."),
        cod(f"{P}-m2-l1-e4", t("""
            Напиши функцию `total_length(words)`, которая считает общую длину всех слов.

            - Получает: `words` — список строк.
            - Возвращает: сумму длин всех строк.

            Примеры:
            ```
            total_length(["api", "ui", "ci"])   # → 7    3 + 2 + 2
            total_length([])                    # → 0
            ```
            Реши одной строкой: `sum(...)` с генераторным выражением внутри.
            """),
            """
            def total_length(words):
                pass
            """,
            """
            def test_total():
                assert total_length(["api", "ui", "ci"]) == 7, "3 + 2 + 2 = 7"

            def test_empty():
                assert total_length([]) == 0, "Пустой список → 0"
            """,
            """
            def total_length(words):
                return sum(len(w) for w in words)
            """),
        cod(f"{P}-m2-l1-e5", t("""
            Напиши функцию `has_errors(log_lines)`, которая проверяет лог на ошибки.

            - Получает: `log_lines` — список строк лога.
            - Возвращает: `True`, если **хотя бы одна** строка начинается с `"ERROR"`, иначе `False`.

            Примеры:
            ```
            has_errors(["INFO start", "ERROR db down", "INFO end"])   # → True
            has_errors(["INFO ok", "WARN slow"])                      # → False
            ```
            Используй `any(...)` с генераторным выражением и метод строки `.startswith()`.
            """),
            """
            def has_errors(log_lines):
                pass
            """,
            """
            def test_yes():
                assert has_errors(["INFO start", "ERROR db down", "INFO end"]) is True, "Есть строка ERROR → True"

            def test_no():
                assert has_errors(["INFO ok", "WARN slow"]) is False, "Нет ERROR → False"
            """,
            """
            def has_errors(log_lines):
                return any(line.startswith("ERROR") for line in log_lines)
            """),
        cod(f"{P}-m2-l1-e6", t("""
            Напиши функцию `all_passed(results)`, которая проверяет, прошли ли все тесты.

            - Получает: `results` — список словарей вида `{"name": "login", "status": "passed"}`. Статус может быть `"passed"` или `"failed"`.
            - Возвращает: `True`, если у **всех** тестов статус `"passed"`, иначе `False`.

            Примеры:
            ```
            all_passed([{"name": "a", "status": "passed"}, {"name": "b", "status": "passed"}])   # → True
            all_passed([{"name": "a", "status": "passed"}, {"name": "b", "status": "failed"}])   # → False
            ```
            Используй `all(...)` с генераторным выражением.
            """),
            """
            def all_passed(results):
                pass
            """,
            """
            def test_true():
                assert all_passed([{"name": "a", "status": "passed"}, {"name": "b", "status": "passed"}]) is True, "Все passed → True"

            def test_false():
                assert all_passed([{"name": "a", "status": "passed"}, {"name": "b", "status": "failed"}]) is False, "Есть failed → False"
            """,
            """
            def all_passed(results):
                return all(r["status"] == "passed" for r in results)
            """),
    ),
    lesson(f"{P}-m2-l2", "Конвейеры и itertools", """
        # Конвейер из генераторов

        Генераторы удобно соединять в цепочку — каждый этап берёт данные у предыдущего:

        ```
        lines = ["INFO a", "ERROR b", "ERROR c"]
        errors = (l for l in lines if l.startswith("ERROR"))
        messages = (l.split()[1] for l in errors)
        print(list(messages))    # ['b', 'c']
        ```

        **yield from** — отдать все значения другого итерируемого:
        ```
        def both():
            yield from [1, 2]
            yield from "ab"
        ```

        **itertools** — стандартная библиотека полезных итераторов:
        - `islice(it, n)` — первые n элементов (даже из бесконечного генератора)
        - `count(start)` — бесконечный счётчик
        - `chain(a, b)` — склеить последовательности
        - `product(a, b)` — все комбинации (пригодится для матрицы тестов!)
        """,
        out(f"{P}-m2-l2-e1", "Что выведет программа?", """
            def both():
                yield from [1, 2]
                yield from "ab"

            print(list(both()))
            """),
        out(f"{P}-m2-l2-e2", "Что выведет программа?", """
            from itertools import count, islice
            print(list(islice(count(10, 5), 4)))
            """, hint="count(10, 5) — 10, 15, 20, … бесконечно; islice берёт первые 4."),
        out(f"{P}-m2-l2-e3", "Что выведет программа?", """
            from itertools import product
            for browser, os in product(["chrome", "firefox"], ["win", "mac"]):
                print(browser, os)
            """),
        cod(f"{P}-m2-l2-e4", t("""
            Напиши генератор `flatten(lists)`, который «распрямляет» список списков.

            - Получает: `lists` — список, элементы которого тоже списки (некоторые могут быть пустыми).
            - Выдаёт по одному все элементы вложенных списков подряд.

            Пример:
            ```
            list(flatten([[1, 2], [], [3], [4, 5]]))   # → [1, 2, 3, 4, 5]
            ```
            Для каждого вложенного списка используй `yield from` — он выдаёт все его элементы по очереди.
            """),
            """
            def flatten(lists):
                pass
            """,
            """
            import inspect

            def test_is_generator():
                assert inspect.isgeneratorfunction(flatten), "flatten должна быть генератором"

            def test_values():
                assert list(flatten([[1, 2], [], [3], [4, 5]])) == [1, 2, 3, 4, 5], f"Получено {list(flatten([[1, 2], [], [3], [4, 5]]))}"
            """,
            """
            def flatten(lists):
                for inner in lists:
                    yield from inner
            """),
        cod(f"{P}-m2-l2-e5", t("""
            Напиши генератор `error_messages(lines)`, который вытаскивает из лога тексты ошибок.

            - Получает: `lines` — строки лога в формате `"УРОВЕНЬ текст сообщения"`, например `"ERROR нет связи с БД"`. Уровень — первое слово до пробела.
            - Выдаёт: только **текст** (без слова `ERROR` и пробела) для строк с уровнем `ERROR`. Остальные строки пропускает.

            Пример:
            ```
            lines = ["INFO старт", "ERROR нет связи с БД", "WARN медленно", "ERROR таймаут"]
            list(error_messages(lines))   # → ["нет связи с БД", "таймаут"]
            ```
            Разделить строку по **первому** пробелу удобно методом `line.partition(" ")`.
            """),
            """
            def error_messages(lines):
                pass
            """,
            """
            import inspect

            def test_is_generator():
                assert inspect.isgeneratorfunction(error_messages), "Нужен генератор (yield)"

            def test_values():
                lines = ["INFO старт", "ERROR нет связи с БД", "WARN медленно", "ERROR таймаут"]
                assert list(error_messages(lines)) == ["нет связи с БД", "таймаут"], f"Получено {list(error_messages(lines))}"
            """,
            """
            def error_messages(lines):
                for line in lines:
                    level, _, text = line.partition(" ")
                    if level == "ERROR":
                        yield text
            """,
            hint="`line.partition(\" \")` делит строку по первому пробелу на три части.", xp=20),
        cod(f"{P}-m2-l2-e6", t("""
            Напиши функцию `test_matrix(browsers, sizes)` — матрицу кроссбраузерного прогона.

            - Получает: `browsers` — список браузеров; `sizes` — список ширин экрана.
            - Возвращает: список строк `"браузер@ширина"` для **всех комбинаций** — сначала все размеры для первого браузера, потом для второго и т. д.

            Пример:
            ```
            test_matrix(["chrome", "safari"], [1920, 375])
            # → ["chrome@1920", "chrome@375", "safari@1920", "safari@375"]
            ```
            Все комбинации в нужном порядке даёт `itertools.product(browsers, sizes)`.
            """),
            """
            from itertools import product

            def test_matrix(browsers, sizes):
                pass
            """,
            """
            def test_combinations():
                assert test_matrix(["chrome", "safari"], [1920, 375]) == ["chrome@1920", "chrome@375", "safari@1920", "safari@375"], \\
                    f"Получено {test_matrix(['chrome', 'safari'], [1920, 375])}"
            """,
            """
            from itertools import product

            def test_matrix(browsers, sizes):
                return [f"{b}@{s}" for b, s in product(browsers, sizes)]
            """,
            xp=20),
    ),
)

TOPIC = topic("generators", "Генераторы", "♻️", "#1cb0f6",
              "Итераторы, yield, ленивые вычисления и itertools", m1, m2, group="Python")
