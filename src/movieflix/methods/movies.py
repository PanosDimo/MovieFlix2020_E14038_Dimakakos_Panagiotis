"""Movies Methods."""
from typing import Any, Dict

from flask import abort

from ..database import mongo
from ..models import movies as models
from ..schemas import movies as schemas


def search_movies(criteria: schemas.SearchMoviesRequest) -> models.Movies:
    """Search movies.

    :param criteria: The search criteria.
    :return: The movies found.
    """
    movies = mongo.database.get_collection("movies")
    db_criteria: Dict[str, Any] = {}
    if criteria.title:
        db_criteria["title"] = criteria.title
    if criteria.year:
        db_criteria["year"] = criteria.year
    if criteria.actors:
        db_criteria["actors"] = {"$elemMatch": {"$in": criteria.actors}}
    results = [models.Movie(**result) for result in movies.find(db_criteria)]
    return models.Movies(movies=results)


def get_movie(args: schemas.GetMovieRequest) -> models.Movie:
    """Get movie.

    :param args: The arguments of the request.
    :return: The movie.
    """
    movies = mongo.database.get_collection("movies")
    datum = movies.find_one({"_id": args.movie})
    if not datum:
        abort(404, f"Movie {args.movie} not found")
    return models.Movie(**datum)


def get_comments(args: schemas.GetCommentsRequest) -> models.MovieDeref:
    """Get comments.

    :param args: The arguments of the request.
    :return: The comments.
    """
    movies = mongo.database.get_collection("movies")
    comments = mongo.database.get_collection("comments")
    datum = movies.find_one({"_id": args.movie})
    if not datum:
        abort(404, f"Movie {args.movie} not found")
    movie = models.Movie(**datum)
    data = comments.find({"_id": {"$in": movie.comments}})
    comments = [models.Comment(**datum) for datum in data]
    return models.MovieDeref(comments=comments, **movie.dict(by_alias=True, exclude={"comments"}))
