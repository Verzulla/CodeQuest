"""Теория темы «Область видимости»: полный урок (full), шпаргалка (short) и «Проверь себя» (quiz)
для каждого урока. Разложена по модулям в _scp_t1.py … _scp_t3.py; build.py подставляет её в уроки."""
from ._scp_t1 import T as T1
from ._scp_t2 import T as T2
from ._scp_t3 import T as T3

THEORY = {**T1, **T2, **T3}
