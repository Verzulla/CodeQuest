"""Теория модуля «uv и запуск» темы «Python-проект».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- prj-uv ----------
'prj-uv': dict(
    full=t(r'''
## Зачем это нужно

`uv` — современный менеджер Python-проектов от создателей ruff. Он заменяет сразу `pip`, `venv`, `pip-tools` и `pyenv`, работает в десятки раз быстрее и сам следит, чтобы у всех в команде и в CI стояли одинаковые версии пакетов. Всё больше проектов с автотестами переходят на него.

## Новый проект

```bash
$ uv init
Initialized project `api-tests`
$ uv add requests pydantic
$ uv add --dev pytest ruff
$ uv remove selenium
```

Что делает каждая команда:

- `uv init` — создать `pyproject.toml`, `.python-version`, `README.md` и пример `main.py`.
- `uv add пакет` — добавить зависимость: записать её в `pyproject.toml`, обновить lock-файл `uv.lock` и установить в `.venv` (окружение uv создаёт сам).
- `uv add --dev` — зависимость только для разработки (в группу `dev`): тестам и линтеру не место в продакшене.
- `uv add 'pydantic>=2'` — с ограничением версии.
- `uv remove` — удалить из `pyproject.toml` и окружения.

## Готовый проект

```bash
$ git clone https://github.com/acme/api-tests.git
$ cd api-tests
$ uv sync
$ uv run pytest
```

- `uv sync` — создать `.venv` и установить **ровно** то, что записано в `uv.lock`. У всех одинаково.
- `uv run команда` — выполнить команду в окружении проекта, без `source .venv/bin/activate`. Перед запуском uv сам проверит, что окружение актуально.

## Сравнение с pip

- pip: `python -m venv .venv` → `activate` → `pip install -r requirements.txt` → `pytest`.
- uv: `uv sync` → `uv run pytest`.
- `pyproject.toml` описывает, **что** нужно (с диапазонами версий), а `uv.lock` — **какие именно** версии установлены.

## Итог

- `uv init` — проект; `uv add` / `uv add --dev` / `uv remove` — зависимости.
- `uv sync` — установить по `uv.lock`; `uv run` — запустить в окружении.
- `.venv` uv создаёт и обновляет сам.
'''),
    short=t(r'''
```bash
uv init                      # новый проект
uv add requests              # зависимость
uv add --dev pytest ruff     # для разработки
uv remove selenium
uv sync                      # установить по uv.lock
uv run pytest                # запуск в окружении проекта
```
'''),
    quiz=[
        q('Что делает `uv add requests`?',
            ['Только скачивает', 'Добавляет в pyproject.toml, обновляет uv.lock и устанавливает', 'Удаляет', 'Запускает'],
            1, 'Всё одной командой.'),
        q('Как запустить тесты в окружении проекта без активации?',
            ['uv pytest', 'uv run pytest', 'uv sync pytest', 'uv test'],
            1, 'uv run выполнит команду в .venv.'),
        q('Зачем `--dev` в `uv add --dev pytest`?',
            ['Скачать dev-версию', 'Пометить зависимость как нужную только для разработки', 'Установить глобально', 'Ускорить'],
            1, 'Группа dev.'),
    ],
),

# ---------- prj-uvlock ----------
'prj-uvlock': dict(
    full=t(r'''
## Зачем это нужно

«У меня тесты проходят, а в CI падают» — частая причина: там установилась другая версия библиотеки. **Lock-файл** фиксирует точные версии всех пакетов (включая зависимости зависимостей) и их хеши. Кроме того, uv умеет сам ставить нужную версию Python.

## uv.lock

```bash
$ uv lock
$ uv lock --upgrade-package requests
$ uv sync --locked
```

- `uv lock` — пересчитать `uv.lock` по `pyproject.toml`, ничего не устанавливая.
- `--upgrade-package пакет` — обновить в lock-файле только этот пакет до последней допустимой версии. `uv lock --upgrade` — обновить всё.
- `uv sync --locked` — установить и **упасть**, если lock-файл не соответствует `pyproject.toml` (кто-то добавил зависимость и забыл обновить lock). Идеально для CI. `--frozen` — установить из lock, не проверяя.
- `uv.lock` **коммитят** в git.

## Версии Python

```bash
$ uv python install 3.12
$ uv python pin 3.12
$ uv python list
```

- `uv python install` — скачать нужную версию Python (не нужен pyenv или установщик с сайта).
- `uv python pin` — записать версию в `.python-version`; `uv sync` и `uv run` будут использовать её.

## pip-совместимый режим

```bash
$ uv venv
$ uv pip install -r requirements.txt
$ uv pip list
```

- Для старых проектов с `requirements.txt`: `uv venv` вместо `python -m venv`, `uv pip install` вместо `pip install` — те же команды, но гораздо быстрее.

## Итог

- `uv.lock` — точные версии; коммитить.
- `uv lock` (`--upgrade-package`) — обновить lock.
- `uv sync --locked` — в CI.
- `uv python install/pin` — версия Python.
- `uv venv`, `uv pip install` — быстрая замена pip для старых проектов.
'''),
    short=t(r'''
```bash
uv lock                           # пересчитать uv.lock
uv lock --upgrade-package requests
uv sync --locked                  # CI: упасть, если lock устарел
uv python install 3.12
uv python pin 3.12                # .python-version
uv venv && uv pip install -r requirements.txt
```
'''),
    quiz=[
        q('Что хранит `uv.lock`?',
            ['Пароли', 'Точные версии всех пакетов и их хеши', 'Настройки ruff', 'Список тестов'],
            1, 'Одинаковое окружение у всех.'),
        q('Какую команду использовать в CI, чтобы упасть при устаревшем lock-файле?',
            ['uv lock', 'uv sync --locked', 'uv add', 'uv run'],
            1, 'Защита от забытого uv lock.'),
        q('Нужно ли коммитить uv.lock?',
            ['Нет', 'Да', 'Только в main', 'Только при релизе'],
            1, 'Иначе версии разойдутся.'),
    ],
),

# ---------- prj-uvtools ----------
'prj-uvtools': dict(
    full=t(r'''
## Зачем это нужно

Некоторые утилиты нужны «сбоку» от проекта: линтер, форматтер, `pre-commit`, генератор отчётов. Их не хочется добавлять в зависимости каждого проекта. `uv` умеет запускать такие инструменты во временных изолированных окружениях или ставить их глобально.

## uvx: запустить без установки

```bash
$ uvx ruff check .
$ uvx --from httpie http GET https://api.example.com/health
```

- `uvx инструмент` (= `uv tool run`) — скачать инструмент во временное окружение (с кэшем) и запустить. Второй запуск мгновенный.
- `--from пакет` — когда имя команды отличается от имени пакета.

## uv tool: установить глобально

```bash
$ uv tool install ruff
$ uv tool list
$ uv tool upgrade ruff
```

- Каждый инструмент получает своё окружение, а команда становится доступна везде.

## uv run: команды проекта

```bash
$ uv run pytest -n 4
$ uv run scripts/seed_data.py
$ uv run --with requests check.py
$ uv tree
```

- Всё после `uv run` — обычная команда, выполненная в окружении проекта. Флаги передаются дальше как есть (`-n 4` — для pytest-xdist).
- `uv run скрипт.py` — запустить скрипт.
- `--with пакет` — добавить временную зависимость только для этого запуска.
- `uv tree` — дерево зависимостей: видно, кто притащил тот или иной пакет.

## Установка самого uv

```bash
$ curl -LsSf https://astral.sh/uv/install.sh | sh
$ pip install uv
$ brew install uv
```

- Официальный скрипт скачивается `curl` и сразу выполняется `sh`. Есть и другие способы: pip, Homebrew, winget.

## Итог

- `uvx инструмент` — запустить без установки.
- `uv tool install` — глобально, в изолированном окружении.
- `uv run` — команды и скрипты проекта; `--with` — временная зависимость.
- `uv tree` — дерево зависимостей.
'''),
    short=t(r'''
```bash
uvx ruff check .              # запустить без установки
uv tool install ruff          # глобально
uv tool list
uv run pytest -n 4            # в окружении проекта
uv run scripts/seed.py
uv run --with requests x.py   # временная зависимость
uv tree
curl -LsSf https://astral.sh/uv/install.sh | sh
```
'''),
    quiz=[
        q('Что делает `uvx ruff check .`?',
            ['Добавляет ruff в проект', 'Запускает ruff во временном окружении без установки', 'Удаляет ruff', 'Обновляет uv'],
            1, 'То же, что uv tool run.'),
        q('Куда попадёт `-n 4` в `uv run pytest -n 4`?',
            ['В uv', 'В pytest', 'Никуда', 'В Python'],
            1, 'Всё после имени команды передаётся ей.'),
        q('Что показывает `uv tree`?',
            ['Файлы проекта', 'Дерево зависимостей', 'Ветки git', 'Структуру тестов'],
            1, 'Кто от кого зависит.'),
    ],
),

# ---------- prj-run ----------
'prj-run': dict(
    full=t(r'''
## Зачем это нужно

Тестировщик постоянно запускает скрипты: генерация тестовых данных, очистка стенда, выгрузка отчёта. Скрипту нужно передать параметры (стенд, количество пользователей), а CI должен понять, успешно ли он отработал. Для этого есть аргументы командной строки и **код выхода**.

## Способы запуска

```bash
$ python seed.py --users 10
$ python -m pytest
$ python -c "import sys; print(sys.version)"
```

- `python файл.py аргументы` — запустить скрипт.
- `python -m модуль` — запустить модуль как программу. `python -m pytest` гарантирует pytest **того же** Python (и добавляет текущую папку в пути импорта).
- `python -c "код"` — выполнить однострочник.

## sys.argv

```python
import sys

argv = ["seed.py", "--users", "10"]   # так выглядит sys.argv при запуске python seed.py --users 10
print(argv[0], argv[1:])
```

- `sys.argv` — список: имя скрипта и аргументы строками.
- Вывод: `seed.py ['--users', '10']`.

## argparse

```python
import argparse

parser = argparse.ArgumentParser(description="Генератор тестовых данных")
parser.add_argument("--env", default="dev")
parser.add_argument("--workers", type=int, default=1)
parser.add_argument("--headless", action="store_true")
args = parser.parse_args(["--env", "stage", "--headless"])
print(args.env, args.workers, args.headless)
```

- `add_argument("--имя")` — именованный аргумент; `type=int` — преобразование; `default` — значение по умолчанию.
- `action="store_true"` — флаг без значения: есть — `True`, нет — `False`.
- `parse_args()` без списка читает настоящий `sys.argv`; `--help` argparse сгенерирует сам.
- Вывод: `stage 1 True`.

## Код выхода

```python
def main(argv):
    if not argv:
        print("usage: check.py FILE...")
        return 2
    print("проверяю:", ", ".join(argv))
    return 0

print(main([]), main(["a.json"]))
```

- Каждая программа возвращает число: **0 — успех**, всё остальное — ошибка. CI и `&&` смотрят именно на него.
- В реальном скрипте: `if __name__ == "__main__": sys.exit(main(sys.argv[1:]))`.
- `echo $?` в bash — код выхода последней команды. pytest возвращает 0, если все тесты прошли, и 1, если есть падения.
- Вывод: `usage: check.py FILE...`, `проверяю: a.json`, `2 0`.

## Итог

- `python скрипт.py`, `python -m модуль`, `python -c "код"`.
- `sys.argv` — сырые аргументы; `argparse` — удобный разбор.
- Код выхода: 0 — успех; `sys.exit(код)`; `echo $?`.
'''),
    short=t(r'''
```bash
python seed.py --users 10
python -m pytest            # pytest нужного Python
python -c "print(1)"
echo $?                     # код выхода (0 — успех)
# argparse: add_argument("--env", default="dev")
#           add_argument("--n", type=int)
#           add_argument("--headless", action="store_true")
# if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
```
'''),
    quiz=[
        q('Что лежит в `sys.argv[0]`?',
            ['Первый аргумент', 'Имя скрипта', 'Путь к Python', 'Код выхода'],
            1, 'Аргументы — начиная с sys.argv[1].'),
        q('Какой код выхода означает успех?',
            ['1', '0', '-1', '200'],
            1, 'Любой ненулевой — ошибка.'),
        q('Что делает `action="store_true"` в argparse?',
            ['Сохраняет в файл', 'Делает флаг без значения (True, если указан)', 'Проверяет тип', 'Требует аргумент'],
            1, 'Например, --headless.'),
    ],
),

}
