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
    PROCEED_BUTTON = (By.XPATH, "//*[contains(text(), 'Proceed')]")


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
            # Save page source for debugging in CI
            self._save_page_source_for_debug("before_cookie_check")
            
            # Check if the modal is present with a short timeout
            if self.is_element_present(self.PROCEED_BUTTON, timeout=3):
                # Save page source when modal is detected
                self._save_page_source_for_debug("cookie_modal_detected")
                print("🍪 Cookie consent modal detected, clicking Proceed button")
                self.click_element(self.PROCEED_BUTTON, timeout=5)
                print("✅ Cookie consent modal dismissed successfully")
            else:
                print("ℹ️  No cookie modal detected")
        except Exception as e:
            # Save page source on error for debugging
            self._save_page_source_for_debug("cookie_modal_error")
            print(f"⚠️  Cookie modal handling failed: {e}")
            # Don't let cookie handling break the main test flow
            pass

    def _save_page_source_for_debug(self, suffix: str) -> None:
        """Save page source to file for CI debugging"""
        try:
            import os
            import time
            
            # Create debug directory
            debug_dir = os.path.join("reports", "debug")
            os.makedirs(debug_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = int(time.time() * 1000)
            filename = f"page_source_{suffix}_{timestamp}.html"
            filepath = os.path.join(debug_dir, filename)
            
            # Save page source
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            
            print(f"📄 Page source saved: {filepath}")
            
        except Exception as e:
            print(f"Failed to save page source: {e}")

    def click_search_button(self) -> bool:
        """Click the search button/icon
        
        Returns:
            bool: True if search button was clicked successfully, False otherwise
        """
        try:
            # Use flexible locators - try multiple selectors in sequence
            self.click_element([
                self.SEARCH_BUTTON,
                (By.CSS_SELECTOR, "input[type='search']"),
            ], timeout=5)
            return True
        except ElementNotFoundException:
            # Log the error but return False instead of raising exception
            # This maintains the current behavior of the test
            return False
