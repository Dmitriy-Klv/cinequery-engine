from typing import Dict, List

from app.core.config import settings
from app.core.database.mongo import db_mongo


class LogRepository:
    """Repository for managing and retrieving application logs from MongoDB."""

    def __init__(self):
        """Initializes the repository with a specific MongoDB collection."""
        self.collection = db_mongo.connection[settings.MONGO_COLLECTION]

    def get_top_queries(self, limit: int = 5) -> List[Dict]:
        """Aggregates and returns the most frequent search queries."""
        pipeline = [
            {"$group": {"_id": "$search_text", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit},
            {"$project": {"_id": 0, "query": "$_id", "count": 1}},
        ]
        return list(self.collection.aggregate(pipeline))

    def get_history(self, limit: int = 10) -> List[Dict]:
        """Retrieves and formats the recent log history."""
        logs = list(self.collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit))

        for log in logs:
            if "date" in log and "hour" in log:
                log["time"] = f"{log['date']} {log['hour']:02d}:00"
            else:
                log["time"] = (
                    log["timestamp"].strftime("%Y-%m-%d %H:%M") if "timestamp" in log else "N/A"
                )

            log["query"] = log.get("search_text", log.get("query", "N/A"))
            log["results_found"] = log.get("results_count", log.get("results_found", 0))

        return logs
