from langchain_core.prompts import ChatPromptTemplate
from gap_days import *
from obtain_timezone import getTimeZone
from models import *
from fastapi import HTTPException
from progressive_insights.first_day_insight import NewUserInsightGenerator
from prompt_templates import *
from checkins_repository import check_which_user, get_days_since_last_checkin, is_new_user, is_new_user_with_checkin
from setup import *
from langchain_core.output_parsers import JsonOutputParser
# from models import MoodAnalysis       
from new_users_overall_mood import overall_mood




def Join_States(request: GenerateInsightsRequest) -> JoinedInsightRequest:
    
    """ This function takes a GenerateInsightsRequest object and joins the feelings into comma-separated strings. """
    
    # Create a dictionary to hold the joined states
    states_map = {
        "feelings": request.feelings,
    }
    
    # Join the states into comma-separated strings
    joined = {
        name: ", ".join(states) if len(states) > 1 else (states[0] if states else "")
        for name, states in states_map.items()
    }
    
    print(f'joined = {joined}') # for logging purposes
    return JoinedInsightRequest(
        energyLevel=request.energyLevel,
        mirrorQuestion=request.mirrorQuestion,
        emotionalIntelligenceQuestion=request.emotionalIntelligenceQuestion,
        
        # add summarized answers later
        
        
        **joined
    ) 




async def LLM_Query(request: GenerateInsightsRequest, user_id: str,  user_timezone: str):
    """ 
        This function takes a GenerateInsightsRequest object and sends it to the LLM model to generate response. 
        If the primary model fails, it falls back to the secondary model. 
    """
    
    # Get current date and time in user's timezone
    timezone = getTimeZone(user_timezone)
    # date_now = f"{timezone.current_month} {timezone.current_time} {timezone.current_day}"
    
    system_template = ''
    user_template = ''
    
    # Determine user type
    user_type = check_which_user(user_id)
    
    # if user_type == "new_user":    
    #     print("\n\n\nnew user")
    #     SUPABASE.table("users").insert({"timezone_user": user_timezone}).execute()  
    
    
    # response = await PRIMARY_LLM.ainvoke("generate")
    # Create a prompt based on the user type 
    # instantiate the prompt class
    prompt = prompts() 
    
    joined_request = Join_States(request)
    parser = JsonOutputParser(pydantic_object=moodInsightOutputParser)
    
    if user_type == "existing_user":
        # system_template = prompt.existing_user_system_template()
        # user_template =  prompt.existing_user_template(Join_States(request))
        system_template = prompt.existing_user_prev_data(joined_request, user_id, timezone.days_in_month, timezone.current_day, user_timezone)
        user_template =  prompt.existing_user_input_(joined_request, timezone.current_day, timezone.current_month, timezone.days_in_month)
        pass
    else:
        system_template = prompt.new_user_system_template()
        user_template =  prompt.new_user_template(joined_request)
        
    # create the parser for output formatting
    print(f"parser: {parser}")
    # Create a ChatPromptTemplate object with system and user messages in a list of tuples
    template = ChatPromptTemplate([
        ('system', system_template + "\n\n {format_instructions}"),
        ('user', user_template)
    ])  

    # Convert the template into a list of formatted messages that the LLM can understand
    messages = template.format_messages(
        format_instructions=parser.get_format_instructions()
    )

    print(f"mesages: {messages}")

    try:
        # Send the formatted messages to the LLM asynchronously and await the response
        response = await PRIMARY_LLM.ainvoke(messages)
        
        # generated insights 
        insights = parser.parse(response.content)
        
        if user_type == "new_user":
            insights['overall_mood'] = overall_mood(request.energyLevel)
            insights['comparison_insight'] = f"""This is your baseline - we'll help you understand patterns as you continue checking in. \nEven this single entry tells us you're someone who values self-awareness."""
            insights['pattern_noticed'] = random.choice(pattern_messages_for_new_users) 
            insights['mood_trend'] = random.choice(mood_trend_messages_for_new_users)
            print("New User insights: ", insights)
        elif user_type == "existing_user_with_missed_checkins":
            # obtain gap messages depending on days missed
            gap_days = get_days_since_last_checkin(user_id, user_timezone)
            gap_message = gap_messages(gap_days)
            
            insights['overall_mood'] = overall_mood(request.energyLevel)
            insights['comparison_insight'] = gap_message
            
            # checks if user has missed more than 3 days then add pattern/mood trend messages to encourage checking in
            if gap_days >= 3:
                    insights['pattern_noticed'] = random.choice(pattern_gap_messages).format(days=gap_days)
                    insights['mood_trend'] = random.choice(mood_trend_gap_messages).format(days=gap_days) #why only mood trend, pattern noticed...? because LLM will generate the suggestion
            # else generate insights
        # for existing user
        else:
            # to be continued
            pass
            
     
     
        # add  to prompt: watch also for missing checkin days cause that will also give insights
        
        # print(f"insights: {insights}")
        # print(f"date_now: {date_now}")
        return insights
        
        # # return response.content
        # return parser.parse(response.content)

    except Exception as e:
        print(f"Primary model failed: {e}")
        
        # Fallback to secondary model
        try:
            response = await FALLBACK_LLM.ainvoke(messages)
            
            insights = parser.parse(response.content)
            
            insights['comparison_insight'] = f"""This is your baseline - we'll help you understand patterns as you continue checking in. \nEven this single entry tells us you're someone who values self-awareness."""
                        
            print(f"insights: {insights}")
            return insights
        except Exception as fallback_e:
            print(f"Messages: {messages}")
            error_msg = f"Both models failed: {fallback_e}" 
            print(error_msg) # For server-side logging
            raise HTTPException(
                status_code=503,  # Service Unavailable
                detail="Language model services are currently unavailable"
            )
            

def new__user_query(request: GenerateInsightsRequest):
    pass

async def summarize_insight_daily(input_text: str):
    system_template = """
   You are an empathetic mood analysis assistant helping the user understand their emotional progress over time.

    You are given the summarized check-ins from the previous day. 
    Write a reflective insight that helps the user carry forward emotional awareness into the new day.

    Focus on:
    - The emotional pattern or lesson from yesterday
    - The underlying need or mindset that emerged
    - A short, supportive takeaway or reflection for today

    Use warm, psychologically insightful language that sounds like a personal reflection — not advice or instruction. 
    Limit your response to 50 words.
    Respond with the insight only.

    Here is the user's input:
    {input_text}
    """


    # Properly define the prompt structure
    prompt = system_template.format(input_text=input_text)

    # Format the message
    # messages = prompt.format_messages(input_text=input_text)

    # Call the model
    try:
        response = await PRIMARY_LLM.ainvoke(prompt)
        return response.content
    
    except Exception as e:
        print(f"en error occured: {e}")

async def summarize_insight_monthly(input_text: str):
    system_template = """
   You are an empathetic psychological insight assistant.

    You will receive the user's daily mood summaries for the previous month.
    Your task is to synthesize these into a single monthly reflection that captures the user's emotional journey and growth.

    Focus on revealing:
    - The recurring emotions or mental themes throughout the month
    - Any visible emotional progress, realizations, or patterns of avoidance
    - The overall tone shift (e.g., from self-doubt to acceptance, confusion to clarity)
    - Key lessons or mindsets the user seems to be developing

    Write in a supportive, reflective tone that sounds like a compassionate monthly self-review.
    Keep the response between 80–100 words.
    Respond only with the final reflection — no explanations, analysis steps, or commentary.


    Here is the user's last months summarized mood checkins:
    {input_text}
    """


    # Properly define the prompt structure
    prompt = system_template.format(input_text=input_text)

    # Call the model
    try:
        response = await PRIMARY_LLM.ainvoke(prompt)
        return response.content
    
    except Exception as e:
        print(f"en error occured: {e}")

