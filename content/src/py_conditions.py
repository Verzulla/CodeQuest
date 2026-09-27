"""Тема «Условные операторы»."""
from ._lib import cod, lesson, module, out, t, topic

P = "cnd"

# ============================================================
m1 = module(f"{P}-m1", "if и сравнения", "⚖️", "if/else, операторы сравнения и elif",

lesson(f"{P}-m1-l1", "if и else", 
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        t = 25
        if t > 20:
            print("жарко")
        else:
            print("прохладно")
        print("конец")
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа? Внимание на отступы.", """
        x = 3
        if x > 5:
            print("A")
            print("B")
        print("C")
        """, hint="«A» и «B» внутри if, «C» — снаружи."),
    cod(f"{P}-m1-l1-e3", t("""
        Напиши функцию `is_adult(age)`, которая проверяет совершеннолетие.

        - Возвращает `True`, если возраст **18 или больше**, иначе `False`.

        Примеры:
        ```
        is_adult(30)   # → True
        is_adult(10)   # → False
        is_adult(18)   # → True
        ```
        """),
        """
        def is_adult(age):
            pass
        """,
        """
        def test_values():
            got = [is_adult(a) for a in (30, 10, 18, 17)]
            assert got == [True, False, True, False], f"Получено {got} — проверь границу 18"
        """,
        """
        def is_adult(age):
            return age >= 18
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `max2(a, b)`, которая возвращает большее из двух чисел, **без** встроенной `max`.

        Примеры:
        ```
        max2(5, 3)    # → 5
        max2(-1, 8)   # → 8
        max2(4, 4)    # → 4
        ```
        """),
        """
        def max2(a, b):
            pass
        """,
        """
        def test_values():
            assert [max2(5, 3), max2(-1, 8), max2(4, 4)] == [5, 8, 4], "Неверный максимум"

        def test_no_max():
            assert "max(" not in open("solution.py", encoding="utf-8").read().replace("max2(", ""), "Не используй встроенную max"
        """,
        """
        def max2(a, b):
            if a > b:
                return a
            return b
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `check_status(code)` для проверки ответа API.

        - Если `code` равен `200` — вернуть строку `"OK"`.
        - Иначе — вернуть `"FAIL: <код>"`, например `"FAIL: 404"`.

        Примеры:
        ```
        check_status(200)   # → "OK"
        check_status(500)   # → "FAIL: 500"
        ```
        """),
        """
        def check_status(code):
            pass
        """,
        """
        def test_values():
            assert check_status(200) == "OK", "200 → OK"
            assert check_status(404) == "FAIL: 404" and check_status(500) == "FAIL: 500", "Иначе — FAIL: код"
        """,
        """
        def check_status(code):
            if code == 200:
                return "OK"
            else:
                return f"FAIL: {code}"
        """)),

lesson(f"{P}-m1-l2", "Операторы сравнения", 
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        print(5 == 5.0, 5 != 6)
        print(3 < 7 < 10, 3 < 7 > 10)
        print("apple" < "banana", "Z" < "a")
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа? Сравнение строк с числами.", """
        print("10" == 10)
        print("10" < "9")
        print(int("10") < int("9"))
        """, hint="Строки сравниваются посимвольно: `\"1\"` меньше `\"9\"`."),
    cod(f"{P}-m1-l2-e3", t("""
        Напиши функцию `in_range(x, low, high)` — лежит ли `x` в отрезке **от `low` до `high` включительно**.

        Используй цепочку сравнений.

        Примеры:
        ```
        in_range(5, 1, 10)    # → True
        in_range(10, 1, 10)   # → True   граница входит
        in_range(0, 1, 10)    # → False
        ```
        """),
        """
        def in_range(x, low, high):
            pass
        """,
        """
        def test_values():
            got = [in_range(5, 1, 10), in_range(10, 1, 10), in_range(1, 1, 10), in_range(0, 1, 10), in_range(11, 1, 10)]
            assert got == [True, True, True, False, False], f"Получено {got}"
        """,
        """
        def in_range(x, low, high):
            return low <= x <= high
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `is_valid_port(port)` — проверка номера порта.

        Порт корректен, если это целое число от **1 до 65535** включительно.

        Примеры:
        ```
        is_valid_port(8080)    # → True
        is_valid_port(0)       # → False
        is_valid_port(65536)   # → False
        ```
        """),
        """
        def is_valid_port(port):
            pass
        """,
        """
        def test_values():
            got = [is_valid_port(p) for p in (8080, 1, 65535, 0, 65536, -1)]
            assert got == [True, True, True, False, False, False], f"Получено {got}"
        """,
        """
        def is_valid_port(port):
            return 1 <= port <= 65535
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `compare_versions(a, b)` для версий вида `"1.10"` и `"1.9"` (ровно две части через точку).

        - Возвращает `-1`, если `a` меньше `b`; `1`, если больше; `0`, если равны.
        - Сравнивать нужно **как числа**, а не как строки: `1.10` больше `1.9`.

        Примеры:
        ```
        compare_versions("1.10", "1.9")   # → 1
        compare_versions("2.0", "2.0")    # → 0
        compare_versions("0.9", "1.0")    # → -1
        ```
        Подсказка: `tuple(int(p) for p in a.split("."))` превращает `"1.10"` в `(1, 10)`, а кортежи сравниваются поэлементно.
        """),
        """
        def compare_versions(a, b):
            pass
        """,
        """
        def test_values():
            got = [compare_versions("1.10", "1.9"), compare_versions("2.0", "2.0"), compare_versions("0.9", "1.0")]
            assert got == [1, 0, -1], f"Получено {got}"
        """,
        """
        def compare_versions(a, b):
            va = tuple(int(p) for p in a.split("."))
            vb = tuple(int(p) for p in b.split("."))
            if va < vb:
                return -1
            if va > vb:
                return 1
            return 0
        """, xp=20)),

lesson(f"{P}-m1-l3", "elif — много вариантов", 
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        n = 15
        if n > 10:
            print("A")
        elif n > 5:
            print("B")
        else:
            print("C")
        """, hint="Сработает только первая подходящая ветка."),
    out(f"{P}-m1-l3-e2", "Что выведет программа? Здесь два отдельных if.", """
        n = 15
        if n > 10:
            print("A")
        if n > 5:
            print("B")
        """),
    cod(f"{P}-m1-l3-e3", t("""
        Напиши функцию `sign(n)`, которая называет знак числа.

        - `"плюс"` — если больше нуля;
        - `"минус"` — если меньше нуля;
        - `"ноль"` — если равно нулю.

        Примеры:
        ```
        sign(5)    # → "плюс"
        sign(-3)   # → "минус"
        sign(0)    # → "ноль"
        ```
        """),
        """
        def sign(n):
            pass
        """,
        """
        def test_values():
            assert [sign(5), sign(-3), sign(0)] == ["плюс", "минус", "ноль"], "Неверный знак"
        """,
        """
        def sign(n):
            if n > 0:
                return "плюс"
            elif n < 0:
                return "минус"
            return "ноль"
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `grade(score)`, которая переводит баллы (0–100) в оценку:

        - 90 и больше → `"A"`
        - от 75 до 89 → `"B"`
        - от 60 до 74 → `"C"`
        - меньше 60 → `"F"`

        Примеры:
        ```
        grade(95)   # → "A"
        grade(75)   # → "B"
        grade(59)   # → "F"
        ```
        """),
        """
        def grade(score):
            pass
        """,
        """
        def test_values():
            got = [grade(s) for s in (95, 90, 89, 75, 74, 60, 59, 0)]
            assert got == ["A", "A", "B", "B", "C", "C", "F", "F"], f"Получено {got}"
        """,
        """
        def grade(score):
            if score >= 90:
                return "A"
            elif score >= 75:
                return "B"
            elif score >= 60:
                return "C"
            return "F"
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Классика собеседований — FizzBuzz. Напиши функцию `fizzbuzz(n)`, которая возвращает **строку**:

        - `"FizzBuzz"` — если `n` делится и на 3, и на 5;
        - `"Fizz"` — если делится только на 3;
        - `"Buzz"` — если делится только на 5;
        - иначе — само число строкой: `str(n)`.

        Примеры:
        ```
        fizzbuzz(9)    # → "Fizz"
        fizzbuzz(10)   # → "Buzz"
        fizzbuzz(30)   # → "FizzBuzz"
        fizzbuzz(7)    # → "7"
        ```
        """),
        """
        def fizzbuzz(n):
            pass
        """,
        """
        def test_values():
            got = [fizzbuzz(n) for n in (9, 10, 30, 7, 15)]
            assert got == ["Fizz", "Buzz", "FizzBuzz", "7", "FizzBuzz"], f"Получено {got} — проверь порядок условий"
        """,
        """
        def fizzbuzz(n):
            if n % 15 == 0:
                return "FizzBuzz"
            elif n % 3 == 0:
                return "Fizz"
            elif n % 5 == 0:
                return "Buzz"
            return str(n)
        """,
        hint="Проверку «на 3 и 5 одновременно» (`n % 15 == 0`) ставь первой.", xp=20)),
)

# ============================================================
m2 = module(f"{P}-m2", "Логика", "🧠", "and, or, not, истинность и вложенные условия",

lesson(f"{P}-m2-l1", "and, or, not", 
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        print(True and False, True or False, not True)
        print(True or False and False)
        print((True or False) and False)
        """, hint="`and` выполняется раньше `or`."),
    out(f"{P}-m2-l1-e2", "Что выведет программа? Короткое замыкание.", """
        def check(name, result):
            print("проверяю", name)
            return result

        print(check("A", False) and check("B", True))
        print(check("C", True) or check("D", True))
        """),
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
        hint="Скобки вокруг `or`-части обязательны: `and` выполняется раньше `or`.", xp=20)),

lesson(f"{P}-m2-l2", "Истинность и оператор in", 
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        for v in [0, "", "0", [], [0], None]:
            print(repr(v), bool(v))
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа?", """
        print("сб" in ("сб", "вс"))
        print("err" in "ERROR: timeout")
        print(3 in [1, 2, 3])
        print("name" in {"name": "Аня"})
        """, hint="Для словаря `in` проверяет ключи."),
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
        """)),
)

# ============================================================
m3 = module(f"{P}-m3", "Короткие условия", "⚡", "Тернарный оператор, значения по умолчанию и match",

lesson(f"{P}-m3-l1", "Тернарный оператор", 
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        x = -5
        print("плюс" if x > 0 else "не плюс")
        print(x if x > 0 else -x)
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа? Вложенный тернарник.", """
        for x in [5, 0, -2]:
            print("плюс" if x > 0 else "минус" if x < 0 else "ноль")
        """),
    cod(f"{P}-m3-l1-e3", t("""
        Перепиши функцию `parity(n)` так, чтобы тело было **одной строкой** `return ... if ... else ...`.

        Поведение не меняется:
        ```
        parity(4)   # → "чёт"
        parity(7)   # → "нечет"
        ```
        """),
        """
        def parity(n):
            if n % 2 == 0:
                return "чёт"
            else:
                return "нечет"
        """,
        """
        import inspect

        def test_values():
            assert parity(4) == "чёт" and parity(7) == "нечет", "parity(4) → чёт, parity(7) → нечет"

        def test_one_line():
            body = [l for l in inspect.getsource(parity).splitlines()[1:] if l.strip()]
            assert len(body) == 1 and " if " in body[0] and " else " in body[0], "Тело — одна строка с тернарником"
        """,
        """
        def parity(n):
            return "чёт" if n % 2 == 0 else "нечет"
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `plural_bugs(n)`, которая склоняет слово «баг» после числа (для чисел 0–20):

        - `1` → `"1 баг"`;
        - `2`–`4` → `"N бага"`;
        - `0`, `5`–`20` → `"N багов"`.

        Выбери форму слова тернарником (можно вложенным), результат собери f-строкой.

        Примеры:
        ```
        plural_bugs(1)    # → "1 баг"
        plural_bugs(3)    # → "3 бага"
        plural_bugs(12)   # → "12 багов"
        ```
        """),
        """
        def plural_bugs(n):
            pass
        """,
        """
        def test_values():
            got = [plural_bugs(n) for n in (0, 1, 2, 4, 5, 12)]
            assert got == ["0 багов", "1 баг", "2 бага", "4 бага", "5 багов", "12 багов"], f"Получено {got}"
        """,
        """
        def plural_bugs(n):
            word = "баг" if n == 1 else "бага" if 2 <= n <= 4 else "багов"
            return f"{n} {word}"
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `clamp(x, low, high)`, которая «зажимает» число в границы — как ползунок громкости:

        - меньше `low` → вернуть `low`;
        - больше `high` → вернуть `high`;
        - иначе — само `x`.

        Реши одной строкой с вложенным тернарником.

        Примеры:
        ```
        clamp(5, 0, 10)    # → 5
        clamp(-3, 0, 10)   # → 0
        clamp(42, 0, 10)   # → 10
        ```
        """),
        """
        def clamp(x, low, high):
            pass
        """,
        """
        def test_values():
            got = [clamp(5, 0, 10), clamp(-3, 0, 10), clamp(42, 0, 10), clamp(0, 0, 10)]
            assert got == [5, 0, 10, 0], f"Получено {got}"
        """,
        """
        def clamp(x, low, high):
            return low if x < low else high if x > high else x
        """)),

lesson(f"{P}-m3-l2", "Значения по умолчанию: or и is None", 
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        print("" or "Гость")
        print("Аня" or "Гость")
        print(0 or 10)
        print(None or 0 or "последний")
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа? Ловушка с нулём.", """
        timeout = 0
        a = timeout or 30
        b = 30 if timeout is None else timeout
        print(a, b)
        """),
    cod(f"{P}-m3-l2-e3", t("""
        Напиши функцию `display_name(name)`:

        - вернуть `name`, если это непустая строка;
        - если `name` — пустая строка или `None`, вернуть `"Аноним"`.

        Реши одной строкой через `or`.

        Примеры:
        ```
        display_name("Вася")   # → "Вася"
        display_name("")       # → "Аноним"
        display_name(None)     # → "Аноним"
        ```
        """),
        """
        def display_name(name):
            pass
        """,
        """
        def test_values():
            assert [display_name("Вася"), display_name(""), display_name(None)] == ["Вася", "Аноним", "Аноним"], "Неверный результат"
        """,
        """
        def display_name(name):
            return name or "Аноним"
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши функцию `get_timeout(value)`:

        - если `value is None` — вернуть `30`;
        - иначе — само значение, **даже если это `0`** (ноль — осознанный выбор «без ожидания»).

        Примеры:
        ```
        get_timeout(None)   # → 30
        get_timeout(5)      # → 5
        get_timeout(0)      # → 0
        ```
        """),
        """
        def get_timeout(value):
            pass
        """,
        """
        def test_values():
            assert get_timeout(None) == 30 and get_timeout(5) == 5, "None → 30, 5 → 5"
            assert get_timeout(0) == 0, "0 должен остаться 0 — не используй or"
        """,
        """
        def get_timeout(value):
            return 30 if value is None else value
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `get_setting(config, key, default)`, которая достаёт настройку из словаря:

        - если ключа нет или значение равно `None` — вернуть `default`;
        - иначе вернуть значение (в том числе `0`, `False`, `""`).

        Примеры:
        ```
        cfg = {"retries": 0, "browser": None, "headless": False}
        get_setting(cfg, "retries", 3)       # → 0
        get_setting(cfg, "browser", "chrome")  # → "chrome"
        get_setting(cfg, "timeout", 30)      # → 30
        get_setting(cfg, "headless", True)   # → False
        ```
        `config.get(key)` вернёт `None`, если ключа нет.
        """),
        """
        def get_setting(config, key, default):
            pass
        """,
        """
        def test_values():
            cfg = {"retries": 0, "browser": None, "headless": False}
            got = [get_setting(cfg, "retries", 3), get_setting(cfg, "browser", "chrome"), get_setting(cfg, "timeout", 30), get_setting(cfg, "headless", True)]
            assert got == [0, "chrome", 30, False], f"Получено {got}"
        """,
        """
        def get_setting(config, key, default):
            value = config.get(key)
            return default if value is None else value
        """, xp=20)),

lesson(f"{P}-m3-l3", "match / case", 
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        def handle(cmd):
            match cmd:
                case "start":
                    return "запуск"
                case "stop" | "exit":
                    return "остановка"
                case _:
                    return "неизвестно"

        print(handle("start"), handle("exit"), handle("pause"))
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа? match умеет разбирать списки.", """
        def describe(point):
            match point:
                case [0, 0]:
                    return "начало координат"
                case [x, 0]:
                    return f"на оси X, x={x}"
                case [x, y]:
                    return f"точка {x}, {y}"

        print(describe([0, 0]))
        print(describe([5, 0]))
        print(describe([2, 3]))
        """),
    cod(f"{P}-m3-l3-e3", t("""
        Напиши функцию `http_method_action(method)` через `match/case`:

        - `"GET"` → `"читать"`
        - `"POST"` → `"создать"`
        - `"PUT"` или `"PATCH"` → `"изменить"`
        - `"DELETE"` → `"удалить"`
        - любой другой → `"неизвестно"`

        Используй `|` для объединения вариантов и `_` для «остального».
        """),
        """
        def http_method_action(method):
            pass
        """,
        """
        def test_values():
            got = [http_method_action(m) for m in ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD")]
            assert got == ["читать", "создать", "изменить", "изменить", "удалить", "неизвестно"], f"Получено {got}"

        def test_uses_match():
            assert "match " in open("solution.py", encoding="utf-8").read(), "Используй match/case"
        """,
        """
        def http_method_action(method):
            match method:
                case "GET":
                    return "читать"
                case "POST":
                    return "создать"
                case "PUT" | "PATCH":
                    return "изменить"
                case "DELETE":
                    return "удалить"
                case _:
                    return "неизвестно"
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `classify_response(resp)` для словаря-ответа API через `match/case` с **шаблонами словарей**:

        - `{"status": 200, "data": ...}` → вернуть значение `data`;
        - `{"status": 404}` → `"не найдено"`;
        - `{"status": код}`, где код ≥ 500 → `"ошибка сервера <код>"` (используй `case {"status": code} if code >= 500:`);
        - всё остальное → `"неожиданный ответ"`.

        Примеры:
        ```
        classify_response({"status": 200, "data": [1, 2]})   # → [1, 2]
        classify_response({"status": 404})                   # → "не найдено"
        classify_response({"status": 503})                   # → "ошибка сервера 503"
        classify_response({"status": 302})                   # → "неожиданный ответ"
        ```
        """),
        """
        def classify_response(resp):
            pass
        """,
        """
        def test_values():
            got = [classify_response({"status": 200, "data": [1, 2]}), classify_response({"status": 404}),
                   classify_response({"status": 503}), classify_response({"status": 302}), classify_response({})]
            assert got == [[1, 2], "не найдено", "ошибка сервера 503", "неожиданный ответ", "неожиданный ответ"], f"Получено {got}"
        """,
        """
        def classify_response(resp):
            match resp:
                case {"status": 200, "data": data}:
                    return data
                case {"status": 404}:
                    return "не найдено"
                case {"status": code} if code >= 500:
                    return f"ошибка сервера {code}"
                case _:
                    return "неожиданный ответ"
        """,
        hint="Шаблон `{\"status\": 200, \"data\": data}` сразу кладёт значение в переменную `data`. Условие после шаблона — `if`.", xp=25),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `parse_command(text)`, которая разбирает текстовую команду через `match` по **списку слов** (`text.split()`):

        - `["go", направление]` → `"иду: <направление>"`
        - `["take", предмет]` → `"беру: <предмет>"`
        - `["look"]` → `"осматриваюсь"`
        - всё остальное → `"не понимаю"`

        Примеры:
        ```
        parse_command("go north")   # → "иду: north"
        parse_command("take key")   # → "беру: key"
        parse_command("look")       # → "осматриваюсь"
        parse_command("dance now please")  # → "не понимаю"
        ```
        """),
        """
        def parse_command(text):
            pass
        """,
        """
        def test_values():
            got = [parse_command(s) for s in ("go north", "take key", "look", "dance now please", "")]
            assert got == ["иду: north", "беру: key", "осматриваюсь", "не понимаю", "не понимаю"], f"Получено {got}"
        """,
        """
        def parse_command(text):
            match text.split():
                case ["go", direction]:
                    return f"иду: {direction}"
                case ["take", item]:
                    return f"беру: {item}"
                case ["look"]:
                    return "осматриваюсь"
                case _:
                    return "не понимаю"
        """, xp=20)),
)

TOPIC = topic("py-conditions", "Условные операторы", "🔀", "#ff9600",
              "if/elif/else, логика, истинность, тернарный оператор и match",
              m1, m2, m3, group="Python")
