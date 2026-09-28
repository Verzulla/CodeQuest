"""Тема «Цикл while», модуль 2 «while на практике» — задания. Теория — в _whl_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "whl"

m2 = module(f"{P}-m2", "while на практике", "⏱️", "Цифры числа, повторы с ожиданием, очереди и стеки, два указателя",

lesson(f"{P}-m2-l1", "Работа с цифрами числа",
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
    out(f"{P}-m2-l1-e6", "Что выведет программа?", """
        n = 12345
        count_even = 0
        while n:
            if n % 10 % 2 == 0:
                count_even += 1
            n //= 10
        print(count_even)
        """, hint="while n — пока число не ноль. Цифры идут с конца: 5, 4, 3, 2, 1."),
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
    cod(f"{P}-m2-l1-e7", t("""
        Напиши функцию `count_digits(n)` — количество цифр в целом числе **без** перевода в строку. У нуля одна цифра, знак минус не считается.

        Примеры:
        ```
        count_digits(12345)   # → 5
        count_digits(0)       # → 1
        count_digits(-42)     # → 2
        ```
        """),
        """
        def count_digits(n):
            pass
        """,
        """
        def test_values():
            assert [count_digits(n) for n in (12345, 0, -42, 7, 1000)] == [5, 1, 2, 1, 4], "Неверное количество цифр"

        def test_no_str():
            assert "str(" not in open("solution.py", encoding="utf-8").read(), "Реши без str()"
        """,
        """
        def count_digits(n):
            n = abs(n)
            count = 1
            while n >= 10:
                n //= 10
                count += 1
            return count
        """, hint="abs(n) убирает минус. Для 0 цикл while n > 0 не выполнится ни разу — учти это."),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `to_binary(n)` — запись неотрицательного числа в **двоичной** системе в виде строки. Без `bin` и `format`.

        Алгоритм: остаток от деления на 2 — очередная цифра **справа**; число делим на 2 нацело; повторяем, пока число больше 0.

        Примеры:
        ```
        to_binary(10)   # → "1010"
        to_binary(1)    # → "1"
        to_binary(0)    # → "0"
        ```
        """),
        """
        def to_binary(n):
            pass
        """,
        """
        def test_values():
            assert [to_binary(n) for n in (10, 1, 0, 2, 255)] == ["1010", "1", "0", "10", "11111111"], "Неверная двоичная запись"

        def test_no_bin():
            src = open("solution.py", encoding="utf-8").read()
            assert "bin(" not in src and "format" not in src and ":b" not in src, "Реши циклом, без bin/format"
        """,
        """
        def to_binary(n):
            if n == 0:
                return "0"
            result = ""
            while n > 0:
                result = str(n % 2) + result
                n //= 2
            return result
        """, hint="Новую цифру приписывай слева: result = str(n % 2) + result.", xp=20),
),

lesson(f"{P}-m2-l2", "Повторы и ожидания",
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
    out(f"{P}-m2-l2-e6", "Что выведет программа? Экспоненциальный откат.", """
        delay = 1
        waited = 0
        attempt = 0
        while attempt < 4:
            attempt += 1
            print("попытка", attempt, "ждём", delay)
            waited += delay
            delay *= 2
        print("всего ждали", waited)
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
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `poll_status(statuses)` — опрашивать статус задачи по очереди (`statuses` — что вернёт сервер на каждый опрос), пока он не станет конечным: `"done"` или `"failed"`.

        Вернуть пару `(итоговый_статус, число_опросов)`. Если опросы кончились, а конечного статуса не было — `("timeout", число_опросов)`.

        Примеры:
        ```
        poll_status(["queued", "running", "done", "x"])   # → ("done", 3)
        poll_status(["running", "running"])               # → ("timeout", 2)
        ```
        """),
        """
        def poll_status(statuses):
            pass
        """,
        """
        def test_values():
            got = [poll_status(["queued", "running", "done", "x"]), poll_status(["running", "running"]), poll_status(["failed"]), poll_status([])]
            assert got == [("done", 3), ("timeout", 2), ("failed", 1), ("timeout", 0)], f"Получено {got}"
        """,
        """
        def poll_status(statuses):
            polls = 0
            while polls < len(statuses):
                status = statuses[polls]
                polls += 1
                if status in ("done", "failed"):
                    return status, polls
            return "timeout", polls
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `retry_call(func, attempts)` — вызывать `func()` (без аргументов), пока вызов не пройдёт **без исключения**, но не больше `attempts` раз.

        - Успех — вернуть результат `func()`.
        - Все попытки упали — вернуть `None`.

        Используй `while` и `try/except Exception`.

        Пример (функция падает дважды, потом отвечает):
        ```
        calls = []
        def flaky():
            calls.append(1)
            if len(calls) < 3:
                raise ConnectionError("нет связи")
            return "ok"

        retry_call(flaky, 5)   # → "ok"  (3 вызова)
        ```
        """),
        """
        def retry_call(func, attempts):
            pass
        """,
        """
        def test_success():
            calls = []
            def flaky():
                calls.append(1)
                if len(calls) < 3:
                    raise ConnectionError("нет связи")
                return "ok"
            assert retry_call(flaky, 5) == "ok" and len(calls) == 3, f"Результат или число вызовов неверны: {len(calls)}"

        def test_fail():
            calls = []
            def broken():
                calls.append(1)
                raise ValueError("x")
            assert retry_call(broken, 2) is None and len(calls) == 2, "Все попытки упали — None, ровно attempts вызовов"
        """,
        """
        def retry_call(func, attempts):
            attempt = 0
            while attempt < attempts:
                attempt += 1
                try:
                    return func()
                except Exception:
                    pass
            return None
        """, hint="try: return func() — при исключении управление попадёт в except, и цикл сделает следующую попытку.", xp=20),
),

lesson(f"{P}-m2-l3", "Очереди и стеки",
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
    out(f"{P}-m2-l3-e6", "Что выведет программа? Стек переворачивает порядок.", """
        stack = []
        for ch in "abc":
            stack.append(ch)
        result = ""
        while stack:
            result += stack.pop()
        print(result)
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
    cod(f"{P}-m2-l3-e7", t("""
        Напиши функцию `serve_queue(queue, capacity)` — очередь к кассам: за один «такт» обслуживается до `capacity` человек **из начала** очереди. Вернуть, за сколько тактов очередь опустеет. Исходный список менять нельзя.

        Примеры:
        ```
        serve_queue(["a", "b", "c", "d", "e"], 2)   # → 3
        serve_queue([], 3)                          # → 0
        ```
        """),
        """
        def serve_queue(queue, capacity):
            pass
        """,
        """
        def test_values():
            src = ["a", "b", "c", "d", "e"]
            assert serve_queue(src, 2) == 3 and src == ["a", "b", "c", "d", "e"], "Неверно или исходная очередь изменилась"
            assert serve_queue([], 3) == 0 and serve_queue(["x"], 5) == 1 and serve_queue([1, 2, 3], 1) == 3, "Неверное число тактов"
        """,
        """
        def serve_queue(queue, capacity):
            queue = list(queue)
            ticks = 0
            while queue:
                queue = queue[capacity:]
                ticks += 1
            return ticks
        """, hint="Сделай копию list(queue). За такт отрезай первые capacity: queue = queue[capacity:]."),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `eval_rpn(tokens)` — вычислить выражение в **обратной польской записи** с помощью стека. Токены — строки: числа и операторы `+`, `-`, `*`.

        - число — положить в стек;
        - оператор — снять два верхних числа (сначала правое, потом левое), вычислить, результат положить обратно.

        В конце в стеке остаётся ответ.

        Пример:
        ```
        eval_rpn(["2", "3", "+", "4", "*"])   # → 20    ((2 + 3) * 4)
        eval_rpn(["10", "4", "-"])            # → 6
        ```
        """),
        """
        def eval_rpn(tokens):
            pass
        """,
        """
        def test_values():
            got = [eval_rpn(["2", "3", "+", "4", "*"]), eval_rpn(["10", "4", "-"]), eval_rpn(["7"]), eval_rpn(["5", "1", "2", "+", "4", "*", "+", "3", "-"])]
            assert got == [20, 6, 7, 14], f"Получено {got}"
        """,
        """
        def eval_rpn(tokens):
            stack = []
            i = 0
            while i < len(tokens):
                tok = tokens[i]
                i += 1
                if tok in ("+", "-", "*"):
                    right = stack.pop()
                    left = stack.pop()
                    if tok == "+":
                        stack.append(left + right)
                    elif tok == "-":
                        stack.append(left - right)
                    else:
                        stack.append(left * right)
                else:
                    stack.append(int(tok))
            return stack.pop()
        """, hint="Для «-» порядок важен: первым снимается ПРАВЫЙ операнд.", xp=25),
),

lesson(f"{P}-pointers", "Два указателя",
    out(f"{P}-pointers-e1", "Что выведет программа?", """
        s = "level"
        i, j = 0, len(s) - 1
        while i < j and s[i] == s[j]:
            i += 1
            j -= 1
        print(i, j, i >= j)
        """, hint="Указатели идут навстречу, пока символы совпадают. Встретились — значит палиндром."),
    out(f"{P}-pointers-e2", "Что выведет программа? Разворот списка на месте.", """
        xs = [1, 2, 3, 4, 5]
        i, j = 0, len(xs) - 1
        while i < j:
            xs[i], xs[j] = xs[j], xs[i]
            i += 1
            j -= 1
        print(xs)
        """),
    out(f"{P}-pointers-e3", "Что выведет программа? Слияние двух отсортированных списков.", """
        a, b = [1, 4, 7], [2, 3, 9]
        i = j = 0
        merged = []
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                merged.append(a[i])
                i += 1
            else:
                merged.append(b[j])
                j += 1
        merged += a[i:] + b[j:]
        print(merged)
        """, hint="Когда один список кончился, хвост второго дописывается целиком."),
    cod(f"{P}-pointers-e4", t("""
        Напиши функцию `is_palindrome(s)` — читается ли строка одинаково с обеих сторон. Используй **два указателя** и `while`, без срезов и `reversed`.

        Примеры:
        ```
        is_palindrome("level")   # → True
        is_palindrome("abca")    # → False
        is_palindrome("")        # → True
        ```
        """),
        """
        def is_palindrome(s):
            pass
        """,
        """
        def test_values():
            got = [is_palindrome(s) for s in ("level", "abca", "", "a", "abba", "ab")]
            assert got == [True, False, True, True, True, False], f"Получено {got}"

        def test_no_slice():
            src = open("solution.py", encoding="utf-8").read()
            assert "::" not in src and "reversed" not in src, "Реши двумя указателями"
        """,
        """
        def is_palindrome(s):
            i, j = 0, len(s) - 1
            while i < j:
                if s[i] != s[j]:
                    return False
                i += 1
                j -= 1
            return True
        """),
    cod(f"{P}-pointers-e5", t("""
        Напиши функцию `merge_sorted(a, b)` — слить два **отсортированных** списка в один отсортированный. Без `sorted` и `sort` — двумя указателями.

        Пример:
        ```
        merge_sorted([1, 4, 7], [2, 3, 9, 10])   # → [1, 2, 3, 4, 7, 9, 10]
        ```
        """),
        """
        def merge_sorted(a, b):
            pass
        """,
        """
        def test_values():
            got = [merge_sorted([1, 4, 7], [2, 3, 9, 10]), merge_sorted([], [1]), merge_sorted([1, 1], [1]), merge_sorted([], [])]
            assert got == [[1, 2, 3, 4, 7, 9, 10], [1], [1, 1, 1], []], f"Получено {got}"

        def test_no_sort():
            src = open("solution.py", encoding="utf-8").read().replace("merge_sorted", "")
            assert "sorted(" not in src and ".sort(" not in src, "Без sorted/sort"
        """,
        """
        def merge_sorted(a, b):
            i = j = 0
            result = []
            while i < len(a) and j < len(b):
                if a[i] <= b[j]:
                    result.append(a[i])
                    i += 1
                else:
                    result.append(b[j])
                    j += 1
            result.extend(a[i:])
            result.extend(b[j:])
            return result
        """, xp=20),
    cod(f"{P}-pointers-e6", t("""
        Напиши функцию `pair_with_sum_sorted(nums, target)` — в **отсортированном** списке найти пару чисел с суммой `target` за один проход двумя указателями (с начала и с конца). Вернуть пару `(a, b)` или `None`.

        - сумма меньше нужной — двигаем левый указатель вправо;
        - больше — правый влево.

        Примеры:
        ```
        pair_with_sum_sorted([1, 2, 4, 7, 11], 9)   # → (2, 7)
        pair_with_sum_sorted([1, 2], 10)            # → None
        ```
        """),
        """
        def pair_with_sum_sorted(nums, target):
            pass
        """,
        """
        def test_values():
            got = [pair_with_sum_sorted([1, 2, 4, 7, 11], 9), pair_with_sum_sorted([1, 2], 10), pair_with_sum_sorted([], 1), pair_with_sum_sorted([3, 3], 6)]
            assert got == [(2, 7), None, None, (3, 3)], f"Получено {got}"
        """,
        """
        def pair_with_sum_sorted(nums, target):
            i, j = 0, len(nums) - 1
            while i < j:
                s = nums[i] + nums[j]
                if s == target:
                    return (nums[i], nums[j])
                if s < target:
                    i += 1
                else:
                    j -= 1
            return None
        """, xp=20),
    cod(f"{P}-pointers-e7", t("""
        Напиши функцию `dedupe_sorted(nums)` — из **отсортированного** списка убрать повторы (новый список). Используй `while` с индексом: элемент добавляется, если он отличается от последнего добавленного.

        Пример:
        ```
        dedupe_sorted([1, 1, 2, 3, 3, 3])   # → [1, 2, 3]
        ```
        """),
        """
        def dedupe_sorted(nums):
            pass
        """,
        """
        def test_values():
            got = [dedupe_sorted([1, 1, 2, 3, 3, 3]), dedupe_sorted([]), dedupe_sorted([5]), dedupe_sorted([1, 2])]
            assert got == [[1, 2, 3], [], [5], [1, 2]], f"Получено {got}"

        def test_no_set():
            assert "set(" not in open("solution.py", encoding="utf-8").read(), "Реши циклом, без set"
        """,
        """
        def dedupe_sorted(nums):
            result = []
            i = 0
            while i < len(nums):
                if not result or nums[i] != result[-1]:
                    result.append(nums[i])
                i += 1
            return result
        """),
    cod(f"{P}-pointers-e8", t("""
        Напиши функцию `is_subsequence(small, big)` — можно ли получить строку `small` из `big`, **вычёркивая** символы (порядок сохраняется). Один указатель идёт по `small`, другой — по `big`.

        Примеры:
        ```
        is_subsequence("ace", "abcde")   # → True
        is_subsequence("aec", "abcde")   # → False
        is_subsequence("", "abc")        # → True
        ```
        """),
        """
        def is_subsequence(small, big):
            pass
        """,
        """
        def test_values():
            got = [is_subsequence("ace", "abcde"), is_subsequence("aec", "abcde"), is_subsequence("", "abc"), is_subsequence("a", ""), is_subsequence("abc", "abc")]
            assert got == [True, False, True, False, True], f"Получено {got}"
        """,
        """
        def is_subsequence(small, big):
            i = j = 0
            while i < len(small) and j < len(big):
                if small[i] == big[j]:
                    i += 1
                j += 1
            return i == len(small)
        """, hint="Указатель по big двигается всегда, по small — только при совпадении.", xp=20),
),
)
