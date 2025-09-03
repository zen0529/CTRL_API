from pydantic import BaseModel

class MoodEntries(BaseModel):
    energy_level: int
    energy_states: list
    emotional_states: list
    mental_states: list