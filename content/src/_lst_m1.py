"""Тема «Списки», модуль 1 «Основы списков» — задания. Теория — в _lst_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "lst"

m1 = module(f"{P}-m1", "Основы списков", "📋", "Создание, индексы, добавление, удаление, распаковка и сравнение",

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
    out(f"{P}-m1-l1-e6", "Что выведет программа? Отрицательные индексы и замена.", """
        nums = [10, 20, 30]
        nums[-1] = 99
        print(nums)
        print(nums[-3], len([]))
        """, hint="`-1` — последний элемент, `-3` в списке из трёх — первый."),
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
        """),
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `swap_ends(items)`, которая **меняет местами** первый и последний элементы списка (сам список)
        и возвращает его.

        Примеры:
        ```
        swap_ends([1, 2, 3])        # → [3, 2, 1]
        swap_ends(["a", "b"])       # → ["b", "a"]
        swap_ends([7])              # → [7]
        ```
        """),
        """
        def swap_ends(items):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3]
            assert swap_ends(data) == [3, 2, 1] and data == [3, 2, 1], "Нужно изменить сам список"
            assert swap_ends(["a", "b"]) == ["b", "a"] and swap_ends([7]) == [7], "Неверный обмен"
        """,
        """
        def swap_ends(items):
            items[0], items[-1] = items[-1], items[0]
            return items
        """,
        hint="Как обмен переменных: `items[0], items[-1] = items[-1], items[0]`."),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `second(items)` — второй элемент списка или `None`, если элементов меньше двух.

        Примеры:
        ```
        second([5, 6, 7])   # → 6
        second([5])         # → None
        second([])          # → None
        ```
        """),
        """
        def second(items):
            pass
        """,
        """
        def test_values():
            got = [second([5, 6, 7]), second([5]), second([]), second(["a", "b"])]
            assert got == [6, None, None, "b"], f"Получено {got}"
        """,
        """
        def second(items):
            if len(items) < 2:
                return None
            return items[1]
        """,
        hint="Сначала проверь длину, иначе `items[1]` даст IndexError.")),

lesson(f"{P}-create", "Как ещё создать список",
    out(f"{P}-create-e1", "Что выведет программа? Списки из range.", """
        print(list(range(5)))
        print(list(range(2, 7)))
        print(list(range(0, 10, 3)))
        print(list(range(5, 0, -1)))
        """, hint="`range(старт, стоп, шаг)`: стоп НЕ входит."),
    out(f"{P}-create-e2", "Что выведет программа? Повторение и склейка.", """
        print([0] * 3)
        print(["a", "b"] * 2)
        print([1] + [2, 3])
        print(list("hi!"))
        """),
    out(f"{P}-create-e3", "Что выведет программа? Строка ↔ список.", """
        words = "раз два  три".split()
        print(words, len(words))
        print("-".join(words))
        print("a,b,,c".split(","))
        """),
    cod(f"{P}-create-e4", t("""
        Напиши функцию `countdown(n)` — список чисел от `n` до 1 **по убыванию** с помощью `range`.

        Примеры:
        ```
        countdown(3)   # → [3, 2, 1]
        countdown(1)   # → [1]
        countdown(0)   # → []
        ```
        """),
        """
        def countdown(n):
            pass
        """,
        """
        def test_values():
            got = [countdown(3), countdown(1), countdown(0)]
            assert got == [[3, 2, 1], [1], []], f"Получено {got}"
        """,
        """
        def countdown(n):
            return list(range(n, 0, -1))
        """,
        hint="Шаг `-1`, а стоп — 0 (он не входит)."),
    cod(f"{P}-create-e5", t("""
        Напиши функцию `zeros(n)` — список из `n` нулей.

        Примеры:
        ```
        zeros(3)   # → [0, 0, 0]
        zeros(0)   # → []
        ```
        """),
        """
        def zeros(n):
            pass
        """,
        """
        def test_values():
            assert zeros(3) == [0, 0, 0] and zeros(0) == [] and len(zeros(10)) == 10, "Неверный список"
        """,
        """
        def zeros(n):
            return [0] * n
        """),
    cod(f"{P}-create-e6", t("""
        Напиши функцию `even_numbers(limit)` — список **чётных** чисел от 0 до `limit` **включительно**, через `range` с шагом.

        Примеры:
        ```
        even_numbers(6)   # → [0, 2, 4, 6]
        even_numbers(5)   # → [0, 2, 4]
        ```
        """),
        """
        def even_numbers(limit):
            pass
        """,
        """
        def test_values():
            got = [even_numbers(6), even_numbers(5), even_numbers(0)]
            assert got == [[0, 2, 4, 6], [0, 2, 4], [0]], f"Получено {got}"
        """,
        """
        def even_numbers(limit):
            return list(range(0, limit + 1, 2))
        """,
        hint="Стоп в `range` не входит — поэтому `limit + 1`."),
    cod(f"{P}-create-e7", t("""
        Напиши функцию `words_of(text)` — список слов текста (слова разделены одним или несколькими пробелами).

        Примеры:
        ```
        words_of("  много   пробелов ")   # → ["много", "пробелов"]
        words_of("")                      # → []
        ```
        """),
        """
        def words_of(text):
            pass
        """,
        """
        def test_values():
            assert words_of("  много   пробелов ") == ["много", "пробелов"] and words_of("") == [], "Неверное разбиение"
        """,
        """
        def words_of(text):
            return text.split()
        """),
    cod(f"{P}-create-e8", t("""
        Напиши функцию `chars(word)` — список символов слова.

        Примеры:
        ```
        chars("кот")   # → ["к", "о", "т"]
        chars("")      # → []
        ```
        """),
        """
        def chars(word):
            pass
        """,
        """
        def test_values():
            assert chars("кот") == ["к", "о", "т"] and chars("") == [] and chars("a b") == ["a", " ", "b"], "Неверный список"
        """,
        """
        def chars(word):
            return list(word)
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
    out(f"{P}-m1-l2-e6", "Что выведет программа? `+=` и `insert` с необычным индексом.", """
        a = [1]
        a += [2, 3]
        a.insert(100, "x")
        a.insert(-1, "y")
        print(a)
        """, hint="`insert` за пределами списка вставляет в конец; `insert(-1, …)` — перед последним."),
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
        """),
    cod(f"{P}-m1-l2-e7", t("""
        Напиши функцию `add_unique(items, value)`: добавить `value` в конец списка, **только если** его там ещё нет.
        Вернуть сам список.

        Примеры:
        ```
        add_unique(["a"], "b")   # → ["a", "b"]
        add_unique(["a"], "a")   # → ["a"]
        ```
        """),
        """
        def add_unique(items, value):
            pass
        """,
        """
        def test_values():
            data = ["a"]
            assert add_unique(data, "b") == ["a", "b"] and data == ["a", "b"], "Добавь в сам список"
            assert add_unique(data, "a") == ["a", "b"], "Повтор не добавляется"
        """,
        """
        def add_unique(items, value):
            if value not in items:
                items.append(value)
            return items
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши функцию `prepend(items, value)` — вставить `value` **в начало** списка и вернуть сам список.

        Пример:
        ```
        prepend([2, 3], 1)   # → [1, 2, 3]
        ```
        """),
        """
        def prepend(items, value):
            pass
        """,
        """
        def test_values():
            data = [2, 3]
            assert prepend(data, 1) == [1, 2, 3] and data == [1, 2, 3], "Вставь в начало самого списка"
            assert prepend([], "x") == ["x"], "В пустой список тоже"
        """,
        """
        def prepend(items, value):
            items.insert(0, value)
            return items
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
    out(f"{P}-m1-l3-e6", "Что выведет программа? Удаление куска и pop с отрицательным индексом.", """
        items = [1, 2, 3, 4, 5]
        del items[1:3]
        print(items)
        x = items.pop(-2)
        print(x, items)
        """, hint="`del items[1:3]` удаляет элементы с индексами 1 и 2."),
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
        """),
    cod(f"{P}-m1-l3-e7", t("""
        Напиши функцию `remove_last(items)`: удалить из списка последний элемент и **вернуть его**.
        Для пустого списка вернуть `None` без ошибки.

        Примеры:
        ```
        data = [1, 2, 3]
        remove_last(data)   # → 3, data == [1, 2]
        remove_last([])     # → None
        ```
        """),
        """
        def remove_last(items):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3]
            assert remove_last(data) == 3 and data == [1, 2], f"Получено data={data}"
            assert remove_last([]) is None, "Для пустого списка — None"
        """,
        """
        def remove_last(items):
            if not items:
                return None
            return items.pop()
        """),
    cod(f"{P}-m1-l3-e8", t("""
        Напиши функцию `drop_at(items, index)`: удалить элемент с индексом `index` через `del` и вернуть сам список.

        Примеры:
        ```
        drop_at(["a", "b", "c"], 1)    # → ["a", "c"]
        drop_at(["a", "b", "c"], -1)   # → ["a", "b"]
        ```
        """),
        """
        def drop_at(items, index):
            pass
        """,
        """
        def test_values():
            assert drop_at(["a", "b", "c"], 1) == ["a", "c"] and drop_at(["a", "b", "c"], -1) == ["a", "b"], "Неверное удаление"

        def test_del():
            src = open("solution.py", encoding="utf-8").read()
            assert "del " in src, "Используй del"
        """,
        """
        def drop_at(items, index):
            del items[index]
            return items
        """)),

lesson(f"{P}-unpack", "Распаковка и сравнение списков",
    out(f"{P}-unpack-e1", "Что выведет программа? Распаковка.", """
        a, b, c = [1, 2, 3]
        first, *rest = [10, 20, 30]
        *start, last = "abc"
        print(a, c, first, rest)
        print(start, last)
        """, hint="Переменная со звёздочкой собирает «всё остальное» в список."),
    out(f"{P}-unpack-e2", "Что выведет программа? Сравнение списков.", """
        print([1, 2] == [1, 2], [1, 2] == [2, 1])
        print([1, 2] < [1, 3], [2] > [1, 99])
        print([1, 2] < [1, 2, 0])
        """, hint="Списки сравниваются поэлементно, как слова по буквам."),
    out(f"{P}-unpack-e3", "Что выведет программа? == и is.", """
        x = [1, 2]
        y = [1, 2]
        z = x
        print(x == y, x is y)
        print(x == z, x is z)
        """),
    cod(f"{P}-unpack-e4", t("""
        Напиши функцию `head_tail(items)` — вернуть **пару**: первый элемент и список остальных. Используй распаковку со звёздочкой.

        Примеры:
        ```
        head_tail([1, 2, 3])   # → (1, [2, 3])
        head_tail(["x"])       # → ("x", [])
        ```
        """),
        """
        def head_tail(items):
            pass
        """,
        """
        def test_values():
            assert head_tail([1, 2, 3]) == (1, [2, 3]) and head_tail(["x"]) == ("x", []), f"Получено {head_tail([1, 2, 3])!r}"

        def test_star():
            src = open("solution.py", encoding="utf-8").read()
            assert "*" in src, "Используй распаковку со звёздочкой"
        """,
        """
        def head_tail(items):
            first, *rest = items
            return first, rest
        """),
    cod(f"{P}-unpack-e5", t("""
        Напиши функцию `last_name_first(full_name)`: строка из имени и фамилии через пробел → «Фамилия Имя».
        Разбей строку на две части и распакуй их в две переменные.

        Пример:
        ```
        last_name_first("Анна Петрова")   # → "Петрова Анна"
        ```
        """),
        """
        def last_name_first(full_name):
            pass
        """,
        """
        def test_values():
            assert last_name_first("Анна Петрова") == "Петрова Анна", f"Получено {last_name_first('Анна Петрова')!r}"
        """,
        """
        def last_name_first(full_name):
            first, last = full_name.split()
            return last + " " + first
        """),
    cod(f"{P}-unpack-e6", t("""
        Напиши функцию `last_and_rest(items)` — пара: **последний** элемент и список всех остальных.

        Примеры:
        ```
        last_and_rest([1, 2, 3])   # → (3, [1, 2])
        last_and_rest([9])         # → (9, [])
        ```
        """),
        """
        def last_and_rest(items):
            pass
        """,
        """
        def test_values():
            assert last_and_rest([1, 2, 3]) == (3, [1, 2]) and last_and_rest([9]) == (9, []), f"Получено {last_and_rest([1, 2, 3])!r}"
        """,
        """
        def last_and_rest(items):
            *rest, last = items
            return last, rest
        """),
    cod(f"{P}-unpack-e7", t("""
        Напиши функцию `point_sum(point)` — сумма координат точки `[x, y]`. Разложи список в две переменные.

        Примеры:
        ```
        point_sum([3, 4])    # → 7
        point_sum([-1, 1])   # → 0
        ```
        """),
        """
        def point_sum(point):
            pass
        """,
        """
        def test_values():
            assert point_sum([3, 4]) == 7 and point_sum([-1, 1]) == 0, "Неверная сумма"
        """,
        """
        def point_sum(point):
            x, y = point
            return x + y
        """),
    cod(f"{P}-unpack-e8", t("""
        Напиши функцию `same_order(a, b)` — одинаковые ли два списка: те же элементы **в том же порядке**.

        Примеры:
        ```
        same_order([1, 2], [1, 2])   # → True
        same_order([1, 2], [2, 1])   # → False
        same_order([], [])           # → True
        ```
        """),
        """
        def same_order(a, b):
            pass
        """,
        """
        def test_values():
            got = [same_order([1, 2], [1, 2]), same_order([1, 2], [2, 1]), same_order([], []), same_order([1], [1, 1])]
            assert got == [True, False, True, False], f"Получено {got}"
        """,
        """
        def same_order(a, b):
            return a == b
        """)),
)
