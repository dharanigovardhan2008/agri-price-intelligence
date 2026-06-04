import sys
sys.path.append('..')

from backend.services.firebase_service import firebase_service
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"

def send_daily_digest():
    """Send daily price digest to subscribed users"""
    try:
        logger.info("📰 Sending daily price digest...")
        
        # Get all users (in production, only get subscribed users)
        # For now, this is a placeholder
        
        logger.info("✅ Daily digest sent")
        
    except Exception as e:
        logger.error(f"❌ Error sending digest: {e}")

def send_telegram_message(telegram_id, message):
    """Send message via Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        data = {
            'chat_id': telegram_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, json=data)
        return response.status_code == 200
        
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return False

if __name__ == '__main__':
    send_daily_digest()