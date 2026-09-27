"""Тема «Списки»."""
from ._lib import cod, lesson, module, out, t, topic

P = "lst"

# ============================================================
m1 = module(f"{P}-m1", "Основы списков", "📋", "Создание, добавление и удаление элементов",

lesson(f"{P}-m1-l1", "Создание списка и доступ к элементам", 
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        nums = [10, 20, 30, 40]
        print(nums[0], nums[2], nums[-1])
        print(len(nums))
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа?", """
        items = ["a", "b", "c"]
        items[1] = "B"
        print(items)
        print("b" in items, "B" in items)
        print(list("abc"))
        """),
    cod(f"{P}-m1-l1-e3", t("""
        Напиши функцию `first_last(items)`, которая возвращает **новый список** из первого и последнего элемента.

        Примеры:
        ```
        first_last([1, 2, 3])   # → [1, 3]
        first_last([7])         # → [7, 7]
        ```
        """),
        """
        def first_last(items):
            pass
        """,
        """
        def test_values():
            assert first_last([1, 2, 3]) == [1, 3] and first_last(["a", "b"]) == ["a", "b"] and first_last([7]) == [7, 7], "Неверный результат"
        """,
        """
        def first_last(items):
            return [items[0], items[-1]]
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `replace_first(items, value)`, которая **заменяет первый элемент** списка на `value` и возвращает этот же список.

        Пример:
        ```
        replace_first(["a", "b"], "z")   # → ["z", "b"]
        ```
        """),
        """
        def replace_first(items, value):
            pass
        """,
        """
        def test_replace():
            data = ["a", "b", "c"]
            result = replace_first(data, "z")
            assert result == ["z", "b", "c"], f"Получено {result}"
            assert data == ["z", "b", "c"], "Нужно изменить сам список"
        """,
        """
        def replace_first(items, value):
            items[0] = value
            return items
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `middle(items)`, которая возвращает **средний элемент** списка нечётной длины.

        Индекс середины — `len(items) // 2`.

        Примеры:
        ```
        middle([1, 2, 3])         # → 2
        middle(["a", "b", "c", "d", "e"])   # → "c"
        middle([42])              # → 42
        ```
        """),
        """
        def middle(items):
            pass
        """,
        """
        def test_values():
            assert middle([1, 2, 3]) == 2 and middle(["a", "b", "c", "d", "e"]) == "c" and middle([42]) == 42, "Неверный средний элемент"
        """,
        """
        def middle(items):
            return items[len(items) // 2]
        """)),

lesson(f"{P}-m1-l2", "Добавление элементов", 
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        items = ["b"]
        items.append("c")
        items.insert(0, "a")
        print(items)
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа? append против extend.", """
        a = [1, 2]
        b = [1, 2]
        a.append([3, 4])
        b.extend([3, 4])
        print(a, len(a))
        print(b, len(b))
        """, hint="`append` добавляет весь объект одним элементом."),
    cod(f"{P}-m1-l2-e3", t("""
        Напиши функцию `add_log(log, message)`, которая добавляет сообщение **в конец** списка `log` и возвращает сам список.

        Пример:
        ```
        add_log(["старт"], "шаг 1")   # → ["старт", "шаг 1"]
        ```
        """),
        """
        def add_log(log, message):
            pass
        """,
        """
        def test_add():
            log = ["старт"]
            assert add_log(log, "шаг 1") == ["старт", "шаг 1"] and log == ["старт", "шаг 1"], "Сообщение должно добавиться в конец этого же списка"
        """,
        """
        def add_log(log, message):
            log.append(message)
            return log
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `build_range(n)`, которая строит список чисел от 1 до `n` **с помощью цикла и `append`** (без `list(range(...))`).

        Примеры:
        ```
        build_range(4)   # → [1, 2, 3, 4]
        build_range(0)   # → []
        ```
        """),
        """
        def build_range(n):
            result = []
            return result
        """,
        """
        def test_values():
            assert build_range(4) == [1, 2, 3, 4] and build_range(0) == [] and build_range(1) == [1], "Неверный список"

        def test_append():
            assert ".append(" in open("solution.py", encoding="utf-8").read(), "Используй append"
        """,
        """
        def build_range(n):
            result = []
            for i in range(1, n + 1):
                result.append(i)
            return result
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `merge_suites(smoke, regress)`, которая возвращает **новый** список: сначала все тесты `smoke`, потом все `regress`.

        Исходные списки **не должны измениться**.

        Пример:
        ```
        merge_suites(["login"], ["pay", "cart"])   # → ["login", "pay", "cart"]
        ```
        """),
        """
        def merge_suites(smoke, regress):
            pass
        """,
        """
        def test_merge():
            a, b = ["login"], ["pay", "cart"]
            assert merge_suites(a, b) == ["login", "pay", "cart"], "Неверный порядок"
            assert a == ["login"] and b == ["pay", "cart"], "Исходные списки изменились — нужен новый список"
        """,
        """
        def merge_suites(smoke, regress):
            return smoke + regress
        """)),

lesson(f"{P}-m1-l3", "Удаление элементов", 
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        items = ["a", "b", "c", "b"]
        items.remove("b")
        print(items)
        last = items.pop()
        print(last, items)
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа?", """
        nums = [10, 20, 30, 40]
        del nums[1]
        first = nums.pop(0)
        print(first, nums)
        nums.clear()
        print(nums, len(nums))
        """),
    cod(f"{P}-m1-l3-e3", t("""
        Напиши функцию `safe_remove(items, value)`, которая удаляет **первое** вхождение `value`, если оно есть, и возвращает `True`. Если значения нет — ничего не делает и возвращает `False` (без ошибки).

        Примеры:
        ```
        data = ["a", "b"]
        safe_remove(data, "a")   # → True,  data == ["b"]
        safe_remove(data, "z")   # → False, data не изменилась
        ```
        """),
        """
        def safe_remove(items, value):
            pass
        """,
        """
        def test_remove():
            data = ["a", "b", "a"]
            assert safe_remove(data, "a") is True and data == ["b", "a"], "Удалить нужно только первое вхождение"

        def test_missing():
            data = ["a"]
            assert safe_remove(data, "z") is False and data == ["a"], "Без значения — False и никаких изменений"
        """,
        """
        def safe_remove(items, value):
            if value in items:
                items.remove(value)
                return True
            return False
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `remove_all(items, value)`, которая удаляет **все** вхождения `value` из списка (изменяет сам список) и возвращает, **сколько** элементов удалено.

        Пример:
        ```
        data = [1, 2, 1, 3, 1]
        remove_all(data, 1)   # → 3, data == [2, 3]
        ```
        """),
        """
        def remove_all(items, value):
            pass
        """,
        """
        def test_remove_all():
            data = [1, 2, 1, 3, 1]
            assert remove_all(data, 1) == 3, "Удалено должно быть 3 элемента"
            assert data == [2, 3], f"В списке осталось {data}"

        def test_nothing():
            data = [5]
            assert remove_all(data, 9) == 0 and data == [5], "Нечего удалять — 0"
        """,
        """
        def remove_all(items, value):
            count = 0
            while value in items:
                items.remove(value)
                count += 1
            return count
        """,
        hint="Цикл `while value in items:` + `remove` + счётчик.", xp=20),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `process_queue(queue)`, которая обрабатывает очередь задач **с начала**: пока очередь не пуста, извлекает первый элемент (`pop(0)`) и добавляет строку `"done: <задача>"` в список результатов. Вернуть список результатов.

        После работы исходная очередь должна стать пустой.

        Пример:
        ```
        q = ["build", "test"]
        process_queue(q)   # → ["done: build", "done: test"],  q == []
        ```
        """),
        """
        def process_queue(queue):
            results = []
            return results
        """,
        """
        def test_queue():
            q = ["build", "test", "deploy"]
            assert process_queue(q) == ["done: build", "done: test", "done: deploy"], "Неверный порядок обработки"
            assert q == [], "Очередь должна опустеть"
        """,
        """
        def process_queue(queue):
            results = []
            while queue:
                task = queue.pop(0)
                results.append(f"done: {task}")
            return results
        """)),
)

# ============================================================
m2 = module(f"{P}-m2", "Работа со списками", "🔧", "Поиск, перебор и сортировка",

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
        """, xp=20)),

lesson(f"{P}-m2-l2", "Перебор: for, enumerate, zip", 
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
        """)),

lesson(f"{P}-m2-l3", "Сортировка", 
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        a = [3, 1, 2]
        b = sorted(a)
        print(a, b)
        a.sort(reverse=True)
        print(a)
        """),
    out(f"{P}-m2-l3-e2", "Что выведет программа? Сортировка строк.", """
        words = ["banana", "Apple", "cherry"]
        print(sorted(words))
        print(sorted(words, key=str.lower))
        print(sorted(words, key=len))
        """, hint="Заглавные буквы идут раньше строчных."),
    cod(f"{P}-m2-l3-e3", t("""
        Напиши функцию `top3(scores)` — три наибольших числа из списка, **по убыванию**. Исходный список не менять.

        Примеры:
        ```
        top3([5, 1, 9, 7, 3])   # → [9, 7, 5]
        top3([2, 1])            # → [2, 1]
        ```
        """),
        """
        def top3(scores):
            pass
        """,
        """
        def test_values():
            data = [5, 1, 9, 7, 3]
            assert top3(data) == [9, 7, 5] and top3([2, 1]) == [2, 1], "Неверный топ"
            assert data == [5, 1, 9, 7, 3], "Исходный список не должен меняться — используй sorted"
        """,
        """
        def top3(scores):
            return sorted(scores, reverse=True)[:3]
        """),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `sort_names(names)` — отсортировать имена по алфавиту **без учёта регистра** и вернуть новый список.

        Пример:
        ```
        sort_names(["боря", "Аня", "вика"])   # → ["Аня", "боря", "вика"]
        ```
        """),
        """
        def sort_names(names):
            pass
        """,
        """
        def test_values():
            assert sort_names(["боря", "Аня", "вика"]) == ["Аня", "боря", "вика"], f"Получено {sort_names(['боря', 'Аня', 'вика'])}"
            assert sort_names(["b", "A", "c"]) == ["A", "b", "c"], "Регистр не должен влиять на порядок"
        """,
        """
        def sort_names(names):
            return sorted(names, key=str.lower)
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `by_duration(tests)`, где `tests` — список пар `(имя, секунды)`. Вернуть список **имён**, отсортированных от самого долгого теста к самому быстрому.

        Пример:
        ```
        by_duration([("login", 1.2), ("pay", 3.4), ("search", 0.2)])   # → ["pay", "login", "search"]
        ```
        Ключ сортировки — второй элемент пары: `key=lambda t: t[1]`.
        """),
        """
        def by_duration(tests):
            pass
        """,
        """
        def test_values():
            got = by_duration([("login", 1.2), ("pay", 3.4), ("search", 0.2)])
            assert got == ["pay", "login", "search"], f"Получено {got}"
        """,
        """
        def by_duration(tests):
            ordered = sorted(tests, key=lambda t: t[1], reverse=True)
            return [name for name, _ in ordered]
        """, xp=20)),
)

# ============================================================
m3 = module(f"{P}-m3", "Продвинутые приёмы", "🧱", "Накопление, копирование и вложенные списки",

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
        """)),

lesson(f"{P}-m3-l2", "Копирование и ссылки", 
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        a = [1, 2]
        b = a
        c = a.copy()
        b.append(3)
        print(a, b, c)
        print(a is b, a is c)
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа? Мелкая копия вложенного списка.", """
        a = [[1], [2]]
        b = a.copy()
        b[0].append(99)
        print(a)
        """, hint="`copy()` копирует только внешний список; вложенные списки общие."),
    cod(f"{P}-m3-l2-e3", t("""
        Напиши функцию `with_item(items, value)`, которая возвращает **новый** список — копию `items` с добавленным в конец `value`. Исходный список не должен измениться.

        Пример:
        ```
        a = [1, 2]
        with_item(a, 3)   # → [1, 2, 3], а a по-прежнему [1, 2]
        ```
        """),
        """
        def with_item(items, value):
            items.append(value)
            return items
        """,
        """
        def test_new_list():
            a = [1, 2]
            b = with_item(a, 3)
            assert b == [1, 2, 3], "В результате должен быть новый элемент"
            assert a == [1, 2], "Исходный список изменился — нужно работать с копией"
            assert a is not b, "Нужен новый список"
        """,
        """
        def with_item(items, value):
            result = items.copy()
            result.append(value)
            return result
        """),
    cod(f"{P}-m3-l2-e4", t("""
        В функции `reset_scores` баг: она должна вернуть **новый** список той же длины, заполненный нулями, но портит исходные данные.

        Исправь её так, чтобы исходный список не менялся.

        Пример:
        ```
        scores = [5, 3, 8]
        reset_scores(scores)   # → [0, 0, 0], а scores == [5, 3, 8]
        ```
        """),
        """
        def reset_scores(scores):
            result = scores
            for i in range(len(result)):
                result[i] = 0
            return result
        """,
        """
        def test_reset():
            scores = [5, 3, 8]
            assert reset_scores(scores) == [0, 0, 0], "Нужен список нулей"
            assert scores == [5, 3, 8], "Исходный список испорчен"
        """,
        """
        def reset_scores(scores):
            return [0] * len(scores)
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `clone_matrix(matrix)`, которая возвращает **полную (глубокую) копию** списка списков: изменения во вложенных списках копии не должны влиять на оригинал.

        Используй `copy.deepcopy` (не забудь `import copy`).

        Пример:
        ```
        m = [[1, 2], [3, 4]]
        c = clone_matrix(m)
        c[0][0] = 99    # m остаётся [[1, 2], [3, 4]]
        ```
        """),
        """
        def clone_matrix(matrix):
            return matrix.copy()
        """,
        """
        def test_deep():
            m = [[1, 2], [3, 4]]
            c = clone_matrix(m)
            c[0][0] = 99
            assert m == [[1, 2], [3, 4]], "Оригинал изменился — копия должна быть глубокой"
            assert c == [[99, 2], [3, 4]], "Копия должна содержать те же данные"
        """,
        """
        import copy

        def clone_matrix(matrix):
            return copy.deepcopy(matrix)
        """)),

lesson(f"{P}-m3-l3", "Вложенные списки", 
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        m = [[1, 2, 3], [4, 5, 6]]
        print(m[0][1], m[1][0], m[-1][-1])
        print(len(m), len(m[0]))
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа?", """
        table = [["login", "pass"], ["pay", "fail"]]
        for name, status in table:
            print(name, "->", status)
        """),
    cod(f"{P}-m3-l3-e3", t("""
        Напиши функцию `matrix_sum(matrix)` — сумма **всех** чисел в списке списков.

        Пример:
        ```
        matrix_sum([[1, 2], [3, 4]])   # → 10
        matrix_sum([[], [5]])          # → 5
        ```
        """),
        """
        def matrix_sum(matrix):
            pass
        """,
        """
        def test_values():
            assert matrix_sum([[1, 2], [3, 4]]) == 10 and matrix_sum([[], [5]]) == 5 and matrix_sum([]) == 0, "Неверная сумма"
        """,
        """
        def matrix_sum(matrix):
            total = 0
            for row in matrix:
                for value in row:
                    total += value
            return total
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `column(matrix, index)` — список значений из столбца с номером `index`.

        Пример:
        ```
        column([[1, 2, 3], [4, 5, 6]], 1)   # → [2, 5]
        ```
        """),
        """
        def column(matrix, index):
            pass
        """,
        """
        def test_values():
            m = [[1, 2, 3], [4, 5, 6]]
            assert column(m, 1) == [2, 5] and column(m, 0) == [1, 4] and column(m, -1) == [3, 6], "Неверный столбец"
        """,
        """
        def column(matrix, index):
            return [row[index] for row in matrix]
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `flatten(nested)` — превратить список списков в один плоский список.

        Пример:
        ```
        flatten([[1, 2], [], [3], [4, 5]])   # → [1, 2, 3, 4, 5]
        ```
        """),
        """
        def flatten(nested):
            pass
        """,
        """
        def test_values():
            assert flatten([[1, 2], [], [3], [4, 5]]) == [1, 2, 3, 4, 5] and flatten([]) == [], "Неверный результат"
        """,
        """
        def flatten(nested):
            result = []
            for inner in nested:
                result.extend(inner)
            return result
        """)),
)

TOPIC = topic("py-lists", "Списки", "📋", "#1cb0f6",
              "Создание, изменение, поиск, перебор, сортировка и копирование списков",
              m1, m2, m3, group="Python")
