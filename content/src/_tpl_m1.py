"""Тема «Кортежи», модуль 1 «Основы кортежей» — задания. Теория — в _tpl_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "tpl"

m1 = module(f"{P}-m1", "Основы кортежей", "📎", "Создание, доступ, упаковка и распаковка",

lesson(f"{P}-m1-l1", "Создание и неизменяемость",
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        a = (42)
        b = (42,)
        c = 1, 2, 3
        print(type(a).__name__, type(b).__name__, type(c).__name__)
        print(len(c), tuple("abc"))
        """, hint="Кортеж создаёт запятая, а не скобки."),
    out(f"{P}-m1-l1-e2", "Что выведет программа?", """
        point = (3, 4)
        try:
            point[0] = 10
        except TypeError:
            print("кортеж нельзя изменить")
        point = (10, point[1])
        print(point)
        """),
    out(f"{P}-m1-l1-e6", "Что выведет программа?", """
        empty = ()
        one = ("a",)
        not_tuple = ("a")
        print(len(empty), len(one), type(not_tuple).__name__)
        print(tuple([1, 2]), tuple(range(3)))
        """),
    cod(f"{P}-m1-l1-e3", t("""
        Создай переменные:
        - `origin` — кортеж из двух нулей `(0, 0)`;
        - `single` — кортеж из **одного** элемента `"only"`;
        - `letters` — кортеж из символов строки `"xyz"` (через `tuple()`).
        """),
        "",
        """
        def test_values():
            assert origin == (0, 0) and isinstance(origin, tuple), "origin — (0, 0)"
            assert single == ("only",) and isinstance(single, tuple), "single — кортеж из одного элемента: не забудь запятую"
            assert letters == ("x", "y", "z"), "letters — ('x', 'y', 'z')"
        """,
        """
        origin = (0, 0)
        single = ("only",)
        letters = tuple("xyz")
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `move(point, dx, dy)` — вернуть **новый** кортеж-точку, сдвинутую на `dx` по X и `dy` по Y. Исходный кортеж неизменяемый, поэтому нужно создать новый.

        ```
        move((3, 4), 1, -2)   # → (4, 2)
        ```
        """),
        """
        def move(point, dx, dy):
            pass
        """,
        """
        def test_values():
            assert move((3, 4), 1, -2) == (4, 2) and move((0, 0), 0, 0) == (0, 0), "Неверная точка"
            assert isinstance(move((1, 1), 1, 1), tuple), "Верни кортеж"
        """,
        """
        def move(point, dx, dy):
            x, y = point
            return (x + dx, y + dy)
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `freeze(items)` — превратить список в кортеж, чтобы его нельзя было случайно изменить. Функция должна возвращать кортеж, а изменения исходного списка **после** вызова не должны влиять на результат.

        ```
        data = [1, 2]
        frozen = freeze(data)
        data.append(3)
        frozen   # → (1, 2)
        ```
        """),
        """
        def freeze(items):
            return items
        """,
        """
        def test_freeze():
            data = [1, 2]
            frozen = freeze(data)
            data.append(3)
            assert frozen == (1, 2) and isinstance(frozen, tuple), f"Получено {frozen!r}"
        """,
        """
        def freeze(items):
            return tuple(items)
        """),
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `ordered_pair(a, b)` — вернуть кортеж из двух чисел: сначала меньшее, потом большее.

        ```
        ordered_pair(5, 2)   # → (2, 5)
        ordered_pair(1, 1)   # → (1, 1)
        ```
        """),
        """
        def ordered_pair(a, b):
            pass
        """,
        """
        def test_values():
            assert ordered_pair(5, 2) == (2, 5) and ordered_pair(1, 1) == (1, 1) and ordered_pair(-1, 3) == (-1, 3), "Неверная пара"
            assert isinstance(ordered_pair(1, 2), tuple), "Верни кортеж"
        """,
        """
        def ordered_pair(a, b):
            if a <= b:
                return (a, b)
            return (b, a)
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `add_item(t, item)` — вернуть **новый** кортеж: элементы `t` и в конце `item`. Исходный кортеж не меняется (он и не может).

        Осторожно: кортеж из одного элемента пишется с запятой — `(item,)`.

        ```
        add_item((1, 2), 3)    # → (1, 2, 3)
        add_item((), "a")      # → ("a",)
        ```
        """),
        """
        def add_item(t, item):
            pass
        """,
        """
        def test_values():
            src = (1, 2)
            assert add_item(src, 3) == (1, 2, 3) and src == (1, 2), "Неверный результат"
            assert add_item((), "a") == ("a",) and add_item(("x",), (5, 6)) == ("x", (5, 6)), "Элемент добавляется целиком"
        """,
        """
        def add_item(t, item):
            return t + (item,)
        """, hint="Кортежи склеиваются через +, но складывать можно только кортеж с кортежем: (item,)."),
),

lesson(f"{P}-m1-l2", "Доступ, срезы, count и index",
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        t = (10, 20, 30, 20)
        print(t[1], t[-1], t[1:3])
        print(t.count(20), t.index(30), 40 in t)
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа?", """
        a = (1, 2)
        b = a + (3,)
        c = a * 2
        print(a, b, c)
        print(a is b)
        """),
    out(f"{P}-m1-l2-e6", "Что выведет программа?", """
        t = (5, 3, 8, 3)
        print(len(t), min(t), max(t), sum(t))
        print(t[::-1], t[::2])
        try:
            t.index(7)
        except ValueError:
            print("7 нет в кортеже")
        """),
    cod(f"{P}-m1-l2-e3", t("""
        Напиши функцию `rgb_to_hex(color)` — перевести кортеж `(r, g, b)` (числа 0–255) в строку `"#rrggbb"` в нижнем регистре.

        ```
        rgb_to_hex((255, 0, 128))   # → "#ff0080"
        rgb_to_hex((0, 0, 0))       # → "#000000"
        ```
        Формат одного числа: `f"{n:02x}"`.
        """),
        """
        def rgb_to_hex(color):
            pass
        """,
        """
        def test_values():
            assert rgb_to_hex((255, 0, 128)) == "#ff0080" and rgb_to_hex((0, 0, 0)) == "#000000" and rgb_to_hex((16, 32, 48)) == "#102030", "Неверный цвет"
        """,
        """
        def rgb_to_hex(color):
            r, g, b = color
            return f"#{r:02x}{g:02x}{b:02x}"
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `most_common(t)` — элемент кортежа, который встречается **чаще всего** (при равенстве — тот, что раньше встречается в кортеже). Используй `count`.

        ```
        most_common(("pass", "fail", "pass", "skip"))   # → "pass"
        most_common((1, 2, 2, 1))                       # → 1
        ```
        """),
        """
        def most_common(t):
            pass
        """,
        """
        def test_values():
            assert most_common(("pass", "fail", "pass", "skip")) == "pass" and most_common((1, 2, 2, 1)) == 1 and most_common(("x",)) == "x", "Неверный результат"
        """,
        """
        def most_common(t):
            return max(t, key=t.count)
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `version_str(version)` — кортеж версии в строку через точку, а функцию `bump_minor(version)` — вернуть **новый** кортеж с увеличенной второй частью и обнулённой третьей.

        ```
        version_str((1, 10, 3))   # → "1.10.3"
        bump_minor((1, 10, 3))    # → (1, 11, 0)
        ```
        """),
        """
        def version_str(version):
            pass

        def bump_minor(version):
            pass
        """,
        """
        def test_str():
            assert version_str((1, 10, 3)) == "1.10.3" and version_str((2, 0, 0)) == "2.0.0", "Неверная строка"

        def test_bump():
            assert bump_minor((1, 10, 3)) == (1, 11, 0) and bump_minor((0, 0, 9)) == (0, 1, 0), "Неверная версия"
        """,
        """
        def version_str(version):
            return ".".join(str(p) for p in version)

        def bump_minor(version):
            major, minor, _ = version
            return (major, minor + 1, 0)
        """),
    cod(f"{P}-m1-l2-e7", t("""
        Напиши функцию `first_and_last(t)` — кортеж из первого и последнего элементов. Для пустого кортежа — `None`.

        ```
        first_and_last((3, 7, 1))   # → (3, 1)
        first_and_last(("x",))      # → ("x", "x")
        first_and_last(())          # → None
        ```
        """),
        """
        def first_and_last(t):
            pass
        """,
        """
        def test_values():
            assert first_and_last((3, 7, 1)) == (3, 1) and first_and_last(("x",)) == ("x", "x") and first_and_last(()) is None, "Неверный результат"
        """,
        """
        def first_and_last(t):
            if not t:
                return None
            return (t[0], t[-1])
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши функцию `safe_index(t, value)` — индекс первого вхождения `value` или `-1`. Метод `index` падает с `ValueError`, если элемента нет, поэтому сначала проверь `in`.

        ```
        safe_index(("a", "b", "a"), "a")   # → 0
        safe_index((1, 2), 5)              # → -1
        ```
        """),
        """
        def safe_index(t, value):
            pass
        """,
        """
        def test_values():
            assert safe_index(("a", "b", "a"), "a") == 0 and safe_index((1, 2), 5) == -1 and safe_index((), 1) == -1, "Неверный индекс"
        """,
        """
        def safe_index(t, value):
            if value in t:
                return t.index(value)
            return -1
        """),
),

lesson(f"{P}-m1-l3", "Упаковка и распаковка",
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        point = (3, 4, 5)
        x, y, z = point
        print(x + y + z)
        first, *rest = point
        print(first, rest)
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа?", """
        results = [("login", True), ("pay", False)]
        for name, ok in results:
            print(name, "✅" if ok else "❌")
        a, b = 1, 2
        a, b = b, a
        print(a, b)
        """),
    out(f"{P}-m1-l3-e6", "Что выведет программа? Упаковка без скобок.", """
        data = 10, 20
        print(type(data).__name__)
        x, y = data
        x, y = y, x
        print(x, y)
        """),
    cod(f"{P}-m1-l3-e3", t("""
        Напиши функцию `distance(p1, p2)` — расстояние между двумя точками-кортежами `(x, y)`, округлённое до 2 знаков. Распакуй координаты в переменные.

        Формула: `√((x2 − x1)² + (y2 − y1)²)`.

        ```
        distance((0, 0), (3, 4))   # → 5.0
        distance((1, 1), (2, 2))   # → 1.41
        ```
        """),
        """
        def distance(p1, p2):
            pass
        """,
        """
        def test_values():
            assert distance((0, 0), (3, 4)) == 5.0 and distance((1, 1), (2, 2)) == 1.41 and distance((5, 5), (5, 5)) == 0, "Неверное расстояние"
        """,
        """
        def distance(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            return round(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5, 2)
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `parse_record(record)` — распаковать кортеж записи теста `(имя, статус, время, *теги)` в словарь:

        ```
        parse_record(("login", "pass", 1.2, "smoke", "auth"))
        # → {"name": "login", "status": "pass", "time": 1.2, "tags": ["smoke", "auth"]}
        parse_record(("pay", "fail", 3.4))
        # → {"name": "pay", "status": "fail", "time": 3.4, "tags": []}
        ```
        """),
        """
        def parse_record(record):
            pass
        """,
        """
        def test_values():
            assert parse_record(("login", "pass", 1.2, "smoke", "auth")) == {"name": "login", "status": "pass", "time": 1.2, "tags": ["smoke", "auth"]}, "Неверная распаковка"
            assert parse_record(("pay", "fail", 3.4))["tags"] == [], "Без тегов — пустой список"
        """,
        """
        def parse_record(record):
            name, status, time, *tags = record
            return {"name": name, "status": status, "time": time, "tags": tags}
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `rotate(t)` — циклический сдвиг кортежа влево на один элемент, используя распаковку со звёздочкой.

        ```
        rotate((1, 2, 3, 4))   # → (2, 3, 4, 1)
        rotate(("a",))         # → ("a",)
        rotate(())             # → ()
        ```
        """),
        """
        def rotate(t):
            pass
        """,
        """
        def test_values():
            assert rotate((1, 2, 3, 4)) == (2, 3, 4, 1) and rotate(("a",)) == ("a",) and rotate(()) == (), "Неверный сдвиг"
        """,
        """
        def rotate(t):
            if not t:
                return ()
            first, *rest = t
            return (*rest, first)
        """),
    cod(f"{P}-m1-l3-e7", t("""
        Напиши функцию `swap_pairs(pairs)` — список пар, в каждой из которых элементы поменяны местами. Распаковывай пары прямо в цикле.

        ```
        swap_pairs([(1, "a"), (2, "b")])   # → [("a", 1), ("b", 2)]
        ```
        """),
        """
        def swap_pairs(pairs):
            pass
        """,
        """
        def test_values():
            assert swap_pairs([(1, "a"), (2, "b")]) == [("a", 1), ("b", 2)] and swap_pairs([]) == [], "Неверный результат"
        """,
        """
        def swap_pairs(pairs):
            result = []
            for a, b in pairs:
                result.append((b, a))
            return result
        """),
    cod(f"{P}-m1-l3-e8", t("""
        Напиши функцию `split_full_name(full)` — кортеж `(имя, остальное)`: первое слово — имя, все остальные слова через пробел — вторая часть. Используй `first, *rest = ...`.

        ```
        split_full_name("Анна Мария Иванова")   # → ("Анна", "Мария Иванова")
        split_full_name("Боря")                 # → ("Боря", "")
        ```
        """),
        """
        def split_full_name(full):
            pass
        """,
        """
        def test_values():
            got = [split_full_name("Анна Мария Иванова"), split_full_name("Боря"), split_full_name("Иван Петров")]
            assert got == [("Анна", "Мария Иванова"), ("Боря", ""), ("Иван", "Петров")], f"Получено {got}"
        """,
        """
        def split_full_name(full):
            first, *rest = full.split()
            return (first, " ".join(rest))
        """),
),

lesson(f"{P}-unpack2", "Распаковка: тонкости",
    out(f"{P}-unpack2-e1", "Что выведет программа? Вложенная распаковка.", """
        record = ("Аня", (25, "Казань"))
        name, (age, city) = record
        print(name, age, city)
        """),
    out(f"{P}-unpack2-e2", "Что выведет программа?", """
        first, *middle, last = (1, 2, 3, 4, 5)
        print(first, middle, last)
        *head, tail = (1,)
        print(head, tail)
        try:
            a, b = (1, 2, 3)
        except ValueError:
            print("ValueError: лишние значения")
        """),
    out(f"{P}-unpack2-e3", "Что выведет программа? Звёздочка в вызове и в литералах.", """
        def area(w, h):
            return w * h

        size = (3, 4)
        print(area(*size))
        merged = (*size, 5)
        print(merged, [*"ab", *size])
        """),
    cod(f"{P}-unpack2-e4", t("""
        Напиши функцию `describe_point(record)` — `record` имеет вид `("A", (1, 2))`: имя точки и пара координат. Распакуй **вложенно** в одну строку и верни `"A: x=1, y=2"`.
        """),
        """
        def describe_point(record):
            pass
        """,
        """
        def test_values():
            assert describe_point(("A", (1, 2))) == "A: x=1, y=2" and describe_point(("B", (-5, 0))) == "B: x=-5, y=0", "Неверная строка"
        """,
        """
        def describe_point(record):
            name, (x, y) = record
            return f"{name}: x={x}, y={y}"
        """),
    cod(f"{P}-unpack2-e5", t("""
        Напиши функцию `middle(t)` — список элементов кортежа без первого и последнего. Используй распаковку `first, *mid, last`. Если элементов меньше двух — `[]`.

        ```
        middle((1, 2, 3, 4))   # → [2, 3]
        middle((1, 2))         # → []
        middle((1,))           # → []
        ```
        """),
        """
        def middle(t):
            pass
        """,
        """
        def test_values():
            got = [middle((1, 2, 3, 4)), middle((1, 2)), middle((1,)), middle(())]
            assert got == [[2, 3], [], [], []], f"Получено {got}"
        """,
        """
        def middle(t):
            if len(t) < 2:
                return []
            first, *mid, last = t
            return mid
        """),
    cod(f"{P}-unpack2-e6", t("""
        Напиши функцию `call_with(func, args)` — вызвать `func`, передав элементы кортежа `args` как отдельные аргументы (`*args` при вызове), и вернуть результат.

        ```
        call_with(max, (3, 9, 2))      # → 9
        call_with(pow, (2, 10))        # → 1024
        ```
        """),
        """
        def call_with(func, args):
            pass
        """,
        """
        def test_values():
            assert call_with(max, (3, 9, 2)) == 9 and call_with(pow, (2, 10)) == 1024 and call_with(len, ("abc",)) == 3, "Неверный вызов"
        """,
        """
        def call_with(func, args):
            return func(*args)
        """),
    cod(f"{P}-unpack2-e7", t("""
        Напиши функцию `head_tail(t)` — пара `(первый_элемент, кортеж_остальных)`. Звёздочка при распаковке даёт **список** — преврати его в кортеж. Для пустого — `(None, ())`.

        ```
        head_tail((1, 2, 3))   # → (1, (2, 3))
        head_tail(())          # → (None, ())
        ```
        """),
        """
        def head_tail(t):
            pass
        """,
        """
        def test_values():
            got = [head_tail((1, 2, 3)), head_tail(()), head_tail(("a",))]
            assert got == [(1, (2, 3)), (None, ()), ("a", ())], f"Получено {got}"
            assert isinstance(head_tail((1, 2))[1], tuple), "Остаток — кортеж"
        """,
        """
        def head_tail(t):
            if not t:
                return (None, ())
            first, *rest = t
            return (first, tuple(rest))
        """),
    cod(f"{P}-unpack2-e8", t("""
        Напиши функцию `concat(a, b, c)` — склеить три кортежа в один с помощью распаковки внутри литерала: `(*a, *b, *c)`.

        ```
        concat((1,), (2, 3), ())   # → (1, 2, 3)
        ```
        """),
        """
        def concat(a, b, c):
            pass
        """,
        """
        def test_values():
            assert concat((1,), (2, 3), ()) == (1, 2, 3) and concat((), (), ()) == (), "Неверный результат"

        def test_star():
            assert "*a" in open("solution.py", encoding="utf-8").read(), "Используй распаковку (*a, *b, *c)"
        """,
        """
        def concat(a, b, c):
            return (*a, *b, *c)
        """),
),
)
