class NewUserInsightGenerator:
    async def generate_day_1_insight(self, mood_data):
        """First impression is everything - make it valuable immediately"""
        
        insight_template = f"""
                        Welcome to your mood tracking journey! 🌟

                        Today you logged an energy level of {mood_data.energy_level}/10 and described feeling {', '.join(mood_data.emotional_states[:2])}. 

                        This is your baseline - we'll help you understand patterns as you continue tracking. Even this single entry tells us you're someone who values self-awareness.

                        Tomorrow's tip: Try logging around the same time to help us spot daily rhythm patterns.
                        """
        
        return {
            'content': insight_template,
            'type': 'onboarding_welcome',
            'next_milestone': 'day_3',
            'encouragement_level': 'high'
        }
        
class EarlyPatternInsights:
    async def generate_early_insight(self, user_id, days_active):
        mood_entries = await self.get_all_user_entries(user_id)
        
        if days_active == 2:
            return await self.day_2_insight(mood_entries)
        elif days_active == 3:
            return await self.day_3_insight(mood_entries)
    
    async def day_2_insight(self, entries):
        """Focus on consistency and basic comparison"""
        
        today_energy = entries[-1].energy_level
        yesterday_energy = entries[-2].energy_level
        
        energy_trend = "higher" if today_energy > yesterday_energy else "lower" if today_energy < yesterday_energy else "similar"
        
        insight = f"""
                    Day 2 check-in complete! Your energy today ({today_energy}/10) was {energy_trend} than yesterday ({yesterday_energy}/10).

                    Early observation: You checked in at {entries[-1].timestamp.strftime('%I:%M %p')} today vs {entries[-2].timestamp.strftime('%I:%M %p')} yesterday. Consistent timing helps us spot daily patterns.

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
        
class MatureUserInsights:
    async def generate_mature_insight(self, user_id, days_active):
        """Rich, personalized insights for established users"""
        
        if days_active < 60:
            return await self.early_maturity_insight(user_id, days_active)
        elif days_active < 90:
            return await self.seasonal_pattern_insight(user_id)
        else:
            return await self.advanced_predictive_insight(user_id)
    
    async def early_maturity_insight(self, user_id, days_active):
        """30-60 days: Rich pattern analysis"""
        
        analysis = await self.comprehensive_analysis(user_id, days_active)
        
        insight = f"""
                {days_active} days of mood tracking - you're building serious self-awareness! 🌟

                **Your Personal Patterns:**

                *Temporal Insights:*
                {analysis['temporal_patterns']}

                *Emotional Journey:*
                {analysis['emotional_evolution']}

                *Energy Optimization:*
                {analysis['energy_insights']}

                **Key Discovery:**
                {analysis['major_insight']}

                **Personalized Recommendation:**
                {analysis['custom_suggestion']}

                **Looking Ahead:**
                {analysis['future_prediction']}
                """
                        
        return {
            'content': insight,
            'complexity_level': 'comprehensive',
            'personalization_level': 'high'
        }