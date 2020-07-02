"""User Models."""
from enum import Enum
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

from ._base import Base


class Role(str, Enum):
    """Application User Roles."""

    ADMIN = "ADMIN"
    USER = "USER"


class UserRef(BaseModel):
    """User Reference Model."""

    id: UUID = Field(default_factory=uuid4, alias="_id")


class User(UserRef):
    """User Model."""

    name: str
    email: EmailStr
    comments: List[UUID] = Field(default_factory=list)
    category: Role


class UserInDB(Base, User):
    """User in Database Model."""

    password: bytes


class UserWithToken(User):
    """User with JWT token Model."""

    token: str


class Users(BaseModel):
    """Users Model."""

    users: List[User] = Field(default_factory=list)
