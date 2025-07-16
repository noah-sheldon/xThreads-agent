"""
Reflector Agent - Analyzes scraped content for patterns and insights
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from collections import Counter
import re

class ReflectorAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize processed data directory
        self.data_dir = Path("data/processed")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def analyze_content(self, trending_content: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Analyze trending content for patterns and insights"""
        self.logger.info("🔍 Analyzing content patterns...")
        
        analysis = {
            'timestamp': datetime.now(),
            'platform_insights': {},
            'keyword_trends': {},
            'engagement_patterns': {},
            'content_formats': {},
            'posting_times': {},
            'recommendations': {}
        }
        
        for platform, posts in trending_content.items():
            if posts:
                analysis['platform_insights'][platform] = self._analyze_platform_content(platform, posts)
                
        # Cross-platform analysis
        analysis['keyword_trends'] = self._extract_trending_keywords(trending_content)
        analysis['engagement_patterns'] = self._analyze_engagement_patterns(trending_content)
        analysis['content_formats'] = self._analyze_content_formats(trending_content)
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        # Save analysis
        today = datetime.now().strftime("%Y-%m-%d")
        file_path = self.data_dir / f"reflection_{today}.json"
        with open(file_path, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
            
        return analysis
    
    def _analyze_platform_content(self, platform: str, posts: List[Dict]) -> Dict[str, Any]:
        """Analyze content specific to a platform"""
        if not posts:
            return {}
            
        insights = {
            'total_posts': len(posts),
            'avg_engagement': 0,
            'top_keywords': [],
            'content_length_stats': {},
            'high_performers': []
        }
        
        # Calculate engagement metrics
        if platform == 'twitter':
            engagements = [(p.get('likes', 0) + p.get('retweets', 0) + p.get('replies', 0)) for p in posts]
            insights['avg_engagement'] = sum(engagements) / len(engagements) if engagements else 0
            
            # Find high performers (top 20%)
            sorted_posts = sorted(posts, key=lambda x: x.get('likes', 0) + x.get('retweets', 0), reverse=True)
            insights['high_performers'] = sorted_posts[:max(1, len(sorted_posts) // 5)]
            
        elif platform == 'reddit':
            scores = [p.get('score', 0) for p in posts]
            insights['avg_engagement'] = sum(scores) / len(scores) if scores else 0
            
            sorted_posts = sorted(posts, key=lambda x: x.get('score', 0), reverse=True)
            insights['high_performers'] = sorted_posts[:max(1, len(sorted_posts) // 5)]
        
        # Analyze content length
        if platform in ['twitter', 'threads']:
            lengths = [len(p.get('content', '')) for p in posts if p.get('content')]
            if lengths:
                insights['content_length_stats'] = {
                    'avg_length': sum(lengths) / len(lengths),
                    'min_length': min(lengths),
                    'max_length': max(lengths)
                }
        
        # Extract keywords from high-performing content
        high_perf_text = ' '.join([
            p.get('content', '') + ' ' + p.get('title', '') 
            for p in insights['high_performers']
        ])
        insights['top_keywords'] = self._extract_keywords(high_perf_text)
        
        return insights
    
    def _extract_trending_keywords(self, trending_content: Dict[str, List[Dict]]) -> Dict[str, int]:
        """Extract trending keywords across all platforms"""
        all_text = ""
        
        for platform, posts in trending_content.items():
            for post in posts:
                text = ""
                if 'content' in post:
                    text += post['content'] + " "
                if 'title' in post:
                    text += post['title'] + " "
                if 'question' in post:
                    text += post['question'] + " "
                all_text += text
        
        keywords = self._extract_keywords(all_text)
        return dict(keywords.most_common(20))
    
    def _extract_keywords(self, text: str) -> Counter:
        """Extract meaningful keywords from text"""
        if not text:
            return Counter()
            
        # Clean and normalize text
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we',
            'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her',
            'its', 'our', 'their', 'just', 'now', 'then', 'here', 'there', 'when',
            'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
            'same', 'so', 'than', 'too', 'very', 'can', 'may', 'might', 'must',
            'shall', 'will', 'would'
        }
        
        # Extract words and filter
        words = text.split()
        meaningful_words = [
            word for word in words 
            if len(word) > 2 and word not in stop_words and word.isalpha()
        ]
        
        # Also extract 2-word phrases
        phrases = []
        for i in range(len(meaningful_words) - 1):
            phrase = f"{meaningful_words[i]} {meaningful_words[i+1]}"
            phrases.append(phrase)
        
        # Combine single words and phrases
        all_terms = meaningful_words + phrases
        
        return Counter(all_terms)
    
    def _analyze_engagement_patterns(self, trending_content: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Analyze what drives engagement"""
        patterns = {
            'high_engagement_indicators': [],
            'content_length_vs_engagement': {},
            'timing_patterns': {}
        }
        
        # Analyze Twitter engagement patterns
        if 'twitter' in trending_content:
            twitter_posts = trending_content['twitter']
            high_engagement = [
                p for p in twitter_posts 
                if (p.get('likes', 0) + p.get('retweets', 0)) > 100
            ]
            
            if high_engagement:
                # Common patterns in high-engagement posts
                common_elements = []
                for post in high_engagement:
                    content = post.get('content', '').lower()
                    if '?' in content:
                        common_elements.append('question')
                    if any(word in content for word in ['tip', 'tips', 'how to']):
                        common_elements.append('educational')
                    if any(word in content for word in ['thread', '🧵', '1/']):
                        common_elements.append('thread')
                    if content.count('\n') > 2:
                        common_elements.append('multi_line')
                
                patterns['high_engagement_indicators'] = list(set(common_elements))
        
        return patterns
    
    def _analyze_content_formats(self, trending_content: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Analyze successful content formats"""
        formats = {
            'twitter': {
                'hooks': [],
                'threads': [],
                'quotes': [],
                'tips': []
            },
            'reddit': {
                'discussions': [],
                'experiences': [],
                'questions': []
            }
        }
        
        # Analyze Twitter formats
        if 'twitter' in trending_content:
            for post in trending_content['twitter']:
                content = post.get('content', '')
                if content:
                    # Classify content type
                    if content.startswith(('What', 'How', 'Why', 'When', 'Where')):
                        formats['twitter']['hooks'].append({
                            'content': content[:100] + '...' if len(content) > 100 else content,
                            'engagement': post.get('likes', 0) + post.get('retweets', 0)
                        })
                    elif 'thread' in content.lower() or '🧵' in content or '1/' in content:
                        formats['twitter']['threads'].append({
                            'content': content[:100] + '...' if len(content) > 100 else content,
                            'engagement': post.get('likes', 0) + post.get('retweets', 0)
                        })
        
        return formats
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate content recommendations based on analysis"""
        recommendations = {
            'content_ideas': [],
            'format_suggestions': [],
            'timing_advice': [],
            'keyword_focus': []
        }
        
        # Content ideas based on trending keywords
        top_keywords = analysis.get('keyword_trends', {})
        if top_keywords:
            top_5_keywords = list(top_keywords.keys())[:5]
            recommendations['content_ideas'] = [
                f"Create content around '{keyword}' (trending)" 
                for keyword in top_5_keywords
            ]
        
        # Format suggestions based on high performers
        twitter_insights = analysis.get('platform_insights', {}).get('twitter', {})
        if twitter_insights.get('high_performers'):
            recommendations['format_suggestions'] = [
                "Use question-based hooks for higher engagement",
                "Consider thread format for complex topics",
                "Keep posts concise but informative"
            ]
        
        # Keyword focus for xthreads.app
        xthreads_keywords = [
            "content creation", "twitter growth", "social media", "writing tools",
            "productivity", "automation", "AI writing", "content strategy"
        ]
        
        relevant_trending = [
            kw for kw in top_keywords.keys() 
            if any(xkw in kw.lower() for xkw in xthreads_keywords)
        ]
        
        if relevant_trending:
            recommendations['keyword_focus'] = relevant_trending[:3]
        else:
            recommendations['keyword_focus'] = ["content creation", "productivity", "AI tools"]
        
        return recommendations