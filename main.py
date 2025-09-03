from typing import Union
from gptQuery import *
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from fastapi import FastAPI
from pydantic import BaseModel
from setup import *

app = FastAPI()

class WhatToDoRequest(BaseModel):
    energy_level: int
    energy_states: list[str]
    emotional_states: list[str] 
    mental_states: list[str]



@app.put("/generate_what_to_do")
async def generate_what_to_do(request: WhatToDoRequest):
    Daily_Action = await LLM_Query(
        request.energy_level, 
        request.energy_states, 
        request.emotional_states, 
        request.mental_states
    )
    return {"message" : Daily_Action}


async def LLM_Query(energy_level : int, energy_states : list, emotional_states: list, mental_states: list):
    try:

        template = """
        what shoud I do today if my energy level (ranged from 1 to 10 (Drained: 1, balanced: 5: Peak: 10)) is {energy_level} , my energy states are {energy_states}, my emotional states are {emotional_states}, and my mental states are {mental_states}?

        Answer in manner in 2 bullet points. Each bullet corresponds to 1 sentence 

    
        """

        # prompt_template = PromptTemplate(template=template)
        

        prompt = PromptTemplate.from_template(template)  
        prompt.format(
            energy_level=energy_level,
            energy_states=energy_states,
            emotional_states=emotional_states,
            mental_states=mental_states
            )
        # prompt_text = prompt_template.invoke()
        
        response = await LLM.invoke(prompt)
        return response.content

    except Exception as e:
        raise ValueError(f"An error occurred while querying the RAG model: {str(e)}")