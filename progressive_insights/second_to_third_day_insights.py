        
# Days 2-3: Early Pattern Recognition
from models import MoodAnalysis

class EarlyPatternInsights:
    async def generate_early_insight(self, user_id, days_active):
        mood_entries = await self.get_all_user_entries(user_id)
        
        if days_active == 2:
            return await self.day_2_insight(mood_entries)
        elif days_active == 3:
            return await self.day_3_insight(mood_entries)
    
    async def day_2_insight(self, entries, llm_output):
        """Focus on consistency and basic comparison"""
        
        today_energy = entries[-1].energy_level
        yesterday_energy = entries[-2].energy_level
        
        energy_trend = "higher" if today_energy > yesterday_energy else "lower" if today_energy < yesterday_energy else "similar"
        
        insight = f"""
                    Day 2 check-in complete!
                    
                    {llm_output}

                    Keep it up - even small data points are building your personal insights foundation!
                    """
        
        return {
            'content': insight,
            'focus': 'consistency_building',
            'data_points': len(entries)
        }
    
    async def day_3_insight(self, entries):
        """Start introducing simple pattern concepts"""
        
        energy_levels = [e.energy_level for e in entries]
        avg_energy = sum(energy_levels) / len(energy_levels)
        
        # Simple trend analysis
        trend_direction = self.calculate_simple_trend(energy_levels)
        
        insight = f"""
                    Three days in! Your average energy so far: {avg_energy:.1f}/10

                    Early pattern emerging: Your energy has been {trend_direction} over these first few days. 

                    Interesting: You tend to select {self.most_common_emotional_state(entries)} as an emotional state. As we gather more data, we'll help you understand what influences these feelings.

                    Milestone unlocked: Keep going for 4 more days to unlock weekly pattern insights! 🎯
                    """
        
        return {
            'content': insight,
            'focus': 'pattern_introduction',
            'milestone_progress': 3/7
        }   
