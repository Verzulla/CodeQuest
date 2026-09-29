"""Теория модуля «Практика» темы «Тестирование UI».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- ui-reports ----------
'ui-reports': dict(
    full=t(r'''
## Зачем это нужно

UI-тест упал ночью в CI. Сообщение «ожидалось: текст 'Заказ оформлен'» не говорит, что было на экране: ошибка сервера? всплывающее окно? страница не догрузилась? Без **артефактов** — скриншота, трейса, шагов — разбор превращается в гадание.

## Скриншоты

```python
import os
from pwfake.sync_api import Page

os.makedirs("shots", exist_ok=True)
page = Page()
page.set_content("<h1>Корзина</h1>")
page.screenshot(path="shots/cart.png")
print(os.path.exists("shots/cart.png"))
print(page.screenshot()[:4])
```

Вывод: `True`, затем `b'\x89PNG'` — первые байты любого PNG-файла.

- `page.screenshot(path="…")` — сохранить файл; без `path` — просто вернуть байты PNG (удобно для отчётов).
- `page.screenshot(full_page=True)` — всю страницу, не только видимую область; `locator.screenshot()` — один элемент.
- В pwfake картинка пустая, но формат и API — как у Playwright.

## Скриншот в Allure

```py
import allure

def test_catalog(page):
    page.goto("/catalog")
    allure.attach(page.screenshot(), name="Каталог", attachment_type=allure.attachment_type.PNG)
```

Шаги делают отчёт читаемым сценарием:

```py
with allure.step("Открыть страницу входа"):
    page.goto("/login")
with allure.step("Нажать «Войти»"):
    page.get_by_role("button", name="Войти").click()
```

## Скриншот только при падении

Хук в `conftest.py` срабатывает после каждой фазы теста; в фазе `call` у упавшего теста берём его `page` и прикладываем снимок:

```py
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            allure.attach(page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)
```

- `hookwrapper=True` + `yield` — наш код выполняется **после** того, как pytest сформировал отчёт.
- `item.funcargs` — фикстуры, которые получил тест.

## Встроенные опции pytest-playwright

```bash
pytest --screenshot only-on-failure    # скриншоты упавших тестов в test-results/
pytest --video retain-on-failure       # видео прогона, только у упавших
pytest --tracing retain-on-failure     # трейс, только у упавших
```

## Трейс — лучший артефакт

**Трейс** (`trace.zip`) — запись всего теста: каждое действие, снимок DOM до и после, сеть, консоль, время. Открывается просмотрщиком:

```bash
playwright show-trace test-results/…/trace.zip
```

или на trace.playwright.dev прямо в браузере. Можно «перемотать» тест к любому шагу и посмотреть страницу в тот момент — флаки разбираются в разы быстрее.

## Итог

- Скриншот: `page.screenshot(path=…)` или байты для `allure.attach`.
- Шаги `allure.step` превращают тест в читаемый сценарий.
- Скриншот при падении — хук `pytest_runtest_makereport` или `--screenshot only-on-failure`.
- Трейс (`--tracing retain-on-failure`, `playwright show-trace`) — самый полный артефакт.
'''),
    short=t(r'''
```py
page.screenshot(path="shots/x.png", full_page=True)
allure.attach(page.screenshot(), name="Каталог", attachment_type=allure.attachment_type.PNG)
with allure.step("Открыть страницу входа"): ...
# conftest: pytest_runtest_makereport(item, call) + hookwrapper → скриншот при report.failed
```
```bash
pytest --screenshot only-on-failure --video retain-on-failure --tracing retain-on-failure
playwright show-trace trace.zip
```
'''),
    quiz=[
        q('Что вернёт `page.screenshot()` без аргумента `path`?',
            ['Ничего', 'Байты PNG-картинки', 'Путь к файлу', 'Ошибку'],
            1, 'Байты удобно сразу приложить к отчёту.'),
        q('Какой артефакт позволяет пошагово «перемотать» упавший тест с DOM и сетью?',
            ['Скриншот', 'Лог pytest', 'Трейс Playwright', 'Allure-шаг'],
            2, 'trace.zip + playwright show-trace.'),
        q('Зачем в хуке `pytest_runtest_makereport` проверка `report.when == "call"`?',
            ['Чтобы хук работал быстрее', 'Отчёты есть для setup, call и teardown; падение самого теста — в фазе call', 'Без неё хук не вызовется', 'Для Allure'],
            1, 'Иначе снимок сделается и при ошибках фикстур.'),
    ],
),

# ---------- ui-lists ----------
'ui-lists': dict(
    full=t(r'''
## Зачем это нужно

Каталог, результаты поиска, корзина, таблица заказов — половина проверок UI про **наборы** элементов: сколько их, в каком порядке, что в конкретной строке. Для этого у локатора есть групповые методы.

## Все тексты сразу

```python
from pwfake.sync_api import Page

page = Page()
page.set_content('<ul><li>Мышь — 1200 ₽</li><li>Коврик — 600 ₽</li></ul>')
items = page.get_by_role("listitem")
print(items.count())
print(items.all_inner_texts())
```

Вывод: `2`, `['Мышь — 1200 ₽', 'Коврик — 600 ₽']`.

`all_inner_texts()` и `count()` **не ждут** — на динамической странице сначала дождись элементов (`expect(items).to_have_count(n)` или `wait_for()` на контейнере).

## Перебор элементов

```python
from pwfake.sync_api import Page

page = Page()
page.set_content("""
<div class="card"><h3>Мышь</h3> <span class="price">1200 ₽</span></div>
<div class="card"><h3>Коврик</h3> <span class="price">600 ₽</span></div>
""")
prices = {}
for card in page.locator(".card").all():
    prices[card.locator("h3").inner_text()] = int(card.locator(".price").inner_text().split()[0])
print(prices)
```

Вывод: `{'Мышь': 1200, 'Коврик': 600}`. `.all()` возвращает список локаторов — по одному на элемент, внутри каждого можно искать дальше.

## Проверка порядка

```py
prices = [int(t.split()[0]) for t in page.locator(".card .price").all_inner_texts()]
assert prices == sorted(prices)                               # по возрастанию
expect(page.locator(".card h3")).to_have_text(["Коврик", "Мышь"])   # точный список по порядку
```

## Нужная строка таблицы

```python
from pwfake.sync_api import Page

page = Page()
page.set_content("""
<table>
  <tr><th>Товар</th> <th>Кол-во</th></tr>
  <tr><td>Мышь</td> <td class="qty">2</td> <td><button>Удалить</button></td></tr>
  <tr><td>Коврик</td> <td class="qty">1</td> <td><button>Удалить</button></td></tr>
</table>
""")
row = page.get_by_role("row").filter(has_text="Коврик")
print(row.locator(".qty").inner_text())
print(row.get_by_role("button", name="Удалить").count())
```

Вывод: `1`, `1`. Приём «найди строку по тексту → действуй внутри неё» решает проблему одинаковых кнопок «Удалить».

- `filter(has_text=...)` / `filter(has_not_text=...)` — сузить набор по тексту.
- Роли таблицы: `row`, `cell`, `columnheader`.

## Итог

- `count()`, `all_inner_texts()`, `all()` — для наборов; перед ними дождись загрузки.
- Порядок проверяй списком в `to_have_text([...])` или сравнением с `sorted`.
- Строку ищи по тексту, действие выполняй внутри строки.
'''),
    short=t(r'''
```py
expect(cards).to_have_count(5)                    # сначала дождись
cards.all_inner_texts()                           # ['…', '…']
for card in cards.all(): card.locator("h3").inner_text()
expect(page.locator(".card h3")).to_have_text(["Коврик", "Мышь"])
rows.filter(has_text="Коврик").get_by_role("button", name="Удалить").click()
rows.filter(has_not_text="Нет в наличии")
```
'''),
    quiz=[
        q('Каталог догружается 1 секунду. Что вернёт `page.locator(".card").all_inner_texts()` сразу после `goto`?',
            ['Все названия', 'Пустой список — метод не ждёт', 'Ошибку таймаута', 'None'],
            1, 'Сначала дождись элементов.'),
        q('Как нажать «Удалить» у «Коврика», если такие кнопки в каждой строке?',
            ['`page.get_by_role("button", name="Удалить").click()`', '`rows.filter(has_text="Коврик").get_by_role("button", name="Удалить").click()`', '`page.click("Удалить")`', '`rows.last.click()`'],
            1, 'Строка по тексту → кнопка внутри неё.'),
        q('Что возвращает `locator.all()`?',
            ['Список текстов', 'Список локаторов, по одному на элемент', 'Число элементов', 'HTML страницы'],
            1, 'Внутри каждого можно искать дальше.'),
    ],
),

# ---------- ui-real ----------
'ui-real': dict(
    full=t(r'''
## Зачем это нужно

Всё, что ты писал на pwfake, переносится в настоящий проект почти без изменений: меняется одна строка импорта. Осталось понять, как поставить Playwright, запустить браузер и пользоваться его инструментами.

## Установка

```bash
pip install pytest-playwright          # плагин + сам Playwright
playwright install chromium            # скачать браузер (или просто playwright install — все три)
playwright install --with-deps chromium   # в CI на Linux — вместе с системными библиотеками
```

Импорт в тестах:

```py
from playwright.sync_api import Page, expect
```

## Запуск

```bash
pytest                                  # headless Chromium
pytest --headed                         # видно окно
pytest --headed --slowmo 500            # и каждое действие замедлено на 500 мс
pytest --browser firefox                # другой движок: chromium, firefox, webkit
pytest --browser chromium --browser firefox   # оба — каждый тест дважды
pytest --base-url https://stage.shop.test     # стенд для page.goto("/…")
pytest --device "iPhone 13"             # эмуляция устройства
pytest -n 4                             # параллельно (pytest-xdist)
```

## Скрипт без pytest

```py
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demo.shop.test/catalog")
    print(page.locator(".card h3").all_inner_texts())
    browser.close()
```

Так пишут утилиты: собрать данные, сделать скриншоты, подготовить стенд. В тестах браузером управляет плагин.

## Codegen — запись тестов

```bash
playwright codegen https://demo.shop.test
```

Откроется браузер и окно с кодом: ты кликаешь — Playwright пишет код с хорошими локаторами (`get_by_role`, `get_by_label`). Это быстрый способ подобрать локатор или набросать сценарий; дальше код переносят в Page Object и добавляют проверки.

## Инструменты отладки

- `PWDEBUG=1 pytest -k test_login` — Playwright Inspector: пошаговое выполнение, подсветка локаторов.
- `page.pause()` — поставить точку остановки прямо в тесте.
- `playwright show-trace trace.zip` — просмотр трейса.

## Чем Playwright отличается от Selenium

- Автоожидание встроено — не нужны явные `WebDriverWait`.
- Локаторы по ролям и тексту из коробки, строгий режим.
- Контексты браузера: изоляция тестов без перезапуска браузера — быстро.
- Трейсы, видео, codegen, перехват сети (`page.route`) — в одном инструменте.

## Итог

- `pip install pytest-playwright` + `playwright install`; импорт — `playwright.sync_api`.
- Опции: `--headed`, `--slowmo`, `--browser`, `--base-url`, `--device`.
- `sync_playwright()` — для скриптов, `codegen` — для записи, трейсы и Inspector — для отладки.
'''),
    short=t(r'''
```bash
pip install pytest-playwright && playwright install chromium
pytest --headed --slowmo 500
pytest --browser chromium --browser firefox
pytest --base-url https://stage.shop.test
playwright codegen https://demo.shop.test
PWDEBUG=1 pytest -k login          # Inspector
```
```py
from playwright.sync_api import Page, expect, sync_playwright
```
'''),
    quiz=[
        q('Что нужно сделать после `pip install pytest-playwright`, чтобы тесты запустились?',
            ['Ничего', 'Скачать браузеры: `playwright install`', 'Установить Selenium', 'Перезагрузить компьютер'],
            1, 'Браузеры скачиваются отдельной командой.'),
        q('Какая команда записывает действия в браузере и генерирует код?',
            ['`playwright record`', '`playwright codegen <url>`', '`pytest --record`', '`playwright show-trace`'],
            1, 'codegen.'),
        q('Как перенести тест из заданий CodeQuest в настоящий проект?',
            ['Переписать целиком', 'Заменить импорт `pwfake.sync_api` на `playwright.sync_api` и указать base_url вместо фикстуры app', 'Никак', 'Добавить Selenium'],
            1, 'API одинаковый.'),
    ],
),

# ---------- ui-project ----------
'ui-project': dict(
    full=t(r'''
## Зачем это нужно

Время собрать всё вместе: сквозные (**E2E**) сценарии магазина, регрессионный набор, требования к скорости и баг-репорт. Так выглядит реальная работа автоматизатора UI.

## E2E-сценарий

Сквозной тест проходит путь пользователя от начала до результата — вход → каталог → корзина → оформление → подтверждение:

```py
def test_full_order(page):
    login(page, "anna", "secret")
    add_to_cart(page, "Мышь")
    page.get_by_test_id("cart-link").click()
    page.get_by_role("link", name="Оформить заказ").click()
    fill_checkout(page, name="Аня", phone="+79991234567")
    expect(page.get_by_role("heading")).to_have_text("Заказ оформлен")
```

- Повторяющиеся шаги — во вспомогательные функции, фикстуры или Page Object'ы.
- Таких тестов немного — это самые дорогие тесты набора.

## Регрессионный набор

Регресс — тесты, которые гарантируют, что старое не сломалось. Хороший набор устроен так, что **каждая** поломка роняет хотя бы один тест: сломали вход — упал `test_login_redirect`, сломали поиск — `test_search`. Проверить качество набора можно, как делают задания этой темы: запустить его на заведомо сломанной версии (это называется **мутационное тестирование**).

## Нефункциональные требования

«Каталог грузится не дольше 4 секунд» — тоже проверяемо: передай таймаут в проверку.

```py
expect(page.get_by_test_id("product")).to_have_count(5, timeout=4000)
```

Для серьёзных замеров производительности есть отдельные инструменты (Lighthouse, нагрузочное тестирование), но базовую проверку «не тормозит ли» UI-тест даёт бесплатно.

## Доступ и навигация

- Защищённые страницы без входа должны отправлять на `/login` — это тоже тест.
- После выхода не должно остаться следов пользователя: имени в шапке, доступа к заказам.

## Баг-репорт

Тест упал, баг воспроизведён — заводим репорт. Минимум:

```bash
Баг: «Итого» не учитывает количество
Шаги:
1. Добавить мышь дважды
2. Открыть корзину
Ожидалось: Итого: 2400 ₽
Фактически: Итого: 1200 ₽
```

Плюс окружение (стенд, браузер, версия), серьёзность и вложения — скриншот и трейс из прогона.

## Итог

- E2E — ключевые пути целиком, общие шаги — в хелперы и Page Object'ы.
- Регресс хорош, если ловит каждую поломку; проверить это помогает прогон на сломанной версии.
- Требования к времени — через `timeout` в `expect`.
- Баг-репорт: заголовок, шаги, ожидаемое и фактическое, окружение, артефакты.
'''),
    short=t(r'''
```py
# E2E: вход → каталог → корзина → оформление → подтверждение
expect(page.get_by_test_id("product")).to_have_count(5, timeout=4000)   # требование ко времени
expect(page).to_have_url("http://app.test/login")                        # защищённая страница
expect(page.get_by_test_id("username")).to_have_count(0)                 # после выхода
```
```bash
# баг-репорт: Баг / Шаги 1..n / Ожидалось / Фактически + окружение и скриншот
```
'''),
    quiz=[
        q('Что такое E2E-тест?',
            ['Тест одной функции', 'Сквозной сценарий пользователя через всё приложение', 'Нагрузочный тест', 'Тест API'],
            1, 'End-to-end — от начала до конца.'),
        q('Как проверить требование «каталог грузится не дольше 4 секунд»?',
            ['`page.wait_for_timeout(4000)`', '`expect(...).to_have_count(5, timeout=4000)`', 'Никак', '`time.sleep(4)`'],
            1, 'Проверка упадёт, если не уложились в 4 с.'),
        q('Как понять, что регрессионный набор действительно ловит баги?',
            ['По количеству тестов', 'Запустить его на заведомо сломанной версии: хотя бы один тест должен упасть', 'По времени прогона', 'По покрытию кода'],
            1, 'Мутационное тестирование.'),
    ],
),

}
