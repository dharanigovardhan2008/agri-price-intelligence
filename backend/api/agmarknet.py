import requests
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

load_dotenv()

class AgmarknetAPI:
    BASE_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    
    def __init__(self):
        self.api_key = os.getenv('DATA_GOV_API_KEY', '')
    
    def fetch_prices(self, commodity=None, state=None, market=None):
        try:
            params = {
                'api-key': self.api_key,
                'format': 'json',
                'limit': 100,
            }
            if commodity:
                params['filters[commodity]'] = commodity
            if state:
                params['filters[state]'] = state
            if market:
                params['filters[market]'] = market

            response = requests.get(self.BASE_URL, params=params, timeout=10)
            data = response.json()

            if data.get('status') == 'ok' and data.get('records'):
                results = []
                for r in data['records']:
                    results.append({
                        'commodity': r.get('commodity', ''),
                        'market': r.get('market', ''),
                        'state': r.get('state', ''),
                        'district': r.get('district', ''),
                        'price': float(r.get('modal_price', 0)),
                        'min_price': float(r.get('min_price', 0)),
                        'max_price': float(r.get('max_price', 0)),
                        'unit': 'quintal',
                        'arrival': 0,
                        'date': r.get('arrival_date', datetime.now().strftime('%d/%m/%Y'))
                    })
                return results
            else:
                return self._mock_prices(commodity, state, market)

        except Exception as e:
            print(f'API Error: {e}')
            return self._mock_prices(commodity, state, market)

    def _mock_prices(self, commodity=None, state=None, market=None):
        mock = [
            {'commodity': 'Wheat', 'market': 'Khanna', 'state': 'Punjab', 'district': 'Ludhiana', 'price': 2180, 'unit': 'quintal', 'arrival': 150, 'date': datetime.now().strftime('%Y-%m-%d')},
            {'commodity': 'Wheat', 'market': 'Ludhiana', 'state': 'Punjab', 'district': 'Ludhiana', 'price': 2150, 'unit': 'quintal', 'arrival': 200, 'date': datetime.now().strftime('%Y-%m-%d')},
            {'commodity': 'Rice', 'market': 'Khanna', 'state': 'Punjab', 'district': 'Ludhiana', 'price': 3200, 'unit': 'quintal', 'arrival': 100, 'date': datetime.now().strftime('%Y-%m-%d')},
            {'commodity': 'Onion', 'market': 'Ludhiana', 'state': 'Punjab', 'district': 'Ludhiana', 'price': 2500, 'unit': 'quintal', 'arrival': 150, 'date': datetime.now().strftime('%Y-%m-%d')},
            {'commodity': 'Tomato', 'market': 'Chennai', 'state': 'Tamil Nadu', 'district': 'Chennai', 'price': 2840, 'unit': 'quintal', 'arrival': 120, 'date': datetime.now().strftime('%Y-%m-%d')},
            {'commodity': 'Potato', 'market': 'Jalandhar', 'state': 'Punjab', 'district': 'Jalandhar', 'price': 1200, 'unit': 'quintal', 'arrival': 300, 'date': datetime.now().strftime('%Y-%m-%d')},
            {'commodity': 'Groundnut', 'market': 'Vellore', 'state': 'Tamil Nadu', 'district': 'Vellore', 'price': 5420, 'unit': 'quintal', 'arrival': 80, 'date': datetime.now().strftime('%Y-%m-%d')},
        ]
        results = mock
        if commodity:
            results = [m for m in results if m['commodity'].lower() == commodity.lower()]
        if state:
            results = [m for m in results if m['state'].lower() == state.lower()]
        if market:
            results = [m for m in results if m['market'].lower() == market.lower()]
        return results

    def get_historical_prices(self, commodity, market, days=30):
        base_price = 2100
        historical = []
        for i in range(days, 0, -1):
            date = datetime.now() - timedelta(days=i)
            variation = random.randint(-50, 80)
            price = base_price + variation
            historical.append({
                'commodity': commodity,
                'market': market,
                'price': price,
                'date': date.strftime('%Y-%m-%d'),
                'arrival': random.randint(80, 200)
            })
            base_price += random.randint(-10, 15)
        return historical

    def get_markets_by_state(self, state):
        markets = {
            'Punjab': [
                {'name': 'Khanna', 'district': 'Ludhiana', 'lat': 30.7051, 'lng': 76.2220},
                {'name': 'Ludhiana', 'district': 'Ludhiana', 'lat': 30.9010, 'lng': 75.8573},
                {'name': 'Jalandhar', 'district': 'Jalandhar', 'lat': 31.3260, 'lng': 75.5762},
            ],
            'Tamil Nadu': [
                {'name': 'Chennai APMC', 'district': 'Chennai', 'lat': 13.0827, 'lng': 80.2707},
                {'name': 'Koyambedu', 'district': 'Chennai', 'lat': 13.0732, 'lng': 80.1964},
                {'name': 'Madurai', 'district': 'Madurai', 'lat': 9.9252, 'lng': 78.1198},
            ]
        }
        return markets.get(state, [])

agmarknet_api = AgmarknetAPI()
