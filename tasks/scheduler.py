from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import sys
sys.path.append('..')

from fetch_daily_prices import fetch_and_save_prices
from check_alerts import check_and_send_alerts
from send_notifications import send_daily_digest

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start_scheduler():
    """Start all scheduled tasks"""
    scheduler = BackgroundScheduler()
    
    # Fetch prices every 6 hours
    scheduler.add_job(
        fetch_and_save_prices,
        'interval',
        hours=6,
        id='fetch_prices',
        name='Fetch commodity prices',
        max_instances=1
    )
    logger.info("✅ Scheduled: Fetch prices every 6 hours")
    
    # Check alerts every hour
    scheduler.add_job(
        check_and_send_alerts,
        'interval',
        hours=1,
        id='check_alerts',
        name='Check price alerts',
        max_instances=1
    )
    logger.info("✅ Scheduled: Check alerts every hour")
    
    # Send daily digest at 8 AM
    scheduler.add_job(
        send_daily_digest,
        CronTrigger(hour=8, minute=0),
        id='daily_digest',
        name='Send daily price digest',
        max_instances=1
    )
    logger.info("✅ Scheduled: Daily digest at 8:00 AM")
    
    # Start scheduler
    scheduler.start()
    logger.info("🚀 Scheduler started successfully!")
    
    return scheduler

if __name__ == '__main__':
    scheduler = start_scheduler()
    
    # Keep running
    try:
        import time
        logger.info("⏰ Scheduler is running. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Shutting down scheduler...")
        scheduler.shutdown()
        logger.info("👋 Scheduler stopped.")