from datetime import timedelta, datetime
from zoneinfo import ZoneInfo
from llm_service import summarize_insight_daily, summarize_insight_monthly
from scipy.stats import linregress
from numerical_calculations import calculations
from obtain_timezone import getTimeZone
from setup import SUPABASE
import numpy as np
import calendar


# async def summarize_insights_daily(insight):
#     summarize_entry = await summarize_insight_d(insight)
#     return summarize_entry



async def summarize_previous_day_checkins(user_id: str, user_timezone: str):
    """Summarize all check-ins from the previous day and store the summary."""

    _get_Timezone = getTimeZone(user_timezone)
    now = _get_Timezone.current_date
    tz = ZoneInfo(user_timezone)

    # # Compute previous day’s date range in user’s local time
    previous_day = now - timedelta(days=1)
    print(previous_day)
    
    # Query all yesterday's data
    start_datetime = f"{previous_day.isoformat()}T00:00:00+00"
    end_datetime = f"{previous_day.isoformat()}T23:59:59+00"
    
    # Fetch all check-ins for the previous day
    response = (
        SUPABASE.table("mood_checkIns")
        .select("*")
        .eq("user_id", user_id)
        .gte("created_at", start_datetime)
        .lte("created_at", end_datetime)
        .execute()
    )
     
    checkins = response.data
    
    print(checkins)
    if not checkins:
        print(f"No check-ins found for {previous_day}")
        return
    # Extract energy values
    energy_values = [
        item.get("energy_value")
        for item in checkins
        if item.get("energy_value") is not None
    ]

    collated_text = ""
    summary_data = {}
    
    # 1 checkin
    if len(energy_values) == 1: 
        avoided_emotion = checkins[0].get("avoided_emotion")
        mirror_question = checkins[0].get("mirror_question")
        collated_text = f"avoided emotion: {avoided_emotion} \nmirror question answer: {mirror_question}"
        
        print("summarizing text...")
        try:    
            summarized_text  = await summarize_insight_daily(collated_text)
            print("text summarized sucessfully:\n\n", summarized_text)
        except Exception as e:
            print(f"Failed to summarize daily: {e}")
            return  
        
        summary_data = {    
            "user_id": user_id,
            "checkin_day": previous_day.isoformat(),        
            "feelings": checkins[0].get("feelings"),
            "energy_value": checkins[0].get("energy_value"),
            "texts_summary": summarized_text,
            "no_of_checkins": 1,
        }
        
        
    else: 
        for checkin in checkins:
            mq = checkin.get("mirror_question")
            ae = checkin.get("avoided_emotion")
            
            collated_text += f"avoided emotion: {ae}\nmirror question answer: {mq}\n\n"
             # Calculate basic statistics
        
        print("collated text:\n\n", collated_text)
        metrics = calculations(energy_values)
    
        print("summarizing text...")
        try: 
            summarized_text  = await summarize_insight_daily(collated_text)
            print("text summarized sucessfully:\n\n", summarized_text)
        except Exception as e:
            print(f"Failed to summarize daily: {e}")
            return
        
    
        # Generate placeholder summaries
        summary_data = {
            "user_id": user_id,
            "checkin_day": previous_day.isoformat(),
            "min": metrics.min,
            "max": metrics.max,
            "mean": metrics.mean,
            "std_dev": metrics.std_dev,
            "trend_slope": metrics.trend_slope,
            "texts_summary": summarized_text,  
            "no_of_checkins": len(energy_values)
        }


    print("inserting to db...")
    try:
        SUPABASE.table("daily_summaries").insert(summary_data).execute()
        print("Daily summary inserted successfully.")
    except Exception as e:
        print(f"Failed to insert daily summary: {e}")
        return

    print(f"✅ Daily summary inserted for {previous_day} (user {user_id}).")

    return 'success'



def is_end_of_month(date: datetime.date) -> bool:
    """Return True if the date is the last day of the month."""
    next_day = date + timedelta(days=1)
    return next_day.month != date.month


def is_start_of_month(date: datetime.date) -> bool:
    """Return True if the date is the first day of the month."""
    previous_day = date - timedelta(days=1)
    return previous_day.month != date.month



async def summarize_monthly_checkins(user_id: str, timezone):
    """Generate and store a monthly summary if it's the end of the month."""
    
    timezone = "Asia/Manila"
    _get_Timezone = getTimeZone(timezone)  
    
    # 1️⃣ Check if today is the last day of the month
    # if not is_start_of_month(_get_Timezone.current_date):
    #     print("Not end of month. Skipping summary generation.")
    #     return

    current_date = _get_Timezone.current_date
    
    tz = ZoneInfo(timezone)
    
    # Step 1: Get the first day of this month
    first_of_this_month = datetime(current_date.year, current_date.month, 1, tzinfo=tz)

    # Step 2: Subtract one day to land in the previous month
    last_day_prev_month = first_of_this_month - timedelta(days=1)

    # Step 3: Derive previous month boundaries
    start_of_prev_month = datetime(last_day_prev_month.year, last_day_prev_month.month, 1, tzinfo=tz).date()
    end_of_prev_month = last_day_prev_month.date()

    
    print("\nstart_datetime:", start_of_prev_month)
    print("\nend_datetime:", end_of_prev_month)

    # 3️⃣ Fetch all check-ins for this month
    response = (
        SUPABASE.table("daily_summaries")
        .select("*")
        .eq("user_id", user_id)
        .gte("checkin_day", start_of_prev_month.isoformat())
        .lte("checkin_day", end_of_prev_month.isoformat())
        .execute()  
    )
    
    
    checkins = response.data
    print("\n\ncheckins:", checkins)

        
    if not checkins:
        print(f"No check-ins found for previous month")
        return
    
    mean_values = [
        item.get("mean")
        for item in checkins
        if item.get("mean") is not None
    ]
    
    print("mean values:", mean_values)
    
    no_of_checkins = [
        item.get("no_of_checkins")
        for item in checkins
        if item.get("no_of_checkins") is not None
    ]
    
    print("no of checkins:", no_of_checkins)
    
    min_values = [
        item.get("min")
        for item in checkins
        if item.get("min") is not None
    ]
    
     
    print("min values:", min_values)
    max_values = [
        item.get("max")
        for item in checkins
        if item.get("max") is not None
    ]
    
    print("max values:", max_values)
    
    std_devs = [
        item.get("std_dev")
        for item in checkins
        if item.get("std_dev") is not None
    ]
    
    
    print("std_devs:", std_devs)
    
    # 1 checkin
    if len(checkins) == 1: 
        text_summary = checkins[0].get("texts_summary")
        min = checkins[0].get("min")
        max = checkins[0].get("max")
        std_dev = checkins[0].get("std_dev")
        mean = checkins[0].get("mean")
        trend_slope = checkins[0].get("trend_slope")
        feelings = checkins[0].get("feelings")
        energy_value = checkins[0].get("energy_value")
        checkin_day= checkins[0].get("checkin_day")

        collated_text = f"checkin_day: {checkin_day} \n text_summary: {text_summary} \n"
        
        print("collated text:\n\n", collated_text)
        
        print("summarizing text...")
        try: 
            summarized_text  = await summarize_insight_monthly(collated_text)
            print("text summarized sucessfully:\n\n", summarized_text)
        except Exception as e:
            print(f"Failed to summarize daily: {e}")
            return
        
        summary_data = {    
                "user_id": user_id,
                "month": _get_Timezone.current_month,    
                "year": _get_Timezone.current_year,   
                "min": min,
                "max": max,
                "std_dev": std_dev,
                "mean": mean,
                "trend_slope": trend_slope,
                "texts_summary": summarized_text,
                "feelings":  feelings,
                "energy_value": energy_value,
            }
     
        
        
    elif len(checkins) == 0:
        print("No checkins found for previous month")
        return
    
    else: 
        collated_text = ""
        for checkin in checkins:
            insight = checkin.get("texts_summary")
            checkin_day = checkin.get("checkin_day")
            

            collated_text += f"checkin_day: {checkin_day} : insight: {insight}\n\n"
        
        print("collated text:\n\n", collated_text)
        
        print("summarizing text...")
        try: 
            summarized_text  = await summarize_insight_monthly(collated_text)
            print("text summarized sucessfully:\n\n", summarized_text)
        except Exception as e:
            print(f"Failed to summarize daily: {e}")
            return
        
        
        max = calculations(max_values)
        min = calculations(min_values)
        
        # Compute linear regression and obtaining trend slope
        x = np.arange(len(mean_values))  # [0, 1, 2, 3, 4, 5, 6]
        slope, intercept, r_value, p_value, std_err = linregress(x, mean_values)

        # Compute root mean square
        rms = np.sqrt(np.mean(np.square(std_devs)))
        
        # Compute weighted mean
        weighted_mean = np.average(mean_values, weights=no_of_checkins)
        
        # Generate placeholder summaries
        summary_data = {
            "user_id": user_id,
            "month": _get_Timezone.current_month,    
            "year": _get_Timezone.current_year, 
            "min": min.min,
            "max": max.max,
            "mean": weighted_mean,
            "std_dev": rms,
            "trend_slope": slope,
            "texts_summary": summarized_text,  
        }


    print("inserting to db...")
    try:
        SUPABASE.table("monthly_summaries").insert(summary_data).execute()
        print("Monthly summary inserted successfully.")
    except Exception as e:
        print(f"Failed to insert daily summary: {e}")
        return

    print(f"✅ Monthly summary inserted for month {_get_Timezone.current_month} (user {user_id}).")

    return 'success'
        