from typing import Any, List

from fastapi import APIRouter, Request

from api.records.shema import Record
from api.records.models import record

router = APIRouter()


@router.get('/records/', summary='Records list', response_model=List[Record])
async def create_item(request: Request) -> Any:
    """Fetch all records."""
    db = request.app.state.db
    return await db.fetch_all(record.select())
