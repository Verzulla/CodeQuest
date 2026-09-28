"""Тема «Python-проект: зависимости и качество кода».

Задания — по модулям в _prj_m1.py … _prj_m3.py, теория — в theory_tools_project.py
(она собирает _prj_t1.py … _prj_t3.py)."""
from ._lib import topic
from ._prj_m1 import m1
from ._prj_m2 import m2
from ._prj_m3 import m3

TOPIC = topic("tools-project", "Python-проект: pip, uv, ruff", "📦", "#7c5cff",
              "Виртуальное окружение, pip и requirements.txt, pyproject.toml, uv (init, add, sync, run, lock, uvx), запуск скриптов и аргументы, линтер и форматтер ruff, pre-commit",
              m1, m2, m3, group="Инструменты")
