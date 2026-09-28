"""Тема «Генераторы», модуль 3 «Продвинутое и практика» — задания. Теория — в _gen_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "gen"

m3 = module(f"{P}-m3", "Продвинутое и практика", "🚀", "send и close, большие данные и пагинация, память и когда нужен список, генераторы в тестах",

lesson(f"{P}-send", "send, close и уборка в генераторе",
    out(f"{P}-send-e1", "Что выведет программа? send передаёт значение внутрь.", """
        def echo():
            received = None
            while True:
                received = yield f"получил {received}"

        g = echo()
        print(next(g))
        print(g.send("привет"))
        print(g.send(42))
        """, hint="yield — это ещё и выражение: send(x) делает его значением x."),
    out(f"{P}-send-e2", "Что выведет программа? Среднее с состоянием.", """
        def averager():
            total = count = 0
            avg = None
            while True:
                value = yield avg
                total += value
                count += 1
                avg = total / count

        a = averager()
        next(a)
        print(a.send(10), a.send(20), a.send(60))
        """, hint="Первым всегда вызывают next() — чтобы дойти до первого yield."),
    out(f"{P}-send-e3", "Что выведет программа? close и finally.", """
        def reader():
            print("открыл")
            try:
                n = 0
                while True:
                    n += 1
                    yield n
            finally:
                print("закрыл")

        r = reader()
        print(next(r), next(r))
        r.close()
        print("после close")
        """, hint="close() завершает генератор, и выполняется его finally."),
    cod(f"{P}-send-e4", t("""
        Напиши генератор-накопитель `collector()`: каждое значение, переданное через `send`, добавляет в список и выдаёт **текущую длину** списка. Первый `next()` выдаёт `0`.
        """),
        """
        def collector():
            pass
        """,
        """
        def test_values():
            c = collector()
            assert next(c) == 0 and c.send("a") == 1 and c.send("b") == 2, "Неверный результат"
        """,
        """
        def collector():
            items = []
            while True:
                value = yield len(items)
                items.append(value)
        """),
    cod(f"{P}-send-e5", t("""
        Напиши генератор `running_max()` — принимает числа через `send` и выдаёт текущий максимум. Первый `next()` выдаёт `None`.
        """),
        """
        def running_max():
            pass
        """,
        """
        def test_values():
            g = running_max()
            assert next(g) is None and [g.send(x) for x in [3, 1, 7, 5]] == [3, 3, 7, 7], "Неверный результат"
        """,
        """
        def running_max():
            best = None
            while True:
                value = yield best
                if best is None or value > best:
                    best = value
        """),
    cod(f"{P}-send-e6", t("""
        Напиши генератор `lines_with_cleanup(lines, log)` — выдаёт строки по одной; при старте добавляет в `log` `"open"`, а при завершении (в том числе если генератор закрыли досрочно через `close()`) — `"close"`. Используй `try/finally`.
        """),
        """
        def lines_with_cleanup(lines, log):
            pass
        """,
        """
        def test_values():
            log = []
            g = lines_with_cleanup(["a", "b", "c"], log)
            assert next(g) == "a" and log == ["open"], log
            g.close()
            assert log == ["open", "close"], log
            log2 = []
            assert list(lines_with_cleanup(["x"], log2)) == ["x"] and log2 == ["open", "close"], log2
        """,
        """
        def lines_with_cleanup(lines, log):
            log.append("open")
            try:
                for line in lines:
                    yield line
            finally:
                log.append("close")
        """),
    cod(f"{P}-send-e7", t("""
        Напиши генератор `state_machine()` — светофор: выдаёт текущий цвет. `next()` переключает на следующий по кругу (`"красный"` → `"зелёный"` → `"жёлтый"` → `"красный"`), а `send("reset")` сразу возвращает `"красный"`. Первый `next()` выдаёт `"красный"`.
        """),
        """
        def state_machine():
            pass
        """,
        """
        def test_values():
            g = state_machine()
            assert [next(g) for _ in range(4)] == ["красный", "зелёный", "жёлтый", "красный"], "Круг"
            next(g)
            assert g.send("reset") == "красный" and next(g) == "зелёный", "reset"
        """,
        """
        COLORS = ["красный", "зелёный", "жёлтый"]


        def state_machine():
            i = 0
            while True:
                command = yield COLORS[i]
                if command == "reset":
                    i = 0
                else:
                    i = (i + 1) % len(COLORS)
        """),
    cod(f"{P}-send-e8", t("""
        Напиши генератор `validator(rules)` — `rules` — словарь «поле → функция-проверка». Через `send` генератор принимает словари-записи и выдаёт список полей, не прошедших проверку (отсутствующее поле — тоже ошибка). Первый `next()` выдаёт `[]`.
        """),
        """
        def validator(rules):
            pass
        """,
        """
        def test_values():
            v = validator({"age": lambda x: x >= 0, "name": lambda x: bool(x)})
            assert next(v) == [], "Первый next"
            assert v.send({"age": 5, "name": "Аня"}) == [] and v.send({"age": -1, "name": ""}) == ["age", "name"] and v.send({"age": 3}) == ["name"], "Неверный результат"
        """,
        """
        def validator(rules):
            errors = []
            while True:
                record = yield errors
                errors = [field for field, check in rules.items() if field not in record or not check(record[field])]
        """, xp=20),
),

lesson(f"{P}-bigdata", "Большие данные и пагинация",
    out(f"{P}-bigdata-e1", "Что выведет программа? Файл построчно через генератор.", """
        with open("big.log", "w", encoding="utf-8") as f:
            for i in range(1000):
                f.write(f"{i} {'ERROR' if i % 250 == 0 else 'INFO'}\\n")

        def errors(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if "ERROR" in line:
                        yield int(line.split()[0])

        print(list(errors("big.log")))
        """),
    out(f"{P}-bigdata-e2", "Что выведет программа? Пагинация API.", """
        DATA = list(range(1, 8))

        def fake_api(page, size=3):
            start = (page - 1) * size
            items = DATA[start:start + size]
            return {"items": items, "has_next": start + size < len(DATA)}

        def all_items():
            page = 1
            while True:
                resp = fake_api(page)
                print("запрос страницы", page)
                yield from resp["items"]
                if not resp["has_next"]:
                    break
                page += 1

        for item in all_items():
            if item > 4:
                break
        print("последний:", item)
        """, hint="Лишние страницы не запрашиваются: генератор остановился вместе с циклом."),
    out(f"{P}-bigdata-e3", "Что выведет программа? Чтение кусками.", """
        import io

        def chunks(f, size):
            while True:
                block = f.read(size)
                if not block:
                    return
                yield block

        stream = io.StringIO("абвгдежз")
        print(list(chunks(stream, 3)))
        """),
    cod(f"{P}-bigdata-e4", t("""
        Напиши генератор `read_records(path)` — читает CSV-файл **без** модуля csv (значения без запятых внутри): первая строка — заголовок; выдаёт словари «колонка → значение» по одному.
        """),
        """
        def read_records(path):
            pass
        """,
        """
        import types

        def test_values():
            with open("r.csv", "w", encoding="utf-8") as f:
                f.write("id,name\\n1,Аня\\n2,Боря\\n")
            g = read_records("r.csv")
            assert isinstance(g, types.GeneratorType) and list(g) == [{"id": "1", "name": "Аня"}, {"id": "2", "name": "Боря"}], "Неверный результат"
        """,
        """
        def read_records(path):
            with open(path, encoding="utf-8") as f:
                header = f.readline().rstrip("\\n").split(",")
                for line in f:
                    values = line.rstrip("\\n").split(",")
                    yield dict(zip(header, values))
        """),
    cod(f"{P}-bigdata-e5", t("""
        Напиши генератор `paginate(fetch)` — `fetch(page)` возвращает список элементов страницы (страницы с 1); пустой список означает конец. Генератор выдаёт все элементы по одному и запрашивает следующую страницу **только когда нужно**.
        """),
        """
        def paginate(fetch):
            pass
        """,
        """
        def test_values():
            pages = {1: ["a", "b"], 2: ["c"], 3: []}
            calls = []
            def fetch(p):
                calls.append(p)
                return pages.get(p, [])
            g = paginate(fetch)
            assert next(g) == "a" and calls == [1], "Ленивая загрузка"
            assert list(g) == ["b", "c"] and calls == [1, 2, 3], calls
        """,
        """
        def paginate(fetch):
            page = 1
            while True:
                items = fetch(page)
                if not items:
                    return
                yield from items
                page += 1
        """),
    cod(f"{P}-bigdata-e6", t("""
        Напиши генератор `read_chunks(path, size)` — читает **двоичный** файл кусками по `size` байт.
        """),
        """
        def read_chunks(path, size):
            pass
        """,
        """
        def test_values():
            with open("b.bin", "wb") as f:
                f.write(bytes(range(10)))
            chunks = list(read_chunks("b.bin", 4))
            assert chunks == [bytes([0, 1, 2, 3]), bytes([4, 5, 6, 7]), bytes([8, 9])], chunks
        """,
        """
        def read_chunks(path, size):
            with open(path, "rb") as f:
                while True:
                    block = f.read(size)
                    if not block:
                        return
                    yield block
        """),
    cod(f"{P}-bigdata-e7", t("""
        Напиши функцию `top_errors(lines, n)` — посчитать, какие сообщения об ошибках (строки вида `"ERROR текст"`) встречаются чаще всего, и вернуть `n` самых частых как список кортежей `(текст, количество)`. Строки приходят генератором — перебрать их можно **только один раз**.
        """),
        """
        from collections import Counter


        def top_errors(lines, n):
            pass
        """,
        """
        def test_values():
            src = ["ERROR timeout", "INFO ok", "ERROR db", "ERROR timeout", "ERROR timeout", "ERROR db", "ERROR auth"]
            assert top_errors((l for l in src), 2) == [("timeout", 3), ("db", 2)], top_errors((l for l in src), 2)
        """,
        """
        from collections import Counter


        def top_errors(lines, n):
            counts = Counter(line[6:] for line in lines if line.startswith("ERROR "))
            return counts.most_common(n)
        """, hint="Counter принимает итерируемое и считает за один проход."),
    cod(f"{P}-bigdata-e8", t("""
        Напиши генератор `merge_sorted(a, b)` — слить два **отсортированных** итерируемых в один отсортированный поток, не загружая их в память целиком (например, два больших отсортированных лога).
        """),
        """
        def merge_sorted(a, b):
            pass
        """,
        """
        def test_values():
            assert list(merge_sorted([1, 4, 9], iter([2, 3, 10, 11]))) == [1, 2, 3, 4, 9, 10, 11], "Неверный результат"
            assert list(merge_sorted([], [1])) == [1] and list(merge_sorted([], [])) == [], "Пустые"
        """,
        """
        _END = object()


        def merge_sorted(a, b):
            ia, ib = iter(a), iter(b)
            x, y = next(ia, _END), next(ib, _END)
            while x is not _END and y is not _END:
                if x <= y:
                    yield x
                    x = next(ia, _END)
                else:
                    yield y
                    y = next(ib, _END)
            while x is not _END:
                yield x
                x = next(ia, _END)
            while y is not _END:
                yield y
                y = next(ib, _END)
        """, hint="Готовая функция — heapq.merge.", xp=25),
),

lesson(f"{P}-memory", "Память: генератор или список",
    out(f"{P}-memory-e1", "Что выведет программа? Размер в памяти.", """
        import sys

        big_list = [x for x in range(100_000)]
        big_gen = (x for x in range(100_000))
        print(sys.getsizeof(big_list) > 100_000, sys.getsizeof(big_gen) < 500)
        print(sum(big_list) == sum(big_gen))
        """, hint="Генератор хранит только своё состояние, а не все значения."),
    out(f"{P}-memory-e2", "Что выведет программа? Чего не умеет генератор.", """
        g = (x * 2 for x in range(5))
        for op in [lambda: len(g), lambda: g[0]]:
            try:
                op()
            except TypeError as e:
                print(type(e).__name__)
        items = list(g)
        print(len(items), items[0], items[-1])
        """),
    out(f"{P}-memory-e3", "Что выведет программа? Два прохода.", """
        from itertools import tee

        def nums():
            yield from [3, 1, 2]

        g = nums()
        print(max(g), min(g, default="пусто"))

        a, b = tee(nums())
        print(max(a), min(b))

        data = list(nums())
        print(max(data), min(data))
        """, hint="Для нескольких проходов нужен список (или tee)."),
    cod(f"{P}-memory-e4", t("""
        Напиши функцию `stats(numbers)` — вернуть кортеж `(минимум, максимум, среднее)` для **итерируемого**, которое можно перебрать только один раз (например, генератора). Вычисли всё за **один проход**, без `list`. Для пустого входа — `(None, None, None)`.
        """),
        """
        def stats(numbers):
            pass
        """,
        """
        def test_values():
            assert stats(x for x in [4, 1, 7]) == (1, 7, 4.0) and stats(iter([])) == (None, None, None), "Неверный результат"
            assert "list(" not in open("solution.py", encoding="utf-8").read(), "Без list"
        """,
        """
        def stats(numbers):
            lo = hi = None
            total = count = 0
            for n in numbers:
                lo = n if lo is None or n < lo else lo
                hi = n if hi is None or n > hi else hi
                total += n
                count += 1
            if count == 0:
                return None, None, None
            return lo, hi, total / count
        """),
    cod(f"{P}-memory-e5", t("""
        Функция `normalize` из заготовки падает, если ей передать генератор: она перебирает данные дважды. Исправь её, чтобы она работала с **любым** итерируемым: вернуть список чисел, делённых на максимум.
        """),
        """
        def normalize(values):
            top = max(values)
            return [v / top for v in values]
        """,
        """
        def test_values():
            assert normalize([2, 4]) == [0.5, 1.0], "Список"
            assert normalize(x for x in [1, 2, 4]) == [0.25, 0.5, 1.0], "Генератор"
        """,
        """
        def normalize(values):
            values = list(values)
            top = max(values)
            return [v / top for v in values]
        """),
    cod(f"{P}-memory-e6", t("""
        Напиши функцию `count_items(iterable)` — количество элементов в любом итерируемом (включая генератор) **без** создания списка и без `len`.
        """),
        """
        def count_items(iterable):
            pass
        """,
        """
        def test_values():
            assert count_items(x for x in range(1000)) == 1000 and count_items([]) == 0 and count_items("abc") == 3, "Неверный результат"
            src = open("solution.py", encoding="utf-8").read()
            assert "list(" not in src and "len(" not in src, "Без list и len"
        """,
        """
        def count_items(iterable):
            return sum(1 for _ in iterable)
        """),
    cod(f"{P}-memory-e7", t("""
        Напиши функцию `split_stream(iterable, predicate)` — разделить поток на два **итератора**: подходящие и неподходящие элементы. Используй `itertools.tee` и генераторные выражения. Вернуть кортеж `(yes, no)`.
        """),
        """
        from itertools import tee


        def split_stream(iterable, predicate):
            pass
        """,
        """
        def test_values():
            yes, no = split_stream((x for x in range(6)), lambda x: x % 2 == 0)
            assert list(yes) == [0, 2, 4] and list(no) == [1, 3, 5], "Неверный результат"
        """,
        """
        from itertools import tee


        def split_stream(iterable, predicate):
            a, b = tee(iterable)
            return (x for x in a if predicate(x)), (x for x in b if not predicate(x))
        """),
    cod(f"{P}-memory-e8", t("""
        Напиши функцию `choose(data_size, passes)` — «советчик»: вернуть `"генератор"`, если нужен один проход (`passes == 1`) и данных много (`data_size > 10_000`); `"список"` — если проходов больше одного; иначе `"любой"`. А также функцию `sum_squares(n)` — сумма квадратов от 1 до `n`, посчитанная через генераторное выражение (без списка).
        """),
        """
        def choose(data_size, passes):
            pass


        def sum_squares(n):
            pass
        """,
        """
        def test_values():
            assert choose(1_000_000, 1) == "генератор" and choose(10, 3) == "список" and choose(100, 1) == "любой" and choose(10**6, 2) == "список", "choose"
            assert sum_squares(3) == 14 and sum_squares(0) == 0, "sum_squares"
        """,
        """
        def choose(data_size, passes):
            if passes > 1:
                return "список"
            if data_size > 10_000:
                return "генератор"
            return "любой"


        def sum_squares(n):
            return sum(i * i for i in range(1, n + 1))
        """),
),

lesson(f"{P}-testing", "Генераторы в тестах",
    out(f"{P}-testing-e1", "Что выведет программа? Уникальные тестовые данные.", """
        from itertools import count

        _ids = count(1)

        def make_user():
            n = next(_ids)
            return {"id": n, "email": f"user{n}@test.ru"}

        print(make_user())
        print(make_user()["email"])
        """),
    out(f"{P}-testing-e2", "Что выведет программа? Набор проверок из генератора.", """
        def cases():
            yield "", False
            yield "a@b.ru", True
            yield "без собаки", False
            yield "@x.ru", False

        def is_email(s):
            return "@" in s and not s.startswith("@")

        for value, expected in cases():
            status = "ok" if is_email(value) == expected else "FAIL"
            print(repr(value), status)
        """, hint="Похоже на данные для @pytest.mark.parametrize."),
    out(f"{P}-testing-e3", "Что выведет программа? Фикстура-генератор.", """
        def db_fixture(log):
            log.append("подключение")
            yield {"users": []}
            log.append("отключение")

        log = []
        gen = db_fixture(log)
        db = next(gen)
        db["users"].append("аня")
        log.append(f"тест: {db['users']}")
        next(gen, None)
        print(log)
        """, hint="Так pytest выполняет фикстуры с yield: next до теста, next после."),
    cod(f"{P}-testing-e4", t("""
        Напиши генератор `user_factory(prefix="user")` — бесконечно выдаёт словари `{"id": N, "login": "prefix_N"}` с N от 1.
        """),
        """
        def user_factory(prefix="user"):
            pass
        """,
        """
        def test_values():
            f = user_factory()
            assert next(f) == {"id": 1, "login": "user_1"} and next(f)["login"] == "user_2", "Неверный результат"
            assert next(user_factory("qa")) == {"id": 1, "login": "qa_1"}, "Свой счётчик у каждой фабрики"
        """,
        """
        def user_factory(prefix="user"):
            n = 1
            while True:
                yield {"id": n, "login": f"{prefix}_{n}"}
                n += 1
        """),
    cod(f"{P}-testing-e5", t("""
        Напиши генератор `boundary_values(low, high)` — граничные значения для тест-дизайна: `low - 1`, `low`, `low + 1`, `high - 1`, `high`, `high + 1` — без повторов, в этом порядке (повторы бывают, когда диапазон узкий).
        """),
        """
        def boundary_values(low, high):
            pass
        """,
        """
        def test_values():
            assert list(boundary_values(1, 100)) == [0, 1, 2, 99, 100, 101] and list(boundary_values(5, 6)) == [4, 5, 6, 7], "Неверный результат"
        """,
        """
        def boundary_values(low, high):
            seen = set()
            for v in (low - 1, low, low + 1, high - 1, high, high + 1):
                if v not in seen:
                    seen.add(v)
                    yield v
        """),
    cod(f"{P}-testing-e6", t("""
        Напиши генератор `combinations_matrix(params)` — `params` — словарь «параметр → список значений». Выдаёт словари со всеми комбинациями (декартово произведение) через `itertools.product`. Порядок параметров — как в словаре.
        """),
        """
        from itertools import product


        def combinations_matrix(params):
            pass
        """,
        """
        def test_values():
            r = list(combinations_matrix({"browser": ["chrome", "firefox"], "lang": ["ru", "en"]}))
            assert r == [
                {"browser": "chrome", "lang": "ru"}, {"browser": "chrome", "lang": "en"},
                {"browser": "firefox", "lang": "ru"}, {"browser": "firefox", "lang": "en"},
            ], r
            assert list(combinations_matrix({"x": []})) == [], "Пустой параметр"
        """,
        """
        from itertools import product


        def combinations_matrix(params):
            keys = list(params)
            for values in product(*params.values()):
                yield dict(zip(keys, values))
        """),
    cod(f"{P}-testing-e7", t("""
        Напиши функцию `run_fixture(fixture_func, test_func)` — выполнить фикстуру-генератор как pytest: вызвать `next` у генератора, передать полученное значение в `test_func`, затем **в любом случае** (даже если тест упал) довести генератор до конца, чтобы выполнилась уборка. Вернуть результат `test_func`; исключение теста пробросить.
        """),
        """
        def run_fixture(fixture_func, test_func):
            pass
        """,
        """
        def test_values():
            log = []
            def fix():
                log.append("setup")
                yield 42
                log.append("teardown")
            assert run_fixture(fix, lambda v: v + 1) == 43 and log == ["setup", "teardown"], log
            log.clear()
            def bad(v):
                raise AssertionError("упал")
            try:
                run_fixture(fix, bad)
            except AssertionError:
                pass
            else:
                assert False, "Ошибка теста должна пробрасываться"
            assert log == ["setup", "teardown"], log
        """,
        """
        def run_fixture(fixture_func, test_func):
            gen = fixture_func()
            value = next(gen)
            try:
                return test_func(value)
            finally:
                next(gen, None)
        """),
    cod(f"{P}-testing-e8", t("""
        Напиши генератор `retry_delays(base=1, factor=2, max_delay=30)` — бесконечная последовательность пауз для повторов: `base`, `base*factor`, `base*factor²`, …, но не больше `max_delay` (после достижения — всегда `max_delay`). И функцию `plan(attempts)` — список первых `attempts` пауз со значениями по умолчанию.
        """),
        """
        def retry_delays(base=1, factor=2, max_delay=30):
            pass


        def plan(attempts):
            pass
        """,
        """
        def test_values():
            assert plan(7) == [1, 2, 4, 8, 16, 30, 30] and plan(0) == [], plan(7)
            g = retry_delays(base=5, factor=3, max_delay=50)
            assert [next(g) for _ in range(4)] == [5, 15, 45, 50], "Свои параметры"
        """,
        """
        from itertools import islice


        def retry_delays(base=1, factor=2, max_delay=30):
            delay = base
            while True:
                yield min(delay, max_delay)
                delay *= factor


        def plan(attempts):
            return list(islice(retry_delays(), attempts))
        """, xp=20),
),
)
