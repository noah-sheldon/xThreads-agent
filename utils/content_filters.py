"""
Content filtering utilities to ensure safe and appropriate content
"""

import re
from typing import List, Dict

class ContentFilter:
    def __init__(self, filter_config: Dict):
        self.config = filter_config
        
        # Load filter lists
        self.profanity_words = self._load_profanity_list()
        self.political_keywords = self._load_political_keywords()
        self.competitor_names = filter_config.get('competitors', [])
        self.nsfw_keywords = self._load_nsfw_keywords()
        
    def is_safe_content(self, content: str) -> bool:
        """Check if content passes all filters"""
        if not content:
            return False
            
        content_lower = content.lower()
        
        # Check profanity filter
        if self.config.get('profanity', True) and self._contains_profanity(content_lower):
            return False
            
        # Check political content filter
        if self.config.get('politics', True) and self._contains_political_content(content_lower):
            return False
            
        # Check competitor mentions
        if self._contains_competitor_mentions(content_lower):
            return False
            
        # Check NSFW content
        if self.config.get('nsfw', True) and self._contains_nsfw_content(content_lower):
            return False
            
        return True
    
    def _load_profanity_list(self) -> List[str]:
        """Load profanity word list"""
        # Basic profanity list - in production, use a comprehensive library
        return [
            'damn', 'hell', 'shit', 'fuck', 'bitch', 'ass', 'bastard',
            'crap', 'piss', 'dick', 'cock', 'pussy', 'whore', 'slut'
        ]
    
    def _load_political_keywords(self) -> List[str]:
        """Load political keywords to avoid"""
        return [
            'trump', 'biden', 'democrat', 'republican', 'liberal', 'conservative',
            'election', 'vote', 'politics', 'political', 'government', 'congress',
            'senate', 'president', 'politician', 'campaign', 'ballot', 'policy',
            'immigration', 'abortion', 'gun control', 'healthcare', 'taxes',
            'climate change', 'covid', 'vaccine', 'mask', 'lockdown'
        ]
    
    def _load_nsfw_keywords(self) -> List[str]:
        """Load NSFW keywords"""
        return [
            'sex', 'sexual', 'porn', 'nude', 'naked', 'adult', 'xxx',
            'erotic', 'fetish', 'kinky', 'orgasm', 'masturbate', 'horny'
        ]
    
    def _contains_profanity(self, content: str) -> bool:
        """Check for profanity"""
        for word in self.profanity_words:
            if re.search(r'\b' + re.escape(word) + r'\b', content):
                return True
        return False
    
    def _contains_political_content(self, content: str) -> bool:
        """Check for political content"""
        for keyword in self.political_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', content):
                return True
        return False
    
    def _contains_competitor_mentions(self, content: str) -> bool:
        """Check for competitor mentions"""
        for competitor in self.competitor_names:
            if re.search(r'\b' + re.escape(competitor.lower()) + r'\b', content):
                return True
        return False
    
    def _contains_nsfw_content(self, content: str) -> bool:
        """Check for NSFW content"""
        for keyword in self.nsfw_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', content):
                return True
        return False
    
    def clean_content(self, content: str) -> str:
        """Clean content by removing filtered words"""
        cleaned = content
        
        # Replace profanity with asterisks
        for word in self.profanity_words:
            pattern = r'\b' + re.escape(word) + r'\b'
            replacement = '*' * len(word)
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
        
        return cleaned