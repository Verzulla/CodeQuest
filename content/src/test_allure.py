"""Тема «Allure и отчёты».

Задания — по модулям в _alr_m1.py … _alr_m3.py, теория — в theory_test_allure.py
(она собирает _alr_t1.py … _alr_t3.py)."""
from ._lib import topic
from ._alr_m1 import m1
from ._alr_m2 import m2
from ._alr_m3 import m3

TOPIC = topic("test-allure", "Allure и отчёты", "📊", "#ff9600",
              "allure-pytest, шаги, вложения, метки и ссылки, generate/serve и история, статусы и категории, JUnit XML, сводка и quality gate, Allure в CI, сервер отчётов, уведомления, conftest для отчётов",
              m1, m2, m3, group="Тестирование")
