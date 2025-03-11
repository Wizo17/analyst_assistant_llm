import psycopg2
from config.global_conf import global_conf
from utils.logger import log_message


DB_POSTGRES_HOST = global_conf.get("DB_POSTGRES_HOST")
DB_POSTGRES_PORT = global_conf.get("DB_POSTGRES_PORT")
DB_POSTGRES_NAME = global_conf.get("DB_POSTGRES_NAME")
DB_POSTGRES_USER = global_conf.get("DB_POSTGRES_USER")
DB_POSTGRES_PASSWORD = global_conf.get("DB_POSTGRES_PASSWORD")
DB_POSTGRES_DEFAULT_SCHEMA = global_conf.get("DB_POSTGRES_DEFAULT_SCHEMA")


class PostgresService:
    """
    PostgresService is a singleton class responsible for managing the connection
    to a PostgreSQL database.
    """
    _instance = None
    _conn_string = None
    _conn = None

    def __new__(cls):
        """
        Create a new instance of the PostgresService class if one does not already exist.

        Returns:
            PostgresService: The singleton instance of the PostgresService class.
        """
        if cls._instance is None:
            cls._instance = super(PostgresService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Initialize the PostgresService instance by creating a connection string
        and establishing a connection to the PostgreSQL database.
        """
        self._conn_string = f"postgresql+psycopg2://{DB_POSTGRES_USER}:{DB_POSTGRES_PASSWORD}@{DB_POSTGRES_HOST}:{DB_POSTGRES_PORT}/{DB_POSTGRES_NAME}"

        try:
            self._conn = psycopg2.connect(
                host=DB_POSTGRES_HOST,
                port=DB_POSTGRES_PORT,
                database=DB_POSTGRES_NAME,
                user=DB_POSTGRES_USER,
                password=DB_POSTGRES_PASSWORD
            )
            log_message("INFO", "Successfully connected to PostgreSQL.")
        except Exception as e:
            log_message("ERROR", f"Failed to connect to PostgreSQL: {str(e)}")

    def get_postgres_connection(self):
        """
        Get the current PostgreSQL connection. Reinitialize the connection if it is closed.

        Returns:
            connection: The PostgreSQL connection object.
        """
        if self._conn is None or self._conn.closed:
            self._initialize()

        return self._conn

    def get_postgres_connection_string(self):
        """
        Get the PostgreSQL connection string.

        Returns:
            str: The PostgreSQL connection string.
        """
        return self._conn_string

    def close_postgres_connection(self):
        """
        Close the current PostgreSQL connection.
        """
        if self._conn is not None:
            self._conn.close()
        log_message("INFO", "PostgreSQL connection closed.")


# Create a single instance for import
postgres_service = PostgresService()