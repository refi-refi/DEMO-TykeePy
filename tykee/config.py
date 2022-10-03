""" Config file to access environment variables across the project."""
from os import getenv, path, makedirs

from dotenv import load_dotenv

load_dotenv()

LOGGER_LVL = getenv("LOGGER_LVL", "INFO")
DB_URL = getenv("DB_URL")

PROJECT_DIR = path.abspath(path.join(path.dirname(__file__), ".."))
LOG_DIR = path.join(PROJECT_DIR, "logs")
DATA_FILES_DIR = path.join(PROJECT_DIR, "tykee", "data", "files")
ML_MODELS_DIR = path.join(PROJECT_DIR, "tykee", "machine_learning", "model_saves")

makedirs(ML_MODELS_DIR, exist_ok=True)
