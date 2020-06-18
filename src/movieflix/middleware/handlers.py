"""Error Handling Middleware."""
from logging import Logger

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from ..types import RouteResponse


def init_app(app: Flask) -> None:
    """Register error handlers.

    :param app: The flask application.
    """
    logger: Logger = app.logger

    @app.errorhandler(HTTPException)
    def http_error(error: HTTPException) -> RouteResponse:
        message = error.description
        status_code = error.code or 500
        logger.error(error)
        response = {"error": message}
        return jsonify(response), status_code

    @app.errorhandler(Exception)
    def internal_error(error: Exception) -> RouteResponse:
        logger.exception(error)
        response = {"error": "INTERNAL_ERROR"}
        return jsonify(response), 500

    logger.info("Registered error handlers middleware.")
