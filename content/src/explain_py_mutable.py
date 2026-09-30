"""Тема «Изменяемость и копии» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "mut"

EXPLAIN = {

# ===== Модуль 1. Объекты и ссылки =====

f"{P}-types-e1": x(
    idea="Список меняется на месте: `append` и присваивание по индексу не создают новый объект — `id` прежний.",
    lines=[
        ("nums.append(4)", "Тот же список."),
        ("nums[0] = 100", "Тот же список."),
        ("print(nums, id(nums) == before)", "`id` не изменился."),
    ],
    mistake="Думать, что изменение создаёт новый список."),

f"{P}-types-e2": x(
    idea="Строку менять нельзя. Методы строк возвращают новую строку — с новым `id`.",
    lines=[
        ('s[0] = "К"', "`TypeError`."),
        ("s = s.upper()", "Новая строка, имя `s` — на неё."),
        ("print(s, id(s) == before)", "Другой объект."),
    ],
    mistake="Ожидать `True` — `upper` не меняет старую строку."),

f"{P}-types-e3": x(
    idea="Неизменяемые встроенные типы хешируемы; `list`, `dict`, `set` — нет.",
    lines=[
        ("hash(v)", "Работает — неизменяемый."),
        ('except TypeError:\n        kind = "изменяемый"', "Список, словарь, множество."),
        ("print(type(v).__name__, kind)", "`None` и `True` — тоже неизменяемые."),
    ],
    mistake="Считать `frozenset` изменяемым, как `set`."),

f"{P}-types-e4": x(
    idea="`isinstance` с кортежем типов — одна проверка на все.",
    lines=[("return isinstance(value, (list, dict, set, bytearray))", "Любой из четырёх.")],
    mistake="`type(value) == list` — не сработает для наследников."),

f"{P}-types-e5": x(
    idea="Строки не меняются — каждое слово даёт новую строку.",
    lines=[("return [w.capitalize() for w in words]", "Новый список новых строк.")],
    mistake="`w[0] = w[0].upper()` — `TypeError`."),

f"{P}-types-e6": x(
    idea="Новая строка: часть до, новый символ, часть после.",
    lines=[("return s[:index] + char + s[index + 1:]", "Пропускаем символ на `index`.")],
    mistake="`s[index] = char` — строку менять нельзя."),

f"{P}-types-e7": x(
    idea="Кортеж + кортеж = новый кортеж. Кортеж из одного элемента — с запятой.",
    lines=[("return tpl + (item,)", "`(item,)` — кортеж, `(item)` — просто значение.")],
    mistake="`tpl + (item)` — `TypeError`: к кортежу нельзя прибавить число."),

f"{P}-types-e8": x(
    idea="Проверка через `hash` в `try`; `else` — ветка без ошибки.",
    lines=[
        ("hash(v)", "Проба."),
        ("except TypeError:\n            mutable.append(v)", "Нехешируемый."),
        ("else:\n            immutable.append(v)", "Хешируемый."),
    ],
    mistake="Добавлять в `immutable` внутри `try` — сработает, но смешивает пробу и результат."),

f"{P}-refs-e1": x(
    idea="`b = a` не копирует — обе переменные указывают на один список.",
    lines=[
        ("b = a", "Вторая ссылка."),
        ("b.append(4)", "Меняем общий объект."),
        ("print(a is b, a == b)", "Один объект — значит, и равны."),
    ],
    mistake="Ожидать `[1, 2, 3]`."),

f"{P}-refs-e2": x(
    idea="`b + [3]` создаёт новый список, и `b` переключается на него. Для чисел `+=` тоже создаёт новый объект.",
    lines=[
        ("b = b + [3]", "Новый список; `a` не тронут."),
        ("print(a, b, a is b)", "Разные объекты."),
        ("y += 1", "Новое число, `x` прежний."),
    ],
    mistake="Путать `b = b + [3]` с `b += [3]` — второе меняет список на месте."),

f"{P}-refs-e3": x(
    idea="`==` сравнивает значения, `is` — один ли это объект. `None` — единственный, `[]` каждый раз новый.",
    lines=[
        ("print(a == b, a is b, a is c)", "Равны, но разные; `c` — тот же, что `a`."),
        ("print(None is None, [] is [])", "Два разных пустых списка."),
    ],
    mistake="Проверять списки через `is` вместо `==`."),

f"{P}-refs-e4": x(
    idea="`is` проверяет тождество объектов.",
    lines=[("return a is b", "Не `==`.")],
    mistake="`a == b` — равные, но разные объекты дадут `True`."),

f"{P}-refs-e5": x(
    idea="`list(items)` создаёт копию — изменения не коснутся исходного списка.",
    lines=[
        ("result = list(items)", "Новый список."),
        ("result.append(item)", "Меняем только копию."),
    ],
    mistake="`result = items` — вторая ссылка на тот же список."),

f"{P}-refs-e6": x(
    idea="`id` — «адрес» объекта. Множество `id` — количество разных объектов.",
    lines=[("return len({id(x) for x in items})", "Одинаковые значения в разных объектах считаются отдельно.")],
    mistake="`len(set(items))` — считает значения, да ещё и упадёт на списках."),

f"{P}-refs-e7": x(
    idea="Внешний список собирается в цикле — каждая строка создаётся заново.",
    lines=[("return [[fill] * cols for _ in range(rows)]", "Новый `[fill] * cols` на каждой итерации.")],
    mistake="`[[fill] * cols] * rows` — все строки будут одним и тем же списком."),

f"{P}-refs-e8": x(
    idea="Группируем имена по `id` объекта; группы больше одного — псевдонимы.",
    lines=[
        ("groups.setdefault(id(obj), []).append(name)", "Ключ — объект, а не значение."),
        ("return [sorted(g) for g in groups.values() if len(g) > 1]", "Словарь хранит порядок появления."),
    ],
    mistake="Группировать по значению — `[]` и `x` окажутся вместе."),

f"{P}-ops-e1": x(
    idea="Для списка `+=` меняет объект на месте (все ссылки видят). Для кортежа — создаёт новый.",
    lines=[
        ("a += [3]", "Тот же список — `b` тоже изменился."),
        ("t += (3,)", "Новый кортеж; `u` — старый."),
    ],
    mistake="Думать, что `+=` всегда работает одинаково."),

f"{P}-ops-e2": x(
    idea="`sort()` меняет список и возвращает `None`. `sorted()` возвращает новый список.",
    lines=[
        ("result = nums.sort()", "`None`."),
        ("new = sorted(nums)", "Новый; исходный прежний."),
    ],
    mistake="`x = x.sort()` — потерять список."),

f"{P}-ops-e3": x(
    idea="Методы строк возвращают новую строку; если её не сохранить — она теряется.",
    lines=[
        ("s.strip()", "Результат выброшен."),
        ("print(repr(s))", "Строка прежняя."),
        ("s = s.strip().lower()", "Теперь сохранили."),
    ],
    mistake="Ожидать `'hello'` в первой строке."),

f"{P}-ops-e4": x(
    idea="`sorted` возвращает новый список, исходный не трогает.",
    lines=[("return sorted(names)", "Не `names.sort()`.")],
    mistake="`return names.sort()` — `None`."),

f"{P}-ops-e5": x(
    idea="Изменение на месте — присваивание по индексу. Переприсвоить `w` внутри цикла недостаточно.",
    lines=[
        ("for i, w in enumerate(words):", "Индекс нужен для записи."),
        ("words[i] = w.lower()", "Меняем элемент списка."),
    ],
    mistake="`w = w.lower()` — список не изменится."),

f"{P}-ops-e6": x(
    idea="`items + [x]` — новый список; `append` — изменение того же.",
    lines=[
        ("return items + [x]", "Копия с новым элементом."),
        ("items.append(x)", "На месте, возврат — `None`."),
    ],
    mistake="`with_item` через `append` — исходный список изменится."),

f"{P}-ops-e7": x(
    idea="`{**base, **extra}` собирает новый словарь; правый перекрывает левый.",
    lines=[("return {**base, **extra}", "Исходные не тронуты.")],
    mistake="`base.update(extra)` — испортит `base`."),

f"{P}-ops-e8": x(
    idea="Строим новый порядок, считаем разницу, потом срезом `[:]` заменяем содержимое того же списка.",
    lines=[
        ("if x not in seen:", "Первое появление."),
        ("removed = len(items) - len(result)", "Сколько ушло."),
        ("items[:] = result", "На месте."),
    ],
    mistake="`items = result` — снаружи список не изменится."),

f"{P}-hash-e1": x(
    idea="Ключ словаря должен быть хешируемым: кортеж и строка подходят, список — нет.",
    lines=[
        ('d[(1, 2)] = "кортеж"', "Можно."),
        ('d[[1, 2]] = "список"', "`TypeError`."),
        ("print(d)", "Список не добавился."),
    ],
    mistake="Ожидать ключ `[1, 2]` в словаре."),

f"{P}-hash-e2": x(
    idea="Кортеж неизменяем, но список внутри него меняется. Такой кортеж нехешируем.",
    lines=[
        ("t[1].append(4)", "Меняем список, не кортеж."),
        ("hash(t)", "Внутри список — ошибка."),
        ("print(hash((1, (2, 3))) == hash((1, (2, 3))))", "Из неизменяемых частей — хешируем."),
    ],
    mistake="Думать, что `t[1].append` запрещён."),

f"{P}-hash-e3": x(
    idea="`frozenset` — неизменяемое множество: его можно класть в множество, порядок элементов неважен.",
    lines=[
        ('groups = {frozenset({"аня", "боря"}), frozenset({"боря", "аня"}), frozenset({"вика"})}', "Первые два равны."),
        ('{{"a"}}', "Обычное множество внутри множества — нельзя."),
        ("print(fs | {3}, type(fs | {3}).__name__)", "Тип левого операнда."),
    ],
    mistake="Ожидать 3 — порядок в `frozenset` не важен."),

f"{P}-hash-e4": x(
    idea="Хешируемость проверяем попыткой `hash`.",
    lines=[
        ("hash(value)", "Проба."),
        ("except TypeError:\n        return False", "Нельзя."),
        ("return True", "Можно."),
    ],
    mistake="Проверять `isinstance(value, (list, dict, set))` — кортеж со списком пройдёт."),

f"{P}-hash-e5": x(
    idea="Список не может быть ключом — превращаем в кортеж.",
    lines=[
        ("key = tuple(p)", "Хешируемый ключ."),
        ("result[key] = result.get(key, 0) + 1", "Счётчик."),
    ],
    mistake="`result[p]` — `TypeError`."),

f"{P}-hash-e6": x(
    idea="Команда — набор без порядка: `frozenset` хешируем и игнорирует порядок.",
    lines=[("return len({frozenset(t) for t in teams})", "Разные наборы.")],
    mistake="`tuple(t)` — `[аня, боря]` и `[боря, аня]` станут разными."),

f"{P}-hash-e7": x(
    idea="Словарь нехешируем — ключом становится кортеж отсортированных пар.",
    lines=[
        ("key = tuple(sorted(d.items()))", "Порядок ключей не важен."),
        ("if key not in seen:", "Первый раз."),
        ("result.append(d)", "Сам словарь, не ключ."),
    ],
    mistake="`set(items)` — `TypeError`."),

f"{P}-hash-e8": x(
    idea="Рекурсия: каждую коллекцию превращаем в неизменяемый аналог, заморозив сначала элементы.",
    lines=[
        ("return tuple(freeze(v) for v in value)", "Список → кортеж."),
        ("return frozenset(freeze(v) for v in value)", "Множество → frozenset."),
        ("return tuple(sorted((k, freeze(v)) for k, v in value.items()))", "Словарь → отсортированные пары."),
        ("return value", "Остальное."),
    ],
    mistake="Не замораживать вложенные — внутри останется список."),

# ===== Модуль 2. Функции и копии =====

f"{P}-args-e1": x(
    idea="Функция получает ссылку на тот же список — изменения видны снаружи.",
    lines=[
        ("scores[i] += 10", "Меняем элементы общего списка."),
        ("print(my)", "Изменился."),
    ],
    mistake="Ожидать `[50, 70]`."),

f"{P}-args-e2": x(
    idea="Переприсвоить параметр — значит переключить локальное имя. Метод (`clear`) меняет сам объект.",
    lines=[
        ("items = []", "Новое имя внутри; `data` прежний."),
        ("print(reset(data), data)", "Новый и старый."),
        ("items.clear()", "Меняет общий объект."),
    ],
    mistake="Думать, что `items = []` очистит внешний список."),

f"{P}-args-e3": x(
    idea="Числа и строки неизменяемы: `+=` внутри функции создаёт новый объект, внешний не меняется.",
    lines=[
        ("n += 1", "Новое число."),
        ('s += "!"', "Новая строка."),
        ("print(shout(word), word)", "Оригинал прежний."),
    ],
    mistake="Ожидать `6 6`."),

f"{P}-args-e4": x(
    idea="Новый список из новых значений.",
    lines=[("return [x + bonus for x in scores]", "Исходный не тронут.")],
    mistake="`scores[i] += bonus` — изменит исходный."),

f"{P}-args-e5": x(
    idea="Первой строкой делаем копию словаря — дальше меняем только её.",
    lines=[
        ("user = dict(user)", "Копия."),
        ('user["name"] = user["name"].strip().title()', "Меняем копию."),
        ("return user", "Новый словарь."),
    ],
    mistake="Копировать после изменений — оригинал уже испорчен."),

f"{P}-args-e6": x(
    idea="Изменение на месте: `todo[:] = ...` заменяет содержимое, `extend` дописывает.",
    lines=[
        ('finished = [t for t in todo if t.endswith("✓")]', "Что переносим."),
        ('todo[:] = [t for t in todo if not t.endswith("✓")]', "Тот же список без готовых."),
        ("done.extend(finished)", "Добавляем в `done`."),
    ],
    mistake="`todo = [...]` — снаружи `todo` не изменится."),

f"{P}-args-e7": x(
    idea="Передаём копию — функция может её портить.",
    lines=[("return func(list(data))", "`data` в безопасности.")],
    mistake="`func(data)` — изменения попадут в оригинал."),

f"{P}-args-e8": x(
    idea="Новый список новых словарей: `{**item, ...}` копирует словарь и заменяет цену.",
    lines=[("return [{**item, \"price\": round(item[\"price\"] * (1 - percent / 100), 2)} for item in cart]", "Копия каждого товара.")],
    mistake="`item[\"price\"] = ...` — исходные словари изменятся."),

f"{P}-default-e1": x(
    idea="Значение по умолчанию создаётся один раз — при определении функции. Список копит элементы между вызовами.",
    lines=[
        ("def add(item, items=[]):", "Один список на все вызовы."),
        ('print(add("b"))', "Тот же список — `a` уже там."),
        ('print(add("c", []))', "Свой список — без ловушки."),
        ('print(add("d"))', "Снова общий."),
    ],
    mistake="Ожидать `['b']` и `['d']`."),

f"{P}-default-e2": x(
    idea="Значения по умолчанию хранятся в `__defaults__` — там видно накопленное.",
    lines=[
        ("history.append(msg)", "Меняем объект по умолчанию."),
        ("print(log.__defaults__)", "Кортеж значений по умолчанию."),
    ],
    mistake="Ожидать `([],)`."),

f"{P}-default-e3": x(
    idea="`None` по умолчанию и новый список внутри — у каждого вызова свой.",
    lines=[
        ("if items is None:\n        items = []", "Новый при каждом вызове."),
        ('print(add("y", shared), shared)', "Переданный список меняется — это нормально."),
    ],
    mistake="Ожидать, что `shared` не изменится."),

f"{P}-default-e4": x(
    idea="Правильный шаблон: `None` и создание списка внутри.",
    lines=[
        ("def add_tag(tag, tags=None):", "Не `[]`."),
        ("if tags is None:\n        tags = []", "Новый каждый раз."),
    ],
    mistake="`tags = tags or []` — переданный пустой список заменится новым."),

f"{P}-default-e5": x(
    idea="`None` по умолчанию; копия переданного словаря — чтобы не портить чужие заголовки.",
    lines=[
        ('headers = dict(headers or {})', "Всегда новый словарь."),
        ('headers["Accept"] = "json"', "Меняем копию."),
    ],
    mistake="`headers = headers or {}` — переданный словарь изменится."),

f"{P}-default-e6": x(
    idea="`__defaults__` может быть `None` — подставляем пустой кортеж.",
    lines=[("return any(isinstance(v, (list, dict, set)) for v in (func.__defaults__ or ()))", "Хоть одно изменяемое.")],
    mistake="Перебирать `func.__defaults__` напрямую — `TypeError` для функции без умолчаний."),

f"{P}-default-e7": x(
    idea="Здесь общий словарь нужен намеренно — это кэш между вызовами.",
    lines=[
        ("if n in _cache:\n        return _cache[n], True", "Уже считали."),
        ("_cache[n] = n * n", "Запоминаем."),
        ("return _cache[n], False", "Посчитали впервые."),
    ],
    mistake="`_cache=None` — кэш будет пустым при каждом вызове."),

f"{P}-default-e8": x(
    idea="В `__init__` тоже `None` по умолчанию; переданный список копируем.",
    lines=[
        ("def __init__(self, name, tests=None):", "Не `[]`."),
        ("self.tests = list(tests) if tests is not None else []", "Свой список у каждого объекта."),
    ],
    mistake="`self.tests = tests or []` — переданный список станет общим."),

f"{P}-copy-e1": x(
    idea="Четыре способа сделать поверхностную копию списка — каждый даёт новый объект.",
    lines=[
        ("copies = [a[:], list(a), a.copy(), [*a]]", "Срез, конструктор, метод, распаковка."),
        ("c.append(4)", "Меняем копии."),
        ("print(a, [c is a for c in copies])", "Оригинал не тронут."),
    ],
    mistake="Думать, что срез — это ссылка."),

f"{P}-copy-e2": x(
    idea="Поверхностная копия копирует только внешний список; вложенные списки общие.",
    lines=[
        ("b = a.copy()", "Новый внешний список."),
        ("b.append([5])", "Только в `b`."),
        ("b[0].append(99)", "Общий вложенный — виден в `a`."),
        ("print(a[0] is b[0])", "Один и тот же объект."),
    ],
    mistake="Ожидать `[[1, 2], [3, 4]]` в `a`."),

f"{P}-copy-e3": x(
    idea="Копия словаря тоже поверхностная: замена значения — только в копии, изменение вложенного списка — везде.",
    lines=[
        ('copy1["name"] = "Боря"', "Замена — только в `copy1`."),
        ('copy2["tags"].append("api")', "Общий список."),
        ("print(user)", "Имя прежнее, теги изменились."),
    ],
    mistake="Ожидать `['qa']` в оригинале."),

f"{P}-copy-e4": x(
    idea="Копия, затем сортировка копии на месте.",
    lines=[
        ("result = items.copy()", "Новый список."),
        ("result.sort()", "Сортируем копию."),
        ("return result", "Не результат `sort()`."),
    ],
    mistake="`return result.sort()` — `None`."),

f"{P}-copy-e5": x(
    idea="Копируем каждую строку отдельно — матрица становится независимой.",
    lines=[("return [row[:] for row in matrix]", "Новая строка на каждую.")],
    mistake="`matrix[:]` — строки останутся общими."),

f"{P}-copy-e6": x(
    idea="Значения простые — достаточно поверхностной копии каждого словаря.",
    lines=[("return [dict(u) for u in users]", "Новый словарь на каждого.")],
    mistake="`list(users)` — словари внутри те же."),

f"{P}-copy-e7": x(
    idea="Множество `id` внутренних списков первого и проверка каждого из второго.",
    lines=[
        ("ids = {id(x) for x in a}", "Объекты `a`."),
        ("return any(id(x) in ids for x in b)", "Хоть один общий."),
    ],
    mistake="Сравнивать `x in a` — это проверка равенства, а не тождества."),

f"{P}-copy-e8": x(
    idea="Копируем внешний словарь и заменяем только изменяемую секцию новым словарём.",
    lines=[
        ("new = dict(config)", "Новый внешний."),
        ("new[section] = {**config.get(section, {}), key: value}", "Новая секция; старая не тронута."),
    ],
    mistake="`new[section][key] = value` — изменит секцию оригинала."),

f"{P}-deepcopy-e1": x(
    idea="`copy.copy` — поверхностная копия, `deepcopy` копирует всё рекурсивно.",
    lines=[
        ("shallow = copy.copy(data)", "Список `users` общий."),
        ("deep = copy.deepcopy(data)", "Всё своё."),
        ('data["users"][0]["name"] = "Изменено"', "Видно в `shallow`."),
    ],
    mistake="Ожидать, что `copy.copy` защитит вложенное."),

f"{P}-deepcopy-e2": x(
    idea="Умножение списка повторяет ссылку: обе строки — один объект. Генератор создаёт новые.",
    lines=[
        ("grid = [[0] * 3] * 2", "Две ссылки на одну строку."),
        ("grid[0][0] = 1", "Меняется «обе»."),
        ("good = [[0] * 3 for _ in range(2)]", "Разные строки."),
    ],
    mistake="Ожидать `[[1, 0, 0], [0, 0, 0]]` в первой строке."),

f"{P}-deepcopy-e3": x(
    idea="`deepcopy` сохраняет структуру ссылок: если внутри был один объект дважды, в копии тоже один (новый).",
    lines=[
        ("clone = copy.deepcopy(pair)", "Копия `shared` одна на оба места."),
        ("clone[0].append(3)", "Видно в `clone[1]`."),
        ("print(clone, clone[0] is clone[1], shared)", "Оригинал не тронут."),
    ],
    mistake="Ожидать `[[1, 2, 3], [1, 2]]`."),

f"{P}-deepcopy-e4": x(
    idea="`deepcopy` — полная независимая копия.",
    lines=[("return copy.deepcopy(data)", "Все уровни.")],
    mistake="`copy.copy` — вложенное останется общим."),

f"{P}-deepcopy-e5": x(
    idea="Рекурсия: список и словарь копируем, их элементы — тоже через `deep_copy`.",
    lines=[
        ("return [deep_copy(v) for v in value]", "Список."),
        ("return {k: deep_copy(v) for k, v in value.items()}", "Словарь."),
        ("return value", "Числа, строки — неизменяемы."),
    ],
    mistake="Не вызывать `deep_copy` для элементов — копия будет поверхностной."),

f"{P}-deepcopy-e6": x(
    idea="Каждая строка поля создаётся заново в генераторе.",
    lines=[("return [[\".\"] * size for _ in range(size)]", "Независимые строки.")],
    mistake="`[[\".\"] * size] * size` — одна строка много раз."),

f"{P}-deepcopy-e7": x(
    idea="Глубокая копия эталона, затем замена ключей верхнего уровня.",
    lines=[
        ("payload = copy.deepcopy(template)", "Эталон не пострадает."),
        ("payload.update(changes)", "Переопределения."),
    ],
    mistake="`dict(template)` — вложенные части общие."),

f"{P}-deepcopy-e8": x(
    idea="Собираем `id` всех списков и словарей обеих структур; пересечение — общие объекты.",
    lines=[
        ("acc.add(id(value))", "Изменяемый — запомнить."),
        ("items = value.values() if isinstance(value, dict) else value", "Что обходить."),
        ("_mutable_ids(v, acc)", "Рекурсия."),
        ("return not (_mutable_ids(a, set()) & _mutable_ids(b, set()))", "Пересечение пусто — независимы."),
    ],
    mistake="Сравнивать только верхний уровень."),

# ===== Модуль 3. Практика =====

f"{P}-iterate-e1": x(
    idea="Удаление при переборе сдвигает элементы: следующий после удалённого пропускается.",
    trace=[
        ("for n in nums:", "i=0: 1", ""),
        ("nums.remove(n)", "i=1: 2 → [1, 2, 3, 2, 4]", ""),
        ("for n in nums:", "i=2: 3 — вторая 2 пропущена", ""),
        ("nums.remove(n)", "i=3: 2 → удаляется первая 2 → [1, 3, 2, 4]", ""),
        ("for n in nums:", "i=4 — за концом, цикл окончен", ""),
        ("print(nums)", "", "[1, 3, 2, 4]"),
    ],
    mistake="Ожидать `[1, 3, 4]`."),

f"{P}-iterate-e2": x(
    idea="Менять размер словаря во время перебора нельзя. Перебирай копию ключей `list(d)`.",
    lines=[
        ('d[k + "!"] = 0', "Новый ключ — `RuntimeError`."),
        ("for k in list(d):", "Копия ключей."),
        ("del d[k]", "Теперь можно."),
    ],
    mistake="Не заметить, что `a!` успел добавиться до ошибки — его убрал второй цикл."),

f"{P}-iterate-e3": x(
    idea="Два надёжных способа: собрать новый список или перебирать копию.",
    lines=[
        ("print([n for n in nums if n != 2])", "Новый список."),
        ("for n in nums[:]:", "Перебор копии."),
        ("nums.remove(n)", "Удаление из оригинала."),
    ],
    mistake="Перебирать `nums` и удалять из него же."),

f"{P}-iterate-e4": x(
    idea="Собираем новый список и присваиванием в срез меняем тот же объект.",
    lines=[("nums[:] = [n for n in nums if n >= 0]", "На месте.")],
    mistake="`nums = [...]` — снаружи ничего не изменится."),

f"{P}-iterate-e5": x(
    idea="Сначала собираем ключи для удаления, потом удаляем — словарь не меняется во время перебора.",
    lines=[
        ('removed = [k for k, v in d.items() if v in ("", None) or v == [] or v == {}]', "Пустые значения; 0 и False сюда не входят."),
        ("for k in removed:\n        del d[k]", "Удаляем по списку."),
    ],
    mistake="`if not v` — удалит и `0`."),

f"{P}-iterate-e6": x(
    idea="Строим результат отдельно и заменяем содержимое — вставка во время перебора зациклила бы цикл.",
    lines=[
        ("result.append(x)", "Сам элемент."),
        ("if x > 10:\n            result.append(x // 2)", "Половина после него."),
        ("items[:] = result", "На месте."),
    ],
    mistake="`items.insert` во время перебора — половина 30 (15) тоже > 10, получится бесконечный цикл."),

f"{P}-iterate-e7": x(
    idea="Перебираем копию ключей; `pop` забирает значение под старым ключом.",
    lines=[
        ("for old in list(d):", "Копия."),
        ("d[mapping[old]] = d.pop(old)", "Перенос под новое имя."),
    ],
    mistake="`for old in d` — `RuntimeError`."),

f"{P}-iterate-e8": x(
    idea="`while queue` работает, пока очередь не пуста; новые задачи дописываются в конец.",
    lines=[
        ("task = queue.pop(0)", "С начала."),
        ("new = handler(task)", "Может породить задачи."),
        ("if new:\n            queue.extend(new)", "В конец очереди."),
    ],
    mistake="`for task in queue` с добавлением — пропуски и путаница."),

f"{P}-frozen-e1": x(
    idea="Кортеж не даёт присваивать по индексу; у `frozenset` вообще нет методов изменения.",
    lines=[
        ("point[0] = 10", "`TypeError`."),
        ('roles.add("admin")', "`AttributeError` — метода нет."),
        ('print("read" in roles)', "Читать можно."),
    ],
    mistake="Ожидать одинаковый тип ошибки."),

f"{P}-frozen-e2": x(
    idea="`MappingProxyType` — вид на словарь только для чтения. Меняется исходный словарь — меняется и вид.",
    lines=[
        ("SETTINGS = MappingProxyType(_settings)", "Обёртка."),
        ('SETTINGS["url"] = "test"', "Запись запрещена."),
        ('_settings["timeout"] = 10', "Через оригинал можно."),
        ('print(SETTINGS["timeout"])', "Вид показывает новое."),
    ],
    mistake="Ожидать 5 — прокси не копия."),

f"{P}-frozen-e3": x(
    idea="`namedtuple` и `dataclass(frozen=True)` неизменяемы; «изменение» — это новый объект через `_replace`/`replace`.",
    lines=[
        ("print(p, p.x, p._replace(x=10))", "Новый кортеж."),
        ("u.age = 31", "`FrozenInstanceError`."),
        ("print(replace(u, age=31), u)", "Новый и старый."),
    ],
    mistake="Ожидать, что `replace` поменяет `u`."),

f"{P}-frozen-e4": x(
    idea="Прокси над копией: исходный словарь можно менять — результат не изменится.",
    lines=[("return MappingProxyType(dict(config))", "Копия + только чтение.")],
    mistake="`MappingProxyType(config)` — изменения оригинала будут видны."),

f"{P}-frozen-e5": x(
    idea="Замороженный dataclass: «изменение» — новый объект.",
    lines=[
        ("@dataclass(frozen=True)", "Поля нельзя менять."),
        ('if self.currency != other.currency:\n            raise ValueError("разные валюты")', "Проверка."),
        ("return Money(self.amount + other.amount, self.currency)", "Новый объект."),
    ],
    mistake="`self.amount += ...` — `FrozenInstanceError`."),

f"{P}-frozen-e6": x(
    idea="`namedtuple` — кортеж с именами полей.",
    lines=[
        ('Point = namedtuple("Point", "x y")', "Тип на уровне модуля."),
        ("return [Point(x, y) for x, y in pairs]", "Распаковка пары."),
    ],
    mistake="Объявлять `Point` внутри функции — каждый вызов создаст новый тип."),

f"{P}-frozen-e7": x(
    idea="Новый словарь со значениями `frozenset`.",
    lines=[("return {user: frozenset(roles) for user, roles in roles_by_user.items()}", "Роли не изменить.")],
    mistake="`tuple(roles)` — тоже неизменяемо, но проверка `in` медленнее и порядок лишний."),

f"{P}-frozen-e8": x(
    idea="`order=True` даёт сравнение по полям по порядку; `replace` создаёт новую версию.",
    lines=[
        ("@dataclass(frozen=True, order=True)", "Неизменяемый и сравнимый."),
        ('return cls(*(int(p) for p in text.split(".")))', "Числа, не строки — 10 > 9."),
        ("return replace(self, minor=self.minor + 1, patch=0)", "Новый объект."),
    ],
    mistake="Сравнивать строки версий — «1.10» < «1.9»."),

f"{P}-classes-e1": x(
    idea="Атрибут класса — один на все объекты. `self.items.append` меняет общий список.",
    lines=[
        ("items = []", "Атрибут класса."),
        ("self.items.append(x)", "Нет своего — берём классовый."),
        ("print(b.items, a.items is b.items)", "У `b` тоже чай."),
    ],
    mistake="Ожидать `[]` у `b`."),

f"{P}-classes-e2": x(
    idea="Возврат внутреннего списка отдаёт ссылку — снаружи его можно испортить. Копия защищает.",
    lines=[
        ('t.members().append("Взломщик")', "Изменили внутренний список."),
        ('t.members_copy().append("Нет")', "Изменили копию."),
        ("print(t._members)", "Взломщик внутри."),
    ],
    mistake="Думать, что `_` в имени защищает."),

f"{P}-classes-e3": x(
    idea="В двух списках лежит один и тот же объект — изменение через один список видно через другой.",
    lines=[
        ('admins[0].name = "АНЯ"', "Меняем объект `u`."),
        ("print([x.name for x in everyone])", "Тот же объект."),
    ],
    mistake="Ожидать «аня»."),

f"{P}-classes-e4": x(
    idea="Список создаётся в `__init__` — у каждой корзины свой.",
    lines=[
        ("self.items = []", "Атрибут объекта."),
        ("self.items.append(item)", "Своя корзина."),
    ],
    mistake="Оставить `items = []` в теле класса."),

f"{P}-classes-e5": x(
    idea="Наружу отдаём кортеж-копию — изменить состав нельзя.",
    lines=[("return tuple(self._members)", "Неизменяемая копия.")],
    mistake="`return self._members` — утечка."),

f"{P}-classes-e6": x(
    idea="Копия при сохранении — внешние изменения не влияют на заказ.",
    lines=[
        ("self.items = list(items)", "Своя копия."),
        ("return sum(self.items)", "Сумма."),
    ],
    mistake="`self.items = items` — заказ изменится вместе со списком снаружи."),

f"{P}-classes-e7": x(
    idea="Копия внутри, прокси наружу, «изменение» — новый объект.",
    lines=[
        ("self._values = dict(values)", "Копия."),
        ("return MappingProxyType(self._values)", "Только чтение."),
        ("return Settings({**self._values, key: value})", "Новый объект."),
    ],
    mistake="Возвращать `self._values` из `values` — его можно изменить."),

f"{P}-classes-e8": x(
    idea="Глубокая копия на входе и на выходе — снимки нельзя испортить ни до, ни после.",
    lines=[
        ("self._snapshots.append(copy.deepcopy(state))", "Сохраняем копию."),
        ("return copy.deepcopy(self._snapshots[i])", "Отдаём копию."),
        ("return len(self._snapshots)", "Количество."),
    ],
    mistake="Копировать только при сохранении — выданный снимок можно изменить."),

f"{P}-tests-e1": x(
    idea="`user = USER` — не копия: тест меняет общие данные, и следующий тест падает.",
    lines=[
        ("user = USER", "Ссылка на глобальный словарь."),
        ('user["roles"].append("admin")', "Испортили эталон."),
        ("print(test_reader())", "Роль admin «протекла»."),
    ],
    mistake="Ожидать `True`."),

f"{P}-tests-e2": x(
    idea="Фабрика создаёт новые данные при каждом вызове — тесты не мешают друг другу.",
    lines=[
        ('user = {"name": "test", "roles": ["reader"]}', "Новый словарь и список каждый раз."),
        ('a["roles"].append("admin")', "Только у `a`."),
        ("print(b)", "Чистый."),
    ],
    mistake="Держать шаблон в глобальной переменной и возвращать его."),

f"{P}-tests-e3": x(
    idea="Снимок до вызова и сравнение после — так ловят функции, которые портят вход.",
    lines=[
        ("scores.sort(reverse=True)", "Сортировка на месте — меняет вход."),
        ("snapshot = copy.deepcopy(data)", "Эталон."),
        ('print("вход не изменён:", data == snapshot)', "Изменён."),
    ],
    mistake="Ожидать `True`."),

f"{P}-tests-e4": x(
    idea="Словарь с пустым списком создаётся внутри функции — у каждого заказа свой.",
    lines=[
        ('order = {"id": 1, "items": [], "status": "new"}', "Новый при каждом вызове."),
        ("order.update(overrides)", "Переопределения."),
    ],
    mistake="Шаблон вне функции — `items` станет общим."),

f"{P}-tests-e5": x(
    idea="Глубокая копия аргументов до вызова, сравнение после.",
    lines=[
        ("before = copy.deepcopy(args)", "Снимок."),
        ("result = func(*args)", "Вызов."),
        ("for i, (old, new) in enumerate(zip(before, args)):", "Попарно с номером."),
        ('raise AssertionError(f"аргумент {i} изменён")', "Нашли изменение."),
    ],
    mistake="`copy.copy` — изменения вложенных данных не заметишь."),

f"{P}-tests-e6": x(
    idea="Эталон отдаём только глубокой копией.",
    lines=[("return copy.deepcopy(FIXTURES[name])", "Тест может менять копию.")],
    mistake="`dict(FIXTURES[name])` — вложенные списки общие."),

f"{P}-tests-e7": x(
    idea="Операции над множествами ключей: разность — добавленные и удалённые, пересечение — общие.",
    lines=[
        ('"added": sorted(after.keys() - before.keys()),', "Есть только после."),
        ('"removed": sorted(before.keys() - after.keys()),', "Были только до."),
        ('"changed": sorted(k for k in before.keys() & after.keys() if before[k] != after[k]),', "Общие с разными значениями."),
    ],
    mistake="Считать изменёнными и добавленные ключи."),

f"{P}-tests-e8": x(
    idea="Работаем с глубокой копией; вложенные словари сливаем рекурсивно, остальное заменяем копией.",
    lines=[
        ("result = copy.deepcopy(resource)", "Оригинал в безопасности."),
        ("if isinstance(value, dict) and isinstance(result.get(key), dict):", "Оба словари — сливаем."),
        ("result[key] = apply_patch(result[key], value)", "Рекурсия."),
        ("result[key] = copy.deepcopy(value)", "Чтобы результат не делил объекты с `patch`."),
    ],
    mistake="`resource.update(patch)` — портит ресурс и затирает вложенные поля целиком."),
}
