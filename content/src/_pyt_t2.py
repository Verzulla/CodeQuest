"""Теория модуля «Фикстуры и параметризация» темы «pytest».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- pyt-fixtures ----------
'pyt-fixtures': dict(
    full=t(r'''
## Зачем это нужно

Почти каждому тесту нужна подготовка: тестовый пользователь, клиент API, открытый браузер, чистая база. Копировать подготовку в каждый тест — плохо. **Фикстура** описывает подготовку один раз, а pytest сам передаёт результат в тесты, которым он нужен, и сам убирает за собой.

## Фикстура и её использование

```py
import pytest


@pytest.fixture
def user():
    return {"name": "anna", "role": "qa"}


def test_role(user):
    assert user["role"] == "qa"
```

- `@pytest.fixture` превращает функцию в фикстуру.
- Тест **называет её параметром**: pytest видит параметр `user`, находит фикстуру с таким именем, вызывает её и подставляет результат. Вызывать `user()` самому не нужно.
- Каждый тест получает **свой** свежий результат (по умолчанию фикстура вызывается заново для каждого теста) — тесты не влияют друг на друга.
- Опечатка в имени параметра → `fixture 'usr' not found` со списком доступных фикстур.

## Фикстуры из фикстур

```py
@pytest.fixture
def base_url():
    return "https://api.test"


@pytest.fixture
def users_url(base_url):
    return base_url + "/users"
```

- Фикстура тоже может запрашивать другие фикстуры параметрами — получается цепочка зависимостей.

## Подготовка и уборка: yield

```py
@pytest.fixture
def api():
    token = login()          # подготовка (setup)
    yield token              # значение для теста
    logout(token)            # уборка (teardown)
```

- Код до `yield` выполняется перед тестом, после — после теста, **даже если тест упал**.
- Порядок для теста с такой фикстурой: setup → тест → teardown.
- Так закрывают браузеры, удаляют тестовые данные, откатывают транзакции.

## Фабрика

```py
@pytest.fixture
def make_user():
    def make(name, role="qa"):
        return {"name": name, "role": role}
    return make


def test_two_users(make_user):
    anna = make_user("anna")
    boss = make_user("boss", role="admin")
    assert anna["role"] != boss["role"]
```

- Фикстура возвращает **функцию**: тест сам создаёт столько объектов, сколько нужно, с нужными параметрами.

## Итог

- `@pytest.fixture` + имя фикстуры в параметрах теста.
- По умолчанию — свежее значение на каждый тест.
- `yield`: до — setup, после — teardown (выполняется всегда).
- Фикстуры могут зависеть от фикстур; фабрика возвращает функцию.
'''),
    short=t(r'''
```py
@pytest.fixture
def user():
    return {"name": "anna"}

@pytest.fixture
def api(base_url):          # фикстура из фикстуры
    token = login()
    yield token             # до — setup, после — teardown
    logout(token)

def test_x(user, api): ...  # pytest подставит по именам
```
'''),
    quiz=[
        q('Как тест получает фикстуру?',
            ['Вызывает user()', 'Указывает её имя параметром', 'Импортирует', 'Через global'],
            1, 'pytest подставит результат сам.'),
        q('Когда выполняется код после `yield` в фикстуре?',
            ['Перед тестом', 'После теста, даже если он упал', 'Только при успехе', 'Никогда'],
            1, 'Это teardown.'),
        q('Сколько раз по умолчанию вызывается фикстура для 3 тестов, которые её используют?',
            ['1', '3', '0', 'Зависит от порядка'],
            1, 'scope="function" — на каждый тест.'),
    ],
),

# ---------- pyt-scope ----------
'pyt-scope': dict(
    full=t(r'''
## Зачем это нужно

Открыть браузер или авторизоваться в API — долго. Делать это перед каждым из 500 тестов — непозволительно. **Scope** (область видимости) задаёт, как часто создаётся фикстура. А `conftest.py` делает фикстуры доступными всем тестам проекта.

## scope

```py
@pytest.fixture(scope="session")
def auth_token():
    return login("qa", "secret")


@pytest.fixture(scope="module")
def db():
    conn = connect()
    yield conn
    conn.close()
```

- `function` (по умолчанию) — на каждый тест.
- `class` — на класс тестов, `module` — на файл, `package` — на пакет.
- `session` — один раз на весь прогон.
- Фикстура с широким scope не может зависеть от фикстуры с узким (session от function) — pytest выдаст ошибку.
- Осторожно с изменяемыми объектами в session-фикстурах: если тест их меняет, это увидят следующие тесты.

## autouse

```py
@pytest.fixture(autouse=True)
def clean_state():
    STATE.clear()
```

- Применяется ко всем тестам в зоне видимости **без** упоминания в параметрах. Удобно для общей подготовки: очистка, логирование, скриншот при падении.

## conftest.py

```bash
tests/
  conftest.py          # фикстуры для всех тестов
  api/
    conftest.py        # фикстуры только для tests/api
    test_users.py
  ui/
    test_login.py
```

- Фикстуры из `conftest.py` доступны всем тестам в этой папке и вложенных — **без импорта**.
- Вложенный `conftest.py` может добавлять свои фикстуры или переопределять общие.
- Туда же кладут хуки pytest — например, свои опции командной строки.

## Своя опция командной строки

```py
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--env", default="dev", help="стенд")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")
```

```bash
$ pytest --env stage
```

- `pytest_addoption` — хук, в котором регистрируют опции.
- `request` — встроенная фикстура с информацией о тесте и конфиге; `request.config.getoption` читает значение.

## Итог

- `scope`: function, class, module, package, session.
- `autouse=True` — для всех тестов без параметра.
- `conftest.py` — общие фикстуры и хуки, без импорта.
- `pytest_addoption` + `request.config.getoption` — свои флаги.
'''),
    short=t(r'''
```py
@pytest.fixture(scope="session")   # function|class|module|package|session
def token(): ...

@pytest.fixture(autouse=True)      # для всех тестов
def clean(): ...

# conftest.py — фикстуры без импорта для папки и вложенных
def pytest_addoption(parser):
    parser.addoption("--env", default="dev")

@pytest.fixture
def env(request):
    return request.config.getoption("--env")
```
'''),
    quiz=[
        q('Какой scope создаёт фикстуру один раз за весь прогон?',
            ['function', 'module', 'session', 'global'],
            2, 'Для авторизации, браузера и т.п.'),
        q('Где разместить фикстуры, чтобы они были доступны всем тестам папки без импорта?',
            ['fixtures.py', 'conftest.py', '__init__.py', 'pytest.ini'],
            1, 'Pytest загружает conftest.py сам.'),
        q('Что делает `autouse=True`?',
            ['Ускоряет', 'Применяет фикстуру ко всем тестам без параметра', 'Кэширует', 'Отключает фикстуру'],
            1, 'Не нужно указывать её в каждом тесте.'),
    ],
),

# ---------- pyt-param ----------
'pyt-param': dict(
    full=t(r'''
## Зачем это нужно

Одну и ту же проверку часто нужно выполнить на многих данных: десять вариантов email, пять ролей, все граничные значения. Копировать тест десять раз — плохо. **Параметризация** запускает один тест на наборе данных, и каждый набор — отдельный тест в отчёте.

## parametrize

```py
@pytest.mark.parametrize("value, expected", [
    ("a@b.ru", True),
    ("no-at.ru", False),
    ("@b.ru", False),
])
def test_email(value, expected):
    assert is_valid_email(value) == expected
```

- Первый аргумент — имена параметров строкой через запятую.
- Второй — список наборов (кортежей), по одному на тест.
- В отчёте: `test_email[a@b.ru-True]`, `test_email[no-at.ru-False]`… — упадёт только конкретный случай.

## Понятные имена: ids

```py
@pytest.mark.parametrize("code, ok", [(200, True), (404, False)], ids=["ok", "not_found"])
def test_status(code, ok):
    assert is_success(code) == ok
```

- `ids` — список имён или функция. В отчёте `test_status[ok]` вместо `test_status[200-True]`.
- Данные из словарей: `ids=[c["name"] for c in CASES]`.

## Все комбинации

```py
@pytest.mark.parametrize("browser", ["chrome", "firefox"])
@pytest.mark.parametrize("lang", ["ru", "en", "de"])
def test_home(browser, lang):
    ...
```

- Два декоратора — декартово произведение: 2 × 3 = 6 тестов.

## Отдельный случай с маркером

```py
@pytest.mark.parametrize("value, expected", [
    (1.234, 1.23),
    pytest.param(2.675, 2.68, marks=pytest.mark.xfail(reason="float")),
])
def test_round(value, expected):
    assert round(value, 2) == expected
```

- `pytest.param(..., marks=..., id=...)` — пометить отдельный набор (xfail, skip) или дать ему имя.

## Параметризованная фикстура

```py
@pytest.fixture(params=["admin", "qa", "guest"])
def role(request):
    return request.param


def test_can_view(role):
    assert can_view(role)
```

- Каждый тест, использующий фикстуру, запустится для каждого параметра: `test_can_view[admin]`, `[qa]`, `[guest]`.

## Итог

- `@pytest.mark.parametrize("a, b", [(…), (…)])` — тест на наборе данных.
- `ids=` — имена случаев; два декоратора — все комбинации.
- `pytest.param(..., marks=...)` — маркер для одного случая.
- `@pytest.fixture(params=[...])` + `request.param`.
'''),
    short=t(r'''
```py
@pytest.mark.parametrize("value, expected", [("a@b.ru", True), ("x", False)],
                         ids=["valid", "no_at"])
def test_email(value, expected): ...

@pytest.mark.parametrize("b", ["chrome", "firefox"])
@pytest.mark.parametrize("lang", ["ru", "en"])     # 2 × 2 = 4 теста
def test_home(b, lang): ...

pytest.param(2.675, 2.68, marks=pytest.mark.xfail)
@pytest.fixture(params=["admin", "qa"])            # request.param
```
'''),
    quiz=[
        q('Сколько тестов создадут два декоратора parametrize по 2 и 3 значения?',
            ['5', '6', '2', '3'],
            1, 'Все комбинации.'),
        q('Зачем нужен `ids`?',
            ['Ускорить', 'Дать случаям понятные имена в отчёте', 'Пропустить случаи', 'Задать порядок'],
            1, 'test_status[ok] понятнее, чем test_status[200-True].'),
        q('Как пометить xfail только один набор данных?',
            ['@pytest.mark.xfail на тесте', 'pytest.param(..., marks=pytest.mark.xfail)', 'ids="xfail"', 'Нельзя'],
            1, 'Маркер на конкретный случай.'),
    ],
),

# ---------- pyt-builtin ----------
'pyt-builtin': dict(
    full=t(r'''
## Зачем это нужно

У pytest есть готовые фикстуры для частых задач: временные файлы, подмена переменных окружения и функций, перехват вывода. Они избавляют от ручной уборки и делают тесты изолированными.

## tmp_path: временная папка

```py
def test_save(tmp_path):
    path = tmp_path / "report.txt"
    save_report(path, "passed: 5")
    assert path.read_text(encoding="utf-8") == "passed: 5"
```

- `tmp_path` — `pathlib.Path` к уникальной пустой папке для **этого** теста. Не нужно думать об уборке и конфликтах между тестами.
- `tmp_path_factory` — то же для session-фикстур.

## monkeypatch: подмены

```py
def test_env(monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://stage.example.com")
    assert base_url() == "https://stage.example.com"


def test_down(monkeypatch):
    monkeypatch.setattr(service, "fetch_status", lambda: 503)
    assert service.status_text() == "недоступен"
```

- `setenv` / `delenv` — переменные окружения.
- `setattr(объект, "имя", значение)` — подменить атрибут: функцию модуля, метод класса, константу. Так отрезают сеть, время, случайность.
- `setitem(словарь, ключ, значение)` — подменить элемент словаря.
- После теста **всё возвращается как было** — подмены не протекают.

## capsys: вывод

```py
def test_greet(capsys):
    greet("Аня")
    captured = capsys.readouterr()
    assert captured.out == "Привет, Аня!\n"
    assert captured.err == ""
```

- `readouterr()` возвращает то, что напечатано с прошлого вызова: `.out` — stdout, `.err` — stderr.
- `caplog` — то же для модуля `logging`: `caplog.text`, `caplog.records`.

## request

- `request` — информация о текущем тесте: `request.node.name` (имя теста), `request.param` (для параметризованных фикстур), `request.config` (конфиг и опции).

## Список фикстур

```bash
$ pytest --fixtures
```

- Все доступные фикстуры с описаниями: встроенные, из плагинов и из твоих `conftest.py`.

## Итог

- `tmp_path` — временная папка на тест.
- `monkeypatch.setenv/setattr/setitem` — подмены с автоматическим откатом.
- `capsys.readouterr().out` — напечатанное; `caplog` — логи.
- `request` — данные о тесте; `pytest --fixtures` — список фикстур.
'''),
    short=t(r'''
```py
def test_file(tmp_path):
    p = tmp_path / "a.txt"; p.write_text("x")

def test_env(monkeypatch):
    monkeypatch.setenv("BASE_URL", "http://x")
    monkeypatch.setattr(module, "fetch", lambda: 503)

def test_print(capsys):
    greet("Аня")
    assert capsys.readouterr().out == "Привет, Аня!\n"
# caplog, request, pytest --fixtures
```
'''),
    quiz=[
        q('Что вернёт `tmp_path`?',
            ['Строку /tmp', 'Уникальную временную папку для теста (Path)', 'Текущую папку', 'Путь к тесту'],
            1, 'Своя папка на каждый тест.'),
        q('Что происходит с подменами monkeypatch после теста?',
            ['Остаются', 'Откатываются автоматически', 'Сохраняются в файл', 'Зависят от scope'],
            1, 'Тесты изолированы.'),
        q('Какой фикстурой проверить напечатанный текст?',
            ['tmp_path', 'monkeypatch', 'capsys', 'request'],
            2, 'capsys.readouterr().out.'),
    ],
),

}
