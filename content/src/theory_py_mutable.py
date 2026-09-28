"""Теория темы «Изменяемые и неизменяемые»: полный урок (full), шпаргалка (short) и «Проверь себя» (quiz)
для каждого урока. Разложена по модулям в _mut_t1.py … _mut_t3.py; build.py подставляет её в уроки."""
from ._mut_t1 import T as T1
from ._mut_t2 import T as T2
from ._mut_t3 import T as T3

THEORY = {**T1, **T2, **T3}
