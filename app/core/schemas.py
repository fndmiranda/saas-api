from typing import List

from pydantic import BaseModel


class SchemaBase(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True


class SchemaPagination(SchemaBase):
    items: List = []
    per_page: int
    num_pages: int
    total: int
    page: int
