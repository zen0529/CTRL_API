
# Mature User Insights (1+ Month)
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