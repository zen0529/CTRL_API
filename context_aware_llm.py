import datetime


class InsightHistoryTracker:
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def store_generated_insight(self, user_id, insight_data):
        """Store insights with semantic fingerprints"""
        # Extract key themes/patterns mentioned
        themes = await self.extract_insight_themes(insight_data['content'])
        
        await self.db.execute("""
            INSERT INTO user_insights_history 
            (user_id, generated_at, content, themes, insight_type, data_period)
            VALUES ($1, $2, $3, $4, $5, $6)
        """, 
            user_id, 
            datetime.now(),
            insight_data['content'],
            themes,  # ["energy_comparison", "weekly_trend", "stability_pattern"]
            insight_data['type'],  # "daily_summary", "weekly_analysis" 
            insight_data['period']  # "2024-09-07:2024-09-14"
        )
    
    async def get_recent_insight_patterns(self, user_id, days=14):
        """Get patterns of recent insights to avoid repetition"""
        return await self.db.fetch("""
            SELECT 
                themes,
                insight_type,
                COUNT(*) as frequency,
                ARRAY_AGG(content ORDER BY generated_at DESC) as recent_examples
            FROM user_insights_history 
            WHERE user_id = $1 
            AND generated_at >= NOW() - INTERVAL '%s days'
            GROUP BY themes, insight_type
            ORDER BY frequency DESC
        """, user_id, days)

    async def extract_insight_themes(self, content):
        """Use lightweight NLP to extract themes"""
        themes = []
        
        # Pattern matching for common insight themes
        theme_patterns = {
            'energy_comparison': r'(energy.*higher|energy.*lower|compared.*energy)',
            'weekly_trend': r'(past 7 days|week|weekly)',
            'mood_stability': r'(stable|consistent|steady)',
            'pattern_correlation': r'(correlat|pattern|tend)',
            'time_of_day': r'(morning|evening|afternoon)',
            'activity_insight': r'(walk|exercise|routine)'
        }
        
        content_lower = content.lower()
        for theme, pattern in theme_patterns.items():
            if re.search(pattern, content_lower):
                themes.append(theme)
        
        return themes
    
    
class DynamicInsightGenerator:
    def __init__(self):
        self.history_tracker = InsightHistoryTracker(db)
        self.insight_templates = InsightTemplateManager()
        
    async def generate_varied_insight(self, user_id, mood_data):
        # Get what we've said recently
        recent_patterns = await self.history_tracker.get_recent_insight_patterns(user_id)
        
        # Build avoidance context
        avoidance_context = self.build_avoidance_prompt(recent_patterns)
        
        # Get fresh perspective angles
        unused_angles = await self.get_unused_insight_angles(user_id, mood_data)
        
        # Generate with explicit variety instructions
        prompt = self.build_varied_insight_prompt(
            mood_data, 
            avoidance_context, 
            unused_angles
        )
        
        insight = await self.llm.generate(prompt)
        
        # Store for future avoidance
        await self.history_tracker.store_generated_insight(user_id, {
            'content': insight,
            'type': 'daily_summary',
            'period': f"{mood_data['start_date']}:{mood_data['end_date']}"
        })
        
        return insight
    
    def build_avoidance_prompt(self, recent_patterns):
        """Create explicit instructions to avoid repetition"""
        if not recent_patterns:
            return ""
        
        overused_themes = [p['themes'] for p in recent_patterns if p['frequency'] > 2]
        recent_examples = []
        
        for pattern in recent_patterns[:3]:  # Last 3 most common patterns
            recent_examples.extend(pattern['recent_examples'][:2])
        
        avoidance_prompt = f"""
AVOID REPETITIVE PATTERNS:
You've recently used these themes too often: {', '.join([str(t) for t in overused_themes])}

Recent examples of what you've already said:
{chr(10).join([f'- "{ex[:100]}..."' for ex in recent_examples[:5]])}

DO NOT:
- Repeat similar phrasing or structure
- Use the same comparison timeframes repeatedly  
- Mention the same patterns in similar ways

INSTEAD: Find fresh angles, different timeframes, or unexplored aspects of their data.
"""
        return avoidance_prompt
    

class InsightAngleManager:
    def __init__(self):
        self.insight_angles = {
            'temporal_focus': [
                'hourly_patterns', 'daily_patterns', 'weekly_patterns', 
                'weekend_vs_weekday', 'morning_vs_evening', 'monthly_trends'
            ],
            'comparison_types': [
                'week_over_week', 'month_over_month', 'seasonal_comparison',
                'personal_baseline', 'goal_comparison', 'recent_vs_longterm'
            ],
            'insight_styles': [
                'pattern_recognition', 'correlation_analysis', 'trend_forecasting',
                'behavioral_insights', 'emotional_journey', 'achievement_focus'
            ],
            'narrative_approaches': [
                'story_telling', 'question_based', 'celebration_focused',
                'challenge_oriented', 'discovery_framed', 'growth_mindset'
            ]
        }
    
    async def get_unused_angles(self, user_id, days=21):
        """Find insight angles not used recently"""
        recent_insights = await self.db.fetch("""
            SELECT content FROM user_insights_history 
            WHERE user_id = $1 AND generated_at >= NOW() - INTERVAL '%s days'
        """, user_id, days)
        
        used_angles = set()
        for insight in recent_insights:
            # Analyze which angles were used
            used_angles.update(self.detect_used_angles(insight['content']))
        
        # Return fresh angles
        all_angles = set().union(*self.insight_angles.values())
        unused_angles = all_angles - used_angles
        
        return {
            category: [angle for angle in angles if angle in unused_angles]
            for category, angles in self.insight_angles.items()
        }
    
    def select_diverse_angle_combination(self, unused_angles, mood_data):
        """Smart selection of complementary angles"""
        selected = {}
        
        # Pick one from each category if available
        for category, available_angles in unused_angles.items():
            if available_angles:
                # Smart selection based on data richness
                if category == 'temporal_focus':
                    selected[category] = self.pick_best_temporal_angle(
                        available_angles, mood_data
                    )
                else:
                    selected[category] = random.choice(available_angles)
        
        return selected
    
class VariationEngine:
    def build_varied_insight_prompt(self, mood_data, avoidance_context, selected_angles):
        """Build prompts that encourage variety"""
        
        base_data_context = self.format_mood_data_context(mood_data)
        
        variation_instructions = f"""
{avoidance_context}

FRESH PERSPECTIVE INSTRUCTIONS:
Use these unexplored angles for today's insight:
- Temporal Focus: {selected_angles.get('temporal_focus', 'free_choice')}
- Comparison Type: {selected_angles.get('comparison_types', 'free_choice')}
- Insight Style: {selected_angles.get('insight_styles', 'pattern_recognition')}
- Narrative Approach: {selected_angles.get('narrative_approaches', 'discovery_framed')}

VARIETY REQUIREMENTS:
1. Start with an unexpected observation or question
2. Use different sentence structures than recent insights
3. Focus on aspects of the data not recently highlighted
4. Vary your language complexity and tone
5. Include specific, concrete details rather than generic patterns

DATA CONTEXT:
{base_data_context}

Generate a unique insight that feels fresh and personally relevant, avoiding the repetitive patterns shown above.
"""
        return variation_instructions
    
    async def post_process_for_uniqueness(self, generated_insight, user_id):
        """Post-processing to catch similar outputs"""
        # Check similarity to recent insights
        recent_insights = await self.get_recent_insights(user_id, limit=10)
        
        # Calculate semantic similarity
        similarity_scores = []
        for past_insight in recent_insights:
            similarity = self.calculate_semantic_similarity(
                generated_insight, past_insight['content']
            )
            similarity_scores.append(similarity)
        
        # If too similar, regenerate with stronger variation prompt
        if max(similarity_scores) > 0.8:  # 80% similarity threshold
            return await self.regenerate_with_stronger_variation(
                generated_insight, user_id
            )
        
        return generated_insight
    
class SemanticVariationEnforcer:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def calculate_semantic_similarity(self, text1, text2):
        """Calculate semantic similarity between insights"""
        embeddings = self.embedding_model.encode([text1, text2])
        return cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    
    async def enforce_semantic_diversity(self, candidate_insight, user_id):
        """Ensure semantic diversity from recent insights"""
        recent = await self.get_recent_insights(user_id, limit=7)
        
        for past_insight in recent:
            similarity = self.calculate_semantic_similarity(
                candidate_insight, past_insight['content']
            )
            
            if similarity > 0.75:  # Too similar
                return await self.request_alternative_insight(
                    candidate_insight, past_insight['content']
                )
        
        return candidate_insight
    
    async def request_alternative_insight(self, similar_insight, past_insight):
        """Request a different angle when similarity is too high"""
        alternative_prompt = f"""
The insight you generated is too similar to a previous one:

Your insight: "{similar_insight}"
Previous insight: "{past_insight}"

Generate a completely different insight using the same data but:
1. Different structural approach (questions vs statements, etc.)
2. Different aspect focus (emotional vs behavioral vs temporal)  
3. Different language style (conversational vs analytical vs encouraging)
4. Different time scope or comparison method

Make it feel like a completely different type of observation.
"""
        
        return await self.llm.generate(alternative_prompt)
    


class ContextAwareInsightGenerator:
    async def generate_contextual_insight(self, user_id, mood_data):
        """Generate insights aware of user's emotional state"""
        
        # Detect user's current emotional state
        current_emotional_tone = self.analyze_emotional_tone(mood_data)
        
        # Adjust insight style based on emotional context
        if current_emotional_tone == 'struggling':
            style_instruction = "Focus on small wins, gentle encouragement, and hope"
        elif current_emotional_tone == 'thriving':
            style_instruction = "Celebrate achievements and suggest building on strengths"
        elif current_emotional_tone == 'stable':
            style_instruction = "Explore curiosity-driven insights and growth opportunities"
        else:
            style_instruction = "Provide balanced, supportive observations"
        
        # Get fresh angles that match emotional context
        appropriate_angles = self.filter_angles_by_emotional_context(
            current_emotional_tone
        )
        
        # Generate with emotional awareness
        insight = await self.generate_emotionally_aware_insight(
            mood_data, style_instruction, appropriate_angles
        )
        
        return insight
    


class ProductionInsightSystem:
    def __init__(self):
        self.history_tracker = InsightHistoryTracker(db)
        self.variation_engine = VariationEngine()
        self.semantic_enforcer = SemanticVariationEnforcer()
        self.angle_manager = InsightAngleManager()
        
    async def generate_daily_insight(self, user_id, mood_data):
        """Complete pipeline for varied insight generation"""
        
        # 1. Analyze recent patterns to avoid
        recent_patterns = await self.history_tracker.get_recent_insight_patterns(user_id)
        
        # 2. Select unused angles
        unused_angles = await self.angle_manager.get_unused_angles(user_id)
        selected_angles = self.angle_manager.select_diverse_angle_combination(
            unused_angles, mood_data
        )
        
        # 3. Build variation-focused prompt
        prompt = self.variation_engine.build_varied_insight_prompt(
            mood_data, recent_patterns, selected_angles
        )
        
        # 4. Generate initial insight
        insight = await self.llm.generate(prompt)
        
        # 5. Enforce semantic diversity
        final_insight = await self.semantic_enforcer.enforce_semantic_diversity(
            insight, user_id
        )
        
        # 6. Store for future avoidance
        await self.history_tracker.store_generated_insight(user_id, {
            'content': final_insight,
            'angles_used': selected_angles,
            'type': 'daily_summary'
        })
        
        return final_insight