"""Теория модуля «Качество и практика» темы «CI/CD для тестировщика».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- ci-gitlab ----------
'ci-gitlab': dict(
    full=t(r'''
## Зачем это нужно

Многие компании (особенно в России) держат код в GitLab, а значит — пайплайны в **GitLab CI**. Идеи те же, что в GitHub Actions, синтаксис другой.

## .gitlab-ci.yml

```yaml
stages: [lint, test, report]

default:
  image: python:3.12-slim

ruff:
  stage: lint
  script:
    - pip install ruff
    - ruff check .

api-tests:
  stage: test
  script:
    - pip install -r requirements.txt
    - pytest tests/api --junitxml=report.xml
  artifacts:
    when: always
    reports:
      junit: report.xml
```

- `stages` — порядок стадий; job-ы одной стадии идут **параллельно**, следующая стадия ждёт окончания предыдущей. Стадия по умолчанию — `test`.
- Job — ключ верхнего уровня со `script` (список команд). Служебные ключи: `stages`, `variables`, `default`, `include`, `workflow`.
- `image` — Docker-образ, в котором идёт job (в GitLab job-ы обычно работают в контейнере).
- `artifacts.reports.junit` — GitLab покажет результаты тестов прямо в merge request. `when: always` — сохранить и при падении.
- `needs: [job]` — начать раньше, не дожидаясь всей стадии.

## rules — когда запускать

```yaml
ui-tests:
  script: [pytest tests/ui]
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
```

Правила проверяются сверху вниз, срабатывает первое подошедшее; ни одно не подошло — job не создаётся. `when: manual` — запуск кнопкой.

Полезные переменные: `$CI_COMMIT_BRANCH`, `$CI_COMMIT_SHA`, `$CI_PIPELINE_SOURCE` (`push`, `merge_request_event`, `schedule`), `$CI_MERGE_REQUEST_IID`. Свои — в `variables:` или в настройках проекта (маскируемые — для секретов).

## Шаблоны

```yaml
.tests:
  image: python:3.12-slim
  before_script:
    - pip install -r requirements.txt

api-tests:
  extends: .tests
  script: [pytest tests/api]
```

Job с именем на точку — скрытый шаблон, не запускается. `extends` берёт его настройки; ключи job-а перекрывают шаблон.

## Итог

- `stages` + job-ы со `script`; одна стадия — параллельно.
- `artifacts: reports: junit` — тесты в merge request.
- `rules` с `$CI_*` — когда запускать; `when: manual` — кнопкой.
- `.шаблон` + `extends` — без копипасты.
'''),
    short=t(r'''
```yaml
stages: [lint, test]
.py: {image: python:3.12-slim}
api:
  extends: .py
  stage: test
  script: [pytest --junitxml=report.xml]
  artifacts: {when: always, reports: {junit: report.xml}}
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
# $CI_COMMIT_BRANCH $CI_COMMIT_SHA $CI_PIPELINE_SOURCE
```
'''),
    quiz=[
        q('Как идут job-ы одной стадии GitLab CI?',
            ['Строго по порядку в файле', 'Параллельно', 'По алфавиту', 'Только один'],
            1, 'Стадии — последовательно, job-ы внутри — параллельно.'),
        q('Что делает `artifacts: reports: junit: report.xml`?',
            ['Удаляет отчёт', 'Показывает результаты тестов в merge request', 'Запускает тесты', 'Сохраняет кэш'],
            1, 'GitLab разбирает JUnit.'),
        q('Job `.base` в `.gitlab-ci.yml`…',
            ['Запустится первым', 'Не запускается — это шаблон для extends', 'Упадёт с ошибкой', 'Запустится последним'],
            1, 'Точка в начале — скрытый job.'),
    ],
),

# ---------- ci-gates ----------
'ci-gates': dict(
    full=t(r'''
## Зачем это нужно

«Тесты запустились» — ещё не качество. **Quality gate** — набор правил, при нарушении которых пайплайн красный и слияние блокируется: упавшие тесты, низкое покрытие, линтер, слишком долгий прогон, выросшее число пропущенных.

## Линтер и форматирование

```bash
ruff check .              # ошибки и подозрительный код
ruff format --check .     # отформатирован ли код (без изменений)
```

## Покрытие

```bash
pytest --cov=app --cov-report=xml --cov-fail-under=80
```

- `pytest-cov` меряет, какие строки кода выполнились в тестах.
- `--cov-fail-under=80` — код выхода ≠ 0, если покрыто меньше 80%.
- `coverage.xml` (формат Cobertura) читают GitLab, SonarQube, Codecov; доля покрытых строк — атрибут `line-rate` корневого тега.

Покрытие — не цель, а сигнал: 100% покрытия без проверок ничего не гарантирует, но резкое падение значит, что новый код пришёл без тестов.

## Правила gate

- упавших тестов — 0;
- покрытие не ниже порога и не падает относительно `main`;
- доля пропущенных (`skip`) не растёт — пропущенные тесты имеют свойство копиться;
- время прогона в пределах бюджета;
- **новые** падения блокируют слияние; известные флаки — в карантине с задачей на починку.

## Карантин флаки

Нестабильный тест помечают (`@pytest.mark.flaky` или свой маркер `quarantine`), его падение не красит пайплайн, но попадает в отчёт. Карантин без срока и владельца превращается в кладбище тестов — у каждого должна быть задача.

## Медленные тесты

```bash
pytest --durations=10        # 10 самых медленных тестов
```

## Защита ветки

В настройках репозитория: **Require status checks to pass before merging** — без зелёного пайплайна кнопка слияния недоступна. Это и делает gate обязательным.

## Итог

- Gate = правила: падения, покрытие, линтер, время, пропуски.
- `--cov-fail-under`, `ruff check`, `ruff format --check`, `--durations`.
- Блокируют новые падения; флаки — в карантин с владельцем.
- Защита ветки делает gate обязательным.
'''),
    short=t(r'''
```bash
ruff check . && ruff format --check .
pytest --cov=app --cov-report=xml --cov-fail-under=80
pytest --durations=10
# coverage.xml: <coverage line-rate="0.83">
# ветка: Require status checks to pass before merging
```
'''),
    quiz=[
        q('Что делает `--cov-fail-under=80`?',
            ['Пропускает 80% тестов', 'Роняет прогон, если покрытие ниже 80%', 'Запускает 80 тестов', 'Ограничивает время 80 секундами'],
            1, 'Порог покрытия как quality gate.'),
        q('Что лучше блокировать при слиянии PR?',
            ['Любое падение, даже известных флаки', 'Новые падения относительно main', 'Ничего', 'Только линтер'],
            1, 'Известные флаки — в карантин с задачей.'),
        q('Как сделать зелёный пайплайн обязательным условием слияния в GitHub?',
            ['Написать в README', 'Защита ветки: Require status checks to pass before merging', 'Добавить `on: merge`', 'Никак'],
            1, 'Branch protection rules.'),
    ],
),

# ---------- ci-notify ----------
'ci-notify': dict(
    full=t(r'''
## Зачем это нужно

Пайплайн упал ночью, а узнали об этом через два дня — значит, CI не работает как система раннего оповещения. Отчёт должен быть **доступен** (ссылка, история), а о падениях должны **узнавать** — но без спама, который перестают читать.

## Allure в CI

```yaml
- run: pytest --alluredir=allure-results
- run: allure generate allure-results -o allure-report --clean
  if: always()
- uses: actions/upload-artifact@v4
  if: always()
  with: {name: allure-report, path: allure-report/}
```

- Для **истории** (графики трендов, «этот тест падал вчера») перед генерацией копируют `allure-report/history` прошлого отчёта в `allure-results/`: `cp -r allure-report/history allure-results/`.
- Публикация: GitHub Pages, GitLab Pages, Allure TestOps / свой сервер отчётов — чтобы у отчёта была постоянная ссылка.

## Уведомления

Чат-боты (Slack, Telegram, Mattermost) принимают сообщение POST-запросом на **вебхук**:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"text": "❌ main: 2 теста упали"}' $WEBHOOK_URL
```

Адрес вебхука — секрет: по нему кто угодно может писать в чат.

Хорошее уведомление:

- статус и ветка в первой строке — понятно без открытия;
- что упало (первые несколько тестов, не простыня);
- ссылка на запуск или отчёт.

```python
import json

print(json.dumps({"text": "Упало"}))
print(json.dumps({"text": "Упало"}, ensure_ascii=False))
```

Вывод: `{"text": "Упало"}` и `{"text": "Упало"}` — оба корректный JSON, но второй читаем в логах.

## Когда уведомлять

- упал — всегда;
- починили (красный → зелёный) — да, чтобы все знали;
- зелёный после зелёного — нет, это шум.

В GitHub Actions шаг уведомления ставят с `if: failure()` (только при падении) или считают смену статуса сами.

## Итог

- Allure: `--alluredir` → `allure generate` (с `if: always()`), история через `history/`, публикация по постоянной ссылке.
- Уведомления — вебхук (секрет), коротко: статус, что упало, ссылка.
- Уведомляй о падениях и починках, не о каждом зелёном прогоне.
'''),
    short=t(r'''
```bash
pytest --alluredir=allure-results
cp -r allure-report/history allure-results/        # история трендов
allure generate allure-results -o allure-report --clean
curl -X POST -H "Content-Type: application/json" -d '{"text": "tests failed"}' $WEBHOOK_URL
# уведомлять: упал — да, починили — да, зелёный→зелёный — нет
```
'''),
    quiz=[
        q('Как сохранить историю прогонов в Allure-отчёте между запусками CI?',
            ['Никак', 'Копировать `history` прошлого отчёта в `allure-results` перед генерацией', 'Не удалять allure-results', 'Запускать allure serve'],
            1, 'Тренды строятся по папке history.'),
        q('Почему адрес вебхука чата хранят в секретах?',
            ['Он длинный', 'По нему любой может отправлять сообщения в чат', 'Так быстрее', 'Иначе curl не работает'],
            1, 'Вебхук — это ключ доступа.'),
        q('О каком прогоне НЕ стоит уведомлять?',
            ['Упал', 'Починили после падения', 'Зелёный после зелёного', 'Первый упавший'],
            2, 'Иначе уведомления станут шумом.'),
    ],
),

# ---------- ci-practice ----------
'ci-practice': dict(
    full=t(r'''
## Зачем это нужно

Соберём всё в пайплайн, который не стыдно показать на собеседовании и поддерживать в команде.

## Пайплайн автотестов

```yaml
name: autotests
on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: "0 3 * * *"

jobs:
  lint:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff
      - run: ruff check .

  api:
    needs: lint
    runs-on: ubuntu-latest
    timeout-minutes: 15
    env:
      BASE_URL: ${{ vars.STAGE_URL }}
      API_TOKEN: ${{ secrets.API_TOKEN }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12", cache: pip}
      - run: pip install -r requirements.txt
      - run: pytest tests/api --junitxml=reports/api.xml
      - uses: actions/upload-artifact@v4
        if: always()
        with: {name: api-reports, path: reports/}

  ui:
    needs: api
    runs-on: ubuntu-latest
    timeout-minutes: 30
    strategy:
      fail-fast: false
      matrix:
        browser: [chromium, firefox]
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt && playwright install --with-deps ${{ matrix.browser }}
      - run: pytest tests/ui --browser ${{ matrix.browser }} --tracing retain-on-failure
      - uses: actions/upload-artifact@v4
        if: always()
        with: {name: "ui-${{ matrix.browser }}", path: test-results/}
```

## Чек-лист хорошего пайплайна

- быстрые проверки первыми, `needs` — только где нужен порядок;
- версии actions и образов зафиксированы (`@v4`, `postgres:16`);
- `timeout-minutes` у каждого job-а;
- секреты — только через `secrets`, в логи не печатаются;
- отчёты, трейсы, скриншоты — артефактами с `if: always()`;
- матрицы с `fail-fast: false` для тестов;
- ночной полный регресс по `schedule`, быстрый смоук — на каждый PR;
- защита ветки: без зелёного пайплайна нет слияния.

## Когда пайплайн красный

1. Открыть сводку и упавший job: `gh run view <id> --log-failed`.
2. Скачать артефакты: отчёт, скриншоты, трейс.
3. Воспроизвести локально **только упавший** тест: `pytest tests/ui/test_cart.py::test_remove_item -v`.
4. Флаки? Посмотреть историю теста в Allure; перезапуск — только чтобы подтвердить гипотезу, не вместо починки.
5. Баг продукта — баг-репорт со ссылкой на запуск; баг теста — чинить тест.

## Итог

- lint → api → ui (матрица), отчёты с `if: always()`, таймауты, секреты.
- Разбор падения: логи упавших шагов → артефакты → локальный запуск одного теста.
- Пайплайн — продукт команды: его тоже тестируют и поддерживают.
'''),
    short=t(r'''
```bash
gh run view <id> --log-failed
gh run download <id> -n api-reports
pytest tests/ui/test_cart.py::test_remove_item -v
# чек-лист: fail fast · @v4 · timeout-minutes · secrets · if: always() · fail-fast: false · защита ветки
```
'''),
    quiz=[
        q('Зачем у каждого job-а `timeout-minutes`?',
            ['Для красоты', 'Зависший тест не будет часами занимать раннер', 'Чтобы тесты шли быстрее', 'Так требует GitHub'],
            1, 'По умолчанию лимит — 6 часов.'),
        q('Пайплайн упал на UI-тесте. Что сделать сначала?',
            ['Перезапустить до зелёного', 'Посмотреть лог упавшего шага и артефакты (трейс, скриншот)', 'Удалить тест', 'Отключить UI-тесты'],
            1, 'Сначала понять, потом чинить.'),
        q('Почему версии actions фиксируют (`actions/checkout@v4`)?',
            ['Так короче', 'Чтобы обновление чужого action не сломало пайплайн внезапно', 'Без версии не работает никогда', 'Для кэша'],
            1, 'Воспроизводимость и безопасность.'),
    ],
),

}
