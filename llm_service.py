from langchain_core.prompts import ChatPromptTemplate
from models import GenerateInsightsRequest, JoinedInsightRequest
from fastapi import HTTPException
from progressive_insights.first_day_insight import NewUserInsightGenerator
from prompt_templates import *
from setup import *
from langchain_core.output_parsers import JsonOutputParser
from models import MoodAnalysis       
from datetime import datetime
from zoneinfo import ZoneInfo





def Join_States(request: GenerateInsightsRequest) -> JoinedInsightRequest:
    
    """ This function takes a WhatToDoRequest object and joins the list of states into comma-separated strings. """
    
    # Create a dictionary to hold the joined states
    states_map = {
        "energyStates": request.energyStates,
        "emotionalStates": request.emotionalStates,
        "mentalStates": request.mentalStates,
        "socialOrRelationalStates": request.socialOrRelationalStates,
        "achievementOrPurposeStates": request.achievementOrPurposeStates,
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
        **joined
    ) 



async def LLM_Query(request: GenerateInsightsRequest, user_timezone: str):
    """ 
        This function takes a WhatToDoRequest object and sends it to the LLM model to generate response. 
        If the primary model fails, it falls back to the secondary model. 
    """
    
    print(f'user_timezone : {user_timezone}')
    
    
    tz = ZoneInfo(user_timezone)

    now = datetime.now(tz)

    current_date = now.date()        # e.g. 2025-09-19
    current_time = now.time()        # e.g. 23:56:41.123456
    current_day = now.strftime("%A") #
    
    
    date_now = f"{current_date} {current_time} {current_day}"
    checkIn_text = """
    Date: {date_now},
    Energy Level: {request.energyLevel},
    Energy States: {request.energyStates},
    Emotional States: {request.emotionalStates},
    Mental States: {request.mentalStates},
    Social/Relational States: {request.socialOrRelationalStates},
    Achievement/Purpose States: {request.achievementOrPurposeStates},
    Emotional Intelligence Question: {request.emotionalIntelligenceQuestion},
    Mirror Question: {request.mirrorQuestion}
    """
    # CHECKINS_DB.add_texts(
    #     texts=[checkIn_text],
    #     metadatas=[{
    #         "date": date_now,
    #         "user_id": "12345"
    #         }],   
    # )
    
    # Join request list into strings to be used for user temeplate_input 
    joined_request = Join_States(request)
        
    # Create user template
    user_template = user_template_input(joined_request)

    # create the parser
    parser = JsonOutputParser(pydantic_object=MoodAnalysis)

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
        
        # Add insights to vectordatabase
        
        
        # insight_gen = NewUserInsightGenerator()
        insights = parser.parse(response.content)
        # insights_json = json.loads(insights)
        
        insights['comparison_insight'] = f"""This is your baseline - we'll help you understand patterns as you continue checking in. \nEven this single entry tells us you're someone who values self-awareness."""
        
        
        # INSIGHTS_DB.add_texts(
        #     texts=[response.content],
        #     metadatas=[{
        #         "date": date_now,
        #         "user_id": "12345" # Replace with actual user ID
        #         }],
        # )
        # insights_json = json.dumps(insights_json)
        # return response.content
        # return parser.parse(response.content)
        print(f"insights: {insights}")
        print(f"date_now: {date_now}")
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
            
            
            # Add insights to vectordatabase
            # INSIGHTS_DB.add_texts(
            #     texts=[response.content],
            #     metadatas=[{
            #         "date": date_now,
            #         "user_id": "12345" # Replace with actual user ID
            #         }],
            # )
                        
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
            
