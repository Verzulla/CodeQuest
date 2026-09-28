"""Тема «sorted, filter и map».

Задания — по модулям в _srt_m1.py … _srt_m3.py, теория — в theory_py_sorted.py
(она собирает _srt_t1.py … _srt_t3.py)."""
from ._lib import topic
from ._srt_m1 import m1
from ._srt_m2 import m2
from ._srt_m3 import m3

TOPIC = topic("py-sorted", "sorted, filter и map", "🔢", "#ff9600",
              "Сортировка с key и по нескольким признакам, filter и map, min/max, reversed, zip, any/all, конвейеры данных",
              m1, m2, m3, group="Python")
