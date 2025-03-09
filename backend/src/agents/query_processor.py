import json
from langchain.schema import SystemMessage, HumanMessage
from templates.prompts import PROCESSOR_SYSTEM_PROMPT, PROCESSOR_HUMAN_PROMPT
from utils.logger import log_message


class QueryProcessor:
    """
    QueryProcessor is responsible for processing user requests
    and generating queries using a language model session.
    """
    session = None

    def __init__(self, session):
        """
        Initialize the QueryProcessor with a session.

        Args:
            session: The session object used to interact with the language model.
        """
        self.session = session
        log_message("INFO", f"QueryProcessor initialized")

    def process_query(self, user_request):
        """
        Process the user request to generate a query and explanation.

        Args:
            user_request (str): The request provided by the user.

        Returns:
            dict: A dictionary containing the generated query and explanation, or an error message if an error occurred.
        """
        if not user_request:
            raise ValueError("User request cannot be empty.")

        # Construct messages
        input_messages = [
            SystemMessage(content=PROCESSOR_SYSTEM_PROMPT),
            HumanMessage(content=PROCESSOR_HUMAN_PROMPT.format(user_request=user_request))
        ]

        try:
            # Send to model via session
            response = self.session.process_query(input_messages)

            # Handle model response
            output = response.get("messages")
            if not output:
                raise Exception("No response from the model.")

            # Format the output as JSON
            output_content = output[-1].content
            output_formated = output_content.replace("```", "")
            output_formated = output_formated.replace("json", "")
            result = json.loads(output_formated)

            # log_message("INFO", f"Generated Query: {result['query']}")
            # log_message("INFO", f"Explanation: {result['explanation']}")

            return result

        except Exception as e:
            log_message("ERROR", f"An error occurred while processing the query: {str(e)}")
            return {
                "query": None,
                "explanation": f"An error occurred: {str(e)}"
            }