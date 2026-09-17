import os
import sys
import json
import time
from datetime import datetime

# PythonAnywhere environment detection
PYTHONANYWHERE_MODE = True

print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 AI Revenue Machine - PythonAnywhere Edition")
print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Mode: PYTHONANYWHERE")

# Load configuration
try:
    with open(os.path.expanduser('~/ai-revenue-machine/config.json'), 'r') as f:
        config = json.load(f)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Config loaded")
except Exception as e:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✗ Config error: {e}")
    sys.exit(1)

# Add project to path
project_path = os.path.expanduser('~/ai-revenue-machine')
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Import tracks
try:
    from track1_content.content_generator import AIContentGenerator
    from track1_content.publisher import DevToPublisher
    from track2_telegram.bot_affiliate import AffiliateBot
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Imports successful")
except Exception as e:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✗ Import error: {e}")
    sys.exit(1)

def run_track_1_job():
    """Run content generation (called by scheduled task)"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] === TRACK 1: Content Generation ===")
    try:
        generator = AIContentGenerator(config.get('openai_api_key'))
        articles = generator.generate_articles(count=3)
        
        publisher = DevToPublisher(config.get('devto_api_key'))
        for article in articles:
            result = publisher.publish(article)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Published: {article['title']}")
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Track 1 completed")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✗ Track 1 error: {e}")

def run_track_2_job():
    """Run Telegram bot (continuous)"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] === TRACK 2: Telegram Bot ===")
    try:
        bot = AffiliateBot(config.get('telegram_bot_token'))
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Bot started")
        bot.run()
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✗ Track 2 error: {e}")

if __name__ == "__main__":
    # For testing - run content generation
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Revenue Orchestrator initialized (PYTHONANYWHERE MODE)")
    run_track_1_job()
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Job completed")
