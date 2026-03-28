import random


class TestMovieRepository:
    """Class for testing repository and search history."""

    def _get_random_titles(self, movie_repo, count=10):
        """Helper method: Gets random names via search_all."""
        all_movies = movie_repo.search_all("")
        all_titles = [m.title for m in all_movies]

        sample_size = min(len(all_titles), count)
        return random.sample(all_titles, sample_size)

    def test_history_pagination_with_random_titles(self, movie_repo, log_repo):
        """Checking history pagination on random data from the database."""
        titles_count = 10
        random_titles = self._get_random_titles(movie_repo, count=titles_count)
        for title in random_titles:
            movie_repo.search(title, page=1)

        limit = 5
        page_1 = log_repo.get_history(limit=limit, skip=0)
        page_2 = log_repo.get_history(limit=limit, skip=limit)

        assert len(page_1) == limit, f"Page 1 should have {limit} items"
        assert len(page_2) == limit, f"Page 2 should have {limit} items"
        assert page_1[0]["_id"] != page_2[0]["_id"], "Pages must contain different records"

        print(f"\n[SUCCESS] Verified pagination for {len(random_titles)} random movies.")
