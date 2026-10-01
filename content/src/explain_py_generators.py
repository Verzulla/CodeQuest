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
}
