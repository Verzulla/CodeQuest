"""Тема «Kafka для тестировщика», модуль 1 «Как устроена Kafka» — задания. Теория — в _kfk_t1.py.

Kafka в песочнице — учебная, в памяти (deploy/runner/kafkafake): API как у confluent-kafka,
отличается только импорт: from kafkafake import Producer, Consumer."""
import re

from ._lib import cmd, cod, lesson, module, out, t

P = "kfk"
CONF = 'CONF = {"bootstrap.servers": "kafka:9092"}'


def kcli(tool, flags, tail=""):
    """Вариант ответа «re:…» для консольных утилит Kafka: tool или tool.sh, флаги в любом порядке.
    Флаг с аргументом пишется «--topic orders»; допускается и «--topic=orders»."""
    def flag(f):
        name, _, arg = f.partition(" ")
        body = re.escape(name) + ((r"(?: |=)" + re.escape(arg)) if arg else "")
        return f"(?=(?:.* )?{body}(?: |$))"
    look = "".join(flag(f) for f in flags)
    rest = f"(?:\\S+ )*{re.escape(tail)}" if tail else "\\S+(?: \\S+)*"
    return f"re:{re.escape(tool)}(?:\\.sh)? {look}{rest}"


m1 = module(f"{P}-m1", "Как устроена Kafka", "🧭", "Продюсеры и консьюмеры, топики и партиции, группы и офсеты, реплики и гарантии доставки",

lesson(f"{P}-intro", "Зачем нужна Kafka",
    out(f"{P}-intro-e1", "Что выведет программа? Журнал сообщений и два читателя, у каждого — свой офсет.", """
        log = ["заказ 1", "заказ 2", "заказ 3"]
        offsets = {"billing": 0, "analytics": 0}

        def read(group):
            pos = offsets[group]
            if pos == len(log):
                return None
            offsets[group] = pos + 1
            return log[pos]

        print(read("billing"), read("billing"))
        print(read("analytics"))
        print(len(log), offsets)
        """),
    cod(f"{P}-intro-e2", t("""
        Напиши функцию `read_from(log, offset)` — что прочитает консьюмер, начиная с офсета.

        - Получает: `log` — список сообщений партиции (офсет = индекс); `offset` — с какого читать.
        - Возвращает: кортеж `(сообщения, новый_офсет)`: все сообщения с `offset` до конца и офсет, с которого читать в следующий раз.
        - Если `offset` уже в конце (или дальше) — `([], len(log))`.

        Пример:
        ```
        read_from(["a", "b", "c"], 1)   # → (["b", "c"], 3)
        read_from(["a", "b", "c"], 3)   # → ([], 3)
        ```
        Журнал не меняется: в Kafka прочитанное не удаляется.
        """),
        """
        def read_from(log, offset):
            pass
        """,
        """
        def test_read():
            assert read_from(["a", "b", "c"], 1) == (["b", "c"], 3)
            assert read_from(["a", "b", "c"], 0) == (["a", "b", "c"], 3)

        def test_end():
            assert read_from(["a", "b", "c"], 3) == ([], 3)
            assert read_from(["a"], 5) == ([], 1), "Офсет дальше конца — читать нечего"

        def test_log_untouched():
            log = ["a", "b"]
            read_from(log, 0)
            assert log == ["a", "b"], "Чтение не должно менять журнал"
        """,
        """
        def read_from(log, offset):
            if offset >= len(log):
                return [], len(log)
            return log[offset:], len(log)
        """,
        hint="Срез `log[offset:]` возвращает новый список, журнал не меняется."),
    cod(f"{P}-intro-e3", t("""
        Напиши функцию `fan_out(log, groups)` — что получит каждая группа консьюмеров.

        - Получает: `log` — список сообщений; `groups` — словарь `{группа: закоммиченный офсет}`.
        - Возвращает: словарь `{группа: список ещё не прочитанных ею сообщений}`.

        Группы независимы: каждая читает **все** сообщения начиная со своего офсета.

        Пример:
        ```
        fan_out(["o1", "o2", "o3"], {"billing": 2, "analytics": 0})
        # → {"billing": ["o3"], "analytics": ["o1", "o2", "o3"]}
        ```
        """),
        """
        def fan_out(log, groups):
            pass
        """,
        """
        def test_fan_out():
            assert fan_out(["o1", "o2", "o3"], {"billing": 2, "analytics": 0}) == {"billing": ["o3"], "analytics": ["o1", "o2", "o3"]}

        def test_caught_up():
            assert fan_out(["o1"], {"billing": 1}) == {"billing": []}
        """,
        """
        def fan_out(log, groups):
            return {group: log[offset:] for group, offset in groups.items()}
        """,
        hint="Словарное включение: для каждой группы — срез журнала с её офсета."),
    cod(f"{P}-intro-e4", t("""
        Напиши функцию `lag(log_end, committed)` — отставание группы по всем партициям.

        - Получает: `log_end` — словарь `{партиция: конец журнала}`; `committed` — `{партиция: закоммиченный офсет}`. Если партиции нет в `committed`, группа её ещё не читала — считай офсет `0`.
        - Возвращает: общее число непрочитанных сообщений (сумму по партициям).

        Пример:
        ```
        lag({0: 120, 1: 130, 2: 141}, {0: 120, 1: 98, 2: 140})   # → 33
        lag({0: 5, 1: 7}, {0: 5})                                 # → 7
        ```
        """),
        """
        def lag(log_end, committed):
            pass
        """,
        """
        def test_lag():
            assert lag({0: 120, 1: 130, 2: 141}, {0: 120, 1: 98, 2: 140}) == 33

        def test_never_read():
            assert lag({0: 5, 1: 7}, {0: 5}) == 7, "Нет коммита — считай с нуля"

        def test_zero():
            assert lag({0: 3}, {0: 3}) == 0
        """,
        """
        def lag(log_end, committed):
            return sum(end - committed.get(p, 0) for p, end in log_end.items())
        """,
        hint="`committed.get(p, 0)` — офсет или ноль."),
    out(f"{P}-intro-e5", "Что выведет программа? Сообщения хранятся заданное время (retention), прочитали их или нет.", """
        retention_hours = 24
        now = 100
        log = [("заказ 1", 70), ("заказ 2", 80), ("заказ 3", 95)]   # (сообщение, час записи)

        kept = [m for m, hour in log if now - hour < retention_hours]
        print(kept)
        print(len(log) - len(kept), "удалено по сроку")
        """),
    cmd(f"{P}-intro-e6", "Как по-английски называется номер сообщения в партиции (0, 1, 2…)? Введи одно слово.",
        ["offset", "re:(?i)offset"],
        hint="«Смещение» по-английски."),
    cmd(f"{P}-intro-e7", "Как называется один сервер Kafka? Введи английский термин одним словом.",
        ["broker", "re:(?i)broker"],
        hint="Несколько таких серверов вместе — кластер."),
    cmd(f"{P}-intro-e8", "Как по-английски называют отставание группы консьюмеров — сколько сообщений ещё не прочитано? Одно слово.",
        ["lag", "re:(?i)(consumer )?lag"],
        hint="Короткое слово из трёх букв."),
),

lesson(f"{P}-partitions", "Ключи и партиции",
    out(f"{P}-partitions-e1", "Что выведет программа? Партиция выбирается по ключу: crc32(ключ) % 3.", """
        import zlib

        for key in ["user-1", "user-2", "user-1", "user-3"]:
            print(key, zlib.crc32(key.encode()) % 3)
        """),
    cod(f"{P}-partitions-e2", t("""
        Напиши функцию `partition_for(key, partitions)` — в какую партицию попадёт сообщение.

        - Получает: `key` — ключ-строку; `partitions` — число партиций.
        - Возвращает: `zlib.crc32(ключ в байтах) % partitions`. Строку в байты — `key.encode()`.

        Пример:
        ```
        partition_for("user-1", 3)   # → то же число, что zlib.crc32(b"user-1") % 3
        ```
        В настоящей Kafka хеш — murmur2, но правило то же: один ключ → одна партиция.
        """),
        """
        import zlib

        def partition_for(key, partitions):
            pass
        """,
        """
        import zlib

        def test_formula():
            for key in ["user-1", "user-2", "order-501", "x"]:
                assert partition_for(key, 3) == zlib.crc32(key.encode()) % 3, key

        def test_stable():
            assert partition_for("anna", 5) == partition_for("anna", 5), "Один ключ — всегда одна партиция"

        def test_range():
            assert all(0 <= partition_for(f"k{i}", 4) < 4 for i in range(50))
        """,
        """
        import zlib

        def partition_for(key, partitions):
            return zlib.crc32(key.encode()) % partitions
        """,
        hint="`zlib.crc32(key.encode()) % partitions`."),
    cod(f"{P}-partitions-e3", t("""
        Напиши функцию `ordered_per_key(messages)` — проверка порядка, которую делают в тестах.

        - Получает: `messages` — список пар `(ключ, номер)` в том порядке, в каком их прочитал консьюмер. Номер — порядковый номер события у этого ключа.
        - Возвращает: `True`, если для **каждого ключа** номера идут строго по возрастанию; иначе `False`.

        Порядок между разными ключами не важен — Kafka его и не гарантирует.

        Пример:
        ```
        ordered_per_key([("a", 1), ("b", 1), ("a", 2), ("b", 2)])   # → True
        ordered_per_key([("a", 2), ("a", 1)])                         # → False
        ```
        """),
        """
        def ordered_per_key(messages):
            pass
        """,
        """
        def test_ok():
            assert ordered_per_key([("a", 1), ("b", 1), ("a", 2), ("b", 2)]) is True
            assert ordered_per_key([("b", 5), ("a", 1), ("a", 3)]) is True, "Между ключами порядок не важен"

        def test_broken():
            assert ordered_per_key([("a", 2), ("a", 1)]) is False
            assert ordered_per_key([("a", 1), ("a", 1)]) is False, "Повтор номера — тоже нарушение"

        def test_empty():
            assert ordered_per_key([]) is True
        """,
        """
        def ordered_per_key(messages):
            last = {}
            for key, num in messages:
                if key in last and num <= last[key]:
                    return False
                last[key] = num
            return True
        """,
        hint="Храни в словаре последний номер для каждого ключа."),
    cod(f"{P}-partitions-e4", t("""
        Напиши функцию `hot_partitions(counts, share=0.5)` — найти горячие партиции.

        - Получает: `counts` — словарь `{партиция: число сообщений}`; `share` — порог доли.
        - Возвращает: **отсортированный** список партиций, в которые пришло больше `share` от всех сообщений. Если сообщений нет — пустой список.

        Пример:
        ```
        hot_partitions({0: 10, 1: 85, 2: 5})        # → [1]
        hot_partitions({0: 30, 1: 35, 2: 35})       # → []
        hot_partitions({0: 30, 1: 35, 2: 35}, 0.3)  # → [1, 2]
        ```
        """),
        """
        def hot_partitions(counts, share=0.5):
            pass
        """,
        """
        def test_hot():
            assert hot_partitions({0: 10, 1: 85, 2: 5}) == [1]

        def test_even():
            assert hot_partitions({0: 30, 1: 35, 2: 35}) == []
            assert hot_partitions({0: 30, 1: 35, 2: 35}, 0.3) == [1, 2]

        def test_empty():
            assert hot_partitions({0: 0, 1: 0}) == []
        """,
        """
        def hot_partitions(counts, share=0.5):
            total = sum(counts.values())
            if total == 0:
                return []
            return sorted(p for p, n in counts.items() if n / total > share)
        """,
        hint="Сначала общий итог, потом отбор `n / total > share`."),
    out(f"{P}-partitions-e5", "Что выведет программа? Число партиций увеличили с 3 до 4 — где теперь окажутся ключи?", """
        import zlib

        keys = ["user-1", "user-2", "user-3", "user-4"]
        moved = [k for k in keys if zlib.crc32(k.encode()) % 3 != zlib.crc32(k.encode()) % 4]
        print(len(moved), "из", len(keys), "ключей сменили партицию")
        """),
    cod(f"{P}-partitions-e6", t("""
        Поработай с учебной Kafka. Напиши функцию `send_events(producer, events)`.

        - Получает: `producer` — продюсер `kafkafake.Producer`; `events` — список пар `(user, текст)`.
        - Делает: отправляет каждое событие в топик `"events"` с ключом `user` и значением `текст`, в конце вызывает `producer.flush()`.
        - Возвращает: словарь `{user: множество партиций, куда ушли его события}`.

        Номер партиции придёт в **колбэк доставки**: `producer.produce(topic, key=..., value=..., on_delivery=cb)`, где `cb(err, msg)`, а `msg.partition()` — номер партиции. Колбэки вызываются во время `flush()`.

        Если всё правильно, у каждого пользователя будет ровно одна партиция.
        """),
        """
        from kafkafake import Producer

        def send_events(producer, events):
            pass
        """,
        """
        import kafkafake
        from kafkafake import Producer, Consumer

        def test_one_partition_per_user():
            kafkafake.reset()
            p = Producer({"bootstrap.servers": "kafka:9092"})
            events = [("anna", "1"), ("bob", "1"), ("anna", "2"), ("eve", "1"), ("bob", "2"), ("anna", "3")]
            res = send_events(p, events)
            assert set(res) == {"anna", "bob", "eve"}, f"Получено {res}"
            assert all(len(parts) == 1 for parts in res.values()), "Один ключ — одна партиция"

        def test_really_sent():
            kafkafake.reset()
            p = Producer({"bootstrap.servers": "kafka:9092"})
            send_events(p, [("anna", "x")])
            c = Consumer({"bootstrap.servers": "kafka:9092", "group.id": "t", "auto.offset.reset": "earliest"})
            c.subscribe(["events"])
            m = c.poll(1)
            assert m is not None and m.key() == b"anna" and m.value() == b"x", "Сообщение должно уйти в топик events с ключом"
        """,
        """
        from kafkafake import Producer

        def send_events(producer, events):
            result = {}

            def on_delivery(err, msg):
                result.setdefault(msg.key().decode(), set()).add(msg.partition())

            for user, text in events:
                producer.produce("events", key=user, value=text, on_delivery=on_delivery)
            producer.flush()
            return result
        """,
        hint="Колбэк складывает `msg.partition()` в словарь по `msg.key().decode()`; не забудь `flush()`.", xp=20),
    cmd(f"{P}-partitions-e7", "Создай топик `orders` с 3 партициями. Брокер — `localhost:9092`.",
        ["kafka-topics.sh --create --topic orders --partitions 3 --bootstrap-server localhost:9092",
         kcli("kafka-topics", ["--create", "--topic orders", "--partitions 3", "--bootstrap-server localhost:9092"])],
        hint="`kafka-topics.sh --create --topic … --partitions … --bootstrap-server …`."),
    cmd(f"{P}-partitions-e8", "Посмотри, сколько партиций у топика `orders` и какие брокеры их лидеры. Брокер — `localhost:9092`.",
        ["kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092",
         kcli("kafka-topics", ["--describe", "--topic orders", "--bootstrap-server localhost:9092"])],
        hint="Флаг `--describe`."),
),

lesson(f"{P}-consumers", "Консьюмеры, группы и офсеты",
    out(f"{P}-consumers-e1", "Что выведет программа? Партиции раздаются консьюмерам группы по кругу.", """
        partitions = [0, 1, 2]
        for consumers in (["c1"], ["c1", "c2"], ["c1", "c2", "c3", "c4"]):
            plan = {c: [] for c in consumers}
            for p in partitions:
                plan[consumers[p % len(consumers)]].append(p)
            print(plan)
        """),
    cod(f"{P}-consumers-e2", t("""
        Напиши функцию `assign(partitions, consumers)` — раздача партиций в группе.

        - Получает: `partitions` — число партиций; `consumers` — список имён консьюмеров группы.
        - Возвращает: словарь `{консьюмер: список его партиций}`: партиция `p` достаётся консьюмеру `consumers[p % len(consumers)]`. У лишних консьюмеров — пустой список.

        Пример:
        ```
        assign(3, ["c1", "c2"])               # → {"c1": [0, 2], "c2": [1]}
        assign(2, ["c1", "c2", "c3"])         # → {"c1": [0], "c2": [1], "c3": []}
        ```
        """),
        """
        def assign(partitions, consumers):
            pass
        """,
        """
        def test_assign():
            assert assign(3, ["c1", "c2"]) == {"c1": [0, 2], "c2": [1]}

        def test_idle():
            assert assign(2, ["c1", "c2", "c3"]) == {"c1": [0], "c2": [1], "c3": []}, "Лишний консьюмер простаивает"

        def test_each_partition_once():
            plan = assign(7, ["a", "b", "c"])
            assert sorted(p for ps in plan.values() for p in ps) == list(range(7)), "Каждая партиция — ровно одному"
        """,
        """
        def assign(partitions, consumers):
            plan = {c: [] for c in consumers}
            for p in range(partitions):
                plan[consumers[p % len(consumers)]].append(p)
            return plan
        """,
        hint="Сначала словарь с пустыми списками, потом раздача по `p % len(consumers)`."),
    cod(f"{P}-consumers-e3", t("""
        Напиши функцию `lag_report(log_end, committed)` — lag по партициям, как в `kafka-consumer-groups --describe`.

        - Получает: `log_end` и `committed` — словари `{партиция: офсет}` (как в предыдущем уроке; нет коммита — `0`).
        - Возвращает: список строк по партициям **в порядке номеров**: `"P1 lag 32"`. В конец — строка `"всего 33"`.

        Пример:
        ```
        lag_report({0: 120, 1: 130, 2: 141}, {0: 120, 1: 98, 2: 140})
        # → ["P0 lag 0", "P1 lag 32", "P2 lag 1", "всего 33"]
        ```
        """),
        """
        def lag_report(log_end, committed):
            pass
        """,
        """
        def test_report():
            assert lag_report({0: 120, 1: 130, 2: 141}, {0: 120, 1: 98, 2: 140}) == ["P0 lag 0", "P1 lag 32", "P2 lag 1", "всего 33"]

        def test_sorted_and_missing():
            assert lag_report({2: 5, 0: 1}, {}) == ["P0 lag 1", "P2 lag 5", "всего 6"]
        """,
        """
        def lag_report(log_end, committed):
            lines, total = [], 0
            for p in sorted(log_end):
                lag = log_end[p] - committed.get(p, 0)
                total += lag
                lines.append(f"P{p} lag {lag}")
            return lines + [f"всего {total}"]
        """,
        hint="`sorted(log_end)` перебирает партиции по порядку."),
    out(f"{P}-consumers-e4", "Что выведет программа? Новая группа без коммитов: откуда она начнёт читать при разных `auto.offset.reset`?", """
        log_end = 50          # в партиции уже 50 сообщений
        committed = None      # группа новая — коммитов нет

        for reset in ("latest", "earliest"):
            start = committed if committed is not None else (log_end if reset == "latest" else 0)
            print(reset, "→ начнёт с офсета", start, "| прочитает старых:", log_end - start)
        """),
    cod(f"{P}-consumers-e5", t("""
        Напиши функцию `read_all(topic, group)` на учебной Kafka: прочитать всё, что лежит в топике, **с начала**.

        - Создай консьюмер: `Consumer({"bootstrap.servers": "kafka:9092", "group.id": group, "auto.offset.reset": "earliest"})`.
        - Подпишись на топик: `subscribe([topic])`.
        - Читай `poll(1.0)`, пока он не вернёт `None` (учебная Kafka отдаёт `None`, когда новых сообщений нет).
        - Закрой консьюмер `close()` и верни список **значений**, декодированных в строки (`msg.value().decode()`).
        """),
        """
        from kafkafake import Consumer

        def read_all(topic, group):
            pass
        """,
        """
        import kafkafake
        from kafkafake import Producer

        def fill(n):
            kafkafake.reset()   # каждая проверка — с чистого кластера
            p = Producer({"bootstrap.servers": "kafka:9092"})
            for i in range(n):
                p.produce("orders", key="u", value=f"m{i}")
            p.flush()

        def test_reads_from_beginning():
            fill(3)
            assert read_all("orders", "g1") == ["m0", "m1", "m2"], "Нужен auto.offset.reset=earliest и чтение до None"

        def test_group_continues():
            fill(2)
            assert read_all("orders", "g2") == ["m0", "m1"]
            assert read_all("orders", "g2") == [], "Та же группа — уже всё прочитала (close закоммитил офсеты)"
            assert read_all("orders", "other") == ["m0", "m1"], "Другая группа читает всё заново"
        """,
        """
        from kafkafake import Consumer

        def read_all(topic, group):
            consumer = Consumer({"bootstrap.servers": "kafka:9092", "group.id": group, "auto.offset.reset": "earliest"})
            consumer.subscribe([topic])
            values = []
            while (msg := consumer.poll(1.0)) is not None:
                values.append(msg.value().decode())
            consumer.close()
            return values
        """,
        hint="Цикл `while (msg := consumer.poll(1.0)) is not None:`.", xp=20),
    cmd(f"{P}-consumers-e6", "Прочитай топик `orders` с самого начала консольным консьюмером. Брокер — `localhost:9092`.",
        ["kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning",
         kcli("kafka-console-consumer", ["--bootstrap-server localhost:9092", "--topic orders", "--from-beginning"])],
        hint="Флаг `--from-beginning`."),
    cmd(f"{P}-consumers-e7", "Посмотри офсеты и lag группы `billing` по партициям. Брокер — `localhost:9092`.",
        ["kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group billing",
         kcli("kafka-consumer-groups", ["--bootstrap-server localhost:9092", "--describe", "--group billing"])],
        hint="`kafka-consumer-groups.sh … --describe --group …`."),
    cmd(f"{P}-consumers-e8", "Перемотай офсеты группы `billing` в топике `orders` на самое начало и примени изменение. Брокер — `localhost:9092`.",
        ["kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group billing --topic orders --reset-offsets --to-earliest --execute",
         kcli("kafka-consumer-groups", ["--bootstrap-server localhost:9092", "--group billing", "--topic orders", "--reset-offsets", "--to-earliest", "--execute"])],
        hint="`--reset-offsets --to-earliest`, а чтобы применить — `--execute`."),
),

lesson(f"{P}-reliability", "Реплики и гарантии доставки",
    out(f"{P}-reliability-e1", "Что выведет программа? Два консьюмера падают на сообщении 3: один коммитит до обработки, другой — после.", """
        def run(commit_first):
            committed, processed = 0, []
            for offset, msg in enumerate(["m0", "m1", "m2", "m3", "m4"]):
                if commit_first:
                    committed = offset + 1
                if msg == "m3":
                    break                      # сбой при обработке m3
                processed.append(msg)
                if not commit_first:
                    committed = offset + 1
            return committed, processed

        for mode in (True, False):
            committed, done = run(mode)
            print("коммит до обработки" if mode else "коммит после обработки", "| обработано:", done, "| после перезапуска читаем с офсета", committed)
        """),
    cod(f"{P}-reliability-e2", t("""
        Напиши функцию `can_write(acks, isr, min_isr)` — примет ли брокер запись.

        - Получает: `acks` — `"0"`, `"1"` или `"all"`; `isr` — сколько реплик сейчас синхронны (in-sync); `min_isr` — настройка `min.insync.replicas`.
        - Возвращает:
          - для `"0"` и `"1"` — `True`, если жив хотя бы лидер (`isr >= 1`);
          - для `"all"` — `True`, только если `isr >= min_isr`.

        Пример:
        ```
        can_write("all", 1, 2)   # → False  (живых копий мало — запись отклонена)
        can_write("1", 1, 2)     # → True   (лидер есть — пишет, но без копий)
        ```
        """),
        """
        def can_write(acks, isr, min_isr):
            pass
        """,
        """
        def test_all():
            assert can_write("all", 3, 2) is True
            assert can_write("all", 2, 2) is True
            assert can_write("all", 1, 2) is False, "acks=all и мало ISR — отказ"

        def test_one_and_zero():
            assert can_write("1", 1, 2) is True
            assert can_write("0", 1, 3) is True
            assert can_write("1", 0, 1) is False, "Нет даже лидера"
        """,
        """
        def can_write(acks, isr, min_isr):
            if acks == "all":
                return isr >= min_isr
            return isr >= 1
        """,
        hint="Отдельно ветка для `\"all\"`, для остальных достаточно живого лидера."),
    cod(f"{P}-reliability-e3", t("""
        Напиши функцию `compact(log)` — что останется после compaction.

        - Получает: `log` — список пар `(ключ, значение)` в порядке записи.
        - Возвращает: список пар, где для каждого ключа осталось только **последнее** значение. Порядок — по позиции этого последнего сообщения в журнале.

        Пример:
        ```
        compact([("anna", "Москва"), ("bob", "Казань"), ("anna", "Сочи")])
        # → [("bob", "Казань"), ("anna", "Сочи")]
        ```
        """),
        """
        def compact(log):
            pass
        """,
        """
        def test_compact():
            assert compact([("anna", "Москва"), ("bob", "Казань"), ("anna", "Сочи")]) == [("bob", "Казань"), ("anna", "Сочи")]

        def test_single():
            assert compact([("x", 1)]) == [("x", 1)]
            assert compact([]) == []
        """,
        """
        def compact(log):
            last = {}
            for i, (key, value) in enumerate(log):
                last[key] = (i, value)
            return [(key, value) for key, (i, value) in sorted(last.items(), key=lambda kv: kv[1][0])]
        """,
        hint="Запомни для каждого ключа позицию и значение последней записи, потом отсортируй по позиции."),
    cod(f"{P}-reliability-e4", t("""
        Напиши класс `IdempotentHandler` — консьюмер, которому не страшны дубли (at-least-once).

        - `IdempotentHandler()` — пустой.
        - `handle(event)` — `event` — словарь с полем `"id"`. Если событие с таким `id` ещё не обрабатывалось — добавить его в список `self.done` и вернуть `True`. Если уже было — ничего не делать и вернуть `False`.

        Пример:
        ```
        h = IdempotentHandler()
        h.handle({"id": 1, "amount": 100})   # → True
        h.handle({"id": 1, "amount": 100})   # → False — дубль
        h.done                               # → [{"id": 1, "amount": 100}]
        ```
        """),
        """
        class IdempotentHandler:
            def __init__(self):
                pass

            def handle(self, event):
                pass
        """,
        """
        def test_dedupe():
            h = IdempotentHandler()
            assert h.handle({"id": 1, "amount": 100}) is True
            assert h.handle({"id": 2, "amount": 50}) is True
            assert h.handle({"id": 1, "amount": 100}) is False, "Повтор id — пропускаем"
            assert h.done == [{"id": 1, "amount": 100}, {"id": 2, "amount": 50}]

        def test_separate_instances():
            a, b = IdempotentHandler(), IdempotentHandler()
            a.handle({"id": 1})
            assert b.handle({"id": 1}) is True, "У каждого обработчика своя память"
        """,
        """
        class IdempotentHandler:
            def __init__(self):
                self.done = []
                self.seen = set()

            def handle(self, event):
                if event["id"] in self.seen:
                    return False
                self.seen.add(event["id"])
                self.done.append(event)
                return True
        """,
        hint="Множество `seen` с уже обработанными id; создавай его в `__init__`, а не на уровне класса."),
    out(f"{P}-reliability-e5", "Что выведет программа? Продюсер повторяет отправку после сетевого сбоя — с идемпотентностью и без.", """
        def broker_log(idempotent):
            log, seen = [], set()
            attempts = [(1, "заказ 1"), (2, "заказ 2"), (2, "заказ 2"), (3, "заказ 3")]   # (номер, данные): 2 отправлен дважды
            for seq, data in attempts:
                if idempotent and seq in seen:
                    continue
                seen.add(seq)
                log.append(data)
            return log

        print(broker_log(False))
        print(broker_log(True))
        """),
    cmd(f"{P}-reliability-e6", "Создай топик `payments` с 3 партициями и тремя копиями каждой партиции. Брокер — `localhost:9092`.",
        ["kafka-topics.sh --create --topic payments --partitions 3 --replication-factor 3 --bootstrap-server localhost:9092",
         kcli("kafka-topics", ["--create", "--topic payments", "--partitions 3", "--replication-factor 3", "--bootstrap-server localhost:9092"])],
        hint="Число копий — `--replication-factor`."),
    cmd(f"{P}-reliability-e7", "Какое значение `acks` у продюсера самое надёжное — ждать записи на всех синхронных репликах?",
        ["all", "re:(?i)(acks=)?(all|-1)"],
        hint="Не 0 и не 1."),
    cmd(f"{P}-reliability-e8", "Консьюмер сначала обрабатывает сообщение, потом коммитит. Как называется эта гарантия доставки? Введи термин по-английски.",
        ["at-least-once", "re:(?i)at[- ]least[- ]once"],
        hint="«Хотя бы один раз» — возможны дубли."),
),
)
