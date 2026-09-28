"""Тема «Linux и терминал».

Задания — по модулям в _lnx_m1.py … _lnx_m3.py, теория — в theory_tools_linux.py
(она собирает _lnx_t1.py … _lnx_t3.py)."""
from ._lib import topic
from ._lnx_m1 import m1
from ._lnx_m2 import m2
from ._lnx_m3 import m3

TOPIC = topic("tools-linux", "Linux и терминал", "🐧", "#4b4b4b",
              "Пути и cd, ls, файлы и папки, cat/head/tail, grep, конвейеры и перенаправление, find, sort/uniq/cut/awk/sed, права и sudo, процессы и порты, переменные окружения, curl, ssh, диск и архивы",
              m1, m2, m3, group="Инструменты")
