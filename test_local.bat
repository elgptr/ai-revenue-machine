@echo off
REM ════════════════════════════════════════════════════════════════
REM   AI REVENUE MACHINE - LOCAL TEST SCRIPT (Windows)
REM ════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════════
echo   Testing AI Revenue Machine Locally
echo ════════════════════════════════════════════════════════════════
echo.

REM Check if Python is installed
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo ✗ Python not found! Install Python 3.10+ first.
    exit /b 1
)

echo ✓ Python found
echo.

REM Install dependencies
echo [1/4] Installing dependencies...
pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo ✗ Failed to install dependencies
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Test imports
echo [2/4] Testing imports...
python -c ^
"import sys; ^
sys.path.insert(0, '.'); ^
from track1_content.content_generator import ContentGenerator; ^
from track2_telegram.bot_affiliate import AffiliateBot; ^
from shared.ai_client import OpenAIClient; ^
print('  ✓ All imports successful')" || (
    echo ✗ Import test failed
    exit /b 1
)
echo.

REM Check config.json
echo [3/4] Checking configuration...
if exist "config.json" (
    echo ✓ config.json found
    python -c ^
    "import json; ^
    with open('config.json') as f: ^
        config = json.load(f); ^
    keys = ['openai_api_key', 'devto_api_key', 'telegram_bot_token']; ^
    for key in keys: ^
        if key in config and config[key]: ^
            print(f'  ✓ {key} configured'); ^
        else: ^
            print(f'  ⚠️  {key} is empty')"
) else (
    echo ⚠️  config.json not found - create it before running!
)
echo.

REM Run test task
echo [4/4] Running test content generation...
python main_pythonanywhere.py 2>&1 | head -20
echo.

echo ════════════════════════════════════════════════════════════════
echo ✓ Local test completed!
echo.
echo Next step: Deploy to PythonAnywhere
echo  1. Go: https://www.pythonanywhere.com
echo  2. Create account (free)
echo  3. Run: bash setup_pythonanywhere.sh
echo ════════════════════════════════════════════════════════════════
