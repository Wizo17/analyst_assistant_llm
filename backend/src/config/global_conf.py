import os
from dotenv import load_dotenv
from typing import Any, Dict

class Configuration:
    """
    Configuration is a singleton class responsible for loading and providing access
    to the application's configuration settings from environment variables.
    """
    _instance = None
    _config: Dict[str, Any] = None

    def __new__(cls):
        """
        Create a new instance of the Configuration class if one does not already exist.

        Returns:
            Configuration: The singleton instance of the Configuration class.
        """
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Initialize the Configuration instance by loading environment variables
        and storing them in a dictionary.
        """
        load_dotenv()
        
        self._config = {
            "API_NAME": os.getenv("API_NAME"),
            "API_VERSION": os.getenv("API_VERSION"),
            "API_DESCRIPTION": os.getenv("API_DESCRIPTION"),

            "LLM_PROVIDER": os.getenv("LLM_PROVIDER"),
            "LLM_MODEL": os.getenv("LLM_MODEL"),

            "DB_EGINE": os.getenv("DB_EGINE"),
            "DB_CONTENT": os.getenv("DB_CONTENT"),
            
            "DATA_SCHEMA_CACHE": os.getenv("DATA_SCHEMA_CACHE"),
            "DATA_FILE_EXPORT_PATH": os.getenv("DATA_FILE_EXPORT_PATH"),
            "MAX_ROWS_TO_LLM": os.getenv("MAX_ROWS_TO_LLM"),

            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),

            "DB_POSTGRES_HOST": os.getenv("DB_POSTGRES_HOST"),
            "DB_POSTGRES_PORT": os.getenv("DB_POSTGRES_PORT"),
            "DB_POSTGRES_NAME": os.getenv("DB_POSTGRES_NAME"),
            "DB_POSTGRES_USER": os.getenv("DB_POSTGRES_USER"),
            "DB_POSTGRES_PASSWORD": os.getenv("DB_POSTGRES_PASSWORD"),
            "DB_POSTGRES_DEFAULT_SCHEMA": os.getenv("DB_POSTGRES_DEFAULT_SCHEMA"),

            "API_HOST": os.getenv("API_HOST"),
            "API_PORT": os.getenv("API_PORT"),
        }

    def get(self, key: str) -> Any:
        """
        Get the value of a configuration setting by key.

        Args:
            key (str): The key of the configuration setting.

        Returns:
            Any: The value of the configuration setting, or an empty string if the key is not found.
        """
        try:
            return self._config[key]
        except (KeyError, ValueError) as e:
            log_message("ERROR", f"Invalid configuration key: {key}")
            return ""


# Create a single instance for import
global_conf = Configuration()