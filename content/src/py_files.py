"""Тема «Файлы».

Задания — по модулям в _fil_m1.py … _fil_m3.py, теория — в theory_py_files.py
(она собирает _fil_t1.py … _fil_t3.py)."""
from ._lib import topic
from ._fil_m1 import m1
from ._fil_m2 import m2
from ._fil_m3 import m3

TOPIC = topic("py-files", "Файлы", "📂", "#ff9600",
              "open и with, режимы, чтение по строкам, запись, кодировки и байты, pathlib, папки и поиск, os и shutil, ошибки, CSV, большие логи, tempfile и StringIO, конфиги",
              m1, m2, m3, group="Python")
