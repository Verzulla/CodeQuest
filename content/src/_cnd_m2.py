"""Тема «Условные операторы», модуль 2 «Логика» — задания. Теория — в _cnd_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "cnd"

m2 = module(f"{P}-m2", "Логика", "🧠", "and, or, not, короткое замыкание, истинность, in, вложенные условия",

lesson(f"{P}-m2-l1", "and, or, not",
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        print(True and False, True or False, not True)
        print(True or False and False)
        print((True or False) and False)
        """, hint="`and` выполняется раньше `or`."),
    out(f"{P}-m2-l1-e6", "Что выведет программа?", """
        x = 15
        print(x > 10 and x < 20)
        print(x < 10 or x > 20)
        print(not x > 10)
        """, hint="Сравнения выполняются раньше `and`, `or` и `not`."),
    out(f"{P}-m2-l1-e7", "Что выведет программа? Приоритет логических операторов.", """
        print(True or True and False)
        print((True or True) and False)
        print(not True or True)
        print(not (True or True))
        """, hint="Порядок: сначала `not`, потом `and`, потом `or`."),
    cod(f"{P}-m2-l1-e3", t("""
        Напиши функцию `can_login(login, password)`.

        Вход разрешён (`True`), только если **оба** условия выполнены:
        1. логин не пустая строка;
        2. в пароле 8 символов или больше.

        Примеры:
        ```
        can_login("anna", "12345678")   # → True
        can_login("anna", "123")        # → False
        can_login("", "supersecret")    # → False
        ```
        """),
        """
        def can_login(login, password):
            pass
        """,
        """
        def test_values():
            got = [can_login("anna", "12345678"), can_login("anna", "123"), can_login("", "supersecret")]
            assert got == [True, False, False], f"Получено {got}"
        """,
        """
        def can_login(login, password):
            return login != "" and len(password) >= 8
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `is_leap(year)` — високосный ли год.

        Правило: год високосный, если он делится на 4, **но не** на 100 — **или** если делится на 400.

        Примеры:
        ```
        is_leap(2024)   # → True
        is_leap(2023)   # → False
        is_leap(1900)   # → False   делится на 100, но не на 400
        is_leap(2000)   # → True    делится на 400
        ```
        """),
        """
        def is_leap(year):
            pass
        """,
        """
        def test_values():
            got = [is_leap(y) for y in (2024, 2023, 1900, 2000)]
            assert got == [True, False, False, True], f"Получено {got}"
        """,
        """
        def is_leap(year):
            return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
        """, xp=20),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `need_retry(status, attempt, max_attempts)` — нужно ли повторить запрос.

        Повторять (`True`), если выполнены **оба** условия:
        - статус — ошибка сервера (от 500 до 599 включительно) **или** статус `429` (слишком много запросов);
        - номер попытки `attempt` **меньше** `max_attempts`.

        Примеры:
        ```
        need_retry(503, 1, 3)   # → True
        need_retry(429, 2, 3)   # → True
        need_retry(503, 3, 3)   # → False   попытки кончились
        need_retry(404, 1, 3)   # → False   клиентская ошибка — повтор бессмысленен
        ```
        """),
        """
        def need_retry(status, attempt, max_attempts):
            pass
        """,
        """
        def test_values():
            got = [need_retry(503, 1, 3), need_retry(429, 2, 3), need_retry(503, 3, 3), need_retry(404, 1, 3), need_retry(200, 1, 3)]
            assert got == [True, True, False, False, False], f"Получено {got}"
        """,
        """
        def need_retry(status, attempt, max_attempts):
            return (500 <= status <= 599 or status == 429) and attempt < max_attempts
        """,
        hint="Скобки вокруг `or`-части обязательны: `and` выполняется раньше `or`.", xp=20),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `can_vote(age, is_citizen)` — может ли человек голосовать: ему **18 или больше** и он гражданин.

        Примеры:
        ```
        can_vote(20, True)    # → True
        can_vote(17, True)    # → False
        can_vote(30, False)   # → False
        ```
        """),
        """
        def can_vote(age, is_citizen):
            pass
        """,
        """
        def test_values():
            got = [can_vote(20, True), can_vote(18, True), can_vote(17, True), can_vote(30, False)]
            assert got == [True, True, False, False], f"Получено {got}"
        """,
        """
        def can_vote(age, is_citizen):
            return age >= 18 and is_citizen
        """),
    cod(f"{P}-m2-l1-e9", t("""
        Напиши функцию `is_triangle(a, b, c)` — можно ли составить треугольник из отрезков длиной `a`, `b`, `c`.
        Условие: **каждая** сторона меньше суммы двух других.

        Примеры:
        ```
        is_triangle(3, 4, 5)    # → True
        is_triangle(1, 2, 3)    # → False   1 + 2 не больше 3
        is_triangle(5, 1, 1)    # → False
        ```
        """),
        """
        def is_triangle(a, b, c):
            pass
        """,
        """
        def test_values():
            got = [is_triangle(3, 4, 5), is_triangle(1, 2, 3), is_triangle(5, 1, 1), is_triangle(2, 2, 2), is_triangle(1, 5, 1)]
            assert got == [True, False, False, True, False], f"Получено {got}"
        """,
        """
        def is_triangle(a, b, c):
            return a < b + c and b < a + c and c < a + b
        """)),

lesson(f"{P}-short", "Короткое замыкание и значения and/or",
    out(f"{P}-m2-l1-e2", "Что выведет программа? Короткое замыкание.", """
        def check(name, result):
            print("проверяю", name)
            return result

        print(check("A", False) and check("B", True))
        print(check("C", True) or check("D", True))
        """),
    out(f"{P}-short-e1", "Что выведет программа? `and` и `or` возвращают одно из значений.", """
        print(0 and 5)
        print(3 and 5)
        print("" or "x")
        print("a" or "b")
        """, hint="`and` возвращает первое ложное (или последнее), `or` — первое истинное (или последнее)."),
    out(f"{P}-short-e2", "Что выведет программа? Защита от None.", """
        name = None
        print(name is not None and name.upper())
        name = "аня"
        print(name is not None and name.upper())
        """, hint="Если левая часть `and` ложна, правая даже не вычисляется — поэтому нет ошибки у `None.upper()`."),
    cod(f"{P}-short-e3", t("""
        Напиши функцию `is_divisible(a, b)` — делится ли `a` на `b` нацело. Если `b` равно 0, вернуть `False`
        **без ошибки** деления на ноль. Реши одним выражением с `and`.

        Примеры:
        ```
        is_divisible(10, 5)   # → True
        is_divisible(10, 3)   # → False
        is_divisible(10, 0)   # → False
        ```
        """),
        """
        def is_divisible(a, b):
            pass
        """,
        """
        def test_values():
            got = [is_divisible(10, 5), is_divisible(10, 3), is_divisible(10, 0), is_divisible(0, 7)]
            assert got == [True, False, False, True], f"Получено {got}"
        """,
        """
        def is_divisible(a, b):
            return b != 0 and a % b == 0
        """,
        hint="Сначала проверь `b != 0`: если это ложь, `a % b` не выполнится."),
    cod(f"{P}-short-e4", t("""
        Напиши функцию `starts_with_capital(s)` — начинается ли строка с заглавной буквы.
        Для пустой строки вернуть `False` **без ошибки** (у пустой строки нет символа `s[0]`).

        Примеры:
        ```
        starts_with_capital("Москва")   # → True
        starts_with_capital("москва")   # → False
        starts_with_capital("")         # → False
        ```
        Метод `ch.isupper()` проверяет, что символ — заглавная буква.
        """),
        """
        def starts_with_capital(s):
            pass
        """,
        """
        def test_values():
            got = [starts_with_capital("Москва"), starts_with_capital("москва"), starts_with_capital(""), starts_with_capital("1abc")]
            assert got == [True, False, False, False], f"Получено {got}"
        """,
        """
        def starts_with_capital(s):
            return s != "" and s[0].isupper()
        """),
    cod(f"{P}-short-e5", t("""
        В функции `is_weekend2(day)` классическая ошибка: для любого дня она возвращает что-то истинное.
        Исправь её так, чтобы она возвращала `True` только для `"сб"` и `"вс"`.
        """),
        """
        def is_weekend2(day):
            return day == "сб" or "вс"
        """,
        """
        def test_values():
            got = [is_weekend2("сб"), is_weekend2("вс"), is_weekend2("пн")]
            assert got == [True, True, False], f"Получено {got!r}"
        """,
        """
        def is_weekend2(day):
            return day == "сб" or day == "вс"
        """,
        hint='`day == "сб" or "вс"` — это `(day == "сб") or "вс"`. Сравнивать нужно с каждым вариантом.'),
    cod(f"{P}-short-e6", t("""
        Напиши функцию `outside_range(x, low, high)` — лежит ли `x` **вне** отрезка от `low` до `high` (границы — внутри отрезка).

        Примеры:
        ```
        outside_range(0, 1, 10)    # → True
        outside_range(1, 1, 10)    # → False
        outside_range(11, 1, 10)   # → True
        ```
        Можно через `not (...)` или через `or`.
        """),
        """
        def outside_range(x, low, high):
            pass
        """,
        """
        def test_values():
            got = [outside_range(0, 1, 10), outside_range(1, 1, 10), outside_range(5, 1, 10), outside_range(10, 1, 10), outside_range(11, 1, 10)]
            assert got == [True, False, False, False, True], f"Получено {got}"
        """,
        """
        def outside_range(x, low, high):
            return x < low or x > high
        """),
    cod(f"{P}-short-e7", t("""
        Напиши функцию `pick_name(nickname, full_name)` — какое имя показать пользователю:
        ник, если он не пустой; иначе полное имя, если оно не пустое; иначе `"Гость"`. Реши одним выражением с `or`.

        Примеры:
        ```
        pick_name("anna_qa", "Анна Петрова")   # → "anna_qa"
        pick_name("", "Анна Петрова")          # → "Анна Петрова"
        pick_name("", "")                      # → "Гость"
        pick_name(None, "")                    # → "Гость"
        ```
        """),
        """
        def pick_name(nickname, full_name):
            pass
        """,
        """
        def test_values():
            got = [pick_name("anna_qa", "Анна Петрова"), pick_name("", "Анна Петрова"), pick_name("", ""), pick_name(None, "")]
            assert got == ["anna_qa", "Анна Петрова", "Гость", "Гость"], f"Получено {got}"
        """,
        """
        def pick_name(nickname, full_name):
            return nickname or full_name or "Гость"
        """)),

lesson(f"{P}-truth", "Истинность значений",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        for v in [0, "", "0", [], [0], None]:
            print(repr(v), bool(v))
        """),
    out(f"{P}-truth-e1", "Что выведет программа?", """
        print(bool(0), bool(-1))
        print(bool(0.0), bool(" "))
        print(bool("False"), bool(None))
        """, hint='Ложь — только ноль, пустое и None. Строка `"False"` не пустая.'),
    out(f"{P}-truth-e2", "Что выведет программа? Значение прямо в `if`.", """
        name = ""
        if name:
            print("есть имя")
        else:
            print("имя пустое")
        count = 0
        if count:
            print("есть")
        else:
            print("ноль")
        """),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `describe_list(items)`:

        - если список пустой — вернуть `"пусто"`;
        - иначе — `"<количество> шт."`.

        Проверку пустоты сделай через истинность (`if not items:`), а не через `len(items) == 0`.

        Примеры:
        ```
        describe_list([])          # → "пусто"
        describe_list([1, 2, 3])   # → "3 шт."
        ```
        """),
        """
        def describe_list(items):
            pass
        """,
        """
        def test_values():
            assert describe_list([]) == "пусто" and describe_list([1, 2, 3]) == "3 шт.", "Неверный результат"
        """,
        """
        def describe_list(items):
            if not items:
                return "пусто"
            return f"{len(items)} шт."
        """),
    cod(f"{P}-truth-e3", t("""
        Напиши функцию `has_text(s)` — есть ли в строке хоть что-то, **кроме пробелов**. Верни `True` или `False`.

        Примеры:
        ```
        has_text("привет")   # → True
        has_text("   ")      # → False
        has_text("")         # → False
        ```
        """),
        """
        def has_text(s):
            pass
        """,
        """
        def test_values():
            got = [has_text("привет"), has_text("   "), has_text(""), has_text(" a ")]
            assert got == [True, False, False, True], f"Получено {got!r}"
        """,
        """
        def has_text(s):
            return bool(s.strip())
        """,
        hint="`s.strip()` убирает пробелы; пустая строка — ложь. `bool(...)` превратит результат в True/False."),
    cod(f"{P}-truth-e4", t("""
        Напиши функцию `describe_value(v)`:

        - `None` → `"нет значения"`
        - любое другое **ложное** значение (`0`, `""`, `False`…) → `"пусто"`
        - истинное → `"есть"`

        Примеры:
        ```
        describe_value(None)   # → "нет значения"
        describe_value(0)      # → "пусто"
        describe_value("")     # → "пусто"
        describe_value(5)      # → "есть"
        ```
        Порядок проверок важен: `None` тоже ложен.
        """),
        """
        def describe_value(v):
            pass
        """,
        """
        def test_values():
            got = [describe_value(None), describe_value(0), describe_value(""), describe_value(False), describe_value(5), describe_value("0")]
            assert got == ["нет значения", "пусто", "пусто", "пусто", "есть", "есть"], f"Получено {got}"
        """,
        """
        def describe_value(v):
            if v is None:
                return "нет значения"
            if not v:
                return "пусто"
            return "есть"
        """),
    cod(f"{P}-truth-e5", t("""
        Напиши функцию `is_filled(name, email)` — заполнены ли оба поля формы (не пустые строки). Верни `True` или `False`.

        Примеры:
        ```
        is_filled("Аня", "a@b.ru")   # → True
        is_filled("Аня", "")         # → False
        is_filled("", "")            # → False
        ```
        """),
        """
        def is_filled(name, email):
            pass
        """,
        """
        def test_values():
            got = [is_filled("Аня", "a@b.ru"), is_filled("Аня", ""), is_filled("", "a@b.ru"), is_filled("", "")]
            assert got == [True, False, False, False], f"Получено {got!r}"
            assert is_filled("Аня", "a@b.ru") is True, "Верни именно True, а не строку"
        """,
        """
        def is_filled(name, email):
            return bool(name) and bool(email)
        """,
        hint="`name and email` вернёт одну из строк; оберни в `bool(...)`."),
    cod(f"{P}-truth-e6", t("""
        Напиши функцию `count_filled(a, b, c)` — сколько из трёх значений **истинны**.

        Примеры:
        ```
        count_filled("x", "", "y")   # → 2
        count_filled(0, None, "")    # → 0
        count_filled(1, [1], "0")    # → 3
        ```
        Пригодится то, что `True` — это 1, а `False` — 0.
        """),
        """
        def count_filled(a, b, c):
            pass
        """,
        """
        def test_values():
            got = [count_filled("x", "", "y"), count_filled(0, None, ""), count_filled(1, [1], "0")]
            assert got == [2, 0, 3], f"Получено {got}"
        """,
        """
        def count_filled(a, b, c):
            return bool(a) + bool(b) + bool(c)
        """)),

lesson(f"{P}-in", "Оператор in",
    out(f"{P}-m2-l2-e2", "Что выведет программа?", """
        print("сб" in ("сб", "вс"))
        print("err" in "ERROR: timeout")
        print(3 in [1, 2, 3])
        print("name" in {"name": "Аня"})
        """, hint="Для словаря `in` проверяет ключи."),
    out(f"{P}-in-e1", "Что выведет программа? `in` для строк и кортежей.", """
        print("py" in "python", "Py" in "python")
        print("" in "abc")
        print(3 in (1, 2, 3), 4 not in (1, 2, 3))
        """, hint="Пустая строка «содержится» в любой строке."),
    out(f"{P}-in-e2", "Что выведет программа? Тип элемента важен.", """
        codes = [200, 201, 204]
        print(201 in codes)
        print(404 not in codes)
        print("200" in codes)
        """, hint='Строка `"200"` и число `200` — разные значения.'),
    cod(f"{P}-m2-l2-e3", t("""
        Напиши функцию `is_weekend(day)`, которая принимает сокращение дня (`"пн"`, …, `"сб"`, `"вс"`) и возвращает `True` для субботы и воскресенья.

        Используй оператор `in`, а не цепочку `or`.

        Примеры:
        ```
        is_weekend("сб")   # → True
        is_weekend("пн")   # → False
        ```
        """),
        """
        def is_weekend(day):
            pass
        """,
        """
        def test_values():
            got = [is_weekend(d) for d in ("пн", "пт", "сб", "вс")]
            assert got == [False, False, True, True], f"Получено {got}"
        """,
        """
        def is_weekend(day):
            return day in ("сб", "вс")
        """),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `is_forbidden(word, banned)` — есть ли слово в списке запрещённых **без учёта регистра** и пробелов по краям.

        Примеры:
        ```
        is_forbidden(" Спам ", ["спам", "реклама"])   # → True
        is_forbidden("привет", ["спам"])             # → False
        ```
        Нормализуй слово: `word.strip().lower()`, затем проверь через `in`.
        """),
        """
        def is_forbidden(word, banned):
            pass
        """,
        """
        def test_values():
            assert is_forbidden(" Спам ", ["спам", "реклама"]) is True, "Регистр и пробелы не важны"
            assert is_forbidden("привет", ["спам"]) is False, "Разрешённое слово — False"
            assert is_forbidden("РЕКЛАМА", ["спам", "реклама"]) is True, "Заглавные тоже должны находиться"
        """,
        """
        def is_forbidden(word, banned):
            return word.strip().lower() in banned
        """),
    cod(f"{P}-in-e3", t("""
        Напиши функцию `is_vowel(ch)` — является ли символ гласной буквой (русской или английской), **без учёта регистра**.

        Гласные: `аеёиоуыэюя` и `aeiou`.

        Примеры:
        ```
        is_vowel("а")   # → True
        is_vowel("E")   # → True
        is_vowel("б")   # → False
        ```
        Проверь, входит ли символ в строку из гласных.
        """),
        """
        def is_vowel(ch):
            pass
        """,
        """
        def test_values():
            got = [is_vowel(c) for c in "аEбzЁо"]
            assert got == [True, True, False, False, True, True], f"Получено {got}"
        """,
        """
        def is_vowel(ch):
            return ch.lower() in "аеёиоуыэюяaeiou"
        """),
    cod(f"{P}-in-e4", t("""
        Напиши функцию `is_success(code)` — успешный ли ответ API: код равен `200`, `201` или `204`. Используй `in`.

        Примеры:
        ```
        is_success(201)   # → True
        is_success(404)   # → False
        ```
        """),
        """
        def is_success(code):
            pass
        """,
        """
        def test_values():
            got = [is_success(c) for c in (200, 201, 204, 202, 404)]
            assert got == [True, True, True, False, False], f"Получено {got}"

        def test_in():
            src = open("solution.py", encoding="utf-8").read()
            assert " in " in src, "Используй оператор in"
        """,
        """
        def is_success(code):
            return code in (200, 201, 204)
        """),
    cod(f"{P}-in-e5", t("""
        Напиши функцию `has_spam(text)` — встречается ли в тексте слово `"спам"` или `"реклама"` **без учёта регистра**.

        Примеры:
        ```
        has_spam("Это СПАМ!")         # → True
        has_spam("Реклама недели")    # → True
        has_spam("Привет, как дела")  # → False
        ```
        """),
        """
        def has_spam(text):
            pass
        """,
        """
        def test_values():
            got = [has_spam("Это СПАМ!"), has_spam("Реклама недели"), has_spam("Привет, как дела")]
            assert got == [True, True, False], f"Получено {got}"
        """,
        """
        def has_spam(text):
            low = text.lower()
            return "спам" in low or "реклама" in low
        """)),

lesson(f"{P}-m2-l3", "Вложенные условия и ранний выход",
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        age, has_ticket = 20, False
        if age >= 18:
            if has_ticket:
                print("проходите")
            else:
                print("купите билет")
        else:
            print("только со взрослыми")
        """),
    out(f"{P}-m2-l3-e2", "Что выведет программа?", """
        def access(role, active):
            if not active:
                return "заблокирован"
            if role == "admin":
                return "полный доступ"
            return "обычный доступ"

        print(access("admin", False))
        print(access("admin", True))
        print(access("qa", True))
        """),
    out(f"{P}-m2-l3-e6", "Что выведет программа?", """
        def check(x):
            if x > 0:
                if x % 2 == 0:
                    return "положительное чётное"
                return "положительное нечётное"
            return "не положительное"

        print(check(4))
        print(check(3))
        print(check(-2))
        """),
    cod(f"{P}-m2-l3-e3", t("""
        Напиши функцию `ticket_price(age, is_student)` — цена билета в музей:

        - младше 7 лет — `0`;
        - от 7 до 17 включительно — `150`;
        - от 18 и старше — `300`, **но** студентам — `200`.

        Примеры:
        ```
        ticket_price(5, False)    # → 0
        ticket_price(12, False)   # → 150
        ticket_price(20, True)    # → 200
        ticket_price(40, False)   # → 300
        ```
        """),
        """
        def ticket_price(age, is_student):
            pass
        """,
        """
        def test_values():
            got = [ticket_price(5, False), ticket_price(7, False), ticket_price(17, True), ticket_price(18, False), ticket_price(20, True), ticket_price(40, False)]
            assert got == [0, 150, 150, 300, 200, 300], f"Получено {got}"
        """,
        """
        def ticket_price(age, is_student):
            if age < 7:
                return 0
            if age < 18:
                return 150
            return 200 if is_student else 300
        """, xp=20),
    cod(f"{P}-m2-l3-e4", t("""
        Перепиши функцию `validate(password)` **без вложенных if** — через ранние `return`.

        Правила (проверять по порядку, вернуть первое нарушение):
        1. длина меньше 8 → `"короткий"`;
        2. нет ни одной цифры → `"нет цифр"`;
        3. всё в нижнем регистре (`password == password.lower()`) → `"нет заглавных"`;
        4. иначе → `"ok"`.

        Проверь, что поведение не изменилось, и что в коде нет `else`.
        """),
        """
        def validate(password):
            if len(password) >= 8:
                if any(ch.isdigit() for ch in password):
                    if password != password.lower():
                        return "ok"
                    else:
                        return "нет заглавных"
                else:
                    return "нет цифр"
            else:
                return "короткий"
        """,
        """
        def test_values():
            got = [validate(p) for p in ("abc", "abcdefgh", "abcdefg1", "Abcdefg1")]
            assert got == ["короткий", "нет цифр", "нет заглавных", "ok"], f"Получено {got}"

        def test_flat():
            src = open("solution.py", encoding="utf-8").read()
            assert "else" not in src, "Избавься от else — используй ранние return"
        """,
        """
        def validate(password):
            if len(password) < 8:
                return "короткий"
            if not any(ch.isdigit() for ch in password):
                return "нет цифр"
            if password == password.lower():
                return "нет заглавных"
            return "ok"
        """,
        hint="Проверяй «плохие» случаи и сразу возвращай ошибку; в конце — `return \"ok\"`.", xp=20),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `bug_priority(severity, users_affected)`, которая определяет приоритет бага:

        - `severity == "critical"` → `"P1"` (всегда);
        - `severity == "major"` и затронуто **больше 100** пользователей → `"P1"`;
        - `severity == "major"` → `"P2"`;
        - любая другая серьёзность → `"P3"`.

        Примеры:
        ```
        bug_priority("critical", 1)   # → "P1"
        bug_priority("major", 500)    # → "P1"
        bug_priority("major", 10)     # → "P2"
        bug_priority("minor", 1000)   # → "P3"
        ```
        """),
        """
        def bug_priority(severity, users_affected):
            pass
        """,
        """
        def test_values():
            got = [bug_priority("critical", 1), bug_priority("major", 500), bug_priority("major", 100), bug_priority("minor", 1000)]
            assert got == ["P1", "P1", "P2", "P3"], f"Получено {got}"
        """,
        """
        def bug_priority(severity, users_affected):
            if severity == "critical":
                return "P1"
            if severity == "major":
                return "P1" if users_affected > 100 else "P2"
            return "P3"
        """),
    cod(f"{P}-m2-l3-e7", t("""
        Напиши функцию `login_message(user_exists, is_blocked, password_ok)` через **ранние return**. Проверки по порядку:

        1. пользователя нет → `"нет такого пользователя"`
        2. заблокирован → `"заблокирован"`
        3. неверный пароль → `"неверный пароль"`
        4. иначе → `"добро пожаловать"`

        Примеры:
        ```
        login_message(False, False, True)   # → "нет такого пользователя"
        login_message(True, True, True)     # → "заблокирован"
        login_message(True, False, False)   # → "неверный пароль"
        login_message(True, False, True)    # → "добро пожаловать"
        ```
        """),
        """
        def login_message(user_exists, is_blocked, password_ok):
            pass
        """,
        """
        def test_values():
            got = [login_message(False, False, True), login_message(False, True, False), login_message(True, True, True),
                   login_message(True, True, False), login_message(True, False, False), login_message(True, False, True)]
            assert got == ["нет такого пользователя", "нет такого пользователя", "заблокирован", "заблокирован",
                           "неверный пароль", "добро пожаловать"], f"Получено {got}"
        """,
        """
        def login_message(user_exists, is_blocked, password_ok):
            if not user_exists:
                return "нет такого пользователя"
            if is_blocked:
                return "заблокирован"
            if not password_ok:
                return "неверный пароль"
            return "добро пожаловать"
        """),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `triangle_type(a, b, c)`:

        - если из сторон нельзя составить треугольник (какая-то сторона не меньше суммы двух других) → `"не треугольник"`
        - все три стороны равны → `"равносторонний"`
        - какие-то две равны → `"равнобедренный"`
        - иначе → `"разносторонний"`

        Примеры:
        ```
        triangle_type(1, 2, 3)   # → "не треугольник"
        triangle_type(2, 2, 2)   # → "равносторонний"
        triangle_type(2, 2, 3)   # → "равнобедренный"
        triangle_type(3, 4, 5)   # → "разносторонний"
        ```
        """),
        """
        def triangle_type(a, b, c):
            pass
        """,
        """
        def test_values():
            got = [triangle_type(1, 2, 3), triangle_type(2, 2, 2), triangle_type(2, 2, 3), triangle_type(3, 2, 3),
                   triangle_type(2, 3, 3), triangle_type(3, 4, 5)]
            assert got == ["не треугольник", "равносторонний", "равнобедренный", "равнобедренный", "равнобедренный",
                           "разносторонний"], f"Получено {got}"
        """,
        """
        def triangle_type(a, b, c):
            if a >= b + c or b >= a + c or c >= a + b:
                return "не треугольник"
            if a == b == c:
                return "равносторонний"
            if a == b or b == c or a == c:
                return "равнобедренный"
            return "разносторонний"
        """, xp=20)),
)
