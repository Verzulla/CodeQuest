"""Тема «Область видимости переменных».

Задания — по модулям в _scp_m1.py … _scp_m3.py, теория — в theory_py_scope.py
(она собирает _scp_t1.py … _scp_t3.py)."""
from ._lib import topic
from ._scp_m1 import m1
from ._scp_m2 import m2
from ._scp_m3 import m3

TOPIC = topic("py-scope", "Область видимости переменных", "🔭", "#ff4b4b",
              "Локальные и глобальные, параметры, UnboundLocalError, global, LEGB, вложенные функции, nonlocal, замыкания, del, модули",
              m1, m2, m3, group="Python")
