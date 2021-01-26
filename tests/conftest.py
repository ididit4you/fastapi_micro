"""Root conftest."""
from typing import Generator

import pytest

from fastapi.testclient import TestClient

import databases
from alembic import command
from alembic.config import Config
from app.settings import conf
from main import app
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

POSTGRES_TEST_DB = str(conf.postgres.POSTGRES_URI)


@pytest.fixture(scope='module')
def cli():  # type: ignore
    """Тестовый клиент."""
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
def with_db() -> Generator[None, None, None]:
    """Создаем тестовую дб."""
    create_engine(POSTGRES_TEST_DB)
    db_exists = database_exists(POSTGRES_TEST_DB)
    if db_exists:
        drop_database(POSTGRES_TEST_DB)
    create_database(POSTGRES_TEST_DB)             # Create the test database.
    config = Config('alembic.ini')   # Run the migrations.
    command.upgrade(config, 'head')
    yield                            # Run the tests.
    drop_database(POSTGRES_TEST_DB)


@pytest.fixture
@pytest.mark.asyncio
async def db_conn():
    """Async db connection."""
    db = databases.Database(POSTGRES_TEST_DB)
    await db.connect()
    yield db
    await db.disconnect()
