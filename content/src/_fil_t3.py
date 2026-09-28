"""Теория модуля «Форматы и практика» темы «Файлы».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- fil-csv ----------
'fil-csv': dict(
    full=t(r'''
## Зачем это нужно

**CSV** (comma-separated values) — таблица в текстовом файле: строка — запись, значения разделены запятыми. В CSV выгружают отчёты, результаты тестов, тестовые данные; его открывает Excel. Разбирать CSV через `split(",")` нельзя: значение может само содержать запятую. Для этого есть модуль `csv`.

## writer и reader

```python
import csv

rows = [["name", "score"], ["Аня", 90], ["Боря, мл.", 85]]
with open("scores.csv", "w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerows(rows)

with open("scores.csv", encoding="utf-8") as f:
    print(f.read(), end="")

with open("scores.csv", encoding="utf-8", newline="") as f:
    for row in csv.reader(f):
        print(row)
```

- `newline=""` в `open` — обязательно для CSV: модуль сам управляет переводами строк. Без этого в Windows появятся пустые строки между записями.
- `csv.writer(f)` — объект для записи; `writerow(список)` — одна строка, `writerows(список_списков)` — много.
- Значение с запятой автоматически взято в **кавычки**: `"Боря, мл."`.
- `csv.reader(f)` — перебор строк, каждая — **список строк**. Числа тоже читаются строками (`'90'`)!
- Вывод: `name,score`, `Аня,90`, `"Боря, мл.",85`, `['name', 'score']`, `['Аня', '90']`, `['Боря, мл.', '85']`.

## DictReader: строки как словари

```python
import csv

with open("users.csv", "w", encoding="utf-8", newline="") as f:
    f.write("id,name,active\n1,Аня,yes\n2,Боря,no\n")

with open("users.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    print(reader.fieldnames)
    for row in reader:
        print(row["name"], row["active"] == "yes", type(row["id"]).__name__)
```

- `DictReader` берёт первую строку как заголовок, а каждую следующую отдаёт словарём «колонка → значение».
- Обращаться по имени колонки удобнее и надёжнее, чем по индексу.
- `fieldnames` — список колонок.
- Вывод: `['id', 'name', 'active']`, `Аня True str`, `Боря False str`.

## Преобразование типов

```python
import csv
import io

text = "id,name,age\n1,Аня,30\n2,Боря,25\n"
users = [
    {"id": int(r["id"]), "name": r["name"], "age": int(r["age"])}
    for r in csv.DictReader(io.StringIO(text))
]
print(users)
print(sum(u["age"] for u in users))
```

- Всё из CSV — строки, числа переводим сами.
- `io.StringIO(text)` — «файл» из строки (подробно — в уроке про временные файлы).
- Вывод: `[{'id': 1, 'name': 'Аня', 'age': 30}, {'id': 2, 'name': 'Боря', 'age': 25}]`, `55`.

## DictWriter и разделитель

```python
import csv

users = [{"id": 1, "name": "Аня"}, {"id": 2, "name": "Боря"}]
with open("out.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name"], delimiter=";")
    writer.writeheader()
    writer.writerows(users)

with open("out.csv", encoding="utf-8") as f:
    print(f.read().splitlines())
```

- `DictWriter(f, fieldnames=[...])` — запись словарей; `fieldnames` задаёт порядок колонок.
- `writeheader()` — записать строку заголовка.
- `delimiter=";"` — другой разделитель. Русский Excel по умолчанию ждёт `;`.
- `extrasaction="ignore"` — не падать, если в словаре есть лишние ключи.
- Вывод: `['id;name', '1;Аня', '2;Боря']`.

## Excel и кодировка

Чтобы Excel в Windows правильно показал кириллицу из CSV, используют кодировку `"utf-8-sig"` — она добавляет в начало файла специальную метку (BOM).

## Итог

- `open(..., newline="", encoding="utf-8")` для CSV.
- `csv.writer` / `csv.reader` — списки; `DictWriter` / `DictReader` — словари.
- Все значения читаются строками.
- `delimiter=";"`, `extrasaction="ignore"`, `"utf-8-sig"` для Excel.
'''),
    short=t(r'''
```py
import csv

with open(p, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "name"], delimiter=";")
    w.writeheader()
    w.writerows(rows)                 # список словарей

with open(p, encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):     # словари, значения — str
        int(row["id"])

csv.writer(f).writerow([1, "a"]); csv.reader(f)   # списки
```
'''),
    quiz=[
        q('Почему CSV нельзя разбирать через `line.split(",")`?',
            ['Медленно', 'Значения могут содержать запятые в кавычках', 'split не работает с файлами', 'Можно'],
            1, 'Модуль csv учитывает кавычки.'),
        q('Какого типа значения возвращает `csv.DictReader`?',
            ['Разных типов', 'Только строки', 'Только числа', 'bytes'],
            1, 'Преобразования — вручную.'),
        q('Зачем `newline=""` при открытии CSV?',
            ['Для кодировки', 'Чтобы модуль csv сам управлял переводами строк', 'Чтобы убрать заголовок', 'Не нужно'],
            1, 'Иначе в Windows появляются пустые строки.'),
    ],
),

# ---------- fil-logs ----------
'fil-logs': dict(
    full=t(r'''
## Зачем это нужно

Логи серверов бывают на гигабайты. `f.read()` на таком файле займёт всю память, и программа упадёт. Большие файлы обрабатывают **построчно** — в памяти одновременно только одна строка. Это основной навык при разборе логов после падения тестов.

## Перебор не загружает файл целиком

```python
with open("big.log", "w", encoding="utf-8") as f:
    for i in range(1, 20_001):
        f.write(f"{i} {'ERROR' if i % 5_000 == 0 else 'INFO'} событие\n")

errors = 0
with open("big.log", encoding="utf-8") as f:
    for line in f:
        if " ERROR " in line:
            errors += 1
print(errors)
```

- `for line in f` читает файл блоками и отдаёт по строке. Память не зависит от размера файла.
- `20_001` — подчёркивание в числе для читаемости.
- Вывод: `4`.

## Генератор над файлом

```python
with open("app.log", "w", encoding="utf-8") as f:
    f.write("INFO старт\nERROR база\nWARN диск\nERROR сеть\nINFO стоп\n")

def errors(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("ERROR"):
                yield line.split(" ", 1)[1].strip()

print(list(errors("app.log")))
print(next(errors("app.log")))
```

- `yield` превращает функцию в **генератор**: она отдаёт значения по одному, когда их просят (подробно — в теме «Генераторы»).
- Файл читается только до тех пор, пока нужны значения: `next(...)` прочитал лишь две строки.
- `split(" ", 1)[1]` — всё после первого пробела.
- Вывод: `['база', 'сеть']`, `база`.

## Подсчёт по уровням

```python
with open("app.log", "w", encoding="utf-8") as f:
    f.write("INFO a\nERROR b\n\nINFO c\nWARN d\nERROR e\n")

counts = {}
with open("app.log", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        level = line.split()[0]
        counts[level] = counts.get(level, 0) + 1
print(counts)
```

- `line.split()[0]` — первое слово строки.
- Пустые строки пропускаем, иначе `split()[0]` упадёт с `IndexError`.
- Вывод: `{'INFO': 2, 'ERROR': 2, 'WARN': 1}`.

## Последние строки

```python
from collections import deque

with open("tail.log", "w", encoding="utf-8") as f:
    for i in range(1, 11):
        f.write(f"строка {i}\n")

with open("tail.log", encoding="utf-8") as f:
    last = deque(f, maxlen=3)
print([line.strip() for line in last])
```

- `deque(итерируемое, maxlen=3)` — очередь, которая хранит только 3 последних элемента: новые вытесняют старые.
- Файл перебирается целиком, но в памяти — максимум 3 строки. Это аналог команды `tail -n 3`.
- Вывод: `['строка 8', 'строка 9', 'строка 10']`.

## Разбор строк лога доступа

```python
with open("access.log", "w", encoding="utf-8") as f:
    f.write("GET /api/users 200 153ms\nPOST /api/login 200 950ms\nGET /health 200 3ms\n")

slow = []
with open("access.log", encoding="utf-8") as f:
    for line in f:
        method, url, status, took = line.split()
        ms = int(took.removesuffix("ms"))
        if ms > 100:
            slow.append((url, ms))
print(sorted(slow, key=lambda r: -r[1]))
```

- Распаковка `method, url, status, took = line.split()` — строка из 4 слов в 4 переменные.
- `removesuffix("ms")` — убрать окончание, если оно есть.
- Вывод: `[('/api/login', 950), ('/api/users', 153)]`.

## Итог

- Большие файлы — только `for line in f`, не `read()`.
- Генератор с `yield` — ленивая обработка.
- `deque(f, maxlen=n)` — последние n строк.
- Пропускай пустые строки перед `split()[0]`.
'''),
    short=t(r'''
```py
with open(p, encoding="utf-8") as f:
    for line in f:              # построчно, память ~ одна строка
        if not line.strip():
            continue
        level = line.split()[0]

def errors(p):                  # ленивый генератор
    with open(p, encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line:
                yield line.rstrip("\n")

from collections import deque
deque(open(p, encoding="utf-8"), maxlen=10)   # хвост
```
'''),
    quiz=[
        q('Как обработать лог на 10 ГБ?',
            ['`f.read()`', '`f.readlines()`', '`for line in f`', 'Нельзя'],
            2, 'Построчно, не загружая целиком.'),
        q('Что хранит `deque(f, maxlen=3)` после перебора файла?',
            ['Первые 3 строки', 'Последние 3 строки', 'Весь файл', '3 случайные строки'],
            1, 'Новые элементы вытесняют старые.'),
        q('Почему перед `line.split()[0]` пропускают пустые строки?',
            ['Для скорости', 'Иначе IndexError', 'Иначе KeyError', 'Не нужно'],
            1, 'split() пустой строки — пустой список.'),
    ],
),

# ---------- fil-temp ----------
'fil-temp': dict(
    full=t(r'''
## Зачем это нужно

Тестам часто нужны файлы: проверить функцию, которая читает конфиг или пишет отчёт. Создавать их в папке проекта плохо: они мешают, конфликтуют между тестами и остаются мусором. Решения: **временные папки**, которые удаляются сами, и **файлы в памяти** — `io.StringIO`.

## Временная папка

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    folder = Path(tmp)
    (folder / "data.txt").write_text("временно", encoding="utf-8")
    print([p.name for p in folder.iterdir()])
    saved = folder
print(saved.exists())
```

- `tempfile.TemporaryDirectory()` создаёт пустую папку в системном месте для временных файлов (например, `/tmp`) с уникальным именем.
- `as tmp` — путь к ней строкой.
- После выхода из `with` папка удаляется **со всем содержимым**.
- Вывод: `['data.txt']`, `False`.
- В pytest то же даёт фикстура `tmp_path`: `def test_x(tmp_path): (tmp_path / "a.txt").write_text(...)`.

## StringIO: файл в памяти

```python
import io

buf = io.StringIO()
buf.write("строка 1\n")
print("строка 2", file=buf)
print(repr(buf.getvalue()))

fake = io.StringIO("a\nb\nc\n")
print([line.strip() for line in fake])
```

- `io.StringIO()` — объект, который ведёт себя как открытый текстовый файл, но хранит данные в памяти.
- Работают `write`, `print(file=...)`, `read`, перебор строк.
- `getvalue()` — всё записанное одной строкой.
- `io.StringIO("текст")` — «файл» с заранее заданным содержимым — для чтения.
- Для байтов есть `io.BytesIO`.
- Вывод: `'строка 1\nстрока 2\n'`, `['a', 'b', 'c']`.

## Функции, принимающие файл, а не путь

```python
import io
import csv

def count_rows(f):
    return sum(1 for _ in csv.DictReader(f))

print(count_rows(io.StringIO("id,name\n1,Аня\n2,Боря\n")))

with open("real.csv", "w", encoding="utf-8", newline="") as f:
    f.write("id\n1\n2\n3\n")
with open("real.csv", encoding="utf-8", newline="") as f:
    print(count_rows(f))
```

- Функция получает **открытый файлоподобный объект**. Ей всё равно, настоящий это файл или `StringIO` — важны методы (утиная типизация).
- В тестах передаём `StringIO` — без файлов на диске. В бою — настоящий файл.
- `sum(1 for _ in ...)` — посчитать элементы.
- Вывод: `2`, `3`.

## Разбор CSV из ответа API

```python
import csv
import io

body = "id,status\n1,passed\n2,failed\n"
rows = list(csv.DictReader(io.StringIO(body)))
print([r["status"] for r in rows])
```

- API вернул CSV строкой — оборачиваем в `StringIO` и разбираем модулем `csv`, не сохраняя на диск.
- Вывод: `['passed', 'failed']`.

## Два файла в одном with

```python
from pathlib import Path

Path("in.txt").write_text("аня\nборя\n", encoding="utf-8")
with open("in.txt", encoding="utf-8") as fin, open("out.txt", "w", encoding="utf-8") as fout:
    for line in fin:
        fout.write(line.upper())
print(Path("out.txt").read_text(encoding="utf-8").splitlines())
```

- В одном `with` можно открыть несколько файлов через запятую — закроются оба.
- Вывод: `['АНЯ', 'БОРЯ']`.

## Итог

- `tempfile.TemporaryDirectory()` — папка, которая удалится сама; в pytest — `tmp_path`.
- `io.StringIO` — текстовый файл в памяти, `getvalue()`; `io.BytesIO` — для байтов.
- Функции лучше писать так, чтобы они принимали открытый файл, — их легко тестировать.
'''),
    short=t(r'''
```py
import tempfile, io
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp) / "a.txt"      # удалится после with
    p.write_text("x", encoding="utf-8")

buf = io.StringIO()              # файл в памяти
print("строка", file=buf)
buf.getvalue()
csv.DictReader(io.StringIO(text))
# pytest: def test_x(tmp_path): ...
with open(a) as fin, open(b, "w") as fout: ...
```
'''),
    quiz=[
        q('Что происходит с `TemporaryDirectory` после выхода из `with`?',
            ['Остаётся', 'Удаляется со всем содержимым', 'Очищается, но остаётся', 'Переносится в корзину'],
            1, 'Мусора после тестов не остаётся.'),
        q('Что такое `io.StringIO`?',
            ['Строка с методами upper', 'Текстовый «файл» в памяти', 'Модуль для кодировок', 'Сетевое соединение'],
            1, 'Поддерживает write, read, перебор строк.'),
        q('Как получить всё записанное в `StringIO`?',
            ['`buf.read_all()`', '`buf.getvalue()`', '`str(buf)`', '`buf.text`'],
            1, 'getvalue() возвращает всё содержимое.'),
    ],
),

# ---------- fil-config ----------
'fil-config': dict(
    full=t(r'''
## Зачем это нужно

Адрес стенда, таймауты, браузер, логины тестовых пользователей не пишут прямо в коде тестов — их выносят в **конфиги** и **файлы тестовых данных**. Тогда один и тот же набор тестов запускают на разных стендах, меняя только файл. Самые частые форматы — `.env`, `.ini` и JSON.

## .env-файл

```python
env_text = """# настройки
BASE_URL=https://api.test
TIMEOUT = 5

TOKEN="abc=123"
"""
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
```

- `.env` — строки `КЛЮЧ=значение`; `#` — комментарий.
- `split("=", 1)` — разрезать только по **первому** `=`: в значении (токене) могут быть свои `=`.
- `strip('"')` — снять кавычки вокруг значения.
- Все значения — строки: `TIMEOUT` нужно перевести в число самим.
- В проектах для этого есть библиотека `python-dotenv`, а секреты в `.env` **не коммитят** в git.
- Вывод: `{'BASE_URL': 'https://api.test', 'TIMEOUT': '5', 'TOKEN': 'abc=123'}`.

## INI-файлы и configparser

```python
import configparser

with open("settings.ini", "w", encoding="utf-8") as f:
    f.write("[api]\nurl = https://api.test\ntimeout = 5\n\n[ui]\nbrowser = chrome\nheadless = yes\n")

config = configparser.ConfigParser()
config.read("settings.ini", encoding="utf-8")
print(config.sections())
print(config["api"]["url"], config.getint("api", "timeout") + 1)
print(config.getboolean("ui", "headless"), config.get("ui", "window", fallback="1920x1080"))
```

- INI — файл с **секциями** в квадратных скобках и парами `ключ = значение`. Такой формат у `pytest.ini`, `setup.cfg`, `tox.ini`.
- `config.read(путь)` — прочитать; если файла нет — молча ничего не прочитает.
- `config["секция"]["ключ"]` — строка.
- `getint`, `getfloat`, `getboolean` — с преобразованием. `getboolean` понимает `yes/no`, `true/false`, `on/off`, `1/0`.
- `fallback=` — значение, если ключа нет.
- Вывод: `['api', 'ui']`, `https://api.test 6`, `True 1920x1080`.

## JSON-конфиг с локальным переопределением

```python
import json

with open("default.json", "w", encoding="utf-8") as f:
    json.dump({"url": "http://prod", "timeout": 10}, f)
with open("local.json", "w", encoding="utf-8") as f:
    json.dump({"url": "http://localhost"}, f)

with open("default.json", encoding="utf-8") as f:
    config = json.load(f)
try:
    with open("local.json", encoding="utf-8") as f:
        config.update(json.load(f))
except FileNotFoundError:
    pass
print(config)
```

- Общие настройки лежат в репозитории, а локальные (у каждого свои) — в отдельном файле, который перекрывает общие.
- `dict.update` — значения из второго словаря заменяют первые.
- Вывод: `{'url': 'http://localhost', 'timeout': 10}`.

## Тестовые данные в файлах

```python
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
```

- Данные отделены от логики: добавить новый случай — дописать строку в JSON, код теста не меняется.
- В pytest такие списки передают в `@pytest.mark.parametrize`.
- Вывод: `admin PASS`, `guest PASS`.

## Итог

- `.env`: строки `KEY=value`, делить по первому `=`, значения — строки.
- `configparser`: секции, `getint`/`getboolean`, `fallback`.
- JSON-конфиги: общий + локальный через `update`.
- Тестовые данные — в отдельных файлах; секреты — не в git.
'''),
    short=t(r'''
```py
# .env
key, value = line.split("=", 1)
value.strip().strip("\"'")

import configparser
c = configparser.ConfigParser()
c.read("settings.ini", encoding="utf-8")
c["api"]["url"]
c.getint("api", "timeout", fallback=10)
c.getboolean("ui", "headless", fallback=False)   # yes/no/true/1

config = json.load(f_default); config.update(json.load(f_local))
```
'''),
    quiz=[
        q('Почему строку `.env` делят через `split("=", 1)`?',
            ['Так быстрее', 'В значении тоже может быть знак =', 'split без 1 не работает', 'Чтобы убрать пробелы'],
            1, 'Токены часто содержат =.'),
        q('Что вернёт `config.getboolean("ui", "headless")` для `headless = yes`?',
            ['"yes"', 'True', '1', 'Ошибку'],
            1, 'configparser понимает yes/no, true/false, on/off, 1/0.'),
        q('Где хранить пароли и токены для тестов?',
            ['В коде теста', 'В .env или переменных окружения, не в git', 'В README', 'В названии теста'],
            1, 'Секреты не коммитят.'),
    ],
),

}
