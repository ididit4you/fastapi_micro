from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from app.events import shutdown_events, startup_events
from app.routes import main_router
from app.settings import conf

app = FastAPI(
    openapi_url=conf.OPENAPI_URL,
)
app.add_event_handler('startup', startup_events(app))
app.add_event_handler('shutdown', shutdown_events(app))

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(main_router)
