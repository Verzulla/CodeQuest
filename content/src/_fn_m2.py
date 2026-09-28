"""Тема «Функции», модуль 2 «Параметры по-взрослому» — задания. Теория — в _fn_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "fn"

m2 = module(f"{P}-m2", "Параметры по-взрослому", "⚙️", "Значения по умолчанию, несколько результатов, документация, композиция",

lesson(f"{P}-m2-l1", "Значения по умолчанию",
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        def greet(name, greeting="Привет"):
            return f"{greeting}, {name}!"

        print(greet("Аня"))
        print(greet("Боря", "Здравствуй"))
        print(greet(greeting="Хай", name="Вика"))
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа? Знаменитая ловушка.", """
        def add_item(item, items=[]):
            items.append(item)
            return items

        print(add_item("a"))
        print(add_item("b"))
        """, hint="Список по умолчанию создаётся один раз при объявлении функции и переиспользуется."),
    out(f"{P}-m2-l1-e6", "Что выведет программа? Когда вычисляется значение по умолчанию.", """
        x = 10

        def f(a=x):
            return a

        x = 20
        print(f(), f(5))
        """, hint="Значение по умолчанию вычисляется один раз — в момент выполнения строки def."),
    cod(f"{P}-m2-l1-e3", t("""
        Напиши функцию `make_url(path, host="localhost", port=8000)`, которая возвращает `"http://<host>:<port><path>"`.

        Примеры:
        ```
        make_url("/api")                          # → "http://localhost:8000/api"
        make_url("/api", port=9000)               # → "http://localhost:9000/api"
        make_url("/", host="staging", port=80)    # → "http://staging:80/"
        ```
        """),
        """
        def make_url(path, host="localhost", port=8000):
            pass
        """,
        """
        def test_values():
            got = [make_url("/api"), make_url("/api", port=9000), make_url("/", host="staging", port=80)]
            assert got == ["http://localhost:8000/api", "http://localhost:9000/api", "http://staging:80/"], f"Получено {got}"
        """,
        """
        def make_url(path, host="localhost", port=8000):
            return f"http://{host}:{port}{path}"
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Исправь функцию `add_tag(tag, tags=[])` — у неё ловушка изменяемого значения по умолчанию: теги «копятся» между вызовами.

        Должно быть так:
        ```
        add_tag("smoke")              # → ["smoke"]
        add_tag("regress")            # → ["regress"]      (а не ["smoke", "regress"])
        add_tag("api", ["ui"])        # → ["ui", "api"]
        ```
        Используй `tags=None` и создавай новый список внутри функции.
        """),
        """
        def add_tag(tag, tags=[]):
            tags.append(tag)
            return tags
        """,
        """
        def test_independent_calls():
            assert add_tag("smoke") == ["smoke"], "Первый вызов — ['smoke']"
            assert add_tag("regress") == ["regress"], "Второй вызов не должен помнить первый"

        def test_given_list():
            assert add_tag("api", ["ui"]) == ["ui", "api"], "Переданный список дополняется"
        """,
        """
        def add_tag(tag, tags=None):
            if tags is None:
                tags = []
            tags.append(tag)
            return tags
        """,
        hint="```py\ndef add_tag(tag, tags=None):\n    if tags is None:\n        tags = []\n```", xp=20),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `retry_delays(attempts=3, base=1.0, factor=2.0)` — список задержек между повторами по экспоненциальной схеме: `base, base*factor, base*factor², …` (всего `attempts` значений).

        Примеры:
        ```
        retry_delays()                   # → [1.0, 2.0, 4.0]
        retry_delays(4, base=0.5)        # → [0.5, 1.0, 2.0, 4.0]
        retry_delays(2, factor=3)        # → [1.0, 3.0]
        ```
        """),
        """
        def retry_delays(attempts=3, base=1.0, factor=2.0):
            pass
        """,
        """
        def test_values():
            got = [retry_delays(), retry_delays(4, base=0.5), retry_delays(2, factor=3)]
            assert got == [[1.0, 2.0, 4.0], [0.5, 1.0, 2.0, 4.0], [1.0, 3.0]], f"Получено {got}"
        """,
        """
        def retry_delays(attempts=3, base=1.0, factor=2.0):
            return [base * factor ** i for i in range(attempts)]
        """, xp=20),
    cod(f"{P}-m2-l1-e7", t("""
        Напиши функцию `power(base, exp=2)` — `base` в степени `exp`; по умолчанию — квадрат.

        Примеры:
        ```
        power(5)        # → 25
        power(2, 10)    # → 1024
        power(exp=3, base=2)   # → 8
        ```
        """),
        """
        def power(base, exp):
            return base ** exp
        """,
        """
        def test_values():
            got = [power(5), power(2, 10), power(exp=3, base=2)]
            assert got == [25, 1024, 8], f"Получено {got}"
        """,
        """
        def power(base, exp=2):
            return base ** exp
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Программа не запускается: `SyntaxError: parameter without a default follows parameter with a default` —
        параметр без значения по умолчанию стоит после параметра со значением. Исправь определение, чтобы работали вызовы:
        ```
        greet("Аня")                 # → "Привет, Аня!"
        greet("Боря", "Здравствуй")  # → "Здравствуй, Боря!"
        ```
        """),
        """
        def greet(greeting="Привет", name):
            return f"{greeting}, {name}!"
        """,
        """
        def test_values():
            assert greet("Аня") == "Привет, Аня!" and greet("Боря", "Здравствуй") == "Здравствуй, Боря!", "Неверное приветствие"
        """,
        """
        def greet(name, greeting="Привет"):
            return f"{greeting}, {name}!"
        """,
        hint="Параметры со значениями по умолчанию — после обычных.")),

lesson(f"{P}-m2-l2", "Несколько возвращаемых значений",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        def min_max(nums):
            return min(nums), max(nums)

        result = min_max([3, 1, 4])
        print(result, type(result).__name__)
        lo, hi = min_max([10, -2, 7])
        print(lo, hi)
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа?", """
        def parse(line):
            name, _, value = line.partition("=")
            return name.strip(), value.strip()

        key, val = parse("timeout = 30")
        print(key, val, int(val) * 2)
        """),
    out(f"{P}-m2-l2-e6", "Что выведет программа? Кортеж можно разобрать по-разному.", """
        def f():
            return 1, 2, 3

        a, *rest = f()
        print(a, rest)
        print(f()[1], len(f()))
        """),
    cod(f"{P}-m2-l2-e3", t("""
        Напиши функцию `divide(a, b)`, которая возвращает **пару** `(целая часть, остаток)`.

        Примеры:
        ```
        divide(17, 5)   # → (3, 2)
        q, r = divide(10, 3)   # q == 3, r == 1
        ```
        """),
        """
        def divide(a, b):
            pass
        """,
        """
        def test_values():
            assert divide(17, 5) == (3, 2) and divide(10, 3) == (3, 1), "Неверная пара"
        """,
        """
        def divide(a, b):
            return a // b, a % b
        """),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `stats(nums)` — вернуть **три** значения: минимум, максимум и среднее (округлённое до 2 знаков).

        Пример:
        ```
        stats([1, 2, 3, 10])   # → (1, 10, 4.0)
        lo, hi, avg = stats([5, 5])   # (5, 5, 5.0)
        ```
        """),
        """
        def stats(nums):
            pass
        """,
        """
        def test_values():
            assert stats([1, 2, 3, 10]) == (1, 10, 4.0) and stats([5, 5]) == (5, 5, 5.0), "Неверная статистика"
        """,
        """
        def stats(nums):
            return min(nums), max(nums), round(sum(nums) / len(nums), 2)
        """),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `split_results(results)` — разделить результаты тестов на два списка: имена прошедших и имена упавших.

        - `results` — список пар `(имя, прошёл_ли)`.
        - Вернуть пару списков `(passed, failed)`.

        Пример:
        ```
        split_results([("login", True), ("pay", False), ("cart", True)])
        # → (["login", "cart"], ["pay"])
        ```
        """),
        """
        def split_results(results):
            pass
        """,
        """
        def test_values():
            got = split_results([("login", True), ("pay", False), ("cart", True)])
            assert got == (["login", "cart"], ["pay"]), f"Получено {got}"
            assert split_results([]) == ([], []), "Пустой вход — два пустых списка"
        """,
        """
        def split_results(results):
            passed, failed = [], []
            for name, ok in results:
                (passed if ok else failed).append(name)
            return passed, failed
        """),
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `swap(a, b)`, которая возвращает два значения в обратном порядке.

        Пример:
        ```
        x, y = swap(1, 2)   # x == 2, y == 1
        ```
        """),
        """
        def swap(a, b):
            pass
        """,
        """
        def test_values():
            assert swap(1, 2) == (2, 1) and swap("a", "b") == ("b", "a"), "Неверный порядок"
        """,
        """
        def swap(a, b):
            return b, a
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `split_name(full_name)` — вернуть имя и фамилию (два значения) из строки `"Имя Фамилия"`.

        Пример:
        ```
        first, last = split_name("Анна Петрова")   # first == "Анна", last == "Петрова"
        ```
        """),
        """
        def split_name(full_name):
            pass
        """,
        """
        def test_values():
            assert split_name("Анна Петрова") == ("Анна", "Петрова"), f"Получено {split_name('Анна Петрова')!r}"
        """,
        """
        def split_name(full_name):
            first, last = full_name.split()
            return first, last
        """)),

lesson(f"{P}-m2-l3", "Docstring и аннотации типов",
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        def add(a: int, b: int) -> int:
            \"\"\"Сложить два числа.\"\"\"
            return a + b

        print(add.__doc__)
        print(add.__annotations__)
        print(add("а", "б"))
        """, hint="Аннотации — только подсказки: строки тоже «сложатся»."),
    out(f"{P}-m2-l3-e2", "Что выведет программа?", """
        def f(items: list[str], limit: int | None = None) -> list[str]:
            return items[:limit]

        print(f(["a", "b", "c"]))
        print(f(["a", "b", "c"], 2))
        """),
    out(f"{P}-m2-l3-e6", "Что выведет программа? Аннотации ничего не проверяют.", """
        def f(x: int) -> str:
            return x * 2

        print(f(3), f("ab"))
        print(f.__annotations__["return"].__name__)
        """),
    cod(f"{P}-m2-l3-e3", t("""
        Напиши функцию `is_valid_email` с **аннотациями типов** и **docstring**:

        - параметр `email: str`, возвращает `bool`;
        - docstring — непустая строка с описанием;
        - логика: в строке ровно один `@`, и после него есть точка.

        Примеры:
        ```
        is_valid_email("a@b.ru")   # → True
        is_valid_email("a@b")      # → False
        is_valid_email("a@@b.ru")  # → False
        ```
        """),
        """
        def is_valid_email(email):
            pass
        """,
        """
        def test_logic():
            got = [is_valid_email(e) for e in ("a@b.ru", "a@b", "a@@b.ru", "ab.ru")]
            assert got == [True, False, False, False], f"Получено {got}"

        def test_docs():
            assert is_valid_email.__doc__ and is_valid_email.__doc__.strip(), "Добавь docstring"
            ann = is_valid_email.__annotations__
            assert ann.get("email") is str and ann.get("return") is bool, f"Нужны аннотации email: str и -> bool, сейчас {ann}"
        """,
        """
        def is_valid_email(email: str) -> bool:
            \"\"\"Проверить, похож ли email на корректный: один @ и точка в домене.\"\"\"
            if email.count("@") != 1:
                return False
            return "." in email.split("@")[1]
        """, xp=20),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `describe_function(func)`, которая возвращает **первую строку** docstring переданной функции, а если docstring нет — `"нет описания"`.

        Пример:
        ```
        def login():
            \"\"\"Войти в систему.
            Подробности...\"\"\"

        describe_function(login)   # → "Войти в систему."
        describe_function(print)   # → первая строка документации print
        ```
        """),
        """
        def describe_function(func):
            pass
        """,
        """
        def test_doc():
            def login():
                \"\"\"Войти в систему.
                Подробности на второй строке.\"\"\"
            assert describe_function(login) == "Войти в систему.", f"Получено {describe_function(login)!r}"

        def test_no_doc():
            def nodoc():
                pass
            assert describe_function(nodoc) == "нет описания", "Без docstring — «нет описания»"
        """,
        """
        def describe_function(func):
            doc = func.__doc__
            if not doc:
                return "нет описания"
            return doc.strip().splitlines()[0]
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `typed_call(func, *args)`, которая проверяет аргументы по аннотациям функции `func` и вызывает её.

        - Для каждого позиционного аргумента: если в `func.__annotations__` есть тип для соответствующего параметра и аргумент не этого типа — бросить `TypeError`.
        - Иначе вернуть `func(*args)`.

        Имена параметров по порядку: `func.__code__.co_varnames[:func.__code__.co_argcount]`.

        Пример:
        ```
        def add(a: int, b: int) -> int:
            return a + b

        typed_call(add, 1, 2)       # → 3
        typed_call(add, 1, "2")     # TypeError
        ```
        """),
        """
        def typed_call(func, *args):
            pass
        """,
        """
        def test_ok():
            def add(a: int, b: int) -> int:
                return a + b
            assert typed_call(add, 1, 2) == 3, "Корректные типы — вызов"

        def test_bad():
            def add(a: int, b: int) -> int:
                return a + b
            try:
                typed_call(add, 1, "2")
            except TypeError:
                return
            assert False, "Неверный тип аргумента — TypeError"

        def test_no_annotation():
            def echo(x):
                return x
            assert typed_call(echo, "что угодно") == "что угодно", "Без аннотаций — без проверки"
        """,
        """
        def typed_call(func, *args):
            names = func.__code__.co_varnames[:func.__code__.co_argcount]
            for name, value in zip(names, args):
                expected = func.__annotations__.get(name)
                if expected is not None and not isinstance(value, expected):
                    raise TypeError(f"{name}: ожидался {expected.__name__}, получен {type(value).__name__}")
            return func(*args)
        """, xp=25),
    cod(f"{P}-m2-l3-e7", t("""
        Напиши функцию `average` с аннотациями и docstring:

        - параметр `nums: list[float]`, результат `-> float`;
        - docstring — непустой;
        - возвращает среднее, округлённое до 2 знаков.

        Пример:
        ```
        average([1, 2, 4])   # → 2.33
        ```
        """),
        """
        def average(nums):
            return round(sum(nums) / len(nums), 2)
        """,
        """
        def test_values():
            assert average([1, 2, 4]) == 2.33 and average([5.0]) == 5.0, "Неверное среднее"

        def test_docs():
            assert average.__doc__ and average.__doc__.strip(), "Добавь docstring"
            ann = average.__annotations__
            assert ann.get("return") is float and "nums" in ann, f"Нужны аннотации nums и -> float, сейчас {ann}"
        """,
        """
        def average(nums: list[float]) -> float:
            \"\"\"Среднее арифметическое, округлённое до 2 знаков.\"\"\"
            return round(sum(nums) / len(nums), 2)
        """),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `repeat_word(word: str, times: int = 1) -> str` — слово, повторённое `times` раз через пробел.
        Аннотации обязательны.

        Примеры:
        ```
        repeat_word("ура")       # → "ура"
        repeat_word("ура", 3)    # → "ура ура ура"
        ```
        """),
        """
        def repeat_word(word, times=1):
            pass
        """,
        """
        def test_values():
            assert repeat_word("ура") == "ура" and repeat_word("ура", 3) == "ура ура ура", "Неверный результат"

        def test_annotations():
            ann = repeat_word.__annotations__
            assert ann.get("word") is str and ann.get("times") is int and ann.get("return") is str, f"Сейчас {ann}"
        """,
        """
        def repeat_word(word: str, times: int = 1) -> str:
            return " ".join([word] * times)
        """)),

lesson(f"{P}-compose", "Функции из функций",
    out(f"{P}-compose-e1", "Что выведет программа? Вызов внутри вызова.", """
        def add1(x):
            return x + 1

        def double(x):
            return x * 2

        print(double(add1(3)), add1(double(3)))
        """, hint="Сначала вычисляется внутренний вызов."),
    out(f"{P}-compose-e2", "Что выведет программа? Вспомогательная функция.", """
        def normalize(s):
            return s.strip().lower()

        def same(a, b):
            return normalize(a) == normalize(b)

        print(same("  Аня", "аня"), same("a", "b"))
        """),
    out(f"{P}-compose-e3", "Что выведет программа? Порядок определений.", """
        def outer():
            return inner() * 2

        def inner():
            return 21

        print(outer())
        """, hint="Важен момент вызова: к вызову outer() функция inner уже определена."),
    cod(f"{P}-compose-e4", t("""
        Напиши две функции:
        - `tax(price)` — налог 20% от цены, округлённый до 2 знаков;
        - `price_with_tax(price)` — цена плюс налог, **используя** `tax`.

        Примеры:
        ```
        tax(100)              # → 20.0
        price_with_tax(100)   # → 120.0
        ```
        """),
        "",
        """
        import inspect

        def test_values():
            assert tax(100) == 20.0 and tax(9.99) == 2.0 and price_with_tax(100) == 120.0, "Неверный расчёт"

        def test_uses_tax():
            assert "tax(" in inspect.getsource(price_with_tax).replace("price_with_tax(", ""), "price_with_tax должна вызывать tax"
        """,
        """
        def tax(price):
            return round(price * 0.2, 2)

        def price_with_tax(price):
            return price + tax(price)
        """),
    cod(f"{P}-compose-e5", t("""
        Напиши функцию `is_strong_password(p)`, собранную из трёх проверок — их тоже напиши:

        - `long_enough(p)` — длина не меньше 8;
        - `has_digit(p)` — есть цифра;
        - `has_upper(p)` — есть заглавная буква (`ch.isupper()`).

        `is_strong_password` возвращает `True`, только если прошли **все три**.
        """),
        "",
        """
        def test_parts():
            assert long_enough("12345678") and not long_enough("123"), "long_enough"
            assert has_digit("a1") and not has_digit("ab"), "has_digit"
            assert has_upper("aB") and not has_upper("ab"), "has_upper"

        def test_strong():
            got = [is_strong_password(p) for p in ("Abcdefg1", "abcdefg1", "Abcdefgh", "Ab1")]
            assert got == [True, False, False, False], f"Получено {got}"
        """,
        """
        def long_enough(p):
            return len(p) >= 8

        def has_digit(p):
            for ch in p:
                if ch.isdigit():
                    return True
            return False

        def has_upper(p):
            for ch in p:
                if ch.isupper():
                    return True
            return False

        def is_strong_password(p):
            return long_enough(p) and has_digit(p) and has_upper(p)
        """, xp=20),
    cod(f"{P}-compose-e6", t("""
        Напиши две функции:
        - `format_money(x)` — сумма с двумя знаками после точки и `" руб."`: `99.5` → `"99.50 руб."`;
        - `receipt_line(name, price)` — строка чека `"<name>: <сумма>"`, **используя** `format_money`.

        Пример:
        ```
        receipt_line("Кофе", 150)   # → "Кофе: 150.00 руб."
        ```
        """),
        "",
        """
        import inspect

        def test_values():
            assert format_money(99.5) == "99.50 руб." and receipt_line("Кофе", 150) == "Кофе: 150.00 руб.", "Неверный формат"

        def test_uses_helper():
            assert "format_money(" in inspect.getsource(receipt_line), "receipt_line должна вызывать format_money"
        """,
        """
        def format_money(x):
            return f"{x:.2f} руб."

        def receipt_line(name, price):
            return f"{name}: {format_money(price)}"
        """),
    cod(f"{P}-compose-e7", t("""
        Напиши две функции:
        - `average(nums)` — среднее;
        - `above_average(nums)` — список чисел **больше среднего**, в исходном порядке, **используя** `average`.

        Пример:
        ```
        above_average([1, 5, 3, 9])   # → [5, 9]   (среднее 4.5)
        ```
        """),
        "",
        """
        def test_values():
            assert average([1, 5, 3, 9]) == 4.5 and above_average([1, 5, 3, 9]) == [5, 9] and above_average([2, 2]) == [], "Неверный результат"
        """,
        """
        def average(nums):
            return sum(nums) / len(nums)

        def above_average(nums):
            avg = average(nums)
            result = []
            for n in nums:
                if n > avg:
                    result.append(n)
            return result
        """),
    cod(f"{P}-compose-e8", t("""
        Напиши две функции:
        - `clean_words(text)` — список слов текста в нижнем регистре, без знаков `.`, `,`, `!` и `?`;
        - `word_count(text, word)` — сколько раз слово встречается в тексте, **используя** `clean_words`
          (регистр и знаки препинания не мешают).

        Пример:
        ```
        clean_words("Кот, кот! И пёс.")   # → ["кот", "кот", "и", "пёс"]
        word_count("Кот, кот! И пёс.", "кот")   # → 2
        ```
        """),
        "",
        """
        def test_values():
            assert clean_words("Кот, кот! И пёс.") == ["кот", "кот", "и", "пёс"], f"Получено {clean_words('Кот, кот! И пёс.')}"
            assert word_count("Кот, кот! И пёс.", "кот") == 2 and word_count("", "x") == 0, "Неверный подсчёт"
        """,
        """
        def clean_words(text):
            for mark in ".,!?":
                text = text.replace(mark, "")
            return text.lower().split()

        def word_count(text, word):
            return clean_words(text).count(word)
        """)),
)
