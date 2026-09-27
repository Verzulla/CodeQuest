"""Тема «Индексы и слайсы»."""
from ._lib import cod, lesson, module, out, q, t, topic

P = "slc"

# ============================================================
m1 = module(f"{P}-m1", "Индексы", "🎯", "Доступ к элементам, отрицательные индексы и вложенность",

lesson(f"{P}-m1-l1", "Положительные и отрицательные индексы", """
    # Индексы

    ```
    s = "Python"      # P  y  t  h  o  n
                      # 0  1  2  3  4  5
                      #-6 -5 -4 -3 -2 -1
    s[0]    # "P"
    s[-1]   # "n"
    s[-2]   # "o"
    ```

    Работает одинаково для строк, списков и кортежей.
    Последний элемент: `x[-1]` или `x[len(x) - 1]`.
    """,
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
        hint="`w[-1 - i]` — i-й символ с конца.", xp=20),
    full="""
    ## Зачем это нужно

    Индекс — адрес элемента в последовательности. Взять первый символ кода ответа, последний элемент истории, предпоследний шаг теста — всё это индексы. Отрицательные индексы Python делают доступ к концу последовательности очень удобным.

    ## Как это работает

    - Индексы начинаются с **0**: первый элемент — `x[0]`.
    - Последний — `x[len(x) - 1]`, короче — `x[-1]`.
    - Отрицательный индекс `-k` означает «k-й с конца»: `x[-k] == x[len(x) - k]`.
    - Допустимые индексы: от `-len(x)` до `len(x) - 1`.

    Индексы одинаково работают для всех последовательностей: `str`, `list`, `tuple`, `range`.

    ### Строки неизменяемы

    Читать `s[0]` можно, менять — нельзя: `s[0] = "X"` → `TypeError`. У списков — можно.

    ## Примеры

    ### Пример 1. Карта индексов

    ```python
    s = "Python"
    for i in range(len(s)):
        print(f"{i:>2} {i - len(s):>3}  {s[i]}")
    ```

    ### Пример 2. Разные последовательности

    ```python
    print("hello"[1], [10, 20, 30][-1], (1, 2, 3)[0], range(10, 20)[-1])
    ```

    ### Пример 3. Первая цифра кода ответа

    ```python
    for code in ["200", "404", "503"]:
        kind = {"2": "успех", "4": "ошибка клиента", "5": "ошибка сервера"}[code[0]]
        print(code, kind)
    ```

    ### Пример 4. Сравнение с двух концов

    ```python
    def is_palindrome(word):
        w = word.lower()
        for i in range(len(w) // 2):
            if w[i] != w[-1 - i]:
                return False
        return True

    print([is_palindrome(w) for w in ["Шалаш", "python", "abba"]])
    ```

    ## Частые ошибки

    **Индексация с единицы.**

    **`x[len(x)]`** — за границей.

    **Изменение символа строки** — строки неизменяемые, нужно собирать новую.

    ## Шпаргалка

    ```py
    x[0]   x[-1]   x[-2]
    x[-k] == x[len(x) - k]
    индексы: от -len(x) до len(x) - 1
    ```
    """,
    quiz=[
        q("Чему равно `\"hello\"[-2]`?", ["`e`", "`l`", "`o`", "`h`"], 1, "`-1` — `o`, `-2` — `l`."),
        q("Какой индекс у первого элемента списка длины 5, если считать отрицательными индексами?", ["`-1`", "`-5`", "`-4`", "`0`"], 1, "`x[-len(x)]` — первый элемент, то есть `-5`."),
        q("Что произойдёт при `s = \"cat\"; s[0] = \"b\"`?", ["s станет \"bat\"", "`TypeError`: строки неизменяемые", "Ничего", "`IndexError`"], 1, "Строку нельзя изменить на месте."),
    ]),

lesson(f"{P}-m1-l2", "IndexError и безопасный доступ", """
    # Выход за границы

    ```
    items = [1, 2, 3]
    items[3]        # IndexError: list index out of range
    ```

    Способы защититься:
    - проверить длину: `items[i] if i < len(items) else None`
    - проверить пустоту: `items[0] if items else None`
    - `try` / `except IndexError`
    - срез не падает: `items[:1]` вернёт `[]` для пустого списка
    """,
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
        """),
    full="""
    ## Зачем это нужно

    `IndexError: list index out of range` — одна из самых частых ошибок в Python. В автотестах она означает «падение теста не из-за бага продукта, а из-за самого теста»: например, API вернул пустой список, а тест сразу взял `items[0]`. Хороший код и хорошие тесты заранее решают, что делать с пустыми данными.

    ## Как это работает

    Обращение к несуществующему индексу бросает `IndexError`. Способы обработки:

    1. **Проверка пустоты**: `items[0] if items else None` — самый частый случай.
    2. **Проверка длины**: `items[i] if -len(items) <= i < len(items) else default`.
    3. **try/except**: попробовать и перехватить `IndexError`. Удобно, когда индекс может быть любым, включая отрицательный.
    4. **Срезы**: `items[:1]`, `items[-1:]` никогда не падают — вернут пустой список.

    ### Что выбрать в тестах

    Если пустой ответ — это баг, тест должен падать **понятно**: `assert items, "API вернул пустой список"`, а не с безликим `IndexError`.

    ## Примеры

    ### Пример 1. Ошибка и её перехват

    ```python
    items = [1, 2, 3]
    try:
        print(items[10])
    except IndexError as e:
        print("поймали:", e)
    ```

    ### Пример 2. Разные способы безопасного доступа

    ```python
    for items in [[], [42]]:
        print("условие:", items[0] if items else None,
              "| срез:", items[:1],
              "| next:", next(iter(items), None))
    ```

    ### Пример 3. Понятная ошибка в тесте

    ```python
    def check_first_user(users):
        assert users, "API вернул пустой список пользователей"
        assert users[0]["id"] == 1, f"первый пользователь: {users[0]}"

    for data in [[{"id": 1}], []]:
        try:
            check_first_user(data)
            print("ok")
        except AssertionError as e:
            print("тест упал:", e)
    ```

    ### Пример 4. Универсальный геттер

    ```python
    def get_or_default(items, index, default=None):
        try:
            return items[index]
        except IndexError:
            return default

    print(get_or_default([1, 2, 3], -1), get_or_default([1, 2, 3], 7, "нет"))
    ```

    ## Частые ошибки

    **`text.split()[0]`** на пустой строке.

    **Проверка `if index < len(items)`** без учёта отрицательных индексов.

    **Голый `except:`** — ловит всё подряд и прячет другие баги. Лови `IndexError`.

    ## Шпаргалка

    ```py
    xs[0] if xs else None
    xs[:1]                         # не падает
    try: xs[i]
    except IndexError: ...
    assert xs, "понятное сообщение"
    ```
    """,
    quiz=[
        q("Что вернёт `[][:1]`?", ["`IndexError`", "`[]`", "`None`", "`[None]`"], 1, "Срезы не выходят за границы с ошибкой — вернут пустой список."),
        q("Что вернёт `\"   \".split()`?", ["`['', '', '']`", "`[]`", "`['   ']`", "Ошибка"], 1, "`split()` без аргумента игнорирует пробелы, слов нет — пустой список."),
        q("Как лучше написать проверку в тесте, если пустой ответ API — это баг?", ["Сразу брать `users[0]`", "`assert users, \"API вернул пустой список\"`", "Обернуть в try и молча пропустить", "Ничего не проверять"], 1,
          "Тест должен падать с понятным сообщением о причине."),
    ]),

lesson(f"{P}-m1-l3", "Индексы во вложенных структурах", """
    # Цепочки индексов

    ```
    resp = {"data": {"users": [{"name": "Аня", "roles": ["qa", "admin"]}]}}
    resp["data"]["users"][0]["roles"][-1]     # "admin"
    ```

    Читается слева направо: ключ → ключ → индекс → ключ → индекс.
    Каждый шаг может упасть: `KeyError` для словаря, `IndexError` для списка.
    """,
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
        """, xp=25),
    full="""
    ## Зачем это нужно

    Ответы API — это вложенные словари и списки. Чтобы проверить нужное поле, приходится «спускаться» по цепочке ключей и индексов. Важно уметь читать такие цепочки и понимать, где они могут сломаться.

    ## Как это работает

    Каждый `[...]` применяется к результату предыдущего:

    ```py
    resp["data"]["users"][0]["roles"][-1]
    #  dict  →  dict  → list → dict → list → str
    ```

    Чтобы не запутаться, разбирай ответ по шагам — или сохраняй промежуточные значения в переменные с понятными именами:

    ```py
    users = resp["data"]["users"]
    first = users[0]
    last_role = first["roles"][-1]
    ```

    ### Где падает

    - нет ключа → `KeyError`;
    - нет индекса → `IndexError`;
    - не тот тип (индексируем `None` или число) → `TypeError`.

    ### Матрицы

    `m[строка][столбец]`. Главная диагональ — `m[i][i]`, побочная — `m[i][-1 - i]`.

    ## Примеры

    ### Пример 1. Разбор ответа по шагам

    ```python
    resp = {"data": {"users": [{"name": "Аня", "roles": ["qa", "admin"]}, {"name": "Боря", "roles": []}]}}
    users = resp["data"]["users"]
    print("пользователей:", len(users))
    for u in users:
        roles = u["roles"]
        print(u["name"], "— последняя роль:", roles[-1] if roles else "нет ролей")
    ```

    ### Пример 2. Где ломается цепочка

    ```python
    resp = {"data": {"users": []}}
    for path in ['resp["data"]["users"][0]', 'resp["meta"]', 'resp["data"]["users"]["x"]']:
        try:
            eval(path)
        except Exception as e:
            print(f"{path:30} -> {type(e).__name__}: {e}")
    ```

    ### Пример 3. Безопасный спуск

    ```python
    def dig(data, path, default=None):
        current = data
        try:
            for step in path:
                current = current[step]
        except (KeyError, IndexError, TypeError):
            return default
        return current

    resp = {"data": {"users": [{"roles": ["qa", "admin"]}]}}
    print(dig(resp, ["data", "users", 0, "roles", -1]))
    print(dig(resp, ["data", "users", 3, "roles"], "нет такого"))
    ```

    ### Пример 4. Диагонали

    ```python
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    n = len(m)
    print([m[i][i] for i in range(n)], [m[i][n - 1 - i] for i in range(n)])
    ```

    ## Частые ошибки

    **Длинная цепочка без промежуточных переменных** — при падении непонятно, какой шаг сломался.

    **Пустой список в середине пути** — `users[0]` на пустом ответе.

    **Строки тоже индексируются** — `"abc"[0]` работает, а `"abc"["x"]` даст `TypeError`.

    ## Шпаргалка

    ```py
    resp["data"]["items"][0]["id"]
    users = resp["data"]["users"]; first = users[0] if users else None
    KeyError — нет ключа · IndexError — нет индекса · TypeError — не тот тип
    ```
    """,
    quiz=[
        q("Какую ошибку даст `{\"a\": []}[\"a\"][0]`?", ["`KeyError`", "`IndexError`", "`TypeError`", "Никакую"], 1, "Ключ есть, но список пуст — нет элемента с индексом 0."),
        q("Что вернёт `[[1, 2], [3, 4]][-1][-1]`?", ["`1`", "`2`", "`3`", "`4`"], 3, "Последняя строка `[3, 4]`, её последний элемент — 4."),
        q("Какую ошибку даст `None[0]`?", ["`IndexError`", "`KeyError`", "`TypeError`", "`ValueError`"], 2, "`None` не поддерживает индексацию — это ошибка типа."),
    ]),
)

# ============================================================
m2 = module(f"{P}-m2", "Срезы", "✂️", "start:stop:step, разворот и подстроки",

lesson(f"{P}-m2-l1", "Срез start:stop", """
    # Срезы

    `x[start:stop]` — новый список/строка с элементами от `start` до `stop - 1`.

    ```
    a = [0, 1, 2, 3, 4, 5]
    a[1:4]     # [1, 2, 3] — stop не входит
    a[:3]      # [0, 1, 2] — первые три
    a[3:]      # [3, 4, 5] — начиная с индекса 3
    a[-2:]     # [4, 5]   — последние два
    a[:]       # копия
    ```

    Срез **не падает**, если границы за пределами.
    """,
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
        """),
    full="""
    ## Зачем это нужно

    Взять первые 10 строк лога, последние 5 прогонов теста, всё кроме заголовка CSV, часть строки — срезы решают это одной конструкцией, без циклов и без риска `IndexError`.

    ## Как это работает

    `x[start:stop]`:
    - берёт элементы с индекса `start` **включительно** до `stop` **не включительно**;
    - пропущенный `start` — с начала, пропущенный `stop` — до конца;
    - отрицательные значения считаются с конца: `x[-3:]` — последние три;
    - всегда возвращает **новый** объект того же типа (список → список, строка → строка);
    - границы за пределами просто «обрезаются» — ошибки не будет.

    Длина среза `x[a:b]` (при корректных границах) — `b - a`.

    ### Полезные шаблоны

    - `x[:n]` — первые n;
    - `x[-n:]` — последние n (но осторожно с `n = 0`!);
    - `x[1:]` — всё, кроме первого (например, без заголовка);
    - `x[:-1]` — всё, кроме последнего;
    - `x[1:-1]` — без краёв;
    - `x[:]` — мелкая копия.

    ### Ловушка -0

    `-0` — это `0`. Поэтому `x[-0:]` — весь список, а не пустой.

    ## Примеры

    ### Пример 1. Основные срезы

    ```python
    a = list(range(10))
    print(a[2:5], a[:3], a[7:], a[-3:], a[:-7])
    ```

    ### Пример 2. Лог без заголовка, последние записи

    ```python
    lines = ["time;level;msg", "10:00;INFO;start", "10:01;ERROR;db", "10:02;INFO;retry", "10:03;INFO;ok"]
    header, rows = lines[0], lines[1:]
    print("колонки:", header.split(";"))
    print("последние 2:", rows[-2:])
    ```

    ### Пример 3. Ловушка -0

    ```python
    items = [1, 2, 3]
    for n in [2, 1, 0]:
        print(n, items[-n:], items[len(items) - n:])
    ```

    ### Пример 4. Срез — копия

    ```python
    original = [1, 2, 3]
    copy_ = original[:]
    copy_.append(4)
    print(original, copy_)
    ```

    ## Частые ошибки

    **Ожидание, что `stop` входит** — `a[1:3]` содержит 2 элемента.

    **`x[-n:]` при `n = 0`** — вернёт всё.

    **Ожидание ошибки** — срез за границами молча вернёт меньше элементов; в тестах это может скрыть проблему.

    ## Шпаргалка

    ```py
    x[a:b]   # a включительно, b нет
    x[:n]  x[-n:]  x[1:]  x[:-1]  x[1:-1]  x[:]
    ```
    """,
    quiz=[
        q("Что вернёт `[0, 1, 2, 3, 4][1:3]`?", ["`[1, 2, 3]`", "`[1, 2]`", "`[0, 1, 2]`", "`[2, 3]`"], 1, "Индекс 3 не входит в срез."),
        q("Что вернёт `[1, 2, 3][-0:]`?", ["`[]`", "`[1, 2, 3]`", "`[3]`", "Ошибка"], 1, "`-0` равно `0`, срез с начала до конца — весь список."),
        q("Что вернёт `\"hello\"[10:]`?", ["Ошибка", "`''`", "`None`", "`'hello'`"], 1, "Срезы не падают за границами — получится пустая строка."),
    ]),

lesson(f"{P}-m2-l2", "Шаг и разворот", """
    # Шаг среза

    `x[start:stop:step]`

    ```
    a = [0, 1, 2, 3, 4, 5, 6]
    a[::2]      # [0, 2, 4, 6] — каждый второй
    a[1::2]     # [1, 3, 5]    — нечётные позиции
    a[::-1]     # [6, 5, 4, 3, 2, 1, 0] — задом наперёд
    a[5:1:-1]   # [5, 4, 3, 2]
    ```

    При отрицательном шаге `start` должен быть **правее** `stop`.
    """,
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
        """),
    full="""
    ## Зачем это нужно

    Каждый второй элемент, чётные и нечётные позиции, разворот строки или списка — задачи на «шаг» встречаются и в работе, и на собеседованиях. Срез с шагом решает их без циклов.

    ## Как это работает

    `x[start:stop:step]`:
    - `step` — через сколько элементов брать; по умолчанию 1;
    - `step = 2` — каждый второй, `3` — каждый третий;
    - **отрицательный** шаг — движение справа налево;
    - `x[::-1]` — классический разворот (новый объект).

    При отрицательном шаге значения по умолчанию меняются местами: `start` — конец последовательности, `stop` — «до начала включительно». Если явно указать `start` левее `stop`, результат будет пустым: `a[1:4:-1]` → `[]`.

    Шаг не может быть нулём (`ValueError`).

    ### Альтернативы развороту

    - `reversed(x)` — ленивый итератор, без копии;
    - `list.reverse()` — на месте.

    ## Примеры

    ### Пример 1. Шаги

    ```python
    a = list(range(10))
    print(a[::2])
    print(a[1::2])
    print(a[::3])
    print(a[2:8:2])
    ```

    ### Пример 2. Отрицательный шаг

    ```python
    a = list(range(6))
    print(a[::-1])
    print(a[4:1:-1])
    print(a[::-2])
    print(a[1:4:-1])       # пусто: start левее stop
    ```

    ### Пример 3. Палиндром

    ```python
    def is_palindrome(text):
        clean = "".join(ch for ch in text.lower() if ch.isalnum())
        return clean == clean[::-1]

    for s in ["А роза упала на лапу Азора", "Python", "Madam, I'm Adam"]:
        print(s, "->", is_palindrome(s))
    ```

    ### Пример 4. Разворот слов и чередование

    ```python
    text = "сборка тесты деплой"
    print(" ".join(text.split()[::-1]))
    players = ["Аня", "Боря", "Вика", "Гоша", "Даша"]
    print("команда 1:", players[::2], "| команда 2:", players[1::2])
    ```

    ## Частые ошибки

    **`a[1:4:-1]`** с отрицательным шагом — пусто; нужно `a[3:0:-1]`.

    **`step = 0`** — `ValueError`.

    **Разворот огромного списка ради перебора** — `reversed()` не создаёт копию.

    ## Шпаргалка

    ```py
    x[::2]    # каждый второй с начала
    x[1::2]   # нечётные позиции
    x[::-1]   # задом наперёд
    x[5:1:-1] # 5, 4, 3, 2
    reversed(x)  # без копии
    ```
    """,
    quiz=[
        q("Что вернёт `\"abcdef\"[::2]`?", ["`'ace'`", "`'bdf'`", "`'ab'`", "`'fdb'`"], 0, "Каждый второй символ начиная с индекса 0."),
        q("Что вернёт `[0, 1, 2, 3][1:3:-1]`?", ["`[2, 1]`", "`[]`", "`[1, 2]`", "Ошибка"], 1, "При отрицательном шаге start должен быть правее stop, иначе результат пуст."),
        q("Чем `reversed(x)` отличается от `x[::-1]`?", ["Ничем", "`reversed` возвращает ленивый итератор без копии", "`reversed` сортирует", "`x[::-1]` меняет список на месте"], 1, "Срез создаёт новый объект, `reversed` — только итератор."),
    ]),

lesson(f"{P}-m2-l3", "Срезы строк", """
    # Срезы строк

    ```
    s = "2024-09-27"
    s[:4]     # "2024"
    s[5:7]    # "09"
    s[-2:]    # "27"
    ```

    Строки неизменяемые — срез всегда создаёт **новую** строку.
    Удобно сочетать с `find`: `s[s.find(":") + 1:]` — всё после двоеточия.
    """,
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
        """),
    full="""
    ## Зачем это нужно

    Строки с фиксированной структурой встречаются постоянно: даты `2024-09-27`, коды `ERR-042`, токены после `Bearer `, домены после `@`. Срезы вместе с `find` позволяют вырезать нужную часть без регулярных выражений. А ещё — маскировать секреты в логах и обрезать длинные сообщения.

    ## Как это работает

    Срезы строк работают так же, как у списков, и возвращают **новую строку**.

    ### Срез + find

    `find(x)` возвращает позицию подстроки (или `-1`). Отсюда:
    - всё **после** разделителя: `s[s.find(sep) + len(sep):]`;
    - всё **до** разделителя: `s[:s.find(sep)]`;
    - не забывай проверять `-1`, иначе получишь неожиданный результат.

    Альтернативы без индексов: `s.partition(sep)` → `(до, sep, после)`, `s.split(sep, 1)`.

    ### Маскирование

    `"*" * (len(s) - 4) + s[-4:]` — стандарт для карт, телефонов, токенов в логах.

    ## Примеры

    ### Пример 1. Разбор даты

    ```python
    date = "2024-09-27"
    year, month, day = date[:4], date[5:7], date[8:]
    print(year, month, day)
    print(int(month) == 9)
    ```

    ### Пример 2. Токен из заголовка

    ```python
    header = "Authorization: Bearer abc123"
    prefix = "Bearer "
    pos = header.find(prefix)
    token = header[pos + len(prefix):] if pos != -1 else None
    print(token)
    print(header.partition(prefix))
    ```

    ### Пример 3. Маскирование секретов

    ```python
    def mask(value, visible=4):
        return "*" * max(0, len(value) - visible) + value[-visible:]

    print(mask("1234567812345678"))
    print(mask("sk-test-9f8e7d6c5b"))
    ```

    ### Пример 4. Обрезка длинного текста

    ```python
    def truncate(text, limit):
        return text if len(text) <= limit else text[:limit - 3] + "..."

    msg = "AssertionError: expected status 201, got 500 with body {...}"
    print(truncate(msg, 30))
    ```

    ## Частые ошибки

    **`s[s.find(x):]` без проверки** — если `find` вернул `-1`, получишь последний символ.

    **Забыли `+ len(sep)`** — в результат попадёт сам разделитель.

    **Ожидание изменения исходной строки** — срез создаёт новую.

    ## Шпаргалка

    ```py
    s[:4]  s[5:7]  s[-2:]
    s[s.find(sep) + len(sep):]     # после разделителя
    before, _, after = s.partition(sep)
    "*" * (len(s) - 4) + s[-4:]    # маска
    ```
    """,
    quiz=[
        q("Что вернёт `\"2024-09-27\"[5:7]`?", ["`'09'`", "`'-0'`", "`'09-'`", "`'9-'`"], 0, "Индексы 5 и 6 — символы `0` и `9`."),
        q("Что вернёт `\"abc\"[\"abc\".find(\"z\"):]`?", ["`''`", "`'c'`", "`'abc'`", "Ошибка"], 1, "`find` вернул -1, срез `[-1:]` — последний символ. Классический баг без проверки."),
        q("Что вернёт `\"key=value\".partition(\"=\")`?", ["`['key', 'value']`", "`('key', '=', 'value')`", "`('key', 'value')`", "`'value'`"], 1, "`partition` возвращает кортеж: до, разделитель, после."),
    ]),
)

# ============================================================
m3 = module(f"{P}-m3", "Приёмы со срезами", "🧩", "Изменение срезами, окна, пачки и распаковка",

lesson(f"{P}-m3-l1", "Изменение списка срезами", """
    # Присваивание и удаление срезом (только списки)

    ```
    a = [0, 1, 2, 3, 4]
    a[1:3] = ["x", "y", "z"]   # заменить часть: [0, 'x', 'y', 'z', 3, 4]
    del a[:2]                  # удалить первые два
    a[:] = []                  # очистить, сохранив тот же объект
    ```

    Длина вставки может отличаться от длины заменяемого куска.
    """,
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
        """, xp=20),
    full="""
    ## Зачем это нужно

    Иногда нужно изменить не один элемент, а целый кусок списка: удалить первые N записей, заменить середину, обрезать историю до последних 100 событий, очистить список, на который ссылаются другие части программы. Для списков срезы работают и «на запись».

    ## Как это работает

    Только для **изменяемых** последовательностей (списков):

    - `a[i:j] = iterable` — заменить кусок. Длины могут не совпадать: список вырастет или сократится.
    - `a[i:i] = [x, y]` — вставка без удаления.
    - `del a[i:j]` — удалить кусок.
    - `a[:] = new` — заменить **всё содержимое**, сохранив тот же объект (все ссылки увидят изменение).
    - Со срезом с шагом длины должны совпадать: `a[::2] = [...]`.

    ### a[:] = ... против a = ...

    - `a = []` — имя `a` теперь указывает на новый пустой список; старый список (и другие ссылки на него) не изменились.
    - `a[:] = []` — очищается сам объект; это видно через все ссылки.

    ## Примеры

    ### Пример 1. Замена и вставка

    ```python
    a = [0, 1, 2, 3, 4]
    a[1:3] = ["x", "y", "z"]
    print(a)
    a[1:1] = ["NEW"]
    print(a)
    a[::2] = ["-"] * len(a[::2])
    print(a)
    ```

    ### Пример 2. Ограничение размера истории

    ```python
    history = list(range(1, 11))
    LIMIT = 3
    del history[:-LIMIT]
    print(history)
    ```

    ### Пример 3. Очистка «для всех»

    ```python
    shared = ["a", "b"]
    alias = shared
    shared[:] = []
    print(alias)

    shared = ["a", "b"]
    alias = shared
    shared = []
    print(alias)
    ```

    ## Частые ошибки

    **Присваивание срезом строке** — строки неизменяемые, `TypeError`.

    **`a[1:3] = "xy"`** — строка разобьётся на символы (это итерируемое).

    **Разная длина при шаге** — `ValueError: attempt to assign sequence of size ...`.

    ## Шпаргалка

    ```py
    a[i:j] = [...]     # заменить кусок
    a[i:i] = [...]     # вставить
    del a[i:j]         # удалить кусок
    del a[:-n]         # оставить последние n
    a[:] = []          # очистить этот же объект
    ```
    """,
    quiz=[
        q("Что станет с `a = [1, 2, 3, 4]` после `a[1:3] = [\"x\"]`?", ["`[1, 'x', 4]`", "`[1, 'x', 3, 4]`", "Ошибка", "`['x']`"], 0, "Кусок из двух элементов заменён одним — список укоротился."),
        q("После `a = [1]; b = a; a[:] = []` чему равно `b`?", ["`[1]`", "`[]`", "`None`", "Ошибка"], 1, "`a[:] = []` очищает сам объект, на который ссылается и `b`."),
        q("Можно ли сделать `s = \"abc\"; s[0:1] = \"X\"`?", ["Да", "Нет, строки неизменяемые", "Только для латиницы", "Да, но s станет списком"], 1, "Присваивание срезом работает только для изменяемых последовательностей."),
    ]),

lesson(f"{P}-m3-l2", "Пачки и скользящее окно", """
    # Пачки (chunks)

    ```
    items[i:i + size]  for i in range(0, len(items), size)
    ```

    # Скользящее окно

    ```
    items[i:i + k]     for i in range(len(items) - k + 1)
    ```

    Пачки не пересекаются, окна — сдвигаются на один элемент.
    """,
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
        """, xp=20),
    full="""
    ## Зачем это нужно

    Два приёма, которые постоянно встречаются на практике:
    - **пачки** — отправить 1000 записей в API по 100, разбить тесты между воркерами, выводить таблицу постранично;
    - **скользящее окно** — среднее время ответа за последние N запросов, поиск серии из N падений подряд, сглаживание графиков.

    ## Как это работает

    ### Пачки

    Начала пачек идут с шагом `size`: `0, size, 2*size, …`

    ```py
    [items[i:i + size] for i in range(0, len(items), size)]
    ```

    Последняя пачка может быть короче — срез не падает.

    ### Окна

    Окно длины `k` сдвигается на 1. Окон всего `len(items) - k + 1` (если элементов меньше `k` — ни одного).

    ```py
    [items[i:i + k] for i in range(len(items) - k + 1)]
    ```

    Для больших данных окна пересчитывают инкрементально (прибавить новый элемент, вычесть ушедший), но принцип тот же.

    ## Примеры

    ### Пример 1. Пачки запросов

    ```python
    ids = list(range(1, 11))
    BATCH = 4
    for n, i in enumerate(range(0, len(ids), BATCH), start=1):
        print(f"запрос {n}: ids={ids[i:i + BATCH]}")
    ```

    ### Пример 2. Скользящее среднее

    ```python
    response_ms = [120, 130, 125, 900, 880, 140, 135]
    k = 3
    for i in range(len(response_ms) - k + 1):
        window = response_ms[i:i + k]
        avg = sum(window) / k
        flag = "⚠️" if avg > 500 else ""
        print(window, round(avg), flag)
    ```

    ### Пример 3. Серия падений

    ```python
    runs = ["pass", "fail", "fail", "pass", "fail", "fail", "fail"]
    k = 3
    streaks = [i for i in range(len(runs) - k + 1) if runs[i:i + k] == ["fail"] * k]
    print("серия из 3 падений начинается на позиции:", streaks)
    ```

    ### Пример 4. Попарные разницы

    ```python
    values = [10, 12, 9, 15]
    print([b - a for a, b in zip(values, values[1:])])
    ```

    ## Частые ошибки

    **`range(len(items) - k)`** без `+ 1` — теряется последнее окно.

    **Шаг `range` для пачек равен 1** — пачки пересекаются.

    **Окно больше данных** — формула даёт отрицательный `range`, результат пустой (это нормально, но проверь, что так и задумано).

    ## Шпаргалка

    ```py
    [xs[i:i + n] for i in range(0, len(xs), n)]      # пачки
    [xs[i:i + k] for i in range(len(xs) - k + 1)]    # окна
    zip(xs, xs[1:])                                  # соседние пары
    ```
    """,
    quiz=[
        q("Сколько окон длины 3 в списке из 5 элементов?", ["2", "3", "5", "15"], 1, "`5 - 3 + 1 = 3` окна."),
        q("Что вернёт `[items[i:i + 2] for i in range(0, 5, 2)]` для `items = [1, 2, 3, 4, 5]`?", ["`[[1, 2], [3, 4]]`", "`[[1, 2], [3, 4], [5]]`", "`[[1, 2], [2, 3], [3, 4], [4, 5]]`", "Ошибка"], 1, "Три пачки; последняя короче."),
        q("Что даст `list(zip([1, 2, 3], [2, 3]))`?", ["`[(1, 2), (2, 3)]`", "`[(1, 2), (2, 3), (3, None)]`", "`[1, 2, 3, 2, 3]`", "Ошибка"], 0, "`zip(xs, xs[1:])` — пары соседних элементов."),
    ]),

lesson(f"{P}-m3-l3", "Распаковка", """
    # Распаковка

    ```
    a, b = [1, 2]
    first, *rest = [1, 2, 3, 4]      # first=1, rest=[2, 3, 4]
    *start, last = [1, 2, 3]         # start=[1, 2], last=3
    head, *_, tail = "Python"        # head="P", tail="n"
    name, (x, y) = ["point", (3, 4)] # вложенная распаковка
    ```

    Число переменных без `*` должно совпадать с числом элементов.
    """,
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
        """),
    full="""
    ## Зачем это нужно

    Распаковка позволяет разложить последовательность по переменным одной строкой: заголовок и строки CSV, первый аргумент и остальные, дата/время/уровень и сообщение лога. Код становится короче и понятнее, чем с индексами `[0]`, `[1]`, `[2:]`.

    ## Как это работает

    ### Простая распаковка

    `a, b, c = [1, 2, 3]` — число переменных должно **совпадать** с числом элементов, иначе `ValueError`. Работает с любым итерируемым: списком, кортежем, строкой, результатом `split`.

    ### Звёздочка

    Одна переменная со `*` собирает «всё остальное» в **список** (может оказаться пустым):
    - `first, *rest = xs`
    - `*start, last = xs`
    - `head, *middle, tail = xs`

    Звёздочка в распаковке — только одна.

    ### _ для ненужного

    По соглашению ненужные значения называют `_`: `name, _, status = row`, `head, *_ = xs`.

    ### Вложенная распаковка

    `name, (x, y) = ["p", (3, 4)]` и в циклах: `for i, (k, v) in enumerate(d.items()):`.

    ### Распаковка при сборке

    `*` работает и в обратную сторону: `[last, *middle, first]`, `print(*items)`.

    ## Примеры

    ### Пример 1. Звёздочка в разных позициях

    ```python
    data = [1, 2, 3, 4, 5]
    first, *rest = data
    *start, last = data
    head, *middle, tail = data
    print(first, rest)
    print(start, last)
    print(head, middle, tail)
    ```

    ### Пример 2. CSV: заголовок и строки

    ```python
    csv_lines = ["name;status;time", "login;pass;1.2", "pay;fail;3.4"]
    header, *rows = csv_lines
    columns = header.split(";")
    for row in rows:
        record = dict(zip(columns, row.split(";")))
        print(record)
    ```

    ### Пример 3. Строка лога

    ```python
    line = "2024-09-27 12:00:01 ERROR нет связи с БД"
    date, time, level, *words = line.split()
    print(level, "|", " ".join(words))
    ```

    ### Пример 4. Ошибка количества

    ```python
    try:
        a, b = [1, 2, 3]
    except ValueError as e:
        print("ошибка:", e)
    a, b, *_ = [1, 2, 3]
    print(a, b)
    ```

    ### Пример 5. Сборка со звёздочкой

    ```python
    first, *middle, last = [1, 2, 3, 4]
    print([last, *middle, first])
    print(*middle, sep=" | ")
    ```

    ## Частые ошибки

    **Несовпадение количества** — `ValueError: too many values to unpack`.

    **Две звёздочки** — `SyntaxError`.

    **Ожидание кортежа в `*rest`** — там всегда список.

    ## Шпаргалка

    ```py
    a, b = pair
    first, *rest = xs
    *init, last = xs
    head, *_, tail = xs
    for i, (k, v) in enumerate(d.items()): ...
    [*a, *b]              # склейка распаковкой
    ```
    """,
    quiz=[
        q("Что будет в `rest` после `first, *rest = [1]`?", ["`None`", "`[]`", "Ошибка", "`[1]`"], 1, "Звёздочка собирает оставшиеся элементы; их нет — пустой список."),
        q("Что произойдёт при `a, b = \"abc\"`?", ["a='a', b='bc'", "`ValueError`: слишком много значений", "a='ab', b='c'", "Ошибка типа"], 1, "Строка из трёх символов не раскладывается на две переменные."),
        q("Какой тип у `middle` в `head, *middle, tail = (1, 2, 3, 4)`?", ["`tuple`", "`list`", "`int`", "Зависит от исходного типа"], 1, "Переменная со звёздочкой всегда получает список."),
    ]),
)

TOPIC = topic("py-slices", "Индексы и слайсы", "✂️", "#ce82ff",
              "Индексы, срезы с шагом, срезы строк, окна, пачки и распаковка",
              m1, m2, m3, group="Python")
