"""Тема «Включения (comprehensions)» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "cmp"

EXPLAIN = {

# ===== Модуль 1. От цикла к включению =====

f"{P}-m1-l1-e1": x(
    idea="Списковое включение `[выражение for x in коллекция]` — короткая запись цикла с `append`.",
    lines=[
        ("for n in range(5):\n    squares.append(n * n)", "Длинная версия."),
        ("print([n * n for n in range(5)])", "То же одной строкой."),
    ],
    mistake="Думать, что включение даёт другой результат, чем цикл."),

f"{P}-m1-l1-e2": x(
    idea="Включение создаёт **новый** список; исходный не меняется.",
    lines=[
        ("print([w.upper() for w in words])", "Преобразование каждого слова."),
        ("print(words)", "Исходный список прежний."),
    ],
    mistake="Ожидать, что `words` станет заглавным."),

f"{P}-m1-l1-e3": x(
    idea="Включение работает с любой коллекцией; `_` — переменная, которая не нужна.",
    lines=[
        ('print([x for x in "abc"])', "Символы строки."),
        ("print([0 for _ in range(3)])", "Три нуля."),
        ("print([str(i) for i in [1, 2]])", "Строки `'1'`, `'2'`."),
    ],
    mistake="Ответить `[1, 2]` в последней строке — это уже строки."),

f"{P}-m1-l1-e4": x(
    idea="Выражение `n * 2` применяется к каждому элементу.",
    lines=[
        ("return [n * 2 for n in nums]", "`[2, 4, 6]`."),
    ],
    mistake="`[nums * 2]` — повтор всего списка."),

f"{P}-m1-l1-e5": x(
    idea="В выражении может быть вызов функции.",
    lines=[
        ("return [len(w) for w in words]", "Длины."),
    ],
    mistake="`len(words)` — это количество слов."),

f"{P}-m1-l1-e6": x(
    idea="Цикл с `append` сворачивается во включение.",
    lines=[
        ("return [str(x) for x in items]", "Каждый элемент — строкой."),
    ],
    mistake="`str(items)` — строка всего списка."),

f"{P}-m1-l1-e7": x(
    idea="Источник — `range` от 1 до `n` включительно.",
    lines=[
        ("return [i * i for i in range(1, n + 1)]", "`n + 1` — чтобы `n` вошло."),
    ],
    mistake="`range(n)` — начнётся с 0."),

f"{P}-m1-l1-e8": x(
    idea="Константу-префикс склеиваем с каждым путём.",
    lines=[
        ("return [BASE + p for p in paths]", "Полные адреса."),
    ],
    mistake="Забыть, что путь уже начинается с `/` — второй слэш не нужен."),

# ===== Фильтр: if в конце =====

f"{P}-m1-l2-e1": x(
    idea="`if` в конце включения — фильтр: элемент попадает в результат, только если условие истинно.",
    lines=[
        ("print([n for n in nums if n > 0])", "0 не больше нуля."),
        ("print([n * 10 for n in nums if n < 0])", "Фильтр и преобразование вместе."),
    ],
    mistake="Включить 0 в положительные."),

f"{P}-m1-l2-e2": x(
    idea="Два `if` подряд в конце — то же, что `and`.",
    lines=[
        ("print([n for n in range(20) if n % 2 == 0 if n % 3 == 0])", "Делятся на 2 и на 3."),
    ],
    mistake="Думать, что второй `if` работает как `or`."),

f"{P}-m1-l2-e3": x(
    idea="`strip()` превращает строку из пробелов в пустую, а пустая строка ложна.",
    lines=[
        ("print([w for w in words if w.strip()])", "Остаются непустые."),
        ("print(len([w for w in words if not w.strip()]))", "`\"\"` и `\"  \"` — 2."),
    ],
    mistake="Считать `\"  \"` непустой."),

f"{P}-m1-l2-e4": x(
    idea="Фильтр по остатку.",
    lines=[
        ("return [n for n in nums if n % 2 == 0]", "Чётные."),
    ],
    mistake="`n % 2` без `== 0` — останутся нечётные."),

f"{P}-m1-l2-e5": x(
    idea="Фильтр по условию `>= 400`.",
    lines=[
        ("return [c for c in codes if c >= 400]", "404 и 500."),
    ],
    mistake="`> 400` — потеряется 400."),

f"{P}-m1-l2-e6": x(
    idea="Фильтр отбирает, выражение преобразует.",
    lines=[
        ("return [w.upper() for w in words if len(w) > n]", "Длинные — заглавными."),
    ],
    mistake="Проверять длину после `upper()` — не ошибка, но порядок чтения «сначала отобрать» понятнее."),

f"{P}-m1-l2-e7": x(
    idea="Два условия через `and` в фильтре.",
    lines=[
        ("return [i for i in range(1, n + 1) if i % a == 0 and i % b == 0]", "6, 12, 18, 24, 30."),
    ],
    mistake="`or` — пройдут кратные хотя бы одному."),

f"{P}-m1-l2-e8": x(
    idea="Пару можно распаковать прямо в `for` включения.",
    lines=[
        ('return [name for name, status in results if status == "fail"]', "`pay`."),
    ],
    mistake="Вернуть пары целиком."),

# ===== Условное выражение в результате =====

f"{P}-m1-l3-e1": x(
    idea="`A if условие else B` **в начале** включения выбирает значение для каждого элемента — ничего не выбрасывая.",
    lines=[
        ('print(["+" if n > 0 else "-" for n in nums])', "0 → `-`."),
        ("print([n if n >= 0 else 0 for n in nums])", "Отрицательные → 0."),
    ],
    mistake="Ожидать, что 0 превратится в `+`."),

f"{P}-m1-l3-e2": x(
    idea="`if` в конце — фильтр (меньше элементов), `if-else` в начале — выбор значения (столько же элементов).",
    lines=[
        ("print([n for n in nums if n % 2 == 0])", "Два элемента."),
        ("print([n if n % 2 == 0 else None for n in nums])", "Четыре, нечётные заменены."),
    ],
    mistake="Путать позицию условия."),

f"{P}-m1-l3-e3": x(
    idea="Можно и выбирать значение, и фильтровать одновременно.",
    lines=[
        ('print(["client" if c < 500 else "server" for c in codes if c >= 400])', "Сначала фильтр ≥ 400, потом выбор."),
    ],
    mistake="Посчитать 200 и 301 — фильтр их убрал."),

f"{P}-m1-l3-e4": x(
    idea="Выбор строки для каждого числа.",
    lines=[
        ('return ["чёт" if n % 2 == 0 else "нечет" for n in nums]', "Длина результата = длине входа."),
    ],
    mistake="Поставить условие в конец — `else` там не бывает."),

f"{P}-m1-l3-e5": x(
    idea="Замена значений, а не отбор.",
    lines=[
        ("return [n if n >= 0 else 0 for n in nums]", "−1 → 0."),
    ],
    mistake="`[n for n in nums if n >= 0]` — отрицательные пропадут, а нужно заменить."),

f"{P}-m1-l3-e6": x(
    idea="Иконка для каждого статуса.",
    lines=[
        ('return ["✅" if s == "pass" else "❌" for s in statuses]', "`skip` тоже ❌."),
    ],
    mistake="Отфильтровать не-pass вместо замены."),

f"{P}-m1-l3-e7": x(
    idea="Вложенные условные выражения читаются слева направо — первое подходящее условие выигрывает. Самое строгое (15) — первым.",
    lines=[
        ('return ["FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else i for i in range(1, n + 1)]', "Иначе — само число."),
    ],
    mistake="Проверить 3 раньше 15 — вместо `FizzBuzz` будет `Fizz`."),

f"{P}-m1-l3-e8": x(
    idea="Результат сравнения — уже `True`/`False`, его можно класть в список.",
    lines=[
        ("return [c >= 500 for c in codes if c >= 400]", "404 → `False`, 503 → `True`."),
    ],
    mistake="Писать `True if c >= 500 else False` — лишнее."),

# ===== Функции, методы, enumerate, zip =====

f"{P}-m1-l4-e1": x(
    idea="В выражении включения — любые методы и функции.",
    lines=[
        ("print([s.strip().lower() for s in raw])", "Очистка."),
        ('print([int(x) for x in "1 2 3".split()])', "Строки → числа."),
    ],
    mistake="Ожидать строки во втором списке."),

f"{P}-m1-l4-e2": x(
    idea="`enumerate` и `zip` работают во включениях так же, как в цикле.",
    lines=[
        ('print([f"{i}. {n}" for i, n in enumerate(names, start=1)])', "Нумерация."),
        ("print([a * b for a, b in zip([1, 2, 3], [10, 20, 30])])", "Попарные произведения."),
    ],
    mistake="Складывать вместо умножения."),

f"{P}-m1-l4-e3": x(
    idea="Своя функция в выражении и фильтр по длине.",
    lines=[
        ("print([square(x) for x in range(4)])", "0, 1, 4, 9."),
        ('print([len(w) for w in "мама мыла раму".split() if len(w) > 3])', "Все три слова по 4 буквы."),
    ],
    mistake="Посчитать пробелы как слова."),

f"{P}-m1-l4-e4": x(
    idea="Цепочка методов в выражении.",
    lines=[
        ("return [e.strip().lower() for e in emails]", "Пробелы и регистр."),
    ],
    mistake="Вызвать методы, но не сохранить результат — строки неизменяемы."),

f"{P}-m1-l4-e5": x(
    idea="`split` по запятой, фильтр пустых, `int` (он сам игнорирует пробелы).",
    lines=[
        ('return [int(part) for part in text.split(",") if part.strip()]', "`\"\"` пропущен."),
    ],
    mistake="Без фильтра — `int(\"\")` упадёт."),

f"{P}-m1-l4-e6": x(
    idea="`enumerate(..., start=1)` во включении.",
    lines=[
        ('return [f"{i}) {x}" for i, x in enumerate(items, start=1)]', "`1) login`."),
    ],
    mistake="Нумерация с 0."),

f"{P}-m1-l4-e7": x(
    idea="`zip` — пары цена/количество.",
    lines=[
        ("return [p * q for p, q in zip(prices, qtys)]", "200, 150."),
    ],
    mistake="Перемножить списки — так нельзя."),

f"{P}-m1-l4-e8": x(
    idea="`enumerate(zip(...), start=1)` — номер и пара; скобки распаковывают пару.",
    lines=[
        ("return [i for i, (e, a) in enumerate(zip(expected, actual), start=1) if e != a]", "Позиция 2."),
    ],
    mistake="`for i, e, a in enumerate(...)` — `ValueError`."),

# ===== Модуль 2. Два for =====

f"{P}-m2-l1-e1": x(
    idea="Два `for` в одном включении читаются как вложенные циклы: первый — внешний.",
    lines=[
        ('print([(a, b) for a in [1, 2] for b in "xy"])', "Для 1 — x, y; для 2 — x, y."),
    ],
    mistake="Ожидать `(1, 'x'), (2, 'y')` — это был бы `zip`."),

f"{P}-m2-l1-e2": x(
    idea="Сплющивание: для каждой строки — каждый её элемент.",
    lines=[
        ("print([x for row in matrix for x in row])", "Порядок `for` — как во вложенных циклах."),
    ],
    mistake="Поставить `for x in row` первым — `row` ещё не определён."),

f"{P}-m2-l1-e3": x(
    idea="Комбинации с исключением через фильтр.",
    lines=[
        ('print([f"{b}@{s}" for b in ["chrome", "ff"] for s in [1920, 375] if not (b == "ff" and s == 375)])', "Три из четырёх."),
    ],
    mistake="`b != \"ff\" and s != 375` — отбросит больше, чем нужно."),

f"{P}-m2-l1-e4": x(
    idea="Два `for`: внешний по спискам, внутренний по элементам.",
    lines=[
        ("return [x for lst in lists for x in lst]", "Пустые списки ничего не дают."),
    ],
    mistake="`[lst for lst in lists]` — останется список списков."),

f"{P}-m2-l1-e5": x(
    idea="Все комбинации — два `for`.",
    lines=[
        ('return [f"{b}@{s}" for b in browsers for s in sizes]', "Сначала все размеры для первого браузера."),
    ],
    mistake="Поменять `for` местами — порядок будет по размерам."),

f"{P}-m2-l1-e6": x(
    idea="Строка перебирается посимвольно — второй `for` по символам слова.",
    lines=[
        ("return [ch for w in words for ch in w]", "a, b, c."),
    ],
    mistake="`list(words)` — получатся слова, а не символы."),

f"{P}-m2-l1-e7": x(
    idea="Второй `for` может использовать переменную первого — так получаются пары без повторов.",
    lines=[
        ("return [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]", "`j` всегда больше `i`."),
    ],
    mistake="Оба `range` от 1 — появятся (2, 1) и (1, 1)."),

f"{P}-m2-l1-e8": x(
    idea="Сначала все теги подряд, потом `dict.fromkeys` убирает повторы, сохраняя порядок.",
    lines=[
        ('flat = [tag for t in tests for tag in t["tags"]]', "smoke, api, api, ui."),
        ("return list(dict.fromkeys(flat))", "Ключи словаря уникальны и идут по порядку появления."),
    ],
    mistake="`list(set(flat))` — порядок не гарантирован."),

# ===== Матрицы =====

f"{P}-m2-l2-e1": x(
    idea="Включение **внутри** включения даёт список списков: внешнее — строки, внутреннее — элементы строки.",
    lines=[
        ("print([[i * j for j in range(1, 4)] for i in range(1, 3)])", "Две строки по три числа."),
    ],
    mistake="Ожидать плоский список."),

f"{P}-m2-l2-e2": x(
    idea="Вложенное включение сохраняет структуру, два `for` в одном — сплющивают.",
    lines=[
        ("print([[x * 10 for x in row] for row in m])", "Матрица."),
        ("print([x * 10 for row in m for x in row])", "Плоский список."),
    ],
    mistake="Считать эти записи одинаковыми."),

f"{P}-m2-l2-e3": x(
    idea="`[[0] * 2] * 2` копирует **ссылку** на одну строку. Включение создаёт новую строку на каждом шаге.",
    lines=[
        ("bad = [[0] * 2] * 2", "Две ссылки на одну строку."),
        ("good = [[0] * 2 for _ in range(2)]", "Две разные строки."),
    ],
    mistake="Ожидать одинаковый результат."),

f"{P}-m2-l2-e4": x(
    idea="Новая строка на каждом шаге внешнего включения.",
    lines=[
        ("return [[0] * cols for _ in range(rows)]", "Строки независимы."),
    ],
    mistake="`[[0] * cols] * rows` — одна строка на всех."),

f"{P}-m2-l2-e5": x(
    idea="Вложенное включение: внешнее — номер строки, внутреннее — столбцы.",
    lines=[
        ("return [[i * j for j in range(1, n + 1)] for i in range(1, n + 1)]", "Таблица умножения."),
    ],
    mistake="Начать с 0 — появятся нулевые строка и столбец."),

f"{P}-m2-l2-e6": x(
    idea="Внешнее включение по номерам столбцов, внутреннее — по строкам.",
    lines=[
        ("return [[row[c] for row in m] for c in range(len(m[0]))]", "Столбец `c` становится строкой."),
    ],
    mistake="Поменять включения местами — получится копия."),

f"{P}-m2-l2-e7": x(
    idea="Структура сохраняется, меняется каждый элемент.",
    lines=[
        ("return [[x * k for x in row] for row in m]", "Новая матрица."),
    ],
    mistake="Сплющить матрицу вторым `for`."),

f"{P}-m2-l2-e8": x(
    idea="Внешнее включение — по строкам текста (с фильтром пустых), внутреннее — по ячейкам.",
    lines=[
        ('return [[cell.strip() for cell in line.split(",")] for line in text.split("\\n") if line.strip()]', "Хвостовой `\\n` даёт пустую строку — её отсеивает фильтр."),
    ],
    mistake="Не фильтровать — появится `[\"\"]` в конце."),

# ===== Словарные включения =====

f"{P}-m2-l3-e1": x(
    idea="`{ключ: значение for …}` — словарное включение, можно с фильтром.",
    lines=[
        ("print({w: len(w) for w in words})", "Слово → длина."),
        ("print({i: i * i for i in range(4) if i % 2})", "Только нечётные."),
    ],
    mistake="Забыть двоеточие — получится множество."),

f"{P}-m2-l3-e2": x(
    idea="Можно менять и ключи, и значения, и местами их поменять.",
    lines=[
        ("print({k.upper(): v * 2 for k, v in prices.items()})", "Ключи заглавные, цены удвоены."),
        ("print({v: k for k, v in prices.items()})", "Обратный словарь."),
    ],
    mistake="Перебирать без `items()` — получатся только ключи."),

f"{P}-m2-l3-e3": x(
    idea="При повторяющемся ключе побеждает **последнее** значение.",
    lines=[
        ("print({w[0]: w for w in words})", "`a` сначала apple, потом avocado."),
    ],
    mistake="Ожидать apple."),

f"{P}-m2-l3-e4": x(
    idea="Имя → длина.",
    lines=[
        ("return {n: len(n) for n in names}", "Словарное включение."),
    ],
    mistake="Список пар вместо словаря."),

f"{P}-m2-l3-e5": x(
    idea="Ключи те же, значения пересчитаны.",
    lines=[
        ("return {k: round(v * (1 - percent / 100), 2) for k, v in prices.items()}", "99.9 → 89.91."),
    ],
    mistake="Изменять исходный словарь."),

f"{P}-m2-l3-e6": x(
    idea="Фильтр по значению в словарном включении.",
    lines=[
        ('return {k: v for k, v in results.items() if v == "fail"}', "Только `b`."),
    ],
    mistake="Удалять из исходного во время перебора — `RuntimeError`."),

f"{P}-m2-l3-e7": x(
    idea="Ключи и значения меняются местами.",
    lines=[
        ("return {v: k for k, v in d.items()}", "1 → a."),
    ],
    mistake="При одинаковых значениях часть пар потеряется — это надо помнить."),

f"{P}-m2-l3-e8": x(
    idea="Фильтр по наличию `=`, ключ и значение — части `split` по первому `=`.",
    lines=[
        ('return {line.split("=", 1)[0].strip(): line.split("=", 1)[1].strip() for line in lines if "=" in line}', "Комментарий без `=` пропущен."),
    ],
    mistake="`split(\"=\")` без лимита — значение с `=` внутри разобьётся."),

# ===== Выражения-генераторы =====

f"{P}-m2-l4-e1": x(
    idea="Включение в круглых скобках — генератор: значения выдаются по одному, список не создаётся. Его сразу передают в `sum`, `max`, `any`, `all`.",
    lines=[
        ("print(sum(n * n for n in nums))", "9 + 49 + 4 = 62."),
        ('print(max(len(w) for w in ["a", "bbb", "cc"]))', "3."),
        ("print(any(n > 5 for n in nums), all(n > 1 for n in nums))", "7 > 5; все больше 1."),
    ],
    mistake="Думать, что нужны двойные скобки — внутри вызова хватает одних."),

f"{P}-m2-l4-e2": x(
    idea="Генератор одноразовый: после полного перебора он пуст.",
    lines=[
        ("print(list(gen))", "`[0, 2, 4]`."),
        ("print(list(gen))", "Уже пусто."),
    ],
    mistake="Ожидать тот же список второй раз."),

f"{P}-m2-l4-e3": x(
    idea="Генератор с фильтром прямо в `join` и `sum`.",
    lines=[
        ('print(", ".join(w.upper() for w in words if w))', "Пустая строка пропущена."),
        ("print(sum(1 for w in words if not w))", "Подсчёт пустых."),
    ],
    mistake="Забыть фильтр — появится лишняя запятая."),

f"{P}-m2-l4-e4": x(
    idea="Сумма без промежуточного списка.",
    lines=[
        ("return sum(n * n for n in nums)", "1 + 4 + 9."),
    ],
    mistake="`sum([...])` — работает, но создаёт лишний список."),

f"{P}-m2-l4-e5": x(
    idea="`any` останавливается на первом `True`.",
    lines=[
        ("return any(c >= 500 for c in codes)", "503."),
    ],
    mistake="`any(codes)` — любое ненулевое число истинно."),

f"{P}-m2-l4-e6": x(
    idea="`all` проверяет условие для каждого адреса; часть после `@` берём через `split(\"@\", 1)`.",
    lines=[
        ('return all("@" in e and "." in e.split("@", 1)[1] for e in emails)', "`and` не даст дойти до `split`, если `@` нет."),
    ],
    mistake="Проверять точку во всём адресе — `a.b@x` пройдёт."),

f"{P}-m2-l4-e7": x(
    idea="Генератор с другими аргументами берут в скобки: `max((…), default=0)`.",
    lines=[
        ("return max((len(w) for w in words), default=0)", "Пустой список — 0."),
    ],
    mistake="`max(len(w) for w in words, default=0)` — `SyntaxError`."),

f"{P}-m2-l4-e8": x(
    idea="Условное выражение внутри генератора для `join`.",
    lines=[
        ('return ",".join("" if v is None else str(v) for v in values)', "`1,,x`."),
    ],
    mistake="`str(None)` — получится `None` в строке."),

# ===== Модуль 3. Включения для множеств =====

f"{P}-m3-l1-e1": x(
    idea="Фигурные скобки без двоеточия — множественное включение: повторы исчезают сами.",
    lines=[
        ("unique = {w.lower() for w in words}", "api, ui, ci."),
    ],
    mistake="Ожидать 5 элементов."),

f"{P}-m3-l1-e2": x(
    idea="Вид скобок решает тип: `[]` — список, `{}` — множество, `{k: v}` — словарь.",
    lines=[
        ("print(a, sorted(b), c)", "Список с повторами, множество без, словарь."),
    ],
    mistake="Путать множество и словарь."),

f"{P}-m3-l1-e3": x(
    idea="Пустые `{}` — словарь. Пустое множество даёт только `set()` или включение.",
    lines=[
        ("print(type({}).__name__, type({1}).__name__, type({x for x in []}).__name__)", "`dict set set`."),
    ],
    mistake="Считать `{}` пустым множеством."),

f"{P}-m3-l1-e4": x(
    idea="Множество доменов убирает повторы, `sorted` — упорядочивает.",
    lines=[
        ('return sorted({e.split("@")[1].lower() for e in emails})', "`Mail.ru` и `mail.ru` — один домен."),
    ],
    mistake="Не опускать регистр — домены задвоятся."),

f"{P}-m3-l1-e5": x(
    idea="Количество различных значений — длина множества.",
    lines=[
        ("return len({len(w) for w in words})", "1, 2, 3."),
    ],
    mistake="`len(words)` — количество слов."),

f"{P}-m3-l1-e6": x(
    idea="Множество общих букв, отсортированное и склеенное.",
    lines=[
        ('return "".join(sorted({ch for ch in a if ch in b}))', "o, p, t, y."),
    ],
    mistake="Список вместо множества — буквы задвоятся."),

f"{P}-m3-l1-e7": x(
    idea="Фильтр по статусу, в множество — модуль.",
    lines=[
        ('return sorted({r.split("::")[0] for r in results if r.split("::")[2] == "fail"})', "auth, cart."),
    ],
    mistake="Список — `auth` может повториться."),

f"{P}-m3-l1-e8": x(
    idea="Множество короче списка, если были повторы.",
    lines=[
        ("return len(set(items)) != len(items)", "`{1, 2}` против трёх элементов."),
    ],
    mistake="Сравнивать сами коллекции — список и множество не равны."),

# ===== Ловушки включений =====

f"{P}-m3-l2-e1": x(
    idea="Переменная включения живёт только внутри него.",
    lines=[
        ("print(squares, x)", "Внешняя `x` не тронута."),
    ],
    mistake="Ожидать `x` = 2."),

f"{P}-m3-l2-e2": x(
    idea="Лямбды во включении ловят общую переменную — позднее связывание. `i=i` фиксирует значение.",
    lines=[
        ("fs = [lambda: i for i in range(3)]", "Все видят последнее `i` = 2."),
        ("fixed = [lambda i=i: i for i in range(3)]", "Каждая со своим."),
    ],
    mistake="Ответить `[0, 1, 2]` в первой строке."),

f"{P}-m3-l2-e3": x(
    idea="Включение ради побочного эффекта создаёт ненужный список: `print` возвращает `None`.",
    lines=[
        ("result = [print(n) for n in [1, 2]]", "Печать 1 и 2."),
        ("print(result)", "`[None, None]`."),
    ],
    mistake="Ожидать `[1, 2]`."),

f"{P}-m3-l2-e4": x(
    idea="Если результат не нужен — пиши обычный цикл.",
    lines=[
        ("for x in items:\n        print(x)", "Никакого лишнего списка."),
    ],
    mistake="Оставить включение — стиль хуже, а смысл тот же."),

f"{P}-m3-l2-e5": x(
    idea="`i=i` фиксирует значение в момент создания каждой лямбды.",
    lines=[
        ("return [lambda x, i=i: x * i for i in range(n)]", "0, 10, 20."),
    ],
    mistake="`lambda x: x * i` — все умножат на 2."),

f"{P}-m3-l2-e6": x(
    idea="Независимые строки — только через включение.",
    lines=[
        ("return [[0] * n for _ in range(n)]", "Новая строка на каждом шаге."),
    ],
    mistake="`[[0] * n] * n`."),

f"{P}-m3-l2-e7": x(
    idea="Внутри включения нельзя написать `try`, поэтому проверку выносят в функцию.",
    lines=[
        ("try:\n        int(s)\n        return True", "Получилось — это целое."),
        ("return [int(s) for s in items if is_int(s)]", "Фильтр вызывает функцию."),
    ],
    mistake="`s.isdigit()` — `\"-3\"` не пройдёт."),

f"{P}-m3-l2-e8": x(
    idea="Новый список через включение — исходный не трогаем.",
    lines=[
        ("return [x for x in items if x != value]", "Без двоек."),
    ],
    mistake="`remove` в цикле по тому же списку — пропустит элементы."),

# ===== Включение или цикл =====

f"{P}-m3-l3-e1": x(
    idea="Цикл и включение делают одно и то же; во включении `strip` вызывается дважды — плата за краткость.",
    lines=[
        ("print([s.strip().lower() for s in data if s.strip()])", "a, b, c."),
    ],
    mistake="Ожидать разный результат."),

f"{P}-m3-l3-e2": x(
    idea="Два `for` и два фильтра в одной строке — корректно, но тяжело читать.",
    lines=[
        ("print([x * 2 for row in m if sum(row) > 0 for x in row if x > 0])", "Строки с положительной суммой: [3, 4] и [-5, 6]; положительные ×2: 6, 8, 12."),
    ],
    mistake="Пропустить строку `[-5, 6]` — её сумма 1 > 0."),

f"{P}-m3-l3-e3": x(
    idea="Сложную обработку одного элемента выносят в функцию — включение остаётся простым.",
    lines=[
        ("print([normalize(s) for s in raw])", "Читается как фраза."),
    ],
    mistake="Писать всю логику прямо в выражении."),

f"{P}-m3-l3-e4": x(
    idea="Когда во включении несколько условий и циклов, циклы с понятными именами читаются лучше.",
    lines=[
        ("if sum(row) <= 0:\n            continue", "Пропуск строк с неположительной суммой."),
        ("if x > 0:\n                result.append(x * 2)", "Положительные удвоенными."),
    ],
    mistake="Перепутать условие: исходное `sum(row) > 0` пропускает строку при `<= 0`."),

f"{P}-m3-l3-e5": x(
    idea="Функция для одного заголовка, включение для всех.",
    lines=[
        ('return "-".join(title.strip().lower().split())', "`split()` без аргумента съедает лишние пробелы."),
        ("return [slugify(t) for t in titles]", "Применяем ко всем."),
    ],
    mistake="`replace(\" \", \"-\")` — двойные пробелы дадут двойные дефисы."),

f"{P}-m3-l3-e6": x(
    idea="Для поиска первого включение избыточно. `next(генератор, по_умолчанию)` остановится на первом найденном.",
    lines=[
        ("return next((n for n in nums if n < 0), None)", "−1; нет таких — `None`."),
    ],
    mistake="`[n for n in nums if n < 0][0]` — переберёт всё и упадёт на пустом."),

f"{P}-m3-l3-e7": x(
    idea="Три коротких включения понятнее одного цикла с тремя ветками.",
    lines=[
        ('"pos": [n for n in nums if n > 0],', "Положительные."),
        ('"zero": sum(1 for n in nums if n == 0),', "Количество нулей."),
    ],
    mistake="Вернуть список нулей вместо количества."),

f"{P}-m3-l3-e8": x(
    idea="Когда нужно состояние между шагами (накопленная сумма), удобнее обычный цикл.",
    lines=[
        ("total += n\n        result.append(total)", "1, 3, 6."),
    ],
    mistake="Пытаться уместить в включение с `sum(nums[:i+1])` — работает, но квадратично медленно."),

# ===== Практика =====

f"{P}-m3-l4-e1": x(
    idea="Три вида включений на одних данных: список, генератор в `sum`, словарь.",
    lines=[
        ('print([r["name"] for r in results if r["status"] == "fail"])', "`pay`."),
        ('print(round(sum(r["time"] for r in results), 1))', "5.1."),
        ('print({r["name"]: r["time"] for r in results if r["time"] > 1})', "login и pay."),
    ],
    mistake="Включить `cart` в последний словарь — 0.5 не больше 1."),

f"{P}-m3-l4-e2": x(
    idea="Множество уровней логов и список текстов ошибок.",
    lines=[
        ("levels = {line.split()[0] for line in log}", "Три уровня, ERROR один раз."),
        ('print([line.split(" ", 1)[1] for line in log if line.startswith("ERROR")])', "Тексты."),
    ],
    mistake="Ожидать ERROR дважды в множестве."),

f"{P}-m3-l4-e3": x(
    idea="Словарное включение с `all` внутри значения.",
    lines=[
        ('print({name: all(s == "pass" for s in runs) for name, runs in suites.items()})', "auth — есть fail."),
    ],
    mistake="`any` — auth станет `True`."),

f"{P}-m3-l4-e4": x(
    idea="Сначала отбор, потом сортировка, потом имена.",
    lines=[
        ('slow = [r for r in results if r["time"] > limit]', "b и c."),
        ('return [r["name"] for r in sorted(slow, key=lambda r: r["time"], reverse=True)]', "По убыванию."),
    ],
    mistake="Сортировать имена — потеряется связь со временем."),

f"{P}-m3-l4-e5": x(
    idea="Фильтр по префиксу и отрезание уровня.",
    lines=[
        ('return [line.split(" ", 1)[1] for line in log if line.startswith("ERROR ")]', "`db down` целиком."),
    ],
    mistake="`split()[1]` — останется `db`."),

f"{P}-m3-l4-e6": x(
    idea="Условное выражение в значении словарного включения.",
    lines=[
        ('return {name: "green" if all(s == "pass" for s in runs) else "red" for name, runs in suites.items()}', "auth red, cart green."),
    ],
    mistake="Путать `all` и `any`."),

f"{P}-m3-l4-e7": x(
    idea="Множество статусов — ключи, для каждого — список имён.",
    lines=[
        ("statuses = {s for _, s in results}", "pass, fail."),
        ("return {st: [n for n, s in results if s == st] for st in statuses}", "Группы."),
    ],
    mistake="Ключ — список статусов с повторами."),

f"{P}-m3-l4-e8": x(
    idea="Условное выражение прямо внутри f-строки включения. Внутренние кавычки — одинарные.",
    lines=[
        ("""return [f"{'✅' if r['status'] == 'pass' else '❌'} {r['name']} ({r['time']} с)" for r in results]""", "`✅ a (1.2 с)`."),
    ],
    mistake="Двойные кавычки внутри f-строки в двойных — ошибка в старых версиях Python."),
}
