"""Тема «Область видимости», модуль 3 «Подводные камни» — задания. Теория — в _scp_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "scp"

m3 = module(f"{P}-m3", "Подводные камни", "⚠️", "Затенение, изменяемые объекты, циклы, время жизни и модули",

lesson(f"{P}-m3-l1", "Затенение имён",
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        def f(sum):
            try:
                return sum([1, 2])
            except TypeError:
                return "sum затенён параметром"

        print(f(10))
        print(sum([1, 2]))
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа?", """
        id = 42
        try:
            print(id(object()) > 0)
        except TypeError:
            print("встроенная id сломана")
        del id
        print(callable(id))
        """),
    out(f"{P}-m3-l1-e6", "Что выведет программа? Затенение внутри функции.", """
        def total(values):
            sum = 0
            for v in values:
                sum += v
            return sum

        print(total([1, 2, 3]), sum([4, 5]))
        """, hint="Локальная sum затеняет встроенную только внутри функции."),
    cod(f"{P}-m3-l1-e3", t("""
        Функция `stats(list)` падает: параметр назван `list`, и внутри не работает встроенная `list()`. Переименуй параметр в `items`, чтобы функция возвращала `(список_уникальных_элементов_по_порядку_первого_появления, количество)`.

        ```
        stats([3, 1, 3, 2, 1])   # → ([3, 1, 2], 5)
        ```
        """),
        """
        def stats(list):
            unique = list(dict.fromkeys(list))
            return unique, len(list)
        """,
        """
        import inspect

        def test_values():
            assert stats([3, 1, 3, 2, 1]) == ([3, 1, 2], 5), f"Получено {stats([3, 1, 3, 2, 1])}"

        def test_param_name():
            params = list(inspect.signature(stats).parameters)
            assert params == ["items"], f"Параметр должен называться items, сейчас {params}"
        """,
        """
        def stats(items):
            unique = list(dict.fromkeys(items))
            return unique, len(items)
        """),
    cod(f"{P}-m3-l1-e4", t("""
        В заготовке функция `find_max_id(users)` использует переменную `max` для текущего максимума — и из-за этого внутри не работает встроенная `max`. Перепиши её: верни наибольший `id` среди пользователей с помощью **встроенной** `max` и генератора. Не используй имена встроенных функций для переменных.

        ```
        find_max_id([{"id": 3}, {"id": 10}, {"id": 7}])   # → 10
        ```
        """),
        """
        def find_max_id(users):
            max = 0
            for u in users:
                if u["id"] > max:
                    max = u["id"]
            return max
        """,
        """
        def test_value():
            assert find_max_id([{"id": 3}, {"id": 10}, {"id": 7}]) == 10 and find_max_id([{"id": -5}]) == -5, "Неверный максимум"

        def test_uses_builtin():
            src = open("solution.py", encoding="utf-8").read()
            assert "max(" in src and "max =" not in src, "Используй встроенную max, не затеняя её"
        """,
        """
        def find_max_id(users):
            return max(u["id"] for u in users)
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `shadowed_builtins(names)` — из списка имён переменных вернуть те, что **совпадают с именами встроенных функций/типов** Python (в исходном порядке).

        Используй модуль `builtins`: имя встроенное, если `hasattr(builtins, name)`.

        ```
        shadowed_builtins(["items", "list", "user_id", "id", "total", "sum"])
        # → ["list", "id", "sum"]
        ```
        """),
        """
        import builtins

        def shadowed_builtins(names):
            pass
        """,
        """
        def test_values():
            got = shadowed_builtins(["items", "list", "user_id", "id", "total", "sum"])
            assert got == ["list", "id", "sum"], f"Получено {got}"
            assert shadowed_builtins([]) == [], "Пусто — пусто"
        """,
        """
        import builtins

        def shadowed_builtins(names):
            return [n for n in names if hasattr(builtins, n)]
        """),
    cod(f"{P}-m3-l1-e7", t("""
        Функция `label(str, n)` падает с `TypeError`: параметр назван `str` и затеняет встроенную `str()`. Переименуй параметр в `text`.

        ```
        label("Тестов", 5)   # → "Тестов: 5"
        ```
        """),
        """
        def label(str, n):
            return str + ": " + str(n)
        """,
        """
        import inspect

        def test_values():
            assert label("Тестов", 5) == "Тестов: 5", f"Получено {label('Тестов', 5)!r}"

        def test_param_name():
            assert list(inspect.signature(label).parameters) == ["text", "n"], "Параметры: text, n"
        """,
        """
        def label(text, n):
            return text + ": " + str(n)
        """),
    cod(f"{P}-m3-l1-e8", t("""
        Функция `describe(value)` падает: локальная переменная `type` затеняет встроенную `type()`. Переименуй переменную в `kind`.

        ```
        describe(5)      # → "число (int)"
        describe("x")    # → "другое (str)"
        ```
        """),
        """
        def describe(value):
            type = "число" if isinstance(value, int) else "другое"
            return f"{type} ({type(value).__name__})"
        """,
        """
        def test_values():
            assert describe(5) == "число (int)" and describe("x") == "другое (str)", "Неверное описание"

        def test_no_shadow():
            assert "type =" not in open("solution.py", encoding="utf-8").read(), "Не называй переменную type"
        """,
        """
        def describe(value):
            kind = "число" if isinstance(value, int) else "другое"
            return f"{kind} ({type(value).__name__})"
        """),
),

lesson(f"{P}-m3-l2", "Изменяемые объекты и области",
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        items = []

        def add(x):
            items.append(x)

        def reset():
            items = []

        add(1)
        add(2)
        reset()
        print(items)
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа?", """
        def modify(lst):
            lst.append(99)
            lst = [0]
            lst.append(1)
            return lst

        data = [1]
        result = modify(data)
        print(data, result)
        """, hint="После `lst = [0]` имя внутри функции указывает на новый список."),
    out(f"{P}-m3-l2-e6", "Что выведет программа? Изменить объект или переприсвоить имя.", """
        config = {"debug": False}

        def enable():
            config["debug"] = True

        def replace():
            config = {"debug": "новый"}

        enable()
        replace()
        print(config)
        """),
    cod(f"{P}-m3-l2-e3", t("""
        Функция `clear_log()` должна **очищать** глобальный список `LOG`, но сейчас не работает: она создаёт локальную переменную.

        Исправь **без `global`**, изменяя сам объект (например, `LOG.clear()`).

        ```
        LOG.append("x"); clear_log(); LOG   # → []
        ```
        """),
        """
        LOG = []

        def clear_log():
            LOG = []
        """,
        """
        def test_clear():
            LOG.append("x")
            LOG.append("y")
            clear_log()
            assert LOG == [], f"LOG не очищен: {LOG}"

        def test_no_global():
            assert "global" not in open("solution.py", encoding="utf-8").read(), "Реши без global — измени сам объект"
        """,
        """
        LOG = []

        def clear_log():
            LOG.clear()
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Функция `add_default_headers(headers)` должна вернуть **новый** словарь заголовков, дополненный `"Accept": "application/json"`, **не изменяя** переданный словарь. Сейчас она портит аргумент.

        ```
        h = {"Authorization": "Bearer x"}
        add_default_headers(h)   # → {"Authorization": "Bearer x", "Accept": "application/json"}
        h                        # → {"Authorization": "Bearer x"}   без изменений
        ```
        """),
        """
        def add_default_headers(headers):
            headers["Accept"] = "application/json"
            return headers
        """,
        """
        def test_new_dict():
            h = {"Authorization": "Bearer x"}
            result = add_default_headers(h)
            assert result == {"Authorization": "Bearer x", "Accept": "application/json"}, "Неверный результат"
            assert h == {"Authorization": "Bearer x"}, "Исходный словарь изменён"
        """,
        """
        def add_default_headers(headers):
            return {**headers, "Accept": "application/json"}
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `reset_in_place(items, value)` — заменить **всё содержимое** переданного списка одним элементом `value`, так чтобы изменение было видно через **все** ссылки на этот список. Функция ничего не возвращает.

        ```
        a = [1, 2, 3]
        b = a
        reset_in_place(a, 0)
        a, b     # → [0], [0]
        ```
        Используй присваивание срезом `items[:] = ...`.
        """),
        """
        def reset_in_place(items, value):
            items = [value]
        """,
        """
        def test_in_place():
            a = [1, 2, 3]
            b = a
            assert reset_in_place(a, 0) is None, "Функция ничего не возвращает"
            assert a == [0] and b == [0], f"a={a}, b={b}"
        """,
        """
        def reset_in_place(items, value):
            items[:] = [value]
        """),
    cod(f"{P}-m3-l2-e7", t("""
        Функция `add_tag(tags, tag)` должна вернуть **новый** список с добавленным тегом и не менять переданный. Сейчас она портит аргумент.

        ```
        t = ["smoke"]
        add_tag(t, "api")   # → ["smoke", "api"]
        t                   # → ["smoke"]
        ```
        """),
        """
        def add_tag(tags, tag):
            tags.append(tag)
            return tags
        """,
        """
        def test_values():
            t = ["smoke"]
            assert add_tag(t, "api") == ["smoke", "api"] and t == ["smoke"], "Исходный список не должен меняться"
        """,
        """
        def add_tag(tags, tag):
            return tags + [tag]
        """),
    cod(f"{P}-m3-l2-e8", t("""
        Напиши функцию `merge_settings(defaults, overrides)` — новый словарь: настройки по умолчанию, поверх которых записаны переопределения. **Ни один** из аргументов не должен измениться.

        ```
        d = {"timeout": 30, "retries": 3}
        o = {"timeout": 5}
        merge_settings(d, o)   # → {"timeout": 5, "retries": 3}
        ```
        """),
        """
        def merge_settings(defaults, overrides):
            pass
        """,
        """
        def test_values():
            d = {"timeout": 30, "retries": 3}
            o = {"timeout": 5}
            assert merge_settings(d, o) == {"timeout": 5, "retries": 3}, "Неверное слияние"
            assert d == {"timeout": 30, "retries": 3} and o == {"timeout": 5}, "Аргументы не должны меняться"
        """,
        """
        def merge_settings(defaults, overrides):
            result = dict(defaults)
            result.update(overrides)
            return result
        """, hint="dict(defaults) — копия; update дописывает ключи из другого словаря."),
),

lesson(f"{P}-m3-l3", "Области в циклах и списочных включениях",
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        for i in range(3):
            pass
        print("после for:", i)

        squares = [n * n for n in range(3)]
        try:
            print(n)
        except NameError:
            print("n из включения не видна")
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа?", """
        x = "снаружи"
        result = [x for x in ["a", "b"]]
        print(result, x)

        for x in ["c", "d"]:
            pass
        print(x)
        """, hint="Включение не трогает внешнюю x, а обычный цикл — перезаписывает."),
    out(f"{P}-m3-l3-e6", "Что выведет программа?", """
        x = 10
        squares = [x * x for x in range(3)]
        print(squares, x)
        total = sum(x for x in range(4))
        print(total, x)
        """),
    cod(f"{P}-m3-l3-e3", t("""
        В функции `process(items)` баг: переменная цикла `item` используется **после** цикла, и для пустого списка функция падает с `UnboundLocalError`.

        Исправь: функция должна возвращать последний элемент списка, а для пустого — `None`.

        ```
        process([1, 2, 3])   # → 3
        process([])          # → None
        ```
        """),
        """
        def process(items):
            for item in items:
                pass
            return item
        """,
        """
        def test_values():
            assert process([1, 2, 3]) == 3 and process(["a"]) == "a", "Нужен последний элемент"
            assert process([]) is None, "Пустой список — None"
        """,
        """
        def process(items):
            last = None
            for item in items:
                last = item
            return last
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `name_after_loop(names)`, которая доказывает разницу областей: верни пару

        1. результат списочного включения `[n.upper() for n in names]`;
        2. значение внешней переменной `n`, которой **до** включения присвоено `"внешняя"` — она не должна измениться.

        ```
        name_after_loop(["a", "b"])   # → (["A", "B"], "внешняя")
        ```
        """),
        """
        def name_after_loop(names):
            n = "внешняя"
            pass
        """,
        """
        def test_values():
            assert name_after_loop(["a", "b"]) == (["A", "B"], "внешняя"), f"Получено {name_after_loop(['a', 'b'])}"
        """,
        """
        def name_after_loop(names):
            n = "внешняя"
            upper = [n.upper() for n in names]
            return upper, n
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `make_multipliers(n)` — список из `n` функций, где функция с индексом `i` умножает аргумент на `i`. Реши **списочным включением** с лямбдой и позаботься о позднем связывании.

        ```
        ms = make_multipliers(4)
        [m(10) for m in ms]   # → [0, 10, 20, 30]
        ```
        """),
        """
        def make_multipliers(n):
            return [lambda x: x * i for i in range(n)]
        """,
        """
        def test_values():
            ms = make_multipliers(4)
            assert [m(10) for m in ms] == [0, 10, 20, 30], f"Получено {[m(10) for m in ms]}"
        """,
        """
        def make_multipliers(n):
            return [lambda x, i=i: x * i for i in range(n)]
        """),
    cod(f"{P}-m3-l3-e7", t("""
        Функция `report(name, scores)` должна вернуть `"Отчёт для <имя>: <предмет>: <оценка>; …"`, но имя в начале получается неверным: переменная цикла **перезаписывает** параметр `name`. Исправь, переименовав переменную цикла.

        ```
        report("Аня", {"math": 5, "art": 4})   # → "Отчёт для Аня: math: 5; art: 4"
        ```
        """),
        """
        def report(name, scores):
            lines = []
            for name in scores:
                lines.append(f"{name}: {scores[name]}")
            return f"Отчёт для {name}: " + "; ".join(lines)
        """,
        """
        def test_values():
            assert report("Аня", {"math": 5, "art": 4}) == "Отчёт для Аня: math: 5; art: 4", f"Получено {report('Аня', {'math': 5, 'art': 4})!r}"
        """,
        """
        def report(name, scores):
            lines = []
            for subject in scores:
                lines.append(f"{subject}: {scores[subject]}")
            return f"Отчёт для {name}: " + "; ".join(lines)
        """),
    cod(f"{P}-m3-l3-e8", t("""
        Напиши функцию `make_adders(values)` — список функций, где каждая прибавляет к аргументу **своё** число из `values`. Используй вспомогательную фабрику `make_adder(n)`, а не лямбду прямо в цикле.

        ```
        adders = make_adders([1, 10, 100])
        [a(5) for a in adders]   # → [6, 15, 105]
        ```
        """),
        """
        def make_adders(values):
            pass
        """,
        """
        def test_values():
            adders = make_adders([1, 10, 100])
            assert [a(5) for a in adders] == [6, 15, 105], f"Получено {[a(5) for a in adders]}"
        """,
        """
        def make_adder(n):
            def add(x):
                return x + n
            return add

        def make_adders(values):
            return [make_adder(v) for v in values]
        """, hint="Каждый вызов make_adder(n) создаёт отдельную область со своим n."),
),

lesson(f"{P}-lifetime", "Время жизни переменных и del",
    out(f"{P}-lifetime-e1", "Что выведет программа?", """
        x = 5
        del x
        try:
            print(x)
        except NameError as e:
            print("NameError:", e)
        """),
    out(f"{P}-lifetime-e2", "Что выведет программа? Переменная из except … as.", """
        try:
            1 / 0
        except ZeroDivisionError as e:
            msg = str(e)
        print(msg)
        try:
            print(e)
        except NameError:
            print("e удалена после except")
        """, hint="Python сам удаляет имя из except … as в конце блока except."),
    out(f"{P}-lifetime-e3", "Что выведет программа? Имя удалено, объект живёт.", """
        def make_list():
            data = [1, 2, 3]
            return data

        a = make_list()
        b = a
        del a
        print(b)
        """),
    cod(f"{P}-lifetime-e4", t("""
        Напиши функцию `remove_keys(d, keys)` — удалить из словаря `d` **на месте** все ключи из списка `keys` оператором `del`; отсутствующие ключи пропускать. Функция ничего не возвращает.

        ```
        d = {"a": 1, "b": 2, "c": 3}
        remove_keys(d, ["a", "x"])
        d   # → {"b": 2, "c": 3}
        ```
        """),
        """
        def remove_keys(d, keys):
            pass
        """,
        """
        def test_values():
            d = {"a": 1, "b": 2, "c": 3}
            assert remove_keys(d, ["a", "x"]) is None and d == {"b": 2, "c": 3}, f"d = {d}"

        def test_del():
            assert "del " in open("solution.py", encoding="utf-8").read(), "Используй del"
        """,
        """
        def remove_keys(d, keys):
            for k in keys:
                if k in d:
                    del d[k]
        """),
    cod(f"{P}-lifetime-e5", t("""
        Функция `safe_div(a, b)` падает с `NameError` при делении на ноль: сообщение ошибки читается из `e` **после** блока `except`, а там переменной уже нет. Исправь: сохрани текст внутри `except`.

        ```
        safe_div(6, 3)   # → 2.0
        safe_div(1, 0)   # → "ошибка: division by zero"
        ```
        """),
        """
        def safe_div(a, b):
            try:
                return a / b
            except ZeroDivisionError as e:
                pass
            return "ошибка: " + str(e)
        """,
        """
        def test_values():
            assert safe_div(6, 3) == 2.0 and safe_div(1, 0) == "ошибка: division by zero", "Неверный результат"
        """,
        """
        def safe_div(a, b):
            try:
                return a / b
            except ZeroDivisionError as e:
                return "ошибка: " + str(e)
        """),
    cod(f"{P}-lifetime-e6", t("""
        Напиши функцию `remove_at(items, indexes)` — удалить из списка **на месте** элементы с указанными индексами (через `del items[i]`).

        Подвох: после удаления элементы сдвигаются, и остальные индексы «уезжают». Удаляй **с самого большого** индекса.

        ```
        x = ["a", "b", "c", "d"]
        remove_at(x, [0, 2])
        x   # → ["b", "d"]
        ```
        """),
        """
        def remove_at(items, indexes):
            pass
        """,
        """
        def test_values():
            x = ["a", "b", "c", "d"]
            remove_at(x, [0, 2])
            assert x == ["b", "d"], f"x = {x}"
            y = [1, 2, 3]
            remove_at(y, [2, 0, 1])
            assert y == [], f"y = {y}"
        """,
        """
        def remove_at(items, indexes):
            for i in sorted(indexes, reverse=True):
                del items[i]
        """, hint="sorted(indexes, reverse=True) — индексы по убыванию.", xp=20),
    cod(f"{P}-lifetime-e7", t("""
        Замыкание продлевает жизнь переменных внешней функции. Напиши фабрику `make_id_generator(prefix)` — возвращает функцию `next_id()`, которая выдаёт `"<prefix>-1"`, `"<prefix>-2"`, … Счётчик живёт в замыкании уже после того, как `make_id_generator` завершилась.

        ```
        gen = make_id_generator("user")
        gen(), gen()   # → "user-1", "user-2"
        ```
        """),
        """
        def make_id_generator(prefix):
            pass
        """,
        """
        def test_values():
            gen = make_id_generator("user")
            other = make_id_generator("order")
            assert [gen(), gen(), other(), gen()] == ["user-1", "user-2", "order-1", "user-3"], "Неверные id"
        """,
        """
        def make_id_generator(prefix):
            n = 0
            def next_id():
                nonlocal n
                n += 1
                return f"{prefix}-{n}"
            return next_id
        """),
    cod(f"{P}-lifetime-e8", t("""
        Функция `find_first_even(nums)` падает с `UnboundLocalError`, если чётных чисел нет: переменная `found` создаётся только внутри `if`. Исправь — для списка без чётных вернуть `None`.

        ```
        find_first_even([1, 4, 6])   # → 4
        find_first_even([1, 3])      # → None
        ```
        """),
        """
        def find_first_even(nums):
            for n in nums:
                if n % 2 == 0:
                    found = n
                    break
            return found
        """,
        """
        def test_values():
            assert find_first_even([1, 4, 6]) == 4 and find_first_even([1, 3]) is None and find_first_even([]) is None, "Неверный результат"
        """,
        """
        def find_first_even(nums):
            found = None
            for n in nums:
                if n % 2 == 0:
                    found = n
                    break
            return found
        """, hint="Заведи found = None до цикла — тогда переменная существует на любом пути."),
),

lesson(f"{P}-modules", "Модули и пространства имён",
    out(f"{P}-modules-e1", "Что выведет программа?", """
        import math
        from math import sqrt

        print(math.sqrt(16), sqrt(25))
        print(math.pi > 3, "pi" in dir(math))
        """),
    out(f"{P}-modules-e2", "Что выведет программа? Конфликт имён при импорте.", """
        from math import pow

        def pow(a, b):
            return "моя pow"

        print(pow(2, 3))
        import math
        print(math.pow(2, 3))
        """, hint="def pow перезаписала имя, импортированное из math. А math.pow доступна через модуль."),
    out(f"{P}-modules-e3", "Что выведет программа? globals() — это словарь.", """
        x = 1
        print("x" in globals(), globals()["x"])
        globals()["y"] = 42
        print(y, type(globals()).__name__)
        """),
    cod(f"{P}-modules-e4", t("""
        Напиши функцию `circle_area(r)` — площадь круга, округлённая до 2 знаков. Число π возьми из модуля `math` (`import math` и `math.pi`).

        ```
        circle_area(1)   # → 3.14
        circle_area(3)   # → 28.27
        ```
        """),
        """
        def circle_area(r):
            pass
        """,
        """
        def test_values():
            assert circle_area(1) == 3.14 and circle_area(3) == 28.27 and circle_area(0) == 0, "Неверная площадь"

        def test_import():
            assert "import math" in open("solution.py", encoding="utf-8").read(), "Импортируй модуль math"
        """,
        """
        import math

        def circle_area(r):
            return round(math.pi * r * r, 2)
        """),
    cod(f"{P}-modules-e5", t("""
        Напиши функцию `hypotenuse(a, b)` — длина гипотенузы `√(a² + b²)`. Импортируй **только** функцию `sqrt`: `from math import sqrt`.

        ```
        hypotenuse(3, 4)   # → 5.0
        ```
        """),
        """
        def hypotenuse(a, b):
            pass
        """,
        """
        def test_values():
            assert hypotenuse(3, 4) == 5.0 and hypotenuse(5, 12) == 13.0, "Неверная гипотенуза"

        def test_from_import():
            assert "from math import sqrt" in open("solution.py", encoding="utf-8").read(), "Используй from math import sqrt"
        """,
        """
        from math import sqrt

        def hypotenuse(a, b):
            return sqrt(a * a + b * b)
        """),
    cod(f"{P}-modules-e6", t("""
        Напиши функцию `has_global(name)` — есть ли глобальная переменная с таким именем в текущем модуле. Используй `globals()`.

        ```
        ALPHA = 1
        has_global("ALPHA")   # → True
        has_global("BETA")    # → False
        ```
        """),
        """
        ALPHA = 1

        def has_global(name):
            pass
        """,
        """
        def test_values():
            assert has_global("ALPHA") is True and has_global("BETA") is False and has_global("has_global") is True, "Неверный результат"
        """,
        """
        ALPHA = 1

        def has_global(name):
            return name in globals()
        """, hint="Функции — тоже глобальные имена модуля."),
    cod(f"{P}-modules-e7", t("""
        Напиши функцию `pick(items, seed)` — выбрать случайный элемент списка, но **воспроизводимо**: создай генератор `random.Random(seed)` и вызови у него `.choice(items)`. С одним и тем же `seed` результат всегда одинаков — так делают стабильные тестовые данные.

        ```
        pick(["a", "b", "c"], 42) == pick(["a", "b", "c"], 42)   # → True
        ```
        """),
        """
        import random

        def pick(items, seed):
            pass
        """,
        """
        import random

        def test_values():
            items = ["a", "b", "c", "d", "e"]
            assert pick(items, 42) == random.Random(42).choice(items), "Используй random.Random(seed).choice(items)"
            assert all(pick(items, s) == pick(items, s) for s in range(10)), "Результат должен повторяться"
        """,
        """
        import random

        def pick(items, seed):
            return random.Random(seed).choice(items)
        """),
    cod(f"{P}-modules-e8", t("""
        Напиши функцию `days_between(d1, d2)` — сколько дней от даты `d1` до `d2` (строки `"ГГГГ-ММ-ДД"`). Импортируй класс `date`: `from datetime import date`; строку в дату превращает `date.fromisoformat(...)`, разность двух дат имеет атрибут `.days`.

        ```
        days_between("2024-01-01", "2024-03-01")   # → 60
        ```
        """),
        """
        def days_between(d1, d2):
            pass
        """,
        """
        def test_values():
            assert days_between("2024-01-01", "2024-03-01") == 60 and days_between("2024-05-10", "2024-05-01") == -9, "Неверное число дней"

        def test_import():
            assert "from datetime import date" in open("solution.py", encoding="utf-8").read(), "Используй from datetime import date"
        """,
        """
        from datetime import date

        def days_between(d1, d2):
            return (date.fromisoformat(d2) - date.fromisoformat(d1)).days
        """),
),
)
