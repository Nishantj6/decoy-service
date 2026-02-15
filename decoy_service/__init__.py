"""
Decoy Service - Privacy Protection through Behavioral Obfuscation

A service that generates random browsing activity to confuse behavioral advertisers
and protect privacy from profiling.

Main components:
  - DecoyService: Main orchestrator
  - BrowserAgent: Browser automation (Selenium/Playwright)
  - DecoyScheduler: Schedule sessions
  - ActivityTracker: Track and report activity
"""

__version__ = "1.0.0"
__author__ = "Privacy Protector"
__license__ = "MIT"

try:
    from decoy_service import DecoyService
    from scheduler import DecoyScheduler
    from .utils import Logger, ConfigManager, ActivityTracker, RandomnessGenerator
    from browser_agent import BrowserAgent, SeleniumAgent, PlaywrightAgent
except ImportError:
    # Module may be run directly without imports
    pass

__all__ = [
    'DecoyService',
    'DecoyScheduler',
    'Logger',
    'ConfigManager',
    'ActivityTracker',
    'RandomnessGenerator',
    'BrowserAgent',
    'SeleniumAgent',
    'PlaywrightAgent',
]
