"""Type Definitions."""
from typing import Any, Callable, Optional, Tuple

from flask import Response
from pydantic import BaseModel

Function = Callable[..., Any]
RouteResponsePre = Tuple[Optional[BaseModel], int]
RouteResponse = Tuple[Response, int]
Route = Callable[..., RouteResponse]
RouteDecorator = Callable[[Route], Route]
