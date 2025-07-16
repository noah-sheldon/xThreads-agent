#!/usr/bin/env python3
"""
xthreads_agent - Local AI Marketing Agent
Generates daily content for xthreads.app across multiple platforms
"""

import os
from dotenv import load_dotenv

load_dotenv()
import sys
import json
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from agents.listener import ListenerAgent
from agents.reflector import ReflectorAgent
from agents.planner import PlannerAgent
from agents.generator import GeneratorAgent
from agents.exporter import ExporterAgent
from agents.notifier import NotifierAgent
from utils.timezone_utils import get_uk_time

def setup_logging():
    """Setup logging configuration"""
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"{today}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def load_config():
    """Load configuration from config.json"""
    config_path = project_root / "config.json"
    with open(config_path, 'r') as f:
        return json.load(f)

def run_agent_pipeline():
    """Run the complete agent pipeline"""
    logger = setup_logging()
    config = load_config()
    
    logger.info("🚀 Starting xthreads_agent daily run")
    logger.info(f"⏰ UK Time: {get_uk_time()}")
    
    # Initialize data storage
    today = datetime.now().strftime("%Y-%m-%d")
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)
    
    pipeline_data = {
        "date": today,
        "trending_content": {},
        "reflections": {},
        "content_plan": {},
        "generated_posts": {},
        "export_files": []
    }
    
    try:
        # Agent 1: Listen - Scrape trending content
        logger.info("🎧 Running Listener Agent...")
        listener = ListenerAgent(config)
        pipeline_data["trending_content"] = listener.scrape_all_platforms()
        logger.info(f"✅ Scraped content from {len(pipeline_data['trending_content'])} platforms")
        
        # Agent 2: Reflect - Analyze patterns
        logger.info("🤔 Running Reflector Agent...")
        reflector = ReflectorAgent(config)
        pipeline_data["reflections"] = reflector.analyze_content(pipeline_data["trending_content"])
        logger.info("✅ Content analysis complete")
        
        # Agent 3: Plan - Select content ideas
        logger.info("📋 Running Planner Agent...")
        planner = PlannerAgent(config)
        pipeline_data["content_plan"] = planner.create_content_plan(pipeline_data["reflections"])
        logger.info(f"✅ Content plan created for {len(pipeline_data['content_plan'])} platforms")
        
        # Agent 4: Generate - Create posts with GPT-4
        logger.info("✍️ Running Generator Agent...")
        generator = GeneratorAgent(config)
        pipeline_data["generated_posts"] = generator.generate_all_posts(pipeline_data["content_plan"])
        logger.info(f"✅ Generated {sum(len(posts) for posts in pipeline_data['generated_posts'].values())} posts")
        
        # Agent 5: Export - Save to files
        logger.info("📤 Running Exporter Agent...")
        exporter = ExporterAgent(config)
        pipeline_data["export_files"] = exporter.export_content_calendar(pipeline_data["generated_posts"])
        logger.info(f"✅ Exported to {len(pipeline_data['export_files'])} files")
        
        # Agent 6: Notify - Alert completion
        logger.info("📢 Running Notifier Agent...")
        notifier = NotifierAgent(config)
        notifier.send_completion_notification(pipeline_data)
        logger.info("✅ Notifications sent")
        
        logger.info("🎉 xthreads_agent pipeline completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed: {str(e)}")
        logger.exception("Full error details:")
        return False

if __name__ == "__main__":
    success = run_agent_pipeline()
    sys.exit(0 if success else 1)