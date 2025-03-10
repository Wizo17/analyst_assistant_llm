import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/src")

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints.chat import router as chat_router
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
    return global_conf.get("API_NAME")

# Include all routes
app.include_router(chat_router, prefix="/chat")

# Remove the uvicorn.run() from here and just keep this check
if __name__ == "__main__":
    log_message("INFO", "API_HOST: " + global_conf.get("API_HOST"))
    log_message("INFO", "API_PORT: " + global_conf.get("API_PORT"))