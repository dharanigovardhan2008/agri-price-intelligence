from models.user import User
from services.firebase_service import firebase_service

class UserManager:
    """Manage users"""
    
    def __init__(self):
        self.db = firebase_service
    
    def create_user(self, name, phone, telegram_id, state, district, language='en'):
        """Create new user"""
        user = User(
            name=name,
            phone=phone,
            telegram_id=telegram_id,
            state=state,
            district=district,
            language=language
        )
        
        is_valid, errors = user.validate()
        if not is_valid:
            return {'success': False, 'errors': errors}
        
        return self.db.create_user(user.to_dict())
    
    def get_user(self, user_id=None, telegram_id=None):
        """Get user"""
        user_data = self.db.get_user(user_id, telegram_id)
        return User.from_dict(user_data) if user_data else None
    
    def update_user(self, user_id, updates):
        """Update user"""
        return self.db.update_user(user_id, updates)

# Create instance
user_manager = UserManager()