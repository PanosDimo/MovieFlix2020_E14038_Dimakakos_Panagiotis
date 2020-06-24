"""Authorization Middleware."""
from functools import wraps
from typing import Any

from flask import abort, g

from ..models.users import Role, User
from ..types import Route, RouteResponse


def is_admin(function: Route) -> Route:
    """Require admin privileges.

    This decorator should be used in conjuction with
    :method:`flask.Flask.route` and
    :func:`movieflix.middleware.authentication.login_required`.

    :param function: The function to decorate.
    :return: The decorated function.
    """

    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> RouteResponse:
        user: User = g.user
        if user.category != Role.ADMIN:
            abort(403)
        return function(*args, **kwargs)

    return wrapper
