"""
Planner Agent - Creates content plan based on reflections and insights
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import random

from utils.timezone_utils import get_optimal_posting_times

class PlannerAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def create_content_plan(self, reflections: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Create a content plan based on reflections and platform settings"""
        self.logger.info("📋 Creating content plan...")
        
        content_plan = {}
        platforms = self.config['platforms']
        
        for platform_name, platform_config in platforms.items():
            if platform_config.get('enabled', False):
                content_plan[platform_name] = self._plan_platform_content(
                    platform_name, 
                    platform_config, 
                    reflections
                )
        
        # Save content plan
        today = datetime.now().strftime("%Y-%m-%d")
        plan_dir = Path("data/plans")
        plan_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = plan_dir / f"content_plan_{today}.json"
        with open(file_path, 'w') as f:
            json.dump(content_plan, f, indent=2, default=str)
            
        return content_plan
    
    def _plan_platform_content(self, platform: str, config: Dict, reflections: Dict) -> List[Dict]:
        """Plan content for a specific platform"""
        posts_per_day = config.get('posts_per_day', 1)
        content_types = config.get('content_types', ['general'])
        optimal_times = config.get('optimal_times_uk', ['12:00'])
        
        # Get trending keywords and recommendations
        trending_keywords = reflections.get('keyword_trends', {})
        recommendations = reflections.get('recommendations', {})
        
        planned_posts = []
        
        for i in range(posts_per_day):
            # Select content type
            content_type = random.choice(content_types)
            
            # Select topic based on trending keywords and xthreads.app relevance
            topic = self._select_topic(trending_keywords, recommendations, platform)
            
            # Select posting time from available slots
            if i < len(optimal_times):
                posting_time_str = optimal_times[i]
            else:
                # If more posts than time slots, add variation to last slot
                base_time = optimal_times[-1]
                base_dt = datetime.strptime(base_time, '%H:%M')
                varied_dt = base_dt + timedelta(minutes=random.randint(15, 45))
                posting_time_str = varied_dt.strftime('%H:%M')
            
            post_plan = {
                'platform': platform,
                'content_type': content_type,
                'topic': topic,
                'posting_time_uk': posting_time_str,
                'target_keywords': self._get_target_keywords(topic, trending_keywords),
                'content_angle': self._get_content_angle(content_type, topic, platform),
                'max_chars': config.get('max_chars', 500),
                'call_to_action': self._get_cta_suggestion(content_type, platform)
            }
            
            planned_posts.append(post_plan)
        
        return planned_posts
    
    def _select_topic(self, trending_keywords: Dict, recommendations: Dict, platform: str) -> str:
        """Select a topic based on trending data and xthreads.app relevance"""
        
        # xthreads.app relevant topics
        xthreads_topics = [
            "content creation struggles",
            "twitter growth tips",
            "writing better posts",
            "social media productivity",
            "overcoming writer's block",
            "content consistency",
            "engagement strategies",
            "personal branding",
            "building audience",
            "content automation"
        ]
        
        # Trending topics that align with our product
        relevant_trending = []
        for keyword in trending_keywords.keys():
            if any(topic_word in keyword.lower() for topic_word in 
                   ['content', 'writing', 'social', 'twitter', 'growth', 'productivity', 'automation']):
                relevant_trending.append(f"trending: {keyword}")
        
        # Combine and select
        all_topics = xthreads_topics + relevant_trending[:3]
        return random.choice(all_topics)
    
    def _get_target_keywords(self, topic: str, trending_keywords: Dict) -> List[str]:
        """Get target keywords for the topic"""
        base_keywords = ["content creation", "productivity", "social media"]
        
        # Add trending keywords that are relevant
        relevant_trending = [
            kw for kw in trending_keywords.keys()
            if any(base in kw.lower() for base in ['content', 'writing', 'social', 'growth'])
        ][:2]
        
        return base_keywords + relevant_trending
    
    def _get_content_angle(self, content_type: str, topic: str, platform: str) -> str:
        """Get the content angle based on type and platform"""
        
        angles = {
            'hook': [
                "Start with a surprising statistic",
                "Ask a thought-provoking question", 
                "Share a contrarian opinion",
                "Use a personal story opener"
            ],
            'thread': [
                "Step-by-step tutorial",
                "Lessons learned breakdown",
                "Myth-busting series",
                "Behind-the-scenes process"
            ],
            'tip': [
                "Quick actionable advice",
                "Tool recommendation",
                "Productivity hack",
                "Common mistake to avoid"
            ],
            'discussion': [
                "Ask for community input",
                "Share experience and ask for similar stories",
                "Debate a common belief",
                "Crowdsource solutions"
            ],
            'experience': [
                "Personal journey story",
                "Failure and lessons learned",
                "Success story with insights",
                "Day-in-the-life content"
            ]
        }
        
        return random.choice(angles.get(content_type, angles['tip']))
    
    def _get_cta_suggestion(self, content_type: str, platform: str) -> str:
        """Get call-to-action suggestion"""
        
        soft_ctas = [
            "What's your experience with this?",
            "Drop your thoughts below 👇",
            "Anyone else struggle with this?",
            "What would you add to this list?",
            "Share if this helped you!",
            "Built with xthreads.app ⚡",
            "Try xthreads.app for faster content creation",
            "Link to xthreads.app in comments"
        ]
        
        # Mix of engagement CTAs and soft product mentions
        if random.random() < 0.3:  # 30% chance of product mention
            return random.choice([cta for cta in soft_ctas if 'xthreads' in cta])
        else:
            return random.choice([cta for cta in soft_ctas if 'xthreads' not in cta])