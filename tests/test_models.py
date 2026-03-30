from app.models.movie import Movie


def test_movie_creation():
    """Verifies Movie model instantiation and its string representation."""
    movie = Movie(movie_id=1, title="ACADEMY DINOSAUR", release_year=2006)
    assert movie.title == "ACADEMY DINOSAUR"
    assert str(movie) == "ACADEMY DINOSAUR (2006)"
