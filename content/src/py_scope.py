"""Тема «Область видимости переменных»."""
from ._lib import cod, lesson, module, out, q, t, topic

P = "scp"

# ============================================================
m1 = module(f"{P}-m1", "Локальные и глобальные", "🏠", "Где живут переменные и как их менять",

lesson(f"{P}-m1-l1", "Локальные переменные", """
    # Локальная область

    ```
    def f():
        x = 10        # локальная: существует только внутри f
        return x

    f()
    print(x)          # NameError: x не определена снаружи
    ```

    - Переменные, созданные внутри функции, **локальные**.
    - Они появляются при вызове и исчезают после выхода.
    - Параметры функции — тоже локальные переменные.
    - У каждого вызова — свой набор локальных переменных.
    """,
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        def f():
            x = 10
            return x * 2

        print(f())
        try:
            print(x)
        except NameError:
            print("x не существует снаружи")
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа? Одинаковые имена в разных функциях.", """
        def a():
            value = "из a"
            return value

        def b():
            value = "из b"
            return value

        print(a(), "|", b())
        """),
    cod(f"{P}-m1-l1-e3", t("""
        Напиши функцию `make_greeting(name)`, которая создаёт **локальную** переменную `greeting` со строкой `"Привет, <имя>!"` и возвращает её.

        После вызова переменная `greeting` не должна существовать снаружи — это проверит тест.

        Пример:
        ```
        make_greeting("Аня")   # → "Привет, Аня!"
        ```
        """),
        """
        def make_greeting(name):
            pass
        """,
        """
        def test_value():
            assert make_greeting("Аня") == "Привет, Аня!", "Неверное приветствие"

        def test_local():
            make_greeting("x")
            assert "greeting" not in globals(), "greeting не должна быть глобальной"
        """,
        """
        def make_greeting(name):
            greeting = f"Привет, {name}!"
            return greeting
        """),
    cod(f"{P}-m1-l1-e4", t("""
        В коде ошибка: результат вычисления внутри функции пытаются использовать снаружи по имени локальной переменной, и программа падает с `NameError`.

        Исправь: функция `total_price(prices)` должна **вернуть** сумму, а снаружи результат нужно сохранить в переменную `total` и напечатать.

        Ожидаемый вывод:
        ```
        450
        ```
        """),
        """
        def total_price(prices):
            s = sum(prices)

        total_price([100, 200, 150])
        print(s)
        """,
        """
        def test_output():
            assert OUTPUT.strip() == "450", f"Напечатано {OUTPUT.strip()!r}"

        def test_function():
            assert total_price([1, 2]) == 3, "total_price должна возвращать сумму"
            assert total == 450, "Результат сохрани в переменную total"
        """,
        """
        def total_price(prices):
            s = sum(prices)
            return s

        total = total_price([100, 200, 150])
        print(total)
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `call_counter_demo()`, которая **трижды** вызывает вложенную логику: внутри неё объяви функцию `step()`, у которой есть локальная переменная `n = 0`, увеличивающаяся на 1 и возвращаемая.

        Вернуть список результатов трёх вызовов `step()`.

        Результат покажет, что локальные переменные создаются **заново** при каждом вызове:
        ```
        call_counter_demo()   # → [1, 1, 1]
        ```
        """),
        """
        def call_counter_demo():
            pass
        """,
        """
        def test_values():
            assert call_counter_demo() == [1, 1, 1], f"Получено {call_counter_demo()}"
        """,
        """
        def call_counter_demo():
            def step():
                n = 0
                n += 1
                return n
            return [step(), step(), step()]
        """),
    full="""
    ## Зачем это нужно

    Область видимости (scope) определяет, **где** переменная существует и откуда к ней можно обратиться. Это защищает от хаоса: переменная `result` в одной функции не ломает `result` в другой. Непонимание областей видимости даёт загадочные `NameError` и `UnboundLocalError` и «почему мой счётчик не растёт».

    ## Как это работает

    ### Локальная область

    Каждый **вызов** функции создаёт свою локальную область:
    - туда попадают параметры и все переменные, которым внутри функции что-то **присваивается**;
    - при выходе из функции область исчезает вместе с переменными (если на них не ссылается замыкание — это позже);
    - следующий вызов начинает с чистого листа.

    Поэтому результат работы функции нужно **возвращать** — к её локальным переменным снаружи не добраться.

    ### Одинаковые имена

    Переменные с одним именем в разных функциях — **разные** переменные. Это нормально и удобно.

    ### Блоки if/for — не области

    В Python, в отличие от многих языков, `if`, `for`, `while` **не создают** новой области: переменная, созданная внутри цикла, видна после него (в той же функции).

    ## Примеры

    ### Пример 1. Локальная переменная не видна снаружи

    ```python
    def compute():
        result = 42
        return result

    value = compute()
    print(value)
    try:
        print(result)
    except NameError as e:
        print("NameError:", e)
    ```

    ### Пример 2. Каждый вызов — заново

    ```python
    def attempt():
        count = 0
        count += 1
        return count

    print(attempt(), attempt(), attempt())
    ```

    ### Пример 3. Блоки не создают области

    ```python
    def demo():
        for i in range(3):
            last = i * 10
        if True:
            flag = "видно"
        return i, last, flag

    print(demo())
    ```

    ### Пример 4. Параметры — локальные

    ```python
    def double(x):
        x = x * 2
        return x

    x = 5
    print(double(x), x)
    ```

    ## Частые ошибки

    **Обращение к локальной переменной снаружи** — `NameError`; нужно вернуть значение.

    **Ожидание, что локальная переменная «помнит» значение между вызовами.**

    **Путаница: присваивание параметру внутри функции меняет внешнюю переменную** — нет, меняется только локальное имя.

    ## Шпаргалка

    ```py
    def f(a):
        b = a + 1     # a, b — локальные
        return b      # единственный путь наружу
    res = f(1)
    ```
    """,
    quiz=[
        q("Что произойдёт при `print(y)` после вызова `def f(): y = 1` и `f()`?", ["Выведет 1", "`NameError`", "Выведет None", "Выведет 0"], 1, "y — локальная переменная f и снаружи не существует."),
        q("Создаёт ли цикл `for` внутри функции новую область видимости?", ["Да", "Нет, переменные цикла видны в функции после цикла", "Только для счётчика", "Только в Python 2"], 1, "Области создают функции (и классы, модули), а не блоки."),
        q("Как передать результат вычисления из функции наружу?", ["Через локальную переменную с тем же именем", "Через return", "Через print", "Никак"], 1, "return — основной путь наружу."),
    ]),

lesson(f"{P}-m1-l2", "Глобальные переменные", """
    # Глобальная область

    ```
    TIMEOUT = 30          # глобальная: объявлена на уровне модуля

    def request():
        return f"таймаут {TIMEOUT}"   # читать глобальную можно
    ```

    - Переменные на верхнем уровне файла — **глобальные**.
    - Функция может их **читать** без ограничений.
    - Если внутри функции **присвоить** значение — создастся **локальная** переменная с тем же именем.
    """,
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        TIMEOUT = 30

        def show():
            return f"таймаут {TIMEOUT}"

        print(show())
        TIMEOUT = 60
        print(show())
        """, hint="Функция читает глобальную переменную в момент вызова."),
    out(f"{P}-m1-l2-e2", "Что выведет программа? Присваивание создаёт локальную.", """
        x = "глобальная"

        def f():
            x = "локальная"
            return x

        print(f())
        print(x)
        """),
    cod(f"{P}-m1-l2-e3", t("""
        Есть глобальная константа `BASE_URL = "https://api.shop.ru"`. Напиши функцию `endpoint(path)`, которая **читает** её и возвращает полный адрес.

        Пример:
        ```
        endpoint("/users")   # → "https://api.shop.ru/users"
        ```
        """),
        """
        BASE_URL = "https://api.shop.ru"

        def endpoint(path):
            pass
        """,
        """
        def test_values():
            assert endpoint("/users") == "https://api.shop.ru/users", "Неверный адрес"

        def test_reads_global():
            g = endpoint.__globals__
            old = g["BASE_URL"]
            g["BASE_URL"] = "http://localhost"
            try:
                assert endpoint("/x") == "http://localhost/x", "Функция должна читать глобальную BASE_URL, а не хардкодить адрес"
            finally:
                g["BASE_URL"] = old
        """,
        """
        BASE_URL = "https://api.shop.ru"

        def endpoint(path):
            return BASE_URL + path
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `describe_env()`, которая возвращает строку `"<ENV>: <BROWSER>"`, используя глобальные настройки `ENV` и `BROWSER`, объявленные в заготовке.

        ```
        describe_env()   # → "staging: chrome"
        ```
        Не создавай внутри функции переменных с такими же именами.
        """),
        """
        ENV = "staging"
        BROWSER = "chrome"

        def describe_env():
            pass
        """,
        """
        def test_value():
            assert describe_env() == "staging: chrome", f"Получено {describe_env()!r}"
        """,
        """
        ENV = "staging"
        BROWSER = "chrome"

        def describe_env():
            return f"{ENV}: {BROWSER}"
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Функция `apply_tax` должна использовать глобальную ставку `TAX = 20`, но вместо этого всегда считает с нулевым налогом: внутри неё по ошибке создаётся **локальная** переменная `TAX = 0`.

        Исправь функцию — она должна читать глобальную ставку.

        ```
        apply_tax(100)   # → 120.0
        ```
        """),
        """
        TAX = 20

        def apply_tax(price):
            TAX = 0
            return price * (1 + TAX / 100)
        """,
        """
        def test_value():
            assert apply_tax(100) == 120.0, f"Получено {apply_tax(100)}"
        """,
        """
        TAX = 20

        def apply_tax(price):
            return price * (1 + TAX / 100)
        """),
    full="""
    ## Зачем это нужно

    На уровне модуля обычно живут константы и настройки: базовый URL API, таймауты, имя браузера. Функции читают их отовсюду. Важно понимать разницу между **чтением** глобальной переменной (можно всегда) и **присваиванием** ей внутри функции (создаёт локальную переменную).

    ## Как это работает

    ### Глобальная область

    Всё, что определено на верхнем уровне файла (модуля): переменные, функции, импорты. Живёт, пока работает программа.

    ### Чтение

    Если внутри функции используется имя, которое не присваивается в ней, Python ищет его снаружи — в глобальной области. Значение берётся **в момент вызова**, а не в момент объявления функции.

    ### Присваивание создаёт локальную

    ```py
    x = 1
    def f():
        x = 2      # новая ЛОКАЛЬНАЯ x; глобальная не меняется
    ```

    Python решает, локальная ли переменная, **при компиляции функции**: если где-то в теле функции есть присваивание имени — оно локальное во всей функции.

    ### Константы

    По соглашению неизменяемые настройки пишут `ЗАГЛАВНЫМИ`: `BASE_URL`, `MAX_RETRIES`. Это сигнал «не менять».

    ## Примеры

    ### Пример 1. Чтение в момент вызова

    ```python
    MAX_RETRIES = 3

    def plan():
        return f"до {MAX_RETRIES} попыток"

    print(plan())
    MAX_RETRIES = 5
    print(plan())
    ```

    ### Пример 2. Присваивание не меняет глобальную

    ```python
    counter = 0

    def increment():
        counter = 1           # локальная
        return counter

    print(increment(), counter)
    ```

    ### Пример 3. Настройки модуля

    ```python
    BASE_URL = "https://staging.shop.ru"
    TIMEOUT = 10

    def request_line(method, path):
        return f"{method} {BASE_URL}{path} (timeout={TIMEOUT}s)"

    print(request_line("GET", "/api/users"))
    ```

    ### Пример 4. Функции — тоже глобальные имена

    ```python
    def helper():
        return "помощник"

    def main():
        return helper() + " вызван из main"

    print(main())
    ```

    ## Частые ошибки

    **Ожидание, что присваивание внутри функции изменит глобальную переменную.**

    **Случайное «затенение»** — локальная переменная с именем глобальной скрывает её.

    **Изменяемое глобальное состояние** — функции начинают зависеть от порядка вызовов (об этом в следующем уроке).

    ## Шпаргалка

    ```py
    CONFIG = "..."          # глобальная константа
    def f():
        return CONFIG       # читать — можно
    def g():
        CONFIG = "x"        # это ЛОКАЛЬНАЯ переменная
    ```
    """,
    quiz=[
        q("Что выведет код?\n```py\nx = 1\ndef f():\n    x = 2\nf()\nprint(x)\n```", ["`2`", "`1`", "Ошибка", "`None`"], 1, "Присваивание внутри f создало локальную x; глобальная не изменилась."),
        q("Когда функция берёт значение глобальной переменной, которую только читает?", ["При объявлении функции", "В момент вызова", "При запуске программы", "Никогда"], 1, "Имя ищется при каждом обращении во время выполнения."),
        q("Что означает имя переменной ЗАГЛАВНЫМИ буквами?", ["Ошибку", "Соглашение: это константа, её не меняют", "Глобальную область автоматически", "Приватную переменную"], 1, "Python не запрещает изменение, но это договорённость."),
    ]),

lesson(f"{P}-m1-l3", "global и почему лучше без него", """
    # Изменение глобальной переменной

    ```
    counter = 0

    def increment():
        global counter      # разрешить изменение глобальной
        counter += 1
    ```

    Без `global` строка `counter += 1` даст `UnboundLocalError`.

    ⚠️ Изменяемое глобальное состояние делает код хрупким и трудно тестируемым. Обычно лучше **передать значение параметром и вернуть результат**.
    """,
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        counter = 0

        def increment():
            global counter
            counter += 1
            return counter

        increment()
        increment()
        print(counter)
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа? UnboundLocalError.", """
        total = 10

        def add():
            try:
                total += 5
            except UnboundLocalError as e:
                return "ошибка: " + type(e).__name__
            return total

        print(add())
        """, hint="Присваивание делает total локальной во всей функции, а читать её до присваивания нельзя."),
    cod(f"{P}-m1-l3-e3", t("""
        Функция `register()` должна увеличивать **глобальный** счётчик `users_count` на 1 и возвращать новое значение. Сейчас она падает с `UnboundLocalError`.

        Исправь с помощью `global`.

        ```
        register()   # → 1
        register()   # → 2
        ```
        """),
        """
        users_count = 0

        def register():
            users_count += 1
            return users_count
        """,
        """
        def test_values():
            g = register.__globals__
            g["users_count"] = 0
            assert register() == 1 and register() == 2 and g["users_count"] == 2, "Глобальный счётчик должен расти"
        """,
        """
        users_count = 0

        def register():
            global users_count
            users_count += 1
            return users_count
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Перепиши код **без `global`**: функция `add_points(score, points)` получает текущий счёт параметром и **возвращает** новый.

        Снаружи обнови переменную `score` результатом двух вызовов (+10, затем +5) и выведи её.

        Ожидаемый вывод:
        ```
        15
        ```
        """),
        """
        score = 0

        def add_points(points):
            global score
            score += points

        add_points(10)
        add_points(5)
        print(score)
        """,
        """
        import inspect

        def test_output():
            assert OUTPUT.strip() == "15", f"Напечатано {OUTPUT.strip()!r}"

        def test_pure():
            assert add_points(3, 4) == 7, "add_points(score, points) должна вернуть сумму"
            assert "global" not in open("solution.py", encoding="utf-8").read(), "Избавься от global"
        """,
        """
        def add_points(score, points):
            return score + points

        score = 0
        score = add_points(score, 10)
        score = add_points(score, 5)
        print(score)
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Сделай счётчик запросов **без `global`**: напиши класс-хранилище не нужно — используй **словарь** состояния, который передаётся в функцию.

        Функция `track(stats, endpoint)` увеличивает счётчик вызовов для `endpoint` в словаре `stats` (изменяя его) и возвращает новое значение счётчика.

        ```
        stats = {}
        track(stats, "/users")   # → 1
        track(stats, "/users")   # → 2
        track(stats, "/items")   # → 1
        stats                    # → {"/users": 2, "/items": 1}
        ```
        """),
        """
        def track(stats, endpoint):
            pass
        """,
        """
        def test_values():
            stats = {}
            assert [track(stats, "/users"), track(stats, "/users"), track(stats, "/items")] == [1, 2, 1], "Неверные счётчики"
            assert stats == {"/users": 2, "/items": 1}, f"Состояние: {stats}"

        def test_no_global():
            assert "global" not in open("solution.py", encoding="utf-8").read(), "Реши без global"
        """,
        """
        def track(stats, endpoint):
            stats[endpoint] = stats.get(endpoint, 0) + 1
            return stats[endpoint]
        """),
    full="""
    ## Зачем это нужно

    Иногда кажется удобным хранить состояние в глобальной переменной: счётчик вызовов, текущего пользователя, открытую сессию. Python разрешает менять глобальную переменную из функции через `global`, но это почти всегда источник проблем — особенно в тестах, где один тест «загрязняет» состояние для следующего.

    ## Как это работает

    ### UnboundLocalError

    ```py
    total = 10
    def add():
        total += 5      # UnboundLocalError
    ```

    Раз в функции есть присваивание `total`, Python считает `total` **локальной во всей функции**. А `total += 5` сначала читает локальную `total`, которой ещё нет.

    ### global

    `global имя` в начале функции говорит: «это имя — глобальная переменная, присваивания меняют её».

    ### Почему лучше без global

    - **Скрытая зависимость**: по сигнатуре функции не видно, что она читает и меняет.
    - **Зависимость от порядка вызовов**: результат зависит от того, что вызывали раньше.
    - **Тесты влияют друг на друга**: глобальное состояние переживает тест.
    - **Параллельный запуск** ломается.

    ### Альтернативы

    1. Передать значение параметром и **вернуть** новое.
    2. Передать изменяемый контейнер (словарь, объект) явно.
    3. Инкапсулировать состояние в объекте класса или замыкании.

    ## Примеры

    ### Пример 1. Ошибка и её причина

    ```python
    total = 10

    def add_broken():
        total += 5

    try:
        add_broken()
    except UnboundLocalError as e:
        print("UnboundLocalError:", e)
    ```

    ### Пример 2. global работает, но…

    ```python
    calls = 0

    def api_call():
        global calls
        calls += 1
        return f"вызов №{calls}"

    print(api_call(), api_call())
    calls = 0                        # «кто-то» сбросил снаружи
    print(api_call())
    ```

    ### Пример 3. Явное состояние

    ```python
    def add_points(score, points):
        return score + points

    score = 0
    for p in [10, 5, 20]:
        score = add_points(score, p)
    print(score)
    ```

    ### Пример 4. Состояние в словаре

    ```python
    def track(stats, endpoint):
        stats[endpoint] = stats.get(endpoint, 0) + 1

    run1, run2 = {}, {}
    track(run1, "/users"); track(run1, "/users")
    track(run2, "/items")
    print(run1, run2)          # прогоны не мешают друг другу
    ```

    ## Частые ошибки

    **`x += 1` без `global`** для глобальной `x` — `UnboundLocalError`.

    **`global` «на всякий случай»** там, где переменная только читается — не нужен.

    **Тесты, полагающиеся на глобальное состояние** — работают по одному и падают вместе.

    ## Шпаргалка

    ```py
    def f():
        global count; count += 1      # можно, но избегай
    def f(count):
        return count + 1              # лучше: явный вход и выход
    ```
    """,
    quiz=[
        q("Почему `x += 1` внутри функции падает с `UnboundLocalError`, если `x` глобальная?", ["Нельзя складывать", "Присваивание делает x локальной во всей функции, а её ещё нет", "global запрещён", "x неизменяемая"], 1, "Python решает про локальность по наличию присваивания в теле функции."),
        q("Нужен ли `global`, чтобы только прочитать глобальную переменную?", ["Да", "Нет", "Только для строк", "Только в классах"], 1, "`global` нужен лишь для присваивания."),
        q("Почему глобальное изменяемое состояние вредно в тестах?", ["Замедляет тесты", "Тесты начинают зависеть друг от друга и от порядка запуска", "Оно запрещено pytest", "Не вредно"], 1, "Состояние, изменённое одним тестом, видят следующие."),
    ]),
)

# ============================================================
m2 = module(f"{P}-m2", "Вложенные функции", "🪆", "Правило LEGB, nonlocal и замыкания",

lesson(f"{P}-m2-l1", "Правило LEGB", """
    # Порядок поиска имени

    **L**ocal → **E**nclosing → **G**lobal → **B**uilt-in

    1. локальная область текущей функции;
    2. области внешних (объемлющих) функций;
    3. глобальная область модуля;
    4. встроенные имена (`len`, `print`, `list`…).

    Используется **первое** найденное.
    """,
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        x = "global"

        def outer():
            x = "enclosing"
            def inner():
                return x
            return inner()

        print(outer())
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа?", """
        x = "global"

        def outer():
            def inner():
                return x
            return inner()

        def outer2():
            x = "enclosing"
            def inner():
                x = "local"
                return x
            return inner(), x

        print(outer())
        print(outer2())
        """),
    cod(f"{P}-m2-l1-e3", t("""
        Напиши функцию `make_formatter(prefix)`, внутри которой объяви функцию `fmt(message)`, возвращающую `"<prefix>: <message>"`. Вложенная функция должна брать `prefix` из **объемлющей** области. `make_formatter` возвращает результат `fmt("готово")`.

        ```
        make_formatter("INFO")   # → "INFO: готово"
        ```
        """),
        """
        def make_formatter(prefix):
            pass
        """,
        """
        def test_value():
            assert make_formatter("INFO") == "INFO: готово" and make_formatter("ERR") == "ERR: готово", "Неверная строка"
        """,
        """
        def make_formatter(prefix):
            def fmt(message):
                return f"{prefix}: {message}"
            return fmt("готово")
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `which_scope()`, возвращающую список из трёх строк: значение переменной `level`, полученное из **трёх** уровней.

        Структура:
        - глобальная `level = "G"` (уже в заготовке);
        - внутри `which_scope` — `level = "E"` и вложенная функция `inner()`, где `level = "L"`;
        - `inner` возвращает свою `level`, а `which_scope` возвращает `[inner(), level, глобальная level]`.

        ```
        which_scope()   # → ["L", "E", "G"]
        ```
        Глобальную прочитай через `globals()["level"]`.
        """),
        """
        level = "G"

        def which_scope():
            pass
        """,
        """
        def test_value():
            assert which_scope() == ["L", "E", "G"], f"Получено {which_scope()}"
        """,
        """
        level = "G"

        def which_scope():
            level = "E"
            def inner():
                level = "L"
                return level
            return [inner(), level, globals()["level"]]
        """),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `count_items(items)`, которая использует встроенную `len` — **но** в заготовке глобально объявлена переменная `len = 5`, которая «ломает» встроенную функцию.

        Исправь заготовку так, чтобы `count_items` работала: удали затеняющую переменную.

        ```
        count_items([1, 2, 3])   # → 3
        ```
        """),
        """
        len = 5

        def count_items(items):
            return len(items)
        """,
        """
        def test_value():
            assert count_items([1, 2, 3]) == 3 and count_items([]) == 0, "count_items должна вернуть длину"
        """,
        """
        def count_items(items):
            return len(items)
        """),
    full="""
    ## Зачем это нужно

    Когда функции вложены друг в друга, а имена совпадают, важно точно знать, какую переменную увидит код. Правило LEGB объясняет всё: от «почему внутренняя функция видит переменную внешней» до «почему после `list = [...]` перестала работать функция `list()`».

    ## Как это работает

    Встретив имя, Python ищет его по порядку:

    1. **L — Local**: локальная область текущей функции.
    2. **E — Enclosing**: области объемлющих функций, от ближайшей к дальней.
    3. **G — Global**: область модуля.
    4. **B — Built-in**: встроенные имена (`len`, `print`, `sum`, `list`, `Exception`…).

    Берётся **первое** найденное. Если нигде — `NameError`.

    ### Следствия

    - Вложенная функция может **читать** переменные внешней (это основа замыканий).
    - Локальное имя **затеняет** одноимённые снаружи.
    - Глобальная переменная с именем встроенной функции её «ломает» — `len = 5` сделает `len(...)` ошибкой во всём модуле.

    Посмотреть содержимое областей: `locals()`, `globals()`, модуль `builtins`.

    ## Примеры

    ### Пример 1. Все четыре уровня

    ```python
    x = "G"

    def outer():
        x = "E"
        def inner():
            x = "L"
            return x
        return inner(), x

    print(outer(), x)
    print(len("B — встроенная функция len"))
    ```

    ### Пример 2. Чтение из объемлющей области

    ```python
    def make_report(title):
        lines = []
        def add(line):
            lines.append(f"[{title}] {line}")    # title и lines — из outer
        add("старт")
        add("финиш")
        return lines

    print(make_report("smoke"))
    ```

    ### Пример 3. Сломанная встроенная функция

    ```python
    list = [1, 2, 3]
    try:
        list("abc")
    except TypeError as e:
        print("TypeError:", e)
    del list                     # вернуть встроенную
    print(list("abc"))
    ```

    ## Частые ошибки

    **Имена переменных как у встроенных**: `list`, `dict`, `str`, `id`, `type`, `input`, `sum`, `max`.

    **Ожидание, что внутренняя функция увидит переменную, созданную после её вызова.**

    **Путаница «читать можно — присваивать нельзя»** для внешних переменных (решение — `nonlocal`, следующий урок).

    ## Шпаргалка

    ```text
    Local → Enclosing → Global → Built-in
    первое найденное имя побеждает
    не называй переменные list, dict, str, id, sum…
    ```
    """,
    quiz=[
        q("В каком порядке Python ищет имя?", ["Global → Local → Built-in", "Local → Enclosing → Global → Built-in", "Built-in → Global → Local", "Случайно"], 1, "Правило LEGB."),
        q("Что станет с `len(\"abc\")` после строки `len = 3` на уровне модуля?", ["Вернёт 3", "`TypeError`: int не вызывается", "Вернёт 3 символа", "Ничего не изменится"], 1, "Глобальное имя len затенило встроенную функцию."),
        q("Может ли вложенная функция читать переменную внешней функции?", ["Нет", "Да, через объемлющую (E) область", "Только через global", "Только если она константа"], 1, "Это Enclosing-уровень LEGB."),
    ]),

lesson(f"{P}-m2-l2", "nonlocal", """
    # Изменение переменной внешней функции

    ```
    def counter():
        count = 0
        def inc():
            nonlocal count     # count — из объемлющей функции
            count += 1
            return count
        return inc
    ```

    - `nonlocal` — как `global`, но для ближайшей **объемлющей функции**.
    - Без него присваивание создаёт локальную переменную (`UnboundLocalError`).
    - Изменять содержимое списка/словаря можно и без `nonlocal`.
    """,
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        def outer():
            count = 0
            def inc():
                nonlocal count
                count += 1
            inc()
            inc()
            return count

        print(outer())
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа? Список меняется без nonlocal.", """
        def outer():
            log = []
            total = 0
            def add(x):
                log.append(x)
            add(1)
            add(2)
            return log, total

        print(outer())
        """, hint="append меняет объект, а не переменную; присваивания нет — nonlocal не нужен."),
    cod(f"{P}-m2-l2-e3", t("""
        Функция `sum_with_helper(nums)` должна суммировать числа через вложенную функцию `add(x)`, которая увеличивает переменную `total` внешней функции. Сейчас она падает с `UnboundLocalError`.

        Исправь с помощью `nonlocal`.

        ```
        sum_with_helper([1, 2, 3])   # → 6
        ```
        """),
        """
        def sum_with_helper(nums):
            total = 0
            def add(x):
                total += x
            for n in nums:
                add(n)
            return total
        """,
        """
        def test_value():
            assert sum_with_helper([1, 2, 3]) == 6 and sum_with_helper([]) == 0, "Неверная сумма"
        """,
        """
        def sum_with_helper(nums):
            total = 0
            def add(x):
                nonlocal total
                total += x
            for n in nums:
                add(n)
            return total
        """),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `make_counter()`, которая возвращает **функцию** `inc()`: каждый вызов `inc()` увеличивает внутренний счётчик на 1 и возвращает его. Используй `nonlocal`.

        ```
        c = make_counter()
        c(), c(), c()      # → 1, 2, 3
        d = make_counter()
        d()                # → 1   у каждого счётчика своё состояние
        ```
        """),
        """
        def make_counter():
            pass
        """,
        """
        def test_counter():
            c = make_counter()
            assert [c(), c(), c()] == [1, 2, 3], "Счётчик должен расти"
            d = make_counter()
            assert d() == 1 and c() == 4, "Счётчики независимы"

        def test_nonlocal():
            assert "nonlocal" in open("solution.py", encoding="utf-8").read(), "Используй nonlocal"
        """,
        """
        def make_counter():
            count = 0
            def inc():
                nonlocal count
                count += 1
                return count
            return inc
        """),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `make_accumulator(start=0)`, возвращающую функцию `add(x)`: она прибавляет `x` к накопленной сумме и возвращает новую сумму. Также у возвращаемой функции должна быть возможность **сбросить** сумму вызовом `add(reset=True)` (вернуть `start`).

        ```
        acc = make_accumulator(10)
        acc(5)            # → 15
        acc(5)            # → 20
        acc(reset=True)   # → 10
        acc(1)            # → 11
        ```
        """),
        """
        def make_accumulator(start=0):
            pass
        """,
        """
        def test_values():
            acc = make_accumulator(10)
            assert [acc(5), acc(5), acc(reset=True), acc(1)] == [15, 20, 10, 11], "Неверные суммы"
            other = make_accumulator()
            assert other(3) == 3, "Независимые аккумуляторы"
        """,
        """
        def make_accumulator(start=0):
            total = start
            def add(x=0, reset=False):
                nonlocal total
                if reset:
                    total = start
                else:
                    total += x
                return total
            return add
        """, xp=20),
    full="""
    ## Зачем это нужно

    Вложенные функции часто должны не только читать, но и **менять** переменные внешней функции: считать вызовы, накапливать результат, помнить состояние. `nonlocal` делает это возможным без глобальных переменных — состояние остаётся спрятанным внутри.

    ## Как это работает

    ```py
    def outer():
        count = 0
        def inner():
            nonlocal count
            count += 1
    ```

    - `nonlocal имя` связывает имя с переменной ближайшей **объемлющей функции** (не глобальной!).
    - Без `nonlocal` присваивание сделает имя локальным для `inner` → `UnboundLocalError` при `+=`.
    - Переменная должна уже существовать во внешней функции.

    ### Когда nonlocal не нужен

    Если ты не **присваиваешь** имя, а меняешь объект — `lst.append(x)`, `d[k] = v` — `nonlocal` не нужен: переменная указывает на тот же объект.

    ### global против nonlocal

    - `global` — переменная модуля;
    - `nonlocal` — переменная внешней функции.

    ## Примеры

    ### Пример 1. Без nonlocal и с ним

    ```python
    def broken():
        count = 0
        def inc():
            count += 1
        try:
            inc()
        except UnboundLocalError as e:
            return f"ошибка: {e}"

    def fixed():
        count = 0
        def inc():
            nonlocal count
            count += 1
        inc(); inc()
        return count

    print(broken())
    print(fixed())
    ```

    ### Пример 2. Независимые счётчики

    ```python
    def make_counter():
        count = 0
        def inc():
            nonlocal count
            count += 1
            return count
        return inc

    requests_counter = make_counter()
    errors_counter = make_counter()
    requests_counter(); requests_counter(); errors_counter()
    print(requests_counter(), errors_counter())
    ```

    ### Пример 3. Изменяемый объект — nonlocal не нужен

    ```python
    def collect():
        items = []
        def add(x):
            items.append(x)        # изменение объекта
        for i in range(3):
            add(i)
        return items

    print(collect())
    ```

    ## Частые ошибки

    **`nonlocal` для глобальной переменной** — `SyntaxError: no binding for nonlocal found`.

    **`nonlocal` там, где только читают** — не нужен.

    **Забыли `nonlocal` при `+=`** — `UnboundLocalError`.

    ## Шпаргалка

    ```py
    def outer():
        n = 0
        def inner():
            nonlocal n
            n += 1
        return inner
    ```
    """,
    quiz=[
        q("Чем `nonlocal` отличается от `global`?", ["Ничем", "`nonlocal` ссылается на переменную объемлющей функции, `global` — на переменную модуля", "`nonlocal` работает только со списками", "`global` устарел"], 1, "Разные уровни LEGB: Enclosing и Global."),
        q("Нужен ли `nonlocal`, чтобы вызвать `items.append(x)` для списка из внешней функции?", ["Да", "Нет, объект меняется без присваивания имени", "Только в Python 2", "Нужен global"], 1, "nonlocal нужен только для присваивания имени."),
        q("Что будет при `nonlocal x`, если во внешних функциях нет переменной x?", ["Создастся новая", "`SyntaxError`", "Возьмётся глобальная", "Ничего"], 1, "nonlocal требует существующей переменной в объемлющей функции."),
    ]),

lesson(f"{P}-m2-l3", "Замыкания", """
    # Функция, которая помнит окружение

    ```
    def multiplier(n):
        def mul(x):
            return x * n      # n «запомнилось»
        return mul

    triple = multiplier(3)
    triple(5)                 # 15
    ```

    Внутренняя функция сохраняет доступ к переменным внешней даже **после** её завершения.
    Так делают фабрики функций, счётчики, кэши, декораторы.
    """,
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        def multiplier(n):
            def mul(x):
                return x * n
            return mul

        double, triple = multiplier(2), multiplier(3)
        print(double(10), triple(10))
        """),
    out(f"{P}-m2-l3-e2", "Что выведет программа? Ловушка позднего связывания.", """
        funcs = []
        for i in range(3):
            funcs.append(lambda: i)
        print([f() for f in funcs])

        fixed = []
        for i in range(3):
            fixed.append(lambda i=i: i)
        print([f() for f in fixed])
        """, hint="Замыкание помнит переменную, а не её значение в момент создания."),
    cod(f"{P}-m2-l3-e3", t("""
        Напиши функцию `make_validator(min_len)` — фабрику проверок: возвращает функцию, которая получает строку и возвращает `True`, если её длина не меньше `min_len`.

        ```
        check8 = make_validator(8)
        check8("12345678")   # → True
        check8("123")        # → False
        ```
        """),
        """
        def make_validator(min_len):
            pass
        """,
        """
        def test_values():
            check8, check2 = make_validator(8), make_validator(2)
            assert check8("12345678") is True and check8("123") is False and check2("ab") is True, "Неверная проверка"
        """,
        """
        def make_validator(min_len):
            def check(s):
                return len(s) >= min_len
            return check
        """),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `make_cache(func)` — возвращает новую функцию, которая вызывает `func(x)` только при **первом** обращении с этим `x`, а дальше берёт результат из словаря-кэша (в замыкании).

        У возвращаемой функции должен быть атрибут-счётчик реальных вызовов недоступен — поэтому проверка сделает сама: `func` будет считать свои вызовы.

        ```
        slow_square = ...   # считает вызовы
        fast = make_cache(slow_square)
        fast(4), fast(4), fast(5)    # → 16, 16, 25; реальных вызовов — 2
        ```
        """),
        """
        def make_cache(func):
            pass
        """,
        """
        def test_cache():
            calls = []
            def slow_square(x):
                calls.append(x)
                return x * x
            fast = make_cache(slow_square)
            assert [fast(4), fast(4), fast(5), fast(4)] == [16, 16, 25, 16], "Неверные результаты"
            assert calls == [4, 5], f"Реальные вызовы: {calls} — повторы должны браться из кэша"
        """,
        """
        def make_cache(func):
            cache = {}
            def cached(x):
                if x not in cache:
                    cache[x] = func(x)
                return cache[x]
            return cached
        """, xp=20),
    cod(f"{P}-m2-l3-e5", t("""
        Исправь ловушку позднего связывания: функция `make_handlers(names)` должна вернуть список функций, каждая из которых возвращает **свою** строку `"обработчик <имя>"`. Сейчас все возвращают последнее имя.

        ```
        hs = make_handlers(["a", "b", "c"])
        [h() for h in hs]   # → ["обработчик a", "обработчик b", "обработчик c"]
        ```
        """),
        """
        def make_handlers(names):
            handlers = []
            for name in names:
                handlers.append(lambda: f"обработчик {name}")
            return handlers
        """,
        """
        def test_values():
            hs = make_handlers(["a", "b", "c"])
            assert [h() for h in hs] == ["обработчик a", "обработчик b", "обработчик c"], f"Получено {[h() for h in hs]}"
        """,
        """
        def make_handlers(names):
            handlers = []
            for name in names:
                handlers.append(lambda name=name: f"обработчик {name}")
            return handlers
        """,
        hint="Зафиксируй значение аргументом по умолчанию: `lambda name=name: ...`."),
    full="""
    ## Зачем это нужно

    Замыкание — функция, которая «запомнила» переменные из места, где её создали. На этом построены фабрики функций (`make_validator(8)`), счётчики без глобальных переменных, кэширование, декораторы, фикстуры pytest. Это одна из ключевых идей Python, без которой не понять следующие темы.

    ## Как это работает

    ```py
    def multiplier(n):
        def mul(x):
            return x * n
        return mul          # возвращаем саму функцию, не вызов
    ```

    1. `multiplier(3)` создаёт локальную `n = 3` и функцию `mul`.
    2. `mul` ссылается на `n` из объемлющей области.
    3. `multiplier` завершилась, но `n` не исчезла — её держит `mul`.
    4. Каждый вызов `multiplier` создаёт **новую** пару «функция + её переменные».

    Запомненные переменные хранятся в `func.__closure__`.

    ### Позднее связывание

    Замыкание помнит **переменную**, а не её значение в момент создания. Значение читается при **вызове**. Поэтому функции, созданные в цикле, увидят **последнее** значение переменной цикла.

    Лечение — зафиксировать значение: аргумент по умолчанию (`lambda i=i: i`) или отдельная функция-фабрика.

    ## Примеры

    ### Пример 1. Фабрика функций

    ```python
    def make_greeter(greeting):
        def greet(name):
            return f"{greeting}, {name}!"
        return greet

    hello = make_greeter("Привет")
    hi = make_greeter("Хай")
    print(hello("Аня"), hi("Боря"))
    print(hello.__closure__[0].cell_contents)
    ```

    ### Пример 2. Кэш в замыкании

    ```python
    def make_cache(func):
        cache = {}
        def cached(x):
            if x not in cache:
                print("  вычисляю", x)
                cache[x] = func(x)
            return cache[x]
        return cached

    square = make_cache(lambda x: x * x)
    print(square(4), square(4), square(5))
    ```

    ### Пример 3. Позднее связывание и лечение

    ```python
    late = [lambda: i for i in range(3)]
    early = [lambda i=i: i for i in range(3)]

    def factory(i):
        return lambda: i
    via_factory = [factory(i) for i in range(3)]

    print([f() for f in late], [f() for f in early], [f() for f in via_factory])
    ```

    ### Пример 4. Проверки с параметрами

    ```python
    def min_len(n):
        return lambda s: len(s) >= n

    def contains(ch):
        return lambda s: ch in s

    rules = {"длина ≥ 8": min_len(8), "есть @": contains("@")}
    for value in ["user@mail.ru", "abc"]:
        failed = [name for name, rule in rules.items() if not rule(value)]
        print(value, "->", failed or "ok")
    ```

    ## Частые ошибки

    **Возврат вызова вместо функции**: `return mul(x)` вместо `return mul`.

    **Позднее связывание** в циклах.

    **Изменение запомненной переменной без `nonlocal`** — `UnboundLocalError`.

    ## Шпаргалка

    ```py
    def factory(param):
        def inner(x):
            return ... param ...
        return inner
    f = factory(3); f(10)
    [lambda i=i: i for i in range(3)]   # зафиксировать значение
    ```
    """,
    quiz=[
        q("Что такое замыкание?", ["Функция без параметров", "Функция, которая помнит переменные из объемлющей области, где была создана", "Функция, закрытая для импорта", "Цикл внутри функции"], 1, "Она сохраняет доступ к этим переменным даже после завершения внешней функции."),
        q("Что вернёт `[f() for f in [lambda: i for i in range(3)]]`?", ["`[0, 1, 2]`", "`[2, 2, 2]`", "`[3, 3, 3]`", "Ошибка"], 1, "Все лямбды читают одну переменную i, равную 2 к моменту вызова."),
        q("Что должна вернуть функция-фабрика?", ["Результат вызова внутренней функции", "Саму внутреннюю функцию", "None", "Список"], 1, "Возвращают объект функции без скобок."),
    ]),
)

# ============================================================
m3 = module(f"{P}-m3", "Подводные камни", "⚠️", "Затенение, изменяемые объекты и области в циклах",

lesson(f"{P}-m3-l1", "Затенение имён", """
    # Shadowing

    Локальное имя **скрывает** одноимённое снаружи:

    ```
    list = [1, 2, 3]       # затенили встроенную list()
    list("abc")            # TypeError: 'list' object is not callable
    ```

    Особенно опасные имена: `list`, `dict`, `str`, `id`, `type`, `input`, `sum`, `max`, `min`, `file`, `filter`.
    Вместо них: `items`, `user_id`, `total`, `max_value`.
    """,
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        def f(sum):
            try:
                return sum([1, 2])
            except TypeError:
                return "sum затенён параметром"

        print(f(10))
        print(sum([1, 2]))
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа?", """
        id = 42
        try:
            print(id(object()) > 0)
        except TypeError:
            print("встроенная id сломана")
        del id
        print(callable(id))
        """),
    cod(f"{P}-m3-l1-e3", t("""
        Функция `stats(list)` падает: параметр назван `list`, и внутри не работает встроенная `list()`. Переименуй параметр в `items`, чтобы функция возвращала `(список_уникальных_элементов_по_порядку_первого_появления, количество)`.

        ```
        stats([3, 1, 3, 2, 1])   # → ([3, 1, 2], 5)
        ```
        """),
        """
        def stats(list):
            unique = list(dict.fromkeys(list))
            return unique, len(list)
        """,
        """
        import inspect

        def test_values():
            assert stats([3, 1, 3, 2, 1]) == ([3, 1, 2], 5), f"Получено {stats([3, 1, 3, 2, 1])}"

        def test_param_name():
            params = list(inspect.signature(stats).parameters)
            assert params == ["items"], f"Параметр должен называться items, сейчас {params}"
        """,
        """
        def stats(items):
            unique = list(dict.fromkeys(items))
            return unique, len(items)
        """),
    cod(f"{P}-m3-l1-e4", t("""
        В заготовке функция `find_max_id(users)` использует переменную `max` для текущего максимума — и из-за этого внутри не работает встроенная `max`. Перепиши её: верни наибольший `id` среди пользователей с помощью **встроенной** `max` и генератора. Не используй имена встроенных функций для переменных.

        ```
        find_max_id([{"id": 3}, {"id": 10}, {"id": 7}])   # → 10
        ```
        """),
        """
        def find_max_id(users):
            max = 0
            for u in users:
                if u["id"] > max:
                    max = u["id"]
            return max
        """,
        """
        def test_value():
            assert find_max_id([{"id": 3}, {"id": 10}, {"id": 7}]) == 10 and find_max_id([{"id": -5}]) == -5, "Неверный максимум"

        def test_uses_builtin():
            src = open("solution.py", encoding="utf-8").read()
            assert "max(" in src and "max =" not in src, "Используй встроенную max, не затеняя её"
        """,
        """
        def find_max_id(users):
            return max(u["id"] for u in users)
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `shadowed_builtins(names)` — из списка имён переменных вернуть те, что **совпадают с именами встроенных функций/типов** Python (в исходном порядке).

        Используй модуль `builtins`: имя встроенное, если `hasattr(builtins, name)`.

        ```
        shadowed_builtins(["items", "list", "user_id", "id", "total", "sum"])
        # → ["list", "id", "sum"]
        ```
        """),
        """
        import builtins

        def shadowed_builtins(names):
            pass
        """,
        """
        def test_values():
            got = shadowed_builtins(["items", "list", "user_id", "id", "total", "sum"])
            assert got == ["list", "id", "sum"], f"Получено {got}"
            assert shadowed_builtins([]) == [], "Пусто — пусто"
        """,
        """
        import builtins

        def shadowed_builtins(names):
            return [n for n in names if hasattr(builtins, n)]
        """),
    full="""
    ## Зачем это нужно

    Назвать переменную `list`, `id` или `sum` очень хочется — это естественные слова. Но в Python это имена встроенных функций, и локальная переменная с таким именем «затеняет» встроенную. Ошибка проявляется позже и в другом месте: `TypeError: 'list' object is not callable` — и непонятно, почему.

    ## Как это работает

    По правилу LEGB поиск имени останавливается на первом найденном. Если в локальной или глобальной области есть `list`, до встроенного `list` (уровень Built-in) Python не дойдёт.

    Затенить можно:
    - переменной: `list = [...]`;
    - параметром функции: `def f(id):`;
    - переменной цикла: `for str in values:`;
    - импортом: `from os import open` (затеняет встроенный `open`).

    ### Как избежать

    - Описательные имена: `items`, `user_id`, `total`, `max_value`, `text`.
    - Если очень нужно слово — суффикс `_`: `id_`, `type_`, `filter_`.
    - Линтеры (ruff, pylint) предупреждают о затенении встроенных имён.

    Вернуть встроенную функцию после затенения в интерактивной сессии: `del list` (или `builtins.list`).

    ## Примеры

    ### Пример 1. Классическая ловушка

    ```python
    list = ["a", "b"]
    try:
        print(list("xyz"))
    except TypeError as e:
        print("TypeError:", e)
    del list
    print(list("xyz"))
    ```

    ### Пример 2. Затенение параметром

    ```python
    def report(id, type):
        # внутри встроенные id() и type() недоступны
        return f"объект {id} типа {type}"

    def report_ok(user_id, kind):
        return f"объект {user_id} типа {kind} ({type(user_id).__name__})"

    print(report(7, "user"))
    print(report_ok(7, "user"))
    ```

    ### Пример 3. Какие имена опасны

    ```python
    import builtins
    candidates = ["items", "list", "data", "id", "input", "total", "max", "filter", "result"]
    print([n for n in candidates if hasattr(builtins, n)])
    ```

    ## Частые ошибки

    **`dict = {}`, `str = "..."`, `input = ...`** — ломают встроенные функции ниже по коду.

    **`for type in types:`** — после цикла `type()` не работает.

    **Затенение в модуле** — ломает встроенную функцию во всём файле.

    ## Шпаргалка

    ```text
    ✗ list, dict, str, id, type, input, sum, max, min, filter, open
    ✓ items, mapping, text, user_id, kind, raw_input, total, max_value
    import builtins; hasattr(builtins, name)   # проверить имя
    ```
    """,
    quiz=[
        q("Почему после `str = \"текст\"` вызов `str(5)` падает?", ["str нельзя вызывать с числом", "Переменная str затенила встроенный тип str", "Строки неизменяемые", "Не падает"], 1, "Имя str теперь указывает на строку, а строку вызвать нельзя."),
        q("Какое имя переменной безопасно?", ["`list`", "`id`", "`user_id`", "`sum`"], 2, "user_id не совпадает со встроенными именами."),
        q("Как проверить, что имя совпадает со встроенным?", ["`name in globals()`", "`hasattr(builtins, name)` после `import builtins`", "`type(name)`", "Никак"], 1, "Встроенные имена — атрибуты модуля builtins."),
    ]),

lesson(f"{P}-m3-l2", "Изменяемые объекты и области", """
    # Изменить объект ≠ присвоить имя

    ```
    items = []

    def add(x):
        items.append(x)      # ОК без global: меняем объект, имя не присваиваем

    def reset():
        items = []           # локальная переменная! глобальная не изменится
    ```

    Функция, получившая список параметром, может изменить его — это видно снаружи.
    """,
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        items = []

        def add(x):
            items.append(x)

        def reset():
            items = []

        add(1)
        add(2)
        reset()
        print(items)
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа?", """
        def modify(lst):
            lst.append(99)
            lst = [0]
            lst.append(1)
            return lst

        data = [1]
        result = modify(data)
        print(data, result)
        """, hint="После `lst = [0]` имя внутри функции указывает на новый список."),
    cod(f"{P}-m3-l2-e3", t("""
        Функция `clear_log()` должна **очищать** глобальный список `LOG`, но сейчас не работает: она создаёт локальную переменную.

        Исправь **без `global`**, изменяя сам объект (например, `LOG.clear()`).

        ```
        LOG.append("x"); clear_log(); LOG   # → []
        ```
        """),
        """
        LOG = []

        def clear_log():
            LOG = []
        """,
        """
        def test_clear():
            LOG.append("x")
            LOG.append("y")
            clear_log()
            assert LOG == [], f"LOG не очищен: {LOG}"

        def test_no_global():
            assert "global" not in open("solution.py", encoding="utf-8").read(), "Реши без global — измени сам объект"
        """,
        """
        LOG = []

        def clear_log():
            LOG.clear()
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Функция `add_default_headers(headers)` должна вернуть **новый** словарь заголовков, дополненный `"Accept": "application/json"`, **не изменяя** переданный словарь. Сейчас она портит аргумент.

        ```
        h = {"Authorization": "Bearer x"}
        add_default_headers(h)   # → {"Authorization": "Bearer x", "Accept": "application/json"}
        h                        # → {"Authorization": "Bearer x"}   без изменений
        ```
        """),
        """
        def add_default_headers(headers):
            headers["Accept"] = "application/json"
            return headers
        """,
        """
        def test_new_dict():
            h = {"Authorization": "Bearer x"}
            result = add_default_headers(h)
            assert result == {"Authorization": "Bearer x", "Accept": "application/json"}, "Неверный результат"
            assert h == {"Authorization": "Bearer x"}, "Исходный словарь изменён"
        """,
        """
        def add_default_headers(headers):
            return {**headers, "Accept": "application/json"}
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `reset_in_place(items, value)` — заменить **всё содержимое** переданного списка одним элементом `value`, так чтобы изменение было видно через **все** ссылки на этот список. Функция ничего не возвращает.

        ```
        a = [1, 2, 3]
        b = a
        reset_in_place(a, 0)
        a, b     # → [0], [0]
        ```
        Используй присваивание срезом `items[:] = ...`.
        """),
        """
        def reset_in_place(items, value):
            items = [value]
        """,
        """
        def test_in_place():
            a = [1, 2, 3]
            b = a
            assert reset_in_place(a, 0) is None, "Функция ничего не возвращает"
            assert a == [0] and b == [0], f"a={a}, b={b}"
        """,
        """
        def reset_in_place(items, value):
            items[:] = [value]
        """),
    full="""
    ## Зачем это нужно

    Самый запутанный момент областей видимости: почему `items.append(x)` внутри функции меняет глобальный список, а `items = []` — нет? Почему функция, получившая словарь заголовков, «испортила» его вызывающему коду? Ответ — в разнице между **изменением объекта** и **присваиванием имени**.

    ## Как это работает

    Переменная — это имя, привязанное к объекту.

    - **Присваивание** `x = ...` перепривязывает имя. Внутри функции (без `global`/`nonlocal`) это всегда **локальное** имя. Внешняя переменная не меняется.
    - **Изменение объекта** — `x.append()`, `x[k] = v`, `x.clear()`, `x[:] = ...` — меняет сам объект, на который указывают **все** ссылки. Никакого `global` для этого не нужно.

    ### Передача аргументов

    В Python аргументы передаются «ссылкой на объект»: параметр — новое имя для того же объекта.
    - Изменишь объект (изменяемый: список, словарь) — изменение видно снаружи.
    - Перепривяжешь параметр — снаружи ничего не изменится.

    Неизменяемые объекты (числа, строки, кортежи) изменить «на месте» нельзя в принципе, поэтому для них функция никак не повлияет на внешнюю переменную.

    ### Хорошая практика

    Либо **не изменяй** аргументы и возвращай новый объект, либо явно документируй, что функция меняет аргумент (как `list.sort()`).

    ## Примеры

    ### Пример 1. Изменение против присваивания

    ```python
    items = [1]

    def mutate():
        items.append(2)        # меняем объект

    def rebind():
        items = ["новый"]       # локальное имя

    mutate(); rebind()
    print(items)
    ```

    ### Пример 2. Функция портит аргумент

    ```python
    def with_accept(headers):
        headers["Accept"] = "application/json"
        return headers

    base = {"Authorization": "Bearer x"}
    h1 = with_accept(base)
    print(base)          # испорчен!

    def with_accept_safe(headers):
        return {**headers, "Accept": "application/json"}

    base = {"Authorization": "Bearer x"}
    h2 = with_accept_safe(base)
    print(base, h2)
    ```

    ### Пример 3. Неизменяемые не меняются

    ```python
    def bump(n, s, t):
        n += 1
        s += "!"
        t += (3,)
        return n, s, t

    n, s, t = 1, "hi", (1, 2)
    print(bump(n, s, t), n, s, t)
    ```

    ### Пример 4. Очистка «для всех»

    ```python
    shared = [1, 2, 3]
    alias = shared

    def clear_all(lst):
        lst[:] = []           # или lst.clear()

    clear_all(shared)
    print(shared, alias)
    ```

    ## Частые ошибки

    **`items = []` внутри функции в надежде очистить глобальный список.**

    **Незаметное изменение аргумента** — баг у вызывающего кода.

    **Ожидание, что функция изменит переданное число или строку.**

    ## Шпаргалка

    ```py
    lst.append(x); d[k] = v; lst.clear(); lst[:] = new   # меняют объект
    lst = []                                             # перепривязка имени
    return {**d, "k": v}                                 # новый объект вместо изменения
    ```
    """,
    quiz=[
        q("Что выведет код?\n```py\nitems = [1]\ndef f():\n    items.append(2)\nf()\nprint(items)\n```", ["`[1]`", "`[1, 2]`", "`UnboundLocalError`", "`[2]`"], 1, "append меняет объект; присваивания имени нет — global не нужен."),
        q("Изменится ли переменная `n = 5` снаружи после вызова `def f(n): n += 1`?", ["Да, станет 6", "Нет, числа неизменяемы, внутри перепривязалось локальное имя", "Будет ошибка", "Станет None"], 1, "Для неизменяемых объектов `+=` создаёт новый объект и перепривязывает локальное имя."),
        q("Как очистить переданный список так, чтобы это увидели все ссылки?", ["`lst = []`", "`lst.clear()` или `lst[:] = []`", "`del lst`", "`lst = None`"], 1, "Нужно изменить сам объект, а не имя."),
    ]),

lesson(f"{P}-m3-l3", "Области в циклах и списочных включениях", """
    # Кто «утекает», а кто нет

    ```
    for i in range(3):
        pass
    print(i)                 # 2 — переменная цикла видна после цикла

    squares = [n * n for n in range(3)]
    print(n)                 # NameError — у списочного включения своя область
    ```

    - Цикл `for` не создаёт области: переменная остаётся после него.
    - Списочные/словарные включения и генераторы — **своя** область.
    """,
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        for i in range(3):
            pass
        print("после for:", i)

        squares = [n * n for n in range(3)]
        try:
            print(n)
        except NameError:
            print("n из включения не видна")
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа?", """
        x = "снаружи"
        result = [x for x in ["a", "b"]]
        print(result, x)

        for x in ["c", "d"]:
            pass
        print(x)
        """, hint="Включение не трогает внешнюю x, а обычный цикл — перезаписывает."),
    cod(f"{P}-m3-l3-e3", t("""
        В функции `process(items)` баг: переменная цикла `item` используется **после** цикла, и для пустого списка функция падает с `UnboundLocalError`.

        Исправь: функция должна возвращать последний элемент списка, а для пустого — `None`.

        ```
        process([1, 2, 3])   # → 3
        process([])          # → None
        ```
        """),
        """
        def process(items):
            for item in items:
                pass
            return item
        """,
        """
        def test_values():
            assert process([1, 2, 3]) == 3 and process(["a"]) == "a", "Нужен последний элемент"
            assert process([]) is None, "Пустой список — None"
        """,
        """
        def process(items):
            last = None
            for item in items:
                last = item
            return last
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `name_after_loop(names)`, которая доказывает разницу областей: верни пару

        1. результат списочного включения `[n.upper() for n in names]`;
        2. значение внешней переменной `n`, которой **до** включения присвоено `"внешняя"` — она не должна измениться.

        ```
        name_after_loop(["a", "b"])   # → (["A", "B"], "внешняя")
        ```
        """),
        """
        def name_after_loop(names):
            n = "внешняя"
            pass
        """,
        """
        def test_values():
            assert name_after_loop(["a", "b"]) == (["A", "B"], "внешняя"), f"Получено {name_after_loop(['a', 'b'])}"
        """,
        """
        def name_after_loop(names):
            n = "внешняя"
            upper = [n.upper() for n in names]
            return upper, n
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `make_multipliers(n)` — список из `n` функций, где функция с индексом `i` умножает аргумент на `i`. Реши **списочным включением** с лямбдой и позаботься о позднем связывании.

        ```
        ms = make_multipliers(4)
        [m(10) for m in ms]   # → [0, 10, 20, 30]
        ```
        """),
        """
        def make_multipliers(n):
            return [lambda x: x * i for i in range(n)]
        """,
        """
        def test_values():
            ms = make_multipliers(4)
            assert [m(10) for m in ms] == [0, 10, 20, 30], f"Получено {[m(10) for m in ms]}"
        """,
        """
        def make_multipliers(n):
            return [lambda x, i=i: x * i for i in range(n)]
        """),
    full="""
    ## Зачем это нужно

    Циклы и списочные включения выглядят похоже, но по-разному обращаются с переменными. Это объясняет классические баги: `UnboundLocalError` после пустого цикла, «переменная неожиданно перезаписалась», все лямбды из включения возвращают одно и то же.

    ## Как это работает

    ### Цикл for

    Не создаёт новой области. Переменная цикла — обычная переменная функции (или модуля):
    - после цикла хранит последнее значение;
    - перезаписывает одноимённую переменную, созданную до цикла;
    - если коллекция пустая, переменная **не создаётся** — обращение к ней после цикла даст `NameError`/`UnboundLocalError`.

    ### Включения и генераторы

    `[... for x in ...]`, `{... for ...}`, `(... for ...)` имеют **собственную** область:
    - переменная `x` не видна снаружи;
    - одноимённая внешняя переменная не перезаписывается.

    Но внутри включения видны внешние переменные (LEGB работает как обычно).

    ### Лямбды во включениях

    Каждая лямбда — замыкание на переменную цикла включения; позднее связывание действует и здесь. Лечение — `lambda x, i=i: ...`.

    ## Примеры

    ### Пример 1. Утечка переменной цикла

    ```python
    total = "моё значение"
    for total in [1, 2, 3]:
        pass
    print(total)              # перезаписано циклом
    ```

    ### Пример 2. Пустой цикл

    ```python
    def last_item(items):
        for item in items:
            pass
        return item

    print(last_item([1, 2]))
    try:
        last_item([])
    except UnboundLocalError as e:
        print("UnboundLocalError:", e)
    ```

    ### Пример 3. Включения изолированы

    ```python
    x = "снаружи"
    squares = [x * 2 for x in [1, 2, 3]]
    print(squares, x)
    factor = 10
    print([n * factor for n in range(3)])     # внешние имена видны
    ```

    ### Пример 4. Лямбды во включении

    ```python
    late = [lambda: i for i in range(3)]
    fixed = [lambda i=i: i for i in range(3)]
    print([f() for f in late], [f() for f in fixed])
    ```

    ## Частые ошибки

    **Использование переменной цикла после пустого цикла.**

    **Одинаковое имя для переменной цикла и важной переменной выше.**

    **Позднее связывание в лямбдах внутри включений.**

    ## Шпаргалка

    ```text
    for x in xs: ...        → x видна после цикла (если xs не пуст)
    [f(x) for x in xs]      → x не видна снаружи
    [lambda i=i: i for i in range(n)]   → зафиксировать значение
    ```
    """,
    quiz=[
        q("Будет ли видна переменная `n` после `squares = [n * n for n in range(3)]`?", ["Да, равна 2", "Нет, у включения своя область", "Да, равна 3", "Зависит от версии"], 1, "Включения изолируют свои переменные."),
        q("Что произойдёт при `for x in []: pass` и затем `print(x)` (если x раньше не было)?", ["Выведет None", "`NameError`", "Выведет []", "Выведет 0"], 1, "Цикл не выполнился ни разу, переменная не создана."),
        q("Перезапишет ли `for x in ...` переменную `x`, созданную до цикла?", ["Нет", "Да, цикл не создаёт отдельной области", "Только если x — число", "Только в функциях"], 1, "Переменная цикла — обычная переменная той же области."),
    ]),
)

TOPIC = topic("py-scope", "Область видимости переменных", "🔭", "#ff4b4b",
              "Локальные и глобальные переменные, LEGB, global, nonlocal и замыкания",
              m1, m2, m3, group="Python")
