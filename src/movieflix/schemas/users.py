"""User Endpoints Schemas."""
from uuid import UUID

from pydantic import BaseModel, EmailStr

from ..models.users import Role


class AuthenticateUserRequest(BaseModel):
    """Authenticate User Request."""

    email: str
    password: str


class AuthenticateUserResponse(BaseModel):
    """Authenticate User Response."""

    id: UUID
    name: str
    category: Role
    token: str


class RegisterUserRequest(BaseModel):
    """Register User Request."""

    email: EmailStr
    name: str
    password: str


class RegisterUserResponse(BaseModel):
    """Register User Response."""

    id: UUID
    email: EmailStr
    name: str
    category: Role
