"""User Endpoints Schemas."""
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from ..models.users import Role


class AuthenticateUserRequest(BaseModel):
    """AUTHENTICATE USER Request."""

    email: str
    password: str


class AuthenticateUserResponse(BaseModel):
    """AUTHENTICATE USER Response."""

    id: UUID
    name: str
    category: Role
    token: str


class RegisterUserRequest(BaseModel):
    """REGISTER USER Request."""

    email: EmailStr
    name: str
    password: str


class RegisterUserResponse(BaseModel):
    """REGISTER USER Response."""

    id: UUID
    email: EmailStr
    name: str
    category: Role


class GetCommentsResponse(BaseModel):
    """GET USER COMMENTS Response."""

    class Comment(BaseModel):
        """Helper Comment class."""

        id: UUID
        movie: str
        comment: str

    comments: List[Comment]


class GetAllCommentsResponse(BaseModel):
    """GET ALL USERS COMMENTS Response."""

    class Comment(BaseModel):
        """Helper Comment class."""

        id: UUID
        movie: str
        user: EmailStr
        comment: str

    comments: List[Comment]


class GetRatingsResponse(BaseModel):
    """GET USER RATINGS Response."""

    class Rating(BaseModel):
        """Helper Rating class."""

        id: UUID
        movie: str
        rating: float = Field(..., ge=0, le=10)

    ratings: List[Rating]
