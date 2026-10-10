"""Теория модуля «JSON и Python» темы «JSON».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- jsn-m1-l1 ----------
'jsn-m1-l1': dict(
    full=t(r'''
## Зачем это нужно

**JSON** (JavaScript Object Notation) — текстовый формат обмена данными. На нём разговаривают почти все веб-API: ты отправляешь запрос — сервер отвечает JSON-текстом. Тестировщик API работает с JSON каждый день: разбирает ответы, собирает тела запросов, сравнивает ожидаемое с фактическим. В Python для этого есть встроенный модуль `json`.

## Как выглядит JSON

```
{
  "name": "Аня",
  "age": 25,
  "active": true,
  "phone": null,
  "skills": ["qa", "sql"]
}
```

- **Объект** `{...}` — пары `"ключ": значение`; ключи — только строки в **двойных** кавычках.
- **Массив** `[...]` — упорядоченный список значений.
- Значения: строки (`"..."`), числа, `true`/`false`, `null`, объекты, массивы.
- Похоже на словари и списки Python, но это **текст** — строка, которую ещё надо разобрать.

## Соответствие типов

- объект `{}` → `dict`;
- массив `[]` → `list`;
- строка `"..."` → `str`;
- число `10` → `int`, `2.5` → `float`;
- `true` / `false` → `True` / `False`;
- `null` → `None`.

```viz
{"type": "paths", "auto": true, "title": "dumps: во что превращаются значения Python", "cases": [{"label": "{'ok': True, 'next': None}", "code": "import json\nprint(json.dumps({'ok': True, 'next': None}))", "note": "`True` → `true`, `None` → `null`, кавычки — только двойные."}, {"label": "(1, 2)", "code": "import json\nprint(json.dumps((1, 2)))", "note": "Кортежа в JSON нет — станет массивом."}, {"label": "{1: 'a'}", "code": "import json\nprint(json.dumps({1: 'a'}))", "note": "Ключи в JSON — всегда строки: `1` стал `\"1\"`."}, {"label": "'Привет'", "code": "import json\nprint(json.dumps('Привет'))", "note": "Кириллица по умолчанию экранируется. `ensure_ascii=False` оставит буквы как есть."}, {"label": "[3.0, 10, False]", "code": "import json\nprint(json.dumps([3.0, 10, False]))", "note": "Числа как есть, `False` → `false`."}]}
```

## loads — из строки в Python

```python
import json
text = '{"name": "Аня", "age": 25, "skills": ["qa", "sql"]}'
data = json.loads(text)
print(type(text).__name__, type(data).__name__)
print(data["name"], data["skills"][1])
```

- `import json` — подключить модуль.
- `json.loads(строка)` («load string») разбирает JSON-текст и возвращает объект Python.
- После разбора работаем с обычным словарём и списком.
- Вывод: `str dict`, `Аня sql`.

Корнем JSON может быть не только объект:

```python
import json
print(json.loads("[1, 2, 3]"), json.loads("true"), json.loads("null"))
print(json.loads('"текст"'), json.loads("3.5"))
```

Вывод: `[1, 2, 3] True None`, `текст 3.5`.

## dumps — из Python в строку

```python
import json
user = {"name": "Аня", "active": True, "phone": None}
print(json.dumps(user, ensure_ascii=False))
```

- `json.dumps(объект)` («dump string») превращает объект в JSON-строку — например, для тела запроса.
- `True` → `true`, `None` → `null`, кавычки — двойные.
- `ensure_ascii=False` — оставить кириллицу как есть (подробнее — урок «json.dumps»).
- Вывод: `{"name": "Аня", "active": true, "phone": null}`.

## Итог

- JSON — текстовый формат: объекты `{}`, массивы `[]`, строки, числа, `true/false`, `null`.
- `json.loads(строка)` → Python (`dict`, `list`…); `json.dumps(объект)` → строка.
- `true/false/null` ↔ `True/False/None`.
- JSON — это строка; работать с данными можно только после `loads`.
'''),
    short=t(r'''
```py
import json
data = json.loads('{"a": 1, "ok": true, "x": null}')   # строка -> dict
data["ok"]                       # True
text = json.dumps({"a": None})   # dict -> '{"a": null}'
json.dumps(d, ensure_ascii=False)   # кириллица как есть
```
- объект→dict, массив→list, true/false→True/False, null→None.
'''),
    quiz=[
        q('Что вернёт `json.loads("null")`?',
            ['`"null"`', '`None`', '`0`', 'Ошибка'],
            1, 'null соответствует None.'),
        q('Что делает `json.dumps`?',
            ['Разбирает JSON-строку', 'Превращает объект Python в JSON-строку', 'Удаляет данные', 'Читает файл'],
            1, 'dump string.'),
        q('Какие кавычки допустимы для строк в JSON?',
            ['Любые', 'Только двойные', 'Только одинарные', 'Обратные'],
            1, 'Одинарные — ошибка разбора.'),
    ],
),

# ---------- jsn-m1-l2 ----------
'jsn-m1-l2': dict(
    full=t(r'''
## Зачем это нужно

Каждый ответ API начинается с разбора: `json.loads(response_text)`. Нужно знать, что получится для каждого типа JSON, как ведут себя числа и что происходит, если текст — **не** корректный JSON (а это случается: сервер вернул HTML-страницу ошибки или пустое тело).

## Вложенные структуры

```python
import json
data = json.loads('{"a": 1, "b": [true, false], "c": {"d": null}}')
print(data)
print(data["c"]["d"] is None, data["b"][0])
```

- Вложенные объекты и массивы превращаются во вложенные словари и списки.
- Вывод: `{'a': 1, 'b': [True, False], 'c': {'d': None}}`, `True True`.

## Числа

```python
import json
print(type(json.loads("10")).__name__, type(json.loads("10.0")).__name__, type(json.loads("1e3")).__name__)
```

- Число без точки и экспоненты → `int`, с точкой или `e` → `float`.
- Вывод: `int float float`.
- Для проверок типов это важно: `10` и `10.0` в JSON дают разные типы Python.

## Обработка массива объектов

```python
import json
text = '[{"id": 3, "price": 300}, {"id": 7, "price": 150.5}]'
items = json.loads(text)
print([i["id"] for i in items], sum(i["price"] for i in items))
```

Вывод: `[3, 7] 450.5`.

## Некорректный JSON

```python
import json
try:
    json.loads("{'name': 'Аня'}")
except json.JSONDecodeError as e:
    print("ошибка:", e.msg)
```

- Если текст не соответствует формату, `loads` выбрасывает `json.JSONDecodeError`.
- Частые причины: одинарные кавычки, запятая после последнего элемента, ключ без кавычек, пустая строка, HTML вместо JSON.
- `e.msg` — описание ошибки. Вывод: `ошибка: Expecting property name enclosed in double quotes`.

```python
import json

def parse_or_none(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None

print(parse_or_none('{"a": 1}'), parse_or_none("{a: 1}"), parse_or_none(""))
```

Вывод: `{'a': 1} None None`. Подробнее — урок «Ошибки разбора».

## Подсчёты по разобранным данным

```python
import json
data = json.loads('{"a": null, "b": 0, "c": null, "d": ""}')
print(sorted(data), sum(1 for v in data.values() if v is None))
```

- После разбора — обычная работа со словарём. Вывод: `['a', 'b', 'c', 'd'] 2`.

## Итог

- `loads` превращает вложенный JSON во вложенные `dict`/`list`.
- `10` → `int`, `10.0` и `1e3` → `float`.
- Некорректный текст → `json.JSONDecodeError` (атрибут `msg` — описание).
- Частые ошибки формата: одинарные кавычки, лишняя запятая, пустая строка.
'''),
    short=t(r'''
```py
json.loads('{"b": [true], "c": {"d": null}}')   # вложенные dict/list
type(json.loads("10"))    # int
type(json.loads("10.0"))  # float
try:
    json.loads("{'a': 1}")
except json.JSONDecodeError as e:
    e.msg                 # описание ошибки
```
'''),
    quiz=[
        q('Какой тип даст `json.loads("7.0")`?',
            ['int', 'float', 'str', 'Decimal'],
            1, 'Число с точкой — float.'),
        q('Что будет при `json.loads("[1, 2,]")`?',
            ['`[1, 2]`', '`json.JSONDecodeError`', '`[1, 2, None]`', '`None`'],
            1, 'Запятая после последнего элемента недопустима.'),
        q('Что вернёт `json.loads(\'{"x": [true]}\')["x"][0]`?',
            ['`"true"`', '`True`', '`1`', 'Ошибка'],
            1, 'true → True.'),
    ],
),

# ---------- jsn-m1-l3 ----------
'jsn-m1-l3': dict(
    full=t(r'''
## Зачем это нужно

`json.dumps` умеет не только превращать объект в строку, но и форматировать её: красиво с отступами — для отчётов и логов; компактно — для передачи по сети; с отсортированными ключами — для сравнения. Разберём параметры.

## sort_keys и separators

```python
import json
d = {"b": 1, "a": [1, 2]}
print(json.dumps(d))
print(json.dumps(d, sort_keys=True))
print(json.dumps(d, separators=(",", ":")))
```

- По умолчанию ключи идут в порядке словаря, после `,` и `:` — пробелы.
- `sort_keys=True` — ключи по алфавиту (на всех уровнях вложенности).
- `separators=(",", ":")` — разделители без пробелов: самая компактная форма.
- Вывод: `{"b": 1, "a": [1, 2]}`, `{"a": [1, 2], "b": 1}`, `{"b":1,"a":[1,2]}`.

## indent — красивый вывод

```python
import json
print(json.dumps({"x": 1, "y": [1, 2]}, indent=2))
```

- `indent=2` — каждый элемент на своей строке с отступом 2 пробела на уровень.
- Вывод — многострочный JSON, удобный для чтения человеком.

## ensure_ascii — кириллица

```python
import json
print(json.dumps("Привет"))
print(json.dumps("Привет", ensure_ascii=False))
```

- По умолчанию (`ensure_ascii=True`) все не-ASCII символы экранируются: `П…`. Это корректный JSON, но читать неудобно.
- `ensure_ascii=False` — символы как есть.
- Вывод: экранированная строка, затем `"Привет"`.

## Каноническая форма для сравнения

```python
import json

def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"))

print(canonical({"b": 1, "a": 2}), canonical({"b": 1, "a": 2}) == canonical({"a": 2, "b": 1}))
```

- Отсортированные ключи и фиксированные разделители дают одну и ту же строку для одинаковых данных. Такую строку удобно сравнивать, хешировать, хранить как «эталон».
- Вывод: `{"a":2,"b":1} True`.

## Размер в байтах

```python
import json
text = json.dumps({"я": 1}, ensure_ascii=False, separators=(",", ":"))
print(text, len(text), len(text.encode("utf-8")))
```

- `len(строки)` — число символов, а по сети идут **байты**. В UTF-8 кириллическая буква занимает 2 байта.
- Вывод: `{"я":1} 7 8`.

## JSON Lines

```python
import json
records = [{"id": 1}, {"id": 2}]
print("\n".join(json.dumps(r, separators=(",", ":")) for r in records))
```

- Формат **JSON Lines**: один компактный JSON-объект на строку. Так пишут логи и большие выгрузки — их можно читать построчно.
- Вывод: две строки `{"id":1}` и `{"id":2}`.

## Итог

- `sort_keys=True` — ключи по алфавиту; `separators=(",", ":")` — компактно.
- `indent=2` — многострочный читаемый вывод.
- `ensure_ascii=False` — кириллица без `\uXXXX`.
- Канонический JSON (`sort_keys` + компактные разделители) — для сравнения.
- JSON Lines — объект на строку.
'''),
    short=t(r'''
```py
json.dumps(d, sort_keys=True)            # ключи по алфавиту
json.dumps(d, separators=(",", ":"))     # компактно
json.dumps(d, indent=2)                  # красиво
json.dumps(d, ensure_ascii=False)        # кириллица как есть
json.dumps(d, sort_keys=True, separators=(",", ":"))   # канон для сравнения
len(text.encode("utf-8"))                # размер в байтах
```
'''),
    quiz=[
        q('Что делает `ensure_ascii=False`?',
            ['Запрещает кириллицу', 'Оставляет не-ASCII символы без экранирования', 'Сжимает JSON', 'Сортирует ключи'],
            1, 'Без \\uXXXX.'),
        q('Какой параметр даёт многострочный вывод с отступами?',
            ['`sort_keys`', '`indent`', '`separators`', '`pretty`'],
            1, 'indent=2.'),
        q('Зачем `sort_keys=True` при сравнении JSON-строк?',
            ['Быстрее', 'Одинаковые данные дают одинаковую строку', 'Меньше размер', 'Иначе ошибка'],
            1, 'Порядок ключей перестаёт влиять.'),
    ],
),

# ---------- jsn-m1-l4 ----------
'jsn-m1-l4': dict(
    full=t(r'''
## Зачем это нужно

Не все объекты Python переводятся в JSON один в один. Кортеж возвращается списком, числовые ключи становятся строками, а множества и даты не сохраняются вовсе. Эти «потери при переводе» — частая причина упавших тестов вида «было `{1: ...}`, стало `{"1": ...}`».

## Что меняется при dumps → loads

```python
import json
data = {"t": (1, 2), 1: "one", "ok": True, "none": None}
text = json.dumps(data)
print(text)
back = json.loads(text)
print(back["t"], back["1"], back == data)
```

- Кортеж `(1, 2)` → массив `[1, 2]` → после `loads` **список**.
- Ключ-число `1` → строка `"1"`: в JSON ключи объектов — только строки.
- `True` → `true`, `None` → `null` — эти возвращаются как были.
- Итог: `back != data`. Вывод: JSON-строка, затем `[1, 2] one False`.

## Что не сохраняется

```python
import json
try:
    json.dumps({"tags": {"a", "b"}})
except TypeError as e:
    print("TypeError:", e)
```

- Множества, даты, свои объекты — `TypeError: Object of type set is not JSON serializable`.
- Вывод: `TypeError: Object of type set is not JSON serializable`.

## Параметр default

```python
import json
from datetime import date
print(json.dumps({"d": date(2024, 1, 15)}, default=str))
```

- `default=функция` — вызывается для каждого объекта, который JSON не умеет сохранять; её результат сохраняется вместо объекта.
- `default=str` — превратить в строку. Вывод: `{"d": "2024-01-15"}`.

Своя функция-конвертер:

```python
import json

def convert(obj):
    if isinstance(obj, set):
        return sorted(obj)
    raise TypeError(f"не умею сохранять {type(obj).__name__}")

print(json.dumps({"tags": {"b", "a"}}, default=convert))
```

- Множество → отсортированный список (отсортированный — чтобы результат был стабильным).
- Для неизвестных типов — снова `TypeError`, чтобы ошибки не прятались. Вывод: `{"tags": ["a", "b"]}`.

## Восстановление числовых ключей

```python
back = {"1": "a", "20": "b", "x": "c"}
print({int(k) if k.isdigit() else k: v for k, v in back.items()})
```

Вывод: `{1: 'a', 20: 'b', 'x': 'c'}`.

## Проверка «туда-обратно»

```python
import json
for data in ({"a": [1, 2]}, {"a": (1, 2)}, {1: "x"}):
    print(json.loads(json.dumps(data)) == data)
```

- Такая проверка показывает, переживут ли данные сохранение в JSON без изменений. Вывод: `True`, `False`, `False`.

## Итог

- `tuple` → `list`; ключи-числа → строки; `True/None` → `true/null` и обратно.
- `set`, даты, свои объекты — `TypeError: not JSON serializable`.
- `default=str` или своя функция — как сохранять «неудобные» объекты.
- `json.loads(json.dumps(x)) == x` — проверка, что данные не исказятся.
'''),
    short=t(r'''
```py
json.dumps((1, 2))          # "[1, 2]" — вернётся списком
json.dumps({1: "a"})        # '{"1": "a"}' — ключ стал строкой
json.dumps({1, 2})          # TypeError: not JSON serializable
json.dumps(obj, default=str)
json.loads(json.dumps(x)) == x   # переживёт ли JSON
```
'''),
    quiz=[
        q('Что вернёт `json.loads(json.dumps((1, 2)))`?',
            ['`(1, 2)`', '`[1, 2]`', '`"(1, 2)"`', 'Ошибка'],
            1, 'Кортеж становится массивом.'),
        q('Что будет с ключом `5` в `json.dumps({5: "x"})`?',
            ['Ошибка', 'Станет строкой "5"', 'Останется числом', 'Удалится'],
            1, 'Ключи объектов JSON — строки.'),
        q('Что делает параметр `default` у `json.dumps`?',
            ['Значение по умолчанию для пустых полей', 'Функция для объектов, которые JSON не умеет сохранять', 'Кодировка', 'Отступ'],
            1, 'Например, default=str.'),
    ],
),
}
