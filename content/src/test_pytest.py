"""Тема «pytest».

Задания — по модулям в _pyt_m1.py … _pyt_m3.py, теория — в theory_test_pytest.py
(она собирает _pyt_t1.py … _pyt_t3.py)."""
from ._lib import topic
from ._pyt_m1 import m1
from ._pyt_m2 import m2
from ._pyt_m3 import m3

TOPIC = topic("test-pytest", "pytest", "🧪", "#0a9edc",
              "Первые тесты, assert и approx, pytest.raises, флаги запуска, фикстуры и yield, scope и conftest.py, parametrize, tmp_path/monkeypatch/capsys, маркеры, pytest-xdist, настройка, хорошие тесты",
              m1, m2, m3, group="Тестирование")
