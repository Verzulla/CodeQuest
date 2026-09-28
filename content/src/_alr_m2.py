"""Тема «Allure и отчёты», модуль 2 «Отчёты» — задания. Теория — в _alr_t2.py."""
from ._lib import cmd, cod, lesson, module, t

P = "alr"

m2 = module(f"{P}-m2", "Отчёты", "📈", "Генерация и история отчёта, статусы и категории, JUnit XML, сводка по результатам",

lesson(f"{P}-report", "Генерация отчёта, история и окружение",
    cmd(f"{P}-report-e1", "Сгенерируй отчёт одним HTML-файлом (удобно отправить по почте или приложить к задаче).",
        ["allure generate allure-results --single-file -o allure-report --clean", "allure generate --single-file allure-results -o allure-report",
         "allure generate allure-results --single-file", "allure generate --single-file allure-results",
         "allure generate allure-results -o allure-report --clean --single-file", "allure generate allure-results --single-file --clean -o allure-report"]),
    cmd(f"{P}-report-e2", "Чтобы в новом отчёте появились графики истории (тренды), что нужно скопировать из прошлого отчёта в `allure-results` перед генерацией? Введи имя папки.",
        ["history", "allure-report/history"]),
    cmd(f"{P}-report-e3", "Скопируй историю прошлого отчёта `allure-report/history` в `allure-results/` одной командой.",
        ["cp -r allure-report/history allure-results/", "cp -r allure-report/history allure-results", "cp -R allure-report/history allure-results/"]),
    cmd(f"{P}-report-e4", "Как называется файл в `allure-results`, который заполняет блок «Environment» (окружение) в отчёте? Введи имя файла.",
        ["environment.properties", "environment.xml"]),
    cmd(f"{P}-report-e5", "Как называется файл в `allure-results`, который задаёт свои категории дефектов (например, «Проблемы окружения»)? Введи имя.",
        ["categories.json"]),
    cod(f"{P}-report-e6", t("""
        Напиши функцию `write_environment(path, env)` — записать словарь `env` в файл формата `environment.properties`: каждая пара — строка `ключ=значение`, ключи отсортированы по алфавиту.
        """),
        """
        def write_environment(path, env):
            pass
        """,
        """
        def test_values():
            write_environment("environment.properties", {"Browser": "chrome", "Base.URL": "https://stage", "Python": "3.12"})
            with open("environment.properties", encoding="utf-8") as f:
                assert f.read() == "Base.URL=https://stage\\nBrowser=chrome\\nPython=3.12\\n", "Неверный формат файла"
        """,
        """
        def write_environment(path, env):
            with open(path, "w", encoding="utf-8") as f:
                for key in sorted(env):
                    f.write(f"{key}={env[key]}\\n")
        """),
    cod(f"{P}-report-e7", t("""
        Напиши функцию `make_categories()` — вернуть список категорий для `categories.json`:

        - `{"name": "Проблемы окружения", "matchedStatuses": ["broken"], "messageRegex": ".*ConnectionError.*"}`;
        - `{"name": "Дефекты продукта", "matchedStatuses": ["failed"]}`.

        И функцию `save_categories(path)` — записать их в файл как JSON (с `ensure_ascii=False`).
        """),
        """
        import json


        def make_categories():
            pass


        def save_categories(path):
            pass
        """,
        """
        import json

        def test_values():
            cats = make_categories()
            assert cats == [
                {"name": "Проблемы окружения", "matchedStatuses": ["broken"], "messageRegex": ".*ConnectionError.*"},
                {"name": "Дефекты продукта", "matchedStatuses": ["failed"]},
            ], cats
            save_categories("categories.json")
            text = open("categories.json", encoding="utf-8").read()
            assert json.loads(text) == cats and "Проблемы" in text, "Файл — JSON с кириллицей без \\\\u-экранирования"
        """,
        """
        import json


        def make_categories():
            return [
                {"name": "Проблемы окружения", "matchedStatuses": ["broken"], "messageRegex": ".*ConnectionError.*"},
                {"name": "Дефекты продукта", "matchedStatuses": ["failed"]},
            ]


        def save_categories(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(make_categories(), f, ensure_ascii=False, indent=2)
        """),
    cmd(f"{P}-report-e8", "Что покажет блок Environment в отчёте для ключа `Browser`?",
        ["firefox"],
        context="""
        $ cat allure-results/environment.properties
        Base.URL=https://stage.example.com
        Browser=firefox
        Browser.Version=128.0
        """, xp=15),
),

lesson(f"{P}-status", "Статусы, категории и флаки",
    cmd(f"{P}-status-e1", "Какой статус Allure получит тест, упавший на `assert`?",
        ["failed"]),
    cmd(f"{P}-status-e2", "Какой статус получит тест, в котором возникло исключение `KeyError` (не assert)?",
        ["broken"]),
    cmd(f"{P}-status-e3", "Какой статус получит тест с `@pytest.mark.skip`?",
        ["skipped"]),
    cmd(f"{P}-status-e4", "Сколько тестов **сломано** (broken)? Введи число.",
        ["2"],
        context="""
        Total: 40
          passed   33
          failed    3
          broken    2
          skipped   2
        """),
    cod(f"{P}-status-e5", t("""
        Напиши функцию `status_of(outcome, exc_type)` — как Allure определяет статус: `outcome` — `"passed"`, `"failed"` или `"skipped"`, `exc_type` — имя класса исключения (или `None`). Если тест упал с `AssertionError` — `"failed"`, с любым другим исключением — `"broken"`; пропущенный — `"skipped"`; прошедший — `"passed"`.
        """),
        """
        def status_of(outcome, exc_type):
            pass
        """,
        """
        def test_values():
            assert status_of("passed", None) == "passed" and status_of("skipped", None) == "skipped", "passed/skipped"
            assert status_of("failed", "AssertionError") == "failed", "assert"
            assert status_of("failed", "KeyError") == "broken" and status_of("failed", "TimeoutError") == "broken", "broken"
        """,
        """
        def status_of(outcome, exc_type):
            if outcome == "failed":
                return "failed" if exc_type == "AssertionError" else "broken"
            return outcome
        """),
    cod(f"{P}-status-e6", t("""
        Реализуй сопоставление с категориями, как делает Allure: функция `categorize(result, categories)` — `result` — словарь `{"status": ..., "message": ...}`, `categories` — список словарей с `name`, `matchedStatuses` и необязательным `messageRegex`. Вернуть имя **первой** подходящей категории: статус входит в `matchedStatuses`, и, если есть `messageRegex`, сообщение ему соответствует целиком (`re.fullmatch`, флаг `re.S`). Если ничего не подошло — `None`.
        """),
        """
        import re


        def categorize(result, categories):
            pass
        """,
        """
        CATS = [
            {"name": "Проблемы окружения", "matchedStatuses": ["broken"], "messageRegex": ".*ConnectionError.*"},
            {"name": "Дефекты продукта", "matchedStatuses": ["failed"]},
            {"name": "Сломанные тесты", "matchedStatuses": ["broken"]},
        ]

        def test_values():
            assert categorize({"status": "broken", "message": "requests.ConnectionError: timeout"}, CATS) == "Проблемы окружения"
            assert categorize({"status": "broken", "message": "KeyError: 'id'"}, CATS) == "Сломанные тесты"
            assert categorize({"status": "failed", "message": "assert 1 == 2"}, CATS) == "Дефекты продукта"
            assert categorize({"status": "passed", "message": ""}, CATS) is None
        """,
        """
        import re


        def categorize(result, categories):
            for cat in categories:
                if result["status"] not in cat["matchedStatuses"]:
                    continue
                pattern = cat.get("messageRegex")
                if pattern and not re.fullmatch(pattern, result.get("message", ""), re.S):
                    continue
                return cat["name"]
            return None
        """),
    cmd(f"{P}-status-e7", "Тест в истории последних прогонов: ✓ ✗ ✓ ✓ ✗. Код не менялся. Как Allure (и тестировщики) называет такой тест? Введи слово латиницей.",
        ["flaky"]),
    cod(f"{P}-status-e8", t("""
        Найди флаки по истории: функция `find_flaky(history)` — `history` — словарь «имя теста → список статусов последних прогонов». Тест флаки, если среди статусов есть и `"passed"`, и `"failed"`/`"broken"`. Вернуть отсортированный список имён.
        """),
        """
        def find_flaky(history):
            pass
        """,
        """
        def test_values():
            h = {
                "test_login": ["passed", "failed", "passed"],
                "test_cart": ["passed", "passed"],
                "test_pay": ["failed", "failed"],
                "test_api": ["broken", "passed"],
            }
            assert find_flaky(h) == ["test_api", "test_login"] and find_flaky({}) == [], find_flaky(h)
        """,
        """
        def find_flaky(history):
            result = []
            for name, statuses in history.items():
                s = set(statuses)
                if "passed" in s and s & {"failed", "broken"}:
                    result.append(name)
            return sorted(result)
        """, xp=20),
),

lesson(f"{P}-junit", "JUnit XML и другие форматы",
    cmd(f"{P}-junit-e1", "Запусти pytest так, чтобы результаты сохранились в формате JUnit XML в файл `report.xml` (его понимают почти все CI).",
        ["pytest --junitxml=report.xml", "pytest --junit-xml=report.xml", "python -m pytest --junitxml=report.xml"]),
    cmd(f"{P}-junit-e2", "Установи плагин для простого HTML-отчёта pytest.",
        ["pip install pytest-html", "python -m pip install pytest-html", "uv add --dev pytest-html"]),
    cmd(f"{P}-junit-e3", "Запусти pytest и сохрани самодостаточный HTML-отчёт в `report.html` (плагин pytest-html установлен).",
        ["pytest --html=report.html --self-contained-html", "pytest --self-contained-html --html=report.html", "pytest --html=report.html"]),
    cmd(f"{P}-junit-e4", "Сколько тестов упало по этому JUnit XML? Введи число.",
        ["1"],
        context="""
        <testsuite name="pytest" tests="5" failures="1" errors="1" skipped="1" time="2.31">
          <testcase classname="tests.test_api" name="test_status" time="0.12"/>
          ...
        </testsuite>
        """, hint="failures — упавшие assert, errors — ошибки (аналог broken)."),
    cod(f"{P}-junit-e5", t("""
        Напиши функцию `junit_summary(xml_text)` — разобрать JUnit XML модулем `xml.etree.ElementTree` и вернуть словарь `{"tests": N, "failures": N, "errors": N, "skipped": N}` из атрибутов корневого `<testsuite>` (числа — int). Если корень — `<testsuites>`, взять первый `<testsuite>` внутри.
        """),
        """
        import xml.etree.ElementTree as ET


        def junit_summary(xml_text):
            pass
        """,
        """
        XML1 = '<testsuite name="pytest" tests="5" failures="1" errors="1" skipped="1" time="2.3"></testsuite>'
        XML2 = '<testsuites><testsuite name="pytest" tests="3" failures="0" errors="0" skipped="0" time="1"/></testsuites>'

        def test_values():
            assert junit_summary(XML1) == {"tests": 5, "failures": 1, "errors": 1, "skipped": 1}, junit_summary(XML1)
            assert junit_summary(XML2) == {"tests": 3, "failures": 0, "errors": 0, "skipped": 0}, junit_summary(XML2)
        """,
        """
        import xml.etree.ElementTree as ET


        def junit_summary(xml_text):
            root = ET.fromstring(xml_text)
            suite = root if root.tag == "testsuite" else root.find("testsuite")
            return {key: int(suite.get(key, 0)) for key in ("tests", "failures", "errors", "skipped")}
        """),
    cod(f"{P}-junit-e6", t("""
        Напиши функцию `failed_cases(xml_text)` — список строк `"classname::name: сообщение"` для каждого `<testcase>`, внутри которого есть `<failure>` или `<error>` (сообщение — атрибут `message`).
        """),
        """
        import xml.etree.ElementTree as ET


        def failed_cases(xml_text):
            pass
        """,
        """
        XML = '''<testsuite tests="3">
          <testcase classname="tests.test_api" name="test_ok" time="0.1"/>
          <testcase classname="tests.test_api" name="test_status" time="0.2"><failure message="assert 500 == 200">...</failure></testcase>
          <testcase classname="tests.test_ui" name="test_login" time="1.0"><error message="TimeoutError">...</error></testcase>
        </testsuite>'''

        def test_values():
            assert failed_cases(XML) == ["tests.test_api::test_status: assert 500 == 200", "tests.test_ui::test_login: TimeoutError"], failed_cases(XML)
        """,
        """
        import xml.etree.ElementTree as ET


        def failed_cases(xml_text):
            result = []
            for case in ET.fromstring(xml_text).iter("testcase"):
                problem = case.find("failure")
                if problem is None:
                    problem = case.find("error")
                if problem is not None:
                    result.append(f"{case.get('classname')}::{case.get('name')}: {problem.get('message')}")
            return result
        """, hint="У Element без детей bool() ложно — сравнивай с None явно."),
    cod(f"{P}-junit-e7", t("""
        Напиши функцию `slowest(xml_text, n)` — `n` самых долгих тестов из JUnit XML как список кортежей `(name, time)` (время — float), по убыванию времени.
        """),
        """
        import xml.etree.ElementTree as ET


        def slowest(xml_text, n):
            pass
        """,
        """
        XML = '''<testsuite>
          <testcase classname="a" name="t1" time="0.5"/>
          <testcase classname="a" name="t2" time="3.25"/>
          <testcase classname="a" name="t3" time="1.0"/>
        </testsuite>'''

        def test_values():
            assert slowest(XML, 2) == [("t2", 3.25), ("t3", 1.0)] and slowest(XML, 0) == [], slowest(XML, 2)
        """,
        """
        import xml.etree.ElementTree as ET


        def slowest(xml_text, n):
            cases = [(c.get("name"), float(c.get("time", 0))) for c in ET.fromstring(xml_text).iter("testcase")]
            return sorted(cases, key=lambda c: -c[1])[:n]
        """),
    cmd(f"{P}-junit-e8", "В каком формате, кроме Allure, почти любой CI (GitHub Actions, GitLab, Jenkins) умеет показывать результаты тестов? Введи название формата.",
        ["JUnit XML", "JUnit", "junit", "junit xml", "JUnit-XML"], xp=15),
),

lesson(f"{P}-summary", "Сводка по результатам",
    cod(f"{P}-summary-e1", t("""
        Напиши функцию `summary(results)` — `results` — список результатов Allure (словари с ключом `"status"`). Вернуть словарь с количеством по статусам `passed`, `failed`, `broken`, `skipped` (все 4 ключа, даже если 0) и `total`.
        """),
        """
        def summary(results):
            pass
        """,
        """
        def test_values():
            res = [{"status": s} for s in ["passed", "passed", "failed", "broken", "passed", "skipped"]]
            assert summary(res) == {"passed": 3, "failed": 1, "broken": 1, "skipped": 1, "total": 6}, summary(res)
            assert summary([]) == {"passed": 0, "failed": 0, "broken": 0, "skipped": 0, "total": 0}
        """,
        """
        def summary(results):
            counts = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0}
            for r in results:
                counts[r["status"]] = counts.get(r["status"], 0) + 1
            counts["total"] = len(results)
            return counts
        """),
    cod(f"{P}-summary-e2", t("""
        Напиши функцию `pass_rate(counts)` — процент успешных тестов (с точностью до одного знака) от **выполненных**: пропущенные не учитываются. `counts` — словарь как из прошлого задания. Если выполненных нет — `0.0`.
        """),
        """
        def pass_rate(counts):
            pass
        """,
        """
        def test_values():
            assert pass_rate({"passed": 3, "failed": 1, "broken": 1, "skipped": 1, "total": 6}) == 60.0
            assert pass_rate({"passed": 2, "failed": 1, "broken": 0, "skipped": 0, "total": 3}) == 66.7
            assert pass_rate({"passed": 0, "failed": 0, "broken": 0, "skipped": 4, "total": 4}) == 0.0
        """,
        """
        def pass_rate(counts):
            executed = counts["passed"] + counts["failed"] + counts["broken"]
            if executed == 0:
                return 0.0
            return round(counts["passed"] * 100 / executed, 1)
        """),
    cod(f"{P}-summary-e3", t("""
        Напиши функцию `load_results(folder)` — прочитать все файлы `*-result.json` в папке (модулем `glob` или `pathlib`) и вернуть список словарей. Проверка сама создаст папку с файлами.
        """),
        """
        import json
        from pathlib import Path


        def load_results(folder):
            pass
        """,
        """
        import json, os

        def test_values():
            os.makedirs("res", exist_ok=True)
            for i, status in enumerate(["passed", "failed"]):
                with open(f"res/{i}-result.json", "w", encoding="utf-8") as f:
                    json.dump({"name": f"t{i}", "status": status}, f)
            with open("res/x-container.json", "w", encoding="utf-8") as f:
                json.dump({"children": []}, f)
            got = sorted(load_results("res"), key=lambda r: r["name"])
            assert got == [{"name": "t0", "status": "passed"}, {"name": "t1", "status": "failed"}], got
        """,
        """
        import json
        from pathlib import Path


        def load_results(folder):
            return [json.loads(p.read_text(encoding="utf-8")) for p in Path(folder).glob("*-result.json")]
        """),
    cod(f"{P}-summary-e4", t("""
        Напиши функцию `by_feature(results)` — сгруппировать упавшие (`failed` и `broken`) тесты по метке `feature`: словарь «feature → список имён», тесты без метки — под ключом `"без feature"`. Порядок имён — как во входном списке.
        """),
        """
        def by_feature(results):
            pass
        """,
        """
        def test_values():
            res = [
                {"name": "a", "status": "failed", "labels": [{"name": "feature", "value": "Корзина"}]},
                {"name": "b", "status": "passed", "labels": [{"name": "feature", "value": "Корзина"}]},
                {"name": "c", "status": "broken", "labels": []},
                {"name": "d", "status": "failed", "labels": [{"name": "feature", "value": "Корзина"}]},
            ]
            assert by_feature(res) == {"Корзина": ["a", "d"], "без feature": ["c"]}, by_feature(res)
        """,
        """
        def by_feature(results):
            groups = {}
            for r in results:
                if r["status"] not in ("failed", "broken"):
                    continue
                features = [l["value"] for l in r.get("labels", []) if l["name"] == "feature"]
                key = features[0] if features else "без feature"
                groups.setdefault(key, []).append(r["name"])
            return groups
        """),
    cod(f"{P}-summary-e5", t("""
        Напиши функцию `duration_sec(result)` — длительность теста в секундах (float, 2 знака) по полям `start` и `stop` результата Allure (миллисекунды). И `total_duration(results)` — сумма по всем тестам (2 знака).
        """),
        """
        def duration_sec(result):
            pass


        def total_duration(results):
            pass
        """,
        """
        def test_values():
            r1 = {"start": 1709899200000, "stop": 1709899201250}
            r2 = {"start": 1709899300000, "stop": 1709899300500}
            assert duration_sec(r1) == 1.25 and total_duration([r1, r2]) == 1.75 and total_duration([]) == 0, (duration_sec(r1), total_duration([r1, r2]))
        """,
        """
        def duration_sec(result):
            return round((result["stop"] - result["start"]) / 1000, 2)


        def total_duration(results):
            return round(sum(duration_sec(r) for r in results), 2)
        """),
    cmd(f"{P}-summary-e6", "Как называется JSON-файл в сгенерированном отчёте с итоговыми цифрами (виджет «Summary»)? Введи путь внутри `allure-report`.",
        ["widgets/summary.json"]),
    cmd(f"{P}-summary-e7", "Выведи из `allure-report/widgets/summary.json` количество упавших тестов утилитой `jq` (поле `.statistic.failed`).",
        ["jq .statistic.failed allure-report/widgets/summary.json", "jq '.statistic.failed' allure-report/widgets/summary.json",
         'jq ".statistic.failed" allure-report/widgets/summary.json', "cat allure-report/widgets/summary.json | jq .statistic.failed",
         "cat allure-report/widgets/summary.json | jq '.statistic.failed'"]),
    cod(f"{P}-summary-e8", t("""
        Напиши функцию `quality_gate(counts, min_rate)` — «ворота качества» для CI: вернуть кортеж `(ok, reason)`. Правила по порядку:

        - есть `broken` → `(False, "есть broken: N")`;
        - процент успешных среди выполненных (без skipped) меньше `min_rate` → `(False, "pass rate X% < Y%")` (X — с одним знаком);
        - иначе `(True, "ok")`.
        """),
        """
        def quality_gate(counts, min_rate):
            pass
        """,
        """
        def test_values():
            assert quality_gate({"passed": 9, "failed": 1, "broken": 0, "skipped": 3}, 90) == (True, "ok")
            assert quality_gate({"passed": 9, "failed": 0, "broken": 2, "skipped": 0}, 50) == (False, "есть broken: 2")
            assert quality_gate({"passed": 8, "failed": 2, "broken": 0, "skipped": 0}, 90) == (False, "pass rate 80.0% < 90%")
        """,
        """
        def quality_gate(counts, min_rate):
            if counts["broken"]:
                return False, f"есть broken: {counts['broken']}"
            executed = counts["passed"] + counts["failed"] + counts["broken"]
            rate = round(counts["passed"] * 100 / executed, 1) if executed else 0.0
            if rate < min_rate:
                return False, f"pass rate {rate}% < {min_rate}%"
            return True, "ok"
        """, xp=25),
),
)
