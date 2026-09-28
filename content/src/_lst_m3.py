"""Тема «Списки», модули 3 «Сортировка» и 4 «Ссылки, функции и вложенность» — задания.
Теория — в _lst_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "lst"

m3 = module(f"{P}-sort", "Сортировка", "🔢", "sort и sorted, reverse, ключ сортировки, стабильность",

lesson(f"{P}-m2-l3", "Сортировка: sort и sorted",
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
    out(f"{P}-m2-l3-e6", "Что выведет программа? Что возвращает sort.", """
        nums = [3, 1, 2]
        r = nums.sort()
        print(r, nums)
        print(sorted("cab"))
        print(sorted([3, 1, 2], reverse=True))
        """, hint="`sort` меняет список на месте и возвращает None; `sorted` принимает любую коллекцию и возвращает список."),
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
    cod(f"{P}-m2-l3-e7", t("""
        Напиши функцию `sort_desc(nums)`, которая сортирует **сам список** по убыванию и возвращает его.

        Пример:
        ```
        data = [2, 9, 4]
        sort_desc(data)   # → [9, 4, 2], и data тоже [9, 4, 2]
        ```
        """),
        """
        def sort_desc(nums):
            pass
        """,
        """
        def test_values():
            data = [2, 9, 4]
            result = sort_desc(data)
            assert data == [9, 4, 2] and result is data, f"Нужно отсортировать сам список, сейчас data={data}"
        """,
        """
        def sort_desc(nums):
            nums.sort(reverse=True)
            return nums
        """,
        hint="`nums.sort(reverse=True)`, затем `return nums` — сам `sort` вернёт None."),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `median(nums)` — медиана списка нечётной длины: средний элемент **отсортированного** списка.
        Исходный список не менять.

        Примеры:
        ```
        median([3, 1, 2])         # → 2
        median([9, 1, 5, 7, 3])   # → 5
        ```
        """),
        """
        def median(nums):
            pass
        """,
        """
        def test_values():
            data = [9, 1, 5, 7, 3]
            assert median([3, 1, 2]) == 2 and median(data) == 5 and median([4]) == 4, "Неверная медиана"
            assert data == [9, 1, 5, 7, 3], "Исходный список не должен меняться"
        """,
        """
        def median(nums):
            ordered = sorted(nums)
            return ordered[len(ordered) // 2]
        """),
    cod(f"{P}-m2-l3-e9", t("""
        Напиши функцию `is_sorted(nums)` — отсортирован ли список по возрастанию.

        Примеры:
        ```
        is_sorted([1, 2, 2, 5])   # → True
        is_sorted([3, 1])         # → False
        is_sorted([])             # → True
        ```
        Подсказка: сравни список с его отсортированной копией.
        """),
        """
        def is_sorted(nums):
            pass
        """,
        """
        def test_values():
            got = [is_sorted([1, 2, 2, 5]), is_sorted([3, 1]), is_sorted([]), is_sorted([1])]
            assert got == [True, False, True, True], f"Получено {got}"
        """,
        """
        def is_sorted(nums):
            return nums == sorted(nums)
        """)),

lesson(f"{P}-key", "Сортировка по ключу и обратный порядок",
    out(f"{P}-key-e1", "Что выведет программа? Встроенные функции как ключ.", """
        print(sorted([-3, 2, -1], key=abs))
        print(sorted(["bb", "a", "ccc"], key=len, reverse=True))
        """),
    out(f"{P}-key-e2", "Что выведет программа? lambda и несколько критериев.", """
        pairs = [("b", 2), ("a", 2), ("c", 1)]
        print(sorted(pairs, key=lambda p: p[1]))
        print(sorted(pairs, key=lambda p: (p[1], p[0])))
        print(sorted(pairs))
        """, hint="Сортировка стабильна; кортеж-ключ сравнивается поэлементно."),
    out(f"{P}-key-e3", "Что выведет программа? reverse и reversed.", """
        items = [1, 2, 3]
        items.reverse()
        print(items)
        print(list(reversed(items)))
        print(items)
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
        """, xp=20),
    cod(f"{P}-key-e4", t("""
        Напиши функцию `by_last_letter(words)` — новый список слов, отсортированных по **последней букве**.

        Пример:
        ```
        by_last_letter(["кот", "сова", "лис"])   # → ["сова", "лис", "кот"]
        ```
        """),
        """
        def by_last_letter(words):
            pass
        """,
        """
        def test_values():
            assert by_last_letter(["кот", "сова", "лис"]) == ["сова", "лис", "кот"], f"Получено {by_last_letter(['кот', 'сова', 'лис'])}"
        """,
        """
        def by_last_letter(words):
            return sorted(words, key=lambda w: w[-1])
        """,
        hint="`key=lambda w: w[-1]`"),
    cod(f"{P}-key-e5", t("""
        Напиши функцию `by_length_then_alpha(words)` — отсортировать слова по длине, а слова одинаковой длины —
        по алфавиту **без учёта регистра**.

        Пример:
        ```
        by_length_then_alpha(["bb", "Ab", "c", "aa"])   # → ["c", "aa", "Ab", "bb"]
        ```
        Ключ — кортеж из двух значений.
        """),
        """
        def by_length_then_alpha(words):
            pass
        """,
        """
        def test_values():
            assert by_length_then_alpha(["bb", "Ab", "c", "aa"]) == ["c", "aa", "Ab", "bb"], f"Получено {by_length_then_alpha(['bb', 'Ab', 'c', 'aa'])}"
        """,
        """
        def by_length_then_alpha(words):
            return sorted(words, key=lambda w: (len(w), w.lower()))
        """),
    cod(f"{P}-key-e6", t("""
        Напиши функцию `leaderboard(players)`. `players` — список пар `(имя, очки)`.
        Вернуть список **имён**: по убыванию очков, а при равных очках — по алфавиту.

        Пример:
        ```
        leaderboard([("Боря", 50), ("Аня", 80), ("Вика", 50)])   # → ["Аня", "Боря", "Вика"]
        ```
        Подсказка: по убыванию очков и по возрастанию имени одновременно — ключ `(-очки, имя)`.
        """),
        """
        def leaderboard(players):
            pass
        """,
        """
        def test_values():
            got = leaderboard([("Вика", 50), ("Аня", 80), ("Боря", 50), ("Гоша", 10)])
            assert got == ["Аня", "Боря", "Вика", "Гоша"], f"Получено {got}"
        """,
        """
        def leaderboard(players):
            ordered = sorted(players, key=lambda p: (-p[1], p[0]))
            result = []
            for name, score in ordered:
                result.append(name)
            return result
        """, xp=20),
    cod(f"{P}-key-e7", t("""
        Напиши функцию `reverse_in_place(items)` — развернуть **сам список** (без создания нового) и вернуть его.

        Пример:
        ```
        data = [1, 2, 3]
        reverse_in_place(data)   # → [3, 2, 1], и data тоже [3, 2, 1]
        ```
        """),
        """
        def reverse_in_place(items):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3]
            result = reverse_in_place(data)
            assert data == [3, 2, 1] and result is data, f"Нужно развернуть сам список, сейчас data={data}"
        """,
        """
        def reverse_in_place(items):
            items.reverse()
            return items
        """)),
)

m4 = module(f"{P}-m3", "Ссылки, функции и вложенность", "🧬", "Копии и ссылки, списки в функциях, таблицы, стек и очередь",

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
    out(f"{P}-m3-l2-e6", "Что выведет программа? `+=` и `+` ведут себя по-разному.", """
        a = [1, 2]
        b = a
        b += [3]
        c = a + [4]
        print(a, c)
        print(a is b, a is c)
        """, hint="`+=` меняет список на месте, `+` создаёт новый."),
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
        """),
    cod(f"{P}-m3-l2-e7", t("""
        Функция `backup_and_clear(items)` должна вернуть **копию** списка, а сам список очистить.
        Сейчас она возвращает пустой список — копия «пропадает» вместе с очисткой. Исправь.

        Пример:
        ```
        data = [1, 2]
        backup_and_clear(data)   # → [1, 2], а data == []
        ```
        """),
        """
        def backup_and_clear(items):
            backup = items
            items.clear()
            return backup
        """,
        """
        def test_values():
            data = [1, 2]
            got = backup_and_clear(data)
            assert got == [1, 2] and data == [], f"Вернулось {got}, data={data}"
        """,
        """
        def backup_and_clear(items):
            backup = items.copy()
            items.clear()
            return backup
        """,
        hint="`backup = items` — не копия, а второе имя того же списка."),
    cod(f"{P}-m3-l2-e8", t("""
        Напиши функцию `make_grid(rows, cols)` — таблица `rows × cols` из нулей, где строки **независимы**:
        изменение одной строки не меняет другие.

        Пример:
        ```
        g = make_grid(2, 3)   # → [[0, 0, 0], [0, 0, 0]]
        g[0][0] = 1           # g == [[1, 0, 0], [0, 0, 0]]
        ```
        """),
        """
        def make_grid(rows, cols):
            pass
        """,
        """
        def test_shape():
            assert make_grid(2, 3) == [[0, 0, 0], [0, 0, 0]] and make_grid(0, 5) == [], "Неверный размер"

        def test_independent():
            g = make_grid(2, 3)
            g[0][0] = 1
            assert g == [[1, 0, 0], [0, 0, 0]], f"Строки связаны: {g}"
        """,
        """
        def make_grid(rows, cols):
            grid = []
            for _ in range(rows):
                grid.append([0] * cols)
            return grid
        """,
        hint="`[[0] * cols] * rows` создаст одну строку, повторённую несколько раз. Создавай новую строку в цикле.")),

lesson(f"{P}-func", "Списки в функциях",
    out(f"{P}-func-e1", "Что выведет программа? Функция меняет переданный список.", """
        def add_one(items):
            items.append(1)

        a = []
        add_one(a)
        add_one(a)
        print(a)
        """),
    out(f"{P}-func-e2", "Что выведет программа? Присваивание внутри функции.", """
        def reset(items):
            items = []
            items.append("new")

        a = [5]
        reset(a)
        print(a)
        """, hint="`items = []` перевешивает локальное имя на новый список; список снаружи не трогается."),
    out(f"{P}-func-e3", "Что выведет программа? Изменяемое значение по умолчанию.", """
        def collect(x, acc=[]):
            acc.append(x)
            return acc

        print(collect(1))
        print(collect(2))
        print(collect(3, []))
        """, hint="Список по умолчанию создаётся один раз и живёт между вызовами."),
    cod(f"{P}-func-e4", t("""
        Напиши функцию `without_value(items, value)` — **новый** список без всех вхождений `value`.
        Исходный список не менять.

        Пример:
        ```
        data = [1, 2, 1, 3]
        without_value(data, 1)   # → [2, 3], а data == [1, 2, 1, 3]
        ```
        """),
        """
        def without_value(items, value):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 1, 3]
            assert without_value(data, 1) == [2, 3] and data == [1, 2, 1, 3], f"data={data}"
        """,
        """
        def without_value(items, value):
            result = []
            for x in items:
                if x != value:
                    result.append(x)
            return result
        """),
    cod(f"{P}-func-e5", t("""
        В функции `add_tag(tag, tags=[])` классическая ошибка: теги от прошлых вызовов «прилипают» к новым.
        Исправь её так, чтобы вызов без второго аргумента каждый раз начинал с **пустого** списка.

        Пример:
        ```
        add_tag("a")          # → ["a"]
        add_tag("b")          # → ["b"]    а не ["a", "b"]
        add_tag("c", ["x"])   # → ["x", "c"]
        ```
        """),
        """
        def add_tag(tag, tags=[]):
            tags.append(tag)
            return tags
        """,
        """
        def test_values():
            assert add_tag("a") == ["a"], "Первый вызов — ['a']"
            assert add_tag("b") == ["b"], "Второй вызов не должен помнить 'a'"
            assert add_tag("c", ["x"]) == ["x", "c"], "С переданным списком — дописать в него"
        """,
        """
        def add_tag(tag, tags=None):
            if tags is None:
                tags = []
            tags.append(tag)
            return tags
        """,
        hint="Значение по умолчанию — `None`, а новый список создавай внутри функции."),
    cod(f"{P}-func-e6", t("""
        Напиши функцию `normalized(names)` — новый список: каждое имя без пробелов по краям и в нижнем регистре.
        Исходный список не менять.

        Пример:
        ```
        normalized(["  Аня", "БОРЯ "])   # → ["аня", "боря"]
        ```
        """),
        """
        def normalized(names):
            pass
        """,
        """
        def test_values():
            data = ["  Аня", "БОРЯ "]
            assert normalized(data) == ["аня", "боря"] and data == ["  Аня", "БОРЯ "], "Новый список, исходный не меняется"
        """,
        """
        def normalized(names):
            result = []
            for name in names:
                result.append(name.strip().lower())
            return result
        """),
    cod(f"{P}-func-e7", t("""
        Напиши функцию `extend_unique(target, extra)`: дописать в **сам** список `target` элементы из `extra`,
        которых там ещё нет (в порядке `extra`, без повторов). Вернуть `target`.

        Пример:
        ```
        data = [1, 2]
        extend_unique(data, [2, 3, 3, 4])   # → [1, 2, 3, 4], data тоже
        ```
        """),
        """
        def extend_unique(target, extra):
            pass
        """,
        """
        def test_values():
            data = [1, 2]
            result = extend_unique(data, [2, 3, 3, 4])
            assert data == [1, 2, 3, 4] and result is data, f"data={data}"
        """,
        """
        def extend_unique(target, extra):
            for x in extra:
                if x not in target:
                    target.append(x)
            return target
        """),
    cod(f"{P}-func-e8", t("""
        Напиши функцию `sorted_scores(scores)`: вернуть **новый** отсортированный по возрастанию список, не меняя исходный.
        Ловушка: `scores.sort()` изменит исходный список и вернёт `None`.

        Пример:
        ```
        data = [3, 1, 2]
        sorted_scores(data)   # → [1, 2, 3], а data == [3, 1, 2]
        ```
        """),
        """
        def sorted_scores(scores):
            return scores.sort()
        """,
        """
        def test_values():
            data = [3, 1, 2]
            got = sorted_scores(data)
            assert got == [1, 2, 3] and data == [3, 1, 2], f"Вернулось {got!r}, data={data}"
        """,
        """
        def sorted_scores(scores):
            return sorted(scores)
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
    out(f"{P}-m3-l3-e6", "Что выведет программа?", """
        grid = [[1, 2], [3, 4]]
        grid[1][0] = 9
        grid.append([5, 6])
        print(grid)
        print(len(grid), grid[-1][-1])
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
        """),
    cod(f"{P}-m3-l3-e7", t("""
        Напиши функцию `row_sums(matrix)` — список сумм каждой строки таблицы.

        Пример:
        ```
        row_sums([[1, 2], [3, 4], []])   # → [3, 7, 0]
        ```
        """),
        """
        def row_sums(matrix):
            pass
        """,
        """
        def test_values():
            assert row_sums([[1, 2], [3, 4], []]) == [3, 7, 0] and row_sums([]) == [], "Неверные суммы"
        """,
        """
        def row_sums(matrix):
            result = []
            for row in matrix:
                result.append(sum(row))
            return result
        """),
    cod(f"{P}-m3-l3-e8", t("""
        Напиши функцию `transpose(matrix)` — поменять строки и столбцы местами. Результат — список **списков**.

        Пример:
        ```
        transpose([[1, 2, 3], [4, 5, 6]])   # → [[1, 4], [2, 5], [3, 6]]
        ```
        Подсказка: `zip(*matrix)` выдаёт столбцы кортежами; преврати каждый в список.
        """),
        """
        def transpose(matrix):
            pass
        """,
        """
        def test_values():
            assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]], f"Получено {transpose([[1, 2, 3], [4, 5, 6]])}"
        """,
        """
        def transpose(matrix):
            result = []
            for col in zip(*matrix):
                result.append(list(col))
            return result
        """, xp=20)),

lesson(f"{P}-stack", "Стек и очередь",
    out(f"{P}-stack-e1", "Что выведет программа? Стек: последним пришёл — первым ушёл.", """
        stack = []
        stack.append(1)
        stack.append(2)
        stack.append(3)
        print(stack.pop(), stack.pop())
        print(stack, stack[-1])
        """),
    out(f"{P}-stack-e2", "Что выведет программа? Очередь на deque.", """
        from collections import deque
        q = deque([1, 2])
        q.append(3)
        q.appendleft(0)
        print(q.popleft(), list(q))
        """),
    out(f"{P}-stack-e3", "Что выведет программа? Список как очередь.", """
        queue = ["a", "b", "c"]
        first = queue.pop(0)
        queue.append("d")
        print(first, queue)
        """),
    cod(f"{P}-stack-e4", t("""
        Напиши функцию `undo(history)`: удалить из списка действий последнее и вернуть его. Если история пуста — `None`.

        Пример:
        ```
        h = ["ввод", "удаление"]
        undo(h)   # → "удаление", h == ["ввод"]
        undo([])  # → None
        ```
        """),
        """
        def undo(history):
            pass
        """,
        """
        def test_values():
            h = ["ввод", "удаление"]
            assert undo(h) == "удаление" and h == ["ввод"], f"h={h}"
            assert undo([]) is None, "Пустая история — None"
        """,
        """
        def undo(history):
            if not history:
                return None
            return history.pop()
        """),
    cod(f"{P}-stack-e5", t("""
        Напиши функцию `is_balanced(text)` — правильно ли расставлены **круглые** скобки: каждая `(` закрыта своей `)`
        и никакая `)` не встречается раньше парной `(`. Используй список как стек.

        Примеры:
        ```
        is_balanced("(a(b)c)")   # → True
        is_balanced("(()")       # → False
        is_balanced(")(")        # → False
        is_balanced("")          # → True
        ```
        """),
        """
        def is_balanced(text):
            pass
        """,
        """
        def test_values():
            got = [is_balanced(s) for s in ("(a(b)c)", "(()", ")(", "", "()()", "(()))")]
            assert got == [True, False, False, True, True, False], f"Получено {got}"
        """,
        """
        def is_balanced(text):
            stack = []
            for ch in text:
                if ch == "(":
                    stack.append(ch)
                elif ch == ")":
                    if not stack:
                        return False
                    stack.pop()
            return not stack
        """, xp=20),
    cod(f"{P}-stack-e6", t("""
        Напиши функцию `serve(queue, n)`: обслужить `n` первых клиентов очереди — удалить их **из начала** списка
        и вернуть списком в порядке обслуживания. Если клиентов меньше `n` — обслужить всех.

        Пример:
        ```
        q = ["Аня", "Боря", "Вика"]
        serve(q, 2)   # → ["Аня", "Боря"], q == ["Вика"]
        ```
        """),
        """
        def serve(queue, n):
            pass
        """,
        """
        def test_values():
            q = ["Аня", "Боря", "Вика"]
            assert serve(q, 2) == ["Аня", "Боря"] and q == ["Вика"], f"q={q}"
            q2 = ["x"]
            assert serve(q2, 5) == ["x"] and q2 == [], "Клиентов меньше n — обслужить всех"
        """,
        """
        def serve(queue, n):
            served = []
            while queue and len(served) < n:
                served.append(queue.pop(0))
            return served
        """),
    cod(f"{P}-stack-e7", t("""
        Напиши функцию `process_fifo(tasks)` с `collections.deque`: пока очередь не пуста, доставать задачи **с начала**
        (`popleft`) и собирать строки `"готово: <задача>"`. Вернуть список строк.

        Пример:
        ```
        process_fifo(["сборка", "тесты"])   # → ["готово: сборка", "готово: тесты"]
        ```
        """),
        """
        from collections import deque

        def process_fifo(tasks):
            pass
        """,
        """
        def test_values():
            assert process_fifo(["сборка", "тесты"]) == ["готово: сборка", "готово: тесты"] and process_fifo([]) == [], "Неверный порядок"

        def test_deque():
            src = open("solution.py", encoding="utf-8").read()
            assert "popleft" in src, "Используй deque и popleft"
        """,
        """
        from collections import deque

        def process_fifo(tasks):
            queue = deque(tasks)
            done = []
            while queue:
                done.append(f"готово: {queue.popleft()}")
            return done
        """),
    cod(f"{P}-stack-e8", t("""
        Напиши функцию `reverse_with_stack(items)` — новый список в обратном порядке, построенный **через стек**:
        скопируй элементы в стек, затем доставай их `pop()` по одному. Без `reversed`, `reverse` и `[::-1]`.

        Пример:
        ```
        reverse_with_stack([1, 2, 3])   # → [3, 2, 1]
        ```
        """),
        """
        def reverse_with_stack(items):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3]
            assert reverse_with_stack(data) == [3, 2, 1] and data == [1, 2, 3], "Новый список, исходный не меняется"

        def test_no_shortcuts():
            src = open("solution.py", encoding="utf-8").read()
            assert "reverse" not in src.replace("reverse_with_stack", "") and "[::-1]" not in src, "Реши через стек"
        """,
        """
        def reverse_with_stack(items):
            stack = items.copy()
            result = []
            while stack:
                result.append(stack.pop())
            return result
        """)),
)
