"""Тема «Kafka для тестировщика», модуль 3 «Тестирование Kafka» — задания. Теория — в _kfk_t3.py.

Задания «напиши тест» (kft): тесты ученика запускаются настоящим pytest на демо-сервисах kafkafake.demo —
сначала исправных (тесты должны пройти), потом с багом (хотя бы один тест должен упасть)."""
from textwrap import dedent

from ._lib import PYTEST_RUNNER, cmd, cod, d, lesson, module, out, t
from ._kfk_m1 import kcli
from ._kfk_m2 import kt

P = "kfk"

HEAD = '''import json
import uuid

import pytest
from kafkafake import Consumer, Producer
from kafkafake.demo import BillingWorker, OrderService

CONF = {"bootstrap.servers": "kafka:9092"}


def read_all(topic):
    """Все сообщения топика с начала: своя группа на каждый вызов, earliest, чтение до None."""
    c = Consumer({**CONF, "group.id": f"test-{uuid.uuid4().hex[:8]}", "auto.offset.reset": "earliest"})
    c.subscribe([topic])
    msgs = []
    while (m := c.poll(1.0)) is not None:
        msgs.append(m)
    c.close()
    return msgs


'''
MAIN = '''

if __name__ == "__main__":
    pytest.main(["-q", "-p", "no:cacheprovider", "solution.py"])
'''
CHECKS = '''import kafkafake
from kafkafake.demo import BillingWorker as _BW, OrderService as _OS


def bug(name, target="OrderService"):
    """Сервис с багом вместо исправного: тест ученика должен упасть."""
    cls = {"OrderService": _OS, "BillingWorker": _BW}[target]
    return {target: lambda *a, **k: cls(*a, **{**k, "bug": name})}


def source():
    return open("solution.py", encoding="utf-8").read()


def passes():
    code, res = run_pytest()
    assert res, "Не найдено ни одного теста test_*"
    assert all(v == "passed" for v in res.values()), f"На исправных сервисах тесты должны проходить: {res}"


def catches(name, target="OrderService", why=""):
    code, res = run_pytest(patch=bug(name, target))
    assert any(v == "failed" for v in res.values()), f"Тест не поймал баг: {why}"
'''


def kft(slug, prompt, starter, tests, solution, hint="", xp=25):
    """Задание «напиши тест для системы на Kafka»."""
    return cod(slug, prompt, HEAD + d(starter).rstrip("\n") + MAIN, PYTEST_RUNNER + CHECKS + d(tests),
               HEAD + d(solution).rstrip("\n") + MAIN, hint=hint, xp=xp)


m3 = module(f"{P}-m3", "Тестирование Kafka", "🧪", "Тесты доставки событий, дубли и порядок, битые сообщения и DLQ, Kafka в Docker, Testcontainers и CI",

lesson(f"{P}-test-delivery", "Тест: событие дошло",
    kft(f"{P}-test-delivery-e1", t("""
        Напиши тест `test_order_event`:
        1. `OrderService().place(501, "anna", 990)`;
        2. прочитай топик `orders` помощником `read_all("orders")` (он уже есть в файле);
        3. проверь, что сообщение **одно**, а его JSON-значение равно `{"order_id": 501, "user": "anna", "amount": 990, "status": "created"}`.

        Проверка запустит тест на исправном сервисе, а потом на сервисах, где статус `"new"`, сумма строкой `"990"` или значение — не JSON.
        """),
        """
        def test_order_event():
            OrderService().place(501, "anna", 990)
        """,
        """
        def test_good():
            passes()

        def test_catches_status():
            catches("status", why="статус «new» вместо «created»")

        def test_catches_amount_type():
            catches("amount_str", why="сумма строкой")

        def test_catches_bad_json():
            catches("bad_json", why="значение — не JSON")
        """,
        """
        def test_order_event():
            OrderService().place(501, "anna", 990)
            msgs = read_all("orders")
            assert len(msgs) == 1
            assert json.loads(msgs[0].value()) == {"order_id": 501, "user": "anna", "amount": 990, "status": "created"}
        """,
        hint="`json.loads(msgs[0].value())` и сравнение со словарём целиком ловит и статус, и тип суммы."),
    kft(f"{P}-test-delivery-e2", t("""
        Ключ сообщения определяет партицию, а значит — порядок событий пользователя.

        Напиши тест `test_key_is_user`: сделай заказ `OrderService().place(7, "bob", 100)` и проверь, что ключ единственного сообщения в `orders` — `b"bob"` (ключи — байты).

        Проверка запустит его на сервисе, который забывает указать ключ.
        """),
        """
        def test_key_is_user():
            pass
        """,
        """
        def test_good():
            passes()

        def test_catches_no_key():
            catches("no_key", why="сообщение без ключа")
        """,
        """
        def test_key_is_user():
            OrderService().place(7, "bob", 100)
            msgs = read_all("orders")
            assert len(msgs) == 1
            assert msgs[0].key() == b"bob"
        """,
        hint="`msgs[0].key() == b\"bob\"`."),
    cod(f"{P}-test-delivery-e3", t("""
        Напиши функцию `wait_for_order(consumer, order_id, attempts=20)` — дождаться события конкретного заказа.

        - Вызывает `consumer.poll(0.5)` не больше `attempts` раз.
        - Пропускает `None`, сообщения с ошибкой и сообщения, значение которых — не JSON (`json.loads` бросил `ValueError`).
        - Возвращает разобранный словарь первого события, у которого `order_id == order_id`; не дождались — `None`.
        """),
        """
        import json

        def wait_for_order(consumer, order_id, attempts=20):
            pass
        """,
        kt("""
        def make():
            c = Consumer({**CONF, "group.id": "t", "auto.offset.reset": "earliest"})
            c.subscribe(["orders"])
            return c

        def test_found_among_others():
            fresh()
            put("orders", [("a", json.dumps({"order_id": 1})), ("a", "мусор"), ("b", json.dumps({"order_id": 2, "user": "b"}))])
            assert wait_for_order(make(), 2) == {"order_id": 2, "user": "b"}

        def test_missing():
            fresh(); put("orders", [("a", json.dumps({"order_id": 1}))])
            assert wait_for_order(make(), 99, attempts=3) is None
        """),
        """
        import json

        def wait_for_order(consumer, order_id, attempts=20):
            for _ in range(attempts):
                msg = consumer.poll(0.5)
                if msg is None or msg.error() is not None:
                    continue
                try:
                    data = json.loads(msg.value())
                except ValueError:
                    continue
                if data.get("order_id") == order_id:
                    return data
            return None
        """,
        hint="Мусор пропускаем через `try/except ValueError: continue`."),
    kft(f"{P}-test-delivery-e4", t("""
        Вынеси консьюмер в фикстуру.

        - Фикстура `orders_consumer`: создаёт `Consumer` с уникальной группой (`f"test-{uuid.uuid4().hex[:8]}"`) и `"auto.offset.reset": "earliest"`, подписывает на `["orders"]`, отдаёт его через `yield`, а после теста — `close()`.
        - Тест `test_event_via_fixture(orders_consumer)`: делает заказ `OrderService().place(3, "eve", 50)`, читает `orders_consumer.poll(1.0)` и проверяет, что `order_id` в событии — `3`.

        Проверка убедится, что после тестов консьюмер закрыт (покинул группу).
        """),
        """
        @pytest.fixture
        def orders_consumer():
            pass


        def test_event_via_fixture(orders_consumer):
            pass
        """,
        """
        def test_good():
            passes()
            assert "yield" in source(), "Фикстура должна отдавать консьюмер через yield"

        def test_closed_after():
            run_pytest()
            alive = [g for g, info in kafkafake.cluster.groups.items() if info["members"]]
            assert not alive, f"После теста консьюмер не закрыт — группы с участниками: {alive}"
        """,
        """
        @pytest.fixture
        def orders_consumer():
            c = Consumer({**CONF, "group.id": f"test-{uuid.uuid4().hex[:8]}", "auto.offset.reset": "earliest"})
            c.subscribe(["orders"])
            yield c
            c.close()


        def test_event_via_fixture(orders_consumer):
            OrderService().place(3, "eve", 50)
            msg = orders_consumer.poll(1.0)
            assert msg is not None
            assert json.loads(msg.value())["order_id"] == 3
        """,
        hint="После `yield c` — `c.close()`: это уборка, она выполнится и при падении теста."),
    kft(f"{P}-test-delivery-e5", t("""
        Иногда сервис теряет события. Напиши тест `test_no_lost_orders`:

        - сделай заказы с номерами от 1 до 6 включительно (пользователь `"anna"`, сумма `100`);
        - прочитай `orders` и проверь, что **отсортированный** список `order_id` из событий — ровно `[1, 2, 3, 4, 5, 6]`.

        Проверка запустит тест на сервисе, который теряет каждый третий заказ.
        """),
        """
        def test_no_lost_orders():
            pass
        """,
        """
        def test_good():
            passes()

        def test_catches_lost():
            catches("lost", why="потерянные заказы")
        """,
        """
        def test_no_lost_orders():
            for i in range(1, 7):
                OrderService().place(i, "anna", 100)
            ids = sorted(json.loads(m.value())["order_id"] for m in read_all("orders"))
            assert ids == [1, 2, 3, 4, 5, 6]
        """,
        hint="Собери `order_id` из всех событий в список и сравни отсортированный."),
    out(f"{P}-test-delivery-e6", "Что выведет программа? Два «теста» читают топик одной и той же группой.", """
        from kafkafake import Consumer, Producer

        conf = {"bootstrap.servers": "kafka:9092"}

        def read(group):
            c = Consumer({**conf, "group.id": group, "auto.offset.reset": "earliest"})
            c.subscribe(["orders"])
            n = 0
            while c.poll(1.0) is not None:
                n += 1
            c.close()
            return n

        p = Producer(conf)
        p.produce("orders", value="заказ 1"); p.flush()
        print("тест 1:", read("autotests"))
        p.produce("orders", value="заказ 2"); p.flush()
        print("тест 2:", read("autotests"))
        print("тест 2 со своей группой:", read("autotests-2"))
        """),
    cod(f"{P}-test-delivery-e7", t("""
        Напиши функцию `unique_group(prefix)` — уникальное имя группы консьюмеров для теста.

        - Возвращает строку `f"{prefix}-{восемь шестнадцатеричных символов}"`, например `"test-1a2b3c4d"`. Возьми их из `uuid.uuid4().hex[:8]`.
        - Каждый вызов — новое имя.
        """),
        """
        import uuid

        def unique_group(prefix):
            pass
        """,
        """
        import re

        def test_format():
            assert re.fullmatch(r"test-[0-9a-f]{8}", unique_group("test")), unique_group("test")

        def test_unique():
            names = {unique_group("g") for _ in range(50)}
            assert len(names) == 50, "Каждый вызов — новое имя"
        """,
        """
        import uuid

        def unique_group(prefix):
            return f"{prefix}-{uuid.uuid4().hex[:8]}"
        """,
        hint="`uuid.uuid4().hex` — 32 случайных шестнадцатеричных символа."),
    cmd(f"{P}-test-delivery-e8", "Какое значение `auto.offset.reset` ставят консьюмеру в тесте, чтобы прочитать сообщение, отправленное **до** его создания?",
        ["earliest", "re:(?i)(auto\\.offset\\.reset\\s*[=:]\\s*)?[\"']?earliest[\"']?"],
        hint="«Самое раннее»."),
),

lesson(f"{P}-test-order", "Тест: дубли и порядок",
    kft(f"{P}-test-order-e1", t("""
        Напиши тест `test_no_duplicate_events`: сделай три заказа (номера 1, 2, 3; пользователь `"anna"`; сумма `100`) и проверь, что в `orders` нет повторов — каждый `order_id` встречается один раз, и событий ровно три.

        Проверка запустит тест на сервисе, который отправляет каждое событие дважды.
        """),
        """
        def test_no_duplicate_events():
            pass
        """,
        """
        def test_good():
            passes()

        def test_catches_dup():
            catches("dup", why="каждое событие дважды")
        """,
        """
        def test_no_duplicate_events():
            for i in (1, 2, 3):
                OrderService().place(i, "anna", 100)
            ids = [json.loads(m.value())["order_id"] for m in read_all("orders")]
            assert len(ids) == 3
            assert len(ids) == len(set(ids))
        """,
        hint="`len(ids) == len(set(ids))` — нет повторов."),
    kft(f"{P}-test-order-e2", t("""
        Самый опасный дубль — повторный **платёж**. Напиши тест `test_single_payment`:

        - заказ `OrderService().place(10, "anna", 500)`;
        - обработка `BillingWorker().run_once()`;
        - в топике `payments` должно быть **ровно одно** событие, и у него `order_id == 10`.

        Проверка запустит тест на биллинге, который пишет платёж дважды.
        """),
        """
        def test_single_payment():
            pass
        """,
        """
        def test_good():
            passes()

        def test_catches_double_payment():
            catches("dup", "BillingWorker", why="двойной платёж")
        """,
        """
        def test_single_payment():
            OrderService().place(10, "anna", 500)
            BillingWorker().run_once()
            payments = read_all("payments")
            assert len(payments) == 1
            assert json.loads(payments[0].value())["order_id"] == 10
        """,
        hint="Действие → обработка → чтение `payments`."),
    kft(f"{P}-test-order-e3", t("""
        Порядок событий пользователя гарантирован, только если они все в одной партиции.

        Напиши тест `test_user_events_in_one_partition`: четыре заказа пользователя `"anna"` (номера 1–4), затем проверь, что у всех его событий в `orders` одна и та же партиция (`msg.partition()`).

        Проверка запустит тест на сервисе, который не указывает ключ, — тогда события разъезжаются по партициям.
        """),
        """
        def test_user_events_in_one_partition():
            pass
        """,
        """
        def test_good():
            passes()

        def test_catches_no_key():
            catches("no_key", why="события пользователя в разных партициях")
        """,
        """
        def test_user_events_in_one_partition():
            for i in range(1, 5):
                OrderService().place(i, "anna", 100)
            msgs = read_all("orders")
            assert len(msgs) == 4
            assert len({m.partition() for m in msgs}) == 1
        """,
        hint="Множество партиций должно состоять из одного элемента."),
    cod(f"{P}-test-order-e4", t("""
        Напиши функцию `find_duplicates(ids)` — найти повторы в списке id событий.

        - Возвращает **отсортированный** список id, которые встречаются больше одного раза (каждый — один раз).

        Пример:
        ```
        find_duplicates([3, 1, 3, 2, 1, 3])   # → [1, 3]
        find_duplicates([1, 2])               # → []
        ```
        """),
        """
        def find_duplicates(ids):
            pass
        """,
        """
        def test_dups():
            assert find_duplicates([3, 1, 3, 2, 1, 3]) == [1, 3]

        def test_none():
            assert find_duplicates([1, 2]) == []
            assert find_duplicates([]) == []
        """,
        """
        from collections import Counter

        def find_duplicates(ids):
            return sorted(i for i, n in Counter(ids).items() if n > 1)
        """,
        hint="`Counter(ids)` посчитает, сколько раз встречается каждый id."),
    cod(f"{P}-test-order-e5", t("""
        Напиши функцию `first_per_order(payments)` — оставить по одному платежу на заказ (защита от дублей при at-least-once).

        - Получает: список словарей-платежей с полем `order_id`, в порядке поступления.
        - Возвращает: новый список — для каждого `order_id` только **первый** платёж, порядок сохранён.

        Пример:
        ```
        first_per_order([{"order_id": 1, "n": "a"}, {"order_id": 2}, {"order_id": 1, "n": "b"}])
        # → [{"order_id": 1, "n": "a"}, {"order_id": 2}]
        ```
        """),
        """
        def first_per_order(payments):
            pass
        """,
        """
        def test_first():
            src = [{"order_id": 1, "n": "a"}, {"order_id": 2}, {"order_id": 1, "n": "b"}]
            assert first_per_order(src) == [{"order_id": 1, "n": "a"}, {"order_id": 2}]
            assert len(src) == 3, "Исходный список не трогаем"
        """,
        """
        def first_per_order(payments):
            seen, result = set(), []
            for p in payments:
                if p["order_id"] not in seen:
                    seen.add(p["order_id"])
                    result.append(p)
            return result
        """,
        hint="Множество `seen` с уже встреченными order_id."),
    out(f"{P}-test-order-e6", "Что выведет программа? Биллинг без коммитов перезапустили — сколько будет платежей?", """
        from kafkafake import Consumer
        from kafkafake.demo import BillingWorker, OrderService

        OrderService().place(1, "anna", 100)
        OrderService().place(2, "bob", 200)

        for bug in (None, "no_commit"):
            w = BillingWorker(bug=bug, group=f"billing-{bug}")
            w.run_once(); w.close()
            BillingWorker(bug=bug, group=f"billing-{bug}").run_once()     # «перезапуск»

        c = Consumer({"bootstrap.servers": "kafka:9092", "group.id": "check", "auto.offset.reset": "earliest"})
        c.subscribe(["payments"])
        n = 0
        while c.poll(1.0) is not None:
            n += 1
        print("платежей:", n, "| заказов: 2 | ожидалось по одному на группу: 4")
        """),
    kft(f"{P}-test-order-e7", t("""
        Проверь, что биллинг не платит повторно после перезапуска. Напиши тест `test_restart_no_double_payment`:

        1. заказ `OrderService().place(5, "eve", 300)`;
        2. первый экземпляр: `worker = BillingWorker()`, `worker.run_once()`, `worker.close()`;
        3. «перезапуск»: `BillingWorker().run_once()`;
        4. в `payments` — ровно одно событие.

        Проверка запустит тест на биллинге, который забывает коммитить офсеты.
        """),
        """
        def test_restart_no_double_payment():
            pass
        """,
        """
        def test_good():
            passes()

        def test_catches_no_commit():
            catches("no_commit", "BillingWorker", why="нет коммита — после перезапуска двойной платёж")
        """,
        """
        def test_restart_no_double_payment():
            OrderService().place(5, "eve", 300)
            worker = BillingWorker()
            worker.run_once()
            worker.close()
            BillingWorker().run_once()
            assert len(read_all("payments")) == 1
        """,
        hint="Новый экземпляр той же группы начнёт с закоммиченного офсета."),
    cmd(f"{P}-test-order-e8", "Как называется гарантия доставки «ровно один раз» (идемпотентный продюсер + транзакции)? Введи термин по-английски.",
        ["exactly-once", "re:(?i)exactly[- ]once"],
        hint="«Точно один раз»."),
),

lesson(f"{P}-test-errors", "Тест: битые сообщения и DLQ",
    kft(f"{P}-test-errors-e1", t("""
        Напиши тест `test_bad_message_to_dlq`:

        1. положи в `orders` битое сообщение напрямую: `p = Producer(CONF)`, `p.produce("orders", key="anna", value="не json")`, `p.flush()`;
        2. запусти `BillingWorker().run_once()` — он **не должен упасть**;
        3. в `orders.dlq` — одно сообщение, а в его заголовках есть `"error"`: `dict(msg.headers())`.

        Проверка запустит тест на биллинге, который падает на битом сообщении вместо отправки в DLQ.
        """),
        """
        def test_bad_message_to_dlq():
            pass
        """,
        """
        def test_good():
            passes()

        def test_catches_no_dlq():
            catches("no_dlq", "BillingWorker", why="консьюмер падает на битом сообщении")
        """,
        """
        def test_bad_message_to_dlq():
            p = Producer(CONF)
            p.produce("orders", key="anna", value="не json")
            p.flush()
            BillingWorker().run_once()
            dlq = read_all("orders.dlq")
            assert len(dlq) == 1
            assert "error" in dict(dlq[0].headers())
        """,
        hint="Если run_once упадёт исключением — тест упадёт сам, отдельная проверка не нужна."),
    kft(f"{P}-test-errors-e2", t("""
        Проверь, что заказ не теряется, если обработка упала посередине. Напиши тест `test_no_loss_after_crash`:

        1. заказы: `OrderService().place(1, "anna", 5000)` и `OrderService().place(2, "bob", 10)`;
        2. первый экземпляр биллинга: `worker = BillingWorker()`, затем `worker.run_once()` внутри `try/except RuntimeError: pass` (так имитируется сбой), затем `worker.close()`;
        3. «перезапуск»: `BillingWorker().run_once()`;
        4. в `payments` есть платёж по заказу `1`.

        На исправном биллинге сбоя не будет, а на биллинге, который коммитит **до** обработки и падает на большой сумме, заказ 1 потеряется.
        """),
        """
        def test_no_loss_after_crash():
            pass
        """,
        """
        def test_good():
            passes()

        def test_catches_commit_first():
            catches("commit_first", "BillingWorker", why="коммит до обработки теряет заказ при сбое")
        """,
        """
        def test_no_loss_after_crash():
            OrderService().place(1, "anna", 5000)
            OrderService().place(2, "bob", 10)
            worker = BillingWorker()
            try:
                worker.run_once()
            except RuntimeError:
                pass
            worker.close()
            BillingWorker().run_once()
            paid = {json.loads(m.value())["order_id"] for m in read_all("payments")}
            assert 1 in paid
        """,
        hint="Собери `order_id` платежей во множество и проверь `1 in paid`."),
    cod(f"{P}-test-errors-e3", t("""
        Напиши функцию `route(raw)` — куда отправить сообщение: в обработку или в DLQ.

        - Получает: `raw` — значение сообщения (байты).
        - Возвращает кортеж:
          - `("dlq", "не JSON")` — если `json.loads` не смог разобрать;
          - `("dlq", "нет order_id")` — если нет поля `order_id`;
          - `("dlq", "amount <= 0")` — если `amount` отсутствует или не больше нуля;
          - иначе `("ok", разобранный_словарь)`.
        """),
        """
        import json

        def route(raw):
            pass
        """,
        """
        def test_ok():
            assert route(b'{"order_id": 1, "amount": 5}') == ("ok", {"order_id": 1, "amount": 5})

        def test_dlq():
            assert route(b"{oops") == ("dlq", "не JSON")
            assert route(b'{"amount": 5}') == ("dlq", "нет order_id")
            assert route(b'{"order_id": 1, "amount": 0}') == ("dlq", "amount <= 0")
            assert route(b'{"order_id": 1}') == ("dlq", "amount <= 0")
        """,
        """
        import json

        def route(raw):
            try:
                data = json.loads(raw)
            except ValueError:
                return "dlq", "не JSON"
            if "order_id" not in data:
                return "dlq", "нет order_id"
            if not data.get("amount", 0) > 0:
                return "dlq", "amount <= 0"
            return "ok", data
        """,
        hint="Проверки по порядку: JSON → order_id → amount."),
    cod(f"{P}-test-errors-e4", t("""
        Напиши функцию `with_retries(func, attempts=3)` — повтор при временной ошибке.

        - Вызывает `func()` до `attempts` раз.
        - Вернул результат без исключения — вернуть его.
        - Все попытки упали — пробросить **последнее** исключение.

        Пауз между попытками в задании не делаем.
        """),
        """
        def with_retries(func, attempts=3):
            pass
        """,
        """
        def test_success_after_failures():
            calls = []
            def flaky():
                calls.append(1)
                if len(calls) < 3:
                    raise TimeoutError("шлюз не отвечает")
                return "ok"
            assert with_retries(flaky, 3) == "ok"
            assert len(calls) == 3

        def test_gives_up():
            calls = []
            def broken():
                calls.append(1)
                raise TimeoutError(f"попытка {len(calls)}")
            try:
                with_retries(broken, 2)
                assert False, "Должно пробросить исключение"
            except TimeoutError as e:
                assert str(e) == "попытка 2", "Пробросить последнее исключение"
            assert len(calls) == 2
        """,
        """
        def with_retries(func, attempts=3):
            for i in range(attempts):
                try:
                    return func()
                except Exception:
                    if i == attempts - 1:
                        raise
        """,
        hint="В `except` проверь, последняя ли это попытка, и тогда `raise`."),
    out(f"{P}-test-errors-e5", "Что выведет программа? Что биллинг отправил в DLQ и почему.", """
        from kafkafake import Consumer, Producer
        from kafkafake.demo import BillingWorker, OrderService

        OrderService().place(1, "anna", 100)
        p = Producer({"bootstrap.servers": "kafka:9092"})
        p.produce("orders", key="bob", value='{"order_id": 2, "amount": -5}')
        p.produce("orders", key="eve", value="мусор")
        p.flush()

        print("обработано:", BillingWorker().run_once())
        c = Consumer({"bootstrap.servers": "kafka:9092", "group.id": "check", "auto.offset.reset": "earliest"})
        c.subscribe(["orders.dlq"])
        while (m := c.poll(1.0)) is not None:
            print(m.key().decode(), "→", dict(m.headers())["error"].decode()[:30])
        """),
    kft(f"{P}-test-errors-e6", t("""
        Напиши тест `test_payment_matches_order`: заказ `OrderService().place(8, "anna", 990)`, затем `BillingWorker().run_once()`. В `payments` должен быть платёж, у которого `order_id == 8`, `amount == 990` и `status == "paid"`.

        Проверка запустит тест, когда сервис заказов отправляет сумму строкой: биллинг сочтёт такое сообщение битым, и платежа не будет.
        """),
        """
        def test_payment_matches_order():
            pass
        """,
        """
        def test_good():
            passes()

        def test_catches_amount_str():
            catches("amount_str", why="сумма строкой — платёж не создан")
        """,
        """
        def test_payment_matches_order():
            OrderService().place(8, "anna", 990)
            BillingWorker().run_once()
            payments = [json.loads(m.value()) for m in read_all("payments")]
            assert payments == [{"order_id": 8, "amount": 990, "status": "paid"}]
        """,
        hint="Сравни список разобранных платежей с ожидаемым целиком."),
    cod(f"{P}-test-errors-e7", t("""
        Напиши функцию `dlq_report(headers_list)` — сводка по причинам в DLQ.

        - Получает: список заголовков сообщений из DLQ; заголовки каждого — список пар `(имя, байты)`.
        - Возвращает: словарь `{причина: сколько раз}` по заголовку `"error"` (декодированному). Сообщения без `"error"` считай с причиной `"неизвестно"`.
        """),
        """
        def dlq_report(headers_list):
            pass
        """,
        """
        def test_report():
            hs = [[("error", b"amount <= 0")], [("error", "не JSON".encode())], [("error", b"amount <= 0")], [("trace-id", b"x")]]
            assert dlq_report(hs) == {"amount <= 0": 2, "не JSON": 1, "неизвестно": 1}

        def test_empty():
            assert dlq_report([]) == {}
        """,
        """
        def dlq_report(headers_list):
            report = {}
            for headers in headers_list:
                h = dict(headers)
                reason = h["error"].decode() if "error" in h else "неизвестно"
                report[reason] = report.get(reason, 0) + 1
            return report
        """,
        hint="`dict(headers)` превращает пары в словарь."),
    cmd(f"{P}-test-errors-e8", "Посмотри все сообщения, накопившиеся в DLQ-топике `orders.dlq`, с самого начала. Брокер — `localhost:9092`.",
        ["kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders.dlq --from-beginning",
         kcli("kafka-console-consumer", ["--bootstrap-server localhost:9092", "--topic orders.dlq", "--from-beginning"])],
        hint="Консольный консьюмер с `--from-beginning`."),
),

lesson(f"{P}-test-env", "Kafka для тестов: Docker, Testcontainers, CI",
    cod(f"{P}-test-env-e1", t("""
        Напиши `docker-compose.yml` с Kafka для локальных тестов — строкой в переменной `COMPOSE`.

        - Сервис `kafka` с образом `apache/kafka:3.8.0`;
        - порт `9092` хоста проброшен на `9092` контейнера (`"9092:9092"`).

        Проверка разберёт YAML.
        """),
        '''
        COMPOSE = """
        services:
        """
        ''',
        """
        import yaml

        def test_kafka_service():
            data = yaml.safe_load(COMPOSE) or {}
            kafka = data.get("services", {}).get("kafka")
            assert kafka, "Нужен сервис kafka"
            assert kafka.get("image") == "apache/kafka:3.8.0", "Образ apache/kafka:3.8.0"
            assert "9092:9092" in [str(p) for p in kafka.get("ports", [])], 'Порт "9092:9092"'
        """,
        '''
        COMPOSE = """
        services:
          kafka:
            image: apache/kafka:3.8.0
            ports:
              - "9092:9092"
        """
        ''',
        hint="Порт пиши в кавычках — \"9092:9092\"."),
    cod(f"{P}-test-env-e2", t("""
        Напиши функцию `topic_for(test_name)` — имя изолированного топика для теста.

        - Возвращает `"test-"` + имя теста, приведённое к нижнему регистру, где каждый символ, кроме латинских букв, цифр, `.`, `_` и `-`, заменён на `-`.
        - Итоговая строка — не длиннее 60 символов (лишнее обрезать).

        Пример:
        ```
        topic_for("test_Order[anna-500]")   # → "test-test_order-anna-500-"
        ```
        """),
        """
        import re

        def topic_for(test_name):
            pass
        """,
        """
        def test_example():
            assert topic_for("test_Order[anna-500]") == "test-test_order-anna-500-"

        def test_long():
            name = topic_for("x" * 100)
            assert len(name) == 60 and name.startswith("test-")

        def test_cyrillic():
            assert topic_for("заказ") == "test-" + "-" * 5
        """,
        """
        import re

        def topic_for(test_name):
            return ("test-" + re.sub(r"[^a-z0-9._-]", "-", test_name.lower()))[:60]
        """,
        hint="`re.sub(r\"[^a-z0-9._-]\", \"-\", …)` после `.lower()`."),
    kft(f"{P}-test-env-e3", t("""
        Сделай изоляцию через отдельный топик на каждый тест.

        - Фикстура `topic`: имя `f"test-{uuid.uuid4().hex[:8]}"`; создай топик `AdminClient(CONF).create_topics([NewTopic(name, num_partitions=1, replication_factor=1)])[name].result()`; отдай имя через `yield`; после теста удали: `admin.delete_topics([name])`.
        - Тест `test_roundtrip(topic)`: отправь в `topic` сообщение `"ping"` (`Producer(CONF)`, `flush()`), прочитай `read_all(topic)` и проверь, что значение — `b"ping"`.

        Импортируй `AdminClient` и `NewTopic` из `kafkafake`.
        """),
        """
        from kafkafake import AdminClient, NewTopic


        @pytest.fixture
        def topic():
            pass


        def test_roundtrip(topic):
            pass
        """,
        """
        def test_good():
            passes()
            assert "delete_topics" in source(), "Удали топик после теста"

        def test_cleaned():
            run_pytest()
            left = [t for t in kafkafake.cluster.topics if t.startswith("test-")]
            assert not left, f"После теста топик не удалён: {left}"
        """,
        """
        from kafkafake import AdminClient, NewTopic


        @pytest.fixture
        def topic():
            name = f"test-{uuid.uuid4().hex[:8]}"
            admin = AdminClient(CONF)
            admin.create_topics([NewTopic(name, num_partitions=1, replication_factor=1)])[name].result()
            yield name
            admin.delete_topics([name])


        def test_roundtrip(topic):
            p = Producer(CONF)
            p.produce(topic, value="ping")
            p.flush()
            msgs = read_all(topic)
            assert [m.value() for m in msgs] == [b"ping"]
        """,
        hint="Всё до `yield` — подготовка, после — уборка."),
    cmd(f"{P}-test-env-e4", "Запусти Kafka в Docker в фоне: контейнер с именем `kafka` из образа `apache/kafka:3.8.0`, порт 9092 хоста → 9092 контейнера.",
        ["docker run -d --name kafka -p 9092:9092 apache/kafka:3.8.0",
         "re:docker (container )?run (?=(?:.* )?(-d|--detach)(?: |$))(?=(?:.* )?--name kafka(?: |$))(?=(?:.* )?(-p|--publish) 9092:9092(?: |$))(?:\\S+ )*apache/kafka:3\\.8\\.0"],
        hint="Флаги `-d`, `--name`, `-p`, затем образ."),
    cmd(f"{P}-test-env-e5", "В проекте есть `docker-compose.yml` с сервисом `kafka`. Подними только его, в фоне.",
        ["docker compose up -d kafka", "docker-compose up -d kafka", "docker compose up --detach kafka"],
        hint="`docker compose up -d имя_сервиса`."),
    cod(f"{P}-test-env-e6", t("""
        Напиши workflow GitHub Actions, где тесты гоняются с Kafka, — строкой YAML в переменной `WORKFLOW`.

        - `on: [push]`;
        - job `tests` с `runs-on: ubuntu-latest`;
        - в job — сервис `kafka` с образом `apache/kafka:3.8.0` и портом `9092:9092`;
        - шаг `run: pytest` с переменной окружения `KAFKA_BOOTSTRAP: localhost:9092` (в `env` этого шага).
        """),
        '''
        WORKFLOW = """
        on: [push]
        jobs:
          tests:
            runs-on: ubuntu-latest
        """
        ''',
        """
        import yaml

        def load():
            data = yaml.safe_load(WORKFLOW) or {}
            if True in data:
                data["on"] = data.pop(True)
            return data

        def test_service():
            job = load().get("jobs", {}).get("tests", {})
            kafka = job.get("services", {}).get("kafka", {})
            assert kafka.get("image") == "apache/kafka:3.8.0", "Сервис kafka с образом apache/kafka:3.8.0"
            assert "9092:9092" in [str(p) for p in kafka.get("ports", [])], "Порт 9092:9092"

        def test_pytest_step():
            steps = load()["jobs"]["tests"].get("steps", [])
            step = next((s for s in steps if str(s.get("run", "")).strip().startswith("pytest")), None)
            assert step, "Нужен шаг run: pytest"
            assert step.get("env", {}).get("KAFKA_BOOTSTRAP") == "localhost:9092", "env: KAFKA_BOOTSTRAP: localhost:9092"
        """,
        '''
        WORKFLOW = """
        on: [push]
        jobs:
          tests:
            runs-on: ubuntu-latest
            services:
              kafka:
                image: apache/kafka:3.8.0
                ports:
                  - 9092:9092
            steps:
              - uses: actions/checkout@v4
              - run: pip install -r requirements.txt
              - run: pytest
                env:
                  KAFKA_BOOTSTRAP: localhost:9092
        """
        ''',
        hint="`services` — внутри job-а, рядом с `steps`.", xp=25),
    cod(f"{P}-test-env-e7", t("""
        Kafka в контейнере стартует несколько секунд. Напиши функцию `wait_until_ready(check, attempts=30)`.

        - `check()` — пробует подключиться: возвращает `True`, если брокер готов; `False` или исключение — ещё нет.
        - Вызывает `check()` до `attempts` раз; вернула `True` — вернуть номер попытки (с 1).
        - Не дождались — `TimeoutError` с текстом `"Kafka не готова за N попыток"` (N — `attempts`).

        Пауз в задании не делаем.
        """),
        """
        def wait_until_ready(check, attempts=30):
            pass
        """,
        """
        def test_ready_on_third():
            state = {"n": 0}
            def check():
                state["n"] += 1
                if state["n"] == 1:
                    raise ConnectionError("нет соединения")
                return state["n"] >= 3
            assert wait_until_ready(check) == 3

        def test_timeout():
            try:
                wait_until_ready(lambda: False, attempts=4)
                assert False, "Должен быть TimeoutError"
            except TimeoutError as e:
                assert str(e) == "Kafka не готова за 4 попыток"
        """,
        """
        def wait_until_ready(check, attempts=30):
            for attempt in range(1, attempts + 1):
                try:
                    if check():
                        return attempt
                except Exception:
                    pass
            raise TimeoutError(f"Kafka не готова за {attempts} попыток")
        """,
        hint="Исключение из `check()` — тоже «ещё не готова», его глушим."),
    cmd(f"{P}-test-env-e8", "Удали временный тестовый топик `test-orders`. Брокер — `localhost:9092`.",
        ["kafka-topics.sh --delete --topic test-orders --bootstrap-server localhost:9092",
         kcli("kafka-topics", ["--delete", "--topic test-orders", "--bootstrap-server localhost:9092"])],
        hint="Флаг `--delete`."),
),
)
