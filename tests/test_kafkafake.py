"""Учебная Kafka (deploy/runner/kafkafake), на которой построены задания темы «Kafka для тестировщика»."""
import json

import pytest

kafkafake = pytest.importorskip("kafkafake")
from kafkafake import AdminClient, Consumer, KafkaException, NewTopic, Producer, TopicPartition  # noqa: E402
from kafkafake.demo import BillingWorker, OrderService  # noqa: E402

CONF = {"bootstrap.servers": "kafka:9092"}


def consumer(group, reset="earliest", **extra):
    return Consumer({**CONF, "group.id": group, "auto.offset.reset": reset, **extra})


def drain(c):
    out = []
    while (m := c.poll(0)) is not None:
        out.append(m)
    return out


def test_produce_and_consume():
    p = Producer(CONF)
    delivered = []
    p.produce("orders", key="u1", value='{"id": 1}', on_delivery=lambda err, msg: delivered.append((err, msg.offset())))
    assert len(p) == 1 and delivered == []          # до flush — в буфере
    p.flush()
    assert delivered == [(None, 0)]
    c = consumer("g"); c.subscribe(["orders"])
    msgs = drain(c)
    assert [(m.key(), m.value()) for m in msgs] == [(b"u1", b'{"id": 1}')]


def test_same_key_same_partition_and_order():
    p = Producer(CONF)
    for i in range(10):
        p.produce("orders", key=f"user-{i % 3}", value=str(i))
    p.flush()
    c = consumer("g"); c.subscribe(["orders"])
    msgs = drain(c)
    by_key = {}
    for m in msgs:
        by_key.setdefault(m.key(), set()).add(m.partition())
    assert all(len(ps) == 1 for ps in by_key.values()), "один ключ — одна партиция"
    for key in by_key:
        values = [int(m.value()) for m in msgs if m.key() == key]
        assert values == sorted(values), "порядок внутри ключа сохраняется"


def test_latest_skips_old_messages():
    p = Producer(CONF)
    p.produce("t", value="old"); p.flush()
    c = consumer("late", reset="latest"); c.subscribe(["t"])
    assert c.poll(0) is None
    p.produce("t", value="new"); p.flush()
    msgs = drain(c)
    assert [m.value() for m in msgs] == [b"new"]


def test_group_rebalance_and_idle_consumer():
    cs = [consumer("billing") for _ in range(4)]
    for c in cs:
        c.subscribe(["orders"])
    sizes = sorted(len(c.assignment()) for c in cs)
    assert sizes == [0, 1, 1, 1], "3 партиции на 4 консьюмеров — один простаивает"
    cs[0].close()
    assert sorted(len(c.assignment()) for c in cs[1:]) == [1, 1, 1]


def test_commit_and_restart():
    p = Producer(CONF)
    for i in range(5):
        p.produce("orders", key="u", value=str(i))
    p.flush()
    c = consumer("g", **{"enable.auto.commit": False}); c.subscribe(["orders"])
    first = c.poll(0); c.commit(message=first)
    c.poll(0)                        # прочитали, но не закоммитили
    c.close()
    c2 = consumer("g", **{"enable.auto.commit": False}); c2.subscribe(["orders"])
    assert [m.value() for m in drain(c2)] == [b"1", b"2", b"3", b"4"], "после перезапуска — с закоммиченного офсета"


def test_groups_are_independent():
    p = Producer(CONF)
    p.produce("orders", value="x"); p.flush()
    a = consumer("a"); a.subscribe(["orders"])
    b = consumer("b"); b.subscribe(["orders"])
    assert len(drain(a)) == 1 and len(drain(b)) == 1


def test_admin_and_lag():
    admin = AdminClient(CONF)
    admin.create_topics([NewTopic("events", num_partitions=2)])["events"].result()
    with pytest.raises(KafkaException):
        admin.create_topics([NewTopic("events", num_partitions=2)])["events"].result()
    assert len(admin.list_topics().topics["events"].partitions) == 2
    p = Producer(CONF)
    for i in range(4):
        p.produce("events", value=str(i), partition=i % 2)
    p.flush()
    c = consumer("g", **{"enable.auto.commit": False}); c.subscribe(["events"])
    m = c.poll(0); c.commit(message=m)
    assert sum(admin.lag("g", "events").values()) == 3
    low, high = c.get_watermark_offsets(TopicPartition("events", 0))
    assert (low, high) == (0, 2)


def test_config_errors():
    with pytest.raises(KafkaException):
        Producer({})
    with pytest.raises(KafkaException):
        Consumer(CONF)


def test_demo_services_and_bugs():
    OrderService().place(1, "anna", 500)
    OrderService().place(2, "anna", 0)          # amount 0 — невалидно → DLQ
    w = BillingWorker()
    assert w.run_once() == 1
    pay = consumer("check"); pay.subscribe(["payments"])
    assert [json.loads(m.value())["order_id"] for m in drain(pay)] == [1]
    dlq = consumer("check"); dlq.subscribe(["orders.dlq"])
    bad = drain(dlq)
    assert len(bad) == 1 and dict(bad[0].headers())["error"]

    kafkafake.reset()
    OrderService(bug="dup").place(7, "bob", 100)
    c = consumer("x"); c.subscribe(["orders"])
    assert len(drain(c)) == 2

    kafkafake.reset()
    OrderService().place(9, "eve", 5000)
    w = BillingWorker(bug="commit_first")
    with pytest.raises(RuntimeError):
        w.run_once()
    w.close()
    assert BillingWorker().run_once() == 0, "коммит до обработки — заказ потерян"
