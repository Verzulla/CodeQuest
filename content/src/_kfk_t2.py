"""Теория модуля «Kafka из Python» темы «Kafka для тестировщика».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

SANDBOX = "В заданиях Kafka — **учебная**, в памяти: импорт `from kafkafake import Producer, Consumer` вместо `from confluent_kafka import …`. Остальной код тот же. Учебная `poll()` не ждёт: нет сообщений — сразу `None`."

T = {

# ---------- kfk-producer ----------
'kfk-producer': dict(
    full=t(r'''
## Зачем это нужно

В автотестах продюсер нужен постоянно: положить в топик тестовое событие и проверить, что сервис его обработал, или подготовить данные. Самая популярная библиотека для Python — **confluent-kafka**.

```bash
pip install confluent-kafka
```

''' + SANDBOX + r'''

## Создать продюсер и отправить сообщение

```py
from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "localhost:9092"})
producer.produce("orders", key="user-1", value='{"order_id": 501}')
producer.flush()
```

- Настройки — словарь с ключами как у Kafka: `bootstrap.servers` — адрес брокера (можно несколько через запятую).
- `produce(topic, key=…, value=…)` **не отправляет сразу**, а кладёт сообщение в буфер внутри продюсера. Так быстрее: сообщения уходят пачками.
- `flush()` — дождаться, пока весь буфер уйдёт в Kafka. В тестах и скриптах вызывай его обязательно, иначе программа закончится раньше, чем сообщения уйдут.
- `len(producer)` — сколько сообщений ещё в буфере.

## Колбэк доставки: узнать, дошло ли

```py
def on_delivery(err, msg):
    if err is not None:
        print("не доставлено:", err)
    else:
        print("доставлено:", msg.topic(), msg.partition(), msg.offset())

producer.produce("orders", key="user-1", value="...", on_delivery=on_delivery)
producer.flush()
```

- Колбэк вызывается, когда брокер подтвердил запись (или вернул ошибку). Вызывает его `flush()` или `poll()`.
- В подтверждении — партиция и офсет: так тест узнаёт, куда именно легло сообщение.

## Настройки надёжности

```py
producer = Producer({
    "bootstrap.servers": "localhost:9092",
    "acks": "all",                 # ждать записи на всех синхронных репликах
    "enable.idempotence": True,    # не создавать дубли при повторах
    "client.id": "autotests",      # имя клиента в логах брокера
})
```

## Ошибки

- Нет брокера или неверный адрес — сообщения копятся в буфере, колбэк получит ошибку по таймауту.
- Топика нет, а авто-создание выключено — ошибка доставки «unknown topic or partition».
- Неверная настройка — исключение `KafkaException` уже при создании продюсера.

## Итог

- `Producer({"bootstrap.servers": …})` → `produce(topic, key, value)` → `flush()`.
- `produce` кладёт в буфер; `flush` дожидается отправки.
- Колбэк `on_delivery(err, msg)` — подтверждение с партицией и офсетом.
- Надёжность: `acks=all`, `enable.idempotence=True`.
'''),
    short=t(r'''
```py
from confluent_kafka import Producer          # в песочнице: from kafkafake import Producer

producer = Producer({"bootstrap.servers": "localhost:9092", "acks": "all", "enable.idempotence": True})

def on_delivery(err, msg):
    print(err or (msg.partition(), msg.offset()))

producer.produce("orders", key="user-1", value='{"order_id": 501}', on_delivery=on_delivery)
producer.flush()                               # дождаться отправки
```
'''),
    quiz=[
        q('Скрипт вызвал `produce()` и сразу завершился. Почему сообщения иногда не доходят?',
            ['Kafka их отбросила', 'produce кладёт в буфер — без flush() программа закончилась раньше отправки', 'Нужен ключ', 'Не создан консьюмер'],
            1, 'В конце всегда flush().'),
        q('Где тест узнаёт партицию и офсет отправленного сообщения?',
            ['В возвращаемом значении produce()', 'В колбэке доставки', 'В len(producer)', 'Нигде'],
            1, 'on_delivery(err, msg): msg.partition(), msg.offset().'),
        q('Что такое bootstrap.servers?',
            ['Список топиков', 'Адрес брокеров Kafka для подключения', 'Имя группы', 'Таймаут'],
            1, 'Обычно host:port одного или нескольких брокеров.'),
    ],
),

# ---------- kfk-consumer ----------
'kfk-consumer': dict(
    full=t(r'''
## Зачем это нужно

Консьюмер в тесте — главный инструмент проверки: «после запроса к API в топике `payments` появилось событие с нужными полями». Важно читать правильно: с нужного места, с таймаутом и без зависаний.

''' + SANDBOX + r'''

## Цикл чтения

```py
from confluent_kafka import Consumer

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "autotests",
    "auto.offset.reset": "earliest",
})
consumer.subscribe(["orders"])
try:
    while True:
        msg = consumer.poll(1.0)          # ждать до 1 секунды
        if msg is None:
            break                          # за секунду ничего не пришло
        if msg.error():
            print("ошибка:", msg.error())
            continue
        print(msg.key(), msg.value().decode(), msg.offset())
finally:
    consumer.close()
```

- `group.id` обязателен: консьюмер всегда в какой-то группе.
- `poll(timeout)` возвращает **одно** сообщение или `None`, если за `timeout` секунд ничего не пришло.
- У сообщения бывает ошибка — проверяй `msg.error()` прежде, чем читать значение.
- `key()` и `value()` — **байты**; строку получают через `.decode()`.
- `close()` — в `finally`: консьюмер покидает группу (сразу начинается ребаланс), а при автокоммите сохраняет офсеты.

## Ручной коммит

```py
consumer = Consumer({..., "enable.auto.commit": False})
...
msg = consumer.poll(1.0)
process(msg)
consumer.commit(message=msg)    # «это сообщение обработано»
```

Сначала обработка, потом коммит — at-least-once: сбой между ними даст повтор, а не потерю.

## Ожидание нужного сообщения

В тестах обычно ждут не «что-нибудь», а **конкретное** событие, и не бесконечно:

```py
def wait_for(consumer, predicate, attempts=20):
    for _ in range(attempts):
        msg = consumer.poll(0.5)
        if msg is not None and not msg.error() and predicate(msg):
            return msg
    return None
```

- Ограниченное число попыток — тест упадёт понятно, а не зависнет.
- Предикат отбирает «своё» сообщение, например по `order_id`.

## Итог

- `Consumer({bootstrap.servers, group.id, auto.offset.reset})` → `subscribe([…])` → цикл `poll()` → `close()` в `finally`.
- `poll` отдаёт одно сообщение или `None`; проверяй `msg.error()`; значения — байты.
- Ручной коммит: `enable.auto.commit=False` и `commit(message=msg)` после обработки.
- В тестах — ожидание конкретного сообщения с лимитом попыток.
'''),
    short=t(r'''
```py
from confluent_kafka import Consumer           # в песочнице: from kafkafake import Consumer

c = Consumer({"bootstrap.servers": "localhost:9092", "group.id": "autotests",
              "auto.offset.reset": "earliest", "enable.auto.commit": False})
c.subscribe(["orders"])
try:
    while (msg := c.poll(1.0)) is not None:
        if msg.error():
            continue
        handle(msg.value().decode())
        c.commit(message=msg)                  # после обработки
finally:
    c.close()
```
'''),
    quiz=[
        q('Что возвращает `poll(1.0)`, если за секунду сообщений не было?',
            ['Пустой список', 'None', 'Исключение', 'Последнее сообщение повторно'],
            1, 'Поэтому цикл проверяет `msg is None`.'),
        q('Зачем `close()` в `finally`?',
            ['Чтобы удалить топик', 'Чтобы консьюмер покинул группу и сохранил офсеты даже при ошибке', 'Чтобы очистить сообщения', 'Не нужен'],
            1, 'Иначе группа ждёт «потерянного» консьюмера до таймаута.'),
        q('Какого типа `msg.value()`?',
            ['str', 'bytes', 'dict', 'int'],
            1, 'Строку получают через `.decode()`, JSON — через `json.loads`.'),
    ],
),

# ---------- kfk-json ----------
'kfk-json': dict(
    full=t(r'''
## Зачем это нужно

Kafka передаёт просто **байты** — ей всё равно, что внутри. Договорённость о формате (обычно JSON) живёт между сервисами. Половина багов на интеграциях — в формате: поле переименовали, тип поменялся, кодировка поломалась. Это и проверяют тесты.

## JSON туда и обратно

```python
import json

event = {"order_id": 501, "user": "Аня", "amount": 990.0}
raw = json.dumps(event, ensure_ascii=False).encode("utf-8")   # dict → строка → байты
back = json.loads(raw.decode("utf-8"))                         # байты → строка → dict
print(raw[:20], back == event)
```

- Отправляем байты: `json.dumps(…)` даёт строку, `.encode("utf-8")` — байты. confluent-kafka принимает и строку — закодирует сам.
- `ensure_ascii=False` оставляет кириллицу читаемой, без `А…`.
- `json.loads` умеет и байты, но явное `decode` понятнее.

## Защита от битых сообщений

```python
def decode(raw):
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return None
```

Битое сообщение (poison message) не должно ронять консьюмер: его откладывают отдельно (об этом — урок про DLQ).

## Контракт: что проверять в событии

- **Обязательные поля** на месте: `order_id`, `user`, `amount`.
- **Типы**: `order_id` — число, а не строка `"501"`; `amount` — число.
- **Значения**: статус из допустимого набора, сумма положительная.
- **Лишнее**: нет паролей и внутренних полей.

## Заголовки

Кроме ключа и значения у сообщения есть **заголовки** (headers) — пары «имя → байты». В них кладут служебное: id запроса для трассировки, тип события, версию схемы.

```py
producer.produce("orders", value=raw, headers=[("event-type", b"OrderCreated"), ("trace-id", b"a1b2")])
...
headers = dict(msg.headers() or [])          # [(имя, байты)] → словарь
print(headers["event-type"].decode())
```

## Схемы и Schema Registry

В больших системах формат описывают **схемой** (Avro, Protobuf или JSON Schema) и хранят в **Schema Registry** — отдельном сервисе. Продюсер не может отправить сообщение, не подходящее под схему, а изменения схемы проверяются на **совместимость**:

- добавить **необязательное** поле — безопасно, старые консьюмеры его проигнорируют;
- удалить поле или сделать новое **обязательным** — сломает тех, кто ещё работает по старой схеме.

## Итог

- В Kafka — байты; JSON: `json.dumps(…).encode()` и `json.loads(…)`.
- Битое сообщение не должно ронять консьюмер — `try/except`, затем отложить.
- Проверяем контракт: поля, типы, значения, отсутствие лишнего.
- Заголовки — служебные пары `(имя, байты)`; схемы и Schema Registry следят за совместимостью.
'''),
    short=t(r'''
```py
raw = json.dumps(event, ensure_ascii=False).encode("utf-8")   # отправка
data = json.loads(msg.value())                                  # чтение
headers = dict(msg.headers() or [])                              # [(имя, байты)] → dict
```

- Битое сообщение — `try/except ValueError` → в сторону (DLQ), не падать.
- Контракт: обязательные поля, типы, значения, ничего лишнего.
- Schema Registry: добавить необязательное поле — можно; удалить или сделать обязательным — ломает.
'''),
    quiz=[
        q('Что Kafka знает о формате значения сообщения?',
            ['Только JSON', 'Ничего — это байты, формат — договорённость сервисов', 'Только Avro', 'Формат задаёт топик'],
            1, 'Поэтому контракт и проверяют тестами.'),
        q('Какое изменение схемы события безопасно для старых консьюмеров?',
            ['Удалить поле', 'Добавить необязательное поле', 'Переименовать поле', 'Сделать поле обязательным'],
            1, 'Старые консьюмеры просто не используют новое поле.'),
        q('Зачем `ensure_ascii=False` в json.dumps?',
            ['Ускоряет отправку', 'Оставляет кириллицу читаемой, без \\u-последовательностей', 'Сжимает JSON', 'Включает проверку схемы'],
            1, 'Иначе «Аня» превратится в \\u0410\\u043d\\u044f.'),
    ],
),

# ---------- kfk-cli ----------
'kfk-cli': dict(
    full=t(r'''
## Зачем это нужно

Когда тест упал или «сообщения не доходят», первым делом смотрят в саму Kafka: есть ли топик, что в нём лежит, какой lag у группы. Для этого — консольные утилиты, `kcat` и `AdminClient` в Python.

## Консольные утилиты

```bash
kafka-topics.sh --list --bootstrap-server localhost:9092
kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning --property print.key=true
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group billing
```

- Консольный продюсер читает строки с клавиатуры: каждая строка — сообщение.
- `--property print.key=true` — показывать ключи, а не только значения.
- В Docker: `docker exec -it kafka /opt/kafka/bin/kafka-topics.sh …` (путь зависит от образа).

## kcat — универсальный инструмент

```bash
kcat -b localhost:9092 -L                              # метаданные: брокеры, топики, партиции
kcat -b localhost:9092 -t orders -C -o beginning -e    # прочитать всё и выйти
echo '{"order_id": 1}' | kcat -b localhost:9092 -t orders -P
```

- `-C` — читать (consumer), `-P` — писать (producer).
- `-o beginning` — с начала, `-e` — выйти, дочитав до конца.

## Как читать вывод --describe

```bash
GROUP    TOPIC   PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG  CONSUMER-ID
billing  orders  0          120             120             0    consumer-1
billing  orders  1          98              130             32   consumer-2
billing  orders  2          140             141             1    consumer-1
```

- `CURRENT-OFFSET` — закоммиченный офсет группы, `LOG-END-OFFSET` — конец журнала, `LAG` — разница.
- Пустой `CONSUMER-ID` — у партиции нет живого консьюмера: группа остановлена или упала.

## AdminClient: то же из Python

```py
from confluent_kafka.admin import AdminClient, NewTopic

admin = AdminClient({"bootstrap.servers": "localhost:9092"})
futures = admin.create_topics([NewTopic("test-orders", num_partitions=3, replication_factor=1)])
futures["test-orders"].result()          # дождаться; ошибка → исключение
print(list(admin.list_topics().topics))
```

- Методы AdminClient возвращают словарь «имя → future»; `.result()` ждёт выполнения и бросает исключение при ошибке, например «топик уже существует».
- Lag из кода считают через консьюмер: `get_watermark_offsets()` даёт начало и конец партиции, `committed()` — офсеты группы.

## Итог

- `kafka-topics` (`--list/--describe/--create`), `kafka-console-producer/consumer`, `kafka-consumer-groups --describe`.
- kcat: `-L` метаданные, `-C` чтение, `-P` запись, `-o beginning -e`.
- В `--describe`: CURRENT-OFFSET, LOG-END-OFFSET, LAG, CONSUMER-ID.
- AdminClient: `create_topics` → future → `.result()`; `list_topics().topics`.
'''),
    short=t(r'''
```bash
kafka-topics.sh --list --bootstrap-server localhost:9092
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning --property print.key=true
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group billing
kcat -b localhost:9092 -t orders -C -o beginning -e
```
```py
admin = AdminClient({"bootstrap.servers": "localhost:9092"})
admin.create_topics([NewTopic("t", num_partitions=3, replication_factor=1)])["t"].result()
```
'''),
    quiz=[
        q('В выводе `--describe` у партиции пустой CONSUMER-ID и растущий LAG. Что это значит?',
            ['Всё нормально', 'Партицию никто не читает — группа остановлена или упала', 'Партиция удалена', 'Это реплика'],
            1, 'Повод посмотреть логи консьюмера.'),
        q('Что делает `kcat -b localhost:9092 -t orders -C -o beginning -e`?',
            ['Пишет в топик', 'Читает топик с начала и выходит', 'Удаляет топик', 'Показывает группы'],
            1, '-C — чтение, -o beginning — с начала, -e — выйти в конце.'),
        q('Как узнать, что create_topics завершился с ошибкой?',
            ['Вернёт False', 'Вызвать .result() у future — будет исключение', 'Ничего не сообщит', 'Через len()'],
            1, 'Например, если топик уже существует.'),
    ],
),

}
