import json
import os
from datetime import datetime
import pytz
import requests
from supabase import create_client, Client

# Initialize Supabase client (only for fetching users)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Your Railway API URL
RAILWAY_API_URL = os.environ.get("RAILWAY_API_URL")  # e.g., https://your-app.up.railway.app

# def get_all_users():
#     """Fetch all users from Supabase."""
#     try:
#         response = SUPABASE.table("users").select("user_id, timezone_user, last_daily_summary, last_monthly_summary").execute()
#         return response.data or []
#     except Exception as e:
#         print(f"❌ Error fetching users: {e}")
#         return []

def get_all_users():
    """Fetch users from Railway API."""
    try:
        response = requests.get(f"{RAILWAY_API_URL}/get_users", timeout=10)
        response.raise_for_status()
        return response.json().get("users", [])
    except Exception as e:
        print(f"❌ Error fetching users: {e}")
        return []

def update_last_summary_date(user_id, summary_type, summary_date):
    """Update via Railway API."""
    try:
        response = requests.post(
            f"{RAILWAY_API_URL}/update_last_summary",
            params={
                "user_id": user_id,
                "summary_type": summary_type,
                "summary_date": str(summary_date)
            },
            timeout=10
        )
        response.raise_for_status()
        print(f"✅ Updated last_{summary_type}_summary for {user_id}")
    except Exception as e:
        print(f"❌ Failed to update: {e}")

def call_railway_api(endpoint, user_id, user_timezone):
    """
    Call your Railway-deployed FastAPI endpoint.
    
    Args:
        endpoint: Either '/summarize_daily' or '/summarize_monthly'
        user_id: User's ID
        user_timezone: User's timezone
    
    Returns:
        Response from API or error dict
    """
    url = f"{RAILWAY_API_URL}{endpoint}"
    params = {
        "user_id": user_id,
        "user_timezone": user_timezone
    }
    
    try:
        response = requests.post(url, params=params, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"⚠️ Timeout calling {endpoint} for user {user_id}")
        return {"error": "timeout"}
    except requests.exceptions.RequestException as e:
        print(f"⚠️ API call failed for user {user_id}: {e}")
        return {"error": str(e)}

def update_last_summary_date(user_id, summary_type, summary_date):
    """
    Update the last summary date for a user in Supabase.
    
    Args:
        user_id: User's ID
        summary_type: Either 'daily' or 'monthly'
        summary_date: Date object or string (YYYY-MM-DD format)
    """
    column = f"last_{summary_type}_summary"
    try:
        SUPABASE.table("users").update({column: str(summary_date)}).eq("user_id", user_id).execute()
        print(f"✅ Updated {column} for user {user_id} to {summary_date}")
    except Exception as e:
        print(f"❌ Failed to update {column} for user {user_id}: {e}")

def lambda_handler(event, context):
    """
    Main Lambda handler - triggered hourly by EventBridge.
    Calls Railway API endpoints for summarization.
    
    Args:
        event: EventBridge event data (not used)
        context: Lambda context object
    
    Returns:
        Response object with status and results
    """
    print("=" * 50)
    print(f"🚀 Lambda invoked at: {datetime.now(pytz.UTC)}")
    print(f"🌐 Railway API: {RAILWAY_API_URL}")
    print("=" * 50)
    
    # Fetch all users with their timezones
    users = get_all_users()
    print(f"👥 Found {len(users)} users to check")
    
    if not users:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'No users found',
                'daily_processed': 0,
                'monthly_processed': 0
            })
        }
    
    now_utc = datetime.now(pytz.UTC)
    daily_count = 0
    monthly_count = 0
    
    # Check each user's timezone for midnight
    for user in users:
        user_id = user["user_id"]
        user_timezone = user["timezone_user"]
        
        try:
            # Convert UTC time to user's local timezone
            user_tz = pytz.timezone(user_timezone)
            local_time = now_utc.astimezone(user_tz)
            local_date = local_time.date()
            
            # Get last run dates from database
            last_daily = user.get("last_daily_summary")
            last_monthly = user.get("last_monthly_summary")
            
            # Daily summary: Check if it's a new day and we haven't processed it yet
            if local_time.hour == 0:  # We're in the midnight hour
                yesterday = str(local_date)
                if last_daily != yesterday:  # Haven't processed today yet
                    print(f"⏰ Processing daily summary for user {user_id} in {user_timezone} (date: {yesterday})")
                    
                    # Call Railway API
                    result = call_railway_api("/summarize_daily", user_id, user_timezone)
                    
                    if result.get("status") == "ok":
                        update_last_summary_date(user_id, "daily", yesterday)
                        print(f"✅ Daily summary done for user {user_id}")
                        daily_count += 1
                    else:
                        print(f"⚠️ Failed to summarize daily for user {user_id}: {result}")
            
            # Monthly summary: Check if it's the 1st of the month and we haven't processed it yet
            if local_time.day == 1 and local_time.hour == 0:  # First day of month, midnight hour
                first_of_month = str(local_date)
                if last_monthly != first_of_month:  # Haven't processed this month yet
                    print(f"🎯 Processing monthly summary for user {user_id} in {user_timezone} (date: {first_of_month})")
                    
                    # Call Railway API
                    result = call_railway_api("/summarize_monthly", user_id, user_timezone)
                    
                    if result.get("status") == "ok":
                        update_last_summary_date(user_id, "monthly", first_of_month)
                        print(f"✅ Monthly summary done for user {user_id}")
                        monthly_count += 1
                    else:
                        print(f"⚠️ Failed to summarize monthly for user {user_id}: {result}")
                    
        except Exception as e:
            print(f"⚠️ Error processing user {user_id}: {e}")
            continue
    
    result = {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Summaries processed successfully',
            'daily_processed': daily_count,
            'monthly_processed': monthly_count,
            'total_users_checked': len(users),
            'timestamp': now_utc.isoformat()
        })
    }
    
    print(f"✅ Daily summaries processed: {daily_count}")
    print(f"✅ Monthly summaries processed: {monthly_count}")
    print("=" * 50)
    print("🏁 Lambda execution completed")
    print("=" * 50)
    
    return result


# import json
# import os
# from datetime import datetime
# import pytz
# from setup import SUPABASE
# from summarizations import summarize_monthly_checkins, summarize_previous_day_checkins

# def get_all_users():
#     """Fetch all users from Supabase."""
#     try:
#         response = SUPABASE.table("users").select("user_id, timezone_user, last_daily_summary, last_monthly_summary").execute()
#         return response.data or []
#     except Exception as e:
#         print(f"❌ Error fetching users: {e}")
#         return []

# def update_last_summary_date(user_id, summary_type, summary_date):
#     """
#     Update the last summary date for a user in Supabase.
    
#     Args:
#         user_id: User's ID
#         summary_type: Either 'daily' or 'monthly'
#         summary_date: Date object or string (YYYY-MM-DD format)
#     """
#     column = f"last_{summary_type}_summary"
#     try:
#         SUPABASE.table("users").update({column: str(summary_date)}).eq("user_id", user_id).execute()
#         print(f"✅ Updated {column} for user {user_id} to {summary_date}")
#     except Exception as e:
#         print(f"❌ Failed to update {column} for user {user_id}: {e}")


# def lambda_handler(event, context):
#     """
#     Main Lambda handler - triggered hourly by EventBridge.
#     This is a direct port of your workers.py logic.
    
#     Args:
#         event: EventBridge event data (not used)
#         context: Lambda context object
    
#     Returns:
#         Response object with status and results
#     """
#     print("=" * 50)
#     print(f"🚀 Lambda invoked at: {datetime.now(pytz.UTC)}")
#     print("=" * 50)
    
#     # Fetch all users with their timezones
#     users = get_all_users()
#     print(f"👥 Found {len(users)} users to check")
    
#     if not users:
#         return {
#             'statusCode': 200,
#             'body': json.dumps({
#                 'message': 'No users found',
#                 'daily_processed': 0,
#                 'monthly_processed': 0
#             })
#         }
    
#     now_utc = datetime.now(pytz.UTC)
#     daily_count = 0
#     monthly_count = 0
    
#     # Check each user's timezone for midnight
#     for user in users:
#         user_id = user["user_id"]
#         user_timezone = user["timezone_user"]
        
#         try:
#             # Convert UTC time to user's local timezone
#             user_tz = pytz.timezone(user_timezone)
#             local_time = now_utc.astimezone(user_tz)
            
#             # Daily summary: Check if it's exactly midnight (00:00) in user's timezone
#             if local_time.hour == 0 and local_time.minute == 0:
#                 print(f"⏰ Midnight for user {user_id} in {user_timezone}")
#                 try:
#                     summarize_previous_day_checkins(user_id, user_timezone)
#                     print(f"✅ Daily summary done for user {user_id}")
#                     daily_count += 1
#                 except Exception as e:
#                     print(f"⚠️ Failed to summarize daily for user {user_id}: {e}")
            
#             # Monthly summary: Check if it's midnight on the 1st of the month
#             if local_time.hour == 0 and local_time.minute == 0 and local_time.day == 1:
#                 print(f"🎯 First of month midnight for user {user_id} in {user_timezone}")
#                 try:
#                     summarize_monthly_checkins(user_id, user_timezone)
#                     print(f"✅ Monthly summary done for user {user_id}")
#                     monthly_count += 1
#                 except Exception as e:
#                     print(f"⚠️ Failed to summarize monthly for user {user_id}: {e}")
                    
#         except Exception as e:
#             print(f"⚠️ Error processing user {user_id}: {e}")
#             continue
    
#     result = {
#         'statusCode': 200,
#         'body': json.dumps({
#             'message': 'Summaries processed successfully',
#             'daily_processed': daily_count,
#             'monthly_processed': monthly_count,
#             'total_users_checked': len(users),
#             'timestamp': now_utc.isoformat()
#         })
#     }
    
#     print(f"✅ Daily summaries processed: {daily_count}")
#     print(f"✅ Monthly summaries processed: {monthly_count}")
#     print("=" * 50)
#     print("🏁 Lambda execution completed")
#     print("=" * 50)
    
#     return result