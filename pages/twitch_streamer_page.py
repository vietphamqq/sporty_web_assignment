"""
Twitch Streamer Page - Page Object Model
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from core.base.base_page import BasePage
from config.constants import TimeoutConstants


class TwitchStreamerPage(BasePage):
    """Page Object for Twitch Streamer Profile Page"""

    # Locators
    LOADING_SPINNER = (By.CSS_SELECTOR, "div[class^=ScLoadingSpinner]")
    FOLLOW_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Follow ']")
    ABOUT_MENU = (By.XPATH, ".//div[text()='About']")
    VIDEOS = (By.CSS_SELECTOR, "button[role='link']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def is_streamer_page_loaded(self) -> bool:
        """Check if streamer page is fully loaded"""
        try:
            # Use flexible locators to check for streamer page elements
            return (
                self.is_element_present(self.FOLLOW_BUTTON, timeout=TimeoutConstants.QUICK_WAIT)
                and self.is_element_present(self.ABOUT_MENU, timeout=TimeoutConstants.QUICK_WAIT)
                and self.is_element_present(self.VIDEOS, timeout=TimeoutConstants.QUICK_WAIT)
            )
        except Exception:
            return False

    def wait_for_streamer_page_load(self) -> bool:
        """Wait for stream content to load completely"""
        try:
            # Wait for page to load
            self.wait_for_page_load()
            return self.is_streamer_page_loaded()
        except:
            return False
