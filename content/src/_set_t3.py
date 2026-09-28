"""Теория модуля «Множества на практике» темы «Множества».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- set-m3-l1 ----------
'set-m3-l1': dict(
    full=t(r'''
## Зачем это нужно

Обычное множество изменяемое, поэтому его нельзя положить в другое множество или сделать ключом словаря. Когда нужен «набор без порядка» в роли ключа — например, комбинация окружения `{"chrome", "linux"}`, где порядок не важен, — используют **`frozenset`**: неизменяемое множество.

## frozenset

```python
fs = frozenset([3, 1, 3])
print(sorted(fs), len(fs), 1 in fs)
try:
    fs.add(5)
except AttributeError:
    print("frozenset нельзя изменить")
```

- `frozenset(коллекция)` — как `set`, но без методов изменения (`add`, `remove`, `update`…).
- Проверки, `len`, перебор — работают.
- Вывод: `[1, 3] 2 True`, `frozenset нельзя изменить`.

## Ключ словаря и элемент множества

```python
combos = {frozenset({"chrome", "linux"}): "ok"}
print(combos[frozenset({"linux", "chrome"})])
try:
    {{1, 2}: "x"}
except TypeError:
    print("обычное множество не может быть ключом")
```

- `frozenset` хешируемый — может быть ключом и элементом множества. Порядок элементов не важен: `{"linux", "chrome"}` — тот же ключ.
- Обычный `set` — `TypeError: unhashable type`.
- Вывод: `ok`, `обычное множество не может быть ключом`.

## Операции

```python
a = frozenset({1, 2})
b = a | {3}
print(type(b).__name__, sorted(b), a == {1, 2})
```

- Операции `|`, `&`, `-`, `^` работают и возвращают `frozenset` (тип левого операнда).
- `frozenset` и `set` с одинаковыми элементами равны.
- Вывод: `frozenset [1, 2, 3] True`.

## Различные комбинации

```python
runs = [["chrome", "linux"], ["linux", "chrome"], ["ff", "mac"]]
print(len({frozenset(r) for r in runs}))
words = ["listen", "silent", "enlist", "abc", "cab"]
print(len({frozenset(w) for w in words}))
```

- Каждую комбинацию превращаем в `frozenset` — порядок перестаёт иметь значение, и множество таких наборов убирает повторы.
- Вывод: `2`, `2`.

## Итог

- `frozenset(...)` — неизменяемое множество; `add`/`remove` нет.
- Хешируемый: может быть ключом словаря и элементом множества.
- Порядок элементов не важен — удобный ключ для «набора без порядка».
- Операции работают как у `set`.
'''),
    short=t(r'''
```py
fs = frozenset([1, 2])
fs.add(3)                            # AttributeError
{frozenset({"chrome", "linux"}): "ok"}   # ключ-набор без порядка
{{1, 2}: "x"}                        # TypeError — set нехешируемый
len({frozenset(r) for r in runs})    # различные комбинации
```
'''),
    quiz=[
        q('Можно ли сделать `frozenset` ключом словаря?',
            ['Нет', 'Да — он хешируемый', 'Только пустой', 'Только из чисел'],
            1, 'В отличие от set.'),
        q('Равны ли `frozenset({1, 2})` и `{2, 1}`?',
            ['Да', 'Нет', 'Ошибка', 'Только по len'],
            0, 'Сравниваются элементы.'),
        q('Что будет при `frozenset([1]).add(2)`?',
            ['Добавится 2', '`AttributeError`', '`TypeError`', 'Ничего'],
            1, 'Методов изменения нет.'),
    ],
),

# ---------- set-m3-l2 ----------
'set-m3-l2': dict(
    full=t(r'''
## Зачем это нужно

Поиск дублей — частая задача тестировщика: API вернул один объект дважды, email зарегистрирован повторно, в выгрузке задвоились строки. Множества находят дубли за один проход, а нормализация перед сравнением ловит «скрытые» дубли вроде `"A@x.ru"` и `"a@x.ru "`.

## Найти повторяющиеся

```python
ids = [3, 1, 3, 2, 1, 3]
seen, dups = set(), set()
for x in ids:
    if x in seen:
        dups.add(x)
    seen.add(x)
print(sorted(dups), sorted(seen))
```

- Два множества: `seen` — всё встреченное, `dups` — встреченное повторно. Каждый дубль попадает в `dups` один раз, сколько бы раз он ни повторялся.
- Вывод: `[1, 3] [1, 2, 3]`.

## Нормализация

```python
emails = ["A@x.ru", "a@x.ru ", "b@x.ru"]
print(len(set(emails)), len({e.strip().lower() for e in emails}))
```

- Без нормализации строки разные — три «уникальных» адреса. После `strip().lower()` видно, что их два.
- Вывод: `3 2`.

## Сколько раз — Counter

```python
from collections import Counter
items = ["a", "b", "a", "c", "a", "b"]
c = Counter(items)
print(sorted(x for x, n in c.items() if n > 1), sorted(x for x, n in c.items() if n == 1))
```

- Когда важно **количество**, а не только факт повтора, — `Counter` (тема «Словари»).
- Вывод: `['a', 'b'] ['c']`.

## Дубли по полю

```python
records = [{"id": 1, "v": "a"}, {"id": 1, "v": "b"}, {"id": 2, "v": "c"}]
seen, result = set(), []
for r in records:
    if r["id"] not in seen:
        seen.add(r["id"])
        result.append(r)
print(result)
```

- Словари нельзя положить в множество, но их **ключевое поле** — можно. Оставляем первую запись для каждого `id`.
- Вывод: `[{'id': 1, 'v': 'a'}, {'id': 2, 'v': 'c'}]`.

## Итог

- Дубли за один проход: `seen` + `dups`.
- Нормализуй перед сравнением: `strip()`, `lower()`.
- Нужны количества — `Counter`.
- Дубли записей — по ключевому полю в множестве `seen`.
'''),
    short=t(r'''
```py
seen, dups = set(), set()
for x in items:
    if x in seen: dups.add(x)
    seen.add(x)
{e.strip().lower() for e in emails}     # нормализуй
Counter(items)                           # количества
if r["id"] not in seen: ...             # дубли по полю
```
'''),
    quiz=[
        q('Сколько раз попадёт `3` в `dups`, если в списке пять троек?',
            ['5', '4', '1', '0'],
            2, 'Множество хранит значение один раз.'),
        q('Зачем нормализовать email перед сравнением?',
            ['Быстрее', 'Чтобы "A@x.ru" и "a@x.ru " считались одним', 'Так требует set', 'Не нужно'],
            1, 'Скрытые дубли.'),
        q('Можно ли положить словарь в множество?',
            ['Да', 'Нет — нехешируемый; кладут его ключевое поле', 'Только пустой', 'Только frozendict'],
            1, 'Используют id записи.'),
    ],
),

# ---------- set-m3-l3 ----------
'set-m3-l3': dict(
    full=t(r'''
## Зачем это нужно

В тестах часто нужно сравнить **наборы** без учёта порядка: роли пользователя, список id в ответе, упавшие тесты. Множества идеальны, но у них есть подвох — они **теряют повторы**. Нужно выбирать инструмент под задачу.

## Порядок не важен

```python
expected = ["admin", "qa", "dev"]
actual = ["qa", "dev", "admin"]
print(expected == actual, set(expected) == set(actual))
```

- Списки с одинаковыми элементами в разном порядке не равны; множества — равны.
- Вывод: `False True`.

## Но повторы теряются

```python
expected = ["a", "a", "b"]
actual = ["a", "b", "b"]
print(set(expected) == set(actual), sorted(expected) == sorted(actual))
```

- Множества равны (`{a, b}`), хотя количества разные — тест, сравнивающий множества, пропустит баг.
- Если важно количество — сравнивай отсортированные списки или `Counter`.
- Вывод: `True False`.

```python
from collections import Counter
print(Counter(["a", "a", "b"]) == Counter(["b", "a", "a"]), Counter(["a", "b"]) == Counter(["a", "a", "b"]))
```

Вывод: `True False`.

Выбор:
- важен только **набор** значений — `set(a) == set(b)`;
- важны **количества**, не важен порядок — `sorted(a) == sorted(b)` или `Counter`;
- важен **порядок** — `a == b`.

## Понятное сообщение об ошибке

```python
def diff_message(expected, actual):
    e, a = set(expected), set(actual)
    if e == a:
        return "ok"
    missing = ", ".join(sorted(e - a)) or "-"
    extra = ", ".join(sorted(a - e)) or "-"
    return f"не хватает: {missing}; лишние: {extra}"

print(diff_message(["a", "b"], ["b", "c"]))
```

- Вместо «наборы не равны» — что именно не так.
- `", ".join([])` — пустая строка, а `"" or "-"` даёт `"-"`.
- Вывод: `не хватает: a; лишние: c`.

## Набор id без дублей

```python
response = [{"id": 2}, {"id": 1}, {"id": 1}]
ids = [r["id"] for r in response]
print(len(ids) == len(set(ids)), set(ids) == {1, 2})
```

- Две проверки: нет дублей **и** набор совпадает. Одна проверка множеств дубль бы не заметила.
- Вывод: `False True`.

## Нестабильные тесты

```python
runs = [{"a", "b"}, {"a"}, {"a", "c"}]
ever = set().union(*runs)
always = set.intersection(*runs)
print(sorted(ever - always))
```

- `*runs` раскладывает список множеств в аргументы (тема «*args»).
- Падали хоть раз (объединение) минус падали всегда (пересечение) = нестабильные. Вывод: `['b', 'c']`.

## Итог

- Набор без порядка — `set(a) == set(b)`, но повторы теряются.
- С количествами — `sorted` или `Counter`.
- Сообщение — недостающие и лишние через разность.
- Проверяй дубли отдельно: `len(ids) == len(set(ids))`.
'''),
    short=t(r'''
```py
set(a) == set(b)           # набор (повторы не важны!)
sorted(a) == sorted(b)     # с количествами, без порядка
Counter(a) == Counter(b)   # то же
a == b                     # с порядком
len(ids) == len(set(ids))  # нет дублей
set().union(*runs) - set.intersection(*runs)   # нестабильные
```
'''),
    quiz=[
        q('Что вернёт `set(["a", "a"]) == set(["a"])`?',
            ['`True`', '`False`', 'Ошибка', '`None`'],
            0, 'Повторы теряются.'),
        q('Как сравнить списки с учётом количества, но без порядка?',
            ['`set(a) == set(b)`', '`sorted(a) == sorted(b)`', '`a is b`', '`a == b`'],
            1, 'Или Counter.'),
        q('Как проверить, что в списке id нет дублей?',
            ['`ids == set(ids)`', '`len(ids) == len(set(ids))`', '`sorted(ids)`', '`ids.unique()`'],
            1, 'Множество короче — есть дубли.'),
    ],
),

# ---------- set-m3-l4 ----------
'set-m3-l4': dict(
    full=t(r'''
## Зачем это нужно

Соберём операции над множествами в реальных задачах: отбор тестов по тегам (как `pytest -m "smoke and not slow"`), сравнение ролей и прав, расчёт покрытия функций тестами, связи между пользователями.

## Отбор тестов по тегам

```python
tests = {"login": {"smoke", "auth"}, "pay": {"payments"}, "logout": {"auth"}}
print([name for name, tags in tests.items() if "auth" in tags])
print(sorted(set().union(*tests.values())))
```

- Тест выбирается, если у него есть нужный тег. Все теги проекта — объединение всех наборов.
- Вывод: `['login', 'logout']`, `['auth', 'payments', 'smoke']`.

«Хотя бы один из include и ни одного из exclude»:

```python
tests = {"a": {"smoke"}, "b": {"smoke", "slow"}, "c": {"api"}}
include, exclude = {"smoke"}, {"slow"}
print(sorted(n for n, tags in tests.items() if include & tags and not exclude & tags))
```

- Непустое пересечение истинно, пустое — ложно. Вывод: `['a']`.

## Роли и права

```python
roles = {"admin": {"read", "write", "delete"}, "qa": {"read", "write"}, "guest": {"read"}}
print(sorted(roles["admin"] - roles["qa"]))
print([r for r, perms in roles.items() if "write" in perms])
print(roles["guest"] <= roles["qa"] <= roles["admin"])
```

- Чем админ отличается от QA; у каких ролей есть запись; иерархия ролей — цепочка подмножеств.
- Вывод: `['delete']`, `['admin', 'qa']`, `True`.

## Покрытие

```python
features = {"login", "search", "pay", "cart"}
tested = {"login", "pay", "profile"}
print(f"покрыто {len(features & tested)} из {len(features)}")
print(sorted(features - tested), sorted(tested - features))
print(round(len(features & tested) / len(features) * 100))
```

- Покрытые — пересечение; непокрытые — разность; «лишние» тесты — обратная разность (может, функция удалена, а тесты остались).
- Вывод: `покрыто 2 из 4`, `['cart', 'search'] ['profile']`, `50`.

## Общие теги и общие друзья

```python
tests = {"a": {"smoke", "api"}, "b": {"api", "slow"}}
print(sorted(set.intersection(*tests.values())))
graph = {"ann": {"bob", "cat"}, "bob": {"ann", "cat"}}
print(sorted(graph["ann"] & graph["bob"]))
```

- `set.intersection(*наборы)` — общее для всех. Общие друзья — пересечение двух наборов.
- Вывод: `['api']`, `['cat']`.

## Итог

- Отбор по тегам: `include & tags` и `not exclude & tags`.
- Права: разность — чем роли отличаются; `<=` — иерархия.
- Покрытие: `&` — покрыто, `-` — не покрыто.
- Общее для многих наборов — `set.intersection(*наборы)`; всё — `set().union(*наборы)`.
'''),
    short=t(r'''
```py
include & tags and not exclude & tags   # отбор тестов
roles["admin"] - roles["qa"]            # чем отличаются
guest <= qa <= admin                    # иерархия
features & tested; features - tested    # покрыто / нет
set.intersection(*sets); set().union(*sets)
```
'''),
    quiz=[
        q('Как выбрать тесты, у которых есть тег из `include` и нет тегов из `exclude`?',
            ['`include | tags`', '`include & tags and not exclude & tags`', '`tags - include`', '`include <= tags`'],
            1, 'Пустое пересечение ложно.'),
        q('Как найти непокрытые функции?',
            ['`features & tested`', '`features - tested`', '`tested - features`', '`features | tested`'],
            1, 'Есть в продукте, нет в тестах.'),
        q('Что вернёт `set.intersection({1, 2}, {2, 3}, {2})`?',
            ['`{1, 2, 3}`', '`{2}`', '`set()`', 'Ошибка'],
            1, 'Общее для всех.'),
    ],
),
}
