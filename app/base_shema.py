from typing import Union

import orjson
from pydantic import BaseModel


def handle_extra_types(to_serialize: object) -> Union[float, str]:
    """Handle types which orjson does not understand."""
    return str(to_serialize)


def orjson_dumps(value, *, default):  # type: ignore
    """orjson.dumps returns bytes, to match standard json.dumps we need to decode."""
    return orjson.dumps(value, default=handle_extra_types).decode()


class CustomBaseModel(BaseModel):
    """Base model whith better and faster serialization/deserialization."""

    class Config:
        """Set custom loader and dumper."""

        json_loads = orjson.loads
        json_dumps = orjson_dumps
