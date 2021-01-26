import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from app.events import shutdown_events, startup_events
from app.routes import main_router
from app.settings import conf

app = FastAPI(
    title=conf.PROJECT_NAME,
    version=conf.PROJECT_VERSION,
    description=conf.PROJECT_DESCRIPTION,
    # The root_path is used to handle cases when proxy adds an extra path prefix that is not seen by application.
    root_path=conf.ROOT_PATH,
)

app.add_event_handler('startup', startup_events(app))
app.add_event_handler('shutdown', shutdown_events(app))


# Sentry
if conf.SENTRY_DSN:
    sentry_sdk.init(dsn=conf.SENTRY_DSN)
    app.add_middleware(SentryAsgiMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(main_router)
