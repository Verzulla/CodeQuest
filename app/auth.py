"""Аккаунты и сессии.

Регистрация — ник + пароль, без подтверждений. Пароль хранится как scrypt-хеш
с солью; сессия — случайный токен в httpOnly-cookie, в базе лежит только его sha256.
Сессия живёт SESSION_TTL и продлевается, пока пользователь активен.
"""
import base64
import hashlib
import hmac
import re
import secrets
import sqlite3
import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta

from . import game
from .db import claim_legacy_progress, has_legacy_progress

SESSION_TTL = timedelta(days=5)
SESSION_REFRESH_EVERY = timedelta(hours=1)   # чаще не переписываем срок — лишние записи в БД

USERNAME_RE = re.compile(r"^[A-Za-zА-Яа-яЁё0-9_]{3,20}$")
PASSWORD_MIN, PASSWORD_MAX = 6, 128

SCRYPT = {"n": 2 ** 14, "r": 8, "p": 1}


class AuthError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


# ---------- пароли ----------

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, dklen=32, **SCRYPT)
    b64 = lambda b: base64.b64encode(b).decode()  # noqa: E731
    return f"scrypt${SCRYPT['n']}${SCRYPT['r']}${SCRYPT['p']}${b64(salt)}${b64(digest)}"


def verify_password(password: str, stored: str) -> bool:
    try:
        _algo, n, r, p, salt, digest = stored.split("$")
        expected = base64.b64decode(digest)
        actual = hashlib.scrypt(password.encode(), salt=base64.b64decode(salt),
                                n=int(n), r=int(r), p=int(p), dklen=len(expected))
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(actual, expected)


# Проверяем пароль и для несуществующего ника — чтобы по времени ответа нельзя было
# понять, есть ли такой пользователь.
_DUMMY_HASH = hash_password(secrets.token_hex(8))


def validate_credentials(username: str, password: str) -> str:
    username = username.strip()
    if not USERNAME_RE.fullmatch(username):
        raise AuthError(400, "Ник: от 3 до 20 символов — буквы, цифры и _")
    check_password_rules(password)
    return username


def check_password_rules(password: str) -> None:
    if not PASSWORD_MIN <= len(password) <= PASSWORD_MAX:
        raise AuthError(400, f"Пароль: от {PASSWORD_MIN} до {PASSWORD_MAX} символов")


# ---------- пользователи ----------

def find_user(conn, username: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM users WHERE username_key = ?", (username.strip().casefold(),)
    ).fetchone()


def create_user(conn, username: str, password: str) -> tuple[sqlite3.Row, bool]:
    """→ (пользователь, забрал ли он прогресс однопользовательской версии).
    Первый зарегистрированный пользователь становится администратором."""
    username = validate_credentials(username, password)
    if find_user(conn, username):
        raise AuthError(409, "Этот ник уже занят")
    first = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0
    cur = conn.execute(
        "INSERT INTO users (username, username_key, password_hash, is_admin, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (username, username.casefold(), hash_password(password), int(first), game.now().isoformat()),
    )
    uid = cur.lastrowid
    conn.execute("INSERT INTO user_state (user_id, onboarded) VALUES (?, 0)", (uid,))   # покажем приветствие
    claimed = has_legacy_progress(conn) and claim_legacy_progress(conn, uid)
    return conn.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone(), claimed


def authenticate(conn, username: str, password: str) -> sqlite3.Row | None:
    user = find_user(conn, username)
    ok = verify_password(password, user["password_hash"] if user else _DUMMY_HASH)
    return user if user and ok else None


def set_password(conn, uid: int, password: str) -> None:
    check_password_rules(password)
    conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hash_password(password), uid))


def set_admin(conn, username: str, is_admin: bool) -> sqlite3.Row:
    user = find_user(conn, username)
    if not user:
        raise AuthError(404, f"Пользователь «{username}» не найден")
    conn.execute("UPDATE users SET is_admin = ? WHERE id = ?", (int(is_admin), user["id"]))
    return user


def public(user: sqlite3.Row) -> dict:
    return {"id": user["id"], "username": user["username"], "is_admin": bool(user["is_admin"])}


# ---------- сессии ----------

def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def new_session(conn, uid: int) -> str:
    token = secrets.token_urlsafe(32)
    t = game.now()
    conn.execute(
        "INSERT INTO sessions (token_hash, user_id, created_at, expires_at, refreshed_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (_token_hash(token), uid, t.isoformat(), (t + SESSION_TTL).isoformat(), t.isoformat()),
    )
    return token


def session_user(conn, token: str) -> tuple[sqlite3.Row | None, bool]:
    """→ (пользователь или None, продлили ли сессию — тогда cookie нужно выдать заново)."""
    t = game.now()
    conn.execute("DELETE FROM sessions WHERE expires_at <= ?", (t.isoformat(),))
    row = conn.execute(
        "SELECT s.refreshed_at, u.* FROM sessions s JOIN users u ON u.id = s.user_id "
        "WHERE s.token_hash = ?", (_token_hash(token),)
    ).fetchone()
    if not row:
        return None, False
    if t - datetime.fromisoformat(row["refreshed_at"]) < SESSION_REFRESH_EVERY:
        return row, False
    conn.execute(
        "UPDATE sessions SET expires_at = ?, refreshed_at = ? WHERE token_hash = ?",
        ((t + SESSION_TTL).isoformat(), t.isoformat(), _token_hash(token)),
    )
    return row, True


def end_session(conn, token: str) -> None:
    conn.execute("DELETE FROM sessions WHERE token_hash = ?", (_token_hash(token),))


def end_other_sessions(conn, uid: int, keep_token: str) -> None:
    conn.execute("DELETE FROM sessions WHERE user_id = ? AND token_hash != ?",
                 (uid, _token_hash(keep_token)))


# ---------- ограничение попыток ----------

class RateLimiter:
    """Скользящее окно в памяти процесса: не больше limit событий за window секунд на ключ."""

    def __init__(self):
        self._events: dict[str, deque] = defaultdict(deque)
        self._lock = threading.Lock()

    def _trim(self, key: str, window: float) -> deque:
        q = self._events[key]
        edge = time.monotonic() - window
        while q and q[0] <= edge:
            q.popleft()
        return q

    def allowed(self, key: str, limit: int, window: float) -> bool:
        with self._lock:
            return len(self._trim(key, window)) < limit

    def add(self, key: str) -> None:
        with self._lock:
            self._events[key].append(time.monotonic())

    def clear(self) -> None:
        with self._lock:
            self._events.clear()


limiter = RateLimiter()
LOGIN_FAILS = (10, 15 * 60)      # неверных паролей с одного IP за 15 минут
REGISTRATIONS = (5, 60 * 60)     # новых аккаунтов с одного IP за час
CODE_RUNS = (30, 60)             # запусков кода (▶ и проверка) одного пользователя за минуту
