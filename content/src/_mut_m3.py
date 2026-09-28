"""Тема «Изменяемые и неизменяемые», модуль 3 «Практика» — задания. Теория — в _mut_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "mut"

m3 = module(f"{P}-m3", "Практика", "🛡️", "Изменение во время перебора, неизменяемые структуры, изменяемость в классах, данные в тестах",

lesson(f"{P}-iterate", "Изменение коллекции во время перебора",
    out(f"{P}-iterate-e1", "Что выведет программа? Удаление при переборе.", """
        nums = [1, 2, 2, 3, 2, 4]
        for n in nums:
            if n == 2:
                nums.remove(n)
        print(nums)
        """, hint="После удаления элементы сдвигаются, и цикл перескакивает через следующий."),
    out(f"{P}-iterate-e2", "Что выведет программа? Словарь во время перебора.", """
        d = {"a": 1, "b": 2}
        try:
            for k in d:
                d[k + "!"] = 0
        except RuntimeError as e:
            print(e)
        for k in list(d):
            if d[k] == 0:
                del d[k]
        print(d)
        """, hint="list(d) — копия ключей, по ней перебирать безопасно."),
    out(f"{P}-iterate-e3", "Что выведет программа? Правильные способы.", """
        nums = [1, 2, 2, 3, 2, 4]
        print([n for n in nums if n != 2])

        for n in nums[:]:
            if n == 2:
                nums.remove(n)
        print(nums)
        """),
    cod(f"{P}-iterate-e4", t("""
        Функция `remove_negatives` из заготовки удаляет элементы во время перебора и пропускает некоторые из них. Исправь: удалить **все** отрицательные числа из переданного списка **на месте**.
        """),
        """
        def remove_negatives(nums):
            for n in nums:
                if n < 0:
                    nums.remove(n)
        """,
        """
        def test_values():
            x = [-1, -2, 3, -4, -5, 6]
            ref = x
            remove_negatives(x)
            assert x == [3, 6] and x is ref, x
        """,
        """
        def remove_negatives(nums):
            nums[:] = [n for n in nums if n >= 0]
        """),
    cod(f"{P}-iterate-e5", t("""
        Напиши функцию `drop_empty(d)` — удалить из словаря **на месте** все ключи, у которых значение пустое (`""`, `None`, `[]`, `{}`). Вернуть список удалённых ключей.
        """),
        """
        def drop_empty(d):
            pass
        """,
        """
        def test_values():
            d = {"a": 1, "b": "", "c": None, "d": [], "e": 0, "f": {}}
            assert drop_empty(d) == ["b", "c", "d", "f"] and d == {"a": 1, "e": 0}, d
        """,
        """
        def drop_empty(d):
            removed = [k for k, v in d.items() if v in ("", None) or v == [] or v == {}]
            for k in removed:
                del d[k]
            return removed
        """, hint="0 — не пустое значение, его оставляем."),
    cod(f"{P}-iterate-e6", t("""
        Напиши функцию `expand(items)` — **на месте** после каждого числа больше 10 вставить его половину (целочисленно). Перебирай по копии или с индексами, чтобы не зациклиться.

        ```
        expand([4, 20, 7, 30])   # список становится [4, 20, 10, 7, 30, 15]
        ```
        """),
        """
        def expand(items):
            pass
        """,
        """
        def test_values():
            x = [4, 20, 7, 30]
            expand(x)
            assert x == [4, 20, 10, 7, 30, 15], x
        """,
        """
        def expand(items):
            result = []
            for x in items:
                result.append(x)
                if x > 10:
                    result.append(x // 2)
            items[:] = result
        """),
    cod(f"{P}-iterate-e7", t("""
        Напиши функцию `rename_keys(d, mapping)` — **на месте** переименовать ключи словаря по словарю `mapping` («старое → новое»). Ключи, которых нет в `mapping`, оставить.
        """),
        """
        def rename_keys(d, mapping):
            pass
        """,
        """
        def test_values():
            d = {"user_name": "Аня", "age": 30}
            ref = d
            rename_keys(d, {"user_name": "name", "missing": "x"})
            assert d == {"age": 30, "name": "Аня"} and d is ref, d
        """,
        """
        def rename_keys(d, mapping):
            for old in list(d):
                if old in mapping:
                    d[mapping[old]] = d.pop(old)
        """),
    cod(f"{P}-iterate-e8", t("""
        Напиши функцию `process_queue(queue, handler)` — обработать очередь задач (список): брать задачи **с начала**, вызывать `handler(task)`; handler может вернуть список новых задач — их добавить в конец. Вернуть список обработанных задач в порядке обработки. Очередь в конце пустая.
        """),
        """
        def process_queue(queue, handler):
            pass
        """,
        """
        def test_values():
            q = ["a", "b"]
            def h(task):
                return ["a1", "a2"] if task == "a" else None
            assert process_queue(q, h) == ["a", "b", "a1", "a2"] and q == [], q
        """,
        """
        def process_queue(queue, handler):
            done = []
            while queue:
                task = queue.pop(0)
                done.append(task)
                new = handler(task)
                if new:
                    queue.extend(new)
            return done
        """, hint="while queue и pop(0) — безопасно: мы не перебираем список for-ом.", xp=20),
),

lesson(f"{P}-frozen", "Неизменяемые структуры",
    out(f"{P}-frozen-e1", "Что выведет программа? Кортеж и frozenset.", """
        point = (3, 4)
        try:
            point[0] = 10
        except TypeError as e:
            print(e)
        roles = frozenset({"read", "write"})
        try:
            roles.add("admin")
        except AttributeError as e:
            print(e)
        print("read" in roles)
        """),
    out(f"{P}-frozen-e2", "Что выведет программа? Словарь только для чтения.", """
        from types import MappingProxyType

        _settings = {"url": "prod", "timeout": 5}
        SETTINGS = MappingProxyType(_settings)
        print(SETTINGS["url"])
        try:
            SETTINGS["url"] = "test"
        except TypeError as e:
            print(e)
        _settings["timeout"] = 10
        print(SETTINGS["timeout"])
        """, hint="MappingProxyType — «окно» в словарь без права записи. Изменения оригинала в нём видны."),
    out(f"{P}-frozen-e3", "Что выведет программа? namedtuple и frozen dataclass.", """
        from collections import namedtuple
        from dataclasses import dataclass, replace

        Point = namedtuple("Point", "x y")
        p = Point(1, 2)
        print(p, p.x, p._replace(x=10))

        @dataclass(frozen=True)
        class User:
            name: str
            age: int

        u = User("Аня", 30)
        try:
            u.age = 31
        except Exception as e:
            print(type(e).__name__)
        print(replace(u, age=31), u)
        """),
    cod(f"{P}-frozen-e4", t("""
        Напиши функцию `freeze_config(config)` — вернуть «замороженную» версию словаря конфигурации через `types.MappingProxyType` **над копией**, чтобы ни запись через результат, ни изменение исходного словаря не влияли на результат.
        """),
        """
        from types import MappingProxyType


        def freeze_config(config):
            pass
        """,
        """
        def test_values():
            src = {"url": "prod"}
            f = freeze_config(src)
            src["url"] = "hacked"
            assert f["url"] == "prod", "Результат не должен зависеть от исходного словаря"
            try:
                f["url"] = "x"
            except TypeError:
                return
            assert False, "Запись должна быть запрещена"
        """,
        """
        from types import MappingProxyType


        def freeze_config(config):
            return MappingProxyType(dict(config))
        """),
    cod(f"{P}-frozen-e5", t("""
        Опиши неизменяемый класс `Money` через `@dataclass(frozen=True)` с полями `amount: int` и `currency: str` и методом `add(other)` — возвращает **новый** `Money` с суммой (валюты должны совпадать, иначе `ValueError`).
        """),
        """
        from dataclasses import dataclass
        """,
        """
        def test_values():
            a = Money(100, "RUB")
            b = a.add(Money(50, "RUB"))
            assert b == Money(150, "RUB") and a == Money(100, "RUB"), "Сложение"
            try:
                a.amount = 1
            except AttributeError:
                pass
            else:
                assert False, "Money должен быть неизменяемым"
            try:
                a.add(Money(1, "USD"))
            except ValueError:
                return
            assert False, "Нужен ValueError"
        """,
        """
        from dataclasses import dataclass


        @dataclass(frozen=True)
        class Money:
            amount: int
            currency: str

            def add(self, other):
                if self.currency != other.currency:
                    raise ValueError("разные валюты")
                return Money(self.amount + other.amount, self.currency)
        """),
    cod(f"{P}-frozen-e6", t("""
        Напиши функцию `to_points(pairs)` — превратить список пар `[x, y]` в список `namedtuple` `Point(x, y)`. Объяви `Point` на уровне модуля.
        """),
        """
        from collections import namedtuple
        """,
        """
        def test_values():
            ps = to_points([[1, 2], [3, 4]])
            assert ps == [(1, 2), (3, 4)] and ps[1].y == 4 and type(ps[0]).__name__ == "Point", ps
            assert len({ps[0], Point(1, 2)}) == 1, "Point хешируемый"
        """,
        """
        from collections import namedtuple

        Point = namedtuple("Point", "x y")


        def to_points(pairs):
            return [Point(x, y) for x, y in pairs]
        """),
    cod(f"{P}-frozen-e7", t("""
        Напиши функцию `readonly_roles(roles_by_user)` — `roles_by_user` — словарь «пользователь → список ролей». Вернуть новый словарь, где роли — `frozenset`, чтобы их нельзя было случайно изменить.
        """),
        """
        def readonly_roles(roles_by_user):
            pass
        """,
        """
        def test_values():
            r = readonly_roles({"аня": ["read", "write", "read"], "боря": []})
            assert r == {"аня": frozenset({"read", "write"}), "боря": frozenset()} and all(type(v) is frozenset for v in r.values()), r
        """,
        """
        def readonly_roles(roles_by_user):
            return {user: frozenset(roles) for user, roles in roles_by_user.items()}
        """),
    cod(f"{P}-frozen-e8", t("""
        Создай неизменяемый класс `Version` через `@dataclass(frozen=True, order=True)` с полями `major`, `minor`, `patch` (int), классовым методом `parse(text)` (`"1.10.2"` → `Version(1, 10, 2)`) и методом `bump_minor()` — новая версия с `minor + 1` и `patch = 0`.
        """),
        """
        from dataclasses import dataclass, replace
        """,
        """
        def test_values():
            v = Version.parse("1.10.2")
            assert v == Version(1, 10, 2) and v.bump_minor() == Version(1, 11, 0) and v == Version(1, 10, 2), "parse и bump"
            assert Version.parse("1.10.0") > Version.parse("1.9.9") and len({v, Version(1, 10, 2)}) == 1, "Сравнение и хеш"
        """,
        """
        from dataclasses import dataclass, replace


        @dataclass(frozen=True, order=True)
        class Version:
            major: int
            minor: int
            patch: int

            @classmethod
            def parse(cls, text):
                return cls(*(int(p) for p in text.split(".")))

            def bump_minor(self):
                return replace(self, minor=self.minor + 1, patch=0)
        """, xp=20),
),

lesson(f"{P}-classes", "Изменяемость и классы",
    out(f"{P}-classes-e1", "Что выведет программа? Общий список в атрибуте класса.", """
        class Cart:
            items = []

            def add(self, x):
                self.items.append(x)

        a, b = Cart(), Cart()
        a.add("чай")
        print(b.items, a.items is b.items)
        """, hint="Атрибут класса — один на все объекты."),
    out(f"{P}-classes-e2", "Что выведет программа? Утечка внутреннего списка.", """
        class Team:
            def __init__(self):
                self._members = []

            def add(self, name):
                self._members.append(name)

            def members(self):
                return self._members

            def members_copy(self):
                return list(self._members)

        t = Team()
        t.add("Аня")
        t.members().append("Взломщик")
        t.members_copy().append("Нет")
        print(t._members)
        """, hint="Возвращая внутренний список, мы даём внешнему коду менять объект."),
    out(f"{P}-classes-e3", "Что выведет программа? Объект в двух списках.", """
        class User:
            def __init__(self, name):
                self.name = name

        u = User("аня")
        admins = [u]
        everyone = [u, User("боря")]
        admins[0].name = "АНЯ"
        print([x.name for x in everyone])
        """),
    cod(f"{P}-classes-e4", t("""
        Исправь класс `Cart` из заготовки: товары всех корзин попадают в общий список.
        """),
        """
        class Cart:
            items = []

            def add(self, item):
                self.items.append(item)
        """,
        """
        def test_values():
            a, b = Cart(), Cart()
            a.add("чай")
            assert a.items == ["чай"] and b.items == [], (a.items, b.items)
        """,
        """
        class Cart:
            def __init__(self):
                self.items = []

            def add(self, item):
                self.items.append(item)
        """),
    cod(f"{P}-classes-e5", t("""
        Создай класс `Team` с методами `add(name)` и `members()`. `members()` должен возвращать **кортеж** участников, чтобы внешний код не мог изменить состав команды.
        """),
        """
        class Team:
            pass
        """,
        """
        def test_values():
            t = Team()
            t.add("Аня")
            m = t.members()
            assert m == ("Аня",) and isinstance(m, tuple), m
            t.add("Боря")
            assert t.members() == ("Аня", "Боря") and m == ("Аня",), "Снимок не меняется"
        """,
        """
        class Team:
            def __init__(self):
                self._members = []

            def add(self, name):
                self._members.append(name)

            def members(self):
                return tuple(self._members)
        """),
    cod(f"{P}-classes-e6", t("""
        Создай класс `Order(items)`: в конструкторе сохрани **копию** переданного списка (чтобы изменения снаружи не влияли на заказ). Метод `total()` — сумма цен (элементы — числа).
        """),
        """
        class Order:
            pass
        """,
        """
        def test_values():
            prices = [100, 200]
            o = Order(prices)
            prices.append(1000)
            assert o.total() == 300, o.total()
        """,
        """
        class Order:
            def __init__(self, items):
                self.items = list(items)

            def total(self):
                return sum(self.items)
        """),
    cod(f"{P}-classes-e7", t("""
        Создай класс `Settings(values)` — неизменяемый объект настроек: хранит копию словаря, метод `get(key, default=None)`, метод `with_value(key, value)` возвращает **новый** `Settings`. Прямого доступа к словарю на запись не давай: свойство `values` возвращает `MappingProxyType`.
        """),
        """
        from types import MappingProxyType


        class Settings:
            pass
        """,
        """
        def test_values():
            s = Settings({"url": "prod"})
            s2 = s.with_value("url", "test")
            assert s.get("url") == "prod" and s2.get("url") == "test" and s.get("x", 1) == 1, "get и with_value"
            try:
                s.values["url"] = "hack"
            except TypeError:
                pass
            else:
                assert False, "values только для чтения"
        """,
        """
        from types import MappingProxyType


        class Settings:
            def __init__(self, values):
                self._values = dict(values)

            @property
            def values(self):
                return MappingProxyType(self._values)

            def get(self, key, default=None):
                return self._values.get(key, default)

            def with_value(self, key, value):
                return Settings({**self._values, key: value})
        """),
    cod(f"{P}-classes-e8", t("""
        Создай класс `History`, который хранит снимки состояния: `save(state)` сохраняет **глубокую копию** переданной структуры, `get(i)` возвращает **глубокую копию** i-го снимка (чтобы ни сохранённое, ни выданное нельзя было испортить снаружи), `count()` — количество снимков.
        """),
        """
        import copy


        class History:
            pass
        """,
        """
        def test_values():
            h = History()
            state = {"cart": ["чай"]}
            h.save(state)
            state["cart"].append("кофе")
            h.save(state)
            got = h.get(0)
            got["cart"].append("взлом")
            assert h.get(0) == {"cart": ["чай"]} and h.get(1) == {"cart": ["чай", "кофе"]} and h.count() == 2, h.get(0)
        """,
        """
        import copy


        class History:
            def __init__(self):
                self._snapshots = []

            def save(self, state):
                self._snapshots.append(copy.deepcopy(state))

            def get(self, i):
                return copy.deepcopy(self._snapshots[i])

            def count(self):
                return len(self._snapshots)
        """, xp=20),
),

lesson(f"{P}-tests", "Практика: данные в тестах",
    out(f"{P}-tests-e1", "Что выведет программа? Данные протекают между тестами.", """
        USER = {"name": "test", "roles": ["reader"]}

        def test_admin():
            user = USER
            user["roles"].append("admin")
            return user["roles"]

        def test_reader():
            return USER["roles"] == ["reader"]

        print(test_admin())
        print(test_reader())
        """, hint="Первый тест испортил общий эталон, и второй упал бы без вины."),
    out(f"{P}-tests-e2", "Что выведет программа? Фабрика вместо общей переменной.", """
        def make_user(**overrides):
            user = {"name": "test", "roles": ["reader"]}
            user.update(overrides)
            return user

        a = make_user()
        a["roles"].append("admin")
        b = make_user(name="боря")
        print(a)
        print(b)
        """, hint="Каждый вызов создаёт новые словарь и список."),
    out(f"{P}-tests-e3", "Что выведет программа? Проверка, что функция не меняет вход.", """
        import copy

        def top3(scores):
            scores.sort(reverse=True)
            return scores[:3]

        data = [5, 1, 9, 3, 7]
        snapshot = copy.deepcopy(data)
        print(top3(data))
        print("вход не изменён:", data == snapshot)
        """),
    cod(f"{P}-tests-e4", t("""
        Напиши функцию-фабрику `make_order(**overrides)` — каждый вызов возвращает **новый** заказ `{"id": 1, "items": [], "status": "new"}` с применёнными переопределениями. Изменение списка `items` одного заказа не должно влиять на другие.
        """),
        """
        def make_order(**overrides):
            pass
        """,
        """
        def test_values():
            a = make_order()
            a["items"].append("чай")
            b = make_order(status="paid")
            assert b == {"id": 1, "items": [], "status": "paid"} and a["items"] == ["чай"], b
        """,
        """
        def make_order(**overrides):
            order = {"id": 1, "items": [], "status": "new"}
            order.update(overrides)
            return order
        """),
    cod(f"{P}-tests-e5", t("""
        Напиши функцию `assert_not_mutated(func, *args)` — вызвать `func(*args)` и проверить, что ни один аргумент не изменился (сравни с глубокими копиями до вызова). Если изменился — `AssertionError(f"аргумент {номер} изменён")` (номер с 0). Иначе вернуть результат.
        """),
        """
        import copy


        def assert_not_mutated(func, *args):
            pass
        """,
        """
        def test_values():
            assert assert_not_mutated(sorted, [3, 1]) == [1, 3], "sorted не меняет"
            def bad(a, b):
                b.append(1)
            try:
                assert_not_mutated(bad, [1], [2])
            except AssertionError as e:
                assert str(e) == "аргумент 1 изменён", str(e)
                return
            assert False, "Нужен AssertionError"
        """,
        """
        import copy


        def assert_not_mutated(func, *args):
            before = copy.deepcopy(args)
            result = func(*args)
            for i, (old, new) in enumerate(zip(before, args)):
                if old != new:
                    raise AssertionError(f"аргумент {i} изменён")
            return result
        """),
    cod(f"{P}-tests-e6", t("""
        Напиши функцию `load_fixture(name)` — возвращает **глубокую копию** эталонных данных из словаря `FIXTURES` (уже есть в заготовке). Тесты могут менять полученные данные, но эталон — никогда.
        """),
        """
        import copy

        FIXTURES = {
            "admin": {"name": "admin", "roles": ["read", "write"]},
            "cart": {"items": [{"sku": "A1", "qty": 1}]},
        }


        def load_fixture(name):
            pass
        """,
        """
        def test_values():
            c = load_fixture("cart")
            c["items"][0]["qty"] = 99
            c["items"].append({"sku": "B2", "qty": 1})
            assert load_fixture("cart") == {"items": [{"sku": "A1", "qty": 1}]}, load_fixture("cart")
        """,
        """
        import copy

        FIXTURES = {
            "admin": {"name": "admin", "roles": ["read", "write"]},
            "cart": {"items": [{"sku": "A1", "qty": 1}]},
        }


        def load_fixture(name):
            return copy.deepcopy(FIXTURES[name])
        """),
    cod(f"{P}-tests-e7", t("""
        Напиши функцию `diff(before, after)` — сравнить два словаря (снимки состояния до и после действия) и вернуть словарь изменений: `{"added": [...], "removed": [...], "changed": [...]}` — отсортированные списки ключей.
        """),
        """
        def diff(before, after):
            pass
        """,
        """
        def test_values():
            r = diff({"a": 1, "b": 2, "c": [1]}, {"a": 1, "c": [1, 2], "d": 4})
            assert r == {"added": ["d"], "removed": ["b"], "changed": ["c"]}, r
        """,
        """
        def diff(before, after):
            return {
                "added": sorted(after.keys() - before.keys()),
                "removed": sorted(before.keys() - after.keys()),
                "changed": sorted(k for k in before.keys() & after.keys() if before[k] != after[k]),
            }
        """),
    cod(f"{P}-tests-e8", t("""
        Функция `apply_patch(resource, patch)` из заготовки должна вести себя как PATCH-запрос: вернуть **новый** ресурс, где поля из `patch` заменены (вложенные словари — объединяются рекурсивно). Сейчас она портит исходный ресурс. Перепиши её так, чтобы `resource` не менялся ни на каком уровне.
        """),
        """
        def apply_patch(resource, patch):
            for key, value in patch.items():
                if isinstance(value, dict) and isinstance(resource.get(key), dict):
                    apply_patch(resource[key], value)
                else:
                    resource[key] = value
            return resource
        """,
        """
        def test_values():
            res = {"name": "Аня", "address": {"city": "Москва", "zip": "101"}, "tags": ["qa"]}
            r = apply_patch(res, {"address": {"city": "Казань"}, "age": 30})
            assert r == {"name": "Аня", "address": {"city": "Казань", "zip": "101"}, "tags": ["qa"], "age": 30}, r
            assert res == {"name": "Аня", "address": {"city": "Москва", "zip": "101"}, "tags": ["qa"]}, "Исходный ресурс изменился"
            r["tags"].append("x")
            assert res["tags"] == ["qa"], "Результат не должен делить списки с исходным"
        """,
        """
        import copy


        def apply_patch(resource, patch):
            result = copy.deepcopy(resource)
            for key, value in patch.items():
                if isinstance(value, dict) and isinstance(result.get(key), dict):
                    result[key] = apply_patch(result[key], value)
                else:
                    result[key] = copy.deepcopy(value)
            return result
        """, xp=25),
),
)
