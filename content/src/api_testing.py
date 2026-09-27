"""Тема «Тестирование API».

Сети в песочнице нет, поэтому практика — на имитации HTTP-клиента.
В заданиях «напиши тест» ученик пишет функцию test_*, а проверка
запускает её против исправного API (тест должен пройти) и против
сломанного (тест должен упасть с AssertionError).
"""
from textwrap import dedent

from ._lib import t, cod, lesson, module, out, topic

P = "api"

# Общий кусок проверок для заданий «напиши тест»: фейковый клиент.
FAKE = '''
class Resp:
    def __init__(self, status_code, data=None):
        self.status_code = status_code
        self._data = data

    def json(self):
        return self._data


class Client:
    """Имитация API. broken — какой баг «сломать» в ответах."""
    def __init__(self, broken=None):
        self.broken = broken
        self.users = {1: {"id": 1, "name": "Аня", "email": "anna@mail.ru"}}

    def get(self, path):
        if self.broken == "500":
            return Resp(500, {"error": "internal"})
        uid = int(path.rstrip("/").split("/")[-1])
        if uid not in self.users:
            return Resp(200 if self.broken == "no404" else 404, {"error": "not found"})
        user = dict(self.users[uid])
        if self.broken == "wrong_id":
            user["id"] = 999
        if self.broken == "no_email":
            del user["email"]
        return Resp(200, user)

    def post(self, path, json=None):
        if self.broken == "500":
            return Resp(500, {"error": "internal"})
        new = {"id": len(self.users) + 1, **(json or {})}
        if self.broken == "lost_name":
            new["name"] = None
        self.users[new["id"]] = new
        return Resp(200 if self.broken == "status200" else 201, new)


def must_fail(test_func, client, why):
    try:
        test_func(client)
    except AssertionError:
        return
    assert False, f"Твой тест не поймал баг: {why}"
'''

def with_fake(tests):
    return FAKE + dedent(tests)


m1 = module(f"{P}-m1", "HTTP для тестировщика", "🌐", "Методы, статус-коды, URL и JSON",
    lesson(f"{P}-m1-l1", "Запрос и ответ", """
        # Как устроен HTTP

        Клиент отправляет **запрос**, сервер возвращает **ответ**.

        **Запрос:** метод + URL + заголовки + (иногда) тело.
        ```
        POST https://api.shop.ru/v1/orders?debug=1
        Content-Type: application/json

        {"item": 42, "count": 2}
        ```

        **Методы:**
        - `GET` — получить, `POST` — создать, `PUT` — заменить целиком, `PATCH` — изменить частично, `DELETE` — удалить.
        - **Идемпотентный** метод даёт тот же результат при повторе: GET, PUT, DELETE. POST — нет (два POST = два заказа).

        **Статус-коды** — первая цифра говорит главное:
        - `2xx` успех: 200 OK, 201 Created, 204 No Content
        - `3xx` перенаправление: 301, 302, 304
        - `4xx` ошибка клиента: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Unprocessable
        - `5xx` ошибка сервера: 500, 502 Bad Gateway, 503, 504

        💡 Для тестировщика: `4xx` на невалидные данные — это **правильное** поведение, а `5xx` почти всегда баг.
        """,
        out(f"{P}-m1-l1-e1", "Что выведет программа? Класс статус-кода — это первая цифра.", """
            for code in [201, 404, 503]:
                print(code, code // 100)
            """),
        out(f"{P}-m1-l1-e2", "Что выведет программа? Разбираем URL стандартной библиотекой.", """
            from urllib.parse import urlparse, parse_qs

            url = urlparse("https://api.shop.ru/v1/orders?status=new&page=2")
            print(url.netloc)
            print(url.path)
            print(parse_qs(url.query))
            """),
        cod(f"{P}-m1-l1-e3", t("""
            Напиши функцию `status_class(code)`, которая определяет класс HTTP-ответа по его коду.

            - Получает: `code` — трёхзначный код ответа (число от 200 до 599).
            - Возвращает строку по первой цифре кода:
              - `2xx` → `"success"`
              - `3xx` → `"redirect"`
              - `4xx` → `"client_error"`
              - `5xx` → `"server_error"`

            Примеры:
            ```
            status_class(200)   # → "success"
            status_class(301)   # → "redirect"
            status_class(404)   # → "client_error"
            status_class(503)   # → "server_error"
            ```
            Первая цифра числа — это `code // 100`.
            """),
            """
            def status_class(code):
                pass
            """,
            """
            def test_classes():
                got = [status_class(c) for c in (200, 204, 301, 404, 422, 500, 503)]
                assert got == ["success", "success", "redirect", "client_error", "client_error", "server_error", "server_error"], f"Получено {got}"
            """,
            """
            def status_class(code):
                return {2: "success", 3: "redirect", 4: "client_error", 5: "server_error"}[code // 100]
            """,
            hint="`code // 100` даёт первую цифру."),
        cod(f"{P}-m1-l1-e4", t("""
            Напиши функцию `is_idempotent(method)`, которая определяет, идемпотентен ли HTTP-метод.

            Идемпотентный метод при повторе даёт тот же результат, что и при одном вызове.

            - Получает: `method` — название метода строкой. Регистр может быть любым: `"GET"`, `"get"`, `"Delete"`.
            - Возвращает:
              - `True` для `GET`, `HEAD`, `OPTIONS`, `PUT`, `DELETE`;
              - `False` для `POST` и `PATCH`.

            Примеры:
            ```
            is_idempotent("GET")      # → True
            is_idempotent("Delete")   # → True
            is_idempotent("post")     # → False
            ```
            Приведи метод к одному регистру через `.upper()`.
            """),
            """
            def is_idempotent(method):
                pass
            """,
            """
            def test_values():
                assert all(is_idempotent(m) for m in ["GET", "put", "Delete", "HEAD"]), "GET, PUT, DELETE, HEAD — идемпотентны"
                assert not is_idempotent("POST") and not is_idempotent("patch"), "POST и PATCH — нет"
            """,
            """
            def is_idempotent(method):
                return method.upper() in {"GET", "HEAD", "OPTIONS", "PUT", "DELETE"}
            """),
        cod(f"{P}-m1-l1-e5", t("""
            Напиши функцию `build_url(base, path, params)`, которая собирает адрес запроса с параметрами.

            - Получает:
              - `base` — адрес сервера, например `"https://api.ru"`;
              - `path` — путь, например `"/users"`;
              - `params` — словарь query-параметров (может быть пустым).
            - Возвращает строку `base + path`, а если параметры есть — ещё `?` и параметры в формате `ключ=значение`, соединённые через `&`.

            Примеры:
            ```
            build_url("https://api.ru", "/users", {"page": 2, "limit": 10})
            # → "https://api.ru/users?page=2&limit=10"

            build_url("https://api.ru", "/health", {})
            # → "https://api.ru/health"          без параметров — без знака ?

            build_url("https://api.ru", "/s", {"q": "a b"})
            # → "https://api.ru/s?q=a+b"         пробел кодируется как +
            ```
            Строку параметров с правильным кодированием соберёт `urlencode(params)` из `urllib.parse`.
            """),
            """
            from urllib.parse import urlencode

            def build_url(base, path, params):
                pass
            """,
            """
            def test_url():
                assert build_url("https://api.ru", "/users", {"page": 2, "limit": 10}) == "https://api.ru/users?page=2&limit=10", \\
                    f"Получено {build_url('https://api.ru', '/users', {'page': 2, 'limit': 10})}"

            def test_no_params():
                assert build_url("https://api.ru", "/health", {}) == "https://api.ru/health", "Без параметров знака ? быть не должно"

            def test_encoding():
                assert build_url("https://api.ru", "/s", {"q": "a b"}) == "https://api.ru/s?q=a+b", "Пробел должен кодироваться"
            """,
            """
            from urllib.parse import urlencode

            def build_url(base, path, params):
                url = base + path
                return f"{url}?{urlencode(params)}" if params else url
            """,
            hint="`urlencode({\"a\": 1, \"b\": 2})` → `\"a=1&b=2\"`. Не забудь случай без параметров.", xp=20),
        cod(f"{P}-m1-l1-e6", t("""
            Напиши функцию `is_bug(method, status)` для быстрого разбора ответов API: баг это или нет.

            - Получает: `method` — HTTP-метод (`"GET"`, `"POST"`, …); `status` — код ответа.
            - Возвращает `True` (это баг), если выполнено **хотя бы одно**:
              1. код ответа `5xx` (500 и больше) — сервер упал;
              2. метод `POST` вернул `200` — при создании ресурса положено `201 Created`.

            Во всех остальных случаях — `False`.

            Примеры:
            ```
            is_bug("GET", 500)    # → True
            is_bug("POST", 200)   # → True
            is_bug("POST", 201)   # → False
            is_bug("GET", 404)    # → False   404 на несуществующее — нормальное поведение
            ```
            """),
            """
            def is_bug(method, status):
                pass
            """,
            """
            def test_5xx():
                assert is_bug("GET", 500) and is_bug("POST", 502), "5xx — всегда баг"

            def test_post_200():
                assert is_bug("POST", 200) is True, "POST должен возвращать 201 Created"

            def test_ok():
                assert not is_bug("GET", 200) and not is_bug("POST", 201) and not is_bug("GET", 404), "Это не баги"
            """,
            """
            def is_bug(method, status):
                return status >= 500 or (method == "POST" and status == 200)
            """),
    ),
    lesson(f"{P}-m1-l2", "JSON и валидация ответа", """
        # JSON

        API обычно отвечает в формате JSON. В Python это словари и списки:

        ```
        import json
        text = '{"id": 1, "name": "Аня", "tags": ["qa"], "active": true, "boss": null}'
        data = json.loads(text)     # строка → объект
        data["name"]                # 'Аня'
        json.dumps(data)            # объект → строка
        ```

        Соответствие типов: `object → dict`, `array → list`, `true/false → True/False`, `null → None`.

        # Что проверять в ответе

        1. Статус-код.
        2. **Структуру**: все обязательные поля на месте.
        3. **Типы**: `id` — число, `email` — строка…
        4. **Значения**: email содержит `@`, возраст неотрицательный, `id` совпадает с запрошенным.

        В реальных проектах для этого используют JSON Schema или pydantic, но принцип тот же.
        """,
        out(f"{P}-m1-l2-e1", "Что выведет программа?", """
            import json
            data = json.loads('{"ok": true, "items": [1, 2], "next": null}')
            print(data["ok"], data["next"], len(data["items"]))
            print(type(data).__name__)
            """),
        out(f"{P}-m1-l2-e2", "Что выведет программа? Доступ к вложенным данным.", """
            resp = {"data": {"users": [{"name": "Аня", "roles": ["qa", "admin"]}, {"name": "Боря", "roles": []}]}}
            print(resp["data"]["users"][0]["roles"][-1])
            print([u["name"] for u in resp["data"]["users"] if u["roles"]])
            """),
        cod(f"{P}-m1-l2-e3", t("""
            Напиши функцию `get_name(body)`, которая достаёт имя пользователя из ответа API.

            - Получает: `body` — **строку** с JSON (так приходит тело ответа), например:
              `'{"user": {"name": "Аня", "id": 7}}'`
            - Возвращает: значение поля `name` внутри объекта `user`.

            Пример:
            ```
            get_name('{"user": {"name": "Аня", "id": 7}}')   # → "Аня"
            ```
            Сначала превращаем строку в словарь: `json.loads(body)`, потом берём вложенное поле.
            """),
            """
            import json

            def get_name(body):
                pass
            """,
            """
            def test_name():
                assert get_name('{"user": {"name": "Аня", "id": 7}}') == "Аня", "Нужно распарсить JSON и достать user.name"
            """,
            """
            import json

            def get_name(body):
                return json.loads(body)["user"]["name"]
            """),
        cod(f"{P}-m1-l2-e4", t("""
            Напиши функцию `missing_fields(data, required)`, которая ищет отсутствующие обязательные поля в ответе.

            - Получает: `data` — словарь (ответ API); `required` — список имён обязательных полей.
            - Возвращает: список тех полей из `required`, которых **нет** среди ключей `data`, в том же порядке, что в `required`.

            Примеры:
            ```
            missing_fields({"id": 1, "name": "A"}, ["id", "name", "email", "age"])   # → ["email", "age"]
            missing_fields({"id": 1}, ["id"])                                        # → []
            ```
            """),
            """
            def missing_fields(data, required):
                pass
            """,
            """
            def test_missing():
                assert missing_fields({"id": 1, "name": "A"}, ["id", "name", "email", "age"]) == ["email", "age"], "Не хватает email и age"

            def test_all_present():
                assert missing_fields({"id": 1}, ["id"]) == [], "Все поля есть → []"
            """,
            """
            def missing_fields(data, required):
                return [f for f in required if f not in data]
            """),
        cod(f"{P}-m1-l2-e5", t("""
            Напиши функцию `validate_user(data)` — валидатор ответа API с пользователем.

            - Получает: `data` — словарь (ответ API).
            - Возвращает: **список ошибок** (строк). Если всё правильно — пустой список.

            Проверки и тексты ошибок (проверяй **в этом порядке**, каждая даёт не больше одной ошибки):
            1. `id` должен быть целым числом (`int`). Иначе ошибка `"id: must be int"`.
            2. `email` должен быть строкой, содержащей `@`. Иначе `"email: invalid"`.
            3. `age` должен быть целым числом **и** не меньше 0. Иначе `"age: must be >= 0"`.

            Если поля нет совсем — это тоже ошибка по соответствующему правилу.

            Примеры:
            ```
            validate_user({"id": 1, "email": "a@b.ru", "age": 30})
            # → []

            validate_user({"id": "1", "email": "abc", "age": -3})
            # → ["id: must be int", "email: invalid", "age: must be >= 0"]

            validate_user({})
            # → ["id: must be int", "email: invalid", "age: must be >= 0"]
            ```
            `data.get("id")` не упадёт на отсутствующем поле, а вернёт `None`. Тип проверяется через `isinstance(x, int)`.
            """),
            """
            def validate_user(data):
                errors = []
                return errors
            """,
            """
            def test_valid():
                assert validate_user({"id": 1, "email": "a@b.ru", "age": 30}) == [], "Валидный пользователь — без ошибок"

            def test_all_bad():
                assert validate_user({"id": "1", "email": "abc", "age": -3}) == ["id: must be int", "email: invalid", "age: must be >= 0"], \\
                    f"Получено {validate_user({'id': '1', 'email': 'abc', 'age': -3})}"

            def test_missing():
                assert validate_user({}) == ["id: must be int", "email: invalid", "age: must be >= 0"], "Пустой объект — три ошибки"
            """,
            """
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
            """,
            hint="`data.get(\"id\")` не упадёт, если поля нет, а вернёт None. Проверка типа — `isinstance(x, int)`.", xp=25),
        cod(f"{P}-m1-l2-e6", t("""
            Напиши функцию `find_user(users, user_id)`, которая ищет пользователя в списке из ответа API.

            - Получает: `users` — список словарей, у каждого есть поле `id`; `user_id` — искомый id.
            - Возвращает: словарь пользователя с таким `id`, а если его нет — `None`.

            Примеры:
            ```
            users = [{"id": 1, "name": "A"}, {"id": 5, "name": "B"}]
            find_user(users, 5)    # → {"id": 5, "name": "B"}
            find_user(users, 42)   # → None
            ```
            Можно циклом, а можно одной строкой: `next((... for ... if ...), None)`.
            """),
            """
            def find_user(users, user_id):
                pass
            """,
            """
            def test_found():
                users = [{"id": 1, "name": "A"}, {"id": 5, "name": "B"}]
                assert find_user(users, 5) == {"id": 5, "name": "B"}, "Пользователь с id=5 — B"

            def test_not_found():
                assert find_user([{"id": 1}], 42) is None, "Нет такого id → None"
            """,
            """
            def find_user(users, user_id):
                return next((u for u in users if u["id"] == user_id), None)
            """),
    ),
)

m2 = module(f"{P}-m2", "Пишем автотесты API", "🤖", "Структура теста, негативные сценарии и моки",
    lesson(f"{P}-m2-l1", "Первые автотесты", """
        # Как выглядит API-тест в реальном проекте

        Обычно это `pytest` + библиотека `requests`:

        ```
        import requests

        BASE = "https://api.example.com"

        def test_get_user():
            # Arrange — подготовка
            user_id = 1
            # Act — действие
            resp = requests.get(f"{BASE}/users/{user_id}")
            # Assert — проверка
            assert resp.status_code == 200
            assert resp.json()["id"] == user_id
        ```

        Схема **AAA (Arrange-Act-Assert)** делает тесты читаемыми.

        # В этом уроке

        Сети в песочнице нет, поэтому тест получает объект `client` — он ведёт себя как `requests`:

        - `client.get("/users/1")` → ответ
        - `client.post("/users", json={...})` → ответ
        - у ответа есть `resp.status_code` и `resp.json()`

        API содержит пользователя `{"id": 1, "name": "Аня", "email": "anna@mail.ru"}`.

        ⚠️ Проверяющий запустит **твой тест** на исправном API (тест должен пройти) и на сломанных версиях (тест должен упасть). Хороший тест ловит баги!
        """,
        cod(f"{P}-m2-l1-e1", t("""
            Допиши автотест `test_get_user(client)` — проверку получения пользователя.

            Запрос уже написан: `resp = client.get("/users/1")`. Добавь две проверки через `assert`:
            1. код ответа (`resp.status_code`) равен `200`;
            2. в теле ответа (`resp.json()` — это словарь) поле `id` равно `1`.

            Как будет проверяться: твой тест запустят на исправном API — он должен **пройти**; и на сломанных версиях (сервер отдаёт 500 или возвращает чужой `id`) — он должен **упасть**. Тест без проверок ничего не ловит и не засчитывается.
            """),
            """
            def test_get_user(client):
                # Act
                resp = client.get("/users/1")
                # Assert — допиши проверки
            """,
            with_fake("""
            def test_zz_passes_on_good_api():
                test_get_user(Client())

            def test_zz_catches_500():
                must_fail(test_get_user, Client("500"), "сервер вернул 500")

            def test_zz_catches_wrong_id():
                must_fail(test_get_user, Client("wrong_id"), "в ответе id=999 вместо 1")
            """),
            """
            def test_get_user(client):
                resp = client.get("/users/1")
                assert resp.status_code == 200
                assert resp.json()["id"] == 1
            """,
            hint="Две строки: `assert resp.status_code == 200` и `assert resp.json()[\"id\"] == 1`."),
        cod(f"{P}-m2-l1-e2", t("""
            Напиши автотест `test_user_has_email(client)`, который проверяет наличие почты у пользователя.

            Шаги теста:
            1. Запроси пользователя: `client.get("/users/1")`.
            2. Достань тело ответа: `.json()` — получится словарь.
            3. Проверь `assert`-ами, что в словаре **есть ключ** `"email"` и что его значение содержит символ `@`.

            Твой тест должен проходить на исправном API и падать на сломанном, где поле `email` пропало из ответа.
            """),
            "",
            with_fake("""
            def test_zz_passes_on_good_api():
                test_user_has_email(Client())

            def test_zz_catches_missing_email():
                must_fail(test_user_has_email, Client("no_email"), "в ответе нет поля email")
            """),
            """
            def test_user_has_email(client):
                data = client.get("/users/1").json()
                assert "email" in data
                assert "@" in data["email"]
            """,
            hint="`assert \"email\" in data` проверяет наличие ключа."),
        cod(f"{P}-m2-l1-e3", t("""
            Напиши **негативный** автотест `test_unknown_user_404(client)`.

            Негативный тест проверяет, что система правильно реагирует на неправильный запрос. Здесь — на запрос несуществующего пользователя.

            Шаги:
            1. Запроси пользователя, которого нет: `client.get("/users/999")`.
            2. Проверь, что код ответа — `404` (Not Found).

            Тест должен падать, если API вместо 404 возвращает `200` (выдаёт несуществующего пользователя) или `500` (сервер падает).
            """),
            "",
            with_fake("""
            def test_zz_passes_on_good_api():
                test_unknown_user_404(Client())

            def test_zz_catches_200():
                must_fail(test_unknown_user_404, Client("no404"), "API вернул 200 для несуществующего пользователя")

            def test_zz_catches_500():
                must_fail(test_unknown_user_404, Client("500"), "API вернул 500")
            """),
            """
            def test_unknown_user_404(client):
                resp = client.get("/users/999")
                assert resp.status_code == 404
            """),
        cod(f"{P}-m2-l1-e4", t("""
            Напиши автотест `test_create_user(client)` — проверку создания пользователя.

            Шаги:
            1. Создай пользователя: `resp = client.post("/users", json={"name": "Боря"})`.
            2. Проверь, что код ответа — `201` (Created). Именно 201, а не 200!
            3. Достань тело `resp.json()` и проверь, что в нём есть поле `"id"`,
            4. и что поле `"name"` равно `"Боря"`.

            Тест должен падать на сломанных версиях API: где POST возвращает 200 и где имя теряется при сохранении.
            """),
            "",
            with_fake("""
            def test_zz_passes_on_good_api():
                test_create_user(Client())

            def test_zz_catches_wrong_status():
                must_fail(test_create_user, Client("status200"), "POST вернул 200 вместо 201")

            def test_zz_catches_lost_name():
                must_fail(test_create_user, Client("lost_name"), "API потерял имя")
            """),
            """
            def test_create_user(client):
                resp = client.post("/users", json={"name": "Боря"})
                assert resp.status_code == 201
                data = resp.json()
                assert "id" in data
                assert data["name"] == "Боря"
            """,
            xp=20),
        cod(f"{P}-m2-l1-e5", t("""
            Напиши сквозной автотест `test_created_user_can_be_fetched(client)`: созданного пользователя действительно можно получить.

            Шаги:
            1. Создай пользователя через `client.post("/users", json={"name": "Вика"})`.
            2. Возьми из ответа (`.json()`) его `id`.
            3. Запроси этого пользователя: `client.get(f"/users/{id}")`.
            4. Проверь, что у полученного пользователя имя — `"Вика"`.

            Такой тест ловит баги, которые не видны по одному запросу: например, API ответил «создано», но на самом деле не сохранил имя.
            """),
            "",
            with_fake("""
            def test_zz_passes_on_good_api():
                test_created_user_can_be_fetched(Client())

            def test_zz_catches_lost_name():
                must_fail(test_created_user_can_be_fetched, Client("lost_name"), "имя не сохранилось")
            """),
            """
            def test_created_user_can_be_fetched(client):
                created = client.post("/users", json={"name": "Вика"}).json()
                fetched = client.get(f"/users/{created['id']}").json()
                assert fetched["name"] == "Вика"
            """,
            hint="Сохрани ответ POST в переменную, id возьми из `.json()[\"id\"]`, подставь в URL f-строкой.", xp=20),
    ),
    lesson(f"{P}-m2-l2", "Моки и параметризация", """
        # Параметризация

        Один тест — много наборов данных. В pytest:

        ```
        import pytest

        @pytest.mark.parametrize("code, expected", [(200, True), (404, False), (500, False)])
        def test_is_ok(code, expected):
            assert is_ok(code) == expected
        ```

        # Моки

        **Мок** — объект-заглушка вместо настоящей зависимости (сети, БД, почты).
        Он возвращает то, что скажешь, и запоминает, как его вызывали:

        ```
        from unittest.mock import Mock

        mailer = Mock()
        mailer.send("a@b.ru", "Привет")
        mailer.send.assert_called_once_with("a@b.ru", "Привет")   # проверка вызова

        api = Mock()
        api.get.return_value = {"id": 1}      # что вернёт вызов
        api.get("/users/1")                    # {'id': 1}

        api.get.side_effect = [TimeoutError(), {"id": 1}]   # 1-й вызов — ошибка, 2-й — ответ
        ```

        Чтобы код можно было тестировать с моками, зависимости **передают параметром** (dependency injection), а не создают внутри.
        """,
        out(f"{P}-m2-l2-e1", "Что выведет программа?", """
            from unittest.mock import Mock

            api = Mock()
            api.get.return_value = {"status": "ok"}
            print(api.get("/health"))
            print(api.get.call_count)
            api.get("/users")
            print(api.get.call_count)
            """),
        out(f"{P}-m2-l2-e2", "Что выведет программа? `side_effect` со списком.", """
            from unittest.mock import Mock

            m = Mock(side_effect=[1, 2, ValueError("стоп")])
            print(m(), m())
            try:
                m()
            except ValueError as e:
                print("ошибка:", e)
            """),
        cod(f"{P}-m2-l2-e3", t("""
            Напиши функцию `run_cases(func, cases)` — мини-версию параметризации тестов.

            - Получает:
              - `func` — проверяемую функцию одного аргумента;
              - `cases` — список пар `(аргумент, ожидаемый_результат)`.
            - Для каждой пары вызывает `func(аргумент)` и сравнивает с ожидаемым.
            - Возвращает: список описаний **упавших** случаев в формате
              `"func(<аргумент>) = <что получили>, expected <что ожидали>"`.
              Если всё совпало — пустой список.

            Примеры:
            ```
            run_cases(abs, [(-1, 1), (2, 2)])   # → []

            double = lambda x: x * 2
            run_cases(double, [(1, 2), (3, 7), (0, 0)])
            # → ["func(3) = 6, expected 7"]
            ```
            """),
            """
            def run_cases(func, cases):
                failures = []
                return failures
            """,
            """
            def test_all_ok():
                assert run_cases(abs, [(-1, 1), (2, 2)]) == [], "Всё верно → пустой список"

            def test_failures():
                double = lambda x: x * 2
                got = run_cases(double, [(1, 2), (3, 7), (0, 0)])
                assert got == ["func(3) = 6, expected 7"], f"Получено {got}"
            """,
            """
            def run_cases(func, cases):
                failures = []
                for arg, expected in cases:
                    got = func(arg)
                    if got != expected:
                        failures.append(f"func({arg}) = {got}, expected {expected}")
                return failures
            """),
        cod(f"{P}-m2-l2-e4", t("""
            Напиши функцию `register(email, mailer)` — регистрацию пользователя с приветственным письмом.

            - Получает: `email` — адрес; `mailer` — объект для отправки почты с методом `send(адрес, текст)`.
            - Логика:
              - если в `email` нет символа `@` — бросить `ValueError` и **ничего не отправлять**;
              - иначе вызвать `mailer.send(email, "Добро пожаловать!")` и вернуть `True`.

            Пример:
            ```
            register("a@b.ru", mailer)   # → True, отправлено письмо "Добро пожаловать!" на a@b.ru
            register("плохой", mailer)   # ValueError, писем нет
            ```
            Проверка подставит вместо настоящей почты **мок** (`unittest.mock.Mock`) и посмотрит, с какими аргументами был вызван `send`. Поэтому текст письма должен совпадать точно.
            """),
            """
            def register(email, mailer):
                pass
            """,
            """
            from unittest.mock import Mock

            def test_sends_email():
                mailer = Mock()
                assert register("a@b.ru", mailer) is True, "register должна вернуть True"
                mailer.send.assert_called_once_with("a@b.ru", "Добро пожаловать!")

            def test_invalid_email():
                mailer = Mock()
                try:
                    register("плохой", mailer)
                except ValueError:
                    pass
                else:
                    assert False, "Для email без @ нужен ValueError"
                assert mailer.send.call_count == 0, "Письмо при ошибке отправляться не должно"
            """,
            """
            def register(email, mailer):
                if "@" not in email:
                    raise ValueError("invalid email")
                mailer.send(email, "Добро пожаловать!")
                return True
            """),
        cod(f"{P}-m2-l2-e5", t("""
            Напиши функцию `get_with_retry(client, path, attempts=3)` — запрос с повторами при сбоях сервера.

            - Получает: `client` — объект с методом `get(path)`; `path` — путь; `attempts` — максимальное число попыток.
            - Логика:
              - делает запрос `client.get(path)`;
              - если код ответа **меньше 500** — сразу возвращает этот ответ (успех или ошибка клиента — повторять бессмысленно);
              - если код `5xx` — пробует снова;
              - всего не больше `attempts` запросов. Если все вернули 5xx — возвращает последний ответ.

            Примеры (коды по очереди, которые вернёт сервер):
            ```
            503, 502, 200      → 3 запроса, вернёт ответ с 200
            404                → 1 запрос,  вернёт ответ с 404
            500, 500 (attempts=2) → 2 запроса, вернёт ответ с 500
            ```
            """),
            """
            def get_with_retry(client, path, attempts=3):
                pass
            """,
            """
            from unittest.mock import Mock

            def r(code):
                resp = Mock()
                resp.status_code = code
                return resp

            def test_retry_then_ok():
                client = Mock()
                client.get.side_effect = [r(503), r(502), r(200)]
                assert get_with_retry(client, "/x").status_code == 200, "После двух 5xx третья попытка вернула 200"
                assert client.get.call_count == 3, "Должно быть 3 запроса"

            def test_no_retry_on_4xx():
                client = Mock()
                client.get.side_effect = [r(404)]
                assert get_with_retry(client, "/x").status_code == 404, "На 4xx повторять не нужно"
                assert client.get.call_count == 1, "Только 1 запрос"

            def test_gives_up():
                client = Mock()
                client.get.side_effect = [r(500)] * 5
                assert get_with_retry(client, "/x", attempts=2).status_code == 500, "Сдаёмся после attempts попыток"
                assert client.get.call_count == 2, "Ровно attempts запросов"
            """,
            """
            def get_with_retry(client, path, attempts=3):
                for _ in range(attempts):
                    resp = client.get(path)
                    if resp.status_code < 500:
                        return resp
                return resp
            """,
            hint="Цикл `for _ in range(attempts)`: сделал запрос — если статус < 500, сразу `return`.", xp=25),
    ),
)

TOPIC = topic("api-testing", "Тестирование API", "🌐", "#00a88e",
              "HTTP, статус-коды, JSON, автотесты, негативные сценарии и моки", m1, m2, group="Тестирование и DevOps")
