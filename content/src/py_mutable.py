"""Тема «Изменяемые и неизменяемые».

Задания — по модулям в _mut_m1.py … _mut_m3.py, теория — в theory_py_mutable.py
(она собирает _mut_t1.py … _mut_t3.py)."""
from ._lib import topic
from ._mut_m1 import m1
from ._mut_m2 import m2
from ._mut_m3 import m3

TOPIC = topic("py-mutable", "Изменяемые и неизменяемые", "🧊", "#1cb0f6",
              "Изменяемые и неизменяемые типы, ссылки и is, операции на месте, хешируемость, аргументы функций, значения по умолчанию, copy и deepcopy, перебор с изменением, frozenset и frozen dataclass, данные в тестах",
              m1, m2, m3, group="Python")
