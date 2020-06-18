"""Base Model Definition."""
from datetime import datetime

from pydantic import BaseModel, Field


class Base(BaseModel):
    """Base Model."""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
