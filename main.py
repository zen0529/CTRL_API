from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import APIKeyHeader
from setup import *
from dotenv import load_dotenv

# initialing the fastAPI app
app = FastAPI(title="CTRL_API", description="An API to provide daily action recommendations based on user's current state using LLM.", version="1.0.0")

# verify the api key
def verify_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key != CTRL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key is required to Access this route"
        )
    return api_key

# Request to generate the action based on the user states
@app.post("/Recommend_Actions")
async def Recommend_Actions(request: WhatToDoRequest, api_key: str = Depends(verify_api_key)):
    Daily_Action = await LLM_Query(request)
    return {"message" : Daily_Action}


