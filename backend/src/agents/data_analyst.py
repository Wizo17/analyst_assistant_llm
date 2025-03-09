from langchain.schema import SystemMessage, HumanMessage
from utils.logger import log_message
from templates.prompts import EXPLAINER_SYSTEM_PROMPT_FULL, EXPLAINER_SYSTEM_PROMPT_DIRECT, EXPLAINER_HUMAN_PROMPT


class DataAnalyst:
    # TODO Write documentation
    session = None


    def __init__(self, session):
        # TODO Write documentation
        self.session = session

        log_message("INFO", f"DataAnalyst initialized")

    
    def explain_results(self, user_query, data_sample, full=True):
        # Construct messages
        if full:
            system_message = EXPLAINER_SYSTEM_PROMPT_FULL
        else:
            system_message = EXPLAINER_SYSTEM_PROMPT_DIRECT
        input_messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=EXPLAINER_HUMAN_PROMPT.format(
                user_query=user_query, 
                data_sample=data_sample
                ))
        ]

        try:
            # Send to model via session
            response = self.session.process_query(input_messages)

            # Handle model response
            output = response.get("messages")
            if not output:
                raise Exception("No response from the model.")

            # Get result
            result = output[-1].content

            return result

        except Exception as e:
            log_message("ERROR", f"An error occurred durring explaination: {str(e)}")
            return None


