"""Тема «Цикл while», модуль 3 «Алгоритмы на while» — задания. Теория — в _whl_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "whl"

m3 = module(f"{P}-m3", "Алгоритмы на while", "🧠", "Двоичный поиск, последовательности, симуляции, пороги и отладка циклов",

lesson(f"{P}-m3-l1", "Двоичный поиск",
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
    out(f"{P}-m3-l1-e6", "Что выведет программа? Проследи границы поиска.", """
        xs = [2, 4, 6, 8, 10, 12, 14]
        lo, hi = 0, len(xs) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            print(lo, hi, mid)
            if xs[mid] < 5:
                lo = mid + 1
            else:
                hi = mid - 1
        print("lo =", lo)
        """, hint="Когда элемента нет, lo в конце указывает, куда его можно вставить."),
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
    cod(f"{P}-m3-l1-e7", t("""
        Напиши функцию `insert_position(xs, x)` — индекс, куда нужно вставить `x` в **отсортированный** список, чтобы порядок сохранился (если `x` уже есть — позиция **перед** первым таким). Двоичный поиск, без перебора.

        Примеры:
        ```
        insert_position([1, 3, 5], 4)   # → 2
        insert_position([1, 3, 5], 0)   # → 0
        insert_position([1, 3, 5], 6)   # → 3
        insert_position([1, 3, 3], 3)   # → 1
        ```
        """),
        """
        def insert_position(xs, x):
            pass
        """,
        """
        def test_values():
            got = [insert_position([1, 3, 5], 4), insert_position([1, 3, 5], 0), insert_position([1, 3, 5], 6), insert_position([1, 3, 3], 3), insert_position([], 7)]
            assert got == [2, 0, 3, 1, 0], f"Получено {got}"

        def test_while():
            src = open("solution.py", encoding="utf-8").read()
            assert "while " in src and "for " not in src, "Реши двоичным поиском на while"
        """,
        """
        def insert_position(xs, x):
            lo, hi = 0, len(xs) - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if xs[mid] < x:
                    lo = mid + 1
                else:
                    hi = mid - 1
            return lo
        """, hint="Это двоичный поиск, где при xs[mid] >= x мы идём влево. Ответ — lo.", xp=20),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `guess_game(secret, low, high)` — компьютер угадывает загаданное число от `low` до `high`, всегда называя **середину** оставшегося диапазона (`(low + high) // 2`). Вернуть, за сколько догадок он угадает.

        Примеры:
        ```
        guess_game(50, 1, 100)   # → 1   (первая догадка — 50)
        guess_game(25, 1, 100)   # → 2   (50 → «меньше» → 25)
        ```
        Для любого числа от 1 до 100 хватает 7 догадок.
        """),
        """
        def guess_game(secret, low, high):
            pass
        """,
        """
        def test_values():
            assert guess_game(50, 1, 100) == 1 and guess_game(25, 1, 100) == 2, "Неверное число догадок"
            assert max(guess_game(s, 1, 100) for s in range(1, 101)) == 7, "Для 1..100 максимум 7 догадок"
        """,
        """
        def guess_game(secret, low, high):
            guesses = 0
            while True:
                guess = (low + high) // 2
                guesses += 1
                if guess == secret:
                    return guesses
                if guess < secret:
                    low = guess + 1
                else:
                    high = guess - 1
        """, xp=20),
),

lesson(f"{P}-m3-l2", "Последовательности",
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
    out(f"{P}-m3-l2-e6", "Что выведет программа?", """
        x = 1
        powers = []
        while x < 100:
            powers.append(x)
            x *= 3
        print(powers, x)
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
    cod(f"{P}-m3-l2-e7", t("""
        Напиши функцию `lcm(a, b)` — наименьшее общее кратное двух положительных чисел. Сначала найди НОД алгоритмом Евклида (`while`), потом `a * b // НОД`. Без `math`.

        Примеры:
        ```
        lcm(4, 6)    # → 12
        lcm(5, 7)    # → 35
        lcm(10, 5)   # → 10
        ```
        """),
        """
        def lcm(a, b):
            pass
        """,
        """
        def test_values():
            assert [lcm(4, 6), lcm(5, 7), lcm(10, 5), lcm(1, 1)] == [12, 35, 10, 1], "Неверное НОК"

        def test_no_math():
            src = open("solution.py", encoding="utf-8").read()
            assert "math" not in src and "while " in src, "Реализуй через Евклида на while"
        """,
        """
        def lcm(a, b):
            x, y = a, b
            while y:
                x, y = y, x % y
            return a * b // x
        """, hint="Сохрани a и b — они понадобятся после цикла, а x, y алгоритм «съедает»."),
    cod(f"{P}-m3-l2-e8", t("""
        Напиши функцию `triangular_until(limit)` — треугольные числа `1, 3, 6, 10, 15, …` (сумма `1 + 2 + … + n`), не превышающие `limit`.

        Примеры:
        ```
        triangular_until(20)   # → [1, 3, 6, 10, 15]
        triangular_until(0)    # → []
        ```
        """),
        """
        def triangular_until(limit):
            pass
        """,
        """
        def test_values():
            assert triangular_until(20) == [1, 3, 6, 10, 15] and triangular_until(0) == [] and triangular_until(1) == [1] and triangular_until(21) == [1, 3, 6, 10, 15, 21], "Неверная последовательность"
        """,
        """
        def triangular_until(limit):
            result = []
            n, value = 1, 1
            while value <= limit:
                result.append(value)
                n += 1
                value += n
            return result
        """),
),

lesson(f"{P}-m3-l3", "Симуляции",
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
    out(f"{P}-m3-l3-e6", "Что выведет программа? Рост популяции.", """
        population = 100
        year = 0
        while population < 200:
            population = int(population * 1.3)
            year += 1
            print(year, population)
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
    cod(f"{P}-m3-l3-e7", t("""
        Напиши функцию `elevator(requests, start=0)` — лифт стоит на этаже `start` и едет по вызовам из списка по очереди. Вернуть, сколько этажей он проехал всего.

        Пример:
        ```
        elevator([5, 2, 8])       # → 14   (0→5: 5, 5→2: 3, 2→8: 6)
        elevator([3], start=3)    # → 0
        ```
        Используй `while`.
        """),
        """
        def elevator(requests, start=0):
            pass
        """,
        """
        def test_values():
            assert elevator([5, 2, 8]) == 14 and elevator([3], start=3) == 0 and elevator([]) == 0 and elevator([1, -1]) == 3, "Неверное расстояние"

        def test_while():
            assert "while " in open("solution.py", encoding="utf-8").read(), "Используй while"
        """,
        """
        def elevator(requests, start=0):
            floor = start
            total = 0
            i = 0
            while i < len(requests):
                total += abs(requests[i] - floor)
                floor = requests[i]
                i += 1
            return total
        """, hint="abs(a - b) — расстояние между этажами без знака."),
    cod(f"{P}-m3-l3-e8", t("""
        Напиши функцию `battle(hp_a, hp_b, dmg_a, dmg_b)` — пошаговый бой. Каждый раунд:

        1. A бьёт B (`hp_b -= dmg_a`); если у B здоровье `<= 0` — побеждает A;
        2. иначе B бьёт A (`hp_a -= dmg_b`); если у A `<= 0` — побеждает B.

        Вернуть пару `(победитель, номер_раунда)`.

        Пример:
        ```
        battle(10, 10, 3, 4)   # → ("B", 3)
        battle(5, 5, 10, 1)    # → ("A", 1)
        ```
        """),
        """
        def battle(hp_a, hp_b, dmg_a, dmg_b):
            pass
        """,
        """
        def test_values():
            got = [battle(10, 10, 3, 4), battle(5, 5, 10, 1), battle(10, 9, 3, 3)]
            assert got == [("B", 3), ("A", 1), ("A", 3)], f"Получено {got}"
        """,
        """
        def battle(hp_a, hp_b, dmg_a, dmg_b):
            round_no = 0
            while True:
                round_no += 1
                hp_b -= dmg_a
                if hp_b <= 0:
                    return "A", round_no
                hp_a -= dmg_b
                if hp_a <= 0:
                    return "B", round_no
        """, xp=20),
),

lesson(f"{P}-threshold", "Пока не достигнем цели: пороги и приближения",
    out(f"{P}-threshold-e1", "Что выведет программа? Сложные проценты.", """
        balance = 1000
        years = 0
        while balance < 1500:
            balance = balance * 1.1
            years += 1
        print(years, round(balance, 2))
        """),
    out(f"{P}-threshold-e2", "Что выведет программа? Метод Ньютона для корня из 2.", """
        n = 2
        x = n
        while abs(x * x - n) > 0.0001:
            x = (x + n / x) / 2
            print(round(x, 5))
        """, hint="Каждый шаг приближения резко уточняет ответ; цикл идёт, пока ошибка больше допуска."),
    out(f"{P}-threshold-e3", "Что выведет программа? Загрузка до лимита.", """
        weights = [4, 3, 5, 2]
        load, i = 0, 0
        while i < len(weights) and load + weights[i] <= 10:
            load += weights[i]
            i += 1
        print(i, load)
        """),
    cod(f"{P}-threshold-e4", t("""
        Напиши функцию `months_to_save(goal, monthly)` — сколько месяцев откладывать по `monthly`, чтобы накопить **не меньше** `goal`. Используй `while`.

        Примеры:
        ```
        months_to_save(1000, 300)   # → 4
        months_to_save(900, 300)    # → 3
        months_to_save(0, 100)      # → 0
        ```
        """),
        """
        def months_to_save(goal, monthly):
            pass
        """,
        """
        def test_values():
            assert [months_to_save(1000, 300), months_to_save(900, 300), months_to_save(0, 100), months_to_save(1, 1000)] == [4, 3, 0, 1], "Неверное число месяцев"

        def test_while():
            assert "while " in open("solution.py", encoding="utf-8").read(), "Используй while"
        """,
        """
        def months_to_save(goal, monthly):
            saved = 0
            months = 0
            while saved < goal:
                saved += monthly
                months += 1
            return months
        """),
    cod(f"{P}-threshold-e5", t("""
        Напиши функцию `sqrt_approx(n, eps=1e-9)` — квадратный корень из неотрицательного `n` **методом Ньютона**:

        - начальное приближение `x = n` (для `n = 0` сразу вернуть 0);
        - пока `abs(x * x - n) > eps`: `x = (x + n / x) / 2`.

        Без `**`, `math` и `pow`.

        Примеры:
        ```
        sqrt_approx(9)    # ≈ 3.0
        sqrt_approx(2)    # ≈ 1.41421356
        ```
        """),
        """
        def sqrt_approx(n, eps=1e-9):
            pass
        """,
        """
        def test_values():
            for n in (9, 2, 1, 0.25, 1e6):
                r = sqrt_approx(n)
                assert abs(r * r - n) < 1e-6, f"sqrt_approx({n}) = {r}"
            assert sqrt_approx(0) == 0, "Корень из 0 — 0"

        def test_no_pow():
            src = open("solution.py", encoding="utf-8").read()
            assert "**" not in src and "math" not in src and "pow(" not in src, "Реализуй метод Ньютона сам"
        """,
        """
        def sqrt_approx(n, eps=1e-9):
            if n == 0:
                return 0
            x = n
            while abs(x * x - n) > eps:
                x = (x + n / x) / 2
            return x
        """, hint="1e-9 — это 0.000000001, запись числа в научном формате.", xp=20),
    cod(f"{P}-threshold-e6", t("""
        Напиши функцию `halving_steps(value, limit)` — сколько раз нужно **делить пополам** (`/ 2`) число `value`, чтобы оно стало **меньше** `limit`.

        Примеры:
        ```
        halving_steps(100, 1)   # → 7   (50, 25, 12.5, 6.25, 3.125, 1.5625, 0.78125)
        halving_steps(0.5, 1)   # → 0
        ```
        """),
        """
        def halving_steps(value, limit):
            pass
        """,
        """
        def test_values():
            assert [halving_steps(100, 1), halving_steps(0.5, 1), halving_steps(8, 1), halving_steps(1, 1)] == [7, 0, 4, 1], "Неверное число шагов"
        """,
        """
        def halving_steps(value, limit):
            steps = 0
            while value >= limit:
                value /= 2
                steps += 1
            return steps
        """),
    cod(f"{P}-threshold-e7", t("""
        Напиши функцию `fill_boxes(items, capacity)` — раскладывать грузы по коробкам **по порядку**: кладём в текущую коробку, пока влезает; если очередной не влезает — начинаем новую. Каждый груз не больше `capacity`. Вернуть число коробок.

        Пример:
        ```
        fill_boxes([4, 3, 5, 2], 10)   # → 2   ([4, 3] и [5, 2])
        fill_boxes([], 10)             # → 0
        ```
        """),
        """
        def fill_boxes(items, capacity):
            pass
        """,
        """
        def test_values():
            got = [fill_boxes([4, 3, 5, 2], 10), fill_boxes([], 10), fill_boxes([10, 10], 10), fill_boxes([6, 5, 4, 3], 10)]
            assert got == [2, 0, 2, 3], f"Получено {got}"
        """,
        """
        def fill_boxes(items, capacity):
            boxes = 0
            load = 0
            i = 0
            while i < len(items):
                if boxes == 0 or load + items[i] > capacity:
                    boxes += 1
                    load = 0
                load += items[i]
                i += 1
            return boxes
        """, hint="Новая коробка нужна для самого первого груза и когда очередной не влезает.", xp=20),
    cod(f"{P}-threshold-e8", t("""
        Напиши функцию `loan_months(debt, rate, payment)` — за сколько месяцев погасится кредит. Каждый месяц:

        1. долг растёт на `rate` процентов;
        2. вычитается платёж `payment`.

        Как только долг `<= 0` — кредит погашен. Если платёж не покрывает даже проценты первого месяца (`payment <= debt * rate / 100`), долг никогда не уменьшится — вернуть `-1`.

        Примеры:
        ```
        loan_months(1000, 1, 300)    # → 4
        loan_months(1000, 10, 100)   # → -1
        ```
        """),
        """
        def loan_months(debt, rate, payment):
            pass
        """,
        """
        def test_values():
            got = [loan_months(1000, 1, 300), loan_months(1000, 10, 100), loan_months(100, 0, 100), loan_months(1000, 10, 101)]
            assert got[:3] == [4, -1, 1], f"Получено {got}"
            assert got[3] > 30, "При платеже чуть выше процентов кредит гасится очень долго"
        """,
        """
        def loan_months(debt, rate, payment):
            if payment <= debt * rate / 100:
                return -1
            months = 0
            while debt > 0:
                debt = debt * (1 + rate / 100) - payment
                months += 1
            return months
        """, hint="Сначала проверь «вечный» случай — иначе цикл никогда не закончится.", xp=25),
),

lesson(f"{P}-debug", "Отладка циклов и защита от зависаний",
    out(f"{P}-debug-e1", "Что выведет программа? Отладочная печать.", """
        n = 10
        step = 0
        while n > 1:
            step += 1
            n = n // 2
            print(f"шаг {step}: n = {n}")
        """),
    out(f"{P}-debug-e2", "Что выведет программа? Дробные числа и !=.", """
        x = 0.0
        steps = 0
        while x != 1.0 and steps < 20:
            x += 0.1
            steps += 1
        print(steps, x == 1.0, round(x, 2))
        """, hint="0.1 в компьютере хранится неточно: десять раз по 0.1 — не ровно 1.0."),
    out(f"{P}-debug-e3", "Что выведет программа? Счётчик-предохранитель.", """
        n = 7
        guard = 0
        while n != 0 and guard < 5:
            n -= 2
            guard += 1
        print(n, guard)
        """),
    cod(f"{P}-debug-e4", t("""
        Функция `inclusive_list(a, b)` должна вернуть все числа от `a` до `b` **включительно**, но теряет последнее. Найди ошибку «на единицу» и исправь.

        Примеры:
        ```
        inclusive_list(1, 4)   # → [1, 2, 3, 4]
        inclusive_list(3, 3)   # → [3]
        inclusive_list(5, 2)   # → []
        ```
        """),
        """
        def inclusive_list(a, b):
            result = []
            i = a
            while i < b:
                result.append(i)
                i += 1
            return result
        """,
        """
        def test_values():
            got = [inclusive_list(1, 4), inclusive_list(3, 3), inclusive_list(5, 2)]
            assert got == [[1, 2, 3, 4], [3], []], f"Получено {got}"
        """,
        """
        def inclusive_list(a, b):
            result = []
            i = a
            while i <= b:
                result.append(i)
                i += 1
            return result
        """, hint="Проверь крайний случай: при i == b тело должно выполниться."),
    cod(f"{P}-debug-e5", t("""
        Напиши функцию `trace_halving(n)` — «журнал» работы цикла: делить `n` нацело на 2, пока `n > 1`, и записывать каждое значение (включая начальное) строкой `"n=<значение>"`.

        Пример:
        ```
        trace_halving(10)   # → ["n=10", "n=5", "n=2", "n=1"]
        trace_halving(1)    # → ["n=1"]
        ```
        """),
        """
        def trace_halving(n):
            pass
        """,
        """
        def test_values():
            got = [trace_halving(10), trace_halving(1), trace_halving(8)]
            assert got == [["n=10", "n=5", "n=2", "n=1"], ["n=1"], ["n=8", "n=4", "n=2", "n=1"]], f"Получено {got}"
        """,
        """
        def trace_halving(n):
            log = [f"n={n}"]
            while n > 1:
                n //= 2
                log.append(f"n={n}")
            return log
        """),
    cod(f"{P}-debug-e6", t("""
        Напиши функцию `reach(target, step)` — сколько раз нужно прибавить дробный `step` к нулю, чтобы сумма стала **не меньше** `target`.

        Осторожно: `0.1 * 10` в компьютере — это `0.9999999999999999`, и наивное условие `while x < target` даст для `reach(1, 0.1)` лишний шаг. Сравнивай с допуском: `while x < target - 1e-9`.

        Примеры:
        ```
        reach(1, 0.1)    # → 10
        reach(1, 0.25)   # → 4
        reach(0.3, 0.1)  # → 3
        ```
        """),
        """
        def reach(target, step):
            pass
        """,
        """
        def test_values():
            got = [reach(1, 0.1), reach(1, 0.25), reach(0.3, 0.1), reach(0, 0.5), reach(0.7, 0.1)]
            assert got == [10, 4, 3, 0, 7], f"Получено {got}"
        """,
        """
        def reach(target, step):
            x = 0.0
            steps = 0
            while x < target - 1e-9:
                x += step
                steps += 1
            return steps
        """, hint="1e-9 — крошечный допуск, который «прощает» ошибку округления дробных чисел.", xp=20),
    cod(f"{P}-debug-e7", t("""
        Напиши функцию `run_until(values, stop_value, max_steps)` — искать `stop_value` в списке с **предохранителем**. Вернуть пару:

        - `("found", i)` — нашли на индексе `i` (в пределах `max_steps` проверок);
        - `("limit", max_steps)` — сделали `max_steps` проверок и не нашли;
        - `("end", len(values))` — список кончился раньше лимита.

        Примеры:
        ```
        run_until([5, 3, 9], 9, 10)   # → ("found", 2)
        run_until([5, 3, 9], 9, 2)    # → ("limit", 2)
        run_until([5, 3], 7, 10)      # → ("end", 2)
        ```
        """),
        """
        def run_until(values, stop_value, max_steps):
            pass
        """,
        """
        def test_values():
            got = [run_until([5, 3, 9], 9, 10), run_until([5, 3, 9], 9, 2), run_until([5, 3], 7, 10), run_until([], 1, 0)]
            assert got == [("found", 2), ("limit", 2), ("end", 2), ("limit", 0)], f"Получено {got}"
        """,
        """
        def run_until(values, stop_value, max_steps):
            i = 0
            while True:
                if i >= max_steps:
                    return "limit", max_steps
                if i >= len(values):
                    return "end", len(values)
                if values[i] == stop_value:
                    return "found", i
                i += 1
        """, hint="Порядок проверок определяет ответ для пограничных случаев: сначала лимит, потом конец списка.", xp=20),
    cod(f"{P}-debug-e8", t("""
        Функция `product_digits(n)` должна вернуть произведение цифр положительного числа, но для многозначных чисел результат неверный. Найди ошибку в условии цикла и исправь.

        Примеры:
        ```
        product_digits(234)   # → 24
        product_digits(5)     # → 5
        product_digits(101)   # → 0
        ```
        """),
        """
        def product_digits(n):
            result = 1
            while n > 9:
                result *= n % 10
                n //= 10
            return result
        """,
        """
        def test_values():
            assert [product_digits(n) for n in (234, 5, 101, 99)] == [24, 5, 0, 81], "Неверное произведение цифр"
        """,
        """
        def product_digits(n):
            result = 1
            while n > 0:
                result *= n % 10
                n //= 10
            return result
        """, hint="Проследи по шагам для 234: какая цифра не попадает в произведение?"),
),
)
