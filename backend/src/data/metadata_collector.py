import json
from config import global_conf
from services.postgres import postgres_service


class MetadataCollector:
    _instance = None
    _infos_schema = None
    _schema = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MetadataCollector, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        if (global_conf("DB_EGINE") == "postgres"):
            schema = global_conf('DB_POSTGRES_DEFAULT_SCHEMA')
            self._infos_schema = f"""
                                    SELECT table_name, column_name, data_type 
                                    FROM information_schema.columns 
                                    WHERE table_schema = '{schema}'
                                """
            self.extract_schema_from_postgres()
        else:
            raise Exception("Sorry, please define query engine") 
    

    def extract_schema_from_postgres(self):
        """
        Retrieves table structure from PostgreSQL and updates cache.
        """
        # TODO Add try catch
        conn = postgres_service.get_postgres_connection()
        cursor = conn.cursor()
        
        cursor.execute(self._infos_schema)
        
        for table, column, data_type in cursor.fetchall():
            if table not in self._schema:
                self._schema[table] = []
            self._schema[table].append({"column": column, "type": data_type})
        
        cursor.close()
        conn.close()

        # Save in cache
        with open(global_conf("DATA_SCHEMA_CACHE"), "w") as f:
            json.dump(self._schema, f, indent=4)
        
    def get_schema(self):
        return self._schema
    

db_metadata = MetadataCollector()
