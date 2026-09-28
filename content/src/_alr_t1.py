"""Теория модуля «Allure в тестах» темы «Allure и отчёты».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- alr-intro ----------
'alr-intro': dict(
    full=t(r'''
## Зачем это нужно

Вывод pytest в терминале удобен разработчику, но менеджеру, аналитику или коллеге нужен понятный отчёт: сколько тестов прошло, что упало, на каком шаге, со скриншотами и логами, с историей прошлых прогонов. **Allure Report** — самый популярный формат отчётов об автотестах. Его ждут почти во всех вакансиях QA Automation.

## Как это устроено

1. Плагин **allure-pytest** во время прогона пишет сырые результаты: по JSON-файлу на тест, вложения, контейнеры фикстур — в папку `allure-results`.
2. Утилита **Allure** (командная строка, работает на Java) превращает эти файлы в HTML-отчёт.

## Подключение

```bash
$ pip install allure-pytest
$ pytest --alluredir=allure-results
$ ls allure-results
1b2c-result.json  7f8e-result.json  3d4e-container.json  5c6d-attachment.png
```

- `--alluredir=папка` — куда складывать результаты. Без этого флага плагин ничего не пишет.
- Один `*-result.json` — один тест (со статусом, шагами, метками); `*-container.json` — фикстуры; `*-attachment.*` — вложения.
- Результаты накапливаются между прогонами. Чтобы отчёт был только по последнему прогону, папку очищают: `--clean-alluredir`.

## Отчёт

```bash
$ allure serve allure-results
$ allure generate allure-results -o allure-report --clean
$ allure open allure-report
```

- `allure serve` — сгенерировать во временную папку и сразу открыть в браузере. Удобно локально.
- `allure generate … -o папка --clean` — сохранить отчёт (для CI, публикации). `--clean` — очистить папку перед генерацией.
- `allure open` — открыть готовый отчёт (он запускает локальный веб-сервер: открыть `index.html` просто двойным кликом не получится).
- Установка утилиты: нужна Java; дальше `brew install allure`, `scoop install allure` или архив с GitHub.

## Что внутри отчёта

- **Overview** — сводка, графики, окружение, тренды истории.
- **Suites** — дерево тестов по файлам и классам.
- **Behaviors** — дерево по epic/feature/story.
- **Graphs**, **Timeline** — статистика и время выполнения, в том числе параллельного.
- У каждого теста: шаги, вложения, параметры, метки, ссылки, история.

## Итог

- `allure-pytest` + `pytest --alluredir=allure-results` — сырые результаты.
- `allure serve` — посмотреть; `allure generate -o … --clean` — сохранить; `allure open` — открыть.
- Утилите `allure` нужна Java.
- Один `*-result.json` = один тест.
'''),
    short=t(r'''
```bash
pip install allure-pytest
pytest --alluredir=allure-results [--clean-alluredir]
allure serve allure-results                       # сразу в браузере
allure generate allure-results -o allure-report --clean
allure open allure-report
# *-result.json — тест, *-container.json — фикстуры, *-attachment.* — вложения
```
'''),
    quiz=[
        q('Что делает флаг `--alluredir`?',
            ['Генерирует HTML', 'Указывает папку для сырых результатов Allure', 'Открывает отчёт', 'Устанавливает Allure'],
            1, 'HTML строит утилита allure.'),
        q('Чем `allure serve` отличается от `allure generate`?',
            ['Ничем', 'serve генерирует во временную папку и сразу открывает', 'generate открывает браузер', 'serve только для CI'],
            1, 'generate сохраняет отчёт в папку.'),
        q('Что нужно установить для команды `allure`?',
            ['Node.js', 'Java', 'Docker', 'Go'],
            1, 'Allure Commandline работает на Java.'),
    ],
),

# ---------- alr-steps ----------
'alr-steps': dict(
    full=t(r'''
## Зачем это нужно

Когда падает длинный UI- или API-тест, из трассировки не всегда понятно, где именно: на входе, в корзине или при оплате? **Шаги** делят тест на понятные действия. В отчёте видно, какие шаги прошли, на каком упало, и сколько каждый занял — тест читается как сценарий, даже без знания кода.

## Контекстный менеджер

```py
import allure


def test_login():
    with allure.step("Открыть страницу входа"):
        page.open()
    with allure.step("Ввести логин и пароль"):
        page.login("anna", "secret")
    with allure.step("Проверить приветствие"):
        assert page.greeting() == "Привет, anna"
```

- Всё, что выполняется внутри `with allure.step("…")`, попадает в этот шаг.
- Статус шага — как у кода внутри: упал `assert` — шаг `failed`, остальные шаги после него не выполняются.

## Вложенные шаги

```py
with allure.step("Оформить заказ"):
    with allure.step("Заполнить адрес"):
        ...
    with allure.step("Оплатить"):
        ...
```

- Вложенность отображается деревом — удобно для крупных сценариев.

## Декоратор

```py
@allure.step("Добавить {item} в корзину")
def add_to_cart(item):
    ...


class LoginPage:
    @allure.step("Войти как {user}")
    def login(self, user):
        ...
```

- Каждый вызов функции становится шагом. `{имя}` в названии заменяется значением параметра (строки подставляются через `repr`, с кавычками: `Войти как 'anna'`).
- Так шаги встраивают в **Page Object** и клиенты API: тест остаётся коротким, а отчёт — подробным.

## Статусы в отчёте

- `passed` — прошёл.
- `failed` — не прошла проверка (`AssertionError`) — вероятно, баг продукта.
- `broken` — любое другое исключение: ошибка в тесте, в окружении, таймаут.
- `skipped` — пропущен.

## Итог

- `with allure.step("…")` — шаг; вложенные шаги — дерево.
- `@allure.step("… {param} …")` — каждый вызов функции — шаг.
- Шаги в Page Object и API-клиентах делают отчёт читаемым.
- failed — проверка, broken — другое исключение.
'''),
    short=t(r'''
```py
with allure.step("Открыть страницу"):
    page.open()

@allure.step("Войти как {user}")
def login(user): ...

with allure.step("Заказ"):
    with allure.step("Оплатить"): ...
# failed — assert, broken — другое исключение
```
'''),
    quiz=[
        q('Какой статус будет у теста, упавшего на `assert`?',
            ['broken', 'failed', 'skipped', 'passed'],
            1, 'broken — другие исключения.'),
        q('Что подставится в `@allure.step("Войти как {user}")` при вызове `login("anna")`?',
            ['{user}', "'anna'", 'user', 'Ничего'],
            1, 'Значение параметра через repr.'),
        q('Выполнятся ли шаги после упавшего шага?',
            ['Да', 'Нет, тест прерывается', 'Только вложенные', 'Только в CI'],
            1, 'Исключение прерывает тест.'),
    ],
),

# ---------- alr-attach ----------
'alr-attach': dict(
    full=t(r'''
## Зачем это нужно

Упавший UI-тест без скриншота — загадка; упавший API-тест без тела запроса и ответа — повод перезапускать. **Вложения** сохраняют в отчёте доказательства: логи, JSON, HTML страницы, скриншоты, видео. Разработчик видит всё нужное, не запуская тест.

## allure.attach

```py
import json
import allure


def test_api():
    body = {"id": 1, "status": "active"}
    allure.attach(json.dumps(body, ensure_ascii=False), name="response",
                  attachment_type=allure.attachment_type.JSON)
    allure.attach("GET /users -> 200", name="request", attachment_type=allure.attachment_type.TEXT)
```

- `allure.attach(содержимое, name=…, attachment_type=…)` — строка или байты.
- Типы: `TEXT`, `JSON`, `HTML`, `XML`, `CSV`, `PNG`, `JPG`, `MP4` и другие. От типа зависит, как вложение покажется в отчёте.
- Вложение внутри `with allure.step(...)` привязывается к этому шагу.

## allure.attach.file

```py
def test_file(tmp_path):
    path = tmp_path / "report.csv"
    path.write_text("id,status\n1,ok\n", encoding="utf-8")
    allure.attach.file(path, name="report", attachment_type=allure.attachment_type.CSV)
```

- Приложить существующий файл: лог сервера, выгрузку, скачанный документ, видео.

## Скриншот при падении

```py
# conftest.py
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(page.screenshot(), name="screenshot",
                          attachment_type=allure.attachment_type.PNG)
```

- Хук `pytest_runtest_makereport` вызывается после каждого этапа теста (setup, call, teardown). `report.failed` на этапе `call` — тест упал.
- `item.funcargs` — фикстуры теста; из них берём браузерную страницу и делаем скриншот.
- Подробно хуки разберём в практическом уроке модуля 3.

## Что прикладывать

- API: метод, URL, заголовки (без секретов!), тело запроса, статус и тело ответа.
- UI: скриншот, HTML страницы, логи консоли браузера, видео.
- Всегда: логи приложения за время теста.
- Не прикладывай пароли и токены — отчёты читают многие.

## Итог

- `allure.attach(данные, name, attachment_type)`; внутри шага — к шагу.
- `allure.attach.file(путь, …)` — готовый файл.
- Скриншот при падении — хук `pytest_runtest_makereport` в conftest.
- Секреты не прикладывать.
'''),
    short=t(r'''
```py
allure.attach(json.dumps(body), name="response", attachment_type=allure.attachment_type.JSON)
allure.attach("text", name="log", attachment_type=allure.attachment_type.TEXT)
allure.attach(png_bytes, name="screenshot", attachment_type=allure.attachment_type.PNG)
allure.attach.file(path, name="report", attachment_type=allure.attachment_type.CSV)
# внутри with allure.step(...) — вложение шага
# скриншот при падении — pytest_runtest_makereport в conftest
```
'''),
    quiz=[
        q('Куда попадёт вложение, сделанное внутри `with allure.step(...)`?',
            ['В тест целиком', 'В этот шаг', 'В отдельный отчёт', 'Никуда'],
            1, 'Вложение привязывается к текущему шагу.'),
        q('Какой тип вложения выбрать для скриншота?',
            ['TEXT', 'PNG', 'JSON', 'HTML'],
            1, 'attachment_type.PNG.'),
        q('Что нельзя прикладывать к отчёту?',
            ['Скриншоты', 'Тела ответов', 'Пароли и токены', 'Логи'],
            2, 'Отчёты видят многие.'),
    ],
),

# ---------- alr-labels ----------
'alr-labels': dict(
    full=t(r'''
## Зачем это нужно

В отчёте на тысячу тестов нужно быстро понять: что сломалось в «Корзине», какие упали критичные тесты, какие связаны с багом BUG-42. **Метки** (labels) и **ссылки** (links) делают отчёт структурированным: группировка по функциональности, приоритеты, связь с задачами и тест-кейсами.

## Название и описание

```py
@allure.title("Вход с правильным паролем")
@allure.description("Проверяем успешный вход и приветствие")
def test_login():
    ...
```

- `title` — человекочитаемое название вместо `test_login`.
- `description` — описание (есть `description_html`). Docstring теста тоже станет описанием.

## Важность

```py
@allure.severity(allure.severity_level.CRITICAL)
def test_payment():
    ...
```

- Уровни: `BLOCKER`, `CRITICAL`, `NORMAL` (по умолчанию), `MINOR`, `TRIVIAL`.
- В отчёте можно отфильтровать упавшие критичные тесты — с них начинают разбор.

## Группировка: epic, feature, story

```py
@allure.epic("Магазин")
@allure.feature("Корзина")
class TestCart:
    @allure.story("Добавление товара")
    def test_add(self):
        ...

    @allure.story("Удаление товара")
    def test_remove(self):
        ...
```

- Три уровня бизнес-структуры: эпик → функциональность → пользовательская история. Вкладка **Behaviors** показывает дерево по ним.
- Декоратор на классе применяется ко всем его тестам.
- `@allure.tag("smoke")` — теги; `@allure.label("owner", "qa-team")` — любая своя метка.

## Ссылки

```py
@allure.testcase("https://tms/TC-15", "TC-15")
@allure.issue("https://tracker/BUG-42", "BUG-42")
@allure.link("https://docs/cart", name="Требования")
def test_refund():
    ...
```

- Ссылки на тест-кейс, баг и любые страницы кликабельны в отчёте.
- В `pytest.ini` можно задать шаблоны: `--allure-link-pattern=issue:https://tracker/{}`, тогда достаточно `@allure.issue("BUG-42")`.

## Динамически

```py
@pytest.mark.parametrize("role", ["admin", "qa"])
def test_role(role):
    allure.dynamic.title(f"Доступ для роли {role}")
    allure.dynamic.severity(allure.severity_level.CRITICAL if role == "admin" else allure.severity_level.NORMAL)
```

- `allure.dynamic.title / description / severity / feature / tag / label / link` — задать внутри теста, когда значение зависит от данных.
- Параметры parametrize Allure показывает сам в блоке Parameters.

## Итог

- `@allure.title`, `@allure.description`, `@allure.severity(...)`.
- `epic` → `feature` → `story` — дерево Behaviors; `tag`, `label` — свои метки.
- `testcase`, `issue`, `link` — ссылки.
- `allure.dynamic.*` — метки внутри теста.
'''),
    short=t(r'''
```py
@allure.title("Вход с правильным паролем")
@allure.description("…")
@allure.severity(allure.severity_level.CRITICAL)   # blocker critical normal minor trivial
@allure.epic("Магазин") @allure.feature("Корзина") @allure.story("Оплата")
@allure.tag("smoke")   @allure.label("owner", "qa")
@allure.testcase(url, "TC-15")  @allure.issue(url, "BUG-42")  @allure.link(url, name=…)
allure.dynamic.title(f"… {param}")
```
'''),
    quiz=[
        q('Какой severity у теста по умолчанию?',
            ['critical', 'normal', 'minor', 'blocker'],
            1, 'Если метка не указана.'),
        q('В каком порядке идут уровни группировки?',
            ['story → feature → epic', 'epic → feature → story', 'feature → epic → story', 'tag → story → epic'],
            1, 'От крупного к мелкому.'),
        q('Как задать название теста в зависимости от параметра?',
            ['@allure.title с f-строкой', 'allure.dynamic.title(...) внутри теста', 'ids=', 'Нельзя'],
            1, 'Декоратор вычисляется до параметров.'),
    ],
),

}
