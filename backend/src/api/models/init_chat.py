from pydantic import BaseModel
from typing import Optional
from config.global_conf import global_conf


class InitChat(BaseModel):
    """
    InitChat is a model for initializing a chat session with optional parameters
    for the language model provider and model.

    Attributes:
        provider (Optional[str]): The language model provider. Defaults to the value from global configuration.
        model (Optional[str]): The language model. Defaults to the value from global configuration.
    """
    provider: Optional[str] = global_conf.get("LLM_PROVIDER")
    model: Optional[str] = global_conf.get("LLM_MODEL")
    # TODO Add key to change model auto