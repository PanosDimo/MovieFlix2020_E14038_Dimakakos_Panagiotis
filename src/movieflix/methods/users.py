"""Users Methods."""
from flask import abort
from flask import current_app as app
from flask import g

from ..database import mongo
from ..models import users as models
from ..models.comments import CommentInDB, Comments
from ..models.movies import MovieInDB
from ..models.ratings import RatingInDB, Ratings
from ..schemas import users as schemas
from ..utils import crypto, tokens


def authenticate_user(credentials: schemas.AuthenticateUserRequest) -> models.UserWithToken:
    """Authenticate a user.

    :param credentials: The user's credentials.
    :return: User information with JWT token.
    """
    email = credentials.email
    password = credentials.password
    users = mongo.database.get_collection("users")
    res = users.find_one({"email": email})
    if res is None:
        abort(404, "User not found")
    user_ref = models.UserRef(**res)
    user = models.UserInDB(**res)
    if not crypto.verify(password, user.password):
        abort(404, "User not found")
    token = tokens.generate(user_ref)
    return models.UserWithToken(token=token, **res)


def register_user(info: schemas.RegisterUserRequest) -> models.User:
    """Register a new user.

    :param info: The user's information.
    :return: The user.
    """
    users = mongo.database.get_collection("users")
    # Check if user already exists.
    if users.find_one({"email": info.email}):
        abort(400, "User already exists")
    # Create the user.
    hashed_password = crypto.hashify(info.password)
    user = models.UserInDB(
        email=info.email, name=info.name, password=hashed_password, category=models.Role.USER
    )
    app.logger.info("Creating user %s", user.id)
    users.insert_one(user.dict(by_alias=True))
    return models.User(**user.dict(by_alias=True))


def get_my_comments() -> Comments:
    """Get user's comments.

    :return: The comments.
    """
    user: models.UserInDB = g.user
    movies = mongo.database.get_collection("movies")
    comments = mongo.database.get_collection("comments")
    data = comments.find({"user": user.email})
    res = []
    for datum in data:
        comment = CommentInDB(**datum)
        movie = MovieInDB(**movies.find_one({"_id": comment.movie}))
        new_datum = {**comment.dict(exclude={"movie"}), "movie": movie.title}
        res.append(new_datum)
    return Comments(comments=res)  # type: ignore


def get_all_comments() -> Comments:
    """Get all users' comments.

    :return: The comments.
    """
    movies = mongo.database.get_collection("movies")
    comments = mongo.database.get_collection("comments")
    data = comments.find({})
    res = []
    for datum in data:
        comment = CommentInDB(**datum)
        movie = MovieInDB(**movies.find_one({"_id": comment.movie}))
        new_datum = {**comment.dict(exclude={"movie"}), "movie": movie.title}
        res.append(new_datum)
    return Comments(comments=res)  # type: ignore


def get_my_ratings() -> Ratings:
    """Get user's ratings.

    :return: The ratings.
    """
    user: models.UserInDB = g.user
    movies = mongo.database.get_collection("movies")
    ratings = mongo.database.get_collection("ratings")
    data = ratings.find({"user": user.email})
    res = []
    for datum in data:
        rating = RatingInDB(**datum)
        movie = MovieInDB(**movies.find_one({"_id": rating.movie}))
        new_datum = {**rating.dict(exclude={"movie"}), "movie": movie.title}
        res.append(new_datum)
    return Ratings(ratings=res)  # type: ignore
