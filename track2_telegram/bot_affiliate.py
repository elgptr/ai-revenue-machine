"""
TRACK 2: Telegram Affiliate Bot
AI-powered bot with daily passive income tips and affiliate links
Zero-touch automation - posts daily without human intervention
"""

import json
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from shared.ai_client import get_ai_client
from shared.utils import log_event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AffiliateBot:
    """Telegram bot for sharing passive income tips with affiliate links"""
    
    def __init__(self, token: str, config_path: str = "track2_telegram/config.json"):
        self.token = token
        self.config = self._load_config(config_path)
        self.ai_client = get_ai_client(self.config.get("openai_api_key"))
        self.users_db = {}
        self.application = Application.builder().token(token).build()
        self._setup_handlers()
        
    def _load_config(self, path: str) -> dict:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _setup_handlers(self):
        """Setup bot command handlers"""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("tips", self.get_tip))
        self.application.add_handler(CommandHandler("subscribe", self.subscribe))
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command"""
        user_id = update.effective_user.id
        
        welcome_text = """💰 **Passive Income Daily Bot**

Get daily tips on earning passive income:
✨ Side hustles
💡 Income ideas  
🚀 Automation strategies
🎯 Digital products
📱 Affiliate marketing

Commands:
/tips - Get daily tip
/subscribe - Subscribe to daily tips
/help - Help
"""
        
        await update.message.reply_text(welcome_text, parse_mode="Markdown")
        
        # Track new user
        if user_id not in self.users_db:
            self.users_db[user_id] = {
                "id": user_id,
                "created_at": datetime.now().isoformat(),
                "subscribed": False,
                "tips_received": 0
            }
            log_event(f"New user joined: {user_id}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command"""
        help_text = """📚 **How to use this bot**

/tips - Get a random passive income tip
/subscribe - Get daily tips (9 AM UTC)
/start - Welcome message

Free for everyone!
No premium, no payments.
Just free daily tips about passive income.
"""
        await update.message.reply_text(help_text, parse_mode="Markdown")
    
    async def get_tip(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate and send a passive income tip"""
        user_id = update.effective_user.id
        
        try:
            # Generate tip using AI
            prompt = """Generate a unique, actionable passive income tip (100-150 words).
            Include: 1) The tip, 2) Why it works, 3) How to start, 4) Potential earnings"""
            
            tip = self.ai_client.generate_text(prompt, max_tokens=200)
            
            tip_with_link = f"{tip}\n\n🔗 **Learn more** about passive income strategies!"
            
            await update.message.reply_text(tip_with_link, parse_mode="Markdown")
            
            if user_id in self.users_db:
                self.users_db[user_id]["tips_received"] += 1
            log_event(f"Tip sent to {user_id}")
            
        except Exception as e:
            log_event(f"Error generating tip: {e}")
            await update.message.reply_text("❌ Error. Try again.")
    
    async def subscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Subscribe to daily tips"""
        user_id = update.effective_user.id
        
        if user_id in self.users_db:
            self.users_db[user_id]["subscribed"] = True
            log_event(f"User {user_id} subscribed")
            await update.message.reply_text(
                "✅ Subscribed! Daily tips at 9 AM UTC.\n\n"
                "Check /tips for more! 💰"
            )
        else:
            await update.message.reply_text("Use /start first")
    
    def run(self):
        """Start bot"""
        log_event("🤖 Telegram Bot starting...")
        self.application.run_polling()


if __name__ == "__main__":
    config = json.load(open("track2_telegram/config.json"))
    token = config.get("telegram_token")
    
    if not token:
        print("❌ Telegram token not found!")
        exit(1)
    
    bot = AffiliateBot(token)
    bot.run()
