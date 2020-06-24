"""HTTP Middleware."""
from logging import Logger
from typing import Any, Dict

from flask import Flask, g, request


def init_app(app: Flask) -> None:
    """Gather request args, view_args, json into one dictionary.

    :param app: The flask application.
    """
    logger: Logger = app.logger

    @app.before_request
    def gather() -> None:
        gathered: Dict[str, Any] = {}
        for key, value in request.args.items():
            if key in gathered:
                logger.warn(
                    "Key %s found @ args already exists " "and will be overwritten", key,
                )
            gathered[key] = value
        for key, value in request.form.items():
            if key in gathered:
                logger.warn(
                    "Key %s found @ form already exists " "and will be overwritten", key,
                )
            gathered[key] = value
        if request.get_json(silent=True):
            for key, value in request.json.items():
                if key in gathered:
                    logger.warn(
                        "Key %s found @ json already exists " "and will be overwritten", key,
                    )
                gathered[key] = value
        if request.files:
            gathered["files"] = request.files
        if request.view_args:
            for key, value in request.view_args.items():
                if key in gathered:
                    logger.warn(
                        "Key %s found @ view_args already exists " "and will be overwritten", key,
                    )
                gathered[key] = value
        g.input = gathered

    logger.info("Registered HTTP middleware.")
