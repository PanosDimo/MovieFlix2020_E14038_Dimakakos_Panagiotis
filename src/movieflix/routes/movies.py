"""Movies Endpoints."""
from flask import Blueprint

from ..methods import movies as methods
from ..middleware.authentication import login_required
from ..middleware.content import accepts
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
