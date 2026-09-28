"""Тема «Файлы», модуль 2 «Пути и папки» — задания. Теория — в _fil_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "fil"

m2 = module(f"{P}-m2", "Пути и папки", "📁", "pathlib.Path, части пути, папки и поиск файлов, os и shutil, ошибки файловой системы",

lesson(f"{P}-path", "Пути: pathlib.Path",
    out(f"{P}-path-e1", "Что выведет программа?", """
        from pathlib import PurePosixPath as Path

        p = Path("reports/2024/allure-report.html")
        print(p.name)
        print(p.stem, p.suffix)
        print(p.parent, p.parent.name)
        print(p.parts)
        """, hint="PurePosixPath ведёт себя как Path, но всегда с прямыми слешами — чтобы вывод не зависел от ОС."),
    out(f"{P}-path-e2", "Что выведет программа? Склеивание путей.", """
        from pathlib import PurePosixPath as Path

        base = Path("project")
        cfg = base / "config" / "settings.json"
        print(cfg)
        print(cfg.with_suffix(".yaml"))
        print(cfg.with_name("local.json"))
        print(Path("a/b/../c").parts)
        """, hint="Оператор / склеивает части пути."),
    out(f"{P}-path-e3", "Что выведет программа? Существует ли.", """
        from pathlib import Path

        folder = Path("demo_dir")
        folder.mkdir(exist_ok=True)
        file = folder / "a.txt"
        file.write_text("данные", encoding="utf-8")
        print(folder.exists(), folder.is_dir(), folder.is_file())
        print(file.exists(), file.is_file())
        print((folder / "нет.txt").exists())
        """),
    cod(f"{P}-path-e4", t("""
        Напиши функцию `extension(filename)` — расширение файла в нижнем регистре **без точки**; если расширения нет — пустая строка. Используй `Path(...).suffix`.

        ```
        extension("Report.HTML")       # → "html"
        extension("archive.tar.gz")    # → "gz"
        extension("Makefile")          # → ""
        ```
        """),
        """
        from pathlib import Path


        def extension(filename):
            pass
        """,
        """
        def test_values():
            assert extension("Report.HTML") == "html" and extension("archive.tar.gz") == "gz" and extension("Makefile") == "" and extension("dir/photo.JPG") == "jpg", "Неверный результат"
        """,
        """
        from pathlib import Path


        def extension(filename):
            return Path(filename).suffix.lower().lstrip(".")
        """),
    cod(f"{P}-path-e5", t("""
        Напиши функцию `report_path(base, date_str, name)` — путь отчёта `base/reports/<date_str>/<name>.html` как **строку** с прямыми слешами. Используй `PurePosixPath` и оператор `/`.
        """),
        """
        from pathlib import PurePosixPath


        def report_path(base, date_str, name):
            pass
        """,
        """
        def test_values():
            assert report_path("/tmp/app", "2024-03-08", "smoke") == "/tmp/app/reports/2024-03-08/smoke.html" and report_path("out", "d", "x") == "out/reports/d/x.html", report_path("out", "d", "x")
        """,
        """
        from pathlib import PurePosixPath


        def report_path(base, date_str, name):
            return str(PurePosixPath(base) / "reports" / date_str / f"{name}.html")
        """),
    cod(f"{P}-path-e6", t("""
        Напиши функцию `rename_ext(filenames, new_ext)` — заменить расширение у всех имён файлов. `new_ext` передаётся с точкой.

        ```
        rename_ext(["a.txt", "dir/b.log"], ".bak")   # → ["a.bak", "dir/b.bak"]
        ```
        """),
        """
        from pathlib import PurePosixPath


        def rename_ext(filenames, new_ext):
            pass
        """,
        """
        def test_values():
            assert rename_ext(["a.txt", "dir/b.log", "c"], ".bak") == ["a.bak", "dir/b.bak", "c.bak"] and rename_ext([], ".x") == [], "Неверный результат"
        """,
        """
        from pathlib import PurePosixPath


        def rename_ext(filenames, new_ext):
            return [str(PurePosixPath(name).with_suffix(new_ext)) for name in filenames]
        """),
    cod(f"{P}-path-e7", t("""
        Напиши функцию `group_by_ext(filenames)` — словарь «расширение (с точкой, нижний регистр) → список имён файлов (только `name`, без папок)». Файлы без расширения — под ключом `""`.
        """),
        """
        from pathlib import PurePosixPath


        def group_by_ext(filenames):
            pass
        """,
        """
        def test_values():
            r = group_by_ext(["a/x.PY", "b.py", "c.txt", "Makefile"])
            assert r == {".py": ["x.PY", "b.py"], ".txt": ["c.txt"], "": ["Makefile"]}, r
        """,
        """
        from pathlib import PurePosixPath


        def group_by_ext(filenames):
            result = {}
            for name in filenames:
                p = PurePosixPath(name)
                result.setdefault(p.suffix.lower(), []).append(p.name)
            return result
        """),
    cod(f"{P}-path-e8", t("""
        Напиши функцию `safe_filename(title)` — превратить название теста в безопасное имя файла: оставить буквы, цифры, `-` и `_`; пробелы заменить на `_`; остальные символы удалить; обрезать до 50 символов; добавить `.png`.

        ```
        safe_filename("Вход: неверный пароль?")   # → "Вход_неверный_пароль.png"
        ```
        """),
        """
        def safe_filename(title):
            pass
        """,
        """
        def test_values():
            assert safe_filename("Вход: неверный пароль?") == "Вход_неверный_пароль.png", safe_filename("Вход: неверный пароль?")
            assert safe_filename("a/b\\\\c*d") == "abcd.png" and safe_filename("x" * 80) == "x" * 50 + ".png", "Спецсимволы и длина"
        """,
        """
        def safe_filename(title):
            chars = []
            for ch in title.replace(" ", "_"):
                if ch.isalnum() or ch in "-_":
                    chars.append(ch)
            return "".join(chars)[:50] + ".png"
        """, xp=20),
),

lesson(f"{P}-dirs", "Папки: создание, обход, поиск",
    out(f"{P}-dirs-e1", "Что выведет программа?", """
        from pathlib import Path

        root = Path("proj")
        (root / "src").mkdir(parents=True, exist_ok=True)
        (root / "tests").mkdir(exist_ok=True)
        (root / "src" / "app.py").write_text("print(1)", encoding="utf-8")
        (root / "README.md").write_text("# Проект", encoding="utf-8")

        print(sorted(p.name for p in root.iterdir()))
        print((root / "src" / "app.py").read_text(encoding="utf-8"))
        """, hint="iterdir() — содержимое папки (без вложенных). Порядок не гарантирован, поэтому sorted."),
    out(f"{P}-dirs-e2", "Что выведет программа? glob и rglob.", """
        from pathlib import Path

        root = Path("site")
        for rel in ["index.html", "css/main.css", "js/app.js", "js/lib/util.js", "about.html"]:
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")

        print(sorted(p.name for p in root.glob("*.html")))
        print(sorted(p.name for p in root.rglob("*.js")))
        print(sorted(str(p.relative_to(root)) for p in root.glob("js/*")))
        """, hint="glob — только в этой папке, rglob — во всех вложенных."),
    out(f"{P}-dirs-e3", "Что выведет программа? Размер и статистика.", """
        from pathlib import Path

        d = Path("sizes")
        d.mkdir(exist_ok=True)
        (d / "a.txt").write_text("12345", encoding="utf-8")
        (d / "b.txt").write_text("яя", encoding="utf-8")
        for p in sorted(d.iterdir()):
            print(p.name, p.stat().st_size)
        print(sum(p.stat().st_size for p in d.iterdir()))
        """, hint="st_size — размер в байтах, а не в символах."),
    cod(f"{P}-dirs-e4", t("""
        Напиши функцию `make_dirs(base, names)` — создать внутри папки `base` подпапки с именами из списка (и саму `base`, если её нет). Повторный вызов не должен падать.
        """),
        """
        from pathlib import Path


        def make_dirs(base, names):
            pass
        """,
        """
        from pathlib import Path

        def test_values():
            make_dirs("mk/deep/base", ["logs", "reports"])
            make_dirs("mk/deep/base", ["logs", "screens"])
            assert sorted(p.name for p in Path("mk/deep/base").iterdir()) == ["logs", "reports", "screens"], "Неверные папки"
        """,
        """
        from pathlib import Path


        def make_dirs(base, names):
            for name in names:
                (Path(base) / name).mkdir(parents=True, exist_ok=True)
        """),
    cod(f"{P}-dirs-e5", t("""
        Напиши функцию `list_files(folder, ext)` — отсортированный список **имён** файлов в папке (без вложенных) с расширением `ext` (например, `".log"`). Папки не включать.
        """),
        """
        from pathlib import Path


        def list_files(folder, ext):
            pass
        """,
        """
        from pathlib import Path

        def test_values():
            d = Path("lf")
            (d / "sub.log").mkdir(parents=True, exist_ok=True)
            for n in ["b.log", "a.log", "c.txt"]:
                (d / n).write_text("x", encoding="utf-8")
            assert list_files("lf", ".log") == ["a.log", "b.log"] and list_files("lf", ".csv") == [], list_files("lf", ".log")
        """,
        """
        from pathlib import Path


        def list_files(folder, ext):
            return sorted(p.name for p in Path(folder).iterdir() if p.is_file() and p.suffix == ext)
        """),
    cod(f"{P}-dirs-e6", t("""
        Напиши функцию `find_tests(root)` — найти во всех вложенных папках файлы вида `test_*.py`. Вернуть отсортированный список путей **относительно** `root` в виде строк с `/`.
        """),
        """
        from pathlib import Path


        def find_tests(root):
            pass
        """,
        """
        from pathlib import Path

        def test_values():
            r = Path("ft")
            for rel in ["test_a.py", "api/test_users.py", "api/helpers.py", "ui/pages/test_login.py", "ui/conftest.py"]:
                p = r / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("", encoding="utf-8")
            assert find_tests("ft") == ["api/test_users.py", "test_a.py", "ui/pages/test_login.py"], find_tests("ft")
        """,
        """
        from pathlib import Path


        def find_tests(root):
            root = Path(root)
            return sorted(p.relative_to(root).as_posix() for p in root.rglob("test_*.py"))
        """, hint="p.relative_to(root).as_posix() — относительный путь с прямыми слешами."),
    cod(f"{P}-dirs-e7", t("""
        Напиши функцию `folder_size(folder)` — суммарный размер в байтах всех файлов в папке, включая вложенные.
        """),
        """
        from pathlib import Path


        def folder_size(folder):
            pass
        """,
        """
        from pathlib import Path

        def test_values():
            r = Path("fs")
            (r / "x" / "y").mkdir(parents=True, exist_ok=True)
            (r / "a.bin").write_bytes(b"12345")
            (r / "x" / "b.bin").write_bytes(b"123")
            (r / "x" / "y" / "c.bin").write_bytes(b"1" * 10)
            assert folder_size("fs") == 18, folder_size("fs")
        """,
        """
        from pathlib import Path


        def folder_size(folder):
            return sum(p.stat().st_size for p in Path(folder).rglob("*") if p.is_file())
        """),
    cod(f"{P}-dirs-e8", t("""
        Напиши функцию `tree(folder)` — список строк-дерева содержимого папки: сначала папки, потом файлы, каждая группа по алфавиту; вложенность — отступ по 2 пробела; у папок в конце `/`.

        ```
        tree("t")   # для t/b.txt, t/a/x.txt, t/a/c/ →
        ["a/", "  c/", "  x.txt", "b.txt"]
        ```
        """),
        """
        from pathlib import Path


        def tree(folder, indent=0):
            pass
        """,
        """
        from pathlib import Path

        def test_values():
            r = Path("tr")
            (r / "a" / "c").mkdir(parents=True, exist_ok=True)
            (r / "b.txt").write_text("", encoding="utf-8")
            (r / "a" / "x.txt").write_text("", encoding="utf-8")
            assert tree("tr") == ["a/", "  c/", "  x.txt", "b.txt"], tree("tr")
        """,
        """
        from pathlib import Path


        def tree(folder, indent=0):
            lines = []
            items = sorted(Path(folder).iterdir(), key=lambda p: (not p.is_dir(), p.name))
            for p in items:
                if p.is_dir():
                    lines.append(" " * indent + p.name + "/")
                    lines.extend(tree(p, indent + 2))
                else:
                    lines.append(" " * indent + p.name)
            return lines
        """, xp=25),
),

lesson(f"{P}-os", "Копирование, перемещение, удаление: os и shutil",
    out(f"{P}-os-e1", "Что выведет программа?", """
        import os
        import shutil

        os.makedirs("box/in", exist_ok=True)
        with open("box/in/a.txt", "w", encoding="utf-8") as f:
            f.write("A")
        shutil.copy("box/in/a.txt", "box/b.txt")
        os.rename("box/b.txt", "box/c.txt")
        print(sorted(os.listdir("box")))
        os.remove("box/c.txt")
        print(sorted(os.listdir("box")), os.path.exists("box/c.txt"))
        """),
    out(f"{P}-os-e2", "Что выведет программа? os.path.", """
        import os.path

        path = "reports/2024/result.json"
        print(os.path.basename(path), os.path.dirname(path))
        print(os.path.splitext(path))
        print(os.path.join("a", "b", "c.txt").replace(os.sep, "/"))
        print(os.path.isabs("/etc/hosts"), os.path.isabs("etc/hosts"))
        """, hint="Это старый способ работы с путями — pathlib его заменяет, но встречается повсюду."),
    out(f"{P}-os-e3", "Что выведет программа? Удалить папку.", """
        import os
        import shutil
        from pathlib import Path

        Path("trash/sub").mkdir(parents=True, exist_ok=True)
        Path("trash/sub/f.txt").write_text("x", encoding="utf-8")
        try:
            os.rmdir("trash")
        except OSError:
            print("rmdir: папка не пуста")
        shutil.rmtree("trash")
        print(Path("trash").exists())
        """, hint="rmdir удаляет только пустую папку, shutil.rmtree — со всем содержимым. Осторожно!"),
    cod(f"{P}-os-e4", t("""
        Напиши функцию `backup(path)` — сделать копию файла рядом с именем `<имя>.bak` (например, `config.json` → `config.json.bak`) через `shutil.copy`. Вернуть путь копии строкой.
        """),
        """
        import shutil


        def backup(path):
            pass
        """,
        """
        def test_values():
            with open("config.json", "w", encoding="utf-8") as f:
                f.write('{"a": 1}')
            assert backup("config.json") == "config.json.bak", "Путь копии"
            with open("config.json.bak", encoding="utf-8") as f:
                assert f.read() == '{"a": 1}', "Содержимое копии"
        """,
        """
        import shutil


        def backup(path):
            target = path + ".bak"
            shutil.copy(path, target)
            return target
        """),
    cod(f"{P}-os-e5", t("""
        Напиши функцию `clean_folder(folder, ext)` — удалить в папке (без вложенных) все файлы с расширением `ext` и вернуть их количество.
        """),
        """
        from pathlib import Path


        def clean_folder(folder, ext):
            pass
        """,
        """
        from pathlib import Path

        def test_values():
            d = Path("cf")
            d.mkdir(exist_ok=True)
            for n in ["a.tmp", "b.tmp", "c.txt"]:
                (d / n).write_text("x", encoding="utf-8")
            assert clean_folder("cf", ".tmp") == 2 and sorted(p.name for p in d.iterdir()) == ["c.txt"], "Удаление"
            assert clean_folder("cf", ".tmp") == 0, "Повторный вызов"
        """,
        """
        from pathlib import Path


        def clean_folder(folder, ext):
            count = 0
            for p in Path(folder).iterdir():
                if p.is_file() and p.suffix == ext:
                    p.unlink()
                    count += 1
            return count
        """, hint="Path.unlink() удаляет файл."),
    cod(f"{P}-os-e6", t("""
        Напиши функцию `archive_logs(src, dst)` — **переместить** все файлы `*.log` из папки `src` в папку `dst` (создать её при необходимости). Вернуть отсортированный список перемещённых имён.
        """),
        """
        import shutil
        from pathlib import Path


        def archive_logs(src, dst):
            pass
        """,
        """
        from pathlib import Path

        def test_values():
            s = Path("al_src")
            s.mkdir(exist_ok=True)
            for n in ["b.log", "a.log", "keep.txt"]:
                (s / n).write_text(n, encoding="utf-8")
            assert archive_logs("al_src", "al_dst/old") == ["a.log", "b.log"], "Список"
            assert sorted(p.name for p in s.iterdir()) == ["keep.txt"] and (Path("al_dst/old") / "a.log").read_text(encoding="utf-8") == "a.log", "Перемещение"
        """,
        """
        import shutil
        from pathlib import Path


        def archive_logs(src, dst):
            Path(dst).mkdir(parents=True, exist_ok=True)
            moved = []
            for p in sorted(Path(src).glob("*.log")):
                shutil.move(str(p), str(Path(dst) / p.name))
                moved.append(p.name)
            return moved
        """),
    cod(f"{P}-os-e7", t("""
        Напиши функцию `split_path(path)` — через `os.path` вернуть кортеж `(папка, имя_без_расширения, расширение)`.

        ```
        split_path("logs/2024/run.log")   # → ("logs/2024", "run", ".log")
        ```
        """),
        """
        import os.path


        def split_path(path):
            pass
        """,
        """
        def test_values():
            assert split_path("logs/2024/run.log") == ("logs/2024", "run", ".log") and split_path("a.tar.gz") == ("", "a.tar", ".gz") and split_path("dir/Makefile") == ("dir", "Makefile", ""), "Неверный результат"
        """,
        """
        import os.path


        def split_path(path):
            folder = os.path.dirname(path)
            stem, ext = os.path.splitext(os.path.basename(path))
            return folder, stem, ext
        """),
    cod(f"{P}-os-e8", t("""
        Напиши функцию `keep_latest(folder, n)` — в папке оставить только `n` файлов с «самыми большими» именами (имена вида `report_2024-03-08.html` сортируются по дате), остальные удалить. Вернуть отсортированный список удалённых имён.
        """),
        """
        from pathlib import Path


        def keep_latest(folder, n):
            pass
        """,
        """
        from pathlib import Path

        def test_values():
            d = Path("kl")
            d.mkdir(exist_ok=True)
            names = ["report_2024-03-01.html", "report_2024-03-08.html", "report_2024-02-20.html", "report_2024-03-05.html"]
            for name in names:
                (d / name).write_text("", encoding="utf-8")
            assert keep_latest("kl", 2) == ["report_2024-02-20.html", "report_2024-03-01.html"], "Удалённые"
            assert sorted(p.name for p in d.iterdir()) == ["report_2024-03-05.html", "report_2024-03-08.html"], "Оставшиеся"
            assert keep_latest("kl", 5) == [], "Удалять нечего"
        """,
        """
        from pathlib import Path


        def keep_latest(folder, n):
            files = sorted((p for p in Path(folder).iterdir() if p.is_file()), key=lambda p: p.name)
            to_delete = files[:max(len(files) - n, 0)]
            for p in to_delete:
                p.unlink()
            return [p.name for p in to_delete]
        """, xp=20),
),

lesson(f"{P}-errors", "Ошибки при работе с файлами",
    out(f"{P}-errors-e1", "Что выведет программа?", """
        from pathlib import Path

        Path("err_dir").mkdir(exist_ok=True)
        checks = [
            lambda: open("нет_такого.txt", encoding="utf-8"),
            lambda: open("err_dir", encoding="utf-8"),
            lambda: Path("err_dir").mkdir(),
        ]
        for check in checks:
            try:
                check()
            except OSError as e:
                print(type(e).__name__)
        """, hint="Все ошибки файловой системы — наследники OSError."),
    out(f"{P}-errors-e2", "Что выведет программа? Информация в ошибке.", """
        try:
            open("missing/config.json", encoding="utf-8")
        except FileNotFoundError as e:
            print(e.filename)
            print(e.strerror)
            print(isinstance(e, OSError))
        """),
    out(f"{P}-errors-e3", "Что выведет программа? Проверить или попробовать.", """
        import os

        path = "maybe.txt"
        if os.path.exists(path):
            os.remove(path)

        if os.path.exists(path):
            print("LBYL: читаю")
        else:
            print("LBYL: файла нет")

        try:
            with open(path, encoding="utf-8") as f:
                print(f.read())
        except FileNotFoundError:
            print("EAFP: файла нет")
        """, hint="LBYL — «посмотри, прежде чем прыгать», EAFP — «проще попросить прощения»."),
    cod(f"{P}-errors-e4", t("""
        Напиши функцию `read_or_default(path, default="")` — вернуть содержимое файла, а если его нет — `default`.
        """),
        """
        def read_or_default(path, default=""):
            pass
        """,
        """
        def test_values():
            with open("rd.txt", "w", encoding="utf-8") as f:
                f.write("есть")
            assert read_or_default("rd.txt") == "есть" and read_or_default("нет.txt") == "" and read_or_default("нет.txt", "пусто") == "пусто", "Неверный результат"
        """,
        """
        def read_or_default(path, default=""):
            try:
                with open(path, encoding="utf-8") as f:
                    return f.read()
            except FileNotFoundError:
                return default
        """),
    cod(f"{P}-errors-e5", t("""
        Напиши функцию `load_config(path)` — прочитать файл с JSON и вернуть словарь. Ошибки перевести в понятные:

        - файла нет → `FileNotFoundError(f"нет конфига: {path}")`;
        - плохой JSON → `ValueError(f"битый конфиг: {path}")`.
        """),
        """
        import json


        def load_config(path):
            pass
        """,
        """
        def test_values():
            with open("good.json", "w", encoding="utf-8") as f:
                f.write('{"url": "http://x"}')
            with open("bad.json", "w", encoding="utf-8") as f:
                f.write("{url: ")
            assert load_config("good.json") == {"url": "http://x"}, "Хороший конфиг"
            for path, exc, msg in [("none.json", FileNotFoundError, "нет конфига: none.json"), ("bad.json", ValueError, "битый конфиг: bad.json")]:
                try:
                    load_config(path)
                except exc as e:
                    assert str(e) == msg, str(e)
                else:
                    assert False, f"Нужен {exc.__name__}"
        """,
        """
        import json


        def load_config(path):
            try:
                with open(path, encoding="utf-8") as f:
                    return json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"нет конфига: {path}") from None
            except json.JSONDecodeError:
                raise ValueError(f"битый конфиг: {path}") from None
        """, hint="json.JSONDecodeError — наследник ValueError."),
    cod(f"{P}-errors-e6", t("""
        Напиши функцию `read_many(paths)` — прочитать несколько файлов. Вернуть кортеж `(данные, ошибки)`: `данные` — словарь «путь → содержимое» для прочитанных, `ошибки` — список путей, которые прочитать не удалось (любая `OSError`).
        """),
        """
        def read_many(paths):
            pass
        """,
        """
        from pathlib import Path

        def test_values():
            Path("rm_dir").mkdir(exist_ok=True)
            with open("rm1.txt", "w", encoding="utf-8") as f:
                f.write("один")
            data, errors = read_many(["rm1.txt", "нет.txt", "rm_dir"])
            assert data == {"rm1.txt": "один"} and errors == ["нет.txt", "rm_dir"], (data, errors)
        """,
        """
        def read_many(paths):
            data = {}
            errors = []
            for path in paths:
                try:
                    with open(path, encoding="utf-8") as f:
                        data[path] = f.read()
                except OSError:
                    errors.append(path)
            return data, errors
        """),
    cod(f"{P}-errors-e7", t("""
        Напиши функцию `safe_write(path, text)` — записать файл **атомарно**: сначала во временный файл `path + ".tmp"`, затем заменить им исходный через `os.replace`. Так при сбое посередине записи старый файл останется целым.
        """),
        """
        import os


        def safe_write(path, text):
            pass
        """,
        """
        import os

        def test_values():
            safe_write("atomic.txt", "v1")
            safe_write("atomic.txt", "v2")
            with open("atomic.txt", encoding="utf-8") as f:
                assert f.read() == "v2", "Содержимое"
            assert not os.path.exists("atomic.txt.tmp"), "Временный файл не должен оставаться"
            assert "os.replace" in open("solution.py", encoding="utf-8").read(), "Используй os.replace"
        """,
        """
        import os


        def safe_write(path, text):
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(text)
            os.replace(tmp, path)
        """),
    cod(f"{P}-errors-e8", t("""
        Напиши функцию `ensure_file(path, default_text)` — гарантировать, что файл существует: если его нет, создать (вместе с папками) с текстом `default_text`. Если по этому пути **папка** — выбросить `IsADirectoryError(f"{path} — это папка")`. Вернуть содержимое файла.
        """),
        """
        from pathlib import Path


        def ensure_file(path, default_text):
            pass
        """,
        """
        from pathlib import Path

        def test_values():
            p = Path("ef/sub/settings.ini")
            if p.exists():
                p.unlink()
            assert ensure_file("ef/sub/settings.ini", "[main]") == "[main]", "Создание"
            p.write_text("изменено", encoding="utf-8")
            assert ensure_file("ef/sub/settings.ini", "[main]") == "изменено", "Существующий не трогаем"
            try:
                ensure_file("ef/sub", "x")
            except IsADirectoryError as e:
                assert str(e) == "ef/sub — это папка", str(e)
                return
            assert False, "Нужен IsADirectoryError"
        """,
        """
        from pathlib import Path


        def ensure_file(path, default_text):
            p = Path(path)
            if p.is_dir():
                raise IsADirectoryError(f"{path} — это папка")
            if not p.exists():
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(default_text, encoding="utf-8")
            return p.read_text(encoding="utf-8")
        """, xp=20),
),
)
