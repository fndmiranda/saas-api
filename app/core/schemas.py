from typing import List

from pydantic import BaseModel


class RootSchema(BaseModel):
    application: str
    version: str


class SchemaBase(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True


class PaginationSchema(SchemaBase):
    items: List = []
    per_page: int
    num_pages: int
    total: int
    page: int


class PhoneSchema(SchemaBase):
    name: str
    number: int
    default: bool
