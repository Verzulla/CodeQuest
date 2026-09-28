"""Тема «Дата и время», модуль 2 «Арифметика дат» — задания. Теория — в _dt_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "dt"

m2 = module(f"{P}-m2", "Арифметика дат", "➕", "timedelta, разница дат, календарь и месяцы, диапазоны и рабочие дни",

lesson(f"{P}-timedelta", "Промежуток времени: timedelta",
    out(f"{P}-timedelta-e1", "Что выведет программа?", """
        from datetime import date, timedelta

        d = date(2024, 2, 27)
        print(d + timedelta(days=3))
        print(d - timedelta(weeks=1))
        print(timedelta(days=1, hours=5))
        print(timedelta(hours=36))
        """, hint="2024 — високосный: в феврале 29 дней."),
    out(f"{P}-timedelta-e2", "Что выведет программа? Из чего состоит timedelta.", """
        from datetime import timedelta

        td = timedelta(days=2, hours=3, minutes=30)
        print(td.days, td.seconds)
        print(td.total_seconds())
        print(td.total_seconds() / 3600)
        print(timedelta(minutes=90) > timedelta(hours=1))
        """, hint="Внутри хранятся только дни, секунды и микросекунды."),
    out(f"{P}-timedelta-e3", "Что выведет программа? Арифметика timedelta.", """
        from datetime import datetime, timedelta

        start = datetime(2024, 3, 8, 23, 30)
        print(start + timedelta(minutes=45))
        step = timedelta(minutes=20)
        print(step * 3, step / 2)
        print(timedelta(hours=2) // timedelta(minutes=25))
        print(-timedelta(hours=1))
        """),
    cod(f"{P}-timedelta-e4", t("""
        Напиши функцию `deadline(start, days)` — дата дедлайна через `days` дней после `start` (объект `date`).
        """),
        """
        from datetime import date, timedelta


        def deadline(start, days):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert deadline(date(2024, 2, 27), 3) == date(2024, 3, 1) and deadline(date(2023, 12, 31), 1) == date(2024, 1, 1) and deadline(date(2024, 1, 1), 0) == date(2024, 1, 1), "Неверный результат"
        """,
        """
        from datetime import date, timedelta


        def deadline(start, days):
            return start + timedelta(days=days)
        """),
    cod(f"{P}-timedelta-e5", t("""
        Напиши функцию `to_hms(td)` — перевести `timedelta` в строку `"ЧЧ:ММ:СС"` (часы могут быть больше 24). Микросекунды отбросить.

        ```
        to_hms(timedelta(hours=26, minutes=5, seconds=3))   # → "26:05:03"
        ```
        """),
        """
        from datetime import timedelta


        def to_hms(td):
            pass
        """,
        """
        from datetime import timedelta

        def test_values():
            assert to_hms(timedelta(hours=26, minutes=5, seconds=3)) == "26:05:03" and to_hms(timedelta(seconds=59, microseconds=999)) == "00:00:59" and to_hms(timedelta()) == "00:00:00", "Неверный формат"
        """,
        """
        from datetime import timedelta


        def to_hms(td):
            total = int(td.total_seconds())
            hours, rest = divmod(total, 3600)
            minutes, seconds = divmod(rest, 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        """, hint="divmod(a, b) возвращает (частное, остаток)."),
    cod(f"{P}-timedelta-e6", t("""
        Напиши функцию `total_duration(durations)` — `durations` — список строк `"ММ:СС"` (длительности тестов). Верни общую длительность как `timedelta`.
        """),
        """
        from datetime import timedelta


        def total_duration(durations):
            pass
        """,
        """
        from datetime import timedelta

        def test_values():
            assert total_duration(["01:30", "00:45", "10:00"]) == timedelta(minutes=12, seconds=15) and total_duration([]) == timedelta(0), "Неверная сумма"
        """,
        """
        from datetime import timedelta


        def total_duration(durations):
            total = timedelta()
            for d in durations:
                minutes, seconds = d.split(":")
                total += timedelta(minutes=int(minutes), seconds=int(seconds))
            return total
        """),
    cod(f"{P}-timedelta-e7", t("""
        Напиши функцию `schedule(start, count, interval_minutes)` — список из `count` моментов запуска (`datetime`), начиная со `start`, с шагом `interval_minutes` минут.
        """),
        """
        from datetime import datetime, timedelta


        def schedule(start, count, interval_minutes):
            pass
        """,
        """
        from datetime import datetime

        def test_values():
            r = schedule(datetime(2024, 3, 8, 23, 30), 3, 20)
            assert r == [datetime(2024, 3, 8, 23, 30), datetime(2024, 3, 8, 23, 50), datetime(2024, 3, 9, 0, 10)] and schedule(datetime(2024, 1, 1), 0, 5) == [], r
        """,
        """
        from datetime import datetime, timedelta


        def schedule(start, count, interval_minutes):
            step = timedelta(minutes=interval_minutes)
            return [start + step * i for i in range(count)]
        """),
    cod(f"{P}-timedelta-e8", t("""
        Напиши функцию `human_duration(td)` — длительность словами: `"2 д 3 ч 5 мин"`. Нулевые части не писать; если все части нулевые — `"0 мин"`. Секунды отбросить.
        """),
        """
        from datetime import timedelta


        def human_duration(td):
            pass
        """,
        """
        from datetime import timedelta

        def test_values():
            assert human_duration(timedelta(days=2, hours=3, minutes=5)) == "2 д 3 ч 5 мин", human_duration(timedelta(days=2, hours=3, minutes=5))
            assert human_duration(timedelta(hours=1)) == "1 ч" and human_duration(timedelta(days=1, minutes=1)) == "1 д 1 мин" and human_duration(timedelta(seconds=30)) == "0 мин", "Нулевые части"
        """,
        """
        from datetime import timedelta


        def human_duration(td):
            hours, rest = divmod(td.seconds, 3600)
            minutes = rest // 60
            parts = []
            if td.days:
                parts.append(f"{td.days} д")
            if hours:
                parts.append(f"{hours} ч")
            if minutes:
                parts.append(f"{minutes} мин")
            return " ".join(parts) or "0 мин"
        """, xp=20),
),

lesson(f"{P}-diff", "Разница между датами",
    out(f"{P}-diff-e1", "Что выведет программа?", """
        from datetime import date, datetime

        delta = date(2024, 12, 31) - date(2024, 1, 1)
        print(delta, delta.days)
        d2 = datetime(2024, 3, 8, 18, 0) - datetime(2024, 3, 8, 9, 30)
        print(d2, d2.total_seconds() / 3600)
        print(date(2024, 1, 1) - date(2024, 1, 10))
        """, hint="Разность двух дат — timedelta."),
    out(f"{P}-diff-e2", "Что выведет программа? Нельзя смешивать.", """
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
        """),
    out(f"{P}-diff-e3", "Что выведет программа? Возраст.", """
        from datetime import date

        def age(born, today):
            years = today.year - born.year
            if (today.month, today.day) < (born.month, born.day):
                years -= 1
            return years

        print(age(date(2000, 5, 20), date(2024, 5, 19)))
        print(age(date(2000, 5, 20), date(2024, 5, 20)))
        print((date(2024, 5, 20) - date(2000, 5, 20)).days // 365)
        """, hint="Делить дни на 365 неточно — мешают високосные годы."),
    cod(f"{P}-diff-e4", t("""
        Напиши функцию `days_until(today, event)` — сколько дней осталось до события. Если событие уже прошло — отрицательное число.
        """),
        """
        from datetime import date


        def days_until(today, event):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert days_until(date(2024, 12, 25), date(2025, 1, 1)) == 7 and days_until(date(2024, 1, 1), date(2024, 1, 1)) == 0 and days_until(date(2024, 3, 10), date(2024, 3, 8)) == -2, "Неверный результат"
        """,
        """
        from datetime import date


        def days_until(today, event):
            return (event - today).days
        """),
    cod(f"{P}-diff-e5", t("""
        Напиши функцию `age(born, today)` — полных лет на дату `today`. Учти, был ли уже день рождения в этом году.
        """),
        """
        from datetime import date


        def age(born, today):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert age(date(2000, 5, 20), date(2024, 5, 19)) == 23 and age(date(2000, 5, 20), date(2024, 5, 20)) == 24 and age(date(2000, 12, 31), date(2001, 1, 1)) == 0, "Неверный возраст"
        """,
        """
        from datetime import date


        def age(born, today):
            years = today.year - born.year
            if (today.month, today.day) < (born.month, born.day):
                years -= 1
            return years
        """),
    cod(f"{P}-diff-e6", t("""
        Напиши функцию `is_overdue(deadline, now)` — `True`, если `now` (datetime) позже дедлайна. И `hours_left(deadline, now)` — сколько целых часов осталось (для просроченного — 0).
        """),
        """
        from datetime import datetime


        def is_overdue(deadline, now):
            pass


        def hours_left(deadline, now):
            pass
        """,
        """
        from datetime import datetime

        def test_values():
            dl = datetime(2024, 3, 8, 18, 0)
            assert not is_overdue(dl, datetime(2024, 3, 8, 17, 59)) and is_overdue(dl, datetime(2024, 3, 8, 18, 1)) and not is_overdue(dl, dl), "is_overdue"
            assert hours_left(dl, datetime(2024, 3, 7, 15, 30)) == 26 and hours_left(dl, datetime(2024, 3, 9)) == 0, "hours_left"
        """,
        """
        from datetime import datetime


        def is_overdue(deadline, now):
            return now > deadline


        def hours_left(deadline, now):
            if now >= deadline:
                return 0
            return int((deadline - now).total_seconds() // 3600)
        """),
    cod(f"{P}-diff-e7", t("""
        Напиши функцию `max_gap(dates)` — наибольший промежуток **в днях** между соседними датами (после сортировки). Для списка из менее чем двух дат — 0.
        """),
        """
        def max_gap(dates):
            pass
        """,
        """
        from datetime import date

        def test_values():
            ds = [date(2024, 1, 10), date(2024, 1, 1), date(2024, 2, 1)]
            assert max_gap(ds) == 22 and max_gap([date(2024, 1, 1)]) == 0 and max_gap([]) == 0, max_gap(ds)
        """,
        """
        def max_gap(dates):
            ds = sorted(dates)
            return max(((b - a).days for a, b in zip(ds, ds[1:])), default=0)
        """),
    cod(f"{P}-diff-e8", t("""
        Напиши функцию `sla_report(tickets)` — `tickets` — список словарей `{"id": ..., "opened": datetime, "closed": datetime}`. Верни список id заявок, решённых дольше 24 часов, в исходном порядке.
        """),
        """
        from datetime import timedelta


        def sla_report(tickets):
            pass
        """,
        """
        from datetime import datetime

        def test_values():
            ts = [
                {"id": 1, "opened": datetime(2024, 3, 1, 9), "closed": datetime(2024, 3, 2, 9)},
                {"id": 2, "opened": datetime(2024, 3, 1, 9), "closed": datetime(2024, 3, 2, 9, 1)},
                {"id": 3, "opened": datetime(2024, 3, 1, 9), "closed": datetime(2024, 3, 5)},
            ]
            assert sla_report(ts) == [2, 3] and sla_report([]) == [], sla_report(ts)
        """,
        """
        from datetime import timedelta


        def sla_report(tickets):
            limit = timedelta(hours=24)
            return [t["id"] for t in tickets if t["closed"] - t["opened"] > limit]
        """, xp=20),
),

lesson(f"{P}-calendar", "Месяцы, годы и модуль calendar",
    out(f"{P}-calendar-e1", "Что выведет программа?", """
        import calendar

        print(calendar.isleap(2024), calendar.isleap(1900), calendar.isleap(2000))
        print(calendar.monthrange(2024, 2))
        print(calendar.monthrange(2023, 2)[1])
        """, hint="monthrange → (день недели 1-го числа, количество дней в месяце)."),
    out(f"{P}-calendar-e2", "Что выведет программа? Месяц вперёд.", """
        from datetime import date, timedelta

        d = date(2024, 1, 31)
        print(d + timedelta(days=30))
        try:
            print(d.replace(month=2))
        except ValueError as e:
            print("ошибка:", e)
        """, hint="timedelta не умеет «месяц»: месяцы разной длины."),
    out(f"{P}-calendar-e3", "Что выведет программа? Первый и последний день.", """
        import calendar
        from datetime import date

        d = date(2024, 2, 14)
        first = d.replace(day=1)
        last = d.replace(day=calendar.monthrange(d.year, d.month)[1])
        print(first, last)
        print(calendar.month_abbr[2], calendar.day_abbr[0])
        """),
    cod(f"{P}-calendar-e4", t("""
        Напиши функцию `days_in_month(year, month)` — количество дней в месяце. Используй модуль `calendar`.
        """),
        """
        import calendar


        def days_in_month(year, month):
            pass
        """,
        """
        def test_values():
            assert [days_in_month(2024, m) for m in (1, 2, 4, 12)] == [31, 29, 30, 31] and days_in_month(2023, 2) == 28 and days_in_month(1900, 2) == 28, "Неверный результат"
        """,
        """
        import calendar


        def days_in_month(year, month):
            return calendar.monthrange(year, month)[1]
        """),
    cod(f"{P}-calendar-e5", t("""
        Напиши функцию `last_day(d)` — последний день месяца для даты `d` (объект `date`).
        """),
        """
        import calendar
        from datetime import date


        def last_day(d):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert last_day(date(2024, 2, 10)) == date(2024, 2, 29) and last_day(date(2023, 12, 1)) == date(2023, 12, 31) and last_day(date(2024, 4, 30)) == date(2024, 4, 30), "Неверный результат"
        """,
        """
        import calendar
        from datetime import date


        def last_day(d):
            return d.replace(day=calendar.monthrange(d.year, d.month)[1])
        """),
    cod(f"{P}-calendar-e6", t("""
        Напиши функцию `add_months(d, n)` — сдвинуть дату на `n` месяцев (можно отрицательное). Если в целевом месяце нет такого дня — взять последний день месяца.

        ```
        add_months(date(2024, 1, 31), 1)    # → date(2024, 2, 29)
        add_months(date(2024, 11, 15), 3)   # → date(2025, 2, 15)
        ```
        """),
        """
        import calendar
        from datetime import date


        def add_months(d, n):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert add_months(date(2024, 1, 31), 1) == date(2024, 2, 29) and add_months(date(2024, 11, 15), 3) == date(2025, 2, 15), "Вперёд"
            assert add_months(date(2024, 3, 31), -1) == date(2024, 2, 29) and add_months(date(2024, 1, 10), -1) == date(2023, 12, 10) and add_months(date(2024, 5, 5), 0) == date(2024, 5, 5), "Назад"
        """,
        """
        import calendar
        from datetime import date


        def add_months(d, n):
            index = d.year * 12 + (d.month - 1) + n
            year, month = divmod(index, 12)
            month += 1
            day = min(d.day, calendar.monthrange(year, month)[1])
            return date(year, month, day)
        """, hint="Переведи дату в «номер месяца от нулевого года»: year * 12 + (month - 1)."),
    cod(f"{P}-calendar-e7", t("""
        Напиши функцию `leap_years(start, end)` — список високосных годов в диапазоне `start…end` включительно.
        """),
        """
        import calendar


        def leap_years(start, end):
            pass
        """,
        """
        def test_values():
            assert leap_years(1896, 1912) == [1896, 1904, 1908, 1912] and leap_years(1999, 2001) == [2000] and leap_years(2021, 2023) == [], "Неверный результат"
        """,
        """
        import calendar


        def leap_years(start, end):
            return [y for y in range(start, end + 1) if calendar.isleap(y)]
        """),
    cod(f"{P}-calendar-e8", t("""
        Напиши функцию `month_bounds(year, month)` — кортеж `(первый_день, последний_день)` месяца как объекты `date`. И функцию `in_month(d, year, month)` — принадлежит ли дата месяцу.
        """),
        """
        import calendar
        from datetime import date


        def month_bounds(year, month):
            pass


        def in_month(d, year, month):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert month_bounds(2024, 2) == (date(2024, 2, 1), date(2024, 2, 29)) and month_bounds(2023, 12) == (date(2023, 12, 1), date(2023, 12, 31)), "month_bounds"
            assert in_month(date(2024, 2, 29), 2024, 2) and not in_month(date(2024, 3, 1), 2024, 2) and not in_month(date(2023, 2, 5), 2024, 2), "in_month"
        """,
        """
        import calendar
        from datetime import date


        def month_bounds(year, month):
            last = calendar.monthrange(year, month)[1]
            return date(year, month, 1), date(year, month, last)


        def in_month(d, year, month):
            first, last = month_bounds(year, month)
            return first <= d <= last
        """, xp=20),
),

lesson(f"{P}-ranges", "Диапазоны дат и рабочие дни",
    out(f"{P}-ranges-e1", "Что выведет программа?", """
        from datetime import date, timedelta

        start = date(2024, 2, 27)
        days = [start + timedelta(days=i) for i in range(4)]
        print([d.isoformat() for d in days])
        """),
    out(f"{P}-ranges-e2", "Что выведет программа? Только будни.", """
        from datetime import date, timedelta

        d = date(2024, 3, 7)
        end = date(2024, 3, 12)
        while d <= end:
            if d.weekday() < 5:
                print(d.strftime("%d.%m"), end=" ")
            d += timedelta(days=1)
        print()
        """),
    out(f"{P}-ranges-e3", "Что выведет программа? Понедельник недели.", """
        from datetime import date, timedelta

        for d in [date(2024, 3, 8), date(2024, 3, 11), date(2024, 3, 17)]:
            monday = d - timedelta(days=d.weekday())
            print(d, "→", monday)
        print(date(2024, 3, 8).isocalendar().week)
        """, hint="weekday() — сколько дней прошло с понедельника."),
    cod(f"{P}-ranges-e4", t("""
        Напиши функцию `date_range(start, end)` — список всех дат от `start` до `end` включительно. Если `start > end` — пустой список.
        """),
        """
        from datetime import date, timedelta


        def date_range(start, end):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert date_range(date(2024, 2, 28), date(2024, 3, 1)) == [date(2024, 2, 28), date(2024, 2, 29), date(2024, 3, 1)], "Диапазон"
            assert date_range(date(2024, 1, 1), date(2024, 1, 1)) == [date(2024, 1, 1)] and date_range(date(2024, 1, 2), date(2024, 1, 1)) == [], "Границы"
        """,
        """
        from datetime import date, timedelta


        def date_range(start, end):
            count = (end - start).days + 1
            return [start + timedelta(days=i) for i in range(max(count, 0))]
        """),
    cod(f"{P}-ranges-e5", t("""
        Напиши функцию `count_workdays(start, end)` — количество будних дней (пн–пт) от `start` до `end` включительно.
        """),
        """
        from datetime import date, timedelta


        def count_workdays(start, end):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert count_workdays(date(2024, 3, 4), date(2024, 3, 10)) == 5 and count_workdays(date(2024, 3, 9), date(2024, 3, 10)) == 0 and count_workdays(date(2024, 3, 1), date(2024, 3, 31)) == 21, "Неверный подсчёт"
        """,
        """
        from datetime import date, timedelta


        def count_workdays(start, end):
            count = 0
            d = start
            while d <= end:
                if d.weekday() < 5:
                    count += 1
                d += timedelta(days=1)
            return count
        """),
    cod(f"{P}-ranges-e6", t("""
        Напиши функцию `add_workdays(start, n)` — дата через `n` рабочих дней после `start` (выходные пропускаются, сам `start` не считается).

        ```
        add_workdays(date(2024, 3, 8), 1)   # пятница → понедельник 11.03
        ```
        """),
        """
        from datetime import date, timedelta


        def add_workdays(start, n):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert add_workdays(date(2024, 3, 8), 1) == date(2024, 3, 11) and add_workdays(date(2024, 3, 4), 5) == date(2024, 3, 11) and add_workdays(date(2024, 3, 9), 1) == date(2024, 3, 11) and add_workdays(date(2024, 3, 4), 0) == date(2024, 3, 4), "Неверный результат"
        """,
        """
        from datetime import date, timedelta


        def add_workdays(start, n):
            d = start
            while n > 0:
                d += timedelta(days=1)
                if d.weekday() < 5:
                    n -= 1
            return d
        """),
    cod(f"{P}-ranges-e7", t("""
        Напиши функцию `week_bounds(d)` — кортеж `(понедельник, воскресенье)` недели, в которую попадает дата.
        """),
        """
        from datetime import date, timedelta


        def week_bounds(d):
            pass
        """,
        """
        from datetime import date

        def test_values():
            assert week_bounds(date(2024, 3, 8)) == (date(2024, 3, 4), date(2024, 3, 10)) and week_bounds(date(2024, 3, 4)) == (date(2024, 3, 4), date(2024, 3, 10)) and week_bounds(date(2024, 3, 10)) == (date(2024, 3, 4), date(2024, 3, 10)), "Неверные границы"
        """,
        """
        from datetime import date, timedelta


        def week_bounds(d):
            monday = d - timedelta(days=d.weekday())
            return monday, monday + timedelta(days=6)
        """),
    cod(f"{P}-ranges-e8", t("""
        Напиши функцию `workdays_with_holidays(start, end, holidays)` — список рабочих дат от `start` до `end` включительно: не выходные и не из множества `holidays`.
        """),
        """
        from datetime import date, timedelta


        def workdays_with_holidays(start, end, holidays):
            pass
        """,
        """
        from datetime import date

        def test_values():
            r = workdays_with_holidays(date(2024, 3, 6), date(2024, 3, 12), {date(2024, 3, 8)})
            assert r == [date(2024, 3, 6), date(2024, 3, 7), date(2024, 3, 11), date(2024, 3, 12)], r
        """,
        """
        from datetime import date, timedelta


        def workdays_with_holidays(start, end, holidays):
            result = []
            d = start
            while d <= end:
                if d.weekday() < 5 and d not in holidays:
                    result.append(d)
                d += timedelta(days=1)
            return result
        """, xp=20),
),
)
