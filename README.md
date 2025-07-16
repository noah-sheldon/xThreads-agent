# xthreads_agent 🤖

A fully local AI agent system that generates daily content to market xthreads.app across multiple social platforms.

## 🎯 What it does

Every day at 6 AM UK time, this system:
1. **Listens** - Scrapes trending content from X, Reddit, Threads, and Quora
2. **Reflects** - Analyzes patterns, keywords, and engagement metrics
3. **Plans** - Creates a content strategy based on insights
4. **Generates** - Uses GPT-4 to write platform-specific posts
5. **Exports** - Saves content calendar in Excel, CSV, and Markdown
6. **Notifies** - Alerts you when content is ready

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

Required API keys:
- `OPENAI_API_KEY` - Your OpenAI API key
- `REDDIT_CLIENT_ID` - Reddit API client ID
- `REDDIT_CLIENT_SECRET` - Reddit API secret
- `REDDIT_USER_AGENT` - Your app name (e.g., "xthreads_agent/1.0")

Optional:
- `TELEGRAM_BOT_TOKEN` - For notifications
- `TELEGRAM_CHAT_ID` - Your Telegram chat ID

### 3. Test Run
```bash
python main.py
```

### 4. Setup Daily Automation (Mac)
```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

## 📁 Project Structure

```
xthreads_agent/
├── main.py                 # Main orchestrator
├── config.json            # Platform settings
├── agents/                 # AI agents
│   ├── listener.py        # Scrapes trending content
│   ├── reflector.py       # Analyzes patterns
│   ├── planner.py         # Creates content plan
│   ├── generator.py       # Generates posts with GPT-4
│   ├── exporter.py        # Exports to files
│   └── notifier.py        # Sends notifications
├── utils/                  # Utilities
│   ├── scraper_utils.py   # Ethical scraping tools
│   ├── content_filters.py # Content safety filters
│   └── timezone_utils.py  # UK/US time conversion
├── data/                   # Generated data
│   ├── raw/               # Scraped content
│   ├── processed/         # Analysis results
│   ├── generated/         # AI-generated posts
│   └── exports/           # Final content calendars
└── logs/                   # Daily logs
```

## 🎛️ Configuration

Edit `config.json` to customize:

- **Platforms**: Enable/disable platforms, set posts per day
- **Content Types**: Hook tweets, threads, discussions, etc.
- **Posting Times**: Optimal UK times for each platform
- **Filters**: Content safety and competitor filtering
- **Scraping**: Rate limits and engagement thresholds

## 📊 Output Formats

The system exports daily content in multiple formats:

### Excel (.xlsx)
- **Content Calendar** sheet with all posts
- **Summary** sheet with statistics
- Auto-formatted columns and styling

### CSV (.csv)
- Simple format for importing into other tools
- Compatible with scheduling platforms

### Markdown (.md)
- Human-readable format
- Great for Notion or documentation
- Organized by platform and time

### JSON (.json)
- Raw data backup
- Programmatic access to all metadata

## 🤖 AI Agents Explained

### 1. Listener Agent
- Scrapes trending content from social platforms
- Uses ethical scraping with rate limiting
- Respects robots.txt and implements delays
- Filters content for safety and relevance

### 2. Reflector Agent
- Analyzes scraped content for patterns
- Extracts trending keywords and topics
- Identifies high-engagement content formats
- Generates insights for content strategy

### 3. Planner Agent
- Creates daily content plan based on insights
- Selects topics relevant to xthreads.app audience
- Assigns optimal posting times per platform
- Balances product promotion with value content

### 4. Generator Agent
- Uses GPT-4 to generate platform-specific content
- Includes xthreads.app context in all prompts
- Implements quality checks and retry logic
- Optimizes for engagement and authenticity

### 5. Exporter Agent
- Formats content into multiple file types
- Creates comprehensive content calendars
- Adds metadata and performance tracking
- Generates summary statistics

### 6. Notifier Agent
- Sends CLI notifications with daily summary
- Optional Telegram notifications
- Error reporting and status updates
- Performance metrics and next steps

## 🛡️ Content Safety

The system includes comprehensive content filtering:

- **Profanity Filter**: Removes inappropriate language
- **Political Filter**: Avoids controversial topics
- **Competitor Filter**: Prevents competitor mentions
- **NSFW Filter**: Blocks adult content
- **Quality Checks**: Ensures content meets standards

## ⏰ Optimal Posting Times

All times optimized for US engagement, converted to UK time:

| Platform | US Best Time | UK Time (BST) | Posts/Day | Format Mix |
|----------|--------------|---------------|-----------|------------|
| X/Twitter | 9AM–12PM EST | **2PM–5PM** | 3-4 | Text, image, hook, reply |
| Threads | 9AM–12PM EST | **2PM–5PM** | 2-3 | Text, meme, carousel |
| LinkedIn | 8–10AM EST | **1PM–3PM** | 1 | Carousel or video |
| Instagram | 11AM–2PM EST | **4PM–7PM** | 1 | Reels or carousel |
| TikTok | 12PM–3PM EST | **5PM–8PM** | 1 | Short video |
| Facebook | 1–3PM EST | **6PM–8PM** | 1 | Post + image or link |
| Reddit | 7AM–10AM EST | **12PM–3PM** | 1-2 | Comment, thread |
| Quora | 6–9PM EST | **11PM–2AM** | 1 | Answer or post |

## 🔧 Troubleshooting

### Common Issues

**"OpenAI API Error"**
- Check your API key in `.env`
- Ensure you have sufficient credits
- Verify the model name (default: gpt-4)

**"Reddit API Error"**
- Create a Reddit app at reddit.com/prefs/apps
- Add client ID and secret to `.env`
- Use a descriptive user agent

**"Scraping Failed"**
- Check internet connection
- Some sites may block automated requests
- Rate limiting may be too aggressive

**"No Content Generated"**
- Check content filters aren't too strict
- Verify trending content was scraped
- Review GPT-4 prompts for clarity

### Logs and Debugging

Daily logs are saved in `logs/YYYY-MM-DD.log`:
```bash
tail -f logs/$(date +%F).log  # Follow today's log
grep ERROR logs/*.log         # Find all errors
```

## 🚀 Advanced Usage

### Custom Prompts
Edit prompts in the `prompts/` directory to customize content generation.

### Platform Extensions
Add new platforms by:
1. Adding scraper method to `listener.py`
2. Updating `config.json` with platform settings
3. Adding platform-specific prompts

### Performance Tracking
The system saves metadata for future performance analysis:
- Engagement predictions
- Keyword effectiveness
- Content format success rates

## 📈 Roadmap

Future enhancements:
- [ ] Automated posting via APIs
- [ ] Performance tracking and optimization
- [ ] A/B testing for content variations
- [ ] Visual content generation
- [ ] Sentiment analysis
- [ ] Competitor monitoring
- [ ] Weekly/monthly reporting

## 🤝 Contributing

This is a local tool for xthreads.app marketing. For issues or improvements:

1. Check logs for error details
2. Review configuration settings
3. Test individual agents: `python -m agents.listener`
4. Submit detailed bug reports

## 📄 License

Private tool for xthreads.app marketing. Not for redistribution.

---

**Built with ❤️ for xthreads.app**

*Helping developers, founders, and creators write better content faster.*