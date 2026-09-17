"""
TRACK 1: Auto-Publisher - Part 1
Publishes generated content to Medium, Dev.to, Substack, Blog
"""

import json
import requests
from datetime import datetime
from shared.utils import log_event

class PublisherManager:
    def __init__(self, config_path: str = "track1_content/config.json"):
        self.config = self._load_config(config_path)
        self.platforms = {}
        self._init_platforms()
    
    def _load_config(self, path: str) -> dict:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _init_platforms(self):
        """Initialize platform APIs"""
        if self.config.get("medium_token"):
            self.platforms["medium"] = MediumPublisher(self.config["medium_token"])
        
        if self.config.get("devto_token"):
            self.platforms["devto"] = DevtoPublisher(self.config["devto_token"])
        
        if self.config.get("ghost_url"):
            self.platforms["ghost"] = GhostPublisher(
                self.config["ghost_url"],
                self.config["ghost_token"]
            )
    
    def publish_article(self, article: dict, platforms: list = None) -> dict:
        """Publish article to selected platforms"""
        if not platforms:
            platforms = list(self.platforms.keys())
        
        results = {"article_id": article["id"], "platforms": {}}
        
        for platform in platforms:
            if platform not in self.platforms:
                continue
            
            try:
                publisher = self.platforms[platform]
                result = publisher.publish(article)
                results["platforms"][platform] = {
                    "status": "success",
                    "url": result.get("url"),
                    "id": result.get("id")
                }
                log_event(f"✓ Published to {platform}: {result.get('url')}")
            except Exception as e:
                results["platforms"][platform] = {"status": "error", "error": str(e)}
                log_event(f"✗ Failed to publish to {platform}: {e}")
        
        return results
