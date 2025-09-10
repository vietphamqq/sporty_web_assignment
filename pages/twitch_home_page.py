"""
Twitch Home Page - Page Object Model
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from core.base.base_page import BasePage
from core.exceptions.framework_exceptions import ElementNotFoundException


class TwitchHomePage(BasePage):
    """Page Object for Twitch Home Page"""

    # Locators
    SEARCH_BUTTON = (By.XPATH, ".//a[./div/div[.='Browse']]")
    PROCEED_BUTTON = (By.XPATH, "//div[contains(text(), 'Proceed')]")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = "https://m.twitch.tv/"

    def navigate_to_home(self) -> None:
        """Navigate to Twitch home page"""
        self.navigate_to(self.url)
        self.wait_for_page_load()
        # Handle cookie consent modal if it appears
        self._dismiss_cookie_modal()

    def _dismiss_cookie_modal(self) -> None:
        """Dismiss the cookie consent modal if it appears"""
        try:
            # Check if the modal is present with a short timeout
            if self.is_element_present(self.PROCEED_BUTTON, timeout=3):
                self.click_element(self.PROCEED_BUTTON, timeout=5)
        except Exception:
            # Don't let cookie handling break the main test flow
            pass

    def click_search_button(self) -> bool:
        """Click the search button/icon

        Returns:
            bool: True if search button was clicked successfully, False otherwise
        """
        try:
            # Use flexible locators - try multiple selectors in sequence
            self.click_element(
                [
                    self.SEARCH_BUTTON,
                    (By.CSS_SELECTOR, "input[type='search']"),
                ],
                timeout=5,
            )
            return True
        except ElementNotFoundException:
            # Log the error but return False instead of raising exception
            # This maintains the current behavior of the test
            return False
