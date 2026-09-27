"""Тема «Условные операторы»."""
from ._lib import cod, lesson, module, out, q, t, topic

P = "cnd"

# ============================================================
m1 = module(f"{P}-m1", "if и сравнения", "⚖️", "if/else, операторы сравнения и elif",

lesson(f"{P}-m1-l1", "if и else", """
    # Условие if

    ```
    if age >= 18:
        print("Можно")
    else:
        print("Нельзя")
    ```

    - После условия — **двоеточие**.
    - Тело — с **отступом** 4 пробела. Отступ — часть синтаксиса.
    - `else` необязателен.
    - Код без отступа после блока выполняется всегда.
    """,
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
        """),
    full="""
    ## Зачем это нужно

    Программа, которая всегда делает одно и то же, мало полезна. Условия позволяют **реагировать на данные**: пустить на сайт только взрослых, показать ошибку при неверном пароле, пометить тест как упавший.

    ## Как это работает

    ```py
    if условие:
        код, если условие истинно
    else:
        код, если ложно
    ```

    1. Python вычисляет условие. Результат приводится к `True`/`False`.
    2. Выполняется ровно одна ветка.
    3. Затем программа продолжается после всего блока.

    **Отступ** — не украшение: по нему Python понимает, какие строки относятся к ветке. Стандарт — 4 пробела (в редакторе CodeQuest это делает Tab).

    ### Условие — любое выражение

    Необязательно сравнение: `if items:` (список не пуст), `if name:` (строка не пустая), `if user is None:`.

    ### Ранний return вместо else

    В функции после `return` код ветки завершается, поэтому `else` часто не нужен:

    ```py
    def max2(a, b):
        if a > b:
            return a
        return b
    ```

    ## Примеры

    ### Пример 1. Базовый if/else

    ```python
    for temperature in [25, 12]:
        if temperature > 20:
            print(temperature, "— жарко")
        else:
            print(temperature, "— прохладно")
    ```

    ### Пример 2. Отступ решает всё

    ```python
    x = 3
    if x > 5:
        print("A — внутри if")
        print("B — тоже внутри")
    print("C — выполняется всегда")
    ```

    ### Пример 3. Функция с проверкой

    ```python
    def check_status(code):
        if code == 200:
            return "OK"
        return f"FAIL: {code}"

    for code in [200, 404, 500]:
        print(code, check_status(code))
    ```

    ### Пример 4. Вернуть результат сравнения

    ```python
    def is_adult(age):
        return age >= 18          # сравнение уже даёт True/False

    print([is_adult(a) for a in [30, 18, 17]])
    ```

    ## Частые ошибки

    **Забытое двоеточие** — `SyntaxError`.

    **Смешанные табы и пробелы** — `IndentationError`.

    **`if x = 5:`** — присваивание вместо сравнения, синтаксическая ошибка.

    **Лишний if ради True/False**: `if a > b: return True else: return False` — просто `return a > b`.

    ## Шпаргалка

    ```py
    if cond:
        ...
    else:
        ...
    return a >= b     # сравнение само по себе bool
    ```
    """,
    quiz=[
        q("Что выведет код?\n```py\nx = 10\nif x > 5:\n    print(\"A\")\nprint(\"B\")\n```", ["`A`", "`B`", "`A` и `B`", "Ничего"], 2,
          "Условие истинно — печатается `A`; строка без отступа выполняется всегда — `B`."),
        q("Какой вариант функции `is_even(n)` самый лаконичный и верный?",
          ["`if n % 2 == 0: return True`", "`return n % 2 == 0`", "`return n / 2`", "`if n % 2: return True else: return False`"], 1,
          "Сравнение само даёт `True`/`False`, дополнительный `if` не нужен."),
        q("Что обязательно после условия в `if`?", ["Точка с запятой", "Двоеточие", "Скобки", "Слово then"], 1, "Строка `if` заканчивается двоеточием, дальше — блок с отступом."),
    ]),

lesson(f"{P}-m1-l2", "Операторы сравнения", """
    # Сравнения

    `==` равно · `!=` не равно · `<` `>` `<=` `>=`

    - Результат — `True` или `False`.
    - Цепочки: `0 < x < 10` — то же, что `0 < x and x < 10`.
    - Строки сравниваются по алфавиту посимвольно, заглавные «меньше» строчных.
    - `==` сравнивает **значения**, `is` — что это **один и тот же объект** (для `None`).
    """,
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
        """, xp=20),
    full="""
    ## Зачем это нужно

    Любая проверка в программе и в тесте — это сравнение: статус равен 200? время ответа меньше секунды? версия не ниже требуемой? Важно знать тонкости: как сравниваются строки, чем `==` отличается от `is` и почему `"10" < "9"`.

    ## Как это работает

    Операторы: `==`, `!=`, `<`, `>`, `<=`, `>=`. Результат — `bool`.

    ### Цепочки

    `a < b < c` — это `a < b and b < c`, причём `b` вычисляется один раз. Удобно для диапазонов: `1 <= port <= 65535`.

    ### Числа разных типов

    `5 == 5.0` — `True`: сравниваются значения. А вот число и строка никогда не равны: `10 == "10"` — `False` (и `<` между ними — `TypeError`).

    ### Строки

    Сравниваются **посимвольно по кодам символов** (лексикографически):
    - `"apple" < "banana"` — по первой букве;
    - `"Z" < "a"` — заглавные латинские имеют меньшие коды;
    - `"10" < "9"` — потому что `"1" < "9"`.

    Поэтому числа, версии и даты в виде строк сравнивать напрямую нельзя.

    ### == и is

    - `==` — равны ли **значения**;
    - `is` — один ли это **объект** в памяти.

    `is` используют только для `None`, `True`, `False`.

    ## Примеры

    ### Пример 1. Базовые сравнения

    ```python
    print(5 == 5.0, 5 != 5, 3 <= 3)
    print(1 <= 8080 <= 65535)
    print("abc" == "ABC", "abc" == "ABC".lower())
    ```

    ### Пример 2. Строки против чисел

    ```python
    versions = ["1.10", "1.9", "1.2"]
    print(sorted(versions))
    print(sorted(versions, key=lambda v: tuple(int(p) for p in v.split("."))))
    ```

    ### Пример 3. Кортежи сравниваются поэлементно

    ```python
    print((1, 9) < (1, 10))
    print((2, 0) > (1, 99))
    print((1, 2, 3) == (1, 2, 3))
    ```

    ### Пример 4. == и is

    ```python
    a = [1, 2]
    b = [1, 2]
    print(a == b, a is b)
    x = None
    print(x is None)
    ```

    ## Частые ошибки

    **Сравнение строковых чисел** — `"10" < "9"` даёт `True`.

    **`is` для чисел и строк** — может «случайно» работать для маленьких значений и сломаться для больших. Для значений — только `==`.

    **Сравнение float через `==`** — используй `round` или `math.isclose`.

    ## Шпаргалка

    ```py
    ==  !=  <  >  <=  >=
    low <= x <= high               # диапазон
    tuple(map(int, v.split(".")))  # версия для сравнения
    x is None                      # только для None/True/False
    ```
    """,
    quiz=[
        q("Что вернёт `\"10\" < \"9\"`?", ["`False`", "`True`", "Ошибка", "`None`"], 1,
          "Строки сравниваются посимвольно: `\"1\"` меньше `\"9\"`, поэтому `\"10\" < \"9\"` истинно."),
        q("Что вернёт `1 < 5 > 3`?", ["`True`", "`False`", "Ошибка", "`3`"], 0, "Это `1 < 5 and 5 > 3` — оба истинны."),
        q("Когда уместно использовать `is`?", ["Для сравнения чисел", "Для сравнения строк", "Для проверки на `None`", "Всегда вместо `==`"], 2,
          "`is` проверяет идентичность объектов; для значений используют `==`."),
    ]),

lesson(f"{P}-m1-l3", "elif — много вариантов", """
    # elif

    ```
    if score >= 90:
        grade = "A"
    elif score >= 75:
        grade = "B"
    else:
        grade = "C"
    ```

    - Условия проверяются **сверху вниз**.
    - Выполняется **только первая** подходящая ветка.
    - Поэтому более строгие условия ставят **выше**.
    """,
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
        hint="Проверку «на 3 и 5 одновременно» (`n % 15 == 0`) ставь первой.", xp=20),
    full="""
    ## Зачем это нужно

    Вариантов часто больше двух: оценка A/B/C/F, класс HTTP-ответа, уровень серьёзности бага. Вложенные `if/else` превращаются в «лестницу», а `elif` делает выбор плоским и читаемым.

    ## Как это работает

    ```py
    if условие1:
        ...
    elif условие2:
        ...
    else:
        ...
    ```

    - Условия проверяются по порядку.
    - Выполняется **первая** истинная ветка, остальные пропускаются — даже если их условия тоже истинны.
    - `else` — если не подошло ничего.

    Следствие: в каждой следующей ветке ты уже **знаешь**, что предыдущие условия ложны. Поэтому не нужно писать `elif 75 <= score < 90` — достаточно `elif score >= 75`.

    ### elif против нескольких if

    Отдельные `if` проверяются все, и может выполниться несколько веток. `elif` — взаимоисключающий выбор.

    ## Примеры

    ### Пример 1. Шкала

    ```python
    def grade(score):
        if score >= 90:
            return "A"
        elif score >= 75:
            return "B"
        elif score >= 60:
            return "C"
        return "F"

    print([grade(s) for s in [95, 90, 80, 60, 10]])
    ```

    ### Пример 2. elif против двух if

    ```python
    n = 15
    if n > 10:
        print("elif-версия: больше 10")
    elif n > 5:
        print("elif-версия: больше 5")

    if n > 10:
        print("if-версия: больше 10")
    if n > 5:
        print("if-версия: больше 5")
    ```

    ### Пример 3. Порядок решает — FizzBuzz

    ```python
    def wrong(n):
        if n % 3 == 0:
            return "Fizz"
        elif n % 15 == 0:
            return "FizzBuzz"     # сюда 15 уже не дойдёт
        return str(n)

    def right(n):
        if n % 15 == 0:
            return "FizzBuzz"
        elif n % 3 == 0:
            return "Fizz"
        return str(n)

    print(wrong(15), right(15))
    ```

    ### Пример 4. Классификация статуса

    ```python
    def status_class(code):
        if code < 300:
            return "success"
        elif code < 400:
            return "redirect"
        elif code < 500:
            return "client error"
        return "server error"

    for c in [200, 302, 404, 503]:
        print(c, status_class(c))
    ```

    ## Частые ошибки

    **Широкое условие выше узкого** — узкое никогда не сработает.

    **Лишние проверки в elif** — усложняют код и провоцируют ошибки на границах.

    **Нет `else`** — функция молча вернёт `None` для неучтённых значений.

    ## Шпаргалка

    ```py
    if a:       # самое строгое
        ...
    elif b:     # только если a ложно
        ...
    else:       # всё остальное
        ...
    ```
    """,
    quiz=[
        q("Что вернёт функция при `n = 20`?\n```py\nif n > 5:\n    return \"A\"\nelif n > 10:\n    return \"B\"\nreturn \"C\"\n```", ["`\"A\"`", "`\"B\"`", "`\"C\"`", "Оба"], 0,
          "Первое же истинное условие `n > 5` срабатывает, дальше не проверяется."),
        q("Сколько веток может выполниться в цепочке `if/elif/elif/else`?", ["Сколько угодно", "Ровно одна", "Не больше двух", "Ни одной"], 1,
          "Ровно одна: первая истинная или `else`."),
        q("В `grade`: `if s >= 90: ... elif s >= 75:` — нужно ли во второй ветке проверять `s < 90`?", ["Да, обязательно", "Нет, это уже известно — первая ветка не сработала", "Только для s = 90", "Да, иначе SyntaxError"], 1,
          "Раз мы дошли до `elif`, условие `s >= 90` ложно."),
    ]),
)

# ============================================================
m2 = module(f"{P}-m2", "Логика", "🧠", "and, or, not, истинность и вложенные условия",

lesson(f"{P}-m2-l1", "and, or, not", """
    # Логические операторы

    - `a and b` — истина, если **оба** истинны
    - `a or b` — истина, если **хотя бы один**
    - `not a` — отрицание

    Приоритет: `not` → `and` → `or`. Сомневаешься — ставь скобки.

    **Короткое замыкание**: в `a and b` при ложном `a` часть `b` не вычисляется.
    """,
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
        hint="Скобки вокруг `or`-части обязательны: `and` выполняется раньше `or`.", xp=20),
    full="""
    ## Зачем это нужно

    Реальные условия составные: «вход разрешён, если логин есть **и** пароль верный», «повторить запрос, если ошибка сервера **или** лимит запросов, **и** попытки ещё остались». Логические операторы соединяют простые условия в сложные.

    ## Как это работает

    - `a and b` — `True`, только если оба истинны.
    - `a or b` — `True`, если хотя бы один истинен.
    - `not a` — переворачивает.

    Приоритет: сначала `not`, потом `and`, потом `or`. То есть `a or b and c` — это `a or (b and c)`.

    ### Короткое замыкание

    Python вычисляет ровно столько, сколько нужно:
    - `a and b`: если `a` ложно — ответ ясен, `b` не вычисляется;
    - `a or b`: если `a` истинно — `b` не вычисляется.

    Это защищает от ошибок: `if items and items[0] > 0:` не упадёт на пустом списке.

    ### and/or возвращают операнд

    На самом деле `and`/`or` возвращают **один из операндов**, а не обязательно `True`/`False`: `"" or "гость"` → `"гость"`. Подробнее — в уроке про значения по умолчанию.

    ## Примеры

    ### Пример 1. Таблица истинности

    ```python
    for a in [True, False]:
        for b in [True, False]:
            print(f"{a!s:5} {b!s:5} | and={a and b!s:5} or={a or b}")
    ```

    ### Пример 2. Приоритет

    ```python
    print(True or False and False)       # or (False and False)
    print((True or False) and False)
    ```

    ### Пример 3. Короткое замыкание защищает

    ```python
    for items in [[], [5], [-1]]:
        if items and items[0] > 0:
            print(items, "— первый положительный")
        else:
            print(items, "— пусто или не положительный")
    ```

    ### Пример 4. Условие повтора запроса

    ```python
    def need_retry(status, attempt, max_attempts):
        return (500 <= status <= 599 or status == 429) and attempt < max_attempts

    for args in [(503, 1, 3), (503, 3, 3), (404, 1, 3), (429, 2, 3)]:
        print(args, need_retry(*args))
    ```

    ## Частые ошибки

    **`day == "сб" or "вс"`** — всегда истинно: это `(day == "сб") or "вс"`, а непустая строка — истина. Правильно: `day in ("сб", "вс")`.

    **Забытые скобки** при смешивании `and` и `or`.

    **`if flag == True:`** — достаточно `if flag:`.

    ## Шпаргалка

    ```py
    a and b     a or b     not a
    (x or y) and z          # скобки при смешивании
    items and items[0]      # безопасный доступ
    ```
    """,
    quiz=[
        q("Чему равно `True or False and False`?", ["`True`", "`False`", "Ошибка", "`None`"], 0,
          "`and` выполняется первым: `False and False` → `False`; затем `True or False` → `True`."),
        q("Чему равно `day == \"сб\" or \"вс\"` при `day = \"пн\"`?", ["`False`", "`True`", "`\"вс\"`", "Ошибка"], 2,
          "Первая часть ложна, поэтому `or` возвращает вторую — строку `\"вс\"`, а она истинна. Классический баг."),
        q("Почему `items and items[0] > 0` не падает на пустом списке?", ["Python игнорирует ошибки в условиях", "Пустой список ложен, и правая часть не вычисляется", "`items[0]` пустого списка — 0", "Падает"], 1,
          "Короткое замыкание: при ложной левой части `and` правую не вычисляет."),
    ]),

lesson(f"{P}-m2-l2", "Истинность и оператор in", """
    # Истинность

    Ложью считаются: `False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `()`.
    Всё остальное — истина (даже `"0"` и `[0]`).

    ```
    if items:        # список не пуст
    if not name:     # строка пустая
    ```

    # Оператор in

    `x in коллекция` — есть ли элемент: `day in ("сб", "вс")`, `"err" in line`, `key in dict`.
    """,
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
        """),
    full="""
    ## Зачем это нужно

    Проверки «пусто ли?» и «есть ли среди вариантов?» встречаются в каждом втором условии. Python позволяет писать их коротко и читаемо — если знать, что считается ложью и как работает `in`.

    ## Как это работает

    ### Истинность (truthiness)

    В условии любое значение приводится к `bool`. **Ложь**:
    - `False`, `None`;
    - ноль любого числового типа: `0`, `0.0`;
    - пустые коллекции: `""`, `[]`, `()`, `{}`, `set()`, `range(0)`.

    Всё остальное — **истина**. Внимание: `"0"`, `" "`, `[0]`, `[[]]` — истинны, это непустые значения.

    Питоничный стиль:
    - `if items:` вместо `if len(items) > 0:`
    - `if not name:` вместо `if name == "":`

    ### Оператор in

    - для строк — есть ли **подстрока**;
    - для списков, кортежей, множеств — есть ли **элемент**;
    - для словарей — есть ли **ключ**.

    `not in` — отрицание: `if x not in banned:`.

    Для частых проверок по большому набору используй `set` — поиск в множестве мгновенный, а в списке — перебором.

    ## Примеры

    ### Пример 1. Что ложно, что истинно

    ```python
    for v in [0, 0.0, "", " ", "0", [], [0], {}, None, False]:
        print(f"{v!r:6} -> {bool(v)}")
    ```

    ### Пример 2. Проверка пустоты

    ```python
    def report(failed):
        if not failed:
            return "всё зелёное"
        return "упали: " + ", ".join(failed)

    print(report([]))
    print(report(["test_login", "test_pay"]))
    ```

    ### Пример 3. in для разных коллекций

    ```python
    print("time" in "timeout")
    print(404 in [200, 404, 500])
    print("admin" in {"admin", "qa"})
    print("id" in {"id": 1, "name": "Аня"})
    print("Аня" in {"id": 1, "name": "Аня"})     # значения не проверяются!
    ```

    ### Пример 4. in вместо цепочки or

    ```python
    def is_error(level):
        return level.upper() in ("ERROR", "CRITICAL", "FATAL")

    print([is_error(l) for l in ["info", "error", "Fatal"]])
    ```

    ## Частые ошибки

    **`if value:` для чисел, где 0 — допустимое значение** — ноль воспримется как «нет значения». Проверяй `if value is not None:`.

    **`in` по словарю ищет значения** — нет, только ключи. Для значений — `x in d.values()`.

    **`"0"` считается ложью** — нет, это непустая строка.

    ## Шпаргалка

    ```py
    if items:            # непустой
    if not text:         # пустой
    x in (1, 2, 3)       # один из вариантов
    key in d             # ключ в словаре
    x not in banned
    ```
    """,
    quiz=[
        q("Какое значение **истинно**?", ["`0`", "`\"\"`", "`[0]`", "`None`"], 2, "`[0]` — непустой список, значит истина, хотя внутри ноль."),
        q("Что проверяет `\"Аня\" in {\"name\": \"Аня\"}`?", ["Есть ли такое значение", "Есть ли такой ключ", "Есть ли подстрока", "Ошибка"], 1,
          "Для словаря `in` проверяет только ключи — результат `False`."),
        q("Как по-питоничному проверить, что список `items` пустой?", ["`if items == []:`", "`if len(items) == 0:`", "`if not items:`", "`if items is None:`"], 2,
          "Пустой список ложен, поэтому `not items` — истина."),
    ]),

lesson(f"{P}-m2-l3", "Вложенные условия и ранний выход", """
    # Вложенные условия

    ```
    if user:
        if user.active:
            if user.is_admin:
                ...
    ```

    Глубокая вложенность («лесенка») читается плохо. Лучше **ранний выход** (guard clauses):

    ```
    if not user:
        return "нет пользователя"
    if not user.active:
        return "заблокирован"
    return "ok"
    ```
    """,
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
        """),
    full="""
    ## Зачем это нужно

    Бизнес-правила часто многоступенчатые: цена зависит от возраста, а для взрослых — ещё и от статуса студента; доступ зависит от активности аккаунта и роли. Если просто вкладывать `if` в `if`, код уезжает вправо и становится нечитаемым. Навык — выстроить проверки так, чтобы логика была очевидна.

    ## Как это работает

    ### Вложенность

    `if` внутри `if` — нормально, когда второе условие имеет смысл только при выполненном первом. Но уже на третьем уровне стоит остановиться.

    ### Ранний выход (guard clauses)

    Идея: сначала отсечь все «плохие» и особые случаи, сразу вернув результат, а основную логику оставить без отступов.

    ```py
    def process(order):
        if order is None:
            return "нет заказа"
        if not order["items"]:
            return "пустой заказ"
        if order["total"] <= 0:
            return "некорректная сумма"
        # здесь всё проверено — основная логика
        return "ok"
    ```

    Плюсы: каждое правило — одна строка, порядок проверок очевиден, нет `else`.

    ### Объединение условий

    Иногда вложенность заменяется одним условием с `and`: `if age >= 18 and has_ticket:`.

    ## Примеры

    ### Пример 1. Лесенка

    ```python
    def access_nested(user):
        if user is not None:
            if user["active"]:
                if user["role"] == "admin":
                    return "полный доступ"
                else:
                    return "обычный доступ"
            else:
                return "заблокирован"
        else:
            return "нет пользователя"

    print(access_nested({"active": True, "role": "admin"}))
    ```

    ### Пример 2. То же с ранним выходом

    ```python
    def access(user):
        if user is None:
            return "нет пользователя"
        if not user["active"]:
            return "заблокирован"
        if user["role"] == "admin":
            return "полный доступ"
        return "обычный доступ"

    for u in [None, {"active": False, "role": "admin"}, {"active": True, "role": "admin"}, {"active": True, "role": "qa"}]:
        print(access(u))
    ```

    ### Пример 3. Валидация с первой ошибкой

    ```python
    def validate(password):
        if len(password) < 8:
            return "короткий"
        if not any(ch.isdigit() for ch in password):
            return "нет цифр"
        if password == password.lower():
            return "нет заглавных"
        return "ok"

    for p in ["abc", "abcdefgh", "abcdefg1", "Abcdefg1"]:
        print(f"{p:10} -> {validate(p)}")
    ```

    ## Частые ошибки

    **Больше трёх уровней вложенности** — сигнал переписать через ранний выход или вынести часть в функцию.

    **Разные ветки делают одно и то же** — объедини условие.

    **Потерянная ветка** в глубокой вложенности — функция возвращает `None`.

    ## Шпаргалка

    ```py
    def f(x):
        if плохо_1:
            return ...
        if плохо_2:
            return ...
        return основной_результат
    ```
    """,
    quiz=[
        q("В чём главная идея «раннего выхода» (guard clause)?", ["Вызывать `exit()`", "Сразу возвращать результат для особых случаев, а основную логику писать без вложенности", "Проверять условия в конце функции", "Использовать только else"], 1,
          "Отсекаем плохие случаи вверху функции — дальше код без лишних отступов."),
        q("Что вернёт `access(None)` из примера 2?", ["`\"заблокирован\"`", "`\"нет пользователя\"`", "Ошибка", "`None`"], 1, "Первая же проверка `user is None` срабатывает."),
        q("Когда вложенный `if` уместен?", ["Никогда", "Когда внутреннее условие имеет смысл только при выполненном внешнем", "Всегда вместо and", "Только в циклах"], 1,
          "Вложенность нормальна, если отражает реальную зависимость условий; проблема — глубокая «лесенка»."),
    ]),
)

# ============================================================
m3 = module(f"{P}-m3", "Короткие условия", "⚡", "Тернарный оператор, значения по умолчанию и match",

lesson(f"{P}-m3-l1", "Тернарный оператор", """
    # Условие в одну строку

    ```
    status = "взрослый" if age >= 18 else "ребёнок"
    ```

    Читается: «значение-да, **если** условие, **иначе** значение-нет».

    - Это **выражение** — его можно присвоить, вернуть, вставить в f-строку.
    - `else` обязателен.
    - Вычисляется только выбранная ветка.
    - Вложенный: `A if c1 else B if c2 else C` — не больше одного уровня.
    """,
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
        """),
    full="""
    ## Зачем это нужно

    Часто `if/else` нужен только для того, чтобы **выбрать одно из двух значений**. Четыре строки ради одной мысли — многовато. Тернарный оператор записывает такой выбор в одну строку и, главное, делает его **выражением**, которое можно подставить куда угодно: в `return`, в f-строку, в аргумент функции, в генератор списка.

    ## Как это работает

    ```py
    значение_да if условие else значение_нет
    ```

    1. Вычисляется условие.
    2. Истинно — вычисляется и возвращается левая часть, ложно — правая.
    3. Невыбранная ветка **не выполняется** вовсе.

    ### Вложенный тернарник

    `A if c1 else B if c2 else C` читается слева направо: «A, если c1; иначе B, если c2; иначе C». Три варианта — предел читаемости.

    ### Где особенно удобно

    - `return "OK" if passed else "FAIL"`
    - `f"{n} {'файл' if n == 1 else 'файлов'}"`
    - `["pass" if ok else "fail" for ok in results]`

    ## Примеры

    ### Пример 1. Присвоение и return

    ```python
    def label(code):
        return "OK" if code < 400 else "ERROR"

    for code in [200, 301, 404, 500]:
        print(code, label(code))
    ```

    ### Пример 2. Вычисляется только одна ветка

    ```python
    items = []
    first = items[0] if items else "список пуст"    # items[0] не вычисляется
    print(first)
    ```

    ### Пример 3. В f-строке и генераторе

    ```python
    results = {"login": True, "pay": False}
    for name, ok in results.items():
        print(f"{name}: {'✅' if ok else '❌'}")
    print(["pass" if ok else "fail" for ok in results.values()])
    ```

    ### Пример 4. Скобки в выражениях

    ```python
    price, is_member = 1000, True
    total = price * (0.9 if is_member else 1.0)
    print(total)
    wrong = price * 0.9 if is_member else 1.0      # то же? нет! без скобок смысл другой
    print(wrong, "(для не-участника было бы 1.0, а не 1000)")
    ```

    ## Частые ошибки

    **Нет `else`** — синтаксическая ошибка.

    **Действия вместо значений** — `print("да") if x else print("нет")` работает, но это плохой стиль; для действий — обычный `if`.

    **Глубокая вложенность** — для трёх и более вариантов пиши `if/elif/else`.

    ## Шпаргалка

    ```py
    x = a if cond else b
    return a if cond else b
    f"{'да' if ok else 'нет'}"
    [a if cond(x) else b for x in xs]
    ```
    """,
    quiz=[
        q("Что выведет `print(\"да\" if 0 else \"нет\")`?", ["`да`", "`нет`", "`0`", "Ошибка"], 1, "Ноль — ложь, выбирается ветка после `else`."),
        q("Какая запись правильная?", ["`x = a > b ? a : b`", "`x = a if a > b else b`", "`x = if a > b a else b`", "`x = a if a > b`"], 1,
          "Порядок: значение-да, `if`, условие, `else`, значение-нет."),
        q("Что будет при `first = items[0] if items else None` для пустого `items`?", ["IndexError", "`first` = `None`", "`first` = `[]`", "SyntaxError"], 1,
          "Пустой список ложен, выполняется только ветка `else`."),
    ]),

lesson(f"{P}-m3-l2", "Значения по умолчанию: or и is None", """
    # Значение по умолчанию

    `a or b` возвращает `a`, если оно истинно, иначе `b`:

    ```
    name = user_name or "Гость"
    ```

    ⚠️ `or` заменит **любое** ложное значение: и `""`, и `0`, и `[]`.
    Если `0` допустим — проверяй именно `None`:

    ```
    timeout = 30 if value is None else value
    ```
    """,
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
        """, xp=20),
    full="""
    ## Зачем это нужно

    Подставить значение по умолчанию — одна из самых частых задач: имя «Гость», таймаут 30 секунд, браузер Chrome, если в настройках пусто. Это делают через `or` или через проверку на `None`. Путаница между ними — источник реальных багов: «ретраи отключили, а они всё равно работают».

    ## Как это работает

    ### or возвращает операнд

    `a or b`:
    - если `a` истинно — возвращается `a` (и `b` даже не вычисляется);
    - иначе — возвращается `b`.

    Цепочка `a or b or c` вернёт первое истинное значение (или последнее, если все ложны).

    Аналогично `a and b` возвращает `a`, если оно ложно, иначе `b`.

    ### Когда or опасен

    `or` считает «пустыми» **все** ложные значения: `0`, `0.0`, `False`, `""`, `[]`. Если хоть одно из них — допустимое значение, `or` его «съест».

    ### Проверка на None

    ```py
    value = default if value is None else value
    ```

    Заменяется только отсутствие значения. `0` и `False` сохраняются.

    Для словарей — `d.get(key, default)`, но осторожно: если ключ **есть** со значением `None`, `get` вернёт `None`, а не default.

    ## Примеры

    ### Пример 1. or с разными значениями

    ```python
    for v in ["Аня", "", None, 0, 5, [], ["x"]]:
        print(f"{v!r:8} or 'default' -> {v or 'default'!r}")
    ```

    ### Пример 2. Баг с ретраями

    ```python
    def retries_bad(value):
        return value or 3

    def retries_good(value):
        return 3 if value is None else value

    for v in [None, 5, 0]:
        print(f"{v!r:5} bad={retries_bad(v)} good={retries_good(v)}")
    ```

    ### Пример 3. Настройки с разными источниками

    ```python
    cli_arg = None
    env_value = ""
    file_value = "firefox"
    browser = cli_arg or env_value or file_value or "chrome"
    print(browser)
    ```

    ### Пример 4. get с default против None в значении

    ```python
    cfg = {"browser": None}
    print(cfg.get("browser", "chrome"))       # ключ есть — вернётся None!
    print(cfg.get("browser") or "chrome")
    value = cfg.get("browser")
    print("chrome" if value is None else value)
    ```

    ## Частые ошибки

    **`count or 1`, `enabled or True`** — ломаются на `0`/`False`.

    **`d.get(k, default)` при `None` в значении** — вернёт `None`.

    **`== None` вместо `is None`.**

    ## Шпаргалка

    ```py
    name = x or "Гость"                     # любое пустое → по умолчанию
    t = 30 if x is None else x              # только None → по умолчанию
    first = a or b or c or "fallback"       # первое непустое
    ```
    """,
    quiz=[
        q("Что вернёт `0 or \"\" or []`?", ["`0`", "`\"\"`", "`[]`", "`False`"], 2, "Все три ложны, поэтому `or` вернёт последний операнд — `[]`."),
        q("`retries = value or 3`. Пользователь передал `0` (без повторов). Что получится?", ["`0`", "`3`", "`None`", "Ошибка"], 1,
          "Ноль — ложь, `or` подставит 3. Правильно — `3 if value is None else value`."),
        q("Что вернёт `{\"a\": None}.get(\"a\", 5)`?", ["`5`", "`None`", "`KeyError`", "`\"a\"`"], 1, "Ключ существует, его значение — `None`; default используется только при отсутствии ключа."),
    ]),

lesson(f"{P}-m3-l3", "match / case", """
    # Сопоставление с образцом (Python 3.10+)

    ```
    match command:
        case "start":
            ...
        case "stop" | "exit":         # несколько вариантов
            ...
        case _:                        # всё остальное
            ...
    ```

    - Выполняется первый подходящий `case`.
    - `_` — «что угодно», как `else`.
    - Умеет разбирать структуры: `case [x, y]:`, `case {"status": 200}:`.
    """,
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
        """, xp=20),
    full="""
    ## Зачем это нужно

    Когда нужно выбрать действие по значению (команда, HTTP-метод, код ответа), длинная цепочка `if/elif` с `==` становится однообразной. `match/case` (Python 3.10+) делает такой выбор нагляднее, а главное — умеет **разбирать структуру** данных: списки, словари, объекты, сразу раскладывая части по переменным. Для разбора JSON-ответов это очень удобно.

    ## Как это работает

    ```py
    match значение:
        case шаблон1:
            ...
        case шаблон2 | шаблон3:
            ...
        case шаблон if условие:
            ...
        case _:
            ...
    ```

    Выполняется **первый** подходящий `case`.

    ### Виды шаблонов

    - **литерал**: `case 200:`, `case "GET":`;
    - **или**: `case "PUT" | "PATCH":`;
    - **захват**: `case x:` — подходит всё, значение кладётся в `x` (осторожно: это не сравнение с переменной `x`!);
    - **wildcard**: `case _:` — всё остальное;
    - **последовательность**: `case [x, y]:`, `case ["go", direction]:`, `case [first, *rest]:`;
    - **словарь**: `case {"status": 200, "data": data}:` — ключи должны быть, лишние ключи допускаются;
    - **охранное условие**: `case {"status": code} if code >= 500:`.

    ## Примеры

    ### Пример 1. Простой выбор

    ```python
    def action(method):
        match method:
            case "GET":
                return "читать"
            case "POST":
                return "создать"
            case "PUT" | "PATCH":
                return "изменить"
            case _:
                return "?"

    print([action(m) for m in ["GET", "PATCH", "HEAD"]])
    ```

    ### Пример 2. Разбор ответа API

    ```python
    def handle(resp):
        match resp:
            case {"status": 200, "data": {"items": [first, *rest]}}:
                return f"первый: {first}, ещё {len(rest)}"
            case {"status": 200, "data": {"items": []}}:
                return "пустой список"
            case {"status": code, "error": msg} if code >= 400:
                return f"ошибка {code}: {msg}"
            case _:
                return "неожиданный ответ"

    print(handle({"status": 200, "data": {"items": [1, 2, 3]}}))
    print(handle({"status": 200, "data": {"items": []}}))
    print(handle({"status": 422, "error": "email invalid"}))
    print(handle({"status": 302}))
    ```

    ### Пример 3. Команды из текста

    ```python
    def parse(text):
        match text.split():
            case ["go", direction]:
                return f"идём на {direction}"
            case ["say", *words]:
                return "говорим: " + " ".join(words)
            case []:
                return "пусто"
            case _:
                return "не понимаю"

    for t in ["go north", "say hello world", "", "fly"]:
        print(repr(t), "->", parse(t))
    ```

    ## Частые ошибки

    **`case имя_переменной:`** не сравнивает с переменной, а захватывает любое значение — все следующие `case` станут недостижимы. Для сравнения с константой используй точечное имя (`case Status.OK:`) или литерал.

    **Забытый `case _:`** — если ничего не подошло, `match` просто ничего не делает, и функция вернёт `None`.

    **Python старше 3.10** — `match` не поддерживается.

    ## Шпаргалка

    ```py
    match x:
        case 1 | 2:              ...
        case [a, b]:             ...
        case {"k": v}:           ...
        case {"code": c} if c >= 500: ...
        case _:                  ...
    ```
    """,
    quiz=[
        q("Что делает `case _:`?", ["Ничего не ловит", "Ловит всё, что не подошло выше", "Ловит только None", "Синтаксическая ошибка"], 1, "`_` — шаблон-«что угодно», аналог `else`."),
        q("Что вернёт `match [1, 2]: case [x, y]: return x + y`?", ["`[1, 2]`", "`3`", "`None`", "Ошибка"], 1, "Шаблон `[x, y]` раскладывает список: x=1, y=2."),
        q("Подойдёт ли `{\"status\": 200, \"data\": 1, \"extra\": 5}` под `case {\"status\": 200}:`?", ["Нет, лишние ключи мешают", "Да, лишние ключи допускаются", "Только если extra=None", "Ошибка"], 1,
          "Шаблон словаря проверяет только указанные ключи; остальные игнорируются."),
    ]),
)

TOPIC = topic("py-conditions", "Условные операторы", "🔀", "#ff9600",
              "if/elif/else, логика, истинность, тернарный оператор и match",
              m1, m2, m3, group="Python")
