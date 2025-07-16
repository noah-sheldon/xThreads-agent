"""
Listener Agent - Scrapes trending content from social platforms
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

import requests
import praw
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.scraper_utils import ScraperUtils
from utils.content_filters import ContentFilter

class ListenerAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.scraper_utils = ScraperUtils()
        self.content_filter = ContentFilter(config['content_filters'])
        
        # Initialize data directory
        self.data_dir = Path("data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def scrape_all_platforms(self) -> Dict[str, List[Dict]]:
        """Scrape trending content from all enabled platforms"""
        results = {}
        
        platforms = self.config['platforms']
        
        if platforms.get('twitter', {}).get('enabled'):
            results['twitter'] = self._scrape_twitter()
            
        if platforms.get('reddit', {}).get('enabled'):
            results['reddit'] = self._scrape_reddit()
            
        if platforms.get('threads', {}).get('enabled'):
            results['threads'] = self._scrape_threads()
            
        # Save raw data
        today = datetime.now().strftime("%Y-%m-%d")
        for platform, data in results.items():
            file_path = self.data_dir / f"{platform}_{today}.json"
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
        return results
    
    def _scrape_twitter(self) -> List[Dict]:
        """Scrape trending Twitter content using snscrape"""
        self.logger.info("🐦 Scraping Twitter trending content...")
        
        try:
            import snscrape.modules.twitter as sntwitter
            
            # Search for trending topics related to our audience
            search_terms = [
                "indie hacker",
                "startup founder", 
                "content creation",
                "twitter growth",
                "social media tips",
                "building in public"
            ]
            
            posts = []
            max_posts = self.config['scraping']['max_posts_per_platform']
            
            for term in search_terms:
                try:
                    query = f'"{term}" min_faves:50 lang:en'
                    scraper = sntwitter.TwitterSearchScraper(query)
                    
                    for i, tweet in enumerate(scraper.get_items()):
                        if i >= max_posts // len(search_terms):
                            break
                            
                        if tweet.date > datetime.now() - timedelta(hours=24):
                            post_data = {
                                'id': tweet.id,
                                'content': tweet.rawContent,
                                'author': tweet.user.username,
                                'likes': tweet.likeCount,
                                'retweets': tweet.retweetCount,
                                'replies': tweet.replyCount,
                                'created_at': tweet.date,
                                'url': tweet.url,
                                'search_term': term
                            }
                            
                            if self.content_filter.is_safe_content(post_data['content']):
                                posts.append(post_data)
                                
                    time.sleep(self.scraper_utils.get_random_delay())
                    
                except Exception as e:
                    self.logger.warning(f"Failed to scrape term '{term}': {e}")
                    continue
                    
            self.logger.info(f"✅ Scraped {len(posts)} Twitter posts")
            return posts
            
        except Exception as e:
            self.logger.error(f"Twitter scraping failed: {e}")
            return []
    
    def _scrape_reddit(self) -> List[Dict]:
        """Scrape trending Reddit content using praw"""
        self.logger.info("🔴 Scraping Reddit trending content...")
        
        try:
            reddit = praw.Reddit(
                client_id=os.getenv('REDDIT_CLIENT_ID'),
                client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                user_agent=os.getenv('REDDIT_USER_AGENT')
            )
            
            posts = []
            subreddits = self.config['platforms']['reddit'].get('subreddits', [])
            max_posts = self.config['scraping']['max_posts_per_platform']
            
            for subreddit_name in subreddits:
                try:
                    subreddit = reddit.subreddit(subreddit_name)
                    
                    for submission in subreddit.hot(limit=max_posts // len(subreddits)):
                        # Check if post is recent
                        post_time = datetime.fromtimestamp(submission.created_utc)
                        if post_time > datetime.now() - timedelta(hours=24):
                            
                            post_data = {
                                'id': submission.id,
                                'title': submission.title,
                                'content': submission.selftext,
                                'author': str(submission.author),
                                'score': submission.score,
                                'comments': submission.num_comments,
                                'created_at': post_time,
                                'url': submission.url,
                                'subreddit': subreddit_name
                            }
                            
                            if self.content_filter.is_safe_content(f"{post_data['title']} {post_data['content']}"):
                                posts.append(post_data)
                                
                    time.sleep(self.scraper_utils.get_random_delay())
                    
                except Exception as e:
                    self.logger.warning(f"Failed to scrape r/{subreddit_name}: {e}")
                    continue
                    
            self.logger.info(f"✅ Scraped {len(posts)} Reddit posts")
            return posts
            
        except Exception as e:
            self.logger.error(f"Reddit scraping failed: {e}")
            return []
    
    def _scrape_threads(self) -> List[Dict]:
        """Scrape Threads content using Selenium"""
        self.logger.info("🧵 Scraping Threads trending content...")
        
        try:
            # Setup headless Chrome
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument(f"--user-agent={self.scraper_utils.get_random_user_agent()}")
            
            driver = webdriver.Chrome(options=chrome_options)
            posts = []
            
            try:
                # Navigate to Threads (public content only)
                driver.get("https://www.threads.net/")
                time.sleep(3)
                
                # Look for post elements (this is a simplified example)
                # In practice, you'd need to analyze the actual DOM structure
                post_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='post']")
                
                for element in post_elements[:20]:  # Limit to avoid rate limiting
                    try:
                        content = element.find_element(By.CSS_SELECTOR, "[data-testid='post-text']").text
                        author = element.find_element(By.CSS_SELECTOR, "[data-testid='username']").text
                        
                        post_data = {
                            'content': content,
                            'author': author,
                            'platform': 'threads',
                            'scraped_at': datetime.now()
                        }
                        
                        if self.content_filter.is_safe_content(content):
                            posts.append(post_data)
                            
                    except Exception as e:
                        continue
                        
            finally:
                driver.quit()
                
            self.logger.info(f"✅ Scraped {len(posts)} Threads posts")
            return posts
            
        except Exception as e:
            self.logger.error(f"Threads scraping failed: {e}")
            return []
    
    def _scrape_quora(self) -> List[Dict]:
        """Scrape Quora trending questions"""
        self.logger.info("❓ Scraping Quora trending content...")
        
        try:
            headers = self.scraper_utils.get_headers()
            
            # Search for relevant topics
            search_terms = ["startup", "entrepreneurship", "content marketing"]
            posts = []
            
            for term in search_terms:
                url = f"https://www.quora.com/search?q={term}"
                
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract questions (simplified - actual selectors may vary)
                    questions = soup.find_all('a', class_='question_link')
                    
                    for q in questions[:10]:
                        post_data = {
                            'question': q.get_text().strip(),
                            'url': f"https://www.quora.com{q.get('href')}",
                            'search_term': term,
                            'scraped_at': datetime.now()
                        }
                        
                        if self.content_filter.is_safe_content(post_data['question']):
                            posts.append(post_data)
                
                time.sleep(self.scraper_utils.get_random_delay())
                
            self.logger.info(f"✅ Scraped {len(posts)} Quora questions")
            return posts
            
        except Exception as e:
            self.logger.error(f"Quora scraping failed: {e}")
            return []