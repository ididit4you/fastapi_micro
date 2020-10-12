from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get('/hc', name='healthcheck', summary='Simple healthcheck')
async def healthcheck() -> Any:
    """Healthcheck."""
    return {'message': 'OK'}
