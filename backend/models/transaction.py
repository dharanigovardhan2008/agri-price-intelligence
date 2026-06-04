from datetime import datetime

class Transaction:
    """Transaction model"""
    
    def __init__(self, transaction_id=None, user_id=None, commodity=None,
                 quantity=0, cost_per_quintal=0, recommendation=None,
                 status='pending', **kwargs):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.commodity = commodity
        self.quantity = quantity
        self.cost_per_quintal = cost_per_quintal
        self.recommendation = recommendation
        self.status = status
        self.request_date = kwargs.get('request_date', datetime.now())
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'transactionId': self.transaction_id,
            'userId': self.user_id,
            'commodity': self.commodity,
            'quantity': self.quantity,
            'costPerQuintal': self.cost_per_quintal,
            'recommendation': self.recommendation,
            'status': self.status,
            'requestDate': self.request_date
        }
    
    @staticmethod
    def from_dict(data):
        """Create from dictionary"""
        return Transaction(
            transaction_id=data.get('transactionId'),
            user_id=data.get('userId'),
            commodity=data.get('commodity'),
            quantity=data.get('quantity', 0),
            cost_per_quintal=data.get('costPerQuintal', 0),
            recommendation=data.get('recommendation'),
            status=data.get('status', 'pending'),
            request_date=data.get('requestDate')
        )