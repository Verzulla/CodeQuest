"""Тема «Функции».

Задания — по модулям в _fn_m1.py … _fn_m3.py, теория — в theory_py_functions.py
(она собирает _fn_t1.py … _fn_t3.py)."""
from ._lib import topic
from ._fn_m1 import m1
from ._fn_m2 import m2
from ._fn_m3 import m3

TOPIC = topic("py-functions", "Функции", "🧰", "#e05ab0",
              "def, параметры и аргументы, return, значения по умолчанию, документация, функции как объекты, рекурсия, тесты",
              m1, m2, m3, group="Python")
