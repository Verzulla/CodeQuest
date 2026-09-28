"""Тема «Цикл while», модуль 1 «Основы while» — задания. Теория — в _whl_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "whl"

m1 = module(f"{P}-m1", "Основы while", "🔄", "Условие, while или for, счётчики, while True, continue/else, ввод данных",

lesson(f"{P}-m1-l1", "while и условие",
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
    out(f"{P}-m1-l1-e6", "Что выведет программа? Когда проверяется условие?", """
        n = 0
        while n < 3:
            n += 1
            print("внутри", n)
        print("после", n)
        """, hint="Условие проверяется только перед каждым шагом, а не после каждой строки."),
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
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `count_down_by(start, step)` — список чисел от `start` вниз с шагом `step`, пока числа **больше нуля**. Используй `while`.

        Примеры:
        ```
        count_down_by(10, 3)   # → [10, 7, 4, 1]
        count_down_by(6, 2)    # → [6, 4, 2]
        count_down_by(0, 1)    # → []
        ```
        """),
        """
        def count_down_by(start, step):
            pass
        """,
        """
        def test_values():
            got = [count_down_by(10, 3), count_down_by(6, 2), count_down_by(0, 1), count_down_by(1, 5)]
            assert got == [[10, 7, 4, 1], [6, 4, 2], [], [1]], f"Получено {got}"

        def test_while():
            assert "while " in open("solution.py", encoding="utf-8").read(), "Используй while"
        """,
        """
        def count_down_by(start, step):
            result = []
            n = start
            while n > 0:
                result.append(n)
                n -= step
            return result
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `first_multiple_over(k, limit)` — наименьшее число, кратное `k`, которое **строго больше** `limit`. Перебирай кратные `k, 2k, 3k, …` циклом `while`.

        Примеры:
        ```
        first_multiple_over(7, 20)   # → 21
        first_multiple_over(5, 5)    # → 10
        first_multiple_over(3, 0)    # → 3
        ```
        """),
        """
        def first_multiple_over(k, limit):
            pass
        """,
        """
        def test_values():
            got = [first_multiple_over(7, 20), first_multiple_over(5, 5), first_multiple_over(3, 0), first_multiple_over(10, 99)]
            assert got == [21, 10, 3, 100], f"Получено {got}"

        def test_while():
            assert "while " in open("solution.py", encoding="utf-8").read(), "Используй while"
        """,
        """
        def first_multiple_over(k, limit):
            m = k
            while m <= limit:
                m += k
            return m
        """, hint="Начни с k и прибавляй k, пока число не больше limit."),
),

lesson(f"{P}-vs-for", "while или for",
    out(f"{P}-vs-for-e1", "Что выведет программа? Перебор списка через while.", """
        items = ["a", "b", "c"]
        i = 0
        while i < len(items):
            print(i, items[i])
            i += 1
        """),
    out(f"{P}-vs-for-e2", "Что выведет программа? «Пока список не пуст».", """
        todo = ["код", "тесты", "деплой"]
        while todo:
            task = todo.pop()
            print("делаю", task)
        print(todo, bool(todo))
        """, hint="Непустой список — истина, пустой — ложь. pop() берёт с конца."),
    out(f"{P}-vs-for-e3", "Что выведет программа? Заранее неизвестно, сколько шагов.", """
        total, n = 0, 0
        while total <= 10:
            n += 1
            total += n
        print(n, total)
        """),
    cod(f"{P}-vs-for-e4", t("""
        Напиши функцию `sum_list_while(nums)` — сумма чисел списка через `while` с индексом. Без `for` и без `sum`.

        Примеры:
        ```
        sum_list_while([3, 4, 5])   # → 12
        sum_list_while([])          # → 0
        ```
        """),
        """
        def sum_list_while(nums):
            pass
        """,
        """
        def test_values():
            assert sum_list_while([3, 4, 5]) == 12 and sum_list_while([]) == 0 and sum_list_while([-1]) == -1, "Неверная сумма"

        def test_while():
            src = open("solution.py", encoding="utf-8").read()
            assert "while " in src and "for " not in src and "sum(" not in src.replace("sum_list_while(", ""), "Используй while, без for и sum"
        """,
        """
        def sum_list_while(nums):
            total = 0
            i = 0
            while i < len(nums):
                total += nums[i]
                i += 1
            return total
        """),
    cod(f"{P}-vs-for-e5", t("""
        Напиши функцию `how_many_to_reach(nums, target)` — сколько **первых** элементов списка нужно сложить, чтобы сумма стала `>= target`. Если даже всех не хватает — `-1`. Для `target <= 0` — `0`.

        Примеры:
        ```
        how_many_to_reach([5, 3, 8, 1], 10)   # → 3   (5 + 3 + 8 = 16)
        how_many_to_reach([1, 1], 5)          # → -1
        ```
        """),
        """
        def how_many_to_reach(nums, target):
            pass
        """,
        """
        def test_values():
            got = [how_many_to_reach([5, 3, 8, 1], 10), how_many_to_reach([1, 1], 5), how_many_to_reach([4], 0), how_many_to_reach([2, 3], 5)]
            assert got == [3, -1, 0, 2], f"Получено {got}"
        """,
        """
        def how_many_to_reach(nums, target):
            total = 0
            i = 0
            while total < target and i < len(nums):
                total += nums[i]
                i += 1
            if total >= target:
                return i
            return -1
        """, hint="Два условия продолжения: сумма ещё мала И элементы не кончились.", xp=20),
    cod(f"{P}-vs-for-e6", t("""
        Напиши функцию `first_index_while(items, value)` — индекс первого вхождения `value` или `-1`. Используй `while` с **составным условием**: `while i < len(items) and items[i] != value:`. Без `for` и `index`.

        Примеры:
        ```
        first_index_while(["a", "b", "c"], "b")   # → 1
        first_index_while([1, 2], 9)              # → -1
        ```
        """),
        """
        def first_index_while(items, value):
            pass
        """,
        """
        def test_values():
            got = [first_index_while(["a", "b", "c"], "b"), first_index_while([1, 2], 9), first_index_while([], 1), first_index_while([5, 5], 5)]
            assert got == [1, -1, -1, 0], f"Получено {got}"

        def test_while():
            src = open("solution.py", encoding="utf-8").read()
            assert "while " in src and "for " not in src and ".index(" not in src, "Используй while, без for и index"
        """,
        """
        def first_index_while(items, value):
            i = 0
            while i < len(items) and items[i] != value:
                i += 1
            if i < len(items):
                return i
            return -1
        """, hint="Порядок в and важен: сначала i < len(items), иначе items[i] даст IndexError."),
    cod(f"{P}-vs-for-e7", t("""
        Напиши функцию `drain(stack)` — снимать элементы с конца списка (`pop()`), пока он не опустеет, и вернуть их в порядке снятия. Исходный список после вызова должен стать пустым.

        Пример:
        ```
        s = [1, 2, 3]
        drain(s)   # → [3, 2, 1]
        s          # → []
        ```
        """),
        """
        def drain(stack):
            pass
        """,
        """
        def test_values():
            s = [1, 2, 3]
            assert drain(s) == [3, 2, 1] and s == [], "Неверный результат или список не опустел"
            assert drain([]) == [], "Пустой — пусто"

        def test_while():
            assert "while " in open("solution.py", encoding="utf-8").read(), "Используй while"
        """,
        """
        def drain(stack):
            result = []
            while stack:
                result.append(stack.pop())
            return result
        """),
    cod(f"{P}-vs-for-e8", t("""
        Напиши функцию `chunks(items, size)` — разбить список на куски по `size` элементов (последний может быть короче). Используй `while` и срезы.

        Пример:
        ```
        chunks([1, 2, 3, 4, 5], 2)   # → [[1, 2], [3, 4], [5]]
        ```
        """),
        """
        def chunks(items, size):
            pass
        """,
        """
        def test_values():
            got = [chunks([1, 2, 3, 4, 5], 2), chunks([1, 2], 5), chunks([], 3), chunks([1, 2, 3], 1)]
            assert got == [[[1, 2], [3, 4], [5]], [[1, 2]], [], [[1], [2], [3]]], f"Получено {got}"
        """,
        """
        def chunks(items, size):
            result = []
            i = 0
            while i < len(items):
                result.append(items[i:i + size])
                i += size
            return result
        """, hint="Срез items[i:i + size], затем сдвиг i += size."),
),

lesson(f"{P}-m1-l2", "Счётчики и бесконечные циклы",
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
    out(f"{P}-m1-l2-e6", "Что выведет программа? Условие != и «перепрыгивание».", """
        n = 0
        while n != 10:
            n += 3
            if n > 20:
                print("проскочили!")
                break
        print(n)
        """, hint="0 → 3 → 6 → 9 → 12 … ровно 10 не получится никогда."),
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
    cod(f"{P}-m1-l2-e7", t("""
        В функции `count_vowels(text)` баг: на некоторых строках она зависает. Найди и исправь — функция должна считать гласные `aeiou` в строке.

        Примеры:
        ```
        count_vowels("hello")   # → 2
        count_vowels("xyz")     # → 0
        ```
        """),
        """
        def count_vowels(text):
            count = 0
            i = 0
            while i < len(text):
                if text[i] in "aeiou":
                    count += 1
                    i += 1
            return count
        """,
        """
        def test_values():
            assert [count_vowels(s) for s in ("hello", "xyz", "", "aaa")] == [2, 0, 0, 3], "Неверный подсчёт"
        """,
        """
        def count_vowels(text):
            count = 0
            i = 0
            while i < len(text):
                if text[i] in "aeiou":
                    count += 1
                i += 1
            return count
        """, hint="i увеличивается только для гласных. На согласной индекс застревает навсегда."),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши функцию `collatz_limited(n, max_steps)` — число шагов Коллатца до 1 (как в `collatz_steps`), но со **страховкой**: если шагов стало больше `max_steps`, остановиться и вернуть `-1`.

        Примеры:
        ```
        collatz_limited(6, 50)    # → 8
        collatz_limited(27, 50)   # → -1   (нужно 111 шагов)
        collatz_limited(1, 0)     # → 0
        ```
        """),
        """
        def collatz_limited(n, max_steps):
            pass
        """,
        """
        def test_values():
            got = [collatz_limited(6, 50), collatz_limited(27, 50), collatz_limited(1, 0), collatz_limited(27, 111), collatz_limited(27, 110)]
            assert got == [8, -1, 0, 111, -1], f"Получено {got}"
        """,
        """
        def collatz_limited(n, max_steps):
            steps = 0
            while n != 1:
                if steps >= max_steps:
                    return -1
                n = n // 2 if n % 2 == 0 else 3 * n + 1
                steps += 1
            return steps
        """, hint="Перед каждым шагом проверь: не исчерпан ли лимит.", xp=20),
),

lesson(f"{P}-m1-l3", "while True и break",
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
    out(f"{P}-m1-l3-e6", "Что выведет программа? Проверка в конце тела.", """
        n = 100
        while True:
            n //= 3
            print(n)
            if n < 5:
                break
        """, hint="Тело выполняется хотя бы раз — проверка стоит в конце."),
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
    cod(f"{P}-m1-l3-e7", t("""
        Напиши функцию `guess_number(secret, guesses)` — игра «угадай число». Перебирай догадки по очереди через `while True` и собирай ответы:

        - догадка меньше `secret` → `"больше"`;
        - больше → `"меньше"`;
        - равна → `"угадал"` и игра заканчивается.

        Если догадки кончились — вернуть собранное.

        Пример:
        ```
        guess_number(7, [5, 9, 7, 1])   # → ["больше", "меньше", "угадал"]
        guess_number(3, [1])            # → ["больше"]
        ```
        """),
        """
        def guess_number(secret, guesses):
            pass
        """,
        """
        def test_values():
            got = [guess_number(7, [5, 9, 7, 1]), guess_number(3, [1]), guess_number(2, []), guess_number(4, [4, 4])]
            assert got == [["больше", "меньше", "угадал"], ["больше"], [], ["угадал"]], f"Получено {got}"

        def test_while_true():
            assert "while True" in open("solution.py", encoding="utf-8").read(), "Используй while True"
        """,
        """
        def guess_number(secret, guesses):
            answers = []
            i = 0
            while True:
                if i >= len(guesses):
                    break
                g = guesses[i]
                i += 1
                if g < secret:
                    answers.append("больше")
                elif g > secret:
                    answers.append("меньше")
                else:
                    answers.append("угадал")
                    break
            return answers
        """, xp=20),
    cod(f"{P}-m1-l3-e8", t("""
        Напиши функцию `menu(commands)` — простой командный интерпретатор на `while True`:

        - `"add N"` — прибавить число N к итогу (итог сначала 0);
        - `"show"` — добавить текущий итог в список вывода;
        - `"exit"` — завершить работу;
        - любая другая команда — добавить в вывод `"?"`.

        Работа заканчивается и когда команды кончились. Вернуть список вывода.

        Пример:
        ```
        menu(["add 5", "show", "add 2", "hello", "show", "exit", "show"])   # → [5, "?", 7]
        ```
        """),
        """
        def menu(commands):
            pass
        """,
        """
        def test_values():
            got = menu(["add 5", "show", "add 2", "hello", "show", "exit", "show"])
            assert got == [5, "?", 7], f"Получено {got}"
            assert menu([]) == [] and menu(["show"]) == [0], "Неверный результат"
        """,
        """
        def menu(commands):
            total = 0
            output = []
            i = 0
            while True:
                if i >= len(commands):
                    break
                cmd = commands[i]
                i += 1
                if cmd == "exit":
                    break
                if cmd == "show":
                    output.append(total)
                elif cmd.startswith("add "):
                    total += int(cmd.split()[1])
                else:
                    output.append("?")
            return output
        """, hint="cmd.split()[1] — число после add; int(...) превращает его в число.", xp=20),
),

lesson(f"{P}-ctrl", "continue, else и флаги в while",
    out(f"{P}-ctrl-e1", "Что выведет программа?", """
        i = 0
        while i < 6:
            i += 1
            if i % 2 == 0:
                continue
            print(i)
        """, hint="Счётчик увеличивается ДО continue — поэтому цикл не зависает."),
    out(f"{P}-ctrl-e2", "Что выведет программа? else у while.", """
        n = 3
        while n > 0:
            n -= 1
        else:
            print("условие стало ложным, n =", n)
        k = 0
        while k < 10:
            k += 1
            if k == 4:
                break
        else:
            print("не напечатается")
        print("k =", k)
        """),
    out(f"{P}-ctrl-e3", "Что выведет программа? Цикл с флагом.", """
        running = True
        fuel, distance = 3, 0
        while running:
            fuel -= 1
            distance += 10
            if fuel == 0:
                running = False
        print(distance, fuel)
        """),
    cod(f"{P}-ctrl-e4", t("""
        Функция `sum_odd_until(n)` должна вернуть сумму нечётных чисел **меньше** `n`, но зависает. Исправь её, сохранив `continue`.

        Примеры:
        ```
        sum_odd_until(6)   # → 9   (1 + 3 + 5)
        sum_odd_until(1)   # → 0
        ```
        """),
        """
        def sum_odd_until(n):
            total = 0
            i = 0
            while i < n:
                if i % 2 == 0:
                    continue
                total += i
                i += 1
            return total
        """,
        """
        def test_values():
            assert [sum_odd_until(n) for n in (6, 1, 0, 10)] == [9, 0, 0, 25], "Неверная сумма"

        def test_continue():
            assert "continue" in open("solution.py", encoding="utf-8").read(), "Оставь continue"
        """,
        """
        def sum_odd_until(n):
            total = 0
            i = 0
            while i < n:
                if i % 2 == 0:
                    i += 1
                    continue
                total += i
                i += 1
            return total
        """, hint="continue перескакивает i += 1 в конце тела. Увеличь счётчик и перед continue."),
    cod(f"{P}-ctrl-e5", t("""
        Напиши функцию `find_divisor(n)` — наименьший делитель числа `n >= 2`, больший 1. Перебирай `d` от 2, пока `d * d <= n`. Если делитель не найден — число простое, верни само `n`. Используй `while … else`.

        Примеры:
        ```
        find_divisor(15)   # → 3
        find_divisor(13)   # → 13
        find_divisor(49)   # → 7
        ```
        """),
        """
        def find_divisor(n):
            pass
        """,
        """
        def test_values():
            assert [find_divisor(n) for n in (15, 13, 49, 2, 4, 97)] == [3, 13, 7, 2, 2, 97], "Неверный делитель"

        def test_while_else():
            src = open("solution.py", encoding="utf-8").read()
            assert "while " in src and "else:" in src and "break" in src, "Используй while … else с break"
        """,
        """
        def find_divisor(n):
            d = 2
            while d * d <= n:
                if n % d == 0:
                    result = d
                    break
                d += 1
            else:
                result = n
            return result
        """, hint="Если у n есть делитель, то есть и делитель не больше корня из n — поэтому d * d <= n.", xp=20),
    cod(f"{P}-ctrl-e6", t("""
        Напиши функцию `process_orders(orders)` — обработать суммы заказов по очереди, пока всё хорошо. Используй флаг `ok = True` в условии цикла:

        - положительная сумма — прибавить к итогу;
        - отрицательная — это ошибка: поставить `ok = False` и больше ничего не обрабатывать.

        Вернуть пару `(итог, ok)`.

        Примеры:
        ```
        process_orders([10, 20, -5, 7])   # → (30, False)
        process_orders([1, 2])            # → (3, True)
        ```
        """),
        """
        def process_orders(orders):
            pass
        """,
        """
        def test_values():
            got = [process_orders([10, 20, -5, 7]), process_orders([1, 2]), process_orders([]), process_orders([-1])]
            assert got == [(30, False), (3, True), (0, True), (0, False)], f"Получено {got}"
        """,
        """
        def process_orders(orders):
            total = 0
            ok = True
            i = 0
            while ok and i < len(orders):
                if orders[i] < 0:
                    ok = False
                else:
                    total += orders[i]
                i += 1
            return total, ok
        """),
    cod(f"{P}-ctrl-e7", t("""
        Напиши функцию `skip_comments(lines)` — через `while` и `continue` собрать строки, которые **не пустые** (после `strip()`) и **не начинаются** с `#`. Вернуть их очищенными от пробелов.

        Пример:
        ```
        skip_comments(["# conf", "  a=1 ", "", "#x", "b=2"])   # → ["a=1", "b=2"]
        ```
        """),
        """
        def skip_comments(lines):
            pass
        """,
        """
        def test_values():
            assert skip_comments(["# conf", "  a=1 ", "", "#x", "b=2"]) == ["a=1", "b=2"] and skip_comments([]) == [], "Неверный результат"

        def test_while_continue():
            src = open("solution.py", encoding="utf-8").read()
            assert "while " in src and "continue" in src, "Используй while и continue"
        """,
        """
        def skip_comments(lines):
            result = []
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                i += 1
                if not line or line.startswith("#"):
                    continue
                result.append(line)
            return result
        """, hint="Увеличь i сразу после чтения строки — до любого continue."),
    cod(f"{P}-ctrl-e8", t("""
        Напиши функцию `first_stable(values)` — индекс первого места, где значение **не изменилось**: `values[i] == values[i + 1]`. Если такого нет — `-1`. Используй `while` с составным условием.

        Примеры:
        ```
        first_stable([1, 3, 3, 5])   # → 1
        first_stable([1, 2, 3])      # → -1
        ```
        """),
        """
        def first_stable(values):
            pass
        """,
        """
        def test_values():
            got = [first_stable([1, 3, 3, 5]), first_stable([1, 2, 3]), first_stable([]), first_stable([4, 4])]
            assert got == [1, -1, -1, 0], f"Получено {got}"
        """,
        """
        def first_stable(values):
            i = 0
            while i < len(values) - 1 and values[i] != values[i + 1]:
                i += 1
            if i < len(values) - 1:
                return i
            return -1
        """),
),

lesson(f"{P}-input", "Ввод и проверка данных",
    out(f"{P}-input-e1", "Что выведет программа? Ответы пользователя заменены списком.", """
        answers = ["abc", "-5", "42"]
        i = 0
        while True:
            text = answers[i]
            i += 1
            if not text.lstrip("-").isdigit():
                print("не число:", text)
                continue
            n = int(text)
            if n < 0:
                print("отрицательное:", n)
                continue
            break
        print("принято", n, "с попытки", i)
        """),
    out(f"{P}-input-e2", "Что выведет программа?", """
        inputs = ["ок", "может", "нет"]
        answer = ""
        while answer not in ("да", "нет"):
            answer = inputs.pop(0)
            print("ввели:", answer)
        """),
    out(f"{P}-input-e3", "Что выведет программа? try/except внутри цикла.", """
        raw = ["x", "7.5", "8"]
        while raw:
            text = raw.pop(0)
            try:
                value = int(text)
                break
            except ValueError:
                print("повторите ввод:", text)
        print(value)
        """, hint='int("7.5") тоже ValueError — это не целое число.'),
    cod(f"{P}-input-e4", t("""
        Напиши функцию `ask_int(inputs)` — «спрашивать» пользователя, пока он не введёт целое число. Ответы — строки из списка `inputs` по порядку. Вернуть первое, которое `int()` смог разобрать; если ответы кончились — `None`.

        Используй `while` и `try/except ValueError`.

        Примеры:
        ```
        ask_int(["abc", "", "12"])   # → 12
        ask_int([" 7 "])             # → 7    (int терпит пробелы по краям)
        ask_int(["x"])               # → None
        ```
        """),
        """
        def ask_int(inputs):
            pass
        """,
        """
        def test_values():
            got = [ask_int(["abc", "", "12"]), ask_int([" 7 "]), ask_int(["x"]), ask_int([]), ask_int(["-3", "5"])]
            assert got == [12, 7, None, None, -3], f"Получено {got}"

        def test_try():
            src = open("solution.py", encoding="utf-8").read()
            assert "while " in src and "except" in src, "Используй while и try/except"
        """,
        """
        def ask_int(inputs):
            i = 0
            while i < len(inputs):
                text = inputs[i]
                i += 1
                try:
                    return int(text)
                except ValueError:
                    pass
            return None
        """, hint="try: return int(text) — если строка не число, будет ValueError, и цикл пойдёт дальше."),
    cod(f"{P}-input-e5", t("""
        Напиши функцию `ask_in_range(inputs, low, high)` — первый ответ, который является целым числом **от `low` до `high` включительно**. Нечисловые и вне диапазона пропускать. Если подходящего нет — `None`.

        Пример:
        ```
        ask_in_range(["0", "abc", "11", "7"], 1, 10)   # → 7
        ```
        """),
        """
        def ask_in_range(inputs, low, high):
            pass
        """,
        """
        def test_values():
            got = [ask_in_range(["0", "abc", "11", "7"], 1, 10), ask_in_range(["5"], 5, 5), ask_in_range(["100"], 1, 10), ask_in_range([], 1, 2)]
            assert got == [7, 5, None, None], f"Получено {got}"
        """,
        """
        def ask_in_range(inputs, low, high):
            i = 0
            while i < len(inputs):
                text = inputs[i]
                i += 1
                try:
                    n = int(text)
                except ValueError:
                    continue
                if low <= n <= high:
                    return n
            return None
        """),
    cod(f"{P}-input-e6", t("""
        Напиши функцию `ask_yes_no(inputs)` — ждать ответа «да» или «нет». Ответ очищается `strip().lower()`:

        - `"да"`, `"yes"`, `"y"` → вернуть `True`;
        - `"нет"`, `"no"`, `"n"` → вернуть `False`;
        - остальное — пропустить и «спросить» снова.

        Если ответы кончились — `None`.

        Пример:
        ```
        ask_yes_no(["ну", " ДА "])   # → True
        ask_yes_no(["N"])            # → False
        ```
        """),
        """
        def ask_yes_no(inputs):
            pass
        """,
        """
        def test_values():
            got = [ask_yes_no(["ну", " ДА "]), ask_yes_no(["N"]), ask_yes_no(["?", "maybe"]), ask_yes_no(["yes", "no"])]
            assert got == [True, False, None, True], f"Получено {got}"
        """,
        """
        def ask_yes_no(inputs):
            i = 0
            while i < len(inputs):
                answer = inputs[i].strip().lower()
                i += 1
                if answer in ("да", "yes", "y"):
                    return True
                if answer in ("нет", "no", "n"):
                    return False
            return None
        """),
    cod(f"{P}-input-e7", t("""
        Напиши функцию `collect_until_empty(inputs)` — собирать строки, пока не встретится **пустая** (после `strip()`), как при вводе списка «по одной строке, пустая — конец». Пустую не включать; строки возвращать очищенными.

        Пример:
        ```
        collect_until_empty([" молоко", "хлеб ", "  ", "сыр"])   # → ["молоко", "хлеб"]
        ```
        """),
        """
        def collect_until_empty(inputs):
            pass
        """,
        """
        def test_values():
            got = [collect_until_empty([" молоко", "хлеб ", "  ", "сыр"]), collect_until_empty(["a"]), collect_until_empty([""])]
            assert got == [["молоко", "хлеб"], ["a"], []], f"Получено {got}"
        """,
        """
        def collect_until_empty(inputs):
            result = []
            i = 0
            while i < len(inputs):
                line = inputs[i].strip()
                if not line:
                    break
                result.append(line)
                i += 1
            return result
        """),
    cod(f"{P}-input-e8", t("""
        Напиши функцию `sum_inputs(inputs)` — калькулятор суммы: читать ответы по порядку, пока не встретится `"стоп"` (или пока ответы не кончатся).

        - числа (целые, можно со знаком) — прибавлять к сумме;
        - всё остальное — считать ошибкой ввода и пропускать.

        Вернуть пару `(сумма, число_ошибок)`.

        Пример:
        ```
        sum_inputs(["5", "x", "-2", "стоп", "100"])   # → (3, 1)
        ```
        """),
        """
        def sum_inputs(inputs):
            pass
        """,
        """
        def test_values():
            got = [sum_inputs(["5", "x", "-2", "стоп", "100"]), sum_inputs([]), sum_inputs(["a", "b"]), sum_inputs(["10"])]
            assert got == [(3, 1), (0, 0), (0, 2), (10, 0)], f"Получено {got}"
        """,
        """
        def sum_inputs(inputs):
            total = 0
            errors = 0
            i = 0
            while i < len(inputs):
                text = inputs[i]
                i += 1
                if text == "стоп":
                    break
                try:
                    total += int(text)
                except ValueError:
                    errors += 1
            return total, errors
        """, xp=20),
),
)
