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
    
    # Daily_Action = await LLM_Query(request, user_id ,user_timezone)
    # return Daily_Action

    # with open("mockdata.json", "r") as f:
    #     mock_data = json.load(f)
        
    # for row in mock_data:
    #     response = SUPABASE.table("mood_checkIns").insert(row).execute()
    #     print(response)
    # lol = summarize_monthly_checkins(user_id)
    
    # if should_generate_daily_summary(user_id, user_timezone):
    #     background_tasks.add_task(summarize_previous_day_checkins, user_id, user_timezone)

    # if is_end_of_month(getTimeZone(user_timezone).current_date):
    #     background_tasks.add_task(summarize_monthly_checkins, user_id, user_timezone)
    
    
    # insights = await LLM_Query(request, user_timezone)
    # lol1 = lol(user_id, user_timezone)
    # lol1 = get_all_users
    # lol1 = daily_summary_job()
    # lol1 = summarize_previous_day_checkins(user_id, user_timezone)
    # h = f"""
    # Avoided emotion: I’m avoiding disappointment. I’ve failed so many times that I’d rather not try than face that feeling again. It keeps me from taking chances that could actually change things.
    # Mirror answer: I’d tell them failure doesn’t define them — it just means they’re trying. Courage isn’t about avoiding disappointment; it’s about showing up despite it.
    
    # Avoided emotion: I’m pushing away anger because it makes me feel out of control. But bottling it up just turns into exhaustion and fake calmness that drains my creativity.
    # Mirror question answer: I’d remind them anger is just information. If you listen instead of suppress it, you can learn what boundary was crossed and fix it with clarity instead of rage.
    
    # Avoided emotion: ’m avoiding sadness over a friendship that ended badly. Pretending it doesn’t bother me makes me feel strong, but it also stops me from forming new connections.
    # Mirror question answer: I’d say healing means admitting it hurt. Letting yourself grieve doesn’t make you weak — it frees you to actually move forward and connect again.
    
    # Avoided emotion: I’m ignoring my anxiety about the future. I distract myself with work, but deep down it’s stopping me from planning long-term or taking real ownership of what I want.
    # Mirror question answer:I’d tell them fear of uncertainty is normal. Plan small steps, not perfect ones. Clarity only shows up once you’re already walking.
    
    # Avoided emotion: I’m avoiding guilt for letting people down. Instead of apologizing or improving, I keep overcompensating and burning out trying to “make up” for everything silently.
    # Mirror question answer: I’d tell them guilt can become fuel for growth. You can’t undo the past, but you can start living in a way that honors what you’ve learned.

    # """
    # lol1 = await summarize_previous_day_checkins(user_id, user_timezone)
    
    lol1 = await summarize_monthly_checkins(user_id, user_timezone)
    # lol1 = get_monthly_summaries(user_id, user_timezone)
    # lol1 = obtain_previous_checkins_of_the_current_week(user_id, user_timezone)
    
    # lol1 = await summarize_previous_day_checkins(user_id, user_timezone)
    return lol1


@app.post("/summarize_daily")
async def summarize_daily( user_timezone: str, user_id:str):
    # data = await request.json() 
    result = summarize_previous_day_checkins(user_id, user_timezone)
    return {"status": "ok", "message": "Daily summary completed", "user_id": user_id}


@app.post("/summarize_monthly")
async def summarize_monthly(user_timezone: str, user_id:str):
    result = summarize_monthly_checkins(user_id, user_timezone)
    return {"status": "ok", "message": "Monthly summary completed", "user_id": user_id}


def update_last_summary_date(user_id, summary_type, summary_date):
    """Update last_daily_summary or last_monthly_summary in Supabase."""
    column = f"last_{summary_type}_summary"
    try:
        SUPABASE.table("users").update({column: str(summary_date)}).eq("user_id", user_id).execute()
        print(f"✅ Updated {column} for user {user_id} to {summary_date}")
    except Exception as e:
        print(f"❌ Failed to update {column} for user {user_id}: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
