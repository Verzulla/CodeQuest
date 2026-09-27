"""Тема «Индексы и слайсы»."""
from ._lib import cod, lesson, module, out, t, topic

P = "slc"

# ============================================================
m1 = module(f"{P}-m1", "Индексы", "🎯", "Доступ к элементам, отрицательные индексы и вложенность",

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
        hint="`w[-1 - i]` — i-й символ с конца.", xp=20)),

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
        """, xp=25)),
)

# ============================================================
m2 = module(f"{P}-m2", "Срезы", "✂️", "start:stop:step, разворот и подстроки",

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
        """)),

lesson(f"{P}-m2-l2", "Шаг и разворот", 
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        a = list(range(8))
        print(a[::2], a[1::2], a[::3])
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа? Отрицательный шаг.", """
        a = [0, 1, 2, 3, 4, 5]
        print(a[::-1])
        print(a[4:1:-1])
        print(a[1:4:-1])
        print("abc"[::-1])
        """, hint="При шаге -1 срез идёт справа налево; если start левее stop — результат пустой."),
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
        """)),
)

# ============================================================
m3 = module(f"{P}-m3", "Приёмы со срезами", "🧩", "Изменение срезами, окна, пачки и распаковка",

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
        """, xp=20)),

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
        """, xp=20)),

lesson(f"{P}-m3-l3", "Распаковка", 
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
        """)),
)

TOPIC = topic("py-slices", "Индексы и слайсы", "✂️", "#ce82ff",
              "Индексы, срезы с шагом, срезы строк, окна, пачки и распаковка",
              m1, m2, m3, group="Python")
