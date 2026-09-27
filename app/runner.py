"""Запуск пользовательского Python-кода в отдельном процессе.

Код исполняется в дочернем интерпретаторе (python -I) во временной папке,
с лимитом по времени и по CPU. Результат харнесс пишет в result.json,
поэтому print() пользователя не может сломать разбор результата.

Формат тестов в задании — обычный Python с функциями test_*:

    def test_sum():
        assert add(2, 3) == 5, "add(2, 3) должно быть 5"

    def test_prints_hello():
        assert OUTPUT.strip() == "Hello"

В тестах доступны все имена из кода пользователя, а также:
    OUTPUT          — всё, что код напечатал при запуске
    capture(f, *a)  — вызвать f(*a) и вернуть напечатанное
"""
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field, asdict
from pathlib import Path

TIMEOUT_SEC = 5
MAX_OUTPUT = 10_000

HARNESS = r'''
import ast, contextlib, io, json, sys, traceback

def _short_tb(exc, filename):
    frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == filename]
    line = frames[-1].lineno if frames else getattr(exc, "lineno", None)
    return f"{type(exc).__name__}: {exc}", line

def capture(fn, *args, **kwargs):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args, **kwargs)
    return buf.getvalue()

result = {"stdout": "", "error": None, "error_line": None, "tests": []}
user_src = open("solution.py", encoding="utf-8").read()
tests_src = open("tests.py", encoding="utf-8").read()
ns = {"__name__": "__main__", "capture": capture}
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        exec(compile(user_src, "solution.py", "exec"), ns)
except BaseException as e:
    result["error"], result["error_line"] = _short_tb(e, "solution.py")
result["stdout"] = buf.getvalue()[:%(max_output)d]

if result["error"] is None and tests_src.strip():
    ns["OUTPUT"] = buf.getvalue()
    tns = dict(ns)
    try:
        exec(compile(tests_src, "tests.py", "exec"), tns)
    except BaseException as e:
        result["error"] = "Ошибка в тестах задания: " + _short_tb(e, "tests.py")[0]
    # Тестами считаем только функции test_*, объявленные в самом файле тестов:
    # ученик тоже может написать свои test_* (в уроках про тестирование) — они не в счёт.
    names = [] if result["error"] else [
        node.name for node in ast.parse(tests_src).body
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
    for name in names:
        item = {"name": name, "passed": True, "message": ""}
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                tns[name]()
        except AssertionError as e:
            item["passed"] = False
            item["message"] = str(e) or "Проверка не прошла"
        except BaseException as e:
            item["passed"] = False
            item["message"] = f"{type(e).__name__}: {e}"
        result["tests"].append(item)

with open("result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False)
''' % {"max_output": MAX_OUTPUT}


@dataclass
class RunResult:
    stdout: str = ""
    error: str | None = None
    error_line: int | None = None
    tests: list = field(default_factory=list)
    timed_out: bool = False

    @property
    def passed(self) -> bool:
        return (
            not self.timed_out
            and self.error is None
            and bool(self.tests)
            and all(t["passed"] for t in self.tests)
        )

    def to_dict(self) -> dict:
        d = asdict(self)
        d["passed"] = self.passed
        return d


def _limits():  # pragma: no cover - выполняется в дочернем процессе
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_CPU, (TIMEOUT_SEC, TIMEOUT_SEC + 1))
    except (ImportError, ValueError, OSError):
        pass


def run(user_code: str, tests: str = "") -> RunResult:
    with tempfile.TemporaryDirectory(prefix="codequest-") as tmp:
        d = Path(tmp)
        (d / "solution.py").write_text(user_code, encoding="utf-8")
        (d / "tests.py").write_text(tests, encoding="utf-8")
        (d / "harness.py").write_text(HARNESS, encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, "-I", "harness.py"],
                cwd=d,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SEC,
                stdin=subprocess.DEVNULL,
                preexec_fn=_limits if sys.platform != "win32" else None,
                env={"PYTHONIOENCODING": "utf-8", "PATH": "/usr/bin:/bin"},
            )
        except subprocess.TimeoutExpired:
            return RunResult(
                error=f"Код выполнялся дольше {TIMEOUT_SEC} секунд — возможно, бесконечный цикл?",
                timed_out=True,
            )
        result_file = d / "result.json"
        if proc.returncode < 0 and not result_file.exists():
            # убит сигналом — чаще всего SIGXCPU от лимита процессорного времени
            return RunResult(
                error=f"Код выполнялся дольше {TIMEOUT_SEC} секунд — возможно, бесконечный цикл?",
                timed_out=True,
            )
        if not result_file.exists():
            err = (proc.stderr or "").strip().splitlines()
            return RunResult(error=err[-1] if err else "Процесс завершился аварийно")
        data = json.loads(result_file.read_text(encoding="utf-8"))
        return RunResult(**data)


def normalize_output(text: str) -> str:
    """Сравнение вывода без учёта хвостовых пробелов и пустых строк в конце."""
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)
