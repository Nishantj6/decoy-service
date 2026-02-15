"""
Main decoy service orchestrator
Coordinates browser agents and generates random browsing activity
"""

import logging
import time
import random
from typing import Dict, Any, List
from datetime import datetime, timedelta

from .utils import Logger, ConfigManager, ActivityTracker, RandomnessGenerator
from .browser_agent import create_agent


class DecoyService:
    """Main service class that coordinates decoy activity"""
    
    def __init__(self, config_dir: str = 'config'):
        # Load configuration
        self.config_manager = ConfigManager(config_dir)
        self.settings = self.config_manager.load_settings()
        self.websites_config = self.config_manager.load_websites()
        
        # Setup logging
        self.logger = Logger.setup_logging(self.settings)
        self.logger.info("Decoy Service initialized")
        
        # Activity tracking
        self.tracker = ActivityTracker(self.logger)
        
        # Browser agent
        self.agent = None
        
        # Session control
        self.running = False
        self.start_time = None
    
    def _flatten_website_list(self) -> List[str]:
        """Flatten website categories into a single list"""
        websites = []
        for category, urls in self.websites_config.items():
            websites.extend(urls)
        return websites
    
    def _get_search_queries(self) -> List[str]:
        """Get search queries from config"""
        return self.websites_config.get('search_queries', [])
    
    def _get_random_website(self) -> str:
        """Get a random website from config"""
        websites = self._flatten_website_list()
        return RandomnessGenerator.get_random_element(websites)
    
    def _get_random_query(self) -> str:
        """Get a random search query"""
        queries = self._get_search_queries()
        if not queries:
            return "random topic"
        return RandomnessGenerator.get_random_element(queries)
    
    def _interact_with_page(self):
        """Perform deep, natural interactions on current page"""
        config = self.settings.get('clicking', {})

        # Handle popups first (cookie banners, etc.)
        self.agent.handle_popups()
        time.sleep(random.uniform(0.5, 1.0))

        # Choose interaction style: deep reading vs quick browsing
        interaction_style = random.choice(['deep_read', 'quick_browse', 'media_focus'])

        if interaction_style == 'deep_read':
            # Natural scrolling as if reading an article
            self.logger.debug("Deep reading interaction")
            if config.get('enable_scrolling', True):
                self.agent.natural_scroll()

            # Occasional clicks while reading
            num_clicks = random.randint(1, 2)
            for _ in range(num_clicks):
                if self.agent.random_click():
                    self.tracker.record_click()
                time.sleep(random.uniform(1.5, 3.0))

        elif interaction_style == 'media_focus':
            # Focus on images and videos
            self.logger.debug("Media-focused interaction")
            self.agent.interact_with_media()

            # Some scrolling to find more media
            if config.get('enable_scrolling', True):
                scroll_amount = random.randint(300, 600)
                self.agent.scroll_page(scroll_amount)
                time.sleep(random.uniform(1.0, 2.0))
                self.agent.interact_with_media()

        else:  # quick_browse
            # Quick scanning with multiple clicks
            self.logger.debug("Quick browsing interaction")
            clicks_min = config.get('clicks_per_page_min', 1)
            clicks_max = config.get('clicks_per_page_max', 5)
            num_clicks = random.randint(clicks_min, clicks_max)

            for _ in range(num_clicks):
                if self.agent.random_click():
                    self.tracker.record_click()

                delay = RandomnessGenerator.get_random_delay(2, 5)
                time.sleep(delay)

            # Basic scrolling
            if config.get('enable_scrolling', True):
                scroll_amount = random.randint(300, 1000)
                self.agent.scroll_page(scroll_amount)
                time.sleep(1)
    
    def _visit_and_interact(self):
        """Visit a website and interact with it naturally"""
        website = self._get_random_website()

        self.logger.info(f"Visiting: {website}")

        if self.agent.visit_url(website):
            self.tracker.record_website_visit(website)

            # Initial page load pause (human-like)
            time.sleep(random.uniform(1.5, 3.0))

            # Random dwell time - longer for "interesting" pages
            activity_config = self.settings.get('activity', {})
            dwell_min = activity_config.get('page_dwell_min', 5)
            dwell_max = activity_config.get('page_dwell_max', 30)

            # Occasionally spend much longer (found something interesting)
            if random.random() < 0.15:  # 15% chance
                dwell_max = dwell_max * 2  # Double the time
                self.logger.debug("Extended visit - 'interesting' content")

            dwell_time = RandomnessGenerator.get_random_delay(dwell_min, dwell_max)

            # Deep interaction with the page
            self._interact_with_page()

            # Remaining dwell time for final "reading"
            remaining_time = dwell_time - 10  # Account for interaction time
            if remaining_time > 0:
                time.sleep(remaining_time)
    
    def _perform_search(self):
        """Perform a random search on a search engine"""
        search_engines = [
            "https://www.google.com",
            "https://www.bing.com",
            "https://duckduckgo.com",
        ]
        
        engine = random.choice(search_engines)
        query = self._get_random_query()
        
        self.logger.info(f"Searching: '{query}' on {engine}")
        
        if self.agent.visit_url(engine):
            if self.agent.fill_search_form(query):
                self.tracker.record_search(query)
                
                # Dwell on search results
                dwell_time = RandomnessGenerator.get_random_delay(10, 20)
                self._interact_with_page()
                time.sleep(dwell_time - 5)
    
    def _session_expired(self) -> bool:
        """Check if session duration has expired"""
        session_duration = self.settings.get('service', {}).get('session_duration', 0)
        
        if session_duration == 0:  # Infinite session
            return False
        
        elapsed = (datetime.now() - self.start_time).total_seconds() / 60
        return elapsed >= session_duration
    
    def start_session(self, duration_minutes: int = 0):
        """Start a decoy activity session"""
        try:
            self.logger.info("="*60)
            self.logger.info("STARTING DECOY SERVICE SESSION")
            self.logger.info("="*60)
            
            # Create browser agent
            self.agent = create_agent(self.logger, self.settings)
            
            # Open browser
            headless = self.settings.get('browser', {}).get('headless', True)
            if not self.agent.open_browser(headless=headless):
                self.logger.error("Failed to open browser")
                return False
            
            self.running = True
            self.start_time = datetime.now()
            
            activity_config = self.settings.get('activity', {})
            click_interval_min = activity_config.get('click_interval_min', 2)
            click_interval_max = activity_config.get('click_interval_max', 8)
            
            activity_count = 0
            
            # Main activity loop
            while self.running:
                if self._session_expired():
                    self.logger.info("Session duration expired")
                    break
                
                # Random action: visit website or search
                if random.random() > 0.3:  # 70% website visits, 30% searches
                    self._visit_and_interact()
                else:
                    self._perform_search()
                
                activity_count += 1
                
                # Random interval between activities
                interval = RandomnessGenerator.get_random_delay(
                    click_interval_min,
                    click_interval_max
                )
                
                self.logger.info(f"Activity #{activity_count} complete. "
                               f"Waiting {interval:.1f}s before next activity...")
                time.sleep(interval)
            
            return True
            
        except KeyboardInterrupt:
            self.logger.info("Session interrupted by user")
            return True
        
        except Exception as e:
            self.logger.error(f"Error during session: {str(e)}", exc_info=True)
            return False
        
        finally:
            self.stop_session()
    
    def stop_session(self):
        """Stop the decoy session"""
        self.running = False

        if self.agent:
            self.agent.close_browser()

        self.tracker.print_summary()
        self.logger.info("="*60)
        self.logger.info("DECOY SERVICE SESSION ENDED")
        self.logger.info("="*60)

    def get_status(self) -> Dict[str, Any]:
        """Get current service status and stats for API/extension"""
        from datetime import datetime

        # Calculate session duration
        if self.tracker.stats.get('session_start'):
            session_duration = (datetime.now() - self.tracker.stats['session_start']).total_seconds() / 60
        else:
            session_duration = 0

        return {
            'stats': {
                'sitesVisited': self.tracker.stats.get('websites_visited', 0),
                'clicksMade': self.tracker.stats.get('clicks_made', 0),
                'searchesPerformed': self.tracker.stats.get('search_queries', 0),
                'sessionDurationMinutes': round(session_duration, 1)
            }
        }


def main():
    """Main entry point"""
    import sys
    import os
    
    # Get config directory from command line or use default
    config_dir = 'config'
    if len(sys.argv) > 1:
        config_dir = sys.argv[1]
    
    # Make sure we're using absolute paths
    if not os.path.isabs(config_dir):
        config_dir = os.path.join(os.path.dirname(__file__), config_dir)
    
    service = DecoyService(config_dir)
    service.start_session()


if __name__ == '__main__':
    main()
