"""Игровая логика: XP, уровни, streak, сердечки, дневная цель, награды, достижения.

Все функции принимают открытое соединение и id пользователя (uid) и работают
внутри транзакции вызывающего кода. Время берётся через now() — тесты подменяют его.
"""
import sqlite3
from datetime import date, datetime, timedelta

MAX_HEARTS = 5
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

def _state(conn, uid: int) -> sqlite3.Row:
    conn.execute("INSERT OR IGNORE INTO user_state (user_id) VALUES (?)", (uid,))
    return conn.execute("SELECT * FROM user_state WHERE user_id = ?", (uid,)).fetchone()


def _counter(conn, uid: int, name: str) -> int:
    row = conn.execute(
        "SELECT value FROM counters WHERE user_id = ? AND name = ?", (uid, name)
    ).fetchone()
    return row["value"] if row else 0


def _bump(conn, uid: int, name: str, by: int = 1) -> None:
    conn.execute(
        "INSERT INTO counters (user_id, name, value) VALUES (?, ?, ?) "
        "ON CONFLICT(user_id, name) DO UPDATE SET value = value + excluded.value",
        (uid, name, by),
    )


def _day_add(conn, uid: int, column: str, amount: int) -> None:
    conn.execute(
        f"INSERT INTO daily_activity (user_id, day, {column}) VALUES (?, ?, ?) "
        f"ON CONFLICT(user_id, day) DO UPDATE SET {column} = {column} + excluded.{column}",
        (uid, today().isoformat(), amount),
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


def get_state(conn, uid: int) -> dict:
    st = _state(conn, uid)
    streak, at_risk = _displayed_streak(st)
    day = conn.execute(
        "SELECT xp FROM daily_activity WHERE user_id = ? AND day = ?", (uid, today().isoformat())
    ).fetchone()
    monday = today() - timedelta(days=today().weekday())
    active = {r["day"] for r in conn.execute(
        "SELECT day FROM daily_activity WHERE user_id = ? AND day >= ? AND xp > 0", (uid, monday.isoformat()))}
    return {
        "xp": st["xp"],
        **level_info(st["xp"]),
        "hearts": st["hearts"],
        "max_hearts": MAX_HEARTS,
        "hearts_enabled": bool(st["hearts_enabled"]),
        "sequential_lessons": bool(st["sequential_lessons"]),
        "onboarded": bool(st["onboarded"]),
        "streak": streak,
        "streak_at_risk": at_risk,
        "longest_streak": st["longest_streak"],
        "freezes": st["freezes"],
        "daily_goal": st["daily_goal"],
        "today_xp": day["xp"] if day else 0,
        "week": [(monday + timedelta(days=i)).isoformat() in active for i in range(7)],  # занятия пн…вс этой недели
        "theme": st["theme"],
        "path_view": st["path_view"],
        "review_count": conn.execute(
            "SELECT COUNT(*) FROM exercise_progress ep JOIN exercises e ON e.slug = ep.exercise_slug "
            "WHERE ep.user_id = ? AND ep.in_review = 1", (uid,)
        ).fetchone()[0],
    }


# ---------- XP и streak ----------

def _touch_streak(conn, uid: int, events: list) -> None:
    st = _state(conn, uid)
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
        "freezes = ?, last_active_date = ? WHERE user_id = ?",
        (streak, streak, freezes, t.isoformat(), uid),
    )


def add_xp(conn, uid: int, amount: int, events: list, reason: str) -> None:
    if amount <= 0:
        return
    before = level_info(_state(conn, uid)["xp"])["level"]
    _touch_streak(conn, uid, events)
    conn.execute("UPDATE user_state SET xp = xp + ? WHERE user_id = ?", (amount, uid))
    _day_add(conn, uid, "xp", amount)
    events.append({"type": "xp", "amount": amount, "reason": reason})

    st = _state(conn, uid)
    day = today().isoformat()
    row = conn.execute(
        "SELECT xp, goal_met FROM daily_activity WHERE user_id = ? AND day = ?", (uid, day)
    ).fetchone()
    if not row["goal_met"] and row["xp"] >= st["daily_goal"]:
        conn.execute("UPDATE daily_activity SET goal_met = 1 WHERE user_id = ? AND day = ?",
                     (uid, day))
        events.append({"type": "goal_met", "goal": st["daily_goal"]})
    after = level_info(st["xp"])["level"]
    if after > before:
        events.append({"type": "level_up", "level": after})


# ---------- ответы ----------

class NoHearts(Exception):
    pass


def record_answer(conn, uid: int, ex: sqlite3.Row, correct: bool, answer: str, mode: str) -> list:
    """mode:
    'lesson'   — обычное прохождение: ошибка стоит сердечко и попадает в повторение;
    'review'   — работа над ошибками: сердечки не тратятся; исправленное задание возвращает
                 столько сердечек, сколько на нём было потеряно (со временем они не восстанавливаются);
    'practice' — «решить заново» уже решённое задание: ошибка ничего не отнимает;
    'warmup'   — тренировка на непройденном материале: задание не засчитывается и прогресс урока
                 не меняется, верный ответ даёт только XP_PRACTICE, ошибка ничего не отнимает."""
    events: list = []
    if mode == "warmup":
        _bump(conn, uid, "attempts")
        if correct:
            _bump(conn, uid, "correct")
            add_xp(conn, uid, XP_PRACTICE, events, "practice")
        return events
    st = _state(conn, uid)
    hearts_on = bool(st["hearts_enabled"])
    if mode == "lesson" and hearts_on and st["hearts"] <= 0:
        raise NoHearts()

    key = (uid, ex["slug"])
    conn.execute(
        "INSERT OR IGNORE INTO exercise_progress (user_id, exercise_slug) VALUES (?, ?)", key
    )
    prog = conn.execute(
        "SELECT * FROM exercise_progress WHERE user_id = ? AND exercise_slug = ?", key
    ).fetchone()
    _bump(conn, uid, "attempts")

    if correct:
        _bump(conn, uid, "correct")
        conn.execute(
            "UPDATE exercise_progress SET last_answer = ?, draft = '' "
            "WHERE user_id = ? AND exercise_slug = ?",
            (answer, *key),
        )
        if not prog["solved"]:
            conn.execute(
                "UPDATE exercise_progress SET solved = 1, solved_at = ? "
                "WHERE user_id = ? AND exercise_slug = ?",
                (now().isoformat(), *key),
            )
            _bump(conn, uid, "solved")
            if ex["type"] == "code":
                _bump(conn, uid, "code_solved")
            add_xp(conn, uid, ex["xp"], events, "exercise")
        elif mode == "review" and prog["in_review"]:
            add_xp(conn, uid, XP_REVIEW_FIX, events, "review_fix")
        else:
            add_xp(conn, uid, XP_PRACTICE, events, "practice")

        if mode == "review" and prog["in_review"]:
            conn.execute(
                "UPDATE exercise_progress SET in_review = 0, hearts_lost = 0 "
                "WHERE user_id = ? AND exercise_slug = ?",
                key,
            )
            _bump(conn, uid, "review_fixed")
            back = min(prog["hearts_lost"], MAX_HEARTS - st["hearts"]) if hearts_on else 0
            if back > 0:
                conn.execute("UPDATE user_state SET hearts = hearts + ? WHERE user_id = ?", (back, uid))
                events.append({"type": "heart_restored", "amount": back})
        if 0 <= now().hour < 5:
            _bump(conn, uid, "night_solves")
        _day_add(conn, uid, "solved", 1)
    elif mode == "practice":
        pass  # перерешивание решённого: без штрафов и без попадания в повторение
    else:
        conn.execute(
            "UPDATE exercise_progress SET mistakes = mistakes + 1, in_review = 1 "
            "WHERE user_id = ? AND exercise_slug = ?",
            key,
        )
        _day_add(conn, uid, "mistakes", 1)
        if mode == "lesson" and hearts_on:
            conn.execute("UPDATE user_state SET hearts = MAX(0, hearts - 1) WHERE user_id = ?",
                         (uid,))
            # запоминаем, сколько сердечек стоило задание: исправив его в повторении, их вернёшь
            conn.execute("UPDATE exercise_progress SET hearts_lost = hearts_lost + 1 "
                         "WHERE user_id = ? AND exercise_slug = ?", key)
            events.append({"type": "heart_lost"})

    events += check_achievements(conn, uid)
    return events


# ---------- завершение урока, награды за модули и темы ----------

class LessonNotFinished(Exception):
    pass


def complete_lesson(conn, uid: int, lesson: sqlite3.Row, mistakes: int) -> list:
    events: list = []
    # Урок можно завершить, когда каждое задание решено или уже попало в работу над ошибками
    # (была попытка с ошибкой) — нерешённые дорешиваются там.
    rows = conn.execute(
        "SELECT COALESCE(ep.solved, 0) AS solved, COALESCE(ep.in_review, 0) AS in_review "
        "FROM exercises e LEFT JOIN exercise_progress ep "
        "ON ep.exercise_slug = e.slug AND ep.user_id = ? WHERE e.lesson_id = ?",
        (uid, lesson["id"]),
    ).fetchall()
    if any(not r["solved"] and not r["in_review"] for r in rows):
        raise LessonNotFinished()
    unsolved = sum(1 for r in rows if not r["solved"])

    perfect = mistakes == 0 and unsolved == 0
    prev = conn.execute(
        "SELECT * FROM lesson_completions WHERE user_id = ? AND lesson_slug = ?",
        (uid, lesson["slug"]),
    ).fetchone()
    if prev is None:
        conn.execute(
            "INSERT INTO lesson_completions (user_id, lesson_slug, completed_at, perfect) "
            "VALUES (?, ?, ?, ?)",
            (uid, lesson["slug"], now().isoformat(), int(perfect)),
        )
        add_xp(conn, uid, XP_LESSON_FIRST, events, "lesson")
    else:
        conn.execute(
            "UPDATE lesson_completions SET times = times + 1, perfect = MAX(perfect, ?) "
            "WHERE user_id = ? AND lesson_slug = ?",
            (int(perfect), uid, lesson["slug"]),
        )
        add_xp(conn, uid, XP_LESSON_REPEAT, events, "lesson_repeat")
    if perfect:
        _bump(conn, uid, "perfect_lessons")
        add_xp(conn, uid, XP_LESSON_PERFECT, events, "perfect")
        events.append({"type": "perfect"})

    module = conn.execute("SELECT * FROM modules WHERE id = ?", (lesson["module_id"],)).fetchone()
    if _all_lessons_done(conn, uid, "l.module_id = ?", module["id"]):
        if _grant_trophy(conn, uid, "module", module["slug"]):
            add_xp(conn, uid, XP_MODULE, events, "module")
            events.append({"type": "trophy", "kind": "module", "title": module["title"],
                           "icon": module["icon"]})
            topic = conn.execute(
                "SELECT * FROM topics WHERE id = ?", (module["topic_id"],)
            ).fetchone()
            if _all_lessons_done(conn, uid, "m.topic_id = ?", topic["id"]):
                if _grant_trophy(conn, uid, "topic", topic["slug"]):
                    add_xp(conn, uid, XP_TOPIC, events, "topic")
                    events.append({"type": "trophy", "kind": "topic", "title": topic["title"],
                                   "icon": topic["icon"]})

    events += check_achievements(conn, uid)
    return events


def _all_lessons_done(conn, uid: int, where: str, arg) -> bool:
    row = conn.execute(
        "SELECT COUNT(*) AS total, COUNT(lc.lesson_slug) AS done FROM lessons l "
        "JOIN modules m ON m.id = l.module_id "
        "LEFT JOIN lesson_completions lc ON lc.lesson_slug = l.slug AND lc.user_id = ? "
        f"WHERE {where}",
        (uid, arg),
    ).fetchone()
    return row["total"] > 0 and row["total"] == row["done"]


def _grant_trophy(conn, uid: int, kind: str, slug: str) -> bool:
    cur = conn.execute(
        "INSERT OR IGNORE INTO trophies (user_id, kind, slug, earned_at) VALUES (?, ?, ?, ?)",
        (uid, kind, slug, now().isoformat()),
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


def stats(conn, uid: int) -> dict:
    st = _state(conn, uid)
    count = lambda sql: conn.execute(sql, (uid,)).fetchone()[0]  # noqa: E731
    return {
        "xp": st["xp"],
        "level": level_info(st["xp"])["level"],
        "longest_streak": st["longest_streak"],
        "solved": _counter(conn, uid, "solved"),
        "code_solved": _counter(conn, uid, "code_solved"),
        "perfect_lessons": _counter(conn, uid, "perfect_lessons"),
        "review_fixed": _counter(conn, uid, "review_fixed"),
        "night_solves": _counter(conn, uid, "night_solves"),
        "attempts": _counter(conn, uid, "attempts"),
        "correct": _counter(conn, uid, "correct"),
        "lessons": count("SELECT COUNT(*) FROM lesson_completions WHERE user_id = ?"),
        "modules": count("SELECT COUNT(*) FROM trophies WHERE user_id = ? AND kind = 'module'"),
        "topics": count("SELECT COUNT(*) FROM trophies WHERE user_id = ? AND kind = 'topic'"),
        "goal_days": count("SELECT COUNT(*) FROM daily_activity WHERE user_id = ? AND goal_met = 1"),
    }


def check_achievements(conn, uid: int) -> list:
    s = stats(conn, uid)
    have = {r["code"] for r in conn.execute("SELECT code FROM achievements WHERE user_id = ?", (uid,))}
    events = []
    for code, icon, title, desc, (metric, need) in ACHIEVEMENTS:
        if code not in have and s[metric] >= need:
            conn.execute(
                "INSERT INTO achievements (user_id, code, unlocked_at) VALUES (?, ?, ?)",
                (uid, code, now().isoformat()),
            )
            events.append({"type": "achievement", "code": code, "icon": icon,
                           "title": title, "description": desc})
    return events


def achievements_view(conn, uid: int) -> list:
    s = stats(conn, uid)
    got = {r["code"]: r["unlocked_at"]
           for r in conn.execute("SELECT * FROM achievements WHERE user_id = ?", (uid,))}
    return [
        {"code": code, "icon": icon, "title": title, "description": desc,
         "unlocked_at": got.get(code), "progress": min(s[metric], need), "goal": need}
        for code, icon, title, desc, (metric, need) in ACHIEVEMENTS
    ]
