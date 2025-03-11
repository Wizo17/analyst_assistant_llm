import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/src")

import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints.chat import router as chat_router
from src.services.postgres import postgres_service
from src.config.global_conf import global_conf
from src.utils.logger import log_message


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """
    Handles the root URL access.
    Logs an informational message when the root URL is accessed. Attempts to establish a connection
    to the PostgreSQL database. If the connection is successful, returns the API name from the global
    configuration. If the connection fails, logs an error message and raises an HTTP 500 exception
    indicating that the database is unavailable. In case of any other exceptions, logs the error and
    raises an HTTP 500 exception with the error details.
    Returns:
        str: The API name from the global configuration if the database connection is successful.
    Raises:
        HTTPException: If the database is unavailable or any other internal error occurs.
    """
    log_message("INFO", "Accessed URL /")
    try:
        if postgres_service.get_postgres_connection():
            return global_conf.get("API_NAME")
        else:
            log_message("ERROR", f"Database is unvailable")
            raise HTTPException(status_code=500, detail="Database is unvailable.")

    except Exception as e:
        log_message("ERROR", f"Internal error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Include all routes
app.include_router(chat_router, prefix="/chat")

if __name__ == "__main__":
    log_message("INFO", "API_HOST: " + global_conf.get("API_HOST"))
    log_message("INFO", "API_PORT: " + global_conf.get("API_PORT"))