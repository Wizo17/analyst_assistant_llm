import json

from services.api_service import check_api_status
from services.api_service import init_chat
from services.api_service import send_query
from services.api_service import download_file


if __name__ == "__main__":

    if check_api_status():
        session_id = init_chat()
        if session_id:
            query = "Quels sont toutes les lignes de métro ?"
            response = send_query(session_id, query, output_format="csv")
            print(json.dumps(response, indent=2))
            file_path = download_file(session_id, response.get("download_link"))
            print(f"File downloaded: {file_path}")
        else:
            print("Failed to initialize chat")
    else:
        print("API not available")

