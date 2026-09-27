"""Подробная теория и «Проверь себя» для темы «Тестирование API»."""
from ._lib import t

THEORY = {
"api-m1-l1": {"full": t("""
    ## Зачем это нужно

    Большинство современных приложений — это фронтенд (сайт, мобильное приложение), который общается с бэкендом через **API** по протоколу HTTP. Тестировать API выгодно: тесты быстрые, стабильные, не зависят от вёрстки и находят баги раньше, чем они доберутся до интерфейса. Чтобы тестировать API, нужно уверенно читать HTTP-запросы и ответы.

    ## Как это работает

    ### Запрос

    ```http
    POST /v1/orders?debug=1 HTTP/1.1
    Host: api.shop.ru
    Content-Type: application/json
    Authorization: Bearer eyJhbGciOi...

    {"item_id": 42, "count": 2}
    ```

    - **Метод** — что сделать.
    - **URL** — с каким ресурсом: схема (`https`), хост (`api.shop.ru`), путь (`/v1/orders`), query-параметры (`?debug=1`).
    - **Заголовки** — метаданные: формат тела, авторизация, язык.
    - **Тело** — данные (обычно JSON), есть не у всех методов.

    ### Методы

    - `GET` — получить. Тела нет, параметры в URL.
    - `POST` — создать.
    - `PUT` — заменить ресурс целиком.
    - `PATCH` — изменить частично.
    - `DELETE` — удалить.

    **Идемпотентность** — повтор запроса не меняет результат: GET, PUT, DELETE, HEAD, OPTIONS идемпотентны; POST и PATCH — нет. Два одинаковых POST создадут два заказа. Это важно для тест-дизайна: что будет при двойном клике или повторе запроса после таймаута?

    ### Ответ и статус-коды

    - `2xx` успех: `200 OK`, `201 Created` (после создания), `204 No Content` (успех без тела).
    - `3xx` перенаправление: `301`, `302`, `304 Not Modified`.
    - `4xx` ошибка **клиента**: `400` неверный запрос, `401` не авторизован, `403` нет прав, `404` не найдено, `409` конфликт, `422` данные не прошли валидацию, `429` слишком много запросов.
    - `5xx` ошибка **сервера**: `500`, `502 Bad Gateway`, `503` сервис недоступен, `504` таймаут шлюза.

    💡 Для тестировщика: `4xx` на невалидные данные — **правильное** поведение, а `5xx` почти всегда баг — сервер не должен падать от плохого ввода.

    ## Примеры

    ### Пример 1. Разбор URL

    ```python
    from urllib.parse import urlparse, parse_qs

    url = urlparse("https://api.shop.ru/v1/orders?status=new&page=2&page=3")
    print("схема:", url.scheme)
    print("хост:", url.netloc)
    print("путь:", url.path)
    print("параметры:", parse_qs(url.query))
    ```

    ### Пример 2. Сборка URL с кодированием

    ```python
    from urllib.parse import urlencode

    params = {"q": "кофе с молоком", "page": 2}
    print("https://api.shop.ru/search?" + urlencode(params))
    ```

    Пробелы и кириллица в URL должны кодироваться — `urlencode` делает это сам.

    ### Пример 3. Классификация статусов

    ```python
    def status_class(code):
        return {2: "success", 3: "redirect", 4: "client_error", 5: "server_error"}[code // 100]

    for code in [200, 201, 304, 404, 422, 500, 503]:
        print(code, status_class(code))
    ```

    ### Пример 4. Как это выглядит с requests

    В реальном проекте запросы отправляют библиотекой `requests` (в песочнице сети нет, поэтому этот код без кнопки запуска):

    ```py
    import requests

    resp = requests.get("https://api.shop.ru/v1/orders", params={"status": "new"}, timeout=10)
    print(resp.status_code)          # 200
    print(resp.headers["Content-Type"])
    print(resp.json())               # тело как dict/list

    resp = requests.post("https://api.shop.ru/v1/orders",
                         json={"item_id": 42, "count": 2},
                         headers={"Authorization": "Bearer ..."})
    assert resp.status_code == 201
    ```

    ## Частые ошибки

    **Проверять только статус.** `200` с пустым или неверным телом — тоже баг.

    **Считать любой 4xx багом.** `404` на несуществующий ресурс и `422` на невалидные данные — ожидаемое поведение.

    **Запросы без таймаута.** `requests.get(url)` без `timeout` может зависнуть навсегда и подвесить весь прогон.

    ## Шпаргалка

    ```text
    GET — прочитать   POST — создать   PUT — заменить   PATCH — изменить   DELETE — удалить
    2xx ок   3xx редирект   4xx ошибка клиента   5xx ошибка сервера (почти всегда баг)
    200 OK · 201 Created · 204 No Content · 400 · 401 · 403 · 404 · 422 · 500 · 503
    ```
    """), "quiz": [
    {"q": "Какой статус-код правильно вернуть после успешного **создания** ресурса через POST?",
     "options": ["`200`", "`201`", "`204`", "`302`"], "answer": 1,
     "explain": "`201 Created` — ресурс создан. `200` допустим, но менее точен, и в заданиях курса такой ответ считается багом."},
    {"q": "Сервер вернул `500` в ответ на запрос с некорректным email. Это баг?",
     "options": ["Нет, запрос же некорректный", "Да: на плохие данные нужно отвечать `4xx`, а не падать", "Зависит от браузера", "Нет, 500 — это норма"], "answer": 1,
     "explain": "Невалидный ввод — ошибка клиента (`400`/`422`). `500` означает, что сервер не обработал ситуацию — это баг."},
    {"q": "Какой из методов **не** идемпотентен?",
     "options": ["`GET`", "`PUT`", "`DELETE`", "`POST`"], "answer": 3,
     "explain": "Повторный POST обычно создаёт ещё один ресурс. GET, PUT и DELETE при повторе дают тот же результат."},
]},

"api-m1-l2": {"full": t("""
    ## Зачем это нужно

    API почти всегда общается в формате **JSON**. Тест API — это в основном проверка JSON-ответа: все ли поля на месте, правильных ли они типов, корректны ли значения. Чем точнее эти проверки, тем больше багов ловят тесты.

    ## Как это работает

    ### JSON и Python

    - `object {...}` → `dict`
    - `array [...]` → `list`
    - `string` → `str`, `number` → `int`/`float`
    - `true`/`false` → `True`/`False`
    - `null` → `None`

    Модуль `json`:
    - `json.loads(строка)` — строка → объект Python;
    - `json.dumps(объект)` — объект → строка (`ensure_ascii=False` сохранит кириллицу, `indent=2` — красиво).

    ### Что проверять в ответе

    1. **Статус-код.**
    2. **Структура**: все обязательные поля присутствуют, лишних нет (если важно).
    3. **Типы**: `id` — число, `email` — строка, `tags` — список.
    4. **Значения и бизнес-правила**: email содержит `@`, возраст ≥ 0, `id` совпадает с запрошенным, сумма заказа равна сумме позиций.

    В больших проектах структуру описывают схемой (JSON Schema, модели pydantic) и валидируют ответ целиком, но принцип тот же, что ты напишешь руками.

    ### Безопасный доступ

    `data["field"]` упадёт с `KeyError`, если поля нет. `data.get("field")` вернёт `None` — удобно для проверок.

    ## Примеры

    ### Пример 1. loads и dumps

    ```python
    import json

    text = '{"id": 1, "name": "Аня", "tags": ["qa"], "active": true, "boss": null}'
    data = json.loads(text)
    print(type(data).__name__, data["active"], data["boss"])
    print(json.dumps(data, ensure_ascii=False))
    print(json.dumps(data, ensure_ascii=False, indent=2))
    ```

    ### Пример 2. Вложенные данные

    ```python
    resp = {"data": {"users": [{"id": 1, "roles": ["qa", "admin"]}, {"id": 2, "roles": []}]}, "total": 2}
    users = resp["data"]["users"]
    print(len(users) == resp["total"])
    print([u["id"] for u in users if "admin" in u["roles"]])
    ```

    ### Пример 3. Валидатор ответа

    ```python
    def validate_user(data):
        errors = []
        if not isinstance(data.get("id"), int):
            errors.append("id: must be int")
        email = data.get("email")
        if not isinstance(email, str) or "@" not in email:
            errors.append("email: invalid")
        age = data.get("age")
        if not isinstance(age, int) or age < 0:
            errors.append("age: must be >= 0")
        return errors

    for sample in [{"id": 1, "email": "a@b.ru", "age": 30},
                   {"id": "1", "email": "abc", "age": -3},
                   {}]:
        print(sample, "->", validate_user(sample) or "OK")
    ```

    Функция возвращает **все** ошибки сразу, а не падает на первой — так отчёт о баге информативнее.

    ### Пример 4. Проверка бизнес-правила

    ```python
    order = {"items": [{"price": 300, "qty": 2}, {"price": 150, "qty": 1}], "total": 750}
    expected = sum(i["price"] * i["qty"] for i in order["items"])
    print("сумма верна" if expected == order["total"] else f"БАГ: {order['total']} != {expected}")
    ```

    ### Пример 5. Поиск в списке

    ```python
    users = [{"id": 1, "name": "A"}, {"id": 5, "name": "B"}]
    print(next((u for u in users if u["id"] == 5), None))
    print(next((u for u in users if u["id"] == 42), None))
    ```

    ## Частые ошибки

    **`isinstance(True, int)` — `True`!** В Python `bool` — подкласс `int`. Если важно отличать, проверяй `type(x) is int` или сначала исключай `bool`.

    **Сравнение float на равенство** в деньгах — используй целые копейки или `round`.

    **Проверка только «поле есть»**, без типа и значения — пропустит `"id": "1"` вместо `1`.

    ## Шпаргалка

    ```py
    data = json.loads(text)                 # str → dict/list
    json.dumps(obj, ensure_ascii=False)     # dict/list → str
    data.get("x")                           # None вместо KeyError
    isinstance(v, int)                      # тип
    [f for f in required if f not in data]  # отсутствующие поля
    next((x for x in xs if cond), None)     # найти или None
    ```
    """), "quiz": [
    {"q": "Во что превращается JSON-значение `null` после `json.loads`?",
     "options": ["`\"null\"`", "`0`", "`None`", "`False`"], "answer": 2,
     "explain": "`null` в JSON соответствует `None` в Python."},
    {"q": "Что вернёт `{\"id\": 1}.get(\"email\")`?",
     "options": ["`KeyError`", "`None`", "`\"\"`", "`False`"], "answer": 1,
     "explain": "`.get()` не падает на отсутствующем ключе, а возвращает `None` (или значение по умолчанию, если указано)."},
    {"q": "API вернул `{\"id\": \"42\"}`, а по контракту `id` — число. Какая проверка это поймает?",
     "options": ["`\"id\" in data`", "`data[\"id\"] == 42`", "`isinstance(data[\"id\"], int)`", "Любая из них"], "answer": 2,
     "explain": "Наличие поля есть, а `\"42\" == 42` просто `False` без понятной причины. Проверка типа прямо указывает на нарушение контракта."},
]},

"api-m2-l1": {"full": t("""
    ## Зачем это нужно

    Проверять API руками в Postman удобно разово, но регрессию из сотен проверок нужно запускать автоматически — на каждый коммит. Автотест — это функция, которая готовит данные, делает запрос и проверяет ответ. Главное свойство хорошего автотеста: **он падает, когда есть баг**, и проходит, когда всё работает.

    ## Как это работает

    ### pytest

    Самый популярный фреймворк для тестов на Python:
    - тест — функция с именем `test_...`;
    - проверки — обычный `assert`; при провале pytest покажет, что с чем сравнивалось;
    - запуск — `pytest` в терминале, он сам найдёт файлы `test_*.py`.

    ### Структура AAA

    - **Arrange** — подготовка: данные, пользователь, авторизация.
    - **Act** — одно действие: запрос к API.
    - **Assert** — проверки результата.

    ```py
    def test_create_user(client):
        # Arrange
        payload = {"name": "Боря", "email": "bor@ya.ru"}
        # Act
        resp = client.post("/users", json=payload)
        # Assert
        assert resp.status_code == 201
        body = resp.json()
        assert body["name"] == payload["name"]
        assert isinstance(body["id"], int)
    ```

    ### Позитивные и негативные тесты

    - **Позитивный** — корректные данные, ожидаем успех.
    - **Негативный** — некорректные данные или условия (несуществующий id, пустое поле, нет прав), ожидаем **правильную** ошибку: `404`, `422`, `403`.

    Негативных сценариев обычно больше, и именно они чаще находят баги.

    ### Сквозные сценарии

    Создать → получить → изменить → удалить → убедиться, что удалено. Такие цепочки ловят баги, которые не видны по одному запросу: API ответил «создано», но на самом деле не сохранил.

    ### Тест должен уметь падать

    Тест без проверок проходит всегда — он бесполезен. Хорошая привычка: временно «сломай» ожидаемое значение и убедись, что тест упал.

    ## Примеры

    ### Пример 1. Фейковый клиент и тест

    Здесь вместо сети — простой класс с таким же интерфейсом, как у `requests`:

    ```python
    class Resp:
        def __init__(self, status_code, data):
            self.status_code, self._data = status_code, data
        def json(self):
            return self._data

    class FakeAPI:
        def __init__(self):
            self.users = {1: {"id": 1, "name": "Аня"}}
        def get(self, path):
            uid = int(path.split("/")[-1])
            if uid in self.users:
                return Resp(200, self.users[uid])
            return Resp(404, {"error": "not found"})

    def test_get_user(client):
        resp = client.get("/users/1")
        assert resp.status_code == 200
        assert resp.json()["id"] == 1

    def test_unknown_user_404(client):
        assert client.get("/users/999").status_code == 404

    for test in [test_get_user, test_unknown_user_404]:
        test(FakeAPI())
        print("✅", test.__name__)
    ```

    ### Пример 2. Хороший тест ловит баг

    ```python
    class Resp:
        def __init__(self, status_code, data):
            self.status_code, self._data = status_code, data
        def json(self):
            return self._data

    class BrokenAPI:
        def get(self, path):
            return Resp(200, {"id": 999, "name": "кто-то другой"})   # баг: чужой пользователь

    def weak_test(client):
        assert client.get("/users/1").status_code == 200

    def strong_test(client):
        resp = client.get("/users/1")
        assert resp.status_code == 200
        assert resp.json()["id"] == 1, f"ожидали id=1, получили {resp.json()['id']}"

    for test in [weak_test, strong_test]:
        try:
            test(BrokenAPI())
            print(test.__name__, "— прошёл (баг НЕ пойман)")
        except AssertionError as e:
            print(test.__name__, "— упал, баг пойман:", e)
    ```

    ### Пример 3. Сквозной сценарий

    ```python
    class Resp:
        def __init__(self, status_code, data=None):
            self.status_code, self._data = status_code, data
        def json(self):
            return self._data

    class FakeAPI:
        def __init__(self):
            self.db, self.next_id = {}, 1
        def post(self, path, json):
            user = {"id": self.next_id, **json}
            self.db[self.next_id] = user
            self.next_id += 1
            return Resp(201, user)
        def get(self, path):
            uid = int(path.split("/")[-1])
            return Resp(200, self.db[uid]) if uid in self.db else Resp(404)
        def delete(self, path):
            uid = int(path.split("/")[-1])
            return Resp(204) if self.db.pop(uid, None) else Resp(404)

    api = FakeAPI()
    created = api.post("/users", json={"name": "Вика"}).json()
    assert api.get(f"/users/{created['id']}").json()["name"] == "Вика"
    assert api.delete(f"/users/{created['id']}").status_code == 204
    assert api.get(f"/users/{created['id']}").status_code == 404
    print("сквозной сценарий пройден:", created)
    ```

    ## Частые ошибки

    **Несколько действий в одном тесте** — непонятно, что именно сломалось. Один тест — один сценарий.

    **Зависимость тестов друг от друга** (второй использует пользователя, созданного первым). Тесты должны работать в любом порядке и по одному.

    **Магические значения.** `assert body["name"] == "Боря"` лучше писать как `== payload["name"]` — меньше рассинхрона.

    **Assert без сообщения** на сложных проверках — добавляй текст: `assert x == y, f"ожидали {y}, получили {x}"`.

    ## Шпаргалка

    ```py
    def test_что_проверяем(client):
        # Arrange
        payload = {...}
        # Act
        resp = client.post("/items", json=payload)
        # Assert
        assert resp.status_code == 201
        assert resp.json()["name"] == payload["name"]
    ```
    """), "quiz": [
    {"q": "Тест `def test_x(client): client.get(\"/users/1\")` — без единого assert. Что с ним не так?",
     "options": ["Всё хорошо", "Он проходит всегда, даже когда API сломан — багов не ловит", "Он всегда падает", "pytest его не найдёт"], "answer": 1,
     "explain": "Тест без проверок не может упасть по результату запроса. Он создаёт ложное ощущение, что всё протестировано."},
    {"q": "Что из перечисленного — негативный тест?",
     "options": ["Создать пользователя с корректными данными", "Запросить несуществующего пользователя и ожидать 404", "Получить список пользователей", "Проверить, что GET /health возвращает 200"], "answer": 1,
     "explain": "Негативный тест проверяет правильную реакцию системы на некорректные условия."},
    {"q": "Что означает буква «A» посередине в AAA?",
     "options": ["Assert", "Act — выполнить действие", "Arrange", "API"], "answer": 1,
     "explain": "Arrange (подготовка) → Act (действие) → Assert (проверка)."},
]},

"api-m2-l2": {"full": t("""
    ## Зачем это нужно

    Два приёма, без которых не обходится ни один серьёзный набор API-тестов:
    - **параметризация** — один тест, много наборов данных (все невалидные email, все граничные значения);
    - **моки** — подмена внешних зависимостей (почта, платёжный шлюз, сторонний API), чтобы тест не зависел от них и мог проверить, **как** с ними общается код.

    ## Как это работает

    ### Параметризация в pytest

    ```py
    import pytest

    @pytest.mark.parametrize("email, expected", [
        ("a@b.ru", 201),
        ("", 422),
        ("no-at-sign", 422),
        ("a" * 300 + "@b.ru", 422),
    ])
    def test_register(client, email, expected):
        resp = client.post("/register", json={"email": email})
        assert resp.status_code == expected
    ```

    pytest запустит **4 отдельных теста** — и в отчёте будет видно, какой именно набор данных упал.

    ### Моки: unittest.mock

    `Mock()` — объект, который принимает любые вызовы, возвращает то, что настроишь, и запоминает, как его вызывали:

    - `m.method.return_value = X` — что вернёт вызов;
    - `m.method.side_effect = [A, B, Error()]` — вернуть по очереди A, B, потом выбросить исключение;
    - `m.method.assert_called_once_with(...)` — проверить вызов;
    - `m.method.call_count`, `m.method.call_args` — как вызывали.

    ### Dependency injection

    Чтобы подставить мок, зависимость нужно **передать** в код (аргументом или в конструктор), а не создавать внутри. Это делает код тестируемым.

    ### Retry

    Сервер может временно отвечать `503`. Повторять имеет смысл только `5xx` и сетевые ошибки, и только ограниченное число раз. `4xx` повторять бессмысленно: запрос неверен.

    ## Примеры

    ### Пример 1. Mock: return_value и проверка вызовов

    ```python
    from unittest.mock import Mock

    api = Mock()
    api.get.return_value = {"status": "ok"}
    print(api.get("/health"))
    api.get("/users")
    print("вызовов:", api.get.call_count)
    print("последний вызов:", api.get.call_args)
    api.get.assert_called_with("/users")
    print("assert_called_with прошёл")
    ```

    ### Пример 2. side_effect — последовательность и ошибки

    ```python
    from unittest.mock import Mock

    m = Mock(side_effect=[503, 502, 200])
    print(m(), m(), m())

    boom = Mock(side_effect=TimeoutError("сервер не ответил"))
    try:
        boom()
    except TimeoutError as e:
        print("поймали:", e)
    ```

    ### Пример 3. Тестируем код, который шлёт письма

    ```python
    from unittest.mock import Mock

    def register(email, mailer):
        if "@" not in email:
            raise ValueError("invalid email")
        mailer.send(email, "Добро пожаловать!")
        return True

    mailer = Mock()
    assert register("a@b.ru", mailer) is True
    mailer.send.assert_called_once_with("a@b.ru", "Добро пожаловать!")
    print("письмо отправлено правильно")

    mailer = Mock()
    try:
        register("плохой", mailer)
    except ValueError:
        pass
    print("писем при ошибке:", mailer.send.call_count)
    ```

    ### Пример 4. Retry с моком

    ```python
    from unittest.mock import Mock

    def resp(code):
        r = Mock()
        r.status_code = code
        return r

    def get_with_retry(client, path, attempts=3):
        for _ in range(attempts):
            r = client.get(path)
            if r.status_code < 500:
                return r
        return r

    client = Mock()
    client.get.side_effect = [resp(503), resp(502), resp(200)]
    print(get_with_retry(client, "/x").status_code, "за", client.get.call_count, "запроса")

    client = Mock()
    client.get.side_effect = [resp(404)]
    print(get_with_retry(client, "/x").status_code, "за", client.get.call_count, "запрос")
    ```

    ### Пример 5. Параметризация вручную

    ```python
    def is_valid_email(email):
        return "@" in email and "." in email.split("@")[-1] and len(email) <= 254

    cases = [("a@b.ru", True), ("", False), ("no-at", False), ("a@b", False), ("x" * 260 + "@b.ru", False)]
    for value, expected in cases:
        got = is_valid_email(value)
        mark = "✅" if got == expected else "❌"
        print(mark, repr(value[:20]), "->", got)
    ```

    ## Частые ошибки

    **Мокать то, что тестируешь.** Мок заменяет **зависимости**, а не проверяемую логику.

    **`assert_called_once_with` с опечаткой в имени** (`assert_called_onse_with`) — в старых версиях Python такой вызов молча «проходил». Копируй имена методов внимательно.

    **Бесконечный retry** или retry на `4xx` — тесты зависают или маскируют настоящие ошибки.

    ## Шпаргалка

    ```py
    from unittest.mock import Mock
    m = Mock()
    m.f.return_value = 1
    m.f.side_effect = [1, 2, Exception()]
    m.f.assert_called_once_with(arg)
    m.f.call_count

    @pytest.mark.parametrize("x, expected", [(1, 2), (2, 4)])
    def test_double(x, expected): assert double(x) == expected
    ```
    """), "quiz": [
    {"q": "Что вернёт третий вызов `m()` для `m = Mock(side_effect=[1, 2, ValueError()])`?",
     "options": ["`3`", "`ValueError()` как значение", "Будет выброшено исключение `ValueError`", "`None`"], "answer": 2,
     "explain": "Если элемент `side_effect` — исключение, мок его выбрасывает, а не возвращает."},
    {"q": "Зачем параметризовать тест через `@pytest.mark.parametrize`?",
     "options": ["Чтобы тест работал быстрее", "Чтобы прогнать одну проверку на многих наборах данных, видя в отчёте каждый набор отдельно", "Чтобы отключить тест", "Чтобы тест запускался параллельно"], "answer": 1,
     "explain": "Каждый набор данных становится отдельным тестом — сразу видно, на каком значении система ошибается."},
    {"q": "На какие ответы разумно делать повтор запроса (retry)?",
     "options": ["На любые", "На `404` и `422`", "На `5xx` и сетевые ошибки, ограниченное число раз", "Только на `200`"], "answer": 2,
     "explain": "`5xx` и таймауты бывают временными. `4xx` означает неверный запрос — повтор даст тот же результат."},
]},
}
