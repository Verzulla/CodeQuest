import json
import os
from datetime import datetime, timedelta

# Тесты гоняют код без Docker; сам docker-режим проверяет test_sandbox.py.
os.environ.setdefault("CODEQUEST_SANDBOX", "local")

import pytest
from fastapi.testclient import TestClient

from app import auth, game, runner
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
def anon(tmp_path, monkeypatch, clock):
    """Клиент без входа в аккаунт."""
    monkeypatch.setenv("CODEQUEST_DB", str(tmp_path / "test.db"))
    auth.limiter.clear()
    from app.main import app
    with TestClient(app) as c:
        yield c


@pytest.fixture
def client(anon):
    """Клиент, вошедший как первый (и потому админ) пользователь."""
    r = anon.post("/api/auth/register", json={"username": "tester", "password": "secret1"})
    assert r.status_code == 200, r.text
    return anon


def new_client(anon, username, password="secret1", register=True):
    """Второй браузер к тому же серверу — со своими cookie."""
    c = TestClient(anon.app)
    r = c.post(f"/api/auth/{'register' if register else 'login'}",
               json={"username": username, "password": password})
    assert r.status_code == 200, r.text
    return c


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


def test_sequential_lessons_can_be_disabled(client):
    lessons = first_lessons(client)
    assert client.put("/api/settings", json={"sequential_lessons": False}).json()["sequential_lessons"] is False
    lessons = first_lessons(client)
    assert lessons[0]["status"] == "current" and all(l["status"] == "open" for l in lessons[1:])
    assert client.get(f"/api/lessons/{lessons[3]['id']}").status_code == 200
    solve_lesson(client, lessons[3]["id"])
    client.put("/api/settings", json={"sequential_lessons": True})
    statuses = [l["status"] for l in first_lessons(client)]
    assert statuses[:5] == ["current", "locked", "locked", "done", "current"]


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
    pkg = json.loads((ROOT / "content" / "py-vars.json").read_text(encoding="utf-8"))
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


def _make_single_user_db(path):
    """База однопользовательской версии: прогресс без user_id, старая колонка draft отсутствует."""
    import sqlite3
    old = sqlite3.connect(path)
    old.executescript("""
        CREATE TABLE user_state (id INTEGER PRIMARY KEY CHECK (id = 1), xp INTEGER NOT NULL DEFAULT 0,
            hearts INTEGER NOT NULL DEFAULT 5, hearts_updated_at TEXT, hearts_enabled INTEGER NOT NULL DEFAULT 1,
            streak INTEGER NOT NULL DEFAULT 0, longest_streak INTEGER NOT NULL DEFAULT 0, last_active_date TEXT,
            freezes INTEGER NOT NULL DEFAULT 1, daily_goal INTEGER NOT NULL DEFAULT 30,
            theme TEXT NOT NULL DEFAULT 'light', last_lesson_slug TEXT);
        INSERT INTO user_state (id, xp, theme, daily_goal) VALUES (1, 80, 'dark', 50);
        CREATE TABLE exercise_progress (exercise_slug TEXT PRIMARY KEY, solved INTEGER NOT NULL DEFAULT 0,
            solved_at TEXT, mistakes INTEGER NOT NULL DEFAULT 0, in_review INTEGER NOT NULL DEFAULT 0,
            last_answer TEXT NOT NULL DEFAULT '');
        INSERT INTO exercise_progress (exercise_slug, solved, last_answer) VALUES ('x', 1, 'print(1)');
        CREATE TABLE achievements (code TEXT PRIMARY KEY, unlocked_at TEXT NOT NULL);
        INSERT INTO achievements VALUES ('first_step', '2026-01-01T10:00:00');
    """)
    old.commit()
    old.close()


def test_single_user_progress_goes_to_first_account(tmp_path, monkeypatch, clock):
    path = tmp_path / "old.db"
    _make_single_user_db(path)
    monkeypatch.setenv("CODEQUEST_DB", str(path))
    auth.limiter.clear()
    from app.main import app
    from app.db import transaction
    with TestClient(app) as c:
        r = c.post("/api/auth/register", json={"username": "Валера", "password": "secret1"}).json()
        assert r["claimed_progress"] is True and r["is_admin"] is True
        st = c.get("/api/state").json()
        assert st["xp"] == 80 and st["theme"] == "dark" and st["daily_goal"] == 50
        assert any(a["code"] == "first_step" and a["unlocked_at"]
                   for a in c.get("/api/achievements").json()["achievements"])
        with transaction() as conn:
            row = conn.execute("SELECT * FROM exercise_progress WHERE exercise_slug = 'x'").fetchone()
            assert row["solved"] == 1 and row["last_answer"] == "print(1)" and row["draft"] == ""
            legacy = conn.execute("SELECT name FROM sqlite_master WHERE name LIKE 'legacy_%'").fetchall()
            assert legacy == []
        # второй аккаунт начинает с нуля и не админ
        other = new_client(c, "second")
        r = other.get("/api/auth/me").json()
        assert r["is_admin"] is False and other.get("/api/state").json()["xp"] == 0


# ---------- аккаунты ----------

def test_api_requires_login(anon):
    for url in ("/api/state", "/api/path", "/api/continue", "/api/review", "/api/stats",
                "/api/achievements", "/api/auth/me", "/api/admin/tree"):
        assert anon.get(url).status_code == 401, url
    assert anon.post("/api/run", json={"code": "print(1)"}).status_code == 401
    assert anon.get("/api/rules").status_code == 200


def test_register_login_logout(anon):
    r = anon.post("/api/auth/register", json={"username": "Аня_1", "password": "secret1"})
    assert r.status_code == 200 and r.json()["username"] == "Аня_1"
    cookie = r.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=lax" in cookie and "max-age=432000" in cookie
    assert anon.get("/api/state").status_code == 200
    assert anon.post("/api/auth/logout").status_code == 200
    assert anon.get("/api/state").status_code == 401
    # ник без учёта регистра, в том числе для кириллицы
    assert anon.post("/api/auth/login", json={"username": "аня_1", "password": "secret1"}).status_code == 200
    assert anon.get("/api/auth/me").json()["username"] == "Аня_1"
    assert anon.post("/api/auth/login", json={"username": "Аня_1", "password": "wrong!!"}).status_code == 401
    assert anon.post("/api/auth/login", json={"username": "nobody", "password": "secret1"}).status_code == 401


def test_registration_rules(anon):
    bad = [("ab", "secret1"), ("a" * 21, "secret1"), ("with space", "secret1"), ("dash-name", "secret1"),
           ("valid", "12345"), ("valid", "x" * 129)]
    for username, password in bad:
        r = anon.post("/api/auth/register", json={"username": username, "password": password})
        assert r.status_code == 400, (username, r.text)
    assert anon.post("/api/auth/register", json={"username": "Boris", "password": "secret1"}).status_code == 200
    dup = TestClient(anon.app)
    assert dup.post("/api/auth/register", json={"username": "BORIS", "password": "secret1"}).status_code == 409


def test_progress_is_per_user(client):
    lesson_id = first_lessons(client)[0]["id"]
    solve_lesson(client, lesson_id)
    other = new_client(client, "second")
    assert other.get("/api/state").json()["xp"] == 0
    assert other.get("/api/stats").json()["solved"] == 0
    assert first_lessons(other)[0]["status"] == "current"
    assert all(not e["solved"] for e in other.get(f"/api/lessons/{lesson_id}").json()["exercises"])
    # черновик одного не виден другому
    ex = other.get(f"/api/lessons/{lesson_id}").json()["exercises"][0]
    other.put(f"/api/exercises/{ex['id']}/draft", json={"draft": "мой черновик"})
    mine = client.get(f"/api/lessons/{lesson_id}").json()["exercises"][0]
    assert mine["draft"] == "" and mine["solved"]
    # сброс прогресса второго не трогает первого
    other.post("/api/progress/reset", json={"confirm": "RESET"})
    assert client.get("/api/state").json()["xp"] > 0
    # настройки тоже свои
    other.put("/api/settings", json={"theme": "dark"})
    assert client.get("/api/state").json()["theme"] == "light"


def test_only_admin_edits_content(client):
    other = new_client(client, "student")
    assert other.get("/api/admin/tree").status_code == 403
    assert other.post("/api/admin/topics", json={"title": "Взлом"}).status_code == 403
    assert other.get("/api/admin/export").status_code == 403
    assert client.get("/api/admin/tree").status_code == 200


def test_cli_admin_commands(client, capsys):
    from app import cli
    other = new_client(client, "student")
    assert cli.main(["make-admin", "STUDENT"]) == 0
    assert other.get("/api/admin/tree").status_code == 200
    assert cli.main(["revoke-admin", "student"]) == 0
    assert other.get("/api/admin/tree").status_code == 403
    assert cli.main(["make-admin", "ghost"]) == 1
    assert cli.main(["users"]) == 0
    assert "tester" in capsys.readouterr().out


def test_session_expires_after_idle_and_refreshes(client, clock):
    clock.t += timedelta(days=4)
    r = client.get("/api/state")
    assert r.status_code == 200 and "cq_session" in r.headers.get("set-cookie", "")   # продлена
    clock.t += timedelta(days=4)                     # 8 дней с входа, но 4 с последней активности
    assert client.get("/api/state").status_code == 200
    clock.t += timedelta(days=5, minutes=1)          # 5 дней без активности — сессия истекла
    assert client.get("/api/state").status_code == 401


def test_change_password_ends_other_sessions(client):
    laptop = new_client(client, "tester", register=False)
    bad = client.put("/api/account/password", json={"current_password": "nope!!", "new_password": "newpass1"})
    assert bad.status_code == 400
    short = client.put("/api/account/password", json={"current_password": "secret1", "new_password": "123"})
    assert short.status_code == 400
    ok = client.put("/api/account/password", json={"current_password": "secret1", "new_password": "newpass1"})
    assert ok.status_code == 200
    assert client.get("/api/state").status_code == 200       # текущая сессия жива
    assert laptop.get("/api/state").status_code == 401       # другая завершена
    fresh = TestClient(client.app)
    assert fresh.post("/api/auth/login", json={"username": "tester", "password": "secret1"}).status_code == 401
    assert fresh.post("/api/auth/login", json={"username": "tester", "password": "newpass1"}).status_code == 200


def test_delete_account_removes_progress(client):
    from app.db import transaction
    solve_lesson(client, first_lessons(client)[0]["id"])
    assert client.post("/api/account/delete", json={"password": "wrong!!"}).status_code == 400
    assert client.post("/api/account/delete", json={"password": "secret1"}).status_code == 200
    assert client.get("/api/state").status_code == 401
    with transaction() as conn:
        for table in ("users", "sessions", "user_state", "exercise_progress", "lesson_completions",
                      "daily_activity", "counters", "achievements"):
            assert conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == 0, table
        assert conn.execute("SELECT COUNT(*) FROM exercises").fetchone()[0] > 0   # контент на месте
    again = TestClient(client.app)
    assert again.post("/api/auth/login", json={"username": "tester", "password": "secret1"}).status_code == 401


def test_login_rate_limit(anon):
    anon.post("/api/auth/register", json={"username": "victim", "password": "secret1"})
    anon.post("/api/auth/logout")
    codes = [anon.post("/api/auth/login", json={"username": "victim", "password": f"guess{i:02}"}).status_code
             for i in range(11)]
    assert codes[:10] == [401] * 10 and codes[10] == 429
    # даже верный пароль не пускает, пока не истечёт окно
    assert anon.post("/api/auth/login", json={"username": "victim", "password": "secret1"}).status_code == 429


def test_registration_rate_limit(anon):
    codes = [TestClient(anon.app).post("/api/auth/register", json={"username": f"bot{i}", "password": "secret1"}).status_code
             for i in range(6)]
    assert codes == [200] * 5 + [429]


def test_cross_origin_writes_rejected(client):
    r = client.post("/api/progress/reset", json={"confirm": "RESET"}, headers={"Origin": "https://evil.example"})
    assert r.status_code == 403
    r = client.put("/api/settings", json={"theme": "dark"}, headers={"Origin": "http://testserver"})
    assert r.status_code == 200


def test_password_stored_hashed(client):
    from app.db import transaction
    with transaction() as conn:
        user = conn.execute("SELECT password_hash FROM users").fetchone()
        session = conn.execute("SELECT token_hash FROM sessions").fetchone()
    assert user["password_hash"].startswith("scrypt$") and "secret1" not in user["password_hash"]
    assert session["token_hash"] != client.cookies.get("cq_session")


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
    assert c["lesson"]["id"] == lessons[1]["id"] and c["topic"]["title"] == "Переменные и типы данных"


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
        conn.execute("UPDATE user_state SET last_lesson_slug = NULL")   # единственный пользователь
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
    assert len(problems) == 1 and "пример №2 в подробной" in problems[0]
    short = content.Package.model_validate({"topics": [{"slug": "t", "title": "T", "modules": [{"slug": "m", "title": "M", "lessons": [
        {"slug": "l", "title": "L", "theory": "```python\nprint(undefined_name)\n```"}]}]}]})
    problems = cli.validate(short)
    assert len(problems) == 1 and "пример №1 в краткой" in problems[0] and "NameError" in problems[0]


def test_code_runs_rate_limited_per_user(client):
    codes = [client.post("/api/run", json={"code": "print(1)"}).status_code for _ in range(31)]
    assert codes[:30] == [200] * 30 and codes[30] == 429
    other = new_client(client, "second")                     # у другого пользователя свой лимит
    assert other.post("/api/run", json={"code": "print(1)"}).status_code == 200


# ---------- PWA ----------

def test_manifest_and_icons(anon):
    r = anon.get("/manifest.webmanifest")
    assert r.status_code == 200 and r.headers["content-type"].startswith("application/manifest+json")
    m = r.json()
    assert m["display"] == "standalone" and m["start_url"] == "/"
    purposes = {i["purpose"] for i in m["icons"]}
    assert {"any", "maskable"} <= purposes
    import struct
    for icon in m["icons"]:
        png = anon.get(icon["src"]).content
        assert png[:8] == b"\x89PNG\r\n\x1a\n"
        w, h = struct.unpack(">II", png[16:24])
        assert f"{w}x{h}" == icon["sizes"]
    html = anon.get("/").text
    assert 'rel="manifest"' in html and 'rel="apple-touch-icon"' in html and "viewport-fit=cover" in html


def test_service_worker_served_from_root(anon):
    r = anon.get("/sw.js")
    assert r.status_code == 200 and "javascript" in r.headers["content-type"]
    assert r.headers["cache-control"] == "no-cache"
    body = r.text
    assert "__VERSION__" not in body and "__SHELL__" not in body
    shell = json.loads(body.split("const SHELL = ", 1)[1].split(";\n", 1)[0])
    assert "/" in shell and "/static/js/app.js" in shell and "/static/icons/icon-192.png" in shell
    assert not any(p.startswith("/api") for p in shell)
    for path in shell:                       # всё, что кладём в кэш при установке, реально отдаётся
        assert anon.get(path).status_code == 200, path


def test_sync_prunes_removed_lessons(tmp_path, monkeypatch):
    """Урок, исчезнувший из пакета (например, разделённый на два), удаляется при sync."""
    monkeypatch.setenv("CODEQUEST_DB", str(tmp_path / "sync.db"))
    from app import cli
    from app.db import init_db, transaction
    pkg_dir = tmp_path / "content"
    pkg_dir.mkdir()
    def write(lessons):
        pkg = {"topics": [{"slug": "t", "title": "T", "modules": [{"slug": "m", "title": "M", "lessons": [
            {"slug": s, "title": s, "exercises": [{"slug": f"{s}-e", "type": "output", "prompt": "?",
                                                    "code": "print(1)", "expected_output": "1"}]} for s in lessons]}]}]}
        (pkg_dir / "t.json").write_text(json.dumps(pkg), encoding="utf-8")
    monkeypatch.setattr(cli, "CONTENT_DIR", pkg_dir)
    init_db()
    write(["a", "b"])
    assert cli.sync() == 0
    write(["a", "c"])
    assert cli.sync() == 0
    with transaction() as conn:
        lessons = [r[0] for r in conn.execute("SELECT slug FROM lessons ORDER BY slug")]
        exercises = [r[0] for r in conn.execute("SELECT slug FROM exercises ORDER BY slug")]
    assert lessons == ["a", "c"] and exercises == ["a-e", "c-e"]


# ---------- Задания «Терминал» ----------

def test_command_matches():
    variants = "git checkout -b feature\ngit switch -c feature\nre:git branch feature && git (checkout|switch) feature"
    assert runner.command_matches("  git   checkout -b feature ", variants)
    assert runner.command_matches("$ git switch -c feature", variants)
    assert runner.command_matches("git branch feature && git switch feature", variants)
    assert not runner.command_matches("git checkout feature", variants)
    assert not runner.command_matches("", variants)


def test_command_exercise_check(client):
    pkg = {"topics": [{"slug": "cli-demo", "title": "Терминал", "modules": [{"slug": "cli-m1", "title": "М",
           "lessons": [{"slug": "cli-l1", "title": "Урок", "exercises": [
               {"slug": "cli-e1", "type": "command", "prompt": "Покажи текущую папку",
                "expected_output": "pwd", "solution": "pwd", "code": "$ cd /tmp"}]}]}]}]}
    assert client.post("/api/admin/import", json=pkg).status_code == 200
    topic = next(t for t in client.get("/api/path").json() if t["title"] == "Терминал")
    lesson = client.get(f"/api/lessons/{topic['modules'][0]['lessons'][0]['id']}").json()
    ex = lesson["exercises"][0]
    assert ex["type"] == "command" and ex["code"] == "$ cd /tmp"
    wrong = client.post(f"/api/exercises/{ex['id']}/check", json={"answer": "ls"}).json()
    assert not wrong["correct"] and wrong["expected"] == "pwd"
    right = client.post(f"/api/exercises/{ex['id']}/check", json={"answer": "$ pwd"}).json()
    assert right["correct"]


def test_old_exercises_table_gets_command_type(tmp_path, monkeypatch):
    import sqlite3
    from app import db
    path = tmp_path / "old.db"
    old = sqlite3.connect(path)
    old.executescript(db.SCHEMA.replace("('code', 'output', 'command')", "('code', 'output')"))
    old.executescript("""
        INSERT INTO topics (id, slug, title) VALUES (1, 't', 'Т');
        INSERT INTO modules (id, topic_id, slug, title) VALUES (1, 1, 'm', 'М');
        INSERT INTO lessons (id, module_id, slug, title) VALUES (1, 1, 'l', 'Л');
        INSERT INTO exercises (lesson_id, slug, type, prompt) VALUES (1, 'old-e1', 'output', 'что выведет?');
    """)
    old.commit()
    old.close()
    monkeypatch.setenv("CODEQUEST_DB", str(path))
    db.init_db()
    with db.transaction() as conn:
        assert conn.execute("SELECT slug FROM exercises").fetchone()["slug"] == "old-e1"
        conn.execute("INSERT INTO exercises (lesson_id, slug, type, prompt) VALUES (1, 'new-e1', 'command', 'pwd?')")
