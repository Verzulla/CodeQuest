"""SQLite: подключение и схема.

Контент, аккаунты и прогресс всех пользователей живут в одном файле data/codequest.db.
Путь можно переопределить переменной окружения CODEQUEST_DB (используют тесты).
"""
import os
import re
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
-- type = 'command': «Терминал» — вводишь команду или короткий ответ; expected_output —
--                   допустимые варианты по одному на строку (строка «re:…» — регулярное
--                   выражение), code — необязательный контекст (вывод терминала), solution — эталон
CREATE TABLE IF NOT EXISTS exercises (
    id              INTEGER PRIMARY KEY,
    lesson_id       INTEGER NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    slug            TEXT NOT NULL UNIQUE,
    type            TEXT NOT NULL CHECK (type IN ('code', 'output', 'command')),
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

-- ===== Аккаунты =====

-- username — как ввёл пользователь, username_key — casefold() для уникальности без учёта
-- регистра (COLLATE NOCASE не понимает кириллицу).
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY,
    username      TEXT NOT NULL,
    username_key  TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_admin      INTEGER NOT NULL DEFAULT 0,
    created_at    TEXT NOT NULL
);

-- В базе только sha256 от токена: утечка файла БД не даёт готовых сессий.
CREATE TABLE IF NOT EXISTS sessions (
    token_hash   TEXT PRIMARY KEY,
    user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at   TEXT NOT NULL,
    expires_at   TEXT NOT NULL,
    refreshed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS sessions_user ON sessions(user_id);

-- ===== Прогресс (у каждого пользователя свой) =====

CREATE TABLE IF NOT EXISTS user_state (
    user_id            INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    xp                 INTEGER NOT NULL DEFAULT 0,
    hearts             INTEGER NOT NULL DEFAULT 5,
    hearts_updated_at  TEXT,
    hearts_enabled     INTEGER NOT NULL DEFAULT 1,
    sequential_lessons INTEGER NOT NULL DEFAULT 1,  -- уроки темы открываются по порядку
    onboarded          INTEGER NOT NULL DEFAULT 1,  -- видел приветствие; новым аккаунтам ставится 0
    streak             INTEGER NOT NULL DEFAULT 0,
    longest_streak     INTEGER NOT NULL DEFAULT 0,
    last_active_date   TEXT,
    freezes            INTEGER NOT NULL DEFAULT 1,
    daily_goal         INTEGER NOT NULL DEFAULT 30,
    theme              TEXT NOT NULL DEFAULT 'dark',
    path_view          TEXT NOT NULL DEFAULT 'zigzag',  -- дорожка уроков: 'zigzag' или 'list'
    last_lesson_slug   TEXT                           -- для плашки «Продолжить»
);

-- Слаги (а не id) — чтобы прогресс переживал переимпорт контента.
CREATE TABLE IF NOT EXISTS exercise_progress (
    user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    exercise_slug TEXT NOT NULL,
    solved        INTEGER NOT NULL DEFAULT 0,
    solved_at     TEXT,
    mistakes      INTEGER NOT NULL DEFAULT 0,
    in_review     INTEGER NOT NULL DEFAULT 0,
    hearts_lost   INTEGER NOT NULL DEFAULT 0,   -- сколько сердечек стоило; вернутся при исправлении
    last_answer   TEXT NOT NULL DEFAULT '',   -- последнее верное решение
    draft         TEXT NOT NULL DEFAULT '',   -- недописанный ответ (автосохранение)
    PRIMARY KEY (user_id, exercise_slug)
);

CREATE TABLE IF NOT EXISTS lesson_completions (
    user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lesson_slug  TEXT NOT NULL,
    completed_at TEXT NOT NULL,
    times        INTEGER NOT NULL DEFAULT 1,
    perfect      INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, lesson_slug)
);

-- Награды за модули и темы (kind = 'module' | 'topic')
CREATE TABLE IF NOT EXISTS trophies (
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    kind       TEXT NOT NULL,
    slug       TEXT NOT NULL,
    earned_at  TEXT NOT NULL,
    PRIMARY KEY (user_id, kind, slug)
);

CREATE TABLE IF NOT EXISTS achievements (
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    code        TEXT NOT NULL,
    unlocked_at TEXT NOT NULL,
    PRIMARY KEY (user_id, code)
);

CREATE TABLE IF NOT EXISTS daily_activity (
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    day             TEXT NOT NULL,
    xp              INTEGER NOT NULL DEFAULT 0,
    solved          INTEGER NOT NULL DEFAULT 0,
    mistakes        INTEGER NOT NULL DEFAULT 0,
    goal_met        INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, day)
);

CREATE TABLE IF NOT EXISTS counters (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name    TEXT NOT NULL,
    value   INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, name)
);
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
    ("topics", "group_name", "TEXT NOT NULL DEFAULT ''"),          # группа в каталоге тем
    ("lessons", "theory_full", "TEXT NOT NULL DEFAULT ''"),        # подробный теоретический урок
    ("lessons", "quiz", "TEXT NOT NULL DEFAULT '[]'"),             # «Проверь себя»: JSON-список вопросов
    ("user_state", "sequential_lessons", "INTEGER NOT NULL DEFAULT 1"),  # уроки по порядку (замки)
    ("user_state", "onboarded", "INTEGER NOT NULL DEFAULT 1"),  # приветствие: старым аккаунтам не показываем
    ("exercise_progress", "hearts_lost", "INTEGER NOT NULL DEFAULT 0"),  # сердечки, потерянные на задании
    ("user_state", "path_view", "TEXT NOT NULL DEFAULT 'zigzag'"),  # вид дорожки уроков (редизайн)
]


PROGRESS_TABLES = ("user_state", "exercise_progress", "lesson_completions", "trophies",
                   "achievements", "daily_activity", "counters")


def _columns(conn, table: str) -> list[str]:
    return [r["name"] for r in conn.execute(f"PRAGMA table_info({table})")]


def _park_legacy_progress(conn) -> None:
    """База из однопользовательской версии: таблицы прогресса без user_id.
    Откладываем их как legacy_* — их заберёт первый зарегистрированный аккаунт."""
    for table in PROGRESS_TABLES:
        cols = _columns(conn, table)
        if cols and "user_id" not in cols and not _columns(conn, f"legacy_{table}"):
            conn.execute(f"ALTER TABLE {table} RENAME TO legacy_{table}")


def has_legacy_progress(conn) -> bool:
    return any(_columns(conn, f"legacy_{t}") for t in PROGRESS_TABLES)


def claim_legacy_progress(conn, user_id: int) -> bool:
    """Переносит прогресс однопользовательской версии в аккаунт user_id и удаляет legacy_*."""
    claimed = False
    for table in PROGRESS_TABLES:
        legacy = f"legacy_{table}"
        old_cols = _columns(conn, legacy)
        if not old_cols:
            continue
        common = [c for c in _columns(conn, table) if c in old_cols and c != "user_id"]
        if table == "user_state":
            conn.execute("DELETE FROM user_state WHERE user_id = ?", (user_id,))
        cols = ", ".join(common)
        conn.execute(f"INSERT INTO {table} (user_id, {cols}) SELECT ?, {cols} FROM {legacy}", (user_id,))
        conn.execute(f"DROP TABLE {legacy}")
        claimed = True
    return claimed


def init_db() -> None:
    with transaction() as conn:
        _park_legacy_progress(conn)
        conn.executescript(SCHEMA)
        for table, column, definition in MIGRATIONS:
            existing = {r["name"] for r in conn.execute(f"PRAGMA table_info({table})")}
            if column not in existing:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
                if column == "hearts_lost":
                    # Сердечки больше не восстанавливаются со временем, а сколько их потеряно на старых
                    # ошибках, неизвестно — чтобы никто не застрял без сердечек, один раз заполняем их.
                    conn.execute("UPDATE user_state SET hearts = 5")
                if column == "path_view":
                    # Редизайн рассчитан на тёмную тему — при переходе на него включаем её всем один раз.
                    conn.execute("UPDATE user_state SET theme = 'dark'")
        _migrate_exercise_types(conn)


def _migrate_exercise_types(conn) -> None:
    """Старые базы: в CHECK таблицы exercises нет типа 'command'. SQLite не умеет менять
    CHECK, поэтому таблица пересоздаётся с тем же содержимым (прогресс хранится по слагам
    в других таблицах и не затрагивается)."""
    row = conn.execute("SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'exercises'").fetchone()
    if row is None or "'command'" in row["sql"]:
        return
    create = re.search(r"CREATE TABLE IF NOT EXISTS exercises \(.*?\n\);", SCHEMA, re.S).group(0)
    cols = ", ".join(_columns(conn, "exercises"))
    conn.execute("ALTER TABLE exercises RENAME TO exercises_old")
    conn.execute(create)
    conn.execute(f"INSERT INTO exercises ({cols}) SELECT {cols} FROM exercises_old")
    conn.execute("DROP TABLE exercises_old")
