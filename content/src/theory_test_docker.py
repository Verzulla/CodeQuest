"""Теория темы «Docker для тестировщика»: полный урок (full), шпаргалка (short) и «Проверь себя» (quiz)
для каждого урока. Разложена по модулям в _dkr_t1.py … _dkr_t4.py; build.py подставляет её в уроки."""
from ._dkr_t1 import T as T1
from ._dkr_t2 import T as T2
from ._dkr_t3 import T as T3
from ._dkr_t4 import T as T4

THEORY = {**T1, **T2, **T3, **T4}
