"""
WSGI app for PythonAnywhere - Telegram Bot Handler
File path: /var/www/[username]_pythonanywhere_com_wsgi.py
"""

import os
import sys
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project to path
project_path = os.path.expanduser('~/ai-revenue-machine')
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Load config
try:
    with open(os.path.join(project_path, 'config.json'), 'r') as f:
        CONFIG = json.load(f)
    logger.info("✓ Config loaded")
except Exception as e:
    logger.error(f"✗ Config error: {e}")
    CONFIG = {}

from track2_telegram.bot_affiliate import AffiliateBot

# Initialize bot
try:
    BOT = AffiliateBot(CONFIG.get('telegram_bot_token'))
    logger.info("✓ Bot initialized")
except Exception as e:
    logger.error(f"✗ Bot init error: {e}")
    BOT = None

def application(environ, start_response):
    """WSGI application for handling Telegram webhooks"""
    
    if environ['REQUEST_METHOD'] == 'GET':
        status = '200 OK'
        response_body = b'AI Revenue Machine Bot Active'
        response_headers = [('Content-Type', 'text/plain'),
                           ('Content-Length', str(len(response_body)))]
        start_response(status, response_headers)
        return [response_body]
    
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            body = environ['wsgi.input'].read(content_length)
            
            if BOT:
                BOT.handle_webhook(body)
            
            status = '200 OK'
            response_body = b'OK'
        except Exception as e:
            logger.error(f"Error handling webhook: {e}")
            status = '500 Internal Server Error'
            response_body = b'Error'
        
        response_headers = [('Content-Type', 'text/plain'),
                           ('Content-Length', str(len(response_body)))]
        start_response(status, response_headers)
        return [response_body]
    
    status = '405 Method Not Allowed'
    response_body = b'Method not allowed'
    response_headers = [('Content-Type', 'text/plain'),
                       ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]
