"""Теория модуля «Окружение и pip» темы «Python-проект».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- prj-venv ----------
'prj-venv': dict(
    full=t(r'''
## Зачем это нужно

Одному проекту нужен `pytest 7`, другому — `pytest 8`; один использует `selenium`, другой — `playwright`. Если ставить всё в системный Python, версии начнут конфликтовать, а «у меня работает, у тебя нет» станет нормой. **Виртуальное окружение** — отдельная папка со своим Python и своими пакетами для каждого проекта.

## Создать и активировать

```bash
$ python -m venv .venv
$ source .venv/bin/activate
(.venv) $ which python
/home/anna/api-tests/.venv/bin/python
(.venv) $ deactivate
```

Что делает каждая команда:

- `python -m venv .venv` — создать окружение в папке `.venv`. `-m venv` — запустить стандартный модуль `venv`.
- `source .venv/bin/activate` — **активировать**: в этом терминале команды `python` и `pip` теперь берутся из `.venv`. В приглашении появляется `(.venv)`.
- В Windows: `.venv\Scripts\activate` (cmd) или `.venv\Scripts\Activate.ps1` (PowerShell).
- `which python` — проверить, что используется Python окружения.
- `deactivate` — вернуться к системному Python.

## Без активации

```bash
$ .venv/bin/python -m pytest
$ .venv/bin/pip install requests
```

- Можно вызывать программы окружения по полному пути — удобно в скриптах и CI.

## Правила

- Папку `.venv` **не коммитят** в git (она в `.gitignore`) — окружение пересоздают из списка зависимостей.
- Одно окружение — один проект. Папка обычно лежит прямо в проекте.
- Редактор (VS Code, PyCharm) нужно указать на интерпретатор `.venv/bin/python`, иначе он не увидит установленные пакеты.

## Как код узнаёт, что он в venv

```python
import sys

print(sys.prefix != sys.base_prefix)
```

- `sys.prefix` — корень текущего окружения, `sys.base_prefix` — исходного Python. Если они различаются — мы внутри venv.

## Итог

- `python -m venv .venv` → `source .venv/bin/activate` → работа → `deactivate`.
- `(.venv)` в приглашении и `which python` — проверка.
- `.venv/bin/python` — запуск без активации.
- `.venv` — в `.gitignore`.
'''),
    short=t(r'''
```bash
python -m venv .venv            # создать
source .venv/bin/activate       # активировать (Linux/macOS)
.venv\Scripts\activate          # Windows
which python                    # проверить
deactivate                      # выйти
.venv/bin/python -m pytest      # без активации
```
'''),
    quiz=[
        q('Зачем нужно виртуальное окружение?',
            ['Для скорости', 'Чтобы у каждого проекта были свои версии пакетов', 'Для запуска Docker', 'Для git'],
            1, 'Проекты не мешают друг другу.'),
        q('Нужно ли коммитить папку `.venv`?',
            ['Да', 'Нет, её пересоздают из списка зависимостей', 'Только в main', 'Только requirements'],
            1, '.venv — в .gitignore.'),
        q('Как понять, что окружение активно?',
            ['Никак', '(.venv) в приглашении и which python указывает в .venv', 'Появится файл', 'python --venv'],
            1, 'Проверяй перед установкой пакетов.'),
    ],
),

# ---------- prj-pip ----------
'prj-pip': dict(
    full=t(r'''
## Зачем это нужно

Почти все инструменты тестировщика — сторонние пакеты: `pytest`, `requests`, `playwright`, `allure-pytest`, `pydantic`. `pip` — стандартный установщик пакетов из каталога **PyPI**.

## Установка

```bash
$ pip install requests
$ pip install pytest==8.3.2
$ pip install -U requests
$ python -m pip install requests
```

- `pip install пакет` — последняя версия со всеми зависимостями.
- `пакет==версия` — ровно эта версия.
- `-U` (`--upgrade`) — обновить до последней.
- `python -m pip` — pip **того** Python, который запускаешь. Надёжнее голого `pip`, когда на компьютере несколько Python.

## Посмотреть и удалить

```bash
$ pip list
Package    Version
---------- -------
pytest     8.3.2
requests   2.32.3
$ pip show pytest
$ pip uninstall -y selenium
```

- `pip list` — все установленные пакеты; `pip freeze` — то же в формате `имя==версия`.
- `pip show` — версия, зависимости, путь установки.
- `pip uninstall -y` — удалить без вопроса. Зависимости пакета при этом **не** удаляются.

## Версии

- Формат **семантического версионирования**: `МАЖОРНАЯ.МИНОРНАЯ.ПАТЧ` — `2.32.3`.
- Патч — исправления, минорная — новые возможности, мажорная — несовместимые изменения (после обновления мажорной версии тесты могут сломаться).
- Сравнивать версии строками нельзя: `"2.10" < "2.9"` как строки, но версия 2.10 новее.

```python
def parse_version(v):
    return tuple(int(p) for p in v.split("."))

print("2.10.0" > "2.9.5", parse_version("2.10.0") > parse_version("2.9.5"))
```

- Кортежи чисел сравниваются поэлементно — правильно.
- Вывод: `False True`.

## Итог

- `pip install пакет[==версия]`, `-U` — обновить.
- `pip list`, `pip freeze`, `pip show`, `pip uninstall -y`.
- `python -m pip` — pip нужного интерпретатора; ставь пакеты в активное venv.
- Версия `мажорная.минорная.патч`; сравнивай как числа.
'''),
    short=t(r'''
```bash
pip install requests            # последняя
pip install pytest==8.3.2       # точная
pip install -U requests         # обновить
python -m pip install x         # pip нужного python
pip list / pip freeze           # установленные
pip show pytest                 # подробности
pip uninstall -y selenium
```
'''),
    quiz=[
        q('Почему `python -m pip` надёжнее `pip`?',
            ['Быстрее', 'Гарантирует pip того Python, который ты запускаешь', 'Ставит глобально', 'Не требует интернета'],
            1, 'Когда Python несколько, pip может оказаться «чужим».'),
        q('Что означает мажорная версия?',
            ['Исправления', 'Несовместимые изменения', 'Номер сборки', 'Дату'],
            1, 'После обновления мажорной версии код может сломаться.'),
        q('Какая версия новее: 2.10.0 или 2.9.5?',
            ['2.9.5', '2.10.0', 'Одинаковые', 'Нельзя сравнить'],
            1, 'Сравниваем числа: 10 > 9.'),
    ],
),

# ---------- prj-requirements ----------
'prj-requirements': dict(
    full=t(r'''
## Зачем это нужно

Коллега склонировал репозиторий с тестами — какие пакеты ему поставить? CI запускает тесты на чистой машине — откуда он узнает зависимости? Список хранится в файле `requirements.txt`, и одна команда устанавливает всё нужное.

## Формат

```bash
$ cat requirements.txt
# тесты
pytest==8.3.2
requests>=2.31
allure-pytest~=2.13.0
pydantic
```

Операторы версий:

- `==8.3.2` — ровно эта версия (самое предсказуемое).
- `>=2.31` — не ниже.
- `~=2.13.0` — «совместимая»: `>=2.13.0` и `<2.14`.
- `>=2,<3` — диапазон.
- Без версии — любая (опасно: завтра выйдет новая и сломает тесты).
- `#` — комментарий.

## Установить и сохранить

```bash
$ pip install -r requirements.txt
$ pip freeze > requirements.txt
```

- `-r файл` — установить всё из файла.
- `pip freeze >` — записать **точные** версии всего установленного, включая зависимости зависимостей. Это «снимок» рабочего окружения.

## Разделение на файлы

```bash
$ cat requirements-dev.txt
-r requirements.txt
ruff==0.6.9
pre-commit
$ pip install -r requirements-dev.txt
```

- `-r другой_файл` внутри — включить его содержимое.
- Основные зависимости и инструменты разработки хранят отдельно.

## Разбор файла в коде

```python
text = """pytest==8.3.2
Requests>=2.31  # http
-r base.txt
pydantic"""
deps = {}
for line in text.splitlines():
    line = line.split("#")[0].strip()
    if line and not line.startswith("-"):
        name = line.split("=")[0].split(">")[0].split("~")[0].strip().lower()
        deps[name] = line[len(name):].strip()
print(deps)
```

- Имена пакетов нечувствительны к регистру: `Requests` = `requests`.
- Вывод: `{'pytest': '==8.3.2', 'requests': '>=2.31', 'pydantic': ''}`.

## Итог

- `requirements.txt`: `пакет==версия`, `>=`, `~=`, комментарии `#`.
- `pip install -r` — установить; `pip freeze >` — сохранить точные версии.
- `-r base.txt` — включить другой файл; dev-зависимости — отдельно.
- Фиксируй версии, чтобы тесты не ломались от чужих обновлений.
'''),
    short=t(r'''
```bash
pip install -r requirements.txt
pip freeze > requirements.txt
# pytest==8.3.2      ровно
# requests>=2.31     не ниже
# allure-pytest~=2.13.0   2.13.x
# -r requirements.txt   (в requirements-dev.txt)
```
'''),
    quiz=[
        q('Что означает `~=2.13.0`?',
            ['Ровно 2.13.0', 'Любая 2.13.x, но не 2.14', 'Не ниже 2.13', 'Любая версия'],
            1, 'Совместимая версия.'),
        q('Что делает `pip freeze > requirements.txt`?',
            ['Удаляет пакеты', 'Сохраняет точные версии установленных пакетов', 'Замораживает Python', 'Устанавливает пакеты'],
            1, 'Снимок окружения.'),
        q('Почему опасно указывать пакет без версии?',
            ['Не установится', 'Новая версия может сломать тесты', 'Медленно', 'Не опасно'],
            1, 'Сегодня работает, завтра нет.'),
    ],
),

# ---------- prj-pyproject ----------
'prj-pyproject': dict(
    full=t(r'''
## Зачем это нужно

`pyproject.toml` — современный единый файл настроек Python-проекта: имя, версия, зависимости и настройки инструментов (pytest, ruff, mypy, coverage). Вместо десятка файлов (`setup.py`, `pytest.ini`, `.flake8`) — один.

## Структура

```bash
$ cat pyproject.toml
[project]
name = "api-tests"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31",
    "pydantic>=2",
]

[project.optional-dependencies]
dev = ["pytest>=8", "ruff"]

[tool.pytest.ini_options]
addopts = "-v --tb=short"
testpaths = ["tests"]

[tool.ruff]
line-length = 120
```

Разбор:

- Формат **TOML**: `[секция]`, `ключ = значение`, строки в кавычках, списки в `[]`.
- `[project]` — метаданные: имя, версия, минимальная версия Python, обязательные зависимости.
- `[project.optional-dependencies]` — группы дополнительных зависимостей (`dev`, `ui`).
- `[tool.имя]` — настройки инструментов: `[tool.pytest.ini_options]`, `[tool.ruff]`.

## Установка проекта

```bash
$ pip install -e .
$ pip install -e ".[dev]"
```

- `-e` (editable) — режим разработки: пакет ссылается на твою папку, правки кода видны сразу.
- `.[dev]` — вместе с группой `dev`. Кавычки нужны, потому что zsh раскрывает `[ ]`.

## Чтение в коде: tomllib

```python
import tomllib

text = """
[project]
name = "api-tests"
version = "0.1.0"
dependencies = ["requests>=2.31"]

[tool.pytest.ini_options]
addopts = "-v -n 2"
"""
data = tomllib.loads(text)
print(data["project"]["name"], data["project"]["dependencies"])
print(data["tool"]["pytest"]["ini_options"]["addopts"].split())
```

- `tomllib` — стандартный модуль (Python 3.11+) для чтения TOML. `loads` — из строки, `load(f)` — из файла, открытого в режиме `"rb"`.
- Результат — обычный словарь; вложенные секции — вложенные словари.
- Вывод: `api-tests ['requests>=2.31']`, `['-v', '-n', '2']`.

## Итог

- `pyproject.toml`: `[project]` (name, version, dependencies), `[project.optional-dependencies]`, `[tool.*]`.
- `pip install -e ".[dev]"` — проект в режиме разработки с доп. зависимостями.
- `tomllib.loads` / `tomllib.load` — чтение TOML в Python.
'''),
    short=t(r'''
```bash
[project]
name = "api-tests"
requires-python = ">=3.11"
dependencies = ["requests>=2.31"]
[project.optional-dependencies]
dev = ["pytest", "ruff"]
[tool.pytest.ini_options]
addopts = "-v"
[tool.ruff]
line-length = 120
# pip install -e ".[dev]"   ·   tomllib.loads(text)
```
'''),
    quiz=[
        q('В какой секции лежат обязательные зависимости?',
            ['[tool]', '[project] → dependencies', '[dev]', '[requirements]'],
            1, 'Список строк со спецификаторами.'),
        q('Что делает `pip install -e .`?',
            ['Удаляет проект', 'Устанавливает проект в режиме разработки', 'Проверяет ошибки', 'Экспортирует зависимости'],
            1, 'Правки кода подхватываются сразу.'),
        q('Каким модулем читать TOML в Python 3.11+?',
            ['json', 'tomllib', 'configparser', 'yaml'],
            1, 'Стандартная библиотека.'),
    ],
),

}
