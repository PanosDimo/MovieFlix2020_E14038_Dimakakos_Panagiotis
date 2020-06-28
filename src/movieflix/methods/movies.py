"""Movies Methods."""
from datetime import datetime
from typing import Any, Dict

from flask import abort, g

from ..database import mongo
from ..models import movies as models
from ..models.comments import CommentInDB
from ..models.ratings import RatingInDB
from ..models.users import UserInDB
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


def rate_movie(args: schemas.RateMovieRequest) -> None:
    """Rate movie.

    :param args: The arguments of the request.
    """
    movies = mongo.database.get_collection("movies")
    ratings = mongo.database.get_collection("ratings")
    user: UserInDB = g.user
    datum = movies.find_one({"_id": args.movie})
    if not datum:
        abort(404, f"Movie {args.movie} not found")
    movie = models.MovieInDB(**datum)
    rating = RatingInDB(movie=args.movie, user=user.email, rating=args.rating)
    datum = ratings.find_one({"movie": args.movie, "user": user.email})
    if not datum:
        ratings.insert_one(rating.dict(by_alias=True))
    else:
        rating = RatingInDB(**datum)
        rating.rating = args.rating
        rating.updated_at = datetime.utcnow()
        ratings.update_one(
            {"movie": args.movie, "user": user.email},
            {"$set": rating.dict(by_alias=True, exclude={"id"})},
        )
    data = ratings.find({"movie": args.movie})
    new_rating = 0.0
    num = 0
    for datum in data:
        new_rating += RatingInDB(**datum).rating
        num += 1
    if num:
        new_rating = new_rating / num
    movie.rating = new_rating
    movie.updated_at = datetime.utcnow()
    movies.update_one({"_id": movie.id}, {"$set": movie.dict(by_alias=True, exclude={"id"})})
    return None


def remove_movie_rating(args: schemas.RemoveMovieRatingRequest) -> None:
    """Remove movie rating.

    :param args: The arguments of the request.
    """
    movies = mongo.database.get_collection("movies")
    ratings = mongo.database.get_collection("ratings")
    user: UserInDB = g.user
    datum = movies.find_one({"_id": args.movie})
    if not datum:
        abort(404, f"Movie {args.movie} not found")
    movie = models.MovieInDB(**datum)
    datum = ratings.find_one({"movie": args.movie, "user": user.email})
    if not datum:
        return None
    ratings.delete_one({"movie": args.movie, "user": user.email})
    data = ratings.find({"movie": args.movie})
    new_rating = 0.0
    num = 0
    for datum in data:
        new_rating += RatingInDB(**datum).rating
        num += 1
    if num:
        new_rating = new_rating / num
    movie.rating = new_rating
    movie.updated_at = datetime.utcnow()
    movies.update_one({"_id": movie.id}, {"$set": movie.dict(by_alias=True, exclude={"id"})})
    return None


def comment_movie(args: schemas.CommentMovieRequest) -> None:
    """Comment movie.

    :param args: The arguments of the request.
    """
    movies = mongo.database.get_collection("movies")
    comments = mongo.database.get_collection("comments")
    users = mongo.database.get_collection("users")
    user: UserInDB = g.user
    datum = movies.find_one({"_id": args.movie})
    if not datum:
        abort(404, f"Movie {args.movie} not found")
    movie = models.MovieInDB(**datum)
    comment = CommentInDB(movie=args.movie, user=user.email, comment=args.comment)
    movie.comments.append(comment.id)
    movie.updated_at = datetime.utcnow()
    user.comments.append(comment.id)
    user.updated_at = datetime.utcnow()
    comments.insert_one(comment.dict(by_alias=True))
    movies.update_one({"_id": movie.id}, {"$set": movie.dict(by_alias=True, exclude={"id"})})
    users.update_one({"_id": user.id}, {"$set": user.dict(by_alias=True, exclude={"id"})})
    return None


def create_movie(args: schemas.CreateMovieRequest) -> models.MovieInDB:
    """Create movie.

    :param args: The arguments.
    :return: The created movie.
    """
    movies = mongo.database.get_collection("movies")
    movie = models.MovieInDB(
        title=args.title, year=args.year, description=args.description, actors=args.actors
    )
    movies.insert_one(movie.dict(by_alias=True))
    return movie


def update_movie(args: schemas.UpdateMovieRequest) -> None:
    """Update movie.

    :param args: The arguments.
    """
    movies = mongo.database.get_collection("movies")
    datum = movies.find_one({"_id": args.movie})
    if not datum:
        abort(404, f"Movie {args.movie} not found")
    movie = models.MovieInDB(**datum)
    update = args.dict(exclude={"movie"}, exclude_none=True)
    if not update:
        return None
    movie = movie.copy(update=update)
    movie.updated_at = datetime.utcnow()
    movies.update_one({"_id": movie.id}, {"$set": movie.dict(by_alias=True, exclude={"id"})})
    return None


def delete_movie(args: schemas.DeleteMovieRequest) -> None:
    """Delete movie.

    :param args: The arguments.
    """
    movies = mongo.database.get_collection("movies")
    datum = movies.find_one({"_id": args.movie})
    if not datum:
        abort(404, f"Movie {args.movie} not found")
    movies.delete_one({"_id": args.movie})
    return None
