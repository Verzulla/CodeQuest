"""Тема «Итераторы и генераторы» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "gen"

EXPLAIN = {

# ===== Модуль 1. Итераторы и yield =====

f"{P}-m1-l1-e1": x(
    idea="`iter` даёт итератор, `next` берёт следующий элемент. Второй аргумент `next` — что вернуть, когда элементы кончились.",
    lines=[
        ('print(next(it, "конец"))', "Третий элемент — `c`."),
        ('print(next(it, "конец"))', "Элементов нет — значение по умолчанию."),
    ],
    mistake="Ожидать `StopIteration` — его гасит второй аргумент."),

f"{P}-m1-l1-e2": x(
    idea="Итератор одноразовый: после полного прохода он пуст.",
    lines=[
        ("print(list(it))", "Забрал всё."),
        ("print(list(it))", "Ничего не осталось."),
    ],
    mistake="Ожидать два одинаковых списка."),

f"{P}-m1-l1-e3": x(
    idea="`for` продолжает итератор с текущего места.",
    lines=[
        ("next(it)", "Единица забрана и выброшена."),
        ("for x in it:", "С двойки."),
    ],
    mistake="Ожидать 1 в выводе."),

f"{P}-m1-l1-e4": x(
    idea="У итератора нет индексов, но `iter` + `next` работают для любого перебираемого.",
    lines=[
        ("it = iter(items)", "Итератор из чего угодно."),
        ("return [next(it), next(it)]", "Два первых."),
    ],
    mistake="`items[:2]` — не сработает для итератора."),

f"{P}-m1-l1-e5": x(
    idea="`__next__` отдаёт следующее значение или бросает `StopIteration` — сигнал «конец» для `for`.",
    lines=[
        ("if self.n <= 0:\n            raise StopIteration", "Числа кончились."),
        ("self.n -= 1", "Сдвигаем счётчик."),
        ("return self.n + 1", "Значение до уменьшения."),
    ],
    mistake="`return None` в конце — `for` будет крутиться бесконечно."),

f"{P}-m1-l1-e6": x(
    idea="Итератор возвращает из `iter` сам себя. Список — итерируемый: `iter` каждый раз даёт новый итератор. `__next__` есть только у итератора.",
    lines=[
        ("print(iter(it) is it, iter(nums) is iter(nums))", "Тот же / два новых."),
        ('print(hasattr(nums, "__next__"), hasattr(it, "__next__"))', "У списка нет `__next__`."),
    ],
    mistake="Путать итерируемое (можно перебрать) и итератор (помнит позицию)."),

f"{P}-m1-l1-e7": x(
    idea="Так устроен `for` внутри: брать `next`, пока не прилетит `StopIteration`.",
    lines=[
        ("it = iter(iterable)", "Итератор."),
        ("total += next(it)", "Следующий элемент."),
        ("except StopIteration:\n            return total", "Кончились — ответ."),
    ],
    mistake="Не ловить `StopIteration` — функция упадёт в конце."),

f"{P}-m1-l1-e8": x(
    idea="`next(it, None)` пропускает первый элемент и не падает на пустом входе.",
    lines=[
        ("next(it, None)", "Заголовок выброшен."),
        ("return list(it)", "Остаток."),
    ],
    mistake="`lines[1:]` — не сработает для итератора."),

f"{P}-protocol-e1": x(
    idea="Объект, который сам себе итератор, одноразовый: `current` не сбрасывается.",
    lines=[
        ("self.current += 1\n        return self.current", "1, 2, 3."),
        ("print(list(u))", "Счётчик уже на 3 — пусто."),
    ],
    mistake="Ожидать второй `[1, 2, 3]`."),

f"{P}-protocol-e2": x(
    idea="Итерируемый класс возвращает новый итератор из `__iter__` — его можно перебирать сколько угодно.",
    lines=[
        ("return iter(self.songs)", "Новый итератор каждый раз."),
        ("print(list(p), list(p))", "Два полных списка."),
    ],
    mistake="Думать, что `Playlist` одноразовый."),

f"{P}-protocol-e3": x(
    idea="Цикл `for` — это `while True` + `next` + перехват `StopIteration`.",
    lines=[
        ("item = next(it)", "Следующий."),
        ('except StopIteration:\n        print("конец")\n        break', "Элементы кончились."),
        ('print("элемент", item)', "Обработка."),
    ],
    mistake="Ожидать «конец» после каждого элемента."),

f"{P}-protocol-e4": x(
    idea="Запомнить текущее, сдвинуть, вернуть запомненное.",
    lines=[
        ("if self.current > self.stop:\n            raise StopIteration", "`stop` включительно."),
        ("value = self.current\n        self.current += 1\n        return value", "Возвращаем до сдвига."),
    ],
    mistake="`>=` — потеряется `stop`."),

f"{P}-protocol-e5": x(
    idea="Общее число шагов известно заранее; индекс по кругу — остаток от деления.",
    lines=[
        ("self.total = len(items) * times", "Сколько выдать."),
        ("value = self.items[self.index % len(self.items)]", "По кругу."),
        ("self.index += 1", "Следующий."),
    ],
    mistake="Без `%` — `IndexError` на втором круге."),

f"{P}-protocol-e6": x(
    idea="`__iter__` с `yield` — генератор: каждый вызов создаёт новый итератор, объект можно перебирать многократно.",
    lines=[
        ("current = self.start", "Локальная — своя на каждый перебор."),
        ("while current < self.stop:", "`stop` не включён, как у `range`."),
        ("yield current", "Выдаём."),
    ],
    mistake="Хранить `current` в `self` — второй перебор начнётся с конца."),

f"{P}-protocol-e7": x(
    idea="Позиция сдвигается на `size`; срез сам обрежет последнюю страницу.",
    lines=[
        ("if self.pos >= len(self.items):\n            raise StopIteration", "Всё выдали."),
        ("page = self.items[self.pos:self.pos + self.size]", "Страница."),
        ("self.pos += self.size", "Следующая."),
    ],
    mistake="Проверять `pos + size > len` — потеряется короткая последняя страница."),

f"{P}-protocol-e8": x(
    idea="Буфер хранит подсмотренный элемент. `_EMPTY` — метка «пусто», отличимая от `None`.",
    lines=[
        ("if self.buffer is not _EMPTY:\n            value, self.buffer = self.buffer, _EMPTY\n            return value", "Сначала отдаём подсмотренное."),
        ("return next(self.it)", "Иначе — из источника."),
        ("self.buffer = next(self.it, _EMPTY)", "Подсмотреть и запомнить."),
        ("return default if self.buffer is _EMPTY else self.buffer", "Кончились — default."),
    ],
    mistake="Использовать `None` как метку — поток с `None` сломается."),

f"{P}-m1-l2-e1": x(
    idea="Функция с `yield` возвращает генератор; каждый `next` доходит до следующего `yield`.",
    lines=[
        ("print(list(gen()))", "Все три."),
        ("print(next(g), next(g))", "Новый генератор — с начала."),
    ],
    mistake="Ожидать `2 3` — `g` новый."),

f"{P}-m1-l2-e2": x(
    idea="Код генератора выполняется кусками: от одного `yield` до следующего, только по запросу.",
    lines=[
        ("g = gen()", "Тело не выполняется."),
        ("print(next(g))", "До первого `yield`: «старт», A."),
        ("print(next(g))", "До второго: «середина», B."),
        ('print("конец")', "Не выполнится — третьего `next` не было."),
    ],
    mistake="Ожидать «старт» раньше «создан»."),

f"{P}-m1-l2-e3": x(
    idea="`yield` внутри цикла с условием выдаёт только подходящие значения.",
    lines=[
        ("if i % 2 == 0:\n            yield i", "Чётные."),
        ("print(sum(evens(10)))", "0 + 2 + 4 + 6 + 8."),
    ],
    mistake="Включить 10 — `range(10)` до 9."),

f"{P}-m1-l2-e4": x(
    idea="Вместо списка — `yield` по одному.",
    lines=[
        ("for i in range(1, n + 1):", "От 1 до n."),
        ("yield i * i", "Квадрат."),
    ],
    mistake="`range(n)` — начнётся с 0."),

f"{P}-m1-l2-e5": x(
    idea="Бесконечный генератор — `while True` с `yield`; значения считаются только по запросу.",
    lines=[
        ("a, b = 0, 1", "Начало."),
        ("yield a", "Текущее."),
        ("a, b = b, a + b", "Одновременное присваивание."),
    ],
    mistake="`a = b; b = a + b` — `a` уже изменился."),

f"{P}-m1-l2-e6": x(
    idea="Шаг `range` равен размеру куска; срез обрезает последний.",
    lines=[
        ("for i in range(0, len(items), size):", "0, size, 2·size…"),
        ("yield items[i:i + size]", "Кусок."),
    ],
    mistake="`range(len(items) // size)` — потеряется хвост."),

f"{P}-m1-l2-e7": x(
    idea="После цикла можно выдать ещё значение — генератор продолжается.",
    lines=[
        ("while n > 0:\n        yield n\n        n -= 1", "Отсчёт."),
        ('yield "старт!"', "Финал."),
    ],
    mistake="`return \"старт!\"` — значение не попадёт в перебор."),

f"{P}-m1-l2-e8": x(
    idea="Состояние — локальная переменная генератора; она живёт между `yield`.",
    lines=[
        ("total += n", "Накопили."),
        ("yield total", "Выдали сумму."),
    ],
    mistake="Выдавать `n` вместо `total`."),

f"{P}-lazy-e1": x(
    idea="Создание генератора не запускает его тело.",
    lines=[
        ("g = gen()", "Ничего не печатается."),
        ("print(next(g))", "Теперь «начал», потом 1."),
    ],
    mistake="Ожидать «начал» первым."),

f"{P}-lazy-e2": x(
    idea="Генератор одноразовый; новый вызов функции — новый генератор.",
    lines=[
        ("print(sum(g), sum(g))", "Второй `sum` — по пустому."),
        ("print(sum(nums()), sum(nums()))", "Два разных генератора."),
    ],
    mistake="Ожидать `3 3` в первой строке."),

f"{P}-lazy-e3": x(
    idea="`return` завершает генератор; значение попадает в `StopIteration.value`, но не в перебор.",
    lines=[
        ('return "итог"', "Конец."),
        ('print("стоп, значение:", e.value)', "Значение `return`."),
        ("print(list(limited()))", "Только `a`."),
    ],
    mistake="Ожидать «итог» в списке."),

f"{P}-lazy-e4": x(
    idea="Бесконечный генератор безопасен, пока берём конечное число элементов.",
    lines=[
        ('yield f"{prefix}-{n}"', "Следующий id."),
        ("return [next(gen) for _ in range(n)]", "Ровно `n`."),
    ],
    mistake="`list(ids(\"u\"))` — бесконечный цикл."),

f"{P}-lazy-e5": x(
    idea="`next` берёт первый элемент генератора — перебор останавливается на совпадении.",
    lines=[("return next((x for x in items if predicate(x)), None)", "Нет совпадений — `None`.")],
    mistake="`[x for ...][0]` — проверит все элементы и упадёт на пустом."),

f"{P}-lazy-e6": x(
    idea="Запись в журнал — перед `yield`: она случается только при запросе элемента.",
    lines=[
        ('log.append(f"выдаю {x}")', "Перед выдачей."),
        ("yield x", "Пауза до следующего `next`."),
    ],
    mistake="Сначала записать всё в журнал, потом выдавать — теряется ленивость."),

f"{P}-lazy-e7": x(
    idea="Значение `return` генератора достаётся из `StopIteration.value`.",
    lines=[
        ("return count", "Уходит в `StopIteration`."),
        ("items.append(next(gen))", "Собираем элементы."),
        ("except StopIteration as e:\n            return items, e.value", "Конец и итог."),
    ],
    mistake="`list(gen)` — значение `return` потеряется."),

f"{P}-lazy-e8": x(
    idea="Длину последовательности считаем `sum(1 for ...)` — без списка. Ключ `(длина, -k)` при равенстве выбирает меньшее число.",
    lines=[
        ("while n != 1:\n        yield n", "До единицы."),
        ("n = n // 2 if n % 2 == 0 else 3 * n + 1", "Шаг Коллатца."),
        ("yield 1", "Единица тоже в последовательности."),
        ("return max(range(1, limit + 1), key=lambda k: (sum(1 for _ in collatz(k)), -k))", "Самая длинная, при равенстве — меньший старт."),
    ],
    mistake="`len(collatz(k))` — у генератора нет длины."),

# ===== Модуль 2. Выражения и конвейеры =====

f"{P}-m2-l1-e1": x(
    idea="Круглые скобки вместо квадратных дают генератор — ленивый и одноразовый.",
    lines=[
        ("g = (x * 10 for x in range(3))", "Не список."),
        ("print(list(g))", "Все значения."),
        ("print(list(g))", "Уже пусто."),
    ],
    mistake="Ожидать два одинаковых списка."),

f"{P}-m2-l1-e2": x(
    idea="Генератор прямо внутри `sum`/`any`/`all` — без лишнего списка.",
    lines=[
        ("print(sum(n for n in nums if n > 0))", "3 + 8 + 4."),
        ("print(any(n < 0 for n in nums))", "Есть −1."),
        ("print(all(n < 10 for n in nums))", "Все меньше 10."),
    ],
    mistake="Сложить и −1."),

f"{P}-m2-l1-e3": x(
    idea="`any` останавливается на первом `True` — генератор дальше не считается.",
    lines=[
        ('print("считаю", x)', "Для 1 и 2."),
        ("return x > 1", "2 > 1 — `True`, стоп."),
    ],
    mistake="Ожидать «считаю 3» и «считаю 4»."),

f"{P}-m2-l1-e4": x(
    idea="Генератор длин внутри `sum`.",
    lines=[("return sum(len(w) for w in words)", "Пустой список — 0.")],
    mistake="`len(words)` — число слов."),

f"{P}-m2-l1-e5": x(
    idea="`any` с генератором — остановится на первой ошибке.",
    lines=[("return any(line.startswith(\"ERROR\") for line in log_lines)", "Хоть одна.")],
    mistake="`\"ERROR\" in line` — поймает и «NO_ERROR»."),

f"{P}-m2-l1-e6": x(
    idea="`all` — все элементы подходят; для пустого списка `True`.",
    lines=[("return all(r[\"status\"] == \"passed\" for r in results)", "Остановится на первом провале.")],
    mistake="Сравнивать `results == \"passed\"`."),

f"{P}-m2-l1-e7": x(
    idea="Если генератор — единственный аргумент, лишние скобки не нужны. Работают `max`, `join`, `sorted`, `dict`.",
    lines=[
        ("print(max(len(w) for w in words))", "Самое длинное — 6."),
        ('print(", ".join(w.upper() for w in words))', "Склейка."),
        ("print(sorted((len(w), w) for w in words))", "Кортежи — по длине."),
        ("print(dict((w, len(w)) for w in words))", "Пары → словарь."),
    ],
    mistake="Ожидать «собака» от `max` — сравниваются длины."),

f"{P}-m2-l1-e8": x(
    idea="Считаем единицы для подходящих — количество без списка.",
    lines=[("return sum(1 for w in words if len(w) > n)", "По единице на слово.")],
    mistake="`len([w for w in words if ...])` — лишний список."),

f"{P}-pipeline-e1": x(
    idea="Конвейер: каждый генератор берёт из предыдущего. Работа идёт только когда `sum` запрашивает значения.",
    lines=[
        ("stripped = (s.strip() for s in lines)", "Без пробелов."),
        ("non_empty = (s for s in stripped if s)", "Без пустых."),
        ("numbers = (int(s) for s in non_empty if s.isdigit())", "`abc` отброшен."),
        ("print(sum(numbers))", "10 + 25 + 7."),
    ],
    mistake="Ожидать ошибку на `abc` — его отсеял `isdigit`."),

f"{P}-pipeline-e2": x(
    idea="Элементы проходят конвейер по одному: взял → удвоил → получил, потом следующий.",
    lines=[
        ('print("взял", x)', "Источник."),
        ('print("удвоил", x)', "Сразу следом."),
        ('print("получил", result)', "И до потребителя."),
    ],
    mistake="Ожидать «взял 1, 2, 3» подряд, как со списками."),

f"{P}-pipeline-e3": x(
    idea="Бесконечный источник безопасен: берём лишь столько, сколько попросили.",
    lines=[
        ("squares = (n * n for n in numbers())", "1, 4, 9, …"),
        ("big = (s for s in squares if s > 50)", "Первый — 64."),
        ("print(next(big), next(big))", "Два значения."),
    ],
    mistake="Ожидать зависание."),

f"{P}-pipeline-e4": x(
    idea="Три маленьких генератора и сборка вложенными вызовами; `dict` принимает поток пар.",
    lines=[
        ("yield line.strip()", "Очистка."),
        ('if line and not line.startswith("#"):', "Пропуск пустых и комментариев."),
        ('key, value = line.split("=", 1)', "По первому `=`."),
        ("return dict(parse(skip_comments(read(lines))))", "Конвейер."),
    ],
    mistake="Перепутать порядок: `skip_comments` до `read` не уберёт строки из пробелов."),

f"{P}-pipeline-e5": x(
    idea="Элемент по очереди проходит через все функции.",
    lines=[
        ("for f in funcs:\n            item = f(item)", "Результат одной — вход следующей."),
        ("yield item", "Итог."),
    ],
    mistake="`yield` внутри внутреннего цикла — выдаст промежуточные значения."),

f"{P}-pipeline-e6": x(
    idea="Фильтр по двум условиям, наружу — только имена.",
    lines=[
        ('if r["status"] == "failed" and r["duration"] > 1:', "Упал и долгий."),
        ('yield r["name"]', "Имя."),
    ],
    mistake="`return [...]` — не генератор."),

f"{P}-pipeline-e7": x(
    idea="Множество увиденных — выдаём только новое, сразу.",
    lines=[
        ("if x not in seen:", "Новый."),
        ("seen.add(x)\n            yield x", "Запомнить и выдать."),
    ],
    mistake="`set(items)` — не ленив и теряет порядок."),

f"{P}-pipeline-e8": x(
    idea="`deque(maxlen=size)` — окно: новое число вытесняет самое старое.",
    lines=[
        ("window = deque(maxlen=size)", "Окно."),
        ("window.append(n)", "Сдвиг."),
        ("if len(window) == size:", "Окно заполнено."),
        ("yield round(sum(window) / size, 2)", "Среднее."),
    ],
    mistake="Выдавать среднее, пока окно неполное."),

f"{P}-m2-l2-e1": x(
    idea="`yield from` выдаёт все элементы другого перебираемого по очереди.",
    lines=[
        ("yield from [1, 2]", "1, 2."),
        ('yield from "ab"', "Строка — по символу."),
    ],
    mistake="Ожидать `'ab'` одним элементом."),

f"{P}-m2-l2-e2": x(
    idea="`count(10, 5)` — бесконечный счёт с шагом; `islice` берёт первые 4.",
    lines=[("print(list(islice(count(10, 5), 4)))", "10, 15, 20, 25.")],
    mistake="`list(count(...))` без `islice` — бесконечность."),

f"{P}-m2-l2-e3": x(
    idea="`product` — все комбинации, как вложенные циклы: правый меняется быстрее.",
    lines=[("for browser, os in product([\"chrome\", \"firefox\"], [\"win\", \"mac\"]):", "4 пары.")],
    mistake="Ожидать только совпадающие по индексу пары, как у `zip`."),

f"{P}-m2-l2-e4": x(
    idea="`yield from inner` — все элементы вложенного списка.",
    lines=[
        ("for inner in lists:", "Каждый вложенный."),
        ("yield from inner", "Пустой — ничего."),
    ],
    mistake="`yield inner` — выдаст списки целиком."),

f"{P}-m2-l2-e5": x(
    idea="`partition(\" \")` делит по первому пробелу на три части.",
    lines=[
        ('level, _, text = line.partition(" ")', "Уровень, пробел, текст."),
        ('if level == "ERROR":\n            yield text', "Только ошибки."),
    ],
    mistake="`split()` — текст разобьётся на слова."),

f"{P}-m2-l2-e6": x(
    idea="`product` перебирает все пары в нужном порядке.",
    lines=[("return [f\"{b}@{s}\" for b, s in product(browsers, sizes)]", "Все размеры первого браузера — первыми.")],
    mistake="`zip` — только пары с одинаковым индексом."),

f"{P}-m2-l2-e7": x(
    idea="Рекурсивный генератор: узел, затем `yield from` для каждого ребёнка с глубиной +1.",
    lines=[
        ('yield "  " * depth + tree["name"]', "Сам узел."),
        ("yield from walk(child, depth + 1)", "Поддерево."),
    ],
    mistake="`walk(child, ...)` без `yield from` — вызов создаст генератор и ничего не выдаст."),

f"{P}-m2-l2-e8": x(
    idea="Список или кортеж — рекурсивно разворачиваем; остальное (и строки) — выдаём как есть.",
    lines=[
        ("if isinstance(item, (list, tuple)):", "Вложенная коллекция."),
        ("yield from deep_flatten(item)", "Рекурсия."),
        ("yield item", "Лист."),
    ],
    mistake="Проверять «перебираемое вообще» — строки разложатся на символы бесконечно."),

f"{P}-itertools-e1": x(
    idea="`chain` склеивает потоки, `accumulate` — накопительные суммы, `pairwise` — соседние пары.",
    lines=[
        ('print(list(chain([1, 2], (3,), "ab")))', "Подряд."),
        ("print(list(accumulate([1, 2, 3, 4])))", "1, 1+2, …"),
        ("print(list(pairwise([10, 13, 19])))", "Пар на одну меньше."),
    ],
    mistake="Ожидать `(19, None)` в конце."),

f"{P}-itertools-e2": x(
    idea="`takewhile` берёт, пока условие истинно; `dropwhile` пропускает, пока истинно, дальше берёт всё. `batched` режет на кортежи.",
    lines=[
        ("print(list(takewhile(lambda n: n % 2, nums)))", "До первого чётного."),
        ("print(list(dropwhile(lambda n: n % 2, nums)))", "С 8 — всё, включая нечётные."),
        ('print(list(batched("abcdefg", 3)))', "Последний — короче."),
    ],
    mistake="Думать, что `dropwhile` фильтрует все нечётные."),

f"{P}-itertools-e3": x(
    idea="`groupby` группирует только **соседние** одинаковые. `combinations` — пары без повторов и без учёта порядка.",
    lines=[
        ("print([(k, len(list(g))) for k, g in groupby(log)])", "Каждая серия отдельно."),
        ('print(list(combinations(["api", "ui", "db"], 2)))', "3 пары."),
    ],
    mistake="Ожидать `('ERROR', 3)` — `groupby` не сортирует."),

f"{P}-itertools-e4": x(
    idea="`chain(*logs)` — все списки подряд.",
    lines=[("return list(chain(*logs))", "`*` распаковывает списки аргументами.")],
    mistake="`chain(logs)` — получится список списков."),

f"{P}-itertools-e5": x(
    idea="`pairwise` даёт соседние пары — разница `b - a`.",
    lines=[("return [b - a for a, b in pairwise(values)]", "Следующее минус предыдущее.")],
    mistake="`a - b` — знак обратный."),

f"{P}-itertools-e6": x(
    idea="`groupby` разбивает на серии; длины fail-серий, максимум с `default=0`.",
    lines=[("return max((len(list(g)) for k, g in groupby(results) if k == \"fail\"), default=0)", "Нет fail — 0.")],
    mistake="`results.count(\"fail\")` — все провалы, а не серия подряд."),

f"{P}-itertools-e7": x(
    idea="`batched` выдаёт кортежи — превращаем в списки.",
    lines=[("return [list(b) for b in batched(ids, size)]", "Пачки.")],
    mistake="Вернуть кортежи — просили списки."),

f"{P}-itertools-e8": x(
    idea="`accumulate` даёт баланс после каждой операции; `min(..., default=0)` — для пустого.",
    lines=[
        ("balances = list(accumulate(operations))", "Нарастающий итог."),
        ("return balances, min(balances, default=0)", "Минимум."),
    ],
    mistake="`min(balances)` без `default` — ошибка на пустом."),

# ===== Модуль 3. Продвинутое и практика =====

f"{P}-send-e1": x(
    idea="`send` возобновляет генератор и передаёт значение — оно становится результатом выражения `yield`. Первый `next` доводит до первого `yield`.",
    trace=[
        ("print(next(g))", "received = None", "получил None"),
        ('print(g.send("привет"))', "received = привет", "получил привет"),
        ("print(g.send(42))", "received = 42", "получил 42"),
    ],
    mistake="`send` до первого `next` — ошибка."),

f"{P}-send-e2": x(
    idea="Генератор хранит сумму и счётчик между вызовами; `send` отдаёт число, получает среднее.",
    lines=[
        ("next(a)", "Запуск до первого `yield`."),
        ("value = yield avg", "Получили значение."),
        ("avg = total / count", "10, 15, 30."),
    ],
    mistake="Забыть `next(a)` — `TypeError` на первом `send`."),

f"{P}-send-e3": x(
    idea="`close()` завершает генератор на текущем `yield` — срабатывает `finally`.",
    lines=[
        ("print(next(r), next(r))", "«открыл», 1 2."),
        ("r.close()", "`finally` — «закрыл»."),
    ],
    mistake="Думать, что незавершённый генератор не делает уборку."),

f"{P}-send-e4": x(
    idea="`yield` выдаёт длину и принимает новое значение.",
    lines=[
        ("value = yield len(items)", "Выдать длину, получить значение."),
        ("items.append(value)", "Накопить."),
    ],
    mistake="Добавлять `None` от первого `next` — длина собьётся."),

f"{P}-send-e5": x(
    idea="Состояние — текущий максимум; `None` — ещё ничего не было.",
    lines=[
        ("value = yield best", "Выдать максимум, получить число."),
        ("if best is None or value > best:\n            best = value", "Обновить."),
    ],
    mistake="Начать с `best = 0` — отрицательные числа не станут максимумом."),

f"{P}-send-e6": x(
    idea="`finally` вокруг `yield` срабатывает и при обычном завершении, и при `close()`.",
    lines=[
        ('log.append("open")', "Старт."),
        ("yield line", "Может прерваться на `close`."),
        ('finally:\n        log.append("close")', "Всегда."),
    ],
    mistake="Записать «close» после цикла без `finally` — при `close()` не выполнится."),

f"{P}-send-e7": x(
    idea="`next()` отправляет `None` — значит «дальше»; `send(\"reset\")` — сброс.",
    lines=[
        ("command = yield COLORS[i]", "Цвет наружу, команда внутрь."),
        ('if command == "reset":\n            i = 0', "Сброс."),
        ("i = (i + 1) % len(COLORS)", "По кругу."),
    ],
    mistake="Сбросить на `i = -1` — после reset выдастся не красный."),

f"{P}-send-e8": x(
    idea="Генератор принимает запись и выдаёт ошибки предыдущей проверки.",
    lines=[
        ("record = yield errors", "Выдали ошибки, получили запись."),
        ("errors = [field for field, check in rules.items() if field not in record or not check(record[field])]", "Нет поля или проверка не прошла."),
    ],
    mistake="Сначала `check(record[field])` — `KeyError` на отсутствующем поле."),

f"{P}-bigdata-e1": x(
    idea="Генератор по файлу держит в памяти одну строку.",
    lines=[
        ("f.write(f\"{i} {'ERROR' if i % 250 == 0 else 'INFO'}\\n\")", "ERROR на 0, 250, 500, 750."),
        ("yield int(line.split()[0])", "Номер строки."),
    ],
    mistake="Забыть 0 — `0 % 250 == 0`."),

f"{P}-bigdata-e2": x(
    idea="Ленивая пагинация: следующая страница запрашивается, только когда кончилась текущая.",
    lines=[
        ('print("запрос страницы", page)', "Страница 1: 1, 2, 3."),
        ('yield from resp["items"]', "Страница 2: 4, 5, 6."),
        ("if item > 4:\n        break", "На 5 остановились — третья страница не нужна."),
    ],
    mistake="Ожидать запрос третьей страницы."),

f"{P}-bigdata-e3": x(
    idea="Читаем кусками фиксированного размера, пустой кусок — конец.",
    lines=[
        ("block = f.read(size)", "До 3 символов."),
        ("if not block:\n            return", "Конец потока."),
        ("yield block", "Кусок."),
    ],
    mistake="Ожидать `'жз '` — последний кусок просто короче."),

f"{P}-bigdata-e4": x(
    idea="Заголовок — первая строка, дальше каждая строка → словарь через `zip`.",
    lines=[
        ('header = f.readline().rstrip("\\n").split(",")', "Названия колонок."),
        ('values = line.rstrip("\\n").split(",")', "Значения."),
        ("yield dict(zip(header, values))", "Колонка → значение."),
    ],
    mistake="Не убрать `\\n` — последняя колонка станет `\"значение\\n\"`."),

f"{P}-bigdata-e5": x(
    idea="Запрос страницы — только когда предыдущая выдана полностью.",
    lines=[
        ("items = fetch(page)", "Запрос."),
        ("if not items:\n            return", "Пустая — конец."),
        ("yield from items", "По одному."),
        ("page += 1", "Следующая."),
    ],
    mistake="Сначала собрать все страницы в список — теряется ленивость."),

f"{P}-bigdata-e6": x(
    idea="Двоичный режим и чтение кусками — работает для файлов любого размера.",
    lines=[
        ('with open(path, "rb") as f:', "Байты."),
        ("block = f.read(size)", "До `size` байт."),
        ("if not block:\n                return", "Конец файла."),
    ],
    mistake="`f.read()` без размера — весь файл в памяти."),

f"{P}-bigdata-e7": x(
    idea="`Counter` принимает генератор — один проход; `most_common` даёт топ.",
    lines=[
        ('counts = Counter(line[6:] for line in lines if line.startswith("ERROR "))', "`ERROR ` — 6 символов."),
        ("return counts.most_common(n)", "Пары (текст, количество)."),
    ],
    mistake="Перебирать `lines` дважды — генератор второй раз пуст."),

f"{P}-bigdata-e8": x(
    idea="Слияние двух отсортированных: держим текущий элемент каждого, выдаём меньший. `_END` — метка конца.",
    lines=[
        ("x, y = next(ia, _END), next(ib, _END)", "Первые элементы."),
        ("if x <= y:\n            yield x\n            x = next(ia, _END)", "Меньший — наружу."),
        ("while x is not _END:\n        yield x\n        x = next(ia, _END)", "Хвост первого."),
        ("while y is not _END:\n        yield y\n        y = next(ib, _END)", "Хвост второго."),
    ],
    mistake="`sorted(chain(a, b))` — всё в памяти."),

f"{P}-memory-e1": x(
    idea="Список хранит все элементы, генератор — только своё состояние. Результат вычислений одинаковый.",
    lines=[
        ("print(sys.getsizeof(big_list) > 100_000, sys.getsizeof(big_gen) < 500)", "Сотни килобайт против пары сотен байт."),
        ("print(sum(big_list) == sum(big_gen))", "Одинаковая сумма."),
    ],
    mistake="Думать, что генератор хранит значения заранее."),

f"{P}-memory-e2": x(
    idea="У генератора нет длины и индексов. Нужны — превращаем в список.",
    lines=[
        ("for op in [lambda: len(g), lambda: g[0]]:", "Обе операции — `TypeError`."),
        ("items = list(g)", "Теперь можно."),
        ("print(len(items), items[0], items[-1])", "0 и 8."),
    ],
    mistake="Ожидать, что неудачные попытки «съели» элементы."),

f"{P}-memory-e3": x(
    idea="Один генератор — один проход. `tee` делает два независимых итератора, `list` — многоразовые данные.",
    lines=[
        ('print(max(g), min(g, default="пусто"))', "`max` съел всё."),
        ("a, b = tee(nums())", "Два потока."),
        ("data = list(nums())", "Список — сколько угодно проходов."),
    ],
    mistake="Ожидать `3 1` в первой строке."),

f"{P}-memory-e4": x(
    idea="Все показатели за один проход: минимум, максимум, сумма и счётчик одновременно.",
    lines=[
        ("lo = n if lo is None or n < lo else lo", "Минимум."),
        ("hi = n if hi is None or n > hi else hi", "Максимум."),
        ("if count == 0:\n        return None, None, None", "Пустой вход."),
        ("return lo, hi, total / count", "Среднее."),
    ],
    mistake="`min(numbers), max(numbers)` — второй проход по пустому генератору."),

f"{P}-memory-e5": x(
    idea="Нужны два прохода — сначала материализуем в список.",
    lines=[
        ("values = list(values)", "Теперь можно перебирать много раз."),
        ("top = max(values)", "Первый проход."),
        ("return [v / top for v in values]", "Второй."),
    ],
    mistake="Оставить генератор — после `max` он пуст, результат `[]`."),

f"{P}-memory-e6": x(
    idea="Считаем единицы при переборе — без списка.",
    lines=[("return sum(1 for _ in iterable)", "По одной на элемент.")],
    mistake="`len(list(iterable))` — список в памяти."),

f"{P}-memory-e7": x(
    idea="`tee` даёт два независимых итератора, на каждом свой фильтр.",
    lines=[
        ("a, b = tee(iterable)", "Две копии потока."),
        ("return (x for x in a if predicate(x)), (x for x in b if not predicate(x))", "Два ленивых фильтра."),
    ],
    mistake="Оба фильтра по одному итератору — они будут отбирать элементы друг у друга."),

f"{P}-memory-e8": x(
    idea="Много проходов — список; один проход по большим данным — генератор.",
    lines=[
        ('if passes > 1:\n        return "список"', "Генератор одноразовый."),
        ('if data_size > 10_000:\n        return "генератор"', "Экономия памяти."),
        ("return sum(i * i for i in range(1, n + 1))", "Без списка."),
    ],
    mistake="Проверять размер раньше проходов — для многих проходов посоветуешь генератор."),

f"{P}-testing-e1": x(
    idea="`count(1)` — бесконечный счётчик: каждый вызов фабрики получает новый номер.",
    lines=[
        ("_ids = count(1)", "1, 2, 3…"),
        ("n = next(_ids)", "Следующий номер."),
        ('print(make_user()["email"])', "Второй вызов — user2."),
    ],
    mistake="Ожидать user1 во второй строке."),

f"{P}-testing-e2": x(
    idea="Генератор тестовых случаев: пары «вход, ожидание».",
    lines=[
        ('return "@" in s and not s.startswith("@")', "Проверяемая функция."),
        ("for value, expected in cases():", "Распаковка пар."),
        ('status = "ok" if is_email(value) == expected else "FAIL"', "Сравнение с ожиданием."),
    ],
    mistake="Думать, что `False` в ожидании — провал."),

f"{P}-testing-e3": x(
    idea="Так устроены фикстуры pytest: до `yield` — подготовка, после — уборка.",
    lines=[
        ("db = next(gen)", "Подготовка, получили данные."),
        ("log.append(f\"тест: {db['users']}\")", "Тест."),
        ("next(gen, None)", "Уборка; `None` гасит `StopIteration`."),
    ],
    mistake="Забыть второй `next` — «отключение» не выполнится."),

f"{P}-testing-e4": x(
    idea="Бесконечная фабрика с номером в замыкании генератора.",
    lines=[
        ('yield {"id": n, "login": f"{prefix}_{n}"}', "Новый словарь."),
        ("n += 1", "Следующий номер."),
    ],
    mistake="Один и тот же словарь — изменения одного теста попадут в другой."),

f"{P}-testing-e5": x(
    idea="Шесть граничных значений; множество убирает повторы при узком диапазоне.",
    lines=[
        ("for v in (low - 1, low, low + 1, high - 1, high, high + 1):", "В нужном порядке."),
        ("if v not in seen:", "Без повторов."),
    ],
    mistake="`set(...)` — порядок потеряется."),

f"{P}-testing-e6": x(
    idea="`product(*значения)` — все комбинации; `zip` с ключами превращает кортеж в словарь.",
    lines=[
        ("keys = list(params)", "Имена параметров."),
        ("for values in product(*params.values()):", "Каждая комбинация."),
        ("yield dict(zip(keys, values))", "Словарь параметров."),
    ],
    mistake="`product(params.values())` без `*` — один аргумент, комбинаций не будет."),

f"{P}-testing-e7": x(
    idea="Подготовка — первый `next`; уборка — второй `next` в `finally`.",
    lines=[
        ("value = next(gen)", "Данные фикстуры."),
        ("return test_func(value)", "Тест."),
        ("finally:\n        next(gen, None)", "Уборка даже при падении."),
    ],
    mistake="`next(gen)` без `None` — `StopIteration` в `finally`."),

f"{P}-testing-e8": x(
    idea="Задержка растёт в `factor` раз, но выдаётся не больше `max_delay`. `islice` берёт первые N.",
    lines=[
        ("yield min(delay, max_delay)", "Потолок."),
        ("delay *= factor", "Рост."),
        ("return list(islice(retry_delays(), attempts))", "Первые `attempts`."),
    ],
    mistake="`list(retry_delays())` — бесконечность."),
}
