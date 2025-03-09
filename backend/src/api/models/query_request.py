from pydantic import BaseModel
from typing import Optional


# TODO Write documentation
class QueryRequest(BaseModel):
    session_id: str
    query: str
    explanation_full: Optional[bool] = False
    output_format: Optional[str] = "csv"
    full_data: Optional[bool] = False


class DownloadFileDataRequest(BaseModel):
    session_id: Optional[str]
    file_path: Optional[str]

