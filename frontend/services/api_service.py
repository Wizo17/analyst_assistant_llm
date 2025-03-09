import requests
from utils.logger import log_message

BASE_URL = "http://localhost:7575"

def check_api_status():
    """
    Checks the status of the API.

    Sends a GET request to the base URL of the API to check if it is available.

    Returns:
        bool: True if the API is available, False otherwise.
    """
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        log_message("ERROR", "API not available", str(e))
        return False

def init_chat():
    """
    Initializes a chat session.

    Sends a POST request to the '/chat/init' endpoint to initialize a new chat session.

    Returns:
        str: The session ID if initialization is successful, None otherwise.
    """
    url = f"{BASE_URL}/chat/init"
    try:
        response = requests.post(url)
        response.raise_for_status()
        return response.json().get("session_id")
    except requests.RequestException as e:
        log_message("ERROR", "Failed to initialize chat:", str(e))
        return None

def send_query(session_id, query, explanation_full=False, output_format="json", full_data=False):
    """
    Sends a chat query to the API.

    Args:
        session_id (str): The chat session ID.
        query (str): The query to send.
        explanation_full (bool, optional): If True, requests a full explanation. Default is False.
        output_format (str, optional): The desired output format. Default is "json".
        full_data (bool, optional): If True, requests all data. Default is False.

    Returns:
        dict: The API response as a dictionary if the request is successful, None otherwise.
    """
    url = f"{BASE_URL}/chat/query"
    payload = {
        "session_id": session_id,
        "query": query,
        "explanation_full": explanation_full,
        "output_format": output_format,
        "full_data": full_data
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        log_message("ERROR", "Failed to send query:", str(e))
        return None

def download_file(session_id, file_path):
    """
    Downloads a file from the API.

    Args:
        session_id (str): The chat session ID.
        file_path (str): The path of the file to download.

    Returns:
        str: The path of the downloaded file if the download is successful, None otherwise.
    """
    url = f"{BASE_URL}/chat/download/"
    payload = {
        "session_id": session_id,
        "file_path": file_path
    }
    import os

    try:
        # Send request
        response = requests.post(url, json=payload)
        response.raise_for_status()

        # Save the file in the Downloads directory
        file_name = os.path.basename(file_path)
        download_dir = os.path.expanduser("~/Downloads")
        os.makedirs(download_dir, exist_ok=True)
        file_path = os.path.join(download_dir, file_name)

        # Save the file
        log_message("INFO", "Downloading file:", str(file_name))
        with open(file_path, "wb") as file:
            file.write(response.content)
        return file_path
    except requests.RequestException as e:
        log_message("ERROR", "Error when download file:", str(e))
        return None