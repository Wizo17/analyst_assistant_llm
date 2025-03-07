# from agents.query_analyzer import QueryAnalyzer
from agents.query_analyzer import QueryAnalyzer
from data.metadata_collector import db_metadata
from config.global_conf import global_conf


if __name__ == "__main__":
    # print("Tests programs !")

    # print(db_metadata.get_schema())

    analyzer = QueryAnalyzer()
    query = "Quels sont heures de passage des métros 1, 2 et 3 entre 7h et 11h ?"
    print(f"query: {query}")

    response = analyzer.analyze_query(query)
    # print(f"response type: {type(response)}")
    print(f"response content: {response.content}")

