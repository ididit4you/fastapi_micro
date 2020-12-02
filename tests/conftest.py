"""Root conftest."""
import pytest

from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope='module')
def cli():  # type: ignore
    """Тестовый клиент."""
    with TestClient(app) as client:
        yield client