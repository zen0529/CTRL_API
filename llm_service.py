from langchain_core.prompts import ChatPromptTemplate
from models import WhatToDoRequest, JoinedRequest
from fastapi import HTTPException
from prompt_templates import *
from setup import *
from langchain_core.output_parsers import JsonOutputParser
from models import MoodAnalysis       



def Join_States(request: WhatToDoRequest) -> JoinedRequest:
    
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
    return JoinedRequest(
        energyLevel=request.energyLevel,
        mirrorQuestion=request.mirrorQuestion,
        emotionalIntelligenceQuestion=request.emotionalIntelligenceQuestion,
        **joined
    ) 



async def LLM_Query(request: WhatToDoRequest):
    """ 
        This function takes a WhatToDoRequest object and sends it to the LLM model to generate response. 
        If the primary model fails, it falls back to the secondary model. 
    """
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
        # return response.content
        return parser.parse(response.content)

    except Exception as e:
        print(f"Primary model failed: {e}")
        # Fallback to secondary model
        try:
            response = await FALLBACK_LLM.ainvoke(messages)
            # return response.content
            return parser.parse(response.content)
        except Exception as fallback_e:
            print(f"Messages: {messages}")
            error_msg = f"Both models failed: {fallback_e}"
            print(error_msg) # For server-side logging
            raise HTTPException(
                status_code=503,  # Service Unavailable
                detail="Language model services are currently unavailable"
            )
            
