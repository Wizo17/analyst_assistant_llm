import csv
import io
import pandas as pd
import psycopg2.extras
from utils.logger import log_message
from config.global_conf import global_conf
from services.postgres import postgres_service


class SQLExecutor:
    """
    SQLExecutor is responsible for executing SQL queries on a database
    and returning the results in various formats.
    """
    db_connection = None

    def __init__(self, db_connection=None):
        """
        Initialize the SQLExecutor with a database connection.

        Args:
            db_connection: The database connection object. If not provided, it will be created based on the global configuration.
        """
        if db_connection:
            self.db_connection = db_connection
        elif global_conf.get("DB_EGINE") == "PostgreSQL":
            self.db_connection = postgres_service.get_postgres_connection()
        else:
            raise Exception("Sorry, please define connection or query engine")
        
        log_message("INFO", f"SQLExecutor initialized")

    def _execute_postgres_query(self, sql_query, format='df'):
        """
        Execute a PostgreSQL query and return the results in the specified format.

        Args:
            sql_query (str): The SQL query to be executed.
            format (str): The format of the results ('json', 'csv', 'df').

        Returns:
            The query results in the specified format, or None if an error occurred.
        """
        if not sql_query:
            raise ValueError("SQL query cannot be empty.")
        
        if format not in ['json', 'csv', 'df']:
            raise ValueError(f"Format {format} not supported.")

        try:
            with self.db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                # Retrieve all columns
                columns = [desc[0] for desc in cursor.description]

                if format == 'json':
                    return {
                        "results": [dict(row) for row in rows],
                        "metadata": {
                            "columns": columns,
                            "row_count": len(rows)
                        }
                    }
                
                elif format == 'csv':
                    output = io.StringIO()
                    writer = csv.DictWriter(output, fieldnames=columns)
                    writer.writeheader()
                    for row in rows:
                        writer.writerow(dict(row))

                    csv_data = output.getvalue()
                    output.close()
                    return csv_data
                else:
                    if not rows:
                        return pd.DataFrame()
                    
                    df = pd.DataFrame(rows, columns=columns)
                    return df
        except Exception as e:
            log_message("ERROR", f"Error during query execution: {str(e)}")
            return None

    def execute_query(self, sql_query, format='df'):
        """
        Execute a SQL query and return the results in the specified format.

        Args:
            sql_query (str): The SQL query to be executed.
            format (str): The format of the results ('json', 'csv', 'df').

        Returns:
            The query results in the specified format, or None if an error occurred.
        """
        if format not in ['json', 'csv', 'df']:
            raise ValueError(f"Format {format} not supported.")
        
        if global_conf.get("DB_EGINE") == "PostgreSQL":
            return self._execute_postgres_query(sql_query, format)
        else:
            raise Exception("Sorry, query engine is not supported")