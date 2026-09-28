"""Тема «Файлы», модуль 3 «Форматы и практика» — задания. Теория — в _fil_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "fil"

m3 = module(f"{P}-m3", "Форматы и практика", "🗂️", "CSV, большие логи построчно, временные файлы и StringIO, конфиги и тестовые данные",

lesson(f"{P}-csv", "CSV-файлы",
    out(f"{P}-csv-e1", "Что выведет программа? Запись и чтение.", """
        import csv

        rows = [["name", "score"], ["Аня", 90], ["Боря, мл.", 85]]
        with open("scores.csv", "w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerows(rows)

        with open("scores.csv", encoding="utf-8") as f:
            print(f.read(), end="")

        with open("scores.csv", encoding="utf-8", newline="") as f:
            for row in csv.reader(f):
                print(row)
        """, hint="Значение с запятой csv сам берёт в кавычки. Все значения читаются как строки."),
    out(f"{P}-csv-e2", "Что выведет программа? DictReader.", """
        import csv

        with open("users.csv", "w", encoding="utf-8", newline="") as f:
            f.write("id,name,active\\n1,Аня,yes\\n2,Боря,no\\n")

        with open("users.csv", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            print(reader.fieldnames)
            for row in reader:
                print(row["name"], row["active"] == "yes", type(row["id"]).__name__)
        """),
    out(f"{P}-csv-e3", "Что выведет программа? DictWriter и разделитель.", """
        import csv

        users = [{"id": 1, "name": "Аня"}, {"id": 2, "name": "Боря"}]
        with open("out.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "name"], delimiter=";")
            writer.writeheader()
            writer.writerows(users)

        with open("out.csv", encoding="utf-8") as f:
            print(f.read().splitlines())
        """, hint="В русском Excel разделитель часто ';'."),
    cod(f"{P}-csv-e4", t("""
        Напиши функцию `write_csv(path, header, rows)` — записать CSV: строку заголовка и строки данных. Не забудь `newline=""`.
        """),
        """
        import csv


        def write_csv(path, header, rows):
            pass
        """,
        """
        def test_values():
            write_csv("wc.csv", ["a", "b"], [[1, "x, y"], [2, "z"]])
            with open("wc.csv", encoding="utf-8", newline="") as f:
                assert f.read() == 'a,b\\r\\n1,"x, y"\\r\\n2,z\\r\\n', "Неверное содержимое"
        """,
        """
        import csv


        def write_csv(path, header, rows):
            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(rows)
        """),
    cod(f"{P}-csv-e5", t("""
        Напиши функцию `read_users(path)` — прочитать CSV с колонками `id,name,age` и вернуть список словарей, где `id` и `age` — **числа**.
        """),
        """
        import csv


        def read_users(path):
            pass
        """,
        """
        def test_values():
            with open("ru.csv", "w", encoding="utf-8", newline="") as f:
                f.write("id,name,age\\n1,Аня,30\\n2,Боря,25\\n")
            assert read_users("ru.csv") == [{"id": 1, "name": "Аня", "age": 30}, {"id": 2, "name": "Боря", "age": 25}], read_users("ru.csv")
        """,
        """
        import csv


        def read_users(path):
            with open(path, encoding="utf-8", newline="") as f:
                return [
                    {"id": int(row["id"]), "name": row["name"], "age": int(row["age"])}
                    for row in csv.DictReader(f)
                ]
        """),
    cod(f"{P}-csv-e6", t("""
        Напиши функцию `column_avg(path, column)` — среднее значение числовой колонки CSV (с заголовком), округлённое до 2 знаков. Пустые ячейки пропускать. Если чисел нет — `None`.
        """),
        """
        import csv


        def column_avg(path, column):
            pass
        """,
        """
        def test_values():
            with open("avg.csv", "w", encoding="utf-8", newline="") as f:
                f.write("test,time\\na,1.5\\nb,\\nc,2.25\\nd,3\\n")
            assert column_avg("avg.csv", "time") == 2.25, column_avg("avg.csv", "time")
            with open("avg2.csv", "w", encoding="utf-8", newline="") as f:
                f.write("test,time\\na,\\n")
            assert column_avg("avg2.csv", "time") is None, "Нет чисел"
        """,
        """
        import csv


        def column_avg(path, column):
            with open(path, encoding="utf-8", newline="") as f:
                values = [float(row[column]) for row in csv.DictReader(f) if row[column].strip()]
            if not values:
                return None
            return round(sum(values) / len(values), 2)
        """),
    cod(f"{P}-csv-e7", t("""
        Напиши функцию `export_results(path, results)` — `results` — список словарей с ключами `test`, `status`, `duration`. Записать CSV с разделителем `;` и заголовком `test;status;duration` через `DictWriter`. Лишние ключи в словарях игнорировать.
        """),
        """
        import csv


        def export_results(path, results):
            pass
        """,
        """
        def test_values():
            export_results("er.csv", [{"test": "login", "status": "passed", "duration": 1.2, "extra": 1}, {"test": "cart", "status": "failed", "duration": 3}])
            with open("er.csv", encoding="utf-8") as f:
                assert f.read().splitlines() == ["test;status;duration", "login;passed;1.2", "cart;failed;3"], "Неверное содержимое"
        """,
        """
        import csv


        def export_results(path, results):
            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["test", "status", "duration"], delimiter=";", extrasaction="ignore")
                writer.writeheader()
                writer.writerows(results)
        """, hint='extrasaction="ignore" — не падать на лишних ключах.'),
    cod(f"{P}-csv-e8", t("""
        Напиши функцию `failed_by_suite(path)` — CSV с колонками `suite,test,status`. Вернуть словарь «сьют → количество упавших (`status == "failed"`)» только для сьютов, где есть падения, отсортированный по убыванию количества.
        """),
        """
        import csv


        def failed_by_suite(path):
            pass
        """,
        """
        def test_values():
            with open("fs.csv", "w", encoding="utf-8", newline="") as f:
                f.write("suite,test,status\\napi,a,failed\\nui,b,passed\\nui,c,failed\\napi,d,failed\\ndb,e,passed\\n")
            r = failed_by_suite("fs.csv")
            assert r == {"api": 2, "ui": 1} and list(r) == ["api", "ui"], r
        """,
        """
        import csv


        def failed_by_suite(path):
            counts = {}
            with open(path, encoding="utf-8", newline="") as f:
                for row in csv.DictReader(f):
                    if row["status"] == "failed":
                        counts[row["suite"]] = counts.get(row["suite"], 0) + 1
            return dict(sorted(counts.items(), key=lambda kv: -kv[1]))
        """, xp=20),
),

lesson(f"{P}-logs", "Большие файлы и логи",
    out(f"{P}-logs-e1", "Что выведет программа? Файл читается лениво.", """
        with open("big.log", "w", encoding="utf-8") as f:
            for i in range(1, 20_001):
                f.write(f"{i} {'ERROR' if i % 5_000 == 0 else 'INFO'} событие\\n")

        errors = 0
        with open("big.log", encoding="utf-8") as f:
            for line in f:
                if " ERROR " in line:
                    errors += 1
        print(errors)
        """, hint="for line in f читает по одной строке — память не зависит от размера файла."),
    out(f"{P}-logs-e2", "Что выведет программа? Генератор над файлом.", """
        with open("app.log", "w", encoding="utf-8") as f:
            f.write("INFO старт\\nERROR база\\nWARN диск\\nERROR сеть\\nINFO стоп\\n")

        def errors(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if line.startswith("ERROR"):
                        yield line.split(" ", 1)[1].strip()

        print(list(errors("app.log")))
        print(next(errors("app.log")))
        """),
    out(f"{P}-logs-e3", "Что выведет программа? Хвост файла.", """
        from collections import deque

        with open("tail.log", "w", encoding="utf-8") as f:
            for i in range(1, 11):
                f.write(f"строка {i}\\n")

        with open("tail.log", encoding="utf-8") as f:
            last = deque(f, maxlen=3)
        print([line.strip() for line in last])
        """, hint="deque с maxlen хранит только последние элементы."),
    cod(f"{P}-logs-e4", t("""
        Напиши функцию `count_levels(path)` — словарь «уровень → количество» для лога, где уровень — **первое слово** строки. Пустые строки пропускать. Читай построчно.
        """),
        """
        def count_levels(path):
            pass
        """,
        """
        def test_values():
            with open("cl.log", "w", encoding="utf-8") as f:
                f.write("INFO a\\nERROR b\\n\\nINFO c\\nWARN d\\nERROR e\\n")
            assert count_levels("cl.log") == {"INFO": 2, "ERROR": 2, "WARN": 1}, count_levels("cl.log")
        """,
        """
        def count_levels(path):
            counts = {}
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    level = line.split()[0]
                    counts[level] = counts.get(level, 0) + 1
            return counts
        """),
    cod(f"{P}-logs-e5", t("""
        Напиши **генератор** `read_errors(path)` — выдаёт строки лога (без `\\n`), в которых есть `"ERROR"`. Файл должен читаться построчно, а не целиком.
        """),
        """
        def read_errors(path):
            pass
        """,
        """
        import types

        def test_values():
            with open("re.log", "w", encoding="utf-8") as f:
                f.write("ok\\nERROR 1\\nok\\nxx ERROR 2\\n")
            g = read_errors("re.log")
            assert isinstance(g, types.GeneratorType), "Нужен генератор (yield)"
            assert list(g) == ["ERROR 1", "xx ERROR 2"], "Неверные строки"
        """,
        """
        def read_errors(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if "ERROR" in line:
                        yield line.rstrip("\\n")
        """),
    cod(f"{P}-logs-e6", t("""
        Напиши функцию `tail(path, n)` — последние `n` строк файла без `\\n`. Используй `collections.deque(maxlen=n)`, чтобы не держать в памяти весь файл.
        """),
        """
        from collections import deque


        def tail(path, n):
            pass
        """,
        """
        def test_values():
            with open("tl.log", "w", encoding="utf-8") as f:
                f.write("".join(f"{i}\\n" for i in range(1, 8)))
            assert tail("tl.log", 3) == ["5", "6", "7"] and tail("tl.log", 10) == [str(i) for i in range(1, 8)], tail("tl.log", 3)
        """,
        """
        from collections import deque


        def tail(path, n):
            with open(path, encoding="utf-8") as f:
                return [line.rstrip("\\n") for line in deque(f, maxlen=n)]
        """),
    cod(f"{P}-logs-e7", t("""
        Напиши функцию `slow_requests(path, limit_ms)` — лог доступа, строки вида `GET /api/users 200 153ms`. Вернуть список кортежей `(метод, путь, время)` для запросов медленнее `limit_ms`, отсортированный по убыванию времени.
        """),
        """
        def slow_requests(path, limit_ms):
            pass
        """,
        """
        def test_values():
            with open("access.log", "w", encoding="utf-8") as f:
                f.write("GET /api/users 200 153ms\\nPOST /api/login 200 950ms\\nGET /health 200 3ms\\nGET /api/report 500 1200ms\\n")
            assert slow_requests("access.log", 500) == [("GET", "/api/report", 1200), ("POST", "/api/login", 950)] and slow_requests("access.log", 5000) == [], slow_requests("access.log", 500)
        """,
        """
        def slow_requests(path, limit_ms):
            result = []
            with open(path, encoding="utf-8") as f:
                for line in f:
                    method, url, status, took = line.split()
                    ms = int(took.removesuffix("ms"))
                    if ms > limit_ms:
                        result.append((method, url, ms))
            return sorted(result, key=lambda r: -r[2])
        """),
    cod(f"{P}-logs-e8", t("""
        Напиши функцию `split_file(path, lines_per_part)` — разрезать большой файл на части по `lines_per_part` строк: `path.part1`, `path.part2`, … Вернуть количество частей. Читай построчно.
        """),
        """
        def split_file(path, lines_per_part):
            pass
        """,
        """
        def test_values():
            with open("sp.txt", "w", encoding="utf-8") as f:
                f.write("".join(f"{i}\\n" for i in range(1, 8)))
            assert split_file("sp.txt", 3) == 3, "Количество частей"
            parts = []
            for k in (1, 2, 3):
                with open(f"sp.txt.part{k}", encoding="utf-8") as f:
                    parts.append(f.read())
            assert parts == ["1\\n2\\n3\\n", "4\\n5\\n6\\n", "7\\n"], parts
        """,
        """
        def split_file(path, lines_per_part):
            part = 0
            out = None
            with open(path, encoding="utf-8") as f:
                for i, line in enumerate(f):
                    if i % lines_per_part == 0:
                        if out:
                            out.close()
                        part += 1
                        out = open(f"{path}.part{part}", "w", encoding="utf-8")
                    out.write(line)
            if out:
                out.close()
            return part
        """, xp=20),
),

lesson(f"{P}-temp", "Временные файлы и StringIO",
    out(f"{P}-temp-e1", "Что выведет программа? Временная папка.", """
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "data.txt").write_text("временно", encoding="utf-8")
            print([p.name for p in folder.iterdir()])
            saved = folder
        print(saved.exists())
        """, hint="После выхода из with папка удаляется со всем содержимым."),
    out(f"{P}-temp-e2", "Что выведет программа? StringIO — файл в памяти.", """
        import io

        buf = io.StringIO()
        buf.write("строка 1\\n")
        print("строка 2", file=buf)
        print(repr(buf.getvalue()))

        fake = io.StringIO("a\\nb\\nc\\n")
        print([line.strip() for line in fake])
        """),
    out(f"{P}-temp-e3", "Что выведет программа? Функция, принимающая файл.", """
        import io
        import csv

        def count_rows(f):
            return sum(1 for _ in csv.DictReader(f))

        data = io.StringIO("id,name\\n1,Аня\\n2,Боря\\n")
        print(count_rows(data))

        with open("real.csv", "w", encoding="utf-8", newline="") as f:
            f.write("id\\n1\\n2\\n3\\n")
        with open("real.csv", encoding="utf-8", newline="") as f:
            print(count_rows(f))
        """, hint="Функция работает и с настоящим файлом, и с StringIO — ей важны только методы."),
    cod(f"{P}-temp-e4", t("""
        Напиши функцию `sum_numbers(f)` — принимает **открытый файлоподобный объект** (не путь!) и возвращает сумму чисел, по одному на строке. Пустые строки пропускать. Тест передаст `io.StringIO`.
        """),
        """
        def sum_numbers(f):
            pass
        """,
        """
        import io

        def test_values():
            assert sum_numbers(io.StringIO("1\\n2\\n\\n3.5\\n")) == 6.5 and sum_numbers(io.StringIO("")) == 0, "Неверная сумма"
        """,
        """
        def sum_numbers(f):
            return sum(float(line) for line in f if line.strip())
        """),
    cod(f"{P}-temp-e5", t("""
        Напиши функцию `render_report(results)` — сформировать текст отчёта через `io.StringIO` и `print(..., file=buf)`: для каждого `(имя, ok)` строка `✓ имя` или `✗ имя`, в конце `итого: N`. Вернуть строку.
        """),
        """
        import io


        def render_report(results):
            pass
        """,
        """
        def test_values():
            assert render_report([("login", True), ("cart", False)]) == "✓ login\\n✗ cart\\nитого: 2\\n", repr(render_report([("login", True), ("cart", False)]))
            assert "StringIO" in open("solution.py", encoding="utf-8").read(), "Используй io.StringIO"
        """,
        """
        import io


        def render_report(results):
            buf = io.StringIO()
            for name, ok in results:
                print("✓" if ok else "✗", name, file=buf)
            print(f"итого: {len(results)}", file=buf)
            return buf.getvalue()
        """),
    cod(f"{P}-temp-e6", t("""
        Напиши функцию `roundtrip(lines)` — записать строки во **временный файл** (через `tempfile.TemporaryDirectory`), прочитать их обратно и вернуть список прочитанных строк. После работы временных файлов остаться не должно.
        """),
        """
        import tempfile
        from pathlib import Path


        def roundtrip(lines):
            pass
        """,
        """
        def test_values():
            assert roundtrip(["a", "б", "c"]) == ["a", "б", "c"] and roundtrip([]) == [], "Неверный результат"
            assert "tempfile" in open("solution.py", encoding="utf-8").read(), "Используй tempfile"
        """,
        """
        import tempfile
        from pathlib import Path


        def roundtrip(lines):
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "data.txt"
                path.write_text("".join(line + "\\n" for line in lines), encoding="utf-8")
                return path.read_text(encoding="utf-8").splitlines()
        """),
    cod(f"{P}-temp-e7", t("""
        Напиши функцию `parse_csv_text(text)` — разобрать CSV **из строки** (например, из тела HTTP-ответа) в список словарей. Используй `io.StringIO` и `csv.DictReader`.
        """),
        """
        import csv
        import io


        def parse_csv_text(text):
            pass
        """,
        """
        def test_values():
            assert parse_csv_text("id,name\\n1,Аня\\n2,\\"Боря, мл.\\"\\n") == [{"id": "1", "name": "Аня"}, {"id": "2", "name": "Боря, мл."}], "Неверный результат"
        """,
        """
        import csv
        import io


        def parse_csv_text(text):
            return list(csv.DictReader(io.StringIO(text)))
        """),
    cod(f"{P}-temp-e8", t("""
        Напиши функцию `process_file(src, dst, transform)` — прочитать файл `src` построчно, применить к каждой строке (без `\\n`) функцию `transform` и записать результат в `dst`. В тесте функцию проверят на временной папке.
        """),
        """
        def process_file(src, dst, transform):
            pass
        """,
        """
        import tempfile
        from pathlib import Path

        def test_values():
            with tempfile.TemporaryDirectory() as tmp:
                src = Path(tmp) / "in.txt"
                dst = Path(tmp) / "out.txt"
                src.write_text("аня\\nборя\\n", encoding="utf-8")
                process_file(src, dst, str.upper)
                assert dst.read_text(encoding="utf-8") == "АНЯ\\nБОРЯ\\n", dst.read_text(encoding="utf-8")
        """,
        """
        def process_file(src, dst, transform):
            with open(src, encoding="utf-8") as fin, open(dst, "w", encoding="utf-8") as fout:
                for line in fin:
                    fout.write(transform(line.rstrip("\\n")) + "\\n")
        """, hint="В одном with можно открыть два файла через запятую.", xp=20),
),

lesson(f"{P}-config", "Практика: конфиги и тестовые данные",
    out(f"{P}-config-e1", "Что выведет программа? .env-файл.", """
        env_text = '''# настройки
        BASE_URL=https://api.test
        TIMEOUT = 5

        TOKEN="abc=123"
        '''
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_text)

        settings = {}
        with open(".env", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                settings[key.strip()] = value.strip().strip('"')
        print(settings)
        """, hint="split('=', 1) режет только по первому '=' — значение может его содержать."),
    out(f"{P}-config-e2", "Что выведет программа? configparser.", """
        import configparser

        with open("settings.ini", "w", encoding="utf-8") as f:
            f.write("[api]\\nurl = https://api.test\\ntimeout = 5\\n\\n[ui]\\nbrowser = chrome\\nheadless = yes\\n")

        config = configparser.ConfigParser()
        config.read("settings.ini", encoding="utf-8")
        print(config.sections())
        print(config["api"]["url"], config.getint("api", "timeout") + 1)
        print(config.getboolean("ui", "headless"), config.get("ui", "window", fallback="1920x1080"))
        """),
    out(f"{P}-config-e3", "Что выведет программа? Тестовые данные из файла.", """
        import json
        from pathlib import Path

        Path("testdata").mkdir(exist_ok=True)
        Path("testdata/users.json").write_text(json.dumps([
            {"login": "admin", "password": "secret", "expected": 200},
            {"login": "guest", "password": "", "expected": 400},
        ]), encoding="utf-8")

        def login(user, password):
            return 200 if password else 400

        cases = json.loads(Path("testdata/users.json").read_text(encoding="utf-8"))
        for case in cases:
            status = login(case["login"], case["password"])
            print(case["login"], "PASS" if status == case["expected"] else "FAIL")
        """, hint="Данные отделены от кода теста — их можно менять без правки кода."),
    cod(f"{P}-config-e4", t("""
        Напиши функцию `load_env(path)` — прочитать `.env`-файл в словарь:

        - пустые строки и строки с `#` в начале пропускать;
        - делить по **первому** `=`;
        - пробелы вокруг ключа и значения убрать, кавычки вокруг значения (`"` или `'`) снять.
        """),
        """
        def load_env(path):
            pass
        """,
        """
        def test_values():
            with open("t.env", "w", encoding="utf-8") as f:
                f.write("# comment\\nA=1\\n\\n B = two words \\nC=\\"x=y\\"\\nD='q'\\n")
            assert load_env("t.env") == {"A": "1", "B": "two words", "C": "x=y", "D": "q"}, load_env("t.env")
        """,
        """
        def load_env(path):
            result = {}
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    key, value = line.split("=", 1)
                    result[key.strip()] = value.strip().strip("\\"'")
            return result
        """),
    cod(f"{P}-config-e5", t("""
        Напиши функцию `read_settings(path)` — прочитать INI-файл через `configparser` и вернуть словарь:

        - `"url"` — из секции `[api]`, ключ `url`;
        - `"timeout"` — `[api] timeout` как **int**, по умолчанию `10`;
        - `"headless"` — `[ui] headless` как **bool**, по умолчанию `False`.
        """),
        """
        import configparser


        def read_settings(path):
            pass
        """,
        """
        def test_values():
            with open("s1.ini", "w", encoding="utf-8") as f:
                f.write("[api]\\nurl = http://a\\ntimeout = 3\\n[ui]\\nheadless = true\\n")
            with open("s2.ini", "w", encoding="utf-8") as f:
                f.write("[api]\\nurl = http://b\\n[ui]\\n")
            assert read_settings("s1.ini") == {"url": "http://a", "timeout": 3, "headless": True}, read_settings("s1.ini")
            assert read_settings("s2.ini") == {"url": "http://b", "timeout": 10, "headless": False}, read_settings("s2.ini")
        """,
        """
        import configparser


        def read_settings(path):
            config = configparser.ConfigParser()
            config.read(path, encoding="utf-8")
            return {
                "url": config.get("api", "url"),
                "timeout": config.getint("api", "timeout", fallback=10),
                "headless": config.getboolean("ui", "headless", fallback=False),
            }
        """),
    cod(f"{P}-config-e6", t("""
        Напиши функцию `merge_configs(default_path, local_path)` — прочитать два JSON-конфига и вернуть объединённый словарь: значения из `local` перекрывают `default`. Если `local`-файла нет — вернуть только `default`.
        """),
        """
        import json


        def merge_configs(default_path, local_path):
            pass
        """,
        """
        import json

        def test_values():
            with open("default.json", "w", encoding="utf-8") as f:
                json.dump({"url": "http://prod", "timeout": 10}, f)
            with open("local.json", "w", encoding="utf-8") as f:
                json.dump({"url": "http://localhost"}, f)
            assert merge_configs("default.json", "local.json") == {"url": "http://localhost", "timeout": 10}, "С local"
            assert merge_configs("default.json", "нет.json") == {"url": "http://prod", "timeout": 10}, "Без local"
        """,
        """
        import json


        def merge_configs(default_path, local_path):
            with open(default_path, encoding="utf-8") as f:
                config = json.load(f)
            try:
                with open(local_path, encoding="utf-8") as f:
                    config.update(json.load(f))
            except FileNotFoundError:
                pass
            return config
        """),
    cod(f"{P}-config-e7", t("""
        Напиши функцию `load_cases(folder)` — в папке лежат JSON-файлы с тестовыми случаями (каждый файл — один словарь). Вернуть список пар `(имя_файла_без_расширения, данные)`, отсортированный по имени. Файлы других типов пропускать.
        """),
        """
        import json
        from pathlib import Path


        def load_cases(folder):
            pass
        """,
        """
        import json
        from pathlib import Path

        def test_values():
            d = Path("cases")
            d.mkdir(exist_ok=True)
            (d / "b_empty_login.json").write_text(json.dumps({"login": ""}), encoding="utf-8")
            (d / "a_ok.json").write_text(json.dumps({"login": "anna"}), encoding="utf-8")
            (d / "notes.txt").write_text("не тест", encoding="utf-8")
            assert load_cases("cases") == [("a_ok", {"login": "anna"}), ("b_empty_login", {"login": ""})], load_cases("cases")
        """,
        """
        import json
        from pathlib import Path


        def load_cases(folder):
            result = []
            for p in sorted(Path(folder).glob("*.json")):
                result.append((p.stem, json.loads(p.read_text(encoding="utf-8"))))
            return result
        """, hint="Так готовят данные для @pytest.mark.parametrize."),
    cod(f"{P}-config-e8", t("""
        Напиши функцию `save_screenshot(folder, test_name, data)` — сохранить байты скриншота упавшего теста в `folder/<test_name>.png` (папку создать). Если такой файл уже есть — добавить суффикс `_2`, `_3`, … Вернуть **имя** сохранённого файла.
        """),
        """
        from pathlib import Path


        def save_screenshot(folder, test_name, data):
            pass
        """,
        """
        import shutil
        from pathlib import Path

        def test_values():
            shutil.rmtree("shots", ignore_errors=True)
            names = [save_screenshot("shots/fail", "test_login", b"PNG" + bytes([i])) for i in range(3)]
            assert names == ["test_login.png", "test_login_2.png", "test_login_3.png"], names
            assert (Path("shots/fail") / "test_login_2.png").read_bytes() == b"PNG\\x01", "Содержимое"
        """,
        """
        from pathlib import Path


        def save_screenshot(folder, test_name, data):
            folder = Path(folder)
            folder.mkdir(parents=True, exist_ok=True)
            path = folder / f"{test_name}.png"
            n = 2
            while path.exists():
                path = folder / f"{test_name}_{n}.png"
                n += 1
            path.write_bytes(data)
            return path.name
        """, xp=20),
),
)
