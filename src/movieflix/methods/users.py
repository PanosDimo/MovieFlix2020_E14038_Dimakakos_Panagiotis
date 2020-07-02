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
        new_datum = {**comment.dict(by_alias=True, exclude={"movie"}), "movie": movie.title}
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
        new_datum = {**comment.dict(by_alias=True, exclude={"movie"}), "movie": movie.title}
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
        new_datum = {**rating.dict(by_alias=True, exclude={"movie"}), "movie": movie.title}
        res.append(new_datum)
    return Ratings(ratings=res)  # type: ignore


def delete_my_comment(args: schemas.DeleteCommentRequest) -> None:
    """Delete user's comment.

    :param args: The arguments.
    """
    user: models.UserInDB = g.user
    comments = mongo.database.get_collection("comments")
    movies = mongo.database.get_collection("movies")
    users = mongo.database.get_collection("users")
    datum = comments.find_one({"_id": args.comment, "user": user.email})
    if not datum:
        abort(404, f"Comment {args.comment} not found")
    comment = CommentInDB(**datum)
    movie_id = comment.movie
    datum = movies.find_one({"_id": movie_id})
    movie = MovieInDB(**datum)
    movie.comments.remove(args.comment)
    movies.update_one({"_id": movie_id}, {"$set": movie.dict(by_alias=True, exclude={"id"})})
    user.comments.remove(args.comment)
    users.update_one({"_id": user.id}, {"$set": user.dict(by_alias=True, exclude={"id"})})
    comments.delete_one({"_id": args.comment, "user": user.email})
    return None


def delete_my_account() -> None:
    """Delete user's account."""
    user: models.UserInDB = g.user
    users = mongo.database.get_collection("users")
    users.delete_one({"_id": user.id})
    return None


def delete_comment(args: schemas.DeleteCommentRequest) -> None:
    """Delete any user's comment.

    :param args: The arguments.
    """
    comments = mongo.database.get_collection("comments")
    movies = mongo.database.get_collection("movies")
    users = mongo.database.get_collection("users")
    datum = comments.find_one({"_id": args.comment})
    if not datum:
        abort(404, f"Comment {args.comment} not found")
    comment = CommentInDB(**datum)
    movie_id = comment.movie
    user_email = comment.user
    datum = movies.find_one({"_id": movie_id})
    movie = MovieInDB(**datum)
    movie.comments.remove(args.comment)
    movies.update_one({"_id": movie_id}, {"$set": movie.dict(by_alias=True, exclude={"id"})})
    datum = users.find_one({"email": user_email})
    user = models.UserInDB(**datum)
    user.comments.remove(args.comment)
    users.update_one({"_id": user.id}, {"$set": user.dict(by_alias=True, exclude={"id"})})
    comments.delete_one({"_id": args.comment, "user": user.email})
    return None


def get_users() -> models.Users:
    """Get all users.

    :return: The users.
    """
    users = mongo.database.get_collection("users")
    data = users.find()
    return models.Users(users=[models.User(**datum) for datum in data])


def delete_user(args: schemas.DeleteUserRequest) -> None:
    """Delete user.

    :param args: The arguments.
    """
    users = mongo.database.get_collection("users")
    datum = users.find_one({"_id": args.user})
    if not datum:
        abort(404, f"User {args.user} not found")
    user = models.UserInDB(**datum)
    if user.category == models.Role.ADMIN:
        abort(400, "Bad request")
    users.delete_one({"_id": user.id})
    return None


def make_admin(args: schemas.MakeAdminRequest) -> None:
    """Make admin user.

    :param args: The arguments.
    """
    users = mongo.database.get_collection("users")
    datum = users.find_one({"_id": args.user})
    if not datum:
        abort(404, f"User {args.user} not found")
    user = models.UserInDB(**datum)
    if user.category == models.Role.ADMIN:
        return None
    user.category = models.Role.ADMIN
    users.update_one({"_id": user.id}, {"$set": user.dict(by_alias=True, exclude={"id"})})
    return None
