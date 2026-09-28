"""Тема «*args и **kwargs», модуль 2 «**kwargs» — задания. Теория — в _arg_t2.py."""
from ._lib import cod, lesson, module, out, t

P = "arg"

m2 = module(f"{P}-m2", "**kwargs", "🔑", "Любые именованные аргументы, распаковка словаря и практика",

lesson(f"{P}-m2-l1", "**kwargs: именованные аргументы в словарь",
    out(f"{P}-m2-l1-e1", "Что выведет программа?", """
        def show(**kwargs):
            print(kwargs, type(kwargs).__name__)

        show(a=1, b="x")
        show()
        """),
    out(f"{P}-m2-l1-e2", "Что выведет программа?", """
        def describe(**info):
            for key, value in info.items():
                print(f"{key} = {value}")

        describe(name="Аня", age=25)
        """),
    out(f"{P}-m2-l1-e3", "Что выведет программа?", """
        def count(**kw):
            return len(kw)

        print(count(), count(x=1), count(a=1, b=2, c=3))
        """),
    cod(f"{P}-m2-l1-e4", t("""
        Напиши функцию `make_dict(**kwargs)` — вернуть словарь из переданных именованных аргументов.

        ```
        make_dict(host="localhost", port=8080)   # → {"host": "localhost", "port": 8080}
        make_dict()                              # → {}
        ```
        """),
        """
        def make_dict(**kwargs):
            pass
        """,
        """
        def test_values():
            assert make_dict(host="localhost", port=8080) == {"host": "localhost", "port": 8080} and make_dict() == {}, "Неверный словарь"
        """,
        """
        def make_dict(**kwargs):
            return kwargs
        """),
    cod(f"{P}-m2-l1-e5", t("""
        Напиши функцию `keys_sorted(**kwargs)` — отсортированный список имён переданных аргументов.

        ```
        keys_sorted(b=1, a=2, c=3)   # → ["a", "b", "c"]
        ```
        """),
        """
        def keys_sorted(**kwargs):
            pass
        """,
        """
        def test_values():
            assert [keys_sorted(b=1, a=2, c=3), keys_sorted()] == [["a", "b", "c"], []], "Неверный результат"
        """,
        """
        def keys_sorted(**kwargs):
            return sorted(kwargs)
        """),
    cod(f"{P}-m2-l1-e6", t("""
        Напиши функцию `format_kwargs(**kwargs)` — строка вида `"a=1, b=2"` в порядке передачи аргументов.

        ```
        format_kwargs(timeout=5, retries=3)   # → "timeout=5, retries=3"
        format_kwargs()                       # → ""
        ```
        """),
        """
        def format_kwargs(**kwargs):
            pass
        """,
        """
        def test_values():
            assert [format_kwargs(timeout=5, retries=3), format_kwargs()] == ["timeout=5, retries=3", ""], "Неверная строка"
        """,
        """
        def format_kwargs(**kwargs):
            return ", ".join(f"{k}={v}" for k, v in kwargs.items())
        """),
    cod(f"{P}-m2-l1-e7", t("""
        Напиши функцию `only_numbers(**kwargs)` — словарь только с теми аргументами, значения которых — числа `int` или `float` (но не `bool`).

        ```
        only_numbers(a=1, b="x", c=2.5, d=True)   # → {"a": 1, "c": 2.5}
        ```
        """),
        """
        def only_numbers(**kwargs):
            pass
        """,
        """
        def test_values():
            assert only_numbers(a=1, b="x", c=2.5, d=True) == {"a": 1, "c": 2.5} and only_numbers() == {}, "Неверный результат"
        """,
        """
        def only_numbers(**kwargs):
            return {k: v for k, v in kwargs.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
        """, hint="bool — подтип int, его нужно исключить отдельно."),
    cod(f"{P}-m2-l1-e8", t("""
        Напиши функцию `to_query(**params)` — строка параметров URL: пары `ключ=значение` через `&`.

        ```
        to_query(page=2, sort="name")   # → "page=2&sort=name"
        to_query()                      # → ""
        ```
        """),
        """
        def to_query(**params):
            pass
        """,
        """
        def test_values():
            assert [to_query(page=2, sort="name"), to_query()] == ["page=2&sort=name", ""], "Неверная строка"
        """,
        """
        def to_query(**params):
            return "&".join(f"{k}={v}" for k, v in params.items())
        """),
),

lesson(f"{P}-m2-l2", "**kwargs с обычными параметрами",
    out(f"{P}-m2-l2-e1", "Что выведет программа?", """
        def connect(host, port=80, **options):
            print(host, port, options)

        connect("db")
        connect("db", 5432, timeout=5, ssl=True)
        connect(host="x", retries=3)
        """, hint="В **options попадают только те именованные аргументы, для которых нет своего параметра."),
    out(f"{P}-m2-l2-e2", "Что выведет программа? get и pop у kwargs.", """
        def f(**kw):
            timeout = kw.get("timeout", 30)
            debug = kw.pop("debug", False)
            return timeout, debug, kw

        print(f(), f(timeout=5, debug=True, x=1))
        """),
    out(f"{P}-m2-l2-e3", "Что выведет программа?", """
        def strict(a, b):
            return a + b

        def loose(a, b, **extra):
            return a + b

        try:
            strict(1, 2, c=3)
        except TypeError:
            print("TypeError")
        print(loose(1, 2, c=3))
        """),
    cod(f"{P}-m2-l2-e4", t("""
        Напиши функцию `create_user(name, **fields)` — словарь пользователя: `"name"` и все дополнительные поля. Если поле `"role"` не передано — `"user"`.

        ```
        create_user("Аня", age=25)          # → {"name": "Аня", "role": "user", "age": 25}
        create_user("root", role="admin")   # → {"name": "root", "role": "admin"}
        ```
        """),
        """
        def create_user(name, **fields):
            pass
        """,
        """
        def test_values():
            assert create_user("Аня", age=25) == {"name": "Аня", "role": "user", "age": 25}, "Роль по умолчанию — user"
            assert create_user("root", role="admin") == {"name": "root", "role": "admin"}, "Переданная роль"
        """,
        """
        def create_user(name, **fields):
            user = {"name": name, "role": "user"}
            user.update(fields)
            return user
        """),
    cod(f"{P}-m2-l2-e5", t("""
        Напиши функцию `request(method, url, **options)` — описание запроса словарём:

        - `"method"` — метод в верхнем регистре;
        - `"url"` — адрес;
        - `"timeout"` — из опций, по умолчанию `10`;
        - `"headers"` — из опций, по умолчанию пустой словарь.

        ```
        request("get", "/users", timeout=3)
        # → {"method": "GET", "url": "/users", "timeout": 3, "headers": {}}
        ```
        """),
        """
        def request(method, url, **options):
            pass
        """,
        """
        def test_values():
            assert request("get", "/users", timeout=3) == {"method": "GET", "url": "/users", "timeout": 3, "headers": {}}, "Неверный запрос"
            assert request("post", "/x", headers={"A": "1"}) == {"method": "POST", "url": "/x", "timeout": 10, "headers": {"A": "1"}}, "Неверные умолчания"
        """,
        """
        def request(method, url, **options):
            return {
                "method": method.upper(),
                "url": url,
                "timeout": options.get("timeout", 10),
                "headers": options.get("headers", {}),
            }
        """),
    cod(f"{P}-m2-l2-e6", t("""
        Напиши функцию `configure(**settings)` — настройки по умолчанию `DEFAULTS` из заготовки, поверх которых записаны переданные. `DEFAULTS` не менять.

        ```
        configure(timeout=5)   # → {"timeout": 5, "retries": 3}
        ```
        """),
        """
        DEFAULTS = {"timeout": 30, "retries": 3}

        def configure(**settings):
            pass
        """,
        """
        def test_values():
            assert configure(timeout=5) == {"timeout": 5, "retries": 3} and configure() == {"timeout": 30, "retries": 3}, "Неверные настройки"
            assert DEFAULTS == {"timeout": 30, "retries": 3}, "DEFAULTS изменился"
        """,
        """
        DEFAULTS = {"timeout": 30, "retries": 3}

        def configure(**settings):
            return {**DEFAULTS, **settings}
        """),
    cod(f"{P}-m2-l2-e7", t("""
        Напиши функцию `greet(name, **opts)` — приветствие с настройками: `greeting` (по умолчанию `"Привет"`) и `end` (по умолчанию `"!"`).

        ```
        greet("Аня")                             # → "Привет, Аня!"
        greet("Боря", greeting="Хай", end=".")   # → "Хай, Боря."
        ```
        """),
        """
        def greet(name, **opts):
            pass
        """,
        """
        def test_values():
            assert [greet("Аня"), greet("Боря", greeting="Хай", end=".")] == ["Привет, Аня!", "Хай, Боря."], "Неверное приветствие"
        """,
        """
        def greet(name, **opts):
            greeting = opts.get("greeting", "Привет")
            end = opts.get("end", "!")
            return f"{greeting}, {name}{end}"
        """),
    cod(f"{P}-m2-l2-e8", t("""
        Напиши функцию `split_known(**kw)` — разделить аргументы на известные (`"timeout"`, `"retries"`) и остальные. Вернуть пару словарей `(known, unknown)`.

        ```
        split_known(timeout=5, color="red", retries=1)
        # → ({"timeout": 5, "retries": 1}, {"color": "red"})
        ```
        """),
        """
        def split_known(**kw):
            pass
        """,
        """
        def test_values():
            assert split_known(timeout=5, color="red", retries=1) == ({"timeout": 5, "retries": 1}, {"color": "red"}), "Неверное разделение"
            assert split_known() == ({}, {}), "Пусто — два пустых словаря"
        """,
        """
        KNOWN = ("timeout", "retries")

        def split_known(**kw):
            known = {k: v for k, v in kw.items() if k in KNOWN}
            unknown = {k: v for k, v in kw.items() if k not in KNOWN}
            return known, unknown
        """),
),

lesson(f"{P}-m2-l3", "Распаковка словаря при вызове: f(**d)",
    out(f"{P}-m2-l3-e1", "Что выведет программа?", """
        def connect(host, port):
            return f"{host}:{port}"

        cfg = {"host": "localhost", "port": 5432}
        print(connect(**cfg))
        print(connect("db", **{"port": 1}))
        """),
    out(f"{P}-m2-l3-e2", "Что выведет программа?", """
        def f(a, b):
            return a - b

        params = {"b": 1, "a": 10}
        print(f(**params))
        try:
            f(**{"a": 1, "c": 2})
        except TypeError:
            print("лишний или отсутствующий ключ")
        """, hint="Порядок ключей не важен — значения раздаются по именам."),
    out(f"{P}-m2-l3-e3", "Что выведет программа? Настройки print из словаря.", """
        opts = {"sep": ", ", "end": "!\\n"}
        print("a", "b", **opts)
        print("x", "y", **{"sep": "-"})
        """),
    cod(f"{P}-m2-l3-e4", t("""
        Напиши функцию `call_with_config(func, config)` — вызвать `func`, передав пары словаря `config` как именованные аргументы.

        ```
        def area(width, height): return width * height
        call_with_config(area, {"width": 3, "height": 4})   # → 12
        ```
        """),
        """
        def call_with_config(func, config):
            pass
        """,
        """
        def test_values():
            def area(width, height):
                return width * height
            assert call_with_config(area, {"width": 3, "height": 4}) == 12 and call_with_config(dict, {"a": 1}) == {"a": 1}, "Неверный вызов"
        """,
        """
        def call_with_config(func, config):
            return func(**config)
        """),
    cod(f"{P}-m2-l3-e5", t("""
        Напиши функцию `build_url(host, port, path="/")` — строка `"http://<host>:<port><path>"` — и функцию `url_from(cfg)`, которая строит адрес из словаря настроек через `build_url(**cfg)`.

        ```
        url_from({"host": "localhost", "port": 8000})                  # → "http://localhost:8000/"
        url_from({"host": "x", "port": 1, "path": "/api"})             # → "http://x:1/api"
        ```
        """),
        """
        def build_url(host, port, path="/"):
            pass

        def url_from(cfg):
            pass
        """,
        """
        def test_values():
            assert url_from({"host": "localhost", "port": 8000}) == "http://localhost:8000/", "Неверный адрес"
            assert url_from({"host": "x", "port": 1, "path": "/api"}) == "http://x:1/api", "Путь из словаря"

        def test_unpack():
            assert "**cfg" in open("solution.py", encoding="utf-8").read(), "Используй build_url(**cfg)"
        """,
        """
        def build_url(host, port, path="/"):
            return f"http://{host}:{port}{path}"

        def url_from(cfg):
            return build_url(**cfg)
        """),
    cod(f"{P}-m2-l3-e6", t("""
        Напиши функцию `merge_call(func, defaults, overrides)` — вызвать `func` с именованными аргументами из `defaults`, поверх которых записаны `overrides`.

        ```
        def connect(host, port): return f"{host}:{port}"
        merge_call(connect, {"host": "localhost", "port": 80}, {"port": 8080})   # → "localhost:8080"
        ```
        """),
        """
        def merge_call(func, defaults, overrides):
            pass
        """,
        """
        def test_values():
            def connect(host, port):
                return f"{host}:{port}"
            assert merge_call(connect, {"host": "localhost", "port": 80}, {"port": 8080}) == "localhost:8080", "Неверный вызов"
        """,
        """
        def merge_call(func, defaults, overrides):
            return func(**{**defaults, **overrides})
        """),
    cod(f"{P}-m2-l3-e7", t("""
        Напиши функцию `safe_call(func, params)` — вызвать `func(**params)`; если ключи не подходят к параметрам функции (`TypeError`) — вернуть `None`.

        ```
        def f(a, b): return a + b
        safe_call(f, {"a": 1, "b": 2})   # → 3
        safe_call(f, {"a": 1, "c": 2})   # → None
        ```
        """),
        """
        def safe_call(func, params):
            pass
        """,
        """
        def test_values():
            def f(a, b):
                return a + b
            assert [safe_call(f, {"a": 1, "b": 2}), safe_call(f, {"a": 1, "c": 2}), safe_call(f, {"a": 1})] == [3, None, None], "Неверный результат"
        """,
        """
        def safe_call(func, params):
            try:
                return func(**params)
            except TypeError:
                return None
        """),
    cod(f"{P}-m2-l3-e8", t("""
        Напиши функцию `format_user(name, age, city="?")` — строка `"<name>, <age>, <city>"` — и `format_all(records)` — применить `format_user` к каждому словарю из списка через `**`.

        ```
        format_all([{"name": "Аня", "age": 25}, {"age": 30, "name": "Боря", "city": "Казань"}])
        # → ["Аня, 25, ?", "Боря, 30, Казань"]
        ```
        """),
        """
        def format_user(name, age, city="?"):
            pass

        def format_all(records):
            pass
        """,
        """
        def test_values():
            got = format_all([{"name": "Аня", "age": 25}, {"age": 30, "name": "Боря", "city": "Казань"}])
            assert got == ["Аня, 25, ?", "Боря, 30, Казань"], f"Получено {got}"
        """,
        """
        def format_user(name, age, city="?"):
            return f"{name}, {age}, {city}"

        def format_all(records):
            return [format_user(**r) for r in records]
        """),
),

lesson(f"{P}-m2-l4", "kwargs на практике",
    out(f"{P}-m2-l4-e1", "Что выведет программа?", """
        def payload(**fields):
            return {k: v for k, v in fields.items() if v is not None}

        print(payload(name="Аня", email=None, age=25))
        """),
    out(f"{P}-m2-l4-e2", "Что выведет программа?", """
        def update(obj, **changes):
            new = dict(obj)
            new.update(changes)
            return new

        user = {"name": "Аня", "age": 25}
        print(update(user, age=26), user)
        """),
    out(f"{P}-m2-l4-e3", "Что выведет программа? Атрибуты HTML-тега.", """
        def html(tag, text, **attrs):
            parts = "".join(f' {k}="{v}"' for k, v in attrs.items())
            return f"<{tag}{parts}>{text}</{tag}>"

        print(html("a", "ссылка", href="/x"))
        print(html("p", "текст"))
        """),
    cod(f"{P}-m2-l4-e4", t("""
        Напиши функцию `payload(**fields)` — тело запроса: словарь из переданных полей **без** тех, у которых значение `None` (значения `0`, `False`, `""` оставить).

        ```
        payload(name="Аня", email=None, age=0)   # → {"name": "Аня", "age": 0}
        ```
        """),
        """
        def payload(**fields):
            pass
        """,
        """
        def test_values():
            assert payload(name="Аня", email=None, age=0) == {"name": "Аня", "age": 0} and payload(a=False) == {"a": False}, "Неверное тело"
        """,
        """
        def payload(**fields):
            return {k: v for k, v in fields.items() if v is not None}
        """),
    cod(f"{P}-m2-l4-e5", t("""
        Напиши функцию `update_copy(obj, **changes)` — новый словарь: копия `obj` с применёнными изменениями. Исходный не менять.

        ```
        update_copy({"name": "Аня", "age": 25}, age=26)   # → {"name": "Аня", "age": 26}
        ```
        """),
        """
        def update_copy(obj, **changes):
            pass
        """,
        """
        def test_values():
            src = {"name": "Аня", "age": 25}
            assert update_copy(src, age=26) == {"name": "Аня", "age": 26} and src == {"name": "Аня", "age": 25}, "Неверный результат или исходный изменён"
        """,
        """
        def update_copy(obj, **changes):
            return {**obj, **changes}
        """),
    cod(f"{P}-m2-l4-e6", t("""
        Напиши функцию `filter_users(users, **criteria)` — пользователи (словари), у которых **все** указанные поля равны заданным значениям. Без критериев — все пользователи.

        ```
        users = [{"name": "Аня", "role": "qa"}, {"name": "Боря", "role": "dev"}]
        filter_users(users, role="qa")   # → [{"name": "Аня", "role": "qa"}]
        ```
        """),
        """
        def filter_users(users, **criteria):
            pass
        """,
        """
        def test_values():
            users = [{"name": "Аня", "role": "qa", "age": 25}, {"name": "Боря", "role": "dev", "age": 25}]
            assert filter_users(users, role="qa") == [users[0]], "Фильтр по роли"
            assert filter_users(users, age=25) == users and filter_users(users) == users, "Все подходят"
            assert filter_users(users, role="qa", age=30) == [], "Оба условия"
        """,
        """
        def filter_users(users, **criteria):
            result = []
            for u in users:
                if all(u.get(k) == v for k, v in criteria.items()):
                    result.append(u)
            return result
        """, xp=20),
    cod(f"{P}-m2-l4-e7", t("""
        Напиши функцию `html(tag, text, **attrs)` — HTML-тег с атрибутами. Слово `class` в Python зарезервировано, поэтому его передают как `class_` — у имён атрибутов убирай `_` в конце.

        ```
        html("div", "hi", class_="card", id="x")   # → '<div class="card" id="x">hi</div>'
        html("p", "текст")                         # → "<p>текст</p>"
        ```
        """),
        """
        def html(tag, text, **attrs):
            pass
        """,
        """
        def test_values():
            assert html("div", "hi", class_="card", id="x") == '<div class="card" id="x">hi</div>', f"Получено {html('div', 'hi', class_='card', id='x')!r}"
            assert html("p", "текст") == "<p>текст</p>", "Без атрибутов"
        """,
        """
        def html(tag, text, **attrs):
            parts = "".join(f' {k.rstrip("_")}="{v}"' for k, v in attrs.items())
            return f"<{tag}{parts}>{text}</{tag}>"
        """),
    cod(f"{P}-m2-l4-e8", t("""
        Напиши функцию `log_event(event, **data)` — строка лога: имя события и пары `ключ=значение`, **отсортированные по ключу**, через пробел.

        ```
        log_event("login", user="anna", ok=True)   # → "login ok=True user=anna"
        log_event("start")                         # → "start"
        ```
        """),
        """
        def log_event(event, **data):
            pass
        """,
        """
        def test_values():
            assert [log_event("login", user="anna", ok=True), log_event("start")] == ["login ok=True user=anna", "start"], "Неверная строка"
        """,
        """
        def log_event(event, **data):
            parts = [event] + [f"{k}={data[k]}" for k in sorted(data)]
            return " ".join(parts)
        """),
),
)
