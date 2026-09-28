"""Тема «Дата и время».

Задания — по модулям в _dt_m1.py … _dt_m3.py, теория — в theory_py_datetime.py
(она собирает _dt_t1.py … _dt_t3.py)."""
from ._lib import topic
from ._dt_m1 import m1
from ._dt_m2 import m2
from ._dt_m3 import m3

TOPIC = topic("py-datetime", "Дата и время", "📅", "#2b70c9",
              "date, datetime, time, strftime и strptime, ISO, timedelta, разница дат, calendar, рабочие дни, часовые пояса, timestamp, даты в API, тесты со временем",
              m1, m2, m3, group="Python")
