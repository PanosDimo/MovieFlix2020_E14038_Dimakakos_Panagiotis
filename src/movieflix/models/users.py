"""User Models."""
from enum import Enum
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ._base import Base
from .comments import Comment


class Role(str, Enum):
    """Application User Roles."""

    ADMIN = "ADMIN"
    USER = "USER"


class UserComment(Comment):
    """Comment made by user."""

    movie: UUID


class UserRef(BaseModel):
    """User Reference Model."""

    id: UUID = Field(default_factory=uuid4)


class User(UserRef):
    """User Model."""

    name: str
    email: str
    comments: List[UserComment] = Field(default_factory=list)
    category: Role


class UserInDB(Base, User):
    """User in Database Model."""

    password: bytes


class UserWithToken(User):
    """User with JWT token Model."""

    token: str
