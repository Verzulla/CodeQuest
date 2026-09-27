"""Тема «Цикл while»."""
from ._lib import cod, lesson, module, out, q, t, topic

P = "whl"

# ============================================================
m1 = module(f"{P}-m1", "Основы while", "🔄", "Условие, счётчики и while True",

lesson(f"{P}-m1-l1", "while и условие", """
    # Цикл while

    ```
    n = 3
    while n > 0:
        print(n)
        n -= 1
    print("Старт!")
    ```

    - Повторяет тело, **пока условие истинно**.
    - Условие проверяется **перед** каждой итерацией.
    - Если условие ложно сразу — тело не выполнится ни разу.
    """,
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        n = 3
        while n > 0:
            print(n)
            n -= 1
        print("Старт!")
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа?", """
        x = 10
        while x < 5:
            print("не выполнится")
        print("x =", x)
        n = 1
        while n < 20:
            n *= 3
        print(n)
        """, hint="Во втором цикле: 1 → 3 → 9 → 27, проверка идёт перед итерацией."),
    cod(f"{P}-m1-l1-e3", t("""
        С помощью `while` выведи числа от 1 до 5, каждое на новой строке.

        Ожидаемый вывод:
        ```
        1
        2
        3
        4
        5
        ```
        Не используй `for`.
        """),
        "",
        """
        def test_output():
            assert OUTPUT.split() == ["1", "2", "3", "4", "5"], f"Напечатано {OUTPUT.split()}"

        def test_while():
            src = open("solution.py", encoding="utf-8").read()
            assert "while " in src and "for " not in src, "Используй while, без for"
        """,
        """
        i = 1
        while i <= 5:
            print(i)
            i += 1
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `doubling_steps(start, limit)` — сколько раз нужно удвоить `start`, чтобы число стало **больше или равно** `limit`.

        Примеры:
        ```
        doubling_steps(1, 10)    # → 4   (1 → 2 → 4 → 8 → 16)
        doubling_steps(5, 5)     # → 0
        doubling_steps(3, 100)   # → 6   (3 → 6 → 12 → 24 → 48 → 96 → 192)
        ```
        """),
        """
        def doubling_steps(start, limit):
            pass
        """,
        """
        def test_values():
            assert [doubling_steps(1, 10), doubling_steps(5, 5), doubling_steps(3, 100)] == [4, 0, 6], "Неверное число шагов"
        """,
        """
        def doubling_steps(start, limit):
            steps = 0
            while start < limit:
                start *= 2
                steps += 1
            return steps
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `years_to_goal(balance, goal, rate)` — сколько лет нужно, чтобы вклад `balance` вырос до `goal` при ежегодном росте на `rate` процентов (проценты начисляются раз в год на текущую сумму).

        Примеры:
        ```
        years_to_goal(1000, 2000, 10)   # → 8
        years_to_goal(1000, 1000, 5)    # → 0
        ```
        """),
        """
        def years_to_goal(balance, goal, rate):
            pass
        """,
        """
        def test_values():
            assert years_to_goal(1000, 2000, 10) == 8 and years_to_goal(1000, 1000, 5) == 0 and years_to_goal(100, 121, 10) == 2, "Неверное число лет"
        """,
        """
        def years_to_goal(balance, goal, rate):
            years = 0
            while balance < goal:
                balance *= 1 + rate / 100
                years += 1
            return years
        """, xp=20),
    full="""
    ## Зачем это нужно

    `for` хорош, когда заранее известно, что перебирать. А если повторять нужно, **пока выполняется условие**? Пока сервер не ответил, пока число не стало меньше порога, пока в очереди есть задачи, пока пользователь не ввёл правильный пароль. Для этого есть `while`.

    ## Как это работает

    ```py
    while условие:
        тело
    ```

    1. Проверяется условие.
    2. Истинно — выполняется тело, и всё повторяется с шага 1.
    3. Ложно — цикл завершается, программа идёт дальше.

    Если условие ложно с самого начала, тело не выполнится ни разу.

    ### Главное правило

    В теле должно быть что-то, что **приближает** условие к ложному: уменьшение счётчика, изменение данных, `break`. Иначе цикл будет бесконечным (в CodeQuest такой код остановится через 5 секунд).

    ### for или while?

    - Известна коллекция или число повторов → `for`.
    - Повторяем «до события» → `while`.

    ## Примеры

    ### Пример 1. Обратный отсчёт

    ```python
    n = 5
    while n > 0:
        print(n, end=" ")
        n -= 1
    print("Старт!")
    ```

    ### Пример 2. Сколько шагов до порога

    ```python
    value, steps = 1, 0
    while value < 1000:
        value *= 2
        steps += 1
    print(steps, value)
    ```

    ### Пример 3. Рост вклада

    ```python
    balance, years = 1000.0, 0
    while balance < 2000:
        balance *= 1.10
        years += 1
    print(f"через {years} лет: {balance:.2f}")
    ```

    ### Пример 4. Условие ложно сразу

    ```python
    tasks = []
    while tasks:
        print("обрабатываю", tasks.pop())
    print("очередь пуста — цикл не выполнялся")
    ```

    ## Частые ошибки

    **Забыли изменить переменную условия** — бесконечный цикл.

    **Ошибка на единицу** — `<` против `<=`.

    **`while` для перебора списка по индексу** — многословно; для этого есть `for`.

    ## Шпаргалка

    ```py
    while cond:
        ...
        изменить_условие
    while items:          # пока не пусто
        items.pop()
    ```
    """,
    quiz=[
        q("Сколько раз выполнится тело `n = 0\\nwhile n < 3:\\n    n += 1`?", ["2", "3", "4", "Бесконечно"], 1, "n: 0 → 1 → 2 → 3, после трёх итераций условие ложно."),
        q("Что будет, если условие `while` ложно с самого начала?", ["Тело выполнится один раз", "Тело не выполнится", "Ошибка", "Бесконечный цикл"], 1, "Условие проверяется перед каждой итерацией, включая первую."),
        q("Когда `while` предпочтительнее `for`?", ["Для перебора списка", "Когда повторяем до наступления события и число шагов заранее неизвестно", "Всегда", "Никогда"], 1, "while — «пока условие истинно»."),
    ]),

lesson(f"{P}-m1-l2", "Счётчики и бесконечные циклы", """
    # Счётчик

    ```
    attempt = 0
    while attempt < 3:
        attempt += 1       # ← без этой строки цикл бесконечный
        print("попытка", attempt)
    ```

    Типичные причины бесконечного цикла:
    - переменная условия не меняется;
    - меняется «не в ту сторону»;
    - «перепрыгивает» точное значение (`x != 0` при шаге 2).
    """,
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        attempt = 0
        while attempt < 3:
            attempt += 1
            print("попытка", attempt)
        print("итого", attempt)
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа?", """
        i = 0
        total = 0
        while i < 10:
            i += 3
            total += i
        print(i, total)
        """),
    cod(f"{P}-m1-l2-e3", t("""
        В функции `sum_to(n)` баг: цикл никогда не заканчивается. Исправь его, чтобы функция возвращала сумму чисел от 1 до `n`.

        Примеры:
        ```
        sum_to(4)   # → 10
        sum_to(0)   # → 0
        ```
        """),
        """
        def sum_to(n):
            total = 0
            i = 1
            while i <= n:
                total += i
            return total
        """,
        """
        def test_values():
            assert [sum_to(n) for n in (4, 0, 1, 100)] == [10, 0, 1, 5050], "Неверная сумма"
        """,
        """
        def sum_to(n):
            total = 0
            i = 1
            while i <= n:
                total += i
                i += 1
            return total
        """),
    cod(f"{P}-m1-l2-e4", t("""
        В функции `countdown_even(n)` баг: для нечётного `n` цикл бесконечный, потому что условие `n != 0` «перепрыгивается». Исправь так, чтобы функция возвращала список чётных чисел от `n` вниз до 0 включительно (для нечётного `n` — начиная с `n - 1`).

        Примеры:
        ```
        countdown_even(6)   # → [6, 4, 2, 0]
        countdown_even(5)   # → [4, 2, 0]
        ```
        """),
        """
        def countdown_even(n):
            result = []
            while n != 0:
                if n % 2 == 0:
                    result.append(n)
                n -= 2
            result.append(0)
            return result
        """,
        """
        def test_values():
            assert countdown_even(6) == [6, 4, 2, 0] and countdown_even(5) == [4, 2, 0] and countdown_even(0) == [0] and countdown_even(1) == [0], "Неверный результат"
        """,
        """
        def countdown_even(n):
            if n % 2:
                n -= 1
            result = []
            while n >= 0:
                result.append(n)
                n -= 2
            return result
        """, xp=20),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `collatz_steps(n)` — сколько шагов гипотезы Коллатца нужно, чтобы из `n` получить 1:

        - чётное число делим на 2;
        - нечётное — умножаем на 3 и прибавляем 1.

        Примеры:
        ```
        collatz_steps(1)    # → 0
        collatz_steps(6)    # → 8    (6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1)
        collatz_steps(27)   # → 111
        ```
        """),
        """
        def collatz_steps(n):
            pass
        """,
        """
        def test_values():
            assert [collatz_steps(n) for n in (1, 6, 27)] == [0, 8, 111], "Неверное число шагов"
        """,
        """
        def collatz_steps(n):
            steps = 0
            while n != 1:
                n = n // 2 if n % 2 == 0 else 3 * n + 1
                steps += 1
            return steps
        """),
    full="""
    ## Зачем это нужно

    Бесконечный цикл — самая частая ошибка с `while`. В автотестах он выглядит как «тест завис и CI убил его через час». Нужно уметь писать циклы так, чтобы они гарантированно завершались, и находить причину, когда не завершаются.

    ## Как это работает

    Цикл завершается, когда условие становится ложным. Значит, **каждая итерация** должна менять что-то, от чего зависит условие.

    ### Типичные причины зависаний

    1. **Переменная не меняется**: забыли `i += 1`.
    2. **Меняется не в ту сторону**: `while i < 10: i -= 1`.
    3. **Точное значение «перепрыгивается»**: `while x != 0: x -= 2` при нечётном `x`. Надёжнее условия с неравенствами: `while x > 0`.
    4. **`continue` до изменения счётчика** — изменение пропускается.
    5. **Дробные числа**: `while x != 1.0: x += 0.1` — из-за погрешности `x` может никогда не стать ровно `1.0`.

    ### Страховка

    Для циклов «до события» полезен **предохранитель**: максимальное число итераций или таймаут. В тестах так делают все ожидания.

    ## Примеры

    ### Пример 1. Правильный счётчик

    ```python
    i, total = 1, 0
    while i <= 5:
        total += i
        i += 1
    print(total)
    ```

    ### Пример 2. Перепрыгнутое значение

    ```python
    x = 5
    steps = 0
    while x != 0 and steps < 10:     # предохранитель спасает от зависания
        x -= 2
        steps += 1
    print("x =", x, "шагов:", steps)
    x = 5
    while x > 0:                      # надёжное условие
        x -= 2
    print("x =", x)
    ```

    ### Пример 3. Погрешность дробных

    ```python
    x, steps = 0.0, 0
    while x != 1.0 and steps < 20:
        x += 0.1
        steps += 1
    print(x, steps)     # 1.0 так и не получилось ровно
    ```

    ### Пример 4. Коллатц — цикл без заранее известной длины

    ```python
    n, path = 6, [6]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        path.append(n)
    print(path, "шагов:", len(path) - 1)
    ```

    ## Частые ошибки

    **Нет изменения условия** · **`!=` вместо `>`/`<`** · **сравнение float на равенство** · **нет предохранителя** в ожиданиях.

    ## Шпаргалка

    ```py
    while i < n:
        ...
        i += 1                 # всегда меняй условие
    while x > 0: ...           # неравенство надёжнее !=
    while not done and tries < MAX: ...   # предохранитель
    ```
    """,
    quiz=[
        q("Почему `x = 5\\nwhile x != 0: x -= 2` зависает?", ["Ошибка синтаксиса", "x проходит 5, 3, 1, -1… и никогда не равен 0", "while не работает с вычитанием", "Не зависает"], 1, "Нечётное число при шаге 2 перепрыгивает ноль."),
        q("Как защитить цикл ожидания от бесконечного выполнения?", ["Никак", "Добавить предохранитель: максимум попыток или таймаут", "Использовать for", "Убрать условие"], 1, "Ограничение числа итераций гарантирует завершение."),
        q("Почему опасно `while x != 1.0: x += 0.1`?", ["Нельзя складывать float", "Из-за погрешности x может никогда не стать ровно 1.0", "0.1 — не число", "Это безопасно"], 1, "Дробные хранятся приближённо, точное равенство может не наступить."),
    ]),

lesson(f"{P}-m1-l3", "while True и break", """
    # Цикл с выходом из середины

    ```
    while True:
        команда = получить()
        if команда == "stop":
            break
        обработать(команда)
    ```

    - `while True` — «бесконечный» цикл, выход — только через `break` (или `return`).
    - Удобно, когда условие выхода проверяется **в середине** тела.
    """,
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        commands = ["start", "status", "stop", "never"]
        i = 0
        while True:
            cmd = commands[i]
            i += 1
            if cmd == "stop":
                break
            print("выполняю", cmd)
        print("остановлено")
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа?", """
        n = 0
        while True:
            n += 1
            if n % 2 == 0:
                continue
            if n > 7:
                break
            print(n)
        """),
    cod(f"{P}-m1-l3-e3", t("""
        Напиши функцию `read_until_stop(lines)` — перебирать строки через `while True` и собирать их в список, пока не встретится строка `"STOP"` (её не включать). Если `"STOP"` нет — собрать все строки.

        Пример:
        ```
        read_until_stop(["a", "b", "STOP", "c"])   # → ["a", "b"]
        read_until_stop(["a"])                     # → ["a"]
        ```
        """),
        """
        def read_until_stop(lines):
            pass
        """,
        """
        def test_values():
            assert read_until_stop(["a", "b", "STOP", "c"]) == ["a", "b"] and read_until_stop(["a"]) == ["a"] and read_until_stop([]) == [], "Неверный результат"

        def test_while_true():
            assert "while True" in open("solution.py", encoding="utf-8").read(), "Используй while True"
        """,
        """
        def read_until_stop(lines):
            result = []
            i = 0
            while True:
                if i >= len(lines) or lines[i] == "STOP":
                    break
                result.append(lines[i])
                i += 1
            return result
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `first_power_over(base, limit)` — наименьшую степень `base` (base¹, base², …), которая **больше** `limit`. Используй `while True`.

        Примеры:
        ```
        first_power_over(2, 100)   # → 128
        first_power_over(10, 5)    # → 10
        ```
        """),
        """
        def first_power_over(base, limit):
            pass
        """,
        """
        def test_values():
            assert first_power_over(2, 100) == 128 and first_power_over(10, 5) == 10 and first_power_over(3, 27) == 81, "Неверная степень"
        """,
        """
        def first_power_over(base, limit):
            value = base
            while True:
                if value > limit:
                    return value
                value *= base
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `login_attempts(passwords, correct, max_attempts=3)` — симуляция входа:

        - перебирай пароли по очереди через `while True`;
        - верный пароль → вернуть `"вход выполнен с попытки <N>"`;
        - после `max_attempts` неверных попыток (или если пароли кончились) → `"аккаунт заблокирован"`.

        Примеры:
        ```
        login_attempts(["1", "2", "qwerty"], "qwerty")   # → "вход выполнен с попытки 3"
        login_attempts(["1", "2", "3", "qwerty"], "qwerty")   # → "аккаунт заблокирован"
        ```
        """),
        """
        def login_attempts(passwords, correct, max_attempts=3):
            pass
        """,
        """
        def test_values():
            assert login_attempts(["1", "2", "qwerty"], "qwerty") == "вход выполнен с попытки 3", "Третья попытка верная"
            assert login_attempts(["1", "2", "3", "qwerty"], "qwerty") == "аккаунт заблокирован", "Три неверных — блок"
            assert login_attempts(["qwerty"], "qwerty") == "вход выполнен с попытки 1", "Первая попытка верная"
            assert login_attempts(["x"], "qwerty") == "аккаунт заблокирован", "Пароли кончились — блок"
        """,
        """
        def login_attempts(passwords, correct, max_attempts=3):
            attempt = 0
            while True:
                if attempt >= max_attempts or attempt >= len(passwords):
                    return "аккаунт заблокирован"
                if passwords[attempt] == correct:
                    return f"вход выполнен с попытки {attempt + 1}"
                attempt += 1
        """, xp=20),
    full="""
    ## Зачем это нужно

    Иногда условие выхода удобно проверять не в начале итерации, а в середине: сначала получить данные, потом решить, продолжать ли. Классика — меню программы, чтение команд до «stop», игровой цикл, повторы запроса с проверкой ответа. Для этого используют `while True` с `break`.

    ## Как это работает

    ```py
    while True:
        данные = получить()
        if конец(данные):
            break
        обработать(данные)
    ```

    - `while True` сам по себе не завершится — выход **только** через `break`, `return` или исключение.
    - Проверка стоит там, где у нас уже есть всё нужное для решения.
    - Хорошо сочетается с предохранителем: `if attempt >= MAX: break`.

    ### Сравни

    С условием в заголовке приходится дублировать получение данных:

    ```py
    cmd = get()
    while cmd != "stop":
        process(cmd)
        cmd = get()       # повтор строки
    ```

    `while True` убирает дублирование.

    ## Примеры

    ### Пример 1. Команды до stop

    ```python
    commands = iter(["start", "status", "stop", "never"])
    while True:
        cmd = next(commands)
        if cmd == "stop":
            break
        print("выполняю", cmd)
    print("остановлено")
    ```

    ### Пример 2. Повторы запроса

    ```python
    responses = iter([503, 502, 200])
    attempt = 0
    while True:
        attempt += 1
        status = next(responses)
        print(f"попытка {attempt}: {status}")
        if status == 200 or attempt >= 5:
            break
    ```

    ### Пример 3. return вместо break в функции

    ```python
    def first_power_over(base, limit):
        value = base
        while True:
            if value > limit:
                return value
            value *= base

    print(first_power_over(2, 1000), first_power_over(3, 10))
    ```

    ## Частые ошибки

    **Нет ни одного `break`** (или он недостижим) — вечный цикл.

    **`break` внутри вложенного цикла** — выходит только из него, а не из `while True`.

    **Нет предохранителя** там, где событие может не наступить никогда.

    ## Шпаргалка

    ```py
    while True:
        x = get()
        if stop(x):
            break
        handle(x)
    ```
    """,
    quiz=[
        q("Как завершить цикл `while True`?", ["Он завершится сам", "Через break, return или исключение", "Только перезапуском программы", "Через continue"], 1, "Условие всегда истинно, поэтому выход — только явный."),
        q("Зачем использовать `while True` вместо условия в заголовке?", ["Он быстрее", "Когда решение о выходе принимается в середине итерации и не хочется дублировать код", "Так требует PEP 8", "Нет причин"], 1, "Условие проверяется там, где уже есть данные."),
        q("Что выведет `n = 0\\nwhile True:\\n    n += 1\\n    if n == 3: break\\nprint(n)`?", ["`2`", "`3`", "`4`", "Зависнет"], 1, "Цикл прерывается, когда n становится 3."),
    ]),
)

# ============================================================
m2 = module(f"{P}-m2", "while на практике", "⏱️", "Цифры числа, повторы с ожиданием и очереди",

lesson(f"{P}-m2-l1", "Работа с цифрами числа", """
    # Разбор числа на цифры

    ```
    n = 2024
    while n > 0:
        digit = n % 10     # последняя цифра
        n //= 10           # отбросить её
    ```

    Так считают количество цифр, их сумму, переворачивают число — без превращения в строку.
    """,
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        n = 2024
        while n > 0:
            print(n % 10)
            n //= 10
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа?", """
        n, count = 1000, 0
        while n > 0:
            n //= 10
            count += 1
        print(count)
        """),
    cod(f"{P}-m2-l1-e3", t("""
        Напиши функцию `digit_sum(n)` — сумма цифр неотрицательного числа **без** перевода в строку.

        Примеры:
        ```
        digit_sum(2024)   # → 8
        digit_sum(0)      # → 0
        digit_sum(999)    # → 27
        ```
        """),
        """
        def digit_sum(n):
            pass
        """,
        """
        def test_values():
            assert [digit_sum(n) for n in (2024, 0, 999, 7)] == [8, 0, 27, 7], "Неверная сумма цифр"

        def test_no_str():
            assert "str(" not in open("solution.py", encoding="utf-8").read(), "Реши без str()"
        """,
        """
        def digit_sum(n):
            total = 0
            while n > 0:
                total += n % 10
                n //= 10
            return total
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `reverse_number(n)` — число с цифрами в обратном порядке, **без** строк.

        Примеры:
        ```
        reverse_number(1234)   # → 4321
        reverse_number(100)    # → 1
        reverse_number(7)      # → 7
        ```
        Идея: `result = result * 10 + n % 10`.
        """),
        """
        def reverse_number(n):
            pass
        """,
        """
        def test_values():
            assert [reverse_number(n) for n in (1234, 100, 7, 0)] == [4321, 1, 7, 0], "Неверный результат"

        def test_no_str():
            assert "str(" not in open("solution.py", encoding="utf-8").read(), "Реши без str()"
        """,
        """
        def reverse_number(n):
            result = 0
            while n > 0:
                result = result * 10 + n % 10
                n //= 10
            return result
        """, xp=20),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `digital_root(n)` — «цифровой корень»: складывай цифры числа, пока не останется одна цифра.

        Примеры:
        ```
        digital_root(16)       # → 7    (1 + 6)
        digital_root(942)      # → 6    (9 + 4 + 2 = 15 → 1 + 5 = 6)
        digital_root(132189)   # → 6
        ```
        Понадобятся два вложенных цикла `while`.
        """),
        """
        def digital_root(n):
            pass
        """,
        """
        def test_values():
            assert [digital_root(n) for n in (16, 942, 132189, 5, 0)] == [7, 6, 6, 5, 0], "Неверный цифровой корень"
        """,
        """
        def digital_root(n):
            while n >= 10:
                total = 0
                while n > 0:
                    total += n % 10
                    n //= 10
                n = total
            return n
        """),
    full="""
    ## Зачем это нужно

    Задачи с цифрами числа — классика собеседований и отличная тренировка `while`: количество заранее неизвестно, и мы повторяем, пока число не «закончится». Приём `% 10` и `// 10` пригождается и в практике: контрольные суммы, номера документов, проверка номеров карт (алгоритм Луна).

    ## Как это работает

    Для неотрицательного целого `n`:
    - `n % 10` — последняя цифра;
    - `n // 10` — число без последней цифры.

    Цикл:

    ```py
    while n > 0:
        d = n % 10
        ...
        n //= 10
    ```

    Особый случай — `0`: цикл не выполнится ни разу. Если ноль должен считаться «одной цифрой», обработай его отдельно.

    ### Сборка числа обратно

    `result = result * 10 + d` — дописать цифру справа.

    ## Примеры

    ### Пример 1. Цифры справа налево

    ```python
    n = 90417
    digits = []
    while n > 0:
        digits.append(n % 10)
        n //= 10
    print(digits, list(reversed(digits)))
    ```

    ### Пример 2. Разворот числа

    ```python
    n, result = 1230, 0
    while n > 0:
        result = result * 10 + n % 10
        n //= 10
    print(result)
    ```

    ### Пример 3. Проверка номера карты (алгоритм Луна)

    ```python
    def luhn_ok(number):
        total, position = 0, 0
        while number > 0:
            d = number % 10
            if position % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            total += d
            number //= 10
            position += 1
        return total % 10 == 0

    print(luhn_ok(4539578763621486), luhn_ok(4539578763621487))
    ```

    ### Пример 4. Цифровой корень

    ```python
    n = 942
    while n >= 10:
        s = 0
        while n > 0:
            s += n % 10
            n //= 10
        n = s
        print("шаг:", n)
    ```

    ## Частые ошибки

    **Ноль** — цикл не выполняется, «цифр 0».

    **Отрицательные числа** — `-7 % 10` в Python равно `3`. Работай с `abs(n)`.

    **Забыли `n //= 10`** — бесконечный цикл.

    ## Шпаргалка

    ```py
    while n > 0:
        d = n % 10       # последняя цифра
        n //= 10         # отбросить
    result = result * 10 + d   # дописать справа
    ```
    """,
    quiz=[
        q("Что вернёт `1234 % 10` и `1234 // 10`?", ["`4` и `123`", "`1` и `234`", "`123` и `4`", "`4` и `123.4`"], 0, "Остаток — последняя цифра, целая часть — число без неё."),
        q("Сколько раз выполнится тело `while n > 0: n //= 10` при `n = 0`?", ["1", "0", "Бесконечно", "10"], 1, "Условие сразу ложно."),
        q("Что даст `result = result * 10 + 7` при `result = 12`?", ["`19`", "`127`", "`84`", "`1207`"], 1, "Умножение на 10 сдвигает цифры, 7 дописывается справа."),
    ]),

lesson(f"{P}-m2-l2", "Повторы и ожидания", """
    # Опрос с таймаутом

    ```
    start = now()
    while not condition():
        if now() - start >= timeout:
            raise TimeoutError
        sleep(poll)
    ```

    Так устроены явные ожидания в UI-тестах и повторы запросов к API.
    Всегда есть **ограничение**: число попыток или время.
    """,
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        responses = [503, 502, 200]
        attempt = 0
        status = None
        while attempt < 5 and status != 200:
            status = responses[attempt]
            attempt += 1
            print(f"попытка {attempt}: {status}")
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа? Фейковые часы вместо реального ожидания.", """
        t = 0.0
        ready_at = 1.2
        polls = 0
        while t < ready_at:
            t += 0.5
            polls += 1
        print(t, polls)
        """),
    cod(f"{P}-m2-l2-e3", t("""
        Напиши функцию `retry(statuses, max_attempts)` — симуляция повторов запроса. `statuses` — статусы, которые сервер вернёт по очереди.

        - Повторяй, пока статус ≥ 500 и попытки не кончились.
        - Вернуть пару `(последний_статус, число_попыток)`.

        Примеры:
        ```
        retry([503, 502, 200], 5)   # → (200, 3)
        retry([500, 500, 500], 2)   # → (500, 2)
        retry([404], 3)             # → (404, 1)   4xx не повторяем
        ```
        """),
        """
        def retry(statuses, max_attempts):
            pass
        """,
        """
        def test_values():
            got = [retry([503, 502, 200], 5), retry([500, 500, 500], 2), retry([404], 3)]
            assert got == [(200, 3), (500, 2), (404, 1)], f"Получено {got}"
        """,
        """
        def retry(statuses, max_attempts):
            attempt = 0
            status = None
            while attempt < max_attempts and attempt < len(statuses):
                status = statuses[attempt]
                attempt += 1
                if status < 500:
                    break
            return status, attempt
        """, xp=20),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `wait_until(condition, timeout, clock, poll=0.5)` — явное ожидание.

        - `clock.now()` — текущее время в секундах, `clock.sleep(s)` — подождать.
        - Проверяй `condition()`; если истинно — вернуть `True`.
        - Если с начала прошло `timeout` секунд или больше — бросить `TimeoutError`.
        - Иначе `clock.sleep(poll)` и повторить.

        Проверка подставит «фейковые часы», которые сдвигают время мгновенно.
        """),
        """
        def wait_until(condition, timeout, clock, poll=0.5):
            pass
        """,
        """
        class FakeClock:
            def __init__(self):
                self.t = 0.0
            def now(self):
                return self.t
            def sleep(self, s):
                self.t += s

        def test_ready():
            c = FakeClock()
            assert wait_until(lambda: c.now() >= 2, 10, c) is True and c.now() < 3, "Должно вернуть True около 2-й секунды"

        def test_timeout():
            c = FakeClock()
            try:
                wait_until(lambda: False, 3, c)
            except TimeoutError:
                assert 3 <= c.now() <= 3.5, f"Сдаваться сразу после таймаута, сейчас {c.now()}"
                return
            assert False, "Нужен TimeoutError"
        """,
        """
        def wait_until(condition, timeout, clock, poll=0.5):
            start = clock.now()
            while True:
                if condition():
                    return True
                if clock.now() - start >= timeout:
                    raise TimeoutError(f"не дождались за {timeout} с")
                clock.sleep(poll)
        """, xp=25),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `backoff_schedule(max_total)` — список задержек экспоненциального отката `1, 2, 4, 8, …` секунд, пока **суммарное** время ожидания не превысит `max_total` (задержку, которая превысит лимит, не добавлять).

        Примеры:
        ```
        backoff_schedule(10)   # → [1, 2, 4]      (1+2+4 = 7, следующая 8 дала бы 15)
        backoff_schedule(15)   # → [1, 2, 4, 8]
        backoff_schedule(0)    # → []
        ```
        """),
        """
        def backoff_schedule(max_total):
            pass
        """,
        """
        def test_values():
            assert [backoff_schedule(n) for n in (10, 15, 0, 1)] == [[1, 2, 4], [1, 2, 4, 8], [], [1]], "Неверное расписание"
        """,
        """
        def backoff_schedule(max_total):
            delays = []
            delay, total = 1, 0
            while total + delay <= max_total:
                delays.append(delay)
                total += delay
                delay *= 2
            return delays
        """),
    full="""
    ## Зачем это нужно

    Это, пожалуй, самое практичное применение `while` для тестировщика. UI-тест ждёт, пока появится элемент; API-тест повторяет запрос, пока сервис не поднимется; CI ждёт готовности базы данных в контейнере. Все эти ожидания — цикл «проверь → не готово → подожди → повтори» с обязательным ограничением.

    ## Как это работает

    ### Повторы с ограничением попыток

    ```py
    attempt = 0
    while attempt < MAX:
        attempt += 1
        resp = request()
        if resp.ok:
            break
    ```

    ### Ожидание с таймаутом

    ```py
    start = time.monotonic()
    while not ready():
        if time.monotonic() - start >= timeout:
            raise TimeoutError("не дождались")
        time.sleep(poll)
    ```

    Используй `time.monotonic()` — эти часы не прыгают при переводе системного времени.

    ### Экспоненциальный откат (backoff)

    Интервал между повторами растёт: 1, 2, 4, 8 секунд. Так не «добиваем» перегруженный сервер. Часто добавляют случайный разброс (jitter), чтобы тысячи клиентов не повторяли синхронно.

    ### Что повторять

    Только временные сбои: `5xx`, `429`, таймауты. `4xx` — ошибка запроса, повтор даст то же самое.

    ## Примеры

    ### Пример 1. Повторы до успеха

    ```python
    responses = iter([503, 502, 200])
    attempt, status = 0, None
    while attempt < 5:
        attempt += 1
        status = next(responses)
        print(f"попытка {attempt}: {status}")
        if status < 500:
            break
    ```

    ### Пример 2. Ожидание на фейковых часах

    ```python
    class FakeClock:
        def __init__(self):
            self.t = 0.0
        def now(self):
            return self.t
        def sleep(self, s):
            self.t += s

    clock = FakeClock()
    element_appears_at = 1.7
    start = clock.now()
    while clock.now() < element_appears_at:
        if clock.now() - start >= 10:
            raise TimeoutError
        clock.sleep(0.5)
    print(f"элемент появился, ждали {clock.now()} с")
    ```

    ### Пример 3. Расписание отката

    ```python
    delay, total, schedule = 1, 0, []
    while total + delay <= 30:
        schedule.append(delay)
        total += delay
        delay *= 2
    print(schedule, "всего", total, "с")
    ```

    ## Частые ошибки

    **Ожидание без таймаута** — зависший тест.

    **`time.time()` для измерения интервалов** — может «прыгнуть»; нужен `time.monotonic()`.

    **Повтор на `4xx`** — бесполезная трата времени.

    ## Шпаргалка

    ```py
    while attempt < MAX: ...                  # лимит попыток
    while not ready():
        if monotonic() - start >= timeout: raise TimeoutError
        sleep(poll)
    delay *= 2                                # backoff
    ```
    """,
    quiz=[
        q("Какие ответы имеет смысл повторять?", ["Любые", "`5xx`, `429` и таймауты", "Только `404`", "Только `200`"], 1, "Это временные сбои; 4xx повторять бессмысленно."),
        q("Зачем в цикле ожидания нужен таймаут?", ["Для красоты", "Чтобы тест не завис навсегда, если событие не наступит", "Чтобы ускорить тест", "Не нужен"], 1, "Ожидание без ограничения может никогда не закончиться."),
        q("Какие часы лучше использовать для измерения интервалов?", ["`time.time()`", "`time.monotonic()`", "`datetime.now()`", "Любые"], 1, "Монотонные часы не прыгают при изменении системного времени."),
    ]),

lesson(f"{P}-m2-l3", "Очереди и стеки", """
    # Пока есть работа

    ```
    queue = ["build", "test", "deploy"]
    while queue:                 # пока не пусто
        task = queue.pop(0)      # взять первую (очередь)
        ...

    stack = ["a", "b"]
    while stack:
        item = stack.pop()       # взять последнюю (стек)
    ```

    Во время обработки можно добавлять новые задачи — цикл их тоже обработает.
    """,
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        queue = ["build", "test"]
        while queue:
            task = queue.pop(0)
            print("выполняю", task)
            if task == "build":
                queue.append("deploy")
        """, hint="Задача, добавленная во время работы, тоже будет обработана."),
    out(f"{P}-m2-l3-e2", "Что выведет программа?", """
        stack = [1, 2, 3]
        while stack:
            print(stack.pop())
        print(stack)
        """),
    cod(f"{P}-m2-l3-e3", t("""
        Напиши функцию `is_balanced(text)` — правильно ли расставлены скобки `()[]{}` в строке. Используй **стек**: открывающие кладём, на закрывающей — проверяем пару с верхушкой.

        Примеры:
        ```
        is_balanced("{[()]}")      # → True
        is_balanced("([)]")        # → False
        is_balanced("((")          # → False
        is_balanced("f(x[1])")     # → True
        ```
        """),
        """
        def is_balanced(text):
            pass
        """,
        """
        def test_values():
            got = [is_balanced(s) for s in ("{[()]}", "([)]", "((", "f(x[1])", "", ")")]
            assert got == [True, False, False, True, True, False], f"Получено {got}"
        """,
        """
        def is_balanced(text):
            pairs = {")": "(", "]": "[", "}": "{"}
            stack = []
            i = 0
            while i < len(text):
                ch = text[i]
                if ch in "([{":
                    stack.append(ch)
                elif ch in pairs:
                    if not stack or stack.pop() != pairs[ch]:
                        return False
                i += 1
            return not stack
        """, xp=25),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `run_pipeline(tasks, deps)` — выполнить задачи из очереди `tasks` по порядку. Словарь `deps` говорит, какие задачи **добавляются в конец очереди** после выполнения данной. Вернуть порядок выполнения.

        Пример:
        ```
        run_pipeline(["build"], {"build": ["unit", "lint"], "unit": ["report"]})
        # → ["build", "unit", "lint", "report"]
        ```
        """),
        """
        def run_pipeline(tasks, deps):
            pass
        """,
        """
        def test_values():
            got = run_pipeline(["build"], {"build": ["unit", "lint"], "unit": ["report"]})
            assert got == ["build", "unit", "lint", "report"], f"Получено {got}"
            assert run_pipeline([], {}) == [], "Пусто — пусто"
        """,
        """
        def run_pipeline(tasks, deps):
            queue = list(tasks)
            done = []
            while queue:
                task = queue.pop(0)
                done.append(task)
                queue.extend(deps.get(task, []))
            return done
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `undo_history(actions)` — симуляция «отмены»: `actions` — список команд; обычная команда добавляется в историю, команда `"undo"` отменяет последнюю (если есть). Вернуть итоговую историю.

        Пример:
        ```
        undo_history(["type a", "type b", "undo", "type c", "undo", "undo"])   # → []
        undo_history(["a", "b", "undo", "c"])                                  # → ["a", "c"]
        ```
        """),
        """
        def undo_history(actions):
            pass
        """,
        """
        def test_values():
            assert undo_history(["type a", "type b", "undo", "type c", "undo", "undo"]) == [], "Всё отменено"
            assert undo_history(["a", "b", "undo", "c"]) == ["a", "c"], "Неверная история"
            assert undo_history(["undo"]) == [], "Отмена пустой истории — без ошибки"
        """,
        """
        def undo_history(actions):
            history = []
            i = 0
            while i < len(actions):
                if actions[i] == "undo":
                    if history:
                        history.pop()
                else:
                    history.append(actions[i])
                i += 1
            return history
        """),
    full="""
    ## Зачем это нужно

    «Пока есть работа — делай» — естественная задача для `while`. Очередь задач CI, обход ссылок сайта краулером, отмена действий в редакторе, проверка скобок в JSON-шаблоне — всё это очереди и стеки с циклом `while список:`.

    ## Как это работает

    ### Очередь (FIFO — первым пришёл, первым ушёл)

    ```py
    while queue:
        item = queue.pop(0)     # из начала
        queue.append(new)       # новые — в конец
    ```

    На больших объёмах `pop(0)` у списка медленный; для настоящих очередей — `collections.deque` с `popleft()`.

    ### Стек (LIFO — последним пришёл, первым ушёл)

    ```py
    while stack:
        item = stack.pop()      # с конца
    ```

    ### Цикл по изменяющейся коллекции

    `while queue:` проверяет пустоту **каждую** итерацию, поэтому задачи, добавленные во время работы, тоже будут обработаны. С `for` так делать нельзя.

    ## Примеры

    ### Пример 1. Очередь с добавлением задач

    ```python
    from collections import deque
    queue = deque(["build"])
    followups = {"build": ["unit", "lint"], "unit": ["report"]}
    while queue:
        task = queue.popleft()
        print("выполняю", task)
        queue.extend(followups.get(task, []))
    ```

    ### Пример 2. Стек для скобок

    ```python
    def is_balanced(text):
        pairs = {")": "(", "]": "[", "}": "{"}
        stack = []
        for ch in text:
            if ch in "([{":
                stack.append(ch)
            elif ch in pairs:
                if not stack or stack.pop() != pairs[ch]:
                    return False
        return not stack

    for s in ['{"a": [1, (2)]}', "([)]", "(("]:
        print(s, is_balanced(s))
    ```

    ### Пример 3. Обход «ссылок» в ширину

    ```python
    links = {"/": ["/login", "/catalog"], "/catalog": ["/item/1", "/item/2"], "/login": ["/"]}
    queue, seen = ["/"], {"/"}
    while queue:
        page = queue.pop(0)
        print("проверяю", page)
        for nxt in links.get(page, []):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    ```

    Множество `seen` защищает от бесконечного хождения по кругу (`/login` → `/`).

    ## Частые ошибки

    **`for` по списку, который меняется в цикле** — пропуски и сюрпризы.

    **Обход графа без `seen`** — бесконечный цикл на циклических ссылках.

    **`pop()` на пустом списке** — `IndexError`; проверяй `while stack:`.

    ## Шпаргалка

    ```py
    while queue: item = queue.pop(0)     # очередь
    while stack: item = stack.pop()      # стек
    deque(...).popleft()                 # быстрая очередь
    seen = set()                         # защита от повторов
    ```
    """,
    quiz=[
        q("Какой элемент извлекает `stack.pop()`?", ["Первый", "Последний", "Случайный", "Минимальный"], 1, "Стек — последним пришёл, первым ушёл."),
        q("Обработает ли `while queue:` задачи, добавленные в очередь во время цикла?", ["Нет", "Да, условие проверяется на каждой итерации", "Только одну", "Ошибка"], 1, "Цикл продолжается, пока очередь не пуста."),
        q("Зачем при обходе ссылок множество `seen`?", ["Для сортировки", "Чтобы не посещать страницу повторно и не зациклиться", "Для скорости печати", "Не нужно"], 1, "Ссылки могут образовывать циклы."),
    ]),
)

# ============================================================
m3 = module(f"{P}-m3", "Алгоритмы на while", "🧠", "Двоичный поиск, последовательности и симуляции",

lesson(f"{P}-m3-l1", "Двоичный поиск", """
    # Поиск делением пополам

    В **отсортированном** списке:

    ```
    lo, hi = 0, len(xs) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if xs[mid] == target:
            return mid
        if xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
    ```

    Каждая итерация отбрасывает половину — 1 000 000 элементов за ~20 шагов.
    """,
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        xs = [1, 3, 5, 7, 9, 11]
        lo, hi, steps = 0, len(xs) - 1, 0
        target = 9
        while lo <= hi:
            steps += 1
            mid = (lo + hi) // 2
            if xs[mid] == target:
                break
            if xs[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        print(mid, steps)
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа? Сколько шагов нужно для миллиона?", """
        n, steps = 1_000_000, 0
        while n > 1:
            n //= 2
            steps += 1
        print(steps)
        """),
    cod(f"{P}-m3-l1-e3", t("""
        Напиши функцию `binary_search(xs, target)` — индекс `target` в **отсортированном** списке или `-1`. Используй `while` и деление пополам (без `in`, `index` и перебора всех элементов).

        Примеры:
        ```
        binary_search([1, 3, 5, 7, 9], 7)   # → 3
        binary_search([1, 3, 5], 4)         # → -1
        ```
        """),
        """
        def binary_search(xs, target):
            pass
        """,
        """
        def test_values():
            xs = [1, 3, 5, 7, 9, 11, 13]
            assert all(binary_search(xs, v) == i for i, v in enumerate(xs)), "Каждый элемент должен находиться"
            assert binary_search(xs, 4) == -1 and binary_search([], 1) == -1 and binary_search(xs, 100) == -1, "Отсутствующий — -1"

        def test_no_index():
            src = open("solution.py", encoding="utf-8").read()
            assert ".index(" not in src and " in xs" not in src, "Реализуй двоичный поиск сам"
        """,
        """
        def binary_search(xs, target):
            lo, hi = 0, len(xs) - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if xs[mid] == target:
                    return mid
                if xs[mid] < target:
                    lo = mid + 1
                else:
                    hi = mid - 1
            return -1
        """, xp=25),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `int_sqrt(n)` — целая часть квадратного корня неотрицательного числа **двоичным поиском** (без `** 0.5` и `math`).

        Примеры:
        ```
        int_sqrt(16)   # → 4
        int_sqrt(17)   # → 4
        int_sqrt(0)    # → 0
        int_sqrt(1_000_000)   # → 1000
        ```
        Ищи наибольшее `m`, для которого `m * m <= n`.
        """),
        """
        def int_sqrt(n):
            pass
        """,
        """
        def test_values():
            assert [int_sqrt(n) for n in (16, 17, 0, 1, 1_000_000, 99)] == [4, 4, 0, 1, 1000, 9], "Неверный корень"

        def test_no_pow():
            src = open("solution.py", encoding="utf-8").read()
            assert "**" not in src and "math" not in src, "Реши двоичным поиском"
        """,
        """
        def int_sqrt(n):
            lo, hi = 0, n
            while lo <= hi:
                mid = (lo + hi) // 2
                if mid * mid <= n:
                    lo = mid + 1
                else:
                    hi = mid - 1
            return hi
        """, xp=25),
    cod(f"{P}-m3-l1-e5", t("""
        «Поиск сломанного коммита» (как `git bisect`). Напиши функцию `first_bad(commits, is_bad)`:

        - `commits` — список коммитов по порядку; сначала идут хорошие, потом все плохие;
        - `is_bad(commit)` — функция-проверка.

        Вернуть **первый плохой** коммит (или `None`, если плохих нет), вызывая `is_bad` как можно реже — двоичным поиском.
        """),
        """
        def first_bad(commits, is_bad):
            pass
        """,
        """
        def test_values():
            commits = [f"c{i}" for i in range(100)]
            calls = []
            def is_bad(c):
                calls.append(c)
                return int(c[1:]) >= 37
            assert first_bad(commits, is_bad) == "c37", "Первый плохой — c37"
            assert len(calls) <= 8, f"Слишком много проверок: {len(calls)} (двоичный поиск уложится в 7-8)"

        def test_none():
            assert first_bad(["a", "b"], lambda c: False) is None, "Плохих нет — None"
            assert first_bad(["a", "b"], lambda c: True) == "a", "Все плохие — первый"
        """,
        """
        def first_bad(commits, is_bad):
            lo, hi = 0, len(commits) - 1
            answer = None
            while lo <= hi:
                mid = (lo + hi) // 2
                if is_bad(commits[mid]):
                    answer = commits[mid]
                    hi = mid - 1
                else:
                    lo = mid + 1
            return answer
        """, xp=25),
    full="""
    ## Зачем это нужно

    Двоичный поиск — один из самых известных алгоритмов и частый вопрос на собеседованиях. А ещё это рабочий инструмент: `git bisect` находит коммит, сломавший сборку, делением истории пополам — из 1000 коммитов нужно проверить всего ~10. Тот же подход помогает найти, на каком объёме данных начинает падать сервис.

    ## Как это работает

    Работает **только на отсортированных данных** (или на «монотонном» свойстве: сначала все хорошие, потом все плохие).

    1. Держим границы области поиска `lo` и `hi`.
    2. Смотрим на середину `mid`.
    3. По результату сравнения отбрасываем половину, где искомого точно нет.
    4. Повторяем, пока область не пуста (`lo <= hi`).

    Число шагов — логарифм: для миллиона элементов ~20, для миллиарда ~30.

    ### Поиск границы

    Вариант «найти первый элемент, удовлетворяющий условию»: при совпадении запоминаем ответ и продолжаем искать **левее** (`hi = mid - 1`).

    В стандартной библиотеке есть модуль `bisect`.

    ## Примеры

    ### Пример 1. Шаги поиска

    ```python
    xs = list(range(0, 100, 3))
    target, lo, hi, step = 57, 0, len(xs) - 1, 0
    while lo <= hi:
        step += 1
        mid = (lo + hi) // 2
        print(f"шаг {step}: lo={lo} hi={hi} mid={mid} xs[mid]={xs[mid]}")
        if xs[mid] == target:
            break
        if xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    ```

    ### Пример 2. git bisect своими руками

    ```python
    commits = [f"c{i}" for i in range(1000)]
    checks = 0
    def is_broken(commit):
        global checks
        checks += 1
        return int(commit[1:]) >= 613

    lo, hi, first = 0, len(commits) - 1, None
    while lo <= hi:
        mid = (lo + hi) // 2
        if is_broken(commits[mid]):
            first, hi = commits[mid], mid - 1
        else:
            lo = mid + 1
    print("сломал:", first, "| проверок:", checks)
    ```

    ### Пример 3. Модуль bisect

    ```python
    import bisect
    thresholds = [100, 300, 1000]           # границы времени ответа, мс
    labels = ["быстро", "нормально", "медленно", "очень медленно"]
    for ms in [50, 250, 700, 5000]:
        print(ms, labels[bisect.bisect(thresholds, ms)])
    ```

    ## Частые ошибки

    **Неотсортированные данные** — алгоритм молча вернёт неверный ответ.

    **`lo < hi` вместо `lo <= hi`** или `lo = mid` вместо `mid + 1` — пропуск элемента или вечный цикл.

    **Ожидание, что найдётся первое вхождение дубликата** — классический вариант находит любое.

    ## Шпаргалка

    ```py
    lo, hi = 0, len(xs) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if xs[mid] == t: return mid
        if xs[mid] < t: lo = mid + 1
        else: hi = mid - 1
    return -1
    ```
    """,
    quiz=[
        q("Какое главное требование двоичного поиска?", ["Список не пуст", "Данные отсортированы (или свойство монотонно)", "Элементы — числа", "Длина — степень двойки"], 1, "Иначе нельзя понять, какую половину отбросить."),
        q("Примерно сколько шагов нужно для поиска среди 1 000 000 элементов?", ["1 000 000", "1000", "20", "2"], 2, "Каждый шаг делит область пополам: log₂(10⁶) ≈ 20."),
        q("Почему нужно `lo = mid + 1`, а не `lo = mid`?", ["Так быстрее", "Иначе mid может повторяться и цикл зависнет", "Это требование синтаксиса", "Без разницы"], 1, "Середина уже проверена; не исключив её, можно застрять."),
    ]),

lesson(f"{P}-m3-l2", "Последовательности", """
    # Генерация до предела

    ```
    a, b = 0, 1
    while a <= limit:
        print(a)
        a, b = b, a + b      # Фибоначчи
    ```

    Когда неизвестно, сколько членов последовательности получится, — `while` с условием на значение.
    """,
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        a, b = 0, 1
        result = []
        while a <= 20:
            result.append(a)
            a, b = b, a + b
        print(result)
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа?", """
        n = 7
        path = [n]
        while n != 1:
            n = n // 2 if n % 2 == 0 else 3 * n + 1
            path.append(n)
        print(len(path) - 1, max(path))
        """),
    cod(f"{P}-m3-l2-e3", t("""
        Напиши функцию `fib_until(limit)` — список чисел Фибоначчи (0, 1, 1, 2, 3, 5, …), не превышающих `limit`.

        Примеры:
        ```
        fib_until(10)   # → [0, 1, 1, 2, 3, 5, 8]
        fib_until(0)    # → [0]
        ```
        """),
        """
        def fib_until(limit):
            pass
        """,
        """
        def test_values():
            assert fib_until(10) == [0, 1, 1, 2, 3, 5, 8] and fib_until(0) == [0] and fib_until(1) == [0, 1, 1], "Неверная последовательность"
        """,
        """
        def fib_until(limit):
            a, b = 0, 1
            result = []
            while a <= limit:
                result.append(a)
                a, b = b, a + b
            return result
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши функцию `gcd(a, b)` — наибольший общий делитель по **алгоритму Евклида**: пока `b` не ноль, заменяй `(a, b)` на `(b, a % b)`; ответ — `a`.

        Примеры:
        ```
        gcd(48, 18)   # → 6
        gcd(17, 5)    # → 1
        gcd(0, 7)     # → 7
        ```
        Без `math.gcd`.
        """),
        """
        def gcd(a, b):
            pass
        """,
        """
        def test_values():
            assert [gcd(48, 18), gcd(17, 5), gcd(0, 7), gcd(100, 75)] == [6, 1, 7, 25], "Неверный НОД"

        def test_no_math():
            assert "math" not in open("solution.py", encoding="utf-8").read(), "Реализуй алгоритм Евклида сам"
        """,
        """
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `primes_until(limit)` — список простых чисел не больше `limit`. Используй `while` для перебора кандидатов и проверку делителей до корня из числа (`d * d <= n`).

        Примеры:
        ```
        primes_until(20)   # → [2, 3, 5, 7, 11, 13, 17, 19]
        primes_until(1)    # → []
        ```
        """),
        """
        def primes_until(limit):
            pass
        """,
        """
        def test_values():
            assert primes_until(20) == [2, 3, 5, 7, 11, 13, 17, 19] and primes_until(1) == [] and primes_until(2) == [2], "Неверный список"
            assert len(primes_until(1000)) == 168, "До 1000 ровно 168 простых"
        """,
        """
        def primes_until(limit):
            primes = []
            n = 2
            while n <= limit:
                d = 2
                is_prime = True
                while d * d <= n:
                    if n % d == 0:
                        is_prime = False
                        break
                    d += 1
                if is_prime:
                    primes.append(n)
                n += 1
            return primes
        """, xp=20),
    full="""
    ## Зачем это нужно

    Многие задачи — «генерировать значения, пока не выполнится условие»: числа Фибоначчи до предела, простые числа, шаги алгоритма до сходимости. Число итераций заранее неизвестно, поэтому это работа для `while`. Такие задачи часто встречаются на собеседованиях и тренируют аккуратность с условиями.

    ## Как это работает

    Общая форма:

    ```py
    текущее = начальное
    while не_достигли_предела(текущее):
        использовать(текущее)
        текущее = следующее(текущее)
    ```

    ### Параллельное присваивание

    `a, b = b, a + b` — правая часть вычисляется целиком **до** присваивания. Без этого пришлось бы заводить временную переменную.

    ### Алгоритм Евклида

    НОД(a, b) = НОД(b, a % b), пока `b` не станет нулём. Один из древнейших алгоритмов — и прекрасный пример цикла, который гарантированно сходится.

    ### Проверка простоты до корня

    Если у `n` есть делитель больше `√n`, то есть и парный меньше `√n`. Поэтому проверять достаточно `d * d <= n` — это в разы быстрее.

    ## Примеры

    ### Пример 1. Фибоначчи до предела

    ```python
    a, b = 0, 1
    while a < 200:
        print(a, end=" ")
        a, b = b, a + b
    print()
    ```

    ### Пример 2. Евклид по шагам

    ```python
    a, b = 1071, 462
    while b:
        print(f"НОД({a}, {b})")
        a, b = b, a % b
    print("ответ:", a)
    ```

    ### Пример 3. Простые числа

    ```python
    def is_prime(n):
        if n < 2:
            return False
        d = 2
        while d * d <= n:
            if n % d == 0:
                return False
            d += 1
        return True

    print([n for n in range(50) if is_prime(n)])
    ```

    ### Пример 4. Сходимость — корень методом Ньютона

    ```python
    x, target, steps = 1.0, 2.0, 0
    while abs(x * x - target) > 1e-12:
        x = (x + target / x) / 2
        steps += 1
    print(x, "за", steps, "шагов")
    ```

    ## Частые ошибки

    **Последовательное присваивание** `a = b; b = a + b` — `b` посчитается уже от нового `a`.

    **Сравнение float на точное равенство** в условии сходимости — используй допуск (`abs(...) > eps`).

    **Проверка делителей до `n`** — работает, но очень медленно на больших числах.

    ## Шпаргалка

    ```py
    a, b = b, a + b              # Фибоначчи
    while b: a, b = b, a % b     # Евклид
    while d * d <= n: ...        # делители до корня
    while abs(err) > 1e-9: ...   # сходимость с допуском
    ```
    """,
    quiz=[
        q("Что будет в `a, b` после `a, b = 1, 1` и затем `a, b = b, a + b` два раза?", ["`(2, 3)`", "`(1, 2)`", "`(3, 5)`", "`(2, 2)`"], 0, "(1,1) → (1,2) → (2,3)."),
        q("Почему делители числа достаточно проверять до √n?", ["Так принято", "Если есть делитель больше √n, есть и парный меньше √n", "Больших делителей не бывает", "Из-за ограничений Python"], 1, "Делители идут парами d и n/d."),
        q("Чему равно НОД(48, 18) по Евклиду?", ["`2`", "`3`", "`6`", "`18`"], 2, "48 % 18 = 12, 18 % 12 = 6, 12 % 6 = 0 → 6."),
    ]),

lesson(f"{P}-m3-l3", "Симуляции", """
    # Цикл «шаг мира»

    ```
    while not game_over:
        прочитать действие
        обновить состояние
        проверить условия окончания
    ```

    Так устроены игры, симуляторы, конечные автоматы и прогон сценариев в тестах.
    """,
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        position, target, moves = 0, 10, 0
        steps = [3, 4, 5]
        i = 0
        while position < target:
            position += steps[i % len(steps)]
            i += 1
            moves += 1
        print(position, moves)
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа? Простой конечный автомат.", """
        state = "idle"
        events = ["start", "pause", "start", "stop"]
        transitions = {("idle", "start"): "running", ("running", "pause"): "paused",
                       ("paused", "start"): "running", ("running", "stop"): "stopped"}
        i = 0
        while state != "stopped" and i < len(events):
            state = transitions.get((state, events[i]), state)
            print(events[i], "->", state)
            i += 1
        """),
    cod(f"{P}-m3-l3-e3", t("""
        Напиши функцию `bank_account(operations)` — симуляция счёта. `operations` — список строк `"deposit N"`, `"withdraw N"` или `"close"`.

        - Обрабатывай операции по очереди циклом `while`.
        - `withdraw` больше баланса — пропустить (баланс не меняется).
        - `close` — прекратить обработку (остальные операции игнорировать).
        - Вернуть итоговый баланс.

        Пример:
        ```
        bank_account(["deposit 100", "withdraw 30", "withdraw 500", "close", "deposit 1000"])   # → 70
        ```
        """),
        """
        def bank_account(operations):
            pass
        """,
        """
        def test_values():
            assert bank_account(["deposit 100", "withdraw 30", "withdraw 500", "close", "deposit 1000"]) == 70, "Неверный баланс"
            assert bank_account([]) == 0 and bank_account(["deposit 5", "deposit 5"]) == 10, "Неверный баланс"
        """,
        """
        def bank_account(operations):
            balance = 0
            i = 0
            while i < len(operations):
                parts = operations[i].split()
                i += 1
                if parts[0] == "close":
                    break
                amount = int(parts[1])
                if parts[0] == "deposit":
                    balance += amount
                elif parts[0] == "withdraw" and amount <= balance:
                    balance -= amount
            return balance
        """, xp=20),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `traffic_light(ticks)` — симуляция светофора на `ticks` тактов. Цикл состояний: `"green"` длится 3 такта, `"yellow"` — 1, `"red"` — 2, затем снова `"green"`.

        Вернуть список состояний по тактам.

        Пример:
        ```
        traffic_light(8)
        # → ["green", "green", "green", "yellow", "red", "red", "green", "green"]
        ```
        """),
        """
        def traffic_light(ticks):
            pass
        """,
        """
        def test_values():
            assert traffic_light(8) == ["green", "green", "green", "yellow", "red", "red", "green", "green"], f"Получено {traffic_light(8)}"
            assert traffic_light(0) == [], "0 тактов — пусто"
        """,
        """
        def traffic_light(ticks):
            cycle = [("green", 3), ("yellow", 1), ("red", 2)]
            result = []
            phase = 0
            while len(result) < ticks:
                color, duration = cycle[phase % len(cycle)]
                left = duration
                while left > 0 and len(result) < ticks:
                    result.append(color)
                    left -= 1
                phase += 1
            return result
        """, xp=20),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `robot(commands)` — робот стартует в точке `(0, 0)` и выполняет команды по очереди:

        - `"U"`, `"D"`, `"L"`, `"R"` — шаг вверх (y+1), вниз (y-1), влево (x-1), вправо (x+1);
        - если робот возвращается в `(0, 0)` **после хотя бы одного шага** — он останавливается, оставшиеся команды не выполняются.

        Вернуть пару `(x, y)` — итоговую позицию и число выполненных команд: `((x, y), steps)`.

        Примеры:
        ```
        robot("UURR")    # → ((2, 2), 4)
        robot("URDLUU")  # → ((0, 0), 4)
        ```
        """),
        """
        def robot(commands):
            pass
        """,
        """
        def test_values():
            assert robot("UURR") == ((2, 2), 4), f"Получено {robot('UURR')}"
            assert robot("URDLUU") == ((0, 0), 4), f"Получено {robot('URDLUU')}"
            assert robot("") == ((0, 0), 0), "Нет команд"
        """,
        """
        def robot(commands):
            moves = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
            x = y = steps = 0
            while steps < len(commands):
                dx, dy = moves[commands[steps]]
                x, y = x + dx, y + dy
                steps += 1
                if (x, y) == (0, 0):
                    break
            return (x, y), steps
        """),
    full="""
    ## Зачем это нужно

    Симуляция — это цикл, который шаг за шагом обновляет состояние мира: игра, светофор, банковский счёт, конечный автомат заказа (создан → оплачен → доставлен). В тестировании такие модели используют, чтобы прогнать сценарии и проверить переходы состояний: можно ли оплатить отменённый заказ? что будет при двойной отмене?

    ## Как это работает

    ```py
    состояние = начальное
    while не_конец(состояние):
        событие = следующее_событие()
        состояние = перейти(состояние, событие)
    ```

    ### Конечный автомат

    Состояния + таблица переходов `(состояние, событие) → новое_состояние`. Неизвестный переход — либо игнор (состояние не меняется), либо ошибка. Удобно хранить таблицу в словаре.

    Автоматы — основа **тестирования переходов состояний**: по таблице видно, какие переходы допустимы, а какие нужно проверить как негативные.

    ### Условия окончания

    - достигли цели (позиция, баланс);
    - событие «стоп»;
    - кончились события;
    - предохранитель — максимум шагов.

    ## Примеры

    ### Пример 1. Автомат заказа

    ```python
    transitions = {
        ("created", "pay"): "paid",
        ("created", "cancel"): "cancelled",
        ("paid", "ship"): "shipped",
        ("shipped", "deliver"): "delivered",
    }
    state = "created"
    for event in ["pay", "cancel", "ship", "deliver"]:
        new = transitions.get((state, event))
        if new is None:
            print(f"❌ {event} недопустим в состоянии {state}")
            continue
        state = new
        print(f"✅ {event} -> {state}")
    ```

    ### Пример 2. Игровой цикл

    ```python
    import random
    random.seed(1)
    hp_hero, hp_boss, turn = 30, 40, 0
    while hp_hero > 0 and hp_boss > 0 and turn < 50:
        turn += 1
        hp_boss -= random.randint(3, 8)
        if hp_boss > 0:
            hp_hero -= random.randint(2, 6)
    print(f"ход {turn}: герой {hp_hero}, босс {hp_boss}")
    ```

    ### Пример 3. Робот на плоскости

    ```python
    moves = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
    x = y = 0
    visited = {(0, 0)}
    for cmd in "URRDLLU":
        dx, dy = moves[cmd]
        x, y = x + dx, y + dy
        if (x, y) in visited:
            print("снова в", (x, y))
        visited.add((x, y))
    print("итог:", (x, y))
    ```

    ## Частые ошибки

    **Нет условия окончания или предохранителя** — вечный цикл.

    **Состояние меняется в нескольких местах** — трудно отлаживать; держи переходы в одной таблице.

    **Недопустимые переходы молча игнорируются** там, где нужна ошибка.

    ## Шпаргалка

    ```py
    state = "idle"
    while state != "done" and steps < MAX:
        state = transitions.get((state, event), state)
    ```
    """,
    quiz=[
        q("Что такое конечный автомат?", ["Цикл for", "Набор состояний и правил переходов между ними по событиям", "Функция без return", "Тип данных"], 1, "Состояние меняется только по разрешённым переходам."),
        q("Почему в симуляции нужен предохранитель (максимум шагов)?", ["Для красоты", "Чтобы гарантировать завершение, даже если условие окончания не наступит", "Так быстрее", "Не нужен"], 1, "Ошибка в правилах не должна вешать программу."),
        q("Как в тестах используют таблицу переходов состояний?", ["Никак", "Проверяют и допустимые переходы, и недопустимые как негативные сценарии", "Только для документации", "Для генерации паролей"], 1, "Недопустимые переходы — важный источник негативных тест-кейсов."),
    ]),
)

TOPIC = topic("py-while", "Цикл while", "🔄", "#2b70c9",
              "while, счётчики, while True, повторы с ожиданием, очереди и алгоритмы",
              m1, m2, m3, group="Python")
