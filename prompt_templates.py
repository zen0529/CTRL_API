import random
from numerical_calculations import calculations
from fake_data import data
from obtain_timezone import getTimeZone

def overall_mood_for_new_users(energy):
    energyMessages = {
    1: [
        f"Your overall mood today feels {energy}.",
        f"You reported feeling pretty {energy} today.",
        f"It looks like you're having a {energy.lower()} kind of day.",
        f"Today seems like a {energy.lower()} day — noticing it is a powerful first step.",
        f"Feeling {energy.lower()} today is okay — this is your starting point."
    ]}
    
    overall_mood_message = random.choice(energyMessages[1])
    
    return overall_mood_message


class prompts: 
        
        def __init__(self):
                pass
        
        def get_energy_levels(user_id):
                """" Get all energy levels for all user checkins """
                energy_level_arr = []
                for d in data: #fake data only
                        if d['user_id'] == user_id:
                                # print(d)
                                for e in d['entries']:
                                        energy_level_arr.append(e['energy_level'])
                                        print(energy_level_arr)
                                break
                return energy_level_arr
        
        def get_number_of_checkins(user_id):
                """" Get number of checkins for a user """
                number_of_checkins = 0
                for d in data: #fake data only
                        if d['user_id'] == user_id:
                                # print(d)
                                for e in d['entries']:
                                        number_of_checkins += 1
                                        print(number_of_checkins)
                                
                return number_of_checkins
        
        def get_first_week_user_summary(self, joined_request, user_id):
                number_of_checkins = 0
                for d in data: #fake data only  
                        if d['user_id'] == user_id:
                                # print(d)
                                for e in d['entries']:
                                        number_of_checkins += 1
                                        print(number_of_checkins)
                
        def new_user_template(joined_request):
                """" User template input for new users """
                user_tempate_for_new_user = f"""
                  "Today's mood check in:
                        - Enery Level (1-10): {joined_request.energyLevel}
                        {f'- Energy States: {joined_request.energyStates}' if joined_request.energyStates else ''}
                        {f'- Emotional States: {joined_request.emotionalStates}' if joined_request.emotionalStates else ''}
                        {f'- Mental States: {joined_request.mentalStates}' if joined_request.mentalStates else ''}
                        {f'- Social/Relational States: {joined_request.socialOrRelationalStates}' if joined_request.socialOrRelationalStates else ''}
                        {f'- Achievement/Purpose States: {joined_request.achievementOrPurposeStates}' if joined_request.achievementOrPurposeStates else ''}
                        {f'- Emotional Intelligence Question: {joined_request.emotionalIntelligenceQuestion}' if joined_request.emotionalIntelligenceQuestion else ''}
                        {f'- Mirror Question: {joined_request.mirrorQuestion}' if joined_request.mirrorQuestion else ''}
                """     
                
                return user_tempate_for_new_user
        
        def new_user_system_template():
                system_template_for_new_users = """
                        - Analyze all provided states, considering interplay (e.g., low energy + anxious = restorative focus).
                        - Prioritize safety and well-being; for conflicting states, address negative ones first.
                        - Draw from evidence-based practices (CBT, mindfulness, exercise science, positive psychology).
                        - Provide immediate, practical actions (not long-term therapy or medical advice).
                        - Ensure recommendations are diverse (e.g., physical, mental, social) and positive.

                        SAFETY GUIDELINES:
                        - If concerning patterns detected, include gentle resource suggestions
                        - Never provide medical or clinical diagnoses
                        - Focus on empowerment and self-awareness, not pathology
                        - For crisis indicators, prioritize immediate support resources over analysis

                        STRICT OUTPUT RULES:
                        - Respond ONLY with a valid JSON object
                        """

                return system_template_for_new_users
        
        def existing_user_prev_data(self, joined_request, user_id: str, number_of_days_in_this_month:int, day:str, user_timezone:str):
                # obtain energy levels from user data
                # energy_levels = [data['energyLevel'] for data in user_data]
                
                # check current date
                
                energy_level_user_data = self.get_energy_levels(user_id)
                
                # calculate numerical calculations for user data(mean, median, min, max, std_dev)
                calculations_for_user = calculations(energy_level_user_data)
                
                # count number of checkins for user
                number_of_checkins = self.get_number_of_checkins(user_id)
                
                total_number_of_prev_checkins = 14
                
                prev_day_data = f"""
                                - Enery Level (1-10): {joined_request.energyLevel}
                                {f'- Energy States: {joined_request.energyStates}' if joined_request.energyStates else ''}
                                {f'- Emotional States: {joined_request.emotionalStates}' if joined_request.emotionalStates else ''}
                                {f'- Mental States: {joined_request.mentalStates}' if joined_request.mentalStates else ''}
                                {f'- Social/Relational States: {joined_request.socialOrRelationalStates}' if joined_request.socialOrRelationalStates else ''}
                                {f'- Achievement/Purpose States: {joined_request.achievementOrPurposeStates}' if joined_request.achievementOrPurposeStates else ''}
                                {f'- Emotional Intelligence Question: {joined_request.emotionalIntelligenceQuestion}' if joined_request.emotionalIntelligenceQuestion else ''}
                                {f'- Mirror Question: {joined_request.mirrorQuestion}' if joined_request.mirrorQuestion else ''}        
                                """
                
                # Check if user has 1 day of data then add a days section in the prompt with daily breakdown
                if len(number_of_checkins) == 1:
                        previous_day_text = f"""
                        Yesterday\'s mood check in:'
                        
                        {prev_day_data}
                        
                        """
                        return previous_day_text
                
                # Check if user has 2 to days of data or less than numer of days in this month
                
                elif len(number_of_checkins) >= 2 and len(number_of_checkins) < total_number_of_prev_checkins:
                        timezone=getTimeZone(user_timezone)
                        current_day = timezone.current_day
                        
                        
                        # libog anhon ang week grrrr
                        
                        
                        
                        
                        
                        
                        
                        
                        
                elif len(number_of_checkins) >= number_of_days_in_this_month:
                        f'- Previous {number_of_days_in_this_month} :'
                        f'- Mean : {calculations_for_user.mean} | Median : {calculations_for_user.median} | Min : {calculations_for_user.min} | Max : {calculations_for_user.max} | Std Dev : {calculations_for_user.std_dev}'
                        
                        
                user_template_for_existing_user_days = f"""
                  "Today's mood check in:
                        - Enery Level (1-10): {joined_request.energyLevel}
                        {f'- Energy States: {joined_request.energyStates}' if joined_request.energyStates else ''}
                        {f'- Emotional States: {joined_request.emotionalStates}' if joined_request.emotionalStates else ''}
                        {f'- Mental States: {joined_request.mentalStates}' if joined_request.mentalStates else ''}
                        {f'- Social/Relational States: {joined_request.socialOrRelationalStates}' if joined_request.socialOrRelationalStates else ''}
                        {f'- Achievement/Purpose States: {joined_request.achievementOrPurposeStates}' if joined_request.achievementOrPurposeStates else ''}
                        {f'- Emotional Intelligence Question: {joined_request.emotionalIntelligenceQuestion}' if joined_request.emotionalIntelligenceQuestion else ''}
                        {f'- Mirror Question: {joined_request.mirrorQuestion}' if joined_request.mirrorQuestion else ''}

                        
                         """     
                
                return user_template_for_existing_user_days
        
        def existing_user_input_(joined_request, day, month, energy_levels):
                # """ User template input """
                
                
                numerical_calculations = calculations(energy_levels)
                
                # Please analyze my current state and provide personalized recommendations for what I can do today based on the following information:
                user_template = f"""
                
                "Today's mood check in:
                - Enery Level (1-10): {joined_request.energyLevel}
                {f'- Energy States: {joined_request.energyStates}' if joined_request.energyStates else ''}
                {f'- Emotional States: {joined_request.emotionalStates}' if joined_request.emotionalStates else ''}
                {f'- Mental States: {joined_request.mentalStates}' if joined_request.mentalStates else ''}
                {f'- Social/Relational States: {joined_request.socialOrRelationalStates}' if joined_request.socialOrRelationalStates else ''}
                {f'- Achievement/Purpose States: {joined_request.achievementOrPurposeStates}' if joined_request.achievementOrPurposeStates else ''}
                {f'- Emotional Intelligence Question: {joined_request.emotionalIntelligenceQuestion}' if joined_request.emotionalIntelligenceQuestion else ''}
                {f'- Mirror Question: {joined_request.mirrorQuestion}' if joined_request.mirrorQuestion else ''}
                
                Last {day}-day Summary: 
                
                - Mean : {numerical_calculations.mean} | Median : {numerical_calculations.median} | Min : {numerical_calculations.min} | Max : {numerical_calculations.max} | Std Dev : {numerical_calculations.std_dev}
                
                
                """
                # Check if user has  of data then add a months section in the prompt with monthly breakdown
                # Check if user has a month only of data then add a month section in the prompt with weekly breakdown
                # Check if user has months of data then add a months section in the prompt with monthly breakdown
                
                return user_template

 




system_template = """
- Analyze all provided states, considering interplay (e.g., low energy + anxious = restorative focus).
- Prioritize safety and well-being; for conflicting states, address negative ones first.
- Draw from evidence-based practices (CBT, mindfulness, exercise science, positive psychology).
- Provide immediate, practical actions (not long-term therapy or medical advice).
- Ensure recommendations are diverse (e.g., physical, mental, social) and positive.

SAFETY GUIDELINES:
- If concerning patterns detected, include gentle resource suggestions
- Never provide medical or clinical diagnoses
- Focus on empowerment and self-awareness, not pathology
- For crisis indicators, prioritize immediate support resources over analysis

STRICT OUTPUT RULES:
- Respond ONLY with a valid JSON object
"""
   





# OUTPUT FORMAT RULES:

# **overall_mood:**
# - Maximum 15 words
# - Use format: "Your overall mood today was [classification]."
# - Classifications: Thriving, Positive, Stable, Neutral, Mixed, Challenging, Struggling
# - Choose based on energy level and emotional balance

# **comparison_insight:**
# - Compare to specified timeframe (7 days, 2 weeks, etc.)
# - Include 2-3 specific observations from the data
# - Maximum 2 sentences, 50 words total
# - Start with "Compared to the past [timeframe]..."
# - Highlight what's different or notable about today vs. recent pattern

# **pattern_noticed:**
# - Identify ONE specific, actionable correlation
# - Use format: "[Specific trigger/behavior] tends to correlate with [mood outcome]"
# - Base on actual data provided, not generic advice
# - Maximum 25 words
# - Focus on behavioral patterns, timing, or contextual factors

# **mood_trend:**
# - Describe direction over time with specific timeframe
# - Use trend language: "gradually improving", "declining", "stabilizing", "fluctuating"
# - Include starting and current state
# - Maximum 30 words
# - Be specific about timeframes (e.g., "since last Thursday", "over the past week")

# **suggestions:**
# - Provide 1-2 concrete, immediate actions
# - Base suggestions on identified patterns and current state
# - Use actionable language ("Try...", "Consider...", "Continue...")
# - Maximum 40 words total
# - Prioritize evidence-based interventions matching their current needs

# QUALITY REQUIREMENTS:
# - Use specific details from user data, not generic responses
# - Avoid repetitive phrasing across different insights for the same user
# - Ensure suggestions directly relate to patterns noticed
# - Keep tone supportive but not overly clinical
# - If insufficient data for a field, acknowledge limitations honestly

# EXAMPLE RESPONSE FORMAT:

# {
#   "overall_mood": "Your overall mood today was Mixed with underlying resilience.",
#   "comparison_insight": "Compared to the past 7 days, today shows more emotional complexity but stable energy. Your text responses reveal increased self-awareness.",
#   "pattern_noticed": "Morning check-ins after physical activity correlate with clearer mental states.",
#   "mood_trend": "Energy has been stabilizing over the past week, shifting from fluctuating to more consistent levels.",
#   "suggestions": "Continue your morning routine pattern. Try a brief mindfulness check-in after physical activity to reinforce the clarity you've noticed."
# }

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