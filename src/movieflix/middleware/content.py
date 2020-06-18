"""Content Middleware."""
from enum import Enum
from functools import wraps
from typing import Any, Optional

from flask import abort, request

from ..types import RouteResponse, Route, RouteDecorator


class ContentType(str, Enum):
    """Content Types enumeration."""

    JSON = "application/json"

    def __str__(self) -> str:
        """Override __str__ builtin."""
        return self.value


def accepts(content_type: Optional[ContentType]) -> RouteDecorator:
    """Accept only the specified content type.

    :param content_type: The content type.
    :return: The decorator.
    """

    def decorator(function: Route) -> Route:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> RouteResponse:
            # No content expected, but request has content.
            if not content_type and request.content_length:
                abort(415, "Expected no content, but got content.")
            # Content expected, but request has no content.
            if content_type and not request.content_length:
                abort(
                    415,
                    f"Expected content of type {content_type}, "
                    f"but got no content",
                )
            # Content type and request content (check matching).
            actual_content_type = request.mimetype
            if (
                content_type
                and request.content_length
                and actual_content_type != content_type
            ):
                abort(
                    415,
                    f"Expected content of type {content_type}, "
                    f"but got {actual_content_type}",
                )
            return function(*args, **kwargs)

        return wrapper

    return decorator
