from services.profit_calculator import profit_calculator

class MarketComparator:
    """Compare markets and find best options"""
    
    def __init__(self):
        self.profit_calc = profit_calculator
    
    def compare_markets(self, commodity, quantity, cost_per_quintal, user_location, market_prices):
        """Compare all markets"""
        comparisons = []
        
        for market in market_prices:
            # Add location if missing
            if 'location' not in market:
                market['location'] = self._get_location(market['market'])
            
            # Calculate profit
            profit_data = self.profit_calc.calculate_profit(
                market, quantity, cost_per_quintal, user_location
            )
            
            comparisons.append(profit_data)
        
        # Sort by profit
        comparisons.sort(key=lambda x: x['net_profit'], reverse=True)
        
        return {
            'best': comparisons[0] if comparisons else None,
            'all': comparisons,
            'worst': comparisons[-1] if comparisons else None,
            'average_profit': sum(c['net_profit'] for c in comparisons) / len(comparisons) if comparisons else 0
        }
    
    def _get_location(self, market_name):
        """Get market coordinates"""
        locations = {
            'Khanna': {'lat': 30.7051, 'lng': 76.2220},
            'Ludhiana': {'lat': 30.9010, 'lng': 75.8573},
            'Jalandhar': {'lat': 31.3260, 'lng': 75.5762},
            'Amritsar': {'lat': 31.6340, 'lng': 74.8723},
            'Bathinda': {'lat': 30.2110, 'lng': 74.9455},
            'Karnal': {'lat': 29.6857, 'lng': 76.9905},
        }
        return locations.get(market_name, {'lat': 30.7051, 'lng': 76.2220})

# Create instance
market_comparator = MarketComparator()