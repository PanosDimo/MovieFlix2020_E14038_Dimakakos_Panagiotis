"""User Endpoints Schemas."""
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr

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
