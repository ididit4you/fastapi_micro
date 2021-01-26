import databases

from fastapi import FastAPI

from app.settings import conf


async def connect_db(app: FastAPI) -> None:
    """Connect pg."""
    database = databases.Database(
        conf.POSTGRES_URI,
        min_size=conf.POSTGRES_POOL_MIN,
        max_size=conf.POSTGRES_POOL_MAX,
    )
    await database.connect()
    app.state.db = database


async def disconnect_db(app: FastAPI) -> None:
    """Disconnect pg."""
    await app.state.db.disconnect()
