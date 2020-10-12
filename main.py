from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.settings import conf
from app.routes import main_router


app = FastAPI(
    openapi_url=conf.OPENAPI_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(main_router)
