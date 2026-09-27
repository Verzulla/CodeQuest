"""Теория темы «Условные операторы»: полный урок (full), шпаргалка (short) и «Проверь себя» (quiz)
для каждого урока. Разложена по модулям в _cnd_t1.py … _cnd_t3.py; build.py подставляет её в уроки."""
from ._cnd_t1 import T as T1
from ._cnd_t2 import T as T2
from ._cnd_t3 import T as T3

THEORY = {**T1, **T2, **T3}
