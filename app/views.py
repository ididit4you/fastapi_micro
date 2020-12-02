from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get(
    '/_health',
    name='healthcheck',
    summary='Simple healthcheck',
    include_in_schema=False,
)
async def healthcheck() -> Any:
    """Healthcheck."""
    return {'message': 'OK'}
