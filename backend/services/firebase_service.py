import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime
import json
from config import Config

class FirebaseService:
    """Firebase service for database operations"""
    
    _instance = None
    _db = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
            # Do not initialize Firebase at import time; initialize lazily
            cls._instance._db = None
            cls._instance._initialized = False
        return cls._instance
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS)
            firebase_admin.initialize_app(cred)
            self._db = firestore.client()
            print("✅ Firebase initialized successfully")
        except Exception as e:
            # Don't raise during initialization to avoid import-time failures.
            print(f"❌ Firebase initialization error: {e}")
            self._db = None
        finally:
            self._initialized = True
    
    @property
    def db(self):
        """Get Firestore database instance"""
        # Lazy initialization: try to initialize on first access
        if not getattr(self, '_initialized', False):
            self._initialize_firebase()
        return self._db
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, user_data):
        """Create a new user"""
        try:
            user_data['createdAt'] = datetime.now()
            user_data['updatedAt'] = datetime.now()
            
            doc_ref = self.db.collection('users').document()
            doc_ref.set(user_data)
            
            return {
                'success': True,
                'userId': doc_ref.id,
                'message': 'User created successfully'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_user(self, user_id=None, telegram_id=None):
        """Get user by ID or Telegram ID"""
        try:
            if user_id:
                doc = self.db.collection('users').document(user_id).get()
                if doc.exists:
                    data = doc.to_dict()
                    data['userId'] = doc.id
                    return data
            
            if telegram_id:
                users = self.db.collection('users')\
                    .where('telegramId', '==', str(telegram_id))\
                    .limit(1)\
                    .stream()
                
                for user in users:
                    data = user.to_dict()
                    data['userId'] = user.id
                    return data
            
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def update_user(self, user_id, updates):
        """Update user data"""
        try:
            updates['updatedAt'] = datetime.now()
            self.db.collection('users').document(user_id).update(updates)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== PRICE OPERATIONS ====================
    
    def save_prices(self, prices_data):
        """Save commodity prices"""
        try:
            batch = self.db.batch()
            
            for price in prices_data:
                doc_ref = self.db.collection('prices').document()
                price['timestamp'] = datetime.now()
                batch.set(doc_ref, price)
            
            batch.commit()
            return {'success': True, 'count': len(prices_data)}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_latest_price(self, commodity, market=None, state=None):
        """Get latest price for a commodity"""
        try:
            query = self.db.collection('prices')\
                .where('commodity', '==', commodity)\
                .order_by('timestamp', direction=firestore.Query.DESCENDING)\
                .limit(1)
            
            if market:
                query = query.where('market', '==', market)
            if state:
                query = query.where('state', '==', state)
            
            results = query.stream()
            
            for doc in results:
                data = doc.to_dict()
                data['priceId'] = doc.id
                return data
            
            return None
        except Exception as e:
            print(f"Error getting price: {e}")
            return None
    
    def get_prices_by_state(self, commodity, state, days=1):
        """Get all prices for a commodity in a state"""
        try:
            from datetime import timedelta
            
            start_date = datetime.now() - timedelta(days=days)
            
            prices = self.db.collection('prices')\
                .where('commodity', '==', commodity)\
                .where('state', '==', state)\
                .where('timestamp', '>=', start_date)\
                .order_by('timestamp', direction=firestore.Query.DESCENDING)\
                .stream()
            
            results = []
            for doc in prices:
                data = doc.to_dict()
                data['priceId'] = doc.id
                results.append(data)
            
            return results
        except Exception as e:
            print(f"Error getting prices: {e}")
            return []
    
    def get_historical_prices(self, commodity, market, days=30):
        """Get historical prices for trend analysis"""
        try:
            from datetime import timedelta
            
            start_date = datetime.now() - timedelta(days=days)
            
            prices = self.db.collection('prices')\
                .where('commodity', '==', commodity)\
                .where('market', '==', market)\
                .where('timestamp', '>=', start_date)\
                .order_by('timestamp')\
                .stream()
            
            results = []
            for doc in prices:
                data = doc.to_dict()
                results.append(data)
            
            return results
        except Exception as e:
            print(f"Error getting historical prices: {e}")
            return []
    
    # ==================== ALERT OPERATIONS ====================
    
    def create_alert(self, alert_data):
        """Create a new price alert"""
        try:
            alert_data['createdAt'] = datetime.now()
            alert_data['isActive'] = True
            
            doc_ref = self.db.collection('alerts').document()
            doc_ref.set(alert_data)
            
            return {
                'success': True,
                'alertId': doc_ref.id
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_user_alerts(self, user_id):
        """Get all alerts for a user"""
        try:
            alerts = self.db.collection('alerts')\
                .where('userId', '==', user_id)\
                .where('isActive', '==', True)\
                .stream()
            
            results = []
            for doc in alerts:
                data = doc.to_dict()
                data['alertId'] = doc.id
                results.append(data)
            
            return results
        except Exception as e:
            print(f"Error getting alerts: {e}")
            return []
    
    def delete_alert(self, alert_id):
        """Delete an alert"""
        try:
            self.db.collection('alerts').document(alert_id).update({
                'isActive': False,
                'deletedAt': datetime.now()
            })
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_all_active_alerts(self):
        """Get all active alerts for checking"""
        try:
            alerts = self.db.collection('alerts')\
                .where('isActive', '==', True)\
                .stream()
            
            results = []
            for doc in alerts:
                data = doc.to_dict()
                data['alertId'] = doc.id
                results.append(data)
            
            return results
        except Exception as e:
            print(f"Error getting all alerts: {e}")
            return []
    
    # ==================== TRANSACTION OPERATIONS ====================
    
    def create_transaction(self, transaction_data):
        """Save a sell transaction/recommendation"""
        try:
            transaction_data['requestDate'] = datetime.now()
            transaction_data['status'] = 'pending'
            
            doc_ref = self.db.collection('sell_transactions').document()
            doc_ref.set(transaction_data)
            
            return {
                'success': True,
                'transactionId': doc_ref.id
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_user_transactions(self, user_id, limit=10):
        """Get user's transaction history"""
        try:
            transactions = self.db.collection('sell_transactions')\
                .where('userId', '==', user_id)\
                .order_by('requestDate', direction=firestore.Query.DESCENDING)\
                .limit(limit)\
                .stream()
            
            results = []
            for doc in transactions:
                data = doc.to_dict()
                data['transactionId'] = doc.id
                results.append(data)
            
            return results
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []
    
    def update_transaction_status(self, transaction_id, status):
        """Update transaction status"""
        try:
            self.db.collection('sell_transactions').document(transaction_id).update({
                'status': status,
                'updatedAt': datetime.now()
            })
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== MARKET TRENDS ====================
    
    def save_market_trend(self, trend_data):
        """Save market trend analysis"""
        try:
            trend_data['lastUpdated'] = datetime.now()
            
            # Use commodity+market as document ID for easy updates
            doc_id = f"{trend_data['commodity']}_{trend_data['market']}".replace(' ', '_')
            
            self.db.collection('market_trends').document(doc_id).set(trend_data)
            
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_market_trend(self, commodity, market):
        """Get trend data for commodity in market"""
        try:
            doc_id = f"{commodity}_{market}".replace(' ', '_')
            doc = self.db.collection('market_trends').document(doc_id).get()
            
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"Error getting trend: {e}")
            return None
    
    # ==================== NOTIFICATIONS ====================
    
    def create_notification(self, notification_data):
        """Create a notification record"""
        try:
            notification_data['sentAt'] = datetime.now()
            notification_data['read'] = False
            
            doc_ref = self.db.collection('notifications').document()
            doc_ref.set(notification_data)
            
            return {'success': True, 'notificationId': doc_ref.id}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_user_notifications(self, user_id, unread_only=False):
        """Get user notifications"""
        try:
            query = self.db.collection('notifications')\
                .where('userId', '==', user_id)\
                .order_by('sentAt', direction=firestore.Query.DESCENDING)\
                .limit(50)
            
            if unread_only:
                query = query.where('read', '==', False)
            
            notifications = query.stream()
            
            results = []
            for doc in notifications:
                data = doc.to_dict()
                data['notificationId'] = doc.id
                results.append(data)
            
            return results
        except Exception as e:
            print(f"Error getting notifications: {e}")
            return []
    
    def mark_notification_read(self, notification_id):
        """Mark notification as read"""
        try:
            self.db.collection('notifications').document(notification_id).update({
                'read': True,
                'readAt': datetime.now()
            })
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Create singleton instance
firebase_service = FirebaseService()