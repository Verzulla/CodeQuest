"""Теория модуля «JSON в тестах API» темы «JSON».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- jsn-m3-l1 ----------
'jsn-m3-l1': dict(
    full=t(r'''
## Зачем это нужно

Проверка ответа API — это не только «статус 200». Нужно убедиться, что в теле есть **все обязательные поля** и что у них **правильные типы**: частый баг бэкенда — `"id": "7"` (строка) вместо `7` (число), или `null` там, где ожидали список.

## Проверка типов

```python
import json
body = json.loads('{"id": 7, "name": "Аня", "tags": [], "score": 4.5}')
checks = {"id": int, "name": str, "tags": list, "score": float}
print(all(isinstance(body[k], t) for k, t in checks.items()))
```

- Схема «поле → тип» и `isinstance` для каждого поля. Вывод: `True`.

```python
import json
body = json.loads('{"id": "7"}')
print(isinstance(body["id"], int), type(body["id"]).__name__)
```

- Число в кавычках — это строка. Вывод: `False str`.

## int или float

```python
import json
body = json.loads('{"price": 10}')
print(isinstance(body["price"], float), isinstance(body["price"], (int, float)))
```

- `10` в JSON становится `int`. Если по смыслу поле — «любое число», проверяй кортежем типов `(int, float)`.
- Вывод: `False True`.

## Ловушка: true — это тоже int

```python
import json
body = json.loads('{"id": true}')
print(isinstance(body["id"], int), isinstance(body["id"], bool))
```

- `bool` — подтип `int`, поэтому `true` пройдёт проверку `isinstance(x, int)`. Для полей-чисел исключай `bool` явно.
- Вывод: `True True`.

## Отсутствует или null

```python
import json
body = json.loads('{"a": null}')
print("a" in body, "b" in body, body.get("a"), body.get("b"))
```

- `"a" in body` — поле **есть** (со значением `null`); `"b"` — нет вовсе. Через `get` оба дают `None` — не путай эти случаи в проверках.
- Вывод: `True False None None`.

## Сбор всех ошибок

```python
import json

def validate_user(text):
    u = json.loads(text)
    errors = []
    uid = u.get("id")
    if not (isinstance(uid, int) and not isinstance(uid, bool) and uid > 0):
        errors.append("bad id")
    if not (isinstance(u.get("email"), str) and "@" in u["email"]):
        errors.append("bad email")
    return errors

print(validate_user('{"id": 1, "email": "a@x"}'), validate_user('{"id": "1"}'))
```

- Каждая проверка добавляет свою ошибку — отчёт сразу показывает все проблемы.
- Вывод: `[] ['bad id', 'bad email']`.

## Итог

- Обязательные поля — `поле in body`; типы — `isinstance(body[поле], тип)`.
- Число в кавычках — строка; `10` → `int`; «любое число» — `(int, float)`.
- `true` проходит `isinstance(x, int)` — исключай `bool`.
- «Нет поля» и «поле = null» — разные случаи.
- Собирай все ошибки в список.
'''),
    short=t(r'''
```py
[f for f in required if f not in body]            # нет полей
isinstance(body["id"], int)                       # тип
isinstance(x, (int, float))                       # любое число
isinstance(x, int) and not isinstance(x, bool)    # true — не id!
"a" in body    # поле есть (может быть null)
```
'''),
    quiz=[
        q('Что вернёт `isinstance(json.loads("true"), int)`?',
            ['`False`', '`True`', 'Ошибка', '`None`'],
            1, 'bool — подтип int.'),
        q('Какой тип у значения из `{"id": "7"}`?',
            ['int', 'str', 'float', 'None'],
            1, 'Кавычки — строка.'),
        q('Чем `"a" in body` отличается от `body.get("a") is not None`?',
            ['Ничем', 'in проверяет наличие ключа, даже со значением null', 'get быстрее', 'in проверяет значение'],
            1, 'null — это присутствующее поле.'),
    ],
),

# ---------- jsn-m3-l2 ----------
'jsn-m3-l2': dict(
    full=t(r'''
## Зачем это нужно

Главная проверка API-теста — «фактический ответ совпадает с ожидаемым». Сравнивать JSON-**строки** нельзя: у одинаковых данных может быть разный порядок ключей и разные пробелы. Сравнивают **разобранные** объекты — и учитывают тонкости Python.

## Строки против объектов

```python
import json
a = json.loads('{"x": 1, "y": 2}')
b = json.loads('{"y": 2, "x": 1}')
print(a == b, json.dumps(a) == json.dumps(b), json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True))
```

- Словари равны без учёта порядка ключей.
- Строки `dumps` различаются — порядок сохранился. С `sort_keys=True` строки совпадают.
- Вывод: `True False True`.

## Порядок в массивах важен

```python
import json
print(json.loads("[1, 2]") == json.loads("[2, 1]"))
print(json.loads("1") == json.loads("1.0"), json.loads("true") == json.loads("1"))
```

- Списки сравниваются поэлементно по порядку.
- В Python `1 == 1.0` и `True == 1` — поэтому обычное сравнение не заметит, что API вернул `true` вместо `1`.
- Вывод: `False`, `True True`.

## Строгое сравнение через канонический JSON

```python
import json

def strict_equal(a, b):
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)

print(strict_equal({"ok": True}, {"ok": 1}), strict_equal({"a": 1, "b": 2}, {"b": 2, "a": 1}))
```

- В JSON-тексте `true` и `1` пишутся по-разному, поэтому сравнение канонических строк их различает. Вывод: `False True`.

## Игнорировать изменчивые поля

```python
import json
expected = {"id": 1, "status": "ok"}
actual = json.loads('{"id": 1, "status": "ok", "ts": 1712}')
actual.pop("ts", None)
print(actual == expected)
```

- Время, id запроса, токены меняются от прогона к прогону — их убирают перед сравнением. Вывод: `True`.

## Массивы без учёта порядка

```python
import json

def same_items(a, b):
    def canon(text):
        return sorted(json.dumps(obj, sort_keys=True) for obj in json.loads(text))
    return canon(a) == canon(b)

print(same_items('[{"id": 1}, {"id": 2}]', '[{"id": 2}, {"id": 1}]'))
```

- Словари нельзя сортировать напрямую, но их канонические строки — можно. Одинаковые наборы дадут одинаковые отсортированные списки строк.
- Вывод: `True`.

## Различия в полях

```python
import json
a = json.loads('{"id": 1, "x": 2}')
b = json.loads('{"id": 1, "y": 3}')
print(sorted(a.keys() - b.keys()), sorted(b.keys() - a.keys()))
```

Вывод: `['x'] ['y']` — такой список удобно выводить в сообщении упавшего теста.

## Итог

- Сравнивай разобранные объекты, а не JSON-строки.
- Порядок ключей не важен, порядок элементов массива — важен.
- `True == 1`, `1 == 1.0` в Python; строго — канонический `dumps(sort_keys=True)`.
- Изменчивые поля удаляй перед сравнением.
- Массив без учёта порядка — сравнение отсортированных канонических строк.
'''),
    short=t(r'''
```py
json.loads(a) == json.loads(b)          # по содержимому
[1, 2] != [2, 1]                        # порядок в массивах важен
True == 1                               # осторожно!
json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)   # строго
actual.pop("ts", None)                  # убрать изменчивое
sorted(json.dumps(o, sort_keys=True) for o in items)             # без порядка
```
'''),
    quiz=[
        q('Равны ли `json.loads(\'{"a":1,"b":2}\')` и `json.loads(\'{"b":2,"a":1}\')`?',
            ['Да', 'Нет', 'Ошибка', 'Зависит от пробелов'],
            0, 'Словари сравниваются без порядка.'),
        q('Что вернёт `json.loads("[1, 2]") == json.loads("[2, 1]")`?',
            ['`True`', '`False`', 'Ошибка', '`None`'],
            1, 'Порядок элементов важен.'),
        q('Как отличить `true` от `1` при сравнении?',
            ['Через ==', 'Сравнить канонические JSON-строки', 'Нельзя', 'Через is'],
            1, 'В тексте JSON они разные.'),
    ],
),

# ---------- jsn-m3-l3 ----------
'jsn-m3-l3': dict(
    full=t(r'''
## Зачем это нужно

Сервер не всегда возвращает корректный JSON: при ошибке прокси придёт HTML-страница, при таймауте — пустое тело, при баге — обрезанный текст. Тест должен не падать с непонятной трассой, а сообщать: «тело ответа — не JSON». Для этого ошибки разбора перехватывают.

## Что не является JSON

```python
import json
for text in ['{"a": 1}', "{'a': 1}", '{"a": 1,}', "", "null"]:
    try:
        print(repr(json.loads(text)))
    except json.JSONDecodeError:
        print("не JSON:", repr(text))
```

- Одинарные кавычки, запятая в конце, пустая строка — ошибки.
- `"null"` — корректный JSON, результат `None`.
- `repr(...)` показывает значение с кавычками — видно, где пустая строка.
- Вывод: `{'a': 1}`, три строки «не JSON», `None`.

## Где именно ошибка

```python
import json
try:
    json.loads('{"a": 1,\n "b": }')
except json.JSONDecodeError as e:
    print(e.lineno, e.colno, e.msg)
```

- `lineno` — номер строки, `colno` — номер символа в строке (с 1), `msg` — описание, `pos` — позиция от начала текста.
- Вывод: `2 7 Expecting value` — на второй строке, 7-м символе ожидалось значение.

## JSONDecodeError — это ValueError

```python
import json
print(issubclass(json.JSONDecodeError, ValueError))
try:
    json.loads("abc")
except ValueError:
    print("поймали как ValueError")
```

- `issubclass(A, B)` — является ли класс `A` разновидностью `B`. Поэтому `except ValueError` тоже ловит ошибки разбора.
- Вывод: `True`, `поймали как ValueError`.

## Безопасный разбор тела

```python
import json

def parse_body(text):
    if not text.strip():
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "invalid json"}

print(parse_body("  "), parse_body('{"a": 1}'), parse_body("<html>"))
```

- Пустое тело — отдельный понятный случай; некорректный JSON — маркер ошибки вместо падения.
- Вывод: `{} {'a': 1} {'error': 'invalid json'}`.

## Проверка корневого типа

```python
import json

def parse_object(text):
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("ожидали объект")
    return data

try:
    parse_object("[1, 2]")
except ValueError as e:
    print(e)
```

- Корректный JSON может оказаться массивом или числом там, где ждали объект. `raise ValueError(...)` — выбросить свою понятную ошибку (тема «Исключения»).
- Вывод: `ожидали объект`.

## Итог

- Некорректный текст → `json.JSONDecodeError` (подтип `ValueError`).
- `e.lineno`, `e.colno`, `e.msg` — где и что не так.
- Пустое тело, HTML, обрезанный текст — обрабатывай явно.
- Проверяй тип корня: `isinstance(data, dict)`.
'''),
    short=t(r'''
```py
try:
    data = json.loads(text)
except json.JSONDecodeError as e:
    e.lineno, e.colno, e.msg     # где и что
if not text.strip(): ...         # пустое тело
issubclass(json.JSONDecodeError, ValueError)   # True
if not isinstance(data, dict):
    raise ValueError("ожидали объект")
```
'''),
    quiz=[
        q('Какую ошибку вызовет `json.loads("")`?',
            ['KeyError', '`json.JSONDecodeError`', 'TypeError', 'Никакую'],
            1, 'Пустая строка — не JSON.'),
        q('Поймает ли `except ValueError` ошибку разбора JSON?',
            ['Нет', 'Да — JSONDecodeError наследует ValueError', 'Только в Python 2', 'Только для пустой строки'],
            1, 'issubclass(...) — True.'),
        q('Что вернёт `json.loads("null")`?',
            ['Ошибка', '`None`', '`"null"`', '`{}`'],
            1, 'null — корректный JSON.'),
    ],
),

# ---------- jsn-m3-l4 ----------
'jsn-m3-l4': dict(
    full=t(r'''
## Зачем это нужно

Результаты прогона тестов принято сохранять в JSON: его читают CI-системы, дашборды, скрипты уведомлений. Соберём всё изученное в одну задачу: построить отчёт, превратить в JSON, прочитать и проанализировать.

## Построить отчёт

```python
import json
results = [("login", "pass", 1.2), ("pay", "fail", 3.4)]
report = {"total": len(results), "tests": [{"name": n, "status": s, "time": t} for n, s, t in results]}
print(json.dumps(report, ensure_ascii=False))
```

- Сначала словарь Python, потом `dumps`. Кортежи результатов распаковываются в поля объектов.
- Вывод: `{"total": 2, "tests": [{"name": "login", "status": "pass", "time": 1.2}, {"name": "pay", "status": "fail", "time": 3.4}]}`.

Полный отчёт со счётчиками:

```python
results = [("a", "pass", 1.0), ("b", "fail", 2.0)]
tests = [{"name": n, "status": s, "time": t} for n, s, t in results]
report = {
    "total": len(tests),
    "passed": sum(1 for t in tests if t["status"] == "pass"),
    "failed": sum(1 for t in tests if t["status"] == "fail"),
}
print(report)
```

Вывод: `{'total': 2, 'passed': 1, 'failed': 1}`.

## Прочитать отчёт

```python
import json
text = '{"tests": [{"name": "a", "status": "pass"}, {"name": "b", "status": "fail"}]}'
report = json.loads(text)
failed = [t["name"] for t in report["tests"] if t["status"] == "fail"]
print(failed, len(report["tests"]) - len(failed))
```

Вывод: `['b'] 1`.

```python
import json
text = '{"tests": [{"name": "a", "time": 1.2}, {"name": "b", "time": 3.4}]}'
tests = json.loads(text)["tests"]
print(max(tests, key=lambda t: t["time"])["name"] if tests else None)
```

Вывод: `b`.

## Процент успешных

```python
import json
summary = {"passed": 2, "failed": 1}
summary["rate"] = round(summary["passed"] / (summary["passed"] + summary["failed"]) * 100, 1)
print(json.dumps(summary, sort_keys=True))
```

- `sort_keys=True` делает отчёт стабильным: одинаковые данные — одинаковый текст (удобно хранить в git и сравнивать).
- Вывод: `{"failed": 1, "passed": 2, "rate": 66.7}`.

## Сложить несколько прогонов

```python
import json
texts = ['{"passed": 2, "failed": 1}', '{"passed": 5, "failed": 0}']
total = {"passed": 0, "failed": 0}
for text in texts:
    r = json.loads(text)
    total["passed"] += r["passed"]
    total["failed"] += r["failed"]
print(total)
```

Вывод: `{'passed': 7, 'failed': 1}`.

## Итог

- Отчёт собирают словарём и сохраняют через `dumps`/`dump`.
- Счётчики — `sum(1 for t in tests if ...)`.
- Читают через `loads` и обрабатывают как список словарей.
- `sort_keys=True` — стабильный текст отчёта.
- Несколько отчётов — разобрать и сложить.
'''),
    short=t(r'''
```py
report = {"total": len(tests), "tests": tests}
json.dumps(report, ensure_ascii=False, sort_keys=True)
sum(1 for t in tests if t["status"] == "fail")
[t["name"] for t in json.loads(text)["tests"] if t["status"] == "fail"]
max(tests, key=lambda t: t["time"])["name"]
```
'''),
    quiz=[
        q('Зачем в отчёте `sort_keys=True`?',
            ['Быстрее', 'Стабильный текст: одинаковые данные — одинаковый JSON', 'Меньше размер', 'Так требует CI'],
            1, 'Удобно сравнивать и хранить.'),
        q('Как посчитать упавшие тесты в списке `tests`?',
            ['`len(tests)`', '`sum(1 for t in tests if t["status"] == "fail")`', '`tests.count("fail")`', '`max(tests)`'],
            1, 'Генератор с условием.'),
        q('В каком порядке строят JSON-отчёт?',
            ['Сразу строкой', 'Словарь Python, затем dumps', 'dumps, затем словарь', 'Через loads'],
            1, 'Строку собирать вручную — источник ошибок.'),
    ],
),
}
