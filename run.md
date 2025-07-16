 How to Run xthreads_agent
Here's the complete step-by-step guide to get your AI marketing agent running:

📋 Prerequisites
Python 3.9+ (for zoneinfo support)
Mac/Linux (for cron scheduling)
API Keys (OpenAI required, Reddit optional)
🛠️ Step 1: Install Dependencies

# Install Python packages
pip install -r requirements.txt

# If you get permission errors, use:
pip install --user -r requirements.txt
🔑 Step 2: Setup API Keys

# Copy the environment template
cp .env.example .env

# Edit with your actual keys
nano .env
# or
open .env
Required in .env:


# OpenAI API Key (REQUIRED)
OPENAI_API_KEY=sk-your-openai-key-here

# Reddit API (OPTIONAL but recommended)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=xthreads_agent/1.0

# Telegram Bot (OPTIONAL)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
🔗 Getting API Keys:
OpenAI API Key:

Go to platform.openai.com
Sign up/login → API Keys → Create new key
Copy the key (starts with sk-)
Reddit API (Optional):

Go to reddit.com/prefs/apps
Click "Create App" → Choose "script"
Copy Client ID and Secret
🧪 Step 3: Test the Setup

# Verify everything is configured correctly
python test_run.py
You should see:


🧪 Testing xthreads_agent setup...
✅ Directory 'agents' exists
✅ OPENAI_API_KEY is set
✅ OpenAI library imported
✅ Agents imported successfully
✅ Configuration loaded
🎉 Setup test complete!
🎯 Step 4: Run Your First Generation

# Generate today's content
python main.py
What happens:

Scrapes trending content (2-3 minutes)
Analyzes patterns and keywords (30 seconds)
Plans content strategy (10 seconds)
Generates 14 posts with GPT-4 (1-2 minutes)
Exports to Excel/CSV/Markdown (10 seconds)
Notifies you when complete
Expected output:


🚀 Starting xthreads_agent daily run
🎧 Running Listener Agent...
✅ Scraped content from 4 platforms
🤔 Running Reflector Agent...
✅ Content analysis complete
📋 Running Planner Agent...
✅ Content plan created for 8 platforms
✍️ Running Generator Agent...
✅ Generated 14 posts
📤 Running Exporter Agent...
✅ Exported to 3 files
📢 Running Notifier Agent...
✅ Notifications sent
🎉 xthreads_agent pipeline completed successfully!
📁 Step 5: Check Your Generated Content
Your content will be saved in:


data/exports/
├── content-calendar-2025-01-17.xlsx  ← Main file to use
├── content-calendar-2025-01-17.csv   ← Backup format
└── content-calendar-2025-01-17.md    ← Human-readable
Open the Excel file - it contains:

All 14 posts ready to copy-paste
Optimal posting times (UK timezone)
Platform-specific formatting
Character counts
Target keywords
⏰ Step 6: Setup Daily Automation

# Make the setup script executable
chmod +x setup_cron.sh

# Run the cron setup
./setup_cron.sh
This will:

Show you the cron command
Ask if you want to add it automatically
Set up daily runs at 6 AM UK time
Manual cron setup:


# Edit crontab
crontab -e

# Add this line (replace /path/to with your actual path):
0 6 * * * cd /path/to/xthreads_agent && python main.py >> logs/$(date +\%F).log 2>&1
🔍 Troubleshooting
"OpenAI API Error"

# Check your API key
echo $OPENAI_API_KEY
# Should show your key starting with sk-

# Test API connection
python -c "import openai; print('OpenAI connected!')"
"Module not found"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
"Permission denied"

# Fix script permissions
chmod +x setup_cron.sh
chmod +x test_run.py
"No content generated"

# Check logs for details
tail -f logs/$(date +%F).log

# Run with verbose output
python main.py 2>&1 | tee debug.log
📊 Daily Workflow
Once set up, here's your daily routine:

6 AM UK: Agent runs automatically
6:05 AM: Check your email/Telegram for completion notification
Morning: Open the Excel file from data/exports/
Copy-paste posts to respective platforms at scheduled times
Monitor engagement and adjust strategy
🎯 What You'll Get Daily
14 posts across 8 platforms:

4 Twitter posts (hooks, tips, threads, replies)
3 Threads posts (stories, memes, carousels)
2 Reddit posts (discussions, comments)
1 each: LinkedIn, Instagram, TikTok, Facebook, Quora
All optimized for:

✅ US peak engagement times
✅ xthreads.app promotion (subtle, not salesy)
✅ Trending keywords and topics
✅ Platform-specific formats
✅ Character limits and best practices
🚀 Ready to Launch?
Run this command to start generating your first batch of content:


python main.py
Your AI marketing agent is now ready to generate daily content that grows xthreads.app! 🎉

