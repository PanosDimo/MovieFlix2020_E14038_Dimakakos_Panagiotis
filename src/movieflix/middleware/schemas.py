"""Schemas Middleware."""
import json
from functools import wraps
from typing import Any, Callable, Dict, Optional, Type

from flask import abort, g, jsonify
from pydantic import BaseModel, ValidationError

from ..types import Route, RouteDecorator, RouteResponse, RouteResponsePre

Schema = Type[BaseModel]
RoutePre = Callable[..., RouteResponsePre]


def request_schema(schema: Schema, kwarg: str = "args") -> RouteDecorator:
    """Parse input with the specified schema.

    :param schema: The schema to use.
    :param kwarg: The keyword argument to be used to inject the data.
    :return: The decorator.
    """

    def decorator(function: Route) -> Route:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> RouteResponse:
            input: Dict[str, Any] = g.input
            try:
                data = schema(**input)
            except ValidationError as error:
                abort(422, error.json())
            kwargs[kwarg] = data
            return function(*args, **kwargs)

        return wrapper

    return decorator


def response_schema(schema: Optional[Schema]) -> Callable[[RoutePre], Route]:
    """Parse response and convert through schema.

    :param schema: The schema to use.
    :return: The decorator.
    """

    def decorator(function: RoutePre) -> Route:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> RouteResponse:
            data, status = function(*args, **kwargs)
            if schema is not None and data is not None:
                return (
                    jsonify(json.loads(schema(**data.dict()).json())),
                    status,
                )
            if schema is not None and data is None:
                abort(500, "Do not specify a response model when returning a response.")
            if schema is None and data is not None:
                abort(500, "Specify a response model when returning a response.")
            return jsonify(), status

        return wrapper

    return decorator
