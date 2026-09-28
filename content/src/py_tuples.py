"""Тема «Кортежи».

Задания — по модулям в _tpl_m1.py … _tpl_m3.py, теория — в theory_py_tuples.py
(она собирает _tpl_t1.py … _tpl_t3.py)."""
from ._lib import topic
from ._tpl_m1 import m1
from ._tpl_m2 import m2
from ._tpl_m3 import m3

TOPIC = topic("py-tuples", "Кортежи", "📎", "#ff86d0",
              "Неизменяемые последовательности, распаковка, преобразования, ключи словаря, сортировка, namedtuple",
              m1, m2, m3, group="Python")
