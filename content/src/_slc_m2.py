"""Тема «Индексы и слайсы», модуль 2 «Срезы» — задания. Теория — в _slc_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "slc"

m2 = module(f"{P}-m2", "Срезы", "✂️", "start:stop, копии, шаг, отрицательный шаг, срезы строк и методы",

lesson(f"{P}-m2-l1", "Срез start:stop",
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        a = [0, 1, 2, 3, 4, 5]
        print(a[1:4], a[:2], a[4:])
        print(a[-3:], a[:-3])
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа? Границы за пределами.", """
        a = [1, 2, 3]
        print(a[1:100])
        print(a[5:])
        print(a[-100:2])
        """),
    out(f"{P}-m2-l1-e6", "Что выведет программа? Пустые срезы.", """
        a = [0, 1, 2, 3, 4, 5]
        print(a[2:2], a[3:1])
        print(a[-2:-1], a[-1:])
        """, hint="Если start не левее stop — срез пустой."),
    cod(f"{P}-m2-l1-e3", t("""
        Напиши функцию `first_n(items, n)` — первые `n` элементов списка. Если элементов меньше — вернуть сколько есть.

        Примеры:
        ```
        first_n([1, 2, 3, 4], 2)   # → [1, 2]
        first_n([1], 5)            # → [1]
        ```
        """),
        """
        def first_n(items, n):
            pass
        """,
        """
        def test_values():
            assert first_n([1, 2, 3, 4], 2) == [1, 2] and first_n([1], 5) == [1] and first_n([], 3) == [], "Неверный срез"
        """,
        """
        def first_n(items, n):
            return items[:n]
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `last_n(items, n)` — последние `n` элементов. При `n = 0` вернуть пустой список.

        Примеры:
        ```
        last_n([1, 2, 3, 4], 2)   # → [3, 4]
        last_n([1, 2], 5)         # → [1, 2]
        last_n([1, 2], 0)         # → []
        ```
        Осторожно: `items[-0:]` — это `items[0:]`, то есть весь список!
        """),
        """
        def last_n(items, n):
            return items[-n:]
        """,
        """
        def test_values():
            assert last_n([1, 2, 3, 4], 2) == [3, 4] and last_n([1, 2], 5) == [1, 2], "Неверный срез"

        def test_zero():
            assert last_n([1, 2], 0) == [], "При n = 0 — пустой список (ловушка -0)"
        """,
        """
        def last_n(items, n):
            return items[len(items) - n:] if n > 0 else []
        """,
        hint="Либо отдельно обработай `n == 0`, либо используй `items[len(items) - n:]` с проверкой.", xp=20),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `without_edges(items)` — список без первого и последнего элемента.

        Примеры:
        ```
        without_edges([1, 2, 3, 4])   # → [2, 3]
        without_edges([1, 2])         # → []
        ```
        """),
        """
        def without_edges(items):
            pass
        """,
        """
        def test_values():
            assert without_edges([1, 2, 3, 4]) == [2, 3] and without_edges([1, 2]) == [] and without_edges(["a", "b", "c"]) == ["b"], "Неверный срез"
        """,
        """
        def without_edges(items):
            return items[1:-1]
        """),
    cod(f"{P}-m2-l1-e7", t("""
        Напиши функцию `first_half(items)` — первая половина списка (при нечётной длине средний элемент **не** входит).

        Примеры:
        ```
        first_half([1, 2, 3, 4])      # → [1, 2]
        first_half([1, 2, 3, 4, 5])   # → [1, 2]
        first_half([])                # → []
        ```
        """),
        """
        def first_half(items):
            pass
        """,
        """
        def test_values():
            got = [first_half([1, 2, 3, 4]), first_half([1, 2, 3, 4, 5]), first_half([]), first_half([7])]
            assert got == [[1, 2], [1, 2], [], []], f"Получено {got}"
        """,
        """
        def first_half(items):
            return items[:len(items) // 2]
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `drop_n(items, n)` — список без первых `n` элементов. Если `n` больше длины — пустой список.

        Примеры:
        ```
        drop_n([1, 2, 3, 4], 1)   # → [2, 3, 4]
        drop_n([1, 2], 5)         # → []
        ```
        """),
        """
        def drop_n(items, n):
            pass
        """,
        """
        def test_values():
            got = [drop_n([1, 2, 3, 4], 1), drop_n([1, 2], 5), drop_n([1, 2], 0)]
            assert got == [[2, 3, 4], [], [1, 2]], f"Получено {got}"
        """,
        """
        def drop_n(items, n):
            return items[n:]
        """)),

lesson(f"{P}-copy", "Срез создаёт копию",
    out(f"{P}-copy-e1", "Что выведет программа? Копия через `[:]`.", """
        a = [1, 2, 3]
        b = a[:]
        b.append(4)
        print(a, b)
        print(a is b, a == b[:3])
        """),
    out(f"{P}-copy-e2", "Что выведет программа? Срез — мелкая копия.", """
        a = [[1], [2]]
        b = a[:]
        b[0].append(9)
        b.append([3])
        print(a)
        print(b)
        """, hint="Внешний список новый, а вложенные — те же."),
    out(f"{P}-copy-e3", "Что выведет программа? Изменение среза не трогает оригинал.", """
        nums = [5, 6, 7, 8]
        part = nums[1:3]
        part[0] = 100
        print(nums, part)
        """),
    cod(f"{P}-copy-e4", t("""
        Напиши функцию `without_first(items)` — **новый** список без первого элемента. Исходный не менять.

        Пример:
        ```
        data = [1, 2, 3]
        without_first(data)   # → [2, 3], data == [1, 2, 3]
        ```
        """),
        """
        def without_first(items):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3]
            assert without_first(data) == [2, 3] and data == [1, 2, 3], "Новый список, исходный не меняется"
            assert without_first([]) == [], "Пустой — пустой"
        """,
        """
        def without_first(items):
            return items[1:]
        """),
    cod(f"{P}-copy-e5", t("""
        Напиши функцию `sorted_copy(items)` — отсортированная **копия**, сделанная через срез `[:]` и метод `sort`.
        Исходный список не менять.

        Пример:
        ```
        data = [3, 1, 2]
        sorted_copy(data)   # → [1, 2, 3], data == [3, 1, 2]
        ```
        """),
        """
        def sorted_copy(items):
            pass
        """,
        """
        def test_values():
            data = [3, 1, 2]
            assert sorted_copy(data) == [1, 2, 3] and data == [3, 1, 2], "Сортируй копию"

        def test_slice():
            src = open("solution.py", encoding="utf-8").read()
            assert "[:]" in src and ".sort(" in src, "Используй [:] и sort"
        """,
        """
        def sorted_copy(items):
            copy = items[:]
            copy.sort()
            return copy
        """),
    cod(f"{P}-copy-e6", t("""
        Напиши функцию `rotate_left(items, k)` — сдвиг списка по кругу **влево** на `k` позиций (новый список).
        `k` может быть больше длины; для пустого списка — пустой.

        Примеры:
        ```
        rotate_left([1, 2, 3, 4, 5], 2)   # → [3, 4, 5, 1, 2]
        rotate_left([1, 2, 3], 4)         # → [2, 3, 1]
        rotate_left([], 3)                # → []
        ```
        Подсказка: `k % len(items)`, затем склей два среза.
        """),
        """
        def rotate_left(items, k):
            pass
        """,
        """
        def test_values():
            got = [rotate_left([1, 2, 3, 4, 5], 2), rotate_left([1, 2, 3], 4), rotate_left([], 3), rotate_left([1, 2], 0)]
            assert got == [[3, 4, 5, 1, 2], [2, 3, 1], [], [1, 2]], f"Получено {got}"
        """,
        """
        def rotate_left(items, k):
            if not items:
                return []
            k = k % len(items)
            return items[k:] + items[:k]
        """, xp=20),
    cod(f"{P}-copy-e7", t("""
        Напиши функцию `rotate_right(items, k)` — сдвиг по кругу **вправо** на `k` позиций (новый список).

        Примеры:
        ```
        rotate_right([1, 2, 3, 4, 5], 2)   # → [4, 5, 1, 2, 3]
        rotate_right([1, 2, 3], 3)         # → [1, 2, 3]
        ```
        """),
        """
        def rotate_right(items, k):
            pass
        """,
        """
        def test_values():
            got = [rotate_right([1, 2, 3, 4, 5], 2), rotate_right([1, 2, 3], 3), rotate_right([], 1), rotate_right([1, 2, 3], 4)]
            assert got == [[4, 5, 1, 2, 3], [1, 2, 3], [], [3, 1, 2]], f"Получено {got}"
        """,
        """
        def rotate_right(items, k):
            if not items:
                return []
            k = k % len(items)
            return items[len(items) - k:] + items[:len(items) - k]
        """, xp=20),
    cod(f"{P}-copy-e8", t("""
        Напиши функцию `head(items, n)` — **новый** список из первых `n` элементов. Изменение результата не должно
        затрагивать исходный список.

        Пример:
        ```
        data = [1, 2, 3]
        h = head(data, 2)   # → [1, 2]
        h.append(99)        # data по-прежнему [1, 2, 3]
        ```
        """),
        """
        def head(items, n):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3]
            h = head(data, 2)
            h.append(99)
            assert h == [1, 2, 99] and data == [1, 2, 3], f"data={data}"
        """,
        """
        def head(items, n):
            return items[:n]
        """)),

lesson(f"{P}-m2-l2", "Шаг среза",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        a = list(range(8))
        print(a[::2], a[1::2], a[::3])
        """),
    out(f"{P}-m2-l2-e6", "Что выведет программа? Шаг с границами.", """
        a = list(range(10))
        print(a[1:8:3])
        print(a[::5], a[2::4])
        print("abcdefgh"[::2])
        """),
    out(f"{P}-m2-l2-e7", "Что выведет программа? Шаг больше длины.", """
        a = [10, 20, 30]
        print(a[::10], a[1::100])
        """),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `split_even_odd(items)` — пара списков: элементы на **чётных** позициях (0, 2, 4…) и на **нечётных** (1, 3, 5…). Используй срезы с шагом.

        Пример:
        ```
        split_even_odd(["a", "b", "c", "d", "e"])   # → (["a", "c", "e"], ["b", "d"])
        ```
        """),
        """
        def split_even_odd(items):
            pass
        """,
        """
        def test_values():
            assert split_even_odd(["a", "b", "c", "d", "e"]) == (["a", "c", "e"], ["b", "d"]) and split_even_odd([]) == ([], []), "Неверное разбиение"
        """,
        """
        def split_even_odd(items):
            return items[::2], items[1::2]
        """),
    cod(f"{P}-m2-l2-e10", t("""
        Напиши функцию `sample(items, k)` — каждый `k`-й элемент, **начиная с `k`-го** (то есть с индекса `k - 1`).

        Примеры:
        ```
        sample([1, 2, 3, 4, 5, 6, 7], 3)   # → [3, 6]
        sample([1, 2], 1)                  # → [1, 2]
        ```
        """),
        """
        def sample(items, k):
            pass
        """,
        """
        def test_values():
            got = [sample([1, 2, 3, 4, 5, 6, 7], 3), sample([1, 2], 1), sample([1, 2], 5)]
            assert got == [[3, 6], [1, 2], []], f"Получено {got}"
        """,
        """
        def sample(items, k):
            return items[k - 1::k]
        """),
    cod(f"{P}-m2-l2-e11", t("""
        Напиши функцию `columns_of(text, width)` — из строки, где записи идут подряд блоками по `width` символов,
        вернуть **первые символы** всех блоков.

        Примеры:
        ```
        columns_of("a1b2c3", 2)      # → "abc"
        columns_of("xyzXYZ", 3)      # → "xX"
        ```
        """),
        """
        def columns_of(text, width):
            pass
        """,
        """
        def test_values():
            got = [columns_of("a1b2c3", 2), columns_of("xyzXYZ", 3), columns_of("", 2)]
            assert got == ["abc", "xX", ""], f"Получено {got}"
        """,
        """
        def columns_of(text, width):
            return text[::width]
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `every_nth(items, n)` — каждый `n`-й элемент, начиная с первого.

        Примеры:
        ```
        every_nth([1, 2, 3, 4, 5, 6, 7], 3)   # → [1, 4, 7]
        every_nth("abcdef", 2)                # → "ace"
        ```
        """),
        """
        def every_nth(items, n):
            pass
        """,
        """
        def test_values():
            assert every_nth([1, 2, 3, 4, 5, 6, 7], 3) == [1, 4, 7] and every_nth("abcdef", 2) == "ace", "Неверный срез"
        """,
        """
        def every_nth(items, n):
            return items[::n]
        """),
    cod(f"{P}-m2-l2-e9", t("""
        Напиши функцию `odd_positions_sum(nums)` — сумма элементов на **нечётных** позициях (1, 3, 5, …).

        Примеры:
        ```
        odd_positions_sum([10, 1, 20, 2, 30, 3])   # → 6
        odd_positions_sum([5])                     # → 0
        ```
        """),
        """
        def odd_positions_sum(nums):
            pass
        """,
        """
        def test_values():
            got = [odd_positions_sum([10, 1, 20, 2, 30, 3]), odd_positions_sum([5]), odd_positions_sum([])]
            assert got == [6, 0, 0], f"Получено {got}"
        """,
        """
        def odd_positions_sum(nums):
            return sum(nums[1::2])
        """)),

lesson(f"{P}-negstep", "Отрицательный шаг и разворот",
    out(f"{P}-m2-l2-e2", "Что выведет программа? Отрицательный шаг.", """
        a = [0, 1, 2, 3, 4, 5]
        print(a[::-1])
        print(a[4:1:-1])
        print(a[1:4:-1])
        print("abc"[::-1])
        """, hint="При шаге -1 срез идёт справа налево; если start левее stop — результат пустой."),
    out(f"{P}-negstep-e1", "Что выведет программа?", """
        a = [0, 1, 2, 3, 4, 5]
        print(a[::-2])
        print(a[-1:-4:-1])
        print(a[:2:-1])
        """, hint="При отрицательном шаге start по умолчанию — конец, stop — начало."),
    out(f"{P}-negstep-e2", "Что выведет программа? Строки.", """
        s = "abcdef"
        print(repr(s[4:1:-1]), repr(s[1:4:-1]))
        print(repr(s[::-3]))
        """),
    cod(f"{P}-m2-l2-e3", t("""
        Напиши функцию `reverse_words(text)` — слова в обратном порядке, через один пробел.

        Пример:
        ```
        reverse_words("one two three")   # → "three two one"
        ```
        Разбей на слова, разверни список срезом `[::-1]`, склей через `" ".join`.
        """),
        """
        def reverse_words(text):
            pass
        """,
        """
        def test_values():
            assert reverse_words("one two three") == "three two one" and reverse_words("solo") == "solo", "Неверный порядок слов"
        """,
        """
        def reverse_words(text):
            return " ".join(text.split()[::-1])
        """),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `is_palindrome(text)` — палиндром ли фраза, **игнорируя регистр и пробелы**. Используй срез `[::-1]`.

        Примеры:
        ```
        is_palindrome("А роза упала на лапу Азора")   # → True
        is_palindrome("Python")                        # → False
        ```
        """),
        """
        def is_palindrome(text):
            pass
        """,
        """
        def test_values():
            got = [is_palindrome(s) for s in ("А роза упала на лапу Азора", "Python", "Шалаш", "a")]
            assert got == [True, False, True, True], f"Получено {got}"
        """,
        """
        def is_palindrome(text):
            clean = text.replace(" ", "").lower()
            return clean == clean[::-1]
        """),
    cod(f"{P}-negstep-e3", t("""
        Напиши функцию `last_k_reversed(items, k)` — последние `k` элементов **в обратном порядке**.
        Если элементов меньше — все в обратном порядке; при `k = 0` — пустой список.

        Примеры:
        ```
        last_k_reversed([1, 2, 3, 4, 5], 2)   # → [5, 4]
        last_k_reversed([1, 2], 5)            # → [2, 1]
        last_k_reversed([1, 2], 0)            # → []
        ```
        """),
        """
        def last_k_reversed(items, k):
            pass
        """,
        """
        def test_values():
            got = [last_k_reversed([1, 2, 3, 4, 5], 2), last_k_reversed([1, 2], 5), last_k_reversed([1, 2], 0)]
            assert got == [[5, 4], [2, 1], []], f"Получено {got}"
        """,
        """
        def last_k_reversed(items, k):
            return items[::-1][:k]
        """,
        hint="Сначала разверни, потом возьми первые k: `items[::-1][:k]`."),
    cod(f"{P}-negstep-e4", t("""
        Напиши функцию `reverse_segment(items, i, j)` — новый список, в котором кусок `items[i:j]` развёрнут, а остальное на месте.

        Пример:
        ```
        reverse_segment([1, 2, 3, 4, 5], 1, 4)   # → [1, 4, 3, 2, 5]
        ```
        """),
        """
        def reverse_segment(items, i, j):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3, 4, 5]
            assert reverse_segment(data, 1, 4) == [1, 4, 3, 2, 5] and data == [1, 2, 3, 4, 5], "Неверный результат или изменён исходный"
            assert reverse_segment([1, 2, 3], 0, 3) == [3, 2, 1], "Весь список"
        """,
        """
        def reverse_segment(items, i, j):
            return items[:i] + items[i:j][::-1] + items[j:]
        """, xp=20),
    cod(f"{P}-negstep-e5", t("""
        Напиши функцию `is_mirror(a, b)` — является ли строка `b` зеркальным отражением строки `a` (та же строка, прочитанная справа налево).

        Примеры:
        ```
        is_mirror("abc", "cba")   # → True
        is_mirror("abc", "abc")   # → False
        is_mirror("", "")         # → True
        ```
        """),
        """
        def is_mirror(a, b):
            pass
        """,
        """
        def test_values():
            got = [is_mirror("abc", "cba"), is_mirror("abc", "abc"), is_mirror("", ""), is_mirror("aba", "aba")]
            assert got == [True, False, True, True], f"Получено {got}"
        """,
        """
        def is_mirror(a, b):
            return a == b[::-1]
        """)),


lesson(f"{P}-m2-l3", "Срезы строк",
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        date = "2024-09-27"
        print(date[:4], date[5:7], date[-2:])
        print(date[::-1])
        """),
    out(f"{P}-m2-l3-e2", "Что выведет программа?", """
        line = "Authorization: Bearer abc123"
        token = line[line.find("Bearer ") + len("Bearer "):]
        print(token)
        print(line[:13])
        """),
    out(f"{P}-m2-l3-e6", "Что выведет программа? Фиксированные позиции в имени файла.", """
        fname = "report_2024.final.pdf"
        print(fname[:6], fname[-3:])
        print(fname[7:11], len(fname))
        """),
    cod(f"{P}-m2-l3-e3", t("""
        Напиши функцию `mask_card(number)` — маскирование номера карты: оставить **последние 4 цифры**, остальное заменить на `*` (длина сохраняется).

        Пример:
        ```
        mask_card("1234567812345678")   # → "************5678"
        ```
        """),
        """
        def mask_card(number):
            pass
        """,
        """
        def test_values():
            assert mask_card("1234567812345678") == "************5678", f"Получено {mask_card('1234567812345678')!r}"
            assert mask_card("12345") == "*2345", "Длина должна сохраняться"
        """,
        """
        def mask_card(number):
            return "*" * (len(number) - 4) + number[-4:]
        """),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `truncate(text, limit)` — обрезать текст до `limit` символов. Если текст обрезан — последние **3** символа результата заменить на `"..."` (итоговая длина ровно `limit`). Если текст не длиннее лимита — вернуть как есть.

        Примеры:
        ```
        truncate("Очень длинное сообщение об ошибке", 12)   # → "Очень дли..."
        truncate("коротко", 12)                             # → "коротко"
        ```
        """),
        """
        def truncate(text, limit):
            pass
        """,
        """
        def test_values():
            assert truncate("Очень длинное сообщение об ошибке", 12) == "Очень дли...", f"Получено {truncate('Очень длинное сообщение об ошибке', 12)!r}"
            assert truncate("коротко", 12) == "коротко", "Короткий текст не трогаем"
            assert len(truncate("x" * 50, 10)) == 10, "Длина результата — ровно limit"
        """,
        """
        def truncate(text, limit):
            if len(text) <= limit:
                return text
            return text[:limit - 3] + "..."
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `domain(email)` — часть email после `@`. Если `@` нет — вернуть пустую строку.

        Примеры:
        ```
        domain("anna@mail.ru")   # → "mail.ru"
        domain("no-at")          # → ""
        ```
        Используй `find("@")` и срез.
        """),
        """
        def domain(email):
            pass
        """,
        """
        def test_values():
            assert domain("anna@mail.ru") == "mail.ru" and domain("x@y") == "y" and domain("no-at") == "", "Неверный домен"
        """,
        """
        def domain(email):
            pos = email.find("@")
            return email[pos + 1:] if pos != -1 else ""
        """),
    cod(f"{P}-m2-l3-e7", t("""
        Напиши функцию `year_of(date)` — год **числом** из даты формата `"ГГГГ-ММ-ДД"`.

        Примеры:
        ```
        year_of("2024-09-27")   # → 2024
        year_of("1999-01-01")   # → 1999
        ```
        """),
        """
        def year_of(date):
            pass
        """,
        """
        def test_values():
            assert year_of("2024-09-27") == 2024 and year_of("1999-01-01") == 1999, "Нужен год числом"
        """,
        """
        def year_of(date):
            return int(date[:4])
        """),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `short_id(uid)` — первые 8 символов идентификатора, а если он короче — весь.

        Примеры:
        ```
        short_id("3f2a9c7e-11aa-4bcd")   # → "3f2a9c7e"
        short_id("abc")                  # → "abc"
        ```
        """),
        """
        def short_id(uid):
            pass
        """,
        """
        def test_values():
            assert short_id("3f2a9c7e-11aa-4bcd") == "3f2a9c7e" and short_id("abc") == "abc", "Неверный результат"
        """,
        """
        def short_id(uid):
            return uid[:8]
        """)),

lesson(f"{P}-strtools", "Срезы и методы строк вместе",
    out(f"{P}-strtools-e1", "Что выведет программа? Поиск с конца.", """
        path = "/home/anna/report.pdf"
        i = path.rfind("/")
        print(path[i + 1:])
        print(path[:i])
        print(path.find("/"), i)
        """),
    out(f"{P}-strtools-e2", "Что выведет программа? partition и rpartition.", """
        print("key=value=x".partition("="))
        print("a.b.c".rpartition("."))
        print("no-sep".partition("="))
        """, hint="`partition` всегда возвращает три части; если разделителя нет — две последние пустые."),
    out(f"{P}-strtools-e3", "Что выведет программа? removeprefix и removesuffix.", """
        print("test_login".removeprefix("test_"))
        print("report.pdf".removesuffix(".pdf"))
        print("abc".removeprefix("x"), "aaa".removeprefix("a"))
        """),
    cod(f"{P}-strtools-e4", t("""
        Напиши функцию `file_name(path)` — имя файла из пути: всё после **последнего** `/`. Если `/` нет — весь путь.

        Примеры:
        ```
        file_name("/home/anna/report.pdf")   # → "report.pdf"
        file_name("notes.txt")               # → "notes.txt"
        ```
        """),
        """
        def file_name(path):
            pass
        """,
        """
        def test_values():
            got = [file_name("/home/anna/report.pdf"), file_name("notes.txt"), file_name("dir/")]
            assert got == ["report.pdf", "notes.txt", ""], f"Получено {got}"
        """,
        """
        def file_name(path):
            return path[path.rfind("/") + 1:]
        """,
        hint="`rfind` вернёт -1, если `/` нет, и `-1 + 1` = 0 — срез с начала."),
    cod(f"{P}-strtools-e5", t("""
        Напиши функцию `extension(filename)` — расширение файла (после **последней** точки) или `""`, если точки нет.
        Используй `rpartition`.

        Примеры:
        ```
        extension("archive.tar.gz")   # → "gz"
        extension("README")           # → ""
        ```
        """),
        """
        def extension(filename):
            pass
        """,
        """
        def test_values():
            got = [extension("archive.tar.gz"), extension("README"), extension("a.pdf")]
            assert got == ["gz", "", "pdf"], f"Получено {got}"
        """,
        """
        def extension(filename):
            head, sep, tail = filename.rpartition(".")
            return tail if sep else ""
        """),
    cod(f"{P}-strtools-e6", t("""
        Напиши функцию `test_title(name)` — убрать у имени теста префикс `"test_"` (если он есть) и заменить `_` на пробелы.

        Примеры:
        ```
        test_title("test_user_login")   # → "user login"
        test_title("smoke_check")       # → "smoke check"
        ```
        """),
        """
        def test_title(name):
            pass
        """,
        """
        def test_values():
            got = [test_title("test_user_login"), test_title("smoke_check"), test_title("test_")]
            assert got == ["user login", "smoke check", ""], f"Получено {got}"
        """,
        """
        def test_title(name):
            return name.removeprefix("test_").replace("_", " ")
        """),
    cod(f"{P}-strtools-e7", t("""
        Напиши функцию `key_value(line)` — разобрать строку `"ключ = значение"` в пару `(ключ, значение)` без пробелов по краям.
        Делить по **первому** `=` (в значении тоже может быть `=`).

        Примеры:
        ```
        key_value("timeout = 30")      # → ("timeout", "30")
        key_value("query=a=b")         # → ("query", "a=b")
        ```
        """),
        """
        def key_value(line):
            pass
        """,
        """
        def test_values():
            assert key_value("timeout = 30") == ("timeout", "30") and key_value("query=a=b") == ("query", "a=b"), "Неверный разбор"
        """,
        """
        def key_value(line):
            key, _, value = line.partition("=")
            return key.strip(), value.strip()
        """),
    cod(f"{P}-strtools-e8", t("""
        Напиши функцию `between(text, left, right)` — подстрока между первым вхождением `left` и следующим за ним `right`.
        Если какой-то метки нет — пустая строка.

        Примеры:
        ```
        between("id=[42] ok", "[", "]")   # → "42"
        between("<b>жирный</b>", "<b>", "</b>")   # → "жирный"
        between("нет меток", "[", "]")    # → ""
        ```
        """),
        """
        def between(text, left, right):
            pass
        """,
        """
        def test_values():
            got = [between("id=[42] ok", "[", "]"), between("<b>жирный</b>", "<b>", "</b>"), between("нет меток", "[", "]"), between("[без конца", "[", "]")]
            assert got == ["42", "жирный", "", ""], f"Получено {got}"
        """,
        """
        def between(text, left, right):
            start = text.find(left)
            if start == -1:
                return ""
            start += len(left)
            end = text.find(right, start)
            if end == -1:
                return ""
            return text[start:end]
        """, xp=20)),
)
