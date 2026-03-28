import pytest

from app.models.movie import Movie


class TestMovieRepository:
    """A set of tests to test the logic of the movie repository."""

    def test_multiple_search_queries(self, movie_repo):
        """Verifies search functionality by iterating through a list of titles and simulating multiple 'clicks'."""

        movies_to_search = [
            "ACADEMY DINOSAUR",
            "ALABAMA DEVIL",
            "AGENT TRUMAN",
            "ALADDIN CALENDAR",
            "ALIEN CENTER",
        ]

        press_count = 1

        for title in movies_to_search:
            for i in range(press_count):
                movies, has_more = movie_repo.search(title, page=1)

                assert len(movies) > 0, f"Movie '{title}' was not found in the database!"

                assert (
                    title.upper() in movies[0].title.upper()
                ), f"Expected {title}, but received {movies[0].title}"

                print(f"Search for '{title}' successful (Attempt {i + 1})")

    def test_search_five_specific_titles(self, movie_repo):
        """Verifies search functionality for 5 standard movie titles."""

        titles_to_check = [
            "ARIZONA BANG",
            "BAKED CLEOPATRA",
            "BEACH HEARTBREAKERS",
            "CAT CONEHEADS",
            "EGG IGBY",
        ]

        press_count = 1

        for title in titles_to_check:
            for i in range(press_count):
                movies, _ = movie_repo.search(title, page=1)

                assert len(movies) > 0, f"Search Failed: Movie '{title}' not found."
                assert title.upper() in movies[0].title.upper(), f"Mismatch for {title}"

                print(f"Verified: {title} (Attempt {i + 1})")

    def test_check_every_category_one_by_one(self, movie_repo):
        """Checks that each category in the database returns movies."""
        all_categories = movie_repo.get_all_categories()

        for name in all_categories:
            movies, has_more = movie_repo.find_by_category_and_year([name], 1900, 2026, page=1)

            assert len(movies) > 0, f"Error: category '{name}' empty!"
            assert isinstance(
                movies[0], Movie
            ), f"Error: The data in '{name}' is not a Movie object"

    def test_search_by_keyword_limit(self, movie_repo):
        """Verifies that the search returns a maximum of 10 movies per page."""
        movies, has_more = movie_repo.search("a", page=1)
        assert len(movies) <= 10
        assert isinstance(movies[0], Movie)

    def test_pagination_logic(self, movie_repo):
        """Checks the correctness of the has_more pagination flag."""
        movies, has_more = movie_repo.search("e", page=1)
        if len(movies) == 10:
            assert has_more is True

    def test_get_all_categories(self, movie_repo):
        """Ensures the list of categories is retrieved correctly from the database."""
        categories = movie_repo.get_all_categories()
        assert len(categories) > 0
        assert "Action" in categories or "Horror" in categories

    def test_year_range(self, movie_repo):
        """Validates the release year range retrieval."""
        min_y, max_y = movie_repo.get_year_range()
        assert min_y <= max_y
        assert min_y > 1900

    def test_search_no_results(self, movie_repo):
        """Checks that a non-existent movie search returns an empty result set."""
        movies, has_more = movie_repo.search("zxy_non_existent_movie_123", page=1)
        assert len(movies) == 0
        assert has_more is False

    def test_find_by_category_and_year_logic(self, movie_repo):
        """Validates filtering by category and release year range."""
        categories = movie_repo.get_all_categories()
        if not categories:
            pytest.skip("No categories in database")

        category = categories[0]
        movies, has_more = movie_repo.find_by_category_and_year(category, 1900, 2026, page=1)

        assert isinstance(movies, list)
        if movies:
            assert isinstance(movies[0], Movie)

    def test_find_by_category_exact_year(self, movie_repo):
        """Verifies filtering results for a specific exact year."""
        movies, _ = movie_repo.find_by_category_and_year("Action", 2006, 2006, page=1)
        for movie in movies:
            assert movie.release_year == 2006

    def test_search_case_insensitivity(self, movie_repo):
        """Checking that the search is case-insensitive (Title vs. title)."""
        results_upper, _ = movie_repo.search("ACADEMY", page=1)
        results_lower, _ = movie_repo.search("academy", page=1)

        assert len(results_upper) == len(results_lower)
        if results_upper:
            assert results_upper[0].movie_id == results_lower[0].movie_id

    def test_find_by_category_multiple_pages(self, movie_repo):
        """Checking pagination when filtering by category"""
        categories = movie_repo.get_all_categories()
        if not categories:
            pytest.skip("Categories are missing from the database")

        cat = categories[0]
        movies_p1, has_more_p1 = movie_repo.find_by_category_and_year([cat], 1900, 2026, page=1)

        if has_more_p1:
            movies_p2, _ = movie_repo.find_by_category_and_year([cat], 1900, 2026, page=2)
            if movies_p1 and movies_p2:
                assert movies_p1[0].movie_id != movies_p2[0].movie_id

    def test_search_special_characters(self, movie_repo):
        """Checking search using special characters (protection against crashes)."""
        movies, _ = movie_repo.search("'; --", page=1)
        assert isinstance(movies, list)
