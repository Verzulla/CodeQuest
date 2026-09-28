"""Теория модуля «Качество кода» темы «Python-проект».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- prj-lint ----------
'prj-lint': dict(
    full=t(r'''
## Зачем это нужно

**Линтер** читает код, не запуская его, и находит проблемы: неиспользуемые импорты, необъявленные переменные, опасные конструкции, слишком длинные строки. Ошибка вроде опечатки в имени фикстуры найдётся ещё до запуска тестов. **ruff** — самый быстрый линтер для Python: заменяет flake8, isort, pyupgrade и десятки плагинов.

## Проверка

```bash
$ ruff check
tests/test_api.py:1:8: F401 [*] `os` imported but unused
tests/test_api.py:9:89: E501 Line too long (104 > 88)
Found 2 errors.
[*] 1 fixable with the `--fix` option.
```

Как читать строку:

- `tests/test_api.py:9:89` — файл, строка 9, столбец 89.
- `E501` — **код правила**. Буквы — группа: `F` — pyflakes (логические ошибки), `E`/`W` — pycodestyle (стиль), `I` — сортировка импортов, `B` — bugbear (подозрительные конструкции), `S` — безопасность.
- `[*]` — ruff умеет исправить это сам.
- Код выхода: 0 — ошибок нет, 1 — есть (CI упадёт).

## Исправление и справка

```bash
$ ruff check --fix
$ ruff check tests
$ ruff rule F401
```

- `--fix` — автоматически исправить безопасные ошибки (например, удалить неиспользуемый импорт).
- Можно проверить отдельную папку или файл.
- `ruff rule КОД` — объяснение правила с примерами.

## Отключить для строки

```python
import os  # noqa: F401

LONG_URL = "https://example.com/very/long/path"  # noqa: E501
```

- `# noqa: КОД` в конце строки — не проверять это правило здесь. Используй редко и осознанно.

## Как устроена проверка F401

Линтер разбирает код в **дерево синтаксиса** (AST) и анализирует его:

```python
import ast

source = "import os\nimport json\nprint(json.dumps({}))"
tree = ast.parse(source)
imported = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
print(sorted(imported - used))
```

- `ast.parse` — код в дерево, `ast.walk` — обход всех узлов.
- Импортированные имена минус использованные — неиспользуемые.
- Вывод: `['os']`.

## Итог

- `ruff check` — проверить, `--fix` — исправить, `ruff rule` — справка.
- Формат: `файл:строка:столбец: КОД описание`.
- Группы правил: `F`, `E`, `W`, `I`, `B`, `S`.
- `# noqa: КОД` — исключение для строки.
'''),
    short=t(r'''
```bash
ruff check              # проверить
ruff check --fix        # исправить безопасное
ruff check tests        # папку
ruff rule F401          # объяснение
# файл:строка:столбец: КОД  [*] — исправимо
# F pyflakes · E/W стиль · I импорты · B bugbear · S безопасность
x = 1  # noqa: E501
```
'''),
    quiz=[
        q('Что означает `[*]` в выводе ruff?',
            ['Критическая ошибка', 'Ruff может исправить это сам через --fix', 'Предупреждение', 'Новое правило'],
            1, 'Запусти ruff check --fix.'),
        q('К какой группе относится F401?',
            ['Стиль', 'pyflakes — логические ошибки', 'Безопасность', 'Импорты'],
            1, 'Неиспользуемый импорт.'),
        q('Чем линтер отличается от тестов?',
            ['Ничем', 'Анализирует код без запуска', 'Запускает код', 'Только форматирует'],
            1, 'Статический анализ.'),
    ],
),

# ---------- prj-format ----------
'prj-format': dict(
    full=t(r'''
## Зачем это нужно

Споры «ставить ли пробел», «одинарные или двойные кавычки» отнимают время на ревью, а разный стиль мешает читать код. **Форматтер** приводит весь код к единому виду автоматически. `ruff format` делает то же, что популярный `black`, но быстрее.

## Форматирование

```bash
$ ruff format
3 files reformatted, 14 files left unchanged
$ ruff format tests/test_cart.py
```

- Переписывает файлы: отступы, пробелы, кавычки (двойные, если внутри нет двойных), переносы длинных строк, запятые в конце многострочных списков.
- Смысл кода не меняется.

## Проверка без изменений

```bash
$ ruff format --check
Would reformat: tests/test_api.py
1 file would be reformatted, 16 files already formatted
$ ruff format --diff
```

- `--check` — ничего не менять, но вернуть код 1, если есть неотформатированные файлы. Используют в CI.
- `--diff` — показать, что изменилось бы.

## Линтер и форматтер вместе

```bash
$ ruff check --fix && ruff format
```

- Сначала исправить ошибки линтера (например, сортировку импортов), потом отформатировать.
- `&&` — вторая команда выполнится, только если первая завершилась успешно.

## Пример правила: кавычки

```python
import re

def normalize_quotes(line):
    return re.sub(r"'([^'\"]*)'", r'"\1"', line)

print(normalize_quotes("d = {'a': 'b'}"))
```

- Упрощённая версия одного правила форматтера: одинарные кавычки → двойные, если внутри нет двойных.
- Вывод: `d = {"a": "b"}`.

## Итог

- `ruff format` — отформатировать; `--check` — проверить в CI; `--diff` — показать изменения.
- Порядок: `ruff check --fix && ruff format`.
- Форматтер меняет вид, а не смысл кода.
'''),
    short=t(r'''
```bash
ruff format                 # отформатировать всё
ruff format file.py
ruff format --check         # CI: 1, если есть что форматировать
ruff format --diff          # показать изменения
ruff check --fix && ruff format
```
'''),
    quiz=[
        q('Что делает `ruff format --check`?',
            ['Форматирует файлы', 'Только проверяет и возвращает ошибку, если нужно форматирование', 'Удаляет файлы', 'Проверяет ошибки линтера'],
            1, 'Для CI.'),
        q('Меняет ли форматтер логику кода?',
            ['Да', 'Нет, только оформление', 'Иногда удаляет строки', 'Переименовывает функции'],
            1, 'Смысл сохраняется.'),
        q('Какой порядок правильный?',
            ['format, потом check --fix', 'check --fix, потом format', 'Не важно', 'Только format'],
            1, 'Исправления линтера могут изменить оформление.'),
    ],
),

# ---------- prj-ruffcfg ----------
'prj-ruffcfg': dict(
    full=t(r'''
## Зачем это нужно

По умолчанию ruff включает только базовые правила. Команда договаривается о своих: длина строки, какие группы правил включить, что разрешить в тестах. Настройки хранятся в `pyproject.toml` — у всех одинаковые, и CI проверяет по ним же.

## Пример настройки

```bash
[tool.ruff]
line-length = 120
target-version = "py312"
exclude = ["migrations"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "S"]
ignore = ["E501"]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]

[tool.ruff.format]
quote-style = "double"
```

Разбор:

- `line-length` — максимальная длина строки (по умолчанию 88).
- `target-version` — версия Python, под которую писать (ruff подскажет современный синтаксис).
- `exclude` — какие папки не проверять.
- `select` — включённые группы правил; `ignore` — отключённые конкретные правила.
- `per-file-ignores` — исключения по шаблону путей. В тестах отключают `S101` («использован assert»): в тестах `assert` — основа.
- `[tool.ruff.format]` — настройки форматтера.

## Полезные группы для тестов

- `F` — ошибки (неиспользуемое, неопределённое).
- `E`, `W` — стиль PEP 8.
- `I` — порядок импортов.
- `B` — частые ошибки: изменяемые значения по умолчанию, `except:` без типа.
- `PT` — правила для pytest: стиль фикстур, `pytest.raises` без `match`.
- `S` — безопасность: пароли в коде, `verify=False`.

## Чтение настроек в Python

```python
import tomllib

text = """
[tool.ruff]
line-length = 120
[tool.ruff.lint]
select = ["E", "F", "I"]
"""
ruff = tomllib.loads(text)["tool"]["ruff"]
print(ruff["line-length"], ruff["lint"]["select"])
```

- Ключи с дефисом (`line-length`) читаются как обычные строки-ключи.
- Вывод: `120 ['E', 'F', 'I']`.

## Итог

- `[tool.ruff]`: `line-length`, `target-version`, `exclude`.
- `[tool.ruff.lint]`: `select`, `ignore`, `per-file-ignores`.
- В тестах обычно `"tests/**" = ["S101"]`; для pytest есть группа `PT`.
'''),
    short=t(r'''
```bash
[tool.ruff]
line-length = 120
target-version = "py312"
[tool.ruff.lint]
select = ["E", "F", "I", "B", "PT"]
ignore = ["E501"]
[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]
```
'''),
    quiz=[
        q('Какая длина строки у ruff по умолчанию?',
            ['79', '88', '100', '120'],
            1, 'Как у black.'),
        q('Зачем в тестах отключают S101?',
            ['Он медленный', 'Он ругается на assert, а в тестах assert — норма', 'Он для Django', 'Не отключают'],
            1, 'per-file-ignores.'),
        q('Какая группа правил проверяет порядок импортов?',
            ['F', 'I', 'B', 'S'],
            1, 'isort.'),
    ],
),

# ---------- prj-precommit ----------
'prj-precommit': dict(
    full=t(r'''
## Зачем это нужно

Забыл запустить линтер, закоммитил — CI упал через 10 минут. **pre-commit** запускает проверки автоматически при каждом `git commit`: если ruff нашёл ошибки или переформатировал файл, коммит не создастся, пока ты не добавишь исправления.

## Настройка

```bash
$ cat .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
```

- `repos` — откуда брать хуки; `rev` — версия.
- `hooks` — какие проверки запускать: ruff с автоисправлением, форматтер, удаление пробелов в конце строк, перевод строки в конце файла, проверка синтаксиса YAML.
- Формат YAML: отступы пробелами, `-` — элемент списка.

## Команды

```bash
$ pip install pre-commit
$ pre-commit install
$ pre-commit run --all-files
$ pre-commit run ruff-format --all-files
$ pre-commit autoupdate
```

- `pre-commit install` — подключить к git (один раз после клонирования). Дальше хуки запускаются при каждом `git commit` только для изменённых файлов.
- `run --all-files` — прогнать на всём проекте (полезно после подключения и в CI).
- `run хук` — только один хук.
- `autoupdate` — обновить `rev` до последних версий.

## Как выглядит срабатывание

```bash
$ git commit -m "test: add cart"
ruff.....................................................Failed
- files were modified by this hook
ruff-format..............................................Passed
$ git add . && git commit -m "test: add cart"
```

- Хук исправил файлы → коммит отменён. Добавь исправления (`git add`) и повтори коммит.
- `git commit --no-verify` — пропустить хуки. Только в экстренных случаях: CI всё равно проверит.

## Итог

- `.pre-commit-config.yaml` — список хуков; `pre-commit install` — подключить.
- Хуки проверяют изменённые файлы при каждом коммите.
- `pre-commit run --all-files` — всё сразу; `autoupdate` — обновить.
- Хук изменил файлы → `git add` и коммит заново.
'''),
    short=t(r'''
```bash
pip install pre-commit
pre-commit install              # подключить к git
pre-commit run --all-files      # весь проект
pre-commit run ruff-format -a   # один хук
pre-commit autoupdate
git commit --no-verify          # пропустить (только в крайнем случае)
# хук изменил файлы → git add → commit ещё раз
```
'''),
    quiz=[
        q('Когда запускаются хуки после `pre-commit install`?',
            ['При push', 'При каждом git commit', 'Раз в день', 'Только вручную'],
            1, 'Для изменённых файлов.'),
        q('Хук ruff исправил файлы и коммит не создался. Что делать?',
            ['Удалить хук', 'git add исправления и закоммитить снова', 'git reset --hard', 'Ничего'],
            1, 'Исправленные файлы нужно добавить.'),
        q('Что делает `pre-commit run --all-files`?',
            ['Устанавливает хуки', 'Прогоняет хуки на всех файлах проекта', 'Удаляет хуки', 'Обновляет версии'],
            1, 'Удобно после подключения и в CI.'),
    ],
),

}
