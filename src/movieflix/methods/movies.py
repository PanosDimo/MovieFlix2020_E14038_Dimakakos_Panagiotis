"""Movies Methods."""
from typing import Any, Dict

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
