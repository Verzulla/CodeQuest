"""Помощники для описания контента на Python вместо ручного JSON.

expected_output для заданий «что выведет код» вычисляется запуском кода
в той же песочнице, что и в приложении — расхождений быть не может.
"""
from textwrap import dedent

from app import runner


def d(s: str) -> str:
    return dedent(s).strip("\n") + "\n" if s.strip() else ""


def out(slug, prompt, code, hint="", xp=10):
    code = d(code)
    res = runner.run(code)
    if res.error:
        raise ValueError(f"{slug}: код упал — {res.error}")
    return {"slug": slug, "type": "output", "prompt": prompt, "code": code,
            "expected_output": res.stdout.rstrip("\n"), "hint": hint, "xp": xp}


def cod(slug, prompt, starter, tests, solution, hint="", xp=15):
    return {"slug": slug, "type": "code", "prompt": prompt, "starter_code": d(starter),
            "tests": d(tests), "solution": d(solution), "hint": hint, "xp": xp}


def cmd(slug, prompt, answers, context="", hint="", xp=10):
    """Задание «Терминал»: ученик вводит команду или короткий ответ.

    answers — допустимые варианты (первый — эталон, его покажем при ошибке);
    вариант «re:…» — регулярное выражение. context — что показать над полем ввода
    (например, вывод терминала), без запуска."""
    answers = [answers] if isinstance(answers, str) else list(answers)
    return {"slug": slug, "type": "command", "prompt": prompt, "code": d(context),
            "expected_output": "\n".join(answers), "solution": answers[0], "hint": hint, "xp": xp}


def lesson(slug, title, *items, full="", quiz=None):
    """lesson(slug, title, [краткая теория,] *задания, full=подробный урок, quiz=«Проверь себя»).

    Теорию можно не указывать здесь, а описать в content/src/theory_<тема>.py —
    build.py подставит её (так устроены все новые темы)."""
    theory, exercises = (items[0], items[1:]) if items and isinstance(items[0], str) else ("", items)
    return {"slug": slug, "title": title, "theory": d(theory), "exercises": list(exercises),
            "theory_full": t(full) if full else "", "quiz": quiz or []}


def q(question, options, answer, explain):
    """Вопрос «Проверь себя»."""
    return {"q": question, "options": options, "answer": answer, "explain": explain}


def module(slug, title, icon, description, *lessons):
    return {"slug": slug, "title": title, "icon": icon, "description": description,
            "lessons": list(lessons)}


def topic(slug, title, icon, color, description, *modules, group=""):
    return {"slug": slug, "title": title, "icon": icon, "color": color,
            "description": description, "group": group, "modules": list(modules)}


def t(s: str) -> str:
    """Многострочный текст условия: убрать общий отступ и пустые края."""
    return dedent(s).strip()
