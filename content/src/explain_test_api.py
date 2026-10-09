"""Тема «API-тестирование» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "api"

EXPLAIN = {

# ===== Модуль 1. HTTP для тестировщика =====

f"{P}-m1-l1-e1": x(
    idea="Класс ответа — первая цифра кода: целочисленное деление на 100.",
    lines=[("print(code, code // 100)", "201 → 2, 404 → 4, 503 → 5.")],
    mistake="`code / 100` — получится 2.01."),

f"{P}-m1-l1-e2": x(
    idea="`urlparse` делит адрес на части, `parse_qs` разбирает параметры — значения всегда списки.",
    lines=[
        ("print(url.netloc)", "Хост."),
        ("print(url.path)", "Путь без параметров."),
        ("print(parse_qs(url.query))", "Параметр может повторяться — поэтому списки."),
    ],
    mistake="Ожидать `{'status': 'new'}` — `parse_qs` даёт списки."),

f"{P}-m1-l1-e3": x(
    idea="Первая цифра — ключ словаря классов.",
    lines=[('return {2: "success", 3: "redirect", 4: "client_error", 5: "server_error"}[code // 100]', "Словарь вместо цепочки if.")],
    mistake="`str(code)[0]` — получится строка, а ключи — числа."),

f"{P}-m1-l1-e4": x(
    idea="Идемпотентные методы: повтор не меняет результат. POST и PATCH — нет.",
    lines=[('return method.upper() in {"GET", "HEAD", "OPTIONS", "PUT", "DELETE"}', "Регистр приводим к верхнему.")],
    mistake="Считать PUT неидемпотентным — повторная замена даёт то же состояние."),

f"{P}-m1-l1-e5": x(
    idea="`urlencode` правильно склеивает и экранирует параметры.",
    lines=[("url = base + path", "Адрес."), ('return f"{url}?{urlencode(params)}" if params else url', "Без параметров — без `?`.")],
    mistake="Склеивать `k=v` вручную — пробелы и `&` в значениях сломают адрес."),

f"{P}-m1-l1-e6": x(
    idea="Два признака бага: сервер упал (5xx) или создание вернуло 200 вместо 201.",
    lines=[('return status >= 500 or (method == "POST" and status == 200)', "Хватит одного.")],
    mistake="Считать багом любой 4xx — это часто правильная реакция на плохой запрос."),

f"{P}-m1-l1-e7": x(
    idea="Первая строка запроса: метод, цель (путь с параметрами), версия.",
    lines=[("POST /v1/orders?debug=1 HTTP/1.1", "Путь — до `?`.")],
    mistake="Включить `?debug=1` в путь."),

f"{P}-m1-l1-e8": x(
    idea="Строку делим на три части, цель разбираем `urlsplit`, параметры — `parse_qsl` в словарь.",
    lines=[
        ("method, target, _version = line.split()", "Три слова."),
        ("parts = urlsplit(target)", "Путь и строка запроса."),
        ('return {"method": method, "path": parts.path, "query": dict(parse_qsl(parts.query))}', "`parse_qsl` — пары, значения строками."),
    ],
    mistake="`parse_qs` — значения окажутся списками."),

f"{P}-methods-e1": x(
    idea="`HTTPStatus(code).phrase` — стандартная фраза кода. Полезно запомнить основные.",
    lines=[("print(code, HTTPStatus(code).phrase)", "Код и его название.")],
    mistake="Путать 401 (не авторизован) и 403 (нет прав)."),

f"{P}-methods-e2": x(
    idea="Имена HTTP-заголовков нечувствительны к регистру — `requests` хранит их в `CaseInsensitiveDict`.",
    lines=[('print(h["content-type"], "CONTENT-TYPE" in h)', "Любой регистр работает.")],
    mistake="Ожидать `KeyError` для строчного имени."),

f"{P}-methods-e3": x(
    idea="Успешное создание — 201 Created.",
    lines=[("201", "Created.")],
    mistake="200 — тоже «успех», но для создания правильнее 201."),

f"{P}-methods-e4": x(
    idea="401 — не представился (нет или неверный токен).",
    lines=[("401", "Unauthorized.")],
    mistake="403 — представился, но прав нет."),

f"{P}-methods-e5": x(
    idea="403 — авторизован, но действие запрещено.",
    lines=[("403", "Forbidden.")],
    mistake="401 — это про отсутствие авторизации."),

f"{P}-methods-e6": x(
    idea="Токен передают в заголовке `Authorization`, обычно `Bearer <токен>`.",
    lines=[("Authorization", "Заголовок авторизации.")],
    mistake="`Token` или `Auth` — нестандартные имена."),

f"{P}-methods-e7": x(
    idea="Имена заголовков приводим к нижнему регистру — и сравниваем уже их.",
    lines=[
        ("h = {k.lower(): v for k, v in headers.items()}", "Регистр не важен."),
        ('if not h.get("content-type", "").startswith("application/json"):', "Нет заголовка — пустая строка."),
        ('if "debug" in h.get("server", "").lower():', "Отладочный сервер."),
        ('if "x-request-id" not in h:', "Нет id запроса."),
    ],
    mistake="`== \"application/json\"` — не пройдёт `application/json; charset=utf-8`."),

f"{P}-methods-e8": x(
    idea="Сначала неуспешный случай, потом таблица кодов с запасным 200.",
    lines=[
        ('return 422 if method == "POST" else 404', "Ошибка: невалидные данные или нет ресурса."),
        ('return {"POST": 201, "DELETE": 204}.get(method, 200)', "Остальные — 200."),
    ],
    mistake="Ждать 200 от DELETE — по REST обычно 204 без тела."),

f"{P}-m1-l2-e1": x(
    idea="JSON → Python: `true` → `True`, `null` → `None`, объект → dict.",
    lines=[('print(data["ok"], data["next"], len(data["items"]))', "Типы Python."), ("print(type(data).__name__)", "Словарь.")],
    mistake="Ожидать `true` и `null` в выводе."),

f"{P}-m1-l2-e2": x(
    idea="Вложенные данные читают цепочкой ключей и индексов.",
    lines=[
        ('print(resp["data"]["users"][0]["roles"][-1])', "Первый пользователь, последняя роль."),
        ('print([u["name"] for u in resp["data"]["users"] if u["roles"]])', "Пустой список ролей — ложь."),
    ],
    mistake="Ожидать Боря во втором списке — у него ролей нет."),

f"{P}-m1-l2-e3": x(
    idea="Тело ответа — строка; `json.loads` превращает её в словарь.",
    lines=[('return json.loads(body)["user"]["name"]', "Разбор и доступ к полю.")],
    mistake="`body[\"user\"]` — у строки нет ключей."),

f"{P}-m1-l2-e4": x(
    idea="Проверяем каждое обязательное поле по ключам ответа.",
    lines=[("return [f for f in required if f not in data]", "Порядок — как в required.")],
    mistake="Проверять значения на истинность — поле со значением 0 окажется «отсутствующим»."),

f"{P}-m1-l2-e5": x(
    idea="Каждая проверка добавляет не больше одной ошибки; `get` — без падения на отсутствующих полях.",
    lines=[
        ('if not isinstance(data.get("id"), int):', "Тип id."),
        ('if not isinstance(email, str) or "@" not in email:', "Сначала тип, потом `@`."),
        ("if not isinstance(age, int) or age < 0:", "Отрицательный возраст."),
    ],
    mistake="`\"@\" in email` без проверки типа — упадёт на `None`."),

f"{P}-m1-l2-e6": x(
    idea="`next` с генератором — первый подходящий или значение по умолчанию.",
    lines=[('return next((u for u in users if u["id"] == user_id), None)', "Нет — `None`.")],
    mistake="`[u for ...][0]` — `IndexError`, если пользователя нет."),

f"{P}-m1-l2-e7": x(
    idea="`.get(ключ, {})` по цепочке не падает; `or {}` заменяет `None`.",
    lines=[
        ('print(body.get("data", {}).get("user", {}).get("name"))', "Есть — имя."),
        ('print((body["data"]["user"].get("address") or {}).get("city", "нет"))', "`None or {}` → `{}`."),
        ('print(body.get("meta", {}).get("total", 0))', "Нет meta — 0."),
    ],
    mistake="`.get(\"address\", {})` — ключ есть, вернётся `None`, и `.get` на нём упадёт."),

f"{P}-m1-l2-e8": x(
    idea="Идём по частям пути: число — индекс списка, иначе — ключ словаря; не нашли — default.",
    lines=[
        ('for part in path.split("."):', "Части пути."),
        ("if isinstance(current, list) and part.isdigit() and int(part) < len(current):", "Индекс в пределах."),
        ("elif isinstance(current, dict) and part in current:", "Ключ есть."),
        ("return default", "Иначе — запасное значение."),
    ],
    mistake="Ловить все исключения `try/except` — скроются и настоящие ошибки."),

f"{P}-rest-e1": x(
    idea="REST: ресурс во множественном числе, id — в пути, чтение — GET.",
    lines=[("GET /users/7", "Один пользователь.")],
    mistake="`GET /getUser?id=7` — не REST-стиль."),

f"{P}-rest-e2": x(
    idea="Удаление — DELETE на адрес ресурса.",
    lines=[("DELETE /orders/15", "Заказ 15.")],
    mistake="`POST /orders/15/delete` — действие в пути."),

f"{P}-rest-e3": x(
    idea="PATCH — частичное изменение, PUT — замена целиком.",
    lines=[("PATCH", "Только email.")],
    mistake="PUT — потребует прислать весь объект."),

f"{P}-rest-e4": x(
    idea="Страниц = округление вверх от total / per_page.",
    lines=[('{"items": [...], "page": 1, "per_page": 20, "total": 93}', "93 / 20 = 4.65 → 5.")],
    mistake="Ответить 4 — последняя неполная страница тоже страница."),

f"{P}-rest-e5": x(
    idea="Полный CRUD-сценарий заканчивается проверкой, что удалённого больше нет (404).",
    lines=[
        ('item = f"{base}/{{id}}"', "`{{` — фигурная скобка в f-строке."),
        ('("POST", base, 201), ("GET", item, 200), ("PUT", item, 200),', "Создать, прочитать, заменить."),
        ('("PATCH", item, 200), ("DELETE", item, 204), ("GET", item, 404),', "Частично, удалить, проверить удаление."),
    ],
    mistake="Не проверять GET после DELETE — «удалённый» ресурс может остаться."),

f"{P}-rest-e6": x(
    idea="Округление вверх без float: `(total + per_page - 1) // per_page`. Страница — срез.",
    lines=[
        ("return (total + per_page - 1) // per_page", "93, 20 → 5."),
        ("start = (page - 1) * per_page", "Страницы с 1."),
        ("return items[start:start + per_page]", "Вне диапазона — пустой срез."),
    ],
    mistake="`total // per_page` — потеряется неполная страница."),

f"{P}-rest-e7": x(
    idea="Запрашиваем страницы, пока текущая не последняя.",
    lines=[
        ("resp = fetch_page(page)", "Очередная страница."),
        ('items.extend(resp["items"])', "Копим элементы."),
        ('if resp["page"] >= resp["pages"]:\n            return items', "Последняя — выходим."),
    ],
    mistake="`append` вместо `extend` — получится список списков."),

f"{P}-rest-e8": x(
    idea="Фильтр, сортировка и страница — параметры строки запроса через `&`.",
    lines=[("GET /users?status=active&sort=name&page=2", "Первый — после `?`, остальные — через `&`.")],
    mistake="Писать все через `?`."),

# ===== Модуль 2. Клиенты и автотесты =====

f"{P}-requests-e1": x(
    idea="`responses` подменяет сервер: запрос не уходит в сеть, а получает заданный ответ.",
    lines=[
        ('mock.get("https://api.test/users/1", json={"id": 1, "name": "Аня"}, status=200)', "Заготовленный ответ."),
        ("print(r.status_code, r.ok)", "`ok` — True для кодов меньше 400."),
        ('print(r.json()["name"], r.headers["Content-Type"])', "`json=` выставил Content-Type."),
    ],
    mistake="Думать, что тест обращается к настоящему серверу."),

f"{P}-requests-e2": x(
    idea="`params` — в адрес, `json` — в тело, `headers` — заголовки. `mock.calls` хранит отправленное.",
    lines=[
        ('sent = mock.calls[0].request', "Что реально ушло."),
        ("print(r.status_code, sent.url)", "Параметры добавились в URL."),
        ('print(json.loads(sent.body), sent.headers["Authorization"])', "Тело и заголовок."),
    ],
    mistake="Ожидать `notify=false` в теле — это параметр адреса."),

f"{P}-requests-e3": x(
    idea="`raise_for_status` бросает `HTTPError` для 4xx/5xx; ответ доступен в `e.response`.",
    lines=[("r.raise_for_status()", "403 — исключение."), ('print("ошибка:", e.response.status_code)', "Код из исключения.")],
    mistake="Думать, что `requests.get` сам падает на 403 — нет, только после `raise_for_status`."),

f"{P}-requests-e4": x(
    idea="Таймаут обязателен; не 200 — своя понятная ошибка.",
    lines=[
        ('response = requests.get(f"{base_url}/users/{user_id}", timeout=5)', "Запрос с таймаутом."),
        ('raise LookupError(f"user {user_id}: {response.status_code}")', "Ошибка с кодом."),
        ("return response.json()", "Тело."),
    ],
    mistake="Без timeout — тест повиснет, если сервер не ответит."),

f"{P}-requests-e5": x(
    idea="`json=` сериализует тело и ставит Content-Type; токен — в заголовке.",
    lines=[
        ('json={"name": name},', "Тело."),
        ('headers={"Authorization": f"Bearer {token}"},', "Авторизация."),
        ("return response.status_code, response.json()", "Кортеж."),
    ],
    mistake="`data={...}` — отправится форма, а не JSON."),

f"{P}-requests-e6": x(
    idea="`params=` собирает и экранирует строку запроса.",
    lines=[('response = requests.get(f"{base_url}/search", params={"q": query, "page": page}, timeout=5)', "Параметры словарём.")],
    mistake="Склеивать `?q=` вручную — запрос с пробелом или `&` сломается."),

f"{P}-requests-e7": x(
    idea="Недоступный сервер — исключение; ловим только сетевые ошибки.",
    lines=[
        ("response = requests.get(url, timeout=2)", "Попытка."),
        ('except (requests.ConnectionError, requests.Timeout):\n        return "down"', "Сервер не ответил."),
        ('return "up" if response.status_code == 200 else "down"', "Код ответа."),
    ],
    mistake="`except Exception` — спрячет ошибки в самом коде."),

f"{P}-requests-e8": x(
    idea="Без `timeout` запрос может ждать бесконечно.",
    lines=[("timeout", "Секунды ожидания.")],
    mistake="Надеяться на таймаут по умолчанию — у requests его нет."),

f"{P}-m2-l1-e1": x(
    idea="Две базовые проверки ответа: код и содержимое.",
    lines=[("assert resp.status_code == 200", "Код."), ('assert resp.json()["id"] == 1', "Тело.")],
    mistake="Проверить только код — сервер может вернуть 200 с чужими данными."),

f"{P}-m2-l1-e2": x(
    idea="Сначала наличие ключа, потом его содержимое — так ошибка будет понятной.",
    lines=[('data = client.get("/users/1").json()', "Тело."), ('assert "email" in data', "Ключ есть."), ('assert "@" in data["email"]', "Похоже на почту.")],
    mistake="Сразу `data[\"email\"]` — при отсутствии ключа упадёт с KeyError."),

f"{P}-m2-l1-e3": x(
    idea="Негативный тест: неправильный запрос — правильная ошибка.",
    lines=[('resp = client.get("/users/999")', "Несуществующий."), ("assert resp.status_code == 404", "Not Found.")],
    mistake="Ожидать 500 — это баг сервера, а не правильный ответ."),

f"{P}-m2-l1-e4": x(
    idea="Создание: 201, в ответе есть id и переданные данные.",
    lines=[
        ("assert resp.status_code == 201", "Created."),
        ('assert "id" in data', "Сервер выдал id."),
        ('assert data["name"] == "Боря"', "Данные сохранились."),
    ],
    mistake="Проверять 200 — тест пропустит неправильный код."),

f"{P}-m2-l1-e5": x(
    idea="Сквозная проверка: созданное действительно сохраняется и читается.",
    lines=[
        ('created = client.post("/users", json={"name": "Вика"}).json()', "Создаём."),
        ("fetched = client.get(f\"/users/{created['id']}\").json()", "Читаем по выданному id."),
        ('assert fetched["name"] == "Вика"', "Совпадает."),
    ],
    mistake="Проверять только ответ POST — сервер мог не сохранить данные."),

f"{P}-m2-l1-e6": x(
    idea="`@responses.activate` включает подмену на время теста.",
    lines=[
        ("@responses.activate", "Сеть подменена."),
        ('responses.get("https://api.test/users/1", json={"id": 1, "name": "Аня"})', "Ответ сервера."),
        ('assert get_user(1) == {"id": 1, "name": "Аня"}', "Функция вернула тело."),
    ],
    mistake="Забыть декоратор — запрос уйдёт в настоящую сеть."),

f"{P}-m2-l1-e7": x(
    idea="Подменяем ответ 404 и проверяем, что функция выбросит ошибку.",
    lines=[
        ('responses.get("https://api.test/users/99", status=404, json={"error": "not found"})', "Сервер «не нашёл»."),
        ("with pytest.raises(requests.HTTPError):", "`raise_for_status` внутри функции."),
    ],
    mistake="Ждать `None` — функция бросает исключение."),

f"{P}-m2-l1-e8": x(
    idea="`responses.calls` хранит отправленные запросы — проверяем, что клиент отправил правильное тело.",
    lines=[
        ('assert create_user("Аня") == 201', "Ответ."),
        ('assert json.loads(responses.calls[0].request.body) == {"name": "Аня"}', "Тело запроса."),
    ],
    mistake="Сравнивать `body` со строкой — порядок и пробелы в JSON могут отличаться."),

f"{P}-client-e1": x(
    idea="Заголовки сессии добавляются ко всем её запросам.",
    lines=[('s.headers.update({"Authorization": "Bearer t1"})', "Один раз."), ('print([c.request.headers["Authorization"] for c in mock.calls])', "У обоих запросов.")],
    mistake="Передавать токен в каждом вызове вручную."),

f"{P}-client-e2": x(
    idea="Клиент хранит базовый адрес и сессию; общий метод `request` добавляет таймаут.",
    lines=[
        ('self.base_url = base_url.rstrip("/")', "Без двойного `//`."),
        ('self.session.headers["Authorization"] = f"Bearer {token}"', "Токен — в сессию."),
        ('kwargs.setdefault("timeout", 10)', "Таймаут, если не задан."),
        ('return self.request("GET", path, **kwargs)', "get и post — через общий метод."),
    ],
    mistake="`kwargs[\"timeout\"] = 10` — затрёт переданный таймаут."),

f"{P}-client-e3": x(
    idea="Обёртка над эндпоинтами: тест читается как `users.create(\"anna\")`, а пути живут в одном месте.",
    lines=[
        ('return self.client.request("GET", f"/users/{user_id}")', "Чтение."),
        ('return self.client.request("POST", "/users", json={"name": name, "role": role})', "Создание."),
        ('return self.client.request("DELETE", f"/users/{user_id}")', "Удаление."),
    ],
    mistake="Писать URL прямо в тестах — при смене пути правок десятки."),

f"{P}-client-e4": x(
    idea="Логин: получить токен и вернуть сессию, которая дальше авторизована.",
    lines=[
        ('if response.status_code == 401:\n        raise PermissionError("неверный логин или пароль")', "Понятная ошибка."),
        ("response.raise_for_status()", "Прочие ошибки."),
        ("session.headers[\"Authorization\"] = f\"Bearer {response.json()['access_token']}\"", "Токен в сессию."),
    ],
    mistake="Не проверить статус — KeyError на `access_token` вместо понятной ошибки."),

f"{P}-client-e5": x(
    idea="`response.elapsed` — время ответа (`timedelta`); переводим в миллисекунды.",
    lines=[
        ("ms = int(response.elapsed.total_seconds() * 1000)", "Секунды → миллисекунды."),
        ('self.log.append(f"GET {url} -> {response.status_code} ({ms} ms)")', "Строка лога."),
    ],
    mistake="`response.elapsed.seconds` — только целые секунды, миллисекунды пропадут."),

f"{P}-client-e6": x(
    idea="`Session` держит соединение и общие заголовки, cookies.",
    lines=[("requests.Session", "Переиспользуемая сессия.")],
    mistake="`requests.Client` — это из httpx."),

f"{P}-client-e7": x(
    idea="`elapsed` — время от отправки запроса до получения заголовков ответа.",
    lines=[("response.elapsed", "`timedelta`.")],
    mistake="`response.time` — такого поля нет."),

f"{P}-client-e8": x(
    idea="Фикстура отдаёт клиента, а подмена сервера живёт внутри теста.",
    lines=[
        ('return ApiClient("https://api.test")', "Один клиент на тест."),
        ("with responses.RequestsMock() as mock:", "Подмена только в этом блоке."),
        ('assert client.get("/me").json()["name"] == "Аня"', "Клиент собрал правильный адрес."),
    ],
    mistake="Создавать клиента в каждом тесте вручную."),

f"{P}-m2-l2-e1": x(
    idea="`Mock` записывает вызовы и возвращает `return_value`.",
    lines=[
        ('api.get.return_value = {"status": "ok"}', "Что вернёт вызов."),
        ("print(api.get.call_count)", "Сколько раз вызывали."),
        ('api.get("/users")', "Второй вызов."),
    ],
    mistake="Ожидать, что разные аргументы дадут разные ответы — ответ один на все."),

f"{P}-m2-l2-e2": x(
    idea="`side_effect` со списком: каждый вызов берёт следующий элемент; исключение — выбрасывается.",
    lines=[('m = Mock(side_effect=[1, 2, ValueError("стоп")])', "Три вызова."), ("print(m(), m())", "1 и 2."), ("m()", "Третий — ошибка.")],
    mistake="Ожидать, что ValueError вернётся как значение."),

f"{P}-m2-l2-e3": x(
    idea="Прогоняем все случаи и копим описания несовпадений.",
    lines=[
        ("for arg, expected in cases:", "Пары."),
        ("got = func(arg)", "Фактический результат."),
        ('failures.append(f"func({arg}) = {got}, expected {expected}")', "Описание ошибки."),
    ],
    mistake="Остановиться на первом несовпадении — остальные не будут видны."),

f"{P}-m2-l2-e4": x(
    idea="Зависимость (почта) передаётся параметром — в тесте её подменяют `Mock`, чтобы проверить вызов.",
    lines=[
        ('if "@" not in email:\n        raise ValueError("invalid email")', "Плохой адрес — письма нет."),
        ('mailer.send(email, "Добро пожаловать!")', "Вызов, который проверит тест."),
    ],
    mistake="Отправить письмо до проверки адреса."),

f"{P}-m2-l2-e5": x(
    idea="Повторяем только при 5xx; 4xx — ошибка клиента, повтор не поможет.",
    lines=[
        ("for _ in range(attempts):", "До N попыток."),
        ("if resp.status_code < 500:\n            return resp", "Не серверная ошибка — сразу ответ."),
        ("return resp", "Попытки кончились — последний ответ."),
    ],
    mistake="Повторять на 404 — бессмысленные запросы."),

f"{P}-m2-l2-e6": x(
    idea="Несколько ответов на один URL отдаются по очереди; последний повторяется.",
    lines=[('mock.get("https://api.test/job", json={"status": "pending"})', "Первый."), ('mock.get("https://api.test/job", json={"status": "done"})', "Второй и дальше.")],
    mistake="Ожидать ошибку на третьем запросе."),

f"{P}-m2-l2-e7": x(
    idea="Параметризация и подмена вместе: каждый случай подменяет свой статус.",
    lines=[
        ('@pytest.mark.parametrize("code, expected", [(200, True), (503, False), (500, False)])', "Случаи."),
        ("@responses.activate", "Подмена на каждый случай."),
        ('responses.get("https://api.test/health", status=code)', "Ответ с нужным кодом."),
    ],
    mistake="Забыть `@responses.activate` — запрос уйдёт в настоящую сеть."),

f"{P}-m2-l2-e8": x(
    idea="Три ответа подряд моделируют «сервер ожил на третьей попытке».",
    lines=[
        ('responses.get("https://api.test/data", status=503)', "1."),
        ('responses.get("https://api.test/data", json={"ok": True}, status=200)', "3 — успех."),
        ("assert len(responses.calls) == 3", "Ровно три запроса."),
    ],
    mistake="Не проверить число вызовов — лишние повторы останутся незамеченными."),

# ===== Модуль 3. Валидация: Pydantic и JSON Schema =====

f"{P}-pydantic-e1": x(
    idea="Pydantic приводит типы: строка «7» стала числом; значения по умолчанию подставляются.",
    lines=[
        ('u = User.model_validate({"id": "7", "name": "Аня"})', "Проверка и приведение."),
        ("print(u.id, type(u.id).__name__, u.active)", "int, active по умолчанию."),
        ("print(u.model_dump())", "Обратно в словарь."),
    ],
    mistake="Ожидать строку `'7'` — режим по умолчанию нестрогий."),

f"{P}-pydantic-e2": x(
    idea="`ValidationError` собирает все ошибки сразу; у каждой есть путь и тип.",
    lines=[
        ('User.model_validate({"id": "abc"})', "Две проблемы."),
        ("print(e.error_count())", "2."),
        ('print(err["loc"], err["type"])', "Поле и тип ошибки."),
    ],
    mistake="Ожидать только первую ошибку."),

f"{P}-pydantic-e3": x(
    idea="Модель описывает форму данных аннотациями типов.",
    lines=[("tags: list[str] = []", "Необязательное поле."), ("return Product.model_validate(data)", "Объект из словаря.")],
    mistake="Бояться `= []` — Pydantic копирует значение по умолчанию для каждого объекта."),

f"{P}-pydantic-e4": x(
    idea="`err[\"loc\"]` — кортеж пути; склеиваем его через точку.",
    lines=[
        ("model.model_validate(data)", "Проверка."),
        ('return sorted(".".join(str(p) for p in err["loc"]) for err in e.errors())', "Пути ошибок."),
        ("return []", "Ошибок нет."),
    ],
    mistake="`\".\".join(err[\"loc\"])` — индексы списков в пути — числа."),

f"{P}-pydantic-e5": x(
    idea="`extra=\"forbid\"` — лишние поля в ответе считаются ошибкой.",
    lines=[('model_config = ConfigDict(extra="forbid")', "Строгая модель."), ("except ValidationError:\n        return False", "Не прошёл.")],
    mistake="По умолчанию лишние поля игнорируются — утечка данных в ответе пройдёт незамеченной."),

f"{P}-pydantic-e6": x(
    idea="`exclude_none=True` — не отправлять поля без значения.",
    lines=[("age: int | None = None", "Необязательное поле."), ("return user.model_dump(exclude_none=True)", "Без `None`.")],
    mistake="Отправить `\"age\": null` — сервер может трактовать это как «стереть»."),

f"{P}-pydantic-e7": x(
    idea="В Pydantic v2 — `model_validate`.",
    lines=[("Model.model_validate", "Словарь → объект с проверкой.")],
    mistake="`parse_obj` — это v1."),

f"{P}-pydantic-e8": x(
    idea="В v2 — `model_dump()`.",
    lines=[("obj.model_dump()", "Объект → словарь.")],
    mistake="`.dict()` — устаревший метод v1."),

f"{P}-pydantic-adv-e1": x(
    idea="`Field` задаёт ограничения: длину строки, границы числа.",
    lines=[
        ("title: str = Field(min_length=2, max_length=20)", "Длина."),
        ("qty: int = Field(gt=0, le=100)", "gt — строго больше, le — не больше."),
        ('print([err["type"] for err in e.errors()])', "Обе ошибки второго случая."),
    ],
    mistake="Думать, что `gt=0` пропустит 0."),

f"{P}-pydantic-adv-e2": x(
    idea="`alias` — имя поля в JSON; в Python используем своё имя.",
    lines=[
        ('user_id: int = Field(alias="userId")', "В API — camelCase."),
        ("print(u.user_id, u.first_name)", "В коде — snake_case."),
        ("print(u.model_dump(by_alias=True))", "Обратно с именами API."),
    ],
    mistake="Ждать `userId` в `model_dump()` без `by_alias`."),

f"{P}-pydantic-adv-e3": x(
    idea="Ограничения через `Field`: длина, диапазон, регулярное выражение.",
    lines=[
        ("username: str = Field(min_length=3, max_length=20)", "Длина имени."),
        ("age: int = Field(ge=18, le=120)", "Включительно."),
        ('email: str = Field(pattern=r"^[^@]+@[^@]+\\.[a-z]+$")', "Шаблон почты."),
    ],
    mistake="`gt=18` — 18 лет не пройдёт."),

f"{P}-pydantic-adv-e4": x(
    idea="`@field_validator` — своя проверка или преобразование поля; возвращает итоговое значение.",
    lines=[
        ('@field_validator("code")', "Для поля code."),
        ('raise ValueError("неизвестный HTTP-код")', "Станет ошибкой валидации."),
        ("return value.strip().lower()", "Нормализация текста."),
    ],
    mistake="Забыть `return value` — поле станет `None`."),

f"{P}-pydantic-adv-e5": x(
    idea="Вложенные модели разбираются автоматически — список словарей станет списком `Item`.",
    lines=[
        ("items: list[Item]", "Список моделей."),
        ("coupon: str | None = None", "Необязательное поле."),
        ("return sum(item.price for item in self.items)", "Методы — как у обычного класса."),
    ],
    mistake="`item[\"price\"]` — это объекты, а не словари."),

f"{P}-pydantic-adv-e6": x(
    idea="`Literal` разрешает только перечисленные значения.",
    lines=[
        ('status: Literal["new", "in_progress", "done"]', "Допустимые статусы."),
        ('bad.add(data.get("status"))', "Запоминаем неверный."),
        ("return sorted(bad)", "Уникальные по алфавиту."),
    ],
    mistake="Сравнивать со списком вручную — модель уже умеет."),

f"{P}-pydantic-adv-e7": x(
    idea="`populate_by_name` — можно создать и по псевдониму, и по имени поля; `datetime` разберёт ISO-строку.",
    lines=[
        ("model_config = ConfigDict(populate_by_name=True)", "Оба способа."),
        ('created_at: datetime = Field(alias="createdAt")', "Строка → datetime."),
        ('is_admin: bool = Field(default=False, alias="isAdmin")', "Значение по умолчанию и псевдоним."),
    ],
    mistake="`Field(False, alias=…)` — работает, но `default=` понятнее."),

f"{P}-pydantic-adv-e8": x(
    idea="`by_alias=True` выводит ключи как в API.",
    lines=[("by_alias=True", "camelCase на выходе.")],
    mistake="`alias=True` — неверное имя параметра."),

f"{P}-schema-e1": x(
    idea="`validate` молчит при успехе и бросает `ValidationError` при первой ошибке.",
    lines=[('validate({"id": 1, "name": "Аня"}, schema)', "Валидно."), ('validate({"id": "1"}, schema)', "Первая найденная ошибка — нет name.")],
    mistake="Ожидать ошибку про тип id — сообщается одна ошибка."),

f"{P}-schema-e2": x(
    idea="`iter_errors` выдаёт все ошибки; `path` — где, `validator` — какое правило нарушено.",
    lines=[
        ("errors = sorted(v.iter_errors({\"tags\": [\"a\", 2]}), key=lambda e: list(e.path))", "Все ошибки по порядку пути."),
        ("print(list(e.path), e.validator)", "Нет id (корень) и не строка в tags[1]."),
    ],
    mistake="`validate` — покажет только одну."),

f"{P}-schema-e3": x(
    idea="Схема описывает типы, обязательные поля, ограничения и запрет лишнего.",
    lines=[
        ('"required": ["id", "email"],', "Обязательные."),
        ('"additionalProperties": False,', "Лишние поля — ошибка."),
        ('"role": {"enum": ["admin", "qa", "guest"]},', "Одно из значений."),
    ],
    mistake="Забыть `additionalProperties` — лишние поля пройдут."),

f"{P}-schema-e4": x(
    idea="Схема для каждого элемента массива — в `items`; путь ошибки склеиваем через `/`.",
    lines=[
        ('"items": {"type": "object", "required": ["id"], "properties": {"id": {"type": "integer"}}},', "Схема элемента."),
        ('path = "/".join(str(p) for p in error.path) or "$"', "Корень — `$`."),
        ('result.append(f"{path}: {error.validator}")', "Сообщение."),
    ],
    mistake="`required` внутри `properties` — так не работает, это отдельное ключевое слово."),

f"{P}-schema-e5": x(
    idea="Pydantic сам строит JSON Schema по модели.",
    lines=[("return model.model_json_schema()", "Схема модели."), ('return sorted(schema_for(model).get("required", []))', "Поля без значения по умолчанию.")],
    mistake="Писать схему вручную, когда модель уже есть."),

f"{P}-schema-e6": x(
    idea="`required` — список обязательных полей объекта.",
    lines=[("required", "Обязательные.")],
    mistake="`properties` — описывает поля, но не делает их обязательными."),

f"{P}-schema-e7": x(
    idea="`items` — схема каждого элемента массива.",
    lines=[("items", "Для элементов.")],
    mistake="`properties` — для полей объекта."),

f"{P}-schema-e8": x(
    idea="Если модели уже есть, Pydantic проверит ответ и даст удобный объект.",
    lines=[("Pydantic", "Модели и есть контракт.")],
    mistake="Дублировать одни и те же поля в моделях и схемах."),

f"{P}-practice-e1": x(
    idea="Контрактный тест: подменили ответ, провалидировали моделью, проверили данные.",
    lines=[
        ('responses.get("https://api.test/users/1", json={"id": 1, "name": "Аня", "email": "anna@x.ru"})', "Ответ сервера."),
        ("user = User.model_validate(api_get_user(1))", "Форма ответа."),
        ('assert user.name == "Аня"', "Содержимое."),
    ],
    mistake="Проверять только поля — изменение типа (id строкой) не заметишь."),

f"{P}-practice-e2": x(
    idea="Негативные случаи в параметризации; подмена — внутри теста на каждый случай.",
    lines=[
        ("({}, 422),", "Пустое тело."),
        ('({"name": "Аня"}, 201),', "Контрольный хороший случай."),
        ('mock.post("https://api.test/users", status=expected_status, json={})', "Ответ под случай."),
    ],
    mistake="Не добавить позитивный случай — сломанную подмену не отличить от правильной валидации."),

f"{P}-practice-e3": x(
    idea="SLA — и успешный статус, и время в пределах лимита.",
    lines=[
        ("ms = int(response.elapsed.total_seconds() * 1000)", "Время ответа."),
        ("return response.status_code == 200 and ms <= max_ms, ms", "Оба условия."),
    ],
    mistake="Проверять только время — быстрый ответ 500 «пройдёт»."),

f"{P}-practice-e4": x(
    idea="Объединение ключей обоих словарей; вложенные словари сравниваем рекурсивно.",
    lines=[
        ("for key in expected.keys() | actual.keys():", "Все ключи."),
        ('if key not in actual:\n            result.append("-" + path)', "Пропало."),
        ('elif key not in expected:\n            result.append("+" + path)', "Лишнее."),
        ('result.extend(diff_keys(expected[key], actual[key], path + "."))', "Глубже."),
    ],
    mistake="Сравнивать значения — для контракта важна структура."),

f"{P}-practice-e5": x(
    idea="Одинаковые запросы получают ответы по очереди — так моделируется «был, удалили, нет».",
    lines=[
        ('responses.get(f"{BASE}/users/7", json={"id": 7, "name": "Аня"}, status=200)', "Первый GET."),
        ('responses.get(f"{BASE}/users/7", status=404)', "Второй GET."),
        ('user_id = created.json()["id"]', "id из ответа, а не константа."),
        ("assert api.get(user_id).status_code == 404", "После удаления."),
    ],
    mistake="Захардкодить id 7 в тесте — не проверится, что клиент берёт id из ответа."),

f"{P}-practice-e6": x(
    idea="HTTPie — `http GET url` с подсветкой и удобным синтаксисом.",
    lines=[("httpie", "Утилита `http`.")],
    mistake="Postman — графическая программа, не командная строка."),

f"{P}-practice-e7": x(
    idea="OpenAPI (бывший Swagger) — формат описания REST API.",
    lines=[("OpenAPI", "Стандарт.")],
    mistake="Путать спецификацию OpenAPI с инструментом Swagger UI."),

f"{P}-practice-e8": x(
    idea="Три теста: контракт, что отправляет клиент, и реакция на ошибку сервера.",
    lines=[
        ('page = OrdersPage.model_validate(get_orders("new"))', "Контракт."),
        ('assert responses.calls[0].request.url.endswith("?status=paid")', "Параметр фильтра ушёл."),
        ("with pytest.raises(requests.HTTPError):", "500 — исключение."),
    ],
    mistake="Тестировать только «счастливый путь»."),
}
