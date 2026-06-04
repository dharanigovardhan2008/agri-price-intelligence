from models.alert import Alert
from services.firebase_service import firebase_service

class AlertManager:
    """Manage price alerts"""
    
    def __init__(self):
        self.db = firebase_service
    
    def create_alert(self, user_id, commodity, target_price, alert_type='price_above', market=None):
        """Create new alert"""
        alert = Alert(
            user_id=user_id,
            commodity=commodity,
            target_price=target_price,
            alert_type=alert_type,
            market=market
        )
        
        return self.db.create_alert(alert.to_dict())
    
    def get_user_alerts(self, user_id):
        """Get user's alerts"""
        return self.db.get_user_alerts(user_id)
    
    def check_alerts(self, current_prices):
        """Check if any alerts should trigger"""
        all_alerts = self.db.get_all_active_alerts()
        triggered = []
        
        for alert_data in all_alerts:
            alert = Alert.from_dict(alert_data)
            
            # Find matching price
            for price in current_prices:
                if price['commodity'].lower() == alert.commodity.lower():
                    if self._should_trigger(alert, price['price']):
                        triggered.append({
                            'alert': alert.to_dict(),
                            'current_price': price['price']
                        })
        
        return triggered
    
    def _should_trigger(self, alert, current_price):
        """Check if alert should trigger"""
        if alert.alert_type == 'price_above':
            return current_price >= alert.target_price
        elif alert.alert_type == 'price_below':
            return current_price <= alert.target_price
        return False

# Create instance
alert_manager = AlertManager()