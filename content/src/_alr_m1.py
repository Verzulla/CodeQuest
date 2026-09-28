"""Тема «Allure и отчёты», модуль 1 «Allure в тестах» — задания. Теория — в _alr_t1.py.

Проверки запускают pytest с --alluredir и читают настоящие результаты Allure (JSON)."""
from textwrap import dedent

from ._lib import cmd, lesson, module, pyt, t

P = "alr"

ALLURE_RUNNER = """
import glob, json, shutil


def run_allure(*args, patch=None):
    # Прогон с --alluredir. Возвращает (код, {имя в отчёте: результат}) — результат как в JSON Allure.
    shutil.rmtree("ar", ignore_errors=True)
    code, _ = run_pytest("--alluredir=ar", *args, patch=patch)
    results = {}
    for path in glob.glob("ar/*-result.json"):
        with open(path, encoding="utf-8") as f:
            r = json.load(f)
        results[r["name"]] = r
    return code, results


def label(result, name):
    return [l["value"] for l in result.get("labels", []) if l["name"] == name]


def step_names(result):
    names = []
    def walk(steps, depth):
        for s in steps:
            names.append("  " * depth + s["name"])
            walk(s.get("steps", []), depth + 1)
    walk(result.get("steps", []), 0)
    return names


def attachments(result):
    found = list(result.get("attachments", []))
    def walk(steps):
        for s in steps:
            found.extend(s.get("attachments", []))
            walk(s.get("steps", []))
    walk(result.get("steps", []))
    return found
"""


def at(body):
    """Тесты задания: помощники Allure + проверки."""
    return ALLURE_RUNNER + dedent(body)


m1 = module(f"{P}-m1", "Allure в тестах", "📊", "Подключение, шаги, вложения, метки и ссылки",

lesson(f"{P}-intro", "Что такое Allure и как его подключить",
    cmd(f"{P}-intro-e1", "Установи плагин Allure для pytest.",
        ["pip install allure-pytest", "python -m pip install allure-pytest", "uv add --dev allure-pytest", "uv add allure-pytest --dev"]),
    cmd(f"{P}-intro-e2", "Запусти тесты так, чтобы результаты для Allure сохранялись в папку `allure-results`.",
        ["pytest --alluredir=allure-results", "pytest --alluredir allure-results", "python -m pytest --alluredir=allure-results"]),
    cmd(f"{P}-intro-e3", "Сгенерируй HTML-отчёт из `allure-results` в папку `allure-report`, очистив её перед генерацией.",
        ["allure generate allure-results -o allure-report --clean", "allure generate allure-results --clean -o allure-report",
         "allure generate --clean allure-results -o allure-report", "allure generate allure-results -o allure-report -c",
         "allure generate -c allure-results -o allure-report", "allure generate allure-results --output allure-report --clean"]),
    cmd(f"{P}-intro-e4", "Сгенерируй отчёт во временную папку и сразу открой его в браузере одной командой.",
        ["allure serve allure-results"]),
    cmd(f"{P}-intro-e5", "Открой уже сгенерированный отчёт из папки `allure-report`.",
        ["allure open allure-report"]),
    cmd(f"{P}-intro-e6", "Какую программу нужно установить, чтобы работала команда `allure` (генератор отчётов)? Введи название языковой платформы.",
        ["Java", "java", "JRE", "JDK"], hint="Allure Commandline написан на Java."),
    cmd(f"{P}-intro-e7", "Сколько тестов в прогоне, если в `allure-results` лежат эти файлы? Введи число.",
        ["3"],
        context="""
        $ ls allure-results
        1b2c-result.json   7f8e-result.json   9a0b-result.json
        3d4e-container.json   5c6d-attachment.png
        """, hint="Один тест — один *-result.json."),
    pyt(f"{P}-intro-e8", t("""
        Проверка запустит твои тесты с `--alluredir`. Напиши тест `test_status`, который проверяет, что `health()` возвращает `"ok"`. Больше ничего не нужно — Allure запишет результат сам. Это позволит убедиться, что плагин подключён.
        """),
        """
        import allure
        import pytest


        def health():
            return "ok"
        """,
        at("""
        def test_allure_result():
            code, res = run_allure()
            assert "test_status" in res, f"В отчёте нет test_status: {list(res)}"
            assert res["test_status"]["status"] == "passed", res["test_status"]["status"]
        """),
        """
        import allure
        import pytest


        def health():
            return "ok"


        def test_status():
            assert health() == "ok"
        """, xp=15),
),

lesson(f"{P}-steps", "Шаги: allure.step",
    pyt(f"{P}-steps-e1", t("""
        Разбей тест `test_login` на шаги Allure контекстным менеджером `with allure.step(...)`: `"Открыть страницу входа"`, `"Ввести логин и пароль"`, `"Проверить приветствие"`. Внутри шагов вызывай функции из заготовки.
        """),
        """
        import allure
        import pytest


        def open_login():
            return "login page"


        def enter(user, password):
            return user == "anna" and password == "secret"


        def greeting(user):
            return f"Привет, {user}"
        """,
        at("""
        def test_steps():
            code, res = run_allure()
            r = res.get("test_login")
            assert r and r["status"] == "passed", f"Нужен проходящий test_login: {list(res)}"
            assert step_names(r) == ["Открыть страницу входа", "Ввести логин и пароль", "Проверить приветствие"], step_names(r)
        """),
        """
        import allure
        import pytest


        def open_login():
            return "login page"


        def enter(user, password):
            return user == "anna" and password == "secret"


        def greeting(user):
            return f"Привет, {user}"


        def test_login():
            with allure.step("Открыть страницу входа"):
                assert open_login() == "login page"
            with allure.step("Ввести логин и пароль"):
                assert enter("anna", "secret")
            with allure.step("Проверить приветствие"):
                assert greeting("anna") == "Привет, anna"
        """),
    pyt(f"{P}-steps-e2", t("""
        Шаг можно объявить **декоратором** — тогда каждый вызов функции станет шагом, а параметры подставятся в название. Сделай функцию `add_to_cart(item)` шагом с названием `"Добавить {item} в корзину"` и тест `test_cart`, который вызывает её для `"чай"` и `"кофе"`.
        """),
        """
        import allure
        import pytest

        CART = []


        def add_to_cart(item):
            CART.append(item)
        """,
        at("""
        def test_steps():
            code, res = run_allure()
            r = res.get("test_cart")
            assert r and r["status"] == "passed", list(res)
            names = step_names(r)
            assert len(names) == 2 and "чай" in names[0] and "кофе" in names[1] and names[0].startswith("Добавить"), names
        """),
        """
        import allure
        import pytest

        CART = []


        @allure.step("Добавить {item} в корзину")
        def add_to_cart(item):
            CART.append(item)


        def test_cart():
            add_to_cart("чай")
            add_to_cart("кофе")
            assert CART == ["чай", "кофе"]
        """, hint="@allure.step('… {item} …') над функцией."),
    pyt(f"{P}-steps-e3", t("""
        Шаги бывают **вложенными**. Напиши тест `test_order` со шагом `"Оформить заказ"`, внутри которого два шага: `"Заполнить адрес"` и `"Оплатить"`.
        """),
        """
        import allure
        import pytest
        """,
        at("""
        def test_steps():
            code, res = run_allure()
            r = res.get("test_order")
            assert r and r["status"] == "passed", list(res)
            assert step_names(r) == ["Оформить заказ", "  Заполнить адрес", "  Оплатить"], step_names(r)
        """),
        """
        import allure
        import pytest


        def test_order():
            with allure.step("Оформить заказ"):
                with allure.step("Заполнить адрес"):
                    pass
                with allure.step("Оплатить"):
                    pass
        """),
    cmd(f"{P}-steps-e4", "Какой шаг **упал**? Введи его название.",
        ["Оплатить"],
        context="""
        test_order  ✗ failed
          ✓ Открыть корзину
          ✓ Заполнить адрес
          ✗ Оплатить
              AssertionError: статус 500
          · Проверить письмо
        """, hint="Шаги после упавшего не выполняются."),
    cmd(f"{P}-steps-e5", "Каким будет название шага при вызове `login(\"anna\")`, если функция объявлена как `@allure.step(\"Войти как {user}\")`? Введи название.",
        ["Войти как 'anna'", "Войти как anna"], hint="allure-pytest подставляет строковые параметры через repr — с кавычками."),
    pyt(f"{P}-steps-e6", t("""
        Статус шага — как у кода внутри. Напиши тест `test_payment` с двумя шагами: `"Создать заказ"` (проходит) и `"Проверить статус"`, внутри которого `assert pay() == "paid"`. Функция `pay()` сейчас с багом — тест упадёт, и в отчёте будет видно, **на каком шаге**.
        """),
        """
        import allure
        import pytest


        def pay():
            return "error"
        """,
        at("""
        def test_steps():
            code, res = run_allure()
            r = res.get("test_payment")
            assert r and r["status"] == "failed", f"Тест должен упасть на баге: {list(res)}"
            steps = r.get("steps", [])
            assert [s["name"] for s in steps] == ["Создать заказ", "Проверить статус"], step_names(r)
            assert [s["status"] for s in steps] == ["passed", "failed"], [s["status"] for s in steps]
        """),
        """
        import allure
        import pytest


        def pay():
            return "error"


        def test_payment():
            with allure.step("Создать заказ"):
                order = {"id": 1}
            with allure.step("Проверить статус"):
                assert pay() == "paid"
        """),
    cmd(f"{P}-steps-e7", "Чем в отчёте Allure отличается статус `broken` от `failed`? Введи слово `assert`, если `failed` — это упавшая проверка, или `другое`.",
        ["assert"], hint="failed — не прошёл assert; broken — любое другое исключение (ошибка в коде или окружении)."),
    pyt(f"{P}-steps-e8", t("""
        В реальных проектах шаги прячут в **Page Object**. Создай класс `LoginPage` с методами-шагами (декоратором): `open()` — `"Открыть страницу входа"`, `login(user)` — `"Войти как {user}"`. Тест `test_page` вызывает `open()` и `login("anna")`.
        """),
        """
        import allure
        import pytest
        """,
        at("""
        def test_steps():
            code, res = run_allure()
            r = res.get("test_page")
            assert r and r["status"] == "passed", list(res)
            names = step_names(r)
            assert len(names) == 2 and names[0] == "Открыть страницу входа" and names[1].startswith("Войти как") and "anna" in names[1], names
        """),
        """
        import allure
        import pytest


        class LoginPage:
            @allure.step("Открыть страницу входа")
            def open(self):
                return self

            @allure.step("Войти как {user}")
            def login(self, user):
                return user


        def test_page():
            page = LoginPage()
            page.open()
            page.login("anna")
        """, xp=25),
),

lesson(f"{P}-attach", "Вложения: логи, JSON, скриншоты",
    pyt(f"{P}-attach-e1", t("""
        Приложи к тесту `test_api` тело ответа как JSON-вложение с именем `"response"`: `allure.attach(json.dumps(body), name="response", attachment_type=allure.attachment_type.JSON)`. `body` — результат `fake_response()`.
        """),
        """
        import json
        import allure
        import pytest


        def fake_response():
            return {"id": 1, "status": "active"}
        """,
        at("""
        def test_attach():
            code, res = run_allure()
            r = res.get("test_api")
            assert r and r["status"] == "passed", list(res)
            att = [a for a in attachments(r) if a["name"] == "response"]
            assert att and att[0]["type"] == "application/json", attachments(r)
            with open("ar/" + att[0]["source"], encoding="utf-8") as f:
                assert json.load(f) == {"id": 1, "status": "active"}, "Во вложении должно быть тело ответа"
        """),
        """
        import json
        import allure
        import pytest


        def fake_response():
            return {"id": 1, "status": "active"}


        def test_api():
            body = fake_response()
            allure.attach(json.dumps(body), name="response", attachment_type=allure.attachment_type.JSON)
            assert body["status"] == "active"
        """),
    pyt(f"{P}-attach-e2", t("""
        Приложи **текстовый** лог к шагу. В тесте `test_log` создай шаг `"Выполнить запрос"` и внутри него приложи строку `"GET /users -> 200"` с именем `"request"` и типом `TEXT`.
        """),
        """
        import allure
        import pytest
        """,
        at("""
        def test_attach():
            code, res = run_allure()
            r = res.get("test_log")
            assert r and r["status"] == "passed", list(res)
            steps = r.get("steps", [])
            assert steps and steps[0]["name"] == "Выполнить запрос", step_names(r)
            att = steps[0].get("attachments", [])
            assert att and att[0]["name"] == "request" and att[0]["type"] == "text/plain", f"Вложение должно быть внутри шага: {att}"
            with open("ar/" + att[0]["source"], encoding="utf-8") as f:
                assert f.read() == "GET /users -> 200"
        """),
        """
        import allure
        import pytest


        def test_log():
            with allure.step("Выполнить запрос"):
                allure.attach("GET /users -> 200", name="request", attachment_type=allure.attachment_type.TEXT)
        """),
    pyt(f"{P}-attach-e3", t("""
        Приложи **файл**: тест `test_file(tmp_path)` пишет в `tmp_path / "report.csv"` строку `"id,status\\n1,ok\\n"` и прикладывает файл через `allure.attach.file(путь, name="report", attachment_type=allure.attachment_type.CSV)`.
        """),
        """
        import allure
        import pytest
        """,
        at("""
        def test_attach():
            code, res = run_allure()
            r = res.get("test_file")
            assert r and r["status"] == "passed", list(res)
            att = [a for a in attachments(r) if a["name"] == "report"]
            assert att and att[0]["type"] == "text/csv", attachments(r)
            with open("ar/" + att[0]["source"], encoding="utf-8") as f:
                assert f.read() == "id,status\\n1,ok\\n"
        """),
        """
        import allure
        import pytest


        def test_file(tmp_path):
            path = tmp_path / "report.csv"
            path.write_text("id,status\\n1,ok\\n", encoding="utf-8")
            allure.attach.file(path, name="report", attachment_type=allure.attachment_type.CSV)
        """),
    cmd(f"{P}-attach-e4", "Какой тип вложения (`allure.attachment_type.…`) выбрать для скриншота браузера? Введи имя константы.",
        ["PNG"]),
    cmd(f"{P}-attach-e5", "Как называется хук pytest в `conftest.py`, в котором обычно делают скриншот, если тест упал? Введи имя функции.",
        ["pytest_runtest_makereport"]),
    pyt(f"{P}-attach-e6", t("""
        Скриншот нужен только при **падении**. Твой код станет частью тестов: напиши функцию-помощник `attach_on_failure(passed, screenshot)`. Если `passed` ложно — приложить байты `screenshot` как PNG с именем `"screenshot"`. Затем тесты `test_ok` (вызывает помощник с `True` и проходит) и `test_bad` (вызывает с `False` и падает `assert False`).
        """),
        """
        import allure
        import pytest

        FAKE_PNG = b"\\x89PNG\\r\\n\\x1a\\n" + bytes(16)
        """,
        at("""
        def test_attach():
            code, res = run_allure()
            ok, bad = res.get("test_ok"), res.get("test_bad")
            assert ok and bad, list(res)
            assert not [a for a in attachments(ok) if a["name"] == "screenshot"], "У прошедшего теста скриншота быть не должно"
            shots = [a for a in attachments(bad) if a["name"] == "screenshot"]
            assert shots and shots[0]["type"] == "image/png", attachments(bad)
        """),
        """
        import allure
        import pytest

        FAKE_PNG = b"\\x89PNG\\r\\n\\x1a\\n" + bytes(16)


        def attach_on_failure(passed, screenshot):
            if not passed:
                allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)


        def test_ok():
            attach_on_failure(True, FAKE_PNG)


        def test_bad():
            attach_on_failure(False, FAKE_PNG)
            assert False
        """),
    cmd(f"{P}-attach-e7", "Сколько вложений у теста? Введи число.",
        ["2"],
        context="""
        def test_api():
            with allure.step("Запрос"):
                allure.attach(req, name="request", attachment_type=allure.attachment_type.JSON)
                allure.attach(resp, name="response", attachment_type=allure.attachment_type.JSON)
            assert resp_status == 200
        """),
    pyt(f"{P}-attach-e8", t("""
        Напиши функцию `attach_request(method, url, status, body)` — шаг `"{method} {url}"` (декоратором или контекстным менеджером), внутри которого приложены: текст `"status: <status>"` с именем `"status"` и тело как JSON с именем `"body"`. Тест `test_users` вызывает `attach_request("GET", "/users", 200, {"items": []})`.
        """),
        """
        import json
        import allure
        import pytest
        """,
        at("""
        def test_attach():
            code, res = run_allure()
            r = res.get("test_users")
            assert r and r["status"] == "passed", list(res)
            steps = r.get("steps", [])
            assert steps and "GET" in steps[0]["name"] and "/users" in steps[0]["name"], step_names(r)
            names = {a["name"]: a for a in steps[0].get("attachments", [])}
            assert set(names) == {"status", "body"}, f"Внутри шага нужны вложения status и body: {list(names)}"
            with open("ar/" + names["status"]["source"], encoding="utf-8") as f:
                assert f.read() == "status: 200"
            with open("ar/" + names["body"]["source"], encoding="utf-8") as f:
                assert json.load(f) == {"items": []}
        """),
        """
        import json
        import allure
        import pytest


        def attach_request(method, url, status, body):
            with allure.step(f"{method} {url}"):
                allure.attach(f"status: {status}", name="status", attachment_type=allure.attachment_type.TEXT)
                allure.attach(json.dumps(body), name="body", attachment_type=allure.attachment_type.JSON)


        def test_users():
            attach_request("GET", "/users", 200, {"items": []})
        """, xp=25),
),

lesson(f"{P}-labels", "Метки: title, severity, feature, story, ссылки",
    pyt(f"{P}-labels-e1", t("""
        Дай тесту `test_login` человекочитаемое название `"Вход с правильным паролем"` через `@allure.title` и описание `"Проверяем успешный вход"` через `@allure.description`.
        """),
        """
        import allure
        import pytest
        """,
        at("""
        def test_labels():
            code, res = run_allure()
            r = res.get("Вход с правильным паролем")
            assert r, f"Не найден тест с таким названием: {list(res)}"
            assert r.get("description") == "Проверяем успешный вход", r.get("description")
        """),
        """
        import allure
        import pytest


        @allure.title("Вход с правильным паролем")
        @allure.description("Проверяем успешный вход")
        def test_login():
            assert True
        """),
    pyt(f"{P}-labels-e2", t("""
        Укажи важность: тест `test_payment` — `CRITICAL`, тест `test_avatar` — `MINOR` (через `@allure.severity(allure.severity_level.…)`).
        """),
        """
        import allure
        import pytest
        """,
        at("""
        def test_labels():
            code, res = run_allure()
            assert label(res["test_payment"], "severity") == ["critical"], label(res["test_payment"], "severity")
            assert label(res["test_avatar"], "severity") == ["minor"], label(res["test_avatar"], "severity")
        """),
        """
        import allure
        import pytest


        @allure.severity(allure.severity_level.CRITICAL)
        def test_payment():
            assert True


        @allure.severity(allure.severity_level.MINOR)
        def test_avatar():
            assert True
        """),
    pyt(f"{P}-labels-e3", t("""
        Сгруппируй тесты по функциональности: `@allure.epic("Магазин")`, `@allure.feature("Корзина")` и `@allure.story(...)`. Тест `test_add` — story `"Добавление товара"`, тест `test_remove` — story `"Удаление товара"`; epic и feature у обоих одинаковые. Подсказка: epic и feature можно повесить на **класс** `TestCart`.
        """),
        """
        import allure
        import pytest
        """,
        at("""
        def test_labels():
            code, res = run_allure()
            add, rem = res.get("test_add"), res.get("test_remove")
            assert add and rem, list(res)
            for r in (add, rem):
                assert label(r, "epic") == ["Магазин"] and label(r, "feature") == ["Корзина"], r["labels"]
            assert label(add, "story") == ["Добавление товара"] and label(rem, "story") == ["Удаление товара"], (label(add, "story"), label(rem, "story"))
        """),
        """
        import allure
        import pytest


        @allure.epic("Магазин")
        @allure.feature("Корзина")
        class TestCart:
            @allure.story("Добавление товара")
            def test_add(self):
                assert True

            @allure.story("Удаление товара")
            def test_remove(self):
                assert True
        """),
    pyt(f"{P}-labels-e4", t("""
        Свяжи тест с задачами: тесту `test_refund` добавь ссылку на тест-кейс `@allure.testcase("https://tms/TC-15", "TC-15")` и на баг `@allure.issue("https://tracker/BUG-42", "BUG-42")`.
        """),
        """
        import allure
        import pytest
        """,
        at("""
        def test_links():
            code, res = run_allure()
            r = res.get("test_refund")
            assert r, list(res)
            links = {(l["type"], l["url"]) for l in r.get("links", [])}
            assert ("test_case", "https://tms/TC-15") in links or ("tms", "https://tms/TC-15") in links, links
            assert ("issue", "https://tracker/BUG-42") in links, links
        """),
        """
        import allure
        import pytest


        @allure.testcase("https://tms/TC-15", "TC-15")
        @allure.issue("https://tracker/BUG-42", "BUG-42")
        def test_refund():
            assert True
        """),
    cmd(f"{P}-labels-e5", "Какие уровни `severity` есть в Allure, если перечислить от самого важного? Введи первый (самый важный).",
        ["blocker", "BLOCKER"], hint="blocker, critical, normal, minor, trivial."),
    cmd(f"{P}-labels-e6", "Какой уровень severity у теста **по умолчанию**, если метка не указана?",
        ["normal", "NORMAL"]),
    pyt(f"{P}-labels-e7", t("""
        Название можно задать **динамически** внутри теста — например, для параметризованного случая. Параметризуй `test_role(role)` значениями `"admin"` и `"qa"` и внутри задай название `f"Доступ для роли {role}"` через `allure.dynamic.title`.
        """),
        """
        import allure
        import pytest
        """,
        at("""
        def test_dynamic():
            code, res = run_allure()
            assert set(res) == {"Доступ для роли admin", "Доступ для роли qa"}, list(res)
            assert res["Доступ для роли qa"]["parameters"] == [{"name": "role", "value": "'qa'"}], res["Доступ для роли qa"]["parameters"]
        """),
        """
        import allure
        import pytest


        @pytest.mark.parametrize("role", ["admin", "qa"])
        def test_role(role):
            allure.dynamic.title(f"Доступ для роли {role}")
            assert role
        """),
    pyt(f"{P}-labels-e8", t("""
        Итог модуля. Оформи тест `test_checkout` полностью: название `"Оформление заказа"`, severity `CRITICAL`, feature `"Заказы"`, тег `"smoke"` (`@allure.tag`), два шага `"Добавить товар"` и `"Оплатить"`, а внутри «Оплатить» — вложение-текст `"paid"` с именем `"status"`.
        """),
        """
        import allure
        import pytest
        """,
        at("""
        def test_full():
            code, res = run_allure()
            r = res.get("Оформление заказа")
            assert r and r["status"] == "passed", list(res)
            assert label(r, "severity") == ["critical"] and label(r, "feature") == ["Заказы"] and "smoke" in label(r, "tag"), r["labels"]
            assert [s["name"] for s in r["steps"]] == ["Добавить товар", "Оплатить"], step_names(r)
            att = r["steps"][1].get("attachments", [])
            assert att and att[0]["name"] == "status", "Вложение status должно быть внутри шага «Оплатить»"
        """),
        """
        import allure
        import pytest


        @allure.title("Оформление заказа")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.feature("Заказы")
        @allure.tag("smoke")
        def test_checkout():
            with allure.step("Добавить товар"):
                pass
            with allure.step("Оплатить"):
                allure.attach("paid", name="status", attachment_type=allure.attachment_type.TEXT)
        """, xp=25),
),
)
