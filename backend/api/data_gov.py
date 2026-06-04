import requests
from datetime import datetime

class DataGovAPI:
    """Data.gov.in API handler"""
    
    BASE_URL = "https://api.data.gov.in"
    
    def __init__(self, api_key=None):
        self.api_key = api_key
    
    def fetch_data(self, resource_id, filters=None):
        """Fetch data from data.gov.in"""
        try:
            params = {
                'api-key': self.api_key,
                'format': 'json',
                'resource_id': resource_id
            }
            
            if filters:
                params.update(filters)
            
            response = requests.get(
                f"{self.BASE_URL}/resource/{resource_id}",
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

# Create instance
data_gov_api = DataGovAPI()