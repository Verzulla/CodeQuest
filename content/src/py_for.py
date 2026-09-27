"""Тема «Цикл for»."""
from ._lib import cod, lesson, module, out, t, topic

P = "for"

# ============================================================
m1 = module(f"{P}-m1", "Основы for", "🔁", "Перебор коллекций, range и вложенные циклы",

lesson(f"{P}-m1-l1", "Перебор коллекций", 
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
        """, xp=20)),

lesson(f"{P}-m1-l2", "range", 
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
        """)),

lesson(f"{P}-m1-l3", "Вложенные циклы", 
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
        """, xp=25)),
)

# ============================================================
m2 = module(f"{P}-m2", "Управление циклом", "🎛️", "break, continue и else у цикла",

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
        """)),

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
        """)),

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
        """)),
)

# ============================================================
m3 = module(f"{P}-m3", "Шаблоны циклов", "🧮", "Подсчёт, поиск и перебор с помощниками",

lesson(f"{P}-m3-l1", "Подсчёт и накопление", 
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
        """)),

lesson(f"{P}-m3-l2", "Поиск в цикле", 
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
        """, xp=20)),

lesson(f"{P}-m3-l3", "Помощники перебора", 
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
        """)),
)

TOPIC = topic("py-for", "Цикл for", "🔁", "#00a88e",
              "Перебор коллекций, range, вложенные циклы, break, continue и шаблоны",
              m1, m2, m3, group="Python")
