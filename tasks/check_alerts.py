import sys
sys.path.append('..')

from backend.services.firebase_service import firebase_service
from backend.alert import alert_manager
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"

def check_and_send_alerts():
    """Check price alerts and send notifications"""
    try:
        logger.info("🔔 Checking price alerts...")
        
        # Get all active alerts
        alerts = firebase_service.get_all_active_alerts()
        
        if not alerts:
            logger.info("  No active alerts to check")
            return
        
        logger.info(f"  Checking {len(alerts)} alerts")
        
        # Get current prices
        from backend.api.agmarknet import agmarknet_api
        
        triggered_count = 0
        
        for alert in alerts:
            try:
                commodity = alert['commodity']
                target_price = alert['targetPrice']
                alert_type = alert['alertType']
                user_id = alert['userId']
                
                # Get current price
                prices = agmarknet_api.fetch_prices(commodity=commodity)
                
                if not prices:
                    continue
                
                max_price = max(p['price'] for p in prices)
                
                # Check if alert should trigger
                triggered = False
                
                if alert_type == 'price_above' and max_price >= target_price:
                    triggered = True
                elif alert_type == 'price_below' and max_price <= target_price:
                    triggered = True
                
                if triggered:
                    # Get user telegram ID
                    user = firebase_service.get_user(user_id=user_id)
                    
                    if user and user.get('telegramId'):
                        # Send Telegram notification
                        send_telegram_alert(
                            user['telegramId'],
                            commodity,
                            max_price,
                            target_price
                        )
                        
                        # Mark alert as triggered
                        firebase_service.delete_alert(alert['alertId'])
                        
                        triggered_count += 1
                        logger.info(f"  ✓ Alert triggered for {commodity} @ ₹{max_price}")
                        
            except Exception as e:
                logger.error(f"  ✗ Error processing alert: {e}")
        
        logger.info(f"✅ Checked alerts. {triggered_count} triggered.")
        
    except Exception as e:
        logger.error(f"❌ Error in check_alerts: {e}")

def send_telegram_alert(telegram_id, commodity, current_price, target_price):
    """Send alert via Telegram"""
    try:
        message = f"""
🔔 *PRICE ALERT!*

🌾 *{commodity}*
💰 Current Price: ₹{current_price}/quintal
🎯 Your Target: ₹{target_price}/quintal

✅ Your target price has been reached!

Use /sell to analyze if you should sell now.
        """
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        data = {
            'chat_id': telegram_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            logger.info(f"  ✓ Sent alert to user {telegram_id}")
        else:
            logger.error(f"  ✗ Failed to send alert: {response.text}")
            
    except Exception as e:
        logger.error(f"  ✗ Error sending Telegram alert: {e}")

if __name__ == '__main__':
    check_and_send_alerts()