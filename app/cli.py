"""Командная строка для работы с контент-пакетами.

    python -m app.cli validate content/py-vars.json   # проверить пакет
    python -m app.cli import   content/py-vars.json   # загрузить в БД
    python -m app.cli export   backup.json            # выгрузить весь контент
    python -m app.cli sync                            # привести БД к content/: загрузить все пакеты
                                                      # в порядке content/ORDER и удалить темы,
                                                      # которых больше нет среди пакетов
    python -m app.cli sandbox-check                   # собрать образ docker-песочницы и проверить изоляцию
    python -m app.cli users                           # список аккаунтов
    python -m app.cli make-admin   <ник>              # выдать права администратора
    python -m app.cli revoke-admin <ник>              # забрать права администратора
    python -m app.cli reset-progress <ник> --yes      # обнулить прогресс пользователя (контент остаётся)

validate прогоняет каждое эталонное решение через тесты задания и
сверяет expected_output с реальным выводом кода. Пакет, который не
прошёл validate, импортировать не стоит.
"""
import json
import os
import re
import sys
from pathlib import Path

from . import auth, content, runner
from .db import PROGRESS_TABLES, init_db, transaction


PY_BLOCK = re.compile(r"^```python[ \t]*\n(.*?)^```", re.S | re.M)


def validate(pkg: content.Package) -> list[str]:
    problems, slugs = [], set()
    for t in pkg.topics:
        for m in t.modules:
            for l in m.lessons:
                # примеры теории с кнопкой «Запустить» обязаны работать
                for kind, text in (("краткой", l.theory), ("подробной", l.theory_full)):
                    for k, block in enumerate(PY_BLOCK.findall(text), 1):
                        res = runner.run(block)
                        if res.error:
                            problems.append(f"{t.slug} / {l.slug}: пример №{k} в {kind} теории упал — {res.error}")
                for e in l.exercises:
                    where = f"{t.slug} / {m.slug} / {l.slug} / {e.slug}"
                    if e.slug in slugs:
                        problems.append(f"{where}: повторяющийся slug")
                    slugs.add(e.slug)
                    if e.type == "code":
                        if not e.tests.strip() or not e.solution.strip():
                            problems.append(f"{where}: у code-задания нужны tests и solution")
                            continue
                        res = runner.run(e.solution, e.tests)
                        if not res.passed:
                            problems.append(f"{where}: эталон не прошёл тесты — {res.error or res.tests}")
                        starter = runner.run(e.starter_code, e.tests)
                        if starter.passed:
                            problems.append(f"{where}: заготовка уже проходит тесты")
                    elif e.type == "command":
                        if not e.expected_output.strip() or not e.solution.strip():
                            problems.append(f"{where}: у command-задания нужны expected_output и solution")
                        elif not runner.command_matches(e.solution, e.expected_output):
                            problems.append(f"{where}: эталон {e.solution!r} не входит в допустимые варианты")
                    else:
                        res = runner.run(e.code)
                        if res.error:
                            problems.append(f"{where}: код упал — {res.error}")
                        elif runner.normalize_output(res.stdout) != runner.normalize_output(e.expected_output):
                            problems.append(
                                f"{where}: expected_output {e.expected_output!r} ≠ реальный {res.stdout!r}")
    return problems


CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"


def sync() -> int:
    files = content.content_files(CONTENT_DIR)
    pkgs = [(f, content.Package.model_validate_json(f.read_text(encoding="utf-8"))) for f in files]
    problems = [f"{f.name}: {p}" for f, pkg in pkgs for p in validate(pkg)]
    if problems:
        print(f"❌ Синхронизация отменена, проблем: {len(problems)}")
        for p in problems:
            print("  -", p)
        return 1
    order = [t.slug for _, pkg in pkgs for t in pkg.topics]
    with transaction() as conn:
        for f, pkg in pkgs:
            st = content.import_package(conn, pkg)
            print(f"  {f.name}: создано {st['created']}, обновлено {st['updated']}")
        for pos, slug in enumerate(order):
            conn.execute("UPDATE topics SET position = ? WHERE slug = ?", (pos, slug))
        stale = conn.execute(
            f"SELECT slug, title FROM topics WHERE slug NOT IN ({', '.join('?' * len(order))})", order
        ).fetchall()
        for row in stale:
            conn.execute("DELETE FROM topics WHERE slug = ?", (row["slug"],))
            print(f"  удалена тема «{row['title']}» ({row['slug']}) — её нет среди пакетов")
        # Внутри тем тоже убираем то, чего больше нет в пакетах (урок разделили, задание удалили…).
        # Прогресс привязан к слагам и не удаляется — если элемент вернётся, прогресс найдётся.
        for _, pkg in pkgs:
            for t in pkg.topics:
                keep = {
                    "modules": {m.slug for m in t.modules},
                    "lessons": {l.slug for m in t.modules for l in m.lessons},
                    "exercises": {e.slug for m in t.modules for l in m.lessons for e in l.exercises},
                }
                rows = {
                    "modules": conn.execute(
                        "SELECT m.slug, m.title FROM modules m JOIN topics t ON t.id = m.topic_id "
                        "WHERE t.slug = ?", (t.slug,)).fetchall(),
                    "lessons": conn.execute(
                        "SELECT l.slug, l.title FROM lessons l JOIN modules m ON m.id = l.module_id "
                        "JOIN topics t ON t.id = m.topic_id WHERE t.slug = ?", (t.slug,)).fetchall(),
                    "exercises": conn.execute(
                        "SELECT e.slug, e.slug AS title FROM exercises e JOIN lessons l ON l.id = e.lesson_id "
                        "JOIN modules m ON m.id = l.module_id JOIN topics t ON t.id = m.topic_id "
                        "WHERE t.slug = ?", (t.slug,)).fetchall(),
                }
                for table in ("modules", "lessons", "exercises"):
                    for row in rows[table]:
                        if row["slug"] not in keep[table]:
                            conn.execute(f"DELETE FROM {table} WHERE slug = ?", (row["slug"],))
                            print(f"  {t.slug}: удалено «{row['title']}» ({table}) — его нет в пакете")
    print(f"✅ Синхронизировано тем: {len(order)}")
    return 0


def sandbox_check() -> int:
    """Готовит сервер к приёму кода из интернета: образ на месте, изоляция работает."""
    import subprocess
    os.environ["CODEQUEST_SANDBOX"] = "docker"
    image = runner.docker_image()
    print(f"Образ песочницы: {image}")
    context = Path(__file__).resolve().parent.parent / "deploy" / "runner"
    try:
        built = subprocess.run(["docker", "build", "-q", "-t", image, str(context)], capture_output=True, text=True)
    except FileNotFoundError:
        print("❌ Команда docker не найдена — установи Docker")
        return 1
    if built.returncode:
        print(f"❌ Не удалось собрать образ: {built.stderr.strip()}")
        return 1
    checks = [
        ("код выполняется", "print(2 + 2)", "4"),
        ("библиотеки для тестов на месте",
         "import pytest, xdist, pydantic, allure, requests, responses, httpx, jsonschema, pwfake.sync_api, pwfake.demo, pwfake.pytest_plugin\nprint('ok')", "ok"),
        ("нет сети", "import socket\ntry:\n    socket.create_connection(('1.1.1.1', 53), timeout=2)\n"
                     "    print('online')\nexcept OSError:\n    print('offline')", "offline"),
        ("пользователь nobody", "import os\nprint(os.getuid())", "65534"),
        ("корень только для чтения", "try:\n    open('/pwned', 'w')\n    print('writable')\n"
                                     "except OSError:\n    print('ro')", "ro"),
    ]
    ok = True
    for title, code, expected in checks:
        res = runner.run(code)
        got = res.error or res.stdout.strip()
        ok &= got == expected
        print(f"  {'✅' if got == expected else '❌'} {title}" + ("" if got == expected else f": {got}"))
    timeout = runner.run("while True:\n    pass\n")
    ok &= timeout.timed_out
    print(f"  {'✅' if timeout.timed_out else '❌'} бесконечный цикл обрывается")
    print("✅ Песочница готова" if ok else "❌ Песочница НЕ готова — не открывай сервер в интернет")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    # Контент из репозитория доверенный: проверяем его без контейнеров — в сотни раз быстрее.
    # Чтобы валидировать в docker-песочнице, задай CODEQUEST_SANDBOX=docker явно.
    os.environ.setdefault("CODEQUEST_SANDBOX", "local")
    if argv == ["sync"]:
        init_db()
        return sync()
    if argv == ["sandbox-check"]:
        return sandbox_check()
    if argv == ["users"]:
        init_db()
        with transaction() as conn:
            rows = conn.execute(
                "SELECT u.username, u.is_admin, u.created_at, COALESCE(s.xp, 0) AS xp "
                "FROM users u LEFT JOIN user_state s ON s.user_id = u.id ORDER BY u.id").fetchall()
        for r in rows:
            print(f"  {r['username']:20} {'админ' if r['is_admin'] else '     '}  {r['xp']:6} XP  "
                  f"с {r['created_at'][:10]}")
        print(f"Всего аккаунтов: {len(rows)}")
        return 0
    if len(argv) == 2 and argv[0] in ("make-admin", "revoke-admin"):
        init_db()
        try:
            with transaction() as conn:
                user = auth.set_admin(conn, argv[1], argv[0] == "make-admin")
        except auth.AuthError as e:
            print(e.message)
            return 1
        print(f"«{user['username']}»: права администратора "
              f"{'выданы' if argv[0] == 'make-admin' else 'сняты'}")
        return 0
    if len(argv) == 3 and argv[0] == "reset-progress" and argv[2] == "--yes":
        init_db()
        with transaction() as conn:
            user = auth.find_user(conn, argv[1])
            if not user:
                print(f"Пользователь «{argv[1]}» не найден")
                return 1
            for table in PROGRESS_TABLES:
                conn.execute(f"DELETE FROM {table} WHERE user_id = ?", (user["id"],))
        print(f"Прогресс «{user['username']}» обнулён")
        return 0
    if len(argv) != 2 or argv[0] not in ("validate", "import", "export"):
        print(__doc__)
        return 2
    cmd, path = argv
    init_db()
    if cmd == "export":
        with transaction() as conn:
            data = content.export_package(conn)
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Сохранено в {path}")
        return 0

    pkg = content.Package.model_validate_json(Path(path).read_text(encoding="utf-8"))
    problems = validate(pkg)
    n = sum(len(l.exercises) for t in pkg.topics for m in t.modules for l in m.lessons)
    if problems:
        print(f"❌ Найдено проблем: {len(problems)}")
        for p in problems:
            print("  -", p)
        return 1
    print(f"✅ Пакет корректен: {n} заданий")
    if cmd == "import":
        with transaction() as conn:
            stats = content.import_package(conn, pkg)
        print(f"Импортировано: создано {stats['created']}, обновлено {stats['updated']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
