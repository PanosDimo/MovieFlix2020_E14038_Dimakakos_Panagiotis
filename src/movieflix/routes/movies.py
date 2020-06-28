"""Movies Endpoints."""
from flask import Blueprint

from ..methods import movies as methods
from ..middleware.authentication import login_required
from ..middleware.authorization import is_admin
from ..middleware.content import ContentType, accepts
from ..middleware.schemas import request_schema, response_schema
from ..schemas import movies as schemas
from ..types import RouteResponsePre

blueprint = Blueprint("movies", __name__, url_prefix="/movies")


@blueprint.route("/", methods=["GET"])
@accepts(None)
@login_required
@request_schema(schemas.SearchMoviesRequest)
@response_schema(schemas.SearchMoviesResponse)
def search_movies(*, args: schemas.SearchMoviesRequest) -> RouteResponsePre:
    """Search movies endpoint."""
    result = methods.search_movies(criteria=args)
    return result, 200


@blueprint.route("/<movie>", methods=["GET"])
@accepts(None)
@login_required
@request_schema(schemas.GetMovieRequest)
@response_schema(schemas.GetMovieResponse)
def get_movie(*, args: schemas.GetMovieRequest, movie: str) -> RouteResponsePre:
    """Get movie endpoint."""
    result = methods.get_movie(args)
    return result, 200


@blueprint.route("/<movie>/comments", methods=["GET"])
@accepts(None)
@login_required
@request_schema(schemas.GetCommentsRequest)
@response_schema(schemas.GetCommentsResponse)
def get_comments(*, args: schemas.GetCommentsRequest, movie: str) -> RouteResponsePre:
    """Get comments endpoint."""
    result = methods.get_comments(args)
    return result, 200


@blueprint.route("/<movie>/rate", methods=["POST"])
@accepts(ContentType.JSON)
@login_required
@request_schema(schemas.RateMovieRequest)
@response_schema(None)
def rate_movie(*, args: schemas.RateMovieRequest, movie: str) -> RouteResponsePre:
    """Rate movie endpoint."""
    methods.rate_movie(args)
    return None, 204


@blueprint.route("/<movie>/rate", methods=["DELETE"])
@accepts(None)
@login_required
@request_schema(schemas.RemoveMovieRatingRequest)
@response_schema(None)
def remove_movie_rating(*, args: schemas.RemoveMovieRatingRequest, movie: str) -> RouteResponsePre:
    """Remove movie rating endpoint."""
    methods.remove_movie_rating(args)
    return None, 204


@blueprint.route("/<movie>/comment", methods=["POST"])
@accepts(ContentType.JSON)
@login_required
@request_schema(schemas.CommentMovieRequest)
@response_schema(None)
def comment_movie(*, args: schemas.CommentMovieRequest, movie: str) -> RouteResponsePre:
    """Comment movie endpoint."""
    methods.comment_movie(args)
    return None, 204


@blueprint.route("/", methods=["POST"])
@accepts(ContentType.JSON)
@login_required
@is_admin
@request_schema(schemas.CreateMovieRequest)
@response_schema(schemas.CreateMovieResponse)
def create_movie(*, args: schemas.CreateMovieRequest) -> RouteResponsePre:
    """Create movie endpoint."""
    result = methods.create_movie(args)
    return result, 201


@blueprint.route("/<movie>", methods=["PUT"])
@accepts(ContentType.JSON)
@login_required
@is_admin
@request_schema(schemas.UpdateMovieRequest)
@response_schema(None)
def update_movie(*, args: schemas.UpdateMovieRequest, movie: str) -> RouteResponsePre:
    """Create movie endpoint."""
    methods.update_movie(args)
    return None, 204
