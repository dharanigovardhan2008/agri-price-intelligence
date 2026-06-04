from datetime import datetime

class Price:
    """Price model"""
    
    def __init__(self, price_id=None, commodity=None, market=None, state=None,
                 district=None, price=0, unit='quintal', arrival=0, date=None, **kwargs):
        self.price_id = price_id
        self.commodity = commodity
        self.market = market
        self.state = state
        self.district = district
        self.price = price
        self.unit = unit
        self.arrival = arrival
        self.date = date or datetime.now().strftime('%Y-%m-%d')
        self.timestamp = kwargs.get('timestamp', datetime.now())
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'priceId': self.price_id,
            'commodity': self.commodity,
            'market': self.market,
            'state': self.state,
            'district': self.district,
            'price': self.price,
            'unit': self.unit,
            'arrival': self.arrival,
            'date': self.date,
            'timestamp': self.timestamp
        }
    
    @staticmethod
    def from_dict(data):
        """Create from dictionary"""
        return Price(
            price_id=data.get('priceId'),
            commodity=data.get('commodity'),
            market=data.get('market'),
            state=data.get('state'),
            district=data.get('district'),
            price=data.get('price', 0),
            unit=data.get('unit', 'quintal'),
            arrival=data.get('arrival', 0),
            date=data.get('date'),
            timestamp=data.get('timestamp')
        )