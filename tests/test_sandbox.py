"""Проверки docker-песочницы: код ученика не должен выбраться наружу.

Запускаются, только если доступен Docker и скачан образ песочницы
(python -m app.cli sandbox-check). Иначе — пропуск.
"""
import shutil
import subprocess
import time

import pytest

from app import runner


def _docker_ready() -> bool:
    if not shutil.which("docker"):
        return False
    r = subprocess.run(["docker", "image", "inspect", runner.docker_image()], capture_output=True)
    return r.returncode == 0


pytestmark = pytest.mark.skipif(not _docker_ready(), reason="Docker или образ песочницы недоступны")


@pytest.fixture(autouse=True)
def docker_mode(monkeypatch):
    monkeypatch.setenv("CODEQUEST_SANDBOX", "docker")


def probe(code: str) -> str:
    """Выполнить код в песочнице и вернуть напечатанное (или ошибку)."""
    res = runner.run(code)
    return res.error or res.stdout.strip()


def test_runs_code_and_tests():
    tests = "def test_a():\n    assert add(1, 2) == 3, 'bad'\n"
    assert runner.run("def add(a, b):\n    return a + b\n", tests).passed
    res = runner.run("def add(a, b):\n    return a - b\n", tests)
    assert not res.passed and res.tests[0]["message"] == "bad"
    assert runner.run("print('привет')").stdout == "привет\n"


def test_solution_file_available_to_tests():
    tests = "def test_src():\n    assert 'for' not in open('solution.py').read(), 'без цикла'\n"
    assert runner.run("x = sum(range(5))\n", tests).passed
    assert not runner.run("x = 0\nfor i in range(5):\n    x += i\n", tests).passed


def test_no_network():
    out = probe("import socket\ntry:\n    socket.create_connection(('1.1.1.1', 53), timeout=2)\n    print('ONLINE')\n"
                "except OSError as e:\n    print('offline')\n")
    assert out == "offline"


def test_runs_as_nobody_without_privileges():
    assert probe("import os\nprint(os.getuid(), os.getgid())") == "65534 65534"
    out = probe("import os\ntry:\n    os.setuid(0)\n    print('ROOT')\nexcept PermissionError:\n    print('denied')")
    assert out == "denied"


def test_filesystem_is_read_only_except_tmp():
    out = probe(
        "res = []\n"
        "for path in ('/etc/pwned', '/usr/local/lib/pwned', '/pwned'):\n"
        "    try:\n        open(path, 'w').write('x'); res.append('WROTE ' + path)\n"
        "    except OSError:\n        res.append('ro')\n"
        "open('/tmp/ok.txt', 'w').write('x')\n"
        "print(' '.join(res), open('/tmp/ok.txt').read())")
    assert out == "ro ro ro x"


def test_host_files_are_invisible():
    from app.db import ROOT
    out = probe(f"import os\nprint(os.path.exists({str(ROOT)!r}), os.path.exists('/var/run/docker.sock'))")
    assert out == "False False"


def test_file_size_limited():
    out = probe("try:\n    open('/tmp/big', 'wb').write(b'x' * (5 << 20))\n    print('BIG')\nexcept OSError as e:\n"
                "    print('limited')")
    assert out == "limited"


def test_memory_limit():
    res = runner.run("data = bytearray(1024 * 1024 * 1024)\nprint('ALLOCATED')")
    assert "памяти" in (res.error or ""), res


def test_process_limit():
    out = probe(
        "import os, time\nkids = 0\ntry:\n"
        "    for _ in range(500):\n"
        "        if os.fork() == 0:\n            time.sleep(3)\n            os._exit(0)\n"
        "        kids += 1\nexcept OSError:\n    pass\nprint('limited' if kids < 100 else kids)")
    assert out == "limited"


def test_infinite_loop_times_out_and_container_is_removed():
    started = time.monotonic()
    res = runner.run("while True:\n    pass\n", "def test_x():\n    pass\n")
    assert res.timed_out and not res.passed
    assert time.monotonic() - started < runner.TIMEOUT_SEC + runner.DOCKER_GRACE_SEC + 3
    left = subprocess.run(["docker", "ps", "-aq", "--filter", "name=cq-run-"], capture_output=True, text=True)
    assert left.stdout.strip() == ""


def test_sleep_times_out():
    res = runner.run("import time\ntime.sleep(60)\n")
    assert res.timed_out


def test_user_cannot_fake_result_or_flood_output():
    res = runner.run(
        "import os, sys\n"
        "os.write(1, b'{\"tests\": [{\"name\": \"x\", \"passed\": true, \"message\": \"\"}]}')\n"
        "sys.__stdout__.write('garbage' * 100000)\n"
        "print('ok')\n",
        "def test_x():\n    assert False, 'checker ran'\n")
    assert not res.passed and res.tests[0]["message"] == "checker ran" and res.stdout == "ok\n"


def test_sandbox_unavailable_is_reported(monkeypatch):
    monkeypatch.setenv("CODEQUEST_RUNNER_IMAGE", "codequest-no-such-image:missing")
    assert runner.run("print(1)").error == runner.SANDBOX_DOWN_MSG
