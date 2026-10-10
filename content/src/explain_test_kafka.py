"""Тема «Kafka для тестировщика» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "kfk"

EXPLAIN = {

# ===== Модуль 1. Как устроена Kafka =====

f"{P}-intro-e1": x(
    idea="Журнал общий, а офсет у каждой группы свой: чтение одной группы не мешает другой.",
    trace=[
        ('print(read("billing"), read("billing"))', "billing: 0 → 1 → 2", "заказ 1 заказ 2"),
        ('print(read("analytics"))', "analytics читает с нуля: 0 → 1", "заказ 1"),
        ("print(len(log), offsets)", "журнал не уменьшился", "3 {'billing': 2, 'analytics': 1}"),
    ],
    mistake="Думать, что billing «забрал» заказы 1 и 2 и аналитике они не достанутся."),

f"{P}-intro-e2": x(
    idea="Консьюмер читает с офсета до конца; новый офсет — длина журнала. Сам журнал не меняется.",
    lines=[
        ("if offset >= len(log):\n        return [], len(log)", "Читать нечего."),
        ("return log[offset:], len(log)", "Срез — новый список, журнал цел."),
    ],
    mistake="Удалять прочитанное из списка (`pop`) — в Kafka так не бывает, другие группы его ещё не читали."),

f"{P}-intro-e3": x(
    idea="Каждая группа получает свой срез журнала — со своего офсета.",
    lines=[("return {group: log[offset:] for group, offset in groups.items()}", "Срез на каждую группу.")],
    mistake="Делить сообщения между группами — делят партиции только консьюмеры внутри одной группы."),

f"{P}-intro-e4": x(
    idea="Lag по партиции = конец журнала − закоммиченный офсет; общий — сумма.",
    lines=[("return sum(end - committed.get(p, 0) for p, end in log_end.items())", "Нет коммита — офсет 0.")],
    mistake="`committed[p]` упадёт с KeyError на партиции, которую группа ещё не читала."),

f"{P}-intro-e5": x(
    idea="Retention удаляет сообщения старше срока — неважно, прочитаны они или нет.",
    trace=[
        ("kept = [m for m, hour in log if now - hour < retention_hours]", "возраст: 30, 20, 5 часов", ""),
        ("print(kept)", "старше 24 часов только заказ 1", "['заказ 2', 'заказ 3']"),
        ('print(len(log) - len(kept), "удалено по сроку")', "", "1 удалено по сроку"),
    ],
    mistake="Считать, что сообщение удаляется после чтения."),

f"{P}-intro-e6": x(idea="Номер сообщения в партиции — offset.", lines=[("offset", "0, 1, 2… внутри одной партиции.")],
    mistake="Путать с partition — номером самой партиции."),

f"{P}-intro-e7": x(idea="Один сервер Kafka — broker; несколько — кластер.", lines=[("broker", "Хранит партиции и отдаёт сообщения.")],
    mistake="Называть брокером весь кластер."),

f"{P}-intro-e8": x(idea="Lag — сколько сообщений группа ещё не прочитала.", lines=[("lag", "Растёт — консьюмеры не успевают.")],
    mistake="Путать lag с задержкой сети (latency)."),

f"{P}-partitions-e1": x(
    idea="Партиция = crc32(ключ) % 3: одинаковый ключ всегда даёт одинаковый результат.",
    trace=[
        ('print(key, zlib.crc32(key.encode()) % 3)', "user-1", "user-1 2"),
        ('print(key, zlib.crc32(key.encode()) % 3)', "user-2", "user-2 1"),
        ('print(key, zlib.crc32(key.encode()) % 3)', "user-1 снова — та же партиция", "user-1 2"),
        ('print(key, zlib.crc32(key.encode()) % 3)', "user-3", "user-3 0"),
    ],
    mistake="Ожидать, что ключи разложатся по порядку 0, 1, 2 — хеш их «перемешивает»."),

f"{P}-partitions-e2": x(
    idea="Строку переводим в байты и берём остаток от деления хеша на число партиций.",
    lines=[("return zlib.crc32(key.encode()) % partitions", "Байты → хеш → остаток.")],
    mistake="`hash(key)` — встроенный hash строк в Python меняется от запуска к запуску."),

f"{P}-partitions-e3": x(
    idea="Для каждого ключа помним последний номер; новый должен быть строго больше.",
    lines=[
        ("if key in last and num <= last[key]:\n            return False", "Номер не вырос — порядок нарушен."),
        ("last[key] = num", "Запомнили последний номер ключа."),
    ],
    mistake="Проверять порядок по всему списку — между ключами порядок и не гарантирован."),

f"{P}-partitions-e4": x(
    idea="Доля партиции = её сообщения / все сообщения; горячие — выше порога.",
    lines=[
        ("if total == 0:\n        return []", "Без сообщений делить нельзя."),
        ("return sorted(p for p, n in counts.items() if n / total > share)", "Отбор и сортировка."),
    ],
    mistake="Забыть про ноль сообщений — ZeroDivisionError."),

f"{P}-partitions-e5": x(
    idea="Добавили партицию — изменился делитель, и большинство ключей переехали.",
    trace=[("moved = [k for k in keys if zlib.crc32(k.encode()) % 3 != zlib.crc32(k.encode()) % 4]", "сравниваем % 3 и % 4", ""),
           ('print(len(moved), "из", len(keys), "ключей сменили партицию")', "3 ключа поменяли партицию", "3 из 4 ключей сменили партицию")],
    mistake="Считать, что старые ключи остаются на месте после увеличения числа партиций."),

f"{P}-partitions-e6": x(
    idea="Номер партиции знает только брокер — он приходит в колбэк доставки во время flush().",
    lines=[
        ("result.setdefault(msg.key().decode(), set()).add(msg.partition())", "Ключ в байтах → строка; копим партиции."),
        ('producer.produce("events", key=user, value=text, on_delivery=on_delivery)', "Ключ — пользователь."),
        ("producer.flush()", "Без flush колбэки не вызовутся."),
    ],
    mistake="Читать результат до `flush()` — сообщения ещё в буфере продюсера."),

f"{P}-partitions-e7": x(idea="Создание топика: имя, число партиций и адрес брокера.",
    lines=[("kafka-topics.sh --create", "Создать."), ("--topic orders --partitions 3", "Имя и партиции."), ("--bootstrap-server localhost:9092", "Куда подключаться.")],
    mistake="Забыть `--bootstrap-server` — утилита не знает, где кластер."),

f"{P}-partitions-e8": x(idea="`--describe` показывает партиции, лидеров и реплики топика.",
    lines=[("kafka-topics.sh --describe --topic orders", "Описание топика.")],
    mistake="`--list` — только имена топиков, без партиций."),

f"{P}-consumers-e1": x(
    idea="Партиция p достаётся консьюмеру с индексом p % число_консьюмеров.",
    trace=[
        ("print(plan)", "1 консьюмер — все партиции", "{'c1': [0, 1, 2]}"),
        ("print(plan)", "2 консьюмера", "{'c1': [0, 2], 'c2': [1]}"),
        ("print(plan)", "4 консьюмера, 3 партиции — c4 без работы", "{'c1': [0], 'c2': [1], 'c3': [2], 'c4': []}"),
    ],
    mistake="Ожидать, что 4-й консьюмер ускорит чтение 3 партиций."),

f"{P}-consumers-e2": x(
    idea="Сначала у всех пустые списки, потом раздача партиций по кругу.",
    lines=[("plan = {c: [] for c in consumers}", "Лишний консьюмер останется с пустым списком."),
           ("plan[consumers[p % len(consumers)]].append(p)", "По кругу.")],
    mistake="Создавать ключи только при раздаче — тогда простаивающего консьюмера не будет в ответе."),

f"{P}-consumers-e3": x(
    idea="Идём по партициям по порядку, считаем lag каждой и общий итог.",
    lines=[("for p in sorted(log_end):", "Порядок номеров."),
           ("lag = log_end[p] - committed.get(p, 0)", "Нет коммита — 0."),
           ('return lines + [f"всего {total}"]', "Итог в конце.")],
    mistake="Перебирать словарь без sorted — порядок партиций может быть любым."),

f"{P}-consumers-e4": x(
    idea="Без коммитов стартовую точку задаёт auto.offset.reset: latest — конец, earliest — начало.",
    trace=[('print(reset, "→ начнёт с офсета", start, "| прочитает старых:", log_end - start)', "latest: start = 50", "latest → начнёт с офсета 50 | прочитает старых: 0"),
           ('print(reset, "→ начнёт с офсета", start, "| прочитает старых:", log_end - start)', "earliest: start = 0", "earliest → начнёт с офсета 0 | прочитает старых: 50")],
    mistake="Писать в тесте консьюмер с latest после отправки сообщения — он его не увидит."),

f"{P}-consumers-e5": x(
    idea="Подписка, чтение до None, закрытие. earliest — чтобы прочитать уже лежащие сообщения.",
    lines=[('consumer = Consumer({"bootstrap.servers": "kafka:9092", "group.id": group, "auto.offset.reset": "earliest"})', "С начала."),
           ("while (msg := consumer.poll(1.0)) is not None:", "Пока есть сообщения."),
           ("values.append(msg.value().decode())", "Байты → строка."),
           ("consumer.close()", "Закрытие коммитит офсеты — та же группа второй раз прочитает пусто.")],
    mistake="Не закрыть консьюмер — группа не закоммитит офсеты и «висит» в кластере."),

f"{P}-consumers-e6": x(idea="`--from-beginning` — читать топик с самого начала.",
    lines=[("kafka-console-consumer.sh", "Консольный консьюмер."), ("--from-beginning", "С офсета 0.")],
    mistake="Без флага увидишь только новые сообщения."),

f"{P}-consumers-e7": x(idea="`--describe --group` показывает CURRENT-OFFSET, LOG-END-OFFSET и LAG по партициям.",
    lines=[("kafka-consumer-groups.sh", "Утилита групп."), ("--describe --group billing", "Описание группы.")],
    mistake="`--list` — только имена групп."),

f"{P}-consumers-e8": x(idea="`--reset-offsets --to-earliest` перематывает группу на начало, `--execute` применяет.",
    lines=[("--group billing --topic orders", "Кого и где."), ("--reset-offsets --to-earliest", "Куда."), ("--execute", "Применить.")],
    mistake="Без `--execute` команда только покажет план, ничего не изменив."),

f"{P}-reliability-e1": x(
    idea="Коммит до обработки теряет сообщение при сбое, коммит после — обработает его повторно.",
    trace=[('print("коммит до обработки" if mode else "коммит после обработки", "| обработано:", done, "| после перезапуска читаем с офсета", committed)', "коммит до: офсет 4 уже сохранён, m3 не обработан", "коммит до обработки | обработано: ['m0', 'm1', 'm2'] | после перезапуска читаем с офсета 4"),
           ('print("коммит до обработки" if mode else "коммит после обработки", "| обработано:", done, "| после перезапуска читаем с офсета", committed)', "коммит после: сохранён офсет 3", "коммит после обработки | обработано: ['m0', 'm1', 'm2'] | после перезапуска читаем с офсета 3")],
    mistake="Не видеть, что офсет 4 значит «m3 уже обработан» — хотя это не так."),

f"{P}-reliability-e2": x(
    idea="acks=all требует min.insync.replicas живых копий; acks 0 и 1 — только живого лидера.",
    lines=[('if acks == "all":\n        return isr >= min_isr', "Мало копий — отказ."), ("return isr >= 1", "Лидер жив.")],
    mistake="Считать, что acks=all пишет всегда — при нехватке ISR запись отклоняется."),

f"{P}-reliability-e3": x(
    idea="Для каждого ключа запоминаем позицию и значение последней записи, потом сортируем по позиции.",
    lines=[("last[key] = (i, value)", "Поздняя запись перекрывает раннюю."),
           ("return [(key, value) for key, (i, value) in sorted(last.items(), key=lambda kv: kv[1][0])]", "Порядок — по последней записи.")],
    mistake="Оставлять первое значение ключа — compaction хранит последнее."),

f"{P}-reliability-e4": x(
    idea="Идемпотентный обработчик помнит id обработанных событий и пропускает повторы.",
    lines=[("self.seen = set()", "Своя память у каждого экземпляра."),
           ('if event["id"] in self.seen:\n            return False', "Дубль."),
           ("self.seen.add(event[\"id\"])\n        self.done.append(event)", "Новое событие.")],
    mistake="`seen = set()` на уровне класса — память станет общей для всех обработчиков."),

f"{P}-reliability-e5": x(
    idea="Идемпотентный продюсер нумерует сообщения, и брокер отбрасывает повтор с тем же номером.",
    trace=[("print(broker_log(False))", "повтор записан", "['заказ 1', 'заказ 2', 'заказ 2', 'заказ 3']"),
           ("print(broker_log(True))", "повтор номера 2 отброшен", "['заказ 1', 'заказ 2', 'заказ 3']")],
    mistake="Думать, что дубли появляются только у консьюмера — продюсер тоже их создаёт при повторах."),

f"{P}-reliability-e6": x(idea="`--replication-factor 3` — три копии каждой партиции на разных брокерах.",
    lines=[("--partitions 3 --replication-factor 3", "Партиции и копии.")],
    mistake="Ставить replication factor больше числа брокеров — Kafka откажет."),

f"{P}-reliability-e7": x(idea="`acks=all` (или -1) ждёт записи на всех синхронных репликах.", lines=[("all", "Самый надёжный.")],
    mistake="`acks=1` — подтверждение лидера, без гарантии копий."),

f"{P}-reliability-e8": x(idea="Обработка, потом коммит — at-least-once: потерь нет, но возможны дубли.", lines=[("at-least-once", "Хотя бы один раз.")],
    mistake="Путать с exactly-once — тот требует идемпотентности и транзакций."),

# ===== Модуль 2. Kafka из Python =====

f"{P}-producer-e1": x(
    idea="produce кладёт в буфер; колбэки доставки срабатывают во время flush().",
    trace=[
        ('print("до flush в буфере:", len(producer))', "три сообщения ждут отправки", "до flush в буфере: 3"),
        ('print(msg.key().decode(), "→ P", msg.partition(), "offset", msg.offset())', "колбэк: user-1 в P2", "user-1 → P 2 offset 0"),
        ('print(msg.key().decode(), "→ P", msg.partition(), "offset", msg.offset())', "user-2 в P1", "user-2 → P 1 offset 0"),
        ('print(msg.key().decode(), "→ P", msg.partition(), "offset", msg.offset())', "user-1 снова в P2 — следующий офсет", "user-1 → P 2 offset 1"),
        ('print("после flush:", len(producer))', "буфер пуст", "после flush: 0"),
    ],
    mistake="Ожидать вывода колбэков сразу после produce — они приходят при flush/poll."),

f"{P}-producer-e2": x(
    idea="Ключ — пользователь (порядок его заказов), значение — JSON заказа; в конце flush.",
    lines=[('producer.produce("orders", key=order["user"], value=json.dumps(order, ensure_ascii=False))', "Ключ и JSON."),
           ("producer.flush()", "Дождаться отправки.")],
    mistake="Передать словарь в value — Kafka принимает только строки и байты."),

f"{P}-producer-e3": x(
    idea="Офсеты приходят в колбэк; при ошибке вместо офсета — None.",
    lines=[("offsets.append(None if err is not None else msg.offset())", "Ошибка или офсет."),
           ("producer.produce(topic, value=value, on_delivery=on_delivery)", "Колбэк на каждое сообщение."),
           ("producer.flush()", "Колбэки срабатывают здесь.")],
    mistake="Вернуть список до flush — он будет пустым."),

f"{P}-producer-e4": x(
    idea="Адрес — из окружения со значением по умолчанию; надёжность — acks=all и идемпотентность.",
    lines=[('"bootstrap.servers": env.get("KAFKA_BOOTSTRAP", "localhost:9092"),', "Стенд меняется переменной."),
           ('"acks": "all",', "Все ISR."), ('"enable.idempotence": True,', "Без дублей при повторах.")],
    mistake="Захардкодить адрес стенда — тесты не запустятся в CI."),

f"{P}-producer-e5": x(
    idea="Пока продюсер не сделал flush, сообщения нет в Kafka — консьюмер его не видит.",
    trace=[('print("до flush:", consumer.poll(1.0))', "сообщение ещё в буфере продюсера", "до flush: None"),
           ('print("после flush:", msg.value().decode())', "после flush — в топике", "после flush: привет")],
    mistake="Искать баг в консьюмере, когда продюсер просто не сделал flush."),

f"{P}-producer-e6": x(
    idea="Отсутствие топика при выключенном авто-создании — исключение KafkaException; ловим и возвращаем False.",
    lines=[("try:\n        producer.produce(topic, value=value)\n        producer.flush()", "Отправка."),
           ("except KafkaException:\n        return False", "Не роняем тест.")],
    mistake="Ловить голый `except:` — спрячет и опечатки в коде."),

f"{P}-producer-e7": x(idea="Python-клиент от Confluent ставится пакетом confluent-kafka.", lines=[("pip install confluent-kafka", "Импорт потом — confluent_kafka.")],
    mistake="`pip install kafka` — это другая, устаревшая библиотека."),

f"{P}-producer-e8": x(idea="Консольный продюсер: каждая введённая строка — сообщение.",
    lines=[("kafka-console-producer.sh", "Утилита."), ("--bootstrap-server localhost:9092 --topic orders", "Куда писать.")],
    mistake="Ждать отправки по Enter без указания топика — утилита не запустится."),

f"{P}-consumer-e1": x(
    idea="poll отдаёт сообщения по одному, None — когда новых нет; close — в finally.",
    trace=[("print(msg.offset(), msg.value().decode())", "офсет 0", "0 заказ 0"),
           ("print(msg.offset(), msg.value().decode())", "офсет 1", "1 заказ 1"),
           ("print(msg.offset(), msg.value().decode())", "офсет 2", "2 заказ 2"),
           ('print("готово")', "poll вернул None — выход", "готово")],
    mistake="Читать в бесконечном цикле без выхода — тест повиснет."),

f"{P}-consumer-e2": x(
    idea="Ограничиваем число poll и выходим, как только набрали n значений.",
    lines=[("for _ in range(max_polls):", "Не больше max_polls попыток."),
           ("if msg is None or msg.error() is not None:\n            continue", "Пусто или ошибка — дальше."),
           ("if len(values) == n:\n                break", "Набрали — хватит.")],
    mistake="Цикл `while len(values) < n` — повиснет, если сообщений меньше n."),

f"{P}-consumer-e3": x(
    idea="Ищем конкретное сообщение по предикату, с лимитом попыток.",
    lines=[("if msg is not None and msg.error() is None and predicate(msg):\n            return msg", "Наше сообщение."),
           ("return None", "Не дождались.")],
    mistake="Проверять первое попавшееся сообщение — в топике могут быть чужие события."),

f"{P}-consumer-e4": x(
    idea="Коммит только после успешной обработки: исключение прерывает цикл до коммита.",
    lines=[("handler(msg.value().decode())", "Может бросить исключение."),
           ("consumer.commit(message=msg)", "Сюда дойдём, только если обработка прошла.")],
    mistake="Коммитить в начале цикла — упавшее сообщение будет потеряно."),

f"{P}-consumer-e5": x(
    idea="Каждая группа читает всё; повторный запуск той же группы продолжает с закоммиченного офсета.",
    trace=[('print("billing:", count("billing"), "| analytics:", count("analytics"), "| billing снова:", count("billing"))',
            "billing 3, analytics 3, billing уже всё прочитал", "billing: 3 | analytics: 3 | billing снова: 0")],
    mistake="Ждать, что analytics получит 0, потому что billing «забрал» сообщения."),

f"{P}-consumer-e6": x(
    idea="Откуда читать — earliest или latest; автокоммит выключен, коммитим сами.",
    lines=[('"auto.offset.reset": "earliest" if from_beginning else "latest",', "Начальная точка."),
           ('"enable.auto.commit": False,', "Ручной коммит.")],
    mistake="Оставить автокоммит в тестах обработки — офсет сдвинется до проверки."),

f"{P}-consumer-e7": x(
    idea="После перезапуска группа читает с закоммиченного офсета: m1 прочитали, но не закоммитили — прочитаем снова.",
    trace=[("c.commit(message=first)", "закоммичен офсет 1 (m0 обработан)", ""),
           ("print([m.value().decode() for m in iter(lambda: c.poll(1.0), None)])", "с офсета 1", "['m1', 'm2', 'm3']")],
    mistake="Думать, что m1 потерян: без коммита его просто прочитают ещё раз."),

f"{P}-consumer-e8": x(idea="close() — покинуть группу и (при автокоммите) сохранить офсеты.", lines=[("consumer.close()", "В finally.")],
    mistake="Не закрывать — группа ждёт «мёртвого» консьюмера до таймаута сессии."),

f"{P}-json-e1": x(
    idea="ensure_ascii=False оставляет кириллицу байтами UTF-8 — короче, чем \\u-последовательности.",
    trace=[("print(len(a), len(b))", "\\u0410\\u043d\\u044f против «Аня» в UTF-8", "47 35"),
           ("print(json.loads(b) == event, type(b).__name__)", "", "True bytes")],
    mistake="Считать, что ensure_ascii меняет данные — меняется только запись кириллицы."),

f"{P}-json-e2": x(
    idea="JSON с сортировкой ключей и кириллицей как есть, затем — в байты UTF-8.",
    lines=[('return json.dumps(event, ensure_ascii=False, sort_keys=True).encode("utf-8")', "Строка → байты.")],
    mistake="Вернуть строку — проверка ждёт байты."),

f"{P}-json-e3": x(
    idea="Битый JSON или не-объект — None, а не падение консьюмера.",
    lines=[("except (ValueError, TypeError):\n        return None", "Мусор или None."),
           ("return data if isinstance(data, dict) else None", "Только объект.")],
    mistake="Ловить только ValueError — json.loads(None) бросает TypeError."),

f"{P}-json-e4": x(
    idea="Проверяем поля по очереди и копим ошибки, а не падаем на первой.",
    lines=[("if not isinstance(order_id, int) or isinstance(order_id, bool):", "bool — подкласс int."),
           ("if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:", "Число больше нуля."),
           ('if "password" in event:', "Лишнее поле.")],
    mistake="`isinstance(True, int)` — True; без отдельной проверки bool пропустит True как номер заказа."),

f"{P}-json-e5": x(
    idea="Заголовки — список пар с байтами; превращаем в словарь строк.",
    lines=[('return {name: value.decode("utf-8") for name, value in headers or []}', "None → пустой список.")],
    mistake="Не учесть None — у сообщения без заголовков headers() возвращает None."),

f"{P}-json-e6": x(
    idea="Заголовки едут вместе с сообщением и читаются как список пар (имя, байты).",
    trace=[('print(headers["event-type"].decode(), headers["trace-id"].decode())', "dict из пар", "OrderCreated req-42")],
    mistake="Искать trace-id в значении — служебное кладут в заголовки."),

f"{P}-json-e7": x(
    idea="Ломают совместимость удалённые поля и новые обязательные; новое необязательное — безопасно.",
    lines=[('problems = [f"удалено: {f}" for f in old if f not in new]', "Удалённые."),
           ('problems += [f"новое обязательное: {f}" for f, required in new.items() if f not in old and required]', "Новые обязательные."),
           ("return sorted(problems)", "По алфавиту.")],
    mistake="Считать проблемой любое новое поле."),

f"{P}-json-e8": x(idea="Schema Registry хранит схемы сообщений и проверяет совместимость изменений.", lines=[("Schema Registry", "Реестр схем.")],
    mistake="Путать с Kafka Connect — тот переносит данные между системами."),

f"{P}-cli-e1": x(
    idea="Строки вывода делим по пробелам; партиция — 3-я колонка, lag — 6-я.",
    trace=[("lags = {int(r[2]): int(r[5]) for r in rows}", "{0: 0, 1: 32, 2: 1}", ""),
           ("print(lags, sum(lags.values()))", "", "{0: 0, 1: 32, 2: 1} 33"),
           ('print("отстаёт больше всего: партиция", max(lags, key=lags.get))', "максимум lag у P1", "отстаёт больше всего: партиция 1")],
    mistake="Брать первую строку как данные — это заголовок."),

f"{P}-cli-e2": x(
    idea="Номера колонок берём из заголовка; «-» в LAG — коммита нет, весь журнал не прочитан.",
    lines=[('part, lag, end = head.index("PARTITION"), head.index("LAG"), head.index("LOG-END-OFFSET")', "Колонки по заголовку."),
           ('result[int(row[part])] = int(row[end]) if row[lag] == "-" else int(row[lag])', "«-» → конец журнала.")],
    mistake="Захардкодить номера колонок — в другой версии Kafka порядок иной."),

f"{P}-cli-e3": x(
    idea="Проверяем список топиков; создаём только недостающий и ждём результат.",
    lines=[("if name in admin.list_topics().topics:\n        return False", "Уже есть."),
           ("futures[name].result()", "Дождаться и увидеть ошибку, если будет.")],
    mistake="Не вызвать result() — ошибка создания останется незамеченной."),

f"{P}-cli-e4": x(idea="`--list` — имена всех топиков.", lines=[("kafka-topics.sh --list", "Список.")],
    mistake="`--describe` без топика выведет описание всех топиков — долго."),

f"{P}-cli-e5": x(idea="`--property print.key=true` показывает ключи рядом со значениями.",
    lines=[("--from-beginning", "С начала."), ("--property print.key=true", "Ключи.")],
    mistake="Без него не видно, по какому ключу ушло сообщение."),

f"{P}-cli-e6": x(idea="kcat: -C читать, -o beginning с начала, -e выйти в конце.",
    lines=[("kcat -b localhost:9092 -t orders", "Брокер и топик."), ("-C -o beginning -e", "Чтение с начала до конца.")],
    mistake="Без -e kcat будет ждать новые сообщения бесконечно."),

f"{P}-cli-e7": x(
    idea="Lag партиции = конец журнала (high watermark) − закоммиченный офсет группы.",
    lines=[("low, high = consumer.get_watermark_offsets(TopicPartition(topic, p))", "Начало и конец."),
           ("committed = consumer.committed([TopicPartition(topic, p)])[0].offset", "Офсет группы."),
           ("result[p] = high - max(committed, 0)", "Нет коммита (−1001) → 0.")],
    mistake="Вычесть отрицательный «нет коммита» — lag окажется больше журнала."),

f"{P}-cli-e8": x(
    idea="create_topics возвращает future; ошибка проявится в .result() исключением.",
    trace=[("print(sorted(admin.list_topics().topics))", "топик создан", "['test-orders']"),
           ('print("ошибка:", e.args[0].str())', "второй раз — уже существует", "ошибка: Topic 'test-orders' already exists.")],
    mistake="Думать, что create_topics сам бросит исключение — без result() ошибка пройдёт тихо."),

# ===== Модуль 3. Тестирование Kafka =====

f"{P}-test-delivery-e1": x(
    idea="Действие → прочитать топик → ровно одно событие → сравнить JSON целиком.",
    lines=[('OrderService().place(501, "anna", 990)', "Действие."),
           ('msgs = read_all("orders")', "Своя группа, с начала."),
           ("assert len(msgs) == 1", "Одно событие."),
           ('assert json.loads(msgs[0].value()) == {"order_id": 501, "user": "anna", "amount": 990, "status": "created"}', "Целиком: ловит и статус, и тип суммы.")],
    mistake="Проверять только наличие сообщения — неверный статус или сумма строкой пройдут."),

f"{P}-test-delivery-e2": x(
    idea="Ключ — байты; сравниваем с b\"bob\".",
    lines=[('assert msgs[0].key() == b"bob"', "Ключ определяет партицию и порядок.")],
    mistake="Сравнивать со строкой \"bob\" — байты не равны строке."),

f"{P}-test-delivery-e3": x(
    idea="Ждём событие конкретного заказа, пропуская пустые, ошибочные и битые сообщения.",
    lines=[("if msg is None or msg.error() is not None:\n            continue", "Пусто или ошибка."),
           ("except ValueError:\n                continue", "Битый JSON — дальше."),
           ('if data.get("order_id") == order_id:\n                return data', "Наше событие.")],
    mistake="Падать на чужом битом сообщении — тест упадёт не из-за своего сервиса."),

f"{P}-test-delivery-e4": x(
    idea="Фикстура создаёт консьюмер, отдаёт через yield и закрывает после теста.",
    lines=[('c = Consumer({**CONF, "group.id": f"test-{uuid.uuid4().hex[:8]}", "auto.offset.reset": "earliest"})', "Уникальная группа, с начала."),
           ("yield c", "Тест получает консьюмер."),
           ("c.close()", "Уборка — даже при падении теста.")],
    mistake="`return c` вместо `yield` — закрыть консьюмер будет негде."),

f"{P}-test-delivery-e5": x(
    idea="Отправили 6 заказов — должны найти все 6 id.",
    lines=[('for i in range(1, 7):\n        OrderService().place(i, "anna", 100)', "Номера 1–6."),
           ('ids = sorted(json.loads(m.value())["order_id"] for m in read_all("orders"))', "Все id из топика."),
           ("assert ids == [1, 2, 3, 4, 5, 6]", "Ничего не потеряно.")],
    mistake="Проверить один заказ — теряется каждый третий, первый дойдёт."),

f"{P}-test-delivery-e6": x(
    idea="Группа помнит офсет: второй «тест» той же группой не видит старых сообщений.",
    trace=[('print("тест 1:", read("autotests"))', "группа прочитала заказ 1", "тест 1: 1"),
           ('print("тест 2:", read("autotests"))', "только новый заказ 2", "тест 2: 1"),
           ('print("тест 2 со своей группой:", read("autotests-2"))', "новая группа — всё с начала", "тест 2 со своей группой: 2")],
    mistake="Общая группа на все тесты — тест зависит от того, что читали до него."),

f"{P}-test-delivery-e7": x(idea="Префикс + 8 случайных шестнадцатеричных символов — новое имя на каждый вызов.",
    lines=[('return f"{prefix}-{uuid.uuid4().hex[:8]}"', "uuid4 — случайный.")],
    mistake="Брать время в секундах — два теста в одну секунду получат одну группу."),

f"{P}-test-delivery-e8": x(idea="earliest — читать с начала, иначе сообщение, отправленное до консьюмера, не увидишь.",
    lines=[("earliest", "auto.offset.reset=earliest.")], mistake="latest (по умолчанию) — только новые сообщения."),

f"{P}-test-order-e1": x(
    idea="Нет дублей — длина списка id равна длине множества.",
    lines=[('ids = [json.loads(m.value())["order_id"] for m in read_all("orders")]', "Все id."),
           ("assert len(ids) == len(set(ids))", "Повторов нет.")],
    mistake="Проверять только наличие каждого заказа — дубль пройдёт."),

f"{P}-test-order-e2": x(
    idea="Заказ → обработка → в payments ровно один платёж с нужным order_id.",
    lines=[("BillingWorker().run_once()", "Обработка."),
           ('payments = read_all("payments")', "Платежи."),
           ("assert len(payments) == 1", "Без двойного платежа.")],
    mistake="Проверять «платёж есть» (`>= 1`) — двойной платёж пройдёт."),

f"{P}-test-order-e3": x(
    idea="Все события пользователя — в одной партиции, иначе порядок не гарантирован.",
    lines=[("assert len({m.partition() for m in msgs}) == 1", "Одна партиция.")],
    mistake="Проверять видимый порядок — на стенде он может совпасть случайно."),

f"{P}-test-order-e4": x(idea="Counter считает вхождения; берём id с количеством больше одного.",
    lines=[("return sorted(i for i, n in Counter(ids).items() if n > 1)", "Только повторы.")],
    mistake="`list.count` в цикле — медленно и с повторами в ответе."),

f"{P}-test-order-e5": x(idea="Оставляем первый платёж каждого заказа, сохраняя порядок.",
    lines=[('if p["order_id"] not in seen:', "Ещё не встречали."), ("result.append(p)", "Первый — оставляем.")],
    mistake="Словарь `{order_id: p}` оставит последний платёж, а не первый."),

f"{P}-test-order-e6": x(
    idea="Без коммита перезапущенный биллинг обрабатывает всё заново — платежи удваиваются.",
    trace=[('print("платежей:", n, "| заказов: 2 | ожидалось по одному на группу: 4")', "исправная группа — 2, без коммитов — 4", "платежей: 6 | заказов: 2 | ожидалось по одному на группу: 4")],
    mistake="Думать, что перезапуск безопасен всегда — без коммита это повторная обработка."),

f"{P}-test-order-e7": x(
    idea="Имитируем перезапуск: close и новый экземпляр той же группы. Платёж должен остаться один.",
    lines=[("worker.close()", "Первый экземпляр остановлен."),
           ("BillingWorker().run_once()", "Перезапуск — с закоммиченного офсета."),
           ('assert len(read_all("payments")) == 1', "Без повторного платежа.")],
    mistake="Перезапуск с другой группой — она прочитает всё с начала и даст ложный дубль."),

f"{P}-test-order-e8": x(idea="Exactly-once — ровно один раз: идемпотентный продюсер и транзакции.", lines=[("exactly-once", "Ровно один раз.")],
    mistake="Считать, что exactly-once защищает внешние действия (письма, платежи) — их всё равно делают идемпотентными."),

f"{P}-test-errors-e1": x(
    idea="Битое сообщение не роняет консьюмер, а уходит в DLQ с причиной.",
    lines=[('p.produce("orders", key="anna", value="не json")', "Битое сообщение напрямую."),
           ("BillingWorker().run_once()", "Не должен упасть."),
           ('assert "error" in dict(dlq[0].headers())', "Причина в заголовке.")],
    mistake="Оборачивать run_once в try/except в тесте — так тест не заметит, что консьюмер падает."),

f"{P}-test-errors-e2": x(
    idea="Сбой посреди обработки → перезапуск → заказ всё равно оплачен.",
    lines=[("try:\n        worker.run_once()\n    except RuntimeError:\n        pass", "Сбой допускаем."),
           ("BillingWorker().run_once()", "Перезапуск."),
           ("assert 1 in paid", "Заказ не потерян.")],
    mistake="Не делать перезапуск — тогда не проверить, что сообщение осталось непрочитанным."),

f"{P}-test-errors-e3": x(
    idea="Проверки по порядку: разбор JSON, наличие order_id, сумма больше нуля.",
    lines=[('except ValueError:\n        return "dlq", "не JSON"', "Мусор."),
           ('if not data.get("amount", 0) > 0:\n        return "dlq", "amount <= 0"', "Нет суммы — как ноль.")],
    mistake="`data[\"amount\"] > 0` упадёт KeyError, если суммы нет."),

f"{P}-test-errors-e4": x(
    idea="Повторяем до успеха; на последней неудачной попытке пробрасываем исключение.",
    lines=[("return func()", "Успех — сразу результат."),
           ("if i == attempts - 1:\n                raise", "Последнее исключение — наружу.")],
    mistake="Глотать все исключения и вернуть None — ошибка станет невидимой."),

f"{P}-test-errors-e5": x(
    idea="Валидный заказ обработан, отрицательная сумма и мусор ушли в DLQ с причинами.",
    trace=[('print("обработано:", BillingWorker().run_once())', "только заказ 1", "обработано: 1"),
           ('print(m.key().decode(), "→", dict(m.headers())["error"].decode()[:30])', "eve: не JSON (её партицию прочитали раньше)", "eve → Expecting value: line 1 column"),
           ('print(m.key().decode(), "→", dict(m.headers())["error"].decode()[:30])', "bob: сумма -5", "bob → amount должен быть положительн")],
    mistake="Ожидать, что биллинг упадёт на первом же битом сообщении."),

f"{P}-test-errors-e6": x(
    idea="Сравниваем платежи с ожидаемым списком целиком: и наличие, и поля.",
    lines=[('payments = [json.loads(m.value()) for m in read_all("payments")]', "Все платежи."),
           ('assert payments == [{"order_id": 8, "amount": 990, "status": "paid"}]', "Ровно этот.")],
    mistake="Проверять только статус — пропустишь, что платежа нет вовсе."),

f"{P}-test-errors-e7": x(idea="Причину берём из заголовка error, нет — «неизвестно»; считаем.",
    lines=[("h = dict(headers)", "Пары → словарь."), ('reason = h["error"].decode() if "error" in h else "неизвестно"', "Причина."),
           ("report[reason] = report.get(reason, 0) + 1", "Счётчик.")],
    mistake="Забыть decode — ключами станут байты."),

f"{P}-test-errors-e8": x(idea="DLQ — обычный топик, читается тем же консольным консьюмером.",
    lines=[("--topic orders.dlq --from-beginning", "Всё, что накопилось.")], mistake="Искать DLQ в логах — это отдельный топик."),

f"{P}-test-env-e1": x(idea="Сервис kafka из официального образа, порт 9092 наружу.",
    lines=[("image: apache/kafka:3.8.0", "Одиночный брокер KRaft."), ('- "9092:9092"', "Хост:контейнер.")],
    mistake="Порт без кавычек вида 22:22 YAML может прочитать как число — в кавычках надёжнее."),

f"{P}-test-env-e2": x(idea="Нижний регистр, запрещённые символы → «-», префикс и обрезка до 60.",
    lines=[('return ("test-" + re.sub(r"[^a-z0-9._-]", "-", test_name.lower()))[:60]', "Всё в одной строке.")],
    mistake="Обрезать до добавления префикса — итог превысит лимит."),

f"{P}-test-env-e3": x(
    idea="Свой топик на тест: создать до, удалить после.",
    lines=[("admin.create_topics([NewTopic(name, num_partitions=1, replication_factor=1)])[name].result()", "Создать и дождаться."),
           ("yield name", "Тест получает имя."), ("admin.delete_topics([name])", "Уборка.")],
    mistake="Не удалять топики — кластер стенда зарастает тысячами test-*."),

f"{P}-test-env-e4": x(idea="Одиночная Kafka в фоне, порт наружу.",
    lines=[("docker run -d --name kafka", "Фон и имя."), ("-p 9092:9092 apache/kafka:3.8.0", "Порт и образ.")],
    mistake="Забыть -p — с хоста к брокеру не подключиться."),

f"{P}-test-env-e5": x(idea="`docker compose up -d kafka` — поднять только нужный сервис.", lines=[("docker compose up -d kafka", "Фон, один сервис.")],
    mistake="Без имени сервиса поднимется весь стенд."),

f"{P}-test-env-e6": x(
    idea="Kafka — сервис job-а; тестам адрес передаётся переменной окружения.",
    lines=[("services:\n      kafka:\n        image: apache/kafka:3.8.0", "Брокер рядом с job-ом."),
           ("- run: pytest\n        env:\n          KAFKA_BOOTSTRAP: localhost:9092", "Адрес для тестов.")],
    mistake="Писать адрес в коде тестов — локально и в CI он разный."),

f"{P}-test-env-e7": x(
    idea="Пробуем до успеха; исключение — тоже «не готова»; не дождались — TimeoutError.",
    lines=[("if check():\n                return attempt", "Готово — номер попытки."),
           ("except Exception:\n                pass", "Не подключились — ещё раз."),
           ('raise TimeoutError(f"Kafka не готова за {attempts} попыток")', "Понятная ошибка.")],
    mistake="Не ловить исключение check() — первая же неудача уронит ожидание."),

f"{P}-test-env-e8": x(idea="`--delete` удаляет топик.", lines=[("kafka-topics.sh --delete --topic test-orders", "Удалить.")],
    mistake="Удалять общий топик стенда — удаляют только свои временные test-*."),
}
