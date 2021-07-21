from datetime import datetime
from typing import Optional

from pydantic import Field

from app.core.schemas import SchemaBase


class SegmentBase(SchemaBase):
    title: str = Field(None, min_length=3, max_length=64)
    is_active: Optional[bool] = True
    image: Optional[str] = None
    color: Optional[str] = None


class SegmentCreate(SegmentBase):
    title: str


class SegmentUpdate(SegmentBase):
    pass


class Segment(SegmentBase):
    id: int
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
