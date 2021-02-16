"""Root conftest."""
from typing import AsyncGenerator, Generator

import databases
import pytest
from alembic import command
from alembic.config import Config
from databases.core import Database
from sqlalchemy_utils import create_database, database_exists, drop_database

from fastapi.testclient import TestClient

from app.settings import conf
from main import app

TEST_DB = str(conf.postgres.POSTGRES_URI)


@pytest.fixture(autouse=True, scope='session')
def temp_db() -> Generator[None, None, None]:
    """Create new test db for testing session."""
    assert TEST_DB.endswith('.pytest')
    db_exists = database_exists(TEST_DB)

    if db_exists:
        drop_database(TEST_DB)
    create_database(TEST_DB)  # Create the test database.
    config = Config('alembic.ini')  # Run the migrations.
    config.set_main_option('sqlalchemy.url', TEST_DB)
    command.upgrade(config, 'head')
    yield  # Run tests.
    drop_database(TEST_DB)


@pytest.fixture
@pytest.mark.asyncio
async def db_conn() -> AsyncGenerator[databases.Database, None]:
    """Async db connection."""
    db = databases.Database(TEST_DB)
    await db.connect()
    yield db
    if db.is_connected:
        await db.disconnect()


@pytest.fixture
def cli(db_conn: Database):  # type: ignore
    """Test cli."""
    with TestClient(app) as client:
        client.app.state.db = db_conn
        yield client
