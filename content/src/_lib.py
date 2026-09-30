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


# Проверка заданий, где ученик пишет pytest-тесты: тесты задания запускают настоящий pytest
# на solution.py и смотрят исходы. patch= подменяет имена в модуле решения (например,
# на «сломанную» реализацию) — так проверяется, что тесты ученика ловят баги.
PYTEST_RUNNER = """
import importlib, os, sys
import pytest


class _Collect:
    def __init__(self):
        self.outcomes = {}

    def pytest_runtest_logreport(self, report):
        name = report.nodeid.split("::", 1)[-1]
        if report.when == "call" or report.outcome != "passed":
            self.outcomes[name] = report.outcome


def run_pytest(*args, patch=None):
    \"\"\"Запустить pytest на решении. Возвращает (код выхода, {имя теста: passed/failed/skipped}).\"\"\"
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())
    sys.modules.pop("solution", None)
    if patch:
        # Модуль импортируется заранее только ради подмены: иначе пусть его импортирует сам
        # pytest — с уже подключёнными плагинами (декораторы Allure работают только так).
        module = importlib.import_module("solution")
        for name, value in patch.items():
            setattr(module, name, value)
    collector = _Collect()
    code = pytest.main(["-q", "-p", "no:cacheprovider", "solution.py", *args], plugins=[collector])
    return int(code), collector.outcomes

"""

# Хвост заготовки и эталона: «▶ Запустить» покажет обычный вывод pytest.
PYTEST_MAIN = """

if __name__ == "__main__":
    pytest.main(["-q", "-p", "no:cacheprovider", "solution.py"])
"""


def pyt(slug, prompt, starter, tests, solution, hint="", xp=20):
    """Задание «напиши pytest-тесты»: к заготовке и эталону добавляется запуск pytest,
    к тестам задания — помощник run_pytest()."""
    return cod(slug, prompt, d(starter).rstrip("\n") + PYTEST_MAIN, PYTEST_RUNNER + d(tests),
               d(solution).rstrip("\n") + PYTEST_MAIN, hint=hint, xp=xp)


def x(idea="", lines=(), trace=(), mistake="", summary=""):
    """Ручной разбор решения (для content/src/explain_<тема>.py).

    idea — главная мысль задачи; lines — [(строка кода, что она делает и почему), ...];
    trace — выполнение по шагам для «что выведет»: [(строка, значения переменных, что напечатано), ...];
    mistake — частая ошибка. В тексте `…` — код, **…** — выделение."""
    item = {"idea": t(idea), "lines": [[d(c).rstrip("\n"), t(s)] for c, s in lines],
            "trace": [[c, v, o] for c, v, o in trace], "mistake": t(mistake), "summary": t(summary)}
    return {k: v for k, v in item.items() if v}


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
