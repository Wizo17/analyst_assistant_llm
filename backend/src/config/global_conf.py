import os
from dotenv import load_dotenv
from typing import Any, Dict

class Configuration:
    _instance = None
    _config: Dict[str, Any] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        load_dotenv()
        
        self._config = {
            "LLM_PROVIDER": os.getenv("LLM_PROVIDER"),
            "LLM_MODEL": os.getenv("LLM_MODEL"),
            "DB_EGINE": os.getenv("DB_EGINE"),
            "DATA_SCHEMA_CACHE": os.getenv("DATA_SCHEMA_CACHE"),

            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),

            "DB_POSTGRES_HOST": os.getenv("DB_POSTGRES_HOST"),
            "DB_POSTGRES_PORT": os.getenv("DB_POSTGRES_PORT"),
            "DB_POSTGRES_NAME": os.getenv("DB_POSTGRES_NAME"),
            "DB_POSTGRES_USER": os.getenv("DB_POSTGRES_USER"),
            "DB_POSTGRES_PASSWORD": os.getenv("DB_POSTGRES_PASSWORD"),
            "DB_POSTGRES_DEFAULT_SCHEMA": os.getenv("DB_POSTGRES_DEFAULT_SCHEMA"),
        }
    
    def get(self, key: str):
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

