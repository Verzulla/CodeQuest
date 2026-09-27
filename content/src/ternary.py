"""Тема «Тернарный оператор»."""
from ._lib import t, cod, lesson, module, out, topic

P = "tern"

m1 = module(f"{P}-m1", "Выражение if-else", "⚖️", "Условие в одну строку",
    lesson(f"{P}-m1-l1", "Синтаксис тернарника", """
        # Тернарный оператор

        Иногда `if/else` нужен только чтобы выбрать **одно из двух значений**:

        ```
        if age >= 18:
            status = "взрослый"
        else:
            status = "ребёнок"
        ```

        То же самое одной строкой:

        ```
        status = "взрослый" if age >= 18 else "ребёнок"
        ```

        Читается почти по-английски: *«значение_1, если условие, иначе значение_2»*.

        - Это **выражение** — у него есть значение, его можно присвоить, вернуть, передать в функцию.
        - Ветка `else` **обязательна**.
        - Вычисляется только та ветка, которая выбрана.
        """,
        out(f"{P}-m1-l1-e1", "Что выведет программа?", """
            age = 20
            status = "взрослый" if age >= 18 else "ребёнок"
            print(status)
            """),
        out(f"{P}-m1-l1-e2", "Что выведет программа?", """
            x = -5
            print("плюс" if x > 0 else "не плюс")
            print(x if x > 0 else -x)
            """, hint="Вторая строка — это модуль числа: для отрицательных берём -x."),
        out(f"{P}-m1-l1-e3", "Что выведет программа?", """
            items = []
            print("пусто" if not items else "есть элементы")
            items.append(1)
            print("пусто" if not items else "есть элементы")
            """),
        cod(f"{P}-m1-l1-e4", t("""
            Перепиши функцию `parity(n)` короче — через тернарный оператор.

            Сейчас в заготовке функция работает правильно, но занимает 4 строки с `if/else`. Сделай так, чтобы тело функции было **одной строкой** вида:
            ```
            return ... if ... else ...
            ```
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
                assert len(body) == 1 and " if " in body[0] and " else " in body[0], "Тело функции должно быть одной строкой с тернарником"
            """,
            """
            def parity(n):
                return "чёт" if n % 2 == 0 else "нечет"
            """,
            hint="`return \"чёт\" if n % 2 == 0 else \"нечет\"`"),
        cod(f"{P}-m1-l1-e5", t("""
            Напиши функцию `abs_value(x)` — модуль числа (расстояние от нуля).

            - Получает: `x` — число.
            - Возвращает: само число, если оно неотрицательное, и число без минуса, если отрицательное.

            Примеры:
            ```
            abs_value(5)    # → 5
            abs_value(-8)   # → 8
            abs_value(0)    # → 0
            ```
            Ограничения: встроенную `abs` не использовать; реши **одной строкой** через тернарный оператор.
            """),
            """
            def abs_value(x):
                pass
            """,
            """
            def test_positive():
                assert abs_value(5) == 5, "abs_value(5) → 5"

            def test_negative():
                assert abs_value(-8) == 8, "abs_value(-8) → 8"

            def test_zero():
                assert abs_value(0) == 0, "abs_value(0) → 0"
            """,
            """
            def abs_value(x):
                return x if x >= 0 else -x
            """),
        cod(f"{P}-m1-l1-e6", t("""
            Напиши функцию `min2(a, b)`, которая возвращает меньшее из двух чисел.

            - Получает: два числа `a` и `b`.
            - Возвращает: меньшее из них (если равны — любое).

            Примеры:
            ```
            min2(2, 9)    # → 2
            min2(9, -1)   # → -1
            min2(3, 3)    # → 3
            ```
            Реши одной строкой `return ... if ... else ...`, без встроенной `min`.
            """),
            """
            def min2(a, b):
                pass
            """,
            """
            def test_first():
                assert min2(2, 9) == 2, "min2(2, 9) → 2"

            def test_second():
                assert min2(9, -1) == -1, "min2(9, -1) → -1"

            def test_equal():
                assert min2(3, 3) == 3, "min2(3, 3) → 3"
            """,
            """
            def min2(a, b):
                return a if a < b else b
            """),
    ),
    lesson(f"{P}-m1-l2", "Тернарник в деле", """
        # Где тернарник особенно удобен

        **В f-строках:**
        ```
        n = 1
        print(f"{n} {'файл' if n == 1 else 'файлов'}")
        ```

        **В аргументах функций:**
        ```
        print("OK" if passed else "FAIL")
        ```

        **В генераторах списков** (об этом ещё поговорим):
        ```
        labels = ["чёт" if x % 2 == 0 else "нечет" for x in [1, 2, 3]]
        ```

        **Вложенный тернарник** возможен, но читается тяжело:
        ```
        sign = "плюс" if x > 0 else "минус" if x < 0 else "ноль"
        ```
        Если условий больше двух — лучше обычный `if/elif/else`.
        """,
        out(f"{P}-m1-l2-e1", "Что выведет программа?", """
            for n in [1, 3]:
                print(f"{n} {'тест' if n == 1 else 'теста'}")
            """),
        out(f"{P}-m1-l2-e2", "Что выведет программа?", """
            print(["чёт" if x % 2 == 0 else "нечет" for x in range(4)])
            """),
        out(f"{P}-m1-l2-e3", "Что выведет программа? Разбери вложенный тернарник по шагам.", """
            for x in [5, 0, -2]:
                print("плюс" if x > 0 else "минус" if x < 0 else "ноль")
            """, hint="Читай слева направо: если x > 0 — «плюс», иначе снова тернарник."),
        cod(f"{P}-m1-l2-e4", t("""
            Напиши функцию `status_line(passed, failed)`, которая формирует строку статуса тестового прогона.

            - Получает: `passed` — сколько тестов прошло, `failed` — сколько упало.
            - Возвращает строку:
              - `"✅ all green"` — если упавших нет (`failed == 0`);
              - `"❌ N failed"` — иначе, где вместо `N` стоит число упавших.

            Примеры:
            ```
            status_line(10, 0)   # → "✅ all green"
            status_line(8, 2)    # → "❌ 2 failed"
            ```
            Используй тернарный оператор и f-строку.
            """),
            """
            def status_line(passed, failed):
                pass
            """,
            """
            def test_green():
                assert status_line(10, 0) == "✅ all green", f"Получено {status_line(10, 0)!r}"

            def test_red():
                assert status_line(8, 2) == "❌ 2 failed", f"Получено {status_line(8, 2)!r}"
            """,
            """
            def status_line(passed, failed):
                return "✅ all green" if failed == 0 else f"❌ {failed} failed"
            """),
        cod(f"{P}-m1-l2-e5", t("""
            Напиши функцию `clamp(x, low, high)`, которая «зажимает» число в заданные границы.

            Представь ползунок громкости от `low` до `high`: значение не может выйти за его пределы.

            - Получает: `x` — число; `low` и `high` — нижняя и верхняя граница (`low ≤ high`).
            - Возвращает:
              - `low` — если `x` меньше нижней границы;
              - `high` — если `x` больше верхней границы;
              - сам `x` — если он уже внутри диапазона.

            Примеры:
            ```
            clamp(5, 0, 10)    # → 5    внутри диапазона — без изменений
            clamp(-3, 0, 10)   # → 0    меньше нижней границы — поднимаем до 0
            clamp(42, 0, 10)   # → 10   больше верхней — опускаем до 10
            ```
            Попробуй уложиться в одну строку с **вложенным** тернарником: `A if условие1 else B if условие2 else C`.
            """),
            """
            def clamp(x, low, high):
                pass
            """,
            """
            def test_inside():
                assert clamp(5, 0, 10) == 5, "clamp(5, 0, 10) → 5"

            def test_low():
                assert clamp(-3, 0, 10) == 0, "clamp(-3, 0, 10) → 0"

            def test_high():
                assert clamp(42, 0, 10) == 10, "clamp(42, 0, 10) → 10"
            """,
            """
            def clamp(x, low, high):
                return low if x < low else high if x > high else x
            """,
            hint="`low if x < low else (high if x > high else x)`", xp=20),
    ),
)

m2 = module(f"{P}-m2", "Практикум", "🛠️", "Короткие условия в реальных задачах",
    lesson(f"{P}-m2-l1", "Значения по умолчанию", """
        # Значение по умолчанию: тернарник и `or`

        Частая задача — подставить значение, если пришло «пустое»:

        ```
        name = user_name if user_name else "Гость"
        ```

        Короче через `or` — он возвращает **первый истинный** операнд (или последний):

        ```
        name = user_name or "Гость"
        ```

        ⚠️ Ловушка: `or` заменит и `0`, и `""`, и `[]` — они тоже «ложные».
        Если `0` — допустимое значение, пиши явно: `x if x is not None else 10`.
        """,
        out(f"{P}-m2-l1-e1", "Что выведет программа?", """
            print("" or "Гость")
            print("Аня" or "Гость")
            print(0 or 10)
            """, hint="`or` возвращает первый «истинный» операнд, а не True/False."),
        out(f"{P}-m2-l1-e2", "Что выведет программа?", """
            timeout = 0
            a = timeout or 30
            b = timeout if timeout is not None else 30
            print(a, b)
            """, hint="Ноль — «ложь», поэтому `or` его заменит, а проверка на None — нет."),
        cod(f"{P}-m2-l1-e3", t("""
            Напиши функцию `display_name(name)`, которая готовит имя для показа на экране.

            - Получает: `name` — строку с именем, пустую строку `""` или `None`.
            - Возвращает: само имя, а если имени нет (пустая строка или `None`) — строку `"Аноним"`.

            Примеры:
            ```
            display_name("Вася")   # → "Вася"
            display_name("")       # → "Аноним"
            display_name(None)     # → "Аноним"
            ```
            Короче всего через `or` из теории.
            """),
            """
            def display_name(name):
                pass
            """,
            """
            def test_name():
                assert display_name("Вася") == "Вася", 'display_name("Вася") → "Вася"'

            def test_empty():
                assert display_name("") == "Аноним", 'Пустая строка → "Аноним"'

            def test_none():
                assert display_name(None) == "Аноним", 'None → "Аноним"'
            """,
            """
            def display_name(name):
                return name or "Аноним"
            """),
        cod(f"{P}-m2-l1-e4", t("""
            Напиши функцию `get_timeout(value)`, которая подставляет таймаут по умолчанию.

            - Получает: `value` — число секунд или `None` (значит «не задано»).
            - Возвращает: `30`, если `value` равно `None`; иначе — само `value`.

            Примеры:
            ```
            get_timeout(None)   # → 30
            get_timeout(5)      # → 5
            get_timeout(0)      # → 0    ноль — допустимый таймаут, его нельзя заменять!
            ```
            Ловушка: `value or 30` здесь не подойдёт — `or` заменит и `0`. Проверяй именно на `None`: `value is None`.
            """),
            """
            def get_timeout(value):
                pass
            """,
            """
            def test_none():
                assert get_timeout(None) == 30, "None → 30"

            def test_zero():
                assert get_timeout(0) == 0, "0 должен остаться 0 — не используй `or`!"

            def test_value():
                assert get_timeout(5) == 5, "5 → 5"
            """,
            """
            def get_timeout(value):
                return 30 if value is None else value
            """,
            hint="`30 if value is None else value`"),
        cod(f"{P}-m2-l1-e5", t("""
            Напиши функцию `pluralize(n)`, которая склоняет слово «баг» после числа.

            - Получает: `n` — целое число от 0 до 20.
            - Возвращает строку «число + слово в нужной форме»:
              - `1` → `"1 баг"`;
              - `2`, `3`, `4` → `"2 бага"`, `"3 бага"`, `"4 бага"`;
              - `0` и `5`…`20` → `"0 багов"`, `"7 багов"`, `"12 багов"`.

            Примеры:
            ```
            pluralize(1)    # → "1 баг"
            pluralize(3)    # → "3 бага"
            pluralize(7)    # → "7 багов"
            pluralize(12)   # → "12 багов"
            ```
            Сначала выбери форму слова тернарником, потом собери строку f-строкой.
            """),
            """
            def pluralize(n):
                pass
            """,
            """
            def test_one():
                assert pluralize(1) == "1 баг", f"pluralize(1) → {pluralize(1)!r}"

            def test_few():
                assert pluralize(3) == "3 бага", f"pluralize(3) → {pluralize(3)!r}"

            def test_many():
                assert pluralize(7) == "7 багов" and pluralize(0) == "0 багов", "7 → «7 багов», 0 → «0 багов»"

            def test_teens():
                assert pluralize(12) == "12 багов", "12 → «12 багов»"
            """,
            """
            def pluralize(n):
                word = "баг" if n == 1 else "бага" if 2 <= n <= 4 else "багов"
                return f"{n} {word}"
            """,
            xp=20),
    ),
    lesson(f"{P}-m2-l2", "Тернарник и списки", """
        # Тернарник внутри генератора списка

        Тернарник **меняет значение** каждого элемента:
        ```
        ["OK" if s == 200 else "ERR" for s in codes]
        ```

        А `if` **в конце** генератора — **фильтрует** элементы:
        ```
        [s for s in codes if s != 200]
        ```

        Не путай: `if ... else` стоит **перед** `for`, одиночный `if` — **после**.
        """,
        out(f"{P}-m2-l2-e1", "Что выведет программа?", """
            codes = [200, 404, 200, 500]
            print(["OK" if c == 200 else "ERR" for c in codes])
            print([c for c in codes if c != 200])
            """),
        out(f"{P}-m2-l2-e2", "Что выведет программа?", """
            nums = [3, -1, 0, -7]
            print([n if n > 0 else 0 for n in nums])
            """),
        cod(f"{P}-m2-l2-e3", t("""
            Напиши функцию `mark_results(results)`, которая превращает результаты тестов в понятные метки.

            - Получает: `results` — список из `True` (тест прошёл) и `False` (тест упал).
            - Возвращает: новый список той же длины, где вместо `True` стоит `"pass"`, а вместо `False` — `"fail"`.

            Примеры:
            ```
            mark_results([True, False, True])   # → ["pass", "fail", "pass"]
            mark_results([])                    # → []
            ```
            Реши одной строкой: генератор списка с тернарником внутри.
            """),
            """
            def mark_results(results):
                pass
            """,
            """
            def test_mixed():
                assert mark_results([True, False, True]) == ["pass", "fail", "pass"], f"Получено {mark_results([True, False, True])}"

            def test_empty():
                assert mark_results([]) == [], "Пустой список → []"
            """,
            """
            def mark_results(results):
                return ["pass" if r else "fail" for r in results]
            """),
        cod(f"{P}-m2-l2-e4", t("""
            Напиши функцию `censor(words, banned)`, которая скрывает запрещённые слова.

            - Получает: `words` — список слов; `banned` — список запрещённых слов.
            - Возвращает: новый список, где каждое запрещённое слово заменено на `"***"`, а остальные остались как были.

            Примеры:
            ```
            censor(["хороший", "плохой", "день"], ["плохой"])   # → ["хороший", "***", "день"]
            censor(["a", "b"], [])                               # → ["a", "b"]
            ```
            """),
            """
            def censor(words, banned):
                pass
            """,
            """
            def test_basic():
                assert censor(["хороший", "плохой", "день"], ["плохой"]) == ["хороший", "***", "день"], "плохой → ***"

            def test_nothing():
                assert censor(["a", "b"], []) == ["a", "b"], "Если запрещённых нет — список не меняется"
            """,
            """
            def censor(words, banned):
                return ["***" if w in banned else w for w in words]
            """),
        cod(f"{P}-m2-l2-e5", t("""
            Напиши функцию `fizzbuzz_list(n)` — FizzBuzz для всех чисел от 1 до `n` сразу.

            - Получает: `n` — целое положительное число.
            - Возвращает: список длины `n`, где для каждого числа `i` от 1 до `n` стоит:
              - `"FizzBuzz"` — если `i` делится на 15 (и на 3, и на 5);
              - `"Fizz"` — если делится на 3;
              - `"Buzz"` — если делится на 5;
              - иначе — само число `i` (**числом**, не строкой).

            Пример:
            ```
            fizzbuzz_list(5)    # → [1, 2, "Fizz", 4, "Buzz"]
            fizzbuzz_list(15)   # → [..., 14, "FizzBuzz"]   последний элемент
            ```
            Попробуй одним генератором списка с вложенным тернарником.
            """),
            """
            def fizzbuzz_list(n):
                pass
            """,
            """
            def test_15():
                expected = [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz", 11, "Fizz", 13, 14, "FizzBuzz"]
                assert fizzbuzz_list(15) == expected, f"Получено {fizzbuzz_list(15)}"
            """,
            """
            def fizzbuzz_list(n):
                return ["FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else i
                        for i in range(1, n + 1)]
            """,
            xp=20),
    ),
)

TOPIC = topic("ternary", "Тернарный оператор", "❓", "#ff9600",
              "Условие в одну строку: if-else как выражение", m1, m2, group="Python")
