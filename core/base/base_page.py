"""
Base page class for Web automation using Page Object Model
"""

import time
from typing import Any, List, Optional, Tuple, Union

from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import Settings
from config.constants import TimeoutConstants, ReportConstants
from core.exceptions.framework_exceptions import (ElementNotFoundException,
                                                  PageNotFoundException)
from core.exceptions.framework_exceptions import \
    TimeoutException as SportyTimeoutException


class BasePage:
    """Base page class with common functionality for all pages"""

    def __init__(self, driver=None):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, Settings.BROWSER.explicit_wait)

    def navigate_to(self, url: str) -> None:
        """Navigate to a specific URL

        Args:
            url: URL to navigate to

        Raises:
            PageNotFoundException: If page fails to load
        """
        try:
            self.driver.get(url)
            if not self._wait_for_page_load():
                raise PageNotFoundException(url, "Page failed to load completely")
        except WebDriverException as e:
            raise PageNotFoundException(url, f"Failed to navigate to page: {str(e)}")

    def get_title(self) -> str:
        """Get the current page title"""
        return self.driver.title

    @property
    def current_url(self) -> str:
        """Get the current URL"""
        return self.driver.current_url

    def find_element(
        self, locator: Union[Tuple[str, str], List[Tuple[str, str]]], timeout: int = 5
    ) -> WebElement:
        """Find a single element with explicit wait

        Args:
            locator: Single locator tuple (strategy, value) or list of locator tuples to try in sequence
            timeout: Optional timeout override

        Returns:
            WebElement: The first element found

        Raises:
            ElementNotFoundException: If no element is found with any of the provided locators
        """
        # Convert single locator to list for uniform handling
        locators = [locator] if isinstance(locator, tuple) else locator

        if not locators:
            raise ElementNotFoundException([], "No locators provided")

        wait_time = timeout or Settings.BROWSER.explicit_wait
        wait = WebDriverWait(self.driver, wait_time)

        for i, loc in enumerate(locators):
            try:
                return wait.until(EC.presence_of_element_located(loc))
            except TimeoutException:
                # If this is not the last locator, continue trying
                if i < len(locators) - 1:
                    continue

        # If we get here, all locators failed
        raise ElementNotFoundException(locators, timeout=wait_time)

    def find_elements(
        self, locator: Union[Tuple[str, str], List[Tuple[str, str]]], timeout: int = 5
    ) -> List[WebElement]:
        """Find multiple elements

        Args:
            locator: Single locator tuple (strategy, value) or list of locator tuples to try in sequence
            timeout: Optional timeout override

        Returns:
            List[WebElement]: List of elements found (empty if none found)
        """
        # Convert single locator to list for uniform handling
        locators = [locator] if isinstance(locator, tuple) else locator

        if not locators:
            return []

        wait_time = timeout or Settings.BROWSER.explicit_wait
        wait = WebDriverWait(self.driver, wait_time)

        for loc in locators:
            try:
                wait.until(EC.presence_of_element_located(loc))
                return self.driver.find_elements(*loc)
            except TimeoutException:
                continue

        return []

    def click_element(
        self, locator: Union[Tuple[str, str], List[Tuple[str, str]]], timeout: int = 5
    ) -> None:
        """Click an element with explicit wait

        Args:
            locator: Single locator tuple (strategy, value) or list of locator tuples to try in sequence
            timeout: Optional timeout override

        Raises:
            ElementNotFoundException: If no clickable element is found with any of the provided locators
        """
        # Convert single locator to list for uniform handling
        locators = [locator] if isinstance(locator, tuple) else locator

        if not locators:
            raise ElementNotFoundException(
                [], "No locators provided for click operation"
            )

        wait_time = timeout or Settings.BROWSER.explicit_wait
        wait = WebDriverWait(self.driver, wait_time)

        for i, loc in enumerate(locators):
            try:
                element = wait.until(EC.element_to_be_clickable(loc))
                element.click()
                return
            except TimeoutException:
                # If this is not the last locator, continue trying
                if i < len(locators) - 1:
                    continue

        # If we get here, all locators failed
        raise ElementNotFoundException(
            locators, "Clickable element not found", wait_time
        )

    def send_keys(
        self,
        locator: Union[Tuple[str, str], List[Tuple[str, str]]],
        text: str,
        clear_first: bool = True,
    ) -> None:
        """Send keys to an element

        Args:
            locator: Single locator tuple (strategy, value) or list of locator tuples to try in sequence
            text: Text to send to the element
            clear_first: Whether to clear the element before sending keys
        """
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Union[Tuple[str, str], List[Tuple[str, str]]]) -> str:
        """Get text from an element

        Args:
            locator: Single locator tuple (strategy, value) or list of locator tuples to try in sequence

        Returns:
            str: Text content of the element
        """
        element = self.find_element(locator)
        return element.text

    def get_attribute(
        self, locator: Union[Tuple[str, str], List[Tuple[str, str]]], attribute: str
    ) -> str:
        """Get attribute value from an element

        Args:
            locator: Single locator tuple (strategy, value) or list of locator tuples to try in sequence
            attribute: Name of the attribute to get

        Returns:
            str: Value of the attribute
        """
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    def is_element_present(
        self, locator: Union[Tuple[str, str], List[Tuple[str, str]]], timeout: int = 5
    ) -> bool:
        """Check if element is present

        Args:
            locator: Single locator tuple (strategy, value) or list of locator tuples to try in sequence
            timeout: Timeout for the check

        Returns:
            bool: True if any element is found, False otherwise
        """
        # Convert single locator to list for uniform handling
        locators = [locator] if isinstance(locator, tuple) else locator

        if not locators:
            return False

        wait = WebDriverWait(self.driver, timeout)

        for loc in locators:
            try:
                wait.until(EC.presence_of_element_located(loc))
                return True
            except TimeoutException:
                continue

        return False

    def is_element_not_present(
        self, locator: Union[Tuple[str, str], List[Tuple[str, str]]], timeout: int = 5
    ) -> bool:
        """Check if element is not present

        Args:
            locator: Single locator tuple (strategy, value) or list of locator tuples to try in sequence
            timeout: Timeout for the check

        Returns:
            bool: True if no elements are found, False otherwise
        """
        # Convert single locator to list for uniform handling
        locators = [locator] if isinstance(locator, tuple) else locator

        if not locators:
            return True

        wait = WebDriverWait(self.driver, timeout)

        for loc in locators:
            try:
                wait.until(EC.invisibility_of_element_located(loc))
                return True
            except TimeoutException:
                continue

        return False

    def is_element_visible(
        self, locator: Union[Tuple[str, str], List[Tuple[str, str]]], timeout: int = 5
    ) -> bool:
        """Check if element is visible

        Args:
            locator: Single locator tuple (strategy, value) or list of locator tuples to try in sequence
            timeout: Timeout for the check

        Returns:
            bool: True if any element is visible, False otherwise
        """
        # Convert single locator to list for uniform handling
        locators = [locator] if isinstance(locator, tuple) else locator

        if not locators:
            return False

        wait = WebDriverWait(self.driver, timeout)

        for loc in locators:
            try:
                wait.until(EC.visibility_of_element_located(loc))
                return True
            except TimeoutException:
                continue

        return False

    def is_element_clickable(
        self, locator: Union[Tuple[str, str], List[Tuple[str, str]]], timeout: int = 5
    ) -> bool:
        """Check if element is clickable

        Args:
            locator: Single locator tuple (strategy, value) or list of locator tuples to try in sequence
            timeout: Timeout for the check

        Returns:
            bool: True if any element is clickable, False otherwise
        """
        # Convert single locator to list for uniform handling
        locators = [locator] if isinstance(locator, tuple) else locator

        if not locators:
            return False

        wait = WebDriverWait(self.driver, timeout)

        for loc in locators:
            try:
                wait.until(EC.element_to_be_clickable(loc))
                return True
            except TimeoutException:
                continue

        return False

    def wait_for_text(
        self,
        locator: Union[Tuple[str, str], List[Tuple[str, str]]],
        text: str,
        timeout: int = None,
    ) -> bool:
        """Wait for specific text in element

        Args:
            locator: Single locator tuple (strategy, value) or list of locator tuples to try in sequence
            text: Text to wait for
            timeout: Timeout for the wait

        Returns:
            bool: True if text is found, False otherwise
        """
        # Convert single locator to list for uniform handling
        locators = [locator] if isinstance(locator, tuple) else locator

        if not locators:
            return False

        wait_time = timeout or Settings.BROWSER.explicit_wait
        wait = WebDriverWait(self.driver, wait_time)

        for loc in locators:
            try:
                wait.until(EC.text_to_be_present_in_element(loc, text))
                return True
            except TimeoutException:
                continue

        return False

    def wait_for_element_to_disappear(
        self,
        locator: Union[Tuple[str, str], List[Tuple[str, str]]],
        timeout: int = None,
    ) -> bool:
        """Wait for element to disappear

        Args:
            locator: Single locator tuple (strategy, value) or list of locator tuples to try in sequence
            timeout: Timeout for the wait

        Returns:
            bool: True if element disappears, False otherwise
        """
        # Convert single locator to list for uniform handling
        locators = [locator] if isinstance(locator, tuple) else locator

        if not locators:
            return False

        wait_time = timeout or Settings.BROWSER.explicit_wait
        wait = WebDriverWait(self.driver, wait_time)

        for loc in locators:
            try:
                wait.until(EC.invisibility_of_element_located(loc))
                return True
            except TimeoutException:
                continue

        return False

    def scroll_to_element(
        self, locator: Union[Tuple[str, str], List[Tuple[str, str]]]
    ) -> None:
        """Scroll to an element

        Args:
            locator: Single locator tuple (strategy, value) or list of locator tuples to try in sequence
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def scroll_to_top(self) -> None:
        """Scroll to top of page"""
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_down_in_viewport(self):
        """Scroll down by one viewport height"""
        viewport_height = self.driver.execute_script("return window.innerHeight;")
        self.driver.execute_script(
            f"""
                window.scrollBy({{
                    top: {viewport_height},
                    left: 0,
                    behavior: "smooth"
                }});
            """
        )
        time.sleep(2)  # Allow time for content to load

    def is_element_within_viewport(self, element: WebElement) -> bool:
        """Check if element is within viewport"""
        try:
            return self.driver.execute_script(
                """
                var elem = arguments[0],                 box = elem.getBoundingClientRect(),
                cx = box.left + box.width / 2,         cy = box.top + box.height / 2,
                e = document.elementFromPoint(cx, cy);
                for (; e; e = e.parentElement) {
                    if (e === elem)
                        return true;
                }
                return false;
                """,
                element,
            )
        except WebDriverException:
            return False

    def switch_to_frame(self, frame_locator: Tuple[str, str]) -> None:
        """Switch to a frame"""
        frame = self.find_element(frame_locator)
        self.driver.switch_to.frame(frame)

    def switch_to_default_content(self) -> None:
        """Switch back to default content"""
        self.driver.switch_to.default_content()

    def switch_to_window(self, window_handle: str) -> None:
        """Switch to a specific window"""
        self.driver.switch_to.window(window_handle)

    def get_all_window_handles(self) -> List[str]:
        """Get all window handles"""
        return self.driver.window_handles

    def close_current_window(self) -> None:
        """Close current window"""
        self.driver.close()

    def take_screenshot(self, filename: str = None, include_device: bool = True) -> str:
        """Take a screenshot and return the file path

        Args:
            filename: Optional filename for the screenshot
            include_device: Whether to include device name in filename

        Returns:
            str: Path to the screenshot file
        """
        if not filename:
            import time

            timestamp = time.strftime("%Y%m%d_%H%M%S")

            # Try to get current device name for better filename
            device_suffix = ""
            if include_device:
                try:
                    from core.driver_manager import DriverManager

                    current_device = DriverManager.get_current_device()
                    if current_device:
                        # Convert device name to filename-safe format
                        device_suffix = f"_{current_device.lower().replace(' ', '_').replace('+', '_plus')}"
                except:
                    pass  # If we can't get device name, just continue without it

            filename = f"screenshot_{timestamp}{device_suffix}.png"

        # Ensure screenshots directory exists
        import os

        screenshot_dir = os.path.join(Settings.REPORT.report_dir, ReportConstants.SCREENSHOTS_DIR)
        os.makedirs(screenshot_dir, exist_ok=True)

        filepath = os.path.join(screenshot_dir, filename)

        try:
            self.driver.save_screenshot(filepath)
            return filepath
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
            return None

    def execute_javascript(self, script: str, *args) -> Any:
        """Execute JavaScript code"""
        return self.driver.execute_script(script, *args)

    def wait_for_page_load(self) -> None:
        """Wait for page to load completely"""
        self._wait_for_page_load()

    def refresh_page(self) -> None:
        """Refresh the current page"""
        self.driver.refresh()
        self.wait_for_page_load()

    def go_back(self) -> None:
        """Go back to previous page"""
        self.driver.back()
        self.wait_for_page_load()

    def go_forward(self) -> None:
        """Go forward to next page"""
        self.driver.forward()
        self.wait_for_page_load()

    def _wait_for_page_load(self, timeout: int = None) -> bool:
        """Internal method to wait for page to load completely

        Args:
            timeout: Optional timeout override

        Returns:
            bool: True if page loaded successfully, False otherwise
        """
        timeout = timeout or Settings.BROWSER.page_load_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
            return True
        except TimeoutException:
            return False
