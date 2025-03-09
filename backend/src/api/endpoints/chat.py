from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
import os
from cryptography.fernet import Fernet
from api.common.helpers import export_dataframe_to_file
from chat.session import ChatSession
from agents.query_processor import QueryProcessor
from agents.sql_validator import SQLValidator
from agents.sql_executor import SQLExecutor
from agents.data_analyst import DataAnalyst
from api.models.init_chat import InitChat
from api.models.query_request import DownloadFileDataRequest, QueryRequest
from api.models.query_response import QueryResponse
from config.global_conf import global_conf
from utils.logger import log_message


router = APIRouter()

# Key for encryption
key = Fernet.generate_key()
fernet = Fernet(key)

# In-memory storage for sessions
sessions = {}


@router.post("/init")
def init_chat():
    """
    Initialize a new chat session.

    Returns:
        dict: A dictionary containing the session ID.
    """
    log_message("INFO", "Accessed URL /chat/init/")
    try:
        session = ChatSession()
        processor = QueryProcessor(session)
        sql_validator = SQLValidator()
        sql_executor = SQLExecutor()
        data_analyst = DataAnalyst(session)

        session_id = fernet.encrypt(session.get_thread_id().encode()).decode()
        sessions[session_id] = {
            "session": session,
            "processor": processor,
            "sql_validator": sql_validator,
            "sql_executor": sql_executor,
            "data_analyst": data_analyst
        }

        return {"session_id": session_id}
    except Exception as e:
        log_message("ERROR", f"Failed to initialize chat session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    


@router.post("/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    """
    Process a user query to generate SQL, validate it, execute it, and provide explanations.

    Args:
        request (QueryRequest): The request containing the user query and other parameters.

    Returns:
        QueryResponse: The response containing the SQL query, explanations, and download link.
    """
    log_message("INFO", "Accessed URL /chat/query/")
    log_message("INFO", f"Request data: {request}")
    try:
        session_data = sessions.get(request.session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")
        
        if request.output_format not in ["csv", "json"]:
            raise HTTPException(status_code=404, detail="File format not supported.")

        processor = session_data["processor"]
        sql_validator = session_data["sql_validator"]
        sql_executor = session_data["sql_executor"]
        data_analyst = session_data["data_analyst"]

        # Generate SQL
        response = processor.process_query(request.query)
        sql_query = response['query']

        # Validate SQL
        if sql_query and sql_validator.pass_all_tests(sql_query):
            # Execute SQL
            df_data_result = sql_executor.execute_query(sql_query)

            # Extract sample
            df_sample = df_data_result.head(int(global_conf.get("MAX_ROWS_TO_LLM")))

            # Format sample
            data_sample = df_sample.to_json(orient="records", lines=False, indent=2)

            # Generate explanation
            analysis = data_analyst.explain_results(request.query, data_sample, request.explanation_full)

            # Save file
            file_path = export_dataframe_to_file(df_data_result, request.output_format, request.full_data)

            return QueryResponse(
                user_query=request.query,
                sql_query=sql_query,
                sql_explanation=response['explanation'],
                business_explanation=analysis,
                download_link=file_path
            )
        else:
            log_message("ERROR", "SQL query validation failed.")
            return QueryResponse(
                user_query=request.query,
                sql_query="",
                sql_explanation="Impossible to answer the query.",
                business_explanation="Impossible to answer the query.",
                download_link=""
            )

    except Exception as e:
        log_message("ERROR", f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/download/")
def get_result(request: DownloadFileDataRequest):
    """
    Download the result file for a given session.

    Args:
        request (DownloadFileDataRequest): The request containing the session ID and file path.

    Returns:
        FileResponse: The response containing the file to be downloaded.
    """
    log_message("INFO", "Accessed URL /chat/download/")
    log_message("INFO", f"Request data: {request}")
    session_data = sessions.get(request.session_id)
    if not session_data:
        log_message("ERROR", f"Session {request.session_id} not found.")
        raise HTTPException(status_code=404, detail="Session not found.")

    if os.path.exists(request.file_path):
        return FileResponse(request.file_path)
    else:
        log_message("ERROR", f"File not found for session {request.session_id}: {request.file_path}")
        raise HTTPException(status_code=404, detail="Resource does not exist.")