"""
TRACK 2: Telegram Premium Bot
AI-powered bot with premium subscription features
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from shared.ai_client import get_ai_client
from shared.utils import log_event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, token: str, config_path: str = "track2_telegram/config.json"):
        self.token = token
        self.config = self._load_config(config_path)
        self.ai_client = get_ai_client(self.config.get("openai_api_key"))
        self.users_db = {}  # In production: use database
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
        self.application.add_handler(CommandHandler("subscribe", self.subscribe))
        self.application.add_handler(CommandHandler("status", self.status))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command"""
        user_id = update.effective_user.id
        
        welcome_text = """🤖 **AI Assistant Bot**

I can help you with:
✨ Text generation
🎨 Image creation (premium)
📝 Summarization
💡 Ideas & brainstorming
🔍 Content analysis

**Free:** Limited features
**Premium ($2.99/month):** Unlimited everything

Commands:
/help - Get help
/subscribe - Go premium
/status - Check account
"""
        
        keyboard = [
            [InlineKeyboardButton("Go Premium 💳", callback_data='premium'),
             InlineKeyboardButton("Help ❓", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)
        
        # Track new user
        if user_id not in self.users_db:
            self.users_db[user_id] = {
                "id": user_id,
                "created_at": datetime.now().isoformat(),
                "premium": False,
                "messages": 0
            }
            log_event(f"New user: {user_id}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command"""
        help_text = """📚 **Commands & Features**

**Free tier:**
- 5 messages/day
- Basic text generation
- Limited features

**Premium tier ($2.99/month):**
- Unlimited messages
- Image generation
- Priority support
- Advanced AI models
- Custom models

Type your message to start!
"""
        await update.message.reply_text(help_text, parse_mode="Markdown")
    
    async def subscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Premium subscription"""
        user_id = update.effective_user.id
        
        keyboard = [
            [InlineKeyboardButton("Pay with Stripe 💳", url=f"https://buy.stripe.com/premium?user={user_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = """💳 **Upgrade to Premium**

Only $2.99/month

Benefits:
✅ Unlimited messages
✅ Image generation
✅ Priority support
✅ Advanced models

Click button to subscribe:
"""
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check account status"""
        user_id = update.effective_user.id
        user = self.users_db.get(user_id, {})
        
        status_text = f"""📊 **Your Account**

User ID: `{user_id}`
Plan: {'🌟 Premium' if user.get('premium') else '🆓 Free'}
Messages: {user.get('messages', 0)}
Member since: {user.get('created_at', 'unknown')}
"""
        await update.message.reply_text(status_text, parse_mode="Markdown")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle user messages"""
        user_id = update.effective_user.id
        user_text = update.message.text
        
        # Check if user is premium or within free limit
        user = self.users_db.get(user_id, {})
        if not user.get("premium") and user.get("messages", 0) >= 5:
            await update.message.reply_text(
                "🚫 Free limit reached. Upgrade to premium: /subscribe"
            )
            return
        
        # Generate response
        await update.message.chat.send_action("typing")
        
        response = self.ai_client.generate_text(user_text, max_tokens=500)
        
        if response:
            await update.message.reply_text(response)
            user["messages"] = user.get("messages", 0) + 1
            log_event(f"Message from {user_id}: {len(user_text)} chars")
        else:
            await update.message.reply_text("❌ Error generating response")
    
    def run(self):
        """Start bot"""
        log_event("🤖 Telegram bot starting...")
        self.application.run_polling()


if __name__ == "__main__":
    token = "YOUR_TELEGRAM_BOT_TOKEN"
    bot = TelegramBot(token)
    bot.run()
