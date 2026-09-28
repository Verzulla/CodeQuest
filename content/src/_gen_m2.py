"""Тема «Генераторы», модуль 2 «Выражения и конвейеры» — задания. Теория — в _gen_t2.py.

Слаги gen-m2-l1, gen-m2-l2 унаследованы от старой темы — так сохраняется прогресс."""
from ._lib import cod, lesson, module, out, t

P = "gen"

m2 = module(f"{P}-m2", "Выражения и конвейеры", "🛤️", "Генераторные выражения, конвейеры обработки, yield from, модуль itertools",

lesson(f"{P}-m2-l1", "Генераторные выражения",
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
    out(f"{P}-m2-l1-e7", "Что выведет программа? Скобки у аргумента.", """
        words = ["кот", "собака", "ёж"]
        print(max(len(w) for w in words))
        print(", ".join(w.upper() for w in words))
        print(sorted((len(w), w) for w in words))
        print(dict((w, len(w)) for w in words))
        """, hint="Если генераторное выражение — единственный аргумент, вторые скобки не нужны."),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `count_long(words, n)` — сколько слов длиннее `n` символов. Используй генераторное выражение внутри `sum(...)`, без создания списка.
        """),
        """
        def count_long(words, n):
            pass
        """,
        """
        def test_values():
            assert count_long(["a", "abcd", "abc", "abcdef"], 3) == 2 and count_long([], 1) == 0, "Неверный результат"
            assert "[" not in open("solution.py", encoding="utf-8").read(), "Без списков"
        """,
        """
        def count_long(words, n):
            return sum(1 for w in words if len(w) > n)
        """),
),

lesson(f"{P}-pipeline", "Конвейеры из генераторов",
    out(f"{P}-pipeline-e1", "Что выведет программа? Цепочка генераторов.", """
        lines = ["  10 ", "", "abc", "25", "  ", "7"]

        stripped = (s.strip() for s in lines)
        non_empty = (s for s in stripped if s)
        numbers = (int(s) for s in non_empty if s.isdigit())
        print(sum(numbers))
        """, hint="Каждый этап берёт данные из предыдущего по одному элементу."),
    out(f"{P}-pipeline-e2", "Что выведет программа? Порядок вычислений.", """
        def source():
            for x in [1, 2, 3]:
                print("взял", x)
                yield x

        def double(items):
            for x in items:
                print("удвоил", x)
                yield x * 2

        for result in double(source()):
            print("получил", result)
        """, hint="Элементы проходят весь конвейер по одному, а не этапами целиком."),
    out(f"{P}-pipeline-e3", "Что выведет программа? Остановка конвейера.", """
        def numbers():
            n = 0
            while True:
                n += 1
                yield n

        squares = (n * n for n in numbers())
        big = (s for s in squares if s > 50)
        print(next(big), next(big))
        """, hint="Бесконечный источник не страшен: конвейер считает только то, что попросили."),
    cod(f"{P}-pipeline-e4", t("""
        Напиши три генератора и собери из них конвейер:

        - `read(lines)` — выдаёт строки без пробелов по краям;
        - `skip_comments(lines)` — пропускает пустые строки и строки, начинающиеся с `#`;
        - `parse(lines)` — строку `"ключ=значение"` превращает в кортеж `(ключ, значение)`.

        Функция `load_config(lines)` возвращает `dict(parse(skip_comments(read(lines))))`.
        """),
        """
        def read(lines):
            pass


        def skip_comments(lines):
            pass


        def parse(lines):
            pass


        def load_config(lines):
            pass
        """,
        """
        import types

        def test_values():
            lines = ["# конфиг", " url=http://a ", "", "timeout=5", "  # ещё"]
            assert load_config(lines) == {"url": "http://a", "timeout": "5"}, load_config(lines)
            assert all(isinstance(f([]), types.GeneratorType) for f in (read, skip_comments, parse)), "Этапы — генераторы"
        """,
        """
        def read(lines):
            for line in lines:
                yield line.strip()


        def skip_comments(lines):
            for line in lines:
                if line and not line.startswith("#"):
                    yield line


        def parse(lines):
            for line in lines:
                key, value = line.split("=", 1)
                yield key, value


        def load_config(lines):
            return dict(parse(skip_comments(read(lines))))
        """),
    cod(f"{P}-pipeline-e5", t("""
        Напиши генератор `apply(funcs, items)` — пропускает каждый элемент через **все** функции из списка по очереди и выдаёт результат.

        ```
        list(apply([str.strip, str.upper], [" a", "b "]))   # → ["A", "B"]
        ```
        """),
        """
        def apply(funcs, items):
            pass
        """,
        """
        def test_values():
            assert list(apply([str.strip, str.upper], [" a", "b "])) == ["A", "B"] and list(apply([], [1, 2])) == [1, 2], "Неверный результат"
        """,
        """
        def apply(funcs, items):
            for item in items:
                for f in funcs:
                    item = f(item)
                yield item
        """),
    cod(f"{P}-pipeline-e6", t("""
        Напиши генератор `failed_tests(results)` — `results` — итерируемое словарей `{"name", "status", "duration"}`. Выдаёт **имена** упавших тестов (`status == "failed"`), которые длились дольше 1 секунды. Обработка должна быть ленивой (генератор).
        """),
        """
        def failed_tests(results):
            pass
        """,
        """
        import types

        def test_values():
            rs = [
                {"name": "a", "status": "failed", "duration": 2.5},
                {"name": "b", "status": "passed", "duration": 3},
                {"name": "c", "status": "failed", "duration": 0.5},
                {"name": "d", "status": "failed", "duration": 1.1},
            ]
            g = failed_tests(iter(rs))
            assert isinstance(g, types.GeneratorType) and list(g) == ["a", "d"], "Неверный результат"
        """,
        """
        def failed_tests(results):
            for r in results:
                if r["status"] == "failed" and r["duration"] > 1:
                    yield r["name"]
        """),
    cod(f"{P}-pipeline-e7", t("""
        Напиши генератор `dedupe(items)` — выдаёт элементы, пропуская уже встречавшиеся, и работает лениво (подходит для бесконечного потока).
        """),
        """
        def dedupe(items):
            pass
        """,
        """
        import itertools

        def test_values():
            assert list(dedupe([3, 1, 3, 2, 1])) == [3, 1, 2], "Порядок и повторы"
            infinite = itertools.cycle([1, 2, 3])
            g = dedupe(infinite)
            assert [next(g) for _ in range(3)] == [1, 2, 3], "Ленивость"
        """,
        """
        def dedupe(items):
            seen = set()
            for x in items:
                if x not in seen:
                    seen.add(x)
                    yield x
        """),
    cod(f"{P}-pipeline-e8", t("""
        Напиши генератор `window_avg(numbers, size)` — скользящее среднее: для каждого окна из `size` подряд идущих чисел выдаёт их среднее (округлить до 2 знаков). Окна начинаются, когда набралось `size` чисел.

        ```
        list(window_avg([1, 2, 3, 4], 2))   # → [1.5, 2.5, 3.5]
        ```
        """),
        """
        from collections import deque


        def window_avg(numbers, size):
            pass
        """,
        """
        def test_values():
            assert list(window_avg([1, 2, 3, 4], 2)) == [1.5, 2.5, 3.5] and list(window_avg([10, 20, 30], 3)) == [20.0] and list(window_avg([1], 2)) == [], "Неверный результат"
            assert list(window_avg(iter([2, 4, 6]), 2)) == [3.0, 5.0], "Итератор на входе"
        """,
        """
        from collections import deque


        def window_avg(numbers, size):
            window = deque(maxlen=size)
            for n in numbers:
                window.append(n)
                if len(window) == size:
                    yield round(sum(window) / size, 2)
        """, xp=20),
),

lesson(f"{P}-m2-l2", "yield from и itertools",
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
    out(f"{P}-m2-l2-e7", "Что выведет программа? Рекурсия с yield from.", """
        def walk(tree, depth=0):
            yield "  " * depth + tree["name"]
            for child in tree.get("children", []):
                yield from walk(child, depth + 1)

        site = {"name": "главная", "children": [
            {"name": "каталог", "children": [{"name": "товар"}]},
            {"name": "корзина"},
        ]}
        for line in walk(site):
            print(line)
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши генератор `deep_flatten(data)` — разворачивает списки и кортежи **любой** вложенности, используя `yield from` для рекурсии. Строки не разворачивать.
        """),
        """
        def deep_flatten(data):
            pass
        """,
        """
        def test_values():
            assert list(deep_flatten([1, [2, (3, ["ab", [4]])], []])) == [1, 2, 3, "ab", 4] and list(deep_flatten([])) == [], "Неверный результат"
            assert "yield from" in open("solution.py", encoding="utf-8").read(), "Используй yield from"
        """,
        """
        def deep_flatten(data):
            for item in data:
                if isinstance(item, (list, tuple)):
                    yield from deep_flatten(item)
                else:
                    yield item
        """, xp=20),
),

lesson(f"{P}-itertools", "Ещё itertools",
    out(f"{P}-itertools-e1", "Что выведет программа? chain, accumulate, pairwise.", """
        from itertools import chain, accumulate, pairwise

        print(list(chain([1, 2], (3,), "ab")))
        print(list(accumulate([1, 2, 3, 4])))
        print(list(pairwise([10, 13, 19])))
        """),
    out(f"{P}-itertools-e2", "Что выведет программа? takewhile, dropwhile, batched.", """
        from itertools import takewhile, dropwhile, batched

        nums = [1, 3, 5, 8, 9, 11]
        print(list(takewhile(lambda n: n % 2, nums)))
        print(list(dropwhile(lambda n: n % 2, nums)))
        print(list(batched("abcdefg", 3)))
        """, hint="batched появился в Python 3.12."),
    out(f"{P}-itertools-e3", "Что выведет программа? groupby и combinations.", """
        from itertools import groupby, combinations

        log = ["ERROR", "ERROR", "INFO", "ERROR", "INFO", "INFO"]
        print([(k, len(list(g))) for k, g in groupby(log)])
        print(list(combinations(["api", "ui", "db"], 2)))
        """, hint="groupby группирует только соседние одинаковые элементы."),
    cod(f"{P}-itertools-e4", t("""
        Напиши функцию `merge_logs(*logs)` — объединить несколько списков строк в один список через `itertools.chain`.
        """),
        """
        from itertools import chain


        def merge_logs(*logs):
            pass
        """,
        """
        def test_values():
            assert merge_logs(["a"], [], ["b", "c"]) == ["a", "b", "c"] and merge_logs() == [], "Неверный результат"
        """,
        """
        from itertools import chain


        def merge_logs(*logs):
            return list(chain(*logs))
        """, hint="chain.from_iterable(logs) — то же самое."),
    cod(f"{P}-itertools-e5", t("""
        Напиши функцию `deltas(values)` — список разниц между соседними значениями (например, времени отклика) через `itertools.pairwise`.

        ```
        deltas([100, 120, 90])   # → [20, -30]
        ```
        """),
        """
        from itertools import pairwise


        def deltas(values):
            pass
        """,
        """
        def test_values():
            assert deltas([100, 120, 90]) == [20, -30] and deltas([5]) == [] and deltas([]) == [], "Неверный результат"
        """,
        """
        from itertools import pairwise


        def deltas(values):
            return [b - a for a, b in pairwise(values)]
        """),
    cod(f"{P}-itertools-e6", t("""
        Напиши функцию `streaks(results)` — `results` — список `"pass"`/`"fail"`. Вернуть самую длинную серию подряд идущих `"fail"` (число). Используй `itertools.groupby`.
        """),
        """
        from itertools import groupby


        def streaks(results):
            pass
        """,
        """
        def test_values():
            assert streaks(["pass", "fail", "fail", "pass", "fail", "fail", "fail"]) == 3 and streaks(["pass"]) == 0 and streaks([]) == 0, "Неверный результат"
        """,
        """
        from itertools import groupby


        def streaks(results):
            return max((len(list(g)) for k, g in groupby(results) if k == "fail"), default=0)
        """),
    cod(f"{P}-itertools-e7", t("""
        Напиши функцию `send_in_batches(ids, size)` — разбить список id на пачки по `size` через `itertools.batched` и вернуть список **списков**.
        """),
        """
        from itertools import batched


        def send_in_batches(ids, size):
            pass
        """,
        """
        def test_values():
            assert send_in_batches([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]] and send_in_batches([], 3) == [], "Неверный результат"
        """,
        """
        from itertools import batched


        def send_in_batches(ids, size):
            return [list(b) for b in batched(ids, size)]
        """),
    cod(f"{P}-itertools-e8", t("""
        Напиши функцию `cumulative_balance(operations)` — `operations` — список сумм (+ пополнение, − списание). Вернуть кортеж `(список_балансов_после_каждой_операции, минимальный_баланс)`. Используй `itertools.accumulate`. Для пустого списка — `([], 0)`.
        """),
        """
        from itertools import accumulate


        def cumulative_balance(operations):
            pass
        """,
        """
        def test_values():
            assert cumulative_balance([100, -30, -90, 50]) == ([100, 70, -20, 30], -20) and cumulative_balance([]) == ([], 0), "Неверный результат"
        """,
        """
        from itertools import accumulate


        def cumulative_balance(operations):
            balances = list(accumulate(operations))
            return balances, min(balances, default=0)
        """, xp=20),
),
)
