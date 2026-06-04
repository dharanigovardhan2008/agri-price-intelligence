from flask import Blueprint, request, jsonify
from services.decision_engine import decision_engine
from transaction import transaction_manager

sell_bp = Blueprint('sell', __name__)

@sell_bp.route('/analyze', methods=['POST'])
def analyze_sell():
    """Analyze sell decision"""
    try:
        data = request.json
        
        # Validate
        required = ['commodity', 'quantity', 'costPerQuintal', 'userLocation']
        if not all(k in data for k in required):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        if not all(k in data['userLocation'] for k in ['state', 'lat', 'lng']):
            return jsonify({'success': False, 'error': 'Invalid location'}), 400
        
        # Analyze
        recommendation = decision_engine.analyze(
            commodity=data['commodity'],
            quantity=data['quantity'],
            cost_per_quintal=data['costPerQuintal'],
            user_location=data['userLocation']
        )
        
        # Save transaction
        if 'userId' in data and recommendation.get('success'):
            transaction_manager.create_transaction(
                user_id=data['userId'],
                commodity=data['commodity'],
                quantity=data['quantity'],
                cost_per_quintal=data['costPerQuintal'],
                recommendation=recommendation
            )
        
        if recommendation.get('success'):
            return jsonify(recommendation), 200
        else:
            return jsonify(recommendation), 400
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@sell_bp.route('/history/<user_id>', methods=['GET'])
def get_history(user_id):
    """Get sell history"""
    try:
        limit = int(request.args.get('limit', 10))
        transactions = transaction_manager.get_user_transactions(user_id, limit)
        
        return jsonify({
            'success': True,
            'count': len(transactions),
            'transactions': [t.to_dict() for t in transactions]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500