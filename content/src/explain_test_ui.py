"""Тема «UI-тестирование (Playwright)» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py).
Строка `pytest.main(...)` в конце решений — только для кнопки «▶ Запустить», её не разбираем."""
from ._lib import x

P = "ui"

EXPLAIN = {

# ===== Модуль 1. Playwright: первые шаги =====

f"{P}-m1-l1-e1": x(
    idea="`get_by_role` ищет элементы так, как их видит пользователь: кнопка, ссылка, заголовок. `name` уточняет по тексту.",
    lines=[
        ('print(page.get_by_role("button").count())', "Две кнопки."),
        ('print(page.get_by_role("button", name="Купить").inner_text())', "Одна из них — по имени."),
        ('print(page.get_by_role("heading").inner_text())', "`<h1>` — роль heading."),
    ],
    mistake="Посчитать ссылку кнопкой — у `<a>` роль link."),

f"{P}-m1-l1-e2": x(
    idea="Поле находят по подписи (`label`) или плейсхолдеру — как пользователь.",
    lines=[
        ('print(page.get_by_label("Почта").get_attribute("name"))', "Подпись связана через `for`."),
        ('print(page.get_by_label("Пароль").get_attribute("type"))', "Поле внутри `<label>` — тоже связано."),
        ('print(page.get_by_role("textbox").count())', "Поле пароля — не textbox."),
    ],
    mistake="Посчитать 3 текстовых поля — пароль имеет другую роль."),

f"{P}-m1-l1-e3": x(
    idea="`get_by_text` по умолчанию — подстрока без учёта регистра; `exact=True` — точный текст целиком.",
    lines=[
        ('print(page.get_by_text("товар").count())', "Все три."),
        ('print(page.get_by_text("Товар добавлен").count())', "Два содержат фразу."),
        ('print(page.get_by_text("Товар добавлен", exact=True).count())', "Только точное совпадение."),
    ],
    mistake="Ждать учёта регистра без `exact`."),

f"{P}-m1-l1-e4": x(
    idea="`locator(css)` — по CSS; `first`, `last`, `nth(i)` — выбор из найденных; `get_by_test_id` — по `data-testid`.",
    lines=[
        ('items = page.locator("ul.menu li")', "Все пункты."),
        ("print(items.nth(1).inner_text())", "Индекс с 0 — второй."),
        ('print(page.get_by_test_id("cart").inner_text())', "Стабильный атрибут для тестов."),
    ],
    mistake="Думать, что `nth(1)` — первый."),

f"{P}-m1-l1-e5": x(
    idea="Роль + имя отличают кнопку от ссылки с тем же текстом.",
    lines=[('return page.get_by_role("button", name="Купить")', "Локатор, а не клик.")],
    mistake="`get_by_text(\"Купить\")` — найдёт и ссылку."),

f"{P}-m1-l1-e6": x(
    idea="`get_by_label` находит поле по подписи; `fill` вводит значение.",
    lines=[('page.get_by_label("Логин").fill(user)', "Логин."), ('page.get_by_label("Пароль").fill(password)', "Пароль.")],
    mistake="Искать по `#user` — подпись стабильнее и ближе к пользователю."),

f"{P}-m1-l1-e7": x(
    idea="`filter(has_text=…)` сужает набор карточек до одной; дальше ищем цену внутри неё.",
    lines=[
        ('text = page.get_by_test_id("product").filter(has_text=name).locator(".price").inner_text()', "Карточка → цена."),
        ("return int(text.split()[0])", "«1200 ₽» → 1200."),
    ],
    mistake="Искать `.price` по всей странице — цен несколько."),

f"{P}-m1-l1-e8": x(
    idea="Кнопка по роли и доступному имени.",
    lines=[('page.get_by_role("button", name="Оформить заказ")', "Роль + имя.")],
    mistake="`page.locator(\"button\")` — кнопок может быть много."),

f"{P}-m1-l2-e1": x(
    idea="`is_visible` проверяет сразу, а `expect(...).to_be_visible()` ждёт, пока элемент появится.",
    lines=[
        ('print(page.locator("#done").is_visible())', "Сейчас — ещё нет."),
        ('expect(page.locator("#done")).to_be_visible()', "Ждём."),
        ("print(page.clock)", "Прошло 1500 мс."),
    ],
    mistake="Проверять видимость через `is_visible` в тесте — флаки."),

f"{P}-m1-l2-e2": x(
    idea="`count()` — мгновенный снимок; `to_have_count` ждёт нужного числа.",
    lines=[("print(items.count())", "Пока 0."), ("expect(items).to_have_count(2)", "Дождались."), ("print(items.count(), page.clock)", "Через 800 мс.")],
    mistake="`assert items.count() == 2` — упадёт, если список ещё грузится."),

f"{P}-m1-l2-e3": x(
    idea="Действия ждут элемент, но не дольше таймаута — потом `TimeoutError`.",
    lines=[
        ('page.locator("#pay").click(timeout=1000)', "Ждём только секунду."),
        ('print("не дождались, часы:", page.clock)', "1000 мс."),
        ('page.locator("#pay").click()', "Обычный таймаут дождался 3000."),
    ],
    mistake="Ставить огромные таймауты везде — тесты станут медленными при настоящих ошибках."),

f"{P}-m1-l2-e6": x(
    idea="Ждём появления блока, потом читаем все названия разом.",
    lines=[
        ('page.locator("#products").wait_for()', "Загрузка завершилась."),
        ('return page.locator(".card h3").all_inner_texts()', "Тексты всех заголовков."),
    ],
    mistake="Читать сразу — получишь пустой список."),

f"{P}-m1-l2-e7": x(
    idea="`expect` с ожиданием вместо фиксированной паузы: тест быстрый, когда сайт быстрый, и терпеливый, когда медленный.",
    lines=[
        ("return shop_app()   # тестируемый сайт «Шоп»", "Фикстура `app` — какой сайт тестируем."),
        ('page.goto("/catalog")', "Открыть каталог."),
        ('expect(page.get_by_test_id("product")).to_have_count(5)', "Подождёт пять карточек."),
    ],
    mistake="`page.wait_for_timeout(3000)` — либо зря ждём, либо не дожидаемся."),

f"{P}-m1-l2-e4": x(
    idea="Повторяем тест до `retries + 1` раз; последняя неудача пробрасывается.",
    lines=[
        ("for attempt in range(1, retries + 2):", "Первая попытка и перезапуски."),
        ("test()\n            return attempt", "Прошёл — номер попытки."),
        ("if attempt == retries + 1:\n                raise", "Перезапуски кончились."),
    ],
    mistake="`range(retries)` — перезапусков на один меньше."),

f"{P}-m1-l2-e5": x(
    idea="Флаки — в истории есть и успех, и провал.",
    lines=[('return sorted(name for name, h in runs.items() if "pass" in h and "fail" in h)', "Оба результата.")],
    mistake="Считать флаки тест, который падает всегда — это просто сломанный тест."),

f"{P}-m1-l2-e8": x(
    idea="`--reruns N` из pytest-rerunfailures перезапускает упавшие тесты.",
    lines=[("pytest --reruns 2", "До двух перезапусков.")],
    mistake="Лечить перезапусками настоящую нестабильность — причину надо найти."),

f"{P}-actions-e1": x(
    idea="`fill` заменяет значение целиком, `clear` очищает, `input_value` читает.",
    lines=[("box.fill(\"мышь\")", "Было «клав» — стало «мышь»."), ("box.clear()", "Пусто.")],
    mistake="Думать, что `fill` дописывает."),

f"{P}-actions-e2": x(
    idea="`check` ставит галочку, `select_option` выбирает пункт и возвращает список выбранных значений.",
    lines=[
        ("agree.check()", "Галочка."),
        ('print(page.locator("select").input_value())', "По умолчанию первый — courier."),
        ('print(page.locator("select").select_option(label="Самовывоз"))', "Выбор по тексту → `['pickup']`."),
    ],
    mistake="Ожидать текст «Самовывоз» в input_value — там value."),

f"{P}-actions-e3": x(
    idea="Клик переключает видимость блока; `is_visible` показывает текущее состояние.",
    lines=[
        ('print(info.is_visible())', "Скрыт атрибутом hidden."),
        ('page.get_by_role("button", name="Подробнее").click()', "Показать."),
        ("print(info.is_visible())", "Второй клик — снова скрыт."),
    ],
    mistake="Ждать, что второй клик оставит блок открытым."),

f"{P}-actions-e4": x(
    idea="Строгий режим: действие с локатором, нашедшим несколько элементов, — ошибка. Нужно уточнить, например `.first`.",
    lines=[
        ('print(page.get_by_role("button", name="Нет в наличии").is_enabled())', "disabled — False."),
        ('page.get_by_role("button", name="В корзину").click()', "Две кнопки — strict mode violation."),
        ('page.get_by_role("button", name="В корзину").first.click()', "Явно первая."),
    ],
    mistake="Ожидать, что Playwright сам нажмёт первую."),

f"{P}-actions-e5": x(
    idea="Вход: открыть страницу, заполнить поля, нажать кнопку.",
    lines=[
        ('page.goto("/login")', "Страница входа."),
        ('page.get_by_label("Пароль").fill(password)', "Поля по подписям."),
        ('page.get_by_role("button", name="Войти").click()', "Отправка."),
    ],
    mistake="Забыть `goto` — функция будет зависеть от того, где тест сейчас."),

f"{P}-actions-e6": x(
    idea="`press(\"Enter\")` отправляет форму, как пользователь с клавиатуры.",
    lines=[('box = page.get_by_placeholder("Поиск")', "Поле."), ("box.fill(text)", "Текст."), ('box.press("Enter")', "Отправить.")],
    mistake="`fill(text + \"\\n\")` — перевод строки форму не отправит."),

f"{P}-actions-e7": x(
    idea="Сначала карточка нужного товара, потом кнопка внутри неё.",
    lines=[
        ('card = page.get_by_test_id("product").filter(has_text=name)', "Одна карточка."),
        ('card.get_by_role("button", name="В корзину").click()', "Её кнопка."),
    ],
    mistake="`page.get_by_role(\"button\", name=\"В корзину\")` — кнопок несколько, strict mode."),

f"{P}-actions-e8": x(
    idea="Тест = действия + проверка результата. `to_have_url` подождёт перехода.",
    lines=[
        ('page.get_by_label("Логин").fill("anna")', "Логин."),
        ('page.get_by_role("button", name="Войти").click()', "Вход."),
        ('expect(page).to_have_url("http://app.test/catalog")', "Перешли в каталог."),
    ],
    mistake="Тест без проверки — пройдёт, даже если вход сломан."),

f"{P}-expect-e1": x(
    idea="Неудачный `expect` бросает `AssertionError` с ожидаемым и фактическим значением.",
    lines=[
        ('expect(page.get_by_role("button")).to_have_text("Войти")', "Совпало."),
        ('expect(page.get_by_role("button")).to_have_text("Выйти", timeout=300)', "Ждали 300 мс — не дождались."),
        ("print(e)", "Понятное сообщение."),
    ],
    mistake="Ловить `TimeoutError` — expect бросает AssertionError."),

f"{P}-expect-e2": x(
    idea="`to_have_text` — весь текст, `to_contain_text` — подстрока, `not_to_…` — отрицание.",
    lines=[
        ('expect(total).to_contain_text("1800")', "Подстрока есть."),
        ('expect(page.locator(".error")).not_to_be_visible()', "Ошибка скрыта."),
        ('expect(total).to_have_text("1800", timeout=0)', "Весь текст — «Итого: 1800 ₽»."),
    ],
    mistake="Проверять кусок текста через to_have_text."),

f"{P}-expect-e3": x(
    idea="Для набора элементов `to_have_text` принимает список — порядок важен.",
    lines=[('expect(items).to_have_text(["Мышь", "Коврик"])', "По порядку."), ('expect(items).to_have_text(["Коврик", "Мышь"], timeout=0)', "Другой порядок — провал.")],
    mistake="Ждать, что порядок не важен."),

f"{P}-expect-e4": x(
    idea="Недоступность кнопки — `to_be_disabled()`.",
    lines=[('expect(page.get_by_role("button", name="Оплатить")).to_be_disabled()', "Проверка с ожиданием.")],
    mistake="`assert not button.is_enabled()` — без ожидания."),

f"{P}-expect-e5": x(
    idea="Негативный тест: неверный пароль — сообщение об ошибке в элементе с ролью alert.",
    lines=[
        ('page.get_by_label("Пароль").fill("wrong")', "Неверный пароль."),
        ('expect(page.get_by_role("alert")).to_have_text("Неверный логин или пароль")', "Текст ошибки."),
    ],
    mistake="Проверить только, что URL остался `/login`."),

f"{P}-expect-e6": x(
    idea="После входа имя пользователя видно в шапке — проверяем элемент по test id.",
    lines=[('expect(page.get_by_test_id("username")).to_have_text("anna")', "Имя в шапке.")],
    mistake="Искать имя `get_by_text(\"anna\")` — оно может встретиться и в другом месте."),

f"{P}-expect-e7": x(
    idea="После поиска ждём одну карточку и проверяем её содержимое.",
    lines=[
        ('page.get_by_placeholder("Поиск").fill("мыш")', "Запрос."),
        ("expect(cards).to_have_count(1)", "Подождать результата."),
        ('expect(cards).to_contain_text("Мышь")', "Нужный товар."),
    ],
    mistake="`assert cards.count() == 1` — проверит до загрузки."),

f"{P}-expect-e8": x(
    idea="Две проверки: кнопка недоступна, а обычных кнопок ровно 4.",
    lines=[
        ('expect(page.get_by_role("button", name="Нет в наличии")).to_be_disabled()', "Недоступна."),
        ('expect(page.get_by_role("button", name="В корзину")).to_have_count(4)', "Остальные товары доступны."),
    ],
    mistake="Проверить только наличие текста «Нет в наличии» — кнопка может оказаться активной."),

# ===== Модуль 2. Архитектура UI-тестов =====

f"{P}-m2-l1-e1": x(
    idea="Локатор — это описание поиска, а не найденный элемент: элементы ищутся в момент действия.",
    lines=[
        ('self.button = page.get_by_role("button", name="Найти")', "Создан до появления кнопки."),
        ("print(search.button.count())", "Пока страница пуста — 0."),
        ("print(search.button.count(), search.button.inner_text())", "После `set_content` — нашёлся."),
        ('print(search.type_query("мышь").box.input_value())', "Метод вернул `self` — цепочка."),
    ],
    mistake="Думать, что локатор «застывает» при создании."),

f"{P}-m2-l1-e2": x(
    idea="Page Object хранит локаторы страницы и даёт действия на языке пользователя.",
    lines=[
        ('self.user_input = page.get_by_label("Логин")', "Локаторы — атрибуты."),
        ('self.error = page.get_by_role("alert")', "Пригодится в негативных тестах."),
        ('self.page.goto("/login")', "open."),
        ("self.submit.click()", "login: заполнить и отправить."),
    ],
    mistake="Писать проверки (`expect`) внутри Page Object — проверки делает тест."),

f"{P}-m2-l1-e3": x(
    idea="Каталог: поиск, ожидание загрузки, названия и добавление товара.",
    lines=[
        ('self.page.get_by_role("button", name="Найти").click()', "Поиск."),
        ('self.page.locator("#products").wait_for()', "Дождаться товаров."),
        ('return self.page.locator(".card h3").all_inner_texts()', "Названия."),
        ('self.products.filter(has_text=name).get_by_role("button", name="В корзину").click()', "Кнопка нужного товара."),
    ],
    mistake="Читать названия без ожидания — пустой список."),

f"{P}-m2-l1-e4": x(
    idea="Корзина: строки, итог числом, удаление строки по названию.",
    lines=[
        ('self.rows = page.get_by_test_id("cart-row")', "Все строки."),
        ("return int(text.split()[1])", "«Итого: 2400 ₽» → второе слово."),
        ('self.rows.filter(has_text=name).get_by_role("button", name="Удалить").click()', "Своя кнопка «Удалить»."),
    ],
    mistake="`text.split()[0]` — это слово «Итого:»."),

f"{P}-m2-l1-e5": x(
    idea="Тест через Page Object короткий и читается как сценарий.",
    lines=[
        ("login_page = LoginPage(page)", "Объект страницы."),
        ('login_page.login("anna", "secret")', "Действие."),
        ('expect(page).to_have_url("http://app.test/catalog")', "Проверка в тесте."),
    ],
    mistake="Повторять локаторы в тесте, когда есть Page Object."),

f"{P}-m2-l1-e6": x(
    idea="Локатор ошибки уже в Page Object — тест проверяет текст и что переход не случился.",
    lines=[
        ('login_page.login("blocked", "blocked")', "Заблокированный пользователь."),
        ('expect(login_page.error).to_have_text("Пользователь заблокирован")', "Сообщение."),
        ('expect(page).to_have_url("http://app.test/login")', "Остались на входе."),
    ],
    mistake="Проверить только текст — пользователь мог всё-таки войти."),

f"{P}-m2-l1-e7": x(
    idea="Методы возвращают следующую страницу — тест строится цепочкой.",
    lines=[
        ("return self", "open → та же страница."),
        ("return CatalogPage(self.page)", "login → каталог."),
    ],
    mistake="Возвращать `None` — цепочка оборвётся."),

f"{P}-m2-l1-e8": x(
    idea="Общий компонент (шапка) — отдельный класс, его используют разные страницы.",
    lines=[
        ('return int(text[text.index("(") + 1:text.index(")")])', "Число между скобками."),
        ("return self.user.inner_text() if self.user.count() else None", "Не вошёл — имени нет."),
        ('self.page.get_by_role("link", name="Выйти").click()', "Выход."),
    ],
    mistake="Копировать методы шапки в каждый Page Object."),

f"{P}-m2-l2-e1": x(
    idea="Пирамида: больше всего модульных тестов, меньше всего UI.",
    lines=[("total = sum(tests.values())", "Всего 1000."), ('print(level, f"{n / total:.0%}")', "`:.0%` — процент без знаков.")],
    mistake="Ожидать `0.7` — формат `%` умножает на 100."),

f"{P}-m2-l2-e2": x(
    idea="Цепочка сравнений проверяет оба условия сразу.",
    lines=[("return unit > api > ui", "unit > api и api > ui.")],
    mistake="`>=` — равенство не считается пирамидой по условию."),

f"{P}-m2-l2-e3": x(
    idea="Имя файла: нижний регистр, пробелы → `_`, лишние символы выкидываем.",
    lines=[
        ('clean = "".join(ch for ch in test_name.lower().replace(" ", "_") if ch.isalnum() or ch == "_")', "Очистка."),
        ('return f"{browser}_{clean}.png"', "Браузер в начале."),
    ],
    mistake="Оставить `/` или `:` — файл не создастся."),

f"{P}-m2-l2-e4": x(
    idea="Срез с шагом `n` раздаёт элементы по кругу.",
    lines=[("return [tests[i::n] for i in range(n)]", "Воркер i берёт каждый n-й, начиная с i.")],
    mistake="Делить на куски подряд — по условию нужно по кругу."),

f"{P}-m2-l2-e5": x(
    idea="Процент считаем от запущенных; пропущенные не учитываем.",
    lines=[
        ("run = passed + failed", "Выполненные."),
        ('"pass_rate": round(100 * passed / run) if run else 0,', "Без деления на ноль."),
    ],
    mistake="Делить на `len(results)` — пропуски занизят процент."),

f"{P}-m2-l2-e6": x(
    idea="pytest-xdist: `-n` — число процессов.",
    lines=[("pytest -n 4", "Четыре воркера.")],
    mistake="Параллелить тесты с общим состоянием — начнутся флаки."),

f"{P}-m2-l2-e7": x(
    idea="Хрупкий селектор привязан к структуре вёрстки, а не к смыслу элемента.",
    lines=[('return selector.startswith("/") or "nth-child" in selector or selector.count(">") >= 2', "Абсолютный XPath, позиция, длинная цепочка.")],
    mistake="Считать хрупким любой CSS — `[data-testid=…]` стабилен."),

f"{P}-m2-l2-e8": x(
    idea="`--browser` выбирает браузер для pytest-playwright.",
    lines=[("pytest --browser firefox", "Firefox вместо Chromium.")],
    mistake="Менять код тестов ради другого браузера."),

f"{P}-fixtures-e1": x(
    idea="Фикстура `app` говорит плагину, какой сайт открыть в `page`.",
    lines=[("return shop_app()", "Тестируемый сайт."), ('expect(page).to_have_title("Вход")', "Заголовок вкладки.")],
    mistake="Проверять `<h1>` вместо title — это разные вещи."),

f"{P}-fixtures-e2": x(
    idea="Вход — в фикстуре: тесты начинаются сразу с нужного состояния.",
    lines=[
        ("def logged_in_page(page):", "Строится на `page`."),
        ("return page", "Отдаёт вошедшую страницу."),
        ('expect(logged_in_page.get_by_test_id("username")).to_have_text("anna")', "Тест — одна проверка."),
    ],
    mistake="Повторять вход в каждом тесте."),

f"{P}-fixtures-e3": x(
    idea="Фикстура на фикстуре: «вошёл» → «положил две мыши».",
    lines=[
        ("def two_mice(logged_in_page):", "Зависит от входа."),
        ('mouse = page.get_by_test_id("product").filter(has_text="Мышь").get_by_role("button", name="В корзину")', "Кнопка мыши."),
        ("mouse.click()", "Дважды."),
        ('expect(two_mice.locator("#total")).to_have_text("Итого: 2400 ₽")', "2 × 1200."),
    ],
    mistake="Копировать вход в фикстуру `two_mice` — дублирование."),

f"{P}-fixtures-e4": x(
    idea="До `yield` — подготовка, после — уборка (выход).",
    lines=[("yield page", "Тест работает здесь."), ('page.get_by_role("link", name="Выйти").click()', "После теста — выход.")],
    mistake="`return` — код уборки не выполнится."),

f"{P}-fixtures-e5": x(
    idea="Фикстуры из `conftest.py` доступны всем тестам папки без импорта.",
    lines=[("def app():", "Сайт для всех тестов."), ("def logged_in_page(page):", "Общий вход.")],
    mistake="Импортировать фикстуры из conftest — pytest подхватывает их сам."),

f"{P}-fixtures-e6": x(
    idea="`base_url` — к нему дописываются пути в `goto`. Переопределил — тесты пошли на другой стенд.",
    lines=[('return "http://stage.shop.test"', "Новый адрес."), ('expect(page).to_have_url("http://stage.shop.test/login")', "Путь дописан к base_url.")],
    mistake="Писать полный адрес в каждом `goto`."),

f"{P}-fixtures-e7": x(
    idea="Изоляция: у каждого теста своя страница и свежий сайт — корзина пустая в начале каждого.",
    lines=[
        ('page.get_by_test_id("product").filter(has_text=name).get_by_role("button", name="В корзину").click()', "Общий помощник."),
        ('expect(page.get_by_test_id("cart-link")).to_have_text("Корзина (1)")', "В обоих тестах — 1."),
    ],
    mistake="Ожидать «Корзина (2)» во втором тесте — состояние не переносится."),

f"{P}-fixtures-e8": x(
    idea="`--headed` показывает окно браузера — удобно при отладке.",
    lines=[("pytest --headed", "Видимый браузер.")],
    mistake="Запускать headed в CI — там нет экрана."),

f"{P}-params-e1": x(
    idea="Параметризация: один сценарий, три набора данных.",
    lines=[
        ('@pytest.mark.parametrize("user, password", [', "Имена параметров."),
        ('("nobody", "secret"),', "Один из случаев."),
        ('expect(page.get_by_role("alert")).to_have_text("Неверный логин или пароль")', "Общая проверка."),
    ],
    mistake="Три почти одинаковых теста."),

f"{P}-params-e2": x(
    idea="Пустые поля — отдельная ошибка; все три случая в одном тесте.",
    lines=[('@pytest.mark.parametrize("user, password", [("", "secret"), ("anna", ""), ("", "")])', "Логин, пароль, оба."), ('expect(page.get_by_role("alert")).to_have_text("Введите логин и пароль")', "Сообщение.")],
    mistake="Проверить только оба пустых."),

f"{P}-params-e3": x(
    idea="Список ожидаемых названий — `to_have_text` со списком, порядок важен.",
    lines=[('("к", ["Клавиатура", "Наушники", "Коврик"]),', "Несколько результатов."), ('expect(page.locator(".card h3")).to_have_text(expected)', "Сравнение списком.")],
    mistake="Проверять только количество — не те товары останутся незамеченными."),

f"{P}-params-e4": x(
    idea="Выпадающий список по подписи, `select_option(value)`, затем проверяем первый товар.",
    lines=[
        ('page.get_by_label("Сортировка").select_option(sort)', "Значение варианта."),
        ('expect(page.locator(".card h3").first).to_have_text(first)', "Первый после сортировки."),
    ],
    mistake="Забыть нажать «Найти» — сортировка не применится."),

f"{P}-params-e5": x(
    idea="`pytest.param(..., id=…)` — понятные имена случаев в отчёте.",
    lines=[
        ('pytest.param("", "+79991234567", True, "Укажите имя", id="no-name"),', "Случай с именем."),
        ('page.get_by_label("Согласен с условиями").check()', "Галочка — только если нужно."),
        ("expect(page.get_by_role(\"alert\")).to_have_text(error)", "Своя ошибка."),
    ],
    mistake="Без id — имена вида `[-+79991234567-True-…]`."),

f"{P}-params-e6": x(
    idea="`csv.reader` разбирает строки, первую (заголовок) пропускаем.",
    lines=[("rows = list(csv.reader(text.splitlines()))", "Списки значений."), ("return [tuple(row) for row in rows[1:]]", "Без заголовка, кортежами.")],
    mistake="`split(\",\")` вручную — сломается на значениях с запятой в кавычках."),

f"{P}-params-e7": x(
    idea="Проверяем, что в шапке имя именно этого пользователя — параметр идёт и в проверку.",
    lines=[('@pytest.mark.parametrize("user, password", [("anna", "secret"), ("boris", "qwerty123")])', "Два пользователя."), ('expect(page.get_by_test_id("username")).to_have_text(user)', "Своё имя.")],
    mistake="Проверять константу «anna» для обоих."),

f"{P}-params-e8": x(
    idea="Один случай параметризации запускают по полному id узла; кавычки защищают `[]` от оболочки.",
    lines=[('pytest "test_checkout.py::test_checkout_errors[bad-phone]"', "Только bad-phone.")],
    mistake="Без кавычек в zsh — `no matches found`."),

# ===== Модуль 3. Практика =====

f"{P}-reports-e1": x(
    idea="`screenshot(path=…)` пишет PNG и возвращает его байты — их можно сразу приложить к отчёту.",
    lines=[
        ('data = page.screenshot(path="catalog.png")', "Файл и байты."),
        ("print(data[1:4])", "Сигнатура PNG: байты 1–3 — «PNG»."),
        ('print(os.path.exists("catalog.png"))', "Файл создан."),
    ],
    mistake="Ожидать строку — это `bytes`."),

f"{P}-reports-e2": x(
    idea="Создаём папку (если нет) и сохраняем скриншот по имени.",
    lines=[
        ('os.makedirs("screenshots", exist_ok=True)', "Папка."),
        ('path = f"screenshots/{name}.png"', "Путь."),
        ("page.screenshot(path=path)", "Снимок."),
    ],
    mistake="Без `exist_ok` — второй вызов упадёт."),

f"{P}-reports-e3": x(
    idea="Сначала дождаться загрузки, потом снимать — иначе в отчёте будет пустая страница.",
    lines=[
        ('expect(page.get_by_test_id("product")).to_have_count(5)', "Ждём товары."),
        ('allure.attach(page.screenshot(), name="Каталог", attachment_type=allure.attachment_type.PNG)', "Байты в отчёт."),
    ],
    mistake="Скриншот сразу после `goto` — снимешь «Загрузка…»."),

f"{P}-reports-e4": x(
    idea="Шаги Allure превращают UI-тест в читаемый сценарий в отчёте.",
    lines=[
        ('with allure.step("Открыть страницу входа"):', "Шаг 1."),
        ('with allure.step("Ввести логин и пароль"):', "Шаг 2."),
        ('expect(page).to_have_url("http://app.test/catalog")', "Проверка — в последнем шаге."),
    ],
    mistake="Один шаг на весь тест — не видно, где упало."),

f"{P}-reports-e5": x(
    idea="Хук после теста: при падении берём фикстуру `page` из `item.funcargs` и прикладываем скриншот.",
    lines=[
        ('if report.when == "call" and report.failed:', "Упал сам тест."),
        ('page = item.funcargs.get("page")', "Тест мог и не использовать page."),
        ('allure.attach(page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)', "Скриншот в отчёт."),
    ],
    mistake="`item.funcargs[\"page\"]` — KeyError у тестов без браузера."),

f"{P}-reports-e6": x(
    idea="Трейс — запись теста по шагам; просмотрщик показывает DOM, сеть и консоль на каждом шаге.",
    lines=[("playwright show-trace trace.zip", "Открыть трейс.")],
    mistake="Распаковывать zip вручную."),

f"{P}-reports-e7": x(
    idea="Опция pytest-playwright `--screenshot only-on-failure`.",
    lines=[("pytest --screenshot only-on-failure", "Только упавшие.")],
    mistake="`--screenshot on` — снимки для всех тестов."),

f"{P}-reports-e8": x(
    idea="`--tracing retain-on-failure` — трейс пишется всегда, но остаётся только у упавших.",
    lines=[("pytest --tracing retain-on-failure", "Трейсы упавших.")],
    mistake="`--tracing on` — трейс у каждого теста, много места."),

f"{P}-lists-e1": x(
    idea="`all_inner_texts` — тексты всех элементов списком; дальше обычный Python.",
    lines=[
        ('texts = page.get_by_role("listitem").all_inner_texts()', "Три строки."),
        ("prices = [int(t.split()[-2]) for t in texts]", "Предпоследнее слово — цена."),
        ("print(prices, prices == sorted(prices))", "Убывают — не по возрастанию."),
    ],
    mistake="`split()[-1]` — это «₽»."),

f"{P}-lists-e2": x(
    idea="`.all()` — список локаторов, по одному на элемент; внутри каждого ищем дальше.",
    lines=[
        ('for card in page.locator(".card").all():', "Каждая карточка."),
        ('name = card.locator("h3").inner_text()', "Поиск внутри карточки."),
    ],
    mistake="Искать `h3` по всей странице — strict mode при двух карточках."),

f"{P}-lists-e3": x(
    idea="`filter(has_text=…)` оставляет содержащие текст, `has_not_text` — не содержащие.",
    lines=[
        ('print(cards.filter(has_text="В корзину").count())', "Две доступные."),
        ('print(cards.filter(has_not_text="В корзину").inner_text())', "Наушники."),
        ('print(cards.filter(has_text="Коврик").get_by_role("button").is_enabled())', "Кнопка Коврика активна."),
    ],
    mistake="Считать кнопку «Нет в наличии» подходящей под «В корзину»."),

f"{P}-lists-e4": x(
    idea="Строка таблицы — роль row (заголовок тоже строка), ячейки — роль cell.",
    lines=[
        ("print(rows.count())", "Заголовок + 2 строки."),
        ('print(rows.filter(has_text="Мышь").locator(".qty").inner_text())', "Ячейка в строке Мыши."),
        ('print(page.get_by_role("cell").all_inner_texts())', "`<th>` — не cell."),
    ],
    mistake="Посчитать 2 строки — забыть строку заголовка."),

f"{P}-lists-e5": x(
    idea="Ждём загрузки, проходим по карточкам и собираем словарь.",
    lines=[
        ('page.locator("#products").wait_for()', "Товары появились."),
        ('for card in page.get_by_test_id("product").all():', "Каждая карточка."),
        ('result[name] = int(card.locator(".price").inner_text().split()[0])', "Цена числом."),
    ],
    mistake="Собирать без ожидания — пустой словарь."),

f"{P}-lists-e6": x(
    idea="Проверка сортировки: собрать цены, сравнить с `sorted`.",
    lines=[
        ('page.get_by_label("Сортировка").select_option("price")', "Выбор сортировки."),
        ('expect(page.get_by_test_id("product")).to_have_count(5)', "Дождаться."),
        ('prices = [int(text.split()[0]) for text in page.locator(".card .price").all_inner_texts()]', "Числа."),
        ("assert prices == sorted(prices), prices", "В сообщении — фактический порядок."),
    ],
    mistake="Сравнивать строки цен — «600» > «1200»."),

f"{P}-lists-e7": x(
    idea="Удаляем строку по названию и проверяем, что осталась нужная.",
    lines=[
        ('rows.filter(has_text="Коврик").get_by_role("button", name="Удалить").click()', "Кнопка в строке Коврика."),
        ("expect(rows).to_have_count(1)", "Одна строка."),
        ('expect(rows).to_contain_text("Мышь")', "Нужная."),
    ],
    mistake="Проверить только количество — могла удалиться не та строка."),

f"{P}-lists-e8": x(
    idea="Количество в строке и итог корзины: 2 × 1200 + 3500 = 5900.",
    lines=[
        ('mouse = page.get_by_test_id("cart-row").filter(has_text="Мышь")', "Строка мыши."),
        ('expect(mouse.locator(".qty")).to_have_text("2")', "Количество."),
        ('expect(page.locator("#total")).to_have_text("Итого: 5900 ₽")', "Сумма."),
    ],
    mistake="Ждать две отдельные строки мыши — корзина складывает количество."),

f"{P}-real-e1": x(
    idea="`pytest-playwright` ставит Playwright и даёт фикстуру `page`.",
    lines=[("pip install pytest-playwright", "Плагин.")],
    mistake="`pip install playwright` — без фикстур pytest."),

f"{P}-real-e2": x(
    idea="Браузеры скачиваются отдельной командой.",
    lines=[("playwright install chromium", "Только Chromium.")],
    mistake="Ждать, что pip скачает браузеры."),

f"{P}-real-e3": x(
    idea="`codegen` записывает действия в браузере и генерирует код.",
    lines=[("playwright codegen https://demo.shop.test", "Генератор тестов.")],
    mistake="Оставлять сгенерированный код как есть — его нужно чистить и добавлять проверки."),

f"{P}-real-e4": x(
    idea="`--headed` — видимый браузер, `--slowmo` — пауза перед каждым действием.",
    lines=[("pytest --headed --slowmo 500", "Видно и неспешно.")],
    mistake="Оставлять slowmo в CI — тесты станут в разы медленнее."),

f"{P}-real-e5": x(
    idea="В настоящем проекте модуль — `playwright.sync_api`.",
    lines=[("from playwright.sync_api import Page, expect", "Тот же API.")],
    mistake="Импортировать `pwfake` в рабочем проекте — это учебная подделка."),

f"{P}-real-e6": x(
    idea="Без pytest: менеджер `sync_playwright`, запуск браузера, новая страница, закрытие.",
    lines=[
        ("with sync_playwright() as p:", "Playwright запущен."),
        ("browser = p.chromium.launch()", "Браузер."),
        ('page.locator("#products").wait_for()', "Ждём товары."),
        ("browser.close()", "Закрыть браузер."),
    ],
    mistake="Не закрыть браузер — процессы останутся висеть."),

f"{P}-real-e7": x(
    idea="`--base-url` задаёт адрес, к которому дописываются пути `goto`.",
    lines=[("pytest --base-url https://stage.shop.test", "Тесты на стенде.")],
    mistake="Менять адреса в коде тестов."),

f"{P}-real-e8": x(
    idea="Опцию `--browser` можно указать несколько раз — каждый тест пройдёт во всех браузерах.",
    lines=[("pytest --browser chromium --browser firefox", "Два прогона каждого теста.")],
    mistake="`--browser chromium,firefox` — так не работает."),

f"{P}-project-e1": x(
    idea="Сквозной тест проходит весь путь пользователя: вход → корзина → оформление → подтверждение.",
    lines=[
        ('page.get_by_test_id("product").filter(has_text="Мышь").get_by_role("button", name="В корзину").click()', "Товар в корзину."),
        ('page.get_by_role("link", name="Оформить заказ").click()', "К оформлению."),
        ('page.get_by_label("Согласен с условиями").check()', "Согласие."),
        ('expect(page.get_by_test_id("order-number")).to_have_text("Номер заказа: 1001")', "Итог."),
    ],
    mistake="Сквозных тестов много — они медленные; их держат для главных сценариев."),

f"{P}-project-e2": x(
    idea="Гость пытается оформить заказ — сайт отправляет на вход.",
    lines=[('page.get_by_role("link", name="Оформить заказ").click()', "Без входа."), ('expect(page).to_have_url("http://app.test/login")', "Редирект.")],
    mistake="Начинать с входа — проверяем как раз гостя."),

f"{P}-project-e3": x(
    idea="После выхода элемента с именем нет (`to_have_count(0)`), а ссылка «Войти» видна.",
    lines=[
        ('page.get_by_role("link", name="Выйти").click()', "Выход."),
        ('expect(page.get_by_test_id("username")).to_have_count(0)', "Имени нет."),
        ('expect(page.get_by_role("link", name="Войти")).to_be_visible()', "Можно войти снова."),
    ],
    mistake="`not_to_be_visible` — пройдёт и для скрытого, но существующего элемента."),

f"{P}-project-e4": x(
    idea="Параметризация вариантов доставки: значение в списке и подпись на странице заказа.",
    lines=[
        ('@pytest.mark.parametrize("value, label", [("courier", "Курьер"), ("pickup", "Самовывоз")])', "Два варианта."),
        ('page.get_by_label("Доставка").select_option(value)', "Выбор по value."),
        ('expect(page.get_by_text("Доставка:")).to_have_text(f"Доставка: {label}")', "Подпись на странице."),
    ],
    mistake="Сравнивать с value — на странице показывается подпись."),

f"{P}-project-e5": x(
    idea="Повторяющиеся шаги — во вспомогательную функцию, тест остаётся коротким.",
    lines=[
        ("def place_order(page):", "Оформление заказа целиком."),
        ('expect(page.get_by_test_id("order-number")).to_have_text("Номер заказа: 1001")', "Первый заказ."),
        ('expect(page.get_by_test_id("order-number")).to_have_text("Номер заказа: 1002")', "Номер вырос."),
    ],
    mistake="Копировать шаги оформления дважды."),

f"{P}-project-e6": x(
    idea="Баг-репорт: заголовок, нумерованные шаги, ожидаемое и фактическое.",
    lines=[
        ('lines = [f"Баг: {title}", "Шаги:"]', "Шапка."),
        ('lines += [f"{i}. {step}" for i, step in enumerate(steps, 1)]', "Шаги с 1."),
        ('return "\\n".join(lines)', "Строки через перевод строки."),
    ],
    mistake="Нумерация с 0."),

f"{P}-project-e7": x(
    idea="Каждый регрессионный тест проверяет одну вещь — при падении сразу видно, что сломалось.",
    lines=[
        ('expect(page).to_have_url("http://app.test/catalog")', "Редирект после входа."),
        ('expect(page.get_by_test_id("product")).to_have_count(1)', "Поиск."),
        ('expect(page.get_by_test_id("cart-link")).to_have_text("Корзина (1)")', "Счётчик корзины."),
    ],
    mistake="Один большой тест на всё — первая ошибка скроет остальные."),

f"{P}-project-e8": x(
    idea="Свой таймаут в `expect` превращает его в проверку скорости.",
    lines=[('expect(page.get_by_test_id("product")).to_have_count(5, timeout=4000)', "Не дольше 4 секунд.")],
    mistake="Мерить время вручную через `time.time()` вокруг ожидания."),
}
