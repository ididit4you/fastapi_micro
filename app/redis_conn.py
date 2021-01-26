import aioredis

from fastapi import FastAPI

from app.settings import conf


async def connect_redis(app: FastAPI) -> None:
    """Add redis connection to app state."""
    app.state.redis = await aioredis.create_redis_pool(conf.redis.REDIS_URI)


async def disconnect_redis(app: FastAPI) -> None:
    """Disconnect redis."""
    app.state.redis.close()
    await app.state.redis.wait_closed()
