#!/bin/bash

# xthreads_agent Cron Setup Script
# This script helps you set up daily automated runs

echo "🤖 xthreads_agent Cron Setup"
echo "=============================="

# Get current directory
CURRENT_DIR=$(pwd)
PYTHON_PATH=$(which python3)

echo "Current directory: $CURRENT_DIR"
echo "Python path: $PYTHON_PATH"

# Create logs directory
mkdir -p logs

# Create the cron command
CRON_COMMAND="0 6 * * * cd $CURRENT_DIR && $PYTHON_PATH main.py >> logs/\$(date +\\%F).log 2>&1"

echo ""
echo "Cron command to add:"
echo "===================="
echo "$CRON_COMMAND"
echo ""

# Ask user if they want to add it automatically
read -p "Do you want to add this to your crontab automatically? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -
    echo "✅ Cron job added successfully!"
    echo ""
    echo "The agent will now run daily at 6:00 AM UK time."
    echo "Logs will be saved in the logs/ directory."
else
    echo ""
    echo "Manual setup instructions:"
    echo "========================="
    echo "1. Run: crontab -e"
    echo "2. Add this line:"
    echo "   $CRON_COMMAND"
    echo "3. Save and exit"
fi

echo ""
echo "To view current cron jobs: crontab -l"
echo "To remove the cron job: crontab -e (then delete the line)"
echo "To test manually: python3 main.py"
echo ""
echo "🎉 Setup complete!"