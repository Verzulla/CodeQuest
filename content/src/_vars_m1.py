"""Тема «Переменные и типы данных», модуль 1 «Первые шаги» — задания.
Теория уроков — в _vars_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "var"

m1 = module(f"{P}-m1", "Первые шаги", "🐣", "print, комментарии и ошибки, переменные и функции в заданиях",

lesson(f"{P}-m1-l1", "Первая программа: print",
    out(f"{P}-m1-l1-e1", "Что выведет программа?", """
        print("Hello")
        print("Python")
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа? Обрати внимание на запятые.", """
        print("Мне", 20, "лет")
        print("2024", "09", "27", sep="-")
        """, hint="Через запятую — через пробел, а `sep` заменяет пробел на свой разделитель."),
    cod(f"{P}-m1-l1-e3", t("""
        Выведи на экран фразу `Hello, World!`.

        Текст должен совпасть **символ в символ**: заглавные `H` и `W`, запятая, пробел, восклицательный знак.

        Ожидаемый вывод:
        ```
        Hello, World!
        ```
        """),
        "",
        """
        def test_output():
            assert OUTPUT.strip() == "Hello, World!", f"Ожидалось 'Hello, World!', а напечатано {OUTPUT.strip()!r}"
        """,
        'print("Hello, World!")',
        hint="`print(\"...\")` — текст внутри кавычек."),
    cod(f"{P}-m1-l1-e4", t("""
        Выведи три слова, каждое на отдельной строке.

        Ожидаемый вывод:
        ```
        один
        два
        три
        ```
        """),
        "",
        """
        def test_words():
            assert OUTPUT.split() == ["один", "два", "три"], f"Напечатано: {OUTPUT.split()}"

        def test_lines():
            assert len(OUTPUT.strip().splitlines()) == 3, "Каждое слово — на своей строке"
        """,
        """
        print("один")
        print("два")
        print("три")
        """),
    cod(f"{P}-m1-l1-e5", t("""
        Выведи время в формате `часы:минуты:секунды` **одним вызовом** `print`, передав три числа через запятую и задав разделитель `sep`.

        Числа: `12`, `30`, `45`. Ожидаемый вывод:
        ```
        12:30:45
        ```
        """),
        "",
        """
        import inspect

        def test_output():
            assert OUTPUT.strip() == "12:30:45", f"Напечатано {OUTPUT.strip()!r}"

        def test_one_print():
            src = open("solution.py", encoding="utf-8").read()
            assert src.count("print(") == 1 and "sep" in src, "Нужен один print с параметром sep"
        """,
        'print(12, 30, 45, sep=":")',
        hint="`print(a, b, c, sep=\":\")`"),
    out(f"{P}-m1-l1-e6", "Что выведет программа? Обрати внимание на `end`.", """
        print("A", end="")
        print("B")
        print("C", end="!\\n")
        print("D")
        """, hint="`end` — то, что печатается после значений вместо перехода на новую строку."),
    cod(f"{P}-m1-l1-e7", t("""
        Выведи `Загрузка...готово` **на одной строке**, но **двумя** вызовами `print`:
        первый печатает `Загрузка...`, второй — `готово`.

        Ожидаемый вывод:
        ```
        Загрузка...готово
        ```
        Подсказка: первому `print` нужен параметр `end`, чтобы он не переходил на новую строку.
        """),
        "",
        """
        def test_output():
            assert OUTPUT == "Загрузка...готово\\n", f"Напечатано {OUTPUT!r}"

        def test_two_prints():
            src = open("solution.py", encoding="utf-8").read()
            assert src.count("print(") == 2 and "end" in src, "Нужно два print, у первого — параметр end"
        """,
        """
        print("Загрузка...", end="")
        print("готово")
        """,
        hint='`print("Загрузка...", end="")`'),
    cod(f"{P}-m1-l1-e8", t("""
        Выведи фразу **вместе с кавычками**:
        ```
        Он сказал: "Привет"
        ```
        Двойные кавычки должны напечататься. Подсказка: возьми всю строку в **одинарные** кавычки.
        """),
        "",
        """
        def test_output():
            assert OUTPUT.strip() == 'Он сказал: "Привет"', f"Напечатано {OUTPUT.strip()!r}"
        """,
        """
        print('Он сказал: "Привет"')
        """,
        hint="""`print('... "Привет"')` — снаружи одинарные, внутри двойные.""")),

lesson(f"{P}-errors", "Комментарии и ошибки",
    out(f"{P}-errors-e1", "Что выведет программа? Строки с `#` — комментарии.", """
        # print("A")
        print("B")  # print("C")
        print("D")
        """, hint="Всё после `#` до конца строки Python пропускает."),
    out(f"{P}-errors-e2", "Что выведет программа? `#` внутри кавычек.", """
        print("# это не комментарий")
        print("цена: 100")  # а это комментарий
        """, hint="Внутри строки `#` — обычный символ."),
    out(f"{P}-errors-e3", "Что выведет программа?", """
        x = 5  # x = 10
        # x = 20
        print(x)
        """),
    cod(f"{P}-errors-e4", t("""
        В программе **синтаксическая ошибка** (`SyntaxError`) — она даже не запускается. Найди и исправь её.

        Программа должна вывести:
        ```
        Привет
        ```
        """),
        """
        print("Привет)
        """,
        """
        def test_output():
            assert OUTPUT.strip() == "Привет", f"Напечатано {OUTPUT.strip()!r}"
        """,
        """
        print("Привет")
        """,
        hint="Строка открыта кавычкой, но не закрыта."),
    cod(f"{P}-errors-e5", t("""
        Программа падает с ошибкой `NameError: name 'Привет' is not defined`. Исправь её.

        Программа должна вывести:
        ```
        Привет, мир
        ```
        """),
        """
        print(Привет, мир)
        """,
        """
        def test_output():
            assert OUTPUT.strip() == "Привет, мир", f"Напечатано {OUTPUT.strip()!r}"
        """,
        """
        print("Привет, мир")
        """,
        hint="Без кавычек Python считает слова именами переменных. Текст — в кавычки."),
    cod(f"{P}-errors-e6", t("""
        Программа падает с `IndentationError: unexpected indent` — «неожиданный отступ». Исправь её.

        Программа должна вывести две строки:
        ```
        a
        b
        ```
        """),
        """
        print("a")
            print("b")
        """,
        """
        def test_output():
            assert OUTPUT.split() == ["a", "b"], f"Напечатано {OUTPUT!r}"
        """,
        """
        print("a")
        print("b")
        """,
        hint="Обе строки должны начинаться с самого левого края — без пробелов."),
    cod(f"{P}-errors-e7", t("""
        Программа падает с `TypeError: can only concatenate str (not "int") to str` — нельзя склеить строку с числом.
        Исправь её, **не меняя** строку `age = 25` (возраст должен остаться числом).

        Программа должна вывести:
        ```
        Мне 25 лет
        ```
        """),
        """
        age = 25
        print("Мне " + age + " лет")
        """,
        """
        def test_output():
            assert OUTPUT.strip() == "Мне 25 лет", f"Напечатано {OUTPUT.strip()!r}"

        def test_age_is_number():
            assert age == 25 and isinstance(age, int), "age должна остаться числом 25"
        """,
        """
        age = 25
        print("Мне " + str(age) + " лет")
        """,
        hint='`str(age)` превращает число в строку. Или передай части через запятую: `print("Мне", age, "лет")`.'),
    cod(f"{P}-errors-e8", t("""
        Программа печатает лишнюю отладочную строку `DEBUG`. **Не удаляй** её, а **закомментируй** — поставь `#` в начале строки,
        чтобы Python её пропускал.

        Программа должна вывести:
        ```
        старт
        финиш
        ```
        """),
        """
        print("старт")
        print("DEBUG")
        print("финиш")
        """,
        """
        def test_output():
            assert OUTPUT.split() == ["старт", "финиш"], f"Напечатано {OUTPUT!r}"

        def test_commented():
            src = open("solution.py", encoding="utf-8").read()
            assert "DEBUG" in src and any(line.strip().startswith("#") and "DEBUG" in line for line in src.splitlines()), \\
                "Строка с DEBUG должна остаться в коде, но закомментированной"
        """,
        """
        print("старт")
        # print("DEBUG")
        print("финиш")
        """,
        hint='`# print("DEBUG")`')),

lesson(f"{P}-m1-l2", "Переменные",
    out(f"{P}-m1-l2-e1", "Что выведет программа?", """
        x = 5
        x = 10
        print(x)
        """, hint="Второе присваивание перезаписывает первое."),
    out(f"{P}-m1-l2-e2", "Что выведет программа?", """
        a = 3
        b = a
        a = 7
        print(a, b)
        """, hint="`b = a` копирует текущее значение `a`; дальнейшие изменения `a` на `b` не влияют."),
    cod(f"{P}-m1-l2-e3", t("""
        Создай две переменные:
        - `city` — строка `"Казань"`;
        - `year` — **число** `2024` (без кавычек).

        Печатать ничего не нужно — тесты сами прочитают переменные.
        """),
        "",
        """
        def test_city():
            assert city == "Казань", "city должна быть строкой 'Казань'"

        def test_year():
            assert year == 2024 and isinstance(year, int), "year должна быть числом 2024, без кавычек"
        """,
        """
        city = "Казань"
        year = 2024
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Поменяй местами значения переменных `a` и `b`.

        В заготовке `a = 10`, `b = 20`. Допиши код так, чтобы строка `print(a, b)` вывела:
        ```
        20 10
        ```
        Нельзя просто написать `a = 20` — код должен работать для любых значений.
        """),
        """
        a = 10
        b = 20
        # поменяй a и b местами

        print(a, b)
        """,
        """
        import re

        def test_swapped():
            assert (a, b) == (20, 10), f"Ожидалось a=20, b=10, сейчас a={a}, b={b}"

        def test_no_hardcode():
            src = open("solution.py", encoding="utf-8").read()
            assert not re.search(r"^\\s*a\\s*=\\s*20\\s*$", src, re.M), "Не присваивай числа напрямую — поменяй значения местами"
        """,
        """
        a = 10
        b = 20
        a, b = b, a
        print(a, b)
        """,
        hint="В Python можно так: `a, b = b, a`."),
    cod(f"{P}-m1-l2-e5", t("""
        Счётчик попыток.

        Создай переменную `attempts` со значением `0`, затем **три раза** увеличь её на 1 (используй `+=`) и выведи.

        Ожидаемый вывод:
        ```
        3
        ```
        """),
        "",
        """
        def test_value():
            assert attempts == 3, f"attempts должна быть 3, сейчас {attempts}"

        def test_output():
            assert OUTPUT.strip() == "3", f"Напечатано {OUTPUT.strip()!r}"

        def test_increment():
            src = open("solution.py", encoding="utf-8").read()
            assert src.count("+=") >= 3, "Увеличь переменную три раза через +="
        """,
        """
        attempts = 0
        attempts += 1
        attempts += 1
        attempts += 1
        print(attempts)
        """),
    out(f"{P}-m1-l2-e6", "Что выведет программа? Имя в кавычках и без.", """
        name = "Аня"
        print("name")
        print(name)
        """, hint="В кавычках — просто текст. Без кавычек — значение переменной."),
    out(f"{P}-m1-l2-e7", "Что выведет программа? Регистр букв в именах.", """
        score = 1
        Score = 2
        SCORE = 3
        print(score, Score, SCORE)
        """, hint="Для Python `score`, `Score` и `SCORE` — три разные переменные."),
    cod(f"{P}-m1-l2-e8", t("""
        В программе недопустимые имена переменных — она падает с `SyntaxError`. Переименуй переменные:

        - `2nd_place` → `second_place`;
        - `user-name` → `user_name`.

        Значения оставь прежними: `"Боря"` и `"Аня"`.
        """),
        """
        2nd_place = "Боря"
        user-name = "Аня"
        """,
        """
        def test_names():
            assert second_place == "Боря", "second_place должна быть 'Боря'"
            assert user_name == "Аня", "user_name должна быть 'Аня'"
        """,
        """
        second_place = "Боря"
        user_name = "Аня"
        """,
        hint="Имя не может начинаться с цифры и содержать дефис — только буквы, цифры и `_`.")),

lesson(f"{P}-update", "Изменение переменных",
    out(f"{P}-update-e1", "Что выведет программа? Следи за значением `x` после каждой строки.", """
        x = 10
        x += 5
        x -= 3
        x *= 2
        print(x)
        """, hint="10 → 15 → 12 → 24."),
    out(f"{P}-update-e2", "Что выведет программа? Цепочка присваиваний.", """
        a = b = 0
        a += 1
        print(a, b)
        """, hint="`a = b = 0` кладёт 0 в обе переменные, но дальше они независимы."),
    out(f"{P}-update-e3", "Что выведет программа? Деление в `/=` и `//=`.", """
        n = 7
        n /= 2
        print(n)
        m = 7
        m //= 2
        print(m)
        """, hint="`/` всегда даёт дробное число, `//` — целое."),
    cod(f"{P}-update-e4", t("""
        Баланс счёта.

        1. Создай переменную `balance` со значением `1000`.
        2. Потрать 250 — уменьши `balance` через `-=`.
        3. Получи 100 — увеличь через `+=`.
        4. Удвой сумму через `*=`.
        5. Выведи `balance`.

        Ожидаемый вывод:
        ```
        1700
        ```
        """),
        "",
        """
        def test_value():
            assert balance == 1700, f"balance должна быть 1700, сейчас {balance}"

        def test_ops():
            src = open("solution.py", encoding="utf-8").read()
            assert "-=" in src and "+=" in src and "*=" in src, "Используй -=, += и *="

        def test_output():
            assert OUTPUT.strip() == "1700", f"Напечатано {OUTPUT.strip()!r}"
        """,
        """
        balance = 1000
        balance -= 250
        balance += 100
        balance *= 2
        print(balance)
        """),
    cod(f"{P}-update-e5", t("""
        Сдвиг по кругу. В заготовке `a, b, c = 1, 2, 3`.

        Допиши **одну строку**, после которой `a` получит старое значение `b`, `b` — старое `c`, а `c` — старое `a`.
        Строка `print(a, b, c)` должна вывести:
        ```
        2 3 1
        ```
        Код должен работать для любых значений — не пиши числа напрямую.
        """),
        """
        a, b, c = 1, 2, 3
        # допиши одну строку

        print(a, b, c)
        """,
        """
        def test_values():
            assert (a, b, c) == (2, 3, 1), f"Сейчас a={a}, b={b}, c={c}"

        def test_no_hardcode():
            src = open("solution.py", encoding="utf-8").read()
            assert "= 2, 3, 1" not in src and "=2,3,1" not in src.replace(" ", ""), "Не присваивай числа напрямую"
        """,
        """
        a, b, c = 1, 2, 3
        a, b, c = b, c, a
        print(a, b, c)
        """,
        hint="Как обмен двух переменных, только для трёх: `a, b, c = b, c, a`."),
    cod(f"{P}-update-e6", t("""
        Создай три переменные `x`, `y` и `z`, равные `0`, **одной строкой** — цепочкой присваиваний.
        """),
        "",
        """
        def test_values():
            assert x == 0 and y == 0 and z == 0, "Все три переменные должны быть 0"

        def test_one_line():
            src = open("solution.py", encoding="utf-8").read().replace(" ", "")
            assert "x=y=z=0" in src, "Нужна цепочка: x = y = z = 0"
        """,
        """
        x = y = z = 0
        """),
    cod(f"{P}-update-e7", t("""
        Вклад с процентами.

        1. Создай `deposit = 1000`.
        2. **Три раза** увеличь его на 10% через `*=` (увеличить на 10% — значит умножить на `1.1`).
        3. Выведи результат, округлённый до 2 знаков: `print(round(deposit, 2))`.

        Ожидаемый вывод:
        ```
        1331.0
        ```
        """),
        "",
        """
        def test_output():
            assert OUTPUT.strip() == "1331.0", f"Напечатано {OUTPUT.strip()!r}"

        def test_ops():
            src = open("solution.py", encoding="utf-8").read()
            assert src.count("*=") >= 3, "Увеличь вклад три раза через *="
        """,
        """
        deposit = 1000
        deposit *= 1.1
        deposit *= 1.1
        deposit *= 1.1
        print(round(deposit, 2))
        """,
        hint="`round` страхует от «хвоста» вроде `...0000005`: дробные числа хранятся приближённо."),
    cod(f"{P}-update-e8", t("""
        Сумма покупок.

        Создай `total = 0`, затем через `+=` добавь цены `150`, `99` и `250` и выведи строку `Итого: 499`.

        Ожидаемый вывод:
        ```
        Итого: 499
        ```
        """),
        "",
        """
        def test_total():
            assert total == 499, f"total должна быть 499, сейчас {total}"

        def test_output():
            assert OUTPUT.strip() == "Итого: 499", f"Напечатано {OUTPUT.strip()!r}"

        def test_ops():
            src = open("solution.py", encoding="utf-8").read()
            assert src.count("+=") >= 3, "Добавь каждую цену через +="
        """,
        """
        total = 0
        total += 150
        total += 99
        total += 250
        print("Итого:", total)
        """)),

lesson(f"{P}-func", "Функции в заданиях: def и return",
    out(f"{P}-func-e1", "Что выведет программа?", """
        def double(x):
            return x * 2

        print(double(4))
        print(double(10))
        """),
    out(f"{P}-func-e2", "Что выведет программа? Разница между `print` и `return`.", """
        def say():
            print("внутри")

        result = say()
        print(result)
        """, hint="Функция без `return` возвращает `None`."),
    out(f"{P}-func-e3", "Что выведет программа? Что происходит после `return`.", """
        def f():
            return 1
            print("после return")

        print(f())
        print(f() + f())
        """, hint="`return` сразу завершает функцию — строки после него не выполняются."),
    cod(f"{P}-func-e4", t("""
        Напиши функцию `square(n)`, которая **возвращает** квадрат числа `n` (`n` умножить на `n`).

        Примеры:
        ```
        square(3)    # → 9
        square(-4)   # → 16
        ```
        Печатать ничего не нужно — тесты сами вызовут функцию.
        """),
        """
        def square(n):
            pass
        """,
        """
        def test_values():
            assert square(3) == 9 and square(-4) == 16 and square(0) == 0, "Неверный квадрат"
        """,
        """
        def square(n):
            return n * n
        """,
        hint="`return n * n`"),
    cod(f"{P}-func-e5", t("""
        Напиши функцию `greet(name)`, которая возвращает строку `"Привет, <имя>!"`.

        Примеры:
        ```
        greet("Аня")   # → "Привет, Аня!"
        greet("Bob")   # → "Привет, Bob!"
        ```
        """),
        """
        def greet(name):
            pass
        """,
        """
        def test_values():
            assert greet("Аня") == "Привет, Аня!", f"Получено {greet('Аня')!r}"
            assert greet("Bob") == "Привет, Bob!", f"Получено {greet('Bob')!r}"
        """,
        """
        def greet(name):
            return "Привет, " + name + "!"
        """),
    cod(f"{P}-func-e6", t("""
        Напиши функцию `full_name(first, last)` с **двумя** параметрами: возвращает имя и фамилию через пробел.

        Примеры:
        ```
        full_name("Анна", "Петрова")   # → "Анна Петрова"
        ```
        """),
        """
        def full_name(first, last):
            pass
        """,
        """
        def test_values():
            assert full_name("Анна", "Петрова") == "Анна Петрова", f"Получено {full_name('Анна', 'Петрова')!r}"
            assert full_name("A", "B") == "A B", "Между именем и фамилией — один пробел"
        """,
        """
        def full_name(first, last):
            return first + " " + last
        """),
    cod(f"{P}-func-e7", t("""
        Функция `add(a, b)` должна **возвращать** сумму, но сейчас она её только печатает — и тест получает `None`.
        Исправь функцию.

        Пример:
        ```
        add(2, 3)   # → 5
        ```
        """),
        """
        def add(a, b):
            print(a + b)
        """,
        """
        def test_returns():
            assert add(2, 3) == 5, f"add(2, 3) вернула {add(2, 3)!r} — нужно return, а не print"
        """,
        """
        def add(a, b):
            return a + b
        """,
        hint="Замени `print(...)` на `return ...`."),
    cod(f"{P}-func-e8", t("""
        Напиши функцию `minutes_to_seconds(minutes)`, которая возвращает количество секунд в `minutes` минутах.

        Затем **вызови** её для `5` и **выведи** результат.

        Ожидаемый вывод:
        ```
        300
        ```
        """),
        """
        def minutes_to_seconds(minutes):
            pass
        """,
        """
        def test_function():
            assert minutes_to_seconds(2) == 120 and minutes_to_seconds(0) == 0, "В минуте 60 секунд"

        def test_output():
            assert OUTPUT.strip() == "300", f"Напечатано {OUTPUT.strip()!r} — вызови функцию для 5 и выведи результат"
        """,
        """
        def minutes_to_seconds(minutes):
            return minutes * 60

        print(minutes_to_seconds(5))
        """,
        hint="После функции (без отступа): `print(minutes_to_seconds(5))`.")),
)
