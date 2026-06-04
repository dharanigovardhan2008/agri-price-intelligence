import math
from config import Config

class ProfitCalculator:
    """Calculate profit for selling commodities"""
    
    def __init__(self):
        self.transport_cost_per_km = Config.TRANSPORT_COST_PER_KM
        self.commission_percent = Config.MANDI_COMMISSION_PERCENT
        self.loading_cost = Config.LOADING_COST_PER_QUINTAL
    
    def calculate_distance(self, location1, location2):
        """
        Calculate distance between two locations using Haversine formula
        location format: {'lat': float, 'lng': float}
        """
        if not all(k in location1 for k in ['lat', 'lng']) or \
           not all(k in location2 for k in ['lat', 'lng']):
            return 50  # Default distance if coordinates not available
        
        # Haversine formula
        R = 6371  # Earth's radius in km
        
        lat1 = math.radians(location1['lat'])
        lat2 = math.radians(location2['lat'])
        dlat = math.radians(location2['lat'] - location1['lat'])
        dlng = math.radians(location2['lng'] - location1['lng'])
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        distance = R * c
        return round(distance, 2)
    
    def estimate_transport_cost(self, distance, quantity):
        """
        Estimate transportation cost
        distance in km, quantity in quintals
        """
        # Base cost + per km per quintal cost
        base_cost = 500  # Minimum charge
        variable_cost = distance * quantity * self.transport_cost_per_km
        
        return round(base_cost + variable_cost, 2)
    
    def calculate_profit(self, market_data, quantity, cost_per_quintal, user_location):
        """
        Calculate detailed profit for a specific market
        """
        # Revenue
        price_per_quintal = market_data['price']
        total_revenue = price_per_quintal * quantity
        
        # Costs
        total_cost = cost_per_quintal * quantity
        
        # Get market location
        market_location = market_data.get('location', {'lat': 30.7051, 'lng': 76.2220})
        
        # Transportation cost
        distance = self.calculate_distance(user_location, market_location)
        transport_cost = self.estimate_transport_cost(distance, quantity)
        
        # Mandi commission (percentage of revenue)
        commission = (total_revenue * self.commission_percent) / 100
        
        # Loading/unloading cost
        loading_cost = quantity * self.loading_cost
        
        # Total expenses
        total_expenses = total_cost + transport_cost + commission + loading_cost
        
        # Net profit
        net_profit = total_revenue - total_expenses
        
        # Profit margin
        profit_margin = (net_profit / total_cost * 100) if total_cost > 0 else 0
        
        # Profit per quintal
        profit_per_quintal = net_profit / quantity if quantity > 0 else 0
        
        return {
            'market_name': market_data['market'],
            'state': market_data.get('state', ''),
            'district': market_data.get('district', ''),
            'distance': distance,
            'price_per_quintal': price_per_quintal,
            'quantity': quantity,
            'revenue': round(total_revenue, 2),
            'cost': round(total_cost, 2),
            'transport_cost': round(transport_cost, 2),
            'commission': round(commission, 2),
            'loading_cost': round(loading_cost, 2),
            'total_expenses': round(total_expenses, 2),
            'net_profit': round(net_profit, 2),
            'profit_margin': round(profit_margin, 2),
            'profit_per_quintal': round(profit_per_quintal, 2),
            'location': market_location
        }
    
    def compare_all_markets(self, commodity, quantity, cost_per_quintal, user_location, market_prices):
        """
        Compare profits across all available markets
        """
        results = []
        
        for market in market_prices:
            # Add location if not present (mock data)
            if 'location' not in market:
                market['location'] = self._get_market_location(market['market'])
            
            profit_data = self.calculate_profit(
                market,
                quantity,
                cost_per_quintal,
                user_location
            )
            results.append(profit_data)
        
        # Sort by net profit (descending)
        results.sort(key=lambda x: x['net_profit'], reverse=True)
        
        if not results:
            return {
                'best_option': None,
                'all_options': [],
                'worst_option': None,
                'average_profit': 0
            }
        
        return {
            'best_option': results[0],
            'all_options': results,
            'worst_option': results[-1],
            'average_profit': round(sum(r['net_profit'] for r in results) / len(results), 2)
        }
    
    def _get_market_location(self, market_name):
        """Get coordinates for market (mock data)"""
        # Mock market locations
        locations = {
            'Khanna': {'lat': 30.7051, 'lng': 76.2220},
            'Ludhiana': {'lat': 30.9010, 'lng': 75.8573},
            'Jalandhar': {'lat': 31.3260, 'lng': 75.5762},
            'Amritsar': {'lat': 31.6340, 'lng': 74.8723},
            'Bathinda': {'lat': 30.2110, 'lng': 74.9455},
            'Patiala': {'lat': 30.3398, 'lng': 76.3869},
        }
        
        return locations.get(market_name, {'lat': 30.7051, 'lng': 76.2220})

# Create instance
profit_calculator = ProfitCalculator()