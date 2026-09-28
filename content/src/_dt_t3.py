"""Теория модуля «Пояса, timestamp и тесты» темы «Дата и время».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- dt-timezone ----------
'dt-timezone': dict(
    full=t(r'''
## Зачем это нужно

Когда в Москве 15:00, в Лондоне 12:00, а в Нью-Йорке 7:00 — и это **один и тот же момент**. Серверы, базы данных и API обычно хранят время в **UTC** (всемирное время), а пользователю показывают местное. Если не учитывать пояса, появляются баги «заказ создан в будущем» и «тест падает только ночью».

## naive и aware

- **naive** («наивный») `datetime` — без часового пояса. Непонятно, какой это момент: 12:00 где?
- **aware** («осведомлённый») — с поясом (`tzinfo`). Однозначно указывает момент.

```python
from datetime import datetime, timezone, timedelta

naive = datetime(2024, 3, 8, 12, 0)
utc = datetime(2024, 3, 8, 12, 0, tzinfo=timezone.utc)
print(naive.tzinfo, utc.tzinfo)
print(utc)
```

- `timezone.utc` — готовый пояс UTC.
- `tzinfo=` — параметр для пояса при создании.
- В выводе aware-объекта появляется смещение `+00:00`.
- Вывод: `None UTC`, `2024-03-08 12:00:00+00:00`.

## Пояс с фиксированным смещением

```python
from datetime import datetime, timezone, timedelta

msk = timezone(timedelta(hours=3), "MSK")
ny = timezone(timedelta(hours=-5), "NY")
utc_time = datetime(2024, 3, 8, 12, 0, tzinfo=timezone.utc)
print(utc_time.astimezone(msk))
print(utc_time.astimezone(ny).strftime("%H:%M %Z"))
```

- `timezone(timedelta(hours=3), "MSK")` — пояс со смещением +3 часа от UTC; имя необязательно.
- `astimezone(пояс)` — **перевести** момент в другой пояс: цифры на часах меняются, момент остаётся тем же.
- `%Z` — имя пояса в `strftime`.
- Вывод: `2024-03-08 15:00:00+03:00`, `07:00 NY`.

## Сравнение aware-времени

```python
from datetime import datetime, timezone, timedelta

msk = timezone(timedelta(hours=3))
a = datetime(2024, 3, 8, 15, 0, tzinfo=msk)
b = datetime(2024, 3, 8, 12, 0, tzinfo=timezone.utc)
print(a == b, a - b)
```

- Aware-объекты сравниваются как **моменты**, а не как цифры на часах. 15:00 MSK = 12:00 UTC.
- Вывод: `True 0:00:00`.

## naive и aware не смешиваются

```python
from datetime import datetime, timezone

naive = datetime(2024, 3, 8, 12, 0)
aware = datetime(2024, 3, 8, 12, 0, tzinfo=timezone.utc)
try:
    naive < aware
except TypeError:
    print("сравнивать naive и aware нельзя")
print(naive == aware)
print(naive.replace(tzinfo=timezone.utc) == aware)
```

- `<`, `>`, вычитание naive и aware → `TypeError`.
- `==` не падает, но всегда `False` — коварно!
- `replace(tzinfo=...)` — **прикрепить** пояс, не меняя цифр («считаем, что это было UTC»). Не путай с `astimezone` — тот пересчитывает время.
- Вывод: `сравнивать naive и aware нельзя`, `False`, `True`.

## Настоящие пояса: zoneinfo

Смещение многих стран меняется (летнее время), поэтому для городов используют базу поясов:

```py
from zoneinfo import ZoneInfo           # Python 3.9+
dt = datetime(2024, 7, 1, 12, tzinfo=ZoneInfo("Europe/London"))
dt.astimezone(ZoneInfo("Europe/Moscow"))
```

- Имена поясов вида `"Europe/Moscow"`, `"America/New_York"`. Базе нужен системный пакет `tzdata`.

## Правила

- Храни и передавай время в **UTC**, в местное переводи только для показа.
- Используй aware-объекты: `datetime.now(timezone.utc)` вместо `datetime.now()`.
- `datetime.utcnow()` устарел: он возвращает naive-время.

## Итог

- naive — без пояса, aware — с `tzinfo`.
- `timezone.utc`, `timezone(timedelta(hours=3))`.
- `astimezone(tz)` — пересчитать; `replace(tzinfo=tz)` — прикрепить.
- naive и aware нельзя сравнивать и вычитать.
'''),
    short=t(r'''
```py
from datetime import datetime, timezone, timedelta

UTC = timezone.utc
MSK = timezone(timedelta(hours=3), "MSK")

datetime.now(UTC)                     # aware «сейчас»
dt = datetime(2024, 3, 8, 12, tzinfo=UTC)
dt.astimezone(MSK)                    # 15:00+03:00 (пересчёт)
naive.replace(tzinfo=UTC)             # прикрепить пояс
dt.tzinfo is None                     # naive?
dt.utcoffset()                        # смещение
# naive < aware → TypeError
```
'''),
    quiz=[
        q('Чем `astimezone(tz)` отличается от `replace(tzinfo=tz)`?',
            ['Ничем', 'astimezone пересчитывает цифры, replace только прикрепляет пояс', 'replace пересчитывает, astimezone нет', 'astimezone работает только с UTC'],
            1, 'Момент при astimezone не меняется.'),
        q('Что будет при `naive < aware`?',
            ['False', 'TypeError', 'Сравнение по цифрам', 'True'],
            1, 'Смешивать нельзя.'),
        q('В каком поясе принято хранить время на сервере?',
            ['Местном', 'UTC', 'Московском', 'Без пояса'],
            1, 'В местное переводят только для показа.'),
    ],
),

# ---------- dt-timestamp ----------
'dt-timestamp': dict(
    full=t(r'''
## Зачем это нужно

Многие системы хранят время одним числом — **Unix-временем** (timestamp): сколько секунд прошло с полуночи 1 января 1970 года UTC. Такие числа приходят из API, JWT-токенов, логов, баз данных. Ещё есть модуль `time` для пауз и замеров.

## timestamp ↔ datetime

```python
from datetime import datetime, timezone

epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
dt = datetime(2024, 3, 8, 12, 0, tzinfo=timezone.utc)
print(dt.timestamp())
print((dt - epoch).total_seconds())
print(datetime.fromtimestamp(0, tz=timezone.utc))
print(datetime.fromtimestamp(1709899200, tz=timezone.utc))
```

- **Эпоха** (epoch) — точка отсчёта: 1970-01-01 00:00 UTC.
- `dt.timestamp()` — секунды от эпохи (дробное число). Это ровно разность с эпохой.
- `datetime.fromtimestamp(ts, tz=timezone.utc)` — обратно в aware-`datetime`. Без `tz=` получится naive-время **в поясе компьютера** — источник багов.
- Вывод: `1709899200.0`, `1709899200.0`, `1970-01-01 00:00:00+00:00`, `2024-03-08 12:00:00+00:00`.

## Секунды или миллисекунды

```python
from datetime import datetime, timezone

ms = 1709899200500
dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
print(dt)
print(int(dt.timestamp() * 1000) == ms)
print(len(str(ms)), len(str(ms // 1000)))
```

- JavaScript и многие API отдают **миллисекунды** — 13 цифр вместо 10. Раздели на 1000.
- Обратно: `int(dt.timestamp() * 1000)`.
- Если не разделить — получится дата в далёком будущем или `ValueError`.
- Вывод: `2024-03-08 12:00:00.500000+00:00`, `True`, `13 10`.

## Модуль time

```python
import time

start = time.perf_counter()
time.sleep(0.05)
elapsed = time.perf_counter() - start
print(elapsed >= 0.05, elapsed < 1)
print(type(time.time()).__name__, time.time() > 1_700_000_000)
```

- `time.time()` — текущий timestamp (секунды, дробное число).
- `time.sleep(секунды)` — пауза.
- `time.perf_counter()` — точные часы для **замеров длительности**: само значение ничего не значит, важна разность. Они не прыгают, если системное время перевели.
- Вывод: `True True`, `float True`.

## Проверка «свежести»

```python
now = 1_700_000_000
created = now - 120
max_age = 300
age = now - created
print(age, 0 <= age <= max_age)
```

- С timestamp удобно считать возраст записи простым вычитанием.
- `1_700_000_000` — подчёркивания в числе для читаемости.
- Вывод: `120 True`.

## Итог

- Timestamp — секунды от 1970-01-01 UTC.
- `dt.timestamp()`; `datetime.fromtimestamp(ts, tz=timezone.utc)` — всегда с `tz`.
- 13 цифр — миллисекунды: `/ 1000`.
- `time.time()` — сейчас, `time.sleep()` — пауза, `time.perf_counter()` — замеры.
'''),
    short=t(r'''
```py
from datetime import datetime, timezone
import time

dt.timestamp()                                   # → float секунд
datetime.fromtimestamp(ts, tz=timezone.utc)      # tz обязательно!
datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
int(dt.timestamp() * 1000)                       # → миллисекунды

time.time()          # сейчас, timestamp
time.sleep(0.5)      # пауза
t0 = time.perf_counter(); ...; time.perf_counter() - t0
```
'''),
    quiz=[
        q('От какого момента отсчитывается Unix-время?',
            ['0001-01-01', '1970-01-01 00:00 UTC', '2000-01-01', 'Запуска компьютера'],
            1, 'Это «эпоха».'),
        q('Timestamp из API содержит 13 цифр. Что это значит?',
            ['Микросекунды', 'Миллисекунды', 'Ошибка', 'Секунды'],
            1, 'Раздели на 1000.'),
        q('Какую функцию использовать для замера длительности?',
            ['`time.time()`', '`time.perf_counter()`', '`datetime.now()`', '`time.sleep()`'],
            1, 'Она точная и монотонная.'),
    ],
),

# ---------- dt-api ----------
'dt-api': dict(
    full=t(r'''
## Зачем это нужно

В JSON нет типа «дата» — даты передают строками, почти всегда в ISO 8601. Тестировщику API нужно уметь отправлять даты в правильном формате и проверять даты в ответах: формат, порядок, пояс.

## json не умеет datetime

```python
import json
from datetime import datetime

data = {"created": datetime(2024, 3, 8, 12, 0)}
try:
    json.dumps(data)
except TypeError as e:
    print(e)
print(json.dumps(data, default=str))
print(json.dumps({"created": data["created"].isoformat()}))
```

- `json.dumps` не знает, как записать `datetime` → `TypeError`.
- `default=str` — для неизвестных объектов вызвать `str()`. Работает, но даёт пробел вместо `T`.
- Надёжнее явно вызывать `isoformat()`.
- Вывод: `Object of type datetime is not JSON serializable`, `{"created": "2024-03-08 12:00:00"}`, `{"created": "2024-03-08T12:00:00"}`.

## Своя функция default

```python
import json
from datetime import date, datetime

def encode(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    raise TypeError(f"не умею {type(value).__name__}")

order = {"id": 1, "day": date(2024, 3, 8), "at": datetime(2024, 3, 8, 9, 0)}
print(json.dumps(order, default=encode))
```

- `default=` получает каждый объект, который json не умеет записать. Возвращаем его JSON-представление.
- Для остальных типов выбрасываем `TypeError` — так json и ожидает.
- `datetime` — подкласс `date`, поэтому достаточно было бы проверки на `date`.
- Вывод: `{"id": 1, "day": "2024-03-08", "at": "2024-03-08T09:00:00"}`.

## Разбор дат из ответа

```python
import json
from datetime import datetime

body = '{"id": 7, "created_at": "2024-03-08T09:30:00Z", "updated_at": "2024-03-08T12:00:00+03:00"}'
user = json.loads(body)
created = datetime.fromisoformat(user["created_at"])
updated = datetime.fromisoformat(user["updated_at"])
print(created, updated)
print(updated - created, updated > created)
```

- После `json.loads` даты — это просто строки. Для сравнения их нужно разобрать.
- 12:00 по Москве (+03:00) = 09:00 UTC, то есть **раньше** 09:30 UTC.
- Вывод: `2024-03-08 09:30:00+00:00 2024-03-08 12:00:00+03:00`, `-1 day, 23:30:00 False`.
- `-1 day, 23:30:00` — так Python показывает минус 30 минут.

## Не сравнивай даты строками

```python
a = "2024-03-08T12:00:00+03:00"
b = "2024-03-08T10:00:00Z"
print(a > b)
```

- Строки сравниваются посимвольно: `"12" > "10"`. Но момент `a` (09:00 UTC) — **раньше** `b` (10:00 UTC).
- Строковое сравнение ISO-дат работает только при одинаковом формате и одинаковом поясе.
- Вывод: `True` — неправильный ответ!

## Отправка времени в API

```python
from datetime import datetime, timezone, timedelta

msk = timezone(timedelta(hours=3))
dt = datetime(2024, 3, 8, 15, 0, 0, 999, tzinfo=msk)
print(dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
```

- Частое требование API: UTC, без микросекунд, с `Z`.
- Вывод: `2024-03-08T12:00:00Z`.

## Типичные проверки в тестах

- Поле разбирается как ISO (`fromisoformat` не падает).
- У времени есть пояс (`dt.tzinfo is not None`).
- `updated_at >= created_at`.
- `created_at` близко к моменту запроса (± несколько секунд).

## Итог

- В JSON даты — ISO-строки: `isoformat()` при отправке, `fromisoformat()` при разборе.
- `json.dumps(obj, default=функция)` — свои типы.
- Сравнивай разобранные `datetime`, а не строки.
- Для API — UTC и `Z`.
'''),
    short=t(r'''
```py
import json
from datetime import date, datetime, timezone

json.dumps(data, default=str)            # быстро, но с пробелом
def encode(v):
    if isinstance(v, date): return v.isoformat()
    raise TypeError
json.dumps(data, default=encode)

dt = datetime.fromisoformat(resp["created_at"])
dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
# сравнивать datetime, НЕ строки
```
'''),
    quiz=[
        q('Что будет при `json.dumps({"d": datetime.now()})`?',
            ['Строка ISO', 'TypeError', 'Число', 'null'],
            1, 'json не умеет datetime без default.'),
        q('Почему опасно сравнивать ISO-строки дат?',
            ['Нельзя сравнивать строки', 'При разных поясах порядок строк не совпадает с порядком моментов', 'Это медленно', 'Это безопасно'],
            1, 'Сравнивай разобранные datetime.'),
        q('Как передать свою функцию преобразования в `json.dumps`?',
            ['`encoder=`', '`default=`', '`convert=`', '`cls=` обязательно'],
            1, 'default вызывается для неизвестных объектов.'),
    ],
),

# ---------- dt-testing ----------
'dt-testing': dict(
    full=t(r'''
## Зачем это нужно

Код, который сам вызывает `datetime.now()`, трудно тестировать: результат зависит от того, когда запущен тест. Такие тесты проходят днём и падают ночью, работают в феврале и ломаются 29-го числа. Разберём приёмы, которые делают время управляемым.

## Приём 1: время — параметр

```python
from datetime import datetime

def greeting(now):
    if now.hour < 12:
        return "Доброе утро"
    if now.hour < 18:
        return "Добрый день"
    return "Добрый вечер"

for h in [8, 13, 21]:
    print(greeting(datetime(2024, 3, 8, h)))
```

- Функция не узнаёт время сама, а **получает** его. В тесте передаём любой момент.
- Вывод: `Доброе утро`, `Добрый день`, `Добрый вечер`.

Чтобы вызывающему коду не приходилось передавать время всегда:

```python
from datetime import datetime

def is_expired(expires_at, now=None):
    if now is None:
        now = datetime.now()
    return now > expires_at

print(is_expired(datetime(2024, 3, 8, 12), now=datetime(2024, 3, 8, 13)))
```

- `now=None` и вычисление внутри. **Не пиши** `now=datetime.now()` в сигнатуре: значение по умолчанию вычисляется **один раз** при объявлении функции и потом не меняется.
- Вывод: `True`.

## Приём 2: поддельные часы

```python
from datetime import datetime, timedelta

class FakeClock:
    def __init__(self, start):
        self.current = start

    def now(self):
        return self.current

    def advance(self, **kwargs):
        self.current += timedelta(**kwargs)

class Session:
    def __init__(self, clock, ttl_minutes):
        self.clock = clock
        self.expires = clock.now() + timedelta(minutes=ttl_minutes)

    def is_active(self):
        return self.clock.now() < self.expires

clock = FakeClock(datetime(2024, 3, 8, 12, 0))
s = Session(clock, 30)
print(s.is_active())
clock.advance(minutes=30)
print(s.is_active())
```

- Класс получает объект «часы» (внедрение зависимости). В бою — настоящие часы, в тесте — `FakeClock`.
- `advance(minutes=30)` — «перемотать» время. Тест проверяет истечение сессии мгновенно, без `sleep`.
- `timedelta(**kwargs)` — передать именованные аргументы дальше.
- Вывод: `True`, `False`.

## Приём 3: граничные даты

```python
from datetime import date, timedelta

edge = [date(2024, 2, 28), date(2023, 12, 31), date(2024, 12, 31)]
for d in edge:
    print(d, "→", d + timedelta(days=1))
print(date(2024, 3, 1) - date(2024, 2, 1), date(2023, 3, 1) - date(2023, 2, 1))
```

- Обязательный набор дат для тестов: конец месяца, конец года, 29 февраля (и не високосный февраль), переход через полночь, понедельник и воскресенье.
- Вывод: `2024-02-28 → 2024-02-29`, `2023-12-31 → 2024-01-01`, `2024-12-31 → 2025-01-01`, `29 days, 0:00:00 28 days, 0:00:00`.

## Приём 4: «почти равно»

```python
from datetime import datetime

def assert_close(actual, expected, seconds=2):
    diff = abs((actual - expected).total_seconds())
    if diff > seconds:
        raise AssertionError(f"разница {int(diff)} с")

assert_close(datetime(2024, 3, 8, 12, 0, 1), datetime(2024, 3, 8, 12, 0, 0))
try:
    assert_close(datetime(2024, 3, 8, 11, 59, 50), datetime(2024, 3, 8, 12, 0, 0))
except AssertionError as e:
    print(e)
```

- Сервер ставит `created_at` сам — точного значения мы не знаем. Проверяем, что оно близко к моменту запроса.
- `abs(...)` — разница в любую сторону.
- Вывод: `разница 10 с`.

## Библиотеки

В реальных проектах время «замораживают» библиотеками `freezegun` (`@freeze_time("2024-03-08")`) или `time-machine`. Они подменяют `datetime.now()` на время теста. Но передавать время параметром — проще и работает без библиотек.

## Итог

- Не вызывай `now()` глубоко в логике — передавай время параметром или через объект-часы.
- `now=None` в сигнатуре, а не `now=datetime.now()`.
- Тестируй граничные даты.
- Время от сервера проверяй с допуском.
'''),
    short=t(r'''
```py
def f(..., now=None):          # НЕ now=datetime.now()
    if now is None:
        now = datetime.now()

class FakeClock:
    def __init__(self, start): self.current = start
    def now(self): return self.current
    def advance(self, **kw): self.current += timedelta(**kw)

# граничные даты: 28/29 фев, 31 дек, полночь, пн/вс
abs((a - b).total_seconds()) <= 2   # «почти равно»
```
'''),
    quiz=[
        q('Почему нельзя писать `def f(now=datetime.now())`?',
            ['SyntaxError', 'Значение вычислится один раз при объявлении', 'datetime нельзя по умолчанию', 'Будет naive-время'],
            1, 'Все вызовы получат одно и то же время.'),
        q('Зачем нужен `FakeClock` в тестах?',
            ['Чтобы тест работал быстрее и не зависел от реального времени', 'Чтобы изменить системные часы', 'Для часовых поясов', 'Ни зачем'],
            0, 'Время можно перематывать мгновенно.'),
        q('Какая дата — классическая граничная для тестов?',
            ['15 июня', '29 февраля', '10 октября', '5 мая'],
            1, 'Бывает не каждый год.'),
    ],
),

}
