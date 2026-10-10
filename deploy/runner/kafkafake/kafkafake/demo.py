"""Демо-сервисы для заданий «напиши тест».

OrderService публикует заказы в топик orders, BillingWorker их обрабатывает и пишет платежи в payments,
а битые сообщения отправляет в orders.dlq. Параметр bug включает типичную ошибку — так проверяется,
что тест ученика её ловит.

Баги OrderService:  "no_key" — без ключа (ломается порядок по пользователю), "dup" — каждое событие дважды,
                    "lost" — теряется каждый третий заказ, "bad_json" — значение не JSON,
                    "status" — статус "new" вместо "created", "amount_str" — сумма строкой.
Баги BillingWorker: "dup" — платёж дважды, "no_dlq" — на битом сообщении падает, вместо отправки в DLQ,
                    "commit_first" — коммитит до обработки (сбой на сумме > 1000 теряет заказ),
                    "no_commit" — не коммитит (после перезапуска обработает всё заново).
"""
import json

from .core import Consumer, Producer

BOOTSTRAP = "kafka:9092"


class OrderService:
    """Сервис заказов: place() публикует событие «заказ создан» в топик orders, ключ — пользователь."""

    def __init__(self, bug=None, topic="orders"):
        self.bug, self.topic = bug, topic
        self.producer = Producer({"bootstrap.servers": BOOTSTRAP})

    def place(self, order_id, user, amount):
        event = {"order_id": order_id, "user": user, "amount": amount, "status": "created"}
        if self.bug == "lost" and order_id % 3 == 0:
            return event
        if self.bug == "status":
            event["status"] = "new"
        if self.bug == "amount_str":
            event["amount"] = str(amount)
        value = repr(event) if self.bug == "bad_json" else json.dumps(event)
        key = None if self.bug == "no_key" else user
        for _ in range(2 if self.bug == "dup" else 1):
            self.producer.produce(self.topic, key=key, value=value)
        self.producer.flush()
        return event


class BillingWorker:
    """Биллинг: читает orders, на каждый заказ пишет платёж в payments; битые сообщения — в orders.dlq."""

    def __init__(self, bug=None, group="billing"):
        self.bug = bug
        self.consumer = Consumer({"bootstrap.servers": BOOTSTRAP, "group.id": group,
                                  "auto.offset.reset": "earliest", "enable.auto.commit": False})
        self.consumer.subscribe(["orders"])
        self.producer = Producer({"bootstrap.servers": BOOTSTRAP})

    def _check(self, raw):
        data = json.loads(raw)
        if not isinstance(data.get("order_id"), int):
            raise ValueError("order_id должен быть числом")
        if not isinstance(data.get("amount"), (int, float)) or data["amount"] <= 0:
            raise ValueError("amount должен быть положительным числом")
        return data

    def run_once(self):
        """Обработать всё, что накопилось. Возвращает число обработанных сообщений."""
        n = 0
        while (msg := self.consumer.poll(1.0)) is not None:
            if self.bug == "commit_first":
                self.consumer.commit(message=msg)
            try:
                data = self._check(msg.value())
            except ValueError as e:
                if self.bug == "no_dlq":
                    raise
                self.producer.produce("orders.dlq", key=msg.key(), value=msg.value(), headers=[("error", str(e).encode())])
                self.producer.flush()
                self.consumer.commit(message=msg)
                continue
            if self.bug == "commit_first" and data["amount"] > 1000:
                raise RuntimeError("сбой платёжного шлюза")
            payment = json.dumps({"order_id": data["order_id"], "amount": data["amount"], "status": "paid"})
            for _ in range(2 if self.bug == "dup" else 1):
                self.producer.produce("payments", key=msg.key(), value=payment)
            self.producer.flush()
            if self.bug != "no_commit":
                self.consumer.commit(message=msg)
            n += 1
        return n

    def close(self):
        self.consumer.close()
