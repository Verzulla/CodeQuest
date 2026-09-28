"""Тема «Дата и время», модуль 3 «Пояса, timestamp и тесты» — задания. Теория — в _dt_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "dt"

m3 = module(f"{P}-m3", "Пояса, timestamp и тесты", "🌍", "Часовые пояса, Unix-время, даты в API и JSON, тесты, зависящие от времени",

lesson(f"{P}-timezone", "Часовые пояса",
    out(f"{P}-timezone-e1", "Что выведет программа?", """
        from datetime import datetime, timezone, timedelta

        naive = datetime(2024, 3, 8, 12, 0)
        utc = datetime(2024, 3, 8, 12, 0, tzinfo=timezone.utc)
        print(naive.tzinfo, utc.tzinfo)
        print(utc)
        msk = timezone(timedelta(hours=3))
        print(utc.astimezone(msk))
        """, hint="+00:00 и +03:00 — смещение от UTC."),
    out(f"{P}-timezone-e2", "Что выведет программа? Один момент — разные часы.", """
        from datetime import datetime, timezone, timedelta

        msk = timezone(timedelta(hours=3), "MSK")
        ny = timezone(timedelta(hours=-5), "NY")
        a = datetime(2024, 3, 8, 15, 0, tzinfo=msk)
        b = datetime(2024, 3, 8, 7, 0, tzinfo=ny)
        print(a == b, a - b)
        print(b.astimezone(msk).strftime("%H:%M %Z"))
        """, hint="Aware-даты сравниваются как моменты времени, а не как цифры на часах."),
    out(f"{P}-timezone-e3", "Что выведет программа? Смешивать нельзя.", """
        from datetime import datetime, timezone

        naive = datetime(2024, 3, 8, 12, 0)
        aware = datetime(2024, 3, 8, 12, 0, tzinfo=timezone.utc)
        try:
            naive < aware
        except TypeError:
            print("сравнивать naive и aware нельзя")
        print(naive == aware)
        print(naive.replace(tzinfo=timezone.utc) == aware)
        """),
    cod(f"{P}-timezone-e4", t("""
        Напиши функцию `to_utc(dt)` — перевести aware-`datetime` в UTC. Если передан naive (`tzinfo is None`) — выбросить `ValueError("нужен часовой пояс")`.
        """),
        """
        from datetime import datetime, timezone


        def to_utc(dt):
            pass
        """,
        """
        from datetime import datetime, timezone, timedelta

        def test_values():
            msk = timezone(timedelta(hours=3))
            r = to_utc(datetime(2024, 3, 8, 2, 0, tzinfo=msk))
            assert r == datetime(2024, 3, 7, 23, 0, tzinfo=timezone.utc) and r.utcoffset() == timedelta(0), r
            try:
                to_utc(datetime(2024, 3, 8))
            except ValueError as e:
                assert str(e) == "нужен часовой пояс", str(e)
                return
            assert False, "Нужен ValueError"
        """,
        """
        from datetime import datetime, timezone


        def to_utc(dt):
            if dt.tzinfo is None:
                raise ValueError("нужен часовой пояс")
            return dt.astimezone(timezone.utc)
        """),
    cod(f"{P}-timezone-e5", t("""
        Напиши функцию `local_time(utc_dt, offset_hours)` — показать время UTC в поясе со смещением `offset_hours` в виде строки `"ЧЧ:ММ"`.

        ```
        local_time(datetime(2024, 3, 8, 22, 30, tzinfo=timezone.utc), 3)   # → "01:30"
        ```
        """),
        """
        from datetime import datetime, timezone, timedelta


        def local_time(utc_dt, offset_hours):
            pass
        """,
        """
        from datetime import datetime, timezone

        def test_values():
            dt = datetime(2024, 3, 8, 22, 30, tzinfo=timezone.utc)
            assert local_time(dt, 3) == "01:30" and local_time(dt, -5) == "17:30" and local_time(dt, 0) == "22:30", "Неверное время"
        """,
        """
        from datetime import datetime, timezone, timedelta


        def local_time(utc_dt, offset_hours):
            tz = timezone(timedelta(hours=offset_hours))
            return utc_dt.astimezone(tz).strftime("%H:%M")
        """),
    cod(f"{P}-timezone-e6", t("""
        Напиши функцию `same_moment(a, b)` — `True`, если два aware-`datetime` обозначают один и тот же момент, **даже если** пояса разные.
        """),
        """
        def same_moment(a, b):
            pass
        """,
        """
        from datetime import datetime, timezone, timedelta

        def test_values():
            msk = timezone(timedelta(hours=3))
            assert same_moment(datetime(2024, 3, 8, 15, tzinfo=msk), datetime(2024, 3, 8, 12, tzinfo=timezone.utc)), "Один момент"
            assert not same_moment(datetime(2024, 3, 8, 15, tzinfo=msk), datetime(2024, 3, 8, 15, tzinfo=timezone.utc)), "Разные моменты"
        """,
        """
        def same_moment(a, b):
            return a == b
        """, hint="Aware-объекты сравниваются по моменту времени."),
    cod(f"{P}-timezone-e7", t("""
        Напиши функцию `assume_utc(dt)` — если `dt` naive, считать, что он в UTC (прикрепить `timezone.utc`, не меняя цифр); если aware — вернуть как есть.
        """),
        """
        from datetime import datetime, timezone


        def assume_utc(dt):
            pass
        """,
        """
        from datetime import datetime, timezone, timedelta

        def test_values():
            assert assume_utc(datetime(2024, 3, 8, 12)) == datetime(2024, 3, 8, 12, tzinfo=timezone.utc) and assume_utc(datetime(2024, 3, 8, 12)).tzinfo is timezone.utc, "naive"
            msk = datetime(2024, 3, 8, 12, tzinfo=timezone(timedelta(hours=3)))
            assert assume_utc(msk) is msk, "aware не меняется"
        """,
        """
        from datetime import datetime, timezone


        def assume_utc(dt):
            if dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt
        """),
    cod(f"{P}-timezone-e8", t("""
        Напиши функцию `meeting_for_all(utc_dt, offsets)` — `offsets` — словарь «город → смещение в часах». Верни словарь «город → строка `"дд.мм ЧЧ:ММ"`» с местным временем встречи.
        """),
        """
        from datetime import datetime, timezone, timedelta


        def meeting_for_all(utc_dt, offsets):
            pass
        """,
        """
        from datetime import datetime, timezone

        def test_values():
            r = meeting_for_all(datetime(2024, 3, 8, 22, 0, tzinfo=timezone.utc), {"Москва": 3, "Нью-Йорк": -5, "Токио": 9})
            assert r == {"Москва": "09.03 01:00", "Нью-Йорк": "08.03 17:00", "Токио": "09.03 07:00"}, r
        """,
        """
        from datetime import datetime, timezone, timedelta


        def meeting_for_all(utc_dt, offsets):
            result = {}
            for city, hours in offsets.items():
                local = utc_dt.astimezone(timezone(timedelta(hours=hours)))
                result[city] = local.strftime("%d.%m %H:%M")
            return result
        """, xp=20),
),

lesson(f"{P}-timestamp", "Unix-время и модуль time",
    out(f"{P}-timestamp-e1", "Что выведет программа?", """
        from datetime import datetime, timezone

        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        dt = datetime(2024, 3, 8, 12, 0, tzinfo=timezone.utc)
        print(dt.timestamp())
        print((dt - epoch).total_seconds())
        print(datetime.fromtimestamp(0, tz=timezone.utc))
        """, hint="Timestamp — секунды, прошедшие с 1 января 1970 года UTC."),
    out(f"{P}-timestamp-e2", "Что выведет программа? Миллисекунды из API.", """
        from datetime import datetime, timezone

        ms = 1709899200500
        dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
        print(dt)
        print(int(dt.timestamp() * 1000) == ms)
        print(len(str(ms)), len(str(ms // 1000)))
        """, hint="13 цифр — миллисекунды, 10 цифр — секунды."),
    out(f"{P}-timestamp-e3", "Что выведет программа? Модуль time.", """
        import time

        start = time.perf_counter()
        time.sleep(0.05)
        elapsed = time.perf_counter() - start
        print(elapsed >= 0.05, elapsed < 1)
        print(type(time.time()).__name__, time.time() > 1_700_000_000)
        """),
    cod(f"{P}-timestamp-e4", t("""
        Напиши функцию `from_ms(ms)` — перевести timestamp в миллисекундах в aware-`datetime` UTC.
        """),
        """
        from datetime import datetime, timezone


        def from_ms(ms):
            pass
        """,
        """
        from datetime import datetime, timezone

        def test_values():
            assert from_ms(0) == datetime(1970, 1, 1, tzinfo=timezone.utc) and from_ms(1709899200000) == datetime(2024, 3, 8, 12, 0, tzinfo=timezone.utc) and from_ms(1500).microsecond == 500000, "Неверный результат"
        """,
        """
        from datetime import datetime, timezone


        def from_ms(ms):
            return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
        """),
    cod(f"{P}-timestamp-e5", t("""
        Напиши функцию `to_seconds(dt)` — целый Unix-timestamp (секунды) для aware-`datetime`.
        """),
        """
        def to_seconds(dt):
            pass
        """,
        """
        from datetime import datetime, timezone, timedelta

        def test_values():
            assert to_seconds(datetime(2024, 3, 8, 12, tzinfo=timezone.utc)) == 1709899200 and to_seconds(datetime(2024, 3, 8, 15, tzinfo=timezone(timedelta(hours=3)))) == 1709899200 and type(to_seconds(datetime(1970, 1, 1, tzinfo=timezone.utc))) is int, "Неверный результат"
        """,
        """
        def to_seconds(dt):
            return int(dt.timestamp())
        """),
    cod(f"{P}-timestamp-e6", t("""
        Напиши функцию `normalize_ts(value)` — API присылает время то в секундах (10 цифр), то в миллисекундах (13 цифр). Верни aware-`datetime` UTC в обоих случаях. Считай миллисекундами числа больше `10**11`.
        """),
        """
        from datetime import datetime, timezone


        def normalize_ts(value):
            pass
        """,
        """
        from datetime import datetime, timezone

        def test_values():
            expected = datetime(2024, 3, 8, 12, tzinfo=timezone.utc)
            assert normalize_ts(1709899200) == expected and normalize_ts(1709899200000) == expected, "Секунды и миллисекунды"
        """,
        """
        from datetime import datetime, timezone


        def normalize_ts(value):
            if value > 10 ** 11:
                value = value / 1000
            return datetime.fromtimestamp(value, tz=timezone.utc)
        """),
    cod(f"{P}-timestamp-e7", t("""
        Напиши функцию `measure(func)` — вызвать `func()` и вернуть кортеж `(результат, время_в_секундах)`. Время измеряй через `time.perf_counter()`.
        """),
        """
        import time


        def measure(func):
            pass
        """,
        """
        import time as _t

        def test_values():
            result, spent = measure(lambda: (_t.sleep(0.05), "ok")[1])
            assert result == "ok" and 0.04 < spent < 1, f"{result}, {spent}"
        """,
        """
        import time


        def measure(func):
            start = time.perf_counter()
            result = func()
            return result, time.perf_counter() - start
        """),
    cod(f"{P}-timestamp-e8", t("""
        Напиши функцию `is_fresh(ts_seconds, now_seconds, max_age)` — `True`, если запись не старше `max_age` секунд (и не из будущего более чем на 5 секунд — допуск на рассинхрон часов).
        """),
        """
        def is_fresh(ts_seconds, now_seconds, max_age):
            pass
        """,
        """
        def test_values():
            now = 1_700_000_000
            assert is_fresh(now - 60, now, 300) and is_fresh(now - 300, now, 300) and is_fresh(now + 5, now, 300), "Свежие"
            assert not is_fresh(now - 301, now, 300) and not is_fresh(now + 6, now, 300), "Несвежие"
        """,
        """
        def is_fresh(ts_seconds, now_seconds, max_age):
            age = now_seconds - ts_seconds
            return -5 <= age <= max_age
        """, xp=20),
),

lesson(f"{P}-api", "Даты в JSON и API",
    out(f"{P}-api-e1", "Что выведет программа? json не знает дат.", """
        import json
        from datetime import datetime

        data = {"created": datetime(2024, 3, 8, 12, 0)}
        try:
            json.dumps(data)
        except TypeError as e:
            print(e)
        print(json.dumps(data, default=str))
        print(json.dumps({"created": data["created"].isoformat()}))
        """),
    out(f"{P}-api-e2", "Что выведет программа? Разбор ответа API.", """
        import json
        from datetime import datetime

        body = '{"id": 7, "created_at": "2024-03-08T09:30:00Z", "updated_at": "2024-03-08T12:00:00+03:00"}'
        user = json.loads(body)
        created = datetime.fromisoformat(user["created_at"])
        updated = datetime.fromisoformat(user["updated_at"])
        print(created, updated)
        print(updated - created, updated > created)
        """),
    out(f"{P}-api-e3", "Что выведет программа? Свой формат для JSON.", """
        import json
        from datetime import date, datetime

        def encode(value):
            if isinstance(value, (date, datetime)):
                return value.isoformat()
            raise TypeError(f"не умею {type(value).__name__}")

        order = {"id": 1, "day": date(2024, 3, 8), "at": datetime(2024, 3, 8, 9, 0)}
        print(json.dumps(order, default=encode))
        try:
            json.dumps({"s": {1, 2}}, default=encode)
        except TypeError as e:
            print(e)
        """),
    cod(f"{P}-api-e4", t("""
        Напиши функцию `to_json(data)` — `json.dumps` словаря, в котором могут встречаться `date` и `datetime`: они превращаются в ISO-строки. Остальное — как обычно.
        """),
        """
        import json
        from datetime import date, datetime


        def to_json(data):
            pass
        """,
        """
        from datetime import date, datetime

        def test_values():
            assert to_json({"d": date(2024, 3, 8), "t": datetime(2024, 3, 8, 9, 5), "n": 1}) == '{"d": "2024-03-08", "t": "2024-03-08T09:05:00", "n": 1}', to_json({"d": date(2024, 3, 8)})
        """,
        """
        import json
        from datetime import date, datetime


        def to_json(data):
            def encode(value):
                if isinstance(value, (date, datetime)):
                    return value.isoformat()
                raise TypeError(type(value).__name__)
            return json.dumps(data, default=encode)
        """),
    cod(f"{P}-api-e5", t("""
        Напиши функцию `parse_dates(obj, fields)` — вернуть **копию** словаря, в которой поля из списка `fields` (ISO-строки) заменены на `datetime`. Отсутствующие поля пропускать.
        """),
        """
        from datetime import datetime


        def parse_dates(obj, fields):
            pass
        """,
        """
        from datetime import datetime, timezone

        def test_values():
            src = {"id": 1, "created_at": "2024-03-08T09:30:00Z", "name": "Аня"}
            r = parse_dates(src, ["created_at", "deleted_at"])
            assert r == {"id": 1, "created_at": datetime(2024, 3, 8, 9, 30, tzinfo=timezone.utc), "name": "Аня"} and src["created_at"] == "2024-03-08T09:30:00Z", r
        """,
        """
        from datetime import datetime


        def parse_dates(obj, fields):
            result = dict(obj)
            for field in fields:
                if field in result:
                    result[field] = datetime.fromisoformat(result[field])
            return result
        """),
    cod(f"{P}-api-e6", t("""
        Напиши функцию `check_timestamps(user)` — проверка ответа API. Вернуть список ошибок (пустой, если всё хорошо):

        - `"created_at: не ISO"` — если поле не разбирается;
        - `"updated_at: не ISO"` — то же;
        - `"updated_at раньше created_at"` — если обе даты разобрались, но порядок неверный.
        """),
        """
        from datetime import datetime


        def check_timestamps(user):
            pass
        """,
        """
        def test_values():
            assert check_timestamps({"created_at": "2024-03-08T09:00:00Z", "updated_at": "2024-03-08T10:00:00Z"}) == [], "Корректный"
            assert check_timestamps({"created_at": "вчера", "updated_at": "2024-03-08T10:00:00Z"}) == ["created_at: не ISO"], "Неверное created_at"
            assert check_timestamps({"created_at": "2024-03-08T09:00:00Z", "updated_at": "2024-03-08T08:00:00Z"}) == ["updated_at раньше created_at"], "Порядок"
            assert check_timestamps({"created_at": "x", "updated_at": "y"}) == ["created_at: не ISO", "updated_at: не ISO"], "Оба неверные"
        """,
        """
        from datetime import datetime


        def check_timestamps(user):
            errors = []
            parsed = {}
            for field in ["created_at", "updated_at"]:
                try:
                    parsed[field] = datetime.fromisoformat(user[field])
                except ValueError:
                    errors.append(f"{field}: не ISO")
            if len(parsed) == 2 and parsed["updated_at"] < parsed["created_at"]:
                errors.append("updated_at раньше created_at")
            return errors
        """),
    cod(f"{P}-api-e7", t("""
        Напиши функцию `utc_iso(dt)` — строка ISO 8601 для отправки в API: всегда в UTC, без микросекунд и с буквой `Z` вместо `+00:00`. На вход приходит aware-`datetime` в любом поясе.

        ```
        utc_iso(datetime(2024, 3, 8, 15, 0, 0, 999, tzinfo=MSK))   # → "2024-03-08T12:00:00Z"
        ```
        """),
        """
        from datetime import datetime, timezone


        def utc_iso(dt):
            pass
        """,
        """
        from datetime import datetime, timezone, timedelta

        def test_values():
            msk = timezone(timedelta(hours=3))
            assert utc_iso(datetime(2024, 3, 8, 15, 0, 0, 999, tzinfo=msk)) == "2024-03-08T12:00:00Z" and utc_iso(datetime(2024, 1, 1, tzinfo=timezone.utc)) == "2024-01-01T00:00:00Z", "Неверный формат"
        """,
        """
        from datetime import datetime, timezone


        def utc_iso(dt):
            return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        """),
    cod(f"{P}-api-e8", t("""
        Напиши функцию `latest_by_user(events)` — `events` — список словарей `{"user": ..., "at": "ISO-строка"}`. Верни словарь «пользователь → самое позднее время (строка в исходном виде)». Сравнивать нужно **моменты времени**, а не строки: пояса могут быть разными.
        """),
        """
        from datetime import datetime


        def latest_by_user(events):
            pass
        """,
        """
        def test_values():
            events = [
                {"user": "аня", "at": "2024-03-08T12:00:00+03:00"},
                {"user": "аня", "at": "2024-03-08T10:00:00Z"},
                {"user": "боря", "at": "2024-03-08T09:00:00Z"},
            ]
            assert latest_by_user(events) == {"аня": "2024-03-08T10:00:00Z", "боря": "2024-03-08T09:00:00Z"} and latest_by_user([]) == {}, latest_by_user(events)
        """,
        """
        from datetime import datetime


        def latest_by_user(events):
            best = {}
            for e in events:
                moment = datetime.fromisoformat(e["at"])
                user = e["user"]
                if user not in best or moment > best[user][0]:
                    best[user] = (moment, e["at"])
            return {user: text for user, (_, text) in best.items()}
        """, hint="Строка '12:00+03:00' больше '10:00Z', но момент — раньше.", xp=20),
),

lesson(f"{P}-testing", "Тесты, зависящие от времени",
    out(f"{P}-testing-e1", "Что выведет программа? Время передаётся параметром.", """
        from datetime import datetime

        def greeting(now):
            if now.hour < 12:
                return "Доброе утро"
            if now.hour < 18:
                return "Добрый день"
            return "Добрый вечер"

        for h in [8, 13, 21]:
            print(greeting(datetime(2024, 3, 8, h)))
        """, hint="Функция не вызывает datetime.now() сама — поэтому её легко проверить в любое время."),
    out(f"{P}-testing-e2", "Что выведет программа? Поддельные часы.", """
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
        clock.advance(minutes=29)
        print(s.is_active())
        clock.advance(minutes=1)
        print(s.is_active())
        """, hint="30 минут «прошли» мгновенно — тест не ждёт."),
    out(f"{P}-testing-e3", "Что выведет программа? Коварные даты.", """
        from datetime import date, timedelta

        edge = [date(2024, 2, 28), date(2023, 12, 31), date(2024, 12, 31)]
        for d in edge:
            print(d, "→", d + timedelta(days=1))
        print(date(2024, 3, 1) - date(2024, 2, 1), date(2023, 3, 1) - date(2023, 2, 1))
        """, hint="Конец месяца, конец года, високосный февраль — классика тест-дизайна."),
    cod(f"{P}-testing-e4", t("""
        Функция `is_expired` из заготовки сама вызывает `datetime.now()` — её невозможно проверить на конкретную дату. Перепиши её: пусть принимает `now` вторым параметром со значением по умолчанию `None`; если `now` не передан — брать `datetime.now()`.
        """),
        """
        from datetime import datetime


        def is_expired(expires_at):
            return datetime.now() > expires_at
        """,
        """
        from datetime import datetime

        def test_values():
            exp = datetime(2024, 3, 8, 12, 0)
            assert is_expired(exp, now=datetime(2024, 3, 8, 12, 1)) and not is_expired(exp, now=datetime(2024, 3, 8, 11, 59)), "С переданным now"
            assert is_expired(datetime(2000, 1, 1)) and not is_expired(datetime(2999, 1, 1)), "Без now — текущее время"
        """,
        """
        from datetime import datetime


        def is_expired(expires_at, now=None):
            if now is None:
                now = datetime.now()
            return now > expires_at
        """, hint="Не пиши now=datetime.now() в сигнатуре — значение вычислится один раз при объявлении."),
    cod(f"{P}-testing-e5", t("""
        Создай класс `FakeClock(start)` с методами `now()` (текущее «время») и `advance(seconds)` (сдвинуть вперёд). И класс `RateLimiter(clock, limit, window_seconds)` с методом `allow()` — разрешает не больше `limit` вызовов за последние `window_seconds` секунд (вызовы старше окна забываются).
        """),
        """
        from datetime import datetime, timedelta


        class FakeClock:
            pass


        class RateLimiter:
            pass
        """,
        """
        from datetime import datetime

        def test_values():
            clock = FakeClock(datetime(2024, 3, 8, 12, 0))
            rl = RateLimiter(clock, 2, 60)
            assert rl.allow() and rl.allow() and not rl.allow(), "Лимит 2"
            clock.advance(59)
            assert not rl.allow(), "Окно ещё не прошло"
            clock.advance(1)
            assert rl.allow(), "Старые вызовы забыты"
        """,
        """
        from datetime import datetime, timedelta


        class FakeClock:
            def __init__(self, start):
                self.current = start

            def now(self):
                return self.current

            def advance(self, seconds):
                self.current += timedelta(seconds=seconds)


        class RateLimiter:
            def __init__(self, clock, limit, window_seconds):
                self.clock = clock
                self.limit = limit
                self.window = timedelta(seconds=window_seconds)
                self.calls = []

            def allow(self):
                now = self.clock.now()
                self.calls = [t for t in self.calls if now - t < self.window]
                if len(self.calls) >= self.limit:
                    return False
                self.calls.append(now)
                return True
        """),
    cod(f"{P}-testing-e6", t("""
        Напиши функцию `billing_period(today)` — период оплаты: с 1-го числа текущего месяца по последний день месяца. Вернуть кортеж двух `date`. Функция должна правильно работать на граничных датах (конец года, високосный февраль) — это и проверят тесты.
        """),
        """
        import calendar
        from datetime import date


        def billing_period(today):
            pass
        """,
        """
        from datetime import date

        def test_values():
            cases = {
                date(2024, 2, 29): (date(2024, 2, 1), date(2024, 2, 29)),
                date(2023, 2, 1): (date(2023, 2, 1), date(2023, 2, 28)),
                date(2024, 12, 31): (date(2024, 12, 1), date(2024, 12, 31)),
                date(2024, 1, 1): (date(2024, 1, 1), date(2024, 1, 31)),
            }
            for day, expected in cases.items():
                assert billing_period(day) == expected, f"{day}: {billing_period(day)}"
        """,
        """
        import calendar
        from datetime import date


        def billing_period(today):
            last = calendar.monthrange(today.year, today.month)[1]
            return today.replace(day=1), today.replace(day=last)
        """),
    cod(f"{P}-testing-e7", t("""
        Напиши функцию `make_order(created_at, **overrides)` — фабрика тестовых заказов. Возвращает словарь:

        - `"created_at"` — переданное время;
        - `"pay_until"` — через 3 дня после `created_at`;
        - `"status"` — `"new"`;

        любые поля можно переопределить через `overrides`.
        """),
        """
        from datetime import timedelta


        def make_order(created_at, **overrides):
            pass
        """,
        """
        from datetime import datetime

        def test_values():
            t0 = datetime(2024, 3, 8, 12)
            assert make_order(t0) == {"created_at": t0, "pay_until": datetime(2024, 3, 11, 12), "status": "new"}, "Значения по умолчанию"
            assert make_order(t0, status="paid")["status"] == "paid" and make_order(t0, pay_until=None)["pay_until"] is None, "overrides"
        """,
        """
        from datetime import timedelta


        def make_order(created_at, **overrides):
            order = {
                "created_at": created_at,
                "pay_until": created_at + timedelta(days=3),
                "status": "new",
            }
            order.update(overrides)
            return order
        """),
    cod(f"{P}-testing-e8", t("""
        Напиши функцию `assert_close(actual, expected, seconds=2)` — проверка «время почти совпадает»: если разница между двумя `datetime` больше `seconds` секунд (в любую сторону), выбросить `AssertionError(f"разница {N} с")`, где N — целое число секунд. Так проверяют поле `created_at`, которое сервер ставит сам.
        """),
        """
        from datetime import datetime


        def assert_close(actual, expected, seconds=2):
            pass
        """,
        """
        from datetime import datetime

        def test_values():
            base = datetime(2024, 3, 8, 12, 0, 0)
            assert_close(datetime(2024, 3, 8, 12, 0, 1), base)
            assert_close(datetime(2024, 3, 8, 11, 59, 58), base)
            try:
                assert_close(datetime(2024, 3, 8, 11, 59, 50), base)
            except AssertionError as e:
                assert str(e) == "разница 10 с", str(e)
                return
            assert False, "Нужен AssertionError"
        """,
        """
        from datetime import datetime


        def assert_close(actual, expected, seconds=2):
            diff = abs((actual - expected).total_seconds())
            if diff > seconds:
                raise AssertionError(f"разница {int(diff)} с")
        """, xp=20),
),
)
