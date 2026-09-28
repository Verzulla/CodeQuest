"""Тема «Контекстные менеджеры», модуль 3 «Практика» — задания. Теория — в _ctx_t3.py."""
from ._lib import cod, lesson, module, out, t

P = "ctx"

m3 = module(f"{P}-m3", "Практика", "🧪", "Временная подмена состояния, замеры и шаги, менеджеры в тестах, ресурсы тестового окружения",

lesson(f"{P}-state", "Временно изменить и вернуть",
    out(f"{P}-state-e1", "Что выведет программа? Временная настройка.", """
        from contextlib import contextmanager

        config = {"debug": False, "url": "prod"}

        @contextmanager
        def override(settings, **changes):
            old = dict(settings)
            settings.update(changes)
            try:
                yield settings
            finally:
                settings.clear()
                settings.update(old)

        with override(config, debug=True, url="test"):
            print(config)
        print(config)
        """),
    out(f"{P}-state-e2", "Что выведет программа? Подмена атрибута.", """
        from contextlib import contextmanager

        class Api:
            base_url = "https://prod.example"

        @contextmanager
        def patched(obj, name, value):
            old = getattr(obj, name)
            setattr(obj, name, value)
            try:
                yield
            finally:
                setattr(obj, name, old)

        with patched(Api, "base_url", "http://localhost:8000"):
            print(Api.base_url)
        print(Api.base_url)
        """, hint="getattr/setattr читают и пишут атрибут по имени-строке. Так устроен unittest.mock.patch."),
    out(f"{P}-state-e3", "Что выведет программа? Переменные окружения.", """
        import os
        from contextlib import contextmanager

        @contextmanager
        def env(**values):
            old = {k: os.environ.get(k) for k in values}
            os.environ.update(values)
            try:
                yield
            finally:
                for k, v in old.items():
                    if v is None:
                        del os.environ[k]
                    else:
                        os.environ[k] = v

        with env(STAND="stage"):
            print(os.environ["STAND"])
        print(os.environ.get("STAND"))
        """),
    cod(f"{P}-state-e4", t("""
        Напиши через `@contextmanager` функцию `temp_value(data, key, value)`: временно установить `data[key] = value`, а после блока вернуть старое значение. Если ключа раньше не было — удалить его. Восстановление — даже при ошибке.
        """),
        """
        from contextlib import contextmanager
        """,
        """
        def test_values():
            d = {"a": 1}
            with temp_value(d, "a", 99):
                assert d == {"a": 99}, "Внутри"
            with temp_value(d, "b", 2):
                assert d == {"a": 1, "b": 2}, "Новый ключ"
            assert d == {"a": 1}, f"После: {d}"
            try:
                with temp_value(d, "a", 5):
                    raise ValueError
            except ValueError:
                pass
            assert d == {"a": 1}, "Восстановление после ошибки"
        """,
        """
        from contextlib import contextmanager

        _MISSING = object()


        @contextmanager
        def temp_value(data, key, value):
            old = data.get(key, _MISSING)
            data[key] = value
            try:
                yield data
            finally:
                if old is _MISSING:
                    del data[key]
                else:
                    data[key] = old
        """, hint="Уникальный объект-маркер отличает «ключа не было» от «значение было None»."),
    cod(f"{P}-state-e5", t("""
        Напиши через `@contextmanager` функцию `patch_attr(obj, name, value)` — временно заменить атрибут объекта (`setattr`) и вернуть старое значение после блока, даже при ошибке. В `as` отдать **старое** значение.
        """),
        """
        from contextlib import contextmanager
        """,
        """
        def test_values():
            class Settings:
                timeout = 30
            with patch_attr(Settings, "timeout", 1) as old:
                assert Settings.timeout == 1 and old == 30, "Внутри"
            assert Settings.timeout == 30, "После"
            try:
                with patch_attr(Settings, "timeout", 2):
                    raise KeyError
            except KeyError:
                pass
            assert Settings.timeout == 30, "После ошибки"
        """,
        """
        from contextlib import contextmanager


        @contextmanager
        def patch_attr(obj, name, value):
            old = getattr(obj, name)
            setattr(obj, name, value)
            try:
                yield old
            finally:
                setattr(obj, name, old)
        """),
    cod(f"{P}-state-e6", t("""
        Напиши через `@contextmanager` функцию `fake_function(module_dict, name, replacement)` — временно подменить функцию в словаре глобальных имён (например, `globals()`), чтобы код, который её вызывает, получил подделку. После блока вернуть оригинал.

        В тесте подменят функцию `now()` из заготовки — функция `greeting()` должна увидеть подделку.
        """),
        """
        from contextlib import contextmanager


        def now():
            import datetime
            return datetime.datetime.now().hour


        def greeting():
            return "утро" if now() < 12 else "день"
        """,
        """
        def test_values():
            g = greeting.__globals__
            with fake_function(g, "now", lambda: 9):
                assert greeting() == "утро", "Подделка 9 часов"
            with fake_function(g, "now", lambda: 15):
                assert greeting() == "день", "Подделка 15 часов"
            assert g["now"].__name__ == "now", "Оригинал восстановлен"
        """,
        """
        from contextlib import contextmanager


        def now():
            import datetime
            return datetime.datetime.now().hour


        def greeting():
            return "утро" if now() < 12 else "день"


        @contextmanager
        def fake_function(module_dict, name, replacement):
            original = module_dict[name]
            module_dict[name] = replacement
            try:
                yield
            finally:
                module_dict[name] = original
        """),
    cod(f"{P}-state-e7", t("""
        Напиши класс-менеджер `Frozen(items)` для списка: внутри блока список можно менять как угодно, а после выхода он **возвращается** к исходному содержимому (тот же объект).
        """),
        """
        class Frozen:
            pass
        """,
        """
        def test_values():
            data = [1, 2, 3]
            with Frozen(data) as d:
                d.append(4)
                d.remove(1)
                assert d is data and data == [2, 3, 4], "Внутри меняется"
            assert data == [1, 2, 3], f"После: {data}"
        """,
        """
        class Frozen:
            def __init__(self, items):
                self.items = items

            def __enter__(self):
                self.saved = list(self.items)
                return self.items

            def __exit__(self, exc_type, exc, tb):
                self.items[:] = self.saved
                return False
        """, hint="items[:] = saved заменяет содержимое того же списка."),
    cod(f"{P}-state-e8", t("""
        Напиши через `@contextmanager` функцию `env_vars(**values)` — временно установить переменные окружения (`os.environ`) и после блока восстановить: прежние значения вернуть, новые переменные удалить.
        """),
        """
        import os
        from contextlib import contextmanager
        """,
        """
        import os

        def test_values():
            os.environ["CQ_A"] = "old"
            os.environ.pop("CQ_B", None)
            with env_vars(CQ_A="new", CQ_B="added"):
                assert os.environ["CQ_A"] == "new" and os.environ["CQ_B"] == "added", "Внутри"
            assert os.environ["CQ_A"] == "old" and "CQ_B" not in os.environ, "После"
        """,
        """
        import os
        from contextlib import contextmanager


        @contextmanager
        def env_vars(**values):
            old = {key: os.environ.get(key) for key in values}
            os.environ.update(values)
            try:
                yield
            finally:
                for key, value in old.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value
        """, xp=20),
),

lesson(f"{P}-timing", "Замеры времени и шаги",
    out(f"{P}-timing-e1", "Что выведет программа? Секундомер.", """
        import time
        from contextlib import contextmanager

        @contextmanager
        def stopwatch(results, name):
            start = time.perf_counter()
            try:
                yield
            finally:
                results[name] = time.perf_counter() - start

        results = {}
        with stopwatch(results, "пауза"):
            time.sleep(0.05)
        print(list(results), 0.04 < results["пауза"] < 1)
        """),
    out(f"{P}-timing-e2", "Что выведет программа? Класс-таймер.", """
        import time

        class Timer:
            def __enter__(self):
                self.start = time.perf_counter()
                self.elapsed = None
                return self

            def __exit__(self, *args):
                self.elapsed = time.perf_counter() - self.start
                return False

        with Timer() as t:
            print("внутри:", t.elapsed)
            time.sleep(0.02)
        print("после:", t.elapsed > 0.01)
        """, hint="Объект из as доступен и после блока."),
    out(f"{P}-timing-e3", "Что выведет программа? Вложенные шаги.", """
        from contextlib import contextmanager

        depth = 0

        @contextmanager
        def step(name):
            global depth
            print("  " * depth + "▶ " + name)
            depth += 1
            try:
                yield
            finally:
                depth -= 1

        with step("оформление заказа"):
            with step("корзина"):
                pass
            with step("оплата"):
                with step("ввод карты"):
                    pass
        """, hint="Так выглядят шаги в Allure: with allure.step('...')."),
    cod(f"{P}-timing-e4", t("""
        Напиши класс-менеджер `Timer` — при входе запоминает `time.perf_counter()`, при выходе сохраняет длительность в атрибут `elapsed` (секунды). `__enter__` возвращает `self`.
        """),
        """
        import time


        class Timer:
            pass
        """,
        """
        import time as _t

        def test_values():
            with Timer() as t:
                _t.sleep(0.05)
            assert 0.04 < t.elapsed < 1, t.elapsed
        """,
        """
        import time


        class Timer:
            def __enter__(self):
                self.start = time.perf_counter()
                return self

            def __exit__(self, *args):
                self.elapsed = time.perf_counter() - self.start
                return False
        """),
    cod(f"{P}-timing-e5", t("""
        Напиши через `@contextmanager` функцию `time_limit(seconds, clock)` — проверка производительности: замерить время блока с помощью функции `clock()` (она возвращает секунды) и, если оно **больше** `seconds`, выбросить `AssertionError(f"медленно: {время:.2f} c > {seconds} c")`. В тесте передадут поддельные часы.
        """),
        """
        from contextlib import contextmanager
        """,
        """
        def test_values():
            ticks = iter([0.0, 0.5, 10.0, 12.25])
            clock = lambda: next(ticks)
            with time_limit(1, clock):
                pass
            try:
                with time_limit(2, clock):
                    pass
            except AssertionError as e:
                assert str(e) == "медленно: 2.25 c > 2 c", str(e)
                return
            assert False, "Нужен AssertionError"
        """,
        """
        from contextlib import contextmanager


        @contextmanager
        def time_limit(seconds, clock):
            start = clock()
            yield
            spent = clock() - start
            if spent > seconds:
                raise AssertionError(f"медленно: {spent:.2f} c > {seconds} c")
        """),
    cod(f"{P}-timing-e6", t("""
        Напиши класс-менеджер `Profiler` — копит суммарное время по именам: `with profiler.measure("db"): ...`. Метод `measure(name)` возвращает менеджер (сделай его через `@contextmanager`), который прибавляет длительность блока к `profiler.totals[name]`. Часы передаются в конструктор: `Profiler(clock)`.
        """),
        """
        from contextlib import contextmanager


        class Profiler:
            pass
        """,
        """
        def test_values():
            ticks = iter([0, 1, 1, 4, 10, 12])
            p = Profiler(lambda: next(ticks))
            with p.measure("db"):
                pass
            with p.measure("db"):
                pass
            with p.measure("api"):
                pass
            assert p.totals == {"db": 4, "api": 2}, p.totals
        """,
        """
        from contextlib import contextmanager


        class Profiler:
            def __init__(self, clock):
                self.clock = clock
                self.totals = {}

            @contextmanager
            def measure(self, name):
                start = self.clock()
                try:
                    yield
                finally:
                    self.totals[name] = self.totals.get(name, 0) + self.clock() - start
        """, hint="@contextmanager можно применить и к методу класса."),
    cod(f"{P}-timing-e7", t("""
        Напиши через `@contextmanager` функцию `step(report, name)` — шаг для отчёта. `report` — список. При входе добавить словарь `{"name": name, "status": None, "steps": []}` в текущий уровень и отдать в `as` **список вложенных шагов** этого словаря. При выходе поставить `"status"`: `"passed"` или `"failed"` (при любом исключении; исключение пробросить).

        ```
        report = []
        with step(report, "заказ") as sub:
            with step(sub, "корзина"):
                pass
        # report == [{"name": "заказ", "status": "passed",
        #             "steps": [{"name": "корзина", "status": "passed", "steps": []}]}]
        ```
        """),
        """
        from contextlib import contextmanager
        """,
        """
        def test_values():
            report = []
            try:
                with step(report, "заказ") as sub:
                    with step(sub, "корзина"):
                        pass
                    with step(sub, "оплата"):
                        raise AssertionError("отказ банка")
            except AssertionError:
                pass
            assert report == [{"name": "заказ", "status": "failed", "steps": [
                {"name": "корзина", "status": "passed", "steps": []},
                {"name": "оплата", "status": "failed", "steps": []},
            ]}], report
        """,
        """
        from contextlib import contextmanager


        @contextmanager
        def step(report, name):
            node = {"name": name, "status": None, "steps": []}
            report.append(node)
            try:
                yield node["steps"]
            except BaseException:
                node["status"] = "failed"
                raise
            node["status"] = "passed"
        """),
    cod(f"{P}-timing-e8", t("""
        Напиши класс-менеджер `SlowLog(threshold, clock, log)`: если блок выполнялся дольше `threshold` секунд, добавить в список `log` строку `"медленно: N c"` (N — с одной цифрой после точки). Использовать можно много раз подряд: каждый `with` — новый замер.
        """),
        """
        class SlowLog:
            pass
        """,
        """
        def test_values():
            ticks = iter([0, 0.3, 1, 3.5, 5, 5.9])
            log = []
            s = SlowLog(0.5, lambda: next(ticks), log)
            for _ in range(3):
                with s:
                    pass
            assert log == ["медленно: 2.5 c", "медленно: 0.9 c"], log
        """,
        """
        class SlowLog:
            def __init__(self, threshold, clock, log):
                self.threshold = threshold
                self.clock = clock
                self.log = log

            def __enter__(self):
                self.start = self.clock()
                return self

            def __exit__(self, *args):
                spent = self.clock() - self.start
                if spent > self.threshold:
                    self.log.append(f"медленно: {spent:.1f} c")
                return False
        """, xp=20),
),

lesson(f"{P}-testing", "Менеджеры в тестах",
    out(f"{P}-testing-e1", "Что выведет программа? Свой raises.", """
        from contextlib import contextmanager

        @contextmanager
        def raises(exc_type):
            try:
                yield
            except exc_type:
                print("ожидаемая ошибка", exc_type.__name__)
            else:
                raise AssertionError(f"не было {exc_type.__name__}")

        with raises(ZeroDivisionError):
            1 / 0
        try:
            with raises(KeyError):
                pass
        except AssertionError as e:
            print(e)
        """, hint="Так устроен pytest.raises."),
    out(f"{P}-testing-e2", "Что выведет программа? Фикстура с yield.", """
        from contextlib import contextmanager

        @contextmanager
        def user_fixture(db):
            user = {"id": len(db) + 1, "name": "test"}
            db.append(user)
            print("создан", user["id"])
            try:
                yield user
            finally:
                db.remove(user)
                print("удалён", user["id"])

        db = []
        with user_fixture(db) as u:
            print("тест с", u["name"], len(db))
        print(len(db))
        """, hint="В pytest фикстура с yield работает так же: до yield — подготовка, после — уборка."),
    out(f"{P}-testing-e3", "Что выведет программа? Проверка вывода.", """
        import io
        from contextlib import redirect_stdout

        def greet(name):
            print(f"Привет, {name}!")

        buf = io.StringIO()
        with redirect_stdout(buf):
            greet("Аня")
        assert buf.getvalue() == "Привет, Аня!\\n"
        print("вывод совпал:", repr(buf.getvalue()))
        """),
    cod(f"{P}-testing-e4", t("""
        Напиши через `@contextmanager` функцию `raises(exc_type, match=None)` — упрощённый `pytest.raises`:

        - отдать в `as` словарь `info` (изначально `{"value": None}`);
        - если внутри блока ошибка типа `exc_type` — заглушить, сохранить в `info["value"]`;
        - если задан `match` и его нет в тексте ошибки — `AssertionError(f"текст не содержит {match!r}")`;
        - если ошибки не было — `AssertionError(f"не было {exc_type.__name__}")`.
        """),
        """
        from contextlib import contextmanager
        """,
        """
        def test_values():
            with raises(ValueError, match="invalid") as info:
                int("x")
            assert isinstance(info["value"], ValueError), "Ошибка сохранена"
            for block, msg in [(lambda: None, "не было KeyError"), (lambda: {}["zz"], "текст не содержит 'qq'")]:
                try:
                    with raises(KeyError, match="qq" if "qq" in msg else None):
                        block()
                except AssertionError as e:
                    assert str(e) == msg, str(e)
                else:
                    assert False, "Нужен AssertionError"
        """,
        """
        from contextlib import contextmanager


        @contextmanager
        def raises(exc_type, match=None):
            info = {"value": None}
            try:
                yield info
            except exc_type as e:
                info["value"] = e
                if match is not None and match not in str(e):
                    raise AssertionError(f"текст не содержит {match!r}") from e
                return
            raise AssertionError(f"не было {exc_type.__name__}")
        """),
    cod(f"{P}-testing-e5", t("""
        Напиши функцию `captured(func, *args)` — вызвать функцию, перехватив всё, что она печатает, и вернуть кортеж `(результат, напечатанный_текст)`.
        """),
        """
        import io
        from contextlib import redirect_stdout


        def captured(func, *args):
            pass
        """,
        """
        def test_values():
            def noisy(a, b):
                print("считаю")
                print(a, b)
                return a + b
            assert captured(noisy, 2, 3) == (5, "считаю\\n2 3\\n"), captured(noisy, 2, 3)
        """,
        """
        import io
        from contextlib import redirect_stdout


        def captured(func, *args):
            buf = io.StringIO()
            with redirect_stdout(buf):
                result = func(*args)
            return result, buf.getvalue()
        """),
    cod(f"{P}-testing-e6", t("""
        Напиши через `@contextmanager` фикстуру `created_users(api, names)`: создаёт пользователей через `api.create(name)` (возвращает id), отдаёт в `as` список id, а после блока удаляет **всех созданных** через `api.delete(id)` — даже если тест упал. Если создание одного из пользователей упало — удалить уже созданных и пробросить ошибку.
        """),
        """
        from contextlib import contextmanager
        """,
        """
        def test_values():
            class Api:
                def __init__(self):
                    self.users = {}
                    self.next = 1
                def create(self, name):
                    if not name:
                        raise ValueError("пустое имя")
                    self.users[self.next] = name
                    self.next += 1
                    return self.next - 1
                def delete(self, uid):
                    del self.users[uid]
            api = Api()
            try:
                with created_users(api, ["аня", "боря"]) as ids:
                    assert ids == [1, 2] and len(api.users) == 2, "Созданы"
                    raise AssertionError("тест упал")
            except AssertionError:
                pass
            assert api.users == {}, "Удалены после падения"
            try:
                with created_users(api, ["вика", ""]):
                    pass
            except ValueError:
                pass
            assert api.users == {}, "Удалены при ошибке создания"
        """,
        """
        from contextlib import contextmanager


        @contextmanager
        def created_users(api, names):
            ids = []
            try:
                for name in names:
                    ids.append(api.create(name))
                yield ids
            finally:
                for uid in ids:
                    api.delete(uid)
        """),
    cod(f"{P}-testing-e7", t("""
        Напиши класс-менеджер `AssertNoNewKeys(data)` — проверка, что код внутри блока не добавил в словарь новых ключей. При выходе (если в блоке не было исключения) сравнить ключи; если появились новые — `AssertionError(f"новые ключи: {отсортированный список}")`.
        """),
        """
        class AssertNoNewKeys:
            pass
        """,
        """
        def test_values():
            d = {"a": 1}
            with AssertNoNewKeys(d):
                d["a"] = 2
            try:
                with AssertNoNewKeys(d):
                    d["z"] = 1
                    d["b"] = 1
            except AssertionError as e:
                assert str(e) == "новые ключи: ['b', 'z']", str(e)
            else:
                assert False, "Нужен AssertionError"
            try:
                with AssertNoNewKeys(d):
                    d["c"] = 1
                    raise KeyError("своя")
            except KeyError:
                pass
            else:
                assert False, "Исходная ошибка важнее проверки"
        """,
        """
        class AssertNoNewKeys:
            def __init__(self, data):
                self.data = data

            def __enter__(self):
                self.before = set(self.data)
                return self.data

            def __exit__(self, exc_type, exc, tb):
                if exc_type is None:
                    new = set(self.data) - self.before
                    if new:
                        raise AssertionError(f"новые ключи: {sorted(new)}")
                return False
        """),
    cod(f"{P}-testing-e8", t("""
        Напиши через `@contextmanager` функцию `mock_calls(obj, name)` — временно заменить метод/функцию `obj.name` на «шпиона»: он записывает аргументы каждого вызова в список и вызывает оригинал, возвращая его результат. В `as` отдать список вызовов (кортежи `args`). После блока вернуть оригинал.
        """),
        """
        from contextlib import contextmanager
        """,
        """
        def test_values():
            class Math:
                @staticmethod
                def add(a, b):
                    return a + b
            with mock_calls(Math, "add") as calls:
                assert Math.add(1, 2) == 3 and Math.add(5, 5) == 10, "Оригинал вызывается"
            assert calls == [(1, 2), (5, 5)], calls
            Math.add(9, 9)
            assert calls == [(1, 2), (5, 5)], "После блока шпион снят"
        """,
        """
        from contextlib import contextmanager


        @contextmanager
        def mock_calls(obj, name):
            original = getattr(obj, name)
            calls = []

            def spy(*args):
                calls.append(args)
                return original(*args)

            setattr(obj, name, spy)
            try:
                yield calls
            finally:
                setattr(obj, name, original)
        """, hint="Так работает unittest.mock: patch + запись вызовов.", xp=25),
),

lesson(f"{P}-resources", "Практика: ресурсы тестового окружения",
    out(f"{P}-resources-e1", "Что выведет программа? Сессия API.", """
        class ApiSession:
            def __init__(self, base_url):
                self.base_url = base_url
                self.token = None

            def __enter__(self):
                self.token = "t-123"
                print("вход, токен", self.token)
                return self

            def __exit__(self, *args):
                print("выход, токен отозван")
                self.token = None
                return False

            def get(self, path):
                return f"GET {self.base_url}{path} [{self.token}]"

        with ApiSession("https://api.test") as s:
            print(s.get("/users"))
        print(s.token)
        """),
    out(f"{P}-resources-e2", "Что выведет программа? Пул соединений.", """
        from contextlib import contextmanager

        class Pool:
            def __init__(self, size):
                self.free = [f"conn{i}" for i in range(size)]

            @contextmanager
            def connection(self):
                conn = self.free.pop()
                try:
                    yield conn
                finally:
                    self.free.append(conn)

        pool = Pool(2)
        with pool.connection() as a:
            with pool.connection() as b:
                print(a, b, pool.free)
            print(pool.free)
        print(sorted(pool.free))
        """),
    out(f"{P}-resources-e3", "Что выведет программа? Всё окружение одним with.", """
        from contextlib import contextmanager, ExitStack

        @contextmanager
        def service(name, log):
            log.append("up " + name)
            try:
                yield name
            finally:
                log.append("down " + name)

        log = []
        with ExitStack() as stack:
            names = [stack.enter_context(service(n, log)) for n in ["db", "cache", "api"]]
            log.append("тесты: " + ", ".join(names))
        print(log)
        """),
    cod(f"{P}-resources-e4", t("""
        Напиши класс-менеджер `Connection(log)` для фейковой БД:

        - `__enter__` добавляет в `log` строку `"connect"` и возвращает `self`;
        - метод `execute(sql)` добавляет `sql` в `log`; если соединение закрыто — `RuntimeError("соединение закрыто")`;
        - `__exit__` добавляет `"close"` и помечает соединение закрытым.
        """),
        """
        class Connection:
            pass
        """,
        """
        def test_values():
            log = []
            with Connection(log) as c:
                c.execute("SELECT 1")
            assert log == ["connect", "SELECT 1", "close"], log
            try:
                c.execute("SELECT 2")
            except RuntimeError as e:
                assert str(e) == "соединение закрыто", str(e)
                return
            assert False, "Нужен RuntimeError"
        """,
        """
        class Connection:
            def __init__(self, log):
                self.log = log
                self.closed = True

            def __enter__(self):
                self.log.append("connect")
                self.closed = False
                return self

            def execute(self, sql):
                if self.closed:
                    raise RuntimeError("соединение закрыто")
                self.log.append(sql)

            def __exit__(self, *args):
                self.log.append("close")
                self.closed = True
                return False
        """),
    cod(f"{P}-resources-e5", t("""
        Допиши к классу `Pool(size)` метод-менеджер `connection()` (через `@contextmanager`): взять свободное соединение из `self.free` (если свободных нет — `RuntimeError("пул исчерпан")`), отдать в `as` и **всегда** вернуть обратно.
        """),
        """
        from contextlib import contextmanager


        class Pool:
            def __init__(self, size):
                self.free = [f"conn{i}" for i in range(size)]
        """,
        """
        def test_values():
            pool = Pool(1)
            with pool.connection() as c:
                assert c == "conn0" and pool.free == [], "Взято"
                try:
                    with pool.connection():
                        pass
                except RuntimeError as e:
                    assert str(e) == "пул исчерпан", str(e)
                else:
                    assert False, "Нужен RuntimeError"
            assert pool.free == ["conn0"], "Возвращено"
            try:
                with pool.connection():
                    raise ValueError
            except ValueError:
                pass
            assert pool.free == ["conn0"], "Возвращено после ошибки"
        """,
        """
        from contextlib import contextmanager


        class Pool:
            def __init__(self, size):
                self.free = [f"conn{i}" for i in range(size)]

            @contextmanager
            def connection(self):
                if not self.free:
                    raise RuntimeError("пул исчерпан")
                conn = self.free.pop()
                try:
                    yield conn
                finally:
                    self.free.append(conn)
        """),
    cod(f"{P}-resources-e6", t("""
        Напиши класс-менеджер `Browser(log)` — фейковый браузер для UI-тестов. При выходе из блока **с ошибкой** он должен «сделать скриншот» — добавить в `log` строку `"screenshot: ИмяОшибки"`, — затем в любом случае `"quit"`. Ошибку не глушить. При входе — `"start"`.
        """),
        """
        class Browser:
            pass
        """,
        """
        def test_values():
            log = []
            with Browser(log):
                pass
            try:
                with Browser(log):
                    raise AssertionError
            except AssertionError:
                pass
            assert log == ["start", "quit", "start", "screenshot: AssertionError", "quit"], log
        """,
        """
        class Browser:
            def __init__(self, log):
                self.log = log

            def __enter__(self):
                self.log.append("start")
                return self

            def __exit__(self, exc_type, exc, tb):
                if exc_type is not None:
                    self.log.append(f"screenshot: {exc_type.__name__}")
                self.log.append("quit")
                return False
        """),
    cod(f"{P}-resources-e7", t("""
        Напиши функцию `environment(names, log)` — через `ExitStack` поднять сервисы с помощью менеджера `service(name, log)` из заготовки в порядке списка и вернуть **сам** `ExitStack`, не закрывая его (метод `pop_all()` переносит всё в новый стек). Вызывающий код потом закроет его через `with`.

        ```
        stack = environment(["db", "api"], log)   # сервисы уже подняты
        with stack:
            ...                                   # после блока — опущены
        ```
        """),
        """
        from contextlib import contextmanager, ExitStack


        @contextmanager
        def service(name, log):
            log.append("up " + name)
            try:
                yield name
            finally:
                log.append("down " + name)


        def environment(names, log):
            pass
        """,
        """
        def test_values():
            log = []
            stack = environment(["db", "api"], log)
            assert log == ["up db", "up api"], "Сервисы подняты сразу"
            with stack:
                log.append("tests")
            assert log == ["up db", "up api", "tests", "down api", "down db"], log
        """,
        """
        from contextlib import contextmanager, ExitStack


        @contextmanager
        def service(name, log):
            log.append("up " + name)
            try:
                yield name
            finally:
                log.append("down " + name)


        def environment(names, log):
            with ExitStack() as stack:
                for name in names:
                    stack.enter_context(service(name, log))
                return stack.pop_all()
        """, hint="Если при подъёме сервиса будет ошибка, with закроет уже поднятые. pop_all() — «успех, закрывать будет вызывающий»."),
    cod(f"{P}-resources-e8", t("""
        Напиши класс-менеджер `TestCase(name, results)`, который оформляет один тест:

        - в `as` отдаёт `self`; метод `check(condition, message)` — мягкая проверка: при ложном условии добавляет `message` в свой список `self.errors`, но **не** прерывает тест;
        - при выходе добавляет в словарь `results` запись `name → "passed"`, если ошибок не было, иначе `"failed: "` + сообщения через `"; "`;
        - если в блоке было исключение — статус `"broken: ИмяОшибки"`, исключение заглушить (тест «сломан», но прогон продолжается).
        """),
        """
        class TestCase:
            pass
        """,
        """
        def test_values():
            results = {}
            with TestCase("ok", results) as t:
                t.check(1 == 1, "не выполнится")
            with TestCase("soft", results) as t:
                t.check(False, "нет заголовка")
                t.check(2 > 1, "-")
                t.check(False, "нет кнопки")
            with TestCase("crash", results):
                {}["x"]
            assert results == {"ok": "passed", "soft": "failed: нет заголовка; нет кнопки", "crash": "broken: KeyError"}, results
        """,
        """
        class TestCase:
            def __init__(self, name, results):
                self.name = name
                self.results = results
                self.errors = []

            def __enter__(self):
                return self

            def check(self, condition, message):
                if not condition:
                    self.errors.append(message)

            def __exit__(self, exc_type, exc, tb):
                if exc_type is not None:
                    self.results[self.name] = f"broken: {exc_type.__name__}"
                    return True
                if self.errors:
                    self.results[self.name] = "failed: " + "; ".join(self.errors)
                else:
                    self.results[self.name] = "passed"
                return False
        """, xp=25),
),
)
