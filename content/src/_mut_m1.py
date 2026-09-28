"""Тема «Изменяемые и неизменяемые», модуль 1 «Объекты и ссылки» — задания. Теория — в _mut_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "mut"

m1 = module(f"{P}-m1", "Объекты и ссылки", "🔗", "Изменяемые и неизменяемые типы, ссылки и is, операции на месте, хешируемость",

lesson(f"{P}-types", "Какие типы изменяемые",
    out(f"{P}-types-e1", "Что выведет программа? Список меняется на месте.", """
        nums = [1, 2, 3]
        before = id(nums)
        nums.append(4)
        nums[0] = 100
        print(nums, id(nums) == before)
        """, hint="id — номер объекта. У изменённого списка он тот же."),
    out(f"{P}-types-e2", "Что выведет программа? Строку изменить нельзя.", """
        s = "кот"
        try:
            s[0] = "К"
        except TypeError as e:
            print(e)
        before = id(s)
        s = s.upper()
        print(s, id(s) == before)
        """, hint="upper() не меняет строку, а создаёт новую."),
    out(f"{P}-types-e3", "Что выведет программа? Изменяемо или нет.", """
        values = [1, 2.5, "a", (1, 2), frozenset({1}), [1], {"a": 1}, {1, 2}, None, True]
        for v in values:
            try:
                hash(v)
                kind = "неизменяемый"
            except TypeError:
                kind = "изменяемый"
            print(type(v).__name__, kind)
        """, hint="Встроенные неизменяемые типы хешируемы, изменяемые — нет."),
    cod(f"{P}-types-e4", t("""
        Напиши функцию `is_mutable(value)` — `True` для изменяемых встроенных коллекций (`list`, `dict`, `set`, `bytearray`), иначе `False`.
        """),
        """
        def is_mutable(value):
            pass
        """,
        """
        def test_values():
            assert all(is_mutable(v) for v in [[], {}, set(), bytearray()]), "Изменяемые"
            assert not any(is_mutable(v) for v in [1, "a", (1,), frozenset(), b"x", None, 2.5]), "Неизменяемые"
        """,
        """
        def is_mutable(value):
            return isinstance(value, (list, dict, set, bytearray))
        """),
    cod(f"{P}-types-e5", t("""
        Напиши функцию `capitalize_all(words)` — список слов с заглавной первой буквой. Строки менять «на месте» нельзя — собери новые.
        """),
        """
        def capitalize_all(words):
            pass
        """,
        """
        def test_values():
            words = ["аня", "боря"]
            assert capitalize_all(words) == ["Аня", "Боря"] and words == ["аня", "боря"] and capitalize_all([]) == [], "Неверный результат"
        """,
        """
        def capitalize_all(words):
            return [w.capitalize() for w in words]
        """),
    cod(f"{P}-types-e6", t("""
        Напиши функцию `replace_char(s, index, char)` — вернуть новую строку, в которой символ на позиции `index` заменён на `char`. Используй срезы.

        ```
        replace_char("кот", 0, "К")   # → "Кот"
        ```
        """),
        """
        def replace_char(s, index, char):
            pass
        """,
        """
        def test_values():
            assert replace_char("кот", 0, "К") == "Кот" and replace_char("abc", 2, "Z") == "abZ" and replace_char("abc", 1, "") == "ac", "Неверный результат"
        """,
        """
        def replace_char(s, index, char):
            return s[:index] + char + s[index + 1:]
        """),
    cod(f"{P}-types-e7", t("""
        Напиши функцию `add_to_tuple(tpl, item)` — вернуть **новый** кортеж с добавленным в конец элементом (кортеж изменить нельзя).
        """),
        """
        def add_to_tuple(tpl, item):
            pass
        """,
        """
        def test_values():
            t = (1, 2)
            assert add_to_tuple(t, 3) == (1, 2, 3) and t == (1, 2) and add_to_tuple((), "a") == ("a",), "Неверный результат"
        """,
        """
        def add_to_tuple(tpl, item):
            return tpl + (item,)
        """),
    cod(f"{P}-types-e8", t("""
        Напиши функцию `split_by_mutability(values)` — кортеж из двух списков: `(изменяемые, неизменяемые)`. Считай значение неизменяемым, если `hash(value)` работает без `TypeError`.
        """),
        """
        def split_by_mutability(values):
            pass
        """,
        """
        def test_values():
            m, im = split_by_mutability([1, [2], "a", {"k": 1}, (3,), {4}])
            assert m == [[2], {"k": 1}, {4}] and im == [1, "a", (3,)], (m, im)
        """,
        """
        def split_by_mutability(values):
            mutable, immutable = [], []
            for v in values:
                try:
                    hash(v)
                except TypeError:
                    mutable.append(v)
                else:
                    immutable.append(v)
            return mutable, immutable
        """, xp=20),
),

lesson(f"{P}-refs", "Переменные — это ссылки",
    out(f"{P}-refs-e1", "Что выведет программа? Две переменные, один список.", """
        a = [1, 2, 3]
        b = a
        b.append(4)
        print(a)
        print(a is b, a == b)
        """, hint="b = a не копирует список, а даёт ему второе имя."),
    out(f"{P}-refs-e2", "Что выведет программа? Переприсваивание не меняет объект.", """
        a = [1, 2]
        b = a
        b = b + [3]
        print(a, b, a is b)

        x = 10
        y = x
        y += 1
        print(x, y)
        """, hint="b + [3] создаёт новый список, и имя b начинает указывать на него."),
    out(f"{P}-refs-e3", "Что выведет программа? == и is.", """
        a = [1, 2]
        b = [1, 2]
        c = a
        print(a == b, a is b, a is c)
        print(None is None, [] is [])
        """),
    cod(f"{P}-refs-e4", t("""
        Напиши функцию `same_object(a, b)` — `True`, если две переменные ссылаются на **один и тот же** объект (а не просто равные).
        """),
        """
        def same_object(a, b):
            pass
        """,
        """
        def test_values():
            x = [1]
            assert same_object(x, x) and not same_object(x, [1]) and not same_object({}, {}), "Неверный результат"
        """,
        """
        def same_object(a, b):
            return a is b
        """),
    cod(f"{P}-refs-e5", t("""
        Функция `add_item` из заготовки случайно меняет исходный список, потому что `result = items` не копирует его. Исправь: исходный список должен остаться прежним.
        """),
        """
        def add_item(items, item):
            result = items
            result.append(item)
            return result
        """,
        """
        def test_values():
            src = [1, 2]
            assert add_item(src, 3) == [1, 2, 3] and src == [1, 2], f"Исходный: {src}"
        """,
        """
        def add_item(items, item):
            result = list(items)
            result.append(item)
            return result
        """),
    cod(f"{P}-refs-e6", t("""
        Напиши функцию `count_unique_objects(items)` — сколько разных объектов в списке (по `id`, а не по значению).
        """),
        """
        def count_unique_objects(items):
            pass
        """,
        """
        def test_values():
            a = [1]
            assert count_unique_objects([a, a, [1]]) == 2 and count_unique_objects([]) == 0, "Неверный результат"
        """,
        """
        def count_unique_objects(items):
            return len({id(x) for x in items})
        """),
    cod(f"{P}-refs-e7", t("""
        Напиши функцию `make_grid(rows, cols, fill)` — список списков размером `rows × cols`, где **каждая строка — отдельный список** (изменение одной строки не должно менять другие).
        """),
        """
        def make_grid(rows, cols, fill):
            pass
        """,
        """
        def test_values():
            g = make_grid(3, 2, 0)
            g[0][0] = 9
            assert g == [[9, 0], [0, 0], [0, 0]], g
            assert make_grid(0, 5, 1) == [], "Пустая сетка"
        """,
        """
        def make_grid(rows, cols, fill):
            return [[fill] * cols for _ in range(rows)]
        """, hint="[[0] * cols] * rows — ловушка: одна строка повторена rows раз."),
    cod(f"{P}-refs-e8", t("""
        Напиши функцию `find_aliases(named)` — `named` — словарь «имя переменной → объект». Верни список групп имён (отсортированных), которые ссылаются на **один и тот же** объект, если в группе больше одного имени. Группы — в порядке первого появления.

        ```
        x = []
        find_aliases({"a": x, "b": [], "c": x})   # → [["a", "c"]]
        ```
        """),
        """
        def find_aliases(named):
            pass
        """,
        """
        def test_values():
            x, y = [], {}
            assert find_aliases({"a": x, "b": [], "c": x, "d": y, "e": y}) == [["a", "c"], ["d", "e"]] and find_aliases({"a": []}) == [], "Неверный результат"
        """,
        """
        def find_aliases(named):
            groups = {}
            for name, obj in named.items():
                groups.setdefault(id(obj), []).append(name)
            return [sorted(g) for g in groups.values() if len(g) > 1]
        """, xp=20),
),

lesson(f"{P}-ops", "Изменить на месте или создать новое",
    out(f"{P}-ops-e1", "Что выведет программа? += у списка и у кортежа.", """
        a = [1, 2]
        b = a
        a += [3]
        print(a, b)

        t = (1, 2)
        u = t
        t += (3,)
        print(t, u)
        """, hint="Для списка += меняет объект на месте, для кортежа — создаёт новый."),
    out(f"{P}-ops-e2", "Что выведет программа? sort и sorted.", """
        nums = [3, 1, 2]
        result = nums.sort()
        print(result, nums)

        nums = [3, 1, 2]
        new = sorted(nums)
        print(new, nums)
        """, hint="Методы, меняющие список на месте, возвращают None."),
    out(f"{P}-ops-e3", "Что выведет программа? Методы строки возвращают новое.", """
        s = "  Hello  "
        s.strip()
        s.lower()
        print(repr(s))
        s = s.strip().lower()
        print(repr(s))
        """),
    cod(f"{P}-ops-e4", t("""
        Исправь функцию `sorted_names` из заготовки: она возвращает `None`, потому что `list.sort()` ничего не возвращает. Функция должна вернуть **новый** отсортированный список и не менять исходный.
        """),
        """
        def sorted_names(names):
            return names.sort()
        """,
        """
        def test_values():
            src = ["вика", "аня", "боря"]
            assert sorted_names(src) == ["аня", "боря", "вика"] and src == ["вика", "аня", "боря"], "Неверный результат"
        """,
        """
        def sorted_names(names):
            return sorted(names)
        """),
    cod(f"{P}-ops-e5", t("""
        Напиши функцию `normalize_inplace(words)` — привести все слова списка к нижнему регистру **на месте** (тот же список) и вернуть `None`.
        """),
        """
        def normalize_inplace(words):
            pass
        """,
        """
        def test_values():
            w = ["Аня", "БОРЯ"]
            ref = w
            assert normalize_inplace(w) is None and w == ["аня", "боря"] and w is ref, "Неверный результат"
        """,
        """
        def normalize_inplace(words):
            for i, w in enumerate(words):
                words[i] = w.lower()
        """, hint="words[:] = [...] тоже меняет тот же список."),
    cod(f"{P}-ops-e6", t("""
        Напиши две функции:

        - `with_item(items, x)` — вернуть **новый** список с добавленным `x` (исходный не меняется);
        - `add_item(items, x)` — добавить `x` **в тот же** список и вернуть `None`.
        """),
        """
        def with_item(items, x):
            pass


        def add_item(items, x):
            pass
        """,
        """
        def test_values():
            a = [1]
            b = with_item(a, 2)
            assert b == [1, 2] and a == [1] and b is not a, "with_item"
            assert add_item(a, 3) is None and a == [1, 3], "add_item"
        """,
        """
        def with_item(items, x):
            return items + [x]


        def add_item(items, x):
            items.append(x)
        """),
    cod(f"{P}-ops-e7", t("""
        Напиши функцию `merge_settings(base, extra)` — вернуть **новый** словарь: всё из `base`, поверх — из `extra`. Ни один из исходных словарей не менять.
        """),
        """
        def merge_settings(base, extra):
            pass
        """,
        """
        def test_values():
            base, extra = {"a": 1, "b": 2}, {"b": 3}
            r = merge_settings(base, extra)
            assert r == {"a": 1, "b": 3} and base == {"a": 1, "b": 2} and extra == {"b": 3}, r
        """,
        """
        def merge_settings(base, extra):
            return {**base, **extra}
        """, hint="{**a, **b} или a | b — новый словарь; a.update(b) меняет a."),
    cod(f"{P}-ops-e8", t("""
        Напиши функцию `dedupe_inplace(items)` — убрать повторы из списка **на месте**, сохранив порядок первого появления. Вернуть количество удалённых элементов.
        """),
        """
        def dedupe_inplace(items):
            pass
        """,
        """
        def test_values():
            x = [3, 1, 3, 2, 1]
            ref = x
            assert dedupe_inplace(x) == 2 and x == [3, 1, 2] and x is ref, x
        """,
        """
        def dedupe_inplace(items):
            seen = set()
            result = []
            for x in items:
                if x not in seen:
                    seen.add(x)
                    result.append(x)
            removed = len(items) - len(result)
            items[:] = result
            return removed
        """, xp=20),
),

lesson(f"{P}-hash", "Хешируемость: ключи словаря и элементы множества",
    out(f"{P}-hash-e1", "Что выведет программа?", """
        d = {}
        d[(1, 2)] = "кортеж"
        d["a"] = "строка"
        try:
            d[[1, 2]] = "список"
        except TypeError as e:
            print(e)
        print(d)
        """, hint="Ключом словаря может быть только хешируемый объект."),
    out(f"{P}-hash-e2", "Что выведет программа? Кортеж со списком внутри.", """
        t = (1, [2, 3])
        t[1].append(4)
        print(t)
        try:
            hash(t)
        except TypeError as e:
            print(e)
        print(hash((1, (2, 3))) == hash((1, (2, 3))))
        """, hint="Кортеж неизменяем, но список внутри него — изменяем."),
    out(f"{P}-hash-e3", "Что выведет программа? frozenset.", """
        groups = {frozenset({"аня", "боря"}), frozenset({"боря", "аня"}), frozenset({"вика"})}
        print(len(groups))
        try:
            {{"a"}}
        except TypeError as e:
            print(e)
        fs = frozenset([1, 2])
        print(fs | {3}, type(fs | {3}).__name__)
        """),
    cod(f"{P}-hash-e4", t("""
        Напиши функцию `is_hashable(value)` — `True`, если значение можно использовать как ключ словаря.
        """),
        """
        def is_hashable(value):
            pass
        """,
        """
        def test_values():
            assert is_hashable(1) and is_hashable("a") and is_hashable((1, 2)) and is_hashable(frozenset()), "Хешируемые"
            assert not is_hashable([]) and not is_hashable({}) and not is_hashable((1, [2])), "Нехешируемые"
        """,
        """
        def is_hashable(value):
            try:
                hash(value)
            except TypeError:
                return False
            return True
        """),
    cod(f"{P}-hash-e5", t("""
        Напиши функцию `count_pairs(pairs)` — `pairs` — список **списков** из двух элементов. Верни словарь «пара (как кортеж) → сколько раз встретилась».
        """),
        """
        def count_pairs(pairs):
            pass
        """,
        """
        def test_values():
            assert count_pairs([[1, 2], [3, 4], [1, 2]]) == {(1, 2): 2, (3, 4): 1} and count_pairs([]) == {}, "Неверный результат"
        """,
        """
        def count_pairs(pairs):
            result = {}
            for p in pairs:
                key = tuple(p)
                result[key] = result.get(key, 0) + 1
            return result
        """),
    cod(f"{P}-hash-e6", t("""
        Напиши функцию `unique_teams(teams)` — `teams` — список списков имён. Команда — это **набор** людей, порядок не важен. Верни количество разных команд.
        """),
        """
        def unique_teams(teams):
            pass
        """,
        """
        def test_values():
            assert unique_teams([["аня", "боря"], ["боря", "аня"], ["вика"]]) == 2 and unique_teams([]) == 0, "Неверный результат"
        """,
        """
        def unique_teams(teams):
            return len({frozenset(t) for t in teams})
        """),
    cod(f"{P}-hash-e7", t("""
        Напиши функцию `unique_dicts(items)` — убрать дубликаты из списка **словарей** (с простыми значениями), сохранив порядок. Словари нехешируемы — используй в качестве ключа `tuple(sorted(d.items()))`.
        """),
        """
        def unique_dicts(items):
            pass
        """,
        """
        def test_values():
            data = [{"a": 1, "b": 2}, {"b": 2, "a": 1}, {"a": 2}]
            assert unique_dicts(data) == [{"a": 1, "b": 2}, {"a": 2}] and unique_dicts([]) == [], unique_dicts(data)
        """,
        """
        def unique_dicts(items):
            seen = set()
            result = []
            for d in items:
                key = tuple(sorted(d.items()))
                if key not in seen:
                    seen.add(key)
                    result.append(d)
            return result
        """),
    cod(f"{P}-hash-e8", t("""
        Напиши функцию `freeze(value)` — рекурсивно превратить структуру в хешируемую: список → кортеж, множество → `frozenset`, словарь → кортеж отсортированных пар `(ключ, freeze(значение))`. Остальное — как есть.
        """),
        """
        def freeze(value):
            pass
        """,
        """
        def test_values():
            r = freeze({"b": [1, {2}], "a": {"x": [3]}})
            assert r == (("a", (("x", (3,)),)), ("b", (1, frozenset({2})))), r
            hash(r)
            assert freeze(5) == 5 and freeze([]) == (), "Простые значения"
        """,
        """
        def freeze(value):
            if isinstance(value, list):
                return tuple(freeze(v) for v in value)
            if isinstance(value, set):
                return frozenset(freeze(v) for v in value)
            if isinstance(value, dict):
                return tuple(sorted((k, freeze(v)) for k, v in value.items()))
            return value
        """, xp=25),
),
)
