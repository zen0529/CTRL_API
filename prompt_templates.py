system_template = """
- Analyze all provided states, considering interplay (e.g., low energy + anxious = restorative focus).
- Prioritize safety and well-being; for conflicting states, address negative ones first.
- Draw from evidence-based practices (CBT, mindfulness, exercise science, positive psychology).
- Provide immediate, practical actions (not long-term therapy or medical advice).
- Ensure recommendations are diverse (e.g., physical, mental, social) and positive.

OUTPUT FORMAT:
- Write a short recommendation (2–4 sentences).
- First sentence: brief summary of the user’s state (in natural, empathetic tone).
- Following sentences: 2–4 concrete action steps, in imperative mood.
- Keep under 60 words total.
"""
        
def user_template_input(joined_request):
    
        # User template input
        user_template = f"""
        Please analyze my current state and provide personalized recommendations for what I can do today based on the following information:
        
        Enery Level (1-10): {joined_request.energyLevel}
        {f'Energy States: {joined_request.energyStates}' if joined_request.energyStates else ''}
        {f'Emotional States: {joined_request.emotionalStates}' if joined_request.emotionalStates else ''}
        {f'Mental States: {joined_request.mentalStates}' if joined_request.mentalStates else ''}
        {f'Social/Relational States: {joined_request.socialOrRelationalStates}' if joined_request.socialOrRelationalStates else ''}
        {f'Achievement/Purpose States: {joined_request.achievementOrPurposeStates}' if joined_request.achievementOrPurposeStates else ''}
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