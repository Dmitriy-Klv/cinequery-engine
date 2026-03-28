import pytest


class TestMovieRepository:
    """Integration tests using unique random titles from database."""

    def test_history_pagination_with_random_titles(
        self, movie_repo, log_repo, random_titles_factory
    ):
        """
        Verifies history pagination by:
        1. Fetching 10 UNIQUE random titles .
        2. Searching for each title via a loop.
        3. Checking that the history is correctly split into pages.
        """
        count_to_test = 10

        random_titles = random_titles_factory(count=count_to_test)

        print(f"\n[STARTING SEARCH FOR {len(random_titles)} UNIQUE TITLES]")

        for title in random_titles:
            print(f"Feeding search for: {title}")
            movie_repo.search(title, page=1)

        all_history = log_repo.get_history(limit=10)

        page_1 = all_history[:5]
        page_2 = all_history[5:10]

        # Assertions
        assert len(page_1) == 5, f"Expected 5 items on page 1, got {len(page_1)}"
        assert len(page_2) == 5, f"Expected 5 items on page 2, got {len(page_2)}"

        # Compare entire objects to ensure they are different unique records
        assert page_1[0] != page_2[0], "Records on Page 1 and Page 2 must be different movies"

        print(
            f"\n[SUCCESS] History successfully populated with {len(random_titles)} unique titles."
        )
