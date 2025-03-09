import os
from dotenv import load_dotenv
from typing import Any, Dict

class Configuration:
    # TODO Write documentation
    _instance = None
    _config: Dict[str, Any] = None
    

    def __new__(cls):
        # TODO Write documentation
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    

    def _initialize(self):
        # TODO Write documentation
        load_dotenv()
        
        self._config = {
            "LLM_PROVIDER": os.getenv("LLM_PROVIDER"),
            "LLM_MODEL": os.getenv("LLM_MODEL"),
            "DB_EGINE": os.getenv("DB_EGINE"),
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
    
    
    def get(self, key: str):
        # TODO Write documentation
        """
        Retrieves a configuration value using a key
        
        Args:
            key: Access key
            
        Returns:
            The requested configuration value
        """
        try:
            return self._config[key]
        except (KeyError, ValueError) as e:
            #raise KeyError(f"Invalid configuration path: {path}") from e
            return ""


# Create a single instance for import
global_conf = Configuration()

