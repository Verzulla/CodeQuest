"""Тема «Тестирование UI» на Playwright (заменила старую, слаги ui-* сохранены ради прогресса).

Задания — по модулям в _ui_m1.py … _ui_m3.py, теория — в theory_test_ui.py
(она собирает _ui_t1.py … _ui_t3.py). Код заданий работает на pwfake — учебном Playwright без браузера."""
from ._lib import topic
from ._ui_m1 import m1
from ._ui_m2 import m2
from ._ui_m3 import m3

TOPIC = topic("test-ui", "Тестирование UI", "🎭", "#e05ab0",
              "Playwright: локаторы, автоожидание, действия и expect; Page Object, фикстуры и параметризация; скриншоты, трейсы и Allure; итоговые e2e-тесты магазина",
              m1, m2, m3, group="Тестирование")
