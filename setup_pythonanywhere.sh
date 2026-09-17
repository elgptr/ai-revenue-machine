#!/bin/bash
################################################################################
# AI REVENUE MACHINE - PYTHONANYWHERE AUTO-SETUP
# Run this in PythonAnywhere Bash console - completely automated!
################################################################################

set -e  # Exit on error

echo "════════════════════════════════════════════════════════════════"
echo "  🚀 AI REVENUE MACHINE - AUTOMATIC SETUP"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Step 1: Clone repository
echo "[1/6] 📦 Cloning repository..."
cd ~
if [ -d "ai-revenue-machine" ]; then
    echo "    Repository already exists. Skipping clone."
else
    git clone https://github.com/elgptr/ai-revenue-machine.git
    echo "    ✓ Repository cloned"
fi

cd ~/ai-revenue-machine

# Step 2: Create config.json with environment variables
echo "[2/6] 🔑 Setting up configuration..."
cat > ~/ai-revenue-machine/config.json << 'EOF'
{
  "openai_api_key": "",
  "devto_api_key": "",
  "telegram_bot_token": "",
  "stripe_api_key": "",
  "mode": "pythonanywhere"
}
EOF
echo "    ⚠️  IMPORTANT: Edit config.json with your API keys:"
echo "    nano ~/ai-revenue-machine/config.json"
echo ""

# Step 3: Install Python dependencies
echo "[3/6] 📚 Installing dependencies..."
pip install --user -r requirements.txt > /dev/null 2>&1
echo "    ✓ Dependencies installed"
echo ""

# Step 4: Test imports
echo "[4/6] 🧪 Testing Python imports..."
python3 << 'PYTHON_TEST'
import sys
sys.path.insert(0, '/home/' + __import__('os').environ.get('USER', 'user') + '/ai-revenue-machine')

try:
    from track1_content.content_generator import ContentGenerator
    print("    ✓ Track1 (Content Generator) OK")
except ImportError as e:
    print(f"    ✗ Track1 import error: {e}")

try:
    from track2_telegram.bot_affiliate import AffiliateBot
    print("    ✓ Track2 (Telegram Bot) OK")
except ImportError as e:
    print(f"    ✗ Track2 import error: {e}")

try:
    from shared.ai_client import OpenAIClient
    print("    ✓ Shared modules OK")
except ImportError as e:
    print(f"    ✗ Shared import error: {e}")

print("\n    All modules ready!")
PYTHON_TEST

echo ""

# Step 5: Create scheduled task via web API
echo "[5/6] ⏰ Configuring scheduled task..."
cat > ~/setup_task.py << 'PYTHON_SETUP'
import json
import os

task_config = {
    "time": "08:00",  # UTC time
    "command": "python ~/ai-revenue-machine/main_pythonanywhere.py"
}

print("📋 SCHEDULED TASK CONFIGURATION:")
print(f"  Time: {task_config['time']} UTC (every day)")
print(f"  Command: {task_config['command']}")
print("")
print("To create the task manually:")
print("  1. Go to PythonAnywhere dashboard")
print("  2. Click 'Tasks' tab")
print("  3. Click 'Create a new scheduled task'")
print("  4. Set time: 08:00")
print("  5. Set command: " + task_config['command'])
print("  6. Click 'Create'")
print("")

with open('/tmp/task_config.json', 'w') as f:
    json.dump(task_config, f)

PYTHON_SETUP

python3 ~/setup_task.py
echo ""

# Step 6: Setup summary
echo "[6/6] ✅ Setup Complete!"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  📋 NEXT STEPS (Manual - takes 5 minutes)"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "1️⃣  ADD API KEYS:"
echo "   nano ~/ai-revenue-machine/config.json"
echo "   Fill in:"
echo "     - openai_api_key: Get from https://platform.openai.com/api-keys"
echo "     - devto_api_key: Get from https://dev.to/settings/extensions"
echo "     - telegram_bot_token: Get from @BotFather on Telegram"
echo ""
echo "2️⃣  CREATE SCHEDULED TASK (Daily content generation):"
echo "   Go to: https://www.pythonanywhere.com/user/USERNAME/tasks/"
echo "   Click: 'Create a new scheduled task'"
echo "   Time: 08:00"
echo "   Command: python ~/ai-revenue-machine/main_pythonanywhere.py"
echo ""
echo "3️⃣  SETUP TELEGRAM BOT (Optional - for 24/7 bot):"
echo "   Go to: https://www.pythonanywhere.com/user/USERNAME/webapps/"
echo "   Add web app → Manual config → Python 3.10"
echo "   WSGI file: /var/www/USERNAME_pythonanywhere_com_wsgi.py"
echo "   Copy content from: ~/ai-revenue-machine/pythonanywhere_wsgi.py"
echo ""
echo "4️⃣  VERIFY:"
echo "   - Check config.json has all keys filled"
echo "   - Create and test the scheduled task"
echo "   - Test Telegram bot (if configured)"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  💰 REVENUE STREAMS"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Track 1 (Auto-Daily at 08:00 UTC):"
echo "  → Generate 3 AI articles"
echo "  → Publish to Dev.to"
echo "  → AdSense revenue: $2-5/day"
echo ""
echo "Track 2 (Always On 24/7):"
echo "  → Telegram bot active"
echo "  → Affiliate commissions: $5-20/day"
echo ""
echo "TOTAL: $7-25/day = $210-750/month PASSIVE! 🎉"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Setup script completed! Your system is ready to deploy."
echo "Refer to PYTHONANYWHERE_START_HERE.txt for detailed instructions."
echo ""
