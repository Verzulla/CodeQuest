"""Теория модуля «Практика» темы «Контекстные менеджеры».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- ctx-state ----------
'ctx-state': dict(
    full=t(r'''
## Зачем это нужно

В тестах постоянно нужно **временно** что-то поменять: включить отладочный режим, подставить тестовый адрес API, задать переменную окружения, подменить функцию. После теста всё должно вернуться как было — иначе следующий тест получит «грязное» состояние и упадёт непонятно почему. Контекстный менеджер — идеальный инструмент: «поменять → блок → вернуть».

## Временная настройка в словаре

```python
from contextlib import contextmanager

config = {"debug": False, "url": "prod"}

@contextmanager
def override(settings, **changes):
    old = dict(settings)
    settings.update(changes)
    try:
        yield settings
    finally:
        settings.clear()
        settings.update(old)

with override(config, debug=True, url="test"):
    print(config)
print(config)
```

- `dict(settings)` — снимок до изменений.
- `**changes` — любые именованные аргументы собираются в словарь.
- `finally` восстанавливает снимок в **тот же** объект — даже если тест упал.
- Вывод: `{'debug': True, 'url': 'test'}`, `{'debug': False, 'url': 'prod'}`.

## Подмена атрибута

```python
from contextlib import contextmanager

class Api:
    base_url = "https://prod.example"

@contextmanager
def patched(obj, name, value):
    old = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield old
    finally:
        setattr(obj, name, old)

with patched(Api, "base_url", "http://localhost:8000"):
    print(Api.base_url)
print(Api.base_url)
```

- `getattr(obj, "имя")` / `setattr(obj, "имя", значение)` — прочитать и записать атрибут, имя которого задано строкой.
- Именно так устроен `unittest.mock.patch` — главный инструмент подмены в Python-тестах.
- Вывод: `http://localhost:8000`, `https://prod.example`.

## Ключа не было

```python
from contextlib import contextmanager

_MISSING = object()

@contextmanager
def temp_value(data, key, value):
    old = data.get(key, _MISSING)
    data[key] = value
    try:
        yield
    finally:
        if old is _MISSING:
            del data[key]
        else:
            data[key] = old

d = {"a": None}
with temp_value(d, "a", 1), temp_value(d, "b", 2):
    print(d)
print(d)
```

- Если ключа раньше не было, после блока его нужно **удалить**, а не записать `None`.
- `_MISSING = object()` — уникальный объект-маркер. Его не спутать ни с каким настоящим значением, даже с `None`.
- Вывод: `{'a': 1, 'b': 2}`, `{'a': None}`.

## Переменные окружения

```python
import os
from contextlib import contextmanager

@contextmanager
def env(**values):
    old = {k: os.environ.get(k) for k in values}
    os.environ.update(values)
    try:
        yield
    finally:
        for k, v in old.items():
            if v is None:
                del os.environ[k]
            else:
                os.environ[k] = v

with env(STAND="stage"):
    print(os.environ["STAND"])
print(os.environ.get("STAND"))
```

- `os.environ` — словарь переменных окружения процесса. Конфигурацию тестов (стенд, токены) часто передают через них.
- Вывод: `stage`, `None`.
- В pytest то же делает фикстура `monkeypatch`: `monkeypatch.setenv("STAND", "stage")`.

## Итог

- Шаблон: запомнить → изменить → `try: yield` → `finally: восстановить`.
- `getattr`/`setattr` — подмена атрибутов по имени.
- Отсутствующий ключ — маркер `object()`, после блока удалить.
- В реальных тестах: `unittest.mock.patch`, `monkeypatch`.
'''),
    short=t(r'''
```py
@contextmanager
def patched(obj, name, value):
    old = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield old
    finally:
        setattr(obj, name, old)     # вернуть всегда

_MISSING = object()                 # «ключа не было»
old = d.get(k, _MISSING)
# pytest: monkeypatch.setattr / setenv; unittest.mock.patch
```
'''),
    quiz=[
        q('Почему восстановление ставят в `finally`?',
            ['Так быстрее', 'Чтобы состояние вернулось и при упавшем тесте', 'Этого требует yield', 'Не обязательно'],
            1, 'Иначе следующий тест получит изменённое состояние.'),
        q('Что делает `setattr(obj, "x", 5)`?',
            ['Читает obj.x', 'Присваивает obj.x = 5', 'Удаляет obj.x', 'Создаёт копию'],
            1, 'Имя атрибута задано строкой.'),
        q('Зачем маркер `_MISSING = object()`, а не `None`?',
            ['None нельзя хранить в словаре', 'Чтобы отличить «ключа не было» от «значение было None»', 'Так быстрее', 'Так требует contextmanager'],
            1, 'object() уникален.'),
    ],
),

# ---------- ctx-timing ----------
'ctx-timing': dict(
    full=t(r'''
## Зачем это нужно

«Сколько длился этот шаг?», «Страница грузится дольше 2 секунд?», «Покажи шаги теста в отчёте». Всё это — «сделать что-то до и после блока кода», то есть работа для контекстного менеджера. Так устроены `allure.step` и многие профилировщики.

## Секундомер на функции

```python
import time
from contextlib import contextmanager

@contextmanager
def stopwatch(results, name):
    start = time.perf_counter()
    try:
        yield
    finally:
        results[name] = time.perf_counter() - start

results = {}
with stopwatch(results, "пауза"):
    time.sleep(0.05)
print(list(results), 0.04 < results["пауза"] < 1)
```

- `time.perf_counter()` — точные часы для замеров; разность двух показаний — длительность в секундах.
- `finally` — замер записывается, даже если блок упал.
- Точное время каждый раз немного разное, поэтому печатаем проверку, а не число.
- Вывод: `['пауза'] True`.

## Класс-таймер

```python
import time

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        self.elapsed = None
        return self

    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start
        return False

with Timer() as t:
    print("внутри:", t.elapsed)
    time.sleep(0.02)
print("после:", t.elapsed > 0.01)
```

- Объект из `as` живёт и после блока — результат замера читаем из его атрибута.
- Вывод: `внутри: None`, `после: True`.

## Проверка производительности

```python
from contextlib import contextmanager

@contextmanager
def time_limit(seconds, clock):
    start = clock()
    yield
    spent = clock() - start
    if spent > seconds:
        raise AssertionError(f"медленно: {spent:.2f} c > {seconds} c")

ticks = iter([0.0, 0.5, 10.0, 12.25])
fake_clock = lambda: next(ticks)
with time_limit(1, fake_clock):
    pass
try:
    with time_limit(2, fake_clock):
        pass
except AssertionError as e:
    print(e)
```

- Часы передаются параметром: в тестах — поддельные (`iter` + `next` выдают заранее известные значения), в бою — `time.perf_counter`.
- Проверка после `yield` без `try`: если блок упал, проверять время уже не нужно.
- Вывод: `медленно: 2.25 c > 2 c`.

## Шаги теста

```python
from contextlib import contextmanager

depth = 0

@contextmanager
def step(name):
    global depth
    print("  " * depth + "▶ " + name)
    depth += 1
    try:
        yield
    finally:
        depth -= 1

with step("оформление заказа"):
    with step("корзина"):
        pass
    with step("оплата"):
        with step("ввод карты"):
            pass
```

- Глубина вложенности растёт при входе и уменьшается при выходе — получается дерево шагов.
- В Allure: `with allure.step("Открыть корзину"): ...` — шаг с именем, временем и статусом в отчёте.
- Вывод: `▶ оформление заказа`, `  ▶ корзина`, `  ▶ оплата`, `    ▶ ввод карты`.

## @contextmanager на методе

```python
from contextlib import contextmanager

class Profiler:
    def __init__(self, clock):
        self.clock = clock
        self.totals = {}

    @contextmanager
    def measure(self, name):
        start = self.clock()
        try:
            yield
        finally:
            self.totals[name] = self.totals.get(name, 0) + self.clock() - start

ticks = iter([0, 1, 1, 4])
p = Profiler(lambda: next(ticks))
with p.measure("db"):
    pass
with p.measure("db"):
    pass
print(p.totals)
```

- Декоратор работает и на методах: `self` передаётся как обычно.
- Вывод: `{'db': 4}`.

## Итог

- Замер: `perf_counter()` до и после, запись в `finally`.
- Часы — параметром, чтобы тестировать без ожидания.
- Шаги отчёта — вложенные менеджеры (`allure.step`).
- `@contextmanager` можно применять к методам.
'''),
    short=t(r'''
```py
import time
from contextlib import contextmanager

@contextmanager
def stopwatch(results, name, clock=time.perf_counter):
    start = clock()
    try:
        yield
    finally:
        results[name] = clock() - start

with stopwatch(res, "login"):
    ...
# allure: with allure.step("Открыть корзину"): ...
```
'''),
    quiz=[
        q('Почему запись времени ставят в `finally`?',
            ['Так точнее', 'Чтобы замер записался и при ошибке', 'Этого требует perf_counter', 'Не обязательно'],
            1, 'Упавший шаг тоже важно замерить.'),
        q('Зачем передавать часы параметром?',
            ['Для скорости', 'Чтобы в тестах подставить поддельные и не ждать', 'Так требует Python', 'Для часовых поясов'],
            1, 'Предсказуемые значения — стабильные тесты.'),
        q('Можно ли применить `@contextmanager` к методу класса?',
            ['Нет', 'Да', 'Только к staticmethod', 'Только к __enter__'],
            1, 'self передаётся как обычно.'),
    ],
),

# ---------- ctx-testing ----------
'ctx-testing': dict(
    full=t(r'''
## Зачем это нужно

Главные инструменты тестировщика на Python построены на контекстных менеджерах: `pytest.raises` проверяет исключения, фикстуры с `yield` готовят и убирают данные, `mock.patch` подменяет зависимости, `redirect_stdout` перехватывает вывод. Напишем их упрощённые версии, чтобы понимать, как они работают.

## Ожидаемое исключение: raises

```python
from contextlib import contextmanager

@contextmanager
def raises(exc_type):
    try:
        yield
    except exc_type:
        print("ожидаемая ошибка", exc_type.__name__)
    else:
        raise AssertionError(f"не было {exc_type.__name__}")

with raises(ZeroDivisionError):
    1 / 0
try:
    with raises(KeyError):
        pass
except AssertionError as e:
    print(e)
```

- Нужная ошибка — тест проходит (ошибка заглушена).
- Ошибки не было — это провал: `AssertionError`.
- Другая ошибка — летит дальше, тест «сломан».
- В pytest: `with pytest.raises(ValueError, match="invalid"): int("x")`.
- Вывод: `ожидаемая ошибка ZeroDivisionError`, `не было KeyError`.

## Фикстура с yield

```python
from contextlib import contextmanager

@contextmanager
def user_fixture(db):
    user = {"id": len(db) + 1, "name": "test"}
    db.append(user)
    print("создан", user["id"])
    try:
        yield user
    finally:
        db.remove(user)
        print("удалён", user["id"])

db = []
with user_fixture(db) as u:
    print("тест с", u["name"], len(db))
print(len(db))
```

- До `yield` — подготовка (setup), `yield` отдаёт данные тесту, после — уборка (teardown).
- Фикстура pytest выглядит так же: `@pytest.fixture` + функция с `yield`. Pytest сам оборачивает тест в такой менеджер.
- Вывод: `создан 1`, `тест с test 1`, `удалён 1`, `0`.

## Проверка вывода

```python
import io
from contextlib import redirect_stdout

def greet(name):
    print(f"Привет, {name}!")

buf = io.StringIO()
with redirect_stdout(buf):
    greet("Аня")
assert buf.getvalue() == "Привет, Аня!\n"
print("вывод совпал:", repr(buf.getvalue()))
```

- Перехватываем вывод в буфер и сравниваем.
- В pytest то же делает фикстура `capsys`: `capsys.readouterr().out`.
- Вывод: `вывод совпал: 'Привет, Аня!\n'`.

## Шпион: запись вызовов

```python
from contextlib import contextmanager

@contextmanager
def spy(obj, name):
    original = getattr(obj, name)
    calls = []

    def wrapper(*args):
        calls.append(args)
        return original(*args)

    setattr(obj, name, wrapper)
    try:
        yield calls
    finally:
        setattr(obj, name, original)

class Mailer:
    @staticmethod
    def send(to, text):
        return "sent"

with spy(Mailer, "send") as calls:
    Mailer.send("anna@test.ru", "привет")
print(calls)
```

- Временно заменяем метод обёрткой, которая записывает аргументы и вызывает оригинал.
- Тест может проверить: «письмо отправлено ровно один раз и на правильный адрес».
- В `unittest.mock`: `with patch.object(Mailer, "send") as m: ...; m.assert_called_once_with(...)`.
- Вывод: `[('anna@test.ru', 'привет')]`.

## Итог

- `raises` — ожидаемая ошибка: глушим нужную, падаем без неё.
- Фикстура: setup → `yield данные` → teardown в `finally`.
- `redirect_stdout` — проверка вывода.
- Шпион — `setattr` обёртки, запись вызовов, восстановление.
'''),
    short=t(r'''
```py
@contextmanager
def raises(exc):
    try:
        yield
    except exc:
        return                        # ок, заглушить
    raise AssertionError(f"не было {exc.__name__}")

@contextmanager
def fixture():
    data = setup()
    try:
        yield data
    finally:
        teardown(data)
# pytest.raises, @pytest.fixture + yield, capsys, mock.patch
```
'''),
    quiz=[
        q('Что делает `pytest.raises`, если исключения не было?',
            ['Ничего', 'Роняет тест', 'Пропускает тест', 'Печатает предупреждение'],
            1, 'Ожидаемая ошибка не произошла — это провал.'),
        q('Где в фикстуре с yield выполняется уборка?',
            ['До yield', 'После yield', 'В начале теста', 'Не выполняется'],
            1, 'Лучше — в finally.'),
        q('Как в pytest проверить, что функция напечатала текст?',
            ['assert print', 'Фикстура capsys (или redirect_stdout)', 'suppress', 'ExitStack'],
            1, 'capsys.readouterr().out.'),
    ],
),

# ---------- ctx-resources ----------
'ctx-resources': dict(
    full=t(r'''
## Зачем это нужно

Тестовое окружение состоит из ресурсов: сессия API с токеном, соединение с базой, пул соединений, браузер, поднятые сервисы. Каждый нужно корректно открыть и закрыть, а при падении теста — ещё и сохранить улики (скриншот, логи). Соберём всё изученное в практические шаблоны.

## Сессия API

```python
class ApiSession:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None

    def __enter__(self):
        self.token = "t-123"
        print("вход, токен", self.token)
        return self

    def __exit__(self, *args):
        print("выход, токен отозван")
        self.token = None
        return False

    def get(self, path):
        return f"GET {self.base_url}{path} [{self.token}]"

with ApiSession("https://api.test") as s:
    print(s.get("/users"))
print(s.token)
```

- Вход — авторизация, выход — выход из системы. Токен не «висит» после тестов.
- Вывод: `вход, токен t-123`, `GET https://api.test/users [t-123]`, `выход, токен отозван`, `None`.

## Пул соединений

```python
from contextlib import contextmanager

class Pool:
    def __init__(self, size):
        self.free = [f"conn{i}" for i in range(size)]

    @contextmanager
    def connection(self):
        conn = self.free.pop()
        try:
            yield conn
        finally:
            self.free.append(conn)

pool = Pool(2)
with pool.connection() as a:
    with pool.connection() as b:
        print(a, b, pool.free)
    print(pool.free)
print(sorted(pool.free))
```

- Соединение «берётся» из пула и **обязательно** возвращается — иначе пул быстро опустеет.
- Вывод: `conn1 conn0 []`, `['conn0']`, `['conn0', 'conn1']`.

## Скриншот при падении

```python
class Browser:
    def __init__(self, log):
        self.log = log

    def __enter__(self):
        self.log.append("start")
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.log.append(f"screenshot: {exc_type.__name__}")
        self.log.append("quit")
        return False

log = []
try:
    with Browser(log):
        raise AssertionError("нет кнопки")
except AssertionError:
    pass
print(log)
```

- `__exit__` знает об ошибке — самое место сохранить скриншот и логи браузера для отчёта.
- Вывод: `['start', 'screenshot: AssertionError', 'quit']`.

## Всё окружение через ExitStack

```python
from contextlib import contextmanager, ExitStack

@contextmanager
def service(name, log):
    log.append("up " + name)
    try:
        yield name
    finally:
        log.append("down " + name)

def environment(names, log):
    with ExitStack() as stack:
        for name in names:
            stack.enter_context(service(name, log))
        return stack.pop_all()

log = []
stack = environment(["db", "api"], log)
with stack:
    log.append("tests")
print(log)
```

- Если подъём какого-то сервиса упадёт, `with ExitStack()` закроет уже поднятые.
- `pop_all()` — «всё поднялось»: переносит менеджеры в новый стек, который возвращается вызывающему. Он закроет их позже своим `with`.
- Вывод: `['up db', 'up api', 'tests', 'down api', 'down db']`.

## Мягкие проверки

```python
class SoftAssert:
    def __init__(self):
        self.errors = []

    def __enter__(self):
        return self

    def check(self, condition, message):
        if not condition:
            self.errors.append(message)

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None and self.errors:
            raise AssertionError("; ".join(self.errors))
        return False

try:
    with SoftAssert() as s:
        s.check(1 + 1 == 2, "математика")
        s.check("a" in "xyz", "нет буквы a")
        s.check([] != [], "списки")
except AssertionError as e:
    print(e)
```

- Проверки не прерывают тест сразу: все ошибки собираются и выбрасываются одним `AssertionError` в конце. Так за один прогон видно все проблемы страницы.
- Вывод: `нет буквы a; списки`.

## Итог

- Сессии, соединения, браузеры — менеджеры: вход открывает, выход закрывает.
- Пул: взять → `yield` → вернуть в `finally`.
- `__exit__` с ошибкой — время для скриншотов и логов.
- `ExitStack` + `pop_all()` — окружение из многих ресурсов.
- Мягкие проверки — сбор ошибок и один `AssertionError` в `__exit__`.
'''),
    short=t(r'''
```py
class Browser:
    def __enter__(self):
        self.start(); return self
    def __exit__(self, exc_type, exc, tb):
        if exc_type: self.screenshot()   # улики
        self.quit()
        return False

with ExitStack() as stack:
    for s in services:
        stack.enter_context(s)
    env = stack.pop_all()                # закроет вызывающий
with env: run_tests()
```
'''),
    quiz=[
        q('Где удобнее всего делать скриншот упавшего UI-теста?',
            ['В __enter__', 'В __exit__ при exc_type не None', 'В начале теста', 'В __init__'],
            1, '__exit__ знает, была ли ошибка.'),
        q('Что делает `ExitStack.pop_all()`?',
            ['Закрывает всё', 'Переносит менеджеры в новый стек, не закрывая их', 'Удаляет последний', 'Очищает без закрытия навсегда'],
            1, 'Закрыть их должен вызывающий код.'),
        q('Чем мягкие проверки отличаются от обычных assert?',
            ['Ничем', 'Собирают все ошибки и падают один раз в конце', 'Никогда не падают', 'Работают быстрее'],
            1, 'Видно все проблемы за один прогон.'),
    ],
),

}
