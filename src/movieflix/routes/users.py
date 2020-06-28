"""Users Endpoints."""
from flask import Blueprint

from ..methods import users as methods
from ..middleware.authentication import login_required
from ..middleware.authorization import is_admin
from ..middleware.content import ContentType, accepts
from ..middleware.schemas import request_schema, response_schema
from ..schemas import users as schemas
from ..types import RouteResponsePre

blueprint = Blueprint("users", __name__, url_prefix="/users")


@blueprint.route("/authenticate", methods=["POST"])
@accepts(ContentType.JSON)
@request_schema(schemas.AuthenticateUserRequest)
@response_schema(schemas.AuthenticateUserResponse)
def authenticate_user(*, args: schemas.AuthenticateUserRequest) -> RouteResponsePre:
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


@blueprint.route("/my/comments", methods=["GET"])
@accepts(None)
@login_required
@response_schema(schemas.GetCommentsResponse)
def get_my_comments() -> RouteResponsePre:
    """Get user's comments endpoint."""
    result = methods.get_my_comments()
    return result, 200


@blueprint.route("/comments", methods=["GET"])
@accepts(None)
@login_required
@is_admin
@response_schema(schemas.GetAllCommentsResponse)
def get_all_comments() -> RouteResponsePre:
    """Get all users' comments endpoint."""
    result = methods.get_all_comments()
    return result, 200
