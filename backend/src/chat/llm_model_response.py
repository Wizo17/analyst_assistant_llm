from pydantic import BaseModel, Field
from config.global_conf import global_conf


class LLMModelResponse(BaseModel):
    """
    LLMModelResponse is a Pydantic model that represents the response from an LLM (Language Learning Model).

    Attributes:
        query (str): A valid SQL query using the syntax specified by the database engine configured in `global_conf`.
        explanation (str): A detailed explanation of the query, including how joins, filters, and aggregations are applied. The explanation is provided in markdown format and in the user's language.
    """
    query: str = Field(description=f"A valid SQL query using {global_conf.get('DB_EGINE')} syntax.")
    explanation: str = Field(description="A detailed explanation of the query, including how joins, filters, and aggregations are applied in markdown in user language.")
