# AI Revenue Machine

Automated 2-track passive income system with AI content generation and Telegram bot.

## Features

- **Track 1:** Daily AI-generated articles published to Dev.to (AdSense revenue)
- **Track 2:** 24/7 Telegram bot for community building (affiliate commissions)
- **Deployment:** Render.com Background Worker for 24/7 operation
- **Revenue:** Expected $150-700/month fully automated

## Quick Start

See `RENDER_DEPLOY.txt` in the original source folder for complete deployment instructions.

## Structure

- `main_render.py` - Render.com entry point
- `main.py` - Local orchestrator
- `track1_content/` - Content generation system
- `track2_telegram/` - Telegram bot system
- `shared/` - Shared utilities
- `requirements.txt` - Python dependencies
- `render.yaml` - Render configuration

## Important

- Never commit `config.json` (contains API keys)
- Use environment variables on Render for API keys
- Select "Background Worker" on Render (not Web Service)

## Deployment

1. Push to GitHub
2. Connect to Render.com
3. Add environment variables
4. Deploy as Background Worker

Ready for 24/7 passive income! 💰
