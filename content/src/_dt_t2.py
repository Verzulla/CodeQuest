"""Теория модуля «Арифметика дат» темы «Дата и время».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- dt-timedelta ----------
'dt-timedelta': dict(
    full=t(r'''
## Зачем это нужно

«Через 3 дня», «неделю назад», «длительность 2 часа 15 минут» — это не момент, а **промежуток** времени. В Python для него есть класс `timedelta`. Его можно прибавлять к датам и вычитать из них, складывать, умножать и сравнивать.

## Сдвиг даты

```python
from datetime import date, timedelta

d = date(2024, 2, 27)
print(d + timedelta(days=3))
print(d - timedelta(weeks=1))
```

- `timedelta(days=..., hours=..., minutes=..., seconds=..., weeks=...)` — все параметры именованные и необязательные.
- `дата + timedelta` — новая дата. Python сам учитывает длину месяцев и високосные годы: 2024 — високосный, поэтому 27 февраля + 3 дня = 1 марта.
- Вывод: `2024-03-01`, `2024-02-20`.

## Как timedelta выглядит и хранится

```python
from datetime import timedelta

print(timedelta(days=1, hours=5))
print(timedelta(hours=36))
td = timedelta(days=2, hours=3, minutes=30)
print(td.days, td.seconds)
print(td.total_seconds())
print(td.total_seconds() / 3600)
```

- Внутри хранятся только **дни**, **секунды** (меньше суток) и микросекунды. Часы и минуты переводятся в секунды, лишние сутки — в дни: 36 часов = 1 день и 12 часов.
- `td.seconds` — только «хвост» меньше суток, **не** все секунды! Частая ошибка.
- `td.total_seconds()` — вся длительность в секундах (дробное число). Чтобы получить часы — дели на 3600.
- Вывод: `1 day, 5:00:00`, `1 day, 12:00:00`, `2 12600`, `185400.0`, `51.5`.

```viz
{"type": "paths", "auto": true, "title": "Сдвиги через timedelta: календарь Python считает сам", "cases": [{"label": "days=1", "code": "from datetime import datetime, timedelta\nstart = datetime(2026, 1, 30, 22, 0)\nprint(start + timedelta(days=1))", "note": "Плюс сутки."}, {"label": "days=2", "code": "from datetime import datetime, timedelta\nstart = datetime(2026, 1, 30, 22, 0)\nprint(start + timedelta(days=2))", "note": "Перешли через конец января — 1 февраля."}, {"label": "hours=5", "code": "from datetime import datetime, timedelta\nstart = datetime(2026, 1, 30, 22, 0)\nprint(start + timedelta(hours=5))", "note": "Плюс 5 часов — уже следующий день."}, {"label": "weeks=1", "code": "from datetime import datetime, timedelta\nstart = datetime(2026, 1, 30, 22, 0)\nprint(start + timedelta(weeks=1))", "note": "Неделя = 7 дней."}, {"label": "minutes=-90", "code": "from datetime import datetime, timedelta\nstart = datetime(2026, 1, 30, 22, 0)\nprint(start + timedelta(minutes=-90))", "note": "Отрицательный промежуток — назад во времени."}, {"label": "days=30", "code": "from datetime import datetime, timedelta\nstart = datetime(2026, 1, 30, 22, 0)\nprint(start + timedelta(days=30))", "note": "В феврале 2026 года 28 дней — Python это учёл."}]}
```

## Арифметика промежутков

```python
from datetime import datetime, timedelta

start = datetime(2024, 3, 8, 23, 30)
print(start + timedelta(minutes=45))
step = timedelta(minutes=20)
print(step * 3, step / 2)
print(timedelta(hours=2) // timedelta(minutes=25))
print(timedelta(minutes=90) > timedelta(hours=1))
```

- Прибавление минут может перейти на следующие сутки — это учитывается.
- `timedelta * число`, `timedelta / число` — растянуть или сжать промежуток.
- `timedelta // timedelta` — сколько целых раз один промежуток помещается в другом.
- Промежутки сравниваются.
- Вывод: `2024-03-09 00:15:00`, `1:00:00 0:10:00`, `4`, `True`.

## Расписание

```python
from datetime import datetime, timedelta

start = datetime(2024, 3, 8, 9, 0)
step = timedelta(minutes=20)
for i in range(3):
    print((start + step * i).strftime("%H:%M"))
```

- `step * i` — 0, 20, 40 минут от начала.
- Вывод: `09:00`, `09:20`, `09:40`.

## Длительность в виде ЧЧ:ММ:СС

```python
from datetime import timedelta

td = timedelta(hours=26, minutes=5, seconds=3)
total = int(td.total_seconds())
hours, rest = divmod(total, 3600)
minutes, seconds = divmod(rest, 60)
print(f"{hours:02}:{minutes:02}:{seconds:02}")
```

- `divmod(a, b)` — пара (целая часть, остаток).
- `:02` — дополнить число нулём до двух цифр.
- `str(td)` дал бы `1 day, 2:05:03` — не всегда то, что нужно.
- Вывод: `26:05:03`.

## Итог

- `timedelta(days=, hours=, minutes=, seconds=, weeks=)`.
- `дата ± timedelta` → дата; длина месяцев учитывается.
- `.days`, `.seconds` (только хвост!), `.total_seconds()` (всё).
- Промежутки складываются, умножаются, делятся и сравниваются.
- Месяцев и лет в `timedelta` нет — они разной длины.
'''),
    short=t(r'''
```py
from datetime import timedelta

d + timedelta(days=3)
dt - timedelta(hours=2, minutes=30)
timedelta(weeks=1)
td.days, td.seconds        # seconds — только хвост < суток
td.total_seconds()         # всё в секундах
td.total_seconds() / 3600  # часы
step * 3, step / 2, td1 // td2
h, rest = divmod(int(td.total_seconds()), 3600)
```
'''),
    quiz=[
        q('Что вернёт `timedelta(hours=36).seconds`?',
            ['129600', '43200', '36', '1.5'],
            1, 'Полные сутки уходят в days, seconds — остаток 12 часов.'),
        q('Как получить длительность `td` в часах?',
            ['`td.hours`', '`td.total_seconds() / 3600`', '`td.seconds / 60`', '`td.days * 24`'],
            1, 'Атрибута hours нет.'),
        q('Можно ли написать `timedelta(months=1)`?',
            ['Да', 'Нет — месяцы разной длины', 'Только в Python 3.12', 'Да, это 30 дней'],
            1, 'TypeError: неизвестный аргумент months.'),
    ],
),

# ---------- dt-diff ----------
'dt-diff': dict(
    full=t(r'''
## Зачем это нужно

Сколько дней до дедлайна? Сколько длилась сессия? Сколько лет пользователю? Просрочен ли заказ? Всё это — **разность** двух дат.

## Разность дат — timedelta

```python
from datetime import date, datetime

delta = date(2024, 12, 31) - date(2024, 1, 1)
print(delta, delta.days)
d2 = datetime(2024, 3, 8, 18, 0) - datetime(2024, 3, 8, 9, 30)
print(d2, d2.total_seconds() / 3600)
print(date(2024, 1, 1) - date(2024, 1, 10))
```

- `поздняя - ранняя` → положительный `timedelta`; наоборот — отрицательный.
- Для `date` интересны `.days`, для `datetime` — чаще `.total_seconds()`.
- Вывод: `365 days, 0:00:00 365`, `8:30:00 8.5`, `-9 days, 0:00:00`.

## Что можно, а что нельзя

```python
from datetime import date, datetime

try:
    date(2024, 1, 1) + date(2024, 1, 2)
except TypeError:
    print("даты нельзя складывать")
try:
    datetime(2024, 1, 1) - date(2024, 1, 1)
except TypeError:
    print("datetime и date нельзя вычитать")
print(datetime(2024, 1, 2).date() - date(2024, 1, 1))
```

- `дата + дата` не имеет смысла → `TypeError`.
- `datetime - date` — разные типы → `TypeError`. Приведи к одному: `.date()`.
- Можно: `дата - дата`, `дата ± timedelta`, `timedelta ± timedelta`.
- Вывод: `даты нельзя складывать`, `datetime и date нельзя вычитать`, `1 day, 0:00:00`.

## Дней до события

```python
from datetime import date

today = date(2024, 12, 25)
new_year = date(2025, 1, 1)
print((new_year - today).days)
```

- Вывод: `7`.

## Возраст

```python
from datetime import date

def age(born, today):
    years = today.year - born.year
    if (today.month, today.day) < (born.month, born.day):
        years -= 1
    return years

print(age(date(2000, 5, 20), date(2024, 5, 19)))
print(age(date(2000, 5, 20), date(2024, 5, 20)))
```

- Разница годов, минус 1, если день рождения в этом году ещё не наступил.
- `(месяц, день) < (месяц, день)` — сравнение кортежей: сначала месяц, при равенстве — день.
- `дни // 365` — неточно из-за високосных лет, так возраст не считают.
- Вывод: `23`, `24`.

## Просрочено ли

```python
from datetime import datetime

deadline = datetime(2024, 3, 8, 18, 0)
now = datetime(2024, 3, 7, 15, 30)
print(now > deadline)
left = deadline - now
print(int(left.total_seconds() // 3600), "ч")
```

- Сравнение — самый простой способ проверить просрочку.
- Остаток в целых часах: `total_seconds() // 3600`.
- Вывод: `False`, `26 ч`.

## Промежутки между событиями

```python
from datetime import date

ds = sorted([date(2024, 1, 10), date(2024, 1, 1), date(2024, 2, 1)])
gaps = [(b - a).days for a, b in zip(ds, ds[1:])]
print(gaps, max(gaps))
```

- `zip(ds, ds[1:])` — пары соседних элементов.
- Вывод: `[9, 22] 22`.

## Итог

- `дата - дата` → `timedelta`; `.days` или `.total_seconds()`.
- Нельзя: `дата + дата`, `datetime - date`.
- Возраст — через годы и сравнение `(месяц, день)`, не делением на 365.
- «Просрочено» — просто `now > deadline`.
'''),
    short=t(r'''
```py
(date2 - date1).days                 # дней между
(dt2 - dt1).total_seconds() / 3600   # часов между
now > deadline                       # просрочено?
dt.date() - d                        # привести к одному типу

def age(born, today):
    y = today.year - born.year
    if (today.month, today.day) < (born.month, born.day):
        y -= 1
    return y
```
'''),
    quiz=[
        q('Что получится при вычитании двух `date`?',
            ['date', 'int', 'timedelta', 'Ошибка'],
            2, 'Разность дат — промежуток.'),
        q('Что будет при `datetime(2024,1,1) - date(2024,1,1)`?',
            ['0 дней', 'TypeError', 'None', 'date'],
            1, 'Нужно привести к одному типу.'),
        q('Почему возраст нельзя считать как `дни // 365`?',
            ['Медленно', 'Високосные годы дают ошибку на границе', 'Нельзя делить timedelta', 'Можно, это точно'],
            1, 'Около дня рождения результат может быть на год неверным.'),
    ],
),

# ---------- dt-calendar ----------
'dt-calendar': dict(
    full=t(r'''
## Зачем это нужно

Месяцы бывают по 28, 29, 30 и 31 дню, а `timedelta` не умеет прибавлять «месяц». Последний день месяца, високосный ли год, «через месяц» — для этого есть модуль `calendar` и немного арифметики.

## Високосные годы и длина месяца

```python
import calendar

print(calendar.isleap(2024), calendar.isleap(1900), calendar.isleap(2000))
print(calendar.monthrange(2024, 2))
print(calendar.monthrange(2023, 2)[1])
```

- Високосный год: делится на 4, но не на 100 — или делится на 400. Поэтому 1900 — нет, 2000 — да.
- `calendar.monthrange(год, месяц)` возвращает кортеж: (день недели 1-го числа, количество дней). Нас обычно интересует второй элемент.
- День недели в Python 3.12 выводится как `calendar.THURSDAY` — это именованная константа, равная `3` (нумерация как у `weekday()`).
- Вывод: `True False True`, `(calendar.THURSDAY, 29)`, `28`.

## Почему нет «плюс месяц»

```python
from datetime import date, timedelta

d = date(2024, 1, 31)
print(d + timedelta(days=30))
try:
    print(d.replace(month=2))
except ValueError as e:
    print("ошибка:", e)
```

- «30 дней» ≠ «месяц»: из 31 января получилось 1 марта.
- `replace(month=2)` для 31-го числа ломается: 31 февраля нет.
- Вывод: `2024-03-01`, `ошибка: day is out of range for month`.

## Первый и последний день месяца

```python
import calendar
from datetime import date

d = date(2024, 2, 14)
first = d.replace(day=1)
last = d.replace(day=calendar.monthrange(d.year, d.month)[1])
print(first, last)
```

- Первый день — всегда `day=1`.
- Последний — количество дней в месяце.
- Вывод: `2024-02-01 2024-02-29`.

## Прибавить месяцы

```python
import calendar
from datetime import date

def add_months(d, n):
    index = d.year * 12 + (d.month - 1) + n
    year, month = divmod(index, 12)
    month += 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)

print(add_months(date(2024, 1, 31), 1))
print(add_months(date(2024, 11, 15), 3))
print(add_months(date(2024, 1, 10), -1))
```

Что делает каждая строка:

- `d.year * 12 + (d.month - 1)` — «номер месяца от начала летоисчисления». Январь 2024 → `24288`. Месяц уменьшаем на 1, чтобы нумерация шла с нуля.
- `+ n` — сдвигаем на `n` месяцев (можно назад).
- `divmod(index, 12)` — обратно в год и месяц (с нуля), затем `month += 1`.
- `min(d.day, дней_в_месяце)` — если дня нет (31 февраля), берём последний.
- Вывод: `2024-02-29`, `2025-02-15`, `2023-12-10`.
- В сторонней библиотеке `dateutil` это делает `relativedelta(months=1)`.

## Названия из calendar

```python
import calendar

print(calendar.month_name[3], calendar.month_abbr[2], calendar.day_abbr[0])
```

- `month_name[1..12]`, `day_name[0..6]` — названия на языке системы (обычно английском). Индекс 0 у месяцев — пустая строка.
- Вывод: `March Feb Mon`.

## Итог

- `calendar.isleap(год)`; `calendar.monthrange(год, мес)[1]` — дней в месяце.
- Первый день — `replace(day=1)`, последний — `replace(day=дней)`.
- Сдвиг на месяцы: через номер месяца и `divmod`, с обрезкой дня.
- `timedelta(days=30)` — не месяц.
'''),
    short=t(r'''
```py
import calendar

calendar.isleap(2024)                 # True
calendar.monthrange(2024, 2)          # (THURSDAY=3, 29)
days = calendar.monthrange(y, m)[1]   # дней в месяце
d.replace(day=1)                      # первый день
d.replace(day=days)                   # последний

# +n месяцев
i = d.year * 12 + d.month - 1 + n
y, m = divmod(i, 12); m += 1
date(y, m, min(d.day, calendar.monthrange(y, m)[1]))
```
'''),
    quiz=[
        q('Високосный ли 1900 год?',
            ['Да, делится на 4', 'Нет, делится на 100 и не делится на 400', 'Да, делится на 100', 'Нет, не делится на 4'],
            1, 'Правило: /4, кроме /100, но включая /400.'),
        q('Что возвращает `calendar.monthrange(2024, 2)[1]`?',
            ['2', '29', '28', '3'],
            1, 'Второй элемент — количество дней.'),
        q('Что будет при `date(2024, 1, 31).replace(month=2)`?',
            ['date(2024, 2, 29)', 'ValueError', 'date(2024, 3, 2)', 'date(2024, 2, 28)'],
            1, '31 февраля не существует.'),
    ],
),

# ---------- dt-ranges ----------
'dt-ranges': dict(
    full=t(r'''
## Зачем это нужно

Отчёт за каждый день недели, количество рабочих дней в месяце, срок «5 рабочих дней», границы недели — это перебор **диапазона дат**. `range` для дат не работает, но его легко заменить.

## Список дат подряд

```python
from datetime import date, timedelta

start = date(2024, 2, 27)
end = date(2024, 3, 1)
count = (end - start).days + 1
days = [start + timedelta(days=i) for i in range(count)]
print([d.isoformat() for d in days])
```

- `(end - start).days + 1` — сколько дат в диапазоне включительно.
- `start + timedelta(days=i)` — i-й день от начала.
- Вывод: `['2024-02-27', '2024-02-28', '2024-02-29', '2024-03-01']`.

## Цикл while по датам

```python
from datetime import date, timedelta

d = date(2024, 3, 7)
end = date(2024, 3, 12)
while d <= end:
    if d.weekday() < 5:
        print(d.strftime("%d.%m"), end=" ")
    d += timedelta(days=1)
print()
```

- `d += timedelta(days=1)` — следующий день (новый объект кладётся в `d`).
- `weekday() < 5` — только будни.
- Вывод: `07.03 08.03 11.03 12.03`.

## Прибавить рабочие дни

```python
from datetime import date, timedelta

def add_workdays(start, n):
    d = start
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d

print(add_workdays(date(2024, 3, 8), 1))
print(add_workdays(date(2024, 3, 4), 5))
```

- Шагаем по одному дню и уменьшаем счётчик только на буднях.
- Пятница + 1 рабочий день = понедельник.
- Вывод: `2024-03-11`, `2024-03-11`.

## Праздники

```python
from datetime import date, timedelta

holidays = {date(2024, 3, 8)}
d, end = date(2024, 3, 6), date(2024, 3, 12)
work = []
while d <= end:
    if d.weekday() < 5 and d not in holidays:
        work.append(d.day)
    d += timedelta(days=1)
print(work)
```

- Даты хешируемы — праздники удобно хранить в множестве, проверка `in` мгновенная.
- Вывод: `[6, 7, 11, 12]`.

## Границы недели

```python
from datetime import date, timedelta

for d in [date(2024, 3, 8), date(2024, 3, 11), date(2024, 3, 17)]:
    monday = d - timedelta(days=d.weekday())
    print(d, "→", monday, monday + timedelta(days=6))
print(date(2024, 3, 8).isocalendar().week)
```

- `weekday()` — сколько дней прошло с понедельника. Отнимаем их — получаем понедельник.
- Воскресенье — понедельник + 6 дней.
- `isocalendar()` — (год, номер недели, день недели) по стандарту ISO; `.week` — номер недели.
- Вывод: `2024-03-08 → 2024-03-04 2024-03-10`, `2024-03-11 → 2024-03-11 2024-03-17`, `2024-03-17 → 2024-03-11 2024-03-17`, `10`.

## Итог

- Диапазон: `[start + timedelta(days=i) for i in range(n)]` или `while d <= end: ... d += timedelta(days=1)`.
- Будни: `weekday() < 5`; праздники — множество дат.
- Понедельник недели: `d - timedelta(days=d.weekday())`.
- `d.isocalendar().week` — номер недели.
'''),
    short=t(r'''
```py
n = (end - start).days + 1
days = [start + timedelta(days=i) for i in range(n)]

d = start
while d <= end:
    if d.weekday() < 5 and d not in holidays:
        ...
    d += timedelta(days=1)

monday = d - timedelta(days=d.weekday())
sunday = monday + timedelta(days=6)
d.isocalendar().week
```
'''),
    quiz=[
        q('Сколько дат в диапазоне с 1 по 3 марта включительно, если `(end - start).days == 2`?',
            ['2', '3', '1', '4'],
            1, 'Нужно прибавить 1.'),
        q('Как получить понедельник недели для даты `d`?',
            ['`d.replace(weekday=0)`', '`d - timedelta(days=d.weekday())`', '`d - timedelta(days=7)`', '`d.monday()`'],
            1, 'weekday() — дней с понедельника.'),
        q('Почему праздники удобно хранить в множестве?',
            ['Даты нельзя хранить в списке', 'Проверка `in` быстрая, дубликатов нет', 'Множество сортирует даты', 'Так требует datetime'],
            1, 'Даты хешируемы.'),
    ],
),

}
