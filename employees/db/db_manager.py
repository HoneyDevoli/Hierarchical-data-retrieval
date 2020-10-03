import psycopg2


class DatabaseManager:
    """Context manager for working with db.
    :param database: name of db
    :param user: user login
    :param password: user password
    """
    def __init__(self,
                 database: str,
                 user: str,
                 password: str):
        self.database = database
        self.user = user
        self.password = password

    def __enter__(self) -> psycopg2.extensions.connection:
        """Create active database connection.
        :return: connection
        """
        self.conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password
        )
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Close database connection.
        :return: None"""
        self.conn.close()
