"""Тема «Тестирование API», модуль 1 «HTTP для тестировщика» — задания. Теория — в _api_t1.py.

Слаги api-m1-l1, api-m1-l2 унаследованы от старой темы — так сохраняется прогресс."""
from ._lib import cmd, cod, lesson, module, out, t

P = "api"

m1 = module(f"{P}-m1", "HTTP для тестировщика", "🌐", "Запрос и ответ, методы и статусы, заголовки, REST, JSON и проверка ответа",

lesson(f"{P}-m1-l1", "Запрос и ответ",
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
    cmd(f"{P}-m1-l1-e7", "Какой метод и путь в этом запросе? Введи через пробел.",
        ["POST /v1/orders"],
        context="""
        POST /v1/orders?debug=1 HTTP/1.1
        Host: api.shop.ru
        Content-Type: application/json

        {"item": 42, "count": 2}
        """),
    cod(f"{P}-m1-l1-e8", t("""
        Напиши функцию `parse_request_line(line)` — разобрать первую строку HTTP-запроса вида `"GET /users?page=2 HTTP/1.1"` и вернуть словарь `{"method": ..., "path": ..., "query": {...}}`, где `query` — параметры строки запроса (значения — строки). Используй `urllib.parse`.
        """),
        """
        from urllib.parse import urlsplit, parse_qsl


        def parse_request_line(line):
            pass
        """,
        """
        def test_values():
            assert parse_request_line("GET /users?page=2&sort=name HTTP/1.1") == {"method": "GET", "path": "/users", "query": {"page": "2", "sort": "name"}}
            assert parse_request_line("DELETE /users/7 HTTP/1.1") == {"method": "DELETE", "path": "/users/7", "query": {}}
        """,
        """
        from urllib.parse import urlsplit, parse_qsl


        def parse_request_line(line):
            method, target, _version = line.split()
            parts = urlsplit(target)
            return {"method": method, "path": parts.path, "query": dict(parse_qsl(parts.query))}
        """, xp=20),
),

lesson(f"{P}-methods", "Методы, статусы и заголовки",
    out(f"{P}-methods-e1", "Что выведет программа? Классы статус-кодов.", """
        from http import HTTPStatus

        for code in [200, 201, 204, 301, 400, 401, 403, 404, 409, 422, 500, 503]:
            print(code, HTTPStatus(code).phrase)
        """, hint="HTTPStatus — стандартный справочник статусов."),
    out(f"{P}-methods-e2", "Что выведет программа? Заголовки нечувствительны к регистру.", """
        import requests

        h = requests.structures.CaseInsensitiveDict({"Content-Type": "application/json"})
        print(h["content-type"], "CONTENT-TYPE" in h)
        """),
    cmd(f"{P}-methods-e3", "Какой статус должен вернуть сервер на успешное **создание** ресурса (POST)? Введи число.",
        ["201"]),
    cmd(f"{P}-methods-e4", "Какой статус означает «нужно авторизоваться» (нет или неверный токен)? Введи число.",
        ["401"]),
    cmd(f"{P}-methods-e5", "Какой статус означает «авторизован, но прав на это действие нет»? Введи число.",
        ["403"]),
    cmd(f"{P}-methods-e6", "Какой заголовок запроса передаёт токен авторизации? Введи его имя.",
        ["Authorization"]),
    cod(f"{P}-methods-e7", t("""
        Напиши функцию `check_headers(headers)` — проверить заголовки ответа API и вернуть список проблем (пустой, если всё хорошо). Имена заголовков сравнивай **без учёта регистра**.

        - нет `Content-Type` или он не начинается с `application/json` → `"не JSON"`;
        - есть `Server` со словом `debug` (в любом регистре) → `"отладочный сервер"`;
        - нет `X-Request-Id` → `"нет X-Request-Id"`.
        """),
        """
        def check_headers(headers):
            pass
        """,
        """
        def test_values():
            assert check_headers({"content-type": "application/json; charset=utf-8", "x-request-id": "abc"}) == []
            assert check_headers({"Content-Type": "text/html", "Server": "Debug-Server", "X-Request-Id": "1"}) == ["не JSON", "отладочный сервер"]
            assert check_headers({}) == ["не JSON", "нет X-Request-Id"]
        """,
        """
        def check_headers(headers):
            h = {k.lower(): v for k, v in headers.items()}
            problems = []
            if not h.get("content-type", "").startswith("application/json"):
                problems.append("не JSON")
            if "debug" in h.get("server", "").lower():
                problems.append("отладочный сервер")
            if "x-request-id" not in h:
                problems.append("нет X-Request-Id")
            return problems
        """),
    cod(f"{P}-methods-e8", t("""
        Напиши функцию `expected_status(method, action_ok)` — какой код ожидать от REST API:

        - `"POST"` — `201`, `"DELETE"` — `204`, остальные (`GET`, `PUT`, `PATCH`) — `200`, если `action_ok`;
        - если `action_ok` ложно (ресурса нет) — `404` для любого метода, кроме `POST` (для него — `422`: невалидные данные).
        """),
        """
        def expected_status(method, action_ok):
            pass
        """,
        """
        def test_values():
            assert [expected_status(m, True) for m in ["GET", "POST", "PUT", "PATCH", "DELETE"]] == [200, 201, 200, 200, 204]
            assert [expected_status(m, False) for m in ["GET", "POST", "DELETE"]] == [404, 422, 404]
        """,
        """
        def expected_status(method, action_ok):
            if not action_ok:
                return 422 if method == "POST" else 404
            return {"POST": 201, "DELETE": 204}.get(method, 200)
        """, xp=20),
),

lesson(f"{P}-m1-l2", "JSON и проверка ответа",
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
    out(f"{P}-m1-l2-e7", "Что выведет программа? Безопасный доступ к вложенным полям.", """
        body = {"data": {"user": {"name": "Аня", "address": None}}}
        print(body.get("data", {}).get("user", {}).get("name"))
        print((body["data"]["user"].get("address") or {}).get("city", "нет"))
        print(body.get("meta", {}).get("total", 0))
        """),
    cod(f"{P}-m1-l2-e8", t("""
        Напиши функцию `get_path(data, path, default=None)` — достать вложенное значение по пути через точку, где числа — индексы списков: `get_path(body, "data.users.0.name")`. Если чего-то нет по пути — вернуть `default`.
        """),
        """
        def get_path(data, path, default=None):
            pass
        """,
        """
        BODY = {"data": {"users": [{"name": "Аня", "roles": ["qa"]}], "total": 1}}

        def test_values():
            assert get_path(BODY, "data.users.0.name") == "Аня" and get_path(BODY, "data.users.0.roles.0") == "qa"
            assert get_path(BODY, "data.total") == 1 and get_path(BODY, "data.users.5.name", "нет") == "нет"
            assert get_path(BODY, "meta.page") is None and get_path(BODY, "data.users.x") is None
        """,
        """
        def get_path(data, path, default=None):
            current = data
            for part in path.split("."):
                if isinstance(current, list) and part.isdigit() and int(part) < len(current):
                    current = current[int(part)]
                elif isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return default
            return current
        """, xp=20),
),

lesson(f"{P}-rest", "REST: ресурсы, CRUD, пагинация",
    cmd(f"{P}-rest-e1", "Каким методом и путём по REST получить пользователя с id 7? Введи `МЕТОД путь`.",
        ["GET /users/7"]),
    cmd(f"{P}-rest-e2", "Каким методом и путём **удалить** заказ 15? Введи `МЕТОД путь`.",
        ["DELETE /orders/15"]),
    cmd(f"{P}-rest-e3", "Каким методом **частично** обновить пользователя (изменить только email)?",
        ["PATCH"]),
    cmd(f"{P}-rest-e4", "Сколько всего страниц при таком ответе? Введи число.",
        ["5"],
        context="""
        GET /users?page=1&per_page=20
        {"items": [...], "page": 1, "per_page": 20, "total": 93}
        """, hint="Округление вверх."),
    cod(f"{P}-rest-e5", t("""
        Напиши функцию `crud_plan(resource)` — список запросов для CRUD-теста ресурса: создать, прочитать, обновить целиком, частично, удалить, прочитать удалённый. Формат — кортежи `(метод, путь, ожидаемый_код)`; id созданного ресурса обозначь `{id}`.

        ```
        crud_plan("users")[0]   # → ("POST", "/users", 201)
        ```
        """),
        """
        def crud_plan(resource):
            pass
        """,
        """
        def test_values():
            assert crud_plan("users") == [
                ("POST", "/users", 201), ("GET", "/users/{id}", 200), ("PUT", "/users/{id}", 200),
                ("PATCH", "/users/{id}", 200), ("DELETE", "/users/{id}", 204), ("GET", "/users/{id}", 404),
            ], crud_plan("users")
        """,
        """
        def crud_plan(resource):
            base = f"/{resource}"
            item = f"{base}/{{id}}"
            return [
                ("POST", base, 201), ("GET", item, 200), ("PUT", item, 200),
                ("PATCH", item, 200), ("DELETE", item, 204), ("GET", item, 404),
            ]
        """),
    cod(f"{P}-rest-e6", t("""
        Напиши функцию `pages_count(total, per_page)` — сколько страниц нужно, и `page_items(items, page, per_page)` — элементы страницы `page` (с 1). Страница вне диапазона — пустой список.
        """),
        """
        def pages_count(total, per_page):
            pass


        def page_items(items, page, per_page):
            pass
        """,
        """
        def test_values():
            assert [pages_count(t, 20) for t in (0, 1, 20, 21, 93)] == [0, 1, 1, 2, 5]
            items = list(range(1, 8))
            assert page_items(items, 1, 3) == [1, 2, 3] and page_items(items, 3, 3) == [7] and page_items(items, 4, 3) == [] and page_items(items, 0, 3) == []
        """,
        """
        def pages_count(total, per_page):
            return (total + per_page - 1) // per_page


        def page_items(items, page, per_page):
            if page < 1:
                return []
            start = (page - 1) * per_page
            return items[start:start + per_page]
        """),
    cod(f"{P}-rest-e7", t("""
        Напиши функцию `collect_all(fetch_page)` — собрать все элементы из пагинированного API. `fetch_page(page)` возвращает словарь `{"items": [...], "page": N, "pages": M}`. Начни с первой страницы и остановись, когда `page >= pages`.
        """),
        """
        def collect_all(fetch_page):
            pass
        """,
        """
        def test_values():
            data = {1: [1, 2], 2: [3, 4], 3: [5]}
            calls = []
            def fetch(p):
                calls.append(p)
                return {"items": data[p], "page": p, "pages": 3}
            assert collect_all(fetch) == [1, 2, 3, 4, 5] and calls == [1, 2, 3], calls
            assert collect_all(lambda p: {"items": [], "page": 1, "pages": 1}) == [], "Пустой ответ"
        """,
        """
        def collect_all(fetch_page):
            items = []
            page = 1
            while True:
                resp = fetch_page(page)
                items.extend(resp["items"])
                if resp["page"] >= resp["pages"]:
                    return items
                page += 1
        """),
    cmd(f"{P}-rest-e8", "Какой запрос вернёт активных пользователей, отсортированных по имени, вторую страницу? Собери путь с параметрами `status`, `sort`, `page` в этом порядке.",
        ["GET /users?status=active&sort=name&page=2", "/users?status=active&sort=name&page=2"], xp=15),
),
)
