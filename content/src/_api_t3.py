"""Теория модуля «Валидация: Pydantic и JSON Schema» темы «Тестирование API».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- api-pydantic ----------
'api-pydantic': dict(
    full=t(r'''
## Зачем это нужно

Проверять каждое поле ответа отдельным `assert` долго и легко что-то пропустить. **Pydantic** позволяет один раз описать структуру данных классом — **моделью** — и проверять ответ одной строкой: все поля, типы, вложенность. Если что-то не так, ошибка точно скажет, какое поле и почему. Pydantic — стандарт де-факто в современных API-тестах на Python (и в FastAPI).

## Модель

```python
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    active: bool = True


u = User.model_validate({"id": "7", "name": "Аня"})
print(u.id, type(u.id).__name__, u.active)
print(u.model_dump())
```

- Класс наследует `BaseModel`; поля описываются аннотациями типов. Поле со значением по умолчанию — необязательное.
- `Model.model_validate(словарь)` — создать объект с проверкой. `User(id=7, name="Аня")` — то же через аргументы.
- Pydantic **приводит** совместимые значения: строка `"7"` станет числом `7`. Несовместимые (`"abc"` для `int`) — ошибка.
- `obj.model_dump()` — обратно в словарь; `model_dump_json()` — в JSON-строку.
- Вывод: `7 int True`, `{'id': 7, 'name': 'Аня', 'active': True}`.

## Ошибки валидации

```python
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
```

- `ValidationError` собирает **все** ошибки сразу, а не только первую.
- `e.errors()` — список словарей: `loc` — путь к полю, `type` — вид ошибки, `msg` — описание.
- Вывод: `2`, `('id',) int_parsing`, `('name',) missing`.

## Строгость

```py
from pydantic import ConfigDict


class Order(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: int
    status: str
```

- По умолчанию лишние поля игнорируются. `extra="forbid"` делает их ошибкой: тест заметит утечку внутренних полей в ответе.
- `strict=True` в конфиге запретит приведение типов (`"7"` для `int` станет ошибкой) — для строгих контрактов.

## В тесте

```py
def test_user_contract(client):
    resp = client.get("/users/1")
    assert resp.status_code == 200
    user = User.model_validate(resp.json())   # упадёт с понятной ошибкой
    assert user.name == "Аня"
```

## Итог

- `class M(BaseModel)` + аннотации; значение по умолчанию → необязательное поле.
- `M.model_validate(dict)` — проверка; `obj.model_dump()` — словарь.
- `ValidationError.errors()` — все ошибки с путями.
- `extra="forbid"` — запрет лишних полей; `strict` — без приведения типов.
'''),
    short=t(r'''
```py
from pydantic import BaseModel, ValidationError, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: int
    name: str
    email: str | None = None      # необязательное

user = User.model_validate(resp.json())
user.model_dump(exclude_none=True)
except ValidationError as e: e.errors()   # loc, type, msg
```
'''),
    quiz=[
        q('Что сделает Pydantic со значением `"7"` для поля `id: int`?',
            ['Ошибка', 'Приведёт к 7', 'Оставит строкой', 'Заменит на None'],
            1, 'В нестрогом режиме приводит совместимые значения.'),
        q('Как запретить лишние поля в ответе?',
            ['strict=True', 'model_config = ConfigDict(extra="forbid")', 'Optional', 'Field(...)'],
            1, 'По умолчанию лишние игнорируются.'),
        q('Сколько ошибок сообщает ValidationError?',
            ['Только первую', 'Все найденные', 'Последнюю', 'Не больше трёх'],
            1, 'e.errors() — полный список.'),
    ],
),

# ---------- api-pydantic-adv ----------
'api-pydantic-adv': dict(
    full=t(r'''
## Зачем это нужно

Типа поля мало: цена должна быть положительной, email — похожим на email, статус — одним из допустимых, а API отдаёт `camelCase` вместо привычного `snake_case`. Pydantic умеет всё это описать декларативно.

## Ограничения: Field

```python
from pydantic import BaseModel, Field, ValidationError


class Item(BaseModel):
    title: str = Field(min_length=2, max_length=20)
    qty: int = Field(gt=0, le=100)


for data in [{"title": "чай", "qty": 3}, {"title": "x", "qty": 0}]:
    try:
        print(Item(**data))
    except ValidationError as e:
        print([err["type"] for err in e.errors()])
```

- Числа: `gt`, `ge`, `lt`, `le` (больше, больше или равно, меньше, меньше или равно).
- Строки и списки: `min_length`, `max_length`; строки: `pattern=r"..."` (регулярное выражение).
- Вывод: `title='чай' qty=3`, `['string_too_short', 'greater_than']`.

## Перечисления и Optional

```py
from typing import Literal


class Task(BaseModel):
    status: Literal["new", "in_progress", "done"]
    assignee: str | None = None
```

- `Literal[...]` — только эти значения.
- `X | None = None` — поле может отсутствовать или быть `null`.

## Свой валидатор

```py
from pydantic import field_validator


class Status(BaseModel):
    code: int

    @field_validator("code")
    @classmethod
    def known_code(cls, value):
        if not 100 <= value <= 599:
            raise ValueError("неизвестный HTTP-код")
        return value
```

- Валидатор получает уже приведённое значение; выброшенный `ValueError` станет ошибкой валидации. Вернуть нужно значение (можно изменённое — например, `strip().lower()`).

## Вложенные модели

```py
class Item(BaseModel):
    name: str
    price: float


class Order(BaseModel):
    id: int
    items: list[Item]

    def total(self):
        return sum(i.price for i in self.items)
```

- Поле-модель и списки моделей проверяются рекурсивно; путь к ошибке будет вроде `items.1.price`.
- В модель можно добавлять методы.

## Псевдонимы

```python
from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int = Field(alias="userId")
    first_name: str = Field(alias="firstName")


u = User.model_validate({"userId": 5, "firstName": "Аня"})
print(u.user_id, u.model_dump(by_alias=True))
```

- `alias` — имя поля в JSON. `model_dump(by_alias=True)` — вывести как в API.
- `ConfigDict(populate_by_name=True)` — разрешить создавать и по имени поля.
- `datetime` поле принимает ISO-строки: `"2024-03-08T12:00:00Z"`.
- Вывод: `5 {'userId': 5, 'firstName': 'Аня'}`.

## Итог

- `Field(gt=, ge=, lt=, le=, min_length=, max_length=, pattern=)`.
- `Literal[...]`, `X | None = None`.
- `@field_validator("поле")` + `@classmethod`.
- Вложенные модели, `list[Model]`; `alias` + `by_alias=True`.
'''),
    short=t(r'''
```py
class Item(BaseModel):
    title: str = Field(min_length=2, pattern=r"^\w+$")
    qty: int = Field(gt=0, le=100)
    status: Literal["new", "done"]
    note: str | None = None
    user_id: int = Field(alias="userId")

    @field_validator("title")
    @classmethod
    def clean(cls, v): return v.strip()
# model_config = ConfigDict(populate_by_name=True) · model_dump(by_alias=True)
```
'''),
    quiz=[
        q('Какой параметр Field задаёт «строго больше нуля»?',
            ['ge=0', 'gt=0', 'min=0', 'positive=True'],
            1, 'gt — greater than.'),
        q('Как ограничить поле значениями "new", "done"?',
            ['Enum строкой', 'Literal["new", "done"]', 'Field(values=...)', 'str | None'],
            1, 'Литеральный тип.'),
        q('Что должен вернуть field_validator?',
            ['True', 'Значение поля (возможно изменённое)', 'None', 'Модель'],
            1, 'Ошибка — через raise ValueError.'),
    ],
),

# ---------- api-schema ----------
'api-schema': dict(
    full=t(r'''
## Зачем это нужно

**JSON Schema** — язык описания структуры JSON, не привязанный к Python. Схемы часто выдаёт сам API (в спецификации OpenAPI/Swagger), ими обмениваются команды на разных языках. Библиотека `jsonschema` проверяет ответ по такой схеме.

## Схема и проверка

```python
from jsonschema import validate, ValidationError

schema = {
    "type": "object",
    "required": ["id", "name"],
    "properties": {
        "id": {"type": "integer", "minimum": 1},
        "name": {"type": "string"},
        "role": {"enum": ["admin", "qa", "guest"]},
    },
    "additionalProperties": False,
}
validate({"id": 1, "name": "Аня"}, schema)
print("ok")
try:
    validate({"id": 0, "name": "Аня"}, schema)
except ValidationError as e:
    print(e.message)
```

Основные ключевые слова:

- `type` — `object`, `array`, `string`, `integer`, `number`, `boolean`, `null`.
- `required` — обязательные поля; `properties` — схемы полей.
- `additionalProperties: false` — запрет лишних полей.
- `enum` — список допустимых значений; `minimum`, `maximum`, `minLength`, `pattern`.
- `items` — схема каждого элемента массива.
- `validate` выбрасывает первую найденную ошибку.
- Вывод: `ok`, `0 is less than the minimum of 1`.

## Все ошибки

```python
from jsonschema import Draft202012Validator

schema = {"type": "array", "items": {"type": "object", "required": ["id"]}}
for error in Draft202012Validator(schema).iter_errors([{"id": 1}, {}, {"name": "x"}]):
    print(list(error.path), error.validator)
```

- `iter_errors` — все ошибки; `error.path` — путь к месту, `error.validator` — какое правило нарушено, `error.message` — текст.
- Вывод: `[1] required`, `[2] required`.

## Схема из модели Pydantic

```python
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


print(User.model_json_schema()["required"])
```

- `model_json_schema()` генерирует JSON Schema — удобно отдать другой команде или сравнить с OpenAPI.
- Вывод: `['id', 'name']`.

## Что выбрать

- Тесты на Python со своими моделями — **Pydantic**: удобнее, есть приведение типов и валидаторы.
- Схемы уже есть в OpenAPI или нужны нескольким языкам — **JSON Schema**.

## Итог

- `type`, `required`, `properties`, `additionalProperties`, `enum`, `items`, `minimum`, `pattern`.
- `validate(data, schema)` — первая ошибка; `Draft202012Validator(schema).iter_errors(data)` — все.
- `Model.model_json_schema()` — схема из Pydantic.
'''),
    short=t(r'''
```py
schema = {"type": "object", "required": ["id"], "additionalProperties": False,
          "properties": {"id": {"type": "integer", "minimum": 1},
                         "tags": {"type": "array", "items": {"type": "string"}},
                         "role": {"enum": ["admin", "qa"]}}}
validate(data, schema)                                  # ValidationError
for e in Draft202012Validator(schema).iter_errors(data):
    e.path, e.validator, e.message
User.model_json_schema()
```
'''),
    quiz=[
        q('Как запретить лишние поля в JSON Schema?',
            ['strict: true', '"additionalProperties": false', '"extra": "forbid"', 'required: all'],
            1, 'По умолчанию лишние разрешены.'),
        q('Чем iter_errors отличается от validate?',
            ['Ничем', 'Возвращает все ошибки, а не только первую', 'Работает быстрее', 'Не требует схемы'],
            1, 'validate выбрасывает первую.'),
        q('Как получить JSON Schema из модели Pydantic?',
            ['User.schema_json()', 'User.model_json_schema()', 'json.dumps(User)', 'Нельзя'],
            1, 'Метод v2.'),
    ],
),

# ---------- api-practice ----------
'api-practice': dict(
    full=t(r'''
## Зачем это нужно

Соберём всё в одну картину: как выглядит набор API-тестов в реальном проекте — клиент, фикстуры, модели, позитивные и негативные сценарии, проверка контракта и времени ответа.

## Структура проекта

```bash
api-tests/
  pyproject.toml
  src/api/client.py        # ApiClient, UsersApi, OrdersApi
  src/api/models.py        # модели Pydantic
  tests/conftest.py        # фикстуры: base_url, client, созданные данные
  tests/test_users.py
  tests/test_orders.py
```

## Контрактный тест

```py
@responses.activate
def test_get_user_contract():
    responses.get(f"{BASE}/users/1", json={"id": 1, "name": "Аня", "email": "anna@x.ru"})
    user = User.model_validate(api_get_user(1))
    assert user.name == "Аня"
```

- **Контракт** — договорённость о структуре ответа. Контрактный тест падает, если поле пропало, сменило тип или появилось лишнее — до того, как сломается фронтенд.

## Негативные проверки параметризацией

```py
@pytest.mark.parametrize("payload, expected", [
    ({}, 422),
    ({"name": ""}, 422),
    ({"name": "Аня", "age": -1}, 422),
    ({"name": "Аня"}, 201),
])
def test_create(payload, expected, users):
    assert users.create(payload).status_code == expected
```

## CRUD-сценарий

```py
def test_crud(users):
    created = users.create({"name": "Аня"})
    assert created.status_code == 201
    user_id = created.json()["id"]
    assert users.get(user_id).json()["name"] == "Аня"
    assert users.delete(user_id).status_code == 204
    assert users.get(user_id).status_code == 404
```

## Время ответа

```py
def test_sla(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.elapsed.total_seconds() < 0.5
```

- Простая проверка производительности. Для нагрузочного тестирования есть отдельные инструменты (Locust, k6).

## Изоляция данных

- Каждый тест создаёт свои данные (уникальные имена, например, с `uuid`) и удаляет их в teardown фикстуры.
- Не полагайся на данные, созданные другими тестами, — иначе тесты не запустить параллельно.

## Инструменты вокруг

- **OpenAPI / Swagger** — спецификация API: из неё берут эндпоинты и схемы.
- **HTTPie**, **curl**, **Postman** — ручная проверка и воспроизведение.
- Allure — шаги с запросами и ответами во вложениях.

## Итог

- Клиент + модели + фикстуры + тесты по файлам.
- Контракт (Pydantic), негативы (parametrize), CRUD, время ответа.
- Свои данные в каждом тесте, уборка в teardown.
'''),
    short=t(r'''
```py
user = User.model_validate(resp.json())                  # контракт
@pytest.mark.parametrize("payload, code", [({}, 422), ({"name": "A"}, 201)])
# CRUD: create 201 → get 200 → delete 204 → get 404
assert resp.elapsed.total_seconds() < 0.5                # SLA
# свои данные в тесте, удаление в teardown фикстуры
```
'''),
    quiz=[
        q('Что проверяет контрактный тест?',
            ['Нагрузку', 'Структуру ответа: поля, типы, отсутствие лишнего', 'Дизайн', 'Логи сервера'],
            1, 'Договорённость о формате.'),
        q('Почему тест должен создавать свои данные?',
            ['Так быстрее', 'Чтобы не зависеть от других тестов и запускаться параллельно', 'Чтобы было больше данных', 'Так требует REST'],
            1, 'Изоляция.'),
        q('Как в requests узнать время ответа?',
            ['r.time', 'r.elapsed', 'r.duration', 'r.ms'],
            1, 'timedelta.'),
    ],
),

}
