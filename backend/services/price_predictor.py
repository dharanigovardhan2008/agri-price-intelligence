import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

class SimplePricePredictor:
    """
    Simple price prediction using linear regression
    Can be enhanced with more sophisticated models
    """
    
    def predict_next_days(self, historical_prices, days=7):
        """
        Predict prices for next N days
        historical_prices: list of prices (most recent last)
        """
        if not historical_prices or len(historical_prices) < 3:
            # Not enough data for prediction
            return historical_prices[-1:] * days if historical_prices else []
        
        try:
            # Prepare data
            X = np.array(range(len(historical_prices))).reshape(-1, 1)
            y = np.array(historical_prices)
            
            # Train linear regression model
            model = LinearRegression()
            model.fit(X, y)
            
            # Predict future days
            future_indices = np.array(
                range(len(historical_prices), len(historical_prices) + days)
            ).reshape(-1, 1)
            
            predictions = model.predict(future_indices)
            
            # Add some realistic variance
            predictions = self._add_variance(predictions, historical_prices)
            
            # Ensure predictions are positive and realistic
            predictions = np.maximum(predictions, historical_prices[-1] * 0.8)
            predictions = np.minimum(predictions, historical_prices[-1] * 1.3)
            
            return predictions.tolist()
            
        except Exception as e:
            print(f"Prediction error: {e}")
            # Fallback: return last price
            return [historical_prices[-1]] * days
    
    def _add_variance(self, predictions, historical_prices):
        """Add realistic variance to predictions"""
        # Calculate historical volatility
        if len(historical_prices) < 2:
            return predictions
        
        price_changes = np.diff(historical_prices)
        std_dev = np.std(price_changes)
        
        # Add small random variations
        np.random.seed(42)  # For reproducibility
        variance = np.random.normal(0, std_dev * 0.5, len(predictions))
        
        return predictions + variance
    
    def calculate_trend(self, historical_prices):
        """
        Calculate price trend
        Returns: 'rising', 'falling', or 'stable'
        """
        if not historical_prices or len(historical_prices) < 5:
            return 'stable'
        
        recent = historical_prices[-7:]
        older = historical_prices[-14:-7] if len(historical_prices) >= 14 else historical_prices[:-7]
        
        recent_avg = np.mean(recent)
        older_avg = np.mean(older) if older else recent_avg
        
        change_percent = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
        
        if change_percent > 3:
            return 'rising'
        elif change_percent < -3:
            return 'falling'
        return 'stable'
    
    def predict_best_selling_day(self, historical_prices, future_days=15):
        """
        Predict the best day to sell in the next N days
        Returns day number (1-N) and expected price
        """
        predictions = self.predict_next_days(historical_prices, future_days)
        
        if not predictions:
            return {'day': 1, 'price': historical_prices[-1] if historical_prices else 0}
        
        max_price = max(predictions)
        best_day = predictions.index(max_price) + 1
        
        return {
            'day': best_day,
            'price': round(max_price, 2),
            'current_price': historical_prices[-1] if historical_prices else 0,
            'expected_gain': round(max_price - historical_prices[-1], 2) if historical_prices else 0
        }

# Create instance
price_predictor = SimplePricePredictor()