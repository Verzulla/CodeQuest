"""Тема «Словари».

Задания — по модулям в _dct_m1.py … _dct_m3.py, теория — в theory_py_dicts.py
(она собирает _dct_t1.py … _dct_t3.py)."""
from ._lib import topic
from ._dct_m1 import m1
from ._dct_m2 import m2
from ._dct_m3 import m3

TOPIC = topic("py-dicts", "Словари", "📖", "#ffc800",
              "Ключи и значения, создание, get, тонкости ключей, перебор, подсчёт, сортировка, вложенность, слияние, сравнение, проверки API",
              m1, m2, m3, group="Python")
