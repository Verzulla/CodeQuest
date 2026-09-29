"""Тема «Тестирование UI», модуль 2 «Архитектура UI-тестов» — задания. Теория — в _ui_t2.py.

Слаги ui-m2-l1, ui-m2-l2 унаследованы от старой темы — так сохраняется прогресс."""
from textwrap import indent

from ._lib import cmd, cod, lesson, module, out, pyt, t
from ._pyt_m2 import ct
from ._ui_m1 import uic, uit

P = "ui"

# Шапка без фикстуры app — её пишет сам ученик.
HEAD_NOAPP = """import pytest
from pwfake.sync_api import Page, expect
from pwfake.demo import shop_app


"""

LOGIN_PAGE = '''
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.user_input = page.get_by_label("Логин")
        self.password_input = page.get_by_label("Пароль")
        self.submit = page.get_by_role("button", name="Войти")
        self.error = page.get_by_role("alert")

    def open(self):
        self.page.goto("/login")
        return self

    def login(self, user, password):
        self.user_input.fill(user)
        self.password_input.fill(password)
        self.submit.click()


'''
# Отступ как у тел заданий, чтобы склейка «LOGIN_PAGE + тело» дедентилась целиком.
LOGIN_PAGE = indent(LOGIN_PAGE, " " * 8).rstrip("\n") + "\n\n"

LOGGED_IN = '''
@pytest.fixture
def logged_in_page(page):
    page.goto("/login")
    page.get_by_label("Логин").fill("anna")
    page.get_by_label("Пароль").fill("secret")
    page.get_by_role("button", name="Войти").click()
    return page


'''
LOGGED_IN = indent(LOGGED_IN, " " * 8).rstrip("\n") + "\n\n"

m2 = module(f"{P}-m2", "Архитектура UI-тестов", "🏗️", "Page Object, стратегия автоматизации, фикстуры и параметризация",

lesson(f"{P}-m2-l1", "Page Object",
    out(f"{P}-m2-l1-e1", "Что выведет программа? Локаторы ленивые: объект создан до того, как на странице что-то появилось, а элементы ищутся в момент действия.", """
        from pwfake.sync_api import Page


        class SearchPage:
            def __init__(self, page):
                self.page = page
                self.box = page.get_by_placeholder("Поиск")
                self.button = page.get_by_role("button", name="Найти")

            def type_query(self, text):
                self.box.fill(text)
                return self


        page = Page()
        search = SearchPage(page)
        print(search.button.count())
        page.set_content('<input placeholder="Поиск"> <button>Найти</button>')
        print(search.button.count(), search.button.inner_text())
        print(search.type_query("мышь").box.input_value())
        """),
    uic(f"{P}-m2-l1-e2", t("""
        Напиши Page Object страницы входа — класс `LoginPage`.

        - `__init__(self, page)` сохраняет `page` и создаёт **локаторы-атрибуты**:
          - `user_input` — поле «Логин»;
          - `password_input` — поле «Пароль»;
          - `submit` — кнопка «Войти»;
          - `error` — блок ошибки с ролью `alert`.
        - `open(self)` — переходит на `/login`.
        - `login(self, user, password)` — заполняет поля и нажимает кнопку.

        Пример:
        ```python
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("anna", "wrong")
        login_page.error.inner_text()   # → "Неверный логин или пароль"
        ```
        """),
        """
        class LoginPage:
            def __init__(self, page):
                self.page = page

            def open(self):
                pass

            def login(self, user, password):
                pass
        """,
        """
        from pwfake.sync_api import Locator

        def test_locators():
            lp = LoginPage(Page(_shop_app()))
            for name in ("user_input", "password_input", "submit", "error"):
                assert isinstance(getattr(lp, name, None), Locator), f"Атрибут {name} должен быть локатором"

        def test_flow():
            page = Page(_shop_app())
            lp = LoginPage(page)
            lp.open()
            assert page.url.endswith("/login"), "open() должен открыть /login"
            lp.login("anna", "wrong")
            assert lp.error.inner_text() == "Неверный логин или пароль"
            lp.login("anna", "secret")
            assert page.url.endswith("/catalog"), "После верного входа — каталог"
        """,
        """
        class LoginPage:
            def __init__(self, page):
                self.page = page
                self.user_input = page.get_by_label("Логин")
                self.password_input = page.get_by_label("Пароль")
                self.submit = page.get_by_role("button", name="Войти")
                self.error = page.get_by_role("alert")

            def open(self):
                self.page.goto("/login")

            def login(self, user, password):
                self.user_input.fill(user)
                self.password_input.fill(password)
                self.submit.click()
        """, xp=20),
    uic(f"{P}-m2-l1-e3", t("""
        Напиши Page Object каталога — класс `CatalogPage(page)` с методами:

        - `open()` — переходит на `/catalog`;
        - `search(text)` — вводит `text` в поле «Поиск» и нажимает «Найти»;
        - `names()` — **дожидается** загрузки товаров (блок `#products`) и возвращает список названий (тексты `.card h3`);
        - `add(name)` — нажимает «В корзину» в карточке товара `name` (карточки — `get_by_test_id("product")`).
        """),
        """
        class CatalogPage:
            def __init__(self, page):
                self.page = page

            def open(self):
                pass

            def search(self, text):
                pass

            def names(self):
                pass

            def add(self, name):
                pass
        """,
        """
        def test_names_and_search():
            page = Page(_shop_app())
            cat = CatalogPage(page)
            cat.open()
            assert cat.names() == ["Клавиатура", "Мышь", "Монитор", "Наушники", "Коврик"], "names() должен дождаться товаров"
            cat.search("мо")
            assert cat.names() == ["Монитор"], f"После поиска «мо»: {cat.names()}"

        def test_add():
            page = Page(_shop_app())
            cat = CatalogPage(page)
            cat.open()
            cat.add("Коврик")
            cat.add("Мышь")
            assert page.app.state["cart"] == {5: 1, 2: 1}, page.app.state["cart"]
        """,
        """
        class CatalogPage:
            def __init__(self, page):
                self.page = page
                self.search_box = page.get_by_placeholder("Поиск")
                self.products = page.get_by_test_id("product")

            def open(self):
                self.page.goto("/catalog")

            def search(self, text):
                self.search_box.fill(text)
                self.page.get_by_role("button", name="Найти").click()

            def names(self):
                self.page.locator("#products").wait_for()
                return self.page.locator(".card h3").all_inner_texts()

            def add(self, name):
                self.products.filter(has_text=name).get_by_role("button", name="В корзину").click()
        """, xp=20),
    uic(f"{P}-m2-l1-e4", t("""
        Напиши Page Object корзины — класс `CartPage(page)`:

        - атрибут `rows` — локатор строк товаров (`get_by_test_id("cart-row")`);
        - `open()` — переходит на `/cart`;
        - `total()` — возвращает сумму из `<p id="total">Итого: 2400 ₽</p>` **числом** (`2400`);
        - `remove(name)` — нажимает «Удалить» в строке товара `name`.

        Строка корзины выглядит так:
        ```html
        <tr data-testid="cart-row"><td class="name">Мышь</td> <td class="qty">2</td> <td class="sum">2400 ₽</td> <td>…<button>Удалить</button>…</td></tr>
        ```
        """),
        """
        class CartPage:
            def __init__(self, page):
                self.page = page

            def open(self):
                pass

            def total(self):
                pass

            def remove(self, name):
                pass
        """,
        """
        def filled():
            app = _shop_app()
            app.state["cart"] = {2: 2, 5: 1}
            return Page(app)

        def test_total():
            cart = CartPage(filled())
            cart.open()
            assert cart.rows.count() == 2, "rows — строки товаров"
            assert cart.total() == 3000, f"Итого: {cart.total()!r}"

        def test_remove():
            page = filled()
            cart = CartPage(page)
            cart.open()
            cart.remove("Коврик")
            assert page.app.state["cart"] == {2: 2}, "Удалить нужно Коврик"
            assert cart.rows.count() == 1 and cart.total() == 2400
        """,
        """
        class CartPage:
            def __init__(self, page):
                self.page = page
                self.rows = page.get_by_test_id("cart-row")

            def open(self):
                self.page.goto("/cart")

            def total(self):
                text = self.page.locator("#total").inner_text()
                return int(text.split()[1])

            def remove(self, name):
                self.rows.filter(has_text=name).get_by_role("button", name="Удалить").click()
        """,
        hint='`"Итого: 2400 ₽".split()` → `["Итого:", "2400", "₽"]`.', xp=20),
    uit(f"{P}-m2-l1-e5", t("""
        Page Object `LoginPage` уже готов (он в заготовке). Напиши тест `test_login_via_page_object(page)`, который **через него** входит как `anna` / `secret` и проверяет, что открылся каталог:
        ```python
        expect(page).to_have_url("http://app.test/catalog")
        ```
        """),
        LOGIN_PAGE + """
        def test_login_via_page_object(page):
            login_page = LoginPage(page)
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_login_via_page_object") == "passed", res
            assert ".login(" in source(), "Входи методом LoginPage.login"

        def test_catches_bug():
            code, res = run_pytest(patch=bug("login_no_redirect"))
            assert res.get("test_login_via_page_object") == "failed", "Тест не поймал баг: после входа сайт остался на /login"
        """,
        LOGIN_PAGE + """
        def test_login_via_page_object(page):
            login_page = LoginPage(page)
            login_page.open()
            login_page.login("anna", "secret")
            expect(page).to_have_url("http://app.test/catalog")
        """),
    uit(f"{P}-m2-l1-e6", t("""
        Через тот же `LoginPage` напиши негативный тест `test_blocked_user(page)`: пользователь `blocked` с паролем `blocked` заблокирован. Проверь, что в `login_page.error` текст **«Пользователь заблокирован»**, а адрес остался `http://app.test/login`.
        """),
        LOGIN_PAGE + """
        def test_blocked_user(page):
            login_page = LoginPage(page)
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_blocked_user") == "passed", res
            src = source()
            assert "login_page.error" in src and "to_have_url" in src, "Проверь и ошибку (login_page.error), и адрес (to_have_url)"
        """,
        LOGIN_PAGE + """
        def test_blocked_user(page):
            login_page = LoginPage(page)
            login_page.open()
            login_page.login("blocked", "blocked")
            expect(login_page.error).to_have_text("Пользователь заблокирован")
            expect(page).to_have_url("http://app.test/login")
        """),
    uic(f"{P}-m2-l1-e7", t("""
        Переходы между страницами удобно выражать через возвращаемые Page Object'ы — тогда тест читается цепочкой:
        ```python
        catalog = LoginPage(page).open().login("anna", "secret")
        catalog.heading.inner_text()   # → "Каталог"
        ```
        Класс `CatalogPage` уже есть. Допиши `LoginPage`:

        - `open()` переходит на `/login` и возвращает **сам объект** (`self`);
        - `login(user, password)` заполняет поля, нажимает «Войти» и возвращает `CatalogPage(self.page)`.
        """),
        """
        class CatalogPage:
            def __init__(self, page):
                self.page = page
                self.heading = page.get_by_role("heading", name="Каталог")


        class LoginPage:
            def __init__(self, page):
                self.page = page

            def open(self):
                pass

            def login(self, user, password):
                pass
        """,
        """
        def test_chain():
            page = Page(_shop_app())
            lp = LoginPage(page)
            assert lp.open() is lp, "open() должен вернуть self"
            catalog = lp.login("anna", "secret")
            assert isinstance(catalog, CatalogPage), "login() должен вернуть CatalogPage"
            assert catalog.heading.inner_text() == "Каталог"
            assert page.get_by_test_id("username").inner_text() == "anna"
        """,
        """
        class CatalogPage:
            def __init__(self, page):
                self.page = page
                self.heading = page.get_by_role("heading", name="Каталог")


        class LoginPage:
            def __init__(self, page):
                self.page = page

            def open(self):
                self.page.goto("/login")
                return self

            def login(self, user, password):
                self.page.get_by_label("Логин").fill(user)
                self.page.get_by_label("Пароль").fill(password)
                self.page.get_by_role("button", name="Войти").click()
                return CatalogPage(self.page)
        """),
    uic(f"{P}-m2-l1-e8", t("""
        Шапка сайта одинакова на всех страницах — её выносят в отдельный **компонент**, который используют разные Page Object'ы.

        Напиши класс `Header(page)`:

        - `cart_count()` — число из ссылки «Корзина (3)» (`get_by_test_id("cart-link")`) → `3`;
        - `username()` — имя из `get_by_test_id("username")` или `None`, если пользователь не вошёл (такого элемента нет — `count() == 0`);
        - `logout()` — нажимает ссылку «Выйти».
        """),
        """
        class Header:
            def __init__(self, page):
                self.page = page

            def cart_count(self):
                pass

            def username(self):
                pass

            def logout(self):
                pass
        """,
        """
        def test_guest():
            h = Header(fresh("/catalog"))
            assert h.username() is None, "Гость — username() is None"
            assert h.cart_count() == 0

        def test_logged():
            app = _shop_app()
            app.state["cart"] = {1: 2, 3: 1}
            app.state["user"] = "anna"
            page = Page(app)
            page.goto("/cart")
            h = Header(page)
            assert h.username() == "anna" and h.cart_count() == 3, (h.username(), h.cart_count())
            h.logout()
            assert page.url.endswith("/login") and h.username() is None
        """,
        """
        class Header:
            def __init__(self, page):
                self.page = page
                self.cart_link = page.get_by_test_id("cart-link")
                self.user = page.get_by_test_id("username")

            def cart_count(self):
                text = self.cart_link.inner_text()
                return int(text[text.index("(") + 1:text.index(")")])

            def username(self):
                return self.user.inner_text() if self.user.count() else None

            def logout(self):
                self.page.get_by_role("link", name="Выйти").click()
        """,
        hint='Из «Корзина (3)»: `text.strip("Корзина ()")` или срез между скобками.'),
),

lesson(f"{P}-m2-l2", "Стратегия UI-автоматизации",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
            tests = {"unit": 700, "api": 250, "ui": 50}
            total = sum(tests.values())
            for level, n in tests.items():
                print(level, f"{n / total:.0%}")
            """),
    cod(f"{P}-m2-l2-e2", t("""
            Напиши функцию `pyramid_ok(unit, api, ui)`, которая проверяет, соблюдена ли пирамида тестирования.

            - Получает: количество модульных (`unit`), API (`api`) и UI (`ui`) тестов.
            - Возвращает: `True`, если модульных тестов **больше**, чем API, **и** API **больше**, чем UI. Иначе `False`.

            Примеры:
            ```
            pyramid_ok(700, 250, 50)   # → True    правильная пирамида
            pyramid_ok(10, 50, 300)    # → False   «рожок мороженого» — UI-тестов больше всего
            ```
            Python умеет цепочки сравнений: `a > b > c`.
            """),
            """
            def pyramid_ok(unit, api, ui):
                pass
            """,
            """
            def test_ok():
                assert pyramid_ok(700, 250, 50) is True, "700 > 250 > 50 — правильная пирамида"

            def test_ice_cream():
                assert pyramid_ok(10, 50, 300) is False, "Перевёрнутая пирамида («рожок мороженого») — плохо"
            """,
            """
            def pyramid_ok(unit, api, ui):
                return unit > api > ui
            """),
    cod(f"{P}-m2-l2-e3", t("""
            Напиши функцию `screenshot_name(test_name, browser)`, которая придумывает имя файла для скриншота упавшего теста.

            - Получает: `test_name` — имя теста в свободной форме; `browser` — имя браузера.
            - Возвращает: строку `"<browser>_<очищенное имя>.png"`, где имя теста очищено так:
              1. все буквы — строчные;
              2. пробелы заменены на `_`;
              3. удалены все символы, кроме букв, цифр и `_`.

            Примеры:
            ```
            screenshot_name("Login Works", "chrome")      # → "chrome_login_works.png"
            screenshot_name("Pay: 100$ OK!", "firefox")   # → "firefox_pay_100_ok.png"
            ```
            Проверить, буква или цифра ли символ: `ch.isalnum()`.
            """),
            """
            def screenshot_name(test_name, browser):
                pass
            """,
            """
            def test_simple():
                assert screenshot_name("Login Works", "chrome") == "chrome_login_works.png", f"Получено {screenshot_name('Login Works', 'chrome')!r}"

            def test_symbols():
                assert screenshot_name("Pay: 100$ OK!", "firefox") == "firefox_pay_100_ok.png", f"Получено {screenshot_name('Pay: 100$ OK!', 'firefox')!r}"
            """,
            """
            def screenshot_name(test_name, browser):
                clean = "".join(ch for ch in test_name.lower().replace(" ", "_") if ch.isalnum() or ch == "_")
                return f"{browser}_{clean}.png"
            """,
            hint="`.lower()`, `.replace(\" \", \"_\")`, затем оставить символы, для которых `ch.isalnum() or ch == \"_\"`."),
    cod(f"{P}-m2-l2-e4", t("""
            Напиши функцию `split_for_workers(tests, n)`, которая распределяет тесты между параллельными процессами.

            - Получает: `tests` — список тестов; `n` — количество воркеров.
            - Раздаёт тесты **по кругу**: 1-й тест — первому воркеру, 2-й — второму, …, `n`-й — последнему, `n+1`-й — снова первому и т. д.
            - Возвращает: список из `n` списков — тесты каждого воркера. Если тестов меньше, чем воркеров, у лишних — пустые списки.

            Примеры:
            ```
            split_for_workers(["a", "b", "c", "d", "e"], 2)   # → [["a", "c", "e"], ["b", "d"]]
            split_for_workers(["a"], 3)                       # → [["a"], [], []]
            ```
            """),
            """
            def split_for_workers(tests, n):
                pass
            """,
            """
            def test_split():
                assert split_for_workers(["a", "b", "c", "d", "e"], 2) == [["a", "c", "e"], ["b", "d"]], f"Получено {split_for_workers(['a', 'b', 'c', 'd', 'e'], 2)}"

            def test_more_workers():
                assert split_for_workers(["a"], 3) == [["a"], [], []], "Лишние воркеры получают пустые списки"
            """,
            """
            def split_for_workers(tests, n):
                return [tests[i::n] for i in range(n)]
            """,
            hint="Срез с шагом: `tests[i::n]` — элементы i, i+n, i+2n…"),
    cod(f"{P}-m2-l2-e5", t("""
            Напиши функцию `summarize(results)` — сводку прогона для отчёта.

            - Получает: `results` — список статусов тестов: `"passed"`, `"failed"` или `"skipped"`.
            - Возвращает словарь с четырьмя ключами:
              - `"passed"`, `"failed"`, `"skipped"` — сколько тестов с каждым статусом;
              - `"pass_rate"` — процент прошедших среди **запущенных** (запущенные = passed + failed, пропущенные не считаются), округлённый до целого. Если запущенных нет — `0`.

            Примеры:
            ```
            summarize(["passed", "failed", "passed", "skipped", "passed"])
            # → {"passed": 3, "failed": 1, "skipped": 1, "pass_rate": 75}   3 из 4 запущенных

            summarize(["skipped"])
            # → {"passed": 0, "failed": 0, "skipped": 1, "pass_rate": 0}
            ```
            """),
            """
            def summarize(results):
                pass
            """,
            """
            def test_summary():
                got = summarize(["passed", "failed", "passed", "skipped", "passed"])
                assert got == {"passed": 3, "failed": 1, "skipped": 1, "pass_rate": 75}, f"Получено {got}"

            def test_all_skipped():
                assert summarize(["skipped"]) == {"passed": 0, "failed": 0, "skipped": 1, "pass_rate": 0}, "Без запущенных pass_rate = 0"
            """,
            """
            def summarize(results):
                passed = results.count("passed")
                failed = results.count("failed")
                run = passed + failed
                return {
                    "passed": passed,
                    "failed": failed,
                    "skipped": results.count("skipped"),
                    "pass_rate": round(100 * passed / run) if run else 0,
                }
            """,
            xp=20),
    cmd(f"{P}-m2-l2-e6", "Запусти тесты параллельно в **4** процесса (плагин pytest-xdist).",
        ["pytest -n 4", r"re:(python -m )?pytest (.* )?-n ?4( .*)?", r"re:(python -m )?pytest (.* )?--numprocesses[ =]4( .*)?"],
        hint="Опция xdist — `-n N`."),
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `is_brittle(selector)`, которая определяет **хрупкий** CSS/XPath-селектор — такой, что сломается от малейшей правки вёрстки.

        Селектор хрупкий (`True`), если выполняется хотя бы одно:
        - начинается с `/` — абсолютный XPath вроде `/html/body/div[2]/span`;
        - содержит `nth-child` — привязка к позиции;
        - в нём **два и больше** символа `>` — длинная цепочка вложенности.

        Иначе — `False`.

        Примеры:
        ```
        is_brittle("/html/body/div[2]/button")          # → True
        is_brittle("ul > li:nth-child(3)")              # → True
        is_brittle("div.main > div > form > button")    # → True
        is_brittle("[data-testid=submit]")              # → False
        is_brittle("form > button")                     # → False
        ```
        """),
        """
        def is_brittle(selector):
            pass
        """,
        """
        def test_brittle():
            for s in ["/html/body/div[2]/button", "ul > li:nth-child(3)", "div.main > div > form > button", "a>b>c"]:
                assert is_brittle(s) is True, f"{s!r} — хрупкий"

        def test_ok():
            for s in ["[data-testid=submit]", "form > button", "#login", ".card .price"]:
                assert is_brittle(s) is False, f"{s!r} — нормальный"
        """,
        """
        def is_brittle(selector):
            return selector.startswith("/") or "nth-child" in selector or selector.count(">") >= 2
        """),
    cmd(f"{P}-m2-l2-e8", "Плагин pytest-playwright запускает тесты в Chromium. Запусти их в **Firefox**.",
        ["pytest --browser firefox", r"re:(python -m )?pytest (.* )?--browser[ =]firefox( .*)?"],
        hint="Опция `--browser`."),
),

lesson(f"{P}-fixtures", "Фикстуры и conftest",
    uit(f"{P}-fixtures-e1", t("""
        Плагин даёт фикстуру `page`, но какой сайт в ней открыть, он узнаёт из фикстуры `app`. Напиши её сам: `app()` возвращает `shop_app()`.

        И тест `test_login_title(page)`: открой `/login` и проверь заголовок вкладки — `expect(page).to_have_title("Вход")`.
        """),
        """
        # фикстура app


        def test_login_title(page):
            pass
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_login_title") == "passed", res
            assert "def app(" in source(), "Нужна фикстура app"
        """,
        """
        @pytest.fixture
        def app():
            return shop_app()


        def test_login_title(page):
            page.goto("/login")
            expect(page).to_have_title("Вход")
        """, head=HEAD_NOAPP),
    uit(f"{P}-fixtures-e2", t("""
        Почти каждому тесту нужен вошедший пользователь. Вынеси вход в фикстуру `logged_in_page(page)`: открывает `/login`, входит как `anna` / `secret` и **возвращает** `page`.

        Тест `test_header_name(logged_in_page)` проверяет имя в шапке (`get_by_test_id("username")`) — `anna`.
        """),
        """
        def test_header_name(logged_in_page):
            pass
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_header_name") == "passed", res
            assert "def logged_in_page(" in source(), "Нужна фикстура logged_in_page"

        def test_catches_bug():
            code, res = run_pytest(patch=bug("wrong_username"))
            assert res.get("test_header_name") == "failed", "Тест не поймал баг: в шапке чужое имя"
        """,
        LOGGED_IN + """
        def test_header_name(logged_in_page):
            expect(logged_in_page.get_by_test_id("username")).to_have_text("anna")
        """),
    uit(f"{P}-fixtures-e3", t("""
        Фикстуры строятся друг на друге. `logged_in_page` уже есть. Напиши фикстуру `two_mice(logged_in_page)`: открывает `/catalog`, **дважды** нажимает «В корзину» у «Мыши» и возвращает страницу.

        Тест `test_cart_total(two_mice)`: открой `/cart` и проверь `#total` — «Итого: 2400 ₽».
        """),
        LOGGED_IN + """
        def test_cart_total(two_mice):
            pass
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_cart_total") == "passed", res
            import re
            assert re.search(r"def two_mice\\(\\s*logged_in_page\\s*\\)", source()), "Нужна фикстура two_mice(logged_in_page)"

        def test_catches_bug():
            code, res = run_pytest(patch=bug("total_wrong"))
            assert res.get("test_cart_total") == "failed", "Тест не поймал баг: «Итого» не учитывает количество"
        """,
        LOGGED_IN + """
        @pytest.fixture
        def two_mice(logged_in_page):
            page = logged_in_page
            page.goto("/catalog")
            mouse = page.get_by_test_id("product").filter(has_text="Мышь").get_by_role("button", name="В корзину")
            mouse.click()
            mouse.click()
            return page


        def test_cart_total(two_mice):
            two_mice.goto("/cart")
            expect(two_mice.locator("#total")).to_have_text("Итого: 2400 ₽")
        """),
    uit(f"{P}-fixtures-e4", t("""
        Фикстура с `yield` умеет «прибираться» после теста. Перепиши `logged_in_page`: до `yield` — вход как `anna` / `secret`, `yield page`, а **после** — выход: нажать ссылку «Выйти».

        Тест `test_header_name(logged_in_page)` — как раньше: в шапке имя `anna`.
        """),
        """
        @pytest.fixture
        def logged_in_page(page):
            page.goto("/login")
            page.get_by_label("Логин").fill("anna")
            page.get_by_label("Пароль").fill("secret")
            page.get_by_role("button", name="Войти").click()
            return page


        def test_header_name(logged_in_page):
            expect(logged_in_page.get_by_test_id("username")).to_have_text("anna")
        """,
        """
        def test_teardown():
            apps = []
            def recording():
                a = _shop_app()
                apps.append(a)
                return a
            code, res = run_pytest(patch={"shop_app": recording})
            assert res.get("test_header_name") == "passed", res
            assert "yield" in source(), "Используй yield"
            assert apps and apps[0].state["user"] is None, "После теста фикстура должна выйти из аккаунта (ссылка «Выйти»)"
        """,
        """
        @pytest.fixture
        def logged_in_page(page):
            page.goto("/login")
            page.get_by_label("Логин").fill("anna")
            page.get_by_label("Пароль").fill("secret")
            page.get_by_role("button", name="Войти").click()
            yield page
            page.get_by_role("link", name="Выйти").click()


        def test_header_name(logged_in_page):
            expect(logged_in_page.get_by_test_id("username")).to_have_text("anna")
        """),
    pyt(f"{P}-fixtures-e5", t("""
        Твой код станет файлом `conftest.py` — его фикстуры доступны всем тестам папки без импорта.

        Объяви в нём две фикстуры:
        - `app()` — возвращает `shop_app()`;
        - `logged_in_page(page)` — входит как `anna` / `secret` и возвращает `page`.

        Проверка создаст рядом файл с тестом, который использует `logged_in_page`.
        """),
        """
        import pytest
        from pwfake.demo import shop_app
        """,
        ct("""
        TEST = '''
        from pwfake.sync_api import expect

        def test_generated(logged_in_page):
            expect(logged_in_page).to_have_url("http://app.test/catalog")
            expect(logged_in_page.get_by_test_id("username")).to_have_text("anna")
        '''

        def test_conftest():
            import textwrap
            code, res = run_with_conftest(textwrap.dedent(TEST), "-W", "ignore::pytest.PytestAssertRewriteWarning")
            assert res.get("test_generated") == "passed", f"Тест с фикстурой logged_in_page не прошёл: {res}"
        """),
        """
        import pytest
        from pwfake.demo import shop_app


        @pytest.fixture
        def app():
            return shop_app()


        @pytest.fixture
        def logged_in_page(page):
            page.goto("/login")
            page.get_by_label("Логин").fill("anna")
            page.get_by_label("Пароль").fill("secret")
            page.get_by_role("button", name="Войти").click()
            return page
        """),
    uit(f"{P}-fixtures-e6", t("""
        Адрес сайта в pytest-playwright задаёт фикстура `base_url` — тогда `page.goto("/login")` дописывает путь к ней. Так один и тот же набор тестов гоняют на тестовом стенде и на предпроде.

        Переопредели фикстуру `base_url`: пусть возвращает `"http://stage.shop.test"`. Тест `test_stage_url(page)` открывает `/login` и проверяет адрес `http://stage.shop.test/login`.
        """),
        """
        def test_stage_url(page):
            page.goto("/login")
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_stage_url") == "passed", res
            assert "def base_url(" in source(), "Переопредели фикстуру base_url"
        """,
        """
        @pytest.fixture
        def base_url():
            return "http://stage.shop.test"


        def test_stage_url(page):
            page.goto("/login")
            expect(page).to_have_url("http://stage.shop.test/login")
        """),
    uit(f"{P}-fixtures-e7", t("""
        Каждый тест получает **свою** страницу и свежий сайт — тесты не влияют друг на друга, и порядок запуска не важен.

        Напиши два теста:
        - `test_add_mouse(page)` — в каталоге добавь «Мышь» и проверь ссылку корзины: «Корзина (1)»;
        - `test_add_keyboard(page)` — то же с «Клавиатурой», тоже «Корзина (1)».

        Ссылка корзины — `get_by_test_id("cart-link")`.
        """),
        """
        def test_add_mouse(page):
            pass


        def test_add_keyboard(page):
            pass
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_add_mouse") == "passed" and res.get("test_add_keyboard") == "passed", res

        def test_catches_bug():
            code, res = run_pytest(patch=bug("cart_count"))
            assert res.get("test_add_mouse") == "failed" and res.get("test_add_keyboard") == "failed", "Тесты не поймали баг: счётчик корзины не меняется"
        """,
        """
        def add(page, name):
            page.goto("/catalog")
            page.get_by_test_id("product").filter(has_text=name).get_by_role("button", name="В корзину").click()


        def test_add_mouse(page):
            add(page, "Мышь")
            expect(page.get_by_test_id("cart-link")).to_have_text("Корзина (1)")


        def test_add_keyboard(page):
            add(page, "Клавиатура")
            expect(page.get_by_test_id("cart-link")).to_have_text("Корзина (1)")
        """),
    cmd(f"{P}-fixtures-e8", "По умолчанию pytest-playwright запускает браузер без окна (headless). Запусти тесты так, чтобы окно браузера было **видно**.",
        ["pytest --headed", r"re:(python -m )?pytest (.* )?--headed( .*)?"],
        hint="Опция `--headed`."),
),

lesson(f"{P}-params", "Параметризация и тестовые данные",
    uit(f"{P}-params-e1", t("""
        Один тест — много данных. Напиши `test_bad_login(page, user, password)` с `@pytest.mark.parametrize("user, password", [...])` на три случая:

        - `anna` / `wrong`
        - `nobody` / `secret`
        - `boris` / `secret`

        В каждом — войти и проверить ошибку (`get_by_role("alert")`) «Неверный логин или пароль».
        """),
        """
        def test_bad_login(page, user, password):
            pass
        """,
        """
        def cases(res):
            return {k: v for k, v in res.items() if k.startswith("test_bad_login[")}

        def test_passes():
            code, res = run_pytest()
            got = cases(res)
            assert len(got) == 3 and set(got.values()) == {"passed"}, f"Нужно 3 прошедших случая: {res}"

        def test_catches_bug():
            code, res = run_pytest(patch=bug("login_no_error"))
            assert set(cases(res).values()) == {"failed"}, "Тесты не поймали баг: ошибка входа не показывается"
        """,
        """
        @pytest.mark.parametrize("user, password", [
            ("anna", "wrong"),
            ("nobody", "secret"),
            ("boris", "secret"),
        ])
        def test_bad_login(page, user, password):
            page.goto("/login")
            page.get_by_label("Логин").fill(user)
            page.get_by_label("Пароль").fill(password)
            page.get_by_role("button", name="Войти").click()
            expect(page.get_by_role("alert")).to_have_text("Неверный логин или пароль")
        """),
    uit(f"{P}-params-e2", t("""
        Параметризуй проверку пустых полей: `test_empty_fields(page, user, password)` на три случая — пустой логин (`""`, `"secret"`), пустой пароль (`"anna"`, `""`) и оба пустые. Ожидаемая ошибка — «Введите логин и пароль».
        """),
        """
        def test_empty_fields(page, user, password):
            pass
        """,
        """
        def test_passes():
            code, res = run_pytest()
            got = {k: v for k, v in res.items() if k.startswith("test_empty_fields[")}
            assert len(got) == 3 and set(got.values()) == {"passed"}, f"Нужно 3 прошедших случая: {res}"
            assert "Введите логин и пароль" in source()
        """,
        """
        @pytest.mark.parametrize("user, password", [("", "secret"), ("anna", ""), ("", "")])
        def test_empty_fields(page, user, password):
            page.goto("/login")
            page.get_by_label("Логин").fill(user)
            page.get_by_label("Пароль").fill(password)
            page.get_by_role("button", name="Войти").click()
            expect(page.get_by_role("alert")).to_have_text("Введите логин и пароль")
        """),
    uit(f"{P}-params-e3", t("""
        Параметризуй поиск: `test_search(page, query, expected)` — ввести `query` в «Поиск», нажать «Найти» и проверить **список** названий найденных товаров (`page.locator(".card h3")`, `to_have_text([...])`).

        | query | expected |
        |---|---|
        | `"мыш"` | `["Мышь"]` |
        | `"к"` | `["Клавиатура", "Наушники", "Коврик"]` |
        | `"МОН"` | `["Монитор"]` |
        """),
        """
        def test_search(page, query, expected):
            pass
        """,
        """
        def test_passes():
            code, res = run_pytest()
            got = {k: v for k, v in res.items() if k.startswith("test_search[")}
            assert len(got) == 3 and set(got.values()) == {"passed"}, f"Нужно 3 прошедших случая: {res}"

        def test_catches_bug():
            code, res = run_pytest(patch=bug("search_broken"))
            got = {k: v for k, v in res.items() if k.startswith("test_search[")}
            assert set(got.values()) == {"failed"}, "Тесты не поймали баг: поиск игнорирует запрос"
        """,
        """
        @pytest.mark.parametrize("query, expected", [
            ("мыш", ["Мышь"]),
            ("к", ["Клавиатура", "Наушники", "Коврик"]),
            ("МОН", ["Монитор"]),
        ])
        def test_search(page, query, expected):
            page.goto("/catalog")
            page.get_by_placeholder("Поиск").fill(query)
            page.get_by_role("button", name="Найти").click()
            expect(page.locator(".card h3")).to_have_text(expected)
        """),
    uit(f"{P}-params-e4", t("""
        Сортировка каталога — выпадающий список с подписью «Сортировка» (`get_by_label`), варианты `price`, `price_desc`, `name`. После выбора нужно нажать «Найти».

        Параметризуй `test_sort(page, sort, first)`: после сортировки **первый** товар (`page.locator(".card h3").first`) — ожидаемый:

        | sort | first |
        |---|---|
        | `"price"` | `"Коврик"` |
        | `"price_desc"` | `"Монитор"` |
        | `"name"` | `"Клавиатура"` |
        """),
        """
        def test_sort(page, sort, first):
            pass
        """,
        """
        def test_passes():
            code, res = run_pytest()
            got = {k: v for k, v in res.items() if k.startswith("test_sort[")}
            assert len(got) == 3 and set(got.values()) == {"passed"}, f"Нужно 3 прошедших случая: {res}"

        def test_catches_bug():
            code, res = run_pytest(patch=bug("sort_broken"))
            got = {k: v for k, v in res.items() if k.startswith("test_sort[")}
            assert list(got.values()).count("failed") >= 2, "Тесты не поймали баг: сортировка не работает"
        """,
        """
        @pytest.mark.parametrize("sort, first", [
            ("price", "Коврик"),
            ("price_desc", "Монитор"),
            ("name", "Клавиатура"),
        ])
        def test_sort(page, sort, first):
            page.goto("/catalog")
            page.get_by_label("Сортировка").select_option(sort)
            page.get_by_role("button", name="Найти").click()
            expect(page.locator(".card h3").first).to_have_text(first)
        """),
    uit(f"{P}-params-e5", t("""
        Фикстура `checkout_page` (в заготовке) входит, кладёт в корзину мышь и открывает оформление заказа. Параметризуй `test_checkout_errors(checkout_page, name, phone, agree, error)` через `pytest.param(..., id=...)`:

        | id | name | phone | agree | error |
        |---|---|---|---|---|
        | `no-name` | `""` | `"+79991234567"` | `True` | «Укажите имя» |
        | `bad-phone` | `"Аня"` | `"123"` | `True` | «Неверный телефон» |
        | `no-agree` | `"Аня"` | `"+79991234567"` | `False` | «Нужно согласие с условиями» |

        Поля — «Имя», «Телефон», чекбокс «Согласен с условиями» (отметь его, только если `agree`), кнопка «Подтвердить». Ошибка — `get_by_role("alert")`.
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


        def test_checkout_errors(checkout_page, name, phone, agree, error):
            pass
        """,
        """
        IDS = ["test_checkout_errors[no-name]", "test_checkout_errors[bad-phone]", "test_checkout_errors[no-agree]"]

        def test_passes():
            code, res = run_pytest()
            assert all(res.get(i) == "passed" for i in IDS), f"Ожидались случаи {IDS}: {res}"

        def test_catches_bug():
            code, res = run_pytest(patch=bug("checkout_no_validation"))
            assert res.get(IDS[0]) == "failed", "Случай no-name не поймал баг: заказ оформляется без имени"
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


        @pytest.mark.parametrize("name, phone, agree, error", [
            pytest.param("", "+79991234567", True, "Укажите имя", id="no-name"),
            pytest.param("Аня", "123", True, "Неверный телефон", id="bad-phone"),
            pytest.param("Аня", "+79991234567", False, "Нужно согласие с условиями", id="no-agree"),
        ])
        def test_checkout_errors(checkout_page, name, phone, agree, error):
            page = checkout_page
            page.get_by_label("Имя").fill(name)
            page.get_by_label("Телефон").fill(phone)
            if agree:
                page.get_by_label("Согласен с условиями").check()
            page.get_by_role("button", name="Подтвердить").click()
            expect(page.get_by_role("alert")).to_have_text(error)
        """, xp=25),
    cod(f"{P}-params-e6", t("""
        Тестовые данные часто хранят в CSV-файле. Напиши функцию `cases_from_csv(text)`, которая превращает содержимое CSV в список кортежей для `parametrize`.

        - Получает: `text` — строку CSV; первая строка — заголовок, её пропусти.
        - Возвращает: список кортежей — по одному на каждую строку данных.

        Пример:
        ```
        text = "login,password,error\\nanna,wrong,Неверный логин или пароль\\n,secret,Введите логин и пароль\\n"
        cases_from_csv(text)
        # → [("anna", "wrong", "Неверный логин или пароль"), ("", "secret", "Введите логин и пароль")]
        ```
        Модуль `csv` умеет разбирать строки: `csv.reader(text.splitlines())`.
        """),
        """
        import csv


        def cases_from_csv(text):
            pass
        """,
        """
        def test_cases():
            text = "login,password,error\\nanna,wrong,Неверный логин или пароль\\n,secret,Введите логин и пароль\\n"
            got = cases_from_csv(text)
            assert got == [("anna", "wrong", "Неверный логин или пароль"), ("", "secret", "Введите логин и пароль")], f"Получено {got}"

        def test_quotes():
            got = cases_from_csv('name,comment\\n"Иванов, Иван","ok"\\n')
            assert got == [("Иванов, Иван", "ok")], f"Запятая в кавычках — часть значения: {got}"
        """,
        """
        import csv


        def cases_from_csv(text):
            rows = list(csv.reader(text.splitlines()))
            return [tuple(row) for row in rows[1:]]
        """,
        hint="`list(csv.reader(...))[1:]` — строки без заголовка; каждую переведи в `tuple`."),
    uit(f"{P}-params-e7", t("""
        Параметризуй успешный вход: `test_user_login(page, user, password)` для пар `("anna", "secret")` и `("boris", "qwerty123")`. После входа в шапке (`get_by_test_id("username")`) должно быть имя **этого** пользователя.
        """),
        """
        def test_user_login(page, user, password):
            pass
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_user_login[anna-secret]") == "passed" and res.get("test_user_login[boris-qwerty123]") == "passed", res

        def test_catches_bug():
            code, res = run_pytest(patch=bug("wrong_username"))
            assert res.get("test_user_login[anna-secret]") == "failed", "Тест не поймал баг: в шапке имя другого пользователя"
        """,
        """
        @pytest.mark.parametrize("user, password", [("anna", "secret"), ("boris", "qwerty123")])
        def test_user_login(page, user, password):
            page.goto("/login")
            page.get_by_label("Логин").fill(user)
            page.get_by_label("Пароль").fill(password)
            page.get_by_role("button", name="Войти").click()
            expect(page.get_by_test_id("username")).to_have_text(user)
        """),
    cmd(f"{P}-params-e8", "Упал только случай `bad-phone`. Запусти **только его** — по идентификатору узла из списка ниже.",
        ['pytest "test_checkout.py::test_checkout_errors[bad-phone]"',
         r're:(python -m )?pytest ["\']?test_checkout\.py::test_checkout_errors\[bad-phone\]["\']?( .*)?'],
        context="""
        $ pytest --collect-only -q
        test_checkout.py::test_checkout_errors[no-name]
        test_checkout.py::test_checkout_errors[bad-phone]
        test_checkout.py::test_checkout_errors[no-agree]
        """,
        hint="Передай pytest строку из списка целиком, лучше в кавычках — из-за квадратных скобок."),
),
)
