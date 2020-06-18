"""Users Endpoints."""
from flask import Blueprint

from ..methods import users as methods
from ..middleware.content import ContentType, accepts
from ..middleware.schemas import request_schema, response_schema
from ..schemas import users as schemas
from ..types import RouteResponsePre

blueprint = Blueprint("users", __name__, url_prefix="/users")


@blueprint.route("/authenticate", methods=["POST"])
@accepts(ContentType.JSON)
@request_schema(schemas.AuthenticateUserRequest)
@response_schema(schemas.AuthenticateUserResponse)
def authenticate_user(
    *, args: schemas.AuthenticateUserRequest
) -> RouteResponsePre:  # type: ignore
    """Authenticate user endpoint.

    :return: The flask response.
    """
    result = methods.authenticate_user(credentials=args)
    return result, 200
