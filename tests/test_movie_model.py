from app.models.movie import Movie


def test_movie_string_representation():
    """Verifies that the string representation is uppercase and includes the year."""
    movie = Movie(movie_id=1, title="Aladdin", release_year=2006)
    assert str(movie) == "ALADDIN (2006)"


def test_movie_creation_with_none_fields():
    """Ensures the model instantiates correctly with optional fields set to None."""
    movie = Movie(movie_id=99, title="Test", release_year=2024)
    assert movie.description is None
    assert movie.rating is None


def test_movie_id_type():
    """Validates that the movie ID can be correctly interpreted as an integer."""
    movie = Movie(movie_id="123", title="Type Test", release_year=2020)
    assert int(movie.movie_id) == 123


def test_str_method_with_missing_year():
    """Checks the string output behavior when the release year is missing."""
    movie = Movie(movie_id=1, title="Mystery Movie", release_year=None)
    assert str(movie) == "MYSTERY MOVIE "
