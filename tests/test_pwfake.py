"""Учебная реализация Playwright (deploy/runner/pwfake), на которой построены UI-задания."""
import re

import pytest

pytest_plugins = ["pytester"]

pwfake = pytest.importorskip("pwfake.sync_api")
from pwfake.sync_api import App, Redirect, Page, expect, sync_playwright, set_app, Error, TimeoutError  # noqa: E402

LOGIN = """
<html><head><title>Вход</title></head><body>
  <h1>Вход в магазин</h1>
  <form method="post" action="/login">
    <label for="user">Логин</label><input id="user" name="user" data-testid="login-input">
    <label>Пароль <input type="password" name="password" placeholder="Пароль"></label>
    <label><input type="checkbox" name="remember"> Запомнить</label>
    <select name="lang"><option value="ru">Русский</option><option value="en">English</option></select>
    <button type="submit" class="btn primary">Войти</button>
  </form>
  <a href="/help">Помощь</a>
  <div id="error" class="alert" hidden>Неверный пароль</div>
  <button data-toggle="#details">Подробнее</button>
  <p id="details" hidden>Скрытый текст</p>
  <ul class="menu"><li>Главная</li><li>Каталог</li><li>Корзина</li></ul>
  <div id="spinner" data-disappear-after="800">Загрузка…</div>
  <div id="late" data-appear-after="1500">Готово</div>
</body></html>
"""


def make_app():
    app = App()

    @app.route("/login")
    def login(request):
        return LOGIN

    @app.route("/login", method="POST")
    def do_login(request):
        app.state["form"] = dict(request.form)
        if request.form.get("user") == "anna" and request.form.get("password") == "secret":
            return Redirect("/dashboard")
        return LOGIN.replace('id="error" class="alert" hidden', 'id="error" class="alert"')

    @app.route("/dashboard")
    def dashboard(request):
        return "<html><head><title>Кабинет</title></head><body><h1>Привет, anna</h1></body></html>"

    @app.route("/help")
    def help_page(request):
        return "<title>Помощь</title><p>FAQ</p>"

    return app


@pytest.fixture
def page():
    p = Page(make_app())
    p.goto("/login")
    return p


def test_locators(page):
    assert page.title() == "Вход" and page.url == "http://app.test/login"
    assert page.locator("button.primary").inner_text() == "Войти"
    assert page.locator("form input[name=user]").count() == 1
    assert page.locator("ul.menu > li").count() == 3
    assert page.get_by_role("heading", name="Вход в магазин").is_visible()
    assert page.get_by_role("button", name="Войти").count() == 1
    assert page.get_by_role("link", name="Помощь").count() == 1
    assert page.get_by_label("Логин").get_attribute("name") == "user"
    assert page.get_by_label("Пароль").get_attribute("type") == "password"
    assert page.get_by_placeholder("Пароль").count() == 1
    assert page.get_by_test_id("login-input").get_attribute("id") == "user"
    assert page.get_by_text("Каталог").count() == 1
    assert page.locator("li").nth(2).inner_text() == "Корзина"
    assert page.locator("li").filter(has_text="Глав").count() == 1
    assert page.locator("text=Помощь").count() == 1


def test_strict_mode(page):
    with pytest.raises(Error, match="strict mode violation"):
        page.locator("li").click()


def test_form_submit_redirect(page):
    page.get_by_label("Логин").fill("anna")
    page.get_by_placeholder("Пароль").fill("secret")
    page.get_by_label("Запомнить").check()
    page.locator("select").select_option("en")
    page.get_by_role("button", name="Войти").click()
    assert page.url == "http://app.test/dashboard"
    expect(page).to_have_title("Кабинет")
    expect(page.get_by_role("heading")).to_have_text("Привет, anna")


def test_form_values_and_error(page):
    app = page.app
    page.get_by_label("Логин").fill("bob")
    page.get_by_label("Пароль").press("Enter")
    assert app.state["form"] == {"user": "bob", "password": "", "lang": "ru"}
    expect(page.locator("#error")).to_be_visible()
    expect(page.locator("#error")).to_have_text("Неверный пароль")


def test_navigation_and_toggle(page):
    expect(page.locator("#details")).to_be_hidden()
    page.get_by_role("button", name="Подробнее").click()
    expect(page.locator("#details")).to_be_visible()
    page.get_by_role("link", name="Помощь").click()
    expect(page).to_have_url(re.compile(r"/help$"))
    page.go_back()
    assert page.url.endswith("/login")


def test_auto_wait(page):
    assert not page.locator("#late").is_visible()
    expect(page.locator("#late")).to_have_text("Готово")         # ждёт появления
    assert page.clock >= 1500
    expect(page.locator("#spinner")).not_to_be_visible()


def test_expect_failure_message(page):
    with pytest.raises(AssertionError, match="ожидалось: текст 'Выйти'"):
        expect(page.get_by_role("button", name="Войти")).to_have_text("Выйти", timeout=300)


def test_action_timeout(page):
    with pytest.raises(TimeoutError):
        page.locator("#nope").click(timeout=200)


def test_sync_playwright_default_app():
    set_app(make_app())
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pg = browser.new_page()
        pg.goto("/login")
        assert pg.get_by_role("button", name="Войти").is_enabled()
        browser.close()
    set_app(None)


def test_pytest_plugin_page_fixture(pytester):
    pytester.makepyfile("""
        import pytest
        from pwfake.sync_api import App, expect

        @pytest.fixture
        def app():
            app = App()
            app.route("/")(lambda r: "<title>Главная</title><h1>Привет</h1>")
            return app

        def test_home(page):
            page.goto("/")
            expect(page).to_have_title("Главная")
            expect(page.get_by_role("heading")).to_have_text("Привет")
    """)
    pytester.runpytest("-p", "no:cacheprovider").assert_outcomes(passed=1)
