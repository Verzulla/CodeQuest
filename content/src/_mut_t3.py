"""Теория модуля «Практика» темы «Изменяемые и неизменяемые».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- mut-iterate ----------
'mut-iterate': dict(
    full=t(r'''
## Зачем это нужно

«Пройти по списку и удалить лишнее» — одна из самых частых задач. Если удалять элементы из списка прямо во время перебора `for`, часть элементов будет пропущена. А словарь во время перебора вообще нельзя менять по размеру.

## Удаление при переборе пропускает элементы

```python
nums = [1, 2, 2, 3, 2, 4]
for n in nums:
    if n == 2:
        nums.remove(n)
print(nums)
```

- `for` идёт по индексам 0, 1, 2… Когда элемент удалён, все следующие сдвигаются влево, и цикл «перешагивает» через тот, что встал на место удалённого.
- Вывод: `[1, 3, 2, 4]` — одна двойка осталась!

## Правильно: новый список или копия

```python
nums = [1, 2, 2, 3, 2, 4]
print([n for n in nums if n != 2])

for n in nums[:]:
    if n == 2:
        nums.remove(n)
print(nums)

data = [1, -2, 3, -4]
data[:] = [x for x in data if x >= 0]
print(data)
```

- Лучший вариант — построить новый список списковым включением.
- Если нужно изменить **тот же** список — перебирай копию (`nums[:]`) или замени содержимое `data[:] = ...`.
- Вывод: `[1, 3, 4]`, `[1, 3, 4]`, `[1, 3]`.

## Словарь нельзя менять во время перебора

```python
d = {"a": 1, "b": 2}
try:
    for k in d:
        d[k + "!"] = 0
except RuntimeError as e:
    print(e)
for k in list(d):
    if d[k] == 0:
        del d[k]
print(d)
```

- Добавление или удаление ключей во время перебора словаря → `RuntimeError`.
- `list(d)` — копия ключей; по ней перебирать безопасно, а удалять — из оригинала.
- Менять **значения** существующих ключей во время перебора можно.
- Вывод: `dictionary changed size during iteration`, `{'a': 1, 'b': 2}`.

## Очередь: while вместо for

```python
queue = ["a", "b"]
done = []
while queue:
    task = queue.pop(0)
    done.append(task)
    if task == "a":
        queue.extend(["a1", "a2"])
print(done, queue)
```

- Если коллекция должна меняться по ходу обработки (очередь задач, обход дерева), используй `while` и явное извлечение элементов.
- `pop(0)` берёт элемент с начала. Для длинных очередей быстрее `collections.deque` с `popleft()`.
- Вывод: `['a', 'b', 'a1', 'a2'] []`.

## Итог

- Не удаляй из списка во время `for` по нему самому.
- Новый список через включение; или перебор копии `lst[:]`; или `lst[:] = [...]`.
- Словарь: перебирай `list(d)`, если меняешь ключи.
- Очередь — `while queue: queue.pop(0)`.
'''),
    short=t(r'''
```py
for x in lst: lst.remove(x)          # ✗ пропуски
lst = [x for x in lst if ok(x)]      # ✓ новый
lst[:] = [x for x in lst if ok(x)]   # ✓ тот же объект
for x in lst[:]: lst.remove(x)       # ✓ по копии
for k in list(d): del d[k]           # ✓ словарь
while queue: task = queue.pop(0)     # ✓ очередь
```
'''),
    quiz=[
        q('Что будет при удалении элементов списка во время `for` по нему?',
            ['Всё удалится правильно', 'Некоторые элементы будут пропущены', 'Ошибка', 'Бесконечный цикл'],
            1, 'Элементы сдвигаются.'),
        q('Что будет при добавлении ключей в словарь во время перебора?',
            ['Ничего', 'RuntimeError', 'Ключи пропустятся', 'KeyError'],
            1, 'Размер словаря нельзя менять при переборе.'),
        q('Как безопасно удалять ключи словаря в цикле?',
            ['for k in d', 'for k in list(d)', 'for k in d.values()', 'Нельзя'],
            1, 'Перебираем копию ключей.'),
    ],
),

# ---------- mut-frozen ----------
'mut-frozen': dict(
    full=t(r'''
## Зачем это нужно

Неизменяемые данные безопаснее: их можно спокойно передавать куда угодно, класть в множества и использовать как ключи, не боясь, что кто-то их испортит. Для настроек, эталонов, координат, версий удобно сразу выбирать неизменяемые структуры.

## tuple и frozenset

```python
point = (3, 4)
try:
    point[0] = 10
except TypeError as e:
    print(e)
roles = frozenset({"read", "write"})
try:
    roles.add("admin")
except AttributeError as e:
    print(e)
print("read" in roles)
```

- Кортеж — неизменяемый список, `frozenset` — неизменяемое множество (нет методов `add`, `remove`).
- Вывод: `'tuple' object does not support item assignment`, `'frozenset' object has no attribute 'add'`, `True`.

## Словарь только для чтения

```python
from types import MappingProxyType

_settings = {"url": "prod", "timeout": 5}
SETTINGS = MappingProxyType(_settings)
print(SETTINGS["url"])
try:
    SETTINGS["url"] = "test"
except TypeError as e:
    print(e)
_settings["timeout"] = 10
print(SETTINGS["timeout"])
```

- `MappingProxyType(d)` — «окно» в словарь: читать можно, писать нельзя.
- Изменения **исходного** словаря в окне видны. Чтобы результат был полностью неизменным — оборачивай копию: `MappingProxyType(dict(d))`.
- Вывод: `prod`, `'mappingproxy' object does not support item assignment`, `10`.

## namedtuple

```python
from collections import namedtuple

Point = namedtuple("Point", "x y")
p = Point(1, 2)
print(p, p.x, p[1])
print(p._replace(x=10), p)
```

- Кортеж с именованными полями: доступ по имени и по индексу, неизменяемый, хешируемый.
- `_replace(поле=...)` — новая копия с изменённым полем.
- Вывод: `Point(x=1, y=2) 1 2`, `Point(x=10, y=2) Point(x=1, y=2)`.

## frozen dataclass

```python
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class User:
    name: str
    age: int

u = User("Аня", 30)
try:
    u.age = 31
except Exception as e:
    print(type(e).__name__)
print(replace(u, age=31), u)
print(len({u, User("Аня", 30)}))
```

- `frozen=True` запрещает менять поля после создания и делает объект хешируемым.
- «Изменение» — создание нового объекта через `replace`.
- Вывод: `FrozenInstanceError`, `User(name='Аня', age=31) User(name='Аня', age=30)`, `1`.

## Неизменяемость — поверхностная

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Team:
    name: str
    members: list

t = Team("qa", ["Аня"])
t.members.append("Боря")
print(t)
```

- Нельзя заменить поле `members`, но сам список внутри — изменяемый. Для полной неизменности храни `tuple` или `frozenset`.
- Вывод: `Team(name='qa', members=['Аня', 'Боря'])`.

## Итог

- `tuple`, `frozenset` — неизменяемые коллекции.
- `MappingProxyType(dict(d))` — словарь только для чтения.
- `namedtuple`, `@dataclass(frozen=True)` — неизменяемые записи; изменение — `_replace`/`replace`.
- Неизменяемость поверхностная: вложенные списки лучше заменить кортежами.
'''),
    short=t(r'''
```py
point = (3, 4)                         # tuple
roles = frozenset({"read"})            # frozenset
from types import MappingProxyType
CFG = MappingProxyType(dict(cfg))      # dict только для чтения

from collections import namedtuple
P = namedtuple("P", "x y"); p._replace(x=1)

@dataclass(frozen=True)
class User: name: str
replace(u, name="X")                   # новый объект
```
'''),
    quiz=[
        q('Что вернёт попытка `roles.add("x")` для `frozenset`?',
            ['Добавит', 'AttributeError — метода нет', 'TypeError', 'None'],
            1, 'frozenset не имеет методов изменения.'),
        q('Как «изменить» поле frozen dataclass?',
            ['obj.field = x', 'Создать новый через dataclasses.replace', 'Нельзя никак', 'setattr'],
            1, 'replace возвращает копию.'),
        q('Видны ли в `MappingProxyType(d)` изменения исходного `d`?',
            ['Нет', 'Да', 'Только новые ключи', 'Ошибка'],
            1, 'Это окно, а не копия.'),
    ],
),

# ---------- mut-classes ----------
'mut-classes': dict(
    full=t(r'''
## Зачем это нужно

Объекты своих классов изменяемы, а их атрибуты часто — списки и словари. Здесь поджидают три ловушки: общий изменяемый атрибут класса, утечка внутреннего списка наружу и хранение чужого списка без копии.

## Общий атрибут класса

```python
class Cart:
    items = []

    def add(self, x):
        self.items.append(x)

a, b = Cart(), Cart()
a.add("чай")
print(b.items, a.items is b.items)
```

- `items = []` в теле класса — один список на **все** объекты.
- Решение: создавать список в `__init__` через `self.items = []`.
- Вывод: `['чай'] True`.

## Утечка внутреннего списка

```python
class Team:
    def __init__(self):
        self._members = []

    def add(self, name):
        self._members.append(name)

    def members(self):
        return self._members

    def members_copy(self):
        return tuple(self._members)

t = Team()
t.add("Аня")
t.members().append("Взломщик")
print(t._members)
print(t.members_copy())
```

- Возвращая `self._members`, класс отдаёт ссылку на своё внутреннее состояние — любой может изменить состав команды в обход `add`.
- Возвращай копию или неизменяемый кортеж.
- Вывод: `['Аня', 'Взломщик']`, `('Аня', 'Взломщик')`.

## Хранение чужого списка

```python
class Order:
    def __init__(self, items):
        self.items = list(items)

prices = [100, 200]
o = Order(prices)
prices.append(1000)
print(o.items)
```

- `list(items)` — защитная копия. Без неё заказ менялся бы вместе со списком вызывающего кода.
- Вывод: `[100, 200]`.

## Один объект в нескольких местах

```python
class User:
    def __init__(self, name):
        self.name = name

u = User("аня")
admins = [u]
everyone = [u, User("боря")]
admins[0].name = "АНЯ"
print([x.name for x in everyone])
```

- В двух списках лежит **один и тот же** объект. Изменение через один список видно через другой. Иногда это и нужно (один пользователь), иногда — баг.
- Вывод: `['АНЯ', 'боря']`.

## Неизменяемый объект с «изменениями»

```python
from types import MappingProxyType

class Settings:
    def __init__(self, values):
        self._values = dict(values)

    @property
    def values(self):
        return MappingProxyType(self._values)

    def with_value(self, key, value):
        return Settings({**self._values, key: value})

s = Settings({"url": "prod"})
s2 = s.with_value("url", "test")
print(s.values["url"], s2.values["url"])
```

- Вместо изменения — метод, возвращающий новый объект. Старые ссылки остаются корректными.
- Вывод: `prod test`.

## Итог

- Изменяемые атрибуты — в `__init__`, не в теле класса.
- Не отдавай внутренние списки наружу: копия, `tuple`, `MappingProxyType`.
- Сохраняй копию переданных коллекций (`list(items)`, `dict(values)`).
- Для «неизменяемых» классов — методы, возвращающие новый объект.
'''),
    short=t(r'''
```py
class Team:
    def __init__(self, members=()):
        self._members = list(members)   # защитная копия

    def members(self):
        return tuple(self._members)     # не отдаём внутренний список

# НЕ: items = [] в теле класса
# «изменение» неизменяемого: return Settings({**self._values, k: v})
```
'''),
    quiz=[
        q('Чем опасен метод, возвращающий `self._items`?',
            ['Ничем', 'Внешний код может изменить внутреннее состояние', 'Медленно', 'Ошибка'],
            1, 'Отдавай копию или кортеж.'),
        q('Зачем в `__init__` писать `self.items = list(items)`?',
            ['Чтобы превратить в список', 'Защитная копия — внешние изменения не влияют на объект', 'Так быстрее', 'Не нужно'],
            1, 'Иначе объект делит список с вызывающим кодом.'),
        q('Где создавать изменяемые атрибуты объекта?',
            ['В теле класса', 'В __init__ через self', 'В глобальной области', 'Не важно'],
            1, 'Атрибут класса — общий для всех.'),
    ],
),

# ---------- mut-tests ----------
'mut-tests': dict(
    full=t(r'''
## Зачем это нужно

Тесты должны быть **независимыми**: результат одного не должен зависеть от того, какие тесты выполнились до него. Общие изменяемые данные ломают это правило: один тест испортил эталон — упали другие. Такие «плавающие» падения очень трудно искать. Решения: фабрики, глубокие копии, неизменяемые эталоны, проверка, что функция не меняет вход.

## Данные протекают между тестами

```python
USER = {"name": "test", "roles": ["reader"]}

def check_admin():
    user = USER
    user["roles"].append("admin")
    return user["roles"]

def check_reader():
    return USER["roles"] == ["reader"]

print(check_admin())
print(check_reader())
```

- `user = USER` — не копия. Первый «тест» испортил общий эталон, второй получил неверные данные.
- Если поменять порядок запуска — оба пройдут. Так появляются тесты, которые падают «иногда».
- Вывод: `['reader', 'admin']`, `False`.

## Фабрика: новые данные на каждый вызов

```python
def make_user(**overrides):
    user = {"name": "test", "roles": ["reader"]}
    user.update(overrides)
    return user

a = make_user()
a["roles"].append("admin")
b = make_user(name="боря")
print(a)
print(b)
```

- Литералы `{...}` и `[...]` внутри функции создают новые объекты при каждом вызове.
- `**overrides` — меняем только поля, важные для теста.
- В pytest то же делают фикстуры (они вызываются заново для каждого теста) или библиотеки вроде `factory_boy`.
- Вывод: `{'name': 'test', 'roles': ['reader', 'admin']}`, `{'name': 'боря', 'roles': ['reader']}`.

## Эталон + глубокая копия

```python
import copy

FIXTURES = {"cart": {"items": [{"sku": "A1", "qty": 1}]}}

def load_fixture(name):
    return copy.deepcopy(FIXTURES[name])

c = load_fixture("cart")
c["items"][0]["qty"] = 99
print(load_fixture("cart"))
```

- Эталон хранится в одном месте, а тесты получают свои независимые копии.
- Вывод: `{'items': [{'sku': 'A1', 'qty': 1}]}`.

## Проверка: функция не меняет вход

```python
import copy

def top3(scores):
    scores.sort(reverse=True)
    return scores[:3]

data = [5, 1, 9, 3, 7]
snapshot = copy.deepcopy(data)
print(top3(data))
print("вход не изменён:", data == snapshot)
```

- Снимок до вызова + сравнение после — простой способ поймать побочный эффект.
- Здесь `top3` испортила порядок входного списка — это баг: правильнее `sorted(scores, reverse=True)[:3]`.
- Вывод: `[9, 7, 5]`, `вход не изменён: False`.

## Сравнение состояний до и после

```python
before = {"a": 1, "b": 2}
after = {"a": 1, "c": 3}
print(sorted(after.keys() - before.keys()), sorted(before.keys() - after.keys()))
```

- `keys()` поддерживает операции множеств: разность показывает добавленные и удалённые ключи.
- Вывод: `['c'] ['b']`.

## Итог

- Общие изменяемые данные между тестами — источник «плавающих» падений.
- Фабрики и фикстуры создают свежие данные для каждого теста.
- Эталоны отдавай через `copy.deepcopy`.
- Проверяй, что функции не меняют входные данные: снимок до, сравнение после.
'''),
    short=t(r'''
```py
def make_user(**kw):                   # фабрика
    u = {"name": "test", "roles": []}  # новые объекты каждый раз
    u.update(kw)
    return u

def load_fixture(name):
    return copy.deepcopy(FIXTURES[name])

snap = copy.deepcopy(arg); f(arg); assert arg == snap   # не меняет вход
after.keys() - before.keys()           # добавленные ключи
```
'''),
    quiz=[
        q('Почему тесты с общими изменяемыми данными «плавают»?',
            ['Из-за сети', 'Результат зависит от порядка запуска тестов', 'Из-за pytest', 'Не плавают'],
            1, 'Один тест портит данные другому.'),
        q('Как фабрика защищает от протекания данных?',
            ['Кэширует объект', 'Создаёт новые объекты при каждом вызове', 'Замораживает словарь', 'Удаляет данные'],
            1, 'Литералы внутри функции — новые объекты.'),
        q('Как проверить, что функция не изменила аргумент?',
            ['Никак', 'Сохранить глубокую копию до вызова и сравнить после', 'Проверить id', 'Посмотреть return'],
            1, 'id не меняется при изменении на месте.'),
    ],
),

}
