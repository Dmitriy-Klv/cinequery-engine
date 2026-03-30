import random

SQL_INJECTION_PAYLOADS = [
    "' OR '1'='1",
    "'; DROP TABLE film; --",
    "'; SELECT user, password FROM mysql.user; --",
    "%; --",
    "A" * 1000,
]


def get_random_titles(movie_repo, count=10):
    """Helper function to get unique random titles from DB."""
    all_movies = movie_repo.search_all("")
    all_titles = [m.title for m in all_movies]
    if not all_titles:
        return []
    sample_size = min(len(all_titles), count)
    return random.sample(all_titles, sample_size)
