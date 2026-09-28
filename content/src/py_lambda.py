"""Тема «lambda» (заменила старую «Лямбда-функции»; слаги lam-* сохранены ради прогресса).

Задания — по модулям в _lam_m1.py … _lam_m3.py, теория — в theory_py_lambda.py
(она собирает _lam_t1.py … _lam_t3.py)."""
from ._lib import topic
from ._lam_m1 import m1
from ._lam_m2 import m2
from ._lam_m3 import m3

TOPIC = topic("py-lambda", "lambda", "λ", "#ce82ff",
              "Анонимные функции, колбэки, ключи сортировки, map/filter/reduce, operator и partial, диспетчеры и ловушки",
              m1, m2, m3, group="Python")
