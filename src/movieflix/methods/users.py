"""Users Methods."""
from flask import abort

from ..database import mongo
from ..models import users as models
from ..schemas import users as schemas
from ..utils import crypto, tokens


def authenticate_user(
    credentials: schemas.AuthenticateUserRequest,
) -> models.UserWithToken:
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
