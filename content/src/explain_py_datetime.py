"""Тема «Дата и время» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "dt"

EXPLAIN = {

# ===== Модуль 1. Даты и их запись =====

f"{P}-date-e1": x(
    idea="`date` хранит год, месяц и день. Печатается в формате ISO: `ГГГГ-ММ-ДД`.",
    lines=[
        ("print(d)", "Месяц и день с ведущим нулём."),
        ("print(d.year, d.month, d.day)", "Атрибуты — обычные числа, без нулей."),
        ("print(type(d).__name__)", "Имя класса."),
    ],
    mistake="Ожидать `8.3.2024` — формат по умолчанию ISO."),

f"{P}-date-e2": x(
    idea="`weekday()` считает от понедельника = 0, `isoweekday()` — от понедельника = 1. 8 марта 2024 — пятница.",
    lines=[
        ("print(d.weekday(), d.isoweekday())", "4 и 5."),
        ("print(days[d.weekday()])", "Индекс 4 — «пт»."),
        ("print(date(2024, 3, 10).weekday() >= 5)", "Воскресенье: 6 ≥ 5."),
    ],
    mistake="Считать, что `weekday()` начинается с 1."),

f"{P}-date-e3": x(
    idea="Даты сравниваются как числа на шкале времени, поэтому работают `sorted`, `min`, `max`. Несуществующая дата — `ValueError`.",
    lines=[
        ("print(a > b, a == date(2024, 1, 15))", "2024 позже 2023; одинаковые даты равны."),
        ("print(sorted(dates)[0], max(dates))", "Самая ранняя и самая поздняя."),
        ("date(2023, 2, 29)", "2023 — не високосный."),
    ],
    mistake="Думать, что `date` сама «перенесёт» 29 февраля на 1 марта."),

f"{P}-date-e4": x(
    idea="Суббота — 5, воскресенье — 6 в `weekday()`.",
    lines=[("return d.weekday() >= 5", "Выходные — 5 и 6.")],
    mistake="`d.weekday() > 5` — суббота окажется будним днём."),

f"{P}-date-e5": x(
    idea="`weekday()` — готовый индекс для списка названий, начинающегося с понедельника.",
    lines=[
        ('DAYS = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]', "Индекс 0 — понедельник."),
        ("return DAYS[d.weekday()]", "Название по индексу."),
    ],
    mistake="Начать список с воскресенья, как в американском календаре."),

f"{P}-date-e6": x(
    idea="Проверять високосные годы и длину месяцев вручную не нужно — `date` сама выбросит `ValueError`.",
    lines=[
        ("date(year, month, day)", "Пробуем создать."),
        ("except ValueError:\n        return False", "Такой даты нет."),
        ("return True", "Создалась — существует."),
    ],
    mistake="Писать свою проверку с таблицей дней в месяцах."),

f"{P}-date-e7": x(
    idea="`min` работает с датами. Пустой список — отдельный случай.",
    lines=[("return min(dates) if dates else None", "`min([])` упал бы с ошибкой.")],
    mistake="Вызвать `min` без проверки на пустоту."),

f"{P}-date-e8": x(
    idea="Месяцы 1–12 сдвигаем к 0–11, делим на 3 нацело — получаем 0–3, прибавляем 1.",
    lines=[
        ("return (d.month - 1) // 3 + 1", "Март: 2 // 3 + 1 = 1; апрель: 3 // 3 + 1 = 2."),
        ("return a.year == b.year and quarter(a) == quarter(b)", "Один квартал разных лет не считается."),
    ],
    mistake="`d.month // 3 + 1` — март попадёт во второй квартал."),

f"{P}-datetime-e1": x(
    idea="`datetime` — дата плюс время. `.date()` и `.time()` разбивают его на части.",
    lines=[
        ("print(dt)", "Дата и время через пробел."),
        ("print(dt.hour, dt.minute, dt.second)", "Числа без ведущих нулей."),
        ("print(dt.date(), dt.time())", "Две части вместе дают ту же строку."),
    ],
    mistake="Ожидать `T` между датой и временем — его добавляет только `isoformat()`."),

f"{P}-datetime-e2": x(
    idea="`replace` возвращает новый объект, исходный не меняется. `combine` собирает `datetime` из `date` и `time`.",
    lines=[
        ("print(dt.replace(hour=9, minute=0))", "Новый объект: 9:00."),
        ("print(dt)", "Старый не изменился: 14:30."),
        ("start = datetime.combine(date(2024, 1, 1), time(10, 15))", "Дата + время."),
        ("print(start, start.replace(day=31).day)", "В январе 31 день — можно."),
    ],
    mistake="Думать, что `replace` меняет объект на месте."),

f"{P}-datetime-e3": x(
    idea="Начало дня — `combine(дата, time.min)` или `replace` с нулями. Объекты `time` тоже сравниваются.",
    lines=[
        ("print(dt.replace(microsecond=0))", "Микросекунды убраны из вывода."),
        ("midnight = datetime.combine(dt.date(), time.min)", "`time.min` — 00:00."),
        ("print(time(9, 0) < time(18, 0) < time(23, 59))", "Цепочка сравнений."),
    ],
    mistake="Ожидать `.123456` в первой строке."),

f"{P}-datetime-e4": x(
    idea="Два условия: будний день и время в полуинтервале [9:00, 18:00).",
    lines=[("return dt.weekday() < 5 and time(9, 0) <= dt.time() < time(18, 0)", "18:00 уже не рабочее.")],
    mistake="`<= time(18, 0)` — ровно 18:00 окажется рабочим."),

f"{P}-datetime-e5": x(
    idea="`replace` с явными значениями всех частей времени.",
    lines=[
        ("return dt.replace(hour=0, minute=0, second=0, microsecond=0)", "Начало дня."),
        ("return dt.replace(hour=23, minute=59, second=59, microsecond=999999)", "Последняя микросекунда дня."),
    ],
    mistake="Забыть `microsecond` — останутся микросекунды из исходного значения."),

f"{P}-datetime-e6": x(
    idea="`combine` соединяет день и время в `datetime`.",
    lines=[("return datetime.combine(d, time(hour, minute))", "Минуты по умолчанию — 0.")],
    mistake="`datetime(d, hour, minute)` — `datetime` не принимает объект `date` первым аргументом."),

f"{P}-datetime-e7": x(
    idea="Цепочка `if` с ранним `return`: каждая проверка отсекает свой диапазон часов.",
    lines=[
        ('if dt.hour < 6:\n        return "ночь"', "0–5."),
        ('if dt.hour < 12:\n        return "утро"', "6–11: до этой строки доходят только часы ≥ 6."),
        ('if dt.hour < 18:\n        return "день"', "12–17."),
        ('return "вечер"', "Всё остальное."),
    ],
    mistake="`dt.hour <= 6` — 6:00 станет ночью."),

f"{P}-datetime-e8": x(
    idea="Сортируем события заранее — тогда и ключи, и списки времён окажутся по возрастанию.",
    lines=[
        ("for dt in sorted(events):", "По времени."),
        ("result.setdefault(dt.date(), []).append(dt.time())", "Создать список дня при первом событии."),
    ],
    mistake="Не сортировать — порядок ключей и времён будет как во входе."),

f"{P}-format-e1": x(
    idea="`strftime` собирает строку по шаблону: `%d` день, `%m` месяц, `%Y` год из 4 цифр, `%y` — из 2, `%H:%M:%S` — время.",
    lines=[
        ('print(dt.strftime("%d.%m.%Y"))', "Нули добавляются: 08.03."),
        ('print(dt.strftime("%H:%M:%S"))', "09:05:07."),
        ('print(dt.strftime("%d/%m/%y"))', "`%y` — 24."),
    ],
    mistake="Перепутать `%m` (месяц) и `%M` (минуты)."),

f"{P}-format-e2": x(
    idea="`isoformat` ставит `T` между датой и временем и всегда пишет секунды. В f-строке формат пишется после двоеточия.",
    lines=[
        ("print(dt.isoformat())", "С `T` и секундами."),
        ("print(date(2024, 3, 8).isoformat())", "У даты — только дата."),
        ('print(f"{dt:%d.%m.%Y}", f"{dt:%H:%M}")', "Как `strftime`."),
        ("print(str(dt))", "С пробелом вместо `T`."),
    ],
    mistake="Ожидать `09:05` без секунд от `isoformat()`."),

f"{P}-format-e3": x(
    idea="`%A`/`%B` — полные английские названия, `%a`/`%b` — сокращённые. `%j` — день года, `%w` — день недели от воскресенья = 0. `%%` — сам знак процента.",
    lines=[
        ('print(d.strftime("%A, %B"))', "Friday, March."),
        ('print(d.strftime("%j"), d.strftime("%w"))', "31 + 29 + 8 = 68-й день; пятница = 5."),
        ('print(d.strftime("%%Y = %Y"))', "`%%Y` — просто текст «%Y»."),
    ],
    mistake="Считать `%w` как `weekday()` — там понедельник 0, здесь воскресенье 0."),

f"{P}-format-e4": x(
    idea="Шаблон `%d.%m.%Y` — привычный русский формат с ведущими нулями.",
    lines=[("return d.strftime(\"%d.%m.%Y\")", "Работает и для `date`, и для `datetime`.")],
    mistake="`f\"{d.day}.{d.month}.{d.year}\"` — потеряются нули: 8.3.2024."),

f"{P}-format-e5": x(
    idea="Формат даты прямо внутри f-строки.",
    lines=[('return f"[{dt:%Y-%m-%d %H:%M:%S}] {level.upper()}: {msg}"', "Время в скобках, уровень заглавными.")],
    mistake="Забыть `.upper()` у уровня."),

f"{P}-format-e6": x(
    idea="`%B` зависит от языка системы и даёт именительный падеж. Свой список — надёжно и по-русски.",
    lines=[
        ('MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня",\n          "июля", "августа", "сентября", "октября", "ноября", "декабря"]', "Родительный падеж."),
        ('return f"{d.day} {MONTHS[d.month - 1]} {d.year}"', "`d.day` — без нуля; месяц с 1, индекс с 0."),
    ],
    mistake="`MONTHS[d.month]` — сдвиг на месяц и `IndexError` в декабре."),

f"{P}-format-e7": x(
    idea="В имени файла двоеточие заменено дефисом, дата и время разделены `_`.",
    lines=[('return f"{prefix}_{dt:%Y-%m-%d_%H-%M}.html"', "`%H-%M` вместо `%H:%M`.")],
    mistake="Использовать `isoformat()` — в имени появятся двоеточия."),

f"{P}-format-e8": x(
    idea="`timespec` задаёт точность: `\"seconds\"` отбрасывает микросекунды.",
    lines=[('return dt.isoformat(timespec="seconds")', "`2024-03-08T09:05:07`.")],
    mistake="`str(dt)` — пробел вместо `T` и возможные микросекунды."),

f"{P}-parse-e1": x(
    idea="`strptime` — обратная к `strftime`: строка + шаблон → `datetime`. Шаблон должен совпадать со строкой полностью.",
    lines=[
        ('dt = datetime.strptime("08.03.2024 14:30", "%d.%m.%Y %H:%M")', "Разбор по шаблону."),
        ("print(repr(dt))", "`repr` показывает конструктор; нулевые секунды не пишутся."),
        ('print(datetime.strptime("2024-03-08", "%Y-%m-%d").date())', "`.date()` — только дата."),
    ],
    mistake="Ожидать `datetime(2024, 3, 8, 14, 30, 0)` в `repr`."),

f"{P}-parse-e2": x(
    idea="`fromisoformat` понимает ISO-строки: с `T` или пробелом, без секунд, с `Z` (UTC, с Python 3.11).",
    lines=[
        ('print(datetime.fromisoformat("2024-03-08 14:30"))', "Секунды дописаны нулями."),
        ('print(datetime.fromisoformat("2024-03-08T14:30:00Z"))', "`Z` → часовой пояс `+00:00`."),
    ],
    mistake="Ожидать `Z` в выводе — Python печатает смещение."),

f"{P}-parse-e3": x(
    idea="Строка должна соответствовать шаблону и быть существующей датой. Ведущие нули при разборе необязательны.",
    lines=[
        ('tests = ["31.12.2024", "2024-12-31", "32.01.2024", "1.2.2024"]', "Первая подходит; вторая — другой формат; 32-го дня нет; последняя подходит: `%d` принимает и «1»."),
        ('print(datetime.strptime(text, "%d.%m.%Y").date())', "Удачный разбор."),
        ('except ValueError:\n        print("ошибка:", text)', "Неудачный."),
    ],
    mistake="Думать, что `1.2.2024` не подходит под `%d.%m`."),

f"{P}-parse-e4": x(
    idea="Разбираем в `datetime` и берём дату.",
    lines=[('return datetime.strptime(text, "%d.%m.%Y").date()', "`date` своего `strptime` не имеет.")],
    mistake="Вернуть `datetime` — ответ будет с временем 00:00."),

f"{P}-parse-e5": x(
    idea="Разобрать ISO-строку и собрать новую по другому шаблону.",
    lines=[('return date.fromisoformat(text).strftime("%d.%m.%Y")', "Строка → дата → строка.")],
    mistake="Переставлять части `split(\"-\")` вручную — сработает, но без проверки даты."),

f"{P}-parse-e6": x(
    idea="Перебор форматов: первый удачный разбор — сразу `return`, неудачный — пробуем следующий.",
    lines=[
        ("for fmt in FORMATS:", "По очереди."),
        ("return datetime.strptime(text, fmt).date()", "Подошёл — выходим."),
        ("except ValueError:\n            pass", "Не подошёл — дальше."),
        ("return None", "Ни один формат."),
    ],
    mistake="`return None` внутри `except` — второй формат не будет проверен."),

f"{P}-parse-e7": x(
    idea="Корректность проверяем попыткой разбора.",
    lines=[
        ("datetime.fromisoformat(text)", "Результат не нужен — важна ошибка."),
        ("except ValueError:\n        return False", "Не ISO."),
        ("return True", "Разобралось."),
    ],
    mistake="Проверять регулярным выражением — пропустит `2024-13-45`."),

f"{P}-parse-e8": x(
    idea="`split(\" \", 3)` делит строку не больше трёх раз — текст сообщения с пробелами остаётся целым. Кортежи сортируются по первому элементу — времени.",
    lines=[
        ('day, clock, level, _ = line.split(" ", 3)', "Четыре части."),
        ('if level == "ERROR":', "Только ошибки."),
        ('dt = datetime.strptime(f"{day} {clock}", "%Y-%m-%d %H:%M:%S")', "Склеиваем обратно и разбираем."),
        ("return sorted(result)", "По времени."),
    ],
    mistake="`line.split()` без ограничения — распаковка упадёт, если в тексте есть пробелы."),

# ===== Модуль 2. Арифметика дат =====

f"{P}-timedelta-e1": x(
    idea="`timedelta` — промежуток. Прибавляешь к дате — получаешь новую дату; переходы через месяц и високосный февраль учитываются сами.",
    lines=[
        ("print(d + timedelta(days=3))", "27.02 + 3: 28, 29 (2024 високосный), 1 марта."),
        ("print(d - timedelta(weeks=1))", "Неделя назад."),
        ("print(timedelta(days=1, hours=5))", "Печать: `дни, Ч:ММ:СС`."),
        ("print(timedelta(hours=36))", "36 часов = 1 день и 12 часов."),
    ],
    mistake="Забыть про 29 февраля — ответ `2024-03-02`."),

f"{P}-timedelta-e2": x(
    idea="Внутри `timedelta` хранит дни и секунды остатка (меньше суток). Для всего промежутка в секундах — `total_seconds()`.",
    lines=[
        ("print(td.days, td.seconds)", "3 ч 30 мин = 12600 с — только остаток, без дней."),
        ("print(td.total_seconds())", "2 × 86400 + 12600."),
        ("print(td.total_seconds() / 3600)", "В часах: 51.5."),
        ("print(timedelta(minutes=90) > timedelta(hours=1))", "Промежутки сравниваются."),
    ],
    mistake="Считать, что `.seconds` — все секунды промежутка."),

f"{P}-timedelta-e3": x(
    idea="`timedelta` можно умножать, делить на число и делить друг на друга. Отрицательный промежуток хранится как «−1 день + положительный остаток».",
    lines=[
        ("print(start + timedelta(minutes=45))", "23:30 + 45 мин — следующий день."),
        ("print(step * 3, step / 2)", "Час и 10 минут."),
        ("print(timedelta(hours=2) // timedelta(minutes=25))", "Сколько целых 25-минуток в 2 часах: 4."),
        ("print(-timedelta(hours=1))", "−1 день + 23 часа."),
    ],
    mistake="Ожидать `-1:00:00`."),

f"{P}-timedelta-e4": x(
    idea="Дата + промежуток = новая дата.",
    lines=[("return start + timedelta(days=days)", "Именованный аргумент `days=`.")],
    mistake="`start + days` — к дате нельзя прибавить число."),

f"{P}-timedelta-e5": x(
    idea="Берём все секунды и раскладываем через `divmod`: часы, затем минуты и секунды.",
    lines=[
        ("total = int(td.total_seconds())", "Все секунды, дробь отброшена."),
        ("hours, rest = divmod(total, 3600)", "Часы и остаток."),
        ("minutes, seconds = divmod(rest, 60)", "Минуты и секунды."),
        ('return f"{hours:02}:{minutes:02}:{seconds:02}"', "`:02` — ведущий ноль."),
    ],
    mistake="`str(td)` — выдаст `1 day, 2:05:03`."),

f"{P}-timedelta-e6": x(
    idea="Копим сумму в `timedelta()` — пустой промежуток; каждую строку разбираем в минуты и секунды.",
    lines=[
        ("total = timedelta()", "Ноль."),
        ('minutes, seconds = d.split(":")', "Две строки."),
        ("total += timedelta(minutes=int(minutes), seconds=int(seconds))", "Числа — через `int`."),
    ],
    mistake="`total = 0` — `0 + timedelta` вызовет `TypeError`."),

f"{P}-timedelta-e7": x(
    idea="i-й запуск — `start + шаг × i`.",
    lines=[
        ("step = timedelta(minutes=interval_minutes)", "Шаг."),
        ("return [start + step * i for i in range(count)]", "Первый — сам `start` (i = 0)."),
    ],
    mistake="`range(1, count + 1)` — потеряется первый запуск."),

f"{P}-timedelta-e8": x(
    idea="Дни — `td.days`, часы и минуты — из остатка `td.seconds`. Пустые части не добавляем.",
    lines=[
        ("hours, rest = divmod(td.seconds, 3600)", "Часы внутри суток."),
        ("minutes = rest // 60", "Секунды отброшены."),
        ('if td.days:\n        parts.append(f"{td.days} д")', "Только ненулевые."),
        ('return " ".join(parts) or "0 мин"', "Пустая строка — ложь, тогда `0 мин`."),
    ],
    mistake="Брать часы из `total_seconds()` — дни посчитаются дважды."),

f"{P}-diff-e1": x(
    idea="Разность дат — `timedelta`. У двух `date` время всегда `0:00:00`.",
    lines=[
        ("delta = date(2024, 12, 31) - date(2024, 1, 1)", "365 дней (последний не включён)."),
        ("print(d2, d2.total_seconds() / 3600)", "8 ч 30 мин = 8.5 ч."),
        ("print(date(2024, 1, 1) - date(2024, 1, 10))", "Из ранней вычли позднюю — минус."),
    ],
    mistake="Ожидать 366 — в 2024 году 366 дней, но разница 1 января и 31 декабря — 365."),

f"{P}-diff-e2": x(
    idea="Даты вычитают, но не складывают. `date` и `datetime` не смешиваются — приведи `datetime` к дате через `.date()`.",
    lines=[
        ("date(2024, 1, 1) + date(2024, 1, 2)", "Бессмыслица — `TypeError`."),
        ("datetime(2024, 1, 1) - date(2024, 1, 1)", "Разные типы — `TypeError`."),
        ("print(datetime(2024, 1, 2).date() - date(2024, 1, 1))", "Обе `date` — можно."),
    ],
    mistake="Думать, что `datetime` можно вычесть из `date`, раз он её наследник."),

f"{P}-diff-e3": x(
    idea="Возраст — разность годов, минус один, если день рождения в этом году ещё не наступил. Кортежи `(месяц, день)` сравниваются по порядку.",
    lines=[
        ("if (today.month, today.day) < (born.month, born.day):", "19 мая раньше 20 мая — ещё нет."),
        ("print(age(date(2000, 5, 20), date(2024, 5, 20)))", "Ровно в день рождения — уже 24."),
        ("print((date(2024, 5, 20) - date(2000, 5, 20)).days // 365)", "Здесь совпало, но из-за високосных лет так считать ненадёжно."),
    ],
    mistake="Считать возраст как `today.year - born.year` без проверки."),

f"{P}-diff-e4": x(
    idea="Разность дат — `timedelta`, число дней — `.days`.",
    lines=[("return (event - today).days", "Прошло — отрицательное.")],
    mistake="`today - event` — знак будет обратным."),

f"{P}-diff-e5": x(
    idea="Годы по разности, минус один, если день рождения ещё впереди.",
    lines=[
        ("years = today.year - born.year", "Черновой возраст."),
        ("if (today.month, today.day) < (born.month, born.day):\n        years -= 1", "Сравниваем кортежи."),
    ],
    mistake="`.days // 365` — ошибка в день-два около дня рождения."),

f"{P}-diff-e6": x(
    idea="Сравнение моментов и перевод разницы в часы; просроченное даёт 0.",
    lines=[
        ("return now > deadline", "Позже дедлайна."),
        ("if now >= deadline:\n        return 0", "Не отрицательные часы."),
        ("return int((deadline - now).total_seconds() // 3600)", "Целые часы."),
    ],
    mistake="`(deadline - now).seconds // 3600` — пропадут дни."),

f"{P}-diff-e7": x(
    idea="`zip(ds, ds[1:])` даёт соседние пары. `default=0` — ответ для пустой последовательности.",
    lines=[
        ("ds = sorted(dates)", "По порядку."),
        ("return max(((b - a).days for a, b in zip(ds, ds[1:])), default=0)", "Меньше двух дат — пар нет, ответ 0."),
    ],
    mistake="Забыть `default` — `max` упадёт на одной дате."),

f"{P}-diff-e8": x(
    idea="Разность `datetime` сравнивается с `timedelta` напрямую.",
    lines=[
        ("limit = timedelta(hours=24)", "Порог."),
        ('return [t["id"] for t in tickets if t["closed"] - t["opened"] > limit]', "Строго дольше."),
    ],
    mistake="Сравнивать `.days > 1` — 36 часов не попадут."),

f"{P}-calendar-e1": x(
    idea="Високосный — кратен 4, кроме кратных 100, но кратные 400 — снова да. `monthrange` — (день недели 1-го числа, дней в месяце).",
    lines=[
        ("print(calendar.isleap(2024), calendar.isleap(1900), calendar.isleap(2000))", "1900 кратен 100, 2000 — 400."),
        ("print(calendar.monthrange(2024, 2))", "1 февраля 2024 — четверг, 29 дней."),
        ("print(calendar.monthrange(2023, 2)[1])", "Только число дней."),
    ],
    mistake="Считать 1900 високосным."),

f"{P}-calendar-e2": x(
    idea="`timedelta` не знает про месяцы: +30 дней — не «+1 месяц». `replace(month=2)` для 31-го числа падает.",
    lines=[
        ("print(d + timedelta(days=30))", "31 января + 30 дней = 1 марта."),
        ("print(d.replace(month=2))", "31 февраля не бывает."),
    ],
    mistake="Ожидать `2024-02-29` от `replace`."),

f"{P}-calendar-e3": x(
    idea="Первый день — `replace(day=1)`, последний — `replace(day=дней_в_месяце)`.",
    lines=[
        ("first = d.replace(day=1)", "1-е число."),
        ("last = d.replace(day=calendar.monthrange(d.year, d.month)[1])", "29 — февраль 2024."),
        ("print(calendar.month_abbr[2], calendar.day_abbr[0])", "Месяцы с 1, дни недели с 0 (понедельник)."),
    ],
    mistake="Ожидать `Jan` для `month_abbr[2]` — индекс 0 там пустой."),

f"{P}-calendar-e4": x(
    idea="Второй элемент `monthrange` — количество дней.",
    lines=[("return calendar.monthrange(year, month)[1]", "Первый элемент — день недели.")],
    mistake="Взять `[0]`."),

f"{P}-calendar-e5": x(
    idea="Последнее число месяца подставляем через `replace`.",
    lines=[("return d.replace(day=calendar.monthrange(d.year, d.month)[1])", "Год и месяц — из самой даты.")],
    mistake="`d + timedelta(days=30)` — уйдёт в следующий месяц."),

f"{P}-calendar-e6": x(
    idea="Месяцы переводим в сквозной номер (год × 12 + месяц), сдвигаем, раскладываем обратно. День ограничиваем длиной целевого месяца.",
    lines=[
        ("index = d.year * 12 + (d.month - 1) + n", "Месяц с нуля, чтобы деление работало."),
        ("year, month = divmod(index, 12)", "Год и месяц 0–11."),
        ("month += 1", "Обратно к 1–12."),
        ("day = min(d.day, calendar.monthrange(year, month)[1])", "31 января → 29 февраля."),
    ],
    mistake="`d.month + n` без переноса — месяц 14 и `ValueError`."),

f"{P}-calendar-e7": x(
    idea="Фильтр по `isleap`, конец диапазона включительно.",
    lines=[("return [y for y in range(start, end + 1) if calendar.isleap(y)]", "`end + 1` — включить конец.")],
    mistake="`y % 4 == 0` — ошибка на 1900 и 2100."),

f"{P}-calendar-e8": x(
    idea="Границы месяца — две даты; принадлежность — двойное сравнение.",
    lines=[
        ("last = calendar.monthrange(year, month)[1]", "Дней в месяце."),
        ("return date(year, month, 1), date(year, month, last)", "Кортеж."),
        ("return first <= d <= last", "Включительно."),
    ],
    mistake="Сравнивать только `d.month == month` — забудешь про год."),

f"{P}-ranges-e1": x(
    idea="Диапазон дат — список `start + i дней`.",
    lines=[
        ("days = [start + timedelta(days=i) for i in range(4)]", "0…3 дня."),
        ("print([d.isoformat() for d in days])", "Строки в кавычках — это список строк."),
    ],
    mistake="Пропустить 29 февраля."),

f"{P}-ranges-e2": x(
    idea="Цикл по дням с пропуском выходных. 9 и 10 марта 2024 — суббота и воскресенье.",
    lines=[
        ("while d <= end:", "По дням включительно."),
        ("if d.weekday() < 5:", "Только будни."),
        ("d += timedelta(days=1)", "Следующий день."),
    ],
    mistake="Забыть про `end=\" \"` — даты окажутся в отдельных строках."),

f"{P}-ranges-e3": x(
    idea="Понедельник недели — дата минус `weekday()` дней. `isocalendar().week` — номер недели ISO.",
    lines=[
        ("monday = d - timedelta(days=d.weekday())", "Пятница − 4, понедельник − 0, воскресенье − 6."),
        ("print(date(2024, 3, 8).isocalendar().week)", "10-я неделя."),
    ],
    mistake="Думать, что воскресенье начинает новую неделю."),

f"{P}-ranges-e4": x(
    idea="Количество дней — разность + 1; отрицательное превращаем в 0.",
    lines=[
        ("count = (end - start).days + 1", "Включая оба конца."),
        ("return [start + timedelta(days=i) for i in range(max(count, 0))]", "`range` отрицательного пуст, но `max` делает намерение явным."),
    ],
    mistake="Забыть `+ 1` — потеряется `end`."),

f"{P}-ranges-e5": x(
    idea="Идём по дням и считаем будние.",
    lines=[
        ("while d <= end:", "Включая `end`."),
        ("if d.weekday() < 5:\n            count += 1", "Пн–пт."),
        ("d += timedelta(days=1)", "Не забыть шаг."),
    ],
    mistake="Забыть шаг — бесконечный цикл."),

f"{P}-ranges-e6": x(
    idea="Шагаем по дню вперёд и уменьшаем счётчик только на будних днях.",
    lines=[
        ("while n > 0:", "Пока остались рабочие дни."),
        ("d += timedelta(days=1)", "Сначала шаг — `start` не считается."),
        ("if d.weekday() < 5:\n            n -= 1", "Выходные не считаются."),
    ],
    mistake="Прибавить `n` дней и перескочить на понедельник — не учтёт выходные в середине."),

f"{P}-ranges-e7": x(
    idea="Понедельник — минус `weekday()`, воскресенье — понедельник + 6.",
    lines=[
        ("monday = d - timedelta(days=d.weekday())", "Начало недели."),
        ("return monday, monday + timedelta(days=6)", "Конец."),
    ],
    mistake="`+ 7` — следующий понедельник."),

f"{P}-ranges-e8": x(
    idea="Два фильтра: будний день и не праздник. Множество — быстрая проверка `in`.",
    lines=[
        ("if d.weekday() < 5 and d not in holidays:", "Оба условия."),
        ("result.append(d)", "Рабочий."),
        ("d += timedelta(days=1)", "Следующий."),
    ],
    mistake="`or` вместо `and` — праздничные будни попадут в список."),

# ===== Модуль 3. Пояса, timestamp и тесты =====

f"{P}-timezone-e1": x(
    idea="Naive — без пояса (`tzinfo is None`), aware — с поясом. `astimezone` показывает тот же момент в другом поясе.",
    lines=[
        ("print(naive.tzinfo, utc.tzinfo)", "None и UTC."),
        ("print(utc)", "Смещение `+00:00` в конце."),
        ("print(utc.astimezone(msk))", "12:00 UTC = 15:00 по Москве."),
    ],
    mistake="Думать, что `astimezone` меняет момент, а не только запись."),

f"{P}-timezone-e2": x(
    idea="Aware-даты сравниваются как моменты: 15:00 MSK и 7:00 NY — одно и то же (12:00 UTC).",
    lines=[
        ("print(a == b, a - b)", "Равны, разница — ноль."),
        ('print(b.astimezone(msk).strftime("%H:%M %Z"))', "`%Z` — имя пояса."),
    ],
    mistake="Сравнивать цифры часов: 15 ≠ 7."),

f"{P}-timezone-e3": x(
    idea="Naive и aware нельзя сравнивать на больше-меньше; `==` просто даёт `False`. `replace(tzinfo=...)` прикрепляет пояс без пересчёта.",
    lines=[
        ("naive < aware", "`TypeError`."),
        ("print(naive == aware)", "Не ошибка, но всегда `False`."),
        ("print(naive.replace(tzinfo=timezone.utc) == aware)", "Теперь оба aware."),
    ],
    mistake="Ожидать ошибку и на `==`."),

f"{P}-timezone-e4": x(
    idea="Naive непонятно как переводить — отказываемся. Aware переводим `astimezone`.",
    lines=[
        ("if dt.tzinfo is None:", "Нет пояса."),
        ('raise ValueError("нужен часовой пояс")', "Отказ."),
        ("return dt.astimezone(timezone.utc)", "Тот же момент в UTC."),
    ],
    mistake="`replace(tzinfo=timezone.utc)` — цифры не пересчитаются."),

f"{P}-timezone-e5": x(
    idea="Пояс по смещению — `timezone(timedelta(hours=...))`.",
    lines=[
        ("tz = timezone(timedelta(hours=offset_hours))", "Например, +3."),
        ('return utc_dt.astimezone(tz).strftime("%H:%M")', "22:30 UTC → 01:30."),
    ],
    mistake="Прибавить `timedelta(hours=3)` к UTC — цифры верны, но пояс останется UTC."),

f"{P}-timezone-e6": x(
    idea="`==` у aware-дат сравнивает моменты, а не записи.",
    lines=[("return a == b", "Пояса учитываются автоматически.")],
    mistake="Сравнивать `a.hour == b.hour`."),

f"{P}-timezone-e7": x(
    idea="`replace(tzinfo=...)` прикрепляет пояс, не меняя цифр — ровно то, что нужно для «считаем, что это UTC».",
    lines=[
        ("if dt.tzinfo is None:", "Naive."),
        ("return dt.replace(tzinfo=timezone.utc)", "Прикрепить UTC."),
        ("return dt", "Aware не трогаем."),
    ],
    mistake="`astimezone` для naive — Python сочтёт его местным временем компьютера."),

f"{P}-timezone-e8": x(
    idea="Один момент — разные местные часы. Для каждого города свой пояс.",
    lines=[
        ("for city, hours in offsets.items():", "Город и смещение."),
        ("local = utc_dt.astimezone(timezone(timedelta(hours=hours)))", "Местное время."),
        ('result[city] = local.strftime("%d.%m %H:%M")', "Дата тоже может смениться."),
    ],
    mistake="Не показывать дату — встреча у кого-то окажется на другой день."),

f"{P}-timestamp-e1": x(
    idea="Unix-время — секунды с 1 января 1970 UTC. `timestamp()` и вычитание эпохи дают одно и то же.",
    lines=[
        ("print(dt.timestamp())", "float."),
        ("print((dt - epoch).total_seconds())", "То же число."),
        ("print(datetime.fromtimestamp(0, tz=timezone.utc))", "Ноль — сама эпоха."),
    ],
    mistake="Забыть `tz=` — получится местное время компьютера."),

f"{P}-timestamp-e2": x(
    idea="API часто присылают миллисекунды (13 цифр). Для `fromtimestamp` делим на 1000.",
    lines=[
        ("dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)", "500 мс → `.500000`."),
        ("print(int(dt.timestamp() * 1000) == ms)", "Обратное преобразование."),
        ("print(len(str(ms)), len(str(ms // 1000)))", "13 и 10 цифр."),
    ],
    mistake="Передать миллисекунды без деления — год 56 тысяч и ошибка."),

f"{P}-timestamp-e3": x(
    idea="`perf_counter` — для замеров, `time.time()` — Unix-время (float).",
    lines=[
        ("elapsed = time.perf_counter() - start", "Не меньше 0.05."),
        ("print(elapsed >= 0.05, elapsed < 1)", "Проверяем диапазон, не точное значение."),
        ("print(type(time.time()).__name__, time.time() > 1_700_000_000)", "Сейчас больше 1.7 млрд секунд."),
    ],
    mistake="Сравнивать время выполнения на равенство — оно всегда немного разное."),

f"{P}-timestamp-e4": x(
    idea="Миллисекунды → секунды → `datetime` с поясом UTC.",
    lines=[("return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)", "`/`, а не `//` — миллисекунды сохранятся.")],
    mistake="`ms // 1000` — потеряются доли секунды."),

f"{P}-timestamp-e5": x(
    idea="`timestamp()` — float; `int` отбрасывает дробь.",
    lines=[("return int(dt.timestamp())", "Целые секунды.")],
    mistake="`round` — может округлить вверх."),

f"{P}-timestamp-e6": x(
    idea="По размеру числа отличаем миллисекунды от секунд.",
    lines=[
        ("if value > 10 ** 11:\n        value = value / 1000", "13 цифр — миллисекунды."),
        ("return datetime.fromtimestamp(value, tz=timezone.utc)", "Теперь всегда секунды."),
    ],
    mistake="Проверять `len(str(value))` — не сработает для float."),

f"{P}-timestamp-e7": x(
    idea="Замер: отметка до, вызов, разница после.",
    lines=[
        ("start = time.perf_counter()", "До."),
        ("result = func()", "Вызов."),
        ("return result, time.perf_counter() - start", "Кортеж."),
    ],
    mistake="Засечь время после вызова и вернуть 0."),

f"{P}-timestamp-e8": x(
    idea="Возраст записи в секундах; допускаем небольшой «минус» из-за рассинхрона часов.",
    lines=[
        ("age = now_seconds - ts_seconds", "Сколько прошло."),
        ("return -5 <= age <= max_age", "Двойное сравнение."),
    ],
    mistake="Не допустить отрицательный возраст — свежие записи с чужого сервера станут «невалидными»."),

f"{P}-api-e1": x(
    idea="`json` не знает `datetime`. `default=str` превращает незнакомое в строку; `isoformat()` — стандарт для API.",
    lines=[
        ("json.dumps(data)", "`TypeError`."),
        ("print(json.dumps(data, default=str))", "`str` — с пробелом."),
        ('print(json.dumps({"created": data["created"].isoformat()}))', "ISO — с `T`."),
    ],
    mistake="Ожидать, что `json.dumps` сам вызовет `str`."),

f"{P}-api-e2": x(
    idea="Строки из API превращаем в aware-даты и сравниваем моменты. 12:00 +03:00 — это 9:00 UTC, раньше чем 9:30 UTC.",
    lines=[
        ('created = datetime.fromisoformat(user["created_at"])', "9:30 UTC."),
        ('updated = datetime.fromisoformat(user["updated_at"])', "9:00 UTC."),
        ("print(updated - created, updated > created)", "−30 минут: баг в API."),
    ],
    mistake="Сравнивать строки: `12:00` > `09:30`."),

f"{P}-api-e3": x(
    idea="Функция `default` вызывается для незнакомых объектов; для совсем чужих — `TypeError`.",
    lines=[
        ("if isinstance(value, (date, datetime)):\n        return value.isoformat()", "Даты — в ISO."),
        ('raise TypeError(f"не умею {type(value).__name__}")', "Множество — ошибка."),
        ('json.dumps({"s": {1, 2}}, default=encode)', "`set` не JSON."),
    ],
    mistake="Вернуть `None` для незнакомого — в JSON тихо появится `null`."),

f"{P}-api-e4": x(
    idea="Вложенная функция-кодировщик и `default=`.",
    lines=[
        ("if isinstance(value, (date, datetime)):\n            return value.isoformat()", "Даты."),
        ("raise TypeError(type(value).__name__)", "Остальное незнакомое — ошибка."),
        ("return json.dumps(data, default=encode)", "Числа, строки — как обычно."),
    ],
    mistake="`default=str` — `datetime` выйдет с пробелом, не ISO."),

f"{P}-api-e5": x(
    idea="Копия словаря — чтобы не менять исходный.",
    lines=[
        ("result = dict(obj)", "Поверхностная копия."),
        ("if field in result:", "Отсутствующее пропускаем."),
        ("result[field] = datetime.fromisoformat(result[field])", "Строка → `datetime`."),
    ],
    mistake="Менять `obj` на месте — вызывающий код получит неожиданные `datetime`."),

f"{P}-api-e6": x(
    idea="Разбираем оба поля, копим ошибки; порядок проверяем, только если оба разобрались.",
    lines=[
        ("parsed[field] = datetime.fromisoformat(user[field])", "Удачно — запоминаем."),
        ('except ValueError:\n            errors.append(f"{field}: не ISO")', "Ошибка поля."),
        ('if len(parsed) == 2 and parsed["updated_at"] < parsed["created_at"]:', "Оба есть и порядок неверный."),
    ],
    mistake="Сравнивать при ошибке разбора — `KeyError`."),

f"{P}-api-e7": x(
    idea="Переводим в UTC и форматируем вручную: `strftime` без микросекунд и с буквой `Z`.",
    lines=[('return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")', "`Z` — просто символ в шаблоне.")],
    mistake="`isoformat()` — даст `+00:00` и микросекунды."),

f"{P}-api-e8": x(
    idea="Храним лучший момент и исходную строку. Сравниваем `datetime`, а не строки — пояса разные.",
    lines=[
        ('moment = datetime.fromisoformat(e["at"])', "Момент."),
        ("if user not in best or moment > best[user][0]:", "Первый или более поздний."),
        ('best[user] = (moment, e["at"])', "Пара: для сравнения и для ответа."),
        ("return {user: text for user, (_, text) in best.items()}", "Оставляем только строки."),
    ],
    mistake="`max` по строкам — `10:00+05:00` покажется позже `08:00Z`."),

f"{P}-testing-e1": x(
    idea="Время передаётся параметром — функцию легко проверить на любой час.",
    lines=[
        ("def greeting(now):", "Не вызывает `datetime.now()` сама."),
        ("print(greeting(datetime(2024, 3, 8, h)))", "8, 13, 21 часов."),
    ],
    mistake="Писать `datetime.now()` внутри — тест будет зависеть от времени запуска."),

f"{P}-testing-e2": x(
    idea="Поддельные часы: время двигается вручную, тест мгновенный и предсказуемый.",
    trace=[
        ("s = Session(clock, 30)", "истекает 12:30", ""),
        ("print(s.is_active())", "12:00 < 12:30", "True"),
        ("clock.advance(minutes=29)", "12:29", ""),
        ("print(s.is_active())", "12:29 < 12:30", "True"),
        ("clock.advance(minutes=1)", "12:30", ""),
        ("print(s.is_active())", "12:30 < 12:30 — нет", "False"),
    ],
    mistake="Ожидать `True` ровно в момент истечения."),

f"{P}-testing-e3": x(
    idea="Граничные даты — любимое место багов: високосный год, смена года, разная длина февраля.",
    lines=[
        ('edge = [date(2024, 2, 28), date(2023, 12, 31), date(2024, 12, 31)]', "Коварные даты."),
        ('print(d, "→", d + timedelta(days=1))', "29 февраля; новый год."),
        ("print(date(2024, 3, 1) - date(2024, 2, 1), date(2023, 3, 1) - date(2023, 2, 1))", "29 и 28 дней."),
    ],
    mistake="Ожидать `2024-03-01` после 28 февраля 2024."),

f"{P}-testing-e4": x(
    idea="Внедрение времени: параметр со значением `None`, а «сейчас» берём только если его не передали.",
    lines=[
        ("def is_expired(expires_at, now=None):", "Тест передаст своё время."),
        ("if now is None:\n        now = datetime.now()", "В проде — настоящее."),
        ("return now > expires_at", "Сравнение."),
    ],
    mistake="`now=datetime.now()` в заголовке — время застынет в момент импорта."),

f"{P}-testing-e5": x(
    idea="Ограничитель хранит времена вызовов и выбрасывает старые из окна. Поддельные часы делают тест мгновенным.",
    lines=[
        ("self.current += timedelta(seconds=seconds)", "Время двигаем вручную."),
        ("self.calls = [t for t in self.calls if now - t < self.window]", "Забываем старые."),
        ("if len(self.calls) >= self.limit:\n            return False", "Лимит в окне."),
        ("self.calls.append(now)\n        return True", "Разрешено — запоминаем."),
    ],
    mistake="Запоминать отклонённые вызовы — лимит не освободится."),

f"{P}-testing-e6": x(
    idea="Первый день — `replace(day=1)`, последний — через `monthrange`. Граничные случаи `calendar` обрабатывает сам.",
    lines=[
        ("last = calendar.monthrange(today.year, today.month)[1]", "28/29/30/31."),
        ("return today.replace(day=1), today.replace(day=last)", "Кортеж."),
    ],
    mistake="Считать последний день как «1-е следующего месяца − 1» с `month + 1` — в декабре месяц 13."),

f"{P}-testing-e7": x(
    idea="Фабрика с разумными значениями по умолчанию; тест меняет только нужное через `**overrides`.",
    lines=[
        ('"pay_until": created_at + timedelta(days=3),', "Вычисляемое поле."),
        ("order.update(overrides)", "Переопределения — поверх."),
    ],
    mistake="`update` до заполнения — переопределения затрутся."),

f"{P}-testing-e8": x(
    idea="Точное равенство времени сервера ловить бессмысленно — проверяем, что разница в допуске.",
    lines=[
        ("diff = abs((actual - expected).total_seconds())", "В любую сторону."),
        ('if diff > seconds:\n        raise AssertionError(f"разница {int(diff)} с")', "Вне допуска."),
    ],
    mistake="Без `abs` — отставание не заметишь."),
}
