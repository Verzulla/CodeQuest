"""SQLite: подключение и схема.

Весь прогресс и весь контент живут в одном файле data/codequest.db.
Путь можно переопределить переменной окружения CODEQUEST_DB (используют тесты).
"""
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "data" / "codequest.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS topics (
    id          INTEGER PRIMARY KEY,
    slug        TEXT NOT NULL UNIQUE,
    title       TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    icon        TEXT NOT NULL DEFAULT '🐍',
    color       TEXT NOT NULL DEFAULT '#58cc02',
    position    INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS modules (
    id          INTEGER PRIMARY KEY,
    topic_id    INTEGER NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    slug        TEXT NOT NULL UNIQUE,
    title       TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    icon        TEXT NOT NULL DEFAULT '⭐',
    position    INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS lessons (
    id          INTEGER PRIMARY KEY,
    module_id   INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    slug        TEXT NOT NULL UNIQUE,
    title       TEXT NOT NULL,
    theory      TEXT NOT NULL DEFAULT '',
    position    INTEGER NOT NULL DEFAULT 0
);

-- type = 'code'   : пишешь код, он запускается и проверяется тестами (tests)
-- type = 'output' : читаешь код (code) и вводишь, что он выведет (expected_output)
CREATE TABLE IF NOT EXISTS exercises (
    id              INTEGER PRIMARY KEY,
    lesson_id       INTEGER NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    slug            TEXT NOT NULL UNIQUE,
    type            TEXT NOT NULL CHECK (type IN ('code', 'output')),
    prompt          TEXT NOT NULL,
    code            TEXT NOT NULL DEFAULT '',
    starter_code    TEXT NOT NULL DEFAULT '',
    tests           TEXT NOT NULL DEFAULT '',
    expected_output TEXT NOT NULL DEFAULT '',
    solution        TEXT NOT NULL DEFAULT '',
    hint            TEXT NOT NULL DEFAULT '',
    xp              INTEGER NOT NULL DEFAULT 10,
    position        INTEGER NOT NULL DEFAULT 0
);

-- ===== Прогресс =====

CREATE TABLE IF NOT EXISTS user_state (
    id                 INTEGER PRIMARY KEY CHECK (id = 1),
    xp                 INTEGER NOT NULL DEFAULT 0,
    hearts             INTEGER NOT NULL DEFAULT 5,
    hearts_updated_at  TEXT,
    hearts_enabled     INTEGER NOT NULL DEFAULT 1,
    streak             INTEGER NOT NULL DEFAULT 0,
    longest_streak     INTEGER NOT NULL DEFAULT 0,
    last_active_date   TEXT,
    freezes            INTEGER NOT NULL DEFAULT 1,
    daily_goal         INTEGER NOT NULL DEFAULT 30,
    theme              TEXT NOT NULL DEFAULT 'light'
);

-- Слаги (а не id) — чтобы прогресс переживал переимпорт контента.
CREATE TABLE IF NOT EXISTS exercise_progress (
    exercise_slug TEXT PRIMARY KEY,
    solved        INTEGER NOT NULL DEFAULT 0,
    solved_at     TEXT,
    mistakes      INTEGER NOT NULL DEFAULT 0,
    in_review     INTEGER NOT NULL DEFAULT 0,
    last_answer   TEXT NOT NULL DEFAULT '',   -- последнее верное решение
    draft         TEXT NOT NULL DEFAULT ''    -- недописанный ответ (автосохранение)
);

CREATE TABLE IF NOT EXISTS lesson_completions (
    lesson_slug  TEXT PRIMARY KEY,
    completed_at TEXT NOT NULL,
    times        INTEGER NOT NULL DEFAULT 1,
    perfect      INTEGER NOT NULL DEFAULT 0
);

-- Награды за модули и темы (kind = 'module' | 'topic')
CREATE TABLE IF NOT EXISTS trophies (
    kind       TEXT NOT NULL,
    slug       TEXT NOT NULL,
    earned_at  TEXT NOT NULL,
    PRIMARY KEY (kind, slug)
);

CREATE TABLE IF NOT EXISTS achievements (
    code        TEXT PRIMARY KEY,
    unlocked_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS daily_activity (
    day             TEXT PRIMARY KEY,
    xp              INTEGER NOT NULL DEFAULT 0,
    solved          INTEGER NOT NULL DEFAULT 0,
    mistakes        INTEGER NOT NULL DEFAULT 0,
    goal_met        INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS counters (
    name  TEXT PRIMARY KEY,
    value INTEGER NOT NULL DEFAULT 0
);

INSERT OR IGNORE INTO user_state (id) VALUES (1);
"""


def db_path() -> Path:
    return Path(os.environ.get("CODEQUEST_DB", DEFAULT_DB))


def connect() -> sqlite3.Connection:
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


@contextmanager
def transaction():
    """Одна транзакция на запрос: либо всё записалось, либо ничего."""
    conn = connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# Колонки, добавленные после первой версии: (таблица, колонка, определение).
# Для уже существующих баз добавляются через ALTER TABLE — прогресс не теряется.
MIGRATIONS = [
    ("exercise_progress", "draft", "TEXT NOT NULL DEFAULT ''"),
    ("topics", "group_name", "TEXT NOT NULL DEFAULT ''"),          # группа в каталоге тем
    ("user_state", "last_lesson_slug", "TEXT"),                     # для плашки «Продолжить»
    ("lessons", "theory_full", "TEXT NOT NULL DEFAULT ''"),        # подробный теоретический урок
    ("lessons", "quiz", "TEXT NOT NULL DEFAULT '[]'"),             # «Проверь себя»: JSON-список вопросов
]


def init_db() -> None:
    with transaction() as conn:
        conn.executescript(SCHEMA)
        for table, column, definition in MIGRATIONS:
            existing = {r["name"] for r in conn.execute(f"PRAGMA table_info({table})")}
            if column not in existing:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
