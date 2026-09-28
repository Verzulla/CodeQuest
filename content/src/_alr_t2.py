"""Теория модуля «Отчёты» темы «Allure и отчёты».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- alr-report ----------
'alr-report': dict(
    full=t(r'''
## Зачем это нужно

Один отчёт показывает один прогон. Но важнее динамика: стало лучше или хуже, какие тесты начали падать, какие мигают. Для этого Allure умеет хранить **историю**. А блоки **Environment** и **Categories** отвечают на вопросы «на чём гоняли» и «что это за падения».

## Варианты генерации

```bash
$ allure generate allure-results -o allure-report --clean
$ allure generate allure-results --single-file -o allure-report --clean
```

- Обычный отчёт — папка с `index.html` и данными; открывается через веб-сервер (`allure open`, GitHub Pages).
- `--single-file` — один самодостаточный HTML-файл: можно отправить по почте или приложить к задаче.

## История и тренды

```bash
$ cp -r allure-report/history allure-results/
$ allure generate allure-results -o allure-report --clean
```

- В сгенерированном отчёте есть папка `history`. Если перед следующей генерацией скопировать её в `allure-results`, отчёт покажет графики трендов и историю каждого теста (вкладка History, пометки flaky).
- В CI историю хранят между запусками: в ветке `gh-pages`, в кэше или на сервере отчётов.

## Окружение: environment.properties

```bash
$ cat allure-results/environment.properties
Base.URL=https://stage.example.com
Browser=firefox
Python=3.12
```

- Пары `ключ=значение`; отображаются в блоке Environment на главной. Сразу видно, какой стенд, браузер и версия тестировались.
- Файл пишут скриптом или хуком pytest перед генерацией.

## Категории: categories.json

```bash
$ cat allure-results/categories.json
[
  {"name": "Проблемы окружения", "matchedStatuses": ["broken"], "messageRegex": ".*ConnectionError.*"},
  {"name": "Дефекты продукта", "matchedStatuses": ["failed"]}
]
```

- Свои правила группировки падений: по статусу и регулярному выражению для сообщения (`messageRegex`) или трассировки (`traceRegex`).
- Вкладка **Categories** сразу отделяет «сервер лёг» от настоящих багов.
- Правила проверяются по порядку; падение попадает в первую подходящую категорию. Стандартные категории — Product defects (failed) и Test defects (broken).

## Итог

- `--single-file` — отчёт одним HTML.
- История: скопировать `allure-report/history` в `allure-results` перед генерацией.
- `environment.properties` — окружение, `categories.json` — свои категории.
'''),
    short=t(r'''
```bash
allure generate allure-results --single-file -o allure-report --clean
cp -r allure-report/history allure-results/     # тренды и история
# allure-results/environment.properties:  Browser=firefox
# allure-results/categories.json:
#   [{"name": "Окружение", "matchedStatuses": ["broken"], "messageRegex": ".*Timeout.*"}]
```
'''),
    quiz=[
        q('Что нужно, чтобы в отчёте появились тренды?',
            ['Флаг --trend', 'Скопировать history прошлого отчёта в allure-results', 'Allure TestOps', 'Ничего'],
            1, 'История хранится в папке history.'),
        q('Какой файл заполняет блок Environment?',
            ['env.json', 'environment.properties', 'settings.ini', '.env'],
            1, 'Пары ключ=значение.'),
        q('Для чего categories.json?',
            ['Для меток feature', 'Для своих правил группировки падений', 'Для истории', 'Для скриншотов'],
            1, 'По статусу и тексту ошибки.'),
    ],
),

# ---------- alr-status ----------
'alr-status': dict(
    full=t(r'''
## Зачем это нужно

Разбор упавшего прогона начинается с вопроса «что это за падение»: баг продукта, ошибка в тесте, нестабильность окружения? Статусы и категории Allure отвечают на него до того, как ты откроешь первый тест.

## Статусы

- **passed** — тест прошёл.
- **failed** — не прошла проверка (`AssertionError`). Скорее всего, баг продукта или изменились требования.
- **broken** — упал с другим исключением: `KeyError`, `TimeoutError`, `ConnectionError`. Скорее проблема теста или окружения.
- **skipped** — пропущен (`skip`, `skipif`, xfail).
- **unknown** — результат не определён (например, прогон прервали).

```python
def status_of(outcome, exc_type):
    if outcome == "failed":
        return "failed" if exc_type == "AssertionError" else "broken"
    return outcome

print(status_of("failed", "AssertionError"), status_of("failed", "KeyError"), status_of("passed", None))
```

- Вывод: `failed broken passed`.

## Порядок разбора

1. Сначала **broken** в категории «проблемы окружения» — если лёг стенд, остальные падения могут быть следствием.
2. Потом **failed** с высокой severity.
3. Для каждого: шаги, вложения, история. Тест падал раньше? Падает стабильно?

## Flaky

- Тест, который меняет статус без изменений в коде (✓ ✗ ✓ ✓ ✗), Allure помечает иконкой flaky — по данным истории.
- Частые причины: ожидания в UI, гонки при параллельном запуске, общие тестовые данные, нестабильный стенд.
- Такие тесты заводят задачами и исправляют: они подрывают доверие ко всему набору.

## Retries

- Если тест перезапускался (плагин `pytest-rerunfailures`), Allure покажет все попытки на вкладке Retries. Прошёл со второй попытки — всё равно повод разобраться.

## Итог

- failed — проверка не прошла; broken — другое исключение; skipped; unknown.
- Разбор: окружение → критичные failed → детали.
- Flaky — по истории; retries — все попытки.
'''),
    short=t(r'''
```py
# passed · failed (AssertionError) · broken (другое исключение) · skipped · unknown
# разбор: broken окружения → critical failed → шаги/вложения/история
# flaky — меняет статус без изменений кода; retries — все попытки
```
'''),
    quiz=[
        q('Тест упал с `ConnectionError`. Какой статус?',
            ['failed', 'broken', 'skipped', 'unknown'],
            1, 'Не AssertionError.'),
        q('Как Allure узнаёт, что тест flaky?',
            ['По имени', 'По истории прошлых прогонов', 'По severity', 'По времени'],
            1, 'Нужна сохранённая история.'),
        q('С чего разумно начать разбор упавшего прогона?',
            ['С тестов по алфавиту', 'С broken из-за окружения', 'С пропущенных', 'С passed'],
            1, 'Упавшее окружение ломает всё остальное.'),
    ],
),

# ---------- alr-junit ----------
'alr-junit': dict(
    full=t(r'''
## Зачем это нужно

Allure — не единственный формат. **JUnit XML** понимают почти все CI-системы: GitHub Actions, GitLab, Jenkins, TeamCity показывают по нему результаты прямо в интерфейсе merge request. Иногда нужен и простой HTML-отчёт без Java. А разбирать эти форматы скриптом полезно для уведомлений и статистики.

## JUnit XML

```bash
$ pytest --junitxml=report.xml
$ cat report.xml
<testsuites>
  <testsuite name="pytest" tests="5" failures="1" errors="1" skipped="1" time="2.31">
    <testcase classname="tests.test_api" name="test_status" time="0.12"/>
    <testcase classname="tests.test_api" name="test_users" time="0.30">
      <failure message="assert 500 == 200">…трассировка…</failure>
    </testcase>
  </testsuite>
</testsuites>
```

- `failures` — упавшие проверки (аналог failed), `errors` — ошибки (аналог broken), `skipped`.
- Каждый `<testcase>`: `classname` (модуль/класс), `name`, `time`; внутри — `<failure>`, `<error>` или `<skipped>`.

## Разбор в Python

```python
import xml.etree.ElementTree as ET

xml_text = """<testsuite tests="2" failures="1">
  <testcase classname="tests.test_api" name="test_ok" time="0.1"/>
  <testcase classname="tests.test_api" name="test_bad" time="0.2"><failure message="assert 1 == 2"/></testcase>
</testsuite>"""
root = ET.fromstring(xml_text)
print(root.get("tests"), root.get("failures"))
for case in root.iter("testcase"):
    failure = case.find("failure")
    if failure is not None:
        print(case.get("name"), failure.get("message"))
```

- `ET.fromstring` — разобрать строку, `ET.parse(путь).getroot()` — файл.
- `.get("атрибут")` — значение атрибута (строка), `.iter("тег")` — все элементы на любой глубине, `.find("тег")` — первый дочерний.
- `find` возвращает `None`, если элемента нет. Сравнивай с `None` явно: у элемента без детей `bool()` ложно.
- Вывод: `2 1`, `test_bad assert 1 == 2`.

## pytest-html

```bash
$ pip install pytest-html
$ pytest --html=report.html --self-contained-html
```

- Простой HTML-отчёт без Java: таблица тестов, логи, возможность добавить картинки. Хорош для небольших проектов.

## Итог

- `pytest --junitxml=report.xml` — формат для любого CI.
- `failures` ≈ failed, `errors` ≈ broken; `<testcase>` с `<failure>/<error>/<skipped>`.
- `xml.etree.ElementTree`: `fromstring`, `iter`, `find`, `get`.
- `pytest-html` — простой отчёт без Java.
'''),
    short=t(r'''
```bash
pytest --junitxml=report.xml
pytest --html=report.html --self-contained-html   # pytest-html
```
```py
import xml.etree.ElementTree as ET
root = ET.fromstring(text)               # или ET.parse(path).getroot()
root.get("failures")
for case in root.iter("testcase"):
    f = case.find("failure")             # None, если нет
```
'''),
    quiz=[
        q('Что в JUnit XML соответствует статусу broken?',
            ['failures', 'errors', 'skipped', 'tests'],
            1, 'failures — это упавшие assert.'),
        q('Что вернёт `case.find("failure")`, если элемента нет?',
            ['Пустую строку', 'None', 'Ошибку', 'False'],
            1, 'Проверяй через is not None.'),
        q('Зачем JUnit XML, если есть Allure?',
            ['Он красивее', 'Его понимают почти все CI и показывают в интерфейсе', 'Он быстрее', 'Allure его требует'],
            1, 'Встроенная поддержка в CI.'),
    ],
),

# ---------- alr-summary ----------
'alr-summary': dict(
    full=t(r'''
## Зачем это нужно

Результаты прогона нужны не только в отчёте: скрипт должен решить, пропускать ли релиз, отправить уведомление, посчитать процент успешных. Для этого читают сырые результаты Allure (`*-result.json`) или готовую сводку сгенерированного отчёта.

## Чтение результатов

```python
import json
from pathlib import Path

folder = Path("res")
folder.mkdir(exist_ok=True)
for i, status in enumerate(["passed", "failed", "passed"]):
    (folder / f"{i}-result.json").write_text(json.dumps({"name": f"t{i}", "status": status}), encoding="utf-8")

results = [json.loads(p.read_text(encoding="utf-8")) for p in folder.glob("*-result.json")]
counts = {}
for r in results:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
print(len(results), sorted(counts.items()))
```

- Каждый `*-result.json` — словарь: `name`, `status`, `statusDetails` (сообщение и трассировка), `steps`, `attachments`, `labels`, `parameters`, `start`, `stop` (время в миллисекундах).
- Вывод: `3 [('failed', 1), ('passed', 2)]`.

## Процент успешных

```python
counts = {"passed": 3, "failed": 1, "broken": 1, "skipped": 1}
executed = counts["passed"] + counts["failed"] + counts["broken"]
print(round(counts["passed"] * 100 / executed, 1))
```

- Пропущенные тесты не выполнялись — их не считают в знаменателе.
- Вывод: `60.0`.

## Сводка готового отчёта

```bash
$ jq .statistic allure-report/widgets/summary.json
{"failed": 1, "broken": 0, "skipped": 2, "passed": 37, "unknown": 0, "total": 40}
```

- В сгенерированном отчёте файл `widgets/summary.json` содержит итоговую статистику и время прогона. Удобнее, чем разбирать все результаты.
- `jq` — утилита для JSON в терминале.

## Quality gate

- **Ворота качества** — правило, по которому CI решает, можно ли выпускать: «нет broken», «pass rate не ниже 95%», «нет упавших critical». Скрипт считает метрики и завершается с кодом 1, если правило нарушено.

## Итог

- `*-result.json`: `status`, `labels`, `steps`, `start`/`stop`.
- Pass rate — от выполненных (без skipped).
- `widgets/summary.json` — готовая статистика.
- Quality gate — правило + ненулевой код выхода.
'''),
    short=t(r'''
```py
results = [json.loads(p.read_text()) for p in Path("allure-results").glob("*-result.json")]
# r["status"], r["labels"], r["steps"], r["start"], r["stop"] (мс)
rate = passed * 100 / (passed + failed + broken)      # без skipped
# allure-report/widgets/summary.json → statistic
# quality gate: нарушено правило → sys.exit(1)
```
'''),
    quiz=[
        q('Учитываются ли skipped при расчёте pass rate?',
            ['Да, как успешные', 'Да, как упавшие', 'Нет, они не выполнялись', 'Только в Allure'],
            2, 'Считают от выполненных.'),
        q('Где в сгенерированном отчёте итоговая статистика?',
            ['index.html', 'widgets/summary.json', 'history/', 'data/tests'],
            1, 'Поле statistic.'),
        q('Что делает quality gate в CI?',
            ['Генерирует отчёт', 'Роняет сборку, если метрики хуже порога', 'Перезапускает тесты', 'Шлёт уведомления'],
            1, 'Ненулевой код выхода.'),
    ],
),

}
