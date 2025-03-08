import uuid
import json
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from config.global_conf import global_conf
from data.metadata_collector import db_metadata
from utils.logger import log_message
from templates.prompts import CONTEXT_HUMAN_PROMPT_UPDATED, CONTEXT_SYSTEM_PROMPT, CONTEXT_HUMAN_PROMPT


class ChatSession:
    # TODO Write documentation
    # TODO Add Langsmith
    provider = None
    model = None
    llm = None
    thread_id = None
    schema_file_path = None
    db_schema = None
    config = None
    memory = MemorySaver()
    workflow = StateGraph(state_schema=MessagesState)
    app = None


    def __init__(self, provider="default", model="default"):
        # TODO Write documentation
        # Define provider
        if provider == "default":
            self.provider = global_conf.get("LLM_PROVIDER")
        else:
            self.provider = provider

        # Define model
        if model == "default":
            self.model = global_conf.get("LLM_MODEL")
        else:
            self.model = model

        # Init LLM Chat
        model_providers = {
            "openai": lambda: ChatOpenAI(model=self.model),
            "anthropic": lambda: ChatAnthropic(model=self.model),
            "ollama": lambda: ChatOllama(model=self.model),
        }
        if self.provider in model_providers:
            self.llm = model_providers[self.provider]()
        else:
            raise Exception(f"Invalid LLM provider: {self.provider}")

        # Define variables
        self.thread_id = str(uuid.uuid4())
        self.schema_file_path = global_conf.get("DATA_SCHEMA_CACHE")
        self.db_schema = self._load_schema()

        # Define the (single) node in the graph
        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", self._call_model)

        self.config = {"configurable": {"thread_id": self.thread_id}}

        # Add memory
        self.app = self.workflow.compile(checkpointer=self.memory)

        # Send schema to LLM model
        self._send_schema_to_model()

        log_message("INFO", f"ChatSession initialized")


    # Define the function that calls the model
    def _call_model(self, state: MessagesState):
        try:
            response = self.llm.invoke(state["messages"])
            return {"messages": response}
        except Exception as e:
            log_message("ERROR", f"Error invoking LLM: {str(e)}")
            return {"messages": f"Error: {str(e)}"}


    def _load_schema(self):
        # TODO Write documentation
        try:
            with open(self.schema_file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            log_message("WARNING", "Schema cache not found.")
            log_message("INFO", f"Loading schema from {global_conf.get('DB_ENGINE')}.")
            schema = db_metadata.get_schema()
            if not schema:
                raise Exception("Cannot load schema from database.")
            return schema


    def _send_schema_to_model(self, new_schema=False):
        # TODO Write documentation
        if not self.db_schema:
            log_message("ERROR", "Database schema not found.")
            return False
        
        try:
            if new_schema:
                human_message = CONTEXT_HUMAN_PROMPT_UPDATED
            else:
                human_message = CONTEXT_HUMAN_PROMPT

            input_messages = [
                SystemMessage(content=CONTEXT_SYSTEM_PROMPT),
                HumanMessage(content=human_message.format(schema=json.dumps(self.db_schema, indent=2)))
            ]
        
            self.app.invoke({"messages": input_messages}, self.config)
            return True
        except Exception as e:
            log_message("ERROR", f"An error occurred when sending schema to the model. {str(e)}")
            return False



    def update_schema(self):
        # TODO Write documentation
        self.db_schema = db_metadata.reload_schema()
        return self._send_schema_to_model(new_schema=True)


    def get_thread_id(self):
        # TODO Write documentation
        return self.thread_id


    def process_query(self, input_messages):
        # TODO Write documentation
        try:
            return self.app.invoke({"messages": input_messages}, self.config)
        except Exception as e:
            log_message("ERROR", f"An error occurred when sending query to the model. {str(e)}")
            return None

