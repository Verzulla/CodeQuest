"""Теория модуля «Playwright: первые шаги» темы «Тестирование UI».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- ui-m1-l1 ----------
'ui-m1-l1': dict(
    full=t(r'''
## Зачем это нужно

UI-тест делает то же, что пользователь: открывает страницу, нажимает кнопки, заполняет формы и смотрит на результат. Инструмент для этого — **Playwright**: он управляет настоящим браузером (Chromium, Firefox, WebKit) из Python. Любое действие начинается с вопроса «с каким элементом?». Ответ на него — **локатор**.

## Как устроены задания этой темы

Настоящий браузер в песочнице CodeQuest не запустить, поэтому задания работают на **pwfake** — учебной реализации Playwright без браузера. API тот же, отличается только импорт:

```py
from playwright.sync_api import Page, expect   # настоящий проект
from pwfake.sync_api import Page, expect       # задания CodeQuest
```

Для опытов страницу можно создать прямо так: `page = Page()`, а HTML подставить методом `page.set_content(...)` (он есть и в настоящем Playwright). В тестах страница приходит из фикстуры `page` — об этом дальше.

## Локаторы по смыслу: get_by_*

Playwright советует искать элементы так, как их видит пользователь, — по роли, подписи, тексту:

```python
from pwfake.sync_api import Page

page = Page()
page.set_content("""
<h1>Вход</h1>
<label for="user">Логин</label> <input id="user">
<input type="password" placeholder="Пароль">
<button>Войти</button>
<a href="/help">Помощь</a>
<span data-testid="version">v1.2</span>
""")
print(page.get_by_role("button", name="Войти").inner_text())
print(page.get_by_role("heading").inner_text())
print(page.get_by_label("Логин").get_attribute("id"))
print(page.get_by_placeholder("Пароль").get_attribute("type"))
print(page.get_by_text("Помощь").get_attribute("href"))
print(page.get_by_test_id("version").inner_text())
```

Вывод: `Войти`, `Вход`, `user`, `password`, `/help`, `v1.2`.

- `get_by_role(роль, name=...)` — **главный** локатор. Роль — то, чем элемент является для пользователя: `button`, `link`, `heading`, `textbox`, `checkbox`, `combobox` (выпадающий список), `listitem`, `row`, `cell`, `alert`. Роль берётся из тега (`<button>` → `button`, `<a href>` → `link`, `<h1>`…`<h6>` → `heading`) или из атрибута `role`.
- `get_by_label("Логин")` — поле по тексту его `<label>` (или `aria-label`).
- `get_by_placeholder(...)`, `get_by_text(...)`, `get_by_alt_text(...)` (картинки), `get_by_title(...)`.
- `get_by_test_id("version")` — по атрибуту `data-testid`. Его разработчики добавляют специально для тестов: он не меняется при редизайне.

Текст в `name=` и `get_by_text` по умолчанию ищется **как подстрока без учёта регистра**. Для точного совпадения — `exact=True`.

## CSS-селекторы

`page.locator("...")` принимает CSS: `"#id"`, `".class"`, `"form button"`, `"ul.menu > li"`, `"[name=q]"`, а также `"text=Войти"`. CSS привязан к вёрстке — поменяли класс, и тест сломался. Поэтому порядок предпочтения такой: **роль → подпись/текст → test id → CSS**.

## Несколько элементов

Локатор может найти много элементов. Для чтения это нормально (`count()`, `all_inner_texts()`), а для **действия** — ошибка **strict mode violation**: Playwright не угадывает, какую из кнопок нажать. Уточнить можно так:

```python
from pwfake.sync_api import Page

page = Page()
page.set_content("""
<div class="card"><h3>Мышь</h3> <button>В корзину</button></div>
<div class="card"><h3>Коврик</h3> <button>В корзину</button></div>
""")
buttons = page.get_by_role("button", name="В корзину")
print(buttons.count())
print(page.locator(".card").filter(has_text="Коврик").get_by_role("button").count())
print(buttons.first.is_visible(), buttons.nth(1).is_visible())
```

Вывод: `2`, `1`, `True True`.

- `.filter(has_text=...)` — оставить элементы с текстом; удобно выбрать карточку товара.
- Локаторы вкладываются: `карточка.get_by_role("button")` ищет только внутри карточки.
- `.first`, `.last`, `.nth(i)` — по позиции. Это хрупко (порядок может измениться), используй, когда порядок и есть смысл проверки.

## Локатор — это не элемент

`page.get_by_role(...)` ничего не ищет в момент создания — это «инструкция поиска». Элемент ищется заново при каждом действии или проверке. Поэтому локатор можно создать заранее (например, в Page Object), а страница за это время может перерисоваться.

## Итог

- Предпочитай `get_by_role` с `name=`, затем `get_by_label` / `get_by_text`, затем `get_by_test_id`, и только потом CSS.
- Несколько совпадений при действии — ошибка; сужай через `filter` и вложенные локаторы.
- Локатор ленивый: ищет элемент в момент использования.
'''),
    short=t(r'''
```py
page.get_by_role("button", name="Войти")    # роли: button link heading textbox checkbox combobox row cell alert
page.get_by_label("Логин")                  # поле по <label>
page.get_by_placeholder("Поиск")
page.get_by_text("Готово", exact=True)      # по умолчанию — подстрока без регистра
page.get_by_test_id("cart")                 # data-testid
page.locator("ul.menu > li")                # CSS — в крайнем случае
loc.filter(has_text="Мышь").get_by_role("button")   # сузить
loc.first / loc.last / loc.nth(1) / loc.count()
```
'''),
    quiz=[
        q('Какой локатор Playwright рекомендует в первую очередь?',
            ['`page.locator("div > div:nth-child(2) button")`', '`page.get_by_role("button", name="Войти")`', 'XPath по полному пути', '`page.locator(".btn-primary")`'],
            1, 'Роль и доступное имя — так элемент видит пользователь, и это переживает редизайн.'),
        q('Локатор нашёл две кнопки «В корзину», и ты вызываешь `.click()`. Что будет?',
            ['Нажмётся первая', 'Нажмутся обе', 'Ошибка strict mode violation', 'Нажмётся случайная'],
            2, 'Для действий Playwright требует ровно один элемент — уточни локатор.'),
        q('Зачем разработчики добавляют атрибут `data-testid`?',
            ['Для стилей', 'Чтобы у тестов был стабильный локатор, не зависящий от вёрстки', 'Для SEO', 'Он ускоряет страницу'],
            1, 'test id меняется только осознанно.'),
    ],
),

# ---------- ui-m1-l2 ----------
'ui-m1-l2': dict(
    full=t(r'''
## Зачем это нужно

Страница загружается не мгновенно: данные приходят с сервера, кнопки появляются после анимации, спиннер висит полсекунды. Тест, который проверяет элемент «слишком рано», падает — хотя баги нет. А если ждать фиксированное время, тест то проходит, то падает, в зависимости от нагрузки. Такие тесты называют **флаки** (flaky), и это главная беда UI-автоматизации.

## Автоожидание Playwright

Каждое **действие** (`click`, `fill`, `check`…) и каждая проверка **`expect`** сами ждут, пока элемент появится, станет видимым и доступным. По умолчанию — до **5 секунд**. Опрос идёт постоянно, поэтому тест продолжается сразу, как только условие выполнилось.

```python
from pwfake.sync_api import Page, expect

page = Page()
page.set_content('<p id="msg" data-appear-after="1200">Заказ создан</p>')
print(page.locator("#msg").is_visible())
expect(page.locator("#msg")).to_have_text("Заказ создан")
print(page.clock)
```

Вывод: `False`, затем `1200`.

- `data-appear-after="1200"` — так в pwfake элемент «догружается» через 1200 мс; `data-disappear-after` — исчезает. `page.clock` — фейковые часы страницы: время идёт, только пока тест ждёт.
- `is_visible()` и `count()` **не ждут** — они отвечают про текущий момент. Для проверок используй `expect`, для чтения списков — сначала дождись элементов.

## Как ждать правильно

```py
expect(page.get_by_test_id("product")).to_have_count(5)   # ждёт, пока карточек станет 5
page.locator("#products").wait_for()                     # ждёт появления блока
page.get_by_role("button", name="Оплатить").click()      # ждёт кнопку сам
page.locator(".card h3").all_inner_texts()                # не ждёт! только после ожидания
```

И как **не** надо:

```py
page.wait_for_timeout(2000)   # «поспать 2 секунды» — медленно и всё равно ненадёжно
```

Фиксированная пауза либо слишком длинная (тесты медленные), либо слишком короткая (на медленном CI не хватит). В реальном Playwright `wait_for_timeout` оставляют только для отладки.

## Таймауты

Если условие так и не выполнилось, действие бросает `TimeoutError`, а `expect` — `AssertionError` с пояснением «ожидалось / фактически». Таймаут можно задать точечно — `click(timeout=1000)`, `expect(...).to_be_visible(timeout=10_000)` — или для всей страницы: `page.set_default_timeout(...)`.

## Откуда берутся флаки

- **Ранняя проверка** без ожидания — лечится `expect` и автоожиданием.
- **Зависимость тестов друг от друга**: один тест оставил товар в корзине — другой упал. Каждый тест должен сам готовить данные.
- **Нестабильное окружение**: медленный стенд, сеть, общая база.
- **Хрупкие локаторы**, завязанные на порядок и вёрстку.

## Перезапуски

Плагин **pytest-rerunfailures** перезапускает упавший тест: `pytest --reruns 2`. Это пластырь, а не лечение: он прячет нестабильность. Хорошая практика — собирать статистику: тест, который в истории и проходил, и падал, — флаки, его нужно чинить.

## Итог

- Действия и `expect` ждут сами (до 5 с); `count()`/`is_visible()`/`all_inner_texts()` — нет.
- Жди условия (`expect`, `wait_for`), а не времени (`wait_for_timeout`).
- Флаки лечат причину: ожидания, независимость тестов, стабильные локаторы. Перезапуски — временная мера.
'''),
    short=t(r'''
```py
expect(loc).to_be_visible()             # ждёт до 5 с
expect(loc).to_have_count(5)            # ждёт нужное количество
loc.wait_for()                          # ждёт появления
loc.click(timeout=1000)                 # свой таймаут → TimeoutError
loc.count(), loc.is_visible()           # НЕ ждут
page.wait_for_timeout(2000)             # ✗ фиксированная пауза — источник флаки
# pytest --reruns 2                     # pytest-rerunfailures, временная мера
```
'''),
    quiz=[
        q('Что из этого НЕ ждёт появления элемента?',
            ['`loc.click()`', '`expect(loc).to_be_visible()`', '`loc.count()`', '`loc.fill("x")`'],
            2, '`count()` возвращает количество прямо сейчас.'),
        q('Почему `page.wait_for_timeout(2000)` перед проверкой — плохая идея?',
            ['Такого метода нет', 'Пауза то слишком длинная, то слишком короткая: тест медленный и нестабильный', 'Она ломает браузер', 'Она не работает в headless'],
            1, 'Жди условие, а не время.'),
        q('Тест в истории и проходил, и падал без изменений в коде. Как он называется?',
            ['Смоук', 'Флаки', 'Регрессионный', 'Параметризованный'],
            1, 'Flaky — нестабильный тест.'),
    ],
),

# ---------- ui-actions ----------
'ui-actions': dict(
    full=t(r'''
## Зачем это нужно

Проверить страницу — полдела; пользователь с ней **взаимодействует**: вводит логин, отмечает согласие, выбирает доставку, нажимает «Оформить». UI-тест повторяет эти действия через методы локатора.

## Поля ввода

```python
from pwfake.sync_api import Page

page = Page()
page.set_content('<input name="q" value="старое">')
box = page.locator("input")
box.fill("мышь")
print(box.input_value())
box.clear()
print(repr(box.input_value()))
```

Вывод: `мышь`, затем `''`.

- `fill(text)` — очищает поле и вводит текст целиком (как вставка).
- `clear()` — очистить; `input_value()` — прочитать текущее значение.
- `press_sequentially("abc")` — печатать по символу, если сайт реагирует на каждое нажатие (подсказки поиска).
- `press("Enter")` — нажать клавишу. Enter в поле формы отправляет форму, как в браузере.

## Кнопки и ссылки

- `click()` — нажать. Ссылка переходит по `href`, кнопка `type="submit"` отправляет форму со всеми её полями.
- Недоступную (`disabled`) кнопку нажать нельзя — Playwright будет ждать, пока она станет доступной, а потом упадёт по таймауту. В pwfake нажатие недоступной кнопки сразу даёт ошибку.
- `hover()` — навести мышь (открыть меню).

## Чекбоксы, радиокнопки, списки

```python
from pwfake.sync_api import Page

page = Page()
page.set_content("""
<label><input type="checkbox" name="agree"> Согласен</label>
<label for="d">Доставка</label>
<select id="d"><option value="courier">Курьер</option><option value="pickup">Самовывоз</option></select>
""")
page.get_by_label("Согласен").check()
print(page.get_by_label("Согласен").is_checked())
print(page.get_by_label("Доставка").select_option("pickup"))
print(page.get_by_label("Доставка").input_value())
```

Вывод: `True`, `['pickup']`, `pickup`.

- `check()` / `uncheck()` — поставить или снять галочку (повторный `check()` ничего не ломает, в отличие от `click()`).
- `select_option("pickup")` — выбрать по `value`; `select_option(label="Самовывоз")` — по видимому тексту. Возвращает список выбранных значений.

## Навигация

- `page.goto("/login")` — открыть страницу. Относительный путь дописывается к `base_url` (в заданиях — `http://app.test`).
- `page.url`, `page.title()` — текущий адрес и заголовок вкладки.
- `page.go_back()`, `page.reload()`.

## Сценарий целиком

```py
def test_login_success(page):
    page.goto("/login")
    page.get_by_label("Логин").fill("anna")
    page.get_by_label("Пароль").fill("secret")
    page.get_by_role("button", name="Войти").click()
    expect(page).to_have_url("http://app.test/catalog")
```

## Демо-сайт заданий

Задания тестируют учебный магазин `pwfake.demo.shop_app()`:

- `/login` — вход (`anna` / `secret`, `boris` / `qwerty123`, заблокированный `blocked`);
- `/catalog` — карточки товаров `data-testid="product"`, поиск (плейсхолдер «Поиск»), сортировка, кнопки «В корзину». Товары догружаются через 800 мс;
- `/cart` — строки `data-testid="cart-row"`, `#total`, ссылка «Оформить заказ»;
- `/checkout` — форма заказа; шапка — ссылка корзины `data-testid="cart-link"` и имя `data-testid="username"`.

Проверки запускают твои тесты и на **сломанных** версиях сайта (`shop_app(bug="...")`): хороший тест должен их поймать.

## Итог

- `fill`/`clear`/`press` — поля; `click` — кнопки и ссылки; `check`/`select_option` — галочки и списки.
- Все действия сами ждут элемент.
- После действия — проверка результата: адрес, текст, состояние.
'''),
    short=t(r'''
```py
page.goto("/login"); page.url; page.title(); page.go_back()
loc.fill("текст"); loc.clear(); loc.input_value()
loc.press("Enter")                      # в форме — отправка
loc.click(); loc.hover()
loc.check(); loc.uncheck(); loc.is_checked()
loc.select_option("pickup")             # по value
loc.select_option(label="Самовывоз")    # по тексту
```
'''),
    quiz=[
        q('Чем `fill("abc")` отличается от `press_sequentially("abc")`?',
            ['Ничем', '`fill` вставляет текст целиком, заменяя старый; `press_sequentially` печатает по символу', '`fill` работает только с паролями', '`press_sequentially` очищает поле'],
            1, 'Посимвольный ввод нужен, когда сайт реагирует на каждое нажатие.'),
        q('Как выбрать в `<select>` вариант с текстом «Самовывоз» и value `pickup`?',
            ['`select_option("Самовывоз", "pickup")`', '`select_option("pickup")` или `select_option(label="Самовывоз")`', '`click("Самовывоз")`', '`fill("pickup")`'],
            1, 'По value — позиционно, по тексту — `label=`.'),
        q('Почему для галочки лучше `check()`, а не `click()`?',
            ['`click` не работает с чекбоксами', '`check` гарантирует состояние «отмечено», а повторный `click` снимет галочку', '`check` быстрее', 'Разницы нет'],
            1, '`check()` идемпотентен.'),
    ],
),

# ---------- ui-expect ----------
'ui-expect': dict(
    full=t(r'''
## Зачем это нужно

Тест без проверки — просто скрипт, который кликает. Проверять состояние страницы обычным `assert page.locator(...).inner_text() == ...` можно, но такой assert не ждёт: если текст обновится через 300 мс, тест упадёт. В Playwright для этого есть **`expect`** — проверки с автоожиданием.

## Как работает expect

```python
from pwfake.sync_api import Page, expect

page = Page()
page.set_content('<p id="status" data-appear-after="500">Оплачено</p>')
expect(page.locator("#status")).to_have_text("Оплачено")
print("ok", page.clock)
try:
    expect(page.locator("#status")).to_have_text("Отменён", timeout=200)
except AssertionError as e:
    print(e)
```

Вывод: `ok 500`, затем `ожидалось: текст 'Отменён'; фактически: 'Оплачено' (ждали 200 мс)`.

`expect` повторяет проверку, пока она не пройдёт или не выйдет таймаут (5 с), и только тогда падает с понятным сообщением. (В настоящем Playwright текст сообщения английский, но смысл тот же.)

## Проверки локатора

- `to_be_visible()` / `to_be_hidden()` — виден ли элемент;
- `to_have_text("…")` — текст **целиком** (пробелы по краям не важны); можно регулярное выражение `re.compile(...)` или список — по тексту на каждый элемент;
- `to_contain_text("…")` — текст содержит подстроку;
- `to_have_count(n)` — сколько элементов нашёл локатор;
- `to_have_value("…")` — значение поля;
- `to_be_enabled()` / `to_be_disabled()`, `to_be_checked()`;
- `to_have_attribute("href", "/help")`, `to_have_class("btn primary")`.

## Проверки страницы

```py
expect(page).to_have_url("http://app.test/catalog")
expect(page).to_have_url(re.compile(r"/catalog"))
expect(page).to_have_title("Каталог")
```

## Отрицание

Перед любым методом можно поставить `not_`: `expect(loc).not_to_be_visible()`, `expect(loc).not_to_have_text("Ошибка")`. Отрицание тоже ждёт — пока условие не **перестанет** выполняться. Не пиши `assert not loc.is_visible()`: спиннер может ещё не исчезнуть.

## Негативные тесты

Хороший набор проверяет не только «всё работает», но и «ошибки показываются»: неверный пароль → сообщение, пустое поле → подсказка, товара нет → кнопка недоступна.

```py
def test_wrong_password(page):
    page.goto("/login")
    page.get_by_label("Логин").fill("anna")
    page.get_by_label("Пароль").fill("wrong")
    page.get_by_role("button", name="Войти").click()
    expect(page.get_by_role("alert")).to_have_text("Неверный логин или пароль")
```

## Итог

- Для проверок UI — `expect(...)`, а не голый `assert`: он ждёт и объясняет падение.
- `to_have_text` — целиком, `to_contain_text` — подстрока, список — для нескольких элементов по порядку.
- `not_to_…` — ждущие отрицания.
- Проверяй и позитивные, и негативные сценарии.
'''),
    short=t(r'''
```py
expect(loc).to_be_visible() / to_be_hidden()
expect(loc).to_have_text("Итого: 1800 ₽")        # целиком; или re.compile, или список
expect(loc).to_contain_text("1800")
expect(loc).to_have_count(3)
expect(loc).to_have_value("anna")
expect(loc).to_be_disabled() / to_be_checked()
expect(loc).not_to_be_visible()                  # ждущее отрицание
expect(page).to_have_url("http://app.test/catalog")
expect(page).to_have_title("Каталог")
```
'''),
    quiz=[
        q('Чем `expect(loc).to_have_text("X")` лучше `assert loc.inner_text() == "X"`?',
            ['Ничем', 'Он ждёт, пока текст станет нужным, и даёт понятное сообщение при падении', 'Он быстрее', 'Он не требует локатора'],
            1, 'Автоожидание — главное отличие.'),
        q('Текст элемента — «Итого: 1800 ₽». Какая проверка пройдёт?',
            ['`to_have_text("1800")`', '`to_contain_text("1800")`', '`to_have_count(1800)`', '`to_have_value("1800")`'],
            1, '`to_have_text` сравнивает текст целиком.'),
        q('Как проверить, что спиннер исчез?',
            ['`assert not spinner.is_visible()`', '`expect(spinner).not_to_be_visible()`', '`spinner.count() == 0`', '`page.wait_for_timeout(1000)`'],
            1, 'Отрицание в expect ждёт исчезновения.'),
    ],
),

}
