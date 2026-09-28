"""Тема «lambda», модуль 3 «Лямбды на практике» — задания. Теория — в _lam_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "lam"

m3 = module(f"{P}-m3", "Лямбды на практике", "🛠️", "Диспетчеры, сложные ключи сортировки, ловушки и стиль, практика",

lesson(f"{P}-dispatch", "Лямбды в словарях: диспетчеры и правила",
    out(f"{P}-dispatch-e1", "Что выведет программа?", """
        ops = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b}
        for op in "+-*":
            print(op, ops[op](6, 3))
        """),
    out(f"{P}-dispatch-e2", "Что выведет программа?", """
        formatters = {"upper": str.upper, "title": str.title, "reverse": lambda s: s[::-1]}
        text = "hello world"
        print([formatters[name](text) for name in ["upper", "reverse"]])
        """, hint="В одном словаре могут лежать и готовые функции, и лямбды."),
    out(f"{P}-dispatch-e3", "Что выведет программа? Правила проверки.", """
        rules = {
            "not empty": lambda s: bool(s.strip()),
            "short": lambda s: len(s) <= 5,
        }
        for value in ["abc", "   ", "abcdef"]:
            print(repr(value), [name for name, check in rules.items() if not check(value)])
        """),
    cod(f"{P}-dispatch-e4", t("""
        Напиши функцию `calculate(a, op, b)` — калькулятор на словаре лямбд для `+ - * /`. Деление на ноль — `None` (условное выражение внутри лямбды). Неизвестная операция — `None`.

        ```
        calculate(6, "/", 3)   # → 2.0
        calculate(6, "/", 0)   # → None
        ```
        """),
        """
        def calculate(a, op, b):
            pass
        """,
        """
        def test_values():
            got = [calculate(6, "+", 3), calculate(6, "-", 3), calculate(6, "*", 3), calculate(6, "/", 3), calculate(6, "/", 0), calculate(6, "%", 3)]
            assert got == [9, 3, 18, 2.0, None, None], f"Получено {got}"
        """,
        """
        OPS = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b if b != 0 else None,
        }

        def calculate(a, op, b):
            func = OPS.get(op)
            return func(a, b) if func else None
        """),
    cod(f"{P}-dispatch-e5", t("""
        Напиши функцию `apply_command(text, command)` — команды `"upper"`, `"lower"`, `"strip"`, `"reverse"` из словаря функций; неизвестная команда — вернуть текст без изменений.
        """),
        """
        def apply_command(text, command):
            pass
        """,
        """
        def test_values():
            got = [apply_command("Ab", "upper"), apply_command("Ab", "lower"), apply_command(" a ", "strip"), apply_command("abc", "reverse"), apply_command("x", "?")]
            assert got == ["AB", "ab", "a", "cba", "x"], f"Получено {got}"
        """,
        """
        COMMANDS = {
            "upper": str.upper,
            "lower": str.lower,
            "strip": str.strip,
            "reverse": lambda s: s[::-1],
        }

        def apply_command(text, command):
            return COMMANDS.get(command, lambda s: s)(text)
        """, hint="get с умолчанием lambda s: s — «ничего не делать»."),
    cod(f"{P}-dispatch-e6", t("""
        Напиши функцию `failed_rules(value, rules)` — `rules` это словарь «название → функция-проверка». Вернуть отсортированный список названий проверок, которые значение **не прошло**.

        ```
        failed_rules("", {"not empty": lambda s: bool(s), "short": lambda s: len(s) < 5})   # → ["not empty"]
        ```
        """),
        """
        def failed_rules(value, rules):
            pass
        """,
        """
        def test_values():
            rules = {"not empty": lambda s: bool(s), "short": lambda s: len(s) < 5, "no spaces": lambda s: " " not in s}
            assert failed_rules("", rules) == ["not empty"] and failed_rules("a b cd", rules) == ["no spaces", "short"], "Неверный результат"
        """,
        """
        def failed_rules(value, rules):
            return sorted(name for name, check in rules.items() if not check(value))
        """),
    cod(f"{P}-dispatch-e7", t("""
        Напиши функцию `final_price(price, kind)` — скидки в словаре лямбд: `"none"` — без скидки, `"sale"` — 10%, `"vip"` — 20%. Результат округлить до 2 знаков. Неизвестный вид — `ValueError`.
        """),
        """
        def final_price(price, kind):
            pass
        """,
        """
        def test_values():
            assert [final_price(100, "none"), final_price(100, "sale"), final_price(99.9, "vip")] == [100, 90.0, 79.92], "Неверная цена"

        def test_unknown():
            try:
                final_price(1, "x")
            except ValueError:
                return
            assert False, "Нужен ValueError"
        """,
        """
        DISCOUNTS = {
            "none": lambda p: p,
            "sale": lambda p: p * 0.9,
            "vip": lambda p: p * 0.8,
        }

        def final_price(price, kind):
            if kind not in DISCOUNTS:
                raise ValueError(f"неизвестная скидка: {kind}")
            return round(DISCOUNTS[kind](price), 2)
        """),
    cod(f"{P}-dispatch-e8", t("""
        Напиши функцию `run_pipeline(value, steps)` — применить к числу шаги по очереди. Шаги — названия из словаря `STEPS`: `"double"`, `"inc"`, `"square"`.

        ```
        run_pipeline(3, ["inc", "double", "square"])   # → 64
        ```
        """),
        """
        def run_pipeline(value, steps):
            pass
        """,
        """
        def test_values():
            assert run_pipeline(3, ["inc", "double", "square"]) == 64 and run_pipeline(5, []) == 5, "Неверный результат"
        """,
        """
        STEPS = {"double": lambda x: x * 2, "inc": lambda x: x + 1, "square": lambda x: x * x}

        def run_pipeline(value, steps):
            for name in steps:
                value = STEPS[name](value)
            return value
        """),
),

lesson(f"{P}-sortkeys", "Сложные ключи сортировки",
    out(f"{P}-sortkeys-e1", "Что выведет программа? None в конец.", """
        items = [3, None, 1, None, 2]
        print(sorted(items, key=lambda x: (x is None, x if x is not None else 0)))
        """, hint="False < True: элементы с x is None == True уходят в конец."),
    out(f"{P}-sortkeys-e2", "Что выведет программа? «Естественная» сортировка.", """
        files = ["img10.png", "img2.png", "img1.png"]
        print(sorted(files))
        print(sorted(files, key=lambda f: int(f[3:-4])))
        """),
    out(f"{P}-sortkeys-e3", "Что выведет программа?", """
        tasks = [("low", "b"), ("high", "a"), ("mid", "c"), ("high", "d")]
        prio = {"high": 0, "mid": 1, "low": 2}
        print(sorted(tasks, key=lambda t: (prio[t[0]], t[1])))
        """),
    cod(f"{P}-sortkeys-e4", t("""
        Напиши функцию `none_last(nums)` — числа по возрастанию, а `None` — в конце.

        ```
        none_last([3, None, 1])   # → [1, 3, None]
        ```
        """),
        """
        def none_last(nums):
            pass
        """,
        """
        def test_values():
            assert none_last([3, None, 1]) == [1, 3, None] and none_last([None, None]) == [None, None] and none_last([]) == [], "Неверный порядок"
        """,
        """
        def none_last(nums):
            return sorted(nums, key=lambda x: (x is None, x if x is not None else 0))
        """),
    cod(f"{P}-sortkeys-e5", t("""
        Напиши функцию `natural_sort(names)` — строки вида «буквы + число» (`"test2"`, `"test10"`, `"case1"`) отсортировать по буквенной части, а затем по числу **как числу**. Если цифр нет — число считать 0.

        ```
        natural_sort(["test10", "test2", "case1", "test"])   # → ["case1", "test", "test2", "test10"]
        ```
        """),
        """
        def natural_sort(names):
            pass
        """,
        """
        def test_values():
            assert natural_sort(["test10", "test2", "case1", "test"]) == ["case1", "test", "test2", "test10"], f"Получено {natural_sort(['test10', 'test2', 'case1', 'test'])}"
        """,
        """
        def natural_key(name):
            prefix = name.rstrip("0123456789")
            digits = name[len(prefix):]
            return (prefix, int(digits) if digits else 0)

        def natural_sort(names):
            return sorted(names, key=natural_key)
        """, hint="Сложный ключ удобнее вынести в функцию и передать key=natural_key.", xp=20),
    cod(f"{P}-sortkeys-e6", t("""
        Напиши функцию `by_priority(tasks)` — задачи-словари `{"title": ..., "priority": "high"|"mid"|"low"}`: сначала `high`, потом `mid`, потом `low`; внутри — по названию. Вернуть названия.
        """),
        """
        def by_priority(tasks):
            pass
        """,
        """
        def test_values():
            tasks = [{"title": "b", "priority": "low"}, {"title": "a", "priority": "high"}, {"title": "c", "priority": "high"}, {"title": "d", "priority": "mid"}]
            assert by_priority(tasks) == ["a", "c", "d", "b"], f"Получено {by_priority(tasks)}"
        """,
        """
        PRIO = {"high": 0, "mid": 1, "low": 2}

        def by_priority(tasks):
            return [t["title"] for t in sorted(tasks, key=lambda t: (PRIO[t["priority"]], t["title"]))]
        """),
    cod(f"{P}-sortkeys-e7", t("""
        Напиши функцию `sort_by_extension(files)` — по расширению (после последней точки, без учёта регистра), потом по имени.

        ```
        sort_by_extension(["b.txt", "a.PNG", "c.png", "a.txt"])   # → ["a.PNG", "c.png", "a.txt", "b.txt"]
        ```
        """),
        """
        def sort_by_extension(files):
            pass
        """,
        """
        def test_values():
            assert sort_by_extension(["b.txt", "a.PNG", "c.png", "a.txt"]) == ["a.PNG", "c.png", "a.txt", "b.txt"], "Неверный порядок"
        """,
        """
        def sort_by_extension(files):
            return sorted(files, key=lambda f: (f.rsplit(".", 1)[-1].lower(), f))
        """),
    cod(f"{P}-sortkeys-e8", t("""
        Напиши функцию `triage(results)` — результаты `(имя, статус, время)`: сначала упавшие (`"fail"`), внутри групп — по времени по убыванию. Вернуть имена.

        ```
        triage([("a", "pass", 1), ("b", "fail", 2), ("c", "fail", 5), ("d", "pass", 3)])   # → ["c", "b", "d", "a"]
        ```
        """),
        """
        def triage(results):
            pass
        """,
        """
        def test_values():
            assert triage([("a", "pass", 1), ("b", "fail", 2), ("c", "fail", 5), ("d", "pass", 3)]) == ["c", "b", "d", "a"], "Неверный порядок"
        """,
        """
        def triage(results):
            return [r[0] for r in sorted(results, key=lambda r: (r[1] != "fail", -r[2]))]
        """),
),

lesson(f"{P}-pitfalls", "Ловушки и стиль",
    out(f"{P}-pitfalls-e1", "Что выведет программа? Позднее связывание.", """
        adders = [lambda x: x + i for i in range(3)]
        print([f(10) for f in adders])
        adders = [lambda x, i=i: x + i for i in range(3)]
        print([f(10) for f in adders])
        """),
    out(f"{P}-pitfalls-e2", "Что выведет программа? Лямбда читает переменную при вызове.", """
        factor = 2
        scale = lambda x: x * factor
        print(scale(5))
        factor = 10
        print(scale(5))
        """),
    out(f"{P}-pitfalls-e3", "Что выведет программа? Имена в отладке.", """
        checks = [lambda x: x > 0, lambda x: x < 100]
        print([c.__name__ for c in checks])

        def positive(x):
            return x > 0

        print(positive.__name__)
        """, hint="В трассировке ошибки лямбда тоже будет безымянной <lambda>."),
    cod(f"{P}-pitfalls-e4", t("""
        Исправь позднее связывание: `make_greeters(names)` должна вернуть список функций без аргументов, каждая возвращает `"Привет, <своё имя>"`.
        """),
        """
        def make_greeters(names):
            return [lambda: f"Привет, {name}" for name in names]
        """,
        """
        def test_values():
            assert [g() for g in make_greeters(["Аня", "Боря"])] == ["Привет, Аня", "Привет, Боря"], "Все функции возвращают последнее имя?"
        """,
        """
        def make_greeters(names):
            return [lambda name=name: f"Привет, {name}" for name in names]
        """),
    cod(f"{P}-pitfalls-e5", t("""
        По PEP 8 не присваивают лямбду имени. Перепиши `is_adult` из заготовки через `def` (функция должна называться `is_adult`).
        """),
        "is_adult = lambda age: age >= 18\n",
        """
        def test_def():
            assert is_adult.__name__ == "is_adult", "Нужна функция def is_adult"
            assert is_adult(18) is True and is_adult(17) is False, "Неверный результат"
        """,
        """
        def is_adult(age):
            return age >= 18
        """),
    cod(f"{P}-pitfalls-e6", t("""
        В заготовке `map` с лямбдой используется ради побочного эффекта (`append`) — это плохой стиль. Перепиши `doubled(nums)` так, чтобы она **строила** результат без `append`.
        """),
        """
        def doubled(nums):
            result = []
            list(map(lambda x: result.append(x * 2), nums))
            return result
        """,
        """
        def test_values():
            assert doubled([1, 2, 3]) == [2, 4, 6] and doubled([]) == [], "Неверный результат"

        def test_no_side_effects():
            assert "append" not in open("solution.py", encoding="utf-8").read(), "Построй список без append"
        """,
        """
        def doubled(nums):
            return list(map(lambda x: x * 2, nums))
        """),
    cod(f"{P}-pitfalls-e7", t("""
        Лямбда с цепочкой условий из заготовки нечитаема. Перепиши `grade` обычной функцией с `if/elif/else` (без `lambda`).
        """),
        'grade = lambda s: "A" if s >= 90 else "B" if s >= 75 else "C" if s >= 60 else "F"\n',
        """
        def test_values():
            assert [grade(95), grade(80), grade(60), grade(10)] == ["A", "B", "C", "F"], "Неверная оценка"

        def test_no_lambda():
            assert "lambda" not in open("solution.py", encoding="utf-8").read(), "Перепиши через def"
        """,
        """
        def grade(s):
            if s >= 90:
                return "A"
            elif s >= 75:
                return "B"
            elif s >= 60:
                return "C"
            else:
                return "F"
        """),
    cod(f"{P}-pitfalls-e8", t("""
        Лямбда `collect = lambda x, acc=[]: acc.append(x) or acc` накапливает значения между вызовами — список по умолчанию общий. Напиши функцию `collect(x, acc=None)`, которая возвращает **новый** список: элементы `acc` (если передан) и `x` в конце. Вызовы не должны влиять друг на друга.
        """),
        """
        def collect(x, acc=None):
            pass
        """,
        """
        def test_values():
            assert collect(1) == [1] and collect(2) == [2], "Вызовы не должны накапливаться"
            src = [1]
            assert collect(2, src) == [1, 2] and src == [1], "Переданный список не меняется"
        """,
        """
        def collect(x, acc=None):
            if acc is None:
                acc = []
            return acc + [x]
        """),
),

lesson(f"{P}-practice", "Практика: обработка результатов тестов",
    out(f"{P}-practice-e1", "Что выведет программа?", """
        tests = [{"name": "login", "time": 1.2, "ok": True},
                 {"name": "pay", "time": 3.4, "ok": False},
                 {"name": "cart", "time": 0.5, "ok": True}]
        print([t["name"] for t in sorted(tests, key=lambda t: -t["time"])])
        print(list(map(lambda t: t["name"], filter(lambda t: not t["ok"], tests))))
        """),
    out(f"{P}-practice-e2", "Что выведет программа?", """
        from functools import reduce
        tests = [{"time": 1.2}, {"time": 3.4}, {"time": 0.5}]
        print(round(reduce(lambda acc, t: acc + t["time"], tests, 0), 1))
        print(max(tests, key=lambda t: t["time"])["time"])
        """),
    out(f"{P}-practice-e3", "Что выведет программа? Обработчики ответов.", """
        handlers = {
            200: lambda body: f"ok: {body}",
            404: lambda body: "не найдено",
        }
        for code, body in [(200, "{}"), (404, ""), (500, "x")]:
            print(handlers.get(code, lambda b: f"ошибка {code}")(body))
        """),
    cod(f"{P}-practice-e4", t("""
        Напиши функцию `failed_names(tests)` — имена упавших тестов (`"ok": False`) через `filter` и `map` с лямбдами.
        """),
        """
        def failed_names(tests):
            pass
        """,
        """
        def test_values():
            tests = [{"name": "a", "ok": True}, {"name": "b", "ok": False}]
            assert failed_names(tests) == ["b"] and failed_names([]) == [], "Неверный результат"
        """,
        """
        def failed_names(tests):
            return list(map(lambda t: t["name"], filter(lambda t: not t["ok"], tests)))
        """),
    cod(f"{P}-practice-e5", t("""
        Напиши функцию `total_time(tests)` — сумма времени через `reduce` с лямбдой, округлённая до 2 знаков.
        """),
        """
        from functools import reduce

        def total_time(tests):
            pass
        """,
        """
        def test_values():
            assert [total_time([{"time": 1.2}, {"time": 3.4}]), total_time([])] == [4.6, 0], "Неверная сумма"
        """,
        """
        from functools import reduce

        def total_time(tests):
            return round(reduce(lambda acc, t: acc + t["time"], tests, 0), 2)
        """),
    cod(f"{P}-practice-e6", t("""
        Напиши функцию `rank_tests(tests)` — сначала упавшие, внутри — по времени по убыванию. Вернуть имена.
        """),
        """
        def rank_tests(tests):
            pass
        """,
        """
        def test_values():
            tests = [{"name": "a", "ok": True, "time": 5}, {"name": "b", "ok": False, "time": 1}, {"name": "c", "ok": False, "time": 3}]
            assert rank_tests(tests) == ["c", "b", "a"], f"Получено {rank_tests(tests)}"
        """,
        """
        def rank_tests(tests):
            return [t["name"] for t in sorted(tests, key=lambda t: (t["ok"], -t["time"]))]
        """, hint="False < True: упавшие (ok=False) окажутся первыми."),
    cod(f"{P}-practice-e7", t("""
        Напиши функцию `handle(code, body)` — словарь обработчиков: `200` → `"ok: <body>"`, `404` → `"не найдено"`; для остальных кодов — `"ошибка <code>"` (обработчик по умолчанию через `get`).
        """),
        """
        def handle(code, body):
            pass
        """,
        """
        def test_values():
            assert [handle(200, "{}"), handle(404, ""), handle(500, "x")] == ["ok: {}", "не найдено", "ошибка 500"], "Неверный результат"
        """,
        """
        HANDLERS = {
            200: lambda body: f"ok: {body}",
            404: lambda body: "не найдено",
        }

        def handle(code, body):
            return HANDLERS.get(code, lambda b: f"ошибка {code}")(body)
        """),
    cod(f"{P}-practice-e8", t("""
        Напиши функцию `build_report(tests, formatter=...)` — список строк отчёта: `formatter(t)` для каждого теста. По умолчанию `formatter` — лямбда, возвращающая `"<name>: ok"` или `"<name>: fail"`.

        ```
        build_report([{"name": "a", "ok": True}])                              # → ["a: ok"]
        build_report([{"name": "a", "ok": True}], lambda t: t["name"].upper())  # → ["A"]
        ```
        """),
        """
        def build_report(tests, formatter=None):
            pass
        """,
        """
        def test_values():
            tests = [{"name": "a", "ok": True}, {"name": "b", "ok": False}]
            assert build_report(tests) == ["a: ok", "b: fail"], "Формат по умолчанию"
            assert build_report(tests, lambda t: t["name"].upper()) == ["A", "B"], "Свой форматтер"
        """,
        """
        def build_report(tests, formatter=lambda t: f"{t['name']}: {'ok' if t['ok'] else 'fail'}"):
            return [formatter(t) for t in tests]
        """, hint="Лямбда — неизменяемое значение по умолчанию, в отличие от списка."),
),
)
