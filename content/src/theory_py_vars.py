"""Теория темы «Переменные и типы данных»: полный урок (full), шпаргалка (short) и «Проверь себя» (quiz)
для каждого урока. Разложена по модулям в _vars_t1.py … _vars_t4.py; build.py подставляет её в уроки."""
from ._vars_t1 import T as T1
from ._vars_t2 import T as T2
from ._vars_t3 import T as T3
from ._vars_t4 import T as T4

THEORY = {**T1, **T2, **T3, **T4}
