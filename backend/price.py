from models.price import Price
from services.firebase_service import firebase_service
from api.agmarknet import agmarknet_api

class PriceManager:
    """Manage prices"""
    
    def __init__(self):
        self.db = firebase_service
        self.api = agmarknet_api
    
    def get_current_prices(self, commodity, state):
        """Get current prices"""
        # Try database first
        db_prices = self.db.get_prices_by_state(commodity, state, days=1)
        
        if db_prices:
            return [Price.from_dict(p) for p in db_prices]
        
        # Fetch from API
        api_prices = self.api.fetch_prices(commodity, state)
        return [Price(**p) for p in api_prices]
    
    def save_prices(self, prices_list):
        """Save prices to database"""
        price_dicts = [p.to_dict() if isinstance(p, Price) else p for p in prices_list]
        return self.db.save_prices(price_dicts)

# Create instance
price_manager = PriceManager()