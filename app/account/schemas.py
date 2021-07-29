from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from app.address.schemas import AddressCreate


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
    email: Optional[str] = None
    password: Optional[str] = None
    nickname: Optional[str] = None
    document_number: Optional[str] = None
    accept_legal_term: Optional[bool] = True
    birthdate: Optional[date] = None

    @validator("accept_legal_term")
    def accept_legal_term(cls, v, values):
        if not v:
            raise ValueError("Accept legal term is not acceptable.")
        return v


class AccountCreate(AccountBase):
    password: str
    nickname: str
    addresses: Optional[List[AddressCreate]]


class AccountUpdate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    email_verified_at: datetime = None
    is_admin: bool = False
    is_celebrity: bool = False

    class Config:
        orm_mode = True


class PasswordResetTokenCreate(BaseModel):
    email: str


class PasswordResetToken(BaseModel):
    token: str
    email: str
