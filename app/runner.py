"""Запуск пользовательского Python-кода в песочнице.

Режим задаётся переменной окружения CODEQUEST_SANDBOX:

    docker (по умолчанию) — каждый запуск в отдельном одноразовом контейнере: без сети,
                            с read-only файловой системой, под пользователем nobody, без
                            capabilities, с лимитами памяти, процессов и CPU. Для сервера
                            в интернете — только этот режим.
    local                 — дочерний процесс python -I во временной папке с лимитами
                            времени и CPU. Изоляции нет: только для разработки на своём
                            компьютере, тестов и проверки контента из репозитория.

Код, тесты и сам харнесс передаются через stdin, результат харнесс пишет в свой
дескриптор stdout, а stdout/stderr пользовательского кода уводит в /dev/null и в буфер,
поэтому print() пользователя не может сломать разбор результата. Исходник ученика
кладётся в рабочую папку как solution.py — его читают тесты некоторых заданий.

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
import logging
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from dataclasses import dataclass, field, asdict

log = logging.getLogger("codequest.runner")

TIMEOUT_SEC = 5
MAX_OUTPUT = 10_000              # сколько напечатанного показываем ученику
MAX_RESULT_BYTES = 1_000_000     # больше от харнесса не читаем
MEMORY_MB = 256
DOCKER_GRACE_SEC = 5             # запас на старт контейнера
DEFAULT_IMAGE = "codequest-runner:3"   # собирается из deploy/runner/Dockerfile

TIMEOUT_MSG = f"Код выполнялся дольше {TIMEOUT_SEC} секунд — возможно, бесконечный цикл?"
MEMORY_MSG = f"Программа заняла больше {MEMORY_MB} МБ памяти — возможно, бесконечно растущий список?"
BUSY_MSG = "Сервер сейчас занят проверкой других решений — попробуй ещё раз через несколько секунд"
SANDBOX_DOWN_MSG = "Песочница для запуска кода недоступна — сообщи администратору"

# Выполняется внутри песочницы: читает задание из stdin и запускает харнесс.
BOOTSTRAP = ("import json,sys;_d=json.loads(sys.stdin.buffer.read());"
             "exec(compile(_d['harness'],'<harness>','exec'),{'_INPUT':_d,'__name__':'__harness__'})")

HARNESS = r'''
import ast, contextlib, io, json, os, signal, sys, traceback

_TIMEOUT = %(timeout)d

# Тесты некоторых заданий читают исходник ученика из файла (например, проверяют, что нет цикла).
with open("solution.py", "w", encoding="utf-8") as _f:
    _f.write(_INPUT["solution"])

# Результат уходит в копию настоящего stdout; fd 1 и 2 пользовательского кода — в /dev/null.
_out = os.fdopen(os.dup(1), "w", encoding="utf-8")
_null = os.open(os.devnull, os.O_WRONLY)
os.dup2(_null, 1)
os.dup2(_null, 2)

try:
    import resource
    # CPU: мягкий лимит чуть позже таймера — сначала срабатывает понятный таймаут (SIGALRM),
    # и только если код его перехватил, процесс убивает SIGXCPU, а затем SIGKILL.
    for _res, _soft, _hard in (("RLIMIT_CPU", _TIMEOUT + 1, _TIMEOUT + 2),
                               ("RLIMIT_FSIZE", 1 << 20, 1 << 20),
                               ("RLIMIT_AS", %(memory)d << 20, %(memory)d << 20)):
        try:
            resource.setrlimit(getattr(resource, _res), (_soft, _hard))
        except (ValueError, OSError, AttributeError):
            pass   # macOS не даёт ограничить RLIMIT_AS — это нормально
except ImportError:
    pass

class _Timeout(BaseException):
    pass

def _alarm(signum, frame):
    raise _Timeout()

signal.signal(signal.SIGALRM, _alarm)
signal.alarm(_TIMEOUT)

def _short_tb(exc, filename):
    if isinstance(exc, _Timeout):
        result["timed_out"] = True
        return %(timeout_msg)r, None
    if isinstance(exc, MemoryError):
        return %(memory_msg)r, None
    frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == filename]
    line = frames[-1].lineno if frames else getattr(exc, "lineno", None)
    return f"{type(exc).__name__}: {exc}", line

def capture(fn, *args, **kwargs):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args, **kwargs)
    return buf.getvalue()

result = {"stdout": "", "error": None, "error_line": None, "tests": [], "timed_out": False}
user_src = _INPUT["solution"]
tests_src = _INPUT["tests"]
del _INPUT
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
        except _Timeout:
            result["timed_out"] = True
            result["error"] = %(timeout_msg)r
            break
        except BaseException as e:
            item["passed"] = False
            item["message"] = f"{type(e).__name__}: {e}"
        result["tests"].append(item)

signal.alarm(0)
_out.write(json.dumps(result, ensure_ascii=False))
_out.flush()
''' % {"max_output": MAX_OUTPUT, "timeout": TIMEOUT_SEC, "memory": MEMORY_MB,
       "timeout_msg": TIMEOUT_MSG, "memory_msg": MEMORY_MSG}


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


# ---------- настройки ----------

def sandbox_mode() -> str:
    mode = os.environ.get("CODEQUEST_SANDBOX", "docker")
    if mode not in ("docker", "local"):
        raise RuntimeError(f"CODEQUEST_SANDBOX={mode!r}: допустимо docker или local")
    return mode


def docker_image() -> str:
    return os.environ.get("CODEQUEST_RUNNER_IMAGE", DEFAULT_IMAGE)


# Одновременно запускаем не больше N программ — иначе десяток «while True» положит сервер.
_slots = threading.BoundedSemaphore(int(os.environ.get("CODEQUEST_MAX_RUNS", "4")))


def docker_command(name: str) -> list[str]:
    return [
        "docker", "run", "--rm", "-i", "--name", name,
        "--pull", "never",                         # образ скачивает sandbox-check, не запрос ученика
        "--network", "none",                       # никакой сети
        "--read-only",                             # файловая система только для чтения…
        "--tmpfs", "/tmp:rw,size=16m,mode=1777",   # …кроме маленькой /tmp в памяти
        "--workdir", "/tmp",
        "--user", "65534:65534",                   # nobody
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--memory", f"{MEMORY_MB}m", "--memory-swap", f"{MEMORY_MB}m",
        "--cpus", "1",
        "--pids-limit", "64",
        "--ulimit", "nofile=64:64",
        "--env", "PYTHONIOENCODING=utf-8",
        "--env", "PYTHONDONTWRITEBYTECODE=1",
        docker_image(), "python", "-I", "-c", BOOTSTRAP,
    ]


# ---------- запуск ----------

def _communicate(cmd: list[str], payload: bytes, timeout: float, cwd: str | None = None,
                 env: dict | None = None) -> tuple[int | None, bytes, bytes]:
    """Как subprocess.run, но читает не больше MAX_RESULT_BYTES — поток мусора не съест память.
    Возвращает (код возврата или None при таймауте, stdout, stderr)."""
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, cwd=cwd, env=env)
    streams = {"out": [], "err": []}

    def drain(pipe, key, cap):
        size = 0
        while chunk := pipe.read(65536):
            if size < cap:
                streams[key].append(chunk[:cap - size])
                size += len(chunk)

    readers = [threading.Thread(target=drain, args=(proc.stdout, "out", MAX_RESULT_BYTES), daemon=True),
               threading.Thread(target=drain, args=(proc.stderr, "err", 20_000), daemon=True)]
    for t in readers:
        t.start()
    try:
        proc.stdin.write(payload)
        proc.stdin.close()
    except (BrokenPipeError, OSError):
        pass
    try:
        code = proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        code = None
    for t in readers:
        t.join(timeout=2)
    return code, b"".join(streams["out"]), b"".join(streams["err"])


def _run_local(payload: bytes):
    with tempfile.TemporaryDirectory(prefix="codequest-") as tmp:
        return _communicate([sys.executable, "-I", "-c", BOOTSTRAP], payload, TIMEOUT_SEC + 1, cwd=tmp,
                            env={"PYTHONIOENCODING": "utf-8", "PATH": "/usr/bin:/bin"})


def _run_docker(payload: bytes):
    name = f"cq-run-{uuid.uuid4().hex[:12]}"
    code, out, err = _communicate(docker_command(name), payload, TIMEOUT_SEC + DOCKER_GRACE_SEC)
    if code is None:   # убили клиента docker — контейнер нужно добить отдельно
        subprocess.run(["docker", "kill", name], capture_output=True, timeout=10)
    return code, out, err


def run(user_code: str, tests: str = "") -> RunResult:
    if not _slots.acquire(timeout=15):
        return RunResult(error=BUSY_MSG)
    try:
        payload = json.dumps({"harness": HARNESS, "solution": user_code, "tests": tests}).encode()
        mode = sandbox_mode()
        started = time.monotonic()
        try:
            code, out, err = _run_docker(payload) if mode == "docker" else _run_local(payload)
        except FileNotFoundError:
            log.error("Не найдена команда docker — песочница недоступна")
            return RunResult(error=SANDBOX_DOWN_MSG)
    finally:
        _slots.release()
    return _parse(mode, code, out, err, time.monotonic() - started)


def _parse(mode: str, code: int | None, out: bytes, err: bytes, elapsed: float) -> RunResult:
    if out:
        try:
            return RunResult(**json.loads(out.decode("utf-8")))
        except (ValueError, TypeError):
            pass   # результат обрезан или испорчен — разбираемся по коду возврата
    if code is None:
        return RunResult(error=TIMEOUT_MSG, timed_out=True)
    if mode == "docker":
        if code == 125:   # сам docker не смог запустить контейнер (демон, образ…)
            log.error("docker run: %s", err.decode("utf-8", "replace").strip()[-500:])
            return RunResult(error=SANDBOX_DOWN_MSG)
        if code == 137:   # SIGKILL: быстро — OOM killer, после таймаута — жёсткий лимит CPU
            if elapsed < TIMEOUT_SEC:
                return RunResult(error=MEMORY_MSG)
            return RunResult(error=TIMEOUT_MSG, timed_out=True)
        if code > 128:    # SIGXCPU и прочие сигналы — упёрлись в лимит CPU
            return RunResult(error=TIMEOUT_MSG, timed_out=True)
    elif code < 0:        # убит сигналом — чаще всего SIGXCPU от лимита процессорного времени
        return RunResult(error=TIMEOUT_MSG, timed_out=True)
    lines = err.decode("utf-8", "replace").strip().splitlines()
    return RunResult(error=lines[-1] if lines else "Процесс завершился аварийно")


def _norm_command(text: str) -> str:
    """Команда без лишних пробелов и без приглашения «$ » в начале."""
    text = " ".join(text.strip().split())
    return text[2:] if text.startswith("$ ") else text


def command_matches(answer: str, variants: str) -> bool:
    """Задание «Терминал»: ответ совпадает с одним из вариантов (по одному на строку).
    Вариант «re:…» — регулярное выражение, которому ответ должен соответствовать целиком."""
    got = _norm_command(answer)
    for v in variants.splitlines():
        v = v.strip()
        if not v:
            continue
        if v.startswith("re:"):
            if re.fullmatch(v[3:], got):
                return True
        elif got == _norm_command(v):
            return True
    return False


def normalize_output(text: str) -> str:
    """Сравнение вывода без учёта хвостовых пробелов и пустых строк в конце."""
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)
