from pydantic import BaseModel


class QueryResponse(BaseModel):
    """
    QueryResponse is a model for the response of a processed user query.

    Attributes:
        user_query (str): The original query provided by the user.
        sql_query (str): The generated SQL query.
        sql_explanation (str): The explanation of the SQL query.
        business_explanation (str): The business explanation of the query results.
        download_link (str): The link to download the query results.
    """
    user_query: str
    sql_query: str
    sql_explanation: str
    business_explanation: str
    download_link: str