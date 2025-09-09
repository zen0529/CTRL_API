from pydantic import BaseModel
from typing import Optional


class WhatToDoRequest(BaseModel):
    energyLevel: int
    energyStates: Optional[list[str]] = None 
    emotionalStates: Optional[list[str]] = None 
    mentalStates: Optional[list[str]] = None 
    socialOrRelational_states: Optional[list[str]] = None 
    achievementOrPurposeStates: Optional[list[str]] = None   

class JoinedRequest(BaseModel): 
    energyLevel: int
    energyStates: Optional[str] = None 
    emotionalStates: Optional[str] = None 
    mentalStates: Optional[str] = None 
    socialOrRelationalStates: Optional[str] = None 
    achievementOrPurposeStates: Optional[str] = None 
