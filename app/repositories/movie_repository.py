from datetime import datetime, timezone
from typing import List, Tuple

from app.core.config import settings
from app.core.database.mongo import db_mongo
from app.core.database.mysql import db_mysql
from app.models.movie import Movie


class MovieRepository:
    """Repository for handling movie data operations across MySQL and MongoDB."""

    def __init__(self):
        """Initializes database connections for SQL queries and NoSQL logging."""
        self.mysql = db_mysql
        self.log_col = db_mongo.connection[settings.MONGO_COLLECTION]

    def _map_to_movies(self, records: List[dict]) -> List[Movie]:
        """Maps database records to Movie model instances."""
        return [
            Movie(
                movie_id=r.get("film_id"),
                title=r.get("title", "Unknown"),
                release_year=r.get("release_year"),
                description=r.get("description"),
                rating=r.get("rating"),
            )
            for r in records
        ]

    def _save_log(
        self, query_text: str, results_count: int, search_type: str = "keyword", params: dict = None
    ):
        """Logs search activity to MongoDB."""
        try:
            now = datetime.now(timezone.utc)
            self.log_col.insert_one(
                {
                    "timestamp": now,
                    "search_type": search_type,
                    "params": params or {},
                    "results_count": results_count,
                    "date": now.strftime("%Y-%m-%d"),
                    "hour": now.hour,
                    "search_text": str(query_text).lower().strip(),
                }
            )
        except Exception as e:
            print(f"\n[❌ MongoDB Error]: {e}")

    def search(self, keyword: str, page: int = 1) -> Tuple[List[Movie], bool]:
        """Searches movies by title with pagination support."""
        limit, offset = 10, (page - 1) * 10
        sql = "SELECT film_id, title, release_year, description, rating FROM film WHERE LOWER(title) LIKE %s LIMIT %s OFFSET %s"

        with self.mysql.connection.cursor() as cur:
            cur.execute(sql, (f"%{keyword.lower().strip()}%", limit + 1, offset))
            results = cur.fetchall()

        movies = self._map_to_movies(results[:limit])

        if page == 1 and keyword.strip():
            self._save_log(keyword, len(movies))

        return movies, len(results) > limit

    def search_all(self, keyword: str) -> List[Movie]:
        """Performs a full keyword search with a safety limit.
        Note: Does not create a new log entry because the search
        was already logged on the first page (page=1).
        """
        limit = 1000
        sql = """
            SELECT film_id, title, release_year, description, rating 
            FROM film 
            WHERE LOWER(title) LIKE %s 
            LIMIT %s
        """

        with self.mysql.connection.cursor() as cur:
            cur.execute(sql, (f"%{keyword.lower().strip()}%", limit))
            results = cur.fetchall()

        movies = self._map_to_movies(results)
        return movies

    def find_by_category_and_year(
        self, categories: List[str], start: int, end: int, page: int = 1, limit: int = 10
    ) -> Tuple[List[Movie], bool]:
        """Filters movies by categories and release year range."""
        if not categories:
            return [], False

        if isinstance(categories, str):
            categories = [categories]

        offset = (page - 1) * limit
        placeholders = ", ".join(["%s"] * len(categories))
        sql = f"""
            SELECT f.film_id, f.title, f.release_year, f.description, f.rating
            FROM film f 
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
            WHERE c.name IN ({placeholders}) 
            AND f.release_year BETWEEN %s AND %s 
            LIMIT %s OFFSET %s
        """
        query_params = tuple(categories) + (start, end, limit + 1, offset)

        with self.mysql.connection.cursor() as cur:
            cur.execute(sql, query_params)
            results = cur.fetchall()

        movies = self._map_to_movies(results[:limit])

        if page == 1 and limit <= 50:
            self._save_log(
                ", ".join(categories),
                len(movies),
                "multi_category_filter",
                {"categories": categories, "start": start, "end": end},
            )

        return movies, len(results) > limit

    def get_all_categories(self) -> List[str]:
        """Retrieves a sorted list of all movie categories."""
        with self.mysql.connection.cursor() as cur:
            cur.execute("SELECT name FROM category ORDER BY name")
            return [r["name"] for r in cur.fetchall()]

    def get_year_range(self) -> Tuple[int, int]:
        """Retrieves the minimum and maximum release years from the database."""
        with self.mysql.connection.cursor() as cur:
            cur.execute("SELECT MIN(release_year), MAX(release_year) FROM film")
            res = cur.fetchone()
            min_y = res.get("MIN(release_year)") or 1900
            max_y = res.get("MAX(release_year)") or datetime.now(timezone.utc).year
            return int(min_y), int(max_y)
