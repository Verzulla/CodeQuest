"""pytest-плагин pwfake — как pytest-playwright: даёт тестам фикстуры browser и page.

Страница открывает приложение из фикстуры app. По умолчанию это приложение из
set_app(); свой проект переопределяет фикстуру app (в тестовом файле или conftest.py)."""
import pytest

from . import sync_api


@pytest.fixture
def app():
    # None — страница без сайта: работает только page.set_content()
    return sync_api._DEFAULT_APP


@pytest.fixture
def base_url():
    return "http://app.test"


@pytest.fixture
def browser():
    browser = sync_api._Browser("chromium")
    yield browser
    browser.close()


@pytest.fixture
def page(browser, app, base_url):
    page = browser.new_page(app=app, base_url=base_url)
    yield page
    page.close()
