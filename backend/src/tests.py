import json
from agents.data_analyst import DataAnalyst
from agents.query_processor import QueryProcessor
from agents.sql_executor import SQLExecutor
from agents.sql_validator import SQLValidator
from chat.session import ChatSession
from data.metadata_collector import db_metadata
from config.global_conf import global_conf


if __name__ == "__main__":

    chat_session = ChatSession()
    chat_session2 = ChatSession()

    processor = QueryProcessor(chat_session)
    sql_validator = SQLValidator()
    sql_executor = SQLExecutor()
    data_analyst = DataAnalyst(chat_session)

    query = "Quels sont toutes les lignes de métro ?"
    print(f"query: {query}")
    response = processor.process_query(query)
    if response['query'] is not None:
        # print(f"response content: {response['query']}")
        # query1 = "SELECT DISTINCT r.route_short_name, r.route_long_name FROM public.routes r WHERE r.route_type = 1"
        query1 = response['query']
        print(f"Requête SQL : {query1}")
        if(sql_validator.pass_all_tests(query1)):
            data_result = sql_executor.execute_query(query1, 'csv')
            print(f"Résultat : {data_result}")
            analysis = data_analyst.explain_results(query, data_result, False)
            print(f"Analyse : {analysis}")


    
    # print("\n")
    # query = "Quels sont heures de passage des métros 1, 2 et 3 entre 7h et 11h ?"
    # print(f"query: {query}")
    # response = processor.process_query(query)
    # if response['query'] is not None:
    #     # print(f"response content: {response['query']}")
    #     # query2 = "SELECT DISTINCT st.arrival_time, st.departure_time, r.route_short_name FROM public.stop_times st INNER JOIN public.trips t ON st.trip_id = t.trip_id INNER JOIN public.routes r ON t.route_id = r.route_id WHERE r.route_short_name IN ('1', '2', '3') AND st.arrival_time BETWEEN '07:00:00' AND '11:00:00'"
    #     query2 = response['query']
    #     print(f"Requête SQL : {query2}")
    #     if(sql_validator.pass_all_tests(query2)):
    #         print(f"Résultat : {sql_executor.execute_query(query2).head(5)}")
        

    # print("\n")
    # query = "Donne moi tous les papas de la base ?"
    # print(f"query: {query}")
    # response = processor.process_query(query)
    # print(f"Réponse : {response}")
    # if response['query'] is not None:
    #     # print(f"response content: {response['query']}")
    #     query3 = response['query']
    #     print(f"Requête SQL : {query3}")
    #     if(sql_validator.pass_all_tests(query3)):
    #         print(f"Résultat : {sql_executor.execute_query(query3)}")
    # else:
    #     print(response['explanation'])


