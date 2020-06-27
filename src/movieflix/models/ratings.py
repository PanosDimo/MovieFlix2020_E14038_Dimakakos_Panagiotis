"""Ratings Models."""
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

from ._base import Base


class Comment(BaseModel):
    """Comment Model."""

    id: UUID = Field(default_factory=uuid4, alias="_id")
    movie: UUID
    user: EmailStr
    rating: float = Field(..., ge=0, le=10)


class CommentInDB(Base, Comment):
    """Comment in Database Model."""
