import uuid
import json
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from config.global_conf import global_conf
from data.metadata_collector import db_metadata
from utils.logger import log_message
from templates.prompts import CONTEXT_SYSTEM_PROMPT, CONTEXT_HUMAN_PROMPT


class ChatSession:
    # TODO Write documentation
    model = None
    llm = None
    thread_id = None
    schema_file_path = None
    db_schema = None


    def __init__(self, provider, model):
        # TODO Write documentation
        self.model = model
        self.thread_id = str(uuid.uuid4())
        self.schema_file_path = global_conf.get("DATA_SCHEMA_CACHE")
        self.db_schema = self._load_schema()

        if (global_conf.get("LLM_PROVIDER") == "openai"):
            OPENAI_API_KEY = global_conf.get("OPENAI_API_KEY")
            self.llm = ChatOpenAI(model=self.model)
        elif (global_conf.get("LLM_PROVIDER") == "anthropic"):
            ANTHROPIC_API_KEY = global_conf.get("ANTHROPIC_API_KEY")
            self.llm = ChatAnthropic(model=self.model)
        elif (global_conf.get("LLM_PROVIDER") == "ollama"):
            self.llm = ChatOllama(model=self.model)
        else:
            raise Exception("Sorry, LLM_PROVIDER is not valid") 

        # Send schema to LLM model
        self._send_schema_to_model()

        if not self.model or not self.llm or not self.thread_id or self.schema_file_path or not self.db_schema:
            raise Exception("An error occured in chat session initialisation")


    def _load_schema(self):
        # TODO Write documentation
        try:
            with open(self.schema_file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            log_message("WARNING", "Schema cache not found.")
            log_message("INFO", f"Loading schema from {global_conf.get("DB_EGINE")}.")
            return db_metadata.get_schema()


    def _send_schema_to_model(self, new=False):
        # TODO Write documentation
        if not self.db_schema:
            log_message("ERROR", "Database schema not found.")
            return False
        
        try:
            messages = [
                SystemMessage(content=CONTEXT_SYSTEM_PROMPT),
                HumanMessage(content=CONTEXT_HUMAN_PROMPT.format(schema=json.dumps(self.db_schema, indent=2)))
            ]
        
            self.llm.invoke(messages)
            return True
        except Exception as e:
            log_message("ERROR", f"An error occurred when sending the schematic to the model. {str(e)}")
            return False



    def update_schema(self):
        # TODO Write documentation
        self.db_schema = db_metadata.reload_schema()
        self._send_schema_to_model()


    def get_thread_id(self):
        # TODO Write documentation
        return self.thread_id

