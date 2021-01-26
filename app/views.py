from typing import Any

from fastapi import APIRouter, Request, Response


router = APIRouter()


@router.get(
    '/_health',
    name='healthcheck',
    summary='Simple healthcheck',
    include_in_schema=False,
)
async def healthcheck(
    request: Request,
    response: Response,
) -> Any:
    """Healthcheck."""
    await request.app.state.db.execute(query='SELECT 1')
    await request.app.state.redis.execute('PING')
    return {'message': 'OK'}
