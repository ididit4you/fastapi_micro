from fastapi import APIRouter

from app.views import router

main_router = APIRouter()

main_router.include_router(router)
