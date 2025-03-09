from pydantic import BaseModel
from typing import Optional
from config.global_conf import global_conf


# TODO Write documentation
class InitChat(BaseModel):
    provider: Optional[str] = global_conf.get("LLM_PROVIDER")
    model: Optional[str] = global_conf.get("LLM_MODEL")
    # TODO Add key to change model auto

