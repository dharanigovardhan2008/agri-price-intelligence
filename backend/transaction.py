from models.transaction import Transaction
from services.firebase_service import firebase_service

class TransactionManager:
    """Manage transactions"""
    
    def __init__(self):
        self.db = firebase_service
    
    def create_transaction(self, user_id, commodity, quantity, cost_per_quintal, recommendation):
        """Create new transaction"""
        transaction = Transaction(
            user_id=user_id,
            commodity=commodity,
            quantity=quantity,
            cost_per_quintal=cost_per_quintal,
            recommendation=recommendation
        )
        
        return self.db.create_transaction(transaction.to_dict())
    
    def get_user_transactions(self, user_id, limit=10):
        """Get user's transaction history"""
        transactions_data = self.db.get_user_transactions(user_id, limit)
        return [Transaction.from_dict(t) for t in transactions_data]
    
    def update_status(self, transaction_id, status):
        """Update transaction status"""
        return self.db.update_transaction_status(transaction_id, status)

# Create instance
transaction_manager = TransactionManager()