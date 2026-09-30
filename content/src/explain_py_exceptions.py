"""Тема «Исключения» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "exc"

EXPLAIN = {

# ===== Модуль 1. Что такое исключение =====

f"{P}-m1-l1-e1": x(
    idea="Каждой проблеме — свой тип исключения: неверное значение, деление на ноль, нет индекса, нет ключа, несовместимые типы.",
    lines=[
        ('lambda: int("abc"),', "`ValueError` — строка не число."),
        ("lambda: [1, 2][5],", "`IndexError` — нет такого индекса."),
        ('lambda: {"a": 1}["b"],', "`KeyError` — нет ключа."),
        ('lambda: "5" + 5,', "`TypeError` — строку с числом не сложить."),
        ("print(type(e).__name__)", "Имя класса ошибки."),
    ],
    mistake="Путать `KeyError` (словарь) и `IndexError` (список)."),

f"{P}-m1-l1-e2": x(
    idea="Исключение прерывает выполнение сразу: строки после ошибки не выполняются, управление уходит в `except`, а после него программа продолжается.",
    lines=[
        ("x = 1 / 0", "Здесь всё обрывается."),
        ('print("после ошибки")', "Не выполнится."),
        ('print("программа продолжается")', "Ошибка поймана — дальше как обычно."),
    ],
    mistake="Напечатать «после ошибки»."),

f"{P}-m1-l1-e3": x(
    idea="`except … as e` даёт объект ошибки; при печати он показывает текст сообщения.",
    lines=[
        ("print(int(text))", "12 — без ошибки."),
        ('print("ошибка:", e)', "Сообщение Python про `'x'`."),
    ],
    mistake="Ожидать, что после первой ошибки цикл остановится — `try` внутри цикла."),

f"{P}-m1-l1-e4": x(
    idea="Ловим любую ошибку и возвращаем имя её класса; если ошибки нет — выполняется строка после `try/except`.",
    lines=[
        ("except Exception as e:\n        return type(e).__name__", "`ZeroDivisionError`."),
        ('return "нет ошибки"', "Сюда попадаем, только если `func()` отработал."),
    ],
    mistake="Вернуть `str(e)` — это текст, а не тип."),

f"{P}-m1-l1-e5": x(
    idea="Ловим именно `ValueError` — ту ошибку, которую бросает `int` для нечисловой строки.",
    lines=[
        ("try:\n        return int(text)", "Успех."),
        ("except ValueError:\n        return None", "Не число."),
    ],
    mistake="`except:` без типа — поймает и опечатки в коде."),

f"{P}-m1-l1-e6": x(
    idea="Деление на ноль — `ZeroDivisionError`.",
    lines=[("except ZeroDivisionError:\n        return None", "`1 / 0` — вместо ошибки `None`.")],
    mistake="Проверять `b == 0` тоже можно, но задание про исключения."),

f"{P}-m1-l1-e7": x(
    idea="Выход за границы списка — `IndexError`. Заодно правильно работают отрицательные индексы.",
    lines=[("except IndexError:\n        return None", "Нет индекса — `None`.")],
    mistake="Ловить `KeyError` — это для словарей."),

f"{P}-m1-l1-e8": x(
    idea="Тип и текст ошибки — в одну строку через f-строку.",
    lines=[('return f"{type(e).__name__}: {e}"', "`ValueError: invalid literal…`.")],
    mistake="Вернуть `repr(e)` — формат будет другим."),

# ===== try/except подробно =====

f"{P}-m1-l2-e1": x(
    idea="Несколько `except` — разные реакции на разные ошибки. Срабатывает первый подходящий.",
    lines=[
        ("return 100 / int(text)", "Две возможные ошибки в одной строке."),
        ('except ValueError:\n        return "не число"', "`x`."),
        ('except ZeroDivisionError:\n        return "деление на ноль"', "`0`."),
    ],
    mistake="Ожидать 25 без точки — `/` даёт `25.0`."),

f"{P}-m1-l2-e2": x(
    idea="Кортеж в `except` ловит любую из перечисленных ошибок.",
    lines=[("except (KeyError, IndexError, TypeError) as e:", "`None[0]` — `TypeError`.")],
    mistake="Не ожидать `TypeError` для `None`."),

f"{P}-m1-l2-e3": x(
    idea="Если внутренний `except` не подходит по типу, ошибка летит дальше — к вызывающему коду.",
    lines=[
        ("except KeyError:", "`[][0]` — это `IndexError`, не подходит."),
        ("except IndexError:", "Поймали снаружи."),
    ],
    mistake="Ожидать `KeyError` в выводе."),

f"{P}-m1-l2-e4": x(
    idea="Две ошибки — два `except` с разными ответами.",
    lines=[
        ("return 100 / int(text)", "Две возможные ошибки: `int` и деление."),
        ('except ValueError:\n        return "не число"', "Первый обработчик."),
    ],
    mistake="Один общий `except` — не различить причины."),

f"{P}-m1-l2-e5": x(
    idea="Один `except` с кортежем — для ошибок с одинаковой реакцией.",
    lines=[("except (KeyError, IndexError, TypeError):\n        return None", "Три ошибки — одна реакция.")],
    mistake="`except KeyError, IndexError:` без скобок — `SyntaxError`."),

f"{P}-m1-l2-e6": x(
    idea="`float(\"abc\")` — `ValueError`, `float(None)` — `TypeError`. Обе ловим кортежем.",
    lines=[("except (ValueError, TypeError):\n        return 0.0", "Строка-не-число и `None` — одна реакция.")],
    mistake="Ловить только `ValueError` — `None` уронит функцию."),

f"{P}-m1-l2-e7": x(
    idea="Две разные ошибки в одном выражении: нет ключа — `KeyError`, не число — `ValueError`.",
    lines=[
        ("return int(config[key])", "Сначала поиск ключа, потом `int`."),
        ('except KeyError:\n        return f"нет ключа {key}"', "Ключа нет."),
        ('except ValueError:\n        return f"плохое значение {key}"', "Значение не число."),
    ],
    mistake="Перепутать тексты для ошибок."),

f"{P}-m1-l2-e8": x(
    idea="`try` внутри цикла; на первой ошибке — сразу `return`.",
    lines=[
        ("except Exception as e:\n            return type(e).__name__", "Остальные функции не вызываются."),
        ("return None", "Ошибок не было."),
    ],
    mistake="Поставить `try` вокруг цикла — тоже найдёт первую, но так яснее."),

# ===== else и finally =====

f"{P}-m1-l3-e1": x(
    idea="`else` выполняется, если ошибки **не было**; `finally` — всегда.",
    lines=[
        ('else:\n        print("else", n)', "Для `5`."),
        ('except ValueError:\n        print("except")', "Для `x`."),
        ('finally:\n        print("finally")', "В обоих случаях."),
    ],
    mistake="Ожидать `else` и при ошибке."),

f"{P}-m1-l3-e2": x(
    idea="`finally` выполняется даже при `return` — перед тем как функция отдаст значение.",
    lines=[
        ('return "из try"', "Значение запомнено."),
        ('print("finally выполнился")', "Сначала печать…"),
        ("print(f())", "…потом `print` снаружи получает результат."),
    ],
    mistake="Ожидать `из try` первой строкой."),

f"{P}-m1-l3-e3": x(
    idea="`finally` выполняется и при неперехваченной ошибке — а сама ошибка потом летит дальше.",
    lines=[
        ('raise KeyError("x")', "Ошибка."),
        ('print("уборка")', "`finally` успевает выполниться."),
        ('print("ошибка дошла наружу")', "Потом ловим снаружи."),
    ],
    mistake="Ожидать, что `finally` проглотит ошибку."),

f"{P}-m1-l3-e4": x(
    idea="В `try` — только то, что может упасть. Дальнейшая работа — в `else`: так ошибки из неё не будут случайно пойманы.",
    lines=[
        ("n = int(text)", "Только превращение."),
        ("else:\n        return n * 2", "Когда всё хорошо."),
    ],
    mistake="Держать `return n * 2` внутри `try` — работает, но блок ловит больше, чем нужно."),

f"{P}-m1-l3-e5": x(
    idea="`finally` добавляет запись в лог при любом исходе — и успехе, и ошибке.",
    lines=[
        ("except Exception:\n        return None", "Ошибка — `None`."),
        ('finally:\n        log.append("done")', "Выполнится даже после `return`."),
    ],
    mistake="Добавлять запись после `try` — до неё не дойдёт из-за `return`."),

f"{P}-m1-l3-e6": x(
    idea="`try/finally` без `except`: ресурс гарантированно закрывается, а ошибка идёт дальше к вызывающему.",
    lines=[
        ('resource["open"] = True', "Открыли."),
        ("try:\n        return action()", "Работа."),
        ('finally:\n        resource["open"] = False', "Закрыли в любом случае."),
    ],
    mistake="Добавить `except` — задание просит ошибку не перехватывать."),

f"{P}-m1-l3-e7": x(
    idea="Журнал показывает порядок: `try` → `except` или `else` → `finally`.",
    lines=[
        ('log.append("try")', "Всегда первым."),
        ('except ValueError:\n        log.append("except")', "При ошибке."),
        ('else:\n        log.append("else")', "Без ошибки."),
        ('finally:\n        log.append("finally")', "Всегда последним."),
    ],
    mistake="Поставить `\"try\"` после `int(text)` — при ошибке он не запишется."),

f"{P}-m1-l3-e8": x(
    idea="В `try` — вычисление, которое может упасть; округление — в `else`.",
    lines=[
        ("avg = sum(nums) / len(nums)", "Пустой список — деление на ноль."),
        ("else:\n        return round(avg, 2)", "Только если деление прошло."),
    ],
    mistake="Ловить `ValueError` — здесь ошибка другая."),

# ===== Иерархия исключений =====

f"{P}-m1-l4-e1": x(
    idea="Исключения образуют иерархию: `KeyError` и `IndexError` — виды `LookupError`, `ZeroDivisionError` — вид `ArithmeticError`. `KeyboardInterrupt` — не `Exception`.",
    lines=[
        ("print(issubclass(KeyboardInterrupt, Exception))", "`False` — `except Exception` не мешает остановить программу через Ctrl+C."),
    ],
    mistake="Считать, что все исключения — наследники `Exception`."),

f"{P}-m1-l4-e2": x(
    idea="`except` с базовым классом ловит всех его потомков.",
    lines=[("except LookupError as e:", "Ловит и `KeyError`, и `IndexError`.")],
    mistake="Ожидать, что `LookupError` не поймает `KeyError`."),

f"{P}-m1-l4-e3": x(
    idea="Срабатывает **первый** подходящий `except`. Общий класс выше частного перекрывает его.",
    lines=[
        ("except LookupError:", "Подходит для `KeyError` — срабатывает."),
        ("except KeyError:", "До него дело не доходит."),
    ],
    mistake="Ожидать `KeyError` — порядок решает."),

f"{P}-m1-l4-e4": x(
    idea="Общий базовый класс `LookupError` покрывает и словари, и списки.",
    lines=[("except LookupError:\n        return None", "Покрывает `KeyError` и `IndexError`.")],
    mistake="Перечислять кортежем — работает, но базовый класс короче."),

f"{P}-m1-l4-e5": x(
    idea="От частного к общему: сначала `LookupError`, `ArithmeticError`, потом `Exception`.",
    lines=[
        ('except LookupError:\n        return "lookup"', "Частные классы — выше."),
        ('except Exception:\n        return "other"', "Последним."),
        ('return "ok"', "Без ошибок."),
    ],
    mistake="Поставить `Exception` первым — всё станет `other`."),

f"{P}-m1-l4-e6": x(
    idea="Частный обработчик — выше общего.",
    lines=[
        ('except KeyError:\n        return "нет ключа"', "Теперь срабатывает."),
        ('except Exception:\n        return "ошибка"', "Остальное."),
    ],
    mistake="Оставить `Exception` первым."),

f"{P}-m1-l4-e7": x(
    idea="`__mro__` — цепочка классов от текущего к предкам. Идём по ней до `BaseException`.",
    lines=[
        ("for cls in exc_type.__mro__:", "KeyError, LookupError, Exception, BaseException, object."),
        ("if cls is BaseException:\n            break", "`object` не нужен."),
    ],
    mistake="Не остановиться — в конце окажется `object`."),

f"{P}-m1-l4-e8": x(
    idea="`isinstance` учитывает наследование: `KeyError` — это `LookupError`.",
    lines=[("return isinstance(exc, LookupError)", "`KeyError(\"x\")` → `True`.")],
    mistake="`type(exc) == LookupError` — для `KeyError` даст `False`."),

# ===== Модуль 2. raise =====

f"{P}-m2-l1-e1": x(
    idea="`raise` сообщает об ошибке: функция сразу прерывается, а вызывающий код может её поймать.",
    lines=[
        ('raise ValueError(f"возраст не может быть отрицательным: {age}")', "Понятный текст с данными."),
        ('print("ошибка:", e)', "Этот текст и видим."),
    ],
    mistake="Возвращать строку ошибки вместо `raise` — вызывающий код может её не заметить."),

f"{P}-m2-l1-e2": x(
    idea="Тип ошибки выбирают по смыслу: не тот тип данных — `TypeError`, неверное значение — `ValueError`.",
    lines=[
        ('raise TypeError("нужно целое число")', "Для `\"5\"`."),
        ('raise ValueError("нужно положительное")', "Для −1."),
    ],
    mistake="Использовать один тип для всех проблем."),

f"{P}-m2-l1-e3": x(
    idea="Код после `raise` не выполняется. `e.args` — кортеж аргументов исключения.",
    lines=[
        ('raise RuntimeError("стоп")', "Функция прерывается."),
        ("print(e.args)", "`('стоп',)`."),
    ],
    mistake="Напечатать «не выполнится»."),

f"{P}-m2-l1-e4": x(
    idea="Проверки в начале функции с `raise`, в конце — нормальный результат.",
    lines=[
        ('if amount <= 0:\n        raise ValueError("сумма должна быть положительной")', "Ноль и минус."),
        ('if amount > balance:\n        raise ValueError("недостаточно средств")', "Больше баланса."),
        ("return balance - amount", "Всё в порядке."),
    ],
    mistake="Возвращать `None` при ошибке."),

f"{P}-m2-l1-e5": x(
    idea="Сначала проверяем формат, потом диапазон — две разные ошибки с понятными текстами.",
    lines=[
        ('if not text.isdigit():\n        raise ValueError("порт должен быть числом")', "Формат."),
        ('if not 1 <= port <= 65535:\n        raise ValueError("порт вне диапазона")', "Диапазон."),
    ],
    mistake="`int(text)` без проверки — текст ошибки будет от Python, а не наш."),

f"{P}-m2-l1-e6": x(
    idea="`KeyError(key)` с именем первого отсутствующего ключа.",
    lines=[("if key not in data:\n            raise KeyError(key)", "Первое нарушение прерывает проверку.")],
    mistake="Собирать все отсутствующие — задание про первый."),

f"{P}-m2-l1-e7": x(
    idea="Проверка типа и значения в одном условии через `or`: достаточно одной причины.",
    lines=[
        ('if not isinstance(name, str) or not name:', "Не строка или пустая."),
        ("if not isinstance(age, int) or not 0 <= age <= 150:", "Тип проверяется первым — сравнение со строкой не случится."),
    ],
    mistake="Поменять части местами — `0 <= \"x\"` вызовет чужой `TypeError`."),

f"{P}-m2-l1-e8": x(
    idea="Приём `raise_for_status`: ошибочный HTTP-код превращается в исключение, успешный ответ возвращается как есть.",
    lines=[
        ('if response["status"] >= 400:', "4xx и 5xx."),
        ("""raise RuntimeError(f"HTTP {response['status']}")""", "Одинарные кавычки внутри f-строки."),
    ],
    mistake="Возвращать `None` при ошибке — тест не упадёт, а должен."),

# ===== Свои исключения =====

f"{P}-m2-l2-e1": x(
    idea="Своё исключение — класс-наследник `Exception`. Часто тело — просто `pass`.",
    lines=[
        ("class ValidationError(Exception):\n    pass", "Новый тип ошибки."),
        ('raise ValidationError("email без @")', "Выбрасывается как любое другое."),
    ],
    mistake="Наследоваться от `BaseException` — такие ошибки не ловит `except Exception`."),

f"{P}-m2-l2-e2": x(
    idea="Иерархия своих ошибок: один `except AppError` ловит все подтипы.",
    lines=[("except AppError as e:", "И `NotFound`, и `Forbidden`.")],
    mistake="Ожидать `AppError` в имени типа — печатается реальный класс."),

f"{P}-m2-l2-e3": x(
    idea="Своё исключение может хранить данные — например, HTTP-статус.",
    lines=[
        ('super().__init__(f"{status}: {message}")', "Текст исключения."),
        ("self.status = status", "Отдельное поле."),
        ("print(e.status, str(e))", "`503` и полный текст."),
    ],
    mistake="Забыть `super().__init__` — `str(e)` будет пустым."),

f"{P}-m2-l2-e4": x(
    idea="Своя ошибка валидации делает код понятнее: по типу сразу видно, что пошло не так.",
    lines=[('raise ValidationError("нет @")', "Своё исключение с текстом.")],
    mistake="`raise ValidationError` без текста — сообщение будет пустым."),

f"{P}-m2-l2-e5": x(
    idea="Базовый класс API и два подкласса; функция выбирает нужный по коду.",
    lines=[
        ('if status == 404:\n        raise NotFoundError("не найдено")', "Частный случай."),
        ('if status in (401, 403):\n        raise AuthError("нет доступа")', "Нет прав."),
        ('if status >= 400:\n        raise ApiError(f"ошибка {status}")', "Остальные ошибки."),
    ],
    mistake="Проверить `>= 400` первым — всё станет `ApiError`."),

f"{P}-m2-l2-e6": x(
    idea="Один `except ApiError` ловит все подтипы; имя реального класса — через `type(e).__name__`.",
    lines=[
        ("except ApiError as e:", "404 и 403 тоже сюда."),
        ('return f"{type(e).__name__}: {e}"', "`NotFoundError: не найдено`."),
    ],
    mistake="Писать `ApiError` в строке вручную — потеряется конкретный тип."),

f"{P}-m2-l2-e7": x(
    idea="Данные в исключении: из `except` можно достать `status`.",
    lines=[
        ("except HttpError as e:\n        return e.status", "Поле исключения."),
        ("return 200", "Ошибки не было."),
    ],
    mistake="Парсить статус из текста ошибки."),

f"{P}-m2-l2-e8": x(
    idea="Собираем все ошибки и бросаем **одно** исключение со списком — пользователь увидит все проблемы сразу.",
    lines=[
        ('super().__init__("; ".join(errors))', "Текст — все сообщения."),
        ("self.errors = errors", "Список для программы."),
        ("if errors:\n        raise ValidationError(errors)", "Только если что-то нашли."),
    ],
    mistake="`raise` на первой ошибке — остальные не будут видны."),

# ===== Повторный выброс и цепочки =====

f"{P}-m2-l3-e1": x(
    idea="`raise` без аргументов внутри `except` выбрасывает ту же ошибку дальше — можно записать в лог и не «проглотить» проблему.",
    lines=[
        ('log.append("записали в лог")', "Своя реакция."),
        ("raise", "Та же `ZeroDivisionError` летит наружу."),
        ('print("снаружи тоже поймали", log)', "Лог уже заполнен."),
    ],
    mistake="Думать, что после `except` ошибка исчезла."),

f"{P}-m2-l3-e2": x(
    idea="`raise Новая(...) from e` — выбросить свою ошибку, сохранив исходную причину в `__cause__`.",
    lines=[
        ('raise ConfigError("плохой конфиг") from e', "Понятная ошибка верхнего уровня."),
        ('print(e, "| причина:", type(e.__cause__).__name__)', "Причина — `ValueError` от `int(\"x\")`."),
    ],
    mistake="Ожидать `KeyError` — ключ `port` есть, упал `int`."),

f"{P}-m2-l3-e3": x(
    idea="Ошибка, выброшенная внутри `except` без `from`, всё равно помнит предыдущую — в `__context__`. А `__cause__` пустой.",
    lines=[
        ('raise ValueError("не нашли")', "Новая ошибка во время обработки старой."),
        ('print(e, "|", type(e.__context__).__name__, e.__cause__)', "`KeyError` и `None`."),
    ],
    mistake="Путать `__context__` (неявная связь) и `__cause__` (явная через `from`)."),

f"{P}-m2-l3-e4": x(
    idea="Записать в лог и пробросить дальше — `raise` без аргументов.",
    lines=[
        ('log.append("деление на ноль")', "Запись."),
        ("raise", "Та же ошибка наружу."),
    ],
    mistake="`raise ZeroDivisionError()` — новая ошибка без исходного текста и трассировки."),

f"{P}-m2-l3-e5": x(
    idea="Своя ошибка поверх технической, с `from e` — причина не теряется.",
    lines=[
        ("except (KeyError, ValueError) as e:", "Нет ключа или не число."),
        ('raise ConfigError("плохой порт") from e', "Понятно и с причиной."),
    ],
    mistake="Без `from` — связь всё равно будет в `__context__`, но задание просит явную причину."),

f"{P}-m2-l3-e6": x(
    idea="Идём по цепочке причин, пока следующей нет; последняя — корень проблемы.",
    lines=[
        ("nxt = exc.__cause__ or exc.__context__", "Явная причина или неявная."),
        ("if nxt is None:\n            return type(exc).__name__", "Дошли до начала."),
        ("exc = nxt", "Шаг назад по цепочке."),
    ],
    mistake="Смотреть только `__cause__` — неявные цепочки не пройдутся."),

f"{P}-m2-l3-e7": x(
    idea="Ошибка с контекстом: номер элемента и само значение, а исходная ошибка — причина.",
    lines=[
        ("for i, v in enumerate(values):", "Номер с 0."),
        ('raise ValueError(f"элемент {i}: {v!r}") from e', "`!r` показывает строку в кавычках."),
    ],
    mistake="Ловить ошибку вне цикла — номер элемента будет неизвестен."),

f"{P}-m2-l3-e8": x(
    idea="`from None` скрывает исходную причину — пользователь увидит только новую ошибку.",
    lines=[
        ("except Exception:\n        return default", "`quiet` — просто запасное значение."),
        ('raise RuntimeError("сбой") from None', "`__cause__` пуст, контекст подавлен."),
    ],
    mistake="`raise RuntimeError(\"сбой\")` без `from None` — в трассировке останется исходная ошибка."),

# ===== assert =====

f"{P}-m2-l4-e1": x(
    idea="`assert условие, сообщение` проверяет предположение; если оно ложно — `AssertionError` с этим сообщением.",
    lines=[
        ('assert len(nums) > 0, "список пуст"', "Для `[]` — ошибка."),
        ('print("AssertionError:", e)', "Текст из `assert`."),
    ],
    mistake="Ожидать `ZeroDivisionError` — `assert` сработал раньше деления."),

f"{P}-m2-l4-e2": x(
    idea="`assert (условие, текст)` со скобками проверяет **кортеж** — а непустой кортеж всегда истинен. Такой `assert` никогда не падает.",
    lines=[
        ('assert (1 == 2, "никогда не сработает")', "Кортеж из двух элементов — истина."),
        ('print("assert прошёл!")', "Выполняется."),
    ],
    mistake="Ставить скобки вокруг `assert` — Python даже предупреждает об этом."),

f"{P}-m2-l4-e3": x(
    idea="`AssertionError` — обычное исключение: его можно поймать и продолжить.",
    lines=[
        ('assert x > 0, f"{x} не положительное"', "Для −1 — ошибка."),
        ("results.append(str(e))", "Текст ошибки — в результаты."),
    ],
    mistake="Ожидать, что после первой ошибки цикл остановится."),

f"{P}-m2-l4-e4": x(
    idea="Сообщение `assert` должно объяснять расхождение: что ждали и что получили. `!r` покажет строки в кавычках.",
    lines=[
        ('assert actual == expected, f"ожидали {expected!r}, получили {actual!r}"', "Сообщение показывает оба значения."),
        ("return True", "Совпало."),
    ],
    mistake="Сообщение без значений — непонятно, что сломалось."),

f"{P}-m2-l4-e5": x(
    idea="Без скобок: условие, запятая, сообщение.",
    lines=[('assert x > 0, "нужно положительное"', "Теперь реально проверяет.")],
    mistake="Оставить скобки."),

f"{P}-m2-l4-e6": x(
    idea="Мини-раннер: каждую проверку вызываем в `try` и записываем результат.",
    lines=[
        ('check()\n            result[name] = "ok"', "Не упала."),
        ("except AssertionError as e:\n            result[name] = str(e)", "Текст провала."),
    ],
    mistake="Ловить `Exception` — ошибки кода смешаются с провалами проверок."),

f"{P}-m2-l4-e7": x(
    idea="`assert` — для проверок программиста, его можно отключить флагом `-O`. Проверки пользовательских данных — через `raise`.",
    lines=[('if q <= 0:\n        raise ValueError("количество должно быть положительным")', "Работает всегда.")],
    mistake="Оставить `assert` для входных данных."),

f"{P}-m2-l4-e8": x(
    idea="Своя версия `pytest.raises`: ловим только нужный тип, остальные летят дальше, отсутствие ошибки — провал.",
    lines=[
        ("except exc_type as e:\n        return e", "Нужная ошибка — возвращаем объект."),
        ('raise AssertionError(f"ожидали {exc_type.__name__}")', "Ошибки не было."),
    ],
    mistake="`except Exception` — другие типы тоже будут считаться успехом."),

# ===== Модуль 3. EAFP и LBYL =====

f"{P}-m3-l1-e1": x(
    idea="LBYL — «посмотри, прежде чем прыгать»: сначала проверка. EAFP — «проще попросить прощения»: пробуем и ловим ошибку.",
    lines=[
        ('if "b" in data:', "LBYL."),
        ("except KeyError:", "EAFP."),
    ],
    mistake="Считать, что один стиль «правильный» — оба рабочие."),

f"{P}-m3-l1-e2": x(
    idea="Проверка заранее может не совпадать с тем, что умеет функция: `isdigit` не пропускает `-3` и `\" 7\"`, а `int` их принимает.",
    lines=[
        ("print(repr(text), text.isdigit(), end=\" | \")", "Результат проверки."),
        ("print(int(text))", "Результат реальной попытки."),
    ],
    mistake="Считать `isdigit` надёжной заменой `try`."),

f"{P}-m3-l1-e3": x(
    idea="Для простого «есть ли ключ» удобен `get`; для цепочки «ключ + превращение» — `try`.",
    lines=[
        ('print(config.get("retries", 3))', "Нет ключа — 3."),
        ('print(int(config["timeout"]) * 2)', "Ключ есть, число — 60."),
    ],
    mistake="Ожидать строку `\"3030\"` — есть `int`."),

f"{P}-m3-l1-e4": x(
    idea="Одна попытка покрывает три проблемы: нет ключа, не число, `None`.",
    lines=[("except (KeyError, ValueError, TypeError):\n        return default", "Три проблемы — одна реакция.")],
    mistake="Проверять каждую проблему через `if` — длиннее и легко что-то пропустить."),

f"{P}-m3-l1-e5": x(
    idea="Самый надёжный способ узнать, число ли это, — попробовать `float`.",
    lines=[
        ("float(text)\n        return True", "`1e3` и `-3` проходят."),
        ("except ValueError:\n        return False", "Не получилось — не число."),
    ],
    mistake="`text.isdigit()` — не пропустит минус, точку, пробелы."),

f"{P}-m3-l1-e6": x(
    idea="Вместо проверки `in` — попытка и `except KeyError`.",
    lines=[("except KeyError:\n        return 0", "Нет товара — 0.")],
    mistake="Ловить `Exception` — спрячешь и другие ошибки."),

f"{P}-m3-l1-e7": x(
    idea="Идём по ключам в `try`: отсутствующий ключ — `KeyError`, не словарь — `TypeError`.",
    lines=[
        ("for key in keys:\n            data = data[key]", "Спуск."),
        ("except (KeyError, TypeError):\n        return default", "`1[\"b\"]` — `TypeError`."),
    ],
    mistake="Ловить только `KeyError`."),

f"{P}-m3-l1-e8": x(
    idea="Первое значение, которое превращается в `int`: при ошибке — `continue`.",
    lines=[
        ("try:\n            return int(item)", "Получилось — ответ."),
        ("except (ValueError, TypeError):\n            continue", "Дальше."),
    ],
    mistake="Не ловить `TypeError` — `None` уронит функцию."),

# ===== Ошибки в циклах =====

f"{P}-m3-l2-e1": x(
    idea="Плохие данные пропускаем и считаем, хорошие — суммируем.",
    lines=[
        ("total += int(raw)", "10 + 5 + 7."),
        ("errors += 1\n        continue", "`x` и пустая строка."),
    ],
    mistake="Считать пустую строку нулём."),

f"{P}-m3-l2-e2": x(
    idea="`ValueError` возникает и при неудачной распаковке (не две части), и при `int`. Оба случая уходят в «плохие».",
    lines=[
        ('a, b = row.split(",")', "`\"3\"` — одна часть, ошибка распаковки."),
        ("good.append(int(a) + int(b))", "`\"a\"` — не число."),
    ],
    mistake="Ожидать, что `\"3\"` пройдёт."),

f"{P}-m3-l2-e3": x(
    idea="Повтор при сетевой ошибке: `break` после успеха.",
    lines=[
        ("print(attempt, request())", "Третья попытка — `ok`."),
        ("break", "Больше не пробуем."),
    ],
    mistake="Ожидать четвёртую попытку."),

f"{P}-m3-l2-e4": x(
    idea="Два счётчика: сумма и ошибки.",
    lines=[
        ("total += int(item)", "Число — в сумму."),
        ("except (ValueError, TypeError):\n            errors += 1", "И строки, и `None`."),
    ],
    mistake="Ловить только `ValueError`."),

f"{P}-m3-l2-e5": x(
    idea="Плохая строка не прерывает обработку — её номер уходит в список ошибок.",
    lines=[
        ('name, age = row.split(",")', "Не две части — `ValueError`."),
        ('good.append({"name": name, "age": int(age)})', "Возраст не число — тоже `ValueError`."),
        ("except ValueError:\n            bad.append(i)", "Номер с 1."),
    ],
    mistake="`enumerate` без `start=1`."),

f"{P}-m3-l2-e6": x(
    idea="На последней попытке ошибку не глотаем, а пробрасываем.",
    lines=[
        ("return func()", "Успех."),
        ("if attempt == attempts - 1:\n                raise", "Больше попыток нет."),
    ],
    mistake="Вернуть `None` после всех провалов — задание просит ошибку."),

f"{P}-m3-l2-e7": x(
    idea="Упавшая проверка (`AssertionError`) — это `fail`, любая другая ошибка — `error`: тест сломался, а не нашёл баг.",
    lines=[
        ('except AssertionError:\n            results[name] = "fail"', "Частный — выше."),
        ('except Exception:\n            results[name] = "error"', "Остальное."),
    ],
    mistake="Поставить `Exception` первым — всё станет `error`."),

f"{P}-m3-l2-e8": x(
    idea="Критическое событие останавливает обработку через `raise` с номером шага.",
    lines=[
        ('if event == "critical":\n            raise RuntimeError(f"critical на шаге {i}")', "Остановка с номером шага."),
        ('if event == "ok":\n            count += 1', "`warn` просто пропускается."),
    ],
    mistake="Проверять `critical` после подсчёта — порядок здесь не важен, но проверять опасное первым — хорошая привычка."),

# ===== Исключения и тесты =====

f"{P}-m3-l3-e1": x(
    idea="Тест на ошибку: если исключение было — тест прошёл; если нет — провал.",
    lines=[
        ('except exc_type:\n        return "ok: ошибка есть"', "Ожидаемая ошибка."),
        ('return "плохо: ошибки нет"', "`int(\"5\")` не упал."),
    ],
    mistake="Путать логику: здесь ошибка — это ожидаемый результат."),

f"{P}-m3-l3-e2": x(
    idea="Можно проверять и текст ошибки — через `str(e)` или `e.args[0]`.",
    lines=[('print("недостаточно" in str(e), e.args[0])', "Подстрока найдена; `args[0]` — полный текст.")],
    mistake="Сравнивать весь текст точно — хрупко, если сообщение чуть изменится."),

f"{P}-m3-l3-e3": x(
    idea="Тест, ловящий любое исключение, «проходит» даже на чужом баге. Правильный тест ловит только ожидаемую ошибку.",
    lines=[
        ('except Exception:\n        return "тест прошёл?!"', "`IndexError` замаскирован."),
        ('return f"неожиданная {type(e).__name__}"', "Честный отчёт."),
    ],
    mistake="Писать `except Exception` в тестах."),

f"{P}-m3-l3-e4": x(
    idea="Тест проверяет и хороший случай, и плохие. Если ошибки не было — `assert False` с понятным сообщением.",
    lines=[
        ('assert parse_port("8080") == 8080', "Хороший вход."),
        ("except ValueError:\n            continue", "Ожидаемая ошибка — к следующему."),
        ('assert False, f"для {bad!r} нет ValueError"', "Ошибки не было — провал."),
    ],
    mistake="Забыть `continue` — `assert False` сработает даже при правильной ошибке."),

f"{P}-m3-l3-e5": x(
    idea="Нужный тип — проверяем текст; другой тип или отсутствие ошибки — `False`.",
    lines=[
        ("except exc_type as e:\n        return text in str(e)", "Тип совпал — проверяем текст."),
        ("except Exception:\n        return False", "Не тот тип."),
        ("return False", "Ошибки не было."),
    ],
    mistake="Пропустить последний `return` — функция вернёт `None`."),

f"{P}-m3-l3-e6": x(
    idea="Для каждого случая — результат или имя ошибки.",
    lines=[
        ('lines.append(f"{case!r}: ok {result!r}")', "`'5': ok 5`."),
        ('lines.append(f"{case!r}: {type(e).__name__}")', "`'x': ValueError`."),
    ],
    mistake="Держать `try` вокруг цикла — первая ошибка прервёт отчёт."),

f"{P}-m3-l3-e7": x(
    idea="Тест должен ловить только ожидаемую ошибку; нет ошибки — провал.",
    lines=[
        ("except ZeroDivisionError:\n        return", "Ожидаемо — тест прошёл."),
        ('assert False, "ожидали ZeroDivisionError"', "Иначе — провал."),
    ],
    mistake="`except Exception` — пропустит любую поломку."),

f"{P}-m3-l3-e8": x(
    idea="Три исхода: нужная ошибка, другая ошибка, никакой ошибки — у каждого свой ответ.",
    lines=[
        ("except exc_type as e:\n        return str(e)", "Нужный тип — текст."),
        ('raise AssertionError(f"ожидали {exc_type.__name__}, получили {type(e).__name__}")', "Не тот тип."),
        ('raise AssertionError("не было исключения")', "Ошибки не было вовсе."),
    ],
    mistake="Порядок `except`: общий `Exception` выше частного перехватит всё."),

# ===== Практика =====

f"{P}-m3-l4-e1": x(
    idea="Пустая строка и HTML — не JSON. `int(\"2\")` превращает строковый id в число.",
    lines=[
        ("data = json.loads(body)", "Ошибка разбора — в `except`."),
        ('print("id =", int(data["id"]))', "`\"2\"` → 2."),
    ],
    mistake="Считать пустую строку корректным JSON."),

f"{P}-m3-l4-e2": x(
    idea="Плохой формат — `None` (тихо), нарушение правила — явная ошибка. Разные проблемы — разная реакция.",
    lines=[
        ("except ValueError:\n        return None", "`плохо` — не распаковать."),
        ('raise ValueError("возраст < 0")', "Боря с −1."),
    ],
    mistake="Ожидать `None` для Бори."),

f"{P}-m3-l4-e3": x(
    idea="`Counter` по именам типов ошибок — сводка.",
    lines=[("errors[type(e).__name__] += 1", "Строки — `ValueError`, `None` и `[]` — `TypeError`.")],
    mistake="Считать `[]` за `ValueError`."),

f"{P}-m3-l4-e4": x(
    idea="Одна строка может упасть четырьмя способами — ловим все четыре.",
    lines=[
        ('return int(json.loads(text)["id"])', "Разбор → поле → число."),
        ("except (json.JSONDecodeError, KeyError, ValueError, TypeError):", "Корень-массив даёт `TypeError`."),
    ],
    mistake="Забыть `TypeError` — `[1][\"id\"]` уронит функцию."),

f"{P}-m3-l4-e5": x(
    idea="Словарь-счётчик по имени типа ошибки.",
    lines=[
        ("name = type(e).__name__", "Имя типа."),
        ("stats[name] = stats.get(name, 0) + 1", "Подсчёт."),
    ],
    mistake="Считать текст ошибки вместо типа."),

f"{P}-m3-l4-e6": x(
    idea="Три проверки по очереди, у каждой своё сообщение; `continue` — к следующей строке.",
    lines=[
        ('if len(parts) != 3:\n            errors.append(f"строка {i}: неверный формат")', "Проверка до распаковки."),
        ('except ValueError:\n            errors.append(f"строка {i}: возраст не число")', "`int` не справился."),
        ('if "@" not in email:', "Email."),
    ],
    mistake="Распаковать до проверки длины — `ValueError` спутается с ошибкой возраста."),

f"{P}-m3-l4-e7": x(
    idea="Каждый шаг в своём `try`: знаем, на каком шаге сломалось.",
    lines=[
        ("value = step(value)", "Результат идёт в следующий шаг."),
        ('return ("error", i, type(e).__name__)', "Номер шага и тип ошибки."),
    ],
    mistake="Один `try` вокруг цикла — номер шага придётся вычислять отдельно."),

f"{P}-m3-l4-e8": x(
    idea="Значения по умолчанию через `get`, ошибка с понятным текстом и причиной через `from e`.",
    lines=[
        ('timeout = int(raw.get("timeout", "30"))', "Умолчание — тоже строка."),
        ("""raise ValueError(f"плохое значение timeout: {raw['timeout']!r}") from e""", "Причина сохраняется."),
        ('return {"timeout": timeout, "debug": debug_raw == "true"}', "Строка → `bool`."),
    ],
    mistake="`bool(\"false\")` — непустая строка истинна, получится `True`."),
}
