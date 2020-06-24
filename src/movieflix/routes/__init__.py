"""Application Routes."""
from flask import Flask


def init_app(app: Flask) -> None:
    """Register endpoints.

    :param app: The flask application.
    """
    from . import movies, users

    app.register_blueprint(movies.blueprint)
    app.register_blueprint(users.blueprint)

    app.logger.info("Registered endpoints.")
