import numpy as np
from datetime import datetime
from services.firebase_service import firebase_service
from services.profit_calculator import profit_calculator
from services.price_predictor import price_predictor
from services.price_fetcher import price_fetcher

class SellDecisionEngine:
    """Intelligent sell/hold decision engine"""
    
    def __init__(self):
        self.profit_calc = profit_calculator
        self.predictor = price_predictor
        self.fetcher = price_fetcher
    
    def analyze(self, commodity, quantity, cost_per_quintal, user_location):
        """Main analysis function"""
        try:
            # Get current prices
            current_prices = self.fetcher.fetch_current_prices(
                commodity=commodity,
                state=user_location['state']
            )
            
            if not current_prices:
                return {'success': False, 'error': 'No market data available'}
            
            # Get best market
            best_market = max(current_prices, key=lambda x: x['price'])
            
            # Get historical data
            historical = self.fetcher.get_historical(commodity, best_market['market'])
            
            # Compare markets
            from services.market_comparator import market_comparator
            profit_analysis = market_comparator.compare_markets(
                commodity, quantity, cost_per_quintal, user_location, current_prices
            )
            
            # Predict prices
            predictions = self._predict_prices(historical)
            
            # Make decision
            decision = self._make_decision(
                current_prices, historical, predictions, profit_analysis
            )
            
            return {
                'success': True,
                'commodity': commodity,
                'quantity': quantity,
                'decision': decision['decision'],
                'confidence': decision['confidence'],
                'reasoning': decision['reasoning'],
                'bestMarket': profit_analysis['best'],
                'alternativeMarkets': profit_analysis['all'][1:4],
                'waitOption': decision.get('wait_option'),
                'marketAnalysis': {
                    'currentAverage': np.mean([p['price'] for p in current_prices]),
                    'historicalAverage': np.mean([p['price'] for p in historical]) if historical else 0,
                    'priceDirection': decision.get('price_direction', 'stable'),
                    'marketSupply': decision.get('market_supply', 'normal')
                }
            }
            
        except Exception as e:
            print(f"Decision engine error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _predict_prices(self, historical):
        """Predict future prices"""
        if not historical:
            return []
        prices = [p['price'] for p in historical]
        return self.predictor.predict_next_days(prices, days=15)
    
    def _make_decision(self, current, historical, predictions, profit_analysis):
        """Core decision logic"""
        best_price = max([p['price'] for p in current])
        avg_price = np.mean([p['price'] for p in current])
        
        if historical:
            hist_prices = [p['price'] for p in historical]
            avg_30_day = np.mean(hist_prices)
            recent_7 = np.mean(hist_prices[-7:]) if len(hist_prices) >= 7 else avg_30_day
        else:
            avg_30_day = best_price
            recent_7 = best_price
        
        predicted_max = max(predictions) if predictions else best_price
        
        # Calculate factors
        factors = {
            'price_position': ((best_price - avg_30_day) / avg_30_day * 100) if avg_30_day > 0 else 0,
            'recent_trend': ((recent_7 - avg_30_day) / avg_30_day * 100) if avg_30_day > 0 else 0,
            'prediction_delta': ((predicted_max - best_price) / best_price * 100) if best_price > 0 else 0,
            'profit_margin': profit_analysis['best']['profit_margin'] if profit_analysis['best'] else 0,
            'market_arrival': self._calculate_supply(current)
        }
        
        # Scoring
        sell_score = 0
        wait_score = 0
        reasoning = []
        
        # Price position
        if factors['price_position'] > 8:
            sell_score += 35
            reasoning.append(f"✅ Price {factors['price_position']:.1f}% above 30-day average")
        elif factors['price_position'] < -5:
            wait_score += 30
            reasoning.append(f"⚠️ Price {abs(factors['price_position']):.1f}% below average")
        
        # Trend
        if factors['recent_trend'] < -3:
            sell_score += 20
            reasoning.append("⚠️ Falling prices - Sell now")
        elif factors['recent_trend'] > 3:
            wait_score += 20
            reasoning.append("📈 Rising trend")
        
        # Prediction
        if factors['prediction_delta'] > 4:
            wait_score += 30
            reasoning.append(f"📈 Expected to rise {factors['prediction_delta']:.1f}%")
        elif factors['prediction_delta'] < -2:
            sell_score += 25
            reasoning.append("📉 Expected to fall")
        
        # Profit margin
        if factors['profit_margin'] > 20:
            sell_score += 15
            reasoning.append(f"💰 Excellent profit ({factors['profit_margin']:.1f}%)")
        elif factors['profit_margin'] < 10:
            wait_score += 15
            reasoning.append("⚠️ Low profit margin")
        
        # Supply
        if factors['market_arrival'] == 'high':
            sell_score += 15
            reasoning.append("⚠️ High supply - Prices may drop")
        
        confidence = min(max(sell_score, wait_score), 95)
        
        decision = {
            'confidence': confidence,
            'reasoning': reasoning,
            'price_direction': 'rising' if wait_score > sell_score else 'falling',
            'market_supply': factors['market_arrival']
        }
        
        if sell_score > wait_score + 20:
            decision['decision'] = 'SELL_NOW'
        elif wait_score > sell_score + 20:
            decision['decision'] = 'WAIT'
            decision['wait_option'] = self._calculate_wait(predictions, profit_analysis['best'], factors)
        else:
            decision['decision'] = 'NEUTRAL'
            decision['reasoning'].append("📊 Mixed market conditions")
        
        return decision
    
    def _calculate_supply(self, prices):
        """Calculate supply level"""
        avg_arrival = np.mean([p.get('arrival', 0) for p in prices])
        if avg_arrival > 150:
            return 'high'
        elif avg_arrival < 80:
            return 'low'
        return 'normal'
    
    def _calculate_wait(self, predictions, best_market, factors):
        """Calculate wait option"""
        if not predictions:
            return None
        
        best_predicted = max(predictions[:15])
        current = best_market['price_per_quintal']
        increase = best_predicted - current
        days = predictions.index(best_predicted) + 1
        
        storage_cost = days * 20
        extra_profit = (increase * best_market['quantity']) - storage_cost
        
        risk = 'low'
        if factors['price_position'] > 8 or factors['market_arrival'] == 'high':
            risk = 'high'
        elif abs(factors['prediction_delta']) > 5:
            risk = 'medium'
        
        return {
            'days': days,
            'expectedPrice': round(best_predicted, 2),
            'potentialExtraProfit': round(extra_profit, 2),
            'storageCost': storage_cost,
            'risk': risk,
            'riskFactors': self._get_risks(factors, risk)
        }
    
    def _get_risks(self, factors, risk_level):
        """Get risk factors"""
        risks = []
        if risk_level == 'high':
            if factors['price_position'] > 8:
                risks.append("Prices at peak")
            if factors['market_arrival'] == 'high':
                risks.append("High supply")
            risks.append("Weather uncertainties")
        elif risk_level == 'medium':
            risks.append("Market volatility")
            risks.append("Storage costs")
        else:
            risks.append("Minimal risk")
        return risks

# Create instance
decision_engine = SellDecisionEngine()