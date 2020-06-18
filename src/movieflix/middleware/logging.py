"""Logging Middleware."""
from logging import Logger
from time import time

from flask import Flask, Response, g, request


def init_app(app: Flask) -> None:
    """Register logging middleware.

    :param app: The flask application.
    """
    logger: Logger = app.logger

    @app.before_request
    def log_request() -> None:
        g.start_time = time()
        logger.info(
            "%s %s %s @ %s",
            request.remote_addr,
            request.scheme.upper(),
            request.method,
            request.full_path if request.query_string else request.path,
        )

    @app.after_request
    def log_response(response: Response) -> Response:
        logger.info(
            "%s %s %s @ %s %d (%d ms)",
            request.remote_addr,
            request.scheme.upper(),
            request.method,
            request.full_path if request.query_string else request.path,
            response.status_code,
            round((time() - g.start_time) * 1000),
        )
        return response

    logger.info("Registered logging middleware.")
