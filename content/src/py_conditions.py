"""Тема «Условные операторы».

Задания — по модулям в _cnd_m1.py … _cnd_m3.py, теория — в theory_py_conditions.py
(она собирает _cnd_t1.py … _cnd_t3.py)."""
from ._lib import topic
from ._cnd_m1 import m1
from ._cnd_m2 import m2
from ._cnd_m3 import m3, m4

TOPIC = topic("py-conditions", "Условные операторы", "🔀", "#ff9600",
              "if/elif/else, сравнения, логика, истинность, in, тернарный оператор, := и match/case",
              m1, m2, m3, m4, group="Python")
