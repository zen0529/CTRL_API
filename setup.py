from os import getenv
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import asyncio


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

async def LLM_Query(energy_level : int, energy_states : list, emotional_states: list, mental_states: list):
    try:

        template = """
        what shoud I do today if my energy level (ranged from 1 to 10 (Drained: 1, balanced: 5: Peak: 10)) is {energy_level} , my energy states are {energy_states}, my emotional states are {emotional_states}, and my mental states are {mental_states}?

        Answer in manner in 2 bullet points. Each bullet corresponds to 1 sentence 

    
        """

        # prompt_template = PromptTemplate(template=template)
        

        prompt = PromptTemplate.from_template(template)  
        formatted_promt = prompt.format(
            energy_level=energy_level,
            energy_states=energy_states,
            emotional_states=emotional_states,
            mental_states=mental_states
            )
        # prompt_text = prompt_template.invoke()
        print(f"Prompt is: {prompt}")
        response = await LLM.ainvoke(formatted_promt)
        return response.content

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)  # This will print to terminal
        return None  #
        # raise ValueError(f"An error occurred while querying the RAG model: {str(e)}")
    



async def lol():
  print("okii")
  dlol = await LLM_Query(5, ["tired", "lethargic"], ["happy", "content"], ["focused", "clear"])
  print(f"okii this is: {dlol}")

  
if __name__ == "__main__":
    asyncio.run(lol())