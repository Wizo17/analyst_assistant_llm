from pydantic import BaseModel


# TODO Write documentation
class QueryResponse(BaseModel):
    user_query: str
    sql_query: str
    sql_explanation: str
    business_explanation: str
    download_link: str
