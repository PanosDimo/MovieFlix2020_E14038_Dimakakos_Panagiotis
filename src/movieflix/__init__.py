"""
Welcome to MovieFlix.

This application will help you search, rate and comment on movies.
"""
from pathlib import Path

from dotenv import load_dotenv

__version__ = "0.1.0"

BASE_DIR = Path(__file__).parent
PROJECT_DIR = BASE_DIR.parents[1]

load_dotenv()
