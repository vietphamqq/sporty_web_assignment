"""
Twitch Home Page - Page Object Model
"""
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from core.base.base_page import BasePage
from core.exceptions.framework_exceptions import ElementNotFoundException
from config.constants import TimeoutConstants, URLConstants, BrowserConstants
from pages.twitch_search_page import TwitchSearchPage


class TwitchHomePage(BasePage):
    """Page Object for Twitch Home Page"""

    # Locators
    SEARCH_BUTTON = (By.XPATH, ".//a[./div/div[.='Browse']]")
    PROCEED_BUTTON = (By.XPATH, "//div[contains(text(), 'Proceed')]")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        # Get URL from environment configuration
        from config.settings import Settings
        self.url = Settings.get_test_url(URLConstants.HOME_URL_KEY)

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
            self.driver.implicitly_wait(TimeoutConstants.ELEMENT_CHECK_TIMEOUT)
            if self.is_element_present(self.PROCEED_BUTTON, timeout=TimeoutConstants.ELEMENT_CHECK_TIMEOUT):
                self.click_element(self.PROCEED_BUTTON, timeout=TimeoutConstants.QUICK_WAIT)
        except Exception:
            # Don't let cookie handling break the main test flow
            pass
        finally:
            self.driver.implicitly_wait(BrowserConstants.CHROME_IMPLICIT_WAIT)

    def click_search_button(self) -> Union[TwitchSearchPage, bool]:
        """Click the search button/icon

        Returns:
            TwitchSearchPage: Instance of TwitchSearchPage if navigation is successful
            bool: False if the search button is not found
        """
        try:
            # Use flexible locators - try multiple selectors in sequence
            self.click_element(
                [
                    self.SEARCH_BUTTON,
                    (By.CSS_SELECTOR, "input[type='search']"),
                ],
                timeout=TimeoutConstants.QUICK_WAIT,
            )
            return TwitchSearchPage(self.driver)
        except ElementNotFoundException:
            # Log the error but return False instead of raising exception
            # This maintains the current behavior of the test
            return False
