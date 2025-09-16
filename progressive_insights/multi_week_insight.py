# Multi-Week Evolution (2+ weeks)
class ProgressiveInsightSystem:
    def __init__(self):
        self.insight_complexity_levels = {
            'week_2': 'comparative_analysis',
            'week_3': 'pattern_correlation',  
            'week_4': 'behavioral_insights',
            'month_2': 'predictive_trends',
            'month_3': 'personalized_recommendations'
        }
    
    async def generate_progressive_insight(self, user_id, days_active):
        """Gradually increase insight sophistication"""
        
        if days_active < 7:
            return await self.early_stage_insight(user_id, days_active)
        elif days_active < 14:
            return await self.week_2_insight(user_id)
        elif days_active < 21:
            return await self.week_3_insight(user_id)
        elif days_active < 30:
            return await self.week_4_insight(user_id)
        else:
            return await self.mature_user_insight(user_id, days_active)
    
    async def week_2_insight(self, user_id):
        """Week 2: Introduce week-over-week comparison"""
        
        week_1_data = await self.get_user_entries(user_id, days=14, offset=7)
        week_2_data = await self.get_user_entries(user_id, days=7)
        
        comparison = await self.compare_weeks(week_1_data, week_2_data)
        
        insight = f"""
                Two weeks in! Now we can compare patterns:

                **Week-over-Week Changes:**
                - Energy trend: {comparison['energy_trend']} ({comparison['energy_change']:+.1f} points)
                - Mood stability: {comparison['stability_change']}
                - Check-in consistency: {comparison['consistency_change']}

                **New Pattern Discovered:**
                {comparison['new_pattern']}

                **Week 2 Observation:**
                {comparison['week_2_specific_insight']}

                You're building valuable self-awareness data! 📊
                """
        
        return {
            'content': insight,
            'complexity_level': 'comparative',
            'weeks_available': 2
        }
    
    async def week_3_insight(self, user_id):
        """Week 3: Pattern correlation and deeper analysis"""
        
        all_entries = await self.get_user_entries(user_id, days=21)
        correlations = await self.analyze_correlations(all_entries)
        
        insight = f"""
                Three weeks of insights unlocked! 🔓

                **Correlation Discovery:**
                {correlations['strongest_correlation']}

                **Your 3-Week Journey:**
                - Highest energy day: {correlations['best_day']} ({correlations['best_energy']}/10)
                - Most improvement: {correlations['biggest_improvement']}
                - Consistency streak: {correlations['longest_streak']} days

                **Behavioral Pattern:**
                {correlations['behavioral_insight']}

                **Personalized Suggestion:**
                Based on your 3-week pattern: {correlations['personalized_suggestion']}
                """
        
        return {
            'content': insight,
            'complexity_level': 'correlational',
            'weeks_available': 3
        }