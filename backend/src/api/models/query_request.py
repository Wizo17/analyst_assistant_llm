from pydantic import BaseModel
from typing import Optional


class QueryRequest(BaseModel):
    """
    QueryRequest is a model for processing a user query.

    Attributes:
        session_id (str): The ID of the session.
        query (str): The user query to be processed.
        explanation_full (Optional[bool]): Whether to provide a full explanation. Defaults to False.
        output_format (Optional[str]): The format of the output file ('csv' or 'json'). Defaults to 'csv'.
        full_data (Optional[bool]): Whether to export the full DataFrame or only a subset of rows. Defaults to False.
    """
    session_id: str
    query: str
    explanation_full: Optional[bool] = False
    output_format: Optional[str] = "csv"
    full_data: Optional[bool] = False


class DownloadFileDataRequest(BaseModel):
    """
    DownloadFileDataRequest is a model for downloading the result file for a given session.

    Attributes:
        session_id (Optional[str]): The ID of the session.
        file_path (Optional[str]): The path to the file to be downloaded.
    """
    session_id: Optional[str]
    file_path: Optional[str]