import random

import pytest

from app.repositories.log_repository import LogRepository
from app.repositories.movie_repository import MovieRepository


@pytest.fixture
def movie_repo():
    return MovieRepository()


@pytest.fixture
def log_repo():
    return LogRepository()


@pytest.fixture
def random_titles_factory(movie_repo):
    """
    Factory fixture to fetch a unique set of random titles from DB.
    """

    def _generate_titles(count=10):
        all_movies = movie_repo.search_all("")
        all_titles = [m.title for m in all_movies]

        if not all_titles:
            return []

        random.shuffle(all_titles)

        sample_size = min(len(all_titles), count)
        return random.sample(all_titles, sample_size)

    return _generate_titles
