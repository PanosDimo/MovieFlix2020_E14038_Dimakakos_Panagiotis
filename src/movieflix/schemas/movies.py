"""Movies Schemas."""
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator


class SearchMoviesRequest(BaseModel):
    """SEARCH MOVIES Request."""

    title: Optional[str] = None
    year: Optional[int] = None
    actors: List[str] = Field(default_factory=list)

    @validator("actors", pre=True)
    def convert_to_list(cls, v: Optional[str]) -> List[str]:
        """Convert string to list.

        :param v: The value.
        :return: Value to list.
        """
        if not v:
            return []
        if isinstance(v, str) and "," not in v:
            return [v]
        return [s.strip() for s in v.split(",")]


class SearchMoviesResponse(BaseModel):
    """SEARCH MOVIES Response."""

    class Movie(BaseModel):
        """Helper Movie class."""

        id: UUID
        title: str
        year: int
        rating: float = Field(..., ge=0, le=10)

    movies: List[Movie]


class GetMovieRequest(BaseModel):
    """GET MOVIE Request."""

    movie: UUID


class GetMovieResponse(BaseModel):
    """GET MOVIE Response."""

    title: str
    year: int
    description: str
    actors: List[str]
    rating: float = Field(..., ge=0, le=10)


class GetCommentsRequest(BaseModel):
    """GET MOVIE COMMENTS Request."""

    movie: UUID


class GetCommentsResponse(BaseModel):
    """GET MOVIE COMMENTS Response."""

    class Comment(BaseModel):
        """Helper Comment class."""

        comment: str
        user: EmailStr

    comments: List[Comment]


class RateMovieRequest(BaseModel):
    """RATE MOVIE Request."""

    movie: UUID
    rating: float = Field(..., ge=0, le=10)


class RemoveMovieRatingRequest(BaseModel):
    """REMOVE MOVIE RATING Request."""

    movie: UUID


class CommentMovieRequest(BaseModel):
    """COMMENT MOVIE Request."""

    movie: UUID
    comment: str


class CreateMovieRequest(BaseModel):
    """CREATE MOVIE Request."""

    title: str
    year: int
    description: str
    actors: List[str]


class CreateMovieResponse(BaseModel):
    """CREATE MOVIE Response."""

    id: UUID
    title: str
