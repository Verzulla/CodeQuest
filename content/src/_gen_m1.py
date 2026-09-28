"""Тема «Генераторы», модуль 1 «Итераторы и yield» — задания. Теория — в _gen_t1.py.

Слаги gen-m1-l1, gen-m1-l2 унаследованы от старой темы — так сохраняется прогресс."""
from ._lib import cod, lesson, module, out, t

P = "gen"

m1 = module(f"{P}-m1", "Итераторы и yield", "🔁", "iter и next, свой итератор, функции-генераторы, ленивость и одноразовость",

lesson(f"{P}-m1-l1", "Итераторы",
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
    out(f"{P}-m1-l1-e6", "Что выведет программа? Итерируемое и итератор.", """
        nums = [1, 2]
        it = iter(nums)
        print(iter(it) is it, iter(nums) is iter(nums))
        print(hasattr(nums, "__next__"), hasattr(it, "__next__"))
        """, hint="Список — итерируемый (можно получить итератор), но сам не итератор."),
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `my_sum(iterable)` — сумма элементов **без** `for` и `sum`: используй `iter()`, `next()` и перехват `StopIteration` в цикле `while True`.
        """),
        """
        def my_sum(iterable):
            pass
        """,
        """
        def test_values():
            assert my_sum([1, 2, 3]) == 6 and my_sum(range(5)) == 10 and my_sum([]) == 0, "Неверная сумма"
            src = open("solution.py", encoding="utf-8").read()
            assert "for " not in src and "sum(" not in src.replace("my_sum(", ""), "Без for и sum"
        """,
        """
        def my_sum(iterable):
            it = iter(iterable)
            total = 0
            while True:
                try:
                    total += next(it)
                except StopIteration:
                    return total
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `skip_header(lines)` — получить итератор по строкам, **пропустить первую** (заголовок) и вернуть список остальных. Пустой вход — пустой список. Используй `next(it, None)`.
        """),
        """
        def skip_header(lines):
            pass
        """,
        """
        def test_values():
            assert skip_header(["id,name", "1,a", "2,b"]) == ["1,a", "2,b"] and skip_header([]) == [] and skip_header(iter(["h"])) == [], "Неверный результат"
        """,
        """
        def skip_header(lines):
            it = iter(lines)
            next(it, None)
            return list(it)
        """, xp=20),
),

lesson(f"{P}-protocol", "Свой итератор: __iter__ и __next__",
    out(f"{P}-protocol-e1", "Что выведет программа?", """
        class Upto:
            def __init__(self, n):
                self.n = n
                self.current = 0

            def __iter__(self):
                return self

            def __next__(self):
                if self.current >= self.n:
                    raise StopIteration
                self.current += 1
                return self.current

        u = Upto(3)
        print(list(u))
        print(list(u))
        """, hint="Итератор, вернувший всё, остаётся пустым."),
    out(f"{P}-protocol-e2", "Что выведет программа? Итерируемый класс.", """
        class Playlist:
            def __init__(self, songs):
                self.songs = songs

            def __iter__(self):
                return iter(self.songs)

        p = Playlist(["a", "b"])
        print(list(p), list(p))
        for s in p:
            print(s.upper(), end=" ")
        print()
        """, hint="__iter__ каждый раз возвращает новый итератор — перебирать можно много раз."),
    out(f"{P}-protocol-e3", "Что выведет программа? for изнутри.", """
        items = ["x", "y"]
        it = iter(items)
        while True:
            try:
                item = next(it)
            except StopIteration:
                print("конец")
                break
            print("элемент", item)
        """, hint="Так устроен цикл for."),
    cod(f"{P}-protocol-e4", t("""
        Напиши класс-итератор `Countup(start, stop)` — выдаёт числа от `start` до `stop` включительно, затем `StopIteration`.
        """),
        """
        class Countup:
            pass
        """,
        """
        def test_values():
            assert list(Countup(3, 6)) == [3, 4, 5, 6] and list(Countup(5, 4)) == [], "Неверная последовательность"
            c = Countup(1, 2)
            assert iter(c) is c and next(c) == 1, "Протокол итератора"
        """,
        """
        class Countup:
            def __init__(self, start, stop):
                self.current = start
                self.stop = stop

            def __iter__(self):
                return self

            def __next__(self):
                if self.current > self.stop:
                    raise StopIteration
                value = self.current
                self.current += 1
                return value
        """),
    cod(f"{P}-protocol-e5", t("""
        Напиши класс `Cycle(items, times)` — итератор, который проходит по списку `items` по кругу `times` раз.

        ```
        list(Cycle(["a", "b"], 2))   # → ["a", "b", "a", "b"]
        ```
        """),
        """
        class Cycle:
            pass
        """,
        """
        def test_values():
            assert list(Cycle(["a", "b"], 2)) == ["a", "b", "a", "b"] and list(Cycle([1], 3)) == [1, 1, 1] and list(Cycle([], 5)) == [] and list(Cycle([1, 2], 0)) == [], "Неверный результат"
        """,
        """
        class Cycle:
            def __init__(self, items, times):
                self.items = items
                self.total = len(items) * times
                self.index = 0

            def __iter__(self):
                return self

            def __next__(self):
                if self.index >= self.total:
                    raise StopIteration
                value = self.items[self.index % len(self.items)]
                self.index += 1
                return value
        """),
    cod(f"{P}-protocol-e6", t("""
        Напиши класс `Range2(start, stop, step=1)` — **итерируемый** (не итератор!) аналог `range`: у него `__iter__` каждый раз возвращает новый итератор, поэтому объект можно перебирать много раз. Используй внутри `__iter__` генератор или `iter(...)`.
        """),
        """
        class Range2:
            pass
        """,
        """
        def test_values():
            r = Range2(0, 10, 3)
            assert list(r) == [0, 3, 6, 9] and list(r) == [0, 3, 6, 9], "Повторный перебор"
            assert list(Range2(2, 5)) == [2, 3, 4] and list(Range2(5, 2)) == [], "Шаг 1"
        """,
        """
        class Range2:
            def __init__(self, start, stop, step=1):
                self.start = start
                self.stop = stop
                self.step = step

            def __iter__(self):
                current = self.start
                while current < self.stop:
                    yield current
                    current += self.step
        """),
    cod(f"{P}-protocol-e7", t("""
        Напиши класс-итератор `Pages(items, size)` — выдаёт «страницы»: списки по `size` элементов (последняя может быть короче). Как пагинация в API.
        """),
        """
        class Pages:
            pass
        """,
        """
        def test_values():
            assert list(Pages([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]] and list(Pages([], 3)) == [], "Неверный результат"
        """,
        """
        class Pages:
            def __init__(self, items, size):
                self.items = items
                self.size = size
                self.pos = 0

            def __iter__(self):
                return self

            def __next__(self):
                if self.pos >= len(self.items):
                    raise StopIteration
                page = self.items[self.pos:self.pos + self.size]
                self.pos += self.size
                return page
        """),
    cod(f"{P}-protocol-e8", t("""
        Напиши класс-итератор `Peekable(iterable)` с методом `peek(default=None)` — посмотреть следующий элемент, **не забирая** его. Обычный `next` после `peek` должен вернуть тот же элемент.
        """),
        """
        class Peekable:
            pass
        """,
        """
        def test_values():
            p = Peekable(iter([1, 2]))
            assert p.peek() == 1 and p.peek() == 1 and next(p) == 1, "peek не забирает"
            assert next(p) == 2 and p.peek("пусто") == "пусто", "Конец"
            assert list(Peekable("ab")) == ["a", "b"], "Перебор"
        """,
        """
        _EMPTY = object()


        class Peekable:
            def __init__(self, iterable):
                self.it = iter(iterable)
                self.buffer = _EMPTY

            def __iter__(self):
                return self

            def __next__(self):
                if self.buffer is not _EMPTY:
                    value, self.buffer = self.buffer, _EMPTY
                    return value
                return next(self.it)

            def peek(self, default=None):
                if self.buffer is _EMPTY:
                    self.buffer = next(self.it, _EMPTY)
                return default if self.buffer is _EMPTY else self.buffer
        """, xp=25),
),

lesson(f"{P}-m1-l2", "yield",
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
    cod(f"{P}-m1-l2-e7", t("""
        Напиши генератор `countdown(n)` — выдаёт `n, n-1, …, 1`, а в конце строку `"старт!"`.
        """),
        """
        def countdown(n):
            pass
        """,
        """
        def test_values():
            assert list(countdown(3)) == [3, 2, 1, "старт!"] and list(countdown(0)) == ["старт!"], "Неверный результат"
        """,
        """
        def countdown(n):
            while n > 0:
                yield n
                n -= 1
            yield "старт!"
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши генератор `running_total(numbers)` — после каждого числа выдаёт накопленную сумму.

        ```
        list(running_total([1, 2, 3]))   # → [1, 3, 6]
        ```
        """),
        """
        def running_total(numbers):
            pass
        """,
        """
        import types

        def test_values():
            g = running_total([1, 2, 3])
            assert isinstance(g, types.GeneratorType) and list(g) == [1, 3, 6] and list(running_total([])) == [], "Неверный результат"
        """,
        """
        def running_total(numbers):
            total = 0
            for n in numbers:
                total += n
                yield total
        """),
),

lesson(f"{P}-lazy", "Ленивость и одноразовость",
    out(f"{P}-lazy-e1", "Что выведет программа? Генератор ничего не делает до запроса.", """
        def gen():
            print("начал")
            yield 1

        g = gen()
        print("создан")
        print(next(g))
        """, hint="Вызов функции-генератора только создаёт объект, код не выполняется."),
    out(f"{P}-lazy-e2", "Что выведет программа? Генератор одноразовый.", """
        def nums():
            yield 1
            yield 2

        g = nums()
        print(sum(g), sum(g))
        print(sum(nums()), sum(nums()))
        """),
    out(f"{P}-lazy-e3", "Что выведет программа? return в генераторе.", """
        def limited():
            yield "a"
            return "итог"
            yield "никогда"

        g = limited()
        print(next(g))
        try:
            next(g)
        except StopIteration as e:
            print("стоп, значение:", e.value)
        print(list(limited()))
        """, hint="return завершает генератор; значение прячется в StopIteration.value."),
    cod(f"{P}-lazy-e4", t("""
        Напиши бесконечный генератор `ids(prefix)` — выдаёт `"prefix-1"`, `"prefix-2"`, … И функцию `take(gen, n)` — первые `n` значений из генератора списком.
        """),
        """
        def ids(prefix):
            pass


        def take(gen, n):
            pass
        """,
        """
        def test_values():
            g = ids("user")
            assert take(g, 3) == ["user-1", "user-2", "user-3"] and take(g, 1) == ["user-4"] and take(ids("x"), 0) == [], "Неверный результат"
        """,
        """
        def ids(prefix):
            n = 1
            while True:
                yield f"{prefix}-{n}"
                n += 1


        def take(gen, n):
            return [next(gen) for _ in range(n)]
        """),
    cod(f"{P}-lazy-e5", t("""
        Напиши функцию `first_match(items, predicate)` — вернуть первый элемент, для которого `predicate` истинна, или `None`. Используй генераторное выражение и `next(..., None)` — так перебор остановится на первом совпадении.
        """),
        """
        def first_match(items, predicate):
            pass
        """,
        """
        def test_values():
            checked = []
            def is_big(x):
                checked.append(x)
                return x > 10
            assert first_match([1, 20, 30, 5], is_big) == 20 and checked == [1, 20], f"Проверено лишнее: {checked}"
            assert first_match([], is_big) is None and first_match([1], is_big) is None, "Нет совпадений"
        """,
        """
        def first_match(items, predicate):
            return next((x for x in items if predicate(x)), None)
        """),
    cod(f"{P}-lazy-e6", t("""
        Напиши генератор `trace(items, log)` — выдаёт элементы по одному и перед каждой выдачей добавляет в список `log` строку `"выдаю X"`. Тест проверит, что элементы выдаются **лениво**: после первого `next` в `log` одна запись.
        """),
        """
        def trace(items, log):
            pass
        """,
        """
        def test_values():
            log = []
            g = trace([1, 2, 3], log)
            assert log == [], "До next ничего не выполняется"
            assert next(g) == 1 and log == ["выдаю 1"], log
            assert list(g) == [2, 3] and log == ["выдаю 1", "выдаю 2", "выдаю 3"], log
        """,
        """
        def trace(items, log):
            for x in items:
                log.append(f"выдаю {x}")
                yield x
        """),
    cod(f"{P}-lazy-e7", t("""
        Напиши генератор `with_summary(items)` — выдаёт элементы, а в конце **возвращает** (`return`) их количество. И функцию `consume(gen)` — перебрать генератор до конца и вернуть кортеж `(список_элементов, значение_return)`.
        """),
        """
        def with_summary(items):
            pass


        def consume(gen):
            pass
        """,
        """
        def test_values():
            assert consume(with_summary(["a", "b"])) == (["a", "b"], 2) and consume(with_summary([])) == ([], 0), "Неверный результат"
        """,
        """
        def with_summary(items):
            count = 0
            for x in items:
                count += 1
                yield x
            return count


        def consume(gen):
            items = []
            while True:
                try:
                    items.append(next(gen))
                except StopIteration as e:
                    return items, e.value
        """),
    cod(f"{P}-lazy-e8", t("""
        Напиши генератор `collatz(n)` — последовательность Коллатца от `n` до 1 включительно: если число чётное — делим на 2, иначе `3n + 1`. И функцию `longest_start(limit)` — какое стартовое число от 1 до `limit` даёт самую длинную последовательность (при равенстве — меньшее). Длину считай, не строя список: `sum(1 for _ in collatz(k))`.
        """),
        """
        def collatz(n):
            pass


        def longest_start(limit):
            pass
        """,
        """
        def test_values():
            assert list(collatz(6)) == [6, 3, 10, 5, 16, 8, 4, 2, 1] and list(collatz(1)) == [1], "collatz"
            assert longest_start(10) == 9 and longest_start(1) == 1, "longest_start"
        """,
        """
        def collatz(n):
            while n != 1:
                yield n
                n = n // 2 if n % 2 == 0 else 3 * n + 1
            yield 1


        def longest_start(limit):
            return max(range(1, limit + 1), key=lambda k: (sum(1 for _ in collatz(k)), -k))
        """, xp=20),
),
)
