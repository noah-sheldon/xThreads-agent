"""
Scraper utilities for ethical web scraping
"""

import random
import time
import requests
from fake_useragent import UserAgent
from urllib.robotparser import RobotFileParser

class ScraperUtils:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        
    def get_random_user_agent(self) -> str:
        """Get a random user agent string"""
        try:
            return self.ua.random
        except:
            # Fallback user agents
            fallback_agents = [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            ]
            return random.choice(fallback_agents)
    
    def get_headers(self) -> dict:
        """Get headers for HTTP requests"""
        return {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def get_random_delay(self, min_delay: float = 1.0, max_delay: float = 3.0) -> float:
        """Get a random delay between requests"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        return delay
    
    def can_fetch(self, url: str, user_agent: str = '*') -> bool:
        """Check if we can fetch a URL according to robots.txt"""
        try:
            from urllib.parse import urljoin, urlparse
            
            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            
            return rp.can_fetch(user_agent, url)
        except:
            # If we can't check robots.txt, be conservative and allow
            return True
    
    def make_request(self, url: str, **kwargs) -> requests.Response:
        """Make a request with proper headers and delays"""
        headers = kwargs.pop('headers', self.get_headers())
        
        # Add random delay before request
        self.get_random_delay()
        
        # Check robots.txt
        if not self.can_fetch(url):
            raise Exception(f"Robots.txt disallows fetching {url}")
        
        return self.session.get(url, headers=headers, **kwargs)