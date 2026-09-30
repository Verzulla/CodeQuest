"""Тема «Файлы» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "fil"

EXPLAIN = {

# ===== Модуль 1. Чтение и запись =====

f"{P}-open-e1": x(
    idea="`open` возвращает файловый объект: `\"w\"` — запись, по умолчанию — чтение. После работы файл закрывают.",
    lines=[
        ('f = open("hello.txt", "w", encoding="utf-8")', "Создать или перезаписать."),
        ('f.write("Привет, файл!")', "Записали строку."),
        ("f.close()", "Закрыть — данные точно окажутся на диске."),
        ("text = f.read()", "Всё содержимое строкой."),
        ("print(text, len(text))", "13 символов, включая пробел и `!`."),
    ],
    mistake="Не закрыть файл после записи — при чтении он может оказаться пустым."),

f"{P}-open-e2": x(
    idea="`with` закрывает файл сам, когда блок закончился — даже при ошибке.",
    lines=[
        ('f.write("первая строка\\n")', "`\\n` пишем сами."),
        ("print(f.closed)", "Блок кончился — файл закрыт."),
        ("print(repr(f.read()))", "`repr` показывает `\\n`."),
    ],
    mistake="Ожидать `False`: переменная `f` жива, но файл уже закрыт."),

f"{P}-open-e3": x(
    idea="`\"w\"` стирает файл при открытии, `\"a\"` — дописывает в конец.",
    lines=[
        ('f.write("новое")', "Второе `\"w\"` стёрло «старое»."),
        ('with open("log.txt", "a", encoding="utf-8") as f:', "Дописывание."),
        ("print(f.read())", "Без пробела и переноса — их не писали."),
    ],
    mistake="Ожидать `старое` в файле."),

f"{P}-open-e4": x(
    idea="Запись: режим `\"w\"`, кодировка явно, `with` закроет файл.",
    lines=[
        ('with open(path, "w", encoding="utf-8") as f:', "Перезапись."),
        ("f.write(text)", "Строка целиком."),
    ],
    mistake="Не указать кодировку — на Windows кириллица запишется в cp1251."),

f"{P}-open-e5": x(
    idea="`return` внутри `with` безопасен — файл закроется при выходе.",
    lines=[
        ('with open(path, encoding="utf-8") as f:', "Режим по умолчанию — чтение."),
        ("return f.read()", "Всё содержимое."),
    ],
    mistake="Думать, что `return` оставит файл открытым."),

f"{P}-open-e6": x(
    idea="Режим `\"a\"` дописывает в конец и создаёт файл, если его нет.",
    lines=[
        ('with open(path, "a", encoding="utf-8") as f:', "Дописывание."),
        ('f.write(line + "\\n")', "Перевод строки добавляем сами."),
    ],
    mistake="`\"w\"` — сотрёт прежние строки."),

f"{P}-open-e7": x(
    idea="Прочитать один файл, записать в другой. `write` возвращает число записанных символов.",
    lines=[
        ("text = f.read()", "Содержимое источника."),
        ('with open(dst, "w", encoding="utf-8") as f:', "Второй `with` — после закрытия первого."),
        ("return f.write(text)", "Количество символов."),
    ],
    mistake="Считать `len` в байтах — просили символы."),

f"{P}-open-e8": x(
    idea="Нет файла — начинаем с нуля. Читаем, увеличиваем, записываем число как строку.",
    lines=[
        ("value = int(f.read())", "Файл хранит текст — переводим в число."),
        ("except FileNotFoundError:\n        value = 0", "Первый запуск."),
        ("value += 1", "Новое значение."),
        ("f.write(str(value))", "`write` принимает только строки."),
    ],
    mistake="`f.write(value)` — `TypeError`: нужна строка."),

f"{P}-read-e1": x(
    idea="Файл перебирается по строкам, каждая — вместе с `\\n` в конце.",
    lines=[
        ("for line in f:", "Строка за строкой, без загрузки всего файла."),
        ("print(repr(line))", "Видно `\\n`."),
    ],
    mistake="Ожидать строки без `\\n`."),

f"{P}-read-e2": x(
    idea="Файл читается с текущей позиции. `readline` — одна строка, `readlines` — остальные списком, дальше — пусто. `splitlines` убирает `\\n`.",
    lines=[
        ("print(repr(f.readline()))", "Первая строка."),
        ("print(f.readlines())", "Оставшиеся."),
        ("print(repr(f.read()))", "Конец файла — пустая строка."),
        ("print(f.read().splitlines())", "Новый `open` — снова с начала."),
    ],
    mistake="Ожидать, что `readlines` вернёт все строки после `readline`."),

f"{P}-read-e3": x(
    idea="`strip()` отбрасывает пустые строки и строки из пробелов. `int` сам терпит пробелы и `\\n` по краям.",
    lines=[
        ('f.write("  10 \\n\\n20\\n   \\n30")', "Пять строк, две пустые."),
        ("numbers = [int(line) for line in f if line.strip()]", "Фильтр пустых."),
    ],
    mistake="`int(\"\\n\")` без фильтра — `ValueError`."),

f"{P}-read-e4": x(
    idea="`splitlines()` делит по переводам строк и убирает их.",
    lines=[("return f.read().splitlines()", "Без `\\n`.")],
    mistake="`f.readlines()` — строки останутся с `\\n`."),

f"{P}-read-e5": x(
    idea="Перебор файла по строкам не загружает его в память целиком.",
    lines=[
        ("for line in f:", "Построчно."),
        ("if line.strip():\n                count += 1", "Строки из пробелов — пустые."),
    ],
    mistake="`if line:` — `\"\\n\"` непустая строка."),

f"{P}-read-e6": x(
    idea="`readline` читает одну строку; в конце файла — пустую строку.",
    lines=[("return f.readline().rstrip(\"\\n\")", "Убираем только перевод строки.")],
    mistake="`f.read().split(\"\\n\")[0]` — читает весь файл."),

f"{P}-read-e7": x(
    idea="`enumerate(f, start=1)` нумерует строки с единицы.",
    lines=[
        ("for number, line in enumerate(f, start=1):", "Номер и строка."),
        ('line = line.rstrip("\\n")', "Без перевода строки."),
        ("if word in line:\n                result.append((number, line))", "Кортеж."),
    ],
    mistake="Забыть `start=1` — нумерация с 0."),

f"{P}-read-e8": x(
    idea="Строки — число `\\n`, слова — `split()` по любым пробелам, символы — длина текста.",
    lines=[
        ("text = f.read()", "Всё сразу."),
        ('return {"lines": text.count("\\n"), "words": len(text.split()), "chars": len(text)}', "Как в `wc`."),
    ],
    mistake="`len(text.splitlines())` — последняя строка без `\\n` тоже посчитается."),

f"{P}-write-e1": x(
    idea="`write` и `writelines` не добавляют переводы строк. `write` возвращает число записанных символов.",
    lines=[
        ('f.writelines(["c", "d\\n", "e"])', "Склеивает как есть."),
        ('n = f.write("\\nконец")', "`\\n` + 5 букв = 6."),
        ("print(f.read().splitlines())", "`abcd`, `e`, `конец`."),
    ],
    mistake="Думать, что `writelines` пишет каждый элемент на новой строке."),

f"{P}-write-e2": x(
    idea="`print(..., file=f)` пишет в файл как на экран: с пробелами и `\\n`.",
    lines=[
        ('print("пройдено:", 5, file=f)', "Число само станет текстом."),
        ('print("упало:", 1, sep=" ", end="!\\n", file=f)', "`end` — свой конец строки."),
        ('print(f.read(), end="")', "Без лишней пустой строки."),
    ],
    mistake="Забыть, что `print` сам добавит `\\n`."),

f"{P}-write-e3": x(
    idea="Режим `\"x\"` создаёт новый файл; если файл уже есть — `FileExistsError`.",
    lines=[
        ('os.remove("once.txt")', "Удаляем от прошлых запусков."),
        ('with open("once.txt", "x", encoding="utf-8") as f:', "Создан."),
        ('open("once.txt", "x", encoding="utf-8")', "Второй раз — ошибка."),
    ],
    mistake="Ожидать перезапись, как с `\"w\"`."),

f"{P}-write-e4": x(
    idea="Каждой строке — свой `\\n`.",
    lines=[
        ("for line in lines:", "По одной."),
        ('f.write(line + "\\n")', "Перевод и после последней."),
    ],
    mistake="`\"\\n\".join(lines)` — после последней не будет `\\n`."),

f"{P}-write-e5": x(
    idea="`*row` распаковывает кортеж в аргументы `print`, `sep=\"\\t\"` ставит табуляции.",
    lines=[("print(*row, sep=\"\\t\", file=f)", "Значения — через табуляцию.")],
    mistake="`print(row, ...)` — запишется `(1, 2)` со скобками."),

f"{P}-write-e6": x(
    idea="`\"x\"` не даёт затереть существующий файл.",
    lines=[
        ('with open(path, "x", encoding="utf-8") as f:', "Только новый."),
        ("except FileExistsError:\n        return False", "Уже был."),
        ("return True", "Создан."),
    ],
    mistake="Проверять `exists`, потом открывать `\"w\"` — между проверкой и записью файл может появиться."),

f"{P}-write-e7": x(
    idea="Дописываем результаты; `True` считается как 1, поэтому `sum` значений — число прошедших.",
    lines=[
        ('with open(path, "a", encoding="utf-8") as f:', "Не стираем прошлые логи."),
        ('print("PASS" if ok else "FAIL", name, file=f)', "Статус и имя через пробел."),
        ('print(f"итого: {sum(results.values())}/{len(results)}", file=f)', "Прошло/всего."),
    ],
    mistake="Режим `\"w\"` — прошлые результаты пропадут."),

f"{P}-write-e8": x(
    idea="Прочитать, посчитать, заменить, записать обратно. Одновременно читать и писать один файл нельзя.",
    lines=[
        ("count = text.count(old)", "Сколько будет замен."),
        ("f.write(text.replace(old, new))", "Перезапись."),
    ],
    mistake="Открыть `\"w\"` до чтения — файл уже пуст."),

f"{P}-encoding-e1": x(
    idea="Строка — символы, `bytes` — байты. В UTF-8 кириллица занимает 2 байта, латиница — 1.",
    lines=[
        ('data = text.encode("utf-8")', "Строка → байты."),
        ("print(len(text), len(data))", "3 символа, 6 байт."),
        ('print(data.decode("utf-8"))', "Обратно в строку."),
        ('print(len("Code".encode("utf-8")))', "Латиница — 1 байт."),
    ],
    mistake="Считать, что символ всегда занимает байт."),

f"{P}-encoding-e2": x(
    idea="Читать нужно в той кодировке, в которой писали. `errors=\"replace\"` заменяет неразборчивые байты на `�`.",
    lines=[
        ('with open("ru.txt", "w", encoding="cp1251") as f:', "По байту на букву."),
        ("except UnicodeDecodeError:", "Эти байты — не UTF-8."),
        ('with open("ru.txt", encoding="cp1251") as f:', "Правильная кодировка."),
        ('print(f.read().count("\\ufffd"))', "Шесть букв — шесть замен."),
    ],
    mistake="Думать, что UTF-8 прочитает любой текст."),

f"{P}-encoding-e3": x(
    idea="Режимы `\"wb\"`/`\"rb\"` работают с `bytes`: без кодировки, индекс даёт число 0–255.",
    lines=[
        ("f.write(bytes([0, 1, 2, 255]))", "Байты из чисел."),
        ("print(content, len(content))", "Непечатные — как `\\x..`."),
        ("print(content[3], content[-2:])", "Индекс — число, срез — `bytes`."),
    ],
    mistake="Ожидать символ от `content[3]`."),

f"{P}-encoding-e4": x(
    idea="Размер в байтах — длина закодированной строки.",
    lines=[("return len(text.encode(\"utf-8\"))", "Не `len(text)`.")],
    mistake="`len(text)` — число символов."),

f"{P}-encoding-e5": x(
    idea="Читаем в одной кодировке — получаем строку; пишем в другой.",
    lines=[
        ("with open(src, encoding=from_enc) as f:", "Байты → строка."),
        ('with open(dst, "w", encoding=to_enc) as f:', "Строка → другие байты."),
    ],
    mistake="Копировать байты — кодировка не изменится."),

f"{P}-encoding-e6": x(
    idea="Пробуем UTF-8; не вышло — открываем заново в cp1251.",
    lines=[
        ('with open(path, encoding="utf-8") as f:\n            return f.read()', "Основной вариант."),
        ('except UnicodeDecodeError:\n        with open(path, encoding="cp1251") as f:\n            return f.read()', "Запасной."),
    ],
    mistake="Сначала cp1251 — он «прочитает» любые байты, но UTF-8-текст станет кракозябрами."),

f"{P}-encoding-e7": x(
    idea="Картинки и архивы копируют в двоичном режиме — никакого декодирования.",
    lines=[
        ('with open(src, "rb") as f:', "Байты."),
        ('with open(dst, "wb") as f:', "Байты."),
        ("return len(data)", "Размер в байтах."),
    ],
    mistake="Текстовый режим — `UnicodeDecodeError` на картинке."),

f"{P}-encoding-e8": x(
    idea="Тип файла определяют по первым байтам — «магическим числам», а не по расширению.",
    lines=[
        ("head = f.read(4)", "Только 4 байта."),
        ('if head.startswith(b"\\x89PNG"):', "Сравниваем с `bytes`."),
        ('if head.startswith(b"PK"):', "ZIP — два байта."),
        ('return "unknown"', "Остальное."),
    ],
    mistake="Сравнивать с `\"PK\"` — строка не равна `bytes`."),

# ===== Модуль 2. Пути и папки =====

f"{P}-path-e1": x(
    idea="`Path` разбирает путь на части: `name` — имя, `stem` — без расширения, `suffix` — расширение, `parent` — папка.",
    lines=[
        ("print(p.stem, p.suffix)", "Расширение — с точкой."),
        ("print(p.parent, p.parent.name)", "Папка и её имя."),
        ("print(p.parts)", "Кортеж частей."),
    ],
    mistake="Ожидать `html` без точки."),

f"{P}-path-e2": x(
    idea="Оператор `/` склеивает пути. `with_suffix`/`with_name` дают новый путь. `..` без обращения к диску не сокращается.",
    lines=[
        ('cfg = base / "config" / "settings.json"', "Склейка."),
        ('print(cfg.with_suffix(".yaml"))', "Замена расширения."),
        ('print(cfg.with_name("local.json"))', "Замена имени."),
        ('print(Path("a/b/../c").parts)', "`..` остаётся частью."),
    ],
    mistake="Ожидать `('a', 'c')`."),

f"{P}-path-e3": x(
    idea="`mkdir(exist_ok=True)` не падает, если папка есть. `exists`, `is_dir`, `is_file` проверяют диск.",
    lines=[
        ("folder.mkdir(exist_ok=True)", "Создать, если нет."),
        ('file.write_text("данные", encoding="utf-8")', "Открыть, записать, закрыть — одной строкой."),
        ("print(folder.exists(), folder.is_dir(), folder.is_file())", "Папка — не файл."),
    ],
    mistake="Думать, что `folder / \"нет.txt\"` создаёт файл."),

f"{P}-path-e4": x(
    idea="`suffix` — последнее расширение с точкой; приводим к нижнему регистру и убираем точку.",
    lines=[("return Path(filename).suffix.lower().lstrip(\".\")", "У `Makefile` суффикс пустой.")],
    mistake="`filename.split(\".\")[-1]` — для `Makefile` вернёт само имя."),

f"{P}-path-e5": x(
    idea="`PurePosixPath` всегда ставит `/`, независимо от системы.",
    lines=[("return str(PurePosixPath(base) / \"reports\" / date_str / f\"{name}.html\")", "Склейка и перевод в строку.")],
    mistake="Вернуть объект пути, а не строку."),

f"{P}-path-e6": x(
    idea="`with_suffix` заменяет расширение, папка сохраняется.",
    lines=[("return [str(PurePosixPath(name).with_suffix(new_ext)) for name in filenames]", "Для каждого имени.")],
    mistake="`name.replace(\".txt\", new_ext)` — не сработает для других расширений."),

f"{P}-path-e7": x(
    idea="Ключ — суффикс в нижнем регистре, значение — список имён без папок.",
    lines=[
        ("p = PurePosixPath(name)", "Разбор пути."),
        ("result.setdefault(p.suffix.lower(), []).append(p.name)", "Без расширения — ключ `\"\"`."),
    ],
    mistake="Добавлять `name` целиком — попадут папки."),

f"{P}-path-e8": x(
    idea="Пробелы → `_`, лишние символы выкидываем, длину ограничиваем до добавления расширения.",
    lines=[
        ('for ch in title.replace(" ", "_"):', "Сначала пробелы."),
        ('if ch.isalnum() or ch in "-_":', "`isalnum` пропускает и кириллицу."),
        ('return "".join(chars)[:50] + ".png"', "Обрезка до `.png`."),
    ],
    mistake="Обрезать после добавления `.png` — расширение может отрезаться."),

f"{P}-dirs-e1": x(
    idea="`parents=True` создаёт промежуточные папки. `iterdir` — содержимое одной папки, без вложенных.",
    lines=[
        ('(root / "src").mkdir(parents=True, exist_ok=True)', "Создаст и `proj`."),
        ("print(sorted(p.name for p in root.iterdir()))", "Заглавные буквы идут раньше строчных."),
        ('print((root / "src" / "app.py").read_text(encoding="utf-8"))', "Содержимое файла."),
    ],
    mistake="Ожидать `app.py` в списке — он во вложенной папке."),

f"{P}-dirs-e2": x(
    idea="`glob` ищет в одной папке, `rglob` — во всех вложенных. `js/*` совпадает и с папкой `lib`.",
    lines=[
        ('print(sorted(p.name for p in root.glob("*.html")))', "Только верхний уровень."),
        ('print(sorted(p.name for p in root.rglob("*.js")))', "И `js/lib/util.js`."),
        ('print(sorted(str(p.relative_to(root)) for p in root.glob("js/*")))', "`*` — и файлы, и папки."),
    ],
    mistake="Ожидать `util.js` от `glob(\"*.js\")` или без `lib` в последней строке."),

f"{P}-dirs-e3": x(
    idea="`stat().st_size` — размер в байтах. Кириллица в UTF-8 — 2 байта на букву.",
    lines=[
        ('(d / "b.txt").write_text("яя", encoding="utf-8")', "4 байта."),
        ("print(p.name, p.stat().st_size)", "Байты, не символы."),
        ("print(sum(p.stat().st_size for p in d.iterdir()))", "5 + 4."),
    ],
    mistake="Ожидать `b.txt 2`."),

f"{P}-dirs-e4": x(
    idea="`parents=True` создаст и `base`, `exist_ok=True` — повторный вызов без ошибки.",
    lines=[("(Path(base) / name).mkdir(parents=True, exist_ok=True)", "Оба флага.")],
    mistake="Без `exist_ok` — второй вызов упадёт."),

f"{P}-dirs-e5": x(
    idea="Фильтр по двум условиям: это файл и расширение совпадает.",
    lines=[("return sorted(p.name for p in Path(folder).iterdir() if p.is_file() and p.suffix == ext)", "Папка `x.log` не попадёт.")],
    mistake="Не проверить `is_file` — попадут папки с точкой в имени."),

f"{P}-dirs-e6": x(
    idea="`rglob` обходит все вложенные папки; `relative_to` отрезает корень, `as_posix` ставит `/`.",
    lines=[
        ("root = Path(root)", "Строку — в путь."),
        ('return sorted(p.relative_to(root).as_posix() for p in root.rglob("test_*.py"))', "Относительные пути."),
    ],
    mistake="`str(p)` — на Windows будут `\\`."),

f"{P}-dirs-e7": x(
    idea="`rglob(\"*\")` — всё содержимое; суммируем размеры только файлов.",
    lines=[("return sum(p.stat().st_size for p in Path(folder).rglob(\"*\") if p.is_file())", "Папки пропускаем.")],
    mistake="Складывать размеры папок — это служебные числа, не содержимое."),

f"{P}-dirs-e8": x(
    idea="Рекурсия: для папки — её строка и дерево её содержимого с отступом +2. Ключ сортировки `(не папка, имя)` ставит папки первыми.",
    lines=[
        ("items = sorted(Path(folder).iterdir(), key=lambda p: (not p.is_dir(), p.name))", "`False` < `True` — папки раньше."),
        ('lines.append(" " * indent + p.name + "/")', "Папка со слешем."),
        ("lines.extend(tree(p, indent + 2))", "Вложенное — глубже."),
        ('lines.append(" " * indent + p.name)', "Файл."),
    ],
    mistake="`append` вместо `extend` — внутрь попадёт список."),

f"{P}-os-e1": x(
    idea="`shutil.copy` копирует, `os.rename` переименовывает, `os.remove` удаляет файл. `os.listdir` — имена в папке.",
    lines=[
        ('os.makedirs("box/in", exist_ok=True)', "Папки с вложенными."),
        ('shutil.copy("box/in/a.txt", "box/b.txt")', "Копия."),
        ('os.rename("box/b.txt", "box/c.txt")', "b → c."),
        ('print(sorted(os.listdir("box")))', "`c.txt` и папка `in`."),
        ('os.remove("box/c.txt")', "Удалён."),
    ],
    mistake="Ожидать `b.txt` — после `rename` его нет."),

f"{P}-os-e2": x(
    idea="`os.path` работает со строками: `basename` — имя, `dirname` — папка, `splitext` — (без расширения, расширение), `join` — склейка.",
    lines=[
        ("print(os.path.basename(path), os.path.dirname(path))", "Имя и папка."),
        ("print(os.path.splitext(path))", "Путь остаётся в первой части."),
        ('print(os.path.join("a", "b", "c.txt").replace(os.sep, "/"))', "`join` ставит разделитель системы."),
        ('print(os.path.isabs("/etc/hosts"), os.path.isabs("etc/hosts"))', "Абсолютный — от корня."),
    ],
    mistake="Ожидать `('result', '.json')` — `splitext` не отрезает папки."),

f"{P}-os-e3": x(
    idea="`os.rmdir` удаляет только пустую папку; `shutil.rmtree` — со всем содержимым.",
    lines=[
        ('os.rmdir("trash")', "Не пуста — `OSError`."),
        ('shutil.rmtree("trash")', "Удалена целиком."),
        ('print(Path("trash").exists())', "Больше нет."),
    ],
    mistake="Пользоваться `rmtree` без оглядки — удаляет без корзины и без вопросов."),

f"{P}-os-e4": x(
    idea="Имя копии — исходное + `.bak`; `shutil.copy` копирует содержимое.",
    lines=[
        ('target = path + ".bak"', "config.json.bak."),
        ("shutil.copy(path, target)", "Копия."),
        ("return target", "Путь копии."),
    ],
    mistake="`os.rename` — оригинал исчезнет."),

f"{P}-os-e5": x(
    idea="Удалить файл — `Path.unlink()`. Папки и чужие расширения не трогаем.",
    lines=[
        ("if p.is_file() and p.suffix == ext:", "Только нужные файлы."),
        ("p.unlink()", "Удаление."),
        ("count += 1", "Счёт."),
    ],
    mistake="Удалять без `is_file` — `unlink` на папке упадёт."),

f"{P}-os-e6": x(
    idea="`shutil.move` переносит файл. Папку назначения создаём заранее.",
    lines=[
        ("Path(dst).mkdir(parents=True, exist_ok=True)", "Куда класть."),
        ('for p in sorted(Path(src).glob("*.log")):', "Только логи, по порядку."),
        ("shutil.move(str(p), str(Path(dst) / p.name))", "Перенос с тем же именем."),
        ("moved.append(p.name)", "Запоминаем имя."),
    ],
    mistake="`shutil.copy` — файлы останутся в `src`."),

f"{P}-os-e7": x(
    idea="Сначала папка, затем имя разделяем на основу и расширение.",
    lines=[
        ("folder = os.path.dirname(path)", "logs/2024."),
        ("stem, ext = os.path.splitext(os.path.basename(path))", "run и .log."),
    ],
    mistake="`splitext(path)` — в основе останется папка."),

f"{P}-os-e8": x(
    idea="Имена с датой сортируются хронологически. Удаляем всё, кроме последних `n`.",
    lines=[
        ("files = sorted((p for p in Path(folder).iterdir() if p.is_file()), key=lambda p: p.name)", "Старые — в начале."),
        ("to_delete = files[:max(len(files) - n, 0)]", "Лишние сначала; `max` на случай, когда файлов меньше `n`."),
        ("p.unlink()", "Удаление."),
    ],
    mistake="`files[:-n]` — при `n = 0` не удалится ничего вместо всех."),

f"{P}-errors-e1": x(
    idea="Все файловые ошибки — наследники `OSError`, у каждой своё имя по причине.",
    lines=[
        ('lambda: open("нет_такого.txt", encoding="utf-8"),', "Нет файла."),
        ('lambda: open("err_dir", encoding="utf-8"),', "Это папка."),
        ('lambda: Path("err_dir").mkdir(),', "Уже есть."),
        ("print(type(e).__name__)", "Конкретный класс."),
    ],
    mistake="Ожидать `OSError` в выводе — печатается реальный класс."),

f"{P}-errors-e2": x(
    idea="В ошибке есть подробности: `filename` — путь, `strerror` — описание от системы.",
    lines=[
        ("print(e.filename)", "Путь из `open`."),
        ("print(e.strerror)", "Текст системы."),
        ("print(isinstance(e, OSError))", "Наследник."),
    ],
    mistake="Ожидать только имя файла без папки."),

f"{P}-errors-e3": x(
    idea="LBYL — проверить заранее, EAFP — попробовать и поймать ошибку. В Python чаще второе: между проверкой и открытием файл может исчезнуть.",
    lines=[
        ("if os.path.exists(path):\n    os.remove(path)", "Гарантируем, что файла нет."),
        ("if os.path.exists(path):", "LBYL."),
        ("except FileNotFoundError:", "EAFP."),
    ],
    mistake="Думать, что одно сработает, а другое — нет."),

f"{P}-errors-e4": x(
    idea="Нет файла — значение по умолчанию.",
    lines=[
        ('with open(path, encoding="utf-8") as f:\n            return f.read()', "Есть файл."),
        ("except FileNotFoundError:\n        return default", "Нет файла."),
    ],
    mistake="`except OSError` — спрячет и «нет прав», и «это папка»."),

f"{P}-errors-e5": x(
    idea="Переводим технические ошибки в понятные. `from None` скрывает исходную цепочку.",
    lines=[
        ("return json.load(f)", "Разбор прямо из файла."),
        ('raise FileNotFoundError(f"нет конфига: {path}") from None', "Своё сообщение."),
        ('raise ValueError(f"битый конфиг: {path}") from None', "`JSONDecodeError` → `ValueError`."),
    ],
    mistake="Без `from None` — в выводе будет длинная цепочка из двух ошибок."),

f"{P}-errors-e6": x(
    idea="Ошибка одного файла не мешает остальным: `try` — внутри цикла.",
    lines=[
        ("for path in paths:", "По одному."),
        ("data[path] = f.read()", "Прочитан."),
        ("except OSError:\n            errors.append(path)", "Любая файловая ошибка."),
        ("return data, errors", "Кортеж."),
    ],
    mistake="`try` вокруг цикла — первая ошибка остановит всё."),

f"{P}-errors-e7": x(
    idea="Атомарная запись: пишем во временный файл, затем одной операцией подменяем исходный.",
    lines=[
        ('tmp = path + ".tmp"', "Временное имя рядом."),
        ("f.write(text)", "Сбой здесь не тронет оригинал."),
        ("os.replace(tmp, path)", "Подмена — одним шагом."),
    ],
    mistake="Писать сразу в `path` — при сбое файл останется полупустым."),

f"{P}-errors-e8": x(
    idea="Сначала исключаем папку, потом создаём файл при отсутствии, в конце читаем.",
    lines=[
        ("if p.is_dir():", "Папка — ошибка."),
        ('raise IsADirectoryError(f"{path} — это папка")', "Понятное сообщение."),
        ("p.parent.mkdir(parents=True, exist_ok=True)", "Папки по пути."),
        ('p.write_text(default_text, encoding="utf-8")', "Файл по умолчанию."),
        ('return p.read_text(encoding="utf-8")', "Содержимое."),
    ],
    mistake="Проверять только `exists` — для папки он тоже `True`."),

# ===== Модуль 3. Форматы и практика =====

f"{P}-csv-e1": x(
    idea="`csv.writer` сам берёт в кавычки значения с запятой, `csv.reader` снимает их. Всё читается строками.",
    lines=[
        ('with open("scores.csv", "w", encoding="utf-8", newline="") as f:', "`newline=\"\"` — обязательно для csv."),
        ("csv.writer(f).writerows(rows)", "Числа станут текстом."),
        ("print(row)", "`'90'` — строка."),
    ],
    mistake="Ожидать `90` числом после чтения."),

f"{P}-csv-e2": x(
    idea="`DictReader` берёт заголовок из первой строки; каждая строка — словарь. Значения — строки.",
    lines=[
        ("print(reader.fieldnames)", "Заголовки."),
        ('print(row["name"], row["active"] == "yes", type(row["id"]).__name__)', "`id` — строка."),
    ],
    mistake="Ожидать `int` у `id`."),

f"{P}-csv-e3": x(
    idea="`DictWriter` пишет словари в порядке `fieldnames`; `writeheader` — строка заголовка; `delimiter` меняет разделитель.",
    lines=[
        ('writer = csv.DictWriter(f, fieldnames=["id", "name"], delimiter=";")', "Колонки и разделитель."),
        ("writer.writeheader()", "id;name."),
        ("writer.writerows(users)", "По строке на словарь."),
    ],
    mistake="Забыть `writeheader` — не будет заголовка."),

f"{P}-csv-e4": x(
    idea="Заголовок — `writerow`, данные — `writerows`.",
    lines=[
        ('with open(path, "w", encoding="utf-8", newline="") as f:', "Без `newline` на Windows — пустые строки между записями."),
        ("writer.writerow(header)", "Одна строка."),
        ("writer.writerows(rows)", "Все остальные."),
    ],
    mistake="`writerows(header)` — каждая буква станет строкой."),

f"{P}-csv-e5": x(
    idea="`DictReader` даёт строки — числовые поля переводим `int`.",
    lines=[
        ('{"id": int(row["id"]), "name": row["name"], "age": int(row["age"])}', "Новый словарь с числами."),
        ("for row in csv.DictReader(f)", "Строка за строкой."),
    ],
    mistake="Возвращать генератор после закрытия файла — читать будет уже нечего."),

f"{P}-csv-e6": x(
    idea="Собираем непустые значения колонки как числа и считаем среднее.",
    lines=[
        ("values = [float(row[column]) for row in csv.DictReader(f) if row[column].strip()]", "Пустые ячейки пропускаем."),
        ("if not values:\n        return None", "Делить на ноль нельзя."),
        ("return round(sum(values) / len(values), 2)", "Среднее."),
    ],
    mistake="Не пропустить пустые — `float(\"\")` упадёт."),

f"{P}-csv-e7": x(
    idea="`extrasaction=\"ignore\"` — лишние ключи не вызывают ошибку.",
    lines=[
        ('writer = csv.DictWriter(f, fieldnames=["test", "status", "duration"], delimiter=";", extrasaction="ignore")', "Колонки, разделитель, игнор лишнего."),
        ("writer.writeheader()", "Заголовок."),
    ],
    mistake="Без `extrasaction` — `ValueError` на первом лишнем ключе."),

f"{P}-csv-e8": x(
    idea="Считаем падения по сьютам, затем сортируем пары по убыванию и собираем словарь.",
    lines=[
        ('if row["status"] == "failed":', "Только падения."),
        ('counts[row["suite"]] = counts.get(row["suite"], 0) + 1', "Счётчик."),
        ("return dict(sorted(counts.items(), key=lambda kv: -kv[1]))", "По убыванию количества."),
    ],
    mistake="Считать все сьюты — появятся нули."),

f"{P}-logs-e1": x(
    idea="Перебор файла идёт строка за строкой — память не зависит от размера файла.",
    lines=[
        ("f.write(f\"{i} {'ERROR' if i % 5_000 == 0 else 'INFO'} событие\\n\")", "ERROR на 5000, 10000, 15000, 20000."),
        ('if " ERROR " in line:', "С пробелами — именно слово."),
    ],
    mistake="Посчитать 5 — `range(1, 20_001)` не включает 25000."),

f"{P}-logs-e2": x(
    idea="Генератор над файлом выдаёт по одному значению. `next` берёт только первое.",
    lines=[
        ('if line.startswith("ERROR"):', "Только ошибки."),
        ('yield line.split(" ", 1)[1].strip()', "Текст после уровня."),
        ('print(next(errors("app.log")))', "Новый генератор — с начала."),
    ],
    mistake="Ожидать `сеть` от `next` — это новый генератор."),

f"{P}-logs-e3": x(
    idea="`deque(maxlen=3)` хранит только последние три элемента — хвост файла без загрузки всего.",
    lines=[
        ("last = deque(f, maxlen=3)", "Старые строки вытесняются."),
        ("print([line.strip() for line in last])", "8, 9, 10."),
    ],
    mistake="Ожидать первые три строки."),

f"{P}-logs-e4": x(
    idea="Первое слово — уровень; считаем через `get`.",
    lines=[
        ("if not line.strip():\n                continue", "Пустые пропускаем."),
        ("level = line.split()[0]", "Первое слово."),
        ("counts[level] = counts.get(level, 0) + 1", "Счётчик."),
    ],
    mistake="`split()[0]` у пустой строки — `IndexError`."),

f"{P}-logs-e5": x(
    idea="`yield` внутри `with`: файл открыт, пока генератор работает.",
    lines=[
        ("for line in f:", "Построчно."),
        ('if "ERROR" in line:', "Фильтр."),
        ('yield line.rstrip("\\n")', "Без перевода строки."),
    ],
    mistake="`return [...]` — это список, а не генератор."),

f"{P}-logs-e6": x(
    idea="`deque(f, maxlen=n)` проходит файл и держит только последние `n` строк.",
    lines=[("return [line.rstrip(\"\\n\") for line in deque(f, maxlen=n)]", "Хвост без `\\n`.")],
    mistake="`f.readlines()[-n:]` — весь файл в памяти."),

f"{P}-logs-e7": x(
    idea="Разбиваем строку на 4 поля, время — число без `ms`.",
    lines=[
        ("method, url, status, took = line.split()", "Четыре части."),
        ('ms = int(took.removesuffix("ms"))', "153ms → 153."),
        ("if ms > limit_ms:", "Медленные."),
        ("return sorted(result, key=lambda r: -r[2])", "По убыванию времени."),
    ],
    mistake="`took.strip(\"ms\")` — сработает, но удаляет любые `m` и `s` по краям."),

f"{P}-logs-e8": x(
    idea="Каждые `lines_per_part` строк закрываем текущую часть и открываем следующую.",
    lines=[
        ("if i % lines_per_part == 0:", "Начало новой части."),
        ("if out:\n                    out.close()", "Предыдущую — закрыть."),
        ('out = open(f"{path}.part{part}", "w", encoding="utf-8")', "Новый файл."),
        ("out.write(line)", "Строка в текущую часть."),
        ("if out:\n        out.close()", "Последнюю — тоже закрыть."),
    ],
    mistake="Забыть закрыть последнюю часть — её конец может не записаться."),

f"{P}-temp-e1": x(
    idea="`TemporaryDirectory` удаляет папку со всем содержимым при выходе из `with`.",
    lines=[
        ("with tempfile.TemporaryDirectory() as tmp:", "Путь к новой папке."),
        ("print([p.name for p in folder.iterdir()])", "Внутри блока файл есть."),
        ("print(saved.exists())", "После блока папки нет."),
    ],
    mistake="Думать, что сохранённый путь сохранит и папку."),

f"{P}-temp-e2": x(
    idea="`StringIO` — «файл» в памяти: в него можно писать и из него читать.",
    lines=[
        ('print("строка 2", file=buf)', "`print` пишет туда же."),
        ("print(repr(buf.getvalue()))", "Всё записанное."),
        ('fake = io.StringIO("a\\nb\\nc\\n")', "Готовый «файл» для чтения."),
    ],
    mistake="Читать `buf.read()` после записи — позиция в конце, результат пуст."),

f"{P}-temp-e3": x(
    idea="Функция, принимающая файловый объект, работает и с настоящим файлом, и со `StringIO` — это удобно тестировать.",
    lines=[
        ("return sum(1 for _ in csv.DictReader(f))", "Строки без заголовка."),
        ("print(count_rows(data))", "Две строки данных."),
        ("print(count_rows(f))", "Три строки."),
    ],
    mistake="Считать заголовок строкой."),

f"{P}-temp-e4": x(
    idea="Принимаем объект, а не путь — функцию легко проверить через `StringIO`.",
    lines=[("return sum(float(line) for line in f if line.strip())", "Пустые пропускаем.")],
    mistake="Вызывать `open(f)` — `f` уже открыт."),

f"{P}-temp-e5": x(
    idea="Собираем текст через `print(..., file=buf)` и забираем `getvalue()`.",
    lines=[
        ("buf = io.StringIO()", "Пустой буфер."),
        ('print("✓" if ok else "✗", name, file=buf)', "Строка отчёта."),
        ("return buf.getvalue()", "Весь текст."),
    ],
    mistake="`buf.read()` — вернёт пустую строку."),

f"{P}-temp-e6": x(
    idea="Все файлы — во временной папке; при выходе из `with` она исчезнет.",
    lines=[
        ('path = Path(tmp) / "data.txt"', "Файл во временной папке."),
        ('path.write_text("".join(line + "\\n" for line in lines), encoding="utf-8")', "Каждая строка с `\\n`."),
        ('return path.read_text(encoding="utf-8").splitlines()', "Читаем до удаления папки."),
    ],
    mistake="Читать после `with` — файла уже нет."),

f"{P}-temp-e7": x(
    idea="`StringIO` превращает строку в файловый объект — `DictReader` его понимает.",
    lines=[("return list(csv.DictReader(io.StringIO(text)))", "Список словарей.")],
    mistake="`csv.DictReader(text)` — переберёт символы строки."),

f"{P}-temp-e8": x(
    idea="Два файла в одном `with`: читаем построчно и сразу пишем результат.",
    lines=[
        ('with open(src, encoding="utf-8") as fin, open(dst, "w", encoding="utf-8") as fout:', "Оба закроются."),
        ('fout.write(transform(line.rstrip("\\n")) + "\\n")', "Без `\\n` в функцию, с `\\n` в файл."),
    ],
    mistake="Передавать строку с `\\n` в `transform`."),

f"{P}-config-e1": x(
    idea="Разбор .env: пропуск пустых и комментариев, деление по первому `=`, снятие кавычек.",
    lines=[
        ('if not line or line.startswith("#"):\n            continue', "Пусто или комментарий."),
        ('key, value = line.split("=", 1)', "`abc=123` не разрежется."),
        ("settings[key.strip()] = value.strip().strip('\"')", "Пробелы и кавычки."),
    ],
    mistake="`split(\"=\")` без ограничения — ошибка распаковки на TOKEN."),

f"{P}-config-e2": x(
    idea="`configparser` читает INI: секции и ключи. `getint`/`getboolean` переводят типы, `fallback` — значение по умолчанию.",
    lines=[
        ("print(config.sections())", "Секции."),
        ('print(config["api"]["url"], config.getint("api", "timeout") + 1)', "5 → число."),
        ('print(config.getboolean("ui", "headless"), config.get("ui", "window", fallback="1920x1080"))', "`yes` → True; ключа нет — fallback."),
    ],
    mistake="`config[\"api\"][\"timeout\"] + 1` — это строка."),

f"{P}-config-e3": x(
    idea="Тестовые данные в JSON-файле: один тест прогоняется на всех случаях.",
    lines=[
        ('cases = json.loads(Path("testdata/users.json").read_text(encoding="utf-8"))', "Список словарей."),
        ('status = login(case["login"], case["password"])', "Пустой пароль — 400."),
        ('print(case["login"], "PASS" if status == case["expected"] else "FAIL")', "Оба совпали с ожиданием."),
    ],
    mistake="Считать guest проваленным — 400 и есть ожидаемый ответ."),

f"{P}-config-e4": x(
    idea="Разбор по строкам: пропуски, первый `=`, очистка.",
    lines=[
        ("line = line.strip()", "Без пробелов и `\\n`."),
        ('if not line or line.startswith("#"):\n                continue', "Пропуск."),
        ('key, value = line.split("=", 1)', "По первому `=`."),
        ("result[key.strip()] = value.strip().strip(\"\\\"'\")", "Снять оба вида кавычек."),
    ],
    mistake="Снимать кавычки до `strip()` — пробелы помешают."),

f"{P}-config-e5": x(
    idea="Типизированные геттеры с `fallback`.",
    lines=[
        ('"url": config.get("api", "url"),', "Строка."),
        ('"timeout": config.getint("api", "timeout", fallback=10),', "Число или 10."),
        ('"headless": config.getboolean("ui", "headless", fallback=False),', "yes/no/true/1 → bool."),
    ],
    mistake="`bool(config.get(...))` — `\"no\"` станет `True`."),

f"{P}-config-e6": x(
    idea="Базовый конфиг + локальные переопределения через `update`; нет локального — ничего страшного.",
    lines=[
        ("config = json.load(f)", "Базовый."),
        ("config.update(json.load(f))", "Локальный поверх."),
        ("except FileNotFoundError:\n        pass", "Нет — пропускаем."),
    ],
    mistake="`try` вокруг обоих файлов — пропажа базового тоже будет скрыта."),

f"{P}-config-e7": x(
    idea="`glob(\"*.json\")` отбирает нужные файлы, `stem` — имя без расширения.",
    lines=[
        ('for p in sorted(Path(folder).glob("*.json")):', "По имени."),
        ('result.append((p.stem, json.loads(p.read_text(encoding="utf-8"))))', "Пара."),
    ],
    mistake="`p.name` — останется `.json`."),

f"{P}-config-e8": x(
    idea="Подбираем свободное имя: пока файл есть — пробуем следующий номер.",
    lines=[
        ("folder.mkdir(parents=True, exist_ok=True)", "Папка."),
        ('path = folder / f"{test_name}.png"', "Первый вариант."),
        ('while path.exists():\n        path = folder / f"{test_name}_{n}.png"\n        n += 1', "_2, _3, …"),
        ("path.write_bytes(data)", "Байты скриншота."),
        ("return path.name", "Только имя."),
    ],
    mistake="`write_text` — скриншот не текст."),
}
