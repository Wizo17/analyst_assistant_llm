import uvicorn
from src.config.global_conf import global_conf

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=global_conf.get("API_HOST"),
        port=int(global_conf.get("API_PORT")),
        reload=True,
        access_log=True
    )