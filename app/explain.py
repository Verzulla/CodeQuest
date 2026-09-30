"""Автоматический разбор решения по строкам: что делает каждая строка Python-кода или части команды.

Используется, когда у задания нет написанного вручную объяснения. Правила — по синтаксическому
дереву (ast): присваивания, циклы, условия, функции, классы, вызовы; плюс короткие пояснения
к операторам и встроенным функциям, которые встречаются в строке впервые.
"""
from __future__ import annotations

import ast
import json
import re
import shlex

# ---------- Python: короткие подсказки к операторам и встроенным функциям ----------

OP_NOTES = [
    (r"(?<![/*])//(?!=)", "`//` — деление нацело (без остатка)"),
    (r"%(?!=)", "`%` — остаток от деления"),   # строки уже заменены заглушкой, так что форматирование «%s» сюда не попадёт
    (r"\*\*", "`**` — возведение в степень"),
    (r"==", "`==` — проверка на равенство"),
    (r"!=", "`!=` — «не равно»"),
    (r"\bis not\b", "`is not` — это не тот же самый объект"),
    (r"\bis\b(?! not)", "`is` — тот же самый объект (часто для `None`)"),
    (r"\bnot in\b", "`not in` — значения нет в коллекции"),
    (r"(?<!not )\bin\b(?!.*:\s*$)", "`in` — проверка, есть ли значение в коллекции или строке"),
    (r"\band\b", "`and` — оба условия должны быть верны"),
    (r"\bor\b", "`or` — достаточно одного верного условия"),
    (r"\bnot\b(?! in)", "`not` — отрицание: делает истину ложью и наоборот"),
    (r"\[::-1\]", "`[::-1]` — срез с шагом −1: то же самое задом наперёд"),
    (r"\[[^\]\[]*:[^\]\[]*\]", "`[a:b]` — срез: элементы с позиции a до b (b не включается)"),
    (r"\bf\"|\bf'", "f-строка: выражения в `{}` подставляются в текст"),
    (r"\blambda\b", "`lambda` — короткая безымянная функция в одну строку"),
]
BUILTINS = {
    "print": "`print()` выводит значения на экран, через пробел",
    "len": "`len()` — длина: сколько элементов или символов",
    "range": "`range()` — последовательность чисел",
    "int": "`int()` — превращает в целое число",
    "float": "`float()` — превращает в дробное число",
    "str": "`str()` — превращает в строку",
    "bool": "`bool()` — превращает в `True`/`False`",
    "list": "`list()` — превращает в список",
    "dict": "`dict()` — создаёт словарь",
    "set": "`set()` — множество: только уникальные значения",
    "tuple": "`tuple()` — превращает в кортеж",
    "sum": "`sum()` — сумма всех элементов",
    "min": "`min()` — наименьшее значение",
    "max": "`max()` — наибольшее значение",
    "abs": "`abs()` — модуль числа (без знака)",
    "round": "`round()` — округление",
    "sorted": "`sorted()` — новый отсортированный список, исходный не меняется",
    "reversed": "`reversed()` — элементы в обратном порядке",
    "enumerate": "`enumerate()` — даёт пары (номер, элемент)",
    "zip": "`zip()` — склеивает несколько коллекций попарно",
    "map": "`map()` — применяет функцию к каждому элементу",
    "filter": "`filter()` — оставляет элементы, для которых функция вернула истину",
    "isinstance": "`isinstance()` — проверяет, что объект нужного типа",
    "type": "`type()` — тип значения",
    "input": "`input()` — читает строку, введённую пользователем",
    "open": "`open()` — открывает файл",
    "any": "`any()` — истина, если хотя бы один элемент истинный",
    "all": "`all()` — истина, если все элементы истинные",
    "super": "`super()` — обращение к родительскому классу",
    "next": "`next()` — следующий элемент итератора",
    "iter": "`iter()` — итератор по коллекции",
    "hasattr": "`hasattr()` — есть ли у объекта такой атрибут",
    "getattr": "`getattr()` — достаёт атрибут по имени",
}
METHODS = {
    "append": "добавляем {arg} в конец списка `{obj}`",
    "extend": "добавляем в конец списка `{obj}` все элементы {arg}",
    "insert": "вставляем элемент в список `{obj}` на указанную позицию",
    "pop": "достаём и удаляем элемент из `{obj}` (без аргумента — последний)",
    "remove": "удаляем из списка `{obj}` первое значение {arg}",
    "sort": "сортируем список `{obj}` на месте",
    "reverse": "разворачиваем список `{obj}` на месте",
    "index": "ищем позицию значения {arg} в `{obj}`",
    "count": "считаем, сколько раз {arg} встречается в `{obj}`",
    "copy": "делаем копию `{obj}`",
    "clear": "очищаем `{obj}`",
    "get": "берём значение по ключу {arg} из словаря `{obj}` (если ключа нет — `None` или значение по умолчанию)",
    "items": "пары (ключ, значение) словаря `{obj}`",
    "keys": "ключи словаря `{obj}`",
    "values": "значения словаря `{obj}`",
    "update": "дополняем словарь `{obj}` новыми парами",
    "setdefault": "берём значение по ключу, а если ключа нет — сначала записываем значение по умолчанию",
    "add": "добавляем {arg} в множество `{obj}`",
    "discard": "убираем {arg} из множества `{obj}`, если оно там есть",
    "split": "делим строку `{obj}` на части",
    "join": "склеиваем элементы {arg} в одну строку через `{obj}`",
    "strip": "убираем пробелы по краям строки `{obj}`",
    "lower": "переводим `{obj}` в нижний регистр",
    "upper": "переводим `{obj}` в верхний регистр",
    "replace": "заменяем часть строки `{obj}`",
    "startswith": "проверяем, начинается ли `{obj}` с {arg}",
    "endswith": "проверяем, заканчивается ли `{obj}` на {arg}",
    "find": "ищем позицию подстроки {arg} в `{obj}` (−1, если нет)",
    "format": "подставляем значения в шаблон строки",
    "read": "читаем содержимое файла целиком",
    "write": "записываем {arg} в файл",
    "readlines": "читаем файл списком строк",
}


def _src(node: ast.AST) -> str:
    try:
        s = ast.unparse(node)
    except Exception:  # noqa: BLE001
        return "…"
    return s if len(s) <= 60 else s[:57] + "…"


def _value(node: ast.AST) -> str:
    """Что за значение — простыми словами."""
    if isinstance(node, ast.List):
        return "пустой список" if not node.elts else f"список `{_src(node)}`"
    if isinstance(node, ast.Dict):
        return "пустой словарь" if not node.keys else f"словарь `{_src(node)}`"
    if isinstance(node, ast.Set):
        return f"множество `{_src(node)}`"
    if isinstance(node, ast.Tuple):
        return f"кортеж `{_src(node)}`"
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            return f"`{node.value}`"
        if isinstance(node.value, str):
            return "пустую строку" if node.value == "" else f"строку `{_src(node)}`"
        if node.value is None:
            return "`None` (пока ничего)"
        return f"число `{_src(node)}`"
    if isinstance(node, ast.ListComp):
        return f"новый список из выражения `{_src(node)}`"
    if isinstance(node, (ast.DictComp, ast.SetComp, ast.GeneratorExp)):
        return f"значения выражения `{_src(node)}`"
    if isinstance(node, ast.Call):
        return f"результат `{_src(node)}`"
    if isinstance(node, ast.Lambda):
        return f"функцию `{_src(node)}`"
    return f"`{_src(node)}`"


def _call_text(call: ast.Call) -> str | None:
    f = call.func
    if isinstance(f, ast.Name):
        if f.id == "print":
            args = ", ".join(_src(a) for a in call.args)
            extra = "".join(f", {k.arg}={_src(k.value)}" for k in call.keywords)
            return f"Выводим на экран `{args}`{extra}" if args else "Выводим пустую строку"
        return f"Вызываем `{_src(call)}`"
    if isinstance(f, ast.Attribute):
        tmpl = METHODS.get(f.attr)
        if tmpl:
            arg = f"`{_src(call.args[0])}`" if call.args else ""
            return tmpl.format(obj=_src(f.value), arg=arg or "значение").capitalize()
        return f"Вызываем метод `{f.attr}` у `{_src(f.value)}`"
    return f"Вызываем `{_src(call)}`"


def _for_text(node: ast.For | ast.AsyncFor) -> str:
    it, tgt = node.iter, _src(node.target)
    if isinstance(it, ast.Call) and isinstance(it.func, ast.Name):
        a = [_src(x) for x in it.args]
        if it.func.id == "range":
            if len(a) == 1:
                return f"Повторяем {a[0]} раз: `{tgt}` принимает значения 0, 1, … до {a[0]} − 1"
            if len(a) == 2:
                return f"Перебираем числа от {a[0]} до {a[1]} (не включая {a[1]}) — по очереди в `{tgt}`"
            if len(a) == 3:
                return f"Перебираем числа от {a[0]} до {a[1]} с шагом {a[2]} — по очереди в `{tgt}`"
        if it.func.id == "enumerate":
            return f"Перебираем элементы `{a[0] if a else '…'}` вместе с их номерами: `{tgt}`"
        if it.func.id == "zip":
            return f"Идём параллельно по {', '.join(f'`{x}`' for x in a)}: на каждом шаге по элементу из каждой — `{tgt}`"
    if isinstance(it, ast.Call) and isinstance(it.func, ast.Attribute) and it.func.attr == "items":
        return f"Перебираем пары ключ–значение словаря `{_src(it.func.value)}`: `{tgt}`"
    return f"Перебираем `{_src(it)}` по одному элементу: каждый по очереди попадает в `{tgt}`"


def _stmt_text(node: ast.stmt) -> str:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        params = [a.arg for a in node.args.args if a.arg != "self"]
        if node.args.vararg:
            params.append("*" + node.args.vararg.arg)
        if node.args.kwarg:
            params.append("**" + node.args.kwarg.arg)
        if node.name == "__init__":
            return "Конструктор: выполняется при создании объекта" + (f", получает {', '.join(f'`{p}`' for p in params)}" if params else "")
        what = "метод" if node.args.args and node.args.args[0].arg == "self" else "функцию"
        return f"Объявляем {what} `{node.name}`" + (f" с параметрами {', '.join(f'`{p}`' for p in params)}" if params else " без параметров")
    if isinstance(node, ast.ClassDef):
        base = f", наследник `{_src(node.bases[0])}`" if node.bases else ""
        return f"Объявляем класс `{node.name}`{base}"
    if isinstance(node, ast.Return):
        return "Функция возвращает " + (_value(node.value) if node.value else "`None`")
    if isinstance(node, ast.Assign):
        tg = node.targets[0]
        if isinstance(tg, ast.Tuple):
            return f"Раскладываем {_value(node.value)} сразу в несколько переменных: `{_src(tg)}`"
        if isinstance(tg, ast.Subscript):
            return f"Записываем {_value(node.value)} в `{_src(tg)}`"
        if isinstance(tg, ast.Attribute):
            return f"Сохраняем {_value(node.value)} в атрибут `{_src(tg)}`"
        return f"Создаём переменную `{_src(tg)}` и кладём в неё {_value(node.value)}"
    if isinstance(node, ast.AnnAssign):
        return f"Переменная `{_src(node.target)}` с подсказкой типа `{_src(node.annotation)}`" + (f" = {_value(node.value)}" if node.value else "")
    if isinstance(node, ast.AugAssign):
        op = {ast.Add: "Увеличиваем", ast.Sub: "Уменьшаем", ast.Mult: "Умножаем", ast.Div: "Делим"}.get(type(node.op))
        if op:
            sign = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/"}[type(node.op)]
            return f"{op} `{_src(node.target)}` на `{_src(node.value)}` (короткая запись `{_src(node.target)} = {_src(node.target)} {sign} {_src(node.value)}`)"
        return f"Обновляем `{_src(node.target)}` составным присваиванием"
    if isinstance(node, (ast.For, ast.AsyncFor)):
        return _for_text(node)
    if isinstance(node, ast.While):
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            return "Бесконечный цикл: повторяем, пока внутри не сработает `break`"
        return f"Повторяем, пока верно условие `{_src(node.test)}`"
    if hasattr(ast, "Match") and isinstance(node, ast.Match):
        return f"Сопоставляем `{_src(node.subject)}` с образцами ниже (match): сработает первый подходящий `case`"
    if isinstance(node, ast.If):
        return f"Проверяем условие `{_src(node.test)}`: если оно верно, выполняется блок ниже"
    if isinstance(node, ast.Expr):
        v = node.value
        if isinstance(v, ast.Call):
            return _call_text(v)
        if isinstance(v, ast.Constant) and isinstance(v.value, str):
            return "Строка-документация: описание функции или класса"
        if isinstance(v, (ast.Yield, ast.YieldFrom)):
            return f"Отдаём значение `{_src(v.value) if v.value is not None else 'None'}` наружу и замираем до следующего запроса (генератор)"
        return f"Вычисляем `{_src(v)}`"
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        names = ", ".join(a.name for a in node.names)
        return f"Подключаем {names}" + (f" из модуля `{node.module}`" if isinstance(node, ast.ImportFrom) and node.module else "")
    if isinstance(node, ast.Try):
        return "Пробуем выполнить блок ниже; если случится ошибка — перейдём в `except`"
    if isinstance(node, (ast.With, ast.AsyncWith)):
        items = ", ".join(_src(i.context_expr) + (f" as {_src(i.optional_vars)}" if i.optional_vars else "") for i in node.items)
        return f"Открываем `{items}` на время блока — по его окончании всё закроется автоматически"
    if isinstance(node, ast.Raise):
        return f"Выбрасываем ошибку `{_src(node.exc)}`" if node.exc else "Пробрасываем текущую ошибку дальше"
    if isinstance(node, ast.Assert):
        return f"Проверка (assert): `{_src(node.test)}` должно быть верно, иначе тест упадёт"
    if isinstance(node, ast.Pass):
        return "`pass` — ничего не делаем (пустой блок)"
    if isinstance(node, ast.Break):
        return "`break` — выходим из цикла досрочно"
    if isinstance(node, ast.Continue):
        return "`continue` — пропускаем остаток шага и переходим к следующему"
    if isinstance(node, ast.Delete):
        return f"Удаляем `{', '.join(_src(t) for t in node.targets)}`"
    if isinstance(node, (ast.Global, ast.Nonlocal)):
        kind = "глобальную" if isinstance(node, ast.Global) else "внешнюю"
        return f"Будем менять {kind} переменную {', '.join(f'`{n}`' for n in node.names)}"
    return f"Выполняем `{_src(node)}`"


def _notes(line: str, seen: set) -> list[str]:
    out = []
    code = re.sub(r"(\"[^\"]*\"|'[^']*')", '""', line.split("#")[0])   # не смотрим внутрь строк
    code = re.sub(r"\bfor\s+[\w, ()]+?\s+in\b", "for", code)            # «for x in» — это перебор, а не проверка «in»
    for pat, note in OP_NOTES:
        if note not in seen and re.search(pat, code):
            seen.add(note)
            out.append(note)
    for name in re.findall(r"\b([a-z_]+)\(", code):
        note = BUILTINS.get(name)
        if note and note not in seen and name != "print":
            seen.add(note)
            out.append(note)
    return out


def explain_python(src: str) -> list[dict]:
    """[{code, text}] — по строке кода; пустые строки пропускаются."""
    lines = src.replace("\r\n", "\n").rstrip("\n").split("\n")
    by_line: dict[int, str] = {}
    try:
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.stmt) and node.lineno not in by_line:
                by_line[node.lineno] = _stmt_text(node)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                for d in node.decorator_list:
                    by_line.setdefault(d.lineno, f"Декоратор `@{_src(d)}` — оборачивает функцию ниже, добавляя ей поведение")
            if isinstance(node, ast.ExceptHandler):
                what = f"`{_src(node.type)}`" if node.type else "любой ошибке"
                by_line[node.lineno] = f"Если случилась ошибка {what}" + (f" — она будет в переменной `{node.name}`" if node.name else "") + ", выполняем этот блок"
    except SyntaxError:
        pass
    out, seen = [], set()
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            text = "Комментарий — Python его пропускает, он для людей"
        elif re.match(r"(else|elif\b.*):\s*$", s) or s.startswith("elif "):
            text = "Иначе проверяем следующее условие" if s.startswith("elif") else "Иначе (если условия выше не сработали) — выполняется блок ниже"
        elif s.startswith("case "):
            pat = s[5:].rstrip(":").strip()
            text = "Иначе, если ничего выше не подошло (`case _`)" if pat == "_" else f"Вариант: значение подходит под образец `{pat}`"
        elif s.startswith("finally"):
            text = "Этот блок выполнится в любом случае — была ошибка или нет"
        elif i in by_line:
            text = by_line[i]
        else:
            text = "Продолжение выражения с предыдущей строки"
        notes = _notes(line, seen)
        out.append({"code": line, "text": text, "notes": notes})
    return out


# ---------- Команды терминала ----------

PROGRAMS = {
    "git": "git — система контроля версий", "docker": "docker — контейнеры", "pytest": "pytest — запуск тестов",
    "python": "python — интерпретатор Python", "python3": "python3 — интерпретатор Python", "pip": "pip — установщик пакетов Python",
    "ls": "ls — список файлов", "cd": "cd — перейти в папку", "mkdir": "mkdir — создать папку", "rm": "rm — удалить",
    "cp": "cp — скопировать", "mv": "mv — переместить или переименовать", "cat": "cat — вывести содержимое файла",
    "grep": "grep — поиск строк по шаблону", "touch": "touch — создать пустой файл", "chmod": "chmod — права доступа",
    "echo": "echo — вывести текст", "pwd": "pwd — где я сейчас", "curl": "curl — HTTP-запрос из терминала",
    "head": "head — первые строки файла", "tail": "tail — последние строки файла", "find": "find — поиск файлов",
    "wc": "wc — посчитать строки/слова", "sort": "sort — отсортировать строки", "uv": "uv — менеджер пакетов Python",
    "allure": "allure — отчёты о тестах", "ruff": "ruff — проверка и форматирование кода Python", "gh": "gh — работа с GitHub из терминала",
    "pre-commit": "pre-commit — проверки перед каждым коммитом", "sudo": "sudo — выполнить команду от имени администратора",
    "ps": "ps — список запущенных процессов", "kill": "kill — остановить процесс", "which": "which — где лежит программа", "chown": "chown — сменить владельца файлов", "playwright": "playwright — браузеры для UI-тестов", "source": "source — выполнить скрипт в текущей оболочке",
}
SUBCOMMANDS = {
    ("git", "init"): "создаём новый репозиторий в текущей папке", ("git", "clone"): "скачиваем копию репозитория",
    ("git", "status"): "показываем, что изменено и что добавлено в коммит", ("git", "add"): "добавляем изменения в следующий коммит",
    ("git", "commit"): "сохраняем снимок изменений (коммит)", ("git", "push"): "отправляем коммиты на сервер",
    ("git", "pull"): "забираем новые коммиты с сервера", ("git", "fetch"): "скачиваем изменения с сервера, не сливая их",
    ("git", "log"): "показываем историю коммитов", ("git", "diff"): "показываем разницу в изменениях",
    ("git", "branch"): "работа с ветками", ("git", "checkout"): "переключаемся на ветку или коммит",
    ("git", "switch"): "переключаемся на ветку", ("git", "merge"): "сливаем другую ветку в текущую",
    ("git", "rebase"): "переносим коммиты поверх другой ветки", ("git", "stash"): "откладываем незакоммиченные изменения",
    ("git", "reset"): "откатываем изменения", ("git", "restore"): "возвращаем файл к сохранённому состоянию",
    ("git", "revert"): "создаём коммит, отменяющий другой", ("git", "remote"): "настраиваем удалённые репозитории",
    ("git", "tag"): "ставим метку на коммит", ("git", "show"): "показываем содержимое коммита",
    ("git", "cherry-pick"): "переносим один коммит в текущую ветку", ("git", "blame"): "кто и когда менял строки файла",
    ("docker", "run"): "запускаем контейнер из образа", ("docker", "build"): "собираем образ по Dockerfile",
    ("docker", "ps"): "список запущенных контейнеров", ("docker", "images"): "список образов",
    ("docker", "exec"): "выполняем команду внутри работающего контейнера", ("docker", "stop"): "останавливаем контейнер",
    ("docker", "rm"): "удаляем контейнер", ("docker", "rmi"): "удаляем образ", ("docker", "logs"): "показываем вывод контейнера",
    ("docker", "pull"): "скачиваем образ", ("docker", "compose"): "управляем несколькими контейнерами по compose-файлу",
    ("pip", "install"): "устанавливаем пакет", ("pip", "uninstall"): "удаляем пакет", ("pip", "freeze"): "список установленных пакетов с версиями",
    ("pip", "list"): "список установленных пакетов", ("uv", "add"): "добавляем зависимость в проект", ("uv", "run"): "запускаем команду в окружении проекта",
    ("allure", "serve"): "собираем отчёт и открываем в браузере", ("allure", "generate"): "собираем HTML-отчёт",
    ("playwright", "install"): "скачиваем браузеры для тестов",
    ("ruff", "check"): "ищем ошибки и нарушения стиля", ("ruff", "format"): "форматируем код",
    ("gh", "pr"): "работа с pull request", ("gh", "run"): "запуски GitHub Actions",
    ("pre-commit", "install"): "включаем проверки перед коммитом", ("pre-commit", "run"): "запускаем проверки вручную",
}
FLAGS = {
    "-m": "сообщение коммита (или запуск модуля у python)", "-a": "все файлы / все элементы", "-b": "создать новую ветку и сразу перейти в неё",
    "-d": "в фоне (у docker) / удалить (у git branch)", "-D": "удалить принудительно", "-p": "проброс порта (у docker) / создать вложенные папки (у mkdir)",
    "-v": "подробный вывод (у pytest) / подключить папку (у docker)", "-k": "запустить тесты, в имени которых есть выражение",
    "-x": "остановиться на первом упавшем тесте", "-q": "краткий вывод", "-s": "показывать print из тестов",
    "-r": "рекурсивно, во всех вложенных папках (у pip — из файла)", "-f": "принудительно, без вопросов", "-rf": "рекурсивно и без вопросов",
    "-la": "подробный список, включая скрытые файлы", "-l": "подробный список", "-n": "номера строк", "-i": "без учёта регистра",
    "-it": "интерактивно, с терминалом", "-t": "имя (тег) образа", "-e": "переменная окружения", "-u": "запомнить ветку на сервере (upstream)",
    "--oneline": "каждый коммит одной строкой", "--hard": "жёстко: изменения в файлах тоже пропадут", "--soft": "мягко: изменения остаются",
    "--name": "имя контейнера", "--rm": "удалить контейнер после остановки", "--lf": "перезапустить только упавшие в прошлый раз тесты",
    "--maxfail": "остановиться после N падений", "--alluredir": "куда складывать результаты для Allure", "--staged": "только добавленное в коммит",
    "--all": "все", "--force": "принудительно", "--no-ff": "всегда создавать коммит слияния", "--amend": "исправить последний коммит",
    "-X": "HTTP-метод запроса", "-H": "заголовок запроса", "--graph": "показать ветки графом", "-c": "выполнить строку кода",
    "-h": "в удобочитаемом виде", "--collect-only": "только найти тесты и показать список, не запуская их",
    "-R": "рекурсивно, для всей папки", "--tb": "как подробно показывать ошибки", "-W": "что делать с предупреждениями",
    "--cov": "замерить покрытие кода тестами", "-S": "записать пакет в зависимости", "--dev": "зависимость только для разработки",
    "--fix": "сразу исправить найденное", "-y": "отвечать «да» на все вопросы", "--global": "настройка для всех репозиториев", "--version": "показать версию", "--headed": "показывать окно браузера",
}


FLAGS_BY_PROG = {
    ("tail", "-n"): "сколько последних строк показать", ("head", "-n"): "сколько первых строк показать",
    ("grep", "-n"): "показывать номера строк", ("grep", "-c"): "только количество совпадений", ("grep", "-v"): "строки, где совпадения НЕТ",
    ("sort", "-n"): "сортировать как числа", ("sort", "-r"): "в обратном порядке", ("wc", "-l"): "посчитать строки",
    ("git", "-m"): "сообщение коммита", ("python", "-m"): "запустить модуль как программу", ("python3", "-m"): "запустить модуль как программу",
    ("pytest", "-m"): "запустить тесты с этой меткой", ("docker", "-p"): "проброс порта: снаружи:внутри контейнера",
    ("docker", "-v"): "подключить папку внутрь контейнера", ("pytest", "-v"): "подробный вывод: каждый тест отдельной строкой",
    ("mkdir", "-p"): "создать и все недостающие папки на пути", ("git", "-d"): "удалить ветку", ("docker", "-d"): "запустить в фоне",
    ("cp", "-r"): "копировать папку целиком", ("rm", "-r"): "удалить папку целиком", ("pip", "-r"): "установить всё из файла со списком",
    ("ls", "-a"): "показать и скрытые файлы", ("git", "-a"): "все ветки (или все изменённые файлы)",
}
VALUE_FLAGS = {"-m", "-p", "-v", "-k", "-t", "-e", "--name", "-X", "-H", "--maxfail", "--alluredir", "-c", "-n", "-r", "-o", "-f", "-w"}


def _arg_text(a: str) -> str:
    if re.match(r"https?://", a):
        return f"адрес `{a}`"
    if re.fullmatch(r"-?\d+", a):
        return f"число {a}"
    if "*" in a:
        return f"шаблон `{a}` — все подходящие файлы"
    if a.endswith("/") or ("/" in a and "." not in a.rsplit("/", 1)[-1]):
        return f"папка `{a}`"
    if re.search(r"\.[a-zA-Z0-9]{1,5}$", a):
        return f"файл `{a}`"
    if a in (".", "./"):
        return "текущая папка (`.`)"
    return f"значение `{a}`"


def explain_command(cmd: str) -> list[dict]:
    """Разбор первой команды: программа, подкоманда, флаги, аргументы — каждая часть своей строкой."""
    first = cmd.strip().splitlines()[0] if cmd.strip() else ""
    try:
        parts = shlex.split(first)
    except ValueError:
        parts = first.split()
    if not parts:
        return []
    out = []
    prog = parts[0]
    desc = PROGRAMS.get(prog, "программа, которую запускаем")
    desc = desc.split(" — ", 1)[1] if desc.startswith(prog + " — ") else desc
    out.append({"code": prog, "text": desc[0].upper() + desc[1:], "notes": []})
    rest = parts[1:]
    if prog == "sudo" and rest:                      # sudo <команда>: разбираем саму команду
        return out + explain_command(shlex.join(rest))
    if rest and not rest[0].startswith("-"):
        sub = SUBCOMMANDS.get((prog, rest[0]))
        if sub or prog in ("git", "docker", "pip", "uv", "allure", "playwright"):
            out.append({"code": rest[0], "text": (sub or "подкоманда").capitalize(), "notes": []})
            rest = rest[1:]
    i = 0
    while i < len(rest):
        p = rest[i]
        if p.startswith("-"):
            key = p.split("=")[0]
            text = FLAGS_BY_PROG.get((prog, key)) or FLAGS.get(key) or FLAGS.get(p) or "опция команды"
            if "=" in p:
                out.append({"code": p, "text": f"{text.capitalize()}: `{p.split('=', 1)[1]}`", "notes": []})
            elif i + 1 < len(rest) and key in VALUE_FLAGS and (prog, key) not in (("pytest", "-v"), ("ls", "-a"), ("git", "-a"), ("docker", "-d"), ("git", "-d"), ("mkdir", "-p"), ("cp", "-r"), ("rm", "-r"), ("grep", "-n"), ("grep", "-c"), ("grep", "-v"), ("sort", "-n"), ("sort", "-r"), ("wc", "-l")) and not rest[i + 1].startswith("-"):
                out.append({"code": f"{p} {rest[i + 1]}", "text": f"{text.capitalize()}: `{rest[i + 1]}`", "notes": []})
                i += 1
            else:
                out.append({"code": p, "text": text.capitalize(), "notes": []})
        else:
            sub = out[1]["code"] if len(out) > 1 else ""
            t = (f"ветка `{p}`" if prog == "git" and sub in ("branch", "checkout", "switch", "merge", "rebase") and not re.search(r"\.\w+$", p)
                 else f"образ `{p}`" if prog == "docker" and sub in ("run", "pull", "rmi") and i == len(rest) - 1
                 else _arg_text(p))
            out.append({"code": p, "text": t[0].upper() + t[1:], "notes": []})
        i += 1
    return out


def explain(ex) -> dict:
    """Разбор для задания. Если у задания есть ручной разбор (JSON в ex["explain"]) — он:
    {manual, idea, lines, trace, mistake}; строки, которые автор не расписал, — из автоматического.
    Иначе автоматический: {lines, summary}."""
    auto = _auto(ex)
    raw = ex["explain"] if "explain" in ex.keys() else ""
    if not raw:
        return auto
    m = json.loads(raw)
    # не расписал строки — берём автоматические; но если есть таблица шагов, она их заменяет
    lines = [{"code": c, "text": t, "notes": []} for c, t in m.get("lines", [])] or ([] if m.get("trace") else auto["lines"])
    return {"manual": True, "idea": m.get("idea", ""), "lines": lines, "trace": m.get("trace", []),
            "mistake": m.get("mistake", ""), "summary": m.get("summary", "")}


def _auto(ex) -> dict:
    t = ex["type"]
    if t == "command":
        answer = (ex["solution"] or ex["expected_output"] or "").strip().splitlines()[0] if (ex["solution"] or ex["expected_output"]) else ""
        head = answer.split()[0] if answer.split() else ""
        if head in PROGRAMS:
            return {"lines": explain_command(answer),
                    "summary": "Команда целиком — это программа, затем (если есть) подкоманда, потом опции и аргументы."}
        # Вопрос про вывод команд из условия: разбираем сами команды (строки с «$»), ответ — в итоге
        lines = []
        for ln in (ex["code"] or "").splitlines():
            if ln.startswith("$ "):
                sub = explain_command(ln[2:])
                if sub:
                    lines.append({"code": ln[2:], "text": sub[0]["text"] + ("" if len(sub) == 1 else ": " + "; ".join(
                        (x['text'][0].lower() + x['text'][1:]) if x['text'].lower().endswith(f"`{x['code']}`".lower()) else f"`{x['code']}` — {x['text'][0].lower() + x['text'][1:]}" for x in sub[1:])), "notes": []})
        return {"lines": lines, "summary": f"Поэтому ответ: `{answer}`." if answer else ""}
    if t == "output":
        lines = explain_python(ex["code"] or "")
        # Простая программа без циклов и функций: каждый print — одна строка вывода, покажем её прямо у print
        out_lines = (ex["expected_output"] or "").split("\n")
        try:
            tree = ast.parse(ex["code"] or "")
            simple = not any(isinstance(n, (ast.For, ast.While, ast.FunctionDef, ast.ClassDef, ast.If, ast.Try, ast.With)) for n in ast.walk(tree))
            prints = [n.lineno for n in tree.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                      and isinstance(n.value.func, ast.Name) and n.value.func.id == "print" and not n.value.keywords]
        except SyntaxError:
            simple, prints = False, []
        if simple and prints and len(prints) == len(out_lines):
            src_lines = (ex["code"] or "").replace("\r\n", "\n").split("\n")
            by_code = {}
            for no, out in zip(prints, out_lines):
                by_code.setdefault(src_lines[no - 1], []).append(out)
            for item in lines:
                outs = by_code.get(item["code"])
                if outs:
                    item["text"] += f" → на экране: `{outs.pop(0)}`"
        return {"lines": lines, "summary": "Программа выполняется сверху вниз; всё, что выводит `print`, и есть ответ."}
    lines = explain_python(ex["solution"] or "")
    return {"lines": lines, "summary": ""}
