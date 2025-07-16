#!/usr/bin/env python3
"""
Test script to verify xthreads_agent setup
"""

import os
from dotenv import load_dotenv

load_dotenv()
import sys
from pathlib import Path

def test_environment():
    """Test environment setup"""
    print("🧪 Testing xthreads_agent setup...")
    print("=" * 50)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check required directories
    required_dirs = ['data', 'logs', 'agents', 'utils', 'prompts']
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✅ Directory '{dir_name}' exists")
        else:
            print(f"❌ Directory '{dir_name}' missing")
    
    # Check environment variables
    required_env_vars = ['OPENAI_API_KEY']
    optional_env_vars = ['REDDIT_CLIENT_ID', 'TELEGRAM_BOT_TOKEN']
    
    print("\n🔑 Environment Variables:")
    for var in required_env_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} is missing (required)")
    
    for var in optional_env_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"⚠️  {var} is not set (optional)")
    
    # Test imports
    print("\n📦 Testing imports...")
    try:
        import openai
        print("✅ OpenAI library imported")
    except ImportError:
        print("❌ OpenAI library not found")
    
    try:
        import pandas
        print("✅ Pandas imported")
    except ImportError:
        print("❌ Pandas not found")
    
    try:
        from agents.listener import ListenerAgent
        print("✅ Agents imported successfully")
    except ImportError as e:
        print(f"❌ Agent import failed: {e}")
    
    # Test configuration
    print("\n⚙️  Testing configuration...")
    try:
        import json
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("✅ Configuration loaded")
        
        enabled_platforms = [p for p, conf in config['platforms'].items() if conf.get('enabled')]
        print(f"✅ Enabled platforms: {', '.join(enabled_platforms)}")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Setup test complete!")
    print("\nNext steps:")
    print("1. Add your API keys to .env file")
    print("2. Run: python main.py")
    print("3. Set up cron: ./setup_cron.sh")

if __name__ == "__main__":
    test_environment()