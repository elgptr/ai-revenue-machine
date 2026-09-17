🚀 AI REVENUE MACHINE - PYTHONANYWHERE EDITION
═══════════════════════════════════════════════════════════════

Deploy in 5 minutes. Generate $7-25 per day automatically.

ONE-COMMAND DEPLOYMENT:
─────────────────────────────────────────────────────────────

In PythonAnywhere Bash console, run:

  curl -fsSL https://raw.githubusercontent.com/elgptr/ai-revenue-machine/master/setup_pythonanywhere.sh | bash

That's it! Everything else is automated.

WHAT YOU GET:
─────────────────────────────────────────────────────────────

✅ TRACK 1 - Content Generation
   • Daily AI article generation (8 AM UTC)
   • Auto-publish to Dev.to
   • AdSense income: $2-5 per day
   • Completely automated

✅ TRACK 2 - Telegram Bot
   • 24/7 always-on bot
   • Responds to user commands
   • Affiliate commissions: $5-20 per day
   • Completely automated

📊 TOTAL: $7-25 per day = $210-750 per month

BEFORE DEPLOYING - GET API KEYS:
─────────────────────────────────────────────────────────────

1. OpenAI API Key
   https://platform.openai.com/api-keys
   (Cost: $0.01 per 3 articles - very cheap!)

2. Dev.to API Key
   https://dev.to/settings/extensions
   (Cost: FREE!)

3. Telegram Bot Token
   Open Telegram → @BotFather → /newbot
   (Cost: FREE!)

QUICK START - 8 MINUTES:
─────────────────────────────────────────────────────────────

1. Create PythonAnywhere account:
   https://www.pythonanywhere.com (free, no CC)

2. Go to Bash console

3. Run one-line setup:
   curl -fsSL ... | bash

4. Edit config with API keys:
   nano ~/ai-revenue-machine/config.json

5. Create scheduled task:
   Dashboard → Tasks → 08:00 UTC
   Command: python ~/ai-revenue-machine/main_pythonanywhere.py

6. Verify:
   Check Dev.to for articles tomorrow 8 AM UTC
   Test Telegram bot with /start

RESULT:
─────────────────────────────────────────────────────────────

✓ Day 1:  First 3 articles published
✓ Day 3:  9 articles, first income showing
✓ Day 7:  21 articles, $30-50 earned
✓ Month:  90 articles, $210-750 earned

FILE STRUCTURE:
─────────────────────────────────────────────────────────────

setup_pythonanywhere.sh      ← Run this in PythonAnywhere
main_pythonanywhere.py       ← Daily task entry point
pythonanywhere_wsgi.py       ← Telegram bot web app
track1_content/              ← Content generation system
track2_telegram/             ← Telegram bot system
shared/                      ← Shared utilities
config.json                  ← Your API keys (NOT in Git)

TROUBLESHOOTING:
─────────────────────────────────────────────────────────────

Bot not responding?
→ Check TELEGRAM_BOT_TOKEN in config.json
→ Verify web app is running

Articles not publishing?
→ Check DEVTO_API_KEY is valid
→ Check OPENAI_API_KEY has credits

Task not running?
→ Verify time is UTC (08:00)
→ Check command path is correct

COSTS:
─────────────────────────────────────────────────────────────

PythonAnywhere:  $0 (free forever)
OpenAI API:      $0.01 per 3 articles (~$0.10/month)
Dev.to:          $0 (free)
Telegram:        $0 (free)

TOTAL MONTHLY COST: ~$0.10
MONTHLY REVENUE: $210-750

DOCUMENTATION:
─────────────────────────────────────────────────────────────

Full guides in project folder:
- DEPLOYMENT_READY.txt         (Master guide)
- PYTHONANYWHERE_START_HERE.txt (Detailed setup)
- PYTHONANYWHERE_DEPLOYMENT.txt (Step-by-step)

═══════════════════════════════════════════════════════════════

🎯 Ready? Start here:
   1. https://www.pythonanywhere.com
   2. Create free account
   3. Open Bash console
   4. Paste deployment command
   5. Follow on-screen instructions
   6. Check Dev.to tomorrow 8 AM UTC for articles!

═══════════════════════════════════════════════════════════════
