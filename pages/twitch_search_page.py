"""
Twitch Search Page - Page Object Model
"""

from typing import List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from core.base.base_page import BasePage
from core.exceptions.framework_exceptions import ElementNotFoundException
from config.constants import TimeoutConstants
from pages.twitch_streamer_page import TwitchStreamerPage


class TwitchSearchPage(BasePage):
    """Page Object for Twitch Search Results Page"""

    # Locators
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type=search]")
    SEARCH_RESULTS = (By.CSS_SELECTOR, "div > ul > li img")
    STREAMER_LINK = (By.CSS_SELECTOR, "div[class^= ScTextWrapper] > div > a")
    STREAMER_PREVIEW = (By.CSS_SELECTOR, "article img[class='tw-image']")
    ALL_LINKS = (By.TAG_NAME, "a")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def search_for_term(self, search_term: str) -> bool:
        """Perform search for the given term

        Args:
            search_term: The term to search for

        Returns:
            bool: True if search was performed successfully, False otherwise
        """
        try:
            # Find search input using flexible locators
            search_input = self.find_element(
                [
                    self.SEARCH_INPUT,
                    (By.CSS_SELECTOR, "input[type=search]"),
                    (By.CSS_SELECTOR, "input[placeholder*='Search']"),
                ],
                timeout=TimeoutConstants.QUICK_WAIT,
            )

            # Clear and input search term
            search_input.clear()
            search_input.send_keys(search_term)
            return True
        except ElementNotFoundException:
            # Log the error but return False instead of raising exception
            # This maintains the current behavior of the test
            return False

    def get_search_category_results(self) -> List[WebElement]:
        """Get all search result elements

        Returns:
            list: List of search result elements, empty list if none found
        """
        try:
            # Use flexible locators to find search results
            elements = self.find_elements(self.SEARCH_RESULTS)
            return elements if elements else []
        except ElementNotFoundException:
            return []

    def wait_for_search_streamer_results(self) -> bool:
        self.wait_for_page_load()
        return self.is_element_present(self.STREAMER_LINK) and self.is_element_present(
            self.STREAMER_PREVIEW
        )

    def select_first_streamer(self) -> Union[TwitchStreamerPage, bool]:
        """Select the first available streamer from search results

        Returns:
            TwitchStreamerPage: Instance of TwitchStreamerPage if successful
            bool: False if no streamer found or error occurs
        """
        try:
            # Use flexible locators to find and click first streamer
            streamer_elements = [
                x
                for x in self.find_elements(self.STREAMER_LINK)
                if self.is_element_within_viewport(x)
            ]

            if streamer_elements:
                streamer_elements[0].click()
                return TwitchStreamerPage(self.driver)
            return False
        except ElementNotFoundException:
            return False

    def scroll_down(self, times: int = 1) -> None:
        """Scroll down the specified number of times"""
        # time.sleep(2)  # Wait for any dynamic content to load
        for i in range(times):
            self.scroll_down_in_viewport()
            self.wait_for_page_load()
