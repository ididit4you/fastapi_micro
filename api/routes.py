from fastapi import APIRouter

from api.records.views import router as records_router

api_routes = APIRouter()

# Records routers
api_routes.include_router(records_router, tags=['Records'])
