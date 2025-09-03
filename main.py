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

@app.post("/generate_what_to_do")
async def generate_what_to_do(request: WhatToDoRequest):
    Daily_Action = await LLM_Query(
        request.energy_level, 
        request.energy_states, 
        request.emotional_states, 
        request.mental_states
    )
    return {"message" : Daily_Action}


