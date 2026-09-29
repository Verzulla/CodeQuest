"""Теория модуля «Архитектура UI-тестов» темы «Тестирование UI».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- ui-m2-l1 ----------
'ui-m2-l1': dict(
    full=t(r'''
## Зачем это нужно

Представь 50 тестов, и в каждом `page.get_by_label("Логин").fill(...)`. Дизайнер переименовал подпись в «Email» — и чинить нужно 50 мест. **Page Object** (объект страницы) решает это: всё знание о странице — локаторы и действия — живёт в одном классе, а тесты говорят на языке сценария: «войти», «найти товар», «добавить в корзину».

## Простой Page Object

```py
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
```

Тест становится коротким и читаемым:

```py
def test_wrong_password(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("anna", "wrong")
    expect(login_page.error).to_have_text("Неверный логин или пароль")
```

- Локаторы создаются в `__init__` один раз — это безопасно, потому что локатор **ленивый** и ищет элемент при каждом использовании.
- Методы описывают **действия пользователя**, а не клики: `login(...)`, `search(...)`, `add(name)`.
- Проверки (`expect`) обычно остаются **в тесте** — Page Object отвечает на вопрос «как сделать», тест — «что должно получиться». Методы-«читатели» (`total()`, `names()`) возвращают данные для проверок.

## Ленивые локаторы в деле

```python
from pwfake.sync_api import Page


class CartPage:
    def __init__(self, page):
        self.page = page
        self.rows = page.get_by_test_id("cart-row")

    def total(self):
        return int(self.page.locator("#total").inner_text().split()[1])


page = Page()
cart = CartPage(page)
print(cart.rows.count())
page.set_content('<table><tr data-testid="cart-row"><td>Мышь</td></tr></table> <p id="total">Итого: 1200 ₽</p>')
print(cart.rows.count(), cart.total())
```

Вывод: `0`, затем `1 1200` — объект создан до появления содержимого, но локаторы работают.

## Переходы между страницами

Метод, который ведёт на другую страницу, может вернуть её объект — тест читается цепочкой:

```py
catalog = LoginPage(page).open().login("anna", "secret")   # open() возвращает self, login() — CatalogPage
catalog.add("Мышь")
```

## Компоненты

Шапка, меню, модальное окно повторяются на многих страницах. Их выносят в классы-**компоненты** (`Header`, `CartWidget`) и подключают в Page Object'ы: `self.header = Header(page)`.

## Итог

- Page Object = локаторы + действия одной страницы в одном классе; вёрстка поменялась — правишь один файл.
- Методы — на языке пользователя; проверки — в тестах.
- Возвращай объект следующей страницы для цепочек; общие части — в компоненты.
'''),
    short=t(r'''
```py
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.submit = page.get_by_role("button", name="Войти")   # ленивые локаторы
    def open(self):
        self.page.goto("/login"); return self
    def login(self, user, password):
        ...; return CatalogPage(self.page)                       # переход → новый объект

def test_x(page):
    LoginPage(page).open().login("anna", "secret")
    expect(page).to_have_url(...)                                # проверки — в тесте
```
'''),
    quiz=[
        q('Главная польза Page Object?',
            ['Тесты выполняются быстрее', 'Знание о странице в одном месте: вёрстка изменилась — правишь один класс', 'Не нужны локаторы', 'Можно не писать проверки'],
            1, 'Поддерживаемость — ради неё паттерн и придуман.'),
        q('Где обычно пишут `expect(...)`-проверки при использовании Page Object?',
            ['Только в `__init__`', 'В тесте', 'В conftest.py', 'Нигде'],
            1, 'Page Object — «как сделать», тест — «что проверить».'),
        q('Почему можно создать локаторы в `__init__`, когда страница ещё пустая?',
            ['Нельзя — будет ошибка', 'Локатор ленивый: элемент ищется в момент действия', 'Playwright кэширует элементы', 'Потому что есть `wait_for_timeout`'],
            1, 'Локатор — инструкция поиска, а не найденный элемент.'),
    ],
),

# ---------- ui-m2-l2 ----------
'ui-m2-l2': dict(
    full=t(r'''
## Зачем это нужно

UI-тесты — самые дорогие: медленные (секунды на тест против миллисекунд у unit), хрупкие, требуют стенда и браузера. Автоматизировать всё через интерфейс — путь к набору, который идёт час и краснеет от каждого чиха. Нужна **стратегия**: что проверять через UI, а что — ниже.

## Пирамида тестирования

```bash
       /\        UI (E2E) — мало: ключевые сценарии
      /  \
     / API\      API / интеграционные — больше
    /------\
   /  Unit  \    Модульные — больше всего: быстрые и стабильные
```

- Через UI проверяют **ключевые пути пользователя**: вход, поиск, корзина, оплата — то, что приносит деньги и ломается на стыке фронта и бэка.
- Валидацию каждого поля, расчёты, граничные значения дешевле проверить на уровне API и unit.
- Перевёрнутая пирамида («рожок мороженого»: UI-тестов больше всего) — признак беды: медленно и нестабильно.

## Хорошие практики

- **Независимость**: каждый тест сам готовит данные (лучше через API или фикстуры, а не кликами) и не зависит от порядка.
- **Стабильные локаторы**: роли, подписи, `data-testid`. Хрупкие — абсолютный XPath (`/html/body/div[2]/…`), `:nth-child`, длинные цепочки `div > div > form > button`.
- **Артефакты падения**: скриншот, трейс, лог — без них падение в CI не разобрать.
- **Параллельность**: `pytest -n 4` (pytest-xdist) — независимые тесты гоняются на нескольких процессах.
- **Кроссбраузерность**: `pytest --browser chromium --browser firefox` — один и тот же набор в разных движках.
- **Смоук-набор**: 5–15 самых важных тестов на каждый коммит, полный регресс — ночью.

## Сколько тестов прошло

Отчёт показывает не только «зелёный/красный», но и pass rate среди запущенных (пропущенные не считаются), список флаки и время прогона. Эти метрики помогают решать, что чинить в первую очередь.

## Итог

- Пирамида: много unit, меньше API, мало UI — только ключевые сценарии.
- Независимые тесты, стабильные локаторы, артефакты при падении.
- Параллельный запуск и кроссбраузерность — через опции pytest.
'''),
    short=t(r'''
```bash
# пирамида: unit > api > ui
pytest -n 4                                   # параллельно (pytest-xdist)
pytest --browser chromium --browser firefox   # кроссбраузерно (pytest-playwright)
pytest -m smoke                               # смоук-набор
# хрупко: /html/body/div[2]  :nth-child(3)  div > div > form > button
# стабильно: get_by_role, get_by_label, data-testid
```
'''),
    quiz=[
        q('Что лучше проверять через UI-тесты?',
            ['Каждое правило валидации каждого поля', 'Ключевые пользовательские сценарии: вход, корзина, оплата', 'Все граничные значения расчётов', 'Всё подряд'],
            1, 'Остальное дешевле проверить ниже по пирамиде.'),
        q('Какой селектор самый хрупкий?',
            ['`[data-testid=submit]`', '`get_by_role("button", name="Оплатить")`', '`/html/body/div[2]/div/form/button`', '`get_by_label("Email")`'],
            2, 'Абсолютный XPath ломается от любой правки вёрстки.'),
        q('Что делает `pytest -n 4`?',
            ['Запускает 4 теста', 'Повторяет каждый тест 4 раза', 'Запускает тесты параллельно в 4 процессах', 'Ставит таймаут 4 секунды'],
            2, 'Опция pytest-xdist.'),
    ],
),

# ---------- ui-fixtures ----------
'ui-fixtures': dict(
    full=t(r'''
## Зачем это нужно

Каждому тесту нужен браузер, страница, часто — вошедший пользователь и товары в корзине. Повторять это в каждом тесте — долго и хрупко. **Фикстуры pytest** готовят окружение и отдают его тесту параметром, а плагин **pytest-playwright** уже содержит готовые: `browser`, `context`, `page`.

## Фикстура page

```py
def test_title(page):            # pytest-playwright сам запустит браузер и откроет вкладку
    page.goto("/login")
    expect(page).to_have_title("Вход")
```

Для каждого теста — **новая** страница (и новый контекст браузера: без куки и истории прошлого теста). Поэтому тесты не влияют друг на друга.

В pwfake-заданиях плагин устроен так же, только сайт он берёт из фикстуры `app`:

```py
@pytest.fixture
def app():
    return shop_app()        # в настоящем проекте вместо этого — адрес стенда в base_url
```

## Свои фикстуры поверх page

```py
@pytest.fixture
def logged_in_page(page):
    page.goto("/login")
    page.get_by_label("Логин").fill("anna")
    page.get_by_label("Пароль").fill("secret")
    page.get_by_role("button", name="Войти").click()
    return page


def test_header(logged_in_page):
    expect(logged_in_page.get_by_test_id("username")).to_have_text("anna")
```

Фикстуры строятся цепочкой: `two_mice(logged_in_page)` → `logged_in_page(page)` → `page(browser)`. pytest сам вызовет их в нужном порядке.

В реальных проектах вход часто делают **через API** или сохранённое состояние (`storage_state`), а не кликами: это в разы быстрее. Кликами проверяют только сам вход.

## yield: подготовка и уборка

```py
@pytest.fixture
def logged_in_page(page):
    ...                      # до yield — подготовка
    yield page               # тест работает здесь
    page.get_by_role("link", name="Выйти").click()   # после — уборка (даже если тест упал)
```

## conftest.py

Фикстуры, нужные многим файлам, кладут в `conftest.py` — pytest находит его сам, импортировать не нужно. Типичный UI-проект:

```bash
tests/
  conftest.py          # app/base_url, logged_in_page, данные
  pages/               # Page Object'ы
    login_page.py
  test_login.py
  test_cart.py
```

## base_url

pytest-playwright берёт адрес сайта из фикстуры `base_url` (или опции `--base-url`). `page.goto("/login")` дописывает путь к нему — один набор тестов гоняют на разных стендах:

```py
@pytest.fixture
def base_url():
    return "http://stage.shop.test"
```

## Полезные опции

```bash
pytest --headed                 # видимое окно браузера
pytest --browser firefox        # другой браузер
pytest --slowmo 500             # замедлить каждое действие на 500 мс
```

## Итог

- `page` из плагина — новая вкладка на каждый тест, тесты изолированы.
- Повторяющуюся подготовку — в свои фикстуры, общие — в `conftest.py`.
- `yield` — подготовка до, уборка после.
- `base_url` задаёт стенд.
'''),
    short=t(r'''
```py
def test_x(page): ...                   # pytest-playwright: browser, context, page

@pytest.fixture
def logged_in_page(page):
    ...вход...
    yield page                          # после yield — уборка
    page.get_by_role("link", name="Выйти").click()

@pytest.fixture
def base_url():
    return "http://stage.shop.test"     # page.goto("/login") → stage…/login
# conftest.py — общие фикстуры без импорта
# pytest --headed --browser firefox --slowmo 500
```
'''),
    quiz=[
        q('Почему тесты с фикстурой `page` не влияют друг на друга?',
            ['Они всегда идут по порядку', 'Каждый тест получает новую страницу и чистый контекст браузера', 'Playwright сам откатывает базу данных', 'Не знаю — влияют'],
            1, 'Контекст — как новый профиль браузера.'),
        q('Где держать фикстуру `logged_in_page`, нужную тестам из разных файлов?',
            ['В каждом файле копию', 'В `conftest.py`', 'В `pytest.ini`', 'В Page Object'],
            1, 'conftest.py подключается автоматически.'),
        q('Что делает код после `yield` в фикстуре?',
            ['Ничего', 'Выполняется после теста — уборка', 'Выполняется до теста', 'Повторяет тест'],
            1, 'Teardown — даже если тест упал.'),
    ],
),

# ---------- ui-params ----------
'ui-params': dict(
    full=t(r'''
## Зачем это нужно

Вход с неверным паролем, с несуществующим логином, с пустыми полями — один и тот же сценарий с разными данными. Копировать тест трижды — плохо: при изменении страницы чинить три места. **Параметризация** запускает один тест на наборе данных, и каждый набор — отдельный тест в отчёте.

## parametrize в UI-тестах

```py
@pytest.mark.parametrize("user, password", [
    ("anna", "wrong"),
    ("nobody", "secret"),
])
def test_bad_login(page, user, password):
    page.goto("/login")
    page.get_by_label("Логин").fill(user)
    page.get_by_label("Пароль").fill(password)
    page.get_by_role("button", name="Войти").click()
    expect(page.get_by_role("alert")).to_have_text("Неверный логин или пароль")
```

- Параметры и фикстуры смешиваются свободно: `page` — фикстура, `user` и `password` — из `parametrize`.
- Каждый случай получает свою страницу — случаи независимы.
- В отчёте: `test_bad_login[anna-wrong]`, `test_bad_login[nobody-secret]`.

## Ожидаемый результат — тоже параметр

```py
@pytest.mark.parametrize("sort, first", [
    ("price", "Коврик"),
    ("price_desc", "Монитор"),
])
def test_sort(page, sort, first):
    ...
    expect(page.locator(".card h3").first).to_have_text(first)
```

## Понятные имена случаев

```py
@pytest.mark.parametrize("name, phone, error", [
    pytest.param("", "+79991234567", "Укажите имя", id="no-name"),
    pytest.param("Аня", "123", "Неверный телефон", id="bad-phone"),
])
```

Отчёт покажет `test_checkout_errors[bad-phone]` вместо длинной строки с данными. Запустить один случай:

```bash
pytest "test_checkout.py::test_checkout_errors[bad-phone]"
```

Кавычки нужны из-за квадратных скобок — иначе оболочка может их интерпретировать.

## Данные из файла

Когда случаев много, их выносят в CSV/JSON рядом с тестами:

```python
import csv

text = "login,password\nanna,wrong\nnobody,secret\n"
rows = list(csv.reader(text.splitlines()))
print(rows[0])
print([tuple(r) for r in rows[1:]])
```

Вывод: `['login', 'password']`, затем `[('anna', 'wrong'), ('nobody', 'secret')]` — готовый список для `parametrize`. `csv` правильно разбирает значения с запятыми в кавычках: `"Иванов, Иван"`.

## Итог

- Один сценарий + разные данные = `parametrize`; ожидаемый результат — тоже параметр.
- `pytest.param(..., id="…")` — читаемые имена случаев.
- Большие наборы данных — в файлы, разбор через `csv`/`json`.
'''),
    short=t(r'''
```py
@pytest.mark.parametrize("user, password", [("anna", "wrong"), ("nobody", "secret")])
def test_bad_login(page, user, password): ...

pytest.param("", "123", "Укажите имя", id="no-name")    # имя случая в отчёте

list(csv.reader(text.splitlines()))[1:]                 # данные из CSV без заголовка
# pytest "test_checkout.py::test_checkout_errors[no-name]"
```
'''),
    quiz=[
        q('Сколько тестов увидит pytest у функции с `parametrize` на 3 набора данных?',
            ['1', '3', '6', 'Зависит от браузера'],
            1, 'Каждый набор — отдельный тест.'),
        q('Зачем `pytest.param(..., id="bad-phone")`?',
            ['Чтобы пропустить случай', 'Чтобы у случая было понятное имя в отчёте и командной строке', 'Чтобы запустить его дважды', 'Для ускорения'],
            1, 'id заменяет автоматическое имя из данных.'),
        q('Можно ли в одном тесте использовать и фикстуру `page`, и параметры из `parametrize`?',
            ['Нет', 'Да, в любом порядке в сигнатуре', 'Только если page последняя', 'Только в conftest'],
            1, 'pytest сам разберёт, что откуда.'),
    ],
),

}
