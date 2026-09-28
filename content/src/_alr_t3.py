"""Теория модуля «Отчёты в CI и на сервере» темы «Allure и отчёты».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- alr-ci ----------
'alr-ci': dict(
    full=t(r'''
## Зачем это нужно

Автотесты по-настоящему работают в **CI**: после каждого push или по расписанию. Отчёт должен сохраняться автоматически и быть доступен по ссылке — иначе упавший ночной прогон никто не разберёт. Подробно CI разберём в отдельной теме, здесь — всё про отчёты.

## GitHub Actions

```bash
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --locked
      - run: uv run pytest --alluredir=allure-results
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: allure-results
          path: allure-results
```

- Каждый элемент `steps` — шаг: `uses` — готовое действие, `run` — команда.
- Если тесты упали, шаг `pytest` вернёт код 1, и следующие шаги по умолчанию **не выполнятся**. `if: always()` заставляет выполнить шаг загрузки в любом случае — без него отчёт об упавшем прогоне потеряется.
- `upload-artifact` сохраняет папку как артефакт прогона — её можно скачать со страницы запуска. Следующий job скачивает её через `actions/download-artifact@v4` и генерирует отчёт.

## Публикация

- Отчёт — статический сайт. Его публикуют на **GitHub Pages** (ветка `gh-pages`) или **GitLab Pages**, сохраняя папку `history` между запусками — так появляются тренды.
- Для этого есть готовые действия, например `simple-elf/allure-report-action`, и шаг `peaceiris/actions-gh-pages`.

## GitLab CI

```bash
tests:
  image: python:3.12
  script:
    - pip install -r requirements.txt
    - pytest --alluredir=allure-results --junitxml=report.xml
  artifacts:
    when: always
    paths:
      - allure-results
    reports:
      junit: report.xml
```

- `artifacts: when: always` — сохранить и при падении.
- `reports: junit` — GitLab покажет результаты тестов прямо в merge request.

## Итог

- `pytest --alluredir` → артефакт `allure-results` с `if: always()` / `when: always`.
- Отдельный шаг генерирует отчёт; публикация — Pages, история — между запусками.
- JUnit XML — для встроенного отображения в CI.
'''),
    short=t(r'''
```bash
# GitHub Actions
- run: uv run pytest --alluredir=allure-results
- uses: actions/upload-artifact@v4
  if: always()
  with: {name: allure-results, path: allure-results}
# GitLab
artifacts:
  when: always
  paths: [allure-results]
  reports: {junit: report.xml}
```
'''),
    quiz=[
        q('Зачем `if: always()` у шага загрузки отчёта?',
            ['Для скорости', 'Чтобы отчёт сохранился и при упавших тестах', 'Чтобы тесты не падали', 'Для истории'],
            1, 'Иначе после падения шаги пропускаются.'),
        q('Где удобно публиковать HTML-отчёт Allure бесплатно?',
            ['В README', 'GitHub Pages / GitLab Pages', 'В issue', 'В Docker Hub'],
            1, 'Это статический сайт.'),
        q('Что делает `reports: junit` в GitLab CI?',
            ['Генерирует Allure', 'Показывает результаты тестов в merge request', 'Удаляет отчёт', 'Запускает тесты'],
            1, 'Встроенная поддержка JUnit XML.'),
    ],
),

# ---------- alr-server ----------
'alr-server': dict(
    full=t(r'''
## Зачем это нужно

Статический отчёт — снимок одного прогона. Когда тестов тысячи, а прогонов — десятки в день, нужен **сервер отчётов**: хранит историю всех запусков, показывает тренды и флаки, объединяет прогоны из разных CI-задач, связывает тесты с тест-кейсами. Результаты отправляют туда из CI через HTTP API.

## Варианты

- **Allure TestOps** — коммерческая платформа от авторов Allure: история, тест-кейсы, ручные и автотесты вместе, аналитика. Результаты загружает утилита `allurectl upload allure-results`.
- **allure-docker-service** — открытый сервер: принимает результаты по API и генерирует отчёты с историей. Запускается одной командой в Docker.
- **ReportPortal** — открытая платформа с анализом падений.

## allure-docker-service

```bash
$ docker run -d -p 5050:5050 frankescobar/allure-docker-service
```

- Сервер слушает порт 5050. Результаты отправляют POST-запросом, отчёт генерируют GET-запросом.

## Отправка результатов из Python

```py
import base64
import requests
from pathlib import Path


def build_payload(folder):
    return {"results": [
        {"file_name": p.name, "content_base64": base64.b64encode(p.read_bytes()).decode()}
        for p in sorted(Path(folder).iterdir()) if p.is_file()
    ]}


response = requests.post(
    "https://reports.test/allure-docker-service/send-results",
    params={"project_id": "api"},
    json=build_payload("allure-results"),
    timeout=30,
)
response.raise_for_status()
```

- Каждый файл результатов кодируется в **base64** — это способ передать байты (картинки!) внутри JSON.
- `params` — параметры строки запроса (`?project_id=api`), `json` — тело, `timeout` — не ждать вечно.
- `raise_for_status()` — исключение, если сервер ответил 4xx/5xx.
- Затем `GET …/generate-report?project_id=api` — сервер вернёт ссылку на новый отчёт.

## Тестирование такого кода

В песочнице (и в юнит-тестах) нет сети. HTTP-ответы подменяют библиотекой **responses**:

```py
import responses


@responses.activate
def test_send():
    responses.post("https://reports.test/allure-docker-service/send-results?project_id=api",
                   json={"meta_data": {"message": "ok"}})
    assert send_results("https://reports.test", "api", {"results": []})["meta_data"]["message"] == "ok"
```

- Подробно — в теме «Тестирование API».

## Итог

- Сервер отчётов — история, тренды, флаки, объединение прогонов.
- Allure TestOps (`allurectl upload`), allure-docker-service, ReportPortal.
- Отправка: POST с файлами в base64; генерация отчёта — GET.
- Код с HTTP тестируют через подмену ответов (`responses`).
'''),
    short=t(r'''
```bash
docker run -d -p 5050:5050 frankescobar/allure-docker-service
allurectl upload allure-results                # Allure TestOps
```
```py
payload = {"results": [{"file_name": p.name,
                        "content_base64": base64.b64encode(p.read_bytes()).decode()} for p in files]}
requests.post(f"{base}/allure-docker-service/send-results", params={"project_id": "api"}, json=payload, timeout=30)
requests.get(f"{base}/allure-docker-service/generate-report", params={"project_id": "api"})
```
'''),
    quiz=[
        q('Главное преимущество сервера отчётов?',
            ['Красивее цвета', 'История, тренды и флаки по всем прогонам', 'Не нужны тесты', 'Быстрее pytest'],
            1, 'Отчёт одного прогона этого не даёт.'),
        q('Зачем кодировать файлы в base64 при отправке в JSON?',
            ['Шифрование', 'Чтобы передать байты (картинки) в текстовом JSON', 'Сжатие', 'Так требует pytest'],
            1, 'JSON не умеет байты.'),
        q('Чем подменяют HTTP-ответы в тестах без сети?',
            ['time.sleep', 'библиотекой responses', 'allure.attach', 'ничем'],
            1, 'Подробно — в теме про API.'),
    ],
),

# ---------- alr-notify ----------
'alr-notify': dict(
    full=t(r'''
## Зачем это нужно

Отчёт никто не откроет, если о нём не знают. Команды отправляют итог прогона в чат: Telegram, Slack, Mattermost — с цифрами и ссылкой на отчёт. Короткое сообщение «❌ Упало 3 из 250, ссылка» экономит часы.

## Текст сообщения

```python
counts = {"passed": 7, "failed": 2, "broken": 1, "skipped": 0, "total": 10}
report_url = "https://reports.test/api/42"
if counts["failed"] or counts["broken"]:
    head = f"❌ Упало: {counts['failed']}, сломано: {counts['broken']} из {counts['total']}"
else:
    head = f"✅ Тесты прошли: {counts['passed']}/{counts['total']}"
print(f"{head}\nОтчёт: {report_url}")
```

- Первая строка — главное: прошло или нет, сколько упало. Дальше — ссылка.
- Вывод: `❌ Упало: 2, сломано: 1 из 10`, `Отчёт: https://reports.test/api/42`.

## Telegram

```py
requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage",
    json={"chat_id": chat_id, "text": text},
    timeout=10,
)
```

- Бот создаётся через @BotFather — он выдаёт токен. `chat_id` — идентификатор чата или группы.
- Ответ содержит `"ok": true` при успехе.

## Slack

```py
requests.post(webhook_url, json={
    "text": "❌ Упало: 2",
    "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": "<https://r|Открыть отчёт>"}}],
})
```

- **Incoming webhook** — секретный URL, на который отправляют JSON. `blocks` — форматированные блоки, `<url|текст>` — ссылка.

## Секреты и шум

- Токены и webhook — только в секретах CI: `${{ secrets.TELEGRAM_TOKEN }}` в GitHub Actions, masked variables в GitLab. Никогда не в коде.
- Шлите уведомления о падениях и изменениях статуса, а не о каждом зелёном прогоне — иначе их перестанут читать.
- Список упавших тестов обрезайте: 5 имён и «…и ещё N».

## Итог

- Сообщение: статус и цифры в первой строке, ссылка на отчёт.
- Telegram — `sendMessage` c токеном бота; Slack — incoming webhook.
- Токены — в секретах CI; уведомлять о падениях, не о каждом прогоне.
'''),
    short=t(r'''
```py
text = f"❌ Упало: {f}, сломано: {b} из {total}\nОтчёт: {url}"
requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
              json={"chat_id": chat_id, "text": text}, timeout=10)
requests.post(slack_webhook, json={"text": text, "blocks": [...]})
# токены — ${{ secrets.TELEGRAM_TOKEN }}; уведомлять о падениях
```
'''),
    quiz=[
        q('Где хранить токен бота для уведомлений?',
            ['В коде', 'В секретах CI', 'В README', 'В названии ветки'],
            1, '${{ secrets.X }}.'),
        q('Что должно быть в первой строке уведомления?',
            ['Приветствие', 'Итог: прошло или сколько упало', 'Список всех тестов', 'Версия Python'],
            1, 'Главное — сразу.'),
        q('Почему не стоит слать уведомление о каждом успешном прогоне?',
            ['Дорого', 'Чат зашумится и уведомления перестанут читать', 'Запрещено', 'Telegram не разрешает'],
            1, 'Шлите о падениях и изменениях.'),
    ],
),

# ---------- alr-practice ----------
'alr-practice': dict(
    full=t(r'''
## Зачем это нужно

В реальном проекте Allure настраивают один раз — в `conftest.py`: общие метки, окружение, скриншоты и логи при падении. Тесты остаются короткими, а каждый отчёт получается полным. Для этого используют **хуки** pytest — функции с особыми именами, которые pytest вызывает в определённые моменты.

## Метки для всех тестов

```py
# conftest.py
@pytest.fixture(autouse=True)
def owner():
    allure.dynamic.label("owner", "qa-team")
    allure.dynamic.tag("stage")
```

- autouse-фикстура выполняется перед каждым тестом, `allure.dynamic.*` добавляет метки текущему тесту.

## Вложение при падении

```py
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        allure.attach(collect_logs(item.name), name="log",
                      attachment_type=allure.attachment_type.TEXT)
```

Что здесь происходит:

- `pytest_runtest_makereport` вызывается трижды на тест: для этапов `setup`, `call` (сам тест) и `teardown`.
- `hookwrapper=True` — наш код оборачивает стандартную реализацию: до `yield` — до неё, после — когда отчёт готов.
- `outcome.get_result()` — объект отчёта: `.when`, `.passed`, `.failed`, `.skipped`, `.longrepr` (текст ошибки).
- `item` — сам тест: `item.name`, `item.funcargs` (его фикстуры — например, `page` для скриншота).

## Окружение после прогона

```py
def pytest_sessionfinish(session, exitstatus):
    folder = session.config.getoption("--alluredir")
    if folder:
        with open(os.path.join(folder, "environment.properties"), "w", encoding="utf-8") as f:
            f.write(f"Stand={os.environ.get('STAND', 'dev')}\nPython=3.12\n")
```

- `pytest_sessionfinish` — один раз после всех тестов.
- `session.config.getoption("--alluredir")` — папка результатов; если флаг не задан — `None`, писать некуда.

## Шаги как фикстура

```py
@pytest.fixture
def api_step():
    def step(name):
        return allure.step(f"API: {name}")
    return step


def test_users(api_step):
    with api_step("GET /users"):
        ...
```

- Фабрика шагов с единым префиксом — отчёт выглядит единообразно.

## Итог

- autouse-фикстура + `allure.dynamic.*` — общие метки.
- `pytest_runtest_makereport` (hookwrapper, `when == "call"`, `failed`) — вложения при падении.
- `pytest_sessionfinish` — environment.properties.
- Всё это — в `conftest.py`, тесты остаются чистыми.
'''),
    short=t(r'''
```py
@pytest.fixture(autouse=True)
def labels():
    allure.dynamic.label("owner", "qa-team")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        allure.attach(..., name="log", attachment_type=allure.attachment_type.TEXT)

def pytest_sessionfinish(session, exitstatus):
    folder = session.config.getoption("--alluredir")
```
'''),
    quiz=[
        q('Сколько раз вызывается `pytest_runtest_makereport` на один тест?',
            ['1', '2', '3 (setup, call, teardown)', 'Зависит от шагов'],
            2, 'Нас обычно интересует call.'),
        q('Что даёт `hookwrapper=True`?',
            ['Ускорение', 'Код до и после стандартной реализации через yield', 'Параллельность', 'Отключение хука'],
            1, 'После yield отчёт уже готов.'),
        q('Какой хук вызывается один раз после всех тестов?',
            ['pytest_runtest_setup', 'pytest_sessionfinish', 'pytest_configure', 'pytest_collection'],
            1, 'Удобно записать окружение.'),
    ],
),

}
