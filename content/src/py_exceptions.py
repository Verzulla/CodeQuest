"""Тема «Исключения».

Задания — по модулям в _exc_m1.py … _exc_m3.py, теория — в theory_py_exceptions.py
(она собирает _exc_t1.py … _exc_t3.py)."""
from ._lib import topic
from ._exc_m1 import m1
from ._exc_m2 import m2
from ._exc_m3 import m3

TOPIC = topic("py-exceptions", "Исключения", "🧯", "#ff4b4b",
              "Типы ошибок, try/except/else/finally, иерархия, raise, свои исключения, цепочки, assert, EAFP, исключения в тестах",
              m1, m2, m3, group="Python")
