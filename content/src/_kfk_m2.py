"""Тема «Kafka для тестировщика», модуль 2 «Kafka из Python» — задания. Теория — в _kfk_t2.py.

Код учеников работает с учебной Kafka (kafkafake, API confluent-kafka). Проверки запускаются подряд в одном
процессе, поэтому каждая начинает с kafkafake.reset() — чистого кластера."""
from textwrap import dedent

from ._lib import cmd, cod, lesson, module, out, t
from ._kfk_m1 import kcli

P = "kfk"

KT = """import json
import kafkafake
from kafkafake import AdminClient, Consumer, NewTopic, Producer, TopicPartition

CONF = {"bootstrap.servers": "kafka:9092"}


def fresh():
    kafkafake.reset()


def read_topic(topic):
    c = Consumer({**CONF, "group.id": "checker", "auto.offset.reset": "earliest"})
    c.subscribe([topic])
    out = []
    while (m := c.poll(0)) is not None:
        out.append(m)
    c.close()
    kafkafake.cluster.groups.pop("checker", None)
    return out


def put(topic, items):
    p = Producer(CONF)
    for key, value in items:
        p.produce(topic, key=key, value=value)
    p.flush()
"""


def kt(body):
    """Проверки задания с учебной Kafka: помощники fresh/read_topic/put + тесты."""
    return KT + "\n" + dedent(body)


m2 = module(f"{P}-m2", "Kafka из Python", "🐍", "Продюсер и консьюмер на confluent-kafka, формат сообщений, утилиты Kafka и lag",

lesson(f"{P}-producer", "Продюсер в Python",
    out(f"{P}-producer-e1", "Что выведет программа? Колбэк доставки сообщает партицию и офсет каждого сообщения.", """
        from kafkafake import Producer

        producer = Producer({"bootstrap.servers": "kafka:9092"})

        def on_delivery(err, msg):
            print(msg.key().decode(), "→ P", msg.partition(), "offset", msg.offset())

        for user in ["user-1", "user-2", "user-1"]:
            producer.produce("orders", key=user, value="{}", on_delivery=on_delivery)
        print("до flush в буфере:", len(producer))
        producer.flush()
        print("после flush:", len(producer))
        """),
    cod(f"{P}-producer-e2", t("""
        Напиши функцию `send_order(producer, order)` — отправить заказ в Kafka.

        - Получает: `producer` — продюсер; `order` — словарь с полями `order_id`, `user`, `amount`.
        - Делает: отправляет в топик `"orders"` сообщение с ключом `order["user"]` и значением — JSON заказа (`json.dumps(order, ensure_ascii=False)`), затем `flush()`.

        Проверки прочитают топик и сравнят ключ и разобранный JSON.
        """),
        """
        import json
        from kafkafake import Producer

        def send_order(producer, order):
            pass
        """,
        kt("""
        def test_sent():
            fresh()
            send_order(Producer(CONF), {"order_id": 501, "user": "Аня", "amount": 990})
            msgs = read_topic("orders")
            assert len(msgs) == 1, f"В топике orders {len(msgs)} сообщений"
            assert msgs[0].key().decode() == "Аня", "Ключ — пользователь"
            assert json.loads(msgs[0].value()) == {"order_id": 501, "user": "Аня", "amount": 990}

        def test_cyrillic_readable():
            fresh()
            send_order(Producer(CONF), {"order_id": 1, "user": "Вика", "amount": 1})
            assert "Вика".encode() in read_topic("orders")[0].value(), "ensure_ascii=False — кириллица как есть"
        """),
        """
        import json
        from kafkafake import Producer

        def send_order(producer, order):
            producer.produce("orders", key=order["user"], value=json.dumps(order, ensure_ascii=False))
            producer.flush()
        """,
        hint="`producer.produce(\"orders\", key=…, value=json.dumps(…))`, затем `producer.flush()`."),
    cod(f"{P}-producer-e3", t("""
        Напиши функцию `send_all(producer, topic, values)` — отправить список значений и вернуть их офсеты.

        - Отправляет каждое значение из `values` в `topic` (без ключа) и ждёт доставки `flush()`.
        - Возвращает: список офсетов **в порядке подтверждений**, собранных колбэком доставки. Если пришла ошибка (`err` не `None`), вместо офсета добавь `None`.
        """),
        """
        from kafkafake import Producer

        def send_all(producer, topic, values):
            pass
        """,
        kt("""
        def test_offsets():
            fresh()
            p = Producer(CONF)
            offsets = send_all(p, "logs", ["a", "b", "c", "d"])
            assert len(offsets) == 4 and all(isinstance(o, int) for o in offsets), f"Получено {offsets}"
            assert len(read_topic("logs")) == 4

        def test_error_is_none():
            fresh()
            p = Producer(CONF)
            AdminClient(CONF).create_topics([NewTopic("one", num_partitions=1)])
            # отправка в несуществующую партицию даёт ошибку доставки
            res = []
            def cb(err, msg): res.append(None if err else msg.offset())
            p.produce("one", value="x", partition=5, on_delivery=cb); p.flush()
            assert res == [None], "проверка учебной Kafka"
            assert send_all(p, "one", ["ok"]) == [0]
        """),
        """
        from kafkafake import Producer

        def send_all(producer, topic, values):
            offsets = []

            def on_delivery(err, msg):
                offsets.append(None if err is not None else msg.offset())

            for value in values:
                producer.produce(topic, value=value, on_delivery=on_delivery)
            producer.flush()
            return offsets
        """,
        hint="Колбэк добавляет `msg.offset()` или `None` в список; список возвращай после `flush()`."),
    cod(f"{P}-producer-e4", t("""
        Напиши функцию `producer_config(env)` — настройки надёжного продюсера для автотестов.

        - Получает: `env` — словарь переменных окружения.
        - Возвращает словарь настроек:
          - `"bootstrap.servers"` — из `env["KAFKA_BOOTSTRAP"]`, а если переменной нет — `"localhost:9092"`;
          - `"acks"`: `"all"`;
          - `"enable.idempotence"`: `True`;
          - `"client.id"`: `"autotests"`.
        """),
        """
        def producer_config(env):
            pass
        """,
        """
        def test_defaults():
            assert producer_config({}) == {"bootstrap.servers": "localhost:9092", "acks": "all",
                                           "enable.idempotence": True, "client.id": "autotests"}

        def test_env():
            assert producer_config({"KAFKA_BOOTSTRAP": "kafka:29092"})["bootstrap.servers"] == "kafka:29092"
        """,
        """
        def producer_config(env):
            return {
                "bootstrap.servers": env.get("KAFKA_BOOTSTRAP", "localhost:9092"),
                "acks": "all",
                "enable.idempotence": True,
                "client.id": "autotests",
            }
        """,
        hint="`env.get(\"KAFKA_BOOTSTRAP\", \"localhost:9092\")`."),
    out(f"{P}-producer-e5", "Что выведет программа? Что видит консьюмер до и после `flush()` у продюсера.", """
        from kafkafake import Consumer, Producer

        conf = {"bootstrap.servers": "kafka:9092"}
        producer = Producer(conf)
        consumer = Consumer({**conf, "group.id": "demo", "auto.offset.reset": "earliest"})
        consumer.subscribe(["events"])

        producer.produce("events", value="привет")
        print("до flush:", consumer.poll(1.0))
        producer.flush()
        msg = consumer.poll(1.0)
        print("после flush:", msg.value().decode())
        """),
    cod(f"{P}-producer-e6", t("""
        Напиши функцию `safe_send(producer, topic, value)` — отправка, которая не роняет тест при отсутствии топика.

        - Пытается отправить `value` в `topic` и вызвать `flush()`.
        - Если `produce` бросил `KafkaException` (например, топика нет, а авто-создание выключено) — вернуть `False`.
        - Если всё прошло — вернуть `True`.

        `KafkaException` импортируй из `kafkafake` (в настоящем коде — из `confluent_kafka`).
        """),
        """
        from kafkafake import KafkaException, Producer

        def safe_send(producer, topic, value):
            pass
        """,
        kt("""
        def test_ok():
            fresh()
            assert safe_send(Producer(CONF), "orders", "x") is True
            assert len(read_topic("orders")) == 1

        def test_no_topic():
            fresh()
            kafkafake.cluster.auto_create = False
            assert safe_send(Producer(CONF), "missing", "x") is False, "Нет топика — False, без исключения"
        """),
        """
        from kafkafake import KafkaException, Producer

        def safe_send(producer, topic, value):
            try:
                producer.produce(topic, value=value)
                producer.flush()
            except KafkaException:
                return False
            return True
        """,
        hint="`try: … except KafkaException: return False`."),
    cmd(f"{P}-producer-e7", "Установи Python-клиент Kafka от Confluent через pip.",
        ["pip install confluent-kafka", "re:(python3? -m )?pip3? install confluent[-_]kafka"],
        hint="Пакет называется `confluent-kafka`."),
    cmd(f"{P}-producer-e8", "Запусти консольный продюсер, чтобы вручную отправлять сообщения в топик `orders`. Брокер — `localhost:9092`.",
        ["kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders",
         kcli("kafka-console-producer", ["--bootstrap-server localhost:9092", "--topic orders"])],
        hint="`kafka-console-producer.sh --bootstrap-server … --topic …`."),
),

lesson(f"{P}-consumer", "Консьюмер в Python",
    out(f"{P}-consumer-e1", "Что выведет программа? Цикл чтения до `None`.", """
        from kafkafake import Consumer, Producer

        conf = {"bootstrap.servers": "kafka:9092"}
        p = Producer(conf)
        for i in range(3):
            p.produce("orders", key="u1", value=f"заказ {i}")
        p.flush()

        c = Consumer({**conf, "group.id": "demo", "auto.offset.reset": "earliest"})
        c.subscribe(["orders"])
        try:
            while (msg := c.poll(1.0)) is not None:
                print(msg.offset(), msg.value().decode())
        finally:
            c.close()
        print("готово")
        """),
    cod(f"{P}-consumer-e2", t("""
        Напиши функцию `read_n(consumer, n, max_polls=50)` — прочитать не больше `n` сообщений.

        - Вызывает `consumer.poll(0.5)` не больше `max_polls` раз.
        - Пропускает `None` и сообщения с ошибкой (`msg.error()` не `None`).
        - Собирает значения, декодированные в строки, и останавливается, как только набралось `n`.
        - Возвращает список значений (может быть короче `n`, если сообщения кончились).
        """),
        """
        def read_n(consumer, n, max_polls=50):
            pass
        """,
        kt("""
        def make(group="g"):
            c = Consumer({**CONF, "group.id": group, "auto.offset.reset": "earliest"})
            c.subscribe(["orders"])
            return c

        def test_exact():
            fresh(); put("orders", [("u", f"m{i}") for i in range(5)])
            assert read_n(make(), 3) == ["m0", "m1", "m2"]

        def test_short():
            fresh(); put("orders", [("u", "only")])
            assert read_n(make(), 3, max_polls=5) == ["only"], "Сообщений меньше — вернуть сколько есть"
        """),
        """
        def read_n(consumer, n, max_polls=50):
            values = []
            for _ in range(max_polls):
                msg = consumer.poll(0.5)
                if msg is None or msg.error() is not None:
                    continue
                values.append(msg.value().decode())
                if len(values) == n:
                    break
            return values
        """,
        hint="Цикл `for _ in range(max_polls)`, выход по `len(values) == n`."),
    cod(f"{P}-consumer-e3", t("""
        Напиши функцию `wait_for(consumer, predicate, attempts=20)` — главный помощник тестов: дождаться **конкретного** сообщения.

        - Вызывает `consumer.poll(0.5)` не больше `attempts` раз.
        - Возвращает первое сообщение без ошибки, для которого `predicate(msg)` истинно.
        - Если не дождались — `None`.

        Пример предиката: `lambda m: json.loads(m.value())["order_id"] == 501`.
        """),
        """
        def wait_for(consumer, predicate, attempts=20):
            pass
        """,
        kt("""
        def make():
            c = Consumer({**CONF, "group.id": "g", "auto.offset.reset": "earliest"})
            c.subscribe(["orders"])
            return c

        def test_found():
            fresh(); put("orders", [("u", json.dumps({"order_id": i})) for i in (499, 500, 501, 502)])
            msg = wait_for(make(), lambda m: json.loads(m.value())["order_id"] == 501)
            assert msg is not None and json.loads(msg.value())["order_id"] == 501

        def test_not_found():
            fresh(); put("orders", [("u", json.dumps({"order_id": 1}))])
            assert wait_for(make(), lambda m: False, attempts=3) is None
        """),
        """
        def wait_for(consumer, predicate, attempts=20):
            for _ in range(attempts):
                msg = consumer.poll(0.5)
                if msg is not None and msg.error() is None and predicate(msg):
                    return msg
            return None
        """,
        hint="Три условия сразу: сообщение есть, ошибки нет, предикат истинен."),
    cod(f"{P}-consumer-e4", t("""
        Напиши функцию `process_all(consumer, handler)` — обработка с ручным коммитом (at-least-once).

        - Читает `consumer.poll(1.0)`, пока не придёт `None`.
        - Для каждого сообщения: вызывает `handler(значение_строкой)` и **после этого** коммитит `consumer.commit(message=msg)`.
        - Если `handler` бросил исключение — **не коммитить** это сообщение и пробросить исключение дальше.
        - Возвращает число обработанных сообщений.

        Проверка создаст консьюмер с `enable.auto.commit=False`, уронит обработчик на втором сообщении и убедится, что после перезапуска оно будет прочитано снова.
        """),
        """
        def process_all(consumer, handler):
            pass
        """,
        kt("""
        def make():
            c = Consumer({**CONF, "group.id": "billing", "auto.offset.reset": "earliest", "enable.auto.commit": False})
            c.subscribe(["orders"])
            return c

        def test_all():
            fresh(); put("orders", [("u", "a"), ("u", "b")])
            seen = []
            assert process_all(make(), seen.append) == 2
            assert seen == ["a", "b"]

        def test_no_commit_on_error():
            fresh(); put("orders", [("u", "a"), ("u", "boom"), ("u", "c")])
            def handler(v):
                if v == "boom":
                    raise RuntimeError("сбой")
            c = make()
            try:
                process_all(c, handler)
                assert False, "Исключение обработчика нужно пробросить"
            except RuntimeError:
                pass
            c.close()
            again = []
            process_all(make(), again.append)
            assert again[0] == "boom", f"Упавшее сообщение должно прочитаться снова, а прочитано {again}"
        """),
        """
        def process_all(consumer, handler):
            count = 0
            while (msg := consumer.poll(1.0)) is not None:
                handler(msg.value().decode())
                consumer.commit(message=msg)
                count += 1
            return count
        """,
        hint="Сначала `handler(...)`, потом `commit` — исключение само прервёт цикл до коммита."),
    out(f"{P}-consumer-e5", "Что выведет программа? Две группы читают один топик.", """
        from kafkafake import Consumer, Producer

        conf = {"bootstrap.servers": "kafka:9092"}
        p = Producer(conf)
        for i in range(3):
            p.produce("orders", value=f"o{i}")
        p.flush()

        def count(group):
            c = Consumer({**conf, "group.id": group, "auto.offset.reset": "earliest"})
            c.subscribe(["orders"])
            n = 0
            while c.poll(1.0) is not None:
                n += 1
            c.close()
            return n

        print("billing:", count("billing"), "| analytics:", count("analytics"), "| billing снова:", count("billing"))
        """),
    cod(f"{P}-consumer-e6", t("""
        Напиши функцию `consumer_config(group, from_beginning)` — настройки консьюмера для теста.

        - Возвращает словарь:
          - `"bootstrap.servers"`: `"localhost:9092"`;
          - `"group.id"`: `group`;
          - `"auto.offset.reset"`: `"earliest"`, если `from_beginning` истинно, иначе `"latest"`;
          - `"enable.auto.commit"`: `False`.
        """),
        """
        def consumer_config(group, from_beginning):
            pass
        """,
        """
        def test_beginning():
            assert consumer_config("t1", True) == {"bootstrap.servers": "localhost:9092", "group.id": "t1",
                                                   "auto.offset.reset": "earliest", "enable.auto.commit": False}

        def test_latest():
            assert consumer_config("t2", False)["auto.offset.reset"] == "latest"
        """,
        """
        def consumer_config(group, from_beginning):
            return {
                "bootstrap.servers": "localhost:9092",
                "group.id": group,
                "auto.offset.reset": "earliest" if from_beginning else "latest",
                "enable.auto.commit": False,
            }
        """,
        hint="Условное выражение: `\"earliest\" if from_beginning else \"latest\"`."),
    out(f"{P}-consumer-e7", "Что выведет программа? Консьюмер закоммитил одно сообщение и перезапустился.", """
        from kafkafake import Consumer, Producer

        conf = {"bootstrap.servers": "kafka:9092"}
        p = Producer(conf)
        for i in range(4):
            p.produce("orders", key="u", value=f"m{i}")
        p.flush()

        def consumer():
            c = Consumer({**conf, "group.id": "billing", "auto.offset.reset": "earliest", "enable.auto.commit": False})
            c.subscribe(["orders"])
            return c

        c = consumer()
        first = c.poll(1.0)
        c.commit(message=first)
        c.poll(1.0)              # прочитали m1, но не закоммитили
        c.close()

        c = consumer()
        print([m.value().decode() for m in iter(lambda: c.poll(1.0), None)])
        """),
    cmd(f"{P}-consumer-e8", "Какой метод консьюмера обязательно вызывают в блоке `finally`, чтобы он покинул группу? Введи вызов.",
        ["consumer.close()", "re:(consumer\\.|c\\.)?close(\\(\\))?"],
        hint="Противоположность «открыть»."),
),

lesson(f"{P}-json", "Формат сообщений: JSON и заголовки",
    out(f"{P}-json-e1", "Что выведет программа? JSON в байты и обратно.", """
        import json

        event = {"order_id": 501, "user": "Аня"}
        a = json.dumps(event).encode()
        b = json.dumps(event, ensure_ascii=False).encode()
        print(len(a), len(b))
        print(json.loads(b) == event, type(b).__name__)
        """),
    cod(f"{P}-json-e2", t("""
        Напиши функцию `encode_event(event)` — превратить событие в байты для Kafka.

        - Возвращает: `json.dumps(event, ensure_ascii=False, sort_keys=True)` в кодировке UTF-8 (байты).

        `sort_keys=True` даёт одинаковые байты для одинаковых событий — так проще сравнивать в тестах.

        Пример:
        ```
        encode_event({"b": 1, "a": "я"})   # → '{"a": "я", "b": 1}' в байтах
        ```
        """),
        """
        import json

        def encode_event(event):
            pass
        """,
        """
        def test_encode():
            assert encode_event({"b": 1, "a": "я"}) == '{"a": "я", "b": 1}'.encode("utf-8")

        def test_bytes():
            assert isinstance(encode_event({}), bytes), "Нужны байты: .encode()"
        """,
        """
        import json

        def encode_event(event):
            return json.dumps(event, ensure_ascii=False, sort_keys=True).encode("utf-8")
        """,
        hint="`json.dumps(…, ensure_ascii=False, sort_keys=True).encode(\"utf-8\")`."),
    cod(f"{P}-json-e3", t("""
        Напиши функцию `decode(raw)` — разобрать значение сообщения, не падая на мусоре.

        - Получает: `raw` — байты или `None`.
        - Возвращает: словарь, если это JSON-объект; иначе — `None` (битый JSON, не объект, `None`).

        Пример:
        ```
        decode(b'{"id": 1}')     # → {"id": 1}
        decode(b"{id: 1}")       # → None
        decode(b"[1, 2]")        # → None — это список, а не объект
        ```
        """),
        """
        import json

        def decode(raw):
            pass
        """,
        """
        def test_ok():
            assert decode(b'{"id": 1}') == {"id": 1}

        def test_bad():
            assert decode(b"{id: 1}") is None
            assert decode(b"") is None
            assert decode(None) is None

        def test_not_object():
            assert decode(b"[1, 2]") is None
        """,
        """
        import json

        def decode(raw):
            try:
                data = json.loads(raw)
            except (ValueError, TypeError):
                return None
            return data if isinstance(data, dict) else None
        """,
        hint="`try: json.loads(raw) except (ValueError, TypeError)`, затем проверка `isinstance(data, dict)`."),
    cod(f"{P}-json-e4", t("""
        Напиши функцию `contract_errors(event)` — проверить событие «заказ создан» по контракту.

        Требования к событию (словарю):
        - `order_id` — целое число (`int`, но **не** `bool`);
        - `user` — непустая строка;
        - `amount` — число (`int` или `float`, не `bool`) больше нуля;
        - `status` — строка `"created"`;
        - поля `password` быть **не должно**.

        Возвращает: список строк-ошибок — по одной на нарушенное правило, в порядке правил выше: `"order_id"`, `"user"`, `"amount"`, `"status"`, `"password"`. Нет нарушений — пустой список.
        """),
        """
        def contract_errors(event):
            pass
        """,
        """
        GOOD = {"order_id": 501, "user": "anna", "amount": 990.0, "status": "created"}

        def test_good():
            assert contract_errors(GOOD) == []

        def test_types():
            assert contract_errors({**GOOD, "order_id": "501"}) == ["order_id"], "Строка вместо числа"
            assert contract_errors({**GOOD, "order_id": True}) == ["order_id"], "bool — не число заказа"
            assert contract_errors({**GOOD, "amount": 0}) == ["amount"]

        def test_missing_and_extra():
            bad = {"order_id": 1, "status": "new", "password": "123"}
            assert contract_errors(bad) == ["user", "amount", "status", "password"]
        """,
        """
        def contract_errors(event):
            errors = []
            order_id = event.get("order_id")
            if not isinstance(order_id, int) or isinstance(order_id, bool):
                errors.append("order_id")
            user = event.get("user")
            if not isinstance(user, str) or not user:
                errors.append("user")
            amount = event.get("amount")
            if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
                errors.append("amount")
            if event.get("status") != "created":
                errors.append("status")
            if "password" in event:
                errors.append("password")
            return errors
        """,
        hint="`bool` — подкласс `int`, поэтому отдельная проверка `isinstance(x, bool)`.", xp=20),
    cod(f"{P}-json-e5", t("""
        Напиши функцию `headers_dict(headers)` — заголовки сообщения в удобный словарь.

        - Получает: `headers` — список пар `(имя, байты)` или `None` (заголовков нет).
        - Возвращает: словарь `{имя: строка}` — значения декодированы из UTF-8. Для `None` — пустой словарь.

        Пример:
        ```
        headers_dict([("trace-id", b"a1"), ("event-type", b"OrderCreated")])
        # → {"trace-id": "a1", "event-type": "OrderCreated"}
        ```
        """),
        """
        def headers_dict(headers):
            pass
        """,
        """
        def test_headers():
            assert headers_dict([("trace-id", b"a1"), ("event-type", b"OrderCreated")]) == {"trace-id": "a1", "event-type": "OrderCreated"}

        def test_none():
            assert headers_dict(None) == {}
        """,
        """
        def headers_dict(headers):
            return {name: value.decode("utf-8") for name, value in headers or []}
        """,
        hint="`headers or []` — пустой список вместо `None`."),
    out(f"{P}-json-e6", "Что выведет программа? Заголовки помогают понять, откуда сообщение.", """
        from kafkafake import Consumer, Producer

        conf = {"bootstrap.servers": "kafka:9092"}
        p = Producer(conf)
        p.produce("orders", value='{"order_id": 1}', headers=[("event-type", b"OrderCreated"), ("trace-id", b"req-42")])
        p.flush()

        c = Consumer({**conf, "group.id": "demo", "auto.offset.reset": "earliest"})
        c.subscribe(["orders"])
        msg = c.poll(1.0)
        headers = dict(msg.headers())
        print(headers["event-type"].decode(), headers["trace-id"].decode())
        """),
    cod(f"{P}-json-e7", t("""
        Напиши функцию `breaking_changes(old, new)` — найти изменения схемы события, которые сломают старых консьюмеров.

        - Получает: `old` и `new` — словари `{поле: обязательное ли (True/False)}`.
        - Возвращает **отсортированный** список описаний проблем:
          - `"удалено: X"` — поле было в `old`, а в `new` его нет;
          - `"новое обязательное: X"` — поля не было в `old`, а в `new` оно обязательное.

        Новое **необязательное** поле — безопасно, его не включай.

        Пример:
        ```
        breaking_changes({"id": True, "note": False}, {"id": True, "currency": True, "tag": False})
        # → ["новое обязательное: currency", "удалено: note"]
        ```
        """),
        """
        def breaking_changes(old, new):
            pass
        """,
        """
        def test_changes():
            assert breaking_changes({"id": True, "note": False}, {"id": True, "currency": True, "tag": False}) == ["новое обязательное: currency", "удалено: note"]

        def test_safe():
            assert breaking_changes({"id": True}, {"id": True, "tag": False}) == [], "Необязательное поле — безопасно"
        """,
        """
        def breaking_changes(old, new):
            problems = [f"удалено: {f}" for f in old if f not in new]
            problems += [f"новое обязательное: {f}" for f, required in new.items() if f not in old and required]
            return sorted(problems)
        """,
        hint="Два включения: удалённые поля и новые обязательные, затем `sorted`."),
    cmd(f"{P}-json-e8", "Как называется отдельный сервис, где хранят схемы сообщений (Avro, Protobuf, JSON Schema) и проверяют их совместимость? Введи название по-английски.",
        ["Schema Registry", "re:(?i)(confluent )?schema[ -]?registry"],
        hint="Дословно — «реестр схем»."),
),

lesson(f"{P}-cli", "Утилиты Kafka и lag",
    out(f"{P}-cli-e1", "Что выведет программа? Разбираем вывод `kafka-consumer-groups --describe`.", """
        text = '''GROUP    TOPIC   PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
        billing  orders  0          120             120             0
        billing  orders  1          98              130             32
        billing  orders  2          140             141             1'''

        rows = [line.split() for line in text.splitlines()[1:]]
        lags = {int(r[2]): int(r[5]) for r in rows}
        print(lags, sum(lags.values()))
        print("отстаёт больше всего: партиция", max(lags, key=lags.get))
        """),
    cod(f"{P}-cli-e2", t("""
        Напиши функцию `parse_describe(text)` — разобрать вывод `kafka-consumer-groups --describe`.

        - Получает: `text` — вывод команды: первая строка — заголовок, дальше строки партиций. Колонки разделены пробелами; порядок колонок узнай **из заголовка** (он может меняться между версиями Kafka).
        - Возвращает: словарь `{номер партиции (int): lag (int)}`. Если в колонке `LAG` стоит `-` (группа ещё не коммитила), считай lag равным `LOG-END-OFFSET`.

        Пустые строки пропускай.
        """),
        """
        def parse_describe(text):
            pass
        """,
        """
        T1 = '''GROUP    TOPIC   PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
        billing  orders  0          120             120             0
        billing  orders  1          98              130             32
        '''

        def test_basic():
            assert parse_describe(T1) == {0: 0, 1: 32}

        def test_other_order_and_dash():
            text = "TOPIC PARTITION LAG LOG-END-OFFSET CURRENT-OFFSET GROUP\\norders 0 - 7 - billing\\norders 1 2 9 7 billing"
            assert parse_describe(text) == {0: 7, 1: 2}, "Колонки — по заголовку; «-» — lag = LOG-END-OFFSET"
        """,
        """
        def parse_describe(text):
            lines = [line.split() for line in text.splitlines() if line.strip()]
            head = lines[0]
            part, lag, end = head.index("PARTITION"), head.index("LAG"), head.index("LOG-END-OFFSET")
            result = {}
            for row in lines[1:]:
                result[int(row[part])] = int(row[end]) if row[lag] == "-" else int(row[lag])
            return result
        """,
        hint="`head.index(\"LAG\")` — номер колонки по заголовку.", xp=20),
    cod(f"{P}-cli-e3", t("""
        Напиши функцию `ensure_topic(admin, name, partitions)` — создать топик, если его ещё нет.

        - `admin` — `AdminClient`. Список топиков — `admin.list_topics().topics` (словарь по именам).
        - Если топик есть — ничего не делать и вернуть `False`.
        - Если нет — создать: `admin.create_topics([NewTopic(name, num_partitions=partitions, replication_factor=1)])`, дождаться `.result()` для этого топика и вернуть `True`.
        """),
        """
        from kafkafake import AdminClient, NewTopic

        def ensure_topic(admin, name, partitions):
            pass
        """,
        kt("""
        def test_create_and_skip():
            fresh()
            admin = AdminClient(CONF)
            assert ensure_topic(admin, "test-orders", 4) is True
            assert len(admin.list_topics().topics["test-orders"].partitions) == 4
            assert ensure_topic(admin, "test-orders", 4) is False, "Второй раз — уже есть"
        """),
        """
        from kafkafake import AdminClient, NewTopic

        def ensure_topic(admin, name, partitions):
            if name in admin.list_topics().topics:
                return False
            futures = admin.create_topics([NewTopic(name, num_partitions=partitions, replication_factor=1)])
            futures[name].result()
            return True
        """,
        hint="`create_topics` возвращает словарь «имя → future»."),
    cmd(f"{P}-cli-e4", "Покажи список всех топиков кластера. Брокер — `localhost:9092`.",
        ["kafka-topics.sh --list --bootstrap-server localhost:9092", kcli("kafka-topics", ["--list", "--bootstrap-server localhost:9092"])],
        hint="Флаг `--list`."),
    cmd(f"{P}-cli-e5", "Прочитай топик `orders` с начала так, чтобы видеть и **ключи** сообщений. Брокер — `localhost:9092`.",
        ["kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning --property print.key=true",
         kcli("kafka-console-consumer", ["--bootstrap-server localhost:9092", "--topic orders", "--from-beginning", "--property print.key=true"])],
        hint="`--property print.key=true`."),
    cmd(f"{P}-cli-e6", "Прочитай топик `orders` с начала утилитой `kcat` и выйди, когда сообщения кончатся. Брокер — `localhost:9092`.",
        ["kcat -b localhost:9092 -t orders -C -o beginning -e",
         "re:kcat (?=(?:.* )?-b localhost:9092(?: |$))(?=(?:.* )?-t orders(?: |$))(?=(?:.* )?-C(?: |$))(?=(?:.* )?-o beginning(?: |$))(?=(?:.* )?-e(?: |$)).*"],
        hint="`-C` — читать, `-o beginning` — с начала, `-e` — выйти в конце."),
    cod(f"{P}-cli-e7", t("""
        Напиши функцию `lag_by_partition(consumer, topic, partitions)` — lag группы из кода.

        - `consumer` — консьюмер нужной группы (уже создан).
        - Для каждой партиции `p` от `0` до `partitions - 1`:
          - конец журнала: `low, high = consumer.get_watermark_offsets(TopicPartition(topic, p))` — нужен `high`;
          - закоммиченный офсет: `consumer.committed([TopicPartition(topic, p)])[0].offset`; если он отрицательный (коммита не было) — считай `0`.
        - Возвращает: словарь `{партиция: high − закоммиченный}`.
        """),
        """
        from kafkafake import TopicPartition

        def lag_by_partition(consumer, topic, partitions):
            pass
        """,
        kt("""
        def test_lag():
            fresh()
            AdminClient(CONF).create_topics([NewTopic("events", num_partitions=2)])
            p = Producer(CONF)
            for i in range(5):
                p.produce("events", value=str(i), partition=i % 2)
            p.flush()
            c = Consumer({**CONF, "group.id": "g", "auto.offset.reset": "earliest", "enable.auto.commit": False})
            c.subscribe(["events"])
            m = c.poll(0); c.commit(message=m)
            res = lag_by_partition(c, "events", 2)
            total = sum(res.values())
            assert total == 4 and set(res) == {0, 1}, f"Получено {res}"

        def test_no_commit():
            fresh()
            AdminClient(CONF).create_topics([NewTopic("e2", num_partitions=1)])
            put("e2", [(None, "a"), (None, "b")])
            c = Consumer({**CONF, "group.id": "new", "auto.offset.reset": "earliest"})
            assert lag_by_partition(c, "e2", 1) == {0: 2}, "Нет коммита — считать с нуля"
        """),
        """
        from kafkafake import TopicPartition

        def lag_by_partition(consumer, topic, partitions):
            result = {}
            for p in range(partitions):
                low, high = consumer.get_watermark_offsets(TopicPartition(topic, p))
                committed = consumer.committed([TopicPartition(topic, p)])[0].offset
                result[p] = high - max(committed, 0)
            return result
        """,
        hint="`max(committed, 0)` превращает «нет коммита» (отрицательное число) в ноль.", xp=20),
    out(f"{P}-cli-e8", "Что выведет программа? AdminClient создаёт топик и видит его в списке.", """
        from kafkafake import AdminClient, KafkaException, NewTopic

        admin = AdminClient({"bootstrap.servers": "kafka:9092"})
        admin.create_topics([NewTopic("test-orders", num_partitions=3, replication_factor=1)])["test-orders"].result()
        print(sorted(admin.list_topics().topics))
        try:
            admin.create_topics([NewTopic("test-orders", num_partitions=3)])["test-orders"].result()
        except KafkaException as e:
            print("ошибка:", e.args[0].str())
        """),
),
)
