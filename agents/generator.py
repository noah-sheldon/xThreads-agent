"""
Generator Agent - Uses OpenAI GPT-4 to generate content based on plans
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import time

import openai
from openai import OpenAI

class GeneratorAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('GPT_MODEL', 'gpt-4')
        self.max_retries = int(os.getenv('MAX_RETRIES', '2'))
        
        # Load prompts
        self.prompts_dir = Path("prompts")
        self.system_prompt = self._load_system_prompt()
        
    def generate_all_posts(self, content_plan: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        """Generate posts for all platforms based on content plan"""
        self.logger.info("✍️ Generating content with GPT-4...")
        
        generated_posts = {}
        
        for platform, posts_plan in content_plan.items():
            generated_posts[platform] = []
            
            for post_plan in posts_plan:
                post_content = self._generate_single_post(platform, post_plan)
                if post_content:
                    generated_posts[platform].append(post_content)
        
        # Save generated content
        today = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path("data/generated")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = output_dir / f"generated_posts_{today}.json"
        with open(file_path, 'w') as f:
            json.dump(generated_posts, f, indent=2, default=str)
            
        return generated_posts
    
    def _generate_single_post(self, platform: str, post_plan: Dict) -> Dict[str, Any]:
        """Generate a single post with retry logic"""
        
        for attempt in range(self.max_retries + 1):
            try:
                # Create platform-specific prompt
                prompt = self._create_generation_prompt(platform, post_plan)
                
                # Generate content
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                
                generated_text = response.choices[0].message.content.strip()
                
                # Quality check
                if self._is_quality_content(generated_text, post_plan):
                    return {
                        **post_plan,
                        'generated_content': generated_text,
                        'generated_at': datetime.now(),
                        'attempt': attempt + 1,
                        'status': 'success'
                    }
                else:
                    self.logger.warning(f"Low quality content on attempt {attempt + 1}")
                    
            except Exception as e:
                self.logger.error(f"Generation failed on attempt {attempt + 1}: {e}")
                
            # Wait before retry
            if attempt < self.max_retries:
                time.sleep(2)
        
        # All attempts failed
        return {
            **post_plan,
            'generated_content': None,
            'generated_at': datetime.now(),
            'attempt': self.max_retries + 1,
            'status': 'failed'
        }
    
    def _load_system_prompt(self) -> str:
        """Load the system prompt for xthreads.app context"""
        return """You are generating content for xthreads.app — an AI-powered tool that helps people write better posts on X and Threads. 

Your audience: developers, founders, indie hackers, and content creators who want to write engaging, high-performing posts with less overthinking.

Key messaging:
- Help solve common content creation struggles (writer's block, low engagement, content anxiety)
- Highlight simple wins (scroll-stopping content, faster writing, growing online presence)
- Be punchy, helpful, and human
- Add soft CTAs when appropriate: "Built with xthreads.app" or "Try it free"

Voice & Tone:
- Conversational and authentic
- Helpful without being preachy
- Confident but not arrogant
- Use emojis sparingly and naturally
- Avoid excessive hashtags

Do NOT sound like a sales pitch. Focus on providing value first, product mentions second."""
    
    def _create_generation_prompt(self, platform: str, post_plan: Dict) -> str:
        """Create a specific generation prompt for the post"""
        
        topic = post_plan['topic']
        content_type = post_plan['content_type']
        content_angle = post_plan['content_angle']
        target_keywords = post_plan.get('target_keywords', [])
        max_chars = post_plan.get('max_chars', 500)
        cta = post_plan.get('call_to_action', '')
        
        platform_guidelines = {
            'twitter': "Write for Twitter/X. Keep it concise, engaging, and shareable. Use line breaks for readability.",
            'threads': "Write for Threads. Can be slightly longer than Twitter. Focus on storytelling and community engagement.",
            'reddit': "Write for Reddit. Be authentic, helpful, and community-focused. Avoid obvious self-promotion.",
            'linkedin': "Write for LinkedIn. Professional tone but still engaging. Focus on insights and value."
        }
        
        content_type_instructions = {
            'hook': "Create a compelling hook that stops scrolling. Start strong and make people want to read more.",
            'thread': "Create the first post of a thread. Tease the value and indicate it's a thread (🧵 or 1/X).",
            'text': "Create engaging text content that provides value and encourages interaction.",
            'image': "Write compelling text to accompany an image post. Focus on the caption.",
            'reply': "Write a thoughtful reply or comment that adds value to conversations.",
            'meme': "Create text for a meme-style post that's relatable and shareable.",
            'carousel': "Write the first slide of a carousel post with clear value proposition.",
            'video': "Write a script or caption for video content.",
            'reels': "Create engaging text for Instagram Reels format.",
            'short_video': "Write a brief, punchy script for short-form video content.",
            'post_image': "Create text to accompany an image post on Facebook.",
            'link': "Write compelling text to share a link with context and value.",
            'answer': "Write a comprehensive answer to a question on Quora.",
            'comment': "Create a valuable comment that starts discussions.",
            'tip': "Share a specific, actionable tip that people can implement immediately.",
            'discussion': "Start a discussion by sharing an insight and asking for community input.",
            'experience': "Share a personal experience or story with lessons learned.",
            'professional': "Create professional content suitable for LinkedIn audience."
        }
        
        prompt = f"""
Platform: {platform}
{platform_guidelines.get(platform, '')}

Content Type: {content_type}
{content_type_instructions.get(content_type, '')}

Topic: {topic}
Content Angle: {content_angle}
Target Keywords: {', '.join(target_keywords)}
Character Limit: {max_chars}
Call to Action: {cta}

Requirements:
1. Stay within {max_chars} characters
2. Include relevant keywords naturally
3. Make it engaging and valuable
4. Match the content angle specified
5. Include the CTA if it fits naturally
6. Focus on helping the audience with their content creation challenges

Generate the post content now:
"""
        
        return prompt
    
    def _is_quality_content(self, content: str, post_plan: Dict) -> bool:
        """Check if generated content meets quality standards"""
        if not content:
            return False
            
        # Check length constraints
        max_chars = post_plan.get('max_chars', 500)
        if len(content) > max_chars:
            return False
            
        # Check minimum length (avoid too short posts)
        if len(content) < 50:
            return False
            
        # Check for placeholder text or incomplete content
        placeholder_indicators = [
            '[insert', '[add', '[your', 'lorem ipsum', 'placeholder',
            'example text', 'sample content'
        ]
        
        content_lower = content.lower()
        if any(indicator in content_lower for indicator in placeholder_indicators):
            return False
            
        # Check for basic engagement elements
        engagement_indicators = [
            '?', '!', 'you', 'your', 'we', 'us', 'how', 'why', 'what',
            'tip', 'learn', 'discover', 'secret', 'mistake', 'avoid'
        ]
        
        has_engagement = any(indicator in content_lower for indicator in engagement_indicators)
        
        # Check for xthreads.app relevance (should mention content creation concepts)
        relevance_keywords = [
            'content', 'post', 'write', 'writing', 'create', 'social',
            'twitter', 'thread', 'engagement', 'audience', 'growth'
        ]
        
        has_relevance = any(keyword in content_lower for keyword in relevance_keywords)
        
        return has_engagement and has_relevance