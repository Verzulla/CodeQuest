"""Тема «Сортировка, filter и map» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "srt"

EXPLAIN = {

# ===== Модуль 1. sorted и list.sort =====

f"{P}-m1-l1-e1": x(
    idea="`sorted(x)` возвращает новый список, исходный не трогает. `x.sort()` сортирует сам список.",
    lines=[
        ("result = sorted(nums)", "Новый список."),
        ("print(result, nums)", "Исходный прежний."),
        ("nums.sort()", "Теперь меняется сам."),
    ],
    mistake="Думать, что `sorted` меняет исходный список."),

f"{P}-m1-l1-e2": x(
    idea="`sort()` возвращает `None` — результат сортировки остаётся в самом списке.",
    lines=[("x = nums.sort()", "В `x` — `None`.")],
    mistake="Писать `nums = nums.sort()` — потеряешь список."),

f"{P}-m1-l1-e3": x(
    idea="`sorted` работает с любой коллекцией и всегда возвращает список. Заглавные буквы идут раньше строчных.",
    lines=[
        ('print(sorted("банан"))', "Символы строки."),
        ("print(sorted((3, 1, 2), reverse=True))", "Кортеж → список по убыванию."),
        ('print(sorted(["b", "B", "a", "A"]))', "A, B раньше a, b."),
    ],
    mistake="Ожидать `['a', 'A', 'b', 'B']`."),

f"{P}-m1-l1-e4": x(
    idea="Копия с сортировкой — `sorted`.",
    lines=[("return sorted(nums)", "Исходный список не меняется.")],
    mistake="`nums.sort(); return nums` — испортит исходный."),

f"{P}-m1-l1-e5": x(
    idea="На месте и по убыванию — `sort(reverse=True)`.",
    lines=[("nums.sort(reverse=True)", "Меняется переданный список.")],
    mistake="`return sorted(...)` — исходный не изменится."),

f"{P}-m1-l1-e6": x(
    idea="Отсортировать по убыванию и взять первые три — срез не падает, если чисел меньше.",
    lines=[("return sorted(scores, reverse=True)[:3]", "90, 80, 70.")],
    mistake="`sorted(scores)[-3:]` — порядок будет по возрастанию."),

f"{P}-m1-l1-e7": x(
    idea="Медиана — середина отсортированного списка; при чётной длине — среднее двух средних.",
    lines=[
        ("mid = len(s) // 2", "Индекс середины."),
        ("if len(s) % 2 == 1:\n        return s[mid]", "Нечётная длина."),
        ("return (s[mid - 1] + s[mid]) / 2", "[1, 2, 3, 4] → (2 + 3) / 2."),
    ],
    mistake="Брать середину неотсортированного списка."),

f"{P}-m1-l1-e8": x(
    idea="Список отсортирован, если равен своей отсортированной копии.",
    lines=[("return nums == sorted(nums)", "`sorted` не трогает исходный — сравниваем с копией.")],
    mistake="`nums.sort() == nums` — слева `None`."),

# ===== Параметр key =====

f"{P}-m1-l2-e1": x(
    idea="`key` задаёт, по чему сравнивать: `str.lower` — без регистра, `len` — по длине. Без ключа заглавные идут первыми.",
    lines=[
        ("print(sorted(words))", "Kiwi первая — заглавная K."),
        ("print(sorted(words, key=str.lower))", "По алфавиту без регистра."),
        ("print(sorted(words, key=len))", "По длине; Kiwi и … равной длины — в исходном порядке."),
    ],
    mistake="Забыть, что без ключа регистр важен."),

f"{P}-m1-l2-e2": x(
    idea="Ключ — любая функция: модуль или остаток.",
    lines=[
        ("print(sorted(nums, key=abs))", "1, 3, 4, 5 по модулю."),
        ("print(sorted(nums, key=lambda n: n % 3))", "Остатки: −5→1, 3→0, −1→2, 4→1. При равном остатке — исходный порядок."),
    ],
    mistake="Считать `-5 % 3` равным −2 — в Python остаток берёт знак делителя: 1."),

f"{P}-m1-l2-e3": x(
    idea="Ключ влияет только на порядок; элементы остаются исходными.",
    lines=[("result = sorted(words, key=str.lower)", "`A` осталась заглавной.")],
    mistake="Ожидать `['a', 'b', 'c']`."),

f"{P}-m1-l2-e4": x(
    idea="Сортировка стабильна: равные по ключу сохраняют исходный порядок.",
    lines=[("return sorted(words, key=len)", "`[\"fig\", \"kiwi\", \"banana\"]`.")],
    mistake="Добавлять второй ключ — задание просит исходный порядок."),

f"{P}-m1-l2-e5": x(
    idea="`key=str.lower` — сравнение без регистра.",
    lines=[("return sorted(words, key=str.lower)", "`A` остаётся заглавной.")],
    mistake="`sorted([w.lower() …])` — потеряются заглавные."),

f"{P}-m1-l2-e6": x(
    idea="Близость к нулю — модуль.",
    lines=[("return sorted(nums, key=abs)", "−1, 3, 4, −5.")],
    mistake="Вернуть модули вместо чисел."),

f"{P}-m1-l2-e7": x(
    idea="Ключ — последний символ.",
    lines=[("return sorted(words, key=lambda w: w[-1])", "a, b, c.")],
    mistake="`w[0]` — первый символ."),

f"{P}-m1-l2-e8": x(
    idea="Версия как список чисел сравнивается правильно: 10 > 9.",
    lines=[('return sorted(versions, key=lambda v: [int(p) for p in v.split(".")])', "`[1, 2, 10]` < `[1, 9, 2]` < `[1, 10, 0]`.")],
    mistake="Сортировать строки — `1.10` окажется раньше `1.9`."),

# ===== Несколько признаков и стабильность =====

f"{P}-m1-l3-e1": x(
    idea="Ключ-кортеж: сначала первый признак, при равенстве — второй. Минус переворачивает порядок числового признака.",
    lines=[
        ("print(sorted(people, key=lambda p: (p[1], p[0])))", "По возрасту, потом по имени."),
        ("print(sorted(people, key=lambda p: (-p[1], p[0])))", "Возраст по убыванию, имя по возрастанию."),
    ],
    mistake="Использовать `reverse=True` — перевернутся оба признака."),

f"{P}-m1-l3-e2": x(
    idea="Стабильность: при равных ключах элементы остаются в исходном порядке.",
    lines=[("print(sorted(items, key=lambda x: x[1]))", "b раньше c, как было.")],
    mistake="Ожидать, что b и c отсортируются по букве."),

f"{P}-m1-l3-e3": x(
    idea="Благодаря стабильности можно сортировать в два прохода: сначала по второстепенному признаку, потом по главному.",
    lines=[
        ("step1 = sorted(people, key=lambda p: p[0])", "По имени."),
        ("step2 = sorted(step1, key=lambda p: p[1], reverse=True)", "По возрасту; при равном сохраняется порядок имён."),
    ],
    mistake="Делать проходы в обратном порядке — главный признак испортится."),

f"{P}-m1-l3-e4": x(
    idea="Очки по убыванию (минус), имя по возрастанию.",
    lines=[("return [name for name, _ in sorted(scores, key=lambda s: (-s[1], s[0]))]", "Аня, Боря, Вика.")],
    mistake="`reverse=True` — имена перевернутся."),

f"{P}-m1-l3-e5": x(
    idea="Ключ-кортеж (длина, слово).",
    lines=[("return sorted(words, key=lambda w: (len(w), w))", "fig, kiwi, pear, apple.")],
    mistake="Только длина — kiwi и pear останутся в исходном порядке."),

f"{P}-m1-l3-e6": x(
    idea="Словарь рангов — свой порядок серьёзности; дата-строка сортируется правильно.",
    lines=[
        ('RANK = {"critical": 0, "major": 1, "minor": 2}', "Место каждой серьёзности в порядке."),
        ("return [b[0] for b in sorted(bugs, key=lambda b: (RANK[b[1]], b[2]))]", "id."),
    ],
    mistake="Сортировать по названию серьёзности."),

f"{P}-m1-l3-e7": x(
    idea="Минус к строке не применить — поэтому два прохода: сначала второстепенный признак, потом главный с `reverse`.",
    lines=[
        ("by_age = sorted(people, key=lambda p: p[1])", "По возрасту."),
        ("return sorted(by_age, key=lambda p: p[0], reverse=True)", "Имя Я→А; при равном имени возраст сохраняет порядок."),
    ],
    mistake="`key=lambda p: (-p[0], p[1])` — `TypeError`: у строки нет минуса."),

f"{P}-m1-l3-e8": x(
    idea="Ранг статуса в словаре; внутри группы стабильность сохраняет исходный порядок.",
    lines=[("return sorted(results, key=lambda r: ORDER[r[1]])", "fail, fail, skip, pass.")],
    mistake="Сортировать по названию статуса — fail, pass, skip."),

# ===== Сортировка словарей и записей =====

f"{P}-m1-l4-e1": x(
    idea="`sorted(словарь)` — ключи; `key=d.get` — ключи по значениям; `items()` — пары.",
    lines=[
        ("print(sorted(scores, key=scores.get, reverse=True))", "По очкам."),
        ("print(sorted(scores.items(), key=lambda p: p[1]))", "Пары по очкам."),
    ],
    mistake="Ожидать словарь в результате."),

f"{P}-m1-l4-e2": x(
    idea="Список словарей сортируют ключом-функцией по полю.",
    lines=[('print([u["name"] for u in sorted(users, key=lambda u: u["age"])])', "Аня младше.")],
    mistake="`sorted(users)` — словари нельзя сравнить."),

f"{P}-m1-l4-e3": x(
    idea="`itemgetter(k)` — готовая замена `lambda r: r[k]`, работает и для индексов, и для ключей.",
    lines=[
        ("print(sorted(rows, key=itemgetter(1)))", "По второму элементу."),
        ('print(sorted(users, key=itemgetter("a")))', "По ключу `a`."),
    ],
    mistake="`itemgetter[1]` — квадратные скобки вместо вызова."),

f"{P}-m1-l4-e4": x(
    idea="Ключи словаря по значению, по убыванию, срез.",
    lines=[("return sorted(times, key=times.get, reverse=True)[:n]", "b, c.")],
    mistake="Сортировать `times.values()` — потеряются имена."),

f"{P}-m1-l4-e5": x(
    idea="Имя поля передаётся параметром — лямбда его запоминает.",
    lines=[("return sorted(records, key=lambda r: r[field])", "Поле выбирается параметром.")],
    mistake="`r[\"field\"]` — строка вместо переменной."),

f"{P}-m1-l4-e6": x(
    idea="Словарь помнит порядок вставки — собираем его из отсортированных пар.",
    lines=[("return dict(sorted(d.items()))", "a, b.")],
    mistake="`sorted(d)` — список ключей без значений."),

f"{P}-m1-l4-e7": x(
    idea="Сортируем имена по очкам и нумеруем с 1.",
    lines=[
        ("ordered = sorted(scores, key=scores.get, reverse=True)", "Аня, Боря."),
        ("return {name: i for i, name in enumerate(ordered, start=1)}", "Место."),
    ],
    mistake="Нумерация с 0."),

f"{P}-m1-l4-e8": x(
    idea="Роль по алфавиту, возраст по убыванию (минус).",
    lines=[('return [u["name"] for u in sorted(users, key=lambda u: (u["role"], -u["age"]))]', "dev, потом qa: c (40), a (20).")],
    mistake="`reverse=True` — перевернёт и роли."),

# ===== Модуль 2. filter =====

f"{P}-m2-l1-e1": x(
    idea="`filter(функция, коллекция)` оставляет элементы, для которых функция вернула истину.",
    lines=[
        ("print(list(filter(is_even, [1, 2, 3, 4])))", "Своя функция."),
        ('print(list(filter(lambda s: len(s) > 2, ["a", "api", "ui", "test"])))', "Лямбда."),
    ],
    mistake="Передать `is_even()` со скобками."),

f"{P}-m2-l1-e2": x(
    idea="`filter(None, …)` оставляет только истинные значения.",
    lines=[("print(list(filter(None, values)))", "`[0]` — непустой список, истинен.")],
    mistake="Считать `[0]` ложным."),

f"{P}-m2-l1-e3": x(
    idea="`filter` возвращает ленивый итератор; значения появляются при переборе.",
    lines=[
        ("print(type(f).__name__)", "`filter`."),
        ("print(list(f))", "Только строки из цифр."),
    ],
    mistake="Ожидать список сразу."),

f"{P}-m2-l1-e4": x(
    idea="Условие — лямбда, результат — список.",
    lines=[("return list(filter(lambda n: n > 0, nums))", "`[3, 5]`.")],
    mistake="Вернуть `filter` без `list`."),

f"{P}-m2-l1-e5": x(
    idea="`None` вместо функции — фильтр по истинности: пустые строки ложны.",
    lines=[("return list(filter(None, strings))", "`[\"a\", \"b\"]`.")],
    mistake="`filter(\"\", …)` — строка не функция."),

f"{P}-m2-l1-e6": x(
    idea="Метод класса `str.isdigit` можно передать как функцию.",
    lines=[("return list(filter(str.isdigit, items))", "12, 7.")],
    mistake="`str.isdigit()` со скобками."),

f"{P}-m2-l1-e7": x(
    idea="Лямбда проверяет поле словаря.",
    lines=[('return list(filter(lambda r: r["status"] == "fail", results))', "Словари со статусом fail.")],
    mistake="Вернуть имена — задание просит словари."),

f"{P}-m2-l1-e8": x(
    idea="Сложную проверку выносят в отдельную функцию и передают её в `filter`.",
    lines=[
        ('return email.count("@") == 1 and "." in email.split("@")[1]', "Ровно одна собака и точка в домене."),
        ("return list(filter(is_valid, emails))", "Функция без скобок."),
    ],
    mistake="`\"@\" in email` — пропустит `c@@x.ru`."),

# ===== map =====

f"{P}-m2-l2-e1": x(
    idea="`map(функция, коллекция)` применяет функцию к каждому элементу.",
    lines=[
        ('print(list(map(str.upper, ["api", "ui"])))', "Метод как функция."),
        ('print(list(map(int, "1 2 3".split())))', "Строки → числа."),
    ],
    mistake="Ожидать список без `list(...)`."),

f"{P}-m2-l2-e2": x(
    idea="С несколькими коллекциями `map` передаёт по элементу из каждой и останавливается на короткой.",
    lines=[
        ("print(list(map(pow, [2, 3, 4], [3, 2])))", "2³, 3²; 4 без пары."),
    ],
    mistake="Ожидать три результата."),

f"{P}-m2-l2-e3": x(
    idea="Результат `map` можно сразу распаковать или передать в `sum`.",
    lines=[
        ('a, b = map(int, "3 4".split())', "Два числа."),
        ('print(sum(map(len, ["ab", "cde"])))', "2 + 3."),
    ],
    mistake="Забыть `split` — `map` пройдёт по символам, включая пробел."),

f"{P}-m2-l2-e4": x(
    idea="Готовая функция `int` — лямбда не нужна.",
    lines=[("return list(map(int, strings))", "`[1, 20, -3]`.")],
    mistake="`map(lambda s: int(s), …)` — работает, но длиннее."),

f"{P}-m2-l2-e5": x(
    idea="`map` + распаковка — разбор строки в числа одной строкой.",
    lines=[("w, h = map(int, text.split())", "3 и 4.")],
    mistake="`w, h = text.split()` — останутся строки."),

f"{P}-m2-l2-e6": x(
    idea="`sum` принимает итератор от `map` напрямую.",
    lines=[("return sum(map(len, words))", "2 + 3 = 5.")],
    mistake="`len(words)` — количество слов."),

f"{P}-m2-l2-e7": x(
    idea="Лямбда с двумя параметрами и две коллекции.",
    lines=[("return list(map(lambda p, q: p * q, prices, qtys))", "100 · 2, 50 · 3.")],
    mistake="Одна коллекция пар — нужна другая лямбда."),

f"{P}-m2-l2-e8": x(
    idea="Своя функция для одного адреса, `map` — для всех.",
    lines=[("return list(map(normalize, emails))", "Функция без скобок.")],
    mistake="`map(normalize(), …)`."),

# ===== filter и map против включений =====

f"{P}-m2-l3-e1": x(
    idea="`map`+`filter`, включение и цикл дают одинаковый результат. Включение обычно читается проще.",
    lines=[
        ("a = list(map(lambda x: x * x, filter(lambda x: x % 2, nums)))", "Изнутри наружу: сначала фильтр."),
        ("b = [x * x for x in nums if x % 2]", "То же включением."),
    ],
    mistake="Ожидать разные результаты."),

f"{P}-m2-l3-e2": x(
    idea="С готовой функцией `map` особенно краток.",
    lines=[("print(list(map(str.strip, words)))", "`['a', 'B', 'c']`.")],
    mistake="Ожидать изменения регистра — `strip` его не трогает."),

f"{P}-m2-l3-e3": x(
    idea="`map(str, …)` и `[str(i) …]` — одно и то же.",
    lines=[("print(list(map(str, range(3))), [str(i) for i in range(3)])", "Два одинаковых списка строк.")],
    mistake="Ожидать числа."),

f"{P}-m2-l3-e4": x(
    idea="Фильтр — в конец включения, преобразование — в начало.",
    lines=[("return [x * x for x in nums if x % 2]", "`[1, 9, 25]` для `[1..5]`.")],
    mistake="Поставить условие в начало — это уже выбор значения, а не фильтр."),

f"{P}-m2-l3-e5": x(
    idea="Внутри — `filter`, снаружи — `map`.",
    lines=[("return list(map(str.upper, filter(lambda w: len(w) > 2, words)))", "Длинные слова заглавными.")],
    mistake="Поменять местами — `filter` получит уже заглавные, результат тот же, но порядок читается хуже."),

f"{P}-m2-l3-e6": x(
    idea="Готовый метод — `map` без лямбды.",
    lines=[("return list(map(str.strip, lines))", "Каждая строка без пробелов по краям.")],
    mistake="`lines.strip()` — у списка нет `strip`."),

f"{P}-m2-l3-e7": x(
    idea="Когда нужна формула с `round`, включение читается лучше лямбды в `map`.",
    lines=[("return [round(p * 1.2, 2) for p in prices]", "9.99 · 1.2 = 11.988 → 11.99.")],
    mistake="Забыть `round` — будут хвосты вроде 11.987999…"),

f"{P}-m2-l3-e8": x(
    idea="Фильтр + выбор поля — естественно для включения.",
    lines=[('return [u["id"] for u in users if u["active"]]', "`[1]`.")],
    mistake="`map` + `filter` с двумя лямбдами — тяжелее читать."),

# ===== Ленивость =====

f"{P}-m2-l4-e1": x(
    idea="`map` — объект-итератор, не список.",
    lines=[("print(type(m).__name__, isinstance(m, list))", "`map False`.")],
    mistake="Индексировать `m[0]` — нельзя."),

f"{P}-m2-l4-e2": x(
    idea="Итератор одноразовый: второй `list` получает пустоту.",
    lines=[("print(list(m))", "Во второй раз — `[]`.")],
    mistake="Ожидать повтор."),

f"{P}-m2-l4-e3": x(
    idea="`map` вычисляет значения по требованию: `next` запускает функцию ровно для одного элемента.",
    lines=[
        ("print(next(m), calls)", "Вызвана один раз."),
        ("print(next(m), calls)", "Второй раз."),
    ],
    mistake="Ожидать, что `map` сразу обработает все три."),

f"{P}-m2-l4-e4": x(
    idea="`next(filter(...), None)` — первый подходящий элемент или `None`; дальше список не проверяется.",
    lines=[
        ("found = next(filter(str.isdigit, items), None)", "`\"12\"`."),
        ("return int(found) if found is not None else None", "В число."),
    ],
    mistake="`int(None)` — упадёт, если ничего не найдено."),

f"{P}-m2-l4-e5": x(
    idea="Итератор, который нужен дважды, превращают в список.",
    lines=[
        ("pos = list(filter(lambda n: n > 0, nums))", "Можно использовать сколько угодно раз."),
        ("return sum(pos), len(pos)", "8 и 2."),
    ],
    mistake="`len(filter(...))` — у итератора нет длины."),

f"{P}-m2-l4-e6": x(
    idea="Счётчик в замыкании показывает, что `filter` остановился на первом найденном.",
    lines=[
        ("nonlocal calls\n        calls += 1", "Считаем вызовы."),
        ("next(filter(is_bad, items), None)", "1, 2, −3 — три проверки."),
    ],
    mistake="Ожидать 5 — ленивый поиск не доходит до конца."),

f"{P}-m2-l4-e7": x(
    idea="Цепочка итераторов: каждый следующий берёт значения у предыдущего по одному — промежуточных списков нет.",
    lines=[
        ("cleaned = map(str.strip, lines)", "Очистка."),
        ("non_empty = filter(None, cleaned)", "Пустые отсеяны."),
        ("return sum(numbers)", "Вся работа происходит здесь."),
    ],
    mistake="Превращать каждый шаг в `list` — работает, но теряется смысл ленивости."),

f"{P}-m2-l4-e8": x(
    idea="`iter` даёт итератор, `next` — следующий элемент; конец — исключение `StopIteration`.",
    lines=[
        ("it = iter(iterable)", "Работает и для списков, и для итераторов."),
        ("except StopIteration:\n            break", "Элементы кончились раньше."),
    ],
    mistake="`list(iterable)[:n]` — на бесконечном итераторе зависнет."),

# ===== Модуль 3. min и max =====

f"{P}-m3-l1-e1": x(
    idea="Без ключа строки сравниваются по алфавиту, с `key=len` — по длине.",
    lines=[
        ("print(min(words), max(words))", "banana и kiwi."),
        ("print(min(words, key=len), max(words, key=len))", "fig и banana."),
    ],
    mistake="Ожидать, что `max` без ключа выберет самое длинное."),

f"{P}-m3-l1-e2": x(
    idea="`default` задаёт ответ для пустой коллекции; без него — `ValueError`.",
    lines=[
        ("print(max([], default=0), min([], default=None))", "0 и None."),
        ("max([])", "Ошибка."),
    ],
    mistake="Ожидать 0 от `max([])` без `default`."),

f"{P}-m3-l1-e3": x(
    idea="При равных ключах `max` и `min` возвращают первый элемент.",
    lines=[
        ("print(max(users, key=lambda u: u[1]))", "Аня — первая из 30-летних."),
        ("print(min(users, key=lambda u: u[1])[0])", "Вика."),
    ],
    mistake="Ожидать Борю."),

f"{P}-m3-l1-e4": x(
    idea="`key=len` и `default` для пустого списка.",
    lines=[('return max(words, key=len, default="")', "Самое длинное или пустая строка.")],
    mistake="Без `default` — ошибка на пустом."),

f"{P}-m3-l1-e5": x(
    idea="`min` по цене с `default=None`, потом имя.",
    lines=[
        ('best = min(products, key=lambda p: p["price"], default=None)', "Самый дешёвый товар или `None`."),
        ('return best["name"] if best else None', "Имя, если товар нашёлся."),
    ],
    mistake="`best[\"name\"]` без проверки — `TypeError` на пустом."),

f"{P}-m3-l1-e6": x(
    idea="Ключ словаря с максимальным значением — `max(d, key=d.get)`.",
    lines=[("return max(scores, key=scores.get)", "Боря.")],
    mistake="`max(scores.values())` — вернёт число, а не имя."),

f"{P}-m3-l1-e7": x(
    idea="Ближайшее — минимальное расстояние `abs(n - target)`.",
    lines=[("return min(nums, key=lambda n: abs(n - target))", "|5 − 6| = 1.")],
    mistake="Без `abs` — выберется самое маленькое число."),

f"{P}-m3-l1-e8": x(
    idea="`default=0` у обоих — для пустого списка 0 − 0.",
    lines=[("return max(nums, default=0) - min(nums, default=0)", "Для `[]` — 0 − 0.")],
    mistake="Не задать `default` — ошибка на пустом."),

# ===== reversed, enumerate, zip =====

f"{P}-m3-l2-e1": x(
    idea="`reversed` не меняет список, а перебирает с конца. С `enumerate` номера идут по порядку перебора.",
    lines=[
        ("print(list(reversed(items)), items)", "Исходный цел."),
        ("for i, x in enumerate(reversed(items), start=1):", "c — первый."),
    ],
    mistake="Ожидать, что `items` перевернётся."),

f"{P}-m3-l2-e2": x(
    idea="`zip(*pairs)` — «разархивировать»: из списка пар получить кортеж первых и кортеж вторых.",
    lines=[
        ("pairs = list(zip(names, ages))", "Пары."),
        ("n, a = zip(*pairs)", "Обратно в две последовательности."),
    ],
    mistake="Ожидать списки — `zip` даёт кортежи."),

f"{P}-m3-l2-e3": x(
    idea="`zip` останавливается на коротком; `strict=True` превращает разную длину в ошибку.",
    lines=[
        ('print(list(zip([1, 2, 3], "ab")))', "3 без пары."),
        ('list(zip([1, 2, 3], "ab", strict=True))', "`ValueError`."),
    ],
    mistake="Ожидать `(3, None)`."),

f"{P}-m3-l2-e4": x(
    idea="Перевернуть и взять первые `n`.",
    lines=[("return list(reversed(items))[:n]", "d, c.")],
    mistake="`items[-n:]` — порядок будет c, d."),

f"{P}-m3-l2-e5": x(
    idea="`dict(zip(...))` — словарь из двух списков.",
    lines=[("return dict(zip(keys, values))", "`{\"host\": …, \"port\": …}`.")],
    mistake="`dict(keys, values)`."),

f"{P}-m3-l2-e6": x(
    idea="`zip(*pairs)` раскладывает пары; пустой список обрабатываем отдельно, иначе распаковать нечего.",
    lines=[
        ("if not pairs:\n        return [], []", "`zip()` без аргументов пуст — распаковка упала бы."),
        ("first, second = zip(*pairs)", "Кортежи."),
        ("return list(first), list(second)", "Списки."),
    ],
    mistake="Не обработать пустой — `ValueError`."),

f"{P}-m3-l2-e7": x(
    idea="`strict=True` защищает от тихо обрезанного сравнения списков разной длины.",
    lines=[('return [f"#{i}: {e} != {a}" for i, (e, a) in enumerate(zip(expected, actual, strict=True), start=1) if e != a]', "Номера расхождений с 1.")],
    mistake="Без `strict` — лишние элементы останутся незамеченными."),

f"{P}-m3-l2-e8": x(
    idea="`enumerate` с распаковкой пары во вложенных скобках.",
    lines=[('return [f"{i}. {name}: {status}" for i, (name, status) in enumerate(results, start=1)]', "`1. login: pass`.")],
    mistake="`for i, name, status in …` — `ValueError`."),

# ===== any, all, подсчёты =====

f"{P}-m3-l3-e1": x(
    idea="`any` — есть ли хоть одно истинное, `all` — все ли истинны. Для пустого: `any` — `False`, `all` — `True`.",
    lines=[
        ("print(any(c >= 400 for c in codes), all(c < 500 for c in codes))", "404 есть; все меньше 500."),
        ("print(any([]), all([]))", "`False True`."),
    ],
    mistake="Ожидать `False` для `all([])`."),

f"{P}-m3-l3-e2": x(
    idea="Без генератора `any`/`all` смотрят на истинность элементов.",
    lines=[('print(any([0, "", None]), any([0, "x"]), all([1, "a", [0]]), all([1, []]))', "`[]` ложен, `[0]` истинен.")],
    mistake="Считать `[0]` ложным."),

f"{P}-m3-l3-e3": x(
    idea="`True` считается как 1, поэтому сумма сравнений — количество совпадений.",
    lines=[
        ('print(sum(r == "pass" for r in results))', "2."),
        ('print(sum(1 for r in results if r == "fail"))', "1."),
    ],
    mistake="Ожидать список вместо числа."),

f"{P}-m3-l3-e4": x(
    idea="`all` по условию.",
    lines=[('return all(r == "pass" for r in results)', "Один fail — `False`.")],
    mistake="`all(results)` — любая непустая строка истинна."),

f"{P}-m3-l3-e5": x(
    idea="`any` по диапазону 500–599.",
    lines=[("return any(500 <= c < 600 for c in codes)", "503 → `True`.")],
    mistake="`c >= 500` — пропустит и 600+."),

f"{P}-m3-l3-e6": x(
    idea="Сумма логических значений.",
    lines=[('return sum(r == "pass" for r in results)', "Количество pass.")],
    mistake="`len(results)` — все статусы."),

f"{P}-m3-l3-e7": x(
    idea="Четыре условия через `and`, три из них — `any` по символам. Скобки позволяют разбить выражение на строки.",
    lines=[
        ("return (len(p) >= 8", "Длина."),
        ("and any(ch.isdigit() for ch in p)", "Цифра."),
        ("and any(ch.isupper() for ch in p)", "Заглавная."),
    ],
    mistake="`all(ch.isdigit() …)` — потребует, чтобы все символы были цифрами."),

f"{P}-m3-l3-e8": x(
    idea="`get` на случай отсутствия поля; `bool` исключаем отдельно — он тоже `int`.",
    lines=[('return all(isinstance(i.get("id"), int) and not isinstance(i.get("id"), bool) and i["id"] > 0 for i in items)', "Проверки идут слева направо — до `> 0` дойдём, только если это число.")],
    mistake="`i[\"id\"] > 0` без проверки типа — `TypeError` на строке."),

# ===== Практика: конвейер =====

f"{P}-m3-l4-e1": x(
    idea="Множество — различные ошибки; `max` по множеству с ключом `errors.count` — самая частая.",
    lines=[
        ('errors = [line.split()[1] for line in log if line.startswith("ERROR")]', "db, api, db."),
        ("print(sorted(set(errors)), max(set(errors), key=errors.count))", "db — два раза."),
    ],
    mistake="`max(errors)` без ключа — сравнит по алфавиту."),

f"{P}-m3-l4-e2": x(
    idea="Конвейер: `filter` → `sorted` → `map`. `sorted` принимает итератор и возвращает список.",
    lines=[
        ('passed = filter(lambda r: r[2] == "pass", results)', "login, cart."),
        ("names = map(lambda r: r[0], sorted(passed, key=lambda r: r[1]))", "По времени: cart 0.5, login 1.2."),
    ],
    mistake="Ожидать порядок исходного списка."),

f"{P}-m3-l4-e3": x(
    idea="Очистка через `map`, фильтр `isdigit` и превращение в числа — в одном включении.",
    lines=[
        ("clean = [int(p) for p in map(str.strip, prices) if p.isdigit()]", "`\"\"` и `x` отсеяны."),
        ("print(clean, sum(clean), max(clean, default=0))", "Список, сумма 390, максимум 250."),
    ],
    mistake="Проверять `isdigit` до `strip` — `\" 250 \"` не пройдёт."),

f"{P}-m3-l4-e4": x(
    idea="Уникальные ошибки сортируем по (−частота, текст).",
    lines=[
        ('errors = [line.split(" ", 1)[1] for line in log if line.startswith("ERROR ")]', "Тексты."),
        ("return sorted(unique, key=lambda e: (-errors.count(e), e))[:n]", "db (2), api (1)."),
    ],
    mistake="Сортировать весь список `errors` — будут повторы."),

f"{P}-m3-l4-e5": x(
    idea="Фильтр по статусу и времени, сортировка по времени, имена.",
    lines=[
        ('ok = [r for r in results if r[2] == "pass" and r[1] < limit]', "Прошедшие и быстрые."),
        ("return [r[0] for r in sorted(ok, key=lambda r: r[1])]", "По времени, только имена."),
    ],
    mistake="Забыть условие по статусу."),

f"{P}-m3-l4-e6": x(
    idea="Генератор чисел прямо в `sorted` с `reverse=True`.",
    lines=[("return sorted((int(p) for p in map(str.strip, raw) if p.isdigit()), reverse=True)", "250, 100, 40.")],
    mistake="`int` до `isdigit` — упадёт на `x`."),

f"{P}-m3-l4-e7": x(
    idea="Сводка собирается из встроенных помощников: `len`, `sum`, `max` с `default`, `all`.",
    lines=[
        ('slowest = max(results, key=lambda r: r["time"], default=None)', "Пустой список — `None`."),
        ('"passed": sum(r["status"] == "pass" for r in results),', "Подсчёт."),
        ('"all_green": all(r["status"] == "pass" for r in results),', "Все ли зелёные."),
    ],
    mistake="`slowest[\"name\"]` без проверки."),

f"{P}-m3-l4-e8": x(
    idea="Словарь «имя в нижнем регистре → первый вариант» убирает повторы; `setdefault` не перезаписывает уже сохранённый.",
    lines=[
        ("seen.setdefault(name.lower(), name)", "`anna` уже есть как `Anna`."),
        ("return sorted(seen.values(), key=str.lower)", "Anna, bob, Cat."),
    ],
    mistake="`seen[name.lower()] = name` — победит последний вариант."),
}
