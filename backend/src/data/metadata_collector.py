import json
from config.global_conf import global_conf
from services.postgres import postgres_service
from templates.database_schema import POSTGRES_QUERY
from utils.logger import log_message


class MetadataCollector:
    """
    MetadataCollector is a singleton class responsible for collecting and caching
    the database schema metadata.
    """
    _instance = None
    _infos_schema = None
    _schema = {}

    def __new__(cls):
        """
        Create a new instance of the MetadataCollector class if one does not already exist.

        Returns:
            MetadataCollector: The singleton instance of the MetadataCollector class.
        """
        if cls._instance is None:
            cls._instance = super(MetadataCollector, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Initialize the MetadataCollector instance by determining the database engine
        and extracting the schema metadata.
        """
        if global_conf.get("DB_EGINE") == "PostgreSQL":
            schema = global_conf.get('DB_POSTGRES_DEFAULT_SCHEMA')
            self._infos_schema = POSTGRES_QUERY.format(schema=schema)
            self._extract_schema_from_postgres()
        else:
            raise Exception("Sorry, please define query engine")

    def _extract_schema_from_postgres(self):
        """
        Retrieve table structure from PostgreSQL and update the cache.
        """
        try:
            conn = postgres_service.get_postgres_connection()
            cursor = conn.cursor()
            
            cursor.execute(self._infos_schema)
            
            for table_schema, table_name, column_name, is_nullable, data_type, column_comment in cursor.fetchall():
                table_path = f"{table_schema}.{table_name}"
                if table_path not in self._schema:
                    self._schema[table_path] = []
                self._schema[table_path].append(
                    {
                        "column_name": column_name,
                        "is_nullable": is_nullable,
                        "data_type": data_type,
                        "column_comment": column_comment
                    }
                )
            
            cursor.close()

            # Save in cache
            with open(global_conf.get("DATA_SCHEMA_CACHE"), "w") as f:
                json.dump(self._schema, f, indent=4)
            
            log_message("INFO", "Schema metadata successfully extracted and cached.")
        except Exception as e:
            log_message("ERROR", f"Error extracting schema metadata: {str(e)}")

    def get_schema(self):
        """
        Get the cached database schema metadata.

        Returns:
            dict: The cached database schema metadata.
        """
        return self._schema

    def reload_schema(self):
        """
        Reload the database schema metadata by re-extracting it from the database.

        Returns:
            dict: The reloaded database schema metadata.
        """
        self._extract_schema_from_postgres()
        return self.get_schema()


# Create a single instance for import
db_metadata = MetadataCollector()