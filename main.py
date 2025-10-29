import json
from fastapi import FastAPI, Depends, HTTPException, status
from checkins_repository import get_days_since_last_checkin, get_monthly_summaries, obtain_previous_checkins_of_the_current_week, obtain_previous_checkins_of_the_previous_week
from llm_service import LLM_Query
from setup import *
from models import GenerateInsightsRequest
# from llm_service import LLM_Query
from summarizations import summarize_monthly_checkins, summarize_previous_day_checkins
# from worker import daily_summary_job, get_all_users

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
@app.post("/generate_insights",
           operation_id="recommendActions",   
           summary="Recommend Actions",       
           tags=["Recommendation"]    
          )
async def generate_insights(request: GenerateInsightsRequest, user_timezone: str, user_id:str):
    # print("\nrequest", request)
    
    Daily_Action = await LLM_Query(request, user_id ,user_timezone)
    return Daily_Action


@app.post("/summarize_daily")
async def summarize_daily( user_timezone: str, user_id:str):
    # data = await request.json() 
    result = await summarize_previous_day_checkins(user_id, user_timezone)
    if result == "success":
        return {"status": "ok", "message": "Daily summary completed", "user_id": user_id}
    else: 
        return result


@app.post("/summarize_monthly")
async def summarize_monthly(user_timezone: str, user_id:str):
    result = await summarize_monthly_checkins(user_id, user_timezone)
    
    if result == "success":
        return {"status": "ok", "message": "Monthly summary completed", "user_id": user_id}
    else: 
        return result


@app.get("/get_users")
async def get_users():
    """Return all users with their timezones."""
    response = SUPABASE.table("users").select("user_id, timezone_user, last_daily_summary, last_monthly_summary").execute()
    return {"users": response.data or []}


@app.post("/update_last_summary")
async def update_last_summary(user_id: str, summary_type: str, summary_date: str):
    """Update last_daily_summary or last_monthly_summary."""
    column = f"last_{summary_type}_summary"
    try:
        SUPABASE.table("users").update({column: summary_date}).eq("user_id", user_id).execute()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
# handler = Mangum(app, lifespan="off")