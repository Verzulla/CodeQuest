"""Тема «*args и **kwargs», модуль 1 «*args» — задания. Теория — в _arg_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "arg"

m1 = module(f"{P}-m1", "*args", "✳️", "Любое число позиционных аргументов и звёздочка при вызове",

lesson(f"{P}-m1-l1", "*args: любое число аргументов",
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        def show(*args):
            print(args, type(args).__name__, len(args))

        show(1, 2, 3)
        show("a")
        show()
        """, hint="Все позиционные аргументы собираются в кортеж."),
    out(f"{P}-m1-l1-e2", "Что выведет программа?", """
        def total(*nums):
            s = 0
            for n in nums:
                s += n
            return s

        print(total(1, 2, 3), total(), total(10))
        """),
    out(f"{P}-m1-l1-e3", "Что выведет программа?", """
        def first_or_none(*items):
            return items[0] if items else None

        print(first_or_none(5, 6), first_or_none())
        """, hint="Пустой кортеж ложен."),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `my_sum(*nums)` — сумма любого количества чисел. Без аргументов — `0`.

        ```
        my_sum(1, 2, 3)   # → 6
        my_sum()          # → 0
        ```
        """),
        """
        def my_sum(*nums):
            pass
        """,
        """
        def test_values():
            assert [my_sum(1, 2, 3), my_sum(), my_sum(5), my_sum(1.5, 1.5)] == [6, 0, 5, 3.0], "Неверная сумма"
        """,
        """
        def my_sum(*nums):
            total = 0
            for n in nums:
                total += n
            return total
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `count_args(*args)` — сколько аргументов ей передали.

        ```
        count_args(1, "a", None)   # → 3
        count_args()               # → 0
        ```
        """),
        """
        def count_args(*args):
            pass
        """,
        """
        def test_values():
            assert [count_args(1, "a", None), count_args(), count_args([1, 2])] == [3, 0, 1], "Неверное количество"
        """,
        """
        def count_args(*args):
            return len(args)
        """, hint="Список [1, 2] — это ОДИН аргумент."),
    cod(f"{P}-m1-l1-e6", t("""
        Напиши функцию `average(*nums)` — среднее арифметическое. Без аргументов — `None`.

        ```
        average(2, 4, 9)   # → 5.0
        average()          # → None
        ```
        """),
        """
        def average(*nums):
            pass
        """,
        """
        def test_values():
            assert [average(2, 4, 9), average(), average(7)] == [5.0, None, 7.0], "Неверное среднее"
        """,
        """
        def average(*nums):
            if not nums:
                return None
            return sum(nums) / len(nums)
        """),
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `longest(*words)` — самое длинное из переданных слов (при равенстве — первое). Без аргументов — `""`.

        ```
        longest("api", "docker", "pytest")   # → "docker"
        longest()                            # → ""
        ```
        """),
        """
        def longest(*words):
            pass
        """,
        """
        def test_values():
            assert [longest("api", "docker", "pytest"), longest(), longest("a")] == ["docker", "", "a"], "Неверный результат"
        """,
        """
        def longest(*words):
            best = ""
            for w in words:
                if len(w) > len(best):
                    best = w
            return best
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `join_words(*words)` — склеить слова через пробел, **пропуская пустые** строки.

        ```
        join_words("Привет", "", "мир")   # → "Привет мир"
        join_words()                      # → ""
        ```
        """),
        """
        def join_words(*words):
            pass
        """,
        """
        def test_values():
            assert [join_words("Привет", "", "мир"), join_words(), join_words("a")] == ["Привет мир", "", "a"], "Неверная строка"
        """,
        """
        def join_words(*words):
            return " ".join(w for w in words if w)
        """),
),

lesson(f"{P}-m1-l2", "*args вместе с обычными параметрами",
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        def greet(greeting, *names):
            for name in names:
                print(greeting, name)

        greet("Привет", "Аня", "Боря")
        greet("Пока")
        print("конец")
        """, hint="Первый аргумент уходит в greeting, остальные — в names."),
    out(f"{P}-m1-l2-e2", "Что выведет программа? Параметр после *args.", """
        def join(*parts, sep="-"):
            return sep.join(parts)

        print(join("a", "b", "c"))
        print(join("a", "b", sep="+"))
        print(join("a", "+"))
        """, hint="После *args параметр можно передать только по имени."),
    out(f"{P}-m1-l2-e3", "Что выведет программа?", """
        def f(a, b=10, *rest):
            print(a, b, rest)

        f(1)
        f(1, 2)
        f(1, 2, 3, 4)
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `tag(name, *classes)` — CSS-селектор: имя тега и классы через точку.

        ```
        tag("div", "card", "active")   # → "div.card.active"
        tag("p")                       # → "p"
        ```
        """),
        """
        def tag(name, *classes):
            pass
        """,
        """
        def test_values():
            assert [tag("div", "card", "active"), tag("p")] == ["div.card.active", "p"], "Неверный селектор"
        """,
        """
        def tag(name, *classes):
            return name + "".join("." + c for c in classes)
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `log(level, *messages)` — строка `"[LEVEL] сообщения через пробел"`.

        ```
        log("INFO", "сервер", "запущен")   # → "[INFO] сервер запущен"
        log("WARN")                        # → "[WARN] "
        ```
        """),
        """
        def log(level, *messages):
            pass
        """,
        """
        def test_values():
            assert [log("INFO", "сервер", "запущен"), log("WARN")] == ["[INFO] сервер запущен", "[WARN] "], "Неверная строка"
        """,
        """
        def log(level, *messages):
            return f"[{level}] " + " ".join(messages)
        """),
    cod(f"{P}-m1-l2-e6", t("""
        Напиши функцию `join_with(*parts, sep=", ")` — склеить любые значения (превращая их в строки) через разделитель `sep`, который передаётся **только по имени**.

        ```
        join_with(1, "a", 2.5)          # → "1, a, 2.5"
        join_with("x", "y", sep="|")    # → "x|y"
        ```
        """),
        """
        def join_with(*parts, sep=", "):
            pass
        """,
        """
        def test_values():
            assert [join_with(1, "a", 2.5), join_with("x", "y", sep="|"), join_with()] == ["1, a, 2.5", "x|y", ""], "Неверная строка"
        """,
        """
        def join_with(*parts, sep=", "):
            return sep.join(str(p) for p in parts)
        """),
    cod(f"{P}-m1-l2-e7", t("""
        Напиши функцию `scale(factor, *nums)` — список чисел, умноженных на `factor`.

        ```
        scale(10, 1, 2, 3)   # → [10, 20, 30]
        scale(2)             # → []
        ```
        """),
        """
        def scale(factor, *nums):
            pass
        """,
        """
        def test_values():
            assert [scale(10, 1, 2, 3), scale(2)] == [[10, 20, 30], []], "Неверный результат"
        """,
        """
        def scale(factor, *nums):
            return [n * factor for n in nums]
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши функцию `between(low, high, *values)` — список значений из `values`, попадающих в отрезок `[low, high]`.

        ```
        between(1, 5, 0, 3, 5, 9)   # → [3, 5]
        ```
        """),
        """
        def between(low, high, *values):
            pass
        """,
        """
        def test_values():
            assert [between(1, 5, 0, 3, 5, 9), between(0, 1)] == [[3, 5], []], "Неверный результат"
        """,
        """
        def between(low, high, *values):
            return [v for v in values if low <= v <= high]
        """),
),

lesson(f"{P}-m1-l3", "Звёздочка при вызове: f(*коллекция)",
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        def add3(a, b, c):
            return a + b + c

        nums = [1, 2, 3]
        print(add3(*nums))
        print(add3(10, *[20, 30]))
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа? print и звёздочка.", """
        print(*[1, 2, 3])
        print(*"abc", sep="-")
        print(*range(3), sep=", ")
        """),
    out(f"{P}-m1-l3-e3", "Что выведет программа? Со звёздочкой и без.", """
        def show(*args):
            return len(args)

        data = [1, 2, 3]
        print(show(data), show(*data), show(*data, *data))
        """, hint="Без звёздочки список — один аргумент."),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `call_with_list(func, items)` — вызвать `func`, передав элементы списка `items` отдельными аргументами.

        ```
        call_with_list(max, [3, 9, 2])   # → 9
        call_with_list(pow, [2, 5])      # → 32
        ```
        """),
        """
        def call_with_list(func, items):
            pass
        """,
        """
        def test_values():
            assert [call_with_list(max, [3, 9, 2]), call_with_list(pow, [2, 5])] == [9, 32], "Неверный вызов"
        """,
        """
        def call_with_list(func, items):
            return func(*items)
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Есть список `row = ["id", "name", "status"]`. Выведи его элементы **одной строкой** через `" | "` с помощью `print(*row, sep=...)`.

        Ожидаемый вывод:
        ```
        id | name | status
        ```
        """),
        """
        row = ["id", "name", "status"]
        """,
        """
        def test_output():
            assert OUTPUT.strip() == "id | name | status", f"Напечатано {OUTPUT!r}"

        def test_star():
            assert "*row" in open("solution.py", encoding="utf-8").read(), "Используй print(*row, sep=...)"
        """,
        """
        row = ["id", "name", "status"]
        print(*row, sep=" | ")
        """),
    cod(f"{P}-m1-l3-e6", t("""
        Напиши функцию `max_of_lists(a, b)` — наибольшее число из двух непустых списков вместе. Используй `max(*a, *b)`.

        ```
        max_of_lists([1, 5], [3, 9, 2])   # → 9
        ```
        """),
        """
        def max_of_lists(a, b):
            pass
        """,
        """
        def test_values():
            assert [max_of_lists([1, 5], [3, 9, 2]), max_of_lists([-1], [-5])] == [9, -1], "Неверный максимум"
        """,
        """
        def max_of_lists(a, b):
            return max(*a, *b)
        """),
    cod(f"{P}-m1-l3-e7", t("""
        Напиши функцию `merge_all(*lists)` — склеить любое количество списков в один новый список.

        ```
        merge_all([1], [2, 3], [])   # → [1, 2, 3]
        merge_all()                  # → []
        ```
        """),
        """
        def merge_all(*lists):
            pass
        """,
        """
        def test_values():
            assert [merge_all([1], [2, 3], []), merge_all()] == [[1, 2, 3], []], "Неверный результат"
        """,
        """
        def merge_all(*lists):
            result = []
            for lst in lists:
                result.extend(lst)
            return result
        """),
    cod(f"{P}-m1-l3-e8", t("""
        Напиши функцию `apply_pairs(func, pairs)` — применить функцию двух аргументов к каждой паре из списка и вернуть список результатов.

        ```
        apply_pairs(pow, [(2, 3), (3, 2)])   # → [8, 9]
        ```
        """),
        """
        def apply_pairs(func, pairs):
            pass
        """,
        """
        def test_values():
            assert [apply_pairs(pow, [(2, 3), (3, 2)]), apply_pairs(max, [])] == [[8, 9], []], "Неверный результат"
        """,
        """
        def apply_pairs(func, pairs):
            return [func(*p) for p in pairs]
        """),
),

lesson(f"{P}-m1-l4", "Приёмы с *args",
    out(f"{P}-m1-l4-e1", "Что выведет программа? Хотя бы один аргумент.", """
        def my_max(first, *rest):
            best = first
            for x in rest:
                if x > best:
                    best = x
            return best

        print(my_max(3, 9, 2), my_max(5))
        try:
            my_max()
        except TypeError:
            print("нужен хотя бы один аргумент")
        """),
    out(f"{P}-m1-l4-e2", "Что выведет программа?", """
        def check_types(*values):
            return all(isinstance(v, (int, float)) for v in values)

        print(check_types(1, 2.5), check_types(1, "2"), check_types())
        """, hint="all() для пустого набора — True."),
    out(f"{P}-m1-l4-e3", "Что выведет программа?", """
        def describe(*args):
            if not args:
                return "пусто"
            if len(args) == 1:
                return f"один: {args[0]}"
            return f"{len(args)} шт., первый {args[0]}"

        print(describe(), describe(7), describe(1, 2, 3))
        """),
    cod(f"{P}-m1-l4-e4", t("""
        Напиши функцию `my_min(first, *rest)` — наименьшее из переданных чисел, без `min`. Хотя бы один аргумент обязателен (это гарантирует сигнатура).

        ```
        my_min(4, -2, 7)   # → -2
        my_min(5)          # → 5
        ```
        """),
        """
        def my_min(first, *rest):
            pass
        """,
        """
        def test_values():
            assert [my_min(4, -2, 7), my_min(5)] == [-2, 5], "Неверный минимум"

        def test_no_min():
            assert "min(" not in open("solution.py", encoding="utf-8").read().replace("my_min(", ""), "Без встроенной min"
        """,
        """
        def my_min(first, *rest):
            best = first
            for x in rest:
                if x < best:
                    best = x
            return best
        """),
    cod(f"{P}-m1-l4-e5", t("""
        Напиши функцию `all_positive(*nums)` — все ли числа больше нуля. Без аргументов — `True`.

        ```
        all_positive(1, 5, 2)   # → True
        all_positive(1, 0)      # → False
        ```
        """),
        """
        def all_positive(*nums):
            pass
        """,
        """
        def test_values():
            assert [all_positive(1, 5, 2), all_positive(1, 0), all_positive()] == [True, False, True], "Неверный результат"
        """,
        """
        def all_positive(*nums):
            return all(n > 0 for n in nums)
        """),
    cod(f"{P}-m1-l4-e6", t("""
        Напиши функцию `unique(*items)` — список переданных значений без повторов, в порядке первого появления.

        ```
        unique(3, 1, 3, 2, 1)   # → [3, 1, 2]
        ```
        """),
        """
        def unique(*items):
            pass
        """,
        """
        def test_values():
            assert [unique(3, 1, 3, 2, 1), unique()] == [[3, 1, 2], []], "Неверный результат"
        """,
        """
        def unique(*items):
            result = []
            for x in items:
                if x not in result:
                    result.append(x)
            return result
        """),
    cod(f"{P}-m1-l4-e7", t("""
        Напиши функцию `format_path(*parts)` — собрать URL-путь из частей: у каждой части убрать слэши по краям, пустые части пропустить, соединить через `/` и добавить `/` в начале.

        ```
        format_path("api", "/v1/", "users")   # → "/api/v1/users"
        format_path()                         # → "/"
        ```
        """),
        """
        def format_path(*parts):
            pass
        """,
        """
        def test_values():
            assert [format_path("api", "/v1/", "users"), format_path(), format_path("/", "x")] == ["/api/v1/users", "/", "/x"], "Неверный путь"
        """,
        """
        def format_path(*parts):
            cleaned = [p.strip("/") for p in parts]
            return "/" + "/".join(p for p in cleaned if p)
        """, xp=20),
    cod(f"{P}-m1-l4-e8", t("""
        Напиши функцию `stats(*nums)` — словарь `{"min": ..., "max": ..., "avg": ...}` (среднее округлить до 2 знаков). Без аргументов — пустой словарь.

        ```
        stats(2, 4, 9)   # → {"min": 2, "max": 9, "avg": 5.0}
        stats()          # → {}
        ```
        """),
        """
        def stats(*nums):
            pass
        """,
        """
        def test_values():
            assert stats(2, 4, 9) == {"min": 2, "max": 9, "avg": 5.0} and stats() == {} and stats(1, 2) == {"min": 1, "max": 2, "avg": 1.5}, "Неверный результат"
        """,
        """
        def stats(*nums):
            if not nums:
                return {}
            return {"min": min(nums), "max": max(nums), "avg": round(sum(nums) / len(nums), 2)}
        """),
),
)
