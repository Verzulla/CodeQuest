"""Тема «Цикл for», модуль 1 «Основы for» — задания. Теория — в _for_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "for"

m1 = module(f"{P}-m1", "Основы for", "🔁", "Перебор коллекций, переменная цикла, range, индексы и вложенные циклы",

lesson(f"{P}-m1-l1", "Перебор коллекций",
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        for fruit in ["яблоко", "банан"]:
            print("я люблю", fruit)
        print("готово")
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа?", """
        for ch in "кот":
            print(ch * 2)
        for key in {"a": 1, "b": 2}:
            print(key)
        """, hint="Перебор словаря даёт ключи."),
    out(f"{P}-m1-l1-e6", "Что выведет программа? Смотри на отступы.", """
        total = 0
        for n in [1, 2, 3]:
            total += n
            print("шаг", total)
        print("итог", total)
        """, hint="Строка без отступа выполняется один раз — после цикла."),
    cod(f"{P}-m1-l1-e3", t("""
        Выведи каждый элемент списка `tests = ["login", "search", "pay"]` на отдельной строке с префиксом `"▶ "`.

        Ожидаемый вывод:
        ```
        ▶ login
        ▶ search
        ▶ pay
        ```
        Используй цикл `for`.
        """),
        """
        tests = ["login", "search", "pay"]
        """,
        """
        def test_output():
            assert OUTPUT.strip().splitlines() == ["▶ login", "▶ search", "▶ pay"], f"Напечатано {OUTPUT!r}"

        def test_loop():
            assert "for " in open("solution.py", encoding="utf-8").read(), "Используй цикл for"
        """,
        """
        tests = ["login", "search", "pay"]
        for name in tests:
            print("▶ " + name)
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `count_char(text, ch)` — сколько раз символ `ch` встречается в строке. Реши **циклом** (без метода `count`).

        Примеры:
        ```
        count_char("banana", "a")   # → 3
        count_char("abc", "z")      # → 0
        ```
        """),
        """
        def count_char(text, ch):
            pass
        """,
        """
        def test_values():
            assert count_char("banana", "a") == 3 and count_char("abc", "z") == 0 and count_char("", "a") == 0, "Неверный подсчёт"

        def test_no_count():
            assert ".count(" not in open("solution.py", encoding="utf-8").read(), "Реши циклом, без count()"
        """,
        """
        def count_char(text, ch):
            n = 0
            for c in text:
                if c == ch:
                    n += 1
            return n
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `longest_word(words)` — самое длинное слово из списка. При равной длине — первое из них. Для пустого списка — `""`.

        Реши циклом, без `max`.

        Примеры:
        ```
        longest_word(["api", "docker", "ci", "pytest"])   # → "docker"
        longest_word([])                                  # → ""
        ```
        """),
        """
        def longest_word(words):
            pass
        """,
        """
        def test_values():
            assert longest_word(["api", "docker", "ci", "pytest"]) == "docker", "docker и pytest одной длины — нужно первое"
            assert longest_word([]) == "" and longest_word(["a"]) == "a", "Неверный результат"
        """,
        """
        def longest_word(words):
            best = ""
            for w in words:
                if len(w) > len(best):
                    best = w
            return best
        """, xp=20),
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `total_price(prices)` — сумма цен из списка. Реши **циклом**, без функции `sum`.

        Примеры:
        ```
        total_price([100, 250, 50])   # → 400
        total_price([])               # → 0
        ```
        """),
        """
        def total_price(prices):
            pass
        """,
        """
        def test_values():
            assert total_price([100, 250, 50]) == 400 and total_price([]) == 0 and total_price([9.5]) == 9.5, "Неверная сумма"

        def test_no_sum():
            assert "sum(" not in open("solution.py", encoding="utf-8").read(), "Реши циклом, без sum()"
        """,
        """
        def total_price(prices):
            total = 0
            for p in prices:
                total += p
            return total
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `spell(word)` — слово по буквам: заглавные буквы через дефис. Собери строку в цикле, без `join`.

        Примеры:
        ```
        spell("кот")   # → "К-О-Т"
        spell("a")     # → "A"
        spell("")      # → ""
        ```
        """),
        """
        def spell(word):
            pass
        """,
        """
        def test_values():
            assert spell("кот") == "К-О-Т" and spell("a") == "A" and spell("") == "", f"spell('кот') = {spell('кот')!r}"

        def test_no_join():
            assert ".join(" not in open("solution.py", encoding="utf-8").read(), "Собери строку в цикле, без join"
        """,
        """
        def spell(word):
            result = ""
            for ch in word:
                if result:
                    result += "-"
                result += ch.upper()
            return result
        """, hint="Дефис нужен перед каждой буквой, кроме первой: проверь, пуста ли ещё строка-результат.", xp=20)),

lesson(f"{P}-iter", "Переменная цикла и что можно перебирать",
    out(f"{P}-iter-e1", "Что выведет программа?", """
        for n in [10, 20, 30]:
            print("шаг", n)
        print("после цикла n =", n)
        """, hint="После цикла переменная хранит последнее значение."),
    out(f"{P}-iter-e2", "Что выведет программа? Изменится ли список?", """
        nums = [1, 2, 3]
        for n in nums:
            n = n * 10
        print(nums, n)
        """, hint="n — просто имя для очередного элемента; присваивание n не трогает список."),
    out(f"{P}-iter-e3", "Что выведет программа?", """
        for name, age in [("Аня", 25), ("Боря", 30)]:
            print(name, "—", age)
        for x in (3, 1):
            print(x * 2)
        """),
    cod(f"{P}-iter-e4", t("""
        Напиши функцию `double_all(nums)` — **новый** список, где каждое число удвоено. Исходный список менять нельзя.

        Примеры:
        ```
        double_all([1, 2, 3])   # → [2, 4, 6]
        double_all([])          # → []
        ```
        """),
        """
        def double_all(nums):
            pass
        """,
        """
        def test_values():
            assert double_all([1, 2, 3]) == [2, 4, 6] and double_all([]) == [], f"Получено {double_all([1, 2, 3])}"

        def test_original():
            src = [5, 6]
            double_all(src)
            assert src == [5, 6], "Исходный список изменился"
        """,
        """
        def double_all(nums):
            result = []
            for n in nums:
                result.append(n * 2)
            return result
        """, hint="n = n * 2 внутри цикла ничего не сохранит — собирай результаты в новый список через append."),
    cod(f"{P}-iter-e5", t("""
        Напиши функцию `format_people(people)`, где `people` — список пар `(имя, возраст)`. Верни список строк `"имя (возраст)"`. Распакуй пару прямо в заголовке цикла: `for name, age in people:`.

        Пример:
        ```
        format_people([("Аня", 25), ("Боря", 30)])   # → ["Аня (25)", "Боря (30)"]
        ```
        """),
        """
        def format_people(people):
            pass
        """,
        """
        def test_values():
            got = format_people([("Аня", 25), ("Боря", 30)])
            assert got == ["Аня (25)", "Боря (30)"] and format_people([]) == [], f"Получено {got}"
        """,
        """
        def format_people(people):
            result = []
            for name, age in people:
                result.append(f"{name} ({age})")
            return result
        """),
    cod(f"{P}-iter-e6", t("""
        Напиши функцию `count_items(collection)` — сколько элементов выдаёт цикл `for` по коллекции. Функция должна работать для строки, списка, кортежа, словаря и `range`. Реши циклом, **без `len`**.

        Примеры:
        ```
        count_items("abc")              # → 3
        count_items({"a": 1, "b": 2})   # → 2
        count_items(range(5))           # → 5
        ```
        """),
        """
        def count_items(collection):
            pass
        """,
        """
        def test_values():
            got = [count_items(x) for x in ("abc", [1, 2], (1,), {"a": 1, "b": 2}, range(5), "")]
            assert got == [3, 2, 1, 2, 5, 0], f"Получено {got}"

        def test_no_len():
            assert "len(" not in open("solution.py", encoding="utf-8").read(), "Реши циклом, без len()"
        """,
        """
        def count_items(collection):
            n = 0
            for _ in collection:
                n += 1
            return n
        """, hint="Сам элемент не нужен — назови переменную _ и просто прибавляй 1."),
    cod(f"{P}-iter-e7", t("""
        Напиши функцию `last_item(items)` — последний элемент коллекции, найденный **циклом** (без индексов и срезов). Для пустой коллекции — `None`.

        Примеры:
        ```
        last_item([3, 7, 1])   # → 1
        last_item("кот")       # → "т"
        last_item([])          # → None
        ```
        """),
        """
        def last_item(items):
            pass
        """,
        """
        def test_values():
            assert last_item([3, 7, 1]) == 1 and last_item("кот") == "т" and last_item([]) is None, "Неверный результат"

        def test_no_index():
            src = open("solution.py", encoding="utf-8").read()
            assert "[-1]" not in src and "[len" not in src, "Реши циклом, без индексов"
        """,
        """
        def last_item(items):
            last = None
            for x in items:
                last = x
            return last
        """, hint="После цикла переменная хранит последнее значение. Но если коллекция пуста, цикл не выполнится — заведи значение заранее."),
    cod(f"{P}-iter-e8", t("""
        Напиши функцию `total_of(values)`: если передано одно число (`int`) — вернуть его; если коллекция чисел (список, кортеж) — вернуть сумму, посчитанную циклом.

        Зачем проверка: `for x in 5` падает с `TypeError: 'int' object is not iterable`.

        Примеры:
        ```
        total_of(5)           # → 5
        total_of([1, 2, 3])   # → 6
        total_of((10, 20))    # → 30
        ```
        """),
        """
        def total_of(values):
            pass
        """,
        """
        def test_values():
            assert total_of(5) == 5 and total_of([1, 2, 3]) == 6 and total_of((10, 20)) == 30 and total_of([]) == 0, "Неверный результат"
        """,
        """
        def total_of(values):
            if isinstance(values, int):
                return values
            total = 0
            for v in values:
                total += v
            return total
        """, hint="Сначала isinstance(values, int), потом цикл."),
),

lesson(f"{P}-m1-l2", "range",
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        print(list(range(4)))
        print(list(range(2, 6)))
        print(list(range(0, 10, 3)))
        print(list(range(5, 0, -1)))
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа?", """
        total = 0
        for i in range(1, 5):
            total += i
        print(total)
        print(len(range(100)), list(range(3, 3)))
        """),
    out(f"{P}-m1-l2-e6", "Что выведет программа? range — тоже коллекция.", """
        r = range(1, 10, 2)
        print(r)
        print(len(r), r[0], r[-1], 7 in r, 8 in r)
        """),
    cod(f"{P}-m1-l2-e3", t("""
        С помощью `for` и `range` выведи таблицу умножения на 7 от `7 x 1 = 7` до `7 x 10 = 70`.

        Каждая строка — в формате `7 x N = R`, всего 10 строк:
        ```
        7 x 1 = 7
        7 x 2 = 14
        ...
        7 x 10 = 70
        ```
        """),
        "",
        """
        def test_lines():
            lines = OUTPUT.strip().splitlines()
            assert len(lines) == 10, f"Нужно 10 строк, а напечатано {len(lines)}"
            assert lines[0] == "7 x 1 = 7" and lines[-1] == "7 x 10 = 70", f"Первая: {lines[0]!r}, последняя: {lines[-1]!r}"
        """,
        """
        for n in range(1, 11):
            print(f"7 x {n} = {7 * n}")
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `sum_even(n)` — сумма всех **чётных** чисел от 0 до `n` включительно. Используй `range` **с шагом 2**.

        Примеры:
        ```
        sum_even(10)   # → 30   (0 + 2 + 4 + 6 + 8 + 10)
        sum_even(7)    # → 12   (0 + 2 + 4 + 6)
        ```
        """),
        """
        def sum_even(n):
            pass
        """,
        """
        def test_values():
            assert [sum_even(n) for n in (10, 7, 0, 1)] == [30, 12, 0, 0], "Неверная сумма"
        """,
        """
        def sum_even(n):
            total = 0
            for i in range(0, n + 1, 2):
                total += i
            return total
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `countdown(n)` — список чисел от `n` до 1, а в конце строка `"Старт!"`. Используй `range` с отрицательным шагом.

        Примеры:
        ```
        countdown(3)   # → [3, 2, 1, "Старт!"]
        countdown(0)   # → ["Старт!"]
        ```
        """),
        """
        def countdown(n):
            pass
        """,
        """
        def test_values():
            assert countdown(3) == [3, 2, 1, "Старт!"] and countdown(0) == ["Старт!"] and countdown(1) == [1, "Старт!"], "Неверный отсчёт"
        """,
        """
        def countdown(n):
            result = []
            for i in range(n, 0, -1):
                result.append(i)
            result.append("Старт!")
            return result
        """),
    cod(f"{P}-m1-l2-e7", t("""
        Напиши функцию `odd_numbers(a, b)` — список нечётных чисел от `a` до `b` **включительно**. Используй `range` с шагом 2 — начало подбери так, чтобы оно было нечётным.

        Примеры:
        ```
        odd_numbers(1, 9)    # → [1, 3, 5, 7, 9]
        odd_numbers(4, 10)   # → [5, 7, 9]
        odd_numbers(5, 4)    # → []
        ```
        """),
        """
        def odd_numbers(a, b):
            pass
        """,
        """
        def test_values():
            got = [odd_numbers(1, 9), odd_numbers(4, 10), odd_numbers(5, 4), odd_numbers(7, 7)]
            assert got == [[1, 3, 5, 7, 9], [5, 7, 9], [], [7]], f"Получено {got}"
        """,
        """
        def odd_numbers(a, b):
            start = a if a % 2 == 1 else a + 1
            result = []
            for n in range(start, b + 1, 2):
                result.append(n)
            return result
        """, hint="Если a чётное — начни с a + 1. Конец range не включается, поэтому b + 1.", xp=20),
    cod(f"{P}-m1-l2-e8", t("""
        Выведи числа `10 8 6 4 2 0` **в одну строку** через пробел, используя `range` с отрицательным шагом.

        Подсказка: `print(n, end=" ")` не переводит строку, либо собери строку в переменной.

        Ожидаемый вывод:
        ```
        10 8 6 4 2 0
        ```
        """),
        "",
        """
        def test_output():
            assert OUTPUT.strip() == "10 8 6 4 2 0", f"Напечатано {OUTPUT!r}"

        def test_range():
            assert "range(" in open("solution.py", encoding="utf-8").read(), "Используй range"
        """,
        """
        for n in range(10, -1, -2):
            print(n, end=" ")
        print()
        """, hint="Чтобы 0 попал в результат, конец range должен быть -1."),
),

lesson(f"{P}-range2", "Индексы в цикле: range(len(...))",
    out(f"{P}-range2-e1", "Что выведет программа?", """
        names = ["Аня", "Боря", "Вика"]
        for i in range(len(names)):
            print(i, names[i])
        """),
    out(f"{P}-range2-e2", "Что выведет программа? Здесь список меняется.", """
        nums = [1, 2, 3]
        for i in range(len(nums)):
            nums[i] = nums[i] * 10
        print(nums)
        """, hint="Присваивание по индексу nums[i] = … меняет сам список."),
    out(f"{P}-range2-e3", "Что выведет программа? Соседние элементы.", """
        temps = [3, 5, 4, 8]
        for i in range(len(temps) - 1):
            print(temps[i + 1] - temps[i])
        """, hint="i идёт до предпоследнего индекса, чтобы i + 1 не вышел за границу."),
    cod(f"{P}-range2-e4", t("""
        Напиши функцию `double_in_place(nums)` — удвоить каждое число **в самом списке** (по индексу). Функция ничего не возвращает.

        Пример:
        ```
        data = [1, 5, 10]
        double_in_place(data)
        data   # → [2, 10, 20]
        ```
        """),
        """
        def double_in_place(nums):
            pass
        """,
        """
        def test_in_place():
            data = [1, 5, 10]
            res = double_in_place(data)
            assert data == [2, 10, 20], f"Список стал {data}"
            assert res is None, "Функция, меняющая список на месте, возвращает None"
        """,
        """
        def double_in_place(nums):
            for i in range(len(nums)):
                nums[i] *= 2
        """, hint="for i in range(len(nums)): nums[i] *= 2"),
    cod(f"{P}-range2-e5", t("""
        Напиши функцию `is_sorted(nums)` — отсортирован ли список по неубыванию. Сравнивай **соседей** `nums[i]` и `nums[i + 1]`. Пустой список и список из одного элемента считаются отсортированными.

        Примеры:
        ```
        is_sorted([1, 2, 2, 5])   # → True
        is_sorted([3, 1, 2])      # → False
        ```
        """),
        """
        def is_sorted(nums):
            pass
        """,
        """
        def test_values():
            got = [is_sorted(x) for x in ([1, 2, 2, 5], [3, 1, 2], [], [7], [1, 3, 2])]
            assert got == [True, False, True, True, False], f"Получено {got}"

        def test_no_sorted():
            assert "sorted(" not in open("solution.py", encoding="utf-8").read().replace("is_sorted(", ""), "Сравни соседей в цикле, без sorted()"
        """,
        """
        def is_sorted(nums):
            for i in range(len(nums) - 1):
                if nums[i] > nums[i + 1]:
                    return False
            return True
        """, hint="range(len(nums) - 1) — чтобы nums[i + 1] существовал."),
    cod(f"{P}-range2-e6", t("""
        Напиши функцию `count_increases(values)` — сколько раз следующее значение **больше** предыдущего.

        Примеры:
        ```
        count_increases([1, 2, 2, 5, 3])   # → 2   (1→2 и 2→5)
        count_increases([5])               # → 0
        ```
        """),
        """
        def count_increases(values):
            pass
        """,
        """
        def test_values():
            got = [count_increases(x) for x in ([1, 2, 2, 5, 3], [5], [], [1, 2, 3, 4])]
            assert got == [2, 0, 0, 3], f"Получено {got}"
        """,
        """
        def count_increases(values):
            count = 0
            for i in range(1, len(values)):
                if values[i] > values[i - 1]:
                    count += 1
            return count
        """),
    cod(f"{P}-range2-e7", t("""
        Напиши функцию `every_other(items)` — элементы с **чётными индексами** (0, 2, 4, …). Используй `range` с шагом 2, без срезов.

        Пример:
        ```
        every_other(["a", "b", "c", "d", "e"])   # → ["a", "c", "e"]
        ```
        """),
        """
        def every_other(items):
            pass
        """,
        """
        def test_values():
            assert every_other(["a", "b", "c", "d", "e"]) == ["a", "c", "e"] and every_other([1, 2]) == [1] and every_other([]) == [], "Неверный результат"

        def test_no_slice():
            assert "::" not in open("solution.py", encoding="utf-8").read(), "Реши через range с шагом, без среза"
        """,
        """
        def every_other(items):
            result = []
            for i in range(0, len(items), 2):
                result.append(items[i])
            return result
        """),
    cod(f"{P}-range2-e8", t("""
        Напиши функцию `diff_positions(a, b)` — список индексов, где строки `a` и `b` (одинаковой длины) отличаются.

        Примеры:
        ```
        diff_positions("abcd", "abed")   # → [2]
        diff_positions("кот", "кит")     # → [1]
        diff_positions("ok", "ok")       # → []
        ```
        """),
        """
        def diff_positions(a, b):
            pass
        """,
        """
        def test_values():
            got = [diff_positions("abcd", "abed"), diff_positions("кот", "кит"), diff_positions("ok", "ok"), diff_positions("ab", "ba")]
            assert got == [[2], [1], [], [0, 1]], f"Получено {got}"
        """,
        """
        def diff_positions(a, b):
            result = []
            for i in range(len(a)):
                if a[i] != b[i]:
                    result.append(i)
            return result
        """),
),

lesson(f"{P}-m1-l3", "Вложенные циклы",
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        for i in range(1, 3):
            for j in range(1, 3):
                print(i, j)
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа?", """
        for n in range(1, 4):
            print("*" * n)
        """),
    out(f"{P}-m1-l3-e6", "Что выведет программа? Сколько раз выполнится тело внутреннего цикла?", """
        count = 0
        for i in range(3):
            for j in range(4):
                count += 1
        print(count)
        """, hint="Внутренний цикл целиком выполняется на каждом шаге внешнего: 3 × 4."),
    cod(f"{P}-m1-l3-e3", t("""
        Напиши функцию `test_matrix(browsers, sizes)` — список строк `"браузер@размер"` для **всех комбинаций**, используя вложенные циклы. Сначала все размеры для первого браузера.

        Пример:
        ```
        test_matrix(["chrome", "firefox"], [1920, 375])
        # → ["chrome@1920", "chrome@375", "firefox@1920", "firefox@375"]
        ```
        """),
        """
        def test_matrix(browsers, sizes):
            pass
        """,
        """
        def test_combinations():
            got = test_matrix(["chrome", "firefox"], [1920, 375])
            assert got == ["chrome@1920", "chrome@375", "firefox@1920", "firefox@375"], f"Получено {got}"
            assert test_matrix([], [1]) == [], "Нет браузеров — пусто"
        """,
        """
        def test_matrix(browsers, sizes):
            result = []
            for b in browsers:
                for s in sizes:
                    result.append(f"{b}@{s}")
            return result
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `multiplication_table(n)` — таблица умножения `n × n` в виде **списка строк**, числа в строке через пробел.

        Пример:
        ```
        multiplication_table(3)
        # → ["1 2 3", "2 4 6", "3 6 9"]
        ```
        """),
        """
        def multiplication_table(n):
            pass
        """,
        """
        def test_values():
            assert multiplication_table(3) == ["1 2 3", "2 4 6", "3 6 9"] and multiplication_table(1) == ["1"], "Неверная таблица"
        """,
        """
        def multiplication_table(n):
            rows = []
            for i in range(1, n + 1):
                row = []
                for j in range(1, n + 1):
                    row.append(str(i * j))
                rows.append(" ".join(row))
            return rows
        """, xp=20),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `pairs_with_sum(nums, target)` — список всех пар `(a, b)` из списка, где `a + b == target`, **без повторов** и без пары элемента с самим собой. Пара берётся в порядке индексов (`i < j`).

        Пример:
        ```
        pairs_with_sum([1, 2, 3, 4], 5)   # → [(1, 4), (2, 3)]
        ```
        Подсказка: внешний цикл по `i`, внутренний — по `j` от `i + 1`.
        """),
        """
        def pairs_with_sum(nums, target):
            pass
        """,
        """
        def test_values():
            assert pairs_with_sum([1, 2, 3, 4], 5) == [(1, 4), (2, 3)], f"Получено {pairs_with_sum([1, 2, 3, 4], 5)}"
            assert pairs_with_sum([5], 10) == [] and pairs_with_sum([2, 2], 4) == [(2, 2)], "Неверный результат"
        """,
        """
        def pairs_with_sum(nums, target):
            result = []
            for i in range(len(nums)):
                for j in range(i + 1, len(nums)):
                    if nums[i] + nums[j] == target:
                        result.append((nums[i], nums[j]))
            return result
        """, xp=25),
    cod(f"{P}-m1-l3-e7", t("""
        Напиши функцию `coordinates(rows, cols)` — список всех пар `(строка, столбец)` для сетки `rows × cols`, нумерация с 0, сначала вся первая строка.

        Пример:
        ```
        coordinates(2, 3)
        # → [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
        ```
        """),
        """
        def coordinates(rows, cols):
            pass
        """,
        """
        def test_values():
            assert coordinates(2, 3) == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)], f"Получено {coordinates(2, 3)}"
            assert coordinates(0, 5) == [] and coordinates(1, 1) == [(0, 0)], "Неверный результат"
        """,
        """
        def coordinates(rows, cols):
            result = []
            for r in range(rows):
                for c in range(cols):
                    result.append((r, c))
            return result
        """),
    cod(f"{P}-m1-l3-e8", t("""
        Напиши функцию `has_common(a, b)` — есть ли хотя бы один элемент, который есть и в списке `a`, и в списке `b`. Используй **вложенные циклы** (без `in` для поиска по списку и без множеств).

        Примеры:
        ```
        has_common([1, 2, 3], [5, 3])   # → True
        has_common(["a"], ["b", "c"])   # → False
        ```
        """),
        """
        def has_common(a, b):
            pass
        """,
        """
        def test_values():
            got = [has_common([1, 2, 3], [5, 3]), has_common(["a"], ["b", "c"]), has_common([], [1]), has_common([2], [2])]
            assert got == [True, False, False, True], f"Получено {got}"
        """,
        """
        def has_common(a, b):
            for x in a:
                for y in b:
                    if x == y:
                        return True
            return False
        """, hint="Сравни каждый x из a с каждым y из b; совпало — сразу return True."),
),

lesson(f"{P}-nested2", "Вложенные циклы: таблицы и узоры",
    out(f"{P}-nested2-e1", "Что выведет программа? Список списков — это таблица.", """
        matrix = [[1, 2, 3], [4, 5, 6]]
        for row in matrix:
            line = ""
            for x in row:
                line += str(x * 10) + "|"
            print(line)
        """),
    out(f"{P}-nested2-e2", "Что выведет программа? Внутренний range зависит от внешнего.", """
        for i in range(1, 4):
            for j in range(i):
                print(i, end="")
            print()
        """, hint='end="" не переводит строку; пустой print() — переводит.'),
    out(f"{P}-nested2-e3", "Что выведет программа?", """
        grid = [[1, 2], [3, 4], [5, 6]]
        total = 0
        for row in grid:
            for x in row:
                total += x
        print(total, len(grid), len(grid[0]))
        """),
    cod(f"{P}-nested2-e4", t("""
        Напиши функцию `row_sums(matrix)` — список сумм каждой строки таблицы. Считай вложенным циклом, без `sum`.

        Пример:
        ```
        row_sums([[1, 2, 3], [4, 5, 6]])   # → [6, 15]
        row_sums([[], [7]])                # → [0, 7]
        ```
        """),
        """
        def row_sums(matrix):
            pass
        """,
        """
        def test_values():
            assert row_sums([[1, 2, 3], [4, 5, 6]]) == [6, 15] and row_sums([[], [7]]) == [0, 7] and row_sums([]) == [], "Неверный результат"

        def test_no_sum():
            assert "sum(" not in open("solution.py", encoding="utf-8").read(), "Считай вложенным циклом, без sum()"
        """,
        """
        def row_sums(matrix):
            result = []
            for row in matrix:
                total = 0
                for x in row:
                    total += x
                result.append(total)
            return result
        """, hint="Счётчик total обнуляй внутри внешнего цикла — перед каждой строкой."),
    cod(f"{P}-nested2-e5", t("""
        Напиши функцию `matrix_max(matrix)` — наибольшее число во всей таблице (таблица не пустая, строки не пустые). Без `max`.

        Пример:
        ```
        matrix_max([[3, 8], [1, 9, 2], [-5]])   # → 9
        ```
        """),
        """
        def matrix_max(matrix):
            pass
        """,
        """
        def test_values():
            assert matrix_max([[3, 8], [1, 9, 2], [-5]]) == 9 and matrix_max([[-3, -1], [-7]]) == -1, "Неверный максимум"

        def test_no_max():
            assert "max(" not in open("solution.py", encoding="utf-8").read().replace("matrix_max(", ""), "Реши циклами, без max()"
        """,
        """
        def matrix_max(matrix):
            best = matrix[0][0]
            for row in matrix:
                for x in row:
                    if x > best:
                        best = x
            return best
        """, hint="Начни с matrix[0][0], а не с 0 — числа могут быть отрицательными."),
    cod(f"{P}-nested2-e6", t("""
        Напиши функцию `transpose(matrix)` — «повернуть» таблицу: столбцы становятся строками. Все строки одинаковой длины, таблица не пустая.

        Пример:
        ```
        transpose([[1, 2, 3], [4, 5, 6]])   # → [[1, 4], [2, 5], [3, 6]]
        ```
        Подсказка: внешний цикл — по номеру столбца `c`, внутренний — по строкам.
        """),
        """
        def transpose(matrix):
            pass
        """,
        """
        def test_values():
            assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]], f"Получено {transpose([[1, 2, 3], [4, 5, 6]])}"
            assert transpose([[1]]) == [[1]] and transpose([[1, 2]]) == [[1], [2]], "Неверный результат"
        """,
        """
        def transpose(matrix):
            result = []
            for c in range(len(matrix[0])):
                column = []
                for row in matrix:
                    column.append(row[c])
                result.append(column)
            return result
        """, xp=25),
    cod(f"{P}-nested2-e7", t("""
        Напиши функцию `count_in_matrix(matrix, value)` — сколько раз `value` встречается в таблице.

        Пример:
        ```
        count_in_matrix([["pass", "fail"], ["pass", "pass"]], "pass")   # → 3
        ```
        """),
        """
        def count_in_matrix(matrix, value):
            pass
        """,
        """
        def test_values():
            assert count_in_matrix([["pass", "fail"], ["pass", "pass"]], "pass") == 3 and count_in_matrix([[1, 2]], 5) == 0 and count_in_matrix([], 1) == 0, "Неверный подсчёт"
        """,
        """
        def count_in_matrix(matrix, value):
            count = 0
            for row in matrix:
                for x in row:
                    if x == value:
                        count += 1
            return count
        """),
    cod(f"{P}-nested2-e8", t("""
        Напиши функцию `find_in_matrix(matrix, value)` — координаты `(строка, столбец)` **первого** вхождения `value` (обход по строкам слева направо) или `None`.

        Пример:
        ```
        find_in_matrix([[1, 2], [3, 2]], 2)   # → (0, 1)
        find_in_matrix([[1]], 9)              # → None
        ```
        Подсказка: `enumerate` даёт номер и элемент сразу.
        """),
        """
        def find_in_matrix(matrix, value):
            pass
        """,
        """
        def test_values():
            got = [find_in_matrix([[1, 2], [3, 2]], 2), find_in_matrix([[1]], 9), find_in_matrix([[0, 0], [0, 7]], 7)]
            assert got == [(0, 1), None, (1, 1)], f"Получено {got}"
        """,
        """
        def find_in_matrix(matrix, value):
            for r, row in enumerate(matrix):
                for c, x in enumerate(row):
                    if x == value:
                        return (r, c)
            return None
        """, hint="return внутри двух циклов сразу завершает функцию — и оба цикла.", xp=20),
),
)
