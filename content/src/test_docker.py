"""Тема «Docker для тестировщика» (вместе с test_cicd.py заменила старую «Docker и CI/CD»;
её слаги dci-m1-* сохранены здесь ради прогресса).

Задания — по модулям в _dkr_m1.py … _dkr_m3.py, теория — в theory_test_docker.py
(она собирает _dkr_t1.py … _dkr_t3.py)."""
from ._lib import topic
from ._dkr_m1 import m1
from ._dkr_m2 import m2
from ._dkr_m3 import m3

TOPIC = topic("test-docker", "Docker для тестировщика", "🐳", "#2496ed",
              "Образы и контейнеры, порты, переменные и тома, диагностика и реестры; Dockerfile, слои и кэш, автотесты в контейнере, размер и безопасность; Docker Compose и тестовый стенд",
              m1, m2, m3, group="Тестирование")
