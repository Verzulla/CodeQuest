"""Тема «Условные операторы», модули 3 «Короткие записи» и 4 «match / case» — задания.
Теория — в _cnd_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "cnd"

m3 = module(f"{P}-m3", "Короткие записи", "⚡", "Тернарный оператор, значения по умолчанию, min/max/abs и :=",

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
    out(f"{P}-m3-l1-e6", "Что выведет программа?", """
        x = 0
        print("да" if x else "нет")
        print("плюс" if x >= 0 else "минус")
        print(f"{x} — {'чётное' if x % 2 == 0 else 'нечётное'}")
        """, hint="Ноль ложен, но `0 >= 0` — истина."),
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
        """),
    cod(f"{P}-m3-l1-e7", t("""
        Напиши функцию `status_text(passed)`, которая одной строкой с тернарным оператором возвращает
        `"✅ пройден"` для `True` и `"❌ упал"` для `False`.
        """),
        """
        def status_text(passed):
            pass
        """,
        """
        def test_values():
            assert status_text(True) == "✅ пройден" and status_text(False) == "❌ упал", f"Получено {status_text(True)!r}, {status_text(False)!r}"

        def test_ternary():
            src = open("solution.py", encoding="utf-8").read()
            assert " if " in src and " else " in src and "return" in src, "Используй return ... if ... else ..."
        """,
        """
        def status_text(passed):
            return "✅ пройден" if passed else "❌ упал"
        """),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `files_label(n)` — подпись для количества файлов:
        `"1 файл"` для единицы и `"<n> файлов"` для всех остальных чисел. Форму слова выбери тернарником внутри f-строки.

        Примеры:
        ```
        files_label(1)    # → "1 файл"
        files_label(7)    # → "7 файлов"
        files_label(0)    # → "0 файлов"
        ```
        """),
        """
        def files_label(n):
            pass
        """,
        """
        def test_values():
            got = [files_label(1), files_label(7), files_label(0)]
            assert got == ["1 файл", "7 файлов", "0 файлов"], f"Получено {got}"
        """,
        """
        def files_label(n):
            return f"{n} {'файл' if n == 1 else 'файлов'}"
        """,
        hint="""Внутри f-строки в двойных кавычках используй одинарные: `{'файл' if n == 1 else 'файлов'}`.""")),

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
    out(f"{P}-m3-l2-e6", "Что выведет программа? `get` у словаря.", """
        config = {"debug": None, "retries": 0}
        print(config.get("level", "INFO"))
        print(config.get("debug", True))
        print(config.get("retries") or 3)
        """, hint="`get(key, default)` подставит default, только если ключа нет."),
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
        """, xp=20),
    cod(f"{P}-m3-l2-e7", t("""
        Напиши функцию `greet_user(name=None)` с **необязательным** параметром:
        если имя не передано, `None` или пустая строка — приветствовать `"Гость"`.

        Примеры:
        ```
        greet_user("Аня")   # → "Привет, Аня!"
        greet_user("")      # → "Привет, Гость!"
        greet_user()        # → "Привет, Гость!"
        ```
        """),
        """
        def greet_user(name=None):
            pass
        """,
        """
        def test_values():
            got = [greet_user("Аня"), greet_user(""), greet_user(), greet_user(None)]
            assert got == ["Привет, Аня!", "Привет, Гость!", "Привет, Гость!", "Привет, Гость!"], f"Получено {got}"
        """,
        """
        def greet_user(name=None):
            return f"Привет, {name or 'Гость'}!"
        """),
    cod(f"{P}-m3-l2-e8", t("""
        Напиши функцию `page_size(value, default=20)`: если `value` не задано (`None`) — вернуть `default`,
        иначе само значение, **в том числе 0**.

        Примеры:
        ```
        page_size(None)        # → 20
        page_size(50)          # → 50
        page_size(0)           # → 0
        page_size(None, 100)   # → 100
        ```
        """),
        """
        def page_size(value, default=20):
            pass
        """,
        """
        def test_values():
            got = [page_size(None), page_size(50), page_size(0), page_size(None, 100)]
            assert got == [20, 50, 0, 100], f"Получено {got}"
        """,
        """
        def page_size(value, default=20):
            return default if value is None else value
        """)),

lesson(f"{P}-noif", "Условия без if: min, max, abs и :=",
    out(f"{P}-noif-e1", "Что выведет программа?", """
        print(max(3, 7), min(3, 7))
        print(max(-1, -5), abs(-4))
        print(max(2, 9, 4, 1))
        """),
    out(f"{P}-noif-e2", "Что выведет программа? min и max для строк и смешанных чисел.", """
        print(max("apple", "Banana"))
        print(min(2.5, 2))
        print(max("кот", "Кит"))
        """, hint="Строки сравниваются по кодам символов: строчные латинские буквы «больше» заглавных."),
    out(f"{P}-noif-e3", "Что выведет программа? Оператор `:=` присваивает прямо в условии.", """
        text = "hello world"
        if (n := len(text)) > 5:
            print(f"длинная строка: {n}")
        print(n)
        """),
    cod(f"{P}-noif-e4", t("""
        Напиши функцию `clamp2(x, low, high)` — зажать число в границы **без `if`**, с помощью `min` и `max`.

        Примеры:
        ```
        clamp2(5, 0, 10)    # → 5
        clamp2(-3, 0, 10)   # → 0
        clamp2(42, 0, 10)   # → 10
        ```
        """),
        """
        def clamp2(x, low, high):
            pass
        """,
        """
        def test_values():
            got = [clamp2(5, 0, 10), clamp2(-3, 0, 10), clamp2(42, 0, 10), clamp2(0, 0, 10), clamp2(10, 0, 10)]
            assert got == [5, 0, 10, 0, 10], f"Получено {got}"

        def test_no_if():
            src = open("solution.py", encoding="utf-8").read()
            assert "if" not in src, "Реши без if — через min и max"
        """,
        """
        def clamp2(x, low, high):
            return max(low, min(x, high))
        """,
        hint="`min(x, high)` не даст выйти за верх, `max(low, ...)` — за низ."),
    cod(f"{P}-noif-e5", t("""
        Напиши функцию `bigger_abs(a, b)` — из двух чисел вернуть то, у которого **больше модуль** (дальше от нуля).
        При равных модулях вернуть `a`.

        Примеры:
        ```
        bigger_abs(3, -7)   # → -7
        bigger_abs(-2, 1)   # → -2
        bigger_abs(4, -4)   # → 4
        ```
        """),
        """
        def bigger_abs(a, b):
            pass
        """,
        """
        def test_values():
            got = [bigger_abs(3, -7), bigger_abs(-2, 1), bigger_abs(4, -4), bigger_abs(0, 0)]
            assert got == [-7, -2, 4, 0], f"Получено {got}"
        """,
        """
        def bigger_abs(a, b):
            return a if abs(a) >= abs(b) else b
        """),
    cod(f"{P}-noif-e6", t("""
        Напиши функцию `bonus(passed, perfect)` — бонус за урок: 10 очков, если урок пройден, плюс 5, если без ошибок.
        Реши **без `if`**, пользуясь тем, что `True` — это 1, а `False` — 0.

        Примеры:
        ```
        bonus(True, True)     # → 15
        bonus(True, False)    # → 10
        bonus(False, False)   # → 0
        ```
        """),
        """
        def bonus(passed, perfect):
            pass
        """,
        """
        def test_values():
            got = [bonus(True, True), bonus(True, False), bonus(False, False), bonus(False, True)]
            assert got == [15, 10, 0, 5], f"Получено {got}"

        def test_no_if():
            src = open("solution.py", encoding="utf-8").read()
            assert "if" not in src, "Реши без if"
        """,
        """
        def bonus(passed, perfect):
            return passed * 10 + perfect * 5
        """),
    cod(f"{P}-noif-e7", t("""
        Напиши функцию `sign_number(n)`: `1` для положительного числа, `-1` для отрицательного, `0` для нуля — **без `if`**.

        Подсказка: разность двух логических значений `(n > 0) - (n < 0)`.
        """),
        """
        def sign_number(n):
            pass
        """,
        """
        def test_values():
            got = [sign_number(5), sign_number(-3), sign_number(0), sign_number(0.1)]
            assert got == [1, -1, 0, 1], f"Получено {got}"

        def test_no_if():
            src = open("solution.py", encoding="utf-8").read()
            assert "if" not in src, "Реши без if"
        """,
        """
        def sign_number(n):
            return (n > 0) - (n < 0)
        """),
    cod(f"{P}-noif-e8", t("""
        Напиши функцию `describe_length(s)` с оператором `:=`: посчитай длину строки прямо в условии и
        верни `"длина <n>"`, если она больше 3, иначе `"коротко"`.

        Примеры:
        ```
        describe_length("привет")   # → "длина 6"
        describe_length("да")       # → "коротко"
        ```
        """),
        """
        def describe_length(s):
            pass
        """,
        """
        def test_values():
            got = [describe_length("привет"), describe_length("да"), describe_length("abcd"), describe_length("abc")]
            assert got == ["длина 6", "коротко", "длина 4", "коротко"], f"Получено {got}"

        def test_walrus():
            src = open("solution.py", encoding="utf-8").read()
            assert ":=" in src, "Используй оператор :="
        """,
        """
        def describe_length(s):
            if (n := len(s)) > 3:
                return f"длина {n}"
            return "коротко"
        """,
        hint="`if (n := len(s)) > 3:` — скобки обязательны.")),
)

m4 = module(f"{P}-match", "match / case", "🎯", "Выбор по образцу: значения, условия, списки, словари и типы",

lesson(f"{P}-m3-l3", "match / case: основы",
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
    out(f"{P}-match-e1", "Что выведет программа?", """
        def grade_word(n):
            match n:
                case 5:
                    return "отлично"
                case 4:
                    return "хорошо"
                case 3 | 2:
                    return "так себе"
                case _:
                    return "нет такой оценки"

        print(grade_word(5), grade_word(2), grade_word(7))
        """),
    out(f"{P}-match-e2", "Что выведет программа? Захват значения и условие `if`.", """
        def classify(n):
            match n:
                case 0:
                    return "ноль"
                case x if x < 0:
                    return f"отрицательное {x}"
                case x:
                    return f"положительное {x}"

        print(classify(0))
        print(classify(-3))
        print(classify(8))
        """, hint="Имя без кавычек в `case` подходит под любое значение и запоминает его."),
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
    cod(f"{P}-match-e3", t("""
        Напиши функцию `day_type(day)` через `match`:

        - `"сб"` или `"вс"` → `"выходной"`
        - `"пн"`, `"вт"`, `"ср"`, `"чт"`, `"пт"` → `"будний"`
        - иначе → `"ошибка"`
        """),
        """
        def day_type(day):
            pass
        """,
        """
        def test_values():
            got = [day_type(d) for d in ("сб", "вс", "пн", "ср", "пт", "xx")]
            assert got == ["выходной", "выходной", "будний", "будний", "будний", "ошибка"], f"Получено {got}"

        def test_match():
            src = open("solution.py", encoding="utf-8").read()
            assert "match" in src and "case" in src, "Используй match / case"
        """,
        """
        def day_type(day):
            match day:
                case "сб" | "вс":
                    return "выходной"
                case "пн" | "вт" | "ср" | "чт" | "пт":
                    return "будний"
                case _:
                    return "ошибка"
        """),
    cod(f"{P}-match-e4", t("""
        Напиши функцию `traffic_light(color)` через `match`:
        `"red"` → `"стой"`, `"yellow"` → `"жди"`, `"green"` → `"иди"`, любой другой → `"неизвестный сигнал"`.
        """),
        """
        def traffic_light(color):
            pass
        """,
        """
        def test_values():
            got = [traffic_light(c) for c in ("red", "yellow", "green", "blue")]
            assert got == ["стой", "жди", "иди", "неизвестный сигнал"], f"Получено {got}"

        def test_match():
            src = open("solution.py", encoding="utf-8").read()
            assert "match" in src, "Используй match / case"
        """,
        """
        def traffic_light(color):
            match color:
                case "red":
                    return "стой"
                case "yellow":
                    return "жди"
                case "green":
                    return "иди"
                case _:
                    return "неизвестный сигнал"
        """),
    cod(f"{P}-match-e5", t("""
        Напиши функцию `score_label(score)` через `match` с **условиями** (`case s if ...`):

        - 90 и больше → `"отлично"`
        - 60 и больше → `"зачёт"`
        - иначе → `"незачёт"`
        """),
        """
        def score_label(score):
            pass
        """,
        """
        def test_values():
            got = [score_label(s) for s in (100, 90, 89, 60, 59, 0)]
            assert got == ["отлично", "отлично", "зачёт", "зачёт", "незачёт", "незачёт"], f"Получено {got}"

        def test_match():
            src = open("solution.py", encoding="utf-8").read()
            assert "match" in src and "case" in src, "Используй match / case"
        """,
        """
        def score_label(score):
            match score:
                case s if s >= 90:
                    return "отлично"
                case s if s >= 60:
                    return "зачёт"
                case _:
                    return "незачёт"
        """),
    cod(f"{P}-match-e6", t("""
        Напиши функцию-калькулятор `calc(a, op, b)` через `match` по операции `op`:

        - `"+"`, `"-"`, `"*"` → результат операции;
        - `"/"` → результат деления, но если `b == 0` → строка `"деление на ноль"`;
        - любая другая операция → `"неизвестная операция"`.

        Примеры:
        ```
        calc(6, "*", 7)   # → 42
        calc(1, "/", 0)   # → "деление на ноль"
        calc(9, "/", 3)   # → 3.0
        calc(2, "^", 3)   # → "неизвестная операция"
        ```
        """),
        """
        def calc(a, op, b):
            pass
        """,
        """
        def test_values():
            got = [calc(6, "*", 7), calc(5, "+", 3), calc(5, "-", 8), calc(9, "/", 3), calc(1, "/", 0), calc(2, "^", 3)]
            assert got == [42, 8, -3, 3.0, "деление на ноль", "неизвестная операция"], f"Получено {got}"
        """,
        """
        def calc(a, op, b):
            match op:
                case "+":
                    return a + b
                case "-":
                    return a - b
                case "*":
                    return a * b
                case "/" if b == 0:
                    return "деление на ноль"
                case "/":
                    return a / b
                case _:
                    return "неизвестная операция"
        """, xp=20)),

lesson(f"{P}-match2", "match: списки, словари и типы",
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
    out(f"{P}-match2-e1", "Что выведет программа? Образец со звёздочкой.", """
        def describe(items):
            match items:
                case []:
                    return "пусто"
                case [x]:
                    return f"один: {x}"
                case [first, *rest]:
                    return f"первый {first}, ещё {len(rest)}"

        print(describe([]))
        print(describe([7]))
        print(describe([1, 2, 3]))
        """),
    out(f"{P}-match2-e2", "Что выведет программа? Образцы типов.", """
        def kind(v):
            match v:
                case bool():
                    return "логическое"
                case int() | float():
                    return "число"
                case str() if v == "":
                    return "пустая строка"
                case str():
                    return "строка"
                case None:
                    return "ничего"
                case _:
                    return "другое"

        print(kind(True), kind(3.5), kind(""))
        print(kind("hi"), kind(None), kind([1]))
        """, hint="`bool()` стоит первым: иначе `True` поймал бы образец `int()`."),
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
        """, xp=20),
    cod(f"{P}-match2-e3", t("""
        Напиши функцию `parse_point(p)` через `match` по списку координат:

        - два числа `[x, y]` → `"2D (x, y)"`
        - три числа `[x, y, z]` → `"3D (x, y, z)"`
        - иначе → `"не точка"`

        Примеры:
        ```
        parse_point([1, 2])      # → "2D (1, 2)"
        parse_point([1, 2, 3])   # → "3D (1, 2, 3)"
        parse_point([1])         # → "не точка"
        ```
        """),
        """
        def parse_point(p):
            pass
        """,
        """
        def test_values():
            got = [parse_point([1, 2]), parse_point([1, 2, 3]), parse_point([1]), parse_point([])]
            assert got == ["2D (1, 2)", "3D (1, 2, 3)", "не точка", "не точка"], f"Получено {got}"
        """,
        """
        def parse_point(p):
            match p:
                case [x, y]:
                    return f"2D ({x}, {y})"
                case [x, y, z]:
                    return f"3D ({x}, {y}, {z})"
                case _:
                    return "не точка"
        """),
    cod(f"{P}-match2-e4", t("""
        Напиши функцию `event_message(event)` через `match` с **шаблонами словарей**:

        - `{"type": "click", "x": ..., "y": ...}` → `"клик в x,y"`
        - `{"type": "key", "key": ...}` → `"клавиша <key>"`
        - любой другой словарь с ключом `"type"` → `"неизвестное событие <type>"`
        - всё остальное → `"не событие"`

        Примеры:
        ```
        event_message({"type": "click", "x": 10, "y": 20})   # → "клик в 10,20"
        event_message({"type": "key", "key": "Enter"})       # → "клавиша Enter"
        event_message({"type": "scroll"})                    # → "неизвестное событие scroll"
        event_message({"x": 1})                              # → "не событие"
        ```
        """),
        """
        def event_message(event):
            pass
        """,
        """
        def test_values():
            got = [event_message({"type": "click", "x": 10, "y": 20}), event_message({"type": "key", "key": "Enter"}),
                   event_message({"type": "scroll"}), event_message({"x": 1}), event_message("click")]
            assert got == ["клик в 10,20", "клавиша Enter", "неизвестное событие scroll", "не событие", "не событие"], f"Получено {got}"
        """,
        """
        def event_message(event):
            match event:
                case {"type": "click", "x": x, "y": y}:
                    return f"клик в {x},{y}"
                case {"type": "key", "key": key}:
                    return f"клавиша {key}"
                case {"type": other}:
                    return f"неизвестное событие {other}"
                case _:
                    return "не событие"
        """, xp=20),
    cod(f"{P}-match2-e5", t("""
        Напиши функцию `value_type(v)` через `match` с **образцами типов**:

        - логическое → `"логическое"`
        - целое → `"целое"`
        - дробное → `"дробное"`
        - строка → `"строка"`
        - иначе → `"другое"`

        Примеры:
        ```
        value_type(True)   # → "логическое"
        value_type(5)      # → "целое"
        value_type(2.5)    # → "дробное"
        value_type(None)   # → "другое"
        ```
        Порядок важен: `True` подходит и под `int()`.
        """),
        """
        def value_type(v):
            pass
        """,
        """
        def test_values():
            got = [value_type(True), value_type(5), value_type(2.5), value_type("x"), value_type(None), value_type([1])]
            assert got == ["логическое", "целое", "дробное", "строка", "другое", "другое"], f"Получено {got}"
        """,
        """
        def value_type(v):
            match v:
                case bool():
                    return "логическое"
                case int():
                    return "целое"
                case float():
                    return "дробное"
                case str():
                    return "строка"
                case _:
                    return "другое"
        """)),
)
