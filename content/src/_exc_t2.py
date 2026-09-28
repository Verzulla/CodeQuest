"""Теория модуля «Выбрасывание исключений» темы «Исключения».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- exc-m2-l1 ----------
'exc-m2-l1': dict(
    full=t(r'''
## Зачем это нужно

Исключения выбрасывает не только Python — их выбрасывают и твои функции, когда получают неправильные данные. `raise` — это способ сказать «так нельзя, дальше не продолжаю» и объяснить почему. Лучше громко упасть с понятным сообщением, чем молча вернуть неправильный результат.

## raise

```python
def set_age(age):
    if age < 0:
        raise ValueError(f"возраст не может быть отрицательным: {age}")
    return age

print(set_age(30))
try:
    set_age(-5)
except ValueError as e:
    print("ошибка:", e)
```

- `raise КлассОшибки("сообщение")` — создать исключение и выбросить его.
- Функция прерывается на `raise`, как на `return`, но вместо значения наружу летит исключение.
- Вывод: `30`, `ошибка: возраст не может быть отрицательным: -5`.

## Какой тип выбрать

```python
def check(value):
    if not isinstance(value, int):
        raise TypeError("нужно целое число")
    if value <= 0:
        raise ValueError("нужно положительное")
    return "ok"

for v in [5, "5", -1]:
    try:
        print(check(v))
    except (TypeError, ValueError) as e:
        print(type(e).__name__, "-", e)
```

- `TypeError` — неверный **тип** аргумента.
- `ValueError` — тип правильный, **значение** неверное.
- `KeyError` — нет нужного ключа; `RuntimeError` — общая ошибка выполнения, когда другие не подходят.
- Вывод: `ok`, `TypeError - нужно целое число`, `ValueError - нужно положительное`.

## args исключения

```python
def f():
    print("начало")
    raise RuntimeError("стоп")
    print("не выполнится")

try:
    f()
except RuntimeError as e:
    print(e.args)
```

- `e.args` — кортеж аргументов, переданных при создании. `str(e)` — обычно первый аргумент.
- Вывод: `начало`, `('стоп',)`.

## Валидация и «raise_for_status»

```python
def check_status(response):
    if response["status"] >= 400:
        raise RuntimeError(f"HTTP {response['status']}")
    return response

try:
    check_status({"status": 404})
except RuntimeError as e:
    print(e)
```

- Так работают HTTP-клиенты (`response.raise_for_status()`): код ошибки превращается в исключение, и тест не может его «не заметить».
- Вывод: `HTTP 404`.

## Хорошее сообщение

- Что не так и какое значение пришло: `"порт вне диапазона: 70000"`, а не `"ошибка"`.
- Проверяй в начале функции («охранные» проверки), как с ранним `return`.

## Итог

- `raise ValueError("текст")` — выбросить исключение; функция прерывается.
- `TypeError` — неверный тип; `ValueError` — неверное значение; `KeyError` — нет ключа; `RuntimeError` — прочее.
- `e.args` — аргументы исключения, `str(e)` — текст.
- Сообщение должно объяснять, что не так, со значением.
'''),
    short=t(r'''
```py
if age < 0:
    raise ValueError(f"возраст < 0: {age}")   # функция прерывается
raise TypeError("нужно целое число")   # неверный тип
raise KeyError(key)                    # нет ключа
raise RuntimeError(f"HTTP {status}")   # прочее
e.args; str(e)
```
'''),
    quiz=[
        q('Какой тип исключения подходит, если передали строку вместо числа?',
            ['ValueError', 'TypeError', 'KeyError', 'IndexError'],
            1, 'Неверный тип.'),
        q('Что происходит после `raise` в функции?',
            ['Следующая строка', 'Функция прерывается, исключение летит наружу', 'Функция возвращает None', 'Программа всегда завершается'],
            1, 'Как return, но с ошибкой.'),
        q('Что вернёт `ValueError("a", 1).args`?',
            ['`"a"`', '`("a", 1)`', '`["a", 1]`', 'Ошибка'],
            1, 'Кортеж аргументов.'),
    ],
),

# ---------- exc-m2-l2 ----------
'exc-m2-l2': dict(
    full=t(r'''
## Зачем это нужно

Встроенных исключений не хватает, чтобы выразить смысл ошибок **твоей** программы: «пользователь не найден», «нет доступа», «валидация не прошла». Свои исключения делают код понятнее и позволяют ловить именно ошибки приложения, не смешивая их с системными.

## Своё исключение

```python
class ValidationError(Exception):
    pass

try:
    raise ValidationError("email без @")
except ValidationError as e:
    print(type(e).__name__, "-", e)
print(issubclass(ValidationError, Exception))
```

- `class Имя(Exception): pass` — новый класс исключения, **наследник** `Exception` (подробно классы — в теме «Классы»; сейчас достаточно этого шаблона).
- `pass` — тело пустое: всё поведение (сообщение, `args`) достаётся от `Exception`.
- Имена принято заканчивать на `Error`.
- Вывод: `ValidationError - email без @`, `True`.

## Иерархия своих ошибок

```python
class AppError(Exception):
    pass

class NotFound(AppError):
    pass

class Forbidden(AppError):
    pass

for err in [NotFound("нет пользователя"), Forbidden("нет доступа")]:
    try:
        raise err
    except AppError as e:
        print(type(e).__name__, e)
```

- Общий базовый класс приложения (`AppError`) и частные потомки.
- `except AppError` ловит все ошибки приложения, а конкретные можно ловить по отдельности.
- Вывод: `NotFound нет пользователя`, `Forbidden нет доступа`.

## Исключение с данными

```python
class HttpError(Exception):
    def __init__(self, status, message):
        super().__init__(f"{status}: {message}")
        self.status = status

try:
    raise HttpError(503, "сервис недоступен")
except HttpError as e:
    print(e.status, str(e))
```

- `__init__` — метод, который выполняется при создании объекта (тема «Классы»).
- `super().__init__(...)` — передать текст сообщения базовому `Exception`.
- `self.status = status` — сохранить дополнительное поле, чтобы обработчик мог принять решение по коду, а не разбирать текст.
- Вывод: `503 503: сервис недоступен`.

## Собрать все ошибки в одно исключение

```python
class ValidationError(Exception):
    def __init__(self, errors):
        super().__init__("; ".join(errors))
        self.errors = errors

try:
    raise ValidationError(["name пустое", "age отрицательный"])
except ValidationError as e:
    print(e.errors, "|", e)
```

- Удобно для форм и API: пользователь сразу видит все проблемы.
- Вывод: `['name пустое', 'age отрицательный'] | name пустое; age отрицательный`.

## Итог

- `class MyError(Exception): pass` — своё исключение.
- Общий базовый класс приложения + частные наследники.
- `except База` ловит всех потомков.
- Дополнительные поля — через `__init__` с `super().__init__(текст)`.
'''),
    short=t(r'''
```py
class AppError(Exception): pass
class NotFound(AppError): pass       # иерархия
raise NotFound("нет пользователя")
except AppError as e: ...            # ловит всех потомков

class HttpError(Exception):
    def __init__(self, status, msg):
        super().__init__(f"{status}: {msg}")
        self.status = status         # доп. поле
```
'''),
    quiz=[
        q('От какого класса наследуют свои исключения?',
            ['object', '`Exception`', 'BaseException всегда', 'ValueError всегда'],
            1, 'Exception — база обычных ошибок.'),
        q('Поймает ли `except AppError` исключение `NotFound(AppError)`?',
            ['Нет', 'Да', 'Только с as', 'Только в тестах'],
            1, 'Потомок ловится базовым классом.'),
        q('Зачем своё поле `status` в исключении?',
            ['Для красоты', 'Чтобы обработчик мог решать по коду, не разбирая текст', 'Так требует Python', 'Не нужно'],
            1, 'Данные удобнее текста.'),
    ],
),

# ---------- exc-m2-l3 ----------
'exc-m2-l3': dict(
    full=t(r'''
## Зачем это нужно

Иногда ошибку нужно **заметить, но не проглотить**: записать в лог и передать дальше. А иногда — превратить низкоуровневую ошибку (`KeyError` в конфиге) в понятную ошибку приложения (`ConfigError`), не потеряв исходную причину. Для этого есть повторный выброс и цепочки исключений.

## raise без аргументов

```python
log = []

def process():
    try:
        1 / 0
    except ZeroDivisionError:
        log.append("записали в лог")
        raise

try:
    process()
except ZeroDivisionError:
    print("снаружи тоже поймали", log)
```

- `raise` без аргументов внутри `except` выбрасывает **то же самое** исключение дальше, с исходной трассировкой.
- Вывод: `снаружи тоже поймали ['записали в лог']`.

## raise ... from — явная причина

```python
class ConfigError(Exception):
    pass

def load(cfg):
    try:
        return int(cfg["port"])
    except (KeyError, ValueError) as e:
        raise ConfigError("плохой конфиг") from e

try:
    load({"port": "x"})
except ConfigError as e:
    print(e, "| причина:", type(e.__cause__).__name__)
```

- `raise Новая(...) from e` — новая ошибка «с причиной». Причина сохраняется в `__cause__`.
- В трассировке Python покажет обе: исходную и новую («The above exception was the direct cause…»).
- Вывод: `плохой конфиг | причина: ValueError`.

## Неявная цепочка

```python
try:
    try:
        {}["x"]
    except KeyError:
        raise ValueError("не нашли")
except ValueError as e:
    print(e, "|", type(e.__context__).__name__, e.__cause__)
```

- Если выбросить новое исключение внутри `except` без `from`, Python сам запомнит исходное в `__context__` («During handling of the above exception, another exception occurred»).
- `__cause__` при этом `None`. Вывод: `не нашли | KeyError None`.

## from None — скрыть причину

```python
def wrap(func):
    try:
        return func()
    except Exception:
        raise RuntimeError("сбой") from None

try:
    wrap(lambda: {}["x"])
except RuntimeError as e:
    print(e, e.__cause__, e.__suppress_context__)
```

- `from None` — не показывать исходную ошибку (когда она лишь запутает пользователя).
- Вывод: `сбой None True`.

## Найти первопричину

```python
def root_cause(exc):
    while True:
        nxt = exc.__cause__ or exc.__context__
        if nxt is None:
            return type(exc).__name__
        exc = nxt

try:
    try:
        {}["x"]
    except KeyError as e:
        raise ValueError("v") from e
except ValueError as e:
    print(root_cause(e))
```

Вывод: `KeyError`.

## Итог

- `raise` в `except` — выбросить ту же ошибку дальше (залогировать и не проглотить).
- `raise Новая(...) from e` — новая ошибка с причиной в `__cause__`.
- Без `from` исходная ошибка попадает в `__context__`.
- `from None` — скрыть причину.
'''),
    short=t(r'''
```py
except ZeroDivisionError:
    log.append("...")
    raise                                # то же исключение дальше
except KeyError as e:
    raise ConfigError("плохой конфиг") from e   # e -> __cause__
raise RuntimeError("сбой") from None     # скрыть причину
e.__cause__; e.__context__
```
'''),
    quiz=[
        q('Что делает `raise` без аргументов внутри except?',
            ['Ошибка синтаксиса', 'Выбрасывает то же исключение дальше', 'Создаёт RuntimeError', 'Ничего'],
            1, 'Повторный выброс.'),
        q('Где хранится причина при `raise B() from a`?',
            ['`B.args`', '`B.__cause__`', '`B.__context__`', 'Нигде'],
            1, 'Явная причина — __cause__.'),
        q('Что делает `raise X from None`?',
            ['Ничего не выбрасывает', 'Скрывает исходную ошибку в трассировке', 'Выбрасывает None', 'Ошибка'],
            1, '__suppress_context__ = True.'),
    ],
),

# ---------- exc-m2-l4 ----------
'exc-m2-l4': dict(
    full=t(r'''
## Зачем это нужно

`assert` — проверка «это обязано быть правдой». Если нет — `AssertionError`. На `assert` построены автотесты (pytest), и им же программисты проверяют свои допущения в коде. Но у `assert` есть особенности: его можно отключить и легко написать с ошибкой.

## assert

```python
def average(nums):
    assert len(nums) > 0, "список пуст"
    return sum(nums) / len(nums)

print(average([2, 4]))
try:
    average([])
except AssertionError as e:
    print("AssertionError:", e)
```

- `assert условие, "сообщение"` — если условие ложно, выбрасывается `AssertionError` с сообщением.
- Эквивалент: `if not условие: raise AssertionError("сообщение")`.
- Вывод: `3.0`, `AssertionError: список пуст`.

## Ловушка со скобками

```python
try:
    assert (1 == 2, "никогда не сработает")
    print("assert прошёл!")
except AssertionError:
    print("упал")
```

- Скобки превратили условие и сообщение в **кортеж** из двух элементов — непустой кортеж всегда истинен, проверка никогда не падает. Python даже предупреждает об этом (SyntaxWarning).
- `assert` — не функция: скобки вокруг «аргументов» не ставят.
- Вывод: `assert прошёл!`.

## AssertionError — обычное исключение

```python
print(issubclass(AssertionError, Exception))
results = []
for x in [1, -1]:
    try:
        assert x > 0, f"{x} не положительное"
        results.append("ok")
    except AssertionError as e:
        results.append(str(e))
print(results)
```

- Его можно перехватить — так тестовые фреймворки собирают упавшие проверки, не останавливая весь прогон.
- Вывод: `True`, `['ok', '-1 не положительное']`.

## assert или raise

- `assert` — для проверок **допущений программиста** и в **тестах**: «сюда никогда не должен прийти пустой список».
- `raise ValueError(...)` — для проверки **внешних данных**: ввод пользователя, ответ API, аргументы публичной функции.
- Причина: при запуске `python -O` (оптимизация) все `assert` **отключаются**, и проверка данных исчезла бы.

```python
def set_quantity(q):
    if q <= 0:
        raise ValueError("количество должно быть положительным")
    return q

print(set_quantity(3))
```

Вывод: `3`.

## Проверка «должно упасть»

```python
def assert_raises(exc_type, func):
    try:
        func()
    except exc_type as e:
        return e
    raise AssertionError(f"ожидали {exc_type.__name__}")

print(type(assert_raises(ZeroDivisionError, lambda: 1 / 0)).__name__)
```

- Так устроен `pytest.raises`: тест проходит, только если исключение **было**. Вывод: `ZeroDivisionError`.

## Итог

- `assert условие, "сообщение"` → `AssertionError`, если условие ложно.
- Без скобок! `assert (x, "msg")` всегда проходит.
- `assert` — для тестов и допущений; для внешних данных — `raise ValueError`.
- `python -O` отключает все `assert`.
'''),
    short=t(r'''
```py
assert len(nums) > 0, "список пуст"   # AssertionError, если ложно
assert (x > 0, "msg")                 # ВСЕГДА проходит — кортеж!
except AssertionError as e: ...
if q <= 0:
    raise ValueError("...")           # внешние данные — raise, не assert
# python -O отключает assert
```
'''),
    quiz=[
        q('Почему `assert (1 == 2, "msg")` не падает?',
            ['Из-за сообщения', 'Проверяется непустой кортеж — он истинен', 'assert отключён', 'Падает'],
            1, 'assert — не функция.'),
        q('Что происходит с assert при запуске `python -O`?',
            ['Ничего', 'Все assert отключаются', 'Они становятся raise', 'Ошибка'],
            1, 'Поэтому не проверяй ими данные.'),
        q('Чем проверять ввод пользователя?',
            ['assert', '`raise ValueError(...)`', 'print', 'Никак'],
            1, 'assert можно отключить.'),
    ],
),
}
