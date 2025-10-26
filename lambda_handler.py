import json
import os
from datetime import datetime
import pytz
from setup import SUPABASE
from summarizations import summarize_monthly_checkins, summarize_previous_day_checkins

def get_all_users():
    """Fetch all users from Supabase."""
    try:
        response = SUPABASE.table("users").select("user_id, timezone_user, last_daily_summary, last_monthly_summary").execute()
        return response.data or []
    except Exception as e:
        print(f"❌ Error fetching users: {e}")
        return []

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
    This is a direct port of your workers.py logic.
    
    Args:
        event: EventBridge event data (not used)
        context: Lambda context object
    
    Returns:
        Response object with status and results
    """
    print("=" * 50)
    print(f"🚀 Lambda invoked at: {datetime.now(pytz.UTC)}")
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
            
            # Daily summary: Check if it's exactly midnight (00:00) in user's timezone
            if local_time.hour == 0 and local_time.minute == 0:
                print(f"⏰ Midnight for user {user_id} in {user_timezone}")
                try:
                    summarize_previous_day_checkins(user_id, user_timezone)
                    print(f"✅ Daily summary done for user {user_id}")
                    daily_count += 1
                except Exception as e:
                    print(f"⚠️ Failed to summarize daily for user {user_id}: {e}")
            
            # Monthly summary: Check if it's midnight on the 1st of the month
            if local_time.hour == 0 and local_time.minute == 0 and local_time.day == 1:
                print(f"🎯 First of month midnight for user {user_id} in {user_timezone}")
                try:
                    summarize_monthly_checkins(user_id, user_timezone)
                    print(f"✅ Monthly summary done for user {user_id}")
                    monthly_count += 1
                except Exception as e:
                    print(f"⚠️ Failed to summarize monthly for user {user_id}: {e}")
                    
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