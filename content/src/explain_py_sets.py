"""Тема «Множества» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "set"

EXPLAIN = {

# ===== Модуль 1. Создание и уникальность =====

f"{P}-m1-l1-e1": x(
    idea="Множество хранит только **различные** значения и не хранит порядок. Для печати по порядку его сортируют.",
    lines=[
        ("s = {3, 1, 3, 2, 1}", "Повторы исчезли: 3 элемента."),
        ('print(sorted(set("hello")))', "Две `l` стали одной."),
    ],
    mistake="Ожидать порядок вставки — у множества его нет."),

f"{P}-m1-l1-e2": x(
    idea="`{}` — пустой **словарь**. Пустое множество создаётся только через `set()`.",
    lines=[
        ("print(type(a).__name__, type(b).__name__, len(b))", "`dict set 0`."),
    ],
    mistake="Считать `{}` пустым множеством."),

f"{P}-m1-l1-e3": x(
    idea="`set(список)` убирает повторы; проверка `in` для множества мгновенная.",
    lines=[
        ('print(len(tags), len(unique), "smoke" in unique)', "5 тегов, 3 различных."),
    ],
    mistake="Ожидать, что `set` изменит исходный список."),

f"{P}-m1-l1-e4": x(
    idea="Количество различных — длина множества.",
    lines=[("return len(set(items))", "1, 2, 3.")],
    mistake="`len(items)` — считает повторы."),

f"{P}-m1-l1-e5": x(
    idea="Множество убирает повторы, `sorted` возвращает список.",
    lines=[("return sorted(set(items))", "`[1, 2, 3]`.")],
    mistake="`list(set(items))` — порядок не гарантирован."),

f"{P}-m1-l1-e6": x(
    idea="Нижний регистр, без пробелов, множество, сортировка, склейка.",
    lines=[('return "".join(sorted(set(text.lower().replace(" ", ""))))', "`dehlorw`.")],
    mistake="Забыть `lower()` — `H` и `h` станут разными."),

f"{P}-m1-l1-e7": x(
    idea="Если повторов нет, множество той же длины, что и список.",
    lines=[("return len(set(items)) == len(items)", "Повтор уменьшает множество.")],
    mistake="Сравнивать `set(items) == items` — множество не равно списку."),

f"{P}-m1-l1-e8": x(
    idea="Пустое множество — только `set()`.",
    lines=[("return set()", "Именно вызов `set()` — литерала для пустого множества нет.")],
    mistake="`return {}` — вернётся словарь."),

# ===== Добавление и удаление =====

f"{P}-m1-l2-e1": x(
    idea="`add` добавляет один элемент, `update` — все из коллекции. Уже существующие ничего не меняют.",
    lines=[
        ("s.add(2)", "2 уже есть — ничего."),
        ("s.update([4, 5, 1])", "Добавились 4 и 5."),
    ],
    mistake="Ожидать дубли."),

f"{P}-m1-l2-e2": x(
    idea="`discard` молча игнорирует отсутствующий элемент, `remove` — бросает `KeyError`.",
    lines=[
        ("s.discard(99)", "Без ошибки."),
        ("s.remove(99)", "`KeyError`."),
    ],
    mistake="Путать `remove` и `discard`."),

f"{P}-m1-l2-e3": x(
    idea="`pop` снимает и возвращает произвольный элемент; `clear` очищает; пустое множество печатается как `set()`.",
    lines=[
        ("x = s.pop()", "Единственный элемент `a`."),
        ("print(s)", "`set()`, а не `{}`."),
    ],
    mistake="Ожидать `{}` в выводе."),

f"{P}-m1-l2-e4": x(
    idea="`update` добавляет все элементы коллекции на месте.",
    lines=[
        ("tags.update(new)", "`api` уже было."),
        ("return len(tags)", "2."),
    ],
    mistake="`tags.add(new)` — список в множество не положить."),

f"{P}-m1-l2-e5": x(
    idea="Проверяем наличие, чтобы вернуть правильный флаг.",
    lines=[("if item in s:\n        s.discard(item)\n        return True", "Удалили.")],
    mistake="`s.remove(item)` без проверки — `KeyError`."),

f"{P}-m1-l2-e6": x(
    idea="Вход — `add`, выход — `discard` (повторный выход без ошибки).",
    lines=[
        ('if action == "login":\n            online.add(name)', "Вошёл."),
        ("else:\n            online.discard(name)", "Вышел."),
    ],
    mistake="`remove` — второй `logout` упадёт."),

f"{P}-m1-l2-e7": x(
    idea="Множество само убирает повторные коды.",
    lines=[('if line.startswith("ERROR "):\n            codes.add(line.split()[1])', "Код — второе слово.")],
    mistake="Собирать в список — 500 будет дважды."),

f"{P}-m1-l2-e8": x(
    idea="Пустое множество ложно — `while s` остановится само.",
    lines=[("while s:\n        taken.append(s.pop())", "Снимаем по одному.")],
    mistake="Не сортировать — порядок `pop` произвольный."),

# ===== Принадлежность и хешируемость =====

f"{P}-m1-l3-e1": x(
    idea="Проверка `in` по множеству допустимых значений; регистр приводим заранее.",
    lines=[("print(m, m.upper() in allowed)", "`get` → `GET`.")],
    mistake="Ожидать `False` для `get`."),

f"{P}-m1-l3-e2": x(
    idea="В множество можно положить только хешируемые (неизменяемые) значения. Список — нельзя.",
    lines=[
        ('s = {1, "a", (1, 2), None}', "Всё допустимо."),
        ("s.add([1, 2])", "`unhashable type: 'list'`."),
    ],
    mistake="Считать `None` недопустимым."),

f"{P}-m1-l3-e3": x(
    idea="`1`, `True` и `1.0` равны — для множества это один элемент.",
    lines=[("print(len(s), sorted(s))", "Остались 1 и 2.")],
    mistake="Ожидать 4 элемента."),

f"{P}-m1-l3-e4": x(
    idea="Уже виденные — в множестве. Встретили снова — это и есть первый повтор.",
    lines=[
        ("if x in seen:\n            return x", "Для `[3, 1, 4, 1, 3]` первой повторится 1."),
        ("seen.add(x)", "Запоминаем после проверки."),
    ],
    mistake="Добавлять до проверки — любой элемент станет «повтором»."),

f"{P}-m1-l3-e5": x(
    idea="Константа-множество и проверка `in`.",
    lines=[("return method.upper() in ALLOWED", "Регистр не важен.")],
    mistake="Список вместо множества — работает, но медленнее на больших наборах."),

f"{P}-m1-l3-e6": x(
    idea="Точку-список превращаем в кортеж, чтобы положить в множество.",
    lines=[("return len({tuple(p) for p in points})", "2 различные.")],
    mistake="`set(points)` — `TypeError`."),

f"{P}-m1-l3-e7": x(
    idea="Превращаем запрещённые в множество один раз — дальше каждая проверка мгновенная.",
    lines=[
        ("banned_set = set(banned)", "До цикла."),
        ("return [w for w in words if w not in banned_set]", "Фильтр."),
    ],
    mistake="Создавать `set(banned)` внутри включения — на каждом шаге заново."),

f"{P}-m1-l3-e8": x(
    idea="Для каждого числа проверяем, встречалась ли «пара» `target - n`. Один проход вместо двойного цикла.",
    lines=[
        ("if target - n in seen:\n            return True", "8 + 1: при 1 уже видели 8."),
        ("seen.add(n)", "После проверки — чтобы число не сложилось само с собой."),
    ],
    mistake="Добавлять до проверки — `[4]` с целью 8 даст `True`."),

# ===== Перебор, порядок, преобразования =====

f"{P}-m1-l4-e1": x(
    idea="Упорядочить множество — `sorted`, в том числе в обратном порядке.",
    lines=[("print(list(sorted(s))[0])", "Первый по алфавиту.")],
    mistake="Брать `s[0]` — у множества нет индексов."),

f"{P}-m1-l4-e2": x(
    idea="Множественное включение: остатки от деления на 4 — только 0, 1, 2, 3.",
    lines=[("print(sorted(s), sum(s), max(s))", "Сумма 6.")],
    mistake="Считать сумму по всем десяти числам."),

f"{P}-m1-l4-e3": x(
    idea="`set` теряет порядок, `dict.fromkeys` — сохраняет порядок первого появления.",
    lines=[
        ("print(sorted(set(nums)))", "По возрастанию."),
        ("print(list(dict.fromkeys(nums)))", "5, 1, 3."),
    ],
    mistake="Ожидать одинаковый порядок."),

f"{P}-m1-l4-e4": x(
    idea="Множество — для быстрой проверки, список — для порядка.",
    lines=[("if x not in seen:\n            seen.add(x)\n            result.append(x)", "Первое появление.")],
    mistake="`sorted(set(items))` — порядок станет по значению."),

f"{P}-m1-l4-e5": x(
    idea="Количество и отсортированные элементы через `join`.",
    lines=[('return f"{len(s)}: " + ", ".join(sorted(s))', "`2: api, ui`.")],
    mistake="`str(s)` — фигурные скобки и случайный порядок."),

f"{P}-m1-l4-e6": x(
    idea="Очистка каждого слова и множественное включение.",
    lines=[('return {w.strip(".,!?").lower() for w in text.split()}', "`Тест,` и `тест!` — одно слово.")],
    mistake="Не убрать знаки — `тест,` и `тест!` разные."),

f"{P}-m1-l4-e7": x(
    idea="Множество для быстрых проверок; идём от 1 вверх, пока число есть.",
    lines=[
        ("present = set(nums)", "Один раз."),
        ("while n in present:\n        n += 1", "3, 1, 2, 5 → 4."),
    ],
    mistake="Проверять `in nums` в списке — медленно на больших данных."),

f"{P}-m1-l4-e8": x(
    idea="Начинаем отсчёт только с чисел, у которых нет «предшественника» — так каждая серия считается один раз.",
    lines=[
        ("if n - 1 not in s:", "1 — начало серии, 2 — нет."),
        ("while n + length in s:\n                length += 1", "1, 2, 3, 4."),
    ],
    mistake="Считать серию от каждого числа — работает, но квадратично медленно."),

# ===== Модуль 2. Объединение и пересечение =====

f"{P}-m2-l1-e1": x(
    idea="`|` — объединение (всё из обоих), `&` — пересечение (только общее). Методы `union` и `intersection` делают то же.",
    lines=[("print(sorted(a | b), sorted(a & b))", "1–4 и 3.")],
    mistake="Путать `|` и `&`."),

f"{P}-m2-l1-e2": x(
    idea="Методы принимают любые коллекции, операторы — только множества. Строка `\"12\"` — это символы, а не числа.",
    lines=[
        ('print(sorted(a.union([2, 5])), sorted(a.intersection("12")))', "Символы `\"1\"`, `\"2\"` ≠ числа 1, 2 — пересечение пустое."),
        ("a | [2, 5]", "`TypeError`."),
    ],
    mistake="Ожидать `[1, 2]` во втором пересечении."),

f"{P}-m2-l1-e3": x(
    idea="Операторы можно ставить цепочкой для нескольких множеств.",
    lines=[("print(sorted(x & y & z), sorted(x | y | z))", "Общий только 3.")],
    mistake="Посчитать 2 общим — его нет в `z`."),

f"{P}-m2-l1-e4": x(
    idea="Пересечение множеств навыков.",
    lines=[("return sorted(set(a) & set(b))", "python, qa.")],
    mistake="Двойной цикл — длиннее и медленнее."),

f"{P}-m2-l1-e5": x(
    idea="Накопительное объединение через `|=`.",
    lines=[("result |= set(tags)", "Все теги без повторов.")],
    summary="Короче: `sorted(set().union(*tag_lists))`.",
    mistake="Собирать в список — теги задвоятся."),

f"{P}-m2-l1-e6": x(
    idea="Стартуем с первого набора и сужаем пересечением с каждым следующим.",
    lines=[
        ("result = set(groups[0])", "Старт."),
        ("result &= set(g)", "Остаются общие."),
    ],
    mistake="Начать с пустого множества — пересечение всегда пустое."),

f"{P}-m2-l1-e7": x(
    idea="Те же приёмы для букв слов.",
    lines=[("common &= set(w)", "p, t, y есть везде.")],
    mistake="Объединение вместо пересечения."),

f"{P}-m2-l1-e8": x(
    idea="Коэффициент Жаккара — доля общего в объединении: 1 — наборы одинаковые, 0 — ничего общего.",
    lines=[
        ("union = sa | sb", "4 элемента."),
        ("if not union:\n        return 1.0", "Оба пустые — договорённость."),
        ("return round(len(sa & sb) / len(union), 2)", "2 / 4 = 0.5."),
    ],
    mistake="Делить на длину одного набора."),

# ===== Разность и симметричная разность =====

f"{P}-m2-l2-e1": x(
    idea="`a - b` — то, что есть в `a`, но нет в `b`. `a ^ b` — то, что есть только в одном из двух.",
    lines=[
        ("print(sorted(a - b), sorted(b - a))", "Разность несимметрична."),
        ("print(sorted(a ^ b))", "Без общего 3."),
    ],
    mistake="Думать, что `a - b` == `b - a`."),

f"{P}-m2-l2-e2": x(
    idea="Разность множеств — классическая проверка полей ответа: чего не хватает и что лишнее.",
    lines=[
        ('print("не хватает:", sorted(expected - actual))', "email."),
        ('print("лишние:", sorted(actual - expected))', "debug."),
    ],
    mistake="Перепутать порядок операндов."),

f"{P}-m2-l2-e3": x(
    idea="Методы `difference` и `symmetric_difference` принимают несколько коллекций и списки.",
    lines=[("print(sorted(a.difference([2], {3})), sorted(a.symmetric_difference([3, 9])))", "`[1]` и `[1, 2, 9]`.")],
    mistake="Ожидать ошибку от списков в методах."),

f"{P}-m2-l2-e4": x(
    idea="Разность: ожидаемые минус фактические.",
    lines=[("return sorted(set(expected) - set(actual))", "email, name.")],
    mistake="`set(actual) - set(expected)` — получатся лишние."),

f"{P}-m2-l2-e5": x(
    idea="Две разности в обе стороны.",
    lines=[('return {"missing": sorted(e - a), "extra": sorted(a - e)}', "name и debug.")],
    mistake="Одна симметричная разность — не видно, чего не хватает, а что лишнее."),

f"{P}-m2-l2-e6": x(
    idea="Симметричная разность — элементы, которые есть только в одном списке.",
    lines=[("return sorted(set(before) ^ set(after))", "1 и 4.")],
    mistake="`-` — только одна сторона."),

f"{P}-m2-l2-e7": x(
    idea="Новые падения — сегодняшние минус вчерашние.",
    lines=[("return sorted(set(today) - set(yesterday))", "c, d.")],
    mistake="Наоборот — получатся починенные тесты."),

f"{P}-m2-l2-e8": x(
    idea="Полный набор `1..n` минус имеющиеся.",
    lines=[("return sorted(set(range(1, n + 1)) - set(nums))", "3, 4, 6.")],
    mistake="`range(n)` — 0 появится, а `n` пропадёт."),

# ===== Подмножества =====

f"{P}-m2-l3-e1": x(
    idea="`<=` — подмножество (может совпадать), `<` — строгое подмножество. Множество — подмножество самого себя, но не строгое.",
    lines=[
        ("print(required <= user, required.issubset(user), user >= required)", "Всё `True`."),
        ("print(required < user, user < user, user <= user)", "`user < user` — `False`."),
    ],
    mistake="Считать `user < user` истинным."),

f"{P}-m2-l3-e2": x(
    idea="Множества равны без учёта порядка, списки — с учётом. `isdisjoint` — «нет общих элементов».",
    lines=[
        ("print({1, 2} == {2, 1}, [1, 2] == [2, 1])", "`True False`."),
        ("print({1, 2}.isdisjoint({3, 4}), {1, 2}.isdisjoint([2]))", "Общий 2 — `False`."),
    ],
    mistake="Путать `isdisjoint` с «не равны»."),

f"{P}-m2-l3-e3": x(
    idea="Пустое множество — подмножество любого и не пересекается ни с чем, даже с собой.",
    lines=[("print(e <= {1}, e <= e, e.isdisjoint(e))", "Все `True`.")],
    mistake="Ожидать `False` для `e.isdisjoint(e)`."),

f"{P}-m2-l3-e4": x(
    idea="Все требуемые права ⊆ права пользователя.",
    lines=[("return set(required) <= set(user_perms)", "`admin` не хватает — `False`.")],
    mistake="Поменять операнды."),

f"{P}-m2-l3-e5": x(
    idea="Равенство множеств — одинаковый набор без учёта порядка и повторов.",
    lines=[("return set(a) == set(b)", "Двойная 2 не мешает.")],
    mistake="`sorted(a) == sorted(b)` — учтёт повторы."),

f"{P}-m2-l3-e6": x(
    idea="`isdisjoint` принимает любую коллекцию.",
    lines=[("return set(a).isdisjoint(b)", "Общих дней нет.")],
    mistake="`not set(a) & set(b)` — тоже верно, но `isdisjoint` яснее."),

f"{P}-m2-l3-e7": x(
    idea="Порядок проверок важен: сначала равенство, потом строгие вложения, потом «нет общих», иначе — пересекаются.",
    lines=[
        ('if a == b:\n        return "equal"', "Равенство до `<`."),
        ('if a < b:\n        return "subset"', "Строго внутри."),
        ('if a.isdisjoint(b):\n        return "disjoint"', "Ничего общего."),
    ],
    mistake="`<=` вместо `<` — равные множества станут «subset»."),

f"{P}-m2-l3-e8": x(
    idea="Объединяем всё, что проверяют тесты, и сравниваем с функциями продукта через подмножество.",
    lines=[
        ("tested |= set(checked)", "login, pay, cart."),
        ("return set(features) <= tested", "Все функции покрыты."),
    ],
    mistake="Требовать равенство — лишний `cart` сломает проверку."),

# ===== Изменение на месте =====

f"{P}-m2-l4-e1": x(
    idea="`|=`, `-=`, `&=` меняют множество на месте.",
    lines=[
        ("s |= {4}", "1, 2, 3, 4."),
        ("s -= {1}", "2, 3, 4."),
        ("s &= {2, 3, 4, 5}", "Остались 2, 3, 4."),
    ],
    mistake="Ожидать 5 в результате — `&=` оставляет только общие."),

f"{P}-m2-l4-e2": x(
    idea="`a = a | x` создаёт новое множество, `c |= x` — меняет существующее. Это видно по второй ссылке.",
    lines=[
        ("a = a | {3}", "`b` смотрит на старое."),
        ("c |= {3}", "`d` видит изменение."),
    ],
    mistake="Считать `|=` и `= |` одинаковыми."),

f"{P}-m2-l4-e3": x(
    idea="Методы `*_update` — изменяющие версии операций.",
    lines=[
        ("s.difference_update([1, 9])", "{2, 3}."),
        ("s.intersection_update({2, 3, 4})", "{2, 3}."),
        ("s.symmetric_difference_update({3, 5})", "3 ушёл, 5 добавился."),
    ],
    mistake="Ожидать, что 3 останется."),

f"{P}-m2-l4-e4": x(
    idea="`|=` меняет переданное множество на месте — изменения видны снаружи.",
    lines=[("perms |= set(new)", "Список превращаем в множество — оператор работает только с множествами.")],
    mistake="`perms = perms | set(new)` — изменится только локальное имя."),

f"{P}-m2-l4-e5": x(
    idea="`-=` удаляет на месте, отсутствующие просто игнорируются.",
    lines=[("perms -= set(removed)", "Разность на месте.")],
    mistake="`remove` в цикле — `KeyError` на отсутствующем."),

f"{P}-m2-l4-e6": x(
    idea="`&=` оставляет только разрешённое.",
    lines=[("perms &= set(allowed)", "Пересечение на месте.")],
    mistake="`perms = perms & …` — внешнее множество не изменится."),

f"{P}-m2-l4-e7": x(
    idea="`+` — `add`, `-` — `discard` (без ошибок на отсутствующих).",
    lines=[
        ('if op == "+":\n            perms.add(perm)', "Добавить."),
        ("else:\n            perms.discard(perm)", "`admin` не было — без ошибки."),
    ],
    mistake="`remove` — упадёт на `admin`."),

f"{P}-m2-l4-e8": x(
    idea="Оператор `|` создаёт новое множество, исходное не меняется.",
    lines=[("return s | set(items)", "`s` остаётся `{1}`.")],
    mistake="`s |= …` — изменит исходное."),

# ===== Модуль 3. frozenset =====

f"{P}-m3-l1-e1": x(
    idea="`frozenset` — неизменяемое множество: читать можно, менять нельзя.",
    lines=[
        ("print(sorted(fs), len(fs), 1 in fs)", "Повторы убраны."),
        ("fs.add(5)", "Метода нет — `AttributeError`."),
    ],
    mistake="Ожидать `TypeError` — у frozenset просто нет `add`."),

f"{P}-m3-l1-e2": x(
    idea="`frozenset` хешируемый — может быть ключом словаря. Порядок элементов в нём не важен.",
    lines=[
        ('print(combos[frozenset({"linux", "chrome"})])', "Тот же набор — тот же ключ."),
        ("{{1, 2}: \"x\"}", "Обычное множество — нельзя."),
    ],
    mistake="Ожидать, что порядок в ключе важен."),

f"{P}-m3-l1-e3": x(
    idea="Операции с frozenset дают frozenset; сравнивать с обычным множеством можно.",
    lines=[("print(type(b).__name__, sorted(b), a == {1, 2})", "`frozenset [1, 2, 3] True`.")],
    mistake="Ожидать, что `a` изменится."),

f"{P}-m3-l1-e4": x(
    idea="`frozenset(коллекция)`.",
    lines=[("return frozenset(items)", "Повторы уйдут, изменить результат будет нельзя.")],
    mistake="`set(items)` — изменяемое."),

f"{P}-m3-l1-e5": x(
    idea="Набор без учёта порядка — frozenset; множество frozenset-ов считает различные комбинации.",
    lines=[("return len({frozenset(r) for r in runs})", "Первые две — одна комбинация.")],
    mistake="`tuple(r)` — порядок будет важен."),

f"{P}-m3-l1-e6": x(
    idea="Набор букв слова без учёта порядка и повторов — frozenset.",
    lines=[("return len({frozenset(w) for w in words})", "listen/silent/enlist и abc/cab.")],
    mistake="`sorted(w)` — учтутся повторы букв (здесь не мешает, но задание про набор)."),

f"{P}-m3-l1-e7": x(
    idea="Ключ словаря — frozenset окружения; повтор ключа перезаписывает статус.",
    lines=[("return {frozenset(env): status for env, status in runs}", "Последний — `fail`.")],
    mistake="`set(env)` как ключ — `TypeError`."),

f"{P}-m3-l1-e8": x(
    idea="Хешируемость проверяется попыткой `hash`.",
    lines=[("try:\n        hash(s)\n        return True", "frozenset — можно.")],
    mistake="Проверять `isinstance(s, set)` — frozenset не является `set`."),

# ===== Дубликаты =====

f"{P}-m3-l2-e1": x(
    idea="Два множества: `seen` — всё виденное, `dups` — встреченное повторно.",
    lines=[("if x in seen:\n        dups.add(x)", "3 и 1 повторяются.")],
    mistake="Дубли в списке — 3 попадёт дважды."),

f"{P}-m3-l2-e2": x(
    idea="Без нормализации `A@x.ru` и `a@x.ru ` — разные строки.",
    lines=[("print(len(set(emails)), len({e.strip().lower() for e in emails}))", "3 и 2.")],
    mistake="Ожидать 2 в первом случае."),

f"{P}-m3-l2-e3": x(
    idea="`Counter` показывает, сколько раз встречается каждый элемент.",
    lines=[("print(sorted(x for x, n in c.items() if n > 1), sorted(x for x, n in c.items() if n == 1))", "a и b повторяются, c — один.")],
    mistake="Путать ключи и значения `items()`."),

f"{P}-m3-l2-e4": x(
    idea="`seen` + `dups`: повторные попадают в `dups` один раз.",
    lines=[("if x in seen:\n            dups.add(x)\n        seen.add(x)", "1 и 3.")],
    mistake="Сортировать `seen` — это все элементы."),

f"{P}-m3-l2-e5": x(
    idea="Нормализация внутри множественного включения.",
    lines=[("return len({e.strip().lower() for e in emails})", "2.")],
    mistake="Нормализовать только регистр."),

f"{P}-m3-l2-e6": x(
    idea="Для каждого различного элемента считаем вхождения в исходном списке.",
    lines=[("return sorted(x for x in set(items) if items.count(x) == 1)", "b, c.")],
    mistake="Перебирать `items` — единичные совпадут, но повторы тоже переберутся зря."),

f"{P}-m3-l2-e7": x(
    idea="Тот же приём `seen`/`dups` для поля записи.",
    lines=[('if r["id"] in seen:\n            dups.add(r["id"])', "id 1 дважды.")],
    mistake="Сравнивать словари целиком — разные записи с одним id не найдутся."),

f"{P}-m3-l2-e8": x(
    idea="Множество увиденных значений ключа; добавляем запись, только если значение новое.",
    lines=[("if r[key] not in seen:\n            seen.add(r[key])\n            result.append(r)", "Первая запись для id 1.")],
    mistake="`{r[key]: r for r in records}` — останется последняя, а нужна первая."),

# ===== Сравнение наборов в тестах =====

f"{P}-m3-l3-e1": x(
    idea="Если порядок не важен — сравнивай множества.",
    lines=[("print(expected == actual, set(expected) == set(actual))", "`False True`.")],
    mistake="Сравнивать списки ролей напрямую."),

f"{P}-m3-l3-e2": x(
    idea="Множества теряют повторы. Если количество важно — сравнивай отсортированные списки.",
    lines=[("print(set(expected) == set(actual), sorted(expected) == sorted(actual))", "`True False`.")],
    mistake="Использовать множества, когда важны количества."),

f"{P}-m3-l3-e3": x(
    idea="`Counter` сравнивает «мультимножества»: порядок не важен, количество — важно.",
    lines=[('print(Counter(["a", "a", "b"]) == Counter(["b", "a", "a"]), Counter(["a", "b"]) == Counter(["a", "a", "b"]))', "`True False`.")],
    mistake="Ожидать `True` во втором сравнении."),

f"{P}-m3-l3-e4": x(
    idea="Набор ролей — множество.",
    lines=[("return set(expected) == set(actual)", "Порядок и повторы не влияют.")],
    mistake="Сравнивать списки."),

f"{P}-m3-l3-e5": x(
    idea="Отсортированные списки равны, если совпадают элементы и их количество.",
    lines=[("return sorted(a) == sorted(b)", "После сортировки одинаковые наборы с равными количествами совпадут.")],
    summary="Или `Counter(a) == Counter(b)`.",
    mistake="`set(a) == set(b)` — потеряет повторы."),

f"{P}-m3-l3-e6": x(
    idea="Сообщение из двух разностей; пустая часть — прочерк через `or \"-\"`.",
    lines=[
        ('missing = ", ".join(sorted(e - a)) or "-"', "Пустая строка ложна — подставится `-`."),
        ('return f"не хватает: {missing}; лишние: {extra}"', "Итоговое сообщение."),
    ],
    mistake="Не заменить пустую часть — получится `не хватает: ; …`."),

f"{P}-m3-l3-e7": x(
    idea="Две проверки: нет дублей (длины совпадают) и набор совпадает.",
    lines=[('return len(ids) == len(set(ids)) and set(ids) == set(expected_ids)', "Дубль уменьшит множество по сравнению со списком.")],
    mistake="Только сравнение множеств — дубль id останется незамеченным."),

f"{P}-m3-l3-e8": x(
    idea="Нестабильные = падали хоть раз (объединение) минус падали всегда (пересечение).",
    lines=[
        ("ever = set().union(*sets)", "a, b, c."),
        ("always = set.intersection(*sets)", "a."),
        ("return sorted(ever - always)", "b, c."),
    ],
    mistake="Не обработать пустой список — `set.intersection()` без аргументов упадёт."),

# ===== Практика =====

f"{P}-m3-l4-e1": x(
    idea="Отбор тестов по тегу и объединение всех тегов.",
    lines=[
        ('selected = [name for name, tags in tests.items() if "auth" in tags]', "login, logout."),
        ("print(sorted(set().union(*tests.values())))", "Все теги."),
    ],
    mistake="Путать `union` с пересечением."),

f"{P}-m3-l4-e2": x(
    idea="Разность прав ролей и фильтр ролей по праву.",
    lines=[
        ('print(sorted(roles["admin"] - roles["qa"]))', "delete."),
        ('print([r for r, perms in roles.items() if "write" in perms])', "admin, qa."),
    ],
    mistake="Ожидать `guest` во втором списке."),

f"{P}-m3-l4-e3": x(
    idea="Покрытие: пересечение — покрытые, разности — непокрытые и лишние.",
    lines=[
        ('print(f"покрыто {len(features & tested)} из {len(features)}")', "2 из 4."),
        ("print(sorted(features - tested), sorted(tested - features))", "cart, search и profile."),
    ],
    mistake="Считать `profile` покрытой функцией."),

f"{P}-m3-l4-e4": x(
    idea="«Есть хоть один из include» — непустое пересечение; «нет ни одного из exclude» — пустое.",
    lines=[("return sorted(name for name, tags in tests.items() if inc & set(tags) and not exc & set(tags))", "Пустое множество ложно.")],
    mistake="`inc <= set(tags)` — потребует все теги сразу."),

f"{P}-m3-l4-e5": x(
    idea="Разность прав двух ролей.",
    lines=[("return sorted(set(roles[a]) - set(roles[b]))", "Есть у `a`, нет у `b`.")],
    mistake="Симметричная разность — добавит права `b`."),

f"{P}-m3-l4-e6": x(
    idea="Доля покрытых среди функций продукта. Лишнее в `tested` не считается благодаря пересечению.",
    lines=[
        ("if not f:\n        return 100", "Нечего покрывать."),
        ("return round(len(f & set(tested)) / len(f) * 100)", "2 / 4 = 50."),
    ],
    mistake="Делить на `len(tested)`."),

f"{P}-m3-l4-e7": x(
    idea="`set.intersection(*sets)` — общее для всех наборов.",
    lines=[
        ("if not sets:\n        return []", "Без аргументов `intersection` упадёт."),
        ("return sorted(set.intersection(*sets))", "api."),
    ],
    mistake="Объединение вместо пересечения."),

f"{P}-m3-l4-e8": x(
    idea="Общие друзья — пересечение списков друзей.",
    lines=[("return sorted(set(graph[a]) & set(graph[b]))", "cat.")],
    mistake="Двойной цикл — медленнее и длиннее."),
}
