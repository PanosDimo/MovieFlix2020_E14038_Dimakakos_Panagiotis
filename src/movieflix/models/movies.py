"""Movie Models."""
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ._base import Base
from .comments import Comment


class MovieComment(Comment):
    """Comment made to a movie."""

    user: UUID


class MovieRef(BaseModel):
    """Movie Reference Model."""

    id: UUID = Field(default_factory=uuid4, alias="_id")


class Movie(Base, MovieRef):
    """Movie Model."""

    title: str
    year: int = Field(..., ge=0)
    description: str
    actors: List[str] = Field(default_factory=list)
    rating: float = Field(..., ge=0, le=10)
    comments: List[MovieComment] = Field(default_factory=list)
