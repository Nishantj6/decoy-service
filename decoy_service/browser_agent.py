"""
Browser automation module using Selenium and Playwright
Handles website navigation, clicking, form filling, etc.
"""

import logging
import time
import random
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod


class BrowserAgent(ABC):
    """Abstract base class for browser agents"""
    
    def __init__(self, logger: logging.Logger, config: Dict[str, Any]):
        self.logger = logger
        self.config = config
        self.browser = None
        self.driver = None
    
    @abstractmethod
    def open_browser(self, headless: bool = True):
        """Open browser instance"""
        pass
    
    @abstractmethod
    def visit_url(self, url: str) -> bool:
        """Visit a URL and return success status"""
        pass
    
    @abstractmethod
    def get_clickable_elements(self, max_elements: int = 10) -> List:
        """Get clickable elements on the page"""
        pass
    
    @abstractmethod
    def random_click(self) -> bool:
        """Perform a random click on the page"""
        pass
    
    @abstractmethod
    def scroll_page(self, amount: int = 500):
        """Scroll the page"""
        pass
    
    @abstractmethod
    def close_browser(self):
        """Close browser instance"""
        pass


class SeleniumAgent(BrowserAgent):
    """Browser agent using Selenium WebDriver"""
    
    def __init__(self, logger: logging.Logger, config: Dict[str, Any]):
        super().__init__(logger, config)
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            self.webdriver = webdriver
            self.By = By
            self.WebDriverWait = WebDriverWait
        except ImportError:
            raise ImportError("Selenium not installed. Run: pip install selenium")
    
    def open_browser(self, headless: bool = True):
        """Open Chrome browser with Selenium"""
        try:
            options = self.webdriver.ChromeOptions()
            
            if headless:
                options.add_argument('--headless')
            
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument(f'user-agent={self._get_user_agent()}')
            
            self.driver = self.webdriver.Chrome(options=options)
            self.logger.info("Chrome browser opened")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to open browser: {str(e)}")
            return False
    
    def visit_url(self, url: str, timeout: int = 10) -> bool:
        """Visit a URL"""
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            
            self.driver.get(url)
            time.sleep(2)  # Wait for page load
            self.logger.info(f"Navigated to: {url}")
            return True
            
        except Exception as e:
            self.logger.warning(f"Failed to visit {url}: {str(e)}")
            return False
    
    def get_clickable_elements(self, max_elements: int = 10) -> List:
        """Get clickable elements"""
        try:
            elements = self.driver.find_elements(self.By.XPATH, 
                "//a | //button | //*[contains(@onclick, '')] | //input[@type='button']"
            )
            return elements[:max_elements]
        except Exception as e:
            self.logger.debug(f"Could not find clickable elements: {str(e)}")
            return []
    
    def random_click(self) -> bool:
        """Perform random click"""
        try:
            elements = self.get_clickable_elements(max_elements=20)
            if not elements:
                return False
            
            element = random.choice(elements)
            element.click()
            time.sleep(random.uniform(1, 3))
            self.logger.debug("Random click performed")
            return True
            
        except Exception as e:
            self.logger.debug(f"Click failed: {str(e)}")
            return False
    
    def scroll_page(self, amount: int = 500):
        """Scroll page"""
        try:
            self.driver.execute_script(f"window.scrollBy(0, {amount});")
            self.logger.debug(f"Scrolled {amount}px")
        except Exception as e:
            self.logger.debug(f"Scroll failed: {str(e)}")
    
    def fill_search_form(self, query: str) -> bool:
        """Find and fill a search form"""
        try:
            # Try common search form selectors
            selectors = [
                "input[name='q']",
                "input[type='search']",
                "input[placeholder*='search' i]",
                "input[placeholder*='Search' i]",
            ]
            
            for selector in selectors:
                try:
                    search_box = self.driver.find_element(self.By.CSS_SELECTOR, selector)
                    search_box.clear()
                    search_box.send_keys(query)
                    time.sleep(0.5)
                    search_box.send_keys("\n")  # Press Enter
                    time.sleep(2)
                    self.logger.info(f"Searched for: {query}")
                    return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.logger.debug(f"Search form fill failed: {str(e)}")
            return False
    
    def close_browser(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed")
    
    def _get_user_agent(self) -> str:
        """Get user agent from config or use default"""
        from .utils import RandomnessGenerator
        if self.config.get('browser', {}).get('rotate_user_agents'):
            return RandomnessGenerator.get_random_user_agent()
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


class PlaywrightAgent(BrowserAgent):
    """Browser agent using Playwright"""
    
    def __init__(self, logger: logging.Logger, config: Dict[str, Any]):
        super().__init__(logger, config)
        try:
            from playwright.sync_api import sync_playwright
            self.playwright = sync_playwright()
        except ImportError:
            raise ImportError("Playwright not installed. Run: pip install playwright")
    
    def open_browser(self, headless: bool = True):
        """Open browser with Playwright"""
        try:
            self.browser_context = self.playwright.start()
            self.browser = self.browser_context.chromium.launch(headless=headless)
            self.page = self.browser.new_page()
            self.logger.info("Playwright browser opened")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open Playwright browser: {str(e)}")
            return False
    
    def visit_url(self, url: str) -> bool:
        """Visit URL with Playwright"""
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            
            self.page.goto(url, wait_until='load')
            time.sleep(2)
            self.logger.info(f"Navigated to: {url}")
            return True
        except Exception as e:
            self.logger.warning(f"Failed to visit {url}: {str(e)}")
            return False
    
    def get_clickable_elements(self, max_elements: int = 10) -> List:
        """Get clickable elements"""
        try:
            elements = self.page.query_selector_all('a, button, [onclick], input[type="button"]')
            return elements[:max_elements]
        except Exception as e:
            self.logger.debug(f"Could not find clickable elements: {str(e)}")
            return []
    
    def random_click(self) -> bool:
        """Perform random click"""
        try:
            elements = self.get_clickable_elements(max_elements=20)
            if not elements:
                return False
            
            element = random.choice(elements)
            element.click()
            time.sleep(random.uniform(1, 3))
            self.logger.debug("Random click performed")
            return True
        except Exception as e:
            self.logger.debug(f"Click failed: {str(e)}")
            return False
    
    def scroll_page(self, amount: int = 500):
        """Scroll page"""
        try:
            self.page.evaluate(f"window.scrollBy(0, {amount})")
            self.logger.debug(f"Scrolled {amount}px")
        except Exception as e:
            self.logger.debug(f"Scroll failed: {str(e)}")
    
    def close_browser(self):
        """Close browser"""
        try:
            if self.page:
                self.page.close()
            if self.browser:
                self.browser.close()
            if self.browser_context:
                self.browser_context.stop()
            self.logger.info("Playwright browser closed")
        except Exception as e:
            self.logger.error(f"Error closing browser: {str(e)}")


def create_agent(logger: logging.Logger, config: Dict[str, Any]) -> BrowserAgent:
    """Factory function to create appropriate browser agent"""
    browser_type = config.get('browser', {}).get('type', 'selenium').lower()
    
    if browser_type == 'playwright':
        return PlaywrightAgent(logger, config)
    else:
        return SeleniumAgent(logger, config)


__all__ = [
    'BrowserAgent',
    'SeleniumAgent',
    'PlaywrightAgent',
    'create_agent',
]
