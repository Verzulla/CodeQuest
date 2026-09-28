"""Тема «Декораторы».

Задания — по модулям в _dec_m1.py … _dec_m3.py, теория — в theory_py_decorators.py
(она собирает _dec_t1.py … _dec_t3.py)."""
from ._lib import topic
from ._dec_m1 import m1
from ._dec_m2 import m2
from ._dec_m3 import m3

TOPIC = topic("py-decorators", "Декораторы", "🎁", "#a560f8",
              "Функции как объекты, обёртки, синтаксис @, functools.wraps, логирование, кэш и lru_cache, retry, декораторы с параметрами, порядок, методы и классы, декораторы в тестах",
              m1, m2, m3, group="Python")
