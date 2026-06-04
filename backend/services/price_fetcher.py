from api.agmarknet import agmarknet_api
from api.data_gov import data_gov_api
from services.firebase_service import firebase_service

class PriceFetcher:
    """Fetch and save prices"""
    
    def __init__(self):
        self.agmarknet = agmarknet_api
        self.data_gov = data_gov_api
    
    def fetch_current_prices(self, commodity=None, state=None):
        """Fetch current prices"""
        return self.agmarknet.fetch_prices(commodity, state)
    
    def fetch_and_save(self, commodities, states):
        """Fetch and save to Firebase"""
        all_prices = []
        
        for commodity in commodities:
            for state in states:
                prices = self.fetch_current_prices(commodity, state)
                all_prices.extend(prices)
        
        if all_prices:
            return firebase_service.save_prices(all_prices)
        
        return {'success': False, 'error': 'No prices fetched'}
    
    def get_historical(self, commodity, market, days=30):
        """Get historical prices"""
        # Try Firebase first
        historical = firebase_service.get_historical_prices(commodity, market, days)
        
        # Fallback to API
        if not historical:
            historical = self.agmarknet.get_historical_prices(commodity, market, days)
        
        return historical

# Create instance
price_fetcher = PriceFetcher()