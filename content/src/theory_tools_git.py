"""Теория темы «Git»: полный урок (full), шпаргалка (short) и «Проверь себя» (quiz)
для каждого урока. Разложена по модулям в _git_t1.py … _git_t3.py; build.py подставляет её в уроки."""
from ._git_t1 import T as T1
from ._git_t2 import T as T2
from ._git_t3 import T as T3

THEORY = {**T1, **T2, **T3}
