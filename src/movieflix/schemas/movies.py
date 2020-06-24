"""Movies Schemas."""
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator


class SearchMoviesRequest(BaseModel):
    """Search Movies Request."""

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
    """Search Movies Response."""

    class Movie(BaseModel):
        """Helper Movie class."""

        id: UUID
        title: str

    movies: List[Movie]
