"""Ratings Models."""
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

from ._base import Base


class Rating(BaseModel):
    """Rating Model."""

    id: UUID = Field(default_factory=uuid4, alias="_id")
    movie: UUID
    user: EmailStr
    rating: float = Field(..., ge=0, le=10)


class RatingInDB(Base, Rating):
    """Rating in Database Model."""


class RatingDeref(Rating):
    """Rating with movie dereferenced Model."""

    movie: str  # type: ignore


class Ratings(BaseModel):
    """Ratings Model."""

    ratings: List[RatingDeref]
