import sys
sys.path.append('..')

from backend.api.agmarknet import agmarknet_api
from backend.services.firebase_service import firebase_service
from backend.config import Config
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_and_save_prices():
    """Fetch prices from APIs and save to Firebase"""
    try:
        logger.info(f"🔄 Starting price fetch at {datetime.now()}")
        
        all_prices = []
        commodities = Config.POPULAR_COMMODITIES[:5]  # Top 5 commodities
        states = ['Punjab', 'Haryana', 'Uttar Pradesh']
        
        for commodity in commodities:
            for state in states:
                try:
                    prices = agmarknet_api.fetch_prices(
                        commodity=commodity,
                        state=state
                    )
                    all_prices.extend(prices)
                    logger.info(f"  ✓ Fetched {len(prices)} prices for {commodity} in {state}")
                except Exception as e:
                    logger.error(f"  ✗ Error fetching {commodity} in {state}: {e}")
        
        # Save to Firebase
        if all_prices:
            result = firebase_service.save_prices(all_prices)
            if result['success']:
                logger.info(f"✅ Saved {result['count']} price records to Firebase")
            else:
                logger.error(f"❌ Error saving prices: {result.get('error')}")
        else:
            logger.warning("⚠️ No prices fetched")
        
        logger.info(f"✅ Price fetch completed at {datetime.now()}")
        
    except Exception as e:
        logger.error(f"❌ Error in fetch_and_save_prices: {e}")

if __name__ == '__main__':
    fetch_and_save_prices()