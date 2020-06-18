"""User Endpoints Schemas."""
from uuid import UUID

from pydantic import BaseModel


class AuthenticateUserRequest(BaseModel):
    """Authenticate User Request."""

    email: str
    password: str


class AuthenticateUserResponse(BaseModel):
    """Authenticate User Response."""

    id: UUID
    name: str
    token: str
