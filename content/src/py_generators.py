"""Тема «Генераторы» (заменила старую, слаги gen-* сохранены ради прогресса).

Задания — по модулям в _gen_m1.py … _gen_m3.py, теория — в theory_py_generators.py
(она собирает _gen_t1.py … _gen_t3.py)."""
from ._lib import topic
from ._gen_m1 import m1
from ._gen_m2 import m2
from ._gen_m3 import m3

TOPIC = topic("py-generators", "Генераторы", "🔁", "#58cc02",
              "Итераторы, iter и next, свой итератор, yield, ленивость, генераторные выражения, конвейеры, yield from, itertools, send и close, большие данные, память, генераторы в тестах",
              m1, m2, m3, group="Python")
