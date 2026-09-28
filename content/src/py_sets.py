"""Тема «Множества».

Задания — по модулям в _set_m1.py … _set_m3.py, теория — в theory_py_sets.py
(она собирает _set_t1.py … _set_t3.py)."""
from ._lib import topic
from ._set_m1 import m1
from ._set_m2 import m2
from ._set_m3 import m3

TOPIC = topic("py-sets", "Множества", "🔵", "#00cd9c",
              "Уникальные значения, быстрые проверки, объединение, пересечение, разность, подмножества, frozenset",
              m1, m2, m3, group="Python")
