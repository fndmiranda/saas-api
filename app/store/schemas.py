from datetime import datetime
from typing import Optional, List, Literal

from pydantic import Field

from app.core.schemas import SchemaBase, PhoneSchema
from app.address.schemas import AddressCreate


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


class StoreBase(SchemaBase):
    title: str = Field(None, min_length=3, max_length=64)
    legal: Optional[str] = None
    phones: Optional[List[PhoneSchema]] = None
    information: Optional[dict] = None
    automatic_accept: Optional[bool] = False
    is_active: Optional[bool] = True
    document_type: Optional[Literal["cpf", "cnpj"]] = None
    document_number: Optional[str] = None
    image: Optional[str] = None
    background_image: Optional[str] = None
    segment_id: Optional[int] = None


class StoreCreate(StoreBase):
    title: str = Field(min_length=3, max_length=64)
    legal: str
    phones: List[PhoneSchema]
    addresses: Optional[List[AddressCreate]]
    document_type: str
    document_number: str
    segment_id: int


class StoreUpdate(StoreBase):
    pass


class Store(StoreBase):
    id: int
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    approved_at: Optional[datetime] = None

    class Config:
        orm_mode = True
