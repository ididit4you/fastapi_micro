
from typing import Callable, Coroutine

from fastapi import FastAPI

EventHandlerType = Callable[[], Coroutine[None, None, None]]


def startup_events(app: FastAPI) -> EventHandlerType:
    """Init connections e.t.c."""
    async def startup() -> None:  # noqa: WPS430
        """List startup events here."""
        pass
    return startup


def shutdown_events(app: FastAPI) -> EventHandlerType:
    """Drop connections e.t.c."""
    async def shutdown() -> None:  # noqa: WPS430
        """List shutdown events here."""
        pass
    return shutdown
