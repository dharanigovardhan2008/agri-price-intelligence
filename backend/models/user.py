from datetime import datetime

class User:
    """User model"""
    
    def __init__(self, user_id=None, name=None, phone=None, telegram_id=None,
                 state=None, district=None, language='en', **kwargs):
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.telegram_id = telegram_id
        self.state = state
        self.district = district
        self.language = language
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'userId': self.user_id,
            'name': self.name,
            'phone': self.phone,
            'telegramId': self.telegram_id,
            'location': {
                'state': self.state,
                'district': self.district
            },
            'language': self.language,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        """Create from dictionary"""
        location = data.get('location', {})
        return User(
            user_id=data.get('userId'),
            name=data.get('name'),
            phone=data.get('phone'),
            telegram_id=data.get('telegramId'),
            state=location.get('state'),
            district=location.get('district'),
            language=data.get('language', 'en'),
            created_at=data.get('createdAt'),
            updated_at=data.get('updatedAt')
        )
    
    def validate(self):
        """Validate user data"""
        errors = []
        
        if not self.name:
            errors.append("Name is required")
        
        if not self.state:
            errors.append("State is required")
        
        if not self.district:
            errors.append("District is required")
        
        return len(errors) == 0, errors