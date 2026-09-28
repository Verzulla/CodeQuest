"""Тема «Списки».

Задания — по модулям в _lst_m1.py … _lst_m3.py, теория — в theory_py_lists.py
(она собирает _lst_t1.py … _lst_t3.py)."""
from ._lib import topic
from ._lst_m1 import m1
from ._lst_m2 import m2
from ._lst_m3 import m3, m4

TOPIC = topic("py-lists", "Списки", "📋", "#1cb0f6",
              "Создание, индексы, добавление и удаление, перебор, поиск, сортировка, ссылки, стек и очередь",
              m1, m2, m3, m4, group="Python")
