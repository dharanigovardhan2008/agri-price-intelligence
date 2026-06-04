import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # Firebase
    FIREBASE_CREDENTIALS = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase/firebase-config.json')
    
    # API Keys
    AGMARKNET_API_KEY = os.getenv('AGMARKNET_API_KEY', '')
    DATA_GOV_API_KEY = os.getenv('DATA_GOV_API_KEY', '')
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    
    # Application Settings
    PRICE_UPDATE_INTERVAL = 6  # hours
    PREDICTION_DAYS = 7
    MAX_MARKET_RADIUS = 100  # km
    
    # Transport Cost Calculation (₹ per km per quintal)
    TRANSPORT_COST_PER_KM = 2.5
    MANDI_COMMISSION_PERCENT = 2.0
    LOADING_COST_PER_QUINTAL = 10
    
    # Supported Languages
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'hi': 'हिंदी',
        'pa': 'ਪੰਜਾਬੀ',
        'ta': 'தமிழ்',
        'te': 'తెలుగు'
    }
    
    # Popular Commodities
    POPULAR_COMMODITIES = [
        'Wheat', 'Rice', 'Maize', 'Cotton', 'Bajra',
        'Jowar', 'Potato', 'Onion', 'Tomato', 'Soybean',
        'Groundnut', 'Mustard', 'Sugarcane', 'Chilli', 'Turmeric'
    ]
    
    # Indian States
    STATES = [
        'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
        'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
        'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
        'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
        'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
        'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
    ]