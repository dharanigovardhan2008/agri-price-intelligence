import requests
from datetime import datetime, timedelta
import json

class AgmarknetService:
    """
    Service to fetch commodity prices from Agmarknet API
    Note: Using mock data as Agmarknet API requires authentication
    In production, replace with actual API calls
    """
    
    BASE_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    
    def __init__(self):
        self.api_key = None  # Set your API key here
    
    def fetch_commodity_prices(self, commodity=None, state=None, market=None):
        """
        Fetch commodity prices from Agmarknet
        Using mock data for demonstration
        """
        # Mock data - Replace with actual API call
        mock_markets = [
            {
                'commodity': 'Wheat',
                'market': 'Khanna',
                'state': 'Punjab',
                'district': 'Ludhiana',
                'price': 2180,
                'unit': 'quintal',
                'arrival': 150,
                'date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'commodity': 'Wheat',
                'market': 'Ludhiana',
                'state': 'Punjab',
                'district': 'Ludhiana',
                'price': 2150,
                'unit': 'quintal',
                'arrival': 200,
                'date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'commodity': 'Wheat',
                'market': 'Jalandhar',
                'state': 'Punjab',
                'district': 'Jalandhar',
                'price': 2120,
                'unit': 'quintal',
                'arrival': 120,
                'date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'commodity': 'Rice',
                'market': 'Khanna',
                'state': 'Punjab',
                'district': 'Ludhiana',
                'price': 3200,
                'unit': 'quintal',
                'arrival': 100,
                'date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'commodity': 'Maize',
                'market': 'Khanna',
                'state': 'Punjab',
                'district': 'Ludhiana',
                'price': 1890,
                'unit': 'quintal',
                'arrival': 80,
                'date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'commodity': 'Cotton',
                'market': 'Bathinda',
                'state': 'Punjab',
                'district': 'Bathinda',
                'price': 5800,
                'unit': 'quintal',
                'arrival': 50,
                'date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'commodity': 'Potato',
                'market': 'Jalandhar',
                'state': 'Punjab',
                'district': 'Jalandhar',
                'price': 1200,
                'unit': 'quintal',
                'arrival': 300,
                'date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'commodity': 'Onion',
                'market': 'Ludhiana',
                'state': 'Punjab',
                'district': 'Ludhiana',
                'price': 2500,
                'unit': 'quintal',
                'arrival': 150,
                'date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'commodity': 'Tomato',
                'market': 'Khanna',
                'state': 'Punjab',
                'district': 'Ludhiana',
                'price': 1800,
                'unit': 'quintal',
                'arrival': 200,
                'date': datetime.now().strftime('%Y-%m-%d')
            },
        ]
        
        # Filter based on parameters
        results = mock_markets
        
        if commodity:
            results = [m for m in results if m['commodity'].lower() == commodity.lower()]
        if state:
            results = [m for m in results if m['state'].lower() == state.lower()]
        if market:
            results = [m for m in results if m['market'].lower() == market.lower()]
        
        return results
    
    def fetch_historical_prices(self, commodity, market, days=30):
        """
        Fetch historical prices for trend analysis
        Using mock data - replace with actual API
        """
        # Generate mock historical data
        base_price = 2100
        historical_data = []
        
        for i in range(days, 0, -1):
            date = datetime.now() - timedelta(days=i)
            # Add some variation to simulate real price changes
            import random
            variation = random.randint(-50, 80)
            price = base_price + variation
            
            historical_data.append({
                'commodity': commodity,
                'market': market,
                'price': price,
                'date': date.strftime('%Y-%m-%d'),
                'arrival': random.randint(80, 200)
            })
            
            # Gradually increase base price to show trend
            base_price += random.randint(-10, 15)
        
        return historical_data
    
    def get_markets_by_state(self, state):
        """Get all markets in a state"""
        # Mock market data
        markets = {
            'Punjab': [
                {'name': 'Khanna', 'district': 'Ludhiana', 'lat': 30.7051, 'lng': 76.2220},
                {'name': 'Ludhiana', 'district': 'Ludhiana', 'lat': 30.9010, 'lng': 75.8573},
                {'name': 'Jalandhar', 'district': 'Jalandhar', 'lat': 31.3260, 'lng': 75.5762},
                {'name': 'Amritsar', 'district': 'Amritsar', 'lat': 31.6340, 'lng': 74.8723},
                {'name': 'Bathinda', 'district': 'Bathinda', 'lat': 30.2110, 'lng': 74.9455},
                {'name': 'Patiala', 'district': 'Patiala', 'lat': 30.3398, 'lng': 76.3869},
            ],
            'Haryana': [
                {'name': 'Karnal', 'district': 'Karnal', 'lat': 29.6857, 'lng': 76.9905},
                {'name': 'Panipat', 'district': 'Panipat', 'lat': 29.3909, 'lng': 76.9635},
                {'name': 'Hisar', 'district': 'Hisar', 'lat': 29.1492, 'lng': 75.7217},
            ],
            'Uttar Pradesh': [
                {'name': 'Meerut', 'district': 'Meerut', 'lat': 28.9845, 'lng': 77.7064},
                {'name': 'Agra', 'district': 'Agra', 'lat': 27.1767, 'lng': 78.0081},
                {'name': 'Lucknow', 'district': 'Lucknow', 'lat': 26.8467, 'lng': 80.9462},
            ]
        }
        
        return markets.get(state, [])
    
    def get_all_commodities(self):
        """Get list of all commodities"""
        from config import Config
        return Config.POPULAR_COMMODITIES

# Create instance
agmarknet_service = AgmarknetService()