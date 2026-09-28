"""Тема «Цикл for», модуль 3 «Шаблоны циклов» — задания. Теория — в _for_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "for"

m3 = module(f"{P}-m3", "Шаблоны циклов", "🧮", "Накопление, минимум и максимум, поиск, новый список, enumerate/zip/sorted",

lesson(f"{P}-m3-l1", "Подсчёт и накопление",
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        text = "я иду домой"
        vowels = 0
        for ch in text:
            if ch in "аеёиоуыэюя":
                vowels += 1
        print(vowels)
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа?", """
        counts = {}
        for r in ["pass", "fail", "pass", "skip", "pass"]:
            counts[r] = counts.get(r, 0) + 1
        print(counts)
        """),
    out(f"{P}-m3-l1-e6", "Что выведет программа? Произведение и строка-накопитель.", """
        result = 1
        for n in [2, 3, 4]:
            result *= n
        line = ""
        for ch in "abc":
            line = ch + line
        print(result, line)
        """, hint="Произведение начинают с 1. ch + line приписывает букву слева."),
    cod(f"{P}-m3-l1-e3", t("""
        Напиши функцию `factorial(n)` — произведение чисел от 1 до `n` (для 0 — 1). Используй цикл `for`.

        Примеры:
        ```
        factorial(5)   # → 120
        factorial(0)   # → 1
        ```
        """),
        """
        def factorial(n):
            pass
        """,
        """
        def test_values():
            assert [factorial(n) for n in (0, 1, 5, 10)] == [1, 1, 120, 3628800], "Неверный факториал"
        """,
        """
        def factorial(n):
            result = 1
            for i in range(2, n + 1):
                result *= i
            return result
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `word_freq(text)` — словарь «слово → сколько раз встретилось». Слова сравнивать в нижнем регистре, разбивать по пробелам.

        Пример:
        ```
        word_freq("Тест упал тест прошёл Тест")   # → {"тест": 3, "упал": 1, "прошёл": 1}
        ```
        """),
        """
        def word_freq(text):
            pass
        """,
        """
        def test_values():
            assert word_freq("Тест упал тест прошёл Тест") == {"тест": 3, "упал": 1, "прошёл": 1}, f"Получено {word_freq('Тест упал тест прошёл Тест')}"
            assert word_freq("") == {}, "Пустая строка — пустой словарь"
        """,
        """
        def word_freq(text):
            freq = {}
            for word in text.lower().split():
                freq[word] = freq.get(word, 0) + 1
            return freq
        """),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `acronym(phrase)` — аббревиатура из первых букв слов, заглавными. Накапливай результат в строке через `+=`.

        Примеры:
        ```
        acronym("continuous integration")   # → "CI"
        acronym("quality assurance team")   # → "QAT"
        ```
        """),
        """
        def acronym(phrase):
            pass
        """,
        """
        def test_values():
            assert acronym("continuous integration") == "CI" and acronym("quality assurance team") == "QAT" and acronym("") == "", "Неверная аббревиатура"
        """,
        """
        def acronym(phrase):
            result = ""
            for word in phrase.split():
                result += word[0].upper()
            return result
        """),
    cod(f"{P}-m3-l1-e7", t("""
        Напиши функцию `count_by_first_letter(words)` — словарь «первая буква (в нижнем регистре) → сколько слов на неё начинается».

        Пример:
        ```
        count_by_first_letter(["Аня", "анна", "Боря"])   # → {"а": 2, "б": 1}
        ```
        """),
        """
        def count_by_first_letter(words):
            pass
        """,
        """
        def test_values():
            got = count_by_first_letter(["Аня", "анна", "Боря"])
            assert got == {"а": 2, "б": 1} and count_by_first_letter([]) == {}, f"Получено {got}"
        """,
        """
        def count_by_first_letter(words):
            counts = {}
            for w in words:
                letter = w[0].lower()
                counts[letter] = counts.get(letter, 0) + 1
            return counts
        """, hint="counts.get(letter, 0) + 1 — как в подсчёте слов."),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `running_total(nums)` — список **нарастающих** сумм: каждый элемент — сумма всех чисел до него включительно.

        Примеры:
        ```
        running_total([1, 2, 3, 4])   # → [1, 3, 6, 10]
        running_total([])             # → []
        ```
        """),
        """
        def running_total(nums):
            pass
        """,
        """
        def test_values():
            assert running_total([1, 2, 3, 4]) == [1, 3, 6, 10] and running_total([]) == [] and running_total([5, -5]) == [5, 0], "Неверный результат"
        """,
        """
        def running_total(nums):
            result = []
            total = 0
            for n in nums:
                total += n
                result.append(total)
            return result
        """),
),

lesson(f"{P}-minmax", "Минимум, максимум и лучший элемент",
    out(f"{P}-minmax-e1", "Что выведет программа?", """
        nums = [4, 9, 2, 7]
        best = nums[0]
        for n in nums:
            if n > best:
                best = n
        print(best)
        """),
    out(f"{P}-minmax-e2", "Что выведет программа? Найди ошибку в начальном значении.", """
        nums = [-5, -2, -9]
        best = 0
        for n in nums:
            if n > best:
                best = n
        print(best, max(nums))
        """, hint="Ни одно число не больше 0 — best так и остался нулём."),
    out(f"{P}-minmax-e3", "Что выведет программа? Ищем не значение, а позицию.", """
        scores = [70, 95, 80, 95]
        best_i = 0
        for i in range(1, len(scores)):
            if scores[i] > scores[best_i]:
                best_i = i
        print(best_i, scores[best_i])
        """, hint="Строгое > не заменяет при равенстве — остаётся первый максимум."),
    cod(f"{P}-minmax-e4", t("""
        Напиши функцию `my_min(nums)` — наименьшее число списка, без `min` и `sorted`. Для пустого списка — `None`.

        Примеры:
        ```
        my_min([4, -2, 7])   # → -2
        my_min([])           # → None
        ```
        """),
        """
        def my_min(nums):
            pass
        """,
        """
        def test_values():
            assert my_min([4, -2, 7]) == -2 and my_min([]) is None and my_min([5]) == 5 and my_min([3, 1, 1]) == 1, "Неверный минимум"

        def test_no_builtin():
            src = open("solution.py", encoding="utf-8").read()
            assert "min(" not in src.replace("my_min(", "") and "sorted(" not in src, "Реши циклом, без min/sorted"
        """,
        """
        def my_min(nums):
            if not nums:
                return None
            best = nums[0]
            for n in nums:
                if n < best:
                    best = n
            return best
        """, hint="Пустой список проверь заранее, а начальное значение возьми nums[0]."),
    cod(f"{P}-minmax-e5", t("""
        Напиши функцию `min_max(nums)` — пара `(минимум, максимум)` за **один** проход цикла, без `min`/`max`. Для пустого списка — `None`.

        Примеры:
        ```
        min_max([3, 8, -1, 5])   # → (-1, 8)
        min_max([7])             # → (7, 7)
        ```
        """),
        """
        def min_max(nums):
            pass
        """,
        """
        def test_values():
            got = [min_max([3, 8, -1, 5]), min_max([7]), min_max([])]
            assert got == [(-1, 8), (7, 7), None], f"Получено {got}"

        def test_no_builtin():
            src = open("solution.py", encoding="utf-8").read().replace("min_max(", "")
            assert "min(" not in src and "max(" not in src, "Реши циклом, без min/max"
        """,
        """
        def min_max(nums):
            if not nums:
                return None
            low = high = nums[0]
            for n in nums:
                if n < low:
                    low = n
                if n > high:
                    high = n
            return (low, high)
        """),
    cod(f"{P}-minmax-e6", t("""
        Напиши функцию `slowest_test(results)`, где `results` — список пар `(имя теста, секунды)`. Верни **имя** самого долгого теста; при равенстве — первого из них. Пустой список — `None`.

        Пример:
        ```
        slowest_test([("login", 1.2), ("pay", 3.5), ("search", 3.5)])   # → "pay"
        ```
        """),
        """
        def slowest_test(results):
            pass
        """,
        """
        def test_values():
            got = [slowest_test([("login", 1.2), ("pay", 3.5), ("search", 3.5)]), slowest_test([]), slowest_test([("a", 0)])]
            assert got == ["pay", None, "a"], f"Получено {got}"
        """,
        """
        def slowest_test(results):
            best_name = None
            best_time = None
            for name, seconds in results:
                if best_time is None or seconds > best_time:
                    best_name = name
                    best_time = seconds
            return best_name
        """, hint="Храни сразу два значения: лучшее время и имя. None как начальное значение — «ещё ничего не видели».", xp=20),
    cod(f"{P}-minmax-e7", t("""
        Напиши функцию `second_largest(nums)` — второе по величине **различное** значение. Если такого нет — `None`.

        Примеры:
        ```
        second_largest([5, 1, 5, 3])   # → 3
        second_largest([4, 4])         # → None
        ```
        """),
        """
        def second_largest(nums):
            pass
        """,
        """
        def test_values():
            got = [second_largest([5, 1, 5, 3]), second_largest([4, 4]), second_largest([]), second_largest([1, 2]), second_largest([-1, -5, -3])]
            assert got == [3, None, None, 1, -3], f"Получено {got}"
        """,
        """
        def second_largest(nums):
            first = None
            second = None
            for n in nums:
                if first is None or n > first:
                    second = first
                    first = n
                elif n != first and (second is None or n > second):
                    second = n
            return second
        """, hint="Храни два значения: first и second. Новый максимум сдвигает старый на второе место; равное first пропускай.", xp=25),
    cod(f"{P}-minmax-e8", t("""
        Напиши функцию `longest_streak(results)` — длина самой длинной серии подряд идущих `"pass"`.

        Примеры:
        ```
        longest_streak(["pass", "pass", "fail", "pass"])   # → 2
        longest_streak(["fail"])                           # → 0
        ```
        """),
        """
        def longest_streak(results):
            pass
        """,
        """
        def test_values():
            got = [longest_streak(x) for x in (["pass", "pass", "fail", "pass"], ["fail"], [], ["pass"] * 3, ["pass", "fail", "pass", "pass", "pass", "fail"])]
            assert got == [2, 0, 0, 3, 3], f"Получено {got}"
        """,
        """
        def longest_streak(results):
            best = 0
            current = 0
            for r in results:
                if r == "pass":
                    current += 1
                    if current > best:
                        best = current
                else:
                    current = 0
            return best
        """, hint="Два счётчика: текущая серия (обнуляется на fail) и лучшая.", xp=20),
),

lesson(f"{P}-m3-l2", "Поиск в цикле",
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        users = [{"name": "Аня", "role": "qa"}, {"name": "Боря", "role": "admin"}]
        admin = None
        for u in users:
            if u["role"] == "admin":
                admin = u["name"]
                break
        print(admin)
        print(any(u["role"] == "dev" for u in users))
        """),
    out(f"{P}-m3-l2-e2", "Что выведет программа?", """
        nums = [7, 3, 9, 3]
        pos = -1
        for i, n in enumerate(nums):
            if n == 3:
                pos = i
        print(pos)
        """, hint="Без break в переменной останется индекс последнего совпадения."),
    out(f"{P}-m3-l2-e6", "Что выведет программа? Найти все позиции.", """
        text = "banana"
        positions = []
        for i, ch in enumerate(text):
            if ch == "a":
                positions.append(i)
        print(positions, len(positions))
        """),
    cod(f"{P}-m3-l2-e3", t("""
        Напиши функцию `find_user(users, name)` — словарь пользователя с данным именем (поле `"name"`) или `None`.

        Пример:
        ```
        users = [{"name": "Аня", "age": 25}, {"name": "Боря", "age": 30}]
        find_user(users, "Боря")   # → {"name": "Боря", "age": 30}
        find_user(users, "Гоша")   # → None
        ```
        """),
        """
        def find_user(users, name):
            pass
        """,
        """
        def test_values():
            users = [{"name": "Аня", "age": 25}, {"name": "Боря", "age": 30}]
            assert find_user(users, "Боря") == {"name": "Боря", "age": 30} and find_user(users, "Гоша") is None, "Неверный результат"
        """,
        """
        def find_user(users, name):
            for u in users:
                if u["name"] == name:
                    return u
            return None
        """),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши функцию `last_index(items, value)` — индекс **последнего** вхождения `value` или `-1`.

        Примеры:
        ```
        last_index([1, 2, 1, 3], 1)   # → 2
        last_index([1, 2], 5)         # → -1
        ```
        """),
        """
        def last_index(items, value):
            pass
        """,
        """
        def test_values():
            assert last_index([1, 2, 1, 3], 1) == 2 and last_index([1, 2], 5) == -1 and last_index([], 1) == -1, "Неверный индекс"
        """,
        """
        def last_index(items, value):
            pos = -1
            for i, x in enumerate(items):
                if x == value:
                    pos = i
            return pos
        """),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `has_duplicates(items)` — есть ли в списке повторяющиеся элементы. Иди циклом и храни уже виденные элементы в **множестве** `seen`: как только элемент уже в `seen` — сразу `True`.

        Примеры:
        ```
        has_duplicates([1, 2, 3, 2])   # → True
        has_duplicates(["a", "b"])     # → False
        ```
        """),
        """
        def has_duplicates(items):
            pass
        """,
        """
        def test_values():
            assert has_duplicates([1, 2, 3, 2]) is True and has_duplicates(["a", "b"]) is False and has_duplicates([]) is False, "Неверный результат"
        """,
        """
        def has_duplicates(items):
            seen = set()
            for x in items:
                if x in seen:
                    return True
                seen.add(x)
            return False
        """, xp=20),
    cod(f"{P}-m3-l2-e7", t("""
        Напиши функцию `all_indexes(items, value)` — список **всех** индексов, где встречается `value`.

        Примеры:
        ```
        all_indexes([1, 2, 1, 3, 1], 1)   # → [0, 2, 4]
        all_indexes(["a"], "b")           # → []
        ```
        """),
        """
        def all_indexes(items, value):
            pass
        """,
        """
        def test_values():
            assert all_indexes([1, 2, 1, 3, 1], 1) == [0, 2, 4] and all_indexes(["a"], "b") == [] and all_indexes("abca", "a") == [0, 3], "Неверный результат"
        """,
        """
        def all_indexes(items, value):
            result = []
            for i, x in enumerate(items):
                if x == value:
                    result.append(i)
            return result
        """),
    cod(f"{P}-m3-l2-e8", t("""
        Напиши функцию `find_by_prefix(names, prefix)` — первое имя, которое начинается с `prefix` **без учёта регистра**, или `None`.

        Примеры:
        ```
        find_by_prefix(["Анна", "Борис", "Богдан"], "бо")   # → "Борис"
        find_by_prefix(["Анна"], "Я")                       # → None
        ```
        """),
        """
        def find_by_prefix(names, prefix):
            pass
        """,
        """
        def test_values():
            got = [find_by_prefix(["Анна", "Борис", "Богдан"], "бо"), find_by_prefix(["Анна"], "Я"), find_by_prefix([], "a"), find_by_prefix(["qa-bot"], "QA")]
            assert got == ["Борис", None, None, "qa-bot"], f"Получено {got}"
        """,
        """
        def find_by_prefix(names, prefix):
            for name in names:
                if name.lower().startswith(prefix.lower()):
                    return name
            return None
        """, hint="Приведи к нижнему регистру обе строки, но верни исходное имя."),
),

lesson(f"{P}-build", "Новый список: фильтр и преобразование",
    out(f"{P}-build-e1", "Что выведет программа?", """
        prices = [100, 250, 40, 500]
        cheap = []
        for p in prices:
            if p < 200:
                cheap.append(p)
        print(cheap, prices)
        """),
    out(f"{P}-build-e2", "Что выведет программа? Удаление во время перебора.", """
        nums = [1, 2, 2, 3]
        for n in nums:
            if n == 2:
                nums.remove(n)
        print(nums)
        """, hint="После удаления элементы сдвигаются, и цикл перескакивает через следующий."),
    out(f"{P}-build-e3", "Что выведет программа? Цикл и списковое включение.", """
        words = ["api", "ui", "db"]
        upper = []
        for w in words:
            upper.append(w.upper())
        print(upper == [w.upper() for w in words], upper)
        """),
    cod(f"{P}-build-e4", t("""
        Напиши функцию `only_errors(codes)` — новый список только из кодов ответа `>= 400`, в исходном порядке.

        Пример:
        ```
        only_errors([200, 404, 301, 500])   # → [404, 500]
        ```
        """),
        """
        def only_errors(codes):
            pass
        """,
        """
        def test_values():
            assert only_errors([200, 404, 301, 500]) == [404, 500] and only_errors([200]) == [] and only_errors([]) == [], "Неверный результат"
        """,
        """
        def only_errors(codes):
            result = []
            for code in codes:
                if code >= 400:
                    result.append(code)
            return result
        """),
    cod(f"{P}-build-e5", t("""
        Напиши функцию `apply_discount_all(prices, percent)` — новый список цен со скидкой `percent` процентов, каждая округлена до 2 знаков. Исходный список не менять.

        Пример:
        ```
        apply_discount_all([100, 250, 99.9], 10)   # → [90.0, 225.0, 89.91]
        ```
        """),
        """
        def apply_discount_all(prices, percent):
            pass
        """,
        """
        def test_values():
            src = [100, 250, 99.9]
            got = apply_discount_all(src, 10)
            assert got == [90.0, 225.0, 89.91], f"Получено {got}"
            assert src == [100, 250, 99.9], "Исходный список изменился"
        """,
        """
        def apply_discount_all(prices, percent):
            result = []
            for p in prices:
                result.append(round(p * (1 - percent / 100), 2))
            return result
        """),
    cod(f"{P}-build-e6", t("""
        Напиши функцию `remove_all(items, value)` — **новый** список без всех вхождений `value`. Исходный не менять, метод `remove` не использовать.

        Пример:
        ```
        remove_all([1, 2, 2, 3, 2], 2)   # → [1, 3]
        ```
        """),
        """
        def remove_all(items, value):
            pass
        """,
        """
        def test_values():
            src = [1, 2, 2, 3, 2]
            assert remove_all(src, 2) == [1, 3] and src == [1, 2, 2, 3, 2], "Неверный результат или исходный список изменился"
            assert remove_all([], 1) == [] and remove_all([5], 1) == [5], "Неверный результат"

        def test_no_remove():
            assert ".remove(" not in open("solution.py", encoding="utf-8").read(), "Не используй remove — собери новый список"
        """,
        """
        def remove_all(items, value):
            result = []
            for x in items:
                if x != value:
                    result.append(x)
            return result
        """, hint="Не удаляй, а собирай: добавляй в новый список всё, что не равно value."),
    cod(f"{P}-build-e7", t("""
        Напиши функцию `flatten_once(lists)` — склеить список списков в один список.

        Пример:
        ```
        flatten_once([[1, 2], [3], [], [4, 5]])   # → [1, 2, 3, 4, 5]
        ```
        """),
        """
        def flatten_once(lists):
            pass
        """,
        """
        def test_values():
            assert flatten_once([[1, 2], [3], [], [4, 5]]) == [1, 2, 3, 4, 5] and flatten_once([]) == [], "Неверный результат"
        """,
        """
        def flatten_once(lists):
            result = []
            for part in lists:
                result.extend(part)
            return result
        """, hint="extend добавляет все элементы другого списка; можно и вложенным циклом с append."),
    cod(f"{P}-build-e8", t("""
        Напиши функцию `normalize_emails(emails)` — почистить список адресов:

        - убрать пробелы по краям и перевести в нижний регистр;
        - пропустить пустые строки и строки без `@`;
        - убрать повторы, сохранив порядок первого появления.

        Пример:
        ```
        normalize_emails([" Anna@Mail.ru", "bob", "anna@mail.ru ", "", "Bob@x.io"])
        # → ["anna@mail.ru", "bob@x.io"]
        ```
        """),
        """
        def normalize_emails(emails):
            pass
        """,
        """
        def test_values():
            got = normalize_emails([" Anna@Mail.ru", "bob", "anna@mail.ru ", "", "Bob@x.io"])
            assert got == ["anna@mail.ru", "bob@x.io"] and normalize_emails([]) == [], f"Получено {got}"
        """,
        """
        def normalize_emails(emails):
            result = []
            for e in emails:
                e = e.strip().lower()
                if "@" not in e:
                    continue
                if e not in result:
                    result.append(e)
            return result
        """, hint="Сначала почисти строку, потом проверки через continue, потом «нет ли уже в результате».", xp=20),
),

lesson(f"{P}-m3-l3", "Помощники перебора",
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        for i, name in enumerate(reversed(["a", "b", "c"]), start=1):
            print(i, name)
        """),
    out(f"{P}-m3-l3-e2", "Что выведет программа?", """
        prices = {"чай": 300, "кофе": 500, "сок": 150}
        for item, price in sorted(prices.items(), key=lambda p: p[1]):
            print(item, price)
        """),
    out(f"{P}-m3-l3-e6", "Что выведет программа? Списки разной длины.", """
        names = ["Аня", "Боря", "Вика"]
        ages = [25, 30]
        for name, age in zip(names, ages):
            print(name, age)
        print(len(list(zip(names, ages))))
        """, hint="zip останавливается на самом коротком списке."),
    cod(f"{P}-m3-l3-e3", t("""
        Напиши функцию `leaderboard(scores)`, где `scores` — словарь `{имя: очки}`. Вернуть список строк `"<место>. <имя> — <очки>"`, отсортированный по убыванию очков, места с 1.

        Пример:
        ```
        leaderboard({"Боря": 50, "Аня": 80, "Вика": 65})
        # → ["1. Аня — 80", "2. Вика — 65", "3. Боря — 50"]
        ```
        """),
        """
        def leaderboard(scores):
            pass
        """,
        """
        def test_values():
            got = leaderboard({"Боря": 50, "Аня": 80, "Вика": 65})
            assert got == ["1. Аня — 80", "2. Вика — 65", "3. Боря — 50"], f"Получено {got}"
        """,
        """
        def leaderboard(scores):
            ordered = sorted(scores.items(), key=lambda p: p[1], reverse=True)
            return [f"{i}. {name} — {pts}" for i, (name, pts) in enumerate(ordered, start=1)]
        """, xp=20),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `diff_report(expected, actual)` — сравни два списка одинаковой длины попарно (`zip`) и верни список строк для **несовпадений** в формате `"#<номер с 1>: ожидали <e>, получили <a>"`.

        Пример:
        ```
        diff_report([200, 201, 404], [200, 500, 404])
        # → ["#2: ожидали 201, получили 500"]
        ```
        """),
        """
        def diff_report(expected, actual):
            pass
        """,
        """
        def test_values():
            assert diff_report([200, 201, 404], [200, 500, 404]) == ["#2: ожидали 201, получили 500"], "Неверный отчёт"
            assert diff_report([1], [1]) == [], "Совпадают — пусто"
        """,
        """
        def diff_report(expected, actual):
            report = []
            for i, (e, a) in enumerate(zip(expected, actual), start=1):
                if e != a:
                    report.append(f"#{i}: ожидали {e}, получили {a}")
            return report
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `last_n_lines(lines, n)` — последние `n` строк лога **в обратном порядке** (самая свежая первой), каждая с номером строки в исходном списке (с 1): `"<номер>: <строка>"`.

        Пример:
        ```
        last_n_lines(["a", "b", "c", "d"], 2)   # → ["4: d", "3: c"]
        ```
        Используй `enumerate` и `reversed` (или срез).
        """),
        """
        def last_n_lines(lines, n):
            pass
        """,
        """
        def test_values():
            assert last_n_lines(["a", "b", "c", "d"], 2) == ["4: d", "3: c"] and last_n_lines(["x"], 5) == ["1: x"] and last_n_lines([], 3) == [], "Неверный результат"
        """,
        """
        def last_n_lines(lines, n):
            numbered = [f"{i}: {line}" for i, line in enumerate(lines, start=1)]
            return list(reversed(numbered))[:n]
        """),
    cod(f"{P}-m3-l3-e7", t("""
        Напиши функцию `to_dict(keys, values)` — словарь из двух списков: `keys[i] → values[i]`. Используй `zip` в цикле. Если списки разной длины — лишние элементы отбрасываются.

        Пример:
        ```
        to_dict(["host", "port"], ["localhost", 8080])   # → {"host": "localhost", "port": 8080}
        ```
        """),
        """
        def to_dict(keys, values):
            pass
        """,
        """
        def test_values():
            assert to_dict(["host", "port"], ["localhost", 8080]) == {"host": "localhost", "port": 8080}, "Неверный словарь"
            assert to_dict(["a", "b"], [1]) == {"a": 1} and to_dict([], []) == {}, "Неверный результат"

        def test_zip():
            assert "zip(" in open("solution.py", encoding="utf-8").read(), "Используй zip"
        """,
        """
        def to_dict(keys, values):
            result = {}
            for k, v in zip(keys, values):
                result[k] = v
            return result
        """),
    cod(f"{P}-m3-l3-e8", t("""
        Напиши функцию `numbered(items, start=1)` — список строк `"N. элемент"`, нумерация начинается со `start`. Используй `enumerate` с параметром `start`.

        Примеры:
        ```
        numbered(["login", "pay"])      # → ["1. login", "2. pay"]
        numbered(["x", "y"], start=0)   # → ["0. x", "1. y"]
        ```
        """),
        """
        def numbered(items, start=1):
            pass
        """,
        """
        def test_values():
            assert numbered(["login", "pay"]) == ["1. login", "2. pay"] and numbered(["x", "y"], start=0) == ["0. x", "1. y"] and numbered([]) == [], "Неверный результат"

        def test_enumerate():
            assert "enumerate(" in open("solution.py", encoding="utf-8").read(), "Используй enumerate"
        """,
        """
        def numbered(items, start=1):
            result = []
            for i, item in enumerate(items, start=start):
                result.append(f"{i}. {item}")
            return result
        """),
),
)
