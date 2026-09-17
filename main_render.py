"""
RENDER.COM DEPLOYMENT ENTRY POINT
Adapted version of main.py that reads config from environment variables
"""

import schedule
import time
import json
import os
import sys
import threading
from datetime import datetime
from shared.utils import log_event

class RevenueOrchestrator:
    def __init__(self):
        self.config = self._load_master_config()
        self.daily_stats = {}
        log_event("🚀 Revenue Orchestrator initialized (RENDER MODE)")

    def _load_master_config(self) -> dict:
        """Load configuration from environment or file"""
        config = {
            "track1_enabled": os.getenv("TRACK1_ENABLED", "true").lower() == "true",
            "track2_enabled": os.getenv("TRACK2_ENABLED", "true").lower() == "true",
            "track3_enabled": False,
            "content_per_day": int(os.getenv("CONTENT_PER_DAY", "3")),
            "publish_platforms": ["devto"],
            "log_file": "automation.log",
        }
        
        # API Keys from environment
        config["openai_api_key"] = os.getenv("OPENAI_API_KEY")
        config["devto_api_key"] = os.getenv("DEVTO_API_KEY")
        config["telegram_bot_token"] = os.getenv("TELEGRAM_BOT_TOKEN")
        
        if not all([config["openai_api_key"], config["devto_api_key"], config["telegram_bot_token"]]):
            log_event("⚠️ WARNING: Some API keys not found in environment variables!")
        
        return config

    def run_track1_daily(self):
        """TRACK 1: Generate and publish content"""
        if not self.config["track1_enabled"]:
            log_event("⊘ TRACK 1 disabled")
            return
            
        log_event("📰 TRACK 1: Starting content generation...")
        try:
            from track1_content.content_generator import ContentGenerator
            gen = ContentGenerator()
            articles = gen.batch_generate_articles(count_per_niche=1)
            gen.export_articles()
            log_event(f"✓ TRACK 1: {len(articles)} articles generated & published")
            self.daily_stats["track1_articles"] = len(articles)
        except Exception as e:
            log_event(f"✗ TRACK 1 Error: {e}")

    def run_track2_bot(self):
        """TRACK 2: Start Telegram bot (runs in background)"""
        if not self.config["track2_enabled"]:
            log_event("⊘ TRACK 2 disabled")
            return
            
        log_event("🤖 TRACK 2: Starting Telegram bot...")
        try:
            from track2_telegram.bot_affiliate import AffiliateBot
            
            token = self.config.get("telegram_bot_token")
            if not token:
                log_event("✗ TRACK 2 Error: No Telegram token provided")
                return
            
            bot = AffiliateBot(token)
            
            # Run bot in separate thread
            bot_thread = threading.Thread(target=bot.run, daemon=True)
            bot_thread.start()
            log_event("✓ TRACK 2: Bot started (background thread)")
            
        except Exception as e:
            log_event(f"✗ TRACK 2 Error: {e}")

    def schedule_tasks(self):
        """Schedule daily content generation"""
        log_event("📅 Scheduling tasks...")
        
        # Generate content at 8 AM UTC
        schedule.every().day.at("08:00").do(self.run_track1_daily)
        log_event("✓ Content generation scheduled for 08:00 UTC")
        
        # Log stats every 6 hours
        schedule.every(6).hours.do(self._log_stats)
        
    def _log_stats(self):
        """Log daily statistics"""
        log_event(f"📊 Daily Stats: {self.daily_stats}")

    def run_scheduler(self):
        """Run scheduler in background"""
        log_event("⏰ Scheduler started")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def run(self):
        """Main execution"""
        try:
            # Start Track 2 Bot immediately (listens 24/7)
            if self.config["track2_enabled"]:
                self.run_track2_bot()
                time.sleep(2)  # Give bot time to initialize
            
            # Schedule Track 1 content generation
            self.schedule_tasks()
            
            # Run scheduler
            self.run_scheduler()
            
        except KeyboardInterrupt:
            log_event("🛑 Orchestrator stopped by user")
        except Exception as e:
            log_event(f"🔥 FATAL ERROR: {e}")
            sys.exit(1)

if __name__ == "__main__":
    orchestrator = RevenueOrchestrator()
    orchestrator.run()
