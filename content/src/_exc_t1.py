"""Теория модуля «Ошибки и их перехват» темы «Исключения».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- exc-m1-l1 ----------
'exc-m1-l1': dict(
    full=t(r'''
## Зачем это нужно

Программы постоянно сталкиваются с проблемами: пользователь ввёл буквы вместо числа, сервер вернул пустой ответ, в словаре нет нужного ключа. В Python такая ситуация называется **исключением** (exception). Если его не обработать, программа останавливается с сообщением об ошибке. Умение перехватывать исключения делает код надёжным, а тестировщику помогает понимать, **что именно** пошло не так.

## Частые исключения

```python
checks = [
    lambda: int("abc"),
    lambda: 1 / 0,
    lambda: [1, 2][5],
    lambda: {"a": 1}["b"],
    lambda: "5" + 5,
]
for check in checks:
    try:
        check()
    except Exception as e:
        print(type(e).__name__)
```

- `ValueError` — значение подходящего типа, но неверное: `int("abc")`.
- `ZeroDivisionError` — деление на ноль.
- `IndexError` — индекса нет в списке.
- `KeyError` — ключа нет в словаре.
- `TypeError` — операция с неподходящим типом: строка + число.
- Ещё встречаются `NameError` (имя не определено), `AttributeError` (у объекта нет атрибута/метода).
- `type(e).__name__` — имя класса исключения. Вывод: пять имён по порядку.

## Исключение останавливает выполнение

```python
def risky():
    print("до ошибки")
    x = 1 / 0
    print("после ошибки")

try:
    risky()
except ZeroDivisionError:
    print("поймали")
print("программа продолжается")
```

- Как только возникло исключение, выполнение функции **прерывается**: «после ошибки» не печатается.
- Исключение «летит» наружу по цепочке вызовов, пока его не перехватят. Здесь его поймал `except` снаружи функции.
- Если бы перехвата не было, программа завершилась бы и напечатала **трассировку** (traceback): список вызовов, строку с ошибкой и её тип с текстом.
- Вывод: `до ошибки`, `поймали`, `программа продолжается`.

## Текст ошибки

```python
for text in ["12", "x"]:
    try:
        print(int(text))
    except ValueError as e:
        print("ошибка:", e)
```

- `except ... as e` — сохранить объект исключения в переменную `e`. `print(e)` или `str(e)` — его текст.
- Вывод: `12`, `ошибка: invalid literal for int() with base 10: 'x'`.

## Безопасные версии операций

```python
def safe_int(text):
    try:
        return int(text)
    except ValueError:
        return None

print(safe_int("42"), safe_int("x"))
```

- Частый приём: попробовать, а при ошибке вернуть запасное значение. Вывод: `42 None`.

## Итог

- Исключение — сигнал о проблеме; без перехвата программа останавливается с трассировкой.
- Частые: `ValueError`, `TypeError`, `KeyError`, `IndexError`, `ZeroDivisionError`, `NameError`, `AttributeError`.
- `try: ... except Тип as e:` — перехват; `str(e)` — текст, `type(e).__name__` — тип.
- После исключения остаток кода в `try` не выполняется.
'''),
    short=t(r'''
```py
try:
    n = int(text)
except ValueError as e:
    print("ошибка:", e)      # текст ошибки
type(e).__name__             # имя типа
# ValueError, TypeError, KeyError, IndexError,
# ZeroDivisionError, NameError, AttributeError
```
'''),
    quiz=[
        q('Какое исключение даст `[1, 2][10]`?',
            ['KeyError', 'IndexError', 'ValueError', 'TypeError'],
            1, 'Индекса нет в списке.'),
        q('Какое исключение даст `int("abc")`?',
            ['TypeError', 'ValueError', 'NameError', 'KeyError'],
            1, 'Тип подходит (строка), значение — нет.'),
        q('Что происходит с остатком кода в `try` после исключения?',
            ['Выполняется', 'Пропускается', 'Выполняется после except', 'Зависит от типа'],
            1, 'Управление сразу переходит в except.'),
    ],
),

# ---------- exc-m1-l2 ----------
'exc-m1-l2': dict(
    full=t(r'''
## Зачем это нужно

Одна операция может упасть по разным причинам, и реагировать на них нужно по-разному: «не число» — попросить ввести заново, «деление на ноль» — вернуть особое значение. У `try` может быть несколько `except`, и один `except` может ловить несколько типов.

## Несколько except

```python
def parse(text):
    try:
        return 100 / int(text)
    except ValueError:
        return "не число"
    except ZeroDivisionError:
        return "деление на ноль"

print(parse("4"), parse("x"), parse("0"))
```

- Python проверяет `except` **по порядку** и выполняет первый подходящий.
- Вывод: `25.0 не число деление на ноль`.

## Кортеж типов

```python
def lookup(data, key):
    try:
        return data[key]
    except (KeyError, IndexError, TypeError) as e:
        return f"не найдено ({type(e).__name__})"

print(lookup({"a": 1}, "b"), lookup([1], 3), lookup(None, 0))
```

- `except (A, B, C)` — одна реакция на несколько типов. Скобки обязательны.
- `None[0]` — `TypeError`: объект не поддерживает индексацию.
- Вывод: `не найдено (KeyError) не найдено (IndexError) не найдено (TypeError)`.

## Неперехваченное летит дальше

```python
def inner():
    try:
        return [][0]
    except KeyError:
        return "KeyError"

try:
    inner()
except IndexError:
    print("IndexError поймали снаружи")
```

- `except KeyError` не ловит `IndexError` — исключение выходит из функции и ловится выше.
- Вывод: `IndexError поймали снаружи`.

## Лови конкретные типы

```python
def read_config(config, key):
    try:
        return int(config[key])
    except KeyError:
        return f"нет ключа {key}"
    except ValueError:
        return f"плохое значение {key}"

cfg = {"port": "8080", "host": "x"}
print(read_config(cfg, "port"), read_config(cfg, "timeout"), read_config(cfg, "host"))
```

- Каждая причина — своё понятное сообщение. Вывод: `8080 нет ключа timeout плохое значение host`.

Почему не ловить всё подряд:
- `except Exception:` прячет и **баги** — опечатку в имени (`NameError`), неверный тип. Программа «работает», но неправильно.
- Голый `except:` без типа ловит даже `KeyboardInterrupt` (Ctrl+C) — программу нельзя остановить. Так писать не надо.
- Ловить широко допустимо на «границе» программы: записать ошибку в лог, показать пользователю сообщение, продолжить обработку следующего элемента.

## Итог

- Несколько `except` — проверяются по порядку, срабатывает первый подходящий.
- `except (A, B) as e` — несколько типов сразу.
- Неподходящее исключение летит дальше по вызовам.
- Лови конкретные типы; `except Exception` — только осознанно; голый `except:` — нет.
'''),
    short=t(r'''
```py
try:
    return 100 / int(text)
except ValueError:
    return "не число"
except ZeroDivisionError:
    return "деление на ноль"
except (KeyError, IndexError) as e: ...   # несколько типов
except Exception: ...                     # широко — осознанно
except: ...                               # НЕ надо (ловит и Ctrl+C)
```
'''),
    quiz=[
        q('Какой except сработает при ошибке, если подходят несколько?',
            ['Последний', 'Первый подходящий по порядку', 'Все', 'Самый точный'],
            1, 'Порядок важен.'),
        q('Как поймать KeyError и IndexError одним блоком?',
            ['`except KeyError, IndexError:`', '`except (KeyError, IndexError):`', '`except KeyError or IndexError:`', 'Нельзя'],
            1, 'Кортеж в скобках.'),
        q('Почему опасен голый `except:`?',
            ['Он медленный', 'Ловит всё, включая Ctrl+C и баги', 'Не работает', 'Требует as'],
            1, 'Прячет проблемы.'),
    ],
),

# ---------- exc-m1-l3 ----------
'exc-m1-l3': dict(
    full=t(r'''
## Зачем это нужно

Кроме `try` и `except` есть ещё два блока. `else` — код, который выполняется, **если ошибки не было**. `finally` — код, который выполняется **всегда**: уборка, закрытие ресурсов, запись в лог. В автотестах `finally` гарантирует, что браузер закроется, а тестовые данные удалятся, даже если тест упал.

## Порядок блоков

```python
def run(text):
    try:
        n = int(text)
    except ValueError:
        print("except")
    else:
        print("else", n)
    finally:
        print("finally")

run("5")
run("x")
```

- Успех: `try` → `else` → `finally`. Ошибка: `try` → `except` → `finally`.
- Вывод: `else 5`, `finally`, `except`, `finally`.

## Зачем else

В `try` стоит держать **только** код, который может упасть с ожидаемой ошибкой. Всё, что должно выполниться после успеха, — в `else`. Иначе `except` случайно поймает ошибку из «хорошего» кода.

```python
def parse_and_double(text):
    try:
        n = int(text)
    except ValueError:
        return None
    else:
        return n * 2

print(parse_and_double("4"), parse_and_double("x"))
```

Вывод: `8 None`.

## finally выполняется всегда

```python
def f():
    try:
        return "из try"
    finally:
        print("finally выполнился")

print(f())
```

- Даже `return` не отменяет `finally`: сначала выполняется `finally`, потом функция возвращает значение.
- Вывод: `finally выполнился`, `из try`.

```python
def g():
    try:
        raise KeyError("x")
    finally:
        print("уборка")

try:
    g()
except KeyError:
    print("ошибка дошла наружу")
```

- `try/finally` без `except`: уборка выполнится, а исключение полетит дальше.
- `raise KeyError("x")` — выбросить исключение самому (урок «raise»).
- Вывод: `уборка`, `ошибка дошла наружу`.

## Ресурс, который нужно закрыть

```python
resource = {"open": False}

def use(action):
    resource["open"] = True
    try:
        return action()
    finally:
        resource["open"] = False

try:
    use(lambda: 1 / 0)
except ZeroDivisionError:
    print("упало, но ресурс закрыт:", resource["open"] is False)
```

- Так работают файлы, соединения, браузеры в тестах. Удобная запись того же — `with` (тема «Контекстные менеджеры»).
- Вывод: `упало, но ресурс закрыт: True`.

## Итог

- `else` — если ошибки не было; держи в `try` минимум кода.
- `finally` — всегда: при успехе, ошибке, `return`.
- `try/finally` без `except` — уборка без перехвата.
- Порядок: `try` → `except`… → `else` → `finally`.
'''),
    short=t(r'''
```py
try:
    n = int(text)        # только то, что может упасть
except ValueError:
    ...                  # при ошибке
else:
    ...                  # если ошибки НЕ было
finally:
    ...                  # ВСЕГДА (даже при return)
```
'''),
    quiz=[
        q('Когда выполняется `else` у try?',
            ['Всегда', 'Если в try не было исключения', 'При исключении', 'Никогда'],
            1, 'Успешная ветка.'),
        q('Выполнится ли `finally`, если в `try` стоит `return`?',
            ['Нет', 'Да — перед возвратом', 'Только при ошибке', 'Ошибка синтаксиса'],
            1, 'finally выполняется всегда.'),
        q('Можно ли написать `try/finally` без `except`?',
            ['Нет', 'Да — исключение пройдёт дальше после уборки', 'Только с else', 'Только в функции'],
            1, 'Уборка без перехвата.'),
    ],
),

# ---------- exc-m1-l4 ----------
'exc-m1-l4': dict(
    full=t(r'''
## Зачем это нужно

Исключения в Python образуют **иерархию** классов: `KeyError` и `IndexError` — разновидности `LookupError`, а все обычные ошибки — разновидности `Exception`. `except` ловит указанный класс **и всех его потомков**. Понимание иерархии объясняет, почему порядок `except` важен и почему `except Exception` ловит почти всё.

## Родственные связи

```python
print(issubclass(KeyError, LookupError), issubclass(IndexError, LookupError))
print(issubclass(ZeroDivisionError, ArithmeticError), issubclass(ValueError, Exception))
print(issubclass(KeyboardInterrupt, Exception))
```

- `issubclass(A, B)` — является ли класс `A` разновидностью `B`.
- Часть иерархии:
  - `BaseException` — корень всего;
  - `Exception` — все «обычные» ошибки;
  - `LookupError` → `KeyError`, `IndexError`;
  - `ArithmeticError` → `ZeroDivisionError`, `OverflowError`;
  - `KeyboardInterrupt`, `SystemExit` — наследники `BaseException`, **не** `Exception`: поэтому `except Exception` не мешает остановить программу по Ctrl+C.
- Вывод: `True True`, `True True`, `False`.

## Базовый класс ловит потомков

```python
for bad in [lambda: {}["x"], lambda: [][1]]:
    try:
        bad()
    except LookupError as e:
        print("LookupError поймал", type(e).__name__)
```

- Один `except LookupError` перехватывает и `KeyError`, и `IndexError`. Вывод: `LookupError поймал KeyError`, `LookupError поймал IndexError`.

## Порядок except: от частного к общему

```python
try:
    {}["x"]
except LookupError:
    print("сработал LookupError")
except KeyError:
    print("сработал KeyError")
```

- Первым стоит более общий `LookupError` — он перехватывает `KeyError`, и второй блок **никогда** не сработает.
- Правило: частные типы — выше, общие — ниже. Вывод: `сработал LookupError`.

```python
def classify(func):
    try:
        func()
    except LookupError:
        return "lookup"
    except ArithmeticError:
        return "math"
    except Exception:
        return "other"
    return "ok"

print(classify(lambda: {}["x"]), classify(lambda: 1 / 0), classify(lambda: int("x")), classify(lambda: 1))
```

Вывод: `lookup math other ok`.

## Цепочка предков

```python
print([cls.__name__ for cls in KeyError.__mro__])
print(isinstance(KeyError("x"), LookupError))
```

- `__mro__` — кортеж классов от самого класса до `object` (порядок поиска методов, тема «Классы»).
- `isinstance(объект, Класс)` — проверка для **объекта** исключения (например, пойманного в `except Exception as e`).
- Вывод: `['KeyError', 'LookupError', 'Exception', 'BaseException', 'object']`, `True`.

## Итог

- Исключения — иерархия классов; `except X` ловит `X` и всех потомков.
- `Exception` — база обычных ошибок; `KeyboardInterrupt` в неё не входит.
- `LookupError` ⊃ `KeyError`, `IndexError`; `ArithmeticError` ⊃ `ZeroDivisionError`.
- `except` — от частного к общему.
- `issubclass` — для классов, `isinstance` — для объектов.
'''),
    short=t(r'''
```py
# BaseException
#   Exception
#     LookupError: KeyError, IndexError
#     ArithmeticError: ZeroDivisionError
#     ValueError, TypeError, ...
#   KeyboardInterrupt, SystemExit   (не Exception!)
except LookupError: ...      # ловит KeyError и IndexError
# порядок except: частное -> общее
issubclass(KeyError, LookupError); isinstance(e, LookupError)
```
'''),
    quiz=[
        q('Поймает ли `except LookupError` ошибку `KeyError`?',
            ['Нет', 'Да — KeyError его потомок', 'Только с as', 'Только в Python 2'],
            1, 'except ловит потомков.'),
        q('Почему `except Exception` не мешает остановить программу по Ctrl+C?',
            ['Ctrl+C не исключение', 'KeyboardInterrupt наследует BaseException, а не Exception', 'Python это блокирует', 'Мешает'],
            1, 'Он вне ветки Exception.'),
        q('Как расставлять except?',
            ['От общего к частному', 'От частного к общему', 'По алфавиту', 'Не важно'],
            1, 'Иначе частный блок не сработает.'),
    ],
),
}
