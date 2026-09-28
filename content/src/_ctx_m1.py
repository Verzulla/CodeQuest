"""Тема «Контекстные менеджеры», модуль 1 «Оператор with» — задания. Теория — в _ctx_t1.py.

Слаги ctx-m1-l1, ctx-m1-l2 унаследованы от старой темы — так сохраняется прогресс."""
from ._lib import cod, lesson, module, out, t

P = "ctx"

m1 = module(f"{P}-m1", "Оператор with", "🚪", "try/finally и with, несколько менеджеров, свой класс-менеджер, исключения в __exit__",

lesson(f"{P}-m1-l1", "with и try/finally",
    out(f"{P}-m1-l1-e1", "Что выведет программа? `finally` выполняется всегда.", """
            def f():
                try:
                    return "из try"
                finally:
                    print("finally")

            print(f())
            """, hint="Сначала выполнится finally, и только потом функция вернёт значение."),
    out(f"{P}-m1-l1-e2", "Что выведет программа?", """
            try:
                print("начало")
                1 / 0
                print("не дойдём")
            except ZeroDivisionError:
                print("поймали")
            finally:
                print("уборка")
            """),
    out(f"{P}-m1-l1-e3", "Что выведет программа? Файл пишется во временную папку.", """
            with open("notes.txt", "w", encoding="utf-8") as f:
                f.write("первая\\n")
                f.write("вторая\\n")
            print(f.closed)

            with open("notes.txt", encoding="utf-8") as f:
                print(f.read().splitlines())
            """),
    cod(f"{P}-m1-l1-e4", t("""
            Напиши функцию `save_lines(path, lines)`, которая записывает строки в файл.

            - Получает: `path` — имя файла; `lines` — список строк.
            - Записывает в файл все строки, **каждую на новой строке** (после каждой добавь `"\\n"`). Если файл уже был — перезаписывает.
            - Ничего не возвращает.

            Пример:
            ```
            save_lines("out.txt", ["a", "b", "c"])
            # в файле out.txt:
            # a
            # b
            # c
            ```
            Открой файл через `with open(path, "w", encoding="utf-8") as f:` — тогда он гарантированно закроется.
            """),
            """
            def save_lines(path, lines):
                pass
            """,
            """
            def test_file():
                save_lines("out.txt", ["a", "b", "c"])
                with open("out.txt", encoding="utf-8") as f:
                    content = f.read()
                assert content.splitlines() == ["a", "b", "c"], f"В файле: {content!r}"
            """,
            """
            def save_lines(path, lines):
                with open(path, "w", encoding="utf-8") as f:
                    for line in lines:
                        f.write(line + "\\n")
            """,
            hint="Режим `\"w\"` — запись. Не забудь `\"\\n\"` после каждой строки."),
    cod(f"{P}-m1-l1-e5", t("""
            Напиши функцию `count_lines(path)`, которая считает строки в файле.

            - Получает: `path` — имя существующего текстового файла.
            - Возвращает: количество строк в нём.

            Пример: если в файле `log.txt` записано `"1\\n2\\n3\\n"`, то
            ```
            count_lines("log.txt")   # → 3
            ```
            Открой файл через `with` — после выхода из функции он должен быть закрыт. Файл можно перебирать циклом `for line in f` — по строкам.
            """),
            """
            def count_lines(path):
                pass
            """,
            """
            def test_count():
                with open("log.txt", "w", encoding="utf-8") as f:
                    f.write("1\\n2\\n3\\n")
                assert count_lines("log.txt") == 3, f"Получено {count_lines('log.txt')}"
            """,
            """
            def count_lines(path):
                with open(path, encoding="utf-8") as f:
                    return sum(1 for _ in f)
            """,
            hint="Файл итерируемый: `for line in f` перебирает строки."),
    cod(f"{P}-m1-l1-e6", t("""
            Напиши функцию `safe_divide(a, b, log)` — деление, которое не падает и всегда оставляет запись в журнале.

            - Получает: числа `a` и `b`; `log` — список-журнал.
            - Возвращает: `a / b`, а если `b` равно нулю (возникает `ZeroDivisionError`) — `None`.
            - **В любом случае** — и при успехе, и при ошибке — добавляет в список `log` строку `"done"`.

            Примеры:
            ```
            log = []
            safe_divide(10, 2, log)   # → 5.0,  log == ["done"]

            log = []
            safe_divide(1, 0, log)    # → None, log == ["done"]
            ```
            Используй `try` / `except ZeroDivisionError` / `finally`.
            """),
            """
            def safe_divide(a, b, log):
                pass
            """,
            """
            def test_ok():
                log = []
                assert safe_divide(10, 2, log) == 5, "10 / 2 = 5"
                assert log == ["done"], "После успешного деления в log должно быть 'done'"

            def test_zero():
                log = []
                assert safe_divide(1, 0, log) is None, "Деление на ноль → None"
                assert log == ["done"], "И при ошибке в log должно быть 'done'"
            """,
            """
            def safe_divide(a, b, log):
                try:
                    return a / b
                except ZeroDivisionError:
                    return None
                finally:
                    log.append("done")
            """),
    out(f"{P}-m1-l1-e7", "Что выведет программа? finally при return и break.", """
        def check(x):
            try:
                if x < 0:
                    return "отрицательное"
                return "ок"
            finally:
                print("проверено", x)

        print(check(-1))
        for i in range(3):
            try:
                if i == 1:
                    break
            finally:
                print("итерация", i)
        """, hint="finally выполняется при любом выходе из try — return, break, исключение."),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `run_with_cleanup(action, cleanup)` — вызвать `action()` и **в любом случае** вызвать `cleanup()`, даже если `action` выбросил исключение (исключение должно полететь дальше). Вернуть результат `action()`.
        """),
        """
        def run_with_cleanup(action, cleanup):
            pass
        """,
        """
        def test_values():
            log = []
            assert run_with_cleanup(lambda: 42, lambda: log.append("clean")) == 42 and log == ["clean"], "Успешный вызов"
            def boom():
                raise ValueError("упс")
            try:
                run_with_cleanup(boom, lambda: log.append("clean2"))
            except ValueError:
                assert log == ["clean", "clean2"], "cleanup и при ошибке"
                return
            assert False, "Исключение должно пробрасываться"
        """,
        """
        def run_with_cleanup(action, cleanup):
            try:
                return action()
            finally:
                cleanup()
        """),
),

lesson(f"{P}-multi", "Несколько менеджеров и вложенность",
    out(f"{P}-multi-e1", "Что выведет программа? Два файла в одном with.", """
        with open("a.txt", "w", encoding="utf-8") as fa, open("b.txt", "w", encoding="utf-8") as fb:
            fa.write("A")
            fb.write("B")
        print(fa.closed, fb.closed)
        with open("a.txt", encoding="utf-8") as fa, open("b.txt", encoding="utf-8") as fb:
            print(fa.read() + fb.read())
        """),
    out(f"{P}-multi-e2", "Что выведет программа? Порядок входа и выхода.", """
        class Box:
            def __init__(self, name):
                self.name = name

            def __enter__(self):
                print("открыл", self.name)
                return self

            def __exit__(self, *args):
                print("закрыл", self.name)

        with Box("А") as a, Box("Б") as b:
            print("внутри", a.name, b.name)
        """, hint="Закрываются в обратном порядке — как матрёшка."),
    out(f"{P}-multi-e3", "Что выведет программа? Второй не открылся.", """
        class Box:
            def __init__(self, name, fail=False):
                self.name = name
                self.fail = fail

            def __enter__(self):
                if self.fail:
                    raise OSError(f"не открыть {self.name}")
                print("открыл", self.name)
                return self

            def __exit__(self, *args):
                print("закрыл", self.name)

        try:
            with Box("БД") as db, Box("браузер", fail=True) as br:
                print("тест")
        except OSError as e:
            print(e)
        """, hint="Уже открытые менеджеры закрываются, даже если следующий не открылся."),
    cod(f"{P}-multi-e4", t("""
        Напиши функцию `merge_files(a, b, out)` — записать в файл `out` содержимое `a`, затем `b`. Открой все три файла **в одном** операторе `with`.
        """),
        """
        def merge_files(a, b, out):
            pass
        """,
        """
        def test_values():
            with open("m1.txt", "w", encoding="utf-8") as f:
                f.write("один\\n")
            with open("m2.txt", "w", encoding="utf-8") as f:
                f.write("два\\n")
            merge_files("m1.txt", "m2.txt", "m3.txt")
            with open("m3.txt", encoding="utf-8") as f:
                assert f.read() == "один\\nдва\\n", "Неверное содержимое"
            src = open("solution.py", encoding="utf-8").read()
            assert src.count("with ") == 1, "Нужен один оператор with"
        """,
        """
        def merge_files(a, b, out):
            with open(a, encoding="utf-8") as fa, open(b, encoding="utf-8") as fb, open(out, "w", encoding="utf-8") as fo:
                fo.write(fa.read())
                fo.write(fb.read())
        """),
    cod(f"{P}-multi-e5", t("""
        Напиши функцию `compare_files(a, b)` — список номеров строк (с 1), в которых два файла различаются. Сравнивай построчно до конца **короткого** файла. Открой оба файла одним `with`.
        """),
        """
        def compare_files(a, b):
            pass
        """,
        """
        def test_values():
            with open("c1.txt", "w", encoding="utf-8") as f:
                f.write("a\\nb\\nc\\nd\\n")
            with open("c2.txt", "w", encoding="utf-8") as f:
                f.write("a\\nX\\nc\\nY\\nлишнее\\n")
            assert compare_files("c1.txt", "c2.txt") == [2, 4] and compare_files("c1.txt", "c1.txt") == [], compare_files("c1.txt", "c2.txt")
        """,
        """
        def compare_files(a, b):
            with open(a, encoding="utf-8") as fa, open(b, encoding="utf-8") as fb:
                return [n for n, (x, y) in enumerate(zip(fa, fb), start=1) if x != y]
        """),
    cod(f"{P}-multi-e6", t("""
        Напиши функцию `split_by_level(src, errors_path, other_path)` — строки лога с `ERROR` записать в один файл, остальные — в другой. Все три файла — в одном `with` (можно в скобках на нескольких строках).
        """),
        """
        def split_by_level(src, errors_path, other_path):
            pass
        """,
        """
        def test_values():
            with open("lvl.log", "w", encoding="utf-8") as f:
                f.write("INFO a\\nERROR b\\nINFO c\\nERROR d\\n")
            split_by_level("lvl.log", "err.log", "rest.log")
            with open("err.log", encoding="utf-8") as f:
                assert f.read() == "ERROR b\\nERROR d\\n", "Ошибки"
            with open("rest.log", encoding="utf-8") as f:
                assert f.read() == "INFO a\\nINFO c\\n", "Остальное"
        """,
        """
        def split_by_level(src, errors_path, other_path):
            with (
                open(src, encoding="utf-8") as fin,
                open(errors_path, "w", encoding="utf-8") as ferr,
                open(other_path, "w", encoding="utf-8") as fother,
            ):
                for line in fin:
                    if "ERROR" in line:
                        ferr.write(line)
                    else:
                        fother.write(line)
        """),
    cod(f"{P}-multi-e7", t("""
        Есть класс `Tracker(name, log)` — менеджер, который пишет в список `log` строки `"+имя"` при входе и `"-имя"` при выходе. Напиши функцию `nested(log)`, которая открывает `Tracker("outer", log)`, внутри него — `Tracker("inner", log)`, а внутри добавляет в `log` строку `"work"`. Ожидаемый журнал: `["+outer", "+inner", "work", "-inner", "-outer"]`.
        """),
        """
        class Tracker:
            def __init__(self, name, log):
                self.name = name
                self.log = log

            def __enter__(self):
                self.log.append("+" + self.name)
                return self

            def __exit__(self, *args):
                self.log.append("-" + self.name)


        def nested(log):
            pass
        """,
        """
        def test_values():
            log = []
            nested(log)
            assert log == ["+outer", "+inner", "work", "-inner", "-outer"], log
        """,
        """
        class Tracker:
            def __init__(self, name, log):
                self.name = name
                self.log = log

            def __enter__(self):
                self.log.append("+" + self.name)
                return self

            def __exit__(self, *args):
                self.log.append("-" + self.name)


        def nested(log):
            with Tracker("outer", log), Tracker("inner", log):
                log.append("work")
        """),
    cod(f"{P}-multi-e8", t("""
        Напиши функцию `read_all(paths)` — прочитать несколько файлов (их количество заранее неизвестно) и вернуть список содержимого. Каждый файл открывай через `with`; если файла нет — вместо содержимого `None`.
        """),
        """
        def read_all(paths):
            pass
        """,
        """
        def test_values():
            with open("ra1.txt", "w", encoding="utf-8") as f:
                f.write("x")
            with open("ra2.txt", "w", encoding="utf-8") as f:
                f.write("y")
            assert read_all(["ra1.txt", "нет.txt", "ra2.txt"]) == ["x", None, "y"] and read_all([]) == [], "Неверный результат"
        """,
        """
        def read_all(paths):
            result = []
            for path in paths:
                try:
                    with open(path, encoding="utf-8") as f:
                        result.append(f.read())
                except FileNotFoundError:
                    result.append(None)
            return result
        """, xp=20),
),

lesson(f"{P}-m1-l2", "Свой менеджер: __enter__ и __exit__",
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
            class Tag:
                def __init__(self, name):
                    self.name = name
                def __enter__(self):
                    print(f"<{self.name}>")
                def __exit__(self, *args):
                    print(f"</{self.name}>")

            with Tag("div"):
                with Tag("p"):
                    print("текст")
            """),
    out(f"{P}-m1-l2-e2", "Что выведет программа? Смотри, что возвращает `__exit__`.", """
            class Quiet:
                def __enter__(self):
                    return self
                def __exit__(self, exc_type, exc, tb):
                    print("вышли, ошибка:", exc_type.__name__ if exc_type else None)
                    return True

            with Quiet():
                raise ValueError("упс")
            print("программа продолжается")
            """),
    out(f"{P}-m1-l2-e3", "Что попадёт в переменную после `as`?", """
            class Conn:
                def __enter__(self):
                    return "соединение №1"
                def __exit__(self, *args):
                    return False

            with Conn() as c:
                print(c)
            """, hint="В переменную попадает то, что вернул __enter__."),
    cod(f"{P}-m1-l2-e4", t("""
            Допиши класс `Resource`, чтобы он работал в `with` как контекстный менеджер.

            Добавь два метода:
            - `__enter__(self)` — ставит `self.opened = True` и возвращает `self`;
            - `__exit__(self, exc_type, exc, tb)` — ставит `self.opened = False` и возвращает `False` (исключения не подавляем).

            Как это будет работать:
            ```
            r = Resource()
            with r as inside:      # inside — это тот же объект r
                r.opened           # → True
            r.opened               # → False  (даже если внутри with была ошибка)
            ```
            """),
            """
            class Resource:
                def __init__(self):
                    self.opened = False
            """,
            """
            def test_opened_inside():
                r = Resource()
                with r as inside:
                    assert inside is r, "__enter__ должен вернуть self"
                    assert r.opened is True, "Внутри with opened должен быть True"
                assert r.opened is False, "После with opened должен стать False"

            def test_closed_on_error():
                r = Resource()
                try:
                    with r:
                        raise RuntimeError
                except RuntimeError:
                    pass
                assert r.opened is False, "Ресурс должен закрыться даже при исключении"
            """,
            """
            class Resource:
                def __init__(self):
                    self.opened = False

                def __enter__(self):
                    self.opened = True
                    return self

                def __exit__(self, exc_type, exc, tb):
                    self.opened = False
                    return False
            """),
    cod(f"{P}-m1-l2-e5", t("""
            Допиши контекстный менеджер `Ignore(exc_class)`, который гасит исключения указанного типа.

            - При создании получает класс исключения, например `Ignore(KeyError)`.
            - Если внутри блока `with` возникло исключение **этого класса** (или его наследника) — оно подавляется, программа идёт дальше.
            - Любые **другие** исключения пролетают наружу как обычно.

            Пример:
            ```
            with Ignore(KeyError):
                {}["нет ключа"]     # KeyError — подавлен
            print("живём дальше")

            with Ignore(KeyError):
                1 / 0               # ZeroDivisionError — НЕ подавляется, вылетит наружу
            ```
            Нужны методы `__enter__` и `__exit__`. Чтобы подавить исключение, `__exit__` должен вернуть `True`. Проверить класс: `issubclass(exc_type, self.exc_class)`; помни, что без ошибки `exc_type` равен `None`.
            """),
            """
            class Ignore:
                def __init__(self, exc_class):
                    self.exc_class = exc_class
            """,
            """
            def test_ignores():
                with Ignore(KeyError):
                    {}["нет ключа"]
                # если дошли сюда — KeyError подавлен

            def test_other_passes():
                try:
                    with Ignore(KeyError):
                        1 / 0
                except ZeroDivisionError:
                    return
                assert False, "ZeroDivisionError не должен подавляться"
            """,
            """
            class Ignore:
                def __init__(self, exc_class):
                    self.exc_class = exc_class

                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc, tb):
                    return exc_type is not None and issubclass(exc_type, self.exc_class)
            """,
            hint="В `__exit__` верни True, только если `exc_type` — нужный класс (`issubclass`).", xp=20),
    cod(f"{P}-m1-l2-e6", t("""
            Допиши контекстный менеджер `Recorder(events)`, который записывает вход и выход из блока в журнал.

            - При создании получает `events` — список-журнал.
            - При входе в `with` добавляет в журнал `"enter"`.
            - При выходе добавляет:
              - `"exit"` — если блок завершился без ошибок;
              - `"exit:ИмяИсключения"` — если была ошибка, например `"exit:ValueError"`.
            - Исключения **не подавляет** — они вылетают наружу.

            Пример:
            ```
            ev = []
            with Recorder(ev):
                ev.append("body")
            ev   # → ["enter", "body", "exit"]
            ```
            Имя класса исключения: `exc_type.__name__`.
            """),
            """
            class Recorder:
                def __init__(self, events):
                    self.events = events
            """,
            """
            def test_normal():
                ev = []
                with Recorder(ev):
                    ev.append("body")
                assert ev == ["enter", "body", "exit"], f"Получено {ev}"

            def test_error():
                ev = []
                try:
                    with Recorder(ev):
                        raise ValueError
                except ValueError:
                    pass
                else:
                    assert False, "Исключение не должно подавляться"
                assert ev == ["enter", "exit:ValueError"], f"Получено {ev}"
            """,
            """
            class Recorder:
                def __init__(self, events):
                    self.events = events

                def __enter__(self):
                    self.events.append("enter")
                    return self

                def __exit__(self, exc_type, exc, tb):
                    self.events.append(f"exit:{exc_type.__name__}" if exc_type else "exit")
                    return False
            """,
            xp=20),
    out(f"{P}-m1-l2-e7", "Что выведет программа? Менеджер — обычный объект.", """
        class Counter:
            def __init__(self):
                self.entered = 0

            def __enter__(self):
                self.entered += 1
                return self

            def __exit__(self, *args):
                return False

        c = Counter()
        with c:
            pass
        with c as same:
            print(same is c, same.entered)
        """, hint="Один объект можно использовать в with несколько раз, если он это позволяет."),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши класс-менеджер `Indent(log)`: при входе увеличивает общий счётчик отступа `Indent.level` на 1, при выходе — уменьшает. Метод `write(text)` добавляет в список `log` строку с отступом `"  " * Indent.level`. `__enter__` возвращает `self`.
        """),
        """
        class Indent:
            level = 0
        """,
        """
        def test_values():
            Indent.level = 0
            log = []
            with Indent(log) as a:
                a.write("раз")
                with Indent(log) as b:
                    b.write("два")
                a.write("три")
            assert log == ["  раз", "    два", "  три"] and Indent.level == 0, log
        """,
        """
        class Indent:
            level = 0

            def __init__(self, log):
                self.log = log

            def __enter__(self):
                Indent.level += 1
                return self

            def __exit__(self, *args):
                Indent.level -= 1

            def write(self, text):
                self.log.append("  " * Indent.level + text)
        """, xp=20),
),

lesson(f"{P}-exit", "Исключения внутри with",
    out(f"{P}-exit-e1", "Что выведет программа? Что получает __exit__.", """
        class Show:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                print(exc_type, exc, tb is None)
                return False

        with Show():
            print("без ошибки")

        try:
            with Show():
                int("x")
        except ValueError:
            print("ошибка полетела дальше")
        """),
    out(f"{P}-exit-e2", "Что выведет программа? Глушим только свои ошибки.", """
        class IgnoreKey:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return exc_type is not None and issubclass(exc_type, KeyError)

        with IgnoreKey():
            {}["нет"]
        print("KeyError заглушен")

        try:
            with IgnoreKey():
                [][0]
        except IndexError:
            print("IndexError прошёл насквозь")
        """, hint="True из __exit__ — «исключение обработано», False/None — «пусть летит дальше»."),
    out(f"{P}-exit-e3", "Что выведет программа? Выход из with по return.", """
        class Log:
            def __enter__(self):
                print("вход")
                return self

            def __exit__(self, exc_type, exc, tb):
                print("выход, ошибка:", exc_type)

        def find(items, target):
            with Log():
                for i, x in enumerate(items):
                    if x == target:
                        return i
            return -1

        print(find(["a", "b"], "b"))
        """),
    cod(f"{P}-exit-e4", t("""
        Напиши класс-менеджер `Suppress(*exc_types)` — аналог `contextlib.suppress`: глушит исключения перечисленных типов (и их наследников), остальные пропускает.
        """),
        """
        class Suppress:
            pass
        """,
        """
        def test_values():
            with Suppress(KeyError, ZeroDivisionError):
                1 / 0
            with Suppress(LookupError):
                {}["x"]
            with Suppress(KeyError):
                pass
            try:
                with Suppress(KeyError):
                    int("x")
            except ValueError:
                return
            assert False, "ValueError должен пройти насквозь"
        """,
        """
        class Suppress:
            def __init__(self, *exc_types):
                self.exc_types = exc_types

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return exc_type is not None and issubclass(exc_type, self.exc_types)
        """, hint="issubclass(класс, кортеж_классов) проверяет сразу несколько."),
    cod(f"{P}-exit-e5", t("""
        Напиши класс-менеджер `Capture()`: глушит **любое** `Exception` внутри блока и сохраняет его в атрибут `error` (если ошибки не было — `None`). `__enter__` возвращает `self`.

        ```
        with Capture() as c:
            1 / 0
        type(c.error).__name__   # → "ZeroDivisionError"
        ```
        """),
        """
        class Capture:
            pass
        """,
        """
        def test_values():
            with Capture() as c:
                1 / 0
            assert type(c.error) is ZeroDivisionError, "Ошибка сохранена"
            with Capture() as ok:
                pass
            assert ok.error is None, "Без ошибки — None"
        """,
        """
        class Capture:
            def __init__(self):
                self.error = None

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                if exc_type is not None and issubclass(exc_type, Exception):
                    self.error = exc
                    return True
                return False
        """),
    cod(f"{P}-exit-e6", t("""
        Напиши класс-менеджер `Status(log)`: при выходе из блока добавляет в список `log` строку `"ok"`, если ошибки не было, или `"fail: ИмяОшибки"`, если была. Исключение **не глушить**.
        """),
        """
        class Status:
            pass
        """,
        """
        def test_values():
            log = []
            with Status(log):
                pass
            try:
                with Status(log):
                    raise TimeoutError
            except TimeoutError:
                pass
            else:
                assert False, "Исключение не должно глушиться"
            assert log == ["ok", "fail: TimeoutError"], log
        """,
        """
        class Status:
            def __init__(self, log):
                self.log = log

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                if exc_type is None:
                    self.log.append("ok")
                else:
                    self.log.append(f"fail: {exc_type.__name__}")
                return False
        """),
    cod(f"{P}-exit-e7", t("""
        Напиши класс-менеджер `Transaction(data)` для словаря `data`: при входе запоминает копию словаря; если блок завершился с исключением — **откатывает** `data` к сохранённому состоянию (изменяя тот же объект) и пробрасывает ошибку дальше.
        """),
        """
        class Transaction:
            pass
        """,
        """
        def test_values():
            account = {"balance": 100}
            with Transaction(account):
                account["balance"] -= 30
            assert account == {"balance": 70}, "Успешная транзакция"
            try:
                with Transaction(account):
                    account["balance"] -= 500
                    account["note"] = "x"
                    raise ValueError("недостаточно средств")
            except ValueError:
                pass
            assert account == {"balance": 70}, f"Откат: {account}"
        """,
        """
        class Transaction:
            def __init__(self, data):
                self.data = data

            def __enter__(self):
                self.snapshot = dict(self.data)
                return self.data

            def __exit__(self, exc_type, exc, tb):
                if exc_type is not None:
                    self.data.clear()
                    self.data.update(self.snapshot)
                return False
        """, hint="data.clear() и data.update(копия) меняют тот же объект."),
    cod(f"{P}-exit-e8", t("""
        Напиши класс-менеджер `ExpectError(exc_type)` — упрощённый `pytest.raises`:

        - если внутри блока возникло исключение нужного типа — заглушить его и сохранить в атрибут `value`;
        - если исключения не было — выбросить `AssertionError(f"не было {exc_type.__name__}")`;
        - исключения другого типа — пропустить дальше.
        """),
        """
        class ExpectError:
            pass
        """,
        """
        def test_values():
            with ExpectError(ZeroDivisionError) as e:
                1 / 0
            assert isinstance(e.value, ZeroDivisionError), "Ошибка сохранена"
            try:
                with ExpectError(KeyError):
                    pass
            except AssertionError as err:
                assert str(err) == "не было KeyError", str(err)
            else:
                assert False, "Нужен AssertionError"
            try:
                with ExpectError(KeyError):
                    int("x")
            except ValueError:
                return
            assert False, "Чужая ошибка должна пройти"
        """,
        """
        class ExpectError:
            def __init__(self, exc_type):
                self.exc_type = exc_type
                self.value = None

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                if exc_type is None:
                    raise AssertionError(f"не было {self.exc_type.__name__}")
                if issubclass(exc_type, self.exc_type):
                    self.value = exc
                    return True
                return False
        """, xp=25),
),
)
