from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class RecordIn(BaseModel):
    """
    A record being created or updated. Deliberately schema-flexible (extra='allow')
    because each of the 17 source files has a different, wide column set. Validate
    specific fields at the frontend form level / per-dataset if you need stricter rules.
    """
    model_config = ConfigDict(extra="allow")


class RecordOut(BaseModel):
    """A record as returned from the API, always includes a string id."""
    model_config = ConfigDict(extra="allow")
    id: str = Field(alias="_id")


class DatasetInfo(BaseModel):
    name: str
    label: str
    title_field: str | None = None
    record_count: int


class PaginatedRecords(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[dict[str, Any]]
