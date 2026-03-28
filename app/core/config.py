import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration management via environment variables."""

    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "sakila")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))

    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB_NAME", "cinequery_logs")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "final_project__")


settings = Settings()
