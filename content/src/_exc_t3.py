"""Теория модуля «Исключения на практике» темы «Исключения».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- exc-m3-l1 ----------
'exc-m3-l1': dict(
    full=t(r'''
## Зачем это нужно

Есть два стиля борьбы с ошибками. **LBYL** («Look Before You Leap» — посмотри, прежде чем прыгать): сначала проверить, потом делать. **EAFP** («Easier to Ask Forgiveness than Permission» — проще попросить прощения): сразу делать и перехватить ошибку. В Python принят EAFP — он короче и часто надёжнее. Но у обоих стилей есть своё место.

## Два стиля

```python
data = {"a": 1}
if "b" in data:
    print(data["b"])
else:
    print("нет b (LBYL)")
try:
    print(data["b"])
except KeyError:
    print("нет b (EAFP)")
```

- LBYL проверяет условие заранее; EAFP пробует и ловит конкретное исключение.
- Вывод: `нет b (LBYL)`, `нет b (EAFP)`.

## Проверка не всё предусматривает

```python
for text in ["12", "-3", "4.5", " 7"]:
    print(repr(text), text.isdigit(), end=" | ")
    try:
        print(int(text))
    except ValueError:
        print("ValueError")
```

- `isdigit()` отвергает `"-3"` и `" 7"`, хотя `int` их понимает. Предварительная проверка часто оказывается строже или мягче самой операции.
- EAFP спрашивает саму операцию — ей виднее, получится ли.
- Вывод: четыре строки: `'12' True | 12`, `'-3' False | -3`, `'4.5' False | ValueError`, `' 7' False | 7`.

## EAFP для вложенных данных

```python
def nested_get(data, *keys, default=None):
    try:
        for key in keys:
            data = data[key]
        return data
    except (KeyError, TypeError):
        return default

d = {"a": {"b": 1}, "x": 5}
print(nested_get(d, "a", "b"), nested_get(d, "x", "y", default=0))
```

- Вместо проверок на каждом уровне — один `try`. `5["y"]` даёт `TypeError` — тоже ловим.
- Вывод: `1 0`.

## Когда LBYL лучше

```python
config = {"timeout": "30"}
print(config.get("retries", 3))
```

- Для словаря есть `get` — готовый LBYL без лишнего кода.
- LBYL разумен, когда ошибка — **частая** ситуация (дешевле проверить), когда операция имеет побочные эффекты (нельзя «попробовать» списание денег) или когда проверка простая и понятная.
- Вывод: `3`.

## Итог

- LBYL: `if проверка: действие`. EAFP: `try: действие except Тип:`.
- В Python принят EAFP: операция сама лучше знает, получится ли.
- Лови конкретные исключения, а не все подряд.
- LBYL — для частых ситуаций, операций с побочными эффектами и готовых методов (`get`).
'''),
    short=t(r'''
```py
# LBYL
if key in d:
    value = d[key]
# EAFP (принято в Python)
try:
    value = int(d[key])
except (KeyError, ValueError):
    value = default
d.get(key, default)      # готовый безопасный вариант
```
'''),
    quiz=[
        q('Что такое EAFP?',
            ['Проверить, потом делать', 'Сделать и перехватить ошибку', 'Никогда не ловить ошибки', 'Всегда assert'],
            1, 'Easier to Ask Forgiveness than Permission.'),
        q('Вернёт ли `"-3".isdigit()` True?',
            ['Да', 'Нет', 'Ошибка', 'None'],
            1, 'Минус — не цифра, хотя int("-3") работает.'),
        q('Когда уместен LBYL?',
            ['Никогда', 'Когда операция с побочными эффектами или ошибка частая', 'Всегда', 'Только в тестах'],
            1, 'Нельзя «попробовать» списание денег.'),
    ],
),

# ---------- exc-m3-l2 ----------
'exc-m3-l2': dict(
    full=t(r'''
## Зачем это нужно

При обработке больших данных одна плохая запись не должна останавливать всю работу. Нужно уметь: **пропустить** плохой элемент, **собрать** ошибки в отчёт, **повторить** операцию при временном сбое и **остановиться** при критической проблеме.

## Пропустить и посчитать

```python
total = 0
errors = 0
for raw in ["10", "x", "5", "", "7"]:
    try:
        total += int(raw)
    except ValueError:
        errors += 1
        continue
print(total, errors)
```

- `try` внутри цикла: ошибка одного элемента не прерывает цикл. `continue` — к следующему.
- Вывод: `22 2`.

## Собрать ошибки

```python
rows = ["1,2", "3", "a,4"]
good, bad = [], []
for i, row in enumerate(rows):
    try:
        a, b = row.split(",")
        good.append(int(a) + int(b))
    except ValueError:
        bad.append(i)
print(good, bad)
```

- Распаковка неверного числа частей (`a, b = ["3"]`) — тоже `ValueError`.
- Номера плохих строк — готовый отчёт для пользователя или лога.
- Вывод: `[3] [1, 2]`.

## Повторить при временном сбое

```python
answers = iter([ConnectionError("нет"), ConnectionError("нет"), "ok"])

def request():
    value = next(answers)
    if isinstance(value, Exception):
        raise value
    return value

for attempt in range(1, 5):
    try:
        print(attempt, request())
        break
    except ConnectionError as e:
        print(attempt, "ошибка:", e)
```

- `iter(...)` и `next(...)` выдают заготовленные ответы по одному (тема «sorted, filter и map»).
- Временные ошибки (сеть, 503) повторяют с лимитом попыток; `break` — выход при успехе.
- Вывод: `1 ошибка: нет`, `2 ошибка: нет`, `3 ok`.

Если все попытки неудачны, обычно выбрасывают последнюю ошибку дальше:

```python
def retry(func, attempts):
    for attempt in range(attempts):
        try:
            return func()
        except ConnectionError:
            if attempt == attempts - 1:
                raise

try:
    retry(lambda: 1 / 0, 3)
except ZeroDivisionError:
    print("не ConnectionError — вылетело сразу")
```

- Ловим только то, что имеет смысл повторять. Вывод: `не ConnectionError — вылетело сразу`.

## Разные реакции на разные ошибки

```python
def run_all(tests):
    results = {}
    for name, test in tests.items():
        try:
            test()
            results[name] = "pass"
        except AssertionError:
            results[name] = "fail"
        except Exception:
            results[name] = "error"
    return results

def bad():
    assert False

print(run_all({"ok": lambda: None, "bad": bad, "broken": lambda: 1 / 0}))
```

- Так тестовые фреймворки различают **упавший** тест (проверка не прошла) и **сломанный** (ошибка в самом тесте или коде).
- Вывод: `{'ok': 'pass', 'bad': 'fail', 'broken': 'error'}`.

## Итог

- `try` внутри цикла — ошибка одного элемента не останавливает остальные.
- Собирай плохие элементы в список для отчёта.
- Временные сбои — повтор с лимитом; в конце — `raise` последней ошибки.
- Критическая ошибка — остановиться (`raise`) с понятным сообщением.
- `AssertionError` — «fail», прочие исключения — «error».
'''),
    short=t(r'''
```py
for raw in rows:
    try:
        total += int(raw)
    except ValueError:
        bad.append(raw)          # собрать и продолжить
        continue
for attempt in range(n):         # повтор
    try:
        return func()
    except ConnectionError:
        if attempt == n - 1:
            raise
```
'''),
    quiz=[
        q('Где ставить try, чтобы одна ошибка не остановила обработку списка?',
            ['Вокруг всего цикла', 'Внутри цикла, вокруг обработки элемента', 'Не нужен', 'После цикла'],
            1, 'Тогда цикл продолжится.'),
        q('Какие ошибки стоит повторять?',
            ['Любые', 'Временные: сеть, 503', 'SyntaxError', 'AssertionError'],
            1, 'Логические ошибки от повтора не исчезнут.'),
        q('Чем «fail» отличается от «error» в отчёте тестов?',
            ['Ничем', 'fail — не прошла проверка, error — упал сам код/тест', 'error — мягче', 'fail — ошибка синтаксиса'],
            1, 'AssertionError против других исключений.'),
    ],
),

# ---------- exc-m3-l3 ----------
'exc-m3-l3': dict(
    full=t(r'''
## Зачем это нужно

Хороший тест проверяет не только «правильный вход → правильный результат», но и «неправильный вход → правильная ошибка». Функция, которая должна отвергнуть отрицательную сумму, но молча её принимает, — это баг. Разберём, как проверять исключения в тестах и не наделать типичных ошибок.

## Проверка «ошибка должна быть»

```python
def check_raises(exc_type, func):
    try:
        func()
    except exc_type:
        return "ok: ошибка есть"
    return "плохо: ошибки нет"

print(check_raises(ValueError, lambda: int("x")))
print(check_raises(ValueError, lambda: int("5")))
```

- Если исключение было — проверка пройдена; если нет — провал.
- В pytest то же делают так: `with pytest.raises(ValueError): int("x")`.
- Вывод: `ok: ошибка есть`, `плохо: ошибки нет`.

## Проверка текста ошибки

```python
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError(f"недостаточно средств: {balance} < {amount}")
    return balance - amount

try:
    withdraw(100, 500)
except ValueError as e:
    print("недостаточно" in str(e), e.args[0])
```

- Тип ошибки — это хорошо, но ещё лучше проверить **сообщение**: иначе тест пропустит ошибку «не по той причине».
- Вывод: `True недостаточно средств: 100 < 500`.

## Тест не должен ловить слишком много

```python
def buggy():
    return [][0]

def test_bad():
    try:
        buggy()
    except Exception:
        return "тест прошёл?!"

def test_good():
    try:
        buggy()
    except ValueError:
        return "ожидаемая ошибка"
    except Exception as e:
        return f"неожиданная {type(e).__name__}"

print(test_bad(), "|", test_good())
```

- `except Exception` в тесте «проглатывает» **любую** ошибку — даже баг `IndexError`, и тест зеленеет.
- Правильный тест ловит **ожидаемый** тип, а остальное — провал.
- Вывод: `тест прошёл?! | неожиданная IndexError`.

## Тест целиком

```python
def parse_port(text):
    if not text.isdigit():
        raise ValueError("не число")
    port = int(text)
    if not 1 <= port <= 65535:
        raise ValueError("вне диапазона")
    return port

def test_parse_port():
    assert parse_port("8080") == 8080
    for bad in ["x", "99999"]:
        try:
            parse_port(bad)
        except ValueError:
            continue
        assert False, f"для {bad!r} нет ValueError"

test_parse_port()
print("тест прошёл")
```

- Позитивная проверка — `assert` результата. Негативные — «должна быть ошибка, иначе `assert False`».
- `continue` в `except` — перейти к следующему случаю; если исключения не было, выполняется `assert False` с понятным сообщением.
- Вывод: `тест прошёл`.

## Итог

- Проверяй и успешные сценарии, и ошибочные.
- «Должно упасть»: `try` → `except Ожидаемый` → иначе `assert False` (в pytest — `pytest.raises`).
- Проверяй и тип, и текст ошибки.
- Не лови в тестах `Exception` — это прячет баги.
'''),
    short=t(r'''
```py
try:
    parse_port("x")
except ValueError as e:
    assert "не число" in str(e)       # тип + текст
else:
    assert False, "нет ValueError"
# pytest: with pytest.raises(ValueError, match="не число"): ...
except Exception: ...                 # в тестах — прячет баги!
```
'''),
    quiz=[
        q('Почему `except Exception` в тесте опасен?',
            ['Медленно', 'Тест пройдёт при любой ошибке, включая баги', 'Не работает', 'Не опасен'],
            1, 'Ловить нужно ожидаемый тип.'),
        q('Что проверить кроме типа исключения?',
            ['Ничего', 'Текст/сообщение ошибки', 'Время', 'Имя файла'],
            1, 'Ошибка может быть «не по той причине».'),
        q('Как в pytest проверить, что код выбрасывает ValueError?',
            ['`assert ValueError`', '`with pytest.raises(ValueError):`', '`try: pass`', '`pytest.error()`'],
            1, 'Контекстный менеджер pytest.raises.'),
    ],
),

# ---------- exc-m3-l4 ----------
'exc-m3-l4': dict(
    full=t(r'''
## Зачем это нужно

Соберём всё вместе: разбор ответов API, импорт данных с отчётом об ошибках, сводка ошибок, конвейер с указанием упавшего шага, загрузка настроек с понятными сообщениями. Это ежедневные задачи автотестов и вспомогательных скриптов.

## Разбор тела ответа

```python
import json
bodies = ['{"id": 1}', "<html>", "", '{"id": "2"}']
for body in bodies:
    try:
        data = json.loads(body)
        print("id =", int(data["id"]))
    except json.JSONDecodeError:
        print("не JSON")
```

- `json.JSONDecodeError` — некорректный JSON (тема «JSON»). Ещё возможны `KeyError` (нет поля), `ValueError` (id не число), `TypeError` (корень не объект) — их тоже стоит перечислить, если ответ может быть любым.
- Вывод: `id = 1`, `не JSON`, `не JSON`, `id = 2`.

## Разные ошибки — разная реакция

```python
def load_user(raw):
    try:
        name, age = raw.split(":")
        age = int(age)
    except ValueError:
        return None
    if age < 0:
        raise ValueError("возраст < 0")
    return name, age

for raw in ["Аня:25", "плохо", "Боря:-1"]:
    try:
        print(load_user(raw))
    except ValueError as e:
        print("ошибка данных:", e)
```

- Нечитаемую строку функция сама превращает в `None`, а бессмысленное значение — в явную ошибку для вызывающего кода.
- Вывод: `('Аня', 25)`, `None`, `ошибка данных: возраст < 0`.

## Сводка ошибок

```python
from collections import Counter
errors = Counter()
for value in ["1", "x", None, "2", [], "y"]:
    try:
        int(value)
    except Exception as e:
        errors[type(e).__name__] += 1
print(dict(errors))
```

- Здесь широкий `except Exception` уместен: мы не прячем ошибки, а **считаем** их для отчёта.
- Вывод: `{'ValueError': 2, 'TypeError': 2}`.

## Конвейер с указанием шага

```python
def safe_pipeline(value, steps):
    for i, step in enumerate(steps, start=1):
        try:
            value = step(value)
        except Exception as e:
            return ("error", i, type(e).__name__)
    return ("ok", value)

print(safe_pipeline(" 5 ", [str.strip, int, lambda x: x * 2]))
print(safe_pipeline("x", [str.strip, int, lambda x: x * 2]))
```

- Сообщение «упал шаг 2, ValueError» ускоряет поиск проблемы.
- Вывод: `('ok', 10)`, `('error', 2, 'ValueError')`.

## Настройки с понятными ошибками

```python
def load_settings(raw):
    try:
        timeout = int(raw.get("timeout", "30"))
    except ValueError as e:
        raise ValueError(f"плохое значение timeout: {raw['timeout']!r}") from e
    return {"timeout": timeout}

try:
    load_settings({"timeout": "x"})
except ValueError as e:
    print(e, "|", type(e.__cause__).__name__)
```

- Исходная ошибка `int()` непонятна пользователю («invalid literal…»), поэтому её заменяют понятной, сохранив причину через `from`.
- Вывод: `плохое значение timeout: 'x' | ValueError`.

## Итог

- Перечисляй в `except` все ожидаемые проблемы конкретными типами.
- Нечитаемые данные — пропустить/отметить; бессмысленные — явная ошибка.
- Широкий `except Exception` допустим для подсчёта и отчёта, а не для «проглатывания».
- Указывай, **где** упало (шаг, строка), и заменяй технические сообщения понятными (`raise ... from e`).
'''),
    short=t(r'''
```py
except (json.JSONDecodeError, KeyError, ValueError, TypeError): ...
errors[type(e).__name__] += 1          # сводка ошибок
return ("error", step_no, type(e).__name__)
raise ValueError(f"плохое значение {key}: {v!r}") from e
```
'''),
    quiz=[
        q('Когда уместен `except Exception`?',
            ['Всегда', 'Для подсчёта/логирования ошибок, не для проглатывания', 'Никогда', 'Только в тестах'],
            1, 'Осознанный широкий перехват.'),
        q('Зачем заменять ошибку `int()` своим сообщением через `from e`?',
            ['Быстрее', 'Понятное сообщение и сохранённая причина', 'Так требует Python', 'Чтобы скрыть ошибку'],
            1, 'Пользователю понятнее, отладке — полнее.'),
        q('Что полезно указать в сообщении об ошибке конвейера?',
            ['Ничего', 'Номер шага и тип ошибки', 'Время суток', 'Имя пользователя ОС'],
            1, 'Где и что упало.'),
    ],
),
}
