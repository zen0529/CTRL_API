# Day 1: Welcome & Context Setting
class NewUserInsightGenerator:
    async def generate_day_1_insight(self, mood):
        """First impression is everything - make it valuable immediately"""
        
        insight_template = f"""
                        Welcome to your mood tracking journey! 🌟

                        This is your baseline - we'll help you understand patterns as you continue checking in. 
                        Even this single entry tells us you're someone who values self-awareness.

                        """
        
        return {
            'content': insight_template,
            'type': 'onboarding_welcome',
            'next_milestone': 'day_3',
            'encouragement_level': 'high'
        }
        