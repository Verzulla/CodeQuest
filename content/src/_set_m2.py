"""Тема «Множества», модуль 2 «Операции над множествами» — задания. Теория — в _set_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "set"

m2 = module(f"{P}-m2", "Операции над множествами", "🔀", "Объединение, пересечение, разность, подмножества и изменение на месте",

lesson(f"{P}-m2-l1", "Объединение и пересечение",
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        a = {1, 2, 3}
        b = {3, 4}
        print(sorted(a | b), sorted(a & b))
        print(sorted(a.union(b)), sorted(a.intersection(b)))
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа? Методы принимают списки.", """
        a = {1, 2}
        print(sorted(a.union([2, 5])), sorted(a.intersection("12")))
        try:
            a | [2, 5]
        except TypeError:
            print("оператор | только с множеством")
        """, hint='Строка "12" — символы "1" и "2", а не числа.'),
    out(f"{P}-m2-l1-e3", "Что выведет программа? Несколько множеств.", """
        x, y, z = {1, 2, 3}, {2, 3, 4}, {3, 4, 5}
        print(sorted(x & y & z), sorted(x | y | z))
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `common_skills(a, b)` — отсортированный список навыков, которые есть у обоих (списки строк).

        ```
        common_skills(["qa", "sql", "python"], ["python", "qa", "go"])   # → ["python", "qa"]
        ```
        """),
        """
        def common_skills(a, b):
            pass
        """,
        """
        def test_values():
            assert common_skills(["qa", "sql", "python"], ["python", "qa", "go"]) == ["python", "qa"] and common_skills([], ["x"]) == [], "Неверный результат"
        """,
        """
        def common_skills(a, b):
            return sorted(set(a) & set(b))
        """),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `all_tags(*tag_lists)` — отсортированный список всех различных тегов из любого количества списков.

        ```
        all_tags(["api"], ["ui", "api"], ["smoke"])   # → ["api", "smoke", "ui"]
        ```
        """),
        """
        def all_tags(*tag_lists):
            pass
        """,
        """
        def test_values():
            assert all_tags(["api"], ["ui", "api"], ["smoke"]) == ["api", "smoke", "ui"] and all_tags() == [], "Неверный результат"
        """,
        """
        def all_tags(*tag_lists):
            result = set()
            for tags in tag_lists:
                result |= set(tags)
            return sorted(result)
        """),
    cod(f"{P}-m2-l1-e6", t("""
        Напиши функцию `in_all(*groups)` — отсортированный список элементов, которые есть **во всех** переданных списках. Без аргументов — `[]`.

        ```
        in_all([1, 2, 3], [2, 3, 4], [3, 2])   # → [2, 3]
        ```
        """),
        """
        def in_all(*groups):
            pass
        """,
        """
        def test_values():
            assert in_all([1, 2, 3], [2, 3, 4], [3, 2]) == [2, 3] and in_all() == [] and in_all([1, 1]) == [1], "Неверный результат"
        """,
        """
        def in_all(*groups):
            if not groups:
                return []
            result = set(groups[0])
            for g in groups[1:]:
                result &= set(g)
            return sorted(result)
        """, xp=20),
    cod(f"{P}-m2-l1-e7", t("""
        Напиши функцию `shared_letters(words)` — отсортированная строка из букв, которые есть в **каждом** слове списка.

        ```
        shared_letters(["python", "typo", "type"])   # → "pty"
        ```
        """),
        """
        def shared_letters(words):
            pass
        """,
        """
        def test_values():
            assert shared_letters(["python", "typo", "type"]) == "pty" and shared_letters(["abc"]) == "abc" and shared_letters([]) == "", "Неверный результат"
        """,
        """
        def shared_letters(words):
            if not words:
                return ""
            common = set(words[0])
            for w in words[1:]:
                common &= set(w)
            return "".join(sorted(common))
        """),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `jaccard(a, b)` — **коэффициент Жаккара** двух списков: размер пересечения их множеств, делённый на размер объединения, округлённый до 2 знаков. Если оба пустые — `1.0`.

        ```
        jaccard(["a", "b", "c"], ["b", "c", "d"])   # → 0.5
        ```
        """),
        """
        def jaccard(a, b):
            pass
        """,
        """
        def test_values():
            assert [jaccard(["a", "b", "c"], ["b", "c", "d"]), jaccard([], []), jaccard(["x"], ["y"])] == [0.5, 1.0, 0.0], "Неверный результат"
        """,
        """
        def jaccard(a, b):
            sa, sb = set(a), set(b)
            union = sa | sb
            if not union:
                return 1.0
            return round(len(sa & sb) / len(union), 2)
        """),
),

lesson(f"{P}-m2-l2", "Разность и симметричная разность",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        a = {1, 2, 3}
        b = {3, 4}
        print(sorted(a - b), sorted(b - a))
        print(sorted(a ^ b))
        """, hint="Разность не симметрична: a - b и b - a — разные множества."),
    out(f"{P}-m2-l2-e2", "Что выведет программа?", """
        expected = {"id", "name", "email"}
        actual = {"id", "name", "debug"}
        print("не хватает:", sorted(expected - actual))
        print("лишние:", sorted(actual - expected))
        print("различия:", sorted(expected ^ actual))
        """),
    out(f"{P}-m2-l2-e3", "Что выведет программа?", """
        a = {1, 2, 3}
        print(sorted(a.difference([2], {3})), sorted(a.symmetric_difference([3, 9])))
        """),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `missing(expected, actual)` — отсортированный список элементов из `expected`, которых нет в `actual` (оба — списки).

        ```
        missing(["id", "name", "email"], ["id"])   # → ["email", "name"]
        ```
        """),
        """
        def missing(expected, actual):
            pass
        """,
        """
        def test_values():
            assert missing(["id", "name", "email"], ["id"]) == ["email", "name"] and missing([], [1]) == [], "Неверный результат"
        """,
        """
        def missing(expected, actual):
            return sorted(set(expected) - set(actual))
        """),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `field_report(expected, actual)` — словарь `{"missing": [...], "extra": [...]}` с отсортированными списками полей: чего не хватает в `actual` и что в нём лишнее.

        ```
        field_report(["id", "name"], ["id", "debug"])   # → {"missing": ["name"], "extra": ["debug"]}
        ```
        """),
        """
        def field_report(expected, actual):
            pass
        """,
        """
        def test_values():
            assert field_report(["id", "name"], ["id", "debug"]) == {"missing": ["name"], "extra": ["debug"]}, "Неверный отчёт"
            assert field_report(["a"], ["a"]) == {"missing": [], "extra": []}, "Совпадают"
        """,
        """
        def field_report(expected, actual):
            e, a = set(expected), set(actual)
            return {"missing": sorted(e - a), "extra": sorted(a - e)}
        """),
    cod(f"{P}-m2-l2-e6", t("""
        Напиши функцию `changed(before, after)` — отсортированный список элементов, которые есть **только в одном** из двух списков (симметричная разность).

        ```
        changed([1, 2, 3], [2, 3, 4])   # → [1, 4]
        ```
        """),
        """
        def changed(before, after):
            pass
        """,
        """
        def test_values():
            assert changed([1, 2, 3], [2, 3, 4]) == [1, 4] and changed([1], [1]) == [], "Неверный результат"
        """,
        """
        def changed(before, after):
            return sorted(set(before) ^ set(after))
        """),
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `new_failures(yesterday, today)` — тесты, которые упали **сегодня**, но не падали **вчера** (новые регрессии), отсортированные.

        ```
        new_failures(["a", "b"], ["b", "c", "d"])   # → ["c", "d"]
        ```
        """),
        """
        def new_failures(yesterday, today):
            pass
        """,
        """
        def test_values():
            assert new_failures(["a", "b"], ["b", "c", "d"]) == ["c", "d"] and new_failures(["a"], ["a"]) == [], "Неверный результат"
        """,
        """
        def new_failures(yesterday, today):
            return sorted(set(today) - set(yesterday))
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `missing_numbers(nums, n)` — отсортированный список чисел от 1 до `n`, которых нет в списке.

        ```
        missing_numbers([1, 2, 5], 6)   # → [3, 4, 6]
        ```
        """),
        """
        def missing_numbers(nums, n):
            pass
        """,
        """
        def test_values():
            assert missing_numbers([1, 2, 5], 6) == [3, 4, 6] and missing_numbers([1, 2], 2) == [] and missing_numbers([], 2) == [1, 2], "Неверный результат"
        """,
        """
        def missing_numbers(nums, n):
            return sorted(set(range(1, n + 1)) - set(nums))
        """),
),

lesson(f"{P}-m2-l3", "Подмножества и сравнение множеств",
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        required = {"read"}
        user = {"read", "write"}
        print(required <= user, required.issubset(user), user >= required)
        print(required < user, user < user, user <= user)
        """, hint="< — строгое подмножество: меньше И не равно."),
    out(f"{P}-m2-l3-e2", "Что выведет программа?", """
        print({1, 2} == {2, 1}, [1, 2] == [2, 1])
        print({1, 2}.isdisjoint({3, 4}), {1, 2}.isdisjoint([2]))
        """),
    out(f"{P}-m2-l3-e3", "Что выведет программа? Пустое множество.", """
        e = set()
        print(e <= {1}, e <= e, e.isdisjoint(e))
        """),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `has_permissions(user_perms, required)` — есть ли у пользователя **все** требуемые права (оба аргумента — списки).

        ```
        has_permissions(["read", "write"], ["read"])   # → True
        has_permissions(["read"], ["read", "admin"])   # → False
        ```
        """),
        """
        def has_permissions(user_perms, required):
            pass
        """,
        """
        def test_values():
            assert [has_permissions(["read", "write"], ["read"]), has_permissions(["read"], ["read", "admin"]), has_permissions([], [])] == [True, False, True], "Неверный результат"
        """,
        """
        def has_permissions(user_perms, required):
            return set(required) <= set(user_perms)
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `same_items(a, b)` — содержат ли два списка одинаковый **набор** элементов (порядок и повторы не важны).

        ```
        same_items([1, 2, 2], [2, 1])   # → True
        ```
        """),
        """
        def same_items(a, b):
            pass
        """,
        """
        def test_values():
            assert [same_items([1, 2, 2], [2, 1]), same_items([1], [1, 3]), same_items([], [])] == [True, False, True], "Неверный результат"
        """,
        """
        def same_items(a, b):
            return set(a) == set(b)
        """),
    cod(f"{P}-m2-l3-e6", t("""
        Напиши функцию `no_conflicts(a, b)` — не пересекаются ли два списка (нет ни одного общего элемента). Используй `isdisjoint`.

        ```
        no_conflicts(["mon", "tue"], ["wed"])   # → True
        ```
        """),
        """
        def no_conflicts(a, b):
            pass
        """,
        """
        def test_values():
            assert [no_conflicts(["mon", "tue"], ["wed"]), no_conflicts(["mon"], ["mon"]), no_conflicts([], ["x"])] == [True, False, True], "Неверный результат"
        """,
        """
        def no_conflicts(a, b):
            return set(a).isdisjoint(b)
        """),
    cod(f"{P}-m2-l3-e7", t("""
        Напиши функцию `relation(a, b)` — отношение двух множеств строкой:

        - `"equal"` — равны;
        - `"subset"` — `a` строго внутри `b`;
        - `"superset"` — `a` строго содержит `b`;
        - `"disjoint"` — нет общих элементов;
        - `"overlap"` — иначе.

        ```
        relation({1}, {1, 2})   # → "subset"
        ```
        """),
        """
        def relation(a, b):
            pass
        """,
        """
        def test_values():
            got = [relation({1}, {1, 2}), relation({1, 2}, {2, 1}), relation({1, 2}, {1}), relation({1}, {2}), relation({1, 2}, {2, 3})]
            assert got == ["subset", "equal", "superset", "disjoint", "overlap"], f"Получено {got}"
        """,
        """
        def relation(a, b):
            if a == b:
                return "equal"
            if a < b:
                return "subset"
            if a > b:
                return "superset"
            if a.isdisjoint(b):
                return "disjoint"
            return "overlap"
        """, hint="Проверяй равенство первым: пустые множества и равны, и не пересекаются.", xp=20),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `covered(features, tests)` — покрыты ли тестами все функции продукта. `tests` — словарь «тест → список проверяемых функций».

        ```
        covered(["login", "pay"], {"t1": ["login"], "t2": ["pay", "cart"]})   # → True
        ```
        """),
        """
        def covered(features, tests):
            pass
        """,
        """
        def test_values():
            assert covered(["login", "pay"], {"t1": ["login"], "t2": ["pay", "cart"]}) is True, "Всё покрыто"
            assert covered(["login", "search"], {"t1": ["login"]}) is False and covered([], {}) is True, "Неверный результат"
        """,
        """
        def covered(features, tests):
            tested = set()
            for checked in tests.values():
                tested |= set(checked)
            return set(features) <= tested
        """),
),

lesson(f"{P}-m2-l4", "Изменение на месте: |=, &=, -=, ^=",
    out(f"{P}-m2-l4-e1", "Что выведет программа?", """
        s = {1, 2, 3}
        s |= {4}
        s -= {1}
        s &= {2, 3, 4, 5}
        print(sorted(s))
        """),
    out(f"{P}-m2-l4-e2", "Что выведет программа? Новое или то же самое.", """
        a = {1, 2}
        b = a
        a = a | {3}
        print(sorted(a), sorted(b))
        c = {1, 2}
        d = c
        c |= {3}
        print(sorted(c), sorted(d))
        """, hint="a = a | x создаёт новое множество, а |= меняет существующее."),
    out(f"{P}-m2-l4-e3", "Что выведет программа?", """
        s = {1, 2, 3}
        s.difference_update([1, 9])
        s.intersection_update({2, 3, 4})
        s.symmetric_difference_update({3, 5})
        print(sorted(s))
        """),
    cod(f"{P}-m2-l4-e4", t("""
        Напиши функцию `grant(perms, new)` — добавить права из списка `new` в множество `perms` **на месте** (`|=`). Функция ничего не возвращает.
        """),
        """
        def grant(perms, new):
            pass
        """,
        """
        def test_values():
            p = {"read"}
            assert grant(p, ["write", "read"]) is None and p == {"read", "write"}, f"p = {p}"
        """,
        """
        def grant(perms, new):
            perms |= set(new)
        """),
    cod(f"{P}-m2-l4-e5", t("""
        Напиши функцию `revoke(perms, removed)` — удалить права из списка `removed` **на месте**. Отсутствующие — без ошибок.
        """),
        """
        def revoke(perms, removed):
            pass
        """,
        """
        def test_values():
            p = {"read", "write", "admin"}
            revoke(p, ["admin", "delete"])
            assert p == {"read", "write"}, f"p = {p}"
        """,
        """
        def revoke(perms, removed):
            perms -= set(removed)
        """),
    cod(f"{P}-m2-l4-e6", t("""
        Напиши функцию `keep_only(perms, allowed)` — оставить в множестве **на месте** только права из списка `allowed`.
        """),
        """
        def keep_only(perms, allowed):
            pass
        """,
        """
        def test_values():
            p = {"read", "write", "root"}
            keep_only(p, ["read", "write", "delete"])
            assert p == {"read", "write"}, f"p = {p}"
        """,
        """
        def keep_only(perms, allowed):
            perms &= set(allowed)
        """),
    cod(f"{P}-m2-l4-e7", t("""
        Напиши функцию `apply_changes(perms, changes)` — применить список изменений `("+", право)` / `("-", право)` к множеству **на месте** и вернуть отсортированный список итоговых прав.

        ```
        apply_changes({"read"}, [("+", "write"), ("-", "read"), ("-", "admin")])   # → ["write"]
        ```
        """),
        """
        def apply_changes(perms, changes):
            pass
        """,
        """
        def test_values():
            p = {"read"}
            assert apply_changes(p, [("+", "write"), ("-", "read"), ("-", "admin")]) == ["write"] and p == {"write"}, f"p = {p}"
        """,
        """
        def apply_changes(perms, changes):
            for op, perm in changes:
                if op == "+":
                    perms.add(perm)
                else:
                    perms.discard(perm)
            return sorted(perms)
        """),
    cod(f"{P}-m2-l4-e8", t("""
        Напиши функцию `with_added(s, items)` — вернуть **новое** множество: `s` плюс элементы `items`. Исходное множество не менять (не используй `|=` на `s`).

        ```
        s = {1}
        with_added(s, [2])   # → {1, 2}
        s                    # → {1}
        ```
        """),
        """
        def with_added(s, items):
            pass
        """,
        """
        def test_values():
            s = {1}
            assert with_added(s, [2]) == {1, 2} and s == {1}, f"s = {s}"
        """,
        """
        def with_added(s, items):
            return s | set(items)
        """),
),
)
