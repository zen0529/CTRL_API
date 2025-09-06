from fastapi import FastAPI, Depends, HTTPException, status
from setup import *
from models import WhatToDoRequest
from llm_service import LLM_Query

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
@app.post("/Recommend_Actions",
           operation_id="recommendActions",   
           summary="Recommend Actions",       
           tags=["Recommendation"]    
          )
async def Recommend_Actions(request: WhatToDoRequest):
    Daily_Action = await LLM_Query(request)
    return Daily_Action


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)