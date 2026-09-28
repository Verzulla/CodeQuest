"""Тема «Списковые включения».

Задания — по модулям в _cmp_m1.py … _cmp_m3.py, теория — в theory_py_comprehensions.py
(она собирает _cmp_t1.py … _cmp_t3.py)."""
from ._lib import topic
from ._cmp_m1 import m1
from ._cmp_m2 import m2
from ._cmp_m3 import m3

TOPIC = topic("py-comprehensions", "Списковые включения", "🧺", "#58cc02",
              "Включения списков, словарей и множеств, фильтры, вложенность, выражения-генераторы и читаемость",
              m1, m2, m3, group="Python")
