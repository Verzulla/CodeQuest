"""Тема «Цикл for»."""
from ._lib import cod, lesson, module, out, q, t, topic

P = "for"

# ============================================================
m1 = module(f"{P}-m1", "Основы for", "🔁", "Перебор коллекций, range и вложенные циклы",

lesson(f"{P}-m1-l1", "Перебор коллекций", """
    # Цикл for

    ```
    for item in коллекция:
        тело
    ```

    На каждом шаге `item` получает очередной элемент.

    - Перебирать можно список, строку (по символам), кортеж, словарь (по ключам), `range`.
    - Тело — с отступом; после цикла код продолжается.
    - Переменная цикла после завершения хранит последний элемент.
    """,
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        for fruit in ["яблоко", "банан"]:
            print("я люблю", fruit)
        print("готово")
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа?", """
        for ch in "кот":
            print(ch * 2)
        for key in {"a": 1, "b": 2}:
            print(key)
        """, hint="Перебор словаря даёт ключи."),
    cod(f"{P}-m1-l1-e3", t("""
        Выведи каждый элемент списка `tests = ["login", "search", "pay"]` на отдельной строке с префиксом `"▶ "`.

        Ожидаемый вывод:
        ```
        ▶ login
        ▶ search
        ▶ pay
        ```
        Используй цикл `for`.
        """),
        """
        tests = ["login", "search", "pay"]
        """,
        """
        def test_output():
            assert OUTPUT.strip().splitlines() == ["▶ login", "▶ search", "▶ pay"], f"Напечатано {OUTPUT!r}"

        def test_loop():
            assert "for " in open("solution.py", encoding="utf-8").read(), "Используй цикл for"
        """,
        """
        tests = ["login", "search", "pay"]
        for name in tests:
            print("▶ " + name)
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `count_char(text, ch)` — сколько раз символ `ch` встречается в строке. Реши **циклом** (без метода `count`).

        Примеры:
        ```
        count_char("banana", "a")   # → 3
        count_char("abc", "z")      # → 0
        ```
        """),
        """
        def count_char(text, ch):
            pass
        """,
        """
        def test_values():
            assert count_char("banana", "a") == 3 and count_char("abc", "z") == 0 and count_char("", "a") == 0, "Неверный подсчёт"

        def test_no_count():
            assert ".count(" not in open("solution.py", encoding="utf-8").read(), "Реши циклом, без count()"
        """,
        """
        def count_char(text, ch):
            n = 0
            for c in text:
                if c == ch:
                    n += 1
            return n
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `longest_word(words)` — самое длинное слово из списка. При равной длине — первое из них. Для пустого списка — `""`.

        Реши циклом, без `max`.

        Примеры:
        ```
        longest_word(["api", "docker", "ci", "pytest"])   # → "docker"
        longest_word([])                                  # → ""
        ```
        """),
        """
        def longest_word(words):
            pass
        """,
        """
        def test_values():
            assert longest_word(["api", "docker", "ci", "pytest"]) == "docker", "docker и pytest одной длины — нужно первое"
            assert longest_word([]) == "" and longest_word(["a"]) == "a", "Неверный результат"
        """,
        """
        def longest_word(words):
            best = ""
            for w in words:
                if len(w) > len(best):
                    best = w
            return best
        """, xp=20),
    full="""
    ## Зачем это нужно

    Повторять одно действие для множества элементов — главное, в чём компьютер сильнее человека: проверить каждый ответ API, обработать каждую строку лога, прогнать тест на каждом наборе данных. Цикл `for` перебирает элементы коллекции по одному.

    ## Как это работает

    ```py
    for переменная in итерируемое:
        тело
    ```

    1. Python берёт у коллекции следующий элемент и присваивает его переменной.
    2. Выполняет тело.
    3. Повторяет, пока элементы не кончатся.

    Что можно перебирать:
    - `list`, `tuple` — элементы;
    - `str` — символы;
    - `dict` — ключи (`.values()` — значения, `.items()` — пары);
    - `range(...)` — числа;
    - файлы — строки, и многое другое.

    Переменная цикла — обычная переменная: после цикла в ней остаётся последний элемент (если коллекция была непустой).

    ## Примеры

    ### Пример 1. Разные коллекции

    ```python
    for x in [1, 2, 3]:
        print("число", x)
    for ch in "ok":
        print("символ", ch)
    for k in {"name": "Аня", "role": "qa"}:
        print("ключ", k)
    ```

    ### Пример 2. Обработка каждого элемента

    ```python
    codes = [200, 404, 500, 201]
    for code in codes:
        status = "ok" if code < 400 else "ОШИБКА"
        print(code, status)
    ```

    ### Пример 3. Поиск самого длинного

    ```python
    words = ["api", "docker", "ci", "pytest"]
    best = ""
    for w in words:
        if len(w) > len(best):
            best = w
    print(best)
    ```

    ### Пример 4. Переменная после цикла

    ```python
    for n in [10, 20, 30]:
        pass
    print("последнее значение:", n)
    ```

    ## Частые ошибки

    **Изменение списка во время перебора** — элементы пропускаются.

    **Забытый отступ** — тело не относится к циклу.

    **Ожидание индексов вместо элементов** — `for x in items` даёт сами элементы; нужен индекс — `enumerate`.

    ## Шпаргалка

    ```py
    for x in xs: ...
    for ch in text: ...
    for key in d: ...
    for key, value in d.items(): ...
    ```
    """,
    quiz=[
        q("Что перебирает `for x in {\"a\": 1, \"b\": 2}`?", ["Значения", "Ключи", "Пары ключ-значение", "Ошибка"], 1, "Перебор словаря по умолчанию идёт по ключам."),
        q("Сколько раз выполнится тело `for ch in \"hello\":`?", ["1", "4", "5", "0"], 2, "По одному разу на каждый символ — их пять."),
        q("Что будет в `x` после `for x in [1, 2, 3]: pass`?", ["`None`", "`1`", "`3`", "Ошибка"], 2, "Переменная цикла сохраняет последнее значение."),
    ]),

lesson(f"{P}-m1-l2", "range", """
    # range

    - `range(n)` — `0, 1, …, n-1` (само `n` не входит)
    - `range(a, b)` — `a, …, b-1`
    - `range(a, b, step)` — с шагом; шаг может быть отрицательным

    ```
    for i in range(3):          # 0 1 2
    for i in range(1, 6):       # 1 2 3 4 5
    for i in range(10, 0, -2):  # 10 8 6 4 2
    ```
    """,
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        print(list(range(4)))
        print(list(range(2, 6)))
        print(list(range(0, 10, 3)))
        print(list(range(5, 0, -1)))
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа?", """
        total = 0
        for i in range(1, 5):
            total += i
        print(total)
        print(len(range(100)), list(range(3, 3)))
        """),
    cod(f"{P}-m1-l2-e3", t("""
        С помощью `for` и `range` выведи таблицу умножения на 7 от `7 x 1 = 7` до `7 x 10 = 70`.

        Каждая строка — в формате `7 x N = R`, всего 10 строк:
        ```
        7 x 1 = 7
        7 x 2 = 14
        ...
        7 x 10 = 70
        ```
        """),
        "",
        """
        def test_lines():
            lines = OUTPUT.strip().splitlines()
            assert len(lines) == 10, f"Нужно 10 строк, а напечатано {len(lines)}"
            assert lines[0] == "7 x 1 = 7" and lines[-1] == "7 x 10 = 70", f"Первая: {lines[0]!r}, последняя: {lines[-1]!r}"
        """,
        """
        for n in range(1, 11):
            print(f"7 x {n} = {7 * n}")
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `sum_even(n)` — сумма всех **чётных** чисел от 0 до `n` включительно. Используй `range` **с шагом 2**.

        Примеры:
        ```
        sum_even(10)   # → 30   (0 + 2 + 4 + 6 + 8 + 10)
        sum_even(7)    # → 12   (0 + 2 + 4 + 6)
        ```
        """),
        """
        def sum_even(n):
            pass
        """,
        """
        def test_values():
            assert [sum_even(n) for n in (10, 7, 0, 1)] == [30, 12, 0, 0], "Неверная сумма"
        """,
        """
        def sum_even(n):
            total = 0
            for i in range(0, n + 1, 2):
                total += i
            return total
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `countdown(n)` — список чисел от `n` до 1, а в конце строка `"Старт!"`. Используй `range` с отрицательным шагом.

        Примеры:
        ```
        countdown(3)   # → [3, 2, 1, "Старт!"]
        countdown(0)   # → ["Старт!"]
        ```
        """),
        """
        def countdown(n):
            pass
        """,
        """
        def test_values():
            assert countdown(3) == [3, 2, 1, "Старт!"] and countdown(0) == ["Старт!"] and countdown(1) == [1, "Старт!"], "Неверный отсчёт"
        """,
        """
        def countdown(n):
            result = []
            for i in range(n, 0, -1):
                result.append(i)
            result.append("Старт!")
            return result
        """),
    full="""
    ## Зачем это нужно

    Часто нужно повторить действие определённое число раз или перебрать числа: номера страниц, попытки запроса, строки таблицы. `range` создаёт последовательность чисел, не храня её целиком в памяти.

    ## Как это работает

    - `range(stop)` — от 0 до `stop - 1`;
    - `range(start, stop)` — от `start` до `stop - 1`;
    - `range(start, stop, step)` — с шагом; `step` может быть отрицательным, но не нулём.

    **Правая граница не входит.** Зато `range(n)` даёт ровно `n` чисел, а `range(len(xs))` — все индексы списка.

    `range` — «ленивый» объект: `range(10**9)` не займёт памяти, числа генерируются по мере перебора. Чтобы увидеть содержимое — `list(range(...))`. Длина — `len(range(...))`.

    Если перебор невозможен (например, `range(5, 1)` с положительным шагом), последовательность просто пустая.

    ## Примеры

    ### Пример 1. Все формы

    ```python
    print(list(range(5)))
    print(list(range(2, 8)))
    print(list(range(1, 20, 4)))
    print(list(range(10, 0, -3)))
    print(list(range(5, 1)))
    ```

    ### Пример 2. Повторить N раз

    ```python
    for attempt in range(1, 4):
        print(f"попытка {attempt} из 3")
    for _ in range(3):
        print("-" * 10)
    ```

    `_` — договорённость: «номер не нужен».

    ### Пример 3. Суммы с шагом

    ```python
    print(sum(range(0, 11, 2)))
    print(sum(range(1, 101)))
    ```

    ### Пример 4. Ленивость

    ```python
    r = range(0, 10**12, 7)
    print(len(r), r[5], 700 in r)
    ```

    ## Частые ошибки

    **Ошибка на единицу** — числа от 1 до 5 это `range(1, 6)`.

    **Отрицательный шаг с неправильными границами** — `range(1, 10, -1)` пустой.

    **`range(len(xs))` ради элементов** — перебирай `xs` напрямую.

    ## Шпаргалка

    ```py
    range(5)           # 0..4
    range(1, 6)        # 1..5
    range(0, 10, 2)    # 0 2 4 6 8
    range(10, 0, -1)   # 10..1
    for _ in range(n): ...
    ```
    """,
    quiz=[
        q("Что вернёт `list(range(2, 5))`?", ["`[2, 3, 4, 5]`", "`[2, 3, 4]`", "`[3, 4, 5]`", "`[2, 5]`"], 1, "Правая граница не входит."),
        q("Как получить числа 10, 8, 6, 4, 2?", ["`range(10, 2, -2)`", "`range(10, 0, -2)`", "`range(2, 10, 2)`", "`range(10, 1, 2)`"], 1, "Шаг -2, граница 0 не входит, двойка включается."),
        q("Что вернёт `list(range(5, 1))`?", ["`[5, 4, 3, 2]`", "`[]`", "Ошибка", "`[1, 2, 3, 4, 5]`"], 1, "С шагом +1 от 5 до 1 дойти нельзя — последовательность пуста."),
    ]),

lesson(f"{P}-m1-l3", "Вложенные циклы", """
    # Цикл в цикле

    ```
    for row in range(3):
        for col in range(3):
            print(row, col)
    ```

    Внутренний цикл выполняется **полностью** на каждом шаге внешнего.
    Итераций: `внешний × внутренний`.

    Применения: таблицы, пары элементов, комбинации (браузер × размер экрана).
    """,
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        for i in range(1, 3):
            for j in range(1, 3):
                print(i, j)
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа?", """
        for n in range(1, 4):
            print("*" * n)
        """),
    cod(f"{P}-m1-l3-e3", t("""
        Напиши функцию `test_matrix(browsers, sizes)` — список строк `"браузер@размер"` для **всех комбинаций**, используя вложенные циклы. Сначала все размеры для первого браузера.

        Пример:
        ```
        test_matrix(["chrome", "firefox"], [1920, 375])
        # → ["chrome@1920", "chrome@375", "firefox@1920", "firefox@375"]
        ```
        """),
        """
        def test_matrix(browsers, sizes):
            pass
        """,
        """
        def test_combinations():
            got = test_matrix(["chrome", "firefox"], [1920, 375])
            assert got == ["chrome@1920", "chrome@375", "firefox@1920", "firefox@375"], f"Получено {got}"
            assert test_matrix([], [1]) == [], "Нет браузеров — пусто"
        """,
        """
        def test_matrix(browsers, sizes):
            result = []
            for b in browsers:
                for s in sizes:
                    result.append(f"{b}@{s}")
            return result
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `multiplication_table(n)` — таблица умножения `n × n` в виде **списка строк**, числа в строке через пробел.

        Пример:
        ```
        multiplication_table(3)
        # → ["1 2 3", "2 4 6", "3 6 9"]
        ```
        """),
        """
        def multiplication_table(n):
            pass
        """,
        """
        def test_values():
            assert multiplication_table(3) == ["1 2 3", "2 4 6", "3 6 9"] and multiplication_table(1) == ["1"], "Неверная таблица"
        """,
        """
        def multiplication_table(n):
            rows = []
            for i in range(1, n + 1):
                row = []
                for j in range(1, n + 1):
                    row.append(str(i * j))
                rows.append(" ".join(row))
            return rows
        """, xp=20),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `pairs_with_sum(nums, target)` — список всех пар `(a, b)` из списка, где `a + b == target`, **без повторов** и без пары элемента с самим собой. Пара берётся в порядке индексов (`i < j`).

        Пример:
        ```
        pairs_with_sum([1, 2, 3, 4], 5)   # → [(1, 4), (2, 3)]
        ```
        Подсказка: внешний цикл по `i`, внутренний — по `j` от `i + 1`.
        """),
        """
        def pairs_with_sum(nums, target):
            pass
        """,
        """
        def test_values():
            assert pairs_with_sum([1, 2, 3, 4], 5) == [(1, 4), (2, 3)], f"Получено {pairs_with_sum([1, 2, 3, 4], 5)}"
            assert pairs_with_sum([5], 10) == [] and pairs_with_sum([2, 2], 4) == [(2, 2)], "Неверный результат"
        """,
        """
        def pairs_with_sum(nums, target):
            result = []
            for i in range(len(nums)):
                for j in range(i + 1, len(nums)):
                    if nums[i] + nums[j] == target:
                        result.append((nums[i], nums[j]))
            return result
        """, xp=25),
    full="""
    ## Зачем это нужно

    Когда данные двумерные или нужно перебрать комбинации, одного цикла мало: таблица (строки × столбцы), матрица тестов (браузеры × разрешения), сравнение каждого элемента с каждым (поиск дубликатов, пар).

    ## Как это работает

    ```py
    for a in внешний:
        for b in внутренний:
            ...
    ```

    На **каждом** шаге внешнего цикла внутренний проходит от начала до конца. Общее число итераций — произведение длин. Для 1000 × 1000 это уже миллион — вложенные циклы быстро становятся медленными.

    ### Перебор пар без повторов

    ```py
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            пара xs[i], xs[j]
    ```

    `j` начинается с `i + 1`: пара не повторяется в обратном порядке и элемент не сочетается сам с собой.

    ### break во вложенном цикле

    `break` выходит только из **ближайшего** (внутреннего) цикла.

    ## Примеры

    ### Пример 1. Координаты

    ```python
    for row in range(2):
        for col in range(3):
            print(f"({row},{col})", end=" ")
        print()
    ```

    ### Пример 2. Матрица тестов

    ```python
    browsers = ["chrome", "firefox"]
    sizes = [1920, 768, 375]
    runs = 0
    for b in browsers:
        for s in sizes:
            runs += 1
            print(f"прогон {runs}: {b} @ {s}px")
    ```

    ### Пример 3. Поиск дубликатов

    ```python
    emails = ["a@x.ru", "b@x.ru", "a@x.ru", "c@x.ru", "b@x.ru"]
    dups = []
    for i in range(len(emails)):
        for j in range(i + 1, len(emails)):
            if emails[i] == emails[j] and emails[i] not in dups:
                dups.append(emails[i])
    print(dups)
    ```

    ### Пример 4. Треугольник

    ```python
    for i in range(1, 5):
        print(" ".join(str(j) for j in range(1, i + 1)))
    ```

    ## Частые ошибки

    **Одинаковые имена переменных** во внешнем и внутреннем цикле — внутренний затирает внешний.

    **Ожидание, что break выйдет из обоих циклов.**

    **Квадратичная сложность на больших данных** — для поиска дубликатов лучше `set`.

    ## Шпаргалка

    ```py
    for i in range(rows):
        for j in range(cols): ...
    for i in range(n):
        for j in range(i + 1, n): ...   # пары без повторов
    ```
    """,
    quiz=[
        q("Сколько раз выполнится тело внутреннего цикла: `for i in range(3): for j in range(4):`?", ["7", "12", "3", "4"], 1, "3 × 4 = 12."),
        q("Из какого цикла выходит `break` во внутреннем цикле?", ["Из обоих", "Только из внутреннего", "Только из внешнего", "Из функции"], 1, "`break` прерывает ближайший цикл."),
        q("Зачем внутренний цикл начинают с `i + 1` при переборе пар?", ["Так быстрее компилируется", "Чтобы не повторять пары и не сочетать элемент с самим собой", "Чтобы избежать IndexError", "Это обязательно"], 1, "Каждая неупорядоченная пара встречается ровно один раз."),
    ]),
)

# ============================================================
m2 = module(f"{P}-m2", "Управление циклом", "🎛️", "break, continue и else у цикла",

lesson(f"{P}-m2-l1", "break — досрочный выход", """
    # break

    ```
    for code in codes:
        if code >= 500:
            print("нашли ошибку сервера")
            break          # дальше не перебираем
    ```

    - Немедленно завершает **ближайший** цикл.
    - Удобен для поиска: нашли — вышли.
    """,
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        for i in range(10):
            if i == 3:
                break
            print(i)
        print("после цикла")
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа?", """
        log = ["INFO a", "WARN b", "ERROR c", "ERROR d"]
        for i, line in enumerate(log):
            if line.startswith("ERROR"):
                print("первая ошибка на строке", i)
                break
        """),
    cod(f"{P}-m2-l1-e3", t("""
        Напиши функцию `first_error(codes)` — первый код ответа ≥ 400 из списка. Если таких нет — `None`. Используй цикл и `break` (или `return`).

        Примеры:
        ```
        first_error([200, 201, 404, 500])   # → 404
        first_error([200, 302])             # → None
        ```
        """),
        """
        def first_error(codes):
            pass
        """,
        """
        def test_values():
            assert first_error([200, 201, 404, 500]) == 404 and first_error([200, 302]) is None and first_error([]) is None, "Неверный результат"
        """,
        """
        def first_error(codes):
            found = None
            for code in codes:
                if code >= 400:
                    found = code
                    break
            return found
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `sum_until_negative(nums)` — сумма чисел по порядку, **пока** не встретится отрицательное (само отрицательное и всё после него не суммируется).

        Примеры:
        ```
        sum_until_negative([3, 5, -1, 10])   # → 8
        sum_until_negative([1, 2, 3])        # → 6
        ```
        """),
        """
        def sum_until_negative(nums):
            pass
        """,
        """
        def test_values():
            assert [sum_until_negative(x) for x in ([3, 5, -1, 10], [1, 2, 3], [-5, 1], [])] == [8, 6, 0, 0], "Неверная сумма"
        """,
        """
        def sum_until_negative(nums):
            total = 0
            for n in nums:
                if n < 0:
                    break
                total += n
            return total
        """),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `attempts_until_ok(statuses)` — номер попытки (с 1), на которой пришёл статус `200`. Если 200 не пришёл ни разу — `-1`.

        Примеры:
        ```
        attempts_until_ok([503, 502, 200, 200])   # → 3
        attempts_until_ok([500, 500])             # → -1
        ```
        Используй `enumerate(..., start=1)` и `break`.
        """),
        """
        def attempts_until_ok(statuses):
            pass
        """,
        """
        def test_values():
            assert [attempts_until_ok(x) for x in ([503, 502, 200, 200], [500, 500], [200], [])] == [3, -1, 1, -1], "Неверный номер попытки"
        """,
        """
        def attempts_until_ok(statuses):
            result = -1
            for attempt, status in enumerate(statuses, start=1):
                if status == 200:
                    result = attempt
                    break
            return result
        """),
    full="""
    ## Зачем это нужно

    Часто перебирать до конца не нужно: нашли первую ошибку, первого подходящего пользователя, успешную попытку — дальше можно не смотреть. `break` экономит время и выражает намерение «ищем первое».

    ## Как это работает

    `break` немедленно завершает **ближайший** охватывающий цикл. Выполнение продолжается с первой строки после цикла.

    ### break и функции

    Внутри функции вместо `break` часто пишут `return` — он завершает и цикл, и функцию сразу с результатом. Оба варианта нормальны; `return` обычно короче.

    ### Вложенные циклы

    `break` во внутреннем цикле не прерывает внешний. Чтобы выйти из обоих — вынеси циклы в функцию и используй `return` или флаг.

    ## Примеры

    ### Пример 1. Поиск первого

    ```python
    users = [{"name": "Аня", "active": False}, {"name": "Боря", "active": True}, {"name": "Вика", "active": True}]
    for u in users:
        if u["active"]:
            print("первый активный:", u["name"])
            break
    ```

    ### Пример 2. Повторы до успеха

    ```python
    responses = [503, 502, 200, 200]
    for attempt, status in enumerate(responses, start=1):
        print(f"попытка {attempt}: {status}")
        if status == 200:
            break
    print("итог:", status)
    ```

    ### Пример 3. break против return

    ```python
    def first_error_break(codes):
        found = None
        for c in codes:
            if c >= 400:
                found = c
                break
        return found

    def first_error_return(codes):
        for c in codes:
            if c >= 400:
                return c
        return None

    print(first_error_break([200, 404, 500]), first_error_return([200, 404, 500]))
    ```

    ### Пример 4. Выход из вложенных циклов через функцию

    ```python
    def find_cell(matrix, value):
        for i, row in enumerate(matrix):
            for j, x in enumerate(row):
                if x == value:
                    return i, j
        return None

    print(find_cell([[1, 2], [3, 4]], 3))
    ```

    ## Частые ошибки

    **`break` вне цикла** — `SyntaxError`.

    **Ожидание выхода из всех вложенных циклов.**

    **Переменная результата не инициализирована** до цикла — если `break` не сработал, её нет.

    ## Шпаргалка

    ```py
    for x in xs:
        if found(x):
            result = x
            break
    # или в функции:
    for x in xs:
        if found(x):
            return x
    return None
    ```
    """,
    quiz=[
        q("Что выведет `for i in range(5):\\n    if i == 2: break\\n    print(i)`?", ["`0 1`", "`0 1 2`", "`2 3 4`", "Ничего"], 0, "Цикл прерывается, когда i становится 2, до печати."),
        q("Что делает `break` во внутреннем из двух вложенных циклов?", ["Завершает оба", "Завершает внутренний, внешний продолжается", "Завершает программу", "Пропускает шаг"], 1, "`break` действует на ближайший цикл."),
        q("Чем в функции удобно заменить связку «переменная + break»?", ["`continue`", "`return` значения прямо из цикла", "`pass`", "`global`"], 1, "`return` сразу завершает цикл и функцию с результатом."),
    ]),

lesson(f"{P}-m2-l2", "continue — пропустить шаг", """
    # continue

    ```
    for line in log:
        if line.startswith("#"):
            continue       # пропустить комментарий
        обработать(line)
    ```

    - Прерывает **текущую** итерацию и переходит к следующей.
    - Помогает убрать вложенность: «отсеять неподходящее» в начале тела.
    """,
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        for i in range(6):
            if i % 2 == 0:
                continue
            print(i)
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа?", """
        for word in ["api", "", "ui", "  ", "ci"]:
            if not word.strip():
                continue
            print(word.upper())
        """),
    cod(f"{P}-m2-l2-e3", t("""
        Напиши функцию `parse_config(lines)` — разобрать строки конфигурации `"ключ=значение"` в словарь:

        - пустые строки и строки, начинающиеся с `#`, пропускать через `continue`;
        - ключ и значение очищать от пробелов по краям.

        Пример:
        ```
        parse_config(["# настройки", "host = localhost", "", "port=8080"])
        # → {"host": "localhost", "port": "8080"}
        ```
        """),
        """
        def parse_config(lines):
            pass
        """,
        """
        def test_values():
            got = parse_config(["# настройки", "host = localhost", "", "port=8080", "   "])
            assert got == {"host": "localhost", "port": "8080"}, f"Получено {got}"

        def test_continue():
            assert "continue" in open("solution.py", encoding="utf-8").read(), "Используй continue для пропуска строк"
        """,
        """
        def parse_config(lines):
            config = {}
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
            return config
        """, xp=20),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `sum_valid(values)` — сумма только тех элементов списка, которые являются **числами** (`int` или `float`, но не `bool`). Остальные пропускать через `continue`.

        Пример:
        ```
        sum_valid([10, "20", None, 2.5, True, 7])   # → 19.5
        ```
        """),
        """
        def sum_valid(values):
            pass
        """,
        """
        def test_values():
            assert sum_valid([10, "20", None, 2.5, True, 7]) == 19.5 and sum_valid([]) == 0 and sum_valid(["x"]) == 0, "Неверная сумма"
        """,
        """
        def sum_valid(values):
            total = 0
            for v in values:
                if isinstance(v, bool) or not isinstance(v, (int, float)):
                    continue
                total += v
            return total
        """),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `run_tests(tests)`, где `tests` — список словарей `{"name": ..., "skip": bool, "ok": bool}`.

        - пропущенные (`skip == True`) не считать — `continue`;
        - вернуть словарь `{"passed": N, "failed": M, "skipped": K}`.

        Пример:
        ```
        run_tests([{"name": "a", "skip": False, "ok": True},
                   {"name": "b", "skip": True,  "ok": False},
                   {"name": "c", "skip": False, "ok": False}])
        # → {"passed": 1, "failed": 1, "skipped": 1}
        ```
        """),
        """
        def run_tests(tests):
            pass
        """,
        """
        def test_values():
            tests = [{"name": "a", "skip": False, "ok": True}, {"name": "b", "skip": True, "ok": False}, {"name": "c", "skip": False, "ok": False}]
            assert run_tests(tests) == {"passed": 1, "failed": 1, "skipped": 1}, f"Получено {run_tests(tests)}"
            assert run_tests([]) == {"passed": 0, "failed": 0, "skipped": 0}, "Пусто — нули"
        """,
        """
        def run_tests(tests):
            stats = {"passed": 0, "failed": 0, "skipped": 0}
            for t in tests:
                if t["skip"]:
                    stats["skipped"] += 1
                    continue
                stats["passed" if t["ok"] else "failed"] += 1
            return stats
        """),
    full="""
    ## Зачем это нужно

    При обработке данных часть элементов нужно просто пропустить: пустые строки и комментарии в конфиге, некорректные значения, отключённые тесты. `continue` позволяет сразу перейти к следующему элементу и не вкладывать всю основную логику в `if`.

    ## Как это работает

    `continue` прерывает **текущий** шаг цикла: оставшаяся часть тела пропускается, и цикл переходит к следующему элементу.

    ### Приём «отсеять в начале»

    Вместо:

    ```py
    for line in lines:
        if line and not line.startswith("#"):
            ... длинная логика с отступом ...
    ```

    пишем:

    ```py
    for line in lines:
        if not line or line.startswith("#"):
            continue
        ... логика без лишнего отступа ...
    ```

    Это то же самое, что «ранний выход» в функциях, только для итерации цикла.

    ## Примеры

    ### Пример 1. Пропуск нечётных

    ```python
    for i in range(10):
        if i % 2:
            continue
        print(i, end=" ")
    print()
    ```

    ### Пример 2. Разбор конфигурации

    ```python
    lines = ["# настройки стенда", "host = staging", "", "port=8080", "   # ещё комментарий", "debug = true"]
    config = {}
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        config[key.strip()] = value.strip()
    print(config)
    ```

    ### Пример 3. Фильтрация мусора в данных

    ```python
    values = [10, "20", None, 2.5, True, -3]
    total = 0
    for v in values:
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            print("пропускаю", repr(v))
            continue
        total += v
    print("сумма:", total)
    ```

    ## Частые ошибки

    **`continue` в `while` до изменения счётчика** — бесконечный цикл: изменение переменной не выполнится.

    **`continue` вместо `break`** — цикл не останавливается, а идёт дальше.

    **Лишний `continue` в конце тела** — ничего не меняет.

    ## Шпаргалка

    ```py
    for x in xs:
        if not подходит(x):
            continue
        обработать(x)
    ```
    """,
    quiz=[
        q("Чем `continue` отличается от `break`?", ["Ничем", "`continue` переходит к следующей итерации, `break` завершает цикл", "`continue` завершает программу", "`break` пропускает шаг"], 1, "continue — следующий шаг, break — выход из цикла."),
        q("Что выведет `for i in range(4):\\n    if i == 1: continue\\n    print(i)`?", ["`0 2 3`", "`0`", "`1`", "`0 1 2 3`"], 0, "Итерация с i = 1 пропускается."),
        q("Почему `continue` в `while` может дать бесконечный цикл?", ["Никогда не может", "Если он стоит до изменения переменной условия, изменение пропускается", "while не поддерживает continue", "Из-за отступов"], 1, "Код после continue в этой итерации не выполнится, включая увеличение счётчика."),
    ]),

lesson(f"{P}-m2-l3", "else у цикла", """
    # for … else

    ```
    for user in users:
        if user == target:
            print("найден")
            break
    else:
        print("не найден")     # выполнится, если цикл НЕ был прерван break
    ```

    - `else` у цикла срабатывает, когда цикл завершился **естественно** (без `break`).
    - Удобно для поиска: «прошли всё и не нашли».
    """,
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        for n in [1, 3, 5]:
            if n % 2 == 0:
                print("есть чётное")
                break
        else:
            print("чётных нет")
        """),
    out(f"{P}-m2-l3-e2", "Что выведет программа?", """
        for n in [1, 4, 5]:
            if n % 2 == 0:
                print("есть чётное:", n)
                break
        else:
            print("чётных нет")
        for x in []:
            pass
        else:
            print("пустой цикл тоже завершился")
        """),
    cod(f"{P}-m2-l3-e3", t("""
        Напиши функцию `is_prime(n)` — простое ли число (для `n >= 2`). Используй `for … else`: перебирай делители от 2 до `n - 1`, при находке — `break`, в `else` — число простое.

        Примеры:
        ```
        is_prime(7)    # → True
        is_prime(12)   # → False
        is_prime(2)    # → True
        ```
        """),
        """
        def is_prime(n):
            pass
        """,
        """
        def test_values():
            got = [is_prime(n) for n in (2, 3, 4, 7, 12, 97, 100)]
            assert got == [True, True, False, True, False, True, False], f"Получено {got}"

        def test_for_else():
            src = open("solution.py", encoding="utf-8").read()
            assert "else:" in src and "break" in src, "Используй for … else с break"
        """,
        """
        def is_prime(n):
            result = True
            for d in range(2, n):
                if n % d == 0:
                    result = False
                    break
            else:
                result = True
            return result
        """, xp=20),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `check_all_ok(codes)` через `for … else`:

        - если встретился код ≥ 400 — вернуть `"упал на <код>"` (первый такой);
        - если все коды меньше 400 — вернуть `"все ок"`.

        Примеры:
        ```
        check_all_ok([200, 201, 500, 404])   # → "упал на 500"
        check_all_ok([200, 302])             # → "все ок"
        ```
        """),
        """
        def check_all_ok(codes):
            pass
        """,
        """
        def test_values():
            assert check_all_ok([200, 201, 500, 404]) == "упал на 500" and check_all_ok([200, 302]) == "все ок" and check_all_ok([]) == "все ок", "Неверный результат"
        """,
        """
        def check_all_ok(codes):
            for code in codes:
                if code >= 400:
                    message = f"упал на {code}"
                    break
            else:
                message = "все ок"
            return message
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `find_free_port(busy, start, end)` — первый свободный порт в диапазоне от `start` до `end` включительно (не входящий в список `busy`). Если свободных нет — `None`. Используй `for … else`.

        Пример:
        ```
        find_free_port([8000, 8001], 8000, 8005)   # → 8002
        find_free_port([80, 81], 80, 81)           # → None
        ```
        """),
        """
        def find_free_port(busy, start, end):
            pass
        """,
        """
        def test_values():
            assert find_free_port([8000, 8001], 8000, 8005) == 8002 and find_free_port([80, 81], 80, 81) is None and find_free_port([], 5, 9) == 5, "Неверный порт"
        """,
        """
        def find_free_port(busy, start, end):
            for port in range(start, end + 1):
                if port not in busy:
                    free = port
                    break
            else:
                free = None
            return free
        """),
    full="""
    ## Зачем это нужно

    Классическая задача: «перебрать всё и сказать, нашли или нет». Обычно для этого заводят флаг `found = False`. В Python есть более выразительный инструмент — ветка `else` у цикла, которая выполняется, только если цикл **не был прерван** `break`.

    ## Как это работает

    ```py
    for x in xs:
        if подходит(x):
            ...
            break
    else:
        # сюда попадаем, только если break не случился
    ```

    - Цикл дошёл до конца (в том числе если коллекция пустая) → выполняется `else`.
    - Цикл прерван `break` → `else` пропускается.
    - Работает и с `while`.

    Название неудачное — легче запомнить как «nobreak»: «если не было break».

    ### Флаг против else

    ```py
    found = False
    for x in xs:
        if good(x):
            found = True
            break
    if not found:
        ...
    ```

    `for … else` делает то же без флага. Но если команда с ним не знакома, флаг читается привычнее — оба варианта допустимы.

    ## Примеры

    ### Пример 1. Поиск с сообщением

    ```python
    users = ["anna", "boris", "vika"]
    for target in ["boris", "gosha"]:
        for u in users:
            if u == target:
                print(target, "— найден")
                break
        else:
            print(target, "— не найден")
    ```

    ### Пример 2. Простые числа

    ```python
    def is_prime(n):
        for d in range(2, int(n ** 0.5) + 1):
            if n % d == 0:
                return False
        return True

    print([n for n in range(2, 30) if is_prime(n)])
    ```

    Внутри функции `return` в цикле делает `else` ненужным — это тоже нормальный стиль.

    ### Пример 3. Проверка ответов

    ```python
    for codes in [[200, 201], [200, 503, 200]]:
        for c in codes:
            if c >= 400:
                print(codes, "— упал на", c)
                break
        else:
            print(codes, "— все ок")
    ```

    ## Частые ошибки

    **Ожидание, что `else` срабатывает, если цикл не выполнился ни разу** — он срабатывает и в этом случае (пустой цикл завершился без break).

    **Отступ `else`** — он на уровне `for`, а не внутри тела.

    **Путаница с `if/else` внутри цикла.**

    ## Шпаргалка

    ```py
    for x in xs:
        if cond(x):
            break
    else:
        print("не нашли")      # только если не было break
    ```
    """,
    quiz=[
        q("Когда выполняется `else` у цикла `for`?", ["Всегда", "Если цикл завершился без break", "Если был break", "Если коллекция пустая — никогда"], 1, "`else` — ветка «не было break»."),
        q("Выполнится ли `else`, если перебирается пустой список?", ["Да", "Нет", "Ошибка", "Зависит от содержимого"], 0, "Цикл завершился естественно (ни одной итерации, но и без break)."),
        q("На каком уровне отступа пишется `else` цикла?", ["Внутри тела цикла", "На уровне слова for", "Внутри if", "После return"], 1, "`else` относится к самому циклу."),
    ]),
)

# ============================================================
m3 = module(f"{P}-m3", "Шаблоны циклов", "🧮", "Подсчёт, поиск и перебор с помощниками",

lesson(f"{P}-m3-l1", "Подсчёт и накопление", """
    # Накопитель

    ```
    count = 0            # до цикла
    for x in items:
        if условие(x):
            count += 1   # в цикле
    print(count)         # после
    ```

    Начальные значения: сумма и счётчик — `0`, произведение — `1`, строка — `""`, словарь-счётчик — `{}`.
    """,
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        text = "я иду домой"
        vowels = 0
        for ch in text:
            if ch in "аеёиоуыэюя":
                vowels += 1
        print(vowels)
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа?", """
        counts = {}
        for r in ["pass", "fail", "pass", "skip", "pass"]:
            counts[r] = counts.get(r, 0) + 1
        print(counts)
        """),
    cod(f"{P}-m3-l1-e3", t("""
        Напиши функцию `factorial(n)` — произведение чисел от 1 до `n` (для 0 — 1). Используй цикл `for`.

        Примеры:
        ```
        factorial(5)   # → 120
        factorial(0)   # → 1
        ```
        """),
        """
        def factorial(n):
            pass
        """,
        """
        def test_values():
            assert [factorial(n) for n in (0, 1, 5, 10)] == [1, 1, 120, 3628800], "Неверный факториал"
        """,
        """
        def factorial(n):
            result = 1
            for i in range(2, n + 1):
                result *= i
            return result
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `word_freq(text)` — словарь «слово → сколько раз встретилось». Слова сравнивать в нижнем регистре, разбивать по пробелам.

        Пример:
        ```
        word_freq("Тест упал тест прошёл Тест")   # → {"тест": 3, "упал": 1, "прошёл": 1}
        ```
        """),
        """
        def word_freq(text):
            pass
        """,
        """
        def test_values():
            assert word_freq("Тест упал тест прошёл Тест") == {"тест": 3, "упал": 1, "прошёл": 1}, f"Получено {word_freq('Тест упал тест прошёл Тест')}"
            assert word_freq("") == {}, "Пустая строка — пустой словарь"
        """,
        """
        def word_freq(text):
            freq = {}
            for word in text.lower().split():
                freq[word] = freq.get(word, 0) + 1
            return freq
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `acronym(phrase)` — аббревиатура из первых букв слов, заглавными. Накапливай результат в строке через `+=`.

        Примеры:
        ```
        acronym("continuous integration")   # → "CI"
        acronym("quality assurance team")   # → "QAT"
        ```
        """),
        """
        def acronym(phrase):
            pass
        """,
        """
        def test_values():
            assert acronym("continuous integration") == "CI" and acronym("quality assurance team") == "QAT" and acronym("") == "", "Неверная аббревиатура"
        """,
        """
        def acronym(phrase):
            result = ""
            for word in phrase.split():
                result += word[0].upper()
            return result
        """),
    full="""
    ## Зачем это нужно

    Большая часть задач с циклами сводится к одному шаблону: пройти по данным и **накопить** результат — количество, сумму, произведение, строку, словарь частот. Этот шаблон нужно уметь писать не задумываясь.

    ## Как это работает

    Три шага:

    1. **До** цикла — накопитель с начальным значением.
    2. **В** цикле — обновление для каждого подходящего элемента.
    3. **После** цикла — результат.

    - счётчик/сумма — `0`, обновление `+= 1` / `+= x`;
    - произведение — `1`, `*= x`;
    - строка — `""`, `+= часть` (для больших объёмов лучше собирать список и `"".join`);
    - словарь частот — `{}`, `d[k] = d.get(k, 0) + 1`;
    - максимум/минимум — **первый элемент**.

    Для частых случаев есть готовое: `sum`, `len`, `max`, `min`, `collections.Counter`.

    ## Примеры

    ### Пример 1. Несколько счётчиков за один проход

    ```python
    codes = [200, 404, 200, 500, 201, 503]
    ok = client = server = 0
    for c in codes:
        if c < 400:
            ok += 1
        elif c < 500:
            client += 1
        else:
            server += 1
    print(f"ok={ok} 4xx={client} 5xx={server}")
    ```

    ### Пример 2. Частоты словарём и Counter

    ```python
    from collections import Counter
    results = ["pass", "fail", "pass", "skip", "pass"]
    freq = {}
    for r in results:
        freq[r] = freq.get(r, 0) + 1
    print(freq)
    print(Counter(results).most_common(1))
    ```

    ### Пример 3. Сборка строки

    ```python
    words = ["continuous", "integration", "delivery"]
    abbr = ""
    for w in words:
        abbr += w[0].upper()
    print(abbr)
    print("".join(w[0].upper() for w in words))
    ```

    ### Пример 4. Факториал

    ```python
    result = 1
    for i in range(2, 11):
        result *= i
    print(result)
    ```

    ## Частые ошибки

    **Накопитель внутри цикла** — обнуляется каждый шаг.

    **Произведение с нуля** — всегда 0.

    **`return` внутри цикла** — результат после первого элемента.

    ## Шпаргалка

    ```py
    total = 0; for x in xs: total += x
    d = {}; for k in keys: d[k] = d.get(k, 0) + 1
    s = ""; for w in ws: s += w[0]
    Counter(xs)
    ```
    """,
    quiz=[
        q("С какого значения начинать накопитель для произведения?", ["`0`", "`1`", "`None`", "`[]`"], 1, "Умножение на 0 обнулит результат; 1 — нейтральный элемент."),
        q("Что делает `d[k] = d.get(k, 0) + 1`?", ["Удаляет ключ", "Увеличивает счётчик для ключа, создавая его при первом появлении", "Ошибка, если ключа нет", "Устанавливает значение 1"], 1, "`get` вернёт 0 для нового ключа."),
        q("Где объявить счётчик `count = 0`?", ["Внутри цикла", "До цикла", "После цикла", "В условии if"], 1, "Иначе он будет сбрасываться на каждой итерации."),
    ]),

lesson(f"{P}-m3-l2", "Поиск в цикле", """
    # Шаблоны поиска

    ```
    # есть ли хотя бы один
    found = any(условие(x) for x in xs)

    # первый подходящий
    for x in xs:
        if условие(x):
            return x
    return None

    # индекс первого
    for i, x in enumerate(xs):
        if условие(x):
            return i
    ```
    """,
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        users = [{"name": "Аня", "role": "qa"}, {"name": "Боря", "role": "admin"}]
        admin = None
        for u in users:
            if u["role"] == "admin":
                admin = u["name"]
                break
        print(admin)
        print(any(u["role"] == "dev" for u in users))
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа?", """
        nums = [7, 3, 9, 3]
        pos = -1
        for i, n in enumerate(nums):
            if n == 3:
                pos = i
        print(pos)
        """, hint="Без break в переменной останется индекс последнего совпадения."),
    cod(f"{P}-m3-l2-e3", t("""
        Напиши функцию `find_user(users, name)` — словарь пользователя с данным именем (поле `"name"`) или `None`.

        Пример:
        ```
        users = [{"name": "Аня", "age": 25}, {"name": "Боря", "age": 30}]
        find_user(users, "Боря")   # → {"name": "Боря", "age": 30}
        find_user(users, "Гоша")   # → None
        ```
        """),
        """
        def find_user(users, name):
            pass
        """,
        """
        def test_values():
            users = [{"name": "Аня", "age": 25}, {"name": "Боря", "age": 30}]
            assert find_user(users, "Боря") == {"name": "Боря", "age": 30} and find_user(users, "Гоша") is None, "Неверный результат"
        """,
        """
        def find_user(users, name):
            for u in users:
                if u["name"] == name:
                    return u
            return None
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши функцию `last_index(items, value)` — индекс **последнего** вхождения `value` или `-1`.

        Примеры:
        ```
        last_index([1, 2, 1, 3], 1)   # → 2
        last_index([1, 2], 5)         # → -1
        ```
        """),
        """
        def last_index(items, value):
            pass
        """,
        """
        def test_values():
            assert last_index([1, 2, 1, 3], 1) == 2 and last_index([1, 2], 5) == -1 and last_index([], 1) == -1, "Неверный индекс"
        """,
        """
        def last_index(items, value):
            pos = -1
            for i, x in enumerate(items):
                if x == value:
                    pos = i
            return pos
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `has_duplicates(items)` — есть ли в списке повторяющиеся элементы. Иди циклом и храни уже виденные элементы в **множестве** `seen`: как только элемент уже в `seen` — сразу `True`.

        Примеры:
        ```
        has_duplicates([1, 2, 3, 2])   # → True
        has_duplicates(["a", "b"])     # → False
        ```
        """),
        """
        def has_duplicates(items):
            pass
        """,
        """
        def test_values():
            assert has_duplicates([1, 2, 3, 2]) is True and has_duplicates(["a", "b"]) is False and has_duplicates([]) is False, "Неверный результат"
        """,
        """
        def has_duplicates(items):
            seen = set()
            for x in items:
                if x in seen:
                    return True
                seen.add(x)
            return False
        """, xp=20),
    full="""
    ## Зачем это нужно

    «Есть ли в ответе упавший тест?», «найти пользователя по email», «на какой строке первая ошибка?», «есть ли дубликаты?» — поиск нужен постоянно. Важно выбрать правильный шаблон: нужен ли сам элемент, его индекс или просто факт наличия, первое совпадение или последнее.

    ## Как это работает

    ### Факт наличия
    `any(условие(x) for x in xs)` — останавливается на первом `True`.

    ### Первый подходящий элемент
    Цикл + `return x` (или `break`). После цикла — значение «не найдено» (`None`).

    Короткая форма: `next((x for x in xs if условие(x)), None)`.

    ### Индекс
    `enumerate` + `return i`. Для последнего совпадения — перебрать всё без `break` и запоминать индекс.

    ### Дубликаты
    Храни уже виденные элементы в `set` — проверка `x in seen` мгновенная, в отличие от списка.

    ## Примеры

    ### Пример 1. Разные вопросы — разные шаблоны

    ```python
    results = [("login", "pass"), ("pay", "fail"), ("cart", "fail")]
    print("есть упавшие:", any(s == "fail" for _, s in results))
    print("первый упавший:", next((n for n, s in results if s == "fail"), None))
    print("все упавшие:", [n for n, s in results if s == "fail"])
    ```

    ### Пример 2. Первое и последнее вхождение

    ```python
    log = ["INFO", "ERROR", "INFO", "ERROR", "WARN"]
    first = last = -1
    for i, level in enumerate(log):
        if level == "ERROR":
            if first == -1:
                first = i
            last = i
    print(first, last)
    ```

    ### Пример 3. Дубликаты через множество

    ```python
    emails = ["a@x.ru", "b@x.ru", "a@x.ru"]
    seen, dups = set(), []
    for e in emails:
        if e in seen:
            dups.append(e)
        seen.add(e)
    print(dups)
    ```

    ### Пример 4. Поиск в списке словарей

    ```python
    users = [{"id": 1, "email": "a@x.ru"}, {"id": 2, "email": "b@x.ru"}]
    target = "b@x.ru"
    user = next((u for u in users if u["email"] == target), None)
    print(user)
    ```

    ## Частые ошибки

    **Нет значения «не найдено»** — функция вернёт `None` неявно или упадёт на использовании несуществующей переменной.

    **break там, где нужно последнее совпадение.**

    **Поиск дубликатов через `in` по списку** — медленно на больших данных.

    ## Шпаргалка

    ```py
    any(cond(x) for x in xs)
    next((x for x in xs if cond(x)), None)
    for i, x in enumerate(xs):
        if cond(x): return i
    seen = set(); x in seen; seen.add(x)
    ```
    """,
    quiz=[
        q("Что вернёт `next((x for x in [1, 2, 3] if x > 5), \"нет\")`?", ["`None`", "`\"нет\"`", "`StopIteration`", "`3`"], 1, "Подходящих нет — возвращается значение по умолчанию."),
        q("Почему `seen` для поиска дубликатов делают множеством?", ["Так красивее", "Проверка `x in set` мгновенная, а в списке — перебором", "Список нельзя использовать", "Множество сортирует элементы"], 1, "Множество использует хеш-таблицу."),
        q("Как найти индекс **последнего** совпадения одним проходом?", ["Остановиться на первом с break", "Перебрать всё без break и запоминать индекс при каждом совпадении", "Использовать any", "Невозможно"], 1, "Последнее присвоение и будет последним совпадением."),
    ]),

lesson(f"{P}-m3-l3", "Помощники перебора", """
    # Встроенные помощники

    - `enumerate(xs, start=1)` — номер + элемент
    - `zip(a, b)` — параллельно
    - `reversed(xs)` — в обратном порядке
    - `sorted(xs, key=...)` — в отсортированном порядке
    - `d.items()` — пары ключ-значение словаря

    Они не меняют исходную коллекцию.
    """,
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        for i, name in enumerate(reversed(["a", "b", "c"]), start=1):
            print(i, name)
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа?", """
        prices = {"чай": 300, "кофе": 500, "сок": 150}
        for item, price in sorted(prices.items(), key=lambda p: p[1]):
            print(item, price)
        """),
    cod(f"{P}-m3-l3-e3", t("""
        Напиши функцию `leaderboard(scores)`, где `scores` — словарь `{имя: очки}`. Вернуть список строк `"<место>. <имя> — <очки>"`, отсортированный по убыванию очков, места с 1.

        Пример:
        ```
        leaderboard({"Боря": 50, "Аня": 80, "Вика": 65})
        # → ["1. Аня — 80", "2. Вика — 65", "3. Боря — 50"]
        ```
        """),
        """
        def leaderboard(scores):
            pass
        """,
        """
        def test_values():
            got = leaderboard({"Боря": 50, "Аня": 80, "Вика": 65})
            assert got == ["1. Аня — 80", "2. Вика — 65", "3. Боря — 50"], f"Получено {got}"
        """,
        """
        def leaderboard(scores):
            ordered = sorted(scores.items(), key=lambda p: p[1], reverse=True)
            return [f"{i}. {name} — {pts}" for i, (name, pts) in enumerate(ordered, start=1)]
        """, xp=20),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `diff_report(expected, actual)` — сравни два списка одинаковой длины попарно (`zip`) и верни список строк для **несовпадений** в формате `"#<номер с 1>: ожидали <e>, получили <a>"`.

        Пример:
        ```
        diff_report([200, 201, 404], [200, 500, 404])
        # → ["#2: ожидали 201, получили 500"]
        ```
        """),
        """
        def diff_report(expected, actual):
            pass
        """,
        """
        def test_values():
            assert diff_report([200, 201, 404], [200, 500, 404]) == ["#2: ожидали 201, получили 500"], "Неверный отчёт"
            assert diff_report([1], [1]) == [], "Совпадают — пусто"
        """,
        """
        def diff_report(expected, actual):
            report = []
            for i, (e, a) in enumerate(zip(expected, actual), start=1):
                if e != a:
                    report.append(f"#{i}: ожидали {e}, получили {a}")
            return report
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `last_n_lines(lines, n)` — последние `n` строк лога **в обратном порядке** (самая свежая первой), каждая с номером строки в исходном списке (с 1): `"<номер>: <строка>"`.

        Пример:
        ```
        last_n_lines(["a", "b", "c", "d"], 2)   # → ["4: d", "3: c"]
        ```
        Используй `enumerate` и `reversed` (или срез).
        """),
        """
        def last_n_lines(lines, n):
            pass
        """,
        """
        def test_values():
            assert last_n_lines(["a", "b", "c", "d"], 2) == ["4: d", "3: c"] and last_n_lines(["x"], 5) == ["1: x"] and last_n_lines([], 3) == [], "Неверный результат"
        """,
        """
        def last_n_lines(lines, n):
            numbered = [f"{i}: {line}" for i, line in enumerate(lines, start=1)]
            return list(reversed(numbered))[:n]
        """),
    full="""
    ## Зачем это нужно

    Встроенные функции-помощники избавляют от ручной работы с индексами: пронумеровать, перебрать два списка параллельно, пройти в обратном или отсортированном порядке, перебрать словарь парами. Код становится короче, понятнее и надёжнее.

    ## Как это работает

    - `enumerate(xs, start=0)` — пары `(номер, элемент)`.
    - `zip(a, b, ...)` — кортежи из элементов на одинаковых позициях; останавливается на самой короткой коллекции (`strict=True` — ошибка при разной длине).
    - `reversed(xs)` — итератор в обратном порядке (для последовательностей).
    - `sorted(xs, key=..., reverse=...)` — новый отсортированный список.
    - `dict.items()` / `.keys()` / `.values()` — представления словаря.

    Их можно комбинировать: `enumerate(sorted(...))`, `zip(xs, reversed(ys))`.

    ## Примеры

    ### Пример 1. Комбинации помощников

    ```python
    tests = {"login": 1.2, "pay": 3.4, "search": 0.2}
    for place, (name, sec) in enumerate(sorted(tests.items(), key=lambda p: p[1], reverse=True), start=1):
        print(f"{place}. {name:<7} {sec} с")
    ```

    ### Пример 2. Параллельное сравнение

    ```python
    expected = ["login", "pay", "logout"]
    actual = ["login", "cart", "logout"]
    for i, (e, a) in enumerate(zip(expected, actual), start=1):
        print(f"шаг {i}: {'✅' if e == a else '❌'} {e} / {a}")
    ```

    ### Пример 3. Свежие записи первыми

    ```python
    log = ["10:00 start", "10:01 login", "10:02 ERROR", "10:03 retry"]
    for line in reversed(log[-3:]):
        print(line)
    ```

    ### Пример 4. Соседние элементы

    ```python
    times = [100, 120, 90, 300]
    for prev, cur in zip(times, times[1:]):
        change = cur - prev
        print(f"{prev} -> {cur}: {'+' if change > 0 else ''}{change}")
    ```

    ## Частые ошибки

    **`reversed` для множества или словаря старых версий** — работает только с последовательностями (и словарями с Python 3.8).

    **Повторное использование итератора** `zip`/`enumerate`/`reversed` — одноразовые.

    **`sorted(d)` ожидая пары** — сортирует ключи; для пар — `sorted(d.items())`.

    ## Шпаргалка

    ```py
    for i, x in enumerate(xs, start=1): ...
    for a, b in zip(xs, ys): ...
    for x in reversed(xs): ...
    for k, v in sorted(d.items(), key=lambda p: p[1]): ...
    for a, b in zip(xs, xs[1:]): ...     # соседи
    ```
    """,
    quiz=[
        q("Что перебирает `sorted({\"b\": 1, \"a\": 2})`?", ["Пары", "Значения", "Отсортированные ключи", "Ошибка"], 2, "`sorted` по словарю сортирует ключи: `['a', 'b']`."),
        q("Что даёт `zip(xs, xs[1:])`?", ["Копию списка", "Пары соседних элементов", "Развёрнутый список", "Пары с индексами"], 1, "Элемент и следующий за ним."),
        q("Можно ли дважды перебрать один и тот же объект `enumerate(xs)`?", ["Да", "Нет, это одноразовый итератор", "Только если xs — список", "Только с reversed"], 1, "Второй проход по исчерпанному итератору пуст."),
    ]),
)

TOPIC = topic("py-for", "Цикл for", "🔁", "#00a88e",
              "Перебор коллекций, range, вложенные циклы, break, continue и шаблоны",
              m1, m2, m3, group="Python")
