"""Подробная теория и «Проверь себя» для темы «Тестирование UI»."""
from ._lib import t

THEORY = {
"ui-m1-l1": {"full": t("""
    ## Зачем это нужно

    Любой UI-тест — это «найди элемент и сделай с ним что-то». Если элемент ищется ненадёжно, тест начинает падать после каждого редизайна, хотя функциональность не сломана. Умение выбирать **устойчивые локаторы** — главный навык, отличающий хрупкие UI-тесты от надёжных.

    ## Как это работает

    Локатор — это правило поиска элемента в DOM (дереве HTML-страницы).

    ```html
    <form id="login-form">
      <input id="login" class="field" data-testid="login-input">
      <input id="password" class="field secret" type="password">
      <button id="submit" class="btn primary" data-testid="login-btn">Войти</button>
    </form>
    ```

    ### Виды локаторов — от надёжных к хрупким

    1. **`data-testid`** — атрибут, который разработчики добавляют специально для тестов: `[data-testid="login-btn"]`. Не зависит от дизайна и текстов. Лучший выбор, если команда договорилась его использовать.
    2. **Роль и доступное имя** — `get_by_role("button", name="Войти")` в Playwright. Ищет так, как видит пользователь (и скринридер) — заодно проверяет доступность.
    3. **`id`** — `#submit`. Хорошо, если id стабильные, а не сгенерированные (`#ember-1234` — плохо).
    4. **Текст** — `get_by_text("Войти")`. Удобно, но ломается при смене формулировки или языка.
    5. **CSS-классы** — `.btn.primary`. Классы часто меняются при редизайне.
    6. **XPath с индексами** — `//div[3]/form/button[2]`. Ломается от любой правки вёрстки. Избегай.

    ### CSS-селекторы — минимум

    - `#id`, `.class`, `tag`, `[attr="value"]`;
    - комбинации: `button.primary`, `form#login button`;
    - `>` — прямой потомок, пробел — любой потомок.

    ### Код в реальных фреймворках

    ```py
    # Selenium
    driver.find_element(By.CSS_SELECTOR, '[data-testid="login-btn"]').click()
    driver.find_element(By.ID, "login").send_keys("anna")

    # Playwright
    page.get_by_test_id("login-btn").click()
    page.get_by_role("button", name="Войти").click()
    page.locator("#login").fill("anna")
    ```

    ## Примеры

    Упрощённая модель: страница — список элементов-словарей. Так работает движок поиска внутри браузера, только на настоящем DOM.

    ### Пример 1. Поиск по разным признакам

    ```python
    PAGE = [
        {"tag": "input", "id": "login", "testid": "login-input", "classes": ["field"], "text": "", "visible": True},
        {"tag": "button", "id": "submit", "testid": "login-btn", "classes": ["btn", "primary"], "text": "Войти", "visible": True},
        {"tag": "a", "id": "", "testid": "", "classes": ["link"], "text": "Забыли пароль?", "visible": True},
        {"tag": "div", "id": "error", "testid": "error-msg", "classes": ["alert"], "text": "", "visible": False},
        {"tag": "button", "id": "", "testid": "", "classes": ["btn"], "text": "Помощь", "visible": True},
    ]

    by_testid = next(el for el in PAGE if el["testid"] == "login-btn")
    by_class = [el["text"] for el in PAGE if "btn" in el["classes"]]
    visible_buttons = [el["text"] for el in PAGE if el["tag"] == "button" and el["visible"]]
    print(by_testid["text"], by_class, visible_buttons)
    ```

    ### Пример 2. Лучший локатор для элемента

    ```python
    def best_locator(el):
        if el["testid"]:
            return f'[data-testid="{el["testid"]}"]'
        if el["id"]:
            return "#" + el["id"]
        return el["tag"] + "".join("." + c for c in el["classes"])

    elements = [
        {"tag": "button", "id": "submit", "testid": "login-btn", "classes": ["btn"]},
        {"tag": "button", "id": "submit", "testid": "", "classes": ["btn"]},
        {"tag": "a", "id": "", "testid": "", "classes": ["link", "muted"]},
    ]
    for el in elements:
        print(best_locator(el))
    ```

    ### Пример 3. Почему текст — хрупкий локатор

    ```python
    page_v1 = [{"text": "Войти"}, {"text": "Регистрация"}]
    page_v2 = [{"text": "Вход"}, {"text": "Регистрация"}]     # дизайнер поменял надпись

    for version, page in [("v1", page_v1), ("v2", page_v2)]:
        found = any(el["text"] == "Войти" for el in page)
        print(version, "кнопка найдена" if found else "ТЕСТ УПАЛ — хотя функциональность цела")
    ```

    ## Частые ошибки

    **Длинные XPath из DevTools** («Copy XPath») — `/html/body/div[2]/div/div[3]/button`. Ломаются от любой правки.

    **Поиск невидимого элемента.** Элемент есть в DOM, но скрыт — клик по нему упадёт. Playwright по умолчанию требует видимость, Selenium — нет.

    **Несколько совпадений.** Селектор `.btn` находит все кнопки; тест кликнет не туда. Локатор должен быть **уникальным**.

    ## Шпаргалка

    ```text
    [data-testid="x"]   — лучший вариант
    role + name          — как видит пользователь
    #id                  — если стабильный
    text                 — осторожно, меняется
    .class               — хрупко
    XPath с индексами    — избегать
    ```
    """), "quiz": [
    {"q": "Какой локатор самый устойчивый к редизайну?",
     "options": ["`//div[3]/button[2]`", "`.btn.btn-primary.mt-2`", "`[data-testid=\"login-btn\"]`", "Текст «Войти»"], "answer": 2,
     "explain": "`data-testid` существует специально для тестов и не зависит от вёрстки, стилей и формулировок."},
    {"q": "Почему локатор должен быть уникальным?",
     "options": ["Так быстрее работает браузер", "Иначе тест может взаимодействовать не с тем элементом", "Это требование HTML", "Не обязательно"], "answer": 1,
     "explain": "Если селектор находит несколько элементов, тест возьмёт первый — не факт, что нужный. Такие тесты ведут себя непредсказуемо."},
    {"q": "Какой CSS-селектор найдёт `<button id=\"submit\">`?",
     "options": ["`.submit`", "`#submit`", "`submit`", "`[submit]`"], "answer": 1,
     "explain": "`#` — поиск по id, `.` — по классу, без символа — по тегу."},
]},

"ui-m1-l2": {"full": t("""
    ## Зачем это нужно

    Веб-страница живёт асинхронно: данные подгружаются с сервера, кнопки появляются после анимации, ошибки валидации — после ответа API. Если тест пытается нажать кнопку, которой ещё нет, он падает. Если «лечить» это паузами `sleep`, тесты становятся медленными **и** всё равно нестабильными. Правильные ожидания — основа надёжных UI-тестов.

    ## Как это работает

    ### Почему sleep — плохо

    `time.sleep(5)`:
    - элемент появился за 0.3 с → тест зря ждёт 4.7 с; на 1000 тестов — больше часа;
    - сервер тормозит 6 с → тест падает, хотя бага нет.

    ### Явное ожидание (explicit wait)

    Опрашивать условие с небольшим интервалом, пока оно не выполнится или не истечёт таймаут:

    1. проверить условие → выполнено? вернуть успех **сразу**;
    2. таймаут истёк? → упасть с понятной ошибкой;
    3. подождать `poll` и повторить.

    ```py
    # Selenium
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "error")))

    # Playwright: ожидания встроены в действия и expect
    page.get_by_test_id("login-btn").click()          # сам дождётся видимости и кликабельности
    expect(page.locator("#error")).to_have_text("Неверный пароль", timeout=10_000)
    ```

    ### Флаки-тесты

    **Флаки** (flaky) — тест, который на одном и том же коде то проходит, то падает. Частые причины:
    - нет ожиданий или они неправильные;
    - тесты зависят от порядка запуска или общих данных;
    - анимации, случайные данные, время («сегодня», часовые пояса);
    - нестабильное окружение.

    Перезапуск упавших тестов (`pytest --reruns 2`) — временный пластырь: он скрывает симптом, но причину нужно найти и исправить. Флаки опасны тем, что команда перестаёт доверять красным тестам.

    ## Примеры

    Настоящее время ждать долго, поэтому используем «фейковые часы»: `sleep` мгновенно сдвигает время.

    ### Пример 1. Явное ожидание

    ```python
    class FakeClock:
        def __init__(self):
            self.t = 0.0
        def now(self):
            return self.t
        def sleep(self, s):
            self.t += s

    def wait_until(condition, timeout, clock, poll=0.5):
        start = clock.now()
        while True:
            if condition():
                return True
            if clock.now() - start >= timeout:
                raise TimeoutError(f"условие не выполнилось за {timeout} с")
            clock.sleep(poll)

    clock = FakeClock()
    wait_until(lambda: clock.now() >= 1.3, timeout=10, clock=clock)
    print(f"элемент появился, ждали {clock.now()} с вместо фиксированных 5")

    clock = FakeClock()
    try:
        wait_until(lambda: False, timeout=3, clock=clock)
    except TimeoutError as e:
        print("упали через", clock.now(), "с:", e)
    ```

    ### Пример 2. Сколько теряет sleep

    ```python
    load_times = [0.3, 0.4, 1.2, 0.2, 6.1, 0.5]    # реальное время появления элемента
    SLEEP = 5
    fixed = sum(SLEEP for _ in load_times)
    smart = sum(min(t, 10) for t in load_times)     # явное ожидание с таймаутом 10
    failed_with_sleep = sum(1 for t in load_times if t > SLEEP)
    print(f"sleep: {fixed} с и {failed_with_sleep} ложное падение")
    print(f"явное ожидание: {smart:.1f} с и 0 ложных падений")
    ```

    ### Пример 3. Поиск флаки по истории прогонов

    ```python
    runs = {
        "test_login":  ["pass", "pass", "pass"],
        "test_search": ["pass", "fail", "pass"],
        "test_cart":   ["fail", "pass", "pass"],
        "test_pay":    ["fail", "fail", "fail"],
    }
    for name, history in runs.items():
        if "pass" in history and "fail" in history:
            verdict = "ФЛАКИ — найти причину"
        elif "fail" in history:
            verdict = "стабильно падает — вероятно, баг"
        else:
            verdict = "стабилен"
        print(f"{name:12} {verdict}")
    ```

    ### Пример 4. Retry маскирует проблему

    ```python
    import random
    random.seed(7)

    def flaky_test():
        assert random.random() > 0.4, "элемент не успел появиться"

    for attempt in range(1, 4):
        try:
            flaky_test()
            print(f"прошёл с попытки {attempt} — отчёт зелёный, но проблема осталась")
            break
        except AssertionError as e:
            print(f"попытка {attempt}: {e}")
    ```

    ## Частые ошибки

    **`sleep` «на всякий случай».** Замедляет прогон и не гарантирует стабильность.

    **Слишком маленький таймаут** на медленных стендах CI — ложные падения.

    **Ожидание не того условия.** Элемент уже в DOM, но ещё невидим или перекрыт спиннером — ждать нужно видимости/кликабельности.

    ## Шпаргалка

    ```text
    ✗ time.sleep(5)
    ✓ WebDriverWait(driver, 10).until(условие)       # Selenium
    ✓ expect(locator).to_be_visible(timeout=10000)   # Playwright
    Флаки = один код, разные результаты → искать причину, а не только перезапускать
    ```
    """), "quiz": [
    {"q": "Чем явное ожидание лучше `time.sleep(5)`?",
     "options": ["Ничем", "Продолжает сразу, как только условие выполнено, и ждёт до таймаута, если нужно", "Оно всегда ждёт дольше", "Оно отключает анимации"], "answer": 1,
     "explain": "Явное ожидание не тратит лишнее время на быстрых загрузках и не падает на медленных в пределах таймаута."},
    {"q": "Тест на одном и том же коде прошёл 3 раза и упал 1 раз. Как это называется?",
     "options": ["Регрессия", "Флаки-тест", "Смоук-тест", "Негативный тест"], "answer": 1,
     "explain": "Нестабильный результат без изменения кода — признак флаки-теста."},
    {"q": "Почему автоматический перезапуск упавших тестов — только временная мера?",
     "options": ["Он замедляет прогон", "Он скрывает симптом нестабильности, но не устраняет её причину", "Он запрещён в CI", "Он удаляет отчёты"], "answer": 1,
     "explain": "Retry делает отчёт зелёным, а проблема — в тесте или продукте — остаётся и может маскировать реальный баг."},
]},

"ui-m2-l1": {"full": t("""
    ## Зачем это нужно

    Представь 50 тестов, в каждом из которых написано `driver.find_element(By.ID, "login")`. Разработчик переименовал поле — нужно править 50 мест. **Page Object** собирает всё знание о странице в один класс: где элементы и какие действия на ней возможны. Тесты становятся короче, читаются как сценарии пользователя, а правки вёрстки чинятся в одном месте.

    ## Как это работает

    ```py
    class LoginPage:
        LOGIN = "#login"               # локаторы — константы класса
        PASSWORD = "#password"
        SUBMIT = "#submit"
        ERROR = "#error"

        def __init__(self, page):
            self.page = page           # драйвер / страница Playwright

        def open(self):
            self.page.goto("/login")
            return self

        def login(self, user, password):        # действие пользователя
            self.page.fill(self.LOGIN, user)
            self.page.fill(self.PASSWORD, password)
            self.page.click(self.SUBMIT)

        def error_text(self):                    # чтение состояния
            return self.page.text_content(self.ERROR)
    ```

    Тест:

    ```py
    def test_wrong_password(page):
        login_page = LoginPage(page).open()
        login_page.login("anna", "wrong")
        assert login_page.error_text() == "Неверный логин или пароль"
    ```

    ### Правила хорошего Page Object

    - **Локаторы — только внутри** Page Object, в тестах их нет.
    - **Методы — действия пользователя** (`login`, `add_to_cart`), а не «кликни по кнопке №3».
    - **Проверки (`assert`) — в тестах**, а Page Object только возвращает состояние. Так один Page Object служит и позитивным, и негативным тестам.
    - Метод, который переводит на другую страницу, может возвращать её Page Object: `login()` → `DashboardPage`.

    ## Примеры

    ### Пример 1. Фейковый браузер и Page Object

    ```python
    class FakeDriver:
        USERS = {"anna": "qwerty123"}
        def __init__(self):
            self.url = "/login"
            self.fields = {"#login": "", "#password": ""}
            self.texts = {"#error": "", "#greeting": ""}
        def fill(self, sel, text):
            self.fields[sel] = text
        def click(self, sel):
            user, pwd = self.fields["#login"], self.fields["#password"]
            if self.USERS.get(user) == pwd:
                self.url = "/dashboard"
                self.texts["#greeting"] = f"Привет, {user}!"
            else:
                self.texts["#error"] = "Неверный логин или пароль"
        def text(self, sel):
            return self.texts.get(sel, "")

    class LoginPage:
        LOGIN, PASSWORD, SUBMIT, ERROR, GREETING = "#login", "#password", "#submit", "#error", "#greeting"
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

    def test_successful_login(driver):
        page = LoginPage(driver)
        page.login("anna", "qwerty123")
        assert driver.url == "/dashboard"
        assert page.greeting() == "Привет, anna!"

    def test_wrong_password(driver):
        page = LoginPage(driver)
        page.login("anna", "nope")
        assert page.error_text() == "Неверный логин или пароль"
        assert driver.url == "/login"

    for test in [test_successful_login, test_wrong_password]:
        test(FakeDriver())
        print("✅", test.__name__)
    ```

    ### Пример 2. Переход между страницами

    ```python
    class Driver:
        def __init__(self):
            self.url = "/login"

    class DashboardPage:
        def __init__(self, driver):
            self.driver = driver
        def is_open(self):
            return self.driver.url == "/dashboard"

    class LoginPage:
        def __init__(self, driver):
            self.driver = driver
        def login_as(self, user):
            self.driver.url = "/dashboard"       # в реальности: fill + click
            return DashboardPage(self.driver)    # возвращаем следующую страницу

    dashboard = LoginPage(Driver()).login_as("anna")
    print(type(dashboard).__name__, dashboard.is_open())
    ```

    ## Частые ошибки

    **Локаторы в тестах.** Смысл паттерна теряется.

    **`assert` внутри Page Object** («`login()` проверяет, что вход успешен») — тогда этим методом нельзя написать негативный тест.

    **«Божественный» Page Object** на всё приложение. Один класс — одна страница или один компонент (шапка, модальное окно).

    ## Шпаргалка

    ```py
    class SomePage:
        BUTTON = '[data-testid="x"]'     # локаторы здесь
        def __init__(self, page): self.page = page
        def do_action(self): ...         # действия пользователя
        def get_state(self): return ...  # чтение состояния, без assert

    def test_scenario(page):
        p = SomePage(page)
        p.do_action()
        assert p.get_state() == ...      # проверки в тесте
    ```
    """), "quiz": [
    {"q": "Где должны находиться локаторы при использовании Page Object?",
     "options": ["В каждом тесте", "Внутри классов Page Object", "В конфигурации CI", "В отдельной базе данных"], "answer": 1,
     "explain": "Page Object инкапсулирует знание о странице: при изменении вёрстки правится одно место."},
    {"q": "Почему `assert` лучше писать в тестах, а не в методах Page Object?",
     "options": ["Так требует pytest", "Чтобы один и тот же Page Object использовался и в позитивных, и в негативных сценариях", "`assert` не работает в классах", "Это быстрее"], "answer": 1,
     "explain": "Если `login()` сам проверяет успех, им нельзя проверить сценарий с неверным паролем."},
    {"q": "Какое имя метода лучше для Page Object страницы корзины?",
     "options": ["`click_button_3()`", "`checkout()`", "`find_element_by_xpath()`", "`test_cart()`"], "answer": 1,
     "explain": "Методы описывают действия пользователя, а не технические детали вёрстки."},
]},

"ui-m2-l2": {"full": t("""
    ## Зачем это нужно

    UI-тесты — самые дорогие: медленные, хрупкие, сложные в поддержке. Если автоматизировать всё через UI, прогон займёт часы, а половина времени уйдёт на починку тестов. Стратегия отвечает на вопросы: **что** автоматизировать через UI, а что — на уровне API и модульных тестов, и как организовать прогон, чтобы он был быстрым и информативным.

    ## Как это работает

    ### Пирамида тестирования

    ```text
            /\\        UI / E2E — мало (5–10%): ключевые сценарии пользователя
           /  \\
          / API \\     API / интеграционные — больше (20–30%)
         /------\\
        /  Unit  \\    Модульные — больше всего (60–70%): быстрые и стабильные
    ```

    Перевёрнутая пирамида («рожок мороженого») — много UI-тестов и мало модульных — признак проблем: долгие прогоны, частые флаки, дорогая поддержка.

    ### Что проверять через UI

    ✅ Ключевые сквозные сценарии: регистрация, логин, поиск, оформление заказа, оплата.
    ✅ То, что видно только в браузере: вёрстка критичных элементов, взаимодействие компонентов.

    ❌ Каждую валидацию поля, все комбинации данных, бизнес-логику расчётов — дешевле и надёжнее на уровне API.

    ### Практики

    - **Независимость**: каждый тест сам готовит данные (лучше через API — быстрее) и не зависит от других.
    - **Скриншот, видео, логи при падении** — без них разбор упавшего в CI теста превращается в гадание.
    - **Параллельный запуск**: `pytest -n 4` (плагин pytest-xdist) делит тесты между процессами.
    - **Кроссбраузерность**: матрица браузеров и разрешений.
    - **Отчёты**: Allure или pytest-html — шаги, скриншоты, история прогонов.

    ```py
    # conftest.py — скриншот при падении (Playwright + pytest)
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(item, call):
        outcome = yield
        report = outcome.get_result()
        if report.when == "call" and report.failed and "page" in item.funcargs:
            item.funcargs["page"].screenshot(path=f"screenshots/{item.name}.png")
    ```

    ## Примеры

    ### Пример 1. Проверка формы пирамиды

    ```python
    def pyramid_report(unit, api, ui):
        total = unit + api + ui
        shares = {k: round(100 * v / total) for k, v in {"unit": unit, "api": api, "ui": ui}.items()}
        ok = unit > api > ui
        return shares, "пирамида ✅" if ok else "рожок мороженого ⚠️"

    print(pyramid_report(700, 250, 50))
    print(pyramid_report(40, 60, 300))
    ```

    ### Пример 2. Имя файла скриншота

    ```python
    import re

    def screenshot_name(test_name, browser):
        clean = re.sub(r"[^\\w]", "", test_name.lower().replace(" ", "_"))
        return f"{browser}_{clean}.png"

    print(screenshot_name("Login Works", "chrome"))
    print(screenshot_name("Pay: 100$ OK!", "firefox"))
    ```

    ### Пример 3. Распределение по воркерам

    ```python
    tests = [f"test_{i}" for i in range(1, 11)]
    workers = 3
    buckets = [tests[i::workers] for i in range(workers)]
    for i, b in enumerate(buckets, start=1):
        print(f"воркер {i}: {b}")
    print("время прогона ~", max(len(b) for b in buckets), "тестов вместо", len(tests))
    ```

    ### Пример 4. Сводка прогона

    ```python
    from collections import Counter

    results = ["passed", "failed", "passed", "skipped", "passed", "passed", "failed"]
    c = Counter(results)
    run = c["passed"] + c["failed"]
    print(dict(c))
    print(f"pass rate: {round(100 * c['passed'] / run)}% из {run} запущенных")
    ```

    ## Частые ошибки

    **Автоматизировать всё через UI.** Особенно валидации и расчёты — их место на уровне API.

    **Тесты, зависящие от порядка** — не запускаются параллельно и падают по одному.

    **Нет артефактов при падении** — «упало в CI, у меня не воспроизводится».

    ## Шпаргалка

    ```text
    Пирамида: unit > api > ui
    UI — только ключевые пользовательские сценарии
    Данные для UI-тестов готовить через API
    При падении: скриншот + видео + логи + trace
    Параллель: pytest -n auto  ·  Отчёт: Allure
    ```
    """), "quiz": [
    {"q": "Какое соотношение тестов соответствует пирамиде тестирования?",
     "options": ["UI > API > Unit", "Unit > API > UI", "Поровну", "API > UI > Unit"], "answer": 1,
     "explain": "Модульных тестов больше всего (быстрые и дешёвые), UI — меньше всего (медленные и хрупкие)."},
    {"q": "Где лучше проверять все комбинации валидации поля «email»?",
     "options": ["Через UI для каждой комбинации", "На уровне API или модульных тестов", "Только вручную", "Не проверять"], "answer": 1,
     "explain": "Логика валидации одинакова для любого клиента, а проверять её на уровне API в десятки раз быстрее и стабильнее."},
    {"q": "Зачем сохранять скриншот при падении UI-теста?",
     "options": ["Для красоты отчёта", "Чтобы понять, что было на экране в момент падения, особенно в CI", "Это ускоряет тесты", "Чтобы тест прошёл"], "answer": 1,
     "explain": "В CI браузер не видно. Скриншот (а лучше видео и трасса) — главный артефакт для разбора падения."},
]},
}
