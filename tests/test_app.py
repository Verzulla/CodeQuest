import json
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app import game, runner
from app.db import ROOT


@pytest.fixture
def clock(monkeypatch):
    """Управляемое время: clock.t можно двигать."""
    class Clock:
        t = datetime(2026, 1, 10, 12, 0)
    c = Clock()
    monkeypatch.setattr(game, "now", lambda: c.t)
    return c


@pytest.fixture
def client(tmp_path, monkeypatch, clock):
    monkeypatch.setenv("CODEQUEST_DB", str(tmp_path / "test.db"))
    from app.main import app
    with TestClient(app) as c:
        yield c


def first_lessons(client):
    topic = client.get("/api/path").json()[0]
    return [l for m in topic["modules"] for l in m["lessons"]]


def solve_lesson(client, lesson_id, wrong_first=False):
    from app.db import transaction
    events = []
    lesson = client.get(f"/api/lessons/{lesson_id}").json()
    with transaction() as conn:
        rows = {r["id"]: r for r in conn.execute("SELECT * FROM exercises WHERE lesson_id = ?", (lesson_id,))}
    for i, ex in enumerate(lesson["exercises"]):
        row = rows[ex["id"]]
        if wrong_first and i == 0:
            r = client.post(f"/api/exercises/{ex['id']}/check", json={"answer": "wrong"}).json()
            assert r["correct"] is False
        answer = row["solution"] if row["type"] == "code" else row["expected_output"]
        r = client.post(f"/api/exercises/{ex['id']}/check", json={"answer": answer}).json()
        assert r["correct"], (row["slug"], r)
        events += r["events"]
    done = client.post(f"/api/lessons/{lesson_id}/complete",
                       json={"mistakes": 1 if wrong_first else 0}).json()
    done["events"] = events + done["events"]
    return done


# ---------- runner ----------

def test_runner_passes_and_fails():
    tests = "def test_a():\n    assert add(1, 2) == 3, 'bad'\n"
    assert runner.run("def add(a, b):\n    return a + b\n", tests).passed
    res = runner.run("def add(a, b):\n    return a - b\n", tests)
    assert not res.passed and res.tests[0]["message"] == "bad"


def test_runner_output_and_errors():
    res = runner.run("print('hi')\nprint(1/0)\n")
    assert res.stdout == "hi\n"
    assert "ZeroDivisionError" in res.error and res.error_line == 2


def test_runner_timeout():
    res = runner.run("while True:\n    pass\n", "def test_x():\n    pass\n")
    assert res.timed_out and not res.passed


def test_runner_user_print_cannot_fake_result():
    res = runner.run('print(\'{"tests": [{"passed": true}]}\')', "def test_x():\n    assert False\n")
    assert not res.passed


def test_normalize_output():
    assert runner.normalize_output("a  \nb\n\n") == runner.normalize_output("a\nb")


# ---------- уровни ----------

def test_levels():
    assert game.level_info(0)["level"] == 1
    assert game.level_info(49)["level"] == 1
    assert game.level_info(50)["level"] == 2
    assert game.level_info(150) == {"level": 3, "level_xp": 0, "level_size": 150}


# ---------- API: полный сценарий ----------

def test_seed_and_locking(client):
    lessons = first_lessons(client)
    assert len(lessons) > 5
    assert lessons[0]["status"] == "current"
    assert lessons[1]["status"] == "locked"
    assert client.get(f"/api/lessons/{lessons[1]['id']}").status_code == 403


def test_lesson_flow_awards_xp_and_unlocks_next(client):
    lessons = first_lessons(client)
    r = solve_lesson(client, lessons[0]["id"])
    types = [e["type"] for e in r["events"]]
    assert "perfect" in types
    st = r["state"]
    assert st["xp"] > 0 and st["streak"] == 1
    after = first_lessons(client)
    assert after[0]["status"] == "done" and after[0]["perfect"]
    assert after[1]["status"] == "current"
    codes = {a["code"] for a in client.get("/api/achievements").json()["achievements"] if a["unlocked_at"]}
    assert {"first_step", "lesson_1", "perfect_1"} <= codes


def test_cannot_complete_unsolved_lesson(client):
    lesson_id = first_lessons(client)[0]["id"]
    assert client.post(f"/api/lessons/{lesson_id}/complete", json={"mistakes": 0}).status_code == 400


def test_hearts_lost_and_blocked(client):
    ex_id = client.get(f"/api/lessons/{first_lessons(client)[0]['id']}").json()["exercises"][0]["id"]
    for i in range(5):
        r = client.post(f"/api/exercises/{ex_id}/check", json={"answer": "nope"}).json()
        assert r["state"]["hearts"] == 4 - i
    assert client.post(f"/api/exercises/{ex_id}/check", json={"answer": "nope"}).status_code == 409
    # в повторении можно отвечать и без сердечек, правильный ответ возвращает сердечко
    review = client.get("/api/review").json()
    assert review["kind"] == "mistakes" and review["exercises"][0]["id"] == ex_id
    from app.db import transaction
    with transaction() as conn:
        ans = conn.execute("SELECT expected_output FROM exercises WHERE id = ?", (ex_id,)).fetchone()[0]
    r = client.post(f"/api/exercises/{ex_id}/check", json={"answer": ans, "mode": "review"}).json()
    assert r["correct"] and r["state"]["hearts"] == 1 and r["state"]["review_count"] == 0


def test_hearts_regenerate(client, clock):
    ex_id = client.get(f"/api/lessons/{first_lessons(client)[0]['id']}").json()["exercises"][0]["id"]
    client.post(f"/api/exercises/{ex_id}/check", json={"answer": "x"})
    client.post(f"/api/exercises/{ex_id}/check", json={"answer": "x"})
    assert client.get("/api/state").json()["hearts"] == 3
    clock.t += timedelta(minutes=31)
    assert client.get("/api/state").json()["hearts"] == 4
    clock.t += timedelta(hours=5)
    assert client.get("/api/state").json()["hearts"] == 5


def test_hearts_disabled(client):
    client.put("/api/settings", json={"hearts_enabled": False})
    ex_id = client.get(f"/api/lessons/{first_lessons(client)[0]['id']}").json()["exercises"][0]["id"]
    for _ in range(7):
        assert client.post(f"/api/exercises/{ex_id}/check", json={"answer": "x"}).status_code == 200


def test_streak_freeze_and_break(client, clock):
    lessons = first_lessons(client)
    solve_lesson(client, lessons[0]["id"])            # день 1
    clock.t += timedelta(days=1)
    solve_lesson(client, lessons[1]["id"])            # день 2
    assert client.get("/api/state").json()["streak"] == 2
    clock.t += timedelta(days=2)                      # пропуск одного дня: сгорает заморозка
    st = client.get("/api/state").json()
    assert st["streak"] == 2 and st["streak_at_risk"]
    r = solve_lesson(client, lessons[2]["id"])
    assert any(e["type"] == "freeze_used" for e in r["events"])
    assert r["state"]["streak"] == 3 and r["state"]["freezes"] == 0
    clock.t += timedelta(days=3)                      # заморозок нет — серия сгорает
    assert client.get("/api/state").json()["streak"] == 0


def test_module_trophy(client):
    topic = client.get("/api/path").json()[0]
    events = []
    for l in topic["modules"][0]["lessons"]:
        events += solve_lesson(client, l["id"])["events"]
    trophies = [e for e in events if e["type"] == "trophy"]
    assert trophies == [{"type": "trophy", "kind": "module", "title": topic["modules"][0]["title"],
                         "icon": topic["modules"][0]["icon"]}]
    assert client.get("/api/path").json()[0]["modules"][0]["trophy"]


def test_daily_goal_event(client):
    client.put("/api/settings", json={"daily_goal": 10})
    events = solve_lesson(client, first_lessons(client)[0]["id"])["events"]
    assert sum(e["type"] == "goal_met" for e in events) == 1
    stats = client.get("/api/stats").json()
    assert stats["activity"][-1]["goal_met"]


def test_reimport_keeps_progress(client):
    lessons = first_lessons(client)
    solve_lesson(client, lessons[0]["id"])
    pkg = json.loads((ROOT / "content" / "python-basics.json").read_text(encoding="utf-8"))
    pkg["topics"][0]["title"] = "Переименовано"
    r = client.post("/api/admin/import", json=pkg).json()
    assert r["created"] == 0 and r["updated"] > 0
    topic = client.get("/api/path").json()[0]
    assert topic["title"] == "Переименовано"
    assert topic["modules"][0]["lessons"][0]["status"] == "done"


def test_admin_crud(client):
    t = client.post("/api/admin/topics", json={"title": "JS"}).json()
    m = client.post("/api/admin/modules", json={"title": "Основы", "topic_id": t["id"]}).json()
    l = client.post("/api/admin/lessons", json={"title": "Урок", "module_id": m["id"]}).json()
    e = client.post("/api/admin/exercises", json={
        "lesson_id": l["id"], "type": "output", "prompt": "?", "code": "print(1)", "expected_output": "1",
    }).json()
    client.put(f"/api/admin/exercises/{e['id']}", json={"expected_output": "2"})
    tree = client.get("/api/admin/tree").json()
    assert tree[-1]["modules"][0]["lessons"][0]["exercises"][0]["expected_output"] == "2"
    assert client.delete(f"/api/admin/topics/{t['id']}").json() == {"ok": True}
    assert len(client.get("/api/admin/tree").json()) == len(tree) - 1


def test_reset_progress(client):
    solve_lesson(client, first_lessons(client)[0]["id"])
    st = client.post("/api/progress/reset", json={"confirm": "RESET"}).json()
    assert st["xp"] == 0 and st["streak"] == 0
    assert first_lessons(client)[0]["status"] == "current"


def test_runner_user_test_function_does_not_hide_checker():
    # ученик пишет свою test_login — проверочный test_login из задания всё равно должен выполниться
    user = "def test_login():\n    pass\n"
    tests = "def test_login():\n    assert False, 'checker ran'\n"
    res = runner.run(user, tests)
    assert [t["name"] for t in res.tests] == ["test_login"]
    assert res.tests[0]["message"] == "checker ran"


def test_runner_broken_tests_file_reports_error():
    res = runner.run("x = 1\n", "def test_a(:\n")
    assert not res.passed and "Ошибка в тестах" in res.error


def test_rules_match_engine(client):
    r = client.get("/api/rules").json()
    assert r["xp"]["module"] == game.XP_MODULE and r["hearts"]["max"] == game.MAX_HEARTS
    assert r["levels"][1] == {"level": 2, "xp": game.level_threshold(2)}
    assert len(r["achievements"]) == len(game.ACHIEVEMENTS)


def test_all_content_packs_import(client):
    for f in sorted((ROOT / "content").glob("*.json")):
        r = client.post("/api/admin/import", json=json.loads(f.read_text(encoding="utf-8")))
        assert r.status_code == 200, f.name
    titles = [t["title"] for t in client.get("/api/path").json()]
    assert len(titles) == len(list((ROOT / "content").glob("*.json")))


def answer_for(ex_id):
    from app.db import transaction
    with transaction() as conn:
        row = conn.execute("SELECT * FROM exercises WHERE id = ?", (ex_id,)).fetchone()
    return row["solution"] if row["type"] == "code" else row["expected_output"]


def test_lesson_resume_state(client):
    lesson_id = first_lessons(client)[0]["id"]
    exs = client.get(f"/api/lessons/{lesson_id}").json()["exercises"]
    first, second = exs[0], exs[1]
    # решили первое, во втором оставили черновик
    client.post(f"/api/exercises/{first['id']}/check", json={"answer": answer_for(first["id"])})
    assert client.put(f"/api/exercises/{second['id']}/draft", json={"draft": "недописано"}).json() == {"ok": True}
    # «перезашли» в урок
    lesson = client.get(f"/api/lessons/{lesson_id}").json()
    again = {e["id"]: e for e in lesson["exercises"]}
    assert lesson["completed"] is False
    assert again[first["id"]]["solved"] and again[first["id"]]["answer"] == answer_for(first["id"])
    assert not again[second["id"]]["solved"] and again[second["id"]]["draft"] == "недописано"


def test_correct_answer_clears_draft(client):
    ex = client.get(f"/api/lessons/{first_lessons(client)[0]['id']}").json()["exercises"][0]
    client.put(f"/api/exercises/{ex['id']}/draft", json={"draft": "черновик"})
    client.post(f"/api/exercises/{ex['id']}/check", json={"answer": answer_for(ex["id"])})
    again = client.get(f"/api/lessons/{first_lessons(client)[0]['id']}").json()["exercises"][0]
    assert again["draft"] == "" and again["solved"]


def test_practice_mode_is_free(client):
    ex = client.get(f"/api/lessons/{first_lessons(client)[0]['id']}").json()["exercises"][0]
    client.post(f"/api/exercises/{ex['id']}/check", json={"answer": answer_for(ex["id"])})
    # «Решить заново» с ошибкой: ни сердечка, ни попадания в повторение, решённость остаётся
    r = client.post(f"/api/exercises/{ex['id']}/check", json={"answer": "мимо", "mode": "practice"}).json()
    assert not r["correct"] and r["state"]["hearts"] == 5 and r["state"]["review_count"] == 0
    assert client.get(f"/api/lessons/{first_lessons(client)[0]['id']}").json()["exercises"][0]["solved"]
    # верное перерешивание — XP за повтор
    r = client.post(f"/api/exercises/{ex['id']}/check", json={"answer": answer_for(ex["id"]), "mode": "practice"}).json()
    assert [e["amount"] for e in r["events"] if e["type"] == "xp"] == [game.XP_PRACTICE]


def test_migration_adds_draft_column(tmp_path, monkeypatch):
    import sqlite3
    from app import db
    path = tmp_path / "old.db"
    old = sqlite3.connect(path)
    old.execute("CREATE TABLE exercise_progress (exercise_slug TEXT PRIMARY KEY, solved INTEGER NOT NULL DEFAULT 0, "
                "solved_at TEXT, mistakes INTEGER NOT NULL DEFAULT 0, in_review INTEGER NOT NULL DEFAULT 0, "
                "last_answer TEXT NOT NULL DEFAULT '')")
    old.execute("INSERT INTO exercise_progress (exercise_slug, solved) VALUES ('x', 1)")
    old.commit(); old.close()
    monkeypatch.setenv("CODEQUEST_DB", str(path))
    db.init_db()
    with db.transaction() as conn:
        row = conn.execute("SELECT * FROM exercise_progress").fetchone()
    assert row["solved"] == 1 and row["draft"] == ""


def test_topics_have_groups(client):
    groups = [t["group"] for t in client.get("/api/path").json()]
    assert groups[0] == "Python" and "Тестирование и DevOps" in groups


def test_continue_banner(client):
    lessons = first_lessons(client)
    # ничего не начато — предлагаем самый первый урок
    c = client.get("/api/continue").json()
    assert c["started"] is False and c["lesson"]["id"] == lessons[0]["id"]
    # открыли урок — плашка ведёт в него
    client.get(f"/api/lessons/{lessons[0]['id']}")
    c = client.get("/api/continue").json()
    assert c["started"] is True and c["lesson"]["id"] == lessons[0]["id"]
    # прошли его — плашка предлагает следующий урок той же темы
    solve_lesson(client, lessons[0]["id"])
    c = client.get("/api/continue").json()
    assert c["lesson"]["id"] == lessons[1]["id"] and c["topic"]["title"] == "Python: основы"


def test_admin_can_set_topic_group(client):
    t = client.post("/api/admin/topics", json={"title": "Go", "group_name": "Другие языки"}).json()
    assert t["group_name"] == "Другие языки"
    assert client.get("/api/path").json()[-1]["group"] == "Другие языки"


def test_continue_falls_back_to_last_solved(client):
    lessons = first_lessons(client)
    ex = client.get(f"/api/lessons/{lessons[0]['id']}").json()["exercises"][0]
    client.post(f"/api/exercises/{ex['id']}/check", json={"answer": answer_for(ex["id"])})
    from app.db import transaction
    with transaction() as conn:   # как у пользователя до обновления: поле ещё пустое
        conn.execute("UPDATE user_state SET last_lesson_slug = NULL")
    c = client.get("/api/continue").json()
    assert c["started"] is True and c["lesson"]["id"] == lessons[0]["id"]


def test_lesson_has_full_theory_and_quiz(client):
    lesson = client.get(f"/api/lessons/{first_lessons(client)[0]['id']}").json()
    assert "## Зачем это нужно" in lesson["theory_full"]
    assert "```python" in lesson["theory_full"]
    q = lesson["quiz"][0]
    assert {"q", "options", "answer", "explain"} <= set(q) and 0 <= q["answer"] < len(q["options"])


def test_admin_quiz_validation(client):
    lesson_id = first_lessons(client)[0]["id"]
    bad = client.put(f"/api/admin/lessons/{lesson_id}", json={"quiz": '[{"q": "?", "options": ["a", "b"], "answer": 5}]'})
    assert bad.status_code == 400
    broken_json = client.put(f"/api/admin/lessons/{lesson_id}", json={"quiz": "[{"})
    assert broken_json.status_code == 400
    ok = client.put(f"/api/admin/lessons/{lesson_id}",
                    json={"quiz": '[{"q": "2+2?", "options": ["4", "5"], "answer": 0, "explain": "просто"}]'})
    assert ok.status_code == 200
    assert client.get(f"/api/lessons/{lesson_id}").json()["quiz"][0]["q"] == "2+2?"


def test_export_roundtrip_keeps_theory(client):
    exported = client.get("/api/admin/export").json()
    lesson = exported["topics"][0]["modules"][0]["lessons"][0]
    assert lesson["theory_full"] and lesson["quiz"]
    r = client.post("/api/admin/import", json=exported).json()
    assert r["created"] == 0


def test_validator_runs_theory_examples():
    from app import cli, content
    pkg = content.Package.model_validate({"topics": [{"slug": "t", "title": "T", "modules": [{"slug": "m", "title": "M", "lessons": [
        {"slug": "l", "title": "L", "theory_full": "```python\nprint(1)\n```\n\n```python\n1/0\n```\n\n```py\nnot run(\n```"}]}]}]})
    problems = cli.validate(pkg)
    assert len(problems) == 1 and "пример №2" in problems[0]
