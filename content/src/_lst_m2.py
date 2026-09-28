"""Тема «Списки», модуль 2 «Поиск и перебор» — задания. Теория — в _lst_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "lst"

m2 = module(f"{P}-m2", "Поиск и перебор", "🔎", "index и count, цикл for, enumerate и zip, фильтрация, sum/min/max/any/all",

lesson(f"{P}-m2-l1", "Поиск и подсчёт",
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        codes = [200, 404, 200, 500, 200]
        print(codes.count(200), codes.index(404), 500 in codes)
        print(min(codes), max(codes))
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа?", """
        words = ["b", "a", "c", "a"]
        print(words.index("a"))
        print(words.count("z"))
        print(max(words), min(words))
        """, hint="Строки сравниваются по алфавиту."),
    out(f"{P}-m2-l1-e6", "Что выведет программа? Поиск с позиции и сумма с началом.", """
        nums = [3, 1, 3, 2]
        print(nums.index(3), nums.index(3, 1))
        print(nums.count(3), sum(nums), sum(nums, 10))
        """, hint="`index(x, start)` ищет начиная с позиции `start`."),
    cod(f"{P}-m2-l1-e3", t("""
        Напиши функцию `find_index(items, value)` — индекс первого вхождения `value` или `-1`, если его нет (без ошибки).

        Примеры:
        ```
        find_index(["a", "b"], "b")   # → 1
        find_index(["a", "b"], "z")   # → -1
        ```
        """),
        """
        def find_index(items, value):
            pass
        """,
        """
        def test_values():
            assert find_index(["a", "b", "b"], "b") == 1 and find_index(["a"], "z") == -1 and find_index([], 1) == -1, "Неверный индекс"
        """,
        """
        def find_index(items, value):
            if value in items:
                return items.index(value)
            return -1
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `pass_rate(results)` — процент прошедших тестов.

        - `results` — список строк `"pass"` и `"fail"`.
        - Вернуть целый процент `"pass"` (округление вниз через `//`). Для пустого списка — `0`.

        Примеры:
        ```
        pass_rate(["pass", "pass", "fail"])   # → 66
        pass_rate([])                         # → 0
        ```
        Используй `count`.
        """),
        """
        def pass_rate(results):
            pass
        """,
        """
        def test_values():
            assert pass_rate(["pass", "pass", "fail"]) == 66 and pass_rate([]) == 0 and pass_rate(["pass"]) == 100, "Неверный процент"
        """,
        """
        def pass_rate(results):
            if not results:
                return 0
            return results.count("pass") * 100 // len(results)
        """),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `all_indexes(items, value)` — список **всех** индексов, где встречается `value`.

        Примеры:
        ```
        all_indexes(["a", "b", "a", "c", "a"], "a")   # → [0, 2, 4]
        all_indexes([1, 2], 3)                        # → []
        ```
        Используй `enumerate`.
        """),
        """
        def all_indexes(items, value):
            pass
        """,
        """
        def test_values():
            assert all_indexes(["a", "b", "a", "c", "a"], "a") == [0, 2, 4] and all_indexes([1, 2], 3) == [], "Неверные индексы"
        """,
        """
        def all_indexes(items, value):
            result = []
            for i, item in enumerate(items):
                if item == value:
                    result.append(i)
            return result
        """, xp=20),
    cod(f"{P}-m2-l1-e7", t("""
        Напиши функцию `count_failed(results)` — сколько раз в списке встречается `"fail"`.

        Примеры:
        ```
        count_failed(["pass", "fail", "fail"])   # → 2
        count_failed([])                         # → 0
        ```
        """),
        """
        def count_failed(results):
            pass
        """,
        """
        def test_values():
            assert count_failed(["pass", "fail", "fail"]) == 2 and count_failed([]) == 0 and count_failed(["pass"]) == 0, "Неверный подсчёт"
        """,
        """
        def count_failed(results):
            return results.count("fail")
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `next_index(items, value, start)` — индекс первого вхождения `value` **начиная с позиции `start`**,
        или `-1`, если дальше такого значения нет.

        Примеры:
        ```
        next_index(["a", "b", "a"], "a", 1)   # → 2
        next_index(["a", "b", "a"], "a", 0)   # → 0
        next_index(["a", "b"], "a", 1)        # → -1
        ```
        """),
        """
        def next_index(items, value, start):
            pass
        """,
        """
        def test_values():
            got = [next_index(["a", "b", "a"], "a", 1), next_index(["a", "b", "a"], "a", 0), next_index(["a", "b"], "a", 1)]
            assert got == [2, 0, -1], f"Получено {got}"
        """,
        """
        def next_index(items, value, start):
            try:
                return items.index(value, start)
            except ValueError:
                return -1
        """,
        hint="`items.index(value, start)` падает, если не нашёл. Проверь заранее или перехвати ValueError.")),

lesson(f"{P}-for", "Перебор списка циклом for",
    out(f"{P}-for-e1", "Что выведет программа?", """
        for x in [3, 1, 2]:
            print(x * 10)
        """),
    out(f"{P}-for-e2", "Что выведет программа? Накопление в цикле.", """
        total = 0
        for price in [150, 99, 250]:
            total += price
            print("промежуточно:", total)
        print("итого:", total)
        """, hint="`print` внутри цикла выполняется на каждом шаге, после цикла — один раз."),
    out(f"{P}-for-e3", "Что выведет программа? Индексы и обратный порядок.", """
        items = ["a", "b", "c"]
        for i in range(len(items)):
            print(i, items[i])
        for x in reversed(items):
            print(x, end="")
        print()
        """),
    cod(f"{P}-for-e4", t("""
        Напиши функцию `double_all(nums)` — **новый** список, где каждое число умножено на 2. Исходный список не менять.

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
            data = [1, 2, 3]
            assert double_all(data) == [2, 4, 6] and data == [1, 2, 3], "Новый список, исходный не меняется"
            assert double_all([]) == [], "Пустой — пустой"
        """,
        """
        def double_all(nums):
            result = []
            for n in nums:
                result.append(n * 2)
            return result
        """),
    cod(f"{P}-for-e5", t("""
        Напиши функцию `count_long(words, n)` — сколько слов в списке **длиннее** `n` символов.

        Примеры:
        ```
        count_long(["кот", "собака", "ёж"], 3)   # → 1
        count_long([], 1)                        # → 0
        ```
        """),
        """
        def count_long(words, n):
            pass
        """,
        """
        def test_values():
            got = [count_long(["кот", "собака", "ёж"], 3), count_long([], 1), count_long(["abc", "abcd"], 2)]
            assert got == [1, 0, 2], f"Получено {got}"
        """,
        """
        def count_long(words, n):
            count = 0
            for w in words:
                if len(w) > n:
                    count += 1
            return count
        """),
    cod(f"{P}-for-e6", t("""
        Напиши функцию `increment_all(nums)`, которая увеличивает **каждый элемент самого списка** на 1 (без создания нового)
        и возвращает этот список.

        Пример:
        ```
        data = [1, 5, 9]
        increment_all(data)   # → [2, 6, 10], и data тоже [2, 6, 10]
        ```
        Подсказка: `for n in nums: n += 1` список не меняет — нужен перебор по индексам.
        """),
        """
        def increment_all(nums):
            pass
        """,
        """
        def test_values():
            data = [1, 5, 9]
            result = increment_all(data)
            assert data == [2, 6, 10] and result is data, f"Нужно изменить сам список, сейчас data={data}"
        """,
        """
        def increment_all(nums):
            for i in range(len(nums)):
                nums[i] += 1
            return nums
        """),
    cod(f"{P}-for-e7", t("""
        Напиши функцию `print_items(items)`, которая **печатает** каждый элемент на отдельной строке с дефисом в начале.

        Пример: `print_items(["хлеб", "молоко"])` печатает
        ```
        - хлеб
        - молоко
        ```
        Возвращать ничего не нужно.
        """),
        """
        def print_items(items):
            pass
        """,
        """
        def test_output():
            out = capture(print_items, ["хлеб", "молоко"])
            assert out == "- хлеб\\n- молоко\\n", f"Напечатано {out!r}"

        def test_empty():
            assert capture(print_items, []) == "", "Для пустого списка ничего не печатать"
        """,
        """
        def print_items(items):
            for item in items:
                print("-", item)
        """),
    cod(f"{P}-for-e8", t("""
        Напиши функцию `reversed_copy(items)` — новый список с элементами в обратном порядке. Исходный не менять.
        Используй `reversed`.

        Пример:
        ```
        reversed_copy([1, 2, 3])   # → [3, 2, 1]
        ```
        """),
        """
        def reversed_copy(items):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3]
            assert reversed_copy(data) == [3, 2, 1] and data == [1, 2, 3], "Новый развёрнутый список, исходный не меняется"
        """,
        """
        def reversed_copy(items):
            return list(reversed(items))
        """)),

lesson(f"{P}-m2-l2", "enumerate и zip",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        for i, name in enumerate(["login", "pay"], start=1):
            print(i, name)
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа?", """
        names = ["a", "b", "c"]
        codes = [200, 404]
        for name, code in zip(names, codes):
            print(name, code)
        """, hint="`zip` останавливается на самом коротком."),
    out(f"{P}-m2-l2-e6", "Что выведет программа?", """
        print(list(enumerate("ab", 1)))
        print(list(zip([1, 2], [3, 4], [5, 6])))
        print(list(zip("ab", [1, 2, 3])))
        """),
    cod(f"{P}-m2-l2-e3", t("""
        Напиши функцию `numbered(items)`, которая возвращает список строк вида `"<номер>. <элемент>"`, нумерация с 1.

        Пример:
        ```
        numbered(["login", "pay"])   # → ["1. login", "2. pay"]
        ```
        """),
        """
        def numbered(items):
            pass
        """,
        """
        def test_values():
            assert numbered(["login", "pay"]) == ["1. login", "2. pay"] and numbered([]) == [], "Неверный результат"
        """,
        """
        def numbered(items):
            result = []
            for i, item in enumerate(items, start=1):
                result.append(f"{i}. {item}")
            return result
        """),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `compare_results(expected, actual)`, которая сравнивает два списка попарно и возвращает список **индексов**, где значения не совпали.

        Списки одинаковой длины.

        Пример:
        ```
        compare_results([200, 201, 404], [200, 500, 404])   # → [1]
        ```
        Используй `enumerate(zip(expected, actual))`.
        """),
        """
        def compare_results(expected, actual):
            pass
        """,
        """
        def test_values():
            assert compare_results([200, 201, 404], [200, 500, 404]) == [1], "Не совпал только индекс 1"
            assert compare_results([1, 2], [3, 4]) == [0, 1] and compare_results([], []) == [], "Неверный результат"
        """,
        """
        def compare_results(expected, actual):
            diff = []
            for i, (e, a) in enumerate(zip(expected, actual)):
                if e != a:
                    diff.append(i)
            return diff
        """, xp=20),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `to_dict(keys, values)`, которая собирает словарь из двух списков: ключ из `keys`, значение из `values` на той же позиции.

        Пример:
        ```
        to_dict(["login", "pay"], [True, False])   # → {"login": True, "pay": False}
        ```
        Используй `zip` в цикле или `dict(zip(...))`.
        """),
        """
        def to_dict(keys, values):
            pass
        """,
        """
        def test_values():
            assert to_dict(["login", "pay"], [True, False]) == {"login": True, "pay": False} and to_dict([], []) == {}, "Неверный словарь"
        """,
        """
        def to_dict(keys, values):
            return dict(zip(keys, values))
        """),
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `pair_sums(a, b)` — список сумм элементов на одинаковых позициях двух списков
        (лишние элементы более длинного списка не учитываются).

        Примеры:
        ```
        pair_sums([1, 2, 3], [10, 20, 30])   # → [11, 22, 33]
        pair_sums([1, 2], [5])               # → [6]
        ```
        """),
        """
        def pair_sums(a, b):
            pass
        """,
        """
        def test_values():
            assert pair_sums([1, 2, 3], [10, 20, 30]) == [11, 22, 33] and pair_sums([1, 2], [5]) == [6] and pair_sums([], [1]) == [], "Неверные суммы"
        """,
        """
        def pair_sums(a, b):
            result = []
            for x, y in zip(a, b):
                result.append(x + y)
            return result
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `first_mismatch(a, b)` — индекс **первой** позиции, где элементы двух списков различаются,
        или `-1`, если на общих позициях всё совпадает.

        Примеры:
        ```
        first_mismatch([1, 2, 3], [1, 5, 3])   # → 1
        first_mismatch([1, 2], [1, 2])         # → -1
        ```
        """),
        """
        def first_mismatch(a, b):
            pass
        """,
        """
        def test_values():
            got = [first_mismatch([1, 2, 3], [1, 5, 3]), first_mismatch([1, 2], [1, 2]), first_mismatch([9], [0, 1])]
            assert got == [1, -1, 0], f"Получено {got}"
        """,
        """
        def first_mismatch(a, b):
            for i, (x, y) in enumerate(zip(a, b)):
                if x != y:
                    return i
            return -1
        """)),

lesson(f"{P}-m3-l1", "Накопление и фильтрация",
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        nums = [4, -2, 7, 0, -5]
        positive = []
        for n in nums:
            if n > 0:
                positive.append(n)
        print(positive, sum(positive))
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа?", """
        results = ["pass", "pass", "fail"]
        print(any(r == "fail" for r in results))
        print(all(r == "pass" for r in results))
        """),
    out(f"{P}-m3-l1-e6", "Что выведет программа? Фильтр + преобразование.", """
        words = ["qa", "dev", "ops", "a"]
        short = []
        for w in words:
            if len(w) <= 2:
                short.append(w.upper())
        print(short)
        """),
    cod(f"{P}-m3-l1-e3", t("""
        Напиши функцию `only_even(nums)` — новый список только из чётных чисел, в исходном порядке. Исходный список не менять.

        Пример:
        ```
        only_even([1, 2, 3, 4, 6])   # → [2, 4, 6]
        ```
        """),
        """
        def only_even(nums):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3, 4, 6]
            assert only_even(data) == [2, 4, 6] and only_even([1, 3]) == [], "Неверный результат"
            assert data == [1, 2, 3, 4, 6], "Исходный список не должен меняться"
        """,
        """
        def only_even(nums):
            result = []
            for n in nums:
                if n % 2 == 0:
                    result.append(n)
            return result
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `average(nums)` — среднее арифметическое, округлённое до 2 знаков. Для пустого списка вернуть `0`.

        Примеры:
        ```
        average([2, 4, 6])   # → 4.0
        average([1, 2, 2])   # → 1.67
        average([])          # → 0
        ```
        """),
        """
        def average(nums):
            pass
        """,
        """
        def test_values():
            assert average([2, 4, 6]) == 4 and average([1, 2, 2]) == 1.67 and average([]) == 0, "Неверное среднее"
        """,
        """
        def average(nums):
            if not nums:
                return 0
            return round(sum(nums) / len(nums), 2)
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `my_max(nums)` — максимум непустого списка **без** встроенной `max`.

        Примеры:
        ```
        my_max([3, 9, 2])      # → 9
        my_max([-5, -2, -9])   # → -2
        ```
        Начни не с 0, а с первого элемента — иначе сломаешься на отрицательных.
        """),
        """
        def my_max(nums):
            pass
        """,
        """
        def test_values():
            assert my_max([3, 9, 2]) == 9 and my_max([-5, -2, -9]) == -2 and my_max([4]) == 4, "Неверный максимум"

        def test_no_builtin():
            assert "max(" not in open("solution.py", encoding="utf-8").read().replace("my_max(", ""), "Не используй встроенную max"
        """,
        """
        def my_max(nums):
            best = nums[0]
            for n in nums:
                if n > best:
                    best = n
            return best
        """),
    cod(f"{P}-m3-l1-e7", t("""
        Напиши функцию `positives_sum(nums)` — сумма только **положительных** чисел.

        Примеры:
        ```
        positives_sum([4, -2, 7, 0])   # → 11
        positives_sum([-1, -5])        # → 0
        ```
        """),
        """
        def positives_sum(nums):
            pass
        """,
        """
        def test_values():
            assert positives_sum([4, -2, 7, 0]) == 11 and positives_sum([-1, -5]) == 0 and positives_sum([]) == 0, "Неверная сумма"
        """,
        """
        def positives_sum(nums):
            total = 0
            for n in nums:
                if n > 0:
                    total += n
            return total
        """),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `names_with_status(tests, status)`. `tests` — список пар `[имя, статус]`.
        Вернуть список **имён** тестов с нужным статусом, в исходном порядке.

        Пример:
        ```
        tests = [["login", "pass"], ["pay", "fail"], ["cart", "fail"]]
        names_with_status(tests, "fail")   # → ["pay", "cart"]
        ```
        """),
        """
        def names_with_status(tests, status):
            pass
        """,
        """
        def test_values():
            tests = [["login", "pass"], ["pay", "fail"], ["cart", "fail"]]
            assert names_with_status(tests, "fail") == ["pay", "cart"] and names_with_status(tests, "skip") == [], "Неверный фильтр"
        """,
        """
        def names_with_status(tests, status):
            result = []
            for name, st in tests:
                if st == status:
                    result.append(name)
            return result
        """)),

lesson(f"{P}-aggr", "sum, min, max, any и all",
    out(f"{P}-aggr-e1", "Что выведет программа? Пустые списки.", """
        print(sum([]))
        print(max([3, 1], default=0), max([], default=0))
        print(min(["b", "a", "c"]))
        """),
    out(f"{P}-aggr-e2", "Что выведет программа? any и all.", """
        print(any([]), all([]))
        print(any([0, "", None]), all([1, "a", [0]]))
        print(all(x > 0 for x in [1, 2, -3]))
        """, hint="Для пустого списка: any — False, all — True."),
    out(f"{P}-aggr-e3", "Что выведет программа? Параметр key.", """
        print(max(["kiwi", "banana", "fig"], key=len))
        print(min([-5, 3, -1], key=abs))
        print(max(["b", "A", "c"], key=str.lower))
        """),
    cod(f"{P}-aggr-e4", t("""
        Напиши функцию `longest_word(words)` — самое длинное слово списка (при равной длине — первое из них).
        Для пустого списка вернуть пустую строку.

        Примеры:
        ```
        longest_word(["кот", "собака", "ёж"])   # → "собака"
        longest_word(["ab", "cd"])              # → "ab"
        longest_word([])                        # → ""
        ```
        """),
        """
        def longest_word(words):
            pass
        """,
        """
        def test_values():
            got = [longest_word(["кот", "собака", "ёж"]), longest_word(["ab", "cd"]), longest_word([])]
            assert got == ["собака", "ab", ""], f"Получено {got}"
        """,
        """
        def longest_word(words):
            return max(words, key=len, default="")
        """,
        hint="`max(words, key=len, default=\"\")`"),
    cod(f"{P}-aggr-e5", t("""
        Напиши функцию `closest_to_zero(nums)` — число из списка, ближайшее к нулю (с наименьшим модулем).

        Примеры:
        ```
        closest_to_zero([-5, 3, -1, 8])   # → -1
        closest_to_zero([7])              # → 7
        ```
        """),
        """
        def closest_to_zero(nums):
            pass
        """,
        """
        def test_values():
            assert closest_to_zero([-5, 3, -1, 8]) == -1 and closest_to_zero([7]) == 7, f"Получено {closest_to_zero([-5, 3, -1, 8])!r}"
        """,
        """
        def closest_to_zero(nums):
            return min(nums, key=abs)
        """),
    cod(f"{P}-aggr-e6", t("""
        Напиши функцию `all_passed(results)` — все ли результаты равны `"pass"`. Для пустого списка — `True`.
        Используй `all`.

        Примеры:
        ```
        all_passed(["pass", "pass"])   # → True
        all_passed(["pass", "fail"])   # → False
        ```
        """),
        """
        def all_passed(results):
            pass
        """,
        """
        def test_values():
            got = [all_passed(["pass", "pass"]), all_passed(["pass", "fail"]), all_passed([])]
            assert got == [True, False, True], f"Получено {got}"

        def test_all():
            src = open("solution.py", encoding="utf-8").read()
            assert "all(" in src, "Используй all"
        """,
        """
        def all_passed(results):
            return all(r == "pass" for r in results)
        """),
    cod(f"{P}-aggr-e7", t("""
        Напиши функцию `has_negative(nums)` — есть ли в списке хотя бы одно отрицательное число. Используй `any`.

        Примеры:
        ```
        has_negative([1, -2, 3])   # → True
        has_negative([1, 2])       # → False
        ```
        """),
        """
        def has_negative(nums):
            pass
        """,
        """
        def test_values():
            got = [has_negative([1, -2, 3]), has_negative([1, 2]), has_negative([])]
            assert got == [True, False, False], f"Получено {got}"

        def test_any():
            src = open("solution.py", encoding="utf-8").read()
            assert "any(" in src, "Используй any"
        """,
        """
        def has_negative(nums):
            return any(n < 0 for n in nums)
        """),
    cod(f"{P}-aggr-e8", t("""
        Напиши функцию `spread(nums)` — разница между наибольшим и наименьшим числом списка. Для пустого списка — `0`.

        Примеры:
        ```
        spread([3, 9, 1])   # → 8
        spread([5])         # → 0
        spread([])          # → 0
        ```
        """),
        """
        def spread(nums):
            pass
        """,
        """
        def test_values():
            got = [spread([3, 9, 1]), spread([5]), spread([]), spread([-2, 2])]
            assert got == [8, 0, 0, 4], f"Получено {got}"
        """,
        """
        def spread(nums):
            if not nums:
                return 0
            return max(nums) - min(nums)
        """)),
)
