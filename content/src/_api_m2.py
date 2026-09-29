"""Тема «Тестирование API», модуль 2 «Клиенты и автотесты» — задания. Теория — в _api_t2.py.

Сети в песочнице нет: HTTP-ответы подменяются библиотекой responses, а в старых заданиях
«напиши тест» — фейковым клиентом (FAKE). Слаги api-m2-l1, api-m2-l2 унаследованы от старой темы."""
from textwrap import dedent

from ._lib import cmd, cod, lesson, module, out, pyt, t

P = "api"

# Общий кусок проверок для старых заданий «напиши тест»: фейковый клиент.
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


m2 = module(f"{P}-m2", "Клиенты и автотесты", "🤖", "Библиотека requests, первые автотесты, свой API-клиент, моки и подмена ответов",

lesson(f"{P}-requests", "requests: запросы из Python",
    out(f"{P}-requests-e1", "Что выведет программа? Запрос к подменённому серверу.", """
        import requests
        import responses

        with responses.RequestsMock() as mock:
            mock.get("https://api.test/users/1", json={"id": 1, "name": "Аня"}, status=200)
            r = requests.get("https://api.test/users/1")
            print(r.status_code, r.ok)
            print(r.json()["name"], r.headers["Content-Type"])
        """, hint="responses перехватывает запросы requests и отдаёт заданный ответ — без сети."),
    out(f"{P}-requests-e2", "Что выведет программа? Параметры, тело и заголовки запроса.", """
        import json
        import requests
        import responses

        with responses.RequestsMock() as mock:
            mock.post("https://api.test/users", json={"id": 2}, status=201)
            r = requests.post("https://api.test/users", params={"notify": "false"},
                              json={"name": "Боря"}, headers={"Authorization": "Bearer t1"})
            sent = mock.calls[0].request
            print(r.status_code, sent.url)
            print(json.loads(sent.body), sent.headers["Authorization"])
        """),
    out(f"{P}-requests-e3", "Что выведет программа? raise_for_status.", """
        import requests
        import responses

        with responses.RequestsMock() as mock:
            mock.get("https://api.test/secret", status=403)
            r = requests.get("https://api.test/secret")
            try:
                r.raise_for_status()
            except requests.HTTPError as e:
                print("ошибка:", e.response.status_code)
        """),
    cod(f"{P}-requests-e4", t("""
        Напиши функцию `get_user(base_url, user_id)` — GET-запрос на `{base_url}/users/{user_id}` через `requests` с таймаутом 5 секунд. Вернуть словарь из JSON. Если статус не 200 — выбросить `LookupError(f"user {user_id}: {код}")`.
        """),
        """
        import requests


        def get_user(base_url, user_id):
            pass
        """,
        """
        import responses

        @responses.activate
        def test_values():
            responses.get("https://api.test/users/1", json={"id": 1, "name": "Аня"})
            responses.get("https://api.test/users/9", status=404, json={"error": "not found"})
            assert get_user("https://api.test", 1) == {"id": 1, "name": "Аня"}
            try:
                get_user("https://api.test", 9)
            except LookupError as e:
                assert str(e) == "user 9: 404", str(e)
                return
            assert False, "Нужен LookupError"
        """,
        """
        import requests


        def get_user(base_url, user_id):
            response = requests.get(f"{base_url}/users/{user_id}", timeout=5)
            if response.status_code != 200:
                raise LookupError(f"user {user_id}: {response.status_code}")
            return response.json()
        """),
    cod(f"{P}-requests-e5", t("""
        Напиши функцию `create_user(base_url, name, token)` — POST на `{base_url}/users` с JSON `{"name": name}` и заголовком `Authorization: Bearer <token>`. Вернуть кортеж `(статус, тело)`.
        """),
        """
        import requests


        def create_user(base_url, name, token):
            pass
        """,
        """
        import json
        import responses

        @responses.activate
        def test_values():
            responses.post("https://api.test/users", json={"id": 5, "name": "Вика"}, status=201)
            assert create_user("https://api.test", "Вика", "t-1") == (201, {"id": 5, "name": "Вика"})
            req = responses.calls[0].request
            assert json.loads(req.body) == {"name": "Вика"} and req.headers["Authorization"] == "Bearer t-1", req.headers
        """,
        """
        import requests


        def create_user(base_url, name, token):
            response = requests.post(
                f"{base_url}/users",
                json={"name": name},
                headers={"Authorization": f"Bearer {token}"},
                timeout=5,
            )
            return response.status_code, response.json()
        """),
    cod(f"{P}-requests-e6", t("""
        Напиши функцию `search(base_url, query, page=1)` — GET на `{base_url}/search` с параметрами строки запроса `q` и `page` (через `params=`, а не склейкой строки!). Вернуть список `items` из ответа.
        """),
        """
        import requests


        def search(base_url, query, page=1):
            pass
        """,
        """
        import responses
        from responses import matchers

        @responses.activate
        def test_values():
            responses.get("https://api.test/search", json={"items": ["a", "b"]},
                          match=[matchers.query_param_matcher({"q": "чай с мятой", "page": "2"})])
            assert search("https://api.test", "чай с мятой", page=2) == ["a", "b"]
        """,
        """
        import requests


        def search(base_url, query, page=1):
            response = requests.get(f"{base_url}/search", params={"q": query, "page": page}, timeout=5)
            return response.json()["items"]
        """, hint="params= сам закодирует пробелы и кириллицу."),
    cod(f"{P}-requests-e7", t("""
        Напиши функцию `health(url)` — вернуть `"up"`, если GET вернул 200, `"down"` — если другой статус **или** сервер недоступен (исключение `requests.ConnectionError` или `requests.Timeout`). Таймаут — 2 секунды.
        """),
        """
        import requests


        def health(url):
            pass
        """,
        """
        import requests
        import responses

        @responses.activate
        def test_values():
            responses.get("https://a.test/health", status=200)
            responses.get("https://b.test/health", status=503)
            responses.get("https://c.test/health", body=requests.ConnectionError("нет соединения"))
            responses.get("https://d.test/health", body=requests.Timeout("долго"))
            assert [health(f"https://{h}.test/health") for h in "abcd"] == ["up", "down", "down", "down"]
        """,
        """
        import requests


        def health(url):
            try:
                response = requests.get(url, timeout=2)
            except (requests.ConnectionError, requests.Timeout):
                return "down"
            return "up" if response.status_code == 200 else "down"
        """),
    cmd(f"{P}-requests-e8", "Какой параметр `requests.get(...)` обязательно указывать в тестах и скриптах, чтобы запрос не висел вечно? Введи имя параметра.",
        ["timeout"], xp=15),
),

lesson(f"{P}-m2-l1", "Первые автотесты",
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
    pyt(f"{P}-m2-l1-e6", t("""
        Теперь настоящий pytest с подменой сервера. Напиши тест `test_get_user`, который подменяет ответ `GET https://api.test/users/1` через `@responses.activate` + `responses.get(...)` (тело `{"id": 1, "name": "Аня"}`), вызывает функцию `get_user(1)` и проверяет результат.
        """),
        """
        import pytest
        import requests
        import responses


        def get_user(user_id):
            r = requests.get(f"https://api.test/users/{user_id}", timeout=5)
            r.raise_for_status()
            return r.json()
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_get_user") == "passed", res

        def test_catches_bug():
            import requests as rq
            def wrong(user_id):
                r = rq.get(f"https://api.test/users/{user_id}", timeout=5)
                return {**r.json(), "name": "Боря"}
            code, res = run_pytest(patch={"get_user": wrong})
            assert code == 1, "Тест должен проверять тело ответа"
        """,
        """
        import pytest
        import requests
        import responses


        def get_user(user_id):
            r = requests.get(f"https://api.test/users/{user_id}", timeout=5)
            r.raise_for_status()
            return r.json()


        @responses.activate
        def test_get_user():
            responses.get("https://api.test/users/1", json={"id": 1, "name": "Аня"})
            assert get_user(1) == {"id": 1, "name": "Аня"}
        """),
    pyt(f"{P}-m2-l1-e7", t("""
        Негативный тест: напиши `test_user_not_found`, который подменяет `GET https://api.test/users/99` ответом `404` и проверяет, что `get_user(99)` выбрасывает `requests.HTTPError`.
        """),
        """
        import pytest
        import requests
        import responses


        def get_user(user_id):
            r = requests.get(f"https://api.test/users/{user_id}", timeout=5)
            r.raise_for_status()
            return r.json()
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_user_not_found") == "passed", res

        def test_catches_bug():
            import requests as rq
            def swallow(user_id):
                r = rq.get(f"https://api.test/users/{user_id}", timeout=5)
                return None if r.status_code == 404 else r.json()
            code, res = run_pytest(patch={"get_user": swallow})
            assert code == 1, "Тест должен падать, если ошибка проглочена"
        """,
        """
        import pytest
        import requests
        import responses


        def get_user(user_id):
            r = requests.get(f"https://api.test/users/{user_id}", timeout=5)
            r.raise_for_status()
            return r.json()


        @responses.activate
        def test_user_not_found():
            responses.get("https://api.test/users/99", status=404, json={"error": "not found"})
            with pytest.raises(requests.HTTPError):
                get_user(99)
        """),
    pyt(f"{P}-m2-l1-e8", t("""
        Проверь, **что отправляет** клиент. Напиши тест `test_create_sends_json`, который подменяет `POST https://api.test/users` (ответ 201), вызывает `create_user("Аня")` и проверяет через `responses.calls[0].request`, что тело запроса — JSON `{"name": "Аня"}`.
        """),
        """
        import json
        import pytest
        import requests
        import responses


        def create_user(name):
            r = requests.post("https://api.test/users", json={"name": name}, timeout=5)
            return r.status_code
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_create_sends_json") == "passed", res

        def test_catches_bug():
            import requests as rq
            def wrong(name):
                return rq.post("https://api.test/users", json={"username": name}, timeout=5).status_code
            code, res = run_pytest(patch={"create_user": wrong})
            assert code == 1, "Тест должен проверять тело запроса"
        """,
        """
        import json
        import pytest
        import requests
        import responses


        def create_user(name):
            r = requests.post("https://api.test/users", json={"name": name}, timeout=5)
            return r.status_code


        @responses.activate
        def test_create_sends_json():
            responses.post("https://api.test/users", json={"id": 1}, status=201)
            assert create_user("Аня") == 201
            assert json.loads(responses.calls[0].request.body) == {"name": "Аня"}
        """, xp=25),
),

lesson(f"{P}-client", "Свой API-клиент",
    out(f"{P}-client-e1", "Что выведет программа? Session запоминает заголовки.", """
        import requests
        import responses

        with responses.RequestsMock() as mock:
            mock.get("https://api.test/me", json={"name": "Аня"})
            mock.get("https://api.test/orders", json=[])
            s = requests.Session()
            s.headers.update({"Authorization": "Bearer t1"})
            s.get("https://api.test/me")
            s.get("https://api.test/orders")
            print([c.request.headers["Authorization"] for c in mock.calls])
        """),
    cod(f"{P}-client-e2", t("""
        Создай класс `ApiClient(base_url, token=None)`:

        - хранит `requests.Session()` в атрибуте `session`; если есть токен — добавляет заголовок `Authorization: Bearer <token>` к сессии;
        - метод `get(path, **kwargs)` и `post(path, **kwargs)` — запрос на `base_url + path` через сессию с `timeout=10` (если не передан другой), возвращают ответ.
        """),
        """
        import requests


        class ApiClient:
            pass
        """,
        """
        import responses

        @responses.activate
        def test_values():
            responses.get("https://api.test/me", json={"name": "Аня"})
            responses.post("https://api.test/orders", json={"id": 1}, status=201)
            c = ApiClient("https://api.test", token="t1")
            assert c.get("/me").json() == {"name": "Аня"} and c.post("/orders", json={"item": 1}).status_code == 201
            assert all(call.request.headers.get("Authorization") == "Bearer t1" for call in responses.calls), "Токен в каждом запросе"
            assert "Authorization" not in ApiClient("https://api.test").session.headers, "Без токена — без заголовка"
        """,
        """
        import requests


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

            def post(self, path, **kwargs):
                return self.request("POST", path, **kwargs)
        """),
    cod(f"{P}-client-e3", t("""
        Напиши класс `UsersApi(client)` — обёртку над эндпоинтами пользователей поверх клиента из прошлого задания (он уже есть в заготовке):

        - `get(user_id)` → ответ `GET /users/{id}`;
        - `create(name, role="qa")` → ответ `POST /users` с JSON `{"name", "role"}`;
        - `delete(user_id)` → ответ `DELETE /users/{id}`.
        """),
        """
        import requests


        class ApiClient:
            def __init__(self, base_url):
                self.base_url = base_url
                self.session = requests.Session()

            def request(self, method, path, **kwargs):
                kwargs.setdefault("timeout", 10)
                return self.session.request(method, self.base_url + path, **kwargs)


        class UsersApi:
            pass
        """,
        """
        import json
        import responses

        @responses.activate
        def test_values():
            responses.get("https://api.test/users/1", json={"id": 1})
            responses.post("https://api.test/users", json={"id": 2}, status=201)
            responses.delete("https://api.test/users/2", status=204)
            users = UsersApi(ApiClient("https://api.test"))
            assert users.get(1).json() == {"id": 1} and users.create("Боря").status_code == 201 and users.delete(2).status_code == 204
            assert json.loads(responses.calls[1].request.body) == {"name": "Боря", "role": "qa"}, responses.calls[1].request.body
        """,
        """
        import requests


        class ApiClient:
            def __init__(self, base_url):
                self.base_url = base_url
                self.session = requests.Session()

            def request(self, method, path, **kwargs):
                kwargs.setdefault("timeout", 10)
                return self.session.request(method, self.base_url + path, **kwargs)


        class UsersApi:
            def __init__(self, client):
                self.client = client

            def get(self, user_id):
                return self.client.request("GET", f"/users/{user_id}")

            def create(self, name, role="qa"):
                return self.client.request("POST", "/users", json={"name": name, "role": role})

            def delete(self, user_id):
                return self.client.request("DELETE", f"/users/{user_id}")
        """),
    cod(f"{P}-client-e4", t("""
        Напиши функцию `login(base_url, user, password)` — POST на `{base_url}/auth/login` с JSON `{"username", "password"}`; из ответа взять `access_token` и вернуть `requests.Session` с заголовком авторизации. Если статус 401 — `PermissionError("неверный логин или пароль")`.
        """),
        """
        import requests


        def login(base_url, user, password):
            pass
        """,
        """
        import responses

        @responses.activate
        def test_values():
            responses.post("https://api.test/auth/login", json={"access_token": "abc"}, status=200)
            s = login("https://api.test", "anna", "secret")
            assert s.headers["Authorization"] == "Bearer abc", s.headers

        @responses.activate
        def test_wrong():
            responses.post("https://api.test/auth/login", json={"detail": "bad"}, status=401)
            try:
                login("https://api.test", "anna", "x")
            except PermissionError as e:
                assert str(e) == "неверный логин или пароль", str(e)
                return
            assert False, "Нужен PermissionError"
        """,
        """
        import requests


        def login(base_url, user, password):
            response = requests.post(f"{base_url}/auth/login", json={"username": user, "password": password}, timeout=10)
            if response.status_code == 401:
                raise PermissionError("неверный логин или пароль")
            response.raise_for_status()
            session = requests.Session()
            session.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
            return session
        """),
    cod(f"{P}-client-e5", t("""
        Клиент должен логировать запросы для отчёта. Добавь в класс `LoggingClient(base_url)` метод `get(path)`: выполняет GET и дописывает в список `self.log` строку `"GET <url> -> <статус> (<N> ms)"`, где N — время ответа `response.elapsed` в миллисекундах (целое).
        """),
        """
        import requests


        class LoggingClient:
            def __init__(self, base_url):
                self.base_url = base_url
                self.log = []
        """,
        """
        import re
        import responses

        @responses.activate
        def test_values():
            responses.get("https://api.test/health", json={"ok": True})
            c = LoggingClient("https://api.test")
            assert c.get("/health").status_code == 200
            assert len(c.log) == 1 and re.fullmatch(r"GET https://api\\.test/health -> 200 \\(\\d+ ms\\)", c.log[0]), c.log
        """,
        """
        import requests


        class LoggingClient:
            def __init__(self, base_url):
                self.base_url = base_url
                self.log = []

            def get(self, path):
                url = self.base_url + path
                response = requests.get(url, timeout=10)
                ms = int(response.elapsed.total_seconds() * 1000)
                self.log.append(f"GET {url} -> {response.status_code} ({ms} ms)")
                return response
        """),
    cmd(f"{P}-client-e6", "Какой класс `requests` переиспользует соединение и хранит общие заголовки и cookies между запросами? Введи `requests.Имя`.",
        ["requests.Session"]),
    cmd(f"{P}-client-e7", "Какое поле ответа `requests` хранит время, которое занял запрос? Введи `response.имя`.",
        ["response.elapsed"]),
    pyt(f"{P}-client-e8", t("""
        Фикстуры для API-тестов: напиши фикстуру `client`, возвращающую `ApiClient("https://api.test")` (класс в заготовке), и тест `test_me(client)`, который с помощью `responses` подменяет `GET https://api.test/me` (тело `{"name": "Аня"}`) и проверяет `client.get("/me").json()["name"]`. Используй `responses` как контекстный менеджер внутри теста: `with responses.RequestsMock() as mock:`.
        """),
        """
        import pytest
        import requests
        import responses


        class ApiClient:
            def __init__(self, base_url):
                self.base_url = base_url
                self.session = requests.Session()

            def get(self, path):
                return self.session.get(self.base_url + path, timeout=10)
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_me") == "passed", res
            src = open("solution.py", encoding="utf-8").read()
            assert "@pytest.fixture" in src and "RequestsMock" in src, "Нужна фикстура client и responses.RequestsMock"
        """,
        """
        import pytest
        import requests
        import responses


        class ApiClient:
            def __init__(self, base_url):
                self.base_url = base_url
                self.session = requests.Session()

            def get(self, path):
                return self.session.get(self.base_url + path, timeout=10)


        @pytest.fixture
        def client():
            return ApiClient("https://api.test")


        def test_me(client):
            with responses.RequestsMock() as mock:
                mock.get("https://api.test/me", json={"name": "Аня"})
                assert client.get("/me").json()["name"] == "Аня"
        """, xp=25),
),

lesson(f"{P}-m2-l2", "Моки и параметризация",
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
    out(f"{P}-m2-l2-e6", "Что выведет программа? Несколько ответов подряд.", """
        import requests
        import responses

        with responses.RequestsMock() as mock:
            mock.get("https://api.test/job", json={"status": "pending"})
            mock.get("https://api.test/job", json={"status": "done"})
            print([requests.get("https://api.test/job").json()["status"] for _ in range(3)])
        """, hint="Одинаковые URL отдаются по очереди; последний ответ повторяется."),
    pyt(f"{P}-m2-l2-e7", t("""
        Параметризуй API-тест: `test_status(code, expected)` для функции `is_available(url)` — подменяй `GET https://api.test/health` ответом `code` и проверяй результат: `200 → True`, `503 → False`, `500 → False`.
        """),
        """
        import pytest
        import requests
        import responses


        def is_available(url):
            return requests.get(url, timeout=5).status_code == 200
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert len(res) == 3 and all(v == "passed" for v in res.values()), res

        def test_catches_bug():
            import requests as rq
            code, res = run_pytest(patch={"is_available": lambda url: rq.get(url, timeout=5).status_code < 600})
            assert code == 1, "Тест должен ловить неправильную проверку статуса"
        """,
        """
        import pytest
        import requests
        import responses


        def is_available(url):
            return requests.get(url, timeout=5).status_code == 200


        @pytest.mark.parametrize("code, expected", [(200, True), (503, False), (500, False)])
        @responses.activate
        def test_status(code, expected):
            responses.get("https://api.test/health", status=code)
            assert is_available("https://api.test/health") == expected
        """),
    pyt(f"{P}-m2-l2-e8", t("""
        Проверь повторы при сбоях: функция `fetch_with_retry(url)` делает до 3 попыток при статусах 5xx. Напиши тест `test_retry_until_ok`: подмени **три** ответа для одного URL — `503`, `502`, `200` с телом `{"ok": true}` — и проверь, что функция вернула `{"ok": True}` и было ровно 3 запроса (`len(responses.calls)`).
        """),
        """
        import pytest
        import requests
        import responses


        def fetch_with_retry(url, attempts=3):
            for _ in range(attempts):
                r = requests.get(url, timeout=5)
                if r.status_code < 500:
                    return r.json()
            r.raise_for_status()
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_retry_until_ok") == "passed", res

        def test_catches_bugs():
            import requests as rq
            def no_retry(url, attempts=3):
                r = rq.get(url, timeout=5)
                return r.json() if r.status_code < 500 else None
            def too_many(url, attempts=3):
                result = None
                for _ in range(4):
                    r = rq.get(url, timeout=5)
                    if r.status_code < 500:
                        result = r.json()
                return result
            for bug in (no_retry, too_many):
                code, res = run_pytest(patch={"fetch_with_retry": bug})
                assert code == 1, f"Тест пропустил ошибку ({bug.__name__})"
        """,
        """
        import pytest
        import requests
        import responses


        def fetch_with_retry(url, attempts=3):
            for _ in range(attempts):
                r = requests.get(url, timeout=5)
                if r.status_code < 500:
                    return r.json()
            r.raise_for_status()


        @responses.activate
        def test_retry_until_ok():
            responses.get("https://api.test/data", status=503)
            responses.get("https://api.test/data", status=502)
            responses.get("https://api.test/data", json={"ok": True}, status=200)
            assert fetch_with_retry("https://api.test/data") == {"ok": True}
            assert len(responses.calls) == 3
        """, xp=25),
),
)
