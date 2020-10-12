
from typing import Callable, Coroutine

from fastapi import FastAPI

from database import connect_db, connect_redis, disconnect_db, disconnect_redis

EventHandlerType = Callable[[], Coroutine[None, None, None]]


def startup_events(app: FastAPI) -> EventHandlerType:
    """Init connections e.t.c."""
    async def startup() -> None:  # noqa: WPS430
        """List startup events here."""
        await connect_db(app=app)
        await connect_redis(app=app)
    return startup


def shutdown_events(app: FastAPI) -> EventHandlerType:
    """Drop connections e.t.c."""
    async def shutdown() -> None:  # noqa: WPS430
        """List shutdown events here."""
        await disconnect_db(app=app)
        await disconnect_redis(app=app)
    return shutdown
