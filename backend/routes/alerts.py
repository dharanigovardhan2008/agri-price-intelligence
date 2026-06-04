from flask import Blueprint, request, jsonify
from alert import alert_manager

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/create', methods=['POST'])
def create_alert():
    """Create price alert"""
    try:
        data = request.json
        
        required = ['userId', 'commodity', 'targetPrice', 'alertType']
        if not all(k in data for k in required):
            return jsonify({'success': False, 'error': 'Missing fields'}), 400
        
        result = alert_manager.create_alert(
            user_id=data['userId'],
            commodity=data['commodity'],
            target_price=data['targetPrice'],
            alert_type=data['alertType'],
            market=data.get('market')
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@alerts_bp.route('/user/<user_id>', methods=['GET'])
def get_alerts(user_id):
    """Get user alerts"""
    try:
        alerts = alert_manager.get_user_alerts(user_id)
        
        return jsonify({
            'success': True,
            'count': len(alerts),
            'alerts': alerts
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@alerts_bp.route('/<alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    """Delete alert"""
    try:
        from services.firebase_service import firebase_service
        result = firebase_service.delete_alert(alert_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500