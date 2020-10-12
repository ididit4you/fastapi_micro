from pydantic import BaseModel


class Record(BaseModel):
    """Record serializer."""

    id: int
    text: str
