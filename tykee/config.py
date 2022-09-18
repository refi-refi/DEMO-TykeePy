""" Config file to use environment variables across the project.
"""
from os import getenv, path
from dotenv import load_dotenv

load_dotenv()

LOGGER_LVL = getenv("LOGGER_LVL", "INFO")
DB_URL = getenv("DB_URL")

PROJECT_DIR = path.abspath(path.join(path.dirname(__file__), ".."))
LOG_DIR = path.join(PROJECT_DIR, "logs")
