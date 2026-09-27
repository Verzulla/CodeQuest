"""Собрать JSON-пакеты из описаний в content/src/*.py.

    .venv/bin/python -m content.src.build            # все темы
    .venv/bin/python -m content.src.build ternary    # только указанные модули-файлы

Каждый файл content/src/<name>.py объявляет TOPIC = topic(...).
Результат: content/<slug темы>.json. Затем:

    .venv/bin/python -m app.cli import content/<slug>.json
"""
import importlib
import json
import sys
from pathlib import Path

SRC = Path(__file__).parent
OUT = SRC.parent


def attach_theory(name: str, topic: dict) -> None:
    """Подробная теория и «Проверь себя» лежат в content/src/theory_<name>.py:
    THEORY = {slug_урока: {"full": markdown, "quiz": [вопросы]}}."""
    if not (SRC / f"theory_{name}.py").exists():
        return
    theory = importlib.import_module(f"content.src.theory_{name}").THEORY
    lessons = {l["slug"]: l for m in topic["modules"] for l in m["lessons"]}
    unknown = set(theory) - set(lessons)
    if unknown:
        raise SystemExit(f"theory_{name}.py: нет таких уроков {sorted(unknown)}")
    for slug, lesson in lessons.items():
        item = theory.get(slug)
        if item is None:
            print(f"  ⚠️  {slug}: нет подробной теории")
            continue
        lesson["theory_full"] = item["full"]
        lesson["quiz"] = item.get("quiz", [])


def main(names: list[str]) -> None:
    names = names or sorted(p.stem for p in SRC.glob("*.py") if not p.stem.startswith(("_", "theory_")) and p.stem != "build")
    for name in names:
        topic = getattr(importlib.import_module(f"content.src.{name}"), "TOPIC", None)
        if topic is None:  # вспомогательный файл (theory_*.py, *_extra.py) — не тема
            continue
        attach_theory(name, topic)
        path = OUT / f"{topic['slug']}.json"
        path.write_text(json.dumps({"topics": [topic]}, ensure_ascii=False, indent=2), encoding="utf-8")
        n = sum(len(l["exercises"]) for m in topic["modules"] for l in m["lessons"])
        lessons = sum(len(m["lessons"]) for m in topic["modules"])
        print(f"{path.name}: {len(topic['modules'])} модулей, {lessons} уроков, {n} заданий")


if __name__ == "__main__":
    main(sys.argv[1:])
