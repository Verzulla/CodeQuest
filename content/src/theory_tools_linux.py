"""Теория темы «Linux и терминал»: полный урок (full), шпаргалка (short) и «Проверь себя» (quiz)
для каждого урока. Разложена по модулям в _lnx_t1.py … _lnx_t3.py; build.py подставляет её в уроки."""
from ._lnx_t1 import T as T1
from ._lnx_t2 import T as T2
from ._lnx_t3 import T as T3

THEORY = {**T1, **T2, **T3}
