from fastapi import FastAPI, Depends, HTTPException, status
from setup import *
from models import GenerateInsightsRequest
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

@app.get("/")
def read_root():
    return {"status": "FastAPI deployed successfully"}

# Request to generate the action based on the user states
@app.post("/Generate_Insights",
           operation_id="recommendActions",   
           summary="Recommend Actions",       
           tags=["Recommendation"]    
          )

async def generate_insights(request: GenerateInsightsRequest, user_timezone: str):
    print("\nrequest", request)
    Daily_Action = await LLM_Query(request, user_timezone)
    return Daily_Action


# INSIGHTS_DB.delete_collection()

# stored_docs = INSIGHTS_DB.get()
# print("printing metadata:")
# for doc in stored_docs["metadatas"]:
#     print(doc)

# print("printing docs:")
# for doc in stored_docs["documents"]:
#     print(doc)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
