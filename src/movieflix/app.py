"""
Main Flask application.

This module contains the function `create_app` which will be used to
instantiate the Flask application.
"""
from logging import basicConfig, getLogger

from flask import Flask

from .settings import SETTINGS


def create_app() -> Flask:
    """Create Flask application.

    :return: The flask application.
    """
    app = Flask(__name__, static_folder=None)
    app.config["SETTINGS"] = SETTINGS

    basicConfig(
        format=SETTINGS.LOG_FMT,
        datefmt=SETTINGS.LOG_DATEFMT,
        level=str(SETTINGS.LOG_LEVEL),
    )
    getLogger("werkzeug").disabled = True

    from .middleware import handlers, http, logging

    handlers.init_app(app)
    http.init_app(app)
    logging.init_app(app)

    from .database import mongo

    mongo.init_app(app)

    from . import routes

    routes.init_app(app)

    app.logger.info("Application created successfully.")

    return app
