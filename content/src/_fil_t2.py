"""Теория модуля «Пути и папки» темы «Файлы».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- fil-path ----------
'fil-path': dict(
    full=t(r'''
## Зачем это нужно

Путь к файлу — это не просто строка. В Windows части пути разделяются `\`, в Linux и macOS — `/`. Нужно достать имя файла, расширение, папку; склеить путь из частей; проверить, существует ли файл. Современный способ — модуль `pathlib` и класс `Path`.

## Части пути

```python
from pathlib import PurePosixPath as Path

p = Path("reports/2024/allure-report.html")
print(p.name)
print(p.stem, p.suffix)
print(p.parent, p.parent.name)
print(p.parts)
```

- `Path("строка")` — объект-путь.
- `name` — последняя часть (имя файла с расширением).
- `stem` — имя без расширения, `suffix` — расширение **с точкой**.
- `parent` — папка, в которой лежит файл (тоже `Path`).
- `parts` — кортеж всех частей.
- Здесь `PurePosixPath` — «чистый» путь с прямыми слешами, чтобы вывод не зависел от системы. В обычном коде пишут просто `from pathlib import Path` — у него те же атрибуты.
- Вывод: `allure-report.html`, `allure-report .html`, `reports/2024 2024`, `('reports', '2024', 'allure-report.html')`.

## Склеивание: оператор /

```python
from pathlib import PurePosixPath as Path

base = Path("project")
cfg = base / "config" / "settings.json"
print(cfg)
print(cfg.with_suffix(".yaml"))
print(cfg.with_name("local.json"))
```

- `путь / "часть"` — добавить часть пути. Правильный разделитель подставится сам — не нужно склеивать строки через `+ "/" +`.
- `with_suffix(".yaml")` — тот же путь с другим расширением.
- `with_name("local.json")` — тот же путь с другим именем файла.
- Вывод: `project/config/settings.json`, `project/config/settings.yaml`, `project/config/local.json`.

## Проверки на диске

```python
from pathlib import Path

folder = Path("demo_dir")
folder.mkdir(exist_ok=True)
file = folder / "a.txt"
file.write_text("данные", encoding="utf-8")
print(folder.exists(), folder.is_dir(), folder.is_file())
print(file.exists(), file.is_file())
print((folder / "нет.txt").exists())
```

- `exists()` — есть ли что-то по этому пути; `is_file()` — это файл; `is_dir()` — это папка.
- `mkdir(exist_ok=True)` — создать папку, не падая, если она уже есть.
- `write_text(текст, encoding=...)` — записать файл одной строкой (подробнее — в следующем уроке).
- Вывод: `True True False`, `True True`, `False`.

## Полезное

```python
from pathlib import Path

p = Path("demo_dir/a.txt")
print(p.suffix == ".txt", str(p).endswith("a.txt"))
print(p.resolve().is_absolute())
```

- `str(p)` — путь как строка (для функций, которые ждут строку).
- `resolve()` — полный (абсолютный) путь от корня диска.
- `Path.cwd()` — текущая рабочая папка, `Path.home()` — домашняя папка пользователя.
- Вывод: `True True`, `True`.

## Безопасные имена файлов

Имена файлов не могут содержать `/`, а в Windows — ещё `\ : * ? " < > |`. Если имя строится из названия теста или данных пользователя, лишние символы нужно убрать:

```python
title = "Вход: неверный пароль?"
safe = "".join(ch for ch in title.replace(" ", "_") if ch.isalnum() or ch in "-_")
print(safe + ".png")
```

- `ch.isalnum()` — буква или цифра (включая русские).
- Вывод: `Вход_неверный_пароль.png`.

## Итог

- `from pathlib import Path`; `Path("a") / "b" / "c.txt"`.
- `name`, `stem`, `suffix`, `parent`, `parts`.
- `with_suffix()`, `with_name()`.
- `exists()`, `is_file()`, `is_dir()`, `resolve()`, `Path.cwd()`.
'''),
    short=t(r'''
```py
from pathlib import Path

p = Path("reports") / "2024" / "run.html"
p.name       # 'run.html'
p.stem       # 'run'
p.suffix     # '.html'
p.parent     # Path('reports/2024')
p.with_suffix(".json"), p.with_name("x.html")
p.exists(), p.is_file(), p.is_dir()
str(p), p.resolve(), Path.cwd(), Path.home()
```
'''),
    quiz=[
        q('Что вернёт `Path("a/b/report.html").suffix`?',
            ['html', '.html', 'report', 'report.html'],
            1, 'Расширение с точкой.'),
        q('Как правильно склеить путь из частей?',
            ['`"a" + "/" + "b"`', '`Path("a") / "b"`', '`Path("a") + "b"`', '`Path("a").join("b")`'],
            1, 'Оператор / подставит правильный разделитель.'),
        q('Что вернёт `Path("x.txt").stem`?',
            ['x.txt', 'x', '.txt', 'txt'],
            1, 'Имя без расширения.'),
    ],
),

# ---------- fil-dirs ----------
'fil-dirs': dict(
    full=t(r'''
## Зачем это нужно

Отчёты складывают в папку с датой, скриншоты — в папку упавших тестов, тестовые данные ищут по всему проекту. Нужно уметь создавать папки, смотреть их содержимое, искать файлы по шаблону.

## Создание папок и файлов

```python
from pathlib import Path

root = Path("proj")
(root / "src").mkdir(parents=True, exist_ok=True)
(root / "tests").mkdir(exist_ok=True)
(root / "src" / "app.py").write_text("print(1)", encoding="utf-8")
(root / "README.md").write_text("# Проект", encoding="utf-8")

print(sorted(p.name for p in root.iterdir()))
print((root / "src" / "app.py").read_text(encoding="utf-8"))
```

- `mkdir(parents=True)` — создать и все недостающие папки на пути (`proj`, затем `proj/src`).
- `exist_ok=True` — не падать, если папка уже есть. Без него — `FileExistsError`.
- `write_text(текст)` / `read_text()` — записать или прочитать файл целиком одной строкой, без `with` и `open`.
- `iterdir()` — всё, что лежит в папке (файлы и папки, без вложенных). Порядок **не гарантирован** — поэтому `sorted`.
- Вывод: `['README.md', 'src', 'tests']`, `print(1)`.

## Байты целиком

```python
from pathlib import Path

p = Path("logo.bin")
p.write_bytes(b"\x89PNG")
print(p.read_bytes(), p.stat().st_size)
```

- `write_bytes` / `read_bytes` — то же для двоичных данных.
- `stat().st_size` — размер файла в **байтах**.
- Вывод: `b'\x89PNG' 4`.

## Поиск по шаблону: glob и rglob

```python
from pathlib import Path

root = Path("site")
for rel in ["index.html", "css/main.css", "js/app.js", "js/lib/util.js", "about.html"]:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")

print(sorted(p.name for p in root.glob("*.html")))
print(sorted(p.name for p in root.rglob("*.js")))
print(sorted(str(p.relative_to(root)) for p in root.glob("js/*")))
```

- `path.parent.mkdir(parents=True, exist_ok=True)` — перед записью файла создать его папку. Частый приём.
- `glob("*.html")` — файлы по шаблону в **этой** папке. `*` — любые символы, `?` — один символ.
- `rglob("*.js")` — во всех вложенных папках (recursive). То же, что `glob("**/*.js")`.
- `relative_to(root)` — путь относительно папки: `site/js/app.js` → `js/app.js`.
- Вывод: `['about.html', 'index.html']`, `['app.js', 'util.js']`, `['js/app.js', 'js/lib']`.

## Только файлы

```python
from pathlib import Path

d = Path("site")
for rel in ["index.html", "about.html", "css/main.css", "js/app.js"]:
    (d / rel).parent.mkdir(parents=True, exist_ok=True)
    (d / rel).write_text("", encoding="utf-8")
print(sorted(p.name for p in d.iterdir() if p.is_file()))
print(sorted(p.name for p in d.iterdir() if p.is_dir()))
```

- `iterdir()` отдаёт и файлы, и папки — фильтруй через `is_file()` / `is_dir()`.
- Вывод: `['about.html', 'index.html']`, `['css', 'js']`.

## Размер папки

```python
from pathlib import Path

d = Path("sizes")
d.mkdir(exist_ok=True)
(d / "a.txt").write_text("12345", encoding="utf-8")
(d / "b.txt").write_text("яя", encoding="utf-8")
total = sum(p.stat().st_size for p in d.rglob("*") if p.is_file())
print(total)
```

- `rglob("*")` — всё содержимое на любой глубине. Размер кириллицы — 2 байта на букву.
- Вывод: `9`.

## Итог

- `mkdir(parents=True, exist_ok=True)`.
- `read_text` / `write_text`, `read_bytes` / `write_bytes` — файл целиком.
- `iterdir()` — содержимое папки; `glob("*.ext")`, `rglob("*.ext")` — поиск.
- `relative_to(root)`, `stat().st_size`.
'''),
    short=t(r'''
```py
from pathlib import Path

Path("a/b/c").mkdir(parents=True, exist_ok=True)
p.write_text("x", encoding="utf-8"); p.read_text(encoding="utf-8")
p.write_bytes(b".."); p.read_bytes()
p.parent.mkdir(parents=True, exist_ok=True)   # перед записью

sorted(d.iterdir())            # содержимое (без вложенных)
d.glob("*.log")                # в папке
d.rglob("test_*.py")           # во всех вложенных
p.relative_to(d).as_posix()
p.stat().st_size               # байты
```
'''),
    quiz=[
        q('Что делает `mkdir(parents=True)`?',
            ['Создаёт родительскую папку вместо нужной', 'Создаёт все недостающие папки на пути', 'Удаляет родителей', 'Ничего особенного'],
            1, 'Как mkdir -p в терминале.'),
        q('Чем `rglob` отличается от `glob`?',
            ['Ничем', 'Ищет во всех вложенных папках', 'Ищет только папки', 'Ищет без учёта регистра'],
            1, 'r — recursive.'),
        q('Гарантирует ли `iterdir()` порядок?',
            ['Да, по алфавиту', 'Нет, нужен sorted', 'Да, по дате', 'Да, по размеру'],
            1, 'Порядок зависит от файловой системы.'),
    ],
),

# ---------- fil-os ----------
'fil-os': dict(
    full=t(r'''
## Зачем это нужно

Файлы нужно копировать (бэкап конфига), перемещать (архив старых логов), переименовывать и удалять (очистка временных данных). Для этого есть модули `os` и `shutil`. Модуль `os.path` — старый способ работы с путями, он встречается в огромном количестве кода.

## Копировать, переименовать, удалить

```python
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
```

- `os.makedirs(путь, exist_ok=True)` — как `Path.mkdir(parents=True, exist_ok=True)`.
- `shutil.copy(откуда, куда)` — скопировать файл.
- `os.rename(старое, новое)` — переименовать или переместить в пределах диска.
- `os.listdir(папка)` — список имён в папке (строки, не пути).
- `os.remove(путь)` — удалить файл **навсегда** (не в корзину).
- Вывод: `['c.txt', 'in']`, `['in'] False`.

## То же через pathlib

- `Path("a").rename("b")` — переименовать.
- `Path("a").unlink()` — удалить файл; `unlink(missing_ok=True)` — не падать, если его нет.
- `Path("d").rmdir()` — удалить пустую папку.
- Копирования в `pathlib` нет — используют `shutil`.

## Перемещение и удаление папок

```python
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
```

- `os.rmdir` удаляет только **пустую** папку.
- `shutil.rmtree(папка)` — удалить папку со всем содержимым. Опасная команда: проверяй путь!
- `shutil.move(откуда, куда)` — переместить файл или папку, в том числе на другой диск.
- `shutil.copytree(откуда, куда)` — скопировать папку целиком.
- Вывод: `rmdir: папка не пуста`, `False`.

## os.path

```python
import os.path

path = "reports/2024/result.json"
print(os.path.basename(path), os.path.dirname(path))
print(os.path.splitext(path))
print(os.path.isabs("/etc/hosts"), os.path.isabs("etc/hosts"))
```

- `basename` — имя файла (`Path.name`), `dirname` — папка (`Path.parent`).
- `splitext` — кортеж (всё до расширения, расширение) — аналог `stem` и `suffix`.
- `os.path.join("a", "b")` — склеить части пути (`Path("a") / "b"`).
- `isabs` — абсолютный ли путь (начинается от корня).
- Вывод: `result.json reports/2024`, `('reports/2024/result', '.json')`, `True False`.

## Бэкап и ротация

```python
import shutil
from pathlib import Path

d = Path("rot")
d.mkdir(exist_ok=True)
for day in ["01", "02", "03", "04"]:
    (d / f"report_2024-03-{day}.html").write_text("", encoding="utf-8")

files = sorted(d.iterdir())
for old in files[:-2]:
    old.unlink()
print([p.name for p in sorted(d.iterdir())])
```

- Имена с датой в формате `ГГГГ-ММ-ДД` сортируются хронологически.
- Удаляем всё, кроме двух последних, — так не даём отчётам заполнить диск.
- Вывод: `['report_2024-03-03.html', 'report_2024-03-04.html']`.

## Итог

- `shutil.copy`, `shutil.move`, `shutil.copytree`, `shutil.rmtree`.
- `os.rename`, `os.remove`, `os.rmdir`, `os.makedirs`, `os.listdir`.
- `os.path.basename/dirname/splitext/join/exists`.
- Удаление — навсегда. Перед `rmtree` проверь путь.
'''),
    short=t(r'''
```py
import os, shutil

shutil.copy(src, dst)          # файл
shutil.copytree(src, dst)      # папка
shutil.move(src, dst)          # переместить
shutil.rmtree(folder)          # удалить папку целиком!
os.rename(old, new); os.remove(p); os.rmdir(empty)
os.makedirs(p, exist_ok=True); os.listdir(folder)

os.path.basename(p), os.path.dirname(p)
os.path.splitext(p)            # ('a/b', '.txt')
os.path.join("a", "b"), os.path.exists(p)
Path(p).unlink(missing_ok=True)
```
'''),
    quiz=[
        q('Чем удалить непустую папку?',
            ['`os.rmdir`', '`shutil.rmtree`', '`os.remove`', '`Path.unlink`'],
            1, 'rmdir работает только с пустыми.'),
        q('Что вернёт `os.path.splitext("a/b.tar.gz")`?',
            ["('a/b', '.tar.gz')", "('a/b.tar', '.gz')", "('b', 'tar.gz')", "('a', 'b.tar.gz')"],
            1, 'Отделяется только последнее расширение.'),
        q('Куда попадает файл после `os.remove`?',
            ['В корзину', 'Удаляется навсегда', 'В /tmp', 'В папку backup'],
            1, 'Восстановить его обычными средствами нельзя.'),
    ],
),

# ---------- fil-errors ----------
'fil-errors': dict(
    full=t(r'''
## Зачем это нужно

С файлами постоянно что-то идёт не так: файла нет, по пути лежит папка, нет прав, диск переполнен. Программа не должна падать с непонятной трассировкой — нужно ловить конкретные ошибки и сообщать, что случилось.

## Ошибки файловой системы

```python
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
```

- `FileNotFoundError` — файла или папки нет.
- `IsADirectoryError` — ожидали файл, а там папка.
- `FileExistsError` — файл уже есть (режим `"x"`, `mkdir` без `exist_ok`).
- `PermissionError` — нет прав.
- `NotADirectoryError` — ожидали папку, а там файл.
- Все они — наследники **`OSError`**: `except OSError` ловит их все.
- Вывод: `FileNotFoundError`, `IsADirectoryError`, `FileExistsError`.

## Что внутри ошибки

```python
try:
    open("missing/config.json", encoding="utf-8")
except FileNotFoundError as e:
    print(e.filename)
    print(e.strerror)
    print(isinstance(e, OSError))
```

- `e.filename` — путь, с которым была проблема; `e.strerror` — описание от системы.
- Вывод: `missing/config.json`, `No such file or directory`, `True`.

## Проверить заранее или попробовать

```python
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
```

- **LBYL** («look before you leap») — проверить `exists()`, потом действовать.
- **EAFP** («easier to ask forgiveness than permission») — просто попробовать и поймать ошибку.
- В Python предпочитают EAFP: между проверкой и открытием файл могут удалить, а `try` ловит и эту ситуацию, и нехватку прав.
- Вывод: `LBYL: файла нет`, `EAFP: файла нет`.

## Понятные сообщения

```python
import json

def load_config(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"нет конфига: {path}") from None
    except json.JSONDecodeError:
        raise ValueError(f"битый конфиг: {path}") from None

try:
    load_config("config.json")
except FileNotFoundError as e:
    print(e)
```

- Перехватываем низкоуровневую ошибку и выбрасываем свою, с понятным текстом.
- `from None` — не показывать исходную ошибку в трассировке (она уже «переведена»).
- `json.JSONDecodeError` — ошибка разбора JSON, наследник `ValueError`.
- Вывод: `нет конфига: config.json`.

## Атомарная запись

```python
import os

def safe_write(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)

safe_write("state.json", '{"v": 1}')
safe_write("state.json", '{"v": 2}')
with open("state.json", encoding="utf-8") as f:
    print(f.read(), os.path.exists("state.json.tmp"))
```

- Если программа упадёт посреди записи в `"w"`, файл останется **обрезанным** — старые данные уже стёрты, новые не дописаны.
- Решение: писать во временный файл, а потом одним действием подменить им исходный. `os.replace` заменяет файл целиком за одну операцию.
- Вывод: `{"v": 2} False`.

## Итог

- `FileNotFoundError`, `FileExistsError`, `IsADirectoryError`, `PermissionError` — все `OSError`.
- `e.filename`, `e.strerror`.
- EAFP (`try/except`) предпочтительнее проверки `exists()`.
- Свои понятные ошибки: `raise ... from None`.
- Важные файлы — через временный файл и `os.replace`.
'''),
    short=t(r'''
```py
try:
    with open(p, encoding="utf-8") as f:
        data = f.read()
except FileNotFoundError:      # нет файла
    data = ""
except IsADirectoryError: ...  # это папка
except PermissionError: ...    # нет прав
except OSError as e:           # всё остальное
    print(e.filename, e.strerror)

# атомарно:
open(p + ".tmp", "w").write(text); os.replace(p + ".tmp", p)
```
'''),
    quiz=[
        q('Какой общий родитель у `FileNotFoundError` и `PermissionError`?',
            ['ValueError', 'OSError', 'IOError нет', 'FileError'],
            1, 'Все ошибки файловой системы — OSError.'),
        q('Почему в Python предпочитают `try/except` проверке `exists()`?',
            ['Короче', 'Файл могут удалить между проверкой и открытием', 'exists() медленный', 'exists() не работает с папками'],
            1, 'Это подход EAFP.'),
        q('Зачем писать во временный файл и делать `os.replace`?',
            ['Быстрее', 'Чтобы при сбое не остался обрезанный файл', 'Так требует Windows', 'Для кодировки'],
            1, 'Замена происходит за одну операцию.'),
    ],
),

}
