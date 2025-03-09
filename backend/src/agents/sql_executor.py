import psycopg2.extras
from utils.logger import log_message
from config.global_conf import global_conf
from services.postgres import postgres_service


class SQLExecutor:
    # TODO Write documentation
    db_connection = None


    def __init__(self, db_connection=None):
        # TODO Write documentation
        if db_connection:
            self.db_connection = db_connection
        elif global_conf.get("DB_EGINE") == "PostgreSQL":
            self.db_connection = postgres_service.get_postgres_connection()
        else:
            raise Exception("Sorry, please define connection or query engine") 
        
        log_message("INFO", f"SQLExecutor initialized")


    def _execute_postgres_query(self, sql_query):
        # TODO Write documentation
        if not sql_query:
            raise ValueError("SQL query cannot be empty.")

        try:
            with self.db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                # Retrieve all columns
                columns = [desc[0] for desc in cursor.description]
                return {
                    "results": [dict(row) for row in rows],
                    "metadata": {
                        "columns": columns,
                        "row_count": len(rows)
                    }
                }
        except Exception as e:
            log_message("ERROR", f"Error during query execution: {str(e)}")
            return None
        

    def execute_query(self, sql_query):
        # TODO Write documentation
        if global_conf.get("DB_EGINE") == "PostgreSQL":
            return self._execute_postgres_query(sql_query)
        else:
            raise Exception("Sorry, query engine is not supported") 
        
