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
    """Authenticate user endpoint."""
    result = methods.search_movies(criteria=args)
    return result, 200
