"""
Shared Utilities - Common functions for all revenue tracks
"""

import json
import os
from datetime import datetime
import hashlib
import random
import string

def load_config(config_path: str) -> dict:
    """Load JSON config file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config not found: {config_path}")
        return {}

def save_config(data: dict, config_path: str):
    """Save JSON config file"""
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=2)

def log_event(message: str, log_file: str = "automation.log"):
    """Log events for monitoring"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + "\n")

def generate_id(prefix: str = "id") -> str:
    """Generate unique ID"""
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random_part}"

def estimate_reading_time(text: str) -> int:
    """Estimate reading time in minutes"""
    word_count = len(text.split())
    return max(1, word_count // 200)

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for file system"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename[:255]  # Max filename length

def batch_process(items: list, batch_size: int = 10):
    """Batch process items"""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def calculate_daily_revenue(track_data: dict) -> dict:
    """Calculate revenue across all tracks"""
    summary = {
        "track1_content": track_data.get("adsense_estimated", 0),
        "track2_telegram": track_data.get("telegram_revenue", 0),
        "track3_products": track_data.get("gumroad_revenue", 0),
        "total": 0
    }
    summary["total"] = sum([v for k, v in summary.items() if k != "total"])
    return summary
