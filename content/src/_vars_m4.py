"""Тема «Переменные и типы данных», модуль 4 «Строки» — задания.
Теория уроков — в _vars_t4.py."""
from ._lib import cod, lesson, module, out, t

P = "var"

m4 = module(f"{P}-m3", "Строки", "🔤", "Склейка, методы строк, split/join, f-строки и форматирование",

lesson(f"{P}-m3-l1", "Строки: склейка, длина, спецсимволы",
    out(f"{P}-m3-l1-e1", "Что выведет программа?", """
        s = "Code" + "Quest"
        print(s)
        print(len(s))
        print("-" * 5)
        """),
    out(f"{P}-m3-l1-e2", "Что выведет программа?", """
        s = "автотест"
        print("тест" in s)
        print("Тест" in s)
        print(len(""))
        """, hint="Проверка `in` чувствительна к регистру."),
    out(f"{P}-m3-l1-e6", "Что выведет программа? Кавычки и спецсимволы.", """
        print('Он сказал: "да"')
        print("It's", 'It\\'s')
        print("a\\tb")
        print(len("a\\nb"), len("a b"))
        """, hint="`\\t` — один символ табуляции, `\\n` — один символ перевода строки."),
    cod(f"{P}-m3-l1-e3", t("""
        Напиши функцию `greet(name)`, которая **возвращает** строку `Привет, <имя>!` — через склейку `+`.

        Примеры:
        ```
        greet("Аня")   # → "Привет, Аня!"
        ```
        """),
        """
        def greet(name):
            pass
        """,
        """
        def test_greet():
            assert greet("Аня") == "Привет, Аня!", f"Получено {greet('Аня')!r}"
            assert greet("Bob") == "Привет, Bob!", "Для Bob — «Привет, Bob!»"
        """,
        """
        def greet(name):
            return "Привет, " + name + "!"
        """),
    cod(f"{P}-m3-l1-e4", t("""
        Напиши функцию `frame(text)`, которая возвращает текст в «рамке» из символов `*` — **три строки**, разделённые `\\n`.

        Ширина рамки = длина текста + 4.

        Пример для `frame("hi")`:
        ```
        ******
        * hi *
        ******
        ```
        То есть результат — строка `"******\\n* hi *\\n******"`.
        """),
        """
        def frame(text):
            pass
        """,
        """
        def test_hi():
            assert frame("hi") == "******\\n* hi *\\n******", f"Получено:\\n{frame('hi')}"

        def test_word():
            lines = frame("Python").split("\\n")
            assert lines == ["**********", "* Python *", "**********"], f"Получено: {lines}"
        """,
        """
        def frame(text):
            border = "*" * (len(text) + 4)
            return border + "\\n* " + text + " *\\n" + border
        """,
        hint="Граница — `\"*\" * (len(text) + 4)`. Строки соедини через `\"\\n\"`.", xp=20),
    cod(f"{P}-m3-l1-e5", t("""
        Напиши функцию `contains_ignore_case(text, word)` — есть ли `word` в `text` **без учёта регистра**.

        Примеры:
        ```
        contains_ignore_case("Ошибка ERROR в логе", "error")   # → True
        contains_ignore_case("всё хорошо", "error")            # → False
        ```
        Приведи обе строки к одному регистру методом `.lower()`.
        """),
        """
        def contains_ignore_case(text, word):
            pass
        """,
        """
        def test_values():
            assert contains_ignore_case("Ошибка ERROR в логе", "error") is True, "ERROR и error — одно и то же"
            assert contains_ignore_case("всё хорошо", "error") is False, "Слова нет — False"
            assert contains_ignore_case("Timeout", "TIME") is True, "Регистр не важен"
        """,
        """
        def contains_ignore_case(text, word):
            return word.lower() in text.lower()
        """),
    cod(f"{P}-m3-l1-e7", t("""
        Напиши функцию `shout(word)`, которая возвращает слово **в верхнем регистре** и с тремя восклицательными знаками.
        Три знака сделай **умножением строки**, а не `"!!!"`.

        Примеры:
        ```
        shout("стоп")   # → "СТОП!!!"
        shout("go")     # → "GO!!!"
        ```
        Верхний регистр — метод `.upper()`.
        """),
        """
        def shout(word):
            pass
        """,
        """
        def test_values():
            assert shout("стоп") == "СТОП!!!" and shout("go") == "GO!!!", f"Получено {shout('стоп')!r}"

        def test_multiply():
            src = open("solution.py", encoding="utf-8").read()
            assert "!!!" not in src and "*" in src, "Три восклицательных знака — через умножение строки"
        """,
        """
        def shout(word):
            return word.upper() + "!" * 3
        """),
    cod(f"{P}-m3-l1-e8", t("""
        Напиши функцию `two_lines(first, second)`, которая возвращает **одну строку** из двух строк текста,
        разделённых символом перевода строки.

        Пример:
        ```
        two_lines("Имя: Аня", "Роль: QA")   # → "Имя: Аня\\nРоль: QA"
        ```
        Если напечатать результат, получится:
        ```
        Имя: Аня
        Роль: QA
        ```
        """),
        """
        def two_lines(first, second):
            pass
        """,
        """
        def test_values():
            assert two_lines("Имя: Аня", "Роль: QA") == "Имя: Аня\\nРоль: QA", f"Получено {two_lines('Имя: Аня', 'Роль: QA')!r}"
            assert two_lines("a", "b").count("\\n") == 1, "Ровно один перевод строки"
        """,
        """
        def two_lines(first, second):
            return first + "\\n" + second
        """,
        hint='`first + "\\n" + second`')),

lesson(f"{P}-m3-l2", "Методы строк: регистр, очистка, замена",
    out(f"{P}-m3-l2-e1", "Что выведет программа?", """
        s = "  Hello, World  "
        print(s.strip())
        print(s.strip().upper())
        print(s.strip().replace("World", "Python"))
        """),
    out(f"{P}-m3-l2-e6", "Что выведет программа? Методы регистра.", """
        print("hello world".title())
        print("PyThOn".lower(), "PyThOn".upper())
        print("привет, мир".capitalize())
        """),
    out(f"{P}-m3-l2-e7", "Что выведет программа? Строки не меняются.", """
        s = "  hi  "
        s.strip()
        print(repr(s))
        s = s.strip()
        print(repr(s))
        """, hint="Метод возвращает новую строку. Если её не сохранить — `s` останется прежней."),
    cod(f"{P}-m3-l2-e3", t("""
        Напиши функцию `normalize_email(email)`, которая приводит email к единому виду: убирает пробелы по краям и переводит в нижний регистр.

        Примеры:
        ```
        normalize_email("  Anna@Mail.RU ")   # → "anna@mail.ru"
        ```
        """),
        """
        def normalize_email(email):
            pass
        """,
        """
        def test_email():
            assert normalize_email("  Anna@Mail.RU ") == "anna@mail.ru", f"Получено {normalize_email('  Anna@Mail.RU ')!r}"
        """,
        """
        def normalize_email(email):
            return email.strip().lower()
        """),
    cod(f"{P}-m3-l2-e8", t("""
        Напиши функцию `clean_phone(phone)`, которая убирает из номера телефона пробелы, дефисы и скобки,
        оставляя только `+` и цифры.

        Примеры:
        ```
        clean_phone("+7 (912) 345-67-89")   # → "+79123456789"
        clean_phone("8-800-555-35-35")      # → "88005553535"
        ```
        Вызови `.replace()` несколько раз подряд — цепочкой.
        """),
        """
        def clean_phone(phone):
            pass
        """,
        """
        def test_values():
            assert clean_phone("+7 (912) 345-67-89") == "+79123456789", f"Получено {clean_phone('+7 (912) 345-67-89')!r}"
            assert clean_phone("8-800-555-35-35") == "88005553535", f"Получено {clean_phone('8-800-555-35-35')!r}"
        """,
        """
        def clean_phone(phone):
            return phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        """),
    cod(f"{P}-m3-l2-e9", t("""
        Напиши функцию `censor(text, word)`, которая заменяет **все** вхождения слова `word` в тексте на `***`.

        Примеры:
        ```
        censor("пароль: qwerty, повтор: qwerty", "qwerty")   # → "пароль: ***, повтор: ***"
        censor("всё чисто", "qwerty")                         # → "всё чисто"
        ```
        """),
        """
        def censor(text, word):
            pass
        """,
        """
        def test_values():
            assert censor("пароль: qwerty, повтор: qwerty", "qwerty") == "пароль: ***, повтор: ***", "Замени все вхождения"
            assert censor("всё чисто", "qwerty") == "всё чисто", "Если слова нет — текст без изменений"
        """,
        """
        def censor(text, word):
            return text.replace(word, "***")
        """),
    cod(f"{P}-m3-l2-e10", t("""
        Напиши функцию `strip_brackets(tag)`, которая убирает квадратные скобки **по краям** строки.

        Примеры:
        ```
        strip_brackets("[ERROR]")    # → "ERROR"
        strip_brackets("[[info]]")   # → "info"
        strip_brackets("a[b]c")      # → "a[b]c"    скобки в середине не трогаем
        ```
        У `strip` можно указать, **какие** символы убирать: `s.strip("[]")`.
        """),
        """
        def strip_brackets(tag):
            pass
        """,
        """
        def test_values():
            got = [strip_brackets("[ERROR]"), strip_brackets("[[info]]"), strip_brackets("a[b]c")]
            assert got == ["ERROR", "info", "a[b]c"], f"Получено {got}"
        """,
        """
        def strip_brackets(tag):
            return tag.strip("[]")
        """),
    cod(f"{P}-m3-l2-e11", t("""
        Напиши функцию `make_slug(title)`, которая делает из заголовка «адрес страницы»: убирает пробелы по краям,
        переводит в нижний регистр и заменяет пробелы на дефисы.

        Примеры:
        ```
        make_slug("  Мой Первый Пост ")   # → "мой-первый-пост"
        make_slug("Python для QA")        # → "python-для-qa"
        ```
        """),
        """
        def make_slug(title):
            pass
        """,
        """
        def test_values():
            assert make_slug("  Мой Первый Пост ") == "мой-первый-пост", f"Получено {make_slug('  Мой Первый Пост ')!r}"
            assert make_slug("Python для QA") == "python-для-qa", f"Получено {make_slug('Python для QA')!r}"
        """,
        """
        def make_slug(title):
            return title.strip().lower().replace(" ", "-")
        """,
        hint="Порядок важен: сначала `strip()`, иначе пробелы по краям тоже станут дефисами.")),

lesson(f"{P}-split", "Методы строк: поиск, split и join",
    out(f"{P}-m3-l2-e2", "Что выведет программа?", """
        line = "ERROR;db;timeout"
        parts = line.split(";")
        print(parts)
        print(" | ".join(parts))
        print(line.startswith("ERROR"), line.count("t"))
        """),
    out(f"{P}-split-e1", "Что выведет программа? Поиск в строке.", """
        name = "report.pdf"
        print(name.endswith(".pdf"), name.startswith("rep"))
        print(name.find("."), name.find("z"))
        print("banana".count("an"))
        """, hint="`find` возвращает позицию (с нуля) или `-1`, если не нашёл."),
    out(f"{P}-split-e2", "Что выведет программа? split с разделителем и без.", """
        print("a,b,,c".split(","))
        print("  много   пробелов  ".split())
        print("k=v=w".split("=", 1))
        """, hint="`split()` без аргумента режет по любым пробелам и выкидывает пустые куски."),
    cod(f"{P}-m3-l2-e4", t("""
        Напиши функцию `initials(full_name)`, которая из полного имени делает инициалы.

        - Получает: строку из 2–3 слов через пробел, например `"иванов иван петрович"`.
        - Возвращает: первые буквы слов **заглавными**, каждая с точкой, без пробелов.

        Примеры:
        ```
        initials("иванов иван петрович")   # → "И.И.П."
        initials("Anna Smith")             # → "A.S."
        ```
        """),
        """
        def initials(full_name):
            pass
        """,
        """
        def test_values():
            assert initials("иванов иван петрович") == "И.И.П.", f"Получено {initials('иванов иван петрович')!r}"
            assert initials("Anna Smith") == "A.S.", f"Получено {initials('Anna Smith')!r}"
        """,
        """
        def initials(full_name):
            return "".join(word[0].upper() + "." for word in full_name.split())
        """,
        hint="`split()` разобьёт на слова, `word[0]` — первая буква.", xp=20),
    cod(f"{P}-m3-l2-e5", t("""
        Напиши функцию `log_level(line)`, которая определяет уровень строки лога.

        - Строка лога начинается с уровня в квадратных скобках: `"[ERROR] нет связи"`, `"[info] старт"`.
        - Возвращает: уровень **заглавными буквами** без скобок, например `"ERROR"`.
        - Если строка не начинается с `[` — вернуть `"UNKNOWN"`.

        Примеры:
        ```
        log_level("[ERROR] нет связи")   # → "ERROR"
        log_level("[info] старт")        # → "INFO"
        log_level("просто текст")        # → "UNKNOWN"
        ```
        Пригодятся `startswith`, `find("]")` и срез.
        """),
        """
        def log_level(line):
            pass
        """,
        """
        def test_values():
            got = [log_level(s) for s in ("[ERROR] нет связи", "[info] старт", "просто текст", "[Warn]x")]
            assert got == ["ERROR", "INFO", "UNKNOWN", "WARN"], f"Получено {got}"
        """,
        """
        def log_level(line):
            if not line.startswith("["):
                return "UNKNOWN"
            end = line.find("]")
            return line[1:end].upper()
        """,
        hint="`line[1:end]` — текст между `[` и `]`, где `end = line.find(\"]\")`.", xp=20),
    cod(f"{P}-split-e3", t("""
        Напиши функцию `is_image(filename)` — является ли файл картинкой: имя заканчивается на `.png` или `.jpg`
        **без учёта регистра**.

        Примеры:
        ```
        is_image("cat.png")     # → True
        is_image("PHOTO.JPG")   # → True
        is_image("notes.txt")   # → False
        ```
        `endswith` умеет проверять несколько окончаний сразу: `s.endswith((".png", ".jpg"))` — обрати внимание на двойные скобки.
        """),
        """
        def is_image(filename):
            pass
        """,
        """
        def test_values():
            got = [is_image("cat.png"), is_image("PHOTO.JPG"), is_image("notes.txt"), is_image("png")]
            assert got == [True, True, False, False], f"Получено {got}"
        """,
        """
        def is_image(filename):
            return filename.lower().endswith((".png", ".jpg"))
        """),
    cod(f"{P}-split-e4", t("""
        Напиши функцию `words_count(text)` — сколько слов в тексте. Слова разделены одним или несколькими пробелами,
        по краям тоже могут быть пробелы.

        Примеры:
        ```
        words_count("раз два три")        # → 3
        words_count("  много   пробелов ") # → 2
        words_count("")                    # → 0
        ```
        `split()` без аргумента + `len()`.
        """),
        """
        def words_count(text):
            pass
        """,
        """
        def test_values():
            got = [words_count("раз два три"), words_count("  много   пробелов "), words_count("")]
            assert got == [3, 2, 0], f"Получено {got}"
        """,
        """
        def words_count(text):
            return len(text.split())
        """),
    cod(f"{P}-split-e5", t("""
        Напиши функцию `csv_line(values)`, которая получает список строк и возвращает их одной строкой через запятую.

        Примеры:
        ```
        csv_line(["Аня", "QA", "Казань"])   # → "Аня,QA,Казань"
        csv_line(["один"])                  # → "один"
        ```
        """),
        """
        def csv_line(values):
            pass
        """,
        """
        def test_values():
            assert csv_line(["Аня", "QA", "Казань"]) == "Аня,QA,Казань", f"Получено {csv_line(['Аня', 'QA', 'Казань'])!r}"
            assert csv_line(["один"]) == "один" and csv_line([]) == "", "Один элемент — без запятых, пустой список — пустая строка"
        """,
        """
        def csv_line(values):
            return ",".join(values)
        """,
        hint='`",".join(values)` — метод вызывается у разделителя.')),

lesson(f"{P}-m3-l3", "f-строки: подстановка значений",
    out(f"{P}-m3-l3-e1", "Что выведет программа?", """
        name = "Аня"
        solved = 3
        print(f"{name} решила {solved} задачи и получила {solved * 10} XP")
        """),
    out(f"{P}-m3-l3-e6", "Что выведет программа? Выражения в фигурных скобках.", """
        x = 5
        print(f"{x} + {x} = {x + x}")
        print(f"{{x}} = {x}")
        print("{x}")
        """, hint="Двойные фигурные скобки печатают одну скобку. Без `f` подстановки нет."),
    out(f"{P}-m3-l3-e7", "Что выведет программа? Методы и функции внутри f-строки.", """
        name = "аня"
        print(f"{name.upper()}!")
        print(f"{len(name)} буквы")
        print(f"{name=}")
        """, hint="`{name=}` печатает и имя переменной, и её значение."),
    cod(f"{P}-m3-l3-e4", t("""
        Напиши функцию `progress(done, total)`, которая возвращает строку прогресса вида `"3/10 (30%)"`.

        - Процент — целый, без дробной части.
        - Если `total` равен 0 — процент считать 0.

        Примеры:
        ```
        progress(3, 10)   # → "3/10 (30%)"
        progress(1, 3)    # → "1/3 (33%)"
        progress(0, 0)    # → "0/0 (0%)"
        ```
        """),
        """
        def progress(done, total):
            pass
        """,
        """
        def test_values():
            got = [progress(3, 10), progress(1, 3), progress(0, 0), progress(5, 5)]
            assert got == ["3/10 (30%)", "1/3 (33%)", "0/0 (0%)", "5/5 (100%)"], f"Получено {got}"
        """,
        """
        def progress(done, total):
            pct = done * 100 // total if total else 0
            return f"{done}/{total} ({pct}%)"
        """, xp=20),
    cod(f"{P}-m3-l3-e8", t("""
        Напиши функцию `order_summary(item, qty, price)`, которая возвращает строку заказа через f-строку:
        `"<qty> × <item> = <qty * price> руб."`.

        Примеры:
        ```
        order_summary("кофе", 2, 150)   # → "2 × кофе = 300 руб."
        order_summary("чай", 1, 90)     # → "1 × чай = 90 руб."
        ```
        Знак умножения `×` можно скопировать отсюда.
        """),
        """
        def order_summary(item, qty, price):
            pass
        """,
        """
        def test_values():
            assert order_summary("кофе", 2, 150) == "2 × кофе = 300 руб.", f"Получено {order_summary('кофе', 2, 150)!r}"
            assert order_summary("чай", 1, 90) == "1 × чай = 90 руб.", f"Получено {order_summary('чай', 1, 90)!r}"
        """,
        """
        def order_summary(item, qty, price):
            return f"{qty} × {item} = {qty * price} руб."
        """),
    cod(f"{P}-m3-l3-e9", t("""
        Напиши функцию `user_card(name, age)`, которая возвращает строку `"<name> (<age> лет)"`.
        Используй f-строку — без `str()` и `+`.

        Примеры:
        ```
        user_card("Аня", 25)   # → "Аня (25 лет)"
        ```
        """),
        """
        def user_card(name, age):
            pass
        """,
        """
        def test_values():
            assert user_card("Аня", 25) == "Аня (25 лет)", f"Получено {user_card('Аня', 25)!r}"

        def test_fstring():
            src = open("solution.py", encoding="utf-8").read()
            assert 'f"' in src or "f'" in src, "Используй f-строку"
        """,
        """
        def user_card(name, age):
            return f"{name} ({age} лет)"
        """),
    cod(f"{P}-m3-l3-e10", t("""
        Напиши функцию `greeting(name, hour)`, которая возвращает `"Добрый день, <name>! Сейчас <hour>:00"`.

        Пример:
        ```
        greeting("Аня", 14)   # → "Добрый день, Аня! Сейчас 14:00"
        ```
        """),
        """
        def greeting(name, hour):
            pass
        """,
        """
        def test_values():
            assert greeting("Аня", 14) == "Добрый день, Аня! Сейчас 14:00", f"Получено {greeting('Аня', 14)!r}"
        """,
        """
        def greeting(name, hour):
            return f"Добрый день, {name}! Сейчас {hour}:00"
        """),
    cod(f"{P}-m3-l3-e11", t("""
        Напиши функцию `debug_value(x)`, которая возвращает строку вида `"x=<значение>"` — используй отладочную запись `{x=}`.

        Примеры:
        ```
        debug_value(5)       # → "x=5"
        debug_value("hi")    # → "x='hi'"     строки показываются в кавычках
        ```
        """),
        """
        def debug_value(x):
            pass
        """,
        """
        def test_values():
            assert debug_value(5) == "x=5", f"Получено {debug_value(5)!r}"
            assert debug_value("hi") == "x='hi'", f"Получено {debug_value('hi')!r}"
        """,
        """
        def debug_value(x):
            return f"{x=}"
        """,
        hint='`return f"{x=}"`')),

lesson(f"{P}-format", "Форматирование чисел и выравнивание",
    out(f"{P}-m3-l3-e2", "Что выведет программа? Форматирование чисел.", """
        pi = 3.14159
        print(f"{pi:.2f}")
        print(f"{0.756:.0%}")
        print(f"{1234567:,}")
        """),
    out(f"{P}-format-e1", "Что выведет программа? Ширина и выравнивание.", """
        print(f"[{'ok':^6}]")
        print(f"[{7:03}]")
        print(f"[{3.14159:8.3f}]")
        print(f"[{'ab':*<5}]")
        """, hint="`^` — по центру, `03` — ширина 3 с нулями слева, `*<5` — влево, пустое место заполнить `*`."),
    out(f"{P}-format-e2", "Что выведет программа? Комбинации форматов.", """
        print(f"{1234567.891:,.1f}")
        print(f"{0.5:.1%}")
        print(f"{42:_>5}")
        print(f"{-3.7:.0f}")
        """),
    cod(f"{P}-m3-l3-e3", t("""
        Напиши функцию `price_tag(name, price)`, которая возвращает ценник в формате `"<название>: <цена> руб."`, где цена всегда **с двумя знаками** после точки.

        Примеры:
        ```
        price_tag("Чай", 99)       # → "Чай: 99.00 руб."
        price_tag("Кофе", 249.5)   # → "Кофе: 249.50 руб."
        ```
        Формат с двумя знаками: `{price:.2f}`.
        """),
        """
        def price_tag(name, price):
            pass
        """,
        """
        def test_values():
            assert price_tag("Чай", 99) == "Чай: 99.00 руб.", f"Получено {price_tag('Чай', 99)!r}"
            assert price_tag("Кофе", 249.5) == "Кофе: 249.50 руб.", f"Получено {price_tag('Кофе', 249.5)!r}"
        """,
        """
        def price_tag(name, price):
            return f"{name}: {price:.2f} руб."
        """),
    cod(f"{P}-m3-l3-e5", t("""
        Напиши функцию `table_row(name, passed, failed)`, которая возвращает строку таблицы отчёта:

        - имя теста **выровнено влево** на ширину 12 символов;
        - числа `passed` и `failed` **выровнены вправо** на ширину 4 символа каждое;
        - между колонками по одному пробелу.

        Пример:
        ```
        table_row("login", 10, 2)
        # → "login          10    2"
        #    ^^^^^^^^^^^^ 12 символов, затем пробел, "  10", пробел, "   2"
        ```
        Форматы: `{name:<12}` и `{passed:>4}`.
        """),
        """
        def table_row(name, passed, failed):
            pass
        """,
        """
        def test_row():
            assert table_row("login", 10, 2) == "login          10    2", f"Получено {table_row('login', 10, 2)!r}"
            assert len(table_row("search", 100, 0)) == 22, "Ширина строки: 12 + 1 + 4 + 1 + 4 = 22"
        """,
        """
        def table_row(name, passed, failed):
            return f"{name:<12} {passed:>4} {failed:>4}"
        """),
    cod(f"{P}-format-e3", t("""
        Напиши функцию `money(x)`, которая форматирует сумму: разделитель тысяч — запятая, всегда два знака после точки,
        в конце пробел и `₽`.

        Примеры:
        ```
        money(1234.5)    # → "1,234.50 ₽"
        money(99)        # → "99.00 ₽"
        money(1000000)   # → "1,000,000.00 ₽"
        ```
        Формат `{x:,.2f}`.
        """),
        """
        def money(x):
            pass
        """,
        """
        def test_values():
            got = [money(1234.5), money(99), money(1000000)]
            assert got == ["1,234.50 ₽", "99.00 ₽", "1,000,000.00 ₽"], f"Получено {got}"
        """,
        """
        def money(x):
            return f"{x:,.2f} ₽"
        """),
    cod(f"{P}-format-e4", t("""
        Напиши функцию `ticket(n)`, которая возвращает номер билета: знак `№` и число, дополненное **нулями слева** до 5 цифр.

        Примеры:
        ```
        ticket(42)      # → "№00042"
        ticket(12345)   # → "№12345"
        ```
        """),
        """
        def ticket(n):
            pass
        """,
        """
        def test_values():
            got = [ticket(42), ticket(12345), ticket(7)]
            assert got == ["№00042", "№12345", "№00007"], f"Получено {got}"
        """,
        """
        def ticket(n):
            return f"№{n:05}"
        """,
        hint="`{n:05}` — ширина 5, пустые места заполняются нулями."),
    cod(f"{P}-format-e5", t("""
        Напиши функцию `bar_label(name, share)`, которая возвращает подпись для графика:
        имя **влево** на ширину 10 символов, затем доля **в процентах без знаков после точки** **вправо** на ширину 5.

        Примеры:
        ```
        bar_label("pass", 0.75)   # → "pass        75%"
        bar_label("fail", 0.1)    # → "fail        10%"
        ```
        То есть `"pass"` + 6 пробелов (всего 10 символов) + `"  75%"` (всего 5 символов).
        """),
        """
        def bar_label(name, share):
            pass
        """,
        """
        def test_values():
            assert bar_label("pass", 0.75) == "pass        75%", f"Получено {bar_label('pass', 0.75)!r}"
            assert bar_label("fail", 0.1) == "fail        10%", f"Получено {bar_label('fail', 0.1)!r}"
            assert len(bar_label("x", 1)) == 15, "Ширина: 10 + 5"
        """,
        """
        def bar_label(name, share):
            return f"{name:<10}{share:>5.0%}"
        """,
        hint="`{name:<10}` и `{share:>5.0%}`.", xp=20)),
)
