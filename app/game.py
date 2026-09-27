"""Игровая логика: XP, уровни, streak, сердечки, дневная цель, награды, достижения.

Все функции принимают открытое соединение и работают внутри транзакции
вызывающего кода. Время берётся через now() — тесты подменяют его.
"""
import sqlite3
from datetime import date, datetime, timedelta

MAX_HEARTS = 5
HEART_REGEN = timedelta(minutes=30)
MAX_FREEZES = 2
XP_PRACTICE = 2          # повторное решение уже решённого задания
XP_REVIEW_FIX = 5        # исправил ошибку в режиме «Работа над ошибками»
XP_LESSON_FIRST = 10
XP_LESSON_PERFECT = 5
XP_LESSON_REPEAT = 3
XP_MODULE = 20
XP_TOPIC = 50


def now() -> datetime:
    return datetime.now()


def today() -> date:
    return now().date()


# ---------- уровни ----------

def level_threshold(level: int) -> int:
    """Сколько всего XP нужно, чтобы достичь уровня: 1→0, 2→50, 3→150, 4→300…"""
    return 25 * level * (level - 1)


def level_info(xp: int) -> dict:
    level = 1
    while xp >= level_threshold(level + 1):
        level += 1
    start, end = level_threshold(level), level_threshold(level + 1)
    return {"level": level, "level_xp": xp - start, "level_size": end - start}


# ---------- состояние ----------

def _state(conn) -> sqlite3.Row:
    return conn.execute("SELECT * FROM user_state WHERE id = 1").fetchone()


def _counter(conn, name: str) -> int:
    row = conn.execute("SELECT value FROM counters WHERE name = ?", (name,)).fetchone()
    return row["value"] if row else 0


def _bump(conn, name: str, by: int = 1) -> None:
    conn.execute(
        "INSERT INTO counters (name, value) VALUES (?, ?) "
        "ON CONFLICT(name) DO UPDATE SET value = value + excluded.value",
        (name, by),
    )


def refresh_hearts(conn) -> None:
    st = _state(conn)
    if st["hearts"] >= MAX_HEARTS:
        return
    t = now()
    if not st["hearts_updated_at"]:
        conn.execute("UPDATE user_state SET hearts_updated_at = ? WHERE id = 1", (t.isoformat(),))
        return
    updated = datetime.fromisoformat(st["hearts_updated_at"])
    gained = int((t - updated) / HEART_REGEN)
    if gained <= 0:
        return
    hearts = min(MAX_HEARTS, st["hearts"] + gained)
    new_updated = t if hearts == MAX_HEARTS else updated + gained * HEART_REGEN
    conn.execute(
        "UPDATE user_state SET hearts = ?, hearts_updated_at = ? WHERE id = 1",
        (hearts, new_updated.isoformat()),
    )


def _displayed_streak(st) -> tuple[int, bool]:
    """(streak, at_risk). Streak обнуляется только если пропуск не покрыть заморозками."""
    if not st["last_active_date"]:
        return 0, False
    last = date.fromisoformat(st["last_active_date"])
    gap = (today() - last).days
    if gap <= 0:
        return st["streak"], False
    missed = gap - 1
    if missed <= st["freezes"]:
        return st["streak"], True
    return 0, False


def get_state(conn) -> dict:
    refresh_hearts(conn)
    st = _state(conn)
    streak, at_risk = _displayed_streak(st)
    day = conn.execute(
        "SELECT xp FROM daily_activity WHERE day = ?", (today().isoformat(),)
    ).fetchone()
    next_heart_in = None
    if st["hearts"] < MAX_HEARTS and st["hearts_updated_at"]:
        nxt = datetime.fromisoformat(st["hearts_updated_at"]) + HEART_REGEN
        next_heart_in = max(0, int((nxt - now()).total_seconds()))
    return {
        "xp": st["xp"],
        **level_info(st["xp"]),
        "hearts": st["hearts"],
        "max_hearts": MAX_HEARTS,
        "hearts_enabled": bool(st["hearts_enabled"]),
        "next_heart_in": next_heart_in,
        "streak": streak,
        "streak_at_risk": at_risk,
        "longest_streak": st["longest_streak"],
        "freezes": st["freezes"],
        "daily_goal": st["daily_goal"],
        "today_xp": day["xp"] if day else 0,
        "theme": st["theme"],
        "review_count": conn.execute(
            "SELECT COUNT(*) FROM exercise_progress ep JOIN exercises e ON e.slug = ep.exercise_slug "
            "WHERE ep.in_review = 1"
        ).fetchone()[0],
    }


# ---------- XP и streak ----------

def _touch_streak(conn, events: list) -> None:
    st = _state(conn)
    t = today()
    last = date.fromisoformat(st["last_active_date"]) if st["last_active_date"] else None
    if last == t:
        return
    streak, freezes = st["streak"], st["freezes"]
    if last is None:
        streak = 1
    else:
        missed = (t - last).days - 1
        if missed == 0:
            streak += 1
        elif 0 < missed <= freezes:
            freezes -= missed
            streak += 1
            events.append({"type": "freeze_used", "count": missed})
        else:
            streak = 1
    if streak > 1 and streak % 7 == 0 and freezes < MAX_FREEZES:
        freezes += 1
        events.append({"type": "freeze_earned"})
    events.append({"type": "streak", "streak": streak})
    conn.execute(
        "UPDATE user_state SET streak = ?, longest_streak = MAX(longest_streak, ?), "
        "freezes = ?, last_active_date = ? WHERE id = 1",
        (streak, streak, freezes, t.isoformat()),
    )


def add_xp(conn, amount: int, events: list, reason: str) -> None:
    if amount <= 0:
        return
    before = level_info(_state(conn)["xp"])["level"]
    _touch_streak(conn, events)
    conn.execute("UPDATE user_state SET xp = xp + ? WHERE id = 1", (amount,))
    day = today().isoformat()
    conn.execute(
        "INSERT INTO daily_activity (day, xp) VALUES (?, ?) "
        "ON CONFLICT(day) DO UPDATE SET xp = xp + excluded.xp",
        (day, amount),
    )
    events.append({"type": "xp", "amount": amount, "reason": reason})

    st = _state(conn)
    row = conn.execute("SELECT xp, goal_met FROM daily_activity WHERE day = ?", (day,)).fetchone()
    if not row["goal_met"] and row["xp"] >= st["daily_goal"]:
        conn.execute("UPDATE daily_activity SET goal_met = 1 WHERE day = ?", (day,))
        events.append({"type": "goal_met", "goal": st["daily_goal"]})
    after = level_info(st["xp"])["level"]
    if after > before:
        events.append({"type": "level_up", "level": after})


# ---------- ответы ----------

class NoHearts(Exception):
    pass


def record_answer(conn, ex: sqlite3.Row, correct: bool, answer: str, mode: str) -> list:
    """mode:
    'lesson'   — обычное прохождение: ошибка стоит сердечко и попадает в повторение;
    'review'   — работа над ошибками/тренировка: сердечки не тратятся, а возвращаются;
    'practice' — «решить заново» уже решённое задание: ошибка ничего не отнимает."""
    events: list = []
    refresh_hearts(conn)
    st = _state(conn)
    hearts_on = bool(st["hearts_enabled"])
    if mode == "lesson" and hearts_on and st["hearts"] <= 0:
        raise NoHearts()

    conn.execute(
        "INSERT OR IGNORE INTO exercise_progress (exercise_slug) VALUES (?)", (ex["slug"],)
    )
    prog = conn.execute(
        "SELECT * FROM exercise_progress WHERE exercise_slug = ?", (ex["slug"],)
    ).fetchone()
    _bump(conn, "attempts")

    if correct:
        _bump(conn, "correct")
        conn.execute(
            "UPDATE exercise_progress SET last_answer = ?, draft = '' WHERE exercise_slug = ?",
            (answer, ex["slug"]),
        )
        if not prog["solved"]:
            conn.execute(
                "UPDATE exercise_progress SET solved = 1, solved_at = ? WHERE exercise_slug = ?",
                (now().isoformat(), ex["slug"]),
            )
            _bump(conn, "solved")
            if ex["type"] == "code":
                _bump(conn, "code_solved")
            add_xp(conn, ex["xp"], events, "exercise")
        elif mode == "review" and prog["in_review"]:
            add_xp(conn, XP_REVIEW_FIX, events, "review_fix")
        else:
            add_xp(conn, XP_PRACTICE, events, "practice")

        if mode == "review" and prog["in_review"]:
            conn.execute(
                "UPDATE exercise_progress SET in_review = 0 WHERE exercise_slug = ?", (ex["slug"],)
            )
            _bump(conn, "review_fixed")
        if mode == "review" and hearts_on and st["hearts"] < MAX_HEARTS:
            conn.execute("UPDATE user_state SET hearts = hearts + 1 WHERE id = 1")
            events.append({"type": "heart_restored"})
        if 0 <= now().hour < 5:
            _bump(conn, "night_solves")
        conn.execute(
            "INSERT INTO daily_activity (day, solved) VALUES (?, 1) "
            "ON CONFLICT(day) DO UPDATE SET solved = solved + 1",
            (today().isoformat(),),
        )
    elif mode == "practice":
        pass  # перерешивание решённого: без штрафов и без попадания в повторение
    else:
        conn.execute(
            "UPDATE exercise_progress SET mistakes = mistakes + 1, in_review = 1 "
            "WHERE exercise_slug = ?",
            (ex["slug"],),
        )
        conn.execute(
            "INSERT INTO daily_activity (day, mistakes) VALUES (?, 1) "
            "ON CONFLICT(day) DO UPDATE SET mistakes = mistakes + 1",
            (today().isoformat(),),
        )
        if mode == "lesson" and hearts_on:
            if st["hearts"] >= MAX_HEARTS:
                conn.execute(
                    "UPDATE user_state SET hearts_updated_at = ? WHERE id = 1",
                    (now().isoformat(),),
                )
            conn.execute("UPDATE user_state SET hearts = MAX(0, hearts - 1) WHERE id = 1")
            events.append({"type": "heart_lost"})

    events += check_achievements(conn)
    return events


# ---------- завершение урока, награды за модули и темы ----------

class LessonNotFinished(Exception):
    pass


def complete_lesson(conn, lesson: sqlite3.Row, mistakes: int) -> list:
    events: list = []
    unsolved = conn.execute(
        "SELECT COUNT(*) FROM exercises e LEFT JOIN exercise_progress ep ON ep.exercise_slug = e.slug "
        "WHERE e.lesson_id = ? AND COALESCE(ep.solved, 0) = 0",
        (lesson["id"],),
    ).fetchone()[0]
    if unsolved:
        raise LessonNotFinished()

    perfect = mistakes == 0
    prev = conn.execute(
        "SELECT * FROM lesson_completions WHERE lesson_slug = ?", (lesson["slug"],)
    ).fetchone()
    if prev is None:
        conn.execute(
            "INSERT INTO lesson_completions (lesson_slug, completed_at, perfect) VALUES (?, ?, ?)",
            (lesson["slug"], now().isoformat(), int(perfect)),
        )
        add_xp(conn, XP_LESSON_FIRST, events, "lesson")
    else:
        conn.execute(
            "UPDATE lesson_completions SET times = times + 1, perfect = MAX(perfect, ?) "
            "WHERE lesson_slug = ?",
            (int(perfect), lesson["slug"]),
        )
        add_xp(conn, XP_LESSON_REPEAT, events, "lesson_repeat")
    if perfect:
        _bump(conn, "perfect_lessons")
        add_xp(conn, XP_LESSON_PERFECT, events, "perfect")
        events.append({"type": "perfect"})

    module = conn.execute("SELECT * FROM modules WHERE id = ?", (lesson["module_id"],)).fetchone()
    if _all_lessons_done(conn, "l.module_id = ?", module["id"]):
        if _grant_trophy(conn, "module", module["slug"]):
            add_xp(conn, XP_MODULE, events, "module")
            events.append({"type": "trophy", "kind": "module", "title": module["title"],
                           "icon": module["icon"]})
            topic = conn.execute(
                "SELECT * FROM topics WHERE id = ?", (module["topic_id"],)
            ).fetchone()
            if _all_lessons_done(conn, "m.topic_id = ?", topic["id"]):
                if _grant_trophy(conn, "topic", topic["slug"]):
                    add_xp(conn, XP_TOPIC, events, "topic")
                    events.append({"type": "trophy", "kind": "topic", "title": topic["title"],
                                   "icon": topic["icon"]})

    events += check_achievements(conn)
    return events


def _all_lessons_done(conn, where: str, arg) -> bool:
    row = conn.execute(
        "SELECT COUNT(*) AS total, COUNT(lc.lesson_slug) AS done FROM lessons l "
        "JOIN modules m ON m.id = l.module_id "
        "LEFT JOIN lesson_completions lc ON lc.lesson_slug = l.slug "
        f"WHERE {where}",
        (arg,),
    ).fetchone()
    return row["total"] > 0 and row["total"] == row["done"]


def _grant_trophy(conn, kind: str, slug: str) -> bool:
    cur = conn.execute(
        "INSERT OR IGNORE INTO trophies (kind, slug, earned_at) VALUES (?, ?, ?)",
        (kind, slug, now().isoformat()),
    )
    return cur.rowcount == 1


# ---------- достижения ----------

ACHIEVEMENTS = [
    # code, иконка, название, описание, (метрика, порог)
    ("first_step", "👣", "Первый шаг", "Реши первое задание", ("solved", 1)),
    ("solver_25", "🧩", "Решатель", "Реши 25 заданий", ("solved", 25)),
    ("solver_100", "🧠", "Мозговой штурм", "Реши 100 заданий", ("solved", 100)),
    ("coder_10", "⌨️", "Кодер", "Напиши 10 программ, прошедших тесты", ("code_solved", 10)),
    ("coder_50", "💻", "Хакер", "Напиши 50 программ, прошедших тесты", ("code_solved", 50)),
    ("lesson_1", "📘", "Первый урок", "Заверши первый урок", ("lessons", 1)),
    ("lesson_10", "📚", "Книжный червь", "Заверши 10 уроков", ("lessons", 10)),
    ("perfect_1", "💎", "Без единой ошибки", "Пройди урок без ошибок", ("perfect_lessons", 1)),
    ("perfect_10", "👑", "Перфекционист", "10 уроков без ошибок", ("perfect_lessons", 10)),
    ("module_1", "🏅", "Модуль покорён", "Заверши первый модуль", ("modules", 1)),
    ("module_5", "🎖️", "Коллекционер медалей", "Заверши 5 модулей", ("modules", 5)),
    ("topic_1", "🏆", "Мастер темы", "Заверши целую тему", ("topics", 1)),
    ("streak_3", "🔥", "Разогрев", "Серия 3 дня подряд", ("longest_streak", 3)),
    ("streak_7", "🚀", "Неделя огня", "Серия 7 дней подряд", ("longest_streak", 7)),
    ("streak_30", "🌋", "Вулкан", "Серия 30 дней подряд", ("longest_streak", 30)),
    ("goal_1", "🎯", "В яблочко", "Выполни дневную цель", ("goal_days", 1)),
    ("goal_7", "📅", "Дисциплина", "Выполни дневную цель 7 раз", ("goal_days", 7)),
    ("xp_500", "⚡", "Энергия", "Набери 500 XP", ("xp", 500)),
    ("xp_2000", "🌟", "Звезда", "Набери 2000 XP", ("xp", 2000)),
    ("level_5", "🦉", "Мудрая сова", "Достигни 5 уровня", ("level", 5)),
    ("review_10", "🩹", "Работа над ошибками", "Исправь 10 ошибок в повторении", ("review_fixed", 10)),
    ("night_owl", "🌙", "Ночная сова", "Реши задание между полуночью и 5 утра", ("night_solves", 1)),
]


def stats(conn) -> dict:
    st = _state(conn)
    return {
        "xp": st["xp"],
        "level": level_info(st["xp"])["level"],
        "longest_streak": st["longest_streak"],
        "solved": _counter(conn, "solved"),
        "code_solved": _counter(conn, "code_solved"),
        "perfect_lessons": _counter(conn, "perfect_lessons"),
        "review_fixed": _counter(conn, "review_fixed"),
        "night_solves": _counter(conn, "night_solves"),
        "attempts": _counter(conn, "attempts"),
        "correct": _counter(conn, "correct"),
        "lessons": conn.execute("SELECT COUNT(*) FROM lesson_completions").fetchone()[0],
        "modules": conn.execute("SELECT COUNT(*) FROM trophies WHERE kind='module'").fetchone()[0],
        "topics": conn.execute("SELECT COUNT(*) FROM trophies WHERE kind='topic'").fetchone()[0],
        "goal_days": conn.execute(
            "SELECT COUNT(*) FROM daily_activity WHERE goal_met = 1"
        ).fetchone()[0],
    }


def check_achievements(conn) -> list:
    s = stats(conn)
    have = {r["code"] for r in conn.execute("SELECT code FROM achievements")}
    events = []
    for code, icon, title, desc, (metric, need) in ACHIEVEMENTS:
        if code not in have and s[metric] >= need:
            conn.execute(
                "INSERT INTO achievements (code, unlocked_at) VALUES (?, ?)",
                (code, now().isoformat()),
            )
            events.append({"type": "achievement", "code": code, "icon": icon,
                           "title": title, "description": desc})
    return events


def achievements_view(conn) -> list:
    s = stats(conn)
    got = {r["code"]: r["unlocked_at"] for r in conn.execute("SELECT * FROM achievements")}
    return [
        {"code": code, "icon": icon, "title": title, "description": desc,
         "unlocked_at": got.get(code), "progress": min(s[metric], need), "goal": need}
        for code, icon, title, desc, (metric, need) in ACHIEVEMENTS
    ]
