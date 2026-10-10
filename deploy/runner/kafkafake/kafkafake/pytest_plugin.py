"""pytest-плагин kafkafake: перед каждым тестом учебный кластер очищается — тесты не видят чужих сообщений."""
import pytest

from .core import reset


@pytest.fixture(autouse=True)
def _kafkafake_clean_cluster():
    reset()
    yield
