"""Тема «Дата и время», модуль 1 «Даты и их запись» — задания. Теория — в _dt_t1.py."""
from ._lib import cod, lesson, module, out, t

P = "dt"

m1 = module(f"{P}-m1", "Даты и их запись", "📅", "date, datetime и time, форматирование strftime, разбор строк strptime и ISO",

lesson(f"{P}-date", "Дата: date",
    out(f"{P}-date-e1", "Что выведет программа?", """
        from datetime import date

        d = date(2024, 3, 8)
        print(d)
        print(d.year, d.month, d.day)
        print(type(d).__name__)
        """, hint="print(date) показывает дату в формате ГГГГ-ММ-ДД."),
    out(f"{P}-date-e2", "Что выведет программа? День недели.", """
        from datetime import date

        d = date(2024, 3, 8)
        print(d.weekday(), d.isoweekday())
        days = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
        print(days[d.weekday()])
        print(date(2024, 3, 10).weekday() >= 5)
        """, hint="weekday(): понедельник — 0, воскресенье — 6. isoweekday(): понедельник — 1."),
    out(f"{P}-date-e3", "Что выведет программа? Сравнение и сортировка.", """
        from datetime import date

        a = date(2024, 1, 15)
        b = date(2023, 12, 31)
        print(a > b, a == date(2024, 1, 15))
        dates = [date(2024, 5, 1), date(2023, 1, 1), date(2024, 1, 1)]
        print(sorted(dates)[0], max(dates))
        try:
            date(2023, 2, 29)
        except ValueError as e:
            print(e)
        """),
    cod(f"{P}-date-e4", t("""
        Напиши функцию `is_weekend(d)` — `True`, если дата `d` (объект `date`) выпадает на субботу или воскресенье.
        """),
        """
        from datetime import date


        def is_weekend(d):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert is_weekend(date(2024, 3, 9)) and is_weekend(date(2024, 3, 10)), "Выходные"
            assert not is_weekend(date(2024, 3, 8)) and not is_weekend(date(2024, 3, 11)), "Будни"
        """,
        """
        from datetime import date


        def is_weekend(d):
            return d.weekday() >= 5
        """),
    cod(f"{P}-date-e5", t("""
        Напиши функцию `day_name(d)` — название дня недели по-русски: `"понедельник"`, `"вторник"`, …, `"воскресенье"`.
        """),
        """
        from datetime import date


        def day_name(d):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert day_name(date(2024, 3, 8)) == "пятница" and day_name(date(2024, 3, 11)) == "понедельник" and day_name(date(2024, 3, 10)) == "воскресенье", "Неверный день"
        """,
        """
        from datetime import date

        DAYS = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]


        def day_name(d):
            return DAYS[d.weekday()]
        """),
    cod(f"{P}-date-e6", t("""
        Напиши функцию `is_valid_date(year, month, day)` — `True`, если такая дата существует (используй `date` и перехват `ValueError`).
        """),
        """
        from datetime import date


        def is_valid_date(year, month, day):
            pass
        """,
        """
        def test_values():
            assert is_valid_date(2024, 2, 29) and not is_valid_date(2023, 2, 29), "29 февраля"
            assert not is_valid_date(2024, 4, 31) and not is_valid_date(2024, 13, 1) and is_valid_date(2024, 12, 31), "Прочие даты"
        """,
        """
        from datetime import date


        def is_valid_date(year, month, day):
            try:
                date(year, month, day)
            except ValueError:
                return False
            return True
        """),
    cod(f"{P}-date-e7", t("""
        Напиши функцию `earliest(dates)` — самую раннюю дату из списка объектов `date`; для пустого списка — `None`.
        """),
        """
        from datetime import date


        def earliest(dates):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert earliest([date(2024, 5, 1), date(2023, 1, 2), date(2024, 1, 1)]) == date(2023, 1, 2) and earliest([]) is None, "Неверный результат"
        """,
        """
        from datetime import date


        def earliest(dates):
            return min(dates) if dates else None
        """),
    cod(f"{P}-date-e8", t("""
        Напиши функцию `quarter(d)` — номер квартала (1–4) для даты: январь–март — 1, апрель–июнь — 2 и т. д. Затем функцию `same_quarter(a, b)` — `True`, если две даты в одном квартале **одного года**.
        """),
        """
        from datetime import date


        def quarter(d):
            pass


        def same_quarter(a, b):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert [quarter(date(2024, m, 1)) for m in (1, 3, 4, 6, 7, 10, 12)] == [1, 1, 2, 2, 3, 4, 4], "quarter"
            assert same_quarter(date(2024, 1, 5), date(2024, 3, 31)) and not same_quarter(date(2024, 1, 5), date(2023, 2, 1)) and not same_quarter(date(2024, 3, 31), date(2024, 4, 1)), "same_quarter"
        """,
        """
        from datetime import date


        def quarter(d):
            return (d.month - 1) // 3 + 1


        def same_quarter(a, b):
            return a.year == b.year and quarter(a) == quarter(b)
        """, xp=20),
),

lesson(f"{P}-datetime", "Дата и время: datetime и time",
    out(f"{P}-datetime-e1", "Что выведет программа?", """
        from datetime import datetime

        dt = datetime(2024, 3, 8, 14, 30, 5)
        print(dt)
        print(dt.hour, dt.minute, dt.second)
        print(dt.date(), dt.time())
        """),
    out(f"{P}-datetime-e2", "Что выведет программа? replace и combine.", """
        from datetime import datetime, date, time

        dt = datetime(2024, 3, 8, 14, 30)
        print(dt.replace(hour=9, minute=0))
        print(dt)
        start = datetime.combine(date(2024, 1, 1), time(10, 15))
        print(start, start.replace(day=31).day)
        """, hint="replace возвращает новый объект — datetime неизменяем."),
    out(f"{P}-datetime-e3", "Что выведет программа? Начало дня и сравнение.", """
        from datetime import datetime, time

        dt = datetime(2024, 3, 8, 14, 30, 45, 123456)
        print(dt.replace(microsecond=0))
        midnight = datetime.combine(dt.date(), time.min)
        print(midnight)
        print(time(9, 0) < time(18, 0) < time(23, 59))
        """),
    cod(f"{P}-datetime-e4", t("""
        Напиши функцию `is_working_hours(dt)` — `True`, если `datetime` попадает в рабочее время: будни, с 9:00 (включительно) до 18:00 (не включительно).
        """),
        """
        from datetime import datetime


        def is_working_hours(dt):
            pass
        """,
        """
        from datetime import datetime

        def test_values():
            assert is_working_hours(datetime(2024, 3, 8, 9, 0)) and is_working_hours(datetime(2024, 3, 8, 17, 59)), "Рабочее время"
            assert not is_working_hours(datetime(2024, 3, 8, 18, 0)) and not is_working_hours(datetime(2024, 3, 8, 8, 59)) and not is_working_hours(datetime(2024, 3, 9, 12, 0)), "Нерабочее"
        """,
        """
        from datetime import datetime, time


        def is_working_hours(dt):
            return dt.weekday() < 5 and time(9, 0) <= dt.time() < time(18, 0)
        """),
    cod(f"{P}-datetime-e5", t("""
        Напиши функцию `start_of_day(dt)` — тот же день, но время `00:00:00.000000`. И `end_of_day(dt)` — время `23:59:59.999999`.
        """),
        """
        from datetime import datetime


        def start_of_day(dt):
            pass


        def end_of_day(dt):
            pass
        """,
        """
        from datetime import datetime

        def test_values():
            dt = datetime(2024, 3, 8, 14, 30, 5, 77)
            assert start_of_day(dt) == datetime(2024, 3, 8) and end_of_day(dt) == datetime(2024, 3, 8, 23, 59, 59, 999999), "Неверные границы"
            assert dt == datetime(2024, 3, 8, 14, 30, 5, 77), "Исходный объект не меняется"
        """,
        """
        from datetime import datetime


        def start_of_day(dt):
            return dt.replace(hour=0, minute=0, second=0, microsecond=0)


        def end_of_day(dt):
            return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        """),
    cod(f"{P}-datetime-e6", t("""
        Напиши функцию `meeting_at(d, hour, minute=0)` — `datetime` встречи в день `d` (объект `date`) в указанное время. Используй `datetime.combine`.
        """),
        """
        from datetime import datetime, date, time


        def meeting_at(d, hour, minute=0):
            pass
        """,
        """
        from datetime import datetime, date

        def test_values():
            assert meeting_at(date(2024, 3, 8), 10) == datetime(2024, 3, 8, 10, 0) and meeting_at(date(2024, 1, 1), 9, 30) == datetime(2024, 1, 1, 9, 30), "Неверный результат"
        """,
        """
        from datetime import datetime, date, time


        def meeting_at(d, hour, minute=0):
            return datetime.combine(d, time(hour, minute))
        """),
    cod(f"{P}-datetime-e7", t("""
        Напиши функцию `part_of_day(dt)`: `"ночь"` (0:00–5:59), `"утро"` (6:00–11:59), `"день"` (12:00–17:59), `"вечер"` (18:00–23:59).
        """),
        """
        def part_of_day(dt):
            pass
        """,
        """
        from datetime import datetime

        def test_values():
            hours = [0, 5, 6, 11, 12, 17, 18, 23]
            assert [part_of_day(datetime(2024, 1, 1, h, 30)) for h in hours] == ["ночь", "ночь", "утро", "утро", "день", "день", "вечер", "вечер"], "Неверный результат"
        """,
        """
        def part_of_day(dt):
            if dt.hour < 6:
                return "ночь"
            if dt.hour < 12:
                return "утро"
            if dt.hour < 18:
                return "день"
            return "вечер"
        """),
    cod(f"{P}-datetime-e8", t("""
        Напиши функцию `group_by_date(events)` — `events` — список `datetime`. Верни словарь «дата (`date`) → список времён (`time`) по возрастанию». Ключи — в порядке возрастания дат.
        """),
        """
        def group_by_date(events):
            pass
        """,
        """
        from datetime import datetime, date, time

        def test_values():
            ev = [datetime(2024, 3, 9, 10), datetime(2024, 3, 8, 15), datetime(2024, 3, 8, 9, 30)]
            r = group_by_date(ev)
            assert r == {date(2024, 3, 8): [time(9, 30), time(15)], date(2024, 3, 9): [time(10)]} and list(r) == [date(2024, 3, 8), date(2024, 3, 9)], r
            assert group_by_date([]) == {}, "Пустой список"
        """,
        """
        def group_by_date(events):
            result = {}
            for dt in sorted(events):
                result.setdefault(dt.date(), []).append(dt.time())
            return result
        """, xp=20),
),

lesson(f"{P}-format", "Форматирование: strftime и isoformat",
    out(f"{P}-format-e1", "Что выведет программа?", """
        from datetime import datetime

        dt = datetime(2024, 3, 8, 9, 5, 7)
        print(dt.strftime("%d.%m.%Y"))
        print(dt.strftime("%H:%M:%S"))
        print(dt.strftime("%Y-%m-%d %H:%M"))
        print(dt.strftime("%d/%m/%y"))
        """, hint="%d, %m, %H, %M, %S — всегда две цифры, с ведущим нулём."),
    out(f"{P}-format-e2", "Что выведет программа? isoformat и f-строки.", """
        from datetime import datetime, date

        dt = datetime(2024, 3, 8, 9, 5)
        print(dt.isoformat())
        print(date(2024, 3, 8).isoformat())
        print(f"{dt:%d.%m.%Y}", f"{dt:%H:%M}")
        print(str(dt))
        """),
    out(f"{P}-format-e3", "Что выведет программа? Названия и номера.", """
        from datetime import date

        d = date(2024, 3, 8)
        print(d.strftime("%A, %B"))
        print(d.strftime("%a %b"))
        print(d.strftime("%j"), d.strftime("%w"))
        print(d.strftime("%%Y = %Y"))
        """, hint="Названия дней и месяцев — английские (зависят от языка системы)."),
    cod(f"{P}-format-e4", t("""
        Напиши функцию `ru_date(d)` — дата в формате `"08.03.2024"` (объект `date` или `datetime`).
        """),
        """
        def ru_date(d):
            pass
        """,
        """
        from datetime import date, datetime

        def test_values():
            assert ru_date(date(2024, 3, 8)) == "08.03.2024" and ru_date(datetime(2023, 12, 31, 23, 0)) == "31.12.2023", "Неверный формат"
        """,
        """
        def ru_date(d):
            return d.strftime("%d.%m.%Y")
        """),
    cod(f"{P}-format-e5", t("""
        Напиши функцию `log_line(dt, level, msg)` — строка лога вида `"[2024-03-08 09:05:07] ERROR: текст"`. Уровень — заглавными буквами.
        """),
        """
        def log_line(dt, level, msg):
            pass
        """,
        """
        from datetime import datetime

        def test_values():
            assert log_line(datetime(2024, 3, 8, 9, 5, 7), "error", "упал тест") == "[2024-03-08 09:05:07] ERROR: упал тест", log_line(datetime(2024, 3, 8, 9, 5, 7), "error", "упал тест")
        """,
        """
        def log_line(dt, level, msg):
            return f"[{dt:%Y-%m-%d %H:%M:%S}] {level.upper()}: {msg}"
        """),
    cod(f"{P}-format-e6", t("""
        Напиши функцию `human_date(d)` — дата по-русски: `"8 марта 2024"` (день без ведущего нуля, месяц в родительном падеже). Не используй `%B` — названия месяцев зависят от языка системы; возьми их из своего списка.
        """),
        """
        MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня",
                  "июля", "августа", "сентября", "октября", "ноября", "декабря"]


        def human_date(d):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert human_date(date(2024, 3, 8)) == "8 марта 2024" and human_date(date(2023, 12, 31)) == "31 декабря 2023" and human_date(date(2024, 1, 1)) == "1 января 2024", "Неверный формат"
        """,
        """
        MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня",
                  "июля", "августа", "сентября", "октября", "ноября", "декабря"]


        def human_date(d):
            return f"{d.day} {MONTHS[d.month - 1]} {d.year}"
        """),
    cod(f"{P}-format-e7", t("""
        Напиши функцию `report_name(dt, prefix="report")` — имя файла отчёта: `"report_2024-03-08_09-05.html"`. В имени не должно быть двоеточий (Windows их не разрешает).
        """),
        """
        def report_name(dt, prefix="report"):
            pass
        """,
        """
        from datetime import datetime

        def test_values():
            assert report_name(datetime(2024, 3, 8, 9, 5, 59)) == "report_2024-03-08_09-05.html" and report_name(datetime(2024, 12, 1, 23, 0), "allure") == "allure_2024-12-01_23-00.html", "Неверное имя"
        """,
        """
        def report_name(dt, prefix="report"):
            return f"{prefix}_{dt:%Y-%m-%d_%H-%M}.html"
        """),
    cod(f"{P}-format-e8", t("""
        Напиши функцию `api_timestamp(dt)` — строка для API в формате ISO 8601 **без микросекунд**: `"2024-03-08T09:05:07"`. Используй `isoformat` (у него есть параметр `timespec`).
        """),
        """
        def api_timestamp(dt):
            pass
        """,
        """
        from datetime import datetime

        def test_values():
            assert api_timestamp(datetime(2024, 3, 8, 9, 5, 7, 123456)) == "2024-03-08T09:05:07" and api_timestamp(datetime(2024, 1, 1)) == "2024-01-01T00:00:00", "Неверный формат"
        """,
        """
        def api_timestamp(dt):
            return dt.isoformat(timespec="seconds")
        """, hint='dt.isoformat(timespec="seconds")', xp=20),
),

lesson(f"{P}-parse", "Разбор строк: strptime и fromisoformat",
    out(f"{P}-parse-e1", "Что выведет программа?", """
        from datetime import datetime

        dt = datetime.strptime("08.03.2024 14:30", "%d.%m.%Y %H:%M")
        print(dt)
        print(repr(dt))
        print(datetime.strptime("2024-03-08", "%Y-%m-%d").date())
        """, hint="strptime — string parse time: строка + формат → datetime."),
    out(f"{P}-parse-e2", "Что выведет программа? fromisoformat.", """
        from datetime import datetime, date

        print(date.fromisoformat("2024-03-08"))
        print(datetime.fromisoformat("2024-03-08T14:30:00"))
        print(datetime.fromisoformat("2024-03-08 14:30"))
        print(datetime.fromisoformat("2024-03-08T14:30:00Z"))
        """, hint="Буква Z в конце означает время UTC."),
    out(f"{P}-parse-e3", "Что выведет программа? Ошибки разбора.", """
        from datetime import datetime

        tests = ["31.12.2024", "2024-12-31", "32.01.2024", "1.2.2024"]
        for text in tests:
            try:
                print(datetime.strptime(text, "%d.%m.%Y").date())
            except ValueError:
                print("ошибка:", text)
        """, hint="strptime разрешает числа без ведущего нуля, но не несуществующие даты."),
    cod(f"{P}-parse-e4", t("""
        Напиши функцию `parse_ru(text)` — разобрать дату вида `"08.03.2024"` и вернуть объект `date`.
        """),
        """
        from datetime import datetime


        def parse_ru(text):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert parse_ru("08.03.2024") == date(2024, 3, 8) and parse_ru("31.12.1999") == date(1999, 12, 31) and type(parse_ru("01.01.2000")) is date, "Неверный результат"
        """,
        """
        from datetime import datetime


        def parse_ru(text):
            return datetime.strptime(text, "%d.%m.%Y").date()
        """),
    cod(f"{P}-parse-e5", t("""
        Напиши функцию `convert(text)` — перевести дату из формата `"2024-03-08"` в `"08.03.2024"`.
        """),
        """
        from datetime import date


        def convert(text):
            pass
        """,
        """
        def test_values():
            assert convert("2024-03-08") == "08.03.2024" and convert("1999-12-31") == "31.12.1999", "Неверный результат"
        """,
        """
        from datetime import date


        def convert(text):
            return date.fromisoformat(text).strftime("%d.%m.%Y")
        """),
    cod(f"{P}-parse-e6", t("""
        Напиши функцию `parse_any(text)` — попробовать разобрать дату в одном из форматов: `"%d.%m.%Y"`, `"%Y-%m-%d"`, `"%d/%m/%Y"`. Вернуть `date` для первого подошедшего формата или `None`, если ни один не подошёл.
        """),
        """
        from datetime import datetime

        FORMATS = ["%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"]


        def parse_any(text):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert parse_any("08.03.2024") == date(2024, 3, 8) and parse_any("2024-03-08") == date(2024, 3, 8) and parse_any("08/03/2024") == date(2024, 3, 8), "Форматы"
            assert parse_any("вчера") is None and parse_any("30.02.2024") is None, "Неразборные"
        """,
        """
        from datetime import datetime

        FORMATS = ["%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"]


        def parse_any(text):
            for fmt in FORMATS:
                try:
                    return datetime.strptime(text, fmt).date()
                except ValueError:
                    pass
            return None
        """),
    cod(f"{P}-parse-e7", t("""
        Напиши функцию `is_iso_datetime(text)` — `True`, если строка — корректная дата-время ISO (разбирается `datetime.fromisoformat`), иначе `False`. Используется для проверки поля `created_at` в ответе API.
        """),
        """
        from datetime import datetime


        def is_iso_datetime(text):
            pass
        """,
        """
        def test_values():
            good = ["2024-03-08T14:30:00", "2024-03-08T14:30:00Z", "2024-03-08"]
            bad = ["08.03.2024", "2024-13-01T00:00:00", "", "сегодня"]
            assert all(is_iso_datetime(s) for s in good) and not any(is_iso_datetime(s) for s in bad), "Неверная проверка"
        """,
        """
        from datetime import datetime


        def is_iso_datetime(text):
            try:
                datetime.fromisoformat(text)
            except ValueError:
                return False
            return True
        """),
    cod(f"{P}-parse-e8", t("""
        Напиши функцию `parse_log(lines)` — каждая строка вида `"2024-03-08 14:30:05 ERROR текст"`. Верни список кортежей `(datetime, уровень)` только для строк с уровнем `ERROR`, отсортированный по времени.
        """),
        """
        from datetime import datetime


        def parse_log(lines):
            pass
        """,
        """
        from datetime import datetime

        def test_values():
            lines = [
                "2024-03-08 14:30:05 ERROR база недоступна",
                "2024-03-08 14:29:00 INFO старт",
                "2024-03-08 09:00:00 ERROR таймаут",
            ]
            assert parse_log(lines) == [(datetime(2024, 3, 8, 9, 0), "ERROR"), (datetime(2024, 3, 8, 14, 30, 5), "ERROR")] and parse_log([]) == [], parse_log(lines)
        """,
        """
        from datetime import datetime


        def parse_log(lines):
            result = []
            for line in lines:
                day, clock, level, _ = line.split(" ", 3)
                if level == "ERROR":
                    dt = datetime.strptime(f"{day} {clock}", "%Y-%m-%d %H:%M:%S")
                    result.append((dt, level))
            return sorted(result)
        """, xp=20),
),
)
