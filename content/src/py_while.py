"""Тема «Цикл while».

Задания — по модулям в _whl_m1.py … _whl_m3.py, теория — в theory_py_while.py
(она собирает _whl_t1.py … _whl_t3.py)."""
from ._lib import topic
from ._whl_m1 import m1
from ._whl_m2 import m2
from ._whl_m3 import m3

TOPIC = topic("py-while", "Цикл while", "🔄", "#2b70c9",
              "while и условие, while или for, счётчики, while True, continue/else, ввод, очереди, два указателя, двоичный поиск, приближения, отладка",
              m1, m2, m3, group="Python")
