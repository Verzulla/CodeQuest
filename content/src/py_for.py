"""Тема «Цикл for».

Задания — по модулям в _for_m1.py … _for_m3.py, теория — в theory_py_for.py
(она собирает _for_t1.py … _for_t3.py)."""
from ._lib import topic
from ._for_m1 import m1
from ._for_m2 import m2
from ._for_m3 import m3

TOPIC = topic("py-for", "Цикл for", "🔁", "#00a88e",
              "Перебор коллекций, range и индексы, вложенные циклы, break, continue, else, шаблоны: накопление, минимум, поиск, фильтр",
              m1, m2, m3, group="Python")
