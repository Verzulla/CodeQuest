"""Подробная теория и «Проверь себя» для темы «Контекстные менеджеры»."""
from ._lib import t

THEORY = {
"ctx-m1-l1": {"full": t("""
    ## Зачем это нужно

    Многие ресурсы нужно **обязательно освободить** после использования: закрыть файл, вернуть соединение с БД в пул, закрыть браузер в UI-тесте, удалить тестовые данные. Если между «открыл» и «закрыл» случится ошибка, а закрытие не сработает — ресурсы утекают, файлы остаются заблокированными, тесты влияют друг на друга.

    ## Как это работает

    ### try / except / finally

    ```py
    try:
        рискованный код
    except SomeError:
        обработка ошибки
    else:
        если ошибок не было
    finally:
        выполнится ВСЕГДА
    ```

    `finally` выполняется в любом случае: при успехе, при исключении (пойманном или нет), при `return` из `try`. Это место для «уборки».

    ### with

    `with` — короткая и безопасная форма того же шаблона:

    ```py
    with open("data.txt", "w") as f:
        f.write("hello")
    # здесь файл гарантированно закрыт
    ```

    Объект после `with` — **контекстный менеджер**. Он знает, что делать при входе в блок и при выходе из него, даже аварийном.

    Несколько менеджеров сразу: `with open("a") as a, open("b") as b:`.

    ## Примеры

    ### Пример 1. finally выполняется всегда

    ```python
    def risky(x):
        try:
            print("  делим 10 на", x)
            return 10 / x
        except ZeroDivisionError:
            print("  деление на ноль!")
            return None
        finally:
            print("  finally: уборка")

    print(risky(2))
    print(risky(0))
    ```

    ### Пример 2. with и файл

    ```python
    with open("notes.txt", "w", encoding="utf-8") as f:
        f.write("первая\\n")
        f.write("вторая\\n")
    print("закрыт?", f.closed)

    with open("notes.txt", encoding="utf-8") as f:
        for line in f:
            print("строка:", line.rstrip())
    ```

    ### Пример 3. Файл закроется и при ошибке

    ```python
    try:
        with open("log.txt", "w", encoding="utf-8") as f:
            f.write("начало")
            raise ValueError("что-то сломалось")
    except ValueError as e:
        print("поймали:", e)
    print("файл закрыт?", f.closed)
    ```

    ### Пример 4. Режимы открытия файлов

    ```python
    with open("data.txt", "w", encoding="utf-8") as f:   # w — перезаписать
        f.write("1\\n")
    with open("data.txt", "a", encoding="utf-8") as f:   # a — дописать в конец
        f.write("2\\n")
    with open("data.txt", encoding="utf-8") as f:        # r (по умолчанию) — читать
        print(f.read().splitlines())
    ```

    ## Частые ошибки

    **`f = open(...)` без закрытия.** Если по дороге исключение, файл останется открытым. Всегда `with`.

    **Режим `"w"` вместо `"a"`.** `"w"` стирает содержимое файла.

    **Без `encoding="utf-8"`.** На Windows кодировка по умолчанию другая, и кириллица превратится в кракозябры.

    **Голый `except:`** ловит вообще всё, включая Ctrl+C. Лови конкретные исключения.

    ## Шпаргалка

    ```py
    try: ...
    except ValueError as e: ...
    finally: ...                     # всегда

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)                # закроется сам

    "r" читать · "w" перезаписать · "a" дописать
    ```
    """), "quiz": [
    {"q": "Что выведет функция?\n```py\ndef f():\n    try:\n        return 1\n    finally:\n        print(\"F\")\n\nprint(f())\n```",
     "options": ["`1`", "`F` затем `1`", "`1` затем `F`", "`F`"], "answer": 1,
     "explain": "`finally` выполняется перед тем, как функция действительно вернёт значение. Сначала печатается `F`, потом `print` выводит результат 1."},
    {"q": "Что гарантирует `with open(...) as f:`?",
     "options": ["Файл не может вызвать ошибку", "Файл будет закрыт при выходе из блока, даже при исключении", "Файл откроется быстрее", "Файл создастся, если его нет, в любом режиме"], "answer": 1,
     "explain": "Главная гарантия контекстного менеджера — выполнение кода «уборки» при любом выходе из блока."},
    {"q": "Какой режим `open` дописывает в конец файла, не стирая содержимое?",
     "options": ["`\"w\"`", "`\"r\"`", "`\"a\"`", "`\"x\"`"], "answer": 2,
     "explain": "`\"a\"` (append) — дописать. `\"w\"` перезаписывает файл с нуля."},
]},

"ctx-m1-l2": {"full": t("""
    ## Зачем это нужно

    `with` работает не только с файлами. Любой твой класс может стать контекстным менеджером: соединение с тестовой БД, временный пользователь, открытый браузер, таймер. Для этого нужно реализовать два метода.

    ## Как это работает

    ```py
    class Manager:
        def __enter__(self):
            ...            # подготовка
            return value   # попадёт в переменную после as

        def __exit__(self, exc_type, exc, tb):
            ...            # уборка — вызывается ВСЕГДА
            return False   # False — исключение (если было) летит дальше
    ```

    Что происходит при `with Manager() as x:`:
    1. Создаётся объект `Manager()`.
    2. Вызывается `__enter__()`; его результат присваивается `x`.
    3. Выполняется тело блока.
    4. Вызывается `__exit__(...)`:
       - без ошибки — все три аргумента `None`;
       - при исключении — тип, само исключение и трассировка.
    5. Если `__exit__` вернул `True` — исключение **подавляется**, программа идёт дальше.

    Подавлять исключения нужно осознанно: молча проглоченная ошибка — источник трудноуловимых багов.

    ## Примеры

    ### Пример 1. Вход и выход

    ```python
    class Tag:
        def __init__(self, name):
            self.name = name
        def __enter__(self):
            print(f"<{self.name}>")
            return self
        def __exit__(self, exc_type, exc, tb):
            print(f"</{self.name}>")
            return False

    with Tag("div"):
        with Tag("p"):
            print("текст")
    ```

    ### Пример 2. Что получает __exit__

    ```python
    class Spy:
        def __enter__(self):
            return "значение из __enter__"
        def __exit__(self, exc_type, exc, tb):
            print("exc_type:", exc_type.__name__ if exc_type else None, "| exc:", exc)
            return True                      # подавляем, чтобы пример не упал

    with Spy() as value:
        print("внутри:", value)

    with Spy():
        raise KeyError("нет ключа")
    print("программа продолжается")
    ```

    ### Пример 3. Ресурс, который надо закрыть

    ```python
    class FakeDB:
        def __init__(self):
            self.connected = False
        def __enter__(self):
            self.connected = True
            print("подключились к тестовой БД")
            return self
        def __exit__(self, exc_type, exc, tb):
            self.connected = False
            print("отключились" + (f" (после ошибки {exc_type.__name__})" if exc_type else ""))
            return False

    db = FakeDB()
    try:
        with db:
            raise RuntimeError("тест упал")
    except RuntimeError:
        pass
    print("соединение открыто?", db.connected)
    ```

    ### Пример 4. Подавление только нужных исключений

    ```python
    class Ignore:
        def __init__(self, *exc_classes):
            self.exc_classes = exc_classes
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            return exc_type is not None and issubclass(exc_type, self.exc_classes)

    with Ignore(KeyError, IndexError):
        [][5]
    print("IndexError подавлен")
    try:
        with Ignore(KeyError):
            1 / 0
    except ZeroDivisionError:
        print("ZeroDivisionError пролетел наружу")
    ```

    ## Частые ошибки

    **`__enter__` ничего не возвращает** — тогда `as x` получит `None`.

    **`__exit__` возвращает `True` всегда** — все ошибки внутри блока исчезают бесследно.

    **Проверка `exc_type` без учёта `None`.** `issubclass(None, ...)` упадёт — сначала `exc_type is not None`.

    ## Шпаргалка

    ```py
    class M:
        def __enter__(self):
            return self                          # → as x
        def __exit__(self, exc_type, exc, tb):
            # уборка
            return False                         # не глотать ошибки
    ```

    `True` из `__exit__` — подавить исключение. Без ошибки все аргументы `__exit__` — `None`.
    """), "quiz": [
    {"q": "Что попадёт в `x` в `with M() as x:`?",
     "options": ["Объект `M()`", "То, что вернул `__enter__`", "То, что вернул `__exit__`", "`None` всегда"], "answer": 1,
     "explain": "`as` получает результат `__enter__`. Часто это `self`, но не обязательно — например, `open` возвращает сам файл."},
    {"q": "Что произойдёт, если `__exit__` вернёт `True`, а в блоке было исключение?",
     "options": ["Исключение будет выброшено дальше", "Исключение подавится, программа продолжится после блока", "Блок выполнится заново", "Программа завершится"], "answer": 1,
     "explain": "Истинное значение из `__exit__` означает «исключение обработано» — оно не выходит за пределы `with`."},
    {"q": "Чему равен `exc_type` в `__exit__`, если блок завершился без ошибок?",
     "options": ["`Exception`", "`None`", "`False`", "`StopIteration`"], "answer": 1,
     "explain": "При нормальном завершении все три аргумента — `exc_type`, `exc`, `tb` — равны `None`."},
]},

"ctx-m2-l1": {"full": t("""
    ## Зачем это нужно

    Писать класс с двумя методами ради простого «подготовил — отдал — убрал» многословно. Модуль `contextlib` позволяет сделать контекстный менеджер из обычной функции-генератора. Именно так устроены фикстуры pytest с `yield`: код до `yield` — подготовка, после — уборка.

    ## Как это работает

    ```py
    from contextlib import contextmanager

    @contextmanager
    def resource():
        # __enter__: подготовка
        obj = create()
        try:
            yield obj            # тело with выполняется здесь
        finally:
            # __exit__: уборка
            destroy(obj)
    ```

    - Код до `yield` выполняется при входе в `with`.
    - Значение из `yield` попадает в переменную после `as`.
    - Код после `yield` выполняется при выходе.
    - Если в теле `with` возникло исключение, оно **выбрасывается в точке `yield`**. Поэтому без `try/finally` код уборки при ошибке **не выполнится**.

    ### Параллель с pytest

    ```py
    @pytest.fixture
    def user():
        u = api.create_user()    # подготовка
        yield u                  # тест получает пользователя
        api.delete_user(u)       # уборка после теста
    ```

    ## Примеры

    ### Пример 1. Шаги теста в отчёте

    ```python
    from contextlib import contextmanager

    @contextmanager
    def step(name):
        print(f"▶ {name}")
        yield
        print(f"✔ {name}")

    with step("открыть страницу логина"):
        print("  ...")
    with step("ввести пароль"):
        print("  ...")
    ```

    ### Пример 2. Без try/finally уборка теряется

    ```python
    from contextlib import contextmanager

    @contextmanager
    def fragile():
        print("создан")
        yield
        print("удалён")          # НЕ выполнится при ошибке

    try:
        with fragile():
            raise RuntimeError("упс")
    except RuntimeError:
        print("ошибка поймана, но «удалён» мы так и не увидели")
    ```

    ### Пример 3. Правильная фикстура

    ```python
    from contextlib import contextmanager

    users = []

    @contextmanager
    def temp_user(name):
        users.append(name)
        print("создан", name, "->", users)
        try:
            yield name
        finally:
            users.remove(name)
            print("удалён", name, "->", users)

    try:
        with temp_user("test_anna") as u:
            print("тест работает с", u)
            raise AssertionError("тест упал")
    except AssertionError as e:
        print("результат теста:", e)
    ```

    ### Пример 4. Таймер

    ```python
    import time
    from contextlib import contextmanager

    @contextmanager
    def timer(label):
        start = time.perf_counter()
        try:
            yield
        finally:
            ms = (time.perf_counter() - start) * 1000
            print(f"{label}: {ms:.2f} мс")

    with timer("сумма миллиона"):
        sum(range(1_000_000))
    ```

    ## Частые ошибки

    **Нет `try/finally` вокруг `yield`** — уборка пропускается при ошибке.

    **Два `yield`** в функции-менеджере — `RuntimeError`: менеджер должен отдать значение ровно один раз.

    **Забыли декоратор `@contextmanager`** — тогда это просто генератор, и `with` упадёт.

    ## Шпаргалка

    ```py
    @contextmanager
    def cm():
        setup()
        try:
            yield value
        finally:
            teardown()
    ```
    """), "quiz": [
    {"q": "Где выбрасывается исключение из тела `with` в менеджере на `@contextmanager`?",
     "options": ["В конце функции", "В точке `yield`", "Не выбрасывается", "В `__init__`"], "answer": 1,
     "explain": "Исключение «возвращается» в генератор в месте `yield`. Поэтому код уборки нужно оборачивать в `try/finally`."},
    {"q": "Какой код в менеджере выполнится при входе в `with`?",
     "options": ["Код после `yield`", "Код до `yield`", "Весь код функции сразу", "Никакой"], "answer": 1,
     "explain": "До `yield` — подготовка (аналог `__enter__`), после — уборка (аналог `__exit__`)."},
    {"q": "На что похожи фикстуры pytest с `yield`?",
     "options": ["На лямбды", "На контекстные менеджеры: подготовка → yield → уборка", "На декораторы классов", "Ни на что"], "answer": 1,
     "explain": "Фикстура с `yield` устроена так же: до `yield` готовит данные, после — удаляет их."},
]},

"ctx-m2-l2": {"full": t("""
    ## Зачем это нужно

    В `contextlib` есть готовые менеджеры для частых задач. Знать их — значит не писать велосипеды: подавить ожидаемую ошибку, перехватить вывод программы в тесте, управлять заранее неизвестным количеством ресурсов.

    ## Как это работает

    ### suppress

    ```py
    with suppress(FileNotFoundError):
        os.remove("tmp.txt")
    ```

    Подавляет указанные исключения. Остаток блока после исключения **не выполняется** — выполнение продолжается после `with`.

    ### redirect_stdout

    ```py
    buf = io.StringIO()
    with redirect_stdout(buf):
        print("не на экран, а в буфер")
    buf.getvalue()
    ```

    `io.StringIO` — «файл в памяти». В тестах так проверяют, что функция напечатала.

    ### ExitStack

    Когда менеджеров заранее неизвестное количество (например, открыть все файлы из списка), `ExitStack` собирает их и закрывает все при выходе — **в обратном порядке**.

    ### nullcontext

    Менеджер «ничего не делать» — удобен, когда менеджер нужен не всегда: `with (lock if threaded else nullcontext()):`.

    ## Примеры

    ### Пример 1. suppress

    ```python
    from contextlib import suppress

    data = {"a": 1}
    with suppress(KeyError):
        print("до")
        print(data["нет"])
        print("эта строка не выполнится")
    print("после with")
    ```

    ### Пример 2. Парсинг с пропуском мусора

    ```python
    from contextlib import suppress

    raw = ["1", "abc", "30", "", "-4", "3.5"]
    nums = []
    for s in raw:
        with suppress(ValueError):
            nums.append(int(s))
    print(nums)
    ```

    ### Пример 3. Перехват вывода

    ```python
    import io
    from contextlib import redirect_stdout

    def noisy():
        print("привет")
        print("мир")

    buf = io.StringIO()
    with redirect_stdout(buf):
        noisy()
    captured = buf.getvalue()
    print("перехвачено:", repr(captured))
    print("строк:", len(captured.splitlines()))
    ```

    ### Пример 4. ExitStack и порядок закрытия

    ```python
    from contextlib import contextmanager, ExitStack

    @contextmanager
    def res(name):
        print("открыл", name)
        yield name
        print("закрыл", name)

    with ExitStack() as stack:
        opened = [stack.enter_context(res(n)) for n in ["БД", "кеш", "браузер"]]
        print("работаем с", opened)
    ```

    ### Пример 5. Необязательный менеджер

    ```python
    from contextlib import nullcontext, redirect_stdout
    import io

    def run(quiet):
        buf = io.StringIO()
        with (redirect_stdout(buf) if quiet else nullcontext()):
            print("лог выполнения")
        return buf.getvalue()

    run(quiet=False)
    print("тихий режим поймал:", repr(run(quiet=True)))
    ```

    ## Частые ошибки

    **`suppress(Exception)`** — прячет вообще все ошибки, включая настоящие баги. Подавляй только ожидаемые.

    **Ожидание, что после исключения в `suppress` выполнится остаток блока.** Не выполнится.

    **Забыли `getvalue()`.** `StringIO` сам по себе — объект, а не строка.

    ## Шпаргалка

    ```py
    with suppress(KeyError): ...
    buf = io.StringIO()
    with redirect_stdout(buf): ...;  buf.getvalue()
    with ExitStack() as st: st.enter_context(cm())
    with nullcontext(): ...          # менеджер-пустышка
    ```
    """), "quiz": [
    {"q": "Что выведет код?\n```py\nwith suppress(ZeroDivisionError):\n    print(\"A\")\n    1 / 0\n    print(\"B\")\nprint(\"C\")\n```",
     "options": ["`A B C`", "`A C`", "`A`", "`C`"], "answer": 1,
     "explain": "`A` напечатан, затем исключение: остаток блока (`B`) пропускается, выполнение продолжается после `with` — `C`."},
    {"q": "Для чего в тестах используют `redirect_stdout`?",
     "options": ["Чтобы ускорить печать", "Чтобы перехватить и проверить то, что функция напечатала", "Чтобы писать в файл", "Чтобы отключить исключения"], "answer": 1,
     "explain": "Вывод перенаправляется в буфер (`io.StringIO`), и его можно сравнить с ожидаемым."},
    {"q": "В каком порядке `ExitStack` закрывает менеджеры?",
     "options": ["В порядке открытия", "В обратном порядке", "В случайном", "По алфавиту"], "answer": 1,
     "explain": "Как и вложенные `with`: последний открытый закрывается первым."},
]},
}
