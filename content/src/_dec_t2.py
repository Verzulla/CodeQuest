"""Теория модуля «Практичные декораторы» темы «Декораторы».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- dec-wraps ----------
'dec-wraps': dict(
    full=t(r'''
## Зачем это нужно

После декорирования имя функции указывает на обёртку. Из-за этого функция «забывает» своё имя и описание: в логах, отчётах тестов и подсказках редактора вместо `login` видно `wrapper`. `functools.wraps` решает эту проблему одной строкой — пиши её в **каждом** декораторе.

## Проблема

```python
def deco(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@deco
def login(user):
    """Войти в систему."""
    return user

print(login.__name__, login.__doc__)
```

- Строка в тройных кавычках сразу после `def` — **docstring**, описание функции. Оно хранится в `__doc__`.
- `login` теперь — это `wrapper`, у которого своё имя и нет описания.
- Вывод: `wrapper None`.

## Решение: @wraps(func)

```python
from functools import wraps

def deco(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@deco
def login(user):
    """Войти в систему."""
    return user

print(login.__name__, login.__doc__)
print(login.__wrapped__("аня"))
```

- `from functools import wraps` — импорт из стандартного модуля `functools` (инструменты для функций).
- `@wraps(func)` над обёрткой копирует в неё имя, описание, модуль и другие данные исходной функции.
- Заодно добавляется `wrapper.__wrapped__` — ссылка на исходную функцию. Через неё можно вызвать функцию **без** обёртки (полезно в тестах).
- `wraps` сам является декоратором с параметром — такие мы разберём позже.
- Вывод: `login Войти в систему.`, `аня`.

## Почему это важно в тестах

```python
from functools import wraps

def plain(func):
    def wrapper():
        return func()
    return wrapper

def nice(func):
    @wraps(func)
    def wrapper():
        return func()
    return wrapper

@plain
def test_login(): pass

@nice
def test_signup(): pass

print(test_login.__name__, test_signup.__name__)
```

- Тестовые фреймворки находят тесты и пишут отчёты по `__name__`. Без `wraps` все задекорированные тесты назывались бы `wrapper`.
- Вывод: `wrapper test_signup`.

## Безопасно добраться до исходной функции

```python
from functools import wraps

def upper_result(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

@upper_result
def hi(name):
    return "hi " + name

original = getattr(hi, "__wrapped__", hi)
print(hi("аня"), original("аня"))
```

- `getattr(obj, "имя", по_умолчанию)` — прочитать атрибут, а если его нет — вернуть значение по умолчанию. Так код работает и для незадекорированных функций.
- Вывод: `HI АНЯ hi аня`.

## Декоратор без обёртки

Не каждому декоратору нужна обёртка. Если надо только пометить функцию, достаточно добавить атрибут и вернуть **ту же** функцию:

```python
def mark_slow(func):
    func.slow = True
    return func

@mark_slow
def test_big_report(): pass

def test_small(): pass

print([f.__name__ for f in [test_big_report, test_small] if getattr(f, "slow", False)])
```

- Здесь `wraps` не нужен: функция не подменяется.
- Так устроены метки `@pytest.mark.slow`.
- Вывод: `['test_big_report']`.

## Итог

- Без `wraps` функция получает имя `wrapper` и теряет описание.
- `@wraps(func)` над обёрткой — всегда.
- `f.__wrapped__` — исходная функция.
- Декоратор-метка может не создавать обёртку, а вернуть ту же функцию.
'''),
    short=t(r'''
```py
from functools import wraps

def deco(func):
    @wraps(func)                  # сохранить имя и описание
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

f.__name__                        # 'f', а не 'wrapper'
f.__doc__                         # описание
f.__wrapped__                     # исходная функция
getattr(f, "__wrapped__", f)
```
'''),
    quiz=[
        q('Какое имя у задекорированной функции без `@wraps`?',
            ['Исходное', 'wrapper (имя обёртки)', 'deco', 'None'],
            1, 'Имя указывает на обёртку.'),
        q('Что делает `@wraps(func)`?',
            ['Ускоряет функцию', 'Копирует в обёртку имя, описание и добавляет __wrapped__', 'Кэширует результат', 'Ловит ошибки'],
            1, 'Метаданные исходной функции переносятся на обёртку.'),
        q('Как получить исходную функцию из задекорированной с wraps?',
            ['`f.original`', '`f.__wrapped__`', '`f.__func__`', 'Никак'],
            1, 'wraps добавляет этот атрибут.'),
    ],
),

# ---------- dec-logging ----------
'dec-logging': dict(
    full=t(r'''
## Зачем это нужно

Самые частые декораторы в реальных проектах — служебные: записать в лог вызов и результат, записать упавший вызов, замерить время. Они не меняют логику функции, но очень помогают при отладке и разборе падений тестов.

## Лог вызовов

```python
from functools import wraps

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"→ {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"← {func.__name__} = {result}")
        return result
    return wrapper

@log
def add(a, b):
    return a + b

total = add(2, 3)
print("итог:", total)
```

- До вызова печатаем имя и аргументы: `{args}` — это кортеж, он уже выглядит как скобки вызова.
- Результат сохраняем в `result`, печатаем и **возвращаем**.
- Вывод: `→ add(2, 3)`, `← add = 5`, `итог: 5`.

## Лог ошибок с пробросом

```python
from functools import wraps

def log_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"{func.__name__} упала: {type(e).__name__}")
            raise
    return wrapper

@log_errors
def parse(text):
    return int(text)

print(parse("5"))
try:
    parse("x")
except ValueError:
    print("ошибку поймали снаружи")
```

- `raise` без аргументов внутри `except` — пробросить **ту же** ошибку дальше. Обёртка только записала факт и не спрятала ошибку.
- Прятать ошибки в логирующем декораторе нельзя: вызывающий код должен узнать о проблеме.
- Вывод: `5`, `parse упала: ValueError`, `ошибку поймали снаружи`.

## Замер времени

```python
import time
from functools import wraps

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        wrapper.last_time = time.perf_counter() - start
        return result
    return wrapper

@timed
def nap():
    time.sleep(0.01)
    return "ok"

print(nap(), nap.last_time > 0.005)
```

- `time.perf_counter()` — точные часы для замеров (в секундах, с долями). Абсолютное значение ничего не значит — важна **разность** двух показаний.
- `time.sleep(0.01)` — пауза на 0.01 секунды.
- Время каждый раз немного разное, поэтому печатаем не само число, а проверку.
- Вывод: `ok True`.
- Для замеров не используй `time.time()`: это системное время, его могут подвести назад.

## Статистика вызовов

```python
from functools import wraps

def call_stats(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.stats["calls"] += 1
        try:
            return func(*args, **kwargs)
        except Exception:
            wrapper.stats["errors"] += 1
            raise
    wrapper.stats = {"calls": 0, "errors": 0}
    return wrapper

@call_stats
def inv(x):
    return 1 / x

inv(1)
try:
    inv(0)
except ZeroDivisionError:
    pass
print(inv.stats)
```

- Атрибут-словарь создаётся один раз при декорировании и живёт, пока жива функция.
- Вывод: `{'calls': 2, 'errors': 1}`.

## Модуль logging

В настоящих проектах вместо `print` используют модуль `logging`: `logging.info(...)`, `logging.error(...)`. Он умеет писать в файл, добавлять время и уровень важности. Устройство декоратора от этого не меняется — меняется только строка с `print`.

## Итог

- Логирующий декоратор: записать → вызвать → записать → **вернуть результат**.
- Ошибку записывай и пробрасывай через `raise`.
- Время: `time.perf_counter()` до и после, разность — длительность.
- Статистику храни в атрибутах обёртки.
'''),
    short=t(r'''
```py
import time
from functools import wraps

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"{func.__name__}: {type(e).__name__}")
            raise                          # пробросить!
        finally:
            wrapper.last = time.perf_counter() - start
    return wrapper
```
'''),
    quiz=[
        q('Что делает `raise` без аргументов внутри `except`?',
            ['Ничего', 'Пробрасывает пойманную ошибку дальше', 'Создаёт новую ошибку', 'SyntaxError'],
            1, 'Ошибка продолжает лететь наружу.'),
        q('Какую функцию использовать для замера времени выполнения?',
            ['`time.time()`', '`time.perf_counter()`', '`time.sleep()`', '`datetime.now()`'],
            1, 'Это точные монотонные часы для замеров.'),
        q('Почему логирующий декоратор не должен глотать ошибки?',
            ['Так быстрее', 'Вызывающий код должен узнать о проблеме', 'Иначе SyntaxError', 'Лог станет пустым'],
            1, 'Скрытая ошибка превращается в загадочный None.'),
    ],
),

# ---------- dec-cache ----------
'dec-cache': dict(
    full=t(r'''
## Зачем это нужно

Если функция долго считает (или ходит в сеть) и для одних и тех же аргументов всегда даёт один и тот же ответ, результат можно **запомнить**. Повторный вызов вернёт готовый ответ мгновенно. Это называется **кэширование** или **мемоизация**.

## Свой memoize

```python
from functools import wraps

def memoize(func):
    cache = {}
    @wraps(func)
    def wrapper(n):
        if n not in cache:
            print("считаю", n)
            cache[n] = func(n)
        return cache[n]
    return wrapper

@memoize
def square(n):
    return n * n

print(square(4), square(4), square(5))
```

- `cache = {}` создаётся **один раз** — при декорировании. Обёртка помнит его через замыкание.
- Ключ словаря — аргумент, значение — результат.
- Второй `square(4)` берёт ответ из словаря и функцию не вызывает.
- Вывод: `считаю 4`, `считаю 5`, `16 16 25` (сначала вычисляются все аргументы `print`, потом печатается строка).

## Несколько аргументов

```python
from functools import wraps

def memoize(func):
    @wraps(func)
    def wrapper(*args):
        if args not in wrapper.cache:
            wrapper.cache[args] = func(*args)
        return wrapper.cache[args]
    wrapper.cache = {}
    return wrapper

@memoize
def add(a, b):
    return a + b

add(1, 2)
add(1, 2)
add(2, 1)
print(add.cache)
```

- Ключ — кортеж `args`: кортежи хешируемы и подходят как ключи словаря.
- Аргументы должны быть хешируемыми: список в качестве аргумента даст `TypeError: unhashable type`.
- Вывод: `{(1, 2): 3, (2, 1): 3}`.

## Готовое решение: lru_cache

```python
from functools import lru_cache

calls = 0

@lru_cache(maxsize=None)
def fib(n):
    global calls
    calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(30), calls)
info = fib.cache_info()
print(info.hits, info.misses)
```

- `@lru_cache(maxsize=None)` — встроенный кэш, неограниченный по размеру. С Python 3.9 то же самое — `@functools.cache`.
- Рекурсивные вызовы `fib` тоже идут через кэш, поэтому каждое `n` считается один раз: 31 вызов вместо 2,7 миллиона.
- `cache_info()` — статистика: `hits` (ответ из кэша), `misses` (пришлось считать).
- Вывод: `832040 31`, `28 31`.

## Ограниченный кэш

```python
from functools import lru_cache

@lru_cache(maxsize=2)
def load(name):
    print("загрузка", name)
    return name.upper()

load("a")
load("b")
load("a")
load("c")
load("b")
load.cache_clear()
load("a")
```

- **LRU** — Least Recently Used: при переполнении выкидывается элемент, который **дольше всех не использовали**.
- По шагам: `a`, `b` загружены; `a` — из кэша (теперь `b` самый старый); `c` вытесняет `b`; `b` грузится снова (вытесняя `a`).
- `cache_clear()` — очистить кэш полностью.
- Вывод: `загрузка a`, `загрузка b`, `загрузка c`, `загрузка b`, `загрузка a`.

## Когда кэшировать нельзя

- Функция зависит от времени, случайности, внешних данных (`datetime.now()`, запрос к API, который меняется).
- Функция что-то делает помимо возврата значения (пишет в файл, отправляет письмо) — при повторе ничего не произойдёт.
- Результат изменяемый (список): все вызовы получат **один и тот же** объект.

## Итог

- Memoize: словарь `аргументы → результат` в замыкании или атрибуте.
- Ключ — `args` (кортеж), аргументы должны быть хешируемыми.
- `@lru_cache(maxsize=N)` / `@cache` — готовый кэш; `cache_info()`, `cache_clear()`.
- Кэшируй только «чистые» функции.
'''),
    short=t(r'''
```py
from functools import lru_cache, cache

@lru_cache(maxsize=128)   # последние 128 разных вызовов
def load(name): ...

@cache                    # без ограничения (= maxsize=None)
def fib(n): ...

fib.cache_info()          # hits, misses, maxsize, currsize
fib.cache_clear()

# свой: cache = {}; if args not in cache: cache[args] = func(*args)
```
'''),
    quiz=[
        q('Какие функции можно кэшировать?',
            ['Любые', 'Те, что для одних аргументов всегда дают один результат и ничего не меняют вокруг', 'Только рекурсивные', 'Только без аргументов'],
            1, 'Иначе кэш вернёт устаревший ответ или пропустит действие.'),
        q('Что выкидывает `lru_cache` при переполнении?',
            ['Самый новый', 'Дольше всех не использованный', 'Случайный', 'Самый большой'],
            1, 'Least Recently Used.'),
        q('Почему список нельзя передать в функцию с `lru_cache`?',
            ['Слишком большой', 'Список нехешируемый — не может быть ключом', 'lru_cache принимает только числа', 'Можно'],
            1, 'Аргументы — ключи словаря.'),
    ],
),

# ---------- dec-retry ----------
'dec-retry': dict(
    full=t(r'''
## Зачем это нужно

Сеть иногда сбоит: сервер не ответил, соединение оборвалось, страница ещё не загрузилась. Такие ошибки **временные** — через секунду тот же запрос пройдёт. Декоратор повтора (retry) пробует вызвать функцию ещё раз. В автотестах так борются с нестабильными («флакающими») проверками.

## Простой retry

```python
from functools import wraps

def retry3(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for attempt in range(1, 4):
            try:
                return func(*args, **kwargs)
            except ConnectionError:
                print("попытка", attempt, "не удалась")
        raise ConnectionError("сервер недоступен")
    return wrapper

answers = iter([ConnectionError, "200 OK"])

@retry3
def request():
    a = next(answers)
    if a is ConnectionError:
        raise ConnectionError
    return a

print(request())
```

- Цикл на 3 попытки. `return` внутри `try` сразу завершает обёртку при успехе.
- При `ConnectionError` печатаем и идём на следующую попытку.
- Если все попытки неудачны, цикл заканчивается, и выбрасываем ошибку.
- `iter([...])` и `next(...)` — выдают элементы списка по одному: так имитируем сервер, который сначала падает, потом отвечает.
- Вывод: `попытка 1 не удалась`, `200 OK`.

## Пробросить последнюю ошибку

```python
from functools import wraps

def retry3(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for attempt in range(3):
            try:
                return func(*args, **kwargs)
            except ConnectionError:
                if attempt == 2:
                    raise
    return wrapper

calls = 0

@retry3
def dead():
    global calls
    calls += 1
    raise ConnectionError(f"нет сети #{calls}")

try:
    dead()
except ConnectionError as e:
    print(e)
```

- На последней попытке (`attempt == 2`) делаем `raise` — пробрасываем **настоящую** ошибку с её текстом. Так при разборе падения видна реальная причина.
- Вывод: `нет сети #3`.

## Повторять только временные ошибки

```python
from functools import wraps

def retry_network(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for _ in range(3):
            try:
                return func(*args, **kwargs)
            except ConnectionError:
                print("сеть, повтор")
        return None
    return wrapper

@retry_network
def bad_request():
    raise ValueError("неверные данные")

try:
    bad_request()
except ValueError as e:
    print("сразу:", e)
```

- `except ConnectionError` ловит только сетевые ошибки. `ValueError` пролетает сквозь обёртку с первой попытки.
- Повторять ошибку в данных бессмысленно — результат будет тот же. Никогда не пиши `except Exception` в retry.
- Вывод: `сразу: неверные данные`.

## Паузы между попытками

Повторять мгновенно часто бесполезно: серверу нужно время. Обычно ждут всё дольше — 1, 2, 4 секунды (**экспоненциальная задержка**):

```python
from functools import wraps

waits = []

def sleep(seconds):
    waits.append(seconds)

def retry_with_delays(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        delays = [1, 2, 4]
        for attempt in range(4):
            try:
                return func(*args, **kwargs)
            except ConnectionError:
                if attempt == 3:
                    raise
                sleep(delays[attempt])
    return wrapper

state = {"n": 0}

@retry_with_delays
def req():
    state["n"] += 1
    if state["n"] < 3:
        raise ConnectionError
    return "ok"

print(req(), waits)
```

- В настоящем коде `sleep` — это `time.sleep`. Здесь он подменён функцией, которая только записывает паузу: так пример (и тест) не ждёт реальные секунды.
- Вывод: `ok [1, 2]`.

## Ожидание условия

```python
from functools import wraps

def until_true(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for _ in range(5):
            result = func(*args, **kwargs)
            if result:
                return result
        raise TimeoutError("не дождались")
    return wrapper

answers = iter([None, "", "кнопка"])

@until_true
def find_button():
    return next(answers)

print(find_button())
```

- Похожий приём — повторять не при ошибке, а пока результат ложный. Так работают «явные ожидания» в Selenium и Playwright.
- Вывод: `кнопка`.

## Итог

- Retry: цикл попыток, `return` при успехе, `raise` на последней.
- Ловить **только** временные ошибки (`ConnectionError`, `TimeoutError`).
- Паузы между попытками, лучше растущие.
- Retry прячет нестабильность — не лечит её. Если тест флакает, ищи причину.
'''),
    short=t(r'''
```py
from functools import wraps
import time

def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for attempt in range(3):
            try:
                return func(*args, **kwargs)   # успех — выход
            except (ConnectionError, TimeoutError):
                if attempt == 2:
                    raise                      # последняя ошибка
                time.sleep(2 ** attempt)       # 1, 2 с
    return wrapper
```
'''),
    quiz=[
        q('Какие ошибки имеет смысл повторять?',
            ['Любые', 'Временные: сетевые, таймауты', 'ValueError', 'SyntaxError'],
            1, 'Ошибка в данных при повторе будет той же.'),
        q('Что сделать, если все попытки неудачны?',
            ['Вернуть None молча', 'Пробросить последнюю ошибку', 'Повторять бесконечно', 'Вернуть True'],
            1, 'Вызывающий должен узнать о проблеме и её причине.'),
        q('Что такое экспоненциальная задержка?',
            ['Пауза одинаковая', 'Паузы растут: 1, 2, 4…', 'Без пауз', 'Случайные паузы'],
            1, 'Серверу даётся всё больше времени восстановиться.'),
    ],
),

}
