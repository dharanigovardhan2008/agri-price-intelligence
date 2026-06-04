import requests
from datetime import datetime, timedelta
import random

class AgmarknetAPI:
    """Agmarknet API handler"""
    
    BASE_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    
    def __init__(self):
        self.api_key = None
    
    def fetch_prices(self, commodity=None, state=None, market=None):
        """Fetch commodity prices"""
        # Mock data for demonstration
        mock_markets = [
            # Punjab Markets
            {'commodity': 'Wheat', 'market': 'Khanna', 'state': 'Punjab', 'district': 'Ludhiana', 
             'price': 2180, 'unit': 'quintal', 'arrival': 150, 'date': datetime.now().strftime('%Y-%m-%d')},
            {'commodity': 'Wheat', 'market': 'Ludhiana', 'state': 'Punjab', 'district': 'Ludhiana', 
             'price': 2150, 'unit': 'quintal', 'arrival': 200, 'date': datetime.now().strftime('%Y-%m-%d')},
            {'commodity': 'Wheat', 'market': 'Jalandhar', 'state': 'Punjab', 'district': 'Jalandhar', 
             'price': 2120, 'unit': 'quintal', 'arrival': 120, 'date': datetime.now().strftime('%Y-%m-%d')},
            {'commodity': 'Rice', 'market': 'Khanna', 'state': 'Punjab', 'district': 'Ludhiana', 
             'price': 3200, 'unit': 'quintal', 'arrival': 100, 'date': datetime.now().strftime('%Y-%m-%d')},
            {'commodity': 'Maize', 'market': 'Khanna', 'state': 'Punjab', 'district': 'Ludhiana', 
             'price': 1890, 'unit': 'quintal', 'arrival': 80, 'date': datetime.now().strftime('%Y-%m-%d')},
            {'commodity': 'Cotton', 'market': 'Bathinda', 'state': 'Punjab', 'district': 'Bathinda', 
             'price': 5800, 'unit': 'quintal', 'arrival': 50, 'date': datetime.now().strftime('%Y-%m-%d')},
            {'commodity': 'Potato', 'market': 'Jalandhar', 'state': 'Punjab', 'district': 'Jalandhar', 
             'price': 1200, 'unit': 'quintal', 'arrival': 300, 'date': datetime.now().strftime('%Y-%m-%d')},
            {'commodity': 'Onion', 'market': 'Ludhiana', 'state': 'Punjab', 'district': 'Ludhiana', 
             'price': 2500, 'unit': 'quintal', 'arrival': 150, 'date': datetime.now().strftime('%Y-%m-%d')},
            
            # Haryana Markets
            {'commodity': 'Wheat', 'market': 'Karnal', 'state': 'Haryana', 'district': 'Karnal', 
             'price': 2160, 'unit': 'quintal', 'arrival': 170, 'date': datetime.now().strftime('%Y-%m-%d')},
            {'commodity': 'Rice', 'market': 'Karnal', 'state': 'Haryana', 'district': 'Karnal', 
             'price': 3180, 'unit': 'quintal', 'arrival': 110, 'date': datetime.now().strftime('%Y-%m-%d')},
        ]
        
        results = mock_markets
        
        if commodity:
            results = [m for m in results if m['commodity'].lower() == commodity.lower()]
        if state:
            results = [m for m in results if m['state'].lower() == state.lower()]
        if market:
            results = [m for m in results if m['market'].lower() == market.lower()]
        
        return results
    
    def get_historical_prices(self, commodity, market, days=30):
        """Get historical prices"""
        base_price = 2100
        historical_data = []
        
        for i in range(days, 0, -1):
            date = datetime.now() - timedelta(days=i)
            variation = random.randint(-50, 80)
            price = base_price + variation
            
            historical_data.append({
                'commodity': commodity,
                'market': market,
                'price': price,
                'date': date.strftime('%Y-%m-%d'),
                'arrival': random.randint(80, 200)
            })
            
            base_price += random.randint(-10, 15)
        
        return historical_data
    
    def get_markets_by_state(self, state):
        """Get all markets in a state"""
        markets = {
            'Punjab': [
                {'name': 'Khanna', 'district': 'Ludhiana', 'lat': 30.7051, 'lng': 76.2220},
                {'name': 'Ludhiana', 'district': 'Ludhiana', 'lat': 30.9010, 'lng': 75.8573},
                {'name': 'Jalandhar', 'district': 'Jalandhar', 'lat': 31.3260, 'lng': 75.5762},
                {'name': 'Amritsar', 'district': 'Amritsar', 'lat': 31.6340, 'lng': 74.8723},
                {'name': 'Bathinda', 'district': 'Bathinda', 'lat': 30.2110, 'lng': 74.9455},
            ],
            'Haryana': [
                {'name': 'Karnal', 'district': 'Karnal', 'lat': 29.6857, 'lng': 76.9905},
                {'name': 'Panipat', 'district': 'Panipat', 'lat': 29.3909, 'lng': 76.9635},
                {'name': 'Hisar', 'district': 'Hisar', 'lat': 29.1492, 'lng': 75.7217},
            ]
        }
        
        return markets.get(state, [])

# Create instance
agmarknet_api = AgmarknetAPI()