# Week 1 (Days 4-7): Building Foundation

class Week1InsightGenerator:
    async def generate_week1_insight(self, user_id, days_active):
        entries = await self.get_user_entries(user_id)
        
        if days_active == 4:
            return await self.halfway_to_week_insight(entries)
        elif days_active == 5:
            return await self.consistency_momentum_insight(entries)
        elif days_active == 6:
            return await self.almost_week_insight(entries)
        elif days_active == 7:
            return await self.first_week_complete_insight(entries)
    
    async def halfway_to_week_insight(self, entries):
        """Day 4 - Halfway to first week"""
        
        # Look for time-of-day patterns
        check_in_times = [e.timestamp.hour for e in entries]
        most_common_hour = max(set(check_in_times), key=check_in_times.count)
        
        # Energy consistency
        energy_levels = [e.energy_level for e in entries]
        energy_range = max(energy_levels) - min(energy_levels)
        
        stability_note = "fairly stable" if energy_range <= 3 else "quite varied"
        
        insight = f"""
                    4 days strong! 💪 

                    Pattern emerging: You typically check in around {self.format_hour(most_common_hour)}, and your energy has been {stability_note} (ranging from {min(energy_levels)} to {max(energy_levels)}).

                    Halfway to your first weekly insight! In 3 more days, we'll show you patterns that are invisible in daily snapshots.
                    """
        
        return {
            'content': insight,
            'focus': 'momentum_building',
            'pattern_hints': True
        }
    
    async def first_week_complete_insight(self, entries):
        """Day 7 - First complete week analysis"""
        
        weekly_analysis = await self.analyze_first_week(entries)
        
        insight = f"""
                🎉 First week complete! Here's what your data reveals:

                **Your Week in Numbers:**
                - Average energy: {weekly_analysis['avg_energy']:.1f}/10
                - Most consistent day: {weekly_analysis['most_consistent_day']}
                - Energy range: {weekly_analysis['energy_range']} points
                - Most common feeling: {weekly_analysis['dominant_emotion']}

                **First Pattern Spotted:**
                {weekly_analysis['primary_pattern']}

                **What's Next:**
                Keep going for another week to unlock comparison insights and see how your patterns evolve!
                """
        
        return {
            'content': insight,
            'type': 'first_week_milestone',
            'unlock_next': 'comparative_analysis'
        }