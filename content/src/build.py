"""Собрать JSON-пакеты из описаний в content/src/*.py.

    .venv/bin/python -m content.src.build            # все темы
    .venv/bin/python -m content.src.build ternary    # только указанные модули-файлы

Каждый файл content/src/<name>.py объявляет TOPIC = topic(...).
Результат: content/<slug темы>.json. Затем:

    .venv/bin/python -m app.cli import content/<slug>.json
"""
import importlib
import json
import re
import sys
from pathlib import Path

SRC = Path(__file__).parent
OUT = SRC.parent


VIZ_TYPES = {"memory", "git", "slice", "fs", "perm", "fixtures", "pipeline", "http", "trace",
             "pipe", "redirect", "select", "params", "json", "schema", "matrix", "trigger", "cron", "itertools",
             "buildcache", "container", "dockerhost", "promote", "vmstack"}
VIZ_NEED_STEPS = {"memory", "git", "trace", "container"}   # остальные — песочницы без заранее заданных шагов


def check_viz(where: str, text: str) -> None:
    """Интерактивные схемы (```viz в теории) — валидный JSON известного типа (static/js/viz.js)."""
    for block in re.findall(r"^```viz\n(.*?)^```", text or "", flags=re.S | re.M):
        try:
            spec = json.loads(block)
        except ValueError as e:
            raise SystemExit(f"{where}: схема viz — не JSON: {e}")
        if spec.get("type") not in VIZ_TYPES:
            raise SystemExit(f"{where}: схема viz неизвестного типа {spec.get('type')!r}")
        if spec["type"] in VIZ_NEED_STEPS and not spec.get("steps"):
            raise SystemExit(f"{where}: в схеме viz нет шагов")


def attach_theory(name: str, topic: dict) -> None:
    """Теория и «Проверь себя» лежат в content/src/theory_<name>.py:
    THEORY = {slug_урока: {"short": краткая теория, "full": подробный урок, "quiz": [вопросы]}}.
    short можно не указывать — тогда остаётся краткая теория из самого урока."""
    lessons = {l["slug"]: l for m in topic["modules"] for l in m["lessons"]}
    if not (SRC / f"theory_{name}.py").exists():   # теория описана прямо в уроках
        for slug, lesson in lessons.items():
            if not lesson.get("theory_full"):
                print(f"  ⚠️  {slug}: нет подробной теории")
        return
    theory = importlib.import_module(f"content.src.theory_{name}").THEORY
    unknown = set(theory) - set(lessons)
    if unknown:
        raise SystemExit(f"theory_{name}.py: нет таких уроков {sorted(unknown)}")
    for slug, lesson in lessons.items():
        item = theory.get(slug)
        if item is None:
            print(f"  ⚠️  {slug}: нет подробной теории")
            continue
        if "short" in item:
            lesson["theory"] = item["short"]
        lesson["theory_full"] = item["full"]
        lesson["quiz"] = item.get("quiz", [])
        check_viz(f"theory_{name}.py: {slug}", item["full"] + "\n" + item.get("short", ""))


def attach_explain(name: str, topic: dict) -> None:
    """Ручные разборы решений лежат в content/src/explain_<name>.py:
    EXPLAIN = {slug_задания: x(idea=..., lines=[(код, пояснение), ...], trace=[...], mistake=...)}.
    Строки кода в lines и trace должны быть в решении (или в коде задания «что выведет»)."""
    if not (SRC / f"explain_{name}.py").exists():
        return
    manual = importlib.import_module(f"content.src.explain_{name}").EXPLAIN
    exercises = {e["slug"]: e for m in topic["modules"] for l in m["lessons"] for e in l["exercises"]}
    unknown = set(manual) - set(exercises)
    if unknown:
        raise SystemExit(f"explain_{name}.py: нет таких заданий {sorted(unknown)}")
    for slug, item in manual.items():
        ex = exercises[slug]
        # «Терминал»: разбирают части команды (и команды из контекста) — ищем как подстроку
        text = ex["code"] if ex["type"] == "output" else ex["solution"] + ("\n" + ex["code"] if ex["type"] == "command" else "")
        src = {ln.strip() for ln in text.splitlines()}
        for code in [c for c, _ in item.get("lines", [])] + [r[0] for r in item.get("trace", [])]:
            for ln in code.splitlines():
                ok = ln.strip() in text if ex["type"] == "command" else ln.strip() in src
                if ln.strip() and not ok:
                    raise SystemExit(f"explain_{name}.py: {slug}: строки «{ln.strip()}» нет в решении")
        empty = [c for c, t in item.get("lines", []) if not t.strip()]
        if empty:
            raise SystemExit(f"explain_{name}.py: {slug}: нет пояснения к строке «{empty[0].splitlines()[0]}»")
        ex["explain"] = json.dumps(item, ensure_ascii=False)
    print(f"  ручных разборов: {len(manual)} из {len(exercises)}")


def main(names: list[str]) -> None:
    names = names or sorted(p.stem for p in SRC.glob("*.py") if not p.stem.startswith(("_", "theory_", "explain_")) and p.stem != "build")
    for name in names:
        topic = getattr(importlib.import_module(f"content.src.{name}"), "TOPIC", None)
        if topic is None:  # вспомогательный файл (theory_*.py, *_extra.py) — не тема
            continue
        attach_theory(name, topic)
        attach_explain(name, topic)
        path = OUT / f"{topic['slug']}.json"
        path.write_text(json.dumps({"topics": [topic]}, ensure_ascii=False, indent=2), encoding="utf-8")
        n = sum(len(l["exercises"]) for m in topic["modules"] for l in m["lessons"])
        lessons = sum(len(m["lessons"]) for m in topic["modules"])
        print(f"{path.name}: {len(topic['modules'])} модулей, {lessons} уроков, {n} заданий")


if __name__ == "__main__":
    main(sys.argv[1:])
