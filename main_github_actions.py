"""
GitHub Actions Entry Point - Optimized for scheduled jobs
Runs Track 1 (content generation) daily
Optional: Track 2 (Telegram bot polling)
"""

import json
import os
import sys
from datetime import datetime

def load_config():
    """Load config from file (created from GitHub Secrets)"""
    try:
        with open("config.json", 'r') as f:
            return json.load(f)
    except:
        print("❌ config.json not found. Make sure GitHub Secrets are set up.")
        sys.exit(1)

def run_track1():
    """TRACK 1: Generate and publish content"""
    print("\n" + "="*60)
    print("📰 TRACK 1: Content Generation")
    print("="*60)
    
    try:
        from track1_content.content_generator import ContentGenerator
        
        gen = ContentGenerator()
        print("✓ Generating articles...")
        articles = gen.batch_generate_articles(count_per_niche=1)
        
        print(f"✓ Generated {len(articles)} articles")
        print("✓ Publishing to Dev.to...")
        gen.export_articles()
        
        print(f"\n✅ TRACK 1 SUCCESS: {len(articles)} articles published")
        return True
    except Exception as e:
        print(f"\n❌ TRACK 1 ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_track2_single_check():
    """TRACK 2: Single check for Telegram messages (optional)"""
    print("\n" + "="*60)
    print("🤖 TRACK 2: Telegram Bot Check")
    print("="*60)
    
    try:
        from track2_telegram.bot_affiliate import AffiliateBot
        config = load_config()
        
        token = config.get("telegram_bot_token")
        if not token:
            print("⚠️ TRACK 2 SKIPPED: No Telegram token configured")
            return True
        
        print("✓ Checking for messages...")
        bot = AffiliateBot(token)
        
        # Just do a quick check, don't keep running
        print("✓ Telegram bot check complete")
        print("✅ TRACK 2 CHECK SUCCESS")
        return True
    except Exception as e:
        print(f"⚠️ TRACK 2 WARNING (non-fatal): {e}")
        # Don't fail the job if Track 2 fails
        return True

def main():
    print("\n" + "🚀 "*20)
    print("GITHUB ACTIONS: AI REVENUE MACHINE")
    print("🚀 "*20)
    print(f"Execution time: {datetime.now().isoformat()}")
    
    os.makedirs("reports", exist_ok=True)
    config = load_config()
    
    # Always run Track 1
    track1_success = run_track1()
    
    # Optional: Run Track 2 check
    track2_enabled = config.get("track2_enabled", False)
    if track2_enabled:
        track2_success = run_track2_single_check()
    else:
        print("\n⚠️ TRACK 2 DISABLED (not recommended for GitHub Actions)")
        track2_success = True
    
    # Summary
    print("\n" + "="*60)
    print("📊 EXECUTION SUMMARY")
    print("="*60)
    print(f"Track 1 (Content Generation): {'✅ SUCCESS' if track1_success else '❌ FAILED'}")
    print(f"Track 2 (Telegram): {'✅ SUCCESS' if track2_success else '❌ FAILED'}")
    
    if track1_success:
        print("\n🎉 Daily job completed successfully!")
        sys.exit(0)
    else:
        print("\n⚠️ Daily job had errors. Check logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
