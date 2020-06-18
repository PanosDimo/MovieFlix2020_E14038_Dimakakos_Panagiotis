"""Encryption utilities."""
import bcrypt


def hashify(plain: str) -> bytes:
    """Hash a string.

    :param plain: The string to hash.
    :return: The hashed version of ``plain``.
    """
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt(10))


def verify(plain: str, crypted: bytes) -> bool:
    """Verify hashed string.

    :param plain: The string to verify.
    :param crypted: The encrypted string to verify against.
    :return: Whether the string is verified.
    """
    return bcrypt.checkpw(plain.encode(), crypted)
