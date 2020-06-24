"""Database Initialization."""
from typing import Optional

from flask import Flask
from pymongo import MongoClient
from pymongo.database import Database

from .settings import Settings


class Mongo:
    """Mongo Connection Class."""

    client: MongoClient
    database: Database

    def __init__(self, app: Optional[Flask] = None) -> None:
        """Initialize instance."""
        if app:
            settings: Settings = app.config["SETTINGS"]
            self.client = MongoClient(settings.MONGODB_URI)
            self.database = self.client.get_database(settings.MONGODB_DB)

    def init_app(self, app: Flask) -> None:
        """Initialize connection from application."""
        settings: Settings = app.config["SETTINGS"]
        self.client = MongoClient(settings.MONGODB_URI)
        self.database = self.client.get_database(settings.MONGODB_DB)
        app.logger.info("Initialized MongoDB connection.")


mongo = Mongo()
