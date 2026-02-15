"""
Scheduler for running decoy service at regular intervals
Supports cron-like scheduling and daemon mode
"""

import logging
import schedule
import time
import threading
from typing import Dict, Any
from .decoy_service import DecoyService


class DecoyScheduler:
    """Schedule decoy activity at regular intervals"""
    
    def __init__(self, config_dir: str = 'config', logger: logging.Logger = None):
        self.config_dir = config_dir
        self.logger = logger or logging.getLogger('DecoyScheduler')
        self.service = DecoyService(config_dir)
        self.scheduler = schedule.Scheduler()
        self.running = False
    
    def schedule_daily(self, hour: int, minute: int, duration_minutes: int = 30):
        """Schedule decoy activity daily at specific time"""
        time_str = f"{hour:02d}:{minute:02d}"
        
        self.scheduler.every().day.at(time_str).do(
            self._run_session,
            duration_minutes=duration_minutes
        )
        
        self.logger.info(f"Scheduled decoy session daily at {time_str} "
                        f"for {duration_minutes} minutes")
    
    def schedule_hourly(self, minute: int = 0, duration_minutes: int = 10):
        """Schedule decoy activity every hour"""
        self.scheduler.every().hour.at(f":{minute:02d}").do(
            self._run_session,
            duration_minutes=duration_minutes
        )
        
        self.logger.info(f"Scheduled decoy session every hour at :{minute:02d} "
                        f"for {duration_minutes} minutes")
    
    def schedule_interval(self, minutes: int, duration_minutes: int = 10):
        """Schedule decoy activity at regular intervals"""
        self.scheduler.every(minutes).minutes.do(
            self._run_session,
            duration_minutes=duration_minutes
        )
        
        self.logger.info(f"Scheduled decoy session every {minutes} minutes "
                        f"for {duration_minutes} minutes")
    
    def _run_session(self, duration_minutes: int = 0):
        """Run a decoy service session"""
        self.logger.info(f"Starting scheduled decoy session ({duration_minutes}m)")
        
        # Create a fresh service instance for each session
        service = DecoyService(self.config_dir)
        service.start_session(duration_minutes)
    
    def start(self):
        """Start the scheduler in a background thread"""
        self.running = True
        scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        scheduler_thread.start()
        self.logger.info("Scheduler started")
    
    def _run_scheduler(self):
        """Run scheduler loop"""
        while self.running:
            self.scheduler.run_pending()
            time.sleep(60)  # Check every minute
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        self.logger.info("Scheduler stopped")


def main():
    """Example usage of scheduler"""
    import sys
    from .utils import Logger, ConfigManager
    
    config_dir = 'config'
    if len(sys.argv) > 1:
        config_dir = sys.argv[1]
    
    # Setup logging
    config_manager = ConfigManager(config_dir)
    settings = config_manager.load_settings()
    logger = Logger.setup_logging(settings)
    
    # Create scheduler
    scheduler = DecoyScheduler(config_dir, logger)
    
    # Schedule decoy activity
    # Example: Run for 15 minutes every 3 hours
    scheduler.schedule_interval(minutes=180, duration_minutes=15)
    
    # Alternative: Run daily at 2 PM for 30 minutes
    # scheduler.schedule_daily(hour=14, minute=0, duration_minutes=30)
    
    # Start scheduler
    scheduler.start()
    
    logger.info("Scheduler running. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
        logger.info("Scheduler stopped by user")


if __name__ == '__main__':
    main()
