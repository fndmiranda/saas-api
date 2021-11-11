from datetime import datetime
from typing import List

from app.core.schemas import PaginationSchema, SchemaBase


class AddressBase(SchemaBase):
    name: str = None
    is_default: bool = True
    street: str = None
    neighborhood: str = None
    city: str = None
    postcode: str = None
    state: str = None
    number: int = None
    complement: str = None
    lat: float = None
    lng: float = None


class AddressCreate(AddressBase):
    name: str
    street: str
    neighborhood: str
    city: str
    postcode: str
    state: str


class AddressUpdate(AddressBase):
    pass


class Address(AddressBase):
    id: int
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


class AddressPagination(PaginationSchema):
    items: List[Address]
