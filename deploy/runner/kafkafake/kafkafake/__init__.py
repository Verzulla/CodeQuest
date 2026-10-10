"""kafkafake — учебная Kafka в памяти с API confluent-kafka (для песочницы CodeQuest).

В настоящем проекте: from confluent_kafka import Producer, Consumer
В песочнице:        from kafkafake import Producer, Consumer — остальной код тот же."""
from .core import (AdminClient, Consumer, KafkaError, KafkaException, Message, NewTopic, Producer,
                   TopicPartition, cluster, reset)

__all__ = ["AdminClient", "Consumer", "KafkaError", "KafkaException", "Message", "NewTopic", "Producer",
           "TopicPartition", "cluster", "reset"]
