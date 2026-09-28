"""Теория модуля «Чтение и запись» темы «Файлы».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- fil-open ----------
'fil-open': dict(
    full=t(r'''
## Зачем это нужно

Всё, что хранится между запусками программы, лежит в файлах: логи, отчёты тестов, конфиги, тестовые данные, скриншоты. Переменные исчезают, когда программа завершается, а файл остаётся. Работа с файлом всегда идёт по схеме: **открыть → читать или писать → закрыть**.

## open, write, read, close

```python
f = open("hello.txt", "w", encoding="utf-8")
f.write("Привет, файл!")
f.close()

f = open("hello.txt", encoding="utf-8")
text = f.read()
f.close()
print(text, len(text))
```

Что делает каждая строка:

- `open(путь, режим, encoding=...)` — открыть файл и получить объект-файл `f`. Путь без папок — файл в текущей рабочей папке.
- `"w"` — режим записи (write). Если файла нет — он создаётся.
- `encoding="utf-8"` — в какой кодировке хранить русские буквы. Пиши **всегда** (подробно — в уроке про кодировки).
- `f.write(строка)` — записать текст.
- `f.close()` — закрыть файл. Только после этого данные гарантированно попадают на диск, а файл освобождается для других программ.
- `open("hello.txt", encoding="utf-8")` — без режима файл открывается на **чтение** (`"r"`).
- `f.read()` — прочитать всё содержимое в одну строку.
- Вывод: `Привет, файл! 13`.

## with: файл закроется сам

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("первая строка\n")
    f.write("вторая строка\n")
print(f.closed)

with open("notes.txt", encoding="utf-8") as f:
    print(repr(f.read()))
```

- `with open(...) as f:` — открыть файл и положить его в `f` на время блока.
- Когда блок заканчивается — **даже из-за ошибки** — файл закрывается автоматически. Забыть `close()` невозможно.
- `f.closed` — закрыт ли файл.
- `write` **не** добавляет перевод строки — `\n` пишем сами.
- `repr(...)` показывает строку с кавычками и `\n`.
- Вывод: `True`, `'первая строка\nвторая строка\n'`.
- Правило: **всегда открывай файлы через `with`**.

## Режимы открытия

```python
with open("log.txt", "w", encoding="utf-8") as f:
    f.write("старое")
with open("log.txt", "w", encoding="utf-8") as f:
    f.write("новое")
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("+ещё")
with open("log.txt", encoding="utf-8") as f:
    print(f.read())
```

- `"r"` — чтение (по умолчанию). Файла нет → `FileNotFoundError`.
- `"w"` — запись. **Существующий файл сразу очищается!** Старое содержимое теряется.
- `"a"` — дозапись (append): новое добавляется в конец.
- `"x"` — создать новый файл; если он уже есть → `FileExistsError`.
- К любому режиму можно добавить `b` (двоичный) или `+` (чтение и запись), например `"rb"`, `"r+"`.
- Вывод: `новое+ещё`.

## Прочитать, изменить, записать

```python
with open("count.txt", "w", encoding="utf-8") as f:
    f.write("41")

with open("count.txt", encoding="utf-8") as f:
    value = int(f.read())
with open("count.txt", "w", encoding="utf-8") as f:
    f.write(str(value + 1))

with open("count.txt", encoding="utf-8") as f:
    print(f.read())
```

- В файл пишутся только **строки**: число переводим через `str()`, при чтении — обратно через `int()`.
- Нельзя открыть файл на `"w"` и сразу прочитать из него старое — он уже очищен. Поэтому сначала читаем, потом записываем.
- Вывод: `42`.

## Итог

- `with open(путь, режим, encoding="utf-8") as f:` — всегда так.
- `"r"` читать, `"w"` перезаписать, `"a"` дописать, `"x"` создать новый.
- `f.read()` — всё содержимое; `f.write(s)` — записать (без автоматического `\n`).
- В текстовый файл пишутся только строки.
'''),
    short=t(r'''
```py
with open("a.txt", "w", encoding="utf-8") as f:   # перезаписать
    f.write("текст\n")                             # \n сам

with open("a.txt", "a", encoding="utf-8") as f:   # дописать
    f.write("ещё\n")

with open("a.txt", encoding="utf-8") as f:        # прочитать
    text = f.read()
# "r" читать · "w" очистить и писать · "a" в конец · "x" только новый
```
'''),
    quiz=[
        q('Что происходит с существующим файлом при открытии в режиме `"w"`?',
            ['Дописывается', 'Очищается', 'Ошибка', 'Открывается на чтение'],
            1, 'Для дозаписи нужен режим "a".'),
        q('Зачем открывать файл через `with`?',
            ['Быстрее', 'Файл закроется автоматически, даже при ошибке', 'Иначе нельзя писать', 'Для кодировки'],
            1, 'Не нужно помнить про close().'),
        q('Добавляет ли `f.write("a")` перевод строки?',
            ['Да', 'Нет', 'Только в режиме "a"', 'Только в Windows'],
            1, '\\n нужно писать самому.'),
    ],
),

# ---------- fil-read ----------
'fil-read': dict(
    full=t(r'''
## Зачем это нужно

Логи, списки пользователей, CSV — это текст из множества строк. Часто нужно обработать файл **построчно**: найти ошибки, посчитать строки, взять заголовок. Есть несколько способов прочитать строки — у каждого свои особенности.

## Перебор строк в цикле

```python
with open("list.txt", "w", encoding="utf-8") as f:
    f.write("яблоко\nгруша\nслива\n")

with open("list.txt", encoding="utf-8") as f:
    for line in f:
        print(repr(line))
```

- Файловый объект можно перебирать в `for`: каждая итерация — одна строка.
- Строка приходит **вместе с `\n`** в конце (кроме, возможно, последней).
- Такой перебор читает файл по кусочкам — подходит для файлов любого размера.
- Вывод: `'яблоко\n'`, `'груша\n'`, `'слива\n'`.

## Убрать \n

```python
with open("list.txt", "w", encoding="utf-8") as f:
    f.write("яблоко\nгруша\nслива\n")

with open("list.txt", encoding="utf-8") as f:
    for line in f:
        print(line.rstrip("\n"), len(line.rstrip("\n")))
```

- `line.rstrip("\n")` — убрать перевод строки справа. `line.strip()` уберёт ещё и пробелы с обеих сторон.
- Если не убрать `\n`, `print(line)` напечатает пустые строки между строками, а сравнение `line == "груша"` не сработает.
- Вывод: `яблоко 6`, `груша 5`, `слива 5`.

## readline, readlines, read и курсор

```python
with open("list.txt", "w", encoding="utf-8") as f:
    f.write("a\nb\nc\n")

with open("list.txt", encoding="utf-8") as f:
    print(repr(f.readline()))
    print(f.readlines())
    print(repr(f.read()))

with open("list.txt", encoding="utf-8") as f:
    print(f.read().splitlines())
```

- `readline()` — одна следующая строка (с `\n`). В конце файла — пустая строка `''`.
- `readlines()` — список **оставшихся** строк (с `\n`).
- У открытого файла есть **курсор** — позиция, до которой уже прочитано. Каждое чтение сдвигает его. После `readlines()` читать больше нечего — `read()` вернул `''`.
- `read().splitlines()` — самый удобный способ получить список строк **без** `\n`.
- Вывод: `'a\n'`, `['b\n', 'c\n']`, `''`, `['a', 'b', 'c']`.

## Пустые строки и числа

```python
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("  10 \n\n20\n   \n30")

with open("data.txt", encoding="utf-8") as f:
    numbers = [int(line) for line in f if line.strip()]
print(numbers, sum(numbers))
```

- `if line.strip()` — пропустить строки из одних пробелов и пустые (`strip()` даёт `""`, а это ложь).
- `int(" 10 \n")` сам игнорирует пробелы и `\n` по краям.
- Вывод: `[10, 20, 30] 60`.

## Номера строк

```python
with open("app.log", "w", encoding="utf-8") as f:
    f.write("INFO старт\nERROR база\nINFO ок\n")

with open("app.log", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        if "ERROR" in line:
            print(number, line.rstrip("\n"))
```

- `enumerate(f, start=1)` — нумерация строк с единицы, как в редакторе.
- Вывод: `2 ERROR база`.

## Какой способ выбрать

- `for line in f` — большие файлы, построчная обработка.
- `f.read()` — небольшой файл целиком одной строкой.
- `f.read().splitlines()` — небольшой файл списком строк без `\n`.
- `f.readline()` — только первая строка (заголовок).

## Итог

- `for line in f:` — строки по одной, с `\n`.
- `line.rstrip("\n")` / `line.strip()` — убрать перевод строки.
- `readline()`, `readlines()`, `read()`; курсор двигается только вперёд.
- `read().splitlines()` — список строк без `\n`.
'''),
    short=t(r'''
```py
with open(p, encoding="utf-8") as f:
    for line in f:                  # по одной, с \n
        line = line.rstrip("\n")

    f.readline()                    # следующая строка
    f.readlines()                   # оставшиеся списком (с \n)

lines = open(p, encoding="utf-8").read().splitlines()   # без \n
for n, line in enumerate(f, start=1): ...
if line.strip(): ...                # не пустая
```
'''),
    quiz=[
        q('Что будет в конце строки при `for line in f`?',
            ['Ничего', 'Символ \\n', 'Пробел', 'Точка'],
            1, 'Убирай через rstrip("\\n") или strip().'),
        q('Что вернёт `f.read()` после `f.readlines()`?',
            ['Весь файл', 'Пустую строку', 'Ошибку', 'Последнюю строку'],
            1, 'Курсор уже в конце файла.'),
        q('Какой способ подходит для файла на несколько гигабайт?',
            ['`f.read()`', '`f.readlines()`', '`for line in f`', '`f.read().splitlines()`'],
            2, 'Он не загружает файл в память целиком.'),
    ],
),

# ---------- fil-write ----------
'fil-write': dict(
    full=t(r'''
## Зачем это нужно

Программа пишет в файлы отчёты, логи, результаты тестов, экспорт данных. Есть несколько способов записи, и важно помнить, кто добавляет переводы строк и что происходит со старым содержимым.

## write и writelines

```python
with open("w.txt", "w", encoding="utf-8") as f:
    f.write("a")
    f.write("b")
    f.writelines(["c", "d\n", "e"])
    n = f.write("\nконец")
print(n)
with open("w.txt", encoding="utf-8") as f:
    print(f.read().splitlines())
```

- `write(строка)` пишет строку как есть и возвращает количество записанных символов.
- `writelines(список)` пишет строки подряд — **без** разделителей и `\n`. Название обманчиво!
- Всё, что пишется в одном `with`, идёт подряд: `"a" + "b" + "c" + "d\n" + ...`.
- Вывод: `6`, `['abcd', 'e', 'конец']`.

## Список строк в файл

```python
lines = ["первая", "вторая", "третья"]
with open("lines.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")

with open("lines.txt", encoding="utf-8") as f:
    print(repr(f.read()))
```

- Добавляем `\n` после каждой строки сами.
- Альтернатива: `f.write("\n".join(lines) + "\n")`.
- Вывод: `'первая\nвторая\nтретья\n'`.

## print в файл

```python
with open("report.txt", "w", encoding="utf-8") as f:
    print("Отчёт", file=f)
    print("пройдено:", 5, file=f)
    print("упало:", 1, sep=" ", end="!\n", file=f)
with open("report.txt", encoding="utf-8") as f:
    print(f.read(), end="")
```

- `print(..., file=f)` — всё как обычный `print` (пробелы между аргументами, `\n` в конце, любые типы), но в файл.
- Удобно для отчётов: не нужно вручную переводить числа в строки и добавлять `\n`.
- `sep` и `end` работают как обычно.
- Вывод: `Отчёт`, `пройдено: 5`, `упало: 1!`.

## Дозапись

```python
with open("results.log", "w", encoding="utf-8") as f:
    pass
for run in range(1, 4):
    with open("results.log", "a", encoding="utf-8") as f:
        print(f"запуск {run}: ok", file=f)
with open("results.log", encoding="utf-8") as f:
    print(f.read().splitlines())
```

- `with open(..., "w") as f: pass` — создать пустой файл (или очистить существующий).
- Режим `"a"` при каждом открытии дописывает в конец — так растут логи.
- Вывод: `['запуск 1: ok', 'запуск 2: ok', 'запуск 3: ok']`.

## Только новый файл: режим "x"

```python
import os

if os.path.exists("once.txt"):
    os.remove("once.txt")
with open("once.txt", "x", encoding="utf-8") as f:
    f.write("создан")
try:
    open("once.txt", "x", encoding="utf-8")
except FileExistsError:
    print("файл уже есть")
```

- `"x"` защищает от случайной перезаписи: если файл существует — `FileExistsError`.
- `os.path.exists(путь)` — есть ли файл; `os.remove(путь)` — удалить (подробно — в уроке про os).
- Вывод: `файл уже есть`.

## Замена текста в файле

```python
with open("cfg.txt", "w", encoding="utf-8") as f:
    f.write("host=dev\nurl=http://dev/api\n")

with open("cfg.txt", encoding="utf-8") as f:
    text = f.read()
with open("cfg.txt", "w", encoding="utf-8") as f:
    f.write(text.replace("dev", "prod"))

with open("cfg.txt", encoding="utf-8") as f:
    print(f.read().splitlines())
```

- «Изменить файл на месте» = прочитать целиком, изменить строку, записать обратно.
- Вывод: `['host=prod', 'url=http://prod/api']`.

## Итог

- `write(s)` — как есть; `writelines(list)` — подряд, без `\n`.
- `print(..., file=f)` — удобная запись с пробелами и `\n`.
- `"a"` — дописать, `"x"` — только новый.
- Изменение файла: прочитать → изменить → перезаписать.
'''),
    short=t(r'''
```py
with open(p, "w", encoding="utf-8") as f:
    f.write("строка\n")              # вернёт кол-во символов
    f.writelines(["a\n", "b\n"])     # \n не добавляет!
    print("итого:", 5, file=f)       # как print, но в файл

open(p, "a", ...)                    # дописать
open(p, "x", ...)                    # FileExistsError, если есть
"\n".join(lines) + "\n"
```
'''),
    quiz=[
        q('Что запишет `f.writelines(["a", "b"])`?',
            ['a\\nb\\n', 'ab', "['a', 'b']", 'a b'],
            1, 'Разделители не добавляются.'),
        q('Как записать в файл строку с числом без ручного `str()`?',
            ['`f.write(5)`', '`print("итого:", 5, file=f)`', '`f.writelines(5)`', 'Никак'],
            1, 'print сам переводит аргументы в строки.'),
        q('Что делает режим `"x"`?',
            ['Удаляет файл', 'Создаёт только новый файл, иначе ошибка', 'Открывает на чтение и запись', 'Дописывает'],
            1, 'Защита от перезаписи.'),
    ],
),

# ---------- fil-encoding ----------
'fil-encoding': dict(
    full=t(r'''
## Зачем это нужно

Компьютер хранит в файле не буквы, а **байты** — числа от 0 до 255. **Кодировка** — правило, по которому буквы превращаются в байты и обратно. Если записать файл в одной кодировке, а прочитать в другой, получится ошибка или «кракозябры». Картинки, архивы и PDF — вообще не текст, их читают как байты.

## Строка и байты

```python
text = "Код"
data = text.encode("utf-8")
print(len(text), len(data))
print(data)
print(data.decode("utf-8"))
print(len("Code".encode("utf-8")))
```

- `str` — текст из символов, `bytes` — последовательность байтов. Байтовая строка записывается как `b'...'`.
- `encode(кодировка)` — текст → байты, `decode(кодировка)` — байты → текст.
- **UTF-8** — самая распространённая кодировка: латиница — 1 байт, кириллица — 2, эмодзи — 4.
- `\xd0\x9a` — байт в шестнадцатеричной записи: байты, которые не являются печатными ASCII-символами, показываются так.
- Вывод: `3 6`, `b'\xd0\x9a\xd0\xbe\xd0\xb4'`, `Код`, `4`.

## Почему всегда encoding="utf-8"

- Без `encoding` Python берёт кодировку **системы**. На Linux и macOS это UTF-8, а на Windows часто `cp1251`. Код, который работает у тебя, упадёт у коллеги или на CI-сервере.
- Поэтому в `open` для текстовых файлов **всегда** указывай `encoding="utf-8"`.

## Не та кодировка

```python
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
    print(f.read().count("�"))
```

- `cp1251` — старая кодировка Windows для кириллицы. В ней каждая буква — 1 байт.
- Прочитать такие байты как UTF-8 не получится → `UnicodeDecodeError`.
- Правильная кодировка при чтении — и текст на месте.
- `errors="replace"` — не падать, а заменять нераспознанные байты символом `�` (`�`). Шесть байт — шесть замен.
- Вывод: `ошибка декодирования`, `Привет`, `6`.

## Двоичный режим

```python
with open("data.bin", "wb") as f:
    f.write(bytes([0, 1, 2, 255]))
    f.write(b"OK")

with open("data.bin", "rb") as f:
    content = f.read()
print(content, len(content))
print(content[3], content[-2:])
print(type(content).__name__)
```

- `"wb"`, `"rb"` — запись и чтение **байтов**. `encoding` в двоичном режиме не указывают.
- `bytes([0, 1, 2, 255])` — байты из списка чисел.
- Индекс байтовой строки даёт **число** (`255`), срез — снова `bytes`.
- Так читают и копируют картинки, архивы, PDF.
- Вывод: `b'\x00\x01\x02\xffOK' 6`, `255 b'OK'`, `bytes`.

## Магические числа

```python
with open("pic.png", "wb") as f:
    f.write(b"\x89PNG\r\n\x1a\n" + bytes(10))

with open("pic.png", "rb") as f:
    head = f.read(4)
print(head, head == b"\x89PNG")
```

- `f.read(n)` — прочитать только `n` байт (или символов в текстовом режиме).
- Многие форматы начинаются с фиксированных байтов: PNG — `\x89PNG`, PDF — `%PDF`, ZIP — `PK`. По ним проверяют, что скачанный файл действительно картинка, а не HTML-страница с ошибкой.
- Вывод: `b'\x89PNG' True`.

## Итог

- Текст (`str`) ↔ байты (`bytes`): `encode` / `decode`.
- Для текстовых файлов всегда `encoding="utf-8"`.
- Не та кодировка → `UnicodeDecodeError`; `errors="replace"` — заменить нераспознанное.
- `"rb"` / `"wb"` — двоичные файлы, без `encoding`.
'''),
    short=t(r'''
```py
"Код".encode("utf-8")          # b'\xd0\x9a\xd0\xbe\xd0\xb4'
b"...".decode("utf-8")         # → str
len(s.encode("utf-8"))         # размер в байтах

open(p, encoding="utf-8")      # всегда указывать!
open(p, encoding="cp1251")     # старые Windows-файлы
open(p, encoding="utf-8", errors="replace")

with open(p, "rb") as f:       # байты: картинки, архивы
    head = f.read(4)
```
'''),
    quiz=[
        q('Сколько байт занимает `"абв"` в UTF-8?',
            ['3', '6', '9', '12'],
            1, 'Кириллица — 2 байта на букву.'),
        q('Почему в `open` нужно указывать `encoding="utf-8"`?',
            ['Иначе ошибка всегда', 'Кодировка по умолчанию зависит от системы', 'Так быстрее', 'Для двоичных файлов'],
            1, 'На Windows по умолчанию часто cp1251.'),
        q('Какой режим нужен для копирования картинки?',
            ['"r" и "w"', '"rb" и "wb"', '"a"', '"x"'],
            1, 'Картинка — не текст.'),
    ],
),

}
