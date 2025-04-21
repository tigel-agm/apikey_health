import logging
from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session
from .db import engine
from .crud import get_api_keys, create_health_check
from .adapters.openai_adapter import test_openai_key

logger = logging.getLogger(__name__)

# Function to perform health checks for all keys
def check_keys():
    logger.info("Running scheduled health checks")
    with Session(engine) as session:
        keys = get_api_keys(session)
        for key in keys:
            status, rt, err = test_openai_key(key.key_value)
            hc = create_health_check(session, key.id, status, rt, err)
            key.last_checked = hc.checked_at
            session.add(key)
        session.commit()
        logger.info("Completed health checks")

# Start the scheduler with a 5-minute interval

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_keys, 'interval', minutes=5)
    scheduler.start()
    logger.info("Scheduler started: health checks every 5 minutes")
