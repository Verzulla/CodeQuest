"""Расчёт интерактивных схем при сборке: код из схемы выполняется настоящим Python,
и шаги (строки, переменные, вывод, объекты в памяти) берутся из реального выполнения,
а не пишутся руками. Так схема никогда не разойдётся с тем, что сделает Python.

Схема с "auto": true в блоке ```viz:
- trace  — шаги «строка → переменные → вывод»; notes: {"5": "…", "5#2": "…"} — пояснения к строке (n-му её выполнению);
- memory — то же, но с объектами в памяти (имена → объекты, списки, словари, объекты классов);
- paths  — cases: [{"label", "setup" | "code"}]: какие строки выполнились при каждом варианте;
- comp   — presets: [{"label", "var", "items", "expr", "cond"}]: включение по элементам;
- sortkey — items и keys: [{"label", "key"}]: ключ сортировки для каждого элемента.

Код схем пишем мы сами (учебные примеры), поэтому он выполняется прямо в процессе сборки."""
import contextlib
import io
import os
import sys
import tempfile
import types

FILE = "<viz>"
MAX_EVENTS = 5000


def short(v, n=48):
    if isinstance(v, (types.FunctionType, types.BuiltinFunctionType)):
        return f"функция {v.__qualname__.replace('.<locals>', '')}"
    if isinstance(v, types.GeneratorType):
        return f"генератор {v.__qualname__.replace('.<locals>', '')}"
    r = repr(v)
    if " object at 0x" in r:      # repr по умолчанию с адресом в памяти — ученику он ничего не говорит
        r = f"объект {type(v).__name__}"
    return r if len(r) <= n else r[: n - 1] + "…"


def _visible(name, value):
    return not name.startswith("_") and not isinstance(value, (types.ModuleType, types.FunctionType, type, types.BuiltinFunctionType))


@contextlib.contextmanager
def _sandbox():
    """Временная папка (для заданий с файлами) и перехват вывода."""
    old = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            yield
        finally:
            os.chdir(old)


def _err_text(e):
    return f"{type(e).__name__}: {e}" if str(e) else type(e).__name__


def _run(code, tracer, setup=""):
    """Выполнить setup (без трассировки) и code (с трассировкой). Возвращает (вывод, ошибка, globals)."""
    g = {"__name__": "__main__"}
    buf = io.StringIO()
    err = None
    with _sandbox(), contextlib.redirect_stdout(buf):
        if setup:
            exec(compile(setup, "<setup>", "exec"), g)
        compiled = compile(code, FILE, "exec")
        sys.settrace(tracer)
        try:
            exec(compiled, g)
        except Exception as e:  # noqa: BLE001 — ошибка — тоже результат для схемы
            err = _err_text(e)
        finally:
            sys.settrace(None)
    return buf, err, g


# ---------- trace / memory: шаги ----------

def _frames(frame):
    """Цепочка кадров кода схемы от внешнего к текущему."""
    chain = []
    f = frame
    while f is not None:
        if f.f_code.co_filename == FILE:
            chain.append(f)
        f = f.f_back
    return chain[::-1]


def _label_frames(chain):
    """Подписи кадров функций: «fact» или «fact #2» при рекурсии."""
    labels, seen = [], {}
    for f in chain:
        if f.f_code.co_name == "<module>":
            labels.append("")
            continue
        name = f.f_code.co_name
        seen[name] = seen.get(name, 0) + 1
        labels.append(name if seen[name] == 1 else f"{name} #{seen[name]}")
    return labels


def _record_steps(code, setup="", snapshot=None):
    """Общий движок: шаг — после выполнения каждой строки кода схемы."""
    steps = []
    pending = {}          # кадр → номер строки, которая сейчас выполняется
    raising = set()       # кадры, из которых летит исключение
    events = [0]
    buf_holder = {}

    def finalize(frame, line, ret=None):
        chain = _frames(frame)
        caller = chain[-2] if len(chain) > 1 else None
        buf = buf_holder["buf"]
        out = buf.getvalue()
        new = out[buf_holder["pos"]:]
        buf_holder["pos"] = len(out)
        step = {"line": line, "call": pending.get(caller) if caller is not None else None,
                "out": new, "snap": snapshot(chain)}
        if ret is not None:
            step["ret"] = ret
        steps.append(step)

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != FILE:
            return None
        events[0] += 1
        if events[0] > MAX_EVENTS:
            raise RuntimeError("схема: слишком много шагов")
        if event == "line":
            raising.discard(frame)
            if frame in pending:
                finalize(frame, pending[frame])
            pending[frame] = frame.f_lineno
        elif event == "return":
            if frame in pending:
                name = frame.f_code.co_name
                inner = name == "<module>" or name.startswith("<")
                gen = frame.f_code.co_flags & 0x20      # CO_GENERATOR: return-событие — это yield
                ret = None if inner else (f"↯ {name}() прервана исключением" if frame in raising
                                          else f"⏸ {name}() отдала {short(arg)} через yield" if gen
                                          else f"↩ {name}() вернула {short(arg)}")
                finalize(frame, pending.pop(frame), ret)
        elif event == "exception":
            raising.add(frame)
        return tracer

    # вывод нужен по ходу выполнения — подменяем redirect вручную
    g = {"__name__": "__main__"}
    buf = io.StringIO()
    buf_holder.update(buf=buf, pos=0)
    err = None
    with _sandbox(), contextlib.redirect_stdout(buf):
        if setup:
            exec(compile(setup, "<setup>", "exec"), g)
            buf_holder["pos"] = len(buf.getvalue())
        compiled = compile(code, FILE, "exec")
        sys.settrace(tracer)
        try:
            exec(compiled, g)
        except Exception as e:  # noqa: BLE001
            err = _err_text(e)
        finally:
            sys.settrace(None)
    if err:
        last_line = steps[-1]["line"] if steps else 1
        # строка, на которой упало, — последняя незавершённая; состояние — на момент ошибки
        line = list(pending.values())[-1] if pending else last_line
        module = types.SimpleNamespace(f_locals=g, f_code=types.SimpleNamespace(co_name="<module>"))
        steps.append({"line": line, "call": None, "out": err, "snap": snapshot([module]), "error": True})
    return steps


def _var_snapshot(hide):
    def snap(chain):
        labels = _label_frames(chain)
        res = {}
        for f, label in zip(chain, labels):
            for name, value in f.f_locals.items():
                if name in hide or not _visible(name, value):
                    continue
                key = name if not label else f"{name} · {label}"
                res[key] = short(value)
        return res
    return snap


def _diff(prev, cur):
    d = {k: v for k, v in cur.items() if prev.get(k) != v}
    d.update({k: None for k in prev if k not in cur})
    return d


def _attach_notes(steps, notes, field="note"):
    count = {}
    for st in steps:
        count[st["line"]] = count.get(st["line"], 0) + 1
        key = f"{st['line']}#{count[st['line']]}"
        if key in notes:
            st[field] = notes[key]
        elif count[st["line"]] == 1 and str(st["line"]) in notes:
            st[field] = notes[str(st["line"])]
    if "end" in notes and steps:
        steps[-1][field] = (steps[-1].get(field, "") + " " + notes["end"]).strip()


def trace_auto(spec):
    raw = _record_steps(spec["code"], spec.get("setup", ""), _var_snapshot(set(spec.get("hide", []))))
    steps, prev = [], {}
    for st in raw:
        item = {"line": st["line"], "vars": _diff(prev, st["snap"])}
        if st["call"]:
            item["call"] = st["call"]
        if st["out"]:
            item["out"] = st["out"].rstrip("\n")
        item["badge"] = st.get("ret", "")
        prev = st["snap"]
        steps.append(item)
    _attach_notes(steps, spec.get("notes", {}))
    _attach_notes(steps, spec.get("badges", {}), "badge")
    return {k: v for k, v in spec.items() if k not in ("auto", "notes", "badges", "hide", "setup")} | {"steps": steps}


# ---------- memory: имена → объекты ----------

SCALARS = (int, float, str, bool, type(None))


def _mem_snapshot(hide, ids):
    def label(obj):
        if id(obj) not in ids:
            ids[id(obj)] = (f"o{len(ids) + 1}", obj)   # держим ссылку — id не переиспользуется
        return ids[id(obj)][0]

    def snap(chain):
        objs, names = {}, {}

        def visit(obj):
            key = label(obj)
            if key in objs:
                return key
            objs[key] = None
            if isinstance(obj, SCALARS):
                objs[key] = obj
            elif isinstance(obj, (list, tuple)):
                cells = [v if isinstance(v, SCALARS) else "@" + visit(v) for v in obj]
                objs[key] = cells if isinstance(obj, list) else {"t": "tuple", "v": cells}
            elif isinstance(obj, dict):
                objs[key] = {"t": "dict", "v": {str(k): (v if isinstance(v, SCALARS) else "@" + visit(v)) for k, v in obj.items()}}
            elif isinstance(obj, (set, frozenset)):
                objs[key] = {"t": type(obj).__name__, "v": sorted((v if isinstance(v, SCALARS) else repr(v)) for v in obj)}
            elif hasattr(obj, "__dict__") and not isinstance(obj, type):
                objs[key] = {"t": type(obj).__name__, "v": {k: (v if isinstance(v, SCALARS) else "@" + visit(v)) for k, v in vars(obj).items()}}
            else:
                objs[key] = {"t": type(obj).__name__, "v": short(obj)}
            return key

        labels = _label_frames(chain)
        for f, lab in zip(chain, labels):
            for name, value in f.f_locals.items():
                if name in hide or not _visible(name, value):
                    continue
                names[name if not lab else f"{name} · {lab}"] = visit(value)
        return {"vars": names, "objs": objs}
    return snap


def memory_auto(spec):
    ids = {}
    raw = _record_steps(spec["code"], spec.get("setup", ""), _mem_snapshot(set(spec.get("hide", [])), ids))
    steps, prev = [], {"vars": {}, "objs": {}}
    for st in raw:
        cur = st["snap"]
        item = {"line": st["line"], "vars": _diff(prev["vars"], cur["vars"]), "objs": _diff(prev["objs"], cur["objs"])}
        if st["out"]:
            item["out"] = st["out"].rstrip("\n")
        prev = cur
        steps.append(item)
    _attach_notes(steps, spec.get("notes", {}))
    return {k: v for k, v in spec.items() if k not in ("auto", "notes", "hide", "setup")} | {"steps": steps}


# ---------- paths: какие строки выполнились ----------

def paths_auto(spec):
    cases = []
    for case in spec["cases"]:
        code = case.get("code", spec.get("code", ""))
        lines = set()

        def tracer(frame, event, arg):
            if frame.f_code.co_filename != FILE:
                return None
            if event == "line":
                lines.add(frame.f_lineno)
            return tracer

        buf, err, g = _run(code, tracer, case.get("setup", ""))
        item = {"label": case["label"], "lines": sorted(lines), "out": buf.getvalue().rstrip("\n")}
        if "code" in case:
            item["code"] = code
        if err:
            item["error"] = err
        if case.get("note"):
            item["note"] = case["note"]
        show = case.get("show", spec.get("show", []))
        if show:
            item["vars"] = {n: short(g[n]) for n in show if n in g}
        cases.append(item)
    return {k: v for k, v in spec.items() if k not in ("auto", "cases", "show")} | {"cases": cases}


# ---------- comp: включение по элементам ----------

def comp_calc(spec):
    presets = []
    for p in spec["presets"]:
        items = eval(p["items"], {})  # noqa: S307 — учебный литерал из нашего же контента
        rows, result = [], []
        for it in items:
            env = {p["var"]: it}
            ok = bool(eval(p["cond"], {}, env)) if p.get("cond") else True  # noqa: S307
            val = eval(p["expr"], {}, env) if ok else None  # noqa: S307
            rows.append({"item": short(it, 24), "ok": ok, "val": short(val, 24) if ok else ""})
            if ok:
                result.append(val)
        name = p.get("name", "items")
        code = f"[{p['expr']} for {p['var']} in {name}" + (f" if {p['cond']}" if p.get("cond") else "") + "]"
        presets.append({**p, "rows": rows, "result": short(result, 200), "code": code})
    return {**spec, "presets": presets}


def sortkey_calc(spec):
    items = eval(spec["items"], {})  # noqa: S307
    keys = []
    for k in spec["keys"]:
        fn = eval(f"lambda x: {k['key']}", {}) if k.get("key") else (lambda x: x)  # noqa: S307
        order = sorted(range(len(items)), key=lambda i: fn(items[i]))
        keys.append({**k, "vals": [short(fn(x), 30) for x in items], "order": order})
    return {**spec, "items_repr": [short(x, 30) for x in items], "keys": keys}


def expand(spec):
    t = spec.get("type")
    if t == "comp":
        return comp_calc(spec)
    if t == "sortkey":
        return sortkey_calc(spec)
    if not spec.get("auto"):
        return spec
    if t == "trace":
        return trace_auto(spec)
    if t == "memory":
        return memory_auto(spec)
    if t == "paths":
        return paths_auto(spec)
    raise SystemExit(f"auto не поддерживается для схемы {t}")
