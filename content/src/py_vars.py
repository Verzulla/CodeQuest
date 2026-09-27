"""Тема «Переменные и типы данных».

Задания — по модулям в _vars_m1.py … _vars_m4.py, теория — в theory_py_vars.py
(она собирает _vars_t1.py … _vars_t4.py)."""
from ._lib import topic
from ._vars_m1 import m1
from ._vars_m2 import m2
from ._vars_m3 import m3
from ._vars_m4 import m4

TOPIC = topic("py-vars", "Переменные и типы данных", "📦", "#58cc02",
              "print, ошибки, переменные, функции в заданиях, типы, числа и строки",
              m1, m2, m3, m4, group="Python")
