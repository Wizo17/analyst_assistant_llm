import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/src")

import uvicorn
from fastapi import FastAPI
from src.api.endpoints.chat import router as chat_router
from src.config.global_conf import global_conf
from src.utils.logger import log_message


app = FastAPI()

@app.get("/")
def read_root():
    return "API Data Analysis"


# Include all routes
app.include_router(chat_router, prefix="/chat")



if __name__ == "__main__":
    log_message("INFO", "API_HOST: " + global_conf.get("API_HOST"))
    log_message("INFO", "API_PORT: " + global_conf.get("API_PORT"))
    uvicorn.run(app, host=global_conf.get("API_HOST"), port=int(global_conf.get("API_PORT")))

