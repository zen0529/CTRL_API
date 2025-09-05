from os import getenv
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from fastapi.security import APIKeyHeader
import asyncio
from models import *

load_dotenv()

# Initialize the LLM
LLM = ChatOpenAI(
  api_key=getenv("OPENROUTER_API_KEY"),
  base_url=getenv("OPENROUTER_BASE_URL"),
  model="deepseek/deepseek-chat-v3.1:free",
)


CTRL_API_KEY = getenv("CTRL_API_KEY")

# Create API key header dependency
API_KEY_HEADER = APIKeyHeader(name="CTRL_API_KEY", description="API Key needed to access the protected endpoint")


def Join_States(request: WhatToDoRequest) -> JoinedRequest:
    
    """ This function takes a WhatToDoRequest object and joins the list of states into comma-separated strings. """
    
    # Create a dictionary to hold the joined states
    states_map = {
        "energy_states": request.energy_states,
        "emotional_states": request.emotional_states,
        "mental_states": request.mental_states,
        "social_or_relational_states": request.social_or_relational_states,
        "achievement_or_purpose_states": request.achievement_or_purpose_states,
    }
    
    # Join the states into comma-separated strings
    joined = {
        name: ", ".join(states) if len(states) > 1 else (states[0] if states else "")
        for name, states in states_map.items()
    }
  
    print(f'joined = {joined}')
    return JoinedRequest(
        energy_level=request.energy_level,
        **joined
    ) 



async def LLM_Query(request: WhatToDoRequest):
    try:
        # Join request list into strings to be used for user template_input 
        joined_request = Join_States(request)

        # System Tempalte input
        sytem_template = """

        You are a professional wellness coach AI with expertise in psychology, productivity, and holistic well-being.
        Your goal is to provide personalized, practical recommendations based on an individual's current state across multiple dimensions: energy, emotional, mental, social/relational, and achievement/purpose.
        The required field is only the energy level. So sometimes, not all dimensions will be provided, so you must be able to work with partial information.   

        CORE PRINCIPLES:
            - Analyze the person's current state across all provided dimensions
            - Focus on immediate, practical actions (not long-term therapy)
            - Consider the interplay between different state types
            - Prioritize safety and well-being over productivity
            - Handle minimal input gracefully (even if only energy level is provided)
            - Avoid medical advice or diagnosing conditions

        OUTPUT FORMAT:
            - Respond with ONLY the recommended action as a direct imperative sentence
            - Start with an action verb (e.g., "Take a 10-minute walk outside")
            - Do not include explanations, context, or reasoning
            - Do not reference the user's input states in your response
            - Maximum 15 words
        """
        
        # User tempalte input
        user_template = f"""
        Please analyze my current state and provide personalized recommendations for what I can do today based on the following information:
        
        Enery Level (1-10): {joined_request.energy_level}
        {f'Energy States: {joined_request.energy_states}' if joined_request.energy_states else ''}
        {f'Emotional States: {joined_request.emotional_states}' if joined_request.emotional_states else ''}
        {f'Mental States: {joined_request.mental_states}' if joined_request.mental_states else ''}
        {f'Social/Relational States: {joined_request.social_or_relational_states}' if joined_request.social_or_relational_states else ''}
        {f'Achievement/Purpose States: {joined_request.achievement_or_purpose_states}' if joined_request.achievement_or_purpose_states else ''}
         """
        
        # Create a ChatPromptTemplate object with system and user messages in a list of tuples
        template = ChatPromptTemplate([
            ('system', sytem_template),
            ('user', user_template)
        ])  

        # Convert the template into a list of formatted messages that the LLM can understand
        messages = template.format_messages()

        # Send the formatted messages to the LLM asynchronously and await the response
        response = await LLM.ainvoke(messages)
        return response.content

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)  # This will print to terminal
        return None  #
        # raise ValueError(f"An error occurred while querying the RAG model: {str(e)}")
    

# if __name__ == "__main__":
   
#     joined = Join_States(test_request)
#     lol =  await LLM_Query(test_request)
#     # print(f"Joined states: {joined}")
#     # print(len(joined.achievement_or_purpose_states))
#     print(lol)

test_request = WhatToDoRequest( 
    energy_level=5,
    energy_states=["tired", "lethargic"], 
    emotional_states=["happy", "content"],
    mental_states=["focused", "clear"],
    social_or_relational_states=[],
    achievement_or_purpose_states=[]
)

# Run the async function
if __name__ == "__main__":
    llm = asyncio.run(LLM_Query(test_request))  
    print(llm)