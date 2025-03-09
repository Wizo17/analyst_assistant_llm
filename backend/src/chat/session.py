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
    memory = None
    graph = None

    def __init__(self, provider="default", model="default"):
        self.provider = provider if provider != "default" else global_conf.get("LLM_PROVIDER")
        self.model = model if model != "default" else global_conf.get("LLM_MODEL")

        model_providers = {
            "openai": lambda: ChatOpenAI(model=self.model),
            "anthropic": lambda: ChatAnthropic(model=self.model),
            "ollama": lambda: ChatOllama(model=self.model),
        }

        if self.provider not in model_providers:
            raise Exception(f"Invalid LLM provider: {self.provider}")

        self.llm = model_providers[self.provider]()

        self.thread_id = str(uuid.uuid4())
        self.schema_file_path = global_conf.get("DATA_SCHEMA_CACHE")
        self.db_schema = self._load_schema()
        self.config = {"configurable": {"thread_id": self.thread_id}}

        # Memory and graph are now instance-specific
        self.memory = MemorySaver()
        self.graph = StateGraph(state_schema=MessagesState)
        self.graph.add_edge(START, "model")
        self.graph.add_node("model", self._call_model)
        self.graph = self.graph.compile(checkpointer=self.memory)

        self._send_schema_to_model()

        log_message("INFO", f"ChatSession initialized.")

    def _call_model(self, state: MessagesState):
        try:
            response = self.llm.invoke(state["messages"])
            return {"messages": response}
        except Exception as e:
            log_message("ERROR", f"Error invoking LLM: {traceback.format_exc()}")
            return {"messages": f"Error: {str(e)}"}

    def _load_schema(self):
        try:
            with open(self.schema_file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            log_message("WARNING", "Schema cache not found. Reloading from database.")
            schema = db_metadata.get_schema()
            if not schema:
                raise Exception("Failed to load schema from database.")
            return schema

    def _send_schema_to_model(self, new_schema=False):
        if not self.db_schema:
            log_message("ERROR", "Database schema not found.")
            return False
        try:
            human_message = CONTEXT_HUMAN_PROMPT_UPDATED if new_schema else CONTEXT_HUMAN_PROMPT
            input_messages = [
                SystemMessage(content=CONTEXT_SYSTEM_PROMPT),
                HumanMessage(content=human_message.format(schema=json.dumps(self.db_schema, indent=2)))
            ]
            self.graph.invoke({"messages": input_messages}, self.config)
            return True
        except Exception as e:
            log_message("ERROR", f"An error occurred when sending schema to the model. {traceback.format_exc()}")
            return False

    def update_schema(self):
        try:
            new_schema = db_metadata.reload_schema()
            if new_schema:
                self.db_schema = new_schema
                return self._send_schema_to_model(new_schema=True)
        except Exception as e:
            log_message("ERROR", f"Failed to update schema: {str(e)}")
            return False

    def get_thread_id(self):
        return self.thread_id

    def process_query(self, input_messages):
        try:
            return self.graph.invoke({"messages": input_messages}, self.config)
        except Exception as e:
            log_message("ERROR", f"Error processing query: {traceback.format_exc()}")
            return {"messages": f"Error: {str(e)}"}
