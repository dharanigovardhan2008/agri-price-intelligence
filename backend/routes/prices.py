from flask import Blueprint, request, jsonify
from services.price_fetcher import price_fetcher
from api.agmarknet import agmarknet_api
from config import Config
from datetime import datetime

prices_bp = Blueprint('prices', __name__)

def get_demo_prices(commodity=None, state=None):
    today = datetime.now().strftime('%d/%m/%Y')
    data = [
        # Tamil Nadu
        {'commodity':'Tomato','variety':'Local','market':'Koyambedu','state':'Tamil Nadu','district':'Chennai','price':2840,'min_price':2600,'max_price':3100,'unit':'quintal','date':today},
        {'commodity':'Tomato','variety':'Hybrid','market':'Coimbatore','state':'Tamil Nadu','district':'Coimbatore','price':2750,'min_price':2500,'max_price':3000,'unit':'quintal','date':today},
        {'commodity':'Tomato','variety':'Local','market':'Madurai','state':'Tamil Nadu','district':'Madurai','price':2650,'min_price':2400,'max_price':2900,'unit':'quintal','date':today},
        {'commodity':'Tomato','variety':'Local','market':'Salem','state':'Tamil Nadu','district':'Salem','price':2600,'min_price':2300,'max_price':2850,'unit':'quintal','date':today},
        {'commodity':'Onion','variety':'Red','market':'Koyambedu','state':'Tamil Nadu','district':'Chennai','price':1560,'min_price':1400,'max_price':1700,'unit':'quintal','date':today},
        {'commodity':'Onion','variety':'Local','market':'Salem','state':'Tamil Nadu','district':'Salem','price':1480,'min_price':1300,'max_price':1650,'unit':'quintal','date':today},
        {'commodity':'Potato','variety':'Red Nanital','market':'Koyambedu','state':'Tamil Nadu','district':'Chennai','price':2700,'min_price':2500,'max_price':2900,'unit':'quintal','date':today},
        {'commodity':'Potato','variety':'Local','market':'Coimbatore','state':'Tamil Nadu','district':'Coimbatore','price':2600,'min_price':2400,'max_price':2800,'unit':'quintal','date':today},
        {'commodity':'Banana','variety':'Besrai','market':'Trichy','state':'Tamil Nadu','district':'Trichy','price':1890,'min_price':1700,'max_price':2100,'unit':'quintal','date':today},
        {'commodity':'Banana','variety':'Nendran','market':'Coimbatore','state':'Tamil Nadu','district':'Coimbatore','price':3200,'min_price':2900,'max_price':3500,'unit':'quintal','date':today},
        {'commodity':'Banana','variety':'Robusta','market':'Madurai','state':'Tamil Nadu','district':'Madurai','price':2100,'min_price':1900,'max_price':2300,'unit':'quintal','date':today},
        {'commodity':'Rice','variety':'Ponni','market':'Thanjavur','state':'Tamil Nadu','district':'Thanjavur','price':3200,'min_price':3000,'max_price':3400,'unit':'quintal','date':today},
        {'commodity':'Rice','variety':'Raw','market':'Tirunelveli','state':'Tamil Nadu','district':'Tirunelveli','price':2980,'min_price':2800,'max_price':3200,'unit':'quintal','date':today},
        {'commodity':'Rice','variety':'Boiled','market':'Trichy','state':'Tamil Nadu','district':'Trichy','price':3100,'min_price':2900,'max_price':3300,'unit':'quintal','date':today},
        {'commodity':'Groundnut','variety':'Local','market':'Vellore','state':'Tamil Nadu','district':'Vellore','price':5420,'min_price':5000,'max_price':5800,'unit':'quintal','date':today},
        {'commodity':'Groundnut','variety':'Bold','market':'Tirunelveli','state':'Tamil Nadu','district':'Tirunelveli','price':5600,'min_price':5200,'max_price':6000,'unit':'quintal','date':today},
        {'commodity':'Turmeric','variety':'Finger','market':'Erode','state':'Tamil Nadu','district':'Erode','price':12000,'min_price':11000,'max_price':13000,'unit':'quintal','date':today},
        {'commodity':'Turmeric','variety':'Bulb','market':'Salem','state':'Tamil Nadu','district':'Salem','price':11000,'min_price':10000,'max_price':12000,'unit':'quintal','date':today},
        {'commodity':'Coconut','variety':'Medium','market':'Pollachi','state':'Tamil Nadu','district':'Coimbatore','price':2200,'min_price':2000,'max_price':2400,'unit':'quintal','date':today},
        {'commodity':'Brinjal','variety':'Local','market':'Koyambedu','state':'Tamil Nadu','district':'Chennai','price':1200,'min_price':1000,'max_price':1400,'unit':'quintal','date':today},
        {'commodity':'Carrot','variety':'Local','market':'Ooty','state':'Tamil Nadu','district':'Nilgiris','price':3500,'min_price':3200,'max_price':3800,'unit':'quintal','date':today},
        {'commodity':'Cabbage','variety':'Local','market':'Mettupalayam','state':'Tamil Nadu','district':'Coimbatore','price':800,'min_price':700,'max_price':950,'unit':'quintal','date':today},
        {'commodity':'Chilli','variety':'Dry','market':'Guntur','state':'Tamil Nadu','district':'Coimbatore','price':8500,'min_price':8000,'max_price':9000,'unit':'quintal','date':today},
        {'commodity':'Sugarcane','variety':'CO 86032','market':'Thanjavur','state':'Tamil Nadu','district':'Thanjavur','price':3200,'min_price':3000,'max_price':3400,'unit':'quintal','date':today},
        {'commodity':'Maize','variety':'Hybrid','market':'Dharmapuri','state':'Tamil Nadu','district':'Dharmapuri','price':1890,'min_price':1750,'max_price':2000,'unit':'quintal','date':today},
        # Punjab
        {'commodity':'Wheat','variety':'Lokwan','market':'Khanna','state':'Punjab','district':'Ludhiana','price':2180,'min_price':2100,'max_price':2250,'unit':'quintal','date':today},
        {'commodity':'Wheat','variety':'PBW 343','market':'Ludhiana','state':'Punjab','district':'Ludhiana','price':2150,'min_price':2050,'max_price':2230,'unit':'quintal','date':today},
        {'commodity':'Wheat','variety':'Local','market':'Jalandhar','state':'Punjab','district':'Jalandhar','price':2120,'min_price':2000,'max_price':2200,'unit':'quintal','date':today},
        {'commodity':'Rice','variety':'Basmati','market':'Amritsar','state':'Punjab','district':'Amritsar','price':4500,'min_price':4200,'max_price':4800,'unit':'quintal','date':today},
        {'commodity':'Rice','variety':'PR 106','market':'Khanna','state':'Punjab','district':'Ludhiana','price':3200,'min_price':3000,'max_price':3400,'unit':'quintal','date':today},
        {'commodity':'Maize','variety':'Local','market':'Khanna','state':'Punjab','district':'Ludhiana','price':1890,'min_price':1750,'max_price':2000,'unit':'quintal','date':today},
        {'commodity':'Cotton','variety':'Long Staple','market':'Bathinda','state':'Punjab','district':'Bathinda','price':5800,'min_price':5500,'max_price':6200,'unit':'quintal','date':today},
        {'commodity':'Potato','variety':'Kufri Jyoti','market':'Jalandhar','state':'Punjab','district':'Jalandhar','price':1200,'min_price':1000,'max_price':1400,'unit':'quintal','date':today},
        {'commodity':'Onion','variety':'Red','market':'Ludhiana','state':'Punjab','district':'Ludhiana','price':2500,'min_price':2200,'max_price':2800,'unit':'quintal','date':today},
        # Maharashtra
        {'commodity':'Onion','variety':'Red','market':'Lasalgaon','state':'Maharashtra','district':'Nashik','price':1800,'min_price':1600,'max_price':2000,'unit':'quintal','date':today},
        {'commodity':'Onion','variety':'White','market':'Nashik','state':'Maharashtra','district':'Nashik','price':1750,'min_price':1550,'max_price':1950,'unit':'quintal','date':today},
        {'commodity':'Tomato','variety':'Local','market':'Pune','state':'Maharashtra','district':'Pune','price':2400,'min_price':2200,'max_price':2600,'unit':'quintal','date':today},
        {'commodity':'Sugarcane','variety':'Co 86032','market':'Kolhapur','state':'Maharashtra','district':'Kolhapur','price':3500,'min_price':3200,'max_price':3800,'unit':'quintal','date':today},
        {'commodity':'Soybean','variety':'Yellow','market':'Latur','state':'Maharashtra','district':'Latur','price':4200,'min_price':3900,'max_price':4500,'unit':'quintal','date':today},
        {'commodity':'Cotton','variety':'Medium Staple','market':'Nagpur','state':'Maharashtra','district':'Nagpur','price':5600,'min_price':5200,'max_price':6000,'unit':'quintal','date':today},
        {'commodity':'Groundnut','variety':'Bold','market':'Akola','state':'Maharashtra','district':'Akola','price':5200,'min_price':4800,'max_price':5600,'unit':'quintal','date':today},
        # Karnataka
        {'commodity':'Tomato','variety':'Hybrid','market':'Bangalore','state':'Karnataka','district':'Bangalore Urban','price':2900,'min_price':2700,'max_price':3100,'unit':'quintal','date':today},
        {'commodity':'Ragi','variety':'Local','market':'Davangere','state':'Karnataka','district':'Davangere','price':2100,'min_price':1900,'max_price':2300,'unit':'quintal','date':today},
        {'commodity':'Maize','variety':'Hybrid','market':'Davangere','state':'Karnataka','district':'Davangere','price':1850,'min_price':1700,'max_price':2000,'unit':'quintal','date':today},
        {'commodity':'Groundnut','variety':'Bold','market':'Raichur','state':'Karnataka','district':'Raichur','price':5100,'min_price':4800,'max_price':5400,'unit':'quintal','date':today},
        {'commodity':'Cotton','variety':'Long Staple','market':'Hubli','state':'Karnataka','district':'Dharwad','price':5700,'min_price':5300,'max_price':6100,'unit':'quintal','date':today},
        {'commodity':'Onion','variety':'Red','market':'Bangalore','state':'Karnataka','district':'Bangalore Urban','price':1650,'min_price':1450,'max_price':1850,'unit':'quintal','date':today},
        # Andhra Pradesh
        {'commodity':'Chilli','variety':'Dry','market':'Guntur','state':'Andhra Pradesh','district':'Guntur','price':8500,'min_price':8000,'max_price':9000,'unit':'quintal','date':today},
        {'commodity':'Chilli','variety':'Green','market':'Warangal','state':'Andhra Pradesh','district':'Warangal','price':3200,'min_price':2900,'max_price':3500,'unit':'quintal','date':today},
        {'commodity':'Rice','variety':'BPT','market':'Vijayawada','state':'Andhra Pradesh','district':'Krishna','price':3400,'min_price':3200,'max_price':3600,'unit':'quintal','date':today},
        {'commodity':'Tomato','variety':'Local','market':'Madanapalle','state':'Andhra Pradesh','district':'Chittoor','price':2100,'min_price':1900,'max_price':2300,'unit':'quintal','date':today},
        {'commodity':'Groundnut','variety':'Bold','market':'Kurnool','state':'Andhra Pradesh','district':'Kurnool','price':5300,'min_price':5000,'max_price':5600,'unit':'quintal','date':today},
        # Kerala
        {'commodity':'Coconut','variety':'Medium','market':'Thrissur','state':'Kerala','district':'Thrissur','price':2800,'min_price':2600,'max_price':3000,'unit':'quintal','date':today},
        {'commodity':'Banana','variety':'Nendran','market':'Kozhikode','state':'Kerala','district':'Kozhikode','price':3500,'min_price':3200,'max_price':3800,'unit':'quintal','date':today},
        {'commodity':'Rubber','variety':'RSS4','market':'Kottayam','state':'Kerala','district':'Kottayam','price':18000,'min_price':17000,'max_price':19000,'unit':'quintal','date':today},
        {'commodity':'Pepper','variety':'Black','market':'Wayanad','state':'Kerala','district':'Wayanad','price':35000,'min_price':33000,'max_price':37000,'unit':'quintal','date':today},
        # Haryana
        {'commodity':'Wheat','variety':'Sharbati','market':'Karnal','state':'Haryana','district':'Karnal','price':2160,'min_price':2050,'max_price':2280,'unit':'quintal','date':today},
        {'commodity':'Rice','variety':'Basmati','market':'Karnal','state':'Haryana','district':'Karnal','price':4200,'min_price':3900,'max_price':4500,'unit':'quintal','date':today},
        {'commodity':'Mustard','variety':'Yellow','market':'Hisar','state':'Haryana','district':'Hisar','price':5100,'min_price':4800,'max_price':5400,'unit':'quintal','date':today},
        {'commodity':'Potato','variety':'Kufri','market':'Panipat','state':'Haryana','district':'Panipat','price':1150,'min_price':1000,'max_price':1300,'unit':'quintal','date':today},
        # Uttar Pradesh
        {'commodity':'Wheat','variety':'Lokwan','market':'Kanpur','state':'Uttar Pradesh','district':'Kanpur','price':2200,'min_price':2100,'max_price':2300,'unit':'quintal','date':today},
        {'commodity':'Potato','variety':'Kufri Jyoti','market':'Agra','state':'Uttar Pradesh','district':'Agra','price':1100,'min_price':950,'max_price':1250,'unit':'quintal','date':today},
        {'commodity':'Sugarcane','variety':'Co 0238','market':'Meerut','state':'Uttar Pradesh','district':'Meerut','price':3600,'min_price':3400,'max_price':3800,'unit':'quintal','date':today},
        {'commodity':'Onion','variety':'Red','market':'Lucknow','state':'Uttar Pradesh','district':'Lucknow','price':1700,'min_price':1500,'max_price':1900,'unit':'quintal','date':today},
        # Rajasthan
        {'commodity':'Mustard','variety':'Yellow','market':'Alwar','state':'Rajasthan','district':'Alwar','price':5200,'min_price':4900,'max_price':5500,'unit':'quintal','date':today},
        {'commodity':'Wheat','variety':'Lokwan','market':'Jaipur','state':'Rajasthan','district':'Jaipur','price':2100,'min_price':2000,'max_price':2200,'unit':'quintal','date':today},
        {'commodity':'Bajra','variety':'Local','market':'Jodhpur','state':'Rajasthan','district':'Jodhpur','price':2300,'min_price':2100,'max_price':2500,'unit':'quintal','date':today},
        {'commodity':'Groundnut','variety':'Bold','market':'Bikaner','state':'Rajasthan','district':'Bikaner','price':5000,'min_price':4700,'max_price':5300,'unit':'quintal','date':today},
    ]
    if commodity:
        data = [d for d in data if d['commodity'].lower() == commodity.lower()]
    if state:
        data = [d for d in data if d['state'].lower() == state.lower()]
    return data

@prices_bp.route('/current', methods=['GET'])
def get_current_prices():
    try:
        commodity = request.args.get('commodity')
        state = request.args.get('state')
        prices = price_fetcher.fetch_current_prices(commodity, state)
        if not prices:
            prices = get_demo_prices(commodity, state)
        return jsonify({'success': True, 'count': len(prices), 'prices': prices}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@prices_bp.route('/historical', methods=['GET'])
def get_historical():
    try:
        commodity = request.args.get('commodity')
        market = request.args.get('market')
        days = int(request.args.get('days', 30))
        if not commodity or not market:
            return jsonify({'success': False, 'error': 'commodity and market required'}), 400
        prices = price_fetcher.get_historical(commodity, market, days)
        return jsonify({'success': True, 'commodity': commodity, 'market': market, 'days': days, 'prices': prices}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@prices_bp.route('/markets', methods=['GET'])
def get_markets():
    try:
        state = request.args.get('state')
        if not state:
            return jsonify({'success': False, 'error': 'state required'}), 400
        markets = agmarknet_api.get_markets_by_state(state)
        return jsonify({'success': True, 'state': state, 'markets': markets}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@prices_bp.route('/commodities', methods=['GET'])
def get_commodities():
    commodities = sorted(list(set([
        'Banana','Bajra','Brinjal','Cabbage','Carrot','Chilli',
        'Coconut','Cotton','Groundnut','Maize','Mustard','Onion',
        'Pepper','Potato','Ragi','Rice','Rubber','Sugarcane',
        'Soybean','Tomato','Turmeric','Wheat'
    ])))
    return jsonify({'success': True, 'commodities': commodities}), 200

@prices_bp.route('/states', methods=['GET'])
def get_states():
    return jsonify({'success': True, 'states': Config.STATES}), 200