# from agents.query_analyzer import QueryAnalyzer
from data.metadata_collector import db_metadata


if __name__ == "__main__":
    print("Hello World !")

    print(db_metadata.get_schema())

    # analyzer = QueryAnalyzer()
    # query = "Quels sont les 5 meilleurs clients en termes de chiffre d'affaires cette année ?"
    # print(analyzer.analyze_query(query))

