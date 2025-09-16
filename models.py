from pydantic import BaseModel, Field
from typing import Optional

class MoodAnalysis(BaseModel):
    overall_mood: str = Field(
        description="Maximum 15 words. Format: 'Your overall mood today was [classification].' "
                    "Classifications: Thriving, Positive, Stable, Neutral, Mixed, Challenging, Struggling."
    )
    comparison_insight: str = Field(
        description="Compare to timeframe (7 days, 2 weeks, etc). Max 2 sentences, 50 words. "
                    "Start with 'Compared to the past [timeframe]...'"
    )
    pattern_noticed: str = Field(
        description="Identify ONE actionable correlation. Max 25 words. "
                    "Format: '[Trigger/behavior] tends to correlate with [mood outcome]'."
    )
    mood_trend: str = Field(
        description="Describe mood direction over time. Max 30 words. "
                    "Use words like 'stabilizing', 'declining', 'gradually improving'. Include timeframe."
    )
    suggestions: str = Field(
        description="1-2 concrete actions, max 40 words. Actionable and based on identified patterns."
    )


class WhatToDoRequest(BaseModel):
    energyLevel: int
    energyStates: Optional[list[str]] = None 
    emotionalStates: Optional[list[str]] = None 
    mentalStates: Optional[list[str]] = None 
    socialOrRelationalStates: Optional[list[str]] = None 
    achievementOrPurposeStates: Optional[list[str]] = None   
    emotionalIntelligenceQuestion: Optional[str] = None
    mirrorQuestion: Optional[str] = None

    

class JoinedRequest(BaseModel): 
    energyLevel: int
    energyStates: Optional[str] = None 
    emotionalStates: Optional[str] = None 
    mentalStates: Optional[str] = None 
    socialOrRelationalStates: Optional[str] = None 
    achievementOrPurposeStates: Optional[str] = None 
    emotionalIntelligenceQuestion: Optional[str] = None
    mirrorQuestion: Optional[str] = None
