from urllib import response

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
                'limit': 200,
            }
            if commodity:
                params['filters[commodity]'] = commodity
            if state:
                params['filters[state]'] = state
            if market:
                params['filters[market]'] = market

            response = requests.get(self.BASE_URL, params=params, timeout=15)
            print(f"API URL: {response.url}")
            print(f"API Status: {response.status_code}")
            print(f"API Response: {response.text[:500]}")   
            data = response.json()

            if data.get('status') == 'ok' and data.get('records'):
                results = []
                for r in data['records']:
                    results.append({
                        'commodity': r.get('commodity', ''),
                        'variety': r.get('variety', ''),
                        'market': r.get('market', ''),
                        'state': r.get('state', ''),
                        'district': r.get('district', ''),
                        'price': float(r.get('modal_price', 0)),
                        'min_price': float(r.get('min_price', 0)),
                        'max_price': float(r.get('max_price', 0)),
                        'unit': 'quintal',
                        'arrival': 0,
                        'date': r.get('arrival_date', '')
                    })
                return results
            else:
                print(f'API returned: {data.get("message", "no records")}')
                return []

        except Exception as e:
            print(f'API Error: {e}')
            return []

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
        try:
            params = {
                'api-key': self.api_key,
                'format': 'json',
                'limit': 100,
                'filters[state]': state
            }
            response = requests.get(self.BASE_URL, params=params, timeout=15)
            print(f"API URL: {response.url}")
            print(f"API Status: {response.status_code}")
            print(f"API Response: {response.text[:500]}")



            data = response.json()
            if data.get('status') == 'ok' and data.get('records'):
                seen = set()
                markets = []
                for r in data['records']:
                    name = r.get('market', '')
                    if name and name not in seen:
                        seen.add(name)
                        markets.append({
                            'name': name,
                            'district': r.get('district', ''),
                        })
                return markets
            return []
        except Exception as e:
            print(f'Markets API Error: {e}')
            return []

agmarknet_api = AgmarknetAPI()
