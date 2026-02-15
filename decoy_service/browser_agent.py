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
    def natural_scroll(self):
        """Scroll naturally like reading an article"""
        pass

    @abstractmethod
    def hover_element(self, element):
        """Hover over an element"""
        pass

    @abstractmethod
    def get_page_height(self) -> int:
        """Get total page height"""
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

    def natural_scroll(self):
        """Scroll naturally like reading an article - simulates human reading behavior"""
        try:
            page_height = self.get_page_height()
            current_position = 0

            # Scroll in smaller increments like reading
            while current_position < page_height * 0.8:  # Don't scroll to absolute bottom
                # Variable scroll amounts (reading different sections)
                scroll_amount = random.randint(150, 400)

                # Scroll down
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                current_position += scroll_amount

                # Reading pause - longer for larger scrolls (more content)
                reading_time = random.uniform(1.5, 4.0) if scroll_amount > 250 else random.uniform(0.8, 2.0)
                time.sleep(reading_time)

                # Occasionally scroll up a bit (re-reading)
                if random.random() < 0.15:  # 15% chance
                    scroll_up = random.randint(50, 150)
                    self.driver.execute_script(f"window.scrollBy(0, -{scroll_up});")
                    current_position -= scroll_up
                    time.sleep(random.uniform(0.5, 1.5))

                # Occasionally pause longer (looking at images, thinking)
                if random.random() < 0.2:  # 20% chance
                    time.sleep(random.uniform(2.0, 5.0))

            self.logger.debug("Natural scroll completed")
            return True

        except Exception as e:
            self.logger.debug(f"Natural scroll failed: {str(e)}")
            return False

    def hover_element(self, element):
        """Hover over an element to simulate mouse movement"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            action = ActionChains(self.driver)
            action.move_to_element(element).perform()
            time.sleep(random.uniform(0.3, 0.8))
            return True
        except Exception as e:
            self.logger.debug(f"Hover failed: {str(e)}")
            return False

    def get_page_height(self) -> int:
        """Get total page height"""
        try:
            return self.driver.execute_script("return document.body.scrollHeight")
        except:
            return 2000  # Default fallback

    def interact_with_media(self):
        """Interact with videos, images, and galleries on the page"""
        try:
            # Look for videos
            videos = self.driver.find_elements(self.By.TAG_NAME, 'video')
            if videos and random.random() < 0.3:  # 30% chance to interact with video
                video = random.choice(videos)
                self.hover_element(video)
                # Scroll to video
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", video)
                time.sleep(random.uniform(2, 5))  # "Watch" for a bit
                self.logger.debug("Interacted with video")

            # Look for image galleries
            images = self.driver.find_elements(self.By.TAG_NAME, 'img')
            if len(images) > 3:
                # "Look at" a few images
                num_images = min(random.randint(2, 4), len(images))
                for _ in range(num_images):
                    img = random.choice(images)
                    self.hover_element(img)
                    time.sleep(random.uniform(0.8, 2.0))
                self.logger.debug(f"Viewed {num_images} images")

            return True
        except Exception as e:
            self.logger.debug(f"Media interaction failed: {str(e)}")
            return False

    def handle_popups(self):
        """Try to close common popups, cookie banners, modals"""
        try:
            # Common close button selectors
            close_selectors = [
                "button[aria-label*='close' i]",
                "button[aria-label*='dismiss' i]",
                ".close", ".modal-close", "[class*='close']",
                "button:has-text('Accept')", "button:has-text('OK')",
                "[class*='cookie'] button", "[id*='cookie'] button"
            ]

            for selector in close_selectors:
                try:
                    elements = self.driver.find_elements(self.By.CSS_SELECTOR, selector)
                    if elements:
                        elements[0].click()
                        time.sleep(0.5)
                        self.logger.debug("Closed popup/banner")
                        return True
                except:
                    continue

            return False
        except Exception as e:
            self.logger.debug(f"Popup handling failed: {str(e)}")
            return False
    
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

    def natural_scroll(self):
        """Scroll naturally like reading an article"""
        try:
            page_height = self.get_page_height()
            current_position = 0

            while current_position < page_height * 0.8:
                scroll_amount = random.randint(150, 400)
                self.page.evaluate(f"window.scrollBy(0, {scroll_amount})")
                current_position += scroll_amount

                reading_time = random.uniform(1.5, 4.0) if scroll_amount > 250 else random.uniform(0.8, 2.0)
                time.sleep(reading_time)

                if random.random() < 0.15:
                    scroll_up = random.randint(50, 150)
                    self.page.evaluate(f"window.scrollBy(0, -{scroll_up})")
                    current_position -= scroll_up
                    time.sleep(random.uniform(0.5, 1.5))

                if random.random() < 0.2:
                    time.sleep(random.uniform(2.0, 5.0))

            self.logger.debug("Natural scroll completed")
            return True
        except Exception as e:
            self.logger.debug(f"Natural scroll failed: {str(e)}")
            return False

    def hover_element(self, element):
        """Hover over an element"""
        try:
            element.hover()
            time.sleep(random.uniform(0.3, 0.8))
            return True
        except Exception as e:
            self.logger.debug(f"Hover failed: {str(e)}")
            return False

    def get_page_height(self) -> int:
        """Get total page height"""
        try:
            return self.page.evaluate("document.body.scrollHeight")
        except:
            return 2000

    def interact_with_media(self):
        """Interact with videos and images"""
        try:
            videos = self.page.query_selector_all('video')
            if videos and random.random() < 0.3:
                video = random.choice(videos)
                video.scroll_into_view_if_needed()
                time.sleep(random.uniform(2, 5))
                self.logger.debug("Interacted with video")

            images = self.page.query_selector_all('img')
            if len(images) > 3:
                num_images = min(random.randint(2, 4), len(images))
                for _ in range(num_images):
                    img = random.choice(images)
                    self.hover_element(img)
                    time.sleep(random.uniform(0.8, 2.0))
                self.logger.debug(f"Viewed {num_images} images")

            return True
        except Exception as e:
            self.logger.debug(f"Media interaction failed: {str(e)}")
            return False

    def handle_popups(self):
        """Close common popups and cookie banners"""
        try:
            close_selectors = [
                "button[aria-label*='close' i]",
                ".close", ".modal-close",
                "button:has-text('Accept')", "button:has-text('OK')"
            ]

            for selector in close_selectors:
                try:
                    element = self.page.query_selector(selector)
                    if element:
                        element.click()
                        time.sleep(0.5)
                        self.logger.debug("Closed popup/banner")
                        return True
                except:
                    continue

            return False
        except Exception as e:
            self.logger.debug(f"Popup handling failed: {str(e)}")
            return False

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
