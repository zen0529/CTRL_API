from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from checkins_repository import summarize_monthly_checkins
from summarizations import summarize_previous_day_checkins
from setup import *
# from obtain_timezone import getTimeZone
import pytz
from pytz import timezone


# scheduler = BlockingScheduler()

scheduler = BlockingScheduler(timezone=pytz.UTC)
def get_all_users():
    """Fetch all users from Supabase."""
    response = SUPABASE.table("users").select("user_id, timezone_user").execute()
    return response.data or []


@scheduler.scheduled_job('cron', hour='*/1', minute=0)  # Every hour at minute 0
def daily_summary_job():
    """Check if it's midnight in any user's timezone for daily summaries."""
    print("🕒 Running daily summary check...")
    users = get_all_users()
    now_utc = datetime.now(pytz.UTC)
   
    for user in users:
        user_id = user["user_id"]
        user_timezone = user["timezone_user"]
        user_tz = pytz.timezone(user_timezone)
        local_time = now_utc.astimezone(user_tz)
       
        # Check if it's exactly midnight (00:00) in user's timezone
        if local_time.hour == 0 and local_time.minute == 0:
            print(f"⏰ Midnight for user {user_id} in {user_timezone}")
            try:
                summarize_previous_day_checkins(user_id, user_timezone)
                print(f"✅ Daily summary done for user {user_id}")
            except Exception as e:
                print(f"⚠️ Failed to summarize daily for user {user_id}: {e}")

@scheduler.scheduled_job('cron', hour='*/1', minute=0)  # Every hour at minute 0
def monthly_summary_job():
    """Check if it's midnight on the 1st of the month in any user's timezone."""
    print("📅 Running monthly summary check...")
    users = get_all_users()
    now_utc = datetime.now(pytz.UTC)
   
    for user in users:
        user_id = user["user_id"]
        user_timezone = user["timezone_user"]
        user_tz = pytz.timezone(user_timezone)
        local_time = now_utc.astimezone(user_tz)
       
        # Check if it's midnight (00:00) AND the 1st day of the month
        if local_time.hour == 0 and local_time.minute == 0 and local_time.day == 1:
            print(f"🎯 First of month midnight for user {user_id} in {user_timezone}")
            try:
                summarize_monthly_checkins(user_id, user_timezone)
                print(f"✅ Monthly summary done for user {user_id}")
            except Exception as e:
                print(f"⚠️ Failed to summarize monthly for user {user_id}: {e}")

# @scheduler.scheduled_job('cron', minute=0) #runs every hour
# def daily_summary_job():
#     print("🕒 Running daily summary job...")
#     users = get_all_users()
#     now_utc = datetime.now(pytz.UTC)
    

#     for user in users:
#         user_tz = pytz.timezone(user["timezone_user"])
#         local_time = now_utc.astimezone(user_tz)
#         user_id = user["user_id"]
#         user_timezone = user["timezone_user"]
        
#         print("user timezone: ", user_timezone)
#         print("user id: ", user_id)
#         if local_time==0:    
#             try:
#                 summarize_previous_day_checkins(user_id, user_timezone)
#             except Exception as e:
#                 print(f"⚠️ Failed to summarize daily for user {user_id}: {e}")
                
# @scheduler.scheduled_job('cron', minute=0) #runs every hour
# def monthly_summary_job():
#     print("📅 Running monthly summary job check...")
#     users = get_all_users()

#     for user in users:
#         user_id = user["user_id"]
#         user_timezone = user["timezone_user"]
#         user_tz = timezone(user_timezone)
#         now = datetime.now(user_tz)
#         tomorrow = now + timedelta(days=1)

#         # Run only at 23:00 local time on the last day of the month
#         if now.hour == 23 and now.minute == 0 and tomorrow.day == 1:
#             try:
#                 summarize_monthly_checkins(user_id, user_timezone)
#                 print(f"✅ Monthly summary done for user {user_id}")
#             except Exception as e:
#                 print(f"⚠️ Failed to summarize monthly for user {user_id}: {e}")


if __name__ == "__main__":
    print("🚀 Worker started. Waiting for schedule triggers...")
    scheduler.start()