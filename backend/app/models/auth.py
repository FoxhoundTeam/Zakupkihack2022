from typing import Optional

from pydantic import BaseModel, EmailStr

from app.database.tables import Roles


class BaseUser(BaseModel):
    username: Optional[str]
    address: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(BaseUser):
    password: str
    role: Roles


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class UserWithRole(User):
    role: Roles


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
