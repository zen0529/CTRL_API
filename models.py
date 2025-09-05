from pydantic import BaseModel
from typing import Optional


class WhatToDoRequest(BaseModel):
    energy_level: int
    energy_states: Optional[list[str]] = None 
    emotional_states: Optional[list[str]] = None 
    mental_states: Optional[list[str]] = None 
    social_or_relational_states: Optional[list[str]] = None 
    achievement_or_purpose_states: Optional[list[str]] = None 

class JoinedRequest(BaseModel): 
    energy_level: int
    energy_states: Optional[str] = None 
    emotional_states: Optional[str] = None 
    mental_states: Optional[str] = None 
    social_or_relational_states: Optional[str] = None 
    achievement_or_purpose_states: Optional[str] = None 
