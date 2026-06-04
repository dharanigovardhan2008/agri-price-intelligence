import sys
sys.path.append('../..')
from backend.services.firebase_service import firebase_service

class TelegramFirebaseHelper:
    """Helper for Telegram bot Firebase operations"""
    
    def __init__(self):
        self.db = firebase_service
    
    def get_user_by_telegram(self, telegram_id):
        """Get user by Telegram ID"""
        return self.db.get_user(telegram_id=telegram_id)
    
    def save_user_preference(self, user_id, key, value):
        """Save user preference"""
        return self.db.update_user(user_id, {key: value})
    
    def log_bot_interaction(self, telegram_id, command, data=None):
        """Log bot interaction for analytics"""
        try:
            log_data = {
                'telegramId': telegram_id,
                'command': command,
                'data': data,
                'timestamp': self.db.firestore.SERVER_TIMESTAMP
            }
            self.db.db.collection('bot_logs').add(log_data)
        except Exception as e:
            print(f"Error logging interaction: {e}")

# Create instance
firebase_helper = TelegramFirebaseHelper()