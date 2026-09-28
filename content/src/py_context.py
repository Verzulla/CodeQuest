"""Тема «Контекстные менеджеры» (заменила старую, слаги ctx-* сохранены ради прогресса).

Задания — по модулям в _ctx_m1.py … _ctx_m3.py, теория — в theory_py_context.py
(она собирает _ctx_t1.py … _ctx_t3.py)."""
from ._lib import topic
from ._ctx_m1 import m1
from ._ctx_m2 import m2
from ._ctx_m3 import m3

TOPIC = topic("py-context", "Контекстные менеджеры", "🚪", "#00a88e",
              "with и try/finally, несколько менеджеров, __enter__ и __exit__, исключения, @contextmanager, suppress, redirect_stdout, ExitStack, closing, временная подмена, таймеры, менеджеры в тестах",
              m1, m2, m3, group="Python")
