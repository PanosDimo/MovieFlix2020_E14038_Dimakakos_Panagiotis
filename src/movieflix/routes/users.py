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


@blueprint.route("/comments/<comment>", methods=["DELETE"])
@accepts(None)
@login_required
@is_admin
@request_schema(schemas.DeleteCommentRequest)
@response_schema(None)
def delete_comment(*, args: schemas.DeleteCommentRequest, comment: str) -> RouteResponsePre:
    """Delete any user's comment endpoint."""
    methods.delete_comment(args)
    return None, 204


@blueprint.route("/my/ratings", methods=["GET"])
@accepts(None)
@login_required
@response_schema(schemas.GetRatingsResponse)
def get_ratings() -> RouteResponsePre:
    """Get user's ratings endpoint."""
    result = methods.get_my_ratings()
    return result, 200


@blueprint.route("/my/comments/<comment>", methods=["DELETE"])
@accepts(None)
@login_required
@request_schema(schemas.DeleteCommentRequest)
@response_schema(None)
def delete_my_comment(*, args: schemas.DeleteCommentRequest, comment: str) -> RouteResponsePre:
    """Delete user's comment endpoint."""
    methods.delete_my_comment(args)
    return None, 204


@blueprint.route("/my/account", methods=["DELETE"])
@accepts(None)
@login_required
@response_schema(None)
def delete_my_account() -> RouteResponsePre:
    """Delete user's account."""
    methods.delete_my_account()
    return None, 204
