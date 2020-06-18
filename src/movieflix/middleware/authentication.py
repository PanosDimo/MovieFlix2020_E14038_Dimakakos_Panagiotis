"""Authentication Middleware."""
from functools import wraps
from typing import Any

import jwt
from flask import abort, g, request

from ..database import mongo
from ..models.users import User
from ..types import Route, RouteResponse
from ..utils import tokens


def login_required(function: Route) -> Route:
    """Require logged in user.

    This decorator should be used in conjuction with
    :method:`~flask.Flask.route`.

    :param function: The function to decorate.
    :return: The decorated function.
    """

    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> RouteResponse:
        authentication = request.headers.get("Authorization")
        if not authentication:
            abort(401)
        if "Bearer " not in authentication:
            abort(400, 'No "Bearer" in "Authorization" header')
        token = authentication.split("Bearer ")[1]
        try:
            user_id = tokens.decode(token).id
        except jwt.ExpiredSignatureError:
            abort(401, "Token has expired")
        except jwt.DecodeError:
            abort(401, "Token is not valid")
        users = mongo.database.get_collection("users")
        res = users.find_one({"_id": user_id})
        if res is None:
            abort(401)
        g.user = User(**res)
        return function(*args, **kwargs)

    return wrapper
