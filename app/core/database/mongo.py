import pymongo

from app.core.config import settings


class MongoDatabase:
    """Manages MongoDB connection and client instance."""

    def __init__(self):
        """Initializes the database client as None."""
        self._client = None

    @property
    def connection(self):
        """Returns the MongoDB database instance."""
        if self._client is None:
            self._client = pymongo.MongoClient(settings.MONGO_URI)
        return self._client[settings.MONGO_DB]

    def close(self):
        """Safely closes MongoDB client."""
        if self._client:
            self._client.close()
            self._client = None


db_mongo = MongoDatabase()
