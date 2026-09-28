"""Тема «Allure и отчёты», модуль 3 «Отчёты в CI и на сервере» — задания. Теория — в _alr_t3.py."""
from textwrap import dedent

from ._lib import cmd, cod, lesson, module, pyt, t
from ._alr_m1 import ALLURE_RUNNER

P = "alr"

# Код ученика становится conftest.py, проверка создаёт файл тестов и читает результаты Allure.
CONFTEST_ALLURE = """
import os


_RUNS = []


def run_conftest_allure(test_code, *args):
    _RUNS.append(1)
    folder = f"ca{len(_RUNS)}"
    os.makedirs(folder, exist_ok=True)
    shutil.copy("solution.py", f"{folder}/conftest.py")
    with open(f"{folder}/test_generated_{len(_RUNS)}.py", "w", encoding="utf-8") as f:
        f.write(test_code)
    for name in [m for m in sys.modules if m == "conftest" or m.startswith("test_generated")]:
        del sys.modules[name]
    shutil.rmtree("ar", ignore_errors=True)
    code = pytest.main(["-q", "-p", "no:cacheprovider", folder, "--alluredir=ar", *args])
    results = {}
    for path in glob.glob("ar/*-result.json"):
        with open(path, encoding="utf-8") as f:
            r = json.load(f)
        results[r["name"]] = r
    return int(code), results
"""


def cta(body):
    return ALLURE_RUNNER + CONFTEST_ALLURE + dedent(body)


m3 = module(f"{P}-m3", "Отчёты в CI и на сервере", "🚀", "Allure в GitHub Actions и GitLab, сервер отчётов и его API, уведомления, conftest для отчётов",

lesson(f"{P}-ci", "Allure в CI",
    cmd(f"{P}-ci-e1", "Шаг CI должен сохранить папку `allure-results` даже если тесты упали. Какое условие пишут в GitHub Actions у шага загрузки артефакта? Введи выражение в `if:`.",
        ["always()", "${{ always() }}", "${{always()}}"]),
    cmd(f"{P}-ci-e2", "Как называется официальное действие GitHub Actions для загрузки артефактов (папок с отчётами)? Введи `владелец/имя@версия` для версии v4.",
        ["actions/upload-artifact@v4"]),
    cmd(f"{P}-ci-e3", "Какая строка в шаге GitLab CI задаёт, что артефакты сохраняются всегда (`when: …`)? Введи значение.",
        ["always"]),
    cmd(f"{P}-ci-e4", "Сколько шагов в этом job? Введи число.",
        ["5"],
        context="""
        jobs:
          tests:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - uses: astral-sh/setup-uv@v3
              - run: uv sync --locked
              - run: uv run pytest --alluredir=allure-results
              - uses: actions/upload-artifact@v4
                if: always()
                with:
                  name: allure-results
                  path: allure-results
        """),
    cmd(f"{P}-ci-e5", "Команда в CI должна упасть (код ≠ 0), если тесты упали, но **всё равно** сгенерировать отчёт следующим шагом. Какой флаг у pytest **не** нужен, чтобы pytest возвращал правильный код? Введи `ничего` — pytest и так вернёт 1 при падениях.",
        ["ничего"]),
    cmd(f"{P}-ci-e6", "Отчёт Allure часто публикуют как статический сайт. Как называется бесплатный хостинг статических страниц GitHub? Введи название.",
        ["GitHub Pages", "github pages", "gh-pages", "Pages"]),
    cod(f"{P}-ci-e7", t("""
        Напиши функцию `ci_steps(use_uv, workers)` — сгенерировать список команд для шага CI: установка зависимостей (`uv sync --locked`, если `use_uv`, иначе `pip install -r requirements.txt`), затем запуск тестов (`uv run pytest` или `pytest`) с `-n <workers>` (если `workers > 1`) и `--alluredir=allure-results`.
        """),
        """
        def ci_steps(use_uv, workers):
            pass
        """,
        """
        def test_values():
            assert ci_steps(True, 4) == ["uv sync --locked", "uv run pytest -n 4 --alluredir=allure-results"], ci_steps(True, 4)
            assert ci_steps(False, 1) == ["pip install -r requirements.txt", "pytest --alluredir=allure-results"], ci_steps(False, 1)
        """,
        """
        def ci_steps(use_uv, workers):
            install = "uv sync --locked" if use_uv else "pip install -r requirements.txt"
            run = "uv run pytest" if use_uv else "pytest"
            if workers > 1:
                run += f" -n {workers}"
            return [install, run + " --alluredir=allure-results"]
        """),
    cmd(f"{P}-ci-e8", "Как в GitHub Actions скачать артефакт `allure-results` из прошлого job в текущий? Введи действие `владелец/имя@v4`.",
        ["actions/download-artifact@v4"], xp=15),
),

lesson(f"{P}-server", "Сервер отчётов и его API",
    cmd(f"{P}-server-e1", "Как называется коммерческая система управления тестированием от авторов Allure (хранит историю, тест-кейсы, запуски)? Введи название.",
        ["Allure TestOps", "TestOps", "allure testops"]),
    cmd(f"{P}-server-e2", "Запусти открытый сервер отчётов Allure в Docker (образ `frankescobar/allure-docker-service`) на порту 5050.",
        ["docker run -p 5050:5050 frankescobar/allure-docker-service", "docker run -d -p 5050:5050 frankescobar/allure-docker-service",
         "docker run -p 5050:5050 -d frankescobar/allure-docker-service"]),
    cmd(f"{P}-server-e3", "Утилита `allurectl` загружает результаты в Allure TestOps. Как называется её подкоманда для загрузки папки? Введи слово.",
        ["upload"]),
    cod(f"{P}-server-e4", t("""
        Сервер отчётов принимает результаты по HTTP. Напиши функцию `build_payload(folder)` — прочитать все файлы в папке `allure-results` и вернуть словарь `{"results": [{"file_name": имя, "content_base64": содержимое в base64}]}` (как у allure-docker-service). Имена — отсортированы.
        """),
        """
        import base64
        from pathlib import Path


        def build_payload(folder):
            pass
        """,
        """
        import base64, os

        def test_values():
            os.makedirs("results", exist_ok=True)
            with open("results/b-result.json", "w", encoding="utf-8") as f:
                f.write('{"status": "passed"}')
            with open("results/a.png", "wb") as f:
                f.write(b"PNG")
            p = build_payload("results")
            assert [x["file_name"] for x in p["results"]] == ["a.png", "b-result.json"], p
            assert base64.b64decode(p["results"][0]["content_base64"]) == b"PNG", "Содержимое в base64"
        """,
        """
        import base64
        from pathlib import Path


        def build_payload(folder):
            files = sorted(p for p in Path(folder).iterdir() if p.is_file())
            return {"results": [
                {"file_name": p.name, "content_base64": base64.b64encode(p.read_bytes()).decode()}
                for p in files
            ]}
        """),
    cod(f"{P}-server-e5", t("""
        Напиши функцию `send_results(base_url, project, payload)` — отправить результаты POST-запросом через `requests` на `{base_url}/allure-docker-service/send-results?project_id={project}` с телом `payload` (JSON). Если ответ не 200 — выбросить `RuntimeError(f"сервер ответил {код}")`. Вернуть `response.json()`.

        Сети в песочнице нет — проверка подменит сервер библиотекой `responses`.
        """),
        """
        import requests


        def send_results(base_url, project, payload):
            pass
        """,
        """
        import json
        import responses

        @responses.activate
        def test_values():
            url = "https://reports.test/allure-docker-service/send-results?project_id=api"
            responses.post(url, json={"meta_data": {"message": "Results successfully sent"}}, status=200)
            got = send_results("https://reports.test", "api", {"results": []})
            assert got["meta_data"]["message"] == "Results successfully sent", got
            assert json.loads(responses.calls[0].request.body) == {"results": []}, "Тело запроса — payload в JSON"

        @responses.activate
        def test_error():
            responses.post("https://reports.test/allure-docker-service/send-results?project_id=api", status=500)
            try:
                send_results("https://reports.test", "api", {"results": []})
            except RuntimeError as e:
                assert str(e) == "сервер ответил 500", str(e)
                return
            assert False, "Нужен RuntimeError"
        """,
        """
        import requests


        def send_results(base_url, project, payload):
            response = requests.post(
                f"{base_url}/allure-docker-service/send-results",
                params={"project_id": project},
                json=payload,
                timeout=30,
            )
            if response.status_code != 200:
                raise RuntimeError(f"сервер ответил {response.status_code}")
            return response.json()
        """, hint="requests.post(url, params={...}, json=payload)"),
    cod(f"{P}-server-e6", t("""
        Напиши функцию `generate_report(base_url, project)` — попросить сервер сгенерировать отчёт GET-запросом на `{base_url}/allure-docker-service/generate-report?project_id={project}` и вернуть ссылку на отчёт из ответа — поле `data.report_url`.
        """),
        """
        import requests


        def generate_report(base_url, project):
            pass
        """,
        """
        import responses

        @responses.activate
        def test_values():
            responses.get("https://reports.test/allure-docker-service/generate-report?project_id=ui",
                          json={"data": {"report_url": "https://reports.test/projects/ui/reports/5/index.html"}})
            assert generate_report("https://reports.test", "ui") == "https://reports.test/projects/ui/reports/5/index.html"
        """,
        """
        import requests


        def generate_report(base_url, project):
            response = requests.get(
                f"{base_url}/allure-docker-service/generate-report",
                params={"project_id": project},
                timeout=60,
            )
            response.raise_for_status()
            return response.json()["data"]["report_url"]
        """),
    cmd(f"{P}-server-e7", "Зачем сервер отчётов, если отчёт можно сгенерировать локально? Введи главное преимущество одним словом: `история`, `скорость` или `цвет`.",
        ["история"], hint="Тренды, флаки и сравнение прогонов требуют хранить прошлые результаты."),
    cmd(f"{P}-server-e8", "Отправь результаты на сервер через `curl`: POST JSON-файла `payload.json` на `https://reports.test/allure-docker-service/send-results?project_id=api`.",
        ["curl -X POST 'https://reports.test/allure-docker-service/send-results?project_id=api' -H 'Content-Type: application/json' -d @payload.json",
         'curl -X POST "https://reports.test/allure-docker-service/send-results?project_id=api" -H "Content-Type: application/json" -d @payload.json',
         "curl -X POST -H 'Content-Type: application/json' -d @payload.json 'https://reports.test/allure-docker-service/send-results?project_id=api'",
         "re:curl .*-d @payload\\.json.*send-results\\?project_id=api.*", "re:curl .*send-results\\?project_id=api.*-d @payload\\.json.*",
         "re:curl .*--data(-binary)? @payload\\.json.*"], xp=15),
),

lesson(f"{P}-notify", "Уведомления о результатах",
    cod(f"{P}-notify-e1", t("""
        Напиши функцию `format_message(counts, report_url)` — текст уведомления для чата:

        ```
        ✅ Тесты прошли: 10/10
        Отчёт: https://…
        ```

        Если есть упавшие или сломанные — первая строка `❌ Упало: F, сломано: B из T` (T — total).
        """),
        """
        def format_message(counts, report_url):
            pass
        """,
        """
        def test_values():
            ok = {"passed": 10, "failed": 0, "broken": 0, "skipped": 0, "total": 10}
            assert format_message(ok, "https://r/1") == "✅ Тесты прошли: 10/10\\nОтчёт: https://r/1", repr(format_message(ok, "https://r/1"))
            bad = {"passed": 7, "failed": 2, "broken": 1, "skipped": 0, "total": 10}
            assert format_message(bad, "https://r/2") == "❌ Упало: 2, сломано: 1 из 10\\nОтчёт: https://r/2", repr(format_message(bad, "https://r/2"))
        """,
        """
        def format_message(counts, report_url):
            if counts["failed"] or counts["broken"]:
                head = f"❌ Упало: {counts['failed']}, сломано: {counts['broken']} из {counts['total']}"
            else:
                head = f"✅ Тесты прошли: {counts['passed']}/{counts['total']}"
            return f"{head}\\nОтчёт: {report_url}"
        """),
    cod(f"{P}-notify-e2", t("""
        Напиши функцию `notify_telegram(token, chat_id, text)` — отправить сообщение через Bot API Telegram: POST на `https://api.telegram.org/bot{token}/sendMessage` с JSON `{"chat_id": chat_id, "text": text}`. Вернуть `True`, если в ответе `"ok": true`.
        """),
        """
        import requests


        def notify_telegram(token, chat_id, text):
            pass
        """,
        """
        import json
        import responses

        @responses.activate
        def test_values():
            responses.post("https://api.telegram.org/botT0KEN/sendMessage", json={"ok": True})
            assert notify_telegram("T0KEN", 42, "привет") is True
            assert json.loads(responses.calls[0].request.body) == {"chat_id": 42, "text": "привет"}, responses.calls[0].request.body
        """,
        """
        import requests


        def notify_telegram(token, chat_id, text):
            response = requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": text},
                timeout=10,
            )
            return response.json().get("ok") is True
        """),
    cod(f"{P}-notify-e3", t("""
        Напиши функцию `slack_payload(counts, report_url, failed_names)` — тело для Slack incoming webhook: `{"text": заголовок, "blocks": [...]}`. Заголовок — как в `format_message` первая строка. Блоки: один `{"type": "section", "text": {"type": "mrkdwn", "text": "<report_url|Открыть отчёт>"}}` и, если есть упавшие, второй блок с текстом `"Упали:\\n• a\\n• b"` (не больше 5 имён, дальше `"• …и ещё N"`).
        """),
        """
        def slack_payload(counts, report_url, failed_names):
            pass
        """,
        """
        def test_values():
            ok = slack_payload({"passed": 3, "failed": 0, "broken": 0, "total": 3}, "https://r", [])
            assert ok == {"text": "✅ Тесты прошли: 3/3", "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": "<https://r|Открыть отчёт>"}}]}, ok
            names = [f"t{i}" for i in range(7)]
            bad = slack_payload({"passed": 0, "failed": 7, "broken": 0, "total": 7}, "https://r", names)
            assert bad["text"] == "❌ Упало: 7, сломано: 0 из 7" and len(bad["blocks"]) == 2, bad
            assert bad["blocks"][1]["text"]["text"] == "Упали:\\n• t0\\n• t1\\n• t2\\n• t3\\n• t4\\n• …и ещё 2", bad["blocks"][1]
        """,
        """
        def slack_payload(counts, report_url, failed_names):
            if counts["failed"] or counts["broken"]:
                title = f"❌ Упало: {counts['failed']}, сломано: {counts['broken']} из {counts['total']}"
            else:
                title = f"✅ Тесты прошли: {counts['passed']}/{counts['total']}"
            blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": f"<{report_url}|Открыть отчёт>"}}]
            if failed_names:
                lines = [f"• {name}" for name in failed_names[:5]]
                if len(failed_names) > 5:
                    lines.append(f"• …и ещё {len(failed_names) - 5}")
                blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": "Упали:\\n" + "\\n".join(lines)}})
            return {"text": title, "blocks": blocks}
        """),
    cmd(f"{P}-notify-e4", "Где хранить токен бота для уведомлений в GitHub Actions? Введи место: `secrets`, `код` или `README`.",
        ["secrets"], hint="${{ secrets.TELEGRAM_TOKEN }}"),
    cmd(f"{P}-notify-e5", "Как в шаге GitHub Actions обратиться к секрету `TELEGRAM_TOKEN`? Введи выражение.",
        ["${{ secrets.TELEGRAM_TOKEN }}", "${{secrets.TELEGRAM_TOKEN}}"]),
    cod(f"{P}-notify-e6", t("""
        Шаблон сообщения не должен падать, если чего-то нет. Напиши функцию `safe_summary(data)` — `data` — содержимое `widgets/summary.json` (словарь). Вернуть `counts` в формате `{"passed", "failed", "broken", "skipped", "total"}` из `data["statistic"]`; отсутствующие поля — 0, а если нет `statistic` — все нули.
        """),
        """
        def safe_summary(data):
            pass
        """,
        """
        def test_values():
            full = {"statistic": {"passed": 5, "failed": 1, "broken": 0, "skipped": 2, "unknown": 0, "total": 8}}
            assert safe_summary(full) == {"passed": 5, "failed": 1, "broken": 0, "skipped": 2, "total": 8}
            assert safe_summary({"statistic": {"passed": 1, "total": 1}}) == {"passed": 1, "failed": 0, "broken": 0, "skipped": 0, "total": 1}
            assert safe_summary({}) == {"passed": 0, "failed": 0, "broken": 0, "skipped": 0, "total": 0}
        """,
        """
        def safe_summary(data):
            stat = data.get("statistic", {})
            return {key: stat.get(key, 0) for key in ("passed", "failed", "broken", "skipped", "total")}
        """),
    cmd(f"{P}-notify-e7", "Отправь сообщение `Тесты упали` в Telegram через `curl` (POST на `https://api.telegram.org/bot$TOKEN/sendMessage` с полями формы `chat_id=$CHAT` и `text=Тесты упали`).",
        ['curl -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" -d chat_id=$CHAT -d text="Тесты упали"',
         'curl -X POST https://api.telegram.org/bot$TOKEN/sendMessage -d chat_id=$CHAT -d text="Тесты упали"',
         'curl "https://api.telegram.org/bot$TOKEN/sendMessage" -d chat_id=$CHAT -d text="Тесты упали"',
         "curl -X POST \"https://api.telegram.org/bot$TOKEN/sendMessage\" -d chat_id=$CHAT -d 'text=Тесты упали'",
         're:curl .*api\\.telegram\\.org/bot\\$TOKEN/sendMessage.*-d .?chat_id=\\$CHAT.*-d .?text=.?Тесты упали.*',
         're:curl .*-d .?chat_id=\\$CHAT.*-d .?text=.?Тесты упали.*api\\.telegram\\.org/bot\\$TOKEN/sendMessage.*']),
    cmd(f"{P}-notify-e8", "Уведомления лучше отправлять при каждом прогоне или только при изменении статуса / падении? Введи `при падении` или `всегда`.",
        ["при падении"], hint="Иначе чат зашумится и уведомления перестанут читать.", xp=15),
),

lesson(f"{P}-practice", "Практика: conftest для отчётов",
    pyt(f"{P}-practice-e1", t("""
        Твой код станет `conftest.py`. Добавь **автоматическую** (`autouse=True`) фикстуру `allure_env`, которая у каждого теста ставит метку-тег `"stage"` через `allure.dynamic.tag("stage")`. Проверка создаст тесты и посмотрит метки в отчёте.
        """),
        """
        import allure
        import pytest
        """,
        cta("""
        def test_conftest():
            code, res = run_conftest_allure("def test_a():\\n    assert True\\n\\ndef test_b():\\n    assert True\\n")
            assert set(res) == {"test_a", "test_b"}, list(res)
            for r in res.values():
                assert "stage" in label(r, "tag"), r["labels"]
        """),
        """
        import allure
        import pytest


        @pytest.fixture(autouse=True)
        def allure_env():
            allure.dynamic.tag("stage")
        """),
    pyt(f"{P}-practice-e2", t("""
        Твой код станет `conftest.py`. Напиши хук `pytest_runtest_makereport(item, call)` с декоратором `@pytest.hookimpl(hookwrapper=True)`, который после выполнения теста (`outcome = yield; report = outcome.get_result()`) при `report.when == "call"` и `report.failed` прикладывает к Allure текст `f"упал: {item.name}"` с именем `"failure"`. Так делают скриншоты при падении.
        """),
        """
        import allure
        import pytest
        """,
        cta("""
        def test_conftest():
            code, res = run_conftest_allure("def test_ok():\\n    assert True\\n\\ndef test_bad():\\n    assert 1 == 2\\n")
            ok, bad = res.get("test_ok"), res.get("test_bad")
            assert ok and bad, list(res)
            assert not [a for a in attachments(ok) if a["name"] == "failure"], "У прошедшего вложения быть не должно"
            att = [a for a in attachments(bad) if a["name"] == "failure"]
            assert att, f"У упавшего теста должно быть вложение failure: {attachments(bad)}"
            files = [f for f in os.listdir("ar") if f == att[0]["source"]]
            with open("ar/" + files[0], encoding="utf-8") as f:
                assert f.read() == "упал: test_bad"
        """),
        """
        import allure
        import pytest


        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtest_makereport(item, call):
            outcome = yield
            report = outcome.get_result()
            if report.when == "call" and report.failed:
                allure.attach(f"упал: {item.name}", name="failure", attachment_type=allure.attachment_type.TEXT)
        """, hint="hookwrapper=True: код до yield — до формирования отчёта, после — когда он готов."),
    pyt(f"{P}-practice-e3", t("""
        Твой код станет `conftest.py`. Напиши хук `pytest_sessionfinish(session, exitstatus)`, который записывает файл `ar/environment.properties` со строками `Python=3.12` и `Stand=stage` (проверка запускает pytest с `--alluredir=ar`). Папку бери из опции: `session.config.getoption("--alluredir")`.
        """),
        """
        import pytest
        """,
        cta("""
        def test_conftest():
            code, res = run_conftest_allure("def test_a():\\n    assert True\\n")
            assert os.path.exists("ar/environment.properties"), "Файл environment.properties не создан"
            with open("ar/environment.properties", encoding="utf-8") as f:
                assert set(f.read().split()) == {"Python=3.12", "Stand=stage"}, "Неверное содержимое"
        """),
        """
        import os
        import pytest


        def pytest_sessionfinish(session, exitstatus):
            folder = session.config.getoption("--alluredir")
            if not folder:
                return
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, "environment.properties"), "w", encoding="utf-8") as f:
                f.write("Python=3.12\\nStand=stage\\n")
        """),
    pyt(f"{P}-practice-e4", t("""
        Твой код станет `conftest.py`. Сделай фикстуру `api_step` — фабрику: она возвращает функцию `step(name)`, которая возвращает контекстный менеджер `allure.step(f"API: {name}")`. Проверка напишет тест, использующий `with api_step("GET /users"):`, и найдёт шаг в отчёте.
        """),
        """
        import allure
        import pytest
        """,
        cta("""
        def test_conftest():
            code, res = run_conftest_allure(
                "def test_users(api_step):\\n    with api_step('GET /users'):\\n        assert True\\n")
            r = res.get("test_users")
            assert r and r["status"] == "passed", list(res)
            assert step_names(r) == ["API: GET /users"], step_names(r)
        """),
        """
        import allure
        import pytest


        @pytest.fixture
        def api_step():
            def step(name):
                return allure.step(f"API: {name}")
            return step
        """),
    cmd(f"{P}-practice-e5", "Какой хук pytest вызывается один раз **после всего прогона** (удобно записать environment.properties)? Введи имя.",
        ["pytest_sessionfinish"]),
    cmd(f"{P}-practice-e6", "Какой параметр декоратора `@pytest.hookimpl(...)` позволяет выполнить код до и после стандартной реализации хука через `yield`? Введи `имя=значение`.",
        ["hookwrapper=True", "wrapper=True"]),
    cmd(f"{P}-practice-e7", "У отчёта `report` в хуке `pytest_runtest_makereport` какое значение `report.when` соответствует выполнению **самого теста** (а не setup/teardown)?",
        ["call"]),
    pyt(f"{P}-practice-e8", t("""
        Итог темы. Твой код станет `conftest.py`:

        - autouse-фикстура `owner` ставит каждому тесту метку `allure.dynamic.label("owner", "qa-team")`;
        - хук `pytest_runtest_makereport` (hookwrapper) при падении теста на этапе `call` прикладывает текст лога `"LOG: " + item.name` с именем `"log"`.
        """),
        """
        import allure
        import pytest
        """,
        cta("""
        def test_conftest():
            code, res = run_conftest_allure("def test_ok():\\n    assert True\\n\\ndef test_fail():\\n    assert False\\n")
            assert set(res) == {"test_ok", "test_fail"}, list(res)
            for r in res.values():
                assert label(r, "owner") == ["qa-team"], r["labels"]
            assert [a["name"] for a in attachments(res["test_fail"])] == ["log"], attachments(res["test_fail"])
            assert attachments(res["test_ok"]) == [], "У прошедшего теста вложений нет"
        """),
        """
        import allure
        import pytest


        @pytest.fixture(autouse=True)
        def owner():
            allure.dynamic.label("owner", "qa-team")


        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtest_makereport(item, call):
            outcome = yield
            report = outcome.get_result()
            if report.when == "call" and report.failed:
                allure.attach("LOG: " + item.name, name="log", attachment_type=allure.attachment_type.TEXT)
        """, xp=30),
),
)
