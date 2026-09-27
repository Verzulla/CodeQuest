"""Тема «Тестирование UI».

Браузера в песочнице нет — практика на имитациях: страница как список
элементов-словарей, фейковые часы для ожиданий и фейковый драйвер
для Page Object. Концепции и код 1-в-1 переносятся на Selenium/Playwright.
"""
from textwrap import dedent

from ._lib import t, cod, lesson, module, out, topic

P = "ui"

PAGE = '''
PAGE = [
    {"tag": "input", "id": "login", "testid": "login-input", "classes": ["field"], "text": "", "visible": True},
    {"tag": "input", "id": "password", "testid": "password-input", "classes": ["field", "secret"], "text": "", "visible": True},
    {"tag": "button", "id": "submit", "testid": "login-btn", "classes": ["btn", "primary"], "text": "Войти", "visible": True},
    {"tag": "a", "id": "", "testid": "", "classes": ["link"], "text": "Забыли пароль?", "visible": True},
    {"tag": "div", "id": "error", "testid": "error-msg", "classes": ["alert"], "text": "", "visible": False},
    {"tag": "button", "id": "", "testid": "", "classes": ["btn"], "text": "Помощь", "visible": True},
]
'''

CLOCK = '''
class FakeClock:
    """Часы, где sleep() не ждёт по-настоящему, а сдвигает время."""
    def __init__(self):
        self.t = 0.0
        self.sleeps = 0

    def now(self):
        return self.t

    def sleep(self, seconds):
        self.sleeps += 1
        self.t += seconds
'''

DRIVER = '''
class FakeDriver:
    """Имитация браузера со страницей логина.
    fill(selector, text), click(selector), text(selector), url.
    broken: 'no_redirect' — после логина не уходит на /dashboard,
            'no_error'    — при неверном пароле не показывает ошибку,
            'wrong_name'  — приветствует не того пользователя."""
    USERS = {"anna": "qwerty123"}

    def __init__(self, broken=None):
        self.broken = broken
        self.url = "/login"
        self.fields = {"#login": "", "#password": ""}
        self.texts = {"#error": "", "#greeting": ""}
        self.log = []

    def fill(self, selector, text):
        if selector not in self.fields:
            raise LookupError(f"Нет поля {selector}")
        self.fields[selector] = text
        self.log.append(("fill", selector, text))

    def click(self, selector):
        if selector != "#submit":
            raise LookupError(f"Нет кнопки {selector}")
        self.log.append(("click", selector))
        login, pwd = self.fields["#login"], self.fields["#password"]
        if self.USERS.get(login) == pwd:
            if self.broken != "no_redirect":
                self.url = "/dashboard"
            name = "boris" if self.broken == "wrong_name" else login
            self.texts["#greeting"] = f"Привет, {name}!"
        elif self.broken != "no_error":
            self.texts["#error"] = "Неверный логин или пароль"

    def text(self, selector):
        return self.texts.get(selector, "")


def must_fail(test_func, driver, why):
    try:
        test_func(driver)
    except AssertionError:
        return
    assert False, f"Твой тест не поймал баг: {why}"
'''

LOGIN_PAGE = '''
class LoginPage:
    LOGIN = "#login"
    PASSWORD = "#password"
    SUBMIT = "#submit"
    ERROR = "#error"
    GREETING = "#greeting"

    def __init__(self, driver):
        self.driver = driver

    def login(self, user, password):
        self.driver.fill(self.LOGIN, user)
        self.driver.fill(self.PASSWORD, password)
        self.driver.click(self.SUBMIT)

    def error_text(self):
        return self.driver.text(self.ERROR)

    def greeting(self):
        return self.driver.text(self.GREETING)
'''


def with_(*parts):
    """Склеить общие куски (PAGE/CLOCK/DRIVER) и тесты задания."""
    *shared, tests = parts
    return "".join(shared) + dedent(tests)


m1 = module(f"{P}-m1", "Локаторы и ожидания", "🎯", "Как найти элемент и дождаться его",
    lesson(f"{P}-m1-l1", "Локаторы", """
        # Локатор — адрес элемента на странице

        Любой UI-тест начинается с поиска элемента. Способы (от надёжных к хрупким):

        1. **data-testid** — атрибут специально для тестов: `[data-testid="login-btn"]`. Не меняется при редизайне.
        2. **id** — `#submit`. Хорошо, если id стабильные.
        3. **Текст / роль** — `get_by_role("button", name="Войти")` в Playwright. Близко к тому, как видит пользователь.
        4. **CSS-классы** — `.btn.primary`. Часто меняются вместе с дизайном.
        5. **XPath с индексами** — `//div[3]/span[2]`. Ломается от любой правки вёрстки. Избегай!

        ```
        # Selenium
        driver.find_element(By.CSS_SELECTOR, '[data-testid="login-btn"]').click()

        # Playwright
        page.get_by_test_id("login-btn").click()
        page.locator("#login").fill("anna")
        ```

        # В этом уроке

        Страница — это список словарей, у каждого элемента есть `tag`, `id`, `testid`, `classes`, `text`, `visible`.
        Ты пишешь функции поиска — так же работает движок браузера под капотом.
        """,
        out(f"{P}-m1-l1-e1", "Что выведет программа? Собираем CSS-селекторы.", """
            testid = "login-btn"
            print(f'[data-testid="{testid}"]')
            print("#" + "submit")
            print("." + ".".join(["btn", "primary"]))
            """),
        out(f"{P}-m1-l1-e2", "Что выведет программа?", with_(PAGE, """
            buttons = [el["text"] for el in PAGE if el["tag"] == "button"]
            hidden = [el["id"] for el in PAGE if not el["visible"]]
            print(buttons)
            print(hidden)
            """)),
        cod(f"{P}-m1-l1-e3", t("""
            Напиши функцию `find_by_testid(page, testid)` — поиск элемента по атрибуту `data-testid`.

            - Получает:
              - `page` — страницу: список элементов-словарей (он есть в заготовке как `PAGE`; у каждого элемента есть ключи `tag`, `id`, `testid`, `classes`, `text`, `visible`);
              - `testid` — искомое значение.
            - Возвращает: **первый** элемент, у которого `testid` совпадает, или `None`, если такого нет.

            Примеры:
            ```
            find_by_testid(PAGE, "login-btn")   # → словарь кнопки с текстом "Войти"
            find_by_testid(PAGE, "nope")        # → None
            ```
            """),
            with_(PAGE, """
            def find_by_testid(page, testid):
                pass
            """),
            with_(PAGE, """
            def test_found():
                el = find_by_testid(PAGE, "login-btn")
                assert el is not None and el["text"] == "Войти", "Должна найтись кнопка «Войти»"

            def test_not_found():
                assert find_by_testid(PAGE, "nope") is None, "Нет элемента → None"
            """),
            with_(PAGE, """
            def find_by_testid(page, testid):
                for el in page:
                    if el["testid"] == testid:
                        return el
                return None
            """)),
        cod(f"{P}-m1-l1-e4", t("""
            Напиши функцию `find_all_by_class(page, cls)` — поиск всех элементов с CSS-классом.

            - Получает: `page` — список элементов (как `PAGE` в заготовке); `cls` — имя класса.
            - Возвращает: список **текстов** (поле `text`) всех элементов, у которых в списке `classes` есть `cls`, в порядке на странице.

            Примеры для `PAGE` из заготовки:
            ```
            find_all_by_class(PAGE, "btn")    # → ["Войти", "Помощь"]
            find_all_by_class(PAGE, "nope")   # → []
            ```
            """),
            with_(PAGE, """
            def find_all_by_class(page, cls):
                pass
            """),
            with_(PAGE, """
            def test_btn():
                assert find_all_by_class(PAGE, "btn") == ["Войти", "Помощь"], f"Получено {find_all_by_class(PAGE, 'btn')}"

            def test_none():
                assert find_all_by_class(PAGE, "nope") == [], "Нет таких → []"
            """),
            with_(PAGE, """
            def find_all_by_class(page, cls):
                return [el["text"] for el in page if cls in el["classes"]]
            """)),
        cod(f"{P}-m1-l1-e5", t("""
            Напиши функцию `find_by_text(page, text)` — поиск элемента по видимому тексту, как `get_by_text` в Playwright.

            - Получает: `page` — список элементов; `text` — искомый текст.
            - Возвращает: **первый видимый** элемент (`visible` равно `True`), у которого `text` совпадает полностью. Невидимые элементы пропускаются — пользователь их не видит. Если ничего не нашлось — `None`.

            Примеры для `PAGE` из заготовки:
            ```
            find_by_text(PAGE, "Забыли пароль?")   # → элемент-ссылка (tag "a")
            find_by_text(PAGE, "Нет такого")       # → None
            ```
            """),
            with_(PAGE, """
            def find_by_text(page, text):
                pass
            """),
            with_(PAGE, """
            def test_link():
                el = find_by_text(PAGE, "Забыли пароль?")
                assert el is not None and el["tag"] == "a", "Должна найтись ссылка"

            def test_hidden_skipped():
                page = PAGE + [{"tag": "span", "id": "", "testid": "", "classes": [], "text": "Секрет", "visible": False}]
                assert find_by_text(page, "Секрет") is None, "Невидимый элемент не должен находиться"
            """),
            with_(PAGE, """
            def find_by_text(page, text):
                return next((el for el in page if el["visible"] and el["text"] == text), None)
            """)),
        cod(f"{P}-m1-l1-e6", t("""
            Напиши функцию `best_locator(el)`, которая выбирает самый надёжный локатор для элемента.

            - Получает: `el` — элемент-словарь с ключами `tag`, `id`, `testid`, `classes`.
            - Возвращает CSS-селектор строкой, выбирая по приоритету:
              1. если `testid` не пустой → `[data-testid="значение"]`;
              2. иначе если `id` не пустой → `#значение`;
              3. иначе → тег и все классы через точку: `tag.класс1.класс2`.

            Примеры:
            ```
            best_locator({"tag": "button", "id": "submit", "testid": "login-btn", "classes": ["btn"]})
            # → '[data-testid="login-btn"]'

            best_locator({"tag": "button", "id": "submit", "testid": "", "classes": ["btn"]})
            # → "#submit"

            best_locator({"tag": "a", "id": "", "testid": "", "classes": ["link"]})
            # → "a.link"
            ```
            """),
            """
            def best_locator(el):
                pass
            """,
            with_(PAGE, """
            def test_testid():
                assert best_locator(PAGE[2]) == '[data-testid="login-btn"]', f"Получено {best_locator(PAGE[2])!r}"

            def test_id():
                el = dict(PAGE[2], testid="")
                assert best_locator(el) == "#submit", f"Без testid → #submit, получено {best_locator(el)!r}"

            def test_classes():
                assert best_locator(PAGE[5]) == "button.btn", f"Получено {best_locator(PAGE[5])!r}"
                assert best_locator(PAGE[3]) == "a.link", f"Получено {best_locator(PAGE[3])!r}"
            """),
            """
            def best_locator(el):
                if el["testid"]:
                    return f'[data-testid="{el["testid"]}"]'
                if el["id"]:
                    return "#" + el["id"]
                return el["tag"] + "".join("." + c for c in el["classes"])
            """,
            xp=20),
    ),
    lesson(f"{P}-m1-l2", "Ожидания и флаки", """
        # Почему нельзя просто time.sleep(5)

        Страница грузится разное время. `sleep(5)`:
        - если элемент появился за 0.3 с — тест зря ждёт 4.7 с (×1000 тестов = часы);
        - если сервер тормозит 6 с — тест падает, хотя бага нет.

        **Явное ожидание** — опрашивать условие, пока оно не выполнится или не выйдет таймаут:

        ```
        # Selenium
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "error")))

        # Playwright ждёт автоматически
        expect(page.locator("#error")).to_be_visible(timeout=10_000)
        ```

        # Флаки (flaky tests)

        **Флаки-тест** то проходит, то падает на одном и том же коде. Частые причины: нет ожиданий, зависимость от порядка тестов, общие тестовые данные, анимации.
        Перезапуск (retry) — временная мера, причину нужно искать.

        # В этом уроке

        Настоящее время ждать долго, поэтому используем `FakeClock`: `clock.now()` — текущее время, `clock.sleep(s)` — мгновенно сдвигает время на `s` секунд.
        """,
        out(f"{P}-m1-l2-e1", "Что выведет программа? Имитация опроса условия.", with_(CLOCK, """
            clock = FakeClock()
            ready_at = 1.2
            while clock.now() < ready_at:
                clock.sleep(0.5)
            print(clock.now(), clock.sleeps)
            """), hint="Опрос каждые 0.5 с: 0 → 0.5 → 1.0 → 1.5."),
        cod(f"{P}-m1-l2-e2", t("""
            Напиши функцию `wait_until(condition, timeout, clock, poll=0.5)` — явное ожидание, как `WebDriverWait` в Selenium.

            - Получает:
              - `condition` — функцию без аргументов, возвращает `True`/`False` (например, «элемент появился?»);
              - `timeout` — сколько секунд максимум ждать;
              - `clock` — часы: `clock.now()` возвращает текущее время в секундах, `clock.sleep(s)` ждёт `s` секунд;
              - `poll` — как часто проверять условие.
            - Алгоритм:
              1. запомни время старта;
              2. проверь `condition()` — если истина, **сразу** верни `True`;
              3. если с момента старта прошло `timeout` секунд или больше — брось `TimeoutError`;
              4. иначе поспи `clock.sleep(poll)` и вернись к шагу 2.

            Примеры:
            - условие стало истинным на 2-й секунде, `timeout=10` → вернёт `True` примерно на 2-й секунде;
            - условие истинно сразу → вернёт `True`, ни разу не вызвав `sleep`;
            - условие никогда не выполняется, `timeout=3` → `TimeoutError` на 3-й секунде.

            Используй только `clock` — настоящий `time.sleep` не нужен.
            """),
            """
            def wait_until(condition, timeout, clock, poll=0.5):
                pass
            """,
            with_(CLOCK, """
            def test_becomes_true():
                clock = FakeClock()
                assert wait_until(lambda: clock.now() >= 2, timeout=10, clock=clock) is True, "Условие стало истинным на 2-й секунде"
                assert clock.now() < 3, f"Ждать после выполнения условия не нужно (время {clock.now()})"

            def test_immediately():
                clock = FakeClock()
                wait_until(lambda: True, timeout=5, clock=clock)
                assert clock.sleeps == 0, "Если условие сразу истинно — не спать"

            def test_timeout():
                clock = FakeClock()
                try:
                    wait_until(lambda: False, timeout=3, clock=clock)
                except TimeoutError:
                    assert 3 <= clock.now() <= 3.5, f"Сдаваться нужно сразу после таймаута (время {clock.now()})"
                    return
                assert False, "Нужен TimeoutError"
            """),
            """
            def wait_until(condition, timeout, clock, poll=0.5):
                start = clock.now()
                while True:
                    if condition():
                        return True
                    if clock.now() - start >= timeout:
                        raise TimeoutError(f"Условие не выполнилось за {timeout} с")
                    clock.sleep(poll)
            """,
            hint="Запомни `start = clock.now()`. В бесконечном цикле: проверь условие → проверь таймаут → поспи.", xp=25),
        cod(f"{P}-m1-l2-e3", t("""
            Напиши функцию `is_flaky(history)`, которая определяет нестабильный (флаки) тест.

            - Получает: `history` — список результатов нескольких прогонов **одного и того же** теста на **одном и том же** коде: строки `"pass"` и `"fail"`.
            - Возвращает: `True`, если тест флаки — в истории встречается **и** `"pass"`, **и** `"fail"`. Если результат всегда одинаковый — `False`.

            Примеры:
            ```
            is_flaky(["pass", "fail", "pass"])   # → True
            is_flaky(["pass", "pass", "pass"])   # → False   стабильно проходит
            is_flaky(["fail", "fail"])           # → False   стабильно падает — это баг, а не флаки
            ```
            """),
            """
            def is_flaky(history):
                pass
            """,
            """
            def test_flaky():
                assert is_flaky(["pass", "fail", "pass"]) is True, "Есть и pass, и fail → флаки"

            def test_stable():
                assert is_flaky(["pass"] * 5) is False and is_flaky(["fail", "fail"]) is False, "Стабильный результат — не флаки"
            """,
            """
            def is_flaky(history):
                return "pass" in history and "fail" in history
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
    ),
)

m2 = module(f"{P}-m2", "Page Object и стратегия", "📄", "Поддерживаемые тесты и здравая автоматизация",
    lesson(f"{P}-m2-l1", "Page Object", """
        # Паттерн Page Object

        Без него селекторы размазаны по всем тестам. Поменяли id кнопки — правим 50 тестов.
        **Page Object** — класс, который знает всё о странице: где элементы и какие на ней действия.

        ```
        class LoginPage:
            LOGIN = "#login"
            PASSWORD = "#password"
            SUBMIT = "#submit"

            def __init__(self, page):
                self.page = page

            def login(self, user, password):
                self.page.fill(self.LOGIN, user)
                self.page.fill(self.PASSWORD, password)
                self.page.click(self.SUBMIT)


        def test_login(page):
            LoginPage(page).login("anna", "qwerty123")
            assert page.url.endswith("/dashboard")
        ```

        Тест читается как сценарий пользователя, а селекторы живут в одном месте.

        # В этом уроке

        `driver` — фейковый браузер с формой логина:
        - `driver.fill(selector, text)`, `driver.click(selector)`, `driver.text(selector)`, `driver.url`
        - поля `#login`, `#password`, кнопка `#submit`; после входа — `#greeting`, при ошибке — `#error`
        - существует пользователь `anna` с паролем `qwerty123`
        """,
        cod(f"{P}-m2-l1-e1", t("""
            Допиши Page Object для страницы логина — класс `LoginPage`.

            Селекторы уже объявлены константами класса (`LOGIN`, `PASSWORD`, `SUBMIT`, `ERROR`), драйвер браузера сохраняется в `self.driver`. Допиши два метода:

            1. `login(user, password)`:
               - заполнить поле логина: `self.driver.fill(self.LOGIN, user)`;
               - заполнить поле пароля;
               - нажать кнопку: `self.driver.click(self.SUBMIT)`.
            2. `error_text()` — вернуть текст сообщения об ошибке: `self.driver.text(self.ERROR)`.

            Используй константы класса, а не строки `"#login"` напрямую — в этом и смысл Page Object.

            Проверка: после `login("anna", "qwerty123")` браузер должен уйти на `/dashboard`, а после неверного пароля `error_text()` вернёт `"Неверный логин или пароль"`.
            """),
            """
            class LoginPage:
                LOGIN = "#login"
                PASSWORD = "#password"
                SUBMIT = "#submit"
                ERROR = "#error"

                def __init__(self, driver):
                    self.driver = driver

                def login(self, user, password):
                    pass

                def error_text(self):
                    pass
            """,
            with_(DRIVER, """
            def test_login_works():
                d = FakeDriver()
                LoginPage(d).login("anna", "qwerty123")
                assert d.url == "/dashboard", f"После login url должен быть /dashboard, а он {d.url}"

            def test_uses_fields():
                d = FakeDriver()
                LoginPage(d).login("anna", "x")
                assert ("fill", "#login", "anna") in d.log and ("click", "#submit") in d.log, "login должен заполнить поля и нажать кнопку"

            def test_error_text():
                d = FakeDriver()
                page = LoginPage(d)
                page.login("anna", "неверный")
                assert page.error_text() == "Неверный логин или пароль", f"error_text вернул {page.error_text()!r}"
            """),
            """
            class LoginPage:
                LOGIN = "#login"
                PASSWORD = "#password"
                SUBMIT = "#submit"
                ERROR = "#error"

                def __init__(self, driver):
                    self.driver = driver

                def login(self, user, password):
                    self.driver.fill(self.LOGIN, user)
                    self.driver.fill(self.PASSWORD, password)
                    self.driver.click(self.SUBMIT)

                def error_text(self):
                    return self.driver.text(self.ERROR)
            """),
        cod(f"{P}-m2-l1-e2", t("""
            Напиши UI-тест `test_successful_login(driver)` — успешный вход.

            Page Object `LoginPage` уже готов в заготовке (методы `login`, `error_text`, `greeting`).

            Шаги теста:
            1. Создай страницу: `page = LoginPage(driver)` (уже написано).
            2. Войди как пользователь `anna` с паролем `qwerty123`.
            3. Проверь, что адрес страницы `driver.url` стал `"/dashboard"`.
            4. Проверь, что приветствие `page.greeting()` равно `"Привет, anna!"`.

            Тест должен падать на сломанных версиях приложения: где после входа нет перехода и где приветствуется не тот пользователь.
            """),
            with_(LOGIN_PAGE, """

            def test_successful_login(driver):
                page = LoginPage(driver)
                # допиши сценарий и проверки
            """),
            with_(DRIVER, """
            def test_zz_passes():
                test_successful_login(FakeDriver())

            def test_zz_catches_no_redirect():
                must_fail(test_successful_login, FakeDriver("no_redirect"), "после входа не произошёл переход на /dashboard")

            def test_zz_catches_wrong_name():
                must_fail(test_successful_login, FakeDriver("wrong_name"), "приветствие не того пользователя")
            """),
            with_(LOGIN_PAGE, """

            def test_successful_login(driver):
                page = LoginPage(driver)
                page.login("anna", "qwerty123")
                assert driver.url == "/dashboard"
                assert page.greeting() == "Привет, anna!"
            """)),
        cod(f"{P}-m2-l1-e3", t("""
            Напиши **негативный** UI-тест `test_wrong_password(driver)` — вход с неверным паролем.

            Шаги:
            1. Создай `LoginPage(driver)` и войди как `anna` с **неправильным** паролем (любым, кроме `qwerty123`).
            2. Проверь, что `error_text()` равен `"Неверный логин или пароль"`.
            3. Проверь, что пользователь остался на странице входа: `driver.url == "/login"`.

            Тест должен падать на версии приложения, которая при неверном пароле не показывает ошибку.
            """),
            with_(LOGIN_PAGE, """

            def test_wrong_password(driver):
                pass
            """),
            with_(DRIVER, """
            def test_zz_passes():
                test_wrong_password(FakeDriver())

            def test_zz_catches_no_error():
                must_fail(test_wrong_password, FakeDriver("no_error"), "при неверном пароле не показана ошибка")
            """),
            with_(LOGIN_PAGE, """

            def test_wrong_password(driver):
                page = LoginPage(driver)
                page.login("anna", "неверный")
                assert page.error_text() == "Неверный логин или пароль"
                assert driver.url == "/login"
            """),
            xp=20),
        cod(f"{P}-m2-l1-e4", t("""
            Напиши UI-тест `test_empty_fields(driver)` — попытка входа с пустой формой.

            Шаги:
            1. Создай `LoginPage(driver)` и вызови `login("", "")` — как будто пользователь нажал «Войти», ничего не заполнив.
            2. Проверь, что сообщение об ошибке **не пустое** (`error_text()` не равен `""`).
            3. Проверь, что перехода не произошло: `driver.url == "/login"`.

            Тест должен падать на версии приложения, где пустая форма не показывает ошибку.
            """),
            with_(LOGIN_PAGE, """

            def test_empty_fields(driver):
                pass
            """),
            with_(DRIVER, """
            def test_zz_passes():
                test_empty_fields(FakeDriver())

            def test_zz_catches_no_error():
                must_fail(test_empty_fields, FakeDriver("no_error"), "пустая форма не показала ошибку")
            """),
            with_(LOGIN_PAGE, """

            def test_empty_fields(driver):
                page = LoginPage(driver)
                page.login("", "")
                assert page.error_text() != ""
                assert driver.url == "/login"
            """)),
    ),
    lesson(f"{P}-m2-l2", "Стратегия UI-автоматизации", """
        # Пирамида тестирования

        ```
               /\\        UI (E2E) — мало: медленные и хрупкие
              /  \\
             /API \\      API / интеграционные — больше
            /------\\
           /  Unit  \\    Модульные — больше всего: быстрые и стабильные
        ```

        UI-тестами проверяют **ключевые пользовательские сценарии** (логин, оплата, оформление заказа), а не каждую валидацию поля — её дешевле проверить на уровне API.

        # Хорошие практики

        - **Независимость**: каждый тест сам готовит данные и не зависит от порядка.
        - **Скриншот и логи при падении** — без них разбирать упавший тест в CI мучительно.
        - **Параллельный запуск** на нескольких воркерах (`pytest -n 4` с pytest-xdist).
        - **Кроссбраузерность** — матрица браузеров и размеров экрана.
        - **Отчёты** — Allure / pytest-html: что упало, скриншоты, шаги.
        """,
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
    ),
)

TOPIC = topic("ui-testing", "Тестирование UI", "🖥️", "#e05ab0",
              "Локаторы, ожидания, флаки, Page Object и стратегия автоматизации", m1, m2, group="Тестирование и DevOps")
