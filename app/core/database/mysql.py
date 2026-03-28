import pymysql

from app.core.config import settings


class MySQLDatabase:
    """Manages MySQL connection pool and client instance."""

    def __init__(self):
        """Initializes the database connection as None."""
        self._connection = None

    @property
    def connection(self):
        """Returns active MySQL connection, creating it if needed."""
        if self._connection is None or not self._connection.open:
            self._connection = pymysql.connect(
                host=settings.MYSQL_HOST,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                database=settings.MYSQL_DATABASE,
                port=settings.MYSQL_PORT,
                cursorclass=pymysql.cursors.DictCursor,
            )
        return self._connection


db_mysql = MySQLDatabase()
