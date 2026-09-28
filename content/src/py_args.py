"""Тема «*args и **kwargs».

Задания — по модулям в _arg_m1.py … _arg_m3.py, теория — в theory_py_args.py
(она собирает _arg_t1.py … _arg_t3.py)."""
from ._lib import topic
from ._arg_m1 import m1
from ._arg_m2 import m2
from ._arg_m3 import m3

TOPIC = topic("py-args", "*args и **kwargs", "✳️", "#7c5cff",
              "Любое число аргументов, звёздочки при вызове, полная сигнатура функции, обёртки и фабрики данных",
              m1, m2, m3, group="Python")
