"""HTTP API + раздача фронтенда. Запуск: ./run.sh (или python -m app)."""
import hashlib
import json
import logging
import os
import random
import re
import sqlite3
from contextlib import asynccontextmanager
from datetime import timedelta
from pathlib import Path
from typing import Annotated, Literal
from urllib.parse import urlsplit

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import auth, content, explain, game, runner
from .db import PROGRESS_TABLES, ROOT, init_db, transaction

STATIC = ROOT / "static"
CONTENT_DIR = ROOT / "content"


def seed_if_empty() -> None:
    """При самом первом запуске загружаем стартовые пакеты из content/.
    Дальше импорт — только явный (админка или CLI), чтобы не затирать правки."""
    with transaction() as conn:
        if conn.execute("SELECT COUNT(*) FROM topics").fetchone()[0]:
            return
        for f in content.content_files(CONTENT_DIR):
            pkg = content.Package.model_validate_json(f.read_text(encoding="utf-8"))
            content.import_package(conn, pkg)


@asynccontextmanager
async def lifespan(_app):
    if runner.sandbox_mode() == "local":
        logging.getLogger("codequest").warning(
            "CODEQUEST_SANDBOX=local: код учеников выполняется БЕЗ изоляции. "
            "Для сервера в интернете используй docker-песочницу.")
    init_db()
    seed_if_empty()
    yield


app = FastAPI(title="CodeQuest", lifespan=lifespan)


@app.middleware("http")
async def no_stale_static(request, call_next):
    """Браузер перепроверяет статику при каждом запросе — после обновления кода не нужен жёсткий релоад."""
    response = await call_next(request)
    if request.url.path.startswith("/static"):
        response.headers["Cache-Control"] = "no-cache"
    return response


@app.middleware("http")
async def same_origin_writes(request, call_next):
    """Защита от CSRF: изменяющие запросы к API принимаем только со своей страницы.
    Браузер всегда шлёт Origin для кросс-доменных POST/PUT/DELETE."""
    if request.method not in ("GET", "HEAD", "OPTIONS") and request.url.path.startswith("/api/"):
        origin = request.headers.get("origin")
        if origin and urlsplit(origin).netloc != request.headers.get("host"):
            return JSONResponse({"detail": "Запрос с чужого сайта отклонён"}, status_code=403)
    return await call_next(request)


# =================== Аккаунты ===================

COOKIE = "cq_session"


def _secure_cookie(request: Request) -> bool:
    # За HTTPS-прокси схема запроса может быть http — тогда включается переменной окружения.
    return request.url.scheme == "https" or os.environ.get("CODEQUEST_SECURE_COOKIE") == "1"


def _set_session_cookie(response: Response, request: Request, token: str) -> None:
    response.set_cookie(COOKIE, token, max_age=int(auth.SESSION_TTL.total_seconds()),
                        httponly=True, samesite="lax", secure=_secure_cookie(request), path="/")


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "?"


def current_user(request: Request, response: Response) -> sqlite3.Row:
    token = request.cookies.get(COOKIE)
    if token:
        with transaction() as conn:
            user, refreshed = auth.session_user(conn, token)
        if user:
            if refreshed:
                _set_session_cookie(response, request, token)
            return user
    raise HTTPException(401, "Нужно войти в аккаунт")


def admin_user(user: Annotated[sqlite3.Row, Depends(current_user)]) -> sqlite3.Row:
    if not user["is_admin"]:
        raise HTTPException(403, "Раздел доступен только администратору")
    return user


User = Annotated[sqlite3.Row, Depends(current_user)]
Admin = Annotated[sqlite3.Row, Depends(admin_user)]


class Credentials(BaseModel):
    username: str = Field(max_length=64)
    password: str = Field(max_length=256)


def _auth_error(e: auth.AuthError):
    return HTTPException(e.status, e.message)


@app.post("/api/auth/register")
def register(body: Credentials, request: Request, response: Response):
    key = f"register:{_client_ip(request)}"
    if not auth.limiter.allowed(key, *auth.REGISTRATIONS):
        raise HTTPException(429, "Слишком много регистраций с этого адреса — попробуй позже")
    with transaction() as conn:
        try:
            user, claimed = auth.create_user(conn, body.username, body.password)
        except auth.AuthError as e:
            raise _auth_error(e)
        token = auth.new_session(conn, user["id"])
    auth.limiter.add(key)
    _set_session_cookie(response, request, token)
    return {**auth.public(user), "claimed_progress": claimed}


def _check_login_limit(request: Request) -> str:
    key = f"login:{_client_ip(request)}"
    if not auth.limiter.allowed(key, *auth.LOGIN_FAILS):
        raise HTTPException(429, "Слишком много неудачных попыток — подожди 15 минут")
    return key


@app.post("/api/auth/login")
def login(body: Credentials, request: Request, response: Response):
    key = _check_login_limit(request)
    with transaction() as conn:
        user = auth.authenticate(conn, body.username, body.password)
        if not user:
            auth.limiter.add(key)
            raise HTTPException(401, "Неверный ник или пароль")
        token = auth.new_session(conn, user["id"])
    _set_session_cookie(response, request, token)
    return auth.public(user)


@app.post("/api/auth/logout")
def logout(request: Request, response: Response):
    token = request.cookies.get(COOKIE)
    if token:
        with transaction() as conn:
            auth.end_session(conn, token)
    response.delete_cookie(COOKIE, path="/")
    return {"ok": True}


@app.get("/api/auth/me")
def me(user: User):
    return auth.public(user)


# Аватарка: только растровые картинки в data-URL (SVG нельзя — в нём может быть скрипт), до ~120 КБ.
AVATAR_RE = re.compile(r"^data:image/(png|jpeg|webp);base64,[A-Za-z0-9+/]+={0,2}$")
AVATAR_MAX = 160_000


class AvatarIn(BaseModel):
    image: str = Field("", max_length=AVATAR_MAX)   # пустая строка — убрать аватарку


@app.put("/api/account/avatar")
def set_avatar(body: AvatarIn, user: User):
    if body.image and not AVATAR_RE.match(body.image):
        raise HTTPException(400, "Нужна картинка PNG, JPEG или WebP")
    with transaction() as conn:
        conn.execute("UPDATE users SET avatar = ? WHERE id = ?", (body.image, user["id"]))
        return auth.public(conn.execute("SELECT * FROM users WHERE id = ?", (user["id"],)).fetchone())


class PasswordIn(BaseModel):
    current_password: str = Field(max_length=256)
    new_password: str = Field(max_length=256)


@app.put("/api/account/password")
def change_password(body: PasswordIn, user: User, request: Request):
    """Смена пароля завершает все остальные сессии — на других устройствах придётся войти заново."""
    key = _check_login_limit(request)
    with transaction() as conn:
        if not auth.verify_password(body.current_password, user["password_hash"]):
            auth.limiter.add(key)
            raise HTTPException(400, "Текущий пароль неверный")
        try:
            auth.set_password(conn, user["id"], body.new_password)
        except auth.AuthError as e:
            raise _auth_error(e)
        auth.end_other_sessions(conn, user["id"], request.cookies[COOKIE])
    return {"ok": True}


class DeleteAccountIn(BaseModel):
    password: str = Field(max_length=256)


@app.post("/api/account/delete")
def delete_account(body: DeleteAccountIn, user: User, request: Request, response: Response):
    """Удаляет аккаунт и весь его прогресс (каскадом по user_id). Контент не трогается."""
    key = _check_login_limit(request)
    if not auth.verify_password(body.password, user["password_hash"]):
        auth.limiter.add(key)
        raise HTTPException(400, "Неверный пароль")
    with transaction() as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user["id"],))
    response.delete_cookie(COOKIE, path="/")
    return {"ok": True}


def _get(conn, table: str, id_: int):
    row = conn.execute(f"SELECT * FROM {table} WHERE id = ?", (id_,)).fetchone()
    if not row:
        raise HTTPException(404, "Не найдено")
    return row


# =================== Обучение ===================

@app.get("/api/state")
def state(user: User):
    with transaction() as conn:
        notice = game.settle_streak(conn, user["id"])
        return {**game.get_state(conn, user["id"]), "notice": notice}


@app.get("/api/rules")
def rules():
    """Правила игры для вкладки «О приложении» — прямо из констант движка,
    чтобы описание никогда не расходилось с реальным поведением."""
    return {
        "xp": {
            "exercise_default": 10,
            "practice": game.XP_PRACTICE,
            "review_fix": game.XP_REVIEW_FIX,
            "lesson_first": game.XP_LESSON_FIRST,
            "lesson_perfect": game.XP_LESSON_PERFECT,
            "lesson_repeat": game.XP_LESSON_REPEAT,
            "module": game.XP_MODULE,
            "topic": game.XP_TOPIC,
        },
        "levels": [{"level": n, "xp": game.level_threshold(n)} for n in range(1, 11)],
        "hearts": {"max": game.MAX_HEARTS},
        "freezes": {"max": game.MAX_FREEZES, "every_days": 7},
        "run_timeout_sec": runner.TIMEOUT_SEC,
        "achievements": [
            {"code": code, "icon": icon, "title": title, "description": desc}
            for code, icon, title, desc, _rule in game.ACHIEVEMENTS
        ],
    }


@app.get("/api/continue")
def continue_learning(user: User):
    with transaction() as conn:
        return content.continue_target(conn, user["id"])


@app.get("/api/topics/{topic_id}/theory")
def topic_theory(topic_id: int, _user: User):
    """Вся теория темы — учебник: модули → уроки с полной теорией и шпаргалкой. Замки не учитываются:
    читать вперёд можно, закрыты только задания."""
    with transaction() as conn:
        t = _get(conn, "topics", topic_id)
        modules = []
        for m in conn.execute("SELECT * FROM modules WHERE topic_id = ? ORDER BY position, id", (topic_id,)):
            lessons = [{"id": l["id"], "title": l["title"], "theory": l["theory"], "theory_full": l["theory_full"]}
                       for l in conn.execute("SELECT * FROM lessons WHERE module_id = ? ORDER BY position, id", (m["id"],))]
            modules.append({"title": m["title"], "icon": m["icon"], "lessons": lessons})
    return {"id": t["id"], "slug": t["slug"], "title": t["title"], "icon": t["icon"], "color": t["color"], "modules": modules}


@app.get("/api/path")
def path(user: User):
    with transaction() as conn:
        return content.learning_path(conn, user["id"])


def _public_exercise(e, progress: dict) -> dict:
    """Задание для ученика: без тестов и эталона, но с его прогрессом —
    чтобы урок продолжался с того же места и показывал прежние решения."""
    p = progress.get(e["slug"])
    solved = bool(p and p["solved"])
    return {
        "id": e["id"], "type": e["type"], "prompt": e["prompt"], "code": e["code"],
        "starter_code": e["starter_code"], "hint": e["hint"], "xp": e["xp"],
        "solved": solved,
        "in_review": bool(p and p["in_review"]),        # была ошибка — задание в работе над ошибками
        "answer": p["last_answer"] if solved else "",   # последнее верное решение
        "draft": p["draft"] if p else "",               # недописанный ответ
    }


def _progress(conn, uid: int) -> dict:
    return {r["exercise_slug"]: r
            for r in conn.execute("SELECT * FROM exercise_progress WHERE user_id = ?", (uid,))}


@app.get("/api/lessons/{lesson_id}")
def get_lesson(lesson_id: int, user: User):
    uid = user["id"]
    with transaction() as conn:
        lesson = _get(conn, "lessons", lesson_id)
        if not content.lesson_is_unlocked(conn, uid, lesson_id):
            raise HTTPException(403, "Урок ещё закрыт — сначала пройди предыдущие")
        module = _get(conn, "modules", lesson["module_id"])
        topic = _get(conn, "topics", module["topic_id"])
        progress = _progress(conn, uid)
        exs = conn.execute(
            "SELECT * FROM exercises WHERE lesson_id = ? ORDER BY position, id", (lesson_id,)
        ).fetchall()
        completed = conn.execute(
            "SELECT 1 FROM lesson_completions WHERE user_id = ? AND lesson_slug = ?",
            (uid, lesson["slug"]),
        ).fetchone() is not None
        conn.execute("UPDATE user_state SET last_lesson_slug = ? WHERE user_id = ?",
                     (lesson["slug"], uid))
        return {
            "id": lesson["id"], "title": lesson["title"], "theory": lesson["theory"],
            "theory_full": lesson["theory_full"], "quiz": json.loads(lesson["quiz"] or "[]"),
            "completed": completed,
            "module": {"title": module["title"], "icon": module["icon"]},
            "topic": {"id": topic["id"], "title": topic["title"], "color": topic["color"]},
            "exercises": [_public_exercise(e, progress) for e in exs],
        }


def _limit_runs(user) -> None:
    key = f"run:{user['id']}"
    if not auth.limiter.allowed(key, *auth.CODE_RUNS):
        raise HTTPException(429, "Слишком много запусков подряд — подожди минутку")
    auth.limiter.add(key)


class RunIn(BaseModel):
    code: str = Field(max_length=20_000)


@app.post("/api/run")
def run_code(body: RunIn, user: User):
    """Просто запустить код (без тестов и без штрафа) — песочница."""
    _limit_runs(user)
    return runner.run(body.code).to_dict()


class CheckIn(BaseModel):
    answer: str = Field(max_length=20_000)
    mode: Literal["lesson", "review", "practice", "warmup"] = "lesson"
    fix: bool = False   # сразу исправляет только что допущенную ошибку (кнопка «Исправить»)


@app.post("/api/exercises/{ex_id}/check")
def check(ex_id: int, body: CheckIn, user: User):
    with transaction() as conn:
        ex = _get(conn, "exercises", ex_id)
    # Код запускаем вне транзакции — это может занять секунды.
    details = None
    if ex["type"] == "code":
        _limit_runs(user)
        res = runner.run(body.answer, ex["tests"])
        correct, details = res.passed, res.to_dict()
    elif ex["type"] == "command":
        correct = runner.command_matches(body.answer, ex["expected_output"])
    else:
        correct = runner.output_matches(body.answer, ex["expected_output"])
    with transaction() as conn:
        try:
            events = game.record_answer(conn, user["id"], ex, correct, body.answer, body.mode, body.fix)
        except game.NoHearts:
            raise HTTPException(409, "Сердечки закончились")
        return {
            "correct": correct,
            "details": details,
            "expected": None if correct else (ex["expected_output"] if ex["type"] == "output"
                                              else ex["solution"] if ex["type"] == "command" else None),
            "events": events,
            "state": game.get_state(conn, user["id"]),
        }


class DraftIn(BaseModel):
    draft: str = Field(max_length=20_000)


@app.put("/api/exercises/{ex_id}/draft")
def save_draft(ex_id: int, body: DraftIn, user: User):
    """Автосохранение недописанного ответа — чтобы после перезахода продолжить с того же места."""
    with transaction() as conn:
        ex = _get(conn, "exercises", ex_id)
        conn.execute(
            "INSERT INTO exercise_progress (user_id, exercise_slug, draft) VALUES (?, ?, ?) "
            "ON CONFLICT(user_id, exercise_slug) DO UPDATE SET draft = excluded.draft",
            (user["id"], ex["slug"], body.draft),
        )
        return {"ok": True}


@app.get("/api/exercises/{ex_id}/solution")
def solution(ex_id: int, _user: User):
    with transaction() as conn:
        ex = _get(conn, "exercises", ex_id)
        return {"solution": ex["solution"] or ex["expected_output"], "explain": explain.explain(ex)}


class CompleteIn(BaseModel):
    mistakes: int = Field(0, ge=0)
    seconds: int = Field(0, ge=0, le=86_400)   # сколько длился урок (для статистики)


@app.post("/api/lessons/{lesson_id}/complete")
def complete(lesson_id: int, body: CompleteIn, user: User):
    with transaction() as conn:
        lesson = _get(conn, "lessons", lesson_id)
        try:
            events = game.complete_lesson(conn, user["id"], lesson, body.mistakes, body.seconds)
        except game.LessonNotFinished:
            raise HTTPException(400, "В уроке остались задания, которые ты ещё не пробовал")
        return {"events": events, "state": game.get_state(conn, user["id"])}


@app.get("/api/review")
def review(user: User):
    """Работа над ошибками; если ошибок нет — тренировка на уже решённом."""
    uid = user["id"]
    with transaction() as conn:
        progress = _progress(conn, uid)
        rows = conn.execute(
            "SELECT e.* FROM exercises e JOIN exercise_progress ep ON ep.exercise_slug = e.slug "
            "WHERE ep.user_id = ? AND ep.in_review = 1 ORDER BY ep.mistakes DESC LIMIT 10", (uid,)
        ).fetchall()
        kind = "mistakes"
        if not rows:
            kind = "practice"
            rows = conn.execute(
                "SELECT e.* FROM exercises e JOIN exercise_progress ep ON ep.exercise_slug = e.slug "
                "WHERE ep.user_id = ? AND ep.solved = 1", (uid,)
            ).fetchall()
            rows = random.sample(rows, min(5, len(rows)))
        # Список для экрана «Повторение»: все задания в работе над ошибками — где они и что вернут.
        items = [dict(r) for r in conn.execute(
            "SELECT e.id, e.type, e.prompt, ep.mistakes, ep.hearts_lost, l.title AS lesson_title, t.title AS topic_title "
            "FROM exercise_progress ep JOIN exercises e ON e.slug = ep.exercise_slug "
            "JOIN lessons l ON l.id = e.lesson_id JOIN modules m ON m.id = l.module_id JOIN topics t ON t.id = m.topic_id "
            "WHERE ep.user_id = ? AND ep.in_review = 1 ORDER BY ep.mistakes DESC, e.id LIMIT 100", (uid,))]
        fixed = conn.execute("SELECT value FROM counters WHERE user_id = ? AND name = 'review_fixed'", (uid,)).fetchone()
        return {"kind": kind, "exercises": [_public_exercise(e, progress) for e in rows],
                "items": items, "fixed": fixed["value"] if fixed else 0, "fix_xp": game.XP_REVIEW_FIX}


# Тренировка: случайные задания выбранных тем. Из пройденных уроков — решённые задания (засчитываются
# как повторение), из непройденных уроков и тем — разминка (warmup: не засчитывается).
_TRAINING_SQL = (
    "SELECT e.*, l.title AS lesson_title, l.theory AS lesson_theory, t.slug AS topic_slug, t.title AS topic_title, "
    "(lc.lesson_slug IS NOT NULL AND COALESCE(ep.solved, 0) = 1) AS done "
    "FROM exercises e JOIN lessons l ON l.id = e.lesson_id JOIN modules m ON m.id = l.module_id "
    "JOIN topics t ON t.id = m.topic_id "
    "LEFT JOIN lesson_completions lc ON lc.lesson_slug = l.slug AND lc.user_id = ? "
    "LEFT JOIN exercise_progress ep ON ep.exercise_slug = e.slug AND ep.user_id = ?"
)
TRAINING_MAX = 100


@app.get("/api/training/topics")
def training_topics(user: User):
    """Все темы: available — решённые задания пройденных уроков, total — все задания темы.
    passed — пройден ли в теме хотя бы один урок."""
    uid = user["id"]
    with transaction() as conn:
        rows = conn.execute(
            f"SELECT t.slug, t.title, t.icon, t.color, t.group_name, SUM(x.done) AS available, COUNT(*) AS total "
            f"FROM ({_TRAINING_SQL}) x JOIN topics t ON t.slug = x.topic_slug "
            "GROUP BY t.id ORDER BY t.position, t.id", (uid, uid)
        ).fetchall()
    return [{"slug": r["slug"], "title": r["title"], "icon": r["icon"], "color": r["color"],
             "group": r["group_name"], "available": r["available"], "total": r["total"],
             "passed": r["available"] > 0} for r in rows]


class TrainingIn(BaseModel):
    topics: list[str] = Field(min_length=1, max_length=200)
    count: int = Field(ge=1, le=TRAINING_MAX)
    include_unfinished: bool = False     # в пройденных темах брать и непройденные уроки


@app.post("/api/training/start")
def training_start(body: TrainingIn, user: User):
    uid = user["id"]
    with transaction() as conn:
        progress = _progress(conn, uid)
        marks = ", ".join("?" * len(body.topics))
        rows = conn.execute(f"{_TRAINING_SQL} WHERE t.slug IN ({marks})", (uid, uid, *body.topics)).fetchall()
    passed = {r["topic_slug"] for r in rows if r["done"]}
    # Пройденная тема — только решённое (или всё, если просили непройденные уроки); непройденная — всё.
    rows = [r for r in rows if r["done"] or body.include_unfinished or r["topic_slug"] not in passed]
    if not rows:
        raise HTTPException(400, "В выбранных темах нет заданий")
    picked = random.sample(rows, min(body.count, len(rows)))
    exercises = []
    for e in picked:
        item = _public_exercise(e, progress)
        # В тренировке задание решается с чистого листа, а к нему — шпаргалка его урока.
        item.update(solved=False, answer="", draft="", cheat=e["lesson_theory"],
                    lesson_title=e["lesson_title"], topic_title=e["topic_title"], warmup=not e["done"])
        exercises.append(item)
    return {"exercises": exercises, "available": len(rows)}


@app.get("/api/achievements")
def achievements(user: User):
    with transaction() as conn:
        earned = {(r["kind"], r["slug"]): r["earned_at"]
                  for r in conn.execute("SELECT * FROM trophies WHERE user_id = ?", (user["id"],))}
        trophies = []
        for t in conn.execute("SELECT * FROM topics ORDER BY position, id"):
            mods = [
                {"title": m["title"], "icon": m["icon"], "earned_at": earned.get(("module", m["slug"]))}
                for m in conn.execute(
                    "SELECT * FROM modules WHERE topic_id = ? ORDER BY position, id", (t["id"],))
            ]
            trophies.append({"id": t["id"], "slug": t["slug"], "title": t["title"], "icon": t["icon"], "color": t["color"],
                             "earned_at": earned.get(("topic", t["slug"])), "modules": mods})
        return {"achievements": game.achievements_view(conn, user["id"]), "trophies": trophies}


ACTIVITY_DAYS = 365


@app.get("/api/stats")
def stats(user: User):
    uid = user["id"]
    with transaction() as conn:
        s = game.stats(conn, uid)
        # Год активности; период календаря (месяц … год) выбирается на странице.
        start = game.today() - timedelta(days=ACTIVITY_DAYS - 1)
        days = {r["day"]: dict(r) for r in conn.execute(
            "SELECT * FROM daily_activity WHERE user_id = ? AND day >= ?", (uid, start.isoformat()))}
        activity = []
        for i in range(ACTIVITY_DAYS):
            d = (start + timedelta(days=i)).isoformat()
            row = days.get(d, {})
            activity.append({"day": d, "xp": row.get("xp", 0), "goal_met": bool(row.get("goal_met")),
                             "frozen": bool(row.get("frozen")) and not row.get("xp")})
        s["accuracy"] = round(100 * s["correct"] / s["attempts"]) if s["attempts"] else None
        s["activity"] = activity
        s["goals"] = game.next_goals(conn, uid, s)
        s["facts"] = game.fun_facts(conn, uid)
        s["state"] = game.get_state(conn, uid)
        return s


class SettingsIn(BaseModel):
    daily_goal: int | None = Field(None, ge=5, le=500)
    hearts_enabled: bool | None = None
    sequential_lessons: bool | None = None
    theme: Literal["light", "dark"] | None = None
    path_view: Literal["zigzag", "list"] | None = None


@app.put("/api/settings")
def settings(body: SettingsIn, user: User):
    uid = user["id"]
    with transaction() as conn:
        game.get_state(conn, uid)   # гарантирует строку user_state
        for key, value in body.model_dump(exclude_none=True).items():
            conn.execute(f"UPDATE user_state SET {key} = ? WHERE user_id = ?", (value, uid))
        if body.hearts_enabled is False:
            conn.execute("UPDATE user_state SET hearts = ? WHERE user_id = ?", (game.MAX_HEARTS, uid))
        return game.get_state(conn, uid)


@app.post("/api/onboarding/done")
def onboarding_done(user: User):
    """Приветствие новичка показано — больше не показывать (на любом устройстве)."""
    with transaction() as conn:
        game.get_state(conn, user["id"])
        conn.execute("UPDATE user_state SET onboarded = 1 WHERE user_id = ?", (user["id"],))
        return game.get_state(conn, user["id"])


class ResetIn(BaseModel):
    confirm: Literal["RESET"]


@app.post("/api/progress/reset")
def reset_progress(_body: ResetIn, user: User):
    with transaction() as conn:
        for table in PROGRESS_TABLES:
            conn.execute(f"DELETE FROM {table} WHERE user_id = ?", (user["id"],))
        return game.get_state(conn, user["id"])


# =================== Админка ===================

@app.get("/api/admin/users")
def admin_users(_admin: Admin):
    with transaction() as conn:
        rows = conn.execute("SELECT username, is_admin FROM users ORDER BY is_admin DESC, username_key").fetchall()
    return [{"username": r["username"], "is_admin": bool(r["is_admin"])} for r in rows]


class AdminRoleIn(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    is_admin: bool


@app.post("/api/admin/users/role")
def admin_set_role(body: AdminRoleIn, admin: Admin):
    with transaction() as conn:
        target = auth.find_user(conn, body.username.strip())
        if target and target["id"] == admin["id"] and not body.is_admin:
            raise HTTPException(400, "Нельзя снять права администратора с самого себя")
        try:
            user = auth.set_admin(conn, body.username.strip(), body.is_admin)
        except auth.AuthError as e:
            raise HTTPException(e.status, e.message) from None
    logging.getLogger("codequest").info("admin %s: «%s» is_admin=%s", admin["username"], user["username"], body.is_admin)
    return {"username": user["username"], "is_admin": body.is_admin}


@app.get("/api/admin/tree")
def admin_tree(_admin: Admin):
    with transaction() as conn:
        tree = []
        for t in conn.execute("SELECT * FROM topics ORDER BY position, id"):
            mods = []
            for m in conn.execute("SELECT * FROM modules WHERE topic_id = ? ORDER BY position, id", (t["id"],)):
                lessons = []
                for l in conn.execute("SELECT * FROM lessons WHERE module_id = ? ORDER BY position, id", (m["id"],)):
                    exs = [dict(e) for e in conn.execute(
                        "SELECT * FROM exercises WHERE lesson_id = ? ORDER BY position, id", (l["id"],))]
                    lessons.append({**dict(l), "exercises": exs})
                mods.append({**dict(m), "lessons": lessons})
            tree.append({**dict(t), "modules": mods})
        return tree


class ValidateIn(BaseModel):
    type: Literal["code", "output"]
    code: str = ""
    tests: str = ""
    solution: str = ""


@app.post("/api/admin/validate")
def admin_validate(body: ValidateIn, _admin: Admin):
    """code: прогнать эталонное решение через тесты. output: вычислить вывод кода."""
    if body.type == "code":
        return runner.run(body.solution, body.tests).to_dict()
    return runner.run(body.code).to_dict()


@app.post("/api/admin/import")
def admin_import(pkg: content.Package, _admin: Admin):
    with transaction() as conn:
        return content.import_package(conn, pkg)


@app.get("/api/admin/export")
def admin_export(_admin: Admin):
    with transaction() as conn:
        return content.export_package(conn)


# kind → (таблица, родительское поле, редактируемые поля)
KINDS = {
    "topics": ("topics", None, ["title", "description", "icon", "color", "group_name"]),
    "modules": ("modules", "topic_id", ["title", "description", "icon"]),
    "lessons": ("lessons", "module_id", ["title", "theory", "theory_full", "quiz"]),
    "exercises": ("exercises", "lesson_id", ["type", "prompt", "code", "starter_code", "tests",
                                             "expected_output", "solution", "hint", "explain", "xp"]),
}


def _kind(kind: str):
    if kind not in KINDS:
        raise HTTPException(404, "Неизвестный тип")
    return KINDS[kind]


def _clean_quiz(data: dict) -> None:
    """Вопросы «Проверь себя» приходят из админки JSON-текстом — проверяем и храним строкой."""
    if "quiz" not in data:
        return
    raw = data["quiz"]
    try:
        items = json.loads(raw or "[]") if isinstance(raw, str) else raw
        data["quiz"] = json.dumps([content.QuizQuestion.model_validate(q).model_dump() for q in items],
                                  ensure_ascii=False)
    except Exception as e:
        raise HTTPException(400, f"Вопросы «Проверь себя»: неверный формат — {e}")


@app.post("/api/admin/{kind}")
def admin_create(kind: str, body: dict, _admin: Admin):
    table, parent, fields = _kind(kind)
    data = {k: body[k] for k in fields if k in body}
    _clean_quiz(data)
    if not str(data.get("title", data.get("prompt", ""))).strip():
        raise HTTPException(400, "Заполни название / условие")
    if kind == "exercises" and data.get("type") not in ("code", "output", "command"):
        raise HTTPException(400, "type должен быть code, output или command")
    with transaction() as conn:
        where, args = "", ()
        if parent:
            if not body.get(parent):
                raise HTTPException(400, f"Нужен {parent}")
            data[parent] = int(body[parent])
            where, args = f"WHERE {parent} = ?", (data[parent],)
        data["position"] = conn.execute(
            f"SELECT COALESCE(MAX(position), -1) + 1 FROM {table} {where}", args).fetchone()[0]
        data["slug"] = content.new_slug(kind[:-1])
        cols = ", ".join(data)
        cur = conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({', '.join('?' * len(data))})",
                           tuple(data.values()))
        return dict(_get(conn, table, cur.lastrowid))


@app.put("/api/admin/{kind}/{item_id}")
def admin_update(kind: str, item_id: int, body: dict, _admin: Admin):
    table, _parent, fields = _kind(kind)
    data = {k: body[k] for k in fields if k in body}
    if not data:
        raise HTTPException(400, "Нечего обновлять")
    _clean_quiz(data)
    with transaction() as conn:
        _get(conn, table, item_id)
        sets = ", ".join(f"{k} = ?" for k in data)
        conn.execute(f"UPDATE {table} SET {sets} WHERE id = ?", (*data.values(), item_id))
        return dict(_get(conn, table, item_id))


@app.delete("/api/admin/{kind}/{item_id}")
def admin_delete(kind: str, item_id: int, _admin: Admin):
    table, _parent, _fields = _kind(kind)
    with transaction() as conn:
        _get(conn, table, item_id)
        conn.execute(f"DELETE FROM {table} WHERE id = ?", (item_id,))
        return {"ok": True}


class MoveIn(BaseModel):
    direction: Literal[-1, 1]


@app.post("/api/admin/{kind}/{item_id}/move")
def admin_move(kind: str, item_id: int, body: MoveIn, _admin: Admin):
    table, parent, _fields = _kind(kind)
    with transaction() as conn:
        item = _get(conn, table, item_id)
        where, args = ("", ()) if not parent else (f"WHERE {parent} = ?", (item[parent],))
        siblings = [r["id"] for r in conn.execute(
            f"SELECT id FROM {table} {where} ORDER BY position, id", args)]
        i = siblings.index(item_id)
        j = i + body.direction
        if 0 <= j < len(siblings):
            siblings[i], siblings[j] = siblings[j], siblings[i]
            for pos, sid in enumerate(siblings):
                conn.execute(f"UPDATE {table} SET position = ? WHERE id = ?", (pos, sid))
        return {"ok": True}


# =================== Фронтенд ===================

app.mount("/static", StaticFiles(directory=STATIC), name="static")

SHELL_EXT = {".html", ".css", ".js", ".png", ".webp", ".woff2", ".webmanifest"}


def _shell_files() -> list[Path]:
    return sorted(p for p in STATIC.rglob("*") if p.suffix in SHELL_EXT and p.name != "sw.js")


@app.get("/sw.js")
def service_worker():
    """Service worker должен жить в корне, чтобы управлять всем сайтом. Версия — хеш файлов
    фронтенда: изменился любой файл — браузер ставит новый worker и обновляет кэш."""
    files = _shell_files()
    digest = hashlib.sha256()
    for f in files:
        digest.update(f.read_bytes())
    shell = ["/"] + [f"/static/{f.relative_to(STATIC).as_posix()}" for f in files if f.name != "index.html"]
    js = ((STATIC / "sw.js").read_text(encoding="utf-8")
          .replace("__VERSION__", digest.hexdigest()[:12])
          .replace("__SHELL__", json.dumps(shell)))
    return Response(js, media_type="application/javascript", headers={"Cache-Control": "no-cache"})


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse(STATIC / "icons" / "favicon-32.png", media_type="image/png")


@app.get("/manifest.webmanifest")
def manifest():
    return FileResponse(STATIC / "manifest.webmanifest", media_type="application/manifest+json",
                        headers={"Cache-Control": "no-cache"})


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html", headers={"Cache-Control": "no-cache"})
