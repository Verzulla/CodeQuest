"""Тема «Тестирование API» (заменила старую, слаги api-* сохранены ради прогресса).

Задания — по модулям в _api_m1.py … _api_m3.py, теория — в theory_test_api.py
(она собирает _api_t1.py … _api_t3.py)."""
from ._lib import topic
from ._api_m1 import m1
from ._api_m2 import m2
from ._api_m3 import m3

TOPIC = topic("test-api", "Тестирование API", "🌐", "#1cb0f6",
              "HTTP: методы, статусы, заголовки, REST и JSON; requests и подмена ответов responses; автотесты API на pytest; свой клиент; моки; Pydantic; JSON Schema; контрактные и CRUD-тесты",
              m1, m2, m3, group="Тестирование")
