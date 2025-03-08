import json
from config.global_conf import global_conf
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
        if (global_conf.get("DB_EGINE") == "PostgreSQL"):
            schema = global_conf.get('DB_POSTGRES_DEFAULT_SCHEMA')
            self._infos_schema = f"""
                                    SELECT 
                                        cols.table_schema,
                                        cols.table_name,
                                        cols.column_name,
                                        cols.is_nullable,
                                        cols.data_type,
                                        pgd.description AS column_comment
                                    FROM information_schema.columns AS cols
                                    LEFT JOIN pg_catalog.pg_statio_all_tables AS st ON 
                                        cols.table_schema = st.schemaname 
                                        AND cols.table_name = st.relname
                                    LEFT JOIN pg_catalog.pg_description AS pgd ON 
                                        pgd.objoid = st.relid 
                                        AND pgd.objsubid = cols.ordinal_position
                                    WHERE cols.table_schema = '{schema}'
                                    ORDER BY cols.table_name, cols.ordinal_position
                                """
            self._extract_schema_from_postgres()
        else:
            raise Exception("Sorry, please define query engine") 
    

    def _extract_schema_from_postgres(self):
        """
        Retrieves table structure from PostgreSQL and updates cache.
        """
        # TODO Add try catch
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
        conn.close()

        # Save in cache
        with open(global_conf.get("DATA_SCHEMA_CACHE"), "w") as f:
            json.dump(self._schema, f, indent=4)
        
    

    def get_schema(self):
        return self._schema
    

    def reload_schema(self):
        self._extract_schema_from_postgres()
        return self.get_schema()


db_metadata = MetadataCollector()
