"""Тема «Файлы», модуль 1 «Чтение и запись» — задания. Теория — в _fil_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "fil"

m1 = module(f"{P}-m1", "Чтение и запись", "📝", "open и with, режимы, чтение целиком и по строкам, запись и дозапись, кодировки и байты",

lesson(f"{P}-open", "Открыть, записать, прочитать",
    out(f"{P}-open-e1", "Что выведет программа?", """
        f = open("hello.txt", "w", encoding="utf-8")
        f.write("Привет, файл!")
        f.close()

        f = open("hello.txt", encoding="utf-8")
        text = f.read()
        f.close()
        print(text, len(text))
        """, hint="Режим 'w' — запись, без режима — чтение."),
    out(f"{P}-open-e2", "Что выведет программа? with.", """
        with open("notes.txt", "w", encoding="utf-8") as f:
            f.write("первая строка\\n")
            f.write("вторая строка\\n")
        print(f.closed)

        with open("notes.txt", encoding="utf-8") as f:
            print(repr(f.read()))
        """, hint="with сам закрывает файл, даже при ошибке."),
    out(f"{P}-open-e3", "Что выведет программа? 'w' стирает файл.", """
        with open("log.txt", "w", encoding="utf-8") as f:
            f.write("старое")
        with open("log.txt", "w", encoding="utf-8") as f:
            f.write("новое")
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write("+ещё")
        with open("log.txt", encoding="utf-8") as f:
            print(f.read())
        """, hint="'w' очищает файл при открытии, 'a' дописывает в конец."),
    cod(f"{P}-open-e4", t("""
        Напиши функцию `save_text(path, text)` — записать строку в файл (перезаписать, если он есть). Используй `with` и `encoding="utf-8"`.
        """),
        """
        def save_text(path, text):
            pass
        """,
        """
        def test_values():
            save_text("t1.txt", "первый")
            save_text("t1.txt", "Привет")
            with open("t1.txt", encoding="utf-8") as f:
                assert f.read() == "Привет", "Файл должен быть перезаписан"
        """,
        """
        def save_text(path, text):
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        """),
    cod(f"{P}-open-e5", t("""
        Напиши функцию `load_text(path)` — прочитать и вернуть всё содержимое файла.
        """),
        """
        def load_text(path):
            pass
        """,
        """
        def test_values():
            with open("t2.txt", "w", encoding="utf-8") as f:
                f.write("строка 1\\nстрока 2")
            assert load_text("t2.txt") == "строка 1\\nстрока 2", "Неверное содержимое"
        """,
        """
        def load_text(path):
            with open(path, encoding="utf-8") as f:
                return f.read()
        """),
    cod(f"{P}-open-e6", t("""
        Напиши функцию `append_line(path, line)` — дописать строку **в конец** файла и добавить после неё перевод строки `\\n`. Если файла нет — он создаётся.
        """),
        """
        def append_line(path, line):
            pass
        """,
        """
        import os

        def test_values():
            if os.path.exists("t3.txt"):
                os.remove("t3.txt")
            append_line("t3.txt", "первая")
            append_line("t3.txt", "вторая")
            with open("t3.txt", encoding="utf-8") as f:
                assert f.read() == "первая\\nвторая\\n", "Неверное содержимое"
        """,
        """
        def append_line(path, line):
            with open(path, "a", encoding="utf-8") as f:
                f.write(line + "\\n")
        """),
    cod(f"{P}-open-e7", t("""
        Напиши функцию `copy_file(src, dst)` — скопировать содержимое текстового файла `src` в `dst`. Вернуть количество скопированных символов.
        """),
        """
        def copy_file(src, dst):
            pass
        """,
        """
        def test_values():
            with open("src.txt", "w", encoding="utf-8") as f:
                f.write("данные\\nещё")
            assert copy_file("src.txt", "dst.txt") == 10, "Количество символов"
            with open("dst.txt", encoding="utf-8") as f:
                assert f.read() == "данные\\nещё", "Содержимое копии"
        """,
        """
        def copy_file(src, dst):
            with open(src, encoding="utf-8") as f:
                text = f.read()
            with open(dst, "w", encoding="utf-8") as f:
                return f.write(text)
        """, hint="f.write() возвращает количество записанных символов."),
    cod(f"{P}-open-e8", t("""
        Напиши функцию `counter_file(path)` — «счётчик запусков»: прочитать число из файла, увеличить на 1, записать обратно и вернуть новое значение. Если файла нет — считать, что там 0.
        """),
        """
        def counter_file(path):
            pass
        """,
        """
        import os

        def test_values():
            if os.path.exists("count.txt"):
                os.remove("count.txt")
            assert [counter_file("count.txt") for _ in range(3)] == [1, 2, 3], "Счётчик"
            with open("count.txt", encoding="utf-8") as f:
                assert f.read().strip() == "3", "В файле должно быть 3"
        """,
        """
        def counter_file(path):
            try:
                with open(path, encoding="utf-8") as f:
                    value = int(f.read())
            except FileNotFoundError:
                value = 0
            value += 1
            with open(path, "w", encoding="utf-8") as f:
                f.write(str(value))
            return value
        """, xp=20),
),

lesson(f"{P}-read", "Чтение по строкам",
    out(f"{P}-read-e1", "Что выведет программа? Перебор строк.", """
        with open("list.txt", "w", encoding="utf-8") as f:
            f.write("яблоко\\nгруша\\nслива\\n")

        with open("list.txt", encoding="utf-8") as f:
            for line in f:
                print(repr(line))
        """, hint="Каждая строка приходит вместе с \\n в конце."),
    out(f"{P}-read-e2", "Что выведет программа? readline, readlines, splitlines.", """
        with open("list.txt", "w", encoding="utf-8") as f:
            f.write("a\\nb\\nc\\n")

        with open("list.txt", encoding="utf-8") as f:
            print(repr(f.readline()))
            print(f.readlines())
            print(repr(f.read()))

        with open("list.txt", encoding="utf-8") as f:
            print(f.read().splitlines())
        """, hint="Файл читается «курсором»: прочитанное второй раз не выдаётся."),
    out(f"{P}-read-e3", "Что выведет программа? Пустые строки и strip.", """
        with open("data.txt", "w", encoding="utf-8") as f:
            f.write("  10 \\n\\n20\\n   \\n30")

        with open("data.txt", encoding="utf-8") as f:
            numbers = [int(line) for line in f if line.strip()]
        print(numbers, sum(numbers))
        """, hint="int() сам игнорирует пробелы и \\n вокруг числа."),
    cod(f"{P}-read-e4", t("""
        Напиши функцию `read_lines(path)` — список строк файла **без** символов перевода строки.
        """),
        """
        def read_lines(path):
            pass
        """,
        """
        def test_values():
            with open("r1.txt", "w", encoding="utf-8") as f:
                f.write("один\\nдва\\nтри\\n")
            assert read_lines("r1.txt") == ["один", "два", "три"], read_lines("r1.txt")
            with open("r2.txt", "w", encoding="utf-8") as f:
                f.write("")
            assert read_lines("r2.txt") == [], "Пустой файл"
        """,
        """
        def read_lines(path):
            with open(path, encoding="utf-8") as f:
                return f.read().splitlines()
        """),
    cod(f"{P}-read-e5", t("""
        Напиши функцию `count_lines(path)` — количество **непустых** строк (строка из одних пробелов считается пустой). Читай файл построчно, не загружая целиком.
        """),
        """
        def count_lines(path):
            pass
        """,
        """
        def test_values():
            with open("r3.txt", "w", encoding="utf-8") as f:
                f.write("a\\n\\n  \\nb\\nc")
            assert count_lines("r3.txt") == 3, count_lines("r3.txt")
        """,
        """
        def count_lines(path):
            count = 0
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        count += 1
            return count
        """),
    cod(f"{P}-read-e6", t("""
        Напиши функцию `first_line(path)` — первая строка файла без `\\n`; для пустого файла — пустая строка. Не читай весь файл.
        """),
        """
        def first_line(path):
            pass
        """,
        """
        def test_values():
            with open("r4.txt", "w", encoding="utf-8") as f:
                f.write("заголовок\\nданные\\n")
            with open("r5.txt", "w", encoding="utf-8") as f:
                pass
            assert first_line("r4.txt") == "заголовок" and first_line("r5.txt") == "", "Неверный результат"
        """,
        """
        def first_line(path):
            with open(path, encoding="utf-8") as f:
                return f.readline().rstrip("\\n")
        """),
    cod(f"{P}-read-e7", t("""
        Напиши функцию `grep(path, word)` — список кортежей `(номер_строки, строка)` для строк, содержащих `word`. Нумерация с 1, строки без `\\n`.
        """),
        """
        def grep(path, word):
            pass
        """,
        """
        def test_values():
            with open("r6.txt", "w", encoding="utf-8") as f:
                f.write("INFO старт\\nERROR база\\nINFO ок\\nERROR сеть\\n")
            assert grep("r6.txt", "ERROR") == [(2, "ERROR база"), (4, "ERROR сеть")] and grep("r6.txt", "WARN") == [], grep("r6.txt", "ERROR")
        """,
        """
        def grep(path, word):
            result = []
            with open(path, encoding="utf-8") as f:
                for number, line in enumerate(f, start=1):
                    line = line.rstrip("\\n")
                    if word in line:
                        result.append((number, line))
            return result
        """),
    cod(f"{P}-read-e8", t("""
        Напиши функцию `word_stats(path)` — словарь `{"lines": ..., "words": ..., "chars": ...}` как у утилиты `wc`: строки считаются по символам `\\n`, слова — через `split()`, символы — все, включая `\\n`.
        """),
        """
        def word_stats(path):
            pass
        """,
        """
        def test_values():
            with open("r7.txt", "w", encoding="utf-8") as f:
                f.write("раз два\\nтри\\n\\nчетыре пять шесть\\n")
            assert word_stats("r7.txt") == {"lines": 4, "words": 6, "chars": 31}, word_stats("r7.txt")
        """,
        """
        def word_stats(path):
            with open(path, encoding="utf-8") as f:
                text = f.read()
            return {"lines": text.count("\\n"), "words": len(text.split()), "chars": len(text)}
        """, xp=20),
),

lesson(f"{P}-write", "Запись: write, print и режимы",
    out(f"{P}-write-e1", "Что выведет программа? write не добавляет \\n.", """
        with open("w.txt", "w", encoding="utf-8") as f:
            f.write("a")
            f.write("b")
            f.writelines(["c", "d\\n", "e"])
            n = f.write("\\nконец")
        print(n)
        with open("w.txt", encoding="utf-8") as f:
            print(f.read().splitlines())
        """),
    out(f"{P}-write-e2", "Что выведет программа? print в файл.", """
        with open("report.txt", "w", encoding="utf-8") as f:
            print("Отчёт", file=f)
            print("пройдено:", 5, file=f)
            print("упало:", 1, sep=" ", end="!\\n", file=f)
        with open("report.txt", encoding="utf-8") as f:
            print(f.read(), end="")
        """, hint="print(..., file=f) пишет в файл, добавляя пробелы и \\n как обычно."),
    out(f"{P}-write-e3", "Что выведет программа? Режим 'x'.", """
        import os

        if os.path.exists("once.txt"):
            os.remove("once.txt")
        with open("once.txt", "x", encoding="utf-8") as f:
            f.write("создан")
        try:
            open("once.txt", "x", encoding="utf-8")
        except FileExistsError:
            print("файл уже есть")
        """, hint="'x' — создать только новый файл, существующий не трогать."),
    cod(f"{P}-write-e4", t("""
        Напиши функцию `write_lines(path, lines)` — записать список строк в файл, каждую на своей строке (после последней тоже `\\n`).
        """),
        """
        def write_lines(path, lines):
            pass
        """,
        """
        def test_values():
            write_lines("w1.txt", ["a", "b", "c"])
            with open("w1.txt", encoding="utf-8") as f:
                assert f.read() == "a\\nb\\nc\\n", "Неверное содержимое"
            write_lines("w2.txt", [])
            with open("w2.txt", encoding="utf-8") as f:
                assert f.read() == "", "Пустой список — пустой файл"
        """,
        """
        def write_lines(path, lines):
            with open(path, "w", encoding="utf-8") as f:
                for line in lines:
                    f.write(line + "\\n")
        """),
    cod(f"{P}-write-e5", t("""
        Напиши функцию `save_table(path, rows)` — `rows` — список кортежей. Записать каждую строку таблицы через `print(..., sep="\\t", file=f)`: значения разделены табуляцией.
        """),
        """
        def save_table(path, rows):
            pass
        """,
        """
        def test_values():
            save_table("tab.txt", [("имя", "балл"), ("Аня", 90), ("Боря", 85)])
            with open("tab.txt", encoding="utf-8") as f:
                assert f.read() == "имя\\tбалл\\nАня\\t90\\nБоря\\t85\\n", "Неверное содержимое"
        """,
        """
        def save_table(path, rows):
            with open(path, "w", encoding="utf-8") as f:
                for row in rows:
                    print(*row, sep="\\t", file=f)
        """),
    cod(f"{P}-write-e6", t("""
        Напиши функцию `create_once(path, text)` — создать файл с текстом, только если его ещё нет (режим `"x"`). Вернуть `True`, если создан, и `False`, если файл уже существовал (его содержимое не менять).
        """),
        """
        def create_once(path, text):
            pass
        """,
        """
        import os

        def test_values():
            if os.path.exists("w3.txt"):
                os.remove("w3.txt")
            assert create_once("w3.txt", "первый") is True and create_once("w3.txt", "второй") is False, "Результаты"
            with open("w3.txt", encoding="utf-8") as f:
                assert f.read() == "первый", "Содержимое не должно меняться"
        """,
        """
        def create_once(path, text):
            try:
                with open(path, "x", encoding="utf-8") as f:
                    f.write(text)
            except FileExistsError:
                return False
            return True
        """),
    cod(f"{P}-write-e7", t("""
        Напиши функцию `log_results(path, results)` — `results` — словарь «имя теста → True/False». **Дописать** в файл строки вида `PASS имя` / `FAIL имя`, затем строку `итого: N/M` (прошло/всего).
        """),
        """
        def log_results(path, results):
            pass
        """,
        """
        import os

        def test_values():
            if os.path.exists("res.log"):
                os.remove("res.log")
            log_results("res.log", {"login": True, "cart": False})
            log_results("res.log", {"api": True})
            with open("res.log", encoding="utf-8") as f:
                assert f.read() == "PASS login\\nFAIL cart\\nитого: 1/2\\nPASS api\\nитого: 1/1\\n", "Неверное содержимое"
        """,
        """
        def log_results(path, results):
            with open(path, "a", encoding="utf-8") as f:
                for name, ok in results.items():
                    print("PASS" if ok else "FAIL", name, file=f)
                print(f"итого: {sum(results.values())}/{len(results)}", file=f)
        """),
    cod(f"{P}-write-e8", t("""
        Напиши функцию `replace_in_file(path, old, new)` — заменить в файле все вхождения `old` на `new` и вернуть количество замен.
        """),
        """
        def replace_in_file(path, old, new):
            pass
        """,
        """
        def test_values():
            with open("w4.txt", "w", encoding="utf-8") as f:
                f.write("host=dev\\nurl=http://dev/api\\n")
            assert replace_in_file("w4.txt", "dev", "prod") == 2, "Количество замен"
            with open("w4.txt", encoding="utf-8") as f:
                assert f.read() == "host=prod\\nurl=http://prod/api\\n", "Содержимое"
            assert replace_in_file("w4.txt", "xxx", "y") == 0, "Нет вхождений"
        """,
        """
        def replace_in_file(path, old, new):
            with open(path, encoding="utf-8") as f:
                text = f.read()
            count = text.count(old)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text.replace(old, new))
            return count
        """, xp=20),
),

lesson(f"{P}-encoding", "Кодировки и двоичные файлы",
    out(f"{P}-encoding-e1", "Что выведет программа? Символы и байты.", """
        text = "Код"
        data = text.encode("utf-8")
        print(len(text), len(data))
        print(data)
        print(data.decode("utf-8"))
        print(len("Code".encode("utf-8")))
        """, hint="Русская буква в UTF-8 занимает 2 байта, латинская — 1."),
    out(f"{P}-encoding-e2", "Что выведет программа? Не та кодировка.", """
        with open("ru.txt", "w", encoding="cp1251") as f:
            f.write("Привет")

        try:
            with open("ru.txt", encoding="utf-8") as f:
                f.read()
        except UnicodeDecodeError:
            print("ошибка декодирования")

        with open("ru.txt", encoding="cp1251") as f:
            print(f.read())
        with open("ru.txt", encoding="utf-8", errors="replace") as f:
            print(f.read().count("\\ufffd"))
        """, hint="cp1251 — старая кодировка Windows."),
    out(f"{P}-encoding-e3", "Что выведет программа? Двоичный режим.", """
        with open("data.bin", "wb") as f:
            f.write(bytes([0, 1, 2, 255]))
            f.write(b"OK")

        with open("data.bin", "rb") as f:
            content = f.read()
        print(content, len(content))
        print(content[3], content[-2:])
        print(type(content).__name__)
        """, hint="В режиме 'b' читаются и пишутся байты, а не строки."),
    cod(f"{P}-encoding-e4", t("""
        Напиши функцию `byte_size(text)` — сколько байт займёт строка в UTF-8.
        """),
        """
        def byte_size(text):
            pass
        """,
        """
        def test_values():
            assert byte_size("abc") == 3 and byte_size("абв") == 6 and byte_size("") == 0 and byte_size("😀") == 4, "Неверный размер"
        """,
        """
        def byte_size(text):
            return len(text.encode("utf-8"))
        """),
    cod(f"{P}-encoding-e5", t("""
        Напиши функцию `convert_encoding(src, dst, from_enc, to_enc)` — прочитать текстовый файл в одной кодировке и записать в другой.
        """),
        """
        def convert_encoding(src, dst, from_enc, to_enc):
            pass
        """,
        """
        def test_values():
            with open("e1.txt", "w", encoding="cp1251") as f:
                f.write("Привет, мир")
            convert_encoding("e1.txt", "e2.txt", "cp1251", "utf-8")
            with open("e2.txt", encoding="utf-8") as f:
                assert f.read() == "Привет, мир", "Неверное содержимое"
        """,
        """
        def convert_encoding(src, dst, from_enc, to_enc):
            with open(src, encoding=from_enc) as f:
                text = f.read()
            with open(dst, "w", encoding=to_enc) as f:
                f.write(text)
        """),
    cod(f"{P}-encoding-e6", t("""
        Напиши функцию `read_any(path)` — прочитать текст в UTF-8, а если возникла `UnicodeDecodeError` — прочитать в `cp1251`.
        """),
        """
        def read_any(path):
            pass
        """,
        """
        def test_values():
            with open("e3.txt", "w", encoding="utf-8") as f:
                f.write("юникод")
            with open("e4.txt", "w", encoding="cp1251") as f:
                f.write("виндовс")
            assert read_any("e3.txt") == "юникод" and read_any("e4.txt") == "виндовс", "Неверный результат"
        """,
        """
        def read_any(path):
            try:
                with open(path, encoding="utf-8") as f:
                    return f.read()
            except UnicodeDecodeError:
                with open(path, encoding="cp1251") as f:
                    return f.read()
        """),
    cod(f"{P}-encoding-e7", t("""
        Напиши функцию `copy_binary(src, dst)` — скопировать **любой** файл (картинку, архив) побайтно. Вернуть размер в байтах.
        """),
        """
        def copy_binary(src, dst):
            pass
        """,
        """
        def test_values():
            payload = bytes(range(256)) * 3
            with open("b1.bin", "wb") as f:
                f.write(payload)
            assert copy_binary("b1.bin", "b2.bin") == 768, "Размер"
            with open("b2.bin", "rb") as f:
                assert f.read() == payload, "Содержимое"
        """,
        """
        def copy_binary(src, dst):
            with open(src, "rb") as f:
                data = f.read()
            with open(dst, "wb") as f:
                f.write(data)
            return len(data)
        """),
    cod(f"{P}-encoding-e8", t("""
        Напиши функцию `file_type(path)` — определить тип файла по первым байтам («магическим числам»):

        - начинается с `b"\\x89PNG"` → `"png"`;
        - с `b"%PDF"` → `"pdf"`;
        - с `b"PK"` → `"zip"`;
        - иначе → `"unknown"`.

        Читай только первые 4 байта.
        """),
        """
        def file_type(path):
            pass
        """,
        """
        def test_values():
            samples = {"a.png": b"\\x89PNG\\r\\n", "a.pdf": b"%PDF-1.7", "a.zip": b"PK\\x03\\x04", "a.txt": b"hello"}
            for name, data in samples.items():
                with open(name, "wb") as f:
                    f.write(data)
            assert [file_type(n) for n in samples] == ["png", "pdf", "zip", "unknown"], [file_type(n) for n in samples]
        """,
        """
        def file_type(path):
            with open(path, "rb") as f:
                head = f.read(4)
            if head.startswith(b"\\x89PNG"):
                return "png"
            if head.startswith(b"%PDF"):
                return "pdf"
            if head.startswith(b"PK"):
                return "zip"
            return "unknown"
        """, xp=20),
),
)
