"""Теория модуля «Даты и их запись» темы «Дата и время».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- dt-date ----------
'dt-date': dict(
    full=t(r'''
## Зачем это нужно

Даты повсюду: срок действия токена, дата заказа, время создания записи в API, имя файла отчёта. Хранить дату строкой `"08.03.2024"` неудобно: её не сравнить правильно, к ней не прибавить неделю. В Python для этого есть модуль `datetime` со специальными классами.

## Модуль datetime

В стандартном модуле `datetime` несколько классов:

- `date` — только дата (год, месяц, день);
- `time` — только время (часы, минуты, секунды);
- `datetime` — дата и время вместе;
- `timedelta` — промежуток времени («3 дня», «2 часа»);
- `timezone` — часовой пояс.

Внимание: модуль и один из классов называются одинаково — `datetime`. Поэтому обычно пишут `from datetime import date, datetime`.

## Создание даты

```python
from datetime import date

d = date(2024, 3, 8)
print(d)
print(d.year, d.month, d.day)
print(type(d).__name__)
```

- `date(год, месяц, день)` — порядок всегда «от большего к меньшему».
- `print(d)` показывает дату в международном формате **ISO**: `ГГГГ-ММ-ДД`.
- `year`, `month`, `day` — атрибуты-числа.
- Вывод: `2024-03-08`, `2024 3 8`, `date`.

## Сегодняшняя дата

```py
date.today()      # сегодняшняя дата, например date(2026, 9, 28)
```

- Результат меняется каждый день, поэтому в примерах и тестах мы используем **фиксированные** даты. Как тестировать код, который зависит от «сегодня», — в последнем уроке темы.

## День недели

```python
from datetime import date

d = date(2024, 3, 8)
print(d.weekday(), d.isoweekday())
days = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
print(days[d.weekday()])
print(date(2024, 3, 10).weekday() >= 5)
```

- `weekday()` — номер дня недели с нуля: понедельник `0`, …, воскресенье `6`. Удобно как индекс списка.
- `isoweekday()` — «человеческая» нумерация: понедельник `1`, …, воскресенье `7`.
- `weekday() >= 5` — выходной (суббота 5 или воскресенье 6).
- Вывод: `4 5`, `пт`, `True`.

## Сравнение и сортировка

```python
from datetime import date

a = date(2024, 1, 15)
b = date(2023, 12, 31)
print(a > b, a == date(2024, 1, 15))
dates = [date(2024, 5, 1), date(2023, 1, 1), date(2024, 1, 1)]
print(sorted(dates)[0], max(dates))
```

- Даты сравниваются по времени: более поздняя — «больше».
- Работают `sorted`, `min`, `max`.
- Вывод: `True True`, `2023-01-01 2024-05-01`.

## Несуществующая дата

```python
from datetime import date

try:
    date(2023, 2, 29)
except ValueError as e:
    print(e)
```

- 2023 — не високосный год, 29 февраля нет → `ValueError`. Так же для 31 апреля или 13-го месяца.
- Вывод: `day is out of range for month`.
- Это удобный способ проверить, существует ли дата: попробовать создать и поймать ошибку.

## Даты неизменяемы

Объект `date` нельзя изменить: `d.day = 5` → `AttributeError`. Все операции (сдвиг, замена дня) возвращают **новый** объект. Поэтому даты можно смело класть в множества и использовать как ключи словаря.

## Итог

- `from datetime import date`; `date(2024, 3, 8)`; `date.today()`.
- `.year`, `.month`, `.day`; `weekday()` (пн = 0), `isoweekday()` (пн = 1).
- Даты сравниваются и сортируются.
- Несуществующая дата → `ValueError`.
'''),
    short=t(r'''
```py
from datetime import date

d = date(2024, 3, 8)       # год, месяц, день
date.today()               # сегодня
d.year, d.month, d.day     # 2024 3 8
d.weekday()                # 4  (пн=0 … вс=6)
d.isoweekday()             # 5  (пн=1 … вс=7)
d.weekday() >= 5           # выходной?
min(dates), sorted(dates)
date(2023, 2, 29)          # ValueError
```
'''),
    quiz=[
        q('Что вернёт `date(2024, 3, 11).weekday()`, если 11 марта 2024 — понедельник?',
            ['1', '0', '7', '6'],
            1, 'weekday() считает с нуля.'),
        q('Что будет при `date(2023, 2, 29)`?',
            ['date(2023, 3, 1)', 'ValueError', 'None', 'date(2023, 2, 28)'],
            1, 'В 2023 году нет 29 февраля.'),
        q('Как выглядит `print(date(2024, 3, 8))`?',
            ['08.03.2024', '2024-03-08', '3/8/2024', 'date(2024, 3, 8)'],
            1, 'Формат ISO: год-месяц-день.'),
    ],
),

# ---------- dt-datetime ----------
'dt-datetime': dict(
    full=t(r'''
## Зачем это нужно

Часто нужна не только дата, но и время: когда создан заказ, когда упал тест, до какого момента действует токен. Для этого есть `datetime` (дата + время) и `time` (только время).

## datetime

```python
from datetime import datetime

dt = datetime(2024, 3, 8, 14, 30, 5)
print(dt)
print(dt.hour, dt.minute, dt.second)
print(dt.date(), dt.time())
```

- `datetime(год, месяц, день, час, минута, секунда, микросекунда)` — всё после дня необязательно (по умолчанию 0).
- Атрибуты: `year`, `month`, `day`, `hour`, `minute`, `second`, `microsecond`.
- `dt.date()` — только дата (`date`), `dt.time()` — только время (`time`).
- Вывод: `2024-03-08 14:30:05`, `14 30 5`, `2024-03-08 14:30:05`.

## Текущий момент

```py
datetime.now()    # текущие дата и время на компьютере
```

- Как и `date.today()`, результат меняется — в тестах так не делают. Подробнее — в последнем уроке.

## replace: изменить часть

```python
from datetime import datetime

dt = datetime(2024, 3, 8, 14, 30)
print(dt.replace(hour=9, minute=0))
print(dt)
```

- `datetime` неизменяем. `replace(...)` возвращает **новый** объект с заменёнными полями, остальные поля копируются.
- Исходный `dt` не изменился.
- Вывод: `2024-03-08 09:00:00`, `2024-03-08 14:30:00`.

## combine: дата + время

```python
from datetime import datetime, date, time

start = datetime.combine(date(2024, 1, 1), time(10, 15))
print(start)
midnight = datetime.combine(date(2024, 1, 1), time.min)
print(midnight)
```

- `time(часы, минуты, секунды)` — объект «время суток».
- `datetime.combine(дата, время)` — склеить их.
- `time.min` — `00:00:00`, `time.max` — `23:59:59.999999`.
- Вывод: `2024-01-01 10:15:00`, `2024-01-01 00:00:00`.

## Микросекунды

```python
from datetime import datetime

dt = datetime(2024, 3, 8, 14, 30, 45, 123456)
print(dt)
print(dt.replace(microsecond=0))
```

- Микросекунда — миллионная доля секунды. Они часто приходят из API и мешают сравнивать.
- `replace(microsecond=0)` — отбросить их.
- Вывод: `2024-03-08 14:30:45.123456`, `2024-03-08 14:30:45`.

## Сравнение времени

```python
from datetime import datetime, time

dt = datetime(2024, 3, 8, 17, 59)
print(time(9, 0) <= dt.time() < time(18, 0))
print(dt.weekday() < 5)
```

- Объекты `time` сравниваются между собой — удобно проверять «рабочие часы».
- Двойное сравнение `a <= x < b` работает и здесь.
- Вывод: `True`, `True`.

## Группировка по дням

```python
from datetime import datetime

events = [datetime(2024, 3, 9, 10), datetime(2024, 3, 8, 15), datetime(2024, 3, 8, 9, 30)]
by_day = {}
for dt in sorted(events):
    by_day.setdefault(dt.date(), []).append(dt.time())
for day, times in by_day.items():
    print(day, [t.strftime("%H:%M") for t in times])
```

- `dt.date()` — ключ группы. `setdefault` создаёт пустой список для нового ключа.
- `strftime("%H:%M")` — время в виде «часы:минуты» (подробно — в следующем уроке).
- Вывод: `2024-03-08 ['09:30', '15:00']`, `2024-03-09 ['10:00']`.

## Итог

- `datetime(год, мес, день, ч, мин, сек, мкс)`; `datetime.now()`.
- `.date()`, `.time()`; `time(ч, мин)`, `time.min`, `time.max`.
- `replace(...)` — новый объект; `combine(date, time)`.
- `datetime` и `time` сравниваются.
'''),
    short=t(r'''
```py
from datetime import datetime, date, time

dt = datetime(2024, 3, 8, 14, 30, 5)
datetime.now()
dt.hour, dt.minute, dt.second, dt.microsecond
dt.date(), dt.time()
dt.replace(hour=0, minute=0, second=0, microsecond=0)
datetime.combine(date(2024, 1, 1), time(10, 15))
time.min, time.max           # 00:00, 23:59:59.999999
time(9) <= dt.time() < time(18)
```
'''),
    quiz=[
        q('Что делает `dt.replace(hour=9)`?',
            ['Меняет dt', 'Возвращает новый datetime с часом 9', 'Ошибка — datetime неизменяем', 'Возвращает None'],
            1, 'Исходный объект остаётся прежним.'),
        q('Как получить только дату из `datetime`?',
            ['`dt.day`', '`dt.date()`', '`date(dt)`', '`dt.today()`'],
            1, '`dt.day` — только число месяца.'),
        q('Как склеить объекты `date` и `time`?',
            ['`d + t`', '`datetime.combine(d, t)`', '`datetime(d, t)`', '`d.time(t)`'],
            1, 'combine — метод класса datetime.'),
    ],
),

# ---------- dt-format ----------
'dt-format': dict(
    full=t(r'''
## Зачем это нужно

Для людей и для API даты пишут в разных форматах: `08.03.2024`, `2024-03-08T09:05:00`, `8 марта 2024`. Превратить объект даты в строку нужного вида помогает `strftime` (string format time) и `isoformat`.

## strftime и коды формата

```python
from datetime import datetime

dt = datetime(2024, 3, 8, 9, 5, 7)
print(dt.strftime("%d.%m.%Y"))
print(dt.strftime("%H:%M:%S"))
print(dt.strftime("%Y-%m-%d %H:%M"))
print(dt.strftime("%d/%m/%y"))
```

- `strftime(шаблон)` — подставляет части даты вместо кодов с `%`; всё остальное (точки, пробелы, слеши) копируется как есть.
- Главные коды:
  - `%Y` — год четырьмя цифрами, `%y` — двумя;
  - `%m` — месяц `01`–`12`;
  - `%d` — день `01`–`31`;
  - `%H` — час `00`–`23`, `%M` — минуты, `%S` — секунды.
- Числовые коды всегда дают **две цифры** с ведущим нулём.
- Внимание: `%m` — месяц, `%M` — минуты. Перепутать их — частая ошибка.
- Вывод: `08.03.2024`, `09:05:07`, `2024-03-08 09:05`, `08/03/24`.

## Формат прямо в f-строке

```python
from datetime import datetime

dt = datetime(2024, 3, 8, 9, 5)
print(f"{dt:%d.%m.%Y}", f"{dt:%H:%M}")
print(f"[{dt:%Y-%m-%d %H:%M:%S}] ERROR: упал тест")
```

- После двоеточия в `{}` можно написать тот же шаблон — это короче, чем `strftime`.
- Вывод: `08.03.2024 09:05`, `[2024-03-08 09:05:00] ERROR: упал тест`.

## isoformat

```python
from datetime import datetime, date

dt = datetime(2024, 3, 8, 9, 5, 7, 123456)
print(dt.isoformat())
print(dt.isoformat(timespec="seconds"))
print(dt.isoformat(sep=" ", timespec="minutes"))
print(date(2024, 3, 8).isoformat())
```

- **ISO 8601** — международный стандарт записи дат: `ГГГГ-ММ-ДДTЧЧ:ММ:СС`. Буква `T` разделяет дату и время. Его используют почти все API и JSON.
- `timespec="seconds"` — без микросекунд; `"minutes"` — до минут.
- `sep=" "` — пробел вместо `T`.
- Вывод: `2024-03-08T09:05:07.123456`, `2024-03-08T09:05:07`, `2024-03-08 09:05`, `2024-03-08`.

## Названия дней и месяцев

```python
from datetime import date

d = date(2024, 3, 8)
print(d.strftime("%A, %B"))
print(d.strftime("%a %b"))
print(d.strftime("%j"), d.strftime("%w"))
```

- `%A` / `%a` — день недели полностью / сокращённо, `%B` / `%b` — месяц.
- Язык названий зависит от настроек системы (**локали**); на серверах обычно английский.
- `%j` — номер дня в году, `%w` — день недели (воскресенье `0`).
- Вывод: `Friday, March`, `Fri Mar`, `068 5`.

Для русских названий надёжнее свой список:

```python
from datetime import date

MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня",
          "июля", "августа", "сентября", "октября", "ноября", "декабря"]

d = date(2024, 3, 8)
print(f"{d.day} {MONTHS[d.month - 1]} {d.year}")
```

- `d.day` — число без ведущего нуля; `d.month - 1` — индекс в списке с нуля.
- Вывод: `8 марта 2024`.

## Имя файла из даты

```python
from datetime import datetime

dt = datetime(2024, 3, 8, 9, 5)
print(f"report_{dt:%Y-%m-%d_%H-%M}.html")
```

- Формат «год-месяц-день» удобен: такие имена сортируются по алфавиту в правильном порядке.
- Двоеточия в именах файлов запрещены в Windows — используем дефис.
- Вывод: `report_2024-03-08_09-05.html`.

## Итог

- `dt.strftime("%d.%m.%Y %H:%M")` или `f"{dt:%d.%m.%Y}"`.
- `%Y %m %d %H %M %S` — год, месяц, день, час, минуты, секунды; `%%` — знак процента.
- `isoformat()` — стандарт для API; `timespec="seconds"`.
- `%A`, `%B` зависят от локали — для русского языка свой список.
'''),
    short=t(r'''
```py
dt.strftime("%d.%m.%Y")         # 08.03.2024
dt.strftime("%H:%M:%S")         # 09:05:07
f"{dt:%Y-%m-%d %H:%M}"          # 2024-03-08 09:05
dt.isoformat()                  # 2024-03-08T09:05:07.123456
dt.isoformat(timespec="seconds")
# %Y год  %y год(2)  %m месяц  %d день
# %H час  %M минуты  %S секунды
# %A/%a день нед.  %B/%b месяц  %j день года  %% — %
```
'''),
    quiz=[
        q('Какой код означает минуты?',
            ['%m', '%M', '%i', '%min'],
            1, '%m — месяц, %M — минуты.'),
        q('Что выведет `date(2024, 3, 8).strftime("%d.%m")`?',
            ['8.3', '08.03', '03.08', '8.03'],
            1, 'Числовые коды дают две цифры.'),
        q('Какой формат дат стандартен для API и JSON?',
            ['дд.мм.гггг', 'ISO 8601: гггг-мм-ддTчч:мм:сс', 'мм/дд/гггг', 'Unix-строка'],
            1, 'Его дают isoformat() и понимают почти все системы.'),
    ],
),

# ---------- dt-parse ----------
'dt-parse': dict(
    full=t(r'''
## Зачем это нужно

Обратная задача: из строки получить объект даты. Даты приходят строками отовсюду — из форм, CSV-файлов, логов, JSON-ответов API. Чтобы сравнивать и считать, их нужно **разобрать** (распарсить).

## strptime: строка + шаблон

```python
from datetime import datetime

dt = datetime.strptime("08.03.2024 14:30", "%d.%m.%Y %H:%M")
print(dt)
print(repr(dt))
print(datetime.strptime("2024-03-08", "%Y-%m-%d").date())
```

- `datetime.strptime(строка, шаблон)` — string **parse** time. Коды те же, что в `strftime`.
- Шаблон должен **точно** описывать строку: каждая точка, пробел и двоеточие.
- Возвращает всегда `datetime`; если нужна дата — `.date()`.
- `repr` показывает, как объект создать в коде.
- Вывод: `2024-03-08 14:30:00`, `datetime.datetime(2024, 3, 8, 14, 30)`, `2024-03-08`.

## fromisoformat: для ISO-строк

```python
from datetime import datetime, date

print(date.fromisoformat("2024-03-08"))
print(datetime.fromisoformat("2024-03-08T14:30:00"))
print(datetime.fromisoformat("2024-03-08 14:30"))
print(datetime.fromisoformat("2024-03-08T14:30:00Z"))
```

- `fromisoformat` разбирает ISO-строки без шаблона. Быстрее и проще, чем `strptime`.
- Понимает и `T`, и пробел, секунды необязательны.
- `Z` в конце — «Zulu time», то есть UTC. Результат получает часовой пояс `+00:00` (о поясах — в модуле 3).
- Вывод: `2024-03-08`, `2024-03-08 14:30:00`, `2024-03-08 14:30:00`, `2024-03-08 14:30:00+00:00`.

## Ошибки разбора

```python
from datetime import datetime

tests = ["31.12.2024", "2024-12-31", "32.01.2024", "1.2.2024"]
for text in tests:
    try:
        print(datetime.strptime(text, "%d.%m.%Y").date())
    except ValueError:
        print("ошибка:", text)
```

- Строка не подходит под шаблон или дата не существует → `ValueError`.
- `strptime` разрешает числа **без** ведущего нуля (`1.2.2024`).
- Вывод: `2024-12-31`, `ошибка: 2024-12-31`, `ошибка: 32.01.2024`, `2024-02-01`.

## Несколько форматов

```python
from datetime import datetime

FORMATS = ["%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"]

def parse_any(text):
    for fmt in FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    return None

print(parse_any("08/03/2024"), parse_any("вчера"))
```

- Пробуем форматы по очереди; первый подошедший — возвращаем.
- `pass` в `except` — «ошибка ожидаема, идём дальше».
- Вывод: `2024-03-08 None`.

## Перевод из формата в формат

```python
from datetime import date

text = "2024-03-08"
print(date.fromisoformat(text).strftime("%d.%m.%Y"))
```

- Правильный путь: строка → объект → строка. Не режь строки вручную срезами — легко ошибиться.
- Вывод: `08.03.2024`.

## Разбор строки лога

```python
from datetime import datetime

line = "2024-03-08 14:30:05 ERROR база недоступна"
day, clock, level, message = line.split(" ", 3)
dt = datetime.strptime(f"{day} {clock}", "%Y-%m-%d %H:%M:%S")
print(dt.hour, level, message)
```

- `split(" ", 3)` — разрезать не больше трёх раз: сообщение с пробелами останется целым.
- Вывод: `14 ERROR база недоступна`.

## Итог

- `datetime.strptime(s, "%d.%m.%Y")` — разбор по шаблону.
- `date.fromisoformat(s)`, `datetime.fromisoformat(s)` — для ISO, понимает `Z`.
- Неразборная строка → `ValueError`: лови его для проверки формата.
- Перевод форматов: строка → объект → строка.
'''),
    short=t(r'''
```py
from datetime import datetime, date

datetime.strptime("08.03.2024 14:30", "%d.%m.%Y %H:%M")
datetime.strptime("08.03.2024", "%d.%m.%Y").date()
date.fromisoformat("2024-03-08")
datetime.fromisoformat("2024-03-08T14:30:00Z")   # +00:00

try:
    datetime.strptime(text, fmt)
except ValueError:
    ...   # не тот формат или нет такой даты
```
'''),
    quiz=[
        q('Что вернёт `datetime.strptime("08.03.2024", "%d.%m.%Y")`?',
            ['date', 'datetime с временем 00:00', 'Строку', 'Ошибку'],
            1, 'strptime всегда возвращает datetime.'),
        q('Что будет, если строка не подходит под шаблон?',
            ['None', 'ValueError', 'TypeError', 'Пустая дата'],
            1, 'Так и проверяют формат.'),
        q('Что означает `Z` в конце ISO-строки?',
            ['Ноль секунд', 'Время UTC', 'Конец строки', 'Зимнее время'],
            1, 'Zulu time — всемирное время.'),
    ],
),

}
