"""Тема «Тестирование UI», модуль 3 «Практика» — задания. Теория — в _ui_t3.py."""
from ._lib import cmd, cod, d, lesson, module, out, pyt, t
from ._alr_m1 import ALLURE_RUNNER
from ._alr_m3 import cta
from ._ui_m1 import HEAD, uic, uit

P = "ui"

HEAD_ALLURE = "import allure\n" + HEAD


def alr(body):
    """Проверки задания с Allure: помощники run_allure/label/step_names/attachments + тесты."""
    return ALLURE_RUNNER + d(body)


m3 = module(f"{P}-m3", "Практика", "🚀", "Скриншоты, трейсы и Allure, списки и таблицы, настоящий Playwright, итоговые e2e-тесты магазина",

lesson(f"{P}-reports", "Скриншоты, трейсы и отчёты",
    out(f"{P}-reports-e1", "Что выведет программа? `page.screenshot(path=...)` сохраняет PNG-файл и возвращает его байты (в pwfake картинка пустая, но формат настоящий).", """
        import os
        from pwfake.sync_api import Page

        page = Page()
        page.set_content("<h1>Каталог</h1>")
        data = page.screenshot(path="catalog.png")
        print(type(data).__name__)
        print(data[1:4])
        print(os.path.exists("catalog.png"))
        """),
    uic(f"{P}-reports-e2", t("""
        Напиши функцию `save_screenshot(page, name)`, которая сохраняет скриншот страницы в папку `screenshots`.

        - Путь файла — `screenshots/<name>.png`.
        - Папки может не быть — создай её: `os.makedirs("screenshots", exist_ok=True)`.
        - Возвращает путь к файлу.

        Пример: `save_screenshot(page, "login_failed")` → `"screenshots/login_failed.png"`.
        """),
        """
        import os


        def save_screenshot(page, name):
            pass
        """,
        """
        import os, shutil

        def test_saves():
            shutil.rmtree("screenshots", ignore_errors=True)
            path = save_screenshot(fresh(), "login_failed")
            assert path == "screenshots/login_failed.png", f"Вернулся путь {path!r}"
            assert os.path.exists(path), "Файл не создан"
            assert open(path, "rb").read(4) == b"\\x89PNG", "Это должен быть PNG от page.screenshot"

        def test_twice():
            save_screenshot(fresh(), "a")
            save_screenshot(fresh(), "b")
            assert {"a.png", "b.png"} <= set(os.listdir("screenshots")), "Оба скриншота должны лежать в screenshots"
        """,
        """
        import os


        def save_screenshot(page, name):
            os.makedirs("screenshots", exist_ok=True)
            path = f"screenshots/{name}.png"
            page.screenshot(path=path)
            return path
        """),
    uit(f"{P}-reports-e3", t("""
        Приложи скриншот к отчёту Allure. Тест `test_catalog_screenshot(page)`: открой `/catalog`, дождись 5 карточек (`get_by_test_id("product")`) и приложи скриншот:
        ```python
        allure.attach(page.screenshot(), name="Каталог", attachment_type=allure.attachment_type.PNG)
        ```
        """),
        """
        def test_catalog_screenshot(page):
            page.goto("/catalog")
        """,
        alr("""
        def test_attached():
            code, res = run_allure()
            r = res.get("test_catalog_screenshot")
            assert r and r["status"] == "passed", {k: v["status"] for k, v in res.items()}
            att = [a for a in attachments(r) if a["name"] == "Каталог"]
            assert att and att[0]["type"] == "image/png", f"Нужно PNG-вложение «Каталог»: {attachments(r)}"
            assert "to_have_count(5)" in source().replace(" ", ""), "Сначала дождись 5 карточек"
        """),
        """
        def test_catalog_screenshot(page):
            page.goto("/catalog")
            expect(page.get_by_test_id("product")).to_have_count(5)
            allure.attach(page.screenshot(), name="Каталог", attachment_type=allure.attachment_type.PNG)
        """, head=HEAD_ALLURE),
    uit(f"{P}-reports-e4", t("""
        Разметь UI-тест шагами Allure, чтобы в отчёте был виден сценарий. Тест `test_login_steps(page)` — вход `anna` / `secret` из трёх шагов:

        1. `"Открыть страницу входа"` — переход на `/login`;
        2. `"Ввести логин и пароль"` — заполнение полей;
        3. `"Нажать «Войти»"` — клик и проверка, что адрес `http://app.test/catalog`.
        """),
        """
        def test_login_steps(page):
            with allure.step("Открыть страницу входа"):
                page.goto("/login")
        """,
        alr("""
        def test_steps():
            code, res = run_allure()
            r = res.get("test_login_steps")
            assert r and r["status"] == "passed", {k: v["status"] for k, v in res.items()}
            assert step_names(r) == ["Открыть страницу входа", "Ввести логин и пароль", "Нажать «Войти»"], step_names(r)

        def test_catches_bug():
            code, res = run_allure(patch=bug("login_no_redirect"))
            assert res["test_login_steps"]["status"] == "failed", "Тест не поймал баг: после входа сайт остался на /login"
        """),
        """
        def test_login_steps(page):
            with allure.step("Открыть страницу входа"):
                page.goto("/login")
            with allure.step("Ввести логин и пароль"):
                page.get_by_label("Логин").fill("anna")
                page.get_by_label("Пароль").fill("secret")
            with allure.step("Нажать «Войти»"):
                page.get_by_role("button", name="Войти").click()
                expect(page).to_have_url("http://app.test/catalog")
        """, head=HEAD_ALLURE),
    pyt(f"{P}-reports-e5", t("""
        Скриншот при падении — must have UI-автотестов. Твой код станет `conftest.py`. В нём уже есть фикстура `app`; допиши хук:

        ```python
        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtest_makereport(item, call):
            outcome = yield
            report = outcome.get_result()
            ...
        ```
        Если `report.when == "call"` и `report.failed`, возьми страницу теста — `item.funcargs.get("page")` — и, если она есть, приложи к Allure её скриншот с именем `"screenshot"` (тип `PNG`).
        """),
        """
        import allure
        import pytest
        from pwfake.demo import shop_app


        @pytest.fixture
        def app():
            return shop_app()
        """,
        cta("""
        TESTS = (
            "def test_ok(page):\\n    page.goto('/login')\\n\\n"
            "def test_bad(page):\\n    page.goto('/login')\\n    assert page.title() == 'Каталог'\\n\\n"
            "def test_no_page():\\n    assert 1 == 2\\n"
        )

        def test_conftest():
            code, res = run_conftest_allure(TESTS, "-W", "ignore::pytest.PytestAssertRewriteWarning")
            assert set(res) == {"test_ok", "test_bad", "test_no_page"}, list(res)
            shot = lambda r: [a for a in attachments(r) if a["name"] == "screenshot"]
            assert not shot(res["test_ok"]), "У прошедшего теста скриншота быть не должно"
            bad = shot(res["test_bad"])
            assert bad and bad[0]["type"] == "image/png", f"У упавшего теста нужен PNG «screenshot»: {attachments(res['test_bad'])}"
            assert not shot(res["test_no_page"]), "Если у теста нет page — скриншот не нужен"
        """),
        """
        import allure
        import pytest
        from pwfake.demo import shop_app


        @pytest.fixture
        def app():
            return shop_app()


        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtest_makereport(item, call):
            outcome = yield
            report = outcome.get_result()
            if report.when == "call" and report.failed:
                page = item.funcargs.get("page")
                if page is not None:
                    allure.attach(page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)
        """, xp=25),
    cmd(f"{P}-reports-e6", "Тест упал в CI, и там сохранился трейс `trace.zip` — запись всех шагов с DOM, сетью и консолью. Открой его в просмотрщике Playwright.",
        ["playwright show-trace trace.zip", "npx playwright show-trace trace.zip", "python -m playwright show-trace trace.zip"],
        hint="Команда `playwright show-trace <файл>`."),
    cmd(f"{P}-reports-e7", "В pytest-playwright скриншоты можно включить опцией, без своего хука. Запусти тесты так, чтобы скриншот сохранялся **только для упавших** тестов.",
        ["pytest --screenshot only-on-failure", r"re:(python -m )?pytest (.* )?--screenshot[ =]only-on-failure( .*)?"],
        hint="Опция `--screenshot` принимает `on`, `off` или `only-on-failure`."),
    cmd(f"{P}-reports-e8", "Запусти тесты с записью трейса, который **сохраняется только у упавших** тестов (у прошедших удаляется).",
        ["pytest --tracing retain-on-failure", r"re:(python -m )?pytest (.* )?--tracing[ =]retain-on-failure( .*)?"],
        hint="Опция `--tracing`: `on`, `off`, `retain-on-failure`."),
),

lesson(f"{P}-lists", "Списки и таблицы",
    out(f"{P}-lists-e1", "Что выведет программа? Тексты всех найденных элементов сразу.", """
        from pwfake.sync_api import Page

        page = Page()
        page.set_content('''
        <ul>
          <li>Клавиатура — 3500 ₽</li>
          <li>Мышь — 1200 ₽</li>
          <li>Коврик — 600 ₽</li>
        </ul>
        ''')
        texts = page.get_by_role("listitem").all_inner_texts()
        print(texts)
        prices = [int(t.split()[-2]) for t in texts]
        print(prices, prices == sorted(prices))
        """),
    out(f"{P}-lists-e2", "Что выведет программа? `.all()` даёт список локаторов — по одному на элемент.", """
        from pwfake.sync_api import Page

        page = Page()
        page.set_content('''
        <div class="card"><h3>Мышь</h3> <span class="price">1200 ₽</span></div>
        <div class="card"><h3>Коврик</h3> <span class="price">600 ₽</span></div>
        ''')
        for card in page.locator(".card").all():
            name = card.locator("h3").inner_text()
            price = card.locator(".price").inner_text()
            print(f"{name}: {price}")
        """),
    out(f"{P}-lists-e3", "Что выведет программа? `filter` сужает набор по тексту: `has_text` — содержит, `has_not_text` — не содержит.", """
        from pwfake.sync_api import Page

        page = Page()
        page.set_content('''
        <div class="card">Клавиатура <button>В корзину</button></div>
        <div class="card">Наушники <button disabled>Нет в наличии</button></div>
        <div class="card">Коврик <button>В корзину</button></div>
        ''')
        cards = page.locator(".card")
        print(cards.filter(has_text="В корзину").count())
        print(cards.filter(has_not_text="В корзину").inner_text())
        print(cards.filter(has_text="Коврик").get_by_role("button").is_enabled())
        """),
    out(f"{P}-lists-e4", "Что выведет программа? В таблице ищем строку по тексту и берём ячейку из неё.", """
        from pwfake.sync_api import Page

        page = Page()
        page.set_content('''
        <table>
          <tr><th>Товар</th> <th>Кол-во</th></tr>
          <tr><td>Мышь</td> <td class="qty">2</td></tr>
          <tr><td>Коврик</td> <td class="qty">1</td></tr>
        </table>
        ''')
        rows = page.get_by_role("row")
        print(rows.count())
        print(rows.filter(has_text="Мышь").locator(".qty").inner_text())
        print(page.get_by_role("cell").all_inner_texts())
        """),
    uic(f"{P}-lists-e5", t("""
        Напиши функцию `product_prices(page)`: на странице каталога дожидается товаров и возвращает словарь «название → цена числом».

        Карточка: `<div class="card" data-testid="product"><h3>Мышь</h3> <span class="price">1200 ₽</span> …</div>`.

        Пример результата:
        ```
        {"Клавиатура": 3500, "Мышь": 1200, "Монитор": 15000, "Наушники": 4200, "Коврик": 600}
        ```
        Дождись блока `#products` (`wait_for()`), затем пройди по карточкам через `.all()`.
        """),
        """
        def product_prices(page):
            pass
        """,
        """
        def test_prices():
            got = product_prices(fresh("/catalog"))
            assert got == {"Клавиатура": 3500, "Мышь": 1200, "Монитор": 15000, "Наушники": 4200, "Коврик": 600}, f"Получено {got}"
        """,
        """
        def product_prices(page):
            page.locator("#products").wait_for()
            result = {}
            for card in page.get_by_test_id("product").all():
                name = card.locator("h3").inner_text()
                result[name] = int(card.locator(".price").inner_text().split()[0])
            return result
        """),
    uit(f"{P}-lists-e6", t("""
        Тест `test_sort_by_price(page)`: в каталоге выбери сортировку `price` (список «Сортировка»), нажми «Найти», дождись 5 карточек и проверь, что цены (`.card .price`) идут **по возрастанию**.

        Цены — тексты вида `"600 ₽"`: собери их через `all_inner_texts()`, переведи в числа и сравни со `sorted(...)`.
        """),
        """
        def test_sort_by_price(page):
            page.goto("/catalog")
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_sort_by_price") == "passed", res

        def test_catches_bug():
            code, res = run_pytest(patch=bug("sort_broken"))
            assert res.get("test_sort_by_price") == "failed", "Тест не поймал баг: сортировка не работает"
        """,
        """
        def test_sort_by_price(page):
            page.goto("/catalog")
            page.get_by_label("Сортировка").select_option("price")
            page.get_by_role("button", name="Найти").click()
            expect(page.get_by_test_id("product")).to_have_count(5)
            prices = [int(text.split()[0]) for text in page.locator(".card .price").all_inner_texts()]
            assert prices == sorted(prices), prices
        """),
    uit(f"{P}-lists-e7", t("""
        Тест `test_remove_from_cart(page)`: добавь в корзину «Мышь» и «Коврик», открой `/cart`, в строке «Коврика» нажми «Удалить». Проверь, что осталась одна строка (`get_by_test_id("cart-row")`) и в ней «Мышь».
        """),
        """
        def test_remove_from_cart(page):
            page.goto("/catalog")
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_remove_from_cart") == "passed", res

        def test_catches_bug():
            code, res = run_pytest(patch=bug("remove_broken"))
            assert res.get("test_remove_from_cart") == "failed", "Тест не поймал баг: «Удалить» ничего не удаляет"
        """,
        """
        def test_remove_from_cart(page):
            page.goto("/catalog")
            for name in ("Мышь", "Коврик"):
                page.get_by_test_id("product").filter(has_text=name).get_by_role("button", name="В корзину").click()
            page.goto("/cart")
            rows = page.get_by_test_id("cart-row")
            rows.filter(has_text="Коврик").get_by_role("button", name="Удалить").click()
            expect(rows).to_have_count(1)
            expect(rows).to_contain_text("Мышь")
        """),
    uit(f"{P}-lists-e8", t("""
        Тест `test_cart_sum(page)`: добавь «Мышь» **дважды** и «Клавиатуру» один раз, открой `/cart` и проверь:

        - в строке «Мыши» количество (`.qty`) — `2`;
        - итог `#total` — «Итого: 5900 ₽».
        """),
        """
        def test_cart_sum(page):
            page.goto("/catalog")
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_cart_sum") == "passed", res

        def test_catches_bug():
            code, res = run_pytest(patch=bug("total_wrong"))
            assert res.get("test_cart_sum") == "failed", "Тест не поймал баг: «Итого» не учитывает количество"
        """,
        """
        def add(page, name):
            page.get_by_test_id("product").filter(has_text=name).get_by_role("button", name="В корзину").click()


        def test_cart_sum(page):
            page.goto("/catalog")
            add(page, "Мышь")
            add(page, "Мышь")
            add(page, "Клавиатура")
            page.goto("/cart")
            mouse = page.get_by_test_id("cart-row").filter(has_text="Мышь")
            expect(mouse.locator(".qty")).to_have_text("2")
            expect(page.locator("#total")).to_have_text("Итого: 5900 ₽")
        """),
),

lesson(f"{P}-real", "Настоящий Playwright",
    cmd(f"{P}-real-e1", "Установи плагин pytest-playwright — он ставит и сам Playwright, и даёт фикстуру `page`.",
        ["pip install pytest-playwright", "python -m pip install pytest-playwright", "uv add --dev pytest-playwright", "uv add pytest-playwright --dev"],
        hint="`pip install <пакет>`."),
    cmd(f"{P}-real-e2", "Пакет установлен, но браузеров ещё нет. Скачай браузер **Chromium** для Playwright.",
        ["playwright install chromium", "python -m playwright install chromium", "playwright install --with-deps chromium", "python -m playwright install --with-deps chromium"],
        hint="`playwright install <браузер>`."),
    cmd(f"{P}-real-e3", "Запиши сценарий мышкой, а Playwright сгенерирует код: открой генератор тестов для сайта `https://demo.shop.test`.",
        ["playwright codegen https://demo.shop.test", "python -m playwright codegen https://demo.shop.test", "npx playwright codegen https://demo.shop.test"],
        hint="Команда `codegen`."),
    cmd(f"{P}-real-e4", "Чтобы глазами посмотреть, что делает тест, запусти его с **видимым браузером** и **замедлением** каждого действия на 500 мс.",
        ["pytest --headed --slowmo 500", r"re:(python -m )?pytest (.* )?(--headed (.* )?--slowmo[ =]500|--slowmo[ =]500 (.* )?--headed)( .*)?"],
        hint="`--headed` и `--slowmo <мс>`."),
    cmd(f"{P}-real-e5", "В учебных заданиях импорт `from pwfake.sync_api import Page, expect`. Как выглядит **эта же строка** в настоящем проекте на Playwright?",
        ["from playwright.sync_api import Page, expect", "from playwright.sync_api import expect, Page"],
        hint="Модуль называется `playwright.sync_api`."),
    uic(f"{P}-real-e6", t("""
        Playwright работает и без pytest — обычным скриптом. Напиши функцию `catalog_names()`:

        ```python
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            ...
        ```
        Открой `http://app.test/catalog`, дождись блока `#products`, собери названия товаров (`.card h3`), закрой браузер (`browser.close()`) и верни список.
        """),
        """
        from pwfake.sync_api import sync_playwright


        def catalog_names():
            pass
        """,
        """
        from pwfake.sync_api import set_app

        def test_script():
            set_app(_shop_app())
            try:
                assert catalog_names() == ["Клавиатура", "Мышь", "Монитор", "Наушники", "Коврик"], "Товары не дождались или не те"
            finally:
                set_app(None)
            assert "sync_playwright()" in source() and "browser.close()" in source(), "Открой браузер через sync_playwright() и закрой его"
        """,
        """
        from pwfake.sync_api import sync_playwright


        def catalog_names():
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto("http://app.test/catalog")
                page.locator("#products").wait_for()
                names = page.locator(".card h3").all_inner_texts()
                browser.close()
                return names
        """),
    cmd(f"{P}-real-e7", "Тесты открывают страницы относительными путями (`page.goto(\"/login\")`). Запусти их на стенде `https://stage.shop.test` опцией командной строки.",
        ["pytest --base-url https://stage.shop.test", r"re:(python -m )?pytest (.* )?--base-url[ =]https://stage\.shop\.test/?( .*)?"],
        hint="Опция `--base-url`."),
    cmd(f"{P}-real-e8", "Запусти тесты сразу в двух браузерах — **Chromium** и **Firefox** (каждый тест выполнится дважды).",
        ["pytest --browser chromium --browser firefox", "pytest --browser firefox --browser chromium",
         r"re:(python -m )?pytest (.* )?--browser[ =]chromium --browser[ =]firefox( .*)?",
         r"re:(python -m )?pytest (.* )?--browser[ =]firefox --browser[ =]chromium( .*)?"],
        hint="Опцию `--browser` можно повторить."),
),

lesson(f"{P}-project", "Итоговый проект",
    uit(f"{P}-project-e1", t("""
        Главный сценарий магазина — сквозной (e2e) тест `test_full_order(page)`:

        1. войти как `anna` / `secret`;
        2. добавить в корзину «Мышь»;
        3. открыть корзину (ссылка `get_by_test_id("cart-link")`) и нажать ссылку «Оформить заказ»;
        4. заполнить «Имя» — `Аня`, «Телефон» — `+79991234567`, отметить «Согласен с условиями», нажать «Подтвердить»;
        5. проверить заголовок «Заказ оформлен» (`get_by_role("heading")`) и номер `get_by_test_id("order-number")` — «Номер заказа: 1001».
        """),
        """
        def test_full_order(page):
            page.goto("/login")
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_full_order") == "passed", res

        def test_catches_bug():
            code, res = run_pytest(patch=bug("login_no_redirect"))
            assert res.get("test_full_order") == "failed", "Тест должен падать, если вход не работает"
        """,
        """
        def test_full_order(page):
            page.goto("/login")
            page.get_by_label("Логин").fill("anna")
            page.get_by_label("Пароль").fill("secret")
            page.get_by_role("button", name="Войти").click()
            page.get_by_test_id("product").filter(has_text="Мышь").get_by_role("button", name="В корзину").click()
            page.get_by_test_id("cart-link").click()
            page.get_by_role("link", name="Оформить заказ").click()
            page.get_by_label("Имя").fill("Аня")
            page.get_by_label("Телефон").fill("+79991234567")
            page.get_by_label("Согласен с условиями").check()
            page.get_by_role("button", name="Подтвердить").click()
            expect(page.get_by_role("heading")).to_have_text("Заказ оформлен")
            expect(page.get_by_test_id("order-number")).to_have_text("Номер заказа: 1001")
        """, xp=25),
    uit(f"{P}-project-e2", t("""
        Тест `test_checkout_requires_login(page)`: гость (без входа) добавляет «Мышь», открывает `/cart` и нажимает «Оформить заказ». Сайт должен отправить его на вход: проверь адрес `http://app.test/login`.
        """),
        """
        def test_checkout_requires_login(page):
            page.goto("/catalog")
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_checkout_requires_login") == "passed", res
            assert "to_have_url" in source(), "Проверь адрес через to_have_url"
        """,
        """
        def test_checkout_requires_login(page):
            page.goto("/catalog")
            page.get_by_test_id("product").filter(has_text="Мышь").get_by_role("button", name="В корзину").click()
            page.goto("/cart")
            page.get_by_role("link", name="Оформить заказ").click()
            expect(page).to_have_url("http://app.test/login")
        """),
    uit(f"{P}-project-e3", t("""
        Тест `test_logout(page)`: войди как `anna`, нажми ссылку «Выйти» и проверь, что:

        - имени в шапке больше нет — `expect(page.get_by_test_id("username")).to_have_count(0)`;
        - видна ссылка «Войти» — `to_be_visible()`.
        """),
        """
        def test_logout(page):
            page.goto("/login")
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_logout") == "passed", res
            src = source()
            assert "to_have_count(0)" in src.replace(" ", "") and "to_be_visible" in src, "Нужны обе проверки"
        """,
        """
        def test_logout(page):
            page.goto("/login")
            page.get_by_label("Логин").fill("anna")
            page.get_by_label("Пароль").fill("secret")
            page.get_by_role("button", name="Войти").click()
            page.get_by_role("link", name="Выйти").click()
            expect(page.get_by_test_id("username")).to_have_count(0)
            expect(page.get_by_role("link", name="Войти")).to_be_visible()
        """),
    uit(f"{P}-project-e4", t("""
        Фикстура `checkout_page` (в заготовке) готовит страницу оформления. Параметризуй `test_delivery(checkout_page, value, label)`: выбери в списке «Доставка» вариант `value`, заполни имя `Аня`, телефон `+79991234567`, согласие — и подтверди. На странице заказа должен быть текст `f"Доставка: {label}"`.

        | value | label |
        |---|---|
        | `"courier"` | `"Курьер"` |
        | `"pickup"` | `"Самовывоз"` |
        """),
        """
        @pytest.fixture
        def checkout_page(page):
            page.goto("/login")
            page.get_by_label("Логин").fill("anna")
            page.get_by_label("Пароль").fill("secret")
            page.get_by_role("button", name="Войти").click()
            page.get_by_test_id("product").filter(has_text="Мышь").get_by_role("button").click()
            page.goto("/checkout")
            return page


        def test_delivery(checkout_page, value, label):
            pass
        """,
        """
        def test_passes():
            code, res = run_pytest()
            got = {k: v for k, v in res.items() if k.startswith("test_delivery[")}
            assert len(got) == 2 and set(got.values()) == {"passed"}, f"Нужно 2 прошедших случая: {res}"
        """,
        """
        @pytest.fixture
        def checkout_page(page):
            page.goto("/login")
            page.get_by_label("Логин").fill("anna")
            page.get_by_label("Пароль").fill("secret")
            page.get_by_role("button", name="Войти").click()
            page.get_by_test_id("product").filter(has_text="Мышь").get_by_role("button").click()
            page.goto("/checkout")
            return page


        @pytest.mark.parametrize("value, label", [("courier", "Курьер"), ("pickup", "Самовывоз")])
        def test_delivery(checkout_page, value, label):
            page = checkout_page
            page.get_by_label("Доставка").select_option(value)
            page.get_by_label("Имя").fill("Аня")
            page.get_by_label("Телефон").fill("+79991234567")
            page.get_by_label("Согласен с условиями").check()
            page.get_by_role("button", name="Подтвердить").click()
            expect(page.get_by_text("Доставка:")).to_have_text(f"Доставка: {label}")
        """),
    uit(f"{P}-project-e5", t("""
        Тест `test_order_numbers(page)`: войди и оформи **два** заказа подряд (каждый раз добавляя «Мышь» и заполняя форму). Номер первого — «Номер заказа: 1001», второго — «Номер заказа: 1002».

        Повторяющиеся шаги вынеси во вспомогательную функцию `place_order(page)` — так тест будет коротким.
        """),
        """
        def place_order(page):
            pass


        def test_order_numbers(page):
            pass
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_order_numbers") == "passed", res
            src = source()
            assert "1001" in src and "1002" in src, "Проверь оба номера"
        """,
        """
        def place_order(page):
            page.goto("/catalog")
            page.get_by_test_id("product").filter(has_text="Мышь").get_by_role("button", name="В корзину").click()
            page.goto("/checkout")
            page.get_by_label("Имя").fill("Аня")
            page.get_by_label("Телефон").fill("+79991234567")
            page.get_by_label("Согласен с условиями").check()
            page.get_by_role("button", name="Подтвердить").click()


        def test_order_numbers(page):
            page.goto("/login")
            page.get_by_label("Логин").fill("anna")
            page.get_by_label("Пароль").fill("secret")
            page.get_by_role("button", name="Войти").click()
            place_order(page)
            expect(page.get_by_test_id("order-number")).to_have_text("Номер заказа: 1001")
            place_order(page)
            expect(page.get_by_test_id("order-number")).to_have_text("Номер заказа: 1002")
        """),
    cod(f"{P}-project-e6", t("""
        Тест нашёл баг — пора завести баг-репорт. Напиши функцию `bug_report(title, steps, expected, actual)`, которая собирает текст репорта.

        - `title` — заголовок, `steps` — список шагов, `expected` / `actual` — ожидаемый и фактический результат.
        - Формат (строки через `\\n`, шаги пронумерованы с 1):
        ```
        Баг: Итого не учитывает количество
        Шаги:
        1. Добавить мышь дважды
        2. Открыть корзину
        Ожидалось: Итого: 2400 ₽
        Фактически: Итого: 1200 ₽
        ```
        """),
        """
        def bug_report(title, steps, expected, actual):
            pass
        """,
        """
        def test_report():
            got = bug_report("Итого не учитывает количество", ["Добавить мышь дважды", "Открыть корзину"], "Итого: 2400 ₽", "Итого: 1200 ₽")
            want = "Баг: Итого не учитывает количество\\nШаги:\\n1. Добавить мышь дважды\\n2. Открыть корзину\\nОжидалось: Итого: 2400 ₽\\nФактически: Итого: 1200 ₽"
            assert got == want, f"Получено:\\n{got}"

        def test_one_step():
            got = bug_report("X", ["Открыть сайт"], "a", "b")
            assert got == "Баг: X\\nШаги:\\n1. Открыть сайт\\nОжидалось: a\\nФактически: b", f"Получено:\\n{got}"
        """,
        """
        def bug_report(title, steps, expected, actual):
            lines = [f"Баг: {title}", "Шаги:"]
            lines += [f"{i}. {step}" for i, step in enumerate(steps, 1)]
            lines += [f"Ожидалось: {expected}", f"Фактически: {actual}"]
            return "\\n".join(lines)
        """,
        hint="Собери список строк и склей через `\"\\n\".join(...)`; нумерация — `enumerate(steps, 1)`."),
    uit(f"{P}-project-e7", t("""
        Регрессионный набор. Напиши **три** теста — каждый ловит свой баг:

        - `test_login_redirect(page)` — после входа `anna` / `secret` адрес `http://app.test/catalog`;
        - `test_search_keyboard(page)` — поиск «клав» оставляет одну карточку;
        - `test_cart_counter(page)` — после добавления «Коврика» ссылка корзины — «Корзина (1)».

        Проверка прогонит набор на трёх сломанных версиях сайта: каждая поломка должна уронить хотя бы один тест, а на исправном сайте все три должны пройти.
        """),
        """
        def test_login_redirect(page):
            pass


        def test_search_keyboard(page):
            pass


        def test_cart_counter(page):
            pass
        """,
        """
        NAMES = ["test_login_redirect", "test_search_keyboard", "test_cart_counter"]

        def test_passes():
            code, res = run_pytest()
            assert all(res.get(n) == "passed" for n in NAMES), res

        def test_catches_bugs():
            for name, why in [("login_no_redirect", "после входа сайт остаётся на /login"),
                              ("search_broken", "поиск игнорирует запрос"),
                              ("cart_count", "счётчик корзины не меняется")]:
                code, res = run_pytest(patch=bug(name))
                assert code == 1, f"Набор не поймал баг: {why}"
        """,
        """
        def test_login_redirect(page):
            page.goto("/login")
            page.get_by_label("Логин").fill("anna")
            page.get_by_label("Пароль").fill("secret")
            page.get_by_role("button", name="Войти").click()
            expect(page).to_have_url("http://app.test/catalog")


        def test_search_keyboard(page):
            page.goto("/catalog")
            page.get_by_placeholder("Поиск").fill("клав")
            page.get_by_role("button", name="Найти").click()
            expect(page.get_by_test_id("product")).to_have_count(1)


        def test_cart_counter(page):
            page.goto("/catalog")
            page.get_by_test_id("product").filter(has_text="Коврик").get_by_role("button", name="В корзину").click()
            expect(page.get_by_test_id("cart-link")).to_have_text("Корзина (1)")
        """, xp=25),
    uit(f"{P}-project-e8", t("""
        Требование: каталог должен загружаться **не дольше 4 секунд**. Обычное автоожидание ждёт 5 — поэтому передай свой таймаут прямо в проверку:
        ```python
        expect(...).to_have_count(5, timeout=4000)
        ```
        Напиши `test_catalog_fast(page)`: открой `/catalog` и проверь 5 карточек с таймаутом 4000 мс. Тест должен проходить, когда каталог грузится 3 секунды, и падать, когда 8.
        """),
        """
        def test_catalog_fast(page):
            page.goto("/catalog")
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_catalog_fast") == "passed", res

        def test_slow_ok():
            code, res = run_pytest(patch=bug("slow"))
            assert res.get("test_catalog_fast") == "passed", "Загрузка за 3 секунды укладывается в требование"

        def test_too_slow():
            code, res = run_pytest(patch=bug("too_slow"))
            assert res.get("test_catalog_fast") == "failed", "Загрузка за 8 секунд должна ронять тест"
            assert "timeout=4000" in source().replace(" ", ""), "Передай timeout=4000"
        """,
        """
        def test_catalog_fast(page):
            page.goto("/catalog")
            expect(page.get_by_test_id("product")).to_have_count(5, timeout=4000)
        """),
),
)
