import pytest
from tests.utils import SQL_INJECTION_PAYLOADS


class TestSecurity:
    """Security testing suite to ensure protection against injections."""

    @pytest.mark.parametrize("malicious_input", SQL_INJECTION_PAYLOADS)
    def test_search_sql_injection_resilience(self, movie_repo, malicious_input):
        """Checks that SQL injection attempts are treated as plain text."""
        try:
            movies, _ = movie_repo.search(malicious_input, page=1)
            assert isinstance(movies, list)
            assert len(movies) == 0
        except Exception as e:
            pytest.fail(f"SQL Injection protection failed on input {malicious_input}: {e}")

    def test_search_with_quotes(self, movie_repo):
        """Ensures that single quotes (common in names) don't break the query."""
        quote_title = "L'AMOUR"
        movies, _ = movie_repo.search(quote_title, page=1)
        assert isinstance(movies, list)

    def test_mongodb_injection_resilience(self, movie_repo, log_repo):
        """Checks that NoSQL operators are logged as text, not executed by MongoDB."""
        mongo_payload = "{'$gt': ''}"
        movie_repo.search(mongo_payload, page=1)

        history = log_repo.get_history(limit=1)
        assert history[0]["query"] == mongo_payload