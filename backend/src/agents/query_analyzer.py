import json
import psycopg2
from langchain.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from config import global_conf
from data.metadata_collector import db_metadata
from utils.logger import log_message

class QueryAnalyzer:
    """
    Analyzes a user query in natural language and identifies the tables/columns concerned.
    """
    llm = None
    db_schema = None

    def __init__(self):
        self.llm = ChatOllama(model=global_conf("LLM_MODEL"))
        self.db_schema = self.load_schema()


    def load_schema(self):
        """
        Loads table structure from database.
        """
        try:
            with open(global_conf("DATA_SCHEMA_CACHE"), "r") as f:
                return json.load(f)
        except FileNotFoundError:
            log_message("INFO", "Schema cache not found. Loading from PostgreSQL.")
            return db_metadata.get_schema()


    def analyze_query(self, user_query):
        """
        Analyzes the user query and identifies relevant tables.
        """
        prompt = PromptTemplate(
            input_variables=["query", "schema"],
            template="""
            Tu es un assistant SQL expert. Voici la structure de la base de données :
            {schema}
            
            L'utilisateur demande : "{query}"
            Liste les tables et colonnes nécessaires pour répondre à la requête.
            """
        )

        response = self.llm.invoke(
            prompt.format(query=user_query, schema=json.dumps(self.db_schema, indent=2))
        )
        
        return response


