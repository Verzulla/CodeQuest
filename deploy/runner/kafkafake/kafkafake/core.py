"""Учебная Kafka в памяти процесса.

Повторяет основной API библиотеки confluent-kafka (Producer, Consumer, AdminClient), чтобы код
из уроков переносился на настоящую Kafka заменой одного импорта. Внутри — один «кластер» на процесс:
топики из партиций-журналов, группы консьюмеров с закоммиченными офсетами.

Упрощения относительно настоящей Kafka (о них сказано в уроках):
- партиция по ключу — crc32(key) % число_партиций (в Kafka — murmur2, правило то же: один ключ → одна партиция);
- poll() не ждёт: если сообщений нет, сразу возвращает None;
- автокоммит происходит при следующем poll() и при close(), а не по таймеру.
"""
import zlib
from itertools import count

_clock = count(1_700_000_000_000)  # «время» сообщений, мс — растёт на 1 с каждым сообщением


class KafkaError:
    """Ошибка доставки или чтения (как confluent_kafka.KafkaError)."""
    _PARTITION_EOF = -191
    UNKNOWN_TOPIC_OR_PART = 3
    INVALID_CONFIG = -186

    def __init__(self, code, reason=""):
        self._code, self._reason = code, reason

    def code(self):
        return self._code

    def str(self):
        return self._reason

    def __repr__(self):
        return f"KafkaError({self._code}, {self._reason!r})"


class KafkaException(Exception):
    """Исключение клиента (как confluent_kafka.KafkaException)."""


class TopicPartition:
    def __init__(self, topic, partition=-1, offset=-1001):
        self.topic, self.partition, self.offset = topic, partition, offset

    def __repr__(self):
        return f"TopicPartition({self.topic!r}, {self.partition}, {self.offset})"

    def __eq__(self, other):
        return isinstance(other, TopicPartition) and (self.topic, self.partition) == (other.topic, other.partition)

    def __hash__(self):
        return hash((self.topic, self.partition))


class Message:
    """Сообщение, как его отдаёт poll() и колбэк доставки."""

    def __init__(self, topic, partition, offset, key, value, headers=None, timestamp=None, error=None):
        self._t, self._p, self._o = topic, partition, offset
        self._k, self._v, self._h = key, value, headers
        self._ts = timestamp if timestamp is not None else next(_clock)
        self._e = error

    def topic(self):
        return self._t

    def partition(self):
        return self._p

    def offset(self):
        return self._o

    def key(self):
        return self._k

    def value(self):
        return self._v

    def headers(self):
        return self._h

    def timestamp(self):
        return (1, self._ts)   # (тип метки, мс)

    def error(self):
        return self._e

    def __repr__(self):
        return f"Message(topic={self._t!r}, partition={self._p}, offset={self._o}, key={self._k!r}, value={self._v!r})"


def _to_bytes(x):
    if x is None or isinstance(x, bytes):
        return x
    if isinstance(x, str):
        return x.encode("utf-8")
    raise TypeError(f"ключ и значение должны быть str или bytes, а не {type(x).__name__}")


class _Cluster:
    def __init__(self):
        self.reset()

    def reset(self, default_partitions=3):
        self.topics = {}          # имя → [журнал партиции 0, журнал 1, …]; журнал — список Message
        self.groups = {}          # group.id → {"members": [Consumer], "committed": {(topic, p): offset}}
        self.default_partitions = default_partitions
        self.auto_create = True
        self._rr = count()

    def topic(self, name, create=True):
        if name not in self.topics:
            if not (create and self.auto_create):
                return None
            self.topics[name] = [[] for _ in range(self.default_partitions)]
        return self.topics[name]

    def partition_for(self, topic, key):
        n = len(self.topic(topic))
        if key is None:
            return next(self._rr) % n          # без ключа — по кругу
        return zlib.crc32(key) % n

    def append(self, topic, partition, key, value, headers):
        log = self.topic(topic)[partition]
        msg = Message(topic, partition, len(log), key, value, headers)
        log.append(msg)
        return msg

    def group(self, gid):
        return self.groups.setdefault(gid, {"members": [], "committed": {}})

    def rebalance(self, gid):
        """Раздать партиции подписанных топиков консьюмерам группы (как range-стратегия)."""
        g = self.group(gid)
        members = [m for m in g["members"] if not m._closed]
        for m in members:
            m._assignment = []
        topics = sorted({t for m in members for t in m._topics})
        for t in topics:
            subs = [m for m in members if t in m._topics]
            parts = self.topic(t)
            for p in range(len(parts)):
                m = subs[p % len(subs)]
                m._assignment.append(TopicPartition(t, p))
        for m in members:
            m._positions = {tp: m._start_offset(tp) for tp in m._assignment}
            m._rebalances += 1


cluster = _Cluster()


def reset(default_partitions=3):
    """Очистить учебный кластер: все топики, сообщения и группы."""
    cluster.reset(default_partitions)


# ---------------------------------------------------------------- Producer

class Producer:
    """Отправка сообщений. Как в confluent-kafka: produce() кладёт в буфер, poll()/flush() доставляют."""

    def __init__(self, config=None):
        config = dict(config or {})
        if "bootstrap.servers" not in config:
            raise KafkaException("Не указан bootstrap.servers — адрес кластера Kafka")
        self.config = config
        self._queue = []

    def produce(self, topic, value=None, key=None, partition=-1, on_delivery=None, callback=None, headers=None, timestamp=0):
        key, value = _to_bytes(key), _to_bytes(value)
        if cluster.topic(topic) is None:
            raise KafkaException(KafkaError(KafkaError.UNKNOWN_TOPIC_OR_PART, f"Топика {topic} нет"))
        self._queue.append((topic, value, key, partition, on_delivery or callback, headers))

    def poll(self, timeout=None):
        return self._deliver()

    def flush(self, timeout=None):
        self._deliver()
        return 0

    def __len__(self):
        return len(self._queue)

    def _deliver(self):
        n = 0
        queue, self._queue = self._queue, []
        for topic, value, key, partition, cb, headers in queue:
            parts = cluster.topic(topic)
            if partition is None or partition < 0:
                partition = cluster.partition_for(topic, key)
            if partition >= len(parts):
                err = KafkaError(KafkaError.UNKNOWN_TOPIC_OR_PART, f"В топике {topic} нет партиции {partition}")
                if cb:
                    cb(err, Message(topic, partition, -1, key, value, headers, error=err))
                continue
            msg = cluster.append(topic, partition, key, value, headers)
            n += 1
            if cb:
                cb(None, msg)
        return n


# ---------------------------------------------------------------- Consumer

class Consumer:
    """Чтение сообщений в составе группы. poll() отдаёт по одному сообщению или None."""

    def __init__(self, config=None):
        config = dict(config or {})
        if "group.id" not in config:
            raise KafkaException("Не указан group.id — имя группы консьюмеров")
        if "bootstrap.servers" not in config:
            raise KafkaException("Не указан bootstrap.servers — адрес кластера Kafka")
        self.config = config
        self.group_id = config["group.id"]
        self.reset_policy = config.get("auto.offset.reset", "latest")
        self.auto_commit = str(config.get("enable.auto.commit", True)).lower() not in ("false", "0")
        self._topics = []
        self._assignment = []
        self._positions = {}
        self._pending = None       # что закоммитить автоматически при следующем poll
        self._closed = False
        self._rebalances = 0
        self._rr = 0

    def _start_offset(self, tp):
        committed = cluster.group(self.group_id)["committed"].get((tp.topic, tp.partition))
        if committed is not None:
            return committed
        log = cluster.topic(tp.topic)[tp.partition]
        return 0 if self.reset_policy in ("earliest", "smallest", "beginning") else len(log)

    def subscribe(self, topics, on_assign=None, on_revoke=None):
        self._check()
        self._topics = list(topics)
        for t in self._topics:
            cluster.topic(t)
        g = cluster.group(self.group_id)
        if self not in g["members"]:
            g["members"].append(self)
        cluster.rebalance(self.group_id)
        if on_assign:
            on_assign(self, list(self._assignment))

    def assignment(self):
        return list(self._assignment)

    def poll(self, timeout=None):
        self._check()
        if self.auto_commit and self._pending:
            self._commit_positions(self._pending)
            self._pending = None
        tps = self._assignment
        for i in range(len(tps)):
            tp = tps[(self._rr + i) % len(tps)]
            log = cluster.topic(tp.topic)[tp.partition]
            pos = self._positions.get(tp, 0)
            if pos < len(log):
                self._positions[tp] = pos + 1
                self._rr = (self._rr + i + 1) % len(tps)
                if self.auto_commit:
                    self._pending = dict(self._positions)
                return log[pos]
        return None

    def consume(self, num_messages=1, timeout=None):
        out = []
        for _ in range(num_messages):
            m = self.poll(timeout)
            if m is None:
                break
            out.append(m)
        return out

    def commit(self, message=None, offsets=None, asynchronous=True):
        self._check()
        if message is not None:
            self._commit_positions({TopicPartition(message.topic(), message.partition()): message.offset() + 1})
        elif offsets is not None:
            self._commit_positions({TopicPartition(tp.topic, tp.partition): tp.offset for tp in offsets})
        else:
            self._commit_positions(dict(self._positions))
        return None

    def _commit_positions(self, positions):
        committed = cluster.group(self.group_id)["committed"]
        for tp, off in positions.items():
            committed[(tp.topic, tp.partition)] = off

    def committed(self, partitions, timeout=None):
        c = cluster.group(self.group_id)["committed"]
        return [TopicPartition(tp.topic, tp.partition, c.get((tp.topic, tp.partition), -1001)) for tp in partitions]

    def position(self, partitions):
        return [TopicPartition(tp.topic, tp.partition, self._positions.get(TopicPartition(tp.topic, tp.partition), -1001)) for tp in partitions]

    def get_watermark_offsets(self, partition, timeout=None, cached=False):
        log = cluster.topic(partition.topic)[partition.partition]
        return (0, len(log))

    def seek(self, partition):
        self._positions[TopicPartition(partition.topic, partition.partition)] = partition.offset

    def list_topics(self, topic=None, timeout=None):
        return _metadata()

    def close(self):
        if self._closed:
            return
        if self.auto_commit:
            self._commit_positions(dict(self._positions))
        self._closed = True
        g = cluster.group(self.group_id)
        if self in g["members"]:
            g["members"].remove(self)
        cluster.rebalance(self.group_id)

    def _check(self):
        if self._closed:
            raise RuntimeError("Consumer closed")


# ---------------------------------------------------------------- AdminClient

class NewTopic:
    def __init__(self, topic, num_partitions=1, replication_factor=1, config=None):
        self.topic, self.num_partitions, self.replication_factor = topic, num_partitions, replication_factor
        self.config = config or {}


class _Future:
    def __init__(self, error=None):
        self._error = error

    def result(self, timeout=None):
        if self._error:
            raise KafkaException(self._error)
        return None


class _TopicMeta:
    def __init__(self, name, n):
        self.topic = name
        self.partitions = {p: p for p in range(n)}


class _ClusterMeta:
    def __init__(self):
        self.topics = {name: _TopicMeta(name, len(parts)) for name, parts in cluster.topics.items()}


def _metadata():
    return _ClusterMeta()


class AdminClient:
    def __init__(self, config=None):
        self.config = dict(config or {})

    def create_topics(self, new_topics, operation_timeout=None):
        res = {}
        for nt in new_topics:
            if nt.topic in cluster.topics:
                res[nt.topic] = _Future(KafkaError(36, f"Topic '{nt.topic}' already exists."))
            else:
                cluster.topics[nt.topic] = [[] for _ in range(nt.num_partitions)]
                res[nt.topic] = _Future()
        return res

    def delete_topics(self, topics, operation_timeout=None):
        for t in topics:
            cluster.topics.pop(t, None)
        return {t: _Future() for t in topics}

    def list_topics(self, topic=None, timeout=None):
        return _metadata()

    def list_groups(self):
        return list(cluster.groups)

    def lag(self, group_id, topic):
        """Учебный помощник (в confluent-kafka его нет): lag группы по партициям — {партиция: отставание}."""
        committed = cluster.group(group_id)["committed"]
        return {p: len(log) - committed.get((topic, p), 0) for p, log in enumerate(cluster.topic(topic))}
