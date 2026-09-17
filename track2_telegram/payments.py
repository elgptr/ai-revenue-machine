"""
TRACK 2: Telegram Bot - Stripe Payment Integration
"""

import json
import stripe
from datetime import datetime, timedelta
from shared.utils import log_event

class StripePaymentHandler:
    def __init__(self, stripe_key: str, config_path: str = "track2_telegram/config.json"):
        stripe.api_key = stripe_key
        self.config = self._load_config(config_path)
        self.subscriptions = {}
    
    def _load_config(self, path: str) -> dict:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def create_subscription(self, user_id: str, email: str) -> dict:
        """Create Stripe subscription"""
        try:
            customer = stripe.Customer.create(
                email=email,
                metadata={"user_id": user_id}
            )
            
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{"price": self.config.get("stripe_price_id")}],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"]
            )
            
            self.subscriptions[user_id] = {
                "stripe_id": subscription.id,
                "customer_id": customer.id,
                "status": "active",
                "created": datetime.now().isoformat()
            }
            
            log_event(f"✓ Subscription created: {user_id}")
            
            return {
                "success": True,
                "subscription_id": subscription.id,
                "client_secret": subscription.latest_invoice.payment_intent.client_secret
            }
        except Exception as e:
            log_event(f"✗ Subscription error: {e}")
            return {"success": False, "error": str(e)}
    
    def verify_subscription(self, user_id: str) -> bool:
        """Check if subscription is active"""
        if user_id not in self.subscriptions:
            return False
        
        sub = self.subscriptions[user_id]
        return sub.get("status") == "active"
    
    def get_revenue_metrics(self) -> dict:
        """Get subscription revenue"""
        active_subs = [s for s in self.subscriptions.values() if s.get("status") == "active"]
        
        return {
            "active_subscriptions": len(active_subs),
            "monthly_revenue": len(active_subs) * 2.99,  # $2.99/month
            "total_customers": len(self.subscriptions)
        }
