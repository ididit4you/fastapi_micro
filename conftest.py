# type: ignore

"""Корневой conftest достпуный из всех тестов проекта."""
from typing import Generator

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from fastapi.testclient import TestClient

from app.settings import conf
from main import get_app


@pytest.fixture(scope='module')
def cli() -> Generator:
    """Тестовый клиент."""
    app = get_app()
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
def create_test_database():
    """Создаем тестовую дб."""
    conf.ENV = 'TEST'
    url = str(conf.pg_dsn)
    create_engine(url)
    assert not database_exists(url), 'Test database already exists. Aborting tests.'
    create_database(url)             # Create the test database.
    config = Config('alembic.ini')   # Run the migrations.
    command.upgrade(config, 'head')
    yield                            # Run the tests.
    drop_database(url)
