from pydantic import BaseModel, Field

# class MoodEntries(BaseModel):
#     energy_level: int
#     energy_states: list
#     emotional_states: list
#     mental_states: list

class WhatToDoRequest(BaseModel):
    energy_level: int
    energy_states: list[str] | None
    emotional_states: list[str] | None
    mental_states: list[str] | None
    social_or_relational_states: list[str] | None
    achievement_or_purpose_states: list[str] | None

class JoinedRequest(BaseModel): 
    energy_level: int
    energy_states: str 
    emotional_states: str 
    mental_states: str 
    social_or_relational_states: str
    achievement_or_purpose_states: str