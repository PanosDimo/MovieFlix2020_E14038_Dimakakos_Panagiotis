"""Type Definitions."""
from typing import Any, Callable, Optional, Tuple, TypeVar

from flask import Response
from pydantic import BaseModel

Model = TypeVar("Model", bound=BaseModel)
Function = Callable[..., Any]
RouteResponsePre = Tuple[Optional[Model], int]
RouteResponse = Tuple[Response, int]
Route = Callable[..., RouteResponse]
RouteDecorator = Callable[[Route], Route]
