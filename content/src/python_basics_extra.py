"""Дополнительная практика к урокам «Python: основы» (по slug урока)."""
from ._lib import t, cod, out

P = "pyb"

EXTRA = {
    f"{P}-m1-l1": [
        out(f"{P}-m1-l1-x1", "Что выведет программа? Параметр `sep` задаёт разделитель.", """
            print("2024", "09", "27", sep="-")
            """, hint="Вместо пробела между значениями будет стоять `sep`."),
        cod(f"{P}-m1-l1-x2", t("""
            Выведи заголовок с «рамкой» из знаков `=`.

            Ожидаемый вывод:
            ```
            ===== START =====
            ```
            Слева и справа — ровно по 5 знаков `=`, между ними и словом `START` по одному пробелу.

            Не набирай пять `=` вручную: строку можно умножить на число — `"=" * 5` даёт `=====`.
            """),
            "",
            """
            def test_line():
                assert OUTPUT.strip() == "===== START =====", f"Напечатано {OUTPUT.strip()!r}"
            """,
            """
            print("=" * 5, "START", "=" * 5)
            """,
            hint="`print(\"=\" * 5, \"START\", \"=\" * 5)` — три значения через пробел."),
    ],
    f"{P}-m1-l2": [
        out(f"{P}-m1-l2-x1", "Что выведет программа? Строки можно складывать.", """
            first = "Код"
            second = "Квест"
            name = first + second
            print(name)
            print(len(name))
            """, hint="`+` склеивает строки без пробела, `len` считает символы."),
        cod(f"{P}-m1-l2-x2", t("""
            Напиши функцию `greet(name)`, которая собирает приветствие.

            - Получает: `name` — имя (строка).
            - **Возвращает** (через `return`, а не печатает!) строку вида `Привет, <имя>!`.

            Примеры:
            ```
            greet("Аня")   # → "Привет, Аня!"
            greet("Bob")   # → "Привет, Bob!"
            ```
            Удобнее всего через f-строку: `f"Привет, {name}!"`.
            """),
            """
            def greet(name):
                pass
            """,
            """
            def test_anna():
                assert greet("Аня") == "Привет, Аня!", f'greet("Аня") вернула {greet("Аня")!r}'

            def test_bob():
                assert greet("Bob") == "Привет, Bob!", 'greet("Bob") → "Привет, Bob!"'
            """,
            """
            def greet(name):
                return f"Привет, {name}!"
            """,
            hint="Функция должна именно вернуть строку (`return`), а не напечатать её."),
    ],
    f"{P}-m1-l3": [
        out(f"{P}-m1-l3-x1", "Что выведет программа?", """
            price = 250
            count = 3
            total = price * count
            print(total // 100, total % 100)
            """, hint="750 // 100 и 750 % 100."),
        cod(f"{P}-m1-l3-x2", t("""
            Напиши функцию `split_time(seconds)`, которая раскладывает секунды на минуты и секунды.

            - Получает: `seconds` — целое число секунд.
            - Возвращает: **пару** (кортеж) `(минуты, оставшиеся_секунды)`.

            Примеры:
            ```
            split_time(135)   # → (2, 15)   потому что 135 = 2·60 + 15
            split_time(120)   # → (2, 0)
            split_time(59)    # → (0, 59)
            ```
            Пригодятся `//` (целая часть от деления) и `%` (остаток). Вернуть пару можно так: `return a, b`.
            """),
            """
            def split_time(seconds):
                pass
            """,
            """
            def test_135():
                assert split_time(135) == (2, 15), f"split_time(135) вернула {split_time(135)!r}"

            def test_exact():
                assert split_time(120) == (2, 0), "split_time(120) → (2, 0)"

            def test_small():
                assert split_time(59) == (0, 59), "split_time(59) → (0, 59)"
            """,
            """
            def split_time(seconds):
                return seconds // 60, seconds % 60
            """,
            hint="Целые минуты — `//`, остаток секунд — `%`. Вернуть пару: `return a, b`."),
    ],
    f"{P}-m2-l1": [
        out(f"{P}-m2-l1-x1", "Что выведет программа? Внимание на отступы.", """
            x = 3
            if x > 5:
                print("A")
                print("B")
            print("C")
            """, hint="«A» и «B» внутри if, «C» — снаружи."),
        cod(f"{P}-m2-l1-x2", t("""
            Напиши функцию `ticket_price(age)`, которая считает цену билета в музей.

            - Получает: `age` — возраст посетителя.
            - Возвращает: `0`, если посетителю **меньше 7 лет** (вход бесплатный), иначе `300`.

            Примеры:
            ```
            ticket_price(3)    # → 0
            ticket_price(7)    # → 300   ровно 7 лет — уже платно
            ticket_price(40)   # → 300
            ```
            """),
            """
            def ticket_price(age):
                pass
            """,
            """
            def test_baby():
                assert ticket_price(3) == 0, "ticket_price(3) → 0"

            def test_border():
                assert ticket_price(7) == 300, "Ровно 7 лет — уже платно: 300"

            def test_adult():
                assert ticket_price(40) == 300, "ticket_price(40) → 300"
            """,
            """
            def ticket_price(age):
                if age < 7:
                    return 0
                return 300
            """),
    ],
    f"{P}-m2-l2": [
        out(f"{P}-m2-l2-x1", "Что выведет программа? Пустая строка и ноль считаются «ложью».", """
            print(bool(""))
            print(bool("0"))
            print(bool(0))
            print(bool([]))
            """, hint="`\"0\"` — непустая строка, поэтому истина."),
        cod(f"{P}-m2-l2-x2", t("""
            Напиши функцию `can_login(login, password)`, которая проверяет данные для входа.

            - Получает: `login` и `password` — строки.
            - Возвращает `True`, только если выполнены **оба** условия:
              1. логин не пустая строка;
              2. в пароле **8 символов или больше**.

            Иначе — `False`.

            Примеры:
            ```
            can_login("anna", "12345678")   # → True
            can_login("anna", "123")        # → False   пароль короткий
            can_login("", "supersecret")    # → False   логин пустой
            ```
            """),
            """
            def can_login(login, password):
                pass
            """,
            """
            def test_ok():
                assert can_login("anna", "12345678") is True, "Логин есть, пароль 8 символов — True"

            def test_short_password():
                assert can_login("anna", "123") is False, "Короткий пароль — False"

            def test_empty_login():
                assert can_login("", "supersecret") is False, "Пустой логин — False"
            """,
            """
            def can_login(login, password):
                return login != "" and len(password) >= 8
            """,
            hint="Два условия через `and`."),
    ],
    f"{P}-m2-l3": [
        out(f"{P}-m2-l3-x1", "Что выведет программа?", """
            temp = 0
            if temp < 0:
                print("мороз")
            elif temp == 0:
                print("ноль")
            elif temp < 15:
                print("прохладно")
            else:
                print("тепло")
            """),
        cod(f"{P}-m2-l3-x2", t("""
            Напиши функцию `grade(score)`, которая переводит баллы в оценку-букву.

            - Получает: `score` — число баллов от 0 до 100.
            - Возвращает букву по шкале:

            - 90 и больше → `"A"`
            - от 75 до 89 → `"B"`
            - от 60 до 74 → `"C"`
            - меньше 60 → `"F"`

            Примеры:
            ```
            grade(95)   # → "A"
            grade(90)   # → "A"
            grade(75)   # → "B"
            grade(60)   # → "C"
            grade(59)   # → "F"
            ```
            """),
            """
            def grade(score):
                pass
            """,
            """
            def test_a():
                assert grade(95) == "A" and grade(90) == "A", "90 и выше — A"

            def test_b():
                assert grade(75) == "B" and grade(89) == "B", "75..89 — B"

            def test_c():
                assert grade(60) == "C", "60 — это C"

            def test_f():
                assert grade(59) == "F", "59 — F"
            """,
            """
            def grade(score):
                if score >= 90:
                    return "A"
                elif score >= 75:
                    return "B"
                elif score >= 60:
                    return "C"
                return "F"
            """,
            hint="Проверяй от большего к меньшему: сначала `>= 90`, потом `>= 75`…"),
    ],
    f"{P}-m3-l1": [
        out(f"{P}-m3-l1-x1", "Что выведет программа?", """
            for i in range(1, 4):
                print("*" * i)
            """),
        cod(f"{P}-m3-l1-x2", t("""
            С помощью цикла выведи таблицу умножения на 7 — от 1 до 10.

            Каждая строка в формате `7 x N = R`, где `N` — множитель, `R` — результат. Всего 10 строк:
            ```
            7 x 1 = 7
            7 x 2 = 14
            ...
            7 x 10 = 70
            ```
            Между числами и знаками `x` и `=` — по одному пробелу.
            """),
            "",
            """
            def test_lines():
                lines = OUTPUT.strip().split("\\n")
                assert len(lines) == 10, f"Нужно 10 строк, а напечатано {len(lines)}"

            def test_first_last():
                lines = OUTPUT.strip().split("\\n")
                assert lines[0].strip() == "7 x 1 = 7", f"Первая строка: {lines[0]!r}"
                assert lines[-1].strip() == "7 x 10 = 70", f"Последняя строка: {lines[-1]!r}"
            """,
            """
            for n in range(1, 11):
                print(f"7 x {n} = {7 * n}")
            """,
            hint="f-строка: `f\"7 x {n} = {7 * n}\"`, n от 1 до 10."),
    ],
    f"{P}-m3-l2": [
        out(f"{P}-m3-l2-x1", "Что выведет программа?", """
            best = 0
            for n in [4, 9, 2, 7]:
                if n > best:
                    best = n
            print(best)
            """),
        cod(f"{P}-m3-l2-x2", t("""
            Напиши функцию `count_vowels(text)`, которая считает гласные буквы.

            - Получает: `text` — строка из **строчных** русских букв (и, возможно, пробелов).
            - Возвращает: сколько в строке гласных букв. Гласные: `а е ё и о у ы э ю я`.

            Примеры:
            ```
            count_vowels("молоко")        # → 3
            count_vowels("брр")           # → 0
            count_vowels("я иду домой")   # → 5
            ```
            """),
            """
            def count_vowels(text):
                pass
            """,
            """
            def test_word():
                assert count_vowels("молоко") == 3, 'В "молоко" три гласных'

            def test_none():
                assert count_vowels("брр") == 0, 'В "брр" гласных нет'

            def test_phrase():
                assert count_vowels("я иду домой") == 5, 'В "я иду домой" пять гласных'
            """,
            """
            def count_vowels(text):
                count = 0
                for ch in text:
                    if ch in "аеёиоуыэюя":
                        count += 1
                return count
            """,
            hint="`ch in \"аеёиоуыэюя\"` проверяет, есть ли символ в строке гласных."),
    ],
    f"{P}-m3-l3": [
        out(f"{P}-m3-l3-x1", "Что выведет программа?", """
            n = 10
            steps = 0
            while n != 1:
                if n % 2 == 0:
                    n //= 2
                else:
                    n = 3 * n + 1
                steps += 1
            print(steps)
            """, hint="10 → 5 → 16 → 8 → 4 → 2 → 1. Посчитай стрелки."),
        cod(f"{P}-m3-l3-x2", t("""
            Напиши функцию `first_divisor(n)`, которая находит наименьший делитель числа, больший 1.

            - Получает: `n` — целое число, `n ≥ 2`.
            - Возвращает: самое маленькое число `d > 1`, на которое `n` делится без остатка.

            Примеры:
            ```
            first_divisor(10)   # → 2
            first_divisor(15)   # → 3
            first_divisor(13)   # → 13   у простого числа наименьший делитель — оно само
            ```
            Используй цикл `while`: перебирай `d = 2, 3, 4, …`, пока не найдёшь делитель.
            """),
            """
            def first_divisor(n):
                pass
            """,
            """
            def test_even():
                assert first_divisor(10) == 2, "first_divisor(10) → 2"

            def test_odd():
                assert first_divisor(15) == 3, "first_divisor(15) → 3"

            def test_prime():
                assert first_divisor(13) == 13, "У простого числа наименьший делитель — оно само"
            """,
            """
            def first_divisor(n):
                d = 2
                while n % d != 0:
                    d += 1
                return d
            """,
            hint="Начни с `d = 2` и увеличивай, пока `n % d != 0`."),
    ],
    f"{P}-m4-l1": [
        out(f"{P}-m4-l1-x1", "Что выведет программа? Методы списка меняют его на месте.", """
            items = ["b", "a"]
            items.append("c")
            items.insert(0, "z")
            items.remove("a")
            print(items)
            print("c" in items)
            """),
        cod(f"{P}-m4-l1-x2", t("""
            Напиши функцию `middle(items)`, которая отрезает у списка первый и последний элементы.

            - Получает: `items` — список.
            - Возвращает: новый список — всё, кроме первого и последнего элементов.

            Примеры:
            ```
            middle([1, 2, 3, 4])      # → [2, 3]
            middle(["a", "b", "c"])   # → ["b"]
            middle([1, 2])            # → []
            ```
            Реши одной строкой через срез.
            """),
            """
            def middle(items):
                pass
            """,
            """
            def test_four():
                assert middle([1, 2, 3, 4]) == [2, 3], "middle([1, 2, 3, 4]) → [2, 3]"

            def test_two():
                assert middle([1, 2]) == [], "middle([1, 2]) → []"

            def test_words():
                assert middle(["a", "b", "c"]) == ["b"], 'middle(["a","b","c"]) → ["b"]'
            """,
            """
            def middle(items):
                return items[1:-1]
            """,
            hint="Срез `items[1:-1]` — со второго до предпоследнего."),
    ],
    f"{P}-m4-l2": [
        out(f"{P}-m4-l2-x1", "Что выведет программа? `enumerate` даёт пары (индекс, значение).", """
            for i, name in enumerate(["Аня", "Боря"], start=1):
                print(i, name)
            """),
        cod(f"{P}-m4-l2-x2", t("""
            Напиши функцию `average(nums)`, которая считает среднее арифметическое.

            - Получает: `nums` — непустой список чисел.
            - Возвращает: сумму чисел, делённую на их количество, **округлённую до 2 знаков** после запятой.

            Примеры:
            ```
            average([2, 4, 6])   # → 4.0
            average([1, 2, 2])   # → 1.67   5 / 3 = 1.666… → 1.67
            average([5])         # → 5.0
            ```
            Пригодятся `sum()`, `len()` и `round(x, 2)`.
            """),
            """
            def average(nums):
                pass
            """,
            """
            def test_simple():
                assert average([2, 4, 6]) == 4, "average([2, 4, 6]) → 4"

            def test_round():
                assert average([1, 2, 2]) == 1.67, f"average([1, 2, 2]) → 1.67, а получено {average([1, 2, 2])}"

            def test_single():
                assert average([5]) == 5, "average([5]) → 5"
            """,
            """
            def average(nums):
                return round(sum(nums) / len(nums), 2)
            """,
            hint="`sum(nums) / len(nums)`, затем `round(..., 2)`."),
        cod(f"{P}-m4-l2-x3", t("""
            Напиши функцию `count_words(words)`, которая считает, сколько раз встречается каждое слово.

            - Получает: `words` — список слов.
            - Возвращает: **словарь**, где ключ — слово, а значение — сколько раз оно встретилось.

            Примеры:
            ```
            count_words(["a", "b", "a"])   # → {"a": 2, "b": 1}
            count_words([])                # → {}
            ```
            """),
            """
            def count_words(words):
                pass
            """,
            """
            def test_basic():
                assert count_words(["a", "b", "a"]) == {"a": 2, "b": 1}, f"Получено {count_words(['a', 'b', 'a'])}"

            def test_empty():
                assert count_words([]) == {}, "Для пустого списка — пустой словарь"
            """,
            """
            def count_words(words):
                result = {}
                for w in words:
                    result[w] = result.get(w, 0) + 1
                return result
            """,
            hint="`result.get(w, 0)` вернёт 0, если слова ещё нет в словаре.", xp=20),
    ],
}
