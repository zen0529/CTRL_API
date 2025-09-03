from os import getenv
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import asyncio
from models import WhatToDoRequest

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

def generate_what_to_do(request: WhatToDoRequest):
    if len(request.energy_states) > 1:
      request.energy_states = ", ".join(request.energy_states)
    
    
    # energy_states = ", ".join(energy_states)


async def LLM_Query(request: WhatToDoRequest):
    try:
        joined_energy_states = ", ".join(request.energy_states)
        print(f"Energy level is: {joined_energy_states}")
        joined_emotional_states = ", ".join(request.emotional_states)
        print(f"Emotional level is: {joined_emotional_states}")
        joined_mental_states = ", ".join(request.mental_states)
        print(f"Mental level is: {joined_mental_states}")

        template = """
        what shoud I do today if my energy level (ranged from 1 to 10 (Drained: 1, balanced: 5: Peak: 10)) is {energy_level} , my energy states are {joined_energy_states}, my emotional states are {joined_emotional_states}, and my mental states are {joined_mental_states}?

        Answer in 1 sentence only. 

        """
        # print(f"Template is: {template}")
        # prompt_template = PromptTemplate(template=template)
        

        prompt = PromptTemplate.from_template(template)  
        print(f"Prompt is: {prompt}")
        formatted_promt = prompt.format(
            energy_level=request.energy_level,
            energy_states=joined_energy_states,
            emotional_states=joined_emotional_states,
            mental_states=joined_mental_states
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
    



# async def lol():
#   print("okii")
#   dlol = await LLM_Query(5, ["tired", "lethargic"], ["happy", "content"], ["focused", "clear"])
#   print(f"okii this is: {dlol}")

  
# if __name__ == "__main__":
#     asyncio.run(lol())