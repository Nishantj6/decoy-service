"""
Decoy Service - Privacy Protection through Behavioral Obfuscation
Generates random browsing activity to confuse advertising profilers
"""

import logging
import random
import time
from datetime import datetime
from typing import List, Dict, Any
import yaml
import os
from pathlib import Path


class Logger:
    """Centralized logging setup"""
    
    @staticmethod
    def setup_logging(config: Dict[str, Any]) -> logging.Logger:
        """Configure logging based on settings"""
        log_config = config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        log_file = log_config.get('log_file', 'logs/decoy_service.log')
        
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        logger = logging.getLogger('DecoyService')
        logger.setLevel(log_level)
        
        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(log_level)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger


class ConfigManager:
    """Load and manage configuration files"""
    
    def __init__(self, config_dir: str = 'config'):
        self.config_dir = config_dir
        self.settings = {}
        self.websites = {}
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings.yaml"""
        settings_file = os.path.join(self.config_dir, 'settings.yaml')
        
        if not os.path.exists(settings_file):
            raise FileNotFoundError(f"Settings file not found: {settings_file}")
        
        with open(settings_file, 'r') as f:
            self.settings = yaml.safe_load(f)
        
        return self.settings
    
    def load_websites(self) -> Dict[str, List[str]]:
        """Load websites.yaml"""
        websites_file = os.path.join(self.config_dir, 'websites.yaml')
        
        if not os.path.exists(websites_file):
            raise FileNotFoundError(f"Websites file not found: {websites_file}")
        
        with open(websites_file, 'r') as f:
            data = yaml.safe_load(f)
            self.websites = data.get('categories', {})
        
        return self.websites
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a nested config value"""
        keys = key.split('.')
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default


class ActivityTracker:
    """Track and log decoy activities"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.stats = {
            'websites_visited': 0,
            'clicks_made': 0,
            'forms_filled': 0,
            'search_queries': 0,
            'session_start': datetime.now(),
            'total_time_seconds': 0,
        }
    
    def record_website_visit(self, url: str):
        """Record a website visit"""
        self.stats['websites_visited'] += 1
        self.logger.info(f"Visited: {url}")
    
    def record_click(self, description: str = ""):
        """Record a click action"""
        self.stats['clicks_made'] += 1
        self.logger.debug(f"Clicked: {description}")
    
    def record_search(self, query: str):
        """Record a search query"""
        self.stats['search_queries'] += 1
        self.logger.info(f"Searched: {query}")
    
    def record_form_fill(self):
        """Record form interaction"""
        self.stats['forms_filled'] += 1
        self.logger.debug("Form filled")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get activity summary"""
        elapsed = (datetime.now() - self.stats['session_start']).total_seconds()
        self.stats['total_time_seconds'] = elapsed
        
        return {
            'session_duration_minutes': elapsed / 60,
            'websites_visited': self.stats['websites_visited'],
            'total_clicks': self.stats['clicks_made'],
            'search_queries': self.stats['search_queries'],
            'forms_filled': self.stats['forms_filled'],
        }
    
    def print_summary(self):
        """Print activity summary"""
        summary = self.get_summary()
        self.logger.info("\n" + "="*50)
        self.logger.info("DECOY ACTIVITY SUMMARY")
        self.logger.info("="*50)
        for key, value in summary.items():
            self.logger.info(f"{key}: {value}")
        self.logger.info("="*50)


class RandomnessGenerator:
    """Generate random but realistic browsing patterns"""
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    ]
    
    @staticmethod
    def get_random_user_agent() -> str:
        """Return a random user agent string"""
        return random.choice(RandomnessGenerator.USER_AGENTS)
    
    @staticmethod
    def get_random_delay(min_val: float, max_val: float) -> float:
        """Get a random delay with normal-ish distribution"""
        # Use triangular distribution for more realistic delays
        return random.triangular(min_val, max_val, (min_val + max_val) / 2)
    
    @staticmethod
    def get_random_element(items: List[str]) -> str:
        """Get random element from list"""
        return random.choice(items)
    
    @staticmethod
    def shuffle_list(items: List[str]) -> List[str]:
        """Shuffle a list"""
        shuffled = items.copy()
        random.shuffle(shuffled)
        return shuffled


# Module initialization
__all__ = [
    'Logger',
    'ConfigManager',
    'ActivityTracker',
    'RandomnessGenerator',
]
