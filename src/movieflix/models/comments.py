"""Comments Models."""
from ._base import Base


class Comment(Base):
    """Comment Model."""

    comment: str
