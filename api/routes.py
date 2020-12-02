# Api root router
# Register routes from apps here
from fastapi import APIRouter

from api.calc.views import router as calc_router

api_routes = APIRouter()

api_routes.include_router(calc_router, tags=['Calc'])
