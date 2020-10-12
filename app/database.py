import aioredis
import databases

from fastapi import FastAPI

from app.settings import conf


async def connect_redis(app: FastAPI) -> None:
    """Connect redis."""
    redis_host = conf.REDIS_HOST
    app.state.redis = await aioredis.create_redis_pool(redis_host)


async def disconnect_redis(app: FastAPI) -> None:
    """Disconnect redis."""
    app.state.redis.close()
    await app['redis'].wait_closed()


async def connect_db(app: FastAPI) -> None:
    """Connect pg."""
    database = databases.Database(conf.pg_dsn, min_size=10, max_size=20)
    await database.connect()
    app.state.db = database


async def disconnect_db(app: FastAPI) -> None:
    """Disconnect pg."""
    await app.state.db.disconnect()
