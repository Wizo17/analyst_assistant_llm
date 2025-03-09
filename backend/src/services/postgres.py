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
    # TODO Write documentation
    _instance = None
    _conn_string = None
    _conn = None


    def __new__(cls):
        # TODO Write documentation
        if cls._instance is None:
            cls._instance = super(PostgresService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    

    def _initialize(self):
        # TODO Write documentation
        self._conn_string = f"postgresql+psycopg2://{DB_POSTGRES_USER}:{DB_POSTGRES_PASSWORD}@{DB_POSTGRES_HOST}:{DB_POSTGRES_PORT}/{DB_POSTGRES_NAME}"

        try:
            self._conn = psycopg2.connect(
                host=DB_POSTGRES_HOST,
                port=DB_POSTGRES_PORT,
                database=DB_POSTGRES_NAME,
                user=DB_POSTGRES_USER,
                password=DB_POSTGRES_PASSWORD
            )
            #log_message("INFO", "Successful PostgreSQL connection!")
        except Exception as e:
            log_message("ERROR", f"Connection to postgres failed : {e}")


    def get_postgres_connection(self):
        # TODO Write documentation
        if self._conn.closed:
            self._initialize()

        return self._conn            

    
    def get_postgres_connection_string(self):
        # TODO Write documentation
        return self._conn_string
    

    def close_postgres_connection(self):
        self._conn.close() 


postgres_service = PostgresService()
