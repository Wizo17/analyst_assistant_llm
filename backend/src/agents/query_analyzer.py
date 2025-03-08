import json
import psycopg2
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from config.global_conf import global_conf
from data.metadata_collector import db_metadata
from utils.logger import log_message

class QueryAnalyzer:
    """
    Analyzes a user query in natural language and identifies the tables/columns concerned.
    """
    llm = None
    db_schema = None

    def __init__(self):
        # TODO catch error if failed
        if (global_conf.get("LLM_PROVIDER") == "openai"):
            OPENAI_API_KEY = global_conf.get("OPENAI_API_KEY")
            self.llm = ChatOpenAI(model=global_conf.get("LLM_MODEL"))
        
        elif (global_conf.get("LLM_PROVIDER") == "anthropic"):
            ANTHROPIC_API_KEY = global_conf.get("ANTHROPIC_API_KEY")
            self.llm = ChatAnthropic(model=global_conf.get("LLM_MODEL"))

        elif (global_conf.get("LLM_PROVIDER") == "ollama"):
            self.llm = ChatOllama(model=global_conf.get("LLM_MODEL"))
        
        else:
            raise Exception("Sorry, LLM_PROVIDER is not valid") 
        
        self.db_schema = self.load_schema()


    def load_schema(self):
        """
        Loads table structure from database.
        """
        try:
            with open(global_conf.get("DATA_SCHEMA_CACHE"), "r") as f:
                return json.load(f)
        except FileNotFoundError:
            log_message("INFO", "Schema cache not found. Loading from PostgreSQL.")
            return db_metadata.get_schema()


    def analyze_query(self, user_query):
        """
        Analyzes the user query and identifies relevant tables.
        """
        # TODO Gerer une seule session
        prompt = PromptTemplate(
            input_variables=["query", "schema"],
            template="""
            Tu es un assistant SQL expert. Les données des tables proviennent de fichier GTFS fournis par Ile-De-France Mobilité.
            Voici la structure de la base de données :
            {schema}
            
            L'utilisateur demande : "{query}"
            Liste les tables et colonnes nécessaires pour répondre à la requête. 
            Attention, les id technique ne servent que pour les jointures. 
            Il faut prendre en compte les descriptions des colonnes pour les filtres sur les données.
            Si tu ne sais pas, il faut indiquer que tu ne peux pas répondre par manque d'informations. Mais tu peux fournis une piste.
            """
        )

        response = self.llm.invoke(
            prompt.format(query=user_query, schema=json.dumps(self.db_schema, indent=2))
        )
        
        return response


