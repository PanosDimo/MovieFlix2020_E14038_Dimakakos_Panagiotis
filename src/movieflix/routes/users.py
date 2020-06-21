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
) -> RouteResponsePre:
    """Authenticate user endpoint."""
    result = methods.authenticate_user(credentials=args)
    return result, 200


@blueprint.route("/register", methods=["POST"])
@accepts(ContentType.JSON)
@request_schema(schemas.RegisterUserRequest)
@response_schema(schemas.RegisterUserResponse)
def register_user(*, args: schemas.RegisterUserRequest) -> RouteResponsePre:
    """Register user endpoint."""
    result = methods.register_user(info=args)
    return result, 201
