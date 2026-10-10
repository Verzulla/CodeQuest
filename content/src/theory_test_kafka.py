"""Теория темы «Kafka для тестировщика»: полный урок (full), шпаргалка (short) и «Проверь себя» (quiz).
Разложена по модулям в _kfk_t1.py … _kfk_t3.py; build.py подставляет её в уроки."""
from ._kfk_t1 import T as T1
from ._kfk_t2 import T as T2
from ._kfk_t3 import T as T3

THEORY = {**T1, **T2, **T3}
