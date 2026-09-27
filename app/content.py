"""Контент: темы → модули → уроки → задания.

Два способа наполнения пишут в одни и те же таблицы:
  * админ-панель (CRUD по одному элементу);
  * импорт JSON-пакета (content/*.json) — upsert по slug.

Slug — стабильный ключ. Прогресс привязан к slug, поэтому переимпорт
обновлённого пакета не сбрасывает прогресс, а удаление/добавление через
админку не ломает импорт.
"""
import uuid
from typing import Literal

import json

from pydantic import BaseModel, Field, model_validator


class ExerciseIn(BaseModel):
    slug: str
    type: Literal["code", "output"]
    prompt: str
    code: str = ""
    starter_code: str = ""
    tests: str = ""
    expected_output: str = ""
    solution: str = ""
    hint: str = ""
    xp: int = Field(10, ge=1, le=100)


class QuizQuestion(BaseModel):
    """Вопрос «Проверь себя»: без штрафов и XP, с объяснением после ответа."""
    q: str
    options: list[str] = Field(min_length=2)
    answer: int = Field(ge=0)          # индекс правильного варианта
    explain: str = ""

    @model_validator(mode="after")
    def _answer_in_range(self):
        if self.answer >= len(self.options):
            raise ValueError("answer указывает за пределы options")
        return self


class LessonIn(BaseModel):
    slug: str
    title: str
    theory: str = ""
    theory_full: str = ""              # подробный урок: markdown, ```python-блоки запускаются
    quiz: list[QuizQuestion] = []
    exercises: list[ExerciseIn] = []


class ModuleIn(BaseModel):
    slug: str
    title: str
    description: str = ""
    icon: str = "⭐"
    lessons: list[LessonIn] = []


class TopicIn(BaseModel):
    slug: str
    title: str
    description: str = ""
    icon: str = "🐍"
    color: str = "#58cc02"
    group: str = ""          # группа в каталоге тем, например «Python»
    modules: list[ModuleIn] = []


class Package(BaseModel):
    topics: list[TopicIn]


def new_slug(kind: str) -> str:
    return f"{kind}-{uuid.uuid4().hex[:10]}"


def _upsert(conn, table: str, slug: str, fields: dict) -> tuple[int, bool]:
    row = conn.execute(f"SELECT id FROM {table} WHERE slug = ?", (slug,)).fetchone()
    if row:
        sets = ", ".join(f"{k} = ?" for k in fields)
        conn.execute(f"UPDATE {table} SET {sets} WHERE id = ?", (*fields.values(), row["id"]))
        return row["id"], False
    cols = ", ".join(["slug", *fields])
    marks = ", ".join("?" * (len(fields) + 1))
    cur = conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({marks})", (slug, *fields.values()))
    return cur.lastrowid, True


def import_package(conn, pkg: Package) -> dict:
    stats = {"created": 0, "updated": 0}

    def count(created: bool):
        stats["created" if created else "updated"] += 1

    next_topic_pos = conn.execute("SELECT COALESCE(MAX(position), -1) + 1 FROM topics").fetchone()[0]
    for t in pkg.topics:
        existing = conn.execute("SELECT position FROM topics WHERE slug = ?", (t.slug,)).fetchone()
        pos = existing["position"] if existing else next_topic_pos
        if not existing:
            next_topic_pos += 1
        topic_id, c = _upsert(conn, "topics", t.slug, {
            "title": t.title, "description": t.description, "icon": t.icon,
            "color": t.color, "group_name": t.group, "position": pos,
        })
        count(c)
        for mi, m in enumerate(t.modules):
            module_id, c = _upsert(conn, "modules", m.slug, {
                "topic_id": topic_id, "title": m.title, "description": m.description,
                "icon": m.icon, "position": mi,
            })
            count(c)
            for li, l in enumerate(m.lessons):
                lesson_id, c = _upsert(conn, "lessons", l.slug, {
                    "module_id": module_id, "title": l.title, "theory": l.theory,
                    "theory_full": l.theory_full,
                    "quiz": json.dumps([q.model_dump() for q in l.quiz], ensure_ascii=False),
                    "position": li,
                })
                count(c)
                for ei, e in enumerate(l.exercises):
                    data = e.model_dump(exclude={"slug"})
                    _, c = _upsert(conn, "exercises", e.slug, {
                        "lesson_id": lesson_id, **data, "position": ei,
                    })
                    count(c)
    return stats


def export_package(conn) -> dict:
    topics = []
    for t in conn.execute("SELECT * FROM topics ORDER BY position, id"):
        mods = []
        for m in conn.execute("SELECT * FROM modules WHERE topic_id = ? ORDER BY position, id", (t["id"],)):
            lessons = []
            for l in conn.execute("SELECT * FROM lessons WHERE module_id = ? ORDER BY position, id", (m["id"],)):
                exs = [
                    {k: e[k] for k in ExerciseIn.model_fields}
                    for e in conn.execute(
                        "SELECT * FROM exercises WHERE lesson_id = ? ORDER BY position, id", (l["id"],)
                    )
                ]
                lessons.append({"slug": l["slug"], "title": l["title"], "theory": l["theory"],
                                "theory_full": l["theory_full"], "quiz": json.loads(l["quiz"] or "[]"),
                                "exercises": exs})
            mods.append({"slug": m["slug"], "title": m["title"], "description": m["description"],
                         "icon": m["icon"], "lessons": lessons})
        topics.append({"slug": t["slug"], "title": t["title"], "description": t["description"],
                       "icon": t["icon"], "color": t["color"], "group": t["group_name"],
                       "modules": mods})
    return {"topics": topics}


def learning_path(conn) -> list:
    """Карта пути. Внутри темы уроки открываются последовательно;
    темы независимы друг от друга — можно учить несколько параллельно."""
    done = {r["lesson_slug"]: r for r in conn.execute("SELECT * FROM lesson_completions")}
    trophies = {(r["kind"], r["slug"]) for r in conn.execute("SELECT kind, slug FROM trophies")}
    solved = {
        r["exercise_slug"]
        for r in conn.execute("SELECT exercise_slug FROM exercise_progress WHERE solved = 1")
    }
    result = []
    for t in conn.execute("SELECT * FROM topics ORDER BY position, id"):
        prev_done = True
        modules, total, completed = [], 0, 0
        for m in conn.execute("SELECT * FROM modules WHERE topic_id = ? ORDER BY position, id", (t["id"],)):
            lessons = []
            for l in conn.execute("SELECT * FROM lessons WHERE module_id = ? ORDER BY position, id", (m["id"],)):
                ex_slugs = [r[0] for r in conn.execute(
                    "SELECT slug FROM exercises WHERE lesson_id = ?", (l["id"],))]
                is_done = l["slug"] in done
                status = "done" if is_done else ("current" if prev_done else "locked")
                lessons.append({
                    "id": l["id"], "title": l["title"], "status": status,
                    "perfect": bool(done[l["slug"]]["perfect"]) if is_done else False,
                    "exercises": len(ex_slugs),
                    "solved": sum(1 for s in ex_slugs if s in solved),
                })
                prev_done = is_done
                total += 1
                completed += is_done
            modules.append({
                "id": m["id"], "title": m["title"], "description": m["description"],
                "icon": m["icon"], "lessons": lessons,
                "trophy": ("module", m["slug"]) in trophies,
            })
        result.append({
            "id": t["id"], "title": t["title"], "description": t["description"],
            "icon": t["icon"], "color": t["color"], "group": t["group_name"], "modules": modules,
            "total": total, "completed": completed,
            "trophy": ("topic", t["slug"]) in trophies,
        })
    return result


def lesson_is_unlocked(conn, lesson_id: int) -> bool:
    for topic in learning_path(conn):
        for m in topic["modules"]:
            for l in m["lessons"]:
                if l["id"] == lesson_id:
                    return l["status"] != "locked"
    return False


def continue_target(conn) -> dict | None:
    """Куда ведёт плашка «Продолжить»: последний открытый урок, если он не пройден,
    иначе следующий открытый урок той же темы. Если ничего не начато — первый урок первой темы."""
    last = conn.execute("SELECT last_lesson_slug FROM user_state WHERE id = 1").fetchone()[0]
    if not last:  # урок ещё не открывали после обновления — берём урок последнего решённого задания
        row = conn.execute(
            "SELECT l.slug FROM exercise_progress ep JOIN exercises e ON e.slug = ep.exercise_slug "
            "JOIN lessons l ON l.id = e.lesson_id WHERE ep.solved_at IS NOT NULL "
            "ORDER BY ep.solved_at DESC LIMIT 1"
        ).fetchone()
        last = row["slug"] if row else None
    path = learning_path(conn)
    last_topic = None
    if last:
        row = conn.execute("SELECT id FROM lessons WHERE slug = ?", (last,)).fetchone()
        for t in path:
            for m in t["modules"]:
                for l in m["lessons"]:
                    if row and l["id"] == row["id"]:
                        last_topic = t
                        if l["status"] != "done":
                            return _target(t, m, l, started=True)
    for t in ([last_topic] if last_topic else []) + path:
        for m in t["modules"]:
            for l in m["lessons"]:
                if l["status"] == "current":
                    return _target(t, m, l, started=bool(last))
    return None


def _target(t, m, l, started: bool) -> dict:
    return {
        "started": started,
        "topic": {"id": t["id"], "title": t["title"], "icon": t["icon"], "color": t["color"]},
        "module": m["title"],
        "lesson": {"id": l["id"], "title": l["title"], "solved": l["solved"], "exercises": l["exercises"]},
    }
