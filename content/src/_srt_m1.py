"""Тема «sorted, filter и map», модуль 1 «Сортировка» — задания. Теория — в _srt_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "srt"

m1 = module(f"{P}-m1", "Сортировка", "🔢", "sorted и sort, key, несколько признаков, словари и записи",

lesson(f"{P}-m1-l1", "sorted и list.sort",
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        nums = [3, 1, 2]
        result = sorted(nums)
        print(result, nums)
        nums.sort()
        print(nums)
        """, hint="sorted возвращает новый список, sort меняет исходный."),
    out(f"{P}-m1-l1-e2", "Что выведет программа? Ловушка sort.", """
        nums = [3, 1, 2]
        x = nums.sort()
        print(x, nums)
        """, hint="Методы, меняющие объект на месте, возвращают None."),
    out(f"{P}-m1-l1-e3", "Что выведет программа?", """
        print(sorted("банан"))
        print(sorted((3, 1, 2), reverse=True))
        print(sorted(["b", "B", "a", "A"]))
        """, hint="Заглавные буквы идут раньше строчных."),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `sorted_copy(nums)` — вернуть отсортированную копию списка, **не меняя** исходный.

        ```
        src = [3, 1, 2]
        sorted_copy(src)   # → [1, 2, 3]
        src                # → [3, 1, 2]
        ```
        """),
        """
        def sorted_copy(nums):
            pass
        """,
        """
        def test_values():
            src = [3, 1, 2]
            assert sorted_copy(src) == [1, 2, 3] and src == [3, 1, 2], "Неверный результат или исходный изменён"
        """,
        """
        def sorted_copy(nums):
            return sorted(nums)
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `sort_in_place(nums)` — отсортировать список **по убыванию на месте**. Функция ничего не возвращает.
        """),
        """
        def sort_in_place(nums):
            pass
        """,
        """
        def test_values():
            a = [3, 1, 2]
            assert sort_in_place(a) is None and a == [3, 2, 1], f"a = {a}"
        """,
        """
        def sort_in_place(nums):
            nums.sort(reverse=True)
        """),
    cod(f"{P}-m1-l1-e6", t("""
        Напиши функцию `top3(scores)` — три наибольших числа по убыванию (если чисел меньше — сколько есть).

        ```
        top3([50, 90, 70, 80])   # → [90, 80, 70]
        ```
        """),
        """
        def top3(scores):
            pass
        """,
        """
        def test_values():
            assert [top3([50, 90, 70, 80]), top3([1]), top3([])] == [[90, 80, 70], [1], []], "Неверный результат"
        """,
        """
        def top3(scores):
            return sorted(scores, reverse=True)[:3]
        """),
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `median(nums)` — медиана непустого списка: средний элемент отсортированного списка; для чётной длины — среднее двух средних.

        ```
        median([3, 1, 2])      # → 2
        median([4, 1, 3, 2])   # → 2.5
        ```
        """),
        """
        def median(nums):
            pass
        """,
        """
        def test_values():
            assert [median([3, 1, 2]), median([4, 1, 3, 2]), median([5])] == [2, 2.5, 5], "Неверная медиана"
        """,
        """
        def median(nums):
            s = sorted(nums)
            mid = len(s) // 2
            if len(s) % 2 == 1:
                return s[mid]
            return (s[mid - 1] + s[mid]) / 2
        """, xp=20),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `is_sorted(nums)` — отсортирован ли список по возрастанию (сравни со `sorted`).
        """),
        """
        def is_sorted(nums):
            pass
        """,
        """
        def test_values():
            assert [is_sorted([1, 2, 2]), is_sorted([2, 1]), is_sorted([])] == [True, False, True], "Неверный результат"
        """,
        """
        def is_sorted(nums):
            return nums == sorted(nums)
        """),
),

lesson(f"{P}-m1-l2", "Параметр key",
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        words = ["banana", "Kiwi", "apple", "fig"]
        print(sorted(words))
        print(sorted(words, key=str.lower))
        print(sorted(words, key=len))
        """, hint="key — функция, по результату которой сравниваются элементы."),
    out(f"{P}-m1-l2-e2", "Что выведет программа?", """
        nums = [-5, 3, -1, 4]
        print(sorted(nums, key=abs))
        print(sorted(nums, key=lambda n: n % 3))
        """),
    out(f"{P}-m1-l2-e3", "Что выведет программа? key не меняет элементы.", """
        words = ["b", "A", "c"]
        result = sorted(words, key=str.lower)
        print(result)
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `by_length(words)` — слова по возрастанию длины (при равной длине — в исходном порядке).

        ```
        by_length(["banana", "fig", "kiwi"])   # → ["fig", "kiwi", "banana"]
        ```
        """),
        """
        def by_length(words):
            pass
        """,
        """
        def test_values():
            assert by_length(["banana", "fig", "kiwi"]) == ["fig", "kiwi", "banana"] and by_length(["bb", "aa"]) == ["bb", "aa"], "Неверный результат"
        """,
        """
        def by_length(words):
            return sorted(words, key=len)
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `case_insensitive(words)` — сортировка без учёта регистра.

        ```
        case_insensitive(["b", "A", "c"])   # → ["A", "b", "c"]
        ```
        """),
        """
        def case_insensitive(words):
            pass
        """,
        """
        def test_values():
            assert case_insensitive(["b", "A", "c"]) == ["A", "b", "c"], "Неверный результат"
        """,
        """
        def case_insensitive(words):
            return sorted(words, key=str.lower)
        """),
    cod(f"{P}-m1-l2-e6", t("""
        Напиши функцию `closest_to_zero(nums)` — числа, упорядоченные по близости к нулю (по модулю).

        ```
        closest_to_zero([-5, 3, -1, 4])   # → [-1, 3, 4, -5]
        ```
        """),
        """
        def closest_to_zero(nums):
            pass
        """,
        """
        def test_values():
            assert closest_to_zero([-5, 3, -1, 4]) == [-1, 3, 4, -5], "Неверный результат"
        """,
        """
        def closest_to_zero(nums):
            return sorted(nums, key=abs)
        """),
    cod(f"{P}-m1-l2-e7", t("""
        Напиши функцию `by_last_char(words)` — сортировка слов по последней букве.

        ```
        by_last_char(["abc", "xya", "mnb"])   # → ["xya", "mnb", "abc"]
        ```
        """),
        """
        def by_last_char(words):
            pass
        """,
        """
        def test_values():
            assert by_last_char(["abc", "xya", "mnb"]) == ["xya", "mnb", "abc"], "Неверный результат"
        """,
        """
        def by_last_char(words):
            return sorted(words, key=lambda w: w[-1])
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши функцию `sort_versions(versions)` — строки версий `"X.Y.Z"` по возрастанию **как чисел**.

        ```
        sort_versions(["1.10.0", "1.9.2", "1.2.10"])   # → ["1.2.10", "1.9.2", "1.10.0"]
        ```
        """),
        """
        def sort_versions(versions):
            pass
        """,
        """
        def test_values():
            assert sort_versions(["1.10.0", "1.9.2", "1.2.10"]) == ["1.2.10", "1.9.2", "1.10.0"], "Неверный порядок"
        """,
        """
        def sort_versions(versions):
            return sorted(versions, key=lambda v: [int(p) for p in v.split(".")])
        """, hint="Ключ — список чисел: списки сравниваются поэлементно."),
),

lesson(f"{P}-m1-l3", "Несколько признаков и стабильность",
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        people = [("Боря", 30), ("Аня", 25), ("Вика", 30)]
        print(sorted(people, key=lambda p: (p[1], p[0])))
        print(sorted(people, key=lambda p: (-p[1], p[0])))
        """, hint="Ключ-кортеж: сначала первый элемент, при равенстве — второй."),
    out(f"{P}-m1-l3-e2", "Что выведет программа? Стабильность.", """
        items = [("b", 1), ("a", 2), ("c", 1)]
        print(sorted(items, key=lambda x: x[1]))
        """, hint="При равных ключах элементы сохраняют исходный порядок."),
    out(f"{P}-m1-l3-e3", "Что выведет программа? Сортировка в два прохода.", """
        people = [("Боря", 30), ("Аня", 25), ("Вика", 30)]
        step1 = sorted(people, key=lambda p: p[0])
        step2 = sorted(step1, key=lambda p: p[1], reverse=True)
        print(step2)
        """),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `leaderboard(scores)` — список пар `(имя, очки)`: по очкам по убыванию, при равенстве — по имени по алфавиту. Вернуть имена.

        ```
        leaderboard([("Боря", 50), ("Аня", 80), ("Вика", 50)])   # → ["Аня", "Боря", "Вика"]
        ```
        """),
        """
        def leaderboard(scores):
            pass
        """,
        """
        def test_values():
            assert leaderboard([("Боря", 50), ("Аня", 80), ("Вика", 50)]) == ["Аня", "Боря", "Вика"], "Неверный порядок"
        """,
        """
        def leaderboard(scores):
            return [name for name, _ in sorted(scores, key=lambda s: (-s[1], s[0]))]
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `by_len_then_alpha(words)` — по длине по возрастанию, при равной длине — по алфавиту.

        ```
        by_len_then_alpha(["pear", "fig", "kiwi", "apple"])   # → ["fig", "kiwi", "pear", "apple"]
        ```
        """),
        """
        def by_len_then_alpha(words):
            pass
        """,
        """
        def test_values():
            assert by_len_then_alpha(["pear", "fig", "kiwi", "apple"]) == ["fig", "kiwi", "pear", "apple"], "Неверный порядок"
        """,
        """
        def by_len_then_alpha(words):
            return sorted(words, key=lambda w: (len(w), w))
        """),
    cod(f"{P}-m1-l3-e6", t("""
        Напиши функцию `sort_bugs(bugs)` — баги `(id, severity, created)`: по серьёзности `critical` → `major` → `minor` (словарь рангов), при равной — по дате (строка `"YYYY-MM-DD"`) от старых. Вернуть id.

        ```
        sort_bugs([(1, "minor", "2024-01-01"), (2, "critical", "2024-03-01"), (3, "critical", "2024-01-15")])   # → [3, 2, 1]
        ```
        """),
        """
        def sort_bugs(bugs):
            pass
        """,
        """
        def test_values():
            assert sort_bugs([(1, "minor", "2024-01-01"), (2, "critical", "2024-03-01"), (3, "critical", "2024-01-15"), (4, "major", "2023-01-01")]) == [3, 2, 4, 1], "Неверный порядок"
        """,
        """
        RANK = {"critical": 0, "major": 1, "minor": 2}

        def sort_bugs(bugs):
            return [b[0] for b in sorted(bugs, key=lambda b: (RANK[b[1]], b[2]))]
        """, xp=20),
    cod(f"{P}-m1-l3-e7", t("""
        Напиши функцию `name_desc_age_asc(people)` — пары `(имя, возраст)`: по имени **по убыванию** (Я→А), при равенстве — по возрасту по возрастанию. Для строк минус не работает — используй **два прохода** стабильной сортировки.

        ```
        name_desc_age_asc([("Аня", 30), ("Боря", 20), ("Аня", 25)])   # → [("Боря", 20), ("Аня", 25), ("Аня", 30)]
        ```
        """),
        """
        def name_desc_age_asc(people):
            pass
        """,
        """
        def test_values():
            assert name_desc_age_asc([("Аня", 30), ("Боря", 20), ("Аня", 25)]) == [("Боря", 20), ("Аня", 25), ("Аня", 30)], "Неверный порядок"
        """,
        """
        def name_desc_age_asc(people):
            by_age = sorted(people, key=lambda p: p[1])
            return sorted(by_age, key=lambda p: p[0], reverse=True)
        """, hint="Сначала сортируй по второстепенному признаку, потом по главному.", xp=20),
    cod(f"{P}-m1-l3-e8", t("""
        Напиши функцию `status_order(results)` — пары `(тест, статус)` так: сначала `fail`, потом `skip`, потом `pass`; внутри группы — исходный порядок (стабильность).

        ```
        status_order([("a", "pass"), ("b", "fail"), ("c", "skip"), ("d", "fail")])
        # → [("b", "fail"), ("d", "fail"), ("c", "skip"), ("a", "pass")]
        ```
        """),
        """
        def status_order(results):
            pass
        """,
        """
        def test_values():
            got = status_order([("a", "pass"), ("b", "fail"), ("c", "skip"), ("d", "fail")])
            assert got == [("b", "fail"), ("d", "fail"), ("c", "skip"), ("a", "pass")], f"Получено {got}"
        """,
        """
        ORDER = {"fail": 0, "skip": 1, "pass": 2}

        def status_order(results):
            return sorted(results, key=lambda r: ORDER[r[1]])
        """),
),

lesson(f"{P}-m1-l4", "Сортировка словарей и записей",
    out(f"{P}-m1-l4-e1", "Что выведет программа?", """
        scores = {"Боря": 50, "Аня": 80, "Вика": 65}
        print(sorted(scores))
        print(sorted(scores, key=scores.get, reverse=True))
        print(sorted(scores.items(), key=lambda p: p[1]))
        """),
    out(f"{P}-m1-l4-e2", "Что выведет программа? Список словарей.", """
        users = [{"name": "Боря", "age": 30}, {"name": "Аня", "age": 25}]
        print([u["name"] for u in sorted(users, key=lambda u: u["age"])])
        """),
    out(f"{P}-m1-l4-e3", "Что выведет программа? itemgetter.", """
        from operator import itemgetter
        rows = [("b", 2), ("a", 3), ("c", 1)]
        print(sorted(rows, key=itemgetter(1)))
        users = [{"n": "x", "a": 2}, {"n": "y", "a": 1}]
        print(sorted(users, key=itemgetter("a")))
        """),
    cod(f"{P}-m1-l4-e4", t("""
        Напиши функцию `slowest(times, n)` — имена `n` самых медленных тестов из словаря `{имя: секунды}` по убыванию.

        ```
        slowest({"a": 1.2, "b": 3.4, "c": 2.0}, 2)   # → ["b", "c"]
        ```
        """),
        """
        def slowest(times, n):
            pass
        """,
        """
        def test_values():
            assert slowest({"a": 1.2, "b": 3.4, "c": 2.0}, 2) == ["b", "c"] and slowest({}, 1) == [], "Неверный результат"
        """,
        """
        def slowest(times, n):
            return sorted(times, key=times.get, reverse=True)[:n]
        """),
    cod(f"{P}-m1-l4-e5", t("""
        Напиши функцию `sort_by_field(records, field)` — список словарей, отсортированный по значению поля `field`.

        ```
        sort_by_field([{"id": 3}, {"id": 1}], "id")   # → [{"id": 1}, {"id": 3}]
        ```
        """),
        """
        def sort_by_field(records, field):
            pass
        """,
        """
        def test_values():
            assert sort_by_field([{"id": 3}, {"id": 1}], "id") == [{"id": 1}, {"id": 3}], "Неверный порядок"
        """,
        """
        def sort_by_field(records, field):
            return sorted(records, key=lambda r: r[field])
        """),
    cod(f"{P}-m1-l4-e6", t("""
        Напиши функцию `sorted_dict(d)` — новый словарь с ключами по алфавиту.

        ```
        sorted_dict({"b": 1, "a": 2})   # → {"a": 2, "b": 1}   (и порядок ключей a, b)
        ```
        """),
        """
        def sorted_dict(d):
            pass
        """,
        """
        def test_values():
            got = sorted_dict({"b": 1, "a": 2, "c": 0})
            assert got == {"a": 2, "b": 1, "c": 0} and list(got) == ["a", "b", "c"], f"Получено {got}"
        """,
        """
        def sorted_dict(d):
            return dict(sorted(d.items()))
        """),
    cod(f"{P}-m1-l4-e7", t("""
        Напиши функцию `rank_places(scores)` — словарь «имя → место» (с 1) по убыванию очков (очки различны).

        ```
        rank_places({"Боря": 50, "Аня": 80})   # → {"Аня": 1, "Боря": 2}
        ```
        """),
        """
        def rank_places(scores):
            pass
        """,
        """
        def test_values():
            assert rank_places({"Боря": 50, "Аня": 80, "Вика": 65}) == {"Аня": 1, "Вика": 2, "Боря": 3}, "Неверные места"
        """,
        """
        def rank_places(scores):
            ordered = sorted(scores, key=scores.get, reverse=True)
            return {name: i for i, name in enumerate(ordered, start=1)}
        """),
    cod(f"{P}-m1-l4-e8", t("""
        Напиши функцию `sort_users(users)` — список словарей `name`, `role`, `age`: по роли по алфавиту, внутри роли — по возрасту по убыванию. Вернуть имена.

        ```
        sort_users([{"name": "a", "role": "qa", "age": 20}, {"name": "b", "role": "dev", "age": 30}, {"name": "c", "role": "qa", "age": 40}])
        # → ["b", "c", "a"]
        ```
        """),
        """
        def sort_users(users):
            pass
        """,
        """
        def test_values():
            users = [{"name": "a", "role": "qa", "age": 20}, {"name": "b", "role": "dev", "age": 30}, {"name": "c", "role": "qa", "age": 40}]
            assert sort_users(users) == ["b", "c", "a"], f"Получено {sort_users(users)}"
        """,
        """
        def sort_users(users):
            return [u["name"] for u in sorted(users, key=lambda u: (u["role"], -u["age"]))]
        """),
),
)
