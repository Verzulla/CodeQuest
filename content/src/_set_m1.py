"""Тема «Множества», модуль 1 «Основы множеств» — задания. Теория — в _set_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "set"

m1 = module(f"{P}-m1", "Основы множеств", "🔵", "Создание, уникальность, add/remove/discard, принадлежность, перебор",

lesson(f"{P}-m1-l1", "Создание и уникальность",
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        s = {3, 1, 3, 2, 1}
        print(len(s), sorted(s))
        print(sorted(set("hello")))
        """, hint="Повторы в множестве не хранятся."),
    out(f"{P}-m1-l1-e2", "Что выведет программа? Пустое множество.", """
        a = {}
        b = set()
        print(type(a).__name__, type(b).__name__, len(b))
        """),
    out(f"{P}-m1-l1-e3", "Что выведет программа?", """
        tags = ["api", "ui", "api", "smoke", "ui"]
        unique = set(tags)
        print(len(tags), len(unique), "smoke" in unique)
        """),
    cod(f"{P}-m1-l1-e4", t("""
        Напиши функцию `count_unique(items)` — сколько различных элементов в списке.

        ```
        count_unique([1, 2, 2, 3, 3, 3])   # → 3
        ```
        """),
        """
        def count_unique(items):
            pass
        """,
        """
        def test_values():
            assert [count_unique([1, 2, 2, 3, 3, 3]), count_unique([]), count_unique(["a", "A"])] == [3, 0, 2], "Неверный результат"
        """,
        """
        def count_unique(items):
            return len(set(items))
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Напиши функцию `unique_sorted(items)` — отсортированный **список** различных элементов.

        ```
        unique_sorted([3, 1, 3, 2])   # → [1, 2, 3]
        ```
        """),
        """
        def unique_sorted(items):
            pass
        """,
        """
        def test_values():
            assert unique_sorted([3, 1, 3, 2]) == [1, 2, 3] and unique_sorted([]) == [], "Неверный результат"
        """,
        """
        def unique_sorted(items):
            return sorted(set(items))
        """),
    cod(f"{P}-m1-l1-e6", t("""
        Напиши функцию `letters(text)` — отсортированная строка из различных букв текста (без пробелов, в нижнем регистре).

        ```
        letters("Hello World")   # → "dehlorw"
        ```
        """),
        """
        def letters(text):
            pass
        """,
        """
        def test_values():
            assert letters("Hello World") == "dehlorw" and letters("") == "", "Неверный результат"
        """,
        """
        def letters(text):
            return "".join(sorted(set(text.lower().replace(" ", ""))))
        """),
    cod(f"{P}-m1-l1-e7", t("""
        Напиши функцию `all_unique(items)` — все ли элементы различны.

        ```
        all_unique([1, 2, 3])   # → True
        all_unique([1, 2, 1])   # → False
        ```
        """),
        """
        def all_unique(items):
            pass
        """,
        """
        def test_values():
            assert [all_unique([1, 2, 3]), all_unique([1, 2, 1]), all_unique([])] == [True, False, True], "Неверный результат"
        """,
        """
        def all_unique(items):
            return len(set(items)) == len(items)
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `empty_set()` — вернуть **пустое множество** (осторожно: `{}` — это словарь).
        """),
        """
        def empty_set():
            pass
        """,
        """
        def test_value():
            s = empty_set()
            assert isinstance(s, set) and len(s) == 0, f"Получено {s!r}"
        """,
        """
        def empty_set():
            return set()
        """),
),

lesson(f"{P}-m1-l2", "Добавление и удаление",
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        s = {1, 2}
        s.add(3)
        s.add(2)
        s.update([4, 5, 1])
        print(sorted(s))
        """, hint="add — один элемент, update — много; повторы игнорируются."),
    out(f"{P}-m1-l2-e2", "Что выведет программа? remove против discard.", """
        s = {1, 2, 3}
        s.discard(2)
        s.discard(99)
        try:
            s.remove(99)
        except KeyError:
            print("remove: KeyError")
        print(sorted(s))
        """),
    out(f"{P}-m1-l2-e3", "Что выведет программа?", """
        s = {"a"}
        x = s.pop()
        print(x, s, len(s))
        s.update("bc")
        s.clear()
        print(s)
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `add_tags(tags, new)` — добавить в множество `tags` все элементы из списка `new` **на месте**; вернуть количество элементов после добавления.

        ```
        t = {"api"}
        add_tags(t, ["ui", "api"])   # → 2, t == {"api", "ui"}
        ```
        """),
        """
        def add_tags(tags, new):
            pass
        """,
        """
        def test_values():
            t = {"api"}
            assert add_tags(t, ["ui", "api"]) == 2 and t == {"api", "ui"}, f"t = {t}"
        """,
        """
        def add_tags(tags, new):
            tags.update(new)
            return len(tags)
        """),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `safe_remove(s, item)` — удалить элемент, если он есть, без ошибок; вернуть `True`, если элемент был удалён.

        ```
        s = {1, 2}
        safe_remove(s, 2)   # → True
        safe_remove(s, 9)   # → False
        ```
        """),
        """
        def safe_remove(s, item):
            pass
        """,
        """
        def test_values():
            s = {1, 2}
            assert safe_remove(s, 2) is True and safe_remove(s, 9) is False and s == {1}, f"s = {s}"
        """,
        """
        def safe_remove(s, item):
            if item in s:
                s.discard(item)
                return True
            return False
        """),
    cod(f"{P}-m1-l2-e6", t("""
        Напиши функцию `online_users(events)` — по списку событий `("login"|"logout", имя)` вернуть отсортированный список пользователей, которые сейчас онлайн. Повторный `logout` не должен вызывать ошибку.

        ```
        online_users([("login", "a"), ("login", "b"), ("logout", "a"), ("logout", "a")])   # → ["b"]
        ```
        """),
        """
        def online_users(events):
            pass
        """,
        """
        def test_values():
            assert online_users([("login", "a"), ("login", "b"), ("logout", "a"), ("logout", "a")]) == ["b"] and online_users([]) == [], "Неверный результат"
        """,
        """
        def online_users(events):
            online = set()
            for action, name in events:
                if action == "login":
                    online.add(name)
                else:
                    online.discard(name)
            return sorted(online)
        """, xp=20),
    cod(f"{P}-m1-l2-e7", t("""
        Напиши функцию `collect_errors(lines)` — множество различных кодов ошибок из строк `"ERROR <код>"`; остальные строки пропускать. Используй `add`.

        ```
        collect_errors(["ERROR 500", "INFO ok", "ERROR 404", "ERROR 500"])   # → {"500", "404"}
        ```
        """),
        """
        def collect_errors(lines):
            pass
        """,
        """
        def test_values():
            assert collect_errors(["ERROR 500", "INFO ok", "ERROR 404", "ERROR 500"]) == {"500", "404"} and collect_errors([]) == set(), "Неверный результат"
        """,
        """
        def collect_errors(lines):
            codes = set()
            for line in lines:
                if line.startswith("ERROR "):
                    codes.add(line.split()[1])
            return codes
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши функцию `drain(s)` — снимать элементы множества через `pop()`, пока оно не опустеет, и вернуть **отсортированный** список снятых. Исходное множество должно стать пустым.
        """),
        """
        def drain(s):
            pass
        """,
        """
        def test_values():
            s = {3, 1, 2}
            assert drain(s) == [1, 2, 3] and s == set(), f"s = {s}"
        """,
        """
        def drain(s):
            taken = []
            while s:
                taken.append(s.pop())
            return sorted(taken)
        """),
),

lesson(f"{P}-m1-l3", "Принадлежность, скорость и хешируемость",
    out(f"{P}-m1-l3-e1", "Что выведет программа?", """
        allowed = {"GET", "POST"}
        for m in ["get", "POST", "DELETE"]:
            print(m, m.upper() in allowed)
        """),
    out(f"{P}-m1-l3-e2", "Что выведет программа? Что можно положить в множество.", """
        s = {1, "a", (1, 2), None}
        print(len(s))
        try:
            s.add([1, 2])
        except TypeError as e:
            print("TypeError:", e)
        """),
    out(f"{P}-m1-l3-e3", "Что выведет программа? 1 и True.", """
        s = {1, True, 1.0, 2}
        print(len(s), sorted(s))
        """, hint="1 == True == 1.0 — для множества это одно значение."),
    cod(f"{P}-m1-l3-e4", t("""
        Напиши функцию `first_repeat(items)` — первый элемент, который встречается **повторно** (при проходе слева направо), или `None`. Храни уже виденные в множестве.

        ```
        first_repeat([3, 1, 4, 1, 3])   # → 1
        ```
        """),
        """
        def first_repeat(items):
            pass
        """,
        """
        def test_values():
            assert [first_repeat([3, 1, 4, 1, 3]), first_repeat([1, 2]), first_repeat([])] == [1, None, None], "Неверный результат"
        """,
        """
        def first_repeat(items):
            seen = set()
            for x in items:
                if x in seen:
                    return x
                seen.add(x)
            return None
        """),
    cod(f"{P}-m1-l3-e5", t("""
        Напиши функцию `is_allowed(method)` — есть ли HTTP-метод (в любом регистре) в множестве `ALLOWED = {"GET", "POST", "PUT", "DELETE"}`.
        """),
        """
        ALLOWED = {"GET", "POST", "PUT", "DELETE"}

        def is_allowed(method):
            pass
        """,
        """
        def test_values():
            assert [is_allowed("get"), is_allowed("Patch"), is_allowed("DELETE")] == [True, False, True], "Неверный результат"
        """,
        """
        ALLOWED = {"GET", "POST", "PUT", "DELETE"}

        def is_allowed(method):
            return method.upper() in ALLOWED
        """),
    cod(f"{P}-m1-l3-e6", t("""
        Напиши функцию `unique_points(points)` — количество различных точек в списке списков `[x, y]`. Список в множество не положить — превращай в кортеж.

        ```
        unique_points([[1, 2], [3, 4], [1, 2]])   # → 2
        ```
        """),
        """
        def unique_points(points):
            pass
        """,
        """
        def test_values():
            assert unique_points([[1, 2], [3, 4], [1, 2]]) == 2 and unique_points([]) == 0, "Неверный результат"
        """,
        """
        def unique_points(points):
            return len({tuple(p) for p in points})
        """),
    cod(f"{P}-m1-l3-e7", t("""
        Напиши функцию `filter_banned(words, banned)` — слова, которых нет в списке запрещённых. Для быстрой проверки преврати `banned` в множество один раз.

        ```
        filter_banned(["a", "spam", "b"], ["spam", "ads"])   # → ["a", "b"]
        ```
        """),
        """
        def filter_banned(words, banned):
            pass
        """,
        """
        def test_values():
            assert filter_banned(["a", "spam", "b"], ["spam", "ads"]) == ["a", "b"] and filter_banned([], ["x"]) == [], "Неверный результат"
        """,
        """
        def filter_banned(words, banned):
            banned_set = set(banned)
            return [w for w in words if w not in banned_set]
        """),
    cod(f"{P}-m1-l3-e8", t("""
        Напиши функцию `has_pair_sum(nums, target)` — есть ли два **разных по позиции** числа с суммой `target`. Проход один: для каждого числа проверяй, встречалось ли уже `target - n`.

        ```
        has_pair_sum([3, 8, 1, 5], 9)   # → True   (8 + 1)
        has_pair_sum([4], 8)            # → False
        ```
        """),
        """
        def has_pair_sum(nums, target):
            pass
        """,
        """
        def test_values():
            assert [has_pair_sum([3, 8, 1, 5], 9), has_pair_sum([4], 8), has_pair_sum([4, 4], 8), has_pair_sum([], 0)] == [True, False, True, False], "Неверный результат"
        """,
        """
        def has_pair_sum(nums, target):
            seen = set()
            for n in nums:
                if target - n in seen:
                    return True
                seen.add(n)
            return False
        """, xp=20),
),

lesson(f"{P}-m1-l4", "Перебор, порядок и преобразования",
    out(f"{P}-m1-l4-e1", "Что выведет программа?", """
        s = {"b", "a", "c"}
        print(sorted(s))
        print(sorted(s, reverse=True))
        print(list(sorted(s))[0])
        """, hint="Порядок элементов множества не гарантирован — сортируй для вывода."),
    out(f"{P}-m1-l4-e2", "Что выведет программа?", """
        s = {x % 4 for x in range(10)}
        print(sorted(s), sum(s), max(s))
        """),
    out(f"{P}-m1-l4-e3", "Что выведет программа?", """
        nums = [5, 1, 5, 3, 1]
        print(sorted(set(nums)))
        print(list(dict.fromkeys(nums)))
        """, hint="dict.fromkeys сохраняет порядок первого появления, set — нет."),
    cod(f"{P}-m1-l4-e4", t("""
        Напиши функцию `unique_in_order(items)` — элементы без повторов **в порядке первого появления**.

        ```
        unique_in_order([3, 1, 3, 2, 1])   # → [3, 1, 2]
        ```
        """),
        """
        def unique_in_order(items):
            pass
        """,
        """
        def test_values():
            assert unique_in_order([3, 1, 3, 2, 1]) == [3, 1, 2] and unique_in_order([]) == [], "Неверный результат"
        """,
        """
        def unique_in_order(items):
            seen = set()
            result = []
            for x in items:
                if x not in seen:
                    seen.add(x)
                    result.append(x)
            return result
        """),
    cod(f"{P}-m1-l4-e5", t("""
        Напиши функцию `set_summary(s)` — строка `"<количество>: <элементы через запятую по алфавиту>"`.

        ```
        set_summary({"ui", "api"})   # → "2: api, ui"
        ```
        """),
        """
        def set_summary(s):
            pass
        """,
        """
        def test_values():
            assert set_summary({"ui", "api"}) == "2: api, ui" and set_summary(set()) == "0: ", "Неверная строка"
        """,
        """
        def set_summary(s):
            return f"{len(s)}: " + ", ".join(sorted(s))
        """),
    cod(f"{P}-m1-l4-e6", t("""
        Напиши функцию `word_set(text)` — множество различных слов текста в нижнем регистре, без знаков `.,!?` по краям слов.

        ```
        word_set("Тест, тест! Ok.")   # → {"тест", "ok"}
        ```
        """),
        """
        def word_set(text):
            pass
        """,
        """
        def test_values():
            assert word_set("Тест, тест! Ok.") == {"тест", "ok"} and word_set("") == set(), "Неверный результат"
        """,
        """
        def word_set(text):
            return {w.strip(".,!?").lower() for w in text.split()}
        """),
    cod(f"{P}-m1-l4-e7", t("""
        Напиши функцию `smallest_missing(nums)` — наименьшее **положительное** целое, которого нет в списке.

        ```
        smallest_missing([3, 1, 2, 5])   # → 4
        smallest_missing([-1, 0])        # → 1
        ```
        """),
        """
        def smallest_missing(nums):
            pass
        """,
        """
        def test_values():
            assert [smallest_missing([3, 1, 2, 5]), smallest_missing([-1, 0]), smallest_missing([1, 2, 3])] == [4, 1, 4], "Неверный результат"
        """,
        """
        def smallest_missing(nums):
            present = set(nums)
            n = 1
            while n in present:
                n += 1
            return n
        """, xp=20),
    cod(f"{P}-m1-l4-e8", t("""
        Напиши функцию `longest_run(nums)` — длина самой длинной последовательности **подряд идущих целых чисел** (в любом порядке в списке).

        ```
        longest_run([100, 4, 200, 1, 3, 2])   # → 4   (1, 2, 3, 4)
        ```
        Подсказка: начинай отсчёт только с тех `n`, для которых `n - 1` нет в множестве.
        """),
        """
        def longest_run(nums):
            pass
        """,
        """
        def test_values():
            assert [longest_run([100, 4, 200, 1, 3, 2]), longest_run([]), longest_run([5, 5]), longest_run([1, 3])] == [4, 0, 1, 1], "Неверный результат"
        """,
        """
        def longest_run(nums):
            s = set(nums)
            best = 0
            for n in s:
                if n - 1 not in s:
                    length = 1
                    while n + length in s:
                        length += 1
                    best = max(best, length)
            return best
        """, xp=25),
),
)
