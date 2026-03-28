from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Movie:
    """Represents a movie entity with core metadata."""

    movie_id: int
    title: str
    release_year: int
    description: Optional[str] = None
    rating: Optional[str] = None
    length: Optional[int] = None
    categories: Optional[List[str]] = None

    @property
    def rating_text(self) -> str:
        """Provides a descriptive string for the movie rating."""
        ratings = {
            "G": "General (All ages)",
            "PG": "Parental Guidance",
            "PG-13": "Teens 13+",
            "R": "Restricted 17+",
            "NC-17": "Adults Only 18+",
        }
        return ratings.get(self.rating, "Not Rated")

    def __str__(self) -> str:
        """Returns a string representation of the movie."""
        year = f"({self.release_year})" if self.release_year else ""
        return f"{self.title.upper()} {year}"
