"""Тема «CI/CD для тестировщика» (вместе с test_docker.py заменила старую «Docker и CI/CD»;
её слаги dci-m2-* сохранены здесь ради прогресса).

Задания — по модулям в _ci_m1.py … _ci_m3.py, теория — в theory_test_cicd.py
(она собирает _ci_t1.py … _ci_t3.py)."""
from ._lib import topic
from ._ci_m1 import m1
from ._ci_m2 import m2
from ._ci_m3 import m3

TOPIC = topic("test-cicd", "CI/CD для тестировщика", "🚀", "#8a63d2",
              "Пайплайн и коды выхода, события и ветки, job-ы и параллельность, артефакты и кэш; GitHub Actions: матрицы, секреты, Docker и сервисы; GitLab CI, quality gates, отчёты и уведомления",
              m1, m2, m3, group="Тестирование")
