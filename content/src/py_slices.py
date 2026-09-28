"""Тема «Индексы и слайсы».

Задания — по модулям в _slc_m1.py … _slc_m3.py, теория — в theory_py_slices.py
(она собирает _slc_t1.py … _slc_t3.py)."""
from ._lib import topic
from ._slc_m1 import m1
from ._slc_m2 import m2
from ._slc_m3 import m3

TOPIC = topic("py-slices", "Индексы и слайсы", "✂️", "#ce82ff",
              "Индексы строк, списков и кортежей, срезы с шагом, копии, методы строк, присваивание срезам и окна",
              m1, m2, m3, group="Python")
