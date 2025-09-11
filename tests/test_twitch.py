"""
Twitch Web automation test using Design Patterns
- Page Object Model (POM)
- Factory Pattern
"""

from core.base.test_base import BaseTest
from pages.twitch_home_page import TwitchHomePage


class TestTwitch(BaseTest):
    """Twitch Web automation test using Page Object Model"""

    def _prepare_test_data(self):
        """Setup test data for Twitch streamer test"""
        # We can use self.test_data["search_term"] = "Starcraft II" instead of self.search_term = "Starcraft II"
        # But we will use self.search_term = "Starcraft II" for now
        self.search_term = "Starcraft II"
        self.test_data["search_term"] = self.search_term


    def test_twitch_search_and_navigate_to_streamer(self, driver):
        """Test: Go to Twitch, search for Starcraft II, scroll, select streamer, and take screenshot"""
        # Initialize the home page
        self.home_page = TwitchHomePage(driver)
        
        self.log_test_step("Starting Twitch test")

        # Step 1: Go to Twitch
        self.log_test_step("Step 1: Navigate to Twitch")
        self.home_page.navigate_to_home()

        # Verify we're on Twitch
        current_url = driver.current_url
        assert (
            "m.twitch.tv" in current_url
        ), f"Expected to be on Twitch, but current URL is: {current_url}"

        # Step 2: Click search button
        self.log_test_step("Step 2: Click search button")
        self.search_page = self.home_page.click_search_button()
        assert self.search_page, "Failed to click search button"

        # Take screenshot after clicking search button
        step2_screenshot = self.search_page.take_screenshot("step2_click_search_button.png")
        self.log_test_step("Step 2 completed - Screenshot taken", {"screenshot": step2_screenshot})

        # Step 3: Input "Starcraft II"
        self.log_test_step("Step 3: Input search term 'Starcraft II'")
        search_successful = self.search_page.search_for_term(self.search_term)
        assert search_successful, "Failed to input search term"

        # Take screenshot after inputting search term
        step3_screenshot = self.search_page.take_screenshot("step3_input_search_term.png")
        self.log_test_step("Step 3 completed - Screenshot taken", {"screenshot": step3_screenshot})

        # Step 3.5: Select Starcraft II first search result
        self.log_test_step(
            "Step 3.5: Select 'Starcraft II' from search results if available"
        )
        search_results = self.search_page.get_search_category_results()
        assert len(search_results) > 0, "No search results found"
        search_results[0].click()

        # Take screenshot after selecting search result
        step35_screenshot = self.search_page.take_screenshot("step35_select_search_result.png")
        self.log_test_step("Step 3.5 completed - Screenshot taken", {"screenshot": step35_screenshot})

        # Step 4: Scroll down 2 times
        self.log_test_step("Step 4: Scroll down 2 times")
        self.search_page.wait_for_search_streamer_results()
        self.search_page.scroll_down(2)

        # Take screenshot after scrolling down
        step4_screenshot = self.search_page.take_screenshot("step4_scroll_down.png")
        self.log_test_step("Step 4 completed - Screenshot taken", {"screenshot": step4_screenshot})

        # Step 5: Select one streamer
        self.log_test_step("Step 5: Select one streamer from search results")
        self.streamer_page = self.search_page.select_first_streamer()
        assert self.streamer_page, "Failed to select streamer, no streamer found"

        # Take screenshot after selecting streamer
        step5_screenshot = self.streamer_page.take_screenshot("step5_select_streamer.png")
        self.log_test_step("Step 5 completed - Screenshot taken", {"screenshot": step5_screenshot})

        # Step 6: Wait until all is loaded then take screenshot
        self.log_test_step(
            "Step 6: Wait for streamer page to load completely and take screenshot"
        )

        # Wait for streamer page to load completely
        streamer_loaded = self.streamer_page.wait_for_streamer_page_load()
        assert streamer_loaded, "Streamer page failed to load completely"

        # Take screenshot after page load
        step6_screenshot = self.streamer_page.take_screenshot("step6_page_loaded.png")
        self.log_test_step("Step 6 completed - Screenshot taken", {"screenshot": step6_screenshot})
        assert step6_screenshot is not None, "Screenshot was not taken successfully"

        # Take final screenshot (keeping the original name for backward compatibility)
        screenshot_path = self.streamer_page.take_screenshot("twitch_streamer.png")
        assert screenshot_path is not None, "Final screenshot was not taken successfully"

        self.log_test_step(
            "Test completed successfully",
            {
                "search_term": self.search_term,
                "final_url": self.streamer_page.current_url,
                "screenshot": screenshot_path,
            },
        )
