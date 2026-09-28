"""Тема «Цикл for», модуль 2 «Управление циклом» — задания. Теория — в _for_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "for"

m2 = module(f"{P}-m2", "Управление циклом", "🎛️", "break, continue, else у цикла и управление вложенными циклами",

lesson(f"{P}-m2-l1", "break — досрочный выход",
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
    out(f"{P}-m2-l1-e6", "Что выведет программа?", """
        for ch in "python":
            if ch == "h":
                break
            print(ch, end="")
        print()
        print("стоп на", ch)
        """, hint="break срабатывает до print, поэтому h не печатается; а переменная ch сохраняет значение."),
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
    cod(f"{P}-m2-l1-e7", t("""
        Напиши функцию `take_until(words, stop)` — слова по порядку **до** стоп-слова (само стоп-слово и всё после него не берётся). Используй `break`.

        Примеры:
        ```
        take_until(["a", "b", "STOP", "c"], "STOP")   # → ["a", "b"]
        take_until(["a", "b"], "STOP")                # → ["a", "b"]
        ```
        """),
        """
        def take_until(words, stop):
            pass
        """,
        """
        def test_values():
            got = [take_until(["a", "b", "STOP", "c"], "STOP"), take_until(["a", "b"], "STOP"), take_until(["STOP", "x"], "STOP")]
            assert got == [["a", "b"], ["a", "b"], []], f"Получено {got}"

        def test_break():
            assert "break" in open("solution.py", encoding="utf-8").read(), "Используй break"
        """,
        """
        def take_until(words, stop):
            result = []
            for w in words:
                if w == stop:
                    break
                result.append(w)
            return result
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `budget_items(prices, budget)` — покупаем товары **по порядку**, пока хватает денег. Как только очередной товар не влезает в остаток бюджета — покупки прекращаются (`break`), даже если дальше есть дешёвые. Верни список купленных цен.

        Пример:
        ```
        budget_items([100, 200, 300, 50], 350)   # → [100, 200]
        ```
        100 + 200 = 300; 300 уже не влезает (осталось 50) — стоп, 50 не покупаем.
        """),
        """
        def budget_items(prices, budget):
            pass
        """,
        """
        def test_values():
            got = [budget_items([100, 200, 300, 50], 350), budget_items([10, 20], 100), budget_items([500], 100), budget_items([50, 50], 100)]
            assert got == [[100, 200], [10, 20], [], [50, 50]], f"Получено {got}"

        def test_break():
            assert "break" in open("solution.py", encoding="utf-8").read(), "Используй break"
        """,
        """
        def budget_items(prices, budget):
            bought = []
            spent = 0
            for p in prices:
                if spent + p > budget:
                    break
                bought.append(p)
                spent += p
            return bought
        """, hint="Перед покупкой проверь spent + p > budget.", xp=20),
),

lesson(f"{P}-m2-l2", "continue — пропустить шаг",
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
    out(f"{P}-m2-l2-e6", "Что выведет программа?", """
        total = 0
        for n in [5, -2, 8, -1, 3]:
            if n < 0:
                continue
            total += n
            print("+", n)
        print(total)
        """, hint="continue пропускает весь остаток тела — и прибавление, и печать."),
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
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `clean_log(lines)` — строки лога без мусора:

        - пустые строки (и строки из одних пробелов) пропускать;
        - строки, начинающиеся с `DEBUG`, пропускать;
        - остальные вернуть **очищенными** от пробелов по краям.

        Пропуски делай через `continue`.

        Пример:
        ```
        clean_log(["  INFO start ", "", "DEBUG x=1", "ERROR boom", "   "])
        # → ["INFO start", "ERROR boom"]
        ```
        """),
        """
        def clean_log(lines):
            pass
        """,
        """
        def test_values():
            got = clean_log(["  INFO start ", "", "DEBUG x=1", "ERROR boom", "   "])
            assert got == ["INFO start", "ERROR boom"] and clean_log([]) == [], f"Получено {got}"

        def test_continue():
            assert "continue" in open("solution.py", encoding="utf-8").read(), "Используй continue"
        """,
        """
        def clean_log(lines):
            result = []
            for line in lines:
                line = line.strip()
                if not line or line.startswith("DEBUG"):
                    continue
                result.append(line)
            return result
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `numbers_without(n, bad)` — числа от 1 до `n` включительно, **кроме** кратных `bad`. Пропускай их через `continue`.

        Пример:
        ```
        numbers_without(10, 3)   # → [1, 2, 4, 5, 7, 8, 10]
        ```
        """),
        """
        def numbers_without(n, bad):
            pass
        """,
        """
        def test_values():
            assert numbers_without(10, 3) == [1, 2, 4, 5, 7, 8, 10] and numbers_without(4, 1) == [] and numbers_without(0, 2) == [], "Неверный результат"

        def test_continue():
            assert "continue" in open("solution.py", encoding="utf-8").read(), "Используй continue"
        """,
        """
        def numbers_without(n, bad):
            result = []
            for i in range(1, n + 1):
                if i % bad == 0:
                    continue
                result.append(i)
            return result
        """),
),

lesson(f"{P}-m2-l3", "else у цикла",
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
    out(f"{P}-m2-l3-e6", "Что выведет программа?", """
        for n in [2, 4]:
            print("проверяю", n)
        else:
            print("цикл дошёл до конца")
        print("дальше")
        """, hint="else выполняется, если цикл завершился без break."),
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
    cod(f"{P}-m2-l3-e7", t("""
        Напиши функцию `all_positive(nums)` — все ли числа больше нуля. Используй `for … else` с `break`: нашли не положительное — `break`, в `else` — все положительные. Для пустого списка — `True`.

        Примеры:
        ```
        all_positive([1, 5, 2])    # → True
        all_positive([3, 0, 4])    # → False
        ```
        """),
        """
        def all_positive(nums):
            pass
        """,
        """
        def test_values():
            got = [all_positive(x) for x in ([1, 5, 2], [3, 0, 4], [], [-1])]
            assert got == [True, False, True, False], f"Получено {got}"

        def test_for_else():
            src = open("solution.py", encoding="utf-8").read()
            assert "else:" in src and "break" in src, "Используй for … else с break"
        """,
        """
        def all_positive(nums):
            for n in nums:
                if n <= 0:
                    result = False
                    break
            else:
                result = True
            return result
        """),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `login_attempts(passwords, correct)` — пробуем пароли из списка по порядку.

        - если пароль совпал — вернуть `"вход с попытки N"` (N с 1);
        - если ни один не подошёл — `"доступ запрещён"`.

        Используй `for … else`.

        Примеры:
        ```
        login_attempts(["1234", "qwerty", "s3cret"], "qwerty")   # → "вход с попытки 2"
        login_attempts(["a", "b"], "c")                          # → "доступ запрещён"
        ```
        """),
        """
        def login_attempts(passwords, correct):
            pass
        """,
        """
        def test_values():
            got = [login_attempts(["1234", "qwerty", "s3cret"], "qwerty"), login_attempts(["a", "b"], "c"), login_attempts([], "x"), login_attempts(["x"], "x")]
            assert got == ["вход с попытки 2", "доступ запрещён", "доступ запрещён", "вход с попытки 1"], f"Получено {got}"

        def test_for_else():
            src = open("solution.py", encoding="utf-8").read()
            assert "else:" in src and "break" in src, "Используй for … else с break"
        """,
        """
        def login_attempts(passwords, correct):
            for i, p in enumerate(passwords, start=1):
                if p == correct:
                    message = f"вход с попытки {i}"
                    break
            else:
                message = "доступ запрещён"
            return message
        """),
),

lesson(f"{P}-ctrl2", "break и continue во вложенных циклах",
    out(f"{P}-ctrl2-e1", "Что выведет программа? Какой цикл прерывает break?", """
        for i in range(3):
            for j in range(3):
                if j == 1:
                    break
                print(i, j)
        """, hint="break прерывает только внутренний цикл — внешний идёт дальше."),
    out(f"{P}-ctrl2-e2", "Что выведет программа?", """
        for i in range(1, 3):
            for j in range(1, 4):
                if j == 2:
                    continue
                print(i, j)
        """),
    out(f"{P}-ctrl2-e3", "Что выведет программа? Флаг для выхода из двух циклов.", """
        grid = [[1, 2], [3, -4], [5, 6]]
        found = False
        for row in grid:
            for x in row:
                if x < 0:
                    found = True
                    break
            if found:
                break
            print("строка", row, "без минусов")
        print(found)
        """),
    cod(f"{P}-ctrl2-e4", t("""
        Напиши функцию `find_pair(nums, target)` — **первую** пару `(nums[i], nums[j])`, где `i < j` и сумма равна `target`. Если пары нет — `None`. Как только нашли — выходи сразу из обоих циклов (`return`).

        Примеры:
        ```
        find_pair([1, 4, 2, 3], 5)   # → (1, 4)
        find_pair([1, 2], 10)        # → None
        ```
        """),
        """
        def find_pair(nums, target):
            pass
        """,
        """
        def test_values():
            got = [find_pair([1, 4, 2, 3], 5), find_pair([1, 2], 10), find_pair([2, 2], 4), find_pair([], 0)]
            assert got == [(1, 4), None, (2, 2), None], f"Получено {got}"
        """,
        """
        def find_pair(nums, target):
            for i in range(len(nums)):
                for j in range(i + 1, len(nums)):
                    if nums[i] + nums[j] == target:
                        return (nums[i], nums[j])
            return None
        """),
    cod(f"{P}-ctrl2-e5", t("""
        Напиши функцию `rows_without_zero(matrix)` — сколько строк таблицы **не содержат** ни одного нуля. Проверяй строку внутренним циклом: нашёл 0 — `break`.

        Пример:
        ```
        rows_without_zero([[1, 2], [0, 3], [4, 5]])   # → 2
        ```
        Подсказка: удобно `for … else` — `else` у внутреннего цикла выполнится, если нуля не нашлось.
        """),
        """
        def rows_without_zero(matrix):
            pass
        """,
        """
        def test_values():
            got = [rows_without_zero([[1, 2], [0, 3], [4, 5]]), rows_without_zero([[0]]), rows_without_zero([[], [1]]), rows_without_zero([])]
            assert got == [2, 0, 2, 0], f"Получено {got}"

        def test_break():
            assert "break" in open("solution.py", encoding="utf-8").read(), "Используй break во внутреннем цикле"
        """,
        """
        def rows_without_zero(matrix):
            count = 0
            for row in matrix:
                for x in row:
                    if x == 0:
                        break
                else:
                    count += 1
            return count
        """, xp=20),
    cod(f"{P}-ctrl2-e6", t("""
        Напиши функцию `primes_up_to(n)` — список всех простых чисел от 2 до `n` включительно. Внешний цикл — по числам, внутренний — по возможным делителям; `for … else` у внутреннего.

        Пример:
        ```
        primes_up_to(20)   # → [2, 3, 5, 7, 11, 13, 17, 19]
        primes_up_to(1)    # → []
        ```
        """),
        """
        def primes_up_to(n):
            pass
        """,
        """
        def test_values():
            assert primes_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19] and primes_up_to(1) == [] and primes_up_to(2) == [2], f"Получено {primes_up_to(20)}"
        """,
        """
        def primes_up_to(n):
            primes = []
            for num in range(2, n + 1):
                for d in range(2, num):
                    if num % d == 0:
                        break
                else:
                    primes.append(num)
            return primes
        """, hint="Это задача is_prime, повторённая для каждого числа.", xp=25),
    cod(f"{P}-ctrl2-e7", t("""
        Напиши функцию `sum_until_stop(matrix)` — сумма чисел таблицы по строкам слева направо, но как только встретилась строка `"STOP"` — остановиться **полностью** (дальше не считать ни в этой строке, ни в следующих).

        Пример:
        ```
        sum_until_stop([[1, 2], [3, "STOP", 5], [6]])   # → 6
        sum_until_stop([[1], [2]])                      # → 3
        ```
        """),
        """
        def sum_until_stop(matrix):
            pass
        """,
        """
        def test_values():
            got = [sum_until_stop([[1, 2], [3, "STOP", 5], [6]]), sum_until_stop([[1], [2]]), sum_until_stop([["STOP"], [9]]), sum_until_stop([])]
            assert got == [6, 3, 0, 0], f"Получено {got}"
        """,
        """
        def sum_until_stop(matrix):
            total = 0
            for row in matrix:
                for x in row:
                    if x == "STOP":
                        return total
                    total += x
            return total
        """, hint="break выйдет только из внутреннего цикла. return — сразу из функции."),
    cod(f"{P}-ctrl2-e8", t("""
        Напиши функцию `no_repeats(words)` — слова, в которых **ни одна буква не повторяется**. Для каждого слова внутренний цикл проверяет буквы: встретил уже виденную — слово не подходит.

        Пример:
        ```
        no_repeats(["кот", "мама", "дом", "аа"])   # → ["кот", "дом"]
        ```
        """),
        """
        def no_repeats(words):
            pass
        """,
        """
        def test_values():
            got = no_repeats(["кот", "мама", "дом", "аа"])
            assert got == ["кот", "дом"] and no_repeats([]) == [] and no_repeats([""]) == [""], f"Получено {got}"
        """,
        """
        def no_repeats(words):
            result = []
            for w in words:
                seen = ""
                for ch in w:
                    if ch in seen:
                        break
                    seen += ch
                else:
                    result.append(w)
            return result
        """, hint="Копи просмотренные буквы в строке seen; else у внутреннего цикла — «повторов не нашлось».", xp=20),
),
)
