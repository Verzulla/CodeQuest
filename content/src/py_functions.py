"""Тема «Функции»."""
from ._lib import cod, lesson, module, out, q, t, topic

P = "fn"

# ============================================================
m1 = module(f"{P}-m1", "Основы функций", "🧰", "def, параметры, return",

lesson(f"{P}-m1-l1", "def и вызов функции", """
    # Функция

    ```
    def greet(name):
        return f"Привет, {name}!"

    greet("Аня")      # вызов → "Привет, Аня!"
    ```

    - `def` — объявить функцию; тело — с отступом.
    - Функция выполняется **только при вызове** (со скобками).
    - Одну функцию можно вызывать сколько угодно раз.
    """,
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        def hello():
            print("Привет!")

        print("до")
        hello()
        hello()
        print("после")
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа? Функцию объявили, но…", """
        def boom():
            print("бум")

        print("старт")
        boom
        print("финиш")
        """, hint="Без скобок функция не вызывается — это просто обращение к объекту."),
    cod(f"{P}-m1-l1-e3", t("""
        Напиши функцию `square(x)`, которая возвращает квадрат числа.

        Примеры:
        ```
        square(3)    # → 9
        square(-4)   # → 16
        ```
        """),
        "",
        """
        def test_values():
            assert square(3) == 9 and square(-4) == 16 and square(0) == 0, "Неверный квадрат"
        """,
        """
        def square(x):
            return x * x
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `separator()` **без параметров**, которая возвращает строку из 20 символов `-`.

        Затем **вызови её дважды** и выведи результат каждого вызова через `print`.

        Ожидаемый вывод:
        ```
        --------------------
        --------------------
        ```
        """),
        "",
        """
        def test_function():
            assert separator() == "-" * 20, "separator() должна вернуть 20 дефисов"

        def test_output():
            assert OUTPUT.split() == ["-" * 20] * 2, f"Напечатано {OUTPUT!r}"
        """,
        """
        def separator():
            return "-" * 20

        print(separator())
        print(separator())
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `celsius_to_fahrenheit(c)` — перевод температуры: `F = C * 9 / 5 + 32`.

        Примеры:
        ```
        celsius_to_fahrenheit(0)     # → 32.0
        celsius_to_fahrenheit(100)   # → 212.0
        celsius_to_fahrenheit(-40)   # → -40.0
        ```
        """),
        """
        def celsius_to_fahrenheit(c):
            pass
        """,
        """
        def test_values():
            got = [celsius_to_fahrenheit(c) for c in (0, 100, -40)]
            assert got == [32.0, 212.0, -40.0], f"Получено {got}"
        """,
        """
        def celsius_to_fahrenheit(c):
            return c * 9 / 5 + 32
        """),
    full="""
    ## Зачем это нужно

    Функция — это именованный кусок кода, который можно вызывать много раз. Без функций программы превращаются в длинные простыни с повторами: поменял логику в одном месте — забыл в другом. В автотестах всё построено на функциях: каждый тест — функция, помощники (`login_as`, `create_user`) — функции, Page Object — набор функций-методов.

    ## Как это работает

    ```py
    def имя(параметры):
        \"\"\"Необязательное описание\"\"\"
        тело
        return результат
    ```

    1. `def` **создаёт** функцию и связывает её с именем. Тело при этом **не выполняется**.
    2. Вызов `имя(аргументы)` выполняет тело.
    3. `return` возвращает значение и сразу завершает функцию.

    ### Имя без скобок — это не вызов

    `boom` — ссылка на функцию-объект, `boom()` — вызов. Забытые скобки — частая причина «почему ничего не происходит».

    ### Порядок

    Функцию нужно объявить **до** того, как её вызовут при выполнении. Внутри одной функции можно вызывать другую, объявленную ниже — главное, чтобы к моменту вызова она уже существовала.

    ### Имена

    Глагол, описывающий действие: `calculate_total`, `is_valid_email`, `create_user`. Функции-проверки часто начинаются с `is_`/`has_`.

    ## Примеры

    ### Пример 1. Объявление и вызовы

    ```python
    def greet(name):
        return f"Привет, {name}!"

    print(greet("Аня"))
    print(greet("Боря"))
    message = greet("Вика")
    print(message.upper())
    ```

    ### Пример 2. Тело выполняется только при вызове

    ```python
    def setup():
        print("  готовлю тестовые данные")

    print("функция объявлена")
    setup()
    print(setup)          # сам объект функции
    ```

    ### Пример 3. Функции вызывают функции

    ```python
    def to_fahrenheit(c):
        return c * 9 / 5 + 32

    def describe(c):
        return f"{c}°C = {to_fahrenheit(c)}°F"

    for c in [0, 36.6, 100]:
        print(describe(c))
    ```

    ### Пример 4. Убираем повторы

    ```python
    def check(name, expected, actual):
        mark = "✅" if expected == actual else "❌"
        print(f"{mark} {name}: ожидали {expected}, получили {actual}")

    check("статус", 200, 200)
    check("id", 1, 999)
    ```

    ## Частые ошибки

    **Забыли скобки при вызове** — функция не выполнилась.

    **Вызов до объявления** — `NameError`.

    **Забыли отступ тела** — `IndentationError`.

    ## Шпаргалка

    ```py
    def area(w, h):
        return w * h

    area(3, 4)      # вызов
    area            # объект функции, не вызов
    ```
    """,
    quiz=[
        q("Когда выполняется тело функции?", ["При объявлении через def", "При каждом вызове со скобками", "Один раз при запуске программы", "Никогда без return"], 1, "`def` только создаёт функцию; тело работает при вызове."),
        q("Что выведет код?\n```py\ndef f():\n    return 5\nprint(f)\n```", ["`5`", "Объект функции вида `<function f at ...>`", "`None`", "Ошибка"], 1, "Без скобок функция не вызывается."),
        q("Какое имя лучше для функции, проверяющей email?", ["`email`", "`is_valid_email`", "`EmailCheck`", "`e`"], 1, "Функции-проверки удобно называть с `is_`: сразу понятно, что вернётся bool."),
    ]),

lesson(f"{P}-m1-l2", "Параметры и аргументы", """
    # Параметры

    ```
    def power(base, exp):      # base, exp — параметры
        return base ** exp

    power(2, 10)               # позиционные аргументы
    power(exp=3, base=5)       # именованные — порядок не важен
    power(2, exp=5)            # смешанно: сначала позиционные
    ```

    Количество аргументов должно совпадать с параметрами (иначе `TypeError`).
    """,
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        def power(base, exp):
            return base ** exp

        print(power(2, 3), power(3, 2))
        print(power(exp=2, base=5))
        """, hint="Для позиционных аргументов порядок важен, для именованных — нет."),
    out(f"{P}-m1-l2-e2", "Что выведет программа?", """
        def describe(name, role):
            return f"{name} — {role}"

        print(describe("Аня", "QA"))
        print(describe(role="QA", name="Боря"))
        try:
            describe("Вика")
        except TypeError:
            print("не хватает аргумента")
        """),
    cod(f"{P}-m1-l2-e3", t("""
        Напиши функцию `rectangle_area(width, height)` — площадь прямоугольника.

        Примеры:
        ```
        rectangle_area(3, 4)                  # → 12
        rectangle_area(height=2, width=10)    # → 20
        ```
        """),
        """
        def rectangle_area(width, height):
            pass
        """,
        """
        def test_values():
            assert rectangle_area(3, 4) == 12 and rectangle_area(height=2, width=10) == 20, "Неверная площадь"
        """,
        """
        def rectangle_area(width, height):
            return width * height
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `format_user(name, age, city)`, которая возвращает строку `"<имя>, <возраст> лет, <город>"`.

        Затем **вызови её с именованными аргументами** в порядке `city`, `name`, `age` для данных: Аня, 25, Казань — и выведи результат.

        Ожидаемый вывод:
        ```
        Аня, 25 лет, Казань
        ```
        """),
        "",
        """
        def test_function():
            assert format_user("Боря", 30, "Сочи") == "Боря, 30 лет, Сочи", "Неверный формат строки"

        def test_output():
            assert OUTPUT.strip() == "Аня, 25 лет, Казань", f"Напечатано {OUTPUT.strip()!r}"

        def test_keywords():
            src = open("solution.py", encoding="utf-8").read()
            assert "city=" in src and "name=" in src and "age=" in src, "Вызови функцию с именованными аргументами"
        """,
        """
        def format_user(name, age, city):
            return f"{name}, {age} лет, {city}"

        print(format_user(city="Казань", name="Аня", age=25))
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `discount_price(price, percent)` — цена со скидкой в процентах, округлённая до 2 знаков.

        Примеры:
        ```
        discount_price(1000, 15)    # → 850.0
        discount_price(99.9, 10)    # → 89.91
        discount_price(500, 0)      # → 500.0
        ```
        """),
        """
        def discount_price(price, percent):
            pass
        """,
        """
        def test_values():
            got = [discount_price(1000, 15), discount_price(99.9, 10), discount_price(500, 0)]
            assert got == [850.0, 89.91, 500.0], f"Получено {got}"
        """,
        """
        def discount_price(price, percent):
            return round(price * (1 - percent / 100), 2)
        """),
    full="""
    ## Зачем это нужно

    Параметры делают функцию универсальной: одна `create_user(name, role)` создаёт любого пользователя, одна `check_status(expected, actual)` проверяет любой ответ. Важно понимать, как аргументы сопоставляются с параметрами — от этого зависит читаемость вызовов.

    ## Как это работает

    - **Параметры** — имена в объявлении функции: `def f(a, b):`.
    - **Аргументы** — конкретные значения при вызове: `f(1, 2)`.

    ### Позиционные аргументы

    Сопоставляются по порядку: первый аргумент — первому параметру. Путаница порядка — логический баг, который Python не заметит.

    ### Именованные аргументы

    `f(b=2, a=1)` — по имени, порядок не важен. Вызов становится самодокументируемым: `create_user(name="Аня", role="admin", active=True)` читается лучше, чем `create_user("Аня", "admin", True)`.

    ### Правила смешивания

    - сначала позиционные, потом именованные: `f(1, b=2)` — можно, `f(a=1, 2)` — `SyntaxError`;
    - один параметр нельзя передать дважды: `f(1, a=1)` — `TypeError`;
    - число аргументов должно совпадать (если нет значений по умолчанию) — иначе `TypeError: missing ... required positional argument`.

    ## Примеры

    ### Пример 1. Позиционные и именованные

    ```python
    def power(base, exp):
        return base ** exp

    print(power(2, 10))
    print(power(10, 2))              # порядок важен!
    print(power(exp=2, base=10))
    ```

    ### Пример 2. Читаемость вызова

    ```python
    def create_user(name, role, active):
        return {"name": name, "role": role, "active": active}

    print(create_user("Аня", "admin", True))
    print(create_user(name="Боря", role="qa", active=False))
    ```

    ### Пример 3. Ошибки вызова

    ```python
    def f(a, b):
        return a + b

    for call in ["f(1)", "f(1, 2, 3)", "f(1, a=2)"]:
        try:
            eval(call)
        except TypeError as e:
            print(f"{call:12} -> {e}")
    ```

    ### Пример 4. Функция-калькулятор цены

    ```python
    def final_price(price, discount_percent, tax_percent):
        after_discount = price * (1 - discount_percent / 100)
        return round(after_discount * (1 + tax_percent / 100), 2)

    print(final_price(price=1000, discount_percent=10, tax_percent=20))
    ```

    ## Частые ошибки

    **Перепутанный порядок позиционных аргументов** — Python не подскажет.

    **Позиционный аргумент после именованного** — `SyntaxError`.

    **Лишние или недостающие аргументы** — `TypeError`.

    ## Шпаргалка

    ```py
    def f(a, b): ...
    f(1, 2)          # позиционно
    f(b=2, a=1)      # по имени
    f(1, b=2)        # смешанно — сначала позиционные
    ```
    """,
    quiz=[
        q("Что вернёт `power(exp=2, base=3)` для `def power(base, exp): return base ** exp`?", ["`8`", "`9`", "`6`", "Ошибка"], 1, "Именованные аргументы сопоставляются по имени: 3 ** 2 = 9."),
        q("Какой вызов вызовет SyntaxError?", ["`f(1, b=2)`", "`f(a=1, b=2)`", "`f(a=1, 2)`", "`f(1, 2)`"], 2, "Позиционный аргумент не может идти после именованного."),
        q("Что такое параметр?", ["Значение при вызове", "Имя в объявлении функции, которое получит значение", "Возвращаемое значение", "Имя функции"], 1, "Параметры объявляются в `def`, аргументы передаются при вызове."),
    ]),

lesson(f"{P}-m1-l3", "return против print, None", """
    # return и print — не одно и то же

    - `return` — **отдаёт** значение вызывающему коду и завершает функцию.
    - `print` — только **выводит** на экран; результатом не является.

    ```
    def f():
        print(5)      # на экран, но вернёт None

    x = f()           # x == None
    ```

    Функция без `return` (или с пустым `return`) возвращает `None`.
    """,
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        def shows(x):
            print(x * 2)

        def gives(x):
            return x * 2

        a = shows(5)
        b = gives(5)
        print(a, b)
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа? Код после return не выполняется.", """
        def check(n):
            if n < 0:
                return "отрицательное"
            return "неотрицательное"
            print("это не выполнится")

        print(check(-1), check(3))
        """),
    cod(f"{P}-m1-l3-e3", t("""
        В функции `total(prices)` ошибка: она **печатает** сумму вместо того, чтобы её **вернуть**, поэтому `result` получается `None`.

        Исправь функцию, чтобы она возвращала сумму и ничего не печатала.

        Пример:
        ```
        total([100, 250, 50])   # → 400
        ```
        """),
        """
        def total(prices):
            s = 0
            for p in prices:
                s += p
            print(s)
        """,
        """
        def test_returns():
            assert total([100, 250, 50]) == 400 and total([]) == 0, "Функция должна вернуть сумму"

        def test_no_print():
            assert capture(total, [1, 2]) == "", "Функция не должна ничего печатать"
        """,
        """
        def total(prices):
            s = 0
            for p in prices:
                s += p
            return s
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `find_negative(nums)` — вернуть **первое** отрицательное число списка, а если таких нет — `None`.

        Используй `return` внутри цикла, чтобы выйти сразу, как только нашлось число.

        Примеры:
        ```
        find_negative([3, -1, -5])   # → -1
        find_negative([1, 2])        # → None
        ```
        """),
        """
        def find_negative(nums):
            pass
        """,
        """
        def test_values():
            assert find_negative([3, -1, -5]) == -1 and find_negative([1, 2]) is None and find_negative([]) is None, "Неверный результат"
        """,
        """
        def find_negative(nums):
            for n in nums:
                if n < 0:
                    return n
            return None
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `report(passed, failed)`, которая **возвращает** строку отчёта (а не печатает её):

        - если упавших нет → `"Все <passed> тестов прошли"`;
        - иначе → `"Прошло: <passed>, упало: <failed>"`.

        Затем **выведи** результат вызова `report(10, 0)` через `print`.

        Ожидаемый вывод:
        ```
        Все 10 тестов прошли
        ```
        """),
        "",
        """
        def test_returns():
            assert report(10, 0) == "Все 10 тестов прошли" and report(8, 2) == "Прошло: 8, упало: 2", "Неверная строка отчёта"

        def test_function_does_not_print():
            assert capture(report, 1, 1) == "", "report должна возвращать строку, а не печатать"

        def test_output():
            assert OUTPUT.strip() == "Все 10 тестов прошли", f"Напечатано {OUTPUT.strip()!r}"
        """,
        """
        def report(passed, failed):
            if failed == 0:
                return f"Все {passed} тестов прошли"
            return f"Прошло: {passed}, упало: {failed}"

        print(report(10, 0))
        """),
    full="""
    ## Зачем это нужно

    Путаница `return` и `print` — ошибка номер один у начинающих. Функция, которая печатает результат вместо возврата, бесполезна для остального кода: её результат нельзя сохранить, проверить в тесте, передать дальше. Автотесты проверяют именно **возвращаемые** значения.

    ## Как это работает

    ### return

    - Отдаёт значение туда, где функция была вызвана: `x = f()`.
    - **Сразу завершает** функцию: код после `return` не выполняется.
    - Может стоять в нескольких местах (ранний выход).
    - `return` без значения или отсутствие `return` → функция вернёт `None`.

    ### print

    - Выводит текст для человека.
    - Возвращает `None`.
    - В функциях-вычислениях — только для отладки.

    ### Правило

    Функция либо **вычисляет и возвращает** (как `len`, `sorted`), либо **выполняет действие** (как `print`, запись в файл). Смешивание усложняет тестирование. Печатать результат лучше снаружи: `print(calculate(...))`.

    ## Примеры

    ### Пример 1. Разница в действии

    ```python
    def shows(x):
        print(x * 2)

    def gives(x):
        return x * 2

    a = shows(5)
    b = gives(5)
    print("a =", a, "| b =", b)
    print("b + 1 =", b + 1)
    ```

    ### Пример 2. Ранний return

    ```python
    def find_first_error(log):
        for i, line in enumerate(log):
            if line.startswith("ERROR"):
                return i, line
        return None

    print(find_first_error(["INFO ok", "ERROR db", "ERROR again"]))
    print(find_first_error(["INFO ok"]))
    ```

    ### Пример 3. Функция без return

    ```python
    def nothing():
        x = 42

    result = nothing()
    print(result, result is None)
    ```

    ### Пример 4. Тестируемость

    ```python
    def summary(passed, failed):
        return f"{passed} passed, {failed} failed"

    assert summary(3, 1) == "3 passed, 1 failed"
    print("функцию с return легко проверить assert-ом")
    ```

    ## Частые ошибки

    **`print` вместо `return`** — результат вызова `None`.

    **Код после `return`** — никогда не выполнится.

    **`return` внутри цикла** там, где нужно обработать все элементы.

    ## Шпаргалка

    ```py
    def f(x):
        if bad(x):
            return None        # ранний выход
        return compute(x)      # результат

    print(f(10))               # печать — снаружи
    ```
    """,
    quiz=[
        q("Что будет в `x` после `x = print(\"hi\")`?", ["`\"hi\"`", "`None`", "`True`", "Ошибка"], 1, "`print` выводит текст и возвращает `None`."),
        q("Что вернёт функция без `return`?", ["`0`", "`None`", "Ошибка", "Последнее вычисленное значение"], 1, "Отсутствие `return` означает возврат `None`."),
        q("Что происходит после выполнения `return` внутри функции?", ["Функция продолжает работу", "Функция сразу завершается", "Функция перезапускается", "Выполняется код после return, затем выход"], 1, "`return` немедленно завершает функцию."),
    ]),
)

# ============================================================
m2 = module(f"{P}-m2", "Параметры по-взрослому", "⚙️", "Значения по умолчанию, несколько результатов, аннотации",

lesson(f"{P}-m2-l1", "Значения по умолчанию", """
    # Параметры со значением по умолчанию

    ```
    def connect(host, port=8080, timeout=30):
        ...

    connect("localhost")                # port=8080, timeout=30
    connect("localhost", 9000)          # port=9000
    connect("localhost", timeout=5)     # только timeout
    ```

    - Параметры по умолчанию идут **после** обязательных.
    - ⚠️ Не используй изменяемое значение по умолчанию (`[]`, `{}`) — оно создаётся **один раз** и общее для всех вызовов. Используй `None`.
    """,
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
    full="""
    ## Зачем это нужно

    У многих функций есть «разумные настройки»: таймаут 30 секунд, порт 8080, браузер Chrome. Значения по умолчанию позволяют не указывать их каждый раз, но переопределять при необходимости. Так устроены почти все библиотеки: `requests.get(url, timeout=...)`, `sorted(xs, reverse=False)`.

    ## Как это работает

    ```py
    def connect(host, port=8080, timeout=30):
        ...
    ```

    - Параметры без значения — **обязательные**, со значением — **необязательные**.
    - Необязательные идут **после** обязательных.
    - При вызове часто пропускают средние параметры и задают дальние по имени: `connect("db", timeout=5)`.

    ### Ловушка изменяемого значения по умолчанию

    Значение по умолчанию вычисляется **один раз** — в момент выполнения `def`, а не при каждом вызове. Для чисел и строк это не проблема (они неизменяемые). Но список или словарь по умолчанию — **один объект на все вызовы**: изменения накапливаются.

    Правильный шаблон:

    ```py
    def add_item(item, items=None):
        if items is None:
            items = []
        items.append(item)
        return items
    ```

    ## Примеры

    ### Пример 1. Пропуск параметров

    ```python
    def connect(host, port=8080, timeout=30, secure=False):
        scheme = "https" if secure else "http"
        return f"{scheme}://{host}:{port} (timeout {timeout}s)"

    print(connect("localhost"))
    print(connect("api.shop.ru", 443, secure=True))
    print(connect("db", timeout=5))
    ```

    ### Пример 2. Ловушка в действии

    ```python
    def add_bad(item, items=[]):
        items.append(item)
        return items

    print(add_bad("a"))
    print(add_bad("b"))
    print(add_bad.__defaults__)      # тот самый общий список
    ```

    ### Пример 3. Правильный вариант

    ```python
    def add_good(item, items=None):
        if items is None:
            items = []
        items.append(item)
        return items

    print(add_good("a"))
    print(add_good("b"))
    print(add_good("c", ["x"]))
    ```

    ### Пример 4. Экспоненциальные задержки

    ```python
    def retry_delays(attempts=3, base=1.0, factor=2.0):
        return [base * factor ** i for i in range(attempts)]

    print(retry_delays())
    print(retry_delays(5, base=0.1))
    ```

    ## Частые ошибки

    **`def f(a=1, b):`** — `SyntaxError`: обязательный после необязательного.

    **`items=[]` / `config={}` по умолчанию** — общий объект между вызовами.

    **Значение по умолчанию из вызова функции** — `def log(ts=time.time()):` зафиксирует время объявления, а не вызова.

    ## Шпаргалка

    ```py
    def f(required, optional=10): ...
    def f(x, items=None):
        items = [] if items is None else items
    f(1, optional=5)      # переопределить по имени
    ```
    """,
    quiz=[
        q("Что выведет второй вызов?\n```py\ndef f(x, acc=[]):\n    acc.append(x)\n    return acc\nf(1)\nprint(f(2))\n```", ["`[2]`", "`[1, 2]`", "`[1]`", "Ошибка"], 1,
          "Список по умолчанию общий для всех вызовов — в нём уже лежит 1."),
        q("Какое объявление корректно?", ["`def f(a=1, b):`", "`def f(a, b=1):`", "`def f(=1, b):`", "`def f(a=, b=1):`"], 1, "Параметры со значением по умолчанию идут после обязательных."),
        q("Как правильно задать список по умолчанию?", ["`items=[]`", "`items=None` и создать список внутри", "`items=list`", "`items=()`"], 1, "Шаблон с `None` создаёт новый список при каждом вызове."),
    ]),

lesson(f"{P}-m2-l2", "Несколько возвращаемых значений", """
    # return a, b

    ```
    def min_max(nums):
        return min(nums), max(nums)     # на самом деле возвращается кортеж

    lo, hi = min_max([3, 1, 4])        # распаковка
    ```

    - Результат — **кортеж** `(a, b)`.
    - Удобно распаковывать сразу в переменные.
    - Для многих значений лучше вернуть словарь или dataclass — с понятными именами.
    """,
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
    full="""
    ## Зачем это нужно

    Функция часто вычисляет сразу несколько связанных значений: минимум и максимум, частное и остаток, прошедшие и упавшие тесты, статус и тело ответа. В Python их можно вернуть «одним `return`» и сразу разложить по переменным.

    ## Как это работает

    `return a, b` — это на самом деле `return (a, b)`: создаётся **кортеж**. При вызове его удобно распаковать:

    ```py
    lo, hi = min_max(nums)
    ```

    Или сохранить целиком и обращаться по индексу: `result[0]` (хуже читается).

    ### Когда значений много

    Три-четыре значения в кортеже — предел понятности: `x[2]` ничего не говорит о смысле. Для большего числа — словарь, `namedtuple` или `dataclass`:

    ```py
    return {"min": lo, "max": hi, "avg": avg}
    ```

    ### Встроенные примеры

    `divmod(17, 5)` → `(3, 2)`, `str.partition` → тройка, `dict.items()` → пары.

    ## Примеры

    ### Пример 1. Кортеж и распаковка

    ```python
    def min_max(nums):
        return min(nums), max(nums)

    r = min_max([3, 1, 4, 1, 5])
    print(r, type(r).__name__)
    lo, hi = r
    print("диапазон:", hi - lo)
    ```

    ### Пример 2. Статус и данные

    ```python
    def fetch_user(users, uid):
        for u in users:
            if u["id"] == uid:
                return True, u
        return False, None

    users = [{"id": 1, "name": "Аня"}]
    for uid in [1, 7]:
        found, user = fetch_user(users, uid)
        print(uid, "->", user["name"] if found else "не найден")
    ```

    ### Пример 3. Разделение на группы

    ```python
    def split_results(results):
        passed, failed = [], []
        for name, ok in results:
            (passed if ok else failed).append(name)
        return passed, failed

    ok, bad = split_results([("login", True), ("pay", False), ("cart", True)])
    print("прошли:", ok, "| упали:", bad)
    ```

    ### Пример 4. Когда лучше словарь

    ```python
    def summary(times):
        return {"count": len(times), "min": min(times), "max": max(times),
                "avg": round(sum(times) / len(times), 2)}

    s = summary([0.3, 1.2, 0.8])
    print(s["avg"], s)
    ```

    ## Частые ошибки

    **Неверное число переменных при распаковке** — `ValueError`.

    **Кортеж из 5+ значений** — теряется смысл; используй словарь/dataclass.

    **Разные типы возврата** (`return x` в одной ветке и `return x, y` в другой) — вызывающий код не сможет одинаково обработать результат.

    ## Шпаргалка

    ```py
    def f(): return a, b        # кортеж
    x, y = f()                  # распаковка
    q, r = divmod(17, 5)
    return {"key": value, ...}  # для многих значений
    ```
    """,
    quiz=[
        q("Какой тип у результата `return 1, 2`?", ["`list`", "`tuple`", "`dict`", "Два отдельных значения"], 1, "Запятые создают кортеж."),
        q("Что будет при `a, b = f()`, если `f` возвращает `(1, 2, 3)`?", ["a=1, b=2", "`ValueError`", "a=1, b=(2, 3)", "a=(1, 2), b=3"], 1, "Число переменных должно совпадать с числом элементов."),
        q("Что лучше вернуть, если значений шесть?", ["Кортеж из шести", "Словарь или dataclass с понятными именами полей", "Шесть отдельных return", "Строку"], 1, "Именованные поля понятнее индексов."),
    ]),

lesson(f"{P}-m2-l3", "Docstring и аннотации типов", """
    # Документация функции

    ```
    def discount(price: float, percent: int = 0) -> float:
        \"\"\"Вернуть цену со скидкой в процентах.\"\"\"
        return price * (1 - percent / 100)
    ```

    - **Docstring** — строка сразу после `def`; видна в `help()` и в IDE.
    - **Аннотации** (`price: float`, `-> float`) — подсказки о типах для людей и инструментов. Python их **не проверяет** при выполнении.
    """,
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
    full="""
    ## Зачем это нужно

    Код читают гораздо чаще, чем пишут. Docstring объясняет, **что** делает функция, а аннотации типов — **что** она принимает и возвращает. IDE показывает их в подсказках, инструменты вроде mypy находят ошибки типов до запуска, а коллеги понимают твои хелперы для тестов без чтения тела функции.

    ## Как это работает

    ### Docstring

    Строковый литерал первой строкой тела функции:

    ```py
    def create_user(name, role="qa"):
        \"\"\"Создать тестового пользователя через API.

        Возвращает словарь с полями id, name, role.
        \"\"\"
    ```

    Доступен как `func.__doc__` и через `help(func)`. Первая строка — краткое описание, дальше — подробности.

    ### Аннотации типов

    ```py
    def discount(price: float, percent: int = 0) -> float:
    ```

    - `имя: тип` — ожидаемый тип параметра;
    - `-> тип` — тип результата;
    - сложные типы: `list[str]`, `dict[str, int]`, `int | None` (или `Optional[int]`), `tuple[int, int]`.

    **Python их не проверяет** при выполнении — это подсказки. Хранятся в `func.__annotations__`. Проверяют их внешние инструменты (mypy, pyright) и IDE; библиотеки вроде pydantic и FastAPI используют аннотации для валидации данных.

    ## Примеры

    ### Пример 1. Документация доступна из кода

    ```python
    def discount(price: float, percent: int = 0) -> float:
        \"\"\"Вернуть цену со скидкой.

        percent — размер скидки в процентах (0–100).
        \"\"\"
        return round(price * (1 - percent / 100), 2)

    print(discount.__doc__.splitlines()[0])
    print(discount.__annotations__)
    print(discount(1000, 15))
    ```

    ### Пример 2. Аннотации не проверяются

    ```python
    def double(x: int) -> int:
        return x * 2

    print(double(21))
    print(double("ха"))       # Python не возражает
    ```

    ### Пример 3. Сложные типы

    ```python
    def group_by_status(results: list[tuple[str, bool]]) -> dict[str, list[str]]:
        \"\"\"Разложить имена тестов по статусу.\"\"\"
        groups: dict[str, list[str]] = {"passed": [], "failed": []}
        for name, ok in results:
            groups["passed" if ok else "failed"].append(name)
        return groups

    print(group_by_status([("login", True), ("pay", False)]))
    ```

    ### Пример 4. Опциональные значения

    ```python
    def find(items: list[str], prefix: str) -> str | None:
        \"\"\"Первый элемент с префиксом или None.\"\"\"
        for item in items:
            if item.startswith(prefix):
                return item
        return None

    print(find(["test_login", "test_pay"], "test_p"), find([], "x"))
    ```

    ## Частые ошибки

    **Надежда, что аннотации защитят от неверных типов** — без внешних инструментов они ничего не проверяют.

    **Docstring не первой строкой** — тогда это просто строка, а `__doc__` будет `None`.

    **Устаревшая документация** — хуже её отсутствия: обновляй вместе с кодом.

    ## Шпаргалка

    ```py
    def f(x: int, items: list[str] | None = None) -> dict[str, int]:
        \"\"\"Кратко, что делает функция.\"\"\"
    f.__doc__, f.__annotations__, help(f)
    ```
    """,
    quiz=[
        q("Что произойдёт при вызове `def f(x: int): return x` как `f(\"текст\")`?", ["TypeError", "Вернётся `\"текст\"` — аннотации не проверяются", "Вернётся 0", "SyntaxError"], 1, "Аннотации — подсказки; Python их не проверяет при выполнении."),
        q("Где должна стоять строка документации функции?", ["Перед def", "Первой строкой тела функции", "В конце функции", "Где угодно"], 1, "Только строка первой строкой тела становится `__doc__`."),
        q("Как аннотировать параметр, который может быть строкой или None?", ["`x: str or None`", "`x: str | None`", "`x: str, None`", "`x: (str, None)`"], 1, "`str | None` (или `Optional[str]`) — объединение типов."),
    ]),
)

# ============================================================
m3 = module(f"{P}-m3", "Функции глубже", "🚀", "Функции как объекты, рекурсия и чистые функции",

lesson(f"{P}-m3-l1", "Функции как объекты", """
    # Функция — тоже значение

    ```
    def shout(s):
        return s.upper()

    f = shout            # без скобок — сама функция
    f("hi")              # "HI"

    def apply(func, value):
        return func(value)

    apply(len, "abc")    # 3
    ```

    Функции можно класть в переменные, списки, словари и передавать в другие функции.
    """,
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        def shout(s):
            return s.upper() + "!"

        f = shout
        print(f("привет"))
        print(f is shout, f.__name__)
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа?", """
        def apply_all(funcs, value):
            return [f(value) for f in funcs]

        print(apply_all([len, str.upper, str.title], "codeQuest"))
        """),
    cod(f"{P}-m3-l1-e3", t("""
        Напиши функцию `apply_twice(func, value)` — применить функцию к значению **дважды**: `func(func(value))`.

        Примеры:
        ```
        apply_twice(lambda x: x + 3, 10)   # → 16
        apply_twice(str.upper, "ab")       # → "AB"
        ```
        """),
        """
        def apply_twice(func, value):
            pass
        """,
        """
        def test_values():
            assert apply_twice(lambda x: x + 3, 10) == 16 and apply_twice(lambda x: x * 2, 1) == 4 and apply_twice(str.upper, "ab") == "AB", "Неверный результат"
        """,
        """
        def apply_twice(func, value):
            return func(func(value))
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `calculate(op, a, b)`, которая выбирает операцию из **словаря функций**:

        ```
        OPS = {"+": ..., "-": ..., "*": ..., "/": ...}
        ```

        - Вернуть результат операции `op` над `a` и `b`.
        - Если операции нет в словаре — бросить `ValueError`.

        Примеры:
        ```
        calculate("+", 2, 3)   # → 5
        calculate("/", 7, 2)   # → 3.5
        calculate("%", 1, 1)   # ValueError
        ```
        """),
        """
        def calculate(op, a, b):
            pass
        """,
        """
        def test_values():
            got = [calculate("+", 2, 3), calculate("-", 2, 3), calculate("*", 2, 3), calculate("/", 7, 2)]
            assert got == [5, -1, 6, 3.5], f"Получено {got}"

        def test_unknown():
            try:
                calculate("%", 1, 1)
            except ValueError:
                return
            assert False, "Неизвестная операция — ValueError"
        """,
        """
        OPS = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }

        def calculate(op, a, b):
            if op not in OPS:
                raise ValueError(f"неизвестная операция {op}")
            return OPS[op](a, b)
        """, xp=20),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `run_checks(value, checks)`, где `checks` — список функций-проверок, каждая возвращает `True`/`False`.

        Вернуть список **имён** проверок (`func.__name__`), которые **не прошли**.

        Пример:
        ```
        def not_empty(s): return s != ""
        def has_digit(s): return any(c.isdigit() for c in s)
        def long_enough(s): return len(s) >= 8

        run_checks("abc", [not_empty, has_digit, long_enough])
        # → ["has_digit", "long_enough"]
        ```
        """),
        """
        def run_checks(value, checks):
            pass
        """,
        """
        def not_empty(s): return s != ""
        def has_digit(s): return any(c.isdigit() for c in s)
        def long_enough(s): return len(s) >= 8

        def test_values():
            assert run_checks("abc", [not_empty, has_digit, long_enough]) == ["has_digit", "long_enough"], f"Получено {run_checks('abc', [not_empty, has_digit, long_enough])}"
            assert run_checks("abcdefg1", [not_empty, has_digit, long_enough]) == [], "Все проверки прошли"
        """,
        """
        def run_checks(value, checks):
            return [check.__name__ for check in checks if not check(value)]
        """),
    full="""
    ## Зачем это нужно

    В Python функции — «граждане первого класса»: их можно хранить в переменных и структурах данных, передавать в другие функции и возвращать из них. На этом построены `sorted(key=...)`, `map`, `filter`, обработчики событий, декораторы, фикстуры pytest, наборы проверок. Это один из самых мощных приёмов языка.

    ## Как это работает

    - Имя функции без скобок — ссылка на объект функции: `f = shout`.
    - Вызвать можно через любую ссылку: `f("hi")`.
    - Функцию можно передать аргументом: `apply(len, "abc")` — это называют **callback** (функция обратного вызова).
    - Функции можно хранить в словаре — получается «таблица диспетчеризации» вместо длинного `if/elif`.
    - У функции есть атрибуты: `__name__`, `__doc__`, `__annotations__`.

    ### Функции высшего порядка

    Функция, которая принимает или возвращает другую функцию: `sorted`, `map`, `filter`, `max(key=...)` — всё это они. Скоро ты напишешь свои — декораторы.

    ## Примеры

    ### Пример 1. Функция в переменной и в аргументе

    ```python
    def shout(s):
        return s.upper() + "!"

    def whisper(s):
        return s.lower() + "..."

    def speak(style, text):
        return style(text)

    print(speak(shout, "Тест прошёл"))
    print(speak(whisper, "Тест прошёл"))
    ```

    ### Пример 2. Словарь функций вместо if/elif

    ```python
    handlers = {
        "json": lambda data: f"JSON с {len(data)} полями",
        "text": lambda data: f"текст длиной {len(data)}",
    }

    for kind, payload in [("json", {"a": 1, "b": 2}), ("text", "hello")]:
        print(handlers[kind](payload))
    ```

    ### Пример 3. Набор проверок

    ```python
    def not_empty(s): return s != ""
    def has_digit(s): return any(c.isdigit() for c in s)
    def long_enough(s): return len(s) >= 8

    CHECKS = [not_empty, has_digit, long_enough]
    for password in ["", "abc", "abcdefg1"]:
        failed = [c.__name__ for c in CHECKS if not c(password)]
        print(repr(password), "->", failed or "ok")
    ```

    ### Пример 4. key — это тоже callback

    ```python
    tests = [("login", 1.2), ("pay", 3.4), ("cart", 0.5)]
    def by_time(t):
        return t[1]
    print(sorted(tests, key=by_time))
    print(max(tests, key=by_time)[0])
    ```

    ## Частые ошибки

    **Передали результат вместо функции** — `sorted(xs, key=len())` или `apply(shout("x"), ...)`.

    **Длинный `if/elif` по строковым командам** — часто заменяется словарём функций.

    **Лямбда там, где нужна понятная именованная функция** — именованную проще отлаживать и переиспользовать.

    ## Шпаргалка

    ```py
    f = func                  # ссылка, не вызов
    def apply(fn, x): return fn(x)
    OPS = {"+": add, "-": sub}; OPS[op](a, b)
    sorted(xs, key=fn); max(xs, key=fn)
    fn.__name__
    ```
    """,
    quiz=[
        q("Что передаётся в `sorted(words, key=len)`?", ["Результат вызова len", "Сама функция len", "Длина списка", "Строка \"len\""], 1, "В `key` передают функцию без скобок; sorted вызывает её сам."),
        q("Что вернёт `(lambda f: f(\"ab\"))(str.upper)`?", ["`\"ab\"`", "`\"AB\"`", "Ошибка", "`str.upper`"], 1, "Функция `str.upper` передана как аргумент и вызвана внутри."),
        q("Чем хорош словарь функций вместо длинного if/elif?", ["Работает только в Python 3.12", "Добавить вариант — одна строка в словаре; выбор действия — одна операция", "Он быстрее компилируется", "Ничем"], 1, "Логика выбора становится данными, код короче и расширяемее."),
    ]),

lesson(f"{P}-m3-l2", "Рекурсия", """
    # Функция вызывает сама себя

    ```
    def factorial(n):
        if n <= 1:            # базовый случай — остановка
            return 1
        return n * factorial(n - 1)   # шаг к базовому случаю
    ```

    - Обязателен **базовый случай**, иначе бесконечная рекурсия (`RecursionError`).
    - Каждый вызов должен **приближать** к базовому случаю.
    - Хорошо подходит для вложенных структур: деревья, вложенные списки, JSON.
    """,
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        def countdown(n):
            if n == 0:
                print("Старт!")
                return
            print(n)
            countdown(n - 1)

        countdown(3)
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа?", """
        def depth(item):
            if not isinstance(item, list):
                return 0
            return 1 + max((depth(x) for x in item), default=0)

        print(depth(5), depth([]), depth([1, [2, [3]]]))
        """),
    cod(f"{P}-m3-l2-e3", t("""
        Напиши **рекурсивную** функцию `factorial(n)` (без циклов).

        Примеры:
        ```
        factorial(0)   # → 1
        factorial(5)   # → 120
        ```
        """),
        """
        def factorial(n):
            pass
        """,
        """
        def test_values():
            assert [factorial(n) for n in (0, 1, 5, 10)] == [1, 1, 120, 3628800], "Неверный факториал"

        def test_recursive():
            src = open("solution.py", encoding="utf-8").read()
            assert "for " not in src and "while " not in src, "Реши без циклов — рекурсией"
        """,
        """
        def factorial(n):
            if n <= 1:
                return 1
            return n * factorial(n - 1)
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши рекурсивную функцию `deep_sum(data)` — сумма всех чисел во вложенных списках любой глубины.

        Примеры:
        ```
        deep_sum([1, [2, 3], [[4]], []])   # → 10
        deep_sum([])                       # → 0
        ```
        """),
        """
        def deep_sum(data):
            pass
        """,
        """
        def test_values():
            assert deep_sum([1, [2, 3], [[4]], []]) == 10 and deep_sum([]) == 0 and deep_sum([[[[5]]], 5]) == 10, "Неверная сумма"
        """,
        """
        def deep_sum(data):
            total = 0
            for item in data:
                if isinstance(item, list):
                    total += deep_sum(item)
                else:
                    total += item
            return total
        """, xp=20),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши рекурсивную функцию `find_keys(data, key)` — список **всех** значений по ключу `key` в JSON-подобной структуре (вложенные словари и списки).

        Пример:
        ```
        data = {"id": 1, "items": [{"id": 2}, {"meta": {"id": 3}}], "owner": {"name": "x"}}
        find_keys(data, "id")   # → [1, 2, 3]
        ```
        Порядок — обход «сначала сам словарь, потом вложенные значения по порядку».
        """),
        """
        def find_keys(data, key):
            pass
        """,
        """
        def test_values():
            data = {"id": 1, "items": [{"id": 2}, {"meta": {"id": 3}}], "owner": {"name": "x"}}
            assert find_keys(data, "id") == [1, 2, 3], f"Получено {find_keys(data, 'id')}"
            assert find_keys([], "id") == [] and find_keys(5, "id") == [], "Нет словарей — пусто"
        """,
        """
        def find_keys(data, key):
            found = []
            if isinstance(data, dict):
                if key in data:
                    found.append(data[key])
                for value in data.values():
                    found.extend(find_keys(value, key))
            elif isinstance(data, list):
                for item in data:
                    found.extend(find_keys(item, key))
            return found
        """, xp=25),
    full="""
    ## Зачем это нужно

    Некоторые задачи естественно описываются через «ту же задачу поменьше»: сумма вложенного списка = сумма элементов, где вложенный список — снова такая же задача. Рекурсия незаменима для **древовидных данных**: вложенный JSON, дерево папок, DOM-страницы, меню с подменю. В тестировании API это типично: найти все поля `id` в ответе любой вложенности.

    ## Как это работает

    Рекурсивная функция состоит из двух частей:

    1. **Базовый случай** — простая ситуация, где ответ известен без рекурсии (`n <= 1`, пустой список, «не список»).
    2. **Рекурсивный шаг** — свести задачу к меньшей и вызвать себя.

    Каждый вызов получает собственные локальные переменные и ждёт, пока вернётся вложенный. Цепочка вызовов хранится в **стеке**; у Python ограничение глубины (~1000), дальше — `RecursionError`.

    ### Рекурсия или цикл?

    - Для линейных задач (факториал, сумма списка) цикл обычно проще и быстрее.
    - Для вложенных структур рекурсия гораздо понятнее.

    ## Примеры

    ### Пример 1. Раскрутка вызовов

    ```python
    def factorial(n, indent=""):
        print(f"{indent}factorial({n})")
        if n <= 1:
            return 1
        result = n * factorial(n - 1, indent + "  ")
        print(f"{indent}= {result}")
        return result

    factorial(4)
    ```

    ### Пример 2. Вложенные списки

    ```python
    def flatten(data):
        result = []
        for item in data:
            if isinstance(item, list):
                result.extend(flatten(item))
            else:
                result.append(item)
        return result

    print(flatten([1, [2, [3, [4, []]]], 5]))
    ```

    ### Пример 3. Все id в JSON-ответе

    ```python
    def find_keys(data, key):
        found = []
        if isinstance(data, dict):
            if key in data:
                found.append(data[key])
            for value in data.values():
                found.extend(find_keys(value, key))
        elif isinstance(data, list):
            for item in data:
                found.extend(find_keys(item, key))
        return found

    resp = {"id": 1, "items": [{"id": 2, "tags": [{"id": 9}]}, {"meta": {"id": 3}}]}
    print(find_keys(resp, "id"))
    ```

    ### Пример 4. Предел глубины

    ```python
    import sys

    def infinite(n):
        return infinite(n + 1)          # нет базового случая!

    try:
        infinite(0)
    except RecursionError as e:
        print("RecursionError:", e)
    print("предел:", sys.getrecursionlimit())
    ```

    ## Частые ошибки

    **Нет базового случая** или шаг не приближает к нему — `RecursionError`.

    **Результат рекурсивного вызова не используется** — забыли `return` или `+=`.

    **Рекурсия для очень глубоких линейных данных** — упрёшься в предел; нужен цикл.

    ## Шпаргалка

    ```py
    def solve(x):
        if простой_случай(x):
            return ответ
        return объединить(solve(меньше(x)))

    isinstance(item, list) / dict — признак вложенности
    ```
    """,
    quiz=[
        q("Что обязательно должно быть в рекурсивной функции?", ["Цикл for", "Базовый случай, на котором рекурсия останавливается", "Глобальная переменная", "Декоратор"], 1, "Без базового случая вызовы продолжаются до RecursionError."),
        q("Что вернёт `f(3)` для `def f(n): return 0 if n == 0 else n + f(n - 1)`?", ["`3`", "`6`", "`0`", "`RecursionError`"], 1, "3 + 2 + 1 + 0 = 6."),
        q("Для какой задачи рекурсия подходит лучше всего?", ["Сумма чисел от 1 до 10", "Обход вложенного JSON произвольной глубины", "Вывод строки на экран", "Сортировка из двух элементов"], 1, "Рекурсия естественна для древовидных, вложенных структур."),
    ]),

lesson(f"{P}-m3-l3", "Чистые функции и побочные эффекты", """
    # Чистая функция

    - Результат зависит **только от аргументов**.
    - **Не меняет** ничего снаружи (глобальные переменные, аргументы, файлы).

    ```
    def total(prices):             # чистая
        return sum(prices)

    def add_bad(items, x):         # грязная: меняет аргумент
        items.append(x)
    ```

    Чистые функции легко тестировать и безопасно переиспользовать.
    """,
    out(f"{P}-m3-l3-e1", "Что выведет программа? Функция меняет аргумент.", """
        def add_bad(items, x):
            items.append(x)
            return items

        data = [1]
        result = add_bad(data, 2)
        print(data, result, data is result)
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа?", """
        counter = 0

        def next_id():
            global counter
            counter += 1
            return counter

        print(next_id(), next_id(), next_id())
        print(counter)
        """, hint="Функция с global зависит от внешнего состояния — одинаковый вызов даёт разные результаты."),
    cod(f"{P}-m3-l3-e3", t("""
        Функция `normalize(names)` «грязная»: она изменяет переданный список. Перепиши её **чистой** — вернуть **новый** список с именами в нижнем регистре без пробелов по краям, не трогая исходный.

        Пример:
        ```
        data = ["  Аня ", "БОРЯ"]
        normalize(data)   # → ["аня", "боря"],  data по-прежнему ["  Аня ", "БОРЯ"]
        ```
        """),
        """
        def normalize(names):
            for i in range(len(names)):
                names[i] = names[i].strip().lower()
            return names
        """,
        """
        def test_result():
            assert normalize(["  Аня ", "БОРЯ"]) == ["аня", "боря"], "Неверная нормализация"

        def test_pure():
            data = ["  Аня ", "БОРЯ"]
            normalize(data)
            assert data == ["  Аня ", "БОРЯ"], "Исходный список изменился — функция должна быть чистой"
        """,
        """
        def normalize(names):
            return [name.strip().lower() for name in names]
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Функция `apply_discount` зависит от **глобальной** переменной `DISCOUNT`, из-за чего её трудно тестировать. Перепиши её так, чтобы скидка передавалась **параметром** `percent` (по умолчанию 10).

        Примеры:
        ```
        apply_discount(1000)       # → 900.0
        apply_discount(1000, 25)   # → 750.0
        ```
        В решении не должно быть слова `global` и обращения к `DISCOUNT` внутри функции.
        """),
        """
        DISCOUNT = 10

        def apply_discount(price):
            global DISCOUNT
            return price * (1 - DISCOUNT / 100)
        """,
        """
        import inspect

        def test_values():
            assert apply_discount(1000) == 900.0 and apply_discount(1000, 25) == 750.0, "Неверная цена"

        def test_no_global():
            src = inspect.getsource(apply_discount)
            assert "global" not in src and "DISCOUNT" not in src, "Функция не должна зависеть от глобальной переменной"
        """,
        """
        def apply_discount(price, percent=10):
            return price * (1 - percent / 100)
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Раздели «грязную» функцию на **чистую** логику и действие.

        Напиши две функции:
        1. `build_report(results)` — **чистая**: по списку пар `(имя, прошёл)` возвращает строку отчёта, строки через `\\n`: `"✅ login"` / `"❌ pay"`.
        2. `print_report(results)` — печатает то, что вернула `build_report`.

        Пример:
        ```
        build_report([("login", True), ("pay", False)])   # → "✅ login\\n❌ pay"
        ```
        """),
        """
        def build_report(results):
            pass

        def print_report(results):
            pass
        """,
        """
        def test_pure():
            assert build_report([("login", True), ("pay", False)]) == "✅ login\\n❌ pay", f"Получено {build_report([('login', True), ('pay', False)])!r}"
            assert capture(build_report, [("x", True)]) == "", "build_report ничего не печатает"

        def test_print():
            assert capture(print_report, [("login", True)]).strip() == "✅ login", "print_report печатает отчёт"
        """,
        """
        def build_report(results):
            return "\\n".join(f"{'✅' if ok else '❌'} {name}" for name, ok in results)

        def print_report(results):
            print(build_report(results))
        """, xp=20),
    full="""
    ## Зачем это нужно

    Функции бывают двух видов: те, что просто **вычисляют** результат по аргументам, и те, что **меняют мир**: пишут в файл, отправляют запрос, изменяют переданный список или глобальную переменную. Первые (чистые) предсказуемы и легко тестируются. Вторые необходимы, но их лучше держать отдельно и в меньшинстве. Это один из главных принципов тестируемого кода.

    ## Как это работает

    ### Чистая функция

    1. Результат зависит **только** от аргументов: одинаковый вход → одинаковый выход.
    2. Нет **побочных эффектов**: ничего не меняется снаружи.

    `len`, `sorted`, `abs`, `str.upper` — чистые.

    ### Побочные эффекты

    - изменение аргументов (`items.append`, `d["k"] = ...`);
    - изменение глобальных переменных (`global`);
    - ввод/вывод: `print`, файлы, сеть, база данных;
    - зависимость от времени, случайности, окружения.

    ### Приём: «функциональное ядро, императивная оболочка»

    Логику выносим в чистые функции (их легко проверить `assert`-ом), а побочные действия — в тонкий слой вокруг них. В тестах это даёт возможность проверять логику без базы и сети.

    ### Зависимости — через параметры

    Вместо глобальной переменной — параметр (со значением по умолчанию). Вместо создания клиента API внутри функции — передача клиента аргументом (dependency injection).

    ## Примеры

    ### Пример 1. Грязная и чистая версии

    ```python
    def add_dirty(items, x):
        items.append(x)
        return items

    def add_pure(items, x):
        return items + [x]

    data = [1]
    add_pure(data, 2)
    print("после pure:", data)
    add_dirty(data, 2)
    print("после dirty:", data)
    ```

    ### Пример 2. Скрытая зависимость от глобального состояния

    ```python
    TAX = 20

    def price_with_tax(price):
        return price * (1 + TAX / 100)

    print(price_with_tax(100))
    TAX = 0                          # кто-то поменял «где-то далеко»
    print(price_with_tax(100))       # тот же вызов — другой результат

    def price_with_tax_pure(price, tax=20):
        return price * (1 + tax / 100)
    print(price_with_tax_pure(100), price_with_tax_pure(100, tax=0))
    ```

    ### Пример 3. Разделяем логику и вывод

    ```python
    def build_report(results):
        return "\\n".join(f"{'✅' if ok else '❌'} {name}" for name, ok in results)

    def print_report(results):
        print(build_report(results))

    results = [("login", True), ("pay", False)]
    assert build_report(results) == "✅ login\\n❌ pay"     # логику легко проверить
    print_report(results)
    ```

    ## Частые ошибки

    **Функция тихо меняет переданный список** — вызывающий код не ожидает этого.

    **`global` ради удобства** — порядок вызовов начинает влиять на результат.

    **Логика перемешана с `print`/запросами** — её невозможно протестировать без реального окружения.

    ## Шпаргалка

    ```py
    def pure(x, config=DEFAULT):   # всё нужное — в параметрах
        return new_value           # новый объект, без изменений снаружи

    def action(...):               # побочные эффекты — отдельно
        print(pure(...))
    ```
    """,
    quiz=[
        q("Какая функция чистая?", ["`def f(xs): xs.sort(); return xs`", "`def f(xs): return sorted(xs)`", "`def f(): return time.time()`", "`def f(x): print(x)`"], 1, "`sorted` создаёт новый список и не меняет аргумент; результат зависит только от входа."),
        q("Почему функции с `global` трудно тестировать?", ["Они медленные", "Результат зависит от внешнего состояния, которое может поменять любой код", "global запрещён в тестах", "Они не возвращают значения"], 1, "Одинаковый вызов может дать разные результаты."),
        q("Как сделать зависимость функции явной?", ["Использовать global", "Передать её параметром", "Прочитать из файла внутри функции", "Никак"], 1, "Параметр (или аргумент по умолчанию) делает зависимость видимой и подменяемой в тестах."),
    ]),
)

TOPIC = topic("py-functions", "Функции", "🧰", "#e05ab0",
              "def, параметры, return, значения по умолчанию, функции как объекты и рекурсия",
              m1, m2, m3, group="Python")
