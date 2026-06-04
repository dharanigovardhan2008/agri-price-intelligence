from flask import Blueprint, request, jsonify
from services.price_fetcher import price_fetcher
from api.agmarknet import agmarknet_api
from config import Config

prices_bp = Blueprint('prices', __name__)

@prices_bp.route('/current', methods=['GET'])
def get_current_prices():
    """Get current prices"""
    try:
        commodity = request.args.get('commodity')
        state = request.args.get('state')
        
        prices = price_fetcher.fetch_current_prices(commodity, state)
        
        return jsonify({
            'success': True,
            'count': len(prices),
            'prices': prices
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@prices_bp.route('/historical', methods=['GET'])
def get_historical():
    """Get historical prices"""
    try:
        commodity = request.args.get('commodity')
        market = request.args.get('market')
        days = int(request.args.get('days', 30))
        
        if not commodity or not market:
            return jsonify({'success': False, 'error': 'commodity and market required'}), 400
        
        prices = price_fetcher.get_historical(commodity, market, days)
        
        return jsonify({
            'success': True,
            'commodity': commodity,
            'market': market,
            'days': days,
            'prices': prices
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@prices_bp.route('/markets', methods=['GET'])
def get_markets():
    """Get markets by state"""
    try:
        state = request.args.get('state')
        
        if not state:
            return jsonify({'success': False, 'error': 'state required'}), 400
        
        markets = agmarknet_api.get_markets_by_state(state)
        
        return jsonify({
            'success': True,
            'state': state,
            'markets': markets
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@prices_bp.route('/commodities', methods=['GET'])
def get_commodities():
    """Get commodities list"""
    return jsonify({
        'success': True,
        'commodities': Config.POPULAR_COMMODITIES
    }), 200

@prices_bp.route('/states', methods=['GET'])
def get_states():
    """Get states list"""
    return jsonify({
        'success': True,
        'states': Config.STATES
    }), 200