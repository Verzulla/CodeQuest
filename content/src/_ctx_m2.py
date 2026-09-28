"""Тема «Контекстные менеджеры», модуль 2 «contextlib» — задания. Теория — в _ctx_t2.py.

Слаги ctx-m2-l1, ctx-m2-l2 унаследованы от старой темы — так сохраняется прогресс."""
from ._lib import cod, lesson, module, out, t

P = "ctx"

m2 = module(f"{P}-m2", "contextlib", "🧰", "@contextmanager, ошибки в генераторных менеджерах, suppress, redirect_stdout, ExitStack, closing, nullcontext",

lesson(f"{P}-m2-l1", "@contextmanager",
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
            from contextlib import contextmanager

            @contextmanager
            def step(name):
                print("▶", name)
                yield
                print("✔", name)

            with step("логин"):
                print("вводим пароль")
            """),
    out(f"{P}-m2-l1-e2", "Что выведет программа?", """
            from contextlib import contextmanager

            @contextmanager
            def temp_user():
                user = {"name": "test_user"}
                print("создан")
                try:
                    yield user
                finally:
                    print("удалён")

            try:
                with temp_user() as u:
                    print(u["name"])
                    raise RuntimeError("тест упал")
            except RuntimeError as e:
                print("ошибка:", e)
            """, hint="finally выполнится до того, как исключение поймает внешний except."),
    cod(f"{P}-m2-l1-e3", t("""
            Напиши через декоратор `@contextmanager` функцию `tag(name)`, которая оборачивает вывод в HTML-тег.

            - Получает: `name` — имя тега, например `"b"`.
            - При входе в `with` печатает открывающий тег `<name>`, при выходе — закрывающий `</name>`.

            Пример:
            ```
            with tag("b"):
                print("жирный")
            ```
            Вывод:
            ```
            <b>
            жирный
            </b>
            ```
            Внутри функции: `print` → `yield` → `print`.
            """),
            """
            from contextlib import contextmanager

            # напиши tag здесь
            """,
            """
            def test_output():
                def body():
                    with tag("b"):
                        print("жирный")
                assert capture(body).split() == ["<b>", "жирный", "</b>"], f"Напечатано: {capture(body)!r}"
            """,
            """
            from contextlib import contextmanager

            @contextmanager
            def tag(name):
                print(f"<{name}>")
                yield
                print(f"</{name}>")
            """),
    cod(f"{P}-m2-l1-e4", t("""
            Допиши через `@contextmanager` функцию `temp_list_item(items, value)` — временно добавить элемент в список.

            - Получает: `items` — список; `value` — значение.
            - При входе в `with` добавляет `value` в конец `items` и отдаёт `value` через `yield` (оно попадёт в переменную после `as`).
            - При выходе удаляет `value` из списка — **обязательно, даже если внутри блока случилась ошибка**.

            Пример:
            ```
            data = [1]
            with temp_list_item(data, 99) as v:
                v      # → 99
                data   # → [1, 99]
            data       # → [1]
            ```
            Чтобы удаление выполнилось и при ошибке, оберни `yield` в `try/finally`.
            """),
            """
            from contextlib import contextmanager

            @contextmanager
            def temp_list_item(items, value):
                pass
            """,
            """
            def test_normal():
                data = [1]
                with temp_list_item(data, 99) as v:
                    assert v == 99 and data == [1, 99], "Внутри with значение должно быть в списке"
                assert data == [1], "После with значение должно удалиться"

            def test_error():
                data = []
                try:
                    with temp_list_item(data, "x"):
                        raise ValueError
                except ValueError:
                    pass
                assert data == [], "Даже при ошибке значение должно удалиться — используй try/finally"
            """,
            """
            from contextlib import contextmanager

            @contextmanager
            def temp_list_item(items, value):
                items.append(value)
                try:
                    yield value
                finally:
                    items.remove(value)
            """,
            xp=20),
    cod(f"{P}-m2-l1-e5", t("""
            Допиши через `@contextmanager` функцию `timer(results)` — секундомер для блока кода.

            - Получает: `results` — список, куда записывать замеры.
            - Засекает время при входе в `with` и при выходе, а разницу (число секунд, `float`) добавляет в `results`.
            - Замер записывается **даже если внутри блока была ошибка**.

            Пример:
            ```
            res = []
            with timer(res):
                sum(range(10000))
            res   # → [0.00021...]  один замер, число ≥ 0
            ```
            Текущее время для замеров — `time.perf_counter()`. Для записи при ошибке — `try/finally` вокруг `yield`.
            """),
            """
            import time
            from contextlib import contextmanager

            @contextmanager
            def timer(results):
                pass
            """,
            """
            def test_records():
                res = []
                with timer(res):
                    sum(range(10000))
                assert len(res) == 1 and isinstance(res[0], float) and res[0] >= 0, f"В results: {res}"

            def test_on_error():
                res = []
                try:
                    with timer(res):
                        raise KeyError
                except KeyError:
                    pass
                assert len(res) == 1, "Время должно записаться и при ошибке"
            """,
            """
            import time
            from contextlib import contextmanager

            @contextmanager
            def timer(results):
                start = time.perf_counter()
                try:
                    yield
                finally:
                    results.append(time.perf_counter() - start)
            """,
            xp=20),
    out(f"{P}-m2-l1-e6", "Что выведет программа? Что попадает в as.", """
        from contextlib import contextmanager

        @contextmanager
        def opened(name):
            print("открываю", name)
            yield name.upper()
            print("закрываю", name)

        with opened("db") as handle:
            print("работаю с", handle)
        print(handle)
        """, hint="Значение после yield попадает в переменную после as."),
    cod(f"{P}-m2-l1-e7", t("""
        Напиши через `@contextmanager` функцию `section(log, title)`: при входе добавляет в список `log` строку `"== title =="`, при выходе — `"== конец =="`. Внутри блока ничего не отдаёт (`yield` без значения).
        """),
        """
        from contextlib import contextmanager
        """,
        """
        def test_values():
            log = []
            with section(log, "Вход"):
                log.append("шаг")
            assert log == ["== Вход ==", "шаг", "== конец =="], log
        """,
        """
        from contextlib import contextmanager


        @contextmanager
        def section(log, title):
            log.append(f"== {title} ==")
            yield
            log.append("== конец ==")
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши через `@contextmanager` функцию `collector()` — отдаёт в `as` **новый пустой список**, а после выхода из блока сортирует его на месте.

        ```
        with collector() as items:
            items.append(3); items.append(1)
        items   # → [1, 3]
        ```
        """),
        """
        from contextlib import contextmanager
        """,
        """
        def test_values():
            with collector() as items:
                items.extend([3, 1, 2])
                assert items == [3, 1, 2], "Внутри блока — без сортировки"
            assert items == [1, 2, 3], items
            with collector() as other:
                pass
            assert other == [] and other is not items, "Каждый раз новый список"
        """,
        """
        from contextlib import contextmanager


        @contextmanager
        def collector():
            items = []
            yield items
            items.sort()
        """, xp=20),
),

lesson(f"{P}-gen-errors", "Ошибки в @contextmanager",
    out(f"{P}-gen-errors-e1", "Что выведет программа? Без try уборка теряется.", """
        from contextlib import contextmanager

        @contextmanager
        def resource():
            print("взял")
            yield
            print("вернул")

        try:
            with resource():
                raise ValueError("сбой")
        except ValueError:
            print("ошибка")
        """, hint="Исключение возникает прямо в точке yield — код после yield не выполнится."),
    out(f"{P}-gen-errors-e2", "Что выведет программа? try/finally спасает.", """
        from contextlib import contextmanager

        @contextmanager
        def resource():
            print("взял")
            try:
                yield
            finally:
                print("вернул")

        try:
            with resource():
                raise ValueError("сбой")
        except ValueError:
            print("ошибка")
        """),
    out(f"{P}-gen-errors-e3", "Что выведет программа? Поймать ошибку в менеджере.", """
        from contextlib import contextmanager

        @contextmanager
        def soft(name):
            try:
                yield
            except ZeroDivisionError as e:
                print(f"{name}: поймал {e}")
            else:
                print(f"{name}: без ошибок")

        with soft("A"):
            1 / 0
        with soft("B"):
            pass
        print("дальше")
        """, hint="except вокруг yield работает как return True в __exit__."),
    cod(f"{P}-gen-errors-e4", t("""
        Напиши через `@contextmanager` функцию `borrowed(pool)`: берёт последний элемент из списка `pool` (`pop()`), отдаёт его в `as` и **обязательно** возвращает обратно (`append`) после блока — даже если внутри была ошибка.
        """),
        """
        from contextlib import contextmanager
        """,
        """
        def test_values():
            pool = ["conn1", "conn2"]
            with borrowed(pool) as c:
                assert c == "conn2" and pool == ["conn1"], "Взяли последний"
            assert pool == ["conn1", "conn2"], "Вернули"
            try:
                with borrowed(pool):
                    raise RuntimeError
            except RuntimeError:
                pass
            assert pool == ["conn1", "conn2"], "Вернули и после ошибки"
        """,
        """
        from contextlib import contextmanager


        @contextmanager
        def borrowed(pool):
            item = pool.pop()
            try:
                yield item
            finally:
                pool.append(item)
        """),
    cod(f"{P}-gen-errors-e5", t("""
        Напиши через `@contextmanager` функцию `ignore(*exc_types)` — аналог `suppress`: глушит перечисленные исключения.
        """),
        """
        from contextlib import contextmanager
        """,
        """
        def test_values():
            with ignore(KeyError, IndexError):
                [][1]
            with ignore(KeyError):
                pass
            try:
                with ignore(KeyError):
                    1 / 0
            except ZeroDivisionError:
                return
            assert False, "Чужие ошибки не глушить"
        """,
        """
        from contextlib import contextmanager


        @contextmanager
        def ignore(*exc_types):
            try:
                yield
            except exc_types:
                pass
        """),
    cod(f"{P}-gen-errors-e6", t("""
        Напиши через `@contextmanager` функцию `step(log, name)` — шаг теста для отчёта: добавляет в `log` строку `"PASS name"`, если блок прошёл без ошибок, или `"FAIL name: текст"` при `AssertionError`. Ошибку **пробросить** дальше (`raise`).
        """),
        """
        from contextlib import contextmanager
        """,
        """
        def test_values():
            log = []
            with step(log, "открыть"):
                pass
            try:
                with step(log, "войти"):
                    assert False, "нет кнопки"
            except AssertionError:
                pass
            else:
                assert False, "Ошибка должна пробрасываться"
            assert log == ["PASS открыть", "FAIL войти: нет кнопки"], log
        """,
        """
        from contextlib import contextmanager


        @contextmanager
        def step(log, name):
            try:
                yield
            except AssertionError as e:
                log.append(f"FAIL {name}: {e}")
                raise
            log.append(f"PASS {name}")
        """),
    cod(f"{P}-gen-errors-e7", t("""
        Напиши через `@contextmanager` функцию `temp_file(path, text)`: создаёт файл с текстом, отдаёт путь в `as`, а после блока **всегда** удаляет файл (если он ещё существует).
        """),
        """
        import os
        from contextlib import contextmanager
        """,
        """
        import os

        def test_values():
            with temp_file("tmp_ctx.txt", "данные") as p:
                assert open(p, encoding="utf-8").read() == "данные", "Файл создан"
            assert not os.path.exists("tmp_ctx.txt"), "Файл удалён"
            try:
                with temp_file("tmp_ctx2.txt", "x"):
                    raise ValueError
            except ValueError:
                pass
            assert not os.path.exists("tmp_ctx2.txt"), "Удалён и после ошибки"
            with temp_file("tmp_ctx3.txt", "x") as p:
                os.remove(p)
        """,
        """
        import os
        from contextlib import contextmanager


        @contextmanager
        def temp_file(path, text):
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            try:
                yield path
            finally:
                if os.path.exists(path):
                    os.remove(path)
        """),
    cod(f"{P}-gen-errors-e8", t("""
        Напиши через `@contextmanager` функцию `translate(from_exc, to_exc, message)`: если внутри блока возникло исключение типа `from_exc`, выбросить вместо него `to_exc(message)`, связав с исходным (`raise ... from e`).
        """),
        """
        from contextlib import contextmanager
        """,
        """
        def test_values():
            try:
                with translate(KeyError, LookupError, "нет пользователя"):
                    {}["anna"]
            except LookupError as e:
                assert str(e) == "нет пользователя" and isinstance(e.__cause__, KeyError) and type(e) is LookupError, "Перевод ошибки"
            else:
                assert False, "Нужен LookupError"
            with translate(KeyError, LookupError, "x"):
                pass
        """,
        """
        from contextlib import contextmanager


        @contextmanager
        def translate(from_exc, to_exc, message):
            try:
                yield
            except from_exc as e:
                raise to_exc(message) from e
        """, xp=20),
),

lesson(f"{P}-m2-l2", "Готовые менеджеры: suppress, redirect_stdout, ExitStack",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
            from contextlib import suppress

            with suppress(KeyError):
                print("до")
                {}["x"]
                print("после")
            print("дальше")
            """, hint="После исключения остаток блока with не выполняется."),
    out(f"{P}-m2-l2-e2", "Что выведет программа?", """
            import io
            from contextlib import redirect_stdout

            buf = io.StringIO()
            with redirect_stdout(buf):
                print("секрет")
            print("перехвачено:", buf.getvalue().strip())
            """),
    out(f"{P}-m2-l2-e3", "В каком порядке закрываются менеджеры?", """
            from contextlib import contextmanager, ExitStack

            @contextmanager
            def res(name):
                print("открыл", name)
                yield
                print("закрыл", name)

            with ExitStack() as stack:
                for name in ["БД", "браузер"]:
                    stack.enter_context(res(name))
                print("тест")
            """),
    cod(f"{P}-m2-l2-e4", t("""
            Допиши функцию `get_output(func)`, которая перехватывает всё, что печатает другая функция.

            - Получает: `func` — функцию без аргументов, которая что-то печатает через `print`.
            - Вызывает её, но вывод не попадает на экран, а собирается в строку.
            - Возвращает: эту строку — **ровно** то, что было напечатано, включая переводы строк.

            Пример:
            ```
            def hello():
                print("привет")
                print("мир")

            get_output(hello)   # → "привет\\nмир\\n"
            ```
            Используй `io.StringIO()` как «буфер» и `with redirect_stdout(буфер):`. Содержимое буфера — `.getvalue()`.
            """),
            """
            import io
            from contextlib import redirect_stdout

            def get_output(func):
                pass
            """,
            """
            def test_output():
                def hello():
                    print("привет")
                    print("мир")
                assert get_output(hello) == "привет\\nмир\\n", f"Получено {get_output(hello)!r}"
            """,
            """
            import io
            from contextlib import redirect_stdout

            def get_output(func):
                buf = io.StringIO()
                with redirect_stdout(buf):
                    func()
                return buf.getvalue()
            """),
    cod(f"{P}-m2-l2-e5", t("""
            Допиши функцию `parse_ints(strings)`, которая превращает строки в числа и пропускает мусор.

            - Получает: `strings` — список строк.
            - Возвращает: список целых чисел из тех строк, которые удалось превратить в число через `int()`. Строки, на которых `int()` падает с `ValueError`, пропускаются.

            Пример:
            ```
            parse_ints(["1", "abc", "30", "", "-4"])   # → [1, 30, -4]
            ```
            Вместо `try/except` используй `with suppress(ValueError):` вокруг преобразования.
            """),
            """
            from contextlib import suppress

            def parse_ints(strings):
                pass
            """,
            """
            def test_parse():
                assert parse_ints(["1", "abc", "30", "", "-4"]) == [1, 30, -4], f"Получено {parse_ints(['1', 'abc', '30', '', '-4'])}"
            """,
            """
            from contextlib import suppress

            def parse_ints(strings):
                result = []
                for s in strings:
                    with suppress(ValueError):
                        result.append(int(s))
                return result
            """),
    out(f"{P}-m2-l2-e6", "Что выведет программа? redirect_stderr.", """
        import io
        import sys
        from contextlib import redirect_stderr

        err = io.StringIO()
        with redirect_stderr(err):
            print("предупреждение", file=sys.stderr)
            print("обычный вывод")
        print("stderr:", err.getvalue().strip())
        """),
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `open_all(paths)` — открыть все файлы из списка через `ExitStack`, прочитать и вернуть список содержимого. Все файлы должны закрыться после выхода.
        """),
        """
        from contextlib import ExitStack


        def open_all(paths):
            pass
        """,
        """
        def test_values():
            for i in range(3):
                with open(f"es{i}.txt", "w", encoding="utf-8") as f:
                    f.write(str(i))
            assert open_all([f"es{i}.txt" for i in range(3)]) == ["0", "1", "2"] and open_all([]) == [], "Неверный результат"
            assert "ExitStack" in open("solution.py", encoding="utf-8").read(), "Используй ExitStack"
        """,
        """
        from contextlib import ExitStack


        def open_all(paths):
            with ExitStack() as stack:
                files = [stack.enter_context(open(p, encoding="utf-8")) for p in paths]
                return [f.read() for f in files]
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `with_cleanups(actions)` — `actions` — список функций-уборщиков. Зарегистрируй их через `ExitStack().callback(...)`, внутри блока ничего не делай. Функции должны вызваться при выходе **в обратном порядке**. Вернуть `None`.
        """),
        """
        from contextlib import ExitStack


        def with_cleanups(actions):
            pass
        """,
        """
        def test_values():
            log = []
            with_cleanups([lambda: log.append("a"), lambda: log.append("b"), lambda: log.append("c")])
            assert log == ["c", "b", "a"], log
        """,
        """
        from contextlib import ExitStack


        def with_cleanups(actions):
            with ExitStack() as stack:
                for action in actions:
                    stack.callback(action)
        """, hint="stack.callback(функция) — вызвать её при выходе из with.", xp=20),
),

lesson(f"{P}-stdlib", "Менеджеры стандартной библиотеки",
    out(f"{P}-stdlib-e1", "Что выведет программа? closing.", """
        from contextlib import closing

        class Connection:
            def __init__(self):
                self.open = True

            def query(self):
                return "данные"

            def close(self):
                self.open = False
                print("соединение закрыто")

        with closing(Connection()) as conn:
            print(conn.query())
        print(conn.open)
        """, hint="closing превращает любой объект с методом close() в менеджер."),
    out(f"{P}-stdlib-e2", "Что выведет программа? nullcontext.", """
        from contextlib import nullcontext

        def process(data, lock=None):
            with lock if lock is not None else nullcontext():
                return sum(data)

        print(process([1, 2, 3]))
        with nullcontext("значение") as v:
            print(v)
        """, hint="nullcontext — менеджер, который ничего не делает. Удобен как заглушка."),
    out(f"{P}-stdlib-e3", "Что выведет программа? chdir и localcontext.", """
        import os
        from contextlib import chdir
        from decimal import Decimal, localcontext
        from pathlib import Path

        Path("work/inner").mkdir(parents=True, exist_ok=True)
        start = os.getcwd()
        with chdir("work"):
            print(sorted(os.listdir(".")))
        print(os.getcwd() == start)

        with localcontext() as ctx:
            ctx.prec = 3
            print(Decimal(1) / Decimal(7))
        print(Decimal(1) / Decimal(7))
        """, hint="Оба менеджера временно меняют состояние и восстанавливают его."),
    cod(f"{P}-stdlib-e4", t("""
        Есть класс `Browser` с методом `quit()` (но без `__enter__`/`__exit__`). `closing` здесь не подойдёт: он вызывает `close()`, а не `quit()`. Напиши функцию `use_browser(browser, action)`: вызвать `action(browser)` и **гарантированно** вызвать `browser.quit()` после, вернуть результат `action`.
        """),
        """
        class Browser:
            def __init__(self):
                self.alive = True

            def quit(self):
                self.alive = False


        def use_browser(browser, action):
            pass
        """,
        """
        def test_values():
            b = Browser()
            assert use_browser(b, lambda br: "title") == "title" and not b.alive, "Результат и quit"
            b2 = Browser()
            try:
                use_browser(b2, lambda br: 1 / 0)
            except ZeroDivisionError:
                pass
            assert not b2.alive, "quit и при ошибке"
        """,
        """
        class Browser:
            def __init__(self):
                self.alive = True

            def quit(self):
                self.alive = False


        def use_browser(browser, action):
            try:
                return action(browser)
            finally:
                browser.quit()
        """),
    cod(f"{P}-stdlib-e5", t("""
        Напиши функцию `fetch(conn)` — у объекта `conn` есть методы `read()` и `close()`. Используй `contextlib.closing`, чтобы соединение закрылось после чтения. Вернуть результат `read()`.
        """),
        """
        from contextlib import closing


        def fetch(conn):
            pass
        """,
        """
        def test_values():
            class Conn:
                closed = False
                def read(self):
                    return "ответ"
                def close(self):
                    self.closed = True
            c = Conn()
            assert fetch(c) == "ответ" and c.closed, "Прочитано и закрыто"
            assert "closing" in open("solution.py", encoding="utf-8").read(), "Используй closing"
        """,
        """
        from contextlib import closing


        def fetch(conn):
            with closing(conn) as c:
                return c.read()
        """),
    cod(f"{P}-stdlib-e6", t("""
        Напиши функцию `maybe_log(data, log_file=None)` — вернуть сумму чисел. Если `log_file` передан (путь), открыть его на дозапись и записать туда строку `"сумма: N\\n"`. Используй `nullcontext`, чтобы не дублировать код: один `with` на оба случая.
        """),
        """
        from contextlib import nullcontext


        def maybe_log(data, log_file=None):
            pass
        """,
        """
        import os

        def test_values():
            if os.path.exists("sum.log"):
                os.remove("sum.log")
            assert maybe_log([1, 2]) == 3 and not os.path.exists("sum.log"), "Без файла"
            assert maybe_log([5, 5], "sum.log") == 10, "С файлом"
            with open("sum.log", encoding="utf-8") as f:
                assert f.read() == "сумма: 10\\n", "Содержимое"
            assert "nullcontext" in open("solution.py", encoding="utf-8").read(), "Используй nullcontext"
        """,
        """
        from contextlib import nullcontext


        def maybe_log(data, log_file=None):
            total = sum(data)
            cm = open(log_file, "a", encoding="utf-8") if log_file else nullcontext()
            with cm as f:
                if f is not None:
                    f.write(f"сумма: {total}\\n")
            return total
        """),
    cod(f"{P}-stdlib-e7", t("""
        Напиши функцию `list_in(folder)` — временно перейти в папку через `contextlib.chdir`, вернуть отсортированный список имён в ней (`os.listdir(".")`). После вызова текущая папка должна остаться прежней.
        """),
        """
        import os
        from contextlib import chdir


        def list_in(folder):
            pass
        """,
        """
        import os
        from pathlib import Path

        def test_values():
            Path("li/x").mkdir(parents=True, exist_ok=True)
            Path("li/b.txt").write_text("", encoding="utf-8")
            start = os.getcwd()
            assert list_in("li") == ["b.txt", "x"] and os.getcwd() == start, "Неверный результат"
        """,
        """
        import os
        from contextlib import chdir


        def list_in(folder):
            with chdir(folder):
                return sorted(os.listdir("."))
        """),
    cod(f"{P}-stdlib-e8", t("""
        Напиши функцию `precise_div(a, b, digits)` — разделить два числа как `Decimal` с точностью `digits` значащих цифр через `decimal.localcontext`. Вернуть строку результата. Глобальная точность не должна измениться.

        ```
        precise_div(1, 3, 5)   # → "0.33333"
        ```
        """),
        """
        from decimal import Decimal, localcontext, getcontext


        def precise_div(a, b, digits):
            pass
        """,
        """
        from decimal import getcontext

        def test_values():
            before = getcontext().prec
            assert precise_div(1, 3, 5) == "0.33333" and precise_div(2, 3, 2) == "0.67" and precise_div(10, 4, 10) == "2.5", precise_div(1, 3, 5)
            assert getcontext().prec == before, "Глобальная точность не меняется"
        """,
        """
        from decimal import Decimal, localcontext, getcontext


        def precise_div(a, b, digits):
            with localcontext() as ctx:
                ctx.prec = digits
                return str(Decimal(a) / Decimal(b))
        """, xp=20),
),
)
