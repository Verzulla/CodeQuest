"""Теория модуля «Лямбды на практике» темы «lambda».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- lam-dispatch ----------
'lam-dispatch': dict(
    full=t(r'''
## Зачем это нужно

Словарь, где значения — функции, заменяет длинные цепочки `if/elif`: «операция → как вычислить», «команда → что сделать», «правило → как проверить». Лямбды удобно класть в такие словари прямо при объявлении.

## Калькулятор на словаре

```python
ops = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b}
for op in "+-*":
    print(op, ops[op](6, 3))
```

- `ops[op]` достаёт функцию, `(6, 3)` — вызывает. Новая операция — одна строка в словаре.
- Вывод: `+ 9`, `- 3`, `* 18`.

Особые случаи — условным выражением внутри лямбды или проверкой снаружи:

```python
OPS = {"/": lambda a, b: a / b if b != 0 else None}
func = OPS.get("%")
print(OPS["/"](6, 0), func(1, 2) if func else None)
```

Вывод: `None None`.

## Готовые функции и лямбды вместе

```python
formatters = {"upper": str.upper, "title": str.title, "reverse": lambda s: s[::-1]}
text = "hello world"
print([formatters[name](text) for name in ["upper", "reverse"]])
print({"upper": str.upper}.get("zzz", lambda s: s)("без изменений"))
```

- Значением может быть любая функция. Умолчание в `get` — лямбда «ничего не делать».
- Вывод: `['HELLO WORLD', 'dlrow olleh']`, `без изменений`.

## Правила проверки

```python
rules = {
    "not empty": lambda s: bool(s.strip()),
    "short": lambda s: len(s) <= 5,
}
for value in ["abc", "   ", "abcdef"]:
    print(repr(value), [name for name, check in rules.items() if not check(value)])
```

- Каждое правило — название и функция-проверка. Результат — список нарушенных правил: удобно для сообщений валидации.
- Вывод: `'abc' []`, `'   ' ['not empty']`, `'abcdef' ['short']`.

## Конвейер шагов по названиям

```python
STEPS = {"double": lambda x: x * 2, "inc": lambda x: x + 1, "square": lambda x: x * x}
value = 3
for name in ["inc", "double", "square"]:
    value = STEPS[name](value)
print(value)
```

- Последовательность обработки задаётся списком названий — например, из конфига. Вывод: `64`.

## Итог

- Словарь «ключ → функция» заменяет `if/elif` и легко расширяется.
- `d[key](args)` — достать и вызвать; `d.get(key, умолчание)` — с запасным вариантом.
- Значения — готовые функции или лямбды.
- Правила валидации и шаги обработки удобно хранить так же.
'''),
    short=t(r'''
```py
OPS = {"+": lambda a, b: a + b, "*": lambda a, b: a * b}
OPS[op](a, b)                              # достать и вызвать
COMMANDS.get(cmd, lambda s: s)(text)       # умолчание — ничего не делать
[name for name, check in rules.items() if not check(v)]
```
'''),
    quiz=[
        q('Что вернёт `{"+": lambda a, b: a + b}["+"](2, 3)`?',
            ['Функцию', '`5`', '`"+"`', 'Ошибка'],
            1, 'Достали лямбду и вызвали.'),
        q('Зачем в `d.get(cmd, lambda s: s)(text)` лямбда по умолчанию?',
            ['Для скорости', 'Неизвестная команда вернёт текст без изменений', 'Иначе SyntaxError', 'Не нужна'],
            1, 'Функция «ничего не делать».'),
        q('Что хранится в словаре правил `{"short": lambda s: len(s) <= 5}`?',
            ['Строки', 'Функции-проверки', 'Числа', 'Списки'],
            1, 'Значения — функции.'),
    ],
),

# ---------- lam-sortkeys ----------
'lam-sortkeys': dict(
    full=t(r'''
## Зачем это нужно

Реальные данные редко сортируются «как есть»: пустые значения должны уходить в конец, `img10` — идти после `img2`, приоритеты — в своём порядке. Всё это решается правильным **ключом** — лямбдой или функцией.

## None в конец

```python
items = [3, None, 1, None, 2]
print(sorted(items, key=lambda x: (x is None, x if x is not None else 0)))
```

- `None` нельзя сравнивать с числами — прямая сортировка упала бы с `TypeError`.
- Ключ-кортеж: первый элемент `x is None` — `False` для чисел и `True` для `None`; `False < True`, поэтому числа идут раньше. Второй элемент упорядочивает числа (для `None` подставлен 0, чтобы сравнение не падало).
- Вывод: `[1, 2, 3, None, None]`.

## «Естественная» сортировка

```python
files = ["img10.png", "img2.png", "img1.png"]
print(sorted(files))
print(sorted(files, key=lambda f: int(f[3:-4])))
```

- Строки сравниваются посимвольно: `"img10"` < `"img2"`, потому что `"1"` < `"2"`.
- Ключ вырезает числовую часть и превращает в `int`.
- Вывод: `['img1.png', 'img10.png', 'img2.png']`, `['img1.png', 'img2.png', 'img10.png']`.

Для общего случая ключ удобнее вынести в функцию:

```python
def natural_key(name):
    prefix = name.rstrip("0123456789")
    digits = name[len(prefix):]
    return (prefix, int(digits) if digits else 0)

print(sorted(["test10", "test2", "case1", "test"], key=natural_key))
```

- `rstrip("0123456789")` убирает цифры с конца — остаётся буквенная часть; цифры — то, что было отрезано.
- Вывод: `['case1', 'test', 'test2', 'test10']`.

## Свой порядок через словарь рангов

```python
tasks = [("low", "b"), ("high", "a"), ("mid", "c"), ("high", "d")]
prio = {"high": 0, "mid": 1, "low": 2}
print(sorted(tasks, key=lambda t: (prio[t[0]], t[1])))
```

- Вывод: `[('high', 'a'), ('high', 'd'), ('mid', 'c'), ('low', 'b')]`.

## Сначала упавшие, потом по времени

```python
results = [("a", "pass", 1), ("b", "fail", 2), ("c", "fail", 5), ("d", "pass", 3)]
print([r[0] for r in sorted(results, key=lambda r: (r[1] != "fail", -r[2]))])
```

- `r[1] != "fail"` — `False` для упавших (идут первыми); `-r[2]` — время по убыванию.
- Вывод: `['c', 'b', 'd', 'a']`.

## Итог

- Логический элемент ключа `(условие, ...)` делит на группы: `False` раньше `True`.
- `None` в конец — `(x is None, x or 0)`; числа в строках — вырезать и `int`.
- Нестандартный порядок — словарь рангов.
- Сложный ключ — в отдельную функцию и `key=функция`.
'''),
    short=t(r'''
```py
sorted(xs, key=lambda x: (x is None, x if x is not None else 0))   # None в конец
sorted(files, key=lambda f: int(f[3:-4]))                           # числа как числа
sorted(tasks, key=lambda t: (PRIO[t[0]], t[1]))                     # свой порядок
sorted(rs, key=lambda r: (r[1] != "fail", -r[2]))                   # группы + убывание
```
'''),
    quiz=[
        q('Что будет при `sorted([2, None, 1])`?',
            ['`[None, 1, 2]`', '`TypeError`', '`[1, 2, None]`', '`[2, None, 1]`'],
            1, 'None нельзя сравнить с числом.'),
        q('Почему `sorted(["img10", "img2"])` даёт `["img10", "img2"]`?',
            ['Баг', 'Строки сравниваются посимвольно: "1" < "2"', 'Сортировка по длине', 'Так задумано для чисел'],
            1, 'Нужен ключ с int.'),
        q('Какие элементы окажутся первыми при `key=lambda r: (r.status != "fail", ...)`?',
            ['pass', 'fail — у них False', 'Случайные', 'Ошибка'],
            1, 'False < True.'),
    ],
),

# ---------- lam-pitfalls ----------
'lam-pitfalls': dict(
    full=t(r'''
## Зачем это нужно

Лямбды удобны, но у них есть характерные ловушки: позднее связывание переменных, безымянность в отладке, соблазн запихнуть в одну строку слишком много. Разберём, как их избегать и когда лучше обычная функция.

## Позднее связывание

```python
adders = [lambda x: x + i for i in range(3)]
print([f(10) for f in adders])
adders = [lambda x, i=i: x + i for i in range(3)]
print([f(10) for f in adders])
```

- Все лямбды первого списка ссылаются на **одну** переменную `i`, к моменту вызова равную 2.
- `i=i` фиксирует значение при создании. Вывод: `[12, 12, 12]`, `[10, 11, 12]`.

## Лямбда читает переменную в момент вызова

```python
factor = 2
scale = lambda x: x * factor
print(scale(5))
factor = 10
print(scale(5))
```

- Лямбда не запоминает значение `factor` при создании — она читает переменную при каждом вызове. Изменили переменную — изменилось поведение.
- Вывод: `10`, `50`.

## Безымянность

```python
checks = [lambda x: x > 0, lambda x: x < 100]
print([c.__name__ for c in checks])

def positive(x):
    return x > 0

print(positive.__name__)
```

- В сообщениях об ошибках и отчётах тестов лямбда видна как `<lambda>` — непонятно, какая именно упала.
- Вывод: `['<lambda>', '<lambda>']`, `positive`.

## PEP 8: не присваивай лямбду имени

```py
is_adult = lambda age: age >= 18      # плохо
def is_adult(age):                    # хорошо
    return age >= 18
```

- Если функции нужно имя — пиши `def`: у неё будет нормальное `__name__`, можно добавить docstring, аннотации и несколько строк.

## Не усложняй

```python
grade = lambda s: "A" if s >= 90 else "B" if s >= 75 else "C" if s >= 60 else "F"
print(grade(80))
```

- Работает (вывод: `B`), но читать тяжело. Цепочку условий лучше записать `def` с `if/elif/else`.
- Правило: если лямбда не читается с одного взгляда — это функция.

## Побочные эффекты — не в map и лямбде

```python
result = []
list(map(lambda x: result.append(x * 2), [1, 2]))
print(result, list(map(lambda x: x * 2, [1, 2])))
```

- Первый вариант использует `map` ради побочного эффекта `append` и создаёт бесполезный список `None`. Второй — строит результат напрямую.
- Вывод: `[2, 4] [2, 4]`.

## Изменяемое значение по умолчанию

```python
collect = lambda x, acc=[]: acc.append(x) or acc
print(collect(1), collect(2))
```

- Та же ловушка, что у `def` (тема «Функции»): список по умолчанию создаётся один раз и накапливается. Вывод: `[1, 2] [1, 2]` — оба вызова вернули один и тот же список.

## Итог

- Лямбды в цикле — `lambda x, i=i: ...`.
- Лямбда читает внешние переменные при вызове, а не при создании.
- Нужно имя, docstring или несколько условий — `def`.
- Не используй `map`/лямбды ради побочных эффектов.
- Изменяемое значение по умолчанию — ловушка и в лямбде.
'''),
    short=t(r'''
```py
[lambda x, i=i: x + i for i in range(3)]   # фиксация значения
scale = lambda x: x * factor               # factor читается при вызове
f.__name__ == "<lambda>"                   # в отладке безымянна
is_adult = lambda a: a >= 18               # PEP 8: лучше def
lambda x, acc=[]: ...                      # общий список — ловушка
```
'''),
    quiz=[
        q('Что выведет `[f() for f in [lambda: i for i in range(2)]]`?',
            ['`[0, 1]`', '`[1, 1]`', '`[0, 0]`', 'Ошибка'],
            1, 'Позднее связывание.'),
        q('Почему по PEP 8 не пишут `f = lambda x: ...`?',
            ['Не работает', 'Для именованной функции есть def с нормальным именем', 'Медленно', 'Запрещено синтаксисом'],
            1, 'Лямбда безымянна.'),
        q('Какое значение `factor` использует `lambda x: x * factor`?',
            ['На момент создания', 'На момент вызова', 'Всегда 0', 'Ошибка'],
            1, 'Переменная читается при вызове.'),
    ],
),

# ---------- lam-practice ----------
'lam-practice': dict(
    full=t(r'''
## Зачем это нужно

Соберём лямбды в типичных задачах обработки результатов тестов: сортировка, отбор, свёртка, обработчики ответов, настраиваемое форматирование через функцию-параметр.

## Сортировка и отбор

```python
tests = [{"name": "login", "time": 1.2, "ok": True},
         {"name": "pay", "time": 3.4, "ok": False},
         {"name": "cart", "time": 0.5, "ok": True}]
print([t["name"] for t in sorted(tests, key=lambda t: -t["time"])])
print(list(map(lambda t: t["name"], filter(lambda t: not t["ok"], tests))))
print([t["name"] for t in sorted(tests, key=lambda t: (t["ok"], -t["time"]))])
```

- Самые долгие первыми; имена упавших; упавшие первыми, внутри — по времени.
- `t["ok"]` в ключе: `False < True`, поэтому упавшие впереди.
- Вывод: `['pay', 'login', 'cart']`, `['pay']`, `['pay', 'login', 'cart']`.

## Свёртка и максимум

```python
from functools import reduce
tests = [{"time": 1.2}, {"time": 3.4}, {"time": 0.5}]
print(round(reduce(lambda acc, t: acc + t["time"], tests, 0), 1))
print(max(tests, key=lambda t: t["time"])["time"])
print(round(sum(t["time"] for t in tests), 1))
```

- Общее время через `reduce` и то же через `sum` с генератором (проще). Вывод: `5.1`, `3.4`, `5.1`.

## Обработчики ответов

```python
handlers = {
    200: lambda body: f"ok: {body}",
    404: lambda body: "не найдено",
}
for code, body in [(200, "{}"), (404, ""), (500, "x")]:
    print(handlers.get(code, lambda b: f"ошибка {code}")(body))
```

- Словарь «код → обработчик» и обработчик по умолчанию. Лямбда-умолчание читает `code` при вызове — здесь она вызывается сразу, поэтому видит текущий код.
- Вывод: `ok: {}`, `не найдено`, `ошибка 500`.

## Функция-параметр со значением по умолчанию

```python
def build_report(tests, formatter=lambda t: f"{t['name']}: {'ok' if t['ok'] else 'fail'}"):
    return [formatter(t) for t in tests]

tests = [{"name": "a", "ok": True}, {"name": "b", "ok": False}]
print(build_report(tests))
print(build_report(tests, lambda t: t["name"].upper()))
```

- Поведение по умолчанию задано лямбдой, но вызывающий код может передать свою. Лямбда — неизменяемое значение по умолчанию, ловушки со списком тут нет.
- Вывод: `['a: ok', 'b: fail']`, `['A', 'B']`.

## Итог

- `sorted`/`max` с лямбдой-ключом — упорядочить и найти лучший.
- `filter` + `map` с лямбдами — отобрать и преобразовать (или включение).
- Словарь лямбд — обработчики по кодам и командам.
- Функция-параметр с лямбдой по умолчанию — настраиваемое поведение.
'''),
    short=t(r'''
```py
sorted(tests, key=lambda t: (t["ok"], -t["time"]))
list(map(lambda t: t["name"], filter(lambda t: not t["ok"], tests)))
handlers.get(code, lambda b: f"ошибка {code}")(body)
def build_report(tests, formatter=lambda t: t["name"]): ...
```
'''),
    quiz=[
        q('Какие тесты окажутся первыми при `key=lambda t: t["ok"]`?',
            ['ok=True', 'ok=False', 'Случайные', 'Ошибка'],
            1, 'False < True.'),
        q('Безопасна ли лямбда как значение параметра по умолчанию?',
            ['Нет, как список', 'Да — функцию не изменить', 'Только без аргументов', 'Запрещено'],
            1, 'Ловушка — только у изменяемых значений.'),
        q('Что проще для суммы времени тестов?',
            ['`reduce(lambda a, t: a + t["time"], tests, 0)`', '`sum(t["time"] for t in tests)`', 'Одинаково', 'Цикл while'],
            1, 'sum с генератором.'),
    ],
),
}
