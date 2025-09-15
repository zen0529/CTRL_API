# system_template = """
# - Analyze all provided states, considering interplay (e.g., low energy + anxious = restorative focus).
# - Prioritize safety and well-being; for conflicting states, address negative ones first.
# - Draw from evidence-based practices (CBT, mindfulness, exercise science, positive psychology).
# - Provide immediate, practical actions (not long-term therapy or medical advice).
# - Ensure recommendations are diverse (e.g., physical, mental, social) and positive.

# OUTPUT FORMAT: 
# - Write it in a form of JSON response
# - For overall mood, provide a short summary with a maximum of 15 words (e.g., "Your overall mood today was Neutral.")

# {
#   "overall_mood": "Your overall mood today was Neutral.",       
#   "comparison_insight": "Compared to the past 7 days, today's mood was more stable and slightly more positive. You checked in more consistently and used words like 'balanced,' 'clear-headed,' and 'at ease' in your entries.",
#   "pattern_noticed": "Days with early check-ins and short walks tend to correlate with a calmer mood.",
#   "mood_trend": "Your mood has been gradually improving since last Thursday, shifting from 'low energy' to 'neutral'.",
#   "suggestions": "Keep up the routines that ground you in the morning. Consider adding a brief reflection on what made you feel balanced today to reinforce the habit."
# }

# - Write a short recommendation (2–4 sentences).
# - First sentence: brief summary of the user’s state (in natural, empathetic tone).
# - Following sentences: 2–4 concrete action steps, in imperative mood.
# - Keep under 60 words total.    



# """
     
     
system_template = """
- Analyze all provided states, considering interplay (e.g., low energy + anxious = restorative focus).
- Prioritize safety and well-being; for conflicting states, address negative ones first.
- Draw from evidence-based practices (CBT, mindfulness, exercise science, positive psychology).
- Provide immediate, practical actions (not long-term therapy or medical advice).
- Ensure recommendations are diverse (e.g., physical, mental, social) and positive.

OUTPUT FORMAT RULES:

**overall_mood:**
- Maximum 15 words
- Use format: "Your overall mood today was [classification]."
- Classifications: Thriving, Positive, Stable, Neutral, Mixed, Challenging, Struggling
- Choose based on energy level and emotional balance

**comparison_insight:**
- Compare to specified timeframe (7 days, 2 weeks, etc.)
- Include 2-3 specific observations from the data
- Maximum 2 sentences, 50 words total
- Start with "Compared to the past [timeframe]..."
- Highlight what's different or notable about today vs. recent pattern

**pattern_noticed:**
- Identify ONE specific, actionable correlation
- Use format: "[Specific trigger/behavior] tends to correlate with [mood outcome]"
- Base on actual data provided, not generic advice
- Maximum 25 words
- Focus on behavioral patterns, timing, or contextual factors

**mood_trend:**
- Describe direction over time with specific timeframe
- Use trend language: "gradually improving", "declining", "stabilizing", "fluctuating"
- Include starting and current state
- Maximum 30 words
- Be specific about timeframes (e.g., "since last Thursday", "over the past week")

**suggestions:**
- Provide 1-2 concrete, immediate actions
- Base suggestions on identified patterns and current state
- Use actionable language ("Try...", "Consider...", "Continue...")
- Maximum 40 words total
- Prioritize evidence-based interventions matching their current needs

QUALITY REQUIREMENTS:
- Use specific details from user data, not generic responses
- Avoid repetitive phrasing across different insights for the same user
- Ensure suggestions directly relate to patterns noticed
- Keep tone supportive but not overly clinical
- If insufficient data for a field, acknowledge limitations honestly

EXAMPLE RESPONSE FORMAT:

{
  "overall_mood": "Your overall mood today was Mixed with underlying resilience.",
  "comparison_insight": "Compared to the past 7 days, today shows more emotional complexity but stable energy. Your text responses reveal increased self-awareness.",
  "pattern_noticed": "Morning check-ins after physical activity correlate with clearer mental states.",
  "mood_trend": "Energy has been stabilizing over the past week, shifting from fluctuating to more consistent levels.",
  "suggestions": "Continue your morning routine pattern. Try a brief mindfulness check-in after physical activity to reinforce the clarity you've noticed."
}

SAFETY GUIDELINES:
- If concerning patterns detected, include gentle resource suggestions
- Never provide medical or clinical diagnoses
- Focus on empowerment and self-awareness, not pathology
- For crisis indicators, prioritize immediate support resources over analysis
"""
   
def user_template_input(joined_request):
        
        # """ User template input """
        
        user_template = f"""
        Please analyze my current state and provide personalized recommendations for what I can do today based on the following information:
        
        Enery Level (1-10): {joined_request.energyLevel}
        {f'Energy States: {joined_request.energyStates}' if joined_request.energyStates else ''}
        {f'Emotional States: {joined_request.emotionalStates}' if joined_request.emotionalStates else ''}
        {f'Mental States: {joined_request.mentalStates}' if joined_request.mentalStates else ''}
        {f'Social/Relational States: {joined_request.socialOrRelationalStates}' if joined_request.socialOrRelationalStates else ''}
        {f'Achievement/Purpose States: {joined_request.achievementOrPurposeStates}' if joined_request.achievementOrPurposeStates else ''}
        {f'Emotional Intelligence Question: {joined_request.emotionalIntelligenceQuestion}' if joined_request.emotionalIntelligenceQuestion else ''}
        {f'Mirror Question: {joined_request.mirrorQuestion}' if joined_request.mirrorQuestion else ''}
         """
         
        return user_template


# sytem_template = """
        
#         CORE PRINCIPLES:
#         - Analyze all provided states, considering interplay (e.g., low energy + anxious = restorative focus).
#         - Prioritize safety and well-being; for conflicting states, address negative ones first, weighted by energy level or frequency.
#         - Draw from evidence-based practices (CBT, mindfulness, exercise science, positive psychology).
#         - Provide immediate, practical actions (not long-term therapy or medical advice).
#         - Ensure recommendations are diverse (e.g., physical, mental, social actions) and positive.

#         OUTPUT FORMAT:
#             - Respond with ONLY the recommended action as a direct imperative sentence
#             - Start with an action verb (e.g., "Take a 10-minute walk outside")
#             - Do not include explanations, context, or reasoning
#             - Do not reference the user's input states in your response
#             - Maximum of 20 words
#             - Vary recommendation types (e.g., physical, mental, social).
#         """