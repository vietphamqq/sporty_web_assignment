"""
Twitch Streamer Page - Page Object Model
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from core.base.base_page import BasePage


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
                self.is_element_present(self.FOLLOW_BUTTON, timeout=5)
                and self.is_element_present(self.ABOUT_MENU, timeout=5)
                and self.is_element_present(self.VIDEOS, timeout=5)
            )
        except:
            return False

    def wait_for_streamer_page_load(self, timeout: int = 15) -> bool:
        """Wait for stream content to load completely"""
        try:
            # Wait for page to load
            self.wait_for_page_load()
            return self.is_streamer_page_loaded()
        except:
            return False
