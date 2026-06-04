import requests

class WeatherAPI:
    """Weather API for crop predictions"""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self, api_key=None):
        self.api_key = api_key
    
    def get_weather(self, lat, lng):
        """Get current weather"""
        try:
            params = {
                'lat': lat,
                'lon': lng,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(
                f"{self.BASE_URL}/weather",
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except Exception as e:
            print(f"Weather API error: {e}")
            return None
    
    def get_forecast(self, lat, lng, days=7):
        """Get weather forecast"""
        try:
            params = {
                'lat': lat,
                'lon': lng,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8  # 3-hour intervals
            }
            
            response = requests.get(
                f"{self.BASE_URL}/forecast",
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except Exception as e:
            print(f"Forecast API error: {e}")
            return None

# Create instance
weather_api = WeatherAPI()