"""
Example usage and advanced scenarios for Decoy Service
"""

from decoy_service import DecoyService
from scheduler import DecoyScheduler
from utils import Logger, ConfigManager
import logging


def example_1_simple_session():
    """
    Example 1: Run a simple one-time decoy session
    """
    print("Example 1: Simple Session")
    print("-" * 50)
    
    service = DecoyService('config')
    service.start_session()
    
    # Print summary
    summary = service.tracker.get_summary()
    print("\nSession Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")


def example_2_scheduled_sessions():
    """
    Example 2: Schedule decoy sessions at regular intervals
    """
    print("Example 2: Scheduled Sessions")
    print("-" * 50)
    
    config_manager = ConfigManager('config')
    settings = config_manager.load_settings()
    logger = Logger.setup_logging(settings)
    
    scheduler = DecoyScheduler('config', logger)
    
    # Run for 15 minutes every 3 hours
    scheduler.schedule_interval(minutes=180, duration_minutes=15)
    
    # Run daily at 2 PM
    scheduler.schedule_daily(hour=14, minute=0, duration_minutes=30)
    
    # Start scheduler
    scheduler.start()
    
    print("Scheduler running. Sessions will run according to schedule.")
    print("Press Ctrl+C to stop.")
    
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
        print("Scheduler stopped")


def example_3_custom_configuration():
    """
    Example 3: Use custom configuration
    """
    print("Example 3: Custom Configuration")
    print("-" * 50)
    
    # Load and modify configuration
    config_manager = ConfigManager('config')
    settings = config_manager.load_settings()
    
    # Customize settings
    settings['activity']['session_duration'] = 60  # 1 hour session
    settings['clicking']['clicks_per_page_max'] = 10  # More clicks
    settings['activity']['requests_per_hour'] = 50  # More requests
    
    # Create service with custom config
    service = DecoyService('config')
    service.settings = settings
    
    service.start_session()


def example_4_activity_tracking():
    """
    Example 4: Track and analyze activity
    """
    print("Example 4: Activity Tracking")
    print("-" * 50)
    
    service = DecoyService('config')
    service.start_session()
    
    # Get detailed summary
    summary = service.tracker.get_summary()
    
    print("\nDetailed Activity Summary:")
    print(f"Duration: {summary['session_duration_minutes']:.2f} minutes")
    print(f"Websites visited: {summary['websites_visited']}")
    print(f"Total clicks: {summary['total_clicks']}")
    print(f"Search queries: {summary['search_queries']}")
    print(f"Forms filled: {summary['forms_filled']}")
    
    # Calculate metrics
    if summary['session_duration_minutes'] > 0:
        clicks_per_minute = summary['total_clicks'] / summary['session_duration_minutes']
        print(f"Clicks per minute: {clicks_per_minute:.2f}")
        
        sites_per_hour = (summary['websites_visited'] / summary['session_duration_minutes']) * 60
        print(f"Sites per hour: {sites_per_hour:.2f}")


def example_5_quiet_background_mode():
    """
    Example 5: Run in quiet background mode
    """
    print("Example 5: Background Mode (headless)")
    print("-" * 50)
    
    config_manager = ConfigManager('config')
    settings = config_manager.load_settings()
    
    # Ensure headless mode is enabled
    settings['browser']['headless'] = True
    
    # Reduce logging noise
    settings['logging']['level'] = 'WARNING'
    
    logger = Logger.setup_logging(settings)
    
    service = DecoyService('config')
    service.settings = settings
    service.logger = logger
    
    service.start_session()
    print("Background session completed")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        example_num = int(sys.argv[1])
        
        examples = {
            1: example_1_simple_session,
            2: example_2_scheduled_sessions,
            3: example_3_custom_configuration,
            4: example_4_activity_tracking,
            5: example_5_quiet_background_mode,
        }
        
        if example_num in examples:
            examples[example_num]()
        else:
            print(f"Example {example_num} not found")
    else:
        print("Decoy Service - Example Usage")
        print("=" * 50)
        print("\nRun examples with: python examples.py [1-5]")
        print("\n1. Simple one-time session")
        print("2. Scheduled sessions")
        print("3. Custom configuration")
        print("4. Activity tracking and metrics")
        print("5. Quiet background mode")
