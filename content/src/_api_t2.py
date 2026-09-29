"""Теория модуля «Клиенты и автотесты» темы «Тестирование API».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- api-requests ----------
'api-requests': dict(
    full=t(r'''
## Зачем это нужно

**requests** — самая популярная библиотека Python для HTTP. На ней пишут API-автотесты, скрипты подготовки данных, клиенты сервисов. Её интерфейс простой: метод, адрес, параметры — и объект ответа.

## Запрос и ответ

```py
import requests

r = requests.get("https://api.test/users/1", timeout=5)
r.status_code          # 200
r.ok                   # True, если код < 400
r.json()               # тело как словарь
r.text                 # тело строкой
r.headers["Content-Type"]
r.elapsed              # сколько занял запрос
```

- Методы: `requests.get`, `post`, `put`, `patch`, `delete`.
- `timeout` — **обязательно**: без него зависший сервер повесит тест навсегда.

## Параметры, тело, заголовки

```py
r = requests.post(
    "https://api.test/users",
    params={"notify": "false"},                  # ?notify=false
    json={"name": "Боря"},                       # тело JSON + Content-Type
    headers={"Authorization": "Bearer t1"},
    timeout=5,
)
```

- `params` — строка запроса; requests сам закодирует пробелы и кириллицу. Не склеивай URL руками.
- `json=` — сериализует словарь и ставит `Content-Type: application/json`. `data=` — форма.
- `headers` — заголовки.

## Ошибки

```py
r.raise_for_status()      # HTTPError, если 4xx или 5xx
```

- `requests.ConnectionError` — сервер недоступен, `requests.Timeout` — не ответил вовремя, `requests.HTTPError` — из `raise_for_status()`. Все наследуют `requests.RequestException`.

## Без сети: responses

В этой песочнице (и в юнит-тестах вообще) реальных запросов нет. Библиотека **responses** перехватывает запросы `requests` и отдаёт заданные ответы:

```python
import requests
import responses

with responses.RequestsMock() as mock:
    mock.get("https://api.test/users/1", json={"id": 1, "name": "Аня"}, status=200)
    r = requests.get("https://api.test/users/1", timeout=5)
    print(r.status_code, r.json()["name"])
    print(mock.calls[0].request.url)
```

- `mock.get/post/...(url, json=…, status=…, headers=…)` — зарегистрировать ответ.
- `mock.calls` — все сделанные запросы: можно проверить URL, тело, заголовки.
- Запрос на незарегистрированный адрес → ошибка `ConnectionError`: так видно, что код ходит не туда.
- Вывод: `200 Аня`, `https://api.test/users/1`.

## Итог

- `requests.get/post(url, params=, json=, headers=, timeout=)`.
- `r.status_code`, `r.ok`, `r.json()`, `r.headers`, `r.elapsed`, `r.raise_for_status()`.
- Исключения: ConnectionError, Timeout, HTTPError.
- `responses` — подмена ответов без сети; `calls` — что отправили.
'''),
    short=t(r'''
```py
r = requests.get(url, params={"q": "x"}, headers={...}, timeout=5)
r = requests.post(url, json={"name": "Аня"}, timeout=5)
r.status_code · r.ok · r.json() · r.text · r.headers · r.elapsed
r.raise_for_status()      # HTTPError на 4xx/5xx
# requests.ConnectionError · requests.Timeout
with responses.RequestsMock() as mock:
    mock.get(url, json={...}, status=200)
    ...; mock.calls[0].request.body
```
'''),
    quiz=[
        q('Зачем передавать `timeout` в requests?',
            ['Для скорости', 'Чтобы зависший сервер не повесил тест навсегда', 'Так требует pytest', 'Для кэша'],
            1, 'По умолчанию ожидание бесконечное.'),
        q('Что делает `json=` в `requests.post`?',
            ['Разбирает ответ', 'Отправляет словарь как JSON и ставит Content-Type', 'Добавляет параметры в URL', 'Ничего'],
            1, 'data= — для формы.'),
        q('Что делает библиотека responses?',
            ['Ускоряет requests', 'Подменяет HTTP-ответы без сети', 'Генерирует отчёты', 'Валидирует JSON'],
            1, 'Для тестов без реального сервера.'),
    ],
),

# ---------- api-m2-l1 ----------
'api-m2-l1': dict(
    full=t(r'''
## Зачем это нужно

Автотест API — это pytest-тест, который отправляет запрос и проверяет ответ. Он запускается в CI после каждого изменения и за секунды говорит, не сломался ли контракт. Хороший набор включает позитивные и негативные проверки.

## Структура теста

```py
def test_get_user(client):
    # Arrange — подготовка (данные, клиент)
    # Act — запрос
    resp = client.get("/users/1")
    # Assert — проверки
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == 1
    assert "email" in body
```

- Сначала статус: если он не тот, дальше проверять бессмысленно.
- Затем тело: ключевые поля и значения.

## Позитивные и негативные

```py
def test_unknown_user_404(client):
    resp = client.get("/users/999")
    assert resp.status_code == 404


def test_create_user(client):
    resp = client.post("/users", json={"name": "Боря"})
    assert resp.status_code == 201
    assert resp.json()["name"] == "Боря"
```

- Негативный тест проверяет реакцию на неправильное: несуществующий ресурс, невалидные данные, отсутствие прав.
- Сквозной тест: создать → получить → проверить, что данные сохранились.

## Настоящий pytest с подменой сервера

```py
import pytest
import requests
import responses


@responses.activate
def test_get_user():
    responses.get("https://api.test/users/1", json={"id": 1, "name": "Аня"})
    assert get_user(1) == {"id": 1, "name": "Аня"}


@responses.activate
def test_user_not_found():
    responses.get("https://api.test/users/99", status=404)
    with pytest.raises(requests.HTTPError):
        get_user(99)
```

- `@responses.activate` — включить подмену на время теста.
- Так тестируют собственный код, который ходит в API (клиенты, скрипты), без реального сервера.
- Против настоящего стенда те же тесты работают без `responses` — с реальным `base_url`.

## Проверка отправленного

```py
import json


@responses.activate
def test_create_sends_json():
    responses.post("https://api.test/users", json={"id": 1}, status=201)
    create_user("Аня")
    assert json.loads(responses.calls[0].request.body) == {"name": "Аня"}
```

- `responses.calls` — какие запросы ушли: URL, метод, заголовки, тело.

## Итог

- Тест: запрос → статус → тело; AAA.
- Позитивные, негативные и сквозные сценарии.
- `@responses.activate` + `responses.get/post(...)` — сервер-подделка; `responses.calls` — что отправлено.
'''),
    short=t(r'''
```py
@responses.activate
def test_get_user():
    responses.get(URL, json={"id": 1}, status=200)
    assert get_user(1)["id"] == 1

@responses.activate
def test_404():
    responses.get(URL, status=404)
    with pytest.raises(requests.HTTPError):
        get_user(99)
# json.loads(responses.calls[0].request.body)
```
'''),
    quiz=[
        q('Что обычно проверяют первым в API-тесте?',
            ['Время', 'Статус-код', 'Заголовок Server', 'Порядок ключей'],
            1, 'Если статус неверный, тело может быть любым.'),
        q('Что такое негативный тест?',
            ['Тест, который всегда падает', 'Проверка реакции на неправильные данные или действия', 'Тест без assert', 'Медленный тест'],
            1, 'Например, 404 или 422.'),
        q('Как проверить тело отправленного запроса при использовании responses?',
            ['r.json()', 'responses.calls[0].request.body', 'requests.last', 'Нельзя'],
            1, 'calls хранит отправленные запросы.'),
    ],
),

# ---------- api-client ----------
'api-client': dict(
    full=t(r'''
## Зачем это нужно

Когда тестов сотни, нельзя в каждом писать `requests.get("https://…/users/…", headers=…)`. Базовый адрес меняется между стендами, токен — у каждого пользователя. Поэтому в проектах пишут **API-клиент**: класс, который знает адрес, авторизацию и эндпоинты, логирует запросы для отчёта. Тесты становятся короткими и читаемыми.

## Session

```py
s = requests.Session()
s.headers.update({"Authorization": "Bearer t1"})
s.get("https://api.test/me")        # заголовок уйдёт автоматически
s.get("https://api.test/orders")
```

- `Session` хранит общие заголовки и cookies и переиспользует TCP-соединение — быстрее.

## Базовый клиент

```py
class ApiClient:
    def __init__(self, base_url, token=None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", 10)
        return self.session.request(method, self.base_url + path, **kwargs)

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)
```

- `**kwargs` пробрасывает любые параметры requests (`json`, `params`, `headers`).
- `setdefault("timeout", 10)` — таймаут по умолчанию, если не задан явно.

## Эндпоинты поверх клиента

```py
class UsersApi:
    def __init__(self, client):
        self.client = client

    def get(self, user_id):
        return self.client.request("GET", f"/users/{user_id}")

    def create(self, name, role="qa"):
        return self.client.request("POST", "/users", json={"name": name, "role": role})
```

- Тест: `users.create("Аня")` вместо сырого запроса. Изменится путь — правится одно место.

## Авторизация и фикстуры

```py
@pytest.fixture(scope="session")
def client(base_url):
    token = login(base_url, "qa", os.environ["QA_PASSWORD"])
    return ApiClient(base_url, token=token)
```

- Логин один раз за прогон; пароль — из переменной окружения.
- Для отчёта клиент логирует метод, URL, статус и время (`response.elapsed`) и прикладывает их к Allure.

## Итог

- `requests.Session` — общие заголовки и соединение.
- `ApiClient`: base_url, токен, `request(method, path, **kwargs)` с таймаутом.
- Классы эндпоинтов поверх клиента; клиент — через session-фикстуру.
'''),
    short=t(r'''
```py
class ApiClient:
    def __init__(self, base_url, token=None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
    def request(self, method, path, **kw):
        kw.setdefault("timeout", 10)
        return self.session.request(method, self.base_url + path, **kw)
```
'''),
    quiz=[
        q('Что даёт `requests.Session`?',
            ['Параллельные запросы', 'Общие заголовки, cookies и переиспользование соединения', 'Отчёты', 'Подмену ответов'],
            1, 'Удобно для авторизации.'),
        q('Зачем выносить эндпоинты в отдельный класс?',
            ['Так быстрее', 'Изменится путь — правится одно место, тесты короче', 'Иначе не работает', 'Для Allure'],
            1, 'Как Page Object, только для API.'),
        q('Откуда брать пароль тестового пользователя?',
            ['Из кода теста', 'Из переменной окружения / секретов', 'Из README', 'Из имени ветки'],
            1, 'Секреты не хранят в репозитории.'),
    ],
),

# ---------- api-m2-l2 ----------
'api-m2-l2': dict(
    full=t(r'''
## Зачем это нужно

Код часто зависит от внешних сервисов: почты, платёжного шлюза, другого API. Вызывать их в тестах нельзя (дорого, медленно, нестабильно). **Моки** подменяют зависимость объектом, который отвечает как нужно и запоминает, как его вызвали. Параметризация прогоняет один тест на многих данных.

## unittest.mock.Mock

```python
from unittest.mock import Mock

api = Mock()
api.get.return_value = {"status": "ok"}
print(api.get("/health"))
api.get.assert_called_once_with("/health")
print(api.get.call_count)
```

- У `Mock` любой атрибут — тоже мок; `return_value` — что вернуть.
- `assert_called_once_with(...)` — проверить вызов; `call_count`, `call_args` — сколько раз и с чем.
- Вывод: `{'status': 'ok'}`, `1`.

## side_effect

```python
from unittest.mock import Mock

m = Mock(side_effect=[1, 2, ValueError("стоп")])
print(m(), m())
try:
    m()
except ValueError as e:
    print(e)
```

- Список — последовательные ответы; исключение в списке будет выброшено. Удобно моделировать «два сбоя, потом успех».
- Вывод: `1 2`, `стоп`.

## Последовательные ответы в responses

```python
import requests
import responses

with responses.RequestsMock() as mock:
    mock.get("https://api.test/job", json={"status": "pending"})
    mock.get("https://api.test/job", json={"status": "done"})
    print([requests.get("https://api.test/job").json()["status"] for _ in range(3)])
```

- Ответы на один URL отдаются по порядку регистрации; последний повторяется.
- Вывод: `['pending', 'done', 'done']`.

## Параметризация API-тестов

```py
@pytest.mark.parametrize("code, expected", [(200, True), (503, False), (500, False)])
@responses.activate
def test_status(code, expected):
    responses.get("https://api.test/health", status=code)
    assert is_available("https://api.test/health") == expected
```

- Один тест — много статусов, ролей, невалидных тел.

## Итог

- `Mock`: `return_value`, `side_effect`, `assert_called_once_with`, `call_count`.
- `responses`: несколько ответов на один URL — по очереди.
- `parametrize` — одна проверка на многих данных.
'''),
    short=t(r'''
```py
from unittest.mock import Mock
m = Mock(); m.get.return_value = {...}
m.get.assert_called_once_with("/x"); m.get.call_count
Mock(side_effect=[r1, r2, TimeoutError()])   # по очереди
mock.get(url, status=503); mock.get(url, status=200)   # responses: по порядку
@pytest.mark.parametrize("code, ok", [(200, True), (500, False)])
```
'''),
    quiz=[
        q('Что задаёт `return_value` у Mock?',
            ['Сколько раз вызвать', 'Что вернёт вызов', 'Исключение', 'Имя'],
            1, 'side_effect — последовательность или исключение.'),
        q('Как смоделировать «два сбоя, потом успех»?',
            ['return_value=[...]', 'side_effect=[сбой, сбой, успех]', 'call_count=3', 'Нельзя'],
            1, 'Элементы отдаются по очереди.'),
        q('Что вернёт responses на третий запрос, если зарегистрировано два ответа на URL?',
            ['Ошибку', 'Последний ответ', 'Первый ответ', 'Пустой ответ'],
            1, 'Последний повторяется.'),
    ],
),

}
