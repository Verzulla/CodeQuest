"""Тема «Индексы и слайсы», модуль 3 «Приёмы со срезами» — задания. Теория — в _slc_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "slc"

m3 = module(f"{P}-m3", "Приёмы со срезами", "🧩", "Изменение срезами, шаг и slice(), пачки и окна, разбор записей",

lesson(f"{P}-m3-l1", "Изменение списка срезами",
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        a = [0, 1, 2, 3, 4]
        a[1:3] = ["x", "y", "z"]
        print(a)
        del a[-2:]
        print(a)
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа?", """
        a = [1, 2, 3]
        b = a
        a[:] = [9]
        print(a, b)
        c = a
        a = []
        print(a, c)
        """, hint="`a[:] = ...` меняет содержимое того же объекта, а `a = []` создаёт новый."),
    out(f"{P}-m3-l1-e6", "Что выведет программа? Вставка через пустой срез.", """
        a = [1, 2, 3]
        a[1:1] = ["x", "y"]
        print(a)
        a[:0] = [0]
        print(a)
        a[len(a):] = [9]
        print(a)
        """, hint="Присваивание пустому срезу ничего не заменяет — только вставляет."),
    cod(f"{P}-m3-l1-e3", t("""
        Напиши функцию `drop_first(items, n)`, которая **удаляет** первые `n` элементов из самого списка (через `del` со срезом) и возвращает этот же список.

        Пример:
        ```
        data = [1, 2, 3, 4]
        drop_first(data, 2)   # → [3, 4], и data == [3, 4]
        ```
        """),
        """
        def drop_first(items, n):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3, 4]
            assert drop_first(data, 2) == [3, 4] and data == [3, 4], "Удалить нужно из самого списка"
        """,
        """
        def drop_first(items, n):
            del items[:n]
            return items
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `replace_middle(items, new)` — заменить всё, кроме первого и последнего элемента, на элементы из `new` (изменить сам список и вернуть его).

        Пример:
        ```
        replace_middle([1, 2, 3, 4], ["a"])   # → [1, "a", 4]
        ```
        """),
        """
        def replace_middle(items, new):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3, 4]
            assert replace_middle(data, ["a"]) == [1, "a", 4] and data == [1, "a", 4], "Замена середины через срез"
            assert replace_middle([1, 2], ["x", "y"]) == [1, "x", "y", 2], "Середину можно и расширить"
        """,
        """
        def replace_middle(items, new):
            items[1:-1] = new
            return items
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `keep_last(history, n)` — оставить в списке истории только **последние** `n` записей (изменить сам список, вернуть его). Так ограничивают размер лога.

        Пример:
        ```
        h = [1, 2, 3, 4, 5]
        keep_last(h, 3)   # → [3, 4, 5], h == [3, 4, 5]
        ```
        """),
        """
        def keep_last(history, n):
            pass
        """,
        """
        def test_values():
            h = [1, 2, 3, 4, 5]
            assert keep_last(h, 3) == [3, 4, 5] and h == [3, 4, 5], "Должен измениться сам список"
            h2 = [1, 2]
            assert keep_last(h2, 5) == [1, 2], "Если записей меньше — оставить все"
        """,
        """
        def keep_last(history, n):
            del history[:max(0, len(history) - n)]
            return history
        """, xp=20),
    cod(f"{P}-m3-l1-e7", t("""
        Напиши функцию `insert_many(items, index, values)` — вставить все элементы `values` **перед** позицией `index`
        в сам список (присваиванием пустому срезу) и вернуть его.

        Пример:
        ```
        insert_many([1, 4], 1, [2, 3])   # → [1, 2, 3, 4]
        ```
        """),
        """
        def insert_many(items, index, values):
            pass
        """,
        """
        def test_values():
            data = [1, 4]
            assert insert_many(data, 1, [2, 3]) == [1, 2, 3, 4] and data == [1, 2, 3, 4], "Вставь в сам список"
            assert insert_many([1], 0, []) == [1], "Пустая вставка ничего не меняет"
        """,
        """
        def insert_many(items, index, values):
            items[index:index] = values
            return items
        """),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `replace_all_items(items, new)` — заменить **всё содержимое** списка на элементы `new`,
        сохранив **тот же** объект списка (другие ссылки на него должны увидеть изменения). Вернуть список.

        Пример:
        ```
        data = [1, 2, 3]
        alias = data
        replace_all_items(data, ["a"])   # data и alias == ["a"]
        ```
        """),
        """
        def replace_all_items(items, new):
            items = new
            return items
        """,
        """
        def test_values():
            data = [1, 2, 3]
            alias = data
            result = replace_all_items(data, ["a"])
            assert alias == ["a"] and result is data, f"alias={alias} — нужно менять содержимое, а не перевешивать имя"
        """,
        """
        def replace_all_items(items, new):
            items[:] = new
            return items
        """,
        hint="`items = new` перевешивает только локальное имя. Нужно `items[:] = new`.")),

lesson(f"{P}-ext", "Присваивание с шагом и объект slice",
    out(f"{P}-ext-e1", "Что выведет программа? Замена через срез с шагом.", """
        a = [0, 0, 0, 0, 0, 0]
        a[::2] = [1, 2, 3]
        print(a)
        a[1::2] = ["x"] * 3
        print(a)
        """),
    out(f"{P}-ext-e2", "Что выведет программа? Длины должны совпасть.", """
        a = [1, 2, 3, 4]
        try:
            a[::2] = [9]
        except ValueError as e:
            print("ошибка:", e)
        print(a)
        """, hint="У среза с шагом нельзя изменить количество элементов."),
    out(f"{P}-ext-e3", "Что выведет программа? Именованные срезы.", """
        YEAR = slice(0, 4)
        LEVEL = slice(8, None)
        rec = "20240927ERROR"
        print(rec[YEAR], rec[LEVEL])
        print(rec[slice(4, 6)], YEAR.start, YEAR.stop)
        """),
    cod(f"{P}-ext-e4", t("""
        Напиши функцию `zero_even_positions(items)` — обнулить элементы на чётных позициях (0, 2, 4…) в **самом** списке
        одним присваиванием срезу с шагом. Вернуть список.

        Пример:
        ```
        zero_even_positions([5, 6, 7, 8, 9])   # → [0, 6, 0, 8, 0]
        ```
        """),
        """
        def zero_even_positions(items):
            pass
        """,
        """
        def test_values():
            data = [5, 6, 7, 8, 9]
            assert zero_even_positions(data) == [0, 6, 0, 8, 0] and data == [0, 6, 0, 8, 0], f"data={data}"
            assert zero_even_positions([]) == [], "Пустой список"
        """,
        """
        def zero_even_positions(items):
            items[::2] = [0] * len(items[::2])
            return items
        """,
        hint="Справа нужен список ровно той длины, что и `items[::2]`."),
    cod(f"{P}-ext-e5", t("""
        Напиши функцию `swap_pairs(items)` — поменять местами соседние пары элементов в **самом** списке чётной длины:
        0-й с 1-м, 2-й с 3-м и т. д. Используй срезы с шагом. Вернуть список.

        Пример:
        ```
        swap_pairs([1, 2, 3, 4])   # → [2, 1, 4, 3]
        ```
        """),
        """
        def swap_pairs(items):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3, 4]
            assert swap_pairs(data) == [2, 1, 4, 3] and data == [2, 1, 4, 3], f"data={data}"
            assert swap_pairs(["a", "b"]) == ["b", "a"] and swap_pairs([]) == [], "Неверный обмен"
        """,
        """
        def swap_pairs(items):
            items[::2], items[1::2] = items[1::2], items[::2]
            return items
        """, xp=20),
    cod(f"{P}-ext-e6", t("""
        Напиши функцию `parse_record(rec)` для записей фиксированной ширины `"ГГГГММДДУРОВЕНЬ"`:
        первые 4 символа — год, следующие 2 — месяц, следующие 2 — день, остальное — уровень.
        Верни кортеж `(год, месяц, день, уровень)`, числа — **числами**. Используй именованные срезы `slice(...)`.

        Пример:
        ```
        parse_record("20240927ERROR")   # → (2024, 9, 27, "ERROR")
        ```
        """),
        """
        def parse_record(rec):
            pass
        """,
        """
        def test_values():
            assert parse_record("20240927ERROR") == (2024, 9, 27, "ERROR") and parse_record("19990101INFO") == (1999, 1, 1, "INFO"), "Неверный разбор"

        def test_slice():
            src = open("solution.py", encoding="utf-8").read()
            assert "slice(" in src, "Используй slice(...)"
        """,
        """
        YEAR = slice(0, 4)
        MONTH = slice(4, 6)
        DAY = slice(6, 8)
        LEVEL = slice(8, None)

        def parse_record(rec):
            return int(rec[YEAR]), int(rec[MONTH]), int(rec[DAY]), rec[LEVEL]
        """),
    cod(f"{P}-ext-e7", t("""
        Напиши функцию `fill_every_third(items, value)` — заменить на `value` каждый третий элемент (позиции 0, 3, 6…)
        в самом списке. Вернуть список.

        Пример:
        ```
        fill_every_third([1, 2, 3, 4, 5, 6, 7], "*")   # → ["*", 2, 3, "*", 5, 6, "*"]
        ```
        """),
        """
        def fill_every_third(items, value):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3, 4, 5, 6, 7]
            assert fill_every_third(data, "*") == ["*", 2, 3, "*", 5, 6, "*"] and data[0] == "*", f"data={data}"
        """,
        """
        def fill_every_third(items, value):
            items[::3] = [value] * len(items[::3])
            return items
        """),
    cod(f"{P}-ext-e8", t("""
        Напиши функцию `negate_odd_positions(nums)` — поменять знак у чисел на нечётных позициях (1, 3, 5…) в самом списке.
        Вернуть список.

        Пример:
        ```
        negate_odd_positions([1, 2, 3, 4, 5])   # → [1, -2, 3, -4, 5]
        ```
        """),
        """
        def negate_odd_positions(nums):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3, 4, 5]
            assert negate_odd_positions(data) == [1, -2, 3, -4, 5] and data == [1, -2, 3, -4, 5], f"data={data}"
        """,
        """
        def negate_odd_positions(nums):
            negated = []
            for x in nums[1::2]:
                negated.append(-x)
            nums[1::2] = negated
            return nums
        """)),

lesson(f"{P}-m3-l2", "Пачки и скользящее окно",
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        items = [1, 2, 3, 4, 5]
        for i in range(0, len(items), 2):
            print(items[i:i + 2])
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа?", """
        items = [1, 2, 3, 4]
        for i in range(len(items) - 2 + 1):
            print(items[i:i + 2])
        """),
    out(f"{P}-m3-l2-e6", "Что выведет программа? Пачки из строки.", """
        s = "abcdefg"
        for i in range(0, len(s), 3):
            print(s[i:i + 3])
        """),
    cod(f"{P}-m3-l2-e3", t("""
        Напиши функцию `chunks(items, size)` — разбить список на куски длины `size` (последний может быть короче).

        Примеры:
        ```
        chunks([1, 2, 3, 4, 5], 2)   # → [[1, 2], [3, 4], [5]]
        chunks([], 3)                # → []
        ```
        """),
        """
        def chunks(items, size):
            pass
        """,
        """
        def test_values():
            assert chunks([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]] and chunks([], 3) == [] and chunks([1, 2], 5) == [[1, 2]], "Неверное разбиение"
        """,
        """
        def chunks(items, size):
            return [items[i:i + size] for i in range(0, len(items), size)]
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши функцию `moving_average(values, k)` — список средних по окну длины `k` (окно сдвигается на 1). Каждое среднее округли до 2 знаков.

        Пример:
        ```
        moving_average([1, 2, 3, 4, 5], 3)   # → [2.0, 3.0, 4.0]
        ```
        Если элементов меньше `k` — пустой список.
        """),
        """
        def moving_average(values, k):
            pass
        """,
        """
        def test_values():
            assert moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0], "Неверные средние"
            assert moving_average([1, 2], 3) == [], "Меньше k элементов — пусто"
            assert moving_average([0.3, 0.3, 0.4], 2) == [0.3, 0.35], "Округление до 2 знаков"
        """,
        """
        def moving_average(values, k):
            return [round(sum(values[i:i + k]) / k, 2) for i in range(len(values) - k + 1)]
        """, xp=20),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `has_streak(results, k)` — есть ли в истории прогонов **`k` падений подряд** (`"fail"`). Используй окна.

        Примеры:
        ```
        has_streak(["pass", "fail", "fail", "fail", "pass"], 3)   # → True
        has_streak(["fail", "pass", "fail"], 2)                  # → False
        ```
        """),
        """
        def has_streak(results, k):
            pass
        """,
        """
        def test_values():
            assert has_streak(["pass", "fail", "fail", "fail", "pass"], 3) is True, "Три fail подряд есть"
            assert has_streak(["fail", "pass", "fail"], 2) is False, "Двух подряд нет"
            assert has_streak([], 1) is False, "Пустая история — False"
        """,
        """
        def has_streak(results, k):
            for i in range(len(results) - k + 1):
                if results[i:i + k] == ["fail"] * k:
                    return True
            return False
        """, xp=20),
    cod(f"{P}-m3-l2-e7", t("""
        Напиши функцию `adjacent_pairs(items)` — список соседних пар (окна длины 2), каждое окно — список.

        Примеры:
        ```
        adjacent_pairs([1, 2, 3])   # → [[1, 2], [2, 3]]
        adjacent_pairs([1])         # → []
        ```
        """),
        """
        def adjacent_pairs(items):
            pass
        """,
        """
        def test_values():
            got = [adjacent_pairs([1, 2, 3]), adjacent_pairs([1]), adjacent_pairs([])]
            assert got == [[[1, 2], [2, 3]], [], []], f"Получено {got}"
        """,
        """
        def adjacent_pairs(items):
            result = []
            for i in range(len(items) - 1):
                result.append(items[i:i + 2])
            return result
        """),
    cod(f"{P}-m3-l2-e8", t("""
        Напиши функцию `max_window_sum(nums, k)` — наибольшая сумма среди всех окон длины `k`.
        Если элементов меньше `k` — вернуть `None`.

        Примеры:
        ```
        max_window_sum([1, 5, 2, 8, 1], 2)   # → 10
        max_window_sum([1, 2], 3)            # → None
        ```
        """),
        """
        def max_window_sum(nums, k):
            pass
        """,
        """
        def test_values():
            got = [max_window_sum([1, 5, 2, 8, 1], 2), max_window_sum([1, 2], 3), max_window_sum([-3, -1, -2], 1)]
            assert got == [10, None, -1], f"Получено {got}"
        """,
        """
        def max_window_sum(nums, k):
            if len(nums) < k:
                return None
            best = sum(nums[:k])
            for i in range(1, len(nums) - k + 1):
                best = max(best, sum(nums[i:i + k]))
            return best
        """, xp=20)),

lesson(f"{P}-m3-l3", "Распаковка при разборе записей",
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        first, *rest = [10, 20, 30, 40]
        print(first, rest)
        *start, last = "abc"
        print(start, last)
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа?", """
        header, *rows = ["name;status", "login;pass", "pay;fail"]
        print(header)
        for row in rows:
            name, status = row.split(";")
            print(name, status)
        """),
    out(f"{P}-m3-l3-e6", "Что выведет программа?", """
        record = "Анна;25;Казань"
        name, age, city = record.split(";")
        print(city, int(age) + 1)
        date, _, rest = "2024-09-27 ERROR".partition(" ")
        print(date, rest)
        """),
    cod(f"{P}-m3-l3-e3", t("""
        Напиши функцию `split_head(items)` — пара `(первый, остальные)` через распаковку со звёздочкой. Для пустого списка вернуть `(None, [])`.

        Примеры:
        ```
        split_head([1, 2, 3])   # → (1, [2, 3])
        split_head([5])         # → (5, [])
        split_head([])          # → (None, [])
        ```
        """),
        """
        def split_head(items):
            pass
        """,
        """
        def test_values():
            assert split_head([1, 2, 3]) == (1, [2, 3]) and split_head([5]) == (5, []) and split_head([]) == (None, []), "Неверная распаковка"
        """,
        """
        def split_head(items):
            if not items:
                return None, []
            first, *rest = items
            return first, rest
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `parse_log(line)` — разобрать строку лога `"дата время уровень сообщение из нескольких слов"`:

        - вернуть словарь `{"date": ..., "time": ..., "level": ..., "message": ...}`;
        - `message` — все оставшиеся слова, склеенные через пробел.

        Пример:
        ```
        parse_log("2024-09-27 12:00:01 ERROR нет связи с БД")
        # → {"date": "2024-09-27", "time": "12:00:01", "level": "ERROR", "message": "нет связи с БД"}
        ```
        Используй `date, time, level, *words = line.split()`.
        """),
        """
        def parse_log(line):
            pass
        """,
        """
        def test_values():
            got = parse_log("2024-09-27 12:00:01 ERROR нет связи с БД")
            assert got == {"date": "2024-09-27", "time": "12:00:01", "level": "ERROR", "message": "нет связи с БД"}, f"Получено {got}"
            assert parse_log("d t INFO ok")["message"] == "ok", "Одно слово в сообщении"
        """,
        """
        def parse_log(line):
            date, time, level, *words = line.split()
            return {"date": date, "time": time, "level": level, "message": " ".join(words)}
        """, xp=20),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `swap_ends(items)` — вернуть **новый** список, где первый и последний элементы поменялись местами (список минимум из 2 элементов). Используй распаковку `first, *middle, last = items`.

        Пример:
        ```
        swap_ends([1, 2, 3, 4])   # → [4, 2, 3, 1]
        swap_ends(["a", "b"])     # → ["b", "a"]
        ```
        """),
        """
        def swap_ends(items):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3, 4]
            assert swap_ends(data) == [4, 2, 3, 1] and swap_ends(["a", "b"]) == ["b", "a"], "Неверный результат"
            assert data == [1, 2, 3, 4], "Исходный список не должен меняться"
        """,
        """
        def swap_ends(items):
            first, *middle, last = items
            return [last, *middle, first]
        """),
    cod(f"{P}-m3-l3-e7", t("""
        Напиши функцию `csv_table(lines)`: первая строка списка — заголовок, остальные — данные; значения разделены `;`.
        Вернуть пару: список названий колонок и список строк данных (каждая строка — список значений).

        Пример:
        ```
        csv_table(["name;status", "login;pass", "pay;fail"])
        # → (["name", "status"], [["login", "pass"], ["pay", "fail"]])
        ```
        """),
        """
        def csv_table(lines):
            pass
        """,
        """
        def test_values():
            got = csv_table(["name;status", "login;pass", "pay;fail"])
            assert got == (["name", "status"], [["login", "pass"], ["pay", "fail"]]), f"Получено {got}"
            assert csv_table(["a;b"]) == (["a", "b"], []), "Только заголовок — данных нет"
        """,
        """
        def csv_table(lines):
            header, *rows = lines
            table = []
            for row in rows:
                table.append(row.split(";"))
            return header.split(";"), table
        """),
    cod(f"{P}-m3-l3-e8", t("""
        Напиши функцию `first_and_last_word(text)` — пара: первое и последнее слово текста. Если слово одно — оно и первое, и последнее.

        Примеры:
        ```
        first_and_last_word("раз два три")   # → ("раз", "три")
        first_and_last_word("один")          # → ("один", "один")
        ```
        """),
        """
        def first_and_last_word(text):
            pass
        """,
        """
        def test_values():
            assert first_and_last_word("раз два три") == ("раз", "три") and first_and_last_word("один") == ("один", "один"), "Неверный результат"
        """,
        """
        def first_and_last_word(text):
            words = text.split()
            return words[0], words[-1]
        """)),
)
