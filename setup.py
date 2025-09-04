from os import getenv
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import asyncio
from models import *

load_dotenv()

# Initialize the LLM
LLM = ChatOpenAI(
  api_key=getenv("OPENROUTER_API_KEY"),
  base_url=getenv("OPENROUTER_BASE_URL"),
  model="deepseek/deepseek-chat-v3.1:free",
)



# template = """Question: {question}
# Answer: Let's think step by step."""

# prompt = PromptTemplate(template=template, input_variables=["question"])

# llm_chain = LLMChain(prompt=prompt, llm=LLM)

# question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

# print(llm_chain.run(question))



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
        # joined_energy_states = ", ".join(request.energy_states)
        # print(f"Energy level is: {joined_energy_states}")
        # joined_emotional_states = ", ".join(request.emotional_states)
        # print(f"Emotional level is: {joined_emotional_states}")
        # joined_mental_states = ", ".join(request.mental_states)
        # print(f"Mental level is: {joined_mental_states}")

        joined_request = Join_States(request)
        
        

        template = """
        what shoud I do today if my energy level (ranged from 1 to 10 (Drained: 1, balanced: 5: Peak: 10)) is {joined_request.energy_level} , my energy states are {joined_energy_states}, my emotional states are {joined_emotional_states}, and my mental states are {joined_mental_states}?

        Answer in 1 sentence only. 

        """
        # print(f"Template is: {template}")
        # prompt_template = PromptTemplate(template=template)
        

        prompt = PromptTemplate.from_template(template)  
        print(f"Prompt is: {prompt}")
        formatted_promt = prompt.format(
            energy_level=joined_request.energy_level,
            energy_states=joined_request.energy_states,
            emotional_states=joined_request.emotional_states,
            mental_states=joined_request.mental_states,
            social_or_relational_states=joined_request.social_or_relational_states,
            achievement_or_purpose_states=joined_request.achievement_or_purpose_states
            )
        
        # prompt_text = prompt_template.invoke()
        print(f"Prompt is: {prompt}")
        print(f"Formatted Prompt is: {formatted_promt}")
        response = await LLM.ainvoke(formatted_promt)
        return response.content

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)  # This will print to terminal
        return None  #
        # raise ValueError(f"An error occurred while querying the RAG model: {str(e)}")
    

if __name__ == "__main__":
    test_request = WhatToDoRequest( 
        energy_level=5,
        energy_states=["tired", "lethargic"], 
        emotional_states=["happy", "content"],
        mental_states=["focused", "clear"],
        social_or_relational_states=["connectd"],
        achievement_or_purpose_states=[]
    )
    joined = Join_States(test_request)
    print(f"Joined states: {joined}")