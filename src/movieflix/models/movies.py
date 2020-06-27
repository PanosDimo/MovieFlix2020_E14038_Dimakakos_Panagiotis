"""Movie Models."""
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ._base import Base
from .comments import Comment


class MovieRef(BaseModel):
    """Movie Reference Model."""

    id: UUID = Field(default_factory=uuid4, alias="_id")


class Movie(MovieRef):
    """Movie Model."""

    title: str
    year: int = Field(..., ge=0)
    description: str
    actors: List[str] = Field(default_factory=list)
    rating: float = Field(..., ge=0, le=10)
    comments: List[UUID] = Field(default_factory=list)


class Movies(BaseModel):
    """Movies Model."""

    movies: List[Movie] = Field(default_factory=list)


class MovieInDB(Base, Movie):
    """Movie in Database Model."""


class MovieDeref(Movie):
    """Movie with comments dereferenced Model."""

    comments: List[Comment] = Field(default_factory=list)  # type: ignore
