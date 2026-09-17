"""
MAIN ORCHESTRATOR - Coordinates 2 revenue tracks (zero-touch)
Track 1: Content generation & publishing
Track 2: Telegram bot for passive income community
"""

import schedule
import time
import json
import os
import threading
from datetime import datetime
from shared.utils import log_event

class RevenueOrchestrator:
    def __init__(self):
        self.config = self._load_master_config()
        self.daily_stats = {}
        log_event("🚀 Revenue Orchestrator initialized")
    
    def _load_master_config(self) -> dict:
        """Load master configuration"""
        try:
            with open("config.json", 'r') as f:
                return json.load(f)
        except:
            return {
                "track1_enabled": True,
                "track2_enabled": True,
                "track3_enabled": False,
            }
    
    def run_track1_daily(self):
        """TRACK 1: Generate and publish content"""
        log_event("📰 TRACK 1: Starting content generation...")
        try:
            from track1_content.content_generator import ContentGenerator
            gen = ContentGenerator()
            articles = gen.batch_generate_articles(count_per_niche=1)
            gen.export_articles()
            log_event(f"✓ TRACK 1: {len(articles)} articles generated & published")
        except Exception as e:
            log_event(f"✗ TRACK 1 Error: {e}")
    
    def run_track2_bot(self):
        """TRACK 2: Start Telegram bot (runs in background)"""
        log_event("🤖 TRACK 2: Starting Telegram bot...")
        try:
            from track2_telegram.bot_affiliate import AffiliateBot
            config = self.config
            token = config.get("telegram_bot_token")
            
            if not token:
                log_event("✗ TRACK 2 Error: No Telegram token found")
                return
            
            bot = AffiliateBot(token)
            log_event("✓ TRACK 2: Bot connected & listening")
            bot.run()
        except Exception as e:
            log_event(f"✗ TRACK 2 Error: {e}")
    
    def schedule_daily_tasks(self):
        """Schedule automation tasks"""
        schedule.every().day.at("08:00").do(self.run_track1_daily)
        log_event("✓ Content generation scheduled daily at 08:00 UTC")
        
        # Run scheduler in background
        def scheduler_thread():
            while True:
                schedule.run_pending()
                time.sleep(60)
        
        t = threading.Thread(target=scheduler_thread, daemon=True)
        t.start()
        log_event("✓ Scheduler running in background")
    
    def start_all(self):
        """Start all revenue tracks"""
        log_event("=" * 50)
        log_event("🚀 PASSIVE INCOME MACHINE STARTING")
        log_event("=" * 50)
        
        self.schedule_daily_tasks()
        
        # Start Track 2 (Telegram Bot) in main thread
        log_event("\n🎯 Starting Track 2: Telegram Bot...")
        self.run_track2_bot()


if __name__ == "__main__":
    os.makedirs("reports", exist_ok=True)
    orchestrator = RevenueOrchestrator()
    orchestrator.start_all()
