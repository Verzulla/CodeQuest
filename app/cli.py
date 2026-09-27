"""Командная строка для работы с контент-пакетами.

    python -m app.cli validate content/python-basics.json   # проверить пакет
    python -m app.cli import   content/python-basics.json   # загрузить в БД
    python -m app.cli export   backup.json                  # выгрузить весь контент

validate прогоняет каждое эталонное решение через тесты задания и
сверяет expected_output с реальным выводом кода. Пакет, который не
прошёл validate, импортировать не стоит.
"""
import json
import re
import sys
from pathlib import Path

from . import content, runner
from .db import init_db, transaction


PY_BLOCK = re.compile(r"^```python[ \t]*\n(.*?)^```", re.S | re.M)


def validate(pkg: content.Package) -> list[str]:
    problems, slugs = [], set()
    for t in pkg.topics:
        for m in t.modules:
            for l in m.lessons:
                # примеры из подробной теории с кнопкой «Запустить» обязаны работать
                for k, block in enumerate(PY_BLOCK.findall(l.theory_full), 1):
                    res = runner.run(block)
                    if res.error:
                        problems.append(f"{t.slug} / {l.slug}: пример №{k} в подробной теории упал — {res.error}")
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
                    else:
                        res = runner.run(e.code)
                        if res.error:
                            problems.append(f"{where}: код упал — {res.error}")
                        elif runner.normalize_output(res.stdout) != runner.normalize_output(e.expected_output):
                            problems.append(
                                f"{where}: expected_output {e.expected_output!r} ≠ реальный {res.stdout!r}")
    return problems


def main(argv: list[str]) -> int:
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
