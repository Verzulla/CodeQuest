"""Тема «Тестирование UI», модуль 1 «Playwright: первые шаги» — задания. Теория — в _ui_t1.py.

Слаги ui-m1-l1, ui-m1-l2 унаследованы от старой темы — так сохраняется прогресс.

UI-задания работают на pwfake — учебной реализации Playwright без браузера (deploy/runner/pwfake):
API тот же, отличается только импорт. Тестируемый сайт — демо-магазин pwfake.demo.shop_app(),
а shop_app(bug="...") — он же с багом: так проверяется, что тест ученика ловит ошибку."""
from ._lib import PYTEST_RUNNER, cmd, cod, d, lesson, module, out, t

P = "ui"

# Шапка заданий «напиши тест»: фикстура app говорит плагину pwfake, какой сайт открывать в page.
HEAD = """import pytest
from pwfake.sync_api import Page, expect
from pwfake.demo import shop_app


@pytest.fixture
def app():
    return shop_app()   # тестируемый сайт «Шоп»


"""

# «▶ Запустить» показывает вывод pytest (без шумного предупреждения о перезаписи assert в pwfake).
UI_MAIN = """


if __name__ == "__main__":
    pytest.main(["-q", "-p", "no:cacheprovider", "-W", "ignore::pytest.PytestAssertRewriteWarning", "solution.py"])
"""

UI_TESTS = """from pwfake.sync_api import Page, expect
from pwfake.demo import shop_app as _shop_app


def bug(name):
    # Сайт с багом вместо исправного: тест ученика должен упасть.
    return {"shop_app": lambda: _shop_app(bug=name)}


def source():
    return open("solution.py", encoding="utf-8").read()


def fresh(path="/login"):
    # Страница исправного сайта для проверки функций и Page Object ученика.
    page = Page(_shop_app())
    page.goto(path)
    return page


def logged_in(path="/catalog"):
    page = fresh()
    page.get_by_label("Логин").fill("anna")
    page.get_by_label("Пароль").fill("secret")
    page.get_by_role("button", name="Войти").click()
    page.goto(path)
    return page


"""


def uit(slug, prompt, starter, tests, solution, hint="", xp=20, head=HEAD):
    """Задание «напиши UI-тест»: тесты ученика запускаются pytest'ом на демо-сайте (и на сайте с багом)."""
    return cod(slug, prompt, head + d(starter).rstrip("\n") + UI_MAIN, PYTEST_RUNNER + UI_TESTS + d(tests),
               head + d(solution).rstrip("\n") + UI_MAIN, hint=hint, xp=xp)


def uic(slug, prompt, starter, tests, solution, hint="", xp=15):
    """Задание «напиши функцию/класс над page»: проверки получают страницы демо-сайта через fresh()."""
    return cod(slug, prompt, starter, UI_TESTS + d(tests), solution, hint=hint, xp=xp)


m1 = module(f"{P}-m1", "Playwright: первые шаги", "🎭", "Локаторы, автоожидание, действия с формами и проверки expect",

lesson(f"{P}-m1-l1", "Локаторы",
    out(f"{P}-m1-l1-e1", "Что выведет программа? Ищем элементы по роли.", """
        from pwfake.sync_api import Page

        page = Page()
        page.set_content('''
        <h1>Корзина</h1>
        <button>Купить</button>
        <button>Удалить</button>
        <a href="/help">Помощь</a>
        ''')
        print(page.get_by_role("button").count())
        print(page.get_by_role("button", name="Купить").inner_text())
        print(page.get_by_role("link").inner_text())
        print(page.get_by_role("heading").inner_text())
        """),
    out(f"{P}-m1-l1-e2", "Что выведет программа? Поля ищем по подписи и плейсхолдеру.", """
        from pwfake.sync_api import Page

        page = Page()
        page.set_content('''
        <label for="email">Почта</label>
        <input id="email" name="email" placeholder="you@mail.ru">
        <label>Пароль <input type="password" name="pwd"></label>
        <input name="promo" placeholder="Промокод">
        ''')
        print(page.get_by_label("Почта").get_attribute("name"))
        print(page.get_by_label("Пароль").get_attribute("type"))
        print(page.get_by_placeholder("Промокод").get_attribute("name"))
        print(page.get_by_role("textbox").count())
        """),
    out(f"{P}-m1-l1-e3", "Что выведет программа? `get_by_text` по умолчанию ищет подстроку без учёта регистра, `exact=True` — точное совпадение.", """
        from pwfake.sync_api import Page

        page = Page()
        page.set_content('''
        <p>Товар добавлен</p>
        <p>Товар добавлен в корзину</p>
        <p>ТОВАР ЗАКОНЧИЛСЯ</p>
        ''')
        print(page.get_by_text("товар").count())
        print(page.get_by_text("Товар добавлен").count())
        print(page.get_by_text("Товар добавлен", exact=True).count())
        """),
    out(f"{P}-m1-l1-e4", "Что выведет программа? CSS-селекторы, `data-testid` и выбор из нескольких.", """
        from pwfake.sync_api import Page

        page = Page()
        page.set_content('''
        <ul class="menu">
          <li>Главная</li>
          <li>Каталог</li>
          <li data-testid="cart">Корзина</li>
        </ul>
        ''')
        items = page.locator("ul.menu li")
        print(items.count())
        print(items.first.inner_text(), items.last.inner_text())
        print(items.nth(1).inner_text())
        print(page.get_by_test_id("cart").inner_text())
        """),
    uic(f"{P}-m1-l1-e5", t("""
        Напиши функцию `buy_button(page)`, которая возвращает **локатор** кнопки «Купить».

        На странице несколько кнопок и ссылка с таким же текстом:
        ```html
        <a href="/buy">Купить</a>
        <button>В избранное</button>
        <button>Купить</button>
        ```
        Найди именно кнопку — по **роли** `button` и имени `"Купить"`. Функция ничего не нажимает, только возвращает локатор.
        """),
        """
        def buy_button(page):
            pass
        """,
        """
        HTML = '<a href="/buy">Купить</a> <button>В избранное</button> <button>Купить</button>'

        def test_locator():
            page = Page()
            page.set_content(HTML)
            loc = buy_button(page)
            assert loc is not None, "Функция должна вернуть локатор"
            assert loc.count() == 1, f"Локатор находит {loc.count()} элемент(а), а нужен ровно один"
            assert loc.get_attribute("href") is None and loc.inner_text() == "Купить", "Найдена не кнопка"

        def test_by_role():
            assert "get_by_role" in source(), "Ищи по роли: get_by_role"
        """,
        """
        def buy_button(page):
            return page.get_by_role("button", name="Купить")
        """,
        hint='`page.get_by_role("button", name="Купить")` — ссылка имеет роль `link`, поэтому не попадёт.'),
    uic(f"{P}-m1-l1-e6", t("""
        Напиши функцию `fill_login(page, user, password)`, которая заполняет форму входа демо-сайта. Страница входа уже открыта.

        Форма такая:
        ```html
        <label for="user">Логин</label> <input id="user" name="user">
        <label for="password">Пароль</label> <input id="password" name="password" type="password">
        ```
        Найди поля по подписи — `get_by_label` — и заполни методом `fill(...)`. Кнопку «Войти» нажимать не нужно.
        """),
        """
        def fill_login(page, user, password):
            pass
        """,
        """
        def test_fill():
            page = fresh()
            fill_login(page, "anna", "secret")
            assert page.locator("#user").input_value() == "anna", "Логин не заполнен"
            assert page.locator("#password").input_value() == "secret", "Пароль не заполнен"
            assert page.url.endswith("/login"), "Форму не нужно отправлять"

        def test_by_label():
            assert "get_by_label" in source(), "Ищи поля по подписи: get_by_label"
        """,
        """
        def fill_login(page, user, password):
            page.get_by_label("Логин").fill(user)
            page.get_by_label("Пароль").fill(password)
        """),
    uic(f"{P}-m1-l1-e7", t("""
        Напиши функцию `price_of(page, name)`, которая возвращает цену товара **числом**.

        Карточки товаров на странице такие:
        ```html
        <div class="card" data-testid="product"><h3>Мышь</h3> <span class="price">1200 ₽</span></div>
        <div class="card" data-testid="product"><h3>Коврик</h3> <span class="price">600 ₽</span></div>
        ```
        Возьми все карточки (`get_by_test_id("product")`), оставь нужную через `.filter(has_text=name)`, внутри неё найди `.price` (`.locator(".price")`), прочитай текст и переведи в `int`.

        Пример: `price_of(page, "Мышь")` → `1200`.
        """),
        """
        def price_of(page, name):
            pass
        """,
        """
        HTML = ''.join(f'<div class="card" data-testid="product"><h3>{n}</h3> <span class="price">{p} ₽</span></div>'
                       for n, p in [("Мышь", 1200), ("Коврик", 600), ("Монитор", 15000)])

        def test_prices():
            page = Page()
            page.set_content(HTML)
            got = [price_of(page, n) for n in ("Мышь", "Коврик", "Монитор")]
            assert got == [1200, 600, 15000], f"Получено {got}"

        def test_filter():
            assert "filter(" in source(), "Выбери карточку через .filter(has_text=...)"
        """,
        """
        def price_of(page, name):
            text = page.get_by_test_id("product").filter(has_text=name).locator(".price").inner_text()
            return int(text.split()[0])
        """,
        hint='Текст цены — `"1200 ₽"`: `int(text.split()[0])` или `int(text.replace("₽", ""))`.'),
    cmd(f"{P}-m1-l1-e8", "Напиши выражение-локатор для кнопки «Оформить заказ» по роли (объект страницы — `page`).",
        ['page.get_by_role("button", name="Оформить заказ")',
         r're:page\.get_by_role\(\s*["\']button["\']\s*,\s*name\s*=\s*["\']Оформить заказ["\']\s*(,\s*exact\s*=\s*True\s*)?\)'],
        hint="`page.get_by_role(роль, name=имя)`."),
),

lesson(f"{P}-m1-l2", "Ожидания и флаки",
    out(f"{P}-m1-l2-e1", "Что выведет программа? Элемент появляется через 1,5 секунды (`data-appear-after` — так pwfake имитирует долгую загрузку). У страницы фейковые часы `page.clock` в миллисекундах.", """
        from pwfake.sync_api import Page, expect

        page = Page()
        page.set_content('<div id="done" data-appear-after="1500">Готово</div>')
        print(page.locator("#done").is_visible())
        expect(page.locator("#done")).to_be_visible()
        print(page.locator("#done").is_visible())
        print(page.clock)
        """),
    out(f"{P}-m1-l2-e2", "Что выведет программа? `count()` не ждёт, а `expect(...).to_have_count()` — ждёт.", """
        from pwfake.sync_api import Page, expect

        page = Page()
        page.set_content('''
        <div id="list" data-appear-after="800">
          <p class="item">Мышь</p>
          <p class="item">Коврик</p>
        </div>
        ''')
        items = page.locator(".item")
        print(items.count())
        expect(items).to_have_count(2)
        print(items.count(), page.clock)
        """),
    out(f"{P}-m1-l2-e3", "Что выведет программа? Если элемент так и не появился — ожидание обрывается по таймауту (здесь 1 секунда вместо обычных пяти).", """
        from pwfake.sync_api import Page, TimeoutError

        page = Page()
        page.set_content('<button id="pay" data-appear-after="3000">Оплатить</button>')
        try:
            page.locator("#pay").click(timeout=1000)
        except TimeoutError:
            print("не дождались, часы:", page.clock)
        page.locator("#pay").click()
        print("нажали, часы:", page.clock)
        """),
    uic(f"{P}-m1-l2-e6", t("""
        Функция `product_names(page)` должна вернуть список названий товаров каталога. Но товары подгружаются не сразу — сначала видна надпись «Загрузка…», а через какое-то время появляется блок:
        ```html
        <div id="products">
          <div class="card" data-testid="product"><h3>Клавиатура</h3> …</div>
          …
        </div>
        ```
        Наивное решение `page.locator(".card h3").all_inner_texts()` вернёт `[]`: элементы ещё не загрузились.

        Сначала **дождись** блока `#products` — `page.locator("#products").wait_for()`, — а потом верни тексты всех `.card h3`.
        """),
        """
        def product_names(page):
            return page.locator(".card h3").all_inner_texts()
        """,
        """
        def test_normal():
            page = fresh("/catalog")
            assert product_names(page) == ["Клавиатура", "Мышь", "Монитор", "Наушники", "Коврик"], "Товары не дождались"

        def test_slow():
            page = Page(_shop_app(bug="slow"))
            page.goto("/catalog")
            assert len(product_names(page)) == 5, "При медленной загрузке (3 с) тоже нужно дождаться"

        def test_no_sleep():
            assert "wait_for_timeout" not in source(), "Без фиксированных пауз: жди появления элемента"
        """,
        """
        def product_names(page):
            page.locator("#products").wait_for()
            return page.locator(".card h3").all_inner_texts()
        """,
        hint="`wait_for()` по умолчанию ждёт, пока элемент станет видимым (до 5 секунд)."),
    uit(f"{P}-m1-l2-e7", t("""
        Напиши тест `test_catalog_loaded(page)`: открой `/catalog` и проверь, что загрузились **5** карточек товаров (`get_by_test_id("product")`).

        Товары появляются с задержкой, поэтому проверяй через `expect(...).to_have_count(5)` — он подождёт. Никаких `wait_for_timeout`: тест должен проходить и когда сайт тормозит 3 секунды.
        """),
        """
        def test_catalog_loaded(page):
            page.goto("/catalog")
            # проверь, что карточек 5
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_catalog_loaded") == "passed", res

        def test_slow_site():
            code, res = run_pytest(patch=bug("slow"))
            assert res.get("test_catalog_loaded") == "passed", "На медленном сайте (3 с) тест должен дождаться товаров"

        def test_real_check():
            code, res = run_pytest(patch=bug("too_slow"))
            assert res.get("test_catalog_loaded") == "failed", "Если товары не появились за 5 секунд — тест должен упасть"
            assert "wait_for_timeout" not in source(), "Не используй фиксированные паузы"
        """,
        """
        def test_catalog_loaded(page):
            page.goto("/catalog")
            expect(page.get_by_test_id("product")).to_have_count(5)
        """),
    cod(f"{P}-m1-l2-e4", t("""
        Напиши функцию `run_with_retries(test, retries)` — запуск теста с перезапусками, как плагин pytest-rerunfailures.

        - Получает: `test` — функцию без аргументов (тест), которая падает с `AssertionError`; `retries` — сколько раз можно перезапустить.
        - Логика:
          - запускает `test()`; если прошёл без ошибки — возвращает номер попытки (1, 2, …);
          - если упал с `AssertionError` — пробует снова;
          - всего попыток не больше `1 + retries`;
          - если упали **все** попытки — пробрасывает ошибку наружу.

        Примеры (`retries=2`, то есть до 3 попыток):
        ```
        тест проходит сразу              → 1
        падает 2 раза, потом проходит    → 3
        падает всегда                    → AssertionError
        ```
        Пробросить пойманную ошибку дальше можно командой `raise` без аргументов внутри `except`.
        """),
        """
        def run_with_retries(test, retries):
            pass
        """,
        """
        def make_test(fail_times):
            state = {"calls": 0}
            def test():
                state["calls"] += 1
                assert state["calls"] > fail_times, "упал"
            return test

        def test_first_try():
            assert run_with_retries(make_test(0), 2) == 1, "Прошёл с первого раза → 1"

        def test_third_try():
            assert run_with_retries(make_test(2), 2) == 3, "Два падения, потом успех → 3"

        def test_gives_up():
            try:
                run_with_retries(make_test(10), 2)
            except AssertionError:
                return
            assert False, "Если все попытки упали — нужно пробросить AssertionError"
        """,
        """
        def run_with_retries(test, retries):
            for attempt in range(1, retries + 2):
                try:
                    test()
                    return attempt
                except AssertionError:
                    if attempt == retries + 1:
                        raise
        """,
        hint="Цикл по попыткам; в `except` на последней попытке — голый `raise` пробросит ту же ошибку.", xp=20),
    cod(f"{P}-m1-l2-e5", t("""
        Напиши функцию `flaky_report(runs)` — отчёт о флаки-тестах по истории прогонов.

        - Получает: `runs` — словарь `{имя_теста: [результаты прогонов]}`, результаты — `"pass"` / `"fail"`.
        - Возвращает: **отсортированный по алфавиту** список имён флаки-тестов (у которых в истории есть и `"pass"`, и `"fail"`).

        Пример:
        ```
        flaky_report({
            "test_login":  ["pass", "pass"],
            "test_search": ["pass", "fail", "pass"],
            "test_cart":   ["fail", "pass"],
            "test_pay":    ["fail", "fail"],
        })
        # → ["test_cart", "test_search"]
        ```
        """),
        """
        def flaky_report(runs):
            pass
        """,
        """
        def test_report():
            runs = {
                "test_login": ["pass", "pass"],
                "test_search": ["pass", "fail", "pass"],
                "test_cart": ["fail", "pass"],
                "test_pay": ["fail", "fail"],
            }
            assert flaky_report(runs) == ["test_cart", "test_search"], f"Получено {flaky_report(runs)}"
        """,
        """
        def flaky_report(runs):
            return sorted(name for name, h in runs.items() if "pass" in h and "fail" in h)
        """),
    cmd(f"{P}-m1-l2-e8", "С плагином pytest-rerunfailures упавший тест можно автоматически перезапустить. Запусти тесты так, чтобы каждый упавший перезапускался до **2** раз.",
        ["pytest --reruns 2", r"re:(python -m )?pytest (.* )?--reruns[ =]2( .*)?"],
        hint="Опция плагина — `--reruns N`."),
),

lesson(f"{P}-actions", "Действия: клики и формы",
    out(f"{P}-actions-e1", "Что выведет программа? `fill` заменяет значение поля, `input_value` — читает его.", """
        from pwfake.sync_api import Page

        page = Page()
        page.set_content('<input name="q" value="клав">')
        box = page.locator("input")
        print(repr(box.input_value()))
        box.fill("мышь")
        print(repr(box.input_value()))
        box.clear()
        print(repr(box.input_value()))
        """),
    out(f"{P}-actions-e2", "Что выведет программа? Чекбоксы и выпадающий список.", """
        from pwfake.sync_api import Page

        page = Page()
        page.set_content('''
        <label><input type="checkbox" name="agree"> Согласен</label>
        <select name="delivery">
          <option value="courier">Курьер</option>
          <option value="pickup">Самовывоз</option>
        </select>
        ''')
        agree = page.get_by_label("Согласен")
        print(agree.is_checked())
        agree.check()
        print(agree.is_checked())
        print(page.locator("select").input_value())
        print(page.locator("select").select_option(label="Самовывоз"))
        print(page.locator("select").input_value())
        """),
    out(f"{P}-actions-e3", "Что выведет программа? Кнопка «Подробнее» показывает и прячет блок (в pwfake это атрибут `data-toggle`).", """
        from pwfake.sync_api import Page

        page = Page()
        page.set_content('''
        <button data-toggle="#info">Подробнее</button>
        <p id="info" hidden>Доставка 1–2 дня</p>
        ''')
        info = page.locator("#info")
        print(info.is_visible())
        page.get_by_role("button", name="Подробнее").click()
        print(info.is_visible(), info.inner_text())
        page.get_by_role("button", name="Подробнее").click()
        print(info.is_visible())
        """),
    out(f"{P}-actions-e4", "Что выведет программа? Недоступную кнопку нажать нельзя, а локатор, который нашёл несколько элементов, не знает, какой нажимать.", """
        from pwfake.sync_api import Page, Error

        page = Page()
        page.set_content('''
        <button disabled>Нет в наличии</button>
        <button>В корзину</button>
        <button>В корзину</button>
        ''')
        print(page.get_by_role("button", name="Нет в наличии").is_enabled())
        try:
            page.get_by_role("button", name="В корзину").click()
        except Error as e:
            print(str(e).split(":")[0])
        page.get_by_role("button", name="В корзину").first.click()
        print("нажали первую")
        """),
    uic(f"{P}-actions-e5", t("""
        Напиши функцию `login(page, user, password)`: открывает страницу входа `/login`, заполняет поля «Логин» и «Пароль» и нажимает кнопку «Войти».

        После верного входа сайт переходит в каталог (`/catalog`), после неверного — остаётся на `/login` и показывает ошибку.
        """),
        """
        def login(page, user, password):
            page.goto("/login")
            # заполни поля и нажми «Войти»
        """,
        """
        def test_success():
            page = fresh("/catalog")
            login(page, "anna", "secret")
            assert page.url == "http://app.test/catalog", f"После входа ожидался /catalog, а сейчас {page.url}"
            assert page.get_by_test_id("username").inner_text() == "anna"

        def test_wrong():
            page = fresh("/catalog")
            login(page, "anna", "nope")
            assert page.url.endswith("/login"), "При неверном пароле сайт остаётся на /login"
        """,
        """
        def login(page, user, password):
            page.goto("/login")
            page.get_by_label("Логин").fill(user)
            page.get_by_label("Пароль").fill(password)
            page.get_by_role("button", name="Войти").click()
        """),
    uic(f"{P}-actions-e6", t("""
        Напиши функцию `search(page, text)`: на странице каталога вводит `text` в поле с плейсхолдером «Поиск» и нажимает **Enter** — `press("Enter")` отправляет форму, как в браузере.

        Сайт перейдёт на адрес вида `/catalog?q=мышь&sort=`.
        """),
        """
        def search(page, text):
            pass
        """,
        """
        def test_search():
            page = fresh("/catalog")
            search(page, "мышь")
            assert "q=мышь" in page.url, f"Поиск не отправлен: {page.url}"

        def test_enter():
            assert 'press("Enter")' in source() or "press('Enter')" in source(), "Отправь форму клавишей Enter: press(\\"Enter\\")"
        """,
        """
        def search(page, text):
            box = page.get_by_placeholder("Поиск")
            box.fill(text)
            box.press("Enter")
        """),
    uic(f"{P}-actions-e7", t("""
        Напиши функцию `add_to_cart(page, name)`: в каталоге нажимает кнопку «В корзину» у товара `name`.

        Карточка товара:
        ```html
        <div class="card" data-testid="product">
          <h3>Мышь</h3> <span class="price">1200 ₽</span>
          <form …><button type="submit">В корзину</button></form>
        </div>
        ```
        Кнопок «В корзину» много — выбери карточку через `filter(has_text=name)` и нажми кнопку внутри неё. Действия Playwright сами ждут появления элемента, так что загрузку каталога ждать отдельно не нужно.

        После добавления счётчик в шапке — ссылка «Корзина (1)».
        """),
        """
        def add_to_cart(page, name):
            pass
        """,
        """
        def test_add():
            page = fresh("/catalog")
            add_to_cart(page, "Мышь")
            add_to_cart(page, "Мышь")
            add_to_cart(page, "Коврик")
            assert page.get_by_test_id("cart-link").inner_text() == "Корзина (3)", page.get_by_test_id("cart-link").inner_text()
            assert page.app.state["cart"] == {2: 2, 5: 1}, f"В корзине не те товары: {page.app.state['cart']}"
        """,
        """
        def add_to_cart(page, name):
            card = page.get_by_test_id("product").filter(has_text=name)
            card.get_by_role("button", name="В корзину").click()
        """,
        hint='`page.get_by_test_id("product").filter(has_text=name).get_by_role("button").click()`'),
    uit(f"{P}-actions-e8", t("""
        Напиши первый настоящий UI-тест `test_login_success(page)`: открой `/login`, войди как `anna` / `secret` и проверь, что адрес страницы стал `http://app.test/catalog`:
        ```python
        expect(page).to_have_url("http://app.test/catalog")
        ```
        Фикстура `page` приходит из плагина (как в pytest-playwright), а фикстура `app` сверху говорит ему, какой сайт открыть.
        """),
        """
        def test_login_success(page):
            page.goto("/login")
            # войди и проверь адрес
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_login_success") == "passed", res

        def test_catches_bug():
            code, res = run_pytest(patch=bug("login_no_redirect"))
            assert res.get("test_login_success") == "failed", "Тест не поймал баг: после входа сайт остался на /login"
        """,
        """
        def test_login_success(page):
            page.goto("/login")
            page.get_by_label("Логин").fill("anna")
            page.get_by_label("Пароль").fill("secret")
            page.get_by_role("button", name="Войти").click()
            expect(page).to_have_url("http://app.test/catalog")
        """),
),

lesson(f"{P}-expect", "Проверки: expect",
    out(f"{P}-expect-e1", "Что выведет программа? Если проверка не прошла за отведённое время, `expect` бросает `AssertionError` с понятным сообщением.", """
        from pwfake.sync_api import Page, expect

        page = Page()
        page.set_content('<button>Войти</button>')
        expect(page.get_by_role("button")).to_have_text("Войти")
        print("первая проверка прошла")
        try:
            expect(page.get_by_role("button")).to_have_text("Выйти", timeout=300)
        except AssertionError as e:
            print(e)
        """),
    out(f"{P}-expect-e2", "Что выведет программа? `to_have_text` сравнивает текст целиком, `to_contain_text` ищет подстроку, `not_to_…` — отрицание.", """
        from pwfake.sync_api import Page, expect

        page = Page()
        page.set_content('''
        <p id="total">Итого: 1800 ₽</p>
        <div class="error" hidden>Ошибка оплаты</div>
        ''')
        total = page.locator("#total")
        expect(total).to_contain_text("1800")
        print("contain ok")
        expect(page.locator(".error")).not_to_be_visible()
        print("hidden ok")
        try:
            expect(total).to_have_text("1800", timeout=0)
        except AssertionError:
            print("to_have_text: нужен весь текст")
        """),
    out(f"{P}-expect-e3", "Что выведет программа? Для набора элементов `to_have_text` принимает список — по тексту на каждый элемент, по порядку.", """
        from pwfake.sync_api import Page, expect

        page = Page()
        page.set_content('<ul><li>Мышь</li><li>Коврик</li></ul>')
        items = page.get_by_role("listitem")
        expect(items).to_have_count(2)
        expect(items).to_have_text(["Мышь", "Коврик"])
        print("порядок верный")
        try:
            expect(items).to_have_text(["Коврик", "Мышь"], timeout=0)
        except AssertionError:
            print("порядок важен")
        """),
    cmd(f"{P}-expect-e4", "Напиши проверку, что кнопка «Оплатить» **недоступна** (disabled). Используй `expect` и поиск по роли.",
        ['expect(page.get_by_role("button", name="Оплатить")).to_be_disabled()',
         r're:expect\(\s*page\.get_by_role\(\s*["\']button["\']\s*,\s*name\s*=\s*["\']Оплатить["\']\s*\)\s*\)\s*\.to_be_disabled\(\s*\)',
         r're:expect\(\s*page\.get_by_role\(\s*["\']button["\']\s*,\s*name\s*=\s*["\']Оплатить["\']\s*\)\s*\)\s*\.not_to_be_enabled\(\s*\)'],
        hint="`expect(локатор).to_be_disabled()`"),
    uit(f"{P}-expect-e5", t("""
        Негативный тест `test_wrong_password(page)`: войди как `anna` с паролем `wrong` и проверь, что появилось сообщение об ошибке с текстом **«Неверный логин или пароль»**.

        Сообщение выводится в блоке `<div class="error" role="alert">…</div>` — найди его по роли `alert`.
        """),
        """
        def test_wrong_password(page):
            page.goto("/login")
            # войди с неверным паролем и проверь сообщение
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_wrong_password") == "passed", res

        def test_catches_bug():
            code, res = run_pytest(patch=bug("login_no_error"))
            assert res.get("test_wrong_password") == "failed", "Тест не поймал баг: при неверном пароле ошибки нет"
        """,
        """
        def test_wrong_password(page):
            page.goto("/login")
            page.get_by_label("Логин").fill("anna")
            page.get_by_label("Пароль").fill("wrong")
            page.get_by_role("button", name="Войти").click()
            expect(page.get_by_role("alert")).to_have_text("Неверный логин или пароль")
        """),
    uit(f"{P}-expect-e6", t("""
        Тест `test_username_in_header(page)`: войди как `anna` / `secret` и проверь, что в шапке показано её имя. Имя выводится так:
        ```html
        <span data-testid="username">anna</span>
        ```
        """),
        """
        def test_username_in_header(page):
            page.goto("/login")
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_username_in_header") == "passed", res

        def test_catches_bug():
            code, res = run_pytest(patch=bug("wrong_username"))
            assert res.get("test_username_in_header") == "failed", "Тест не поймал баг: в шапке имя другого пользователя"
        """,
        """
        def test_username_in_header(page):
            page.goto("/login")
            page.get_by_label("Логин").fill("anna")
            page.get_by_label("Пароль").fill("secret")
            page.get_by_role("button", name="Войти").click()
            expect(page.get_by_test_id("username")).to_have_text("anna")
        """),
    uit(f"{P}-expect-e7", t("""
        Тест `test_search_mouse(page)`: открой `/catalog`, введи в поле «Поиск» слово `мыш` и нажми «Найти». Проверь, что осталась **одна** карточка товара и в ней есть текст «Мышь».

        Карточки: `get_by_test_id("product")`. Не забывай: товары подгружаются с задержкой — используй `expect`.
        """),
        """
        def test_search_mouse(page):
            page.goto("/catalog")
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_search_mouse") == "passed", res

        def test_catches_bug():
            code, res = run_pytest(patch=bug("search_broken"))
            assert res.get("test_search_mouse") == "failed", "Тест не поймал баг: поиск возвращает все товары"
        """,
        """
        def test_search_mouse(page):
            page.goto("/catalog")
            page.get_by_placeholder("Поиск").fill("мыш")
            page.get_by_role("button", name="Найти").click()
            cards = page.get_by_test_id("product")
            expect(cards).to_have_count(1)
            expect(cards).to_contain_text("Мышь")
        """),
    uit(f"{P}-expect-e8", t("""
        Тест `test_out_of_stock(page)`: в каталоге у «Наушников» нет товара — вместо «В корзину» у них кнопка «Нет в наличии». Проверь, что:

        - кнопка «Нет в наличии» недоступна — `to_be_disabled()`;
        - кнопок «В корзину» ровно **4** — `to_have_count(4)`.
        """),
        """
        def test_out_of_stock(page):
            page.goto("/catalog")
        """,
        """
        def test_passes():
            code, res = run_pytest()
            assert res.get("test_out_of_stock") == "passed", res

        def test_checks():
            src = source()
            assert "to_be_disabled" in src, "Проверь недоступность через to_be_disabled()"
            assert "to_have_count(4)" in src.replace(" ", ""), "Проверь число кнопок через to_have_count(4)"
        """,
        """
        def test_out_of_stock(page):
            page.goto("/catalog")
            expect(page.get_by_role("button", name="Нет в наличии")).to_be_disabled()
            expect(page.get_by_role("button", name="В корзину")).to_have_count(4)
        """),
),
)
