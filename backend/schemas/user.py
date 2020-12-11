from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Schema stored in DB
class UserInDB(UserBase):
    key: str = None
    hashed_password: str

    class Config:
        orm_mode = True


# Schema passed through API, once object created in DB
class User(UserBase):
    key: str
