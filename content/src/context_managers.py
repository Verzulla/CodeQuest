"""Тема «Контекстные менеджеры»."""
from ._lib import t, cod, lesson, module, out, topic

P = "ctx"

m1 = module(f"{P}-m1", "Оператор with", "🚪", "Гарантированная очистка ресурсов",
    lesson(f"{P}-m1-l1", "with и try/finally", """
        # Зачем нужен with

        Ресурсы (файлы, соединения с БД, браузер в UI-тестах) нужно **закрывать**, даже если по дороге случилась ошибка:

        ```
        f = open("data.txt", "w")
        try:
            f.write("hello")
        finally:
            f.close()        # выполнится в любом случае
        ```

        `with` делает то же самое короче:

        ```
        with open("data.txt", "w") as f:
            f.write("hello")
        # здесь файл уже закрыт — даже если внутри было исключение
        ```

        - `finally` выполняется **всегда**: и при нормальном завершении, и при исключении, и при `return`.
        - Объект, который умеет работать с `with`, называют **контекстным менеджером**.
        - Можно открыть несколько сразу: `with open("a") as a, open("b") as b:`
        """,
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
    ),
    lesson(f"{P}-m1-l2", "Свой менеджер: __enter__ и __exit__", """
        # Как устроен контекстный менеджер

        Любой класс с двумя методами годится для `with`:

        ```
        class Timer:
            def __enter__(self):
                print("старт")
                return self              # это попадёт в переменную после `as`

            def __exit__(self, exc_type, exc, tb):
                print("стоп")
                return False             # False — исключение (если было) полетит дальше

        with Timer() as t:
            print("работаем")
        ```

        - `__enter__` вызывается при входе в блок.
        - `__exit__` вызывается при выходе — **всегда**. Если внутри было исключение, в `exc_type` будет его класс, иначе `None`.
        - Если `__exit__` вернёт `True` — исключение **подавляется**.
        """,
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
    ),
)

m2 = module(f"{P}-m2", "contextlib", "🧰", "Менеджеры из генераторов и готовые помощники",
    lesson(f"{P}-m2-l1", "@contextmanager", """
        # Менеджер из генератора

        Писать класс не обязательно — `contextlib.contextmanager` превращает генератор в менеджер:

        ```
        from contextlib import contextmanager

        @contextmanager
        def tag(name):
            print(f"<{name}>")      # это __enter__
            yield                   # здесь выполняется тело with
            print(f"</{name}>")     # это __exit__
        ```

        - То, что стоит в `yield`, попадёт в переменную после `as`: `yield conn`.
        - Чтобы код «выхода» выполнился **и при ошибке**, оборачивай `yield` в `try/finally`:

        ```
        @contextmanager
        def connection():
            conn = open_connection()
            try:
                yield conn
            finally:
                conn.close()
        ```

        Так в тестах делают фикстуры: создать тестовые данные → отдать тесту → удалить.
        """,
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
    ),
    lesson(f"{P}-m2-l2", "Готовые менеджеры", """
        # Полезное из contextlib

        **suppress** — подавить указанные исключения:
        ```
        from contextlib import suppress
        with suppress(FileNotFoundError):
            os.remove("tmp.txt")       # нет файла — ну и ладно
        ```

        **redirect_stdout** — перехватить всё, что печатается (удобно в тестах):
        ```
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            print("скрыто")
        buf.getvalue()   # 'скрыто\\n'
        ```

        **ExitStack** — управлять заранее неизвестным числом менеджеров:
        ```
        from contextlib import ExitStack
        with ExitStack() as stack:
            files = [stack.enter_context(open(p)) for p in paths]
        ```

        Менеджеры закрываются в **обратном** порядке открытия.
        """,
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
    ),
)

TOPIC = topic("context-managers", "Контекстные менеджеры", "🚪", "#2b70c9",
              "with, try/finally, __enter__/__exit__ и contextlib", m1, m2, group="Python")
