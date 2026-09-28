"""Тема «Индексы и слайсы», модуль 1 «Индексы» — задания. Теория — в _slc_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "slc"

m1 = module(f"{P}-m1", "Индексы", "🎯", "Прямые и обратные индексы, строки и кортежи, IndexError, вложенные структуры",

lesson(f"{P}-m1-l1", "Положительные и отрицательные индексы",
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        s = "Python"
        print(s[0], s[3], s[-1], s[-3])
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа?", """
        items = [10, 20, 30, 40, 50]
        print(items[len(items) - 1] == items[-1])
        print(items[-len(items)])
        """, hint="`-len(items)` — это индекс первого элемента."),
    out(f"{P}-m1-l1-e6", "Что выведет программа? Два способа сказать «последний».", """
        s = "abcdef"
        print(s[1], s[-2])
        print(s[len(s) - 1], s[-1])
        print(s[-len(s)])
        """),
    cod(f"{P}-m1-l1-e3", t("""
        Напиши функцию `edges(text)`, которая возвращает строку из **первого и последнего** символа текста.

        Примеры:
        ```
        edges("Python")   # → "Pn"
        edges("a")        # → "aa"
        ```
        """),
        """
        def edges(text):
            pass
        """,
        """
        def test_values():
            assert edges("Python") == "Pn" and edges("a") == "aa" and edges("ok") == "ok", "Неверный результат"
        """,
        """
        def edges(text):
            return text[0] + text[-1]
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `second_last(items)` — предпоследний элемент списка (в списке минимум 2 элемента).

        Примеры:
        ```
        second_last([1, 2, 3])   # → 2
        second_last(["a", "b"])  # → "a"
        ```
        """),
        """
        def second_last(items):
            pass
        """,
        """
        def test_values():
            assert second_last([1, 2, 3]) == 2 and second_last(["a", "b"]) == "a", "Неверный элемент"
        """,
        """
        def second_last(items):
            return items[-2]
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `is_palindrome(word)` — читается ли слово одинаково в обе стороны. Сравнивай символы **по индексам** с двух концов (без срезов и `reversed`), регистр не учитывай.

        Примеры:
        ```
        is_palindrome("Шалаш")   # → True
        is_palindrome("python")  # → False
        ```
        Идея: для `i` от 0 до середины сравни `w[i]` и `w[-1 - i]`.
        """),
        """
        def is_palindrome(word):
            pass
        """,
        """
        def test_values():
            got = [is_palindrome(w) for w in ("Шалаш", "python", "a", "abba", "abca")]
            assert got == [True, False, True, True, False], f"Получено {got}"

        def test_no_slices():
            src = open("solution.py", encoding="utf-8").read()
            assert "[::-1]" not in src and "reversed" not in src, "Реши через индексы, без [::-1] и reversed"
        """,
        """
        def is_palindrome(word):
            w = word.lower()
            for i in range(len(w) // 2):
                if w[i] != w[-1 - i]:
                    return False
            return True
        """,
        hint="`w[-1 - i]` — i-й символ с конца.", xp=20),
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `middle_char(word)` — средний символ слова **нечётной** длины.

        Примеры:
        ```
        middle_char("кот")     # → "о"
        middle_char("радар")   # → "д"
        middle_char("я")       # → "я"
        ```
        """),
        """
        def middle_char(word):
            pass
        """,
        """
        def test_values():
            got = [middle_char("кот"), middle_char("радар"), middle_char("я")]
            assert got == ["о", "д", "я"], f"Получено {got}"
        """,
        """
        def middle_char(word):
            return word[len(word) // 2]
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `nth_from_end(items, n)` — `n`-й элемент **с конца** (`n = 1` — последний, `n = 2` — предпоследний…).
        Гарантируется, что `1 <= n <= len(items)`.

        Примеры:
        ```
        nth_from_end([10, 20, 30], 1)   # → 30
        nth_from_end([10, 20, 30], 3)   # → 10
        ```
        """),
        """
        def nth_from_end(items, n):
            pass
        """,
        """
        def test_values():
            got = [nth_from_end([10, 20, 30], 1), nth_from_end([10, 20, 30], 3), nth_from_end("abc", 2)]
            assert got == [30, 10, "b"], f"Получено {got}"
        """,
        """
        def nth_from_end(items, n):
            return items[-n]
        """)),

lesson(f"{P}-where", "Где работают индексы: строки, кортежи, range",
    out(f"{P}-where-e1", "Что выведет программа? Индексы у разных коллекций.", """
        t = (10, 20, 30)
        r = range(0, 100, 10)
        print(t[1], t[-1])
        print(r[3], r[-1], len(r))
        print("hey"[0])
        """),
    out(f"{P}-where-e2", "Что выведет программа? Строку по индексу не изменить.", """
        s = "кот"
        try:
            s[0] = "р"
        except TypeError:
            print("строки не меняются")
        print("р" + s[1] + s[2])
        print(s)
        """),
    out(f"{P}-where-e3", "Что выведет программа? Что возвращает индекс.", """
        print(type("abc"[0]).__name__, len("abc"[0]))
        print(type([1, 2][0]).__name__)
        print(type(["ab", "cd"][1][0]).__name__)
        """, hint="Символ строки — тоже строка, длиной 1."),
    cod(f"{P}-where-e4", t("""
        Напиши функцию `replace_char(s, i, ch)` — вернуть **новую** строку, где символ с индексом `i` заменён на `ch`.
        Строку изменить нельзя, поэтому преврати её в список символов, замени элемент и склей обратно.

        Примеры:
        ```
        replace_char("кот", 0, "р")    # → "рот"
        replace_char("abc", -1, "!")   # → "ab!"
        ```
        """),
        """
        def replace_char(s, i, ch):
            pass
        """,
        """
        def test_values():
            got = [replace_char("кот", 0, "р"), replace_char("abc", -1, "!"), replace_char("abc", 1, "X")]
            assert got == ["рот", "ab!", "aXc"], f"Получено {got}"
        """,
        """
        def replace_char(s, i, ch):
            chars = list(s)
            chars[i] = ch
            return "".join(chars)
        """,
        hint='`chars = list(s)`, `chars[i] = ch`, `"".join(chars)`.'),
    cod(f"{P}-where-e5", t("""
        Напиши функцию `last_in_range(start, stop, step)` — последнее число, которое выдаст `range(start, stop, step)`.
        Гарантируется, что диапазон не пустой.

        Примеры:
        ```
        last_in_range(0, 10, 3)    # → 9
        last_in_range(5, 0, -2)    # → 1
        ```
        """),
        """
        def last_in_range(start, stop, step):
            pass
        """,
        """
        def test_values():
            got = [last_in_range(0, 10, 3), last_in_range(5, 0, -2), last_in_range(1, 2, 1)]
            assert got == [9, 1, 1], f"Получено {got}"
        """,
        """
        def last_in_range(start, stop, step):
            return range(start, stop, step)[-1]
        """,
        hint="У `range` работают индексы, в том числе `-1`."),
    cod(f"{P}-where-e6", t("""
        Напиши функцию `second_of_pair(pair)` — второй элемент кортежа из двух значений.

        Пример:
        ```
        second_of_pair(("Аня", 25))   # → 25
        ```
        """),
        """
        def second_of_pair(pair):
            pass
        """,
        """
        def test_values():
            assert second_of_pair(("Аня", 25)) == 25 and second_of_pair((1, "x")) == "x", "Неверный элемент"
        """,
        """
        def second_of_pair(pair):
            return pair[1]
        """),
    cod(f"{P}-where-e7", t("""
        Напиши функцию `char_or_space(s, i)` — символ строки с индексом `i`, а если такого индекса нет — пробел `" "`.
        Отрицательные индексы тоже допустимы.

        Примеры:
        ```
        char_or_space("abc", 1)    # → "b"
        char_or_space("abc", 5)    # → " "
        char_or_space("abc", -1)   # → "c"
        char_or_space("abc", -4)   # → " "
        ```
        """),
        """
        def char_or_space(s, i):
            pass
        """,
        """
        def test_values():
            got = [char_or_space("abc", 1), char_or_space("abc", 5), char_or_space("abc", -1), char_or_space("abc", -4), char_or_space("", 0)]
            assert got == ["b", " ", "c", " ", " "], f"Получено {got}"
        """,
        """
        def char_or_space(s, i):
            if -len(s) <= i < len(s):
                return s[i]
            return " "
        """),
    cod(f"{P}-where-e8", t("""
        Напиши функцию `same_positions(a, b)` — сколько позиций, на которых у двух строк **одинаковые** символы.
        Сравнивать только до длины более короткой строки.

        Примеры:
        ```
        same_positions("кот", "кит")      # → 2
        same_positions("abc", "abcdef")   # → 3
        same_positions("ab", "ba")        # → 0
        ```
        """),
        """
        def same_positions(a, b):
            pass
        """,
        """
        def test_values():
            got = [same_positions("кот", "кит"), same_positions("abc", "abcdef"), same_positions("ab", "ba"), same_positions("", "x")]
            assert got == [2, 3, 0, 0], f"Получено {got}"
        """,
        """
        def same_positions(a, b):
            count = 0
            for i in range(min(len(a), len(b))):
                if a[i] == b[i]:
                    count += 1
            return count
        """)),

lesson(f"{P}-m1-l2", "IndexError и безопасный доступ",
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        items = []
        print(items[:1])
        print(items[0] if items else "пусто")
        try:
            items[0]
        except IndexError:
            print("IndexError")
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа?", """
        data = [5, 6]
        for i in range(4):
            print(data[i] if i < len(data) else "-")
        """),
    out(f"{P}-m1-l2-e6", "Что выведет программа? Допустимые индексы.", """
        items = [1, 2, 3]
        for i in (0, 2, 3, -3, -4):
            print(i, items[i] if -len(items) <= i < len(items) else "нет")
        """, hint="Допустимые индексы: от -len до len - 1."),
    cod(f"{P}-m1-l2-e3", t("""
        Напиши функцию `get_or_default(items, index, default=None)` — элемент по индексу, а если индекс вне списка — `default`. Отрицательные индексы тоже должны работать.

        Примеры:
        ```
        get_or_default([1, 2, 3], 1)        # → 2
        get_or_default([1, 2, 3], 5, 0)     # → 0
        get_or_default([1, 2, 3], -1)       # → 3
        get_or_default([1, 2, 3], -4, "x")  # → "x"
        ```
        """),
        """
        def get_or_default(items, index, default=None):
            pass
        """,
        """
        def test_values():
            got = [get_or_default([1, 2, 3], 1), get_or_default([1, 2, 3], 5, 0), get_or_default([1, 2, 3], -1), get_or_default([1, 2, 3], -4, "x"), get_or_default([], 0)]
            assert got == [2, 0, 3, "x", None], f"Получено {got}"
        """,
        """
        def get_or_default(items, index, default=None):
            try:
                return items[index]
            except IndexError:
                return default
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `first_word(text)` — первое слово строки или пустая строка `""`, если слов нет.

        Примеры:
        ```
        first_word("ERROR db down")   # → "ERROR"
        first_word("   ")             # → ""
        ```
        Осторожно: `"   ".split()` — пустой список, `[0]` у него упадёт.
        """),
        """
        def first_word(text):
            return text.split()[0]
        """,
        """
        def test_values():
            assert first_word("ERROR db down") == "ERROR" and first_word("   ") == "" and first_word("") == "", "Неверный результат"
        """,
        """
        def first_word(text):
            words = text.split()
            return words[0] if words else ""
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `latest_status(history)`, где `history` — список статусов прогонов по времени. Вернуть **последний** статус, а для пустой истории — `"нет данных"`.

        Примеры:
        ```
        latest_status(["pass", "fail", "pass"])   # → "pass"
        latest_status([])                         # → "нет данных"
        ```
        """),
        """
        def latest_status(history):
            pass
        """,
        """
        def test_values():
            assert latest_status(["pass", "fail", "pass"]) == "pass" and latest_status(["fail"]) == "fail" and latest_status([]) == "нет данных", "Неверный статус"
        """,
        """
        def latest_status(history):
            return history[-1] if history else "нет данных"
        """),
    cod(f"{P}-m1-l2-e7", t("""
        Напиши функцию `safe_last(items, default)` — последний элемент или `default` для пустого списка.

        Примеры:
        ```
        safe_last([1, 2], 0)   # → 2
        safe_last([], 0)       # → 0
        ```
        """),
        """
        def safe_last(items, default):
            pass
        """,
        """
        def test_values():
            assert safe_last([1, 2], 0) == 2 and safe_last([], 0) == 0 and safe_last([], None) is None, "Неверный результат"
        """,
        """
        def safe_last(items, default):
            return items[-1] if items else default
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши функцию `pick(items, indices)` — список элементов по индексам из `indices`, **пропуская** недопустимые индексы.

        Примеры:
        ```
        pick(["a", "b", "c"], [0, 2, 5, -1])   # → ["a", "c", "c"]
        pick([], [0])                          # → []
        ```
        """),
        """
        def pick(items, indices):
            pass
        """,
        """
        def test_values():
            got = [pick(["a", "b", "c"], [0, 2, 5, -1]), pick([], [0]), pick([1, 2], [-3, 1])]
            assert got == [["a", "c", "c"], [], [2]], f"Получено {got}"
        """,
        """
        def pick(items, indices):
            result = []
            for i in indices:
                if -len(items) <= i < len(items):
                    result.append(items[i])
            return result
        """)),

lesson(f"{P}-m1-l3", "Индексы во вложенных структурах",
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        resp = {"data": {"users": [{"name": "Аня", "roles": ["qa", "admin"]}, {"name": "Боря", "roles": []}]}}
        print(resp["data"]["users"][0]["name"])
        print(resp["data"]["users"][0]["roles"][-1])
        print(len(resp["data"]["users"][1]["roles"]))
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа?", """
        board = [["X", "O", "X"], [" ", "X", "O"], ["O", " ", "X"]]
        print(board[1][1], board[0][-1], board[-1][0])
        print([board[i][i] for i in range(3)])
        """),
    out(f"{P}-m1-l3-e6", "Что выведет программа? Глубокая вложенность.", """
        data = [[1, [2, 3]], [4]]
        print(data[0][1][0], data[-1][0])
        print(len(data[0][1]), data[0][-1][-1])
        """),
    cod(f"{P}-m1-l3-e3", t("""
        Напиши функцию `first_user_email(resp)` — email первого пользователя из ответа API вида:

        ```
        {"data": {"users": [{"email": "a@b.ru"}, ...]}}
        ```

        Если список пользователей пуст — вернуть `None`.

        Примеры:
        ```
        first_user_email({"data": {"users": [{"email": "a@b.ru"}]}})   # → "a@b.ru"
        first_user_email({"data": {"users": []}})                      # → None
        ```
        """),
        """
        def first_user_email(resp):
            pass
        """,
        """
        def test_values():
            assert first_user_email({"data": {"users": [{"email": "a@b.ru"}, {"email": "c@d.ru"}]}}) == "a@b.ru", "Нужен email первого пользователя"
            assert first_user_email({"data": {"users": []}}) is None, "Пустой список — None"
        """,
        """
        def first_user_email(resp):
            users = resp["data"]["users"]
            return users[0]["email"] if users else None
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `diagonal(matrix)` — список элементов главной диагонали квадратной матрицы (`m[0][0]`, `m[1][1]`, …).

        Пример:
        ```
        diagonal([[1, 2, 3], [4, 5, 6], [7, 8, 9]])   # → [1, 5, 9]
        ```
        """),
        """
        def diagonal(matrix):
            pass
        """,
        """
        def test_values():
            assert diagonal([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 5, 9] and diagonal([[7]]) == [7], "Неверная диагональ"
        """,
        """
        def diagonal(matrix):
            return [matrix[i][i] for i in range(len(matrix))]
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `dig(data, path, default=None)`, которая идёт по вложенной структуре по списку ключей/индексов `path`. Если на любом шаге ключа или индекса нет — вернуть `default`.

        Примеры:
        ```
        resp = {"data": {"users": [{"roles": ["qa", "admin"]}]}}
        dig(resp, ["data", "users", 0, "roles", -1])   # → "admin"
        dig(resp, ["data", "users", 5, "roles"])       # → None
        dig(resp, ["data", "items"], [])               # → []
        ```
        Перехватывай `KeyError`, `IndexError` и `TypeError` (на случай, если по пути попался не контейнер).
        """),
        """
        def dig(data, path, default=None):
            pass
        """,
        """
        def test_values():
            resp = {"data": {"users": [{"roles": ["qa", "admin"]}]}}
            assert dig(resp, ["data", "users", 0, "roles", -1]) == "admin", "Путь до admin"
            assert dig(resp, ["data", "users", 5, "roles"]) is None, "Нет индекса 5 → None"
            assert dig(resp, ["data", "items"], []) == [], "Нет ключа → default"
            assert dig(resp, ["data", "users", 0, "roles", 0, "x"]) is None, "Индексация строки по ключу → default"
        """,
        """
        def dig(data, path, default=None):
            current = data
            try:
                for step in path:
                    current = current[step]
            except (KeyError, IndexError, TypeError):
                return default
            return current
        """, xp=25),
    cod(f"{P}-m1-l3-e7", t("""
        Напиши функцию `anti_diagonal(matrix)` — побочная диагональ квадратной матрицы: из правого верхнего угла в левый нижний.

        Пример:
        ```
        anti_diagonal([[1, 2, 3], [4, 5, 6], [7, 8, 9]])   # → [3, 5, 7]
        ```
        Подсказка: в строке `i` нужен элемент `-1 - i`.
        """),
        """
        def anti_diagonal(matrix):
            pass
        """,
        """
        def test_values():
            assert anti_diagonal([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [3, 5, 7] and anti_diagonal([[5]]) == [5], "Неверная диагональ"
        """,
        """
        def anti_diagonal(matrix):
            result = []
            for i in range(len(matrix)):
                result.append(matrix[i][-1 - i])
            return result
        """),
    cod(f"{P}-m1-l3-e8", t("""
        Напиши функцию `cell(board, row, col)` — значение клетки доски (список списков) или `None`, если такой клетки нет.
        Отрицательные индексы **не** допускаются — для них тоже `None`.

        Примеры:
        ```
        board = [["X", "O"], [" ", "X"]]
        cell(board, 1, 1)    # → "X"
        cell(board, 2, 0)    # → None
        cell(board, 0, -1)   # → None
        ```
        """),
        """
        def cell(board, row, col):
            pass
        """,
        """
        def test_values():
            board = [["X", "O"], [" ", "X"]]
            got = [cell(board, 1, 1), cell(board, 0, 1), cell(board, 2, 0), cell(board, 0, -1), cell(board, 0, 2)]
            assert got == ["X", "O", None, None, None], f"Получено {got}"
        """,
        """
        def cell(board, row, col):
            if 0 <= row < len(board) and 0 <= col < len(board[row]):
                return board[row][col]
            return None
        """)),
)
