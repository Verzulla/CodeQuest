"""Тема «Декораторы», модуль 2 «Практичные декораторы» — задания. Теория — в _dec_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "dec"

m2 = module(f"{P}-m2", "Практичные декораторы", "🛠️", "functools.wraps, логирование и замер времени, кэширование, повтор при ошибке",

lesson(f"{P}-wraps", "functools.wraps: сохраняем имя и описание",
    out(f"{P}-wraps-e1", "Что выведет программа? Без wraps.", """
        def deco(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        @deco
        def login(user):
            \"\"\"Войти в систему.\"\"\"
            return user

        print(login.__name__, login.__doc__)
        """, hint="login теперь — это wrapper, и имя у него wrapper."),
    out(f"{P}-wraps-e2", "Что выведет программа? С wraps.", """
        from functools import wraps

        def deco(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        @deco
        def login(user):
            \"\"\"Войти в систему.\"\"\"
            return user

        print(login.__name__, login.__doc__)
        print(login.__wrapped__("аня"))
        """, hint="__wrapped__ — ссылка на исходную функцию без обёртки."),
    out(f"{P}-wraps-e3", "Что выведет программа? Почему имя важно.", """
        from functools import wraps

        def plain(func):
            def wrapper():
                return func()
            return wrapper

        def nice(func):
            @wraps(func)
            def wrapper():
                return func()
            return wrapper

        @plain
        def test_login(): pass

        @plain
        def test_logout(): pass

        @nice
        def test_signup(): pass

        print([f.__name__ for f in [test_login, test_logout, test_signup]])
        """),
    cod(f"{P}-wraps-e4", t("""
        Исправь декоратор `trace` из заготовки: после декорирования функция должна сохранять своё имя (`__name__`) и описание (`__doc__`). Используй `functools.wraps`.
        """),
        """
        def trace(func):
            def wrapper(*args, **kwargs):
                print("вызов", func.__name__)
                return func(*args, **kwargs)
            return wrapper
        """,
        """
        def test_meta():
            @trace
            def add(a, b):
                \"\"\"Сложить.\"\"\"
                return a + b
            assert add.__name__ == "add" and add.__doc__ == "Сложить." and add(1, 2) == 3, "Имя и описание должны сохраниться"
        """,
        """
        from functools import wraps


        def trace(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print("вызов", func.__name__)
                return func(*args, **kwargs)
            return wrapper
        """),
    cod(f"{P}-wraps-e5", t("""
        Напиши декоратор `upper_result` (результат-строку перевести в верхний регистр) с `@wraps`. Затем функцию `undecorated(func)` — вернуть исходную функцию без обёртки (через `__wrapped__`), а если функция не задекорирована — её саму.
        """),
        """
        def upper_result(func):
            pass


        def undecorated(func):
            pass
        """,
        """
        def test_values():
            @upper_result
            def hi(name):
                return "hi " + name
            assert hi("аня") == "HI АНЯ" and hi.__name__ == "hi", "upper_result"
            assert undecorated(hi)("аня") == "hi аня", "Исходная функция"
            assert undecorated(len) is len, "Незадекорированная функция"
        """,
        """
        from functools import wraps


        def upper_result(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs).upper()
            return wrapper


        def undecorated(func):
            return getattr(func, "__wrapped__", func)
        """, hint="getattr(obj, 'имя', по_умолчанию)"),
    cod(f"{P}-wraps-e6", t("""
        Напиши декоратор `describe` с `@wraps`: добавляет к описанию функции строку `" [задекорировано]"`. Если описания нет (`None`) — описание становится `"[задекорировано]"`.
        """),
        """
        def describe(func):
            pass
        """,
        """
        def test_values():
            @describe
            def a():
                \"\"\"Функция A.\"\"\"
                return 1
            @describe
            def b():
                return 2
            assert a.__doc__ == "Функция A. [задекорировано]" and b.__doc__ == "[задекорировано]", f"{a.__doc__!r}, {b.__doc__!r}"
            assert a() == 1 and b.__name__ == "b", "Функция работает и сохраняет имя"
        """,
        """
        from functools import wraps


        def describe(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            if wrapper.__doc__ is None:
                wrapper.__doc__ = "[задекорировано]"
            else:
                wrapper.__doc__ += " [задекорировано]"
            return wrapper
        """),
    cod(f"{P}-wraps-e7", t("""
        Напиши декоратор `mark_slow` — **без обёртки**: он просто ставит функции атрибут `slow = True` и возвращает **ту же** функцию. И функцию `slow_tests(funcs)` — имена функций, у которых `slow` равно `True` (у непомеченных атрибута нет вообще).
        """),
        """
        def mark_slow(func):
            pass


        def slow_tests(funcs):
            pass
        """,
        """
        def test_values():
            def test_a(): pass
            def test_b(): pass
            original = test_b
            test_b = mark_slow(test_b)
            assert test_b is original, "Возвращается та же функция"
            assert slow_tests([test_a, test_b]) == ["test_b"] and slow_tests([]) == [], "slow_tests"
        """,
        """
        def mark_slow(func):
            func.slow = True
            return func


        def slow_tests(funcs):
            return [f.__name__ for f in funcs if getattr(f, "slow", False)]
        """, hint="Так устроены метки @pytest.mark.*"),
    cod(f"{P}-wraps-e8", t("""
        Напиши декоратор `deprecated` с `@wraps`: при **каждом** вызове добавляет в глобальный список `WARNINGS` строку `"<имя> устарела"` и возвращает результат функции.
        """),
        """
        WARNINGS = []


        def deprecated(func):
            pass
        """,
        """
        def test_values():
            WARNINGS.clear()
            @deprecated
            def old_api(x):
                return x * 2
            assert old_api(2) == 4 and old_api(3) == 6 and old_api.__name__ == "old_api", "Результат и имя"
            assert WARNINGS == ["old_api устарела", "old_api устарела"], WARNINGS
        """,
        """
        from functools import wraps

        WARNINGS = []


        def deprecated(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                WARNINGS.append(f"{func.__name__} устарела")
                return func(*args, **kwargs)
            return wrapper
        """),
),

lesson(f"{P}-logging", "Логирование и замер времени",
    out(f"{P}-logging-e1", "Что выведет программа?", """
        from functools import wraps

        def log(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(f"→ {func.__name__}{args}")
                result = func(*args, **kwargs)
                print(f"← {func.__name__} = {result}")
                return result
            return wrapper

        @log
        def add(a, b):
            return a + b

        total = add(2, 3)
        print("итог:", total)
        """),
    out(f"{P}-logging-e2", "Что выведет программа? Лог ошибок.", """
        from functools import wraps

        def log_errors(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"{func.__name__} упала: {type(e).__name__}")
                    raise
            return wrapper

        @log_errors
        def parse(text):
            return int(text)

        print(parse("5"))
        try:
            parse("x")
        except ValueError:
            print("ошибку поймали снаружи")
        """, hint="raise без аргументов пробрасывает пойманное исключение дальше."),
    out(f"{P}-logging-e3", "Что выведет программа? Замер времени с поддельными часами.", """
        from functools import wraps

        ticks = iter([10.0, 10.25, 20.0, 21.5])

        def fake_clock():
            return next(ticks)

        def timed(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = fake_clock()
                result = func(*args, **kwargs)
                print(f"{func.__name__}: {fake_clock() - start:.2f} с")
                return result
            return wrapper

        @timed
        def fast():
            return 1

        @timed
        def slow():
            return 2

        print(fast() + slow())
        """, hint="Настоящие часы давали бы разное время при каждом запуске — поэтому здесь подделка."),
    cod(f"{P}-logging-e4", t("""
        Напиши декоратор `logged`: каждый вызов добавляет в атрибут-список обёртки `log` кортеж `(args, kwargs, результат)`. Используй `@wraps`.

        ```
        @logged
        def add(a, b=0): return a + b
        add(1, b=2)
        add.log   # → [((1,), {"b": 2}, 3)]
        ```
        """),
        """
        def logged(func):
            pass
        """,
        """
        def test_values():
            @logged
            def add(a, b=0):
                return a + b
            add(1, b=2)
            add(5)
            assert add.log == [((1,), {"b": 2}, 3), ((5,), {}, 5)] and add.__name__ == "add", add.log
        """,
        """
        from functools import wraps


        def logged(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                wrapper.log.append((args, kwargs, result))
                return result
            wrapper.log = []
            return wrapper
        """),
    cod(f"{P}-logging-e5", t("""
        Напиши декоратор `timed`, который измеряет время выполнения функции через `time.perf_counter()` и сохраняет **последнее** измерение (в секундах) в атрибут обёртки `last_time`. Результат функции возвращается как обычно.
        """),
        """
        import time


        def timed(func):
            pass
        """,
        """
        import time as _t

        def test_values():
            @timed
            def nap():
                _t.sleep(0.05)
                return "ok"
            assert nap() == "ok" and nap.__name__ == "nap", "Результат и имя"
            assert 0.04 < nap.last_time < 1, f"last_time = {nap.last_time}"
        """,
        """
        import time
        from functools import wraps


        def timed(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                wrapper.last_time = time.perf_counter() - start
                return result
            wrapper.last_time = None
            return wrapper
        """, hint="perf_counter() — точные часы для замеров; разность двух показаний — прошедшее время."),
    cod(f"{P}-logging-e6", t("""
        Напиши декоратор `report`: печатает `PASS <имя>`, если функция отработала без исключений, и `FAIL <имя>: <текст ошибки>`, если выбросила `AssertionError`. Ошибку **не пробрасывать**; вернуть `True`/`False`.
        """),
        """
        def report(func):
            pass
        """,
        """
        import io, contextlib

        def test_values():
            @report
            def test_ok():
                assert 1 == 1
            @report
            def test_bad():
                assert 2 + 2 == 5, "математика сломалась"
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                r = (test_ok(), test_bad())
            assert r == (True, False), f"Возвращено {r}"
            assert buf.getvalue() == "PASS test_ok\\nFAIL test_bad: математика сломалась\\n", f"Напечатано: {buf.getvalue()!r}"
        """,
        """
        from functools import wraps


        def report(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    func(*args, **kwargs)
                except AssertionError as e:
                    print(f"FAIL {func.__name__}: {e}")
                    return False
                print(f"PASS {func.__name__}")
                return True
            return wrapper
        """),
    cod(f"{P}-logging-e7", t("""
        Напиши декоратор `log_errors`: если функция выбросила исключение, добавить в глобальный список `ERRORS` строку `"<имя>: <ТипОшибки>"` и **пробросить** исключение дальше (`raise`).
        """),
        """
        ERRORS = []


        def log_errors(func):
            pass
        """,
        """
        def test_values():
            ERRORS.clear()
            @log_errors
            def parse(t):
                return int(t)
            assert parse("5") == 5 and ERRORS == [], "Успех без записей"
            try:
                parse("x")
            except ValueError:
                pass
            else:
                assert False, "Исключение должно пробрасываться"
            assert ERRORS == ["parse: ValueError"], ERRORS
        """,
        """
        from functools import wraps

        ERRORS = []


        def log_errors(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    ERRORS.append(f"{func.__name__}: {type(e).__name__}")
                    raise
            return wrapper
        """),
    cod(f"{P}-logging-e8", t("""
        Напиши декоратор `call_stats`: обёртка хранит в атрибуте `stats` словарь `{"calls": N, "errors": M}` — сколько раз функцию вызывали и сколько раз она упала (любое `Exception`). Исключения пробрасываются.
        """),
        """
        def call_stats(func):
            pass
        """,
        """
        def test_values():
            @call_stats
            def inv(x):
                return 1 / x
            inv(1)
            inv(2)
            try:
                inv(0)
            except ZeroDivisionError:
                pass
            assert inv.stats == {"calls": 3, "errors": 1} and inv.__name__ == "inv", inv.stats
        """,
        """
        from functools import wraps


        def call_stats(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                wrapper.stats["calls"] += 1
                try:
                    return func(*args, **kwargs)
                except Exception:
                    wrapper.stats["errors"] += 1
                    raise
            wrapper.stats = {"calls": 0, "errors": 0}
            return wrapper
        """, xp=20),
),

lesson(f"{P}-cache", "Кэширование: memoize и lru_cache",
    out(f"{P}-cache-e1", "Что выведет программа?", """
        from functools import wraps

        def memoize(func):
            cache = {}
            @wraps(func)
            def wrapper(n):
                if n not in cache:
                    print("считаю", n)
                    cache[n] = func(n)
                return cache[n]
            return wrapper

        @memoize
        def square(n):
            return n * n

        print(square(4), square(4), square(5))
        """, hint="Второй вызов с тем же аргументом берёт ответ из словаря."),
    out(f"{P}-cache-e2", "Что выведет программа? lru_cache.", """
        from functools import lru_cache

        calls = 0

        @lru_cache(maxsize=None)
        def fib(n):
            global calls
            calls += 1
            return n if n < 2 else fib(n - 1) + fib(n - 2)

        print(fib(30), calls)
        info = fib.cache_info()
        print(info.hits, info.misses)
        """, hint="Без кэша fib(30) вызвался бы больше миллиона раз."),
    out(f"{P}-cache-e3", "Что выведет программа? Ограничение размера и сброс.", """
        from functools import lru_cache

        @lru_cache(maxsize=2)
        def load(name):
            print("загрузка", name)
            return name.upper()

        load("a")
        load("b")
        load("a")
        load("c")
        load("b")
        load.cache_clear()
        load("a")
        """, hint="При переполнении выкидывается то, что дольше всех не использовали."),
    cod(f"{P}-cache-e4", t("""
        Напиши декоратор `memoize` для функций **с одним** хешируемым аргументом: результаты хранятся в словаре, повторный вызов с тем же аргументом не вызывает функцию.
        """),
        """
        def memoize(func):
            pass
        """,
        """
        def test_values():
            calls = []
            @memoize
            def slow_square(n):
                calls.append(n)
                return n * n
            assert [slow_square(x) for x in [2, 3, 2, 2, 3]] == [4, 9, 4, 4, 9] and calls == [2, 3], f"calls = {calls}"
        """,
        """
        from functools import wraps


        def memoize(func):
            cache = {}

            @wraps(func)
            def wrapper(arg):
                if arg not in cache:
                    cache[arg] = func(arg)
                return cache[arg]
            return wrapper
        """),
    cod(f"{P}-cache-e5", t("""
        Напиши декоратор `memoize` для функций с **любым количеством позиционных** аргументов (ключ кэша — кортеж `args`). Обёртка хранит словарь в атрибуте `cache`.
        """),
        """
        def memoize(func):
            pass
        """,
        """
        def test_values():
            calls = []
            @memoize
            def add(a, b):
                calls.append((a, b))
                return a + b
            assert add(1, 2) == 3 and add(1, 2) == 3 and add(2, 1) == 3 and calls == [(1, 2), (2, 1)], calls
            assert add.cache == {(1, 2): 3, (2, 1): 3}, add.cache
        """,
        """
        from functools import wraps


        def memoize(func):
            @wraps(func)
            def wrapper(*args):
                if args not in wrapper.cache:
                    wrapper.cache[args] = func(*args)
                return wrapper.cache[args]
            wrapper.cache = {}
            return wrapper
        """),
    cod(f"{P}-cache-e6", t("""
        Напиши функцию `count_paths(rows, cols)` — количество путей из левого верхнего угла сетки в правый нижний, если можно ходить только вправо и вниз. Формула рекурсии: `count_paths(r, c) = count_paths(r-1, c) + count_paths(r, c-1)`, а для `r == 1` или `c == 1` путь один. Используй `@lru_cache`, иначе большие сетки будут считаться вечно.

        ```
        count_paths(2, 2)   # → 2
        count_paths(3, 3)   # → 6
        ```
        """),
        """
        def count_paths(rows, cols):
            pass
        """,
        """
        def test_values():
            assert count_paths(2, 2) == 2 and count_paths(3, 3) == 6 and count_paths(1, 5) == 1, "Малые сетки"
            assert count_paths(18, 18) == 2333606220, "Большая сетка"
            assert "lru_cache" in open("solution.py", encoding="utf-8").read() or "cache" in open("solution.py", encoding="utf-8").read(), "Используй кэш"
        """,
        """
        from functools import lru_cache


        @lru_cache(maxsize=None)
        def count_paths(rows, cols):
            if rows == 1 or cols == 1:
                return 1
            return count_paths(rows - 1, cols) + count_paths(rows, cols - 1)
        """),
    cod(f"{P}-cache-e7", t("""
        Напиши декоратор `memoize_with_hits`: как обычный memoize по `args`, но обёртка ведёт атрибуты `hits` (ответ взят из кэша) и `misses` (функцию пришлось вызвать), а метод-атрибут `clear()` очищает кэш и обнуляет счётчики.
        """),
        """
        def memoize_with_hits(func):
            pass
        """,
        """
        def test_values():
            @memoize_with_hits
            def sq(n):
                return n * n
            sq(2); sq(2); sq(3); sq(2)
            assert (sq.hits, sq.misses) == (2, 2), f"hits={sq.hits}, misses={sq.misses}"
            sq.clear()
            sq(2)
            assert (sq.hits, sq.misses) == (0, 1), "После clear"
        """,
        """
        from functools import wraps


        def memoize_with_hits(func):
            cache = {}

            @wraps(func)
            def wrapper(*args):
                if args in cache:
                    wrapper.hits += 1
                else:
                    wrapper.misses += 1
                    cache[args] = func(*args)
                return cache[args]

            def clear():
                cache.clear()
                wrapper.hits = 0
                wrapper.misses = 0

            wrapper.clear = clear
            clear()
            return wrapper
        """),
    cod(f"{P}-cache-e8", t("""
        Напиши декоратор `cache_last`: помнит **только последний** вызов. Если аргументы (`args`) совпадают с предыдущими — вернуть сохранённый результат, иначе вызвать функцию и запомнить новые аргументы и результат.
        """),
        """
        def cache_last(func):
            pass
        """,
        """
        def test_values():
            calls = []
            @cache_last
            def f(x):
                calls.append(x)
                return x * 10
            assert [f(1), f(1), f(2), f(1), f(1)] == [10, 10, 20, 10, 10] and calls == [1, 2, 1], calls
        """,
        """
        from functools import wraps


        def cache_last(func):
            last_args = None
            last_result = None
            has_value = False

            @wraps(func)
            def wrapper(*args):
                nonlocal last_args, last_result, has_value
                if not has_value or args != last_args:
                    last_result = func(*args)
                    last_args = args
                    has_value = True
                return last_result
            return wrapper
        """, xp=20),
),

lesson(f"{P}-retry", "Повтор при ошибке",
    out(f"{P}-retry-e1", "Что выведет программа?", """
        from functools import wraps

        def retry3(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(1, 4):
                    try:
                        return func(*args, **kwargs)
                    except ConnectionError:
                        print("попытка", attempt, "не удалась")
                raise ConnectionError("сервер недоступен")
            return wrapper

        answers = iter([ConnectionError, ConnectionError, "200 OK"])

        @retry3
        def request():
            a = next(answers)
            if a is ConnectionError:
                raise ConnectionError
            return a

        print(request())
        """),
    out(f"{P}-retry-e2", "Что выведет программа? Все попытки неудачны.", """
        from functools import wraps

        def retry3(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                last = None
                for attempt in range(3):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last = e
                raise last
            return wrapper

        calls = 0

        @retry3
        def broken():
            global calls
            calls += 1
            raise TimeoutError(f"таймаут #{calls}")

        try:
            broken()
        except TimeoutError as e:
            print(e, calls)
        """, hint="Пробрасываем последнюю ошибку."),
    out(f"{P}-retry-e3", "Что выведет программа? Какие ошибки повторять.", """
        from functools import wraps

        def retry_network(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for _ in range(3):
                    try:
                        return func(*args, **kwargs)
                    except ConnectionError:
                        print("сеть, повтор")
                return None
            return wrapper

        @retry_network
        def bad_request():
            raise ValueError("неверные данные")

        try:
            bad_request()
        except ValueError as e:
            print("сразу:", e)
        """, hint="Повторять имеет смысл только временные сбои."),
    cod(f"{P}-retry-e4", t("""
        Напиши декоратор `retry3`: вызвать функцию до 3 раз, пока она выбрасывает `ConnectionError`. Если успешно — вернуть результат; если все 3 попытки неудачны — пробросить последнюю ошибку.
        """),
        """
        def retry3(func):
            pass
        """,
        """
        def test_values():
            state = {"n": 0}
            @retry3
            def flaky():
                state["n"] += 1
                if state["n"] < 3:
                    raise ConnectionError("сбой")
                return "ok"
            assert flaky() == "ok" and state["n"] == 3, "Третья попытка успешна"
            state["n"] = -10
            try:
                flaky()
            except ConnectionError:
                assert state["n"] == -7, f"Ровно 3 попытки, n={state['n']}"
                return
            assert False, "Нужно пробросить ConnectionError"
        """,
        """
        from functools import wraps


        def retry3(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(3):
                    try:
                        return func(*args, **kwargs)
                    except ConnectionError:
                        if attempt == 2:
                            raise
            return wrapper
        """),
    cod(f"{P}-retry-e5", t("""
        Напиши декоратор `retry3_log` — как `retry3` (до 3 попыток при `ConnectionError`), но номера неудачных попыток записываются в атрибут-список обёртки `failed_attempts` (1, 2, 3). Список общий для всех вызовов.
        """),
        """
        def retry3_log(func):
            pass
        """,
        """
        def test_values():
            answers = iter([ConnectionError, "a", ConnectionError, ConnectionError, "b"])
            @retry3_log
            def req():
                x = next(answers)
                if x is ConnectionError:
                    raise ConnectionError
                return x
            assert req() == "a" and req() == "b", "Результаты"
            assert req.failed_attempts == [1, 1, 2], req.failed_attempts
        """,
        """
        from functools import wraps


        def retry3_log(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(1, 4):
                    try:
                        return func(*args, **kwargs)
                    except ConnectionError:
                        wrapper.failed_attempts.append(attempt)
                        if attempt == 3:
                            raise
            wrapper.failed_attempts = []
            return wrapper
        """),
    cod(f"{P}-retry-e6", t("""
        Напиши декоратор `fallback_none`: если функция выбросила `KeyError` или `IndexError`, вернуть `None`. Другие ошибки пробрасываются.
        """),
        """
        def fallback_none(func):
            pass
        """,
        """
        def test_values():
            @fallback_none
            def get(data, key):
                return data[key]
            assert get({"a": 1}, "a") == 1 and get({}, "x") is None and get([1], 5) is None, "Перехват"
            try:
                get(None, 1)
            except TypeError:
                return
            assert False, "TypeError должен пробрасываться"
        """,
        """
        from functools import wraps


        def fallback_none(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except (KeyError, IndexError):
                    return None
            return wrapper
        """),
    cod(f"{P}-retry-e7", t("""
        Напиши декоратор `until_true`: вызывает функцию до 5 раз, пока она не вернёт истинное значение (так ждут, пока элемент появится на странице). Вернуть первое истинное значение; если за 5 попыток его нет — `TimeoutError("не дождались")`.
        """),
        """
        def until_true(func):
            pass
        """,
        """
        def test_values():
            answers = iter([None, "", 0, "элемент", "лишнее"])
            @until_true
            def find():
                return next(answers)
            assert find() == "элемент", "Первое истинное значение"
            calls = []
            @until_true
            def never():
                calls.append(1)
                return False
            try:
                never()
            except TimeoutError as e:
                assert str(e) == "не дождались" and len(calls) == 5, f"Попыток: {len(calls)}"
                return
            assert False, "Нужен TimeoutError"
        """,
        """
        from functools import wraps


        def until_true(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for _ in range(5):
                    result = func(*args, **kwargs)
                    if result:
                        return result
                raise TimeoutError("не дождались")
            return wrapper
        """),
    cod(f"{P}-retry-e8", t("""
        Напиши декоратор `retry_with_delays`: до 4 попыток при `ConnectionError`; перед 2-й, 3-й и 4-й попытками «ждать» 1, 2 и 4 секунды — но вместо настоящего `time.sleep` вызывай функцию `sleep(seconds)` из заготовки (в тестах её подменят). Все попытки неудачны — пробросить последнюю ошибку.
        """),
        """
        import time


        def sleep(seconds):
            time.sleep(seconds)


        def retry_with_delays(func):
            pass
        """,
        """
        def test_values():
            waits = []
            retry_with_delays.__globals__["sleep"] = waits.append
            state = {"n": 0}
            @retry_with_delays
            def req():
                state["n"] += 1
                if state["n"] < 3:
                    raise ConnectionError
                return "ok"
            assert req() == "ok" and waits == [1, 2], f"waits = {waits}"
            waits.clear()
            @retry_with_delays
            def dead():
                raise ConnectionError("нет сети")
            try:
                dead()
            except ConnectionError:
                assert waits == [1, 2, 4], f"waits = {waits}"
                return
            assert False, "Нужно пробросить ConnectionError"
        """,
        """
        import time
        from functools import wraps


        def sleep(seconds):
            time.sleep(seconds)


        def retry_with_delays(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                delays = [1, 2, 4]
                for attempt in range(4):
                    try:
                        return func(*args, **kwargs)
                    except ConnectionError:
                        if attempt == 3:
                            raise
                        sleep(delays[attempt])
            return wrapper
        """, xp=25),
),
)
