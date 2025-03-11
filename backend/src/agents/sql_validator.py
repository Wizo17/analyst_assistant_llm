import sqlparse
from psycopg2 import sql, connect
from psycopg2.errors import SyntaxError
from config.global_conf import global_conf
from services.postgres import postgres_service
from utils.logger import log_message

class SQLValidator:
    """
    SQLValidator is responsible for validating SQL queries for syntax correctness,
    safety, and execution feasibility.
    """
    db_connection = None

    def __init__(self, db_connection=None):
        """
        Initialize the SQLValidator with a database connection.

        Args:
            db_connection: The database connection object. If not provided, it will be created based on the global configuration.
        """
        if db_connection:
            self.db_connection = db_connection
        elif global_conf.get("DB_EGINE") == "PostgreSQL":
            self.db_connection = postgres_service.get_postgres_connection()
        else:
            raise Exception("Sorry, please define connection or query engine")
        
        log_message("INFO", f"SQLValidator initialized")

    def validate_syntax(self, query):
        """
        Validate the syntax of the SQL query.

        Args:
            query (str): The SQL query to be validated.

        Returns:
            bool: True if the syntax is valid, False otherwise.
        """
        try:
            # Analysis with sqlparse
            parsed = sqlparse.parse(query)
            if not parsed:
                raise ValueError(f"SQL query `{query}` is invalid.")
            
            statement_type = parsed[0].get_type()
            if statement_type not in ["SELECT", "WITH"]:
                raise ValueError("SQL query type not supported: " + statement_type)
            
            return True
        except Exception as e:
            log_message("ERROR", f"Syntax error detected: {str(e)}")
            return False

    def is_safe_query(self, query):
        """
        Check if the SQL query is safe to execute by looking for dangerous keywords.

        Args:
            query (str): The SQL query to be checked.

        Returns:
            bool: True if the query is safe, False otherwise.
        """
        dangerous_keywords = ["DROP", "INSERT", "UPDATE", "TRUNCATE", "DELETE", "ALTER", "--", ";--", "/*", "*/"]
        query_upper = query.upper()
        
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                log_message("ERROR", f"The query contains prohibited keywords: '{keyword}'")
                return False
        
        return True

    def validate_execution(self, query):
        """
        Validate the execution of the SQL query by running an EXPLAIN command.

        Args:
            query (str): The SQL query to be validated.

        Returns:
            bool: True if the query can be executed, False otherwise.
        """
        if self.db_connection is None:
            raise ValueError("A database connection is required.")
        
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("EXPLAIN " + query)
            return True
        except SyntaxError as e:
            log_message("ERROR", f"Syntax error detected: {str(e)}")
            return False
        except Exception as e:
            log_message("ERROR", f"Error during query execution: {str(e)}")
            return False

    def pass_all_tests(self, query):
        """
        Validate the SQL query by running all tests: syntax, safety, and execution.

        Args:
            query (str): The SQL query to be validated.

        Returns:
            bool: True if the query passes all tests, False otherwise.
        """
        log_message("INFO", f"The query to be validated is: {query}")
        return self.validate_syntax(query) and self.is_safe_query(query) and self.validate_execution(query)