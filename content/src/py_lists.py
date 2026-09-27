"""Тема «Списки»."""
from ._lib import cod, lesson, module, out, q, t, topic

P = "lst"

# ============================================================
m1 = module(f"{P}-m1", "Основы списков", "📋", "Создание, добавление и удаление элементов",

lesson(f"{P}-m1-l1", "Создание списка и доступ к элементам", """
    # Список (list)

    ```
    fruits = ["яблоко", "банан", "киви"]
    fruits[0]        # "яблоко" — нумерация с нуля
    fruits[-1]       # "киви" — с конца
    len(fruits)      # 3
    "киви" in fruits # True
    fruits[1] = "манго"   # список можно изменять
    ```

    - Может хранить что угодно, даже разные типы: `[1, "a", None]`.
    - Пустой список: `[]` или `list()`.
    """,
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        nums = [10, 20, 30, 40]
        print(nums[0], nums[2], nums[-1])
        print(len(nums))
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа?", """
        items = ["a", "b", "c"]
        items[1] = "B"
        print(items)
        print("b" in items, "B" in items)
        print(list("abc"))
        """),
    cod(f"{P}-m1-l1-e3", t("""
        Напиши функцию `first_last(items)`, которая возвращает **новый список** из первого и последнего элемента.

        Примеры:
        ```
        first_last([1, 2, 3])   # → [1, 3]
        first_last([7])         # → [7, 7]
        ```
        """),
        """
        def first_last(items):
            pass
        """,
        """
        def test_values():
            assert first_last([1, 2, 3]) == [1, 3] and first_last(["a", "b"]) == ["a", "b"] and first_last([7]) == [7, 7], "Неверный результат"
        """,
        """
        def first_last(items):
            return [items[0], items[-1]]
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `replace_first(items, value)`, которая **заменяет первый элемент** списка на `value` и возвращает этот же список.

        Пример:
        ```
        replace_first(["a", "b"], "z")   # → ["z", "b"]
        ```
        """),
        """
        def replace_first(items, value):
            pass
        """,
        """
        def test_replace():
            data = ["a", "b", "c"]
            result = replace_first(data, "z")
            assert result == ["z", "b", "c"], f"Получено {result}"
            assert data == ["z", "b", "c"], "Нужно изменить сам список"
        """,
        """
        def replace_first(items, value):
            items[0] = value
            return items
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `middle(items)`, которая возвращает **средний элемент** списка нечётной длины.

        Индекс середины — `len(items) // 2`.

        Примеры:
        ```
        middle([1, 2, 3])         # → 2
        middle(["a", "b", "c", "d", "e"])   # → "c"
        middle([42])              # → 42
        ```
        """),
        """
        def middle(items):
            pass
        """,
        """
        def test_values():
            assert middle([1, 2, 3]) == 2 and middle(["a", "b", "c", "d", "e"]) == "c" and middle([42]) == 42, "Неверный средний элемент"
        """,
        """
        def middle(items):
            return items[len(items) // 2]
        """),
    full="""
    ## Зачем это нужно

    Данных почти всегда больше одного: список пользователей, результаты прогона тестов, строки лога, коды ответов. Список (`list`) — главная коллекция Python: упорядоченная, изменяемая, может хранить элементы любых типов.

    ## Как это работает

    ### Создание

    ```py
    empty = []
    nums = [1, 2, 3]
    mixed = [1, "текст", None, [4, 5]]
    letters = list("abc")        # ['a', 'b', 'c'] — из любого итерируемого
    ```

    ### Доступ по индексу

    - Индексы начинаются с **нуля**: первый элемент — `items[0]`.
    - Отрицательные считают с конца: `items[-1]` — последний, `items[-2]` — предпоследний.
    - Несуществующий индекс — `IndexError`.

    ### Изменение

    Списки **изменяемые**: `items[1] = "новое"` меняет элемент на месте.

    ### Полезное

    - `len(items)` — количество элементов;
    - `x in items` — есть ли элемент;
    - `items == other` — сравнение поэлементно.

    ## Примеры

    ### Пример 1. Индексы

    ```python
    tests = ["login", "search", "cart", "pay"]
    print(tests[0], tests[1], tests[-1], tests[-2])
    print(len(tests), "cart" in tests, "admin" in tests)
    ```

    ### Пример 2. Изменение элемента

    ```python
    statuses = ["pass", "pass", "fail"]
    statuses[2] = "pass"
    print(statuses)
    print(statuses == ["pass"] * 3)
    ```

    ### Пример 3. Разные типы и вложенность

    ```python
    row = ["test_login", 1.25, True, ["smoke", "auth"]]
    name, duration, passed, tags = row
    print(name, duration, passed, tags[0])
    ```

    ### Пример 4. IndexError

    ```python
    items = [1, 2, 3]
    try:
        print(items[3])
    except IndexError as e:
        print("ошибка:", e)
    print(items[len(items) - 1])
    ```

    ## Частые ошибки

    **Индексация с единицы** — `items[1]` это второй элемент.

    **`items[len(items)]`** — выход за границу; последний — `items[-1]`.

    **Путаница `in` для списка и строки** — `"a" in ["abc"]` — `False`: ищется элемент целиком, а не подстрока.

    ## Шпаргалка

    ```py
    xs = [1, 2, 3]
    xs[0]  xs[-1]  len(xs)  2 in xs
    xs[1] = 20       # изменить
    list("abc")      # из строки
    ```
    """,
    quiz=[
        q("Какой индекс у первого элемента списка?", ["`1`", "`0`", "`-1`", "Зависит от списка"], 1, "Индексация в Python начинается с нуля."),
        q("Что вернёт `[\"abc\", \"d\"].__contains__(\"a\")` (то же, что `\"a\" in [\"abc\", \"d\"]`)?", ["`True`", "`False`", "Ошибка", "`\"abc\"`"], 1,
          "`in` для списка ищет элемент целиком; `\"a\"` не равно ни `\"abc\"`, ни `\"d\"`."),
        q("Что вернёт `[10, 20, 30][-2]`?", ["`10`", "`20`", "`30`", "Ошибка"], 1, "`-1` — последний, `-2` — предпоследний."),
    ]),

lesson(f"{P}-m1-l2", "Добавление элементов", """
    # Добавление

    - `items.append(x)` — в конец
    - `items.insert(i, x)` — на позицию `i`
    - `items.extend(other)` — добавить все элементы другого списка
    - `a + b` — **новый** список-склейка (исходные не меняются)

    `append`, `insert`, `extend` меняют список **на месте** и возвращают `None`.
    """,
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        items = ["b"]
        items.append("c")
        items.insert(0, "a")
        print(items)
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа? append против extend.", """
        a = [1, 2]
        b = [1, 2]
        a.append([3, 4])
        b.extend([3, 4])
        print(a, len(a))
        print(b, len(b))
        """, hint="`append` добавляет весь объект одним элементом."),
    cod(f"{P}-m1-l2-e3", t("""
        Напиши функцию `add_log(log, message)`, которая добавляет сообщение **в конец** списка `log` и возвращает сам список.

        Пример:
        ```
        add_log(["старт"], "шаг 1")   # → ["старт", "шаг 1"]
        ```
        """),
        """
        def add_log(log, message):
            pass
        """,
        """
        def test_add():
            log = ["старт"]
            assert add_log(log, "шаг 1") == ["старт", "шаг 1"] and log == ["старт", "шаг 1"], "Сообщение должно добавиться в конец этого же списка"
        """,
        """
        def add_log(log, message):
            log.append(message)
            return log
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `build_range(n)`, которая строит список чисел от 1 до `n` **с помощью цикла и `append`** (без `list(range(...))`).

        Примеры:
        ```
        build_range(4)   # → [1, 2, 3, 4]
        build_range(0)   # → []
        ```
        """),
        """
        def build_range(n):
            result = []
            return result
        """,
        """
        def test_values():
            assert build_range(4) == [1, 2, 3, 4] and build_range(0) == [] and build_range(1) == [1], "Неверный список"

        def test_append():
            assert ".append(" in open("solution.py", encoding="utf-8").read(), "Используй append"
        """,
        """
        def build_range(n):
            result = []
            for i in range(1, n + 1):
                result.append(i)
            return result
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `merge_suites(smoke, regress)`, которая возвращает **новый** список: сначала все тесты `smoke`, потом все `regress`.

        Исходные списки **не должны измениться**.

        Пример:
        ```
        merge_suites(["login"], ["pay", "cart"])   # → ["login", "pay", "cart"]
        ```
        """),
        """
        def merge_suites(smoke, regress):
            pass
        """,
        """
        def test_merge():
            a, b = ["login"], ["pay", "cart"]
            assert merge_suites(a, b) == ["login", "pay", "cart"], "Неверный порядок"
            assert a == ["login"] and b == ["pay", "cart"], "Исходные списки изменились — нужен новый список"
        """,
        """
        def merge_suites(smoke, regress):
            return smoke + regress
        """),
    full="""
    ## Зачем это нужно

    Списки растут по ходу работы программы: собираем упавшие тесты, накапливаем строки отчёта, склеиваем наборы проверок. Важно понимать разницу между методами, которые **меняют список на месте**, и операциями, которые **создают новый**.

    ## Как это работает

    ### Меняют список на месте (возвращают None)

    - `append(x)` — добавить один элемент в конец. Если `x` — список, он добавится **целиком одним элементом**.
    - `extend(iterable)` — добавить **все** элементы другой коллекции.
    - `insert(i, x)` — вставить перед позицией `i` (`insert(0, x)` — в начало).
    - `items += other` — то же, что `extend`.

    ### Создают новый список

    - `a + b` — склейка;
    - `a * 3` — повтор.

    ### Скорость

    `append` в конец — мгновенно. `insert(0, x)` — медленно на больших списках: все элементы сдвигаются. Для очередей с добавлением в начало есть `collections.deque`.

    ## Примеры

    ### Пример 1. append, insert, extend

    ```python
    steps = ["открыть страницу"]
    steps.append("ввести логин")
    steps.insert(0, "запустить браузер")
    steps.extend(["нажать Войти", "проверить URL"])
    for i, s in enumerate(steps, 1):
        print(i, s)
    ```

    ### Пример 2. append списка против extend

    ```python
    a, b = [1, 2], [1, 2]
    a.append([3, 4])
    b.extend([3, 4])
    print(a, len(a))
    print(b, len(b))
    ```

    ### Пример 3. + создаёт новый список

    ```python
    smoke = ["login"]
    regress = ["pay", "cart"]
    all_tests = smoke + regress
    all_tests.append("logout")
    print(all_tests)
    print(smoke, regress)          # исходные не изменились
    ```

    ### Пример 4. Ловушка: результат append

    ```python
    items = [1, 2]
    result = items.append(3)
    print(result)       # None!
    print(items)
    ```

    ## Частые ошибки

    **`items = items.append(x)`** — `items` станет `None`.

    **`append` вместо `extend`** — получается вложенный список.

    **`extend` строкой** — `items.extend("abc")` добавит три символа, а не одну строку.

    ## Шпаргалка

    ```py
    xs.append(x)        # один в конец
    xs.extend([a, b])   # несколько в конец
    xs.insert(0, x)     # в начало
    ys = xs + [x]       # новый список
    ```
    """,
    quiz=[
        q("Какой длины станет `[1, 2]` после `.append([3, 4])`?", ["`4`", "`3`", "`2`", "Ошибка"], 1, "`append` добавляет весь список одним элементом: `[1, 2, [3, 4]]`."),
        q("Что будет в `x` после `x = [1].append(2)`?", ["`[1, 2]`", "`None`", "`2`", "Ошибка"], 1, "`append` меняет список на месте и возвращает `None`."),
        q("Что даст `[\"a\"].extend(\"bc\")` для списка?", ["`['a', 'bc']`", "`['a', 'b', 'c']`", "Ошибка", "`['abc']`"], 1, "`extend` перебирает строку по символам и добавляет каждый."),
    ]),

lesson(f"{P}-m1-l3", "Удаление элементов", """
    # Удаление

    - `items.remove(x)` — удалить **первое** вхождение значения (нет — `ValueError`)
    - `items.pop()` — удалить и **вернуть** последний; `pop(i)` — по индексу
    - `del items[i]` — удалить по индексу
    - `items.clear()` — очистить весь список
    """,
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        items = ["a", "b", "c", "b"]
        items.remove("b")
        print(items)
        last = items.pop()
        print(last, items)
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа?", """
        nums = [10, 20, 30, 40]
        del nums[1]
        first = nums.pop(0)
        print(first, nums)
        nums.clear()
        print(nums, len(nums))
        """),
    cod(f"{P}-m1-l3-e3", t("""
        Напиши функцию `safe_remove(items, value)`, которая удаляет **первое** вхождение `value`, если оно есть, и возвращает `True`. Если значения нет — ничего не делает и возвращает `False` (без ошибки).

        Примеры:
        ```
        data = ["a", "b"]
        safe_remove(data, "a")   # → True,  data == ["b"]
        safe_remove(data, "z")   # → False, data не изменилась
        ```
        """),
        """
        def safe_remove(items, value):
            pass
        """,
        """
        def test_remove():
            data = ["a", "b", "a"]
            assert safe_remove(data, "a") is True and data == ["b", "a"], "Удалить нужно только первое вхождение"

        def test_missing():
            data = ["a"]
            assert safe_remove(data, "z") is False and data == ["a"], "Без значения — False и никаких изменений"
        """,
        """
        def safe_remove(items, value):
            if value in items:
                items.remove(value)
                return True
            return False
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `remove_all(items, value)`, которая удаляет **все** вхождения `value` из списка (изменяет сам список) и возвращает, **сколько** элементов удалено.

        Пример:
        ```
        data = [1, 2, 1, 3, 1]
        remove_all(data, 1)   # → 3, data == [2, 3]
        ```
        """),
        """
        def remove_all(items, value):
            pass
        """,
        """
        def test_remove_all():
            data = [1, 2, 1, 3, 1]
            assert remove_all(data, 1) == 3, "Удалено должно быть 3 элемента"
            assert data == [2, 3], f"В списке осталось {data}"

        def test_nothing():
            data = [5]
            assert remove_all(data, 9) == 0 and data == [5], "Нечего удалять — 0"
        """,
        """
        def remove_all(items, value):
            count = 0
            while value in items:
                items.remove(value)
                count += 1
            return count
        """,
        hint="Цикл `while value in items:` + `remove` + счётчик.", xp=20),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `process_queue(queue)`, которая обрабатывает очередь задач **с начала**: пока очередь не пуста, извлекает первый элемент (`pop(0)`) и добавляет строку `"done: <задача>"` в список результатов. Вернуть список результатов.

        После работы исходная очередь должна стать пустой.

        Пример:
        ```
        q = ["build", "test"]
        process_queue(q)   # → ["done: build", "done: test"],  q == []
        ```
        """),
        """
        def process_queue(queue):
            results = []
            return results
        """,
        """
        def test_queue():
            q = ["build", "test", "deploy"]
            assert process_queue(q) == ["done: build", "done: test", "done: deploy"], "Неверный порядок обработки"
            assert q == [], "Очередь должна опустеть"
        """,
        """
        def process_queue(queue):
            results = []
            while queue:
                task = queue.pop(0)
                results.append(f"done: {task}")
            return results
        """),
    full="""
    ## Зачем это нужно

    Из списков приходится удалять: отработанные задачи из очереди, отключённые тесты из набора, дубликаты. Методов удаления несколько, и они различаются тем, **по чему** удаляют (значение или индекс) и **что** возвращают.

    ## Как это работает

    - `remove(x)` — по **значению**, только первое вхождение. Если значения нет — `ValueError`.
    - `pop()` — удаляет последний элемент и **возвращает** его. `pop(i)` — по индексу. На пустом списке — `IndexError`.
    - `del items[i]` — по индексу, ничего не возвращает. Умеет удалять и срезы: `del items[1:3]`.
    - `clear()` — удалить всё.

    ### Опасность: удаление во время перебора

    ```py
    for x in items:
        if bad(x):
            items.remove(x)     # элементы «перескакиваются»!
    ```

    Когда элемент удаляется, следующий сдвигается на его место, а цикл идёт дальше — один элемент оказывается пропущен. Правильно — собрать **новый** список из нужных элементов (или перебирать копию `items[:]`).

    ## Примеры

    ### Пример 1. Разные способы

    ```python
    items = ["a", "b", "c", "d", "b"]
    items.remove("b")
    print("remove:", items)
    print("pop():", items.pop(), items)
    print("pop(0):", items.pop(0), items)
    del items[0]
    print("del:", items)
    ```

    ### Пример 2. Очередь задач

    ```python
    queue = ["build", "test", "deploy"]
    while queue:
        task = queue.pop(0)
        print("выполняю", task, "| осталось:", queue)
    ```

    ### Пример 3. Баг удаления в цикле

    ```python
    nums = [1, 2, 2, 3]
    for n in nums:
        if n == 2:
            nums.remove(n)
    print("баг:", nums)

    nums = [1, 2, 2, 3]
    nums = [n for n in nums if n != 2]
    print("правильно:", nums)
    ```

    ### Пример 4. Безопасное удаление

    ```python
    def safe_remove(items, value):
        if value in items:
            items.remove(value)
            return True
        return False

    data = ["x", "y"]
    print(safe_remove(data, "x"), safe_remove(data, "z"), data)
    ```

    ## Частые ошибки

    **`remove` несуществующего значения** — `ValueError`. Проверяй `in` заранее.

    **`pop` из пустого списка** — `IndexError`.

    **Удаление в цикле по тому же списку** — пропуски элементов.

    ## Шпаргалка

    ```py
    xs.remove(v)        # по значению, первое
    x = xs.pop()        # последний, с возвратом
    x = xs.pop(0)       # первый
    del xs[i]           # по индексу
    xs.clear()          # всё
    xs = [x for x in xs if ok(x)]   # фильтрация вместо удаления в цикле
    ```
    """,
    quiz=[
        q("Что вернёт `[1, 2, 3].pop()`?", ["`None`", "`3`", "`[1, 2]`", "`1`"], 1, "`pop()` удаляет последний элемент и возвращает его."),
        q("Что произойдёт при `[1, 2].remove(5)`?", ["Ничего", "`ValueError`", "Удалится последний", "Вернётся False"], 1, "`remove` требует, чтобы значение было в списке."),
        q("Почему нельзя удалять элементы из списка в цикле `for` по этому же списку?", ["Это запрещено синтаксисом", "Элементы сдвигаются, и некоторые будут пропущены", "Список станет кортежем", "Это медленно"], 1,
          "После удаления следующий элемент занимает освободившийся индекс, а цикл уже переходит дальше."),
    ]),
)

# ============================================================
m2 = module(f"{P}-m2", "Работа со списками", "🔧", "Поиск, перебор и сортировка",

lesson(f"{P}-m2-l1", "Поиск и подсчёт", """
    # Поиск

    - `x in items` — есть ли элемент
    - `items.index(x)` — индекс первого вхождения (нет — `ValueError`)
    - `items.count(x)` — сколько раз встречается
    - `min(items)`, `max(items)` — наименьший/наибольший
    """,
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        codes = [200, 404, 200, 500, 200]
        print(codes.count(200), codes.index(404), 500 in codes)
        print(min(codes), max(codes))
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа?", """
        words = ["b", "a", "c", "a"]
        print(words.index("a"))
        print(words.count("z"))
        print(max(words), min(words))
        """, hint="Строки сравниваются по алфавиту."),
    cod(f"{P}-m2-l1-e3", t("""
        Напиши функцию `find_index(items, value)` — индекс первого вхождения `value` или `-1`, если его нет (без ошибки).

        Примеры:
        ```
        find_index(["a", "b"], "b")   # → 1
        find_index(["a", "b"], "z")   # → -1
        ```
        """),
        """
        def find_index(items, value):
            pass
        """,
        """
        def test_values():
            assert find_index(["a", "b", "b"], "b") == 1 and find_index(["a"], "z") == -1 and find_index([], 1) == -1, "Неверный индекс"
        """,
        """
        def find_index(items, value):
            if value in items:
                return items.index(value)
            return -1
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `pass_rate(results)` — процент прошедших тестов.

        - `results` — список строк `"pass"` и `"fail"`.
        - Вернуть целый процент `"pass"` (округление вниз через `//`). Для пустого списка — `0`.

        Примеры:
        ```
        pass_rate(["pass", "pass", "fail"])   # → 66
        pass_rate([])                         # → 0
        ```
        Используй `count`.
        """),
        """
        def pass_rate(results):
            pass
        """,
        """
        def test_values():
            assert pass_rate(["pass", "pass", "fail"]) == 66 and pass_rate([]) == 0 and pass_rate(["pass"]) == 100, "Неверный процент"
        """,
        """
        def pass_rate(results):
            if not results:
                return 0
            return results.count("pass") * 100 // len(results)
        """),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `all_indexes(items, value)` — список **всех** индексов, где встречается `value`.

        Примеры:
        ```
        all_indexes(["a", "b", "a", "c", "a"], "a")   # → [0, 2, 4]
        all_indexes([1, 2], 3)                        # → []
        ```
        Используй `enumerate`.
        """),
        """
        def all_indexes(items, value):
            pass
        """,
        """
        def test_values():
            assert all_indexes(["a", "b", "a", "c", "a"], "a") == [0, 2, 4] and all_indexes([1, 2], 3) == [], "Неверные индексы"
        """,
        """
        def all_indexes(items, value):
            result = []
            for i, item in enumerate(items):
                if item == value:
                    result.append(i)
            return result
        """, xp=20),
    full="""
    ## Зачем это нужно

    «Есть ли в ответе код 500?», «сколько тестов упало?», «на какой позиции первая ошибка?», «какое время ответа максимальное?» — поиск и подсчёт в списках нужны постоянно, в том числе в проверках автотестов.

    ## Как это работает

    - `x in items` — `True`/`False`. Самый безопасный способ проверки.
    - `items.index(x)` — индекс **первого** вхождения; если нет — `ValueError`. Можно ограничить поиск: `index(x, start, end)`.
    - `items.count(x)` — количество вхождений.
    - `min(items)`, `max(items)` — работают для чисел и строк; для пустого списка — `ValueError` (можно `max(items, default=0)`).
    - `sum(items)` — сумма чисел.

    Все эти операции перебирают список целиком — для частых проверок по большим данным лучше `set` или `dict`.

    ## Примеры

    ### Пример 1. Анализ кодов ответов

    ```python
    codes = [200, 200, 404, 500, 200, 503]
    print("всего:", len(codes))
    print("успешных:", codes.count(200))
    print("есть 5xx:", 500 in codes or 503 in codes)
    print("первая ошибка на позиции:", codes.index(404))
    ```

    ### Пример 2. Безопасный index

    ```python
    def find_index(items, value):
        return items.index(value) if value in items else -1

    print(find_index(["a", "b"], "b"), find_index(["a", "b"], "z"))
    ```

    ### Пример 3. Все позиции через enumerate

    ```python
    log = ["INFO", "ERROR", "INFO", "ERROR", "WARN"]
    errors = []
    for i, level in enumerate(log):
        if level == "ERROR":
            errors.append(i)
    print(errors)
    ```

    ### Пример 4. min/max и default

    ```python
    times = [0.3, 1.2, 0.8]
    print(min(times), max(times), round(sum(times) / len(times), 2))
    print(max([], default=0))
    ```

    ## Частые ошибки

    **`index` без проверки** — `ValueError`, если элемента нет.

    **`max([])`** — `ValueError`; используй `default=`.

    **Сравнение разных типов в `max`** — `max([1, "a"])` падает.

    ## Шпаргалка

    ```py
    x in xs           # есть ли
    xs.index(x)       # где (или ValueError)
    xs.count(x)       # сколько
    min(xs), max(xs, default=0), sum(xs)
    ```
    """,
    quiz=[
        q("Что вернёт `[1, 2, 1].index(1)`?", ["`0`", "`2`", "`[0, 2]`", "`1`"], 0, "`index` возвращает позицию первого вхождения."),
        q("Что произойдёт при `max([])`?", ["Вернёт 0", "Вернёт None", "`ValueError`", "Вернёт []"], 2, "У пустого списка нет максимума; безопасно — `max(xs, default=...)`."),
        q("Что вернёт `[\"a\", \"b\", \"a\"].count(\"a\")`?", ["`1`", "`2`", "`[0, 2]`", "`True`"], 1, "Значение встречается дважды."),
    ]),

lesson(f"{P}-m2-l2", "Перебор: for, enumerate, zip", """
    # Перебор

    ```
    for item in items:                       # элементы
    for i, item in enumerate(items, 1):      # номер + элемент
    for a, b in zip(list1, list2):           # попарно
    ```

    - Индекс нужен? — `enumerate`, а не `range(len(...))`.
    - `zip` останавливается на самом коротком списке.
    """,
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        for i, name in enumerate(["login", "pay"], start=1):
            print(i, name)
        """),
    out(f"{P}-m2-l2-e2", "Что выведет программа?", """
        names = ["a", "b", "c"]
        codes = [200, 404]
        for name, code in zip(names, codes):
            print(name, code)
        """, hint="`zip` останавливается на самом коротком."),
    cod(f"{P}-m2-l2-e3", t("""
        Напиши функцию `numbered(items)`, которая возвращает список строк вида `"<номер>. <элемент>"`, нумерация с 1.

        Пример:
        ```
        numbered(["login", "pay"])   # → ["1. login", "2. pay"]
        ```
        """),
        """
        def numbered(items):
            pass
        """,
        """
        def test_values():
            assert numbered(["login", "pay"]) == ["1. login", "2. pay"] and numbered([]) == [], "Неверный результат"
        """,
        """
        def numbered(items):
            result = []
            for i, item in enumerate(items, start=1):
                result.append(f"{i}. {item}")
            return result
        """),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `compare_results(expected, actual)`, которая сравнивает два списка попарно и возвращает список **индексов**, где значения не совпали.

        Списки одинаковой длины.

        Пример:
        ```
        compare_results([200, 201, 404], [200, 500, 404])   # → [1]
        ```
        Используй `enumerate(zip(expected, actual))`.
        """),
        """
        def compare_results(expected, actual):
            pass
        """,
        """
        def test_values():
            assert compare_results([200, 201, 404], [200, 500, 404]) == [1], "Не совпал только индекс 1"
            assert compare_results([1, 2], [3, 4]) == [0, 1] and compare_results([], []) == [], "Неверный результат"
        """,
        """
        def compare_results(expected, actual):
            diff = []
            for i, (e, a) in enumerate(zip(expected, actual)):
                if e != a:
                    diff.append(i)
            return diff
        """, xp=20),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `to_dict(keys, values)`, которая собирает словарь из двух списков: ключ из `keys`, значение из `values` на той же позиции.

        Пример:
        ```
        to_dict(["login", "pay"], [True, False])   # → {"login": True, "pay": False}
        ```
        Используй `zip` в цикле или `dict(zip(...))`.
        """),
        """
        def to_dict(keys, values):
            pass
        """,
        """
        def test_values():
            assert to_dict(["login", "pay"], [True, False]) == {"login": True, "pay": False} and to_dict([], []) == {}, "Неверный словарь"
        """,
        """
        def to_dict(keys, values):
            return dict(zip(keys, values))
        """),
    full="""
    ## Зачем это нужно

    Перебор списка — основа любой обработки данных: проверить каждый ответ, пронумеровать шаги отчёта, сравнить ожидаемые результаты с фактическими. В Python есть удобные инструменты, которые избавляют от ручной работы с индексами.

    ## Как это работает

    ### Прямой перебор

    `for item in items:` — самый частый и читаемый вариант.

    ### enumerate — номер и элемент

    `for i, item in enumerate(items):` — `i` начинается с 0; `enumerate(items, start=1)` — с единицы.

    Антипаттерн: `for i in range(len(items)): item = items[i]` — длиннее и легче ошибиться.

    ### zip — параллельный перебор

    `for a, b in zip(xs, ys):` — берёт по элементу из каждой коллекции. Останавливается на **самой короткой**. Если это недопустимо — `zip(xs, ys, strict=True)` (Python 3.10+) бросит ошибку при разной длине.

    `dict(zip(keys, values))` — классический способ собрать словарь из двух списков.

    ## Примеры

    ### Пример 1. Отчёт с номерами

    ```python
    steps = ["открыть страницу", "ввести логин", "нажать Войти"]
    for n, step in enumerate(steps, start=1):
        print(f"Шаг {n}: {step}")
    ```

    ### Пример 2. Сравнение ожидаемого и фактического

    ```python
    expected = [200, 201, 404, 200]
    actual = [200, 500, 404, 200]
    for i, (e, a) in enumerate(zip(expected, actual)):
        mark = "✅" if e == a else "❌"
        print(f"{mark} запрос {i}: ожидали {e}, получили {a}")
    ```

    ### Пример 3. zip и разная длина

    ```python
    print(list(zip([1, 2, 3], ["a", "b"])))
    try:
        list(zip([1, 2, 3], ["a", "b"], strict=True))
    except ValueError as e:
        print("strict:", e)
    ```

    ### Пример 4. Словарь из двух списков

    ```python
    names = ["login", "search", "pay"]
    durations = [1.2, 0.4, 3.1]
    timing = dict(zip(names, durations))
    print(timing)
    print("самый долгий:", max(timing, key=timing.get))
    ```

    ## Частые ошибки

    **`range(len(items))` без необходимости.**

    **Молчаливое обрезание в zip** при списках разной длины — баг прячется. Используй `strict=True`.

    **Изменение списка во время перебора** — перебирай копию или собирай новый.

    ## Шпаргалка

    ```py
    for x in xs: ...
    for i, x in enumerate(xs, start=1): ...
    for a, b in zip(xs, ys, strict=True): ...
    dict(zip(keys, values))
    ```
    """,
    quiz=[
        q("Что выведет `list(enumerate([\"a\", \"b\"]))`?", ["`[(1, 'a'), (2, 'b')]`", "`[(0, 'a'), (1, 'b')]`", "`['a', 'b']`", "`[0, 1]`"], 1, "По умолчанию `enumerate` нумерует с 0."),
        q("Сколько пар даст `zip([1, 2, 3], [\"a\"])`?", ["3", "1", "0", "Ошибка"], 1, "`zip` останавливается на самой короткой коллекции."),
        q("Как собрать словарь из списков `keys` и `values`?", ["`dict(keys, values)`", "`dict(zip(keys, values))`", "`{keys: values}`", "`zip(dict(keys), values)`"], 1, "`zip` даёт пары, `dict` превращает пары в словарь."),
    ]),

lesson(f"{P}-m2-l3", "Сортировка", """
    # Сортировка

    - `sorted(items)` — **новый** отсортированный список, исходный не меняется
    - `items.sort()` — сортирует **сам список**, возвращает `None`
    - `reverse=True` — по убыванию
    - `key=функция` — по какому признаку: `key=len`, `key=str.lower`
    - `items.reverse()` / `reversed(items)` — развернуть порядок
    """,
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        a = [3, 1, 2]
        b = sorted(a)
        print(a, b)
        a.sort(reverse=True)
        print(a)
        """),
    out(f"{P}-m2-l3-e2", "Что выведет программа? Сортировка строк.", """
        words = ["banana", "Apple", "cherry"]
        print(sorted(words))
        print(sorted(words, key=str.lower))
        print(sorted(words, key=len))
        """, hint="Заглавные буквы идут раньше строчных."),
    cod(f"{P}-m2-l3-e3", t("""
        Напиши функцию `top3(scores)` — три наибольших числа из списка, **по убыванию**. Исходный список не менять.

        Примеры:
        ```
        top3([5, 1, 9, 7, 3])   # → [9, 7, 5]
        top3([2, 1])            # → [2, 1]
        ```
        """),
        """
        def top3(scores):
            pass
        """,
        """
        def test_values():
            data = [5, 1, 9, 7, 3]
            assert top3(data) == [9, 7, 5] and top3([2, 1]) == [2, 1], "Неверный топ"
            assert data == [5, 1, 9, 7, 3], "Исходный список не должен меняться — используй sorted"
        """,
        """
        def top3(scores):
            return sorted(scores, reverse=True)[:3]
        """),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `sort_names(names)` — отсортировать имена по алфавиту **без учёта регистра** и вернуть новый список.

        Пример:
        ```
        sort_names(["боря", "Аня", "вика"])   # → ["Аня", "боря", "вика"]
        ```
        """),
        """
        def sort_names(names):
            pass
        """,
        """
        def test_values():
            assert sort_names(["боря", "Аня", "вика"]) == ["Аня", "боря", "вика"], f"Получено {sort_names(['боря', 'Аня', 'вика'])}"
            assert sort_names(["b", "A", "c"]) == ["A", "b", "c"], "Регистр не должен влиять на порядок"
        """,
        """
        def sort_names(names):
            return sorted(names, key=str.lower)
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `by_duration(tests)`, где `tests` — список пар `(имя, секунды)`. Вернуть список **имён**, отсортированных от самого долгого теста к самому быстрому.

        Пример:
        ```
        by_duration([("login", 1.2), ("pay", 3.4), ("search", 0.2)])   # → ["pay", "login", "search"]
        ```
        Ключ сортировки — второй элемент пары: `key=lambda t: t[1]`.
        """),
        """
        def by_duration(tests):
            pass
        """,
        """
        def test_values():
            got = by_duration([("login", 1.2), ("pay", 3.4), ("search", 0.2)])
            assert got == ["pay", "login", "search"], f"Получено {got}"
        """,
        """
        def by_duration(tests):
            ordered = sorted(tests, key=lambda t: t[1], reverse=True)
            return [name for name, _ in ordered]
        """, xp=20),
    full="""
    ## Зачем это нужно

    Самые медленные тесты — вверх отчёта, пользователи — по алфавиту, версии — по возрастанию. Сортировка нужна постоянно, и важно не путать сортировку «на месте» и создание нового списка, а также уметь сортировать по нужному признаку.

    ## Как это работает

    ### sorted и sort

    - `sorted(iterable)` — возвращает **новый** список; работает с любыми коллекциями (строки, кортежи, словари).
    - `list.sort()` — сортирует **сам** список, возвращает `None`. Только для списков.

    ### Параметры

    - `reverse=True` — по убыванию.
    - `key=функция` — функция вызывается для каждого элемента, сравниваются её результаты:
      - `key=len` — по длине;
      - `key=str.lower` — по алфавиту без учёта регистра;
      - `key=lambda t: t[1]` — по второму элементу пары;
      - `key=lambda u: (u["age"], u["name"])` — по двум признакам.

    ### Стабильность

    Сортировка в Python **стабильна**: элементы с одинаковым ключом сохраняют исходный порядок.

    ### Развернуть порядок

    `items.reverse()` — на месте; `reversed(items)` — итератор; `items[::-1]` — новый список.

    ## Примеры

    ### Пример 1. sorted против sort

    ```python
    a = [3, 1, 2]
    b = sorted(a)
    print("sorted:", a, b)
    result = a.sort()
    print("sort:", a, result)
    ```

    ### Пример 2. Разные ключи

    ```python
    words = ["banana", "Apple", "kiwi", "cherry"]
    print(sorted(words))
    print(sorted(words, key=str.lower))
    print(sorted(words, key=len))
    print(sorted(words, key=len, reverse=True))
    ```

    ### Пример 3. Самые медленные тесты

    ```python
    tests = [("login", 1.2), ("pay", 3.4), ("search", 0.2), ("cart", 3.4)]
    for name, sec in sorted(tests, key=lambda t: t[1], reverse=True):
        print(f"{name:8} {sec} с")
    ```

    `pay` и `cart` с одинаковым временем сохранили исходный порядок — это стабильность.

    ### Пример 4. Два критерия

    ```python
    users = [("Боря", 25), ("Аня", 30), ("Вика", 25)]
    print(sorted(users, key=lambda u: (u[1], u[0])))        # по возрасту, потом по имени
    print(sorted(users, key=lambda u: (-u[1], u[0])))       # возраст по убыванию
    ```

    ## Частые ошибки

    **`items = items.sort()`** — список превращается в `None`.

    **`key=len()`** — передаётся сама функция, без скобок.

    **Сортировка смешанных типов** — `sorted([1, "a"])` → `TypeError`.

    ## Шпаргалка

    ```py
    sorted(xs)                        # новый
    xs.sort()                         # на месте, None
    sorted(xs, reverse=True)
    sorted(xs, key=str.lower)
    sorted(pairs, key=lambda p: p[1])
    sorted(xs, key=lambda x: (x.a, -x.b))
    ```
    """,
    quiz=[
        q("Что вернёт `[3, 1, 2].sort()`?", ["`[1, 2, 3]`", "`None`", "`[3, 1, 2]`", "Ошибка"], 1, "`sort` сортирует на месте и возвращает `None`."),
        q("Как отсортировать слова по длине?", ["`sorted(words, key=len)`", "`sorted(words, len)`", "`sorted(len(words))`", "`words.sort(len)`"], 0, "В `key` передаётся функция без вызова."),
        q("Что значит «сортировка стабильна»?", ["Не падает с ошибкой", "Элементы с равным ключом сохраняют исходный порядок", "Всегда по возрастанию", "Работает быстро"], 1,
          "Благодаря стабильности можно сортировать поэтапно по нескольким признакам."),
    ]),
)

# ============================================================
m3 = module(f"{P}-m3", "Продвинутые приёмы", "🧱", "Накопление, копирование и вложенные списки",

lesson(f"{P}-m3-l1", "Накопление и фильтрация", """
    # Шаблон «собрать новый список»

    ```
    result = []
    for x in items:
        if условие(x):
            result.append(преобразовать(x))
    ```

    Встроенные агрегаты: `sum`, `min`, `max`, `len`, `any`, `all`.
    Среднее: `sum(xs) / len(xs)` (проверь, что список не пуст).
    """,
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        nums = [4, -2, 7, 0, -5]
        positive = []
        for n in nums:
            if n > 0:
                positive.append(n)
        print(positive, sum(positive))
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа?", """
        results = ["pass", "pass", "fail"]
        print(any(r == "fail" for r in results))
        print(all(r == "pass" for r in results))
        """),
    cod(f"{P}-m3-l1-e3", t("""
        Напиши функцию `only_even(nums)` — новый список только из чётных чисел, в исходном порядке. Исходный список не менять.

        Пример:
        ```
        only_even([1, 2, 3, 4, 6])   # → [2, 4, 6]
        ```
        """),
        """
        def only_even(nums):
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3, 4, 6]
            assert only_even(data) == [2, 4, 6] and only_even([1, 3]) == [], "Неверный результат"
            assert data == [1, 2, 3, 4, 6], "Исходный список не должен меняться"
        """,
        """
        def only_even(nums):
            result = []
            for n in nums:
                if n % 2 == 0:
                    result.append(n)
            return result
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `average(nums)` — среднее арифметическое, округлённое до 2 знаков. Для пустого списка вернуть `0`.

        Примеры:
        ```
        average([2, 4, 6])   # → 4.0
        average([1, 2, 2])   # → 1.67
        average([])          # → 0
        ```
        """),
        """
        def average(nums):
            pass
        """,
        """
        def test_values():
            assert average([2, 4, 6]) == 4 and average([1, 2, 2]) == 1.67 and average([]) == 0, "Неверное среднее"
        """,
        """
        def average(nums):
            if not nums:
                return 0
            return round(sum(nums) / len(nums), 2)
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `my_max(nums)` — максимум непустого списка **без** встроенной `max`.

        Примеры:
        ```
        my_max([3, 9, 2])      # → 9
        my_max([-5, -2, -9])   # → -2
        ```
        Начни не с 0, а с первого элемента — иначе сломаешься на отрицательных.
        """),
        """
        def my_max(nums):
            pass
        """,
        """
        def test_values():
            assert my_max([3, 9, 2]) == 9 and my_max([-5, -2, -9]) == -2 and my_max([4]) == 4, "Неверный максимум"

        def test_no_builtin():
            assert "max(" not in open("solution.py", encoding="utf-8").read().replace("my_max(", ""), "Не используй встроенную max"
        """,
        """
        def my_max(nums):
            best = nums[0]
            for n in nums:
                if n > best:
                    best = n
            return best
        """),
    full="""
    ## Зачем это нужно

    Большинство задач обработки данных сводится к двум шаблонам: **отфильтровать/преобразовать** список в новый или **свернуть** его в одно значение (сумму, максимум, «все ли прошли?»). Освоив их, ты решишь огромную долю практических задач.

    ## Как это работает

    ### Сбор нового списка

    ```py
    result = []                 # 1. пустой список до цикла
    for x in items:
        if подходит(x):         # 2. фильтр (необязательно)
            result.append(f(x)) # 3. преобразование
    return result               # 4. после цикла
    ```

    Короткая форма — списочное включение `[f(x) for x in items if подходит(x)]` — у него будет своя тема.

    ### Свёртка в одно значение

    - `sum(xs)`, `len(xs)`, `min(xs)`, `max(xs)`;
    - `any(условие for x in xs)` — есть ли хотя бы один;
    - `all(условие for x in xs)` — все ли;
    - ручной накопитель, если нужна своя логика: начальное значение `0` для суммы, `1` для произведения, **первый элемент** для максимума.

    ## Примеры

    ### Пример 1. Фильтр + преобразование

    ```python
    responses = [{"url": "/a", "code": 200}, {"url": "/b", "code": 500}, {"url": "/c", "code": 404}]
    broken = []
    for r in responses:
        if r["code"] >= 400:
            broken.append(f'{r["url"]} ({r["code"]})')
    print(broken)
    ```

    ### Пример 2. Статистика

    ```python
    times = [0.31, 0.29, 1.8, 0.35, 0.3]
    print("всего:", len(times))
    print("среднее:", round(sum(times) / len(times), 2))
    print("max:", max(times), "min:", min(times))
    print("медленнее секунды:", sum(1 for t in times if t > 1))
    ```

    ### Пример 3. any / all

    ```python
    results = ["pass", "pass", "skip"]
    print("есть упавшие:", any(r == "fail" for r in results))
    print("все прошли:", all(r == "pass" for r in results))
    print("все без падений:", all(r != "fail" for r in results))
    ```

    ### Пример 4. Максимум вручную

    ```python
    def my_max(nums):
        best = nums[0]
        for n in nums[1:]:
            if n > best:
                best = n
        return best

    print(my_max([-5, -2, -9]))
    ```

    ## Частые ошибки

    **Накопитель внутри цикла** — сбрасывается каждый шаг.

    **`return` внутри цикла** — функция завершится на первом элементе.

    **Деление на `len` пустого списка** — `ZeroDivisionError`.

    ## Шпаргалка

    ```py
    out = []
    for x in xs:
        if cond(x):
            out.append(f(x))
    sum(xs) / len(xs) if xs else 0
    any(...), all(...)
    ```
    """,
    quiz=[
        q("Что вернёт `all([])`?", ["`True`", "`False`", "Ошибка", "`None`"], 0, "Для пустого набора «все выполнены» вакуумно истинно."),
        q("Почему для максимума начинают с `best = nums[0]`, а не с 0?", ["Так быстрее", "Если все числа отрицательные, 0 окажется «максимумом», которого нет в списке", "Так требует синтаксис", "Без разницы"], 1,
          "Начальное значение должно быть элементом списка."),
        q("Где должен стоять `return result` в шаблоне сбора списка?", ["Внутри if", "Внутри цикла", "После цикла", "До цикла"], 2, "Результат готов только после перебора всех элементов."),
    ]),

lesson(f"{P}-m3-l2", "Копирование и ссылки", """
    # Две переменные — один список

    ```
    a = [1, 2]
    b = a          # НЕ копия — второе имя того же списка
    b.append(3)
    print(a)       # [1, 2, 3]
    ```

    Копия: `a.copy()`, `a[:]`, `list(a)`.
    Для вложенных списков — `copy.deepcopy(a)`.
    """,
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        a = [1, 2]
        b = a
        c = a.copy()
        b.append(3)
        print(a, b, c)
        print(a is b, a is c)
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа? Мелкая копия вложенного списка.", """
        a = [[1], [2]]
        b = a.copy()
        b[0].append(99)
        print(a)
        """, hint="`copy()` копирует только внешний список; вложенные списки общие."),
    cod(f"{P}-m3-l2-e3", t("""
        Напиши функцию `with_item(items, value)`, которая возвращает **новый** список — копию `items` с добавленным в конец `value`. Исходный список не должен измениться.

        Пример:
        ```
        a = [1, 2]
        with_item(a, 3)   # → [1, 2, 3], а a по-прежнему [1, 2]
        ```
        """),
        """
        def with_item(items, value):
            items.append(value)
            return items
        """,
        """
        def test_new_list():
            a = [1, 2]
            b = with_item(a, 3)
            assert b == [1, 2, 3], "В результате должен быть новый элемент"
            assert a == [1, 2], "Исходный список изменился — нужно работать с копией"
            assert a is not b, "Нужен новый список"
        """,
        """
        def with_item(items, value):
            result = items.copy()
            result.append(value)
            return result
        """),
    cod(f"{P}-m3-l2-e4", t("""
        В функции `reset_scores` баг: она должна вернуть **новый** список той же длины, заполненный нулями, но портит исходные данные.

        Исправь её так, чтобы исходный список не менялся.

        Пример:
        ```
        scores = [5, 3, 8]
        reset_scores(scores)   # → [0, 0, 0], а scores == [5, 3, 8]
        ```
        """),
        """
        def reset_scores(scores):
            result = scores
            for i in range(len(result)):
                result[i] = 0
            return result
        """,
        """
        def test_reset():
            scores = [5, 3, 8]
            assert reset_scores(scores) == [0, 0, 0], "Нужен список нулей"
            assert scores == [5, 3, 8], "Исходный список испорчен"
        """,
        """
        def reset_scores(scores):
            return [0] * len(scores)
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `clone_matrix(matrix)`, которая возвращает **полную (глубокую) копию** списка списков: изменения во вложенных списках копии не должны влиять на оригинал.

        Используй `copy.deepcopy` (не забудь `import copy`).

        Пример:
        ```
        m = [[1, 2], [3, 4]]
        c = clone_matrix(m)
        c[0][0] = 99    # m остаётся [[1, 2], [3, 4]]
        ```
        """),
        """
        def clone_matrix(matrix):
            return matrix.copy()
        """,
        """
        def test_deep():
            m = [[1, 2], [3, 4]]
            c = clone_matrix(m)
            c[0][0] = 99
            assert m == [[1, 2], [3, 4]], "Оригинал изменился — копия должна быть глубокой"
            assert c == [[99, 2], [3, 4]], "Копия должна содержать те же данные"
        """,
        """
        import copy

        def clone_matrix(matrix):
            return copy.deepcopy(matrix)
        """),
    full="""
    ## Зачем это нужно

    Один из самых коварных багов новичков — «я изменил одну переменную, а поменялась другая». В тестах это превращается в «тесты влияют друг на друга»: один тест испортил общий список тестовых данных, и следующий падает. Причина — ссылки на один и тот же объект.

    ## Как это работает

    ### Переменная — ссылка

    Переменная в Python — это ярлык на объект. `b = a` вешает второй ярлык на **тот же** список. Изменение через любое имя видно через оба.

    Проверка: `a is b` — один ли это объект; `a == b` — равны ли значения.

    ### Мелкая копия

    Новый внешний список с теми же элементами:
    - `a.copy()`
    - `a[:]`
    - `list(a)`

    Для списка чисел или строк этого достаточно: они неизменяемые.

    ### Глубокая копия

    Если внутри списки или словари, мелкая копия копирует только **ссылки** на них. Изменение вложенного объекта затронет оригинал. Решение — `copy.deepcopy(a)`: копирует всё рекурсивно.

    ### Ловушка `[[0] * 3] * 3`

    Умножение списка копирует **ссылки**: получаются три ссылки на одну и ту же строку матрицы.

    ## Примеры

    ### Пример 1. Ссылка против копии

    ```python
    a = [1, 2]
    b = a
    c = a.copy()
    b.append(3)
    print("a:", a, "| b:", b, "| c:", c)
    print("a is b:", a is b, "| a is c:", a is c, "| a == c:", a == c)
    ```

    ### Пример 2. Мелкая копия и вложенность

    ```python
    import copy
    original = [["login"], ["pay"]]
    shallow = original.copy()
    deep = copy.deepcopy(original)
    shallow[0].append("logout")
    print("original:", original)
    print("deep:", deep)
    ```

    ### Пример 3. Ловушка умножения

    ```python
    grid = [[0] * 3] * 3
    grid[0][0] = 1
    print(grid)
    grid = [[0] * 3 for _ in range(3)]
    grid[0][0] = 1
    print(grid)
    ```

    ### Пример 4. Функция портит аргумент

    ```python
    def add_default_tag(tags):
        tags.append("regress")
        return tags

    my_tags = ["smoke"]
    add_default_tag(my_tags)
    print("изменён снаружи:", my_tags)
    ```

    ## Частые ошибки

    **`b = a` в надежде получить копию.**

    **Мелкая копия для вложенных данных.**

    **`[[]] * n`** — n ссылок на один список.

    **Функции, незаметно меняющие переданный список** — возвращай новый или явно документируй изменение.

    ## Шпаргалка

    ```py
    b = a              # то же самое
    b = a.copy()       # мелкая копия (a[:], list(a))
    b = copy.deepcopy(a)   # глубокая
    a is b             # тот же объект?
    [[0] * n for _ in range(m)]   # правильная матрица
    ```
    """,
    quiz=[
        q("После `a = [1]; b = a; b.append(2)` чему равно `a`?", ["`[1]`", "`[1, 2]`", "`[2]`", "Ошибка"], 1, "`a` и `b` указывают на один список."),
        q("Что выведет `g = [[0] * 2] * 2; g[0][0] = 1; print(g)`?", ["`[[1, 0], [0, 0]]`", "`[[1, 0], [1, 0]]`", "`[[1, 1], [0, 0]]`", "Ошибка"], 1,
          "Обе строки — один и тот же список, поэтому изменение видно в обеих."),
        q("Когда нужен `copy.deepcopy`?", ["Всегда", "Когда внутри есть изменяемые объекты (списки, словари) и их нужно скопировать тоже", "Для списков чисел", "Никогда"], 1,
          "Мелкая копия копирует лишь ссылки на вложенные объекты."),
    ]),

lesson(f"{P}-m3-l3", "Вложенные списки", """
    # Список списков

    ```
    matrix = [[1, 2, 3],
              [4, 5, 6]]
    matrix[1][2]      # 6 — строка 1, столбец 2
    len(matrix)       # 2 строки
    len(matrix[0])    # 3 столбца
    ```

    Перебор:
    ```
    for row in matrix:
        for value in row:
            ...
    ```
    """,
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        m = [[1, 2, 3], [4, 5, 6]]
        print(m[0][1], m[1][0], m[-1][-1])
        print(len(m), len(m[0]))
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа?", """
        table = [["login", "pass"], ["pay", "fail"]]
        for name, status in table:
            print(name, "->", status)
        """),
    cod(f"{P}-m3-l3-e3", t("""
        Напиши функцию `matrix_sum(matrix)` — сумма **всех** чисел в списке списков.

        Пример:
        ```
        matrix_sum([[1, 2], [3, 4]])   # → 10
        matrix_sum([[], [5]])          # → 5
        ```
        """),
        """
        def matrix_sum(matrix):
            pass
        """,
        """
        def test_values():
            assert matrix_sum([[1, 2], [3, 4]]) == 10 and matrix_sum([[], [5]]) == 5 and matrix_sum([]) == 0, "Неверная сумма"
        """,
        """
        def matrix_sum(matrix):
            total = 0
            for row in matrix:
                for value in row:
                    total += value
            return total
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `column(matrix, index)` — список значений из столбца с номером `index`.

        Пример:
        ```
        column([[1, 2, 3], [4, 5, 6]], 1)   # → [2, 5]
        ```
        """),
        """
        def column(matrix, index):
            pass
        """,
        """
        def test_values():
            m = [[1, 2, 3], [4, 5, 6]]
            assert column(m, 1) == [2, 5] and column(m, 0) == [1, 4] and column(m, -1) == [3, 6], "Неверный столбец"
        """,
        """
        def column(matrix, index):
            return [row[index] for row in matrix]
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `flatten(nested)` — превратить список списков в один плоский список.

        Пример:
        ```
        flatten([[1, 2], [], [3], [4, 5]])   # → [1, 2, 3, 4, 5]
        ```
        """),
        """
        def flatten(nested):
            pass
        """,
        """
        def test_values():
            assert flatten([[1, 2], [], [3], [4, 5]]) == [1, 2, 3, 4, 5] and flatten([]) == [], "Неверный результат"
        """,
        """
        def flatten(nested):
            result = []
            for inner in nested:
                result.extend(inner)
            return result
        """),
    full="""
    ## Зачем это нужно

    Табличные данные — строки CSV, результаты тестов по браузерам, игровое поле, матрица прав доступа — удобно хранить как список списков. Нужно уметь обращаться к ячейкам, перебирать строки и столбцы, сворачивать вложенность.

    ## Как это работает

    ```py
    matrix = [
        [1, 2, 3],     # строка 0
        [4, 5, 6],     # строка 1
    ]
    ```

    - `matrix[i]` — строка (сам список);
    - `matrix[i][j]` — ячейка: сначала строка, потом столбец;
    - `len(matrix)` — число строк, `len(matrix[0])` — число столбцов.

    ### Перебор

    - По строкам: `for row in matrix:`
    - По ячейкам: вложенный цикл.
    - С координатами: `for i, row in enumerate(matrix): for j, value in enumerate(row):`
    - Распаковка строк фиксированной длины: `for name, status in table:`

    ### Столбец

    Отдельно столбцы не хранятся: `[row[j] for row in matrix]`. Транспонирование — `list(zip(*matrix))`.

    ## Примеры

    ### Пример 1. Доступ к ячейкам

    ```python
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(m[1], m[1][2], m[-1][0])
    print("диагональ:", [m[i][i] for i in range(len(m))])
    ```

    ### Пример 2. Таблица результатов

    ```python
    results = [
        ["test", "chrome", "firefox"],
        ["login", "pass", "pass"],
        ["pay", "pass", "fail"],
    ]
    header, *rows = results
    for name, *statuses in rows:
        broken = [header[i + 1] for i, s in enumerate(statuses) if s == "fail"]
        print(name, "— упал в:", broken or "нигде")
    ```

    ### Пример 3. Столбцы и транспонирование

    ```python
    m = [[1, 2, 3], [4, 5, 6]]
    print([row[1] for row in m])
    print(list(zip(*m)))
    ```

    ### Пример 4. Сплющивание

    ```python
    nested = [["a", "b"], [], ["c"]]
    flat = []
    for inner in nested:
        flat.extend(inner)
    print(flat)
    ```

    ## Частые ошибки

    **Перепутанный порядок индексов** — `m[столбец][строка]`.

    **Создание матрицы через `[[0] * n] * m`** — строки общие.

    **Строки разной длины** — `row[j]` может упасть с `IndexError`.

    ## Шпаргалка

    ```py
    m[i][j]                       # строка i, столбец j
    for row in m: for x in row: ...
    [row[j] for row in m]         # столбец
    list(zip(*m))                 # транспонирование
    [[0] * cols for _ in range(rows)]
    ```
    """,
    quiz=[
        q("Что вернёт `[[1, 2], [3, 4]][1][0]`?", ["`2`", "`3`", "`[3, 4]`", "`1`"], 1, "Строка 1 — `[3, 4]`, её элемент 0 — `3`."),
        q("Как получить количество столбцов матрицы `m`?", ["`len(m)`", "`len(m[0])`", "`m.cols`", "`len(m[0][0])`"], 1, "`len(m)` — строки, `len(m[0])` — элементы первой строки, то есть столбцы."),
        q("Что даст `list(zip(*[[1, 2], [3, 4]]))`?", ["`[[1, 2], [3, 4]]`", "`[(1, 3), (2, 4)]`", "`[1, 2, 3, 4]`", "Ошибка"], 1, "`zip(*m)` собирает элементы одного столбца — это транспонирование."),
    ]),
)

TOPIC = topic("py-lists", "Списки", "📋", "#1cb0f6",
              "Создание, изменение, поиск, перебор, сортировка и копирование списков",
              m1, m2, m3, group="Python")
