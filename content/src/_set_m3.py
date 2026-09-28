"""Тема «Множества», модуль 3 «Множества на практике» — задания. Теория — в _set_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "set"

m3 = module(f"{P}-m3", "Множества на практике", "🧰", "frozenset, дубликаты, сравнение наборов в тестах, практика",

lesson(f"{P}-m3-l1", "frozenset: неизменяемое множество",
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        fs = frozenset([3, 1, 3])
        print(sorted(fs), len(fs), 1 in fs)
        try:
            fs.add(5)
        except AttributeError:
            print("frozenset нельзя изменить")
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа? Множество как ключ.", """
        combos = {frozenset({"chrome", "linux"}): "ok"}
        print(combos[frozenset({"linux", "chrome"})])
        try:
            {{1, 2}: "x"}
        except TypeError:
            print("обычное множество не может быть ключом")
        """, hint="frozenset хешируемый, set — нет."),
    out(f"{P}-m3-l1-e3", "Что выведет программа?", """
        a = frozenset({1, 2})
        b = a | {3}
        print(type(b).__name__, sorted(b), a == {1, 2})
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `freeze(items)` — неизменяемое множество из списка.

        ```
        freeze([1, 2, 2])   # → frozenset({1, 2})
        ```
        """),
        """
        def freeze(items):
            pass
        """,
        """
        def test_values():
            f = freeze([1, 2, 2])
            assert f == {1, 2} and isinstance(f, frozenset), f"Получено {f!r}"
        """,
        """
        def freeze(items):
            return frozenset(items)
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `count_combos(runs)` — `runs` это список списков вида `["chrome", "linux"]` (порядок внутри не важен). Вернуть, сколько **различных** комбинаций.

        ```
        count_combos([["chrome", "linux"], ["linux", "chrome"], ["ff", "mac"]])   # → 2
        ```
        """),
        """
        def count_combos(runs):
            pass
        """,
        """
        def test_values():
            assert count_combos([["chrome", "linux"], ["linux", "chrome"], ["ff", "mac"]]) == 2 and count_combos([]) == 0, "Неверный результат"
        """,
        """
        def count_combos(runs):
            return len({frozenset(r) for r in runs})
        """),
    cod(f"{P}-m3-l1-e6", t("""
        Напиши функцию `group_anagrams(words)` — количество групп слов, состоящих из одного и того же **набора** букв (без учёта повторов и порядка).

        ```
        group_anagrams(["listen", "silent", "enlist", "abc", "cab"])   # → 2
        ```
        """),
        """
        def group_anagrams(words):
            pass
        """,
        """
        def test_values():
            assert group_anagrams(["listen", "silent", "enlist", "abc", "cab"]) == 2 and group_anagrams([]) == 0, "Неверный результат"
        """,
        """
        def group_anagrams(words):
            return len({frozenset(w) for w in words})
        """),
    cod(f"{P}-m3-l1-e7", t("""
        Напиши функцию `results_by_env(runs)` — `runs` это список пар `(набор_окружения, статус)`, где набор — список строк. Вернуть словарь с ключами-`frozenset` и статусами (при повторе — последний).

        ```
        results_by_env([(["chrome", "linux"], "pass"), (["linux", "chrome"], "fail")])
        # → {frozenset({"chrome", "linux"}): "fail"}
        ```
        """),
        """
        def results_by_env(runs):
            pass
        """,
        """
        def test_values():
            got = results_by_env([(["chrome", "linux"], "pass"), (["linux", "chrome"], "fail"), (["ff"], "pass")])
            assert got == {frozenset({"chrome", "linux"}): "fail", frozenset({"ff"}): "pass"}, f"Получено {got}"
        """,
        """
        def results_by_env(runs):
            return {frozenset(env): status for env, status in runs}
        """),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `is_hashable_set(s)` — вернуть `True`, если объект можно использовать как ключ словаря (попробуй `hash` и лови `TypeError`).

        ```
        is_hashable_set(frozenset({1}))   # → True
        is_hashable_set({1})              # → False
        ```
        """),
        """
        def is_hashable_set(s):
            pass
        """,
        """
        def test_values():
            assert [is_hashable_set(frozenset({1})), is_hashable_set({1}), is_hashable_set((1, 2))] == [True, False, True], "Неверный результат"
        """,
        """
        def is_hashable_set(s):
            try:
                hash(s)
                return True
            except TypeError:
                return False
        """),
),

lesson(f"{P}-m3-l2", "Дубликаты и уникальность",
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        ids = [3, 1, 3, 2, 1, 3]
        seen, dups = set(), set()
        for x in ids:
            if x in seen:
                dups.add(x)
            seen.add(x)
        print(sorted(dups), sorted(seen))
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа?", """
        emails = ["A@x.ru", "a@x.ru ", "b@x.ru"]
        print(len(set(emails)), len({e.strip().lower() for e in emails}))
        """, hint="Для сравнения «по смыслу» сначала нормализуй."),
    out(f"{P}-m3-l2-e3", "Что выведет программа?", """
        from collections import Counter
        items = ["a", "b", "a", "c", "a", "b"]
        c = Counter(items)
        print(sorted(x for x, n in c.items() if n > 1), sorted(x for x, n in c.items() if n == 1))
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши функцию `duplicates(items)` — отсортированный список элементов, встречающихся **больше одного раза**.

        ```
        duplicates([3, 1, 3, 2, 1, 3])   # → [1, 3]
        ```
        """),
        """
        def duplicates(items):
            pass
        """,
        """
        def test_values():
            assert duplicates([3, 1, 3, 2, 1, 3]) == [1, 3] and duplicates([1, 2]) == [] and duplicates([]) == [], "Неверный результат"
        """,
        """
        def duplicates(items):
            seen, dups = set(), set()
            for x in items:
                if x in seen:
                    dups.add(x)
                seen.add(x)
            return sorted(dups)
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `unique_emails(emails)` — сколько различных email-ов после нормализации (пробелы по краям, нижний регистр).

        ```
        unique_emails(["A@x.ru", "a@x.ru ", "b@x.ru"])   # → 2
        ```
        """),
        """
        def unique_emails(emails):
            pass
        """,
        """
        def test_values():
            assert unique_emails(["A@x.ru", "a@x.ru ", "b@x.ru"]) == 2 and unique_emails([]) == 0, "Неверный результат"
        """,
        """
        def unique_emails(emails):
            return len({e.strip().lower() for e in emails})
        """),
    cod(f"{P}-m3-l2-e6", t("""
        Напиши функцию `singles(items)` — отсортированный список элементов, встречающихся **ровно один раз**.

        ```
        singles(["a", "b", "a", "c"])   # → ["b", "c"]
        ```
        """),
        """
        def singles(items):
            pass
        """,
        """
        def test_values():
            assert singles(["a", "b", "a", "c"]) == ["b", "c"] and singles(["x", "x"]) == [], "Неверный результат"
        """,
        """
        def singles(items):
            return sorted(x for x in set(items) if items.count(x) == 1)
        """),
    cod(f"{P}-m3-l2-e7", t("""
        Напиши функцию `duplicate_ids(records)` — отсортированный список `id`, которые встречаются в списке записей (словарей) больше одного раза. Удобно для проверки, что API не вернул дубли.

        ```
        duplicate_ids([{"id": 1}, {"id": 2}, {"id": 1}])   # → [1]
        ```
        """),
        """
        def duplicate_ids(records):
            pass
        """,
        """
        def test_values():
            assert duplicate_ids([{"id": 1}, {"id": 2}, {"id": 1}]) == [1] and duplicate_ids([{"id": 1}]) == [], "Неверный результат"
        """,
        """
        def duplicate_ids(records):
            seen, dups = set(), set()
            for r in records:
                if r["id"] in seen:
                    dups.add(r["id"])
                seen.add(r["id"])
            return sorted(dups)
        """),
    cod(f"{P}-m3-l2-e8", t("""
        Напиши функцию `dedupe_by(records, key)` — оставить из списка словарей только первую запись для каждого значения поля `key`, сохранив порядок.

        ```
        dedupe_by([{"id": 1, "v": "a"}, {"id": 1, "v": "b"}, {"id": 2, "v": "c"}], "id")
        # → [{"id": 1, "v": "a"}, {"id": 2, "v": "c"}]
        ```
        """),
        """
        def dedupe_by(records, key):
            pass
        """,
        """
        def test_values():
            got = dedupe_by([{"id": 1, "v": "a"}, {"id": 1, "v": "b"}, {"id": 2, "v": "c"}], "id")
            assert got == [{"id": 1, "v": "a"}, {"id": 2, "v": "c"}] and dedupe_by([], "id") == [], f"Получено {got}"
        """,
        """
        def dedupe_by(records, key):
            seen = set()
            result = []
            for r in records:
                if r[key] not in seen:
                    seen.add(r[key])
                    result.append(r)
            return result
        """, xp=20),
),

lesson(f"{P}-m3-l3", "Сравнение наборов в тестах",
    out(f"{P}-m3-l3-e1", "Что выведет программа? Порядок не важен.", """
        expected = ["admin", "qa", "dev"]
        actual = ["qa", "dev", "admin"]
        print(expected == actual, set(expected) == set(actual))
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа? Но повторы теряются.", """
        expected = ["a", "a", "b"]
        actual = ["a", "b", "b"]
        print(set(expected) == set(actual), sorted(expected) == sorted(actual))
        """, hint="Если важны количества — сравнивай отсортированные списки или Counter."),
    out(f"{P}-m3-l3-e3", "Что выведет программа?", """
        from collections import Counter
        print(Counter(["a", "a", "b"]) == Counter(["b", "a", "a"]), Counter(["a", "b"]) == Counter(["a", "a", "b"]))
        """),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `same_roles(expected, actual)` — совпадают ли наборы ролей (порядок и повторы не важны).
        """),
        """
        def same_roles(expected, actual):
            pass
        """,
        """
        def test_values():
            assert [same_roles(["a", "b"], ["b", "a", "a"]), same_roles(["a"], ["b"])] == [True, False], "Неверный результат"
        """,
        """
        def same_roles(expected, actual):
            return set(expected) == set(actual)
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `same_multiset(a, b)` — совпадают ли списки с учётом **количества** каждого элемента, но без учёта порядка.

        ```
        same_multiset(["a", "a", "b"], ["b", "a", "a"])   # → True
        same_multiset(["a", "b"], ["a", "b", "b"])        # → False
        ```
        """),
        """
        def same_multiset(a, b):
            pass
        """,
        """
        def test_values():
            assert [same_multiset(["a", "a", "b"], ["b", "a", "a"]), same_multiset(["a", "b"], ["a", "b", "b"]), same_multiset([], [])] == [True, False, True], "Неверный результат"
        """,
        """
        def same_multiset(a, b):
            return sorted(a) == sorted(b)
        """),
    cod(f"{P}-m3-l3-e6", t("""
        Напиши функцию `diff_message(expected, actual)` — сообщение для упавшего теста: `"ok"`, если наборы равны; иначе `"не хватает: <...>; лишние: <...>"` (элементы через запятую, по алфавиту; пустая часть — `-`).

        ```
        diff_message(["a", "b"], ["b", "c"])   # → "не хватает: a; лишние: c"
        diff_message(["a"], ["a", "x", "y"])   # → "не хватает: -; лишние: x, y"
        ```
        """),
        """
        def diff_message(expected, actual):
            pass
        """,
        """
        def test_values():
            assert diff_message(["a", "b"], ["b", "c"]) == "не хватает: a; лишние: c", "Неверное сообщение"
            assert diff_message(["a"], ["a", "x", "y"]) == "не хватает: -; лишние: x, y" and diff_message(["a"], ["a"]) == "ok", "Неверное сообщение"
        """,
        """
        def diff_message(expected, actual):
            e, a = set(expected), set(actual)
            if e == a:
                return "ok"
            missing = ", ".join(sorted(e - a)) or "-"
            extra = ", ".join(sorted(a - e)) or "-"
            return f"не хватает: {missing}; лишние: {extra}"
        """, hint='", ".join([]) — пустая строка; пустая строка or "-" даст "-".', xp=20),
    cod(f"{P}-m3-l3-e7", t("""
        Напиши функцию `response_ids_ok(expected_ids, response)` — `response` это список словарей с полем `"id"`. Вернуть `True`, если набор id в ответе совпадает с ожидаемым **и** в ответе нет дублей.

        ```
        response_ids_ok([1, 2], [{"id": 2}, {"id": 1}])               # → True
        response_ids_ok([1, 2], [{"id": 2}, {"id": 1}, {"id": 1}])    # → False
        ```
        """),
        """
        def response_ids_ok(expected_ids, response):
            pass
        """,
        """
        def test_values():
            got = [response_ids_ok([1, 2], [{"id": 2}, {"id": 1}]), response_ids_ok([1, 2], [{"id": 2}, {"id": 1}, {"id": 1}]), response_ids_ok([1], [{"id": 2}])]
            assert got == [True, False, False], f"Получено {got}"
        """,
        """
        def response_ids_ok(expected_ids, response):
            ids = [r["id"] for r in response]
            return len(ids) == len(set(ids)) and set(ids) == set(expected_ids)
        """),
    cod(f"{P}-m3-l3-e8", t("""
        Напиши функцию `flaky_tests(runs)` — `runs` это список прогонов, каждый прогон — список упавших тестов. «Нестабильный» тест падал **в некоторых, но не во всех** прогонах. Вернуть их отсортированный список.

        ```
        flaky_tests([["a", "b"], ["a"], ["a", "c"]])   # → ["b", "c"]
        ```
        """),
        """
        def flaky_tests(runs):
            pass
        """,
        """
        def test_values():
            assert flaky_tests([["a", "b"], ["a"], ["a", "c"]]) == ["b", "c"] and flaky_tests([]) == [] and flaky_tests([["x"]]) == [], "Неверный результат"
        """,
        """
        def flaky_tests(runs):
            if not runs:
                return []
            sets = [set(r) for r in runs]
            ever = set().union(*sets)
            always = set.intersection(*sets)
            return sorted(ever - always)
        """, hint="Объединение всех прогонов минус пересечение всех.", xp=25),
),

lesson(f"{P}-m3-l4", "Практика: теги, права и покрытие",
    out(f"{P}-m3-l4-e1", "Что выведет программа?", """
        tests = {"login": {"smoke", "auth"}, "pay": {"payments"}, "logout": {"auth"}}
        selected = [name for name, tags in tests.items() if "auth" in tags]
        print(selected)
        print(sorted(set().union(*tests.values())))
        """),
    out(f"{P}-m3-l4-e2", "Что выведет программа?", """
        roles = {"admin": {"read", "write", "delete"}, "qa": {"read", "write"}, "guest": {"read"}}
        print(sorted(roles["admin"] - roles["qa"]))
        print([r for r, perms in roles.items() if "write" in perms])
        """),
    out(f"{P}-m3-l4-e3", "Что выведет программа?", """
        features = {"login", "search", "pay", "cart"}
        tested = {"login", "pay", "profile"}
        print(f"покрыто {len(features & tested)} из {len(features)}")
        print(sorted(features - tested), sorted(tested - features))
        """),
    cod(f"{P}-m3-l4-e4", t("""
        Напиши функцию `select_tests(tests, include, exclude)` — `tests` это словарь «тест → список тегов». Вернуть отсортированный список тестов, у которых есть **хотя бы один** тег из `include` и **нет ни одного** из `exclude`.

        ```
        select_tests({"a": ["smoke"], "b": ["smoke", "slow"], "c": ["api"]}, ["smoke"], ["slow"])   # → ["a"]
        ```
        """),
        """
        def select_tests(tests, include, exclude):
            pass
        """,
        """
        def test_values():
            tests = {"a": ["smoke"], "b": ["smoke", "slow"], "c": ["api"], "d": ["api", "smoke"]}
            assert select_tests(tests, ["smoke"], ["slow"]) == ["a", "d"] and select_tests(tests, ["x"], []) == [], "Неверный результат"
        """,
        """
        def select_tests(tests, include, exclude):
            inc, exc = set(include), set(exclude)
            return sorted(name for name, tags in tests.items() if inc & set(tags) and not exc & set(tags))
        """, xp=20),
    cod(f"{P}-m3-l4-e5", t("""
        Напиши функцию `extra_perms(roles, a, b)` — отсортированный список прав, которые есть у роли `a`, но нет у роли `b`. `roles` — словарь «роль → список прав».
        """),
        """
        def extra_perms(roles, a, b):
            pass
        """,
        """
        def test_values():
            roles = {"admin": ["read", "write", "delete"], "qa": ["read", "write"]}
            assert extra_perms(roles, "admin", "qa") == ["delete"] and extra_perms(roles, "qa", "admin") == [], "Неверный результат"
        """,
        """
        def extra_perms(roles, a, b):
            return sorted(set(roles[a]) - set(roles[b]))
        """),
    cod(f"{P}-m3-l4-e6", t("""
        Напиши функцию `coverage(features, tested)` — процент покрытия функций тестами, округлённый до целого (`round`). Лишние элементы в `tested` не считаются. Пустой `features` — `100`.

        ```
        coverage(["login", "search", "pay", "cart"], ["login", "pay", "profile"])   # → 50
        ```
        """),
        """
        def coverage(features, tested):
            pass
        """,
        """
        def test_values():
            assert [coverage(["login", "search", "pay", "cart"], ["login", "pay", "profile"]), coverage([], ["x"]), coverage(["a", "b", "c"], ["a"])] == [50, 100, 33], "Неверный процент"
        """,
        """
        def coverage(features, tested):
            f = set(features)
            if not f:
                return 100
            return round(len(f & set(tested)) / len(f) * 100)
        """),
    cod(f"{P}-m3-l4-e7", t("""
        Напиши функцию `common_tags(tests)` — отсортированный список тегов, которые есть **у всех** тестов (словарь «тест → список тегов»). Пустой словарь — `[]`.

        ```
        common_tags({"a": ["smoke", "api"], "b": ["api", "slow"]})   # → ["api"]
        ```
        """),
        """
        def common_tags(tests):
            pass
        """,
        """
        def test_values():
            assert common_tags({"a": ["smoke", "api"], "b": ["api", "slow"]}) == ["api"] and common_tags({}) == [], "Неверный результат"
        """,
        """
        def common_tags(tests):
            sets = [set(tags) for tags in tests.values()]
            if not sets:
                return []
            return sorted(set.intersection(*sets))
        """),
    cod(f"{P}-m3-l4-e8", t("""
        Напиши функцию `mutual_friends(graph, a, b)` — `graph` это словарь «пользователь → список друзей». Вернуть отсортированный список общих друзей `a` и `b`.

        ```
        mutual_friends({"ann": ["bob", "cat"], "bob": ["ann", "cat"], "cat": ["ann", "bob"]}, "ann", "bob")   # → ["cat"]
        ```
        """),
        """
        def mutual_friends(graph, a, b):
            pass
        """,
        """
        def test_values():
            g = {"ann": ["bob", "cat"], "bob": ["ann", "cat"], "cat": ["ann", "bob"]}
            assert mutual_friends(g, "ann", "bob") == ["cat"] and mutual_friends({"x": [], "y": []}, "x", "y") == [], "Неверный результат"
        """,
        """
        def mutual_friends(graph, a, b):
            return sorted(set(graph[a]) & set(graph[b]))
        """),
),
)
