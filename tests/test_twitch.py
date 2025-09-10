"""
Twitch Web automation test using Design Patterns
- Page Object Model (POM)
- Factory Pattern
"""

from core.base.test_base import TestBase
from core.driver_manager import DriverManager
from core.exceptions.framework_exceptions import DriverException
from pages.twitch_home_page import TwitchHomePage


class TestTwitch(TestBase):
    """Twitch Web automation test using Page Object Model"""

    def _setup_test_data(self):
        """Setup test data for Twitch streamer test"""
        self.search_term = "Starcraft II"

    def _setup_test_environment(self):
        """Setup Web test environment using Driver Manager (Factory Pattern)"""
        try:
            # Setup web driver
            self.driver = DriverManager.get_mobile_driver()

            # Initialize page objects
            self.home_page = TwitchHomePage(self.driver)

        except DriverException as e:
            self.logger.error(f"Failed to create mobile driver: {e}")
            raise

    def _cleanup_test_environment(self):
        """Cleanup Web test environment"""
        DriverManager.quit_driver()  # Now worker-aware

    def test_twitch_search_and_navigate_to_streamer(self):
        """Test: Go to Twitch, search for Starcraft II, scroll, select streamer, and take screenshot"""
        self.log_test_step("Starting Twitch test")

        # Step 1: Go to Twitch
        self.log_test_step("Step 1: Navigate to Twitch")
        self.home_page.navigate_to_home()

        # Verify we're on Twitch
        current_url = self.driver.current_url
        assert (
            "m.twitch.tv" in current_url
        ), f"Expected to be on Twitch, but current URL is: {current_url}"

        # Step 2: Click search button
        self.log_test_step("Step 2: Click search button")
        self.search_page = self.home_page.click_search_button()
        assert self.search_page, "Failed to click search button"

        # Step 3: Input "Starcraft II"
        self.log_test_step("Step 3: Input search term 'Starcraft II'")
        search_successful = self.search_page.search_for_term(self.search_term)
        assert search_successful, "Failed to input search term"

        # Step 3.5: Select Starcraft II first search result
        self.log_test_step(
            "Step 3.5: Select 'Starcraft II' from search results if available"
        )
        search_results = self.search_page.get_search_category_results()
        assert len(search_results) > 0, "No search results found"
        search_results[0].click()

        # Step 4: Scroll down 2 times
        self.log_test_step("Step 4: Scroll down 2 times")
        self.search_page.wait_for_search_streamer_results()
        self.search_page.scroll_down(2)

        # Step 5: Select one streamer
        self.log_test_step("Step 5: Select one streamer from search results")
        self.streamer_page = self.search_page.select_first_streamer()
        assert self.streamer_page, "Failed to select streamer, no streamer found"

        # Step 6: Wait until all is loaded then take screenshot
        self.log_test_step(
            "Step 6: Wait for streamer page to load completely and take screenshot"
        )

        # Wait for streamer page to load completely
        streamer_loaded = self.streamer_page.wait_for_streamer_page_load()
        assert streamer_loaded, "Streamer page failed to load completely"

        # Take screenshot
        screenshot_path = self.streamer_page.take_screenshot("twitch_streamer.png")
        assert screenshot_path is not None, "Screenshot was not taken successfully"

        self.log_test_step(
            "Test completed successfully",
            {
                "search_term": self.search_term,
                "final_url": self.streamer_page.current_url,
                "screenshot": screenshot_path,
            },
        )
