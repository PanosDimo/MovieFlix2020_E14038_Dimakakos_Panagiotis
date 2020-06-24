"""JWT Tokens."""
import json
from datetime import datetime, timedelta

import jwt

from ..models.users import UserRef
from ..settings import SETTINGS


def generate(payload: UserRef) -> str:
    """Generate JWT token.

    :param payload: The payload to include.
    :return: The JWT token.
    """
    delta = timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
    now = datetime.utcnow()
    return jwt.encode(
        {
            "exp": now + delta,
            "iat": now,
            "payload": json.loads(payload.json(by_alias=True)),
        },
        SETTINGS.SECRET_KEY,
        algorithm="HS256",
    ).decode()


def decode(token: str) -> UserRef:
    """Decode JWT token.

    :param token: The token to decode.
    :return: The decoded JWT token information.
    """
    return UserRef(**jwt.decode(token, SETTINGS.SECRET_KEY)["payload"])
