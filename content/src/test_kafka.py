"""Тема «Kafka для тестировщика».

Задания — по модулям в _kfk_m1.py … _kfk_m3.py, теория — в theory_test_kafka.py (собирает _kfk_t1.py … _kfk_t3.py).
Kafka в песочнице — учебная, в памяти (deploy/runner/kafkafake) с API confluent-kafka; 3D-история — static/stories/kafka."""
from ._lib import topic
from ._kfk_m1 import m1
from ._kfk_m2 import m2
from ._kfk_m3 import m3

TOPIC = topic("test-kafka", "Kafka для тестировщика", "📨", "#ff8a3d",
              "Брокер сообщений Kafka: топики, партиции, группы и офсеты, гарантии доставки; продюсер и консьюмер на Python; как тестируют системы на Kafka",
              m1, m2, m3, group="Тестирование")
