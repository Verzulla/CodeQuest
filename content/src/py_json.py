"""Тема «JSON».

Задания — по модулям в _jsn_m1.py … _jsn_m3.py, теория — в theory_py_json.py
(она собирает _jsn_t1.py … _jsn_t3.py)."""
from ._lib import topic
from ._jsn_m1 import m1
from ._jsn_m2 import m2
from ._jsn_m3 import m3

TOPIC = topic("py-json", "JSON", "🧾", "#1cb0f6",
              "Формат JSON, loads и dumps, типы, вложенные данные, файлы, проверка и сравнение ответов API",
              m1, m2, m3, group="Python")
