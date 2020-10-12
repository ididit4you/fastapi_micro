from typing import Any, List

from fastapi import APIRouter, Request
from fastapi.responses import ORJSONResponse

from api.records.models import record
from api.records.shema import Record

router = APIRouter()


@router.get(
    '/records',
    summary='Records list',
    name='records',
    response_class=ORJSONResponse,
    response_model=List[Record],
)
async def create_item(request: Request) -> Any:
    """Fetch all records."""
    db = request.app.state.db
    return await db.fetch_all(record.select())
