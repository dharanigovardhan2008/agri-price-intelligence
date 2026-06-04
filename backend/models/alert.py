from datetime import datetime

class Alert:
    """Alert model"""
    
    def __init__(self, alert_id=None, user_id=None, commodity=None,
                 target_price=0, condition='above', state=None,
                 is_active=True, triggered=False, **kwargs):
        self.alert_id = alert_id
        self.user_id = user_id
        self.commodity = commodity
        self.target_price = target_price
        self.condition = condition
        self.state = state
        self.is_active = is_active
        self.triggered = triggered
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
    
    def to_dict(self):
        return {
            'alertId': self.alert_id,
            'userId': self.user_id,
            'commodity': self.commodity,
            'targetPrice': self.target_price,
            'condition': self.condition,
            'state': self.state,
            'isActive': self.is_active,
            'triggered': self.triggered,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        return Alert(
            alert_id=data.get('alertId'),
            user_id=data.get('userId'),
            commodity=data.get('commodity'),
            target_price=data.get('targetPrice', 0),
            condition=data.get('condition', 'above'),
            state=data.get('state'),
            is_active=data.get('isActive', True),
            triggered=data.get('triggered', False),
            created_at=data.get('createdAt'),
            updated_at=data.get('updatedAt')
        )
    
    def validate(self):
        errors = []
        if not self.commodity:
            errors.append('Commodity is required')
        if not self.target_price:
            errors.append('Target price is required')
        if self.condition not in ['above', 'below']:
            errors.append('Condition must be above or below')
        return len(errors) == 0, errors
