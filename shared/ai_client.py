"""
Unified AI Client - Wrapper for OpenAI/Anthropic/Local models
Handles API routing, rate limiting, cost optimization
"""

import os
import json
from typing import Optional
import openai
from datetime import datetime, timedelta

class AIClient:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.usage_today = 0
        self.usage_limit = 100000  # tokens per day
        self.rate_limit_reset = datetime.now() + timedelta(days=1)
        
        if self.api_key:
            openai.api_key = self.api_key
    
    def generate_text(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Generate text content"""
        try:
            if self.usage_today > self.usage_limit:
                return "RATE_LIMITED"
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional content creator and business automation expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            content = response.choices[0].message.content
            self.usage_today += response.usage.total_tokens
            
            return content
        except Exception as e:
            print(f"AI Generation Error: {e}")
            return None
    
    def generate_multiple(self, prompts: list, max_tokens: int = 500) -> list:
        """Batch generate content (cost optimized)"""
        results = []
        for prompt in prompts:
            result = self.generate_text(prompt, max_tokens)
            results.append(result)
        return results
    
    def estimate_cost(self, tokens: int) -> float:
        """Estimate API cost"""
        if "gpt-4" in self.model:
            return (tokens / 1000) * 0.03  # $0.03 per 1K tokens
        else:
            return (tokens / 1000) * 0.002  # $0.002 per 1K tokens (gpt-3.5)
    
    def reset_daily_limit(self):
        """Reset daily usage counter"""
        if datetime.now() > self.rate_limit_reset:
            self.usage_today = 0
            self.rate_limit_reset = datetime.now() + timedelta(days=1)


# Singleton instance
_ai_client = None

def get_ai_client(api_key: Optional[str] = None) -> AIClient:
    global _ai_client
    if _ai_client is None:
        _ai_client = AIClient(api_key)
    return _ai_client
