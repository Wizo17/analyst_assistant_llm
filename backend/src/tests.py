import json
from agents.query_processor import QueryProcessor
from chat.session import ChatSession
from data.metadata_collector import db_metadata
from config.global_conf import global_conf


if __name__ == "__main__":
    # print("Tests programs !")

    # print(db_metadata.get_schema())

    chat_session = ChatSession()
    processor = QueryProcessor(chat_session)

    query = "Quels sont heures de passage des métros 1, 2 et 3 entre 7h et 11h ?"
    print(f"query: {query}")

    response = processor.process_query(query)
    print(f"response content: {response['query']}")

