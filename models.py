from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time
class moodInsightOutputParser(BaseModel):
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
        description="1-2 concrete actions, max 40 words. Actionable suggestions based on the input."
    )


# class suggestionOutputParser(BaseModel):
#     suggestions: str = Field(
#         description="1-2 concrete actions, max 40 words. Actionable and based on the input."
#     )

# class moodInsightOutputParserForNewUsers(BaseModel):
#     suggestions: str = Field(
#         description="1-2 concrete actions, max 40 words. Actionable insights based on the input."
#     )

class EnergyStats(BaseModel):
    mean: float
    median: float
    min: int
    max: int
    std_dev: float
    trend_slope: float
    
class GenerateInsightsRequest(BaseModel):
    energy_value: int
    feelings: Optional[list[str]] = None 
    emotionalIntelligenceQuestion: Optional[str] = None
    mirrorQuestion: Optional[str] = None
    

class JoinedInsightRequest(BaseModel): 
    energy_value: int
    feelings: Optional[str] = None 
    emotionalIntelligenceQuestion: Optional[str] = None
    mirrorQuestion: Optional[str] = None
    summarizedAnswers: Optional[str] = None


class timezoneData(BaseModel):
    current_date: date
    current_time: time
    current_day: str
    current_year: int
    current_month: int
    days_in_month: int