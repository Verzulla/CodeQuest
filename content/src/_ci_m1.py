"""Тема «CI/CD для тестировщика», модуль 1 «Основы CI/CD» — задания. Теория — в _ci_t1.py.

Урок dci-m2-l1 унаследован от старой темы «Docker и CI/CD» — так сохраняется прогресс.
Workflow ученик пишет строкой YAML, проверки разбирают её PyYAML (ключ on YAML 1.1 читает как True —
WF_LOAD это исправляет)."""
from textwrap import dedent

from ._lib import cmd, cod, lesson, module, out, t

P = "ci"
O = "dci"

# Разбор workflow в проверках: YAML → dict, ключ True (так PyYAML читает «on:») → "on".
WF_LOAD = '''import yaml


def wf(text=None):
    data = yaml.safe_load(WORKFLOW if text is None else text) or {}
    if True in data:
        data["on"] = data.pop(True)
    return data


def steps(job):
    return wf()["jobs"][job].get("steps", [])


'''


def wfy(body):
    """Проверки задания «напиши workflow»: загрузчик YAML + тесты."""
    return WF_LOAD + dedent(body)


m1 = module(f"{P}-m1", "Основы CI/CD", "🔁", "Пайплайн и коды выхода, события запуска, job-ы и параллельность, артефакты, кэш и отчёты",

lesson(f"{O}-m2-l1", "Пайплайн",
    out(f"{O}-m2-l1-e1", "Что выведет программа? Имитация пайплайна с fail fast.", """
            jobs = [("lint", 0), ("unit", 0), ("api-tests", 1), ("ui-tests", 0), ("deploy", 0)]
            for name, code in jobs:
                if code != 0:
                    print("❌", name)
                    break
                print("✅", name)
            else:
                print("🚀 всё зелёное")
            """, hint="`else` у цикла выполняется, только если не было break."),
    cod(f"{O}-m2-l1-e2", t("""
            Напиши функцию `pipeline_status(jobs)`, которая вычисляет итог CI-пайплайна.

            - Получает: `jobs` — список пар `(имя_job, код_выхода)` в порядке запуска. Код `0` — успех, любой другой — провал.
            - Возвращает:
              - `("failed", имя)` — где имя — **первого** упавшего job-а;
              - `("success", None)` — если все завершились с кодом 0.

            Примеры:
            ```
            pipeline_status([("lint", 0), ("unit", 1), ("ui", 1)])   # → ("failed", "unit")
            pipeline_status([("lint", 0), ("unit", 0)])              # → ("success", None)
            ```
            """),
            """
            def pipeline_status(jobs):
                pass
            """,
            """
            def test_failed():
                assert pipeline_status([("lint", 0), ("unit", 1), ("ui", 1)]) == ("failed", "unit"), "Первый упавший — unit"

            def test_success():
                assert pipeline_status([("lint", 0), ("unit", 0)]) == ("success", None), "Все с кодом 0 → success"
            """,
            """
            def pipeline_status(jobs):
                for name, code in jobs:
                    if code != 0:
                        return "failed", name
                return "success", None
            """),
    cod(f"{O}-m2-l1-e3", t("""
            Напиши функцию `pytest_exit(code)`, которая расшифровывает код выхода pytest.

            - Получает: `code` — число от 0 до 5.
            - Возвращает строку:
              - `0` → `"all passed"`
              - `1` → `"tests failed"`
              - `2` → `"interrupted"`
              - `3` → `"internal error"`
              - `4` → `"usage error"`
              - `5` → `"no tests collected"`

            Пример:
            ```
            pytest_exit(5)   # → "no tests collected"
            ```
            """),
            """
            def pytest_exit(code):
                pass
            """,
            """
            def test_codes():
                got = [pytest_exit(c) for c in range(6)]
                assert got == ["all passed", "tests failed", "interrupted", "internal error", "usage error", "no tests collected"], f"Получено {got}"
            """,
            """
            def pytest_exit(code):
                return ["all passed", "tests failed", "interrupted", "internal error", "usage error", "no tests collected"][code]
            """),
    cod(f"{O}-m2-l1-e4", t("""
            Напиши функцию `should_deploy(branch, jobs)`, которая решает, можно ли выкатывать релиз.

            - Получает: `branch` — имя git-ветки; `jobs` — список кодов выхода всех job-ов пайплайна.
            - Возвращает `True`, только если выполнены **оба** условия:
              1. ветка — `"main"`;
              2. **все** коды выхода равны `0`.

            Примеры:
            ```
            should_deploy("main", [0, 0, 0])          # → True
            should_deploy("feature/login", [0, 0])    # → False   не main
            should_deploy("main", [0, 1])             # → False   есть упавший job
            ```
            """),
            """
            def should_deploy(branch, jobs):
                pass
            """,
            """
            def test_main_green():
                assert should_deploy("main", [0, 0, 0]) is True, "main + всё зелёное → деплой"

            def test_feature_branch():
                assert should_deploy("feature/login", [0, 0]) is False, "Не main → не деплоим"

            def test_red():
                assert should_deploy("main", [0, 1]) is False, "Есть упавший job → не деплоим"
            """,
            """
            def should_deploy(branch, jobs):
                return branch == "main" and all(code == 0 for code in jobs)
            """),
    cod(f"{O}-m2-l1-e5", t("""
            Напиши функцию `run_order(needs)`, которая определяет порядок запуска job-ов с зависимостями.

            - Получает: `needs` — словарь `{job: [список job-ов, от которых он зависит]}`. Job можно запустить только когда **все** его зависимости уже выполнены.
            - Возвращает: список всех job-ов в порядке запуска. Если одновременно готовы несколько — сначала запускается тот, чьё имя раньше **по алфавиту**, и после него готовность пересчитывается заново.

            Пример:
            ```
            run_order({
                "deploy":    ["api-tests", "ui-tests"],
                "api-tests": ["build"],
                "ui-tests":  ["build"],
                "build":     ["lint", "unit"],
                "lint":      [],
                "unit":      [],
            })
            # → ["lint", "unit", "build", "api-tests", "ui-tests", "deploy"]
            ```
            Алгоритм: пока не все выполнены — найди готовые (ещё не выполнен и все зависимости выполнены), отсортируй, возьми первый.
            """),
            """
            def run_order(needs):
                pass
            """,
            """
            def test_pipeline():
                needs = {
                    "deploy": ["api-tests", "ui-tests"],
                    "api-tests": ["build"],
                    "ui-tests": ["build"],
                    "build": ["lint", "unit"],
                    "lint": [],
                    "unit": [],
                }
                assert run_order(needs) == ["lint", "unit", "build", "api-tests", "ui-tests", "deploy"], f"Получено {run_order(needs)}"

            def test_independent():
                assert run_order({"b": [], "a": []}) == ["a", "b"], "Независимые — по алфавиту"
            """,
            """
            def run_order(needs):
                done = []
                while len(done) < len(needs):
                    ready = sorted(j for j, deps in needs.items() if j not in done and all(d in done for d in deps))
                    done.append(ready[0])
                return done
            """,
            hint="Пока не все выполнены: найди готовые (не выполнен, все зависимости в done), отсортируй, возьми первый.", xp=25),
    out(f"{O}-m2-l1-e6", "Что выведет программа? В оболочке `a && b` запускает `b`, только если `a` успешна (код 0), а `a || b` — только если `a` упала. Так в CI склеивают шаги.", """
        def run(name, code):
            print("run", name)
            return code

        def and_(a, b):
            code = a()
            return b() if code == 0 else code

        print("exit", and_(lambda: run("ruff", 1), lambda: run("pytest", 0)))
        print("exit", and_(lambda: run("ruff", 0), lambda: run("pytest", 0)))
        """),
    cmd(f"{O}-m2-l1-e7", "Fail fast внутри одного шага: запусти `pytest` так, чтобы он **остановился на первом упавшем** тесте.",
        ["pytest -x", "pytest --exitfirst", "python -m pytest -x"],
        hint="Флаг `-x`."),
    cmd(f"{O}-m2-l1-e8", "Одной строкой: сначала линтер `ruff check .`, и **только если он прошёл** — `pytest`.",
        ["ruff check . && pytest", "ruff check && pytest"],
        hint="Оператор `&&`."),
),

lesson(f"{P}-triggers", "Когда запускать: события и ветки",
    out(f"{P}-triggers-e1", "Что выведет программа? Ловушка YAML: в старой версии стандарта `on` — это логическое «да». PyYAML читает ключ `on:` как `True`.", """
        import yaml

        data = yaml.safe_load('''
        name: tests
        on: [push, pull_request]
        ''')
        print(list(data))
        print(data[True])
        """),
    cod(f"{P}-triggers-e2", t("""
        Напиши workflow `WORKFLOW` (достаточно `name` и `on`, job-ы не нужны), который запускается:

        - на `push` — только в ветку `main`;
        - на `pull_request` — в ветку `main`;
        - по расписанию — каждую ночь в 03:00 UTC: `schedule` с `cron: "0 3 * * *"`;
        - вручную — `workflow_dispatch:` (пустое значение).
        """),
        '''
        WORKFLOW = """
        name: nightly
        on:
          push:
            branches: [main]
        """
        ''',
        wfy("""
        def test_push_pr():
            on = wf().get("on") or {}
            assert isinstance(on, dict), "on — словарь событий"
            assert (on.get("push") or {}).get("branches") == ["main"], "push: branches: [main]"
            assert (on.get("pull_request") or {}).get("branches") == ["main"], "pull_request: branches: [main]"

        def test_schedule_manual():
            on = wf().get("on") or {}
            assert on.get("schedule") == [{"cron": "0 3 * * *"}], f'schedule: - cron: "0 3 * * *", а сейчас {on.get("schedule")}'
            assert "workflow_dispatch" in on, "Нужен ручной запуск workflow_dispatch"
        """),
        '''
        WORKFLOW = """
        name: nightly
        on:
          push:
            branches: [main]
          pull_request:
            branches: [main]
          schedule:
            - cron: "0 3 * * *"
          workflow_dispatch:
        """
        ''', xp=20),
    cmd(f"{P}-triggers-e3", "Запиши cron-выражение: **по будним дням (пн–пт) в 06:30**. Поля: минута, час, день месяца, месяц, день недели.",
        ["30 6 * * 1-5", "30 6 * * MON-FRI", "30 6 * * mon-fri", "30 06 * * 1-5"],
        hint="Минута `30`, час `6`, дни недели `1-5`."),
    cod(f"{P}-triggers-e4", t("""
        Фильтр веток в CI поддерживает шаблоны: `release/*` — любая ветка вида `release/…`.

        Напиши функцию `branch_matches(branch, patterns)`: `True`, если ветка подходит хотя бы под один шаблон. Сравнивай через `fnmatch.fnmatch`.

        Примеры:
        ```
        branch_matches("main", ["main", "release/*"])          # → True
        branch_matches("release/1.4", ["main", "release/*"])   # → True
        branch_matches("feature/login", ["main", "release/*"]) # → False
        ```
        """),
        """
        from fnmatch import fnmatch


        def branch_matches(branch, patterns):
            pass
        """,
        """
        def test_match():
            p = ["main", "release/*"]
            assert branch_matches("main", p) and branch_matches("release/1.4", p)
            assert not branch_matches("feature/login", p) and not branch_matches("mainline", p)
            assert branch_matches("hotfix-7", ["hotfix-*"])
        """,
        """
        from fnmatch import fnmatch


        def branch_matches(branch, patterns):
            return any(fnmatch(branch, p) for p in patterns)
        """),
    cod(f"{P}-triggers-e5", t("""
        UI-тесты долгие — их запускают, только если изменились файлы фронтенда или самих UI-тестов (фильтр `paths`).

        Напиши функцию `needs_ui_tests(changed, paths)`: `True`, если хотя бы один изменённый файл подходит хотя бы под один шаблон из `paths` (`fnmatch`; в `fnmatch` звёздочка `*` захватывает и `/`).

        Пример:
        ```
        paths = ["frontend/*", "tests/ui/*"]
        needs_ui_tests(["README.md", "frontend/src/App.vue"], paths)   # → True
        needs_ui_tests(["backend/api.py", "docs/x.md"], paths)         # → False
        ```
        """),
        """
        from fnmatch import fnmatch


        def needs_ui_tests(changed, paths):
            pass
        """,
        """
        P = ["frontend/*", "tests/ui/*"]

        def test_ui():
            assert needs_ui_tests(["README.md", "frontend/src/App.vue"], P) is True
            assert needs_ui_tests(["tests/ui/test_login.py"], P) is True

        def test_skip():
            assert needs_ui_tests(["backend/api.py", "docs/x.md"], P) is False
            assert needs_ui_tests([], P) is False
        """,
        """
        from fnmatch import fnmatch


        def needs_ui_tests(changed, paths):
            return any(fnmatch(f, p) for f in changed for p in paths)
        """),
    cod(f"{P}-triggers-e6", t("""
        Напиши функцию `should_run(event, branch, config)`, которая решает, запустится ли workflow.

        - `config` — раздел `on` в виде словаря: `{"push": {"branches": [...]}, "pull_request": {}, ...}`.
        - Событие должно быть в `config`, иначе `False`.
        - Если у события есть список `branches` — ветка должна подходить хотя бы под один шаблон (`fnmatch`); если списка нет — подходит любая ветка.

        Примеры:
        ```
        config = {"push": {"branches": ["main", "release/*"]}, "pull_request": {}}
        should_run("push", "release/2.0", config)        # → True
        should_run("push", "feature/x", config)          # → False
        should_run("pull_request", "feature/x", config)  # → True
        should_run("schedule", "main", config)           # → False
        ```
        Значение события может быть `None` (как у `workflow_dispatch:`) — это значит «без фильтров».
        """),
        """
        from fnmatch import fnmatch


        def should_run(event, branch, config):
            pass
        """,
        """
        C = {"push": {"branches": ["main", "release/*"]}, "pull_request": {}, "workflow_dispatch": None}

        def test_rules():
            assert should_run("push", "release/2.0", C) is True
            assert should_run("push", "feature/x", C) is False
            assert should_run("pull_request", "feature/x", C) is True
            assert should_run("schedule", "main", C) is False
            assert should_run("workflow_dispatch", "any", C) is True
        """,
        """
        from fnmatch import fnmatch


        def should_run(event, branch, config):
            if event not in config:
                return False
            branches = (config[event] or {}).get("branches")
            if branches is None:
                return True
            return any(fnmatch(branch, p) for p in branches)
        """, xp=20),
    cmd(f"{P}-triggers-e7", "В workflow `tests.yml` есть `workflow_dispatch`. Запусти его вручную из терминала утилитой GitHub CLI.",
        ["gh workflow run tests.yml", "gh workflow run tests"],
        hint="`gh workflow run файл`."),
    out(f"{P}-triggers-e8", "Что выведет программа? Какие события запустят workflow с фильтром веток.", """
        from fnmatch import fnmatch

        on = {"push": ["main", "release/*"], "pull_request": ["main"]}
        events = [("push", "main"), ("push", "feature/cart"), ("pull_request", "main"), ("push", "release/1.0")]
        for event, branch in events:
            ok = any(fnmatch(branch, p) for p in on.get(event, []))
            print(f"{event:12} {branch:14} {'▶' if ok else '—'}")
        """),
),

lesson(f"{P}-jobs", "Job-ы, needs и параллельность",
    out(f"{P}-jobs-e1", "Что выведет программа? Job-ы без зависимостей идут параллельно, поэтому время пайплайна — это самая длинная цепочка, а не сумма.", """
        durations = {"lint": 1, "unit": 3, "api": 6, "ui": 12}
        needs = {"lint": [], "unit": [], "api": ["lint", "unit"], "ui": ["lint", "unit"]}

        finish = {}
        for job in ["lint", "unit", "api", "ui"]:
            start = max((finish[d] for d in needs[job]), default=0)
            finish[job] = start + durations[job]
        print(finish)
        print("пайплайн:", max(finish.values()), "мин, последовательно было бы", sum(durations.values()))
        """),
    cod(f"{P}-jobs-e2", t("""
        Напиши функцию `waves(needs)`, которая раскладывает job-ы по «волнам» параллельного запуска.

        - `needs` — словарь `{job: [от кого зависит]}`.
        - Волна 1 — job-ы без зависимостей; волна 2 — те, чьи зависимости все в волне 1; и так далее.
        - Возвращает: список волн, каждая волна — **отсортированный** список имён.

        Пример:
        ```
        waves({"lint": [], "unit": [], "build": ["unit"], "api": ["build"], "ui": ["build", "lint"]})
        # → [["lint", "unit"], ["build"], ["api", "ui"]]
        ```
        """),
        """
        def waves(needs):
            pass
        """,
        """
        def test_waves():
            got = waves({"lint": [], "unit": [], "build": ["unit"], "api": ["build"], "ui": ["build", "lint"]})
            assert got == [["lint", "unit"], ["build"], ["api", "ui"]], got

        def test_single():
            assert waves({"a": []}) == [["a"]]
        """,
        """
        def waves(needs):
            done, result = set(), []
            while len(done) < len(needs):
                wave = sorted(j for j, deps in needs.items() if j not in done and all(d in done for d in deps))
                result.append(wave)
                done.update(wave)
            return result
        """, xp=20),
    cod(f"{P}-jobs-e3", t("""
        Напиши функцию `pipeline_time(durations, needs)` — сколько минут займёт пайплайн, если независимые job-ы идут параллельно.

        Job стартует, когда закончились **все** его зависимости (или сразу, если их нет), и заканчивается через `durations[job]` минут. Ответ — время окончания самого позднего job-а.

        Пример:
        ```
        durations = {"lint": 1, "unit": 3, "api": 6, "ui": 12, "deploy": 2}
        needs = {"lint": [], "unit": [], "api": ["unit"], "ui": ["unit"], "deploy": ["api", "ui", "lint"]}
        pipeline_time(durations, needs)   # → 17   (unit 3 → ui 12 → deploy 2)
        ```
        Job-ы в словаре могут идти в любом порядке — считай время рекурсивно или повторяй проходы.
        """),
        """
        def pipeline_time(durations, needs):
            pass
        """,
        """
        def test_time():
            d = {"lint": 1, "unit": 3, "api": 6, "ui": 12, "deploy": 2}
            n = {"deploy": ["api", "ui", "lint"], "ui": ["unit"], "api": ["unit"], "lint": [], "unit": []}
            assert pipeline_time(d, n) == 17, pipeline_time(d, n)

        def test_parallel():
            assert pipeline_time({"a": 5, "b": 7}, {"a": [], "b": []}) == 7
        """,
        """
        def pipeline_time(durations, needs):
            finish = {}

            def end(job):
                if job not in finish:
                    finish[job] = max((end(d) for d in needs[job]), default=0) + durations[job]
                return finish[job]

            return max(end(job) for job in durations)
        """, xp=20),
    cod(f"{P}-jobs-e4", t("""
        Напиши workflow `WORKFLOW` с четырьмя job-ами (все `runs-on: ubuntu-latest`, шаги — любые `run`):

        - `lint` и `unit` — без зависимостей (идут параллельно);
        - `api-tests` — `needs: [lint, unit]`;
        - `ui-tests` — `needs: [api-tests]`.

        Запуск — на `push`.
        """),
        '''
        WORKFLOW = """
        name: pipeline
        on: [push]
        jobs:
          lint:
            runs-on: ubuntu-latest
            steps:
              - run: ruff check .
        """
        ''',
        wfy("""
        def test_jobs():
            jobs = wf().get("jobs") or {}
            assert set(jobs) == {"lint", "unit", "api-tests", "ui-tests"}, f"Нужны job-ы lint, unit, api-tests, ui-tests: {sorted(jobs)}"
            for name, job in jobs.items():
                assert job.get("runs-on") == "ubuntu-latest", f"{name}: runs-on: ubuntu-latest"
                assert job.get("steps"), f"{name}: нужны steps"

        def test_needs():
            jobs = wf()["jobs"]
            as_list = lambda v: [v] if isinstance(v, str) else list(v or [])
            assert not jobs["lint"].get("needs") and not jobs["unit"].get("needs"), "lint и unit — без needs"
            assert sorted(as_list(jobs["api-tests"].get("needs"))) == ["lint", "unit"], "api-tests: needs [lint, unit]"
            assert as_list(jobs["ui-tests"].get("needs")) == ["api-tests"], "ui-tests: needs api-tests"
        """),
        '''
        WORKFLOW = """
        name: pipeline
        on: [push]
        jobs:
          lint:
            runs-on: ubuntu-latest
            steps:
              - run: ruff check .
          unit:
            runs-on: ubuntu-latest
            steps:
              - run: pytest tests/unit
          api-tests:
            needs: [lint, unit]
            runs-on: ubuntu-latest
            steps:
              - run: pytest tests/api
          ui-tests:
            needs: [api-tests]
            runs-on: ubuntu-latest
            steps:
              - run: pytest tests/ui
        """
        ''', xp=20),
    cod(f"{P}-jobs-e5", t("""
        Если job упал, все job-ы, которые от него **зависят** (напрямую или через цепочку), пропускаются.

        Напиши функцию `skipped_jobs(needs, failed)`: вернуть **отсортированный** список пропущенных job-ов.

        Пример:
        ```
        needs = {"lint": [], "unit": [], "build": ["unit"], "api": ["build"], "ui": ["build"], "report": ["lint"]}
        skipped_jobs(needs, {"unit"})   # → ["api", "build", "ui"]
        ```
        """),
        """
        def skipped_jobs(needs, failed):
            pass
        """,
        """
        N = {"lint": [], "unit": [], "build": ["unit"], "api": ["build"], "ui": ["build"], "report": ["lint"]}

        def test_chain():
            assert skipped_jobs(N, {"unit"}) == ["api", "build", "ui"], skipped_jobs(N, {"unit"})

        def test_leaf():
            assert skipped_jobs(N, {"api"}) == []
            assert skipped_jobs(N, {"lint", "build"}) == ["api", "report", "ui"]
        """,
        """
        def skipped_jobs(needs, failed):
            bad = set(failed)
            skipped = set()
            changed = True
            while changed:
                changed = False
                for job, deps in needs.items():
                    if job not in bad and job not in skipped and any(d in bad or d in skipped for d in deps):
                        skipped.add(job)
                        changed = True
            return sorted(skipped)
        """),
    cod(f"{P}-jobs-e6", t("""
        Долгий набор тестов делят между несколькими параллельными раннерами (**шардинг**). Напиши функцию `shard(tests, index, total)`: тесты раннера номер `index` (с 1) из `total` — каждый `total`-й тест, начиная с `index`-го, в исходном порядке.

        Пример:
        ```
        tests = ["t1", "t2", "t3", "t4", "t5"]
        shard(tests, 1, 2)   # → ["t1", "t3", "t5"]
        shard(tests, 2, 2)   # → ["t2", "t4"]
        ```
        Все шарды вместе должны дать все тесты ровно по разу.
        """),
        """
        def shard(tests, index, total):
            pass
        """,
        """
        def test_shards():
            tests = ["t1", "t2", "t3", "t4", "t5"]
            assert shard(tests, 1, 2) == ["t1", "t3", "t5"] and shard(tests, 2, 2) == ["t2", "t4"]

        def test_cover():
            tests = [f"t{i}" for i in range(10)]
            parts = [shard(tests, i, 3) for i in (1, 2, 3)]
            assert sorted(sum(parts, [])) == sorted(tests), "Шарды должны покрыть все тесты по одному разу"
        """,
        """
        def shard(tests, index, total):
            return tests[index - 1::total]
        """,
        hint="Срез с шагом: `tests[index - 1::total]`."),
    cmd(f"{P}-jobs-e7", "Внутри одного job-а тесты тоже можно распараллелить: запусти pytest на **всех** ядрах раннера (pytest-xdist).",
        ["pytest -n auto", "python -m pytest -n auto", "pytest --numprocesses auto", "pytest --numprocesses=auto"],
        hint="`-n auto`."),
    out(f"{P}-jobs-e8", "Что выведет программа? Итог job-ов: упавший, зависимые от него пропущены.", """
        needs = {"lint": [], "unit": [], "api": ["unit"], "ui": ["api"]}
        result = {}
        for job in ["lint", "unit", "api", "ui"]:
            if any(result[d] != "success" for d in needs[job]):
                result[job] = "skipped"
            else:
                result[job] = "failure" if job == "unit" else "success"
        print(result)
        """),
),

lesson(f"{P}-artifacts", "Артефакты, кэш и отчёты",
    cod(f"{P}-artifacts-e1", t("""
        Напиши workflow `WORKFLOW` с job-ом `tests` (`ubuntu-latest`), шаги:

        1. `uses: actions/checkout@v4`;
        2. `run: pip install -r requirements.txt`;
        3. `run: pytest --junitxml=reports/junit.xml`;
        4. `uses: actions/upload-artifact@v4` с условием `if: always()` и параметрами `with: {name: reports, path: reports/}` — отчёт нужен **особенно** когда тесты упали.
        """),
        '''
        WORKFLOW = """
        name: tests
        on: [push]
        jobs:
          tests:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
        """
        ''',
        wfy("""
        def test_steps():
            s = steps("tests")
            assert s and s[0].get("uses") == "actions/checkout@v4", "Первый шаг — actions/checkout@v4"
            runs = [x.get("run", "") for x in s]
            assert "pip install -r requirements.txt" in runs and "pytest --junitxml=reports/junit.xml" in runs, "Нужны установка и pytest с отчётом"
            assert runs.index("pip install -r requirements.txt") < runs.index("pytest --junitxml=reports/junit.xml")

        def test_upload():
            up = [x for x in steps("tests") if str(x.get("uses", "")).startswith("actions/upload-artifact@")]
            assert up, "Нужен шаг actions/upload-artifact@v4"
            assert str(up[0].get("if", "")).replace("${{", "").replace("}}", "").strip() == "always()", "Условие if: always()"
            assert (up[0].get("with") or {}) == {"name": "reports", "path": "reports/"}, f"with: name reports, path reports/: {up[0].get('with')}"
        """),
        '''
        WORKFLOW = """
        name: tests
        on: [push]
        jobs:
          tests:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - run: pip install -r requirements.txt
              - run: pytest --junitxml=reports/junit.xml
              - uses: actions/upload-artifact@v4
                if: always()
                with:
                  name: reports
                  path: reports/
        """
        ''', xp=20),
    out(f"{P}-artifacts-e2", "Что выведет программа? Ключ кэша зависит от хеша файла зависимостей: поменялся `requirements.txt` — кэш новый.", """
        import hashlib

        def cache_key(requirements):
            digest = hashlib.sha256(requirements.encode()).hexdigest()[:8]
            return f"pip-linux-{digest}"

        a = cache_key("pytest==8.3\\nrequests==2.32\\n")
        b = cache_key("pytest==8.3\\nrequests==2.32\\n")
        c = cache_key("pytest==8.4\\nrequests==2.32\\n")
        print(a == b, a == c)
        print(len(a))
        """),
    cod(f"{P}-artifacts-e3", t("""
        Напиши функцию `cache_key(os_name, python, requirements)` — ключ кэша pip, как `pip-${{ runner.os }}-${{ matrix.python }}-${{ hashFiles('requirements.txt') }}`:

        ```
        "pip-<os_name>-<python>-<первые 12 символов sha256 от текста requirements>"
        ```
        Хеш: `hashlib.sha256(requirements.encode()).hexdigest()[:12]`.
        """),
        """
        import hashlib


        def cache_key(os_name, python, requirements):
            pass
        """,
        """
        import hashlib as _h

        def test_key():
            req = "pytest==8.3\\n"
            want = "pip-Linux-3.12-" + _h.sha256(req.encode()).hexdigest()[:12]
            assert cache_key("Linux", "3.12", req) == want, cache_key("Linux", "3.12", req)

        def test_changes():
            assert cache_key("Linux", "3.12", "a") != cache_key("Linux", "3.12", "b"), "Другие зависимости — другой ключ"
            assert cache_key("Linux", "3.11", "a") != cache_key("Linux", "3.12", "a"), "Другой Python — другой ключ"
        """,
        """
        import hashlib


        def cache_key(os_name, python, requirements):
            digest = hashlib.sha256(requirements.encode()).hexdigest()[:12]
            return f"pip-{os_name}-{python}-{digest}"
        """),
    cmd(f"{P}-artifacts-e4", "Запусти pytest так, чтобы он сохранил отчёт в формате **JUnit XML** в `reports/junit.xml` — его понимают GitHub, GitLab, Jenkins.",
        ["pytest --junitxml=reports/junit.xml", "pytest --junit-xml=reports/junit.xml", "python -m pytest --junitxml=reports/junit.xml",
         "pytest --junitxml reports/junit.xml"],
        hint="Опция `--junitxml=путь`."),
    cod(f"{P}-artifacts-e5", t("""
        GitHub показывает на странице запуска Markdown из файла `$GITHUB_STEP_SUMMARY`. Напиши функцию `step_summary(results)`, которая готовит такую сводку.

        - `results` — словарь `{тест: "passed" | "failed" | "skipped"}`.
        - Первая строка — `### Тесты: X ✅ Y ❌ Z ⏭️` (сколько прошло / упало / пропущено).
        - Если есть упавшие — пустая строка, затем `Упали:` и по строке `- имя` на каждый, **по алфавиту**.
        - Строки соединены `\\n`.

        Пример:
        ```
        step_summary({"test_b": "failed", "test_a": "passed", "test_c": "failed"})
        # → "### Тесты: 1 ✅ 2 ❌ 0 ⏭️\\n\\nУпали:\\n- test_b\\n- test_c"
        ```
        """),
        """
        def step_summary(results):
            pass
        """,
        """
        def test_failed():
            got = step_summary({"test_b": "failed", "test_a": "passed", "test_c": "failed"})
            assert got == "### Тесты: 1 ✅ 2 ❌ 0 ⏭️\\n\\nУпали:\\n- test_b\\n- test_c", repr(got)

        def test_green():
            assert step_summary({"t": "passed", "s": "skipped"}) == "### Тесты: 1 ✅ 0 ❌ 1 ⏭️"
        """,
        """
        def step_summary(results):
            count = lambda status: sum(1 for r in results.values() if r == status)
            lines = [f"### Тесты: {count('passed')} ✅ {count('failed')} ❌ {count('skipped')} ⏭️"]
            failed = sorted(name for name, r in results.items() if r == "failed")
            if failed:
                lines += ["", "Упали:"] + [f"- {name}" for name in failed]
            return "\\n".join(lines)
        """),
    cmd(f"{P}-artifacts-e6", "В шаге workflow добавь в сводку запуска заголовок `### Итоги` — допиши строку в файл из переменной `GITHUB_STEP_SUMMARY`.",
        ['echo "### Итоги" >> $GITHUB_STEP_SUMMARY', 'echo "### Итоги" >> "$GITHUB_STEP_SUMMARY"', "echo '### Итоги' >> $GITHUB_STEP_SUMMARY",
         "echo '### Итоги' >> \"$GITHUB_STEP_SUMMARY\""],
        hint='`echo "текст" >> $ПЕРЕМЕННАЯ` — дописать в файл.'),
    cod(f"{P}-artifacts-e7", t("""
        Имена артефактов в матрице должны различаться, иначе запуски перезапишут друг друга. Напиши функцию `artifact_name(prefix, matrix)`: к префиксу через `-` добавляются значения матрицы **в порядке ключей по алфавиту**; символы `/` и пробелы в значениях заменяются на `_`.

        Пример:
        ```
        artifact_name("reports", {"python": "3.12", "os": "ubuntu-latest"})   # → "reports-ubuntu-latest-3.12"
        artifact_name("shots", {"browser": "chromium", "device": "iPhone 13"}) # → "shots-chromium-iPhone_13"
        ```
        """),
        """
        def artifact_name(prefix, matrix):
            pass
        """,
        """
        def test_names():
            assert artifact_name("reports", {"python": "3.12", "os": "ubuntu-latest"}) == "reports-ubuntu-latest-3.12"
            assert artifact_name("shots", {"browser": "chromium", "device": "iPhone 13"}) == "shots-chromium-iPhone_13"
            assert artifact_name("r", {"ref": "release/1.0"}) == "r-release_1.0"
            assert artifact_name("r", {}) == "r"
        """,
        """
        def artifact_name(prefix, matrix):
            parts = [prefix] + [str(matrix[k]).replace("/", "_").replace(" ", "_") for k in sorted(matrix)]
            return "-".join(parts)
        """),
    cmd(f"{P}-artifacts-e8", "Скачай через GitHub CLI артефакт `reports` из запуска с номером `9876543210`.",
        ["gh run download 9876543210 -n reports", "gh run download 9876543210 --name reports", "gh run download -n reports 9876543210"],
        hint="`gh run download <номер запуска> -n имя`."),
),
)
