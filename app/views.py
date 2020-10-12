from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get('/hc', name='healthcheck')
async def healthcheck() -> Any:
    """Тестовый view."""
    return {'message': 'OK'}
