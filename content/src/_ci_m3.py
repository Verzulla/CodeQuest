"""Тема «CI/CD для тестировщика», модуль 3 «Качество и практика» — задания. Теория — в _ci_t3.py."""
from ._lib import cmd, cod, lesson, module, out, t
from ._ci_m1 import wfy

P = "ci"

GITLAB_LOAD = '''import yaml


def gl():
    return yaml.safe_load(GITLAB_CI) or {}


'''


def gly(body):
    from textwrap import dedent
    return GITLAB_LOAD + dedent(body)


m3 = module(f"{P}-m3", "Качество и практика", "🏁", "GitLab CI, quality gates и покрытие, отчёты и уведомления, итоговый пайплайн автотестов",

lesson(f"{P}-gitlab", "GitLab CI",
    out(f"{P}-gitlab-e1", "Что выведет программа? В GitLab CI job-ы группируются по стадиям (`stages`): стадии идут по очереди, job-ы одной стадии — параллельно.", """
        import yaml

        ci = yaml.safe_load('''
        stages: [lint, test, report]
        ruff:
          stage: lint
          script: [ruff check .]
        api:
          stage: test
          script: [pytest tests/api]
        ui:
          stage: test
          script: [pytest tests/ui]
        ''')
        for stage in ci["stages"]:
            jobs = [name for name, job in ci.items() if isinstance(job, dict) and job.get("stage") == stage]
            print(stage, jobs)
        """),
    cod(f"{P}-gitlab-e2", t("""
        Напиши `.gitlab-ci.yml` строкой `GITLAB_CI`:

        - `stages: [lint, test]`;
        - job `ruff`: `stage: lint`, `image: python:3.12-slim`, `script: ["pip install ruff", "ruff check ."]`;
        - job `pytest`: `stage: test`, `image: python:3.12-slim`, `script: ["pip install -r requirements.txt", "pytest --junitxml=report.xml"]`, и отчёт для GitLab:
        ```yaml
        artifacts:
          when: always
          reports:
            junit: report.xml
        ```
        """),
        '''
        GITLAB_CI = """
        stages: [lint, test]
        """
        ''',
        gly("""
        def test_stages():
            assert gl().get("stages") == ["lint", "test"], "stages: [lint, test]"

        def test_ruff():
            job = gl().get("ruff") or {}
            assert job.get("stage") == "lint" and job.get("image") == "python:3.12-slim", "ruff: stage lint, image python:3.12-slim"
            assert job.get("script") == ["pip install ruff", "ruff check ."], job.get("script")

        def test_pytest():
            job = gl().get("pytest") or {}
            assert job.get("stage") == "test", "pytest: stage test"
            assert job.get("script") == ["pip install -r requirements.txt", "pytest --junitxml=report.xml"], job.get("script")
            art = job.get("artifacts") or {}
            assert art.get("when") == "always" and (art.get("reports") or {}).get("junit") == "report.xml", "artifacts: when always, reports.junit report.xml"
        """),
        '''
        GITLAB_CI = """
        stages: [lint, test]

        ruff:
          stage: lint
          image: python:3.12-slim
          script:
            - pip install ruff
            - ruff check .

        pytest:
          stage: test
          image: python:3.12-slim
          script:
            - pip install -r requirements.txt
            - pytest --junitxml=report.xml
          artifacts:
            when: always
            reports:
              junit: report.xml
        """
        ''', xp=20),
    cod(f"{P}-gitlab-e3", t("""
        Напиши функцию `gitlab_plan(ci)`: по разобранному `.gitlab-ci.yml` (словарь) вернуть план — список пар `(стадия, [job-ы стадии по алфавиту])` в порядке `stages`.

        - Job — любой ключ верхнего уровня со словарём, где есть `script`; служебные ключи (`stages`, `variables`, `default`, имена на `.`) — не job-ы.
        - У job-а без `stage` стадия по умолчанию — `test`.
        - Стадии без job-ов в план не попадают.
        """),
        """
        def gitlab_plan(ci):
            pass
        """,
        """
        CI = {
            "stages": ["build", "test", "deploy"],
            "variables": {"PY": "3.12"},
            ".base": {"image": "python", "script": ["x"]},
            "unit": {"script": ["pytest"]},
            "api": {"stage": "test", "script": ["pytest tests/api"]},
            "image": {"stage": "build", "script": ["docker build ."]},
        }

        def test_plan():
            assert gitlab_plan(CI) == [("build", ["image"]), ("test", ["api", "unit"])], gitlab_plan(CI)
        """,
        """
        def gitlab_plan(ci):
            jobs = {name: job for name, job in ci.items()
                    if isinstance(job, dict) and "script" in job and not name.startswith(".")}
            plan = []
            for stage in ci.get("stages", []):
                names = sorted(n for n, j in jobs.items() if j.get("stage", "test") == stage)
                if names:
                    plan.append((stage, names))
            return plan
        """, xp=20),
    cod(f"{P}-gitlab-e4", t("""
        В GitLab правила запуска job-а задают `rules`. Добавь в `GITLAB_CI` job `ui-tests` (`stage: test`, `script: ["pytest tests/ui"]`) с правилами:

        ```yaml
        rules:
          - if: $CI_PIPELINE_SOURCE == "schedule"
          - if: $CI_COMMIT_BRANCH == "main"
            when: manual
        ```
        По расписанию — автоматически, в `main` — по кнопке, в остальных случаях — не запускать.
        """),
        '''
        GITLAB_CI = """
        stages: [test]
        """
        ''',
        gly("""
        def test_rules():
            job = gl().get("ui-tests") or {}
            assert job.get("stage") == "test" and job.get("script") == ["pytest tests/ui"], "ui-tests: stage test, script pytest tests/ui"
            rules = job.get("rules") or []
            assert len(rules) == 2, "Два правила"
            assert rules[0] == {"if": '$CI_PIPELINE_SOURCE == "schedule"'}, rules[0]
            assert rules[1] == {"if": '$CI_COMMIT_BRANCH == "main"', "when": "manual"}, rules[1]
        """),
        '''
        GITLAB_CI = """
        stages: [test]

        ui-tests:
          stage: test
          script:
            - pytest tests/ui
          rules:
            - if: $CI_PIPELINE_SOURCE == "schedule"
            - if: $CI_COMMIT_BRANCH == "main"
              when: manual
        """
        '''),
    cmd(f"{P}-gitlab-e5", "Как в GitLab CI называется переменная с **именем текущей ветки**? Введи её с `$`.",
        ["$CI_COMMIT_BRANCH", "$CI_COMMIT_REF_NAME"],
        hint="Все предопределённые переменные начинаются с `CI_`."),
    cmd(f"{P}-gitlab-e6", "Как в GitLab CI называется переменная с **полным хешем коммита**? Введи её с `$`.",
        ["$CI_COMMIT_SHA"],
        hint="`CI_COMMIT_…`."),
    out(f"{P}-gitlab-e7", "Что выведет программа? Шаблоны в GitLab: скрытый job `.base` (имя с точки) не запускается, а `extends` берёт из него настройки.", """
        base = {"image": "python:3.12-slim", "before_script": ["pip install -r requirements.txt"]}
        api = {"extends": ".base", "script": ["pytest tests/api"]}

        resolved = {**base, **{k: v for k, v in api.items() if k != "extends"}}
        for key in sorted(resolved):
            print(key, resolved[key])
        """),
    cod(f"{P}-gitlab-e8", t("""
        Напиши функцию `resolve_extends(ci, name)`: вернуть настройки job-а `name` с учётом `extends` (строка — одно имя шаблона). Шаблон сам может иметь `extends` — разворачивай рекурсивно. Ключи job-а перекрывают ключи шаблона; ключа `extends` в результате быть не должно.

        Пример:
        ```
        ci = {
            ".py": {"image": "python:3.12-slim", "tags": ["docker"]},
            ".tests": {"extends": ".py", "before_script": ["pip install -r requirements.txt"]},
            "api": {"extends": ".tests", "script": ["pytest tests/api"], "tags": ["fast"]},
        }
        resolve_extends(ci, "api")
        # → {"image": "python:3.12-slim", "tags": ["fast"], "before_script": ["pip install -r requirements.txt"], "script": ["pytest tests/api"]}
        ```
        """),
        """
        def resolve_extends(ci, name):
            pass
        """,
        """
        CI = {
            ".py": {"image": "python:3.12-slim", "tags": ["docker"]},
            ".tests": {"extends": ".py", "before_script": ["pip install -r requirements.txt"]},
            "api": {"extends": ".tests", "script": ["pytest tests/api"], "tags": ["fast"]},
            "lint": {"script": ["ruff check ."]},
        }

        def test_chain():
            got = resolve_extends(CI, "api")
            assert got == {"image": "python:3.12-slim", "tags": ["fast"], "before_script": ["pip install -r requirements.txt"], "script": ["pytest tests/api"]}, got

        def test_plain():
            assert resolve_extends(CI, "lint") == {"script": ["ruff check ."]}
        """,
        """
        def resolve_extends(ci, name):
            job = dict(ci[name])
            parent = job.pop("extends", None)
            if parent is None:
                return job
            return {**resolve_extends(ci, parent), **job}
        """),
),

lesson(f"{P}-gates", "Quality gates и покрытие",
    cmd(f"{P}-gates-e1", "Запусти тесты с замером покрытия пакета `app` (pytest-cov) так, чтобы прогон **упал**, если покрытие ниже 80%.",
        ["pytest --cov=app --cov-fail-under=80", "pytest --cov app --cov-fail-under 80", "pytest --cov-fail-under=80 --cov=app", "python -m pytest --cov=app --cov-fail-under=80"],
        hint="`--cov=пакет` и `--cov-fail-under=N`."),
    cod(f"{P}-gates-e2", t("""
        Отчёт покрытия в формате Cobertura (`pytest --cov --cov-report=xml` → `coverage.xml`) хранит долю покрытых строк в атрибуте `line-rate` корневого тега `<coverage>` — число от 0 до 1.

        Напиши функцию `coverage_percent(xml_text)`: вернуть покрытие в процентах, округлённое до одного знака (`round(..., 1)`).

        Пример: `<coverage line-rate="0.8347" …>` → `83.5`.
        """),
        """
        import xml.etree.ElementTree as ET


        def coverage_percent(xml_text):
            pass
        """,
        """
        def test_percent():
            xml = '<?xml version="1.0" ?><coverage line-rate="0.8347" branch-rate="0" version="7.6"><packages/></coverage>'
            assert coverage_percent(xml) == 83.5, coverage_percent(xml)
            assert coverage_percent('<coverage line-rate="1"/>') == 100.0
        """,
        """
        import xml.etree.ElementTree as ET


        def coverage_percent(xml_text):
            root = ET.fromstring(xml_text)
            return round(float(root.get("line-rate")) * 100, 1)
        """),
    cod(f"{P}-gates-e3", t("""
        **Quality gate** — правила, при нарушении которых пайплайн красный, даже если «всё запустилось». Напиши функцию `gate(stats, rules)`:

        - `stats` — `{"passed": …, "failed": …, "skipped": …, "coverage": …, "duration": …}` (секунды);
        - `rules` — `{"max_failed": …, "min_coverage": …, "max_skipped_share": …, "max_duration": …}`; любого правила может не быть — тогда оно не проверяется;
        - доля пропущенных — `skipped / (passed + failed + skipped)`.

        Возвращает список нарушений (строки) в порядке правил выше:
        `"failed 3 > 0"`, `"coverage 75.0 < 80"`, `"skipped 25% > 10%"` (проценты целые, `round`), `"duration 700 > 600"`. Пустой список — gate пройден.
        """),
        """
        def gate(stats, rules):
            pass
        """,
        """
        S = {"passed": 12, "failed": 3, "skipped": 5, "coverage": 75.0, "duration": 700}

        def test_violations():
            rules = {"max_failed": 0, "min_coverage": 80, "max_skipped_share": 0.1, "max_duration": 600}
            assert gate(S, rules) == ["failed 3 > 0", "coverage 75.0 < 80", "skipped 25% > 10%", "duration 700 > 600"], gate(S, rules)

        def test_partial():
            assert gate(S, {"min_coverage": 70}) == []
            assert gate(S, {"max_failed": 5, "max_duration": 700}) == []
        """,
        """
        def gate(stats, rules):
            problems = []
            if "max_failed" in rules and stats["failed"] > rules["max_failed"]:
                problems.append(f"failed {stats['failed']} > {rules['max_failed']}")
            if "min_coverage" in rules and stats["coverage"] < rules["min_coverage"]:
                problems.append(f"coverage {stats['coverage']} < {rules['min_coverage']}")
            total = stats["passed"] + stats["failed"] + stats["skipped"]
            if "max_skipped_share" in rules and total and stats["skipped"] / total > rules["max_skipped_share"]:
                problems.append(f"skipped {round(100 * stats['skipped'] / total)}% > {round(100 * rules['max_skipped_share'])}%")
            if "max_duration" in rules and stats["duration"] > rules["max_duration"]:
                problems.append(f"duration {stats['duration']} > {rules['max_duration']}")
            return problems
        """, xp=20),
    out(f"{P}-gates-e4", "Что выведет программа? Флаки-тест в карантине: его падение не ломает пайплайн, но попадает в отчёт.", """
        quarantine = {"test_payment_timeout"}
        results = {"test_login": "passed", "test_payment_timeout": "failed", "test_cart": "passed"}

        real = [t for t, r in results.items() if r == "failed" and t not in quarantine]
        known = [t for t, r in results.items() if r == "failed" and t in quarantine]
        print("упали:", real)
        print("в карантине:", known)
        print("пайплайн:", "красный" if real else "зелёный")
        """),
    cod(f"{P}-gates-e5", t("""
        Напиши функцию `new_failures(before, after)` — сравнить прогон ветки с прогоном `main`:

        - `before`, `after` — словари `{тест: "passed" | "failed" | "skipped"}` (main и ветка);
        - вернуть словарь из трёх **отсортированных** списков:
          - `"new"` — упали в ветке, а в main не падали (прошли, пропущены или их не было);
          - `"fixed"` — в main падали, а в ветке прошли;
          - `"still"` — падают и там, и там.

        Блокировать слияние обычно стоит именно за `"new"`.
        """),
        """
        def new_failures(before, after):
            pass
        """,
        """
        def test_diff():
            before = {"a": "passed", "b": "failed", "c": "failed", "d": "skipped"}
            after = {"a": "failed", "b": "passed", "c": "failed", "d": "failed", "e": "failed"}
            assert new_failures(before, after) == {"new": ["a", "d", "e"], "fixed": ["b"], "still": ["c"]}, new_failures(before, after)
        """,
        """
        def new_failures(before, after):
            failed_before = {t for t, r in before.items() if r == "failed"}
            failed_after = {t for t, r in after.items() if r == "failed"}
            fixed = {t for t in failed_before if after.get(t) == "passed"}
            return {"new": sorted(failed_after - failed_before),
                    "fixed": sorted(fixed),
                    "still": sorted(failed_after & failed_before)}
        """),
    cmd(f"{P}-gates-e6", "Линтер в CI: проверь код линтером ruff **и** что он отформатирован (без изменения файлов). Две команды через `&&`.",
        ["ruff check . && ruff format --check .", "ruff format --check . && ruff check .", "ruff check && ruff format --check"],
        hint="`ruff format --check` только проверяет."),
    cod(f"{P}-gates-e7", t("""
        Напиши функцию `slowest(junit_xml, n)`: из отчёта JUnit XML вернуть `n` самых медленных тестов — список пар `(имя, время)` по убыванию времени. Время — атрибут `time` у `<testcase>` (дробное число). Медленные тесты — первые кандидаты на оптимизацию пайплайна.
        """),
        """
        import xml.etree.ElementTree as ET


        def slowest(junit_xml, n):
            pass
        """,
        """
        R = '''<testsuites><testsuite>
          <testcase name="test_a" time="0.2"/>
          <testcase name="test_ui_checkout" time="14.8"/>
          <testcase name="test_b" time="1.5"/>
        </testsuite><testsuite><testcase name="test_ui_login" time="9.25"/></testsuite></testsuites>'''

        def test_top():
            assert slowest(R, 2) == [("test_ui_checkout", 14.8), ("test_ui_login", 9.25)], slowest(R, 2)
            assert len(slowest(R, 10)) == 4
        """,
        """
        import xml.etree.ElementTree as ET


        def slowest(junit_xml, n):
            cases = [(c.get("name"), float(c.get("time", 0))) for c in ET.fromstring(junit_xml).iter("testcase")]
            return sorted(cases, key=lambda c: c[1], reverse=True)[:n]
        """),
    cmd(f"{P}-gates-e8", "Покажи в выводе pytest **10 самых медленных** тестов прогона.",
        ["pytest --durations=10", "pytest --durations 10", "python -m pytest --durations=10"],
        hint="Опция `--durations=N`."),
),

lesson(f"{P}-notify", "Отчёты и уведомления",
    cmd(f"{P}-notify-e1", "В CI тесты сложили результаты в `allure-results`. Сгенерируй из них HTML-отчёт в папку `allure-report`, очистив старый.",
        ["allure generate allure-results -o allure-report --clean", "allure generate allure-results --clean -o allure-report",
         "allure generate --clean allure-results -o allure-report", "allure generate allure-results -o allure-report -c"],
        hint="`allure generate <результаты> -o <отчёт> --clean`."),
    cod(f"{P}-notify-e2", t("""
        Напиши функцию `chat_message(summary, url)` — текст уведомления в рабочий чат после прогона.

        - `summary` — `{"branch": …, "passed": …, "failed": …, "skipped": …, "failed_names": [...]}`;
        - формат (строки через `\\n`):
        ```
        ❌ main: 2 упало, 40 прошло, 1 пропущено
        • test_login
        • test_cart
        Отчёт: https://ci.example/run/1
        ```
        - если упавших нет — первая строка начинается с `✅`, а строк с `•` нет;
        - упавших в сообщении не больше **5**; если их больше — после пятой строка `…и ещё N`.
        """),
        """
        def chat_message(summary, url):
            pass
        """,
        """
        def test_red():
            s = {"branch": "main", "passed": 40, "failed": 2, "skipped": 1, "failed_names": ["test_login", "test_cart"]}
            assert chat_message(s, "https://ci.example/run/1") == "❌ main: 2 упало, 40 прошло, 1 пропущено\\n• test_login\\n• test_cart\\nОтчёт: https://ci.example/run/1", repr(chat_message(s, "https://ci.example/run/1"))

        def test_green():
            s = {"branch": "dev", "passed": 5, "failed": 0, "skipped": 0, "failed_names": []}
            assert chat_message(s, "u") == "✅ dev: 0 упало, 5 прошло, 0 пропущено\\nОтчёт: u"

        def test_many():
            names = [f"t{i}" for i in range(8)]
            msg = chat_message({"branch": "b", "passed": 0, "failed": 8, "skipped": 0, "failed_names": names}, "u")
            assert msg.count("•") == 5 and "…и ещё 3" in msg, msg
        """,
        """
        def chat_message(summary, url):
            icon = "❌" if summary["failed"] else "✅"
            lines = [f"{icon} {summary['branch']}: {summary['failed']} упало, {summary['passed']} прошло, {summary['skipped']} пропущено"]
            names = summary["failed_names"]
            lines += [f"• {name}" for name in names[:5]]
            if len(names) > 5:
                lines.append(f"…и ещё {len(names) - 5}")
            lines.append(f"Отчёт: {url}")
            return "\\n".join(lines)
        """, xp=20),
    out(f"{P}-notify-e3", "Что выведет программа? Тело запроса к вебхуку чата — JSON; `ensure_ascii=False` сохраняет кириллицу читаемой.", """
        import json

        payload = {"text": "❌ main: 2 упало", "link": "https://ci.example/run/1"}
        print(json.dumps(payload))
        print(json.dumps(payload, ensure_ascii=False))
        """),
    cod(f"{P}-notify-e4", t("""
        Уведомлять на **каждый** прогон — шум, который быстро перестают читать. Напиши функцию `should_notify(prev, cur)`:

        - `prev`, `cur` — статусы прошлого и текущего прогона ветки: `"success"` или `"failure"` (`prev` может быть `None` — первый прогон);
        - уведомлять, если текущий упал (`failure`) **или** если статус изменился (починили: `failure` → `success`);
        - первый прогон — уведомлять, только если он упал.
        """),
        """
        def should_notify(prev, cur):
            pass
        """,
        """
        def test_rules():
            assert should_notify("success", "failure") is True
            assert should_notify("failure", "failure") is True
            assert should_notify("failure", "success") is True, "Починили — сообщить"
            assert should_notify("success", "success") is False, "Зелёный после зелёного — тишина"
            assert should_notify(None, "success") is False and should_notify(None, "failure") is True
        """,
        """
        def should_notify(prev, cur):
            if cur == "failure":
                return True
            return prev is not None and prev != cur
        """),
    cmd(f"{P}-notify-e5", "Отправь уведомление в вебхук чата: POST-запрос с JSON `{\"text\": \"tests failed\"}` на адрес из переменной `WEBHOOK_URL` через `curl`.",
        ["curl -X POST -H \"Content-Type: application/json\" -d '{\"text\": \"tests failed\"}' $WEBHOOK_URL",
         "curl -X POST -H 'Content-Type: application/json' -d '{\"text\": \"tests failed\"}' $WEBHOOK_URL",
         "curl -X POST -H \"Content-Type: application/json\" -d '{\"text\": \"tests failed\"}' \"$WEBHOOK_URL\"",
         "curl -H \"Content-Type: application/json\" -d '{\"text\": \"tests failed\"}' $WEBHOOK_URL",
         "curl -X POST --json '{\"text\": \"tests failed\"}' $WEBHOOK_URL",
         "curl --json '{\"text\": \"tests failed\"}' $WEBHOOK_URL"],
        hint="`curl -X POST -H \"Content-Type: application/json\" -d '<json>' $WEBHOOK_URL`."),
    cod(f"{P}-notify-e6", t("""
        Allure хранит историю, если перед генерацией скопировать папку `history` прошлого отчёта в новые результаты. Напиши функцию `trend(history, current)` для графика «динамика прогонов»:

        - `history` — список прошлых прогонов `{"passed": …, "failed": …}` от старых к новым;
        - `current` — текущий прогон;
        - вернуть список строк — последние **5** прогонов с текущим включительно, по строке на прогон: `"<номер> <полоска>"`, где номер — порядковый с 1 по всей истории, полоска — `"█"` × passed // 10 и `"░"` × failed // 10 (округление вниз).
        """),
        """
        def trend(history, current):
            pass
        """,
        """
        def test_trend():
            history = [{"passed": 50, "failed": 0}] * 5
            got = trend(history, {"passed": 30, "failed": 20})
            assert got == ["2 █████", "3 █████", "4 █████", "5 █████", "6 ███░░"], got

        def test_short():
            assert trend([], {"passed": 19, "failed": 9}) == ["1 █"]
        """,
        """
        def trend(history, current):
            runs = history + [current]
            start = max(0, len(runs) - 5)
            return [f"{i + 1} " + "█" * (r["passed"] // 10) + "░" * (r["failed"] // 10)
                    for i, r in enumerate(runs) if i >= start]
        """),
    cmd(f"{P}-notify-e7", "Сохрани историю Allure между прогонами: перед генерацией скопируй папку `allure-report/history` прошлого отчёта в `allure-results/`.",
        ["cp -r allure-report/history allure-results/", "cp -r allure-report/history allure-results", "cp -R allure-report/history allure-results/",
         "cp -R allure-report/history allure-results"],
        hint="`cp -r откуда куда`."),
    cod(f"{P}-notify-e8", t("""
        Напиши workflow `WORKFLOW`, который после тестов (даже упавших) публикует отчёт Allure. Job `tests` (`ubuntu-latest`), шаги по порядку:

        1. `uses: actions/checkout@v4`;
        2. `run: pytest --alluredir=allure-results`;
        3. `run: allure generate allure-results -o allure-report --clean` с `if: always()`;
        4. `uses: actions/upload-artifact@v4` с `if: always()` и `with: {name: allure-report, path: allure-report/}`.
        """),
        '''
        WORKFLOW = """
        name: allure
        on: [push]
        jobs:
          tests:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
        """
        ''',
        wfy("""
        def cond(step):
            return str(step.get("if", "")).replace("${{", "").replace("}}", "").strip()

        def test_steps():
            s = steps("tests")
            kinds = [x.get("uses", "").split("@")[0] or x.get("run", "") for x in s]
            assert kinds == ["actions/checkout", "pytest --alluredir=allure-results", "allure generate allure-results -o allure-report --clean", "actions/upload-artifact"], kinds
            assert cond(s[2]) == "always()" and cond(s[3]) == "always()", "Генерация и выгрузка — с if: always()"
            assert (s[3].get("with") or {}) == {"name": "allure-report", "path": "allure-report/"}
        """),
        '''
        WORKFLOW = """
        name: allure
        on: [push]
        jobs:
          tests:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - run: pytest --alluredir=allure-results
              - run: allure generate allure-results -o allure-report --clean
                if: always()
              - uses: actions/upload-artifact@v4
                if: always()
                with:
                  name: allure-report
                  path: allure-report/
        """
        '''),
),

lesson(f"{P}-practice", "Практика: пайплайн автотестов",
    cod(f"{P}-practice-e1", t("""
        Итоговый workflow `WORKFLOW` для проекта автотестов:

        - триггеры: `push` в `main` и любой `pull_request`;
        - job `lint`: `ubuntu-latest`, шаги `actions/checkout@v4`, `run: pip install ruff`, `run: ruff check .`;
        - job `api`: `needs: lint`, `ubuntu-latest`, шаги `actions/checkout@v4`, `run: pip install -r requirements.txt`, `run: pytest tests/api --junitxml=reports/api.xml`, выгрузка `reports/` через `actions/upload-artifact@v4` с `if: always()` (имя `api-reports`);
        - job `ui`: `needs: api`, матрица `browser: [chromium, firefox]` с `fail-fast: false`, шаг тестов `run: pytest tests/ui --browser ${{ matrix.browser }}`.
        """),
        '''
        WORKFLOW = """
        name: autotests
        on:
          push:
            branches: [main]
          pull_request:
        jobs:
          lint:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
        """
        ''',
        wfy("""
        def as_list(v):
            return [v] if isinstance(v, str) else list(v or [])

        def test_triggers():
            on = wf().get("on") or {}
            assert (on.get("push") or {}).get("branches") == ["main"] and "pull_request" in on, "push в main и pull_request"

        def test_lint():
            runs = [s.get("run") for s in steps("lint")]
            assert steps("lint")[0].get("uses") == "actions/checkout@v4" and "ruff check ." in runs, "lint: checkout и ruff check ."

        def test_api():
            job = wf()["jobs"]["api"]
            assert as_list(job.get("needs")) == ["lint"], "api: needs lint"
            runs = [s.get("run") for s in job["steps"]]
            assert "pytest tests/api --junitxml=reports/api.xml" in runs, "api: pytest с отчётом"
            up = [s for s in job["steps"] if str(s.get("uses", "")).startswith("actions/upload-artifact")]
            assert up and str(up[0].get("if", "")).replace("${{", "").replace("}}", "").strip() == "always()", "api: выгрузка отчёта с if: always()"
            assert (up[0].get("with") or {}).get("name") == "api-reports" and (up[0].get("with") or {}).get("path") == "reports/"

        def test_ui():
            job = wf()["jobs"]["ui"]
            assert as_list(job.get("needs")) == ["api"], "ui: needs api"
            st = job.get("strategy") or {}
            assert st.get("fail-fast") is False and (st.get("matrix") or {}).get("browser") == ["chromium", "firefox"], "ui: матрица браузеров, fail-fast false"
            assert any(str(s.get("run", "")).replace(" ", "") == "pytesttests/ui--browser${{matrix.browser}}" for s in job["steps"]), "ui: pytest tests/ui --browser ${{ matrix.browser }}"
        """),
        '''
        WORKFLOW = """
        name: autotests
        on:
          push:
            branches: [main]
          pull_request:
        jobs:
          lint:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - run: pip install ruff
              - run: ruff check .
          api:
            needs: lint
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - run: pip install -r requirements.txt
              - run: pytest tests/api --junitxml=reports/api.xml
              - uses: actions/upload-artifact@v4
                if: always()
                with:
                  name: api-reports
                  path: reports/
          ui:
            needs: api
            runs-on: ubuntu-latest
            strategy:
              fail-fast: false
              matrix:
                browser: [chromium, firefox]
            steps:
              - uses: actions/checkout@v4
              - run: pip install -r requirements.txt
              - run: pytest tests/ui --browser ${{ matrix.browser }}
        """
        ''', xp=30),
    cod(f"{P}-practice-e2", t("""
        Напиши функцию `lint_workflow(wf)` — проверку workflow на типичные ошибки (получает уже разобранный словарь). Возвращает **отсортированный** список кодов:

        - `"no-checkout"` — есть job, в шагах которого нет `uses`, начинающегося с `actions/checkout`;
        - `"unpinned-action"` — есть `uses` без версии после `@` (например, `actions/checkout`);
        - `"artifact-not-always"` — есть шаг `actions/upload-artifact…` без `if`, содержащего `always()`;
        - `"no-timeout"` — есть job без `timeout-minutes` (зависший тест съест 6 часов).

        Каждый код — не больше одного раза.
        """),
        """
        def lint_workflow(wf):
            pass
        """,
        """
        BAD = {"jobs": {
            "a": {"steps": [{"run": "pytest"}, {"uses": "actions/upload-artifact@v4", "with": {"path": "r"}}]},
            "b": {"timeout-minutes": 20, "steps": [{"uses": "actions/checkout"}]},
        }}
        GOOD = {"jobs": {"t": {"timeout-minutes": 30, "steps": [
            {"uses": "actions/checkout@v4"}, {"run": "pytest"},
            {"uses": "actions/upload-artifact@v4", "if": "${{ always() }}"}]}}}

        def test_bad():
            assert lint_workflow(BAD) == ["artifact-not-always", "no-checkout", "no-timeout", "unpinned-action"], lint_workflow(BAD)

        def test_good():
            assert lint_workflow(GOOD) == []
        """,
        """
        def lint_workflow(wf):
            problems = set()
            for job in wf.get("jobs", {}).values():
                steps = job.get("steps", [])
                uses = [s.get("uses", "") for s in steps if s.get("uses")]
                if not any(u.startswith("actions/checkout") for u in uses):
                    problems.add("no-checkout")
                if any("@" not in u for u in uses):
                    problems.add("unpinned-action")
                for s in steps:
                    if s.get("uses", "").startswith("actions/upload-artifact") and "always()" not in str(s.get("if", "")):
                        problems.add("artifact-not-always")
                if "timeout-minutes" not in job:
                    problems.add("no-timeout")
            return sorted(problems)
        """, xp=20),
    out(f"{P}-practice-e3", "Что выведет программа? Итог пайплайна по job-ам: одно падение — весь пайплайн красный, а зависимые job-ы пропущены.", """
        jobs = {"lint": "success", "api": "failure", "ui": "skipped", "report": "success"}
        icons = {"success": "✅", "failure": "❌", "skipped": "⏭️"}
        print(" ".join(f"{icons[s]} {name}" for name, s in jobs.items()))
        overall = "failure" if "failure" in jobs.values() else "success"
        print("итог:", overall)
        """),
    cod(f"{P}-practice-e4", t("""
        Напиши функцию `parse_junit(xml_text)` — сводку JUnit XML для уведомления: словарь `{"passed": …, "failed": …, "skipped": …, "failed_names": [...]}`.

        - `<testcase>` с вложенным `<failure>` или `<error>` — упал; с `<skipped>` — пропущен; иначе — прошёл.
        - `failed_names` — имена упавших в формате `classname::name` (атрибуты тега), в порядке отчёта.
        """),
        """
        import xml.etree.ElementTree as ET


        def parse_junit(xml_text):
            pass
        """,
        """
        R = '''<testsuites><testsuite name="pytest">
          <testcase classname="tests.test_api" name="test_get" time="0.1"/>
          <testcase classname="tests.test_api" name="test_post" time="0.2"><failure message="422"/></testcase>
          <testcase classname="tests.test_ui" name="test_login" time="3"><error message="Timeout"/></testcase>
          <testcase classname="tests.test_ui" name="test_old" time="0"><skipped/></testcase>
        </testsuite></testsuites>'''

        def test_parse():
            assert parse_junit(R) == {"passed": 1, "failed": 2, "skipped": 1,
                                      "failed_names": ["tests.test_api::test_post", "tests.test_ui::test_login"]}, parse_junit(R)
        """,
        """
        import xml.etree.ElementTree as ET


        def parse_junit(xml_text):
            summary = {"passed": 0, "failed": 0, "skipped": 0, "failed_names": []}
            for case in ET.fromstring(xml_text).iter("testcase"):
                if case.find("failure") is not None or case.find("error") is not None:
                    summary["failed"] += 1
                    summary["failed_names"].append(f"{case.get('classname')}::{case.get('name')}")
                elif case.find("skipped") is not None:
                    summary["skipped"] += 1
                else:
                    summary["passed"] += 1
            return summary
        """, xp=20),
    cmd(f"{P}-practice-e5", "Упавший в CI тест нужно воспроизвести локально. Запусти только его: файл `tests/ui/test_cart.py`, тест `test_remove_item`, с подробным выводом.",
        ["pytest tests/ui/test_cart.py::test_remove_item -v", "pytest -v tests/ui/test_cart.py::test_remove_item",
         "python -m pytest tests/ui/test_cart.py::test_remove_item -v", "pytest tests/ui/test_cart.py::test_remove_item -vv"],
        hint="`pytest путь::тест -v`."),
    cmd(f"{P}-practice-e6", "Шаг workflow не должен висеть вечно. Как называется ключ job-а (или шага), который ограничивает время выполнения в минутах? Введи ключ.",
        ["timeout-minutes", "timeout-minutes:"],
        hint="`timeout-…`."),
    cod(f"{P}-practice-e7", t("""
        Напиши функцию `retry_report(attempts)`. При перезапусках (`--reruns`) один тест может пройти не с первой попытки — это флаки, о них надо знать, даже если пайплайн зелёный.

        - `attempts` — словарь `{тест: [результаты попыток по порядку]}`, результаты — `"passed"`/`"failed"`;
        - вернуть `{"passed": [...], "flaky": [...], "failed": [...]}` — отсортированные списки:
          - `passed` — прошёл с первой попытки;
          - `flaky` — сначала падал, потом прошёл;
          - `failed` — упал во всех попытках.
        """),
        """
        def retry_report(attempts):
            pass
        """,
        """
        def test_report():
            got = retry_report({"t_login": ["passed"], "t_pay": ["failed", "passed"], "t_cart": ["failed", "failed", "failed"], "t_a": ["failed", "failed", "passed"]})
            assert got == {"passed": ["t_login"], "flaky": ["t_a", "t_pay"], "failed": ["t_cart"]}, got
        """,
        """
        def retry_report(attempts):
            report = {"passed": [], "flaky": [], "failed": []}
            for name, results in attempts.items():
                if results[0] == "passed":
                    report["passed"].append(name)
                elif "passed" in results:
                    report["flaky"].append(name)
                else:
                    report["failed"].append(name)
            return {k: sorted(v) for k, v in report.items()}
        """),
    cmd(f"{P}-practice-e8", "Защита ветки: пайплайн должен быть зелёным перед слиянием. Как в GitHub называется такая настройка ветки — «Require … checks to pass»? Введи пропущенное слово.",
        ["status", "status checks"],
        hint="«Require status checks to pass before merging»."),
),
)
