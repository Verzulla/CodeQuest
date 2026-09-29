"""Тема «Тестирование API», модуль 3 «Валидация: Pydantic и JSON Schema» — задания. Теория — в _api_t3.py."""
from ._lib import cmd, cod, lesson, module, out, pyt, t

P = "api"

m3 = module(f"{P}-m3", "Валидация: Pydantic и JSON Schema", "🛡️", "Модели Pydantic, поля и валидаторы, вложенные модели, JSON Schema, полный API-тест",

lesson(f"{P}-pydantic", "Модели Pydantic",
    out(f"{P}-pydantic-e1", "Что выведет программа?", """
        from pydantic import BaseModel

        class User(BaseModel):
            id: int
            name: str
            active: bool = True

        u = User.model_validate({"id": "7", "name": "Аня"})
        print(u.id, type(u.id).__name__, u.active)
        print(u.model_dump())
        """, hint="Pydantic приводит совместимые типы: строка '7' → число 7."),
    out(f"{P}-pydantic-e2", "Что выведет программа? Ошибка валидации.", """
        from pydantic import BaseModel, ValidationError

        class User(BaseModel):
            id: int
            name: str

        try:
            User.model_validate({"id": "abc"})
        except ValidationError as e:
            print(e.error_count())
            for err in e.errors():
                print(err["loc"], err["type"])
        """),
    cod(f"{P}-pydantic-e3", t("""
        Опиши модель `Product(BaseModel)` с полями `id: int`, `title: str`, `price: float`, `tags: list[str]` (по умолчанию пустой список). Затем функцию `parse_product(data)` — вернуть объект `Product` из словаря.
        """),
        """
        from pydantic import BaseModel
        """,
        """
        def test_values():
            p = parse_product({"id": 1, "title": "чай", "price": "99.5"})
            assert isinstance(p, Product) and p.price == 99.5 and p.tags == [], p
            assert Product(id=2, title="кофе", price=100).tags is not Product(id=3, title="x", price=1).tags, "У каждого свой список"
        """,
        """
        from pydantic import BaseModel


        class Product(BaseModel):
            id: int
            title: str
            price: float
            tags: list[str] = []


        def parse_product(data):
            return Product.model_validate(data)
        """, hint="Pydantic копирует изменяемые значения по умолчанию — [] здесь безопасен."),
    cod(f"{P}-pydantic-e4", t("""
        Напиши функцию `validation_errors(model, data)` — провалидировать словарь моделью и вернуть **отсортированный** список путей к ошибкам в виде строк через точку (`"address.city"`). Если ошибок нет — пустой список.
        """),
        """
        from pydantic import BaseModel, ValidationError


        class Address(BaseModel):
            city: str
            zip: int


        class User(BaseModel):
            id: int
            name: str
            address: Address


        def validation_errors(model, data):
            pass
        """,
        """
        def test_values():
            assert validation_errors(User, {"id": 1, "name": "Аня", "address": {"city": "Москва", "zip": 101000}}) == []
            assert validation_errors(User, {"id": "x", "address": {"zip": "abc"}}) == ["address.city", "address.zip", "id", "name"]
        """,
        """
        from pydantic import BaseModel, ValidationError


        class Address(BaseModel):
            city: str
            zip: int


        class User(BaseModel):
            id: int
            name: str
            address: Address


        def validation_errors(model, data):
            try:
                model.model_validate(data)
            except ValidationError as e:
                return sorted(".".join(str(p) for p in err["loc"]) for err in e.errors())
            return []
        """),
    cod(f"{P}-pydantic-e5", t("""
        Строгая проверка ответа API: опиши модель `Order` с полями `id: int`, `status: str`, `total: float` и настройкой **запрета лишних полей** (`model_config = ConfigDict(extra="forbid")`). Функция `is_valid_order(data)` — `True`/`False`.
        """),
        """
        from pydantic import BaseModel, ConfigDict, ValidationError
        """,
        """
        def test_values():
            assert is_valid_order({"id": 1, "status": "new", "total": 100})
            assert not is_valid_order({"id": 1, "status": "new", "total": 100, "debug": True}), "Лишнее поле — ошибка"
            assert not is_valid_order({"id": 1, "status": "new"}), "Нет обязательного поля"
        """,
        """
        from pydantic import BaseModel, ConfigDict, ValidationError


        class Order(BaseModel):
            model_config = ConfigDict(extra="forbid")

            id: int
            status: str
            total: float


        def is_valid_order(data):
            try:
                Order.model_validate(data)
            except ValidationError:
                return False
            return True
        """),
    cod(f"{P}-pydantic-e6", t("""
        Pydantic и в обратную сторону: опиши модель `NewUser` (`name: str`, `email: str`, `age: int | None = None`) и функцию `request_body(user)` — словарь для отправки в API **без полей, равных None** (`model_dump(exclude_none=True)`).
        """),
        """
        from pydantic import BaseModel
        """,
        """
        def test_values():
            assert request_body(NewUser(name="Аня", email="a@x.ru")) == {"name": "Аня", "email": "a@x.ru"}
            assert request_body(NewUser(name="Боря", email="b@x.ru", age=30)) == {"name": "Боря", "email": "b@x.ru", "age": 30}
        """,
        """
        from pydantic import BaseModel


        class NewUser(BaseModel):
            name: str
            email: str
            age: int | None = None


        def request_body(user):
            return user.model_dump(exclude_none=True)
        """),
    cmd(f"{P}-pydantic-e7", "Каким методом класса модели Pydantic v2 создать объект из словаря с проверкой? Введи `Model.метод`.",
        ["Model.model_validate"]),
    cmd(f"{P}-pydantic-e8", "Каким методом объекта Pydantic v2 получить словарь? Введи `obj.метод()`.",
        ["obj.model_dump()"], xp=15),
),

lesson(f"{P}-pydantic-adv", "Поля, валидаторы, вложенные модели",
    out(f"{P}-pydantic-adv-e1", "Что выведет программа? Ограничения полей.", """
        from pydantic import BaseModel, Field, ValidationError

        class Item(BaseModel):
            title: str = Field(min_length=2, max_length=20)
            qty: int = Field(gt=0, le=100)

        for data in [{"title": "чай", "qty": 3}, {"title": "x", "qty": 0}]:
            try:
                print(Item(**data))
            except ValidationError as e:
                print([err["type"] for err in e.errors()])
        """),
    out(f"{P}-pydantic-adv-e2", "Что выведет программа? Псевдонимы полей.", """
        from pydantic import BaseModel, Field

        class User(BaseModel):
            user_id: int = Field(alias="userId")
            first_name: str = Field(alias="firstName")

        u = User.model_validate({"userId": 5, "firstName": "Аня"})
        print(u.user_id, u.first_name)
        print(u.model_dump(by_alias=True))
        """, hint="API часто отдаёт camelCase, а в Python принято snake_case."),
    cod(f"{P}-pydantic-adv-e3", t("""
        Опиши модель `Registration` с ограничениями через `Field`: `username: str` (от 3 до 20 символов), `age: int` (от 18 до 120 включительно), `email: str` (соответствует регулярному выражению `^[^@]+@[^@]+\\.[a-z]+$`).
        """),
        """
        from pydantic import BaseModel, Field
        """,
        """
        from pydantic import ValidationError

        def ok(data):
            try:
                Registration.model_validate(data)
                return True
            except ValidationError:
                return False

        def test_values():
            assert ok({"username": "anna", "age": 18, "email": "a@x.ru"}) and ok({"username": "bob", "age": 120, "email": "b@mail.com"})
            bad = [
                {"username": "an", "age": 30, "email": "a@x.ru"},
                {"username": "anna", "age": 17, "email": "a@x.ru"},
                {"username": "anna", "age": 121, "email": "a@x.ru"},
                {"username": "anna", "age": 30, "email": "не почта"},
                {"username": "a" * 21, "age": 30, "email": "a@x.ru"},
            ]
            assert not any(ok(b) for b in bad), [b for b in bad if ok(b)]
        """,
        """
        from pydantic import BaseModel, Field


        class Registration(BaseModel):
            username: str = Field(min_length=3, max_length=20)
            age: int = Field(ge=18, le=120)
            email: str = Field(pattern=r"^[^@]+@[^@]+\\.[a-z]+$")
        """),
    cod(f"{P}-pydantic-adv-e4", t("""
        Свой валидатор: модель `Status` с полем `code: int` и `@field_validator("code")`, который пропускает только коды 100–599, иначе выбрасывает `ValueError("неизвестный HTTP-код")`. И поле `text: str`, которое валидатор приводит к нижнему регистру и обрезает пробелы.
        """),
        """
        from pydantic import BaseModel, field_validator
        """,
        """
        from pydantic import ValidationError

        def test_values():
            s = Status(code=404, text="  Not Found ")
            assert s.code == 404 and s.text == "not found", s
            try:
                Status(code=42, text="x")
            except ValidationError as e:
                assert "неизвестный HTTP-код" in str(e), str(e)
                return
            assert False, "Нужна ошибка для кода 42"
        """,
        """
        from pydantic import BaseModel, field_validator


        class Status(BaseModel):
            code: int
            text: str

            @field_validator("code")
            @classmethod
            def known_code(cls, value):
                if not 100 <= value <= 599:
                    raise ValueError("неизвестный HTTP-код")
                return value

            @field_validator("text")
            @classmethod
            def normalize(cls, value):
                return value.strip().lower()
        """, hint="@field_validator('имя') + @classmethod; вернуть (возможно изменённое) значение."),
    cod(f"{P}-pydantic-adv-e5", t("""
        Вложенные модели и списки: опиши `Item(name: str, price: float)`, `Order(id: int, items: list[Item], coupon: str | None = None)` и метод `Order.total()` — сумма цен. Ответ API `{"id": 1, "items": [{"name": "чай", "price": 100}, ...]}` должен разбираться целиком.
        """),
        """
        from pydantic import BaseModel
        """,
        """
        def test_values():
            o = Order.model_validate({"id": 1, "items": [{"name": "чай", "price": 100}, {"name": "кофе", "price": "250.5"}]})
            assert o.total() == 350.5 and isinstance(o.items[0], Item) and o.coupon is None, o
        """,
        """
        from pydantic import BaseModel


        class Item(BaseModel):
            name: str
            price: float


        class Order(BaseModel):
            id: int
            items: list[Item]
            coupon: str | None = None

            def total(self):
                return sum(item.price for item in self.items)
        """),
    cod(f"{P}-pydantic-adv-e6", t("""
        Проверка перечислений: опиши `Literal`-поле. Модель `Task` с полями `title: str` и `status: Literal["new", "in_progress", "done"]`. Функция `bad_statuses(tasks)` — вернуть отсортированный список уникальных недопустимых статусов из списка словарей-задач.
        """),
        """
        from typing import Literal
        from pydantic import BaseModel, ValidationError
        """,
        """
        def test_values():
            tasks = [{"title": "a", "status": "new"}, {"title": "b", "status": "closed"}, {"title": "c", "status": "Done"}, {"title": "d", "status": "closed"}]
            assert bad_statuses(tasks) == ["Done", "closed"], bad_statuses(tasks)
            assert Task(title="x", status="done").status == "done"
        """,
        """
        from typing import Literal
        from pydantic import BaseModel, ValidationError


        class Task(BaseModel):
            title: str
            status: Literal["new", "in_progress", "done"]


        def bad_statuses(tasks):
            bad = set()
            for data in tasks:
                try:
                    Task.model_validate(data)
                except ValidationError:
                    bad.add(data.get("status"))
            return sorted(bad)
        """),
    cod(f"{P}-pydantic-adv-e7", t("""
        API отдаёт camelCase. Опиши модель `Profile` с полями `user_id: int` (alias `userId`), `created_at: datetime` (alias `createdAt`, ISO-строка) и `is_admin: bool = False` (alias `isAdmin`). Разрешите создавать и по имени поля: `model_config = ConfigDict(populate_by_name=True)`.
        """),
        """
        from datetime import datetime
        from pydantic import BaseModel, ConfigDict, Field
        """,
        """
        from datetime import datetime

        def test_values():
            p = Profile.model_validate({"userId": 1, "createdAt": "2024-03-08T12:00:00Z"})
            assert p.user_id == 1 and p.created_at.year == 2024 and p.created_at.tzinfo is not None and p.is_admin is False, p
            q = Profile(user_id=2, created_at=datetime(2024, 1, 1))
            assert q.model_dump(by_alias=True)["userId"] == 2, q.model_dump(by_alias=True)
        """,
        """
        from datetime import datetime
        from pydantic import BaseModel, ConfigDict, Field


        class Profile(BaseModel):
            model_config = ConfigDict(populate_by_name=True)

            user_id: int = Field(alias="userId")
            created_at: datetime = Field(alias="createdAt")
            is_admin: bool = Field(default=False, alias="isAdmin")
        """),
    cmd(f"{P}-pydantic-adv-e8", "Какой параметр `model_dump(...)` выводит ключи в виде псевдонимов (как в API)? Введи `имя=значение`.",
        ["by_alias=True"], xp=15),
),

lesson(f"{P}-schema", "JSON Schema",
    out(f"{P}-schema-e1", "Что выведет программа?", """
        from jsonschema import validate, ValidationError

        schema = {
            "type": "object",
            "required": ["id", "name"],
            "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
        }
        validate({"id": 1, "name": "Аня"}, schema)
        print("ok")
        try:
            validate({"id": "1"}, schema)
        except ValidationError as e:
            print(e.message)
        """),
    out(f"{P}-schema-e2", "Что выведет программа? Все ошибки сразу.", """
        from jsonschema import Draft202012Validator

        schema = {"type": "object", "required": ["id"], "properties": {"id": {"type": "integer"}, "tags": {"type": "array", "items": {"type": "string"}}}}
        v = Draft202012Validator(schema)
        errors = sorted(v.iter_errors({"tags": ["a", 2]}), key=lambda e: list(e.path))
        for e in errors:
            print(list(e.path), e.validator)
        """),
    cod(f"{P}-schema-e3", t("""
        Напиши JSON Schema `USER_SCHEMA` для пользователя: объект, обязательные `id` (целое ≥ 1) и `email` (строка с форматом-шаблоном `@`), необязательный `role` — одно из `"admin"`, `"qa"`, `"guest"`; **лишние поля запрещены**. И функцию `is_valid(data)`.
        """),
        """
        from jsonschema import validate, ValidationError

        USER_SCHEMA = {}


        def is_valid(data):
            pass
        """,
        """
        def test_values():
            assert is_valid({"id": 1, "email": "a@x.ru"}) and is_valid({"id": 2, "email": "b@x.ru", "role": "qa"})
            bad = [{"id": 0, "email": "a@x.ru"}, {"id": 1}, {"id": 1, "email": "нет"}, {"id": 1, "email": "a@x.ru", "role": "boss"},
                   {"id": 1, "email": "a@x.ru", "debug": True}, {"id": "1", "email": "a@x.ru"}]
            assert not any(is_valid(b) for b in bad), [b for b in bad if is_valid(b)]
        """,
        """
        from jsonschema import validate, ValidationError

        USER_SCHEMA = {
            "type": "object",
            "required": ["id", "email"],
            "additionalProperties": False,
            "properties": {
                "id": {"type": "integer", "minimum": 1},
                "email": {"type": "string", "pattern": "@"},
                "role": {"enum": ["admin", "qa", "guest"]},
            },
        }


        def is_valid(data):
            try:
                validate(data, USER_SCHEMA)
            except ValidationError:
                return False
            return True
        """, hint="additionalProperties: false — запрет лишних полей; enum — список значений."),
    cod(f"{P}-schema-e4", t("""
        Схема для списка: напиши `LIST_SCHEMA` — объект с обязательными `items` (массив объектов, у каждого обязательный целый `id`) и `total` (целое ≥ 0). И функцию `schema_errors(data)` — отсортированный список сообщений `"путь: validator"` для всех ошибок (путь — элементы через `/`, пустой путь — `"$"`). Используй `Draft202012Validator(...).iter_errors`.
        """),
        """
        from jsonschema import Draft202012Validator

        LIST_SCHEMA = {}


        def schema_errors(data):
            pass
        """,
        """
        def test_values():
            assert schema_errors({"items": [{"id": 1}], "total": 1}) == []
            assert schema_errors({"items": [{"id": 1}, {"name": "x"}, {"id": "3"}], "total": -1}) == ["items/1: required", "items/2/id: type", "total: minimum"], schema_errors({"items": [{"id": 1}, {"name": "x"}, {"id": "3"}], "total": -1})
            assert schema_errors({}) == ["$: required", "$: required"], schema_errors({})
        """,
        """
        from jsonschema import Draft202012Validator

        LIST_SCHEMA = {
            "type": "object",
            "required": ["items", "total"],
            "properties": {
                "items": {
                    "type": "array",
                    "items": {"type": "object", "required": ["id"], "properties": {"id": {"type": "integer"}}},
                },
                "total": {"type": "integer", "minimum": 0},
            },
        }


        def schema_errors(data):
            result = []
            for error in Draft202012Validator(LIST_SCHEMA).iter_errors(data):
                path = "/".join(str(p) for p in error.path) or "$"
                result.append(f"{path}: {error.validator}")
            return sorted(result)
        """),
    cod(f"{P}-schema-e5", t("""
        Сгенерируй JSON Schema из модели Pydantic: функция `schema_for(model)` — вернуть `model.model_json_schema()`. Затем `required_fields(model)` — отсортированный список обязательных полей из этой схемы.
        """),
        """
        from pydantic import BaseModel


        class User(BaseModel):
            id: int
            name: str
            email: str | None = None


        def schema_for(model):
            pass


        def required_fields(model):
            pass
        """,
        """
        def test_values():
            s = schema_for(User)
            assert s["type"] == "object" and s["properties"]["id"]["type"] == "integer", s
            assert required_fields(User) == ["id", "name"], required_fields(User)
        """,
        """
        from pydantic import BaseModel


        class User(BaseModel):
            id: int
            name: str
            email: str | None = None


        def schema_for(model):
            return model.model_json_schema()


        def required_fields(model):
            return sorted(schema_for(model).get("required", []))
        """),
    cmd(f"{P}-schema-e6", "Какое ключевое слово JSON Schema перечисляет обязательные поля объекта?",
        ["required"]),
    cmd(f"{P}-schema-e7", "Какое ключевое слово JSON Schema задаёт схему для **каждого элемента** массива?",
        ["items"]),
    cmd(f"{P}-schema-e8", "Что использовать для проверки ответа, если тесты на Python и у вас уже есть модели данных: `Pydantic` или отдельные JSON-схемы? Введи `Pydantic` или `JSON Schema`.",
        ["Pydantic", "pydantic"], hint="Схемы удобны, когда их выдаёт сам API (OpenAPI) или ими обмениваются разные языки.", xp=15),
),

lesson(f"{P}-practice", "Практика: полный API-тест",
    pyt(f"{P}-practice-e1", t("""
        Собери всё вместе. Напиши тест `test_get_user_contract`: подмени `GET https://api.test/users/1` ответом `{"id": 1, "name": "Аня", "email": "anna@x.ru"}`, вызови `api_get_user(1)` и провалидируй тело моделью `User` (есть в заготовке) через `User.model_validate`. Проверь и имя.
        """),
        """
        import pytest
        import requests
        import responses
        from pydantic import BaseModel


        class User(BaseModel):
            id: int
            name: str
            email: str


        def api_get_user(user_id):
            r = requests.get(f"https://api.test/users/{user_id}", timeout=5)
            r.raise_for_status()
            return r.json()
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_get_user_contract") == "passed", res
            assert "model_validate" in open("solution.py", encoding="utf-8").read(), "Валидируй моделью User"

        def test_catches_bug():
            import requests as rq
            def no_email(user_id):
                body = rq.get(f"https://api.test/users/{user_id}", timeout=5).json()
                body.pop("email")
                return body
            code, res = run_pytest(patch={"api_get_user": no_email})
            assert code == 1, "Контракт должен ломаться, если поле пропало"
        """,
        """
        import pytest
        import requests
        import responses
        from pydantic import BaseModel


        class User(BaseModel):
            id: int
            name: str
            email: str


        def api_get_user(user_id):
            r = requests.get(f"https://api.test/users/{user_id}", timeout=5)
            r.raise_for_status()
            return r.json()


        @responses.activate
        def test_get_user_contract():
            responses.get("https://api.test/users/1", json={"id": 1, "name": "Аня", "email": "anna@x.ru"})
            user = User.model_validate(api_get_user(1))
            assert user.name == "Аня"
        """),
    pyt(f"{P}-practice-e2", t("""
        Параметризованный негативный тест: `test_create_invalid(payload, expected_status)` для функции `create_user(payload)`. Подменяй `POST https://api.test/users` ответом `expected_status` и проверяй, что функция возвращает этот статус. Случаи: `{}` → 422, `{"name": ""}` → 422, `{"name": "Аня", "age": -1}` → 422, `{"name": "Аня"}` → 201. Используй `responses.RequestsMock()` внутри теста.
        """),
        """
        import pytest
        import requests
        import responses


        def create_user(payload):
            return requests.post("https://api.test/users", json=payload, timeout=5).status_code
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert len(res) == 4 and all(v == "passed" for v in res.values()), res
        """,
        """
        import pytest
        import requests
        import responses


        def create_user(payload):
            return requests.post("https://api.test/users", json=payload, timeout=5).status_code


        @pytest.mark.parametrize("payload, expected_status", [
            ({}, 422),
            ({"name": ""}, 422),
            ({"name": "Аня", "age": -1}, 422),
            ({"name": "Аня"}, 201),
        ])
        def test_create_invalid(payload, expected_status):
            with responses.RequestsMock() as mock:
                mock.post("https://api.test/users", status=expected_status, json={})
                assert create_user(payload) == expected_status
        """),
    cod(f"{P}-practice-e3", t("""
        Проверка SLA: напиши функцию `check_sla(url, max_ms)` — сделать GET и вернуть кортеж `(ok, ms)`: `ms` — время ответа (`response.elapsed`) в миллисекундах (int), `ok` — статус 200 **и** `ms <= max_ms`.
        """),
        """
        import requests


        def check_sla(url, max_ms):
            pass
        """,
        """
        import responses

        @responses.activate
        def test_values():
            responses.get("https://api.test/fast", json={})
            responses.get("https://api.test/fail", status=500)
            ok, ms = check_sla("https://api.test/fast", 1000)
            assert ok and isinstance(ms, int) and ms >= 0, (ok, ms)
            assert check_sla("https://api.test/fail", 1000)[0] is False
        """,
        """
        import requests


        def check_sla(url, max_ms):
            response = requests.get(url, timeout=10)
            ms = int(response.elapsed.total_seconds() * 1000)
            return response.status_code == 200 and ms <= max_ms, ms
        """),
    cod(f"{P}-practice-e4", t("""
        Сравнение контракта: функция `diff_keys(expected, actual)` — сравнить структуру двух JSON-объектов (вложенные словари) и вернуть отсортированный список расхождений: `"+путь"` для лишних полей в `actual`, `"-путь"` для отсутствующих. Путь — через точку.
        """),
        """
        def diff_keys(expected, actual, prefix=""):
            pass
        """,
        """
        def test_values():
            exp = {"id": 1, "user": {"name": "a", "email": "e"}, "tags": []}
            act = {"id": 1, "user": {"name": "a", "phone": "p"}, "debug": True}
            assert diff_keys(exp, act) == ["+debug", "+user.phone", "-tags", "-user.email"], diff_keys(exp, act)
            assert diff_keys(exp, exp) == []
        """,
        """
        def diff_keys(expected, actual, prefix=""):
            result = []
            for key in expected.keys() | actual.keys():
                path = f"{prefix}{key}"
                if key not in actual:
                    result.append("-" + path)
                elif key not in expected:
                    result.append("+" + path)
                elif isinstance(expected[key], dict) and isinstance(actual[key], dict):
                    result.extend(diff_keys(expected[key], actual[key], path + "."))
            return sorted(result)
        """),
    pyt(f"{P}-practice-e5", t("""
        CRUD-сценарий на одной подменённой «базе». Напиши тест `test_crud`: зарегистрируй в `responses` ответы для `POST /users` (201, `{"id": 7, "name": "Аня"}`), `GET /users/7` (200, то же тело), `DELETE /users/7` (204), `GET /users/7` (404) — одинаковый GET регистрируется дважды и отдаётся по очереди. Используй клиент `UsersApi` из заготовки и проверь каждый шаг.
        """),
        """
        import pytest
        import requests
        import responses

        BASE = "https://api.test"


        class UsersApi:
            def create(self, name):
                return requests.post(f"{BASE}/users", json={"name": name}, timeout=5)

            def get(self, user_id):
                return requests.get(f"{BASE}/users/{user_id}", timeout=5)

            def delete(self, user_id):
                return requests.delete(f"{BASE}/users/{user_id}", timeout=5)
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res.get("test_crud") == "passed", res

        def test_catches_bug():
            class NoDelete(sys.modules["solution"].UsersApi):
                def delete(self, user_id):
                    import requests as rq
                    return rq.get(f"https://api.test/users/{user_id}", timeout=5)
            code, res = run_pytest(patch={"UsersApi": NoDelete})
            assert code == 1, "Тест должен замечать, что удаление не работает"
        """,
        """
        import pytest
        import requests
        import responses

        BASE = "https://api.test"


        class UsersApi:
            def create(self, name):
                return requests.post(f"{BASE}/users", json={"name": name}, timeout=5)

            def get(self, user_id):
                return requests.get(f"{BASE}/users/{user_id}", timeout=5)

            def delete(self, user_id):
                return requests.delete(f"{BASE}/users/{user_id}", timeout=5)


        @responses.activate
        def test_crud():
            responses.post(f"{BASE}/users", json={"id": 7, "name": "Аня"}, status=201)
            responses.get(f"{BASE}/users/7", json={"id": 7, "name": "Аня"}, status=200)
            responses.get(f"{BASE}/users/7", status=404)
            responses.delete(f"{BASE}/users/7", status=204)
            api = UsersApi()

            created = api.create("Аня")
            assert created.status_code == 201
            user_id = created.json()["id"]

            assert api.get(user_id).json()["name"] == "Аня"
            assert api.delete(user_id).status_code == 204
            assert api.get(user_id).status_code == 404
        """, hint="Регистрируй ответы до вызовов; одинаковые URL отдаются по порядку регистрации.", xp=25),
    cmd(f"{P}-practice-e6", "Какой инструмент командной строки популярен для ручной проверки API с понятным выводом (не curl)? Введи название утилиты `http` из пакета…",
        ["httpie", "HTTPie"]),
    cmd(f"{P}-practice-e7", "Как называется стандарт описания REST API (из него генерируют документацию Swagger UI и схемы)? Введи название.",
        ["OpenAPI", "openapi", "Swagger", "OpenAPI Specification"]),
    pyt(f"{P}-practice-e8", t("""
        Итог темы. Напиши набор тестов для `get_orders(status)` (функция в заготовке) с подменой `GET https://api.test/orders`:

        - `test_orders_contract` — ответ `{"items": [{"id": 1, "status": "new", "total": 100}], "total": 1}` валидируется моделью `OrdersPage` (в заготовке);
        - `test_filter_param` — проверь, что функция передаёт `status` в строке запроса: `responses.calls[0].request.url` заканчивается на `?status=paid`;
        - `test_server_error` — на ответ 500 функция выбрасывает `requests.HTTPError`.
        """),
        """
        import pytest
        import requests
        import responses
        from pydantic import BaseModel


        class Order(BaseModel):
            id: int
            status: str
            total: float


        class OrdersPage(BaseModel):
            items: list[Order]
            total: int


        def get_orders(status):
            r = requests.get("https://api.test/orders", params={"status": status}, timeout=5)
            r.raise_for_status()
            return r.json()
        """,
        """
        def test_written():
            code, res = run_pytest()
            assert res == {"test_orders_contract": "passed", "test_filter_param": "passed", "test_server_error": "passed"}, res

        def test_catches_bugs():
            import requests as rq
            def no_param(status):
                r = rq.get("https://api.test/orders", timeout=5)
                r.raise_for_status()
                return r.json()
            def swallow(status):
                r = rq.get("https://api.test/orders", params={"status": status}, timeout=5)
                return r.json() if r.ok else {"items": [], "total": 0}
            def lose_total(status):
                r = rq.get("https://api.test/orders", params={"status": status}, timeout=5)
                r.raise_for_status()
                body = r.json()
                body.pop("total", None)
                return body
            for bug in (no_param, swallow, lose_total):
                code, res = run_pytest(patch={"get_orders": bug})
                assert code == 1, f"Тесты пропустили ошибку ({bug.__name__})"
        """,
        """
        import pytest
        import requests
        import responses
        from pydantic import BaseModel


        class Order(BaseModel):
            id: int
            status: str
            total: float


        class OrdersPage(BaseModel):
            items: list[Order]
            total: int


        def get_orders(status):
            r = requests.get("https://api.test/orders", params={"status": status}, timeout=5)
            r.raise_for_status()
            return r.json()


        URL = "https://api.test/orders"


        @responses.activate
        def test_orders_contract():
            responses.get(URL, json={"items": [{"id": 1, "status": "new", "total": 100}], "total": 1})
            page = OrdersPage.model_validate(get_orders("new"))
            assert page.total == 1 and page.items[0].status == "new"


        @responses.activate
        def test_filter_param():
            responses.get(URL, json={"items": [], "total": 0})
            get_orders("paid")
            assert responses.calls[0].request.url.endswith("?status=paid")


        @responses.activate
        def test_server_error():
            responses.get(URL, status=500)
            with pytest.raises(requests.HTTPError):
                get_orders("new")
        """, xp=30),
),
)
