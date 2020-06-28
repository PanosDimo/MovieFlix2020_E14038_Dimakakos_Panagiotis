"""Comments Models."""
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

from ._base import Base


class Comment(BaseModel):
    """Comment Model."""

    id: UUID = Field(default_factory=uuid4, alias="_id")
    movie: UUID
    user: EmailStr
    comment: str


class CommentInDB(Base, Comment):
    """Comment in Database Model."""


class CommentDeref(Comment):
    """Comment with Movie Dereferenced Model."""

    movie: str  # type: ignore


class Comments(BaseModel):
    """Comments Model."""

    comments: List[CommentDeref]
