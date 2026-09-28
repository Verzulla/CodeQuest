"""Тема «Классы» (заменила старую «ООП», слаги oop-* сохранены ради прогресса).

Задания — по модулям в _oop_m1.py … _oop_m3.py, теория — в theory_py_classes.py
(она собирает _oop_t1.py … _oop_t3.py)."""
from ._lib import topic
from ._oop_m1 import m1
from ._oop_m2 import m2
from ._oop_m3 import m3

TOPIC = topic("py-classes", "Классы", "🏛️", "#ff4b4b",
              "Классы и объекты, __init__, методы, атрибуты класса, наследование, полиморфизм, ABC, композиция, dunder-методы, property, dataclass, Page Object",
              m1, m2, m3, group="Python")
