from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class UserBase(BaseModel):
    name: str = Field(None, min_length=2, max_length=64)
    email: str
    nickname: str
    document_number: str
    is_admin: bool = False
    is_celebrity: bool = False
    accept_legal_term: bool = False
    birthdate: date = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


class AccountBase(UserBase):
    name: str = Field(None, min_length=2, max_length=64)
    email: str
    nickname: str
    document_number: str
    is_admin: bool = False
    is_celebrity: bool = False
    accept_legal_term: bool = False
    birthdate: date = None

    @validator("accept_legal_term")
    def accept_legal_term(cls, v, values, **kwargs):
        if not v:
            raise ValueError("Accept legal term is not acceptable.")
        return v


class AccountCreate(AccountBase):
    password: str


class AccountUpdate(AccountBase):
    password: Optional[str] = None


class Account(AccountBase):
    id: int
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    email_verified_at: datetime = None

    class Config:
        orm_mode = True
