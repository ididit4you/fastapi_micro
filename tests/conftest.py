"""Root conftest."""
from typing import AsyncGenerator, Generator

import databases
from databases.core import Database
import pytest
from alembic import command
from alembic.config import Config
from pydantic import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from fastapi.testclient import TestClient

from app.settings import conf
from main import app

TEST_DB = PostgresDsn.build(
    scheme='postgresql',
    user=conf.postgres.POSTGRES_USER,
    password=conf.postgres.POSTGRES_PASSWORD,
    host='localhost',
    port=conf.postgres.POSTGRES_PORT,
    path='/{db}.{ending}'.format(
        db=conf.postgres.POSTGRES_DB,
        ending='pytest',
    ),
)


@pytest.fixture(scope='session', autouse=True)
def temp_db() -> Generator[None, None, None]:
    """Create new test db for testing session."""
    create_engine(TEST_DB)
    db_exists = database_exists(TEST_DB)
    if db_exists:
        drop_database(TEST_DB)
    create_database(TEST_DB)  # Create the test database.
    config = Config('alembic.ini')  # Run the migrations.
    config.set_main_option('sqlalchemy.url', TEST_DB)
    assert config.get_main_option('sqlalchemy.url') == TEST_DB
    command.upgrade(config, 'head')
    yield  # Run the tests.
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
