"""Тема «Контекстные менеджеры» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "ctx"

EXPLAIN = {

# ===== Модуль 1. Оператор with =====

f"{P}-m1-l1-e1": x(
    idea="`finally` выполняется даже при `return`: значение уже вычислено, но функция вернёт его только после `finally`.",
    lines=[
        ('return "из try"', "Результат готов, выход отложен."),
        ('print("finally")', "Печатается раньше результата."),
        ("print(f())", "Потом печатается возвращённое."),
    ],
    mistake="Думать, что `return` пропускает `finally`."),

f"{P}-m1-l1-e2": x(
    idea="Ошибка прерывает `try`, срабатывает `except`, и в конце — `finally`.",
    lines=[
        ("1 / 0", "Отсюда — в `except`."),
        ('print("не дойдём")', "Пропущено."),
        ('print("уборка")', "Всегда."),
    ],
    mistake="Ожидать «не дойдём»."),

f"{P}-m1-l1-e3": x(
    idea="`with` закрывает файл сам при выходе из блока.",
    lines=[
        ("print(f.closed)", "Блок закончился — закрыт."),
        ("print(f.read().splitlines())", "Строки без `\\n`."),
    ],
    mistake="Ожидать `False`."),

f"{P}-m1-l1-e4": x(
    idea="Файл открыт в `with` — закроется сам. Каждой строке — свой `\\n`.",
    lines=[
        ('with open(path, "w", encoding="utf-8") as f:', "Перезапись."),
        ('f.write(line + "\\n")', "Перевод строки после каждой."),
    ],
    mistake="Режим `\"a\"` — старое содержимое останется."),

f"{P}-m1-l1-e5": x(
    idea="Файл — перебираемый объект строк; считаем их без загрузки в память.",
    lines=[("return sum(1 for _ in f)", "По единице на строку; `return` в `with` безопасен.")],
    mistake="`len(f)` — у файла нет длины."),

f"{P}-m1-l1-e6": x(
    idea="`finally` срабатывает и при обычном `return`, и после `except`.",
    lines=[
        ("return a / b", "Успех."),
        ("except ZeroDivisionError:\n        return None", "Деление на ноль."),
        ('finally:\n        log.append("done")', "В любом случае."),
    ],
    mistake="Писать в журнал в `try` и `except` по отдельности — легко забыть одну ветку."),

f"{P}-m1-l1-e7": x(
    idea="`finally` срабатывает при `return` и при `break` — перед тем, как управление уйдёт.",
    lines=[
        ('return "отрицательное"', "Сначала `finally`."),
        ("break", "Перед выходом из цикла — `finally`."),
        ('print("итерация", i)', "Для 0 и 1; до 2 не дошли."),
    ],
    mistake="Не ждать «итерация 1» — `finally` сработал и при `break`."),

f"{P}-m1-l1-e8": x(
    idea="`try/finally` без `except`: уборка гарантирована, а ошибка летит дальше.",
    lines=[
        ("return action()", "Результат или исключение."),
        ("finally:\n        cleanup()", "В любом случае."),
    ],
    mistake="Добавить `except: pass` — ошибка будет проглочена."),

f"{P}-multi-e1": x(
    idea="Несколько менеджеров в одном `with` через запятую — закроются все.",
    lines=[
        ('with open("a.txt", "w", encoding="utf-8") as fa, open("b.txt", "w", encoding="utf-8") as fb:', "Два файла сразу."),
        ("print(fa.closed, fb.closed)", "Оба закрыты."),
        ("print(fa.read() + fb.read())", "A + B."),
    ],
    mistake="Думать, что закрывается только последний."),

f"{P}-multi-e2": x(
    idea="Вход — слева направо, выход — в обратном порядке, как у вложенных `with`.",
    lines=[
        ('with Box("А") as a, Box("Б") as b:', "Открыл А, открыл Б."),
        ('print("внутри", a.name, b.name)', "Тело."),
        ('print("закрыл", self.name)', "Сначала Б, потом А."),
    ],
    mistake="Ожидать «закрыл А» первым."),

f"{P}-multi-e3": x(
    idea="Если второй менеджер не открылся, уже открытый первый всё равно закроется.",
    lines=[
        ('with Box("БД") as db, Box("браузер", fail=True) as br:', "БД открыта, браузер падает."),
        ('print("тест")', "Не выполнится."),
        ("print(e)", "Ошибка — после закрытия БД."),
    ],
    mistake="Ожидать, что БД останется открытой."),

f"{P}-multi-e4": x(
    idea="Три файла в одном `with` — все закроются.",
    lines=[
        ('with open(a, encoding="utf-8") as fa, open(b, encoding="utf-8") as fb, open(out, "w", encoding="utf-8") as fo:', "Два на чтение, один на запись."),
        ("fo.write(fa.read())", "Сначала `a`."),
        ("fo.write(fb.read())", "Потом `b`."),
    ],
    mistake="Открыть `out` без `\"w\"` — режим чтения, запись упадёт."),

f"{P}-multi-e5": x(
    idea="`zip` по двум файлам идёт до конца короткого; `enumerate(start=1)` даёт номера.",
    lines=[("return [n for n, (x, y) in enumerate(zip(fa, fb), start=1) if x != y]", "Пара строк и номер.")],
    mistake="Нумерация с 0."),

f"{P}-multi-e6": x(
    idea="Скобки после `with` позволяют перечислить менеджеры на нескольких строках.",
    lines=[
        ('open(errors_path, "w", encoding="utf-8") as ferr,', "Файл ошибок."),
        ('if "ERROR" in line:\n                ferr.write(line)', "Строка уже с `\\n`."),
        ("else:\n                fother.write(line)", "Остальное."),
    ],
    mistake="Добавлять `\\n` — появятся пустые строки."),

f"{P}-multi-e7": x(
    idea="Два менеджера в одном `with` — вложенность: outer входит первым и выходит последним.",
    lines=[
        ('self.log.append("+" + self.name)', "Вход."),
        ('self.log.append("-" + self.name)', "Выход."),
        ('with Tracker("outer", log), Tracker("inner", log):', "+outer, +inner, …, -inner, -outer."),
        ('log.append("work")', "Середина."),
    ],
    mistake="Поменять порядок — `inner` окажется снаружи."),

f"{P}-multi-e8": x(
    idea="Число файлов заранее неизвестно — открываем по одному в цикле, каждый в своём `with`.",
    lines=[
        ("for path in paths:", "По одному."),
        ("result.append(f.read())", "Содержимое."),
        ("except FileNotFoundError:\n            result.append(None)", "Нет файла — `None`."),
    ],
    mistake="Открыть все сразу списком без `with` — забудешь закрыть."),

f"{P}-m1-l2-e1": x(
    idea="`__enter__` срабатывает при входе, `__exit__` — при выходе. Вложенные блоки — как вложенные теги.",
    lines=[
        ('print(f"<{self.name}>")', "Открывающий."),
        ('print(f"</{self.name}>")', "Закрывающий."),
        ('print("текст")', "В самой середине."),
    ],
    mistake="Закрыть `div` раньше `p`."),

f"{P}-m1-l2-e2": x(
    idea="Если `__exit__` возвращает `True`, исключение подавляется и программа продолжается после `with`.",
    lines=[
        ('print("вышли, ошибка:", exc_type.__name__ if exc_type else None)', "Тип ошибки пришёл в `__exit__`."),
        ("return True", "Ошибка проглочена."),
        ('print("программа продолжается")', "Выполнится."),
    ],
    mistake="Ожидать, что программа упадёт."),

f"{P}-m1-l2-e3": x(
    idea="После `as` — то, что вернул `__enter__`, а не сам объект менеджера.",
    lines=[
        ('return "соединение №1"', "Значение для `as`."),
        ("print(c)", "Строка."),
    ],
    mistake="Ожидать объект `Conn`."),

f"{P}-m1-l2-e4": x(
    idea="Два метода делают класс менеджером: вход и выход.",
    lines=[
        ("self.opened = True\n        return self", "Вход: объект — в `as`."),
        ("self.opened = False", "Выход."),
        ("return False", "Ошибки не глушим."),
    ],
    mistake="Забыть `return self` — в `as` окажется `None`."),

f"{P}-m1-l2-e5": x(
    idea="`__exit__` возвращает `True` только для ошибки нужного типа.",
    lines=[
        ("self.exc_class = exc_class", "Что глушить."),
        ("return exc_type is not None and issubclass(exc_type, self.exc_class)", "Ошибка была и это наш тип (или наследник)."),
    ],
    mistake="`issubclass(None, ...)` без проверки — `TypeError` при выходе без ошибки."),

f"{P}-m1-l2-e6": x(
    idea="В `__exit__` видно, была ли ошибка: `exc_type` — её класс или `None`.",
    lines=[
        ('self.events.append("enter")', "Вход."),
        ('self.events.append(f"exit:{exc_type.__name__}" if exc_type else "exit")', "С именем ошибки или без."),
        ("return False", "Не глушим."),
    ],
    mistake="Писать `exc` вместо `exc_type.__name__` — получится текст сообщения."),

f"{P}-m1-l2-e7": x(
    idea="Менеджер — обычный объект; можно использовать его повторно. `__enter__` вернул `self` — `same` и `c` один объект.",
    lines=[
        ("with c:\n    pass", "entered = 1."),
        ("with c as same:", "entered = 2."),
        ("print(same is c, same.entered)", "Один и тот же объект."),
    ],
    mistake="Ожидать 1 — счётчик общий."),

f"{P}-m1-l2-e8": x(
    idea="Уровень хранится в атрибуте класса — общий для всех вложенных менеджеров.",
    lines=[
        ("level = 0", "Атрибут класса."),
        ("Indent.level += 1", "Через имя класса, не `self`."),
        ("Indent.level -= 1", "Выход."),
        ('self.log.append("  " * Indent.level + text)', "Отступ по уровню."),
    ],
    mistake="`self.level += 1` — создаст атрибут объекта, общий счётчик не изменится."),

f"{P}-exit-e1": x(
    idea="Без ошибки `__exit__` получает три `None`. С ошибкой — класс, объект и трассировку.",
    lines=[
        ("print(exc_type, exc, tb is None)", "Три аргумента."),
        ('print("без ошибки")', "Сначала тело, потом `__exit__`."),
        ('int("x")', "`ValueError` — в `__exit__`, потом наружу."),
        ("return False", "Не глушим."),
    ],
    mistake="Ожидать, что `__exit__` не вызывается при ошибке."),

f"{P}-exit-e2": x(
    idea="Глушим только `KeyError`; для остальных `__exit__` вернёт `False` — ошибка летит дальше.",
    lines=[
        ('{}["нет"]', "KeyError — подавлен."),
        ("[][0]", "IndexError — не наш."),
        ("except IndexError:", "Поймали снаружи."),
    ],
    mistake="Думать, что менеджер глушит всё."),

f"{P}-exit-e3": x(
    idea="`return` изнутри `with` тоже вызывает `__exit__` — без ошибки.",
    lines=[
        ("return i", "Выход из функции."),
        ('print("выход, ошибка:", exc_type)', "Перед возвратом."),
        ('print(find(["a", "b"], "b"))', "Индекс 1."),
    ],
    mistake="Ожидать, что `return` пропустит `__exit__`."),

f"{P}-exit-e4": x(
    idea="`issubclass` принимает кортеж классов — удобно для `*exc_types`.",
    lines=[
        ("self.exc_types = exc_types", "Кортеж типов."),
        ("return exc_type is not None and issubclass(exc_type, self.exc_types)", "Любой из них."),
    ],
    mistake="Забыть проверку на `None`."),

f"{P}-exit-e5": x(
    idea="Ошибку сохраняем в атрибут и глушим. `BaseException` вроде `KeyboardInterrupt` не трогаем.",
    lines=[
        ("self.error = None", "По умолчанию."),
        ("if exc_type is not None and issubclass(exc_type, Exception):", "Обычная ошибка."),
        ("self.error = exc\n            return True", "Сохранить и заглушить."),
        ("return False", "Иначе — не вмешиваемся."),
    ],
    mistake="Сохранять `exc_type` вместо самого исключения."),

f"{P}-exit-e6": x(
    idea="Запись результата без подавления ошибки.",
    lines=[
        ('if exc_type is None:\n            self.log.append("ok")', "Успех."),
        ('self.log.append(f"fail: {exc_type.__name__}")', "Имя ошибки."),
        ("return False", "Ошибка летит дальше."),
    ],
    mistake="`return True` — тест перестанет падать."),

f"{P}-exit-e7": x(
    idea="Снимок при входе, откат при ошибке. `clear` + `update` меняют тот же объект, а не создают новый.",
    lines=[
        ("self.snapshot = dict(self.data)", "Копия."),
        ("return self.data", "В `as` — сам словарь."),
        ("self.data.clear()\n            self.data.update(self.snapshot)", "Откат на месте."),
        ("return False", "Пробрасываем."),
    ],
    mistake="`self.data = self.snapshot` — внешний словарь не изменится."),

f"{P}-exit-e8": x(
    idea="Как `pytest.raises`: нужной ошибки не было — тест падает; была — сохраняем и глушим; чужую — пропускаем.",
    lines=[
        ('if exc_type is None:\n            raise AssertionError(f"не было {self.exc_type.__name__}")', "Ожидали ошибку."),
        ("if issubclass(exc_type, self.exc_type):", "Наш тип."),
        ("self.value = exc\n            return True", "Сохранить, заглушить."),
        ("return False", "Чужая — наружу."),
    ],
    mistake="Путать `self.exc_type` (ожидаемый) и `exc_type` (случившийся)."),

# ===== Модуль 2. contextlib =====

f"{P}-m2-l1-e1": x(
    idea="`@contextmanager` делает менеджер из генератора: код до `yield` — вход, после — выход, а тело `with` выполняется на месте `yield`.",
    lines=[
        ('print("▶", name)', "Вход."),
        ("yield", "Здесь выполняется тело `with`."),
        ('print("✔", name)', "Выход."),
    ],
    mistake="Ожидать тело `with` до «▶»."),

f"{P}-m2-l1-e2": x(
    idea="Ошибка в теле `with` возникает на месте `yield`; `finally` вокруг `yield` гарантирует уборку.",
    lines=[
        ("yield user", "В `as` — словарь."),
        ('raise RuntimeError("тест упал")', "Ошибка приходит в генератор."),
        ('finally:\n        print("удалён")', "Уборка — до внешнего `except`."),
        ('print("ошибка:", e)', "Последней."),
    ],
    mistake="Ожидать «ошибка» раньше «удалён»."),

f"{P}-m2-l1-e3": x(
    idea="До `yield` — открывающий тег, после — закрывающий.",
    lines=[
        ("@contextmanager", "Генератор → менеджер."),
        ('print(f"<{name}>")', "Вход."),
        ("yield", "Тело `with`."),
        ('print(f"</{name}>")', "Выход."),
    ],
    mistake="Забыть `yield` — `with` не сработает."),

f"{P}-m2-l1-e4": x(
    idea="Добавить, отдать, удалить — удаление в `finally`, чтобы сработало и при ошибке.",
    lines=[
        ("items.append(value)", "Вход."),
        ("yield value", "В `as`."),
        ("finally:\n        items.remove(value)", "Выход в любом случае."),
    ],
    mistake="Без `try/finally` — при ошибке элемент останется в списке."),

f"{P}-m2-l1-e5": x(
    idea="Отметка времени до `yield`, запись разницы — в `finally`.",
    lines=[
        ("start = time.perf_counter()", "Вход."),
        ("yield", "Тело блока."),
        ("results.append(time.perf_counter() - start)", "Даже если блок упал."),
    ],
    mistake="Записать замер после `yield` без `finally` — при ошибке его не будет."),

f"{P}-m2-l1-e6": x(
    idea="В `as` попадает значение `yield`. Переменная после `with` остаётся доступной.",
    lines=[
        ("yield name.upper()", "`handle = \"DB\"`."),
        ('print("закрываю", name)', "После тела."),
        ("print(handle)", "Переменная жива."),
    ],
    mistake="Ожидать `NameError` после блока."),

f"{P}-m2-l1-e7": x(
    idea="Две записи в журнал вокруг `yield`.",
    lines=[
        ('log.append(f"== {title} ==")', "Вход."),
        ("yield", "Без значения."),
        ('log.append("== конец ==")', "Выход."),
    ],
    mistake="`yield title` — просили ничего не отдавать."),

f"{P}-m2-l1-e8": x(
    idea="Отдаём список, блок наполняет его, после `yield` сортируем на месте.",
    lines=[
        ("items = []", "Новый каждый раз."),
        ("yield items", "В `as`."),
        ("items.sort()", "Тот же объект."),
    ],
    mistake="`items = sorted(items)` — снаружи останется несортированный."),

f"{P}-gen-errors-e1": x(
    idea="Без `try/finally` ошибка из тела прерывает генератор на `yield` — код после него не выполнится.",
    lines=[
        ("yield", "Сюда прилетает `ValueError`."),
        ('print("вернул")', "Пропущено."),
        ('print("ошибка")', "Внешний `except`."),
    ],
    mistake="Ожидать «вернул»."),

f"{P}-gen-errors-e2": x(
    idea="`finally` вокруг `yield` — уборка при любом исходе.",
    lines=[
        ("try:\n        yield", "Ошибка прилетает сюда."),
        ('finally:\n        print("вернул")', "Выполнится."),
        ('print("ошибка")', "Потом — снаружи."),
    ],
    mistake="Ждать «ошибка» раньше «вернул»."),

f"{P}-gen-errors-e3": x(
    idea="`except` вокруг `yield` ловит ошибку тела и глушит её; `else` — если ошибки не было.",
    lines=[
        ('except ZeroDivisionError as e:\n        print(f"{name}: поймал {e}")', "A — поймал."),
        ('else:\n        print(f"{name}: без ошибок")', "B."),
        ('print("дальше")', "Ошибка заглушена — программа идёт дальше."),
    ],
    mistake="Ожидать, что ошибка полетит наружу."),

f"{P}-gen-errors-e4": x(
    idea="Взять, отдать, обязательно вернуть — через `finally`.",
    lines=[
        ("item = pool.pop()", "Берём последний."),
        ("yield item", "В `as`."),
        ("finally:\n        pool.append(item)", "Возврат при любом исходе."),
    ],
    mistake="Без `finally` элемент потеряется при ошибке."),

f"{P}-gen-errors-e5": x(
    idea="`except` с кортежем типов вокруг `yield` — ошибки проглатываются.",
    lines=[
        ("yield", "Тело."),
        ("except exc_types:\n        pass", "`exc_types` — кортеж."),
    ],
    mistake="`except *exc_types` — это другой синтаксис (группы исключений)."),

f"{P}-gen-errors-e6": x(
    idea="Провал — записать и пробросить `raise`; успех — записать после `try`.",
    lines=[
        ('log.append(f"FAIL {name}: {e}")', "Текст ошибки."),
        ("raise", "Тест должен упасть."),
        ('log.append(f"PASS {name}")', "Сюда доходим только без ошибки."),
    ],
    mistake="Без `raise` — провал будет заглушён."),

f"{P}-gen-errors-e7": x(
    idea="Файл создаём до `try`, удаляем в `finally` — если он ещё существует.",
    lines=[
        ("f.write(text)", "Создать."),
        ("yield path", "В `as` — путь."),
        ("if os.path.exists(path):\n            os.remove(path)", "Блок мог сам удалить файл."),
    ],
    mistake="`os.remove` без проверки — ошибка, если файл уже удалён."),

f"{P}-gen-errors-e8": x(
    idea="Ловим одну ошибку и выбрасываем другую, сохраняя причину через `from e`.",
    lines=[
        ("except from_exc as e:", "Исходная."),
        ("raise to_exc(message) from e", "Новая, со ссылкой на старую."),
    ],
    mistake="`from None` — причина потеряется."),

f"{P}-m2-l2-e1": x(
    idea="`suppress` глушит указанную ошибку, но остаток блока после неё пропускается.",
    lines=[
        ('{}["x"]', "KeyError — выход из блока."),
        ('print("после")', "Не выполнится."),
        ('print("дальше")', "Программа продолжается."),
    ],
    mistake="Ожидать «после» — `suppress` не возобновляет блок."),

f"{P}-m2-l2-e2": x(
    idea="`redirect_stdout` временно отправляет `print` в другой файлоподобный объект.",
    lines=[
        ("with redirect_stdout(buf):", "`print` пишет в `buf`."),
        ('print("секрет")', "На экран не попадёт."),
        ('print("перехвачено:", buf.getvalue().strip())', "После блока — снова на экран."),
    ],
    mistake="Ожидать «секрет» отдельной строкой."),

f"{P}-m2-l2-e3": x(
    idea="`ExitStack` — динамический набор менеджеров; закрывает их в обратном порядке.",
    lines=[
        ("stack.enter_context(res(name))", "Вход в каждый."),
        ('print("тест")', "Тело."),
        ('print("закрыл", name)', "Браузер, потом БД."),
    ],
    mistake="Ожидать закрытие в порядке открытия."),

f"{P}-m2-l2-e4": x(
    idea="Перехват вывода: буфер + `redirect_stdout`.",
    lines=[
        ("buf = io.StringIO()", "Куда писать."),
        ("with redirect_stdout(buf):\n        func()", "Всё, что напечатает `func`."),
        ("return buf.getvalue()", "Строка с `\\n`."),
    ],
    mistake="`.strip()` — просили ровно то, что напечатано."),

f"{P}-m2-l2-e5": x(
    idea="`suppress` внутри цикла: неудачная строка пропускается, цикл идёт дальше.",
    lines=[
        ("with suppress(ValueError):", "Для каждой строки отдельно."),
        ("result.append(int(s))", "Если `int` упал — `append` не выполнится."),
    ],
    mistake="`suppress` вокруг цикла — первый мусор остановит всё."),

f"{P}-m2-l2-e6": x(
    idea="`redirect_stderr` перехватывает только поток ошибок; обычный `print` идёт на экран.",
    lines=[
        ('print("предупреждение", file=sys.stderr)', "В буфер."),
        ('print("обычный вывод")', "На экран — сразу."),
        ('print("stderr:", err.getvalue().strip())', "Потом содержимое буфера."),
    ],
    mistake="Думать, что перехватится и обычный вывод."),

f"{P}-m2-l2-e7": x(
    idea="Число файлов заранее неизвестно — `ExitStack` открывает все и закроет при выходе.",
    lines=[
        ('files = [stack.enter_context(open(p, encoding="utf-8")) for p in paths]', "Каждый файл — под управлением стека."),
        ("return [f.read() for f in files]", "Читаем, пока открыты."),
    ],
    mistake="Читать после выхода из `with` — файлы закрыты."),

f"{P}-m2-l2-e8": x(
    idea="`callback` регистрирует функцию на выход; вызываются в обратном порядке.",
    lines=[
        ("for action in actions:\n            stack.callback(action)", "Регистрация."),
    ],
    mistake="Вызвать `action()` сразу — нужна регистрация, а не вызов."),

f"{P}-stdlib-e1": x(
    idea="`closing` делает менеджер из объекта с методом `close()`: при выходе вызовет его.",
    lines=[
        ("with closing(Connection()) as conn:", "В `as` — сам объект."),
        ("print(conn.query())", "Работа."),
        ("print(conn.open)", "`close` уже вызван."),
    ],
    mistake="Ожидать `True`."),

f"{P}-stdlib-e2": x(
    idea="`nullcontext` — менеджер-пустышка: ничего не делает, в `as` отдаёт переданное значение.",
    lines=[
        ("with lock if lock is not None else nullcontext():", "Нет замка — пустышка."),
        ('with nullcontext("значение") as v:', "`v` — само значение."),
    ],
    mistake="Писать два варианта кода — с `with` и без."),

f"{P}-stdlib-e3": x(
    idea="`chdir` временно меняет текущую папку, `localcontext` — точность `Decimal`. После блока всё возвращается.",
    lines=[
        ('with chdir("work"):', "Внутри — папка `work`."),
        ("print(os.getcwd() == start)", "Вернулись."),
        ("ctx.prec = 3", "Три значащие цифры."),
        ("print(Decimal(1) / Decimal(7))", "Снаружи — снова 28 цифр."),
    ],
    mistake="Ожидать, что точность останется 3."),

f"{P}-stdlib-e4": x(
    idea="Нет подходящего менеджера — `try/finally` делает то же самое.",
    lines=[
        ("return action(browser)", "Работа."),
        ("finally:\n        browser.quit()", "Гарантированно."),
    ],
    mistake="Вызвать `quit` после `return` — строка не выполнится."),

f"{P}-stdlib-e5": x(
    idea="`closing(conn)` вызовет `conn.close()` при выходе.",
    lines=[
        ("with closing(conn) as c:", "Менеджер из объекта."),
        ("return c.read()", "Закроется после возврата."),
    ],
    mistake="`with conn:` — у объекта нет `__enter__`."),

f"{P}-stdlib-e6": x(
    idea="Выбираем менеджер заранее: файл или пустышку. У пустышки в `as` — `None`.",
    lines=[
        ('cm = open(log_file, "a", encoding="utf-8") if log_file else nullcontext()', "Один из двух."),
        ("with cm as f:", "Один `with`."),
        ('if f is not None:\n            f.write(f"сумма: {total}\\n")', "Пишем, только если есть файл."),
    ],
    mistake="Писать без проверки — `None.write`."),

f"{P}-stdlib-e7": x(
    idea="`chdir` вернёт папку сама — даже при ошибке и при `return`.",
    lines=[
        ("with chdir(folder):", "Временно."),
        ('return sorted(os.listdir("."))', "Содержимое текущей."),
    ],
    mistake="`os.chdir` без возврата — сломает остальные тесты."),

f"{P}-stdlib-e8": x(
    idea="`localcontext` меняет точность только внутри блока.",
    lines=[
        ("ctx.prec = digits", "Значащие цифры."),
        ("return str(Decimal(a) / Decimal(b))", "Строка результата."),
    ],
    mistake="`getcontext().prec = digits` — изменит точность для всей программы."),

# ===== Модуль 3. Практика =====

f"{P}-state-e1": x(
    idea="Временная настройка: запомнить, изменить, в `finally` вернуть. `clear` + `update` меняют тот же словарь.",
    lines=[
        ("old = dict(settings)", "Копия."),
        ("settings.update(changes)", "Изменения."),
        ("settings.clear()\n        settings.update(old)", "Откат."),
        ("print(config)", "Внутри — test, снаружи — prod."),
    ],
    mistake="`old = settings` — это не копия, откатывать будет нечего."),

f"{P}-state-e2": x(
    idea="`getattr`/`setattr` читают и меняют атрибут по имени-строке — так подменяют настройки в тестах.",
    lines=[
        ("old = getattr(obj, name)", "Оригинал."),
        ("setattr(obj, name, value)", "Подмена."),
        ("setattr(obj, name, old)", "Возврат в `finally`."),
    ],
    mistake="Ожидать, что localhost останется после блока."),

f"{P}-state-e3": x(
    idea="Запоминаем старые значения переменных окружения; не было переменной — после блока удаляем её.",
    lines=[
        ("old = {k: os.environ.get(k) for k in values}", "`None` — переменной не было."),
        ("os.environ.update(values)", "Установка."),
        ("if v is None:\n                del os.environ[k]", "Не было — удаляем."),
        ('print(os.environ.get("STAND"))', "`get` без ошибки — `None`."),
    ],
    mistake="Оставить переменную — она «протечёт» в следующие тесты."),

f"{P}-state-e4": x(
    idea="Маркер `_MISSING` отличает «ключа не было» от «значение было `None`».",
    lines=[
        ("_MISSING = object()", "Уникальный объект-метка."),
        ("old = data.get(key, _MISSING)", "Старое значение или метка."),
        ("if old is _MISSING:\n            del data[key]", "Ключа не было — убрать."),
        ("data[key] = old", "Иначе вернуть."),
    ],
    mistake="`data.get(key)` — не отличить отсутствие ключа от значения `None`."),

f"{P}-state-e5": x(
    idea="Подмена атрибута с возвратом; в `as` — старое значение.",
    lines=[
        ("old = getattr(obj, name)", "Запомнить."),
        ("setattr(obj, name, value)", "Подменить."),
        ("yield old", "Старое — в `as`."),
        ("setattr(obj, name, old)", "Вернуть в `finally`."),
    ],
    mistake="`yield value` — просили старое."),

f"{P}-state-e6": x(
    idea="Функции ищут имена в глобальном словаре модуля при вызове — подмена в `globals()` меняет поведение `greeting`.",
    lines=[
        ("original = module_dict[name]", "Оригинал."),
        ("module_dict[name] = replacement", "Подделка."),
        ("module_dict[name] = original", "Возврат в `finally`."),
    ],
    mistake="Забыть `finally` — упавший тест оставит подделку для остальных."),

f"{P}-state-e7": x(
    idea="Снимок списка при входе; при выходе срез `[:]` заменяет содержимое того же объекта.",
    lines=[
        ("self.saved = list(self.items)", "Копия."),
        ("return self.items", "В `as` — сам список."),
        ("self.items[:] = self.saved", "Тот же объект, старое содержимое."),
    ],
    mistake="`self.items = self.saved` — внешний список не изменится."),

f"{P}-state-e8": x(
    idea="Сохраняем старые значения, ставим новые, в `finally` возвращаем или удаляем.",
    lines=[
        ("old = {key: os.environ.get(key) for key in values}", "Что было."),
        ("os.environ.update(values)", "Новые."),
        ("os.environ.pop(key, None)", "Не было — удалить (без ошибки)."),
        ("os.environ[key] = value", "Было — вернуть."),
    ],
    mistake="Удалять все переменные из `values` — затрёшь существовавшие."),

f"{P}-timing-e1": x(
    idea="Секундомер пишет время в словарь по имени; проверяем диапазон, а не точное число.",
    lines=[
        ("results[name] = time.perf_counter() - start", "В `finally`."),
        ('print(list(results), 0.04 < results["пауза"] < 1)', "Ключ и разумный диапазон."),
    ],
    mistake="Сравнивать время на равенство с 0.05."),

f"{P}-timing-e2": x(
    idea="`elapsed` заполняется только в `__exit__`; внутри блока он ещё `None`.",
    lines=[
        ("self.elapsed = None", "До выхода."),
        ('print("внутри:", t.elapsed)', "None."),
        ("self.elapsed = time.perf_counter() - self.start", "На выходе."),
        ('print("после:", t.elapsed > 0.01)', "Спали 0.02."),
    ],
    mistake="Ожидать число внутри блока."),

f"{P}-timing-e3": x(
    idea="Глобальная глубина растёт при входе и уменьшается в `finally` — получается дерево шагов.",
    lines=[
        ('print("  " * depth + "▶ " + name)', "Отступ по глубине."),
        ("depth += 1", "Вложенные — глубже."),
        ("depth -= 1", "Выход."),
    ],
    mistake="Ожидать «оплата» глубже «корзины» — корзина уже закрылась."),

f"{P}-timing-e4": x(
    idea="Отметка при входе, разница при выходе.",
    lines=[
        ("self.start = time.perf_counter()", "Вход."),
        ("return self", "Для `as`."),
        ("self.elapsed = time.perf_counter() - self.start", "Выход."),
    ],
    mistake="Не вернуть `self` — `t.elapsed` будет недоступен."),

f"{P}-timing-e5": x(
    idea="Часы передаются параметром — тест подставит поддельные. Превышение — провал.",
    lines=[
        ("start = clock()", "Отметка."),
        ("spent = clock() - start", "Затрачено."),
        ('raise AssertionError(f"медленно: {spent:.2f} c > {seconds} c")', "Два знака."),
    ],
    mistake="Вызвать `time.perf_counter()` вместо `clock()`."),

f"{P}-timing-e6": x(
    idea="Метод класса тоже можно сделать менеджером через `@contextmanager`. Время копится по имени.",
    lines=[
        ("@contextmanager\n    def measure(self, name):", "Метод-менеджер."),
        ("start = self.clock()", "Отметка."),
        ("self.totals[name] = self.totals.get(name, 0) + self.clock() - start", "Суммируем."),
    ],
    mistake="`= self.clock() - start` — перезапишет прошлые замеры."),

f"{P}-timing-e7": x(
    idea="Узел добавляется при входе; в `as` — его список вложенных шагов, чтобы строить дерево.",
    lines=[
        ('node = {"name": name, "status": None, "steps": []}', "Узел."),
        ("report.append(node)", "В текущий уровень."),
        ('yield node["steps"]', "Для вложенных шагов."),
        ('except BaseException:\n        node["status"] = "failed"\n        raise', "Провал и проброс."),
        ('node["status"] = "passed"', "Без ошибки."),
    ],
    mistake="Отдавать в `as` весь `report` — вложенность потеряется."),

f"{P}-timing-e8": x(
    idea="Каждый вход запоминает свою отметку, поэтому менеджер можно использовать многократно.",
    lines=[
        ("self.start = self.clock()", "Новая отметка."),
        ("spent = self.clock() - self.start", "Замер."),
        ('self.log.append(f"медленно: {spent:.1f} c")', "Одна цифра после точки."),
    ],
    mistake="Засекать старт в `__init__` — второй `with` посчитает время с создания."),

f"{P}-testing-e1": x(
    idea="Свой `raises`: нужная ошибка — поймана; не было ошибки — `else` бросает `AssertionError`.",
    lines=[
        ('except exc_type:\n        print("ожидаемая ошибка", exc_type.__name__)', "1 / 0 — поймали."),
        ('else:\n        raise AssertionError(f"не было {exc_type.__name__}")', "Блок `pass` — ошибки не было."),
    ],
    mistake="Думать, что тест без ошибки пройдёт."),

f"{P}-testing-e2": x(
    idea="Фикстура на `yield`: создать до, удалить после — как в pytest.",
    lines=[
        ("db.append(user)", "Подготовка."),
        ("yield user", "Тест."),
        ("db.remove(user)", "Уборка."),
        ("print(len(db))", "После — пусто."),
    ],
    mistake="Ожидать 1 в конце."),

f"{P}-testing-e3": x(
    idea="Перехват вывода позволяет проверить, что функция напечатала.",
    lines=[
        ('greet("Аня")', "В буфер."),
        ('assert buf.getvalue() == "Привет, Аня!\\n"', "`print` добавил `\\n`."),
        ('print("вывод совпал:", repr(buf.getvalue()))', "`repr` показывает `\\n`."),
    ],
    mistake="Сравнивать без `\\n` — assert упадёт."),

f"{P}-testing-e4": x(
    idea="Нужная ошибка — сохранить и проверить текст; `return` завершает генератор без ошибки. Дошли до конца — ошибки не было.",
    lines=[
        ('info = {"value": None}', "Контейнер для `as`."),
        ('info["value"] = e', "Сохранили."),
        ('if match is not None and match not in str(e):', "Текст не тот."),
        ("return", "Ошибка поймана — всё хорошо."),
        ('raise AssertionError(f"не было {exc_type.__name__}")', "Блок прошёл без ошибки."),
    ],
    mistake="Забыть `return` — после `except` сработает «не было»."),

f"{P}-testing-e5": x(
    idea="Результат функции и её вывод — вместе.",
    lines=[
        ("with redirect_stdout(buf):\n        result = func(*args)", "Вывод в буфер."),
        ("return result, buf.getvalue()", "Кортеж."),
    ],
    mistake="Вернуть только вывод."),

f"{P}-testing-e6": x(
    idea="Создание — внутри `try`: если упадёт третий, первые два всё равно удалятся.",
    lines=[
        ("ids.append(api.create(name))", "Копим созданные."),
        ("yield ids", "Тест."),
        ("for uid in ids:\n            api.delete(uid)", "Удаляем все созданные."),
    ],
    mistake="Создавать до `try` — при сбое созданные останутся мусором."),

f"{P}-testing-e7": x(
    idea="Множество ключей до и после; разность — новые ключи.",
    lines=[
        ("self.before = set(self.data)", "Ключи на входе."),
        ("if exc_type is None:", "Проверяем только без ошибки."),
        ("new = set(self.data) - self.before", "Новые."),
        ('raise AssertionError(f"новые ключи: {sorted(new)}")', "Сортировка для стабильного текста."),
    ],
    mistake="Проверять при ошибке — перекроешь исходную ошибку."),

f"{P}-testing-e8": x(
    idea="Шпион записывает аргументы и зовёт оригинал; после блока оригинал возвращается.",
    lines=[
        ("original = getattr(obj, name)", "Запомнить."),
        ("calls.append(args)\n        return original(*args)", "Запись и настоящий вызов."),
        ("setattr(obj, name, spy)", "Подмена."),
        ("setattr(obj, name, original)", "Возврат в `finally`."),
    ],
    mistake="Не вызывать оригинал — код перестанет работать."),

f"{P}-resources-e1": x(
    idea="Сессия получает токен при входе и отзывает при выходе.",
    lines=[
        ('self.token = "t-123"', "Вход."),
        ('print(s.get("/users"))', "Запрос с токеном."),
        ("self.token = None", "Выход."),
        ("print(s.token)", "Отозван."),
    ],
    mistake="Ожидать `t-123` после блока."),

f"{P}-resources-e2": x(
    idea="Пул: `pop` забирает последнее соединение, `finally` возвращает его в конец.",
    lines=[
        ("conn = self.free.pop()", "conn1, затем conn0."),
        ("print(a, b, pool.free)", "Свободных нет."),
        ("print(pool.free)", "b вернулся."),
        ("print(sorted(pool.free))", "Оба дома."),
    ],
    mistake="Ожидать `conn0` первым — `pop` берёт с конца."),

f"{P}-resources-e3": x(
    idea="`ExitStack` поднимает сервисы по порядку и гасит в обратном.",
    lines=[
        ('names = [stack.enter_context(service(n, log)) for n in ["db", "cache", "api"]]', "В `names` — значения `yield`."),
        ('log.append("тесты: " + ", ".join(names))', "Середина."),
        ("print(log)", "down в обратном порядке."),
    ],
    mistake="Ожидать `down db` первым."),

f"{P}-resources-e4": x(
    idea="Флаг `closed` защищает от работы вне `with`.",
    lines=[
        ("self.closed = True", "До входа — закрыто."),
        ('self.log.append("connect")\n        self.closed = False', "Вход."),
        ('if self.closed:\n            raise RuntimeError("соединение закрыто")', "Защита."),
        ('self.log.append("close")\n        self.closed = True', "Выход."),
    ],
    mistake="Начальное `closed = False` — можно работать без `with`."),

f"{P}-resources-e5": x(
    idea="Проверка до взятия; возврат — в `finally`.",
    lines=[
        ('if not self.free:\n            raise RuntimeError("пул исчерпан")', "Свободных нет."),
        ("conn = self.free.pop()", "Берём."),
        ("finally:\n            self.free.append(conn)", "Всегда возвращаем."),
    ],
    mistake="Проверка после `pop` — `IndexError` вместо понятной ошибки."),

f"{P}-resources-e6": x(
    idea="Скриншот — только при ошибке, `quit` — всегда. `return False` — ошибка летит дальше.",
    lines=[
        ('if exc_type is not None:\n            self.log.append(f"screenshot: {exc_type.__name__}")', "Упал — снимок."),
        ('self.log.append("quit")', "Всегда."),
        ("return False", "Тест упадёт."),
    ],
    mistake="`quit` перед скриншотом — снимать будет нечего."),

f"{P}-resources-e7": x(
    idea="`pop_all` переносит менеджеры в новый стек — `with` вокруг старого их не закроет.",
    lines=[
        ("stack.enter_context(service(name, log))", "Поднимаем по порядку."),
        ("return stack.pop_all()", "Отдаём живой стек."),
    ],
    mistake="`return stack` — сервисы погаснут при выходе из `with`."),

f"{P}-resources-e8": x(
    idea="Мягкие проверки копят ошибки, а итог пишется при выходе. Сломанный тест отмечается отдельно.",
    lines=[
        ("if not condition:\n            self.errors.append(message)", "Не прерываем."),
        ('self.results[self.name] = f"broken: {exc_type.__name__}"\n            return True', "Исключение — broken, глушим."),
        ('self.results[self.name] = "failed: " + "; ".join(self.errors)', "Были провалы."),
        ('self.results[self.name] = "passed"', "Чисто."),
    ],
    mistake="`raise` при первой проверке — остальные не выполнятся."),
}
