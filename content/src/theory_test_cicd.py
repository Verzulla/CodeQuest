"""Теория темы «CI/CD для тестировщика»: полный урок (full), шпаргалка (short) и «Проверь себя» (quiz)
для каждого урока. Разложена по модулям в _ci_t1.py … _ci_t3.py; build.py подставляет её в уроки."""
from ._ci_t1 import T as T1
from ._ci_t2 import T as T2
from ._ci_t3 import T as T3

THEORY = {**T1, **T2, **T3}
