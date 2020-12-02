from fastapi import APIRouter

from api.routes import api_routes
from app.views import router

main_router = APIRouter()

main_router.include_router(router)
main_router.include_router(api_routes)
